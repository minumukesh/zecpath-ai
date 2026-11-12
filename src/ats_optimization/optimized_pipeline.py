"""
Day 18 - Optimized ATS Engine

Extends the existing ATS pipeline without duplicating
Day 13, Day 14, or Day 16 functionality.
"""

from pathlib import Path

from src.ats_pipeline.pipeline import ATSPipeline
from src.ats_optimization.optimizer import (
    fast_text_extraction,
    clean_noisy_resume,
    detect_entities,
)


class OptimizedATSPipeline(ATSPipeline):

    def extract_resume_text(self, resume_path):
        path = Path(resume_path)

        # Fast path for TXT resumes
        if path.suffix.lower() == ".txt":
            text = fast_text_extraction(str(path))
            return clean_noisy_resume(text)

        # Existing extraction for other formats
        text = super().extract_resume_text(resume_path)

        return clean_noisy_resume(text)

    def analyze_candidate(
        self,
        resume_text,
        job_text,
        role=None
    ):
        """
        Reuse the existing ATS analysis while adding
        lightweight entity detection.

        role is accepted because the existing ATS pipeline
        passes it during process_candidate().
        """

        analysis = super().analyze_candidate(
            resume_text=resume_text,
            job_text=job_text,
            role=role,
        )

        analysis["entities"] = detect_entities(resume_text)

        return analysis
