---
name: semester-schedule-planner
description: Organizes academic course syllabi, assignments, exams, and project milestones into a structured semester timeline. Use when planning coursework workloads.
---

# Semester Schedule Planner

## Protocol
1. Ingest -> Consolidate syllabus deadlines.
2. Deconflict -> Identify collision weeks.
3. Buffer -> Set milestones 7 days before dues.

## Guardrails
- Never output filler or pleasantries.
- Never schedule deadlines without recovery buffers.
- Never omit grade weights from prioritization.

## Output Schema
### Collision Weeks
- Week [N]: [Colliding deadlines] -> Buffer: [Date]
| Week | Course | Milestone | Due | Buffer |
