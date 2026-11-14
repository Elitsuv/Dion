---
name: flashcard-builder
description: Generates high-retention spaced repetition flashcards in Anki-compatible format for technical terms and formulas. Use when preparing long-term study decks.
---

# Flashcard Builder

## Protocol
1. Decompose -> Extract atomic facts, formulas, and invariants.
2. Format -> Create Front/Back prompts or cloze deletion cards.
3. Export -> Output tab-delimited Anki-ready TSV rows.

## Guardrails
- Never output conversational greetings or filler.
- Never place multiple concepts on a single flashcard.
- Never create cards prompting paragraph answers.

## Output Schema
### Anki TSV Deck
```text
Front<TAB>Back
Cloze {{c1::fact}}<TAB>Context
```
### Summary
- Cards: [N] -> Topic: [Domain]
