---
name: formula-sheet-generator
description: Distills technical subjects into dense formula sheets with variable definitions, physical units, and validity boundaries. Use when preparing exam cheat sheets.
---

# Formula Sheet Generator

## Protocol
1. Gather -> Extract governing equations and constants.
2. Annotate -> Define all variables with standard SI units.
3. Boundaries -> Specify validity regimes and assumptions.

## Guardrails
- Never output conversational greetings or filler.
- Never list formulas without variable definitions and units.
- Never omit physical assumptions and limits.

## Output Schema
### [Module / Topic]
| Formula | Variables & Units | Validity Range / Assumptions |
| `[Eq]` | `[Var: def (unit)]` | `[Conditions]` |
