"""
Day 21 - Role Eligibility Configuration

Initial configurable examples.
Thresholds can be changed without changing the engine.
"""

from src.eligibility_decision.engine import EligibilityRule


ROLE_RULES = {

    "Data Analyst": EligibilityRule(
        role="Data Analyst",
        minimum_ats_score=70,
        review_ats_score=50,
        mandatory_skills=["Python", "SQL", "Excel"],
        min_experience_years=0,
        max_experience_years=None,
        allowed_locations=[],
        availability_required=False
    ),

    "Business Analyst": EligibilityRule(
        role="Business Analyst",
        minimum_ats_score=70,
        review_ats_score=50,
        mandatory_skills=[
            "Business Analysis",
            "Communication",
            "Excel"
        ],
        min_experience_years=0,
        max_experience_years=None,
        allowed_locations=[],
        availability_required=False
    ),

    "Senior Data Analyst": EligibilityRule(
        role="Senior Data Analyst",
        minimum_ats_score=75,
        review_ats_score=55,
        mandatory_skills=["Python", "SQL", "Power BI"],
        min_experience_years=3,
        max_experience_years=None,
        allowed_locations=[],
        availability_required=False
    )
}
