import json
from pathlib import Path

from src.interview_summary import (
    generate_interview_summary,
    save_interview_report,
)


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "day39" / "interview_samples.json"
OUTPUT_DIR = ROOT / "outputs" / "day39"


def main():
    with DATA_FILE.open("r", encoding="utf-8-sig") as file:
        interviews = json.load(file)

    print("=" * 70)
    print("DAY 39 - INTERVIEW SUMMARY GENERATOR")
    print("=" * 70)
    print(f"Sample interviews: {len(interviews)}")

    for interview in interviews:
        summary = generate_interview_summary(interview)
        json_path, markdown_path = save_interview_report(
            summary,
            OUTPUT_DIR,
        )

        print("-" * 70)
        print(f"Candidate: {summary['candidate']['name']}")
        print(f"Role: {summary['candidate']['role']}")
        print(
            "Overall performance: "
            f"{summary['overall_performance']['overall_score']}"
        )
        print(
            "Performance label: "
            f"{summary['overall_performance']['performance_label']}"
        )
        print(f"Strengths: {len(summary['findings']['strengths'])}")
        print(f"Weaknesses: {len(summary['findings']['weaknesses'])}")
        print(f"Risk flags: {len(summary['risk_flags'])}")
        print(
            "Possible inconsistencies: "
            f"{len(summary['inconsistencies'])}"
        )
        print(f"JSON report: {json_path.relative_to(ROOT)}")
        print(f"Markdown report: {markdown_path.relative_to(ROOT)}")
        print("")
        print("NATURAL-LANGUAGE SUMMARY")
        print(summary["natural_language_report"])

    print("-" * 70)
    print("DAY 39 DEMO COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
