"""
ZECPATH-AI Day 53
Hiring Intelligence Report Generator

Combines candidate evaluation information into a recruiter-friendly report.

Sections:
1. Candidate profile
2. ATS summary
3. Screening results
4. HR interview insights
5. Technical performance
6. Behavioral observations
7. Integrity indicators
8. Strengths
9. Weaknesses
10. Risk indicators
11. Final recommendation

Exports:
- JSON
- Markdown
- HTML
"""

from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any
import json
import html


class HiringIntelligenceReportGenerator:

    def __init__(self):

        self.report_version = "1.0"

    # --------------------------------------------------------
    # MAIN REPORT GENERATION
    # --------------------------------------------------------

    def generate_report(self, candidate_data: Dict[str, Any]):

        self._validate(candidate_data)

        profile = candidate_data["candidate"]

        ats = candidate_data.get("ats", {})
        screening = candidate_data.get("screening", {})
        hr = candidate_data.get("hr_interview", {})
        technical = candidate_data.get("technical_interview", {})
        behavioral = candidate_data.get("behavioral", {})
        integrity = candidate_data.get("integrity", {})
        final_decision = candidate_data.get("final_decision", {})

        # ----------------------------------------------------
        # 1. GENERATE STRENGTHS
        # ----------------------------------------------------

        strengths = []
        weaknesses = []
        risk_indicators = []

        hiring_fit_score = final_decision.get(
            "hiring_fit_score"
        )

        if hiring_fit_score is not None:

            if hiring_fit_score >= 85:
                strengths.append(
                    "Strong overall Hiring Fit Score."
                )

            elif hiring_fit_score < 55:
                weaknesses.append(
                    "Overall Hiring Fit Score is below the configured threshold."
                )

        ats_score = ats.get("score")

        if ats_score is not None:

            if ats_score >= 80:
                strengths.append(
                    "Strong ATS profile match."
                )

            elif ats_score < 55:
                weaknesses.append(
                    "ATS profile match requires improvement."
                )

        screening_score = screening.get("score")

        if screening_score is not None:

            if screening_score >= 80:
                strengths.append(
                    "Strong screening assessment performance."
                )

            elif screening_score < 55:
                weaknesses.append(
                    "Screening assessment performance is below the configured threshold."
                )

        hr_score = hr.get("score")

        if hr_score is not None:

            if hr_score >= 80:
                strengths.append(
                    "Strong HR interview assessment."
                )

            elif hr_score < 55:
                weaknesses.append(
                    "HR interview assessment requires improvement."
                )

        technical_score = technical.get("score")

        if technical_score is not None:

            if technical_score >= 80:
                strengths.append(
                    "Strong technical interview performance."
                )

            elif technical_score < 55:
                weaknesses.append(
                    "Technical interview performance requires improvement."
                )

        machine_score = technical.get("machine_test_score")

        if machine_score is not None:

            if machine_score >= 80:
                strengths.append(
                    "Strong practical machine-test performance."
                )

            elif machine_score < 55:
                weaknesses.append(
                    "Practical machine-test performance requires improvement."
                )

        # Add evaluator-provided findings.
        strengths.extend(
            self._safe_list(candidate_data.get("strengths", []))
        )

        weaknesses.extend(
            self._safe_list(candidate_data.get("weaknesses", []))
        )

        # ----------------------------------------------------
        # 2. BEHAVIORAL OBSERVATIONS
        # ----------------------------------------------------

        behavioral_observations = {
            "task_focus_score": behavioral.get("task_focus_score"),
            "distraction_frequency": behavioral.get(
                "distraction_frequency"
            ),
            "contextual_observations": self._safe_list(
                behavioral.get("observations", [])
            ),
            "interpretation": (
                "Behavioral observations are contextual only. "
                "They are not measures of honesty, intelligence, "
                "confidence, or job suitability."
            )
        }

        # ----------------------------------------------------
        # 3. INTEGRITY RISK INDICATORS
        # ----------------------------------------------------

        integrity_flags = integrity.get("flags", [])

        for flag in integrity_flags:

            if isinstance(flag, dict):

                risk_indicators.append({
                    "category": "INTEGRITY",
                    "description": flag.get(
                        "description",
                        flag.get("signal", "Integrity event recorded.")
                    ),
                    "status": flag.get(
                        "status",
                        "REVIEW_REQUIRED"
                    ),
                    "interpretation": (
                        "Requires contextual human review. "
                        "An alert alone is not proof of misconduct."
                    )
                })

            else:

                risk_indicators.append({
                    "category": "INTEGRITY",
                    "description": str(flag),
                    "status": "REVIEW_REQUIRED",
                    "interpretation": (
                        "Requires contextual human review. "
                        "An alert alone is not proof of misconduct."
                    )
                })

        # ----------------------------------------------------
        # 4. OTHER RISK INDICATORS
        # ----------------------------------------------------

        if not candidate_data.get("evidence_verified", True):

            risk_indicators.append({
                "category": "EVIDENCE",
                "description": "Evaluation evidence is not verified.",
                "status": "REVIEW_REQUIRED",
                "interpretation": (
                    "Verify the source and completeness of the evidence."
                )
            })

        missing_stages = candidate_data.get(
            "missing_stages", []
        )

        for stage in missing_stages:

            risk_indicators.append({
                "category": "INCOMPLETE_EVALUATION",
                "description": f"{stage} evaluation is missing.",
                "status": "REVIEW_REQUIRED",
                "interpretation": (
                    "Complete the evaluation before making a final decision."
                )
            })

        # ----------------------------------------------------
        # 5. FINAL RECOMMENDATION
        # ----------------------------------------------------

        recommendation = final_decision.get(
            "recommendation",
            "NOT_PROVIDED"
        )

        decision_explanation = final_decision.get(
            "explanation",
            "No decision explanation was supplied."
        )

        confidence = final_decision.get(
            "confidence_score"
        )

        # ----------------------------------------------------
        # 6. CREATE REPORT
        # ----------------------------------------------------

        report = {

            "project": "ZECPATH-AI",

            "day": 53,

            "report_title": "Hiring Intelligence Report",

            "report_version": self.report_version,

            "generated_at": datetime.now(
                timezone.utc
            ).isoformat(),

            "candidate_profile": {

                "candidate_id": profile["candidate_id"],

                "candidate_name": profile["candidate_name"],

                "email": profile.get("email"),

                "target_role": profile["target_role"],

                "experience": profile.get("experience"),

                "skills": self._safe_list(
                    profile.get("skills", [])
                )
            },

            "evaluation_summary": {

                "ats": {
                    "score": ats_score,
                    "summary": ats.get(
                        "summary",
                        "No ATS summary supplied."
                    )
                },

                "screening": {
                    "score": screening_score,
                    "summary": screening.get(
                        "summary",
                        "No screening summary supplied."
                    )
                },

                "hr_interview": {
                    "score": hr_score,
                    "summary": hr.get(
                        "summary",
                        "No HR interview summary supplied."
                    ),
                    "interviewer_notes": self._safe_list(
                        hr.get("notes", [])
                    )
                },

                "technical_interview": {
                    "score": technical_score,
                    "machine_test_score": machine_score,
                    "summary": technical.get(
                        "summary",
                        "No technical summary supplied."
                    ),
                    "technical_skills": technical.get(
                        "skills",
                        {}
                    )
                }
            },

            "behavioral_analysis": behavioral_observations,

            "integrity_analysis": {

                "flag_count": len(integrity_flags),

                "flags": risk_indicators,

                "human_review_required": (
                    len(integrity_flags) > 0
                )
            },

            "candidate_assessment": {

                "strengths": self._unique(strengths),

                "weaknesses": self._unique(weaknesses),

                "risk_indicators": risk_indicators
            },

            "final_recommendation": {

                "recommendation": recommendation,

                "hiring_fit_score": hiring_fit_score,

                "confidence_score": confidence,

                "explanation": decision_explanation,

                "human_review_required": (
                    final_decision.get(
                        "human_review_required",
                        True
                    )
                ),

                "automatic_hiring_action": False
            },

            "report_disclaimer": (
                "This report supports recruiter decision-making. "
                "It does not independently determine hiring outcomes. "
                "All recommendations require appropriate human review."
            )
        }

        return report

    # --------------------------------------------------------
    # INPUT VALIDATION
    # --------------------------------------------------------

    @staticmethod
    def _validate(data):

        if not isinstance(data, dict):
            raise ValueError("Candidate data must be a dictionary.")

        if "candidate" not in data:
            raise ValueError("Candidate profile is required.")

        profile = data["candidate"]

        required_fields = [
            "candidate_id",
            "candidate_name",
            "target_role"
        ]

        for field in required_fields:

            if not profile.get(field):

                raise ValueError(
                    f"Missing candidate field: {field}"
                )

        score_sections = [
            "ats",
            "screening",
            "hr_interview",
            "technical_interview"
        ]

        for section in score_sections:

            values = data.get(section, {})

            for score_field in ["score", "machine_test_score"]:

                score = values.get(score_field)

                if score is not None:

                    if not isinstance(score, (int, float)):
                        raise ValueError(
                            f"{section}.{score_field} must be numeric."
                        )

                    if not 0 <= score <= 100:
                        raise ValueError(
                            f"{section}.{score_field} must be between 0 and 100."
                        )

        final_decision = data.get("final_decision", {})

        final_score = final_decision.get("hiring_fit_score")

        if final_score is not None:

            if not isinstance(final_score, (int, float)):
                raise ValueError("Hiring Fit Score must be numeric.")

            if not 0 <= final_score <= 100:
                raise ValueError("Hiring Fit Score must be between 0 and 100.")

    # --------------------------------------------------------
    # HELPER METHODS
    # --------------------------------------------------------

    @staticmethod
    def _safe_list(value):

        if value is None:
            return []

        if not isinstance(value, list):
            return [str(value)]

        return value

    @staticmethod
    def _unique(items):

        result = []

        for item in items:

            if item not in result:
                result.append(item)

        return result

    # --------------------------------------------------------
    # JSON EXPORT
    # --------------------------------------------------------

    @staticmethod
    def export_json(report, output_path):

        path = Path(output_path)

        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as file:

            json.dump(report, file, indent=4, ensure_ascii=False)

        return str(path)

    # --------------------------------------------------------
    # MARKDOWN EXPORT
    # --------------------------------------------------------

    @staticmethod
    def export_markdown(report, output_path):

        path = Path(output_path)

        path.parent.mkdir(parents=True, exist_ok=True)

        profile = report["candidate_profile"]

        evaluation = report["evaluation_summary"]

        assessment = report["candidate_assessment"]

        recommendation = report["final_recommendation"]

        lines = [

            "# Hiring Intelligence Report",

            "",

            f"**Candidate:** {profile['candidate_name']}",

            f"**Candidate ID:** {profile['candidate_id']}",

            f"**Position:** {profile['target_role']}",

            f"**Report Date:** {report['generated_at']}",

            "",

            "---",

            "",

            "## 1. Executive Summary",

            f"- Hiring Fit Score: {recommendation['hiring_fit_score']}",

            f"- Final Recommendation: {recommendation['recommendation']}",

            f"- Confidence Score: {recommendation['confidence_score']}",

            "",

            "## 2. Candidate Profile",

            f"- Experience: {profile.get('experience')}",

            f"- Skills: {', '.join(profile['skills'])}",

            "",

            "## 3. Evaluation Summary",

            "| Evaluation Stage | Score | Summary |",

            "|---|---:|---|"

        ]

        stage_names = [
            ("ATS", "ats"),
            ("Screening", "screening"),
            ("HR Interview", "hr_interview"),
            ("Technical Interview", "technical_interview")
        ]

        for label, key in stage_names:

            stage = evaluation[key]

            lines.append(
                f"| {label} | {stage['score']} | {stage['summary']} |"
            )

        lines.extend([

            "",

            "### Machine Test",

            str(
                evaluation["technical_interview"]["machine_test_score"]
            ),

            "",

            "## 4. Behavioral Observations",

            str(
                report["behavioral_analysis"]["contextual_observations"]
            ),

            "",

            report["behavioral_analysis"]["interpretation"],

            "",

            "## 5. Strengths",

        ])

        for item in assessment["strengths"]:
            lines.append(f"- {item}")

        lines.extend(["", "## 6. Weaknesses", ""])

        for item in assessment["weaknesses"]:
            lines.append(f"- {item}")

        lines.extend(["", "## 7. Risk Indicators", ""])

        for item in assessment["risk_indicators"]:

            lines.append(
                f"- **{item['category']}**: {item['description']} "
                f"({item['status']})"
            )

        lines.extend([

            "",

            "## 8. Final Recommendation",

            f"**{recommendation['recommendation']}**",

            "",

            recommendation["explanation"],

            "",

            "## 9. Recruiter Review",

            "- Human review required: Yes",

            "- Automatic hiring action: Disabled",

            "",

            "## Disclaimer",

            report["report_disclaimer"],

            ""
        ])

        path.write_text("\n".join(lines), encoding="utf-8")

        return str(path)

    # --------------------------------------------------------
    # HTML EXPORT
    # --------------------------------------------------------

    @staticmethod
    def export_html(report, output_path):

        path = Path(output_path)

        path.parent.mkdir(parents=True, exist_ok=True)

        profile = report["candidate_profile"]

        evaluation = report["evaluation_summary"]

        assessment = report["candidate_assessment"]

        decision = report["final_recommendation"]

        def safe(value):
            return html.escape(str(value))

        stage_rows = ""

        for label, key in [
            ("ATS", "ats"),
            ("Screening", "screening"),
            ("HR Interview", "hr_interview"),
            ("Technical Interview", "technical_interview")
        ]:

            stage = evaluation[key]

            stage_rows += f"""
            <tr>
                <td>{safe(label)}</td>
                <td>{safe(stage['score'])}</td>
                <td>{safe(stage['summary'])}</td>
            </tr>
            """

        strengths = "".join(
            f"<li>{safe(item)}</li>"
            for item in assessment["strengths"]
        )

        weaknesses = "".join(
            f"<li>{safe(item)}</li>"
            for item in assessment["weaknesses"]
        )

        risks = "".join(
            f"<li>{safe(item['category'])}: "
            f"{safe(item['description'])} "
            f"({safe(item['status'])})</li>"
            for item in assessment["risk_indicators"]
        )

        skills = ", ".join(profile["skills"])

        content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Hiring Intelligence Report</title>

<style>

body {{
    font-family: Arial, sans-serif;
    background: #f3f5f9;
    color: #263238;
    margin: 0;
    padding: 30px;
}}

.container {{
    max-width: 1000px;
    margin: auto;
    background: white;
    padding: 35px;
    border-radius: 10px;
}}

h1 {{
    color: #17365d;
}}

h2 {{
    color: #24527a;
    border-bottom: 1px solid #ddd;
    padding-bottom: 8px;
}}

.card {{
    background: #f5f8fc;
    padding: 18px;
    border-radius: 8px;
    margin: 15px 0;
}}

.score {{
    font-size: 30px;
    font-weight: bold;
    color: #17365d;
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th, td {{
    padding: 12px;
    border: 1px solid #ddd;
    text-align: left;
}}

th {{
    background: #eaf0f7;
}}

li {{
    margin-bottom: 8px;
}}

.disclaimer {{
    background: #fff7e6;
    padding: 15px;
    border-radius: 8px;
}}

@media print {{
    body {{
        background: white;
        padding: 0;
    }}

    .container {{
        box-shadow: none;
        max-width: none;
    }}
}}

</style>
</head>

<body>

<div class="container">

<h1>Hiring Intelligence Report</h1>

<p>ZECPATH-AI | Candidate Evaluation</p>

<div class="card">

<h2>Candidate Profile</h2>

<p><strong>Name:</strong> {safe(profile['candidate_name'])}</p>

<p><strong>Candidate ID:</strong> {safe(profile['candidate_id'])}</p>

<p><strong>Position:</strong> {safe(profile['target_role'])}</p>

<p><strong>Experience:</strong> {safe(profile.get('experience'))}</p>

<p><strong>Skills:</strong> {safe(skills)}</p>

</div>

<div class="card">

<h2>Final Recommendation</h2>

<p class="score">{safe(decision['hiring_fit_score'])}/100</p>

<p><strong>Decision:</strong> {safe(decision['recommendation'])}</p>

<p><strong>Confidence:</strong> {safe(decision['confidence_score'])}/100</p>

<p>{safe(decision['explanation'])}</p>

</div>

<h2>Evaluation Summary</h2>

<table>

<tr>
<th>Stage</th>
<th>Score</th>
<th>Summary</th>
</tr>

{stage_rows}

</table>

<h2>Machine Test</h2>

<p>
{safe(evaluation['technical_interview']['machine_test_score'])}
</p>

<h2>Behavioral Observations</h2>

<p>
{safe(report['behavioral_analysis']['contextual_observations'])}
</p>

<p>
{safe(report['behavioral_analysis']['interpretation'])}
</p>

<h2>Strengths</h2>

<ul>{strengths}</ul>

<h2>Weaknesses</h2>

<ul>{weaknesses}</ul>

<h2>Risk Indicators</h2>

<ul>{risks}</ul>

<h2>Recruiter Review</h2>

<p>Human review required: Yes</p>

<p>Automatic hiring action: Disabled</p>

<div class="disclaimer">

<strong>Disclaimer</strong>

<p>{safe(report['report_disclaimer'])}</p>

</div>

</div>

</body>
</html>
"""

        path.write_text(content, encoding="utf-8")

        return str(path)


def main():

    generator = HiringIntelligenceReportGenerator()

    sample_candidate = {

        "candidate": {

            "candidate_id": "CAND-053",

            "candidate_name": "Demo Candidate",

            "email": "demo@example.com",

            "target_role": "Data Analyst",

            "experience": "Fresher",

            "skills": [
                "Python",
                "SQL",
                "Excel",
                "Power BI",
                "Statistics"
            ]
        },

        "ats": {

            "score": 88,

            "summary": "Strong resume match with relevant technical skills."
        },

        "screening": {

            "score": 85,

            "summary": "Candidate passed the initial screening assessment."
        },

        "hr_interview": {

            "score": 82,

            "summary": "Good communication and role understanding.",

            "notes": [
                "Explained academic projects clearly.",
                "Demonstrated willingness to learn."
            ]
        },

        "technical_interview": {

            "score": 87,

            "machine_test_score": 90,

            "summary": "Strong Python, SQL and analytical problem-solving skills.",

            "skills": {
                "Python": 90,
                "SQL": 88,
                "Statistics": 82
            }
        },

        "behavioral": {

            "task_focus_score": 85,

            "distraction_frequency": 0.2,

            "observations": [
                "Task-related focus observations recorded."
            ]
        },

        "integrity": {

            "flags": []
        },

        "strengths": [

            "Strong project explanation.",

            "Good analytical thinking."
        ],

        "weaknesses": [

            "Limited professional industry experience."
        ],

        "missing_stages": [],

        "evidence_verified": True,

        "final_decision": {

            "recommendation": "SELECTED",

            "hiring_fit_score": 86.5,

            "confidence_score": 95,

            "explanation": (
                "The candidate demonstrated strong performance "
                "across the completed evaluation stages."
            ),

            "human_review_required": True
        }
    }

    report = generator.generate_report(sample_candidate)

    base = "outputs/day53/hiring_intelligence_report"

    generator.export_json(
        report,
        base + ".json"
    )

    generator.export_markdown(
        report,
        base + ".md"
    )

    generator.export_html(
        report,
        base + ".html"
    )

    print("\nHIRING INTELLIGENCE REPORT")
    print("=" * 48)

    print("Candidate:", report["candidate_profile"]["candidate_name"])

    print("Role:", report["candidate_profile"]["target_role"])

    print(
        "Hiring Fit Score:",
        report["final_recommendation"]["hiring_fit_score"]
    )

    print(
        "Recommendation:",
        report["final_recommendation"]["recommendation"]
    )

    print("Strengths:", len(report["candidate_assessment"]["strengths"]))

    print("Weaknesses:", len(report["candidate_assessment"]["weaknesses"]))

    print(
        "Risk Indicators:",
        len(report["candidate_assessment"]["risk_indicators"])
    )

    print("\nJSON report generated.")

    print("Markdown report generated.")

    print("HTML report generated.")

    print("\nDAY 53 DEMONSTRATION COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()
