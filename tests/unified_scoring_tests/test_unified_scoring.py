import unittest

from src.unified_scoring.engine import (
    get_role_weights,
    validate_score,
    calculate_unified_score,
    generate_unified_score
)


class TestUnifiedScoring(unittest.TestCase):

    def test_role_weights_total_100(self):

        for role in [
            "Data Analyst",
            "Software Developer",
            "Business Analyst",
            "HR Executive",
            "Unknown Role"
        ]:

            weights = get_role_weights(role)

            self.assertEqual(
                sum(weights.values()),
                100
            )

    def test_data_analyst_weights(self):

        weights = get_role_weights("Data Analyst")

        self.assertEqual(weights["ats"], 45)
        self.assertEqual(weights["screening"], 25)
        self.assertEqual(weights["hr_interview"], 30)

    def test_unified_score_calculation(self):

        result = calculate_unified_score(
            ats_score=80,
            screening_score=70,
            hr_interview_score=90,
            weights={
                "ats": 40,
                "screening": 30,
                "hr_interview": 30
            }
        )

        self.assertEqual(
            result["unified_score"],
            80.0
        )

    def test_hiring_fit_percentage(self):

        result = calculate_unified_score(
            80,
            70,
            90,
            {
                "ats": 40,
                "screening": 30,
                "hr_interview": 30
            }
        )

        self.assertEqual(
            result["hiring_fit_percentage"],
            80.0
        )

    def test_missing_component_weight_normalization(self):

        result = calculate_unified_score(
            80,
            None,
            90,
            {
                "ats": 40,
                "screening": 30,
                "hr_interview": 30
            }
        )

        self.assertEqual(
            result["unified_score"],
            84.29
        )

        self.assertEqual(
            result["missing_components"],
            ["screening"]
        )

    def test_all_missing_scores_rejected(self):

        with self.assertRaises(ValueError):

            calculate_unified_score(
                None,
                None,
                None,
                {
                    "ats": 40,
                    "screening": 30,
                    "hr_interview": 30
                }
            )

    def test_invalid_score_rejected(self):

        with self.assertRaises(ValueError):
            validate_score(120, "ats")

    def test_negative_score_rejected(self):

        with self.assertRaises(ValueError):
            validate_score(-10, "screening")

    def test_zero_score_is_valid(self):

        self.assertEqual(
            validate_score(0, "ats"),
            0.0
        )

    def test_unified_candidate_object(self):

        result = generate_unified_score(
            candidate_id="UC001",
            candidate_name="Arun Kumar",
            target_role="Data Analyst",
            ats_score=85,
            screening_score=80,
            hr_interview_score=90
        )

        self.assertEqual(
            result["candidate_id"],
            "UC001"
        )

        self.assertIn(
            "hiring_fit_percentage",
            result
        )

        self.assertIn(
            "component_breakdown",
            result
        )


if __name__ == "__main__":
    unittest.main()
