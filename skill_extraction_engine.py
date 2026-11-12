# ============================================================
# DAY 9 - SKILL EXTRACTION ENGINE
# Zecpath AI
# ============================================================

import re
import spacy
from rapidfuzz import process, fuzz

from skill_dictionary import SKILL_DICTIONARY, SKILL_STACKS


# ============================================================
# 1. NLP PIPELINE
# ============================================================

nlp = spacy.blank("en")

ruler = nlp.add_pipe("entity_ruler")


# ============================================================
# 2. BUILD NLP PATTERNS
# ============================================================

patterns = []

for category, skills in SKILL_DICTIONARY.items():

    for canonical_skill, variations in skills.items():

        for variation in variations:

            patterns.append({
                "label": "SKILL",
                "pattern": variation,
                "id": canonical_skill
            })


ruler.add_patterns(patterns)


# ============================================================
# 3. NORMALIZATION MAP
# ============================================================

NORMALIZATION_MAP = {}

for category, skills in SKILL_DICTIONARY.items():

    for canonical_skill, variations in skills.items():

        NORMALIZATION_MAP[
            canonical_skill.lower()
        ] = canonical_skill

        for variation in variations:

            NORMALIZATION_MAP[
                variation.lower()
            ] = canonical_skill


# ============================================================
# 4. GET SKILL CATEGORY
# ============================================================

def get_skill_category(skill):

    for category, skills in SKILL_DICTIONARY.items():

        if skill in skills:
            return category

    return "unknown"


# ============================================================
# 5. NORMALIZE SKILL
# ============================================================

def normalize_skill(skill):

    cleaned = skill.strip().lower()

    return NORMALIZATION_MAP.get(
        cleaned,
        skill.strip()
    )


# ============================================================
# 6. CONFIDENCE SCORING
# ============================================================

def calculate_confidence(method, similarity=100):

    if method == "exact":
        return 0.98

    if method == "synonym":
        return 0.95

    if method == "stack":
        return 0.97

    if method == "fuzzy":

        score = similarity / 100

        return round(
            min(score, 0.90),
            2
        )

    return 0.80


# ============================================================
# 7. DIRECT DICTIONARY MATCHING
# ============================================================

def extract_dictionary_skills(text):

    extracted = []

    text_lower = text.lower()

    # Check longer phrases first.
    # Example:
    # "machine learning" before "learning"
    all_entries = []

    for category, skills in SKILL_DICTIONARY.items():

        for canonical_skill, variations in skills.items():

            all_entries.append(
                (
                    canonical_skill,
                    variations
                )
            )

    # Longest phrases first
    all_entries.sort(
        key=lambda x: max(
            [len(v) for v in x[1] + [x[0]]]
        ),
        reverse=True
    )

    occupied_ranges = []

    for canonical_skill, variations in all_entries:

        candidates = [
            canonical_skill
        ] + variations

        for candidate in candidates:

            pattern = (
                r"(?<![A-Za-z0-9])"
                + re.escape(candidate.lower())
                + r"(?![A-Za-z0-9])"
            )

            for match in re.finditer(
                pattern,
                text_lower
            ):

                start = match.start()
                end = match.end()

                # Prevent overlapping matches
                overlap = False

                for old_start, old_end in occupied_ranges:

                    if (
                        start < old_end
                        and end > old_start
                    ):
                        overlap = True
                        break

                if overlap:
                    continue

                occupied_ranges.append(
                    (start, end)
                )

                source_text = text[
                    start:end
                ]

                if (
                    source_text.lower()
                    == canonical_skill.lower()
                ):

                    method = "exact"

                else:

                    method = "synonym"

                extracted.append({

                    "skill": canonical_skill,

                    "category": get_skill_category(
                        canonical_skill
                    ),

                    "source_text": source_text,

                    "method": method,

                    "confidence":
                        calculate_confidence(
                            method
                        )
                })

    return extracted


# ============================================================
# 8. NLP ENTITY RECOGNITION
# ============================================================

def extract_nlp_skills(text):

    doc = nlp(text)

    extracted = []

    for entity in doc.ents:

        canonical_skill = normalize_skill(
            entity.ent_id_
        )

        # Dictionary matching already handles
        # exact/synonym recognition.
        # NLP entities are kept as additional evidence.

        extracted.append({

            "skill": canonical_skill,

            "category": get_skill_category(
                canonical_skill
            ),

            "source_text": entity.text,

            "method": "nlp",

            "confidence": 0.95
        })

    return extracted


# ============================================================
# 9. SKILL STACK DETECTION
# ============================================================

def extract_skill_stacks(text):

    text_lower = text.lower()

    extracted = []

    for stack, components in SKILL_STACKS.items():

        pattern = (
            r"(?<![A-Za-z0-9])"
            + re.escape(stack.lower())
            + r"(?![A-Za-z0-9])"
        )

        if re.search(pattern, text_lower):

            extracted.append({

                "skill": stack,

                "category": "technical",

                "source_text": stack,

                "method": "stack",

                "confidence":
                    calculate_confidence(
                        "stack"
                    ),

                "components": components
            })

    return extracted


# ============================================================
# 10. FUZZY SPELLING MATCHING
# ============================================================

def fuzzy_skill_matching(text):

    extracted = []

    # Create only canonical skill names
    canonical_skills = []

    for category, skills in SKILL_DICTIONARY.items():

        canonical_skills.extend(
            skills.keys()
        )

    canonical_skills = list(
        set(canonical_skills)
    )

    # Split text into words
    words = re.findall(
        r"[A-Za-z][A-Za-z0-9+#.-]*",
        text
    )

    # Get already recognized exact/synonym text
    known_text = set()

    for skill in extract_dictionary_skills(text):

        known_text.add(
            skill["source_text"].lower()
        )

    for word in words:

        if len(word) < 4:
            continue

        if word.lower() in known_text:
            continue

        match = process.extractOne(
            word,
            canonical_skills,
            scorer=fuzz.ratio
        )

        if not match:
            continue

        matched_skill = match[0]
        similarity = match[1]

        # Strong spelling similarity only
        if similarity >= 90:

            extracted.append({

                "skill": matched_skill,

                "category":
                    get_skill_category(
                        matched_skill
                    ),

                "source_text": word,

                "method": "fuzzy",

                "confidence":
                    calculate_confidence(
                        "fuzzy",
                        similarity
                    )
            })

    return extracted


# ============================================================
# 11. DEDUPLICATION
# ============================================================

def deduplicate_skills(skills):

    unique = {}

    for item in skills:

        skill = item["skill"]

        if skill not in unique:

            unique[skill] = item

        else:

            # Keep highest confidence result
            if (
                item["confidence"]
                >
                unique[skill]["confidence"]
            ):

                unique[skill] = item

    return list(unique.values())


# ============================================================
# 12. COMPLETE EXTRACTION ENGINE
# ============================================================

def extract_skills(text):

    if not text or not text.strip():

        return {
            "skills": [],
            "total_skills": 0
        }

    # Dictionary matching
    dictionary_skills = (
        extract_dictionary_skills(text)
    )

    # NLP recognition
    nlp_skills = (
        extract_nlp_skills(text)
    )

    # Skill stacks
    stack_skills = (
        extract_skill_stacks(text)
    )

    # Fuzzy spelling
    fuzzy_skills = (
        fuzzy_skill_matching(text)
    )

    # Combine
    all_skills = (
        dictionary_skills
        + nlp_skills
        + stack_skills
        + fuzzy_skills
    )

    # Remove duplicates
    final_skills = (
        deduplicate_skills(
            all_skills
        )
    )

    # Sort alphabetically
    final_skills.sort(
        key=lambda x: x["skill"].lower()
    )

    return {

        "skills": final_skills,

        "total_skills":
            len(final_skills)
    }


# ============================================================
# 13. DAY 9 TEST RESUME
# ============================================================

if __name__ == "__main__":

    resume_text = """

    Experienced Python Developer with expertise in
    Machine Learning, Data Analytics, SQL and Power BI.

    Worked with the MERN stack including MongoDB,
    Express, React and Node.js.

    Strong communication and problem solving skills.

    Experienced in GitHub, Docker and Canva.

    Also familiar with AWS, JavaScript and Figma.
    """


    result = extract_skills(
        resume_text
    )


    # ========================================================
    # DISPLAY RESULTS
    # ========================================================

    print()
    print("=" * 60)
    print("           DAY 9 - SKILL EXTRACTION ENGINE")
    print("=" * 60)
    print()

    for skill in result["skills"]:

        print(
            f"Skill       : "
            f"{skill['skill']}"
        )

        print(
            f"Category    : "
            f"{skill['category']}"
        )

        print(
            f"Source      : "
            f"{skill['source_text']}"
        )

        print(
            f"Method      : "
            f"{skill['method']}"
        )

        print(
            f"Confidence  : "
            f"{skill['confidence']}"
        )

        if "components" in skill:

            print(
                f"Components  : "
                f"{skill['components']}"
            )

        print("-" * 60)


    print()

    print(
        f"Total Skills: "
        f"{result['total_skills']}"
    )

    print()

    print("=" * 60)

    print(
        "Skill extraction completed successfully."
    )

    print("=" * 60)