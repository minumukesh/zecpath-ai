import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "outputs" / "day9"

files = sorted(OUTPUT_DIR.glob("*_skills.json"))

all_skills = []

for file in files:
    data = json.loads(
        file.read_text(encoding="utf-8")
    )

    all_skills.extend(
        data.get("skills", [])
    )

total = len(all_skills)

high = sum(
    item["confidence"] >= 0.90
    for item in all_skills
)

medium = sum(
    0.75 <= item["confidence"] < 0.90
    for item in all_skills
)

low = sum(
    item["confidence"] < 0.75
    for item in all_skills
)

average = (
    sum(item["confidence"] for item in all_skills) / total
    if total
    else 0
)

report = f"""# Day 9 – Skill Confidence Report

## Overall Result

- Resumes processed: {len(files)}
- Total unique skill detections: {total}
- Average confidence: {average:.2f}

## Confidence Distribution

| Confidence Level | Count |
|---|---:|
| High (>= 0.90) | {high} |
| Medium (0.75 - 0.89) | {medium} |
| Low (< 0.75) | {low} |

## Confidence Scoring Logic

The Skill Extraction Engine calculates confidence using:

- Exact canonical skill matches.
- Known skill synonyms.
- Spelling normalization.
- Skill-stack detection.
- Resume context.

The confidence score ranges from 0 to 1.

## Skill Normalization

The system converts different representations into canonical skill names.

Examples:

- Python3 -> Python
- Pyhton -> Python
- PowerBI -> Power BI
- ReactJS -> React
- NodeJS -> Node.js
- Mongo DB -> MongoDB

## Skill Stack Expansion

Technology stacks are expanded into individual skills.

Example:

MERN -> MongoDB, Express.js, React, Node.js

## Deduplication

Repeated mentions of the same skill are combined into a single canonical skill entry while retaining the highest-confidence detection.

## Note

The confidence score is a rule-based confidence value and is not a statistically calibrated probability.
"""

report_file = (
    OUTPUT_DIR /
    "skill_confidence_report.md"
)

report_file.write_text(
    report,
    encoding="utf-8"
)

json_file = (
    OUTPUT_DIR /
    "skill_confidence_report.json"
)

json_file.write_text(
    json.dumps(
        {
            "resumes_processed": len(files),
            "total_skill_detections": total,
            "average_confidence": round(
                average,
                2
            ),
            "high_confidence": high,
            "medium_confidence": medium,
            "low_confidence": low
        },
        indent=2
    ),
    encoding="utf-8"
)

print("============================================")
print("DAY 9 SKILL CONFIDENCE REPORT")
print("============================================")
print(f"Resumes processed : {len(files)}")
print(f"Skill detections  : {total}")
print(f"Average confidence: {average:.2f}")
print("--------------------------------------------")
print(f"Markdown report   : {report_file}")
print(f"JSON report       : {json_file}")
print("============================================")
