# Zecpath AI ATS Architecture

## 1. High-Level Architecture

Candidate Resume
        |
        v
Resume Extraction
        |
        v
Resume Section Segmentation
        |
        +-------------------+
        |         |         |
        v         v         v
     Skills   Experience  Education
        |         |         |
        +---------+---------+
                  |
                  v
          Candidate Analysis
                  |
                  v
          Semantic Matching
                  ^
                  |
          Job Description
                  |
                  v
           Job Profile
                  |
                  v
           ATS Scoring
                  |
                  v
        Candidate Ranking
                  |
          +-------+-------+
          |       |       |
          v       v       v
      SHORTLIST REVIEW AUTO-REJECT

## 2. Processing Architecture

Resume
  |
  v
Text Extraction
  |
  v
Section Segmentation
  |
  +----> Skill Extraction
  |
  +----> Experience Parsing
  |
  +----> Education & Certification
  |
  v
Candidate Analysis
  |
  v
Semantic Matching
  |
  v
Day 13 ATS Scoring
  |
  v
Day 14 Candidate Ranking
  |
  v
Decision Zone

## 3. API Architecture

Backend System
      |
      v
REST API
      |
      +----> Resume Upload
      |
      +----> Resume Parsing
      |
      +----> Resume Scoring
      |
      +----> Shortlisting
      |
      +----> Job Status
      |
      v
ATS Pipeline
      |
      v
ATS Processing
      |
      v
Scoring
      |
      v
Ranking
      |
      v
ATS Result

## 4. Optimization Architecture

Resume + Job Description
          |
          v
Optimized ATS Pipeline
          |
          v
Efficient Extraction
          |
          v
Resume Cleaning
          |
          v
Entity Detection
          |
          v
Existing ATS Pipeline
          |
          v
Existing ATS Scoring
          |
          v
Existing Candidate Ranking
          |
          v
ATS Result

## 5. Architectural Principle

Day 18 optimization is an additional processing layer.

It does not replace or duplicate the existing ATS scoring and ranking
components.
