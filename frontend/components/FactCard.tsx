'use client';

import { useState } from 'react';
import { KnowledgeEntity } from '@/lib/api/knowledge';

interface FactCardProps {
  entity: KnowledgeEntity;
  isConfirmed: boolean;
  onConfirm: (id: string) => void;
  onEdit: (id: string, updates: Partial<KnowledgeEntity>) => void;
  onDelete: (id: string) => void;
  isNested?: boolean;
}

export default function FactCard({
  entity,
  isConfirmed,
  onConfirm,
  onEdit,
  onDelete,
  isNested = false,
}: FactCardProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedTitle, setEditedTitle] = useState(entity.title);
  const [editedDescription, setEditedDescription] = useState(entity.description || '');
  const [editedStartDate, setEditedStartDate] = useState(entity.start_date || '');
  const [editedEndDate, setEditedEndDate] = useState(entity.end_date || '');
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const handleSaveEdit = () => {
    onEdit(entity.id, {
      title: editedTitle,
      description: editedDescription,
      start_date: editedStartDate || undefined,
      end_date: editedEndDate || undefined,
    });
    setIsEditing(false);
  };

  const handleCancelEdit = () => {
    setEditedTitle(entity.title);
    setEditedDescription(entity.description || '');
    setEditedStartDate(entity.start_date || '');
    setEditedEndDate(entity.end_date || '');
    setIsEditing(false);
  };

  const handleDelete = () => {
    onDelete(entity.id);
    setShowDeleteConfirm(false);
  };

  // Confidence score color
  const getConfidenceColor = () => {
    if (entity.confidence_score >= 0.85) return 'bg-black';
    if (entity.confidence_score >= 0.7) return 'bg-yellow-600';
    return 'bg-red-600';
  };

  const getConfidenceLabel = () => {
    if (entity.confidence_score >= 0.85) return 'HIGH';
    if (entity.confidence_score >= 0.7) return 'MEDIUM';
    return 'LOW';
  };

  return (
    <div
      className={`brutal-box ${
        isConfirmed ? 'brutal-box-seafoam' : 'bg-white'
      } p-3 ${isNested ? 'ml-6 mt-2' : 'mb-2'}`}
    >
      {isEditing ? (
        /* EDITING MODE - Full Form */
        <div className="space-y-2">
          <input
            type="text"
            value={editedTitle}
            onChange={(e) => setEditedTitle(e.target.value)}
            className="brutal-input w-full text-sm"
            placeholder="Title"
          />
          <textarea
            value={editedDescription}
            onChange={(e) => setEditedDescription(e.target.value)}
            className="brutal-input w-full h-20 text-sm"
            placeholder="Description (optional)"
          />
          {(entity.start_date || entity.end_date) && (
            <div className="flex gap-2">
              <input
                type="text"
                value={editedStartDate}
                onChange={(e) => setEditedStartDate(e.target.value)}
                className="brutal-input w-full text-xs"
                placeholder="Start (YYYY-MM)"
              />
              <input
                type="text"
                value={editedEndDate}
                onChange={(e) => setEditedEndDate(e.target.value)}
                className="brutal-input w-full text-xs"
                placeholder="End (YYYY-MM)"
              />
            </div>
          )}
          <div className="flex gap-2 justify-end">
            <button onClick={handleCancelEdit} className="brutal-btn text-xs px-2 py-1">
              Cancel
            </button>
            <button onClick={handleSaveEdit} className="brutal-btn brutal-btn-primary text-xs px-2 py-1">
              Save
            </button>
          </div>
        </div>
      ) : showDeleteConfirm ? (
        /* DELETE CONFIRMATION */
        <div className="bg-red-50 p-2 -m-3">
          <p className="text-xs font-bold mb-2">Delete this fact?</p>
          <div className="flex gap-2">
            <button
              onClick={() => setShowDeleteConfirm(false)}
              className="brutal-btn text-xs px-2 py-1 flex-1"
            >
              Cancel
            </button>
            <button
              onClick={handleDelete}
              className="brutal-btn text-xs px-2 py-1 flex-1 bg-red-600 border-red-600 text-white"
            >
              Delete
            </button>
          </div>
        </div>
      ) : (
        /* COMPACT VIEW */
        <div className="flex items-start gap-2">
          {/* Checkbox */}
          <input
            type="checkbox"
            checked={isConfirmed}
            onChange={() => onConfirm(entity.id)}
            className="mt-0.5 h-4 w-4 cursor-pointer flex-shrink-0"
          />

          {/* Content */}
          <div className="flex-1 min-w-0">
            <div className="flex items-baseline gap-2 flex-wrap">
              <h4 className="font-bold text-sm">{entity.title}</h4>
              <span className="text-xs uppercase text-gray-500">
                {entity.entity_type.replace('_', ' ')}
              </span>
              {entity.confidence_score < 0.85 && (
                <span className={`text-xs font-bold px-1 ${
                  entity.confidence_score >= 0.7 ? 'text-yellow-600' : 'text-red-600'
                }`}>
                  {getConfidenceLabel()}
                </span>
              )}
            </div>
            {entity.description && (
              <p className="text-xs text-gray-700 mt-1 line-clamp-2">{entity.description}</p>
            )}
            {(entity.start_date || entity.end_date) && (
              <p className="text-xs text-gray-500 mt-0.5">
                {entity.start_date} {entity.end_date ? `→ ${entity.end_date}` : ''}
              </p>
            )}
          </div>

          {/* Actions */}
          <div className="flex gap-1 flex-shrink-0">
            <button
              onClick={() => setIsEditing(true)}
              className="brutal-btn text-xs px-2 py-0.5 h-6"
              title="Edit"
            >
              ✏️
            </button>
            <button
              onClick={() => setShowDeleteConfirm(true)}
              className="brutal-btn text-xs px-2 py-0.5 h-6 border-red-600 text-red-600"
              title="Delete"
            >
              🗑️
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
