from typing import Any

from src.subagents.data_quality_agent import handle_data_quality_question
from src.subagents.overview_agent import handle_overview_question
from src.subagents.returns_agent import handle_returns_question
from src.subagents.sales_agent import handle_sales_question
from src.subagents.trend_agent import handle_trend_question


def route_to_subagent(user_question: str) -> str:
    q = user_question.lower()

    if (
        "return" in q
        or "returns" in q
        or "cancellation" in q
        or "cancellations" in q
        or "negative quantity" in q
        or "rückgabe" in q
        or "retoure" in q
        or "storno" in q
    ):
        return "returns_agent"

    if (
        "month" in q
        or "monthly" in q
        or "trend" in q
        or "time" in q
        or "development" in q
        or "monat" in q
        or "zeit" in q
        or "entwicklung" in q
    ):
        return "trend_agent"

    if (
        "missing" in q
        or "null" in q
        or "nan" in q
        or "columns" in q
        or "structure" in q
        or "describe" in q
        or "overview" in q
        or "fehlende" in q
        or "spalten" in q
        or "struktur" in q
    ):
        return "data_quality_agent"

    if (
        "product" in q
        or "products" in q
        or "item" in q
        or "items" in q
        or "country" in q
        or "countries" in q
        or "market" in q
        or "markets" in q
        or "revenue" in q
        or "sales" in q
        or "umsatz" in q
        or "länder" in q
        or "land" in q
    ):
        return "sales_agent"

    return "overview_agent"


def run_agent(user_question: str) -> dict[str, Any]:
    selected_subagent = route_to_subagent(user_question)

    if selected_subagent == "returns_agent":
        result = handle_returns_question(user_question)

    elif selected_subagent == "trend_agent":
        result = handle_trend_question(user_question)

    elif selected_subagent == "data_quality_agent":
        result = handle_data_quality_question(user_question)

    elif selected_subagent == "sales_agent":
        result = handle_sales_question(user_question)

    else:
        result = handle_overview_question(user_question)

    result["agent_mode"] = "rule_based_subagent_orchestration"
    result["orchestrator_route"] = selected_subagent

    return result