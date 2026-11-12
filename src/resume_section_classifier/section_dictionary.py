SECTION_ALIASES = {
    "skills": [
        "skills",
        "technical skills",
        "technical skill",
        "core skills",
        "key skills",
        "professional skills",
        "skills and competencies",
        "skills & competencies",
        "technical competencies",
        "core competencies",
        "competencies",
        "areas of expertise",
        "expertise",
        "technologies",
        "technical knowledge",
    ],

    "work_experience": [
        "work experience",
        "professional experience",
        "employment history",
        "career history",
        "work history",
        "experience",
        "professional background",
        "employment",
    ],

    "education": [
        "education",
        "educational qualification",
        "educational qualifications",
        "academic qualification",
        "academic qualifications",
        "academic background",
        "education background",
        "academic history",
    ],

    "certifications": [
        "certifications",
        "certification",
        "certificates",
        "professional certifications",
        "professional certification",
        "licenses and certifications",
        "licenses & certifications",
    ],

    "projects": [
        "projects",
        "project",
        "academic projects",
        "personal projects",
        "key projects",
        "major projects",
        "project experience",
    ],
}


CANONICAL_SECTIONS = list(SECTION_ALIASES.keys())


def build_alias_lookup():
    lookup = {}

    for section, aliases in SECTION_ALIASES.items():
        for alias in aliases:
            lookup[alias.lower()] = section

    return lookup


SECTION_ALIAS_LOOKUP = build_alias_lookup()