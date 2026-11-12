import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

sys.path.insert(0, str(ROOT / "src"))

from education_certification import (
    extract_education,
    extract_certifications,
    education_relevance,
)


INPUT_DIR = ROOT / "data" / "education_samples"
OUTPUT_DIR = ROOT / "outputs" / "day11"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

TARGET_ROLE = "Data Analyst"


for resume_file in sorted(INPUT_DIR.glob("*.txt")):

    text = resume_file.read_text(
        encoding="utf-8"
    )

    education = extract_education(text)

    certifications = extract_certifications(text)

    relevance = education_relevance(
        education,
        TARGET_ROLE
    )

    output = {
        "resume_file": resume_file.name,
        "target_role": TARGET_ROLE,

        "academic_profile": {
            "education_count": len(education),
            "education": education
        },

        "certifications": {
            "certification_count": len(certifications),
            "items": certifications
        },

        "education_relevance": relevance
    }

    output_file = (
        OUTPUT_DIR
        / f"{resume_file.stem}_education_profile.json"
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
        f"[EDUCATION] {len(education)} record(s)"
    )

    print(
        f"[CERTIFICATIONS] {len(certifications)}"
    )

    print(
        f"[RELEVANCE] {relevance['score']}"
    )

    print(
        f"[OUTPUT] {output_file}"
    )

    print()


print("============================================")
print("DAY 11 EDUCATION PARSING COMPLETE")
print("============================================")
