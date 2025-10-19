'use client'

import { useState, useEffect } from 'react'
import { useToast } from './Toast'

interface ContactInfo {
  name: string
  email: string
  phone?: string
  location?: string
  linkedin?: string
  portfolio?: string
}

interface Experience {
  title: string
  company: string
  location?: string
  start_date: string
  end_date: string
  bullets: string[]
}

interface Education {
  degree: string
  institution: string
  location?: string
  graduation_date?: string
  gpa?: string
}

interface Certification {
  name: string
  issuer: string
  date_earned?: string
  expiration_date?: string
  credential_id?: string
}

interface ResumeStructure {
  contact_info: ContactInfo
  summary: string
  experience: Experience[]
  skills: { [key: string]: string[] }
  education: Education[]
  certifications: Certification[]
  optimization_report?: {
    ats_score: number
    improvements_made: string[]
    warnings: string[]
    recommendations: string[]
  }
}

interface ResumeEditorProps {
  resumeId: string
  initialData: ResumeStructure
  onSave: (data: ResumeStructure) => Promise<void>
}

export default function ResumeEditor({ resumeId, initialData, onSave }: ResumeEditorProps) {
  const { showToast } = useToast()
  const [resume, setResume] = useState<ResumeStructure | null>(initialData || null)
  const [isSaving, setIsSaving] = useState(false)
  const [activeSection, setActiveSection] = useState<string>('summary')

  if (!resume) {
    return (
      <div className="p-6">
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <p className="text-sm text-yellow-800">Loading resume data...</p>
        </div>
      </div>
    )
  }

  const handleSave = async () => {
    setIsSaving(true)
    try {
      await onSave(resume)
      showToast('Resume saved successfully!', 'success')
    } catch (error) {
      showToast('Failed to save resume', 'error')
    } finally {
      setIsSaving(false)
    }
  }

  const updateSummary = (value: string) => {
    setResume({ ...resume, summary: value })
  }

  const updateExperience = (index: number, field: keyof Experience, value: string | string[]) => {
    const newExperience = [...resume.experience]
    newExperience[index] = { ...newExperience[index], [field]: value }
    setResume({ ...resume, experience: newExperience })
  }

  const updateBullet = (expIndex: number, bulletIndex: number, value: string) => {
    const newExperience = [...resume.experience]
    const newBullets = [...newExperience[expIndex].bullets]
    newBullets[bulletIndex] = value
    newExperience[expIndex] = { ...newExperience[expIndex], bullets: newBullets }
    setResume({ ...resume, experience: newExperience })
  }

  const addBullet = (expIndex: number) => {
    const newExperience = [...resume.experience]
    newExperience[expIndex].bullets.push('')
    setResume({ ...resume, experience: newExperience })
  }

  const removeBullet = (expIndex: number, bulletIndex: number) => {
    const newExperience = [...resume.experience]
    newExperience[expIndex].bullets.splice(bulletIndex, 1)
    setResume({ ...resume, experience: newExperience })
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Header with ATS Score */}
      <div className="mb-6 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold">Resume Editor</h1>
          {resume.optimization_report && (
            <div className="mt-2">
              <span className="text-sm text-gray-600">ATS Score: </span>
              <span className={`text-lg font-bold ${
                resume.optimization_report.ats_score >= 75 ? 'text-green-600' :
                resume.optimization_report.ats_score >= 60 ? 'text-yellow-600' : 'text-red-600'
              }`}>
                {resume.optimization_report.ats_score}/100
              </span>
            </div>
          )}
        </div>
        <button
          onClick={handleSave}
          disabled={isSaving}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
        >
          {isSaving ? 'Saving...' : 'Save Resume'}
        </button>
      </div>

      {/* Section Navigation */}
      <div className="mb-6 border-b">
        <nav className="flex space-x-4">
          {['summary', 'experience', 'skills', 'education'].map((section) => (
            <button
              key={section}
              onClick={() => setActiveSection(section)}
              className={`px-4 py-2 capitalize ${
                activeSection === section
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              {section}
            </button>
          ))}
        </nav>
      </div>

      {/* Content */}
      <div className="bg-white rounded-lg shadow p-6">
        {/* Professional Summary */}
        {activeSection === 'summary' && (
          <div>
            <h2 className="text-xl font-semibold mb-4">Professional Summary</h2>
            <textarea
              value={resume.summary}
              onChange={(e) => updateSummary(e.target.value)}
              className="w-full h-32 p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="Write a compelling 3-4 sentence summary..."
            />
            <p className="mt-2 text-sm text-gray-600">
              💡 Tip: Include your job title, years of experience, and top 3-4 skills
            </p>
          </div>
        )}

        {/* Experience Section */}
        {activeSection === 'experience' && (
          <div>
            <h2 className="text-xl font-semibold mb-4">Work Experience</h2>
            {resume.experience.map((exp, expIndex) => (
              <div key={expIndex} className="mb-8 p-4 border rounded-lg">
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Job Title</label>
                    <input
                      type="text"
                      value={exp.title}
                      onChange={(e) => updateExperience(expIndex, 'title', e.target.value)}
                      className="w-full p-2 border rounded"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Company</label>
                    <input
                      type="text"
                      value={exp.company}
                      onChange={(e) => updateExperience(expIndex, 'company', e.target.value)}
                      className="w-full p-2 border rounded"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Start Date</label>
                    <input
                      type="text"
                      value={exp.start_date}
                      onChange={(e) => updateExperience(expIndex, 'start_date', e.target.value)}
                      className="w-full p-2 border rounded"
                      placeholder="January 2020"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">End Date</label>
                    <input
                      type="text"
                      value={exp.end_date}
                      onChange={(e) => updateExperience(expIndex, 'end_date', e.target.value)}
                      className="w-full p-2 border rounded"
                      placeholder="Present"
                    />
                  </div>
                </div>

                {/* Bullets */}
                <div>
                  <label className="block text-sm font-medium mb-2">Accomplishments</label>
                  {exp.bullets.map((bullet, bulletIndex) => (
                    <div key={bulletIndex} className="flex gap-2 mb-2">
                      <span className="text-gray-600 mt-2">•</span>
                      <textarea
                        value={bullet.replace(/^•\s*/, '')}
                        onChange={(e) => updateBullet(expIndex, bulletIndex, e.target.value)}
                        className="flex-1 p-2 border rounded focus:ring-2 focus:ring-blue-500"
                        rows={2}
                        placeholder="[Action Verb] + [What You Did] + [Quantifiable Result]"
                      />
                      <button
                        onClick={() => removeBullet(expIndex, bulletIndex)}
                        className="px-3 py-1 text-red-600 hover:bg-red-50 rounded"
                      >
                        ✕
                      </button>
                    </div>
                  ))}
                  <button
                    onClick={() => addBullet(expIndex)}
                    className="mt-2 px-4 py-2 text-sm text-blue-600 hover:bg-blue-50 rounded"
                  >
                    + Add Bullet Point
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Skills Section */}
        {activeSection === 'skills' && (
          <div>
            <h2 className="text-xl font-semibold mb-4">Skills</h2>
            {Object.entries(resume.skills).map(([category, skillList]) => (
              <div key={category} className="mb-4">
                <label className="block text-sm font-medium mb-2">{category}</label>
                <input
                  type="text"
                  value={skillList.join(', ')}
                  onChange={(e) => {
                    const newSkills = { ...resume.skills }
                    newSkills[category] = e.target.value.split(',').map(s => s.trim())
                    setResume({ ...resume, skills: newSkills })
                  }}
                  className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
                  placeholder="Skill1, Skill2, Skill3"
                />
              </div>
            ))}
          </div>
        )}

        {/* Education Section */}
        {activeSection === 'education' && (
          <div>
            <h2 className="text-xl font-semibold mb-4">Education</h2>
            {resume.education.map((edu, index) => (
              <div key={index} className="mb-4 p-4 border rounded-lg">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Degree</label>
                    <input
                      type="text"
                      value={edu.degree || ''}
                      className="w-full p-2 border rounded"
                      readOnly
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Institution</label>
                    <input
                      type="text"
                      value={edu.institution || ''}
                      className="w-full p-2 border rounded"
                      readOnly
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Optimization Report */}
      {resume.optimization_report && (
        <div className="mt-6 bg-gray-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4">ATS Optimization Report</h3>

          {resume.optimization_report.recommendations.length > 0 && (
            <div className="mb-4">
              <h4 className="font-medium mb-2">Recommendations:</h4>
              <ul className="list-disc list-inside space-y-1">
                {resume.optimization_report.recommendations.map((rec, i) => (
                  <li key={i} className="text-sm text-gray-700">{rec}</li>
                ))}
              </ul>
            </div>
          )}

          {resume.optimization_report.warnings.length > 0 && (
            <div className="mb-4">
              <h4 className="font-medium mb-2 text-yellow-700">Warnings:</h4>
              <ul className="list-disc list-inside space-y-1">
                {resume.optimization_report.warnings.map((warning, i) => (
                  <li key={i} className="text-sm text-yellow-700">{warning}</li>
                ))}
              </ul>
            </div>
          )}

          {resume.optimization_report.improvements_made.length > 0 && (
            <div>
              <h4 className="font-medium mb-2 text-green-700">Improvements Made:</h4>
              <ul className="list-disc list-inside space-y-1">
                {resume.optimization_report.improvements_made.slice(0, 5).map((imp, i) => (
                  <li key={i} className="text-sm text-green-700">{imp}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
