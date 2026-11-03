---
name: api-spec-designer
description: Designs RESTful and RPC API specifications conforming to OpenAPI/Swagger standards with clear status codes and payloads. Use when defining backend interfaces.
---

# API Spec Designer

Design clean, consistent, and RESTful API specifications with standard HTTP status codes and JSON contracts.

## Trigger Conditions

Activate this skill when:
- A user is designing a backend service, microservice interface, or client-server contract.
- A student asks: 'Design REST endpoints for my app', 'Write an OpenAPI/Swagger spec for this service', or 'Review my API routes'.

## Execution Protocol

Follow these RESTful API design standards:

### 1. Resource Modeling & URI Conventions
- Use plural nouns for resources (e.g., `/api/v1/courses`, `/api/v1/students`).
- Use proper HTTP verbs:
  - `GET`: Retrieve resource (safe and idempotent).
  - `POST`: Create resource.
  - `PUT`: Full update of resource (idempotent).
  - `PATCH`: Partial update of resource.
  - `DELETE`: Remove resource (idempotent).

### 2. Request & Response Payload Contracts
For every endpoint, specify:
- URL parameters and query filters.
- Request body JSON schema with required vs optional fields.
- Response body JSON schema for successful calls.

### 3. HTTP Status Codes & Error Envelope
- Define explicit standard status codes:
  - `200 OK`, `201 Created`, `204 No Content`.
  - `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `409 Conflict`, `422 Unprocessable Entity`.
- Provide a consistent error envelope:
  ```json
  {
    "error": {
      "code": "INVALID_INPUT",
      "message": "Field 'email' must be a valid email address.",
      "details": []
    }
  }
  ```

### 4. Pagination, Filtering & Sorting
- Standardize query parameters for collection endpoints (`?limit=20&page=1&sort=-created_at`).

## Output Quality Rules

- Maintain strict RESTful verb-noun consistency (e.g., avoid `/api/getUsers` or `/api/deleteUser`).
- Include realistic example payloads for both success and error responses.
