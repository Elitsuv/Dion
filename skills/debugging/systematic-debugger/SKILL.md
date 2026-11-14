---
name: systematic-debugger
description: Diagnoses runtime crashes, regressions, and logic bugs using scientific falsification trees and minimal reproduction cases. Use when debugging failing code systems.
---

# Systematic Debugger

## Protocol
1. Reproduce -> Isolate minimal failing input.
2. Hypothesize -> State 2 falsifiable hypotheses.
3. Test -> Run probes to falsify or confirm.
4. Patch -> Fix root cause and add test.

## Guardrails
- Never output filler or pleasantries.
- Never edit code without prior test proof.
- Never close bugs without regression tests.

## Output Schema
### Falsification Matrix
- H1: [Hypothesis] -> [Falsified | Confirmed]
### Patch & Test
- Fix: [Code patch] -> Test: [Assert pass]
