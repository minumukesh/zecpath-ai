import re


SECTION_HEADINGS = {
    "summary": "SUMMARY",
    "professional summary": "PROFESSIONAL SUMMARY",
    "career summary": "CAREER SUMMARY",
    "objective": "OBJECTIVE",
    "career objective": "CAREER OBJECTIVE",
    "education": "EDUCATION",
    "academic qualifications": "EDUCATION",
    "skills": "SKILLS",
    "technical skills": "TECHNICAL SKILLS",
    "soft skills": "SOFT SKILLS",
    "experience": "EXPERIENCE",
    "work experience": "WORK EXPERIENCE",
    "professional experience": "PROFESSIONAL EXPERIENCE",
    "employment history": "EMPLOYMENT HISTORY",
    "projects": "PROJECTS",
    "academic projects": "ACADEMIC PROJECTS",
    "certifications": "CERTIFICATIONS",
    "certificates": "CERTIFICATIONS",
    "achievements": "ACHIEVEMENTS",
    "awards": "AWARDS",
    "internship": "INTERNSHIP",
    "internships": "INTERNSHIPS",
    "languages": "LANGUAGES",
    "interests": "INTERESTS",
    "hobbies": "HOBBIES",
    "references": "REFERENCES"
}


def normalize_bullets(text):
    pattern = r"[\u2022\u25CF\u25AA\u25E6\u2023\u2043\u2219\u00B7\u25C6\u25C7\u25BA\u25B8]"
    return re.sub(pattern, "-", text)


def normalize_section_heading(line):
    line = line.strip()
    line = line.rstrip(":")
    line = re.sub(r"\s+", " ", line)

    key = line.lower()

    if key in SECTION_HEADINGS:
        return SECTION_HEADINGS[key]

    return line


def remove_noise(text):
    text = text.replace("\x00", "")
    text = text.replace("\u2013", "-")
    text = text.replace("\u2014", "-")

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text


def clean_text(text):
    if not text:
        return ""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = normalize_bullets(text)
    text = remove_noise(text)

    lines = []

    for line in text.split("\n"):
        line = line.strip()

        if line:
            line = normalize_section_heading(line)

        lines.append(line)

    cleaned = "\n".join(lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    return cleaned.strip()