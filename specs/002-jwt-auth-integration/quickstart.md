# Quickstart Guide: JWT Authentication Integration

## Prerequisites
- Node.js 18+ installed
- Python 3.11+ installed
- pnpm installed (or npm/yarn alternative)
- PostgreSQL database (Neon recommended)

## Environment Setup
1. Copy `.env.example` to `.env` in both frontend and backend directories
2. Set `BETTER_AUTH_SECRET` to a secure random string (recommended: 32+ characters)
3. Configure database connection strings

## Backend Setup
1. Navigate to `backend/` directory
2. Install dependencies: `pip install -r requirements.txt`
3. Start the server: `uvicorn src.main:app --reload`
4. Server will run on `http://localhost:8000`

## Frontend Setup
1. Navigate to `frontend/` directory
2. Install dependencies: `pnpm install`
3. Start the development server: `pnpm dev`
4. App will be available at `http://localhost:3000`

## Key Components
- **Frontend Authentication**: Better Auth configured with JWT strategy
- **API Client**: Automatic JWT token attachment in requests
- **Backend Protection**: JWT validation middleware on all routes
- **Data Isolation**: Task filtering by authenticated user

## Testing the Integration
1. Register a new user via the frontend
2. Verify JWT token is stored in session
3. Create tasks and verify they're associated with the correct user
4. Attempt to access other users' tasks (should be blocked)