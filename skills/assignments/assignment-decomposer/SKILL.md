---
name: assignment-decomposer
description: Breaks down complex engineering assignments, lab specs, and project rubrics into granular subtasks, test cases, and dependency graphs. Use when a student receives an assignment specification and needs a systematic execution plan.
---

# Assignment Decomposer

Transform dense engineering assignment briefs and lab rubrics into verified, actionable execution plans.

## Trigger Conditions

Activate this skill when:
- A user pastes a course assignment description, lab handout, or project rubric.
- A student asks: "How do I start this assignment?", "Break down this project specification", or "What order should I build these assignment requirements in?".

## Execution Protocol

Follow this structured 5-phase breakdown:

### 1. Requirements & Constraint Extraction
- Parse the handout into explicit constraints:
  - **Permitted Languages & Libraries**: Disallowed third-party packages, required compiler flags (e.g., `-Wall -Wextra -Werror`).
  - **Submission Deliverables**: Exact filenames, archive structures (e.g., `tar.gz`, `zip`), and build automation files (`Makefile`, `CMakeLists.txt`).
  - **Grading Weights**: Allocation across public tests, hidden test suites, memory leak checks (e.g., Valgrind), and documentation.

### 2. Functional Specification Breakdown
- Decompose the overall problem into discrete, testable units:
  - Input parsing and sanitization.
  - Core data structure initialization and memory layout.
  - Algorithm / processing pipeline.
  - Output formatting and error status code handling.

### 3. Dependency Graph & Implementation Order
- Order the subtasks by prerequisite dependencies (bottom-up execution):
  - *Phase 1*: Data structures and memory allocation helpers.
  - *Phase 2*: Core state transition logic on simple, single-threaded inputs.
  - *Phase 3*: Edge case handling (e.g., empty streams, max-sized payloads, invalid tokens).
  - *Phase 4*: End-to-end integration with the required CLI/API interface.

### 4. Verification & Synthetic Test Plan
- For each subtask, specify concrete inputs and expected outputs before writing code:
  | Subtask | Verification Strategy | Input Case | Expected Output / State |
  | :--- | :--- | :--- | :--- |
  | Parser | Unit test | Malformed header line | Return error code `ERR_INVALID_HEADER` |
  | Memory cleanup | Valgrind check | Allocation under failure | 0 bytes leaked in 0 blocks |

### 5. Final Submission Sanity Check
- Provide a pre-submission checklist:
  - Clean compilation with strict flags enabled.
  - No memory leaks or dangling pointers.
  - Output matches exact character-level requirements (trailing newlines, capitalization).

## Output Quality Rules

- Never write the complete assignment solution for the student; provide structural scaffolds, interface contracts, and test plans.
- Always identify subtle rubric traps (e.g., performance penalties for `O(N^2)` search, memory leak zero-tolerance rules).
- Keep task definitions atomic and measurable.

