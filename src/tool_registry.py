from typing import Any, Callable

from src.tools import (
    average_order_value_by_country,
    check_missing_values,
    describe_dataset,
    monthly_average_order_value,
    monthly_orders_trend,
    monthly_revenue_trend,
    retail_summary,
    return_rate_by_country,
    return_rate_by_product,
    returns_analysis,
    revenue_by_country_and_month,
    sales_by_country,
    top_customers_by_revenue,
    top_products_by_country,
    top_products_by_revenue,
)

from src.cached_spark_tools import (
    spark_basket_product_pairs,
    spark_country_performance_scorecard,
    spark_customer_rfm_segmentation,
    spark_data_quality_report,
    spark_monthly_kpi_dashboard,
)


ToolFunction = Callable[..., Any]


TOOL_REGISTRY: dict[str, dict[str, Any]] = {
    # -------------------------
    # Pandas tools
    # -------------------------
    "retail_summary": {
        "function": retail_summary,
        "description": "Creates a general KPI summary of the retail dataset.",
        "allowed_arguments": {},
    },
    "describe_dataset": {
        "function": describe_dataset,
        "description": "Shows dataset structure, columns, numeric columns and categorical columns.",
        "allowed_arguments": {},
    },
    "check_missing_values": {
        "function": check_missing_values,
        "description": "Checks the cleaned dataset for missing values.",
        "allowed_arguments": {},
    },
    "sales_by_country": {
        "function": sales_by_country,
        "description": "Shows revenue, quantity and orders by country.",
        "allowed_arguments": {
            "limit": {"type": "int", "default": 10, "min": 1, "max": 50},
        },
    },
    "top_products_by_revenue": {
        "function": top_products_by_revenue,
        "description": "Shows the top products ranked by revenue across the full dataset.",
        "allowed_arguments": {
            "limit": {"type": "int", "default": 10, "min": 1, "max": 50},
        },
    },
    "top_products_by_country": {
        "function": top_products_by_country,
        "description": (
            "Shows the top products ranked by revenue for one specific country. "
            "Use this tool when the user asks for top products in a specific country, "
            "for example Germany, France or United Kingdom."
        ),
        "allowed_arguments": {
            "country": {
                "type": "str",
                "default": None,
                "required": True,
                "max_length": 100,
            },
            "limit": {"type": "int", "default": 10, "min": 1, "max": 50},
        },
    },
    "top_customers_by_revenue": {
        "function": top_customers_by_revenue,
        "description": "Shows the top customers ranked by revenue.",
        "allowed_arguments": {
            "limit": {"type": "int", "default": 10, "min": 1, "max": 50},
        },
    },
    "average_order_value_by_country": {
        "function": average_order_value_by_country,
        "description": "Shows average order value by country.",
        "allowed_arguments": {
            "limit": {"type": "int", "default": 10, "min": 1, "max": 50},
        },
    },
    "monthly_revenue_trend": {
        "function": monthly_revenue_trend,
        "description": "Shows monthly revenue, quantity and order count across the full dataset.",
        "allowed_arguments": {},
    },
    "monthly_orders_trend": {
        "function": monthly_orders_trend,
        "description": "Shows monthly order development.",
        "allowed_arguments": {},
    },
    "monthly_average_order_value": {
        "function": monthly_average_order_value,
        "description": "Shows monthly average order value development.",
        "allowed_arguments": {},
    },
    "revenue_by_country_and_month": {
        "function": revenue_by_country_and_month,
        "description": (
            "Shows monthly revenue, quantity and orders for one specific country, "
            "or for all countries if no country is provided. Use this when the user "
            "asks how revenue develops over time in a specific country."
        ),
        "allowed_arguments": {
            "country": {
                "type": "str",
                "default": None,
                "required": False,
                "max_length": 100,
            },
            "limit": {"type": "int", "default": 100, "min": 1, "max": 500},
        },
    },
    "returns_analysis": {
        "function": returns_analysis,
        "description": "Analyzes returns, return rows, returned quantity and return value.",
        "allowed_arguments": {},
    },
    "return_rate_by_product": {
        "function": return_rate_by_product,
        "description": "Shows products with the highest return rates.",
        "allowed_arguments": {
            "limit": {"type": "int", "default": 10, "min": 1, "max": 50},
        },
    },
    "return_rate_by_country": {
        "function": return_rate_by_country,
        "description": "Shows return rates by country.",
        "allowed_arguments": {
            "limit": {"type": "int", "default": 10, "min": 1, "max": 50},
        },
    },

    # -------------------------
    # PySpark tools
    # -------------------------
    "spark_customer_rfm_segmentation": {
        "function": spark_customer_rfm_segmentation,
        "description": "Creates an RFM customer segmentation using PySpark.",
        "allowed_arguments": {
            "limit": {"type": "int", "default": 20, "min": 1, "max": 100},
        },
    },
    "spark_basket_product_pairs": {
        "function": spark_basket_product_pairs,
        "description": "Finds product pairs that are often bought together using PySpark.",
        "allowed_arguments": {
            "limit": {"type": "int", "default": 20, "min": 1, "max": 100},
            "min_pair_count": {"type": "int", "default": 2, "min": 1, "max": 100},
        },
    },
    "spark_monthly_kpi_dashboard": {
        "function": spark_monthly_kpi_dashboard,
        "description": (
            "Creates a monthly KPI dashboard with revenue, orders, customers, "
            "average order value and return metrics using PySpark."
        ),
        "allowed_arguments": {},
    },
    "spark_country_performance_scorecard": {
        "function": spark_country_performance_scorecard,
        "description": (
            "Creates a country performance scorecard with revenue, average order value, "
            "return rate and ranks using PySpark."
        ),
        "allowed_arguments": {
            "limit": {"type": "int", "default": 20, "min": 1, "max": 100},
        },
    },
    "spark_data_quality_report": {
        "function": spark_data_quality_report,
        "description": (
            "Creates an extended Spark data quality report with missing values, "
            "distinct values and validation checks."
        ),
        "allowed_arguments": {},
    },
}


def get_tool_menu() -> list[dict[str, Any]]:
    """
    Returns a compact tool menu for the local LLM planner.
    The LLM sees names, descriptions and allowed arguments, but not the Python functions.
    """
    return [
        {
            "name": tool_name,
            "description": tool_data["description"],
            "allowed_arguments": tool_data["allowed_arguments"],
        }
        for tool_name, tool_data in TOOL_REGISTRY.items()
    ]


def coerce_int_argument(
    value: Any,
    default: int,
    min_value: int,
    max_value: int,
) -> int:
    try:
        value = int(value)
    except (TypeError, ValueError):
        value = default

    return max(min_value, min(value, max_value))


def coerce_string_argument(
    value: Any,
    default: str | None = None,
    required: bool = False,
    max_length: int = 100,
) -> str | None:
    if value is None:
        if required:
            raise ValueError("Missing required string argument.")
        return default

    cleaned = str(value).strip()

    if not cleaned:
        if required:
            raise ValueError("Missing required string argument.")
        return default

    return cleaned[:max_length]


def sanitize_arguments(tool_name: str, arguments: dict[str, Any] | None) -> dict[str, Any]:
    """
    Keeps only allowed arguments and converts them to safe types.
    This prevents the LLM from passing unexpected parameters into Python functions.
    """
    if tool_name not in TOOL_REGISTRY:
        raise ValueError(f"Unknown tool: {tool_name}")

    arguments = arguments or {}
    allowed_arguments = TOOL_REGISTRY[tool_name]["allowed_arguments"]

    sanitized: dict[str, Any] = {}

    for argument_name, rules in allowed_arguments.items():
        argument_type = rules.get("type")

        if argument_type == "int":
            sanitized[argument_name] = coerce_int_argument(
                value=arguments.get(argument_name, rules["default"]),
                default=rules["default"],
                min_value=rules["min"],
                max_value=rules["max"],
            )

        elif argument_type == "str":
            sanitized[argument_name] = coerce_string_argument(
                value=arguments.get(argument_name, rules.get("default")),
                default=rules.get("default"),
                required=rules.get("required", False),
                max_length=rules.get("max_length", 100),
            )

    return sanitized


def execute_tool(tool_name: str, arguments: dict[str, Any] | None = None) -> Any:
    """
    Executes one allowed tool from the registry.
    """
    if tool_name not in TOOL_REGISTRY:
        raise ValueError(f"Unknown tool: {tool_name}")

    sanitized_arguments = sanitize_arguments(tool_name, arguments)
    tool_function: ToolFunction = TOOL_REGISTRY[tool_name]["function"]

    return tool_function(**sanitized_arguments)