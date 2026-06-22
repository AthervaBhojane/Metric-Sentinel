from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)


def generate_metric_summary(anomalies, summary):

    prompt = f"""
You are a Senior SRE, Data Analyst and Business Intelligence expert.

Analyze the monitoring results.

Summary:
{summary}

Detected Anomalies:
{json.dumps(anomalies[:10], indent=2)}

Provide:

1. Executive Summary
2. Health Summary
3. Top 3 Key Recommendations

Return ONLY JSON.

{{
    "executive_summary": "",
    "health_summary": "",
    "recommended_actions": [
        ""
    ]
}}
"""

    response = client.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=500
    )

    content = response.choices[0].message.content.strip()

    print("\n AI SUMMARY RAW RESPONSE")
    print(content)

    try:

        if content.startswith("```json"):
            content = content.replace("```json", "")

        if content.startswith("```"):
            content = content.replace("```", "")

        if content.endswith("```"):
            content = content[:-3]

        content = content.strip()

        return json.loads(content)

    except Exception as e:

        print("AI SUMMARY PARSE ERROR:", e)

        return {
            "executive_summary":
                "AI summary generation failed.",

            "health_summary":
                "Unable to generate health summary.",

            "business_impact":
                "Unknown",

            "recommended_actions":
                ["Review anomaly report"]
        }