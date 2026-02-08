# Data Model: Backend API & Data Layer

**Feature**: Backend API & Data
**Created**: 2026-01-28

## Entity: Task

**Representation**: A user's todo item with unique identifier, title, description, completion status, and ownership reference

**Attributes**:
- `id`: UUID - Unique identifier for the task (primary key)
- `title`: String - The task title (required, minimum length 1)
- `description`: String (optional) - Additional details about the task
- `completed`: Boolean - Whether the task is completed (default: false)
- `user_id`: String - ID of the user who owns this task (foreign key reference)
- `created_at`: DateTime - Timestamp when the task was created
- `updated_at`: DateTime - Timestamp when the task was last updated

**Validation Rules**:
- `title` must be provided (not null, length > 0)
- `user_id` must be a valid user identifier from JWT
- `completed` defaults to false when creating new tasks
- `created_at` is set automatically on creation
- `updated_at` is updated automatically on any modification

**State Transitions**:
- `pending` → `completed` (via completion toggle endpoint)
- `completed` → `pending` (via completion toggle endpoint)

## Entity: TaskList

**Representation**: Collection of tasks belonging to a specific user

**Attributes**:
- `tasks`: Array of Task objects - All tasks belonging to the user
- `user_id`: String - ID of the user whose tasks are in this list
- `total_count`: Integer - Total number of tasks for this user
- `completed_count`: Integer - Number of completed tasks
- `incomplete_count`: Integer - Number of incomplete tasks

**Validation Rules**:
- All tasks in the list must belong to the specified user_id
- Count statistics must match actual task counts
- List should only contain tasks visible to the authenticated user

## Entity: TaskUpdate

**Representation**: Data required to update an existing task

**Attributes**:
- `title`: String (optional) - New title for the task
- `description`: String (optional) - New description for the task
- `completed`: Boolean (optional) - New completion status for the task

**Validation Rules**:
- At least one field must be provided for update
- `title` must not be empty if provided
- User must be the owner of the task being updated

## Entity: TaskCreation

**Representation**: Data required to create a new task

**Attributes**:
- `title`: String (required) - Title for the new task
- `description`: String (optional) - Description for the new task

**Validation Rules**:
- `title` must be provided and not empty
- `description` is optional and can be null
- `completed` defaults to false
- `user_id` is taken from authenticated JWT, not request body

## Entity: TaskToggle

**Representation**: Result of toggling a task's completion status

**Attributes**:
- `task_id`: UUID - ID of the task that was toggled
- `previous_status`: Boolean - Completion status before toggle
- `new_status`: Boolean - Completion status after toggle
- `updated_task`: Task - Full task object with new completion status

**Validation Rules**:
- User must own the task being toggled
- Operation must result in flipped completion status
- Updated task must reflect the new completion status

## Relationships

**User → Task** (One-to-Many):
- One user can have multiple tasks
- Each task belongs to exactly one user via user_id foreign key
- All tasks must be filtered by user_id for security

**TaskList → Task** (One-to-Many):
- One task list contains multiple tasks
- All tasks in the list belong to the same user
- Task lists are dynamically generated based on user_id

## Constraints

**Security Constraints**:
- All queries must filter by user_id to prevent unauthorized access
- No task should be accessible by a user who doesn't own it
- User identity must come from JWT, never from request body

**Data Integrity Constraints**:
- Task title cannot be null or empty
- Task ID must be unique across all tasks
- Timestamps are automatically managed by the system
- Completion status can only be true or false

**Performance Constraints**:
- Queries should leverage indexes on user_id
- Response sizes should be manageable for API consumers
- Filtering should happen at the database level for efficiency