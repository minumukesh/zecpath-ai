import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from semantic_matching import semantic_match

INPUT_DIR = ROOT / "data" / "semantic_samples"
OUTPUT_DIR = ROOT / "outputs" / "day12"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SAMPLES = [
    (
        "resume_data_analyst.txt",
        "jd_data_analyst.txt",
        "Data Analyst"
    ),
    (
        "resume_software_developer.txt",
        "jd_software_developer.txt",
        "Software Developer"
    ),
    (
        "resume_ml_engineer.txt",
        "jd_ml_engineer.txt",
        "Machine Learning Engineer"
    ),
]

results = []

for resume_name, jd_name, job_type in SAMPLES:

    resume_text = (
        INPUT_DIR / resume_name
    ).read_text(encoding="utf-8")

    jd_text = (
        INPUT_DIR / jd_name
    ).read_text(encoding="utf-8")

    result = semantic_match(
        resume_text,
        jd_text
    )

    results.append({
        "job_type": job_type,
        "resume": resume_name,
        "job_description": jd_name,
        "result": result
    })

    print(f"[MATCHED] {job_type}")
    print(f"Overall similarity    : {result['overall_similarity']}")
    print(f"Skills similarity     : {result['skills_similarity']}")
    print(f"Experience similarity : {result['experience_similarity']}")
    print(f"Projects similarity   : {result['projects_similarity']}")
    print(f"Match score           : {result['match_score']}")
    print(f"Category              : {result['match_category']}")
    print("--------------------------------------------")


output_file = OUTPUT_DIR / "semantic_matching_results.json"

output_file.write_text(
    json.dumps(results, indent=2),
    encoding="utf-8"
)

print("============================================")
print("DAY 12 SEMANTIC MATCHING COMPLETE")
print("============================================")
print(f"Job types validated : {len(results)}")
print(f"Output              : {output_file}")
print("============================================")
