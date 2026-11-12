"""
Day 18 - ATS Optimization Tests
"""

from pathlib import Path

from src.ats_optimization.optimizer import (
    normalize_resume_text,
    clean_noisy_resume,
    detect_entities,
    calculate_improvement,
)
from src.ats_optimization.optimized_pipeline import (
    OptimizedATSPipeline,
)


def test_text_normalization():
    text = "Python    SQL\tExcel\r\n\r\nPower BI"

    result = normalize_resume_text(text)

    assert "Python SQL Excel" in result
    assert "Power BI" in result


def test_noisy_resume_cleaning():
    text = """
    Arun   Kumar
    Python • • • SQL
    ----------------
    """

    result = clean_noisy_resume(text)

    assert "Arun Kumar" in result
    assert "Python" in result
    assert "SQL" in result


def test_entity_detection():
    text = """
    Email: arun@example.com
    Phone: 9876543210
    Experience: 3 years
    """

    result = detect_entities(text)

    assert "arun@example.com" in result["emails"]
    assert "9876543210" in result["phone_numbers"]
    assert "3 years" in result["experience_mentions"]


def test_improvement_calculation():
    result = calculate_improvement(
        1.0,
        0.5
    )

    assert result == 50.0


def test_optimized_pipeline_creation():
    pipeline = OptimizedATSPipeline()

    assert pipeline is not None
