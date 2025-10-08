# RESUMAKER - Grant Application (Evan's Voice)
## AI for Economic Opportunity Fund - Ready to Submit

---

## **1. PROJECT TITLE**
Resumaker: AI-Powered Resume Builder for Underrepresented Job Seekers

---

## **2. PROJECT SUMMARY** (<150 words)

Resumaker helps people who don't identify as "good writers"—immigrants, people of color, folks from non-dominant cultural backgrounds—create truthful, ATS-optimized resumes through natural conversation in their own language.

Here's how it works: You talk to AI (voice or text) in Spanish, Vietnamese, Mandarin, whatever language you think in. The platform asks you about your work, your accomplishments, your skills—like a really good conversation with a career counselor. Then it translates your authentic story into professional English that gets past applicant tracking systems.

The differentiator? A **Truth Verification System** that flags claims without evidence—we don't want to help people lie, we want to help them tell their truth better. Plus a **Persistent Knowledge Base** that remembers you—come back a year later, and it already knows your career history.

Target: 25% increase in job placements, 15-20% salary bump for low-wage workers. That's $3,000-5,000 more per year, per person. For 500 users in Year 1, that's $1.8 million in economic impact.

---

## **3. PROJECT LEADERSHIP**

**Evan Stoudt** - Founder & CEO
- LinkedIn: [Your LinkedIn URL]
- What I do: Full-stack dev, AI integration, product design
- Track record: 15+ production projects including Car Talker (Gemini OCR), Google Apps Script systems serving 600+ users, proven performance optimization (60-95% improvements)

**Why This Project**

I was a high school principal looking to transition into tech. White male, under 40, resume full of achievements. And I still struggled to get interviews because my background didn't match traditional career paths in software development. If it was that hard for me—someone with every structural advantage—imagine how much harder it is for people facing language barriers, name bias, or cultural discrimination. That's when I realized: the resume system is broken for anyone who doesn't fit the mold. I've experienced firsthand how difficult it is to tell your story when your background doesn't match the boxes employers expect. That's why this project exists.

---

## **4. HOW AI/ML/LLMs ADVANCE PROJECT GOALS**

**The problem**: Traditional resume services cost $150/hour for a human counselor. Most low-wage workers can't afford that. And even if they could, those counselors don't speak 7 languages or understand cultural differences in professional communication.

**How AI changes the game**:

**Conversational AI (Claude)**
- Not forms. Not templates. Actual conversation.
- Asks follow-up questions based on what you say
- Adapts to your communication style
- Remembers context across the whole conversation
- Why it matters: People tell better stories when they're talking, not filling out boxes

**Multi-Language AI (Claude + custom translation)**
- You speak Vietnamese, AI asks questions in Vietnamese, you answer in Vietnamese
- Then translates to professional English—not literal translation, cultural translation
- Example: In some cultures, humility is valued. US resumes need confidence. AI bridges that gap.
- Why it matters: 25 million Limited English Proficiency (LEP) workers in the US can't articulate their value in English—but they have the skills

**Truth Verification AI (custom layer)**
- After generating resume, AI cross-checks every claim against what you said in conversation
- Flags anything that doesn't have evidence: "You said 'large team' but the resume says '25 people'—confirm?"
- User reviews, confirms or corrects
- Why it matters: We're not helping people lie. We're preventing AI hallucination and building user confidence.

**Machine Learning for pattern recognition**
- Analyzes what resumes actually get people hired
- Learns what keywords matter for specific roles
- Adapts recommendations based on success patterns
- Why it matters: Not guessing what works—learning from what actually works

**OCR (Gemini - already built)**
- Upload your old resume, AI extracts the data automatically
- Migrating proven code from Car Talker project (automotive receipt parsing)
- Why it matters: Don't make people re-type everything. Respect their time.

**Speech-to-Text (Web Speech API)**
- Voice-first interaction—talk while driving, cooking, whenever
- Works in multiple languages
- Why it matters: Writing is hard. Talking is natural. Especially for people who aren't "good writers."

**AI Agents for automation**
- Behind the scenes, AI handles onboarding, reminders, data validation
- Keeps the operation lean—no need for 50 staff members
- Why it matters: Low overhead = low cost = accessible to people who need it most

**Bottom line**: This project wouldn't exist without AI. Human counselors at scale? $150/hour. AI at scale? $5/user in API costs. That's the difference between "exclusive service for wealthy professionals" and "accessible tool for low-wage workers."

And the speed—idea to working prototype in months, not years. That's using Claude Code and Gemini for development. AI isn't just IN the product, it IS the product.

---

## **5. SCOPE OF WORK & MILESTONES**

**Goal for 6 months**: Serve 500 people from underrepresented backgrounds. Show a 25% bump in job placement success and 15% higher starting salaries.

### **Months 1-2: Build the Foundation**

**What we're building:**
- Core infrastructure (Next.js frontend, Python backend, Supabase database)
- Basic conversation interface (text + voice in English and Spanish to start)
- Resume upload with OCR (migrating existing Gemini code from Car Talker—it's already built, just needs new prompts)
- User accounts and authentication

**AI deployment:**
- Claude API for conversation
- Gemini OCR for resume parsing (proven tech, just adapting it)
- Web Speech API for voice input

**Partnerships:**
- Sign up 3-5 workforce development centers or immigrant service orgs
- Get 100 beta users enrolled

**Milestone**: Working MVP that lets you talk to AI, upload a resume, and get a basic conversation going.

---

### **Months 3-4: The Differentiators**

**What we're building:**
- **Truth Verification System** - The "no lying" feature. AI checks every claim against the conversation, flags anything unsupported.
- **Persistent Knowledge Base** - Stores your accomplishments, skills, stories. Come back a year later, it remembers you.
- **Multi-language support** - Full 7-language rollout (Spanish, Vietnamese, Mandarin, Tagalog, Arabic, French, Haitian Creole)
- **Smart Import** - Paste your ChatGPT conversation, AI extracts accomplishments/skills automatically

**Why AI is essential here:**
- Truth check: Human fact-checkers cost $50/hour. AI does it instantly for pennies.
- Knowledge base: Semantic search (RAG—Retrieval-Augmented Generation) finds relevant past accomplishments automatically
- Translation: Not Google Translate—cultural context translation. "We achieved" (Vietnamese humility) → "Led team to achieve" (US resume confidence)
- Import parser: NLP extracts structured data from unstructured conversation. Humans would take hours.

**Target**: 300 total users, initial feedback, refine features based on real use.

---

### **Month 5: ATS Optimization**

**What we're building:**
- Resume generation engine with platform-specific rules for Workday, Greenhouse, Lever, Taleo, iCIMS
- Job posting analyzer (paste a job posting, AI extracts keywords and detects which ATS system)
- PDF and DOCX export (WeasyPrint for beautiful PDFs, python-docx for ATS-friendly Word docs)
- Visual editor so users can customize

**The secret weapon**: 2,350-line ATS Optimization Guide (already written, just needs to be integrated)
- Every major ATS platform analyzed
- Platform-specific formatting rules
- Keyword strategies that don't feel like keyword stuffing

**Why AI matters**: Without AI, you'd need an ATS expert ($200/resume). With AI, the 2,350-line guide becomes automatic rule-following.

**Target**: 500 users total (goal reached)

---

### **Month 6: Prove It**

**What we're measuring:**
- Job applications submitted
- Interview rates
- Job placements
- Starting salaries (this is the big one)

**How we're measuring:**
- User surveys (opt-in, incentivized with gift cards)
- Partner organization tracking (workforce centers track placements)
- Follow-up conversations 3 months after resume creation

**Target outcomes:**
- 25% increase in application-to-interview rate
- 15% increase in starting salaries ($3,000-5,000 per person)
- 500 users × $3,750 average = **$1.875 million in Year 1 economic impact**

**What we're showing at Demo Day:**
- Live platform demo (someone creates a resume in real-time, in Spanish, with truth verification)
- Impact data
- User testimonials (video + written)
- Partner endorsements

---

**The AI throughout**: Every milestone is impossible without AI. Conversation depth at scale? AI. Multi-language? AI. Truth checking? AI. ATS optimization? AI. What would take a team of 20 counselors now takes one developer and smart AI integration.

---

## **6. DATA SOURCES**

### **What data we use:**

**Public data (no privacy concerns):**
- ATS formatting rules - public documentation from Workday, Greenhouse, etc. (compiled into that 2,350-line guide)
- General career advice - what LLMs already know from training on public internet
- Job posting data - user pastes job URLs or descriptions (not scraped, user-provided)

**User data (privacy-protected):**
- Conversations (45-60 min initially, 10-15 min on return visits)
- Uploaded resumes (OCR'd then user confirms accuracy)
- Optional: job outcome data (did you apply? get interviews? get hired? salary?)

### **How accessible is this data:**

Stored in Supabase (PostgreSQL, SOC 2 certified). Encrypted at rest (AES-256), encrypted in transit (TLS 1.3).

**User owns their data. Period.**
- Export everything anytime (PDF, CSV, JSON)
- Delete everything permanently with one click
- We don't share it (not with employers, not with government, not with anyone)
- We don't sell it (revenue comes from user fees, not data)
- We don't use it to train public AI models (your story is yours)

**Legal/privacy/regulatory stuff:**
- GDPR compliant (if we expand internationally)
- CCPA compliant (California privacy law)
- No immigration status collection (explicitly don't ask, AI trained to redirect if user mentions it)
- Voice recordings deleted after 48 hours (transcribed to text, original audio gone)
- Demographic data optional (only for impact measurement, never required)

### **Data concerns we've thought through:**

**"Will this be used against immigrants?"**
No. Zero sharing with government or immigration enforcement. Anonymous mode available (create resume without real name until final export).

**"Can my employer see this?"**
No. This is yours. You decide what to share and with whom.

**"What if I want to delete everything?"**
One click, permanent deletion. Gone.

**"How do I know you won't change your mind and sell my data?"**
Because we're structured as a public benefit corporation (or will be). Mission over profit is legally binding.

---

## **7. TECHNICAL EXPERTISE**

### **What I bring:**

I'm a full-stack developer with 15+ production projects shipped. I know Next.js, Python, Supabase, Claude API, Gemini API. I've built AI-integrated systems before (Car Talker with OCR is working code right now). I know how to go from idea to deployed product quickly.

**Honest assessment of what I need help with:**
- Advanced NLP techniques (bias detection algorithms, semantic similarity edge cases)
- Production scaling (going from 500 to 50,000 users without breaking)
- Multilingual NLP edge cases (dialect variations, low-resource languages)
- Security auditing for AI systems (prompt injection, adversarial inputs)

**For the 6-month demonstration phase**: I've got this. Internal expertise is sufficient.

**For the scaling phase**: I'll need specialized advisors.

### **Advisory support I'm seeking:**

**AI/ML Technical Advisor** (through OpenAI cohort)
- Expert in production AI, multilingual NLP, bias mitigation
- Help me scale responsibly
- Probably sourced through the grant cohort or Anthropic Claude community

**Workforce Development Expert** (from pilot partners)
- Career counselor who knows the barriers immigrant and low-income job seekers face
- Validates resume quality and conversation flow
- Ensures we're solving the right problem the right way

**Immigration & Language Access Expert**
- Advisor on culturally responsive design for Limited English Proficiency communities
- Translation quality review
- Probably sourced from Migration Policy Institute or local immigrant services org

**No consulting firm contracted yet.** Lean startup approach—I build, I leverage the cohort support, I recruit advisors as volunteers or small stipends. If we get the scaling grant, then we hire firms for security audits, translation QA, formal user research.

**The point**: I can build this. But I'm smart enough to know where I need expert input.

---

## **8. ETHICS AND BIAS**

### **Why this project exists:**

The traditional resume process is rigged against people of color, immigrants, and anyone who didn't learn the "rules" of corporate America.

**The bias in hiring:**
- **Language bias**: Imperfect English grammar = rejected, even if you're qualified
- **Name bias**: "Ethnic-sounding" names get 50% fewer callbacks (same resume, different name)
- **Cultural bias**: US resumes demand aggressive self-promotion. Some cultures value humility. You lose either way.
- **Format bias**: ATS systems reject creative formats that people unfamiliar with corporate norms use
- **Credential bias**: "Must have degree" filters out people with skills but no paper

**Resumaker's mission**: Help people from marginalized backgrounds compete on a playing field that's currently tilted against them. Not by lying—by telling their truth in the language the system understands.

---

### **Concerns we're addressing:**

**1. "AI might help people lie"**

Yeah, that's why we built the Truth Verification System. After AI generates the resume, it cross-checks every claim against the conversation. Anything unsupported gets flagged for user review.

Example:
- Resume says "Increased revenue by 150%"
- AI checks: Did user mention 150% in conversation?
- If not: "You said 'growth' but didn't specify 150%. Confirm or adjust?"

Not accusatory. Editorial. Empowering. Making sure AI didn't hallucinate.

**Philosophy**: Help people tell their truth better, not help them lie.

---

**2. "AI might use gender-coded language"**

Possible. "Aggressive" is masculine-coded. "Collaborative" is feminine-coded. We don't want the AI generating different resumes based on perceived gender.

**What we're doing:**
- Running every resume through Harvard's Gender Decoder
- Training AI on gender-neutral action verbs
- Testing: Generate resume for same experience with male name vs. female name. Check for differences.
- Quarterly audits by a DEI consultant

**If we find bias, we fix it.**

---

**3. "AI might sound different for different races"**

Same concern as gender. We don't want tone (assertive vs. humble) varying based on inferred race.

**What we're doing:**
- A/B testing: Same experience, different demographic details (name variations, language spoken). Check for tone consistency.
- User controls tone preference (assertive, humble, balanced)—not AI-assumed based on background
- Training data includes diverse resume examples (not just white candidates)
- Advisory board includes people from target communities (Black, Latinx, Asian, immigrant) reviewing outputs

---

**4. "US 'professionalism' standards are culturally biased"**

Yep. What counts as "professional" in corporate America isn't universal. It's a specific cultural norm that favors people who grew up in that culture.

**What we're doing:**
- **Cultural bridging, not erasure**: AI translates norms while preserving authenticity
  - Example: Vietnamese user says "We achieved..." (collective framing valued in Vietnamese culture)
  - AI: "Led team to achieve..." (individual leadership valued in US resumes)
  - Bridges the gap without erasing the original meaning
- **User education**: AI explains WHY US employers expect certain phrasing. Empowering, not forcing.
- **User choice**: "Culturally adapted" vs. "preserve original tone" toggle

---

**5. "What about people without smartphones or internet?"**

Valid concern. Digital divide is real.

**What we're doing:**
- **Partnership access**: Pilot users access platform at workforce development centers (computers and internet provided)
- **Mobile-first design**: Works on cheap smartphones (more accessible than laptops)
- **Low-bandwidth mode**: Optimized for slow connections (rural areas, prepaid data)
- **Offline mode**: Draft resume offline, sync when you get wifi
- **Screen reader compatible**: WCAG 2.1 AA accessibility standards for visually impaired users

---

**6. "Can people afford it?"**

If we charge too much, we replicate the economic barrier we're trying to solve.

**Pricing model:**
- **Sliding scale**: $0-20 based on what you can pay
- **Sponsorship**: Organizations buy "licenses" for their clients (e.g., workforce center pays for 30 users)
- **Pay it forward**: Get a job using Resumaker? Sponsor someone else.
- **All 500 demonstration users: FREE**
- **Structured as public benefit corporation**: Mission over profit, legally binding

**Philosophy**: Getting a job is hard enough. Don't make the tool a barrier.

---

**7. "Privacy fears for vulnerable populations"**

Immigrants, formerly incarcerated folks, people with legitimate reasons to fear surveillance.

**What we're doing:**
- **Radical transparency**: Plain-language privacy policy in all supported languages (not legalese)
- **Zero data sharing**: Explicitly NO sharing with government, employers, anyone. Revenue from users, not data.
- **Anonymous mode**: Create resume without real name/contact info until you're ready to export
- **Community endorsement**: Pilot partners (trusted community orgs) vouch for platform safety
- **Legal review**: Immigration attorneys reviewing our privacy practices

---

### **Testing for bias:**

| Bias Type | How We Test | Success Metric |
|-----------|-------------|----------------|
| **Gender bias** | Harvard Gender Decoder + A/B tests | <5% gender-coded words, no tone variance |
| **Racial bias** | Name-based A/B tests | No phrasing difference by race |
| **Cultural bias** | Cultural advisors + user feedback | 90% user satisfaction with respect |
| **AI hallucination** | Truth verification cross-check | 95% accuracy rate |

---

### **Our ethical principles:**

1. **Center marginalized voices**: Design WITH people of color and immigrants, not FOR them
2. **Transparency**: Users understand how AI works, what data is used, why
3. **User agency**: AI advises, user decides. Never force AI outputs.
4. **Truth over performance**: Authentic self, truthfully presented—not fabricated impressive stories
5. **Privacy as default**: Collect minimal data, give maximum user control
6. **Accessibility first**: Design for the lowest-resourced users (slow internet, old phones, limited English)

---

**Bottom line**: We're building this BECAUSE AI can reduce bias in hiring. But only if we build bias mitigation into the core, not as an afterthought. We're not naive about AI's potential for harm. We're intentional about preventing it.

---

**END OF ANSWERS**

---

**These are ready to copy-paste. They sound like me. They're direct, specific, and honest about both the problem and the solution.**
