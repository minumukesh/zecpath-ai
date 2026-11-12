import re
from datetime import date

from .normalizer import normalize_text, normalize_company, normalize_title
from .role_dictionary import normalize_role


MONTHS = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}

ROLE_KEYWORDS = [
    "analyst",
    "developer",
    "engineer",
    "manager",
    "consultant",
    "intern",
    "scientist",
    "administrator",
    "specialist",
    "associate",
    "executive",
    "lead",
    "architect",
]


def parse_duration(text):
    """Extract start and end dates from an employment range."""

    pattern = re.compile(
        r"(?P<sm>[A-Za-z]+)\s+(?P<sy>\d{4})\s*-\s*"
        r"(?:(?P<em>[A-Za-z]+)\s+(?P<ey>\d{4})|(?P<present>Present|Current))",
        re.IGNORECASE,
    )

    match = pattern.search(text)

    if match:
        sm = MONTHS.get(match.group("sm").lower())

        if not sm:
            return None, None

        start = date(
            int(match.group("sy")),
            sm,
            1,
        )

        if match.group("present"):
            end = date.today().replace(day=1)
        else:
            em = MONTHS.get(match.group("em").lower())

            if not em:
                return None, None

            end = date(
                int(match.group("ey")),
                em,
                1,
            )

        return start, end

    year_pattern = re.compile(
        r"\b(20\d{2})\s*-\s*(20\d{2}|Present|Current)\b",
        re.IGNORECASE,
    )

    match = year_pattern.search(text)

    if match:
        start = date(
            int(match.group(1)),
            1,
            1,
        )

        if match.group(2).lower() in {
            "present",
            "current",
        }:
            end = date.today().replace(day=1)
        else:
            end = date(
                int(match.group(2)),
                12,
                1,
            )

        return start, end

    return None, None


def calculate_months(start, end):
    if not start or not end:
        return 0

    return max(
        0,
        (end.year - start.year) * 12
        + end.month
        - start.month
        + 1,
    )


def is_job_title(line):
    lower = line.lower()

    return any(
        keyword in lower
        for keyword in ROLE_KEYWORDS
    )


def find_company(lines, title_index):
    for index in range(
        title_index + 1,
        min(title_index + 4, len(lines)),
    ):
        candidate = lines[index].strip()

        if not candidate:
            continue

        if parse_duration(candidate)[0]:
            continue

        if is_job_title(candidate):
            continue

        return normalize_company(candidate)

    return "Unknown Company"


def parse_experience(text):
    """Extract structured professional experience."""

    text = normalize_text(text)

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    experiences = []

    for index, line in enumerate(lines):

        if not is_job_title(line):
            continue

        title = normalize_title(line)

        start = None
        end = None

        for offset in range(4):

            position = index + offset

            if position >= len(lines):
                break

            found_start, found_end = parse_duration(
                lines[position]
            )

            if found_start:
                start = found_start
                end = found_end
                break

        company = find_company(
            lines,
            index,
        )

        months = calculate_months(
            start,
            end,
        )

        experiences.append(
            {
                "company": company,
                "job_title": title,
                "canonical_role": normalize_role(title),
                "start_date": (
                    start.isoformat()
                    if start
                    else None
                ),
                "end_date": (
                    end.isoformat()
                    if end
                    else None
                ),
                "duration_months": months,
                "duration_years": round(
                    months / 12,
                    2,
                ),
            }
        )

    return deduplicate_experiences(experiences)


def deduplicate_experiences(experiences):
    unique = []
    seen = set()

    for experience in experiences:

        key = (
            experience["company"].lower(),
            experience["job_title"].lower(),
            experience["start_date"],
            experience["end_date"],
        )

        if key not in seen:
            seen.add(key)
            unique.append(experience)

    return unique


def calculate_total_experience(experiences):
    """Calculate total experience without double-counting overlaps."""

    intervals = []

    for experience in experiences:

        if not experience["start_date"]:
            continue

        if not experience["end_date"]:
            continue

        start = date.fromisoformat(
            experience["start_date"]
        )

        end = date.fromisoformat(
            experience["end_date"]
        )

        intervals.append((start, end))

    if not intervals:
        return {
            "total_months": 0,
            "total_years": 0.0,
        }

    intervals.sort()

    merged = []

    current_start, current_end = intervals[0]

    for start, end in intervals[1:]:

        if start <= current_end:

            if end > current_end:
                current_end = end

        else:
            merged.append(
                (current_start, current_end)
            )

            current_start = start
            current_end = end

    merged.append(
        (current_start, current_end)
    )

    total_months = sum(
        calculate_months(start, end)
        for start, end in merged
    )

    return {
        "total_months": total_months,
        "total_years": round(
            total_months / 12,
            2,
        ),
    }


def detect_gaps(experiences):
    """Detect gaps between employment periods."""

    intervals = []

    for experience in experiences:

        if not experience["start_date"]:
            continue

        if not experience["end_date"]:
            continue

        intervals.append(
            (
                date.fromisoformat(
                    experience["start_date"]
                ),
                date.fromisoformat(
                    experience["end_date"]
                ),
                experience["company"],
            )
        )

    intervals.sort()

    gaps = []

    for previous, current in zip(
        intervals,
        intervals[1:],
    ):

        previous_end = previous[1]
        current_start = current[0]

        if current_start > previous_end:

            gap_months = (
                (current_start.year - previous_end.year) * 12
                + current_start.month
                - previous_end.month
                - 1
            )

            if gap_months > 0:
                gaps.append(
                    {
                        "from": previous_end.isoformat(),
                        "to": current_start.isoformat(),
                        "gap_months": gap_months,
                    }
                )

    return gaps


def detect_overlaps(experiences):
    """Detect overlapping employment periods."""

    overlaps = []

    for i, first in enumerate(experiences):

        if not first["start_date"] or not first["end_date"]:
            continue

        first_start = date.fromisoformat(
            first["start_date"]
        )

        first_end = date.fromisoformat(
            first["end_date"]
        )

        for second in experiences[i + 1:]:

            if not second["start_date"] or not second["end_date"]:
                continue

            second_start = date.fromisoformat(
                second["start_date"]
            )

            second_end = date.fromisoformat(
                second["end_date"]
            )

            if (
                first_start <= second_end
                and second_start <= first_end
            ):
                overlaps.append(
                    {
                        "role_1": first["job_title"],
                        "company_1": first["company"],
                        "role_2": second["job_title"],
                        "company_2": second["company"],
                    }
                )

    return overlaps
