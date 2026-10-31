---
name: research-synthesizer
description: Analyzes academic papers, preprints, and technical surveys by assessing novelty claims, benchmark rigor, and reproducibility hurdles. Use when a user reviews research papers or prepares technical literature surveys.
---

# Research Synthesizer

Evaluate academic papers and technical research with empirical rigor.

## Trigger Conditions

Activate this skill when:
- A user provides a research paper title, abstract, arXiv link, or manuscript excerpt and requests an analysis or summary.
- A user is conducting a literature review, preparing for an academic reading group, or assessing whether a published paper can be implemented in production.

---

## Execution Protocol

Execute the analysis across the following 6 sections:

### 1. Research Problem & Core Thesis
- **One-Sentence Thesis**: State the primary technical claim made by the authors.
- **Problem & Gap**: State the specific failure mode or bottleneck in prior art that this paper addresses.
- **Problem Formulation**: Formalize inputs, objective functions, and operational constraints.

### 2. Novelty & Contribution Matrix
- Separate conceptual breakthroughs from incremental engineering adjustments:
  | Claimed Contribution | Type (Theoretical / Algorithmic / Empirical) | Prior Art Baseline | Novelty Assessment |
  | :--- | :--- | :--- | :--- |
  | ... | ... | ... | High / Moderate / Incremental |

### 3. Methodology & System Pipeline
- Deconstruct the technical mechanism:
  - Theoretical assumptions, axioms, and mathematical derivations.
  - Architecture pipeline: Input representations, internal transformation layers, and output heads.
  - Loss functions, optimization routines, heuristics, or scheduling invariants.

### 4. Empirical Evaluation & Benchmark Analysis
- Scrutinize experimental claims:
  - **Datasets & Workloads**: Standard benchmark datasets vs custom or synthetic corpora.
  - **Baseline Competitiveness**: Were proposed methods compared against contemporary state-of-the-art baselines or weakened predecessors?
  - **Evaluation Metrics**: Precision, recall, latency, throughput, parameter efficiency, or memory footprint.
  - **Statistical Validity**: Did the authors report error bars, confidence intervals, and multiple random seeds, or only cherry-picked runs?

### 5. Reproducibility & Practical Gaps
- Identify undisclosed engineering hurdles:
  - Omitted hyperparameters, warmup schedules, or initialization heuristics.
  - Computational requirements: GPU-hours, cluster requirements, or VRAM constraints.
  - Dataset preprocessing steps or undocumented data cleaning filters.
  - Open-source artifact availability and license terms.

### 6. Reading Group Discussion Questions
- Provide 2–3 probing questions evaluating unstated assumptions, threat model limitations, or failure modes under real-world conditions.

---

## Output Quality Rules

- Reject marketing terms ("revolutionary", "unmatched") in favor of measurable empirical deltas.
- Highlight any benchmark conditions where the proposed technique performed worse than existing baselines.
