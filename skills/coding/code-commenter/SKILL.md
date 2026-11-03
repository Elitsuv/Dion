---
name: code-commenter
description: Writes concise, professional docstrings, function contracts, and inline comments that explain the 'why' rather than narrating syntax. Use when documenting code.
---

# Code Commenter

Add high-density, professional documentation, type specifications, and architectural comments to codebases.

## Trigger Conditions

Activate this skill when:
- A user provides undocumented code and asks for comments, docstrings, or function documentation.
- A student asks: 'Add comments to this assignment code', 'Document this class in Google/Sphinx/Javadoc style', or 'Explain this code with comments'.

## Execution Protocol

Follow these standard documentation protocols:

### 1. Function & Method Docstrings
Format docstrings to the target language convention (e.g., Google Style for Python, Javadoc for Java, JSDoc for JavaScript, Doxygen for C/C++):
- **Summary**: Concise one-line imperative description.
- **Args / Parameters**: Name, type, constraints, and operational purpose.
- **Returns**: Exact type and contract guarantees.
- **Raises / Exceptions**: Explicit conditions that trigger errors.

### 2. Invariant & Non-Obvious Inline Comments
- Add inline comments only where the code logic is subtle:
  - Bitwise operations or algorithmic tricks.
  - Workarounds for language quirks or race conditions.
  - Explanations of *why* an approach was chosen over the obvious alternative.

### 3. Avoid Syntax Narration
- Explicitly delete redundant comments that narrate plain code (e.g., `// increment i by 1`).

## Output Quality Rules

- Never clutter self-explanatory code with obvious comments.
- Ensure all parameter names in docstrings match function signatures exactly.
