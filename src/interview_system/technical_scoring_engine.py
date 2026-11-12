"""
Day 47 - Explainable Technical Skill Scoring Engine.

This is a transparent, evidence-based heuristic scorer, not an LLM or a
substitute for a qualified interviewer. It scores observable answer evidence
against expected concepts and emits component-level explanations.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json
import re


DEFAULT_WEIGHTS = {
    "conceptual": {"accuracy": 0.40, "depth": 0.25, "reasoning": 0.20, "applicability": 0.15},
    "scenario": {"accuracy": 0.25, "depth": 0.20, "reasoning": 0.30, "applicability": 0.25},
    "coding": {"accuracy": 0.35, "depth": 0.20, "reasoning": 0.25, "applicability": 0.20},
    "system_design": {"accuracy": 0.25, "depth": 0.25, "reasoning": 0.25, "applicability": 0.25},
    "behavioral_technical": {"accuracy": 0.20, "depth": 0.25, "reasoning": 0.25, "applicability": 0.30},
}

DIFFICULTY_PROFILES = {
    "beginner": {"minimum_concepts": 1, "minimum_words": 12},
    "intermediate": {"minimum_concepts": 2, "minimum_words": 25},
    "advanced": {"minimum_concepts": 3, "minimum_words": 40},
}

DEPTH_SIGNALS = (
    "because", "therefore", "for example", "for instance", "trade-off",
    "tradeoff", "limitation", "edge case", "alternative", "when", "why",
    "step", "first", "then", "finally", "complexity", "performance",
)
LOGIC_SIGNALS = (
    "first", "second", "then", "next", "because", "therefore", "thus",
    "if", "otherwise", "finally", "as a result", "step",
)
APPLICABILITY_SIGNALS = (
    "production", "project", "application", "user", "database", "api",
    "deploy", "monitor", "logging", "testing", "security", "latency",
    "scalability", "real-world", "real world", "customer", "business",
)
STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in",
    "into", "is", "it", "of", "on", "or", "that", "the", "this", "to",
    "with", "what", "how", "why", "when", "where",
}


@dataclass
class ComponentScore:
    score: float
    evidence: list[str]
    explanation: str


class TechnicalSkillScoringEngine:
    """Score answers on accuracy, depth, logical reasoning and applicability."""

    def __init__(self, weights: dict[str, dict[str, float]] | None = None):
        self.weights = weights or DEFAULT_WEIGHTS
        self._validate_weights()

    def _validate_weights(self) -> None:
        required = {"accuracy", "depth", "reasoning", "applicability"}
        for qtype, rubric in self.weights.items():
            if set(rubric) != required:
                raise ValueError(f"Invalid rubric components for {qtype}")
            if any(not isinstance(v, (int, float)) or v < 0 for v in rubric.values()):
                raise ValueError(f"Weights must be non-negative for {qtype}")
            if abs(sum(rubric.values()) - 1.0) > 1e-8:
                raise ValueError(f"Weights for {qtype} must sum to 1.0")

    @staticmethod
    def _normalise_text(value: str) -> str:
        return re.sub(r"\s+", " ", value.lower()).strip()

    @staticmethod
    def _clamp(value: float) -> float:
        return round(max(0.0, min(100.0, value)), 2)

    @staticmethod
    def _tokens(text: str) -> set[str]:
        return {
            token for token in re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]*", text.lower())
            if len(token) > 1 and token not in STOP_WORDS
        }

    def _accuracy(self, answer: str, expected_concepts: list[str]) -> ComponentScore:
        if not expected_concepts:
            raise ValueError("expected_concepts must contain at least one concept")
        normalised = self._normalise_text(answer)
        found = [concept for concept in expected_concepts
                 if self._normalise_text(concept) in normalised]
        # Exact phrase coverage is deliberately explainable and conservative.
        score = 100.0 * len(found) / len(expected_concepts)
        missing = [c for c in expected_concepts if c not in found]
        evidence = [f"Expected concept found: {c}" for c in found]
        evidence += [f"Expected concept not evidenced: {c}" for c in missing]
        explanation = (
            f"{len(found)} of {len(expected_concepts)} expected concepts were "
            "explicitly mentioned. Mentioning a term does not by itself prove "
            "that the candidate understands it."
        )
        return ComponentScore(self._clamp(score), evidence, explanation)

    def _depth(self, answer: str, difficulty: str) -> ComponentScore:
        normalised = self._normalise_text(answer)
        words = re.findall(r"\b[\w+#.-]+\b", normalised)
        profile = DIFFICULTY_PROFILES[difficulty]
        signals = [s for s in DEPTH_SIGNALS if s in normalised]
        # Word coverage and distinct explanation signals are capped independently.
        length_score = min(100.0, 100.0 * len(words) / profile["minimum_words"])
        signal_score = min(100.0, 25.0 * len(signals))
        score = 0.60 * length_score + 0.40 * signal_score
        evidence = [f"Explanation signal: {s}" for s in signals]
        evidence.append(f"Answer length: {len(words)} words; {profile['minimum_words']} expected for {difficulty}")
        return ComponentScore(
            self._clamp(score), evidence,
            "Depth is estimated from explanation detail and elaboration signals. "
            "A human reviewer should confirm technical correctness and depth."
        )

    def _reasoning(self, answer: str) -> ComponentScore:
        normalised = self._normalise_text(answer)
        signals = [s for s in LOGIC_SIGNALS if re.search(r"\b" + re.escape(s) + r"\b", normalised)]
        # Distinct reasoning signals suggest structure, not necessarily valid logic.
        score = min(100.0, len(signals) * 20.0)
        return ComponentScore(
            self._clamp(score),
            [f"Reasoning structure signal: {s}" for s in signals],
            "Logical structure is estimated from sequencing, conditional and "
            "cause/effect language; the inference itself still needs human review."
        )

    def _applicability(self, answer: str, real_world_indicators: list[str] | None) -> ComponentScore:
        normalised = self._normalise_text(answer)
        indicators = real_world_indicators or list(APPLICABILITY_SIGNALS)
        found = [item for item in indicators if self._normalise_text(item) in normalised]
        score = min(100.0, 25.0 * len(found))
        return ComponentScore(
            self._clamp(score),
            [f"Practical application evidence: {item}" for item in found],
            "Practical relevance is estimated from concrete implementation, "
            "deployment, testing, operational or business references."
        )

    def score_answer(
        self,
        *,
        candidate_id: str,
        skill: str,
        question: str,
        answer: str,
        expected_concepts: list[str],
        question_type: str = "conceptual",
        difficulty: str = "intermediate",
        real_world_indicators: list[str] | None = None,
    ) -> dict[str, Any]:
        if not candidate_id.strip() or not skill.strip() or not question.strip():
            raise ValueError("candidate_id, skill and question are required")
        if not isinstance(answer, str) or not answer.strip():
            raise ValueError("answer must be a non-empty string")
        if question_type not in self.weights:
            raise ValueError(f"Unsupported question_type: {question_type}")
        if difficulty not in DIFFICULTY_PROFILES:
            raise ValueError(f"Unsupported difficulty: {difficulty}")
        if not isinstance(expected_concepts, list) or not expected_concepts:
            raise ValueError("expected_concepts must be a non-empty list")

        components = {
            "accuracy": self._accuracy(answer, expected_concepts),
            "depth": self._depth(answer, difficulty),
            "reasoning": self._reasoning(answer),
            "applicability": self._applicability(answer, real_world_indicators),
        }
        rubric = self.weights[question_type]
        overall = self._clamp(sum(components[name].score * weight for name, weight in rubric.items()))

        words = re.findall(r"\b[\w+#.-]+\b", answer)
        concept_coverage = components["accuracy"].score
        depth_score = components["depth"].score
        shallow_reasons = []
        if len(words) < DIFFICULTY_PROFILES[difficulty]["minimum_words"]:
            shallow_reasons.append("Answer is shorter than the expected depth for this difficulty.")
        if concept_coverage < 50:
            shallow_reasons.append("Less than half of the expected concepts were evidenced.")
        if depth_score < 40:
            shallow_reasons.append("Few explanation or elaboration signals were detected.")
        is_shallow = len(shallow_reasons) >= 2

        return {
            "candidate_id": candidate_id,
            "skill": skill,
            "question": question,
            "question_type": question_type,
            "difficulty": difficulty,
            "overall_score": overall,
            "normalized_score": overall,  # All difficulty levels use the same 0-100 scale.
            "performance_band": (
                "strong" if overall >= 80 else
                "competent" if overall >= 65 else
                "developing" if overall >= 45 else "needs_improvement"
            ),
            "is_shallow": is_shallow,
            "shallow_reasons": shallow_reasons,
            "rubric_weights": rubric,
            "component_scores": {
                name: asdict(component) for name, component in components.items()
            },
            "explanation": (
                "Score = sum(component score × question-type weight). "
                "Scores are normalized to 0–100 for every difficulty level. "
                "Difficulty changes the depth evidence threshold, not the score scale."
            ),
        }

    def build_report(self, candidate_id: str, evaluations: list[dict[str, Any]]) -> dict[str, Any]:
        if not evaluations:
            raise ValueError("At least one evaluation is required")
        if any(item.get("candidate_id") != candidate_id for item in evaluations):
            raise ValueError("All evaluations must belong to the requested candidate")
        skill_groups: dict[str, list[dict[str, Any]]] = {}
        for item in evaluations:
            skill_groups.setdefault(item["skill"], []).append(item)

        skill_breakdown = {}
        for skill, items in sorted(skill_groups.items()):
            avg = self._clamp(sum(x["overall_score"] for x in items) / len(items))
            skill_breakdown[skill] = {
                "average_score": avg,
                "questions_evaluated": len(items),
                "performance_band": (
                    "strong" if avg >= 80 else "competent" if avg >= 65
                    else "developing" if avg >= 45 else "needs_improvement"
                ),
                "shallow_answers": sum(bool(x["is_shallow"]) for x in items),
            }

        overall = self._clamp(
            sum(x["overall_score"] for x in evaluations) / len(evaluations)
        )
        return {
            "report_type": "technical_skill_evaluation",
            "candidate_id": candidate_id,
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "overall_score": overall,
            "performance_band": (
                "strong" if overall >= 80 else "competent" if overall >= 65
                else "developing" if overall >= 45 else "needs_improvement"
            ),
            "questions_evaluated": len(evaluations),
            "skill_wise_breakdown": skill_breakdown,
            "question_evaluations": evaluations,
            "review_note": (
                "Automated scores are heuristic evidence indicators, not definitive "
                "judgments. A qualified interviewer must review the answer content "
                "and confirm or adjust the scores."
            ),
        }

    @staticmethod
    def save_report(report: dict[str, Any], json_path: str | Path, markdown_path: str | Path | None = None) -> None:
        json_file = Path(json_path)
        json_file.parent.mkdir(parents=True, exist_ok=True)
        json_file.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        if markdown_path is not None:
            md_file = Path(markdown_path)
            md_file.parent.mkdir(parents=True, exist_ok=True)
            lines = [
                "# Technical Skill Evaluation Report",
                "",
                f"- Candidate: {report['candidate_id']}",
                f"- Overall score: {report['overall_score']}/100",
                f"- Performance band: {report['performance_band']}",
                f"- Questions evaluated: {report['questions_evaluated']}",
                "",
                "## Skill-wise breakdown",
                "",
                "| Skill | Average score | Band | Questions | Shallow answers |",
                "|---|---:|---|---:|---:|",
            ]
            for skill, data in report["skill_wise_breakdown"].items():
                lines.append(
                    f"| {skill} | {data['average_score']} | {data['performance_band']} "
                    f"| {data['questions_evaluated']} | {data['shallow_answers']} |"
                )
            lines += ["", "## Question-level explanations", ""]
            for index, item in enumerate(report["question_evaluations"], 1):
                lines += [
                    f"### {index}. {item['skill']} ({item['difficulty']}, {item['question_type']})",
                    "",
                    f"- Score: {item['overall_score']}/100",
                    f"- Shallow answer: {item['is_shallow']}",
                    f"- Question: {item['question']}",
                    "",
                ]
                for component, detail in item["component_scores"].items():
                    lines.append(f"- **{component.title()} ({detail['score']}/100):** {detail['explanation']}")
                    for evidence in detail["evidence"]:
                        lines.append(f"  - {evidence}")
                if item["shallow_reasons"]:
                    lines.append("- Shallow-answer indicators:")
                    lines.extend(f"  - {reason}" for reason in item["shallow_reasons"])
                lines.append("")
            lines += ["## Review note", "", report["review_note"], ""]
            md_file.write_text("\n".join(lines), encoding="utf-8")
