/**
 * API Error Handler
 * Handles API errors gracefully with user-friendly messages
 */

export class ApiErrorHandler {
  /**
   * Handle API errors and return user-friendly messages
   */
  static handleError(error: any): { message: string; code: string } {
    // Check if it's a fetch/network error
    if (error instanceof TypeError) {
      return {
        message: 'Network error. Please check your connection and try again.',
        code: 'NETWORK_ERROR'
      };
    }

    // Check if error has response property (HTTP errors)
    if (error && typeof error === 'object' && error.status) {
      const status = error.status;

      switch (status) {
        case 400:
          return {
            message: 'Invalid request. Please check your input and try again.',
            code: 'BAD_REQUEST'
          };
        case 401:
          return {
            message: 'Session expired. Please sign in again.',
            code: 'UNAUTHORIZED'
          };
        case 403:
          return {
            message: 'Access denied. You do not have permission to perform this action.',
            code: 'FORBIDDEN'
          };
        case 404:
          return {
            message: 'Resource not found. It may have been deleted or moved.',
            code: 'NOT_FOUND'
          };
        case 422:
          return {
            message: 'Validation error. Please check your input and try again.',
            code: 'VALIDATION_ERROR'
          };
        case 500:
          return {
            message: 'Server error. Please try again later.',
            code: 'SERVER_ERROR'
          };
        default:
          return {
            message: `Request failed with status ${status}. Please try again.`,
            code: 'REQUEST_FAILED'
          };
      }
    }

    // For other types of errors
    return {
      message: 'An unexpected error occurred. Please try again.',
      code: 'UNKNOWN_ERROR'
    };
  }

  /**
   * Check if error is an authentication error (401)
   */
  static isAuthError(error: any): boolean {
    if (error && typeof error === 'object' && error.status === 401) {
      return true;
    }
    // Also check for network errors that might indicate auth issues
    if (error && typeof error === 'object' && error.message?.includes('Unauthorized')) {
      return true;
    }
    return false;
  }

  /**
   * Check if error is a network error
   */
  static isNetworkError(error: any): boolean {
    return error instanceof TypeError || (error && typeof error === 'object' && error.message?.includes('fetch'));
  }
}