---
name: mock-data-factory
description: Generates realistic mock datasets, JSON payloads, and database seed rows conforming to specific schemas and constraints. Use when preparing test data.
---

# Mock Data Factory

Synthesize realistic, schema-compliant mock datasets, JSON payloads, and relational test fixtures.

## Trigger Conditions

Activate this skill when:
- A user needs sample data to test an API, populate a database, or benchmark an algorithm.
- A student asks: 'Generate sample JSON data for an e-commerce API', 'Create SQL seed data for this schema', or 'Give me 50 mock users with realistic addresses'.

## Execution Protocol

Follow this data generation sequence:

### 1. Schema & Constraint Ingestion
- Extract data requirements:
  - Field names and types (strings, integers, timestamps, UUIDs, booleans).
  - Relational foreign key dependencies.
  - Validation constraints: unique values, regex formats, realistic value distributions.

### 2. Realistic Value Synthesis
- Generate authentic-looking domain data (names, emails, timestamps, addresses) rather than repetitive placeholders (`test1`, `test2`).
- Maintain valid referential integrity across related entities (e.g., `order.user_id` matches an existing `user.id`).

### 3. Format Customization
Deliver data in the requested representation:
- **JSON / REST**: Clean formatted JSON arrays with nested relationships.
- **SQL DDL / DML**: `INSERT INTO` statements with valid syntax and escaped strings.
- **CSV**: Tabular text with valid headers and escaped delimiters.

### 4. Anonymization & Security Guard
- Ensure all synthetic data contains zero real-world personal identification information (PII).

## Output Quality Rules

- Ensure all generated dates, IDs, and foreign keys are consistent and valid.
- Provide clean, copy-pasteable data structures without truncation.
