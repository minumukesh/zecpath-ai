from src.interview_system.cross_round_aggregation_engine import (
    CrossRoundAggregationEngine,
    CandidateStageScores
)


def run_demo():

    engine = CrossRoundAggregationEngine()

    candidates = [

        CandidateStageScores(
            candidate_id="CAND-001",
            candidate_name="Candidate A",
            target_role="data_analyst",
            ats=85,
            screening=80,
            hr_interview=88,
            technical_interview=90,
            machine_test=92,
            profile_group="entry_level"
        ),

        CandidateStageScores(
            candidate_id="CAND-002",
            candidate_name="Candidate B",
            target_role="software_developer",
            ats=75,
            screening=82,
            hr_interview=78,
            technical_interview=85,
            machine_test=90,
            profile_group="experienced"
        ),

        CandidateStageScores(
            candidate_id="CAND-003",
            candidate_name="Candidate C",
            target_role="business_analyst",
            ats=90,
            screening=88,
            hr_interview=85,
            technical_interview=75,
            machine_test=80,
            profile_group="career_transition"
        ),

        # Demonstrates missing-stage handling.
        CandidateStageScores(
            candidate_id="CAND-004",
            candidate_name="Candidate D",
            target_role="data_analyst",
            ats=80,
            screening=75,
            hr_interview=85,
            technical_interview=90,
            machine_test=None,
            profile_group="entry_level"
        )
    ]

    results = []

    print("\nDAY 51 CROSS-ROUND DEMONSTRATION")
    print("=" * 55)

    for candidate in candidates:

        result = engine.aggregate(candidate)

        results.append(result)

        print("\nCandidate:", candidate.candidate_name)

        print("Role:", candidate.target_role)

        print(
            "Hiring Fit Score:",
            result["aggregation"]["hiring_fit_score"]
        )

        print(
            "Performance:",
            result["aggregation"]["performance_category"]
        )

        print(
            "Missing stages:",
            result["aggregation"]["missing_stages"]
        )

    output_directory = "outputs/day51"

    engine.save_json_report(
        {
            "project": "ZECPATH-AI",
            "day": 51,
            "candidate_count": len(results),
            "candidate_results": results
        },
        f"{output_directory}/cross_round_aggregation_results.json"
    )

    # Save individual reports for the first candidate.
    engine.save_json_report(
        results[0],
        f"{output_directory}/unified_candidate_score.json"
    )

    engine.save_markdown_report(
        results[0],
        f"{output_directory}/hiring_intelligence_report.md"
    )

    print("\nReports generated successfully.")

    print("\nDAY 51 DEMONSTRATION COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    run_demo()
