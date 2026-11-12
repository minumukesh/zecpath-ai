from __future__ import annotations

import json
from pathlib import Path
from typing import Any


CATEGORIES = [
    "introduction",
    "education",
    "experience",
    "skills",
    "location",
    "salary",
    "notice_period",
]

SUPPORTED_LANGUAGES = ["en", "ml", "hi"]


ROLE_PROFILES = {
    "Data Analyst": {
        "introduction": "Please briefly introduce yourself and explain why you are interested in the Data Analyst role.",
        "education": "What is your highest qualification, and how is it relevant to data analytics?",
        "experience": "How many years of relevant experience do you have in data analysis or a similar role?",
        "skills": "Which analytics tools, programming languages, databases, or BI tools are you comfortable using?",
        "location": "What is your current location and which work locations are you comfortable with?",
        "salary": "What are your current and expected annual salary ranges for this Data Analyst role?",
        "notice_period": "What is your current notice period, and when could you join if selected?",
    },

    "Software Developer": {
        "introduction": "Please briefly introduce yourself and explain why you are interested in the Software Developer role.",
        "education": "What is your highest qualification, and how is it relevant to software development?",
        "experience": "How many years of relevant software development experience do you have?",
        "skills": "Which programming languages, frameworks, databases, or development tools are you comfortable using?",
        "location": "What is your current location and which work locations are you comfortable with?",
        "salary": "What are your current and expected annual salary ranges for this Software Developer role?",
        "notice_period": "What is your current notice period, and when could you join if selected?",
    },

    "Business Analyst": {
        "introduction": "Please briefly introduce yourself and explain why you are interested in the Business Analyst role.",
        "education": "What is your highest qualification, and how is it relevant to business analysis?",
        "experience": "How many years of relevant business analysis or requirements-related experience do you have?",
        "skills": "Which business analysis, documentation, communication, process, or reporting tools are you comfortable using?",
        "location": "What is your current location and which work locations are you comfortable with?",
        "salary": "What are your current and expected annual salary ranges for this Business Analyst role?",
        "notice_period": "What is your current notice period, and when could you join if selected?",
    },

    "HR Executive": {
        "introduction": "Please briefly introduce yourself and explain why you are interested in the HR Executive role.",
        "education": "What is your highest qualification, and how is it relevant to human resources?",
        "experience": "How many years of relevant HR, recruitment, or people-operations experience do you have?",
        "skills": "Which HR, recruitment, communication, documentation, or HRIS tools are you comfortable using?",
        "location": "What is your current location and which work locations are you comfortable with?",
        "salary": "What are your current and expected annual salary ranges for this HR Executive role?",
        "notice_period": "What is your current notice period, and when could you join if selected?",
    },
}


QUESTION_METADATA = {
    "introduction": {
        "expected_answer_type": "text",
        "mandatory": False,
        "scoring_importance": 3,
    },

    "education": {
        "expected_answer_type": "text",
        "mandatory": True,
        "scoring_importance": 3,
    },

    "experience": {
        "expected_answer_type": "number_years",
        "mandatory": True,
        "scoring_importance": 5,
    },

    "skills": {
        "expected_answer_type": "skill_list",
        "mandatory": True,
        "scoring_importance": 5,
    },

    "location": {
        "expected_answer_type": "location",
        "mandatory": True,
        "scoring_importance": 3,
    },

    "salary": {
        "expected_answer_type": "currency_range",
        "mandatory": False,
        "scoring_importance": 2,
    },

    "notice_period": {
        "expected_answer_type": "notice_period",
        "mandatory": True,
        "scoring_importance": 4,
    },
}


TEMPLATES = {
    "introduction": {
        "template_id": "intro_01",
        "template_text": "Please briefly introduce yourself and explain why you are interested in the {role} role.",
    },

    "education": {
        "template_id": "education_01",
        "template_text": "What is your highest qualification, and how is it relevant to {role}?",
    },

    "experience": {
        "template_id": "experience_01",
        "template_text": "How many years of relevant experience do you have for the {role} role?",
    },

    "skills": {
        "template_id": "skills_01",
        "template_text": "Which skills, tools, or technologies relevant to {role} are you comfortable using?",
    },

    "location": {
        "template_id": "location_01",
        "template_text": "What is your current location and which work locations are you comfortable with for the {role} role?",
    },

    "salary": {
        "template_id": "salary_01",
        "template_text": "What are your current and expected annual salary ranges for the {role} role?",
    },

    "notice_period": {
        "template_id": "notice_01",
        "template_text": "What is your current notice period, and when could you join if selected for the {role} role?",
    },
}


def _question_object(
    question_id: str,
    role: str,
    category: str,
    question: str,
) -> dict[str, Any]:

    metadata = QUESTION_METADATA[category]
    template = TEMPLATES[category]

    return {
        "question_id": question_id,
        "role": role,
        "category": category,
        "question": question,

        "language": "en",

        "supported_languages": SUPPORTED_LANGUAGES,

        "translation_key": question_id,

        "translations": {
            "ml": None,
            "hi": None,
        },

        "expected_answer_type": metadata["expected_answer_type"],

        "mandatory": metadata["mandatory"],

        "scoring_importance": metadata["scoring_importance"],

        "template_id": template["template_id"],
    }


def build_dataset() -> dict[str, Any]:

    questions = []

    number = 1

    for role, role_questions in ROLE_PROFILES.items():

        for category in CATEGORIES:

            question_id = f"HRQ{number:03d}"

            questions.append(
                _question_object(
                    question_id,
                    role,
                    category,
                    role_questions[category],
                )
            )

            number += 1

    return {
        "dataset_id": "zecpath_hr_screening_day22",

        "version": "1.0",

        "language_strategy": {
            "default_language": "en",
            "supported_languages": SUPPORTED_LANGUAGES,
            "translation_status":
                "English seed dataset; Malayalam and Hindi fields are reserved for future localization.",
        },

        "roles": list(ROLE_PROFILES.keys()),

        "categories": CATEGORIES,

        "question_count": len(questions),

        "question_category_mapping": {
            category: {
                "expected_answer_type":
                    QUESTION_METADATA[category]["expected_answer_type"],

                "mandatory":
                    QUESTION_METADATA[category]["mandatory"],

                "scoring_importance":
                    QUESTION_METADATA[category]["scoring_importance"],

                "template_id":
                    TEMPLATES[category]["template_id"],
            }

            for category in CATEGORIES
        },

        "reusable_question_templates": TEMPLATES,

        "questions": questions,
    }


def validate_dataset(dataset: dict[str, Any]) -> list[str]:

    errors = []

    questions = dataset.get("questions", [])

    if not questions:
        errors.append("Dataset contains no questions.")

    expected_roles = set(dataset.get("roles", []))

    expected_categories = set(dataset.get("categories", []))

    for index, item in enumerate(questions, start=1):

        required_fields = [
            "question_id",
            "role",
            "category",
            "question",
            "language",
            "supported_languages",
            "translation_key",
            "translations",
            "expected_answer_type",
            "mandatory",
            "scoring_importance",
            "template_id",
        ]

        for field in required_fields:

            if field not in item:
                errors.append(
                    f"Question {index}: missing field '{field}'."
                )

        if item.get("role") not in expected_roles:

            errors.append(
                f"Question {index}: invalid role."
            )

        if item.get("category") not in expected_categories:

            errors.append(
                f"Question {index}: invalid category."
            )

        if item.get("language") != "en":

            errors.append(
                f"Question {index}: base language must be 'en'."
            )

        if not isinstance(item.get("mandatory"), bool):

            errors.append(
                f"Question {index}: mandatory must be boolean."
            )

        importance = item.get("scoring_importance")

        if (
            not isinstance(importance, int)
            or not 1 <= importance <= 5
        ):

            errors.append(
                f"Question {index}: scoring_importance must be 1-5."
            )

        if not isinstance(item.get("translations"), dict):

            errors.append(
                f"Question {index}: translations must be an object."
            )

    if dataset.get("question_count") != len(questions):

        errors.append(
            "question_count does not match actual question count."
        )

    return errors


def save_dataset(
    dataset: dict[str, Any],
    output_path: str | Path,
) -> None:

    output = Path(output_path)

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output.write_text(
        json.dumps(
            dataset,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
