import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from src.agent import run_agent as run_rule_based_agent
from src.tools import (
    check_missing_values,
    describe_dataset,
    monthly_revenue_trend,
    retail_summary,
    returns_analysis,
    sales_by_country,
    top_products_by_revenue,
)


load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


AVAILABLE_TOOLS = {
    "retail_summary": {
        "description": "General summary of the retail dataset, including rows, orders, revenue, products, customers and countries.",
        "function": retail_summary,
        "accepts_limit": False,
    },
    "describe_dataset": {
        "description": "Structural overview of the dataset, including columns, numeric columns and categorical columns.",
        "function": describe_dataset,
        "accepts_limit": False,
    },
    "check_missing_values": {
        "description": "Check if the cleaned retail dataset contains missing values.",
        "function": check_missing_values,
        "accepts_limit": False,
    },
    "top_products_by_revenue": {
        "description": "Find products with the highest revenue.",
        "function": top_products_by_revenue,
        "accepts_limit": True,
    },
    "sales_by_country": {
        "description": "Summarize revenue, quantity and order count by country.",
        "function": sales_by_country,
        "accepts_limit": True,
    },
    "monthly_revenue_trend": {
        "description": "Analyze monthly revenue development over time.",
        "function": monthly_revenue_trend,
        "accepts_limit": False,
    },
    "returns_analysis": {
        "description": "Analyze product returns and cancellations.",
        "function": returns_analysis,
        "accepts_limit": False,
    },
}


def _extract_json(text: str) -> dict[str, Any]:
    """
    Extracts the first JSON object from a model response.
    This makes the parser more robust if the model accidentally adds text.
    """
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"No valid JSON object found in model response: {text}")

    return json.loads(text[start:end + 1])


def choose_tool_with_llm(user_question: str) -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    client = OpenAI(api_key=api_key)

    tool_descriptions = "\n".join(
        f"- {tool_name}: {tool_info['description']}"
        for tool_name, tool_info in AVAILABLE_TOOLS.items()
    )

    system_prompt = f"""
You are a tool-routing agent for a retail analytics application.

Your task:
- Understand the user's question.
- Select exactly one tool from the allowed tool list.
- Do not invent tools.
- Do not write SQL.
- Do not execute code.
- Return only valid JSON.

Allowed tools:
{tool_descriptions}

JSON schema:
{{
  "tool": "one of the allowed tool names",
  "limit": 10,
  "reason": "short explanation why this tool was selected"
}}

Rules:
- Use "top_products_by_revenue" for product ranking or highest revenue products.
- Use "sales_by_country" for country, market, geography or country-level sales questions.
- Use "monthly_revenue_trend" for month, time, trend or revenue development questions.
- Use "returns_analysis" for returns, cancellations or negative quantity questions.
- Use "check_missing_values" for missing values, nulls or data quality questions.
- Use "describe_dataset" for columns, structure or dataset overview questions.
- Use "retail_summary" for general summary questions.
- If the user asks for a number of results, put it into "limit".
- If no limit is mentioned, use 10.
"""

    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_question,
            },
        ],
    )

    raw_text = response.output_text.strip()
    decision = _extract_json(raw_text)

    tool_name = decision.get("tool")
    limit = decision.get("limit", 10)
    reason = decision.get("reason", "")

    if tool_name not in AVAILABLE_TOOLS:
        raise ValueError(f"Model selected an invalid tool: {tool_name}")

    try:
        limit = int(limit)
    except (TypeError, ValueError):
        limit = 10

    limit = max(1, min(limit, 50))

    return {
        "tool": tool_name,
        "limit": limit,
        "reason": reason,
    }


def run_llm_agent(user_question: str) -> dict[str, Any]:
    """
    LLM-based agent controller.

    The LLM only selects one allowed tool.
    The actual analysis is executed by local, controlled Python functions.
    If the OpenAI API is unavailable, the function falls back to the rule-based agent.
    """
    try:
        decision = choose_tool_with_llm(user_question)

        tool_name = decision["tool"]
        limit = decision["limit"]
        reason = decision["reason"]

        tool_info = AVAILABLE_TOOLS[tool_name]
        tool_function = tool_info["function"]

        if tool_info["accepts_limit"]:
            data = tool_function(limit=limit)
        else:
            data = tool_function()

        return {
            "tool": tool_name,
            "answer": f"Selected tool: {tool_name}. {reason}",
            "data": data,
            "agent_mode": "llm_tool_router",
        }

    except Exception as exc:
        fallback_result = run_rule_based_agent(user_question)
        fallback_result["agent_mode"] = "rule_based_fallback"
        fallback_result["answer"] = (
            f"{fallback_result['answer']} "
            f"The rule-based fallback was used because the LLM router was unavailable: {exc}"
        )
        return fallback_result