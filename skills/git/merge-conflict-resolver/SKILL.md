---
name: merge-conflict-resolver
description: Guides students step-by-step through resolving complex git merge and rebase conflicts without data loss. Use when git operations halt with conflict markers.
---

# Merge Conflict Resolver

Diagnose and safely resolve git merge and rebase conflicts without losing code or breaking repository state.

## Trigger Conditions

Activate this skill when:
- A user's git pull, merge, or rebase halts with `CONFLICT (content): Merge conflict in ...`.
- A student asks: 'How do I resolve this merge conflict?', 'Fix this git conflict in my file', or 'What does HEAD vs incoming change mean?'.

## Execution Protocol

Execute this conflict resolution protocol:

### 1. Conflict State Diagnosis
- Inspect the conflict markers in the affected file:
  ```text
  <<<<<<< HEAD (Current change / your branch)
  local code
  =======
  incoming code
  >>>>>>> branch-name (Incoming change)
  ```
- Identify the semantic intent of both modifications (did both sides edit the same function, rename a variable, or modify imports?).

### 2. Step-by-Step Resolution
- Walk through combining both modifications logically:
  - Keep necessary parts from both branches.
  - Delete conflict marker lines (`<<<<<<<`, `=======`, `>>>>>>>`).
  - Reconcile variable names and imports.

### 3. Finalization Commands
- Provide the exact terminal commands to complete the operation:
  ```bash
  # Check status of resolved files
  git status
  # Stage resolved file
  git add <filename>
  # Complete merge or continue rebase
  git commit -m "merge: resolve conflicts in <module>"
  # OR if rebasing:
  git rebase --continue
  ```

### 4. Emergency Abort Guard
- Provide the emergency command to return to clean state if the student gets lost:
  ```bash
  git merge --abort  # OR git rebase --abort
  ```

## Output Quality Rules

- Never instruct students to blindly delete either side of a conflict without verifying intent.
- Always remind the user to run tests immediately following conflict resolution.
