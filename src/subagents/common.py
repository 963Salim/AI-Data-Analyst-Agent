import re


def extract_limit_from_question(
    question: str,
    default: int = 10,
    max_limit: int = 100,
) -> int:
    """
    Extracts limits from questions like:
    - top 10
    - top 20
    - first 5
    - limit 15
    - 10 rows
    """
    match = re.search(
        r"(?:top|first|limit)\s+(\d+)|(\d+)\s+rows",
        question.lower(),
    )

    if not match:
        return default

    for group in match.groups():
        if group:
            return max(1, min(int(group), max_limit))

    return default


def extract_country_from_question(question: str) -> str | None:
    """
    Extracts known country names for country-specific tools.
    """
    known_countries = [
        "United Kingdom",
        "Germany",
        "France",
        "Netherlands",
        "EIRE",
        "Spain",
        "Switzerland",
        "Belgium",
        "Portugal",
        "Australia",
        "Norway",
        "Italy",
        "Channel Islands",
        "Finland",
        "Cyprus",
        "Sweden",
        "Austria",
        "Denmark",
        "Japan",
        "Poland",
        "USA",
        "Canada",
    ]

    q = question.lower()

    for country in known_countries:
        if country.lower() in q:
            return country

    return None