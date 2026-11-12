from src.answer_understanding import (
    classify_intent,
    extract_answer_details,
    understand_answer,
)


def test_skills_intent():

    assert classify_intent(
        "I know Python, SQL and Power BI."
    ) == "SKILLS"


def test_experience_extraction():

    result = extract_answer_details(
        "I have 3 years of experience in data analysis."
    )

    assert result["experience"]["has_experience"] is True
    assert result["experience"]["total_years"] == 3.0


def test_availability_extraction():

    result = extract_answer_details(
        "I am available immediately."
    )

    assert result["availability"]["available_immediately"] is True
    assert result["availability"]["availability_mentioned"] is True


def test_salary_extraction():

    result = extract_answer_details(
        "My expected salary is 6 LPA."
    )

    assert result["salary"]["salary_mentioned"] is True


def test_off_topic_detection():

    assert classify_intent(
        "I watched a great movie yesterday."
    ) == "OFF_TOPIC"


def test_missing_vague_detection():

    assert classify_intent(
        "Not sure."
    ) == "MISSING_OR_VAGUE"


def test_semantic_object_structure():

    result = understand_answer(
        "I have 2 years of experience with Python and SQL."
    )

    semantic = result["semantic_object"]

    assert "intent" in semantic
    assert "answer_status" in semantic
    assert "confidence" in semantic
    assert "semantic_data" in semantic
    assert "skills" in semantic["semantic_data"]
    assert "experience" in semantic["semantic_data"]
    assert "availability" in semantic["semantic_data"]
    assert "salary" in semantic["semantic_data"]


def test_combined_answer():

    result = understand_answer(
        "I have 2 years of experience with Python and SQL, "
        "and I can join immediately."
    )

    assert result["extracted"]["experience"]["total_years"] == 2.0

    assert (
        result["extracted"]["availability"]["available_immediately"]
        is True
    )


def test_empty_answer():

    result = understand_answer("")

    assert result["intent"] == "MISSING_OR_VAGUE"
    assert result["answer_status"] == "MISSING_OR_VAGUE"


def test_partial_answer():

    result = understand_answer("Python")

    assert result["answer_status"] == "PARTIAL"
