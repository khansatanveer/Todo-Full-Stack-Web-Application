/**
 * Create apiFetch function to automatically attach JWT token from Better Auth session in Authorization header
 * Base URL: http://localhost:8000/api
 */

// Import the auth client functions
import { getSession } from "../auth";

/**
 * apiFetch function that automatically attaches JWT token from Better Auth session in Authorization header
 * @param endpoint - The API endpoint to call (e.g., '/tasks', '/users', etc.)
 * @param options - Additional fetch options to include with the request
 * @returns Promise containing the fetch response
 */
export async function apiFetch(endpoint: string, options: RequestInit = {}) {
  // Get the session to check if authenticated
  const session = await getSession();
  // Get the token from localStorage
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

  if (!session || !token) {
    throw new Error('User not authenticated');
  }

  // Construct the full URL
  const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
  const url = `${apiUrl}/api${endpoint}`;

  // Create headers with authorization token
  const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
    ...options.headers,
  };

  // Make the API request
  const response = await fetch(url, {
    ...options,
    headers,
  });

  return response;
}