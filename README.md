# Zecpath AI System

An AI-powered recruitment and hiring automation system.

## Overview

Zecpath AI is the AI component of an automated job portal and recruitment platform. It supports multiple stages of the hiring lifecycle, including resume processing, candidate screening, ATS evaluation, AI-powered interviews, candidate scoring, and final hiring recommendations.

The system is designed to automate recruitment tasks and help organizations evaluate candidates through structured data processing, intelligent matching, and AI-assisted assessments.

## Key Features

- Resume extraction and classification
- Skill and experience extraction
- Job description parsing
- Semantic matching between candidates and job requirements
- ATS scoring and candidate ranking
- Candidate eligibility evaluation
- Fairness assessment
- AI-assisted interviews
- Technical and behavioral evaluation
- Interview scoring and summaries
- Final hiring recommendations
- API integration

## Technology Stack

- **Programming Language:** Python 3.13
- **API Framework:** FastAPI
- **Data Validation:** Pydantic
- **Natural Language Processing:** spaCy
- **Fuzzy Matching:** RapidFuzz
- **PDF Processing:** PyPDF
- **Word Document Processing:** python-docx
- **Schema Validation:** JSON Schema
- **Testing:** Pytest
- **ASGI Server:** Uvicorn

## Project Structure

```text
ZECPATH-AI/
│
├── ats_engine/          # ATS-related package
├── data/                # Project data and sample datasets
├── docs/                # Project documentation
├── interview_ai/        # Interview-related package
├── logs/                # Application logs
├── parsers/             # Resume and skill parsing utilities
├── scoring/             # Scoring-related package
├── screening_ai/        # Candidate screening package
├── schemas/             # Data and validation schemas
├── src/                 # Core application implementation
├── tests/               # Automated test cases
├── utils/               # Shared utility functions
│
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
