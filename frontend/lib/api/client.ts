import { getSession } from "../auth"; // Import the auth client functions

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ? `${process.env.NEXT_PUBLIC_API_BASE_URL}/api` : "http://localhost:8000/api";

export async function apiFetch(
  endpoint: string,
  options: RequestInit = {}
) {
  const session = await getSession();
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

  if (!session || !token) {
    throw new Error("User not authenticated");
  }

  return fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });
}
