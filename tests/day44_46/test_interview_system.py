import unittest

from src.interview_system.technical_engine import TechnicalInterviewEngine
from src.interview_system.hr_engine import HRInterviewEngine


class TechnicalInterviewTests(unittest.TestCase):

    def setUp(self):
        self.engine = TechnicalInterviewEngine()

    def test_experience_levels(self):
        self.assertEqual(self.engine.get_experience_level(0), "basic")
        self.assertEqual(self.engine.get_experience_level(2), "basic")
        self.assertEqual(self.engine.get_experience_level(3), "intermediate")
        self.assertEqual(self.engine.get_experience_level(4), "intermediate")
        self.assertEqual(self.engine.get_experience_level(5), "advanced")
        self.assertEqual(self.engine.get_experience_level(5.1), "advanced")

    def test_negative_experience_rejected(self):
        with self.assertRaises(ValueError):
            self.engine.get_experience_level(-1)

    def test_role_domains(self):
        self.assertIn("React", self.engine.get_skill_domains("mern"))
        self.assertIn("Spring Boot", self.engine.get_skill_domains("java"))
        self.assertIn("Docker", self.engine.get_skill_domains("devops"))

    def test_role_alias(self):
        self.assertEqual(
            self.engine.normalize_role("Java Developer"),
            "java"
        )

    def test_invalid_role(self):
        with self.assertRaises(ValueError):
            self.engine.generate_questions("unknown", 2)

    def test_question_sections(self):
        result = self.engine.get_interview_blueprint("mern", 1)

        self.assertIn("introduction", result["sections"])
        self.assertIn("experience", result["sections"])
        self.assertIn("conceptual", result["sections"])
        self.assertIn("scenario", result["sections"])

    def test_session_creation(self):
        session = self.engine.create_session("T001", "java", 3)
        self.assertEqual(session.state, "created")

    def test_valid_transition_and_previous_state(self):
        session = self.engine.create_session("T002", "mern", 1)

        result = self.engine.transition(session, "introduction")

        self.assertEqual(result["previous_state"], "created")
        self.assertEqual(result["current_state"], "introduction")

    def test_invalid_transition(self):
        session = self.engine.create_session("T003", "devops", 6)

        with self.assertRaises(ValueError):
            self.engine.transition(session, "completed")

    def test_answer_submission(self):
        session = self.engine.create_session("T004", "java", 2)
        session.state = "conceptual"

        result = self.engine.submit_answer(
            session,
            "What is Java?",
            "A programming language."
        )

        self.assertEqual(result["total_answers"], 1)

    def test_empty_answer(self):
        session = self.engine.create_session("T005", "java", 2)
        session.state = "conceptual"

        with self.assertRaises(ValueError):
            self.engine.submit_answer(session, "Question", "")


class HRInterviewTests(unittest.TestCase):

    def setUp(self):
        self.engine = HRInterviewEngine()

        self.scores = {
            "communication": 90,
            "role_understanding": 80,
            "problem_solving": 85,
            "professionalism": 95
        }

    def test_score_calculation(self):
        result = self.engine.calculate_score(self.scores)

        self.assertEqual(result["overall_score"], 87.5)

    def test_score_breakdown(self):
        result = self.engine.calculate_score(self.scores)

        self.assertIn("communication", result["breakdown"])

    def test_invalid_score(self):
        scores = dict(self.scores)
        scores["communication"] = 101

        with self.assertRaises(ValueError):
            self.engine.calculate_score(scores)

    def test_missing_category(self):
        scores = dict(self.scores)
        del scores["communication"]

        with self.assertRaises(ValueError):
            self.engine.calculate_score(scores)

    def test_recommendation_levels(self):
        self.assertEqual(
            self.engine.recommendation(90),
            "STRONGLY_RECOMMEND"
        )

        self.assertEqual(
            self.engine.recommendation(75),
            "RECOMMEND"
        )

        self.assertEqual(
            self.engine.recommendation(55),
            "HOLD"
        )

        self.assertEqual(
            self.engine.recommendation(40),
            "NOT_RECOMMENDED"
        )

    def test_candidate_evaluation(self):
        result = self.engine.evaluate_candidate(
            "HR001",
            "Candidate A",
            "Data Analyst",
            self.scores,
            "Good performance"
        )

        self.assertEqual(result["evaluation_status"], "completed")
        self.assertEqual(result["candidate_id"], "HR001")


if __name__ == "__main__":
    unittest.main()