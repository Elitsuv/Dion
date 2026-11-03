---
name: complexity-analyzer
description: Derives formal asymptotic Big-O time and space complexity with recurrence relations, loop summations, and call stack depth. Use when analyzing algorithm efficiency.
---

# Complexity Analyzer

Derive rigorous Big-O time and space complexity bounds for algorithms and code implementations.

## Trigger Conditions

Activate this skill when:
- A user provides an algorithm or code snippet and requests its time or space complexity.
- A student asks: 'What is the Big-O of this function?', 'Derive the recurrence relation for this recursive algorithm', or 'Is this O(N log N) or O(N^2)?'.

## Execution Protocol

Follow this mathematical derivation sequence:

### 1. Loop and Operation Counting (Iterative Code)
- Write out the explicit summation for nested loops:
  $$\\sum_{i=0}^{N-1} \\sum_{j=i}^{N-1} 1 = \\frac{N(N+1)}{2} = O(N^2)$$
- Analyze amortized operations (e.g., dynamic array resizing, hash table rehashing).

### 2. Recurrence Relations (Recursive Code)
- Formulate the recurrence relation $T(N) = aT(N/b) + f(N)$.
- Apply the Master Theorem where applicable, identifying the exact case:
  - State values for $a$, $b$, and $f(N)$.
  - Compare $f(N)$ against $N^{\\log_b a}$.
- If Master Theorem does not apply, draw out the recursion tree depth and level costs.

### 3. Space Complexity Breakdown
- Separate input storage from auxiliary space:
  - Heap-allocated buffers and collections.
  - Maximum recursive call stack depth ($O(H)$ for tree traversal).

### 4. Best, Average, and Worst-Case Bounds
- Detail specific input structures that trigger each bound (e.g., sorted array in QuickSort).

## Output Quality Rules

- Always provide the step-by-step mathematical derivation, not just the final $O(\\dots)$ claim.
- Explicitly differentiate between auxiliary space and total space.
