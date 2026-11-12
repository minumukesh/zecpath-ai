"""
ZECPATH-AI Day 50
Machine Test AI Evaluation Engine

Evaluates structured machine-test results for:
- Coding problems
- Debugging tasks
- File-based tasks
- Mini system design tasks

The engine evaluates supplied execution evidence. It does not execute
untrusted candidate code. Production execution requires a secure,
isolated sandbox.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, List
from pathlib import Path
import json


TASK_TYPES = {
    "coding": "Coding Problem",
    "debugging": "Debugging Task",
    "file_based": "File-Based Task",
    "system_design": "Mini System Design"
}


@dataclass
class MachineTestSubmission:

    candidate_id: str
    task_id: str
    task_type: str

    time_limit_minutes: float
    time_taken_minutes: float

    total_test_cases: int
    passed_test_cases: int

    efficiency_score: float
    code_quality_score: float
    problem_solving_score: float

    code_snapshot: str
    execution_output: str

    execution_status: str = "COMPLETED"


class MachineTestEvaluationEngine:

    def __init__(self):

        self.weights = {
            "correctness": 0.40,
            "efficiency": 0.20,
            "code_quality": 0.20,
            "problem_solving": 0.20
        }

        self.time_penalty_per_minute = 2.0

    def evaluate(
        self,
        submission: MachineTestSubmission
    ) -> Dict[str, Any]:

        self._validate(submission)

        # ----------------------------------------------------
        # 1. CORRECTNESS
        # ----------------------------------------------------

        if submission.total_test_cases == 0:
            correctness = 0.0
        else:
            correctness = round(
                submission.passed_test_cases
                / submission.total_test_cases * 100,
                2
            )

        # ----------------------------------------------------
        # 2. OTHER EVALUATION METRICS
        # ----------------------------------------------------

        efficiency = round(submission.efficiency_score, 2)

        code_quality = round(submission.code_quality_score, 2)

        problem_solving = round(
            submission.problem_solving_score, 2
        )

        # ----------------------------------------------------
        # 3. BASE WEIGHTED SCORE
        # ----------------------------------------------------

        base_score = (
            correctness * self.weights["correctness"]
            + efficiency * self.weights["efficiency"]
            + code_quality * self.weights["code_quality"]
            + problem_solving * self.weights["problem_solving"]
        )

        # ----------------------------------------------------
        # 4. TIME-BASED SCORING
        # ----------------------------------------------------

        if submission.time_taken_minutes <= submission.time_limit_minutes:

            time_penalty = 0.0

            time_status = "WITHIN_TIME_LIMIT"

        else:

            excess_time = (
                submission.time_taken_minutes
                - submission.time_limit_minutes
            )

            time_penalty = min(
                excess_time * self.time_penalty_per_minute,
                20.0
            )

            time_status = "TIME_LIMIT_EXCEEDED"

        final_score = round(
            max(0.0, min(100.0, base_score - time_penalty)),
            2
        )

        # ----------------------------------------------------
        # 5. PERFORMANCE CLASSIFICATION
        # ----------------------------------------------------

        if final_score >= 85:
            performance = "EXCELLENT"

        elif final_score >= 70:
            performance = "GOOD"

        elif final_score >= 50:
            performance = "AVERAGE"

        else:
            performance = "NEEDS_IMPROVEMENT"

        # ----------------------------------------------------
        # 6. TASK-SPECIFIC EVALUATION
        # ----------------------------------------------------

        task_feedback = self._task_feedback(
            submission.task_type,
            correctness,
            problem_solving
        )

        # ----------------------------------------------------
        # 7. EXPLAINABLE BREAKDOWN
        # ----------------------------------------------------

        breakdown = {
            "correctness": {
                "score": correctness,
                "weight": self.weights["correctness"],
                "contribution": round(
                    correctness * self.weights["correctness"], 2
                ),
                "explanation": (
                    f"{submission.passed_test_cases} of "
                    f"{submission.total_test_cases} test cases passed."
                )
            },

            "efficiency": {
                "score": efficiency,
                "weight": self.weights["efficiency"],
                "contribution": round(
                    efficiency * self.weights["efficiency"], 2
                ),
                "explanation": (
                    "Efficiency score supplied by the task evaluator."
                )
            },

            "code_quality": {
                "score": code_quality,
                "weight": self.weights["code_quality"],
                "contribution": round(
                    code_quality * self.weights["code_quality"], 2
                ),
                "explanation": (
                    "Code quality score supplied by the task evaluator."
                )
            },

            "problem_solving": {
                "score": problem_solving,
                "weight": self.weights["problem_solving"],
                "contribution": round(
                    problem_solving * self.weights["problem_solving"], 2
                ),
                "explanation": (
                    "Problem-solving score supplied by the task evaluator."
                )
            }
        }

        return {
            "project": "ZECPATH-AI",
            "day": 50,
            "module": "Machine Test AI Design",

            "candidate_id": submission.candidate_id,
            "task_id": submission.task_id,

            "task_type": submission.task_type,
            "task_name": TASK_TYPES[submission.task_type],

            "evaluation_status": submission.execution_status,

            "evaluation_metrics": {
                "correctness": correctness,
                "efficiency": efficiency,
                "code_quality": code_quality,
                "problem_solving": problem_solving
            },

            "weighted_breakdown": breakdown,

            "time_evaluation": {
                "time_limit_minutes": submission.time_limit_minutes,
                "time_taken_minutes": submission.time_taken_minutes,
                "time_status": time_status,
                "time_penalty": round(time_penalty, 2)
            },

            "scoring": {
                "base_score": round(base_score, 2),
                "final_score": final_score,
                "performance": performance
            },

            "task_feedback": task_feedback,

            "input_output_capture": {
                "code_snapshot": submission.code_snapshot,
                "execution_output": submission.execution_output
            },

            "explanation": (
                "The final score combines correctness, efficiency, "
                "code quality, and problem-solving using configured "
                "weights, followed by a time penalty."
            ),

            "limitations": [
                "This prototype evaluates supplied execution evidence.",
                "It does not execute untrusted candidate code.",
                "Efficiency and code-quality scores require an evaluator.",
                "Problem-solving scores require a documented rubric.",
                "Production execution requires an isolated sandbox."
            ]
        }

    @staticmethod
    def _task_feedback(task_type, correctness, problem_solving):

        feedback = {
            "coding": (
                "Evaluate algorithm correctness, edge cases, complexity, "
                "and implementation quality."
            ),
            "debugging": (
                "Evaluate defect identification, root-cause analysis, "
                "and correctness of the fix."
            ),
            "file_based": (
                "Evaluate file processing, output correctness, "
                "data handling, and validation."
            ),
            "system_design": (
                "Evaluate architecture, component separation, scalability, "
                "reliability, and design trade-offs."
            )
        }

        suggestions = []

        if correctness < 70:
            suggestions.append(
                "Review failed test cases and improve correctness."
            )

        if problem_solving < 60:
            suggestions.append(
                "Improve the explanation of the problem-solving approach."
            )

        if not suggestions:
            suggestions.append(
                "Continue practicing with more complex technical tasks."
            )

        return {
            "evaluation_focus": feedback[task_type],
            "improvement_suggestions": suggestions
        }

    @staticmethod
    def _validate(submission):

        if not submission.candidate_id.strip():
            raise ValueError("Candidate ID cannot be empty.")

        if not submission.task_id.strip():
            raise ValueError("Task ID cannot be empty.")

        if submission.task_type not in TASK_TYPES:
            raise ValueError("Unsupported task type.")

        if submission.time_limit_minutes <= 0:
            raise ValueError("Time limit must be greater than zero.")

        if submission.time_taken_minutes < 0:
            raise ValueError("Time taken cannot be negative.")

        if submission.total_test_cases <= 0:
            raise ValueError("Total test cases must be greater than zero.")

        if not (
            0 <= submission.passed_test_cases
            <= submission.total_test_cases
        ):
            raise ValueError("Invalid passed test-case count.")

        scores = [
            submission.efficiency_score,
            submission.code_quality_score,
            submission.problem_solving_score
        ]

        if any(not 0 <= score <= 100 for score in scores):
            raise ValueError("All evaluation scores must be between 0 and 100.")

        if submission.task_type != "system_design":
            if not submission.code_snapshot.strip():
                raise ValueError(
                    "Code snapshot is required for coding-related tasks."
                )

    @staticmethod
    def save_report(report, output_path):

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as file:
            json.dump(report, file, indent=4)

        return str(path)

    @staticmethod
    def save_markdown_report(report, output_path):

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "# ZECPATH-AI Machine Test Evaluation",
            "",
            f"- Candidate: {report['candidate_id']}",
            f"- Task: {report['task_id']}",
            f"- Task type: {report['task_name']}",
            "",
            "## Evaluation Metrics",
            "",
            "| Metric | Score | Weight | Contribution |",
            "|---|---:|---:|---:|"
        ]

        for name, item in report["weighted_breakdown"].items():
            lines.append(
                f"| {name.replace('_', ' ').title()} "
                f"| {item['score']} "
                f"| {item['weight']} "
                f"| {item['contribution']} |"
            )

        lines.extend([
            "",
            "## Final Result",
            "",
            f"- Base score: {report['scoring']['base_score']}",
            f"- Time penalty: {report['time_evaluation']['time_penalty']}",
            f"- Final score: {report['scoring']['final_score']}",
            f"- Performance: {report['scoring']['performance']}",
            "",
            "## Time Evaluation",
            "",
            f"- Time limit: {report['time_evaluation']['time_limit_minutes']} minutes",
            f"- Time taken: {report['time_evaluation']['time_taken_minutes']} minutes",
            f"- Status: {report['time_evaluation']['time_status']}",
            "",
            "## Feedback",
            "",
            report["task_feedback"]["evaluation_focus"],
            ""
        ])

        for suggestion in report["task_feedback"]["improvement_suggestions"]:
            lines.append(f"- {suggestion}")

        lines.extend([
            "",
            "## Limitations",
            ""
        ])

        for limitation in report["limitations"]:
            lines.append(f"- {limitation}")

        path.write_text("\n".join(lines), encoding="utf-8")

        return str(path)
