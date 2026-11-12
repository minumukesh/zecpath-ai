import unittest

from src.day56_simulation.engine import (
    HiringPipeline,
    SimulationError
)


class Day56PipelineTests(unittest.TestCase):

    def setUp(self):

        self.pipeline = HiringPipeline()

        self.candidate = {
            "candidate_id": "TEST001",
            "candidate_name": "Test Candidate",
            "role": "data_analyst",
            "resume_text": (
                "Python SQL Excel Power BI statistics "
                "data analysis dashboard"
            ),
            "screening_score": 85,
            "hr_answers": [80, 85, 90, 85],
            "technical_answers": [90, 85, 88, 92],
            "human_decision": "RECOMMEND"
        }

    def test_resume_upload(self):

        result = self.pipeline.upload_resume(
            self.candidate
        )

        self.assertEqual(
            result["resume_status"],
            "UPLOADED"
        )

    def test_missing_resume_rejected(self):

        candidate = dict(self.candidate)
        candidate["resume_text"] = ""

        with self.assertRaises(SimulationError):

            self.pipeline.upload_resume(candidate)

    def test_invalid_role_rejected(self):

        candidate = dict(self.candidate)
        candidate["role"] = "unknown"

        with self.assertRaises(SimulationError):

            self.pipeline.upload_resume(candidate)

    def test_ats_scoring(self):

        result = self.pipeline.calculate_ats_score(
            self.candidate["resume_text"],
            "data_analyst"
        )

        self.assertEqual(result["score"], 100)

    def test_screening(self):

        result = self.pipeline.evaluate_screening(85)

        self.assertEqual(result["status"], "PASS")

    def test_invalid_screening_score(self):

        with self.assertRaises(SimulationError):

            self.pipeline.evaluate_screening(120)

    def test_hr_interview(self):

        result = self.pipeline.evaluate_hr_interview(
            [80, 90, 85]
        )

        self.assertEqual(result["score"], 85)

    def test_technical_interview(self):

        result = self.pipeline.evaluate_technical_interview(
            [90, 80, 85]
        )

        self.assertEqual(result["score"], 85)

    def test_final_score(self):

        stages = {
            "ats": {"score": 100},
            "screening": {"score": 80},
            "hr": {"score": 90},
            "technical": {"score": 90}
        }

        result = self.pipeline.calculate_final_score(stages)

        self.assertEqual(result, 90.5)

    def test_ai_decision(self):

        stages = {
            "ats": {"score": 100, "status": "PASS"},
            "screening": {"score": 90, "status": "PASS"},
            "hr": {"score": 85, "status": "PASS"},
            "technical": {"score": 90, "status": "PASS"}
        }

        result = self.pipeline.make_ai_decision(stages)

        self.assertEqual(
            result["recommendation"],
            "RECOMMEND"
        )

    def test_human_ai_agreement(self):

        ai = {"recommendation": "RECOMMEND"}

        result = self.pipeline.compare_human_ai(
            ai,
            "RECOMMEND"
        )

        self.assertTrue(result["agreement"])

    def test_human_ai_disagreement(self):

        ai = {"recommendation": "RECOMMEND"}

        result = self.pipeline.compare_human_ai(
            ai,
            "HOLD"
        )

        self.assertFalse(result["agreement"])

    def test_invalid_human_decision(self):

        with self.assertRaises(SimulationError):

            self.pipeline.compare_human_ai(
                {"recommendation": "RECOMMEND"},
                "UNKNOWN"
            )

    def test_complete_pipeline(self):

        result = self.pipeline.process_candidate(
            self.candidate
        )

        self.assertIn("ats", result["stages"])
        self.assertIn("screening", result["stages"])
        self.assertIn("hr", result["stages"])
        self.assertIn("technical", result["stages"])

    def test_inconsistency_detection(self):

        pipeline_result = self.pipeline.process_candidate(
            self.candidate
        )

        comparison = self.pipeline.compare_human_ai(
            pipeline_result["ai_decision"],
            "HOLD"
        )

        issues = self.pipeline.detect_inconsistencies(
            pipeline_result,
            comparison
        )

        self.assertTrue(
            any(
                issue["type"] == "AI_HUMAN_DISAGREEMENT"
                for issue in issues
            )
        )

    def test_complete_simulation(self):

        candidate = dict(self.candidate)

        candidate["human_decision"] = "RECOMMEND"

        report = self.pipeline.run_simulation(
            [candidate]
        )

        self.assertEqual(report["candidate_count"], 1)

        self.assertIn(
            "performance_analysis",
            report
        )

    def test_duplicate_candidate_rejected(self):

        with self.assertRaises(SimulationError):

            self.pipeline.run_simulation([
                self.candidate,
                self.candidate
            ])

    def test_empty_simulation_rejected(self):

        with self.assertRaises(SimulationError):

            self.pipeline.run_simulation([])


if __name__ == "__main__":
    unittest.main()
