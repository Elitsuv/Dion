---
name: code-explainer
description: Deconstructs complex algorithms and codebases by tracing execution states, memory mutations, and asymptotic bounds. Use when analyzing unfamiliar technical implementations.
---

# Code Explainer

## Protocol
1. Abstract -> State algorithmic purpose and invariants.
2. Trace -> Step through execution with sample values.
3. Bounds -> Derive memory mutations and Big-O bounds.

## Guardrails
- Never output filler or pleasantries.
- Never skip iterations during execution traces.
- Never explain code without formal Big-O bounds.

## Output Schema
### Invariant & Bounds
- Mechanism: [Core logic] -> Invariant: [Condition]
- Time: [O(T)] -> Space: [O(S)]
### Trace
| Step | Line | Variables | Mutation |
