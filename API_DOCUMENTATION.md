# 📡 Resumaker API Documentation

Complete API reference for Resumaker backend.

**Base URL:** `http://localhost:8000` (development) or `https://your-app.railway.app` (production)

---

## 🔐 Authentication

All endpoints (except health check) require authentication via Supabase.

**Header:**
```
Authorization: Bearer <supabase_jwt_token>
```

In development, endpoints use `user_id` query parameter for testing.

---

## 📚 API Overview

### Routers
1. **Auth** (`/auth`) - Authentication and user management
2. **Upload** (`/upload`) - Resume file uploads and OCR
3. **Imports** (`/imports`) - Conversation imports
4. **Conversation** (`/conversation`) - AI interview system
5. **References** (`/references`) - Reference request management
6. **Resumes** (`/resumes`) - Resume generation and management
7. **Jobs** (`/jobs`) - Job posting and matching

---

## 🔑 Auth Router

### `POST /auth/signup`
Create new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe"
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "user_id": "uuid",
  "email": "user@example.com"
}
```

### `POST /auth/login`
Authenticate user.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "token": "jwt_token_here",
  "user": {
    "id": "uuid",
    "email": "user@example.com"
  }
}
```

### `POST /auth/logout`
Log out user.

**Response:** `200 OK`
```json
{
  "success": true
}
```

---

## 📤 Upload Router

### `POST /upload/resume`
Upload resume file for OCR processing.

**Request:** `multipart/form-data`
```
file: <resume.pdf|resume.docx|resume.png|resume.jpg>
user_id: uuid
```

**Response:** `200 OK`
```json
{
  "success": true,
  "extracted_data": {
    "work_history": [...],
    "skills": [...],
    "education": [...],
    "accomplishments": [...]
  },
  "entries_added": 25
}
```

**Supported formats:** PDF, DOCX, PNG, JPG

---

## 📥 Imports Router

### `POST /imports/conversation`
Import ChatGPT or Claude conversation.

**Request:**
```json
{
  "conversation_text": "Full conversation text here...",
  "source": "chatgpt",  // or "claude"
  "user_id": "uuid"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "import_id": "uuid",
  "entries_extracted": 15,
  "knowledge_base_entries": [
    {
      "type": "accomplishment",
      "title": "Led team to 30% growth",
      "content": {...}
    }
  ]
}
```

---

## 💬 Conversation Router

### `POST /conversation/start`
Start AI interview session.

**Request:**
```json
{
  "user_id": "uuid"
}
```

**Response:** `200 OK`
```json
{
  "conversation_id": "uuid",
  "first_question": "What is your current or most recent job title?",
  "question_number": 1,
  "total_questions": 40
}
```

### `POST /conversation/answer`
Submit answer to current question.

**Request:**
```json
{
  "conversation_id": "uuid",
  "answer": "Senior Software Engineer at Tech Corp"
}
```

**Response:** `200 OK`
```json
{
  "next_question": "What were your main responsibilities?",
  "question_number": 2,
  "total_questions": 40,
  "completed": false
}
```

### `GET /conversation/{conversation_id}`
Get conversation status.

**Response:** `200 OK`
```json
{
  "conversation_id": "uuid",
  "status": "active",
  "questions_answered": 15,
  "total_questions": 40,
  "progress_percentage": 37.5
}
```

---

## 👥 References Router

### `POST /references/generate-prompt`
Generate shareable reference request prompt.

**Request:**
```json
{
  "user_id": "uuid",
  "reference_name": "Jane Smith",
  "reference_email": "jane@example.com",
  "relationship": "manager"
}
```

**Response:** `200 OK`
```json
{
  "request_id": "uuid",
  "shareable_url": "https://resumaker.com/ref/abc123",
  "prompt_text": "Hi Jane, I'm building my resume...",
  "expires_at": "2025-11-06T00:00:00Z"
}
```

### `POST /references/{request_id}/submit`
Submit reference response (public endpoint).

**Request:**
```json
{
  "response_text": "John was an exceptional team member..."
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "entries_extracted": 8
}
```

---

## 📝 Resumes Router

### `POST /resumes/generate`
Generate new resume from knowledge base.

**Request:**
```json
{
  "user_id": "uuid",
  "job_description": "Optional job description text...",
  "target_role": "Senior Software Engineer",
  "job_posting_id": "uuid (optional)"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "resume_version_id": "uuid",
  "resume": {
    "contact_info": {...},
    "summary": "...",
    "experience": [...],
    "skills": {...},
    "education": [...],
    "optimization_report": {
      "ats_score": 82,
      "improvements_made": [...],
      "warnings": [...],
      "recommendations": [...]
    }
  },
  "verification": {
    "verification_report": {
      "total_checks": 45,
      "passed": 40,
      "flagged": 5
    },
    "flags": [...],
    "requires_review": true
  },
  "ats_score": 82
}
```

### `GET /resumes/list?user_id={uuid}`
List all resumes for user.

**Response:** `200 OK`
```json
{
  "resumes": [
    {
      "id": "uuid",
      "version": 1,
      "status": "truth_check_pending",
      "created_at": "2025-10-06T12:00:00Z",
      "job_title": "Software Engineer",
      "company": "Tech Corp",
      "ats_score": 82
    }
  ]
}
```

### `GET /resumes/{resume_id}?user_id={uuid}`
Get full resume details.

**Response:** `200 OK`
```json
{
  "resume": {
    "id": "uuid",
    "user_id": "uuid",
    "resume_structure": {...},
    "html_content": "...",
    "status": "truth_check_pending",
    "version_number": 1,
    "created_at": "..."
  },
  "flags": [...]
}
```

### `PUT /resumes/{resume_id}?user_id={uuid}`
Update resume structure.

**Request:**
```json
{
  "resume_structure": {
    "contact_info": {...},
    "summary": "Updated summary...",
    "experience": [...],
    "skills": {...}
  }
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "resume": {...},
  "html": "..."
}
```

### `POST /resumes/{resume_id}/verify?user_id={uuid}`
Re-run truth verification.

**Response:** `200 OK`
```json
{
  "success": true,
  "verification": {
    "verification_report": {...},
    "flags": [...]
  }
}
```

### `GET /resumes/{resume_id}/flags?user_id={uuid}`
Get truth check flags.

**Response:** `200 OK`
```json
{
  "flags": [
    {
      "id": "uuid",
      "section": "experience_0",
      "claim_text": "Increased revenue by 150%",
      "flag_reason": "quantification_unsupported",
      "severity": "high",
      "explanation": "No evidence found for 150% increase",
      "suggested_fix": "Add specific metrics or reduce claim",
      "resolved": false
    }
  ]
}
```

### `POST /resumes/flags/{flag_id}/resolve?user_id={uuid}`
Resolve a truth check flag.

**Request:**
```json
{
  "resolution_notes": "Updated with actual Q2 2023 revenue data showing 148% increase"
}
```

**Response:** `200 OK`
```json
{
  "success": true
}
```

### `POST /resumes/{resume_id}/finalize?user_id={uuid}`
Mark resume as finalized.

**Response:** `200 OK`
```json
{
  "success": true
}
```

**Or if blocked:**
```json
{
  "success": false,
  "error": "Cannot finalize resume with unresolved critical flags",
  "unresolved_count": 3
}
```

### `GET /resumes/{resume_id}/export/html?user_id={uuid}`
Export resume as HTML.

**Response:** `200 OK`
```json
{
  "html": "<!DOCTYPE html>..."
}
```

### `GET /resumes/{resume_id}/export/pdf?user_id={uuid}`
Download resume as PDF.

**Response:** `200 OK` (binary file)
```
Content-Type: application/pdf
Content-Disposition: attachment; filename=John_Doe_Resume.pdf
```

### `GET /resumes/{resume_id}/export/docx?user_id={uuid}`
Download resume as DOCX.

**Response:** `200 OK` (binary file)
```
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
Content-Disposition: attachment; filename=John_Doe_Resume.docx
```

### `GET /resumes/stats/verification?user_id={uuid}`
Get verification statistics.

**Response:** `200 OK`
```json
{
  "total_resumes": 5,
  "total_flags": 12,
  "unresolved_flags": 3,
  "severity_breakdown": {
    "low": 1,
    "medium": 1,
    "high": 1
  },
  "truth_score": 85.5
}
```

---

## 💼 Jobs Router

### `POST /jobs/add`
Add and parse job posting.

**Request:**
```json
{
  "job_description": "Full job description text...",
  "job_url": "https://company.com/careers/job-id",
  "company_name": "Tech Corp",
  "user_id": "uuid"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "job_id": "uuid",
  "job_data": {
    "job_title": "Senior Software Engineer",
    "company": "Tech Corp",
    "ats_system": "workday",
    "keywords": {
      "all": ["Python", "AWS", "Kubernetes", ...],
      "required": ["Python", "AWS"],
      "preferred": ["Kubernetes", "Docker"]
    },
    "requirements": {
      "required": ["5+ years experience", ...],
      "preferred": ["Master's degree", ...]
    },
    "experience_level": "senior"
  }
}
```

### `GET /jobs/list?user_id={uuid}`
List all job postings.

**Response:** `200 OK`
```json
{
  "jobs": [
    {
      "id": "uuid",
      "job_title": "Senior Software Engineer",
      "company_name": "Tech Corp",
      "created_at": "2025-10-06T12:00:00Z",
      "extracted_keywords": [...]
    }
  ]
}
```

### `GET /jobs/{job_id}?user_id={uuid}`
Get job posting details.

**Response:** `200 OK`
```json
{
  "job": {
    "id": "uuid",
    "job_title": "...",
    "company_name": "...",
    "job_url": "...",
    "description_text": "...",
    "extracted_keywords": [...],
    "required_skills": [...],
    "preferred_skills": [...],
    "ats_system_details": {...}
  }
}
```

### `POST /jobs/analyze-match`
Analyze resume-job match.

**Request:**
```json
{
  "job_id": "uuid",
  "resume_id": "uuid",
  "user_id": "uuid"
}
```

**Response:** `200 OK`
```json
{
  "match_analysis": {
    "match_score": 78.5,
    "match_level": "good",
    "required_match": 85.0,
    "preferred_match": 60.0,
    "overall_match": 75.0,
    "matched_keywords": {
      "required": ["Python", "AWS"],
      "preferred": ["Docker"],
      "all": [...]
    },
    "missing_keywords": {
      "required": ["Kubernetes"],
      "all": [...]
    },
    "recommendations": [
      "CRITICAL: Add these required keywords: Kubernetes",
      "Consider adding if applicable: Redis, GraphQL"
    ],
    "ats_compatibility": [
      "Use 'Apply with LinkedIn' for fastest application",
      "Answer knockout questions carefully"
    ]
  },
  "keyword_density": {
    "total_keywords": 20,
    "matched_keywords": 15,
    "match_rate": 75.0,
    "density": 2.5,
    "recommendation": "Good keyword match (75%+)"
  }
}
```

### `GET /jobs/{job_id}/keywords?user_id={uuid}`
Get extracted keywords.

**Response:** `200 OK`
```json
{
  "all_keywords": [...],
  "required": [...],
  "preferred": [...]
}
```

### `DELETE /jobs/{job_id}?user_id={uuid}`
Delete job posting.

**Response:** `200 OK`
```json
{
  "success": true
}
```

### `GET /jobs/ats-systems/list`
List known ATS systems.

**Response:** `200 OK`
```json
{
  "ats_systems": [
    {
      "id": "uuid",
      "system_name": "workday",
      "company_count": 5000,
      "parsing_quality": "good",
      "recommendations": [...]
    }
  ]
}
```

---

## 🏥 Health Check

### `GET /health`
Check API health and service availability.

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "database": "connected",
  "services": {
    "claude": "available",
    "gemini": "available",
    "supabase": "available"
  }
}
```

---

## ❌ Error Responses

All endpoints return consistent error format:

### `400 Bad Request`
```json
{
  "detail": "Invalid request parameters"
}
```

### `401 Unauthorized`
```json
{
  "detail": "Authentication required"
}
```

### `404 Not Found`
```json
{
  "detail": "Resource not found"
}
```

### `500 Internal Server Error`
```json
{
  "detail": "Internal server error message"
}
```

---

## 📊 Rate Limits

**Development:** No limits
**Production:** TBD based on deployment platform

---

## 🔧 Testing Endpoints

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Generate resume
curl -X POST http://localhost:8000/resumes/generate \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test-uuid", "target_role": "Software Engineer"}'

# List resumes
curl http://localhost:8000/resumes/list?user_id=test-uuid

# Download PDF
curl -O -J http://localhost:8000/resumes/{resume-id}/export/pdf?user_id=test-uuid
```

### Using Python

```python
import requests

# Generate resume
response = requests.post(
    "http://localhost:8000/resumes/generate",
    json={
        "user_id": "test-uuid",
        "target_role": "Software Engineer"
    }
)

resume_data = response.json()
print(f"ATS Score: {resume_data['ats_score']}")
```

---

## 🚀 API Best Practices

1. **Always include user_id** (in development)
2. **Handle errors gracefully** - Check status codes
3. **Verify file uploads** - Check file size and type
4. **Poll for long operations** - Some operations take time
5. **Cache responses** - Reduce API calls where possible
6. **Use HTTPS in production** - Never send credentials over HTTP

---

**API Version:** 1.0.0
**Last Updated:** October 6, 2025
