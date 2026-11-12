"""
Day 13 - ATS Scoring Engine

Transparent and explainable candidate scoring framework.
"""


# ============================================================
# ROLE-SPECIFIC WEIGHTS
# ============================================================

ROLE_WEIGHTS = {
    "Data Analyst": {
        "skills": 0.40,
        "experience": 0.25,
        "education": 0.15,
        "semantic": 0.20,
    },

    "Software Developer": {
        "skills": 0.45,
        "experience": 0.30,
        "education": 0.10,
        "semantic": 0.15,
    },

    "Machine Learning Engineer": {
        "skills": 0.45,
        "experience": 0.30,
        "education": 0.10,
        "semantic": 0.15,
    },

    "Business Analyst": {
        "skills": 0.45,
        "experience": 0.30,
        "education": 0.10,
        "semantic": 0.15,
    },

    "default": {
        "skills": 0.40,
        "experience": 0.25,
        "education": 0.15,
        "semantic": 0.20,
    },
}


# ============================================================
# GET ROLE WEIGHTS
# ============================================================

def get_role_weights(role):
    """
    Return scoring weights for the selected job role.
    """

    if not role:
        return ROLE_WEIGHTS["default"]

    role_clean = role.strip().lower()

    for configured_role, weights in ROLE_WEIGHTS.items():

        if configured_role.lower() == role_clean:
            return weights

    return ROLE_WEIGHTS["default"]


# ============================================================
# SCORE NORMALIZATION
# ============================================================

def normalize_score(score):
    """
    Normalize a component score to the range 0 to 1.

    Missing or invalid values are treated as 0.
    """

    if score is None:
        return 0.0

    try:
        score = float(score)

    except (TypeError, ValueError):
        return 0.0

    return max(
        0.0,
        min(score, 1.0)
    )


# ============================================================
# WEIGHTED SCORE CALCULATION
# ============================================================

def calculate_component_score(
    skill_match,
    experience_relevance,
    education_alignment,
    semantic_similarity,
    role
):
    """
    Calculate the weighted ATS score.

    Missing components are excluded from the active
    weighting calculation and the remaining weights
    are normalized.
    """

    weights = get_role_weights(role)

    components = {
        "skills": skill_match,
        "experience": experience_relevance,
        "education": education_alignment,
        "semantic": semantic_similarity,
    }

    weighted_total = 0.0
    active_weight = 0.0

    for component, value in components.items():

        normalized = normalize_score(value)

        if value is None:
            continue

        weight = weights[component]

        weighted_total += (
            normalized * weight
        )

        active_weight += weight

    if active_weight == 0:
        return 0.0

    normalized_score = (
        weighted_total / active_weight
    )

    return round(
        normalized_score * 100,
        2
    )


# ============================================================
# CANDIDATE CLASSIFICATION
# ============================================================

def classify_candidate(score):
    """
    Classify a candidate based on ATS score.
    """

    if score >= 85:
        return "Excellent Match"

    if score >= 70:
        return "Strong Match"

    if score >= 50:
        return "Moderate Match"

    if score >= 40:
        return "Weak Match"

    return "Low Match"
# ============================================================
# EXPLANATION GENERATOR
# ============================================================

def build_explanation(
    role,
    classification,
    final_score,
    skill_match,
    experience_relevance,
    education_alignment,
    semantic_similarity,
    missing_data
):
    """
    Build an explainable scoring breakdown.
    """

    return {
        "role": role,

        "classification": classification,

        "final_score": final_score,

        "components": {

            "skills": (
                round(
                    normalize_score(skill_match) * 100,
                    2
                )
                if skill_match is not None
                else 0.0
            ),

            "experience": (
                round(
                    normalize_score(
                        experience_relevance
                    ) * 100,
                    2
                )
                if experience_relevance is not None
                else 0.0
            ),

            "education": (
                round(
                    normalize_score(
                        education_alignment
                    ) * 100,
                    2
                )
                if education_alignment is not None
                else 0.0
            ),

            "semantic": (
                round(
                    normalize_score(
                        semantic_similarity
                    ) * 100,
                    2
                )
                if semantic_similarity is not None
                else 0.0
            ),
        },

        "weights": get_role_weights(role),

        "missing_data": missing_data,
    }


# ============================================================
# CANDIDATE SCORE GENERATOR
# ============================================================

def generate_candidate_score(
    candidate_name=None,
    role=None,
    skill_match=None,
    experience_relevance=None,
    education_alignment=None,
    semantic_similarity=None,
    candidate_id=None
):
    """
    Generate a complete ATS candidate score.
    """

    missing_data = []

    if skill_match is None:
        missing_data.append(
            "skill_match"
        )

    if experience_relevance is None:
        missing_data.append(
            "experience_relevance"
        )

    if education_alignment is None:
        missing_data.append(
            "education_alignment"
        )

    if semantic_similarity is None:
        missing_data.append(
            "semantic_similarity"
        )

    # --------------------------------------------------------
    # Calculate final ATS score
    # --------------------------------------------------------

    ats_score = calculate_component_score(
        skill_match,
        experience_relevance,
        education_alignment,
        semantic_similarity,
        role
    )

    # --------------------------------------------------------
    # Classify candidate
    # --------------------------------------------------------

    classification = classify_candidate(
        ats_score
    )

    # --------------------------------------------------------
    # Build explanation
    # --------------------------------------------------------

    explanation = build_explanation(
        role,
        classification,
        ats_score,
        skill_match,
        experience_relevance,
        education_alignment,
        semantic_similarity,
        missing_data
    )

    # --------------------------------------------------------
    # Get role-specific weights
    # --------------------------------------------------------

    weights = get_role_weights(role)

    # --------------------------------------------------------
    # Return complete ATS result
    # --------------------------------------------------------

    return {

        # Candidate information
        "candidate_id": candidate_id,

        "candidate_name": candidate_name,

        "role": role,

        # Normalized component scores
        "scores": {

            "skill_match": normalize_score(
                skill_match
            ),

            "experience_relevance": normalize_score(
                experience_relevance
            ),

            "education_alignment": normalize_score(
                education_alignment
            ),

            "semantic_similarity": normalize_score(
                semantic_similarity
            ),
        },

        # Direct component values
        "skill_match": normalize_score(
            skill_match
        ),

        "experience_relevance": normalize_score(
            experience_relevance
        ),

        "education_alignment": normalize_score(
            education_alignment
        ),

        "semantic_similarity": normalize_score(
            semantic_similarity
        ),

        # Component scores as percentages
        "skills_score": round(
            normalize_score(skill_match) * 100,
            2
        ),

        "experience_score": round(
            normalize_score(
                experience_relevance
            ) * 100,
            2
        ),

        "education_score": round(
            normalize_score(
                education_alignment
            ) * 100,
            2
        ),

        "semantic_score": round(
            normalize_score(
                semantic_similarity
            ) * 100,
            2
        ),

        # Final ATS score
        "ats_score": ats_score,

        # Candidate classification
        "classification": classification,

        # Compatibility key required by tests
        "category": classification,

        # Role-specific weights
        "weights": weights,

        # Explainable scoring breakdown
        "explanation": explanation,
    }


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "ROLE_WEIGHTS",
    "get_role_weights",
    "normalize_score",
    "calculate_component_score",
    "classify_candidate",
    "build_explanation",
    "generate_candidate_score",
]