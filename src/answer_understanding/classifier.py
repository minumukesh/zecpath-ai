import re


SKILLS = [
    "python",
    "sql",
    "java",
    "javascript",
    "react",
    "node.js",
    "nodejs",
    "excel",
    "power bi",
    "tableau",
    "pandas",
    "numpy",
    "machine learning",
    "data analysis",
    "communication",
    "leadership",
    "customer service",
]


FILLER_ANSWERS = {
    "",
    "yes",
    "no",
    "maybe",
    "not sure",
    "i don't know",
    "dont know",
    "don't know",
    "nothing",
    "okay",
    "ok",
    "fine",
    "whatever",
}


OFF_TOPIC_KEYWORDS = [
    "weather",
    "cricket",
    "movie",
    "football",
    "politics",
    "recipe",
    "weekend",
    "holiday",
]


def classify_intent(answer):

    if answer is None:
        return "MISSING_OR_VAGUE"

    text = str(answer).strip()
    lowered = text.lower()

    if lowered in FILLER_ANSWERS:
        return "MISSING_OR_VAGUE"

    if not text:
        return "MISSING_OR_VAGUE"

    # Detect obviously unrelated responses.
    if any(
        re.search(
            rf"\b{re.escape(word)}\b",
            lowered
        )
        for word in OFF_TOPIC_KEYWORDS
    ):
        return "OFF_TOPIC"

    # Identify skill-related answers.
    if any(
        re.search(
            rf"\b{re.escape(skill)}\b",
            lowered
        )
        for skill in SKILLS
    ):
        return "SKILLS"

    # Identify salary expectations.
    if re.search(
        r"\b(salary|expected salary|expect|lpa|lakhs?|"
        r"package|compensation|per annum)\b|₹|\brupees\b",
        lowered
    ):
        return "SALARY_EXPECTATION"

    # Identify joining availability.
    if re.search(
        r"\b(immediately|immediate|available|availability|"
        r"joining|join|notice period)\b",
        lowered
    ):
        return "AVAILABILITY"

    # Identify experience-related answers.
    if re.search(
        r"\b(experience|experienced|worked|working|"
        r"previous job|company|years?|yrs?|months?)\b",
        lowered
    ):
        return "EXPERIENCE"

    # Very short answers are generally insufficient.
    if len(text.split()) <= 2:
        return "MISSING_OR_VAGUE"

    return "GENERAL"
