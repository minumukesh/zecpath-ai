# Zecpath AI System

## Overview

Zecpath AI is the Artificial Intelligence component of the Zecpath AI-Powered Job Portal and Automated Hiring Platform.

The AI system is designed with a modular architecture to support resume parsing, ATS evaluation, candidate screening, AI interviews, and candidate scoring.

## Project Structure

```text
ZECPATH-AI/
│
├── data/              # Datasets and sample input data
├── parsers/           # Resume and document parsing modules
├── ats_engine/        # Applicant Tracking System scoring logic
├── screening_ai/      # AI-based candidate screening
├── interview_ai/      # AI interview processing and evaluation
├── scoring/           # Candidate scoring and ranking modules
├── utils/             # Shared utilities and logging configuration
├── tests/             # Unit and integration tests
├── logs/              # Generated application logs
│
├── requirements.txt   # Python project dependencies
├── CONTRIBUTING.md    # Coding and documentation standards
└── README.md          # Project documentation
```

## Environment Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Testing

The project uses `pytest` for testing.

Run all tests using:

```bash
python -m pytest -v
```

## Logging

Zecpath AI uses Python's logging module to record important AI system activities.

The centralized logging configuration is located at:

```text
utils/logger.py
```

Generated logs are stored in:

```text
logs/zecpath_ai.log
```

Logging can be used to track activities such as:

- Resume parsing
- ATS processing
- Candidate screening
- Interview evaluation
- Candidate scoring
- System errors

## Code Standards

The project follows PEP 8 Python coding standards.

Detailed development and documentation guidelines are available in:

```text
CONTRIBUTING.md
```

## Technologies

- Python
- NumPy
- Pandas
- Scikit-learn
- Pytest
- Python-dotenv
- Git
- GitHub

## Project Status

Environment and repository foundation successfully configured for further development of the Zecpath AI system.