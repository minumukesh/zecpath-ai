ROLE_ALIASES = {
    "data analyst": [
        "data analyst",
        "data analytics analyst",
        "data analyst intern",
        "junior data analyst",
        "reporting analyst"
    ],
    "business analyst": [
        "business analyst",
        "business systems analyst",
        "junior business analyst"
    ],
    "data scientist": [
        "data scientist",
        "junior data scientist",
        "data science intern"
    ],
    "software developer": [
        "software developer",
        "software engineer",
        "application developer",
        "full stack developer",
        "backend developer",
        "frontend developer"
    ],
    "data engineer": [
        "data engineer",
        "etl developer",
        "big data engineer"
    ],
    "project manager": [
        "project manager",
        "program manager",
        "project coordinator"
    ],
    "machine learning engineer": [
        "machine learning engineer",
        "ml engineer",
        "ai engineer"
    ]
}


ROLE_SKILLS = {
    "data analyst": {
        "python",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "data analysis",
        "statistics"
    },
    "business analyst": {
        "sql",
        "excel",
        "power bi",
        "business analysis",
        "requirements analysis",
        "communication"
    },
    "data scientist": {
        "python",
        "sql",
        "machine learning",
        "statistics",
        "pandas",
        "numpy",
        "scikit-learn"
    },
    "software developer": {
        "python",
        "java",
        "javascript",
        "react",
        "node.js",
        "sql",
        "git",
        "docker"
    },
    "data engineer": {
        "python",
        "sql",
        "etl",
        "spark",
        "hadoop",
        "airflow",
        "aws"
    },
    "project manager": {
        "project management",
        "communication",
        "leadership",
        "teamwork",
        "planning"
    },
    "machine learning engineer": {
        "python",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "scikit-learn",
        "docker"
    }
}


def normalize_role(title):
    title = title.lower().strip()

    for canonical, aliases in ROLE_ALIASES.items():
        if title == canonical:
            return canonical

        if title in aliases:
            return canonical

    return title
