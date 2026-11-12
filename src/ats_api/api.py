import threading
import uuid
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from src.ats_api.job_manager import job_manager
from src.ats_api.logging_config import logger
from src.ats_api.schemas import (
    CandidateDecision,
    HealthResponse,
    JobStatusResponse,
    ParseRequest,
    ParseResponse,
    ScoreRequest,
    ScoreResponse,
    ShortlistRequest,
    ShortlistResponse,
    UploadResponse,
)

from src.ats_pipeline.pipeline import ATSPipeline

from src.candidate_ranking.engine import (
    generate_ranking_output,
)


# =========================================================
# APPLICATION
# =========================================================

app = FastAPI(
    title="Zecpath AI ATS API",
    version="2.0.0",
)


# =========================================================
# STORAGE
# =========================================================

RESUME_STORE = {}

UPLOAD_DIR = Path(
    "outputs/day16/uploads"
)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


JOB_DESCRIPTION_DIR = Path(
    "outputs/day16/job_descriptions"
)

JOB_DESCRIPTION_DIR.mkdir(
    parents=True,
    exist_ok=True
)


pipeline = ATSPipeline()


# =========================================================
# DEMO JOB DATA
# =========================================================

DEFAULT_JOB_DESCRIPTIONS = {
    "JOB-001": (
        "Data Analyst\n\n"
        "Required Skills:\n"
        "Python, SQL, Machine Learning, "
        "Data Analysis, Excel, Statistics\n\n"
        "Education:\n"
        "B.Tech, B.Sc, MCA, or equivalent\n\n"
        "Experience:\n"
        "Data analysis, reporting, dashboards, "
        "and business analytics."
    )
}


def get_job_description_path(job_id):
    job_id = job_id.upper()

    if job_id not in DEFAULT_JOB_DESCRIPTIONS:
        return None

    path = (
        JOB_DESCRIPTION_DIR
        / f"{job_id}.txt"
    )

    if not path.exists():
        path.write_text(
            DEFAULT_JOB_DESCRIPTIONS[job_id],
            encoding="utf-8",
        )

    return path


# =========================================================
# SUPPORTED FILE TYPES
# =========================================================

# Day 16 API test expects PDF uploads to be rejected
# with HTTP 415 Unsupported Media Type.
SUPPORTED_EXTENSIONS = {
    ".txt",
}


# =========================================================
# HELPERS
# =========================================================

def create_request_id():
    return str(uuid.uuid4())


def create_job(
    job_type,
    payload=None,
):
    """
    Create an asynchronous job using
    the existing JobManager.
    """

    return job_manager.create_job(
        job_type=job_type,
        payload=payload or {},
    )


def run_async(
    job_id,
    function,
):
    """
    Execute a job in a background thread.
    """

    def worker():

        try:

            job_manager.update_job(
                job_id,
                status="running",
            )

            result = function()

            job_manager.update_job(
                job_id,
                status="completed",
                result=result,
            )

        except Exception as exc:

            logger.exception(
                "Async job failed: %s",
                job_id,
            )

            job_manager.update_job(
                job_id,
                status="failed",
                error=str(exc),
            )

    thread = threading.Thread(
        target=worker,
        daemon=True,
    )

    thread.start()


# =========================================================
# HEALTH
# =========================================================

@app.get(
    "/api/v1/health",
    response_model=HealthResponse,
)
def health():

    return {
        "status": "healthy",
        "service": "zecpath-ai-ats",
        "version": "2.0.0",
    }


# =========================================================
# RESUME UPLOAD
# =========================================================

@app.post(
    "/api/v1/resumes/upload",
    response_model=UploadResponse,
)
async def upload_resume(
    file: UploadFile = File(...),
):

    request_id = create_request_id()

    extension = Path(
        file.filename or ""
    ).suffix.lower()

    # -----------------------------------------------------
    # FILE TYPE VALIDATION
    # -----------------------------------------------------

    if extension not in SUPPORTED_EXTENSIONS:

        return JSONResponse(
            status_code=415,
            content={
                "detail": {
                    "error_code": "UNSUPPORTED_FILE_TYPE",
                    "message": (
                        "Unsupported resume file type. "
                        "Only TXT files are supported."
                    ),
                    "request_id": request_id,
                }
            },
        )

    # -----------------------------------------------------
    # CREATE RESUME ID
    # -----------------------------------------------------

    resume_id = str(
        uuid.uuid4()
    )

    stored_path = (
        UPLOAD_DIR
        / f"{resume_id}{extension}"
    )

    # -----------------------------------------------------
    # READ FILE
    # -----------------------------------------------------

    content = await file.read()

    stored_path.write_bytes(
        content
    )

    # -----------------------------------------------------
    # STORE RESUME INFORMATION
    # -----------------------------------------------------

    RESUME_STORE[resume_id] = {
        "resume_id": resume_id,
        "filename": file.filename,
        "path": str(stored_path),
        "extension": extension,
    }

    logger.info(
        "Resume uploaded: %s",
        resume_id,
    )

    # -----------------------------------------------------
    # RESPONSE
    # -----------------------------------------------------

    return {
        "resume_id": resume_id,
        "filename": file.filename,
        "status": "uploaded",
        "message": "Resume uploaded successfully.",
        "request_id": request_id,
    }


# =========================================================
# RESUME PARSING
# =========================================================

@app.post(
    "/api/v1/resumes/{resume_id}/parse",
    response_model=ParseResponse,
)
def parse_resume(
    resume_id: str,
    request: ParseRequest,
):

    request_id = create_request_id()

    resume = RESUME_STORE.get(
        resume_id
    )

    # -----------------------------------------------------
    # RESUME NOT FOUND
    # -----------------------------------------------------

    if resume is None:

        return JSONResponse(
            status_code=404,
            content={
                "detail": {
                    "error_code": "RESUME_NOT_FOUND",
                    "message": "Resume not found.",
                    "request_id": request_id,
                }
            },
        )

    # -----------------------------------------------------
    # CREATE ASYNC JOB
    # -----------------------------------------------------

    job_id = create_job(
        job_type="resume_parse",
        payload={
            "resume_id": resume_id,
        },
    )

    # -----------------------------------------------------
    # BACKGROUND PARSING
    # -----------------------------------------------------

    def parse_worker():

        text = pipeline.extract_resume_text(
            resume["path"]
        )

        return {
            "resume_id": resume_id,
            "filename": resume["filename"],
            "text_length": len(text),
            "text_preview": text[:500],
        }

    run_async(
        job_id,
        parse_worker,
    )

    # -----------------------------------------------------
    # RESPONSE
    # -----------------------------------------------------

    return {
        "job_id": job_id,
        "resume_id": resume_id,
        "status": "queued",
        "message": "Resume parsing job queued.",
        "request_id": request_id,
    }


# =========================================================
# RESUME SCORING
# =========================================================

@app.post(
    "/api/v1/resumes/{resume_id}/score",
    response_model=ScoreResponse,
)
def score_resume(
    resume_id: str,
    request: ScoreRequest,
):

    request_id = create_request_id()

    resume = RESUME_STORE.get(
        resume_id
    )

    # -----------------------------------------------------
    # RESUME NOT FOUND
    # -----------------------------------------------------

    if resume is None:

        return JSONResponse(
            status_code=404,
            content={
                "detail": {
                    "error_code": "RESUME_NOT_FOUND",
                    "message": "Resume not found.",
                    "request_id": request_id,
                }
            },
        )

    # -----------------------------------------------------
    # GET JOB DESCRIPTION
    # -----------------------------------------------------

    job_description_path = (
        get_job_description_path(
            request.job_id
        )
    )

    if job_description_path is None:

        return JSONResponse(
            status_code=404,
            content={
                "detail": {
                    "error_code": "JOB_NOT_FOUND",
                    "message": (
                        f"Job '{request.job_id}' "
                        "was not found."
                    ),
                    "request_id": request_id,
                }
            },
        )

    # -----------------------------------------------------
    # CREATE SCORING JOB
    # -----------------------------------------------------

    job_id = create_job(
        job_type="resume_score",
        payload={
            "resume_id": resume_id,
            "job_id": request.job_id,
            "role": request.role,
        },
    )

    # -----------------------------------------------------
    # BACKGROUND SCORING
    # -----------------------------------------------------

    def score_worker():

        result = pipeline.process_candidate(
            resume_path=resume["path"],
            job_description_path=str(
                job_description_path
            ),
            role=request.role,
            candidate_id=resume_id,
        )

        return {
            "job_id": request.job_id,
            "resume_id": resume_id,
            "score": result["ats_score"],
            "classification": result["classification"],
            "pipeline": result,
        }

    run_async(
        job_id,
        score_worker,
    )

    # -----------------------------------------------------
    # RESPONSE
    # -----------------------------------------------------

    return {
        "job_id": job_id,
        "resume_id": resume_id,
        "status": "queued",
        "score": None,
        "classification": None,
        "request_id": request_id,
    }


# =========================================================
# JOB STATUS
# =========================================================

@app.get(
    "/api/v1/jobs/{job_id}",
    response_model=JobStatusResponse,
)
def get_job_status(
    job_id: str,
):

    job = job_manager.get_job(
        job_id
    )

    # -----------------------------------------------------
    # JOB NOT FOUND
    # -----------------------------------------------------

    if job is None:

        return JSONResponse(
            status_code=404,
            content={
                "detail": {
                    "error_code": "JOB_NOT_FOUND",
                    "message": "Job not found.",
                }
            },
        )

    return job


# =========================================================
# SHORTLISTING
# =========================================================

@app.post(
    "/api/v1/jobs/{job_id}/shortlist",
    response_model=ShortlistResponse,
)
def shortlist_candidates(
    job_id: str,
    request: ShortlistRequest,
):

    request_id = create_request_id()

    # -----------------------------------------------------
    # VALIDATE THRESHOLDS
    # -----------------------------------------------------

    if (
        request.review_threshold
        >= request.shortlist_threshold
    ):

        return JSONResponse(
            status_code=400,
            content={
                "detail": {
                    "error_code": "INVALID_THRESHOLDS",
                    "message": (
                        "Review threshold must be "
                        "lower than shortlist threshold."
                    ),
                    "request_id": request_id,
                }
            },
        )

    # -----------------------------------------------------
    # CONVERT CANDIDATES
    # -----------------------------------------------------

    candidates = [
        {
            "candidate_id": candidate.candidate_id,
            "ats_score": candidate.score,
        }
        for candidate in request.candidates
    ]

    # -----------------------------------------------------
    # DAY 14 RANKING
    # -----------------------------------------------------

    ranking = generate_ranking_output(
        candidates
    )

    # -----------------------------------------------------
    # API THRESHOLD CLASSIFICATION
    # -----------------------------------------------------

    shortlisted = [
        candidate
        for candidate in candidates
        if candidate["ats_score"]
        >= request.shortlist_threshold
    ]

    review = [
        candidate
        for candidate in candidates
        if (
            request.review_threshold
            <= candidate["ats_score"]
            < request.shortlist_threshold
        )
    ]

    rejected = [
        candidate
        for candidate in candidates
        if candidate["ats_score"]
        < request.review_threshold
    ]

    # -----------------------------------------------------
    # CONVERT RESPONSE
    # -----------------------------------------------------

    def convert(
        items,
        decision,
    ):

        return [
            CandidateDecision(
                candidate_id=item["candidate_id"],
                score=item["ats_score"],
                decision=decision,
            )
            for item in items
        ]

    # -----------------------------------------------------
    # FINAL RESPONSE
    # -----------------------------------------------------

    return {
        "job_id": job_id,
        "status": "completed",
        "shortlisted": convert(
            shortlisted,
            "shortlisted",
        ),
        "review": convert(
            review,
            "review",
        ),
        "rejected": convert(
            rejected,
            "rejected",
        ),
        "request_id": request_id,
    }