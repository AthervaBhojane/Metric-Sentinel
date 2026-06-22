import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from io import BytesIO
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

API_URL = "http://localhost:8000/analyze"

st.set_page_config(
    page_title="Metric Sentinel",
    layout="wide"
)

st.title("Metric Sentinel")
st.caption(
    "AI-Powered Metric Monitoring & Root Cause Analysis"
)

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)




# Analyze Button
if uploaded_file:

    if st.button("Analyze Metrics"):

        with st.spinner("Analyzing data..."):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "text/csv"
                )
            }

            response = requests.post(
                API_URL,
                files=files
            )

            result = response.json()

            st.session_state["result"] = result




# Results
if "result" in st.session_state:

    result = st.session_state["result"]

    if result["status"] == "success":

        summary = result["summary"]

        st.success("Analysis Complete")

        anomaly_rate = (
            summary["anomalies_found"]
            / summary["total_records"]
        ) * 100

        health_score = max(
            0,
            100 - anomaly_rate
        )

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric(
            "Total Records",
            summary["total_records"]
        )

        col2.metric(
            "Normal Records",
            summary["normal_records"]
        )

        col3.metric(
            "Anomalies",
            summary["anomalies_found"]
        )

        col4.metric(
            "Anomaly Rate",
            f"{anomaly_rate:.1f}%"
        )

        col5.metric(
            "Health Score",
            f"{health_score:.1f}/100"
        )

        

        # AI INSIGHTS
        if "ai_summary" in result:

            ai = result["ai_summary"]

            st.subheader("Executive Summary")

            st.info(
                ai["executive_summary"]
            )

            st.markdown(
                "### System Health"
            )

            st.write(
                ai["health_summary"]
            )

            st.markdown(
                "### Priority Actions"
            )

            for action in ai[
                "recommended_actions"
            ]:

                st.write(
                    f"• {action}"
                )



        # PDF REPORT DOWNLOAD
        pdf_buffer = BytesIO()

        doc = SimpleDocTemplate(
            pdf_buffer
        )

        styles = getSampleStyleSheet()

        content = []

        content.append(
            Paragraph(
                "Metric Sentinel Report",
                styles["Title"]
            )
        )

        content.append(
            Spacer(1, 12)
        )

        content.append(
            Paragraph(
                f"Total Records: {summary['total_records']}",
                styles["BodyText"]
            )
        )

        content.append(
            Paragraph(
                f"Anomalies Found: {summary['anomalies_found']}",
                styles["BodyText"]
            )
        )

        content.append(
            Paragraph(
                f"Health Score: {health_score:.1f}/100",
                styles["BodyText"]
            )
        )

        content.append(
            Spacer(1, 12)
        )

        if "ai_summary" in result:

            content.append(
                Paragraph(
                    "Executive Summary",
                    styles["Heading2"]
                )
            )

            content.append(
                Paragraph(
                    ai["executive_summary"],
                    styles["BodyText"]
                )
            )

        doc.build(content)

        pdf_buffer.seek(0)

        st.download_button(
            label="Download AI Report (PDF)",
            data=pdf_buffer,
            file_name="metric_sentinel_report.pdf",
            mime="application/pdf"
        )



        # AI ANOMALY ANALYSIS
        anomalies = result["anomalies"]

        if anomalies:

            st.subheader(
                "Detected Anomalies"
            )

            for anomaly in anomalies:

                severity = anomaly["severity"]

                if severity == "Critical":
                    icon = "🔴"

                elif severity == "High":
                    icon = "🟠"

                elif severity == "Medium":
                    icon = "🟡"

                else:
                    icon = "🟢"

                with st.expander(
                    f"{icon} {anomaly['metric_name']} | {severity}"
                ):

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "Actual Value",
                            round(
                                anomaly["value"],
                                2
                            )
                        )

                        st.metric(
                            "Expected Value",
                            round(
                                anomaly["expected_value"],
                                2
                            )
                        )

                    with col2:

                        st.metric(
                            "Difference",
                            round(
                                anomaly["difference"],
                                2
                            )
                        )

                        st.metric(
                            "Deviation %",
                            round(
                                anomaly["deviation_percent"],
                                2
                            )
                        )

                    st.markdown("---")

                    st.markdown(
                        "### Root Cause"
                    )

                    st.write(
                        anomaly["root_cause"]
                    )

                    st.markdown(
                        "### Business Impact"
                    )

                    st.write(
                        anomaly["business_impact"]
                    )

                    st.markdown(
                        "### Recommended Action"
                    )

                    st.write(
                        anomaly["recommended_action"]
                    )



            # CSV DOWNLOAD
            anomaly_df = pd.DataFrame(
                anomalies
            )

            csv = anomaly_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="Download Anomaly Report (CSV)",
                data=csv,
                file_name="anomaly_report.csv",
                mime="text/csv"
            )

        else:

            st.info(
                "No anomalies detected."
            )

        st.divider()




        # TIME SERIES
        timeseries_df = pd.DataFrame(
            result["timeseries"]
        )

        timeseries_df["date"] = pd.to_datetime(
            timeseries_df["date"]
        )

        metrics = sorted(
            timeseries_df[
                "metric_name"
            ].unique()
        )



        # METRIC SELECTOR
        selected_metric = st.selectbox(
            "Select Metric",
            metrics
        )

        selected_df = timeseries_df[
            timeseries_df["metric_name"]
            == selected_metric
        ]

        st.subheader(
            f"{selected_metric} Trend"
        )

        fig = px.line(
            selected_df,
            x="date",
            y="value",
            markers=True
        )

        anomalies_selected = selected_df[
            selected_df["anomaly"] == -1
        ]

        fig.add_scatter(
            x=anomalies_selected["date"],
            y=anomalies_selected["value"],
            mode="markers",
            name="Anomaly",
            marker=dict(
                color="red",
                size=12
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()



        # TREND COMPARISON
        st.subheader(
            "Metric Comparison"
        )

        comparison_df = (
            timeseries_df
            .pivot(
                index="date",
                columns="metric_name",
                values="value"
            )
            .reset_index()
        )

        comparison_fig = px.line(
            comparison_df,
            x="date",
            y=comparison_df.columns[1:]
        )

        st.plotly_chart(
            comparison_fig,
            use_container_width=True
        )

        st.divider()



        # SEPARATE CHART FOR EACH METRIC
        st.subheader(
            "All Metric Trends"
        )

        for metric in metrics:

            metric_df = timeseries_df[
                timeseries_df["metric_name"]
                == metric
            ]

            st.markdown(
                f"### {metric}"
            )

            metric_fig = px.line(
                metric_df,
                x="date",
                y="value",
                markers=True
            )

            metric_anomalies = metric_df[
                metric_df["anomaly"] == -1
            ]

            metric_fig.add_scatter(
                x=metric_anomalies["date"],
                y=metric_anomalies["value"],
                mode="markers",
                name="Anomaly",
                marker=dict(
                    color="red",
                    size=10
                )
            )

            st.plotly_chart(
                metric_fig,
                use_container_width=True
            )

        st.divider()

        