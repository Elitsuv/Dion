---
name: arxiv-digest-builder
description: Summarizes recent arXiv preprints into actionable technical digests with core contributions and benchmark results. Use when tracking research literature.
---

# arXiv Digest Builder

## Protocol
1. Extract -> Isolate paper title, problem, and novelty.
2. Mechanics -> Detail algorithmic design and formulation.
3. Benchmarks -> Record quantitative deltas against baselines.

## Guardrails
- Never output filler or pleasantries.
- Never accept claims without citing specific datasets.
- Never omit hardware and compute constraints.

## Output Schema
### Paper Digest: [Title]
- Core Claim: [Novelty] -> Method: [Architecture]
| Dataset | Baseline | Proposed | Delta |
- Constraints: [Compute / Data limit]
