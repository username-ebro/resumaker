# Resumaker - Project Vision

## Core Problem Statement
Help people leverage AI to create optimized resumes, especially those who:
- Don't know how to effectively use AI
- Don't identify as "good writers"
- Come from non-dominant cultural backgrounds
- Have English as a second language

## Key Insight
**Conversational voice input > Text input** for authentic, detailed responses

## Product Overview
**Type**: Web application (MVP)
**UX Model**: Conversational AI (ChatGPT-style voice interaction)
**Core Flow**: Account → Voice/Text Questions → Resume Curation → Output

---

## User Journey

### 1. Onboarding
- Create account
- Upload existing resumes (optional)
- OCR extraction from uploaded documents

### 2. Discovery Phase (Conversational)
- Series of guided questions via voice/text
- Questions based on:
  - Interview prep questions
  - Resume building frameworks
  - Story elicitation (Storyworth-style)

**Question Categories**:
- Accomplishments & results
- Areas of growth
- Proud moments
- Specific data/metrics
- Work experiences
- Skills & competencies

### 3. Job Targeting
- User specifies target job posting
- System extracts job description text
- System identifies ATS (Applicant Tracking System) used
- Customizes resume format/content for specific ATS

### 4. Resume Generation
- AI curates "perfect resume" from conversation data
- Real-time visual editor (GUI)
- Smart formatting with margin/font awareness
- Character/word count optimization per line
- Multiple output formats: PDF, DOCX, TXT

---

## Technical Features

### Core Capabilities
1. **Voice & Text Input**: Conversational interface
2. **OCR Processing**: Extract content from uploaded resumes
3. **ATS Database**: Research/store ATS systems and their requirements
4. **Smart Formatting Engine**:
   - Margin awareness (e.g., 0.25")
   - Font size calculations (e.g., 11pt)
   - Character-per-line optimization
   - Prevent awkward short lines when space available
5. **Multi-format Export**: PDF, DOCX, plain text
6. **Real-time Editor**: Visual resume builder with live preview

### Advanced Features
- ATS-specific optimization (Workday, Greenhouse, Lever, etc.)
- Company research integration
- Cover letter generation from same conversation data
- Resume variation management (different jobs → different resumes)

---

## Technical Stack (Proposed)

### Backend
- **Python**: Core business logic
- **Supabase**: Database, auth, storage
- **AI/LLM**: Resume generation, conversation management
- **OCR**: Document text extraction (existing Gemini integration from Car Talker project)

### Frontend
- **Web Framework**: TBD (React/Next.js/Svelte?)
- **Voice Interface**: Web Speech API or similar
- **PDF Generation**: ReportLab/WeasyPrint
- **DOCX Generation**: python-docx

### Data Architecture
- User profiles & auth
- Conversation transcripts
- Resume versions
- ATS database
- Job posting data
- User artifacts (uploaded resumes, generated resumes)

---

## Key Differentiators

1. **Storyworth Model**: Deep narrative elicitation vs. form-filling
2. **Voice-First**: Authentic responses through conversation
3. **ATS Intelligence**: Database of ATS requirements
4. **Smart Formatting**: Typography-aware text optimization
5. **Cultural Inclusivity**: Designed for non-traditional backgrounds

---

## Success Metrics (MVP)
- User can complete full conversation flow
- System generates ATS-optimized resume
- Export works in all 3 formats (PDF/DOCX/TXT)
- Resume formatting is clean and professional
- Voice input works smoothly

---

## Existing Assets to Integrate
- **Car Talker**: Gemini OCR implementation
- **Resume Logic**: (location TBD - to be migrated)

---

**Vision Date**: October 6, 2025
**Status**: Planning Phase - Do NOT build yet
**Goal**: Create comprehensive build prompt for one-shot implementation
