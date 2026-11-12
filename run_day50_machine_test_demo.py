from src.interview_system.machine_test_engine import (
    MachineTestEvaluationEngine,
    MachineTestSubmission
)


def run_demo():

    engine = MachineTestEvaluationEngine()

    submissions = [

        MachineTestSubmission(
            candidate_id="CANDIDATE-001",
            task_id="CODING-001",
            task_type="coding",
            time_limit_minutes=45,
            time_taken_minutes=38,
            total_test_cases=10,
            passed_test_cases=9,
            efficiency_score=85,
            code_quality_score=88,
            problem_solving_score=90,
            code_snapshot="def find_max(numbers): return max(numbers)",
            execution_output="9/10 test cases passed."
        ),

        MachineTestSubmission(
            candidate_id="CANDIDATE-001",
            task_id="DEBUG-001",
            task_type="debugging",
            time_limit_minutes=30,
            time_taken_minutes=35,
            total_test_cases=8,
            passed_test_cases=6,
            efficiency_score=75,
            code_quality_score=80,
            problem_solving_score=72,
            code_snapshot="Fixed loop boundary condition.",
            execution_output="6/8 debugging tests passed."
        ),

        MachineTestSubmission(
            candidate_id="CANDIDATE-001",
            task_id="FILE-001",
            task_type="file_based",
            time_limit_minutes=40,
            time_taken_minutes=35,
            total_test_cases=10,
            passed_test_cases=10,
            efficiency_score=90,
            code_quality_score=85,
            problem_solving_score=88,
            code_snapshot="CSV processing and validation implementation.",
            execution_output="10/10 file processing tests passed."
        ),

        MachineTestSubmission(
            candidate_id="CANDIDATE-001",
            task_id="DESIGN-001",
            task_type="system_design",
            time_limit_minutes=60,
            time_taken_minutes=55,
            total_test_cases=5,
            passed_test_cases=4,
            efficiency_score=82,
            code_quality_score=90,
            problem_solving_score=92,
            code_snapshot="API gateway, service layer, database, cache.",
            execution_output="4/5 architecture rubric checks passed."
        )
    ]

    reports = []

    for submission in submissions:

        report = engine.evaluate(submission)
        reports.append(report)

        print("\nTASK:", report["task_name"])
        print("Task ID:", report["task_id"])
        print("Correctness:", report["evaluation_metrics"]["correctness"])
        print("Final score:", report["scoring"]["final_score"])
        print("Performance:", report["scoring"]["performance"])

    output_directory = "outputs/day50"

    engine.save_report(
        {
            "project": "ZECPATH-AI",
            "day": 50,
            "candidate_id": "CANDIDATE-001",
            "task_reports": reports
        },
        f"{output_directory}/machine_test_evaluation.json"
    )

    markdown_path = (
        f"{output_directory}/machine_test_evaluation.md"
    )

    with open(markdown_path, "w", encoding="utf-8") as file:

        file.write("# ZECPATH-AI Day 50 Machine Test Report\n\n")

        for report in reports:

            file.write(f"## {report['task_name']}\n\n")
            file.write(
                f"- Final score: {report['scoring']['final_score']}\n"
            )
            file.write(
                f"- Performance: {report['scoring']['performance']}\n\n"
            )

    print("\nJSON report generated.")
    print("Markdown report generated.")
    print("\nDAY 50 DEMONSTRATION COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    run_demo()
