import json
from pathlib import Path

from src.hr_interview_simulation import (
    generate_test_report,
    save_report,
)


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "day40" / "hr_interview_cases.json"
OUTPUT_DIR = ROOT / "outputs" / "day40"


def main():
    with DATA_FILE.open("r", encoding="utf-8-sig") as file:
        candidates = json.load(file)

    report = generate_test_report(candidates)
    json_path, markdown_path = save_report(report, OUTPUT_DIR)

    print("=" * 70)
    print("DAY 40 - HR INTERVIEW SIMULATION")
    print("=" * 70)

    print(f"Simulated interview sessions: {report['total_simulations']}")
    print("Candidate types: Confident, Hesitant, Inexperienced, Overqualified")
    print("")

    for result in report["results"]:
        print("-" * 70)
        print(
            f"{result['candidate_id']} | "
            f"{result['candidate_type']}"
        )
        print(f"AI score: {result['ai_final_score']}")
        print(f"Manual expected score: {result['manual_expected_score']}")
        print(f"AI decision: {result['ai_performance_label']}")
        print(f"Manual decision: {result['manual_decision']}")
        print(f"Score difference: {result['score_difference']}")
        print(f"Evaluation status: {result['evaluation_status']}")
        print(f"Inconsistencies: {result['inconsistencies']}")

    print("")
    print("=" * 70)
    print("EVALUATION METRICS")
    print("=" * 70)

    for name, value in report["metrics"].items():
        print(f"{name}: {value}")

    print("")
    print("IMPROVEMENT RECOMMENDATIONS")

    for index, recommendation in enumerate(
        report["improvement_recommendations"], start=1
    ):
        print(f"{index}. {recommendation}")

    print("")
    print(f"JSON report: {json_path.relative_to(ROOT)}")
    print(f"Markdown report: {markdown_path.relative_to(ROOT)}")
    print("")
    print("DAY 40 DEMO COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
