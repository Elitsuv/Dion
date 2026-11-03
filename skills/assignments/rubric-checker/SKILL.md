---
name: rubric-checker
description: Evaluates assignment drafts against official grading rubrics and assignment criteria to identify missing requirements. Use before submitting an assignment to maximize grade accuracy.
---

# Rubric Checker

Audit academic assignments and engineering projects against official scoring rubrics before final submission.

## Trigger Conditions

Activate this skill when:
- A user provides an assignment draft alongside a grading rubric or syllabus criteria.
- A student asks: 'Does this meet the assignment rubric?', 'What am I missing for full marks?', or 'Check my report against these grading requirements'.

## Execution Protocol

Follow this rigorous audit workflow:

### 1. Rubric Ingestion & Criterion Weighting
- Parse the grading rubric into discrete weighted categories (e.g., Correctness: 40%, Performance: 20%, Code Style: 20%, Documentation: 20%).
- Extract explicit baseline disqualifiers (e.g., memory leak zero-tolerance, missing Makefile, non-compliant directory structure).

### 2. Line-by-Line Compliance Gap Analysis
- Evaluate the submission against every line item in the rubric:
  | Criterion | Maximum Score | Estimated Score | Status | Compliance Evidence / Missing Requirement |
  | :--- | :--- | :--- | :--- | :--- |
  | Input Validation | 10 pts | 10 pts | Fully Met | Handles invalid tokens with custom error codes. |
  | Memory Safety | 15 pts | 8 pts | Partially Met | Leaks 64 bytes on early return in parser. |

### 3. High-Priority Remediations
- List items that represent the highest point deductions first.
- Provide direct, concrete instructions on how to close each gap before submission.

### 4. Edge-Case & Formatting Sanity Checks
- Verify formatting specifications: page limits, naming conventions, required zip structure, and citation format.

## Output Quality Rules

- Be strict and conservative with point estimations; err on the side of rigorous grading.
- Point to specific sections or lines where evidence is lacking.
