'use client'

import { useState } from 'react'

interface Flag {
  id: string
  section: string
  claim_text: string
  context?: string
  flag_reason: string
  severity: 'low' | 'medium' | 'high'
  explanation: string
  suggested_fix: string
  resolved: boolean
  resolution_notes?: string
}

interface TruthCheckReviewProps {
  flags: Flag[]
  onResolveFlag: (flagId: string, resolution: string) => Promise<void>
}

export default function TruthCheckReview({ flags, onResolveFlag }: TruthCheckReviewProps) {
  const [resolving, setResolving] = useState<string | null>(null)
  const [resolutionNotes, setResolutionNotes] = useState<{ [key: string]: string }>({})
  const [filter, setFilter] = useState<'all' | 'unresolved' | 'high' | 'medium' | 'low'>('unresolved')

  const unresolvedFlags = flags.filter(f => !f.resolved)
  const resolvedFlags = flags.filter(f => f.resolved)

  const filteredFlags = (() => {
    switch (filter) {
      case 'unresolved':
        return unresolvedFlags
      case 'high':
        return unresolvedFlags.filter(f => f.severity === 'high')
      case 'medium':
        return unresolvedFlags.filter(f => f.severity === 'medium')
      case 'low':
        return unresolvedFlags.filter(f => f.severity === 'low')
      default:
        return flags
    }
  })()

  const handleResolve = async (flagId: string) => {
    const notes = resolutionNotes[flagId]
    if (!notes || notes.trim() === '') {
      alert('Please add resolution notes')
      return
    }

    setResolving(flagId)
    try {
      await onResolveFlag(flagId, notes)
      setResolutionNotes({ ...resolutionNotes, [flagId]: '' })
    } catch (error) {
      alert('Failed to resolve flag')
    } finally {
      setResolving(null)
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-300'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300'
      case 'low':
        return 'bg-blue-100 text-blue-800 border-blue-300'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300'
    }
  }

  const getSeverityBadge = (severity: string) => {
    const colors = {
      high: 'bg-red-600 text-white',
      medium: 'bg-yellow-500 text-white',
      low: 'bg-blue-500 text-white'
    }
    return colors[severity as keyof typeof colors] || 'bg-gray-500 text-white'
  }

  const getReasonLabel = (reason: string) => {
    const labels: { [key: string]: string } = {
      no_evidence: 'No Evidence',
      weak_evidence: 'Weak Evidence',
      date_mismatch: 'Date Mismatch',
      quantification_unsupported: 'Quantification Unsupported',
      skill_level_mismatch: 'Skill Level Mismatch',
      conflicting_information: 'Conflicting Information'
    }
    return labels[reason] || reason
  }

  return (
    <div className="max-w-5xl mx-auto p-6">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold mb-2">Truth Check Review</h1>
        <p className="text-gray-600">
          Review flagged claims and ensure resume accuracy
        </p>
      </div>

      {/* Stats Summary */}
      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-white rounded-lg shadow p-4">
          <div className="text-2xl font-bold text-gray-900">{flags.length}</div>
          <div className="text-sm text-gray-600">Total Checks</div>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <div className="text-2xl font-bold text-red-600">
            {unresolvedFlags.filter(f => f.severity === 'high').length}
          </div>
          <div className="text-sm text-gray-600">High Severity</div>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <div className="text-2xl font-bold text-yellow-600">
            {unresolvedFlags.filter(f => f.severity === 'medium').length}
          </div>
          <div className="text-sm text-gray-600">Medium Severity</div>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <div className="text-2xl font-bold text-green-600">{resolvedFlags.length}</div>
          <div className="text-sm text-gray-600">Resolved</div>
        </div>
      </div>

      {/* Filters */}
      <div className="mb-6 flex gap-2">
        {['all', 'unresolved', 'high', 'medium', 'low'].map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f as any)}
            className={`px-4 py-2 rounded capitalize ${
              filter === f
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {f}
          </button>
        ))}
      </div>

      {/* Flags List */}
      {filteredFlags.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-8 text-center">
          <div className="text-gray-400 text-lg">
            ✓ {filter === 'all' ? 'No flags found' : `No ${filter} flags`}
          </div>
          <p className="text-gray-500 mt-2">
            {filter === 'unresolved'
              ? 'All claims have been verified!'
              : 'Try adjusting your filter'}
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredFlags.map((flag) => (
            <div
              key={flag.id}
              className={`bg-white rounded-lg shadow border-l-4 p-6 ${getSeverityColor(flag.severity)}`}
            >
              {/* Header */}
              <div className="flex justify-between items-start mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getSeverityBadge(flag.severity)}`}>
                      {flag.severity.toUpperCase()}
                    </span>
                    <span className="px-3 py-1 bg-gray-100 rounded-full text-xs font-medium">
                      {getReasonLabel(flag.flag_reason)}
                    </span>
                    <span className="text-sm text-gray-500">
                      Section: {flag.section}
                    </span>
                  </div>
                </div>
                {flag.resolved && (
                  <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-xs font-semibold">
                    ✓ RESOLVED
                  </span>
                )}
              </div>

              {/* Claim */}
              <div className="mb-4">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Flagged Claim:
                </label>
                <div className="bg-gray-50 p-3 rounded border border-gray-200">
                  <p className="text-gray-900 italic">"{flag.claim_text}"</p>
                  {flag.context && (
                    <p className="text-sm text-gray-600 mt-2">
                      <strong>Context:</strong> {flag.context}
                    </p>
                  )}
                </div>
              </div>

              {/* Explanation */}
              <div className="mb-4">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Why This Was Flagged:
                </label>
                <p className="text-gray-700">{flag.explanation}</p>
              </div>

              {/* Suggestion */}
              <div className="mb-4">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Suggested Fix:
                </label>
                <p className="text-gray-700">{flag.suggested_fix}</p>
              </div>

              {/* Resolution Section */}
              {!flag.resolved ? (
                <div className="border-t pt-4">
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Resolution Notes:
                  </label>
                  <textarea
                    value={resolutionNotes[flag.id] || ''}
                    onChange={(e) => setResolutionNotes({ ...resolutionNotes, [flag.id]: e.target.value })}
                    className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 mb-3"
                    rows={3}
                    placeholder="Explain how you resolved this issue (e.g., 'Updated bullet with actual metrics from Q2 report' or 'Removed claim - not supported by evidence')"
                  />
                  <button
                    onClick={() => handleResolve(flag.id)}
                    disabled={resolving === flag.id}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400"
                  >
                    {resolving === flag.id ? 'Resolving...' : 'Mark as Resolved'}
                  </button>
                </div>
              ) : (
                <div className="border-t pt-4 bg-green-50 -mx-6 -mb-6 px-6 py-4 rounded-b-lg">
                  <label className="block text-sm font-semibold text-green-800 mb-2">
                    Resolution:
                  </label>
                  <p className="text-green-900">{flag.resolution_notes}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Action Buttons */}
      {unresolvedFlags.length > 0 && (
        <div className="mt-8 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-yellow-800">
                {unresolvedFlags.filter(f => f.severity === 'high').length > 0
                  ? 'High priority flags require attention'
                  : 'Review remaining flags before finalizing'}
              </h3>
              <p className="mt-2 text-sm text-yellow-700">
                Resolve all medium and high severity flags to ensure resume accuracy and integrity.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
