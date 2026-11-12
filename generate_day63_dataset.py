import json
import csv
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path("data/day63_demo")

# ----------------------------------------------------------
# 1. JOB DESCRIPTIONS
# ----------------------------------------------------------

jobs = [
    {
        "job_id": "JOB-001",
        "job_title": "Data Analyst",
        "department": "Analytics",
        "required_skills": ["Python", "SQL", "Excel"],
        "preferred_skills": ["Power BI", "Statistics", "Pandas"],
        "minimum_experience": 0,
        "education": "Bachelor's Degree",
        "responsibilities": [
            "Analyze business data",
            "Prepare reports",
            "Create dashboards",
            "Identify business trends"
        ],
        "employment_type": "Full-time"
    },
    {
        "job_id": "JOB-002",
        "job_title": "Python Developer",
        "department": "Engineering",
        "required_skills": ["Python", "Flask", "SQL"],
        "preferred_skills": ["REST API", "Git", "Docker"],
        "minimum_experience": 1,
        "education": "Bachelor's Degree",
        "responsibilities": [
            "Develop Python applications",
            "Build REST APIs",
            "Maintain backend services",
            "Debug application issues"
        ],
        "employment_type": "Full-time"
    },
    {
        "job_id": "JOB-003",
        "job_title": "Business Analyst",
        "department": "Business Operations",
        "required_skills": [
            "Business Analysis",
            "Excel",
            "Communication"
        ],
        "preferred_skills": ["SQL", "Power BI", "Documentation"],
        "minimum_experience": 0,
        "education": "Bachelor's Degree",
        "responsibilities": [
            "Gather business requirements",
            "Analyze business processes",
            "Prepare reports",
            "Coordinate with stakeholders"
        ],
        "employment_type": "Full-time"
    }
]

# ----------------------------------------------------------
# 2. FICTIONAL CANDIDATES
# ----------------------------------------------------------

candidates = [
    {
        "candidate_id": "C001",
        "name": "Aarav Menon",
        "job_id": "JOB-001",
        "experience": 2,
        "education": "BSc Computer Science",
        "skills": ["Python", "SQL", "Excel", "Power BI", "Pandas"],
        "quality": "high",
        "summary": "Data Analyst with experience in reporting and dashboard development.",
        "projects": ["Sales Dashboard", "Customer Data Analysis"],
        "screening": "I use SQL to extract data and Python for analysis. I use Power BI to communicate findings.",
        "hr_answer": "I enjoy solving business problems using data and presenting clear insights.",
        "technical_answer": "I use pandas for cleaning data, SQL for querying databases, and Power BI for visualization.",
        "ats_score": 91.5
    },
    {
        "candidate_id": "C002",
        "name": "Diya Nair",
        "job_id": "JOB-001",
        "experience": 0,
        "education": "BSc Statistics",
        "skills": ["Python", "Excel", "Statistics", "SQL"],
        "quality": "medium",
        "summary": "Recent graduate interested in data analytics.",
        "projects": ["Student Performance Analysis"],
        "screening": "I have academic experience in statistics and basic Python analysis.",
        "hr_answer": "I am interested in learning and applying analytical methods to real business problems.",
        "technical_answer": "I use Python libraries to clean data and calculate descriptive statistics.",
        "ats_score": 78.0
    },
    {
        "candidate_id": "C003",
        "name": "Rahul Varma",
        "job_id": "JOB-001",
        "experience": 1,
        "education": "BCA",
        "skills": ["Excel", "Power BI", "Communication"],
        "quality": "low",
        "summary": "Looking for an opportunity in analytics.",
        "projects": [],
        "screening": "I have worked with spreadsheets and created basic reports.",
        "hr_answer": "I want to improve my analytical and technical skills.",
        "technical_answer": "I use Excel formulas and charts to summarize information.",
        "ats_score": 42.0
    },
    {
        "candidate_id": "C004",
        "name": "Meera Krishnan",
        "job_id": "JOB-002",
        "experience": 3,
        "education": "BTech Computer Science",
        "skills": ["Python", "Flask", "SQL", "REST API", "Git", "Docker"],
        "quality": "high",
        "summary": "Python backend developer experienced in API development.",
        "projects": ["Inventory API", "Employee Management System"],
        "screening": "I have developed Flask APIs and integrated relational databases.",
        "hr_answer": "I enjoy backend development and collaborating with teams to deliver reliable applications.",
        "technical_answer": "I design Flask routes, validate requests, handle exceptions, and use SQL databases for persistence.",
        "ats_score": 94.0
    },
    {
        "candidate_id": "C005",
        "name": "Arjun Das",
        "job_id": "JOB-002",
        "experience": 1,
        "education": "BSc Computer Science",
        "skills": ["Python", "SQL", "Git"],
        "quality": "medium",
        "summary": "Junior Python developer with academic project experience.",
        "projects": ["Library Management System"],
        "screening": "I have used Python and SQL in college projects.",
        "hr_answer": "I am looking for a role where I can improve my development skills.",
        "technical_answer": "I understand Python functions, database queries, and basic application structure.",
        "ats_score": 66.0
    },
    {
        "candidate_id": "C006",
        "name": "Nisha Thomas",
        "job_id": "JOB-002",
        "experience": 0,
        "education": "MCA",
        "skills": ["Java", "HTML", "CSS", "Communication"],
        "quality": "low",
        "summary": "Computer applications postgraduate seeking a software role.",
        "projects": ["Portfolio Website"],
        "screening": "I have studied programming and web technologies.",
        "hr_answer": "I am interested in starting my career in software development.",
        "technical_answer": "I understand basic programming concepts and web page development.",
        "ats_score": 35.0
    },
    {
        "candidate_id": "C007",
        "name": "Ishita Pillai",
        "job_id": "JOB-003",
        "experience": 2,
        "education": "MBA",
        "skills": ["Business Analysis", "Excel", "Communication", "Power BI", "SQL"],
        "quality": "high",
        "summary": "Business Analyst with experience in reporting and stakeholder coordination.",
        "projects": ["Process Improvement Study", "Sales Reporting"],
        "screening": "I gather requirements, document processes, and analyze operational performance.",
        "hr_answer": "I communicate with stakeholders to understand problems and translate them into requirements.",
        "technical_answer": "I use Excel and SQL for analysis and Power BI to present business performance.",
        "ats_score": 90.0
    },
    {
        "candidate_id": "C008",
        "name": "Vishnu Raj",
        "job_id": "JOB-003",
        "experience": 0,
        "education": "BBA",
        "skills": ["Excel", "Communication", "Documentation"],
        "quality": "medium",
        "summary": "Business graduate interested in business analysis.",
        "projects": ["Market Research Assignment"],
        "screening": "I have experience preparing reports and documenting project requirements.",
        "hr_answer": "I enjoy understanding customer and business requirements.",
        "technical_answer": "I use Excel to organize data and prepare reports.",
        "ats_score": 64.0
    },
    {
        "candidate_id": "C009",
        "name": "Ananya Menon",
        "job_id": "JOB-001",
        "experience": 4,
        "education": "MSc Data Science",
        "skills": ["Python", "SQL", "Excel", "Pandas", "Statistics", "Power BI"],
        "quality": "high",
        "summary": "Data professional experienced in analytical reporting and statistical analysis.",
        "projects": ["Customer Segmentation", "Revenue Forecasting"],
        "screening": "I analyze large datasets, identify patterns, and communicate findings to business teams.",
        "hr_answer": "I focus on translating analytical findings into useful business recommendations.",
        "technical_answer": "I use pandas for preprocessing, SQL for data extraction, and statistical techniques for analysis.",
        "ats_score": 96.0
    },
    {
        "candidate_id": "C010",
        "name": "Kiran Joseph",
        "job_id": "JOB-002",
        "experience": 2,
        "education": "BTech IT",
        "skills": ["Python", "Flask", "SQL", "REST API"],
        "quality": "medium",
        "summary": "Backend developer familiar with Python application development.",
        "projects": ["Task Management API"],
        "screening": "I have created backend routes and connected applications to SQL databases.",
        "hr_answer": "I enjoy learning new technologies and working on backend systems.",
        "technical_answer": "I use Flask to create endpoints and SQL queries to retrieve and update records.",
        "ats_score": 82.0
    }
]

# ----------------------------------------------------------
# 3. RESUME FILES
# ----------------------------------------------------------

for c in candidates:
    resume = f"""RESUME

Candidate ID: {c['candidate_id']}
Name: {c['name']}
Target Role: {next(j['job_title'] for j in jobs if j['job_id'] == c['job_id'])}

PROFESSIONAL SUMMARY
{c['summary']}

EDUCATION
{c['education']}

WORK EXPERIENCE
{c['experience']} years

TECHNICAL AND PROFESSIONAL SKILLS
{', '.join(c['skills'])}

PROJECTS
{chr(10).join('- ' + p for p in c['projects']) if c['projects'] else 'No projects listed'}

NOTE
This is a fictional demonstration resume created for software testing.
"""

    (ROOT / "resumes" / f"{c['candidate_id']}_resume.txt").write_text(
        resume, encoding="utf-8"
    )

# ----------------------------------------------------------
# 4. CANDIDATE PROFILES
# ----------------------------------------------------------

profiles = []

for c in candidates:
    profiles.append({
        "candidate_id": c["candidate_id"],
        "name": c["name"],
        "job_id": c["job_id"],
        "education": c["education"],
        "experience_years": c["experience"],
        "skills": c["skills"],
        "projects": c["projects"],
        "resume_quality": c["quality"],
        "source": "synthetic_demo"
    })

# ----------------------------------------------------------
# 5. CANDIDATE SCREENING RESPONSES
# ----------------------------------------------------------

screening = []

for c in candidates:
    screening.append({
        "candidate_id": c["candidate_id"],
        "job_id": c["job_id"],
        "question": "Describe your relevant skills and experience.",
        "response": c["screening"],
        "response_type": "text",
        "source": "simulated_candidate_response"
    })

# ----------------------------------------------------------
# 6. SIMULATED ATS RESULTS
# ----------------------------------------------------------

ats_results = []

for c in candidates:
    score = c["ats_score"]

    if score >= 70:
        decision = "SHORTLIST"
    elif score >= 50:
        decision = "REVIEW"
    else:
        decision = "AUTO-REJECT"

    ats_results.append({
        "candidate_id": c["candidate_id"],
        "job_id": c["job_id"],
        "ats_score": score,
        "decision": decision,
        "score_type": "simulated",
        "model_version": "demo-ats-v1.0",
        "explanation": "Synthetic demonstration result. Not generated by the production ATS engine."
    })

# ----------------------------------------------------------
# 7. SIMULATED SCREENING OUTPUTS
# ----------------------------------------------------------

screening_outputs = []

for c in candidates:
    score = c["ats_score"]

    screening_outputs.append({
        "candidate_id": c["candidate_id"],
        "job_id": c["job_id"],
        "screening_status": (
            "PASSED" if score >= 70 else
            "MANUAL_REVIEW" if score >= 50 else
            "NOT_QUALIFIED"
        ),
        "screening_response": c["screening"],
        "skills_identified": c["skills"],
        "review_required": score < 70,
        "source": "simulated"
    })

# ----------------------------------------------------------
# 8. INTERVIEW RESPONSES
# ----------------------------------------------------------

interviews = []

for c in candidates:
    interviews.append({
        "candidate_id": c["candidate_id"],
        "job_id": c["job_id"],
        "interview_type": "HR",
        "question": "Why are you interested in this role?",
        "answer": c["hr_answer"],
        "evaluation_status": "SIMULATED"
    })

    interviews.append({
        "candidate_id": c["candidate_id"],
        "job_id": c["job_id"],
        "interview_type": "TECHNICAL",
        "question": "Explain how you would use your skills in this role.",
        "answer": c["technical_answer"],
        "evaluation_status": "SIMULATED"
    })

# ----------------------------------------------------------
# 9. COMPLETE HIRING PIPELINE
# ----------------------------------------------------------

pipeline = []

for c in candidates:
    score = c["ats_score"]

    pipeline.append({
        "candidate_id": c["candidate_id"],
        "job_id": c["job_id"],
        "resume_submitted": True,
        "resume_parsed": True,
        "ats_score": score,
        "ats_decision": (
            "SHORTLIST" if score >= 70 else
            "REVIEW" if score >= 50 else
            "AUTO-REJECT"
        ),
        "screening_completed": True,
        "interview_completed": score >= 70,
        "final_status": (
            "INTERVIEW_COMPLETED_PENDING_HR_REVIEW"
            if score >= 70 else
            "PENDING_MANUAL_REVIEW"
            if score >= 50 else
            "CLOSED_AT_INITIAL_SCREENING"
        ),
        "data_type": "synthetic_demo"
    })

# ----------------------------------------------------------
# 10. SAVE JSON FILES
# ----------------------------------------------------------

def save_json(folder, filename, data):
    path = ROOT / folder / filename
    path.write_text(
        json.dumps(data, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

save_json("job_descriptions", "job_descriptions.json", jobs)
save_json("candidate_profiles", "candidate_profiles.json", profiles)
save_json("candidate_responses", "candidate_responses.json", screening)
save_json("ats_results", "ats_results.json", ats_results)
save_json("screening_outputs", "screening_outputs.json", screening_outputs)
save_json("interview_responses", "interview_responses.json", interviews)

save_json("", "hiring_pipeline.json", pipeline)

# ----------------------------------------------------------
# 11. SAVE CSV DATASETS
# ----------------------------------------------------------

def save_csv(filename, rows):
    if not rows:
        return

    path = ROOT / filename

    fields = list(rows[0].keys())

    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()

        for row in rows:
            formatted = {
                key: json.dumps(value, ensure_ascii=False)
                if isinstance(value, (list, dict))
                else value
                for key, value in row.items()
            }
            writer.writerow(formatted)

save_csv("candidate_profiles.csv", profiles)
save_csv("ats_results.csv", ats_results)
save_csv("screening_outputs.csv", screening_outputs)
save_csv("hiring_pipeline.csv", pipeline)

# ----------------------------------------------------------
# 12. DEMO DATASET README
# ----------------------------------------------------------

readme = """# Zecpath AI - Day 63 Demo Dataset

## Purpose

This dataset provides fictional candidate and recruitment information
for demonstrating the Zecpath AI hiring workflow.

## Dataset Contents

- 10 fictional candidate resumes
- 3 job descriptions
- 10 structured candidate profiles
- 10 screening responses
- 10 simulated ATS results
- 10 simulated screening outputs
- 20 interview responses
- 10 end-to-end hiring pipeline records

## Candidate IDs

C001 to C010

## Job IDs

JOB-001: Data Analyst
JOB-002: Python Developer
JOB-003: Business Analyst

## Resume Quality

High, medium and low quality resumes are included to test different
resume completeness and information extraction scenarios.

## ATS Decision Thresholds

Score >= 70: SHORTLIST
Score >= 50 and below 70: REVIEW
Score below 50: AUTO-REJECT

## Important

All candidate names, resumes, responses and scores are fictional.

ATS results and screening outputs are simulated demonstration data.
They are not actual predictions from the production Zecpath AI models.

The dataset is designed for testing and demonstration, not real hiring.
"""

(ROOT / "README.md").write_text(readme, encoding="utf-8")

# ----------------------------------------------------------
# 13. DATASET SUMMARY
# ----------------------------------------------------------

summary = {
    "project": "Zecpath AI",
    "day": 63,
    "dataset_type": "Synthetic Demonstration Dataset",
    "created_at": datetime.now(timezone.utc).isoformat(),
    "candidate_count": len(candidates),
    "job_count": len(jobs),
    "resume_count": len(candidates),
    "candidate_response_count": len(screening),
    "ats_result_count": len(ats_results),
    "screening_output_count": len(screening_outputs),
    "interview_response_count": len(interviews),
    "pipeline_record_count": len(pipeline)
}

save_json("", "dataset_summary.json", summary)

print("\nDATA GENERATION COMPLETED")
print("-------------------------")
print("Candidates:", len(candidates))
print("Job descriptions:", len(jobs))
print("Resumes:", len(candidates))
print("Screening responses:", len(screening))
print("ATS results:", len(ats_results))
print("Screening outputs:", len(screening_outputs))
print("Interview responses:", len(interviews))
print("Pipeline records:", len(pipeline))
