# Data Model: JWT Authentication & Authorization

**Feature**: Authentication & Authorization
**Created**: 2026-01-28

## Entity: User

**Representation**: Authenticated user with unique identifier and authentication status

**Attributes**:
- `id`: String - Unique user identifier (UUID format)
- `email`: String - User's email address (unique, validated)
- `createdAt`: DateTime - Account creation timestamp
- `updatedAt`: DateTime - Last account update timestamp

**Validation Rules**:
- Email must be properly formatted (RFC 5322)
- Email must be unique across all users
- ID must be a valid UUID format
- Email cannot be changed after account creation

**State Transitions**:
- `unregistered` → `registered` (via registration)
- `registered` → `authenticated` (via login)
- `authenticated` → `unauthenticated` (via logout)

## Entity: JWT Token

**Representation**: Secure token containing user identity and validity period, signed with shared secret

**Structure**:
- `header`: Object - Token header with algorithm information
  - `alg`: String - Signing algorithm (HS256)
  - `typ`: String - Token type (JWT)
- `payload`: Object - Token claims
  - `sub`: String - Subject (user ID)
  - `user_id`: String - User identifier (duplicate for clarity)
  - `email`: String - User email (optional)
  - `exp`: Integer - Expiration timestamp (Unix epoch)
  - `iat`: Integer - Issued at timestamp (Unix epoch)
  - `jti`: String - JWT ID (optional, for tracking)
- `signature`: String - Signature computed over header and payload

**Validation Rules**:
- Token must be properly formatted JWT
- Signature must be valid using BETTER_AUTH_SECRET
- Current time must be before expiration (exp)
- All required claims must be present
- User referenced by token must exist in system

## Entity: Authenticated Request

**Representation**: API request containing valid JWT in Authorization header for verification

**Attributes**:
- `method`: String - HTTP method (GET, POST, PUT, DELETE)
- `path`: String - Requested resource path
- `headers`: Object - HTTP headers including Authorization
  - `Authorization`: String - Bearer token format ("Bearer {jwt}")
- `user_context`: Object - Extracted user information from JWT
  - `user_id`: String - Verified user identifier
  - `email`: String - User email (from token)
  - `valid`: Boolean - Whether token is currently valid
  - `expired`: Boolean - Whether token has expired

**Validation Rules**:
- Authorization header must be present for protected endpoints
- Token must be in "Bearer {jwt}" format
- JWT must be properly signed and not expired
- User context must be successfully extracted
- Requested resource must belong to authenticated user (for user-specific data)

## Entity: Authentication Session

**Representation**: Temporary association between user and active authentication state

**Attributes**:
- `user_id`: String - Associated user identifier
- `created_at`: DateTime - Session creation time
- `expires_at`: DateTime - Session expiration time
- `active`: Boolean - Whether session is currently active
- `token_used`: String - Last token used in this session context

**Validation Rules**:
- Session must correspond to valid user
- Session must not be expired
- Session must be marked inactive after logout
- Session state must be stateless (no server-side storage required)

## Relationships

**User → JWT Token** (One-to-Many):
- A user can have multiple valid JWT tokens simultaneously
- Each token is associated with exactly one user via user_id claim

**JWT Token → Authenticated Request** (One-to-Many):
- A JWT token can be used in multiple requests
- Each authenticated request uses exactly one JWT token

**User → Authenticated Request** (One-to-Many):
- A user can make multiple authenticated requests
- Each request is associated with exactly one user via JWT token