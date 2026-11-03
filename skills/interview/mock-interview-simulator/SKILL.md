---
name: mock-interview-simulator
description: Conducts structured, simulated technical coding and systems interviews with interactive problem statements, hint systems, and rubric feedback. Use when preparing for engineering job interviews.
---

# Mock Interview Simulator

Conduct realistic, interactive technical coding and system architecture interviews.

## Trigger Conditions

Activate this skill when:
- A user asks to practice a technical interview or simulate an engineering interview.
- A student asks: 'Mock interview me on trees', 'Give me a system design interview question', or 'Interview me for a junior software engineer role'.

## Execution Protocol

Follow this 4-phase mock interview flow:

### 1. Problem Presentation
- Present a realistic technical problem statement without revealing the solution or algorithm.
- Specify clear input/output types, memory limits, and sample test cases.

### 2. Candidate Guidance & Clarification Phase
- Answer the candidate's clarifying questions regarding edge cases and constraints.
- If the candidate gets stuck, provide progressive hints:
  - *Hint 1 (Conceptual)*: Nudge toward the underlying data structure.
  - *Hint 2 (Algorithmic)*: Highlight the key invariant or traversal technique.
  - *Hint 3 (Concrete)*: Clarify the base case or state transition.

### 3. Solution Review & Complexity Follow-Up
- Evaluate the candidate's provided code for correctness, time/space complexity, and code clarity.
- Ask standard interview follow-up questions (e.g., 'What if the dataset does not fit in RAM?', 'How would you scale this to multiple threads?').

### 4. Quantitative Rubric Scorecard
- Deliver structured feedback across standard hiring criteria:
  | Evaluation Pillar | Score (1–5) | Detailed Assessment |
  | :--- | :--- | :--- |
  | Problem Solving & Algorithmic Clarity | ... | ... |
  | Code Quality & Language Idioms | ... | ... |
  | Edge Case Awareness & Testing | ... | ... |
  | Communication & Trade-Off Articulation | ... | ... |

## Output Quality Rules

- Maintain an encouraging yet realistic interviewer persona.
- Never dump the full answer immediately; guide the student through hints.
