---
name: project-scaffolder
description: Plans software system architectures, directory structures, data contracts, and milestone delivery roadmaps for capstones and technical builds. Use when a user is designing or starting a new software project.
---

# Project Scaffolder

Architect semester projects, capstone deliverables, and software systems into modular, testable structures.

## Trigger Conditions

Activate this skill when:
- A user is initiating a capstone project, semester coursework build, technical prototype, or hackathon project.
- A user asks: "How should I structure my project?", "Plan my software architecture", or "What stack and folder layout should I use for building X?".

---

## Execution Protocol

Execute the architectural planning sequence across these 5 phases:

### 1. Scope Boundaries (MVP vs Later)
- Establish strict scope boundaries:
  - **Must-Have (MVP)**: The single end-to-end user loop required to prove feasibility.
  - **Should-Have**: Secondary capabilities (caching, authentication, export features).
  - **Won't-Have (Initial Phase)**: Premature microservice splits, custom infrastructure, or distributed queues.

### 2. Component Topology & Protocols
- Define the high-level architecture:
  - Ingestion / API layer (HTTP, WebSocket, gRPC).
  - Domain / Business Logic layer (framework-agnostic entities and handlers).
  - Storage / Persistence layer (database schema, repository interfaces).
- Emphasize modular monoliths over complex microservices for small engineering teams.

### 3. Standardized Directory Layout
- Provide a clean, language-idiomatic project structure:
  ```text
  project-root/
  ├── src/
  │   ├── core/           # Domain entities and interfaces
  │   ├── services/       # Business logic and orchestration
  │   ├── api/            # Route handlers and request serializers
  │   └── storage/        # Database models and storage adapters
  ├── tests/
  │   ├── unit/
  │   └── integration/
  ├── docs/
  ├── .gitignore
  └── README.md
  ```

### 4. Schema & Interface Contracts
- Specify initial data entities, relational mappings, and primary keys.
- Define core API route contracts with explicit request and response payload definitions.

### 5. Four-Stage Milestone Delivery Plan
- Structure deliverables into clear milestones:
  - **Milestone 1: Proof of Architecture**: Base skeleton, database connection established, single passing end-to-end integration test.
  - **Milestone 2: Core Loop Implementation**: Core domain models populated, primary workflow functioning end-to-end.
  - **Milestone 3: Error Handling & Verification**: Boundary validation, automated test suite, structured logging.
  - **Milestone 4: Packaging & Demonstration**: Clean environment reproduction script, architecture documentation, deployment setup.

---

## Output Quality Rules

- Favor battle-tested, standard technologies over bleeding-edge frameworks that create setup friction.
- Decouple domain business logic from specific transport protocols and database libraries to enable straightforward unit testing.
