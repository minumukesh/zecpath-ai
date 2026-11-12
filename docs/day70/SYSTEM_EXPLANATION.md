# Day 70 - Zecpath AI System Explanation

## 1. Project Overview

Zecpath AI is an AI-powered recruitment platform designed to organize candidate evaluation and support the hiring workflow.

## 2. Architecture Overview

The high-level architecture includes:

1. Candidate and recruiter interfaces.
2. Frontend application.
3. Backend API services.
4. AI processing modules.
5. Database and data storage.
6. Recruiter decision-support workflow.

## 3. AI Module Responsibilities

### Resume Parsing

Extracts candidate information from resume documents.

### Skill Extraction

Identifies technical and professional skills.

### Experience Parsing

Structures candidate employment history and experience.

### Education and Certification Parsing

Identifies academic qualifications and certifications.

### Semantic Matching

Compares candidate information with job requirements using contextual relevance.

### ATS Scoring

Combines documented evaluation components into a candidate score.

### Candidate Ranking

Organizes candidates based on their generated ATS scores.

### Screening AI

Supports candidate screening against job requirements.

### Interview AI

Supports interview-related evaluation.

### Decision Support

Organizes evaluation evidence for recruiter review.

## 4. ATS Scoring Components

- Skill Match.
- Experience Relevance.
- Education Alignment.
- Semantic Similarity.

The exact weights and scoring behavior must be explained using the current source-code implementation.

## 5. Hiring Workflow

Job Posting
    |
Resume Submission
    |
Resume Parsing
    |
Candidate Profile
    |
Semantic Matching
    |
ATS Scoring
    |
Candidate Ranking
    |
Screening
    |
HR Interview
    |
Technical Interview
    |
Decision Support
    |
Recruiter Review
    |
Final Hiring Decision

## 6. Human Oversight

AI-generated evaluations should support recruiter decisions rather than replace human judgment.

## 7. System Limitations

- Synthetic demo data does not establish real-world model accuracy.
- Simulated ATS results are not production predictions.
- Production readiness requires integration, security, performance and deployment verification.
