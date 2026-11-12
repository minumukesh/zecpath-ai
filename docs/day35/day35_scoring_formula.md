# Day 35 - Communication Skill Evaluation

## Objective

Evaluate written candidate responses using consistent, explainable rules.

## Workflow

Candidate Response
        |
        v
Normalize Text
        |
        v
Detect Filler Words
        |
        v
Evaluate Five Components
        |
        +---- Fluency
        |
        +---- Grammar Quality
        |
        +---- Vocabulary Range
        |
        +---- Clarity
        |
        +---- Answer Structure
        |
        v
Normalize Components to 0-100
        |
        v
Apply Component Weights
        |
        v
Calculate Final Communication Score
        |
        v
Generate Explainable JSON and Markdown Reports

## Scoring Formula

Final Score =
    (Fluency x 0.25)
  + (Grammar Quality x 0.20)
  + (Vocabulary Range x 0.15)
  + (Clarity x 0.25)
  + (Answer Structure x 0.15)

All component scores use a 0-100 scale. The weights total 1.00.

## Component Weights

- Fluency: 25%
- Grammar quality: 20%
- Vocabulary range: 15%
- Clarity of explanation: 25%
- Answer structure: 15%

## Filler Word Detection

The prototype detects predefined expressions such as "um", "uh",
"you know", and "basically" in the text transcript.

## Bias Reduction

The same component weights and normalization scale are used for all samples.
The prototype does not use a candidate's name, demographic identity, accent,
or personal background as a scoring feature.

Consistent rules alone do not prove fairness. The model requires testing
across different roles, languages, response lengths, and candidate groups.

## Limitations

This is a text-based heuristic prototype.

- It does not measure actual speech fluency, pronunciation, pauses, or pace.
- Grammar detection checks a small set of patterns.
- Vocabulary variety is not a measure of intelligence or job suitability.
- Structural phrases are indicators, not mandatory requirements.
- A communication score must not be the sole basis for a hiring decision.
- Human review is required before using results in real recruitment.
