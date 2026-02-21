'use client';

import { Task } from '../../types/task';
import TaskItem from './TaskItem';

interface TaskListProps {
  tasks: Task[];
  onTaskUpdated: (updatedTask: Task) => void;
  onTaskDeleted: (taskId: string) => void;
  onToggleComplete: (taskId: string) => void;
  userId: string;
}

export default function TaskList({
  tasks,
  onTaskUpdated,
  onTaskDeleted,
  onToggleComplete,
  userId
}: TaskListProps) {
  const completedTasks = tasks.filter(task => task.completed);
  const incompleteTasks = tasks.filter(task => !task.completed);

  return (
    <div className="bg-white shadow overflow-hidden sm:rounded-md">
      <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
        <h3 className="text-lg leading-6 font-medium text-gray-900">
          Your Tasks
        </h3>
        <p className="mt-1 max-w-2xl text-sm text-gray-500">
          {tasks.length} total tasks ({incompleteTasks.length} incomplete, {completedTasks.length} completed)
        </p>
      </div>

      <ul className="divide-y divide-gray-200">
        {tasks.length === 0 ? (
          <li className="px-4 py-8 text-center sm:px-6">
            <p className="text-sm text-gray-500">
              No tasks yet. Create your first task to get started!
            </p>
          </li>
        ) : (
          <>
            {/* Incomplete tasks first */}
            {incompleteTasks.map((task) => (
              <li key={task.id}>
                <TaskItem
                  task={task}
                  onTaskUpdated={onTaskUpdated}
                  onTaskDeleted={onTaskDeleted}
                  onToggleComplete={onToggleComplete}
                  userId={userId}
                />
              </li>
            ))}

            {/* Completed tasks */}
            {completedTasks.length > 0 && (
              <>
                <li className="px-4 py-3 sm:px-6 bg-gray-50">
                  <h4 className="text-sm font-medium text-gray-700">Completed Tasks</h4>
                </li>
                {completedTasks.map((task) => (
                  <li key={task.id}>
                    <TaskItem
                      task={task}
                      onTaskUpdated={onTaskUpdated}
                      onTaskDeleted={onTaskDeleted}
                      onToggleComplete={onToggleComplete}
                      userId={userId}
                    />
                  </li>
                ))}
              </>
            )}
          </>
        )}
      </ul>
    </div>
  );
}