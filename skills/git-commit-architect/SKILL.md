---
name: git-commit-architect
description: Structures atomic commits, writes conventional commit messages with contextual rationale, and formats reviewable Pull Requests. Use when a user needs to commit changes, clean up git history, or prepare a PR.
---

# Git Commit Architect

Structure atomic commits, enforce conventional syntax, and format reviewable Pull Requests.

## Trigger Conditions

Activate this skill when:
- A user asks: "How should I commit these changes?", "Write a commit message for this diff", or "Help me draft a Pull Request".
- A user provides a `git diff`, `git status`, or list of modified files and needs structured commit messages.

---

## Execution Protocol

Follow this structured workflow:

### 1. Atomic Change Separation
- Audit changes to ensure each commit represents an atomic logical unit:
  - Separate style, formatting, and linting fixes from functional changes.
  - Separate unrelated bug fixes into independent commits.
  - Exclude temporary debug code, `.env` files, and local build artifacts.
- If multiple concerns are mixed, provide instructions to split them into separate commits.

### 2. Conventional Commit Construction
- Format headers using standard Conventional Commits syntax:
  ```text
  <type>(<optional-scope>): <imperative subject in lowercase, max 50 chars>
  ```
- Use standardized types:
  - `feat`: New user-facing capability.
  - `fix`: Repair of broken behavior.
  - `refactor`: Internal restructure that alters neither features nor fixes.
  - `perf`: Performance optimization.
  - `test`: Addition or correction of tests.
  - `docs`: Documentation updates.
  - `chore`: Build configuration, dependencies, or tool settings.

### 3. Imperative Header Rules
- Use imperative, present-tense verbs (`add`, `fix`, `refactor`, not `added`, `fixes`, `refactoring`).
- Do not capitalize the first character after the colon.
- Do not include a trailing period.
- Strictly adhere to the 50-character limit for the subject line.

### 4. Contextual Commit Body
- When changes are non-trivial, provide a body that answers two fundamental questions:
  1. **Why is this change necessary?** (State the underlying defect, race condition, or requirement).
  2. **How does this change resolve it?** (State the architectural or algorithmic mechanism).

**Example**:
```text
fix(auth): prevent session race condition during concurrent token refresh

When multiple asynchronous requests trigger a token refresh simultaneously,
secondary requests read stale tokens from local cache before the write
completes, triggering spurious 401 Unauthorized errors.

Mutex-guard the token refresh routine and broadcast the newly acquired
session token to all pending requests via an in-memory event emitter.

Fixes #42
```

### 5. Pull Request Synthesis
- When drafting a Pull Request, format the description using this structure:
  - **Summary**: Concise bullet points covering the changes.
  - **Motivation**: Problem context or issue link.
  - **Testing Performed**: Exact commands executed, test cases added, and manual verification steps.
  - **Checklist**: All tests passing, documentation updated, no debug residue.

---

## Output Quality Rules

- Reject vague messages like "update", "wip", "fixed bug", or "cleanup".
- Ensure commits are bisectable: each commit must independently compile and pass tests.
