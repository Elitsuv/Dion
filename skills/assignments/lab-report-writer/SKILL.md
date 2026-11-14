---
name: lab-report-writer
description: Structures engineering laboratory reports with formal abstracts, error propagation models, and tabular observations. Use when drafting scientific or lab submissions.
---

# Lab Report Writer

## Protocol
1. Model -> State apparatus and governing equations.
2. Tabulate -> Record values with SI units and errors.
3. Analyze -> Compute percent error vs reference.

## Guardrails
- Never output filler or pleasantries.
- Never omit SI units or error tolerances.
- Never assert unverified empirical claims.

## Output Schema
### Model & Data
- Law: [Equation] -> Invariant: [Condition]
| Metric | Measured | Reference | Error % |
### Finding
[Quantitative summary]
