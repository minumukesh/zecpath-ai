import json
from pathlib import Path

from src.fairness_normalization import (
    normalize_resume,
    generate_fairness_evaluation,
)


DATA_DIR = Path("data/fairness_samples")
OUTPUT_DIR = Path("outputs/day15")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

sample_candidates = [
    {
        "candidate_name": "Candidate 01",
        "resume_file": "resume_fairness_01.txt",
        "original_score": 82.0,
        "keyword_score": 0.90,
        "semantic_score": 0.82,
        "experience_score": 0.85,
        "education_score": 0.80,
    },
    {
        "candidate_name": "Candidate 02",
        "resume_file": "resume_fairness_02.txt",
        "original_score": 78.0,
        "keyword_score": 0.75,
        "semantic_score": 0.84,
        "experience_score": 0.80,
        "education_score": 0.78,
    },
    {
        "candidate_name": "Candidate 03",
        "resume_file": "resume_fairness_03.txt",
        "original_score": 74.0,
        "keyword_score": 0.65,
        "semantic_score": 0.86,
        "experience_score": 0.88,
        "education_score": 0.75,
    },
]


results = []

for candidate in sample_candidates:

    resume_path = DATA_DIR / candidate["resume_file"]

    with open(
        resume_path,
        "r",
        encoding="utf-8"
    ) as file:
        resume_text = file.read()

    normalized = normalize_resume(resume_text)

    evaluation = generate_fairness_evaluation(
        candidate_name=candidate["candidate_name"],
        original_score=candidate["original_score"],
        keyword_score=candidate["keyword_score"],
        semantic_score=candidate["semantic_score"],
        experience_score=candidate["experience_score"],
        education_score=candidate["education_score"],
        masked_attributes=normalized["masked_attributes"],
    )

    evaluation["normalization"] = normalized

    results.append(evaluation)


output_file = OUTPUT_DIR / "fairness_evaluation.json"

with open(
    output_file,
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        results,
        file,
        indent=2
    )


print("DAY 15 FAIRNESS EVALUATION COMPLETED")
print()
print(f"Candidates evaluated: {len(results)}")

for result in results:
    print(
        f"{result['candidate_name']} | "
        f"Original: {result['original_ats_score']} | "
        f"Fairness-adjusted: "
        f"{result['fairness_adjusted_score']}"
    )

print()
print(f"Output saved to: {output_file}")
