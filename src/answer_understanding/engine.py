from .classifier import classify_intent
from .extractor import extract_answer_details
from .semantic_object import build_semantic_answer


def understand_answer(answer):

    text = str(answer or "").strip()

    intent = classify_intent(text)

    details = extract_answer_details(text)

    if intent == "MISSING_OR_VAGUE":
        status = "MISSING_OR_VAGUE"
        confidence = 0.20

    elif intent == "OFF_TOPIC":
        status = "OFF_TOPIC"
        confidence = 0.90

    elif len(text.split()) <= 2:
        status = "PARTIAL"
        confidence = 0.55

    else:
        status = "VALID"

        evidence = sum([
            bool(details["skills"]),
            details["experience"]["has_experience"],
            details["availability"]["availability_mentioned"],
            details["salary"]["salary_mentioned"],
        ])

        if evidence >= 2:
            confidence = 0.95
        elif evidence == 1:
            confidence = 0.85
        else:
            confidence = 0.70

    semantic_object = build_semantic_answer(
        answer=text,
        intent=intent,
        details=details,
        status=status,
        confidence=confidence,
    )

    return {
        "intent": intent,
        "answer_status": status,
        "confidence": confidence,
        "extracted": details,
        "semantic_object": semantic_object,
    }
