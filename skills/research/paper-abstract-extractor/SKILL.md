---
name: paper-abstract-extractor
description: Extracts core problem statements, methods, and quantitative findings from academic papers into concise executive briefings. Use when quickly scanning paper suitability.
---

# Paper Abstract Extractor

Deconstruct dense academic research abstracts and introductory sections into actionable, high-density briefings.

## Trigger Conditions

Activate this skill when:
- A user provides a research paper abstract or introduction and requests a structured breakdown.
- A student asks: 'Summarize this paper in 3 bullet points', 'What is the main finding of this study?', or 'Is this paper relevant to my thesis?'.

## Execution Protocol

Extract the 4 core pillars of the paper:

### 1. The Core Problem
- What exact real-world or theoretical bottleneck is the paper solving? (1 direct sentence).

### 2. The Proposed Solution / Innovation
- What is the specific algorithmic, mathematical, or architectural mechanism introduced?

### 3. Quantitative Empirical Proof
- What were the measured benchmark results?
  - Baseline score vs proposed score (e.g., `84.2% accuracy vs 79.1% prior state-of-the-art`).
  - Speedup, parameter reduction, or latency gains.

### 4. Verdict on Practical Applicability
- Can this be implemented on commodity hardware by an engineering student, or does it require proprietary enterprise clusters?

## Output Quality Rules

- Strip away academic filler phrases ('In this work we investigate...').
- Always extract exact numerical figures where reported.
