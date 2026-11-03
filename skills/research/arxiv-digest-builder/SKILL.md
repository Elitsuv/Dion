---
name: arxiv-digest-builder
description: Summarizes and categorizes recent arXiv preprints in computer science and engineering into actionable technical digests. Use when keeping up with research trends.
---

# arXiv Digest Builder

Compile and distill recent arXiv preprints into structured, actionable engineering research digests.

## Trigger Conditions

Activate this skill when:
- A user provides a list of arXiv links, preprint titles, or abstracts and requests a categorized summary.
- A student asks: 'Summarize today\'s arXiv papers in computer vision', 'Digest these preprints for our lab meeting', or 'What are the top takeaways from these papers?'.

## Execution Protocol

Structure the preprint digest into categorized sections:

### 1. Categorized Topic Clustering
- Group preprints into distinct sub-fields (e.g., Transformer Efficiency, Reinforcement Learning, Graph Neural Networks, Hardware Acceleration).

### 2. Micro-Briefings per Preprint
For each paper, provide:
- **Paper Title & arXiv Identifier**: With direct link formatting.
- **Core Innovation**: 1 clear sentence explaining what makes the paper distinct.
- **Key Quantitative Claim**: Specific benchmark improvement or efficiency metric.
- **Open-Source Code Link**: Note if code/checkpoints are publicly released.

### 3. Emerging Trends & Paradigm Shifts
- Highlight overarching methodology shifts observed across the digested batch.

## Output Quality Rules

- Focus on actionable engineering takeaways rather than theoretical jargon.
- Highlight whether code and weights are reproducible.
