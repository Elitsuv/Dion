---
name: branch-strategy-planner
description: Designs clean git branch and release workflows (Git Flow, GitHub Flow, Trunk-Based) for student project teams. Use when coordinating collaborative team repositories.
---

# Branch Strategy Planner

Design clean, conflict-free git branching and collaboration workflows for student engineering teams.

## Trigger Conditions

Activate this skill when:
- A team of students is starting a group coding project and needs a branching model.
- A user asks: 'How should my team organize our git branches?', 'Set up GitHub Flow for our project', or 'What branch strategy should we use for our capstone?'.

## Execution Protocol

Follow this git collaboration setup:

### 1. Team Size & Workflow Calibration
- Select the appropriate model:
  - **GitHub Flow (Recommended for student teams)**: Short-lived feature branches branching from `main`, merged via Pull Requests.
  - **Git Flow (Complex releases)**: `develop`, `release`, `hotfix`, and `feature` branches.

### 2. Standardized Branch Naming Conventions
- Enforce strict kebab-case branch prefixes:
  - `feat/<short-description>`: New features.
  - `fix/<bug-identifier>`: Bug fixes.
  - `refactor/<target-module>`: Code restructuring.
  - `docs/<subject>`: Documentation updates.

### 3. Pull Request Review & Protection Rules
- Establish repository settings rules:
  - Require branch protection on `main`.
  - Require at least 1 peer approval before merge.
  - Require automated test checks to pass before merging.

### 4. Merge vs Rebase Policy
- Clarify whether the team uses Squash and Merge (linear history) or standard Merge Commits.

## Output Quality Rules

- Provide concrete git commands for creating, synchronizing, and cleaning up branches.
- Keep the workflow simple to prevent git merge nightmares in student teams.
