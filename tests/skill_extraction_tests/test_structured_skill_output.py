# ============================================================
# DAY 9 - STRUCTURED SKILL OUTPUT
# ============================================================

import json

from parsers.skill_extractor import extract_skills


resume_id = "10001727"


resume_text = """

Project Management
Communication
Team Work
Problem Solving
Time Management
Customer Support
Sales
Marketing
Hospitality
Supervision
Accounting
Revenue Management
Customer Satisfaction
Data Entry
Inventory Management
Auditing
Staffing

"""


skills = extract_skills(
    resume_text
)


structured_output = {

    "resume_id":
        resume_id,

    "skills":
        skills
}


output_path = (
    "tests/"
    "skill_extraction_tests/"
    "structured_skill_output_10001727.json"
)


with open(
    output_path,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        structured_output,
        file,
        indent=4
    )


print()
print("=" * 65)
print("STRUCTURED SKILL OUTPUT")
print("=" * 65)

print()

print(
    json.dumps(
        structured_output,
        indent=4
    )
)

print()

print(
    f"Saved to: {output_path}"
)