"""Day 56 simulation configuration."""

ATS_THRESHOLD = 60
SCREENING_THRESHOLD = 60
HR_THRESHOLD = 60
TECHNICAL_THRESHOLD = 60

FINAL_AI_THRESHOLD = 65

REQUIRED_SKILLS = {
    "data_analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "statistics"
    ],
    "software_developer": [
        "python",
        "java",
        "git",
        "api",
        "database"
    ]
}

WEIGHTS = {
    "ats": 0.25,
    "screening": 0.20,
    "hr": 0.20,
    "technical": 0.35
}
