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
