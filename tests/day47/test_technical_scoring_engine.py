import tempfile
import unittest
from pathlib import Path

from src.interview_system.technical_scoring_engine import TechnicalSkillScoringEngine


class TechnicalSkillScoringTests(unittest.TestCase):
    def setUp(self):
        self.engine = TechnicalSkillScoringEngine()
        self.base = {
            "candidate_id": "T047",
            "skill": "Python",
            "question": "Explain exception handling.",
            "answer": (
                "First, use try and except to handle errors. For example, "
                "log the exception and test edge cases in a production API."
            ),
            "expected_concepts": ["try", "except", "log", "test"],
            "question_type": "scenario",
            "difficulty": "intermediate",
        }

    def test_scores_all_four_components(self):
        result = self.engine.score_answer(**self.base)
        self.assertEqual(
            set(result["component_scores"]),
            {"accuracy", "depth", "reasoning", "applicability"},
        )

    def test_score_is_normalized(self):
        result = self.engine.score_answer(**self.base)
        self.assertGreaterEqual(result["normalized_score"], 0)
        self.assertLessEqual(result["normalized_score"], 100)

    def test_question_type_rubric_exists(self):
        for question_type in ("conceptual", "scenario", "coding", "system_design", "behavioral_technical"):
            self.assertAlmostEqual(sum(self.engine.weights[question_type].values()), 1.0)

    def test_shallow_answer_detection(self):
        data = dict(self.base, answer="Python is useful.", expected_concepts=["try", "except", "logging"])
        result = self.engine.score_answer(**data)
        self.assertTrue(result["is_shallow"])

    def test_nonempty_answer_required(self):
        with self.assertRaises(ValueError):
            self.engine.score_answer(**dict(self.base, answer=" "))

    def test_expected_concepts_required(self):
        with self.assertRaises(ValueError):
            self.engine.score_answer(**dict(self.base, expected_concepts=[]))

    def test_invalid_question_type_rejected(self):
        with self.assertRaises(ValueError):
            self.engine.score_answer(**dict(self.base, question_type="unknown"))

    def test_invalid_difficulty_rejected(self):
        with self.assertRaises(ValueError):
            self.engine.score_answer(**dict(self.base, difficulty="expert"))

    def test_report_has_skill_breakdown(self):
        item = self.engine.score_answer(**self.base)
        report = self.engine.build_report("T047", [item])
        self.assertIn("Python", report["skill_wise_breakdown"])
        self.assertEqual(report["questions_evaluated"], 1)

    def test_report_rejects_mixed_candidates(self):
        item = self.engine.score_answer(**self.base)
        with self.assertRaises(ValueError):
            self.engine.build_report("OTHER", [item])

    def test_report_files_written(self):
        item = self.engine.score_answer(**self.base)
        report = self.engine.build_report("T047", [item])
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp) / "report.json"
            md_path = Path(tmp) / "report.md"
            self.engine.save_report(report, json_path, md_path)
            self.assertTrue(json_path.exists())
            self.assertTrue(md_path.exists())


if __name__ == "__main__":
    unittest.main()
