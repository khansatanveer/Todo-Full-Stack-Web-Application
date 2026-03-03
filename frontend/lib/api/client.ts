import { getSession } from "../auth"; // Import the auth client functions

const API_BASE_URL = "http://localhost:8000/api";

export async function apiFetch(
  endpoint: string,
  options: RequestInit = {}
) {
  const session = await getSession();

  if (!session?.token) {
    throw new Error("User not authenticated");
  }

  return fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      ...(options.headers || {}),
      Authorization: `Bearer ${session.token}`,
      "Content-Type": "application/json",
    },
  });
}
