'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { supabase } from '@/lib/supabase';
import { knowledgeApi, KnowledgeEntity } from '@/lib/api/knowledge';
import FactCard from '@/components/FactCard';
import { useToast } from '@/components/Toast';

export default function KnowledgeBasePage() {
  const router = useRouter();
  const { showToast } = useToast();
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [entities, setEntities] = useState<KnowledgeEntity[]>([]);
  const [filteredEntities, setFilteredEntities] = useState<KnowledgeEntity[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState<string>('all');
  const [summary, setSummary] = useState<any>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    checkUserAndFetch();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [searchQuery, filterType, entities]);

  const checkUserAndFetch = async () => {
    const {
      data: { user },
    } = await supabase.auth.getUser();

    if (!user) {
      router.push('/auth/login');
      return;
    }

    setUser(user);
    await fetchKnowledge(user.id);
  };

  const fetchKnowledge = async (userId: string) => {
    setLoading(true);
    setError('');

    try {
      const [confirmedData, summaryData] = await Promise.all([
        knowledgeApi.getConfirmed(userId),
        knowledgeApi.getSummary(userId),
      ]);

      setEntities(confirmedData.entities);
      setSummary(summaryData);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Failed to load knowledge base');
      }
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = [...entities];

    // Apply type filter
    if (filterType !== 'all') {
      filtered = filtered.filter((e) => e.entity_type === filterType);
    }

    // Apply search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(
        (e) =>
          e.title.toLowerCase().includes(query) ||
          (e.description && e.description.toLowerCase().includes(query))
      );
    }

    setFilteredEntities(filtered);
  };

  const handleEdit = async (id: string, updates: Partial<KnowledgeEntity>) => {
    try {
      await knowledgeApi.updateEntity(id, updates);

      // Update local state
      setEntities((prev) =>
        prev.map((e) => (e.id === id ? { ...e, ...updates } : e))
      );
      showToast('Fact updated successfully', 'success');
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error';
      showToast(`Failed to update: ${message}`, 'error');
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await knowledgeApi.deleteEntity(id);

      // Remove from local state
      setEntities((prev) => prev.filter((e) => e.id !== id));

      // Refresh summary
      if (user) {
        const summaryData = await knowledgeApi.getSummary(user.id);
        setSummary(summaryData);
      }
      showToast('Fact deleted successfully', 'success');
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error';
      showToast(`Failed to delete: ${message}`, 'error');
    }
  };

  // Entity type options
  const entityTypes = [
    { value: 'all', label: 'All Types' },
    { value: 'jobs', label: 'Work Experience' },
    { value: 'skills', label: 'Skills' },
    { value: 'projects', label: 'Projects' },
    { value: 'education', label: 'Education' },
  ];

  // Loading state
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="brutal-box brutal-shadow p-12 text-center">
          <div className="cool-spinner h-12 w-12 border-4 border-black border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-sm font-bold uppercase">Loading knowledge base...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      {/* Nav */}
      <nav className="brutal-box border-b-2 border-black">
        <div className="max-w-7xl mx-auto px-6 py-6 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <button
              onClick={() => router.push('/dashboard')}
              className="brutal-btn brutal-shadow"
            >
              ← Back
            </button>
            <h1 className="text-2xl">KNOWLEDGE BASE</h1>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-12">
        {/* Summary stats */}
        {summary && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div className="brutal-box-seafoam brutal-shadow-seafoam p-4">
              <p className="text-xs font-bold uppercase mb-1">Total Facts</p>
              <p className="text-3xl font-bold">{summary.total}</p>
            </div>
            <div className="brutal-box brutal-shadow p-4">
              <p className="text-xs font-bold uppercase mb-1">Jobs</p>
              <p className="text-3xl font-bold">
                {summary.by_type?.jobs?.confirmed || 0}
              </p>
            </div>
            <div className="brutal-box brutal-shadow p-4">
              <p className="text-xs font-bold uppercase mb-1">Skills</p>
              <p className="text-3xl font-bold">
                {summary.by_type?.skills?.confirmed || 0}
              </p>
            </div>
            <div className="brutal-box brutal-shadow p-4">
              <p className="text-xs font-bold uppercase mb-1">Projects</p>
              <p className="text-3xl font-bold">
                {summary.by_type?.projects?.confirmed || 0}
              </p>
            </div>
          </div>
        )}

        {/* Search and filter */}
        <div className="brutal-box brutal-shadow p-6 mb-8">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search by keyword..."
                className="brutal-input w-full"
              />
            </div>
            <div>
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                className="brutal-input"
              >
                {entityTypes.map((type) => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Results count */}
          <div className="mt-4 text-xs text-gray-600">
            Showing {filteredEntities.length} of {entities.length} facts
          </div>
        </div>

        {/* Error state */}
        {error && (
          <div className="brutal-box bg-red-50 p-6 mb-8">
            <p className="font-bold text-red-600">ERROR</p>
            <p className="text-sm">{error}</p>
          </div>
        )}

        {/* Empty state */}
        {entities.length === 0 && !error && (
          <div className="brutal-box brutal-shadow p-12 text-center">
            <h3 className="text-2xl mb-4">NO FACTS YET</h3>
            <p className="text-sm mb-6">
              Start building your knowledge base by adding experience through
              conversation, upload, or import
            </p>
            <button
              onClick={() => router.push('/dashboard')}
              className="brutal-btn brutal-btn-primary brutal-shadow"
            >
              Go to Dashboard
            </button>
          </div>
        )}

        {/* No results state */}
        {entities.length > 0 && filteredEntities.length === 0 && (
          <div className="brutal-box brutal-shadow p-12 text-center">
            <h3 className="text-2xl mb-4">NO MATCHING FACTS</h3>
            <p className="text-sm mb-6">Try adjusting your search or filter</p>
            <button
              onClick={() => {
                setSearchQuery('');
                setFilterType('all');
              }}
              className="brutal-btn brutal-btn-seafoam brutal-shadow"
            >
              Clear Filters
            </button>
          </div>
        )}

        {/* Facts list */}
        {filteredEntities.length > 0 && (
          <div className="space-y-4">
            {filteredEntities.map((entity) => (
              <FactCard
                key={entity.id}
                entity={entity}
                isConfirmed={true}
                onConfirm={() => {}} // No-op for confirmed entities
                onEdit={handleEdit}
                onDelete={handleDelete}
              />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
