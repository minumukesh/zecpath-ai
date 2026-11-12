import json
from pathlib import Path
from src.interview_system.hr_engine import HRInterviewEngine

def main():
    source = Path("data/day45/hr_demo_dataset.json")
    with source.open("r", encoding="utf-8-sig") as handle:
        candidates = json.load(handle)

    engine = HRInterviewEngine()
    results = []

    print("\n=== Zecpath AI: Day 45 HR Interview Demo ===")
    for candidate in candidates:
        result = engine.evaluate_candidate(
            candidate["candidate_id"],
            candidate["candidate_name"],
            candidate["role"],
            candidate["scores"],
            candidate.get("manager_feedback", "")
        )
        results.append(result)
        print(f"\nCandidate: {result['candidate_name']}")
        print(f"Role: {result['role']}")
        print(f"Overall score: {result['score']}")
        print(f"Recommendation: {result['recommendation']}")
        for name, detail in result["score_breakdown"].items():
            print(f"  {name}: {detail['score']} x {detail['weight']} = {detail['weighted_contribution']}")
        print(f"Manager feedback: {result['manager_feedback']}")

    output = Path("outputs/day45/hr_interview_results.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nSaved results: {output}")

if __name__ == "__main__":
    main()