import json
import tempfile
import unittest
from pathlib import Path

from src.screening_report.builder import (
    build_screening_report,
    generate_markdown_report,
    save_screening_report,
    generate_sample_reports,
)


def sample_candidate():
    return {
        "candidate_id": "TEST-001",
        "candidate_name": "Test Candidate",
        "job_role": "Data Analyst",
        "ats_score": 80,
        "confirmed_skills": ["Python", "SQL", "Python"],
        "salary_expectation": "INR 30000 per month",
        "availability": "30 days",
        "answers": [
            {
                "question": "Which skills do you know?",
                "answer": "Python and SQL",
                "status": "provided",
            },
            {
                "question": "What is your salary expectation?",
                "answer": "",
                "status": "missing",
            },
        ],
    }


class TestScreeningReportGenerator(unittest.TestCase):

    def test_report_contains_candidate_details(self):
        report = build_screening_report(sample_candidate())
        self.assertEqual(
            report["candidate"]["candidate_id"],
            "TEST-001",
        )
        self.assertEqual(
            report["candidate"]["job_role"],
            "Data Analyst",
        )

    def test_score_is_normalised_and_preserved(self):
        report = build_screening_report(sample_candidate())
        self.assertEqual(
            report["screening_summary"]["ats_score"],
            80.0,
        )

    def test_invalid_score_becomes_unavailable(self):
        candidate = sample_candidate()
        candidate["ats_score"] = "unknown"

        report = build_screening_report(candidate)

        self.assertIsNone(
            report["screening_summary"]["ats_score"]
        )

    def test_missing_data_is_identified(self):
        report = build_screening_report(sample_candidate())

        self.assertIn(
            "one_or_more_answers",
            report["screening_summary"]["missing_data"],
        )

    def test_salary_and_availability_are_highlighted(self):
        report = build_screening_report(sample_candidate())
        highlights = report["screening_highlights"]

        self.assertEqual(
            highlights["salary_expectation"],
            "INR 30000 per month",
        )
        self.assertEqual(
            highlights["availability"],
            "30 days",
        )

    def test_duplicate_skills_are_removed(self):
        report = build_screening_report(sample_candidate())

        self.assertEqual(
            report["screening_highlights"]["confirmed_skills"],
            ["Python", "SQL"],
        )

    def test_markdown_report_contains_sections(self):
        report = build_screening_report(sample_candidate())
        markdown = generate_markdown_report(report)

        self.assertIn("# AI Screening Report", markdown)
        self.assertIn("## Strengths", markdown)
        self.assertIn("## Risks and Review Points", markdown)
        self.assertIn("## Missing Data", markdown)
        self.assertIn("## Recruiter Review", markdown)

    def test_json_and_markdown_files_are_created(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = save_screening_report(
                sample_candidate(),
                output_directory=temp_dir,
            )

            json_path = Path(result["json_path"])
            markdown_path = Path(result["markdown_path"])

            self.assertTrue(json_path.exists())
            self.assertTrue(markdown_path.exists())

            saved = json.loads(
                json_path.read_text(encoding="utf-8")
            )

            self.assertEqual(
                saved["candidate"]["candidate_id"],
                "TEST-001",
            )

    def test_multiple_sample_reports_are_generated(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = generate_sample_reports(
                [sample_candidate(), sample_candidate()],
                output_directory=temp_dir,
            )

            self.assertEqual(
                result["summary"]["reports_generated"],
                2,
            )
            self.assertTrue(
                Path(result["summary_path"]).exists()
            )

    def test_invalid_candidate_input_is_rejected(self):
        with self.assertRaises(TypeError):
            build_screening_report("not a dictionary")


if __name__ == "__main__":
    unittest.main()
