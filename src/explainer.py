def generate_explanation(row, baseline_value):

    value = row["value"]

    difference = value - baseline_value
    deviation_percent = ((value - baseline_value) / baseline_value) * 100

    abs_dev = abs(deviation_percent)

    if abs_dev >= 75:
        severity = "Critical"
    elif abs_dev >= 40:
        severity = "High"
    elif abs_dev >= 20:
        severity = "Medium"
    else:
        severity = "Low"

    if deviation_percent <= -50:
        root_cause = (
            "A significant drop was detected. This may indicate a service outage, "
            "tracking failure, data ingestion issue, or sudden business decline."
        )
    elif deviation_percent >= 50:
        root_cause = (
            "A significant spike was detected. This may indicate increased user activity, "
            "marketing impact, bot traffic, or unexpected growth."
        )
    else:
        root_cause = (
            "The metric deviated noticeably from its normal behavior."
        )

    return {
        "severity": severity,
        "expected_value": round(float(baseline_value), 2),
        "difference": round(float(difference), 2),
        "deviation_percent": round(float(deviation_percent), 2),
        "root_cause": root_cause
    }