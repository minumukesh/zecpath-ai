import re

from .normalizer import (
    normalize_skill,
    SKILL_ALIAS_LOOKUP,
)

from .skill_dictionary import (
    ALL_SKILLS,
    SKILL_STACKS,
)


def get_skill_category(skill):
    """Return the category of a canonical skill."""

    for category, skills in ALL_SKILLS.items():
        if skill in skills:
            return category

    return "unknown"


def calculate_confidence(skill, text, source="direct"):
    """
    Calculate a rule-based confidence score between 0 and 1.
    """

    score = 0.70

    text_lower = text.lower()

    if skill.lower() in text_lower:
        score += 0.15

    if source == "synonym":
        score += 0.03

    if source == "stack":
        score += 0.05

    if "skills" in text_lower:
        score += 0.05

    return min(round(score, 2), 0.99)


def extract_skill_mentions(text):
    """
    Extract direct skills and skill synonyms from resume text.
    """

    text_lower = text.lower()

    detections = []

    for alias, canonical in SKILL_ALIAS_LOOKUP.items():

        pattern = rf"(?<!\w){re.escape(alias)}(?!\w)"

        matches = re.finditer(
            pattern,
            text_lower
        )

        for match in matches:

            source = (
                "direct"
                if alias == canonical.lower()
                else "synonym"
            )

            confidence = calculate_confidence(
                canonical,
                text,
                source
            )

            detections.append({
                "skill": canonical,
                "category": get_skill_category(canonical),
                "confidence": confidence,
                "source": source,
                "mention": match.group(0)
            })

    return detections


def extract_skill_stacks(text):
    """
    Detect technology stacks such as MERN and MEAN
    and expand them into individual skills.
    """

    text_lower = text.lower()

    detections = []

    for stack, components in SKILL_STACKS.items():

        pattern = rf"(?<!\w){re.escape(stack)}(?!\w)"

        if re.search(pattern, text_lower):

            for component in components:

                detections.append({
                    "skill": component,
                    "category": get_skill_category(component),
                    "confidence": 0.90,
                    "source": "stack",
                    "stack": stack.upper()
                })

    return detections


def deduplicate_skills(detections):
    """
    Remove duplicate skills and retain the highest-confidence
    detection.
    """

    unique = {}

    for detection in detections:

        skill = detection["skill"]

        if (
            skill not in unique
            or detection["confidence"]
            > unique[skill]["confidence"]
        ):
            unique[skill] = detection

    return sorted(
        unique.values(),
        key=lambda item: (
            -item["confidence"],
            item["skill"]
        )
    )


def extract_skills(text):
    """
    Main Skill Extraction Engine.
    """

    direct_skills = extract_skill_mentions(text)

    stack_skills = extract_skill_stacks(text)

    detections = (
        direct_skills +
        stack_skills
    )

    return deduplicate_skills(detections)
