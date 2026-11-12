import re

from .classifier import SKILLS


def extract_skills(answer):

    text = str(answer or "").lower()
    found = []

    for skill in SKILLS:

        if re.search(
            rf"\b{re.escape(skill)}\b",
            text
        ):
            found.append(skill)

    return sorted(set(found))


def extract_experience(answer):

    text = str(answer or "")

    years = [
        float(value)
        for value in re.findall(
            r"\b(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\b",
            text,
            re.IGNORECASE
        )
    ]

    months = [
        int(value)
        for value in re.findall(
            r"\b(\d+)\s*(?:months?|mos?)\b",
            text,
            re.IGNORECASE
        )
    ]

    total_years = sum(years) + sum(months) / 12

    experience_mentioned = bool(
        years
        or months
        or re.search(
            r"\b(experience|experienced|worked|working)\b",
            text,
            re.IGNORECASE
        )
    )

    return {
        "years_mentioned": years,
        "months_mentioned": months,
        "total_years": round(total_years, 2),
        "has_experience": experience_mentioned,
    }


def extract_availability(answer):

    text = str(answer or "").lower()

    immediate = bool(
        re.search(
            r"\b(immediately|immediate)\b",
            text
        )
    )

    notice_match = re.search(
        r"\b(\d+)\s*(days?|weeks?|months?)\b",
        text
    )

    notice_period = None

    if notice_match:
        notice_period = (
            f"{notice_match.group(1)} "
            f"{notice_match.group(2)}"
        )

    mentioned = bool(
        immediate
        or notice_period
        or re.search(
            r"\b(available|availability|joining|join|notice period)\b",
            text
        )
    )

    return {
        "available_immediately": immediate,
        "notice_period": notice_period,
        "availability_mentioned": mentioned,
    }


def extract_salary(answer):

    text = str(answer or "").lower()

    mentions = []

    # Examples: 6 LPA, 5.5 lakhs, ₹40000, 40k.
    patterns = [
        (
            r"(?:₹|rs\.?\s*)\s*(\d+(?:\.\d+)?)\s*"
            r"(lpa|lakhs?|k)?\b"
        ),
        (
            r"\b(\d+(?:\.\d+)?)\s*"
            r"(lpa|lakhs?|k)\b"
        ),
    ]

    for pattern in patterns:

        for value, unit in re.findall(
            pattern,
            text,
            re.IGNORECASE
        ):

            item = {
                "value": float(value),
                "unit": unit.lower() if unit else "unspecified",
            }

            if item not in mentions:
                mentions.append(item)

    return {
        "salary_mentions": mentions,
        "salary_mentioned": bool(mentions),
    }


def extract_answer_details(answer):

    text = str(answer or "").strip()

    return {
        "skills": extract_skills(text),
        "experience": extract_experience(text),
        "availability": extract_availability(text),
        "salary": extract_salary(text),
    }
