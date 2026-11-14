---
name: mock-data-factory
description: Generates realistic mock datasets, JSON payloads, and database seed rows conforming to specific schemas. Use when preparing test data.
---

# Mock Data Factory

## Protocol
1. Parse -> Extract schema fields, data types, and foreign keys.
2. Seed -> Generate syntactically valid records matching rules.
3. Inject Edges -> Insert boundary values: max lengths, nulls.

## Guardrails
- Never output filler or pleasantries.
- Never generate repetitive dummy values like 'foo1'.
- Never violate foreign key dependencies or constraints.

## Output Schema
### Mock Dataset
```json
[{ "id": "uuid-1", "name": "...", "status": "active" }]
```
- Integrity: [Pass/fail check against constraints]
