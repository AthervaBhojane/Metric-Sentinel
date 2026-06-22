from fastapi import FastAPI, UploadFile, File
import pandas as pd
import shutil
import os
import uuid

from src.data_loader import load_data
from src.preprocess import preprocess_data
from src.detector import detect_anomalies
# from src.explainer import generate_explanation
from src.llm_explainer import generate_llm_explanation
from src.ai_summary import generate_metric_summary

app = FastAPI(
    title="Metric Sentinel API",
    version="1.0"
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "Metric Sentinel API Running"
}



# Upload Endpoint
@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):

    if not file.filename.endswith(".csv"):
        return {
            "status": "error",
            "message": "Only CSV files are allowed"
        }

    unique_filename = f"{uuid.uuid4()}_{file.filename}"

    filepath = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:

        df = pd.read_csv(filepath)

        required_columns = [
            "date",
            "metric_name",
            "value"
        ]

        missing = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing:

            os.remove(filepath)

            return {
                "status": "error",
                "message": f"Missing columns: {missing}"
            }

        return {
            "status": "success",
            "filename": unique_filename,
            "rows": len(df)
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }



# Analyze Endpoint
@app.post("/analyze")
async def analyze_csv(file: UploadFile = File(...)):

    if not file.filename.endswith(".csv"):
        return {
            "status": "error",
            "message": "Only CSV files are allowed"
        }

    unique_filename = f"{uuid.uuid4()}_{file.filename}"

    filepath = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:

        df = load_data(filepath)

        df = preprocess_data(df)

        result_df, model = detect_anomalies(df)

        anomalies = result_df[
            result_df["anomaly"] == -1
        ]

        baseline = result_df[
            result_df["anomaly"] == 1
        ]["value"]

        baseline_value = result_df["value"].median()

        response = []

        for _, row in anomalies.iterrows():

            metric_baseline = result_df[
                (
                    result_df["metric_name"]
                    == row["metric_name"]
                )
                &
                (
                    result_df["anomaly"] == 1
                )
            ]["value"].median()

            history = result_df[
                result_df["metric_name"]
                == row["metric_name"]
            ]["value"].tail(5).tolist()

            expected_value = float(metric_baseline)

            difference = float(
                row["value"] - metric_baseline
            )

            if metric_baseline == 0:
                deviation_percent = 0
            else:
                deviation_percent = (
                    abs(difference)
                    / metric_baseline
                    * 100
                )

            if deviation_percent >= 100:
                severity = "Critical"

            elif deviation_percent >= 50:
                severity = "High"

            elif deviation_percent >= 20:
                severity = "Medium"

            else:
                severity = "Low"

            llm_result = generate_llm_explanation(
                metric_name=row["metric_name"],
                actual_value=float(row["value"]),
                expected_value=expected_value,
                difference=difference,
                deviation_percent=deviation_percent,
                severity=severity,
                history=history
            )

            response.append({
                "metric_name": row["metric_name"],
                "date": str(row["date"]),
                "value": float(row["value"]),
                "score": float(row["anomaly_score"]),

                "severity": severity,
                "expected_value": expected_value,
                "difference": difference,
                "deviation_percent": deviation_percent,

                "root_cause": llm_result.get(
                    "root_cause",
                    "No explanation generated"
                ),
                "business_impact": llm_result.get(
                    "business_impact",
                    "N/A"
                ),
                "recommended_action": llm_result.get(
                    "recommended_action",
                    "N/A"
                )
            })

        ai_summary = generate_metric_summary(
            response,
            {
                "total_records": len(result_df),
                "anomalies_found": len(response)
            }
        )

        result = {
            "status": "success",

            "ai_summary": ai_summary,

            "summary": {
                "total_records": len(result_df),
                "normal_records": len(result_df) - len(response),
                "anomalies_found": len(response)
            },

            "anomalies": response,

            "timeseries": result_df.to_dict(
                orient="records"
            )
        }

        os.remove(filepath)

        return result

    except Exception as e:

        if os.path.exists(filepath):
            os.remove(filepath)

        return {
            "status": "error",
            "message": str(e)
        }