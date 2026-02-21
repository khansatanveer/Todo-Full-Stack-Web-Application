// Authentication constants
export const AUTH_CONSTANTS = {
  // Better Auth uses cookie-based authentication, but we keep some constants for reference
  // JWT Algorithm (not used directly with Better Auth, but kept for API compatibility)
  JWT_ALGORITHM: 'HS256',

  // Token expiration (not used directly with Better Auth)
  TOKEN_EXPIRATION: 7 * 24 * 60 * 60,

  // Local storage keys (not used with Better Auth - it uses cookies)
  ACCESS_TOKEN_KEY: 'better-auth.session_token',
  REFRESH_TOKEN_KEY: 'better-auth.refresh_token',

  // API endpoints
  AUTH_BASE_PATH: '/api/auth',

  // Headers
  AUTHORIZATION_HEADER: 'Authorization',
  BEARER_PREFIX: 'Bearer ',
} as const;