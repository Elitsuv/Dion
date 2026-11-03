---
name: integration-test-planner
description: Designs end-to-end integration test plans covering API routes, database transactions, and component interfaces. Use when verifying multi-tier systems.
---

# Integration Test Planner

Design end-to-end integration test strategies verifying multi-tier software component interactions.

## Trigger Conditions

Activate this skill when:
- A user is connecting frontend, backend API, and database layers and needs an integration testing plan.
- A student asks: 'How do I test my full API pipeline?', 'Write an integration test plan for my web app', or 'Plan testing between my service and database'.

## Execution Protocol

Execute this integration testing workflow:

### 1. Interface Boundary Identification
- Map the critical integration points in the system architecture:
  - Client -> API Gateway / HTTP Routes.
  - Controllers -> Business Service Logic.
  - Service Logic -> Database / Storage Layer.
  - Backend -> External Third-Party APIs or Message Brokers.

### 2. Core User Journey End-to-End Scenarios
Define sequential scenarios that cross multiple components:
- *Scenario 1 (Happy Path Lifecycle)*: Create user -> Authenticate -> Perform core business transaction -> Verify persistent database state.
- *Scenario 2 (Failure & Rollback)*: Initiate transaction -> Simulate downstream failure -> Verify database transaction rollbacks without partial state corruption.

### 3. Environment Teardown & Isolation Strategy
- Detail test isolation mechanisms:
  - In-memory ephemeral databases vs Docker containerized test databases.
  - Fixture setup and teardown routines to reset state between test runs.
  - Authentication token seeding and environment variable overrides.

### 4. Test Execution Matrix
- Tabulate the planned tests:
  | Scenario | Endpoint / Components | Input State | Expected State & Database Verification |
  | :--- | :--- | :--- | :--- |
  | User Registration | `POST /api/v1/users` | Valid email, password | HTTP 201; password hashed in DB table |

## Output Quality Rules

- Focus on component interactions, serialization, and persistence, not isolated unit logic.
- Always include database rollback and teardown strategies to prevent state pollution.
