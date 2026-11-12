# ============================================================
# DAY 9 - SKILL SYNONYM / NORMALIZATION TEST
# ============================================================

from parsers.skill_extractor import extract_skills


text = """

Python
JS
Java Script
PowerBI
Microsoft Power BI
Sklearn
Scikit Learn
NodeJS
Node JS
ReactJS
React.js
Customer Support
Team Work

"""


print()
print("=" * 65)
print("SKILL SYNONYM AND NORMALIZATION TEST")
print("=" * 65)

print()
print("Input:")
print(text)

print()
print("Normalized skills:")
print("-" * 65)


results = extract_skills(text)


for item in results:

    print(
        f"- {item['skill']} "
        f"| confidence={item['confidence']:.2f} "
        f"| source={item['source']}"
    )