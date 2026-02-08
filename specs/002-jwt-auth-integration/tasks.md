# Implementation Tasks: JWT Authentication Integration

**Feature**: JWT Authentication Integration
**Branch**: 002-jwt-auth-integration
**Generated from**: spec.md, plan.md, data-model.md, contracts/api-contract.md

## Implementation Strategy

**MVP Approach**: Focus on User Story 1 (Secure User Registration and Login) first to establish the authentication foundation, then implement User Story 2 (Personalized Task Access) for core functionality, and finally User Story 3 (Secure API Access) for complete security implementation.

**Incremental Delivery**: Each user story builds upon the previous to ensure a working system at every stage.

## Dependencies

- **User Story 2** depends on **User Story 1** (authentication must work before protecting tasks)
- **User Story 3** depends on **User Story 1** and **User Story 2** (secure API access requires both auth and protected endpoints)

## Parallel Execution Examples

Each user story can be developed in parallel by different team members:
- **Team Member A**: Work on frontend auth components (auth.ts, client.ts)
- **Team Member B**: Work on backend auth middleware (auth.py) and task routes
- **Team Member C**: Work on database models and integration

---

## Phase 1: Setup

- [x] T001 Create backend directory structure: backend/src/core/, backend/src/api/
- [x] T002 Create frontend directory structure: frontend/app/lib/, frontend/app/lib/api/
- [x] T003 Set up environment variables for BETTER_AUTH_SECRET in both frontend and backend
- [x] T004 Install required dependencies: Better Auth, FastAPI, SQLModel

## Phase 2: Foundational Tasks

- [x] T010 [P] Create User SQLModel in backend/src/models/user.py with id, email, timestamps
- [x] T011 [P] Create Task SQLModel in backend/src/models/task.py with id, title, completed, user_id, timestamps
- [x] T012 [P] Update existing task routes to include user_id foreign key relationship
- [x] T013 Configure database connection in backend to support user_id filtering

## Phase 3: User Story 1 - Secure User Registration and Login (Priority: P1)

**Goal**: Enable users to register and login with email/password, receiving JWT tokens for authentication.

**Independent Test**: Register a new user, login, and verify that a valid JWT token is received and stored in the frontend session.

- [x] T020 [P] [US1] Configure Better Auth in frontend/app/lib/auth.ts with JWT strategy and 7-day expiry
- [x] T021 [P] [US1] Create apiFetch function in frontend/app/lib/api/client.ts to attach JWT tokens
- [x] T022 [US1] Create get_current_user function in backend/src/core/auth.py to verify JWT tokens
- [x] T023 [US1] Implement JWT verification middleware using BETTER_AUTH_SECRET
- [ ] T024 [US1] Test user registration flow with JWT token issuance
- [ ] T025 [US1] Test user login flow with JWT token retrieval

## Phase 4: User Story 2 - Personalized Task Access (Priority: P1)

**Goal**: Allow authenticated users to create, view, update, and delete only their own tasks.

**Independent Test**: Multiple users create tasks and verify that each user only sees their own tasks when accessing the task list endpoint.

- [x] T030 [P] [US2] Update GET /api/tasks endpoint to filter by authenticated user's ID from JWT
- [x] T031 [P] [US2] Update POST /api/tasks endpoint to assign user_id from JWT to new tasks
- [x] T032 [US2] Update PUT /api/tasks/{task_id} to verify task ownership before updates
- [x] T033 [US2] Update DELETE /api/tasks/{task_id} to verify task ownership before deletion
- [x] T034 [US2] Add user_id validation to all task database queries
- [x] T035 [US2] Test multi-user task isolation to ensure data privacy

## Phase 5: User Story 3 - Secure API Access (Priority: P2)

**Goal**: Ensure all API requests include valid JWT tokens and unauthorized requests return 401 responses.

**Independent Test**: Make API calls with and without valid JWT tokens and verify appropriate responses.

- [x] T040 [P] [US3] Apply JWT authentication dependency to all task routes in backend/src/api/task_routes.py
- [x] T041 [P] [US3] Ensure apiFetch in frontend automatically attaches JWT token to requests
- [x] T042 [US3] Update frontend components to use apiFetch instead of direct API calls
- [x] T043 [US3] Test unauthorized access attempts return 401 responses
- [x] T044 [US3] Verify JWT token expiration handling in both frontend and backend
- [x] T045 [US3] Test malformed JWT token rejection

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T050 Add comprehensive error handling for JWT validation failures
- [x] T051 Implement proper error messages for authentication failures
- [x] T052 Add logging for authentication events and security monitoring
- [x] T053 Update documentation with JWT authentication flow
- [x] T054 Test complete user flow: registration -> login -> task operations -> logout
- [x] T055 Verify all security requirements from specification are met

---

## Task Validation Checklist

Each task must satisfy:
- [ ] Follows the required format: `- [ ] T### [P?] [Story?] Description with file path`
- [ ] Has clear file path in description
- [ ] Includes proper story labeling for user story tasks
- [ ] Parallelizable tasks marked with [P]
- [ ] Sequential dependencies properly ordered
- [ ] Independent test criteria defined for each user story