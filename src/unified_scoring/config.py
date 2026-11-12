"""
Day 41 - Role-based unified scoring weights.

These are configurable initial weights for the project.
Each role's weights must total 100%.
"""

ROLE_WEIGHTS = {
    "data analyst": {
        "ats": 45,
        "screening": 25,
        "hr_interview": 30
    },

    "software developer": {
        "ats": 40,
        "screening": 25,
        "hr_interview": 35
    },

    "business analyst": {
        "ats": 35,
        "screening": 30,
        "hr_interview": 35
    },

    "hr executive": {
        "ats": 30,
        "screening": 35,
        "hr_interview": 35
    },

    "default": {
        "ats": 40,
        "screening": 30,
        "hr_interview": 30
    }
}
