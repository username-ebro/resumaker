# Resumaker - User Demo Script
**Test Guide for End Users**
**Created:** October 8, 2025
**Version:** 1.0

---

## Prerequisites

### System Requirements
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection
- Backend running on http://localhost:8000
- Frontend running on http://localhost:3001

### Starting the Application

**Terminal 1: Backend**
```bash
cd backend
source ../venv/bin/activate
export DYLD_LIBRARY_PATH=/opt/homebrew/lib  # macOS only
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2: Frontend**
```bash
cd frontend
npm run dev
```

**Verify Services:**
- Backend: http://localhost:8000/health (should show `{"status":"healthy"}`)
- Frontend: http://localhost:3001 (should load homepage)

---

## Demo Flow 1: Job-Specific Resume (Recommended)

### Step 1: Sign Up / Login
1. Navigate to http://localhost:3001/auth/signup
2. Fill in:
   - **Email:** demo@example.com
   - **Password:** DemoPass123!
   - **Full Name:** Demo User
3. Click "Sign Up"
4. **Expected:** Redirected to dashboard

**Screenshot Checkpoint:** Dashboard with 3 tabs (Conversation, Upload, Import)

---

### Step 2: Build Knowledge Base

You have 3 options to populate your knowledge base. Choose one:

#### **Option A: Voice Conversation (Recommended for Demo)**

1. Click **"Conversation"** tab
2. Click the **microphone button** (voice mode)
3. Click **"Start Recording"** and speak naturally:

**Sample Script:**
```
"Hi, I'm a senior software engineer with 5 years of experience.
I worked at TechCorp from 2020 to 2023 building scalable APIs in Python and FastAPI.
I reduced API latency by 60% and led a team of 5 engineers.
I'm proficient in Python, AWS, Docker, PostgreSQL, and React.
I have a Computer Science degree from MIT with a 3.8 GPA."
```

4. Click **"Stop Recording"**
5. **Expected:** Audio transcribes → AI responds with follow-up question
6. Continue for 2-3 exchanges

**Troubleshooting:**
- **Microphone permission denied:** Check browser settings → allow microphone access
- **Transcription fails:** Check backend logs for Gemini API errors
- **No response:** Verify ANTHROPIC_API_KEY is set

#### **Option B: Upload Resume**

1. Click **"Upload"** tab
2. Choose a file:
   - **PDF:** Most common, best tested
   - **DOCX:** Word format, well supported
   - **TXT:** Plain text, fastest processing
   - **DOC:** Legacy Word (requires antiword)
   - **JPG/PNG:** Image with text (uses OCR)
3. Click **"Upload & Extract"**
4. **Expected:** Processing spinner → Success message with extracted data

**Sample Test Files:**
- Use an existing resume
- Or create a simple `.txt` file with your experience

#### **Option C: Import Conversation**

1. Click **"Import"** tab
2. Paste a ChatGPT/Claude conversation about your experience
3. Select source: **ChatGPT** or **Claude**
4. Click **"Parse & Import"**
5. **Expected:** AI extracts structured data from conversation

**Sample Import Text:**
```
User: Tell me about your work experience
Assistant: I worked as a senior software engineer at TechCorp...
[paste 5-10 lines of conversation]
```

---

### Step 3: Generate Job-Specific Resume

1. Find a real job posting online (or use sample below)
2. Copy the **full job description**
3. In Resumaker, click **"✨ Generate Resume"**
4. **Paste job posting** in text area

**Sample Job Posting:**
```
Senior Software Engineer - Backend

We're seeking an experienced backend engineer to join our team.

Requirements:
- 5+ years Python experience
- FastAPI or Django framework
- PostgreSQL database design
- AWS cloud infrastructure (EC2, S3, Lambda)
- Docker and Kubernetes
- CI/CD pipelines (GitHub Actions, GitLab CI)
- REST API design

Preferred:
- GraphQL experience
- Redis caching
- Microservices architecture
- Team leadership experience

About Us:
We're a fast-growing startup building the next generation of...
```

5. Click **"Analyze Job"**
6. **Expected:**
   - Processing 5-10 seconds
   - Shows extracted keywords (15-25)
   - Shows ATS system detected (if applicable)
   - Shows job title, company, location

**Screenshot Checkpoint:** Job analysis results

7. Click **"Generate Resume"** (or it may auto-generate)
8. **Expected:**
   - Processing 30-60 seconds (multi-step AI)
   - Tailored resume appears
   - Truth check flags shown (if any)

**What to Look For:**
- ✅ Resume includes keywords from job description
- ✅ Bullet points match job requirements
- ✅ ATS optimization applied
- ✅ Professional formatting
- ⚠️ Truth check warnings (yellow flags)
- ❌ Truth check errors (red flags)

---

### Step 4: Review Truth Check Flags

1. Look at the **flags section** (if present)
2. Each flag shows:
   - **Severity:** Low (green), Medium (yellow), High (red)
   - **Issue:** What claim couldn't be verified
   - **Suggestion:** How to fix it

**Common Flags:**
- "Led team of 5 engineers" → Verify team size claim
- "Reduced latency by 60%" → Verify quantified metric
- "Expert in XYZ" → Verify skill level claim

3. Click **"Resolve"** on each flag to mark as reviewed
4. Edit resume if needed (manual editing not yet implemented)

---

### Step 5: Download Resume

1. Choose export format:
   - **PDF:** Best for applications (ATS-safe)
   - **DOCX:** Editable in Microsoft Word
   - **HTML:** For web/email

2. Click download button
3. **Expected:** File downloads with name `YourName_Resume.pdf`

**Verify Download:**
- Open file in appropriate program
- Check formatting is clean
- No broken layouts or weird spacing
- ATS-friendly (no images, tables, or complex formatting)

---

## Demo Flow 2: Generic Resume (No Job Posting)

### Quick Path
1. Complete **Step 1** (Sign Up) and **Step 2** (Knowledge Base) from Flow 1
2. Click **"✨ Generate Resume"**
3. Instead of job posting, enter a **prompt**:

**Sample Prompts:**
```
"Create a professional resume highlighting my technical skills"
"Generate a resume focused on leadership and team management"
"Build a resume emphasizing problem-solving achievements"
```

4. Click **"Generate"**
5. **Expected:** Generic resume based on all knowledge base entries

**Use Case:** Creating a master resume or general-purpose resume

---

## Demo Flow 3: Multiple Resumes for Different Jobs

### Scenario
Test creating 2-3 resumes for different types of jobs.

1. Complete knowledge base (once)
2. Generate resume for **Backend Job** → Download as `Resume_Backend.pdf`
3. Generate resume for **Data Science Job** → Download as `Resume_DataScience.pdf`
4. Generate resume for **Leadership Role** → Download as `Resume_Leadership.pdf`

**What to Compare:**
- Keywords differ based on job
- Bullet points emphasize different skills
- Professional summary changes tone
- All resumes use same truthful knowledge base

**Expected Insight:** Same experience, different angles = tailored resumes

---

## Common Issues & Troubleshooting

### Issue: "Cannot connect to backend"
**Symptoms:** Frontend loads but no data, API errors in console
**Fix:**
```bash
# Check backend is running
curl http://localhost:8000/health

# If not running, restart:
cd backend && source ../venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Issue: "Voice transcription fails"
**Symptoms:** Recording works but no transcript appears
**Possible Causes:**
1. Missing Gemini API key
2. Wrong Gemini model name
3. Audio format issue

**Fix:**
```bash
# Check backend logs
tail -f /tmp/resumaker_backend.log

# Verify environment variables
echo $GEMINI_API_KEY
echo $ANTHROPIC_API_KEY

# Look for errors like:
# - "ModuleNotFoundError: No module named 'bs4'" → pip install beautifulsoup4
# - "404 model not found" → Check model name in transcription_service.py
```

### Issue: "Resume generation crashes"
**Symptoms:** Job analysis works, but resume generation fails
**Possible Causes:**
1. No knowledge base entries
2. Database schema issue
3. API quota exceeded

**Fix:**
1. Verify knowledge base has entries (Conversation/Upload/Import)
2. Check backend logs for specific error:
```bash
tail -20 /tmp/resumaker_backend.log
```

### Issue: "Database column not found"
**Symptoms:** Backend logs show `PGRST204: Column not found`
**Current Known Issues:**
- `auto_flagged` column missing in `truth_check_flags` table

**Fix:** Run database migration (see PROJECT_STATUS.md)

### Issue: "Upload fails"
**Symptoms:** File upload returns error
**Possible Causes:**
1. File too large (>10MB)
2. Unsupported format
3. OCR service failure

**Supported Formats:**
- PDF (best)
- DOCX (Word 2007+)
- TXT (plain text)
- DOC (legacy Word, requires antiword)
- JPG/PNG (OCR)

**Fix:** Try converting to PDF or TXT first

---

## Performance Expectations

### Normal Processing Times
- **Job Analysis:** 5-10 seconds
- **Resume Generation:** 30-60 seconds
- **File Upload (PDF):** 10-15 seconds
- **Voice Transcription:** 3-5 seconds per recording
- **Export (PDF/DOCX):** <1 second

### When to Worry
- Job analysis > 30 seconds → API issue
- Resume generation > 2 minutes → Check logs
- Voice transcription > 15 seconds → Audio conversion issue

---

## Success Criteria Checklist

Use this checklist to verify the demo is working:

### Core Functionality
- [ ] User can sign up and log in
- [ ] Voice recording captures and transcribes audio
- [ ] File upload extracts resume content
- [ ] Conversation import parses text
- [ ] Job analysis extracts 15-25 keywords
- [ ] ATS system detected (for known systems)
- [ ] Resume generation completes successfully
- [ ] Resume includes job-specific keywords
- [ ] Truth checking identifies unverified claims
- [ ] PDF export downloads successfully
- [ ] DOCX export downloads successfully

### Quality Checks
- [ ] Resume is professionally formatted
- [ ] Bullet points are action-oriented (Action + Result + Metric)
- [ ] Keywords naturally integrated (not stuffed)
- [ ] No spelling or grammar errors
- [ ] Contact information formatted correctly
- [ ] Dates are consistent and logical
- [ ] ATS-friendly (no tables, images, complex layouts)

### User Experience
- [ ] UI is responsive and loads quickly
- [ ] Loading indicators show during processing
- [ ] Error messages are clear and helpful
- [ ] Navigation is intuitive
- [ ] Design is clean and professional
- [ ] Mobile-friendly (bonus if tested)

---

## Demo Tips

### For Live Presentations
1. **Pre-populate knowledge base** before demo to save time
2. **Use sample job posting** that matches your test data
3. **Have backup PDFs** in case live generation fails
4. **Keep backend logs open** to show processing in real-time
5. **Prepare 2-3 job types** to show versatility

### For Video Demos
1. **Screen record in 1080p or higher**
2. **Show before/after** (generic resume vs tailored)
3. **Highlight key features**:
   - Voice input (cool factor)
   - Keyword extraction (AI intelligence)
   - Truth checking (integrity)
   - Multi-format export (convenience)

### For User Testing
1. **Give minimal instructions** - see if they can figure it out
2. **Watch where they click** - identify UX issues
3. **Ask them to "think aloud"** - understand their mental model
4. **Note pain points** - where do they get stuck?
5. **Collect feedback** - what would make it better?

---

## Expected Outcomes

### What Should Work
✅ Full end-to-end resume generation
✅ Voice transcription and conversation
✅ File upload (5 formats)
✅ Job analysis and keyword extraction
✅ ATS detection for major systems
✅ Truth checking with severity levels
✅ PDF and DOCX export
✅ Multiple resume versions per user

### Known Limitations
⚠️ Direct web scraping not exposed (integrated into /jobs/analyze)
⚠️ Company research not exposed as standalone endpoint
⚠️ Resume editing must be done in downloaded file
⚠️ No template selection (single professional template)
⚠️ No cover letter generation
⚠️ No interview prep features

### Known Bugs
❌ Database column `auto_flagged` missing (causes flag storage errors)
❌ Resume generation may fail if knowledge base is empty
❌ Some ATS systems not detected (Workday, Greenhouse need testing)
❌ Empty job descriptions should return error but don't

---

## Feedback Collection

### Questions to Ask Test Users

**Ease of Use:**
1. Was it clear what to do first?
2. Which knowledge base method did you prefer? (Voice/Upload/Import)
3. Did the loading times feel acceptable?
4. Were error messages helpful?

**Features:**
1. Did the resume match the job description well?
2. Were the keywords naturally integrated?
3. Did truth checking catch real issues?
4. Is the exported PDF professional-looking?

**Missing Features:**
1. What would you want to customize?
2. Would you use this for real job applications?
3. What other features would make it more useful?

**Overall:**
1. Rate 1-10: How likely are you to recommend this?
2. What's the #1 thing that needs improvement?
3. What's the #1 thing that impressed you?

---

## Next Steps After Demo

### For Developers
1. Review backend logs for errors
2. Check database for test data cleanup
3. Monitor API usage and costs
4. Fix bugs found during testing

### For Product
1. Prioritize bugs based on user impact
2. Design missing features (resume editing, templates)
3. Plan deployment to production
4. Create marketing materials

### For Users
1. Try with real resume data
2. Test with actual job applications
3. Compare generated resume to current resume
4. Track application success rate

---

**End of Demo Script**

*Built with Claude Code | Last Updated: October 8, 2025*
