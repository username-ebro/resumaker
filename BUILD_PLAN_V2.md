# Resumaker - Build Plan V2 (One-Shot Execution Ready)

**Date**: October 6, 2025
**Est. Build Time**: 45-60 hours (expanded scope)
**Status**: Ready for execution pending API keys

---

## Pre-Build Checklist ✅

### Required Before Starting

**API Keys & Credentials**:
- [ ] Supabase project URL
- [ ] Supabase anon key
- [ ] Supabase service role key
- [ ] Claude API key (Anthropic)
- [ ] Gemini API key (Google - from Car Talker or new)

**Assets to Migrate**:
- [ ] Car Talker OCR code (`/cartalker/test-gemini-ocr.js`)
- [ ] ATS Optimization Guide (`/job_hunt_system/ATS_Resume_Optimization_Guide_2025.md`)
- [ ] Resume parser (`/job_hunt_system/parse_resumes.py`)
- [ ] Sample resume database (69 files in `/job_hunt_system/context_parsed`)

**Decisions Finalized**:
- [x] Tech stack confirmed
- [x] MVP scope defined
- [x] New features specified (truth check, knowledge base, import, translation)
- [x] Database schema designed
- [ ] Domain name chosen (optional for MVP)

---

## Phase 1: Database Setup (Supabase)

### Tables to Create

```sql
-- ============================================
-- CORE USER TABLES
-- ============================================

-- user_profiles (extends Supabase auth.users)
CREATE TABLE user_profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  onboarding_completed BOOLEAN DEFAULT FALSE,
  preferred_language TEXT DEFAULT 'en',
  timezone TEXT DEFAULT 'America/Los_Angeles'
);

-- ============================================
-- KNOWLEDGE BASE (NEW - Core Feature)
-- ============================================

CREATE TYPE knowledge_type AS ENUM (
  'accomplishment',
  'skill',
  'experience',
  'story',
  'metric',
  'certification',
  'education',
  'project',
  'award',
  'publication'
);

CREATE TYPE knowledge_source AS ENUM (
  'conversation',
  'upload',
  'import_chatgpt',
  'import_claude',
  'manual',
  'inferred'
);

CREATE TABLE user_knowledge_base (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  knowledge_type knowledge_type NOT NULL,
  title TEXT, -- Brief title/summary
  content JSONB NOT NULL, -- Flexible structure per type
  source knowledge_source NOT NULL,
  verified BOOLEAN DEFAULT FALSE, -- Passed truth check
  confidence_score FLOAT DEFAULT 0.5, -- AI confidence (0-1)
  tags TEXT[], -- For categorization/search
  created_at TIMESTAMPTZ DEFAULT NOW(),
  last_referenced TIMESTAMPTZ DEFAULT NOW(),
  reference_count INT DEFAULT 0, -- Times used in resumes

  CONSTRAINT valid_confidence CHECK (confidence_score BETWEEN 0 AND 1)
);

CREATE INDEX idx_knowledge_user ON user_knowledge_base(user_id);
CREATE INDEX idx_knowledge_type ON user_knowledge_base(knowledge_type);
CREATE INDEX idx_knowledge_verified ON user_knowledge_base(verified);

-- ============================================
-- CONVERSATIONS
-- ============================================

CREATE TYPE conversation_type AS ENUM (
  'initial',
  'followup',
  'revision',
  'truth_check',
  'job_specific'
);

CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  session_date TIMESTAMPTZ DEFAULT NOW(),
  conversation_type conversation_type DEFAULT 'initial',
  language TEXT DEFAULT 'en', -- Language conversation was conducted in
  transcript JSONB, -- Array of {role, content, timestamp}
  questions_asked JSONB, -- Array of questions
  responses JSONB, -- Array of responses
  extracted_data JSONB, -- Parsed structured data
  duration_seconds INT,
  completed BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_conv_user ON conversations(user_id);
CREATE INDEX idx_conv_date ON conversations(session_date DESC);

-- ============================================
-- CONVERSATION IMPORTS (NEW - ChatGPT Paste Feature)
-- ============================================

CREATE TYPE import_source AS ENUM (
  'chatgpt',
  'claude',
  'gemini',
  'raw_text',
  'unknown'
);

CREATE TABLE conversation_imports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  import_source import_source NOT NULL,
  raw_text TEXT NOT NULL,
  parsed_data JSONB, -- Extracted structured information
  items_extracted INT DEFAULT 0,
  import_date TIMESTAMPTZ DEFAULT NOW(),
  processed BOOLEAN DEFAULT FALSE,
  processing_errors JSONB -- Any issues during parsing
);

CREATE INDEX idx_imports_user ON conversation_imports(user_id);

-- ============================================
-- RESUME ARTIFACTS (Uploaded PDFs/DOCX)
-- ============================================

CREATE TYPE artifact_type AS ENUM (
  'uploaded_resume',
  'uploaded_cv',
  'uploaded_cover_letter',
  'generated_resume',
  'generated_cover_letter',
  'reference_document'
);

CREATE TABLE resume_artifacts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  artifact_type artifact_type NOT NULL,
  file_url TEXT, -- Supabase storage URL
  file_name TEXT,
  file_size INT,
  mime_type TEXT,
  extracted_text TEXT, -- OCR result
  extracted_data JSONB, -- Structured parse
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  ocr_completed BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_artifacts_user ON resume_artifacts(user_id);

-- ============================================
-- JOB POSTINGS & TARGETING
-- ============================================

CREATE TABLE job_postings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  job_title TEXT NOT NULL,
  company_name TEXT NOT NULL,
  job_description TEXT,
  posting_url TEXT,
  location TEXT,
  salary_range TEXT,
  ats_system_id UUID, -- FK to ats_systems
  keywords_extracted JSONB, -- Array of keywords
  requirements JSONB, -- Structured requirements
  scraped_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_jobs_user ON job_postings(user_id);

-- ============================================
-- ATS SYSTEMS DATABASE
-- ============================================

CREATE TABLE ats_systems (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  ats_name TEXT UNIQUE NOT NULL, -- "Workday", "Greenhouse", etc.
  vendor TEXT,
  market_share FLOAT,
  formatting_rules JSONB, -- Specific formatting requirements
  keyword_strategy JSONB, -- How this ATS weights keywords
  special_requirements JSONB, -- Platform quirks
  parsing_quirks TEXT[],
  recommended_format TEXT DEFAULT 'docx',
  supports_pdf BOOLEAN DEFAULT TRUE,
  last_researched TIMESTAMPTZ,
  notes TEXT
);

-- Populate with data from ATS_Resume_Optimization_Guide_2025.md
INSERT INTO ats_systems (ats_name, vendor, market_share, recommended_format, supports_pdf) VALUES
  ('Workday', 'Workday Inc.', 28.0, 'docx', TRUE),
  ('iCIMS', 'iCIMS Inc.', 20.0, 'docx', TRUE),
  ('Taleo', 'Oracle', 18.0, 'docx', FALSE),
  ('Greenhouse', 'Greenhouse Software', 12.0, 'docx', TRUE),
  ('Lever', 'Lever Inc.', 8.0, 'docx', TRUE),
  ('SmartRecruiters', 'SmartRecruiters Inc.', 5.0, 'docx', TRUE),
  ('JazzHR', 'JazzHR', 3.0, 'docx', TRUE),
  ('BambooHR', 'BambooHR', 2.0, 'docx', TRUE),
  ('ADP', 'ADP Inc.', 2.0, 'docx', FALSE),
  ('SAP SuccessFactors', 'SAP', 2.0, 'docx', TRUE);

-- ============================================
-- RESUME VERSIONS (Generated Resumes)
-- ============================================

CREATE TABLE resume_versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  version_number INT NOT NULL,
  title TEXT, -- "Software Engineer - Google", "PM - Startup"
  target_job_id UUID REFERENCES job_postings(id),

  content JSONB NOT NULL, -- Full resume structure
  formatting_params JSONB, -- Font, margins, spacing

  keyword_match_score FLOAT, -- % match with target job
  ats_system_id UUID REFERENCES ats_systems(id),
  ats_optimized BOOLEAN DEFAULT FALSE,

  truth_check_completed BOOLEAN DEFAULT FALSE,
  truth_check_flags_count INT DEFAULT 0,

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  is_active BOOLEAN DEFAULT TRUE,

  pdf_url TEXT, -- Generated PDF in storage
  docx_url TEXT, -- Generated DOCX in storage
  txt_content TEXT -- Plain text version
);

CREATE INDEX idx_resume_user ON resume_versions(user_id);
CREATE INDEX idx_resume_active ON resume_versions(is_active) WHERE is_active = TRUE;

-- ============================================
-- TRUTH CHECK SYSTEM (NEW - Core Feature)
-- ============================================

CREATE TYPE flag_reason_type AS ENUM (
  'unsupported_claim',
  'missing_evidence',
  'exaggerated_language',
  'date_inconsistency',
  'unverified_metric',
  'skill_not_discussed',
  'education_unverified',
  'vague_quantification'
);

CREATE TYPE user_action_type AS ENUM (
  'pending',
  'confirmed',
  'corrected',
  'removed',
  'deferred'
);

CREATE TABLE truth_check_flags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  resume_version_id UUID REFERENCES resume_versions(id) ON DELETE CASCADE,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,

  flagged_item TEXT NOT NULL, -- The specific claim
  flag_reason flag_reason_type NOT NULL,
  flag_explanation TEXT, -- Why it was flagged
  severity TEXT DEFAULT 'medium', -- low, medium, high

  supporting_evidence JSONB, -- References to conversation/knowledge base
  suggested_alternative TEXT, -- AI suggestion

  user_action user_action_type DEFAULT 'pending',
  original_value TEXT,
  corrected_value TEXT,
  user_notes TEXT,

  created_at TIMESTAMPTZ DEFAULT NOW(),
  resolved_at TIMESTAMPTZ,

  CONSTRAINT valid_severity CHECK (severity IN ('low', 'medium', 'high'))
);

CREATE INDEX idx_flags_resume ON truth_check_flags(resume_version_id);
CREATE INDEX idx_flags_pending ON truth_check_flags(user_action) WHERE user_action = 'pending';

-- ============================================
-- TRANSLATIONS (NEW - Multi-Language Support)
-- ============================================

CREATE TABLE user_translations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  conversation_id UUID REFERENCES conversations(id),

  original_language TEXT NOT NULL, -- ISO code: 'es', 'vi', 'zh', etc.
  original_text TEXT NOT NULL,
  translated_text TEXT NOT NULL,

  context TEXT, -- What question was being answered
  translation_quality_score FLOAT, -- AI confidence in translation
  human_reviewed BOOLEAN DEFAULT FALSE,

  translation_date TIMESTAMPTZ DEFAULT NOW(),

  CONSTRAINT valid_quality CHECK (translation_quality_score BETWEEN 0 AND 1)
);

CREATE INDEX idx_trans_user ON user_translations(user_id);
CREATE INDEX idx_trans_conversation ON user_translations(conversation_id);

-- ============================================
-- USER DATA POINTS (Granular Extracted Info)
-- ============================================

CREATE TYPE data_point_category AS ENUM (
  'accomplishment',
  'skill',
  'experience',
  'metric',
  'story',
  'certification',
  'education',
  'project',
  'award',
  'language',
  'tool',
  'methodology'
);

CREATE TABLE user_data_points (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  conversation_id UUID REFERENCES conversations(id),

  category data_point_category NOT NULL,
  question_asked TEXT,
  response_text TEXT,
  response_audio_url TEXT, -- If from voice input

  extracted_value JSONB, -- Structured extraction
  confidence_score FLOAT DEFAULT 0.5,
  verified BOOLEAN DEFAULT FALSE,

  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),

  CONSTRAINT valid_dp_confidence CHECK (confidence_score BETWEEN 0 AND 1)
);

CREATE INDEX idx_datapoints_user ON user_data_points(user_id);
CREATE INDEX idx_datapoints_category ON user_data_points(category);

-- ============================================
-- ACTIVITY LOG (Audit Trail)
-- ============================================

CREATE TABLE activity_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  activity_type TEXT NOT NULL,
  activity_data JSONB,
  ip_address TEXT,
  user_agent TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_activity_user ON activity_log(user_id);
CREATE INDEX idx_activity_date ON activity_log(created_at DESC);

-- ============================================
-- HELPER FUNCTIONS
-- ============================================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_user_profiles_updated_at
  BEFORE UPDATE ON user_profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_resume_versions_updated_at
  BEFORE UPDATE ON resume_versions
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

---

## Phase 2: File Structure

```
resumaker/
├── README.md
├── CONTEXT.md
├── CHANGELOG.md
├── PROJECT_VISION_V2.md
├── BUILD_PLAN_V2.md
├── .env.example
├── .gitignore
│
├── backend/                           # Python (FastAPI)
│   ├── main.py                        # FastAPI app entry
│   ├── config.py                      # Environment config
│   ├── requirements.txt
│   │
│   ├── api/                           # API routes
│   │   ├── __init__.py
│   │   ├── auth.py                    # Auth endpoints
│   │   ├── conversations.py           # Conversation management
│   │   ├── resumes.py                 # Resume CRUD
│   │   ├── jobs.py                    # Job posting management
│   │   ├── uploads.py                 # File upload handling
│   │   ├── truth_check.py             # Truth verification endpoints (NEW)
│   │   ├── knowledge_base.py          # Knowledge base CRUD (NEW)
│   │   ├── imports.py                 # ChatGPT/Claude import (NEW)
│   │   └── translations.py            # Multi-language support (NEW)
│   │
│   ├── services/                      # Business logic
│   │   ├── __init__.py
│   │   ├── ocr_service.py             # Gemini OCR (from Car Talker)
│   │   ├── conversation_ai.py         # Claude conversation management
│   │   ├── resume_generator.py        # Core resume generation
│   │   ├── ats_optimizer.py           # ATS-specific optimization
│   │   ├── formatting_engine.py       # Smart typography
│   │   ├── export_service.py          # PDF/DOCX generation
│   │   ├── truth_checker.py           # Truth verification logic (NEW)
│   │   ├── knowledge_extractor.py     # Extract data from conversations (NEW)
│   │   ├── import_parser.py           # Parse ChatGPT/Claude imports (NEW)
│   │   └── translation_service.py     # Multi-language translation (NEW)
│   │
│   ├── models/                        # Data models (Pydantic)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── conversation.py
│   │   ├── resume.py
│   │   ├── job.py
│   │   ├── knowledge_base.py          # (NEW)
│   │   ├── truth_check.py             # (NEW)
│   │   └── translation.py             # (NEW)
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── supabase_client.py         # Supabase SDK wrapper
│   │   ├── claude_client.py           # Anthropic Claude wrapper
│   │   ├── gemini_client.py           # Google Gemini wrapper
│   │   ├── voice_processor.py         # Audio processing
│   │   ├── text_optimizer.py          # Text manipulation
│   │   └── validators.py              # Input validation
│   │
│   └── data/                          # Static data files
│       ├── ats_systems.json           # ATS platform data
│       ├── question_bank.json         # Conversation prompts
│       ├── question_bank_es.json      # Spanish questions (NEW)
│       ├── question_bank_vi.json      # Vietnamese questions (NEW)
│       ├── question_bank_zh.json      # Mandarin questions (NEW)
│       ├── formatting_rules.json      # Typography rules
│       └── action_verbs.json          # Strong action verbs library
│
├── frontend/                          # Next.js
│   ├── package.json
│   ├── next.config.js
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   │
│   ├── src/
│   │   ├── app/                       # Next.js 13+ app router
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx               # Landing page
│   │   │   ├── auth/
│   │   │   │   ├── login/page.tsx
│   │   │   │   └── signup/page.tsx
│   │   │   ├── dashboard/page.tsx
│   │   │   ├── conversation/page.tsx
│   │   │   ├── truth-check/page.tsx   # (NEW)
│   │   │   ├── knowledge-base/page.tsx # (NEW)
│   │   │   ├── import/page.tsx        # (NEW)
│   │   │   ├── editor/page.tsx
│   │   │   └── export/page.tsx
│   │   │
│   │   ├── components/
│   │   │   ├── Auth/
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   └── SignupForm.tsx
│   │   │   ├── Conversation/
│   │   │   │   ├── VoiceRecorder.tsx
│   │   │   │   ├── QuestionDisplay.tsx
│   │   │   │   ├── ResponseCapture.tsx
│   │   │   │   ├── LanguageSelector.tsx    # (NEW)
│   │   │   │   └── ProgressIndicator.tsx
│   │   │   ├── TruthCheck/                 # (NEW)
│   │   │   │   ├── FlagList.tsx
│   │   │   │   ├── FlagReview.tsx
│   │   │   │   └── VerificationModal.tsx
│   │   │   ├── KnowledgeBase/              # (NEW)
│   │   │   │   ├── KnowledgeGrid.tsx
│   │   │   │   ├── KnowledgeDetail.tsx
│   │   │   │   └── KnowledgeSearch.tsx
│   │   │   ├── Import/                     # (NEW)
│   │   │   │   ├── PasteArea.tsx
│   │   │   │   ├── ParseResults.tsx
│   │   │   │   └── ImportConfirm.tsx
│   │   │   ├── ResumeEditor/
│   │   │   │   ├── VisualEditor.tsx
│   │   │   │   ├── SectionEditor.tsx
│   │   │   │   ├── FormattingControls.tsx
│   │   │   │   └── LivePreview.tsx
│   │   │   ├── Upload/
│   │   │   │   ├── DragDrop.tsx
│   │   │   │   └── OCRStatus.tsx
│   │   │   ├── Export/
│   │   │   │   ├── FormatSelector.tsx
│   │   │   │   └── DownloadButton.tsx
│   │   │   └── Shared/
│   │   │       ├── Button.tsx
│   │   │       ├── Modal.tsx
│   │   │       ├── Toast.tsx
│   │   │       └── LoadingSpinner.tsx
│   │   │
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useConversation.ts
│   │   │   ├── useVoiceRecording.ts
│   │   │   ├── useTruthCheck.ts           # (NEW)
│   │   │   ├── useKnowledgeBase.ts        # (NEW)
│   │   │   ├── useTranslation.ts          # (NEW)
│   │   │   └── useResume.ts
│   │   │
│   │   ├── lib/
│   │   │   ├── supabase.ts                # Supabase client
│   │   │   ├── api.ts                     # API client
│   │   │   └── utils.ts                   # Helper functions
│   │   │
│   │   └── types/
│   │       ├── user.ts
│   │       ├── conversation.ts
│   │       ├── resume.ts
│   │       ├── knowledge.ts               # (NEW)
│   │       └── truth-check.ts             # (NEW)
│   │
│   └── public/
│       ├── images/
│       └── fonts/
│
├── migrations/                        # Supabase migrations
│   └── 001_initial_schema.sql
│
├── scripts/                           # Utility scripts
│   ├── seed_ats_data.py               # Populate ATS systems
│   ├── seed_question_bank.py          # Load question templates
│   └── migrate_cartalker_ocr.py       # Adapt Car Talker code
│
├── tests/                             # Test suite
│   ├── backend/
│   │   ├── test_truth_checker.py      # (NEW)
│   │   ├── test_import_parser.py      # (NEW)
│   │   ├── test_knowledge_extractor.py # (NEW)
│   │   └── ...
│   └── frontend/
│       └── ...
│
└── docs/
    ├── API.md                         # API documentation
    ├── DEPLOYMENT.md                  # Deploy instructions
    ├── TRUTH_CHECK_ALGORITHM.md       # (NEW)
    ├── IMPORT_PARSING_LOGIC.md        # (NEW)
    └── TRANSLATION_GUIDELINES.md      # (NEW)
```

---

## Phase 3: Core Components Build Order

### Priority 0 (Foundation) - 8-10 hours

**1. Backend Setup**
- FastAPI app structure
- Supabase client configuration
- Environment variables
- CORS and middleware
- Health check endpoints

**2. Frontend Setup**
- Next.js project initialization
- Tailwind CSS configuration
- Supabase client setup
- Basic routing structure

**3. Authentication**
- Supabase Auth integration (frontend + backend)
- Login/signup flows
- Protected routes
- Session management

---

### Priority 1 (Core MVP) - 15-18 hours

**4. OCR Service** (from Car Talker)
- Migrate Gemini OCR code to Python
- Adapt prompt from "receipt" to "resume"
- Structured extraction: contact, experience, skills, education
- File upload handling
- Integration with Supabase storage

**5. Conversation System**
- Question bank (English first)
- Claude API integration
- Text input/output
- Conversation state management
- Response storage in database
- Progress tracking

**6. Voice Interface**
- Web Speech API integration
- Record/pause/stop controls
- Audio transcription
- Audio file storage (Supabase)
- Fallback to text input

**7. Knowledge Extractor** (NEW)
- Extract structured data from conversation
- Parse accomplishments, skills, experience
- Assign confidence scores
- Store in user_knowledge_base table
- Deduplicate similar entries

---

### Priority 2 (New Core Features) - 12-15 hours

**8. ChatGPT/Claude Import Parser** (NEW)
- Text paste interface (frontend)
- Smart parsing algorithm (backend)
- Detect conversation structure
- Extract user responses (not AI responses)
- Identify: accomplishments, skills, metrics, stories
- Store in conversation_imports table
- Merge into knowledge base
- Flag potential duplicates

**9. Truth Verification System** (NEW)
- Truth checker algorithm:
  - Compare resume claims vs. conversation data
  - Identify unsupported claims
  - Flag vague/exaggerated language
  - Detect date inconsistencies
  - Check quantitative claims
- Generate truth_check_flags
- Frontend truth check UI:
  - Display flagged items
  - Show supporting evidence (or lack thereof)
  - Allow user to confirm/correct/remove
  - Provide suggested alternatives
- Regenerate resume after corrections

**10. Multi-Language Support** (NEW)
- Language selector (frontend)
- Translate question bank (Spanish, Vietnamese, Mandarin)
- Accept responses in native language
- Claude translation to English
- Preserve meaning and context
- Store translations in user_translations table

---

### Priority 3 (Resume Generation) - 10-12 hours

**11. Resume Generator**
- Compile data from knowledge base
- Apply ATS optimization rules
- Use ATS guide (ATS_Resume_Optimization_Guide_2025.md)
- Structure content by best practices:
  - Professional summary
  - Work experience (bullets with metrics)
  - Skills section
  - Education
  - Certifications
- Generate content JSONB

**12. Job Targeting & ATS Optimization**
- Job description input
- Keyword extraction
- ATS system detection
- Match resume to job posting
- Calculate keyword match score
- Apply platform-specific rules (Workday, Greenhouse, etc.)

**13. Formatting Engine**
- Typography calculations:
  - Character-per-line based on font/margin
  - Line break optimization
  - Prevent orphan text
- Margin/font size controls
- Apply formatting rules from ATS guide

---

### Priority 4 (Export & Polish) - 8-10 hours

**14. PDF Export** (WeasyPrint)
- Convert resume JSONB to HTML template
- Apply CSS styling
- Generate PDF with WeasyPrint
- Store in Supabase storage
- Download link

**15. DOCX Export** (python-docx)
- Convert resume JSONB to Word document
- Maintain ATS-friendly formatting
- No tables, no columns, standard fonts
- Store in Supabase storage
- Download link

**16. Visual Editor** (Basic)
- Live preview of resume
- Section reordering (drag-and-drop)
- Inline editing of text
- Formatting controls (font, margins)
- Real-time character count

---

### Priority 5 (Nice-to-Haves if Time) - 5-8 hours

**17. Knowledge Base UI**
- Grid view of user's knowledge
- Search/filter by type
- Edit/delete knowledge items
- View usage (which resumes reference this)

**18. Resume Versioning**
- Multiple resume versions per user
- Comparison view
- Duplicate and modify
- Archive old versions

**19. Cover Letter Generator**
- Use same knowledge base
- Generate cover letter from resume data
- Job-specific customization

---

## Phase 4: Testing & Deployment - 4-6 hours

**20. Testing**
- Unit tests for truth checker
- Integration tests for import parser
- E2E tests for conversation flow
- OCR accuracy testing
- Translation quality checks

**21. Deployment**
- Deploy backend to Railway
- Deploy frontend to Vercel
- Configure environment variables
- Set up Supabase production instance
- Domain configuration (if ready)

---

## Phase 5: Data Migration & Seeding

### ATS Systems Data
**Source**: `/job_hunt_system/ATS_Resume_Optimization_Guide_2025.md`

**Extracted Data**:
- Platform names (Workday, iCIMS, Greenhouse, Lever, Taleo, etc.)
- Market share statistics
- Formatting requirements
- Parsing quirks
- Keyword strategies
- PDF support
- Recommended formats

**Script**: `scripts/seed_ats_data.py`
- Parse markdown guide
- Extract platform-specific rules
- Insert into ats_systems table
- Populate formatting_rules JSONB

---

### Question Bank
**Sources**:
- Interview prep guides
- Resume writing frameworks
- LLM-generated questions (Claude)

**Categories** (from PROJECT_VISION_V2):
1. Professional Identity (3-5 questions)
2. Accomplishments (5-7 questions)
3. Skills & Expertise (4-6 questions)
4. Growth & Challenges (3-5 questions)
5. Experience Details (5-7 questions)
6. Metrics & Data (4-6 questions)
7. Stories & Anecdotes (3-5 questions)

**Total**: ~30-45 questions in question bank

**Multi-Language**:
- English (primary)
- Spanish translation
- Vietnamese translation
- Mandarin translation
- (Expand as needed)

**Format** (question_bank.json):
```json
[
  {
    "id": "prof_01",
    "category": "professional_identity",
    "order": 1,
    "question_en": "What role are you targeting in your job search?",
    "question_es": "¿Qué puesto buscas en tu búsqueda de empleo?",
    "question_vi": "Bạn đang nhắm đến vị trí nào trong tìm kiếm việc làm?",
    "question_zh": "你在求职中的目标职位是什么？",
    "follow_up_triggers": ["experience_level", "industry_preference"],
    "expected_response_type": "short_answer",
    "importance": "critical"
  },
  ...
]
```

---

## Phase 6: Algorithm Specs

### Truth Checker Algorithm

**Input**:
- Resume version (generated content)
- User's knowledge base
- Conversation transcripts

**Process**:

1. **Extract Claims from Resume**
   - Parse each bullet point
   - Identify quantitative claims (%, $, numbers)
   - Extract skills listed
   - Extract job titles and companies
   - Extract education/certifications

2. **Cross-Reference with Knowledge Base**
   - For each claim, search knowledge base
   - Check conversation transcripts
   - Calculate evidence strength (0-1)

3. **Flag Generation Logic**:
   ```python
   if claim.has_quantitative_data():
       if not knowledge_base.contains_exact_number(claim.number):
           flag(claim, reason="unverified_metric", severity="high")

   if claim.mentions_skill():
       if not conversation.discussed_skill(claim.skill):
           flag(claim, reason="skill_not_discussed", severity="medium")

   if claim.has_superlative() or claim.has_exaggeration():
       if evidence_strength < 0.7:
           flag(claim, reason="exaggerated_language", severity="medium")

   if claim.has_date_range():
       if date_conflict_detected(claim, knowledge_base):
           flag(claim, reason="date_inconsistency", severity="high")
   ```

4. **Output**:
   - List of flagged items
   - For each flag:
     - Claim text
     - Reason for flag
     - Severity
     - Supporting evidence (or lack thereof)
     - Suggested alternative

**Frontend Display**:
```
🚦 TRUTH CHECK: 5 items need review

HIGH PRIORITY:
1. "Increased revenue by 150%" (Work Experience - TechCorp)
   ⚠️ You mentioned growth but didn't specify this percentage
   Evidence: Conversation #1 (June 5): "We saw significant growth"
   → What was the actual percentage increase?

   [Confirm] [Edit] [Remove]

MEDIUM PRIORITY:
2. "Expert in Python, JavaScript, C++, and Go" (Skills)
   ⚠️ You discussed Python extensively, but only briefly mentioned JavaScript
   Evidence: No discussion of C++ or Go found
   → Should we adjust this claim to match your actual experience?

   Suggested: "Proficient in Python, with experience in JavaScript"

   [Accept Suggestion] [Edit Manually] [Keep Original]
```

---

### Import Parser Algorithm (ChatGPT/Claude Conversation)

**Input**: Raw text paste from user

**Process**:

1. **Detect Source**
   ```python
   if "ChatGPT" in text or "gpt-4" in text:
       source = "chatgpt"
   elif "Claude" in text or "Anthropic" in text:
       source = "claude"
   else:
       source = "unknown"
   ```

2. **Parse Conversation Structure**
   - Identify user messages vs. AI messages
   - Extract user responses only
   - Preserve context (what question was being answered)

3. **Extract Structured Data**
   Use Claude to parse user responses:
   ```
   Prompt to Claude:
   "Extract the following from this conversation:
   - Companies mentioned (with dates)
   - Job titles held
   - Skills discussed
   - Accomplishments described
   - Quantitative metrics mentioned
   - Stories or anecdotes
   - Education/certifications

   Return as structured JSON."
   ```

4. **Store Results**:
   - Raw text → `conversation_imports.raw_text`
   - Parsed data → `conversation_imports.parsed_data`
   - Extract items and add to `user_knowledge_base`

5. **Duplicate Detection**:
   - Compare with existing knowledge base
   - Flag potential duplicates
   - Allow user to merge or keep separate

**Example**:
```
Input (pasted from ChatGPT):
User: I worked at Google for 3 years as a product manager
AI: That's great! What were your main accomplishments?
User: I launched a feature that got 10M users in the first month
AI: Impressive! Can you tell me more about...

Parsed Output:
{
  "companies": [
    {
      "name": "Google",
      "duration": "3 years",
      "role": "Product Manager"
    }
  ],
  "accomplishments": [
    {
      "description": "Launched feature with 10M users in first month",
      "metric": "10M users",
      "timeframe": "first month"
    }
  ],
  "skills_implied": ["Product Management", "Feature Launch"]
}
```

---

### Translation Algorithm (Multi-Language)

**Input**:
- User's response in native language
- Original question (for context)
- Target language (English)

**Process**:

1. **Detect Source Language** (Claude can auto-detect)

2. **Translate with Context Preservation**
   ```
   Prompt to Claude:
   "Translate this resume-related response from [language] to professional English:

   Original Question: [question in native language]
   User Response: [response in native language]

   Requirements:
   - Maintain professional tone suitable for resume
   - Preserve specific numbers, dates, company names
   - Adapt cultural references for English-speaking context
   - Maintain authenticity of achievements
   - Use strong action verbs where appropriate

   Return:
   - Translated text
   - Confidence score (0-1)
   - Any cultural notes or ambiguities"
   ```

3. **Quality Check**:
   - Ensure no information lost
   - Flag if translation confidence < 0.7
   - Allow user to review translation

4. **Store**:
   - Original text → `user_translations.original_text`
   - Translated text → `user_translations.translated_text`
   - Quality score → `user_translations.translation_quality_score`

**Example**:
```
Input (Spanish):
Question: "Cuéntame sobre un logro del que estés orgulloso"
Response: "En mi trabajo anterior como gerente de proyectos,
           logré reducir los costos en un 30% mientras mantenía
           la calidad del producto"

Translation Output:
{
  "translated_text": "In my previous role as Project Manager,
                      I reduced costs by 30% while maintaining
                      product quality",
  "quality_score": 0.95,
  "notes": "Direct translation - professional tone maintained"
}
```

---

## Estimated Build Time Breakdown

| Phase | Component | Hours |
|-------|-----------|-------|
| **P0: Foundation** | Backend + Frontend setup, Auth | 8-10 |
| **P1: Core MVP** | OCR, Conversation, Voice, Knowledge Extraction | 15-18 |
| **P2: New Features** | Import Parser, Truth Check, Multi-Language | 12-15 |
| **P3: Resume Gen** | Generator, ATS Optimization, Formatting | 10-12 |
| **P4: Export** | PDF, DOCX, Visual Editor | 8-10 |
| **P5: Polish** | Knowledge Base UI, Versioning, Cover Letters | 5-8 |
| **P6: Deploy** | Testing, Deployment, Configuration | 4-6 |
| **TOTAL** | | **62-79 hours** |

**Realistic Estimate**: 45-60 hours for streamlined MVP (skip P5 nice-to-haves)

---

## Ready to Execute?

### Final Pre-Build Checklist:

**Required**:
- [ ] Supabase project created + credentials
- [ ] Claude API key obtained
- [ ] Gemini API key (from Car Talker or new)
- [ ] Car Talker OCR code migrated to resumaker/backend/services/
- [ ] ATS guide copied to resumaker/backend/data/
- [ ] Question bank drafted (English)

**Recommended**:
- [ ] Domain name decided (or "TBD" acceptable for MVP)
- [ ] Translations for questions (Spanish, Vietnamese, Mandarin) - can be done post-MVP

**Optional**:
- [ ] Sample resumes for testing (use job_hunt_system parsed resumes)
- [ ] Beta testers identified
- [ ] Feedback collection plan

---

**Status**: Comprehensive plan complete ✅
**Next Step**: Gather API keys → Execute one-shot build
**Build Owner**: Claude (following this plan)
**Product Owner**: Evan Stoudt

---

**Questions Before Build**:
1. Should we prioritize all of P2 (import, truth check, translation) or build incrementally?
2. Is multi-language support P0 (must-have MVP) or P1 (nice-to-have for v1)?
3. Do we want full visual editor (complex) or basic preview + edit (simpler)?

Your call - I'm ready to build when you are! 🚀
