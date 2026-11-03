---
name: cheat-sheet-designer
description: Designs ultra-dense, multi-column quick-reference cheat sheets for programming languages, CLI commands, and technical tools. Use when creating fast reference guides.
---

# Cheat Sheet Designer

Design dense, high-yield, multi-column technical cheat sheets and syntax quick-references.

## Trigger Conditions

Activate this skill when:
- A user asks for a quick-reference guide or cheat sheet for a programming language, framework, or CLI tool.
- A student asks: 'Make a Git cheat sheet', 'Give me a Linux command reference', or 'Create a quick-reference for Vim / Bash / Docker'.

## Execution Protocol

Structure cheat sheets into dense, scannable blocks:

### 1. Functional Categorization
- Group commands or syntax into discrete operational categories (e.g., for Git: Setup, Inspecting State, Staging & Committing, Branching, Undoing Changes).

### 2. Command-Description-Example Triad
- Format each entry with:
  - **Syntax / Command**: Exact CLI command or code construct in monospace.
  - **Operational Purpose**: 1-line explanation of what it does.
  - **Practical Example**: Realistic arguments or flags.

### 3. High-Frequency Flags & Parameters
- Document the most essential flags with concise explanations (e.g., `tar -xzvf: [x]tract, g[z]ip, [v]erbose, [f]ile`).

### 4. Common Error Recovery Shortcut
- Include a 'Quick Fixes / Emergency' section for undoing common mistakes (e.g., undoing last commit, killing hung port process).

## Output Quality Rules

- Maximize information density; eliminate filler paragraphs.
- Keep commands directly copy-pasteable.
