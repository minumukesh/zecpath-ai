"""End-to-end hiring simulation, comparison and performance analysis."""

import json
import re
import time

from pathlib import Path
from datetime import datetime, timezone

from .config import (
    ATS_THRESHOLD,
    SCREENING_THRESHOLD,
    HR_THRESHOLD,
    TECHNICAL_THRESHOLD,
    FINAL_AI_THRESHOLD,
    REQUIRED_SKILLS,
    WEIGHTS
)


class SimulationError(Exception):
    """Raised for invalid simulation inputs."""


class HiringPipeline:

    def __init__(self):

        self.stage_names = [
            "resume_upload",
            "ats_scoring",
            "screening",
            "hr_interview",
            "technical_interview",
            "final_decision"
        ]

    # ------------------------------------------------------
    # 1. RESUME UPLOAD
    # ------------------------------------------------------

    def upload_resume(self, candidate):

        if not isinstance(candidate, dict):
            raise SimulationError("Candidate must be a dictionary.")

        required = [
            "candidate_id",
            "candidate_name",
            "role",
            "resume_text"
        ]

        for field in required:

            value = candidate.get(field)

            if not isinstance(value, str) or not value.strip():
                raise SimulationError(
                    f"Missing or invalid candidate field: {field}"
                )

        role = candidate["role"].strip().lower()

        if role not in REQUIRED_SKILLS:
            raise SimulationError(
                f"Unsupported role: {role}"
            )

        resume_text = candidate["resume_text"].strip()

        return {
            "candidate_id": candidate["candidate_id"].strip(),
            "candidate_name": candidate["candidate_name"].strip(),
            "role": role,
            "resume_text": resume_text,
            "resume_status": "UPLOADED",
            "resume_characters": len(resume_text)
        }

    # ------------------------------------------------------
    # 2. ATS SCORING
    # ------------------------------------------------------

    def calculate_ats_score(self, resume, role):

        required_skills = REQUIRED_SKILLS[role]

        text = resume.lower()

        matched = []
        missing = []

        for skill in required_skills:

            pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

            if re.search(pattern, text):
                matched.append(skill)
            else:
                missing.append(skill)

        score = (
            len(matched) / len(required_skills)
        ) * 100

        score = round(score, 2)

        return {
            "score": score,
            "matched_skills": matched,
            "missing_skills": missing,
            "required_skill_count": len(required_skills),
            "matched_skill_count": len(matched),
            "status": (
                "PASS" if score >= ATS_THRESHOLD else "FAIL"
            )
        }

    # ------------------------------------------------------
    # 3. SCREENING
    # ------------------------------------------------------

    def evaluate_screening(self, screening_score):

        if isinstance(screening_score, bool):
            raise SimulationError("Invalid screening score.")

        if not isinstance(screening_score, (int, float)):
            raise SimulationError("Screening score must be numeric.")

        if not 0 <= screening_score <= 100:
            raise SimulationError(
                "Screening score must be between 0 and 100."
            )

        score = float(screening_score)

        return {
            "score": score,
            "status": (
                "PASS"
                if score >= SCREENING_THRESHOLD
                else "FAIL"
            )
        }

    # ------------------------------------------------------
    # 4. HR INTERVIEW
    # ------------------------------------------------------

    def evaluate_hr_interview(self, answers):

        if not isinstance(answers, list) or not answers:
            raise SimulationError("HR answers are required.")

        scores = []

        for answer in answers:

            if isinstance(answer, bool) or not isinstance(
                answer, (int, float)
            ):
                raise SimulationError("HR scores must be numeric.")

            if not 0 <= answer <= 100:
                raise SimulationError(
                    "HR scores must be between 0 and 100."
                )

            scores.append(float(answer))

        average = sum(scores) / len(scores)

        average = round(average, 2)

        return {
            "score": average,
            "question_count": len(scores),
            "individual_scores": scores,
            "status": (
                "PASS" if average >= HR_THRESHOLD else "FAIL"
            )
        }

    # ------------------------------------------------------
    # 5. TECHNICAL INTERVIEW
    # ------------------------------------------------------

    def evaluate_technical_interview(self, answers):

        if not isinstance(answers, list) or not answers:
            raise SimulationError(
                "Technical interview answers are required."
            )

        scores = []

        for answer in answers:

            if isinstance(answer, bool) or not isinstance(
                answer, (int, float)
            ):
                raise SimulationError(
                    "Technical scores must be numeric."
                )

            if not 0 <= answer <= 100:
                raise SimulationError(
                    "Technical scores must be between 0 and 100."
                )

            scores.append(float(answer))

        average = sum(scores) / len(scores)

        average = round(average, 2)

        return {
            "score": average,
            "question_count": len(scores),
            "individual_scores": scores,
            "status": (
                "PASS"
                if average >= TECHNICAL_THRESHOLD
                else "FAIL"
            )
        }

    # ------------------------------------------------------
    # 6. FINAL AI DECISION
    # ------------------------------------------------------

    def calculate_final_score(self, stages):

        total = 0.0

        for stage, weight in WEIGHTS.items():

            if stage not in stages:
                raise SimulationError(
                    f"Missing pipeline stage: {stage}"
                )

            total += stages[stage]["score"] * weight

        return round(total, 2)

    def make_ai_decision(self, stages):

        final_score = self.calculate_final_score(stages)

        failed_stages = [
            name
            for name, result in stages.items()
            if result["status"] == "FAIL"
        ]

        if (
            final_score >= FINAL_AI_THRESHOLD
            and not failed_stages
        ):
            recommendation = "RECOMMEND"

        elif final_score >= 50:
            recommendation = "HOLD"

        else:
            recommendation = "NOT_RECOMMENDED"

        return {
            "final_score": final_score,
            "recommendation": recommendation,
            "failed_stages": failed_stages,
            "decision_source": "AI_SIMULATION",
            "human_review_required": True
        }

    # ------------------------------------------------------
    # COMPLETE CANDIDATE PIPELINE
    # ------------------------------------------------------

    def process_candidate(self, candidate):

        start = time.perf_counter()

        uploaded = self.upload_resume(candidate)

        stages = {}

        # Resume upload
        resume_result = {
            "status": uploaded["resume_status"],
            "characters": uploaded["resume_characters"]
        }

        # ATS
        stages["ats"] = self.calculate_ats_score(
            uploaded["resume_text"],
            uploaded["role"]
        )

        # Screening
        stages["screening"] = self.evaluate_screening(
            candidate["screening_score"]
        )

        # HR
        stages["hr"] = self.evaluate_hr_interview(
            candidate["hr_answers"]
        )

        # Technical
        stages["technical"] = self.evaluate_technical_interview(
            candidate["technical_answers"]
        )

        # Final decision
        ai_decision = self.make_ai_decision(stages)

        elapsed = time.perf_counter() - start

        return {
            "candidate_id": uploaded["candidate_id"],
            "candidate_name": uploaded["candidate_name"],
            "role": uploaded["role"],
            "resume_upload": resume_result,
            "stages": stages,
            "ai_decision": ai_decision,
            "processing_time_seconds": round(elapsed, 6)
        }

    # ------------------------------------------------------
    # HUMAN VS AI JUDGMENT
    # ------------------------------------------------------

    def compare_human_ai(self, ai_decision, human_decision):

        allowed = [
            "RECOMMEND",
            "HOLD",
            "NOT_RECOMMENDED"
        ]

        if human_decision not in allowed:
            raise SimulationError(
                "Invalid human decision."
            )

        ai_result = ai_decision["recommendation"]

        agreement = ai_result == human_decision

        return {
            "ai_decision": ai_result,
            "human_decision": human_decision,
            "agreement": agreement,
            "comparison": (
                "AGREEMENT" if agreement else "DISAGREEMENT"
            ),
            "human_authority": True
        }

    # ------------------------------------------------------
    # INCONSISTENCY DETECTION
    # ------------------------------------------------------

    def detect_inconsistencies(self, pipeline_result, comparison):

        issues = []

        stages = pipeline_result["stages"]

        for name, result in stages.items():

            if result["score"] < 50:

                issues.append({
                    "type": "LOW_STAGE_SCORE",
                    "stage": name,
                    "score": result["score"],
                    "description": (
                        f"{name} score is below 50."
                    )
                })

        ats = stages["ats"]["score"]
        screening = stages["screening"]["score"]

        if abs(ats - screening) >= 30:

            issues.append({
                "type": "ATS_SCREENING_GAP",
                "ats_score": ats,
                "screening_score": screening,
                "difference": abs(ats - screening),
                "description": (
                    "Large difference between ATS and screening scores."
                )
            })

        if not comparison["agreement"]:

            issues.append({
                "type": "AI_HUMAN_DISAGREEMENT",
                "ai_decision": comparison["ai_decision"],
                "human_decision": comparison["human_decision"],
                "description": (
                    "AI recommendation differs from human judgment."
                )
            })

        failed = pipeline_result["ai_decision"]["failed_stages"]

        if failed:

            issues.append({
                "type": "FAILED_PIPELINE_STAGES",
                "stages": failed,
                "description": (
                    "One or more hiring stages failed."
                )
            })

        return issues

    # ------------------------------------------------------
    # PERFORMANCE ANALYSIS
    # ------------------------------------------------------

    def analyze_performance(self, results):

        if not results:
            raise SimulationError(
                "No pipeline results available."
            )

        times = [
            result["processing_time_seconds"]
            for result in results
        ]

        average_time = sum(times) / len(times)

        stage_totals = {}

        for result in results:

            for name, stage in result["stages"].items():

                stage_totals.setdefault(name, []).append(
                    stage["score"]
                )

        stage_averages = {
            name: round(
                sum(scores) / len(scores), 2
            )
            for name, scores in stage_totals.items()
        }

        return {
            "candidate_count": len(results),
            "average_processing_time_seconds": round(
                average_time, 6
            ),
            "maximum_processing_time_seconds": round(
                max(times), 6
            ),
            "minimum_processing_time_seconds": round(
                min(times), 6
            ),
            "average_stage_scores": stage_averages
        }

    # ------------------------------------------------------
    # IMPROVEMENT RECOMMENDATIONS
    # ------------------------------------------------------

    def generate_recommendations(self, results):

        recommendations = []

        for result in results:

            for issue in result["inconsistencies"]:

                issue_type = issue["type"]

                if issue_type == "ATS_SCREENING_GAP":

                    recommendations.append(
                        "Review ATS and screening criteria for alignment."
                    )

                elif issue_type == "AI_HUMAN_DISAGREEMENT":

                    recommendations.append(
                        "Review the evidence behind AI and human decisions."
                    )

                elif issue_type == "LOW_STAGE_SCORE":

                    recommendations.append(
                        f"Review the {issue['stage']} evaluation criteria."
                    )

                elif issue_type == "FAILED_PIPELINE_STAGES":

                    recommendations.append(
                        "Investigate failed stages before final decisions."
                    )

        if not recommendations:

            recommendations.append(
                "Continue monitoring pipeline consistency using labelled data."
            )

        return sorted(set(recommendations))

    # ------------------------------------------------------
    # COMPLETE END-TO-END EXECUTION
    # ------------------------------------------------------

    def run_simulation(self, candidates):

        if not isinstance(candidates, list) or not candidates:
            raise SimulationError(
                "At least one candidate is required."
            )

        results = []
        seen_ids = set()

        for candidate in candidates:

            candidate_id = candidate.get("candidate_id")

            if candidate_id in seen_ids:
                raise SimulationError(
                    f"Duplicate candidate ID: {candidate_id}"
                )

            seen_ids.add(candidate_id)

            pipeline = self.process_candidate(candidate)

            human_decision = candidate["human_decision"]

            comparison = self.compare_human_ai(
                pipeline["ai_decision"],
                human_decision
            )

            inconsistencies = self.detect_inconsistencies(
                pipeline,
                comparison
            )

            pipeline["human_comparison"] = comparison
            pipeline["inconsistencies"] = inconsistencies

            results.append(pipeline)

        performance = self.analyze_performance(results)

        recommendations = self.generate_recommendations(results)

        agreements = sum(
            1
            for result in results
            if result["human_comparison"]["agreement"]
        )

        report = {
            "report_title": "Day 56 - Full System Simulation",
            "generated_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "pipeline_stages": self.stage_names,
            "candidate_count": len(results),
            "results": results,
            "human_ai_comparison": {
                "agreements": agreements,
                "disagreements": len(results) - agreements,
                "agreement_rate": round(
                    agreements / len(results), 4
                )
            },
            "performance_analysis": performance,
            "total_inconsistencies": sum(
                len(result["inconsistencies"])
                for result in results
            ),
            "improvement_recommendations": recommendations,
            "limitations": [
                "This is a synthetic end-to-end simulation.",
                "The ATS, screening and interview stages use demonstration inputs.",
                "It does not establish production model accuracy.",
                "Human decisions in this dataset are illustrative.",
                "Production integration requires adapters to the actual Zecpath modules."
            ]
        }

        return report


def save_report(report, output_directory="outputs/day56"):

    directory = Path(output_directory)

    directory.mkdir(parents=True, exist_ok=True)

    json_path = directory / "end_to_end_test_report.json"

    json_path.write_text(
        json.dumps(report, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    performance = report["performance_analysis"]

    lines = [
        "# Day 56 - End-to-End AI Test Report",
        "",
        "## Objective",
        "Validate the Zecpath AI hiring pipeline end-to-end.",
        "",
        "## Pipeline stages",
    ]

    for index, stage in enumerate(report["pipeline_stages"], 1):
        lines.append(f"{index}. {stage.replace('_', ' ').title()}")

    lines.extend([
        "",
        "## Candidate results",
        "",
        "| Candidate | Role | ATS | Screening | HR | Technical | AI Decision | Human Decision |",
        "|---|---|---:|---:|---:|---:|---|---|"
    ])

    for result in report["results"]:

        stages = result["stages"]

        lines.append(
            f"| {result['candidate_name']} "
            f"| {result['role']} "
            f"| {stages['ats']['score']} "
            f"| {stages['screening']['score']} "
            f"| {stages['hr']['score']} "
            f"| {stages['technical']['score']} "
            f"| {result['ai_decision']['recommendation']} "
            f"| {result['human_comparison']['human_decision']} |"
        )

    lines.extend([
        "",
        "## AI versus human judgment",
        "",
        f"- Agreements: {report['human_ai_comparison']['agreements']}",
        f"- Disagreements: {report['human_ai_comparison']['disagreements']}",
        f"- Agreement rate: {report['human_ai_comparison']['agreement_rate']:.2%}",
        "",
        "## System performance",
        "",
        f"- Candidates processed: {performance['candidate_count']}",
        f"- Average processing time: {performance['average_processing_time_seconds']} seconds",
        f"- Maximum processing time: {performance['maximum_processing_time_seconds']} seconds",
        f"- Minimum processing time: {performance['minimum_processing_time_seconds']} seconds",
        "",
        "### Average stage scores",
        ""
    ])

    for name, score in performance["average_stage_scores"].items():
        lines.append(f"- {name.title()}: {score}")

    lines.extend([
        "",
        "## Inconsistency analysis",
        "",
        f"Total inconsistencies: {report['total_inconsistencies']}",
        "",
        "## Improvement recommendations",
        ""
    ])

    for recommendation in report["improvement_recommendations"]:
        lines.append(f"- {recommendation}")

    lines.extend([
        "",
        "## Limitations",
        ""
    ])

    for limitation in report["limitations"]:
        lines.append(f"- {limitation}")

    md_path = directory / "system_performance_analysis.md"

    md_path.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8"
    )

    return {
        "json_report": str(json_path),
        "markdown_report": str(md_path)
    }
