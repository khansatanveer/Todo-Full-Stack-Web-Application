# Implementation Plan: JWT Authentication Integration

**Branch**: `002-jwt-auth-integration` | **Date**: 2026-02-03 | **Spec**: [link](./spec.md)
**Input**: Feature specification from `/specs/002-jwt-auth-integration/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of JWT-based authentication system for a multi-user Todo application. The system will use Better Auth for frontend authentication to issue JWT tokens, which will then be validated by the FastAPI backend. Each user will only be able to access their own tasks, with strict isolation enforced at the database query level.

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript/JavaScript (frontend)
**Primary Dependencies**: FastAPI, Better Auth, SQLModel, Next.js 16+ with App Router
**Storage**: Neon Serverless PostgreSQL via SQLModel
**Testing**: pytest (backend), vitest (frontend) - NEEDS CLARIFICATION
**Target Platform**: Web application (Linux/Mac/Windows compatible)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <500ms response time for authenticated requests, support 1000+ concurrent users - NEEDS CLARIFICATION
**Constraints**: Stateless authentication (no server-side sessions), JWT validation on all endpoints, user data isolation
**Scale/Scope**: Multi-user support with individual task ownership, 7-day JWT expiration

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Security-first design with multi-user isolation**: All API routes will require JWT validation, with user context validated on each request to ensure data isolation. ✓ PASSED - Plan includes JWT validation on all endpoints and user_id filtering in database queries.
2. **Technology stack compliance with Next.js 16+**: Implementation will use Next.js 16+ with App Router, FastAPI, and Better Auth as specified. ✓ PASSED - Plan uses exactly the required technology stack.
3. **Separation of concerns**: Clear boundaries between frontend (presentation), backend (business logic), and database (storage). ✓ PASSED - Plan defines clear separation between frontend authentication, backend validation, and database storage.
4. **Spec-driven development**: All implementation will follow the detailed specification created in the previous step. ✓ PASSED - Plan directly implements the requirements from the feature specification.

## Project Structure

### Documentation (this feature)

```text
specs/002-jwt-auth-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── core/
│   │   └── auth.py              # JWT verification middleware
│   ├── api/
│   │   └── task_routes.py       # Protected task endpoints
│   └── main.py                  # API router inclusion
└── tests/

frontend/
├── app/
│   ├── lib/
│   │   ├── auth.ts              # Better Auth configuration
│   │   └── api/
│   │       └── client.ts        # API client with JWT attachment
│   └── ...                      # Pages/components using API
└── tests/
```

**Structure Decision**: Web application structure selected as the feature requires both frontend authentication (Better Auth) and backend API protection (FastAPI JWT validation). The frontend handles user authentication and token management, while the backend validates tokens and enforces user data isolation.

## Implementation Roadmap

### Phase 1: Backend Authentication Layer
1. **File**: `backend/src/core/auth.py`
   - **Task**: Create `get_current_user(request: Request)` function
   - **Explanation**: Extracts and verifies JWT token from Authorization header using BETTER_AUTH_SECRET
   - **Dependencies**: Environment variables for BETTER_AUTH_SECRET

2. **File**: `backend/src/main.py`
   - **Task**: Include task routes with `/api` prefix
   - **Explanation**: Sets up the API router to handle protected endpoints
   - **Dependencies**: task_routes.py

3. **File**: `backend/src/api/task_routes.py`
   - **Task**: Protect `/tasks` route and filter by user_id
   - **Explanation**: Ensures each user only accesses their own tasks using JWT claims
   - **Dependencies**: auth.py (for user validation)

### Phase 2: Frontend Authentication Layer
4. **File**: `frontend/app/lib/auth.ts`
   - **Task**: Configure Better Auth with JWT strategy
   - **Explanation**: Sets up frontend authentication with 7-day JWT expiration
   - **Dependencies**: Environment variables for BETTER_AUTH_SECRET

5. **File**: `frontend/app/lib/api/client.ts`
   - **Task**: Create `apiFetch(endpoint, options)` function
   - **Explanation**: Automatically attaches JWT token from Better Auth session to requests
   - **Dependencies**: auth.ts (for session access)

### Phase 3: Integration and Security
6. **Files**: Pages/components in `frontend/app/`
   - **Task**: Update to use `apiFetch` instead of direct API calls
   - **Explanation**: Ensures all frontend requests include proper authentication
   - **Dependencies**: api/client.ts

7. **Environment Variables Configuration**
   - **Task**: Set up BETTER_AUTH_SECRET in both frontend and backend
   - **Explanation**: Shared secret for JWT signing/verification across services
   - **Dependencies**: None

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multi-service architecture | Required for security isolation | Single service would mix authentication and business logic |
| JWT stateless design | Scalability and security requirement | Session-based approach would require server-side storage |
