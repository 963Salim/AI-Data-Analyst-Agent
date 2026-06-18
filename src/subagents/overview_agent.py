from typing import Any


def route_overview_tool(question: str) -> tuple[str, dict[str, Any]]:
    """
    Overview sub-agent:
    Handles broad summary and high-level overview questions.
    """
    q = question.lower()

    if "describe" in q or "columns" in q or "structure" in q or "schema" in q:
        return "describe_dataset", {}

    return "retail_summary", {}