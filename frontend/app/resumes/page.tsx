'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { supabase } from '@/lib/supabase'
import { API_URL } from '@/lib/config'
import { useToast } from '@/components/Toast'
import { LoadingSpinner } from '@/components/LoadingSpinner'

interface Resume {
  id: string
  version: number
  status: string
  created_at: string
  job_title?: string
  company?: string
  ats_score: number
  is_starred?: boolean
  is_archived?: boolean
}

export default function ResumesPage() {
  const { showToast } = useToast()
  const [user, setUser] = useState<any>(null)
  const [resumes, setResumes] = useState<Resume[]>([])
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)
  const [showArchived, setShowArchived] = useState(false)
  const router = useRouter()

  useEffect(() => {
    checkUserAndFetchResumes()
  }, [])

  const checkUserAndFetchResumes = async () => {
    const { data: { user } } = await supabase.auth.getUser()

    if (!user) {
      router.push('/auth/login')
      return
    }

    setUser(user)
    fetchResumes(user.id)
  }

  const fetchResumes = async (userId: string) => {
    try {
      const res = await fetch(`${API_URL}/resumes/list?user_id=${userId}`)

      if (!res.ok) {
        throw new Error('Failed to fetch resumes')
      }

      const data = await res.json()
      setResumes(data.resumes || [])
    } catch (error) {
      console.error('Failed to fetch resumes:', error)
      setResumes([]) // Ensure resumes is always an array
    } finally {
      setLoading(false)
    }
  }

  const generateNewResume = async () => {
    if (!user) return

    setGenerating(true)
    try {
      const res = await fetch(`${API_URL}/resumes/generate?user_id=${user.id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      })

      const data = await res.json()

      if (data.success) {
        // Navigate to the new resume
        router.push(`/resumes/${data.resume_version_id}`)
      } else {
        showToast('Failed to generate resume: ' + (data.error || 'Unknown error'), 'error')
      }
    } catch (error) {
      console.error('Failed to generate resume:', error)
      showToast('Failed to generate resume', 'error')
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

  const toggleStar = async (resumeId: string, currentStarred: boolean) => {
    try {
      // Optimistic update
      setResumes(prev => prev.map(r =>
        r.id === resumeId ? { ...r, is_starred: !currentStarred } : r
      ))

      const res = await fetch(`${API_URL}/resumes/${resumeId}/star`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ is_starred: !currentStarred })
      })

      if (!res.ok) {
        // Revert on error
        setResumes(prev => prev.map(r =>
          r.id === resumeId ? { ...r, is_starred: currentStarred } : r
        ))
        throw new Error('Failed to update star')
      }
    } catch (error) {
      console.error('Failed to toggle star:', error)
    }
  }

  const deleteResume = async (resumeId: string) => {
    if (!confirm('Delete this resume permanently?')) return

    try {
      const res = await fetch(`${API_URL}/resumes/${resumeId}`, {
        method: 'DELETE'
      })

      if (res.ok) {
        setResumes(prev => prev.filter(r => r.id !== resumeId))
      } else {
        throw new Error('Failed to delete')
      }
    } catch (error) {
      console.error('Failed to delete resume:', error)
      showToast('Failed to delete resume', 'error')
    }
  }

  const archiveResume = async (resumeId: string, currentArchived: boolean) => {
    try {
      // Optimistic update
      setResumes(prev => prev.map(r =>
        r.id === resumeId ? { ...r, is_archived: !currentArchived } : r
      ))

      const res = await fetch(`${API_URL}/resumes/${resumeId}/archive`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ is_archived: !currentArchived })
      })

      if (!res.ok) {
        // Revert on error
        setResumes(prev => prev.map(r =>
          r.id === resumeId ? { ...r, is_archived: currentArchived } : r
        ))
        throw new Error('Failed to archive')
      }
    } catch (error) {
      console.error('Failed to toggle archive:', error)
    }
  }

  // Filter resumes based on archived status
  const filteredResumes = showArchived
    ? resumes.filter(r => r.is_archived)
    : resumes.filter(r => !r.is_archived)

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner message="Loading resumes..." />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Nav */}
      <nav className="brutal-box border-b-4 border-black bg-white sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-6 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <button
              onClick={() => router.push('/dashboard')}
              className="brutal-btn brutal-shadow text-sm"
            >
              ← Back
            </button>
            <div>
              <h1 className="text-3xl font-black tracking-tight">MY RESUMES</h1>
              <p className="text-xs text-gray-500 uppercase tracking-wider">Manage your resume versions</p>
            </div>
          </div>
          <button
            onClick={generateNewResume}
            disabled={generating}
            className="brutal-btn brutal-btn-primary brutal-shadow disabled:opacity-50"
          >
            {generating ? 'Generating...' : '+ New Resume'}
          </button>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Archive toggle */}
        <div className="mb-8 flex gap-3">
          <button
            onClick={() => setShowArchived(false)}
            className={`brutal-btn brutal-shadow text-sm ${!showArchived ? 'brutal-btn-primary' : 'brutal-btn-seafoam'}`}
          >
            📋 Active ({resumes.filter(r => !r.is_archived).length})
          </button>
          <button
            onClick={() => setShowArchived(true)}
            className={`brutal-btn brutal-shadow text-sm ${showArchived ? 'brutal-btn-primary' : 'brutal-btn-seafoam'}`}
          >
            📦 Archived ({resumes.filter(r => r.is_archived).length})
          </button>
        </div>

        {/* Empty state */}
        {filteredResumes.length === 0 ? (
          <div className="brutal-box brutal-shadow bg-white p-16 text-center">
            <div className="text-6xl mb-4">{showArchived ? '📦' : '📄'}</div>
            <h3 className="text-3xl font-black mb-3 uppercase">
              {showArchived ? 'No Archived Resumes' : 'No Resumes Yet'}
            </h3>
            <p className="text-sm text-gray-600 mb-8 max-w-md mx-auto">
              {showArchived
                ? 'Archived resumes will appear here'
                : 'Generate your first ATS-optimized resume from your knowledge base'}
            </p>
            {!showArchived && (
              <button
                onClick={generateNewResume}
                disabled={generating}
                className="brutal-btn brutal-btn-primary brutal-shadow"
              >
                {generating ? 'Generating...' : '✨ Generate First Resume'}
              </button>
            )}
          </div>
        ) : (
          <div className="grid gap-5">
            {filteredResumes.map((resume) => (
              <div key={resume.id} className="brutal-box brutal-shadow bg-white p-6 hover:translate-x-1 hover:translate-y-1 transition-transform">
                <div className="flex justify-between items-start gap-6">
                  {/* Left: Title and metadata */}
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-3">
                      {/* Star button */}
                      <button
                        onClick={(e) => {
                          e.preventDefault()
                          toggleStar(resume.id, resume.is_starred || false)
                        }}
                        className="text-2xl hover:scale-125 transition-transform"
                        aria-label={resume.is_starred ? 'Remove star' : 'Star resume'}
                      >
                        {resume.is_starred ? '⭐' : '☆'}
                      </button>

                      <Link href={`/resumes/${resume.id}`}>
                        <h3 className="text-xl font-black hover:underline uppercase tracking-tight">
                          {resume.job_title || `Resume Version ${resume.version}`}
                        </h3>
                      </Link>

                      <span className={`px-3 py-1 text-xs font-bold border-2 border-black ${getStatusBadge(resume.status)}`}>
                        {getStatusLabel(resume.status)}
                      </span>
                    </div>

                    {resume.company && (
                      <p className="text-sm font-semibold text-gray-700 mb-2">📍 {resume.company}</p>
                    )}

                    <div className="flex items-center gap-3 text-xs text-gray-500 font-medium">
                      <span className="bg-gray-100 px-2 py-1 border border-gray-300">v{resume.version}</span>
                      <span>Created {new Date(resume.created_at).toLocaleString('en-US', {
                        month: 'short',
                        day: 'numeric',
                        year: 'numeric',
                        hour: 'numeric',
                        minute: '2-digit',
                        hour12: true
                      })}</span>
                    </div>

                    {/* Truth check warning */}
                    {resume.status === 'truth_check_pending' && (
                      <div className="mt-3 p-3 brutal-box bg-yellow-50 border-yellow-600 text-sm">
                        <span className="font-bold">⚠️ Truth check required before finalizing</span>
                      </div>
                    )}
                  </div>

                  {/* Right: ATS Score */}
                  <div className="brutal-box bg-gray-50 p-4 text-center min-w-[120px]">
                    <div className="text-xs font-bold uppercase mb-2 text-gray-600">ATS Score</div>
                    <div className={`text-5xl font-black ${getATSScoreColor(resume.ats_score)}`}>
                      {resume.ats_score}
                    </div>
                    <div className="text-xs text-gray-500 font-semibold mt-1">/ 100</div>
                  </div>

                  {/* Actions */}
                  <div className="flex flex-col gap-2 min-w-[100px]">
                    <button
                      onClick={() => router.push(`/resumes/${resume.id}`)}
                      className="brutal-btn brutal-btn-primary brutal-shadow text-xs px-4 py-2"
                    >
                      View
                    </button>
                    <button
                      onClick={() => archiveResume(resume.id, resume.is_archived || false)}
                      className="brutal-btn brutal-btn-seafoam brutal-shadow text-xs px-4 py-2"
                      aria-label={resume.is_archived ? 'Unarchive resume' : 'Archive resume'}
                    >
                      {resume.is_archived ? '↩ Restore' : '📦 Archive'}
                    </button>
                    <button
                      onClick={() => deleteResume(resume.id)}
                      className="brutal-btn bg-red-50 border-2 border-red-600 hover:bg-red-100 text-red-600 text-xs px-4 py-2"
                      aria-label="Delete resume"
                    >
                      🗑 Delete
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Quick Stats */}
        {resumes.length > 0 && (
          <div className="mt-12">
            <h3 className="text-sm font-bold uppercase text-gray-600 mb-4">Statistics</h3>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="brutal-box-seafoam brutal-shadow-seafoam p-6 bg-white">
                <p className="text-xs font-bold uppercase mb-2 text-gray-600">Total Resumes</p>
                <p className="text-4xl font-black">{resumes.length}</p>
              </div>
              <div className="brutal-box brutal-shadow bg-white p-6">
                <p className="text-xs font-bold uppercase mb-2 text-gray-600">Starred</p>
                <p className="text-4xl font-black">
                  ⭐ {resumes.filter(r => r.is_starred).length}
                </p>
              </div>
              <div className="brutal-box brutal-shadow bg-white p-6">
                <p className="text-xs font-bold uppercase mb-2 text-gray-600">Finalized</p>
                <p className="text-4xl font-black text-green-600">
                  {resumes.filter(r => r.status === 'finalized').length}
                </p>
              </div>
              <div className="brutal-box brutal-shadow bg-white p-6">
                <p className="text-xs font-bold uppercase mb-2 text-gray-600">Avg ATS Score</p>
                <p className={`text-4xl font-black ${getATSScoreColor(Math.round(resumes.reduce((sum, r) => sum + r.ats_score, 0) / resumes.length))}`}>
                  {Math.round(resumes.reduce((sum, r) => sum + r.ats_score, 0) / resumes.length)}
                </p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
