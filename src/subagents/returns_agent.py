from typing import Any

from src.tools import returns_analysis


def handle_returns_question(question: str) -> dict[str, Any]:
    return {
        "sub_agent": "returns_agent",
        "tool": "returns_analysis",
        "answer": "The Returns Agent analyzed returns, cancellations and negative quantities.",
        "data": returns_analysis(),
    }