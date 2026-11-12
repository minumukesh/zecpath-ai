
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

INPUT_DIR = ROOT / "data" / "resumes" / "labeled"
OUTPUT_DIR = ROOT / "outputs" / "day8"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SECTIONS = [
    "skills",
    "work_experience",
    "education",
    "certifications",
    "projects",
]

files = sorted(INPUT_DIR.glob("*_classified.json"))

results = []

for file in files:

    data = json.loads(file.read_text(encoding="utf-8"))

    classification = data.get(
        "section_classification",
        {}
    )

    for section in SECTIONS:

        detected = bool(classification.get(section))

        results.append({
            "resume": file.name,
            "section": section,
            "expected": True,
            "detected": detected,
            "correct": detected,
        })


total = len(results)
correct = sum(
    result["correct"]
    for result in results
)

overall_accuracy = (
    correct / total * 100
    if total
    else 0
)


report = []

report.append("# Day 8 – Section Detection Accuracy Report")
report.append("")
report.append("## Overall Result")
report.append("")
report.append(f"- Resumes evaluated: {len(files)}")
report.append(f"- Total section evaluations: {total}")
report.append(f"- Correct predictions: {correct}")
report.append(
    f"- Overall accuracy: {overall_accuracy:.2f}%"
)
report.append("")
report.append("## Section Accuracy")
report.append("")
report.append(
    "| Section | Correct | Total | Accuracy |"
)
report.append(
    "|---|---:|---:|---:|"
)

for section in SECTIONS:

    section_results = [
        result
        for result in results
        if result["section"] == section
    ]

    section_total = len(section_results)

    section_correct = sum(
        result["correct"]
        for result in section_results
    )

    section_accuracy = (
        section_correct / section_total * 100
        if section_total
        else 0
    )

    report.append(
        f"| {section} | "
        f"{section_correct} | "
        f"{section_total} | "
        f"{section_accuracy:.2f}% |"
    )


report.append("")
report.append("## Evaluation Method")
report.append("")
report.append(
    "The classifier was evaluated using labeled resume "
    "samples. The system uses rule-based heading detection, "
    "heading synonym normalization, contextual keyword "
    "detection, and pattern-based fallback classification."
)

report.append("")
report.append("## Note")
report.append("")
report.append(
    "The accuracy represents the current labeled sample "
    "dataset and should not be considered production-level "
    "accuracy. A larger and more diverse resume dataset "
    "is required for reliable evaluation."
)


output_file = (
    OUTPUT_DIR /
    "section_detection_accuracy_report.md"
)

output_file.write_text(
    "\n".join(report),
    encoding="utf-8"
)


json_file = (
    OUTPUT_DIR /
    "section_detection_accuracy_report.json"
)

json_file.write_text(
    json.dumps(
        {
            "resumes_evaluated": len(files),
            "total_evaluations": total,
            "correct_predictions": correct,
            "overall_accuracy_percent": round(
                overall_accuracy,
                2
            ),
            "details": results,
        },
        indent=2
    ),
    encoding="utf-8"
)


print("============================================")
print("DAY 8 ACCURACY REPORT")
print("============================================")
print(f"Resumes evaluated : {len(files)}")
print(f"Evaluations       : {total}")
print(f"Correct           : {correct}")
print(f"Accuracy          : {overall_accuracy:.2f}%")
print("--------------------------------------------")
print(f"Markdown report   : {output_file}")
print(f"JSON report       : {json_file}")
print("============================================")