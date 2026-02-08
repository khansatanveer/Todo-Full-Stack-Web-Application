---
id: 1
title: "Update Project Constitution"
stage: constitution
date_iso: "2026-01-28"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "todo-app"
branch: "main"
user: "user"
command: "sp.constitution"
labels: ["constitution", "governance", "setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
---

# Update Project Constitution

## Original Prompt

```
Project: Todo Full-Stack Web Application

Objective:
Transform an existing console-based Todo application into a modern, secure, multi-user full-stack web application using an Agentic Dev Stack workflow with no manual coding.

Core principles:
- Spec-driven development: all implementation must strictly follow approved specifications
- Security-first design: authentication, authorization, and user isolation enforced at every layer
- Separation of concerns: clear boundaries between frontend, backend, database, and auth
- Deterministic behavior: same inputs must always produce the same outputs
- Maintainability: clean architecture, readable structure, and explicit responsibilities
- Reproducibility: project can be set up and run by a third party using documented steps only

Key standards:
- All features must map directly to a written spec requirement
- No manual code edits; all code must be generated via Claude Code
- REST APIs must follow consistent naming, status codes, and error handling
- Authentication must use JWT-based stateless verification
- Every backend request must validate the authenticated user
- Database queries must always be scoped to the authenticated user
- Environment variables must be used for secrets (no hard-coded credentials)

Technology constraints:
- Frontend: Next.js 16+ using App Router
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT-based)
- Auth secret: shared via BETTER_AUTH_SECRET environment variable

Functional requirements:
- Multi-user authentication (signup, signin, signout)
- Secure JWT issuance and verification
- CRUD operations for Todo tasks
- Task completion toggling
- Persistent storage across sessions
- Each user can only access their own tasks
- All API endpoints require valid authentication

Non-functional requirements:
- Stateless backend (no server-side sessions)
- Proper HTTP status codes (401, 403, 404, 200, 201)
- Responsive frontend UI
- Clear loading and error states
- Token expiration handling

Success criteria:
- Application supports multiple users with full data isolation
- Unauthorized requests are consistently rejected
- JWT tokens are correctly issued, attached, and verified
- All required API endpoints function as specified
- Frontend, backend, and database are fully integrated
- Project can be cloned, configured, and run successfully
- No security violations or cross-user data leaks detected
```

## Response Summary

Updated the project constitution file (.specify/memory/constitution.md) to align with the specified requirements for the Todo Full-Stack Web Application. The updated constitution includes:

- Core principles emphasizing spec-driven development, security-first design with multi-user isolation, technology stack compliance, and separation of concerns
- Key standards covering technology stack requirements, authentication flow, API endpoints, database models, and code patterns
- Functional and non-functional requirements sections detailing specific requirements
- Success criteria outlining the measurable outcomes for the project
- Governance section establishing the authority of the constitution

The version was incremented from 1.1.0 to 1.2.0 to reflect the significant updates made to align with the project requirements.