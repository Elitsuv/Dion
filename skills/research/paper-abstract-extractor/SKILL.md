---
name: paper-abstract-extractor
description: Extracts problem statements, proposed methodologies, and quantitative results from academic papers into structured briefings. Use when screening academic literature.
---

# Paper Abstract Extractor

## Protocol
1. Bottleneck -> Identify core problem or limitation.
2. Technique -> State proposed algorithmic or empirical method.
3. Metrics -> Capture performance deltas over baselines.

## Guardrails
- Never output filler or pleasantries.
- Never copy long prose; synthesize into bullets.
- Never omit the baseline model used for comparison.

## Output Schema
### Research Brief
- Problem: [Bottleneck] -> Method: [Technical solution]
- Delta: [Metric: Proposed vs Baseline (+%)]
- Verdict: [Relevance to study]
