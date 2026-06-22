# Metric Sentinel

## AI-Powered Anomaly Detection & Root Cause Analysis Platform

Metric Sentinel is an intelligent monitoring platform that detects anomalies in business and system metrics using Machine Learning and generates AI-powered explanations to help identify potential root causes. The platform provides interactive visualizations, anomaly severity analysis, health scoring, and downloadable reports through a user-friendly dashboard.

---

## Features

* Automated anomaly detection using Isolation Forest
* AI-generated anomaly explanations
* Root cause analysis for detected anomalies
* Severity classification (Low, Medium, High, Critical)
* System health scoring
* Interactive Streamlit dashboard
* Metric trend visualization
* PDF and CSV report generation
* FastAPI backend for data processing
* LLM-powered executive summaries

---

## Technology Stack

### Backend

* Python
* FastAPI

### Machine Learning

* Scikit-learn
* Isolation Forest

### Data Processing

* Pandas
* NumPy

### Frontend

* Streamlit
* Plotly

### AI Layer

* Large Language Models (LLM)

---

## Dataset Format

Input CSV must contain:

| Column      | Description         |
| ----------- | ------------------- |
| date        | Timestamp of metric |
| metric_name | Name of metric      |
| value       | Metric value        |

Example:

```csv
date,metric_name,value
2026-01-01,signups,500
2026-01-02,signups,510
2026-01-03,signups,495
```

---

## How It Works

1. Upload a CSV dataset.
2. Data preprocessing and validation.
3. Isolation Forest model analyzes each metric.
4. Anomalies are detected and scored.
5. Root causes and severity levels are generated.
6. LLM creates executive summaries.
7. Results are displayed on the dashboard.
8. Reports can be downloaded as PDF or CSV.

---

## Running the Project

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start FastAPI Backend

```bash
uvicorn api.main:app --reload
```

### Start Dashboard

```bash
streamlit run dashboard.py
```

---

## Sample Output

The dashboard provides:

* Total Records
* Anomaly Count
* Health Score
* AI Insights
* Root Cause Analysis
* Trend Visualizations
* Downloadable Reports

---

## Machine Learning Approach

Metric Sentinel uses the Isolation Forest algorithm for unsupervised anomaly detection.

The model:

* Learns normal behavior patterns
* Identifies isolated observations
* Assigns anomaly scores
* Flags abnormal metric values

Each metric is analyzed independently to improve detection accuracy.
