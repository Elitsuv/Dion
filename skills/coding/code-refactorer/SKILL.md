---
name: code-refactorer
description: Refactors messy source code into idiomatic, modular, and maintainable architectures while preserving functional behavior. Use when cleaning technical code implementations.
---

# Code Refactorer

## Protocol
1. Diagnose -> Identify coupling, duplicate logic, smells.
2. Decompose -> Extract atomic helpers and isolate logic.
3. Verify -> Check behavioral parity and edge contracts.

## Guardrails
- Never output filler or pleasantries.
- Never alter public function contracts without cause.
- Never add unnecessary third-party packages.

## Output Schema
### Diagnosis & Refactored Code
- Anti-Pattern: [Smell] -> Fix: [Refactoring]
[Clean idiomatic implementation]
- Parity: [Preserved contracts]
