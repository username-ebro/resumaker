'use client';

import { ButtonHTMLAttributes } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  icon?: React.ReactNode;
  children: React.ReactNode;
}

/**
 * Brutalist-styled button component with variants and loading states
 *
 * @example
 * <Button variant="primary" size="lg" loading={isLoading}>
 *   Generate Resume
 * </Button>
 *
 * <Button variant="danger" icon="🗑️" onClick={handleDelete}>
 *   Delete
 * </Button>
 */
export default function Button({
  variant = 'primary',
  size = 'md',
  loading = false,
  icon,
  children,
  className = '',
  disabled,
  type = 'button',
  ...props
}: ButtonProps) {
  const baseClasses = 'brutal-btn font-bold uppercase transition-all inline-flex items-center justify-center gap-2';

  const variantClasses = {
    primary: 'brutal-btn-primary',
    secondary: 'bg-white text-black border-2 border-black hover:bg-gray-100',
    danger: 'bg-white text-red-600 border-2 border-red-600 hover:bg-red-50',
    ghost: 'bg-transparent text-black border-none hover:bg-gray-100',
  };

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-xs',
    md: 'px-6 py-3 text-sm',
    lg: 'px-8 py-4 text-base',
  };

  return (
    <button
      type={type}
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${
        loading || disabled ? 'opacity-50 cursor-not-allowed' : ''
      } ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <span className="cool-spinner h-4 w-4 border-2 border-current border-t-transparent rounded-full" />
      )}
      {!loading && icon && <span className="btn-icon inline-block">{icon}</span>}
      {children}
    </button>
  );
}
