import { useQuery } from '@tanstack/react-query';
import { authClient } from 'better-auth/client';
import { AUTH_CONSTANTS } from '@/lib/auth/constants';

// Initialize Better Auth client
const betterAuthClient = authClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:3000',
  fetchOptions: {
    credentials: 'include',
  }
});

// Create a wrapper for useSession hook that works with Better Auth
export const useSession = () => {
  return useQuery({
    queryKey: ['session'],
    queryFn: async () => {
      try {
        const session = await betterAuthClient.getSession();
        return session?.session ? session.session : null;
      } catch (error: any) {
        console.error('Session verification error:', error.message || error);
        return null;
      }
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 1,
  });
};

// Re-export Better Auth functions
export const signIn = betterAuthClient.signIn.email;
export const signUp = betterAuthClient.signUp.email;
export const signOut = betterAuthClient.signOut;
export const getSession = async () => {
  try {
    const session = await betterAuthClient.getSession();
    return session?.session ? session.session : null;
  } catch (error) {
    console.error('Session verification failed:', error);
    return null;
  }
};