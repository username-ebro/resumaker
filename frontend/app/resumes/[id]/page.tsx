'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { supabase } from '@/lib/supabase'
import ResumeEditor from '@/components/ResumeEditor'
import TruthCheckReview from '@/components/TruthCheckReview'
import { API_URL } from '@/lib/config'
import DOMPurify from 'dompurify'

export default function ResumeDetailPage() {
  const params = useParams()
  const router = useRouter()
  const resumeId = params.id as string

  const [user, setUser] = useState<any>(null)
  const [activeTab, setActiveTab] = useState<'edit' | 'review' | 'preview'>('edit')
  const [resume, setResume] = useState<any>(null)
  const [flags, setFlags] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    checkUserAndFetchResume()
  }, [resumeId])

  const checkUserAndFetchResume = async () => {
    const { data: { user } } = await supabase.auth.getUser()

    if (!user) {
      router.push('/auth/login')
      return
    }

    setUser(user)
    fetchResume(user.id)
  }

  const fetchResume = async (userId: string) => {
    try {
      const res = await fetch(`${API_URL}/resumes/${resumeId}?user_id=${userId}`)

      if (!res.ok) {
        throw new Error('Failed to fetch resume')
      }

      const data = await res.json()

      setResume(data.resume)
      setFlags(data.flags || [])
    } catch (error) {
      console.error('Failed to fetch resume:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async (updatedResume: any) => {
    if (!user) return

    const res = await fetch(`${API_URL}/resumes/${resumeId}?user_id=${user.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ resume_structure: updatedResume })
    })

    const data = await res.json()
    if (data.success) {
      setResume({ ...resume, content: data.resume })
    }
  }

  const handleResolveFlag = async (flagId: string, resolution: string) => {
    if (!user) return

    const res = await fetch(`${API_URL}/resumes/flags/${flagId}/resolve?user_id=${user.id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ resolution_notes: resolution })
    })

    if (res.ok) {
      // Refresh flags
      await fetchResume(user.id)
    }
  }

  const handleFinalize = async () => {
    if (!user) return

    if (!confirm('Finalize this resume? You should resolve all critical flags first.')) {
      return
    }

    try {
      const res = await fetch(`${API_URL}/resumes/${resumeId}/finalize?user_id=${user.id}`, {
        method: 'POST'
      })

      const data = await res.json()

      if (data.success) {
        alert('Resume finalized successfully!')
        await fetchResume(user.id)
      } else {
        alert(data.error || 'Failed to finalize resume')
      }
    } catch (error) {
      alert('Failed to finalize resume')
    }
  }

  const handleExportHTML = async () => {
    if (!user) return

    try {
      const res = await fetch(`${API_URL}/resumes/${resumeId}/export/html?user_id=${user.id}`)
      const data = await res.json()

      // Create a download
      const blob = new Blob([data.html], { type: 'text/html' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `resume-${resumeId}.html`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } catch (error) {
      alert('Failed to export resume')
    }
  }

  const handleExportPDF = async () => {
    if (!user) return

    try {
      const res = await fetch(`${API_URL}/resumes/${resumeId}/export/pdf?user_id=${user.id}`)

      if (!res.ok) {
        throw new Error('Failed to export PDF')
      }

      const blob = await res.blob()
      const contentDisposition = res.headers.get('Content-Disposition')
      let filename = 'resume.pdf'
      if (contentDisposition) {
        const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(contentDisposition)
        if (matches != null && matches[1]) {
          filename = matches[1].replace(/['"]/g, '')
        }
      }

      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = filename
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } catch (error) {
      alert('Failed to export PDF')
    }
  }

  const handleExportDOCX = async () => {
    if (!user) return

    try {
      const res = await fetch(`${API_URL}/resumes/${resumeId}/export/docx?user_id=${user.id}`)

      if (!res.ok) {
        throw new Error('Failed to export DOCX')
      }

      const blob = await res.blob()
      const contentDisposition = res.headers.get('Content-Disposition')
      let filename = 'resume.docx'
      if (contentDisposition) {
        const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(contentDisposition)
        if (matches != null && matches[1]) {
          filename = matches[1].replace(/['"]/g, '')
        }
      }

      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = filename
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } catch (error) {
      alert('Failed to export DOCX')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading resume...</p>
        </div>
      </div>
    )
  }

  if (!resume) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Resume not found</h2>
          <button
            onClick={() => router.push('/resumes')}
            className="text-blue-600 hover:underline"
          >
            ← Back to resumes
          </button>
        </div>
      </div>
    )
  }

  const unresolvedHighFlags = flags.filter(f => !f.resolved && f.severity === 'high').length
  const unresolvedMediumFlags = flags.filter(f => !f.resolved && f.severity === 'medium').length

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <button
                onClick={() => router.push('/resumes')}
                className="text-gray-600 hover:text-gray-900"
              >
                ← Back
              </button>
              <div>
                <h1 className="text-xl font-bold">Resume Version {resume.version_number}</h1>
                <div className="flex items-center gap-3 mt-1">
                  <span className={`px-2 py-1 rounded text-xs font-medium ${
                    resume.status === 'finalized' ? 'bg-blue-100 text-blue-800' :
                    resume.status === 'truth_check_complete' ? 'bg-green-100 text-green-800' :
                    resume.status === 'truth_check_pending' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {resume.status.replace(/_/g, ' ').toUpperCase()}
                  </span>
                  {unresolvedHighFlags > 0 && (
                    <span className="text-xs text-red-600 font-medium">
                      {unresolvedHighFlags} high priority flag{unresolvedHighFlags !== 1 ? 's' : ''}
                    </span>
                  )}
                </div>
              </div>
            </div>

            <div className="flex gap-3">
              {resume.status === 'truth_check_complete' && (
                <button
                  onClick={handleFinalize}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                >
                  Finalize Resume
                </button>
              )}
              <button
                onClick={handleExportPDF}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
              >
                📄 Download PDF
              </button>
              <button
                onClick={handleExportDOCX}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                📝 Download DOCX
              </button>
            </div>
          </div>

          {/* Tabs */}
          <div className="mt-4 flex gap-2 border-b">
            <button
              onClick={() => setActiveTab('edit')}
              className={`px-4 py-2 font-medium ${
                activeTab === 'edit'
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Edit Resume
            </button>
            <button
              onClick={() => setActiveTab('review')}
              className={`px-4 py-2 font-medium flex items-center gap-2 ${
                activeTab === 'review'
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Truth Check
              {(unresolvedHighFlags + unresolvedMediumFlags) > 0 && (
                <span className="bg-red-600 text-white text-xs font-bold px-2 py-0.5 rounded-full">
                  {unresolvedHighFlags + unresolvedMediumFlags}
                </span>
              )}
            </button>
            <button
              onClick={() => setActiveTab('preview')}
              className={`px-4 py-2 font-medium ${
                activeTab === 'preview'
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Preview
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto">
        {activeTab === 'edit' && (
          <ResumeEditor
            resumeId={resumeId}
            initialData={resume.content}
            onSave={handleSave}
          />
        )}

        {activeTab === 'review' && (
          <TruthCheckReview
            flags={flags}
            onResolveFlag={handleResolveFlag}
          />
        )}

        {activeTab === 'preview' && (
          <div className="p-6">
            <div className="bg-white rounded-lg shadow p-8">
              <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(resume.html_content) }} />
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
