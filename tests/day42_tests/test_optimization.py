import unittest

from src.hr_interview_optimization.engine import (
    clean_transcript,
    handle_follow_up,
    validate_score,
    calculate_refined_score,
    evaluate_decisions,
    optimize_threshold,
    benchmark_processing
)

class TestDay42(unittest.TestCase):

    def test_transcript_cleanup(self):
        result = clean_transcript("Um, I used Python, uh, for analysis.")
        self.assertEqual(result["removed_filler_count"], 2)

    def test_transcript_preserves_negation(self):
        result = clean_transcript("I do not know Java.")
        self.assertIn("not", result["cleaned_transcript"])

    def test_empty_answer(self):
        self.assertEqual(
            handle_follow_up("")["trigger"],
            "EMPTY_ANSWER"
        )

    def test_repeated_answer(self):
        result = handle_follow_up(
            "I used Python and SQL.",
            previous_answer="I used Python and SQL."
        )
        self.assertEqual(result["trigger"], "REPEATED_ANSWER")

    def test_retry_limit(self):
        result = handle_follow_up("", retry_count=2, max_retries=2)
        self.assertEqual(result["status"], "REVIEW_REQUIRED")

    def test_valid_answer(self):
        result = handle_follow_up("I built a data dashboard.")
        self.assertEqual(result["status"], "ANSWER_ACCEPTED")

    def test_invalid_score(self):
        with self.assertRaises(ValueError):
            validate_score(120)

    def test_weighted_score(self):
        result = calculate_refined_score(
            {"answer_relevance": 80, "communication": 90},
            {"answer_relevance": 40, "communication": 60}
        )
        self.assertEqual(result["final_score"], 86.0)

    def test_missing_component(self):
        result = calculate_refined_score(
            {"answer_relevance": 80, "communication": None},
            {"answer_relevance": 40, "communication": 60}
        )
        self.assertEqual(result["final_score"], 80.0)

    def test_false_positive_and_negative(self):
        cases = [
            {"candidate_id":"1","score":90,"human_decision":"PASS"},
            {"candidate_id":"2","score":40,"human_decision":"HOLD"},
            {"candidate_id":"3","score":80,"human_decision":"HOLD"},
            {"candidate_id":"4","score":60,"human_decision":"PASS"}
        ]
        result = evaluate_decisions(cases, 70)
        self.assertEqual(result["false_positive"], 1)
        self.assertEqual(result["false_negative"], 1)

    def test_threshold_optimization(self):
        cases = [
            {"candidate_id":"1","score":90,"human_decision":"PASS"},
            {"candidate_id":"2","score":40,"human_decision":"HOLD"}
        ]
        result = optimize_threshold(cases)
        self.assertIn(result["selected_threshold"], range(50, 96, 5))

    def test_processing_benchmark(self):
        result = benchmark_processing([
            {"score":80,"transcript":"I used Python."}
        ])
        self.assertEqual(result["processed_cases"], 1)

if __name__ == "__main__":
    unittest.main()
