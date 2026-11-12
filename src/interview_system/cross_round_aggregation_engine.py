"""
ZECPATH-AI Day 51
Cross-Round Aggregation Engine

Combines:
1. ATS
2. Screening
3. HR Interview
4. Technical Interview
5. Machine Test

Features:
- Role-specific weights
- Score normalization
- Missing-stage handling
- Explainable score contributions
- Unified candidate score object
- Hiring Fit Score calculation

This is a transparent decision-support prototype.
It does not make automatic hiring decisions.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from pathlib import Path
import json


STAGES = [
    "ats",
    "screening",
    "hr_interview",
    "technical_interview",
    "machine_test"
]


DEFAULT_ROLE_WEIGHTS = {
    "data_analyst": {
        "ats": 0.10,
        "screening": 0.15,
        "hr_interview": 0.15,
        "technical_interview": 0.30,
        "machine_test": 0.30
    },

    "data_scientist": {
        "ats": 0.10,
        "screening": 0.10,
        "hr_interview": 0.10,
        "technical_interview": 0.35,
        "machine_test": 0.35
    },

    "software_developer": {
        "ats": 0.10,
        "screening": 0.10,
        "hr_interview": 0.10,
        "technical_interview": 0.30,
        "machine_test": 0.40
    },

    "business_analyst": {
        "ats": 0.10,
        "screening": 0.20,
        "hr_interview": 0.20,
        "technical_interview": 0.25,
        "machine_test": 0.25
    },

    "general": {
        "ats": 0.20,
        "screening": 0.20,
        "hr_interview": 0.20,
        "technical_interview": 0.20,
        "machine_test": 0.20
    }
}


@dataclass
class CandidateStageScores:

    candidate_id: str

    candidate_name: str

    target_role: str

    ats: Optional[float] = None

    screening: Optional[float] = None

    hr_interview: Optional[float] = None

    technical_interview: Optional[float] = None

    machine_test: Optional[float] = None

    profile_group: str = "standard"


class CrossRoundAggregationEngine:

    def __init__(self, custom_weights=None):

        self.role_weights = dict(DEFAULT_ROLE_WEIGHTS)

        if custom_weights:
            for role, weights in custom_weights.items():
                self._validate_weights(weights)
                self.role_weights[role.lower()] = weights.copy()

    # --------------------------------------------------------
    # MAIN AGGREGATION METHOD
    # --------------------------------------------------------

    def aggregate(self, candidate: CandidateStageScores):

        self._validate_candidate(candidate)

        role = candidate.target_role.lower().replace(" ", "_")

        if role not in self.role_weights:
            role = "general"

        configured_weights = self.role_weights[role]

        # Collect available scores.
        available_scores = {}

        for stage in STAGES:

            score = getattr(candidate, stage)

            if score is not None:
                available_scores[stage] = float(score)

        if not available_scores:
            raise ValueError(
                "At least one evaluation stage score is required."
            )

        # Normalize weights across available stages.
        # This prevents missing stages from being treated as zero.
        available_weight_total = sum(
            configured_weights[stage]
            for stage in available_scores
        )

        if available_weight_total <= 0:
            raise ValueError(
                "Available stage weights must total more than zero."
            )

        normalized_weights = {
            stage: configured_weights[stage] / available_weight_total
            for stage in available_scores
        }

        # Calculate individual stage contributions.
        contributions = {}

        for stage, score in available_scores.items():

            weight = normalized_weights[stage]

            contributions[stage] = {
                "raw_score": round(score, 2),
                "original_role_weight": configured_weights[stage],
                "normalized_weight": round(weight, 4),
                "weighted_contribution": round(score * weight, 2)
            }

        # Calculate unified hiring fit score.
        hiring_fit_score = sum(
            available_scores[stage] * normalized_weights[stage]
            for stage in available_scores
        )

        hiring_fit_score = round(
            max(0.0, min(100.0, hiring_fit_score)),
            2
        )

        # ----------------------------------------------------
        # PROFILE NORMALIZATION
        # ----------------------------------------------------

        profile_result = self._normalize_profile(
            hiring_fit_score,
            candidate.profile_group
        )

        # ----------------------------------------------------
        # PERFORMANCE CLASSIFICATION
        # ----------------------------------------------------

        if hiring_fit_score >= 85:
            performance = "EXCELLENT"

        elif hiring_fit_score >= 70:
            performance = "STRONG"

        elif hiring_fit_score >= 55:
            performance = "MODERATE"

        else:
            performance = "DEVELOPMENT_REQUIRED"

        # ----------------------------------------------------
        # STAGE ANALYSIS
        # ----------------------------------------------------

        strongest_stage = max(
            available_scores,
            key=available_scores.get
        )

        weakest_stage = min(
            available_scores,
            key=available_scores.get
        )

        missing_stages = [
            stage for stage in STAGES
            if stage not in available_scores
        ]

        # ----------------------------------------------------
        # EXPLAINABLE RESULT
        # ----------------------------------------------------

        explanation = self._generate_explanation(
            hiring_fit_score,
            contributions,
            missing_stages
        )

        # ----------------------------------------------------
        # UNIFIED CANDIDATE OBJECT
        # ----------------------------------------------------

        result = {

            "project": "ZECPATH-AI",

            "day": 51,

            "module": "Cross-Round Aggregation Engine",

            "candidate": {
                "candidate_id": candidate.candidate_id,
                "candidate_name": candidate.candidate_name,
                "target_role": candidate.target_role,
                "profile_group": candidate.profile_group
            },

            "stage_scores": {
                stage: (
                    round(getattr(candidate, stage), 2)
                    if getattr(candidate, stage) is not None
                    else None
                )
                for stage in STAGES
            },

            "aggregation": {

                "hiring_fit_score": hiring_fit_score,

                "performance_category": performance,

                "available_stages": list(available_scores.keys()),

                "missing_stages": missing_stages,

                "available_stage_count": len(available_scores),

                "total_stage_count": len(STAGES),

                "stage_contributions": contributions,

                "strongest_stage": strongest_stage,

                "weakest_stage": weakest_stage
            },

            "role_weighting": {

                "selected_role": role,

                "configured_weights": configured_weights,

                "normalized_weights": {
                    stage: round(weight, 6)
                    for stage, weight in normalized_weights.items()
                }
            },

            "profile_normalization": profile_result,

            "explanation": explanation,

            "decision_policy": {

                "automatic_hiring_decision": False,

                "human_review_required": True,

                "missing_stage_scores_treated_as_zero": False,

                "score_is_probability_of_success": False
            }
        }

        return result

    # --------------------------------------------------------
    # PROFILE NORMALIZATION
    # --------------------------------------------------------

    @staticmethod
    def _normalize_profile(score, profile_group):

        """
        Applies a transparent profile-group adjustment.

        The current research prototype uses a neutral baseline
        for every profile group. No demographic adjustment is
        applied.

        This method is designed for future validated,
        job-relevant normalization methods.
        """

        supported_groups = [
            "standard",
            "experienced",
            "entry_level",
            "career_transition"
        ]

        if profile_group not in supported_groups:
            raise ValueError("Unsupported candidate profile group.")

        return {

            "profile_group": profile_group,

            "raw_hiring_fit_score": round(score, 2),

            "normalized_hiring_fit_score": round(score, 2),

            "adjustment": 0.0,

            "method": "NEUTRAL_BASELINE",

            "explanation": (
                "No profile-based score adjustment is applied. "
                "All candidates are evaluated using the same "
                "job-relevant scoring framework."
            )
        }

    # --------------------------------------------------------
    # EXPLANATION GENERATION
    # --------------------------------------------------------

    @staticmethod
    def _generate_explanation(
        hiring_fit_score,
        contributions,
        missing_stages
    ):

        strongest_contribution = max(
            contributions.items(),
            key=lambda item: item[1]["weighted_contribution"]
        )

        weakest_contribution = min(
            contributions.items(),
            key=lambda item: item[1]["weighted_contribution"]
        )

        explanation = {

            "summary": (
                f"The candidate achieved a Hiring Fit Score of "
                f"{hiring_fit_score} out of 100."
            ),

            "strongest_weighted_contribution": {
                "stage": strongest_contribution[0],
                "contribution": strongest_contribution[1][
                    "weighted_contribution"
                ]
            },

            "weakest_weighted_contribution": {
                "stage": weakest_contribution[0],
                "contribution": weakest_contribution[1][
                    "weighted_contribution"
                ]
            },

            "missing_stage_warning": (
                f"Missing stages: {', '.join(missing_stages)}"
                if missing_stages
                else "All five evaluation stages are available."
            )
        }

        return explanation

    # --------------------------------------------------------
    # INPUT VALIDATION
    # --------------------------------------------------------

    @staticmethod
    def _validate_candidate(candidate):

        if not candidate.candidate_id.strip():
            raise ValueError("Candidate ID cannot be empty.")

        if not candidate.candidate_name.strip():
            raise ValueError("Candidate name cannot be empty.")

        if not candidate.target_role.strip():
            raise ValueError("Target role cannot be empty.")

        for stage in STAGES:

            score = getattr(candidate, stage)

            if score is not None:

                if not isinstance(score, (int, float)):
                    raise ValueError(
                        f"{stage} score must be numeric."
                    )

                if not 0 <= score <= 100:
                    raise ValueError(
                        f"{stage} score must be between 0 and 100."
                    )

    @staticmethod
    def _validate_weights(weights):

        if set(weights.keys()) != set(STAGES):
            raise ValueError(
                "Custom weights must contain all five evaluation stages."
            )

        if any(
            not isinstance(value, (int, float)) or value < 0
            for value in weights.values()
        ):
            raise ValueError(
                "Weights must be non-negative numbers."
            )

        if abs(sum(weights.values()) - 1.0) > 0.0001:
            raise ValueError(
                "Role weights must add up to 1.0."
            )

    # --------------------------------------------------------
    # REPORT GENERATION
    # --------------------------------------------------------

    @staticmethod
    def save_json_report(result, output_path):

        path = Path(output_path)

        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as file:
            json.dump(result, file, indent=4)

        return str(path)

    @staticmethod
    def save_markdown_report(result, output_path):

        path = Path(output_path)

        path.parent.mkdir(parents=True, exist_ok=True)

        aggregation = result["aggregation"]

        lines = [

            "# ZECPATH-AI Hiring Intelligence Report",

            "",

            "## Candidate Information",

            f"- Candidate ID: {result['candidate']['candidate_id']}",

            f"- Candidate Name: {result['candidate']['candidate_name']}",

            f"- Target Role: {result['candidate']['target_role']}",

            "",

            "## Hiring Fit Result",

            f"- Hiring Fit Score: {aggregation['hiring_fit_score']}/100",

            f"- Performance: {aggregation['performance_category']}",

            "",

            "## Evaluation Stage Scores",

            "| Stage | Score | Original Weight | Normalized Weight | Contribution |",

            "|---|---:|---:|---:|---:|"
        ]

        for stage, data in aggregation["stage_contributions"].items():

            lines.append(
                f"| {stage.replace('_', ' ').title()} "
                f"| {data['raw_score']} "
                f"| {data['original_role_weight']} "
                f"| {data['normalized_weight']} "
                f"| {data['weighted_contribution']} |"
            )

        lines.extend([

            "",

            "## Missing Evaluation Stages",

            ", ".join(aggregation["missing_stages"])
            if aggregation["missing_stages"]
            else "None",

            "",

            "## Explanation",

            result["explanation"]["summary"],

            "",

            result["explanation"]["missing_stage_warning"],

            "",

            "## Decision Policy",

            "- Automatic hiring decision: Disabled",

            "- Human review required: Yes",

            "- Missing stages treated as zero: No",

            "- Score is not a probability of job success.",

            ""
        ])

        path.write_text("\n".join(lines), encoding="utf-8")

        return str(path)


def main():

    engine = CrossRoundAggregationEngine()

    candidate = CandidateStageScores(

        candidate_id="CAND-051",

        candidate_name="Demo Candidate",

        target_role="data_analyst",

        ats=85,

        screening=80,

        hr_interview=88,

        technical_interview=90,

        machine_test=92,

        profile_group="entry_level"
    )

    result = engine.aggregate(candidate)

    engine.save_json_report(
        result,
        "outputs/day51/unified_candidate_score.json"
    )

    engine.save_markdown_report(
        result,
        "outputs/day51/hiring_intelligence_report.md"
    )

    print("\nCROSS-ROUND AGGREGATION RESULT")
    print("=" * 48)

    print("Candidate:", candidate.candidate_name)

    print("Role:", candidate.target_role)

    print(
        "Hiring Fit Score:",
        result["aggregation"]["hiring_fit_score"]
    )

    print(
        "Performance:",
        result["aggregation"]["performance_category"]
    )

    print(
        "Strongest stage:",
        result["aggregation"]["strongest_stage"]
    )

    print(
        "Weakest stage:",
        result["aggregation"]["weakest_stage"]
    )

    print(
        "Available stages:",
        result["aggregation"]["available_stage_count"]
    )

    print("\nJSON report generated.")

    print("Markdown report generated.")


if __name__ == "__main__":
    main()
