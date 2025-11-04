'use client'

import { useState } from 'react'
import Link from 'next/link'
import { Button, Card } from './ui'
import { getATSRecommendation, ATS_SYSTEMS } from '@/lib/ats-systems'

interface ATSDownloadModalProps {
  isOpen: boolean
  onClose: () => void
  onDownload: (format: 'pdf' | 'docx') => void
  format: 'pdf' | 'docx'
  atsSystemId?: string // Optional: If known, show ATS-specific tips
}

export default function ATSDownloadModal({ isOpen, onClose, onDownload, format, atsSystemId }: ATSDownloadModalProps) {
  if (!isOpen) return null

  const formatUpper = format.toUpperCase()
  const isDocx = format === 'docx'
  const atsSystem = atsSystemId ? ATS_SYSTEMS[atsSystemId] : null
  const recommendation = getATSRecommendation(atsSystemId)

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <Card variant="elevated" padding="lg" className="max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h2 className="text-2xl font-black uppercase mb-2">
              📄 Downloading {formatUpper}
            </h2>
            <p className="text-sm text-gray-600">
              {atsSystem ? `Optimized for ${atsSystem.name}` : 'Quick ATS tips for your resume'}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl leading-none"
          >
            ×
          </button>
        </div>

        {/* ATS-Specific Alert */}
        {atsSystem && (
          <Card variant="default" padding="sm" className="bg-purple-50 border-purple-600 mb-4">
            <p className="text-sm font-bold flex items-center gap-2">
              <span className="text-2xl">{atsSystem.emoji}</span>
              <span>Detected: {atsSystem.name} ({atsSystem.marketShare})</span>
            </p>
          </Card>
        )}

        {/* Format-specific guidance */}
        <Card
          variant={isDocx ? "seafoam" : "default"}
          padding="md"
          className={`mb-4 ${isDocx ? '' : 'border-2 border-gray-300'}`}
        >
          <div className="flex gap-3 items-start">
            {isDocx ? (
              <>
                <span className="text-3xl">✅</span>
                <div>
                  <h3 className="font-bold text-lg mb-1">Great choice for ATS!</h3>
                  <p className="text-sm">
                    DOCX is the safest format for online job applications.
                    98.4% of Fortune 500 companies use ATS systems, and Word files parse most reliably.
                  </p>
                </div>
              </>
            ) : (
              <>
                <span className="text-3xl">⚠️</span>
                <div>
                  <h3 className="font-bold text-lg mb-1">Good for humans, riskier for ATS</h3>
                  <p className="text-sm mb-2">
                    PDF works well with modern ATS, but older systems may struggle.
                    Use PDF for:
                  </p>
                  <ul className="text-sm space-y-1">
                    <li className="flex gap-2">
                      <span>•</span> Emailing recruiters directly
                    </li>
                    <li className="flex gap-2">
                      <span>•</span> Networking and LinkedIn
                    </li>
                    <li className="flex gap-2">
                      <span>•</span> When job posting specifically requests PDF
                    </li>
                  </ul>
                </div>
              </>
            )}
          </div>
        </Card>

        {/* Quick tips */}
        <div className="mb-4">
          <h3 className="font-bold text-sm uppercase mb-3 text-gray-700">
            🚀 {atsSystem ? `${atsSystem.name} Tips` : 'Quick ATS Tips'}
          </h3>
          <div className="space-y-2 text-sm">
            {recommendation.tips.map((tip, i) => (
              <Card key={i} variant="default" padding="sm" className="bg-blue-50 border-blue-200">
                <p>{tip}</p>
              </Card>
            ))}
          </div>
        </div>

        {/* Pro tip */}
        <Card variant="default" padding="sm" className="bg-yellow-50 border-yellow-600 mb-4">
          <p className="text-sm font-bold">
            💡 <strong>Pro Tip:</strong> Keep both DOCX and PDF versions ready.
            Use DOCX for job applications, PDF for networking.
          </p>
        </Card>

        {/* Learn more link */}
        <div className="text-center mb-4 space-y-2">
          {atsSystem && (
            <Link
              href={`/tips/ats/${atsSystem.id}`}
              className="block text-sm text-purple-600 hover:underline font-semibold"
              target="_blank"
            >
              🎯 Full {atsSystem.name} Guide →
            </Link>
          )}
          <Link
            href="/tips/ats-optimization"
            className="block text-sm text-blue-600 hover:underline font-semibold"
            target="_blank"
          >
            📚 General ATS optimization guide →
          </Link>
          <Link
            href="/tips/ats-detector"
            className="block text-sm text-gray-600 hover:underline font-semibold"
            target="_blank"
          >
            🔍 ATS Detector Tool →
          </Link>
        </div>

        {/* Action buttons */}
        <div className="flex gap-3 justify-end">
          <Button
            variant="secondary"
            size="md"
            onClick={onClose}
          >
            Cancel
          </Button>
          <Button
            variant="primary"
            size="md"
            onClick={() => {
              onDownload(format)
              onClose()
            }}
          >
            Download {formatUpper}
          </Button>
        </div>
      </Card>
    </div>
  )
}
