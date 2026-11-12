# Day 36 - Confidence & Stress Indicators

## Objective

Identify possible hesitation, sentiment, contradiction, and stress-related
language signals in candidate responses.

## Workflow

Candidate Response
        |
        v
Normalize Text
        |
        v
Detect Hesitation
        |
        +---- Long Pause Markers
        +---- Repeated Words
        +---- Uncertainty Phrases
        |
        v
Analyze Sentiment Wording
        |
        v
Identify Potential Contradictions
        |
        v
Analyze Stress-Related Phrases
        |
        v
Calculate Behavioral Confidence Signal Score
        |
        v
Generate Explainable JSON and Markdown Reports

## Detailed Tasks

1. Detect hesitation patterns.
2. Identify positive and negative wording.
3. Flag possible contradiction patterns.
4. Detect predefined stress-related phrases.
5. Generate a prototype behavioral confidence score.

## Behavioral Confidence Signal Score

The score begins at 70 and applies predefined adjustments for:
- Uncertainty phrases
- Repeated words
- Explicit long-pause markers
- Hesitation words
- Positive wording

The final result is limited to a 0-100 range.

This formula is experimental and is not a scientifically validated confidence
measurement.

## Important Limitations

- Text cannot reliably determine actual confidence or emotional state.
- Pauses are detected only if they are included as transcript markers.
- Sentiment uses a small predefined vocabulary.
- Potential contradictions require contextual human review.
- The score must not be used alone for hiring decisions.
