# Zecpath AI Data Entity Design

## 1. Purpose

The purpose of this document is to define standardized data entities for the Zecpath AI-powered job portal and automated hiring platform.

The entities provide a common structure for representing candidates, jobs, skills, education, experience, and certifications.

This standardized structure allows the AI system to process resume and job description data consistently.

---

## 2. Candidate Profile

The Candidate Profile represents the structured information extracted from a candidate's resume.

### Candidate Profile Fields

| Field | Data Type | Description |
|---|---|---|
| candidate_id | String | Unique identifier for the candidate |
| name | String | Candidate's full name |
| email | String | Candidate's email address |
| phone | String | Candidate's contact number |
| location | String | Candidate's current location |
| summary | String | Professional summary |
| skills | Array | List of candidate skills |
| education | Array | Educational qualifications |
| experience | Array | Previous work experience |
| certifications | Array | Professional certifications |
| projects | Array | Projects completed by the candidate |

---

## 3. Job Profile

The Job Profile represents the structured information extracted from a job description.

### Job Profile Fields

| Field | Data Type | Description |
|---|---|---|
| job_id | String | Unique identifier for the job |
| job_title | String | Name of the position |
| company | String | Hiring organization |
| location | String | Job location |
| employment_type | String | Full-time, part-time, contract, internship, etc. |
| description | String | Overall job description |
| required_skills | Array | Mandatory skills |
| preferred_skills | Array | Additional preferred skills |
| experience | Object | Required experience range |
| education | Array | Required educational qualifications |
| responsibilities | Array | Major responsibilities |
| certifications | Array | Required or preferred certifications |

---

## 4. Skill Object

The Skill Object represents an individual technical or non-technical skill.

### Structure

```json
{
  "name": "Python",
  "category": "Technical",
  "proficiency": "Intermediate"
}