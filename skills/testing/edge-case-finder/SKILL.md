---
name: edge-case-finder
description: Identifies subtle boundary conditions, numeric overflows, and degenerate inputs that break code. Use when testing algorithm robustness or debugging failures.
---

# Edge Case Finder

## Protocol
1. Audit -> Identify types, ranges, collections.
2. Degenerate -> Generate zeros, empties, limits.
3. Stress -> Test off-by-one indices and ordering.

## Guardrails
- Never output filler or pleasantries.
- Never propose happy-path inputs.
- Never omit overflow and precision boundaries.

## Output Schema
### Boundary Matrix
| Category | Input | Failure Mode |
| Empty | `[]` / `None` | Null dereference |
| Extreme | `MAX` / `MIN` | Overflow wrap |
