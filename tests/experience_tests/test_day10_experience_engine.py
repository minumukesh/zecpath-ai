import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.experience_parser.parser import (
    parse_experience,
    calculate_total_experience,
    detect_gaps,
    detect_overlaps,
)

from src.experience_parser.relevance import (
    calculate_relevance,
)


print("=" * 70)
print("DAY 10 - EXPERIENCE PARSING & RELEVANCE ENGINE")
print("=" * 70)


# ============================================================
# TEST 1 - EXPERIENCE PARSING
# ============================================================

resume_text = """
Data Analyst
Jan 2021 - Dec 2022
ABC Analytics

Business Analyst
Jan 2023 - Jun 2024
XYZ Solutions
"""

experiences = parse_experience(resume_text)

print("\n[1] EXPERIENCE PARSING")
print("-" * 70)

for experience in experiences:
    print(json.dumps(experience, indent=4))


# ============================================================
# TEST 2 - TOTAL EXPERIENCE
# ============================================================

total_experience = calculate_total_experience(experiences)

print("\n[2] TOTAL EXPERIENCE")
print("-" * 70)

print(json.dumps(total_experience, indent=4))


# ============================================================
# TEST 3 - GAP DETECTION
# ============================================================

gap_resume = """
Data Analyst
Jan 2020 - Dec 2021
ABC Analytics

Business Analyst
Jul 2022 - Dec 2023
XYZ Solutions
"""

gap_experiences = parse_experience(gap_resume)

gaps = detect_gaps(gap_experiences)

print("\n[3] EMPLOYMENT GAP DETECTION")
print("-" * 70)

if gaps:
    print(json.dumps(gaps, indent=4))
else:
    print("No employment gaps detected.")


# ============================================================
# TEST 4 - OVERLAPPING ROLE DETECTION
# ============================================================

overlap_resume = """
Data Analyst
Jan 2021 - Dec 2023
ABC Analytics

Business Analyst
Jan 2023 - Jun 2024
XYZ Solutions
"""

overlap_experiences = parse_experience(overlap_resume)

overlaps = detect_overlaps(overlap_experiences)

print("\n[4] OVERLAPPING ROLE DETECTION")
print("-" * 70)

if overlaps:
    print(json.dumps(overlaps, indent=4))
else:
    print("No overlapping roles detected.")


# ============================================================
# TEST 5 - ROLE-TO-ROLE RELEVANCE
# ============================================================

target_role = "Data Analyst"

candidate_skills = [
    "python",
    "sql",
    "excel",
    "power bi",
    "tableau",
    "data analysis",
    "statistics",
]

relevance = calculate_relevance(
    experiences[0],
    target_role,
    candidate_skills,
)

print("\n[5] ROLE-TO-ROLE RELEVANCE")
print("-" * 70)

print(json.dumps(relevance, indent=4))


# ============================================================
# TEST 6 - FINAL STRUCTURED EXPERIENCE OBJECT
# ============================================================

structured_output = {
    "candidate_id": "DAY10_TEST_001",
    "experiences": experiences,
    "total_experience": total_experience,
    "employment_gaps": gaps,
    "overlapping_roles": overlaps,
    "target_role": target_role,
    "relevance": relevance,
}

print("\n[6] STRUCTURED EXPERIENCE OBJECT")
print("-" * 70)

print(json.dumps(structured_output, indent=4))


print("\n" + "=" * 70)
print("DAY 10 EXPERIENCE ENGINE TEST COMPLETED")
print("=" * 70)