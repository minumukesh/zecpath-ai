import re

from .normalizer import normalize_heading
from .section_dictionary import SECTION_ALIAS_LOOKUP


def is_heading_candidate(line):
    """
    Determine whether a line looks like a resume section heading.
    """

    stripped = line.strip()

    if not stripped:
        return False

    # Very long lines are unlikely to be section headings.
    if len(stripped) > 80:
        return False

    normalized = normalize_heading(stripped)

    # Exact match with known section headings.
    if normalized in SECTION_ALIAS_LOOKUP:
        return True

    # Detect short uppercase headings.
    letters = re.sub(r"[^A-Za-z]", "", stripped)

    if (
        letters
        and stripped.upper() == stripped
        and len(stripped.split()) <= 6
    ):
        return True

    # Detect short headings ending with a colon.
    if stripped.endswith(":") and len(stripped.split()) <= 6:
        return True

    return False


def classify_heading(line):
    """
    Classify a detected heading into a canonical section.
    """

    normalized = normalize_heading(line)

    return SECTION_ALIAS_LOOKUP.get(normalized)