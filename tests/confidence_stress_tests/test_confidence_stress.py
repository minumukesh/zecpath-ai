import json
import tempfile
import unittest

from src.confidence_stress import (
    normalize_text,
    detect_long_pauses,
    detect_repeated_words,
    detect_hesitation,
    analyze_sentiment,
    detect_contradictions,
    analyze_stress_indicators,
    calculate_behavioral_confidence_score,
    analyze_response,
    save_report,
)


class TestConfidenceStress(unittest.TestCase):

    def test_text_normalization(self):
        self.assertEqual(normalize_text("  hello   world "), "hello world")

    def test_long_pause_marker_detected(self):
        result = detect_long_pauses("I [pause: 3.5s] answered.")
        self.assertEqual(result["long_pause_count"], 1)

    def test_short_pause_not_counted_as_long(self):
        result = detect_long_pauses("I [pause: 1.0s] answered.")
        self.assertEqual(result["long_pause_count"], 0)

    def test_repeated_words_detected(self):
        result = detect_repeated_words("I used the the tool.")
        self.assertEqual(result["repeated_word_count"], 1)

    def test_uncertainty_phrase_detected(self):
        result = detect_hesitation("I think maybe this could work.")
        self.assertGreaterEqual(len(result["uncertainty_phrases"]), 1)

    def test_positive_language_detected(self):
        result = analyze_sentiment(
            "I successfully completed and improved the project."
        )
        self.assertEqual(result["label"], "POSITIVE_LANGUAGE")

    def test_negative_language_detected(self):
        result = analyze_sentiment(
            "I felt worried and overwhelmed by the problem."
        )
        self.assertEqual(result["label"], "NEGATIVE_LANGUAGE")

    def test_potential_contradiction_flagged(self):
        result = detect_contradictions(
            "I always agree, but I never agree."
        )
        self.assertGreater(
            result["potential_contradiction_count"], 0
        )

    def test_stress_phrase_detected(self):
        result = analyze_stress_indicators(
            "I felt overwhelmed by the deadline."
        )
        self.assertGreater(
            len(result["stress_related_phrases"]), 0
        )

    def test_confidence_score_is_in_range(self):
        result = calculate_behavioral_confidence_score(
            "I successfully completed my project."
        )
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)

    def test_empty_answer_has_zero_score(self):
        result = calculate_behavioral_confidence_score("")
        self.assertEqual(result["score"], 0.0)

    def test_complete_analysis_structure(self):
        result = analyze_response(
            "TEST-001",
            "I successfully completed my project.",
        )
        self.assertIn("hesitation_analysis", result)
        self.assertIn("sentiment_analysis", result)
        self.assertIn("contradiction_analysis", result)
        self.assertIn("stress_analysis", result)
        self.assertIn("behavioral_confidence", result)

    def test_report_files_created(self):
        results = [
            analyze_response("TEST-002", "I completed the project.")
        ]

        with tempfile.TemporaryDirectory() as directory:
            json_path, markdown_path = save_report(results, directory)

            self.assertTrue(json_path.exists())
            self.assertTrue(markdown_path.exists())

            with json_path.open("r", encoding="utf-8") as file:
                report = json.load(file)

            self.assertEqual(report["total_responses"], 1)


if __name__ == "__main__":
    unittest.main()
