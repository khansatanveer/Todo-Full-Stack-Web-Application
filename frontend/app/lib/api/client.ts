/**
 * Create apiFetch function to automatically attach JWT token from Better Auth session in Authorization header
 * Base URL: http://localhost:8000/api
 */

// Import the auth utilities from our auth configuration
import { getSession } from '../auth';

/**
 * apiFetch function that automatically attaches JWT token from Better Auth session in Authorization header
 * @param endpoint - The API endpoint to call (e.g., '/tasks', '/users', etc.)
 * @param options - Additional fetch options to include with the request
 * @returns Promise containing the fetch response
 */
export async function apiFetch(endpoint: string, options: RequestInit = {}) {
  // Get the session token to attach to the request
  const session = await getSession();

  if (!session?.token) {
    throw new Error('User not authenticated');
  }

  // Construct the full URL
  const baseUrl = 'http://localhost:8000/api';
  const url = `${baseUrl}${endpoint}`;

  // Create headers with authorization token
  const headers = {
    'Authorization': `Bearer ${session.token}`,
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