# Backend Testing Guide

Quick reference for testing the new backend endpoints.

## Prerequisites

```bash
cd backend
source venv/bin/activate  # or activate your virtual environment
uvicorn main:app --reload
```

Server should start at: `http://localhost:8000`

## Test User Setup

You'll need a test user ID. Create one via the auth endpoint or use an existing user.

```bash
# Get auth token
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'

# Save the user_id from response
```

---

## 1. Test Web Scraper (Jobs Analysis)

### Scrape and analyze a job posting URL:

```bash
curl -X POST http://localhost:8000/jobs/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "job_url": "https://boards.greenhouse.io/embed/job_app?token=your-job-id",
    "user_id": "YOUR_USER_ID_HERE"
  }' | jq
```

**Expected Response:**
```json
{
  "success": true,
  "job_id": "uuid-here",
  "analysis": {
    "job_title": "Software Engineer",
    "company": "Tech Corp",
    "location": "San Francisco, CA",
    "ats_system_detected": "greenhouse",
    "keywords": {
      "all": ["Python", "AWS", "Docker", "..."],
      "required": ["Python", "AWS"],
      "preferred": ["Docker"]
    },
    "requirements": {
      "required": ["5+ years Python experience"],
      "preferred": ["AWS certification"]
    },
    "scraped": true
  }
}
```

### With fallback description (if URL fails):

```bash
curl -X POST http://localhost:8000/jobs/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "job_url": "https://example.com/job/123",
    "job_description": "We are hiring a Senior Developer with 5+ years Python experience...",
    "company_name": "Tech Corp",
    "user_id": "YOUR_USER_ID_HERE"
  }' | jq
```

---

## 2. Test Manual Job Creation

### Create job without AI analysis:

```bash
curl -X POST http://localhost:8000/jobs/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Backend Developer",
    "company": "Acme Corp",
    "location": "Remote",
    "description": "We are looking for an experienced backend developer...",
    "url": "https://acme.com/careers/123",
    "keywords": ["Python", "FastAPI", "PostgreSQL", "AWS"],
    "requirements": ["5+ years Python", "FastAPI experience", "AWS knowledge"],
    "ats_system": "greenhouse",
    "user_id": "YOUR_USER_ID_HERE"
  }' | jq
```

**Expected Response:**
```json
{
  "success": true,
  "job_id": "uuid-here",
  "job": {
    "id": "uuid",
    "job_title": "Senior Backend Developer",
    "company_name": "Acme Corp",
    "extracted_keywords": ["Python", "FastAPI", "PostgreSQL", "AWS"],
    ...
  }
}
```

---

## 3. Test Generic Resume Generation

### First, ensure you have confirmed knowledge entities:

```bash
# Check if user has confirmed entities
curl "http://localhost:8000/knowledge/pending?user_id=YOUR_USER_ID_HERE" | jq

# Confirm some entities if needed
curl -X POST http://localhost:8000/knowledge/confirm \
  -H "Content-Type: application/json" \
  -d '{
    "entity_id": "ENTITY_ID_HERE",
    "user_id": "YOUR_USER_ID_HERE"
  }' | jq
```

### Generate resume with freeform prompt:

```bash
curl -X POST http://localhost:8000/resumes/generate-generic \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "applying for concession stand role",
    "user_id": "YOUR_USER_ID_HERE"
  }' | jq
```

**Expected Response:**
```json
{
  "success": true,
  "resume_id": "uuid-here",
  "resume": {
    "contact_info": {...},
    "summary": "...",
    "experience": [...],
    "skills": {...},
    "education": [...],
    "certifications": [...]
  },
  "html": "<!DOCTYPE html>...",
  "entities_used": 12,
  "prompt": "applying for concession stand role"
}
```

### Try different prompts:

```bash
# Management emphasis
curl -X POST http://localhost:8000/resumes/generate-generic \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "emphasizing management and leadership skills",
    "user_id": "YOUR_USER_ID_HERE"
  }' | jq

# Technical role
curl -X POST http://localhost:8000/resumes/generate-generic \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "software engineering internship",
    "user_id": "YOUR_USER_ID_HERE"
  }' | jq
```

---

## 4. View Generated Resumes

```bash
# List all resumes
curl "http://localhost:8000/resumes/list?user_id=YOUR_USER_ID_HERE" | jq

# Get specific resume
curl "http://localhost:8000/resumes/RESUME_ID_HERE?user_id=YOUR_USER_ID_HERE" | jq

# Export as HTML
curl "http://localhost:8000/resumes/RESUME_ID_HERE/export/html?user_id=YOUR_USER_ID_HERE" | jq
```

---

## 5. Test Error Handling

### No confirmed entities:

```bash
curl -X POST http://localhost:8000/resumes/generate-generic \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "test prompt",
    "user_id": "NEW_USER_WITH_NO_DATA"
  }' | jq
```

**Expected:** HTTP 400 with error message about missing entities

### Invalid job URL:

```bash
curl -X POST http://localhost:8000/jobs/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "job_url": "https://this-will-404.com/job/nonexistent",
    "job_description": "This is the fallback description",
    "user_id": "YOUR_USER_ID_HERE"
  }' | jq
```

**Expected:** Should fall back to analyzing the provided description

---

## 6. Integration Test: Complete Workflow

```bash
# Step 1: Upload and parse a resume (existing endpoint)
curl -X POST http://localhost:8000/upload \
  -F "file=@path/to/resume.pdf" \
  -F "user_id=YOUR_USER_ID_HERE"

# Step 2: Confirm extracted knowledge entities
curl "http://localhost:8000/knowledge/pending?user_id=YOUR_USER_ID_HERE" | jq
# (Confirm entities one by one)

# Step 3: Analyze a job posting
curl -X POST http://localhost:8000/jobs/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "job_url": "https://example.com/job/123",
    "user_id": "YOUR_USER_ID_HERE"
  }' | jq

# Step 4: Generate tailored resume (existing endpoint)
curl -X POST http://localhost:8000/resumes/generate \
  -H "Content-Type: application/json" \
  -d '{
    "job_posting_id": "JOB_ID_FROM_STEP_3",
    "user_id": "YOUR_USER_ID_HERE"
  }' | jq

# Step 5: Generate generic resume
curl -X POST http://localhost:8000/resumes/generate-generic \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "marketing coordinator position",
    "user_id": "YOUR_USER_ID_HERE"
  }' | jq
```

---

## 7. Check Server Logs

While testing, watch the server logs for debug output:

```bash
# You should see:
# - "Fetching URL: ..."
# - "Successfully fetched URL (status: 200)"
# - "Extracted X characters of text from HTML"
# - "Extracted company name: ..."
# - "Selected X relevant entities"
# - "Generated resume [uuid]"
```

---

## 8. Test with Real Job Sites

### Greenhouse:

```bash
curl -X POST http://localhost:8000/jobs/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "job_url": "https://boards.greenhouse.io/company/jobs/123456",
    "user_id": "YOUR_USER_ID_HERE"
  }' | jq
```

### Lever:

```bash
curl -X POST http://localhost:8000/jobs/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "job_url": "https://jobs.lever.co/company/job-id",
    "user_id": "YOUR_USER_ID_HERE"
  }' | jq
```

### Workday:

```bash
curl -X POST http://localhost:8000/jobs/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "job_url": "https://company.wd1.myworkdayjobs.com/en-US/careers/job/job-title_JR12345",
    "user_id": "YOUR_USER_ID_HERE"
  }' | jq
```

---

## 9. Python Integration Test

Create `test_backend.py`:

```python
import asyncio
import httpx

BASE_URL = "http://localhost:8000"
USER_ID = "your-test-user-id"

async def test_job_scraping():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/jobs/analyze",
            json={
                "job_url": "https://example.com/job/123",
                "job_description": "Fallback description",
                "user_id": USER_ID
            }
        )
        print("Job Analysis:", response.json())

async def test_resume_generation():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/resumes/generate-generic",
            json={
                "prompt": "software engineering role",
                "user_id": USER_ID
            }
        )
        print("Resume Generation:", response.json())

if __name__ == "__main__":
    asyncio.run(test_job_scraping())
    asyncio.run(test_resume_generation())
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'requests'"
```bash
pip install requests beautifulsoup4
```

### "ANTHROPIC_API_KEY not found"
```bash
# Add to .env file:
ANTHROPIC_API_KEY=your-key-here
```

### "No confirmed entities found"
- Upload a resume first
- Use conversation interface to extract facts
- Confirm entities via /knowledge/confirm endpoint

### Scraping returns empty text
- Check if site requires JavaScript (needs Selenium)
- Check if site blocks automated requests (Cloudflare)
- Use fallback by providing job_description in request

---

## Quick Reference

### New Endpoints:
1. **POST /jobs/analyze** (enhanced) - Scrape and analyze job
2. **POST /jobs/create** - Create job manually
3. **POST /resumes/generate-generic** - Generate from prompt

### Key Parameters:
- `user_id` - Required for all endpoints
- `job_url` - Optional, enables scraping
- `job_description` - Fallback if scraping fails
- `prompt` - Freeform text for generic resumes

### Response Codes:
- 200 - Success
- 400 - Bad request (missing entities, invalid input)
- 404 - Resource not found
- 500 - Server error (check logs)
