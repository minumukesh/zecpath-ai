from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import re


class ConversationState(str, Enum):
    GREETING = "GREETING"
    ASKING = "ASKING"
    WAITING_FOR_ANSWER = "WAITING_FOR_ANSWER"
    CLARIFYING = "CLARIFYING"
    FALLBACK = "FALLBACK"
    RETRYING = "RETRYING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class ConversationConfig:
    max_silence_retries: int = 2
    max_confusion_retries: int = 2
    max_repeated_answers: int = 1
    max_system_retries: int = 2

    def __post_init__(self):
        values = (
            self.max_silence_retries,
            self.max_confusion_retries,
            self.max_repeated_answers,
            self.max_system_retries,
        )

        if any(value < 0 for value in values):
            raise ValueError("Retry limits cannot be negative.")


@dataclass
class ConversationResult:
    state: str
    action: str
    message: str
    question_id: Optional[str] = None
    should_retry: bool = False
    follow_up_triggered: bool = False
    completed: bool = False
    metadata: dict = field(default_factory=dict)

    def to_dict(self):
        return {
            "state": self.state,
            "action": self.action,
            "message": self.message,
            "question_id": self.question_id,
            "should_retry": self.should_retry,
            "follow_up_triggered": self.follow_up_triggered,
            "completed": self.completed,
            "metadata": self.metadata,
        }


class ConversationEngine:
    CONFUSION_PHRASES = {
        "i don't understand",
        "i do not understand",
        "i am confused",
        "i'm confused",
        "can you explain",
        "what do you mean",
        "please repeat",
        "could you repeat",
        "not clear",
        "i don't know what you mean",
    }

    UNCERTAINTY_PHRASES = {
        "not sure",
        "i am not sure",
        "i'm not sure",
        "maybe",
        "i think",
        "probably",
        "i don't know",
        "i do not know",
    }

    def __init__(self, questions=None, config=None):
        self.config = config or ConversationConfig()

        # FIX 1:
        # An explicitly supplied empty list must not load default questions.
        if questions is None:
            self.questions = [
                {
                    "question_id": "Q1",
                    "category": "skills",
                    "question": "Could you tell me about your main skills?",
                    "fallback": (
                        "Which tools or skills have you used "
                        "in your work or studies?"
                    ),
                    "required": True,
                    "follow_up_if_uncertain": True,
                },
                {
                    "question_id": "Q2",
                    "category": "experience",
                    "question": "Could you describe your relevant experience?",
                    "fallback": (
                        "Have you completed any projects, internships, "
                        "or relevant work?"
                    ),
                    "required": True,
                    "follow_up_if_uncertain": True,
                },
                {
                    "question_id": "Q3",
                    "category": "availability",
                    "question": "When would you be available to join?",
                    "fallback": (
                        "Could you share your expected joining date "
                        "or notice period?"
                    ),
                    "required": True,
                    "follow_up_if_uncertain": True,
                },
            ]
        else:
            self.questions = questions

        self._validate_questions()

        self.state = ConversationState.GREETING
        self.question_index = 0

        self.silence_retries = 0
        self.confusion_retries = 0
        self.repeated_answer_count = 0
        self.system_retries = 0

        # Keep the previous answer when advancing to the next question.
        self.last_answer = None
        self.last_question_id = None
        self.current_question_text = None

        self.answers = []
        self.history = []
        self.follow_up_count = 0

    def _validate_questions(self):
        if not isinstance(self.questions, list) or not self.questions:
            raise ValueError("At least one question must be configured.")

        seen = set()

        for question in self.questions:
            if not isinstance(question, dict):
                raise ValueError("Each question must be a dictionary.")

            question_id = str(question.get("question_id", "")).strip()
            question_text = str(question.get("question", "")).strip()
            fallback = str(question.get("fallback", "")).strip()

            if not question_id or not question_text or not fallback:
                raise ValueError(
                    "Each question needs question_id, question and fallback."
                )

            if question_id in seen:
                raise ValueError(f"Duplicate question ID: {question_id}")

            seen.add(question_id)

    def _record(self, result):
        self.history.append(result.to_dict())
        return result

    def _result(
        self,
        action,
        message,
        question_id=None,
        should_retry=False,
        follow_up_triggered=False,
        completed=False,
        metadata=None,
    ):
        return self._record(
            ConversationResult(
                state=self.state.value,
                action=action,
                message=message,
                question_id=question_id,
                should_retry=should_retry,
                follow_up_triggered=follow_up_triggered,
                completed=completed,
                metadata=metadata or {},
            )
        )

    def _current_question(self):
        if self.question_index >= len(self.questions):
            return None

        return self.questions[self.question_index]

    def start(self):
        if self.state != ConversationState.GREETING:
            return self._result(
                "NO_ACTION",
                "The conversation has already started.",
                completed=self.state == ConversationState.COMPLETED,
            )

        self.state = ConversationState.ASKING

        return self._ask_current_question(
            "Hello! Thank you for joining. Let's begin the screening."
        )

    def _ask_current_question(self, prefix=None):
        question = self._current_question()

        if question is None:
            self.state = ConversationState.COMPLETED

            return self._result(
                "COMPLETE",
                "Thank you for your time. The screening questions are complete.",
                completed=True,
            )

        self.state = ConversationState.WAITING_FOR_ANSWER
        self.current_question_text = question["question"]
        self.last_question_id = question["question_id"]

        message = question["question"]

        if prefix:
            message = f"{prefix} {message}"

        return self._result(
            "ASK_QUESTION",
            message,
            question_id=question["question_id"],
            metadata={
                "category": question.get("category", "general"),
                "required": question.get("required", True),
            },
        )

    def _normalise_answer(self, answer):
        if answer is None:
            return ""

        return re.sub(r"\s+", " ", str(answer)).strip().casefold()

    def _is_confused(self, answer):
        text = self._normalise_answer(answer)
        return any(phrase in text for phrase in self.CONFUSION_PHRASES)

    def _is_uncertain(self, answer):
        text = self._normalise_answer(answer)
        return any(phrase in text for phrase in self.UNCERTAINTY_PHRASES)

    def _save_answer(self, answer, status):
        question = self._current_question()

        if question is None:
            return

        self.answers.append({
            "question_id": question["question_id"],
            "category": question.get("category", "general"),
            "question": question["question"],
            "answer": str(answer).strip() if answer is not None else "",
            "status": status,
        })

    def _advance(self):
        self.question_index += 1

        self.silence_retries = 0
        self.confusion_retries = 0
        self.repeated_answer_count = 0
        self.system_retries = 0

        # FIX 2:
        # Do not clear last_answer here. It is needed to detect
        # a repeated response after moving to the next question.

        if self.question_index >= len(self.questions):
            self.state = ConversationState.COMPLETED

            return self._result(
                "COMPLETE",
                "Thank you for your time. The screening questions are complete.",
                completed=True,
                metadata={"answers_recorded": len(self.answers)},
            )

        return self._ask_current_question(
            "Thank you. Let's move to the next question."
        )

    def handle_silence(self):
        if self.state in {
            ConversationState.COMPLETED,
            ConversationState.FAILED,
        }:
            return self._result(
                "NO_ACTION",
                "The conversation is not accepting further answers.",
                completed=self.state == ConversationState.COMPLETED,
            )

        question = self._current_question()

        if question is None:
            self.state = ConversationState.COMPLETED
            return self._result(
                "COMPLETE",
                "The screening is complete.",
                completed=True,
            )

        if self.silence_retries < self.config.max_silence_retries:
            self.silence_retries += 1
            self.state = ConversationState.RETRYING

            return self._result(
                "PROMPT_AFTER_SILENCE",
                "I couldn't hear a response. Please take your time "
                "and answer when you're ready.",
                question_id=question["question_id"],
                should_retry=True,
                metadata={
                    "retry": self.silence_retries,
                    "retry_limit": self.config.max_silence_retries,
                },
            )

        self.state = ConversationState.FALLBACK
        self._save_answer("", "missing")

        return self._result(
            "USE_FALLBACK",
            "That's okay. I'll ask the question in a different way. "
            + question["fallback"],
            question_id=question["question_id"],
            should_retry=True,
            follow_up_triggered=True,
            metadata={"reason": "silence_retry_limit_reached"},
        )

    def handle_confusion(self):
        question = self._current_question()

        if question is None:
            return self._advance()

        if self.confusion_retries < self.config.max_confusion_retries:
            self.confusion_retries += 1
            self.state = ConversationState.CLARIFYING

            return self._result(
                "CLARIFY_QUESTION",
                "No problem. Let me explain it more simply. "
                + question["fallback"],
                question_id=question["question_id"],
                should_retry=True,
                follow_up_triggered=True,
                metadata={
                    "retry": self.confusion_retries,
                    "retry_limit": self.config.max_confusion_retries,
                },
            )

        self._save_answer("", "unclear")

        return self._result(
            "SKIP_UNCLEAR_QUESTION",
            "No problem. We can move on and return to this if needed.",
            question_id=question["question_id"],
            follow_up_triggered=True,
            metadata={"reason": "confusion_retry_limit_reached"},
        )

    def handle_system_failure(self, error_message=None):
        if self.state in {
            ConversationState.COMPLETED,
            ConversationState.FAILED,
        }:
            return self._result(
                "NO_ACTION",
                "The conversation is not accepting further actions.",
                completed=self.state == ConversationState.COMPLETED,
            )

        if self.system_retries < self.config.max_system_retries:
            self.system_retries += 1
            self.state = ConversationState.RETRYING

            return self._result(
                "RETRY_SYSTEM",
                "Sorry, something went wrong. Please give me a moment "
                "to try again.",
                question_id=self.last_question_id,
                should_retry=True,
                metadata={
                    "retry": self.system_retries,
                    "retry_limit": self.config.max_system_retries,
                    "error": str(error_message or "unspecified error"),
                },
            )

        self.state = ConversationState.FAILED

        return self._result(
            "END_WITH_ERROR",
            "I'm sorry, but I can't continue this screening right now. "
            "The recruiter may need to arrange another attempt.",
            question_id=self.last_question_id,
            metadata={
                "reason": "system_retry_limit_reached",
                "error": str(error_message or "unspecified error"),
            },
        )

    def handle_answer(self, answer):
        if self.state in {
            ConversationState.COMPLETED,
            ConversationState.FAILED,
        }:
            return self._result(
                "NO_ACTION",
                "The conversation has ended. No further answer is required.",
                completed=self.state == ConversationState.COMPLETED,
            )

        question = self._current_question()

        if question is None:
            self.state = ConversationState.COMPLETED
            return self._result(
                "COMPLETE",
                "The screening is complete.",
                completed=True,
            )

        normalised = self._normalise_answer(answer)

        if not normalised:
            return self.handle_silence()

        if self._is_confused(normalised):
            return self.handle_confusion()

        # FIX 3:
        # Detect a repeated answer before treating it as a new answer
        # to the current question.
        # Detect repeated answers before processing them as new answers.
        if normalised == self.last_answer:
            self.repeated_answer_count += 1

            if (
                self.repeated_answer_count
                <= self.config.max_repeated_answers
            ):
                self.state = ConversationState.CLARIFYING

                return self._result(
                    "HANDLE_REPEATED_ANSWER",
                    "I received the same answer again. "
                    "Could you add a little more detail?",
                    question_id=question["question_id"],
                    should_retry=True,
                    follow_up_triggered=True,
                    metadata={
                        "repeat_count": self.repeated_answer_count,
                        "retry_limit": self.config.max_repeated_answers,
                    },
                )

            # Retry limit reached: record the response and continue.
            self._save_answer(str(answer).strip(), "repeated")
            return self._advance()

        # A genuinely new answer starts a new duplicate-check sequence.
        self.last_answer = normalised
        self.repeated_answer_count = 0

        uncertain = self._is_uncertain(normalised)
        too_short = len(normalised.split()) < 2

        if uncertain and question.get("follow_up_if_uncertain", True):
            self.follow_up_count += 1
            self.state = ConversationState.CLARIFYING

            return self._result(
                "FOLLOW_UP_UNCERTAIN_ANSWER",
                "Thank you for sharing that. Could you clarify "
                "your answer a little more?",
                question_id=question["question_id"],
                should_retry=True,
                follow_up_triggered=True,
                metadata={"reason": "uncertainty_detected"},
            )

        if too_short and question.get("required", True):
            self.follow_up_count += 1
            self.state = ConversationState.CLARIFYING

            return self._result(
                "FOLLOW_UP_SHORT_ANSWER",
                "Could you share a little more detail so I can "
                "record your answer accurately?",
                question_id=question["question_id"],
                should_retry=True,
                follow_up_triggered=True,
                metadata={"reason": "answer_may_be_incomplete"},
            )

        self._save_answer(str(answer).strip(), "provided")
        return self._advance()

    def _advance_after_repeated(self):
        """Advance after a repeated answer has reached its retry limit."""
        result = self._advance()
        return result.completed or result.action == "ASK_QUESTION"

    def skip_current_question(self, reason="candidate_skipped"):
        question = self._current_question()

        if question is None:
            self.state = ConversationState.COMPLETED
            return self._result(
                "COMPLETE",
                "The screening is complete.",
                completed=True,
            )

        self._save_answer("", "missing")
        result = self._advance()
        result.metadata["skip_reason"] = reason
        return result

    def get_report(self):
        return {
            "conversation_status": self.state.value,
            "total_questions": len(self.questions),
            "questions_processed": len(self.answers),
            "follow_up_count": self.follow_up_count,
            "answers": self.answers,
            "conversation_history": self.history,
        }


def run_sample_conversation():
    engine = ConversationEngine()
    results = [engine.start()]

    results.append(
        engine.handle_answer(
            "I have used Python, SQL and Excel in my projects."
        )
    )

    results.append(
        engine.handle_answer("I don't understand the question.")
    )

    results.append(
        engine.handle_answer(
            "I completed a data analytics project during my studies."
        )
    )

    results.append(
        engine.handle_answer(
            "I can join within thirty days after receiving the offer."
        )
    )

    return {
        "results": [result.to_dict() for result in results],
        "report": engine.get_report(),
    }
