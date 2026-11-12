# Day 44 - Developer Handbook

## Project files
- `src/interview_system/config.py`: roles, domains and score weights.
- `src/interview_system/technical_engine.py`: technical question selection and flow states.
- `src/interview_system/hr_engine.py`: HR scoring demonstration.
- `src/interview_system/api.py`: local HTTP API.

## Run demonstrations
```powershell
python run_day45_hr_demo.py
python run_day46_technical_demo.py
```

## Start API
```powershell
python -m src.interview_system.api
```

Open another terminal to test:
```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

## Technical blueprint request
```powershell
$body = @{ role = "mern"; experience_years = 3 } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/interviews/technical/blueprint" -Method POST -ContentType "application/json" -Body $body
```

## HR evaluation request
```powershell
$body = @{
 candidate_id = "HR001"
 candidate_name = "Candidate A"
 role = "Data Analyst"
 scores = @{
  communication = 90
  role_understanding = 85
  problem_solving = 88
  professionalism = 92
 }
 manager_feedback = "Good performance."
} | ConvertTo-Json -Depth 5
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/interviews/hr/evaluate" -Method POST -ContentType "application/json" -Body $body
```

The supplied API is a local demonstration, not a production-secured service.