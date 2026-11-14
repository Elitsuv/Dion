# Contributing to Dion

Thank you for contributing to Dion. We build practical, disciplined, token-optimized agent skills for students, learners, and technical researchers following the `agentskills.io` open standard.

---

## 3-Stage LLM Token Optimization Standard

Every skill submitted to Dion MUST adhere to our strict 3-Stage LLM Token Optimization architecture. In agent environments, all skill names and descriptions are loaded into the system prompt on every turn, and context injection costs accumulate rapidly. Output tokens are 3x–5x more expensive than input tokens.

```text
┌─────────────────────────────────────────────────────────────┐
│ STAGE 1: Cold-Start Router Diet (YAML Frontmatter)          │
│ • Name + Description only (no extra keys)                   │
│ • Description: strictly 15–24 words (~20–26 tokens)         │
│ • Formula: [Action Verb] + [Deliverable] + ". Use when " +  │
│            [Exact Trigger].                                 │
├─────────────────────────────────────────────────────────────┤
│ STAGE 2: Context Injection Diet (Markdown Body)             │
│ • Body strictly under 120 tokens (~30 lines max)            │
│ • Zero persona fluff ("You are a tutor...", "Please...")    │
│ • Telegraphic arrows (->) for deterministic step transitions│
│ • Exactly 3 sections: ## Protocol, ## Guardrails,           │
│   ## Output Schema                                          │
├─────────────────────────────────────────────────────────────┤
│ STAGE 3: Output Token Clamp                                 │
│ • Guardrails forbid greetings, pleasantries, & preambles    │
│ • Output Schema provides compact structural skeletons       │
│ • Maximum informational density per token generated         │
└─────────────────────────────────────────────────────────────┘
```

---

## Repository Hierarchy

Skills are organized into domain categories under `skills/`:

```text
skills/
├── assignments/      # Coursework decomposition, rubrics, lab reports
├── coding/           # Syntax explanation, refactoring, complexity
├── debugging/        # Concurrency, leaks, segfaults, stack traces
├── documents/        # LaTeX, markdown tables, PDF specs, cheat sheets
├── exam-prep/        # Question banks, autopsy, PYQ decoding, speed solve
├── git/              # Atomic commits, branch workflows, conflict resolution
├── interview/        # STAR framing, DSA patterns, mock interviews
├── learning/         # Synthesis, Feynman intuition, derivations, Socratic
├── productivity/     # Backlog recovery, active recall, sprint pacing
├── project/          # Scaffolding, architecture, schemas, API contracts
├── research/         # arXiv digests, literature review matrices
├── revision/         # Ultra-dense 1-page trigger sheets
└── testing/          # Edge cases, mocks, unit and integration suites
```

### Folder Rules

- `skills/` contains only domain category folders using `kebab-case`.
- Category folders contain only skill folders using `kebab-case`.
- Each skill folder contains exactly one `SKILL.md`.
- No loose files or extraneous assets inside skill folders.
- The YAML frontmatter `name` must exactly match the skill's folder name.

---

## `SKILL.md` Specification

Every `SKILL.md` must strictly follow this exact template:

```markdown
---
name: your-skill-name
description: [Action Verb] + [Student Deliverable/Workflow] + ". Use when " + [Exact Trigger].
---

# Skill Title

## Protocol
1. Step 1 -> Telegraphic deterministic action.
2. Step 2 -> Explicit state transformation.
3. Step 3 -> Verification and artifact production.

## Guardrails
- Never output filler or pleasantries.
- Never [domain negative constraint].
- Never [scope boundary or unverified claim].

## Output Schema
### [Section 1]
- Item: [Compact key-value or formula]
### [Section 2]
[Dense structural skeleton without conversational narrative]
```

### Constraints Checklist

1. **YAML Description**:
   - Word count: strictly between **15 and 24 words** (`15 <= count <= 24`).
   - Formula: Starts with a capitalized 3rd-person singular action verb (e.g., `Condenses`, `Formats`, `Generates`, `Synthesizes`, `Extracts`, `Diagnoses`, `Analyzes`, `Structures`, `Deconstructs`, `Refactors`, `Derives`, `Identifies`, `Optimizes`), states the deliverable, includes the literal anchor `". Use when "`, and ends with a period.
   - Keys: Exactly `name:` and `description:`. Never add extra keys.
2. **Markdown Body**:
   - Token budget: strictly **< 120 tokens** (measured via `scripts/audit_tokens.py`).
   - Line limit: **<= 30 lines**.
   - Exactly 3 sections: `## Protocol`, `## Guardrails`, `## Output Schema`.
   - Protocol: 3 to 5 numbered steps using telegraphic arrows (`->`).
   - Guardrails: 3 negative constraints starting with `Never ...`.
   - Output token clamp: Guardrails must explicitly forbid conversational intros, pleasantries, preambles, and verbose explanations.

---

## Local Token Audit

Before opening a Pull Request, run the zero-dependency token auditor from repository root:

```bash
python scripts/audit_tokens.py
```

All 59+ skills must report `PASS` with zero failures.

---

## Contribution Workflow

1. **Check Existing Work**: Browse open Issues or PRs to avoid duplicate skills.
2. **Open a Skill Proposal**: Open an issue tagged `Di: Skill` to agree on domain, naming, and triggers.
3. **Branch**:
   ```bash
   git checkout -b skill/<category>/<skill-name>
   ```
4. **Author the Skill**:
   - Create `skills/<category>/<skill-name>/SKILL.md`.
   - Run `python scripts/audit_tokens.py` to confirm < 120 token body and 15–24 word frontmatter.
5. **Update Repository Index**:
   - Update `README.md` category tables and total count badge.
6. **Submit PR**: Complete all items in the Pull Request template.
