import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "outputs" / "day12"

result_file = OUTPUT_DIR / "semantic_matching_results.json"

data = json.loads(
    result_file.read_text(encoding="utf-8")
)

total = len(data)

strong = sum(
    1
    for item in data
    if item["result"]["match_category"] == "strong_match"
)

average_score = (
    sum(
        item["result"]["match_score"]
        for item in data
    ) / total
    if total
    else 0
)

report = f"""# Day 12 – Semantic Matching Accuracy Report

## Overall Result

- Job types evaluated: {total}
- Strong matches: {strong}
- Average matching score: {average_score:.2f}

## Matching Results

| Job Type | Overall Similarity | Skills | Experience | Projects | Match Score | Category |
|---|---:|---:|---:|---:|---:|---|
"""

for item in data:

    result = item["result"]

    report += (
        f"| {item['job_type']} "
        f"| {result['overall_similarity']:.4f} "
        f"| {result['skills_similarity']:.4f} "
        f"| {result['experience_similarity']:.4f} "
        f"| {result['projects_similarity']:.4f} "
        f"| {result['match_score']:.4f} "
        f"| {result['match_category']} |\\n"
    )


report += f"""

## Semantic Matching Method

The system converts resume and job-description text into normalized
vector representations and calculates cosine similarity.

The matching engine evaluates:

- Complete resume-to-JD similarity
- Skills similarity
- Experience similarity
- Project similarity

## Weighted Matching

The section-level score uses the following weights:

- Skills: 45%
- Experience: 35%
- Projects: 20%

The final score combines:

- Overall resume-JD similarity: 30%
- Weighted section similarity: 70%

## Similarity Thresholds

| Score | Classification |
|---:|---|
| 0.70 and above | Strong Match |
| 0.50 – 0.69 | Good Match |
| 0.30 – 0.49 | Partial Match |
| Below 0.30 | Low Match |

## Job Types Validated

The engine was validated across:

1. Data Analyst
2. Software Developer
3. Machine Learning Engineer

## Deliverables

- Semantic matching engine
- Resume-to-JD similarity scorer
- Section-level similarity scoring
- Similarity threshold logic
- Multi-job validation dataset
- Matching results in JSON
- Matching accuracy report

## Limitations

The current implementation uses a lightweight local vector representation
rather than a pretrained transformer embedding model. This provides a
reproducible baseline but may not capture deeper language semantics,
synonyms, or contextual relationships as effectively as modern
transformer-based embeddings.

## Future Improvements

- Sentence Transformer embeddings
- Transformer-based semantic similarity
- Domain-specific embeddings
- Cross-encoder ranking
- Larger validation datasets
- Human-labeled matching benchmarks
- Threshold optimization using validation data

## Final Outcome

The Day 12 Semantic Matching Engine successfully provides resume-to-job
similarity scoring beyond simple keyword matching and evaluates skills,
experience, and project descriptions across multiple job types.
"""

report_file = (
    OUTPUT_DIR /
    "semantic_matching_accuracy_report.md"
)

report_file.write_text(
    report,
    encoding="utf-8"
)

print("============================================")
print("DAY 12 ACCURACY REPORT GENERATED")
print("============================================")
print(f"Job types evaluated : {total}")
print(f"Strong matches      : {strong}")
print(f"Average score       : {average_score:.2f}")
print("--------------------------------------------")
print(f"Report              : {report_file}")
print("============================================")
