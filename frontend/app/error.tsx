'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="brutal-box brutal-shadow bg-red-50 p-8 max-w-md w-full">
        <h2 className="text-2xl font-black mb-4">⚠️ SOMETHING WENT WRONG</h2>
        <p className="text-sm mb-4 font-mono bg-white p-3 border-2 border-black">
          {error.message || 'An unexpected error occurred'}
        </p>
        <button
          onClick={reset}
          className="brutal-btn w-full"
        >
          TRY AGAIN
        </button>
      </div>
    </div>
  );
}
