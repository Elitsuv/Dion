---
name: exam-drill
description: Generates high-yield practice problems, edge-case questions, and conceptual drills tailored for engineering exams and technical assessments. Use when a student requests test preparation, practice questions, or concept verification.
---

# Exam Drill

Generate rigorous, exam-style practice questions with formal grading criteria.

## Trigger Conditions

Activate this skill when:
- A user asks to test their knowledge, drill for an exam, or practice university coursework concepts.
- A user requests: "Quiz me on virtual memory", "Give me hard graph algorithm questions", or "Test my understanding of concurrency".

## Execution Protocol

Follow this structured sequence:

### 1. Topic & Difficulty Calibration
- Confirm the target engineering topic (e.g., Operating Systems, Distributed Systems, Compilers, Algorithms).
- Calibrate against exam difficulty standards:
  - **Level 1 (Foundational)**: Direct state calculation, memory layout tracing, Big-O derivation.
  - **Level 2 (Analytical)**: Edge-case boundary analysis, race condition identification, invariant verification.
  - **Level 3 (Design / Synthesis)**: Trade-off trade analysis between two constrained architectures.

### 2. Multi-Part Question Construction
- Construct 2–3 questions mirroring university examination formats:
  - **Part A (Mechanics / Trace)**: Provide a specific code segment or data structure state and demand the exact execution trace or memory state.
  - **Part B (Boundary Failure)**: Identify the exact input condition that triggers failure or asymptotic degradation.
  - **Part C (Counter-Example / Invariant)**: Disprove a common misconception by providing a concrete counter-example.

### 3. Concealed Solutions & Marking Scheme
- Present the questions cleanly first.
- Provide full, step-by-step solutions beneath a spoiler fold or distinct answer key section:
  - Point-by-point grading rubric (e.g., [2 pts] for identifying base case, [3 pts] for recurrence relation).
  - Explicit explanation of common incorrect student answers.

## Output Quality Rules

- Never generate trivial multiple-choice questions unless specifically requested.
- Ensure all questions have objective, mathematically verifiable answers.
- Avoid vague prompts like "Explain your thoughts"—use exact prompts like "Calculate the total page faults under LRU given page reference string S".

