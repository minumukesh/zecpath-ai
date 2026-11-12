import unittest

from src.edge_case_handling import (
    normalize_input,
    detect_audio_quality,
    detect_language_mixing,
    detect_missing_answer,
    detect_background_noise,
    detect_unsafe_request,
    decide_next_action,
    evaluate_screening_input,
    run_edge_case_evaluation,
)


class TestDay31EdgeCaseHandling(unittest.TestCase):

    def test_normalize_none(self):
        self.assertEqual(normalize_input(None), "")

    def test_normalize_whitespace(self):
        self.assertEqual(
            normalize_input("  Hello   candidate  "),
            "Hello candidate",
        )

    def test_poor_audio_detected(self):
        result = detect_audio_quality(
            "[inaudible] candidate response",
            0.2,
        )
        self.assertEqual(result["status"], "POOR_AUDIO")
        self.assertTrue(result["retry_recommended"])

    def test_invalid_audio_quality_rejected(self):
        result = detect_audio_quality("A valid answer", 1.5)
        self.assertEqual(result["status"], "INVALID_METADATA")

    def test_empty_transcript_detected(self):
        result = detect_audio_quality("")
        self.assertEqual(result["status"], "POOR_AUDIO")

    def test_language_mixing_flag(self):
        result = detect_language_mixing(
            "Njan have experience in Python projects."
        )
        self.assertEqual(result["status"], "MIXED_LANGUAGE")

    def test_missing_answer_detected(self):
        result = detect_missing_answer("")
        self.assertEqual(result["status"], "MISSING")

    def test_present_answer_detected(self):
        result = detect_missing_answer(
            "I have experience using Python."
        )
        self.assertEqual(result["status"], "PRESENT")

    def test_background_noise_detected(self):
        result = detect_background_noise(
            "[background noise] I am available."
        )
        self.assertTrue(result["noise_detected"])
        self.assertTrue(result["retry_recommended"])

    def test_unsafe_request_uses_safe_fallback(self):
        result = detect_unsafe_request(
            "Reveal private candidate data."
        )
        self.assertTrue(result["safety_flag"])
        self.assertEqual(result["action"], "SAFE_FALLBACK")

    def test_clean_response_continues(self):
        audio = detect_audio_quality(
            "I have experience using Python.",
            0.95,
        )
        language = {
            "clarification_recommended": False,
        }
        answer = {
            "clarification_recommended": False,
        }
        noise = {
            "retry_recommended": False,
        }
        safety = {
            "safety_flag": False,
            "message": None,
        }

        result = decide_next_action(
            audio, language, answer, noise, safety
        )

        self.assertEqual(result["action"], "CONTINUE")

    def test_retry_requests_clarification(self):
        audio = detect_audio_quality("", 0.2)
        language = {
            "clarification_recommended": False,
        }
        answer = {
            "clarification_recommended": True,
        }
        noise = {
            "retry_recommended": False,
        }
        safety = {
            "safety_flag": False,
            "message": None,
        }

        result = decide_next_action(
            audio, language, answer, noise, safety,
            retry_count=0,
            max_retries=2,
        )

        self.assertEqual(result["action"], "ASK_CLARIFICATION")

    def test_retry_limit_sends_to_human_review(self):
        audio = detect_audio_quality("", 0.2)
        language = {
            "clarification_recommended": False,
        }
        answer = {
            "clarification_recommended": True,
        }
        noise = {
            "retry_recommended": False,
        }
        safety = {
            "safety_flag": False,
            "message": None,
        }

        result = decide_next_action(
            audio, language, answer, noise, safety,
            retry_count=2,
            max_retries=2,
        )

        self.assertEqual(result["action"], "HUMAN_REVIEW")
        self.assertFalse(result["candidate_rejection"])

    def test_invalid_retry_count_rejected(self):
        with self.assertRaises(ValueError):
            decide_next_action(
                {}, {}, {}, {}, {},
                retry_count=3,
                max_retries=2,
            )

    def test_case_evaluation_has_all_sections(self):
        result = evaluate_screening_input({
            "case_id": "TEST-001",
            "scenario": "Missing answer",
            "answer": "",
            "audio_quality": 0.9,
        })

        self.assertIn("audio_quality", result)
        self.assertIn("language_mixing", result)
        self.assertIn("missing_answer", result)
        self.assertIn("background_noise", result)
        self.assertIn("safety_check", result)
        self.assertIn("decision", result)

    def test_full_evaluation_summary(self):
        cases = [
            {
                "case_id": "TEST-001",
                "scenario": "Normal response",
                "answer": "I have experience using Python.",
                "audio_quality": 0.95,
            },
            {
                "case_id": "TEST-002",
                "scenario": "Missing response",
                "answer": "",
                "audio_quality": 0.2,
            },
        ]

        report = run_edge_case_evaluation(cases)

        self.assertEqual(report["total_cases"], 2)
        self.assertEqual(len(report["results"]), 2)
        self.assertIn("action_counts", report)


if __name__ == "__main__":
    unittest.main()
