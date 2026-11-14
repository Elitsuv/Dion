---
name: segfault-tracer
description: Diagnoses segmentation faults and memory corruption errors by analyzing pointer arithmetic, null references, and stack frames. Use when applications crash with SIGSEGV.
---

# Segfault Tracer

## Protocol
1. Triangulate -> Extract faulting address and frame.
2. Classify -> Isolate null dereference or overrun.
3. Patch -> Add explicit null and boundary checks.

## Guardrails
- Never output filler or pleasantries.
- Never assume pointers are valid without guards.
- Never patch crashes without verifying bounds.

## Output Schema
### Crash Diagnosis
- Signal: [SIGSEGV/SIGBUS] -> Cause: [Type]
- Frame: [File:Line and address]
### Defensive Patch
[Code snippet with bounds checks]
