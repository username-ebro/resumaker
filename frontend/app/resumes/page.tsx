'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { API_URL } from '@/lib/config'

interface Resume {
  id: string
  version: number
  status: string
  created_at: string
  job_title?: string
  company?: string
  ats_score: number
}

export default function ResumesPage() {
  const [resumes, setResumes] = useState<Resume[]>([])
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)
  const router = useRouter()


  useEffect(() => {
    fetchResumes()
  }, [])

  const fetchResumes = async () => {
    try {
      // TODO: Replace with actual user ID from auth
      const userId = 'test-user-id'

      const res = await fetch(`${API_URL}/resumes/list?user_id=${userId}`)
      const data = await res.json()
      setResumes(data.resumes)
    } catch (error) {
      console.error('Failed to fetch resumes:', error)
    } finally {
      setLoading(false)
    }
  }

  const generateNewResume = async () => {
    setGenerating(true)
    try {
      // TODO: Replace with actual user ID from auth
      const userId = 'test-user-id'

      const res = await fetch(`${API_URL}/resumes/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId })
      })

      const data = await res.json()

      if (data.success) {
        // Navigate to the new resume
        router.push(`/resumes/${data.resume_version_id}`)
      }
    } catch (error) {
      console.error('Failed to generate resume:', error)
      alert('Failed to generate resume')
    } finally {
      setGenerating(false)
    }
  }

  const getStatusBadge = (status: string) => {
    const styles = {
      draft: 'bg-gray-100 text-gray-800',
      truth_check_pending: 'bg-yellow-100 text-yellow-800',
      truth_check_complete: 'bg-green-100 text-green-800',
      finalized: 'bg-blue-100 text-blue-800'
    }
    return styles[status as keyof typeof styles] || 'bg-gray-100 text-gray-800'
  }

  const getStatusLabel = (status: string) => {
    const labels = {
      draft: 'Draft',
      truth_check_pending: 'Needs Review',
      truth_check_complete: 'Verified',
      finalized: 'Finalized'
    }
    return labels[status as keyof typeof labels] || status
  }

  const getATSScoreColor = (score: number) => {
    if (score >= 75) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading resumes...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto p-6">
        {/* Header */}
        <div className="mb-8">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">My Resumes</h1>
              <p className="text-gray-600 mt-2">
                Generate, edit, and manage your ATS-optimized resumes
              </p>
            </div>
            <button
              onClick={generateNewResume}
              disabled={generating}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400"
            >
              {generating ? 'Generating...' : '+ New Resume'}
            </button>
          </div>
        </div>

        {/* Resumes List */}
        {resumes.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <div className="mb-4">
              <svg
                className="mx-auto h-12 w-12 text-gray-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No resumes yet</h3>
            <p className="text-gray-600 mb-6">
              Generate your first ATS-optimized resume from your knowledge base
            </p>
            <button
              onClick={generateNewResume}
              disabled={generating}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700"
            >
              {generating ? 'Generating...' : 'Generate First Resume'}
            </button>
          </div>
        ) : (
          <div className="grid gap-4">
            {resumes.map((resume) => (
              <Link
                key={resume.id}
                href={`/resumes/${resume.id}`}
                className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6 block"
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-lg font-semibold text-gray-900">
                        {resume.job_title || `Resume Version ${resume.version}`}
                      </h3>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusBadge(resume.status)}`}>
                        {getStatusLabel(resume.status)}
                      </span>
                    </div>

                    {resume.company && (
                      <p className="text-gray-600 mb-2">{resume.company}</p>
                    )}

                    <div className="flex items-center gap-4 text-sm text-gray-500">
                      <span>Version {resume.version}</span>
                      <span>•</span>
                      <span>Created {new Date(resume.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>

                  <div className="text-right">
                    <div className="text-sm text-gray-600 mb-1">ATS Score</div>
                    <div className={`text-3xl font-bold ${getATSScoreColor(resume.ats_score)}`}>
                      {resume.ats_score}
                    </div>
                    <div className="text-xs text-gray-500">/ 100</div>
                  </div>
                </div>

                {/* Progress indicator for pending reviews */}
                {resume.status === 'truth_check_pending' && (
                  <div className="mt-4 pt-4 border-t border-gray-200">
                    <div className="flex items-center text-yellow-700">
                      <svg className="h-5 w-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                      </svg>
                      <span className="text-sm font-medium">Truth check required - review flagged items</span>
                    </div>
                  </div>
                )}
              </Link>
            ))}
          </div>
        )}

        {/* Quick Stats */}
        {resumes.length > 0 && (
          <div className="mt-8 grid grid-cols-3 gap-4">
            <div className="bg-white rounded-lg shadow p-4">
              <div className="text-2xl font-bold text-gray-900">{resumes.length}</div>
              <div className="text-sm text-gray-600">Total Resumes</div>
            </div>
            <div className="bg-white rounded-lg shadow p-4">
              <div className="text-2xl font-bold text-green-600">
                {resumes.filter(r => r.status === 'finalized').length}
              </div>
              <div className="text-sm text-gray-600">Finalized</div>
            </div>
            <div className="bg-white rounded-lg shadow p-4">
              <div className="text-2xl font-bold text-blue-600">
                {Math.round(resumes.reduce((sum, r) => sum + r.ats_score, 0) / resumes.length)}
              </div>
              <div className="text-sm text-gray-600">Avg ATS Score</div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
