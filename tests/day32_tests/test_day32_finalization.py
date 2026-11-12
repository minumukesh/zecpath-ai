import json
import tempfile
import unittest
from pathlib import Path

from src.day32_finalization import (
    inspect_project,
    load_demo_cases,
    evaluate_demo_case,
    build_finalization_report,
    write_reports,
)


ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data" / "day32" / "finalization_demo_cases.json"


class TestDay32Finalization(unittest.TestCase):

    def test_project_inspection_checks_components(self):
        result = inspect_project(ROOT)
        self.assertIn("components", result)
        self.assertGreater(result["components_checked"], 0)

    def test_demo_dataset_loads(self):
        cases = load_demo_cases(DATA_FILE)
        self.assertGreater(len(cases), 0)

    def test_invalid_demo_dataset_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text('{"not": "a list"}', encoding="utf-8")

            with self.assertRaises(ValueError):
                load_demo_cases(path)

    def test_demo_case_requires_resume(self):
        case = {
            "candidate_id": "TEST-001",
            "role": "Data Analyst",
            "resume_text": "",
            "job_description": "Requires Python",
        }

        with self.assertRaises(ValueError):
            # Validation occurs when loading a dataset.
            from src.day32_finalization.engine import load_demo_cases
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "invalid.json"
                path.write_text(json.dumps([case]), encoding="utf-8")
                load_demo_cases(path)

    def test_demo_returns_transparent_result(self):
        result = evaluate_demo_case({
            "candidate_id": "TEST-002",
            "role": "Data Analyst",
            "resume_text": "Python SQL Excel",
            "job_description": "Python SQL Excel",
        })

        self.assertIn("demo_keyword_overlap_score", result)
        self.assertIn("demo_result", result)
        self.assertIn("note", result)

    def test_demo_score_is_bounded(self):
        result = evaluate_demo_case({
            "candidate_id": "TEST-003",
            "role": "Data Analyst",
            "resume_text": "Python SQL Excel",
            "job_description": "Python SQL Excel",
        })

        self.assertGreaterEqual(
            result["demo_keyword_overlap_score"], 0
        )
        self.assertLessEqual(
            result["demo_keyword_overlap_score"], 100
        )

    def test_finalization_report_has_checklist(self):
        cases = load_demo_cases(DATA_FILE)
        report = build_finalization_report(ROOT, cases)

        self.assertIn("finalization_checklist", report)
        self.assertIn("project_inspection", report)
        self.assertIn("demo", report)

    def test_reports_are_generated(self):
        cases = load_demo_cases(DATA_FILE)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data" / "day32").mkdir(parents=True)
            (root / "data" / "day32" / "placeholder.json").write_text(
                "[]", encoding="utf-8"
            )
            report = build_finalization_report(root, cases)
            generated = write_reports(root, report)

            for path in generated.values():
                self.assertTrue(path.exists())

    def test_api_design_is_documented(self):
        cases = load_demo_cases(DATA_FILE)
        report = build_finalization_report(ROOT, cases)

        self.assertIn("api_design_explanation", report["finalization_checklist"])

    def test_demo_processes_all_cases(self):
        cases = load_demo_cases(DATA_FILE)
        report = build_finalization_report(ROOT, cases)

        self.assertEqual(
            report["demo"]["cases_processed"],
            len(cases),
        )


if __name__ == "__main__":
    unittest.main()
