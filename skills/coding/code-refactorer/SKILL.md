---
name: code-refactorer
description: Refactors messy student code into clean, modular, and idiomatic production-quality implementations while preserving existing behavior. Use when cleaning up working but unreadable code.
---

# Code Refactorer

Restructure working but unmaintainable student code into clean, idiomatic, and maintainable software.

## Trigger Conditions

Activate this skill when:
- A user provides working code that suffers from code smells, deep nesting, duplicate logic, or poor naming.
- A student asks: 'Clean up this code', 'Make this function more readable', or 'Refactor this script into idiomatic Python/C++/Java'.

## Execution Protocol

Execute a structured refactoring sequence:

### 1. Code Smell Diagnosis
- Identify concrete code smells in the provided snippet:
  - God functions (excessive lines of code, multiple responsibilities).
  - Deep conditional/loop nesting (cyclomatic complexity > 4).
  - Magic numbers and hardcoded string literals.
  - Code duplication (DRY violations).
  - Unclear or misleading variable names.

### 2. Behavioral Invariant Verification
- Confirm input/output contracts and edge-case guarantees to ensure refactoring introduces zero regressions.

### 3. Step-by-Step Refactored Implementation
- Present the refactored code clearly.
- Extract helper functions for discrete subtasks.
- Replace magic values with typed constants or enums.
- Use guard clauses (early returns) to flatten nesting.

### 4. Diff & Trade-Off Summary
- Highlight the exact before/after metrics:
  - Cyclomatic complexity reduction.
  - Line count and readability improvements.
  - Potential performance implications.

## Output Quality Rules

- Never alter the public interface or function signature without explicit user agreement.
- Do not introduce heavy third-party dependencies during refactoring.
