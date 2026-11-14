---
name: merge-conflict-resolver
description: Guides step-by-step resolution of git merge and rebase conflicts without data loss. Use when git operations halt with conflict markers.
---

# Merge Conflict Resolver

## Protocol
1. Locate -> Identify conflict markers (`<<<<<<<`, `=======`).
2. Reconcile -> Combine incoming and current intents.
3. Verify -> Remove markers, build project, and test.

## Guardrails
- Never output filler or pleasantries.
- Never discard branch changes without diff analysis.
- Never leave conflict markers in working files.

## Output Schema
### Reconciliation
- File: [Path:Lines] -> Intent: [Current vs Incoming]
[Clean resolved code block]
`git add <file> && git commit -m "fix: resolve conflict"`
