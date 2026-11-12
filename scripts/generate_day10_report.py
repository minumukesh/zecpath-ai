import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "outputs" / "day10"

files = sorted(OUTPUT_DIR.glob("*_experience.json"))

total_resumes = len(files)
total_roles = 0
total_gaps = 0
total_overlaps = 0
scores = []

for file in files:
    data = json.loads(
        file.read_text(encoding="utf-8")
    )

    total_roles += data.get("experience_count", 0)
    total_gaps += len(data.get("employment_gaps", []))
    total_overlaps += len(data.get("overlapping_roles", []))

    for item in data.get("relevance_scores", []):
        scores.append(item["relevance_score"])

average_score = (
    sum(scores) / len(scores)
    if scores else 0
)

report = f"""# Day 10 – Experience Parsing & Relevance Report

## Overall Result

- Resumes processed: {total_resumes}
- Experience records extracted: {total_roles}
- Employment gaps detected: {total_gaps}
- Overlapping roles detected: {total_overlaps}
- Average relevance score: {average_score:.2f}

## Experience Information Extracted

The parser extracts:

- Company names
- Job titles
- Canonical roles
- Employment start dates
- Employment end dates
- Employment duration
- Total professional experience

## Gap and Overlap Detection

The system compares employment periods chronologically to identify:

- Employment gaps
- Overlapping employment periods

## Relevance Scoring

Experience relevance is calculated using:

| Component | Weight |
|---|---:|
| Role similarity | 50% |
| Skill relevance | 30% |
| Experience duration | 20% |

The final relevance score ranges from 0 to 1.

## Role Normalization

Different job-title variations are mapped to canonical roles.

Examples:

- Software Engineer → software developer
- Data Analyst Intern → data analyst
- Junior Data Analyst → data analyst
- ML Engineer → machine learning engineer

## Structured Experience Object

Each experience record is stored in JSON format containing:

- Company
- Job title
- Canonical role
- Start date
- End date
- Duration in months
- Duration in years

## Limitations

The current implementation is rule-based and depends on recognized job-title patterns and date formats.

Complex resume layouts, unusual titles, missing dates, and ambiguous company names may require advanced NLP techniques.

## Future Improvements

- NLP-based Named Entity Recognition
- Transformer-based role classification
- Semantic role embeddings
- Advanced company recognition
- PDF/DOCX layout analysis
- Machine-learning-based relevance scoring
"""

md_file = OUTPUT_DIR / "experience_relevance_report.md"
json_file = OUTPUT_DIR / "experience_relevance_report.json"

md_file.write_text(report, encoding="utf-8")

json_file.write_text(
    json.dumps(
        {
            "resumes_processed": total_resumes,
            "experience_records": total_roles,
            "employment_gaps": total_gaps,
            "overlapping_roles": total_overlaps,
            "average_relevance_score": round(
                average_score, 2
            )
        },
        indent=2
    ),
    encoding="utf-8"
)

print("============================================")
print("DAY 10 EXPERIENCE REPORT GENERATED")
print("============================================")
print(f"Resumes processed : {total_resumes}")
print(f"Experience records: {total_roles}")
print(f"Gaps detected     : {total_gaps}")
print(f"Overlaps detected : {total_overlaps}")
print(f"Average relevance : {average_score:.2f}")
print("--------------------------------------------")
print(f"Markdown report   : {md_file}")
print(f"JSON report       : {json_file}")
print("============================================")
