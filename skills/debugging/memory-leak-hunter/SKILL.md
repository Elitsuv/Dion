---
name: memory-leak-hunter
description: Analyzes Valgrind logs, AddressSanitizer dumps, and heap profiles to pinpoint unreleased allocations and pointer leaks. Use when debugging memory management.
---

# Memory Leak Hunter

## Protocol
1. Ingest -> Parse allocation stacks, types, lost bytes.
2. Trace -> Map allocation site to missing free branch.
3. Fix -> Apply RAII ownership or smart pointers.

## Guardrails
- Never output filler or pleasantries.
- Never suppress sanitizer logs without fixing leaks.
- Never leave early return branches uncleaned.

## Output Schema
### Leak Profile & Path
- Lost: [Bytes] -> Alloc: [File:Line]
- Path: [Allocation] -> [Missing free branch]
### RAII Patch
[Corrected resource cleanup code]
