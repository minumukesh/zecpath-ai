import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

sys.path.insert(0, str(ROOT / "src"))

from skill_extraction import extract_skills

INPUT_DIR = ROOT / "data" / "resumes" / "skill_samples"
OUTPUT_DIR = ROOT / "outputs" / "day9"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for resume_file in sorted(INPUT_DIR.glob("*.txt")):

    text = resume_file.read_text(encoding="utf-8")

    skills = extract_skills(text)

    output = {
        "resume_file": resume_file.name,
        "skill_count": len(skills),
        "skills": skills
    }

    output_file = (
        OUTPUT_DIR /
        f"{resume_file.stem}_skills.json"
    )

    output_file.write_text(
        json.dumps(output, indent=2),
        encoding="utf-8"
    )

    print(f"[PROCESSED] {resume_file.name}")
    print(f"[SKILLS FOUND] {len(skills)}")
    print(f"[OUTPUT] {output_file}")

print("")
print("============================================")
print("DAY 9 SKILL EXTRACTION COMPLETE")
print("============================================")
