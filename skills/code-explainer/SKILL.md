---
name: code-explainer
description: Deconstructs unfamiliar code snippets and algorithms by tracing execution flow, state mutations, memory layout, and asymptotic complexity. Use when a user asks to understand, review, or walk through existing code line by line.
---

# Code Explainer

Analyze unfamiliar, legacy, or complex source code into concrete state transitions and memory profiles.

## Trigger Conditions

Activate this skill when:
- A user provides a function, class, script, or algorithm and asks: "What does this code do?", "How does this work?", or "Walk me through this line by line".
- A user needs to understand data flow, variable state changes, or architectural decisions in unfamiliar code.

---

## Execution Protocol

Structure output using the following sequence:

### 1. Operational Summary
- State the objective in 1–2 direct sentences: *Input -> Transformation -> Output*.
- Name the core pattern, paradigm, or algorithmic category (e.g., Sliding Window, Monotonic Stack, RAII, Visitor Pattern).

### 2. Interface Contract
- Break down the interface:
  - Input parameters: Data types, expected ranges, preconditions, and defaults.
  - Return value: Type, contract guarantees, and nullability.
  - Side effects: In-place mutations, disk/network I/O, memory allocations, or global state shifts.

### 3. Step-by-Step Execution Trace
- Trace execution using a concrete, minimal input.
- Present a chronological state table:
  | Step | Line(s) | Variable State | Condition / Action Evaluated |
  | :--- | :--- | :--- | :--- |
  | 1 | `L4-L6` | `i=0, curr='a'` | Condition `curr in seen` evaluates to False |
  | 2 | `L7` | `seen={'a'}` | Inserted into hash set |

### 4. Memory & Resource Model
- Detail allocation patterns:
  - Stack frame lifecycle vs heap allocations.
  - Reference aliasing or sharing risks.
  - Buffer growth, reallocation overhead, or potential resource leaks.

### 5. Algorithmic Bounds
- **Time Complexity**: Derive Big-O mathematically across nested loops and recursive calls.
- **Space Complexity**: Separate auxiliary memory from input memory. Include recursion call stack depth.

### 6. Edge Cases & Failure Modes
- List specific scenarios where the code fails or degrades:
  - Null, empty, or single-element inputs.
  - Numeric overflow or precision loss.
  - Degenerate inputs (e.g., unbalanced trees, reverse-sorted partitions).

---

## Output Quality Rules

- Anchor explanations to specific line numbers or token references.
- Explain *why* an invariant is maintained rather than reciting syntax mechanically.
- Focus depth on non-trivial operations: bitwise manipulations, pointer updates, and recursive base cases.
