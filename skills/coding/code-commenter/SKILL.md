---
name: code-commenter
description: Generates concise docstrings, function contracts, and invariant comments explaining logic rationale rather than syntax. Use when documenting technical source code.
---

# Code Commenter

## Protocol
1. Contracts -> Map preconditions and types.
2. Docstring -> Generate typed interface documentation.
3. Invariants -> Annotate non-obvious branches with `->`.

## Guardrails
- Never output conversational filler or sign-offs.
- Never narrate syntax; document rationale only.
- Never leave complex branches unannotated.

## Output Schema
### Contract
[Typed docstring]
### Implementation
[Annotated code block]
