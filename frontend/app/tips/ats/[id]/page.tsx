'use client'

import { use } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button, Card, Badge } from '@/components/ui'
import { ATS_SYSTEMS, getDifficultyColor, getDifficultyLabel, getATSRecommendation } from '@/lib/ats-systems'

export default function ATSGuidePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params)
  const router = useRouter()
  const system = ATS_SYSTEMS[id]

  if (!system) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card variant="elevated" padding="lg" className="text-center">
          <h2 className="text-2xl font-black mb-3">ATS System Not Found</h2>
          <p className="text-gray-600 mb-4">We don't have information about this ATS system yet.</p>
          <Button variant="primary" size="md" onClick={() => router.push('/tips/ats-detector')}>
            ← Back to ATS Detector
          </Button>
        </Card>
      </div>
    )
  }

  const recommendation = getATSRecommendation(system.id)

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-6 py-12">
        {/* Header */}
        <div className="mb-8 flex gap-3">
          <Button
            variant="secondary"
            size="sm"
            onClick={() => router.push('/tips/ats-detector')}
          >
            ← All Systems
          </Button>
          <Button
            variant="secondary"
            size="sm"
            onClick={() => router.push('/tips/ats-optimization')}
          >
            General ATS Tips
          </Button>
        </div>

        {/* System Overview */}
        <div className="mb-8">
          <div className="flex items-center gap-4 mb-4">
            <span className="text-6xl">{system.emoji}</span>
            <div className="flex-1">
              <h1 className="text-4xl font-black tracking-tight mb-2">
                {system.name}
              </h1>
              <div className="flex gap-2">
                <Badge variant="default" size="md">
                  {system.marketShare}
                </Badge>
                <Badge
                  variant={
                    system.difficulty === 'easy' ? 'success' :
                    system.difficulty === 'medium' ? 'warning' :
                    system.difficulty === 'hard' ? 'warning' : 'default'
                  }
                  size="md"
                >
                  {getDifficultyLabel(system.difficulty)} Difficulty
                </Badge>
                <Badge variant="info" size="md">
                  {system.formatPreference === 'both' ? 'PDF/DOCX' : system.formatPreference.toUpperCase()}
                </Badge>
              </div>
            </div>
          </div>
          <p className="text-lg text-gray-700">{system.bestFor}</p>
        </div>

        {/* URL Pattern */}
        <Card variant="default" padding="md" className="mb-6 bg-gray-100">
          <p className="text-sm font-bold mb-2 text-gray-700">🔗 URL Pattern</p>
          <code className="block bg-white px-3 py-2 rounded border border-gray-300 text-sm">
            {system.exampleURL}
          </code>
          <p className="text-xs text-gray-600 mt-2">
            Look for <strong>{system.urlPattern}</strong> in job posting URLs
          </p>
        </Card>

        {/* Format Recommendation */}
        <Card variant="elevated" padding="lg" className="mb-6">
          <h2 className="text-2xl font-black mb-4 uppercase">📄 Format Recommendation</h2>

          <Card variant="seafoam" padding="md" className="mb-4">
            <p className="font-bold text-lg mb-2">
              Use <span className="uppercase">{recommendation.format}</span> format
            </p>
            <p className="text-sm">{recommendation.reasoning}</p>
          </Card>

          <div className="grid md:grid-cols-3 gap-3 text-sm">
            <Card variant="default" padding="sm">
              <p className="font-bold mb-1">Parsing Quality</p>
              <p className="capitalize">{system.parsingQuality}</p>
            </Card>
            <Card variant="default" padding="sm">
              <p className="font-bold mb-1">Creative Formatting</p>
              <p>{system.allowsCreativeFormatting ? '✅ Allowed' : '❌ Rejected'}</p>
            </Card>
            <Card variant="default" padding="sm">
              <p className="font-bold mb-1">Keyword Matching</p>
              <p className="capitalize">{system.keywordMatching.replace('-', ' ')}</p>
            </Card>
          </div>
        </Card>

        {/* Optimization Tips */}
        <Card variant="elevated" padding="lg" className="mb-6">
          <h2 className="text-2xl font-black mb-4 uppercase">✅ Optimization Tips</h2>
          <p className="text-sm text-gray-600 mb-4">
            Follow these specific strategies to maximize your success rate with {system.name}
          </p>

          <div className="space-y-3">
            {system.optimizationTips.map((tip, i) => (
              <Card key={i} variant="default" padding="sm" className="bg-green-50 border-green-200">
                <p className="text-sm flex gap-3">
                  <span className="text-green-600 font-bold text-lg">{i + 1}</span>
                  <span>{tip}</span>
                </p>
              </Card>
            ))}
          </div>
        </Card>

        {/* Unique Quirks */}
        <Card variant="elevated" padding="lg" className="mb-6">
          <h2 className="text-2xl font-black mb-4 uppercase">🔍 Unique Quirks</h2>
          <p className="text-sm text-gray-600 mb-4">
            Things you should know about {system.name} that make it different from other ATS platforms
          </p>

          <div className="space-y-3">
            {system.uniqueQuirks.map((quirk, i) => (
              <Card key={i} variant="default" padding="sm" className="bg-blue-50 border-blue-200">
                <p className="text-sm flex gap-3">
                  <span className="text-blue-600 text-lg">•</span>
                  <span>{quirk}</span>
                </p>
              </Card>
            ))}
          </div>
        </Card>

        {/* Common Complaints */}
        <Card variant="elevated" padding="lg" className="mb-6">
          <h2 className="text-2xl font-black mb-4 uppercase">⚠️ Common Complaints</h2>
          <p className="text-sm text-gray-600 mb-4">
            What job seekers commonly struggle with when applying through {system.name}
          </p>

          <div className="space-y-3">
            {system.commonComplaints.map((complaint, i) => (
              <Card key={i} variant="default" padding="sm" className="bg-yellow-50 border-yellow-200">
                <p className="text-sm flex gap-3">
                  <span className="text-yellow-600 text-lg">⚠</span>
                  <span>{complaint}</span>
                </p>
              </Card>
            ))}
          </div>
        </Card>

        {/* Quick Reference */}
        <Card variant="default" padding="lg" className="bg-gradient-to-r from-blue-50 to-purple-50 border-2 border-blue-600">
          <h2 className="text-xl font-black mb-4 uppercase">📋 Quick Reference</h2>
          <div className="grid md:grid-cols-2 gap-4 text-sm">
            <div>
              <p className="font-bold mb-2">DO:</p>
              <ul className="space-y-1">
                <li className="flex gap-2">
                  <span className="text-green-600">✓</span>
                  <span>Use {recommendation.format.toUpperCase()} format</span>
                </li>
                <li className="flex gap-2">
                  <span className="text-green-600">✓</span>
                  <span>Standard section headings</span>
                </li>
                <li className="flex gap-2">
                  <span className="text-green-600">✓</span>
                  <span>Simple, single-column layout</span>
                </li>
                <li className="flex gap-2">
                  <span className="text-green-600">✓</span>
                  <span>Keyword optimize from job description</span>
                </li>
              </ul>
            </div>
            <div>
              <p className="font-bold mb-2">DON'T:</p>
              <ul className="space-y-1">
                <li className="flex gap-2">
                  <span className="text-red-600">✗</span>
                  <span>Use tables or columns</span>
                </li>
                <li className="flex gap-2">
                  <span className="text-red-600">✗</span>
                  <span>Add graphics or images</span>
                </li>
                <li className="flex gap-2">
                  <span className="text-red-600">✗</span>
                  <span>Creative section headings</span>
                </li>
                <li className="flex gap-2">
                  <span className="text-red-600">✗</span>
                  <span>Put info in headers/footers</span>
                </li>
              </ul>
            </div>
          </div>
        </Card>

        {/* Footer Navigation */}
        <div className="mt-8 flex gap-3 justify-center">
          <Button variant="secondary" size="md" onClick={() => router.push('/tips/ats-detector')}>
            ← ATS Detector
          </Button>
          <Button variant="primary" size="md" onClick={() => router.push('/resumes')}>
            Optimize My Resume →
          </Button>
        </div>
      </div>
    </div>
  )
}
