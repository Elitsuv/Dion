<div align="center">
  <img src="assets/dion.png" alt="Dion Logo" width="110" style="border-radius: 20%;" />
  <h1>Dion</h1>
  <p><strong>Systematic, token-optimized AI agent skills for student workflows, problem-solving, and engineering.</strong></p>
  <p>
    <a href="https://github.com/Elitsuv/Dion"><img src="https://img.shields.io/badge/skills-59-blue?style=flat-square" alt="Skills Count" /></a>
    <a href="https://agentskills.io"><img src="https://img.shields.io/badge/spec-agentskills.io-purple?style=flat-square" alt="AgentSkills Spec" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-green?style=flat-square" alt="License" /></a>
    <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/contributions-welcome-orange?style=flat-square" alt="Contributions Welcome" /></a>
  </p>
  <p>
    <a href="#built-to-save-student-tokens-how-dion-works-under-the-hood">Token Architecture</a> &bull;
    <a href="#skills-by-category">Skills Directory</a> &bull;
    <a href="#how-to-use">How to Use</a> &bull;
    <a href="#repository-structure">Structure</a> &bull;
    <a href="CONTRIBUTING.md">Contributing</a> &bull;
    <a href="LICENSE">License</a>
  </p>
</div>

---

## What Dion Is

Most AI prompts for students are bloated with conversational filler, produce shallow summaries, skip crucial mathematical steps, and burn through expensive API tokens or free-tier quotas within minutes.

**Dion** is a curated library of **59 modular Agent Skills** across **13 academic and engineering domains**, designed to fulfill a dual mission:
1. **Universal Student Agency**: Equip students and learners with systematic, universal AI agent capabilities for studying, revising, unrolling derivations, preparing for exams, coding, debugging, and building—without locking them into narrow subject silos.
2. **Native Token Optimization (`agentskills.io` spec)**: Save learners massive amounts of input and output tokens using native progressive disclosure mechanics.

No runtime dependencies. No bloated wrappers. Just high-density markdown protocols compatible with any agent runtime.

---

## Built to Save Student Tokens (How Dion Works Under the Hood)

Students and builders operate on tight API budgets and constrained free tiers. Dion implements a deterministic **3-Stage LLM Token Optimization** architecture across every skill in the repository:

```text
┌───────────────────────────────────────────────────────────────────────────┐
│                     3-STAGE TOKEN OPTIMIZATION ENGINE                     │
├───────────────────────────────────────────────────────────────────────────┤
│ STAGE 1: Cold-Start Router Diet (System Prompt Ingestion)                 │
│ • Agent runtimes inject ALL skill names and descriptions on every turn.   │
│ • Dion clamps descriptions strictly to 15–24 words (~20–26 tokens) using  │
│   a standardized formula: [Verb] + [Deliverable] + ". Use when " + [Cue]. │
│ • Entire 59-skill router footprint: ~2,296 tokens (vs 15,000+ unoptimized)│
├───────────────────────────────────────────────────────────────────────────┤
│ STAGE 2: Context Injection Diet (Markdown Skill Body)                     │
│ • When a skill activates, only its specific protocol enters context.     │
│ • Dion caps every SKILL.md body strictly below 120 tokens (~30 lines max).│
│ • Strips 100% of persona fluff ("You are a world-class tutor...") in     │
│   favor of telegraphic imperative arrows (->).                            │
│ • Exact 3-section protocol: ## Protocol, ## Guardrails, ## Output Schema. │
├───────────────────────────────────────────────────────────────────────────┤
│ STAGE 3: Output Token Clamp (Student Quota Protection)                    │
│ • Output tokens cost 3x–5x more than input tokens.                       │
│ • Dion's guardrails strictly forbid conversational pleasantries, intros,  │
│   preambles, and filler ("Sure! I'd be happy to explain that for you...").│
│ • Compact structural skeletons enforce maximum informational density      │
│   per token generated.                                                    │
└───────────────────────────────────────────────────────────────────────────┘
```

### Verified Live via Token Auditor

Dion includes a zero-dependency auditing script to verify all token budgets in terminal:

```bash
python scripts/audit_tokens.py
```

```text
================================================================================================
DION AGENT SKILLS: 3-STAGE LLM TOKEN OPTIMIZATION AUDIT
Spec: agentskills.io progressive disclosure | Target: Body < 120 toks, Desc 15-24 words
================================================================================================
Audit Summary: 59 total skills | 59 PASSED | 0 FAILED
Aggregate Token Footprint (Passing): Router=2296 toks (avg 38.9) | Body=6647 toks (avg 112.7)
All skills 100% compliant with 3-Stage Token Optimization architecture!
```

---

## Skills by Category

Total active skills: **59** across **13** academic and engineering domains.

### `assignments/` (Coursework & Submission Planning)

| Skill | Description |
| :--- | :--- |
| [`assignment-decomposer`](skills/assignments/assignment-decomposer/SKILL.md) | Deconstructs complex assignment rubrics into milestone subtasks, dependency sequences, and verification tests. Use when planning an academic coursework submission. |
| [`citation-formatter`](skills/assignments/citation-formatter/SKILL.md) | Formats and validates academic bibliographies across IEEE, ACM, APA, and BibTeX standards without syntax errors. Use when compiling research paper references. |
| [`lab-report-writer`](skills/assignments/lab-report-writer/SKILL.md) | Structures engineering laboratory reports with formal abstracts, error propagation models, and tabular observations. Use when drafting scientific or lab submissions. |
| [`presentation-slide-planner`](skills/assignments/presentation-slide-planner/SKILL.md) | Plans technical slide decks and defense talks with time allocations, key visuals, and speaker cues. Use when structuring academic project presentations. |
| [`rubric-checker`](skills/assignments/rubric-checker/SKILL.md) | Evaluates coursework drafts against official grading rubrics to diagnose missing criteria and scoring vulnerabilities. Use when auditing drafts prior to submission. |

### `coding/` (Source Architecture & Algorithmic Rigor)

| Skill | Description |
| :--- | :--- |
| [`code-commenter`](skills/coding/code-commenter/SKILL.md) | Generates concise docstrings, function contracts, and invariant comments explaining logic rationale rather than syntax. Use when documenting technical source code. |
| [`code-explainer`](skills/coding/code-explainer/SKILL.md) | Deconstructs complex algorithms and codebases by tracing execution states, memory mutations, and asymptotic bounds. Use when analyzing unfamiliar technical implementations. |
| [`code-refactorer`](skills/coding/code-refactorer/SKILL.md) | Refactors messy source code into idiomatic, modular, and maintainable architectures while preserving functional behavior. Use when cleaning technical code implementations. |
| [`complexity-analyzer`](skills/coding/complexity-analyzer/SKILL.md) | Derives formal asymptotic Big-O time and space complexity using recurrence relations and loop summations. Use when evaluating algorithmic efficiency. |
| [`pattern-matcher`](skills/coding/pattern-matcher/SKILL.md) | Identifies optimal software design patterns and architectural idioms to resolve structural coupling problems. Use when architecting object-oriented software systems. |

### `debugging/` (Fault Isolation & Memory Diagnostics)

| Skill | Description |
| :--- | :--- |
| [`concurrency-deadlock-detector`](skills/debugging/concurrency-deadlock-detector/SKILL.md) | Identifies race conditions, deadlocks, and synchronization bugs in multithreaded and asynchronous software. Use when concurrent code hangs or behaves nondeterministically. |
| [`memory-leak-hunter`](skills/debugging/memory-leak-hunter/SKILL.md) | Analyzes Valgrind logs, AddressSanitizer dumps, and heap profiles to pinpoint unreleased allocations and pointer leaks. Use when debugging memory management. |
| [`segfault-tracer`](skills/debugging/segfault-tracer/SKILL.md) | Diagnoses segmentation faults and memory corruption errors by analyzing pointer arithmetic, null references, and stack frames. Use when applications crash with SIGSEGV. |
| [`stack-trace-analyzer`](skills/debugging/stack-trace-analyzer/SKILL.md) | Parses dense compiler dumps and multithreaded stack traces to isolate the originating root-cause failure frame. Use when debugging runtime crashes. |
| [`systematic-debugger`](skills/debugging/systematic-debugger/SKILL.md) | Diagnoses runtime crashes, regressions, and logic bugs using scientific falsification trees and minimal reproduction cases. Use when debugging failing code systems. |

### `documents/` (Publishing & Formatting Systems)

| Skill | Description |
| :--- | :--- |
| [`cheat-sheet-designer`](skills/documents/cheat-sheet-designer/SKILL.md) | Designs ultra-dense, multi-column technical cheat sheets for programming languages, CLI utilities, and mathematical conventions. Use when synthesizing quick-reference study guides. |
| [`latex-document-formatter`](skills/documents/latex-document-formatter/SKILL.md) | Generates clean, compilable LaTeX code with formal IEEE and ACM formatting, math environments, and tables. Use when formatting academic papers. |
| [`markdown-table-formatter`](skills/documents/markdown-table-formatter/SKILL.md) | Constructs clean, column-aligned Markdown comparison tables, feature matrices, and technical schemas without formatting inconsistencies. Use when structuring tabular documentation. |
| [`pdf-report-generator`](skills/documents/pdf-report-generator/SKILL.md) | Structures clean, publication-ready markdown and CSS specifications optimized for headless PDF rendering engines. Use when generating exportable technical documents. |

### `exam-prep/` (Question Making & Exam Mastery)

| Skill | Description |
| :--- | :--- |
| [`question-bank-generator`](skills/exam-prep/question-bank-generator/SKILL.md) | Generates tiered practice questions from foundational to advanced trap levels with hidden solutions. Use when practicing a topic or syllabus module. |
| [`mistake-autopsy-analyzer`](skills/exam-prep/mistake-autopsy-analyzer/SKILL.md) | Diagnoses wrong answers from practice sessions into root-cause categories with targeted remedial fixes. Use when reviewing practice test or exam errors. |
| [`pyq-pattern-decoder`](skills/exam-prep/pyq-pattern-decoder/SKILL.md) | Extracts recurring question archetypes, high-yield subtopics, and traps from past exam papers. Use when planning exam strategy or paper analysis. |
| [`speed-solve-optimizer`](skills/exam-prep/speed-solve-optimizer/SKILL.md) | Optimizes exam problem-solving speed using dimensional analysis, symmetry shortcuts, and elimination heuristics. Use when improving timed test-solving efficiency. |

### `git/` (Version Control & Collaboration)

| Skill | Description |
| :--- | :--- |
| [`branch-strategy-planner`](skills/git/branch-strategy-planner/SKILL.md) | Designs clean git branching and release workflows like GitHub Flow and Trunk-Based Development. Use when establishing collaborative team version control. |
| [`git-commit-architect`](skills/git/git-commit-architect/SKILL.md) | Structures atomic git commits and drafts conventional commit messages with clear engineering rationale. Use when staging changes or preparing pull requests. |
| [`gitignore-curator`](skills/git/gitignore-curator/SKILL.md) | Generates clean, language-specific gitignore configurations excluding build artifacts, caches, and secrets. Use when initializing or cleaning git repositories. |
| [`merge-conflict-resolver`](skills/git/merge-conflict-resolver/SKILL.md) | Guides step-by-step resolution of git merge and rebase conflicts without data loss. Use when git operations halt with conflict markers. |

### `interview/` (Technical & Behavioral Assessments)

| Skill | Description |
| :--- | :--- |
| [`behavioral-star-framer`](skills/interview/behavioral-star-framer/SKILL.md) | Structures technical interview responses into concise, impact-quantified STAR method narratives. Use when preparing for behavioral and cultural interviews. |
| [`dsa-pattern-matcher`](skills/interview/dsa-pattern-matcher/SKILL.md) | Maps algorithmic coding interview problems to core data structure and algorithm patterns. Use when solving competitive programming and LeetCode problems. |
| [`mock-interview-simulator`](skills/interview/mock-interview-simulator/SKILL.md) | Conducts simulated technical coding and systems design interviews with graduated hints and rubric evaluations. Use when practicing engineering interviews. |
| [`resume-bullet-optimizer`](skills/interview/resume-bullet-optimizer/SKILL.md) | Transforms passive student resume bullet points into impact-quantified engineering accomplishment statements. Use when editing technical resumes. |

### `learning/` (Chapter Mastery & Conceptual Understanding)

| Skill | Description |
| :--- | :--- |
| [`chapter-synthesizer`](skills/learning/chapter-synthesizer/SKILL.md) | Condenses full chapters or lecture notes into mental models, governing laws, and testable invariants. Use when starting or summarizing a syllabus chapter. |
| [`concept-clarifier`](skills/learning/concept-clarifier/SKILL.md) | Explains core computing concepts through formal invariants, physical analogies, and minimal traces. Use when clarifying complex algorithms, architectures, or theoretical models. |
| [`derivation-unroller`](skills/learning/derivation-unroller/SKILL.md) | Expands skipped steps in textbook proofs and mathematical derivations into line-by-line transitions. Use when a step in a proof feels unclear. |
| [`exam-drill`](skills/learning/exam-drill/SKILL.md) | Generates high-yield practice problems, edge-case drills, and verification questions for engineering exams. Use when preparing for tests or concept assessments. |
| [`feynman-explainer`](skills/learning/feynman-explainer/SKILL.md) | Explains difficult technical and scientific concepts using plain language, intuitive analogies, and zero jargon. Use when struggling with abstract theoretical topics. |
| [`flashcard-builder`](skills/learning/flashcard-builder/SKILL.md) | Generates high-retention spaced repetition flashcards in Anki-compatible format for technical terms and formulas. Use when preparing long-term study decks. |
| [`formula-sheet-generator`](skills/learning/formula-sheet-generator/SKILL.md) | Distills technical subjects into dense formula sheets with variable definitions, physical units, and validity boundaries. Use when preparing exam cheat sheets. |
| [`memory-hook-builder`](skills/learning/memory-hook-builder/SKILL.md) | Generates high-retention mnemonics, contrast tables, and intuitive analogies for dense academic concepts. Use when memorizing tricky facts, formulas, or edge cases. |
| [`socratic-hint-tutor`](skills/learning/socratic-hint-tutor/SKILL.md) | Guides students through challenging academic problems using graduated conceptual hints and questions. Use when clearing concepts or stuck on a problem. |

### `productivity/` (Study Habits & Backlog Recovery)

| Skill | Description |
| :--- | :--- |
| [`active-recall-quizzer`](skills/productivity/active-recall-quizzer/SKILL.md) | Executes rapid-fire active recall questioning on notes and evaluates student answers without conversational filler. Use when testing knowledge retention after reading. |
| [`cli-tool-scaffolder`](skills/productivity/cli-tool-scaffolder/SKILL.md) | Scaffolds ergonomic command-line utility tools in Python, Go, or Rust with argument parsing and subcommands. Use when building developer tools. |
| [`semester-schedule-planner`](skills/productivity/semester-schedule-planner/SKILL.md) | Organizes academic course syllabi, assignments, exams, and project milestones into a structured semester timeline. Use when planning coursework workloads. |
| [`study-sprint-timer`](skills/productivity/study-sprint-timer/SKILL.md) | Designs structured Pomodoro and deep-work sprint schedules tailored for complex technical problem sets. Use when planning focused study sessions. |
| [`syllabus-backlog-crusher`](skills/productivity/syllabus-backlog-crusher/SKILL.md) | Constructs dependency-aware daily study schedules to clear accumulated syllabus backlogs before deadlines. Use when falling behind on academic coursework targets. |

### `project/` (Architecture & Build Scaffolding)

| Skill | Description |
| :--- | :--- |
| [`api-spec-designer`](skills/project/api-spec-designer/SKILL.md) | Designs RESTful and RPC API specifications conforming to OpenAPI standards with schemas and error payloads. Use when defining backend service contracts. |
| [`capstone-milestone-tracker`](skills/project/capstone-milestone-tracker/SKILL.md) | Breaks multi-month senior design and capstone projects into bi-weekly deliverables with risk assessments. Use when tracking engineering capstone projects. |
| [`database-schema-designer`](skills/project/database-schema-designer/SKILL.md) | Designs normalized relational SQL schemas or NoSQL document models with indexes, keys, and integrity constraints. Use when architecting database storage. |
| [`project-scaffolder`](skills/project/project-scaffolder/SKILL.md) | Plans software directory structures, modular architectures, data contracts, and milestone roadmaps. Use when bootstrapping new technical engineering projects. |
| [`readme-architect`](skills/project/readme-architect/SKILL.md) | Crafts professional GitHub README files with architectural diagrams, quickstart setup guides, and feature tables. Use when documenting technical repositories. |

### `research/` (Academic Literature & Preprints)

| Skill | Description |
| :--- | :--- |
| [`arxiv-digest-builder`](skills/research/arxiv-digest-builder/SKILL.md) | Summarizes recent arXiv preprints into actionable technical digests with core contributions and benchmark results. Use when tracking research literature. |
| [`literature-review-matrix`](skills/research/literature-review-matrix/SKILL.md) | Builds comparative literature review matrices cross-examining research papers across methodology, datasets, and benchmark results. Use when synthesizing related works. |
| [`paper-abstract-extractor`](skills/research/paper-abstract-extractor/SKILL.md) | Extracts problem statements, proposed methodologies, and quantitative results from academic papers into structured briefings. Use when screening academic literature. |
| [`research-synthesizer`](skills/research/research-synthesizer/SKILL.md) | Evaluates academic papers by assessing novelty claims, benchmark rigor, and reproducibility hurdles. Use when reviewing research papers or literature surveys. |

### `revision/` (Last-Minute Trigger Sheets)

| Skill | Description |
| :--- | :--- |
| [`revision-sheet-compressor`](skills/revision/revision-sheet-compressor/SKILL.md) | Compresses bulky study notes into an ultra-dense one-page revision trigger sheet. Use when preparing for upcoming exams, finals, or mock tests. |

### `testing/` (Verification & Edge Cases)

| Skill | Description |
| :--- | :--- |
| [`edge-case-finder`](skills/testing/edge-case-finder/SKILL.md) | Identifies subtle boundary conditions, numeric overflows, and degenerate inputs that break code. Use when testing algorithm robustness or debugging failures. |
| [`integration-test-planner`](skills/testing/integration-test-planner/SKILL.md) | Designs end-to-end integration test plans covering API routes, database transactions, and component interfaces. Use when verifying multi-tier systems. |
| [`mock-data-factory`](skills/testing/mock-data-factory/SKILL.md) | Generates realistic mock datasets, JSON payloads, and database seed rows conforming to specific schemas. Use when preparing test data. |
| [`unit-test-generator`](skills/testing/unit-test-generator/SKILL.md) | Generates comprehensive unit test suites with boundary assertions, fixtures, and parameterized test cases. Use when writing automated code tests. |

---

## How to Use

Each skill follows the standard `agentskills.io` directory format:

```text
skills/<category>/<skill-name>/SKILL.md
```

### 1. In AI Agent Runtimes
Drop the `skills/` directory into your agent workspace (Antigravity, Claude Code, Cursor, Copilot, etc.). The runtime discovers all skills via the YAML router and activates the relevant protocol when triggered.

### 2. Direct Instruction Injection
Copy the contents of any `SKILL.md` directly into your system prompt or custom instructions when tackling a focused task (e.g., preparing for a midterm with `mistake-autopsy-analyzer`, or unrolling a skipped textbook proof with `derivation-unroller`).

### 3. Prompting Examples

#### Example A: Studying & Derivation
```text
"I am studying Chapter 4 of my Electrodynamics notes. Between equation 4.12 and 4.13, 
the textbook skips three steps with 'it follows trivially'.
Use derivation-unroller to unroll the intermediate algebra line by line."
```

#### Example B: Exam Preparation & Error Review
```text
"Here is the problem from yesterday's calculus mock test, my attempted working, 
and the examiner's answer key.
Use mistake-autopsy-analyzer to categorize my mistake and give me a targeted counter-drill."
```

#### Example C: Backlog Recovery Schedule
```text
"I have 6 uncompleted operating systems modules and my exam is in 10 days. 
Here are the syllabus topics.
Use syllabus-backlog-crusher to build a realistic dependency-aware daily study schedule."
```

---

## Contributing

We welcome contributions from students, researchers, and engineers. Please read [CONTRIBUTING.md](CONTRIBUTING.md) to understand the strict 24-word description ceiling and 120-token body diet before opening a Pull Request.

---

## License

This project is licensed under the [Apache-2.0 License](LICENSE).
