# ============================================================
# DAY 9 - RESUME SKILL EXTRACTION TEST
# ============================================================

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


results = extract_skills(
    resume_text
)


print()
print("=" * 65)
print("SKILL EXTRACTION TEST")
print("=" * 65)

print()
print(f"Resume ID: {resume_id}")

print()
print("Extracted skills:")
print("-" * 65)


for item in results:

    print(
        f"{item['skill']:<25}"
        f"{item['category']:<12}"
        f"confidence={item['confidence']:.2f} "
        f"source={item['source']}"
    )


print()
print("-" * 65)

print(
    f"Total skills detected: "
    f"{len(results)}"
)