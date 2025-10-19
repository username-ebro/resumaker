import SignupForm from '@/components/SignupForm';
import Link from 'next/link';

export default function SignupPage() {
  return (
    <div className="auth-container page-enter">
      <div className="auth-card">
        <div className="auth-header">
          <h1 className="auth-logo">RESUMAKER</h1>
          <p className="auth-tagline">Start Building Your Future</p>
        </div>

        <SignupForm />

        <div className="text-center mt-8">
          <p className="text-sm text-gray-600">
            Already have an account?{' '}
            <Link href="/auth/login" className="auth-link">
              Login
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
