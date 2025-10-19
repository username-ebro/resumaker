'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { supabase } from '@/lib/supabase'
import { API_URL } from '@/lib/config'
import { useToast } from '@/components/Toast'

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
        <div className="brutal-box brutal-shadow p-12 text-center">
          <div className="cool-spinner h-12 w-12 border-4 border-black border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-sm font-bold uppercase">Loading resumes...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen">
      {/* Nav */}
      <nav className="brutal-box border-b-2 border-black">
        <div className="max-w-7xl mx-auto px-6 py-6 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <button
              onClick={() => router.push('/dashboard')}
              className="brutal-btn brutal-shadow"
            >
              ← Back
            </button>
            <h1 className="text-2xl">MY RESUMES</h1>
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

      <main className="max-w-7xl mx-auto px-6 py-12">
        {/* Archive toggle */}
        <div className="mb-6 flex gap-2">
          <button
            onClick={() => setShowArchived(false)}
            className={`brutal-btn brutal-shadow ${!showArchived ? 'brutal-btn-primary' : ''}`}
          >
            Active ({resumes.filter(r => !r.is_archived).length})
          </button>
          <button
            onClick={() => setShowArchived(true)}
            className={`brutal-btn brutal-shadow ${showArchived ? 'brutal-btn-primary' : ''}`}
          >
            Archived ({resumes.filter(r => r.is_archived).length})
          </button>
        </div>

        {/* Empty state */}
        {filteredResumes.length === 0 ? (
          <div className="brutal-box brutal-shadow p-12 text-center">
            <h3 className="text-2xl mb-4">
              {showArchived ? 'NO ARCHIVED RESUMES' : 'NO RESUMES YET'}
            </h3>
            <p className="text-sm mb-6">
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
                {generating ? 'Generating...' : 'Generate First Resume'}
              </button>
            )}
          </div>
        ) : (
          <div className="grid gap-4">
            {filteredResumes.map((resume) => (
              <div key={resume.id} className="brutal-box brutal-shadow p-6">
                <div className="flex justify-between items-start gap-4">
                  {/* Left: Title and metadata */}
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      {/* Star button */}
                      <button
                        onClick={(e) => {
                          e.preventDefault()
                          toggleStar(resume.id, resume.is_starred || false)
                        }}
                        className="text-2xl hover:scale-110 transition-transform"
                      >
                        {resume.is_starred ? '⭐' : '☆'}
                      </button>

                      <Link href={`/resumes/${resume.id}`}>
                        <h3 className="text-lg font-bold hover:underline">
                          {resume.job_title || `Resume Version ${resume.version}`}
                        </h3>
                      </Link>

                      <span className={`px-3 py-1 text-xs font-bold ${getStatusBadge(resume.status)}`}>
                        {getStatusLabel(resume.status)}
                      </span>
                    </div>

                    {resume.company && (
                      <p className="text-sm mb-2">{resume.company}</p>
                    )}

                    <div className="flex items-center gap-4 text-xs text-gray-600">
                      <span>Version {resume.version}</span>
                      <span>•</span>
                      <span>Created {new Date(resume.created_at).toLocaleString('en-US', {
                        month: 'numeric',
                        day: 'numeric',
                        year: 'numeric',
                        hour: 'numeric',
                        minute: '2-digit',
                        hour12: true
                      })}</span>
                    </div>

                    {/* Truth check warning */}
                    {resume.status === 'truth_check_pending' && (
                      <div className="mt-3 p-2 brutal-box bg-yellow-50 text-xs">
                        <span className="font-bold">⚠️ Truth check required</span>
                      </div>
                    )}
                  </div>

                  {/* Right: ATS Score */}
                  <div className="text-center">
                    <div className="text-xs font-bold uppercase mb-1">ATS Score</div>
                    <div className={`text-4xl font-bold ${getATSScoreColor(resume.ats_score)}`}>
                      {resume.ats_score}
                    </div>
                    <div className="text-xs text-gray-500">/ 100</div>
                  </div>

                  {/* Actions */}
                  <div className="flex flex-col gap-2">
                    <button
                      onClick={() => router.push(`/resumes/${resume.id}`)}
                      className="brutal-btn brutal-btn-primary brutal-shadow text-xs px-3 py-2"
                    >
                      View
                    </button>
                    <button
                      onClick={() => archiveResume(resume.id, resume.is_archived || false)}
                      className="brutal-btn brutal-shadow text-xs px-3 py-2"
                    >
                      {resume.is_archived ? 'Unarchive' : 'Archive'}
                    </button>
                    <button
                      onClick={() => deleteResume(resume.id)}
                      className="brutal-btn bg-red-50 border-2 border-red-600 hover:bg-red-100 text-xs px-3 py-2"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Quick Stats */}
        {resumes.length > 0 && (
          <div className="mt-8 grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="brutal-box-seafoam brutal-shadow-seafoam p-4">
              <p className="text-xs font-bold uppercase mb-1">Total Resumes</p>
              <p className="text-3xl font-bold">{resumes.length}</p>
            </div>
            <div className="brutal-box brutal-shadow p-4">
              <p className="text-xs font-bold uppercase mb-1">Starred</p>
              <p className="text-3xl font-bold">
                {resumes.filter(r => r.is_starred).length}
              </p>
            </div>
            <div className="brutal-box brutal-shadow p-4">
              <p className="text-xs font-bold uppercase mb-1">Finalized</p>
              <p className="text-3xl font-bold text-green-600">
                {resumes.filter(r => r.status === 'finalized').length}
              </p>
            </div>
            <div className="brutal-box brutal-shadow p-4">
              <p className="text-xs font-bold uppercase mb-1">Avg ATS</p>
              <p className={`text-3xl font-bold ${getATSScoreColor(Math.round(resumes.reduce((sum, r) => sum + r.ats_score, 0) / resumes.length))}`}>
                {Math.round(resumes.reduce((sum, r) => sum + r.ats_score, 0) / resumes.length)}
              </p>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
