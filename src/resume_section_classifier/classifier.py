import re

from .detector import classify_heading, is_heading_candidate
from .normalizer import normalize_text


SKILL_TERMS = {
    "python",
    "java",
    "sql",
    "excel",
    "power bi",
    "tableau",
    "pandas",
    "numpy",
    "scikit-learn",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "flask",
    "django",
    "javascript",
    "html",
    "css",
    "git",
}


def classify_block(block):
    """
    Classify a resume block when an explicit section heading
    is missing.
    """

    text = block.strip()
    lower_text = text.lower()

    if not text:
        return "unknown"

    # -----------------------------
    # Skills
    # -----------------------------

    skill_matches = sum(
        1
        for skill in SKILL_TERMS
        if skill in lower_text
    )

    if skill_matches >= 2:
        return "skills"

    comma_items = [
        item.strip()
        for item in text.split(",")
        if item.strip()
    ]

    if len(comma_items) >= 2 and skill_matches >= 1:
        return "skills"

    # -----------------------------
    # Education
    # -----------------------------

    education_pattern = (
        r"\b("
        r"b\.?\s?sc|"
        r"bca|"
        r"b\.?\s?tech|"
        r"b\.?\s?e|"
        r"mca|"
        r"m\.?\s?sc|"
        r"m\.?\s?tech|"
        r"m\.?\s?e|"
        r"mba|"
        r"phd|"
        r"bachelor|"
        r"master|"
        r"degree"
        r")\b"
    )

    if re.search(
        education_pattern,
        text,
        re.IGNORECASE
    ):
        return "education"

    if re.search(
        r"\b(university|college|cgpa|gpa|graduation)\b",
        text,
        re.IGNORECASE
    ):
        return "education"

    # -----------------------------
    # Certifications
    # -----------------------------

    if re.search(
        r"\b("
        r"certified|"
        r"certification|"
        r"certificate|"
        r"credential|"
        r"coursera|"
        r"udemy"
        r")\b",
        text,
        re.IGNORECASE
    ):
        return "certifications"

    # -----------------------------
    # Work Experience
    # -----------------------------

    has_year_range = re.search(
        r"\b(?:19|20)\d{2}\s*[-–]\s*(?:19|20)\d{2}\b",
        text
    )

    has_present_range = re.search(
        r"\b(?:19|20)\d{2}\s*[-–]\s*"
        r"(?:present|current)\b",
        text,
        re.IGNORECASE
    )

    has_job_title = re.search(
        r"\b("
        r"analyst|"
        r"developer|"
        r"engineer|"
        r"intern|"
        r"manager|"
        r"consultant|"
        r"designer|"
        r"administrator"
        r")\b",
        text,
        re.IGNORECASE
    )

    if (
        (has_year_range or has_present_range)
        and has_job_title
    ):
        return "work_experience"

    # -----------------------------
    # Projects
    # -----------------------------

    if re.search(
        r"\b("
        r"project|"
        r"dashboard|"
        r"application|"
        r"system|"
        r"website|"
        r"forecasting|"
        r"prediction"
        r")\b",
        text,
        re.IGNORECASE
    ):
        return "projects"

    return "unknown"


def segment_resume(text):
    """
    Segment resume into labeled sections.

    Explicit headings are detected first.

    When headings are missing, blank-line-separated
    blocks are classified independently.
    """

    text = normalize_text(text)

    # Split resume into logical blocks.
    blocks = re.split(
        r"\n\s*\n",
        text
    )

    sections = []

    current_section = None
    current_content = []

    def save_heading_section():
        nonlocal current_content

        content = "\n".join(
            current_content
        ).strip()

        if content:
            sections.append(
                {
                    "section": current_section or "unknown",
                    "content": content
                }
            )

        current_content = []

    for block in blocks:

        block = block.strip()

        if not block:
            continue

        lines = block.splitlines()

        first_line = lines[0].strip()

        # -----------------------------
        # Explicit heading
        # -----------------------------

        if is_heading_candidate(first_line):

            detected_section = classify_heading(
                first_line
            )

            if detected_section:

                save_heading_section()

                current_section = detected_section

                remaining_lines = lines[1:]

                if remaining_lines:
                    current_content.extend(
                        remaining_lines
                    )

                continue

        # -----------------------------
        # No heading
        # -----------------------------

        if current_section is not None:

            current_content.extend(lines)

        else:

            predicted_section = classify_block(
                block
            )

            sections.append(
                {
                    "section": predicted_section,
                    "content": block
                }
            )

    save_heading_section()

    return sections


def classify_resume(text):
    """
    Convert resume into structured sections.
    """

    sections = segment_resume(text)

    result = {
        "skills": [],
        "work_experience": [],
        "education": [],
        "certifications": [],
        "projects": [],
        "unknown": []
    }

    for item in sections:

        section = item["section"]
        content = item["content"]

        if section not in result:
            result[section] = []

        result[section].append(content)

    return result

# ============================================================
# DAY 19 MAINTENANCE FIX
# Content-based fallback for missing Projects heading
# ============================================================

_original_classify_resume = classify_resume


def _detect_project_content(text):
    """
    Detect project-like content when the resume does not
    contain an explicit Projects heading.

    This is a lightweight content-based fallback and only
    runs when the normal classifier did not identify projects.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    project_keywords = {
        "dashboard",
        "forecasting",
        "application",
        "website",
        "system",
        "model",
        "machine learning",
        "data analysis",
        "automation",
        "implemented",
        "developed",
        "built",
        "created",
        "designed",
        "project"
    }

    results = []

    for index, line in enumerate(lines):

        lower = line.lower()

        score = 0

        for keyword in project_keywords:

            if keyword in lower:
                score += 1

        # A likely project title usually contains a
        # project-related term and is followed by a
        # descriptive implementation line.
        if score >= 1:

            next_line = ""

            if index + 1 < len(lines):
                next_line = lines[index + 1].lower()

            description_keywords = {
                "built",
                "developed",
                "created",
                "designed",
                "implemented",
                "using",
                "dashboard",
                "system",
                "application"
            }

            if any(
                keyword in next_line
                for keyword in description_keywords
            ):

                results.append(
                    line + " - " + lines[index + 1]
                )

    return results


def classify_resume(text):

    result = _original_classify_resume(text)

    # Only use the fallback when the existing classifier
    # did not detect any projects.
    if not result.get("projects"):

        detected_projects = _detect_project_content(text)

        if detected_projects:

            result["projects"] = detected_projects

    return result
