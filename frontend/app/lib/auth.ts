import { useQuery } from '@tanstack/react-query';

// Create a wrapper for useSession hook that works with our implementation
export const useSession = () => {
  return useQuery({
    queryKey: ['session'],
    queryFn: async () => {
      // Check if we have a token in localStorage
      if (typeof window !== 'undefined') {
        const token = localStorage.getItem('access_token');
        if (token) {
          // Verify token by making a request to protected endpoint
          try {
            const response = await fetch('http://localhost:8000/api/users/me', {
              headers: {
                'Authorization': `Bearer ${token}`
              }
            });

            if (response.ok) {
              return await response.json();
            }
          } catch (error) {
            console.error('Session verification failed:', error);
          }
        }
      }
      return null;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 1,
  });
};

// Re-export auth functions
export const signIn = () => {};
export const signUp = () => {};
export const signOut = () => {};
export const getSession = async () => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        const response = await fetch('http://localhost:8000/api/users/me', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          return await response.json();
        }
      } catch (error) {
        console.error('Session verification failed:', error);
      }
    }
  }
  return null;
};