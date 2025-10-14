# 🚀 Autonomous Build Plan - Resume Generation Complete

## Objective
Complete the resume generation system with:
1. Enhanced job analysis (web search, company research, ATS detection)
2. Two-step job creation flow
3. Generic resume generation (no job required)
4. Full integration and testing

## Timeline: 4-6 hours

---

## Agent Assignments

### 1. **Backend/API Specialist**
**Focus:** Jobs router enhancements + new endpoints

**Tasks:**
- Enhance `/jobs/analyze` endpoint:
  - Add web fetching (requests + BeautifulSoup)
  - Extract company name from job description
  - Return structured job data
- Create `/jobs/create` endpoint (save confirmed job to database)
- Create `/resumes/generate-generic` endpoint (no job targeting)
- Add utility functions:
  - `fetch_url_content(url)` - Get page HTML
  - `extract_company_from_text(text, job_title)` - Find company name
  - `extract_location(text)` - Find location
  - `extract_requirements(text)` - Parse bullet points
  - `extract_keywords(text)` - Get important terms

**Deliverables:**
- `backend/app/routers/jobs.py` (enhanced)
- `backend/app/services/web_scraper_service.py` (new)
- `backend/app/services/company_research_service.py` (new)

---

### 2. **ML/AI Specialist**
**Focus:** Company research + ATS detection + keyword extraction

**Tasks:**
- Build `CompanyResearchService`:
  - Google search integration for company website
  - LinkedIn profile search (use Google search "site:linkedin.com/company")
  - Extract core values from company website
  - Extract "About Us" section
- Build `ATSDetectionService`:
  - Detect ATS from URL patterns (Workday, Greenhouse, Lever, etc.)
  - Detect ATS from page HTML (look for signatures)
  - Return ATS system name + optimization tips
- Enhance `JobMatcherService`:
  - Better keyword extraction using Claude
  - Requirement parsing (MUST HAVE vs NICE TO HAVE)
  - Skill matching against user's knowledge base
- Build prompt for generic resume generation:
  - Takes user's freeform request
  - Selects relevant facts from knowledge base
  - Generates resume

**Deliverables:**
- `backend/app/services/company_research_service.py`
- `backend/app/services/ats_detection_service.py`
- Enhanced `backend/app/services/job_matcher.py`
- Generic resume prompt in `backend/app/services/resume_generator.py`

---

### 3. **Database Specialist**
**Focus:** Schema validation + jobs table enhancements

**Tasks:**
- Review `jobs` table schema - ensure it can store:
  - Company info (name, website, LinkedIn, values, about)
  - ATS system name
  - Parsed requirements array
  - Parsed keywords array
  - Location
- Create migration if needed
- Add indexes for performance:
  - `user_id, created_at` (list user's jobs)
  - `company` (search by company)
  - `ats_system` (analytics)
- Ensure foreign keys work properly
- Test job creation flow end-to-end

**Deliverables:**
- `backend/migrations/003_jobs_enhancements.sql` (if needed)
- Database validation report

---

### 4. **Frontend/UX Specialist**
**Focus:** Generic resume UI + polish

**Tasks:**
- Add "Generic Resume" option to dashboard:
  - New tab or toggle on Generate Resume page
  - Text/voice input: "Tell me what kind of role..."
  - Examples/placeholder text
  - "Generate Resume" button
- Polish JobConfirmation component:
  - Make sure all fields display properly
  - Test edit functionality
  - Add loading states
- Add error handling throughout resume generation flow
- Test full user journey:
  1. Build knowledge base via conversation
  2. Confirm facts
  3. Generate job-specific resume (two-step)
  4. Generate generic resume
- Create onboarding tooltips/hints if time permits

**Deliverables:**
- Enhanced `frontend/app/dashboard/page.tsx`
- New `frontend/components/GenericResumeGenerator.tsx`
- Polish on `frontend/components/JobConfirmation.tsx`

---

### 5. **Integration/Testing Lead**
**Focus:** End-to-end testing + coordination

**Tasks:**
- Monitor all agents' progress
- Test each component as it's completed:
  - Web scraping (test on 5 real job URLs)
  - Company research (test on 5 companies)
  - ATS detection (test on all major ATS systems)
  - Job creation (test full flow)
  - Generic resume (test 3 different prompts)
- Create integration tests:
  - Full job-specific resume flow
  - Full generic resume flow
  - Error handling (bad URLs, missing data, etc.)
- Create demo script for user
- Document any issues/blockers
- Coordinate between agents if dependencies arise

**Deliverables:**
- `test_resume_generation_full.py` (comprehensive test)
- `TESTING_REPORT.md` (what works, what doesn't)
- `USER_DEMO_SCRIPT.md` (step-by-step guide)

---

## Dependencies & Order

**Phase 1 (Parallel):**
- Backend Specialist: Web scraping utilities
- ML/AI Specialist: Company research + ATS detection
- Database Specialist: Schema review + migration
- Frontend Specialist: Generic resume UI

**Phase 2 (Parallel - depends on Phase 1):**
- Backend Specialist: Enhanced `/jobs/analyze` endpoint (needs web scraping)
- ML/AI Specialist: Generic resume prompt (needs knowledge base queries)
- Frontend Specialist: Polish + error handling

**Phase 3 (Parallel - depends on Phase 2):**
- Backend Specialist: `/jobs/create` + `/resumes/generate-generic` endpoints
- Integration Lead: Full testing

**Phase 4 (Sequential):**
- Integration Lead: Demo prep + documentation

---

## Success Criteria

✅ User can enter job URL → System fetches, parses, researches company, detects ATS
✅ User reviews job details in confirmation screen → Can edit anything
✅ User confirms → Job saved to database
✅ System generates targeted resume for that job
✅ User can generate generic resume with freeform prompt (no job required)
✅ All tests pass
✅ Demo-ready with documentation

---

## Risks & Mitigations

**Risk 1:** Web scraping blocked by some sites
- **Mitigation:** Add User-Agent headers, retry logic, fallback to manual entry

**Risk 2:** Company research returns no data
- **Mitigation:** Graceful degradation - show what we found, allow manual entry

**Risk 3:** ATS detection unreliable
- **Mitigation:** Show confidence level, allow user to override

**Risk 4:** Generic resume quality poor
- **Mitigation:** Provide examples in prompt, let user preview before finalizing

---

## Agent Coordination

**Communication:**
- Each agent will create a `AGENT_NAME_PROGRESS.md` file with updates
- Integration Lead checks every 30 minutes
- Agents can read each other's progress files

**Handoffs:**
- Backend → ML/AI: Web scraping utilities done
- ML/AI → Backend: Company research service done
- Database → Backend: Schema ready for job creation
- Backend → Frontend: API endpoints ready
- All → Integration: Components ready for testing

---

## Post-Build Tasks

After all agents complete:
1. Integration Lead runs full test suite
2. Create video demo/walkthrough
3. Document any known issues
4. Create backlog for future enhancements:
   - LinkedIn API integration (paid)
   - More ATS systems
   - Cover letter generation
   - Email outreach templates
