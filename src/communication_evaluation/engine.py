import json
import re
from pathlib import Path
from datetime import datetime, timezone


# All weights total 100%.
SCORING_WEIGHTS = {
    "fluency": 0.25,
    "grammar_quality": 0.20,
    "vocabulary_range": 0.15,
    "clarity": 0.25,
    "answer_structure": 0.15,
}

FILLER_WORDS = {
    "um", "uh", "erm", "hmm", "basically",
    "actually", "literally", "like", "you know",
    "i mean", "sort of", "kind of",
}

INTRODUCTION_INDICATORS = {
    "first", "firstly", "introduction", "to begin",
    "i will explain", "my main point",
}

DETAIL_INDICATORS = {
    "because", "for example", "for instance",
    "also", "additionally", "therefore",
    "as a result", "this means",
}

CONCLUSION_INDICATORS = {
    "finally", "in conclusion", "to summarize",
    "overall", "in summary", "as a result",
}

# These are simple heuristic lists, not a complete grammar checker.
GRAMMAR_WARNING_PATTERNS = [
    (r"\bi is\b", "Possible subject-verb agreement issue"),
    (r"\bhe are\b", "Possible subject-verb agreement issue"),
    (r"\bshe are\b", "Possible subject-verb agreement issue"),
    (r"\bthey is\b", "Possible subject-verb agreement issue"),
    (r"\bi has\b", "Possible subject-verb agreement issue"),
    (r"\bhe have\b", "Possible subject-verb agreement issue"),
    (r"\bshe have\b", "Possible subject-verb agreement issue"),
    (r"\bdont\b", "Possible missing apostrophe"),
    (r"\bdoesnt\b", "Possible missing apostrophe"),
    (r"\bcant\b", "Possible missing apostrophe"),
    (r"\bwont\b", "Possible missing apostrophe"),
]


def normalize_text(text):
    """Normalize whitespace without changing the intended wording."""
    if text is None:
        return ""

    return re.sub(r"\s+", " ", str(text)).strip()


def tokenize(text):
    """Extract words for basic text-based analysis."""
    return re.findall(r"\b[a-zA-Z]+(?:'[a-zA-Z]+)?\b", text.lower())


def split_sentences(text):
    """Split text using common sentence-ending punctuation."""
    text = normalize_text(text)

    if not text:
        return []

    return [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", text)
        if sentence.strip()
    ]


def detect_filler_words(text):
    """
    Detect predefined filler words.

    This checks the written transcript. It cannot reliably detect
    pauses or spoken fillers omitted by speech-to-text.
    """
    lowered = normalize_text(text).lower()
    matches = []

    for filler in sorted(FILLER_WORDS, key=len, reverse=True):
        pattern = r"(?<!\w)" + re.escape(filler) + r"(?!\w)"

        for match in re.finditer(pattern, lowered):
            matches.append({
                "word": filler,
                "start": match.start(),
                "end": match.end(),
            })

    matches.sort(key=lambda item: item["start"])

    return {
        "count": len(matches),
        "items": [
            {
                "word": item["word"],
                "position": item["start"],
            }
            for item in matches
        ],
    }


def evaluate_fluency(text):
    """
    Estimate written-response flow from sentence count, length,
    and extremely short fragments.

    Actual spoken fluency requires audio or reliable timing data.
    """
    words = tokenize(text)
    sentences = split_sentences(text)

    if not words:
        return {
            "score": 0.0,
            "sentence_count": 0,
            "average_sentence_length": 0.0,
            "explanation": "No response text was provided.",
        }

    average_length = len(words) / max(len(sentences), 1)
    short_sentences = sum(
        1 for sentence in sentences
        if len(tokenize(sentence)) <= 2
    )

    score = 100.0

    if len(words) < 5:
        score -= 35

    if len(sentences) > 1:
        score += 0
    elif len(words) >= 12:
        score -= 8

    if average_length < 3:
        score -= 20
    elif average_length > 35:
        score -= 15

    if sentences:
        score -= (short_sentences / len(sentences)) * 15

    score = max(0.0, min(100.0, score))

    return {
        "score": round(score, 2),
        "sentence_count": len(sentences),
        "average_sentence_length": round(average_length, 2),
        "explanation": (
            "Estimated from written sentence patterns. "
            "This is not a direct measurement of speaking pace."
        ),
    }


def evaluate_grammar(text):
    """
    Apply a small set of transparent grammar-warning rules.

    This is not a full grammar checker and may miss errors or flag
    wording that is acceptable in a particular context.
    """
    lowered = normalize_text(text).lower()
    words = tokenize(text)

    if not words:
        return {
            "score": 0.0,
            "warnings": [],
            "warning_count": 0,
        }

    warnings = []

    for pattern, description in GRAMMAR_WARNING_PATTERNS:
        for match in re.finditer(pattern, lowered):
            warnings.append({
                "text": match.group(0),
                "position": match.start(),
                "reason": description,
            })

    # The penalty is capped to avoid excessive impact from this
    # deliberately small set of rules.
    penalty = min(60.0, len(warnings) * 15.0)
    score = max(0.0, 100.0 - penalty)

    return {
        "score": round(score, 2),
        "warnings": warnings,
        "warning_count": len(warnings),
    }


def evaluate_vocabulary(text):
    """
    Estimate vocabulary variety using type-token ratio.

    Very short responses are marked as limited evidence rather than
    treated as proof of weak vocabulary.
    """
    words = tokenize(text)

    if not words:
        return {
            "score": 0.0,
            "unique_word_count": 0,
            "total_word_count": 0,
            "type_token_ratio": 0.0,
            "evidence": "No text available.",
        }

    unique_words = set(words)
    ratio = len(unique_words) / len(words)

    # A simple normalized variety score.
    score = min(100.0, ratio * 125.0)

    evidence = (
        "Limited evidence because the response is very short."
        if len(words) < 10
        else "Estimated from unique-word variety."
    )

    return {
        "score": round(score, 2),
        "unique_word_count": len(unique_words),
        "total_word_count": len(words),
        "type_token_ratio": round(ratio, 4),
        "evidence": evidence,
    }


def evaluate_clarity(text):
    """
    Estimate readability from sentence length, word length,
    and basic punctuation.
    """
    words = tokenize(text)
    sentences = split_sentences(text)

    if not words:
        return {
            "score": 0.0,
            "average_word_length": 0.0,
            "average_sentence_length": 0.0,
            "explanation": "No response text was provided.",
        }

    average_word_length = sum(len(word) for word in words) / len(words)
    average_sentence_length = len(words) / max(len(sentences), 1)

    score = 100.0

    if average_sentence_length > 30:
        score -= 20
    elif average_sentence_length > 22:
        score -= 10

    if average_word_length > 8:
        score -= 15
    elif average_word_length > 6.5:
        score -= 7

    if not re.search(r"[.!?]$", normalize_text(text)):
        score -= 5

    return {
        "score": round(max(0.0, min(100.0, score)), 2),
        "average_word_length": round(average_word_length, 2),
        "average_sentence_length": round(average_sentence_length, 2),
        "explanation": (
            "Estimated from sentence and word patterns. "
            "It does not determine whether the answer is factually correct."
        ),
    }


def evaluate_answer_structure(text):
    """
    Check for opening, supporting-detail, and concluding indicators.

    These indicators are optional writing patterns, not mandatory
    phrases that every good answer must contain.
    """
    lowered = normalize_text(text).lower()
    words = tokenize(text)

    if not words:
        return {
            "score": 0.0,
            "introduction_indicator": False,
            "detail_indicator": False,
            "conclusion_indicator": False,
        }

    has_intro = any(
        phrase in lowered for phrase in INTRODUCTION_INDICATORS
    )
    has_detail = any(
        phrase in lowered for phrase in DETAIL_INDICATORS
    )
    has_conclusion = any(
        phrase in lowered for phrase in CONCLUSION_INDICATORS
    )

    # Basic response-length evidence is included so a response
    # is not penalized only because it lacks a formulaic phrase.
    score = 40.0

    if len(words) >= 8:
        score += 20.0

    if has_intro:
        score += 15.0

    if has_detail:
        score += 15.0

    if has_conclusion:
        score += 10.0

    return {
        "score": round(min(100.0, score), 2),
        "introduction_indicator": has_intro,
        "detail_indicator": has_detail,
        "conclusion_indicator": has_conclusion,
    }


def evaluate_communication(text):
    """
    Evaluate a written transcript and produce a 0-100 score.

    The result is an explainable prototype score, not a validated
    measure of a person's communication ability.
    """
    normalized = normalize_text(text)

    fluency = evaluate_fluency(normalized)
    grammar = evaluate_grammar(normalized)
    vocabulary = evaluate_vocabulary(normalized)
    clarity = evaluate_clarity(normalized)
    structure = evaluate_answer_structure(normalized)
    fillers = detect_filler_words(normalized)

    components = {
        "fluency": fluency["score"],
        "grammar_quality": grammar["score"],
        "vocabulary_range": vocabulary["score"],
        "clarity": clarity["score"],
        "answer_structure": structure["score"],
    }

    total_weight = sum(SCORING_WEIGHTS.values())

    # All component values are normalized to the same 0-100 scale.
    final_score = sum(
        components[name] * weight
        for name, weight in SCORING_WEIGHTS.items()
    ) / total_weight

    if not normalized:
        final_score = 0.0

    return {
        "evaluation_id": None,
        "evaluated_at_utc": datetime.now(timezone.utc).isoformat(),
        "word_count": len(tokenize(normalized)),
        "sentence_count": len(split_sentences(normalized)),
        "component_scores": components,
        "scoring_weights": SCORING_WEIGHTS,
        "communication_score": round(final_score, 2),
        "score_range": "0-100",
        "filler_word_analysis": fillers,
        "details": {
            "fluency": fluency,
            "grammar_quality": grammar,
            "vocabulary_range": vocabulary,
            "clarity": clarity,
            "answer_structure": structure,
        },
        "normalization": {
            "component_scale": "0-100",
            "weight_total": round(total_weight, 4),
            "method": "Weighted average of normalized component scores.",
        },
        "limitations": [
            "Evaluates text transcripts, not audio directly.",
            "Does not directly measure pronunciation, accent, speaking pace, or pauses.",
            "Grammar and filler detection use limited predefined rules.",
            "Vocabulary variety is not the same as vocabulary quality.",
            "Scores must not be used alone to make hiring decisions.",
            "Fairness requires validation across roles, languages, and candidate groups.",
        ],
    }


def save_evaluation_report(result, output_dir, evaluation_id="D35-001"):
    """Save JSON and Markdown versions of a sample evaluation."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    result = dict(result)
    result["evaluation_id"] = evaluation_id

    json_path = output_dir / f"{evaluation_id}_communication_score.json"
    markdown_path = output_dir / f"{evaluation_id}_communication_score.md"

    json_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = [
        "# Day 35 - Communication Skill Evaluation",
        "",
        f"Evaluation ID: {evaluation_id}",
        f"Communication Score: {result['communication_score']}/100",
        "",
        "## Component Scores",
        "",
        "| Component | Score | Weight |",
        "|---|---:|---:|",
    ]

    for name, score in result["component_scores"].items():
        weight = result["scoring_weights"][name] * 100
        lines.append(f"| {name} | {score}/100 | {weight:.0f}% |")

    lines.extend([
        "",
        "## Filler Words",
        "",
        f"Count: {result['filler_word_analysis']['count']}",
        "",
        "## Scoring Formula",
        "",
        "Final Score = sum(component score x component weight)",
        "",
        "All components are normalized to a 0-100 scale before aggregation.",
        "",
        "## Limitations",
        "",
    ])

    lines.extend(f"- {item}" for item in result["limitations"])
    lines.append("")

    markdown_path.write_text("\n".join(lines), encoding="utf-8")

    return json_path, markdown_path
