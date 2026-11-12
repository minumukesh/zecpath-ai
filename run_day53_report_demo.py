from src.interview_system.hiring_intelligence_report_generator import (
    HiringIntelligenceReportGenerator
)


def run_demo():

    generator = HiringIntelligenceReportGenerator()

    candidate = {

        "candidate": {
            "candidate_id": "DEMO-053",
            "candidate_name": "Candidate Demo",
            "target_role": "Data Analyst",
            "experience": "Fresher",
            "skills": ["Python", "SQL", "Excel", "Power BI"]
        },

        "ats": {
            "score": 88,
            "summary": "Strong resume match."
        },

        "screening": {
            "score": 85,
            "summary": "Passed initial screening."
        },

        "hr_interview": {
            "score": 82,
            "summary": "Good communication and role understanding.",
            "notes": ["Explained projects clearly."]
        },

        "technical_interview": {
            "score": 87,
            "machine_test_score": 90,
            "summary": "Strong technical performance.",
            "skills": {
                "Python": 90,
                "SQL": 88
            }
        },

        "behavioral": {
            "task_focus_score": 85,
            "distraction_frequency": 0.2,
            "observations": ["Task-related focus observations recorded."]
        },

        "integrity": {
            "flags": []
        },

        "strengths": ["Strong analytical thinking."],

        "weaknesses": ["Limited industry experience."],

        "missing_stages": [],

        "evidence_verified": True,

        "final_decision": {
            "recommendation": "SELECTED",
            "hiring_fit_score": 86.5,
            "confidence_score": 95,
            "explanation": "Strong performance across evaluation stages."
        }
    }

    report = generator.generate_report(candidate)

    output = "outputs/day53/demo_candidate_report"

    generator.export_json(report, output + ".json")

    generator.export_markdown(report, output + ".md")

    generator.export_html(report, output + ".html")

    print("\nDAY 53 REPORT DEMONSTRATION")

    print("Candidate:", report["candidate_profile"]["candidate_name"])

    print("Recommendation:", report["final_recommendation"]["recommendation"])

    print("Hiring Fit Score:", report["final_recommendation"]["hiring_fit_score"])

    print("Strengths:", len(report["candidate_assessment"]["strengths"]))

    print("Weaknesses:", len(report["candidate_assessment"]["weaknesses"]))

    print("Risk indicators:", len(report["candidate_assessment"]["risk_indicators"]))

    print("\nAll three report formats generated successfully.")


if __name__ == "__main__":
    run_demo()
