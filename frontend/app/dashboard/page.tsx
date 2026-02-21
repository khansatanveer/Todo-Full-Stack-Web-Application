'use client';

import React, { useState, useEffect } from 'react';
import { getSession } from '@/lib/auth';
import { Task } from '@/types/task';
import TaskService from '@/services/taskService';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger
} from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import LogoutButton from '@/components/auth/LogoutButton';
import { useRouter } from 'next/navigation';

type TodoFilter = 'all' | 'active' | 'completed';

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');
  const [filter, setFilter] = useState<TodoFilter>('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [user, setUser] = useState<any>(null);

const router = useRouter();
  // Get user from session
useEffect(() => {
  const loadSessionAndTasks = async () => {
    setLoading(true);
    try {
      const session = await getSession();

      if (!session?.user) {
        router.replace('/auth/login'); 
        return;
      }

        setUser(session.user);

        const response = await TaskService.getUserTasks();
        setTasks(response.tasks || []);
    } catch (err) {
      console.error(err);
      setError('Failed to load session or tasks');
      router.replace('/auth/login');
    } finally {
      setLoading(false);
    }
  };

  loadSessionAndTasks();
}, [router]);

  const filteredTasks = tasks.filter(task => {
    if (filter === 'active') return !task.completed;
    if (filter === 'completed') return task.completed;
    return true;
  });

  const completedCount = tasks.filter(task => task.completed).length;
  const activeCount = tasks.length - completedCount;

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!newTaskTitle.trim() || !user?.id) return;

    try {
      const response = await TaskService.createTask({
        title: newTaskTitle,
        description: newTaskDescription, // Pass description
        completed: false
      });

      setTasks([response.task, ...tasks]); // Extract task from response
      setNewTaskTitle('');
      setNewTaskDescription('');
    } catch (err) {
      setError('Failed to add task');
      console.error(err);
    }
  };

  const handleToggleComplete = async (task: Task) => {
    if (!user?.id) return;

    try {
      const response = await TaskService.toggleTaskCompletion(task.id);
      setTasks(tasks.map(t => t.id === task.id ? response.task : t)); // Extract task from response
    } catch (err) {
      setError('Failed to update task');
      console.error(err);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (!user?.id) return;

    try {
      await TaskService.deleteTask(taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err) {
      setError('Failed to delete task');
      console.error(err);
    }
  };

  const handleEditClick = (task: Task) => {
    setEditingTask(task);
    setEditTitle(task.title);
    setEditDescription(task.description || '');
  };

  const handleSaveEdit = async () => {
    if (!editingTask || !user?.id) return;

    try {
      const response = await TaskService.updateTask(editingTask.id, {
        title: editTitle,
        description: editDescription, // Pass description
        completed: editingTask.completed
      });

      setTasks(tasks.map(t => t.id === editingTask.id ? response.task : t)); // Extract task from response
      setEditingTask(null);
      setEditTitle('');
      setEditDescription('');
    } catch (err) {
      setError('Failed to update task');
      console.error(err);
    }
  };


  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
          <p className="mt-4 text-sm text-gray-600">Loading your tasks...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <Card className="max-w-2xl mx-auto mt-8">
        <CardContent className="p-6">
          <p className="text-red-600 text-center">{error}</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold text-gray-900">Todo Dashboard</h1>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-700">
              Welcome, {user?.name || user?.email}
            </span>
            <LogoutButton />
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        <div className="space-y-8">
          <Card>
            <CardHeader>
              <CardTitle>Add New Task</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleAddTask} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="title">Title</Label>
                  <Input
                    id="title"
                    value={newTaskTitle}
                    onChange={(e) => setNewTaskTitle(e.target.value)}
                    placeholder="What needs to be done?"
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="description">Description (optional)</Label>
                  <Input
                    id="description"
                    value={newTaskDescription}
                    onChange={(e) => setNewTaskDescription(e.target.value)}
                    placeholder="Add details..."
                  />
                </div>
                <Button type="submit" className="w-full">
                  Add Task
                </Button>
              </form>
            </CardContent>
          </Card>

          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">Your Tasks</h2>
            <div className="flex space-x-2">
              <Button
                variant={filter === 'all' ? 'default' : 'outline'}
                onClick={() => setFilter('all')}
              >
                All
              </Button>
              <Button
                variant={filter === 'active' ? 'default' : 'outline'}
                onClick={() => setFilter('active')}
              >
                Active ({activeCount})
              </Button>
              <Button
                variant={filter === 'completed' ? 'default' : 'outline'}
                onClick={() => setFilter('completed')}
              >
                Completed ({completedCount})
              </Button>
            </div>
          </div>

          <Card>
            <CardContent className="p-0">
              {filteredTasks.length === 0 ? (
                <div className="p-8 text-center text-gray-500">
                  {filter === 'all'
                    ? 'No tasks yet. Add one above!'
                    : filter === 'active'
                      ? 'No active tasks. Great job!'
                      : 'No completed tasks yet.'}
                </div>
              ) : (
                <ul className="divide-y divide-gray-200">
                  {filteredTasks.map((task) => (
                    <li key={task.id} className="p-4 hover:bg-gray-50">
                      <div className="flex items-center space-x-4">
                        <Checkbox
                          id={`task-${task.id}`}
                          checked={task.completed}
                          onCheckedChange={() => handleToggleComplete(task)}
                        />
                        <div className="flex-1 min-w-0">
                          <p className={`text-sm font-medium truncate ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                            {task.title}
                          </p>
                          {task.description && (
                            <p className="text-sm text-gray-500 truncate">
                              {task.description}
                            </p>
                          )}
                        </div>
                        <div className="flex space-x-2">
                          <Badge variant={task.completed ? 'secondary' : 'outline'}>
                            {task.completed ? 'Completed' : 'Pending'}
                          </Badge>
                          <Dialog>
                            <DialogTrigger asChild>
                              <Button variant="outline" size="sm" onClick={() => handleEditClick(task)}>
                                Edit
                              </Button>
                            </DialogTrigger>
                            <DialogContent className="sm:max-w-[425px]">
                              <DialogHeader>
                                <DialogTitle>Edit Task</DialogTitle>
                                <DialogDescription>
                                  Update your task details here.
                                </DialogDescription>
                              </DialogHeader>
                              <div className="grid gap-4 py-4">
                                <div className="grid grid-cols-4 items-center gap-4">
                                  <Label htmlFor="edit-title" className="text-right">
                                    Title
                                  </Label>
                                  <Input
                                    id="edit-title"
                                    value={editTitle}
                                    onChange={(e) => setEditTitle(e.target.value)}
                                    className="col-span-3"
                                  />
                                </div>
                                <div className="grid grid-cols-4 items-center gap-4">
                                  <Label htmlFor="edit-description" className="text-right">
                                    Description
                                  </Label>
                                  <Input
                                    id="edit-description"
                                    value={editDescription}
                                    onChange={(e) => setEditDescription(e.target.value)}
                                    className="col-span-3"
                                  />
                                </div>
                              </div>
                              <DialogFooter>
                                <Button type="submit" onClick={handleSaveEdit}>Save changes</Button>
                              </DialogFooter>
                            </DialogContent>
                          </Dialog>
                          <Button
                            variant="destructive"
                            size="sm"
                            onClick={() => handleDeleteTask(task.id)}
                          >
                            Delete
                          </Button>
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </CardContent>
          </Card>

          <div className="flex justify-between items-center text-sm text-gray-500">
            <span>{activeCount} active, {completedCount} completed</span>
            <span>Total: {tasks.length} tasks</span>
          </div>
        </div>
      </main>
    </div>
  );
}