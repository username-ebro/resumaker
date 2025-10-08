# Resumaker - Project Vision V2 (Updated)

**Date**: October 6, 2025
**Status**: Planning Phase - Ready for One-Shot Build

---

## Core Problem Statement
Help people leverage AI to create optimized, **truthful** resumes, especially those who:
- Don't know how to effectively use AI
- Don't identify as "good writers"
- Come from non-dominant cultural backgrounds
- Have English as a second language

---

## Critical New Requirements

### 1. Truth Verification System ⚠️ ESSENTIAL
**The Anti-Fabrication Feature**

**Problem**: We don't want to create an app that helps people lie to get jobs.

**Solution**: Built-in fact-checking workflow

**Implementation**:
```
User completes conversational input
  ↓
AI generates resume draft
  ↓
"Truth Serum" Analysis Phase
  ↓
System identifies items worthy of verification
  ↓
User reviews flagged items
  ↓
User confirms/corrects each flagged item
  ↓
Final resume generation
```

**What Gets Flagged**:
- Dates that don't align (gaps, overlaps)
- Claims without supporting evidence from conversation
- Exaggerated language detected by AI
- Quantitative claims not mentioned in conversation
- Skills listed but not demonstrated
- Education/certifications not explicitly stated
- Company names/titles that seem inconsistent

**User Experience**:
```
🚦 TRUTH CHECK: Let's verify some details

The following items need your review:

1. "Increased revenue by 150%"
   ⚠️ You mentioned growth but didn't specify 150%
   → Confirm this number or adjust

2. "Managed team of 25"
   ⚠️ You said "large team" but didn't mention size
   → What was the actual team size?

3. "Expert in Python, Java, C++"
   ⚠️ You only discussed Python experience
   → Remove unmentioned languages or add context
```

**Philosophy**:
- Not accusatory ("You're lying!")
- Editorial/fact-checking frame ("Let's double-check accuracy")
- Empowering users to ensure AI didn't hallucinate
- Every claim should trace back to conversation

---

### 2. Personal Knowledge Database
**Persistent User Data Store**

**Concept**: Each user has their own evolving database of information

**What Gets Stored**:
- All conversation transcripts
- Key accomplishments extracted
- Skills mentioned
- Work history details
- Projects discussed
- Metrics and quantifiable results
- Stories and anecdotes
- Cover letter content
- Interview prep responses

**Benefits**:
- User returns a year later → System already knows them
- Build resume for new role → Pull from existing knowledge base
- Generate multiple resumes → Same data, different emphasis
- Cover letters → Draw from same stories
- Interview prep → Reference same accomplishments

**Database Structure**:
```
user_knowledge_base:
- user_id
- accomplishments (array of objects)
- skills (array with proficiency levels)
- work_experiences (detailed objects)
- stories (indexed by theme/skill)
- metrics (quantifiable results)
- certifications
- education
- projects
- created_at
- last_updated
```

**Key Feature**: Knowledge accumulates over time
- First visit: Extensive conversation
- Return visit: "Last time you mentioned X, still relevant?"
- Continuous refinement of personal data

---

### 3. Smart Import from ChatGPT/Claude
**AI Conversation Parser**

**Problem**: User might have already done resume work with ChatGPT or Claude

**Solution**: Import existing AI conversation data

**How It Works**:
```
User pastes conversation transcript or text
  ↓
Smart AI parsing extracts:
  - Accomplishments mentioned
  - Skills discussed
  - Work experience details
  - Quantifiable results
  - Stories/anecdotes
  ↓
System adds to user's knowledge base
  ↓
"We found 12 accomplishments, 8 skills, and 3 detailed stories. Ready to build?"
```

**What Gets Parsed**:
- User responses (not AI responses)
- Claims about experience
- Mentioned skills and tools
- Quantitative data
- Company names and roles
- Time periods
- Projects described

**Smart Parsing Features**:
- Detect duplicate information
- Consolidate similar accomplishments
- Flag contradictions
- Structure unstructured conversation data

**Example**:
```
Input (from ChatGPT convo):
"I worked at TechCorp for 3 years as a product manager.
I led a team that increased user engagement by 40% and
reduced churn. We used Mixpanel and ran A/B tests..."

Parsed Output:
✅ Company: TechCorp
✅ Role: Product Manager
✅ Duration: 3 years
✅ Accomplishment: Increased user engagement 40%
✅ Accomplishment: Reduced churn (specific % not mentioned - FLAG)
✅ Skill: Mixpanel
✅ Skill: A/B testing
✅ Leadership: Managed team (size unknown - FLAG)
```

---

### 4. Multi-Language Support
**Translation Mode for Non-English Speakers**

**Feature**: Questions can be displayed/asked in user's native language

**Workflow**:
```
User selects language: Spanish, Vietnamese, Mandarin, etc.
  ↓
System asks questions in that language
  ↓
User responds in native language (voice or text)
  ↓
System captures responses
  ↓
User clicks "Translate to English"
  ↓
AI translates responses maintaining meaning/context
  ↓
Resume generated in professional English
```

**Supported Languages (MVP)**:
- Spanish
- Vietnamese
- Mandarin
- Tagalog
- Arabic
- French
- (Expandable)

**Key Feature**: Not just word-for-word translation
- Cultural context preservation
- Professional tone adjustment
- Idiom translation
- Maintains authenticity of story

**Example**:
```
Question (Spanish):
"Cuéntame sobre un momento en el que superaste las expectativas"

User Response (Spanish):
"En mi trabajo anterior, implementé un nuevo sistema..."

Translation to English (Professional):
"In my previous role, I implemented a new system that exceeded
quarterly targets by 35%, demonstrating initiative and technical
expertise valued by leadership."
```

---

## Refined Product Overview

**Type**: Web application (MVP)
**UX Model**: Conversational AI (ChatGPT-style voice interaction)
**Core Values**: Truth, Inclusivity, Accessibility, Intelligence

**Core Flow**:
```
1. Account Creation
2. Language Selection (optional)
3. Import Existing Work (optional - ChatGPT paste)
4. Conversational Discovery (voice/text)
5. Resume Generation
6. TRUTH CHECK ⚠️ (fact verification)
7. User corrections/confirmations
8. Job Targeting & ATS Optimization
9. Visual Editor & Format Optimization
10. Export (PDF/DOCX/TXT)
```

---

## User Journey (Refined)

### 1. Onboarding
- Create account
- Choose language preference
- Optional: Upload existing resumes (OCR)
- Optional: Paste ChatGPT/Claude conversation (smart import)

### 2. Discovery Phase (Storyworth-Style Conversation)
**Questions in user's chosen language**

Categories:
- Professional identity
- Accomplishments & results
- Skills & expertise
- Growth & challenges
- Experience details
- Metrics & quantifiable data
- Stories & anecdotes

**Input Methods**:
- Voice (primary - more authentic)
- Text (fallback)
- Both stored in knowledge base

### 3. AI Resume Generation
- System compiles conversation data
- Generates initial draft
- Identifies best accomplishments per role
- Structures content per best practices

### 4. **TRUTH VERIFICATION ⚠️ NEW**
**Critical Phase - Cannot Skip**

- AI analyzes draft vs. conversation
- Flags unsupported claims
- Presents verification checklist to user
- User reviews each flagged item
- User confirms, corrects, or removes
- System regenerates with verified data only

### 5. Job Targeting
- User specifies target job posting
- System extracts job description
- Identifies ATS system used
- Customizes resume format/keywords for ATS

### 6. Visual Editor
- Real-time resume preview
- Smart formatting with typography awareness
- Character-per-line optimization
- Margin/font size controls
- Section reordering

### 7. Export
- PDF (primary)
- DOCX (ATS-optimized)
- Plain text
- Save to knowledge base for future use

---

## Technical Stack (Confirmed)

### Frontend
- **Framework**: Next.js ✅
- **Voice Interface**: Web Speech API (can upgrade to paid later)
- **UI**: React components

### Backend
- **Language**: Python (FastAPI)
- **AI/LLM**: Claude (Anthropic) ✅
- **OCR**: Gemini (from Car Talker) ✅

### Database
- **Primary**: Supabase (auth, storage, data)
- **Structure**: See updated schema below

### Document Generation
- **PDF**: WeasyPrint (HTML/CSS to PDF) ✅
- **DOCX**: python-docx ✅

### Hosting
- **Frontend**: Vercel ✅
- **Backend**: Railway ✅
- **Storage**: Supabase Storage ✅

---

## Updated Database Schema

### New Tables for Truth Check & Knowledge Base

```sql
-- user_knowledge_base (NEW - persistent personal data)
- id (UUID)
- user_id (FK)
- knowledge_type (enum: accomplishment, skill, experience, story, metric, certification, education, project)
- content (JSONB - flexible structure)
- source (enum: conversation, upload, import, manual)
- verified (boolean - passed truth check)
- created_at
- last_referenced (timestamp)
- confidence_score (float - AI confidence in claim)

-- truth_check_flags (NEW - verification system)
- id (UUID)
- resume_version_id (FK)
- user_id (FK)
- flagged_item (text - the claim being questioned)
- flag_reason (text - why it was flagged)
- supporting_evidence (JSONB - references to conversation)
- user_action (enum: confirmed, corrected, removed, pending)
- original_value (text)
- corrected_value (text)
- created_at
- resolved_at

-- conversation_imports (NEW - ChatGPT paste feature)
- id (UUID)
- user_id (FK)
- import_source (enum: chatgpt, claude, raw_text)
- raw_text (text - original paste)
- parsed_data (JSONB - extracted information)
- items_extracted (int)
- import_date
- processed (boolean)

-- user_translations (NEW - multi-language support)
- id (UUID)
- user_id (FK)
- original_language (text)
- original_text (text)
- translated_text (text)
- translation_date
- quality_score (float)
```

---

## Key Differentiators (Updated)

1. **Truth Verification** 🆕 - Only resume app with built-in fact-checking
2. **Persistent Knowledge Base** 🆕 - Returns get easier over time
3. **Smart Import** 🆕 - Don't start from scratch if you've already done AI work
4. **Multi-Language** 🆕 - Native language input → Professional English output
5. **Storyworth Model** - Deep narrative elicitation vs. form-filling
6. **Voice-First** - Authentic responses through conversation
7. **ATS Intelligence** - Database of ATS requirements
8. **Smart Formatting** - Typography-aware text optimization
9. **Cultural Inclusivity** - Designed for non-traditional backgrounds

---

## Success Metrics (MVP)

**Must Work**:
- ✅ User completes full conversation flow
- ✅ Truth verification flags at least 3 items per resume
- ✅ User can confirm/correct flagged items
- ✅ Knowledge base persists across sessions
- ✅ ChatGPT import extracts key data accurately
- ✅ Multi-language translation maintains meaning
- ✅ System generates ATS-optimized resume
- ✅ Export works in all 3 formats (PDF/DOCX/TXT)
- ✅ Resume formatting is clean and professional
- ✅ Voice input works smoothly

**North Star**:
- Users feel confident their resume is truthful AND competitive
- Non-native English speakers can participate fully
- Return users save 80% of time vs. first-time users

---

## Existing Assets to Integrate

### Car Talker OCR
- **Location**: `/Users/evanstoudt/Documents/File Cabinet/Coding/cartalker`
- **Files**: `test-gemini-ocr.js`, `test-gemini-contract.js`
- **Technology**: Gemini 2.0 Flash (Google)
- **Capability**: Extract text from JPG/PDF receipts
- **Gemini API Key**: Available in code
- **Adaptation Needed**:
  - Change prompt from "receipt" to "resume"
  - Extract: Contact info, work history, skills, education
  - Return structured JSON

### Job Hunt System Resume Logic
- **Location**: `/Users/evanstoudt/Documents/File Cabinet/Coding/job_hunt_system`
- **Key Files**:
  - `ATS_Resume_Optimization_Guide_2025.md` (2,350 lines of ATS research!)
  - `parse_resumes.py` (existing Python resume parser)
  - 69 parsed resume examples in `/context_parsed`
- **Gold Mine**: Comprehensive ATS guide covers:
  - All major ATS platforms (Workday, iCIMS, Greenhouse, Lever, Taleo)
  - Formatting best practices
  - Keyword optimization strategies
  - Platform-specific quirks
  - 2025 AI-powered screening trends

---

## Monetization (Updated)

**MVP**: Free during beta
**Post-Beta**: Flat fee model
- $10-20 one-time payment per hiring season
- No monthly subscription
- No recurring fees
- "Less than a meal out"
- Flat pricing (we eat the tax)
- Return after 3 years? Same low flat fee

**Philosophy**: Getting a job is hard enough - don't make the tool expensive

---

## Ready for One-Shot Build?

**Pre-Build Checklist** (from DECISIONS_NEEDED_FILLED.md):
- ✅ Frontend: Next.js
- ✅ Voice: Web Speech API (start free, can upgrade)
- ✅ LLM: Claude
- ✅ PDF: WeasyPrint (best quality)
- ✅ DOCX: python-docx
- ✅ ATS Research: Use existing comprehensive guide + AI agents for updates
- ✅ Question Bank: Adapt existing + LLM generation + manual curation
- ✅ Car Talker Location: Identified
- ✅ Resume Logic Location: Identified (goldmine!)
- ✅ Hosting: Vercel + Railway + Supabase
- ✅ MVP Scope: Defined with P0 features
- ⚠️ Domain: TBD (resumaker.ai is taken - brainstorm alternatives)

**New Requirements Added**:
- ✅ Truth verification system designed
- ✅ Knowledge base architecture defined
- ✅ ChatGPT import parser specified
- ✅ Multi-language translation flow defined

---

**Status**: Planning Complete ✅
**Next Step**: Final build prompt creation → Execute one-shot build

**Vision Owner**: Evan Stoudt
**Build Date**: TBD (when Supabase project + API keys ready)
