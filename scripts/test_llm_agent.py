import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.llm_agent import run_llm_agent


questions = [
    "Which products generate the highest revenue?",
    "Show the top 5 countries by revenue.",
    "How does monthly revenue develop?",
    "Are there missing values in the dataset?",
    "Analyze returns and cancellations.",
    "Give me a general summary of the retail dataset.",
]


for question in questions:
    print("\nQuestion:")
    print(question)

    result = run_llm_agent(question)

    print("\nAgent mode:")
    print(result.get("agent_mode"))

    print("\nTool:")
    print(result["tool"])

    print("\nAnswer:")
    print(result["answer"])

    print("\nData preview:")
    data = result["data"]

    if isinstance(data, list):
        print(data[:3])
    else:
        print(data)

    print("\n" + "-" * 80)