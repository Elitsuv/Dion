<div align="center">
  <img src="assets/dion.png" alt="Dion Logo" width="110" />
  <h1>Dion</h1>
  <p><strong>Modular Agent Skills for Engineering Students & Researchers</strong></p>
  <p>
    <a href="#skills">Skills</a> &bull;
    <a href="#how-it-works">How It Works</a> &bull;
    <a href="#usage">Usage</a> &bull;
    <a href="#structure">Structure</a> &bull;
    <a href="CONTRIBUTING.md">Contributing</a> &bull;
    <a href="LICENSE">License</a>
  </p>
</div>

---

Most agent prompts return shallow code snippets, gloss over difficult mathematical steps, and ignore boundary conditions.

**Dion** is a curated library of modular Agent Skills designed for computer science students, engineering graduates, and technical researchers. Each skill provides an AI agent with a deterministic, step-by-step protocol: tracing execution state without hand-waving, diagnosing runtime faults through hypothesis trees, planning modular system architectures, and dissecting academic research with empirical rigor.

No wrappers. No runtime dependencies. Just high-density markdown protocols compatible with any agent environment.

---

## Skills

| Skill | Category | Description |
| :--- | :--- | :--- |
| [`concept-clarifier`](skills/concept-clarifier/SKILL.md) | Theory & Foundations | Explains complex algorithms and systems via physical intuition, formal invariants, minimal traces, and complexity bounds. |
| [`code-explainer`](skills/code-explainer/SKILL.md) | Code Understanding | Deconstructs unfamiliar codebases line by line, mapping variable mutations, memory allocation models, and Big-O trade-offs. |
| [`systematic-debugger`](skills/systematic-debugger/SKILL.md) | Debugging & Triage | Diagnoses runtime faults using scientific debugging: failure classification, hypothesis trees, MREs, and surgical patches. |
| [`project-scaffolder`](skills/project-scaffolder/SKILL.md) | System Design | Scaffolds capstone and semester projects into modular monoliths, data contracts, and phased milestone roadmaps. |
| [`research-synthesizer`](skills/research-synthesizer/SKILL.md) | Academic Research | Dissects research papers and lab reports, analyzing novelty claims, baseline validity, and practical reproducibility gaps. |
| [`git-commit-architect`](skills/git-commit-architect/SKILL.md) | Version Control | Structures atomic commits, enforces conventional syntax, writes contextual commit bodies, and formats review-ready PRs. |

---

## How It Works

Each skill in Dion is self-contained in a dedicated directory under `skills/` containing a `SKILL.md` file. 

Every skill file begins with strict YAML frontmatter:

```yaml
---
name: skill-name-in-kebab-case
description: Clear, specific summary of the skill's purpose and precise trigger conditions.
---
```

When an agent processes a task, it scans the YAML descriptions to select the relevant skill. The agent then follows the structured execution protocol defined in the markdown body, ensuring rigorous, predictable output.

---

## Usage

### 1. In Agent-Assisted Workspaces
Place the `skills/` folder in your workspace or agent knowledge directory. The agent will index the frontmatter and activate skills contextually based on user requests.

### 2. Manual Instruction Injection
Copy the contents of any `SKILL.md` directly into your agent's system prompt or project instructions file when focusing on a specific task (such as debugging an assignment or structuring a capstone).

### 3. Prompting Example

```text
"I am debugging a C program that crashes with a segmentation fault when freeing a binary tree node.
Here is the code and the valgrind trace. Apply the systematic-debugger skill to isolate the root cause."
```

---

## Structure

```text
.
├── assets/
│   └── dion.png
├── skills/
│   ├── concept-clarifier/
│   │   └── SKILL.md
│   ├── code-explainer/
│   │   └── SKILL.md
│   ├── systematic-debugger/
│   │   └── SKILL.md
│   ├── project-scaffolder/
│   │   └── SKILL.md
│   ├── research-synthesizer/
│   │   └── SKILL.md
│   └── git-commit-architect/
│       └── SKILL.md
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── skill_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── labels.yml
│   └── sync-labels.sh
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```

---

## License

This project is licensed under the [Apache-2.0 License](LICENSE).
