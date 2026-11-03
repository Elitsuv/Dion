---
name: flashcard-builder
description: Generates high-retention spaced repetition flashcards in Anki-compatible format for engineering terminology, algorithms, and architectures. Use when creating study decks.
---

# Flashcard Builder

Create high-retention, atomic flashcard decks formatted for Anki and active recall study sessions.

## Trigger Conditions

Activate this skill when:
- A user provides lecture slides, book chapters, or notes and requests flashcards.
- A student asks: 'Create an Anki deck for Computer Networks', 'Make flashcards from these notes', or 'Give me active recall questions for my finals'.

## Execution Protocol

Follow the cognitive science rules of effective spaced repetition:

### 1. Enforce the Minimum Information Principle
- Ensure every flashcard tests exactly one atomic concept, invariant, or definition.
- Reject bloated cards containing long paragraphs or multiple bullet points.

### 2. Card Type Formats
Generate cards across two standard categories:
- **Direct Recall (Q&A)**:
  - *Front*: Precise question testing a mechanism or definition.
  - *Back*: Concise, factual answer (maximum 1–2 sentences).
- **Cloze Deletion (Fill-in-the-blank)**:
  - Sentence where the critical technical term is bracketed (e.g., `In TCP, {{c1::SYN-ACK}} is sent by the server during handshake`).

### 3. Tab-Separated Anki Export Block
- Provide a clean, copy-pasteable TSV block ready for direct import into Anki:
  ```text
  Front<TAB>Back
  What is the time complexity of building a heap from an array of N items?<TAB>O(N) amortized
  ```

## Output Quality Rules

- Cards must be concise, unambiguous, and focused on high-yield exam material.
- Never make cards where the front reveals the answer or contains ambiguous clues.
