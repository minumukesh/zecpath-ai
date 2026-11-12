from .role_dictionary import (
    normalize_role,
    ROLE_SKILLS,
)


def role_to_role_similarity(candidate_role, target_role):
    """
    Calculate role similarity using shared role words.
    Returns a score between 0 and 1.
    """

    candidate = set(
        normalize_role(candidate_role).lower().split()
    )

    target = set(
        normalize_role(target_role).lower().split()
    )

    if not candidate or not target:
        return 0.0

    common = candidate & target
    total = candidate | target

    return round(
        len(common) / len(total),
        2
    )


def skill_relevance(candidate_skills, target_role):
    """
    Calculate the percentage of target-role skills
    represented by the candidate's skills.
    """

    target_role = normalize_role(target_role)

    required = ROLE_SKILLS.get(
        target_role,
        set()
    )

    candidate = {
        skill.lower().strip()
        for skill in candidate_skills
    }

    if not required:
        return 0.0

    matched = candidate & required

    return round(
        len(matched) / len(required),
        2
    )


def calculate_relevance(
    experience,
    target_role,
    candidate_skills=None
):
    """
    Calculate overall experience relevance.

    Role similarity  = 50%
    Skill relevance  = 30%
    Duration         = 20%
    """

    if candidate_skills is None:
        candidate_skills = []

    candidate_role = experience.get(
        "canonical_role",
        experience.get(
            "job_title",
            ""
        )
    )

    role_score = role_to_role_similarity(
        candidate_role,
        target_role
    )

    skill_score = skill_relevance(
        candidate_skills,
        target_role
    )

    duration_years = experience.get(
        "duration_years",
        0
    )

    duration_score = min(
        duration_years / 3,
        1.0
    )

    final_score = (
        role_score * 0.50
        + skill_score * 0.30
        + duration_score * 0.20
    )

    return {
        "target_role": normalize_role(
            target_role
        ),
        "candidate_role": candidate_role,
        "role_similarity": role_score,
        "skill_relevance": skill_score,
        "duration_score": round(
            duration_score,
            2
        ),
        "relevance_score": round(
            final_score,
            2
        )
    }
