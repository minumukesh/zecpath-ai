from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


VALID_SPEAKERS = {
    "candidate",
    "interviewer",
    "system",
}


def build_transcript(
    candidate_id: str,
    job_id: str,
    question_id: str,
    speaker: str,
    text: str,
    timestamp: str,
    confidence: float,
    sequence: int,
) -> dict[str, Any]:

    return {
        "candidate_id": str(candidate_id),
        "job_id": str(job_id),
        "question_id": str(question_id),
        "timestamp": str(timestamp),
        "confidence_level": round(
            float(confidence),
            4,
        ),
        "speaker": str(speaker),
        "sequence": int(sequence),
        "text": str(text),
        "language": "en",
    }


def build_screening_interaction(
    candidate_id: str,
    job_id: str,
    question_id: str,
    question_text: str,
    answer_text: str,
    timestamp: str,
    confidence: float,
) -> dict[str, Any]:

    return {
        "candidate_id": str(candidate_id),
        "job_id": str(job_id),
        "question_id": str(question_id),
        "timestamp": str(timestamp),
        "confidence_level": round(
            float(confidence),
            4,
        ),
        "question": {
            "question_id": str(question_id),
            "text": str(question_text),
        },
        "answer": {
            "text": str(answer_text),
            "language": "en",
        },
        "interaction_status": "completed",
    }


def validate_transcript(
    transcript: dict[str, Any],
) -> list[str]:

    errors = []

    required_fields = [
        "candidate_id",
        "job_id",
        "question_id",
        "timestamp",
        "confidence_level",
        "speaker",
        "sequence",
        "text",
        "language",
    ]

    for field in required_fields:

        if field not in transcript:

            errors.append(
                f"Missing required field: {field}"
            )


    if not transcript.get("candidate_id"):

        errors.append(
            "candidate_id cannot be empty."
        )


    if not transcript.get("job_id"):

        errors.append(
            "job_id cannot be empty."
        )


    if not transcript.get("question_id"):

        errors.append(
            "question_id cannot be empty."
        )


    confidence = transcript.get(
        "confidence_level"
    )

    if (
        not isinstance(
            confidence,
            (int, float),
        )
        or not 0.0 <= confidence <= 1.0
    ):

        errors.append(
            "confidence_level must be between 0 and 1."
        )


    if transcript.get("speaker") not in VALID_SPEAKERS:

        errors.append(
            "speaker must be candidate, interviewer, or system."
        )


    if (
        not isinstance(
            transcript.get("sequence"),
            int,
        )
        or transcript.get("sequence") < 1
    ):

        errors.append(
            "sequence must be a positive integer."
        )


    if not isinstance(
        transcript.get("text"),
        str,
    ):

        errors.append(
            "text must be a string."
        )


    if not isinstance(
        transcript.get("language"),
        str,
    ):

        errors.append(
            "language must be a string."
        )


    return errors


def current_timestamp() -> str:

    return datetime.now(
        timezone.utc
    ).isoformat()
