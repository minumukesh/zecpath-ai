import unittest

from src.interview_system.cross_round_aggregation_engine import (
    CrossRoundAggregationEngine,
    CandidateStageScores,
    DEFAULT_ROLE_WEIGHTS
)


class TestCrossRoundAggregationEngine(unittest.TestCase):

    def setUp(self):

        self.engine = CrossRoundAggregationEngine()

    def make_candidate(self, **changes):

        values = {

            "candidate_id": "TEST-051",

            "candidate_name": "Test Candidate",

            "target_role": "data_analyst",

            "ats": 80,

            "screening": 80,

            "hr_interview": 80,

            "technical_interview": 80,

            "machine_test": 80,

            "profile_group": "standard"
        }

        values.update(changes)

        return CandidateStageScores(**values)

    def test_aggregation_completes(self):

        result = self.engine.aggregate(self.make_candidate())

        self.assertIn("aggregation", result)

    def test_equal_scores_produce_equal_fit_score(self):

        result = self.engine.aggregate(
            self.make_candidate()
        )

        self.assertEqual(
            result["aggregation"]["hiring_fit_score"],
            80.0
        )

    def test_data_analyst_weighting(self):

        result = self.engine.aggregate(
            self.make_candidate(
                ats=100,
                screening=100,
                hr_interview=100,
                technical_interview=0,
                machine_test=0
            )
        )

        self.assertEqual(
            result["aggregation"]["hiring_fit_score"],
            40.0
        )

    def test_software_developer_weighting(self):

        candidate = self.make_candidate(
            target_role="software_developer",
            ats=100,
            screening=100,
            hr_interview=100,
            technical_interview=0,
            machine_test=0
        )

        result = self.engine.aggregate(candidate)

        self.assertEqual(
            result["aggregation"]["hiring_fit_score"],
            30.0
        )

    def test_missing_stage_is_not_zero(self):

        result = self.engine.aggregate(
            self.make_candidate(machine_test=None)
        )

        self.assertNotIn(
            "machine_test",
            result["aggregation"]["available_stages"]
        )

        self.assertIn(
            "machine_test",
            result["aggregation"]["missing_stages"]
        )

        self.assertEqual(
            result["aggregation"]["hiring_fit_score"],
            80.0
        )

    def test_available_weights_are_normalized(self):

        result = self.engine.aggregate(
            self.make_candidate(machine_test=None)
        )

        total = sum(
            result["role_weighting"]["normalized_weights"].values()
        )

        self.assertAlmostEqual(total, 1.0, places=4)

    def test_score_is_between_zero_and_hundred(self):

        result = self.engine.aggregate(
            self.make_candidate(
                ats=100,
                screening=100,
                hr_interview=100,
                technical_interview=100,
                machine_test=100
            )
        )

        score = result["aggregation"]["hiring_fit_score"]

        self.assertGreaterEqual(score, 0)

        self.assertLessEqual(score, 100)

    def test_invalid_stage_score(self):

        with self.assertRaises(ValueError):

            self.engine.aggregate(
                self.make_candidate(ats=150)
            )

    def test_invalid_profile_group(self):

        with self.assertRaises(ValueError):

            self.engine.aggregate(
                self.make_candidate(profile_group="unknown")
            )

    def test_empty_candidate_id(self):

        with self.assertRaises(ValueError):

            self.engine.aggregate(
                self.make_candidate(candidate_id="")
            )

    def test_no_available_scores(self):

        with self.assertRaises(ValueError):

            self.engine.aggregate(
                self.make_candidate(
                    ats=None,
                    screening=None,
                    hr_interview=None,
                    technical_interview=None,
                    machine_test=None
                )
            )

    def test_all_role_weights_sum_to_one(self):

        for role, weights in DEFAULT_ROLE_WEIGHTS.items():

            self.assertAlmostEqual(
                sum(weights.values()),
                1.0,
                places=4
            )

    def test_human_review_required(self):

        result = self.engine.aggregate(
            self.make_candidate()
        )

        self.assertTrue(
            result["decision_policy"]["human_review_required"]
        )

    def test_profile_normalization_is_neutral(self):

        result = self.engine.aggregate(
            self.make_candidate(profile_group="entry_level")
        )

        self.assertEqual(
            result["profile_normalization"]["adjustment"],
            0.0
        )

    def test_custom_weights(self):

        custom = {

            "custom_role": {

                "ats": 0.10,

                "screening": 0.10,

                "hr_interview": 0.10,

                "technical_interview": 0.30,

                "machine_test": 0.40
            }
        }

        engine = CrossRoundAggregationEngine(custom_weights=custom)

        candidate = self.make_candidate(
            target_role="custom_role"
        )

        result = engine.aggregate(candidate)

        self.assertEqual(
            result["role_weighting"]["selected_role"],
            "custom_role"
        )

    def test_invalid_custom_weights(self):

        custom = {

            "invalid_role": {

                "ats": 0.50,

                "screening": 0.50,

                "hr_interview": 0.50,

                "technical_interview": 0.50,

                "machine_test": 0.50
            }
        }

        with self.assertRaises(ValueError):

            CrossRoundAggregationEngine(custom_weights=custom)


if __name__ == "__main__":
    unittest.main()
