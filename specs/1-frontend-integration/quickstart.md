# Quickstart Guide: Frontend Application & Integration

**Feature**: Frontend Application & Integration
**Created**: 2026-01-28

## Prerequisites

- Node.js 18+ for frontend development
- Next.js 16+ with App Router
- Tailwind CSS configured
- Access to backend API (from Spec 1-backend-task-api)
- Better Auth configured (from Spec 1-auth-jwt-authentication)

## Environment Setup

### 1. Environment Variables

Create a `.env.local` file in the frontend root directory:

```bash
# Authentication Configuration
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random

# Backend API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# Environment (development/production)
NODE_ENV=development
```

**Important**: The `BETTER_AUTH_SECRET` must match the one used in the backend authentication system for JWT validation to work properly.

### 2. Installation

```bash
cd frontend
npm install
npm install better-auth @better-auth/client
```

Additional dependencies for API client and styling:
```bash
npm install axios
# Tailwind CSS should already be configured
```

## Running the Application

### 1. Start Frontend Development Server
```bash
cd frontend
npm run dev
```

The frontend will be available at: http://localhost:3000

## Testing the Application

### 1. Authentication Flow Testing
1. Navigate to the home page (should redirect to sign-in if not authenticated)
2. Click "Sign Up" to create a new account
3. Verify registration form works with email and password
4. After registration, verify automatic redirect to task dashboard
5. Test sign-in with existing credentials
6. Test sign-out functionality

### 2. Task Management Testing
1. With an authenticated user, navigate to the task dashboard
2. Create a new task with title and optional description
3. Verify the new task appears in the task list
4. Mark a task as complete/incomplete and verify immediate UI feedback
5. Update an existing task's details
6. Delete a task and verify it's removed from the list

### 3. API Integration Testing
1. Verify all API requests include JWT tokens in Authorization headers
2. Test error handling when API endpoints return 401/403/404
3. Verify loading states appear during API operations
4. Test network error handling

### 4. Security Testing
1. Try to access task pages without authentication (should redirect to sign-in)
2. Verify users only see their own tasks
3. Test token expiration handling (should redirect to login)
4. Verify cross-user data isolation

## Verification Steps

### 1. Authentication Verification
- [ ] Users can register with email and password
- [ ] Users can sign in with existing credentials
- [ ] JWT tokens are properly stored and attached to API requests
- [ ] Unauthenticated users are redirected to sign-in page
- [ ] Sign-out functionality works correctly

### 2. Task Management Verification
- [ ] Users can create new tasks with title and description
- [ ] Task list displays all user-specific tasks
- [ ] Users can update task details
- [ ] Users can delete tasks from their list
- [ ] Task completion toggle works with immediate feedback

### 3. API Integration Verification
- [ ] All API requests include valid JWT tokens
- [ ] Loading states appear during API operations
- [ ] Error messages are displayed appropriately
- [ ] Success notifications appear after operations
- [ ] Data is properly synchronized between UI and backend

### 4. UI/UX Verification
- [ ] Interface is responsive on mobile, tablet, and desktop
- [ ] Consistent colors, typography, and spacing
- [ ] Clear call-to-action buttons for task operations
- [ ] Loading indicators for API requests
- [ ] Error messages displayed inline and contextually

## Troubleshooting

### Common Issues

**Issue**: 401 Unauthorized responses on API calls
**Solution**: Verify that the BETTER_AUTH_SECRET matches between frontend and backend, and that JWT tokens are being properly attached to requests

**Issue**: Users seeing other users' tasks
**Solution**: Verify that API calls include proper user_id validation and backend is filtering by authenticated user_id

**Issue**: Authentication state not persisting
**Solution**: Check Better Auth configuration and token storage settings

**Issue**: API calls failing with CORS errors
**Solution**: Verify backend CORS settings allow requests from frontend origin

## Security Notes

- Never log JWT tokens in plain text
- Use HTTPS in production to protect tokens in transit
- Store tokens securely using Better Auth's recommended storage methods
- Regularly rotate the BETTER_AUTH_SECRET in production
- Monitor authentication failure logs for potential attacks
- All API requests must be properly authenticated with valid JWT tokens