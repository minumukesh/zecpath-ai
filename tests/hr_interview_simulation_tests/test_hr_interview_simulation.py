import json
import tempfile
import unittest

from src.hr_interview_simulation import (
    validate_score,
    calculate_weighted_score,
    classify_performance,
    evaluate_candidate,
    compare_evaluations,
    generate_recommendations,
    generate_test_report,
    save_report,
)


def sample_candidate():
    return {
        "candidate_id": "TEST-001",
        "candidate_name": "Test Candidate",
        "role": "HR Executive",
        "candidate_type": "CONFIDENT",
        "scores": {
            "answer_relevance": 90,
            "communication": 90,
            "problem_solving": 90,
            "consistency": 90,
        },
        "manual_expected_score": 90,
        "manual_expected_decision": "STRONG",
        "scenario_notes": "Test case",
    }


class TestHRInterviewSimulation(unittest.TestCase):

    def test_valid_score(self):
        self.assertEqual(validate_score(80), 80.0)

    def test_invalid_score_rejected(self):
        with self.assertRaises(ValueError):
            validate_score(110)

    def test_weighted_score(self):
        score = calculate_weighted_score({
            "answer_relevance": 100,
            "communication": 100,
            "problem_solving": 100,
            "consistency": 100,
        })
        self.assertEqual(score, 100.0)

    def test_performance_classification(self):
        self.assertEqual(classify_performance(90), "STRONG")
        self.assertEqual(classify_performance(75), "GOOD")
        self.assertEqual(classify_performance(60), "MODERATE")
        self.assertEqual(classify_performance(30), "NEEDS_REVIEW")

    def test_candidate_evaluation(self):
        result = evaluate_candidate(sample_candidate())
        self.assertEqual(result["ai_final_score"], 90.0)

    def test_invalid_candidate_type_rejected(self):
        candidate = sample_candidate()
        candidate["candidate_type"] = "UNKNOWN"

        with self.assertRaises(ValueError):
            evaluate_candidate(candidate)

    def test_matching_manual_evaluation(self):
        result = evaluate_candidate(sample_candidate())
        comparison = compare_evaluations(result)

        self.assertTrue(comparison["score_consistent"])
        self.assertTrue(comparison["decision_consistent"])

    def test_scoring_inconsistency_detected(self):
        candidate = sample_candidate()
        candidate["manual_expected_score"] = 50
        candidate["manual_expected_decision"] = "MODERATE"

        result = compare_evaluations(evaluate_candidate(candidate))

        self.assertFalse(result["score_consistent"])
        self.assertFalse(result["decision_consistent"])

    def test_all_four_candidate_types(self):
        candidates = [
            ("CONFIDENT", "STRONG"),
            ("HESITANT", "GOOD"),
            ("INEXPERIENCED", "MODERATE"),
            ("OVERQUALIFIED", "STRONG"),
        ]

        for candidate_type, _ in candidates:
            candidate = sample_candidate()
            candidate["candidate_type"] = candidate_type
            result = evaluate_candidate(candidate)
            self.assertEqual(result["candidate_type"], candidate_type)

    def test_empty_dataset_rejected(self):
        with self.assertRaises(ValueError):
            generate_test_report([])

    def test_report_metrics_created(self):
        report = generate_test_report([sample_candidate()])
        self.assertEqual(report["total_simulations"], 1)
        self.assertIn("decision_accuracy_percent", report["metrics"])

    def test_improvement_recommendations_created(self):
        report = generate_test_report([sample_candidate()])
        self.assertGreater(
            len(report["improvement_recommendations"]), 0
        )

    def test_report_files_created(self):
        report = generate_test_report([sample_candidate()])

        with tempfile.TemporaryDirectory() as directory:
            json_path, markdown_path = save_report(report, directory)

            self.assertTrue(json_path.exists())
            self.assertTrue(markdown_path.exists())

            with json_path.open("r", encoding="utf-8") as file:
                loaded = json.load(file)

            self.assertEqual(loaded["day"], 40)


if __name__ == "__main__":
    unittest.main()
