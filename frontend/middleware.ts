import { NextRequest, NextResponse } from 'next/server';

// Middleware to protect routes
export default function middleware(request: NextRequest) {
  // Allow public routes
  if (request.nextUrl.pathname.startsWith('/auth') ||
      request.nextUrl.pathname === '/' ||
      request.nextUrl.pathname.startsWith('/api/auth') ||
      request.nextUrl.pathname.startsWith('/_next') ||  // Allow Next.js internals
      request.nextUrl.pathname.match(/\.(css|js|png|jpg|jpeg|gif|svg|ico)$/)) {  // Allow static assets
    return NextResponse.next();
  }

  // For protected routes, we allow the request to proceed to the page
  // where client-side authentication will be handled
  // since we can't access localStorage from server-side middleware
  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*', '/((?!api/auth|_next/static|_next/image|favicon.ico).*)'],
};