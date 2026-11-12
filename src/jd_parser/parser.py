import json
from pathlib import Path
from datetime import datetime

from .normalizer import normalize_text
from .extractor import (
    extract_skills,
    extract_role,
    extract_experience,
    extract_education,
    detect_required_sections
)


def parse_job_description(file_path):

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Job description not found: {file_path}"
        )

    if path.suffix.lower() != ".txt":
        raise ValueError(
            "Currently only .txt job descriptions are supported."
        )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        raw_text = file.read()

    normalized_text = normalize_text(raw_text)

    result = {

        "metadata": {
            "file_name": path.name,
            "file_type": "TXT",
            "processed_at": datetime.now().isoformat()
        },

        "job_profile": {

            "role_name": extract_role(
                normalized_text
            ),

            "required_skills": extract_skills(
                normalized_text
            ),

            "experience": extract_experience(
                normalized_text
            ),

            "education_preferences": extract_education(
                normalized_text
            ),

            "requirement_sections": detect_required_sections(
                normalized_text
            ),

            "normalized_description": normalized_text
        }
    }

    return result


def save_parsed_jd(result, output_directory):

    output_dir = Path(output_directory)

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    file_name = result["metadata"]["file_name"]

    output_name = (
        Path(file_name).stem
        + ".json"
    )

    output_path = output_dir / output_name

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            result,
            file,
            indent=4,
            ensure_ascii=False
        )

    return str(output_path)
