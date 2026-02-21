export interface Task {
  id: string;
  title: string;
  description: string; // Added description
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskRequest {
  title: string;
  description?: string;
  completed?: boolean;
}

export interface UpdateTaskData {
  title?: string;
  description?: string; // Added optional description
  completed?: boolean;
}

// Backend API response types
export interface TasksResponse {
  tasks: Task[];
}

export interface TaskResponse {
  task: Task;
}