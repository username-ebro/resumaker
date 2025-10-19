'use client';

/**
 * Skeleton loading components for better loading states
 *
 * @example
 * <SkeletonCard />
 * <SkeletonText width="w-3/4" />
 * <SkeletonButton />
 */

export function SkeletonCard() {
  return (
    <div className="brutal-box brutal-shadow p-6">
      <div className="skeleton skeleton-text w-3/4" />
      <div className="skeleton skeleton-text w-1/2" />
      <div className="skeleton skeleton-text w-full" />
    </div>
  );
}

export function SkeletonText({ width = 'w-full' }: { width?: string }) {
  return <div className={`skeleton skeleton-text ${width}`} />;
}

export function SkeletonButton() {
  return <div className="skeleton h-12 w-32" />;
}

export function SkeletonResume() {
  return (
    <div className="brutal-box brutal-shadow p-8">
      <div className="flex justify-between items-start gap-6 mb-6">
        <div className="flex-1">
          <div className="skeleton skeleton-text w-2/3 mb-3" />
          <div className="skeleton skeleton-text w-1/3" />
        </div>
        <div className="skeleton h-24 w-24" />
      </div>
      <div className="space-y-2">
        <div className="skeleton skeleton-text w-full" />
        <div className="skeleton skeleton-text w-5/6" />
        <div className="skeleton skeleton-text w-4/5" />
      </div>
    </div>
  );
}

export function SkeletonList({ count = 3 }: { count?: number }) {
  return (
    <div className="space-y-4">
      {Array.from({ length: count }).map((_, i) => (
        <SkeletonCard key={i} />
      ))}
    </div>
  );
}
