# ============================================================
# DAY 9 - SKILL STACK TEST
# ============================================================

from parsers.skill_extractor import extract_skills


def run_test(text):

    print()
    print("=" * 65)
    print("SKILL STACK TEST")
    print("=" * 65)

    print()
    print("Input:")
    print(text)

    print()
    print("Extracted skills:")
    print("-" * 65)

    results = extract_skills(text)

    for item in results:

        print(
            f"- {item['skill']} "
            f"| confidence={item['confidence']:.2f} "
            f"| source={item['source']}"
        )


# MERN
run_test(
    "Experienced MERN stack developer."
)


# MEAN
run_test(
    "Worked with MEAN stack applications."
)


# LAMP
run_test(
    "Developed applications using LAMP."
)


# MEVN
run_test(
    "Experienced MEVN developer."
)