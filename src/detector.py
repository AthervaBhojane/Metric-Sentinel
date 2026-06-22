from sklearn.ensemble import IsolationForest
from src.model_manager import save_model, load_model
import pandas as pd


def detect_anomalies(df):

    all_results = []

    metrics = df["metric_name"].unique()

    for metric in metrics:

        metric_df = df[
            df["metric_name"] == metric
        ].copy()

        model = IsolationForest(
            contamination=0.04,
            random_state=42
        )

        model.fit(
            metric_df[["value"]]
        )

        metric_df["anomaly"] = model.predict(
            metric_df[["value"]]
        )

        metric_df["anomaly_score"] = (
            model.decision_function(
                metric_df[["value"]]
            )
        )

        all_results.append(metric_df)

    result_df = pd.concat(
        all_results,
        ignore_index=True
    )

    return result_df, None