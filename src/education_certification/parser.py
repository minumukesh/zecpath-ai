import re


DEGREE_ALIASES = {
    "b.tech": "Bachelor of Technology",
    "btech": "Bachelor of Technology",
    "b.e": "Bachelor of Engineering",
    "be": "Bachelor of Engineering",
    "b.sc": "Bachelor of Science",
    "bsc": "Bachelor of Science",
    "bca": "Bachelor of Computer Applications",
    "m.tech": "Master of Technology",
    "mtech": "Master of Technology",
    "m.sc": "Master of Science",
    "msc": "Master of Science",
    "mca": "Master of Computer Applications",
    "mba": "Master of Business Administration",
    "phd": "Doctor of Philosophy",
}


FIELD_ALIASES = {
    "computer science": "Computer Science",
    "computer science engineering": "Computer Science",
    "cse": "Computer Science",
    "information technology": "Information Technology",
    "it": "Information Technology",
    "data science": "Data Science",
    "data analytics": "Data Analytics",
    "business administration": "Business Administration",
    "business management": "Business Administration",
    "electronics engineering": "Electronics Engineering",
    "mechanical engineering": "Mechanical Engineering",
    "electrical engineering": "Electrical Engineering",
    "commerce": "Commerce",
    "statistics": "Statistics",
}


CERTIFICATION_CATEGORIES = {
    "aws": "Cloud",
    "azure": "Cloud",
    "google cloud": "Cloud",
    "gcp": "Cloud",
    "data analytics": "Data",
    "data science": "Data",
    "tableau": "Data",
    "power bi": "Data",
    "python": "Programming",
    "java": "Programming",
    "javascript": "Programming",
    "pmp": "Project Management",
    "scrum": "Project Management",
    "security+": "Cybersecurity",
    "ceh": "Cybersecurity",
    "cybersecurity": "Cybersecurity",
    "six sigma": "Business",
}


def normalize_degree(value):
    clean = value.lower().strip()
    clean = re.sub(r"\s+", " ", clean)

    for alias, canonical in DEGREE_ALIASES.items():
        if alias in clean:
            return canonical

    return value.strip()


def normalize_field(value):
    clean = value.lower().strip()

    for alias, canonical in FIELD_ALIASES.items():
        if alias in clean:
            return canonical

    return value.strip()


def categorize_certification(name):
    lower = name.lower()

    for keyword, category in CERTIFICATION_CATEGORIES.items():
        if keyword in lower:
            return category

    return "Other"


def extract_education(text):
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    results = []

    year_pattern = re.compile(r"\b(19|20)\d{2}\b")

    for i, line in enumerate(lines):

        degree = None

        for alias in DEGREE_ALIASES:
            if re.search(
                r"\b" + re.escape(alias) + r"\b",
                line,
                re.IGNORECASE
            ):
                degree = normalize_degree(alias)
                break

        if not degree:
            continue

        nearby = " ".join(
            lines[i:min(i + 4, len(lines))]
        )

        field = "Unspecified"

        for alias, canonical in FIELD_ALIASES.items():
            if alias in nearby.lower():
                field = canonical
                break

        institution = "Unknown Institution"

        for candidate in lines[i + 1:min(i + 4, len(lines))]:

            lower = candidate.lower()

            if any(
                word in lower
                for word in [
                    "university",
                    "college",
                    "institute",
                    "school"
                ]
            ):
                institution = candidate
                break

        year_match = year_pattern.search(nearby)

        graduation_year = (
            int(year_match.group(0))
            if year_match
            else None
        )

        results.append({
            "degree": degree,
            "field_of_study": field,
            "institution": institution,
            "graduation_year": graduation_year
        })

    return results


def extract_certifications(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    results = []

    certification_section = False

    for line in lines:

        lower = line.lower()

        if re.match(
            r"^(certifications?|certificates?)\s*:?\s*$",
            lower
        ):
            certification_section = True
            continue

        if certification_section and lower in {
            "education",
            "experience",
            "work experience",
            "skills",
            "projects"
        }:
            certification_section = False
            continue

        if certification_section:

            if any(
                keyword in lower
                for keyword in [
                    "certified",
                    "certificate",
                    "certification",
                    "aws",
                    "azure",
                    "pmp",
                    "scrum",
                    "security+",
                    "ceh",
                    "google",
                    "ibm"
                ]
            ):

                results.append({
                    "name": line,
                    "category": categorize_certification(
                        line
                    )
                })

    return results


def education_relevance(education, target_role):

    role = target_role.lower()

    relevant_fields = {
        "data analyst": {
            "computer science",
            "information technology",
            "data science",
            "data analytics",
            "statistics",
            "commerce",
            "business administration"
        },

        "software developer": {
            "computer science",
            "information technology",
            "electronics engineering"
        },

        "data scientist": {
            "computer science",
            "information technology",
            "data science",
            "data analytics",
            "statistics"
        },

        "business analyst": {
            "business administration",
            "commerce",
            "computer science",
            "information technology",
            "data analytics"
        }
    }

    fields = relevant_fields.get(
        role,
        set()
    )

    matched = []

    for record in education:

        field = record[
            "field_of_study"
        ].lower()

        if field in fields:
            matched.append(record)

    score = (
        len(matched) / len(education)
        if education
        else 0
    )

    return {
        "target_role": target_role,
        "score": round(score, 2),
        "matched_records": matched
    }
