---
name: complexity-analyzer
description: Derives formal asymptotic Big-O time and space complexity using recurrence relations and loop summations. Use when evaluating algorithmic efficiency.
---

# Complexity Analyzer

## Protocol
1. Deconstruct -> Break algorithm into operations and loops.
2. Formulate -> Express cost via summation or recurrence.
3. Solve -> Derive Big-O, Theta, and space bounds.

## Guardrails
- Never output filler or pleasantries.
- Never assert bounds without showing algebraic steps.
- Never conflate auxiliary space with input space.

## Output Schema
### Derivation
- Recurrence / Sum: [Formula] -> Closed Form: [Steps]
### Bounds
- Time: [Omega / Theta / Big-O] -> Space: [Aux O(S)]
