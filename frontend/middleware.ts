import { NextRequest, NextResponse } from 'next/server';

// Simple middleware to protect routes
export default function middleware(request: NextRequest) {
  // Allow public routes
  if (request.nextUrl.pathname.startsWith('/auth') ||
      request.nextUrl.pathname === '/' ||
      request.nextUrl.pathname.startsWith('/api/auth')) {
    return NextResponse.next();
  }

  // For protected routes, check if token exists in localStorage (client-side check will happen)
  // We'll allow the request to proceed and let the component handle authentication
  // since we can't access localStorage from server-side middleware
  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
};