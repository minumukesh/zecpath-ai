import json
import re
from pathlib import Path
from datetime import datetime, timezone


VAGUE_PHRASES = {
    "maybe",
    "i don't know",
    "i dont know",
    "not sure",
    "some things",
    "many things",
    "it was good",
    "nothing much",
    "no idea",
    "okay",
    "fine",
}

CLARIFICATION_PROMPTS = [
    "Could you explain what you mean in a little more detail?",
    "Could you clarify your answer so I can understand it better?",
]

DEEPENING_PROMPTS = [
    "What did you learn from that experience?",
    "What steps did you take, and what was the outcome?",
]

EXAMPLE_PROMPTS = [
    "Could you share a specific example?",
    "Can you describe a real situation where you demonstrated that?",
]

SCENARIO_PROMPTS = [
    "Imagine you faced a similar challenge in your next role. How would you handle it?",
    "What would you do differently if the same situation happened again?",
]


def normalize_answer(answer):
    """Normalize candidate text without changing its meaning."""
    if answer is None:
        return ""

    answer = str(answer).strip()
    answer = re.sub(r"\s+", " ", answer)
    return answer


def detect_answer_quality(answer):
    """
    Detect whether an answer is missing, vague, brief, or detailed.

    This is a transparent rule-based heuristic, not an assessment
    of a candidate's intelligence or professional ability.
    """
    normalized = normalize_answer(answer)
    lowered = normalized.lower().strip(" .!?,")

    if not normalized:
        return {
            "status": "INCOMPLETE",
            "reason": "No answer was provided.",
            "word_count": 0,
        }

    words = re.findall(r"\b[\w'-]+\b", normalized)
    word_count = len(words)

    if lowered in VAGUE_PHRASES:
        return {
            "status": "VAGUE",
            "reason": "The answer is a known vague phrase.",
            "word_count": word_count,
        }

    if word_count <= 2:
        return {
            "status": "TOO_BRIEF",
            "reason": "The answer contains very little information.",
            "word_count": word_count,
        }

    if word_count <= 7:
        return {
            "status": "BRIEF",
            "reason": "The answer may need more explanation.",
            "word_count": word_count,
        }

    return {
        "status": "DETAILED",
        "reason": "The answer contains more information to explore.",
        "word_count": word_count,
    }


def detect_confident_signal(answer):
    """
    Detect a possible signal that an answer contains an explanation.

    This does not measure actual confidence, truthfulness, or emotion.
    """
    normalized = normalize_answer(answer)
    words = re.findall(r"\b[\w'-]+\b", normalized)

    has_example_signal = bool(
        re.search(
            r"\b(for example|for instance|in my project|in my previous role|"
            r"one time|when i)\b",
            normalized,
            flags=re.IGNORECASE,
        )
    )

    has_reasoning_signal = bool(
        re.search(
            r"\b(because|therefore|as a result|which helped|"
            r"the outcome|i learned)\b",
            normalized,
            flags=re.IGNORECASE,
        )
    )

    signal = len(words) >= 12 and (
        has_example_signal or has_reasoning_signal
    )

    return {
        "detailed_answer_signal": signal,
        "example_signal": has_example_signal,
        "reasoning_signal": has_reasoning_signal,
    }


def choose_follow_up(answer, previous_questions=None):
    """
    Choose a follow-up based on answer quality.

    Avoids asking a question that has already been used in the same
    conversation. If every prompt has been used, it requests human review.
    """
    previous_questions = previous_questions or []
    previous_normalized = {
        normalize_answer(question).lower()
        for question in previous_questions
    }

    quality = detect_answer_quality(answer)
    detail_signal = detect_confident_signal(answer)

    if quality["status"] in {"INCOMPLETE", "VAGUE", "TOO_BRIEF"}:
        candidates = [
            ("CLARIFICATION", prompt)
            for prompt in CLARIFICATION_PROMPTS
        ]

        candidates.extend(
            ("EXAMPLE_REQUEST", prompt)
            for prompt in EXAMPLE_PROMPTS
        )

    elif quality["status"] == "BRIEF":
        candidates = [
            ("EXAMPLE_REQUEST", prompt)
            for prompt in EXAMPLE_PROMPTS
        ]

        candidates.extend(
            ("DEEPENING", prompt)
            for prompt in DEEPENING_PROMPTS
        )

    elif detail_signal["detailed_answer_signal"]:
        candidates = [
            ("SCENARIO_FOLLOW_UP", prompt)
            for prompt in SCENARIO_PROMPTS
        ]

        candidates.extend(
            ("DEEPENING", prompt)
            for prompt in DEEPENING_PROMPTS
        )

    else:
        candidates = [
            ("DEEPENING", prompt)
            for prompt in DEEPENING_PROMPTS
        ]

        candidates.extend(
            ("EXAMPLE_REQUEST", prompt)
            for prompt in EXAMPLE_PROMPTS
        )

    for trigger, question in candidates:
        if normalize_answer(question).lower() not in previous_normalized:
            return {
                "trigger": trigger,
                "follow_up_question": question,
                "answer_quality": quality,
                "detail_signals": detail_signal,
                "requires_follow_up": True,
                "human_review_recommended": False,
            }

    return {
        "trigger": "NO_UNUSED_PROMPT",
        "follow_up_question": None,
        "answer_quality": quality,
        "detail_signals": detail_signal,
        "requires_follow_up": False,
        "human_review_recommended": True,
    }


class FollowUpEngine:
    """Track interview state and adaptive follow-up questions."""

    def __init__(self, interview_id, candidate_id, role):
        if not normalize_answer(interview_id):
            raise ValueError("interview_id cannot be empty.")

        if not normalize_answer(candidate_id):
            raise ValueError("candidate_id cannot be empty.")

        if not normalize_answer(role):
            raise ValueError("role cannot be empty.")

        self.interview_id = normalize_answer(interview_id)
        self.candidate_id = normalize_answer(candidate_id)
        self.role = normalize_answer(role)

        self.state = "ACTIVE"
        self.turn_count = 0
        self.history = []
        self.used_follow_ups = []

    def process_answer(self, question_id, question, answer):
        """Process one response and update the interview state."""
        if self.state != "ACTIVE":
            raise ValueError("Cannot process answers for an inactive interview.")

        if not normalize_answer(question_id):
            raise ValueError("question_id cannot be empty.")

        if not normalize_answer(question):
            raise ValueError("question cannot be empty.")

        normalized_answer = normalize_answer(answer)

        decision = choose_follow_up(
            normalized_answer,
            self.used_follow_ups,
        )

        self.turn_count += 1

        if decision["follow_up_question"]:
            self.used_follow_ups.append(
                decision["follow_up_question"]
            )

        record = {
            "turn_id": self.turn_count,
            "question_id": normalize_answer(question_id),
            "question": normalize_answer(question),
            "answer": normalized_answer,
            "answer_quality": decision["answer_quality"],
            "trigger": decision["trigger"],
            "follow_up_question": decision["follow_up_question"],
            "requires_follow_up": decision["requires_follow_up"],
            "human_review_recommended": decision["human_review_recommended"],
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        }

        self.history.append(record)

        return record

    def close(self):
        """Close the conversation explicitly."""
        self.state = "COMPLETED"

    def get_state(self):
        return {
            "interview_id": self.interview_id,
            "candidate_id": self.candidate_id,
            "role": self.role,
            "state": self.state,
            "turn_count": self.turn_count,
            "used_follow_up_count": len(self.used_follow_ups),
            "history": self.history,
        }


def run_demo_cases(cases):
    """Run the follow-up engine against a sample dataset."""
    results = []

    for case in cases:
        engine = FollowUpEngine(
            interview_id=case["interview_id"],
            candidate_id=case["candidate_id"],
            role=case["role"],
        )

        result = engine.process_answer(
            question_id=case["question_id"],
            question=case["question"],
            answer=case.get("answer", ""),
        )

        results.append({
            "scenario": case["scenario"],
            "result": result,
            "conversation_state": engine.get_state(),
        })

    return {
        "project": "Zecpath AI",
        "day": 34,
        "title": "Dynamic Follow-Up Logic",
        "total_cases": len(results),
        "results": results,
        "limitations": [
            "Answer-quality detection uses simple text rules.",
            "A detailed answer is not proof of confidence or correctness.",
            "The engine does not judge candidate suitability.",
            "Human review is recommended when follow-up options are exhausted.",
        ],
    }


def save_report(report, output_dir):
    """Save the follow-up evaluation results as JSON and Markdown."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "day34_follow_up_report.json"
    markdown_path = output_dir / "day34_follow_up_report.md"

    json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = [
        "# Day 34 - Dynamic Follow-Up Logic",
        "",
        "## Objective",
        "",
        "Adapt follow-up questions based on candidate responses.",
        "",
        "## Workflow",
        "",
        "Candidate Answer",
        "→ Normalize Answer",
        "→ Detect Missing, Vague, Brief, or Detailed Response",
        "→ Select Clarification, Example, Deepening, or Scenario Question",
        "→ Avoid Repeated Follow-Up Questions",
        "→ Update Conversation State",
        "",
        "## Results",
        "",
        f"Total cases processed: {report['total_cases']}",
        "",
        "| Scenario | Answer Status | Trigger | Follow-Up |",
        "|---|---|---|---|",
    ]

    for item in report["results"]:
        result = item["result"]
        follow_up = result["follow_up_question"] or "Human review"
        follow_up = follow_up.replace("|", "\\|")
        lines.append(
            f"| {item['scenario']} "
            f"| {result['answer_quality']['status']} "
            f"| {result['trigger']} "
            f"| {follow_up} |"
        )

    lines.extend([
        "",
        "## Limitations",
        "",
        "- The engine uses rule-based answer-quality detection.",
        "- It does not measure actual confidence, truthfulness, or emotion.",
        "- It does not make hiring decisions.",
        "- Human review is recommended when no unused prompt remains.",
        "",
    ])

    markdown_path.write_text("\n".join(lines), encoding="utf-8")

    return json_path, markdown_path
