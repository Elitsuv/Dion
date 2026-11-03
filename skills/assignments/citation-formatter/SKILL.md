---
name: citation-formatter
description: Formats and validates academic citations across IEEE, ACM, APA, and BibTeX formats for engineering papers and lab reports. Use when compiling bibliographies, references, or citations.
---

# Citation Formatter

Format, normalize, and validate academic references and bibliographies in IEEE, ACM, APA, and BibTeX styles.

## Trigger Conditions

Activate this skill when:
- A user provides unstructured links, titles, DOIs, or raw reference data and requests formatted citations.
- A student asks: 'Format this in IEEE style', 'Generate a BibTeX entry for this paper', or 'Fix my references section'.

## Execution Protocol

Follow this citation standardization process:

### 1. Metadata Verification
- Identify and verify core bibliographic components:
  - Author(s) (Primary last name and initials).
  - Title of article, book chapter, or paper.
  - Venue (Journal, Conference Proceedings, Book, Technical Report).
  - Volume, Issue, Page numbers.
  - Publication year and month.
  - Digital Object Identifier (DOI) or canonical persistent URL.

### 2. Style-Specific Formatting
- Generate exact citation text matching the requested style:
  - **IEEE Style**: Numbered bracketed citations (`[1] J. K. Author, "Title of paper," ...`).
  - **ACM Style**: Author-year or numeric style conforming to standard ACM proceedings.
  - **BibTeX**: Clean `@article` or `@inproceedings` blocks with standard field names and valid citation keys.

### 3. In-Text Citation Alignment
- Provide the corresponding in-text citation marker (e.g., `[1]`, `(Author et al., 2024)`).
- Ensure author ordering preserves original publication order.

## Output Quality Rules

- Use standard publication abbreviations for IEEE transactions and conferences.
- Ensure BibTeX citation keys are descriptive and kebab/snake-case (e.g., `author2024title`).
- Never fabricate publication dates, DOIs, or page numbers.
