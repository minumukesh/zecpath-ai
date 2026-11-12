from __future__ import annotations

import re

from .parameters import SCORING_WEIGHTS


def _normalize_text(text: str) -> str:
    text = str(text or "").strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"\b[a-zA-Z0-9+#.]+\b", text.lower()))


def _score_clarity(answer: str) -> tuple[float, str]:
    text = str(answer or "").strip()

    if not text:
        return 0.0, "No answer was provided."

    words = text.split()

    if len(words) == 1:
        return 35.0, "The answer is very short and provides little explanation."

    if len(words) <= 3:
        return 55.0, "The answer is understandable but brief."

    if len(words) <= 8:
        return 75.0, "The answer is reasonably clear."

    if len(words) <= 35:
        return 95.0, "The answer provides a clear explanation."

    return 85.0, "The answer is detailed, but its length may reduce clarity."


def _score_relevance(
    question: str,
    answer: str,
    expected_keywords: list[str] | None = None,
) -> tuple[float, str]:

    if not str(answer or "").strip():
        return 0.0, "An empty answer cannot demonstrate relevance."

    answer_tokens = _tokens(answer)

    keywords = expected_keywords or []
    matched = []

    for keyword in keywords:
        keyword_tokens = _tokens(keyword)

        if keyword_tokens and keyword_tokens.issubset(answer_tokens):
            matched.append(keyword)

    if keywords:
        coverage = len(matched) / len(keywords)
        score = round(coverage * 100, 2)

        if score >= 75:
            reason = "The answer covers most of the expected keywords."
        elif score >= 40:
            reason = "The answer covers some expected keywords."
        else:
            reason = "The answer covers few or none of the expected keywords."

        return score, reason

    question_tokens = _tokens(question)
    overlap = question_tokens.intersection(answer_tokens)

    if not question_tokens:
        return 50.0, "Relevance could not be fully evaluated from the question."

    score = min(
        100.0,
        round(100 * len(overlap) / len(question_tokens), 2),
    )

    return score, "Relevance was estimated from question-answer word overlap."


def _score_completeness(
    answer: str,
    required_fields: list[str] | None = None,
) -> tuple[float, str]:

    text = str(answer or "").strip()

    if not text:
        return 0.0, "The answer is missing."

    required_fields = required_fields or []

    if required_fields:
        lowered = text.lower()
        matched = [
            field for field in required_fields
            if field.lower() in lowered
        ]

        score = round(
            100 * len(matched) / len(required_fields),
            2,
        )

        if score == 100:
            reason = "All configured required information was found."
        elif score > 0:
            reason = "Some configured required information was found."
        else:
            reason = "Configured required information was not found."

        return score, reason

    word_count = len(text.split())

    if word_count <= 2:
        return 25.0, "The answer is too brief to provide much detail."

    if word_count <= 5:
        return 55.0, "The answer provides limited information."

    if word_count <= 15:
        return 80.0, "The answer provides a reasonable amount of information."

    return 100.0, "The answer provides substantial information."


def _score_consistency(
    answer: str,
    previous_answers: list[str] | None = None,
) -> tuple[float, str]:

    text = _normalize_text(answer)

    if not text:
        return 0.0, "A missing answer cannot be checked for consistency."

    previous_answers = previous_answers or []

    if not previous_answers:
        return 100.0, "No contradictory previous answer was supplied."

    current_tokens = _tokens(text)

    if not current_tokens:
        return 50.0, "There is insufficient text to evaluate consistency."

    for previous in previous_answers:
        previous_text = _normalize_text(previous)

        if not previous_text:
            continue

        previous_tokens = _tokens(previous_text)

        if not previous_tokens:
            continue

        overlap = len(current_tokens.intersection(previous_tokens))
        union = len(current_tokens.union(previous_tokens))

        similarity = overlap / union if union else 0.0

        if similarity >= 0.8:
            return 100.0, "The answer closely matches an earlier response."

    # Similarity alone cannot prove consistency or contradiction.
    return 70.0, (
        "No strong textual match was found. "
        "Semantic contradiction requires further review."
    )


def score_question(
    question: str,
    answer: str,
    expected_keywords: list[str] | None = None,
    required_fields: list[str] | None = None,
    previous_answers: list[str] | None = None,
) -> dict:

    clarity, clarity_reason = _score_clarity(answer)

    relevance, relevance_reason = _score_relevance(
        question,
        answer,
        expected_keywords,
    )

    completeness, completeness_reason = _score_completeness(
        answer,
        required_fields,
    )

    consistency, consistency_reason = _score_consistency(
        answer,
        previous_answers,
    )

    breakdown = {
        "clarity": clarity,
        "relevance": relevance,
        "completeness": completeness,
        "consistency": consistency,
    }

    weighted_score = sum(
        breakdown[name] * weight
        for name, weight in SCORING_WEIGHTS.items()
    )

    weighted_score = round(
        max(0.0, min(100.0, weighted_score)),
        2,
    )

    reasons = {
        "clarity": clarity_reason,
        "relevance": relevance_reason,
        "completeness": completeness_reason,
        "consistency": consistency_reason,
    }

    return {
        "question": question,
        "answer": answer,
        "parameter_scores": breakdown,
        "weights": SCORING_WEIGHTS.copy(),
        "weighted_score": weighted_score,
        "explanation": reasons,
    }
