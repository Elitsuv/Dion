---
name: readme-architect
description: Crafts professional GitHub README files with architectural diagrams, quickstart setup guides, and feature tables. Use when documenting technical repositories.
---

# README Architect

## Protocol
1. Header -> State headline, value proposition, architecture.
2. Quickstart -> Provide copy-paste setup commands and prereqs.
3. Operations -> Document configuration, testing, licenses.

## Guardrails
- Never output filler or pleasantries.
- Never write instructions requiring undocumented steps.
- Never omit test suite execution commands.

## Output Schema
### README Blueprint
- Title & Badges: `# Project`
- Architecture: [Mermaid diagram]
- Setup: [Shell commands] -> Tests: `make test`
