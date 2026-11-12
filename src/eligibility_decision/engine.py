"""
Day 21 - Eligibility Decision Engine
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


ELIGIBLE = "ELIGIBLE"
REVIEW = "REVIEW"
REJECTED = "REJECTED"


@dataclass
class EligibilityRule:
    role: str
    minimum_ats_score: float
    review_ats_score: float
    mandatory_skills: List[str] = field(default_factory=list)
    min_experience_years: float = 0.0
    max_experience_years: Optional[float] = None
    allowed_locations: List[str] = field(default_factory=list)
    availability_required: bool = False


class EligibilityDecisionEngine:

    def __init__(self, rules: Optional[Dict[str, EligibilityRule]] = None):
        self.rules = {}

        if rules:
            for role, rule in rules.items():
                self.add_rule(rule)

    def add_rule(self, rule: EligibilityRule) -> None:
        """
        Store rules using a normalized role name.
        This makes 'Data Analyst', 'data analyst',
        and 'DATA ANALYST' resolve to the same rule.
        """
        normalized_role = rule.role.strip().lower()
        self.rules[normalized_role] = rule

    def get_rule(self, role: str) -> EligibilityRule:
        normalized_role = str(role).strip().lower()

        rule = self.rules.get(normalized_role)

        if rule is None:
            raise ValueError(
                f"No eligibility rule configured for role: {role}"
            )

        return rule

    @staticmethod
    def normalize_skills(skills: List[str]) -> set:
        return {
            str(skill).strip().lower()
            for skill in skills
            if str(skill).strip()
        }

    @staticmethod
    def check_mandatory_skills(
        candidate_skills: List[str],
        mandatory_skills: List[str]
    ) -> Dict[str, Any]:

        candidate = EligibilityDecisionEngine.normalize_skills(
            candidate_skills
        )

        required = EligibilityDecisionEngine.normalize_skills(
            mandatory_skills
        )

        matched = sorted(candidate.intersection(required))
        missing = sorted(required.difference(candidate))

        return {
            "passed": len(missing) == 0,
            "matched_skills": matched,
            "missing_skills": missing
        }

    @staticmethod
    def check_experience(
        experience_years: float,
        minimum_years: float,
        maximum_years: Optional[float]
    ) -> Dict[str, Any]:

        experience_years = float(experience_years or 0)

        minimum_passed = experience_years >= minimum_years

        maximum_passed = (
            True
            if maximum_years is None
            else experience_years <= maximum_years
        )

        return {
            "passed": minimum_passed and maximum_passed,
            "experience_years": experience_years,
            "minimum_required": minimum_years,
            "maximum_allowed": maximum_years
        }

    @staticmethod
    def check_location(
        candidate_location: str,
        allowed_locations: List[str]
    ) -> Dict[str, Any]:

        if not allowed_locations:
            return {
                "passed": True,
                "location": candidate_location,
                "allowed_locations": [],
                "constraint_applied": False
            }

        candidate_location = (
            str(candidate_location or "").strip().lower()
        )

        allowed = {
            str(location).strip().lower()
            for location in allowed_locations
        }

        passed = candidate_location in allowed

        return {
            "passed": passed,
            "location": candidate_location,
            "allowed_locations": sorted(allowed),
            "constraint_applied": True
        }

    @staticmethod
    def check_availability(
        available: bool,
        availability_required: bool
    ) -> Dict[str, Any]:

        if not availability_required:
            return {
                "passed": True,
                "available": bool(available),
                "constraint_applied": False
            }

        return {
            "passed": bool(available),
            "available": bool(available),
            "constraint_applied": True
        }

    def evaluate_candidate(
        self,
        candidate: Dict[str, Any],
        role: str
    ) -> Dict[str, Any]:

        rule = self.get_rule(role)

        ats_score = float(
            candidate.get("ats_score", 0) or 0
        )

        skills_result = self.check_mandatory_skills(
            candidate.get("skills", []),
            rule.mandatory_skills
        )

        experience_result = self.check_experience(
            candidate.get("experience_years", 0),
            rule.min_experience_years,
            rule.max_experience_years
        )

        location_result = self.check_location(
            candidate.get("location", ""),
            rule.allowed_locations
        )

        availability_result = self.check_availability(
            candidate.get("available", False),
            rule.availability_required
        )

        rule_checks = {
            "mandatory_skills": skills_result,
            "experience": experience_result,
            "location": location_result,
            "availability": availability_result
        }

        failed_rules = [
            name
            for name, result in rule_checks.items()
            if not result["passed"]
        ]

        score_passed = (
            ats_score >= rule.minimum_ats_score
        )

        review_range = (
            rule.review_ats_score
            <= ats_score
            < rule.minimum_ats_score
        )

        if failed_rules:
            decision = REJECTED
        elif score_passed:
            decision = ELIGIBLE
        elif review_range:
            decision = REVIEW
        else:
            decision = REJECTED

        return {
            "candidate_id": candidate.get("candidate_id"),
            "candidate_name": candidate.get("candidate_name"),
            "role": role,
            "ats_score": round(ats_score, 2),
            "decision": decision,
            "eligible_for_ai_screening": (
                decision == ELIGIBLE
            ),
            "rule_checks": rule_checks,
            "failed_rules": failed_rules,
            "configured_rule": {
                "minimum_ats_score": rule.minimum_ats_score,
                "review_ats_score": rule.review_ats_score,
                "mandatory_skills": rule.mandatory_skills,
                "min_experience_years": (
                    rule.min_experience_years
                ),
                "max_experience_years": (
                    rule.max_experience_years
                ),
                "allowed_locations": (
                    rule.allowed_locations
                ),
                "availability_required": (
                    rule.availability_required
                )
            }
        }

    def evaluate_candidates(
        self,
        candidates: List[Dict[str, Any]],
        role: str
    ) -> List[Dict[str, Any]]:

        return [
            self.evaluate_candidate(candidate, role)
            for candidate in candidates
        ]
