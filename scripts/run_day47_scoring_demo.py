"""Day 47 demonstration: technical skill scoring and explainable report."""
from pathlib import Path
import sys

# Make execution from project root reliable.
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.interview_system.technical_scoring_engine import TechnicalSkillScoringEngine


def main():
    engine = TechnicalSkillScoringEngine()
    candidate_id = "TECH047"

    # Synthetic demonstration answers. Replace with actual interview answers
    # during a real assessment and have an interviewer review the output.
    answers = [
        {
            "skill": "Python",
            "question": "Explain how you handle exceptions in a production Python API.",
            "answer": (
                "First, I validate the input and use try and except to catch expected "
                "exceptions. For example, I return a clear error response and log the "
                "exception with a request identifier. In production I avoid exposing "
                "stack traces to users, add tests for edge cases, and monitor repeated "
                "failures. This improves security and debugging."
            ),
            "expected_concepts": ["try", "except", "logging", "testing"],
            "question_type": "scenario",
            "difficulty": "intermediate",
        },
        {
            "skill": "SQL",
            "question": "Explain the purpose of an index and one trade-off.",
            "answer": (
                "An index helps a database find rows faster instead of scanning the "
                "whole table. However, indexes use storage and can slow inserts and "
                "updates because the index must also be maintained. For example, "
                "I would inspect query plans and measure performance before adding "
                "an index to a production database."
            ),
            "expected_concepts": ["index", "database", "query", "storage"],
            "question_type": "conceptual",
            "difficulty": "intermediate",
        },
        {
            "skill": "REST API",
            "question": "Describe a reliable approach to designing an API endpoint.",
            "answer": (
                "I would define the resource and HTTP method, validate input, "
                "return suitable status codes, and write tests. First I would check "
                "authentication, then handle errors consistently. In a real application "
                "I would add logging, monitoring, and security controls."
            ),
            "expected_concepts": ["HTTP", "validate", "status codes", "tests"],
            "question_type": "system_design",
            "difficulty": "advanced",
        },
    ]

    evaluations = []
    print("\n=== DAY 47: TECHNICAL SKILL SCORING MODEL ===")
    for item in answers:
        result = engine.score_answer(candidate_id=candidate_id, **item)
        evaluations.append(result)
        print(
            f"\n{result['skill']}: {result['overall_score']}/100 "
            f"({result['performance_band']})"
        )
        print("Shallow answer:", result["is_shallow"])
        for name, component in result["component_scores"].items():
            print(f"  {name}: {component['score']}/100")
            print(f"    {component['explanation']}")

    report = engine.build_report(candidate_id, evaluations)
    engine.save_report(
        report,
        "outputs/day47/technical_skill_evaluation.json",
        "outputs/day47/technical_skill_evaluation.md",
    )
    print("\nSkill-wise breakdown:")
    for skill, data in report["skill_wise_breakdown"].items():
        print(f"  {skill}: {data['average_score']}/100 ({data['performance_band']})")
    print("\nSaved:")
    print("  outputs/day47/technical_skill_evaluation.json")
    print("  outputs/day47/technical_skill_evaluation.md")
    print("\nNote: These are synthetic demo answers. Human review is required.")


if __name__ == "__main__":
    main()
