// Main export for auth functionality
export { default as authClient, signIn, signUp, signOut, getSession } from './client';
export { AUTH_CONSTANTS } from './constants';

// Export constants separately for direct access
export * from './constants';