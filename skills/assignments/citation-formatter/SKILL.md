---
name: citation-formatter
description: Formats and validates academic bibliographies across IEEE, ACM, APA, and BibTeX standards without syntax errors. Use when compiling research paper references.
---

# Citation Formatter

## Protocol
1. Extract -> Parse authors, title, venue, DOI.
2. Standardize -> Map fields to target citation style.
3. Validate -> Check punctuation, sorting, and syntax.

## Guardrails
- Never output filler or pleasantries.
- Never fabricate missing fields; use markers.
- Never mix citation standards in output.

## Output Schema
### Citation
[Formatted reference string]
### BibTeX
[Valid BibTeX entry]
