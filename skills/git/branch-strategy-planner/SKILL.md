---
name: branch-strategy-planner
description: Designs clean git branching and release workflows like GitHub Flow and Trunk-Based Development. Use when establishing collaborative team version control.
---

# Branch Strategy Planner

## Protocol
1. Assess -> Evaluate team size, targets, and cadence.
2. Model -> Select Trunk-Based, GitHub Flow, or Git Flow.
3. Policies -> Define branch taxonomy, PR gates, merge rules.

## Guardrails
- Never output filler or pleasantries.
- Never recommend complex branching where trunk-based works.
- Never permit unprotected default branches.

## Output Schema
### Branch Architecture
- Model: [Trunk-Based | GitHub Flow] -> Taxonomy: `feat/`, `fix/`
- Gates: [Merge strategy & required checks]
