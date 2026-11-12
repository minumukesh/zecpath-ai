# Day 46 - Technical Interview AI Blueprint

## Objective
Design a scalable AI system capable of conducting role-based technical interviews.

## Interview structure
1. Introduction
2. Experience-based questions
3. Conceptual questions
4. Scenario-based problems

## Experience-based logic
| Experience | Level | Focus |
|---|---|---|
| 0-2 years | Basic | Fundamentals |
| 3 to less than 5 years | Intermediate | Practical application |
| 5+ years | Advanced | Advanced concepts and system design |

The implementation maps 0-2 years to basic, 3 to less than 5 years to intermediate, and 5+ years to advanced. This resolves the overlap at exactly 5 years by following the explicit 5+ advanced requirement.

## Role to skill mapping
| Role | Skill domains |
|---|---|
| MERN | JavaScript, React, Node.js, Express, MongoDB, REST APIs |
| Java | Java, OOP, Spring Boot, Hibernate, SQL, REST APIs |
| DevOps | Linux, Git, Docker, CI/CD, Kubernetes, Cloud |

## Question hierarchy
```text
Technical Interview
|-- Introduction
|-- Experience
|-- Conceptual
|   |-- Basic
|   |-- Intermediate
|   `-- Advanced
`-- Scenario
    |-- Basic
    |-- Intermediate
    `-- Advanced
```

## Interview flow states
created -> introduction -> experience -> conceptual -> scenario -> completed.
Cancellation is permitted from each active state.

## State transition diagram
```mermaid
stateDiagram-v2
    [*] --> created
    created --> introduction
    created --> cancelled
    introduction --> experience
    introduction --> cancelled
    experience --> conceptual
    experience --> cancelled
    conceptual --> scenario
    conceptual --> cancelled
    scenario --> completed
    scenario --> cancelled
    completed --> [*]
    cancelled --> [*]
```

## Interview workflow
```mermaid
flowchart TD
 A[Candidate Profile] --> B[Select Job Role]
 B --> C[Map Skill Domains]
 C --> D[Read Experience]
 D --> E[Select Difficulty]
 E --> F[Build Interview Structure]
 F --> G[Introduction]
 G --> H[Experience Questions]
 H --> I[Conceptual Questions]
 I --> J[Scenario Problems]
 J --> K[Store Answers]
 K --> L[Interview Completion]
```

## Scope limitation
This implementation generates role-based interview blueprints and manages interview states. It does not implement live voice interviewing, automatic code execution, adaptive question selection based on answer quality or a validated technical answer-scoring model.