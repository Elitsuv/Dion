---
name: markdown-table-formatter
description: Creates clean, aligned, and readable Markdown comparison tables, feature matrices, and data schemas. Use when formatting tabular technical information.
---

# Markdown Table Formatter

Format clean, visually aligned, and high-density Markdown tables for technical documentation and reports.

## Trigger Conditions

Activate this skill when:
- A user provides messy or unaligned tabular data and requests a clean comparison table.
- A student asks: 'Format this data as a markdown table', 'Make a comparison matrix for these frameworks', or 'Align this table cleanly'.

## Execution Protocol

Follow these table formatting standards:

### 1. Header & Column Alignment
- Establish clear, concise column headers.
- Specify column alignment explicitly in the separator row:
  - Left-align for text and labels: `:---`
  - Center-align for status badges, booleans, and dates: `:---:`
  - Right-align for numbers, metrics, and memory sizes: `---:`

### 2. Visual Character-Level Alignment
- Pad columns with spaces so the raw markdown source is readable even without a rendered preview:
  ```markdown
  | Component    | Protocol | Latency (ms) | Fault Tolerance |
  | :----------- | :------: | -----------: | :-------------- |
  | Ingestion    | gRPC     |         1.24 | Automatic retry |
  | Cache Layer  | Redis    |         0.45 | Master-Replica  |
  ```

### 3. Compact Information Density
- Use concise status indicators (`Yes` / `No`, `Supported` / `Unsupported`, or Unicode markers `✓` / `✗`) instead of long sentences.

## Output Quality Rules

- Never generate unaligned tables with ragged pipe boundaries in source.
- Ensure all rows have the exact same number of columns as the header.
