'use client';

import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';
import { useRouter } from 'next/navigation';
import UploadResume from '@/components/UploadResume';
import ImportConversation from '@/components/ImportConversation';
import ConversationInterface from '@/components/ConversationInterface';
import JobConfirmation from '@/components/JobConfirmation';
import GenericResumeGenerator from '@/components/GenericResumeGenerator';
import { knowledgeApi } from '@/lib/api/knowledge';

export default function DashboardPage() {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'conversation' | 'upload' | 'import' | 'generate'>('conversation');
  const [pendingCount, setPendingCount] = useState(0);

  // Resume generation state
  const [analyzingJob, setAnalyzingJob] = useState(false);
  const [generatingResume, setGeneratingResume] = useState(false);
  const [jobTitle, setJobTitle] = useState('');
  const [jobUrl, setJobUrl] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [jobData, setJobData] = useState<any>(null); // Parsed job data
  const [showJobConfirmation, setShowJobConfirmation] = useState(false);
  const [resumeType, setResumeType] = useState<'job-specific' | 'generic'>('job-specific');
  const [error, setError] = useState<string | null>(null);
  const [confirmedCount, setConfirmedCount] = useState(0);
  const [knowledgeSummary, setKnowledgeSummary] = useState<any>(null);

  const router = useRouter();

  useEffect(() => {
    const checkUser = async () => {
      const { data: { user } } = await supabase.auth.getUser();

      if (!user) {
        router.push('/auth/login');
        return;
      }

      setUser(user);
      setLoading(false);

      // Fetch pending facts count (only once on mount)
      try {
        const summary = await knowledgeApi.getSummary(user.id);
        setPendingCount(summary.pending || 0);
        setConfirmedCount(summary.confirmed || 0);
        setKnowledgeSummary(summary);
      } catch (err) {
        console.error('Failed to fetch pending count:', err);
      }
    };

    checkUser();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Only run once on mount

  const handleLogout = async () => {
    await supabase.auth.signOut();
    router.push('/');
  };

  const handleAnalyzeJob = async () => {
    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }

    setAnalyzingJob(true);
    setError(null);

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

      // Step 1: Analyze job posting (web search + parse)
      const response = await fetch(`${API_URL}/jobs/analyze?user_id=${user.id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          job_description: jobDescription,
          job_url: jobUrl || undefined,
          company_name: jobTitle || undefined,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Server error' }));
        const errorMsg = typeof errorData.detail === 'string'
          ? errorData.detail
          : JSON.stringify(errorData.detail || errorData.error || 'Failed to analyze job');
        throw new Error(errorMsg);
      }

      const data = await response.json();

      if (data.success) {
        // Show confirmation screen with extracted data
        setJobData(data.job_data || {
          title: jobTitle,
          description: jobDescription,
          url: jobUrl,
        });
        setShowJobConfirmation(true);
        setError(null);
      } else {
        throw new Error(data.error || 'Job analysis failed');
      }
    } catch (err) {
      console.error('Error analyzing job:', err);
      setError(err instanceof Error ? err.message : 'Failed to analyze job. Please check your connection and try again.');
    } finally {
      setAnalyzingJob(false);
    }
  };

  const handleJobEdit = (field: string, value: any) => {
    setJobData((prev: any) => ({
      ...prev,
      [field]: value
    }));
  };

  const handleJobCancel = () => {
    setShowJobConfirmation(false);
    setJobData(null);
    setError(null);
  };

  const handleJobConfirm = async (confirmedData: any) => {
    setGeneratingResume(true);
    setError(null);

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

      // Step 2: Create job entity in database
      const createJobResponse = await fetch(`${API_URL}/jobs/create?user_id=${user.id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(confirmedData),
      });

      if (!createJobResponse.ok) {
        const errorData = await createJobResponse.json().catch(() => ({ detail: 'Server error' }));
        const errorMsg = typeof errorData.detail === 'string'
          ? errorData.detail
          : JSON.stringify(errorData.detail || errorData.error || 'Failed to create job');
        throw new Error(errorMsg);
      }

      const jobResult = await createJobResponse.json();

      if (!jobResult.success) {
        throw new Error(jobResult.error || 'Failed to create job');
      }

      // Step 3: Generate resume for this job
      const resumeResponse = await fetch(`${API_URL}/resumes/generate?user_id=${user.id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          job_posting_id: jobResult.job_id,
        }),
      });

      if (!resumeResponse.ok) {
        const errorData = await resumeResponse.json().catch(() => ({ detail: 'Server error' }));
        const errorMsg = typeof errorData.detail === 'string'
          ? errorData.detail
          : JSON.stringify(errorData.detail || errorData.error || 'Failed to generate resume');
        throw new Error(errorMsg);
      }

      const resumeData = await resumeResponse.json();

      if (resumeData.success) {
        // Success - redirect to resumes
        router.push('/resumes');
      } else {
        throw new Error(resumeData.error || 'Resume generation failed');
      }
    } catch (err) {
      console.error('Error generating resume:', err);
      setError(err instanceof Error ? err.message : 'Failed to generate resume. Please try again.');
      setGeneratingResume(false);
    } finally {
      // Only clear confirmation if successful (router.push will navigate away)
      // If error, keep confirmation open so user can retry
      if (!error) {
        setShowJobConfirmation(false);
        setJobData(null);
      }
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="brutal-box brutal-shadow p-8">
          <div className="cool-spinner h-12 w-12 border-4 border-black border-t-transparent rounded-full mx-auto"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <nav className="brutal-box border-b-2 border-black">
        <div className="max-w-7xl mx-auto px-6 py-6 flex justify-between items-center">
          <h1 className="text-2xl">RESUMAKER</h1>
          <div className="flex items-center gap-4">
            <button
              onClick={() => router.push('/dashboard/knowledge')}
              className="brutal-btn brutal-btn-seafoam brutal-shadow relative"
            >
              📚 Knowledge Base
              {pendingCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-black text-white text-xs font-bold px-2 py-1 border-2 border-black">
                  {pendingCount}
                </span>
              )}
            </button>
            <button
              onClick={handleLogout}
              className="brutal-btn brutal-btn-seafoam brutal-shadow"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-12">
        <div className="brutal-box-seafoam brutal-shadow-seafoam p-6 mb-8">
          <h2 className="text-xl">Welcome, {user?.email?.split('@')[0]}</h2>
        </div>

        <div className="mb-8">
          {/* Pending facts alert */}
          {pendingCount > 0 && (
            <div className="brutal-box bg-yellow-50 border-yellow-600 p-4 mb-4">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm font-bold uppercase mb-1">⚠ {pendingCount} Facts Pending Review</p>
                  <p className="text-xs">
                    Review and confirm the facts I extracted from your conversation
                  </p>
                </div>
                <button
                  onClick={() => router.push('/dashboard/knowledge/confirm')}
                  className="brutal-btn brutal-btn-primary brutal-shadow"
                >
                  Review Now
                </button>
              </div>
            </div>
          )}

          <div className="brutal-box-seafoam brutal-shadow-seafoam p-4 mb-4">
            <p className="text-sm font-bold uppercase">Build Your Knowledge Base</p>
            <p className="text-xs mt-1">Add your experience through conversation, uploads, or imports</p>
          </div>

          <div className="flex gap-4 mb-8">
            <button
              onClick={() => setActiveTab('conversation')}
              className={`brutal-btn ${
                activeTab === 'conversation' ? 'brutal-btn-primary' : 'brutal-btn-seafoam'
              } brutal-shadow`}
            >
              💬 Conversation
            </button>
            <button
              onClick={() => setActiveTab('upload')}
              className={`brutal-btn ${
                activeTab === 'upload' ? 'brutal-btn-primary' : 'brutal-btn-seafoam'
              } brutal-shadow`}
            >
              📄 Upload
            </button>
            <button
              onClick={() => setActiveTab('import')}
              className={`brutal-btn ${
                activeTab === 'import' ? 'brutal-btn-primary' : 'brutal-btn-seafoam'
              } brutal-shadow`}
            >
              📋 Import
            </button>
          </div>

          <div className="brutal-box brutal-shadow border-dashed p-6 mb-8 text-center">
            <p className="text-sm font-bold mb-3">Ready to apply for a job?</p>
            <button
              onClick={() => setActiveTab('generate')}
              className="brutal-btn brutal-btn-primary brutal-shadow"
            >
              ✨ Generate Resume
            </button>
          </div>
        </div>

        <div>
          {activeTab === 'conversation' && <ConversationInterface userId={user.id} />}
          {activeTab === 'upload' && <UploadResume />}
          {activeTab === 'import' && <ImportConversation />}
          {activeTab === 'generate' && (
            <>
              {/* Knowledge Confirmation Gate */}
              {confirmedCount < 3 && (
                <div className="brutal-box bg-orange-50 border-orange-600 p-6 mb-6">
                  <div className="flex items-start gap-4">
                    <div className="text-4xl">⚠️</div>
                    <div className="flex-1">
                      <p className="text-sm font-bold uppercase mb-2">
                        Insufficient Confirmed Experience
                      </p>
                      <p className="text-sm mb-3">
                        You only have <strong>{confirmedCount} confirmed facts</strong> in your knowledge base.
                        Resumes need at least 3-5 confirmed experiences to avoid AI hallucination.
                      </p>
                      <div className="flex gap-3 mb-3">
                        <div className="brutal-box-seafoam p-3 text-center">
                          <div className="text-2xl font-bold">{confirmedCount}</div>
                          <div className="text-xs">Confirmed</div>
                        </div>
                        <div className="brutal-box bg-yellow-50 p-3 text-center">
                          <div className="text-2xl font-bold">{pendingCount}</div>
                          <div className="text-xs">Pending</div>
                        </div>
                      </div>
                      <div className="flex gap-3">
                        <button
                          onClick={() => router.push('/dashboard/knowledge/confirm')}
                          className="brutal-btn brutal-btn-primary brutal-shadow"
                        >
                          📚 Review Facts First (Recommended)
                        </button>
                        <button
                          onClick={() => {/* Allow to continue */}}
                          className="brutal-btn brutal-shadow text-xs"
                        >
                          ⚠️ Generate Anyway (Risky)
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {confirmedCount >= 3 && (
                <div className="brutal-box bg-green-50 border-green-600 p-4 mb-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-bold">✅ Knowledge Base Ready</p>
                      <p className="text-xs mt-1">
                        {confirmedCount} confirmed facts • Ready to generate accurate resumes
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* Resume Type Toggle */}
              <div className="mb-6">
                <div className="brutal-box-seafoam brutal-shadow-seafoam p-4 mb-4">
                  <p className="text-sm font-bold uppercase">Resume Type</p>
                  <p className="text-xs mt-1">Choose how you want to create your resume</p>
                </div>

                <div className="flex gap-4">
                  <button
                    onClick={() => setResumeType('job-specific')}
                    className={`brutal-btn ${
                      resumeType === 'job-specific' ? 'brutal-btn-primary' : 'brutal-btn-seafoam'
                    } brutal-shadow flex-1`}
                  >
                    🎯 Job-Specific Resume
                  </button>
                  <button
                    onClick={() => setResumeType('generic')}
                    className={`brutal-btn ${
                      resumeType === 'generic' ? 'brutal-btn-primary' : 'brutal-btn-seafoam'
                    } brutal-shadow flex-1`}
                  >
                    ⚡ Quick Generic Resume
                  </button>
                </div>
              </div>

              {/* Global Error Display */}
              {error && (
                <div className="brutal-box bg-red-50 border-red-600 p-4 mb-6">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="text-sm font-bold uppercase mb-1">Error</p>
                      <p className="text-sm">{error}</p>
                    </div>
                    <button
                      onClick={() => setError(null)}
                      className="brutal-btn text-xs px-2 py-1"
                    >
                      Dismiss
                    </button>
                  </div>
                </div>
              )}

              {/* Conditional Rendering Based on Resume Type */}
              {resumeType === 'generic' ? (
                <GenericResumeGenerator userId={user.id} />
              ) : (
                showJobConfirmation && jobData ? (
                  // Step 2: Job Confirmation
                  <JobConfirmation
                    jobData={jobData}
                    onConfirm={handleJobConfirm}
                    onCancel={handleJobCancel}
                    onEdit={handleJobEdit}
                    loading={generatingResume}
                  />
                ) : (
                  // Step 1: Job Input
                  <div className="space-y-6 max-w-3xl mx-auto">
                    {/* Step Indicator */}
                    <div className="flex items-center justify-center gap-2 mb-6">
                      <div className="flex items-center">
                        <div className="brutal-box brutal-btn-primary w-8 h-8 flex items-center justify-center font-bold text-sm">1</div>
                        <span className="ml-2 text-sm font-bold">Enter Job</span>
                      </div>
                      <div className="w-12 h-0.5 bg-gray-300"></div>
                      <div className="flex items-center opacity-40">
                        <div className="brutal-box w-8 h-8 flex items-center justify-center font-bold text-sm">2</div>
                        <span className="ml-2 text-sm">Review</span>
                      </div>
                      <div className="w-12 h-0.5 bg-gray-300"></div>
                      <div className="flex items-center opacity-40">
                        <div className="brutal-box w-8 h-8 flex items-center justify-center font-bold text-sm">3</div>
                        <span className="ml-2 text-sm">Generate</span>
                      </div>
                    </div>

                    <div className="brutal-box-seafoam brutal-shadow-seafoam p-6">
                      <div className="flex justify-between items-start">
                        <div>
                          <h3 className="text-xl mb-2">Generate Targeted Resume</h3>
                          <p className="text-sm">Tell me about the job you're applying for</p>
                        </div>
                        <button
                          onClick={() => {
                            setJobTitle('Product Manager');
                            setJobUrl('https://www.magicschool.ai/careers');
                            setJobDescription('We are looking for a Product Manager to lead our AI-powered education platform. You will work with cross-functional teams to define product strategy, prioritize features, and ensure we are building the right things for teachers and students.\n\nResponsibilities:\n- Define product vision and strategy for EdTech AI features\n- Collaborate with engineering, design, and stakeholders\n- Conduct user research and gather feedback\n- Analyze metrics and make data-driven decisions\n- Lead product launches and go-to-market planning\n\nRequirements:\n- 5+ years product management experience\n- Experience with AI/ML products\n- Strong technical background\n- Excellent communication skills\n- Passion for education technology');
                          }}
                          className="brutal-btn brutal-btn-seafoam brutal-shadow text-xs px-3 py-2"
                        >
                          🧪 Fill Test Data
                        </button>
                      </div>
                    </div>

                    <div className="brutal-box brutal-shadow p-6">
                      <h4 className="text-sm font-bold mb-4 uppercase">Job Details</h4>

                      <div className="space-y-4">
                        <div>
                          <label className="block text-xs font-bold mb-2 uppercase">Job Title</label>
                          <input
                            type="text"
                            value={jobTitle}
                            onChange={(e) => setJobTitle(e.target.value)}
                            placeholder="e.g., Senior Product Manager"
                            className="brutal-input w-full"
                          />
                        </div>

                        <div>
                          <label className="block text-xs font-bold mb-2 uppercase">Job Posting URL (Optional)</label>
                          <input
                            type="text"
                            value={jobUrl}
                            onChange={(e) => setJobUrl(e.target.value)}
                            placeholder="https://..."
                            className="brutal-input w-full"
                          />
                          <p className="text-xs text-gray-600 mt-1">
                            💡 We'll fetch company info and detect their ATS system
                          </p>
                        </div>

                        <div>
                          <label className="block text-xs font-bold mb-2 uppercase">Job Description</label>
                          <textarea
                            value={jobDescription}
                            onChange={(e) => setJobDescription(e.target.value)}
                            placeholder="Paste the full job description here..."
                            className="brutal-input w-full h-48 resize-y"
                          />
                        </div>

                        <button
                          onClick={handleAnalyzeJob}
                          disabled={!jobDescription.trim() || analyzingJob}
                          className={`brutal-btn brutal-shadow w-full disabled:opacity-50 flex items-center justify-center gap-2 ${
                            analyzingJob
                              ? 'bg-[#2d5f5d] text-white border-[#2d5f5d]'
                              : 'brutal-btn-primary'
                          }`}
                        >
                          {analyzingJob && (
                            <div className="cool-spinner h-5 w-5 border-2 border-white border-t-transparent rounded-full"></div>
                          )}
                          {analyzingJob ? 'Analyzing Job...' : '🔍 Analyze Job'}
                        </button>
                      </div>
                    </div>
                  </div>
                )
              )}
            </>
          )}
        </div>
      </main>
    </div>
  );
}
