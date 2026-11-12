# Day 33 - HR Interview Engine Design

## Objective

Design the foundational architecture of the AI HR Interview system.

## 1. Interview Categories

The engine organizes questions into six categories:

1. Self-introduction
2. Career journey
3. Strengths and weaknesses
4. Teamwork and culture fit
5. Career goals
6. Availability and commitment

## 2. Role-Based Question Generation

Questions are selected using two profile settings:

- Experience: fresher or experienced
- Role type: technical or non-technical

This produces different question sets for different candidate profiles.

## 3. Interview State

Each interview stores:

- Interview ID
- Candidate ID
- Job role
- Experience level
- Role type
- Current phase
- Question ID
- Captured response
- Follow-up eligibility
- Interview status

## 4. Workflow Diagram

Candidate Profile
        |
        v
Select Experience Level and Role Type
        |
        v
Generate HR Question Bank
        |
        v
Start Interview
        |
        v
Introduction
        |
        v
Core HR Questions
        |
        v
Role-Based Evaluation
        |
        v
Closing
        |
        v
Save Responses and Interview Report

## 5. Response Workflow

Current Question
        |
        v
Capture Candidate Response
        |
        v
Store Response with Question ID
        |
        v
Check Whether Response Is Missing
        |
        +---- Missing ----> Mark Follow-Up Eligible
        |
        +---- Present ----> Continue to Next Question
        |
        v
Update Interview State
        |
        v
Generate Interview Summary

## 6. API Design Concept

The HR interview engine can be called by an API layer.

Suggested operations:

- Create an interview
- Retrieve the current question
- Submit a response
- Retrieve interview progress
- Export the interview report

These are design-level operations. They must be connected to actual API routes before they can be described as live endpoints.

## 7. Deliverables

- HR interview structure
- Role-based question bank
- Interview state structure
- Response capture logic
- Follow-up eligibility
- Interview flow documentation
- JSON interview report

## 8. Limitations

This implementation provides question generation and interview-state management.
It does not perform speech recognition, judge answer quality, or make hiring
decisions. Those capabilities require their own integration and validation.
