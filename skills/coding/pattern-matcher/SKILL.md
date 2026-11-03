---
name: pattern-matcher
description: Identifies appropriate software design patterns (Gang of Four, architectural patterns) to solve software design problems cleanly. Use when architecting object-oriented systems.
---

# Pattern Matcher

Identify, compare, and implement the optimal software design patterns for object-oriented and systems engineering problems.

## Trigger Conditions

Activate this skill when:
- A user describes an architectural design bottleneck or class design challenge.
- A student asks: 'What design pattern should I use here?', 'Show me how to apply the Strategy pattern in C++', or 'Compare Factory vs Builder for this problem'.

## Execution Protocol

Follow this design pattern evaluation framework:

### 1. Problem Classification
- Categorize the architectural requirement:
  - **Creational**: Object instantiation complexity, subclass decoupling (Factory, Builder, Singleton).
  - **Structural**: Composition, interface adaptation, decorator wrapping (Adapter, Composite, Facade).
  - **Behavioral**: Algorithm substitution, event notification, state transitions (Strategy, Observer, State).

### 2. Pattern Candidate Comparison
- Compare 2 candidate patterns against the problem constraints:
  | Pattern | Core Advantage | Overhead / Boilerplate | Best Fit Scenario |
  | :--- | :--- | :--- | :--- |
  | Pattern A | ... | ... | ... |
  | Pattern B | ... | ... | ... |

### 3. Idiomatic Implementation
- Provide a clean, minimal code demonstration implementing the chosen pattern without extraneous framework baggage.

### 4. Anti-Pattern Warning
- Detail how this pattern is commonly abused or over-engineered (e.g., premature Singleton, over-abstraction with unnecessary interfaces).

## Output Quality Rules

- Keep implementations compact and focused on the interaction between participants.
- Warn against over-engineering when a simple function closure suffices.
