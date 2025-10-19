'use client';

import { useEffect, useState, useCallback } from 'react';
import { supabase } from '@/lib/supabase';
import { useRouter } from 'next/navigation';
import UploadResume from '@/components/UploadResume';
import ImportConversation from '@/components/ImportConversation';
import ConversationInterface from '@/components/ConversationInterface';
import JobConfirmation from '@/components/JobConfirmation';
import GenericResumeGenerator from '@/components/GenericResumeGenerator';
import { knowledgeApi, SummaryResponse } from '@/lib/api/knowledge';
import { User } from '@supabase/supabase-js';
import { Navigation, Button, Card, Input } from '@/components/ui';

interface JobData {
  title: string;
  company?: string;
  location?: string;
  url?: string;
  description: string;
  requirements?: string[];
  keywords?: string[];
  ats_system?: string;
  company_info?: {
    website?: string;
    linkedin?: string;
    values?: string[];
    about?: string;
  };
}

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'conversation' | 'upload' | 'import' | 'generate'>('conversation');
  const [pendingCount, setPendingCount] = useState(0);

  // Resume generation state
  const [analyzingJob, setAnalyzingJob] = useState(false);
  const [generatingResume, setGeneratingResume] = useState(false);
  const [jobTitle, setJobTitle] = useState('');
  const [jobUrl, setJobUrl] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [jobData, setJobData] = useState<JobData | null>(null);
  const [showJobConfirmation, setShowJobConfirmation] = useState(false);
  const [resumeType, setResumeType] = useState<'job-specific' | 'generic'>('job-specific');
  const [error, setError] = useState<string | null>(null);
  const [confirmedCount, setConfirmedCount] = useState(0);
  const [knowledgeSummary, setKnowledgeSummary] = useState<SummaryResponse | null>(null);

  const router = useRouter();

  const checkUser = useCallback(async () => {
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
  }, [router]);

  useEffect(() => {
    checkUser();
  }, [checkUser]);

  const handleLogout = async () => {
    await supabase.auth.signOut();
    router.push('/');
  };

  const handleAnalyzeJob = async () => {
    if (!user) {
      setError('User not authenticated');
      return;
    }

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

  const handleJobEdit = (field: string, value: string | string[] | JobData['company_info']) => {
    setJobData((prev) => {
      if (!prev) return prev;
      return {
        ...prev,
        [field]: value
      };
    });
  };

  const handleJobCancel = () => {
    setShowJobConfirmation(false);
    setJobData(null);
    setError(null);
  };

  const handleJobConfirm = async (confirmedData: JobData) => {
    if (!user) {
      setError('User not authenticated');
      return;
    }

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
    <div className="min-h-screen bg-gray-50 page-enter">
      <Navigation
        user={user ? { email: user.email || '', name: user.user_metadata?.full_name } : undefined}
        onLogout={handleLogout}
        links={[
          { label: 'Dashboard', href: '/dashboard', icon: '🏠' },
          { label: 'Resumes', href: '/resumes', icon: '📄' },
        ]}
        badge={pendingCount > 0 ? { count: pendingCount, href: '/dashboard/knowledge' } : undefined}
      />

      <main className="max-w-7xl mx-auto px-6 py-8">
        <Card variant="seafoam" padding="lg" className="mb-8">
          <h2 className="text-2xl mb-2">Welcome back, {user?.email?.split('@')[0]}!</h2>
          <p className="text-sm text-gray-700">Let's build your next winning resume</p>
        </Card>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Main content area - 2 columns on large screens */}
          <div className="lg:col-span-2 space-y-6">
            {/* Pending facts alert */}
            {pendingCount > 0 && (
              <Card variant="default" padding="lg" className="bg-yellow-50 border-yellow-600">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <p className="text-sm font-bold uppercase mb-2">⚠ {pendingCount} Facts Pending Review</p>
                    <p className="text-sm text-gray-700">
                      Review and confirm the facts I extracted from your conversation
                    </p>
                  </div>
                  <Button
                    variant="primary"
                    size="sm"
                    onClick={() => router.push('/dashboard/knowledge/confirm')}
                  >
                    Review Now
                  </Button>
                </div>
              </Card>
            )}

            <Card variant="seafoam" padding="lg">
              <h3 className="text-lg font-bold uppercase mb-2">Build Your Knowledge Base</h3>
              <p className="text-sm text-gray-700 mb-6">Add your experience through conversation, uploads, or imports</p>

              <div className="grid grid-cols-3 gap-3">
                <Button
                  variant={activeTab === 'conversation' ? 'primary' : 'secondary'}
                  size="md"
                  onClick={() => setActiveTab('conversation')}
                  className="py-4 flex-col"
                >
                  💬<br/>Conversation
                </Button>
                <Button
                  variant={activeTab === 'upload' ? 'primary' : 'secondary'}
                  size="md"
                  onClick={() => setActiveTab('upload')}
                  className="py-4 flex-col"
                >
                  📄<br/>Upload
                </Button>
                <Button
                  variant={activeTab === 'import' ? 'primary' : 'secondary'}
                  size="md"
                  onClick={() => setActiveTab('import')}
                  className="py-4 flex-col"
                >
                  📋<br/>Import
                </Button>
              </div>
            </Card>
          </div>

          {/* Sidebar - 1 column on large screens */}
          <div className="space-y-6">
            <Card variant="dark" padding="lg" className="text-center">
              <p className="text-sm font-bold mb-3 uppercase tracking-wide">Ready to Apply?</p>
              <Button
                variant="secondary"
                size="md"
                icon="✨"
                onClick={() => setActiveTab('generate')}
                className="w-full bg-white text-black border-white hover:bg-gray-100"
              >
                Generate Resume
              </Button>
            </Card>

            {/* Knowledge base stats */}
            {knowledgeSummary && (
              <Card variant="default" padding="lg">
                <h4 className="text-xs font-bold uppercase mb-4 text-gray-600">Knowledge Base</h4>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Confirmed</span>
                    <span className="text-xl font-bold">{confirmedCount}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Pending</span>
                    <span className="text-xl font-bold text-yellow-600">{pendingCount}</span>
                  </div>
                </div>
              </Card>
            )}
          </div>
        </div>

        <div>
          {activeTab === 'conversation' && user && <ConversationInterface userId={user.id} />}
          {activeTab === 'upload' && <UploadResume />}
          {activeTab === 'import' && <ImportConversation />}
          {activeTab === 'generate' && user && (
            <>
              {/* Knowledge Confirmation Gate */}
              {confirmedCount < 3 && (
                <Card variant="default" padding="lg" className="bg-orange-50 border-orange-600 mb-6">
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
                        <Card variant="seafoam" padding="sm" className="text-center">
                          <div className="text-2xl font-bold">{confirmedCount}</div>
                          <div className="text-xs">Confirmed</div>
                        </Card>
                        <Card variant="default" padding="sm" className="bg-yellow-50 text-center">
                          <div className="text-2xl font-bold">{pendingCount}</div>
                          <div className="text-xs">Pending</div>
                        </Card>
                      </div>
                      <div className="flex gap-3">
                        <Button
                          variant="primary"
                          icon="📚"
                          onClick={() => router.push('/dashboard/knowledge/confirm')}
                        >
                          Review Facts First (Recommended)
                        </Button>
                        <Button
                          variant="secondary"
                          size="sm"
                          icon="⚠️"
                          onClick={() => {/* Allow to continue */}}
                        >
                          Generate Anyway (Risky)
                        </Button>
                      </div>
                    </div>
                  </div>
                </Card>
              )}

              {confirmedCount >= 3 && (
                <Card variant="default" padding="md" className="bg-green-50 border-green-600 mb-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-bold">✅ Knowledge Base Ready</p>
                      <p className="text-xs mt-1">
                        {confirmedCount} confirmed facts • Ready to generate accurate resumes
                      </p>
                    </div>
                  </div>
                </Card>
              )}

              {/* Resume Type Toggle */}
              <div className="mb-6">
                <Card variant="seafoam" padding="md" className="mb-4">
                  <p className="text-sm font-bold uppercase">Resume Type</p>
                  <p className="text-xs mt-1">Choose how you want to create your resume</p>
                </Card>

                <div className="flex gap-4">
                  <Button
                    variant={resumeType === 'job-specific' ? 'primary' : 'secondary'}
                    icon="🎯"
                    onClick={() => setResumeType('job-specific')}
                    className="flex-1"
                  >
                    Job-Specific Resume
                  </Button>
                  <Button
                    variant={resumeType === 'generic' ? 'primary' : 'secondary'}
                    icon="⚡"
                    onClick={() => setResumeType('generic')}
                    className="flex-1"
                  >
                    Quick Generic Resume
                  </Button>
                </div>
              </div>

              {/* Global Error Display */}
              {error && (
                <Card variant="default" padding="md" className="bg-red-50 border-red-600 mb-6">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="text-sm font-bold uppercase mb-1">Error</p>
                      <p className="text-sm">{error}</p>
                    </div>
                    <Button
                      variant="secondary"
                      size="sm"
                      onClick={() => setError(null)}
                    >
                      Dismiss
                    </Button>
                  </div>
                </Card>
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

                    <Card variant="seafoam" padding="lg">
                      <div className="flex justify-between items-start">
                        <div>
                          <h3 className="text-xl mb-2">Generate Targeted Resume</h3>
                          <p className="text-sm">Tell me about the job you're applying for</p>
                        </div>
                        <Button
                          variant="secondary"
                          size="sm"
                          icon="🧪"
                          onClick={() => {
                            setJobTitle('Product Manager');
                            setJobUrl('https://www.magicschool.ai/careers');
                            setJobDescription('We are looking for a Product Manager to lead our AI-powered education platform. You will work with cross-functional teams to define product strategy, prioritize features, and ensure we are building the right things for teachers and students.\n\nResponsibilities:\n- Define product vision and strategy for EdTech AI features\n- Collaborate with engineering, design, and stakeholders\n- Conduct user research and gather feedback\n- Analyze metrics and make data-driven decisions\n- Lead product launches and go-to-market planning\n\nRequirements:\n- 5+ years product management experience\n- Experience with AI/ML products\n- Strong technical background\n- Excellent communication skills\n- Passion for education technology');
                          }}
                        >
                          Fill Test Data
                        </Button>
                      </div>
                    </Card>

                    <Card variant="default" padding="lg">
                      <h4 className="text-sm font-bold mb-4 uppercase">Job Details</h4>

                      <div className="space-y-4">
                        <Input
                          label="Job Title"
                          type="text"
                          value={jobTitle}
                          onChange={setJobTitle}
                          placeholder="e.g., Senior Product Manager"
                        />

                        <Input
                          label="Job Posting URL (Optional)"
                          type="text"
                          value={jobUrl}
                          onChange={setJobUrl}
                          placeholder="https://..."
                          helperText="💡 We'll fetch company info and detect their ATS system"
                        />

                        <Input
                          label="Job Description"
                          type="textarea"
                          value={jobDescription}
                          onChange={setJobDescription}
                          placeholder="Paste the full job description here..."
                          rows={8}
                        />

                        <Button
                          variant="primary"
                          size="lg"
                          icon="🔍"
                          loading={analyzingJob}
                          disabled={!jobDescription.trim()}
                          onClick={handleAnalyzeJob}
                          className="w-full"
                        >
                          Analyze Job
                        </Button>
                      </div>
                    </Card>
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
