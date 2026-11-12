import json
from datetime import datetime, timezone
from pathlib import Path
from src.interview_system.hr_engine import HRInterviewEngine

QUESTIONS = [
    ("introduction", "Please introduce yourself and summarize your background."),
    ("role_understanding", "Why are you interested in this role, and what do you understand about it?"),
    ("problem_solving", "Describe a problem you faced and how you solved it."),
    ("teamwork", "Describe how you handled a disagreement or worked with a team.")
]

def ask_score(label):
    while True:
        raw = input(f"Manager score for {label} (0-100): ").strip()
        try:
            score = float(raw)
            if 0 <= score <= 100:
                return score
            print("Enter a value between 0 and 100.")
        except ValueError:
            print("Enter a valid number.")

def main():
    print("\n=== DAY 45: LIVE HR INTERVIEW SIMULATION ===")
    print("This is a local demonstration. The manager enters evaluation scores.")
    candidate_id = input("Candidate ID: ").strip()
    candidate_name = input("Candidate name: ").strip()
    role = input("Job role: ").strip()
    if not candidate_id or not candidate_name or not role:
        raise SystemExit("Candidate ID, name and role are required.")

    answers = []
    print("\n--- Candidate interview ---")
    for section, question in QUESTIONS:
        print(f"\n[{section.upper()}] {question}")
        answer = input("Candidate answer: ").strip()
        if not answer:
            print("No answer entered. Recording as not provided.")
            answer = "[No answer provided]"
        answers.append({"section": section, "question": question, "answer": answer})

    print("\n--- Manager evaluation ---")
    print("Score each category based on the interview evidence.")
    scores = {
        "communication": ask_score("communication"),
        "role_understanding": ask_score("role understanding"),
        "problem_solving": ask_score("problem solving"),
        "professionalism": ask_score("professionalism"),
    }
    feedback = input("Manager feedback: ").strip()

    engine = HRInterviewEngine()
    result = engine.evaluate_candidate(
        candidate_id, candidate_name, role, scores, feedback
    )
    result["interview_answers"] = answers
    result["created_at"] = datetime.now(timezone.utc).isoformat()
    result["evaluation_method"] = "interactive demonstration with manager-entered scores"

    output = Path("outputs/day45/live_hr_interview_result.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n--- Evaluation summary ---")
    print("Candidate:", candidate_name)
    print("Overall score:", result["score"])
    print("Recommendation:", result["recommendation"])
    print("Score breakdown:")
    for name, detail in result["score_breakdown"].items():
        print(f"  {name}: {detail['score']} x {detail['weight']} = {detail['weighted_contribution']}")
    print("Manager feedback:", feedback)
    print("Saved:", output)
    print("\nReminder: recommendation is decision support, not an automated hiring decision.")

if __name__ == "__main__":
    main()
