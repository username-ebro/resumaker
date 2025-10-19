'use client';

import { useState } from 'react';
import { useToast } from './Toast';

interface JobData {
  title: string;
  company?: string;
  location?: string;
  url?: string;
  description: string;
  requirements?: string[];
  keywords?: string[];
  ats_system?: string;
  company_info?: {
    website?: string;
    linkedin?: string;
    values?: string[];
    about?: string;
  };
}

type JobFieldValue = string | string[] | JobData['company_info'];

interface JobConfirmationProps {
  jobData: JobData;
  onConfirm: (confirmedData: JobData) => void;
  onCancel: () => void;
  onEdit: (field: string, value: JobFieldValue) => void;
  loading?: boolean;
}

export default function JobConfirmation({
  jobData,
  onConfirm,
  onCancel,
  onEdit,
  loading = false
}: JobConfirmationProps) {
  const { showToast } = useToast();
  const [isEditing, setIsEditing] = useState<string | null>(null);
  const [editValue, setEditValue] = useState('');
  const [error, setError] = useState<string | null>(null);

  const startEdit = (field: string, currentValue: JobFieldValue) => {
    setIsEditing(field);
    setEditValue(typeof currentValue === 'string' ? currentValue : JSON.stringify(currentValue));
  };

  const saveEdit = (field: string) => {
    try {
      onEdit(field, editValue);
      setIsEditing(null);
      setError(null);
    } catch (err) {
      setError('Failed to save edit. Please try again.');
    }
  };

  const validateJobData = (): boolean => {
    // Validate job title
    if (!jobData.title || jobData.title.trim().length < 3) {
      showToast('Job title must be at least 3 characters', 'error');
      return false;
    }

    // Validate company if provided
    if (jobData.company && jobData.company.trim().length < 2) {
      showToast('Company name must be at least 2 characters', 'error');
      return false;
    }

    // Validate description
    if (!jobData.description || jobData.description.trim().length < 10) {
      showToast('Job description must be at least 10 characters', 'error');
      return false;
    }

    // Validate URL if provided
    if (jobData.url && !jobData.url.match(/^https?:\/\/.+/)) {
      showToast('Please enter a valid URL (starting with http:// or https://)', 'error');
      return false;
    }

    return true;
  };

  const handleConfirm = () => {
    try {
      setError(null);

      // Validate before confirming
      if (!validateJobData()) {
        return;
      }

      onConfirm(jobData);
    } catch (err) {
      setError('Failed to confirm. Please try again.');
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Step Indicator */}
      <div className="flex items-center justify-center gap-2 mb-6">
        <div className="flex items-center opacity-60">
          <div className="brutal-box w-8 h-8 flex items-center justify-center font-bold text-sm">1</div>
          <span className="ml-2 text-sm">Enter Job</span>
        </div>
        <div className="w-12 h-0.5 bg-black"></div>
        <div className="flex items-center">
          <div className="brutal-box brutal-btn-primary w-8 h-8 flex items-center justify-center font-bold text-sm">2</div>
          <span className="ml-2 text-sm font-bold">Review</span>
        </div>
        <div className="w-12 h-0.5 bg-gray-300"></div>
        <div className="flex items-center opacity-40">
          <div className="brutal-box w-8 h-8 flex items-center justify-center font-bold text-sm">3</div>
          <span className="ml-2 text-sm">Generate</span>
        </div>
      </div>

      <div className="brutal-box brutal-shadow p-6">
        <div className="brutal-box-seafoam p-4 mb-6">
          <h2 className="text-xl font-bold mb-2">📋 DOES THIS LOOK RIGHT?</h2>
          <p className="text-sm">Review the job details we extracted. Edit anything that's incorrect.</p>
        </div>

      {/* Error Display */}
      {error && (
        <div className="brutal-box bg-red-50 border-red-600 p-4 mb-4">
          <p className="text-sm font-bold uppercase mb-1">Error</p>
          <p className="text-sm">{error}</p>
        </div>
      )}

      {/* Loading Overlay */}
      {loading && (
        <div className="brutal-box bg-yellow-50 border-yellow-600 p-4 mb-4">
          <div className="flex items-center gap-3">
            <div className="cool-spinner h-6 w-6 border-2 border-black border-t-transparent rounded-full"></div>
            <div>
              <p className="text-sm font-bold uppercase">Generating Resume...</p>
              <p className="text-xs">This may take a minute while we optimize for ATS</p>
            </div>
          </div>
        </div>
      )}

      {/* Job Title & Company */}
      <div className="space-y-4">
        <div className="brutal-box p-4">
          {isEditing === 'title' ? (
            <div>
              <input
                type="text"
                value={editValue}
                onChange={(e) => setEditValue(e.target.value)}
                className="brutal-input w-full mb-2"
                placeholder="Job Title"
              />
              <div className="flex gap-2">
                <button onClick={() => setIsEditing(null)} className="brutal-btn text-xs px-2 py-1">
                  Cancel
                </button>
                <button onClick={() => saveEdit('title')} className="brutal-btn brutal-btn-primary text-xs px-2 py-1">
                  Save
                </button>
              </div>
            </div>
          ) : (
            <div className="flex justify-between items-start">
              <div>
                <p className="text-xs font-bold uppercase text-gray-600 mb-1">Job Title</p>
                <p className="font-bold text-lg">{jobData.title}</p>
              </div>
              <button
                onClick={() => startEdit('title', jobData.title)}
                className="brutal-btn text-xs px-2 py-1"
              >
                ✏️ Edit
              </button>
            </div>
          )}
        </div>

        {jobData.company ? (
          <div className="brutal-box p-4">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-xs font-bold uppercase text-gray-600 mb-1">Company</p>
                <p className="font-bold">{jobData.company}</p>
                {jobData.location && <p className="text-sm text-gray-600">📍 {jobData.location}</p>}
              </div>
            </div>
          </div>
        ) : (
          <div className="brutal-box bg-gray-50 p-4">
            <p className="text-xs text-gray-600">No company information available</p>
          </div>
        )}

        {/* Company Research */}
        {jobData.company_info && Object.keys(jobData.company_info).length > 0 ? (
          <div className="brutal-box brutal-box-seafoam p-4">
            <p className="text-xs font-bold uppercase mb-3">🔍 Company Research</p>
            <div className="space-y-2 text-sm">
              {jobData.company_info.website && (
                <p>🌐 <a href={jobData.company_info.website} target="_blank" rel="noopener noreferrer" className="underline">{jobData.company_info.website}</a></p>
              )}
              {jobData.company_info.linkedin && (
                <p>💼 <a href={jobData.company_info.linkedin} target="_blank" rel="noopener noreferrer" className="underline">LinkedIn</a></p>
              )}
              {jobData.company_info.about && (
                <div>
                  <p className="font-bold text-xs uppercase mt-2 mb-1">About</p>
                  <p className="text-xs">{jobData.company_info.about}</p>
                </div>
              )}
              {jobData.company_info.values && jobData.company_info.values.length > 0 && (
                <div>
                  <p className="font-bold text-xs uppercase mt-2 mb-1">Core Values</p>
                  <div className="flex gap-2 flex-wrap">
                    {jobData.company_info.values.map((value, i) => (
                      <span key={i} className="text-xs bg-white px-2 py-1 border-2 border-black">
                        {value}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="brutal-box bg-gray-50 p-4">
            <p className="text-xs font-bold uppercase mb-1">🔍 Company Research</p>
            <p className="text-xs text-gray-600">No additional company information found. Consider researching the company manually.</p>
          </div>
        )}

        {/* ATS Detection */}
        {jobData.ats_system && (
          <div className="brutal-box bg-yellow-50 border-yellow-600 p-4">
            <p className="text-xs font-bold uppercase mb-1">⚙️ ATS System Detected</p>
            <p className="font-bold">{jobData.ats_system}</p>
            <p className="text-xs mt-1">We'll optimize your resume for this system</p>
          </div>
        )}

        {/* Key Requirements */}
        {jobData.requirements && jobData.requirements.length > 0 ? (
          <div className="brutal-box p-4">
            <p className="text-xs font-bold uppercase mb-3">✅ Key Requirements</p>
            <div className="space-y-1">
              {jobData.requirements.slice(0, 5).map((req, i) => (
                <div key={i} className="flex items-start gap-2">
                  <span className="text-black">•</span>
                  <p className="text-sm">{req}</p>
                </div>
              ))}
              {jobData.requirements.length > 5 && (
                <p className="text-xs text-gray-600 mt-2">
                  + {jobData.requirements.length - 5} more requirements
                </p>
              )}
            </div>
          </div>
        ) : (
          <div className="brutal-box bg-gray-50 p-4">
            <p className="text-xs font-bold uppercase mb-1">✅ Key Requirements</p>
            <p className="text-xs text-gray-600">No specific requirements extracted. We'll match against the full description.</p>
          </div>
        )}

        {/* Important Keywords */}
        {jobData.keywords && jobData.keywords.length > 0 ? (
          <div className="brutal-box p-4">
            <p className="text-xs font-bold uppercase mb-2">🔑 Important Keywords</p>
            <p className="text-sm font-mono leading-relaxed">
              {jobData.keywords.join(', ')}
            </p>
          </div>
        ) : (
          <div className="brutal-box bg-gray-50 p-4">
            <p className="text-xs font-bold uppercase mb-1">🔑 Important Keywords</p>
            <p className="text-xs text-gray-600">No keywords extracted. We'll analyze the description for optimization.</p>
          </div>
        )}
      </div>

      {/* Actions */}
      <div className="flex gap-3 mt-6 pt-6 border-t-4 border-black">
        <button
          onClick={onCancel}
          disabled={loading}
          className="brutal-btn flex-1 disabled:opacity-50"
        >
          ← Go Back
        </button>
        <button
          onClick={handleConfirm}
          disabled={loading}
          className="brutal-btn brutal-btn-primary brutal-shadow flex-1 disabled:opacity-50 flex items-center justify-center gap-2"
        >
          {loading && (
            <div className="cool-spinner h-5 w-5 border-2 border-white border-t-transparent rounded-full"></div>
          )}
          {loading ? 'Creating...' : '✅ Looks Good - Create Resume'}
        </button>
      </div>
      </div>
    </div>
  );
}
