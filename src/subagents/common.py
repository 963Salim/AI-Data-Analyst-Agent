import re


def extract_limit(text: str, default: int = 10, max_limit: int = 50) -> int:
    match = re.search(r"\b(\d+)\b", text)

    if not match:
        return default

    limit = int(match.group(1))
    return max(1, min(limit, max_limit))