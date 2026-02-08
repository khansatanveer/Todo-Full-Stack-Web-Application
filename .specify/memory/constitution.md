<!-- SYNC IMPACT REPORT
Version change: 1.1.0 → 1.2.0
Modified principles: Security-first → Security-first design with multi-user isolation, Exact monorepo structure & declared stack only → Technology stack compliance with Next.js 16+, Agentic purity → Spec-driven development with no manual coding
Added sections: Core principles (Multi-user data isolation, Statelessness, Environment variables), Key standards section, Functional requirements section, Non-functional requirements section, Success criteria section
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/commands/sp.constitution.md ✅ updated
Follow-up TODOs: None
-->

# Todo Full-Stack Web Application Constitution

## Core Principles

### Spec-driven development with no manual coding
All implementation must strictly follow approved specifications: All code changes must originate from written specifications; No manual code edits allowed - all code must be generated via Claude Code; Every feature must map directly to a written spec requirement; Implementation must follow specifications precisely without deviation.

### Security-first design with multi-user isolation
Authentication, authorization, and user isolation enforced at every layer: Mandatory JWT validation on all API routes; Every request must validate authenticated user context; Each user can only access their own tasks; Database queries must always be scoped to the authenticated user; Unauthorized requests must return 401 status.

### Technology stack compliance with Next.js 16+
Strict adherence to specified technology stack: Frontend: Next.js 16+ using App Router with TypeScript and Tailwind CSS; Backend: Python FastAPI with SQLModel; Database: Neon Serverless PostgreSQL; Authentication: Better Auth (JWT-based); No deviations from specified technology stack without explicit constitutional amendment.

### Separation of concerns
Clear boundaries between application layers: Frontend handles presentation logic only; Backend manages business logic and API endpoints; Database stores persistent data; Authentication layer manages user identity; Each layer has explicit responsibilities and clear interfaces.

## Key Standards

### Technology Stack Requirements
- Frontend: Next.js 16+ using App Router + TypeScript + Tailwind CSS + shadcn/ui + Better Auth
- Backend: Python FastAPI with SQLModel ORM
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT-based stateless verification
- Environment variables: BETTER_AUTH_SECRET (shared across services)

### Authentication Flow
Better Auth JWT issuance and verification: Frontend authentication via Better Auth; JWT token issuance upon successful authentication; FastAPI middleware validates JWT tokens on all protected endpoints; User ID extraction from verified tokens; Backend re-validation of ownership on every request.

### API Endpoints
REST API consistency and authentication: All endpoints require valid authentication; Consistent naming, status codes, and error handling; Proper HTTP status codes (401, 403, 404, 200, 201); Every backend request must validate the authenticated user; Response schemas follow documented contracts.

### Database Models/Schema
SQLModel entity compliance: Models must match schema specification exactly; Users table managed by Better Auth; No schema changes outside specification; SQLModel entities must reflect documented schema; Database queries must filter by authenticated user_id.

### Code Patterns
Follow established coding conventions: Adhere to documented coding patterns; Consistent response formats; Tailwind classes only (no inline styles); Proper separation of concerns between application layers; Explicit error paths and constraints stated.

## Functional Requirements

### Authentication Features
- Multi-user authentication (signup, signin, signout)
- Secure JWT issuance and verification
- User session management with proper token handling

### Todo Management
- CRUD operations for Todo tasks (create, read, update, delete)
- Task completion toggling functionality
- Persistent storage across sessions
- Each user can only access their own tasks

### API Requirements
- All API endpoints require valid authentication
- Proper request/response validation
- Consistent error handling and status codes

## Non-functional Requirements

### Performance and Reliability
- Stateless backend (no server-side sessions)
- Proper HTTP status codes implementation
- Responsive frontend UI with smooth interactions
- Clear loading and error states for all operations
- Token expiration handling and refresh mechanisms

### Security Requirements
- JWT-based stateless verification
- User data isolation and access control
- No hard-coded credentials or secrets
- Environment variables for sensitive configuration
- Proper authentication validation on every request

### Quality Standards
- Clean, maintainable code structure
- Comprehensive error handling
- Proper input validation
- Consistent API behavior and responses

## Success Criteria

1. Application supports multiple users with full data isolation: Each user can only access their own data; Database queries properly filter by user_id; Authentication and authorization prevent cross-user access.

2. Unauthorized requests are consistently rejected: All protected endpoints require valid authentication; Invalid tokens return appropriate 401 status codes; Unauthenticated access attempts are properly blocked.

3. JWT tokens are correctly issued, attached, and verified: Token issuance works correctly during authentication; Tokens are properly attached to API requests; Backend verifies tokens consistently across all endpoints.

4. All required API endpoints function as specified: Create, read, update, delete operations work correctly; Task completion toggling functions properly; All endpoints properly authenticate and authorize requests.

5. Frontend, backend, and database are fully integrated: Services communicate seamlessly; Data flows correctly between layers; User actions trigger appropriate backend operations.

6. Project can be cloned, configured, and run successfully: Complete setup instructions work; Environment variables properly configured; All dependencies resolve correctly.

7. No security violations or cross-user data leaks detected: Penetration testing passes; Data isolation maintained under concurrent usage; Authentication mechanisms prevent unauthorized access.

## Governance

This constitution governs all development activities and supersedes any conflicting practices. All implementation work must strictly adhere to the principles and standards outlined above. Amendments require explicit documentation and approval through the constitutional update process. All code generation must follow the agentic development workflow (spec → plan → tasks → implementation via Claude Code). The constitution ensures consistent, secure, and specification-driven development practices across the entire project lifecycle.

**Version**: 1.2.0 | **Ratified**: 2026-01-08 | **Last Amended**: 2026-01-28