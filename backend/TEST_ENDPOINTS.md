# Resumaker Backend - API Endpoint Testing Guide

## Setup

1. Start the server:
```bash
cd /Users/evanstoudt/Documents/File\ Cabinet/Coding/resumaker/backend
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

2. Server will be available at: `http://localhost:8000`
3. API Documentation: `http://localhost:8000/docs`

## Test User ID

For testing, use a dummy user_id (in production, this would come from auth):
```bash
export TEST_USER_ID="00000000-0000-0000-0000-000000000001"
```

---

## 1. Upload Resume Endpoint (Enhanced with DOCX/DOC/TXT Support)

### Upload PDF Resume
```bash
curl -X POST "http://localhost:8000/upload/resume" \
  -F "file=@/path/to/resume.pdf"
```

### Upload DOCX Resume
```bash
curl -X POST "http://localhost:8000/upload/resume" \
  -F "file=@/path/to/resume.docx"
```

### Upload TXT Resume
```bash
curl -X POST "http://localhost:8000/upload/resume" \
  -F "file=@/path/to/resume.txt"
```

### Expected Response:
```json
{
  "success": true,
  "file_id": "uuid-here",
  "file_name": "resume.pdf",
  "extracted_data": {
    "personal_info": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1-555-0123"
    },
    "experience": [...],
    "education": [...],
    "skills": {...}
  }
}
```

---

## 2. Job Analysis Endpoint (NEW)

### Analyze a Job Posting
```bash
curl -X POST "http://localhost:8000/jobs/analyze?user_id=$TEST_USER_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Senior Software Engineer needed for fast-growing startup. We are looking for someone with 5+ years of experience in Python, FastAPI, and PostgreSQL. Must have experience with AWS cloud services and CI/CD pipelines. Bonus points for experience with React and TypeScript. Responsibilities include designing scalable backend systems, mentoring junior developers, and leading technical projects. Required: Python, FastAPI, PostgreSQL, AWS, Docker. Preferred: React, TypeScript, Kubernetes, Redis.",
    "job_url": "https://jobs.lever.co/example/senior-engineer",
    "company_name": "TechStartup Inc"
  }'
```

### Expected Response:
```json
{
  "success": true,
  "job_id": "uuid-of-job-posting",
  "analysis": {
    "job_title": "Senior Software Engineer",
    "company": "TechStartup Inc",
    "ats_system_detected": "Lever",
    "ats_system_id": "uuid-of-ats-system",
    "keywords": {
      "all": ["Python", "FastAPI", "PostgreSQL", "AWS", "Docker", "React", "TypeScript", ...],
      "required": ["Python", "FastAPI", "PostgreSQL", "AWS", "Docker"],
      "preferred": ["React", "TypeScript", "Kubernetes", "Redis"],
      "categorized": {
        "technical_skills": ["Python", "FastAPI", "PostgreSQL"],
        "tools": ["AWS", "Docker", "Kubernetes"],
        ...
      }
    },
    "requirements": {
      "required": ["5+ years experience", "Python expertise", ...],
      "preferred": ["React knowledge", "TypeScript experience", ...]
    },
    "experience_level": "senior",
    "keyword_count": 20,
    "required_count": 5,
    "preferred_count": 4
  }
}
```

---

## 3. Resume Generation Endpoint (Enhanced)

### Generate Resume for a Job Posting
```bash
curl -X POST "http://localhost:8000/resumes/generate?user_id=$TEST_USER_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "job_posting_id": "uuid-from-job-analyze",
    "target_role": "Senior Software Engineer"
  }'
```

### Generate Generic Resume (No Job Targeting)
```bash
curl -X POST "http://localhost:8000/resumes/generate?user_id=$TEST_USER_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "target_role": "Software Engineer"
  }'
```

### Expected Response:
```json
{
  "success": true,
  "resume_version_id": "uuid-of-resume-version",
  "resume": {
    "contact_info": {...},
    "summary": "Experienced Software Engineer with 5+ years...",
    "experience": [...],
    "skills": {...},
    "education": [...],
    "certifications": [...],
    "optimization_report": {
      "ats_score": 87,
      "keyword_matches": 18,
      "suggestions": [...]
    }
  },
  "html": "<html>...</html>",
  "verification": {
    "verification_report": {
      "total_checks": 25,
      "passed": 23,
      "flagged": 2
    },
    "flags": [...],
    "requires_review": false
  },
  "ats_score": 87
}
```

---

## 4. Fact Checking Endpoint (Built-in)

### Get Truth Flags for Resume
```bash
curl "http://localhost:8000/resumes/{resume_id}/flags?user_id=$TEST_USER_ID"
```

### Re-verify Resume
```bash
curl -X POST "http://localhost:8000/resumes/{resume_id}/verify?user_id=$TEST_USER_ID"
```

### Resolve a Flag
```bash
curl -X POST "http://localhost:8000/resumes/flags/{flag_id}/resolve?user_id=$TEST_USER_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "resolution_notes": "Verified with employment records"
  }'
```

### Expected Flag Response:
```json
{
  "flags": [
    {
      "id": "uuid",
      "section": "experience_0",
      "claim_text": "Increased revenue by 250%",
      "flag_reason": "quantification_unsupported",
      "severity": "medium",
      "explanation": "No evidence found for 250% revenue increase claim",
      "suggested_fix": "Add supporting metric or reduce claim",
      "resolved": false,
      "created_at": "2025-01-08T10:00:00Z"
    }
  ]
}
```

---

## 5. PDF Export Endpoint

### Export Resume as PDF
```bash
curl -X GET "http://localhost:8000/resumes/{resume_id}/export/pdf?user_id=$TEST_USER_ID" \
  --output resume.pdf
```

### Test PDF Download
```bash
# After generating a resume, use its ID:
RESUME_ID="your-resume-id-here"
curl -X GET "http://localhost:8000/resumes/$RESUME_ID/export/pdf?user_id=$TEST_USER_ID" \
  --output test_resume.pdf

# Verify file was created
ls -lh test_resume.pdf
```

---

## 6. DOCX Export Endpoint

### Export Resume as DOCX
```bash
curl -X GET "http://localhost:8000/resumes/{resume_id}/export/docx?user_id=$TEST_USER_ID" \
  --output resume.docx
```

### Test DOCX Download
```bash
RESUME_ID="your-resume-id-here"
curl -X GET "http://localhost:8000/resumes/$RESUME_ID/export/docx?user_id=$TEST_USER_ID" \
  --output test_resume.docx

# Verify file was created
ls -lh test_resume.docx
```

---

## Additional Endpoints

### List All Resumes
```bash
curl "http://localhost:8000/resumes/list?user_id=$TEST_USER_ID"
```

### Get Resume Details
```bash
curl "http://localhost:8000/resumes/{resume_id}?user_id=$TEST_USER_ID"
```

### List All Job Postings
```bash
curl "http://localhost:8000/jobs/list?user_id=$TEST_USER_ID"
```

### Get Job Posting Keywords
```bash
curl "http://localhost:8000/jobs/{job_id}/keywords?user_id=$TEST_USER_ID"
```

### Analyze Resume Match to Job
```bash
curl -X POST "http://localhost:8000/jobs/analyze-match?user_id=$TEST_USER_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "uuid-of-job",
    "resume_id": "uuid-of-resume"
  }'
```

---

## Testing Workflow

1. **Upload a resume** to extract baseline data
2. **Analyze a job posting** to get keywords and requirements
3. **Generate a tailored resume** using the job posting ID
4. **Check truth flags** to verify all claims are backed by evidence
5. **Export as PDF/DOCX** for job applications

### Full Example Workflow:
```bash
# 1. Set user ID
export TEST_USER_ID="00000000-0000-0000-0000-000000000001"

# 2. Analyze job posting
JOB_RESPONSE=$(curl -s -X POST "http://localhost:8000/jobs/analyze?user_id=$TEST_USER_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Senior Python Developer needed...",
    "company_name": "Tech Corp"
  }')

JOB_ID=$(echo $JOB_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['job_id'])")

# 3. Generate resume
RESUME_RESPONSE=$(curl -s -X POST "http://localhost:8000/resumes/generate?user_id=$TEST_USER_ID" \
  -H "Content-Type: application/json" \
  -d "{\"job_posting_id\": \"$JOB_ID\"}")

RESUME_ID=$(echo $RESUME_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['resume_version_id'])")

# 4. Check flags
curl "http://localhost:8000/resumes/$RESUME_ID/flags?user_id=$TEST_USER_ID"

# 5. Export as PDF
curl -X GET "http://localhost:8000/resumes/$RESUME_ID/export/pdf?user_id=$TEST_USER_ID" \
  --output final_resume.pdf

echo "Resume generated and exported to final_resume.pdf"
```

---

## Error Handling

All endpoints return proper error responses:

### Example Error Response:
```json
{
  "detail": "Job analysis failed: API key not found"
}
```

### Common HTTP Status Codes:
- `200` - Success
- `400` - Bad request (invalid file type, missing parameters)
- `404` - Resource not found
- `500` - Server error

---

## Dependencies Required

Ensure these are installed:
```bash
pip install python-docx  # For DOCX reading/writing
pip install anthropic    # For Claude API
pip install weasyprint   # For PDF generation
```

For .doc file support (optional):
```bash
# macOS
brew install antiword

# Linux
sudo apt-get install antiword
```

---

## Environment Variables

Make sure `.env` file contains:
```
CLAUDE_API_KEY=your-claude-api-key
GEMINI_API_KEY=your-gemini-api-key
SUPABASE_URL=your-supabase-url
SUPABASE_SECRET_KEY=your-service-key
```
