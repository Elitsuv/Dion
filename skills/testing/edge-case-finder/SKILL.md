---
name: edge-case-finder
description: Identifies subtle boundary conditions, numeric overflows, and degenerate inputs that break code. Use when testing algorithm robustness or debugging hidden judge failures.
---

# Edge Case Finder

Isolate subtle boundary conditions, numeric traps, and degenerate inputs that break software implementations.

## Trigger Conditions

Activate this skill when:
- A user's code passes basic tests but fails hidden test suites or online judge test cases.
- A student asks: 'What edge cases am I missing?', 'Why does my code fail on hidden tests?', or 'Find inputs that break this algorithm'.

## Execution Protocol

Systematically probe the code against these 5 edge-case vectors:

### 1. Numeric & Boundary Traps
- Zero values (`0`, `-0`, division by zero).
- Extreme limits (Integer `INT_MIN`, `INT_MAX`, 64-bit overflow).
- Floating-point precision issues (`0.1 + 0.2 != 0.3`, `NaN`, positive/negative infinity).
- Negative inputs where only positive was assumed.

### 2. Collection & Structural Degeneracy
- Empty collections (`[]`, `""`, `NULL`).
- Single-element collections.
- Duplicate elements in sorted/unique assumptions.
- Maximum allowable size (stress/timeout triggers).

### 3. Structural & Graph Edge Cases
- Disconnected graphs or single-node graphs.
- Cycles in graphs assumed to be DAGs or trees.
- Highly unbalanced binary trees (degenerating to linked lists).
- Self-loops and multi-edges.

### 4. String & Text Encodings
- Strings with spaces, punctuation, or non-ASCII Unicode characters.
- String palindromes or strings with all identical characters.

### 5. Explicit Test Case Table
- Output a clear table of failing inputs with the reason and expected behavior:
  | Test Case Input | Category | Potential Vulnerability | Expected Behavior |
  | :--- | :--- | :--- | :--- |
  | `arr = []` | Empty Collection | IndexOutOfBoundsException | Return 0 or None safely |
  | `x = 2147483647` | Integer Overflow | Silent wrap to negative | Handle via 64-bit integer |

## Output Quality Rules

- Provide concrete input values, not abstract descriptions.
- Focus specifically on boundary conditions that cause crashes or wrong answers.
