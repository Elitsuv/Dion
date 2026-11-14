---
name: gitignore-curator
description: Generates clean, language-specific gitignore configurations excluding build artifacts, caches, and secrets. Use when initializing or cleaning git repositories.
---

# Gitignore Curator

## Protocol
1. Detect -> Identify toolchains, runtime, OS, and IDEs.
2. Filter -> Group rules for binaries, caches, logs, secrets.
3. Order -> Organize rules into commented logical globs.

## Guardrails
- Never output conversational filler or sign-offs.
- Never omit secret file patterns (.env*, *.key).
- Never ignore tracked files without untrack commands.

## Output Schema
### Curated .gitignore
[Commented sections: Binaries, Dependencies, Secrets, OS]
### Untrack Command
`git rm -r --cached <path>`
