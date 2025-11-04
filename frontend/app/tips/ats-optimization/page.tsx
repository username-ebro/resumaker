'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button, Card } from '@/components/ui'

export default function ATSOptimizationPage() {
  const router = useRouter()

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-6 py-12">
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
            ATS OPTIMIZATION GUIDE
          </h1>
          <p className="text-lg text-gray-600">
            Master the resume format game and get past the bots
          </p>
        </div>

        {/* File Format Section */}
        <Card variant="elevated" padding="lg" className="mb-6">
          <h2 className="text-2xl font-black mb-4 uppercase">📄 File Format: The TL;DR</h2>

          <div className="mb-6">
            <p className="text-lg font-semibold mb-4">Keep BOTH formats ready:</p>

            <div className="grid md:grid-cols-2 gap-4 mb-4">
              <Card variant="seafoam" padding="md">
                <h3 className="text-lg font-bold mb-2">📝 DOCX (.docx)</h3>
                <p className="text-sm font-semibold mb-3">Best for:</p>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 font-bold">✓</span>
                    <span>Online job applications</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 font-bold">✓</span>
                    <span>ATS systems (98% compatible)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 font-bold">✓</span>
                    <span>When posting doesn't specify</span>
                  </li>
                </ul>
              </Card>

              <Card variant="default" padding="md" className="border-2 border-gray-300">
                <h3 className="text-lg font-bold mb-2">📄 PDF</h3>
                <p className="text-sm font-semibold mb-3">Best for:</p>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 font-bold">✓</span>
                    <span>Emailing recruiters directly</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 font-bold">✓</span>
                    <span>Networking/LinkedIn</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 font-bold">✓</span>
                    <span>When posting requests PDF</span>
                  </li>
                </ul>
              </Card>
            </div>

            <Card variant="default" padding="sm" className="bg-blue-50 border-blue-600">
              <p className="text-sm font-bold">
                💡 <strong>Pro Tip:</strong> DOCX is safer for ATS. 98.4% of Fortune 500 companies use ATS systems, and Word files parse more reliably. PDFs work with modern ATS, but they're riskier—some older systems struggle.
              </p>
            </Card>
          </div>
        </Card>

        {/* Critical Formatting Rules */}
        <Card variant="elevated" padding="lg" className="mb-6">
          <h2 className="text-2xl font-black mb-4 uppercase">🚨 Critical Formatting Rules</h2>

          {/* AVOID Section */}
          <div className="mb-6">
            <h3 className="text-xl font-bold mb-3 text-red-600">❌ AVOID These (ATS Killers)</h3>
            <div className="space-y-3">
              <Card variant="default" padding="sm" className="bg-red-50 border-red-200">
                <p className="text-sm"><strong>Tables & columns</strong> - ATS reads left-to-right, top-to-bottom only</p>
              </Card>
              <Card variant="default" padding="sm" className="bg-red-50 border-red-200">
                <p className="text-sm"><strong>Text boxes</strong> - Content often ignored completely</p>
              </Card>
              <Card variant="default" padding="sm" className="bg-red-50 border-red-200">
                <p className="text-sm"><strong>Headers/footers</strong> - Only body content gets parsed</p>
              </Card>
              <Card variant="default" padding="sm" className="bg-red-50 border-red-200">
                <p className="text-sm"><strong>Graphics, photos, logos</strong> - Causes parsing errors</p>
              </Card>
              <Card variant="default" padding="sm" className="bg-red-50 border-red-200">
                <p className="text-sm"><strong>Creative fonts</strong> - Use Arial, Calibri, Times New Roman, Helvetica only</p>
              </Card>
              <Card variant="default" padding="sm" className="bg-red-50 border-red-200">
                <p className="text-sm"><strong>Fancy bullet points</strong> (★ ◆ ✓) - Use standard bullets (• - or none)</p>
              </Card>
              <Card variant="default" padding="sm" className="bg-red-50 border-red-200">
                <p className="text-sm"><strong>Creative section headings</strong> ("My Journey", "Where I've Been") - Kills parsing</p>
              </Card>
            </div>
          </div>

          {/* DO Section */}
          <div>
            <h3 className="text-xl font-bold mb-3 text-green-600">✅ DO This (ATS-Friendly)</h3>
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <h4 className="font-bold text-sm uppercase mb-2 text-gray-700">Format & Layout</h4>
                <ul className="space-y-2 text-sm">
                  <li className="flex gap-2"><span className="text-green-600">•</span>Single column format</li>
                  <li className="flex gap-2"><span className="text-green-600">•</span>Standard fonts (10-12pt body, 14-16pt headers)</li>
                  <li className="flex gap-2"><span className="text-green-600">•</span>Margins: 0.75" - 1"</li>
                  <li className="flex gap-2"><span className="text-green-600">•</span>Line spacing: 1.0 - 1.15</li>
                  <li className="flex gap-2"><span className="text-green-600">•</span>Left-aligned text</li>
                  <li className="flex gap-2"><span className="text-green-600">•</span>Reverse chronological order</li>
                </ul>
              </div>
              <div>
                <h4 className="font-bold text-sm uppercase mb-2 text-gray-700">Section Headings</h4>
                <p className="text-sm mb-2">Use EXACTLY these:</p>
                <ul className="space-y-2 text-sm">
                  <li className="flex gap-2"><span className="text-green-600">•</span><strong>Work Experience</strong></li>
                  <li className="flex gap-2"><span className="text-green-600">•</span><strong>Education</strong></li>
                  <li className="flex gap-2"><span className="text-green-600">•</span><strong>Skills</strong></li>
                  <li className="flex gap-2"><span className="text-green-600">•</span><strong>Certifications</strong></li>
                  <li className="flex gap-2"><span className="text-green-600">•</span><strong>Summary</strong></li>
                </ul>
              </div>
            </div>
          </div>
        </Card>

        {/* Keywords Section */}
        <Card variant="elevated" padding="lg" className="mb-6">
          <h2 className="text-2xl font-black mb-4 uppercase">🔑 Keywords Matter!</h2>

          <Card variant="default" padding="sm" className="bg-yellow-50 border-yellow-600 mb-4">
            <p className="text-sm font-bold">
              ⚠️ <strong>99.7% of recruiters use keyword filters in their ATS!</strong>
            </p>
          </Card>

          <div className="space-y-3 text-sm">
            <div className="flex gap-3">
              <span className="text-2xl">1️⃣</span>
              <div>
                <p className="font-bold mb-1">Copy EXACT wording from job description</p>
                <p className="text-gray-600">If they say "project management," don't write "managing projects"</p>
              </div>
            </div>
            <div className="flex gap-3">
              <span className="text-2xl">2️⃣</span>
              <div>
                <p className="font-bold mb-1">Include both acronyms AND full terms</p>
                <p className="text-gray-600">Example: "Search Engine Optimization (SEO)"</p>
              </div>
            </div>
            <div className="flex gap-3">
              <span className="text-2xl">3️⃣</span>
              <div>
                <p className="font-bold mb-1">Use standard names for skills and certifications</p>
                <p className="text-gray-600">Official names parse better: "Project Management Professional (PMP)"</p>
              </div>
            </div>
          </div>
        </Card>

        {/* File Naming */}
        <Card variant="elevated" padding="lg" className="mb-6">
          <h2 className="text-2xl font-black mb-4 uppercase">📝 File Naming Best Practice</h2>
          <div className="space-y-3">
            <div className="flex gap-3 items-center">
              <span className="text-green-600 text-2xl font-bold">✓</span>
              <code className="bg-green-50 px-3 py-2 rounded font-mono text-sm border border-green-600">
                FirstName_LastName_Resume.docx
              </code>
            </div>
            <div className="flex gap-3 items-center">
              <span className="text-red-600 text-2xl font-bold">✗</span>
              <code className="bg-red-50 px-3 py-2 rounded font-mono text-sm border border-red-600">
                my_resume.docx
              </code>
            </div>
          </div>
        </Card>

        {/* Stats */}
        <Card variant="default" padding="lg" className="bg-gradient-to-r from-blue-50 to-purple-50 border-2 border-blue-600">
          <h2 className="text-xl font-black mb-4 uppercase">📊 The Numbers Don't Lie</h2>
          <div className="grid md:grid-cols-2 gap-4 text-sm">
            <div className="flex gap-3">
              <span className="text-3xl">📈</span>
              <div>
                <p className="font-bold text-lg">98.4%</p>
                <p className="text-gray-700">of Fortune 500 companies use ATS</p>
              </div>
            </div>
            <div className="flex gap-3">
              <span className="text-3xl">⚠️</span>
              <div>
                <p className="font-bold text-lg">58%</p>
                <p className="text-gray-700">of resumes rejected before human review</p>
              </div>
            </div>
            <div className="flex gap-3">
              <span className="text-3xl">🔍</span>
              <div>
                <p className="font-bold text-lg">99.7%</p>
                <p className="text-gray-700">of recruiters filter by keywords</p>
              </div>
            </div>
            <div className="flex gap-3">
              <span className="text-3xl">🎯</span>
              <div>
                <p className="font-bold text-lg">75%+</p>
                <p className="text-gray-700">target ATS score for best results</p>
              </div>
            </div>
          </div>
        </Card>

        {/* Footer CTA */}
        <div className="mt-8 text-center">
          <Button
            variant="primary"
            size="lg"
            onClick={() => router.push('/resumes')}
          >
            Apply This to Your Resume →
          </Button>
        </div>
      </div>
    </div>
  )
}
