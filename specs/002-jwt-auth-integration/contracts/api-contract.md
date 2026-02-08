# API Contract: JWT Authentication Integration

## Authentication Endpoints (Handled by Better Auth)
- `POST /api/auth/register` - User registration (frontend only)
- `POST /api/auth/login` - User login (frontend only)
- `GET /api/auth/session` - Get current session (frontend only)

## Protected Task Endpoints
All endpoints below require valid JWT in Authorization header:
- `Authorization: Bearer <jwt-token>`

### GET /api/tasks
**Description**: Retrieve tasks for authenticated user
**Headers**:
- Authorization: Bearer <jwt-token>
**Response**:
- 200: Array of tasks belonging to authenticated user
- 401: Unauthorized if JWT invalid/missing

### POST /api/tasks
**Description**: Create a new task for authenticated user
**Headers**:
- Authorization: Bearer <jwt-token>
**Body**:
```json
{
  "title": "string",
  "completed": "boolean"
}
```
**Response**:
- 201: Created task with user_id set to authenticated user
- 401: Unauthorized if JWT invalid/missing

### PUT /api/tasks/{task_id}
**Description**: Update a task owned by authenticated user
**Headers**:
- Authorization: Bearer <jwt-token>
**Parameters**:
- task_id: ID of the task to update
**Body**:
```json
{
  "title": "string",
  "completed": "boolean"
}
```
**Response**:
- 200: Updated task
- 401: Unauthorized if JWT invalid/missing
- 404: Task not found or not owned by user

### DELETE /api/tasks/{task_id}
**Description**: Delete a task owned by authenticated user
**Headers**:
- Authorization: Bearer <jwt-token>
**Parameters**:
- task_id: ID of the task to delete
**Response**:
- 204: Successfully deleted
- 401: Unauthorized if JWT invalid/missing
- 404: Task not found or not owned by user

## Error Responses
All error responses follow the format:
```json
{
  "detail": "Error message"
}
```

## JWT Claims Format
Valid JWT tokens contain:
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "exp": 1234567890,
  "iat": 1234567890
}
```