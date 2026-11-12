from __future__ import annotations

import re


def normalize_transcript_text(
    text: str,
) -> str:

    if text is None:

        return ""


    normalized = str(text)


    # --------------------------------------------------------
    # Normalize line breaks
    # --------------------------------------------------------

    normalized = normalized.replace(
        "\r\n",
        " ",
    )

    normalized = normalized.replace(
        "\r",
        " ",
    )

    normalized = normalized.replace(
        "\n",
        " ",
    )


    # --------------------------------------------------------
    # Normalize repeated whitespace
    # --------------------------------------------------------

    normalized = re.sub(
        r"\s+",
        " ",
        normalized,
    )


    # --------------------------------------------------------
    # Normalize repeated punctuation
    # --------------------------------------------------------

    normalized = re.sub(
        r"\.{2,}",
        ".",
        normalized,
    )

    normalized = re.sub(
        r"\?{2,}",
        "?",
        normalized,
    )

    normalized = re.sub(
        r"!{2,}",
        "!",
        normalized,
    )


    # --------------------------------------------------------
    # Remove spaces before punctuation
    # --------------------------------------------------------

    normalized = re.sub(
        r"\s+([,.!?])",
        r"\1",
        normalized,
    )


    # --------------------------------------------------------
    # Normalize spaces after punctuation
    # --------------------------------------------------------

    normalized = re.sub(
        r"([,.!?])([A-Za-z])",
        r"\1 \2",
        normalized,
    )


    # --------------------------------------------------------
    # Final cleanup
    # --------------------------------------------------------

    normalized = normalized.strip()


    return normalized
