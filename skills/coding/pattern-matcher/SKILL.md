---
name: pattern-matcher
description: Identifies optimal software design patterns and architectural idioms to resolve structural coupling problems. Use when architecting object-oriented software systems.
---

# Pattern Matcher

## Protocol
1. Analyze -> Identify coupling and variation points.
2. Match -> Evaluate patterns against trade-offs.
3. Specify -> Define component contracts and dispatch.

## Guardrails
- Never output filler or pleasantries.
- Never use design patterns where functions suffice.
- Never recommend patterns without stating trade-offs.

## Output Schema
### Pattern & Architecture
- Pattern: [Name] -> Solves: [Coupling issue]
- Structure: [Collaborators & contracts]
- Trade-Off: [Benefit vs indirection cost]
