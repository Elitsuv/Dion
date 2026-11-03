---
name: formula-sheet-generator
description: Distills complex engineering subjects into dense, high-yield formula sheets with variable definitions, units, and boundary constraints. Use when preparing review sheets for exams.
---

# Formula Sheet Generator

Generate dense, accurate reference sheets of equations, physical laws, and unit conversions for engineering examinations.

## Trigger Conditions

Activate this skill when:
- A user asks to create an equation cheat sheet or formula review for a specific technical course.
- A student asks: 'Summarize all equations for Electromagnetics', 'Make a formula sheet for Thermodynamics', or 'What equations do I need for my exam?'.

## Execution Protocol

Structure the reference sheet into logical topic blocks:

### 1. Topic Taxonomy & Core Equations
- Group formulas by physical subsystem or theorem (e.g., 'Maxwell\'s Equations', 'Conservation of Momentum', 'Laplace Transforms').
- State each governing equation in canonical mathematical notation.

### 2. Variable Definitions & Fundamental Units
- Explicitly define every variable, constant, and subscript:
  | Symbol | Quantity | Standard SI Unit | Typical Dimension |
  | :--- | :--- | :--- | :--- |
  | $\\rho$ | Volume charge density | $C/m^3$ | $[I \\cdot T \\cdot L^{-3}]$ |
  | $\\epsilon_0$ | Permittivity of free space | $F/m$ | $[M^{-1} \\cdot L^{-3} \\cdot T^4 \\cdot I^2]$ |

### 3. Validity Assumptions & Boundary Conditions
- State critical preconditions required for each formula to hold true (e.g., laminar flow only, ideal gas assumption, linear time-invariant system).

### 4. Common Transformation & Substitution Rules
- Provide standard algebraic conversions, identities, and differential relationships used in exam problems.

## Output Quality Rules

- Ensure mathematical notation renders cleanly in LaTeX markdown.
- Never omit validity constraints (e.g., non-zero denominator, temperature in Kelvin).
