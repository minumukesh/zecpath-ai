"""
Day 18 - ATS Optimization & Performance Tuning

Optimization utilities for:
- Faster text extraction
- Reduced repeated processing
- Better memory handling
- Noisy resume normalization
- Lightweight entity detection
"""

import re
import time
import unicodedata
from functools import lru_cache
from pathlib import Path


# ------------------------------------------------------------
# TEXT NORMALIZATION
# ------------------------------------------------------------

def normalize_resume_text(text):
    """
    Normalize noisy resume text before sending it through
    downstream ATS processing.
    """

    if not text:
        return ""

    # Unicode normalization
    text = unicodedata.normalize("NFKC", str(text))

    # Remove null/control characters
    text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", " ", text)

    # Normalize common separators
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove repeated punctuation
    text = re.sub(r"[•●▪■]+", " ", text)

    # Replace tabs and repeated spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Prevent excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove spaces around newlines
    text = re.sub(r" *\n *", "\n", text)

    return text.strip()


# ------------------------------------------------------------
# FAST TEXT EXTRACTION
# ------------------------------------------------------------

@lru_cache(maxsize=128)
def _read_text_file_cached(file_path, modified_time):
    """
    Cached TXT file reader.

    modified_time is included in the cache key so that
    modified files are automatically treated as new data.
    """

    path = Path(file_path)

    with path.open(
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:
        return file.read()


def fast_text_extraction(file_path):
    """
    Fast text extraction for TXT resumes.

    Existing PDF extraction remains available through the
    original ATS extraction system.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Resume not found: {file_path}")

    modified_time = path.stat().st_mtime_ns

    raw_text = _read_text_file_cached(
        str(path.resolve()),
        modified_time
    )

    return normalize_resume_text(raw_text)


# ------------------------------------------------------------
# LIGHTWEIGHT ENTITY DETECTION
# ------------------------------------------------------------

ENTITY_PATTERNS = {
    "email": re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    ),

    "phone": re.compile(
        r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b"
    ),

    "year": re.compile(
        r"\b(?:19|20)\d{2}\b"
    ),

    "experience": re.compile(
        r"\b\d+(?:\.\d+)?\+?\s*(?:years?|yrs?)\b",
        re.IGNORECASE
    ),
}


def detect_entities(text):
    """
    Lightweight regex-based entity detection.

    Returns only useful ATS entities and avoids unnecessary
    repeated parsing.
    """

    text = normalize_resume_text(text)

    return {
        "emails": sorted(set(
            ENTITY_PATTERNS["email"].findall(text)
        )),

        "phone_numbers": sorted(set(
            ENTITY_PATTERNS["phone"].findall(text)
        )),

        "years": sorted(set(
            ENTITY_PATTERNS["year"].findall(text)
        )),

        "experience_mentions": sorted(set(
            ENTITY_PATTERNS["experience"].findall(text)
        )),
    }


# ------------------------------------------------------------
# NOISY RESUME HANDLING
# ------------------------------------------------------------

def clean_noisy_resume(text):
    """
    Additional cleaning for resumes containing:
    - repeated spaces
    - broken lines
    - unusual Unicode characters
    - repeated separators
    - control characters
    """

    text = normalize_resume_text(text)

    # Remove decorative separators
    text = re.sub(
        r"[_=\-]{4,}",
        " ",
        text
    )

    # Remove repeated punctuation
    text = re.sub(
        r"([.!?,:;])\1+",
        r"\1",
        text
    )

    # Collapse spaces again after cleaning
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    return text.strip()


# ------------------------------------------------------------
# PERFORMANCE HELPERS
# ------------------------------------------------------------

def measure_execution_time(function, *args, **kwargs):
    """
    Measure execution time of a function.
    """

    start = time.perf_counter()

    result = function(*args, **kwargs)

    elapsed = time.perf_counter() - start

    return result, elapsed


def calculate_improvement(baseline_time, optimized_time):
    """
    Calculate percentage improvement.

    Positive value means the optimized operation took
    less time than the baseline.
    """

    if baseline_time <= 0:
        return 0.0

    return round(
        ((baseline_time - optimized_time) / baseline_time) * 100,
        2
    )


def get_cache_info():
    """
    Return cache statistics for performance reporting.
    """

    info = _read_text_file_cached.cache_info()

    return {
        "hits": info.hits,
        "misses": info.misses,
        "maxsize": info.maxsize,
        "current_size": info.currsize,
    }


def clear_cache():
    """
    Clear cached text extraction results.
    """

    _read_text_file_cached.cache_clear()


# ------------------------------------------------------------
# MEMORY-FRIENDLY BATCH PROCESSING
# ------------------------------------------------------------

def process_in_batches(items, process_function, batch_size=10):
    """
    Process items in small batches instead of creating
    large intermediate collections.

    This keeps memory usage controlled.
    """

    results = []

    for start in range(0, len(items), batch_size):
        batch = items[start:start + batch_size]

        for item in batch:
            results.append(process_function(item))

    return results
