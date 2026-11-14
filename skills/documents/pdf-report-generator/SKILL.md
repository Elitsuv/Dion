---
name: pdf-report-generator
description: Structures clean, publication-ready markdown and CSS specifications optimized for headless PDF rendering engines. Use when generating exportable technical documents.
---

# PDF Report Generator

## Protocol
1. Page Setup -> Set @page geometry, margins, running headers.
2. Structure -> Organize content into sections and callouts.
3. Print Rules -> Add page-break rules preventing table splits.

## Guardrails
- Never output filler or pleasantries.
- Never allow page breaks to split tables or code.
- Never use screen pixel units for print margins.

## Output Schema
### Print CSS
<style>@page { size: A4; margin: 20mm; } .no-split { break-inside: avoid; }</style>
### Content
[Structured markdown document]
