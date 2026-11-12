import unittest

from src.ats_scoring import (
    ROLE_WEIGHTS,
    get_role_weights,
    normalize_score,
    calculate_component_score,
    classify_candidate,
    generate_candidate_score,
)


class TestATSScoring(unittest.TestCase):

    def test_role_weights(self):
        for role, weights in ROLE_WEIGHTS.items():
            self.assertAlmostEqual(sum(weights.values()), 1.0)

    def test_score_normalization(self):
        self.assertEqual(normalize_score(1.5), 1.0)
        self.assertEqual(normalize_score(-0.5), 0.0)
        self.assertEqual(normalize_score(None), 0.0)

    def test_weighted_score(self):
        score = calculate_component_score(
            1.0, 1.0, 1.0, 1.0, "Data Analyst"
        )
        self.assertEqual(score, 100.0)

    def test_candidate_classification(self):
        self.assertEqual(classify_candidate(85), "Excellent Match")
        self.assertEqual(classify_candidate(70), "Strong Match")
        self.assertEqual(classify_candidate(55), "Moderate Match")
        self.assertEqual(classify_candidate(40), "Weak Match")
        self.assertEqual(classify_candidate(20), "Low Match")

    def test_candidate_score_generator(self):
        result = generate_candidate_score(
            candidate_name="Test Candidate",
            role="Data Analyst",
            skill_match=0.90,
            experience_relevance=0.80,
            education_alignment=0.85,
            semantic_similarity=0.75,
        )

        self.assertIn("ats_score", result)
        self.assertIn("category", result)
        self.assertIn("weights", result)
        self.assertIn("scores", result)
        self.assertIn("explanation", result)

    def test_missing_data(self):
        result = generate_candidate_score(
            candidate_name="Missing Experience Candidate",
            role="Data Analyst",
            skill_match=0.75,
            experience_relevance=None,
            education_alignment=0.80,
            semantic_similarity=0.70,
        )

        self.assertEqual(result["scores"]["experience_relevance"], 0.0)
        self.assertIn(
            "experience_relevance",
            result["explanation"]["missing_data"]
        )


if __name__ == "__main__":
    unittest.main()
