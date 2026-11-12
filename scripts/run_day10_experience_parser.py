import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

sys.path.insert(
    0,
    str(ROOT / "src")
)

from experience_parser import (
    parse_experience,
    calculate_total_experience,
    detect_gaps,
    detect_overlaps,
    calculate_relevance,
)


INPUT_DIR = ROOT / "data" / "experience_samples"
OUTPUT_DIR = ROOT / "outputs" / "day10"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


TARGET_ROLE = "Data Analyst"

CANDIDATE_SKILLS = [
    "python",
    "sql",
    "excel",
    "power bi",
    "data analysis",
    "statistics",
    "tableau",
    "pandas",
]


for resume_file in sorted(INPUT_DIR.glob("*.txt")):

    text = resume_file.read_text(
        encoding="utf-8"
    )

    experiences = parse_experience(text)

    total_experience = calculate_total_experience(
        experiences
    )

    gaps = detect_gaps(
        experiences
    )

    overlaps = detect_overlaps(
        experiences
    )

    relevance_scores = []

    for experience in experiences:

        score = calculate_relevance(
            experience,
            TARGET_ROLE,
            CANDIDATE_SKILLS
        )

        relevance_scores.append(score)

    output = {
        "resume_file": resume_file.name,
        "target_role": TARGET_ROLE,
        "experience_count": len(experiences),
        "total_experience": total_experience,
        "experience": experiences,
        "employment_gaps": gaps,
        "overlapping_roles": overlaps,
        "relevance_scores": relevance_scores
    }

    output_file = (
        OUTPUT_DIR
        / f"{resume_file.stem}_experience.json"
    )

    output_file.write_text(
        json.dumps(
            output,
            indent=2
        ),
        encoding="utf-8"
    )

    print(
        f"[PROCESSED] {resume_file.name}"
    )

    print(
        f"[ROLES FOUND] {len(experiences)}"
    )

    print(
        f"[TOTAL EXPERIENCE] "
        f"{total_experience['total_years']} years"
    )

    print(
        f"[GAPS] {len(gaps)}"
    )

    print(
        f"[OVERLAPS] {len(overlaps)}"
    )

    print(
        f"[OUTPUT] {output_file}"
    )

    print()


print("============================================")
print("DAY 10 EXPERIENCE PARSING COMPLETE")
print("============================================")
