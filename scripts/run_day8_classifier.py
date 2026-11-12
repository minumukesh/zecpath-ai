import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from resume_section_classifier.classifier import classify_resume

INPUT_DIR = ROOT / "data" / "resumes" / "samples"
OUTPUT_DIR = ROOT / "data" / "resumes" / "labeled"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for resume_file in sorted(INPUT_DIR.glob("*.txt")):
    text = resume_file.read_text(encoding="utf-8")
    result = classify_resume(text)

    output = {
        "resume_file": resume_file.name,
        "section_classification": result
    }

    output_file = OUTPUT_DIR / f"{resume_file.stem}_classified.json"

    output_file.write_text(
        json.dumps(output, indent=2),
        encoding="utf-8"
    )

    print(f"[PROCESSED] {resume_file.name}")
    print(f"[OUTPUT] {output_file}")
