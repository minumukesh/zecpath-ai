"""Configuration for the interview demonstration."""

ROLE_DOMAINS = {
    "mern": ["JavaScript", "React", "Node.js", "Express", "MongoDB", "REST APIs"],
    "java": ["Java", "OOP", "Spring Boot", "Hibernate", "SQL", "REST APIs"],
    "devops": ["Linux", "Git", "Docker", "CI/CD", "Kubernetes", "Cloud"],
}

EXPERIENCE_LEVELS = {
    "basic": (0, 2),
    "intermediate": (3, 5),
    "advanced": (5, None),
}

INTERVIEW_SECTIONS = ["introduction", "experience", "conceptual", "scenario"]

HR_SCORE_WEIGHTS = {
    "communication": 0.25,
    "role_understanding": 0.25,
    "problem_solving": 0.25,
    "professionalism": 0.25,
}