---
name: database-schema-designer
description: Designs normalized relational SQL schemas or NoSQL document models with primary keys, indexes, and foreign constraints. Use when modeling database architectures.
---

# Database Schema Designer

Design normalized, performant database schemas with explicit primary keys, foreign constraints, and indexing strategies.

## Trigger Conditions

Activate this skill when:
- A user is designing data models for a web application, mobile backend, or coursework database project.
- A student asks: 'Design an SQL database for a university system', 'Model this in PostgreSQL', or 'What tables do I need for an e-commerce app?'.

## Execution Protocol

Execute this database modeling sequence:

### 1. Entity-Relationship Identification
- Identify core entities, attributes, and relationship cardinalities (1:1, 1:N, N:M).
- Resolve many-to-many relationships using clean join/junction tables.

### 2. Relational Normalization (3NF)
- Enforce Third Normal Form:
  - Eliminate repeating groups (1NF).
  - Ensure all non-key attributes depend on the entire primary key (2NF).
  - Eliminate transitive dependencies (3NF).

### 3. Production-Ready SQL DDL Statements
- Write clean SQL table definitions:
  - Explicit data types (`UUID`, `VARCHAR`, `TIMESTAMP WITH TIME ZONE`, `DECIMAL`).
  - Column constraints (`NOT NULL`, `DEFAULT`, `CHECK`, `UNIQUE`).
  - Explicit `FOREIGN KEY` references with `ON DELETE CASCADE` or `ON DELETE RESTRICT`.

### 4. Indexing & Query Optimization
- Specify index definitions (`CREATE INDEX`) on high-cardinality foreign keys and search columns.

## Output Quality Rules

- Use snake_case for table and column names.
- Always include `created_at` and `updated_at` audit timestamps.
- Explicitly explain indexing trade-offs (query speed vs write throughput).
