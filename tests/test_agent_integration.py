from unittest.mock import MagicMock

from src.agent import run_agent


class TestRunAgentIntegration:
    """Integration tests for run_agent() with monkeypatched sub-agent handlers."""

    def test_run_agent_routes_country_question_to_sales_agent(self, monkeypatch):
        """A country question is routed to the sales agent."""
        mock_handler = MagicMock(
            return_value={
                "sub_agent": "sales_agent",
                "tool": "sales_by_country",
                "answer": "Sales by country",
                "data": [{"country": "Germany", "revenue": 50000.0}],
            }
        )

        monkeypatch.setattr("src.agent.handle_sales_question", mock_handler)

        result = run_agent("What about sales by country?")

        assert result["sub_agent"] == "sales_agent"
        assert result["tool"] == "sales_by_country"
        assert result["orchestrator_route"] == "sales_agent"
        assert result["agent_mode"] == "rule_based_subagent_orchestration"
        mock_handler.assert_called_once_with("What about sales by country?")

    def test_run_agent_routes_returns_question_to_returns_agent(self, monkeypatch):
        """A returns question is routed to the returns agent."""
        mock_handler = MagicMock(
            return_value={
                "sub_agent": "returns_agent",
                "tool": "returns_analysis",
                "answer": "Returns analysis",
                "data": {"return_rows": 15},
            }
        )

        monkeypatch.setattr("src.agent.handle_returns_question", mock_handler)

        result = run_agent("What about returns and cancellations?")

        assert result["sub_agent"] == "returns_agent"
        assert result["tool"] == "returns_analysis"
        assert result["orchestrator_route"] == "returns_agent"
        assert result["agent_mode"] == "rule_based_subagent_orchestration"
        mock_handler.assert_called_once_with("What about returns and cancellations?")

    def test_run_agent_routes_general_question_to_overview_agent(self, monkeypatch):
        """A general question is routed to the overview agent."""
        mock_handler = MagicMock(
            return_value={
                "sub_agent": "overview_agent",
                "tool": "retail_summary",
                "answer": "Overview summary",
                "data": {"total_revenue": 100000.0},
            }
        )

        monkeypatch.setattr("src.agent.handle_overview_question", mock_handler)

        result = run_agent("Hello, what can you do?")

        assert result["sub_agent"] == "overview_agent"
        assert result["tool"] == "retail_summary"
        assert result["orchestrator_route"] == "overview_agent"
        assert result["agent_mode"] == "rule_based_subagent_orchestration"
        mock_handler.assert_called_once_with("Hello, what can you do?")

    def test_run_agent_routes_product_question_to_sales_agent(self, monkeypatch):
        """A product question is routed to the sales agent."""
        mock_handler = MagicMock(
            return_value={
                "sub_agent": "sales_agent",
                "tool": "top_products_by_revenue",
                "answer": "Top products",
                "data": [{"product": "Product_A", "revenue": 25000.0}],
            }
        )

        monkeypatch.setattr("src.agent.handle_sales_question", mock_handler)

        result = run_agent("Which products have the highest revenue?")

        assert result["sub_agent"] == "sales_agent"
        assert result["tool"] == "top_products_by_revenue"
        assert result["orchestrator_route"] == "sales_agent"
        assert result["agent_mode"] == "rule_based_subagent_orchestration"
        mock_handler.assert_called_once_with("Which products have the highest revenue?")

    def test_run_agent_preserves_handler_response_data(self, monkeypatch):
        """The handler response data is preserved and metadata is added."""
        mock_data = {"Germany": 60000, "France": 55000}
        mock_handler = MagicMock(
            return_value={
                "sub_agent": "sales_agent",
                "tool": "sales_by_country",
                "answer": "Sales by country analysis",
                "data": mock_data,
            }
        )

        monkeypatch.setattr("src.agent.handle_sales_question", mock_handler)

        result = run_agent("Sales by country")

        assert result["answer"] == "Sales by country analysis"
        assert result["data"] == mock_data
        assert result["agent_mode"] == "rule_based_subagent_orchestration"
        assert result["orchestrator_route"] == "sales_agent"