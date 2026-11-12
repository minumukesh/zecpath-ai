import re


PERSONAL_ATTRIBUTE_PATTERNS = {
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "phone": r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)",
    "date_of_birth": r"\b(?:DOB|Date of Birth|Birth Date)\s*[:\-]?\s*[0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{2,4}\b",
    "gender": r"\b(?:Gender|Sex)\s*[:\-]?\s*(?:Male|Female|Other|M|F)\b",
    "age": r"\bAge\s*[:\-]?\s*\d{1,3}\b",
}


NON_ESSENTIAL_FIELDS = [
    "email",
    "phone",
    "date_of_birth",
    "gender",
    "age",
]


def normalize_whitespace(text):
    """
    Convert repeated spaces and blank lines into a standard format.
    """

    text = str(text or "")

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    lines = []

    for line in text.split("\n"):
        line = re.sub(r"\s+", " ", line).strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def normalize_sections(text):
    """
    Standardize common resume section headings.
    """

    text = normalize_whitespace(text)

    section_map = {
        "professional experience": "WORK EXPERIENCE",
        "work experience": "WORK EXPERIENCE",
        "employment history": "WORK EXPERIENCE",
        "education": "EDUCATION",
        "academic background": "EDUCATION",
        "skills": "SKILLS",
        "technical skills": "SKILLS",
        "projects": "PROJECTS",
        "certifications": "CERTIFICATIONS",
        "certificates": "CERTIFICATIONS",
        "summary": "SUMMARY",
        "professional summary": "SUMMARY",
        "objective": "SUMMARY",
    }

    lines = []

    for line in text.split("\n"):
        key = line.strip().lower().rstrip(":")

        if key in section_map:
            lines.append(section_map[key])
        else:
            lines.append(line)

    return "\n".join(lines)


def mask_personal_attributes(text):
    """
    Mask non-essential personal attributes before evaluation.
    """

    text = str(text or "")
    masked_fields = []

    for field, pattern in PERSONAL_ATTRIBUTE_PATTERNS.items():
        new_text, count = re.subn(
            pattern,
            f"[MASKED_{field.upper()}]",
            text,
            flags=re.IGNORECASE,
        )

        if count > 0:
            masked_fields.append(field)

        text = new_text

    return text, masked_fields


def normalize_resume(text):
    """
    Produce a standardized and privacy-aware resume representation.
    """

    normalized = normalize_sections(text)

    masked_text, masked_fields = mask_personal_attributes(
        normalized
    )

    return {
        "original_length": len(str(text or "")),
        "normalized_text": masked_text,
        "masked_attributes": masked_fields,
        "normalization_applied": True,
    }
