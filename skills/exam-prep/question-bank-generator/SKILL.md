---
name: question-bank-generator
description: Generates tiered practice questions from foundational to advanced trap levels with hidden solutions. Use when practicing a topic or syllabus module.
---

# Question Bank Generator

## Protocol
1. Extract -> Map syllabus principles and traps.
2. Tier -> Draft Tier 1 (Recall), Tier 2 (Apply), Tier 3 (Trap).
3. Solutions -> Encapsulate derivations in hidden tags.

## Guardrails
- Never output filler or pleasantries.
- Never write questions lacking answers.
- Never reveal trap solutions in initial prompts.

## Output Schema
### Tiered Questions
- T1 (Recall): [Problem] -> Sol: [Proof]
- T2 (Apply): [Problem] -> Sol: [Proof]
- T3 (Trap): [Problem] -> Autopsy: [Trap]
