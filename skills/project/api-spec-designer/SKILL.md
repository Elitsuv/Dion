---
name: api-spec-designer
description: Designs RESTful and RPC API specifications conforming to OpenAPI standards with schemas and error payloads. Use when defining backend service contracts.
---

# API Spec Designer

## Protocol
1. Model -> Define RESTful resources, paths, and HTTP methods.
2. Contract -> Specify query parameters, headers, and schemas.
3. Errors -> Define standard error codes (4xx/5xx) and payloads.

## Guardrails
- Never output filler or pleasantries.
- Never omit error response schemas for bad requests.
- Never use verbs in RESTful URI resource paths.

## Output Schema
### Endpoint Spec
- `[METHOD] /api/v1/[resource]`
[OpenAPI YAML/JSON contract block]
- Errors: `{"error": "[type]", "detail": "[msg]"}`
