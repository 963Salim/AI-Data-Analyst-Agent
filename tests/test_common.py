from src.subagents.common import extract_limit


class TestExtractLimit:
    """Unit tests for the extract_limit() helper function."""

    def test_no_number_returns_default(self):
        """If no number is present, the default value is returned."""
        assert extract_limit("show me some results") == 10
        assert extract_limit("no numbers here") == 10
        assert extract_limit("", default=15) == 15
        assert extract_limit("abc def ghi", default=25) == 25

    def test_number_present_returns_extracted_number(self):
        """If a number is present, this number is returned."""
        assert extract_limit("show 5 results") == 5
        assert extract_limit("I want 12 items") == 12
        assert extract_limit("give me 42 products") == 42
        assert extract_limit("3 records please") == 3

    def test_number_exceeds_max_limit_returns_max_limit(self):
        """If the number is greater than max_limit, max_limit is returned."""
        assert extract_limit("show 100 results", max_limit=50) == 50
        assert extract_limit("I want 75 items", max_limit=30) == 30
        assert extract_limit("give me 99 products", max_limit=10) == 10

    def test_zero_returns_minimum_of_one(self):
        """If the number is 0, at least 1 is returned."""
        assert extract_limit("show 0 results") == 1
        assert extract_limit("I want 0 items") == 1

    def test_custom_max_limit_allows_smaller_valid_number(self):
        """If the extracted number is below max_limit, it is returned unchanged."""
        assert extract_limit("show 7 products", max_limit=20) == 7

    def test_first_number_is_used_when_multiple_numbers_exist(self):
        """If multiple numbers are present, the first matching number is used."""
        assert extract_limit("show 5 of the top 20 products") == 5