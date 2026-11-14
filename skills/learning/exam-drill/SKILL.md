---
name: exam-drill
description: Generates high-yield practice problems, edge-case drills, and verification questions for engineering exams. Use when preparing for tests or concept assessments.
---

# Exam Drill

## Protocol
1. Target -> Identify high-frequency exam concepts and traps.
2. Draft -> Generate 3 exam-style problems with constraints.
3. Solutions -> Provide hidden step-by-step solutions and marks.

## Guardrails
- Never output filler or pleasantries.
- Never create trivial questions; test exam edge traps.
- Never show final answers without intermediate derivation.

## Output Schema
### Exam Problems
- Q[N] ([Pts] pts): [Problem statement]
### Solutions
<details><summary>Sol Q[N]</summary>[Working steps & Trap]</details>
