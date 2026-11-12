"""
Day 41 - Unified Scoring Engine

Combines existing ATS, screening, and HR interview scores.
It does not recreate the previous scoring engines.
"""

from src.unified_scoring.config import ROLE_WEIGHTS


SCORE_COMPONENTS = (
    "ats",
    "screening",
    "hr_interview"
)


def get_role_weights(role):
    """
    Return role-specific weights.
    """

    normalized_role = str(role or "default").strip().lower()

    weights = ROLE_WEIGHTS.get(
        normalized_role,
        ROLE_WEIGHTS["default"]
    )

    if round(sum(weights.values()), 5) != 100:
        raise ValueError(
            f"Weights for {normalized_role} must total 100."
        )

    return weights.copy()


def validate_score(value, component):
    """
    Validate a score between 0 and 100.
    """

    if value is None:
        return None

    if isinstance(value, bool):
        raise ValueError(
            f"{component} score must be numeric."
        )

    try:
        score = float(value)
    except (TypeError, ValueError):
        raise ValueError(
            f"{component} score must be numeric."
        )

    if not 0 <= score <= 100:
        raise ValueError(
            f"{component} score must be between 0 and 100."
        )

    return score


def calculate_unified_score(
    ats_score,
    screening_score,
    hr_interview_score,
    weights
):
    """
    Calculate a weighted unified score.

    Missing components are excluded.
    Remaining weights are normalized.
    """

    input_scores = {
        "ats": ats_score,
        "screening": screening_score,
        "hr_interview": hr_interview_score
    }

    validated_scores = {}
    missing_components = []

    for component, value in input_scores.items():

        score = validate_score(value, component)

        if score is None:
            missing_components.append(component)
        else:
            validated_scores[component] = score

    if not validated_scores:
        raise ValueError(
            "At least one evaluation score is required."
        )

    active_weight_total = sum(
        weights[component]
        for component in validated_scores
    )

    if active_weight_total <= 0:
        raise ValueError(
            "Active scoring weights must be greater than zero."
        )

    component_breakdown = {}
    unified_score = 0.0

    for component, score in validated_scores.items():

        original_weight = weights[component]

        normalized_weight = (
            original_weight / active_weight_total
        )

        contribution = score * normalized_weight

        unified_score += contribution

        component_breakdown[component] = {
            "score": round(score, 2),
            "original_weight": original_weight,
            "active_weight_percentage": round(
                normalized_weight * 100, 2
            ),
            "weighted_contribution": round(
                contribution, 2
            )
        }

    return {
        "unified_score": round(unified_score, 2),
        "hiring_fit_percentage": round(unified_score, 2),
        "component_breakdown": component_breakdown,
        "missing_components": missing_components,
        "active_weight_total": active_weight_total
    }


def generate_unified_score(
    candidate_id,
    candidate_name,
    target_role,
    ats_score,
    screening_score,
    hr_interview_score
):
    """
    Generate the complete unified candidate score object.
    """

    if not candidate_id:
        raise ValueError("Candidate ID is required.")

    if not candidate_name:
        raise ValueError("Candidate name is required.")

    if not target_role:
        raise ValueError("Target role is required.")

    weights = get_role_weights(target_role)

    result = calculate_unified_score(
        ats_score=ats_score,
        screening_score=screening_score,
        hr_interview_score=hr_interview_score,
        weights=weights
    )

    return {
        "candidate_id": candidate_id,
        "candidate_name": candidate_name,
        "target_role": target_role,
        "score_type": "unified_hiring_intelligence_score",
        "ats_score": ats_score,
        "screening_score": screening_score,
        "hr_interview_score": hr_interview_score,
        "role_weights": weights,
        "unified_score": result["unified_score"],
        "hiring_fit_percentage": result[
            "hiring_fit_percentage"
        ],
        "component_breakdown": result[
            "component_breakdown"
        ],
        "missing_components": result[
            "missing_components"
        ],
        "active_weight_total": result[
            "active_weight_total"
        ],
        "explanation": (
            "The unified score combines available ATS, screening, "
            "and HR interview scores using role-specific weights. "
            "Missing components are excluded and remaining weights "
            "are normalized."
        )
    }
