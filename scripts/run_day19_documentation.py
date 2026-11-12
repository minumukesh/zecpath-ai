from pathlib import Path

# =========================================================
# DAY 19 - ATS DOCUMENTATION & KNOWLEDGE TRANSFER
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent
DOCS_DIR = PROJECT_ROOT / "docs" / "day19"

DOCS_DIR.mkdir(parents=True, exist_ok=True)


# =========================================================
# 1. ATS TECHNICAL DOCUMENTATION
# =========================================================

TECHNICAL_DOCUMENTATION = """
# Zecpath AI ATS Technical Documentation

## 1. Overview

Zecpath AI is an AI-powered job portal and automated hiring platform.

The ATS processes candidate resumes against job descriptions and produces
candidate analysis, ATS scores, rankings, and decision zones.

## 2. ATS Workflow

Resume
|
v
Text Extraction
|
v
Resume Section Segmentation
|
v
Skill Extraction
|
v
Experience Parsing
|
v
Education and Certification
|
v
Semantic Matching
|
v
ATS Scoring
|
v
Candidate Ranking
|
v
Shortlist / Review / Auto-Reject
|
v
API Integration
|
v
Optimization and Testing

## 3. Main ATS Components

### Resume Processing

- Resume text extraction
- Text cleaning
- Resume section classification
- Skill extraction
- Experience parsing
- Education parsing
- Certification parsing

### Job Description Processing

Important job information includes:

- Job title
- Required skills
- Preferred skills
- Experience requirements
- Education
- Responsibilities
- Certifications

### Semantic Matching

Semantic matching compares resume content with the target job description.

The result is used as one component of the ATS scoring system.

### ATS Scoring

The scoring engine combines:

- Skill Match
- Experience Relevance
- Education Alignment
- Semantic Similarity

Implementation:

src/ats_scoring/engine.py

### Candidate Ranking

The ranking system consumes ATS scores from the scoring stage.

It does not recalculate the ATS score.

Implementation:

src/candidate_ranking/engine.py

### ATS API

The REST API exposes ATS operations to backend systems.

Implementation:

src/ats_api/api.py

Main operations:

- Resume Upload
- Resume Parsing
- Resume Scoring
- Candidate Shortlisting
- Job Status

### ATS Optimization

Day 18 added an optimization layer without duplicating the existing
ATS scoring and ranking components.

Implementation:

src/ats_optimization/optimizer.py
src/ats_optimization/optimized_pipeline.py

## 4. Important Source Files

| Component | File |
|---|---|
| ATS Pipeline | src/ats_pipeline/pipeline.py |
| ATS Scoring | src/ats_scoring/engine.py |
| Candidate Ranking | src/candidate_ranking/engine.py |
| ATS API | src/ats_api/api.py |
| ATS Optimization | src/ats_optimization/optimized_pipeline.py |
| Optimization Utilities | src/ats_optimization/optimizer.py |
| ATS Testing Metrics | src/ats_testing/metrics.py |

## 5. Testing

The project automated test suite was verified with:

70 passed, 1 warning

The warning is a dependency-level Starlette/AnyIO deprecation warning.

## 6. Design Principle

Existing ATS components should be reused instead of creating duplicate
scoring, ranking, or processing implementations.
"""


# =========================================================
# 2. ATS ARCHITECTURE
# =========================================================

ARCHITECTURE_DOCUMENTATION = """
# Zecpath AI ATS Architecture

## 1. High-Level Architecture

Candidate Resume
        |
        v
Resume Extraction
        |
        v
Resume Section Segmentation
        |
        +-------------------+
        |         |         |
        v         v         v
     Skills   Experience  Education
        |         |         |
        +---------+---------+
                  |
                  v
          Candidate Analysis
                  |
                  v
          Semantic Matching
                  ^
                  |
          Job Description
                  |
                  v
           Job Profile
                  |
                  v
           ATS Scoring
                  |
                  v
        Candidate Ranking
                  |
          +-------+-------+
          |       |       |
          v       v       v
      SHORTLIST REVIEW AUTO-REJECT

## 2. Processing Architecture

Resume
  |
  v
Text Extraction
  |
  v
Section Segmentation
  |
  +----> Skill Extraction
  |
  +----> Experience Parsing
  |
  +----> Education & Certification
  |
  v
Candidate Analysis
  |
  v
Semantic Matching
  |
  v
Day 13 ATS Scoring
  |
  v
Day 14 Candidate Ranking
  |
  v
Decision Zone

## 3. API Architecture

Backend System
      |
      v
REST API
      |
      +----> Resume Upload
      |
      +----> Resume Parsing
      |
      +----> Resume Scoring
      |
      +----> Shortlisting
      |
      +----> Job Status
      |
      v
ATS Pipeline
      |
      v
ATS Processing
      |
      v
Scoring
      |
      v
Ranking
      |
      v
ATS Result

## 4. Optimization Architecture

Resume + Job Description
          |
          v
Optimized ATS Pipeline
          |
          v
Efficient Extraction
          |
          v
Resume Cleaning
          |
          v
Entity Detection
          |
          v
Existing ATS Pipeline
          |
          v
Existing ATS Scoring
          |
          v
Existing Candidate Ranking
          |
          v
ATS Result

## 5. Architectural Principle

Day 18 optimization is an additional processing layer.

It does not replace or duplicate the existing ATS scoring and ranking
components.
"""


# =========================================================
# 3. ATS SCORING LOGIC
# =========================================================

SCORING_DOCUMENTATION = """
# Zecpath AI ATS Scoring Logic

## 1. Purpose

The ATS scoring engine provides a transparent and explainable candidate
score.

Implementation:

src/ats_scoring/engine.py

## 2. Scoring Components

The ATS score uses four components:

1. Skill Match
2. Experience Relevance
3. Education Alignment
4. Semantic Similarity

## 3. Role-Based Weights

| Role | Skills | Experience | Education | Semantic |
|---|---:|---:|---:|---:|
| Data Analyst | 40% | 25% | 15% | 20% |
| Software Developer | 45% | 30% | 10% | 15% |
| ML Engineer | 45% | 30% | 10% | 15% |
| Business Analyst | 45% | 30% | 10% | 15% |
| Default | 40% | 25% | 15% | 20% |

## 4. Formula

Each component is normalized to a value between 0 and 1.

Weighted Score =
Sum of (Normalized Component Score x Component Weight)

The weighted result is converted to a 0-100 ATS score.

## 5. Missing Data

The scoring engine handles missing information.

Rules:

- Missing or invalid values are normalized safely.
- Missing components are recorded.
- Missing components are excluded from active weighting.
- Remaining weights are normalized.
- If all components are missing, the ATS score becomes 0.

## 6. Day 13 Classification

| ATS Score | Classification |
|---:|---|
| 85-100 | Excellent Match |
| 70-84.99 | Strong Match |
| 50-69.99 | Moderate Match |
| 40-49.99 | Weak Match |
| Below 40 | Low Match |

## 7. Explainable Output

generate_candidate_score() returns:

- Candidate information
- Normalized component scores
- Percentage component scores
- Final ATS score
- Classification
- Role-specific weights
- Explanation
- Missing-data information

## 8. Day 14 Ranking Decision Logic

Day 14 consumes the ATS score produced by Day 13.

It does not recalculate the score.

Candidates are sorted by ATS score in descending order.

### Decision Thresholds

| Score | Decision |
|---:|---|
| >= 70 | SHORTLIST |
| 50-69.99 | REVIEW |
| < 50 | AUTO-REJECT |

## 9. Complete Flow

Candidate Data
|
v
Component Analysis
|
v
Normalize Components
|
v
Select Role Weights
|
v
Weighted Score
|
v
ATS Score
|
v
Day 13 Classification
|
v
Day 14 Ranking
|
v
Decision Zone
|
v
SHORTLIST / REVIEW / AUTO-REJECT

## 10. Source Files

ATS scoring:

src/ats_scoring/engine.py

Candidate ranking:

src/candidate_ranking/engine.py

Scoring tests:

tests/ats_tests/test_ats_scoring.py

Ranking tests:

tests/ranking_tests/test_candidate_ranking.py
"""


# =========================================================
# 4. TROUBLESHOOTING NOTES
# =========================================================

TROUBLESHOOTING_DOCUMENTATION = """
# Zecpath AI ATS Troubleshooting Guide

## 1. Full Test Suite

Run:

python -m pytest -v

Verified project result:

70 passed, 1 warning

If a test fails, inspect the first failing test before modifying code.

## 2. Invalid File Type

Run:

python -m pytest -v tests/api_tests/test_ats_api.py::TestATSAPI::test_invalid_file_type

Unsupported resume file types should return:

415 Unsupported Media Type

Implementation:

src/ats_api/api.py

## 3. Resume Not Found

If the API returns:

RESUME_NOT_FOUND

check whether the resume ID exists in the API resume store.

Upload the resume before attempting parse or score operations.

## 4. Job Not Found

If scoring returns:

JOB_NOT_FOUND

check the requested job ID.

The current API contains:

JOB-001

## 5. Unexpected ATS Score

Check:

- Skill Match
- Experience Relevance
- Education Alignment
- Semantic Similarity

Then verify the selected role.

Implementation:

src/ats_scoring/engine.py

## 6. Unexpected Candidate Decision

Day 13 classification and Day 14 decision are different stages.

Flow:

ATS Score
|
v
Day 13 Classification
|
v
Day 14 Decision

Day 14 thresholds:

>= 70       SHORTLIST
50-69.99    REVIEW
< 50        AUTO-REJECT

## 7. Day 17 Mismatch

Day 17 compares AI decisions with manually expected decisions.

Mismatch cases should be recorded instead of silently changing expected
values.

Report:

outputs/day17/day17_ats_testing_report.json

## 8. Optimization Issues

Day 18 files:

src/ats_optimization/optimizer.py
src/ats_optimization/optimized_pipeline.py
run_day18_optimization.py

Run:

python -m pytest -v tests/optimization_tests/test_ats_optimization.py

## 9. Performance Investigation

Day 18 generated:

outputs/day18/day18_performance_report.json

Use the benchmark report when investigating performance changes.

## 10. Import Errors

If Python reports:

ModuleNotFoundError

check:

1. The command is being run from the project root.
2. The virtual environment is activated.
3. The referenced module exists.
4. Required package files are present.

## 11. Safe Debugging Rule

Before changing an existing ATS component:

1. Run the relevant test.
2. Identify the failing component.
3. Inspect the implementation.
4. Make the smallest necessary change.
5. Run the targeted test.
6. Run the complete test suite.

Avoid creating duplicate scoring, ranking, or pipeline implementations.
"""


# =========================================================
# 5. DEVELOPER GUIDE
# =========================================================

DEVELOPER_GUIDE = """
# Zecpath AI ATS Developer Guide

## 1. Purpose

This guide explains how a developer can understand, run, test, and extend
the Zecpath AI ATS system.

The ATS should be extended by reusing existing components rather than
creating duplicate implementations.

## 2. Activate Environment

Windows PowerShell:

.\\venv\\Scripts\\Activate.ps1

## 3. Run Full Test Suite

From the project root:

python -m pytest -v

Verified result:

70 passed, 1 warning

## 4. Main Development Areas

### ATS Pipeline

src/ats_pipeline/pipeline.py

Coordinates resume extraction, job-description processing, candidate
analysis, semantic matching, ATS scoring, and ranking.

### ATS Scoring

src/ats_scoring/engine.py

Used for:

- scoring components
- role weights
- score normalization
- classifications
- explainable score output

### Candidate Ranking

src/candidate_ranking/engine.py

Used for:

- candidate sorting
- rank generation
- shortlist
- review
- auto-reject
- top candidate selection

### API

src/ats_api/api.py

Used for:

- resume upload
- resume parsing
- resume scoring
- job status
- shortlisting

### Optimization

src/ats_optimization/optimizer.py
src/ats_optimization/optimized_pipeline.py

Used for:

- extraction efficiency
- resume cleaning
- lightweight entity detection
- memory-friendly processing

## 5. Development Workflow

Understand Requirement
|
v
Locate Existing Component
|
v
Inspect Current Implementation
|
v
Reuse Existing Logic
|
v
Make Small Change
|
v
Run Targeted Test
|
v
Run Full Test Suite
|
v
Document the Change

## 6. Adding a New ATS Feature

Before creating a new module:

1. Search the existing source tree.
2. Check whether the functionality already exists.
3. Reuse the existing pipeline where possible.
4. Keep scoring and ranking centralized.
5. Add tests for new behaviour.
6. Update technical documentation.

## 7. Scoring Extension Rule

Do not create a second scoring engine.

ATS scoring changes should remain connected to:

src/ats_scoring/engine.py

## 8. Ranking Extension Rule

Do not recalculate ATS scores inside the ranking layer.

Ranking consumes the score generated by Day 13.

Day 13 ATS Score
|
v
Day 14 Ranking
|
v
Decision Zone

## 9. API Extension Rule

New API operations should follow the existing API structure and response
contracts.

API processing should reuse the existing ATS pipeline.

## 10. Testing Before Commit

Run:

python -m pytest -v

Then run the relevant targeted test for the modified component.

Do not commit a change that breaks previously passing tests.

## 11. Documentation Rule

When an ATS component changes, update:

- technical documentation
- architecture documentation if the flow changes
- scoring documentation if scoring changes
- troubleshooting notes if a new failure mode is introduced

## 12. Knowledge Transfer Summary

Resume
|
v
Extraction
|
v
Segmentation
|
v
Skill / Experience / Education / Certification
|
v
Semantic Matching
|
v
ATS Scoring
|
v
Ranking
|
v
Shortlist / Review / Auto-Reject
|
v
API
|
v
Optimization
|
v
Testing
"""


# =========================================================
# DOCUMENT LIST
# =========================================================

DOCUMENTS = {
    "ATS_TECHNICAL_DOCUMENTATION.md": TECHNICAL_DOCUMENTATION,
    "ATS_ARCHITECTURE.md": ARCHITECTURE_DOCUMENTATION,
    "ATS_SCORING_LOGIC.md": SCORING_DOCUMENTATION,
    "TROUBLESHOOTING.md": TROUBLESHOOTING_DOCUMENTATION,
    "DEVELOPER_GUIDE.md": DEVELOPER_GUIDE,
}


# =========================================================
# WRITE DOCUMENTS
# =========================================================

def write_documents():
    print("=" * 70)
    print("DAY 19 - ATS DOCUMENTATION & KNOWLEDGE TRANSFER")
    print("=" * 70)

    for filename, content in DOCUMENTS.items():
        path = DOCS_DIR / filename

        path.write_text(
            content.strip() + "\n",
            encoding="utf-8"
        )

        print(f"[CREATED] {path}")


# =========================================================
# VERIFY EXISTING ATS COMPONENTS
# =========================================================

def verify_existing_components():
    print()
    print("-" * 70)
    print("VERIFYING EXISTING ATS COMPONENTS")
    print("-" * 70)

    required_files = [
        "src/ats_pipeline/pipeline.py",
        "src/ats_scoring/engine.py",
        "src/candidate_ranking/engine.py",
        "src/ats_api/api.py",
        "src/ats_optimization/optimizer.py",
        "src/ats_optimization/optimized_pipeline.py",
    ]

    missing = []

    for relative_path in required_files:
        path = PROJECT_ROOT / relative_path

        if path.exists():
            print(f"[OK]      {relative_path}")
        else:
            print(f"[MISSING] {relative_path}")
            missing.append(relative_path)

    return missing


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    write_documents()

    missing_files = verify_existing_components()

    print()
    print("=" * 70)

    if missing_files:
        print("DOCUMENTATION GENERATED WITH WARNINGS")
        print()
        print("Missing files:")

        for item in missing_files:
            print(f" - {item}")
    else:
        print("DAY 19 DOCUMENTATION GENERATED SUCCESSFULLY")
        print()
        print("Deliverables:")
        print("1. ATS Technical Documentation")
        print("2. Architecture Documentation")
        print("3. ATS Scoring Logic")
        print("4. Troubleshooting Notes")
        print("5. Developer Guide")

    print()
    print(f"Output directory: {DOCS_DIR}")
    print("=" * 70)