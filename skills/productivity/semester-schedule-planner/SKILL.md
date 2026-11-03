---
name: semester-schedule-planner
description: Organizes engineering course syllabi, assignments, exams, and project deadlines into an integrated semester timeline. Use when planning academic workloads.
---

# Semester Schedule Planner

Consolidate course syllabi, assignment due dates, and examination schedules into an integrated semester timeline.

## Trigger Conditions

Activate this skill when:
- A user provides course syllabi or a list of semester deadlines and asks for a unified schedule.
- A student asks: 'Plan my semester schedule', 'Organize these assignment due dates', or 'How do I balance these 5 engineering courses?'.

## Execution Protocol

Execute this academic planning sequence:

### 1. Course Ingestion & Deadline Extraction
- Extract all deliverables across courses:
  - Course code and credit weighting.
  - Weekly homeworks, lab submissions, midterm dates, final projects, and final exams.

### 2. High-Conflict Crunch Period Identification
- Identify weeks where multiple major assignments or exams collide (e.g., 'Week 8: 2 midterms and 1 capstone milestone').
- Formulate an early-start buffer strategy (starting deliverables 10–14 days in advance of crunch weeks).

### 3. Chronological Master Timeline
- Tabulate deadlines chronologically:
  | Week / Date | Course | Deliverable | Weight | Recommended Start Date |
  | :--- | :--- | :--- | :--- | :--- |
  | Oct 14 | CS 301 | Lab 3: Cache Simulation | 10% | Oct 07 |
  | Oct 18 | EE 204 | Midterm Exam | 25% | Oct 04 (Review) |

### 4. Weekly Workload Distribution
- Allocate estimated study/build hours per course based on credit hours and difficulty.

## Output Quality Rules

- Flag hard deadlines versus flexible checkpoint milestones.
- Provide actionable, realistic start dates for large projects to prevent last-minute cramming.
