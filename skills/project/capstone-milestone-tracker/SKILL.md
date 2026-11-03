---
name: capstone-milestone-tracker
description: Breaks multi-month senior design or capstone projects into bi-weekly deliverables with risk assessments and verification criteria. Use when tracking long-term projects.
---

# Capstone Milestone Tracker

Structure multi-month engineering capstone projects into prioritized bi-weekly deliverables with contingency plans.

## Trigger Conditions

Activate this skill when:
- A student is embarking on a semester or year-long senior design / capstone project.
- A user asks: 'Create a milestone schedule for my capstone', 'How do I plan my 4-month engineering project?', or 'Break down my senior project timeline'.

## Execution Protocol

Follow this phased project management sequence:

### 1. Project Charter & Scope Baseline
- Define the primary engineering deliverable and the evaluation criteria.
- Identify external hardware, server access, or dataset dependencies.

### 2. Bi-Weekly Milestone Schedule
Structure the project into 8 bi-weekly sprints:
- **Weeks 1–2 (Feasibility & Literature Review)**: Requirements finalization, tech stack verification, hello-world prototype.
- **Weeks 3–4 (Core Data Model & Skeleton)**: Schema setup, API skeleton, CI/CD pipeline.
- **Weeks 5–6 (Primary Feature Implementation)**: Core algorithmic engine or service workflows.
- **Weeks 7–8 (Midterm Progress Review & MVP)**: Working end-to-end demo proving core loop.
- **Weeks 9–10 (Secondary Capabilities & Refinement)**: Analytics, export features, performance tuning.
- **Weeks 11–12 (System Testing & Hardening)**: Integration test suite, boundary stress testing, security checks.
- **Weeks 13–14 (Documentation & Deployment)**: Capstone report draft, containerized deployment.
- **Weeks 15–16 (Final Polish & Presentation Defense)**: Slide deck completion, demo rehearsal, poster design.

### 3. Risk Matrix & Contingency Triggers
- Identify the 3 highest technical risks and define trigger conditions to pivot or scale back scope:
  | Risk Item | Likelihood | Impact | Mitigation Strategy / Fallback Trigger |
  | :--- | :--- | :--- | :--- |
  | Sensor latency too high | Medium | High | Fallback to pre-recorded dataset if driver unverified by Week 4 |

## Output Quality Rules

- Keep milestones measurable with explicit completion evidence (e.g., 'API passes 20 integration tests').
- Avoid front-loading all implementation into the final weeks.
