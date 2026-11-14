---
name: syllabus-backlog-crusher
description: Constructs dependency-aware daily study schedules to clear accumulated syllabus backlogs before deadlines. Use when falling behind on academic coursework targets.
---

# Syllabus Backlog Crusher

## Protocol
1. Inventory -> Catalog backlogged topics.
2. Order -> Sort modules by prerequisite order.
3. Burn-Down -> Allocate daily study blocks.

## Guardrails
- Never output filler or pleasantries.
- Never exceed 8 study hours per day.
- Never schedule dependent topics before prerequisites.

## Output Schema
### Sequence & Burn-Down
1. [Prereq] ([H] hrs) -> Unlocks: [Target]
| Day | Backlog Target | Hours |
- Check: [Date] -> [% Cleared]
