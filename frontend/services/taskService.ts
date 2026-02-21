import { Task, CreateTaskData, UpdateTaskData, TasksResponse, TaskResponse } from '@/types/task';

const API_BASE_URL = 'http://localhost:8000/api';

// Helper function to get the authorization header
// Better Auth uses cookies for authentication, so we don't need to manually include the token
const getAuthHeaders = (): HeadersInit => {
  return {
    'Content-Type': 'application/json',
  };
};

// Helper function to handle API responses
const handleResponse = async (response: Response): Promise<any> => {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
  }
  return response.json();
};

const TaskService = {
  // Get all tasks for the authenticated user
  async getUserTasks(): Promise<TasksResponse> { // Changed return type
    const response = await fetch(`${API_BASE_URL}/tasks`, {
      method: 'GET',
      headers: getAuthHeaders(),
      credentials: 'include', // Include cookies for authentication
    });

    return handleResponse(response);
  },

  // Create a new task
  async createTask(data: CreateTaskData): Promise<TaskResponse> { // Changed return type
    const response = await fetch(`${API_BASE_URL}/tasks`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
      credentials: 'include', // Include cookies for authentication
    });

    return handleResponse(response);
  },

  // Update a task
  async updateTask(id: string, data: UpdateTaskData): Promise<TaskResponse> { // Changed return type
    const response = await fetch(`${API_BASE_URL}/tasks/${id}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
      credentials: 'include', // Include cookies for authentication
    });

    return handleResponse(response);
  },

  // Delete a task
  async deleteTask(id: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/tasks/${id}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
      credentials: 'include', // Include cookies for authentication
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }
  },

  // Toggle task completion status
  async toggleTaskCompletion(id: string): Promise<TaskResponse> { // Changed return type
    const response = await fetch(`${API_BASE_URL}/tasks/${id}/toggle`, {
      method: 'PATCH',
      headers: getAuthHeaders(),
      credentials: 'include', // Include cookies for authentication
    });

    return handleResponse(response);
  },
};

export default TaskService;