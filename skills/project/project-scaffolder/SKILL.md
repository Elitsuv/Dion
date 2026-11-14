---
name: project-scaffolder
description: Plans software directory structures, modular architectures, data contracts, and milestone roadmaps. Use when bootstrapping new technical engineering projects.
---

# Project Scaffolder

## Protocol
1. Architecture -> Select pattern (Layered, Clean, Hexagonal).
2. Tree -> Generate layout isolating domain logic, I/O, tests.
3. Bootstrap -> Specify config files, dependencies, commands.

## Guardrails
- Never output filler or pleasantries.
- Never place domain logic inside transport layers.
- Never generate empty directory trees without duties.

## Output Schema
### Layout & Quickstart
root/ -> src/ (domain, api) -> tests/ -> config/
- Responsibilities: [Module breakdown]
`setup && build && test`
