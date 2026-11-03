<div align="center">
  <img src="assets/dion.png" alt="Dion Logo" width="110" style="border-radius: 20%;" />
  <h1>Dion</h1>
  <p><strong>Systematic, opinionated AI agent skills for computer science and engineering workflows.</strong></p>
  <p>
    <a href="https://github.com/Elitsuv/Dion"><img src="https://img.shields.io/badge/skills-48-blue?style=flat-square" alt="Skills Count" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-green?style=flat-square" alt="License" /></a>
    <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/contributions-welcome-orange?style=flat-square" alt="Contributions Welcome" /></a>
  </p>
  <p>
    <a href="#skills-by-category">Skills</a> &bull;
    <a href="#what-dion-is">What Dion Is</a> &bull;
    <a href="#how-to-use">How to Use</a> &bull;
    <a href="#repository-structure">Structure</a> &bull;
    <a href="CONTRIBUTING.md">Contributing</a> &bull;
    <a href="LICENSE">License</a>
  </p>
</div>

---

## What Dion Is

Most AI agent prompts produce shallow snippets, gloss over algorithmic invariants, and fail to isolate boundary conditions.

**Dion** is a curated library of 48 modular, domain-categorized Agent Skills engineered specifically for computer science students, engineering graduates, and technical researchers. Each skill equips an AI agent with a deterministic, step-by-step execution protocol: decomposing complex assignment rubrics, formatting laboratory reports, designing normalized database schemas, hunting memory leaks in C/C++, tracing execution state across memory spaces, isolating runtime crashes via falsifiable hypothesis trees, and reviewing literature with empirical rigor.

No wrappers. No runtime dependencies. Just clean, platform-agnostic markdown protocols compatible with any agent runtime.

---

## Skills by Category

Total active skills: **48** across **11** engineering domains.

### `assignments/`

| Skill | Description |
| :--- | :--- |
| [`assignment-decomposer`](skills/assignments/assignment-decomposer/SKILL.md) | Breaks down complex engineering assignments, lab specs, and project rubrics into granular subtasks, test cases, and dependency graphs. Use when a student receives an assignment specification and needs a systematic execution plan. |
| [`citation-formatter`](skills/assignments/citation-formatter/SKILL.md) | Formats and validates academic citations across IEEE, ACM, APA, and BibTeX formats for engineering papers and lab reports. Use when compiling bibliographies, references, or citations. |
| [`lab-report-writer`](skills/assignments/lab-report-writer/SKILL.md) | Formats engineering and science lab reports with standard academic sections, error propagation calculations, and observation tables. Use when a student needs to write or structure an engineering lab report. |
| [`presentation-slide-planner`](skills/assignments/presentation-slide-planner/SKILL.md) | Structures technical presentation slide decks for engineering capstones, term projects, and defense talks. Use when planning visual slides, speaker notes, and time allocations. |
| [`rubric-checker`](skills/assignments/rubric-checker/SKILL.md) | Evaluates assignment drafts against official grading rubrics and assignment criteria to identify missing requirements. Use before submitting an assignment to maximize grade accuracy. |

### `coding/`

| Skill | Description |
| :--- | :--- |
| [`code-commenter`](skills/coding/code-commenter/SKILL.md) | Writes concise, professional docstrings, function contracts, and inline comments that explain the 'why' rather than narrating syntax. Use when documenting code. |
| [`code-explainer`](skills/coding/code-explainer/SKILL.md) | Deconstructs unfamiliar code snippets and algorithms by tracing execution flow, state mutations, memory layout, and asymptotic complexity. Use when a user asks to understand, review, or walk through existing code line by line. |
| [`code-refactorer`](skills/coding/code-refactorer/SKILL.md) | Refactors messy student code into clean, modular, and idiomatic production-quality implementations while preserving existing behavior. Use when cleaning up working but unreadable code. |
| [`complexity-analyzer`](skills/coding/complexity-analyzer/SKILL.md) | Derives formal asymptotic Big-O time and space complexity with recurrence relations, loop summations, and call stack depth. Use when analyzing algorithm efficiency. |
| [`pattern-matcher`](skills/coding/pattern-matcher/SKILL.md) | Identifies appropriate software design patterns (Gang of Four, architectural patterns) to solve software design problems cleanly. Use when architecting object-oriented systems. |

### `debugging/`

| Skill | Description |
| :--- | :--- |
| [`concurrency-deadlock-detector`](skills/debugging/concurrency-deadlock-detector/SKILL.md) | Identifies race conditions, deadlocks, and synchronization pitfalls across threads, mutexes, and async routines. Use when multi-threaded code hangs or yields nondeterministic results. |
| [`memory-leak-hunter`](skills/debugging/memory-leak-hunter/SKILL.md) | Analyzes Valgrind logs, AddressSanitizer output, and memory profiling reports to trace unreleased allocations and pointer leaks. Use when debugging C/C++ memory management. |
| [`segfault-tracer`](skills/debugging/segfault-tracer/SKILL.md) | Diagnoses segmentation faults and bus errors in C/C++ by analyzing pointer arithmetic, null references, and buffer overflows. Use when a binary terminates with SIGSEGV. |
| [`stack-trace-analyzer`](skills/debugging/stack-trace-analyzer/SKILL.md) | Parses complex, multi-threaded, or nested stack traces and compiler error dumps to pinpoint the exact root-cause frame. Use when confronted with dense error logs. |
| [`systematic-debugger`](skills/debugging/systematic-debugger/SKILL.md) | Diagnoses runtime crashes, stack traces, logic failures, and test regressions using a hypothesis-driven debugging workflow. Use when code fails with an error, exception, segmentation fault, or incorrect output. |

### `documents/`

| Skill | Description |
| :--- | :--- |
| [`cheat-sheet-designer`](skills/documents/cheat-sheet-designer/SKILL.md) | Designs ultra-dense, multi-column quick-reference cheat sheets for programming languages, CLI commands, and technical tools. Use when creating fast reference guides. |
| [`latex-document-formatter`](skills/documents/latex-document-formatter/SKILL.md) | Generates clean, compilable LaTeX documents with IEEE/ACM templates, math equations, tables, and TikZ diagrams. Use when writing technical papers and lab reports in LaTeX. |
| [`markdown-table-formatter`](skills/documents/markdown-table-formatter/SKILL.md) | Creates clean, aligned, and readable Markdown comparison tables, feature matrices, and data schemas. Use when formatting tabular technical information. |
| [`pdf-report-generator`](skills/documents/pdf-report-generator/SKILL.md) | Structures clean, publication-ready markdown and styling specifications optimized for PDF conversion (Pandoc, Typst, Weasyprint). Use when preparing professional PDF documents. |

### `git/`

| Skill | Description |
| :--- | :--- |
| [`branch-strategy-planner`](skills/git/branch-strategy-planner/SKILL.md) | Designs clean git branch and release workflows (Git Flow, GitHub Flow, Trunk-Based) for student project teams. Use when coordinating collaborative team repositories. |
| [`git-commit-architect`](skills/git/git-commit-architect/SKILL.md) | Structures atomic commits, writes conventional commit messages with contextual rationale, and formats reviewable Pull Requests. Use when a user needs to commit changes, clean up git history, or prepare a PR. |
| [`gitignore-curator`](skills/git/gitignore-curator/SKILL.md) | Generates clean, language-specific .gitignore files that exclude build artifacts, virtual environments, and secrets. Use when setting up or cleaning git repositories. |
| [`merge-conflict-resolver`](skills/git/merge-conflict-resolver/SKILL.md) | Guides students step-by-step through resolving complex git merge and rebase conflicts without data loss. Use when git operations halt with conflict markers. |

### `interview/`

| Skill | Description |
| :--- | :--- |
| [`behavioral-star-framer`](skills/interview/behavioral-star-framer/SKILL.md) | Structures behavioral engineering interview responses into concise, impact-focused STAR method narratives. Use when preparing answers for behavioral questions. |
| [`dsa-pattern-matcher`](skills/interview/dsa-pattern-matcher/SKILL.md) | Maps coding interview problem statements to core Data Structures and Algorithms patterns (Two Pointers, Sliding Window, Monotonic Stack, Union-Find). Use when approaching LeetCode-style technical interview questions. |
| [`mock-interview-simulator`](skills/interview/mock-interview-simulator/SKILL.md) | Conducts structured, simulated technical coding and systems interviews with interactive problem statements, hint systems, and rubric feedback. Use when preparing for engineering job interviews. |
| [`resume-bullet-optimizer`](skills/interview/resume-bullet-optimizer/SKILL.md) | Transforms passive, task-oriented resume points into strong, impact-quantified engineering accomplishment statements. Use when editing technical resumes. |

### `learning/`

| Skill | Description |
| :--- | :--- |
| [`concept-clarifier`](skills/learning/concept-clarifier/SKILL.md) | Explains core computer science and engineering concepts through physical intuition, formal invariants, minimal traces, and complexity bounds. Use when a user asks to learn, clarify, or prepare for exams on an algorithm, system architecture, or theoretical model. |
| [`exam-drill`](skills/learning/exam-drill/SKILL.md) | Generates high-yield practice problems, edge-case questions, and conceptual drills tailored for engineering exams and technical assessments. Use when a student requests test preparation, practice questions, or concept verification. |
| [`feynman-explainer`](skills/learning/feynman-explainer/SKILL.md) | Explains complex technical and engineering phenomena using simple language, direct intuition, and zero jargon via the Feynman Technique. Use when struggling to grasp an abstract concept. |
| [`flashcard-builder`](skills/learning/flashcard-builder/SKILL.md) | Generates high-retention spaced repetition flashcards in Anki-compatible format for engineering terminology, algorithms, and architectures. Use when creating study decks. |
| [`formula-sheet-generator`](skills/learning/formula-sheet-generator/SKILL.md) | Distills complex engineering subjects into dense, high-yield formula sheets with variable definitions, units, and boundary constraints. Use when preparing review sheets for exams. |

### `productivity/`

| Skill | Description |
| :--- | :--- |
| [`cli-tool-scaffolder`](skills/productivity/cli-tool-scaffolder/SKILL.md) | Scaffolds ergonomic command-line utility tools in Python, Go, or Rust with argument parsing, subcommands, and help text. Use when building developer tools. |
| [`semester-schedule-planner`](skills/productivity/semester-schedule-planner/SKILL.md) | Organizes engineering course syllabi, assignments, exams, and project deadlines into an integrated semester timeline. Use when planning academic workloads. |
| [`study-sprint-timer`](skills/productivity/study-sprint-timer/SKILL.md) | Designs structured Pomodoro and deep-work study sprint schedules tailored for complex technical problem sets. Use when planning focused study sessions. |

### `project/`

| Skill | Description |
| :--- | :--- |
| [`api-spec-designer`](skills/project/api-spec-designer/SKILL.md) | Designs RESTful and RPC API specifications conforming to OpenAPI/Swagger standards with clear status codes and payloads. Use when defining backend interfaces. |
| [`capstone-milestone-tracker`](skills/project/capstone-milestone-tracker/SKILL.md) | Breaks multi-month senior design or capstone projects into bi-weekly deliverables with risk assessments and verification criteria. Use when tracking long-term projects. |
| [`database-schema-designer`](skills/project/database-schema-designer/SKILL.md) | Designs normalized relational SQL schemas or NoSQL document models with primary keys, indexes, and foreign constraints. Use when modeling database architectures. |
| [`project-scaffolder`](skills/project/project-scaffolder/SKILL.md) | Plans software system architectures, directory structures, data contracts, and milestone delivery roadmaps for capstones and technical builds. Use when a user is designing or starting a new software project. |
| [`readme-architect`](skills/project/readme-architect/SKILL.md) | Crafts clear, professional GitHub README files with architecture diagrams, quick-start setup commands, and feature matrices. Use when documenting software projects. |

### `research/`

| Skill | Description |
| :--- | :--- |
| [`arxiv-digest-builder`](skills/research/arxiv-digest-builder/SKILL.md) | Summarizes and categorizes recent arXiv preprints in computer science and engineering into actionable technical digests. Use when keeping up with research trends. |
| [`literature-review-matrix`](skills/research/literature-review-matrix/SKILL.md) | Builds comparative literature review matrices cross-examining research papers across methodology, datasets, and benchmark results. Use when synthesizing related works. |
| [`paper-abstract-extractor`](skills/research/paper-abstract-extractor/SKILL.md) | Extracts core problem statements, methods, and quantitative findings from academic papers into concise executive briefings. Use when quickly scanning paper suitability. |
| [`research-synthesizer`](skills/research/research-synthesizer/SKILL.md) | Analyzes academic papers, preprints, and technical surveys by assessing novelty claims, benchmark rigor, and reproducibility hurdles. Use when a user reviews research papers or prepares technical literature surveys. |

### `testing/`

| Skill | Description |
| :--- | :--- |
| [`edge-case-finder`](skills/testing/edge-case-finder/SKILL.md) | Identifies subtle boundary conditions, numeric overflows, and degenerate inputs that break code. Use when testing algorithm robustness or debugging hidden judge failures. |
| [`integration-test-planner`](skills/testing/integration-test-planner/SKILL.md) | Designs end-to-end integration test plans covering API routes, database transactions, and component interfaces. Use when verifying multi-tier systems. |
| [`mock-data-factory`](skills/testing/mock-data-factory/SKILL.md) | Generates realistic mock datasets, JSON payloads, and database seed rows conforming to specific schemas and constraints. Use when preparing test data. |
| [`unit-test-generator`](skills/testing/unit-test-generator/SKILL.md) | Generates comprehensive unit test suites with boundary assertions, fixtures, and parameterized tests. Use when writing automated tests for functions and classes. |

---

## How to Use

Each skill is self-contained in its own folder and contains a standardized `SKILL.md` file with strict YAML frontmatter:

```yaml
---
name: skill-folder-name
description: What it does and when to use it. Be specific.
---
```

### 1. In Agent-Assisted Workspaces
Add the `skills/` directory to your workspace or agent knowledge directory. The agent parses the YAML metadata and activates the corresponding skill based on your query.

### 2. Manual Instruction Injection
Copy the contents of any `SKILL.md` directly into your agent's system prompt or project instructions when working on a specific task (such as formatting a lab report, debugging a segmentation fault, or preparing for a technical interview).

### 3. Prompting Example

```text
"I received a 12-page specification for our Operating Systems virtual memory assignment.
Here is the rubric and requirements handout.
Use the assignment-decomposer skill to break this into an implementation plan with test cases."
```

---

## Repository Structure

```text
Dion/
├── assets/
│   └── dion.png
├── skills/
│   ├── assignments/
│   │   ├── assignment-decomposer/SKILL.md
│   │   ├── citation-formatter/SKILL.md
│   │   ├── lab-report-writer/SKILL.md
│   │   ├── presentation-slide-planner/SKILL.md
│   │   └── rubric-checker/SKILL.md
│   ├── coding/
│   │   ├── code-commenter/SKILL.md
│   │   ├── code-explainer/SKILL.md
│   │   ├── code-refactorer/SKILL.md
│   │   ├── complexity-analyzer/SKILL.md
│   │   └── pattern-matcher/SKILL.md
│   ├── debugging/
│   │   ├── concurrency-deadlock-detector/SKILL.md
│   │   ├── memory-leak-hunter/SKILL.md
│   │   ├── segfault-tracer/SKILL.md
│   │   ├── stack-trace-analyzer/SKILL.md
│   │   └── systematic-debugger/SKILL.md
│   ├── documents/
│   │   ├── cheat-sheet-designer/SKILL.md
│   │   ├── latex-document-formatter/SKILL.md
│   │   ├── markdown-table-formatter/SKILL.md
│   │   └── pdf-report-generator/SKILL.md
│   ├── git/
│   │   ├── branch-strategy-planner/SKILL.md
│   │   ├── git-commit-architect/SKILL.md
│   │   ├── gitignore-curator/SKILL.md
│   │   └── merge-conflict-resolver/SKILL.md
│   ├── interview/
│   │   ├── behavioral-star-framer/SKILL.md
│   │   ├── dsa-pattern-matcher/SKILL.md
│   │   ├── mock-interview-simulator/SKILL.md
│   │   └── resume-bullet-optimizer/SKILL.md
│   ├── learning/
│   │   ├── concept-clarifier/SKILL.md
│   │   ├── exam-drill/SKILL.md
│   │   ├── feynman-explainer/SKILL.md
│   │   ├── flashcard-builder/SKILL.md
│   │   └── formula-sheet-generator/SKILL.md
│   ├── productivity/
│   │   ├── cli-tool-scaffolder/SKILL.md
│   │   ├── semester-schedule-planner/SKILL.md
│   │   └── study-sprint-timer/SKILL.md
│   ├── project/
│   │   ├── api-spec-designer/SKILL.md
│   │   ├── capstone-milestone-tracker/SKILL.md
│   │   ├── database-schema-designer/SKILL.md
│   │   ├── project-scaffolder/SKILL.md
│   │   └── readme-architect/SKILL.md
│   ├── research/
│   │   ├── arxiv-digest-builder/SKILL.md
│   │   ├── literature-review-matrix/SKILL.md
│   │   ├── paper-abstract-extractor/SKILL.md
│   │   └── research-synthesizer/SKILL.md
│   └── testing/
│       ├── edge-case-finder/SKILL.md
│       ├── integration-test-planner/SKILL.md
│       ├── mock-data-factory/SKILL.md
│       └── unit-test-generator/SKILL.md
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

## Contributing

Contributions from students, researchers, and developers are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for skill authoring standards, folder hierarchy rules, and Pull Request checklists.

---

## License

This project is licensed under the [Apache-2.0 License](LICENSE).
