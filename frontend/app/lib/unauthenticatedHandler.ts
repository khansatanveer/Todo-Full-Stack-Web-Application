import { signOut } from '../../lib/auth/client';
import { redirect } from 'next/navigation';

/**
 * Handler for unauthenticated requests
 * This function handles what happens when a request fails due to authentication issues
 */
export const handleUnauthenticatedRequest = async (redirectUrl: string = '/login') => {
  console.warn('Unauthenticated request detected, redirecting to login...');

  try {
    // Sign out the current user session
    await signOut({
      callbackURL: redirectUrl
    });
  } catch (error) {
    console.error('Error during sign out in unauthenticated handler:', error);
    // Even if sign out fails, still redirect to login
  }

  // In a client-side context, we'd redirect like this:
  // window.location.href = redirectUrl;

  // For Next.js App Router, we'll return a redirect function that can be called
  return () => {
    // This is where you'd handle the actual redirect based on your app structure
    if (typeof window !== 'undefined') {
      window.location.href = redirectUrl;
    }
  };
};

/**
 * Wrapper for API calls that need authentication
 * This ensures proper handling of unauthenticated requests
 */
export const withAuthProtection = async <T>(
  apiCall: () => Promise<T>,
  redirectUrl: string = '/login'
): Promise<T> => {
  try {
    return await apiCall();
  } catch (error: any) {
    if (error.response?.status === 401) {
      // Handle the unauthenticated state
      await handleUnauthenticatedRequest(redirectUrl);
      throw error; // Re-throw to be handled by calling component
    }
    throw error; // Re-throw other errors
  }
};