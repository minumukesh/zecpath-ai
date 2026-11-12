from pathlib import Path

from src.resume_extraction.extractor import extract_resume
from src.jd_parser.parser import parse_job_description
from src.semantic_matching.engine import semantic_match
from src.skill_extraction.extractor import extract_skills
from src.experience_parser.parser import (
    parse_experience,
    calculate_total_experience,
)
from src.education_certification.parser import (
    extract_education,
    extract_certifications,
    education_relevance,
)
from src.ats_scoring.engine import generate_candidate_score
from src.candidate_ranking.engine import generate_ranking_output


class ATSPipeline:

    def extract_resume_text(self, resume_path):
        resume_path = Path(resume_path)

        if not resume_path.exists():
            raise FileNotFoundError(
                f"Resume file not found: {resume_path}"
            )

        if resume_path.suffix.lower() == ".txt":
            return resume_path.read_text(
                encoding="utf-8",
                errors="ignore"
            ).strip()

        result = extract_resume(
            str(resume_path)
        )

        return result["extraction"]["cleaned_text"]

    def extract_job_text(self, job_description_path):
        job_description_path = Path(
            job_description_path
        )

        if not job_description_path.exists():
            raise FileNotFoundError(
                f"Job description file not found: {job_description_path}"
            )

        if job_description_path.suffix.lower() == ".txt":
            return job_description_path.read_text(
                encoding="utf-8",
                errors="ignore"
            ).strip()

        result = parse_job_description(
            str(job_description_path)
        )

        return result["job_profile"]["normalized_description"]

    def analyze_candidate(
        self,
        resume_text,
        job_text,
        role="Default",
    ):
        skills = extract_skills(
            resume_text
        )

        experiences = parse_experience(
            resume_text
        )

        experience_summary = (
            calculate_total_experience(
                experiences
            )
        )

        education = extract_education(
            resume_text
        )

        certifications = (
            extract_certifications(
                resume_text
            )
        )

        education_result = (
            education_relevance(
                education,
                role
            )
        )

        semantic_result = semantic_match(
            resume_text,
            job_text
        )

        return {
            "skills": skills,
            "experiences": experiences,
            "experience_summary": experience_summary,
            "education": education,
            "certifications": certifications,
            "education_relevance": education_result,
            "semantic_matching": semantic_result,
        }

    def calculate_component_scores(
        self,
        analysis,
    ):
        skills = analysis["skills"]

        if skills:
            skill_match = (
                sum(
                    item.get(
                        "confidence",
                        0.0
                    )
                    for item in skills
                )
                / len(skills)
            )
        else:
            skill_match = 0.0

        experience_summary = (
            analysis["experience_summary"]
        )

        total_years = (
            experience_summary.get(
                "total_years",
                0.0
            )
        )

        experience_relevance = min(
            total_years / 4.0,
            1.0
        )

        education_alignment = (
            analysis[
                "education_relevance"
            ].get(
                "score",
                0.0
            )
        )

        semantic_similarity = (
            analysis[
                "semantic_matching"
            ].get(
                "match_score",
                0.0
            )
        )

        return {
            "skill_match": skill_match,
            "experience_relevance": experience_relevance,
            "education_alignment": education_alignment,
            "semantic_similarity": semantic_similarity,
        }

    def process_candidate(
        self,
        resume_path,
        job_description_path,
        role="Default",
        candidate_id=None,
    ):
        resume_text = (
            self.extract_resume_text(
                resume_path
            )
        )

        job_text = (
            self.extract_job_text(
                job_description_path
            )
        )

        analysis = self.analyze_candidate(
            resume_text=resume_text,
            job_text=job_text,
            role=role,
        )

        component_scores = (
            self.calculate_component_scores(
                analysis
            )
        )

        scoring_result = (
            generate_candidate_score(
                role=role,
                skill_match=(
                    component_scores[
                        "skill_match"
                    ]
                ),
                experience_relevance=(
                    component_scores[
                        "experience_relevance"
                    ]
                ),
                education_alignment=(
                    component_scores[
                        "education_alignment"
                    ]
                ),
                semantic_similarity=(
                    component_scores[
                        "semantic_similarity"
                    ]
                ),
                candidate_id=candidate_id,
            )
        )

        return {
            "candidate_id": candidate_id,

            "ats_score": (
                scoring_result[
                    "ats_score"
                ]
            ),

            "classification": (
                scoring_result[
                    "classification"
                ]
            ),

            # Day 13 calls this field "scores".
            # We preserve that exact structure.
            "component_scores": (
                scoring_result[
                    "scores"
                ]
            ),

            "weights": (
                scoring_result[
                    "weights"
                ]
            ),

            "explanation": (
                scoring_result[
                    "explanation"
                ]
            ),

            "analysis": analysis,

            "scoring_engine":
                "day13_ats_scoring_engine",
        }

    def process_candidates(
        self,
        candidates,
    ):
        results = []

        for candidate in candidates:

            result = self.process_candidate(
                resume_path=(
                    candidate[
                        "resume_path"
                    ]
                ),

                job_description_path=(
                    candidate[
                        "job_description_path"
                    ]
                ),

                role=candidate.get(
                    "role",
                    "Default"
                ),

                candidate_id=(
                    candidate.get(
                        "candidate_id"
                    )
                ),
            )

            results.append(result)

        return generate_ranking_output(
            results
        )
