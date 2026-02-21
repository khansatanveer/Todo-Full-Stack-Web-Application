'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LogoutButton() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const handleLogout = () => {
    setLoading(true);

    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token'); // remove JWT token
      localStorage.removeItem('refresh_token'); // optional
    }

    router.push('/auth/login'); // redirect to login
  };

  return (
    <button
      onClick={handleLogout}
      disabled={loading}
      className={`
        inline-flex items-center px-4 py-2 rounded-md shadow-sm
        bg-red-600 text-white text-sm font-medium
        hover:bg-red-700 focus:outline-none focus:ring-2
        focus:ring-offset-2 focus:ring-red-500
        ${loading ? 'opacity-50 cursor-not-allowed' : ''}
      `}
    >
      {loading ? (
        <>
          <svg
            className="-ml-1 mr-2 h-4 w-4 animate-spin"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            ></circle>
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
          Signing out...
        </>
      ) : (
        'Sign Out'
      )}
    </button>
  );
}
