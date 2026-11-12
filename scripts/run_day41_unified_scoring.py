import json
from pathlib import Path

from src.unified_scoring.engine import generate_unified_score


OUTPUT_DIR = Path("outputs/day41")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


CANDIDATES = [
    {
        "candidate_id": "UC001",
        "candidate_name": "Arun Kumar",
        "target_role": "Data Analyst",
        "ats_score": 85,
        "screening_score": 80,
        "hr_interview_score": 90
    },
    {
        "candidate_id": "UC002",
        "candidate_name": "Meera Joseph",
        "target_role": "Business Analyst",
        "ats_score": 78,
        "screening_score": 88,
        "hr_interview_score": 82
    },
    {
        "candidate_id": "UC003",
        "candidate_name": "Rahul Menon",
        "target_role": "Software Developer",
        "ats_score": 90,
        "screening_score": 75,
        "hr_interview_score": 85
    },
    {
        "candidate_id": "UC004",
        "candidate_name": "Anjali Nair",
        "target_role": "Data Analyst",
        "ats_score": 80,
        "screening_score": None,
        "hr_interview_score": 88
    }
]


def main():

    print("=" * 65)
    print("DAY 41 - UNIFIED SCORING ENGINE")
    print("=" * 65)

    results = []

    for candidate in CANDIDATES:

        result = generate_unified_score(**candidate)

        results.append(result)

        print()
        print("-" * 65)

        print("Candidate:", result["candidate_name"])
        print("Role:", result["target_role"])

        print("ATS Score:", result["ats_score"])
        print("Screening Score:", result["screening_score"])
        print("HR Interview Score:", result["hr_interview_score"])

        print(
            "Unified Score:",
            result["unified_score"]
        )

        print(
            "Hiring Fit:",
            str(result["hiring_fit_percentage"]) + "%"
        )

        print(
            "Missing Components:",
            result["missing_components"]
        )

    report = {
        "day": 41,
        "module": "Unified Scoring Engine",
        "total_candidates": len(results),
        "results": results
    }

    report_path = OUTPUT_DIR / "day41_unified_scoring_report.json"

    report_path.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8"
    )

    print()
    print("=" * 65)
    print("DAY 41 DEMO COMPLETED")
    print("=" * 65)

    print("Candidates processed:", len(results))
    print("JSON Report:", report_path)


if __name__ == "__main__":
    main()
