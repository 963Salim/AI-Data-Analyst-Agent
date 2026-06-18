from typing import Any

from src.hybrid_agent import run_hybrid_agent


def run_agent(user_question: str) -> dict[str, Any]:
    """
    Central entry point for the app.

    Hybrid architecture:
    - the local LLM chooses the best sub-agent
    - the selected sub-agent chooses the concrete tool with deterministic logic
    - Python executes only controlled tools from the registry
    """
    return run_hybrid_agent(user_question)