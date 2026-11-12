import pytest

from src.confidence_sentiment import (
    analyze_confidence,
    analyze_response,
    analyze_screening,
    analyze_sentiment,
)

from src.confidence_sentiment.response_metrics import (
    analyze_response_length_and_pace,
)

from src.confidence_sentiment.contradictions import (
    detect_contradictions,
)


def test_hesitation_detection():
    result = analyze_confidence(
        "Um, I think I can do this."
    )
    assert result["hesitation_count"] >= 2


def test_uncertainty_detection():
    result = analyze_confidence(
        "Maybe I am not sure about that."
    )
    assert result["uncertainty_count"] >= 1


def test_positive_sentiment():
    result = analyze_sentiment(
        "I successfully completed a great project."
    )
    assert result["sentiment"] == "POSITIVE"
    assert result["sentiment_score"] > 0


def test_negative_sentiment():
    result = analyze_sentiment(
        "I had a difficult problem and felt frustrated."
    )
    assert result["sentiment"] == "NEGATIVE"
    assert result["sentiment_score"] < 0


def test_neutral_sentiment():
    result = analyze_sentiment(
        "The meeting starts at ten."
    )
    assert result["sentiment"] == "NEUTRAL"
    assert result["sentiment_score"] == 0


def test_response_length():
    result = analyze_response_length_and_pace(
        "I know Python and SQL."
    )
    assert result["word_count"] == 5
    assert result["duration_seconds"] is None


def test_speaking_pace():
    result = analyze_response_length_and_pace(
        "I know Python and SQL.",
        duration_seconds=5
    )
    assert result["words_per_minute"] == 60.0
    assert result["pace_label"] == "SLOW"


def test_invalid_duration():
    with pytest.raises(ValueError):
        analyze_response_length_and_pace(
            "Hello there.",
            duration_seconds=-1
        )


def test_potential_contradiction_detection():
    responses = [
        "I have experience in Python.",
        "I have no experience in Python.",
    ]

    findings = detect_contradictions(responses)

    assert len(findings) >= 1
    assert findings[0]["status"] == "POTENTIAL_CONTRADICTION"


def test_response_analysis_structure():
    result = analyze_response(
        "R001",
        "I enjoy solving problems and learning Python.",
        duration_seconds=10
    )

    assert "confidence_analysis" in result
    assert "sentiment_analysis" in result
    assert "response_metrics" in result
    assert "communication_strength_indicators" in result


def test_screening_report():
    result = analyze_screening(
        "CAND_TEST",
        [
            {
                "response_id": "R001",
                "text": "I completed a great project.",
                "duration_seconds": 10,
            },
            {
                "response_id": "R002",
                "text": "Maybe I need more time.",
                "duration_seconds": 8,
            },
        ]
    )

    assert result["response_count"] == 2
    assert "behavioral_indicators_report" in result
    assert "contradiction_analysis" in result


def test_empty_response():
    result = analyze_response(
        "R001",
        ""
    )

    assert result["response_metrics"]["word_count"] == 0
    assert result["confidence_analysis"]["interpretation"] == "NO_RESPONSE"


def test_empty_screening():
    result = analyze_screening(
        "CAND_EMPTY",
        []
    )

    assert result["response_count"] == 0
    assert result["responses"] == []
    assert (
        result["behavioral_indicators_report"]
        ["positive_sentiment_responses"] == 0
    )
