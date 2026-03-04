// lib/auth/client.ts
// Simple auth client using backend API

// Session helper
export async function getSession() {
  if (typeof window === 'undefined') return null; // safety

  try {
    const token = localStorage.getItem('access_token');
    console.log('getSession - token exists?', !!token);
    if (!token) return null;

    const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    console.log('getSession - fetching from:', `${apiUrl}/api/users/me`);
    
    const response = await fetch(`${apiUrl}/api/users/me`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      cache: 'no-store',
    });
    console.log("API URL:", apiUrl)
    console.log('getSession - response status:', response.status);
    const text = await response.text();
    console.log('getSession - response text:', text.substring(0, 200));

    if (!response.ok) {
      // Check if response is HTML (error page) instead of JSON
      if (text.trim().startsWith('<') || text.includes('Internal')) {
        console.error('Received HTML error instead of JSON');
        localStorage.removeItem('access_token');
        return null;
      }
      
      try {
        const errorData = JSON.parse(text);
        console.error('Error data:', errorData);
      } catch {
        console.error('Non-JSON response:', text);
      }
      
      localStorage.removeItem('access_token'); // invalid token remove kar do
      return null;
    }

    const data = JSON.parse(text);
    console.log('getSession - user data:', data);
    return { user: data }; // assuming backend { id, email, name, ... } return karta
  } catch (err) {
    console.error('getSession error:', err);
    return null;
  }
}

// Export simple auth functions that use the backend API
export const signIn = {
  email: async ({ email, password, callbackURL = '/dashboard' }: { email: string; password: string; callbackURL?: string }) => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/auth/sign-in/email`, {
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
      
      if (!data.access_token) {
        return { error: { message: 'Token not received from server' } };
      }

      // Store token in localStorage
      if (typeof window !== 'undefined') {
        localStorage.setItem('access_token', data.access_token);
        
        // Use window.location.href for immediate redirect to ensure 
        // fresh session state on the target page
        if (callbackURL) {
          window.location.href = callbackURL;
        }
      }

      return { user: data.user || { email } }; 
    } catch (error: any) {
      return { error: { message: error.message || 'Sign in failed' } };
    }
  }
};

export const signUp = {
  email: async ({ email, password, name, callbackURL = '/dashboard' }: { email: string; password: string; name?: string; callbackURL?: string }) => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/auth/sign-up/email`, {
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
      
      if (!data.access_token) {
        return { error: { message: 'Token not received from server' } };
      }

      // Store token in localStorage
      if (typeof window !== 'undefined') {
        localStorage.setItem('access_token', data.access_token);
        
        // Use window.location.href for immediate redirect
        if (callbackURL) {
          window.location.href = callbackURL;
        }
      }
      
      return { user: data.user || { email, name } }; 
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
