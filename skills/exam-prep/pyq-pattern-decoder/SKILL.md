---
name: pyq-pattern-decoder
description: Extracts recurring question archetypes, high-yield subtopics, and traps from past exam papers. Use when planning exam strategy or paper analysis.
---

# PYQ Pattern Decoder

## Protocol
1. Cluster -> Group past questions into archetypes.
2. Rank -> Prioritize topics by frequency and marks.
3. Catalog -> Extract distractor tricks and pitfalls.

## Guardrails
- Never output filler or pleasantries.
- Never summarize papers without frequency ranks.
- Never declare topics skippable without risk levels.

## Output Schema
### PYQ Archetypes
| Archetype | Frequency | Core Law | Recurring Trap |
- Priority: [Top topics] -> Trap Alert: [Common trick]
