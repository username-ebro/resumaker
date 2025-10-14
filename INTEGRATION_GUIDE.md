# ML/AI Services Integration Guide

**Quick reference for integrating the new intelligent services into resumaker**

---

## Services Available

| Service | File | Purpose | Key Method |
|---------|------|---------|------------|
| Company Research | `company_research_service.py` | Gather company info for tailoring | `research_company()` |
| ATS Detection | `ats_detection_service.py` | Identify ATS systems | `detect_ats()` |
| Job Matcher (Enhanced) | `job_matcher.py` | Extract/categorize keywords | `extract_keywords_with_ai()` |
| Resume Generator (Generic) | `resume_generator.py` | Smart fact selection | `select_relevant_facts()` |

---

## Quick Integration Examples

### 1. Add ATS Detection to Job Analysis

**Backend Router:** `/backend/app/routers/jobs.py`

```python
from app.services.ats_detection_service import ats_detection_service

@router.post("/jobs/analyze")
async def analyze_job_posting(job_data: dict):
    """Analyze a job posting with ATS detection"""

    # Detect ATS system
    ats_result = ats_detection_service.detect_ats(
        job_url=job_data.get("job_url"),
        html_content=job_data.get("html_content")
    )

    # Store result
    job_posting = {
        "user_id": job_data["user_id"],
        "job_url": job_data["job_url"],
        "ats_system": ats_result["ats_system"],
        "ats_recommendations": ats_result["recommendations"],
        "optimal_format": ats_result["optimal_format"]
    }

    # Save to database
    result = supabase.table("job_postings").insert(job_posting).execute()

    return {
        "job_id": result.data[0]["id"],
        "ats_detected": ats_result
    }
```

**Frontend Component:** `components/ATSRecommendations.tsx`

```tsx
export function ATSRecommendations({ jobId }: { jobId: string }) {
  const [atsData, setAtsData] = useState(null);

  useEffect(() => {
    fetch(`/api/jobs/${jobId}/ats`)
      .then(res => res.json())
      .then(data => setAtsData(data));
  }, [jobId]);

  if (!atsData) return <div>Analyzing ATS system...</div>;

  return (
    <div className="ats-recommendations">
      <h3>Detected: {atsData.system_name}</h3>
      <p>Optimal Format: <strong>{atsData.optimal_format}</strong></p>
      <p>Parsing Quality: {atsData.parsing_quality}</p>

      <h4>Recommendations:</h4>
      <ul>
        {atsData.recommendations.map((rec, i) => (
          <li key={i}>{rec}</li>
        ))}
      </ul>
    </div>
  );
}
```

---

### 2. Add Company Research to Job Page

**Backend Router:** `/backend/app/routers/company.py` (NEW FILE)

```python
from fastapi import APIRouter
from app.services.company_research_service import company_research_service

router = APIRouter(prefix="/api/company", tags=["company"])

@router.get("/{company_name}")
async def get_company_info(company_name: str):
    """Research a company"""
    result = await company_research_service.research_company(company_name)

    if result["research_success"]:
        suggestions = company_research_service.get_tailoring_suggestions(result)
        return {
            "company": result,
            "tailoring_suggestions": suggestions
        }
    else:
        return {"error": result["error"]}
```

**Frontend Component:** `components/CompanyInsights.tsx`

```tsx
export function CompanyInsights({ companyName }: { companyName: string }) {
  const [company, setCompany] = useState(null);

  useEffect(() => {
    fetch(`/api/company/${encodeURIComponent(companyName)}`)
      .then(res => res.json())
      .then(data => setCompany(data));
  }, [companyName]);

  if (!company) return <div>Researching company...</div>;

  return (
    <div className="company-insights">
      <h3>{company.company.company_name}</h3>

      {company.company.about && (
        <p className="about">{company.company.about}</p>
      )}

      {company.company.values.length > 0 && (
        <div>
          <h4>Core Values</h4>
          <div className="values">
            {company.company.values.map(value => (
              <span key={value} className="badge">{value}</span>
            ))}
          </div>
        </div>
      )}

      <h4>Tailoring Tips</h4>
      <ul>
        {company.tailoring_suggestions.map((tip, i) => (
          <li key={i}>{tip}</li>
        ))}
      </ul>
    </div>
  );
}
```

---

### 3. Add Generic Resume Mode

**Backend Router:** `/backend/app/routers/resumes.py`

```python
from app.services.resume_generator import ResumeGenerator

resume_generator = ResumeGenerator()

@router.post("/resumes/generate")
async def generate_resume(request: dict):
    """Generate resume in job-targeted or generic mode"""

    user_id = request["user_id"]

    # Check which mode to use
    if request.get("job_id"):
        # Job-targeted mode (existing)
        job = supabase.table("job_postings").select("*").eq("id", request["job_id"]).single().execute()
        resume = await resume_generator.generate_resume(
            user_id=user_id,
            job_description=job.data["job_description"]
        )
    elif request.get("user_prompt"):
        # Generic mode (NEW)
        resume = await resume_generator.generate_resume(
            user_id=user_id,
            user_prompt=request["user_prompt"]
        )
    else:
        # General mode (no targeting)
        resume = await resume_generator.generate_resume(user_id=user_id)

    return resume
```

**Frontend Component:** `components/ResumePromptModal.tsx`

```tsx
export function ResumePromptModal({ onGenerate }: { onGenerate: (prompt: string) => void }) {
  const [prompt, setPrompt] = useState("");

  const examples = [
    "applying for concession stand position",
    "software engineering internship",
    "marketing coordinator role at startup",
    "retail sales associate"
  ];

  return (
    <div className="modal">
      <h2>What are you applying for?</h2>
      <p>Describe the role in your own words:</p>

      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="e.g., applying for concession stand"
        className="prompt-input"
      />

      <div className="examples">
        <p>Examples:</p>
        {examples.map(ex => (
          <button
            key={ex}
            onClick={() => setPrompt(ex)}
            className="example-btn"
          >
            {ex}
          </button>
        ))}
      </div>

      <button
        onClick={() => onGenerate(prompt)}
        disabled={!prompt}
        className="generate-btn"
      >
        Generate Resume
      </button>
    </div>
  );
}
```

---

### 4. Enhanced Job Matching Dashboard

**Backend Router:** `/backend/app/routers/jobs.py`

```python
from app.services.job_matcher import JobMatcher

job_matcher = JobMatcher()

@router.post("/jobs/{job_id}/analyze-keywords")
async def analyze_job_keywords(job_id: str):
    """Get enhanced keyword analysis"""

    # Fetch job
    job = supabase.table("job_postings").select("*").eq("id", job_id).single().execute()

    # Enhanced keyword extraction
    keywords = await job_matcher.extract_keywords_with_ai(job.data["job_description"])

    # Requirement categorization
    requirements = await job_matcher.categorize_requirements(job.data["job_description"])

    return {
        "keywords": keywords,
        "requirements": requirements
    }
```

**Frontend Component:** `components/JobAnalysisDashboard.tsx`

```tsx
export function JobAnalysisDashboard({ jobId }: { jobId: string }) {
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    fetch(`/api/jobs/${jobId}/analyze-keywords`, { method: 'POST' })
      .then(res => res.json())
      .then(data => setAnalysis(data));
  }, [jobId]);

  if (!analysis) return <div>Analyzing job...</div>;

  return (
    <div className="job-analysis">
      <section>
        <h3>Keywords by Priority</h3>

        <div className="keyword-group critical">
          <h4>🔴 Critical (Must-Have)</h4>
          {analysis.keywords.critical.map(kw => (
            <span key={kw} className="keyword">{kw}</span>
          ))}
        </div>

        <div className="keyword-group important">
          <h4>🟡 Important</h4>
          {analysis.keywords.important.map(kw => (
            <span key={kw} className="keyword">{kw}</span>
          ))}
        </div>

        <div className="keyword-group nice">
          <h4>🟢 Nice-to-Have</h4>
          {analysis.keywords.nice_to_have.map(kw => (
            <span key={kw} className="keyword">{kw}</span>
          ))}
        </div>
      </section>

      <section>
        <h3>Requirements Breakdown</h3>

        <div className="requirements">
          <h4>Must Have</h4>
          <ul>
            <li>Experience: {analysis.requirements.must_have.experience_years} years</li>
            <li>Education: {analysis.requirements.must_have.education}</li>
            <li>Skills: {analysis.requirements.must_have.skills.join(', ')}</li>
          </ul>

          {analysis.requirements.deal_breakers.length > 0 && (
            <>
              <h4>⚠️ Deal Breakers</h4>
              <ul>
                {analysis.requirements.deal_breakers.map((db, i) => (
                  <li key={i}>{db}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      </section>
    </div>
  );
}
```

---

## Database Migrations Needed

### 1. Add ATS columns to job_postings table

```sql
ALTER TABLE job_postings
ADD COLUMN ats_system TEXT,
ADD COLUMN ats_confidence DECIMAL(3,2),
ADD COLUMN ats_recommendations JSONB,
ADD COLUMN optimal_resume_format TEXT;
```

### 2. Create company_research table

```sql
CREATE TABLE company_research (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  company_name TEXT NOT NULL,
  website TEXT,
  linkedin TEXT,
  about TEXT,
  values JSONB,
  culture_keywords JSONB,
  industry TEXT,
  company_size TEXT,
  locations JSONB,
  researched_at TIMESTAMP DEFAULT NOW(),
  cached_until TIMESTAMP
);

CREATE INDEX idx_company_name ON company_research(company_name);
```

### 3. Add resume generation metadata

```sql
ALTER TABLE generated_resumes
ADD COLUMN generation_mode TEXT,  -- 'job_targeted', 'generic', 'general'
ADD COLUMN user_prompt TEXT,
ADD COLUMN facts_used INTEGER,
ADD COLUMN keywords_targeted JSONB;
```

---

## Environment Variables Required

All services use the existing `ANTHROPIC_API_KEY`:

```bash
# .env file
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```

No additional API keys needed for basic functionality.

For future enhancements:
```bash
# Optional for Phase 2
GOOGLE_SEARCH_API_KEY=xxxxx
GOOGLE_SEARCH_ENGINE_ID=xxxxx
GLASSDOOR_API_KEY=xxxxx
LINKEDIN_API_KEY=xxxxx
```

---

## Testing Checklist

### Before Deployment

- [ ] Test imports: `python3 backend/test_imports.py`
- [ ] Verify ANTHROPIC_API_KEY is set
- [ ] Test company research with real company name
- [ ] Test ATS detection with known job URLs
- [ ] Test generic resume with diverse user background
- [ ] Check error handling (invalid inputs, API failures)

### After Deployment

- [ ] Monitor API token usage
- [ ] Track response times
- [ ] Collect user feedback on relevance
- [ ] A/B test resume success rates

---

## Common Integration Patterns

### Pattern 1: Cache AI Results
```python
# Check cache first
cached = supabase.table("company_research").select("*").eq("company_name", name).execute()

if cached.data and cached.data[0]["cached_until"] > datetime.now():
    return cached.data[0]
else:
    # Fresh research
    result = await company_research_service.research_company(name)
    # Store in cache
    supabase.table("company_research").upsert(result).execute()
    return result
```

### Pattern 2: Progressive Enhancement
```python
# Start with basic data
response = {"job_title": job.title, "company": job.company}

# Add AI enhancements if available
try:
    response["ats_info"] = ats_detection_service.detect_ats(job.url)
    response["company_info"] = await company_research_service.research_company(job.company)
except Exception as e:
    # Log error but return basic response
    print(f"AI enhancement failed: {e}")

return response
```

### Pattern 3: Background Jobs
```python
# Trigger AI analysis in background
@router.post("/jobs/create")
async def create_job(job_data: dict):
    # Store job immediately
    job = supabase.table("job_postings").insert(job_data).execute()

    # Queue AI analysis
    background_tasks.add_task(analyze_job_in_background, job.data[0]["id"])

    return {"job_id": job.data[0]["id"], "status": "analyzing"}

async def analyze_job_in_background(job_id: str):
    # Run all AI services
    # Update job record when complete
    pass
```

---

## Performance Tips

1. **Batch API Calls**: If analyzing multiple jobs, batch them
2. **Cache Aggressively**: Company research rarely changes
3. **Lazy Load**: Only run AI services when user views details
4. **Rate Limiting**: Add rate limits to prevent API abuse
5. **Fallbacks**: Always have non-AI fallback behavior

---

## Support & Troubleshooting

### Service Not Working?

1. Check API key: `echo $ANTHROPIC_API_KEY`
2. Test imports: `python3 backend/test_imports.py`
3. Check error logs for API rate limits
4. Verify input data format

### Common Errors

**Error:** `ModuleNotFoundError: No module named 'anthropic'`
- **Fix:** `pip install anthropic`

**Error:** `API key not found`
- **Fix:** Add `ANTHROPIC_API_KEY` to `.env` file

**Error:** `JSON decode error`
- **Fix:** Check prompt is returning valid JSON, add retry logic

---

## Next Steps

1. **Week 1:** Integrate ATS detection into job analysis page
2. **Week 2:** Add company research to job detail pages
3. **Week 3:** Implement generic resume mode
4. **Week 4:** Add enhanced keyword analysis dashboard

For questions, refer to `/backend/ML_AI_PROGRESS.md` for detailed documentation.
