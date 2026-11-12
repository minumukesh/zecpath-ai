"""Transparent demonstration HR interview scoring."""

from .config import HR_SCORE_WEIGHTS

class HRInterviewEngine:
    def validate_scores(self, scores):
        if not isinstance(scores, dict):
            raise ValueError("Scores must be a JSON object.")
        if set(scores) != set(HR_SCORE_WEIGHTS):
            raise ValueError("All four HR score categories are required.")
        for name, value in scores.items():
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{name} must be numeric.")
            if not 0 <= value <= 100:
                raise ValueError(f"{name} must be between 0 and 100.")

    def calculate_score(self, scores):
        self.validate_scores(scores)
        breakdown = {}
        total = 0.0
        for name, weight in HR_SCORE_WEIGHTS.items():
            contribution = float(scores[name]) * weight
            breakdown[name] = {
                "score": float(scores[name]),
                "weight": weight,
                "weighted_contribution": round(contribution, 2)
            }
            total += contribution
        return {"overall_score": round(total, 2), "breakdown": breakdown}

    def recommendation(self, score):
        if score >= 85:
            return "STRONGLY_RECOMMEND"
        if score >= 70:
            return "RECOMMEND"
        if score >= 50:
            return "HOLD"
        return "NOT_RECOMMENDED"

    def evaluate_candidate(self, candidate_id, candidate_name, role, scores, feedback=""):
        if not isinstance(candidate_id, str) or not candidate_id.strip():
            raise ValueError("Candidate ID is required.")
        if not isinstance(candidate_name, str) or not candidate_name.strip():
            raise ValueError("Candidate name is required.")
        if not isinstance(role, str) or not role.strip():
            raise ValueError("Role is required.")
        if not isinstance(feedback, str):
            raise ValueError("Manager feedback must be text.")
        calculated = self.calculate_score(scores)
        score = calculated["overall_score"]
        return {
            "candidate_id": candidate_id,
            "candidate_name": candidate_name,
            "role": role,
            "interview_type": "HR",
            "score": score,
            "score_breakdown": calculated["breakdown"],
            "recommendation": self.recommendation(score),
            "manager_feedback": feedback,
            "evaluation_status": "completed",
            "note": "Demonstration result. Final hiring decisions require authorized human review."
        }