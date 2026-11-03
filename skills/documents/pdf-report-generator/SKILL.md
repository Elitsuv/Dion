---
name: pdf-report-generator
description: Structures clean, publication-ready markdown and styling specifications optimized for PDF conversion (Pandoc, Typst, Weasyprint). Use when preparing professional PDF documents.
---

# PDF Report Generator

Structure clean, beautifully styled markdown and configuration blocks designed for seamless PDF export.

## Trigger Conditions

Activate this skill when:
- A user wants to generate an academic report, capstone proposal, or technical memo for PDF compilation.
- A student asks: 'Create a clean PDF report template', 'Generate markdown for Pandoc PDF conversion', or 'Format this document for printing/exporting to PDF'.

## Execution Protocol

Follow this publication-ready document layout:

### 1. Frontmatter & Document Metadata
- Include clean YAML frontmatter configured for document engines (Pandoc/LaTeX/Typst):
  ```yaml
  title: "Engineering Technical Report"
  subtitle: "Performance Analysis of Distributed Key-Value Stores"
  author: "Author Name"
  date: "\\today"
  geometry: "margin=1in"
  header-includes:
    - \\usepackage{booktabs}
    - \\usepackage{microtype}
  ```

### 2. Typographic & Visual Hierarchy
- Use disciplined sectioning (`#`, `##`, `###`) ensuring logical page-break balance.
- Format tables using clean Markdown pipes with explicit column alignment.
- Format code listings with explicit language tags for syntax highlighting.

### 3. Callout Boxes & Technical Notes
- Format visual alert blocks for key definitions, warnings, and formulas.

### 4. PDF Compilation Command
- Provide the exact terminal command to compile the document into a high-quality PDF:
  ```bash
  pandoc report.md -o report.pdf --pdf-engine=xelatex -V geometry:margin=1in
  ```

## Output Quality Rules

- Ensure all tables, figures, and code blocks fit within standard 8.5x11 printable page widths.
- Never use broken or unclosed formatting tags that break PDF compilation.
