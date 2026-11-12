# Day 44 - Interview API Specification

Base URL: `http://127.0.0.1:8000`
Content type: `application/json`

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | API health |
| GET | `/api/v1/interviews/technical/roles` | Supported technical roles |
| POST | `/api/v1/interviews/technical/blueprint` | Generate role-based blueprint |
| POST | `/api/v1/interviews/hr/evaluate` | Evaluate HR score input |

## Technical blueprint request
```json
{
  "role": "mern",
  "experience_years": 3
}
```

## HR evaluation request
```json
{
  "candidate_id": "HR001",
  "candidate_name": "Candidate A",
  "role": "Data Analyst",
  "scores": {
    "communication": 90,
    "role_understanding": 85,
    "problem_solving": 88,
    "professionalism": 92
  },
  "manager_feedback": "Good communication."
}
```

## Response and errors
Successful requests return JSON. Invalid input returns HTTP 400. Unknown endpoints return HTTP 404.

## HR scoring
Four equally weighted demonstration dimensions: communication 25%, role understanding 25%, problem solving 25%, professionalism 25%.
Weighted score = sum(component score x component weight).

| Score | Demonstration recommendation |
|---|---|
| 85-100 | STRONGLY_RECOMMEND |
| 70-84.99 | RECOMMEND |
| 50-69.99 | HOLD |
| Below 50 | NOT_RECOMMENDED |

These thresholds are demonstration settings, not validated hiring criteria.