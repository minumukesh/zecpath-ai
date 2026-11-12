import unittest

from src.conversation_flow import (
    ConversationEngine,
    ConversationConfig,
    ConversationState,
)


class TestConversationFlow(unittest.TestCase):

    def setUp(self):
        self.engine = ConversationEngine()

    def test_conversation_starts_with_first_question(self):
        result = self.engine.start()

        self.assertEqual(result.action, "ASK_QUESTION")
        self.assertEqual(result.question_id, "Q1")
        self.assertEqual(
            self.engine.state,
            ConversationState.WAITING_FOR_ANSWER,
        )

    def test_valid_answer_advances_conversation(self):
        self.engine.start()

        result = self.engine.handle_answer(
            "I have used Python and SQL in my projects."
        )

        self.assertEqual(result.action, "ASK_QUESTION")
        self.assertEqual(result.question_id, "Q2")
        self.assertEqual(len(self.engine.answers), 1)

    def test_silence_triggers_polite_retry(self):
        self.engine.start()
        result = self.engine.handle_silence()

        self.assertEqual(result.action, "PROMPT_AFTER_SILENCE")
        self.assertTrue(result.should_retry)

    def test_silence_limit_uses_fallback(self):
        engine = ConversationEngine(
            config=ConversationConfig(max_silence_retries=1)
        )

        engine.start()
        engine.handle_silence()
        result = engine.handle_silence()

        self.assertEqual(result.action, "USE_FALLBACK")
        self.assertTrue(result.follow_up_triggered)

    def test_confusion_triggers_clarification(self):
        self.engine.start()

        result = self.engine.handle_answer(
            "I don't understand the question."
        )

        self.assertEqual(result.action, "CLARIFY_QUESTION")
        self.assertTrue(result.should_retry)

    def test_repeated_answer_is_detected(self):
        self.engine.start()

        answer = "I have used Python and SQL in my projects."

        # First answer is accepted and the engine advances to Q2.
        self.engine.handle_answer(answer)

        # Same answer on Q2 is detected as a duplicate.
        result = self.engine.handle_answer(answer)

        self.assertEqual(
            result.action,
            "HANDLE_REPEATED_ANSWER",
        )

        # Repeating again reaches the configured retry limit.
        result = self.engine.handle_answer(answer)

        self.assertEqual(
            result.action,
            "ASK_QUESTION",
        )
        self.assertEqual(result.question_id, "Q3")

    def test_uncertain_answer_triggers_follow_up(self):
        self.engine.start()

        result = self.engine.handle_answer(
            "I am not sure about my main skills."
        )

        self.assertEqual(
            result.action,
            "FOLLOW_UP_UNCERTAIN_ANSWER",
        )

    def test_system_failure_retries_politely(self):
        self.engine.start()

        result = self.engine.handle_system_failure(
            "temporary failure"
        )

        self.assertEqual(result.action, "RETRY_SYSTEM")
        self.assertTrue(result.should_retry)

    def test_system_retry_limit_ends_safely(self):
        engine = ConversationEngine(
            config=ConversationConfig(max_system_retries=1)
        )

        engine.start()
        engine.handle_system_failure("temporary failure")
        result = engine.handle_system_failure("second failure")

        self.assertEqual(result.action, "END_WITH_ERROR")
        self.assertEqual(engine.state, ConversationState.FAILED)

    def test_conversation_completes_after_all_answers(self):
        self.engine.start()

        answers = [
            "I have used Python and SQL in my projects.",
            "I completed a data analytics project during my studies.",
            "I can join within thirty days after receiving the offer.",
        ]

        for answer in answers:
            result = self.engine.handle_answer(answer)

            if result.completed:
                break

        self.assertEqual(
            self.engine.state,
            ConversationState.COMPLETED,
        )

    def test_report_contains_conversation_history(self):
        self.engine.start()
        self.engine.handle_answer(
            "I have used Python and SQL in my projects."
        )

        report = self.engine.get_report()

        self.assertIn("answers", report)
        self.assertIn("conversation_history", report)
        self.assertGreater(len(report["conversation_history"]), 0)

    def test_empty_question_configuration_is_rejected(self):
        with self.assertRaises(ValueError):
            ConversationEngine(questions=[])

    def test_invalid_retry_limit_is_rejected(self):
        with self.assertRaises(ValueError):
            ConversationConfig(max_silence_retries=-1)


if __name__ == "__main__":
    unittest.main()
