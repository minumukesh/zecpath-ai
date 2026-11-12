# ZECPATH-AI Day 49
# Malpractice and Integrity Detection Framework

## 1. Objective

Design an explainable framework that identifies unusual interview-session
events and sends them for human review.

The system does not determine whether a candidate has cheated.

## 2. Malpractice Signals

| Signal | Observable event | Limitation |
|---|---|---|
| Tab switching | Interview tab loses active status | May be legitimate |
| Screen focus loss | Interview window loses focus | Does not prove external assistance |
| External voice | Background voice event | Does not identify the speaker |
| Looking away | Recorded gaze-direction event | Not evidence of cheating |
| Repeated patterns | Similar events occur repeatedly | Requires context review |

## 3. Detection Logic

The engine compares event counts against configurable thresholds.

A signal is flagged when its observed event count reaches or exceeds
its configured threshold.

Multiple different flagged signals produce a multi-signal review pattern.

A threshold flag is an alert for investigation, not a misconduct verdict.

## 4. Warning and Flagging System

- Threshold alert: a configured event threshold is reached.
- Pattern alert: multiple signal categories exceed thresholds.
- Review tag: indicates the priority for human review.
- Consent alert: blocks assessment if informed consent is missing.

## 5. Review Indicator

The engine calculates a configurable event-based review indicator.
It is not a probability of cheating, a validated integrity score,
or a candidate suitability score.

## 6. Integration with Day 48

Day 48 records contextual behavioral observations.
Day 49 records interview-session integrity events.

The two modules can be displayed together in a review dashboard.
Their outputs must remain separate and must not be combined into an
automatic candidate ranking.

## 7. Human Review

A trained reviewer should:
1. Review the original event context.
2. Check for technical issues.
3. Consider accessibility accommodations.
4. Ask the candidate for an explanation where appropriate.
5. Record the review outcome and rationale.
6. Allow correction or challenge of inaccurate records.

## 8. Privacy and Fairness

- Obtain informed consent before monitoring.
- Collect only necessary event metadata.
- Do not record or identify background speakers unnecessarily.
- Avoid facial recognition and emotion detection.
- Define access controls and retention periods.
- Support accessibility tools and accommodations.
- Do not make automated rejection decisions.
- Audit false-positive rates and system performance.

## 9. Technical Architecture

Interview session
       |
       v
Consent verification
       |
       v
Event collection
       |
       v
Input validation
       |
       v
Threshold-based detection
       |
       v
Pattern recognition
       |
       v
Warning and review flags
       |
       v
Explainable JSON report
       |
       v
Human review

## 10. Limitations

This is a rule-based research prototype. It does not include browser
instrumentation, live audio monitoring, computer vision, or real-time
production alert delivery. Those integrations require separate
privacy, security, consent, and validation work.

## 11. Deliverables

- Integrity detection framework
- Malpractice detection logic
- Risk flagging system design
- Python detection engine
- Unit tests
- Demonstration script
- Sample JSON report
