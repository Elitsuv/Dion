---
name: markdown-table-formatter
description: Constructs clean, column-aligned Markdown comparison tables, feature matrices, and technical schemas without formatting inconsistencies. Use when structuring tabular documentation.
---

# Markdown Table Formatter

## Protocol
1. Schema -> Define columns, datatypes, and alignments.
2. Normalize -> Format casing, empty values (N/A), backticks.
3. Align -> Balance pipes and column padding across rows.

## Guardrails
- Never output conversational filler or sign-offs.
- Never output misaligned pipes or unbalanced columns.
- Never put unescaped pipes inside table cells.

## Output Schema
| Column 1 | Column 2 | Column 3 |
| :--- | :---: | ---: |
| `[Data]` | [Val] | [Metric] |
