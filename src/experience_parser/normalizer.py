import re


def normalize_text(text):
    """Normalize resume text."""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def normalize_company(company):
    """Normalize company name."""

    company = company.strip()
    company = re.sub(r"\s+", " ", company)

    return company


def normalize_title(title):
    """Normalize job title."""

    title = title.strip()
    title = re.sub(r"\s+", " ", title)

    return title
