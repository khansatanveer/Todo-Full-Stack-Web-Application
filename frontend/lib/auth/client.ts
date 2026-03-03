// lib/auth/client.ts
// Simple auth client using backend API

// Session helper
export async function getSession() {
  if (typeof window === 'undefined') return null; // safety

  try {
    const token = localStorage.getItem('access_token');
    if (!token) return null;

    const response = await fetch('http://localhost:8000/api/users/me', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      credentials: 'include', // agar future mein cookie use karo
      cache: 'no-store',
    });

    if (!response.ok) {
      console.error('Session fetch failed:', response.status, await response.text());
      localStorage.removeItem('access_token'); // invalid token remove kar do
      return null;
    }

    const data = await response.json();
    return { user: data }; // assuming backend { id, email, name, ... } return karta
  } catch (err) {
    console.error('getSession error:', err);
    return null;
  }
}

// Export simple auth functions that use the backend API
export const signIn = {
  email: async ({ email, password }: { email: string; password: string }) => {
    try {
      const response = await fetch('http://localhost:8000/api/auth/sign-in/email', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        return { error: { message: errorData.detail || 'Sign in failed' } };
      }

      const data = await response.json();
      // Store token in localStorage
      if (typeof window !== 'undefined') {
        localStorage.setItem('access_token', data.access_token);
      }

      return { user: { email } }; // Simplified response
    } catch (error: any) {
      return { error: { message: error.message || 'Sign in failed' } };
    }
  }
};

export const signUp = {
  email: async ({ email, password, name }: { email: string; password: string; name?: string }) => {
    try {
      const response = await fetch('http://localhost:8000/api/auth/sign-up/email', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, name }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        return { error: { message: errorData.detail || 'Registration failed' } };
      }

      const data = await response.json();
      // Store token in localStorage
      if (typeof window !== 'undefined') {
        localStorage.setItem('access_token', data.access_token);
      }
     const token = localStorage.getItem('access_token');
console.log('getSession - token exists?', !!token);
if (token) console.log('Token first chars:', token.substring(0, 20));
      return { user: { email, name } }; // Simplified response
    } catch (error: any) {
      return { error: { message: error.message || 'Registration failed' } };
    }
  }
};

export const signOut = async ({ callbackURL = '/auth/login' }: { callbackURL?: string } = {}) => {
  try {
    // Clear token from localStorage
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
    }

    // Redirect to callbackURL if provided
    if (callbackURL && typeof window !== 'undefined') {
      window.location.href = callbackURL;
    }
  } catch (error: any) {
    throw new Error(error.message || 'Sign out failed');
  }
};

// ✅ DEFAULT EXPORT
const authClient = {
  signIn,
  signUp,
  signOut,
  getSession,
};

export default authClient;
