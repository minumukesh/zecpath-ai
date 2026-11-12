import unittest

from src.eligibility_decision.engine import (
    EligibilityDecisionEngine,
    EligibilityRule
)


class TestEligibilityDecisionEngine(unittest.TestCase):

    def setUp(self):

        rule = EligibilityRule(
            role="Data Analyst",
            minimum_ats_score=70,
            review_ats_score=50,
            mandatory_skills=["Python", "SQL"],
            min_experience_years=0,
            max_experience_years=None,
            allowed_locations=[],
            availability_required=False
        )

        self.engine = EligibilityDecisionEngine({
            "Data Analyst": rule
        })

    def test_eligible_candidate(self):

        candidate = {
            "candidate_id": "T001",
            "candidate_name": "Test Candidate",
            "ats_score": 80,
            "skills": ["Python", "SQL", "Excel"],
            "experience_years": 2,
            "location": "Kochi",
            "available": True
        }

        result = self.engine.evaluate_candidate(
            candidate,
            "Data Analyst"
        )

        self.assertEqual(result["decision"], "ELIGIBLE")
        self.assertTrue(result["eligible_for_ai_screening"])

    def test_review_candidate(self):

        candidate = {
            "candidate_id": "T002",
            "candidate_name": "Review Candidate",
            "ats_score": 60,
            "skills": ["Python", "SQL"],
            "experience_years": 1,
            "location": "Kochi",
            "available": True
        }

        result = self.engine.evaluate_candidate(
            candidate,
            "Data Analyst"
        )

        self.assertEqual(result["decision"], "REVIEW")
        self.assertFalse(result["eligible_for_ai_screening"])

    def test_rejected_low_score(self):

        candidate = {
            "candidate_id": "T003",
            "candidate_name": "Low Score Candidate",
            "ats_score": 40,
            "skills": ["Python", "SQL"],
            "experience_years": 1,
            "location": "Kochi",
            "available": True
        }

        result = self.engine.evaluate_candidate(
            candidate,
            "Data Analyst"
        )

        self.assertEqual(result["decision"], "REJECTED")

    def test_rejected_missing_mandatory_skill(self):

        candidate = {
            "candidate_id": "T004",
            "candidate_name": "Missing Skill Candidate",
            "ats_score": 85,
            "skills": ["Python"],
            "experience_years": 2,
            "location": "Kochi",
            "available": True
        }

        result = self.engine.evaluate_candidate(
            candidate,
            "Data Analyst"
        )

        self.assertEqual(result["decision"], "REJECTED")
        self.assertIn(
            "mandatory_skills",
            result["failed_rules"]
        )

    def test_role_configuration(self):

        rule = self.engine.get_rule("Data Analyst")

        self.assertEqual(
            rule.minimum_ats_score,
            70
        )

        self.assertEqual(
            rule.review_ats_score,
            50
        )


if __name__ == "__main__":
    unittest.main()
