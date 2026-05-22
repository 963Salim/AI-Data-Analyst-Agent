from typing import Any

from src.tools import retail_summary


def handle_overview_question(question: str) -> dict[str, Any]:
    return {
        "sub_agent": "overview_agent",
        "tool": "retail_summary",
        "answer": "The Overview Agent created a general summary of the retail dataset.",
        "data": retail_summary(),
    }