# Implementation Plan: Backend API & Data Layer

**Feature**: Backend API & Data
**Branch**: 1-backend-task-api
**Created**: 2026-01-28
**Status**: Draft

## Technical Context

This plan implements a FastAPI-based backend for managing user tasks with secure, user-scoped access. The solution will integrate with the existing JWT authentication system and use Neon Serverless PostgreSQL with SQLModel for data persistence.

**Architecture**: FastAPI application with SQLModel ORM connecting to Neon PostgreSQL
**Authentication**: JWT token validation using existing auth system from Spec 1
**Data Isolation**: All queries filtered by authenticated user_id from JWT
**Session Model**: Request-scoped database sessions

**Dependencies**:
- FastAPI framework for web application
- SQLModel for ORM and database modeling
- Neon PostgreSQL for data persistence
- python-jose for JWT validation (from existing auth system)
- asyncpg for PostgreSQL async driver

**Integration Points**:
- JWT verification dependency from existing auth system
- Database connection and session management
- Task CRUD endpoints with user-scoping

## Constitution Check

**Spec-driven development with no manual coding**: All implementation will follow this plan without deviation. No manual code edits allowed - all code must be generated via Claude Code.

**Security-first design with multi-user isolation**:
- Mandatory JWT validation on all API routes
- Every request must validate authenticated user context
- Each user can only access their own tasks
- Database queries must always be scoped to the authenticated user
- Unauthorized requests must return 401 status

**Technology stack compliance with Next.js 16+**:
- Backend: Python FastAPI with SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: JWT-based (integrated with existing system)

**Separation of concerns**:
- Backend manages business logic and API endpoints
- Database stores persistent data
- Authentication layer manages user identity
- Each layer has explicit responsibilities and clear interfaces

## Gates

**GATE 1: Technology Alignment** - ✅ Confirmed: Uses specified stack (FastAPI, SQLModel, Neon PostgreSQL)
**GATE 2: Security Compliance** - ✅ Confirmed: JWT-based auth with data isolation
**GATE 3: Specification Coverage** - ✅ Confirmed: All FR requirements addressed
**GATE 4: Constitution Adherence** - ✅ Confirmed: Follows all constitutional principles

---

## Phase 0: Research & Resolution

### R0.1: SQLModel Best Practices Research
**Task**: Research best practices for SQLModel model definitions and relationships
- Decision: Use SQLModel with SQLAlchemy core for database operations
- Rationale: SQLModel provides Pydantic compatibility with SQLAlchemy power
- Alternatives considered: Pure SQLAlchemy vs SQLModel vs Tortoise ORM (SQLModel chosen for Pydantic integration)

### R0.2: FastAPI Dependency Injection Patterns
**Task**: Research FastAPI dependency injection for database sessions and JWT validation
- Decision: Use request-scoped database sessions with Depends for JWT validation
- Rationale: Ensures proper resource cleanup and follows FastAPI best practices
- Alternatives considered: Global session vs request-scoped (request-scoped chosen for safety)

### R0.3: Neon PostgreSQL Connection Management
**Task**: Research best practices for Neon PostgreSQL connection pooling in async FastAPI app
- Decision: Use asyncpg with SQLModel async engine for connection pooling
- Rationale: Optimizes performance and handles connection limits properly
- Alternatives considered: Synchronous vs asynchronous connections (async chosen for FastAPI)

---

## Phase 1: Design & Contracts

### Step 1: Backend Project Initialization
**Objective**: Initialize FastAPI project structure and configuration

1.1. Create project directory structure:
   - `src/` for application source code
   - `src/main.py` for application entry point
   - `src/config/` for configuration management
   - `src/models/` for SQLModel definitions
   - `src/schemas/` for Pydantic schemas
   - `src/api/` for API routes and dependencies
   - `src/database/` for database connection and session management

1.2. Configure application entry point:
   - Initialize FastAPI app with proper settings
   - Configure CORS for frontend integration
   - Set up logging configuration

1.3. Define configuration management strategy:
   - Environment-based configuration
   - Database URL from environment variables
   - JWT secret configuration

### Step 2: Environment & Database Configuration
**Objective**: Configure Neon PostgreSQL connection and SQLModel setup

2.1. Define required environment variables:
   - `DATABASE_URL`: Neon PostgreSQL connection string
   - `BETTER_AUTH_SECRET`: JWT verification secret (from existing auth system)
   - `ENVIRONMENT`: Development/production settings

2.2. Configure Neon PostgreSQL connection:
   - Set up SQLModel async engine with Neon connection string
   - Configure connection pooling parameters
   - Set up proper SSL settings for Neon

2.3. Establish SQLModel engine and session factory:
   - Create async engine with appropriate settings
   - Create session factory with request-scoped sessions
   - Implement proper connection cleanup patterns

### Step 3: Data Modeling with SQLModel
**Objective**: Define Task model schema with user ownership

3.1. Define Task model schema:
   - Properties: id (UUID), title (string, required), description (optional string), completed (boolean), user_id (foreign key), created_at (datetime), updated_at (datetime)
   - Include proper constraints and validations
   - Add appropriate indexing for user_id for performance

3.2. Implement model relationships and constraints:
   - Foreign key relationship to user (referenced by user_id from JWT)
   - Proper timestamp handling with automatic updates
   - Validation for required fields

3.3. Prepare model metadata for database usage:
   - Define table name and schema
   - Set up proper serialization for API responses
   - Include methods for common operations

### Step 4: Dependency & Middleware Setup
**Objective**: Integrate JWT verification and database session dependencies

4.1. Integrate JWT verification dependency from Spec 1:
   - Import existing JWT validation functions
   - Create FastAPI dependency for JWT validation
   - Extract user_id from JWT for authorization

4.2. Create request-scoped database session dependency:
   - Implement session creation and cleanup
   - Ensure proper error handling and rollback
   - Connect session lifecycle to request lifecycle

4.3. Ensure authentication runs before route logic:
   - Configure dependency injection order
   - Validate JWT before database operations
   - Pass user context to route handlers

### Step 5: CRUD Endpoint Implementation
**Objective**: Implement all required task endpoints with proper authorization

5.1. Implement task listing endpoint (user-scoped):
   - GET /api/{user_id}/tasks
   - Validate JWT matches path user_id
   - Query only tasks belonging to authenticated user
   - Return properly formatted response

5.2. Implement task creation endpoint:
   - POST /api/{user_id}/tasks
   - Validate JWT matches path user_id
   - Create task with authenticated user's ID
   - Return created task with 201 status

5.3. Implement task retrieval by ID with ownership validation:
   - GET /api/{user_id}/tasks/{id}
   - Validate JWT matches path user_id
   - Verify task belongs to authenticated user
   - Return task or 404 if not found

5.4. Implement task update endpoint:
   - PUT /api/{user_id}/tasks/{id}
   - Validate JWT matches path user_id
   - Verify task belongs to authenticated user
   - Update task and return updated object

5.5. Implement task deletion endpoint:
   - DELETE /api/{user_id}/tasks/{id}
   - Validate JWT matches path user_id
   - Verify task belongs to authenticated user
   - Delete task and return success response

5.6. Implement task completion toggle endpoint:
   - PATCH /api/{user_id}/tasks/{id}/complete
   - Validate JWT matches path user_id
   - Verify task belongs to authenticated user
   - Toggle completion status and return updated task

### Step 6: Authorization Enforcement
**Objective**: Implement strict user authorization checks

6.1. Validate user identity from JWT on every request:
   - Extract user_id from JWT claims
   - Compare with path parameter user_id
   - Reject mismatched requests with 403 Forbidden

6.2. Reject mismatched user_id path parameters:
   - Ensure JWT user_id matches path user_id
   - Return 403 Forbidden for mismatches
   - Log potential security violations

6.3. Enforce ownership checks at query level:
   - Filter all database queries by user_id
   - Never return tasks that don't belong to user
   - Use consistent query patterns across all endpoints

### Step 7: Error Handling & Response Standards
**Objective**: Implement consistent error responses and status codes

7.1. Standardize HTTP status codes:
   - 200: Successful GET/PUT/PATCH requests
   - 201: Successful POST (creation)
   - 204: Successful DELETE
   - 400: Bad request (validation errors)
   - 401: Unauthorized (invalid/missing JWT)
   - 403: Forbidden (user ID mismatch)
   - 404: Not found (task doesn't exist for user)

7.2. Define consistent error response formats:
   - Standard error response structure
   - Clear, non-leaking error messages
   - Proper JSON formatting for all error responses

7.3. Prevent leakage of internal or sensitive details:
   - Generic error messages for security
   - No database-specific details in responses
   - Proper logging of actual errors server-side

### Step 8: Verification & Validation Steps
**Objective**: Validate complete backend functionality

8.1. Verify authenticated user can create tasks:
   - Test task creation with valid JWT
   - Confirm task is saved with correct user_id
   - Verify response format and status code

8.2. Verify users can only access their own tasks:
   - Test user A cannot access user B's tasks
   - Confirm 403 Forbidden responses for cross-user access
   - Validate internal filtering at database level

8.3. Verify invalid IDs return correct errors:
   - Test with non-existent task IDs
   - Confirm 404 Not Found responses
   - Verify valid format but non-existent IDs

8.4. Verify unauthorized access is blocked:
   - Test endpoints without JWT
   - Confirm 401 Unauthorized responses
   - Test with invalid/expired JWTs

8.5. Verify database persistence across requests:
   - Create task and retrieve in separate requests
   - Confirm data integrity and consistency
   - Test concurrent access patterns

---

## Phase 2: Implementation Preparation

### Step 9: Quickstart Guide Creation
**Objective**: Document how to set up and run the backend

9.1. Create setup instructions:
   - Environment variable configuration
   - Database setup and migration steps
   - Running the FastAPI application

9.2. Document testing procedures:
   - How to test JWT authentication
   - How to verify task CRUD operations
   - How to validate authorization enforcement

### Step 10: API Contract Documentation
**Objective**: Define API contract for frontend integration

10.1. Document all task endpoints with request/response schemas:
   - GET /api/{user_id}/tasks
   - POST /api/{user_id}/tasks
   - GET /api/{user_id}/tasks/{id}
   - PUT /api/{user_id}/tasks/{id}
   - DELETE /api/{user_id}/tasks/{id}
   - PATCH /api/{user_id}/tasks/{id}/complete

10.2. Define error response formats:
   - Standard error structure
   - HTTP status code meanings
   - Common error scenarios and responses

---

## Success Criteria Verification

The implementation will be considered complete when:
- ✅ All 6 required API endpoints function correctly
- ✅ Tasks are persisted in Neon PostgreSQL database
- ✅ Each task is strictly associated with authenticated user from JWT
- ✅ Users can only access their own tasks (100% data isolation)
- ✅ Unauthorized or cross-user access attempts are rejected with proper status codes
- ✅ All endpoints require valid authentication context
- ✅ API responses follow consistent formats and status codes
- ✅ Database sessions are properly scoped to requests
- ✅ All functional requirements (FR-001 through FR-012) are satisfied
- ✅ All success criteria (SC-001 through SC-008) can be met