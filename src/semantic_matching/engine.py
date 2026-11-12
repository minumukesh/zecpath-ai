import re
import math
from collections import Counter


def tokenize(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s-]", " ", text)
    return [
        word for word in text.split()
        if len(word) > 1
    ]


def build_embedding(text):
    """
    Create a lightweight text embedding using normalized
    TF-IDF-style term weighting.

    This provides a local embedding representation without
    requiring an external model download.
    """

    tokens = tokenize(text)

    if not tokens:
        return {}

    counts = Counter(tokens)
    total = len(tokens)

    embedding = {}

    for token, count in counts.items():
        embedding[token] = count / total

    return embedding


def cosine_similarity(vector_a, vector_b):
    """
    Calculate cosine similarity between two embeddings.
    """

    if not vector_a or not vector_b:
        return 0.0

    common = set(vector_a) & set(vector_b)

    numerator = sum(
        vector_a[key] * vector_b[key]
        for key in common
    )

    magnitude_a = math.sqrt(
        sum(value * value for value in vector_a.values())
    )

    magnitude_b = math.sqrt(
        sum(value * value for value in vector_b.values())
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return numerator / (
        magnitude_a * magnitude_b
    )


def extract_section(text, section_names):
    """
    Extract a section from a structured resume/JD.
    """

    lines = text.splitlines()

    collecting = False
    collected = []

    normalized_names = {
        name.lower()
        for name in section_names
    }

    for line in lines:

        stripped = line.strip()

        if not stripped:
            continue

        if stripped.lower().rstrip(":") in normalized_names:

            collecting = True
            continue

        if collecting:

            possible_heading = (
                stripped.lower().rstrip(":")
            )

            if (
                possible_heading in {
                    "skills",
                    "experience",
                    "work experience",
                    "projects",
                    "education",
                    "requirements",
                    "responsibilities",
                    "qualifications"
                }
            ):
                break

            collected.append(stripped)

    return " ".join(collected)


def compare_texts(resume_text, job_text):
    """
    Compare complete resume and job description.
    """

    resume_embedding = build_embedding(
        resume_text
    )

    job_embedding = build_embedding(
        job_text
    )

    score = cosine_similarity(
        resume_embedding,
        job_embedding
    )

    return round(score, 4)


def compare_sections(resume_text, job_text):
    """
    Compare skills, experience and project-related content.
    """

    resume_skills = extract_section(
        resume_text,
        ["skills"]
    )

    job_skills = extract_section(
        job_text,
        ["skills", "requirements"]
    )

    resume_experience = extract_section(
        resume_text,
        ["experience", "work experience"]
    )

    job_experience = extract_section(
        job_text,
        ["experience", "requirements", "responsibilities"]
    )

    resume_projects = extract_section(
        resume_text,
        ["projects"]
    )

    job_projects = extract_section(
        job_text,
        ["projects", "responsibilities"]
    )

    skill_score = compare_texts(
        resume_skills,
        job_skills
    )

    experience_score = compare_texts(
        resume_experience,
        job_experience
    )

    project_score = compare_texts(
        resume_projects,
        job_projects
    )

    return {
        "skills_similarity": skill_score,
        "experience_similarity": experience_score,
        "projects_similarity": project_score
    }


def calculate_match_score(
    skills_similarity,
    experience_similarity,
    projects_similarity
):
    """
    Weighted resume-to-job similarity score.
    """

    score = (
        skills_similarity * 0.45
        + experience_similarity * 0.35
        + projects_similarity * 0.20
    )

    return round(score, 4)


def classify_match(score):
    """
    Convert similarity score into a matching category.
    """

    if score >= 0.70:
        return "strong_match"

    if score >= 0.50:
        return "good_match"

    if score >= 0.30:
        return "partial_match"

    return "low_match"


def semantic_match(resume_text, job_text):
    """
    Main Semantic Matching Engine.
    """

    section_scores = compare_sections(
        resume_text,
        job_text
    )

    overall_similarity = compare_texts(
        resume_text,
        job_text
    )

    weighted_score = calculate_match_score(
        section_scores["skills_similarity"],
        section_scores["experience_similarity"],
        section_scores["projects_similarity"]
    )

    final_score = round(
        (overall_similarity * 0.30)
        + (weighted_score * 0.70),
        4
    )

    return {
        "overall_similarity": overall_similarity,
        "skills_similarity": section_scores[
            "skills_similarity"
        ],
        "experience_similarity": section_scores[
            "experience_similarity"
        ],
        "projects_similarity": section_scores[
            "projects_similarity"
        ],
        "match_score": final_score,
        "match_category": classify_match(
            final_score
        )
    }
