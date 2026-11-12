import json
import re
from pathlib import Path
from datetime import datetime, timezone


POSITIVE_PHRASES = {
    "confident", "successfully", "achieved", "improved",
    "resolved", "completed", "effective", "proud",
    "learned", "contributed", "positive", "strong",
}

NEGATIVE_PHRASES = {
    "failed", "difficult", "worried", "problem",
    "frustrated", "overwhelmed", "confused", "nervous",
    "unfortunately", "struggled", "negative", "stressed",
}

UNCERTAINTY_PHRASES = {
    "i think", "maybe", "perhaps", "i guess",
    "not sure", "i am not sure", "i'm not sure",
    "probably", "possibly", "i suppose",
    "i don't know", "i dont know",
}

HESITATION_WORDS = {
    "um", "uh", "erm", "hmm", "umm", "uhh",
}

STRESS_PHRASES = {
    "under pressure", "overwhelmed", "very nervous",
    "feeling stressed", "highly stressed",
    "too much pressure", "worried about",
    "struggling to cope",
}

CONTRADICTION_PAIRS = [
    ("always", "never"),
    ("agree", "disagree"),
    ("confident", "not confident"),
    ("available", "unavailable"),
    ("interested", "not interested"),
    ("completed", "not completed"),
    ("can", "cannot"),
]


def normalize_text(text):
    """Normalize whitespace while preserving the original meaning."""
    if text is None:
        return ""

    return re.sub(r"\s+", " ", str(text)).strip()


def tokenize(text):
    """Extract words from text."""
    return re.findall(
        r"\b[a-zA-Z]+(?:'[a-zA-Z]+)?\b",
        normalize_text(text).lower(),
    )


def detect_long_pauses(text, pause_threshold=2.0):
    """
    Detect pause markers only when they are explicitly present in a
    transcript, such as [pause: 3.2s].

    Actual pause duration requires audio timing or timestamp metadata.
    """
    normalized = normalize_text(text)

    pattern = r"\[\s*pause\s*:\s*(\d+(?:\.\d+)?)\s*s?\s*\]"
    matches = re.findall(pattern, normalized, flags=re.IGNORECASE)

    pauses = []

    for value in matches:
        duration = float(value)

        if duration >= pause_threshold:
            pauses.append({
                "duration_seconds": duration,
                "threshold_seconds": pause_threshold,
            })

    return {
        "long_pause_count": len(pauses),
        "pauses": pauses,
        "source": "Explicit transcript pause markers only",
    }


def detect_repeated_words(text):
    """Detect consecutive repeated words."""
    words = tokenize(text)
    repetitions = []

    for index in range(1, len(words)):
        if words[index] == words[index - 1]:
            repetitions.append({
                "word": words[index],
                "position": index,
            })

    return {
        "repeated_word_count": len(repetitions),
        "repetitions": repetitions,
    }


def detect_hesitation(text):
    """Identify uncertainty phrases, filler words, and marked pauses."""
    normalized = normalize_text(text).lower()
    words = tokenize(normalized)

    uncertainty_matches = [
        phrase for phrase in sorted(UNCERTAINTY_PHRASES)
        if phrase in normalized
    ]

    hesitation_matches = [
        word for word in words
        if word in HESITATION_WORDS
    ]

    repeated = detect_repeated_words(normalized)
    pauses = detect_long_pauses(normalized)

    return {
        "uncertainty_phrases": uncertainty_matches,
        "hesitation_word_count": len(hesitation_matches),
        "hesitation_words": hesitation_matches,
        "repeated_word_count": repeated["repeated_word_count"],
        "repeated_words": repeated["repetitions"],
        "long_pause_count": pauses["long_pause_count"],
        "long_pauses": pauses["pauses"],
        "note": (
            "These are language or transcript signals. They do not prove "
            "that a person lacks confidence."
        ),
    }


def analyze_sentiment(text):
    """
    Count predefined positive and negative language indicators.

    This is a simple lexical indicator, not a trained sentiment model.
    """
    normalized = normalize_text(text).lower()
    words = tokenize(normalized)

    positive_found = [
        phrase for phrase in sorted(POSITIVE_PHRASES)
        if re.search(
            r"\b" + re.escape(phrase) + r"\b",
            normalized,
        )
    ]

    negative_found = [
        phrase for phrase in sorted(NEGATIVE_PHRASES)
        if re.search(
            r"\b" + re.escape(phrase) + r"\b",
            normalized,
        )
    ]

    positive_count = len(positive_found)
    negative_count = len(negative_found)

    if positive_count > negative_count:
        label = "POSITIVE_LANGUAGE"
    elif negative_count > positive_count:
        label = "NEGATIVE_LANGUAGE"
    elif positive_count == 0 and negative_count == 0:
        label = "NEUTRAL_OR_UNDETECTED"
    else:
        label = "MIXED_LANGUAGE"

    total = positive_count + negative_count

    if total:
        sentiment_score = (
            (positive_count - negative_count) / total
        ) * 100
    else:
        sentiment_score = 0.0

    return {
        "label": label,
        "positive_indicator_count": positive_count,
        "negative_indicator_count": negative_count,
        "positive_indicators": positive_found,
        "negative_indicators": negative_found,
        "sentiment_score": round(sentiment_score, 2),
        "word_count": len(words),
        "note": (
            "The label describes detected wording, not the person's "
            "actual emotional state."
        ),
    }


def detect_contradictions(text):
    """
    Flag simple opposing phrase patterns in the same response.

    These are potential review signals. Context is required to confirm
    a contradiction, so a flagged pair is not treated as proof.
    """
    normalized = normalize_text(text).lower()
    flags = []

    for first, second in CONTRADICTION_PAIRS:
        first_pattern = r"\b" + re.escape(first) + r"\b"
        second_pattern = r"\b" + re.escape(second) + r"\b"

        if (
            re.search(first_pattern, normalized)
            and re.search(second_pattern, normalized)
        ):
            flags.append({
                "phrase_a": first,
                "phrase_b": second,
                "reason": "Potentially opposing wording detected.",
            })

    return {
        "potential_contradiction_count": len(flags),
        "flags": flags,
        "requires_contextual_review": bool(flags),
    }


def analyze_stress_indicators(text):
    """
    Detect explicit stress-related wording and possible textual signals.

    Actual physiological or psychological stress cannot be determined
    reliably from text alone.
    """
    normalized = normalize_text(text).lower()
    words = tokenize(normalized)

    matched_phrases = [
        phrase for phrase in sorted(STRESS_PHRASES)
        if phrase in normalized
    ]

    hesitation = detect_hesitation(normalized)
    negative_count = analyze_sentiment(normalized)[
        "negative_indicator_count"
    ]

    signal_count = (
        len(matched_phrases)
        + hesitation["long_pause_count"]
        + hesitation["repeated_word_count"]
    )

    if signal_count == 0 and negative_count == 0:
        indicator_level = "NO_EXPLICIT_INDICATORS_DETECTED"
    elif signal_count + negative_count <= 2:
        indicator_level = "SOME_INDICATORS_DETECTED"
    else:
        indicator_level = "MULTIPLE_INDICATORS_DETECTED"

    return {
        "indicator_level": indicator_level,
        "stress_related_phrases": matched_phrases,
        "negative_language_count": negative_count,
        "long_pause_count": hesitation["long_pause_count"],
        "repeated_word_count": hesitation["repeated_word_count"],
        "word_count": len(words),
        "note": (
            "This is a textual signal summary, not a diagnosis or "
            "a reliable measurement of actual stress."
        ),
    }


def calculate_behavioral_confidence_score(text):
    """
    Calculate a transparent prototype score from 0 to 100.

    A higher score means fewer predefined uncertainty and hesitation
    signals were detected. It does not establish actual confidence.
    """
    normalized = normalize_text(text)

    if not normalized:
        return {
            "score": 0.0,
            "score_range": "0-100",
            "explanation": "No response was provided.",
            "signals_used": {},
        }

    words = tokenize(normalized)
    hesitation = detect_hesitation(normalized)
    sentiment = analyze_sentiment(normalized)
    contradictions = detect_contradictions(normalized)

    score = 70.0

    uncertainty_count = len(hesitation["uncertainty_phrases"])
    repeated_count = hesitation["repeated_word_count"]
    pause_count = hesitation["long_pause_count"]
    filler_count = hesitation["hesitation_word_count"]

    score -= min(25.0, uncertainty_count * 8.0)
    score -= min(15.0, repeated_count * 3.0)
    score -= min(15.0, pause_count * 5.0)
    score -= min(10.0, filler_count * 2.0)

    # Neutral language is not automatically treated as negative.
    if sentiment["label"] == "POSITIVE_LANGUAGE":
        score += 5.0

    # Contradiction flags are included for review, not automatically
    # treated as proof of low confidence or dishonesty.
    score = max(0.0, min(100.0, score))

    return {
        "score": round(score, 2),
        "score_range": "0-100",
        "explanation": (
            "Prototype score based on predefined language signals. "
            "It does not measure actual confidence or suitability."
        ),
        "signals_used": {
            "uncertainty_phrase_count": uncertainty_count,
            "repeated_word_count": repeated_count,
            "long_pause_count": pause_count,
            "hesitation_word_count": filler_count,
            "word_count": len(words),
            "sentiment_label": sentiment["label"],
            "potential_contradiction_count": (
                contradictions["potential_contradiction_count"]
            ),
        },
    }


def analyze_response(response_id, text):
    """Run the complete confidence and stress signal analysis."""
    normalized = normalize_text(text)

    return {
        "response_id": response_id,
        "analyzed_at_utc": datetime.now(timezone.utc).isoformat(),
        "word_count": len(tokenize(normalized)),
        "hesitation_analysis": detect_hesitation(normalized),
        "sentiment_analysis": analyze_sentiment(normalized),
        "contradiction_analysis": detect_contradictions(normalized),
        "stress_analysis": analyze_stress_indicators(normalized),
        "behavioral_confidence": calculate_behavioral_confidence_score(
            normalized
        ),
        "original_text": normalized,
        "limitations": [
            "Text does not reliably reveal actual confidence or stress.",
            "Long pauses are detected only when explicit pause markers exist.",
            "Sentiment uses predefined words and phrases.",
            "Contradiction flags require context and human review.",
            "The score is experimental and must not determine hiring decisions.",
        ],
    }


def save_report(results, output_dir):
    """Save detailed JSON and Markdown reports."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "day36_confidence_stress_report.json"
    markdown_path = output_dir / "day36_confidence_stress_report.md"

    report = {
        "day": 36,
        "title": "Confidence & Stress Indicators",
        "total_responses": len(results),
        "results": results,
    }

    json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = [
        "# Day 36 - Confidence & Stress Indicators",
        "",
        f"Responses analyzed: {len(results)}",
        "",
        "## Results",
        "",
        "| Response | Confidence Signal Score | Sentiment Wording | Stress Indicator |",
        "|---|---:|---|---|",
    ]

    for result in results:
        confidence = result["behavioral_confidence"]["score"]
        sentiment = result["sentiment_analysis"]["label"]
        stress = result["stress_analysis"]["indicator_level"]

        lines.append(
            f"| {result['response_id']} | {confidence}/100 "
            f"| {sentiment} | {stress} |"
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "Scores and labels represent rule-based text indicators only.",
        "They do not prove actual confidence, stress, honesty, or suitability.",
        "",
        "## Limitations",
        "",
    ])

    for result in results:
        for limitation in result["limitations"]:
            if limitation not in lines:
                lines.append(f"- {limitation}")

    lines.append("")

    markdown_path.write_text("\n".join(lines), encoding="utf-8")

    return json_path, markdown_path
