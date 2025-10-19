'use client';

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html>
      <body>
        <div className="min-h-screen flex items-center justify-center p-4 bg-gray-100">
          <div className="brutal-box brutal-shadow bg-red-50 p-8 max-w-md w-full">
            <h2 className="text-2xl font-black mb-4">⚠️ CRITICAL ERROR</h2>
            <p className="text-sm mb-4">The application encountered a critical error. Please refresh the page.</p>
            <button onClick={reset} className="brutal-btn w-full">
              RELOAD
            </button>
          </div>
        </div>
      </body>
    </html>
  );
}
