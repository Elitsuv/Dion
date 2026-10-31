---
name: systematic-debugger
description: Diagnoses runtime crashes, stack traces, logic failures, and test regressions using a hypothesis-driven debugging workflow. Use when code fails with an error, exception, segmentation fault, or incorrect output.
---

# Systematic Debugger

Isolate and resolve software faults using disciplined, hypothesis-driven debugging.

## Trigger Conditions

Activate this skill when:
- A user provides an error message, stack trace, crash log, or failing test output.
- A user reports that code crashes, hangs, produces wrong answers, or leaks memory.
- A user asks: "Why is this failing?", "Where is the bug?", or "How do I fix this segmentation fault / exception?".

---

## Execution Protocol

Execute the following 6-step diagnostic workflow:

### 1. Failure Classification & Fault Localization
- Classify the failure:
  - **Compilation / Type Error**: Unresolved symbol, type mismatch, missing header.
  - **Runtime Crash**: Null pointer dereference, segmentation fault, index out of bounds, stack overflow.
  - **Logic Regression**: Divergent computation, stale cache, incorrect loop termination.
  - **Resource Exhaustion**: Memory limit exceeded, file descriptor leak, timeout/deadlock.
- Pinpoint the terminal frame: file, function name, and exact line of execution failure.

### 2. State Discrepancy Analysis
- Contrast expected state with runtime state:
  - **Expected Behavior**: What the function contract promised.
  - **Actual Behavior**: What the processor or interpreter executed.
  - **Divergence Point**: The exact variable, pointer, or register that held an invalid value.

### 3. Falsifiable Hypothesis Tree
- Construct 2–3 specific hypotheses explaining the failure mechanism:
  - *Hypothesis 1*: Off-by-one boundary condition in loop indexing.
  - *Hypothesis 2*: Shared reference mutation or uninitialized memory read.
  - *Hypothesis 3*: Unhandled type truncation or sign-extension error.
- Identify the explicit code evidence that validates or invalidates each hypothesis.

### 4. Minimal Reproducing Example (MRE)
- Provide the smallest deterministic input or snippet that reliably triggers the failure.
- Document the exact command or call to reproduce the issue.

### 5. Surgical Patch
- Provide the corrected code as a clear before/after comparison or diff:
  ```text
  # Defective
  ...
  # Corrected
  ...
  ```
- Explain why this fix resolves the underlying root cause without altering valid interfaces or introducing regressions.

### 6. Regression Defense
- Supply a targeted unit test or assertion to ensure this fault cannot recur.
- Suggest appropriate diagnostic tools where relevant (e.g., `gdb`, `valgrind`, AddressSanitizer, `pdb`).

---

## Output Quality Rules

- Never apply blind try-catch blocks or defensive null checks that mask deeper lifecycle bugs.
- Always explain the underlying mechanism that caused the machine or interpreter to fail.
