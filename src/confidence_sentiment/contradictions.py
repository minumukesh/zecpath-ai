import re

CONTRADICTION_PATTERNS = [
    (
        r"\bi have experience\b",
        r"\bi have no experience\b",
    ),
    (
        r"\bi am available\b",
        r"\bi am not available\b",
    ),
    (
        r"\bi can join immediately\b",
        r"\bi cannot join immediately\b",
    ),
    (
        r"\bi know\b",
        r"\bi do not know\b",
    ),
]


def detect_contradictions(responses):
    normalized = [
        str(response or "").strip().lower()
        for response in responses
    ]

    findings = []

    for index, first in enumerate(normalized):
        for second_index in range(
            index + 1,
            len(normalized)
        ):
            second = normalized[second_index]

            for positive_pattern, negative_pattern in CONTRADICTION_PATTERNS:
                first_positive = bool(
                    re.search(positive_pattern, first)
                )
                first_negative = bool(
                    re.search(negative_pattern, first)
                )
                second_positive = bool(
                    re.search(positive_pattern, second)
                )
                second_negative = bool(
                    re.search(negative_pattern, second)
                )

                if (
                    first_positive and second_negative
                ) or (
                    first_negative and second_positive
                ):
                    findings.append({
                        "response_index_1": index,
                        "response_index_2": second_index,
                        "response_1": responses[index],
                        "response_2": responses[second_index],
                        "status": "POTENTIAL_CONTRADICTION",
                    })

    return findings
