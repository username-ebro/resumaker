'use client';

import { HTMLAttributes } from 'react';

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'elevated' | 'dark' | 'outline' | 'seafoam';
  hover?: boolean;
  padding?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

/**
 * Brutalist-styled card component with multiple variants
 *
 * @example
 * <Card variant="elevated" hover padding="lg">
 *   <h3>Card Title</h3>
 *   <p>Card content</p>
 * </Card>
 *
 * <Card variant="dark" onClick={handleClick}>
 *   Clickable dark card
 * </Card>
 */
export default function Card({
  variant = 'default',
  hover = false,
  padding = 'md',
  children,
  className = '',
  onClick,
  ...props
}: CardProps) {
  const baseClasses = 'border-2 border-black transition-all';

  const variantClasses = {
    default: 'brutal-box brutal-shadow bg-white',
    elevated: 'brutal-box bg-white shadow-[10px_10px_0px_var(--black)]',
    dark: 'bg-gradient-to-br from-black to-gray-800 text-white border-black shadow-[6px_6px_0px_var(--black)]',
    outline: 'bg-white border-2 border-black',
    seafoam: 'brutal-box-seafoam brutal-shadow-seafoam',
  };

  const paddingClasses = {
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  };

  const hoverClasses = hover || onClick
    ? 'card-hover cursor-pointer'
    : '';

  return (
    <div
      className={`${baseClasses} ${variantClasses[variant]} ${paddingClasses[padding]} ${hoverClasses} ${className}`}
      onClick={onClick}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
      {...props}
    >
      {children}
    </div>
  );
}
