'use client';

import { useState, Suspense } from 'react';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';

function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Get callbackUrl from search params, default to /dashboard
  const callbackUrl = searchParams.get('callbackUrl') || '/dashboard';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Use backend API instead of Better Auth
      const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/auth/sign-in/email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const text = await response.text();
        // Check if response is HTML error page
        if (text.trim().startsWith('<') || text.includes('Internal')) {
          throw new Error('Server error. Please try again.');
        }
        try {
          const errorData = JSON.parse(text);
          throw new Error(errorData.detail || errorData.message || 'Sign in failed');
        } catch {
          throw new Error('Sign in failed');
        }
      }

      const text = await response.text();
      // Check if response is valid JSON
      if (text.trim().startsWith('<') || text.includes('Internal')) {
        throw new Error('Server error. Please try again.');
      }

      const data = JSON.parse(text);

      // Store token in localStorage
      if (typeof window !== 'undefined') {
        localStorage.setItem('access_token', data.access_token);
      }

      // Sign in successful, redirect to callbackUrl
      // Use window.location.href for a full page reload to ensure token is available
      window.location.href = callbackUrl;
    } catch (err: any) {
      setError(err.message || 'An error occurred during sign in');
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl text-center">Sign in</CardTitle>
        <CardDescription className="text-center">
          Enter your credentials to access your account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <div className="space-y-2">
            <label htmlFor="email" className="text-sm font-medium">Email</label>
            <Input
              id="email"
              type="email"
              placeholder="your@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="password" className="text-sm font-medium">Password</label>
            <Input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign in'}
          </Button>

          <div className="text-center text-sm pt-4">
            <p>
              Don&apos;t have an account?{' '}
              <Link href={`/auth/signup?callbackUrl=${encodeURIComponent(callbackUrl)}`} className="font-medium text-indigo-600 hover:text-indigo-500">
                Sign up
              </Link>
            </p>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}

export default function LoginPage() {
  return (
    <Suspense fallback={<div className="text-center p-4">Loading login form...</div>}>
      <LoginForm />
    </Suspense>
  );
}