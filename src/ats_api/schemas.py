from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class UploadResponse(BaseModel):
    resume_id: str
    filename: str
    status: str
    message: str
    request_id: str


class ParseRequest(BaseModel):
    resume_id: str


class ParseResponse(BaseModel):
    job_id: str
    resume_id: str
    status: str
    message: str
    request_id: str


class ScoreRequest(BaseModel):
    resume_id: str
    job_id: str
    role: str = "Default"


class ScoreResponse(BaseModel):
    job_id: str
    resume_id: str
    status: str
    score: Optional[float] = None
    classification: Optional[str] = None
    request_id: str


class CandidateInput(BaseModel):
    candidate_id: str
    score: float = Field(..., ge=0.0, le=100.0)


class ShortlistRequest(BaseModel):
    candidates: List[CandidateInput]
    shortlist_threshold: float = Field(
        default=70.0,
        ge=0.0,
        le=100.0
    )
    review_threshold: float = Field(
        default=50.0,
        ge=0.0,
        le=100.0
    )


class CandidateDecision(BaseModel):
    candidate_id: str
    score: float
    decision: str


class ShortlistResponse(BaseModel):
    job_id: str
    status: str
    shortlisted: List[CandidateDecision]
    review: List[CandidateDecision]
    rejected: List[CandidateDecision]
    request_id: str


class JobStatusResponse(BaseModel):
    job_id: str
    job_type: str
    status: str
    created_at: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
