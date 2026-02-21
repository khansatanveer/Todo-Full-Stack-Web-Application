'use client';

import Link from 'next/link';
import { useEffect } from 'react';
import { getSession } from '@/lib/auth/client';

export default function HomePage() {
  useEffect(() => {
    const checkAuth = async () => {
      const session = await getSession();
      if (session?.user) {
        window.location.href = '/dashboard';
      }
    };

    checkAuth();
  }, []);

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 font-sans">
      <div className="flex min-h-screen w-full max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-black sm:items-start sm:text-left">
        <div className="flex flex-col items-center gap-6 text-center sm:items-start sm:text-left">
          <h1 className="max-w-xs text-3xl font-semibold leading-10 tracking-tight text-gray-900 dark:text-zinc-50">
            Welcome to Todo App
          </h1>
          <p className="max-w-md text-lg leading-8 text-gray-600 dark:text-gray-400">
            A secure todo application with authentication. Manage your tasks efficiently and securely.
          </p>
        </div>
        <div className="flex flex-col gap-4 text-base font-medium sm:flex-row">
          <Link
            href="/auth/login"
            className="flex h-12 w-full items-center justify-center gap-2 rounded-full bg-gray-900 px-5 text-white transition-colors hover:bg-gray-800 dark:hover:bg-gray-700 md:w-[158px]"
          >
            Login
          </Link>
          <Link
            href="/auth/register"
            className="flex h-12 w-full items-center justify-center rounded-full border border-solid border-gray-800 px-5 transition-colors hover:border-transparent hover:bg-gray-100 dark:border-gray-300 dark:hover:bg-gray-800 md:w-[158px]"
          >
            Register
          </Link>
        </div>
      </div>
    </div>
  );
}