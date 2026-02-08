# Quickstart Guide: JWT Authentication & Authorization

**Feature**: Authentication & Authorization
**Created**: 2026-01-28

## Prerequisites

- Node.js 18+ for frontend
- Python 3.9+ for backend
- Environment variables configured (see below)

## Environment Setup

### 1. Environment Variables

Create `.env` files in both frontend and backend:

**Frontend (.env.local):**
```
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
```

**Backend (.env):**
```
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
DATABASE_URL=your-database-url-here
```

⚠️ **Important**: The `BETTER_AUTH_SECRET` must be identical in both frontend and backend for JWT validation to work.

### 2. Installation

**Frontend Setup:**
```bash
cd frontend
npm install
npm install better-auth @better-auth/client
```

**Backend Setup:**
```bash
cd backend
pip install fastapi uvicorn python-jose[cryptography] python-multipart
```

## Running the Application

### 1. Start Backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 2. Start Frontend
```bash
cd frontend
npm run dev
```

Both services will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000 (API endpoints)

## Testing Authentication Flow

### 1. User Registration
Make a POST request to register a new user:

```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"securePassword123"}'
```

Expected response:
```json
{
  "success": true,
  "user": {
    "id": "user-uuid-string",
    "email": "test@example.com",
    "createdAt": "2026-01-28T12:00:00.000Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 2. User Login
Authenticate with existing credentials:

```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"securePassword123"}'
```

### 3. Making Authenticated Requests
Use the JWT token to access protected endpoints:

```bash
curl -X GET http://localhost:8000/api/protected-data \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 4. Testing Unauthorized Access
Try accessing protected endpoints without a token:

```bash
curl -X GET http://localhost:8000/api/protected-data
# Should return 401 Unauthorized
```

## Verification Steps

### 1. Verify JWT Issuance
- Register a new user
- Confirm JWT token is returned in the response
- Decode the token to verify standard claims (sub, exp, iat)

### 2. Verify Token Validation
- Make requests to protected endpoints with valid token
- Confirm requests succeed
- Make requests with invalid/malformed tokens
- Confirm requests return 401 Unauthorized

### 3. Verify User Data Isolation
- Register two different users
- Create resources for each user
- Attempt to access User A's resources with User B's token
- Confirm access is denied (403 Forbidden)

### 4. Verify Logout
- Log in as a user and obtain token
- Make authenticated requests to verify token works
- Call logout endpoint
- Attempt to use the same token again
- Confirm subsequent requests fail with 401

## Troubleshooting

### Common Issues

**Issue**: JWT validation fails between frontend and backend
**Solution**: Verify that `BETTER_AUTH_SECRET` is identical in both environments

**Issue**: 401 Unauthorized responses on valid tokens
**Solution**: Check that JWT is properly formatted as "Bearer {token}" in Authorization header

**Issue**: Token expires too quickly
**Solution**: Adjust token expiration time in Better Auth configuration

**Issue**: CORS errors between frontend and backend
**Solution**: Ensure proper CORS configuration in FastAPI backend

## Security Notes

- Never log JWT tokens in plain text
- Use HTTPS in production to protect tokens in transit
- Store tokens securely in browser (preferably in HTTP-only cookies)
- Regularly rotate the BETTER_AUTH_SECRET in production
- Monitor authentication failure logs for potential attacks