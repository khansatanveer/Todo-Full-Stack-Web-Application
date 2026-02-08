# Backend API & Data Quickstart Guide

**Feature**: Backend API & Data Layer
**Created**: 2026-01-28

## Overview

This guide provides instructions for setting up, running, and testing the Backend API & Data Layer for the Todo application with JWT authentication and user-scoped task management.

## Prerequisites

- Node.js 18+ for frontend (with npm)
- Python 3.9+ for backend
- PostgreSQL-compatible database (Neon Serverless PostgreSQL recommended)
- Better Auth configured for JWT generation (from Spec 1-auth-jwt-authentication)

## Environment Setup

### 1. Clone and Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Environment Configuration
Create a `.env` file in the backend root with the following:

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db

# JWT Secret (must match frontend and auth system)
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random

# Environment
ENVIRONMENT=development
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Backend Server

### 1. Start the Backend Server
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

The backend will be available at: `http://localhost:8000`

### 2. Verify Backend is Running
```bash
curl http://localhost:8000/health
```
Expected response: `{"status": "healthy"}`

## API Testing Procedures

### 1. Test Authentication-Required Endpoints
All API endpoints require a valid JWT token in the Authorization header:

```bash
# Get user tasks (will return 401 without valid token)
curl -H "Authorization: Bearer YOUR_VALID_JWT_TOKEN" \
     http://localhost:8000/api/user123/tasks

# Create a task (will return 401 without valid token)
curl -X POST \
     -H "Authorization: Bearer YOUR_VALID_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title":"Test task","description":"A test task"}' \
     http://localhost:8000/api/user123/tasks
```

### 2. Test User-Specific Data Access
- Verify that user A cannot access user B's tasks
- Use JWT with user A's ID to try accessing user B's tasks (should return 403)
- Verify that users can only access tasks with matching user_id

### 3. Test Task CRUD Operations
With a valid JWT token:

1. **Create**: POST to `/api/{user_id}/tasks` with task data
2. **Read**: GET from `/api/{user_id}/tasks` or `/api/{user_id}/tasks/{id}`
3. **Update**: PUT to `/api/{user_id}/tasks/{id}` with updated data
4. **Delete**: DELETE to `/api/{user_id}/tasks/{id}`
5. **Toggle Completion**: PATCH to `/api/{user_id}/tasks/{id}/complete`

## Verification Steps

### 1. Functional Verification
- [ ] All 6 required API endpoints respond correctly (200/201/204/401/403/404)
- [ ] JWT tokens are properly validated on all endpoints
- [ ] Users only see their own tasks (data isolation enforced)
- [ ] Task CRUD operations work correctly
- [ ] Task completion toggle works properly

### 2. Security Verification
- [ ] Unauthorized requests return 401 status
- [ ] Cross-user access attempts return 403 status
- [ ] Invalid JWT tokens are properly rejected
- [ ] Non-existent tasks return 404 status

### 3. Integration Verification
- [ ] Backend connects to Neon PostgreSQL database
- [ ] Tasks are persisted across requests
- [ ] API responses follow consistent format
- [ ] Error responses don't leak sensitive information

## Troubleshooting

### Common Issues

**Issue**: 401 Unauthorized responses on all requests
**Solution**: Verify that BETTER_AUTH_SECRET matches between auth system and backend, and that JWT tokens are properly formatted

**Issue**: 403 Forbidden responses when accessing own tasks
**Solution**: Verify that JWT user_id matches the user_id in the request path

**Issue**: Database connection errors
**Solution**: Verify DATABASE_URL is correctly configured and database is accessible

**Issue**: CORS errors during frontend integration
**Solution**: Check CORS configuration in backend and ensure frontend origin is allowed