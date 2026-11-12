import json
from pathlib import Path

from src.ats_scoring import generate_candidate_score


OUTPUT_DIR = Path("outputs/day13")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

candidates = [
    {
        "candidate_name": "Candidate 01",
        "role": "Data Analyst",
        "skill_match": 0.95,
        "experience_relevance": 0.85,
        "education_alignment": 0.90,
        "semantic_similarity": 0.88,
    },
    {
        "candidate_name": "Candidate 02",
        "role": "Software Developer",
        "skill_match": 0.92,
        "experience_relevance": 0.90,
        "education_alignment": 0.80,
        "semantic_similarity": 0.86,
    },
    {
        "candidate_name": "Candidate 03",
        "role": "Machine Learning Engineer",
        "skill_match": 0.88,
        "experience_relevance": 0.82,
        "education_alignment": 0.85,
        "semantic_similarity": 0.90,
    },
    {
        "candidate_name": "Candidate 04",
        "role": "Data Analyst",
        "skill_match": 0.75,
        "experience_relevance": None,
        "education_alignment": 0.80,
        "semantic_similarity": 0.70,
    },
]

results = []

for candidate in candidates:
    result = generate_candidate_score(**candidate)
    results.append(result)

output_file = OUTPUT_DIR / "candidate_scores.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("Day 13 ATS scoring completed.")
print(f"Output saved to: {output_file}")
