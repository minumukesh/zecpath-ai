import re


def analyze_response_length_and_pace(
    text,
    duration_seconds=None
):
    text = str(text or "").strip()

    words = re.findall(
        r"\b[\w'-]+\b",
        text
    )

    word_count = len(words)

    sentences = [
        sentence
        for sentence in re.split(r"[.!?]+", text)
        if sentence.strip()
    ]

    sentence_count = len(sentences)

    average_words_per_sentence = round(
        word_count / sentence_count,
        2
    ) if sentence_count else 0.0

    duration = None
    words_per_minute = None
    pace_label = "DURATION_NOT_PROVIDED"

    if duration_seconds is not None:
        duration = float(duration_seconds)

        if duration < 0:
            raise ValueError(
                "duration_seconds cannot be negative."
            )

        if duration == 0 and word_count > 0:
            raise ValueError(
                "Duration must be greater than zero "
                "for a non-empty response."
            )

        if duration > 0:
            words_per_minute = round(
                word_count / duration * 60,
                2
            )

            if words_per_minute < 100:
                pace_label = "SLOW"
            elif words_per_minute <= 160:
                pace_label = "MODERATE"
            else:
                pace_label = "FAST"

        elif word_count == 0:
            pace_label = "NO_SPEECH"

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "average_words_per_sentence": average_words_per_sentence,
        "duration_seconds": duration,
        "words_per_minute": words_per_minute,
        "pace_label": pace_label,
    }
