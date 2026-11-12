import json
import tempfile
import unittest
from pathlib import Path

from src.hr_interview import (
    INTERVIEW_CATEGORIES,
    CONVERSATION_PHASES,
    generate_question_bank,
    create_interview_state,
    get_current_question,
    capture_response,
    build_interview_summary,
    save_interview_report,
)


class TestHRInterviewEngine(unittest.TestCase):

    def test_all_six_categories_exist(self):
        self.assertEqual(len(INTERVIEW_CATEGORIES), 6)

    def test_four_conversation_phases_exist(self):
        self.assertEqual(len(CONVERSATION_PHASES), 4)

    def test_fresher_technical_questions_generated(self):
        questions = generate_question_bank("fresher", "technical")
        self.assertGreater(len(questions), 0)
        self.assertTrue(
            all(q["experience_level"] == "fresher" for q in questions)
        )

    def test_experienced_nontechnical_questions_generated(self):
        questions = generate_question_bank("experienced", "non_technical")
        self.assertGreater(len(questions), 0)
        self.assertTrue(
            all(q["role_type"] == "non_technical" for q in questions)
        )

    def test_invalid_experience_level_rejected(self):
        with self.assertRaises(ValueError):
            generate_question_bank("intern", "technical")

    def test_invalid_role_type_rejected(self):
        with self.assertRaises(ValueError):
            generate_question_bank("fresher", "engineering")

    def test_interview_state_created(self):
        state = create_interview_state(
            "TEST-001", "Data Analyst", "fresher", "technical"
        )
        self.assertEqual(state["candidate_id"], "TEST-001")
        self.assertEqual(state["status"], "READY")
        self.assertGreater(len(state["questions"]), 0)

    def test_empty_candidate_id_rejected(self):
        with self.assertRaises(ValueError):
            create_interview_state(
                "", "Data Analyst", "fresher", "technical"
            )

    def test_current_question_returned(self):
        state = create_interview_state(
            "TEST-002", "Data Analyst", "fresher", "technical"
        )
        question = get_current_question(state)
        self.assertIsNotNone(question)
        self.assertIn("question_id", question)

    def test_response_is_captured(self):
        state = create_interview_state(
            "TEST-003", "Data Analyst", "fresher", "technical"
        )
        result = capture_response(state, "I have worked on a project.")
        self.assertEqual(result["response_status"], "ANSWERED")
        self.assertEqual(len(state["responses"]), 1)

    def test_missing_response_enables_followup(self):
        state = create_interview_state(
            "TEST-004", "Data Analyst", "fresher", "technical"
        )
        result = capture_response(state, "")
        self.assertEqual(result["response_status"], "MISSING")
        self.assertTrue(result["follow_up_eligible"])

    def test_summary_contains_progress(self):
        state = create_interview_state(
            "TEST-005", "Data Analyst", "fresher", "technical"
        )
        capture_response(state, "My name is Arun.")
        summary = build_interview_summary(state)
        self.assertEqual(summary["responses_captured"], 1)
        self.assertGreater(summary["completion_percentage"], 0)

    def test_report_file_is_created(self):
        state = create_interview_state(
            "TEST-006", "Data Analyst", "fresher", "technical"
        )

        with tempfile.TemporaryDirectory() as directory:
            report_path = save_interview_report(state, directory)
            self.assertTrue(report_path.exists())

            with report_path.open("r", encoding="utf-8") as file:
                report = json.load(file)

            self.assertEqual(report["candidate_id"], "TEST-006")

    def test_completed_interview_rejects_new_response(self):
        state = create_interview_state(
            "TEST-007", "Data Analyst", "fresher", "technical"
        )

        for _ in range(len(state["questions"])):
            capture_response(state, "Sample response")

        self.assertEqual(state["status"], "COMPLETED")

        with self.assertRaises(ValueError):
            capture_response(state, "An extra response")

    def test_question_ids_are_unique(self):
        questions = generate_question_bank("fresher", "technical")
        ids = [question["question_id"] for question in questions]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
