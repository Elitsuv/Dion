---
name: readme-architect
description: Crafts clear, professional GitHub README files with architecture diagrams, quick-start setup commands, and feature matrices. Use when documenting software projects.
---

# README Architect

Author clean, comprehensive, and professional GitHub README files for software projects and open-source repositories.

## Trigger Conditions

Activate this skill when:
- A user is publishing a software project, course capstone, or open-source tool and needs a README.
- A student asks: 'Write a professional README for my project', 'How do I document my GitHub repo?', or 'Structure a README for my capstone'.

## Execution Protocol

Follow this standard repository documentation hierarchy:

### 1. Title, Tagline & Status Badges
- Provide a clear project title and a sharp 1-sentence description answering *what problem it solves*.
- Add relevant build, license, and version badges where appropriate.

### 2. Architecture Overview & Key Features
- High-level overview of the system architecture.
- Bulleted list of 4–6 core features with concrete technical descriptions.

### 3. Prerequisites & Quick-Start Setup
- Document exact installation and execution commands:
  ```bash
  # Clone and setup
  git clone <repo-url>
  cd <repo-name>
  # Dependency installation
  <install-command>
  # Run application or test suite
  <run-command>
  ```
- Detail required environment variables and configuration files (`.env.example`).

### 4. Project Directory Layout
- Provide a concise visual tree of the repository structure.

### 5. API / Usage Documentation & Demo
- Show minimal usage examples, CLI flags, or core API endpoints with sample curl commands.

### 6. License & Acknowledgments
- State the project license and acknowledge relevant libraries or course mentors.

## Output Quality Rules

- Keep setup instructions verifiable and copy-pasteable.
- Avoid vague marketing text; focus on technical clarity and reproducible execution.
