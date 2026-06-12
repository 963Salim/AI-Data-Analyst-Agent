from src.agent import route_to_subagent


class TestRouteToSubagent:
    """Unit tests for the routing function route_to_subagent()."""

    def test_returns_question_routes_to_returns_agent(self):
        """A returns-related question should route to returns_agent."""
        assert route_to_subagent("What are the latest returns?") == "returns_agent"
        assert route_to_subagent("How many cancellations happened?") == "returns_agent"
        assert route_to_subagent("Zeige mir alle Retouren") == "returns_agent"

    def test_trend_question_routes_to_trend_agent(self):
        """A time- or trend-related question should route to trend_agent."""
        assert route_to_subagent("How does monthly revenue develop?") == "trend_agent"
        assert route_to_subagent("Show the revenue trend over time") == "trend_agent"
        assert route_to_subagent("Zeige mir die monatliche Entwicklung") == "trend_agent"

    def test_data_quality_question_routes_to_data_quality_agent(self):
        """A data-quality-related question should route to data_quality_agent."""
        assert route_to_subagent("Are there missing values?") == "data_quality_agent"
        assert route_to_subagent("Describe the dataset structure") == "data_quality_agent"
        assert route_to_subagent("Welche Spalten gibt es?") == "data_quality_agent"

    def test_sales_or_country_question_routes_to_sales_agent(self):
        """A sales-, revenue-, market- or country-related question should route to sales_agent."""
        assert route_to_subagent("What are the sales by country?") == "sales_agent"
        assert route_to_subagent("Show revenue in each market") == "sales_agent"
        assert route_to_subagent("Welche Länder haben die höchsten Umsätze?") == "sales_agent"

    def test_general_question_routes_to_overview_agent(self):
        """A general question without specific keywords should route to overview_agent."""
        assert route_to_subagent("Hello") == "overview_agent"
        assert route_to_subagent("What can you do?") == "overview_agent"
        assert route_to_subagent("Give me a summary") == "overview_agent"