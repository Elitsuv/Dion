---
name: lab-report-writer
description: Formats engineering and science lab reports with standard academic sections, error propagation calculations, and observation tables. Use when a student needs to write or structure an engineering lab report.
---

# Lab Report Writer

Format rigorous, publication-grade laboratory reports for engineering and scientific coursework.

## Trigger Conditions

Activate this skill when:
- A user asks to write, format, or structure an engineering laboratory experiment report.
- A user provides raw lab notes, equipment lists, and measurements and asks for a formal write-up.

## Execution Protocol

Follow this standard IEEE/academic lab report sequence:

### 1. Title, Objective & Theoretical Background
- Formulate a precise technical title (e.g., 'Transient Response Analysis of Second-Order RLC Circuits').
- State the concise experimental objective in 1–2 sentences.
- Outline the underlying theoretical equations, governing laws, and predicted values.

### 2. Apparatus, Circuit/System Schematics & Components
- List all apparatus with model numbers, tolerances, and operational ranges.
- Describe circuit topology, mechanical setup, or software testbed configuration.

### 3. Step-by-Step Experimental Procedure
- Detail chronological steps in passive, objective past tense.
- Document safety precautions, calibration steps, and zero-error corrections.

### 4. Raw Data, Observations & Error Analysis
- Tabulate raw measurements vs theoretical expectations.
- Perform formal error analysis:
  - Percentage Error = `(|Experimental - Theoretical| / Theoretical) * 100%`.
  - Propagate measurement uncertainties through calculations.

### 5. Discussion & Root Cause of Discrepancies
- Discuss non-ideal component behavior (e.g., internal resistance, thermal noise, friction).
- Differentiate between systematic errors, random errors, and environmental drift.

### 6. Conclusion & Verification
- Summarize whether the empirical findings validated the theoretical model within tolerance.

## Output Quality Rules

- Maintain an objective, dispassionate academic tone throughout.
- Ensure all physical quantities have explicit SI units.
- Never invent fabricated data points; highlight missing parameters clearly.
