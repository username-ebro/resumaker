'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { knowledgeApi, KnowledgeEntity, GroupedEntities } from '@/lib/api/knowledge';
import FactCard from './FactCard';
import { useToast } from './Toast';

interface ConfirmationScreenProps {
  userId: string;
}

export default function ConfirmationScreen({ userId }: ConfirmationScreenProps) {
  const router = useRouter();
  const { showToast } = useToast();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [entities, setEntities] = useState<KnowledgeEntity[]>([]);
  const [groupedEntities, setGroupedEntities] = useState<Record<string, KnowledgeEntity[]>>({});
  const [confirmedIds, setConfirmedIds] = useState<Set<string>>(new Set());

  // Fetch pending entities on mount
  useEffect(() => {
    fetchPendingEntities();
  }, [userId]);

  const fetchPendingEntities = async () => {
    setLoading(true);
    setError('');

    try {
      const data = await knowledgeApi.getPending(userId);
      setEntities(data.entities);
      setGroupedEntities(data.grouped_by_type);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Failed to load entities');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleConfirm = (id: string) => {
    setConfirmedIds((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(id)) {
        newSet.delete(id);
      } else {
        newSet.add(id);
      }
      return newSet;
    });
  };

  const handleConfirmAll = () => {
    setConfirmedIds(new Set(entities.map((e) => e.id)));
  };

  const handleEdit = async (id: string, updates: Partial<KnowledgeEntity>) => {
    try {
      const { entity } = await knowledgeApi.updateEntity(id, updates);

      // Update local state
      setEntities((prev) =>
        prev.map((e) => (e.id === id ? { ...e, ...updates } : e))
      );

      // Update grouped entities
      setGroupedEntities((prev) => {
        const newGrouped = { ...prev };
        Object.keys(newGrouped).forEach((key) => {
          newGrouped[key] = newGrouped[key].map((e: KnowledgeEntity) =>
            e.id === id ? { ...e, ...updates } : e
          );
        });
        return newGrouped;
      });
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

      // Remove from grouped entities
      setGroupedEntities((prev) => {
        const newGrouped = { ...prev };
        Object.keys(newGrouped).forEach((key) => {
          newGrouped[key] = newGrouped[key].filter((e: KnowledgeEntity) => e.id !== id);
        });
        return newGrouped;
      });

      // Remove from confirmed IDs
      setConfirmedIds((prev) => {
        const newSet = new Set(prev);
        newSet.delete(id);
        return newSet;
      });
      showToast('Fact deleted successfully', 'success');
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error';
      showToast(`Failed to delete: ${message}`, 'error');
    }
  };

  const handleSaveAndContinue = async () => {
    if (confirmedIds.size === 0) {
      showToast('Please confirm at least one fact before continuing', 'error');
      return;
    }

    setSaving(true);

    try {
      await knowledgeApi.confirm(userId, Array.from(confirmedIds));
      router.push('/dashboard');
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error';
      showToast(`Failed to save: ${message}`, 'error');
    } finally {
      setSaving(false);
    }
  };

  // Entity type metadata (maps API entity_type to display info)
  const entityTypeInfo: Record<string, { emoji: string; label: string }> = {
    job: { emoji: '🏢', label: 'WORK EXPERIENCE' },
    job_detail: { emoji: '📋', label: 'JOB DETAILS' },
    skill: { emoji: '💻', label: 'SKILLS' },
    project: { emoji: '🚀', label: 'PROJECTS' },
    education: { emoji: '🎓', label: 'EDUCATION' },
  };

  // Loading state
  if (loading) {
    return (
      <div className="brutal-box brutal-shadow p-12 text-center">
        <div className="cool-spinner h-12 w-12 border-4 border-black border-t-transparent rounded-full mx-auto mb-4"></div>
        <p className="text-sm font-bold uppercase">Loading your facts...</p>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="brutal-box bg-red-50 p-6">
        <p className="font-bold text-red-600">ERROR</p>
        <p className="text-sm">{error}</p>
        <button
          onClick={fetchPendingEntities}
          className="brutal-btn brutal-btn-primary brutal-shadow mt-4"
        >
          Try Again
        </button>
      </div>
    );
  }

  // Empty state
  if (entities.length === 0) {
    return (
      <div className="brutal-box brutal-shadow p-12 text-center">
        <h3 className="text-2xl mb-4">NO FACTS TO CONFIRM</h3>
        <p className="text-sm mb-6">
          Add your experience through conversation, upload, or import first
        </p>
        <button
          onClick={() => router.push('/dashboard')}
          className="brutal-btn brutal-btn-primary brutal-shadow"
        >
          Back to Dashboard
        </button>
      </div>
    );
  }

  return (
    <div className="brutal-box brutal-shadow p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl mb-3">HERE'S WHAT I LEARNED ABOUT YOU</h1>
        <p className="text-sm mb-6">
          Review each fact. Confirm what's correct, edit what needs fixing.
        </p>

        {/* Action buttons */}
        <div className="flex gap-3 flex-wrap">
          <button
            onClick={handleConfirmAll}
            className="brutal-btn brutal-btn-seafoam brutal-shadow"
          >
            ✓ Confirm All ({entities.length})
          </button>
          <button
            onClick={handleSaveAndContinue}
            disabled={confirmedIds.size === 0 || saving}
            className="brutal-btn brutal-btn-primary brutal-shadow disabled:opacity-50 flex items-center gap-2"
          >
            {saving && (
              <div className="cool-spinner h-5 w-5 border-2 border-white border-t-transparent rounded-full"></div>
            )}
            {saving
              ? 'Saving...'
              : `Save & Continue (${confirmedIds.size} confirmed)`}
          </button>
        </div>
      </div>

      {/* Entity sections */}
      <div className="space-y-8">
        {Object.entries(groupedEntities).map(([type, entitiesOfType]) => {
          if (!entitiesOfType || entitiesOfType.length === 0) return null;

          const info = entityTypeInfo[type] || { emoji: '📄', label: type.toUpperCase() };

          return (
            <section key={type}>
              <div className="brutal-box-seafoam p-3 mb-4">
                <h2 className="text-lg">
                  {info.emoji} {info.label} ({entitiesOfType.length})
                </h2>
              </div>

              <div className="space-y-3">
                {entitiesOfType.map((entity) => (
                  <FactCard
                    key={entity.id}
                    entity={entity}
                    isConfirmed={confirmedIds.has(entity.id)}
                    onConfirm={handleConfirm}
                    onEdit={handleEdit}
                    onDelete={handleDelete}
                  />
                ))}
              </div>
            </section>
          );
        })}
      </div>

      {/* Bottom actions */}
      <div className="mt-8 pt-6 border-t-2 border-black">
        <div className="flex gap-3 justify-end">
          <button
            onClick={() => router.push('/dashboard')}
            className="brutal-btn brutal-shadow"
          >
            Cancel
          </button>
          <button
            onClick={handleSaveAndContinue}
            disabled={confirmedIds.size === 0 || saving}
            className="brutal-btn brutal-btn-primary brutal-shadow disabled:opacity-50 flex items-center gap-2"
          >
            {saving && (
              <div className="cool-spinner h-5 w-5 border-2 border-white border-t-transparent rounded-full"></div>
            )}
            {saving
              ? 'Saving...'
              : `Save & Continue (${confirmedIds.size} confirmed)`}
          </button>
        </div>
      </div>
    </div>
  );
}
