from pathlib import Path
import json

from src.transcript_architecture.schemas import (
    build_transcript,
    build_screening_interaction,
    validate_transcript,
    current_timestamp,
)

from src.transcript_architecture.normalizer import (
    normalize_transcript_text,
)

from src.transcript_architecture.storage import (
    create_screening_database,
)

from src.transcript_architecture.metadata import (
    METADATA_STANDARDS,
)


ROOT = Path(
    __file__
).resolve().parent


DATA_DIR = (
    ROOT
    / "data"
    / "day23_transcript"
)


OUTPUT_DIR = (
    ROOT
    / "outputs"
    / "day23"
)


def write_json(
    path: Path,
    data: dict,
) -> None:

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def main():

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


    # ========================================================
    # SAMPLE TRANSCRIPT
    # ========================================================

    raw_text = (
        "  I have two years of experience "
        "in data analysis... "
        "\nI mainly work with Python, SQL "
        "and Power BI!!  "
    )


    normalized_text = (
        normalize_transcript_text(
            raw_text
        )
    )


    timestamp = current_timestamp()


    transcript = build_transcript(

        candidate_id="CAND001",

        job_id="JOB_DA_001",

        question_id="HRQ003",

        speaker="candidate",

        text=normalized_text,

        timestamp=timestamp,

        confidence=0.94,

        sequence=1,
    )


    validation_errors = (
        validate_transcript(
            transcript
        )
    )


    if validation_errors:

        print(
            "Transcript validation FAILED"
        )

        for error in validation_errors:

            print(
                f"  - {error}"
            )

        raise SystemExit(1)


    # ========================================================
    # SCREENING INTERACTION
    # ========================================================

    interaction = (
        build_screening_interaction(

            candidate_id="CAND001",

            job_id="JOB_DA_001",

            question_id="HRQ003",

            question_text=(
                "How many years of relevant "
                "experience do you have for "
                "the Data Analyst role?"
            ),

            answer_text=normalized_text,

            timestamp=timestamp,

            confidence=0.94,
        )
    )


    # ========================================================
    # VOICE TRANSCRIPT SCHEMA
    # ========================================================

    voice_schema = {

        "schema_name":
            "zecpath_voice_transcript",

        "version":
            "1.0",

        "description":
            "Structured representation of a voice screening transcript segment.",

        "required_fields": [

            "candidate_id",

            "job_id",

            "question_id",

            "timestamp",

            "confidence_level",

            "speaker",

            "sequence",

            "text",

            "language",
        ],

        "fields": {

            "candidate_id":
                "string",

            "job_id":
                "string",

            "question_id":
                "string",

            "timestamp":
                "ISO-8601 datetime",

            "confidence_level":
                "float 0.0-1.0",

            "speaker":
                "candidate | interviewer | system",

            "sequence":
                "positive integer",

            "text":
                "string",

            "language":
                "string",
        },
    }


    # ========================================================
    # AI SCREENING DATA SCHEMA
    # ========================================================

    ai_screening_schema = {

        "schema_name":
            "zecpath_ai_screening_interaction",

        "version":
            "1.0",

        "description":
            "Structured question-answer object for AI screening.",

        "fields": {

            "candidate_id":
                "string",

            "job_id":
                "string",

            "question_id":
                "string",

            "timestamp":
                "ISO-8601 datetime",

            "confidence_level":
                "float 0.0-1.0",

            "question": {

                "question_id":
                    "string",

                "text":
                    "string",
            },

            "answer": {

                "text":
                    "string",

                "language":
                    "string",
            },

            "interaction_status":
                "completed | incomplete",
        },
    }


    # ========================================================
    # NORMALIZATION RULES
    # ========================================================

    normalization_rules = {

        "rules": [

            "Normalize CRLF and CR line breaks to spaces.",

            "Replace line breaks with single spaces.",

            "Collapse repeated whitespace.",

            "Collapse repeated punctuation.",

            "Remove spaces before punctuation.",

            "Normalize spacing after punctuation.",

            "Trim leading and trailing whitespace.",
        ]
    }


    # ========================================================
    # SAVE JSON FILES
    # ========================================================

    write_json(

        DATA_DIR
        / "voice_transcript_schema.json",

        voice_schema,
    )


    write_json(

        DATA_DIR
        / "ai_screening_data_schema.json",

        ai_screening_schema,
    )


    write_json(

        DATA_DIR
        / "metadata_standards.json",

        METADATA_STANDARDS,
    )


    write_json(

        DATA_DIR
        / "normalization_rules.json",

        normalization_rules,
    )


    write_json(

        DATA_DIR
        / "sample_transcript.json",

        {

            "transcript":
                transcript,

            "screening_interaction":
                interaction,
        },
    )


    # ========================================================
    # DATABASE
    # ========================================================

    database_path = (

        DATA_DIR
        / "screening_interactions.db"
    )


    create_screening_database(
        database_path
    )


    # ========================================================
    # FINAL REPORT
    # ========================================================

    report = {

        "day": 23,

        "title":
            "Transcript Data Architecture",

        "status":
            "COMPLETED",

        "voice_transcript_schema":
            "IMPLEMENTED",

        "ai_screening_data_schema":
            "IMPLEMENTED",

        "metadata_standards":
            "IMPLEMENTED",

        "transcript_normalization":
            "IMPLEMENTED",

        "database_schema":
            "IMPLEMENTED",

        "sample_validation":
            "PASSED",

        "metadata_fields":
            list(
                METADATA_STANDARDS.keys()
            ),

        "deliverables": [

            "voice_transcript_schema.json",

            "ai_screening_data_schema.json",

            "metadata_standards.json",

            "normalization_rules.json",

            "sample_transcript.json",

            "screening_interactions.db",
        ],
    }


    report_path = (

        OUTPUT_DIR
        / "day23_transcript_architecture_report.json"
    )


    write_json(
        report_path,
        report,
    )


    # ========================================================
    # TERMINAL RESULT
    # ========================================================

    print()
    print("=" * 72)
    print(
        "DAY 23 - TRANSCRIPT DATA ARCHITECTURE"
    )
    print("=" * 72)

    print(
        "Voice Transcript Schema : IMPLEMENTED"
    )

    print(
        "AI Screening Schema     : IMPLEMENTED"
    )

    print(
        "Metadata Standards      : IMPLEMENTED"
    )

    print(
        "Normalization Rules     : IMPLEMENTED"
    )

    print(
        "Database Schema         : IMPLEMENTED"
    )

    print(
        "Sample Validation       : PASSED"
    )

    print()

    print(
        "Metadata Fields:"
    )

    for field in METADATA_STANDARDS:

        print(
            f"  - {field}"
        )

    print()

    print(
        "Normalized Transcript:"
    )

    print(
        f"  {normalized_text}"
    )

    print()

    print(
        "Database:"
    )

    print(
        f"  {database_path}"
    )

    print()

    print(
        "Deliverables:"
    )

    for item in report["deliverables"]:

        print(
            f"  - {item}"
        )

    print()

    print(
        "Report:"
    )

    print(
        f"  {report_path}"
    )

    print("=" * 72)


if __name__ == "__main__":

    main()
