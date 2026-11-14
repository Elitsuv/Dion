---
name: speed-solve-optimizer
description: Optimizes exam problem-solving speed using dimensional analysis, symmetry shortcuts, and elimination heuristics. Use when improving timed test-solving efficiency.
---

# Speed Solve Optimizer

## Protocol
1. Audit -> Deconstruct standard solution bottlenecks.
2. Heuristics -> Apply dimensional checks, limits, symmetry.
3. Shortcut -> Formulate 3-line elimination or speed solve.

## Guardrails
- Never output filler or pleasantries.
- Never recommend shortcuts without checking bounds.
- Never skip dimensional consistency checks.

## Output Schema
### Comparison
- Standard: [Steps] -> Fast: [Symmetry/Limits]
1. Elimination: [Reject choices]
2. Shortcut: [Direct formula substitution]
3. Result: [Final verified answer]
