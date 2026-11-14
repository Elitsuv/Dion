---
name: git-commit-architect
description: Structures atomic git commits and drafts conventional commit messages with clear engineering rationale. Use when staging changes or preparing pull requests.
---

# Git Commit Architect

## Protocol
1. Partition -> Split diffs into atomic single-intent commits.
2. Header -> Draft Conventional Commit header with valid type.
3. Context -> Document motivation and behavioral impact.

## Guardrails
- Never output filler or pleasantries.
- Never bundle unrelated changes into one commit.
- Never exceed 72 characters in commit headers.

## Output Schema
### Staging & Message
- Commit [N]: [Files] -> Scope: [Single intent]
`<type>(<scope>): <summary>`
- Why: [Motivation] -> Impact: [What changed]
