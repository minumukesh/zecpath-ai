# Day 7 – Storage Structure Documentation

## 1. Purpose

The storage structure defines how Zecpath stores resumes, parsed candidate profiles, job profiles, ATS scores, screening reports, interview results, datasets, and AI model versions.

The structure separates raw documents, processed data, AI-generated results, training datasets, and model versions.

## 2. Storage Structure

```text
data/
├── job_descriptions/
│   ├── raw/
│   ├── parsed/
│   └── structured/
│
├── resumes/
│   ├── raw/
│   └── parsed/
│
├── ats/
│   └── scores/
│
├── screening/
│   └── reports/
│
└── interviews/
    └── results/

datasets/
├── training/
├── validation/
└── test/

models/
└── versions/