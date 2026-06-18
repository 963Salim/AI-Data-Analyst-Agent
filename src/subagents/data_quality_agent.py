from typing import Any


def route_data_quality_tool(question: str) -> tuple[str, dict[str, Any]]:
    """
    Data quality sub-agent:
    Handles missing values, schema and basic data checks.
    """
    q = question.lower()

    if "missing" in q or "null" in q or "nan" in q:
        return "check_missing_values", {}

    return "describe_dataset", {}