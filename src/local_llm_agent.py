import json
import os
from typing import Any

import requests
from dotenv import load_dotenv

from src.tool_registry import execute_tool, get_tool_menu


load_dotenv()


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
MAX_TOOL_STEPS = 2


def ollama_chat(
    messages: list[dict[str, str]],
    json_mode: bool = False,
    temperature: float = 0.0,
) -> str:
    """
    Sends a chat request to the local Ollama API.
    """
    payload: dict[str, Any] = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
        "keep_alive": "30m",
        "options": {
            "temperature": temperature,
            "num_predict": 120,
            "num_ctx": 2048,
        },
    }

    if json_mode:
        payload["format"] = "json"

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json=payload,
        timeout=180,
    )

    response.raise_for_status()
    data = response.json()

    return data["message"]["content"]


def parse_json_response(text: str) -> dict[str, Any]:
    """
    Parses JSON from the LLM response.
    Local models sometimes return extra text, so this function also tries to extract
    the JSON object from the response.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}") + 1

        if start == -1 or end <= start:
            raise ValueError(f"LLM did not return valid JSON: {text}")

        return json.loads(text[start:end])


