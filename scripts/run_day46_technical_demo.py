import json
from pathlib import Path
from src.interview_system.technical_engine import TechnicalInterviewEngine

def main():
    engine = TechnicalInterviewEngine()
    candidates = [
        {"candidate_id": "TECH001", "role": "mern", "experience_years": 1},
        {"candidate_id": "TECH002", "role": "java", "experience_years": 4},
        {"candidate_id": "TECH003", "role": "devops", "experience_years": 5},
        {"candidate_id": "TECH004", "role": "mern", "experience_years": 7},
    ]
    results = []
    print("\n=== DAY 46: TECHNICAL INTERVIEW BLUEPRINT ===")

    for candidate in candidates:
        blueprint = engine.get_interview_blueprint(
            candidate["role"], candidate["experience_years"]
        )
        sections = blueprint.get("sections")
        if not isinstance(sections, dict):
            raise TypeError("Blueprint 'sections' must be a dictionary.")

        print("\n----------------------------------------")
        print("Candidate:", candidate["candidate_id"])
        print("Role:", blueprint["role"])
        print("Experience:", blueprint["experience_years"])
        print("Level:", blueprint["experience_level"])
        print("Skill domains:", ", ".join(blueprint["skill_domains"]))

        for section_name in ("introduction", "experience", "conceptual", "scenario"):
            questions = sections.get(section_name, [])
            if not isinstance(questions, list):
                raise TypeError(
                    f"Section {section_name!r} must contain a list, "
                    f"not {type(questions).__name__}."
                )
            print("\n" + section_name.upper())
            for number, question in enumerate(questions, 1):
                print(f"{number}. {question}")

        results.append({
            "candidate_id": candidate["candidate_id"],
            "role": blueprint["role"],
            "experience_years": blueprint["experience_years"],
            "experience_level": blueprint["experience_level"],
            "skill_domains": blueprint["skill_domains"],
            "interview_structure": blueprint["interview_structure"],
            "sections": sections,
            "difficulty_progression": blueprint["difficulty_progression"],
        })

    output = Path("outputs/day46/technical_interview_blueprints.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nDay 46 blueprint saved: {output}")
    print("Candidates processed:", len(results))

if __name__ == "__main__":
    main()
