import math


KEYWORD_SIGNAL_WEIGHT = 0.40
SEMANTIC_SIGNAL_WEIGHT = 0.60


def normalize_component_scores(scores):
    """
    Normalize component scores to the 0-1 range.
    """

    normalized = {}

    for name, value in scores.items():
        try:
            value = float(value)
        except (TypeError, ValueError):
            value = 0.0

        normalized[name] = max(0.0, min(1.0, value))

    return normalized


def reduce_keyword_dependence(
    keyword_score,
    semantic_score,
    experience_score=0.0,
    education_score=0.0,
):
    """
    Reduce over-dependence on exact keyword matching.

    Keyword matching contributes 40%.
    Broader semantic/contextual evidence contributes 60%.
    """

    keyword_score = max(
        0.0,
        min(1.0, float(keyword_score or 0))
    )

    semantic_score = max(
        0.0,
        min(1.0, float(semantic_score or 0))
    )

    experience_score = max(
        0.0,
        min(1.0, float(experience_score or 0))
    )

    education_score = max(
        0.0,
        min(1.0, float(education_score or 0))
    )

    contextual_score = (
        semantic_score * 0.60
        + experience_score * 0.25
        + education_score * 0.15
    )

    final_score = (
        keyword_score * KEYWORD_SIGNAL_WEIGHT
        + contextual_score * SEMANTIC_SIGNAL_WEIGHT
    )

    return round(final_score, 4)


def calculate_bias_indicators(
    original_score,
    normalized_score,
    keyword_score,
    semantic_score,
    masked_attributes,
):
    """
    Calculate transparent indicators for potential scoring bias.
    """

    indicators = []

    if keyword_score > 0.85 and semantic_score < 0.50:
        indicators.append(
            "HIGH_KEYWORD_DEPENDENCE"
        )

    if len(masked_attributes) > 0:
        indicators.append(
            "PERSONAL_ATTRIBUTES_MASKED"
        )

    score_difference = abs(
        float(original_score or 0)
        - float(normalized_score or 0)
    )

    if score_difference > 0.15:
        indicators.append(
            "SIGNIFICANT_SCORE_CHANGE_AFTER_NORMALIZATION"
        )

    if not indicators:
        indicators.append(
            "NO_MAJOR_BIAS_INDICATOR_DETECTED"
        )

    return {
        "indicators": indicators,
        "score_difference": round(score_difference, 4),
        "keyword_dependence_flag": (
            "HIGH"
            if keyword_score > 0.85 and semantic_score < 0.50
            else "NORMAL"
        ),
    }


def compare_scores(original_score, fair_score):
    """
    Compare original ATS score with fairness-adjusted score.
    """

    original_score = float(original_score or 0)
    fair_score = float(fair_score or 0)

    return {
        "original_score": round(original_score, 2),
        "fair_score": round(fair_score, 2),
        "difference": round(
            fair_score - original_score,
            2
        ),
    }


def generate_fairness_evaluation(
    candidate_name,
    original_score,
    keyword_score,
    semantic_score,
    experience_score,
    education_score,
    masked_attributes,
):
    """
    Generate a complete fairness evaluation.
    """

    fair_score = reduce_keyword_dependence(
        keyword_score=keyword_score,
        semantic_score=semantic_score,
        experience_score=experience_score,
        education_score=education_score,
    )

    fair_score_100 = round(
        fair_score * 100,
        2
    )

    indicators = calculate_bias_indicators(
        original_score=original_score,
        normalized_score=fair_score,
        keyword_score=keyword_score,
        semantic_score=semantic_score,
        masked_attributes=masked_attributes,
    )

    return {
        "candidate_name": candidate_name,
        "original_ats_score": round(
            float(original_score or 0),
            2
        ),
        "fairness_adjusted_score": fair_score_100,
        "score_comparison": compare_scores(
            original_score,
            fair_score_100,
        ),
        "component_scores": {
            "keyword_score": round(
                float(keyword_score or 0) * 100,
                2
            ),
            "semantic_score": round(
                float(semantic_score or 0) * 100,
                2
            ),
            "experience_score": round(
                float(experience_score or 0) * 100,
                2
            ),
            "education_score": round(
                float(education_score or 0) * 100,
                2
            ),
        },
        "weights": {
            "keyword_signal": 40,
            "contextual_signal": 60,
        },
        "masked_attributes": masked_attributes,
        "bias_evaluation": indicators,
        "fairness_method": (
            "Reduced exact-keyword dependence and "
            "increased contextual/semantic evidence."
        ),
    }
