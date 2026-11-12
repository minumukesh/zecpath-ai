# Day 59 - API Mapping Diagram

## 1. Overall Architecture

`	ext
Candidate / Recruiter
        |
        v
Frontend Application
        |
        v
Backend API Gateway
        |
        v
Authentication and Authorization
        |
        +---- Resume Parsing API ---- Background Worker
        |                                  |
        |                                  v
        |                               Database
        |
        +---- ATS Scoring API ----------> Database
        |
        +---- Screening AI API ---------> Database
        |
        +---- Interview AI API ---------> Database
        |
        +---- Decision AI API ----------> Database
                                           |
                                           v
                                     Backend Response
                                           |
                                           v
                                        Frontend
`",
",


`	ext
Candidate uploads resume
          |
          v
Backend validates request
          |
          v
Create processing job
          |
          v
Return HTTP 202 and job_id
          |
          v
Background worker processes resume
          |
          v
Resume Parsing AI
          |
          v
Store extracted information
          |
          v
Frontend checks processing status
`",
",


`	ext
Candidate submits answer
          |
          v
Frontend sends answer to backend
          |
          v
Backend validates request
          |
          v
Interview AI evaluates answer
          |
          v
Backend stores evaluation
          |
          v
Frontend receives score and feedback
`",
",


| API | Responsibility | Processing |
| --- | --- | --- |
| Resume Parsing | Extract resume information | Asynchronous |
| ATS Scoring | Match candidate and job | Synchronous |
| Screening AI | Evaluate screening responses | Synchronous |
| Interview AI | Evaluate interview answers | Synchronous |
| Decision AI | Generate hiring recommendation | Synchronous |

## 5. Security Boundary
Frontend communicates through the backend.
Internal AI services and database credentials must not be exposed to frontend applications.
