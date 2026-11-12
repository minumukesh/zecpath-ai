from pathlib import Path
import json

from src.hr_screening_dataset.dataset_builder import (
    build_dataset,
    save_dataset,
    validate_dataset,
)


ROOT = Path(__file__).resolve().parent

DATA_DIR = (
    ROOT
    / "data"
    / "day22_hr_screening"
)

OUTPUT_DIR = (
    ROOT
    / "outputs"
    / "day22"
)


def main():

    dataset = build_dataset()

    errors = validate_dataset(dataset)


    if errors:

        print("=" * 70)

        print(
            "DAY 22 - HR SCREENING DATASET CREATION"
        )

        print("VALIDATION: FAILED")

        for error in errors:
            print(f"- {error}")

        raise SystemExit(1)


    dataset_path = (
        DATA_DIR
        / "hr_screening_questions.json"
    )

    mapping_path = (
        DATA_DIR
        / "question_category_mapping.json"
    )

    templates_path = (
        DATA_DIR
        / "reusable_question_templates.json"
    )

    report_path = (
        OUTPUT_DIR
        / "day22_hr_screening_report.json"
    )


    save_dataset(
        dataset,
        dataset_path,
    )


    mapping_path.write_text(
        json.dumps(
            dataset["question_category_mapping"],
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


    templates_path.write_text(
        json.dumps(
            dataset["reusable_question_templates"],
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


    report = {

        "day": 22,

        "title":
            "HR Screening Dataset Creation",

        "status":
            "COMPLETED",

        "roles":
            dataset["roles"],

        "categories":
            dataset["categories"],

        "question_count":
            dataset["question_count"],

        "supported_languages":
            dataset["language_strategy"]
            ["supported_languages"],

        "validation": {
            "status": "PASSED",
            "errors": [],
        },

        "deliverables": {

            "hr_screening_question_dataset":
                str(
                    dataset_path.relative_to(ROOT)
                ),

            "question_category_mapping":
                str(
                    mapping_path.relative_to(ROOT)
                ),

            "ai_conversation_ready_question_objects":
                str(
                    dataset_path.relative_to(ROOT)
                ),

            "reusable_question_templates":
                str(
                    templates_path.relative_to(ROOT)
                ),
        },
    }


    report_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


    report_path.write_text(
        json.dumps(
            report,
            indent=2,
        ),
        encoding="utf-8",
    )


    print("=" * 70)

    print(
        "DAY 22 - HR SCREENING DATASET CREATION"
    )

    print("=" * 70)

    print(
        f"Roles              : "
        f"{len(dataset['roles'])}"
    )

    print(
        f"Categories         : "
        f"{len(dataset['categories'])}"
    )

    print(
        f"Questions          : "
        f"{dataset['question_count']}"
    )

    print(
        f"Languages          : "
        f"{', '.join(dataset['language_strategy']['supported_languages'])}"
    )

    print(
        "Validation         : PASSED"
    )

    print()

    print(
        "Question category mapping:"
    )


    for category, details in (
        dataset["question_category_mapping"]
        .items()
    ):

        required = (
            "Mandatory"
            if details["mandatory"]
            else "Optional"
        )

        print(
            f"  {category:15} | "
            f"{details['expected_answer_type']:16} | "
            f"{required:9} | "
            f"importance="
            f"{details['scoring_importance']}"
        )


    print()

    print(
        "Deliverables generated:"
    )

    print(
        f"  - {dataset_path}"
    )

    print(
        f"  - {mapping_path}"
    )

    print(
        f"  - {templates_path}"
    )

    print(
        f"  - {report_path}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()
