import json
import tempfile
import unittest

from src.aptitude_logic import (
    validate_weights,
    validate_score,
    map_ideal_answer_structure,
    detect_problem_solving_clarity,
    evaluate_reasoning,
    score_answer,
    evaluate_scenario,
    save_report,
)


def sample_result():
    return score_answer(
        question_id="TEST-Q1",
        question="How would you investigate an error?",
        answer="First, I would check the data and test the result.",
        question_type="reasoning",
        reference_points=["check the data", "test the result"],
        reviewer_scores={
            "reasoning": 90,
            "approach": 80,
            "problem_solving": 85,
            "clarity": 90,
        },
    )


class TestAptitudeLogic(unittest.TestCase):

    def test_weights_sum_to_one(self):
        weights = validate_weights()
        self.assertAlmostEqual(sum(weights.values()), 1.0)

    def test_custom_weights_normalized(self):
        weights = validate_weights({
            "reasoning": 2,
            "approach": 1,
            "problem_solving": 1,
            "clarity": 1,
        })
        self.assertAlmostEqual(sum(weights.values()), 1.0)

    def test_invalid_weights_rejected(self):
        with self.assertRaises(ValueError):
            validate_weights({
                "reasoning": -1,
                "approach": 1,
                "problem_solving": 1,
                "clarity": 1,
            })

    def test_score_validation(self):
        self.assertEqual(validate_score(75), 75.0)

    def test_out_of_range_score_rejected(self):
        with self.assertRaises(ValueError):
            validate_score(110)

    def test_reasoning_structure(self):
        result = map_ideal_answer_structure("reasoning")
        self.assertIn("recommended_steps", result)

    def test_situational_structure(self):
        result = map_ideal_answer_structure("situational")
        self.assertGreater(len(result["recommended_steps"]), 0)

    def test_unknown_question_type_rejected(self):
        with self.assertRaises(ValueError):
            map_ideal_answer_structure("unknown")

    def test_clarity_indicators_detected(self):
        result = detect_problem_solving_clarity(
            "First, I check the issue because the data may be incorrect."
        )
        self.assertTrue(result["has_explanation_marker"])
        self.assertTrue(result["has_step_sequence_marker"])

    def test_reference_points_scored(self):
        result = evaluate_reasoning(
            "Test question",
            "I check the source data and compare the results.",
            ["source data", "compare"],
        )
        self.assertEqual(result["score"], 100.0)

    def test_score_breakdown_is_explainable(self):
        result = sample_result()
        self.assertIn("reasoning", result["component_breakdown"])
        self.assertIn(
            "weighted_contribution",
            result["component_breakdown"]["reasoning"],
        )

    def test_final_score_range(self):
        result = sample_result()
        self.assertGreaterEqual(result["final_aptitude_score"], 0)
        self.assertLessEqual(result["final_aptitude_score"], 100)

    def test_empty_answer_rejected(self):
        with self.assertRaises(ValueError):
            score_answer(
                "TEST-Q2",
                "Explain your solution.",
                "",
            )

    def test_situational_evaluation(self):
        result = evaluate_scenario(
            "TEST-S1",
            "A teammate disagrees with your solution.",
            "I would listen and compare both options.",
        )
        self.assertEqual(
            result["evaluation_type"],
            "SITUATIONAL_JUDGMENT",
        )

    def test_report_files_created(self):
        result = sample_result()

        with tempfile.TemporaryDirectory() as directory:
            json_path, markdown_path = save_report(
                [result],
                directory,
            )

            self.assertTrue(json_path.exists())
            self.assertTrue(markdown_path.exists())

            with json_path.open("r", encoding="utf-8") as file:
                report = json.load(file)

            self.assertEqual(report["total_evaluations"], 1)


if __name__ == "__main__":
    unittest.main()
