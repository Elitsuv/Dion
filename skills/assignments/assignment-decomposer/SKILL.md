---
name: assignment-decomposer
description: Deconstructs complex assignment rubrics into milestone subtasks, dependency sequences, and verification tests. Use when planning an academic coursework submission.
---

# Assignment Decomposer

## Protocol
1. Deconstruct -> Parse rubric weights and deadlines.
2. Sequence -> Order subtasks with prerequisite links.
3. Verify -> Define pass/fail checks per milestone.

## Guardrails
- Never output filler or pleasantries.
- Never create milestones lacking pass/fail tests.
- Never omit prerequisite subtask dependencies.

## Output Schema
### Milestone Map
- Task [N]: [Item] -> Prereqs: [IDs] -> Done: [Test]
### Sequence
[Step A] -> [Step B] -> [Submission]
