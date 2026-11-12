# Day 7 – AI Data Pipeline & Storage Design

## 1. AI Data Pipeline

The Zecpath AI data pipeline defines how data moves from resume and job description inputs through AI processing stages until the final hiring decision.

### 1.1 Overall Pipeline

```text
Candidate
    |
    v
Resume Upload
    |
    v
Resume Storage
    |
    v
Resume Parser
    |
    v
Candidate Profile
    |
    |----------------------|
    |                      |
    v                      v
Candidate Profile      Job Profile
    |                  (from Day 6 JD Parser)
    |                      |
    |----------+-----------|
               |
               v
       AI Matching / ATS
               |
               v
          ATS Score
               |
               v
        AI Screening
               |
               v
       Screening Report
               |
               v
        AI Interview
               |
               v
      Interview Results
               |
               v
       Hiring Decision