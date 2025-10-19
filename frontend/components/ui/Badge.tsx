'use client';

import { HTMLAttributes } from 'react';

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'success' | 'warning' | 'error' | 'info';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

/**
 * Brutalist-styled badge component for status indicators
 *
 * @example
 * <Badge variant="success">Verified</Badge>
 * <Badge variant="warning" size="lg">Pending</Badge>
 * <Badge variant="error">Failed</Badge>
 */
export default function Badge({
  variant = 'default',
  size = 'md',
  children,
  className = '',
  ...props
}: BadgeProps) {
  const baseClasses = 'inline-flex items-center justify-center font-bold uppercase border-2 border-black';

  const variantClasses = {
    default: 'bg-gray-200 text-gray-800',
    success: 'bg-green-100 text-green-800 border-green-600',
    warning: 'bg-orange-100 text-orange-800 border-orange-600',
    error: 'bg-red-100 text-red-800 border-red-600',
    info: 'bg-blue-100 text-blue-800 border-blue-600',
  };

  const sizeClasses = {
    sm: 'text-xs px-2 py-0.5',
    md: 'text-xs px-3 py-1',
    lg: 'text-sm px-4 py-2',
  };

  const pulseClass = (variant === 'warning' || variant === 'error') ? 'badge-pulse' : '';

  return (
    <span
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${pulseClass} ${className}`}
      {...props}
    >
      {children}
    </span>
  );
}
