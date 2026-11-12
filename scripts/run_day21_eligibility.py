"""
Day 21 - Eligibility Decision Engine Demo
"""

import json
from pathlib import Path

from src.eligibility_decision.engine import EligibilityDecisionEngine
from src.eligibility_decision.rules import ROLE_RULES


OUTPUT_DIR = Path("outputs/day21")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

engine = EligibilityDecisionEngine(ROLE_RULES)


TEST_CASES = [

    {
        "candidate_id": "ED001",
        "candidate_name": "Arun Kumar",
        "role": "Data Analyst",
        "ats_score": 82,
        "skills": [
            "Python",
            "SQL",
            "Excel",
            "Pandas",
            "Power BI"
        ],
        "experience_years": 1,
        "location": "Kochi",
        "available": True
    },

    {
        "candidate_id": "ED002",
        "candidate_name": "Rahul Menon",
        "role": "Data Analyst",
        "ats_score": 64,
        "skills": [
            "Python",
            "SQL",
            "Excel"
        ],
        "experience_years": 2,
        "location": "Kochi",
        "available": True
    },

    {
        "candidate_id": "ED003",
        "candidate_name": "Meera Joseph",
        "role": "Data Analyst",
        "ats_score": 78,
        "skills": [
            "Python",
            "Excel"
        ],
        "experience_years": 1,
        "location": "Thrissur",
        "available": True
    },

    {
        "candidate_id": "ED004",
        "candidate_name": "Anjali Nair",
        "role": "Senior Data Analyst",
        "ats_score": 81,
        "skills": [
            "Python",
            "SQL",
            "Power BI",
            "Tableau"
        ],
        "experience_years": 5,
        "location": "Kochi",
        "available": True
    },

    {
        "candidate_id": "ED005",
        "candidate_name": "Vishnu Raj",
        "role": "Senior Data Analyst",
        "ats_score": 80,
        "skills": [
            "Python",
            "SQL",
            "Excel"
        ],
        "experience_years": 5,
        "location": "Kochi",
        "available": True
    }
]


results = []

print("=" * 70)
print("DAY 21 - ELIGIBILITY DECISION ENGINE")
print("=" * 70)

for candidate in TEST_CASES:

    result = engine.evaluate_candidate(
        candidate,
        candidate["role"]
    )

    results.append(result)

    print()
    print("-" * 70)
    print(f"CANDIDATE ID       : {result['candidate_id']}")
    print(f"CANDIDATE NAME     : {result['candidate_name']}")
    print(f"ROLE               : {result['role']}")
    print(f"ATS SCORE          : {result['ats_score']}")
    print(f"DECISION           : {result['decision']}")
    print(
        f"AI SCREENING       : "
        f"{'YES' if result['eligible_for_ai_screening'] else 'NO'}"
    )

    print()
    print("RULE CHECKS")

    for rule_name, rule_result in result["rule_checks"].items():
        print(
            f"  {rule_name:<20}: "
            f"{'PASS' if rule_result['passed'] else 'FAIL'}"
        )

    if result["failed_rules"]:
        print(
            "FAILED RULES       : "
            + ", ".join(result["failed_rules"])
        )
    else:
        print("FAILED RULES       : None")


report = {
    "day": 21,
    "title": "Eligibility Decision Engine",
    "total_candidates": len(results),
    "results": results,
    "decision_summary": {
        "eligible": sum(
            r["decision"] == "ELIGIBLE"
            for r in results
        ),
        "review": sum(
            r["decision"] == "REVIEW"
            for r in results
        ),
        "rejected": sum(
            r["decision"] == "REJECTED"
            for r in results
        )
    }
}

report_path = OUTPUT_DIR / "day21_eligibility_report.json"

with open(report_path, "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4)

print()
print("=" * 70)
print("DAY 21 ELIGIBILITY TESTING COMPLETE")
print("=" * 70)
print()
print(f"Report: {report_path.resolve()}")
print("=" * 70)
