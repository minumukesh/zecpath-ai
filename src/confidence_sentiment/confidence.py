import re

HESITATION_PATTERNS = [
    r"\bum+\b",
    r"\buh+\b",
    r"\ber+\b",
    r"\bah+\b",
    r"\bi think\b",
    r"\bi guess\b",
    r"\bmaybe\b",
    r"\bperhaps\b",
    r"\bkind of\b",
    r"\bsort of\b",
    r"\bi am not sure\b",
    r"\bi'm not sure\b",
    r"\bi don't know\b",
    r"\bi do not know\b",
]

UNCERTAINTY_PATTERNS = [
    r"\bmaybe\b",
    r"\bperhaps\b",
    r"\bpossibly\b",
    r"\bprobably\b",
    r"\bi am not sure\b",
    r"\bi'm not sure\b",
    r"\bi don't know\b",
    r"\bi do not know\b",
    r"\bi guess\b",
    r"\bi think\b",
    r"\bnot certain\b",
    r"\buncertain\b",
    r"\bnot confident\b",
]


def _find_matches(text, patterns):
    matches = []

    for pattern in patterns:
        for match in re.finditer(
            pattern,
            text,
            flags=re.IGNORECASE
        ):
            matches.append({
                "phrase": match.group(0),
                "start": match.start(),
                "end": match.end(),
            })

    matches.sort(key=lambda item: item["start"])
    return matches


def analyze_confidence(text):
    text = str(text or "").strip()

    words = re.findall(
        r"\b[\w'-]+\b",
        text
    )

    hesitation_matches = _find_matches(
        text,
        HESITATION_PATTERNS
    )

    uncertainty_matches = _find_matches(
        text,
        UNCERTAINTY_PATTERNS
    )

    word_count = len(words)
    hesitation_count = len(hesitation_matches)
    uncertainty_count = len(uncertainty_matches)

    hesitation_rate = round(
        hesitation_count / word_count,
        4
    ) if word_count else 0.0

    communication_signal = round(
        max(
            0.0,
            min(
                100.0,
                100.0
                - min(60.0, hesitation_rate * 100)
                - min(30.0, uncertainty_count * 5)
            )
        ),
        2
    )

    if word_count == 0:
        interpretation = "NO_RESPONSE"
    elif hesitation_count >= 4 or uncertainty_count >= 3:
        interpretation = "MULTIPLE_HESITATION_OR_UNCERTAINTY_SIGNALS"
    elif hesitation_count > 0 or uncertainty_count > 0:
        interpretation = "SOME_HESITATION_OR_UNCERTAINTY_SIGNALS"
    else:
        interpretation = "FEW_DETECTED_TEXT_SIGNALS"

    return {
        "word_count": word_count,
        "hesitation_count": hesitation_count,
        "hesitation_phrases": [
            item["phrase"]
            for item in hesitation_matches
        ],
        "uncertainty_count": uncertainty_count,
        "uncertainty_phrases": [
            item["phrase"]
            for item in uncertainty_matches
        ],
        "hesitation_rate": hesitation_rate,
        "communication_signal_score": communication_signal,
        "interpretation": interpretation,
        "measurement_note": (
            "Text-based heuristic only. It does not establish "
            "actual confidence, personality, or emotional state."
        ),
    }
