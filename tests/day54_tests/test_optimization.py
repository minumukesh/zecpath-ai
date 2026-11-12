import unittest

from src.day54_optimization.engine import OptimizationEngine


class Day54OptimizationTests(unittest.TestCase):

    def setUp(self):
        self.engine = OptimizationEngine()

    def test_confusion_matrix(self):
        records = [
            {"score": 0.9, "actual_positive": True},
            {"score": 0.8, "actual_positive": False},
            {"score": 0.2, "actual_positive": False},
            {"score": 0.1, "actual_positive": True},
        ]

        result = self.engine.evaluate_predictions(records, 0.5)

        self.assertEqual(result["true_positives"], 1)
        self.assertEqual(result["false_positives"], 1)
        self.assertEqual(result["true_negatives"], 1)
        self.assertEqual(result["false_negatives"], 1)

    def test_empty_threshold_dataset(self):
        with self.assertRaises(ValueError):
            self.engine.optimize_threshold([])

    def test_threshold_optimization(self):
        records = [
            {"score": 0.9, "actual_positive": True},
            {"score": 0.8, "actual_positive": True},
            {"score": 0.2, "actual_positive": False},
            {"score": 0.1, "actual_positive": False},
        ]

        result = self.engine.optimize_threshold(records)

        self.assertIn("optimized", result)
        self.assertIn("baseline", result)

    def test_text_normalization(self):
        result = self.engine.normalize_text("  YES!!!  ")

        self.assertEqual(result, "yes")

    def test_accept_intent(self):
        result = self.engine.detect_intent("Yes, please continue")

        self.assertEqual(result["intent"], "accept")

    def test_reject_intent(self):
        result = self.engine.detect_intent("No, stop")

        self.assertEqual(result["intent"], "reject")

    def test_clarification_intent(self):
        result = self.engine.detect_intent("Please explain this")

        self.assertEqual(result["intent"], "clarification")

    def test_question_intent(self):
        result = self.engine.detect_intent("What is this?")

        self.assertEqual(result["intent"], "question")

    def test_unknown_intent(self):
        result = self.engine.detect_intent("Good morning")

        self.assertEqual(result["intent"], "unknown")

    def test_empty_intent(self):
        result = self.engine.detect_intent("")

        self.assertEqual(result["intent"], "unknown")

    def test_non_string_intent_rejected(self):
        with self.assertRaises(ValueError):
            self.engine.detect_intent(None)

    def test_round_aggregation(self):
        result = self.engine.aggregate_rounds([80, 85, 82])

        self.assertEqual(result["average_score"], 82.33)
        self.assertEqual(result["consistency_status"], "CONSISTENT")

    def test_inconsistent_rounds(self):
        result = self.engine.aggregate_rounds([30, 80, 95])

        self.assertEqual(result["consistency_status"], "REVIEW_REQUIRED")

    def test_empty_rounds_rejected(self):
        with self.assertRaises(ValueError):
            self.engine.aggregate_rounds([])

    def test_invalid_round_score_rejected(self):
        with self.assertRaises(ValueError):
            self.engine.aggregate_rounds([80, 120])

    def test_benchmark(self):
        records = [
            {"score": 0.9, "actual_positive": True, "text": "yes"}
        ]

        result = self.engine.benchmark_processing(records, 5)

        self.assertEqual(result["total_operations"], 5)
        self.assertGreaterEqual(result["elapsed_seconds"], 0)

    def test_invalid_benchmark_iterations(self):
        with self.assertRaises(ValueError):
            self.engine.benchmark_processing(
                [{"score": 0.9, "actual_positive": True, "text": "yes"}],
                0
            )


if __name__ == "__main__":
    unittest.main()
