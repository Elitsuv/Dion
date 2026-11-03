---
name: unit-test-generator
description: Generates comprehensive unit test suites with boundary assertions, fixtures, and parameterized tests. Use when writing automated tests for functions and classes.
---

# Unit Test Generator

Generate exhaustive, structured unit test suites adhering to standard framework conventions.

## Trigger Conditions

Activate this skill when:
- A user provides a function, class, or module and requests unit tests.
- A student asks: 'Write unit tests for this in pytest/JUnit/GoogleTest', 'Generate test cases for my function', or 'How do I test this class?'.

## Execution Protocol

Follow this test suite engineering protocol:

### 1. Function Contract & Boundary Mapping
- Analyze target signatures: input parameters, return values, and explicit exceptions.
- Partition input space into equivalence classes:
  - Standard nominal inputs (happy path).
  - Minimum and maximum boundary values.
  - Zero, null, empty collections, and extreme limits.
  - Invalid types or inputs that must trigger exceptions.

### 2. Test Suite Structure & Framework Idioms
- Structure tests using the standard framework (e.g., `pytest`, `JUnit 5`, `GoogleTest`, `Catch2`).
- Follow the Arrange-Act-Assert (AAA) pattern for each test case:
  - **Arrange**: Set up inputs, mocks, and test state.
  - **Act**: Invoke target function once.
  - **Assert**: Verify return value, state change, or raised exception.

### 3. Parameterized Test Generation
- Use parameterized decorators (e.g., `@pytest.mark.parametrize`, `@ParameterizedTest`) to test multiple input/output tuples without duplicate test code.

### 4. Mocking & Isolation
- Isolate external dependencies (network, disk, databases) using test mocks or dependency injection.

## Output Quality Rules

- Give every test function a descriptive name indicating scenario and expectation (e.g., `test_withdraw_insufficient_funds_raises_error`).
- Ensure test cases are independent and have zero cross-test side effects.
