# Contributing to Dion

Thank you for contributing to Dion. We build practical, disciplined agent skills for computer science students, engineering graduates, and technical researchers.

---

## Design Principles

Every skill in Dion serves as an executable instruction protocol for an AI agent. We maintain high standards for all submissions:

1. **Practical Utility**: Focus on real engineering workflows: analyzing algorithms, isolating runtime faults, planning systems architecture, reviewing academic papers, and maintaining git hygiene. Avoid generic, conversational prompts.
2. **Platform & Vendor Neutral**: Never mention any proprietary company, product, or vendor names. Skills must remain universally applicable across any agent runtime or environment.
3. **No Unnecessary Scaffolding**: Keep skills clean. A single, well-crafted `SKILL.md` is preferred over unnecessary scripts or multi-file boilerplate.
4. **Pedagogical Rigor**: Skills should teach principles, trace states, and build mental models, not just generate blind copy-paste snippets.

---

## Skill Structure Standard

Every skill resides in its own folder under `skills/` using `kebab-case` naming:

```text
skills/
└── your-skill-name/
    └── SKILL.md
```

### SKILL.md Specification

Every `SKILL.md` must begin with YAML frontmatter containing `name` and `description`:

```markdown
---
name: your-skill-name
description: A concise 1-2 sentence description explaining what the skill accomplishes and the exact trigger conditions for when an agent should invoke it.
---

# Your Skill Name

Brief overview of the skill's purpose.

## Trigger Conditions
Specific user queries or operational scenarios that activate this skill.

## Step-by-Step Instructions
The explicit, numbered protocol the agent must follow.

## Quality Standards & Output Format
Constraints and structured response template for the agent.
```

---

## Dion Labels

Dion organizes issues and Pull Requests using branded `Di: ...` labels:

| Label | Description |
| :--- | :--- |
| `Di: Skill` | New agent skill proposal or addition |
| `Di: Update` | Enhancement or update to an existing skill |
| `Di: Fix` | Bug fix or correction in a skill's instructions |
| `Di: Chore` | Repository maintenance, templates, or workflows |
| `Di: Docs` | Improvements to README, CONTRIBUTING, or guides |
| `Di: Pedagogy` | Curriculum alignment or conceptual clarity for students |
| `Di: Good First Issue` | Friendly task for students and first-time contributors |
| `Di: Help Wanted` | Extra domain expertise or student feedback requested |

### Label Setup & Sync

Maintainers can synchronize these labels and purge default GitHub repository labels using the included script:

```bash
bash .github/sync-labels.sh
```

---

## Contribution Workflow

1. **Check Existing Work**: Browse open [Issues](https://github.com/Elitsuv/Dion/issues) or [Pull Requests](https://github.com/Elitsuv/Dion/pulls) to avoid duplicate efforts.
2. **Open an Issue**: For new skill ideas, open a `Skill Request` issue first (`Di: Skill`) to discuss scope and structure.
3. **Create a Branch**:
   ```bash
   git checkout -b skill/your-skill-name
   ```
4. **Author the Skill**:
   - Create `skills/<your-skill-name>/SKILL.md`.
   - Ensure the YAML frontmatter is valid.
   - Verify instructions against the quality checklist.
5. **Update the Index**: Add your new skill and a crisp one-line description to the table in `README.md`.
6. **Submit a Pull Request**: Use the PR template and complete all checklist items.

---

## Submission Checklist

- [ ] Folder name is in `kebab-case`.
- [ ] `SKILL.md` contains valid YAML frontmatter (`name` and `description`).
- [ ] No company or product names are mentioned anywhere.
- [ ] No Python packages, web frameworks, or third-party wrappers are introduced.
- [ ] Description clearly guides agents on when to activate the skill.
- [ ] Instructions are concrete, structured, and free of generic conversational filler.
