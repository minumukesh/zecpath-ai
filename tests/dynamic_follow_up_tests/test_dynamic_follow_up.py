import unittest

from src.dynamic_follow_up import (
    normalize_answer,
    detect_answer_quality,
    detect_confident_signal,
    choose_follow_up,
    FollowUpEngine,
)


class TestDynamicFollowUp(unittest.TestCase):

    def test_normalize_answer(self):
        self.assertEqual(
            normalize_answer("  Hello    there "),
            "Hello there",
        )

    def test_missing_answer(self):
        result = detect_answer_quality("")
        self.assertEqual(result["status"], "INCOMPLETE")

    def test_vague_answer(self):
        result = detect_answer_quality("It was good.")
        self.assertEqual(result["status"], "VAGUE")

    def test_brief_answer(self):
        result = detect_answer_quality("I built a web application.")
        self.assertEqual(result["status"], "BRIEF")

    def test_detailed_answer(self):
        result = detect_answer_quality(
            "I worked on a project and learned several useful skills "
            "while solving the problem with my team."
        )
        self.assertEqual(result["status"], "DETAILED")

    def test_example_signal_detected(self):
        result = detect_confident_signal(
            "In my previous role, I fixed the issue because the "
            "configuration was wrong and the team restored the service."
        )
        self.assertTrue(result["example_signal"])

    def test_missing_answer_triggers_clarification(self):
        result = choose_follow_up("")
        self.assertTrue(result["requires_follow_up"])
        self.assertEqual(result["trigger"], "CLARIFICATION")

    def test_brief_answer_triggers_follow_up(self):
        result = choose_follow_up("I built a web application.")
        self.assertTrue(result["requires_follow_up"])
        self.assertIsNotNone(result["follow_up_question"])

    def test_repeated_follow_up_is_avoided(self):
        first = choose_follow_up("")
        previous = [first["follow_up_question"]]
        second = choose_follow_up("", previous)

        self.assertNotEqual(
            first["follow_up_question"],
            second["follow_up_question"],
        )

    def test_engine_tracks_conversation_state(self):
        engine = FollowUpEngine(
            "INT-001",
            "CAND-001",
            "Data Analyst",
        )

        result = engine.process_answer(
            "Q001",
            "Tell me about yourself.",
            "",
        )

        state = engine.get_state()

        self.assertEqual(result["trigger"], "CLARIFICATION")
        self.assertEqual(state["turn_count"], 1)
        self.assertEqual(len(state["history"]), 1)

    def test_empty_interview_id_rejected(self):
        with self.assertRaises(ValueError):
            FollowUpEngine("", "CAND-001", "Data Analyst")

    def test_empty_question_id_rejected(self):
        engine = FollowUpEngine(
            "INT-002",
            "CAND-002",
            "Data Analyst",
        )

        with self.assertRaises(ValueError):
            engine.process_answer("", "Question", "Answer")

    def test_completed_engine_rejects_new_answer(self):
        engine = FollowUpEngine(
            "INT-003",
            "CAND-003",
            "Data Analyst",
        )
        engine.close()

        with self.assertRaises(ValueError):
            engine.process_answer("Q001", "Question", "Answer")


if __name__ == "__main__":
    unittest.main()
