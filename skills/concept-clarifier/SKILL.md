---
name: concept-clarifier
description: Explains core computer science and engineering concepts through physical intuition, formal invariants, minimal traces, and complexity bounds. Use when a user asks to learn, clarify, or prepare for exams on an algorithm, system architecture, or theoretical model.
---

# Concept Clarifier

Deconstruct technical concepts into rigorous, intuitive mental models.

## Trigger Conditions

Activate this skill when:
- A user asks to understand, learn, or clarify an algorithm, protocol, data structure, or theoretical CS model.
- A user asks: "How does X work?", "Explain Paxos/Raft simply", "Intuition behind dynamic programming", or prepares for technical exams and interviews.

---

## Execution Protocol

Follow this structured sequence:

### 1. Core Problem & Physical Analogy
- State the baseline problem: *What was inefficient, impossible, or fragile before this concept existed?*
- Provide a grounded physical analogy that reflects the exact mechanics without misleading oversimplification.

### 2. Formal Invariants & Mechanics
- State the formal definition.
- Detail the operational mechanics:
  - State transitions or pipeline phases.
  - Invariants (conditions that remain true across all operations).
  - Preconditions and assumptions.

### 3. Minimal Concrete Implementation or Numerical Trace
- Provide a clean, minimal reference implementation or step-by-step numerical trace.
- Keep variables descriptive; annotate critical lines where invariants are updated.
- No third-party dependencies or framework boilerplate.

### 4. Complexity & Trade-Off Matrix
- State asymptotic bounds:
  - Best, Average, and Worst-case Time Complexity.
  - Auxiliary Space Complexity (separate input memory from working memory).
- Compare against 1–2 common alternatives:
  | Approach | Time | Space | Primary Trade-Off | When to Select |
  | :--- | :--- | :--- | :--- | :--- |
  | Target Concept | ... | ... | ... | ... |
  | Alternative | ... | ... | ... | ... |

### 5. Boundary Conditions & Exam Traps
- Detail common edge cases, subtle failure modes, and exam pitfalls:
  - Boundary conditions (empty sets, off-by-one indices, zero values).
  - Implicit resource costs (cache locality, recursion stack limits).
- Provide one diagnostic self-check question that tests invariant understanding.

---

## Output Quality Rules

- Never skip mathematical steps or dismiss transitions with "it is obvious that".
- Distinguish between amortized time, worst-case time, and average-case time.
- Keep code examples focused strictly on the algorithmic core.
