'use client';

import { useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';

interface NavigationLink {
  label: string;
  href: string;
  icon?: string;
}

interface NavigationProps {
  user?: { email: string; name?: string };
  onLogout?: () => void;
  links?: NavigationLink[];
  badge?: { count: number; href: string };
}

/**
 * Brutalist-styled navigation component with user menu and responsive design
 *
 * @example
 * <Navigation
 *   user={{ email: 'user@example.com', name: 'John Doe' }}
 *   onLogout={handleLogout}
 *   links={[
 *     { label: 'Dashboard', href: '/dashboard', icon: '🏠' },
 *     { label: 'Resumes', href: '/resumes', icon: '📄' },
 *   ]}
 *   badge={{ count: 5, href: '/knowledge' }}
 * />
 */
export default function Navigation({
  user,
  onLogout,
  links = [],
  badge,
}: NavigationProps) {
  const [menuOpen, setMenuOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const router = useRouter();
  const pathname = usePathname();

  const displayName = user?.name || user?.email?.split('@')[0] || 'User';

  return (
    <nav className="brutal-box border-b-4 border-black bg-white sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-6">
        <div className="flex justify-between items-center">
          {/* Logo */}
          <div className="flex items-center gap-4">
            <button
              onClick={() => router.push('/')}
              className="text-3xl font-black tracking-tight hover:opacity-70 transition-opacity"
            >
              RESUMAKER
            </button>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-4">
            {/* Navigation Links */}
            {links.map((link) => {
              const isActive = pathname === link.href;
              return (
                <button
                  key={link.href}
                  onClick={() => router.push(link.href)}
                  className={`brutal-btn brutal-shadow text-sm ${
                    isActive ? 'brutal-btn-primary' : 'brutal-btn-seafoam'
                  }`}
                >
                  {link.icon && <span className="mr-1">{link.icon}</span>}
                  {link.label}
                </button>
              );
            })}

            {/* Badge Link (e.g., Knowledge Base with pending count) */}
            {badge && badge.count > 0 && (
              <button
                onClick={() => router.push(badge.href)}
                className="brutal-btn brutal-btn-seafoam brutal-shadow relative text-sm"
              >
                📚 Knowledge Base
                <span className="absolute -top-2 -right-2 bg-black text-white text-xs font-bold px-2 py-1 border-2 border-black">
                  {badge.count}
                </span>
              </button>
            )}

            {/* User Menu */}
            {user && (
              <div className="relative">
                <button
                  onClick={() => setMenuOpen(!menuOpen)}
                  className="brutal-btn brutal-shadow text-sm flex items-center gap-2"
                >
                  <span className="max-w-[120px] truncate">{displayName}</span>
                  <span className={`transition-transform ${menuOpen ? 'rotate-180' : ''}`}>
                    ▼
                  </span>
                </button>

                {menuOpen && (
                  <>
                    <div
                      className="fixed inset-0 z-10"
                      onClick={() => setMenuOpen(false)}
                    />
                    <div className="absolute right-0 mt-2 w-48 brutal-box brutal-shadow bg-white z-20">
                      <div className="p-2 border-b-2 border-black">
                        <p className="text-xs font-bold uppercase text-gray-500">Signed in as</p>
                        <p className="text-sm font-bold truncate">{user.email}</p>
                      </div>
                      <button
                        onClick={() => {
                          setMenuOpen(false);
                          onLogout?.();
                        }}
                        className="w-full text-left px-4 py-3 hover:bg-gray-100 transition-colors text-sm font-bold uppercase"
                      >
                        Logout
                      </button>
                    </div>
                  </>
                )}
              </div>
            )}

            {/* Logout Button (if no user menu) */}
            {!user && onLogout && (
              <button
                onClick={onLogout}
                className="brutal-btn brutal-shadow text-sm"
              >
                Logout
              </button>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden brutal-btn brutal-shadow text-sm px-3"
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? '✕' : '☰'}
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden mt-4 pt-4 border-t-2 border-black space-y-2">
            {links.map((link) => {
              const isActive = pathname === link.href;
              return (
                <button
                  key={link.href}
                  onClick={() => {
                    router.push(link.href);
                    setMobileMenuOpen(false);
                  }}
                  className={`brutal-btn brutal-shadow text-sm w-full ${
                    isActive ? 'brutal-btn-primary' : 'brutal-btn-seafoam'
                  }`}
                >
                  {link.icon && <span className="mr-2">{link.icon}</span>}
                  {link.label}
                </button>
              );
            })}

            {badge && badge.count > 0 && (
              <button
                onClick={() => {
                  router.push(badge.href);
                  setMobileMenuOpen(false);
                }}
                className="brutal-btn brutal-btn-seafoam brutal-shadow w-full text-sm relative"
              >
                📚 Knowledge Base
                <span className="ml-2 bg-black text-white text-xs font-bold px-2 py-1 border-2 border-black">
                  {badge.count}
                </span>
              </button>
            )}

            {user && (
              <>
                <div className="brutal-box p-3 bg-gray-50">
                  <p className="text-xs font-bold uppercase text-gray-500 mb-1">Signed in as</p>
                  <p className="text-sm font-bold truncate">{user.email}</p>
                </div>
                <button
                  onClick={() => {
                    setMobileMenuOpen(false);
                    onLogout?.();
                  }}
                  className="brutal-btn brutal-shadow text-sm w-full"
                >
                  Logout
                </button>
              </>
            )}
          </div>
        )}
      </div>
    </nav>
  );
}
