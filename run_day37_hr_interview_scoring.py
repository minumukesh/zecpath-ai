import json
from pathlib import Path

from src.hr_interview_scoring import (
    score_hr_interview,
    save_interview_report,
)


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "day37" / "hr_interview_samples.json"
OUTPUT_DIR = ROOT / "outputs" / "day37"


def main():
    with DATA_FILE.open("r", encoding="utf-8-sig") as file:
        candidates = json.load(file)

    results = []

    print("=" * 70)
    print("DAY 37 - HR INTERVIEW SCORING ENGINE")
    print("=" * 70)
    print(f"Candidates to evaluate: {len(candidates)}")

    for candidate in candidates:
        result = score_hr_interview(
            candidate_id=candidate["candidate_id"],
            candidate_name=candidate["candidate_name"],
            role=candidate["role"],
            questions=candidate["questions"],
            communication_score=candidate["communication_score"],
            confidence_score=candidate["confidence_score"],
            consistency_score=candidate["consistency_score"],
        )

        results.append(result)

        print("-" * 70)
        print(
            f"Candidate: {result['candidate_name']} "
            f"({result['candidate_id']})"
        )
        print(f"Role: {result['role']}")
        print("Component breakdown:")

        for name, item in result["weighted_breakdown"].items():
            print(
                f"  {name}: score={item['score']:.2f}, "
                f"weight={item['weight']:.2f}, "
                f"contribution={item['weighted_contribution']:.2f}"
            )

        print(
            "Final HR Interview Score: "
            f"{result['final_hr_interview_score']}/100"
        )
        print(f"Score band: {result['score_classification']}")

    json_path, markdown_path = save_interview_report(
        results,
        OUTPUT_DIR,
    )

    print("-" * 70)
    print(f"JSON report: {json_path.relative_to(ROOT)}")
    print(f"Markdown report: {markdown_path.relative_to(ROOT)}")
    print("DAY 37 DEMO COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
