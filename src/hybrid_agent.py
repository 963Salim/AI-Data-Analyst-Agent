from functools import lru_cache
from typing import Any

from src.subagents.data_quality_agent import route_data_quality_tool
from src.subagents.overview_agent import route_overview_tool
from src.subagents.returns_agent import route_returns_tool
from src.subagents.sales_agent import route_sales_tool
from src.subagents.spark_agent import route_spark_tool
from src.subagents.trend_agent import route_trend_tool
from src.local_llm_agent import ollama_chat, parse_json_response
from src.tool_registry import execute_tool


VALID_SUB_AGENTS = {
    "overview_agent",
    "sales_agent",
    "trend_agent",
    "returns_agent",
    "data_quality_agent",
    "spark_agent",
}


SUB_AGENT_ALIASES = {
    "overview_llm_agent": "overview_agent",
    "overview_agent": "overview_agent",
    "overview": "overview_agent",
    "summary_agent": "overview_agent",

    "sales_llm_agent": "sales_agent",
    "sales_agent": "sales_agent",
    "sales": "sales_agent",
    "revenue_agent": "sales_agent",

    "trend_llm_agent": "trend_agent",
    "trend_agent": "trend_agent",
    "trend": "trend_agent",
    "time_series_agent": "trend_agent",

    "returns_llm_agent": "returns_agent",
    "returns_agent": "returns_agent",
    "returns": "returns_agent",
    "return_agent": "returns_agent",

    "data_quality_llm_agent": "data_quality_agent",
    "data_quality_agent": "data_quality_agent",
    "data_quality": "data_quality_agent",
    "quality_agent": "data_quality_agent",

    "spark_llm_agent": "spark_agent",
    "spark_agent": "spark_agent",
    "spark": "spark_agent",
    "pyspark_agent": "spark_agent",
    "pyspark": "spark_agent",
}


def normalize_question(question: str) -> str:
    """
    Normalizes questions so repeated questions can reuse the cached LLM sub-agent route.
    """
    return " ".join(question.lower().strip().split())


def normalize_sub_agent(sub_agent: Any) -> str:
    """
    Cleans and normalizes sub-agent names returned by the LLM.
    """
    cleaned = str(sub_agent).strip().strip("`").strip()
    cleaned = cleaned.replace("-", "_").replace(" ", "_")

    return SUB_AGENT_ALIASES.get(cleaned, cleaned)


def make_result_preview(result: Any, max_records: int = 8) -> Any:
    """
    Creates a small preview for the trace.
    The full result is still returned to the web app.
    """
    if isinstance(result, list):
        return result[:max_records]

    return result


def build_supervisor_messages(user_question: str) -> list[dict[str, str]]:
    """
    Builds a compact prompt for LLM-based sub-agent selection.

    The LLM only chooses the sub-agent.
    The concrete tool is selected later by deterministic sub-agent logic.
    """
    system_prompt = """
You are the supervisor of an AI Retail Data Analyst Agent.

Your job:
Choose exactly one specialized sub-agent for the user's analytics question.

Return JSON only in this exact structure:
{
  "sub_agent": "sales_agent",
  "reason": "brief reason"
}

Valid sub-agent values:

overview_agent:
- General summary
- High-level KPI overview
- Broad dataset overview

sales_agent:
- Revenue
- Sales by country
- Top products
- Top customers
- Average order value
- Product or customer revenue rankings

trend_agent:
- Monthly revenue
- Monthly orders
- Monthly average order value
- Revenue over time
- Time-based development

returns_agent:
- Returns
- Cancellations
- Negative quantities
- Return rates
- Returned value

data_quality_agent:
- Missing values
- Dataset structure
- Columns
- Schema
- Basic data quality checks

spark_agent:
- PySpark
- Spark
- RFM segmentation
- Customer segmentation
- Market basket analysis
- Products bought together
- Product pairs
- KPI dashboard
- Country scorecard
- Country performance comparison
- Advanced or extended data quality report
- Validation report

Rules:
- Return only valid JSON.
- Choose only one sub-agent.
- Do not choose a tool.
- Do not invent a sub-agent name.
"""

    user_prompt = f"""
User question:
{user_question}

Choose the best sub-agent.
"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


@lru_cache(maxsize=200)
def choose_sub_agent_cached(normalized_question: str) -> dict[str, Any]:
    """
    Calls Ollama once to choose the sub-agent.
    Repeated identical questions reuse the cached sub-agent route.
    """
    supervisor_messages = build_supervisor_messages(normalized_question)

    supervisor_text = ollama_chat(
        messages=supervisor_messages,
        json_mode=True,
        temperature=0.0,
    )

    return parse_json_response(supervisor_text)


def choose_sub_agent_with_llm(user_question: str) -> tuple[str, str]:
    """
    Uses the local LLM to choose a sub-agent.
    """
    normalized_question = normalize_question(user_question)
    plan = choose_sub_agent_cached(normalized_question)

    selected_sub_agent = normalize_sub_agent(plan.get("sub_agent", ""))
    reason = str(plan.get("reason", "")).strip()

    if selected_sub_agent not in VALID_SUB_AGENTS:
        selected_sub_agent = "overview_agent"
        reason = f"Invalid sub-agent returned by LLM, fallback used. Original plan: {plan}"

    return selected_sub_agent, reason


def route_tool_with_sub_agent(
    sub_agent: str,
    question: str,
) -> tuple[str, dict[str, Any]]:
    """
    Routes the question to a concrete tool using the selected sub-agent.
    """
    if sub_agent == "overview_agent":
        return route_overview_tool(question)

    if sub_agent == "sales_agent":
        return route_sales_tool(question)

    if sub_agent == "trend_agent":
        return route_trend_tool(question)

    if sub_agent == "returns_agent":
        return route_returns_tool(question)

    if sub_agent == "data_quality_agent":
        return route_data_quality_tool(question)

    if sub_agent == "spark_agent":
        return route_spark_tool(question)

    return "retail_summary", {}


def run_hybrid_agent(user_question: str) -> dict[str, Any]:
    """
    Hybrid agent flow:
    1. The local LLM chooses the best sub-agent.
    2. The selected sub-agent chooses the concrete tool using deterministic logic.
    3. Python executes the controlled tool through the tool registry.
    4. The final answer is a template response without a second LLM call.
    """
    selected_sub_agent, supervisor_reason = choose_sub_agent_with_llm(user_question)

    selected_tool, arguments = route_tool_with_sub_agent(
        sub_agent=selected_sub_agent,
        question=user_question,
    )

    tool_result = execute_tool(
        tool_name=selected_tool,
        arguments=arguments,
    )

    tool_result_preview = make_result_preview(tool_result)

    return {
        "sub_agent": selected_sub_agent,
        "tool": selected_tool,
        "agent_mode": "hybrid_supervisor_keyword_subagents",
        "orchestrator_route": selected_sub_agent,
        "answer": (
            f"{selected_sub_agent} selected the tool '{selected_tool}' "
            "and returned the corresponding analysis results."
        ),
        "data": tool_result,
        "tool_trace": [
            {
                "sub_agent": selected_sub_agent,
                "tool": selected_tool,
                "arguments": arguments,
                "result_preview": tool_result_preview,
                "supervisor_reason": supervisor_reason,
            }
        ],
    }