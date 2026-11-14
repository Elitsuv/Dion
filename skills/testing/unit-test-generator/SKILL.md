---
name: unit-test-generator
description: Generates comprehensive unit test suites with boundary assertions, fixtures, and parameterized test cases. Use when writing automated code tests.
---

# Unit Test Generator

## Protocol
1. Inspect -> Parse function signature, contracts, return invariants.
2. Partition -> Split domain into valid equivalence classes.
3. Implement -> Write parameterized tests with native runners.

## Guardrails
- Never output filler or pleasantries.
- Never write tests without explicit assertions.
- Never test multiple distinct behaviors in one test.

## Output Schema
### Unit Test Suite
[Parameterized test code covering normal and boundary cases]
- Coverage: [Happy path | Boundaries | Exceptions]
