# Zecpath AI - PRD Implementation Map

## Product Goal

Zecpath AI is an AI-powered recruitment platform covering the hiring lifecycle from job creation through candidate evaluation, selection, offer generation and joining.

## PRD Parts

### Part 1: Phases 1-10
Foundation, AI ATS and AI voice screening.

### Part 2: Phases 11-25
AI HR video interview.

### Part 3: Phases 26-50
Second-round and technical interview.

### Part 4: Phases 51-75
Machine test and practical skill evaluation.

### Part 5: Phases 76-90
Final interview and salary negotiation.

### Part 6: Phases 91-100
Selection, offer letter and joining.

## Current Implemented ATS Foundation

src/resume_extraction/
    Resume text extraction foundation.

src/resume_section_classifier/
    Resume section classification.

src/skill_extraction/
    Skill extraction and normalization.

src/experience_parser/
    Experience parsing, role mapping and relevance.

src/education_certification/
    Education and certification parsing.

src/jd_parser/
    Job description parsing foundation.

src/semantic_matching/
    Candidate-job similarity using lightweight vector representations and cosine similarity.

src/ats_scoring/
    ATS candidate scoring and classification.

src/fairness_normalization/
    Sensitive-attribute masking and fairness-oriented normalization.

src/candidate_ranking/
    Candidate ranking and shortlist/review/reject decisions.

src/ats_api/
    FastAPI integration layer.

## Current Testing

tests/ats_tests/
tests/ranking_tests/
tests/fairness_tests/
tests/api_tests/

## Important Current-State Notes

The current implementation is a modular ATS foundation, not the complete 100-phase production platform.

Current semantic matching is lightweight vector-based matching rather than a transformer/LLM implementation.

The current Day 16 API uses a baseline keyword scoring implementation and should later be connected directly to the production ATS scoring pipeline.

The current Day 16 upload implementation supports .txt files. PDF/DOC/DOCX support is a future implementation requirement from the PRD.

Future development should add voice screening, video interviews, technical interviews, machine testing, final interviews, salary negotiation, offer generation, joining workflows, notifications, analytics, security and administration according to the PRD.
