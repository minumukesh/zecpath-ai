from src.interview_system.final_recommendation_engine import (
    FinalRecommendationEngine,
    CandidateDecisionInput
)


def run_demo():

    engine = FinalRecommendationEngine()

    candidates = [

        CandidateDecisionInput(
            candidate_id="CAND-001",
            candidate_name="Candidate A",
            target_role="Data Analyst",
            hiring_fit_score=90,
            available_stages=5,
            total_stages=5,
            integrity_flags=0,
            confirmed_integrity_breach=False,
            human_integrity_review_completed=True,
            behavioral_focus_score=85,
            technical_requirements_met=True,
            evidence_verified=True
        ),

        CandidateDecisionInput(
            candidate_id="CAND-002",
            candidate_name="Candidate B",
            target_role="Software Developer",
            hiring_fit_score=72,
            available_stages=5,
            total_stages=5,
            integrity_flags=0,
            confirmed_integrity_breach=False,
            human_integrity_review_completed=True,
            technical_requirements_met=True,
            evidence_verified=True
        ),

        CandidateDecisionInput(
            candidate_id="CAND-003",
            candidate_name="Candidate C",
            target_role="Data Scientist",
            hiring_fit_score=45,
            available_stages=5,
            total_stages=5,
            integrity_flags=0,
            confirmed_integrity_breach=False,
            human_integrity_review_completed=True,
            technical_requirements_met=True,
            evidence_verified=True
        ),

        CandidateDecisionInput(
            candidate_id="CAND-004",
            candidate_name="Candidate D",
            target_role="Data Analyst",
            hiring_fit_score=90,
            available_stages=5,
            total_stages=5,
            integrity_flags=2,
            confirmed_integrity_breach=False,
            human_integrity_review_completed=False,
            technical_requirements_met=True,
            evidence_verified=True
        ),

        CandidateDecisionInput(
            candidate_id="CAND-005",
            candidate_name="Candidate E",
            target_role="Data Analyst",
            hiring_fit_score=92,
            available_stages=5,
            total_stages=5,
            integrity_flags=0,
            confirmed_integrity_breach=True,
            human_integrity_review_completed=False,
            technical_requirements_met=True,
            evidence_verified=True
        )
    ]

    reports = []

    print("\nDAY 52 FINAL RECOMMENDATION DEMO")
    print("=" * 55)

    for candidate in candidates:

        result = engine.evaluate(candidate)

        reports.append(result)

        print("\nCandidate:", candidate.candidate_name)

        print(
            "Hiring Fit Score:",
            result["decision"]["hiring_fit_score"]
        )

        print(
            "Confidence:",
            result["decision"]["confidence_score"]
        )

        print(
            "Recommendation:",
            result["decision"]["recommendation"]
        )

        print(
            "Human Review:",
            result["human_review"]["required"]
        )

    # Save all candidate results.
    engine.save_json_report(
        {
            "project": "ZECPATH-AI",
            "day": 52,
            "candidate_count": len(reports),
            "candidate_decisions": reports
        },
        "outputs/day52/all_candidate_recommendations.json"
    )

    # Save first candidate's individual reports.
    engine.save_json_report(
        reports[0],
        "outputs/day52/final_recommendation.json"
    )

    engine.save_markdown_report(
        reports[0],
        "outputs/day52/final_recommendation.md"
    )

    print("\nAll recommendation reports generated.")

    print("\nDAY 52 DEMONSTRATION COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    run_demo()
