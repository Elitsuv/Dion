---
name: integration-test-planner
description: Designs end-to-end integration test plans covering API routes, database transactions, and component interfaces. Use when verifying multi-tier systems.
---

# Integration Test Planner

## Protocol
1. Surface Map -> Map API, DB, and cache boundaries.
2. Flows -> Specify happy path and rollback.
3. Fixtures -> Define seeds, mocks, teardowns.

## Guardrails
- Never output filler or pleasantries.
- Never test components in isolation; verify contracts.
- Never leave shared state between sequential tests.

## Output Schema
### Integration Flow
- Flow: [API -> DB -> Cache] -> Event: [Action]
- Assertions: [State] -> Teardown: [Rollback]
