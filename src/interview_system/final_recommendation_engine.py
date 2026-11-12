"""
ZECPATH-AI Day 52
Final Recommendation AI Engine

Features:
- Selected / Hold / Review / Rejected recommendations
- Hybrid score and rule-based decision logic
- Decision confidence based on evidence completeness
- Integrity risk assessment
- Behavioral context safeguards
- Explainable recommendation output
- JSON and Markdown reports

This is a human-supervised decision-support prototype.
It does not automatically hire or reject candidates.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any
import json


@dataclass
class CandidateDecisionInput:

    candidate_id: str
    candidate_name: str
    target_role: str

    hiring_fit_score: float

    available_stages: int = 5
    total_stages: int = 5

    integrity_flags: int = 0

    confirmed_integrity_breach: bool = False

    human_integrity_review_completed: bool = False

    behavioral_focus_score: Optional[float] = None

    technical_requirements_met: bool = True

    evidence_verified: bool = True


class FinalRecommendationEngine:

    def __init__(self):

        # Configurable research thresholds.
        self.thresholds = {
            "selected": 80.0,
            "hold": 55.0
        }

        # Confidence is based on evidence completeness.
        self.confidence_weights = {
            "stage_completeness": 0.50,
            "evidence_verification": 0.30,
            "integrity_review": 0.20
        }

    # --------------------------------------------------------
    # MAIN DECISION METHOD
    # --------------------------------------------------------

    def evaluate(self, candidate: CandidateDecisionInput):

        self._validate(candidate)

        score = float(candidate.hiring_fit_score)

        reasons = []
        risk_factors = []
        safeguards = []

        # ----------------------------------------------------
        # 1. EVIDENCE COMPLETENESS
        # ----------------------------------------------------

        stage_completeness = (
            candidate.available_stages
            / candidate.total_stages
        ) * 100

        evidence_score = (
            100.0 if candidate.evidence_verified else 50.0
        )

        integrity_review_score = (
            100.0
            if candidate.human_integrity_review_completed
            else 50.0
        )

        confidence = (
            stage_completeness
            * self.confidence_weights["stage_completeness"]
            +
            evidence_score
            * self.confidence_weights["evidence_verification"]
            +
            integrity_review_score
            * self.confidence_weights["integrity_review"]
        )

        confidence = round(confidence, 2)

        # ----------------------------------------------------
        # 2. INTEGRITY RISK ANALYSIS
        # ----------------------------------------------------

        if candidate.integrity_flags > 0:

            risk_factors.append({
                "factor": "UNRESOLVED_INTEGRITY_FLAGS",
                "count": candidate.integrity_flags,
                "severity": "REVIEW_REQUIRED",
                "explanation": (
                    "Integrity alerts require contextual human review. "
                    "An alert alone is not proof of misconduct."
                )
            })

            reasons.append(
                "Unresolved integrity alerts require human review."
            )

        if candidate.confirmed_integrity_breach:

            risk_factors.append({
                "factor": "CONFIRMED_INTEGRITY_BREACH",
                "count": 1,
                "severity": "HIGH",
                "explanation": (
                    "A breach has been marked as confirmed. "
                    "The decision must be reviewed by an authorized human."
                )
            })

            reasons.append(
                "A confirmed integrity issue requires authorized human review."
            )

        # ----------------------------------------------------
        # 3. BEHAVIORAL CONTEXT
        # ----------------------------------------------------

        if candidate.behavioral_focus_score is not None:

            safeguards.append(
                "Behavioral focus is contextual information only."
            )

            safeguards.append(
                "Gaze, facial expression, head movement, and nervous "
                "gestures are not used as negative hiring signals."
            )

            if candidate.behavioral_focus_score < 50:

                risk_factors.append({
                    "factor": "LOW_TASK_FOCUS_OBSERVATION",
                    "value": candidate.behavioral_focus_score,
                    "severity": "CONTEXT_ONLY",
                    "explanation": (
                        "A task-focus observation requires contextual "
                        "interpretation and must not independently "
                        "determine the hiring outcome."
                    )
                })

        # ----------------------------------------------------
        # 4. TECHNICAL REQUIREMENT CHECK
        # ----------------------------------------------------

        if not candidate.technical_requirements_met:

            reasons.append(
                "One or more documented essential technical requirements "
                "were not met."
            )

        # ----------------------------------------------------
        # 5. HYBRID DECISION LOGIC
        # ----------------------------------------------------

        # Rule priority:
        # A confirmed integrity breach never triggers automatic rejection.
        # It routes the case to human review.

        if candidate.confirmed_integrity_breach:

            decision = "HOLD / REVIEW"

            reasons.append(
                "Final outcome is deferred pending authorized review."
            )

        elif candidate.integrity_flags > 0:

            decision = "HOLD / REVIEW"

        elif not candidate.evidence_verified:

            decision = "HOLD / REVIEW"

            reasons.append(
                "Evaluation evidence has not been verified."
            )

        elif candidate.available_stages < candidate.total_stages:

            decision = "HOLD / REVIEW"

            reasons.append(
                "Some evaluation stages are incomplete."
            )

        elif confidence < 75:

            decision = "HOLD / REVIEW"

            reasons.append(
                "Decision confidence is below the required threshold."
            )

        elif not candidate.technical_requirements_met:

            decision = "REJECTED"

            reasons.append(
                "The documented essential technical requirement "
                "condition was not met."
            )

        elif score >= self.thresholds["selected"]:

            decision = "SELECTED"

            reasons.append(
                "Candidate achieved the required Hiring Fit Score."
            )

        elif score >= self.thresholds["hold"]:

            decision = "HOLD / REVIEW"

            reasons.append(
                "Candidate score requires additional assessment."
            )

        else:

            decision = "REJECTED"

            reasons.append(
                "Candidate score is below the configured minimum threshold."
            )

        # ----------------------------------------------------
        # 6. DECISION EXPLANATION
        # ----------------------------------------------------

        explanation = self._generate_explanation(
            candidate,
            decision,
            confidence,
            reasons,
            risk_factors
        )

        # ----------------------------------------------------
        # 7. FINAL DECISION OBJECT
        # ----------------------------------------------------

        result = {

            "project": "ZECPATH-AI",

            "day": 52,

            "module": "Final Recommendation AI",

            "candidate": {
                "candidate_id": candidate.candidate_id,
                "candidate_name": candidate.candidate_name,
                "target_role": candidate.target_role
            },

            "decision": {

                "recommendation": decision,

                "hiring_fit_score": round(score, 2),

                "confidence_score": confidence,

                "confidence_meaning": (
                    "Evidence completeness and verification indicator, "
                    "not probability of a correct decision."
                ),

                "decision_status": (
                    "PENDING_HUMAN_APPROVAL"
                ),

                "automatic_hiring_action": False
            },

            "decision_logic": {

                "method": "HYBRID_SCORE_AND_RULE_BASED",

                "thresholds": self.thresholds,

                "selected_threshold": self.thresholds["selected"],

                "hold_threshold": self.thresholds["hold"],

                "rejection_rule": (
                    "Below configured minimum score or failure to meet "
                    "a documented essential technical requirement, "
                    "subject to human review."
                )
            },

            "evidence_completeness": {

                "available_stages": candidate.available_stages,

                "total_stages": candidate.total_stages,

                "stage_completeness": round(stage_completeness, 2),

                "evidence_verified": candidate.evidence_verified,

                "integrity_review_completed": (
                    candidate.human_integrity_review_completed
                )
            },

            "risk_assessment": {

                "integrity_flags": candidate.integrity_flags,

                "confirmed_integrity_breach": (
                    candidate.confirmed_integrity_breach
                ),

                "behavioral_focus_score": (
                    candidate.behavioral_focus_score
                ),

                "risk_factors": risk_factors
            },

            "explanation": {

                "summary": explanation,

                "reasons": reasons,

                "safeguards": safeguards
            },

            "human_review": {

                "required": True,

                "approval_required_before_final_action": True,

                "automatic_rejection_disabled_for_integrity_alerts": True,

                "reviewer_must_document_reason": True
            }
        }

        return result

    # --------------------------------------------------------
    # EXPLANATION GENERATION
    # --------------------------------------------------------

    @staticmethod
    def _generate_explanation(
        candidate,
        decision,
        confidence,
        reasons,
        risk_factors
    ):

        return (
            f"{candidate.candidate_name} received a "
            f"{decision} recommendation for "
            f"{candidate.target_role}. "
            f"The Hiring Fit Score is "
            f"{candidate.hiring_fit_score:.2f}/100 "
            f"and evidence confidence is {confidence:.2f}/100. "
            f"There are {len(risk_factors)} identified risk factor(s). "
            f"Human approval is required before any final hiring action."
        )

    # --------------------------------------------------------
    # INPUT VALIDATION
    # --------------------------------------------------------

    @staticmethod
    def _validate(candidate):

        if not candidate.candidate_id.strip():
            raise ValueError("Candidate ID cannot be empty.")

        if not candidate.candidate_name.strip():
            raise ValueError("Candidate name cannot be empty.")

        if not candidate.target_role.strip():
            raise ValueError("Target role cannot be empty.")

        if not 0 <= candidate.hiring_fit_score <= 100:
            raise ValueError(
                "Hiring Fit Score must be between 0 and 100."
            )

        if candidate.total_stages <= 0:
            raise ValueError(
                "Total stages must be greater than zero."
            )

        if not (
            0 <= candidate.available_stages
            <= candidate.total_stages
        ):
            raise ValueError(
                "Available stages must be between zero and total stages."
            )

        if candidate.integrity_flags < 0:
            raise ValueError(
                "Integrity flag count cannot be negative."
            )

        if candidate.behavioral_focus_score is not None:

            if not 0 <= candidate.behavioral_focus_score <= 100:
                raise ValueError(
                    "Behavioral focus score must be between 0 and 100."
                )

    # --------------------------------------------------------
    # JSON REPORT
    # --------------------------------------------------------

    @staticmethod
    def save_json_report(result, output_path):

        path = Path(output_path)

        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as file:

            json.dump(result, file, indent=4)

        return str(path)

    # --------------------------------------------------------
    # MARKDOWN REPORT
    # --------------------------------------------------------

    @staticmethod
    def save_markdown_report(result, output_path):

        path = Path(output_path)

        path.parent.mkdir(parents=True, exist_ok=True)

        decision = result["decision"]

        lines = [

            "# ZECPATH-AI Final Recommendation Report",

            "",

            "## Candidate Information",

            f"- Candidate ID: {result['candidate']['candidate_id']}",

            f"- Candidate Name: {result['candidate']['candidate_name']}",

            f"- Target Role: {result['candidate']['target_role']}",

            "",

            "## Final Recommendation",

            f"- Decision: {decision['recommendation']}",

            f"- Hiring Fit Score: {decision['hiring_fit_score']}/100",

            f"- Confidence Score: {decision['confidence_score']}/100",

            f"- Status: {decision['decision_status']}",

            "",

            "## Explanation",

            result["explanation"]["summary"],

            "",

            "## Decision Reasons"

        ]

        for reason in result["explanation"]["reasons"]:

            lines.append(f"- {reason}")

        lines.extend([

            "",

            "## Risk Factors"

        ])

        for risk in result["risk_assessment"]["risk_factors"]:

            lines.append(
                f"- {risk['factor']}: {risk['explanation']}"
            )

        lines.extend([

            "",

            "## Evidence Completeness",

            f"- Available stages: "
            f"{result['evidence_completeness']['available_stages']}",

            f"- Total stages: "
            f"{result['evidence_completeness']['total_stages']}",

            "",

            "## Human Review",

            "- Human approval required: Yes",

            "- Automatic hiring action: Disabled",

            "- Reviewer must document the decision.",

            "",

            "## Confidence Interpretation",

            "Confidence represents evidence completeness and verification. "
            "It is not the probability that the decision is correct.",

            ""

        ])

        path.write_text(
            "\n".join(lines),
            encoding="utf-8"
        )

        return str(path)


if __name__ == "__main__":

    engine = FinalRecommendationEngine()

    candidate = CandidateDecisionInput(

        candidate_id="CAND-052",

        candidate_name="Demo Candidate",

        target_role="Data Analyst",

        hiring_fit_score=88,

        available_stages=5,

        total_stages=5,

        integrity_flags=0,

        confirmed_integrity_breach=False,

        human_integrity_review_completed=True,

        behavioral_focus_score=85,

        technical_requirements_met=True,

        evidence_verified=True
    )

    result = engine.evaluate(candidate)

    engine.save_json_report(
        result,
        "outputs/day52/final_recommendation.json"
    )

    engine.save_markdown_report(
        result,
        "outputs/day52/final_recommendation.md"
    )

    print("\nFINAL RECOMMENDATION")
    print("=" * 45)

    print("Candidate:", candidate.candidate_name)

    print(
        "Recommendation:",
        result["decision"]["recommendation"]
    )

    print(
        "Hiring Fit Score:",
        result["decision"]["hiring_fit_score"]
    )

    print(
        "Confidence Score:",
        result["decision"]["confidence_score"]
    )

    print(
        "Human Approval Required:",
        result["human_review"]["required"]
    )

    print("\nJSON report generated.")
    print("Markdown report generated.")
