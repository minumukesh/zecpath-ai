# ============================================================
# ZECPATH AI - DAY 9
# RULE-BASED SKILL EXTRACTION ENGINE
# ============================================================

import re

from parsers.skill_dictionary import (
    SKILL_DICTIONARY,
    SKILL_STACKS,
    NORMALIZATION_MAP
)


# ============================================================
# CONFIDENCE RULES
# ============================================================

EXACT_CONFIDENCE = 1.00
ALIAS_CONFIDENCE = 0.90
STACK_CONFIDENCE = 0.95


# ============================================================
# GET CATEGORY
# ============================================================

def get_category(skill):

    for category, skills in SKILL_DICTIONARY.items():

        if skill in skills:
            return category

    return "unknown"


# ============================================================
# NORMALIZE SKILL
# ============================================================

def normalize_skill(skill):

    return NORMALIZATION_MAP.get(
        skill.strip().lower()
    )


# ============================================================
# EXTRACT DICTIONARY SKILLS
# ============================================================

def extract_dictionary_skills(text):

    results = []

    text_lower = text.lower()

    entries = []

    for category, skills in SKILL_DICTIONARY.items():

        for canonical, aliases in skills.items():

            entries.append(
                (
                    canonical,
                    aliases
                )
            )

    # Longer phrases first
    entries.sort(
        key=lambda item: max(
            len(x)
            for x in [item[0]] + item[1]
        ),
        reverse=True
    )

    occupied = []

    for canonical, aliases in entries:

        candidates = [canonical] + aliases

        for candidate in candidates:

            pattern = (
                r"(?<![a-zA-Z0-9])"
                + re.escape(candidate.lower())
                + r"(?![a-zA-Z0-9])"
            )

            for match in re.finditer(
                pattern,
                text_lower
            ):

                start = match.start()
                end = match.end()

                # Avoid overlapping matches
                overlap = False

                for old_start, old_end in occupied:

                    if (
                        start < old_end
                        and end > old_start
                    ):

                        overlap = True
                        break

                if overlap:
                    continue

                occupied.append(
                    (start, end)
                )

                source_text = text[
                    start:end
                ]

                # Canonical skill
                if (
                    source_text.lower()
                    == canonical.lower()
                ):

                    confidence = EXACT_CONFIDENCE

                # Alias / variation
                else:

                    confidence = ALIAS_CONFIDENCE

                results.append({

                    "skill": canonical,

                    "category":
                        get_category(
                            canonical
                        ),

                    "confidence":
                        confidence,

                    "source":
                        "dictionary"
                })

    return results


# ============================================================
# SKILL STACK EXTRACTION
# ============================================================

def extract_skill_stacks(text):

    results = []

    text_lower = text.lower()

    for stack, components in SKILL_STACKS.items():

        pattern = (
            r"(?<![a-zA-Z0-9])"
            + re.escape(stack)
            + r"(?![a-zA-Z0-9])"
        )

        if not re.search(
            pattern,
            text_lower
        ):

            continue

        for component in components:

            results.append({

                "skill": component,

                "category": "technical",

                "confidence":
                    STACK_CONFIDENCE,

                "source":
                    f"stack:{stack}"
            })

    return results


# ============================================================
# DEDUPLICATION
# ============================================================

def deduplicate_skills(skills):

    unique = {}

    for item in skills:

        skill = item["skill"]

        if skill not in unique:

            unique[skill] = item

        else:

            # Keep higher confidence result
            if (
                item["confidence"]
                >
                unique[skill]["confidence"]
            ):

                unique[skill] = item

    return list(
        unique.values()
    )


# ============================================================
# MAIN ENGINE
# ============================================================

def extract_skills(text):

    if not text:

        return []

    dictionary_results = (
        extract_dictionary_skills(
            text
        )
    )

    stack_results = (
        extract_skill_stacks(
            text
        )
    )

    all_results = (
        dictionary_results
        + stack_results
    )

    return deduplicate_skills(
        all_results
    )