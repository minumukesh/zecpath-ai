import json
from pathlib import Path

from src.hr_interview import (
    generate_question_bank,
    create_interview_state,
    get_current_question,
    capture_response,
    build_interview_summary,
    save_interview_report,
)


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "outputs" / "day33"


def main():
    print("=" * 68)
    print("DAY 33 - HR INTERVIEW ENGINE DESIGN")
    print("=" * 68)

    profiles = [
        ("fresher", "technical"),
        ("fresher", "non_technical"),
        ("experienced", "technical"),
        ("experienced", "non_technical"),
    ]

    print("\nROLE-BASED QUESTION GENERATION")

    for experience, role_type in profiles:
        questions = generate_question_bank(experience, role_type)
        print(
            f"{experience.upper()} | {role_type.upper()} "
            f"| Questions: {len(questions)}"
        )

    state = create_interview_state(
        candidate_id="D33-DEMO-001",
        role="Data Analyst",
        experience_level="fresher",
        role_type="technical",
    )

    print("\nSAMPLE INTERVIEW")

    first_question = get_current_question(state)
    print(f"Question ID: {first_question['question_id']}")
    print(f"Category: {first_question['category']}")
    print(f"Question: {first_question['question_text']}")

    capture_response(
        state,
        "I am a computer science graduate interested in data analytics.",
    )

    second_question = get_current_question(state)
    print(f"\nNext Question ID: {second_question['question_id']}")
    print(f"Question: {second_question['question_text']}")

    capture_response(state, "")

    summary = build_interview_summary(state)
    report_path = save_interview_report(state, OUTPUT_DIR)

    summary_path = OUTPUT_DIR / "day33_demo_summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\nINTERVIEW SUMMARY")
    print(f"Status: {summary['status']}")
    print(f"Current phase: {summary['current_phase']}")
    print(f"Questions: {summary['total_questions']}")
    print(f"Responses captured: {summary['responses_captured']}")
    print(f"Answered: {summary['answered_count']}")
    print(f"Missing: {summary['missing_count']}")
    print(f"Progress: {summary['completion_percentage']}%")

    print("\nGENERATED FILES")
    print(f"Interview report: {report_path.relative_to(ROOT)}")
    print(f"Demo summary: {summary_path.relative_to(ROOT)}")
    print(
        "Workflow documentation: "
        "docs/day33/day33_interview_flow_design.md"
    )

    print("\nDAY 33 DEMO COMPLETED")
    print("=" * 68)


if __name__ == "__main__":
    main()
