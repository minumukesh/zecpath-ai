import sqlite3

from src.transcript_architecture.schemas import (
    build_transcript,
    build_screening_interaction,
    validate_transcript,
)

from src.transcript_architecture.normalizer import (
    normalize_transcript_text,
)

from src.transcript_architecture.storage import (
    create_screening_database,
)


class TestTranscriptArchitecture:


    def test_transcript_schema(self):

        transcript = build_transcript(

            candidate_id="C001",

            job_id="J001",

            question_id="Q001",

            speaker="candidate",

            text="I have two years experience.",

            timestamp=(
                "2026-10-06T10:00:00+00:00"
            ),

            confidence=0.95,

            sequence=1,
        )


        assert (
            transcript["candidate_id"]
            == "C001"
        )

        assert (
            transcript["job_id"]
            == "J001"
        )

        assert (
            transcript["question_id"]
            == "Q001"
        )

        assert (
            transcript["confidence_level"]
            == 0.95
        )

        assert (
            transcript["speaker"]
            == "candidate"
        )


    def test_metadata_validation(self):

        transcript = build_transcript(

            candidate_id="C001",

            job_id="J001",

            question_id="Q001",

            speaker="candidate",

            text="Python and SQL.",

            timestamp=(
                "2026-10-06T10:00:00+00:00"
            ),

            confidence=0.90,

            sequence=1,
        )


        assert (
            validate_transcript(
                transcript
            )
            == []
        )


    def test_invalid_confidence_rejected(self):

        transcript = build_transcript(

            candidate_id="C001",

            job_id="J001",

            question_id="Q001",

            speaker="candidate",

            text="Answer",

            timestamp=(
                "2026-10-06T10:00:00+00:00"
            ),

            confidence=1.5,

            sequence=1,
        )


        errors = validate_transcript(
            transcript
        )


        assert (
            "confidence_level must be between 0 and 1."
            in errors
        )


    def test_transcript_normalization(self):

        text = (
            "  I have Python...   SQL  "
            "\n\n Power BI !!  "
        )


        normalized = (
            normalize_transcript_text(
                text
            )
        )


        assert normalized == (
            "I have Python. SQL Power BI!"
        )


    def test_screening_interaction_schema(self):

        interaction = (
            build_screening_interaction(

                candidate_id="C001",

                job_id="J001",

                question_id="Q001",

                question_text=(
                    "Tell me about yourself."
                ),

                answer_text=(
                    "I am a computer science graduate."
                ),

                timestamp=(
                    "2026-10-06T10:00:00+00:00"
                ),

                confidence=0.92,
            )
        )


        assert (
            interaction["candidate_id"]
            == "C001"
        )

        assert (
            interaction["job_id"]
            == "J001"
        )

        assert (
            interaction["question"]
            ["question_id"]
            == "Q001"
        )

        assert (
            interaction["answer"]
            ["text"]
            == "I am a computer science graduate."
        )

        assert (
            interaction["interaction_status"]
            == "completed"
        )


    def test_database_schema(
        self,
        tmp_path,
    ):

        database = (
            tmp_path
            / "screening.db"
        )


        create_screening_database(
            database
        )


        connection = sqlite3.connect(
            database
        )


        cursor = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'screening_interactions'
            """
        )


        result = cursor.fetchone()


        connection.close()


        assert result is not None


        assert (
            result[0]
            == "screening_interactions"
        )
