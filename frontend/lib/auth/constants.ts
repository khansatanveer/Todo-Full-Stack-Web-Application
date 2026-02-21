// Authentication constants
export const AUTH_CONSTANTS = {
  // JWT Algorithm
  JWT_ALGORITHM: 'HS256',

  // Token expiration (7 days in seconds - as per our spec)
  TOKEN_EXPIRATION: 7 * 24 * 60 * 60,

  // Local storage keys
  ACCESS_TOKEN_KEY: 'better-auth.session_token',
  REFRESH_TOKEN_KEY: 'refresh_token',

  // API endpoints
  AUTH_BASE_PATH: '/api/auth',

  // Headers
  AUTHORIZATION_HEADER: 'Authorization',
  BEARER_PREFIX: 'Bearer ',
} as const;