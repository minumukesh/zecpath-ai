import unittest

from src.interview_system.machine_test_engine import (
    MachineTestEvaluationEngine,
    MachineTestSubmission
)


class TestMachineTestEvaluationEngine(unittest.TestCase):

    def setUp(self):
        self.engine = MachineTestEvaluationEngine()

    def make_submission(self, **changes):

        values = {
            "candidate_id": "TEST-001",
            "task_id": "TASK-001",
            "task_type": "coding",
            "time_limit_minutes": 30,
            "time_taken_minutes": 25,
            "total_test_cases": 10,
            "passed_test_cases": 8,
            "efficiency_score": 80,
            "code_quality_score": 85,
            "problem_solving_score": 90,
            "code_snapshot": "def test(): return True",
            "execution_output": "8/10 passed"
        }

        values.update(changes)

        return MachineTestSubmission(**values)

    def test_evaluation_completes(self):
        result = self.engine.evaluate(self.make_submission())
        self.assertEqual(result["day"], 50)

    def test_correctness_calculation(self):
        result = self.engine.evaluate(self.make_submission())
        self.assertEqual(
            result["evaluation_metrics"]["correctness"], 80.0
        )

    def test_weighted_score(self):
        result = self.engine.evaluate(self.make_submission())
        self.assertEqual(result["scoring"]["base_score"], 83.0)

    def test_within_time_limit(self):
        result = self.engine.evaluate(self.make_submission())
        self.assertEqual(
            result["time_evaluation"]["time_status"],
            "WITHIN_TIME_LIMIT"
        )

    def test_time_penalty(self):
        result = self.engine.evaluate(
            self.make_submission(time_taken_minutes=35)
        )
        self.assertEqual(
            result["time_evaluation"]["time_penalty"], 10.0
        )

    def test_score_is_bounded(self):
        result = self.engine.evaluate(
            self.make_submission(
                passed_test_cases=10,
                efficiency_score=100,
                code_quality_score=100,
                problem_solving_score=100
            )
        )
        self.assertLessEqual(result["scoring"]["final_score"], 100)

    def test_all_task_types(self):

        for task_type in [
            "coding",
            "debugging",
            "file_based",
            "system_design"
        ]:

            result = self.engine.evaluate(
                self.make_submission(task_type=task_type)
            )

            self.assertEqual(result["task_type"], task_type)

    def test_invalid_task_type(self):
        with self.assertRaises(ValueError):
            self.engine.evaluate(
                self.make_submission(task_type="unknown")
            )

    def test_invalid_test_case_count(self):
        with self.assertRaises(ValueError):
            self.engine.evaluate(
                self.make_submission(
                    passed_test_cases=11,
                    total_test_cases=10
                )
            )

    def test_invalid_score(self):
        with self.assertRaises(ValueError):
            self.engine.evaluate(
                self.make_submission(efficiency_score=110)
            )

    def test_invalid_time_limit(self):
        with self.assertRaises(ValueError):
            self.engine.evaluate(
                self.make_submission(time_limit_minutes=0)
            )

    def test_code_snapshot_required(self):
        with self.assertRaises(ValueError):
            self.engine.evaluate(
                self.make_submission(code_snapshot="")
            )

    def test_explainable_breakdown_exists(self):
        result = self.engine.evaluate(self.make_submission())
        self.assertIn("correctness", result["weighted_breakdown"])
        self.assertIn("efficiency", result["weighted_breakdown"])
        self.assertIn("code_quality", result["weighted_breakdown"])
        self.assertIn("problem_solving", result["weighted_breakdown"])


if __name__ == "__main__":
    unittest.main()
