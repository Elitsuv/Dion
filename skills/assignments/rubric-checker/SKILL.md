---
name: rubric-checker
description: Evaluates coursework drafts against official grading rubrics to diagnose missing criteria and scoring vulnerabilities. Use when auditing drafts prior to submission.
---

# Rubric Checker

## Protocol
1. Ingest -> Extract criteria, weights, and rules.
2. Cross-Check -> Audit draft text against rubric rows.
3. Remediate -> Pinpoint scoring gaps with text fixes.

## Guardrails
- Never output filler or pleasantries.
- Never score without citing draft evidence.
- Never give vague praise; cite deficiencies.

## Output Schema
### Rubric Audit
| Criteria | Pts | Evidence | Gap |
### Fixes
- Fix [N]: [Gap] -> Action: [Rewrite]
