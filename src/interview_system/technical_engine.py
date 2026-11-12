"""Role mapping, question hierarchy and technical interview flow."""

from dataclasses import dataclass, field
from .config import ROLE_DOMAINS, INTERVIEW_SECTIONS

ROLE_ALIASES = {
    "mern developer": "mern",
    "mern stack developer": "mern",
    "full stack developer": "mern",
    "java developer": "java",
    "devops engineer": "devops",
}

QUESTION_BANK = {
    "mern": {
        "basic": {
            "conceptual": [
                "What is JavaScript?",
                "What is the difference between let and const?",
                "What is React?"
            ],
            "scenario": [
                "How would you display a list of users in a React application?"
            ]
        },
        "intermediate": {
            "conceptual": [
                "Explain React hooks.",
                "What is middleware in Express?",
                "How does MongoDB store documents?"
            ],
            "scenario": [
                "How would you implement authentication in a MERN application?"
            ]
        },
        "advanced": {
            "conceptual": [
                "Explain frontend performance optimization.",
                "How would you design a scalable Node.js backend?"
            ],
            "scenario": [
                "Design a scalable MERN application for a large number of users."
            ]
        }
    },
    "java": {
        "basic": {
            "conceptual": [
                "What is Java?",
                "Explain object-oriented programming.",
                "What is the difference between JDK and JRE?"
            ],
            "scenario": [
                "How would you create a Java class for employee details?"
            ]
        },
        "intermediate": {
            "conceptual": [
                "Explain exception handling in Java.",
                "What is dependency injection?",
                "Explain Spring Boot."
            ],
            "scenario": [
                "How would you develop a REST API using Spring Boot?"
            ]
        },
        "advanced": {
            "conceptual": [
                "Explain Java multithreading.",
                "How would you optimize a high-volume Java application?"
            ],
            "scenario": [
                "Design a distributed Java application for a banking platform."
            ]
        }
    },
    "devops": {
        "basic": {
            "conceptual": [
                "What is Linux?",
                "What is Git?",
                "What is cloud computing?"
            ],
            "scenario": [
                "How would you deploy a basic application to a server?"
            ]
        },
        "intermediate": {
            "conceptual": [
                "What is Docker?",
                "Explain CI/CD.",
                "What is container orchestration?"
            ],
            "scenario": [
                "How would you create a CI/CD pipeline for an application?"
            ]
        },
        "advanced": {
            "conceptual": [
                "Explain Kubernetes architecture.",
                "How would you monitor distributed infrastructure?"
            ],
            "scenario": [
                "Design a highly available cloud deployment architecture."
            ]
        }
    }
}

@dataclass
class InterviewSession:
    candidate_id: str
    role: str
    experience_years: float
    state: str = "created"
    answers: list = field(default_factory=list)

class TechnicalInterviewEngine:
    TRANSITIONS = {
        "created": ["introduction", "cancelled"],
        "introduction": ["experience", "cancelled"],
        "experience": ["conceptual", "cancelled"],
        "conceptual": ["scenario", "cancelled"],
        "scenario": ["completed", "cancelled"],
        "completed": [],
        "cancelled": []
    }

    def normalize_role(self, role):
        if not isinstance(role, str) or not role.strip():
            raise ValueError("Role is required.")
        key = role.strip().lower()
        key = ROLE_ALIASES.get(key, key)
        if key not in ROLE_DOMAINS:
            raise ValueError(
                f"Unsupported role '{role}'. Supported roles: {', '.join(ROLE_DOMAINS)}"
            )
        return key

    def get_experience_level(self, years):
        years = float(years)
        if years < 0:
            raise ValueError("Experience cannot be negative.")
        if years <= 2:
            return "basic"
        if years < 5:
            return "intermediate"
        return "advanced"

    def get_skill_domains(self, role):
        return ROLE_DOMAINS[self.normalize_role(role)].copy()

    def generate_questions(self, role, experience_years):
        role = self.normalize_role(role)
        level = self.get_experience_level(experience_years)
        bank = QUESTION_BANK[role][level]
        return {
            "role": role,
            "experience_years": float(experience_years),
            "experience_level": level,
            "introduction": [
                "Please introduce yourself.",
                "Briefly explain your technical background."
            ],
            "experience": [
                "Describe a project you have worked on.",
                "What was your contribution to that project?"
            ],
            "conceptual": bank["conceptual"].copy(),
            "scenario": bank["scenario"].copy()
        }

    def get_interview_blueprint(self, role, experience_years):
        questions = self.generate_questions(role, experience_years)
        return {
            "role": questions["role"],
            "experience_years": questions["experience_years"],
            "experience_level": questions["experience_level"],
            "skill_domains": self.get_skill_domains(role),
            "sections": questions,
            "difficulty_progression": ["basic", "intermediate", "advanced"],
            "interview_structure": INTERVIEW_SECTIONS.copy()
        }

    def create_session(self, candidate_id, role, experience_years):
        if not isinstance(candidate_id, str) or not candidate_id.strip():
            raise ValueError("Candidate ID is required.")
        normalized_role = self.normalize_role(role)
        self.get_experience_level(experience_years)
        return InterviewSession(
            candidate_id=candidate_id.strip(),
            role=normalized_role,
            experience_years=float(experience_years)
        )

    def transition(self, session, next_state):
        allowed = self.TRANSITIONS.get(session.state, [])
        if next_state not in allowed:
            raise ValueError(f"Invalid transition: {session.state} -> {next_state}")
        previous_state = session.state
        session.state = next_state
        return {
            "candidate_id": session.candidate_id,
            "previous_state": previous_state,
            "current_state": session.state,
            "status": "success"
        }

    def submit_answer(self, session, question, answer):
        if session.state in ("created", "completed", "cancelled"):
            raise ValueError("Answers can only be submitted during an active interview section.")
        if not isinstance(question, str) or not question.strip():
            raise ValueError("Question cannot be empty.")
        if not isinstance(answer, str) or not answer.strip():
            raise ValueError("Answer cannot be empty.")
        session.answers.append({
            "section": session.state,
            "question": question.strip(),
            "answer": answer.strip()
        })
        return {"status": "answer_recorded", "total_answers": len(session.answers)}