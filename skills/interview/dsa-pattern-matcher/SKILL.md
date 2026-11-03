---
name: dsa-pattern-matcher
description: Maps coding interview problem statements to core Data Structures and Algorithms patterns (Two Pointers, Sliding Window, Monotonic Stack, Union-Find). Use when approaching LeetCode-style technical interview questions.
---

# DSA Pattern Matcher

Classify algorithmic interview problems into canonical Data Structures and Algorithms patterns.

## Trigger Conditions

Activate this skill when:
- A user provides a coding interview question, LeetCode problem, or algorithmic challenge.
- A student asks: 'What algorithm pattern applies here?', 'Is this two pointers or dynamic programming?', or 'How should I approach this technical interview problem?'.

## Execution Protocol

Follow this algorithmic pattern classification sequence:

### 1. Problem Signal & Constraint Analysis
- Identify key signals in the problem statement:
  - Input size $N$ and expected complexity (e.g., $N \le 10^5 \implies O(N \log N)$ or $O(N)$).
  - Data attributes: Contiguous subarray, sorted order, pairwise comparisons, tree/graph structure.
  - Objective: Optimization (minimum/maximum), subset enumeration, existence check, or shortest path.

### 2. Primary & Secondary Pattern Matching
- Match against canonical algorithmic patterns:
  - **Two Pointers**: Sorted arrays, pair sums, palindrome verification.
  - **Sliding Window**: Contiguous subarrays with size or sum constraints.
  - **Monotonic Stack**: Next greater/smaller element, histogram area.
  - **Binary Search on Solution Space**: Monotonic search spaces ('find minimum max value').
  - **Union-Find / Disjoint Set**: Dynamic connectivity, cycle detection in undirected graphs.
  - **Topological Sort / Kahn\'s Algorithm**: Dependency graphs, prerequisite ordering.
  - **Dynamic Programming (Memoization / Tabulation)**: Overlapping subproblems, optimal substructure.

### 3. Step-by-Step Algorithmic Strategy
- Explain *why* the identified pattern fits the constraints.
- Provide high-level pseudocode outlining the algorithm invariant.

### 4. Complexity & Common Trap
- State expected Time and Space complexity.
- Warn against common pitfalls (e.g., duplicate element handling, index out of bounds on empty window).

## Output Quality Rules

- Focus on teaching the underlying pattern recognition, not just giving a solution.
- State time and space bounds before writing code.
