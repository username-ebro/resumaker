import LoginForm from '@/components/LoginForm';
import Link from 'next/link';

export default function LoginPage() {
  return (
    <div className="auth-container page-enter">
      <div className="auth-card">
        <div className="auth-header">
          <h1 className="auth-logo">RESUMAKER</h1>
          <p className="auth-tagline">Build Better Resumes, Faster</p>
        </div>

        <LoginForm />

        <div className="text-center mt-8">
          <p className="text-sm text-gray-600">
            Don't have an account?{' '}
            <Link href="/auth/signup" className="auth-link">
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
