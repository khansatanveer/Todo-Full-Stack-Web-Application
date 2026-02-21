// Authentication constants
export const AUTH_CONSTANTS = {
  // JWT Algorithm
  JWT_ALGORITHM: 'HS256',

  // Token expiration (1 hour in seconds)
  TOKEN_EXPIRATION: 3600,

  // Local storage keys
  ACCESS_TOKEN_KEY: 'access_token',
  REFRESH_TOKEN_KEY: 'refresh_token',

  // API endpoints
  AUTH_BASE_PATH: '/api/auth',

  // Headers
  AUTHORIZATION_HEADER: 'Authorization',
  BEARER_PREFIX: 'Bearer ',
} as const;