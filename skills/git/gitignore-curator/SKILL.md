---
name: gitignore-curator
description: Generates clean, language-specific .gitignore files that exclude build artifacts, virtual environments, and secrets. Use when setting up or cleaning git repositories.
---

# Gitignore Curator

Generate clean, comprehensive, and tailored .gitignore files preventing accidental commits of binaries, secrets, and environment artifacts.

## Trigger Conditions

Activate this skill when:
- A user is creating a new repository or accidentally committed virtual environments or binaries.
- A student asks: 'Generate a .gitignore for Python and React', 'What should I put in my C++ .gitignore?', or 'How do I stop git from tracking build files?'.

## Execution Protocol

Follow this git exclusion curation sequence:

### 1. Tech Stack Detection & Layering
Combine exclusions across all layers of the project:
- Operating system artifacts (`.DS_Store`, `Thumbs.db`).
- IDE and editor configurations (`.vscode/`, `.idea/`, `*.swp`).
- Language runtime caches and bytecode (`__pycache__/`, `*.class`, `*.o`, `*.obj`).
- Package manager dependencies (`node_modules/`, `venv/`, `.venv/`, `vendor/`).
- Build output directories (`dist/`, `build/`, `out/`, `target/`, `bin/`).
- Environment variables and secrets (`.env`, `.env.local`, `*.pem`, `*.key`).

### 2. Untracking Previously Committed Files
Provide the exact commands to stop tracking files already in git history without deleting local copies:
```bash
git rm -r --cached <directory-or-file>
git commit -m "chore(git): untrack files now covered by .gitignore"
```

## Output Quality Rules

- Group entries with clean category headers for maintainability.
- Never add overly broad rules (like `*.json`) that accidentally ignore valid configuration files.
