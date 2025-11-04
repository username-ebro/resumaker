'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button, Card, Badge } from '@/components/ui'
import { ATS_SYSTEMS, detectATSFromURL, getDifficultyColor, getDifficultyLabel, getATSRecommendation } from '@/lib/ats-systems'

export default function ATSDetectorPage() {
  const router = useRouter()
  const [url, setUrl] = useState('')
  const [detectedATS, setDetectedATS] = useState<any>(null)
  const [showAllSystems, setShowAllSystems] = useState(false)

  const handleDetect = () => {
    const detected = detectATSFromURL(url)
    setDetectedATS(detected)
  }

  const recommendation = detectedATS ? getATSRecommendation(detectedATS.id) : null

  const allSystems = Object.values(ATS_SYSTEMS).sort((a, b) => {
    // Sort by market share (extract percentage if available)
    const getShare = (str: string) => {
      const match = str.match(/(\d+\.?\d*)%/)
      return match ? parseFloat(match[1]) : 0
    }
    return getShare(b.marketShare) - getShare(a.marketShare)
  })

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-5xl mx-auto px-6 py-12">
        {/* Header */}
        <div className="mb-8">
          <Button
            variant="secondary"
            size="sm"
            onClick={() => router.back()}
          >
            ← Back
          </Button>
        </div>

        <div className="mb-8">
          <h1 className="text-4xl font-black tracking-tight mb-3">
            🔍 ATS DETECTOR
          </h1>
          <p className="text-lg text-gray-600">
            Find out which Applicant Tracking System a company uses and get specific optimization tips
          </p>
        </div>

        {/* Detection Tool */}
        <Card variant="elevated" padding="lg" className="mb-8">
          <h2 className="text-xl font-bold mb-4">Paste a Job URL</h2>
          <p className="text-sm text-gray-600 mb-4">
            Enter the URL from a job posting to detect which ATS system the company uses
          </p>

          <div className="flex gap-3 mb-4">
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://company.wd5.myworkdayjobs.com/careers/job..."
              className="flex-1 px-4 py-3 border-2 border-black rounded-none focus:outline-none focus:ring-2 focus:ring-blue-600"
              onKeyPress={(e) => e.key === 'Enter' && handleDetect()}
            />
            <Button
              variant="primary"
              size="md"
              onClick={handleDetect}
              disabled={!url}
            >
              Detect ATS
            </Button>
          </div>

          {/* Detection Result */}
          {detectedATS && (
            <Card variant="seafoam" padding="md" className="mb-4">
              <div className="flex items-start gap-4">
                <span className="text-5xl">{detectedATS.emoji}</span>
                <div className="flex-1">
                  <h3 className="text-2xl font-black mb-2">{detectedATS.name}</h3>
                  <div className="flex gap-2 mb-3">
                    <Badge variant="default" size="sm">
                      {detectedATS.marketShare}
                    </Badge>
                    <Badge
                      variant={
                        detectedATS.difficulty === 'easy' ? 'success' :
                        detectedATS.difficulty === 'medium' ? 'warning' :
                        detectedATS.difficulty === 'hard' ? 'warning' : 'default'
                      }
                      size="sm"
                    >
                      {getDifficultyLabel(detectedATS.difficulty)} Difficulty
                    </Badge>
                  </div>
                  <p className="text-sm text-gray-700 mb-3">{detectedATS.bestFor}</p>

                  <Link
                    href={`/tips/ats/${detectedATS.id}`}
                    className="text-sm font-bold text-blue-600 hover:underline"
                  >
                    → View Full {detectedATS.name} Guide
                  </Link>
                </div>
              </div>
            </Card>
          )}

          {detectedATS === null && url && (
            <Card variant="default" padding="sm" className="bg-yellow-50 border-yellow-600">
              <p className="text-sm font-bold">
                ⚠️ Could not detect ATS from this URL. Try copying the URL from the job application page, or browse all systems below.
              </p>
            </Card>
          )}

          {/* Recommendation */}
          {recommendation && (
            <div className="mt-4">
              <h4 className="font-bold text-sm uppercase mb-2 text-gray-700">📄 Format Recommendation</h4>
              <Card variant="default" padding="sm" className="bg-blue-50 border-blue-600 mb-3">
                <p className="text-sm font-bold">
                  Use <span className="uppercase">{recommendation.format}</span> format
                </p>
                <p className="text-sm mt-1">{recommendation.reasoning}</p>
              </Card>

              <h4 className="font-bold text-sm uppercase mb-2 text-gray-700">💡 Top Optimization Tips</h4>
              <div className="space-y-2">
                {recommendation.tips.map((tip, i) => (
                  <Card key={i} variant="default" padding="sm" className="bg-green-50 border-green-200">
                    <p className="text-sm flex gap-2">
                      <span className="text-green-600 font-bold">{i + 1}.</span>
                      <span>{tip}</span>
                    </p>
                  </Card>
                ))}
              </div>
            </div>
          )}
        </Card>

        {/* Common URL Patterns */}
        <Card variant="elevated" padding="lg" className="mb-8">
          <h2 className="text-xl font-bold mb-4">🔗 Common URL Patterns</h2>
          <p className="text-sm text-gray-600 mb-4">
            Look for these patterns in job posting URLs to identify the ATS
          </p>

          <div className="grid md:grid-cols-2 gap-3">
            {allSystems.slice(0, 6).map((system) => (
              <Card key={system.id} variant="default" padding="sm" className="hover:border-blue-600 transition-colors">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{system.emoji}</span>
                  <div className="flex-1 min-w-0">
                    <p className="font-bold text-sm truncate">{system.name}</p>
                    <code className="text-xs text-gray-600 block truncate">
                      {system.urlPattern}
                    </code>
                  </div>
                </div>
              </Card>
            ))}
          </div>

          <div className="mt-4 text-center">
            <button
              onClick={() => setShowAllSystems(!showAllSystems)}
              className="text-sm text-blue-600 hover:underline font-semibold"
            >
              {showAllSystems ? '↑ Show Less' : '↓ Show All Systems'}
            </button>
          </div>
        </Card>

        {/* All ATS Systems */}
        {showAllSystems && (
          <Card variant="elevated" padding="lg" className="mb-8">
            <h2 className="text-xl font-bold mb-4">📊 All Major ATS Systems</h2>

            <div className="grid gap-4">
              {allSystems.map((system) => (
                <Card
                  key={system.id}
                  variant="default"
                  padding="md"
                  className="hover:border-blue-600 transition-colors"
                >
                  <div className="flex items-start gap-4">
                    <span className="text-4xl">{system.emoji}</span>
                    <div className="flex-1">
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <h3 className="text-lg font-black">{system.name}</h3>
                          <p className="text-xs text-gray-600">{system.marketShare}</p>
                        </div>
                        <div className="flex gap-2">
                          <Badge
                            variant={
                              system.difficulty === 'easy' ? 'success' :
                              system.difficulty === 'medium' ? 'warning' : 'default'
                            }
                            size="sm"
                          >
                            {getDifficultyLabel(system.difficulty)}
                          </Badge>
                          <Badge variant="info" size="sm">
                            {system.formatPreference === 'both' ? 'PDF/DOCX' : system.formatPreference.toUpperCase()}
                          </Badge>
                        </div>
                      </div>

                      <p className="text-sm text-gray-700 mb-3">{system.bestFor}</p>

                      <div className="flex gap-2 items-center">
                        <code className="text-xs bg-gray-100 px-2 py-1 rounded">
                          {system.urlPattern}
                        </code>
                        <Link
                          href={`/tips/ats/${system.id}`}
                          className="text-sm font-bold text-blue-600 hover:underline"
                        >
                          Full Guide →
                        </Link>
                      </div>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </Card>
        )}

        {/* Quick Stats */}
        <Card variant="default" padding="lg" className="bg-gradient-to-r from-blue-50 to-purple-50 border-2 border-blue-600">
          <h2 className="text-xl font-black mb-4 uppercase">📊 Market Overview</h2>
          <div className="grid md:grid-cols-3 gap-4 text-sm">
            <div className="flex gap-3">
              <span className="text-3xl">🏢</span>
              <div>
                <p className="font-bold text-lg">97.8%</p>
                <p className="text-gray-700">Fortune 500 use ATS</p>
              </div>
            </div>
            <div className="flex gap-3">
              <span className="text-3xl">👑</span>
              <div>
                <p className="font-bold text-lg">Workday</p>
                <p className="text-gray-700">39% market leader</p>
              </div>
            </div>
            <div className="flex gap-3">
              <span className="text-3xl">🚀</span>
              <div>
                <p className="font-bold text-lg">Phenom</p>
                <p className="text-gray-700">Fastest growing</p>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
}
