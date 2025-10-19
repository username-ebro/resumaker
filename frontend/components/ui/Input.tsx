'use client';

import { InputHTMLAttributes, TextareaHTMLAttributes, useState } from 'react';

interface BaseInputProps {
  label?: string;
  error?: string;
  helperText?: string;
  required?: boolean;
}

interface TextInputProps extends BaseInputProps, Omit<InputHTMLAttributes<HTMLInputElement>, 'type' | 'onChange'> {
  type?: 'text' | 'email' | 'password';
  value: string;
  onChange: (value: string) => void;
}

interface TextareaInputProps extends BaseInputProps, Omit<TextareaHTMLAttributes<HTMLTextAreaElement>, 'onChange'> {
  type: 'textarea';
  value: string;
  onChange: (value: string) => void;
  rows?: number;
}

type InputProps = TextInputProps | TextareaInputProps;

/**
 * Brutalist-styled input component with label, error, and helper text support
 *
 * @example
 * <Input
 *   label="Email Address"
 *   type="email"
 *   value={email}
 *   onChange={setEmail}
 *   placeholder="you@example.com"
 *   required
 * />
 *
 * <Input
 *   label="Description"
 *   type="textarea"
 *   value={description}
 *   onChange={setDescription}
 *   rows={4}
 *   error="Description is required"
 * />
 */
export default function Input({
  label,
  error,
  helperText,
  required,
  className = '',
  ...props
}: InputProps) {
  const [showPassword, setShowPassword] = useState(false);

  const inputClasses = `brutal-input ${error ? 'border-red-600 bg-red-50' : ''} ${className}`;

  const isTextarea = props.type === 'textarea';
  const isPassword = !isTextarea && props.type === 'password';

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    props.onChange(e.target.value);
  };

  return (
    <div className="form-group">
      {label && (
        <label className="form-label">
          {label}
          {required && <span className="text-red-600 ml-1">*</span>}
        </label>
      )}

      {isTextarea ? (
        <textarea
          {...(props as TextareaInputProps)}
          onChange={handleChange}
          className={inputClasses}
          rows={props.rows || 4}
          aria-invalid={!!error}
          aria-describedby={error ? `${props.id}-error` : helperText ? `${props.id}-helper` : undefined}
        />
      ) : isPassword ? (
        <div className="password-input-wrapper">
          <input
            {...(props as TextInputProps)}
            type={showPassword ? 'text' : 'password'}
            onChange={handleChange}
            className={inputClasses}
            aria-invalid={!!error}
            aria-describedby={error ? `${props.id}-error` : helperText ? `${props.id}-helper` : undefined}
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="password-toggle"
            aria-label={showPassword ? 'Hide password' : 'Show password'}
          >
            {showPassword ? '🙈' : '👁️'}
          </button>
        </div>
      ) : (
        <input
          {...(props as TextInputProps)}
          onChange={handleChange}
          className={inputClasses}
          aria-invalid={!!error}
          aria-describedby={error ? `${props.id}-error` : helperText ? `${props.id}-helper` : undefined}
        />
      )}

      {error && (
        <p id={`${props.id}-error`} className="text-xs text-red-600 mt-2 font-medium">
          {error}
        </p>
      )}

      {!error && helperText && (
        <p id={`${props.id}-helper`} className="form-helper">
          {helperText}
        </p>
      )}
    </div>
  );
}
