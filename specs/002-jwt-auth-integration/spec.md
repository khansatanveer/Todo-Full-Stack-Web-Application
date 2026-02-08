# Feature Specification: JWT Authentication Integration

**Feature Branch**: `002-jwt-auth-integration`
**Created**: 2026-02-03
**Status**: Draft
**Input**: User description: "Hackathon: Todo Full-Stack Web App – JWT Auth Integration

Objective:
Transform an existing Next.js (App Router) + FastAPI Todo application into a fully JWT-authenticated multi-user web app using Better Auth for frontend authentication and FastAPI for backend JWT verification. Ensure each user sees only their own tasks. Do not create Better Auth backend; the backend must verify JWT from frontend only.

Requirements:

1️⃣ Frontend (Next.js 13+, App Router / TypeScript):
- File: frontend/app/lib/auth.ts
  - Configure Better Auth with:
    - Email/password login enabled
    - JWT session strategy, 7-day expiry
    - Use BETTER_AUTH_SECRET from environment
- File: frontend/app/lib/api/client.ts
  - Create `apiFetch(endpoint, options)` function
  - Automatically attach JWT token from Better Auth session in Authorization header
  - Base URL: http://localhost:8000/api
- Update pages/components in `app/` to call API via `apiFetch`
- Remove any attempt to call `/api/auth/sign-up/email` or `/api/auth/session` on backend

2️⃣ Backend (FastAPI / Python):
- File: backend/src/core/auth.py
  - Create `get_current_user(request: Request)` function
  - Extract Bearer token from Authorization header
  - Verify JWT signature with BETTER_AUTH_SECRET
  - Return payload (user_id, email, etc.)
- File: backend/src/api/task_routes.py
  - Protect `/tasks` route
  - Filter tasks so that only tasks belonging to the authenticated user are returned
- Include router in backend/src/main.py with prefix `/api`
- Ensure all database operations use `Depends(get_current_user)` to identify current user
- Return 401 Unauthorized if JWT missing or invalid

3️⃣ Database:
- SQLModel tables: User, Task
- Each Task must store `user_id` to relate to creator
- Queries must filter by `user_id` from JWT

4️⃣ Security / Hackathon requirements:
- Shared secret `BETTER_AUTH_SECRET` used in frontend and backend
- Backend is stateless; no sessions stored
- User isolation enforced: users cannot see or modify other users' tasks
- JWT expiry respected (7 days)

5️⃣ Folder structure (App Router version):
frontend/
└── app/
├── lib/auth.ts
└── lib/api/client.ts
backend/
└── src/
├── core/auth.py
├── api/task_routes.py
└── main.py
6️⃣ Output:
- Provide full code for each file listed
- Ensure backend routes are fully JWT-protected
- Ensure frontend automatically attaches token to requests
- Maintain existing task CRUD routes, now JWT-protected
- Include comments explaining key lines
- Ready to copy-paste and run locally

Goal:
After implementation, a user can:
- Sign up / login on frontend (Better Auth)
- JWT issued
- Make API calls to FastAPI backend
- See only their own tasks
- Receive 401 if token missing or invalid"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Secure User Registration and Login (Priority: P1)

A user can register for an account using their email and password, and subsequently log in to access their personalized todo list. The authentication process uses JWT tokens to securely identify the user across frontend and backend services.

**Why this priority**: This is the foundational capability that enables all other functionality. Without secure authentication, users cannot access personalized data or maintain privacy.

**Independent Test**: Can be fully tested by registering a new user, logging in, and verifying that a valid JWT token is received and stored in the frontend session.

**Acceptance Scenarios**:

1. **Given** user is on the registration page, **When** user enters valid email and password and submits, **Then** user account is created and user is logged in with JWT token
2. **Given** user has an existing account, **When** user enters correct email and password and logs in, **Then** user receives valid JWT token and can access protected resources

---

### User Story 2 - Personalized Task Access (Priority: P1)

An authenticated user can only view, create, update, and delete their own tasks. The system enforces user isolation by filtering tasks based on the authenticated user's identity from the JWT token.

**Why this priority**: Critical for data privacy and security. Users must be assured that their personal tasks remain private and inaccessible to others.

**Independent Test**: Can be fully tested by having multiple users create tasks and verifying that each user only sees their own tasks when accessing the task list endpoint.

**Acceptance Scenarios**:

1. **Given** user is authenticated with valid JWT, **When** user creates a new task, **Then** task is associated with the authenticated user and stored with user ID
2. **Given** multiple users have tasks in the system, **When** user requests their task list, **Then** only tasks belonging to the authenticated user are returned

---

### User Story 3 - Secure API Access (Priority: P2)

When making API requests, the frontend automatically includes the user's JWT token in the Authorization header. Unauthenticated users receive 401 Unauthorized responses when attempting to access protected endpoints.

**Why this priority**: Essential for maintaining security boundaries and preventing unauthorized access to user data.

**Independent Test**: Can be fully tested by making API calls with and without valid JWT tokens and verifying appropriate responses.

**Acceptance Scenarios**:

1. **Given** user is authenticated, **When** user makes API request through frontend, **Then** JWT token is automatically attached to the request header
2. **Given** user makes request without valid JWT, **When** request hits protected endpoint, **Then** server returns 401 Unauthorized response

---

### Edge Cases

- What happens when JWT token expires after 7 days?
- How does system handle malformed or tampered JWT tokens?
- What occurs when the shared BETTER_AUTH_SECRET is changed?
- How does the system behave when multiple sessions exist for the same user?
- What happens if the backend cannot verify the JWT signature?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to register with email and password via Better Auth frontend authentication
- **FR-002**: System MUST issue JWT tokens with 7-day expiration upon successful authentication
- **FR-003**: System MUST verify JWT tokens on backend using shared BETTER_AUTH_SECRET
- **FR-004**: System MUST associate each task with the authenticated user who created it
- **FR-005**: System MUST filter task lists to only show tasks belonging to the authenticated user
- **FR-006**: System MUST reject API requests without valid JWT tokens with 401 Unauthorized response
- **FR-007**: System MUST automatically attach JWT token to all frontend API requests
- **FR-008**: System MUST maintain stateless authentication with no server-side session storage
- **FR-009**: System MUST enforce user isolation so users cannot access other users' tasks
- **FR-010**: System MUST validate JWT signature integrity before granting access

### Key Entities

- **User**: Represents a registered user with email, authentication credentials, and unique identifier
- **Task**: Represents a todo item that belongs to a specific user, containing title, description, completion status, and creation timestamp
- **JWT Token**: Cryptographically signed authentication token containing user identity and expiration information

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully register and log in with email/password authentication in under 30 seconds
- **SC-002**: Authenticated users can only access their own tasks with 100% data isolation accuracy
- **SC-003**: API requests automatically include JWT tokens with 99% success rate (failures only on expired/invalid tokens)
- **SC-004**: Unauthorized access attempts are rejected with 401 responses within 500ms response time
- **SC-005**: JWT token verification succeeds for valid tokens and fails appropriately for invalid/expired tokens
