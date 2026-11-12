from __future__ import annotations

from .parameters import SCORING_WEIGHTS
from .question_scorer import score_question


def score_screening(
    candidate_id: str,
    questions: list[dict],
) -> dict:

    if not isinstance(questions, list):
        raise TypeError("questions must be a list.")

    if not questions:
        raise ValueError("At least one screening question is required.")

    scored_questions = []
    previous_answers = []

    for index, item in enumerate(questions, start=1):

        if not isinstance(item, dict):
            raise TypeError(
                f"Question {index} must be a dictionary."
            )

        question = str(item.get("question", "")).strip()
        answer = str(item.get("answer", "") or "").strip()

        if not question:
            raise ValueError(
                f"Question {index} is missing question text."
            )

        result = score_question(
            question=question,
            answer=answer,
            expected_keywords=item.get("expected_keywords", []),
            required_fields=item.get("required_fields", []),
            previous_answers=previous_answers,
        )

        result["question_id"] = item.get(
            "question_id",
            f"Q{index:03d}",
        )

        scored_questions.append(result)

        if answer:
            previous_answers.append(answer)

    overall_score = round(
        sum(
            item["weighted_score"]
            for item in scored_questions
        ) / len(scored_questions),
        2,
    )

    parameter_averages = {}

    for parameter in SCORING_WEIGHTS:
        parameter_averages[parameter] = round(
            sum(
                item["parameter_scores"][parameter]
                for item in scored_questions
            ) / len(scored_questions),
            2,
        )

    if overall_score >= 85:
        classification = "HIGH"
    elif overall_score >= 70:
        classification = "GOOD"
    elif overall_score >= 50:
        classification = "MODERATE"
    else:
        classification = "LOW"

    explanations = []

    for parameter, score in parameter_averages.items():
        explanations.append({
            "parameter": parameter,
            "average_score": score,
            "weight": SCORING_WEIGHTS[parameter],
        })

    return {
        "candidate_id": candidate_id,
        "scoring_engine": "day26_screening_scoring_engine",
        "score_scale": "0-100",
        "question_count": len(scored_questions),
        "overall_screening_score": overall_score,
        "classification": classification,
        "parameter_averages": parameter_averages,
        "parameter_weights": SCORING_WEIGHTS.copy(),
        "question_scores": scored_questions,
        "explainable_output": {
            "parameter_breakdown": explanations,
            "aggregation_method": (
                "Arithmetic mean of per-question weighted scores."
            ),
            "classification_method": (
                "HIGH >= 85; GOOD >= 70; MODERATE >= 50; otherwise LOW."
            ),
            "limitations": [
                "Scoring uses transparent heuristic rules, not a trained evaluator.",
                "Keyword coverage is not a complete measure of semantic relevance.",
                "Text similarity does not reliably detect contradictions.",
                "Scores should support human review, not determine hiring alone.",
            ],
        },
    }
