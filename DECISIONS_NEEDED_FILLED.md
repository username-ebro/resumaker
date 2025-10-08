# Decisions Needed Before Build

## Critical Path Items

### 1. Technology Choices

#### Frontend Framework
- [ ] **React** (most popular, huge ecosystem)
- [ ] **Next.js** (React + SSR, API routes, great for this use case)
- [ ] **Svelte/SvelteKit** (lighter, faster, less boilerplate)

**Recommendation**: Next.js (handles both frontend + API routes, good Supabase integration) i approve this. This sounds good, and I trust your judgment on this. So, like, yeah, I think next makes sense, but just know that you're the expert here. 

---

#### Voice Interface
- [ ] **Web Speech API** (free, browser-native, works offline)
- [ ] **Deepgram** (paid, better accuracy, $0.0043/min)
- [ ] **AssemblyAI** (paid, good features, $0.00025/sec)
- [ ] **OpenAI Whisper API** ($0.006/min)

**Recommendation**: Start with Web Speech API (free MVP), upgrade later I like the Web Speech API because it's free. That sounds fine for me. I personally use the Mac Whisper and love it. And that's local for me, and I think that's just free. I don't know if we could use that for now for me for testing, but I want it to be excellent. We want the we want, it's like voice to text is one thing, but we want the AI to understand, right? So like it's going to respond to the person, and we need that to be relatively fluid like ChatGPT does. So I just want to note that free is good, but I'm not worried about the paid method yet. Sorry, I'm not worried that paid is bad. I think that could be good as well. So should be considered. 

---

#### LLM for Conversations
- [ ] **Claude (Anthropic)** - Better at following instructions, nuanced conversation
- [ ] **GPT-4** - Faster, cheaper, good quality
- [ ] **Both** - Use Claude for resume generation, GPT for conversations

**Recommendation**: Claude for everything (consistency, quality)I like Claude. So let's just stick with that. 

---

#### PDF Generation
- [ ] **ReportLab** (Python, powerful, complex)
- [ ] **WeasyPrint** (HTML/CSS to PDF, easier for styling)
- [ ] **Playwright PDF** (render HTML in browser, convert to PDF)

**Recommendation**: WeasyPrint (HTML/CSS is easier to template)I want it to be whatever is the best, because I think that some of the value proposition here is actually like it looks really good and they don't have to do shit with it afterwards 

---

#### DOCX Generation
- [ ] **python-docx** (standard library)
- [ ] **docxtpl** (template-based, Jinja2)

**Recommendation**: python-docx (more control)That sounds good 

---

### 2. Data & Content

#### ATS Research Strategy
- [ ] **Manual Research** (slow, accurate, free)
- [ ] **Purchase Dataset** (fast, expensive, may exist)
- [ ] **Scrape Job Boards** (medium effort, legal gray area)
- [ ] **Start with Top 5** (Workday, Greenhouse, Lever, Taleo, iCIMS)

**Recommendation**: Manual research for top 5 systems (MVP scope)I think that the like best thing here is to set up a couple of agents to do really deep and thorough research. Like look at job posting forums, scrape LinkedIn, scrape API information, scrape, you know, just like there's job headhunters doing research on this stuff and creating advice. So we want to pull that all together. And I don't want to pay for it. And I don't want to do it manually myself. 

---

#### Question Bank
- [ ] **Write from scratch** (custom, time-consuming)
- [ ] **Adapt existing interview guides** (faster, proven)
- [ ] **Use LLM to generate** (quick, needs curation)

**Recommendation**: Adapt existing + LLM generation + manual curation Yeah, I I like this. I'm gonna manually curate it myself at the end, but you sh you should basically like look at interview guides, knowing that we're trying to get as much information about a person to determine their like the best way to portray their candidacy. And then the LLM can probably generate questions that are going to get them really talking. You know, like there's probably better and worse ways to phrase a question. We also probably could do like a translate mode where it displays or asks the questions in Spanish, in Vietnamese, etc., like with a click of a button, creating something that is correct in someone's native language. That we then click a button and change it to English would be really perfect. 

---

### 3. Existing Code Integration

#### Car Talker OCR
- [ ] **Location**: Where is this code?
- [ ] **Format**: Python? JavaScript?
- [ ] **Gemini API Key**: Do we have access?
- [ ] **PDF Support**: Does it handle PDFs or just images?

**Action Required**: Point me to Car Talker code locationI already answered this in that in the window, you'll see that. 

---

#### Existing Resume Logic
- [ ] **Location**: Where is this?
- [ ] **Language**: Python? JavaScript? Apps Script?
- [ ] **Scope**: What does it do currently?

**Action Required**: Point me to existing resume logicI already answered this in the window, you'll see that. 

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
- Storage: Supabase Storage (keeps everything in one place) Whatever sounds best, like I think those recommendations sound good. I trust you. 

---

#### Domain Name
- [ ] resumaker.com (taken, premium price)
- [ ] resumaker.io
- [ ] resumaker.ai
- [ ] getresumaker.com
- [ ] Other: _______________

**Action Required**: Choose domain (can decide later, but good to know) It looks like resinmaker.ai is already um the exact thing that we're building, so maybe we should make it like Resume. I don't know, we'll think of another name. 

---

### 5. MVP Scope Decisions

#### Must-Have Features (P0)
- [x] User auth (Supabase)
- [x] Text-based conversation
- [x] Upload resume (OCR)
- [x] Job posting input
- [x] Resume generation
- [x] PDF export
- [X] Voice conversation?
- [ ] DOCX export?
- [X] Visual editor?
- [ ] ATS optimization?

#### Nice-to-Have Features (P1)
- [X] Voice interface
- [X] Real-time visual editor
- [X] Multiple resume versions
- [X] Cover letter generation
- [X] ATS database (beyond basic)
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
- [ ] Can users delete their data? Yes 
- [ ] Do we anonymize data for training? I don't know, I trust your gut. Um we could also give them the ability to change like something like it's permanent unless you delete your account, which is easy to do. Our job is our goal is not to distort your data. Our goal is to be there for you when you need a job. And getting a job is hard enough. So like, you know, it'll just be here when you need us, and we're not doing anything with it. We don't we don't look at it. We don't. So, this is just like to help you get a job 

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

**MVP**: Free during beta, decide later Yeah, I'm waning towards like it's like ten dollars. That's it. As long as it's like not gonna make us lose money. And then per, you know, per hiring season. So like you know if they come back three years later it should be ten. I don't know, we could just do like a twenty dollar lifetime thing. I'm not sure. I think people are like, I'll pay whatever if it's gonna help me get a job so it works. I don't want it to be monthly subscription and I don't want it to be a recurring fee. I want it to be really clear, and we'll like we'll eat the tax, you know, like it's a flat fee. It's less than a meal out, you know? Like, that's what we want it to seem like. Oh and yeah, definitely free during beta. 

---
I DID NOT FILL THIS OUT 
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
