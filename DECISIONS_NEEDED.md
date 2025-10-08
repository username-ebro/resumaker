# Decisions Needed Before Build

## Critical Path Items

### 1. Technology Choices

#### Frontend Framework
- [ ] **React** (most popular, huge ecosystem)
- [ ] **Next.js** (React + SSR, API routes, great for this use case)
- [ ] **Svelte/SvelteKit** (lighter, faster, less boilerplate)

**Recommendation**: Next.js (handles both frontend + API routes, good Supabase integration)

---

#### Voice Interface
- [ ] **Web Speech API** (free, browser-native, works offline)
- [ ] **Deepgram** (paid, better accuracy, $0.0043/min)
- [ ] **AssemblyAI** (paid, good features, $0.00025/sec)
- [ ] **OpenAI Whisper API** ($0.006/min)

**Recommendation**: Start with Web Speech API (free MVP), upgrade later

---

#### LLM for Conversations
- [ ] **Claude (Anthropic)** - Better at following instructions, nuanced conversation
- [ ] **GPT-4** - Faster, cheaper, good quality
- [ ] **Both** - Use Claude for resume generation, GPT for conversations

**Recommendation**: Claude for everything (consistency, quality)

---

#### PDF Generation
- [ ] **ReportLab** (Python, powerful, complex)
- [ ] **WeasyPrint** (HTML/CSS to PDF, easier for styling)
- [ ] **Playwright PDF** (render HTML in browser, convert to PDF)

**Recommendation**: WeasyPrint (HTML/CSS is easier to template)

---

#### DOCX Generation
- [ ] **python-docx** (standard library)
- [ ] **docxtpl** (template-based, Jinja2)

**Recommendation**: python-docx (more control)

---

### 2. Data & Content

#### ATS Research Strategy
- [ ] **Manual Research** (slow, accurate, free)
- [ ] **Purchase Dataset** (fast, expensive, may exist)
- [ ] **Scrape Job Boards** (medium effort, legal gray area)
- [ ] **Start with Top 5** (Workday, Greenhouse, Lever, Taleo, iCIMS)

**Recommendation**: Manual research for top 5 systems (MVP scope)

---

#### Question Bank
- [ ] **Write from scratch** (custom, time-consuming)
- [ ] **Adapt existing interview guides** (faster, proven)
- [ ] **Use LLM to generate** (quick, needs curation)

**Recommendation**: Adapt existing + LLM generation + manual curation

---

### 3. Existing Code Integration

#### Car Talker OCR
- [ ] **Location**: Where is this code?
- [ ] **Format**: Python? JavaScript?
- [ ] **Gemini API Key**: Do we have access?
- [ ] **PDF Support**: Does it handle PDFs or just images?

**Action Required**: Point me to Car Talker code location

---

#### Existing Resume Logic
- [ ] **Location**: Where is this?
- [ ] **Language**: Python? JavaScript? Apps Script?
- [ ] **Scope**: What does it do currently?

**Action Required**: Point me to existing resume logic

---

### 4. Deployment & Infrastructure

#### Hosting Strategy
- [ ] **Frontend**: Vercel / Netlify / Cloudflare Pages
- [ ] **Backend**: Railway / Render / Fly.io / AWS Lambda
- [ ] **Database**: Supabase (already decided)
- [ ] **File Storage**: Supabase Storage vs. S3 vs. Cloudflare R2

**Recommendation**:
- Frontend: Vercel (Next.js optimized)
- Backend: Railway (easy Python deployment)
- Storage: Supabase Storage (keeps everything in one place)

---

#### Domain Name
- [ ] resumaker.com (taken, premium price)
- [ ] resumaker.io
- [ ] resumaker.ai
- [ ] getresumaker.com
- [ ] Other: _______________

**Action Required**: Choose domain (can decide later, but good to know)

---

### 5. MVP Scope Decisions

#### Must-Have Features (P0)
- [x] User auth (Supabase)
- [x] Text-based conversation
- [x] Upload resume (OCR)
- [x] Job posting input
- [x] Resume generation
- [x] PDF export
- [ ] Voice conversation?
- [ ] DOCX export?
- [ ] Visual editor?
- [ ] ATS optimization?

#### Nice-to-Have Features (P1)
- [ ] Voice interface
- [ ] Real-time visual editor
- [ ] Multiple resume versions
- [ ] Cover letter generation
- [ ] ATS database (beyond basic)
- [ ] Company research
- [ ] Mobile app

#### Future Features (P2)
- [ ] LinkedIn integration
- [ ] Resume scoring
- [ ] Interview prep
- [ ] Job application tracking
- [ ] Networking suggestions

**Action Required**: Confirm P0 scope

---

### 6. Security & Privacy

#### Data Retention
- [ ] How long do we keep conversation transcripts?
- [ ] Can users delete their data?
- [ ] Do we anonymize data for training?

#### Privacy Considerations
- [ ] Terms of Service needed?
- [ ] Privacy Policy needed?
- [ ] GDPR compliance? (if EU users)
- [ ] Data encryption at rest?

**Recommendation**: Start simple (delete anytime, no training on user data)

---

### 7. Monetization (Future)

#### Business Model Ideas
- [ ] Free MVP (feedback phase)
- [ ] Freemium (1 resume free, more = paid)
- [ ] Subscription ($9.99/mo unlimited)
- [ ] One-time purchase per resume ($29?)
- [ ] B2B (career coaches, universities)

**MVP**: Free during beta, decide later

---

## Decision Summary Template

**Copy this, fill it out, and paste back to me:**

```
FRONTEND: Next.js / React / Svelte
VOICE: Web Speech API / Deepgram / Whisper
LLM: Claude / GPT-4 / Both
PDF: WeasyPrint / ReportLab / Playwright
DOCX: python-docx / docxtpl

ATS RESEARCH: Top 5 manual / Purchase data / Full research
QUESTION BANK: Adapt existing / Write from scratch / LLM-generated

CAR TALKER LOCATION: [path to code]
RESUME LOGIC LOCATION: [path to code]

HOSTING:
- Frontend: Vercel / Netlify / Other
- Backend: Railway / Render / Other
- Storage: Supabase / S3 / R2

MVP SCOPE (P0 only):
- Auth: YES
- Text conversation: YES
- Voice conversation: YES / NO
- Upload + OCR: YES
- Job posting input: YES
- Resume generation: YES
- PDF export: YES
- DOCX export: YES / NO
- Visual editor: YES / NO / BASIC
- ATS optimization: YES / NO / BASIC

DOMAIN: [name] or "decide later"
```

---

**Next Steps After Decisions:**
1. Create comprehensive build prompt
2. Set up Supabase project
3. Get all API keys
4. Migrate existing code
5. Execute one-shot build

**Ready when you are!**
