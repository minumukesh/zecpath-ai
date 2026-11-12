import json
import unittest
from pathlib import Path

from src.screening_optimization import (
    normalize_text,
    detect_intent,
    score_response,
    classify_screening_score,
    evaluate_case,
    calculate_metrics,
    optimize_thresholds,
    run_evaluation,
)


ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data" / "day30" / "screening_test_cases.json"


class TestDay30ScreeningOptimization(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with DATA_FILE.open("r", encoding="utf-8-sig") as file:
            cls.cases = json.load(file)

    def test_text_normalization(self):
        self.assertEqual(
            normalize_text("  Python   SQL  "),
            "python sql",
        )

    def test_skills_intent_detection(self):
        result = detect_intent(
            "I have used Python, SQL and Excel in my projects."
        )
        self.assertEqual(result["intent"], "skills")

    def test_experience_intent_detection(self):
        result = detect_intent(
            "I completed an internship and worked on projects."
        )
        self.assertEqual(result["intent"], "experience")

    def test_unclear_answer_detection(self):
        result = detect_intent("I do not understand the question.")
        self.assertEqual(result["intent"], "unclear")

    def test_off_topic_detection(self):
        result = detect_intent(
            "I enjoy watching movies during the weekend."
        )
        self.assertEqual(result["intent"], "off_topic")

    def test_score_contains_all_parameters(self):
        result = score_response(
            "I have used Python and SQL in my projects.",
            "skills",
        )

        self.assertIn("clarity", result)
        self.assertIn("relevance", result)
        self.assertIn("completeness", result)
        self.assertIn("consistency", result)
        self.assertIn("total_score", result)
        self.assertGreaterEqual(result["total_score"], 0)
        self.assertLessEqual(result["total_score"], 100)

    def test_score_threshold_classification(self):
        self.assertEqual(
            classify_screening_score(80, 60, 35),
            "ACCEPT",
        )
        self.assertEqual(
            classify_screening_score(45, 60, 35),
            "REVIEW",
        )
        self.assertEqual(
            classify_screening_score(20, 60, 35),
            "REJECT",
        )

    def test_invalid_thresholds_are_rejected(self):
        with self.assertRaises(ValueError):
            classify_screening_score(50, 30, 60)

    def test_evaluation_compares_ai_and_human_labels(self):
        result = evaluate_case(
            self.cases[0],
            accept_threshold=60,
            review_threshold=35,
        )

        self.assertIn("ai_decision", result)
        self.assertIn("human_decision", result)
        self.assertIn("decision_match", result)
        self.assertIn("false_rejection", result)

    def test_metrics_are_generated(self):
        results = [
            evaluate_case(case, 60, 35)
            for case in self.cases
        ]

        metrics = calculate_metrics(results)

        self.assertEqual(metrics["total_cases"], len(self.cases))
        self.assertIn("false_rejections", metrics)
        self.assertIn("false_acceptances", metrics)
        self.assertIn("decision_accuracy", metrics)
        self.assertIn("intent_accuracy", metrics)

    def test_threshold_optimization_returns_valid_threshold(self):
        result = optimize_thresholds(self.cases)

        self.assertIn("selected_accept_threshold", result)
        self.assertIn("selected_review_threshold", result)
        self.assertGreaterEqual(
            result["selected_accept_threshold"],
            result["selected_review_threshold"],
        )

    def test_full_evaluation_contains_baseline_and_optimized_results(self):
        result = run_evaluation(self.cases)

        self.assertIn("baseline_metrics", result)
        self.assertIn("optimized_metrics", result)
        self.assertEqual(len(result["results"]), len(self.cases))

    def test_empty_answer_is_not_accepted_as_clear_intent(self):
        result = detect_intent("")
        self.assertEqual(result["intent"], "unclear")


if __name__ == "__main__":
    unittest.main()
