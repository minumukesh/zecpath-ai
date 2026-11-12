import pytest

from src.screening_scoring import score_question, score_screening


def sample_questions():
    return [
        {
            "question_id": "Q001",
            "question": "Which technical skills do you have?",
            "answer": "I have experience with Python, SQL and Excel.",
            "expected_keywords": ["Python", "SQL", "Excel"],
            "required_fields": ["Python", "SQL", "Excel"],
        },
        {
            "question_id": "Q002",
            "question": "When can you join?",
            "answer": "I am available to join immediately.",
            "expected_keywords": ["join", "immediately"],
            "required_fields": ["join"],
        },
    ]


def test_question_scoring_returns_all_parameters():

    result = score_question(
        "Which skills do you have?",
        "I know Python and SQL.",
        expected_keywords=["Python", "SQL"],
    )

    assert set(result["parameter_scores"]) == {
        "clarity",
        "relevance",
        "completeness",
        "consistency",
    }


def test_question_score_is_normalized():

    result = score_question(
        "Which skills do you have?",
        "I know Python and SQL.",
        expected_keywords=["Python", "SQL"],
    )

    assert 0 <= result["weighted_score"] <= 100


def test_empty_answer_scores_zero_for_missing_content():

    result = score_question(
        "Which skills do you have?",
        "",
        expected_keywords=["Python", "SQL"],
        required_fields=["Python", "SQL"],
    )

    assert result["parameter_scores"]["clarity"] == 0
    assert result["parameter_scores"]["relevance"] == 0
    assert result["parameter_scores"]["completeness"] == 0


def test_screening_aggregate_score():

    result = score_screening(
        "CAND_TEST",
        sample_questions(),
    )

    assert 0 <= result["overall_screening_score"] <= 100
    assert result["question_count"] == 2


def test_per_question_breakdown_is_present():

    result = score_screening(
        "CAND_TEST",
        sample_questions(),
    )

    assert len(result["question_scores"]) == 2
    assert all(
        "weighted_score" in item
        for item in result["question_scores"]
    )


def test_explainable_output_is_present():

    result = score_screening(
        "CAND_TEST",
        sample_questions(),
    )

    assert "explainable_output" in result
    assert "limitations" in result["explainable_output"]


def test_parameter_weights_sum_to_one():

    result = score_screening(
        "CAND_TEST",
        sample_questions(),
    )

    assert sum(result["parameter_weights"].values()) == pytest.approx(1.0)


def test_empty_question_list_rejected():

    with pytest.raises(ValueError):
        score_screening("CAND_TEST", [])


def test_missing_question_text_rejected():

    with pytest.raises(ValueError):
        score_screening(
            "CAND_TEST",
            [{"question": "", "answer": "Python"}],
        )


def test_classification_is_generated():

    result = score_screening(
        "CAND_TEST",
        sample_questions(),
    )

    assert result["classification"] in {
        "HIGH",
        "GOOD",
        "MODERATE",
        "LOW",
    }
