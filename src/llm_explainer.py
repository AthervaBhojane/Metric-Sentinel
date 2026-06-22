from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)


def generate_llm_explanation(
    metric_name,
    actual_value,
    expected_value,
    difference,
    deviation_percent,
    severity,
    history
):

    prompt = f"""
You are a senior Site Reliability Engineer,
Business Analyst and Data Scientist.

Analyze this anomaly.

Metric:
{metric_name}

Severity:
{severity}

Actual Value:
{actual_value}

Expected Value:
{expected_value}

Difference:
{difference}

Deviation:
{deviation_percent:.2f}%

Recent Values:
{history}

Explain:

1. Root Cause
2. Business Impact
3. Recommended Action

Return ONLY JSON.

{{
    "root_cause": "",
    "business_impact": "",
    "recommended_action": ""
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
        max_tokens=300
    )

    content = response.choices[0].message.content.strip()

    print("\n LLM RAW RESPONSE")
    print(content)

    try:

        if content.startswith("```json"):
            content = content.replace(
                "```json",
                ""
            )

        if content.startswith("```"):
            content = content.replace(
                "```",
                ""
            )

        if content.endswith("```"):
            content = content[:-3]

        content = content.strip()

        return json.loads(content)

    except Exception as e:

        print("JSON PARSE ERROR:", e)

        return {
            "root_cause": content,
            "business_impact": "N/A",
            "recommended_action": "N/A"
        }