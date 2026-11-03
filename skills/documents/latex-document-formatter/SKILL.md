---
name: latex-document-formatter
description: Generates clean, compilable LaTeX documents with IEEE/ACM templates, math equations, tables, and TikZ diagrams. Use when writing technical papers and lab reports in LaTeX.
---

# LaTeX Document Formatter

Author clean, compilable, and error-free LaTeX source documents for academic papers and mathematical reports.

## Trigger Conditions

Activate this skill when:
- A user asks to format a report, article, or assignment in LaTeX.
- A student asks: 'Convert this report to LaTeX', 'Format these equations in LaTeX', or 'Fix this LaTeX compilation error'.

## Execution Protocol

Follow standard LaTeX engineering practices:

### 1. Document Class & Package Selection
- Set appropriate document class (`article`, `report`, `IEEEtran`, `acmart`).
- Import essential packages:
  - Mathematics: `amsmath`, `amssymb`, `amsfonts`.
  - Figures & Tables: `graphicx`, `booktabs`, `multirow`, `caption`.
  - Code & Algorithms: `listings`, `minted`, `algorithm2e`.
  - Hyperlinks & Cross-references: `hyperref`, `cleveref`.

### 2. Mathematical Equations & Environments
- Typeset equations cleanly using `equation`, `align`, or `bmatrix` environments.
- Ensure all symbols are properly escaped and indexed.

### 3. Tabular & Figure Environments
- Use `booktabs` for clean, professional tables without vertical rules (`\\toprule`, `\\midrule`, `\\bottomrule`).
- Include proper captions and labels (`\\label{tab:...}`, `\\label{fig:...}`).

### 4. Compilable Full-Document Verification
- Provide a complete, standalone, compilable `.tex` file with `\\begin{document}` and `\\end{document}`.

## Output Quality Rules

- Ensure all braces, dollar signs, and environments are properly closed.
- Avoid obsolete packages (e.g., use `booktabs` instead of raw `tabular` with repeated `\\hline`).
