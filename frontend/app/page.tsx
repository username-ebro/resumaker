export default function Home() {
  return (
    <main className="min-h-screen p-24">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-4xl font-bold mb-4">Resumaker</h1>
        <p className="text-lg text-gray-600 mb-8">
          AI-powered resume builder with truth verification
        </p>
        <div className="flex gap-4">
          <a
            href="/auth/signup"
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Get Started
          </a>
          <a
            href="/auth/login"
            className="px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Login
          </a>
        </div>
      </div>
    </main>
  );
}
