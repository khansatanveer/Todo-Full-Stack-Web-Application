# Research Document: JWT Authentication & Authorization

**Feature**: Authentication & Authorization
**Created**: 2026-01-28

## JWT Token Structure Research

**Decision**: Use standard JWT claims with custom user_id claim
- Standard claims: `sub` (subject/user ID), `exp` (expiration), `iat` (issued at)
- Custom claim: `user_id` for authorization checks
- Algorithm: HS256 (HMAC SHA-256) for symmetric signing

**Rationale**: Standard claims ensure compatibility with JWT libraries and best practices. The `user_id` claim enables backend authorization checks to verify users can only access their own data.

**Alternatives considered**:
- Custom token format: Less secure, not interoperable
- Different algorithms (RS256, etc.): More complex, unnecessary for this use case

## Better Auth JWT Plugin Configuration

**Decision**: Configure Better Auth with JWT plugin using shared BETTER_AUTH_SECRET
- Enable JWT plugin in auth configuration
- Use HS256 algorithm with BETTER_AUTH_SECRET
- Set token expiration to 1 hour (configurable)

**Rationale**: Better Auth provides a well-tested, secure JWT implementation that integrates well with Next.js. The JWT plugin handles token signing and verification properly.

**Alternatives considered**:
- Custom JWT implementation: Higher risk of security flaws
- Other auth libraries: Better Auth specifically designed for Next.js with JWT support

## FastAPI JWT Validation Patterns

**Decision**: Implement JWT dependency using Python's `python-jose` library
- Create FastAPI dependency for JWT validation
- Extract user_id from token for authorization checks
- Return 401 for invalid/missing tokens

**Rationale**: FastAPI dependencies provide clean integration with request processing and allow reusable validation logic across endpoints.

**Alternatives considered**:
- Middleware approach: Less flexible, harder to customize per endpoint
- Manual validation in each route: Repetitive, error-prone

## Environment Variable Management

**Decision**: Use BETTER_AUTH_SECRET consistently across frontend and backend
- Same secret used for JWT signing and verification
- Environment variable configuration documented in .env.example
- Secure handling of secrets in both environments

**Rationale**: Ensures JWTs issued by Better Auth can be validated by FastAPI backend. Consistent secret management is essential for JWT validation.

**Alternatives considered**:
- Different secrets: Would break JWT validation
- Hardcoded secrets: Security vulnerability

## Authentication Flow Best Practices

**Decision**: Implement standard authentication flow with proper session management
- Registration → Login → Token issuance → API access
- Secure token storage in browser (HTTP-only cookies or secure localStorage)
- Proper logout to clear tokens

**Rationale**: Standard flow ensures compatibility with user expectations and security best practices.

**Alternatives considered**:
- Custom authentication flows: May introduce security vulnerabilities
- Different token storage mechanisms: Could expose tokens to XSS attacks

## Error Handling Strategies

**Decision**: Consistent 401 responses with minimal information leakage
- Standard error format: `{error: "Unauthorized", message: "Invalid or expired token"}`
- No detailed information about why token is invalid
- Proper logging on server-side without exposing details to clients

**Rationale**: Prevents information leakage that could aid attackers while providing clear feedback to legitimate users.

**Alternatives considered**:
- Detailed error messages: Could reveal system details to attackers
- Different error codes: Would complicate client handling