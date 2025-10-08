# Resumaker - Executive Summary

**Date**: October 6, 2025
**Status**: Planning Complete → Ready for Build

---

## What We're Building

**Resumaker** is a conversational AI-powered resume builder that helps job seekers—especially those who don't consider themselves "good writers" or come from non-dominant cultural backgrounds—create truthful, ATS-optimized resumes through natural voice/text conversations.

---

## Core Differentiators

### 1. **Truth Verification System** 🆕
- Built-in fact-checking to prevent AI hallucination
- Flags unsupported claims for user review
- Editorial approach (not accusatory)
- **Philosophy**: Help people tell their truth better, not help them lie

### 2. **Persistent Knowledge Base** 🆕
- User's accomplishments/skills stored permanently
- Return a year later → System remembers you
- Build multiple resumes from same knowledge base
- Knowledge accumulates and improves over time

### 3. **Smart Import from ChatGPT/Claude** 🆕
- Paste existing AI conversations
- Intelligent parsing extracts accomplishments, skills, stories
- Don't start from scratch if you've already done the work elsewhere

### 4. **Multi-Language Support** 🆕
- Ask questions in Spanish, Vietnamese, Mandarin, etc.
- User responds in native language
- AI translates to professional English
- Preserves cultural context and authenticity

### 5. **Storyworth-Style Conversation**
- Deep narrative elicitation (not forms)
- Voice-first for authentic responses
- Follow-up questions based on responses

### 6. **Comprehensive ATS Intelligence**
- Built from 2,350-line ATS Optimization Guide
- Platform-specific rules (Workday, Greenhouse, Lever, etc.)
- Smart formatting aware of typography constraints
- Keyword optimization without stuffing

---

## Tech Stack (Confirmed)

| Component | Technology | Why |
|-----------|-----------|-----|
| **Frontend** | Next.js | SSR, API routes, Supabase integration |
| **Backend** | Python (FastAPI) | Fast, async, great for AI integration |
| **Database** | Supabase | Auth, storage, Postgres, real-time |
| **AI/LLM** | Claude (Anthropic) | Best at instruction-following, nuanced conversation |
| **OCR** | Gemini (Google) | Proven in Car Talker project |
| **Voice** | Web Speech API | Free, browser-native, can upgrade later |
| **PDF Export** | WeasyPrint | HTML/CSS to PDF, best quality |
| **DOCX Export** | python-docx | Standard library, full control |
| **Hosting** | Vercel (frontend), Railway (backend) | Easy deployment, great DX |

---

## Scope: MVP (P0) Features

### Must-Have for First Release:
✅ User authentication (Supabase Auth)
✅ Text + Voice conversation system
✅ Upload existing resume (OCR with Gemini)
✅ **Truth verification system** (NEW - core differentiator)
✅ **Persistent knowledge base** (NEW - user data store)
✅ **Import ChatGPT/Claude conversations** (NEW - smart parser)
✅ **Multi-language support** (NEW - 3-5 languages)
✅ Job posting input & keyword extraction
✅ Resume generation with ATS optimization
✅ PDF + DOCX export
✅ Basic visual editor

### Nice-to-Have (Post-MVP):
- Advanced visual editor with drag-and-drop
- Cover letter generation
- Multiple resume versions management
- Resume scoring & feedback
- Company research integration

---

## Key Innovations

### Truth Check Workflow
```
User completes conversation
  ↓
AI generates resume draft
  ↓
Truth Serum Analysis
  ↓
System flags 3-10 items for verification:
  • "You mentioned growth but didn't specify 150% - confirm?"
  • "You discussed Python but not C++ - remove or add context?"
  • "Team size not mentioned - what was actual size?"
  ↓
User confirms/corrects each flag
  ↓
Final resume generated with verified data only
```

**Why This Matters**:
- Prevents users from accidentally lying
- Builds confidence in resume accuracy
- Differentiates from "just make it sound good" AI tools
- Ethical AI in action

### Knowledge Base Architecture
```
First Visit (New User):
- Extensive 30-45 min conversation
- Extract 20-40 knowledge items
- Store: accomplishments, skills, stories, metrics

Return Visit (1 year later):
- "Last time you mentioned leading a team of 15 - still relevant?"
- "You had 3 years at TechCorp - any updates?"
- Build new resume in 10-15 minutes using existing knowledge
- Add only new accomplishments since last visit

Benefits:
- Faster resume generation on return
- Consistent data across multiple resumes
- Historical record of career progression
- Cover letters pull from same knowledge base
```

### Smart Import Parser
```
User: [Pastes entire ChatGPT conversation about resume]

System analyzes conversation:
- Detects 15 accomplishments mentioned
- Extracts 8 skills discussed
- Identifies 3 detailed stories
- Finds 12 quantitative metrics
- Notes 2 certifications

System: "I found all this information. Ready to build your resume?"

User: "Yes!"

System: [Generates resume in 2 minutes using imported data]
```

---

## Existing Assets to Leverage

### 1. Car Talker OCR (Gemini)
- **Location**: `/cartalker/test-gemini-ocr.js`
- **Current Use**: Extract data from automotive receipts
- **Adaptation**: Change prompt to parse resumes instead
- **Tech**: Gemini 2.0 Flash (Google)
- **Status**: Working code, ready to migrate

### 2. ATS Optimization Guide
- **Location**: `/job_hunt_system/ATS_Resume_Optimization_Guide_2025.md`
- **Size**: 2,350 lines of comprehensive research
- **Content**:
  - All major ATS platforms analyzed
  - Formatting best practices
  - Keyword optimization strategies
  - Platform-specific quirks (Workday, Greenhouse, Lever, Taleo, iCIMS)
  - 2025 AI-powered screening trends
- **Status**: Ready to integrate into backend logic

### 3. Resume Parser
- **Location**: `/job_hunt_system/parse_resumes.py`
- **Current Use**: Parse .docx resumes to plain text
- **Adaptation**: Can be used for uploaded resume processing
- **Status**: Working Python code

### 4. Sample Resume Database
- **Location**: `/job_hunt_system/context_parsed/` (69 files)
- **Content**: Real resume examples (parsed text)
- **Use**: Testing, training data, examples
- **Status**: Available for reference

---

## Monetization Strategy

**MVP**: Free during beta (gather feedback)

**Post-Beta**: Flat fee model
- $10-20 one-time payment per hiring season
- No monthly subscription
- No recurring fees
- Return after 3 years? Same low flat fee
- "Less than a meal out" positioning
- We eat the transaction fees (true flat pricing)

**Philosophy**: Getting a job is hard enough - don't make the tool a barrier

---

## Build Timeline

| Phase | Description | Est. Hours |
|-------|-------------|------------|
| **P0: Foundation** | Setup backend, frontend, auth | 8-10 |
| **P1: Core MVP** | OCR, conversation, voice, knowledge extraction | 15-18 |
| **P2: New Features** | Truth check, import parser, multi-language | 12-15 |
| **P3: Resume Generation** | Generator, ATS optimization, formatting engine | 10-12 |
| **P4: Export & Editor** | PDF, DOCX, visual editor | 8-10 |
| **P5: Testing & Deploy** | Testing, deployment, configuration | 4-6 |
| **TOTAL** | | **57-71 hours** |

**Realistic Estimate**: 50-60 hours for streamlined MVP (one-shot build)

---

## Risk Mitigation

### Technical Risks:
1. **OCR accuracy on varied resume formats**
   - Mitigation: Test with 69 sample resumes, iteratively improve prompts

2. **Translation quality for non-English input**
   - Mitigation: Claude is strong at translation, add quality scores, allow human review

3. **Truth checker false positives (flagging valid claims)**
   - Mitigation: Conservative flagging (only flag when confidence < 0.5), user can override

4. **Voice recognition accuracy across accents**
   - Mitigation: Start with Web Speech API, upgrade to Deepgram/Whisper if needed

### Product Risks:
1. **Users feel interrogated by truth check**
   - Mitigation: Frame as "editorial fact-check", not accusatory, empowering language

2. **Conversation flow feels robotic**
   - Mitigation: Use Claude's conversational abilities, dynamic follow-ups, natural language

3. **Knowledge base becomes cluttered/outdated**
   - Mitigation: Show last-used date, allow archiving, periodic cleanup prompts

---

## Success Criteria (MVP)

### Technical:
- ✅ 95%+ uptime
- ✅ < 2s response time for AI interactions
- ✅ OCR accuracy > 90% on standard resumes
- ✅ PDF generation works on all browsers
- ✅ Voice recording works on Chrome, Safari, Firefox

### Product:
- ✅ 80%+ of users complete full conversation flow
- ✅ Truth check flags 3-10 items per resume (calibrated correctly)
- ✅ 90%+ of flagged items are confirmed/corrected (not all removed = good)
- ✅ Users feel confident in resume truthfulness (qualitative feedback)
- ✅ Knowledge base persists across sessions (100% reliability)
- ✅ Import parser extracts key data with 85%+ accuracy

### User Satisfaction:
- ✅ "This helped me tell my story better" (qualitative feedback)
- ✅ "I feel confident applying with this resume" (qualitative)
- ✅ NPS > 40 (Net Promoter Score)
- ✅ 30%+ of users return within 3 months (build second resume)

---

## Next Steps

### Before Build:
1. ✅ Planning complete (PROJECT_VISION_V2, BUILD_PLAN_V2)
2. ⏳ Create Supabase project
3. ⏳ Obtain API keys (Claude, Gemini)
4. ⏳ Migrate Car Talker OCR code to new project
5. ⏳ Copy ATS guide to backend/data/
6. ⏳ Draft initial question bank (English)

### Build Execution:
- **Approach**: One-shot build following BUILD_PLAN_V2.md
- **Duration**: 50-60 focused hours
- **Method**: Provide comprehensive prompt with all specifications
- **Checkpoints**: Test after each priority phase (P0, P1, P2, etc.)

### Post-Build:
- Beta testing with 5-10 users
- Collect feedback on truth check UX
- Refine conversation flow
- Add additional languages if needed
- Iterate on translation quality

---

## Questions for Decision

### Before Starting Build:

1. **Language Priority**: Should multi-language support be P0 (must-have for MVP) or P1 (add after core works)?
   - **Recommendation**: P0 - It's a core differentiator, but start with just 1-2 languages (Spanish + English)

2. **Import Parser Priority**: Is ChatGPT/Claude import critical for MVP or nice-to-have?
   - **Recommendation**: P1 - Valuable but not blocking. Users can still do full conversation without it.

3. **Visual Editor Complexity**: Full drag-and-drop editor or simple preview + text edit?
   - **Recommendation**: Simple for MVP - Preview with section-by-section editing, not full WYSIWYG

4. **Truth Check Aggressiveness**: Should we flag conservatively (fewer flags, high confidence) or liberally (more flags, catch everything)?
   - **Recommendation**: Conservative for MVP - Better to miss a few than overwhelm users with false positives

---

## Domain Name Ideas

Since `resumaker.ai` is taken, alternatives:

- `resumetruth.ai` (emphasizes truth-checking)
- `truthfulresume.com`
- `voiceresume.ai` (emphasizes conversational approach)
- `resumemaker.io` (classic, may be available)
- `getresumaker.com` (fallback)
- `resumebuilder.ai` (generic but clear)
- `storyresume.com` (emphasizes Storyworth approach)
- `myresumaker.com`

**Decision**: Can wait until post-MVP, use localhost for development

---

## Conclusion

Resumaker solves a real problem (hard to create competitive resumes, especially for non-traditional candidates) with a unique approach (conversational, truthful, inclusive, persistent).

The technical plan is comprehensive, the assets are available, and the scope is well-defined.

**We're ready to build.** 🚀

---

**Owner**: Evan Stoudt
**Builder**: Claude Code
**Timeline**: TBD (pending API key acquisition)
**Estimated Effort**: 50-60 hours one-shot build

**Let's make job seeking more equitable, one truthful resume at a time.**
