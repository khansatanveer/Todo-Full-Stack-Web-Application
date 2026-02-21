'use client';

import { useState, useEffect } from 'react';
import { getSession, signOut as authSignOut } from '../lib/auth/client';

export const useAuth = () => {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Check session on mount
  useEffect(() => {
    const checkSession = async () => {
      try {
        const session = await getSession();
        if (session?.user) {
          setUser(session.user);
        } else {
          setUser(null);
        }
      } catch (err) {
        setError('Failed to get session');
        console.error('Session error:', err);
      } finally {
        setLoading(false);
      }
    };

    checkSession();
  }, []);

  const logout = async () => {
    try {
      await authSignOut();
      setUser(null);
    } catch (err) {
      setError('Failed to sign out');
      console.error('Sign out error:', err);
    }
  };

  const isAuthenticated = !!user;

  return {
    user,
    loading,
    error,
    isAuthenticated,
    logout,
  };
};