# Resumaker - MVP Scope (Final Decision)

**Date**: October 6, 2025
**Status**: Final scope locked for one-shot build

---

## Decisions Made

### ✅ Confirmed IN SCOPE (P0 - Must Build)

1. **User Authentication** (Supabase Auth)
   - Login/signup
   - Session management
   - Protected routes

2. **Conversation System** (Voice + Text)
   - Text input (primary for MVP)
   - Voice recording (Web Speech API)
   - Question bank (30-45 questions, English only)
   - Response storage
   - Progress tracking

3. **OCR Upload** (Gemini from Car Talker)
   - Upload existing resume (PDF/DOCX)
   - Extract text using Gemini
   - Parse into structured data
   - Store in knowledge base

4. **Import ChatGPT/Claude Conversations** ⭐ HIGH PRIORITY
   - Paste raw conversation text
   - Smart parsing to extract:
     - Accomplishments
     - Skills
     - Metrics
     - Stories
   - Add to knowledge base
   - **Rationale**: This is the foundation - lets users who've already done AI work import it

5. **Knowledge Base** (Persistent Personal Data)
   - Store all user data permanently
   - Categories: accomplishments, skills, experience, stories, metrics
   - Source tracking (conversation, upload, import, reference)
   - Confidence scores
   - Verification status

6. **Truth Verification System** ⭐ CORE DIFFERENTIATOR
   - Analyze resume vs. knowledge base
   - Flag unsupported claims
   - Present for user review
   - User confirms/corrects/removes
   - Regenerate with verified data only
   - Conservative flagging (high confidence only)

7. **Resume Generation**
   - Compile knowledge base data
   - Apply ATS best practices
   - Use formatting rules from ATS guide
   - Generate structured resume content (JSONB)

8. **Job Targeting & ATS Optimization**
   - Job description input
   - Keyword extraction
   - ATS system detection
   - Keyword match scoring
   - Platform-specific optimization

9. **PDF Export** (WeasyPrint)
   - Convert resume to professional PDF
   - Clean formatting
   - ATS-friendly layout
   - Download link

10. **DOCX Export** (python-docx)
    - Generate Word document
    - Standard formatting (no tables/columns)
    - ATS-optimized
    - Download link

11. **Basic Visual Editor**
    - Live preview of resume
    - Section-by-section text editing
    - No drag-and-drop (too complex for MVP)
    - Simple formatting controls (font, margins)

12. **Reference Input System** ⭐ NEW PRIORITY FEATURE
    - Generate shareable prompt for colleagues/managers
    - Copy-paste message template
    - Public form link (no login required)
    - Parse reference responses
    - Extract validated accomplishments/skills
    - Add to knowledge base with high confidence
    - **Rationale**: Adds external validation, enriches knowledge base

---

### ❌ Confirmed OUT OF SCOPE (Post-MVP)

1. **Multi-Language Support**
   - Translation of questions
   - Native language input → English output
   - **Defer to**: v1.1 (after MVP validation)
   - **Rationale**: Complex, not blocking, English-only MVP is sufficient

2. **Advanced Visual Editor**
   - Drag-and-drop section reordering
   - WYSIWYG editing
   - **Defer to**: v1.2
   - **Rationale**: Too time-consuming, basic editor is sufficient

3. **Cover Letter Generation**
   - **Defer to**: v1.1
   - **Rationale**: Resume is core, cover letters are secondary

4. **Multiple Resume Versions Management**
   - Version comparison
   - Resume templates
   - **Defer to**: v1.1
   - **Rationale**: Can build one good resume first, versioning later

5. **Interview Prep / Job Tracking**
   - **Defer to**: v2.0+
   - **Rationale**: Outside core resume scope

6. **Mobile App**
   - **Defer to**: v2.0+
   - **Rationale**: Web-responsive is sufficient for MVP

---

## Build Priority Order

### Phase 1: Foundation (8-10 hours)
1. Project setup (backend + frontend)
2. Supabase integration
3. Authentication (login/signup)
4. Database migrations (all tables)
5. Environment configuration

### Phase 2: Data Collection (18-22 hours)
6. **Import Parser** ⭐ (ChatGPT/Claude conversations)
   - Paste interface
   - Claude-powered parsing
   - Knowledge base storage
   - **Why First**: Foundation for getting data into system

7. **OCR Service** (Upload existing resumes)
   - File upload handling
   - Gemini OCR integration
   - Structured extraction
   - Knowledge base storage

8. **Conversation System**
   - Question bank (30-45 questions)
   - Text input/output
   - Voice recording (Web Speech API)
   - Response storage

9. **Reference Input System** ⭐
   - Generate shareable prompts
   - Public reference form
   - Parse responses
   - Add to knowledge base

10. **Knowledge Base UI**
    - View all stored data
    - Search/filter
    - Edit/delete items
    - See confidence scores

### Phase 3: Resume Generation (12-15 hours)
11. **Resume Generator**
    - Compile knowledge base data
    - Apply ATS optimization rules
    - Use formatting engine
    - Generate structured content

12. **Job Targeting**
    - Job description input
    - Keyword extraction
    - ATS system detection
    - Keyword match scoring

13. **Truth Verification** ⭐
    - Compare resume vs. knowledge base
    - Flag unsupported claims
    - User review interface
    - Corrections/confirmations
    - Regenerate

### Phase 4: Output (10-12 hours)
14. **Visual Editor**
    - Live preview
    - Section editing
    - Basic formatting controls

15. **PDF Export** (WeasyPrint)
    - HTML template → PDF
    - Professional formatting
    - Download

16. **DOCX Export** (python-docx)
    - Structured content → Word
    - ATS-friendly formatting
    - Download

### Phase 5: Polish & Deploy (6-8 hours)
17. Testing (unit + integration)
18. Deployment (Vercel + Railway)
19. Documentation
20. Bug fixes

---

## Revised Time Estimate

| Phase | Components | Hours |
|-------|-----------|--------|
| P1: Foundation | Setup, auth, DB | 8-10 |
| P2: Data Collection | Import parser, OCR, conversation, references, KB UI | 18-22 |
| P3: Resume Gen | Generator, job targeting, truth check | 12-15 |
| P4: Output | Editor, PDF, DOCX | 10-12 |
| P5: Deploy | Testing, deployment, docs | 6-8 |
| **TOTAL** | | **54-67 hours** |

**Realistic One-Shot Build**: 55-60 hours

---

## Feature Comparison (Before vs. After New Feature)

### Original MVP Scope:
- Conversation → Resume → Export
- Truth check for accuracy
- Knowledge base for persistence
- Import ChatGPT conversations

### Enhanced MVP Scope (with References):
- **Conversation** → Resume → Export
- **Upload existing resume** → Parse → Add to knowledge base
- **Import ChatGPT/Claude** → Parse → Add to knowledge base
- **Request references** → Parse responses → Add to knowledge base (validated!)
- Truth check (now has more data sources to validate against)
- Knowledge base (richer, includes external validation)

**Key Insight**: References transform the knowledge base from "self-reported" to "validated by others"

---

## Data Flow Architecture

```
USER DATA COLLECTION (Multiple Sources):

1. Conversation (Voice/Text)
   ↓
   Extract accomplishments, skills, stories
   ↓
   Store in knowledge_base (source: conversation, confidence: 0.5-0.7)

2. Upload Resume (OCR)
   ↓
   Parse existing resume text
   ↓
   Store in knowledge_base (source: upload, confidence: 0.6)

3. Import ChatGPT/Claude
   ↓
   Parse conversation for key data
   ↓
   Store in knowledge_base (source: import, confidence: 0.6-0.8)

4. Reference Input ⭐
   ↓
   Parse reference responses
   ↓
   Store in knowledge_base (source: reference, confidence: 0.9, verified: true)

                    ↓
              KNOWLEDGE BASE
         (All data consolidated)
                    ↓
              RESUME GENERATION
         (Pull from knowledge base)
                    ↓
              TRUTH VERIFICATION
      (Cross-check claims vs. knowledge base)
                    ↓
         USER CONFIRMS/CORRECTS
                    ↓
              FINAL RESUME
          (PDF/DOCX Export)
```

**Power of Multiple Sources**:
- Self-reported (conversation): Medium confidence
- Uploaded resume: Medium confidence
- ChatGPT import: Medium-high confidence
- **References**: HIGH confidence (validated by third party!)

**Truth Check Benefits**:
- Can cite reference validation: "Validated by former manager"
- Higher confidence claims get priority in resume
- Reference data = strong evidence against flags

---

## Success Metrics (MVP)

### Technical Success:
- [ ] All P1-P4 features working
- [ ] Truth check flags 3-10 items per resume (calibrated)
- [ ] Import parser extracts data with 80%+ accuracy
- [ ] Reference parser extracts key points with 85%+ accuracy
- [ ] OCR works on standard resume formats (90%+ accuracy)
- [ ] PDF/DOCX exports are ATS-friendly
- [ ] Knowledge base persists across sessions (100%)

### User Success:
- [ ] User can complete full flow in 30-45 minutes
- [ ] Truth check feels helpful (not punishing)
- [ ] Reference feature gets used (at least 1 reference requested)
- [ ] Users incorporate reference data into resume
- [ ] Final resume feels truthful AND competitive

### Product Validation:
- [ ] 5-10 beta users complete full flow
- [ ] Positive feedback on truth verification UX
- [ ] Reference response rate > 50%
- [ ] Users return to build second resume (knowledge base value)

---

## API Keys & Credentials (Ready)

✅ **Claude API Key**: `sk-ant-api03-QFviv...` (confirmed)
✅ **Gemini API Key**: `AIzaSyDc9...` (confirmed)
✅ **Supabase Project**: `nkfrqysxrwfqqzpsjtlh` (confirmed)
✅ **Supabase Keys**: Publishable + Secret (confirmed)

⚠️ **Missing**: Supabase database password (for direct connection string)
- Can use MCP integration or get password from Supabase dashboard

---

## Questions Resolved

### Q: Import parser vs. multi-language - which is more important?
**A**: Import parser. It's the foundation for getting data into the system quickly.

### Q: Is reference feature worth the complexity?
**A**: Yes. It's a differentiator and solves the "truth verification" problem by adding external validation.

### Q: Multi-language in MVP?
**A**: No. Defer to v1.1. English-only MVP is sufficient for validation.

### Q: Full visual editor or basic?
**A**: Basic. Preview + section editing is enough. Drag-and-drop can wait.

### Q: Truth check aggressiveness?
**A**: Conservative. Only flag high-confidence issues. Better to miss a few than overwhelm users.

---

## Build Sequence (Final)

**Day 1** (10 hours):
- [ ] Project setup (backend + frontend)
- [ ] Supabase integration + migrations
- [ ] Authentication flows
- [ ] Basic UI structure

**Day 2** (10 hours):
- [ ] Import parser (ChatGPT/Claude)
- [ ] OCR service (Gemini)
- [ ] Knowledge base CRUD

**Day 3** (10 hours):
- [ ] Conversation system (text + voice)
- [ ] Reference request generation
- [ ] Reference response form (public)

**Day 4** (10 hours):
- [ ] Resume generator
- [ ] Job targeting + ATS optimization
- [ ] Truth verification system

**Day 5** (10 hours):
- [ ] Visual editor (basic)
- [ ] PDF export (WeasyPrint)
- [ ] DOCX export (python-docx)

**Day 6** (10 hours):
- [ ] Integration testing
- [ ] UI polish
- [ ] Deployment (Vercel + Railway)
- [ ] Documentation

**Total**: 60 hours (spread over 6 focused days or 2-3 weeks part-time)

---

## Ready to Build Checklist

**Before Starting**:
- [x] All credentials obtained
- [x] Scope finalized (this document)
- [x] Database schema designed
- [x] File structure planned
- [x] Algorithms specified
- [x] Success criteria defined
- [ ] Supabase database password (nice-to-have, can use MCP)
- [ ] Final review of BUILD_PLAN_V2.md

**During Build**:
- [ ] Follow phase sequence strictly
- [ ] Test each phase before moving to next
- [ ] Use TodoWrite to track progress
- [ ] Document any deviations from plan

**After Build**:
- [ ] Full integration test
- [ ] Deploy to production
- [ ] Invite 5-10 beta testers
- [ ] Collect feedback
- [ ] Iterate on v1.1

---

**Status**: Planning complete ✅
**Next Step**: Execute one-shot build following this scope
**Owner**: Evan Stoudt
**Builder**: Claude Code

**Let's build something truthful.** 🎯
