---
name: database-schema-designer
description: Designs normalized relational SQL schemas or NoSQL document models with indexes, keys, and integrity constraints. Use when architecting database storage.
---

# Database Schema Designer

## Protocol
1. Entities -> Identify entities, primary keys, relationships.
2. Normalize -> Enforce Third Normal Form (3NF) for integrity.
3. Optimize -> Define indexes and foreign keys for top queries.

## Guardrails
- Never output filler or pleasantries.
- Never omit primary keys or foreign key constraints.
- Never define columns without data types and nullability.

## Output Schema
### SQL DDL Schema
[Clean SQL table definitions with constraints]
- `CREATE INDEX idx_[table]_[col] ON [table]([col]);`
