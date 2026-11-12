import re

from .skill_dictionary import (
    SKILL_SYNONYMS,
    ROLE_VARIATIONS
)


def extract_skills(text):
    text_lower = text.lower()

    detected = []

    for canonical_skill, variations in SKILL_SYNONYMS.items():

        for variation in variations:

            pattern = r"(?<!\w)" + re.escape(variation) + r"(?!\w)"

            if re.search(pattern, text_lower):

                if canonical_skill not in detected:
                    detected.append(canonical_skill)

                break

    return detected


def extract_role(text):
    text_lower = text.lower()

    matches = []

    for canonical_role, variations in ROLE_VARIATIONS.items():

        for variation in variations:

            pattern = r"(?<!\w)" + re.escape(variation) + r"(?!\w)"

            if re.search(pattern, text_lower):

                matches.append(
                    (
                        canonical_role,
                        len(variation)
                    )
                )

    if not matches:
        return None

    matches.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return matches[0][0]


def extract_experience(text):
    patterns = [
        r"(\d+)\s*\+?\s*years?\s*(?:of)?\s*experience",
        r"minimum\s*(?:of\s*)?(\d+)\s*years?",
        r"at least\s*(\d+)\s*years?",
        r"(\d+)\s*-\s*(\d+)\s*years?"
    ]

    text_lower = text.lower()

    for pattern in patterns:

        match = re.search(
            pattern,
            text_lower
        )

        if match:

            if len(match.groups()) == 2:

                return {
                    "minimum_years": int(match.group(1)),
                    "maximum_years": int(match.group(2))
                }

            return {
                "minimum_years": int(match.group(1))
            }

    return None


def extract_education(text):
    text_lower = text.lower()

    education = []

    patterns = {
        "bachelor": [
            "bachelor",
            "b.tech",
            "b.e",
            "b.sc",
            "bca",
            "undergraduate"
        ],

        "master": [
            "master",
            "m.tech",
            "m.e",
            "m.sc",
            "mca",
            "postgraduate"
        ],

        "mba": [
            "mba"
        ],

        "phd": [
            "phd",
            "doctorate"
        ]
    }

    for canonical, variations in patterns.items():

        for variation in variations:

            if variation in text_lower:

                if canonical not in education:
                    education.append(canonical)

                break

    return education


def detect_required_sections(text):
    text_lower = text.lower()

    required = []

    keywords = [
        "required skills",
        "requirements",
        "qualifications",
        "must have",
        "required",
        "what you will need"
    ]

    for keyword in keywords:

        if keyword in text_lower:

            required.append(keyword)

    return required
