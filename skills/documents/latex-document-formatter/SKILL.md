---
name: latex-document-formatter
description: Generates clean, compilable LaTeX code with formal IEEE and ACM formatting, math environments, and tables. Use when formatting academic papers.
---

# LaTeX Document Formatter

## Protocol
1. Preamble -> Configure documentclass, packages, and styling.
2. Math -> Typeset equations with AMS align environments.
3. Elements -> Build booktabs tables and labeled figure anchors.

## Guardrails
- Never output conversational filler or sign-offs.
- Never use deprecated syntax like $$ or \rm.
- Never leave unescaped LaTeX special characters.

## Output Schema
### Preamble
[Compilable packages and styling]
### Document Body
[LaTeX body with aligned equations]
