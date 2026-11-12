import tempfile
import unittest
from pathlib import Path

from src.interview_summary import (
    normalize_score,
    identify_inconsistencies,
    identify_risk_flags,
    identify_cultural_fit_indicators,
    calculate_overall_performance,
    build_strengths_and_weaknesses,
    generate_natural_language_report,
    generate_interview_summary,
    save_interview_report,
)


def sample_interview():
    return {
        "candidate_id": "TEST-001",
        "candidate_name": "Test Candidate",
        "role": "Data Analyst",
        "strengths": ["Explains data checks clearly"],
        "weaknesses": ["Needs more detailed examples"],
        "collaboration_indicators": ["Listens to feedback"],
        "risk_flags": ["Availability requires confirmation"],
        "scores": {
            "answer_relevance": 80,
            "communication": 85,
            "problem_solving": 90,
        },
        "answers": [
            {"topic": "availability", "value": "One month"},
            {"topic": "availability", "value": "Immediately"},
        ],
    }


class TestInterviewSummary(unittest.TestCase):

    def test_score_validation(self):
        self.assertEqual(normalize_score(80), 80.0)

    def test_invalid_score_rejected(self):
        with self.assertRaises(ValueError):
            normalize_score(120)

    def test_inconsistency_detection(self):
        result = identify_inconsistencies([
            {"topic": "notice", "value": "Two weeks"},
            {"topic": "notice", "value": "One month"},
        ])
        self.assertEqual(len(result), 1)

    def test_same_answers_not_flagged(self):
        result = identify_inconsistencies([
            {"topic": "notice", "value": "Two weeks"},
            {"topic": "notice", "value": "Two weeks"},
        ])
        self.assertEqual(result, [])

    def test_risk_flags_are_preserved(self):
        result = identify_risk_flags({
            "risk_flags": ["Needs availability confirmation"]
        })
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["status"], "REVIEW_REQUIRED")

    def test_collaboration_indicators(self):
        result = identify_cultural_fit_indicators({
            "collaboration_indicators": ["Listens to feedback"]
        })
        self.assertEqual(len(result), 1)

    def test_performance_average(self):
        result = calculate_overall_performance({
            "relevance": 80,
            "communication": 100,
        })
        self.assertEqual(result["overall_score"], 90.0)

    def test_empty_scores(self):
        result = calculate_overall_performance({})
        self.assertIsNone(result["overall_score"])
        self.assertEqual(
            result["performance_label"],
            "NOT_ENOUGH_DATA",
        )

    def test_strengths_and_weaknesses(self):
        result = build_strengths_and_weaknesses({
            "strengths": ["Clear explanation"],
            "weaknesses": ["Needs examples"],
        })
        self.assertEqual(len(result["strengths"]), 1)
        self.assertEqual(len(result["weaknesses"]), 1)

    def test_structured_summary(self):
        result = generate_interview_summary(sample_interview())
        self.assertIn("candidate", result)
        self.assertIn("findings", result)
        self.assertIn("overall_performance", result)
        self.assertIn("natural_language_report", result)

    def test_natural_language_report(self):
        summary = generate_interview_summary(sample_interview())
        report = generate_natural_language_report(summary)
        self.assertIn("STRENGTHS", report)
        self.assertIn("RISK FLAGS", report)

    def test_missing_candidate_data_is_recorded(self):
        result = generate_interview_summary({
            "candidate_name": "Unknown",
            "scores": {},
        })
        self.assertIn("candidate_id", result["missing_data"])
        self.assertIn("role", result["missing_data"])
        self.assertIn("scores", result["missing_data"])

    def test_report_files_created(self):
        summary = generate_interview_summary(sample_interview())

        with tempfile.TemporaryDirectory() as directory:
            json_path, markdown_path = save_interview_report(
                summary,
                directory,
            )
            self.assertTrue(Path(json_path).exists())
            self.assertTrue(Path(markdown_path).exists())

    def test_empty_interview_rejected(self):
        with self.assertRaises(ValueError):
            generate_interview_summary(None)


if __name__ == "__main__":
    unittest.main()
