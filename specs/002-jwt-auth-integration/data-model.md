# Data Model: JWT Authentication Integration

## Entity: User
- **Fields**:
  - id (UUID/String): Unique identifier for the user
  - email (String): User's email address (unique)
  - created_at (DateTime): Timestamp of user creation
  - updated_at (DateTime): Timestamp of last update
- **Relationships**:
  - Has many Tasks (one-to-many)
- **Validation**: Email must be valid format, unique constraint on email

## Entity: Task
- **Fields**:
  - id (UUID/String): Unique identifier for the task
  - title (String): Task title/description
  - completed (Boolean): Whether the task is completed
  - user_id (UUID/String): Foreign key linking to User
  - created_at (DateTime): Timestamp of task creation
  - updated_at (DateTime): Timestamp of last update
- **Relationships**:
  - Belongs to User (many-to-one)
- **Validation**: user_id must reference an existing user, title is required

## JWT Token Claims
- **Fields**:
  - sub (Subject): User identifier (user_id)
  - email (Email): User's email address
  - exp (Expiration): Unix timestamp of token expiration (7 days)
  - iat (Issued At): Unix timestamp of token issuance
- **Validation**: Signature must match BETTER_AUTH_SECRET, expiration must be in the future

## Security Constraints
- All Task queries must be filtered by user_id from authenticated user
- Only tasks belonging to authenticated user can be accessed
- Unauthorized access attempts must return 401 status