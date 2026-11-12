import json
import tempfile
import unittest

from pathlib import Path

from src.communication_evaluation import (
    SCORING_WEIGHTS,
    normalize_text,
    detect_filler_words,
    evaluate_fluency,
    evaluate_grammar,
    evaluate_vocabulary,
    evaluate_clarity,
    evaluate_answer_structure,
    evaluate_communication,
    save_evaluation_report,
)


class TestCommunicationEvaluation(unittest.TestCase):

    def test_scoring_weights_total_one(self):
        self.assertAlmostEqual(sum(SCORING_WEIGHTS.values()), 1.0)

    def test_text_normalization(self):
        self.assertEqual(normalize_text("  Hello   world "), "Hello world")

    def test_empty_text_normalizes_to_empty(self):
        self.assertEqual(normalize_text(""), "")

    def test_filler_word_detection(self):
        result = detect_filler_words(
            "Um, I basically worked on the project, you know."
        )
        self.assertGreaterEqual(result["count"], 2)

    def test_fluency_score_is_in_range(self):
        result = evaluate_fluency(
            "I analyzed the data. Then I created a report."
        )
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)

    def test_grammar_warning_detection(self):
        result = evaluate_grammar("I is ready.")
        self.assertGreater(result["warning_count"], 0)

    def test_vocabulary_score_is_in_range(self):
        result = evaluate_vocabulary(
            "I analyzed data and created a useful report."
        )
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)

    def test_clarity_score_is_in_range(self):
        result = evaluate_clarity(
            "I analyzed the data and explained the results clearly."
        )
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)

    def test_structure_indicators_detected(self):
        result = evaluate_answer_structure(
            "First, I analyzed the data. For example, I used Python. "
            "Overall, the project was successful."
        )
        self.assertTrue(result["introduction_indicator"])
        self.assertTrue(result["detail_indicator"])
        self.assertTrue(result["conclusion_indicator"])

    def test_final_score_is_in_range(self):
        result = evaluate_communication(
            "First, I analyzed the data. For example, I used Python. "
            "Overall, the project improved my skills."
        )
        self.assertGreaterEqual(result["communication_score"], 0)
        self.assertLessEqual(result["communication_score"], 100)

    def test_empty_response_returns_zero(self):
        result = evaluate_communication("")
        self.assertEqual(result["communication_score"], 0.0)

    def test_component_scores_are_present(self):
        result = evaluate_communication("I worked on a project.")
        expected = {
            "fluency",
            "grammar_quality",
            "vocabulary_range",
            "clarity",
            "answer_structure",
        }
        self.assertEqual(set(result["component_scores"]), expected)

    def test_report_files_are_created(self):
        result = evaluate_communication("I completed a data project.")

        with tempfile.TemporaryDirectory() as directory:
            json_path, markdown_path = save_evaluation_report(
                result, directory, "TEST-001"
            )

            self.assertTrue(json_path.exists())
            self.assertTrue(markdown_path.exists())

            with json_path.open("r", encoding="utf-8") as file:
                saved_result = json.load(file)

            self.assertEqual(
                saved_result["evaluation_id"],
                "TEST-001",
            )

    def test_filler_positions_are_reported(self):
        result = detect_filler_words("Um, I worked on it.")
        self.assertGreaterEqual(result["count"], 1)
        self.assertIn("position", result["items"][0])


if __name__ == "__main__":
    unittest.main()
