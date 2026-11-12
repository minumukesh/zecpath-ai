from .confidence import analyze_confidence
from .sentiment import analyze_sentiment
from .response_metrics import analyze_response_length_and_pace
from .contradictions import detect_contradictions


def analyze_response(
    response_id,
    text,
    duration_seconds=None
):
    text = str(text or "").strip()

    confidence_result = analyze_confidence(text)
    sentiment_result = analyze_sentiment(text)

    response_metrics = analyze_response_length_and_pace(
        text,
        duration_seconds
    )

    communication_strength = []

    if response_metrics["word_count"] == 0:
        communication_strength.append(
            "NO_RESPONSE_PROVIDED"
        )
    elif response_metrics["word_count"] < 5:
        communication_strength.append(
            "VERY_SHORT_RESPONSE"
        )
    else:
        communication_strength.append(
            "RESPONSE_CONTAINS_MULTIPLE_WORDS"
        )

    if confidence_result["hesitation_count"] == 0:
        communication_strength.append(
            "NO_CONFIGURED_HESITATION_PHRASES_DETECTED"
        )
    else:
        communication_strength.append(
            "HESITATION_PHRASES_DETECTED"
        )

    if sentiment_result["sentiment"] == "POSITIVE":
        communication_strength.append(
            "POSITIVE_LEXICAL_SIGNAL"
        )
    elif sentiment_result["sentiment"] == "NEGATIVE":
        communication_strength.append(
            "NEGATIVE_LEXICAL_SIGNAL"
        )
    else:
        communication_strength.append(
            "NEUTRAL_OR_UNDETECTED_SENTIMENT"
        )

    return {
        "response_id": response_id,
        "response_text": text,
        "confidence_analysis": confidence_result,
        "sentiment_analysis": sentiment_result,
        "response_metrics": response_metrics,
        "communication_strength_indicators": communication_strength,
    }


def analyze_screening(candidate_id, responses):
    if not isinstance(responses, list):
        raise TypeError(
            "responses must be a list."
        )

    analyzed_responses = []

    for index, item in enumerate(responses, start=1):
        if not isinstance(item, dict):
            raise TypeError(
                f"Response {index} must be a dictionary."
            )

        response_id = item.get(
            "response_id",
            f"R{index:03d}"
        )

        analyzed_responses.append(
            analyze_response(
                response_id=response_id,
                text=item.get("text", ""),
                duration_seconds=item.get("duration_seconds"),
            )
        )

    original_texts = [
        item.get("text", "")
        for item in responses
    ]

    contradiction_findings = detect_contradictions(
        original_texts
    )

    behavioral_report = {
        "hesitation_responses": sum(
            1 for item in analyzed_responses
            if item["confidence_analysis"]["hesitation_count"] > 0
        ),
        "uncertainty_responses": sum(
            1 for item in analyzed_responses
            if item["confidence_analysis"]["uncertainty_count"] > 0
        ),
        "positive_sentiment_responses": sum(
            1 for item in analyzed_responses
            if item["sentiment_analysis"]["sentiment"] == "POSITIVE"
        ),
        "negative_sentiment_responses": sum(
            1 for item in analyzed_responses
            if item["sentiment_analysis"]["sentiment"] == "NEGATIVE"
        ),
        "neutral_sentiment_responses": sum(
            1 for item in analyzed_responses
            if item["sentiment_analysis"]["sentiment"] == "NEUTRAL"
        ),
        "interpretation_note": (
            "These are text-based signals, not definitive judgments "
            "about candidate personality, confidence, or suitability."
        ),
    }

    return {
        "candidate_id": candidate_id,
        "analysis_engine": "day27_confidence_sentiment_analysis",
        "response_count": len(analyzed_responses),
        "responses": analyzed_responses,
        "contradiction_analysis": {
            "potential_contradiction_count": len(
                contradiction_findings
            ),
            "findings": contradiction_findings,
            "note": (
                "Only configured text patterns are checked. "
                "This is not comprehensive semantic contradiction detection."
            ),
        },
        "behavioral_indicators_report": behavioral_report,
    }
