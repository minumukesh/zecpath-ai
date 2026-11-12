from pathlib import Path
from datetime import datetime, timezone
import json


INTERVIEW_CATEGORIES = [
    "self_introduction",
    "career_journey",
    "strengths_weaknesses",
    "teamwork_culture_fit",
    "career_goals",
    "availability_commitment",
]

CONVERSATION_PHASES = [
    "INTRODUCTION",
    "CORE_HR_QUESTIONS",
    "ROLE_BASED_EVALUATION",
    "CLOSING",
]

VALID_EXPERIENCE_LEVELS = {"fresher", "experienced"}
VALID_ROLE_TYPES = {"technical", "non_technical"}


QUESTION_BANK = {
    "self_introduction": {
        "fresher": {
            "technical": [
                "Could you introduce yourself and describe your technical interests?",
                "Which academic or personal project are you most proud of?",
            ],
            "non_technical": [
                "Could you introduce yourself and describe your educational background?",
                "What skills have you developed through your studies or activities?",
            ],
        },
        "experienced": {
            "technical": [
                "Could you introduce yourself and summarize your technical experience?",
                "Which technical project best demonstrates your abilities?",
            ],
            "non_technical": [
                "Could you introduce yourself and summarize your professional experience?",
                "Which professional achievement are you most proud of?",
            ],
        },
    },
    "career_journey": {
        "fresher": {
            "technical": [
                "What led you to choose your technical field?",
                "Which project or course helped you learn the most?",
            ],
            "non_technical": [
                "What led you to choose your area of study?",
                "Which academic or extracurricular experience helped you grow?",
            ],
        },
        "experienced": {
            "technical": [
                "How has your technical career developed so far?",
                "How have your responsibilities changed over time?",
            ],
            "non_technical": [
                "How has your professional career developed so far?",
                "Which work experience influenced your career direction?",
            ],
        },
    },
    "strengths_weaknesses": {
        "fresher": {
            "technical": [
                "What technical skill do you consider your strongest?",
                "Which skill are you currently working to improve?",
            ],
            "non_technical": [
                "What personal strength helps you work effectively?",
                "What skill would you like to improve?",
            ],
        },
        "experienced": {
            "technical": [
                "Which technical strength helps you solve difficult problems?",
                "Describe a technical area you are working to improve.",
            ],
            "non_technical": [
                "Which professional strength contributes most to your work?",
                "What professional skill are you currently developing?",
            ],
        },
    },
    "teamwork_culture_fit": {
        "fresher": {
            "technical": [
                "How did you contribute when working on a group project?",
                "How would you handle a disagreement with a teammate?",
            ],
            "non_technical": [
                "How do you contribute to a team?",
                "How would you handle a disagreement during a group activity?",
            ],
        },
        "experienced": {
            "technical": [
                "How do you collaborate with developers or other technical teams?",
                "Describe how you handled a technical disagreement.",
            ],
            "non_technical": [
                "How do you collaborate with colleagues from different teams?",
                "Describe how you handled a workplace disagreement.",
            ],
        },
    },
    "career_goals": {
        "fresher": {
            "technical": [
                "What technical skills would you like to develop in the next few years?",
                "What kind of technical work would you like to do in the future?",
            ],
            "non_technical": [
                "What would you like to achieve in your career over the next few years?",
                "Which professional skills would you like to develop?",
            ],
        },
        "experienced": {
            "technical": [
                "What are your next technical career goals?",
                "Which responsibilities would you like to take on in the future?",
            ],
            "non_technical": [
                "What are your next professional career goals?",
                "How would you like your role to develop over time?",
            ],
        },
    },
    "availability_commitment": {
        "fresher": {
            "technical": [
                "When would you be available to start?",
                "Are there any academic commitments that affect your availability?",
            ],
            "non_technical": [
                "When would you be available to start?",
                "What working arrangement and schedule can you commit to?",
            ],
        },
        "experienced": {
            "technical": [
                "What is your expected joining date or notice period?",
                "What working arrangement can you commit to?",
            ],
            "non_technical": [
                "What is your expected joining date or notice period?",
                "What working arrangement and schedule can you commit to?",
            ],
        },
    },
}


FOLLOW_UP_QUESTIONS = {
    "self_introduction": "Could you tell me a little more about that?",
    "career_journey": "Could you explain what you learned from that experience?",
    "strengths_weaknesses": "Could you share a practical example?",
    "teamwork_culture_fit": "What did you do, and what was the outcome?",
    "career_goals": "What steps would you take to reach that goal?",
    "availability_commitment": "Could you clarify your expected timeline?",
}


def validate_profile(experience_level, role_type):
    experience_level = str(experience_level).strip().lower()
    role_type = str(role_type).strip().lower()

    if experience_level not in VALID_EXPERIENCE_LEVELS:
        raise ValueError(
            "experience_level must be 'fresher' or 'experienced'."
        )

    if role_type not in VALID_ROLE_TYPES:
        raise ValueError(
            "role_type must be 'technical' or 'non_technical'."
        )

    return experience_level, role_type


def generate_question_bank(experience_level, role_type):
    """Generate HR interview questions for the candidate profile."""
    experience_level, role_type = validate_profile(
        experience_level, role_type
    )

    questions = []
    question_number = 1

    for category in INTERVIEW_CATEGORIES:
        category_questions = QUESTION_BANK[category][experience_level][role_type]

        for question_text in category_questions:
            questions.append({
                "question_id": f"HR-{question_number:03d}",
                "category": category,
                "experience_level": experience_level,
                "role_type": role_type,
                "question_text": question_text,
                "expected_answer_type": "open_ended",
                "mandatory": True,
                "follow_up_eligible": True,
            })
            question_number += 1

    return questions


def create_interview_state(candidate_id, role, experience_level, role_type):
    """Create a structured state for one interview."""
    if not str(candidate_id).strip():
        raise ValueError("candidate_id cannot be empty.")

    if not str(role).strip():
        raise ValueError("role cannot be empty.")

    experience_level, role_type = validate_profile(
        experience_level, role_type
    )

    questions = generate_question_bank(experience_level, role_type)

    return {
        "interview_id": f"INT-{str(candidate_id).strip()}",
        "candidate_id": str(candidate_id).strip(),
        "role": str(role).strip(),
        "experience_level": experience_level,
        "role_type": role_type,
        "current_phase": CONVERSATION_PHASES[0],
        "current_question_index": 0,
        "questions": questions,
        "responses": [],
        "status": "READY",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def get_current_question(interview_state):
    """Return the current question, or None if the interview is complete."""
    if interview_state["status"] == "COMPLETED":
        return None

    index = interview_state["current_question_index"]
    questions = interview_state["questions"]

    if index >= len(questions):
        return None

    return questions[index]


def capture_response(interview_state, response_text):
    """Save the candidate response against its question ID."""
    if interview_state["status"] == "COMPLETED":
        raise ValueError("Cannot capture a response for a completed interview.")

    question = get_current_question(interview_state)

    if question is None:
        interview_state["status"] = "COMPLETED"
        return None

    response_text = "" if response_text is None else str(response_text).strip()

    response_record = {
        "question_id": question["question_id"],
        "category": question["category"],
        "response_text": response_text,
        "response_status": "ANSWERED" if response_text else "MISSING",
        "follow_up_eligible": bool(
            question["follow_up_eligible"] and not response_text
        ),
        "follow_up_question": (
            FOLLOW_UP_QUESTIONS[question["category"]]
            if not response_text
            else None
        ),
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
    }

    interview_state["responses"].append(response_record)
    interview_state["current_question_index"] += 1

    if interview_state["current_question_index"] >= len(
        interview_state["questions"]
    ):
        interview_state["current_phase"] = "CLOSING"
        interview_state["status"] = "COMPLETED"
    elif interview_state["current_question_index"] < 2:
        interview_state["current_phase"] = "INTRODUCTION"
        interview_state["status"] = "IN_PROGRESS"
    elif interview_state["current_question_index"] < 8:
        interview_state["current_phase"] = "CORE_HR_QUESTIONS"
        interview_state["status"] = "IN_PROGRESS"
    else:
        interview_state["current_phase"] = "ROLE_BASED_EVALUATION"
        interview_state["status"] = "IN_PROGRESS"

    return response_record


def build_interview_summary(interview_state):
    """Summarize interview progress without making a hiring decision."""
    responses = interview_state["responses"]

    answered_count = sum(
        1 for response in responses
        if response["response_status"] == "ANSWERED"
    )

    missing_count = sum(
        1 for response in responses
        if response["response_status"] == "MISSING"
    )

    return {
        "interview_id": interview_state["interview_id"],
        "candidate_id": interview_state["candidate_id"],
        "role": interview_state["role"],
        "experience_level": interview_state["experience_level"],
        "role_type": interview_state["role_type"],
        "status": interview_state["status"],
        "current_phase": interview_state["current_phase"],
        "total_questions": len(interview_state["questions"]),
        "responses_captured": len(responses),
        "answered_count": answered_count,
        "missing_count": missing_count,
        "completion_percentage": round(
            len(responses) / len(interview_state["questions"]) * 100,
            2,
        ) if interview_state["questions"] else 0.0,
        "responses": responses,
        "note": (
            "This summary records interview progress. It does not score "
            "answers or make a hiring decision."
        ),
    }


def save_interview_report(interview_state, output_dir):
    """Save the interview state and summary as JSON."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = build_interview_summary(interview_state)

    path = output_dir / (
        f"{interview_state['interview_id']}_interview_report.json"
    )

    path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return path
