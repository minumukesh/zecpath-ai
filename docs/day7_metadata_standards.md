# Day 7 – Metadata Standards

## 1. Purpose

Metadata provides information about the identity, origin, processing history, version, and status of AI data within the Zecpath platform.

Metadata allows AI-generated results to be traced back to the candidate, job, application, model, and processing stage that produced them.

## 2. Standard Metadata Fields

| Field | Data Type | Example | Purpose |
|---|---|---|---|
| candidate_id | String | CAND-00125 | Identifies the candidate |
| job_id | String | JOB-00452 | Identifies the job |
| application_id | String | APP-00891 | Identifies the application |
| resume_id | String | RES-00981 | Identifies the resume |
| model_version | String | ATS-v1.0 | Identifies the AI model |
| pipeline_version | String | PIPE-v1.0 | Identifies the pipeline version |
| data_version | String | DATA-v1.0 | Identifies the data version |
| timestamp | DateTime | 2026-08-16T20:30:00+05:30 | Records processing time |
| processing_status | String | SUCCESS | Records processing status |
| source | String | candidate_upload | Identifies data source |
| created_at | DateTime | 2026-08-16T20:30:00+05:30 | Records creation time |
| updated_at | DateTime | 2026-08-16T20:35:00+05:30 | Records last update |

## 3. Metadata Example

```json
{
  "candidate_id": "CAND-00125",
  "job_id": "JOB-00452",
  "application_id": "APP-00891",
  "resume_id": "RES-00981",
  "model_version": "ATS-v1.0",
  "pipeline_version": "PIPE-v1.0",
  "data_version": "DATA-v1.0",
  "timestamp": "2026-08-16T20:30:00+05:30",
  "processing_status": "SUCCESS",
  "source": "candidate_upload",
  "created_at": "2026-08-16T20:30:00+05:30",
  "updated_at": "2026-08-16T20:35:00+05:30"
}