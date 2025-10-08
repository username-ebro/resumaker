# Resumaker - Build Plan & Implementation Prompt

## Pre-Build Checklist
**DO NOT START UNTIL ALL ITEMS COMPLETE:**

- [ ] Supabase project created
- [ ] Supabase credentials/keys obtained
- [ ] API keys secured (OpenAI/Anthropic for conversations)
- [ ] Existing resume logic migrated to /resumaker
- [ ] Car Talker OCR code reviewed & copied
- [ ] ATS research completed (database schema designed)
- [ ] Frontend framework decision made
- [ ] Voice API selected and tested
- [ ] File structure agreed upon
- [ ] All permissions granted to Claude

---

## Phase 1: Architecture & Setup

### Database Schema (Supabase)

**Tables to Create:**

```sql
-- Users (handled by Supabase Auth)

-- user_profiles
- id (UUID, FK to auth.users)
- created_at
- updated_at
- onboarding_completed (boolean)

-- conversations
- id (UUID)
- user_id (FK)
- session_date
- transcript (JSONB)
- questions_asked (JSONB array)
- responses (JSONB array)
- conversation_type (enum: initial, followup, revision)

-- resume_artifacts
- id (UUID)
- user_id (FK)
- artifact_type (enum: uploaded, generated)
- file_url (text - Supabase storage)
- extracted_text (text)
- metadata (JSONB)
- created_at

-- resume_versions
- id (UUID)
- user_id (FK)
- version_number (int)
- target_job_id (FK)
- content (JSONB)
- formatting_params (JSONB)
- created_at
- is_active (boolean)

-- job_postings
- id (UUID)
- user_id (FK)
- job_title
- company_name
- job_description (text)
- ats_system_id (FK)
- posting_url
- scraped_at

-- ats_systems
- id (UUID)
- ats_name (text - "Workday", "Greenhouse", etc.)
- formatting_rules (JSONB)
- keyword_weight (float)
- special_requirements (JSONB)
- last_researched

-- user_data_points
- id (UUID)
- user_id (FK)
- category (enum: accomplishment, skill, experience, metric, story)
- question_asked (text)
- response_text (text)
- response_audio_url (text)
- metadata (JSONB)
- created_at
```

### File Structure

```
resumaker/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── conversations.py
│   │   ├── resumes.py
│   │   ├── jobs.py
│   │   └── uploads.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ocr_service.py          # From Car Talker
│   │   ├── conversation_ai.py      # LLM integration
│   │   ├── resume_generator.py     # Core logic
│   │   ├── ats_optimizer.py        # ATS-specific rules
│   │   ├── formatting_engine.py    # Smart typography
│   │   └── export_service.py       # PDF/DOCX generation
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── conversation.py
│   │   ├── resume.py
│   │   └── job.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── supabase_client.py
│   │   ├── voice_processor.py
│   │   └── text_optimizer.py
│   ├── config.py
│   ├── main.py                     # FastAPI app
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Auth/
│   │   │   ├── Conversation/
│   │   │   ├── ResumeEditor/
│   │   │   ├── Upload/
│   │   │   └── Export/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── App.jsx
│   ├── public/
│   └── package.json
├── data/
│   ├── ats_systems.json            # ATS research data
│   ├── question_bank.json          # Conversation prompts
│   └── formatting_rules.json
├── migrations/                      # Supabase migrations
├── tests/
├── docs/
│   ├── API.md
│   └── DEPLOYMENT.md
├── .env.example
├── .gitignore
├── README.md
├── CONTEXT.md
├── CHANGELOG.md
├── PROJECT_VISION.md
└── BUILD_PLAN.md (this file)
```

---

## Phase 2: Core Components to Build

### 1. OCR Service
**Priority**: HIGH
**Dependencies**: Car Talker code
**Function**: Extract text from uploaded PDF/image resumes

### 2. Conversation AI Service
**Priority**: HIGH
**Dependencies**: LLM API (Claude/GPT)
**Functions**:
- Generate contextual questions
- Process voice/text responses
- Maintain conversation state
- Extract structured data from narratives

### 3. Resume Generator
**Priority**: HIGH
**Dependencies**: User data points, job posting, ATS rules
**Functions**:
- Compile data into resume sections
- Apply ATS-specific optimizations
- Generate multiple resume variations

### 4. Formatting Engine
**Priority**: MEDIUM
**Dependencies**: Resume content, formatting params
**Functions**:
- Calculate character limits per line
- Optimize word breaks
- Enforce margins (0.25", 0.5", etc.)
- Font size awareness (10pt, 11pt, 12pt)
- Prevent orphan/widow text
- Smart bullet point spacing

### 5. Export Service
**Priority**: HIGH
**Dependencies**: Formatted resume data
**Functions**:
- Generate PDF (ReportLab/WeasyPrint)
- Generate DOCX (python-docx)
- Generate plain text
- Maintain formatting consistency

### 6. ATS Optimizer
**Priority**: MEDIUM
**Dependencies**: ATS database
**Functions**:
- Match job posting to ATS system
- Apply ATS-specific rules
- Keyword optimization
- Format adjustments per system

---

## Phase 3: Frontend Components

### 1. Voice Interface
- Web Speech API integration
- Record/pause/stop controls
- Transcription display
- Fallback to text input

### 2. Conversation UI
- Chat-like interface
- Question display
- Response capture (voice + text)
- Progress indicator

### 3. Resume Editor
- Real-time visual preview
- Section editing
- Drag-and-drop reordering
- Formatting controls
- Margin/font size selectors

### 4. Upload Component
- Drag-and-drop file upload
- OCR processing indicator
- Extracted text review

### 5. Export Component
- Format selection (PDF/DOCX/TXT)
- Download buttons
- Version history

---

## Phase 4: Question Bank Design

**Categories:**

1. **Professional Identity**
   - What role are you targeting?
   - What industries interest you?
   - What's your professional superpower?

2. **Accomplishments**
   - Tell me about a project you're proud of
   - What's a result you achieved that surprised you?
   - When have you exceeded expectations?

3. **Skills & Expertise**
   - What tools/technologies do you know well?
   - What do colleagues ask you for help with?
   - What have you taught others?

4. **Growth & Challenges**
   - Tell me about a time you failed and what you learned
   - What's something you're working to improve?
   - Describe a difficult situation you navigated

5. **Experience Details**
   - Walk me through your current/most recent role
   - What were your day-to-day responsibilities?
   - Who did you work with?

6. **Metrics & Data**
   - What numbers can you attach to your work?
   - How did you measure success?
   - What was the before/after of your impact?

7. **Stories & Anecdotes**
   - Tell me about a typical day
   - What's a moment that defined your career?
   - Describe your work style

**Question Flow Logic:**
- Start broad → get specific
- Follow-up based on previous answers
- Detect missing data and probe
- Adaptive based on user's background

---

## Phase 5: ATS Research & Database

**Systems to Research:**
1. Workday
2. Greenhouse
3. Lever
4. iCIMS
5. Taleo
6. SmartRecruiters
7. JazzHR
8. BambooHR
9. ADP
10. SAP SuccessFactors

**Data to Collect per ATS:**
- Parsing quirks
- Keyword weighting algorithm
- Formatting preferences
- Special fields
- Common failure modes
- Optimization tips

---

## Phase 6: Smart Formatting Logic

### Typography Calculations

```python
# Example logic
def calculate_line_capacity(
    margin_left: float,
    margin_right: float,
    page_width: float = 8.5,  # inches
    font_size: int = 11,
    font_family: str = "Arial"
) -> int:
    """
    Calculate max characters per line
    """
    usable_width = page_width - margin_left - margin_right
    avg_char_width = get_char_width(font_family, font_size)
    chars_per_inch = 1 / avg_char_width
    return int(usable_width * chars_per_inch)

def optimize_line_breaks(
    text: str,
    max_chars: int,
    available_space: int
) -> str:
    """
    Prevent short lines when space allows more text
    """
    # Smart word wrapping logic
    # Avoid orphans
    # Balance line lengths
    pass
```

### Margin Presets
- Conservative: 1" all sides
- Standard: 0.75" all sides
- Aggressive: 0.5" all sides
- Custom: User-defined

---

## Phase 7: Integration Points

### Supabase
- Auth: `supabase.auth`
- Database: `supabase.from_('table_name')`
- Storage: `supabase.storage` (for files)
- Realtime: Optional for live collaboration

### LLM (Claude/GPT)
- Conversation management
- Question generation
- Response parsing
- Resume writing
- Cover letter generation

### Voice Processing
- Speech-to-text
- Text-to-speech (optional for questions)
- Audio storage

### Car Talker OCR
- Migrate existing Gemini integration
- Extract text from images/PDFs
- Handle multi-page documents

---

## One-Shot Build Prompt Template

**When ready to build, provide:**

```
CONTEXT:
- Supabase project URL: [URL]
- Supabase anon key: [KEY]
- Supabase service key: [KEY]
- LLM API key: [KEY]
- Frontend framework choice: [React/Next/Svelte]
- Voice API choice: [Web Speech API/other]

INSTRUCTIONS:
Build the Resumaker MVP according to BUILD_PLAN.md with the following specifications:

1. Set up backend (FastAPI) with all services in Phase 2
2. Set up frontend with components in Phase 3
3. Implement database schema from Phase 1
4. Integrate OCR from [Car Talker location]
5. Create question bank from Phase 4
6. Implement formatting engine from Phase 6
7. Build export functionality (PDF/DOCX/TXT)

PRIORITY ORDER:
1. Auth & user profiles
2. OCR upload
3. Conversation system (text first, voice second)
4. Resume generation
5. Export (PDF priority)
6. ATS optimization
7. Visual editor

DELIVERABLES:
- Fully functional backend API
- Working frontend application
- Database migrations
- Environment setup docs
- Testing suite
- Deployment instructions

SPECIAL REQUIREMENTS:
- Follow file structure exactly as specified
- Use existing Car Talker OCR code
- Smart formatting with typography awareness
- Voice interface that feels conversational
- Clean, professional resume outputs
```

---

## Open Questions to Resolve Before Build

1. **Frontend Framework**: React/Next.js/Svelte?
2. **Voice API**: Web Speech API vs. paid service?
3. **LLM Choice**: Claude (Anthropic) vs. GPT (OpenAI) vs. both?
4. **PDF Library**: ReportLab vs. WeasyPrint?
5. **Hosting**: Vercel/Netlify (frontend) + Railway/Render (backend)?
6. **Domain**: resumaker.com? Different name?
7. **ATS Research**: Manual vs. scrape vs. purchase data?
8. **Existing Resume Logic**: Where is it? What format?
9. **Car Talker OCR**: Confirm it works with PDFs, not just images?
10. **MVP Scope**: Which features are truly essential vs. nice-to-have?

---

## Estimated Build Time
- **Backend Core**: 12-16 hours
- **Frontend Core**: 10-14 hours
- **Integration & Testing**: 6-8 hours
- **Polish & Deployment**: 4-6 hours
- **TOTAL**: 32-44 hours (one-shot execution)

---

**Status**: Planning Complete - Awaiting Decisions
**Next Step**: Answer open questions → Finalize prompt → Execute build
