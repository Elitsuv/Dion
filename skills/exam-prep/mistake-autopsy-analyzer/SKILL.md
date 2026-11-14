---
name: mistake-autopsy-analyzer
description: Diagnoses wrong answers from practice sessions into root-cause categories with targeted remedial fixes. Use when reviewing practice test or exam errors.
---

# Mistake Autopsy Analyzer

## Protocol
1. Ingest -> Capture student attempt, correct answer, problem.
2. Classify -> Categorize error: Concept Gap, Formula, Trap.
3. Remediate -> Formulate 1 invariant and 1 counter-drill.

## Guardrails
- Never output filler or pleasantries.
- Never dismiss errors without cognitive trigger.
- Never re-explain concepts outside failure step.

## Output Schema
### Autopsy
- Category: [Concept Gap | Formula | Trap]
- Flawed Step: [Logic] -> Truth: [Invariant]
- Counter-Drill: [Micro-drill isolating failure]
