from pprint import pprint
from typing import Any

import pandas as pd

from src.agent import run_agent


def print_result(data: Any) -> None:
    if isinstance(data, list):
        if not data:
            print("No records found.")
            return

        df = pd.DataFrame(data)
        print(df.to_string(index=False))
        return

    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{key}: {value}")
        return

    pprint(data)


def main():
    print("AI Retail Data Analyst Agent")
    print("Type a question about the retail dataset.")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("Question: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        result = run_agent(question)

        print("\nTool used:")
        print(result["tool"])

        print("\nAnswer:")
        print(result["answer"])

        print("\nResult:")
        print_result(result["data"])

        print("\n" + "-" * 80 + "\n")


if __name__ == "__main__":
    main()