from unittest.mock import MagicMock

from src.subagents.returns_agent import handle_returns_question


class TestReturnsAgent:
    """Unit tests for returns_agent.py with monkeypatching."""

    def test_handle_returns_question_returns_correct_structure(self, monkeypatch):
        """The return value contains all required keys."""
        mock_data = {"return_rows": 15, "return_percentage": 2.5}
        mock_returns_analysis = MagicMock(return_value=mock_data)

        monkeypatch.setattr(
            "src.subagents.returns_agent.returns_analysis",
            mock_returns_analysis,
        )

        result = handle_returns_question("What about returns?")

        assert "sub_agent" in result
        assert "tool" in result
        assert "answer" in result
        assert "data" in result

    def test_handle_returns_question_calls_returns_analysis(self, monkeypatch):
        """returns_analysis is called exactly once."""
        mock_returns_analysis = MagicMock(return_value={"return_rows": 10})

        monkeypatch.setattr(
            "src.subagents.returns_agent.returns_analysis",
            mock_returns_analysis,
        )

        handle_returns_question("Show returns")

        mock_returns_analysis.assert_called_once()

    def test_handle_returns_question_sets_correct_agent_name(self, monkeypatch):
        """sub_agent is always returns_agent."""
        monkeypatch.setattr(
            "src.subagents.returns_agent.returns_analysis",
            MagicMock(return_value={}),
        )

        result = handle_returns_question("Any question")

        assert result["sub_agent"] == "returns_agent"

    def test_handle_returns_question_sets_correct_tool_name(self, monkeypatch):
        """tool is always returns_analysis."""
        monkeypatch.setattr(
            "src.subagents.returns_agent.returns_analysis",
            MagicMock(return_value={}),
        )

        result = handle_returns_question("Any question")

        assert result["tool"] == "returns_analysis"

    def test_handle_returns_question_includes_mocked_data(self, monkeypatch):
        """Mocked data is included in the response."""
        mock_data = {"return_rows": 25, "return_percentage": 5.0}

        monkeypatch.setattr(
            "src.subagents.returns_agent.returns_analysis",
            MagicMock(return_value=mock_data),
        )

        result = handle_returns_question("Analyze returns")

        assert result["data"] == mock_data
        assert result["data"]["return_rows"] == 25
        
        
from unittest.mock import MagicMock

from src.subagents.overview_agent import handle_overview_question


class TestOverviewAgent:
    """Unit tests for overview_agent.py with monkeypatching."""

    def test_handle_overview_question_returns_correct_structure(self, monkeypatch):
        """The return value contains all required keys."""
        mock_data = {"total_sales": 50000, "products": 120, "countries": 8}

        monkeypatch.setattr(
            "src.subagents.overview_agent.retail_summary",
            MagicMock(return_value=mock_data),
        )

        result = handle_overview_question("Give me a summary")

        assert "sub_agent" in result
        assert "tool" in result
        assert "answer" in result
        assert "data" in result

    def test_handle_overview_question_calls_retail_summary(self, monkeypatch):
        """retail_summary is called exactly once."""
        mock_retail_summary = MagicMock(return_value={"summary": "data"})

        monkeypatch.setattr(
            "src.subagents.overview_agent.retail_summary",
            mock_retail_summary,
        )

        handle_overview_question("What can you do?")

        mock_retail_summary.assert_called_once()

    def test_handle_overview_question_sets_correct_agent_name(self, monkeypatch):
        """sub_agent is always overview_agent."""
        monkeypatch.setattr(
            "src.subagents.overview_agent.retail_summary",
            MagicMock(return_value={}),
        )

        result = handle_overview_question("Any question")

        assert result["sub_agent"] == "overview_agent"

    def test_handle_overview_question_sets_correct_tool_name(self, monkeypatch):
        """tool is always retail_summary."""
        monkeypatch.setattr(
            "src.subagents.overview_agent.retail_summary",
            MagicMock(return_value={}),
        )

        result = handle_overview_question("Any question")

        assert result["tool"] == "retail_summary"

    def test_handle_overview_question_includes_mocked_data(self, monkeypatch):
        """Mocked data is included in the response."""
        mock_data = {
            "total_sales": 75000,
            "products": 250,
            "countries": 15,
            "avg_order_value": 125,
        }

        monkeypatch.setattr(
            "src.subagents.overview_agent.retail_summary",
            MagicMock(return_value=mock_data),
        )

        result = handle_overview_question("Summarize the data")

        assert result["data"] == mock_data
        assert result["data"]["total_sales"] == 75000
        assert result["data"]["countries"] == 15
        
        
        
        
from src.subagents.trend_agent import handle_trend_question


class TestTrendAgent:
    """Unit tests for trend_agent.py with monkeypatching."""

    def test_handle_trend_question_returns_correct_structure(self, monkeypatch):
        """The return value contains all required keys."""
        mock_data = [{"month": "2011-01", "revenue": 10000.0}]

        monkeypatch.setattr(
            "src.subagents.trend_agent.monthly_revenue_trend",
            MagicMock(return_value=mock_data),
        )

        result = handle_trend_question("What is the trend?")

        assert "sub_agent" in result
        assert "tool" in result
        assert "answer" in result
        assert "data" in result

    def test_handle_trend_question_calls_monthly_revenue_trend(self, monkeypatch):
        """monthly_revenue_trend is called exactly once."""
        mock_monthly_revenue_trend = MagicMock(
            return_value=[{"month": "2011-01", "revenue": 10000.0}]
        )

        monkeypatch.setattr(
            "src.subagents.trend_agent.monthly_revenue_trend",
            mock_monthly_revenue_trend,
        )

        handle_trend_question("Show monthly development")

        mock_monthly_revenue_trend.assert_called_once()

    def test_handle_trend_question_sets_correct_agent_name(self, monkeypatch):
        """sub_agent is always trend_agent."""
        monkeypatch.setattr(
            "src.subagents.trend_agent.monthly_revenue_trend",
            MagicMock(return_value=[]),
        )

        result = handle_trend_question("Any question")

        assert result["sub_agent"] == "trend_agent"

    def test_handle_trend_question_sets_correct_tool_name(self, monkeypatch):
        """tool is always monthly_revenue_trend."""
        monkeypatch.setattr(
            "src.subagents.trend_agent.monthly_revenue_trend",
            MagicMock(return_value=[]),
        )

        result = handle_trend_question("Any question")

        assert result["tool"] == "monthly_revenue_trend"

    def test_handle_trend_question_includes_mocked_data(self, monkeypatch):
        """Mocked data is included in the response."""
        mock_data = [
            {"month": "2011-01", "revenue": 45000.0},
            {"month": "2011-02", "revenue": 48000.0},
            {"month": "2011-03", "revenue": 52000.0},
        ]

        monkeypatch.setattr(
            "src.subagents.trend_agent.monthly_revenue_trend",
            MagicMock(return_value=mock_data),
        )

        result = handle_trend_question("Analyze revenue trend")

        assert result["data"] == mock_data
        assert result["data"][0]["month"] == "2011-01"
        assert result["data"][2]["revenue"] == 52000.0
        
        
        
        
from src.subagents.data_quality_agent import handle_data_quality_question


class TestDataQualityAgent:
    """Unit tests for data_quality_agent.py with monkeypatching."""

    def test_missing_question_uses_check_missing_values(self, monkeypatch):
        """A question with 'missing' should call check_missing_values."""
        mock_data = [{"column": "customerid", "missing_values": 5}]
        mock_check_missing_values = MagicMock(return_value=mock_data)

        monkeypatch.setattr(
            "src.subagents.data_quality_agent.check_missing_values",
            mock_check_missing_values,
        )

        result = handle_data_quality_question("What are the missing values?")

        assert result["sub_agent"] == "data_quality_agent"
        assert result["tool"] == "check_missing_values"
        assert result["data"] == mock_data
        mock_check_missing_values.assert_called_once()

    def test_null_question_uses_check_missing_values(self, monkeypatch):
        """A question with 'null' should call check_missing_values."""
        mock_data = [{"column": "country", "missing_values": 10}]
        mock_check_missing_values = MagicMock(return_value=mock_data)

        monkeypatch.setattr(
            "src.subagents.data_quality_agent.check_missing_values",
            mock_check_missing_values,
        )

        result = handle_data_quality_question("How many null values exist?")

        assert result["tool"] == "check_missing_values"
        assert result["data"] == mock_data
        mock_check_missing_values.assert_called_once()

    def test_nan_question_uses_check_missing_values(self, monkeypatch):
        """A question with 'nan' should call check_missing_values."""
        mock_data = [{"column": "description", "missing_values": 3}]
        mock_check_missing_values = MagicMock(return_value=mock_data)

        monkeypatch.setattr(
            "src.subagents.data_quality_agent.check_missing_values",
            mock_check_missing_values,
        )

        result = handle_data_quality_question("Are there any NaN values?")

        assert result["tool"] == "check_missing_values"
        assert result["data"] == mock_data
        mock_check_missing_values.assert_called_once()

    def test_german_missing_question_uses_check_missing_values(self, monkeypatch):
        """A German question with 'fehlende' should call check_missing_values."""
        mock_data = [{"column": "customerid", "missing_values": 7}]
        mock_check_missing_values = MagicMock(return_value=mock_data)

        monkeypatch.setattr(
            "src.subagents.data_quality_agent.check_missing_values",
            mock_check_missing_values,
        )

        result = handle_data_quality_question("Zeige mir die fehlenden Werte")

        assert result["tool"] == "check_missing_values"
        assert result["data"] == mock_data
        mock_check_missing_values.assert_called_once()

    def test_structure_question_uses_describe_dataset(self, monkeypatch):
        """A structure-related question should call describe_dataset."""
        mock_data = {"rows": 1000, "columns": 15}
        mock_describe_dataset = MagicMock(return_value=mock_data)

        monkeypatch.setattr(
            "src.subagents.data_quality_agent.describe_dataset",
            mock_describe_dataset,
        )

        result = handle_data_quality_question("What is the structure?")

        assert result["sub_agent"] == "data_quality_agent"
        assert result["tool"] == "describe_dataset"
        assert result["data"] == mock_data
        mock_describe_dataset.assert_called_once()

    def test_overview_question_uses_describe_dataset(self, monkeypatch):
        """A question with 'overview' should call describe_dataset in the data-quality agent."""
        mock_data = {"rows": 500, "columns": 10}
        mock_describe_dataset = MagicMock(return_value=mock_data)

        monkeypatch.setattr(
            "src.subagents.data_quality_agent.describe_dataset",
            mock_describe_dataset,
        )

        result = handle_data_quality_question("Give me an overview")

        assert result["tool"] == "describe_dataset"
        assert result["data"] == mock_data
        mock_describe_dataset.assert_called_once()

    def test_missing_values_path_returns_required_keys(self, monkeypatch):
        """The missing-values path returns all required keys."""
        monkeypatch.setattr(
            "src.subagents.data_quality_agent.check_missing_values",
            MagicMock(return_value=[]),
        )

        result = handle_data_quality_question("Show missing values")

        assert "sub_agent" in result
        assert "tool" in result
        assert "answer" in result
        assert "data" in result

    def test_describe_dataset_path_returns_required_keys(self, monkeypatch):
        """The dataset-description path returns all required keys."""
        monkeypatch.setattr(
            "src.subagents.data_quality_agent.describe_dataset",
            MagicMock(return_value={"rows": 500, "columns": 10}),
        )

        result = handle_data_quality_question("Describe the dataset")

        assert "sub_agent" in result
        assert "tool" in result
        assert "answer" in result
        assert "data" in result
        
        
        
        
from src.subagents.sales_agent import handle_sales_question


class TestSalesAgent:
    """Unit tests for sales_agent.py with monkeypatching."""

    def test_country_question_uses_sales_by_country(self, monkeypatch):
        """A country-related question should call sales_by_country."""
        mock_data = [{"country": "Germany", "revenue": 50000.0}]
        mock_sales_by_country = MagicMock(return_value=mock_data)

        monkeypatch.setattr(
            "src.subagents.sales_agent.sales_by_country",
            mock_sales_by_country,
        )

        result = handle_sales_question("What about sales by country?")

        assert result["sub_agent"] == "sales_agent"
        assert result["tool"] == "sales_by_country"
        assert result["data"] == mock_data
        mock_sales_by_country.assert_called_once_with(limit=10)

    def test_market_question_uses_sales_by_country(self, monkeypatch):
        """A market-related question should call sales_by_country."""
        mock_data = [{"country": "France", "revenue": 45000.0}]
        mock_sales_by_country = MagicMock(return_value=mock_data)

        monkeypatch.setattr(
            "src.subagents.sales_agent.sales_by_country",
            mock_sales_by_country,
        )

        result = handle_sales_question("Show me market performance")

        assert result["tool"] == "sales_by_country"
        assert result["data"] == mock_data
        mock_sales_by_country.assert_called_once_with(limit=10)

    def test_country_question_passes_extracted_limit(self, monkeypatch):
        """A country question with a number should pass the extracted limit."""
        mock_sales_by_country = MagicMock(return_value=[])

        monkeypatch.setattr(
            "src.subagents.sales_agent.sales_by_country",
            mock_sales_by_country,
        )

        result = handle_sales_question("Top 5 countries by sales")

        assert result["tool"] == "sales_by_country"
        mock_sales_by_country.assert_called_once_with(limit=5)

    def test_product_question_uses_top_products_by_revenue(self, monkeypatch):
        """A product-related question should call top_products_by_revenue."""
        mock_data = [{"product": "WHITE MUG", "revenue": 10000.0}]
        mock_top_products = MagicMock(return_value=mock_data)

        monkeypatch.setattr(
            "src.subagents.sales_agent.top_products_by_revenue",
            mock_top_products,
        )

        result = handle_sales_question("What are the best products?")

        assert result["sub_agent"] == "sales_agent"
        assert result["tool"] == "top_products_by_revenue"
        assert result["data"] == mock_data
        mock_top_products.assert_called_once_with(limit=10)

    def test_item_question_uses_top_products_by_revenue(self, monkeypatch):
        """An item-related question should call top_products_by_revenue."""
        mock_data = [{"product": "RED BAG", "revenue": 8000.0}]
        mock_top_products = MagicMock(return_value=mock_data)

        monkeypatch.setattr(
            "src.subagents.sales_agent.top_products_by_revenue",
            mock_top_products,
        )

        result = handle_sales_question("Show me the top items")

        assert result["tool"] == "top_products_by_revenue"
        assert result["data"] == mock_data
        mock_top_products.assert_called_once_with(limit=10)

    def test_product_question_passes_extracted_limit(self, monkeypatch):
        """A product question with a number should pass the extracted limit."""
        mock_top_products = MagicMock(return_value=[])

        monkeypatch.setattr(
            "src.subagents.sales_agent.top_products_by_revenue",
            mock_top_products,
        )

        result = handle_sales_question("Show top 10 products by revenue")

        assert result["tool"] == "top_products_by_revenue"
        mock_top_products.assert_called_once_with(limit=10)

    def test_general_sales_question_uses_retail_summary(self, monkeypatch):
        """A general sales question should fall back to retail_summary."""
        mock_data = {"rows": 1000, "total_revenue": 100000.0}
        mock_retail_summary = MagicMock(return_value=mock_data)

        monkeypatch.setattr(
            "src.subagents.sales_agent.retail_summary",
            mock_retail_summary,
        )

        result = handle_sales_question("What about sales in general?")

        assert result["sub_agent"] == "sales_agent"
        assert result["tool"] == "retail_summary"
        assert result["data"] == mock_data
        mock_retail_summary.assert_called_once()

    def test_sales_agent_response_contains_required_keys(self, monkeypatch):
        """The sales agent response contains all required keys."""
        monkeypatch.setattr(
            "src.subagents.sales_agent.sales_by_country",
            MagicMock(return_value=[]),
        )

        result = handle_sales_question("Sales by country")

        assert "sub_agent" in result
        assert "tool" in result
        assert "answer" in result
        assert "data" in result