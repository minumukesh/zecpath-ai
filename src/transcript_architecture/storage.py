from __future__ import annotations

import sqlite3
from pathlib import Path


SCREENING_SCHEMA = """
CREATE TABLE IF NOT EXISTS screening_interactions (

    interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,

    candidate_id TEXT NOT NULL,

    job_id TEXT NOT NULL,

    question_id TEXT NOT NULL,

    timestamp TEXT NOT NULL,

    confidence_level REAL NOT NULL,

    question_text TEXT NOT NULL,

    answer_text TEXT,

    answer_language TEXT DEFAULT 'en',

    interaction_status TEXT DEFAULT 'completed'
);


CREATE INDEX IF NOT EXISTS
idx_screening_candidate
ON screening_interactions(candidate_id);


CREATE INDEX IF NOT EXISTS
idx_screening_job
ON screening_interactions(job_id);


CREATE INDEX IF NOT EXISTS
idx_screening_question
ON screening_interactions(question_id);
"""


def create_screening_database(
    database_path: str | Path,
) -> Path:

    path = Path(
        database_path
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


    connection = sqlite3.connect(
        path
    )


    try:

        connection.executescript(
            SCREENING_SCHEMA
        )

        connection.commit()

    finally:

        connection.close()


    return path
