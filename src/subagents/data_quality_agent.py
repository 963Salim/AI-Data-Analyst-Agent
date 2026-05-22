from typing import Any

from src.tools import check_missing_values, describe_dataset


def handle_data_quality_question(question: str) -> dict[str, Any]:
    q = question.lower()

    if (
        "missing" in q
        or "null" in q
        or "nan" in q
        or "fehlende" in q
        or "missing values" in q
    ):
        return {
            "sub_agent": "data_quality_agent",
            "tool": "check_missing_values",
            "answer": "The Data Quality Agent checked the cleaned dataset for missing values.",
            "data": check_missing_values(),
        }

    return {
        "sub_agent": "data_quality_agent",
        "tool": "describe_dataset",
        "answer": "The Data Quality Agent created a structural overview of the dataset.",
        "data": describe_dataset(),
    }