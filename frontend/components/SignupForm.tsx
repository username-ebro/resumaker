'use client';

import { useState } from 'react';
import { supabase } from '@/lib/supabase';
import { useRouter } from 'next/navigation';
import { Input, Button } from '@/components/ui';

export default function SignupForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: {
            full_name: fullName,
          },
        },
      });

      if (error) throw error;

      router.push('/dashboard');
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Signup failed');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSignup} className="space-y-6">
      {error && (
        <div className="form-error">
          <strong>Error:</strong> {error}
        </div>
      )}

      <Input
        label="Full Name"
        type="text"
        value={fullName}
        onChange={setFullName}
        placeholder="John Doe"
        autoComplete="name"
        required
      />

      <Input
        label="Email Address"
        type="email"
        value={email}
        onChange={setEmail}
        placeholder="you@example.com"
        autoComplete="email"
        required
      />

      <Input
        label="Password"
        type="password"
        value={password}
        onChange={setPassword}
        placeholder="At least 6 characters"
        autoComplete="new-password"
        helperText="Must be at least 6 characters"
        required
        minLength={6}
      />

      <Button
        type="submit"
        variant="primary"
        size="lg"
        loading={loading}
        className="w-full"
      >
        Sign Up
      </Button>
    </form>
  );
}
