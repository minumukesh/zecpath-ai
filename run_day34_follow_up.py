import json
from pathlib import Path

from src.dynamic_follow_up import run_demo_cases, save_report


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "day34" / "follow_up_test_cases.json"
OUTPUT_DIR = ROOT / "outputs" / "day34"


def main():
    with DATA_FILE.open("r", encoding="utf-8-sig") as file:
        cases = json.load(file)

    report = run_demo_cases(cases)
    json_path, markdown_path = save_report(report, OUTPUT_DIR)
--
    print("=" * 68)
    print("DAY 34 - DYNAMIC FOLLOW-UP LOGIC")
    print("=" * 68)
    print(f"Sample cases processed: {report['total_cases']}")

    for item in report["results"]:
        result = item["result"]
        print("-" * 52)
        print(f"Scenario: {item['scenario']}")
        print(f"Answer status: {result['answer_quality']['status']}")
        print(f"Trigger: {result['trigger']}")
        print(f"Follow-up: {result['follow_up_question']}")
        print(
            "Human review recommended: "
            f"{result['human_review_recommended']}"
        )

    print("-" * 52)
    print(f"JSON report: {json_path.relative_to(ROOT)}")
    print(f"Markdown report: {markdown_path.relative_to(ROOT)}")
    print("DAY 34 DEMO COMPLETED")
    print("=" * 68)


if __name__ == "__main__":
    main()
