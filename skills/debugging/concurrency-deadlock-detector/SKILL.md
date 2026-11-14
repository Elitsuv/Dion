---
name: concurrency-deadlock-detector
description: Identifies race conditions, deadlocks, and synchronization bugs in multithreaded and asynchronous software. Use when concurrent code hangs or behaves nondeterministically.
---

# Concurrency Deadlock Detector

## Protocol
1. Map -> Trace thread lifecycles and locks.
2. Verify -> Check Coffman conditions for circular wait.
3. Remediate -> Enforce strict lock ordering or atomics.

## Guardrails
- Never output filler or pleasantries.
- Never dismiss race conditions as timing quirks.
- Never use sleep calls to fix synchronization.

## Output Schema
### Concurrency Hazard
- Hazard: [Deadlock | Race] -> Cycle: [A(L1->L2) vs B(L2->L1)]
### Patch
[Remediated lock order or atomic code]
