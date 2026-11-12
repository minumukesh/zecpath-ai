import unittest

from src.interview_system.final_recommendation_engine import (
    FinalRecommendationEngine,
    CandidateDecisionInput
)


class TestFinalRecommendationEngine(unittest.TestCase):

    def setUp(self):

        self.engine = FinalRecommendationEngine()

    def make_candidate(self, **changes):

        values = {

            "candidate_id": "TEST-052",

            "candidate_name": "Test Candidate",

            "target_role": "Data Analyst",

            "hiring_fit_score": 90,

            "available_stages": 5,

            "total_stages": 5,

            "integrity_flags": 0,

            "confirmed_integrity_breach": False,

            "human_integrity_review_completed": True,

            "behavioral_focus_score": None,

            "technical_requirements_met": True,

            "evidence_verified": True
        }

        values.update(changes)

        return CandidateDecisionInput(**values)

    def test_evaluation_completes(self):

        result = self.engine.evaluate(
            self.make_candidate()
        )

        self.assertIn("decision", result)

    def test_selected_decision(self):

        result = self.engine.evaluate(
            self.make_candidate(hiring_fit_score=90)
        )

        self.assertEqual(
            result["decision"]["recommendation"],
            "SELECTED"
        )

    def test_hold_decision(self):

        result = self.engine.evaluate(
            self.make_candidate(hiring_fit_score=70)
        )

        self.assertEqual(
            result["decision"]["recommendation"],
            "HOLD / REVIEW"
        )

    def test_rejected_decision(self):

        result = self.engine.evaluate(
            self.make_candidate(hiring_fit_score=40)
        )

        self.assertEqual(
            result["decision"]["recommendation"],
            "REJECTED"
        )

    def test_integrity_flags_force_review(self):

        result = self.engine.evaluate(
            self.make_candidate(
                integrity_flags=3
            )
        )

        self.assertEqual(
            result["decision"]["recommendation"],
            "HOLD / REVIEW"
        )

    def test_confirmed_integrity_breach_does_not_auto_reject(self):

        result = self.engine.evaluate(
            self.make_candidate(
                confirmed_integrity_breach=True,
                hiring_fit_score=95
            )
        )

        self.assertEqual(
            result["decision"]["recommendation"],
            "HOLD / REVIEW"
        )

    def test_missing_stages_force_review(self):

        result = self.engine.evaluate(
            self.make_candidate(available_stages=3)
        )

        self.assertEqual(
            result["decision"]["recommendation"],
            "HOLD / REVIEW"
        )

    def test_unverified_evidence_forces_review(self):

        result = self.engine.evaluate(
            self.make_candidate(evidence_verified=False)
        )

        self.assertEqual(
            result["decision"]["recommendation"],
            "HOLD / REVIEW"
        )

    def test_failed_technical_requirement(self):

        result = self.engine.evaluate(
            self.make_candidate(
                technical_requirements_met=False
            )
        )

        self.assertEqual(
            result["decision"]["recommendation"],
            "REJECTED"
        )

    def test_confidence_score_range(self):

        result = self.engine.evaluate(
            self.make_candidate()
        )

        confidence = result["decision"]["confidence_score"]

        self.assertGreaterEqual(confidence, 0)

        self.assertLessEqual(confidence, 100)

    def test_behavioral_focus_is_not_direct_rejection_factor(self):

        result = self.engine.evaluate(
            self.make_candidate(
                behavioral_focus_score=10,
                hiring_fit_score=90
            )
        )

        self.assertEqual(
            result["decision"]["recommendation"],
            "SELECTED"
        )

    def test_human_approval_required(self):

        result = self.engine.evaluate(
            self.make_candidate()
        )

        self.assertTrue(
            result["human_review"]["approval_required_before_final_action"]
        )

    def test_automatic_hiring_action_disabled(self):

        result = self.engine.evaluate(
            self.make_candidate()
        )

        self.assertFalse(
            result["decision"]["automatic_hiring_action"]
        )

    def test_invalid_hiring_fit_score(self):

        with self.assertRaises(ValueError):

            self.engine.evaluate(
                self.make_candidate(hiring_fit_score=150)
            )

    def test_invalid_stage_count(self):

        with self.assertRaises(ValueError):

            self.engine.evaluate(
                self.make_candidate(available_stages=6)
            )

    def test_invalid_integrity_count(self):

        with self.assertRaises(ValueError):

            self.engine.evaluate(
                self.make_candidate(integrity_flags=-1)
            )

    def test_invalid_behavioral_score(self):

        with self.assertRaises(ValueError):

            self.engine.evaluate(
                self.make_candidate(behavioral_focus_score=150)
            )

    def test_empty_candidate_id(self):

        with self.assertRaises(ValueError):

            self.engine.evaluate(
                self.make_candidate(candidate_id="")
            )


if __name__ == "__main__":
    unittest.main()
