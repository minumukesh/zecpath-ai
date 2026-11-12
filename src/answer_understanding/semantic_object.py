def build_semantic_answer(
    answer,
    intent,
    details,
    status,
    confidence
):

    return {
        "answer_text": answer,
        "intent": intent,
        "answer_status": status,
        "confidence": round(float(confidence), 4),
        "semantic_data": {
            "skills": details["skills"],
            "experience": details["experience"],
            "availability": details["availability"],
            "salary": details["salary"],
        },
    }
