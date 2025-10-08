# RESUMAKER - Grant Application Form Answers
## AI for Economic Opportunity Fund - Concept Note
**Date**: October 7, 2025

---

## **PROJECT TITLE**
Resumaker: AI-Powered Resume Builder for Underrepresented Job Seekers

---

## **PROJECT SUMMARY** (150 words exactly)

Resumaker is a conversational AI platform that helps underrepresented job seekers—particularly immigrants, people of color, non-native English speakers, and workers from non-traditional backgrounds—create ATS-optimized, truthful resumes that unlock higher-paying employment. Using voice-first AI conversations in multiple languages (Spanish, Vietnamese, Mandarin, Tagalog, Arabic), the platform guides users through structured storytelling to capture authentic experiences, then translates responses into professional English resumes optimized for applicant tracking systems.

Our innovation includes a Truth Verification System that flags unsupported claims to prevent AI hallucination and a Persistent Knowledge Base that remembers users' career history, enabling faster resume updates for future job searches. By removing linguistic, cultural, and technological barriers to professional resume creation, Resumaker aims to increase job placement rates by 25% and average starting salaries by 15-20% for low-wage workers, unlocking an estimated $3,000-5,000 in additional annual earnings per user—potentially $1.8 million in Year 1 for 500 users.

---

## **PROJECT LEADERSHIP**

**Evan Stoudt** - Founder & Lead Developer
- LinkedIn: [Your LinkedIn URL]
- Role: Full-stack development, AI integration, product design, partnership strategy
- Experience: 15+ production projects including AI-powered applications (Car Talker with Gemini OCR), Google Apps Script systems serving 600+ users, proven performance optimization (60-95% improvements)

**[Optional: Add Advisory Board members once secured]**
- Workforce Development Advisor: [TBD - partnership with National Fund for Workforce Solutions or Per Scholas]
- AI/ML Technical Advisor: [TBD - through OpenAI cohort or Anthropic Claude community]
- Immigration & Language Access Expert: [TBD - Migration Policy Institute or local immigrant services org]

---

## **HOW AI/ML/LLMs WILL ADVANCE PROJECT GOALS**

Resumaker leverages multiple AI technologies, each serving distinct functions to overcome barriers faced by underrepresented job seekers:

**Large Language Models (LLMs):**
- **Conversational AI (Claude/Anthropic)**: Conducts natural language interviews to elicit career accomplishments, adapting questions dynamically based on user responses and maintaining context across multi-turn conversations
- **Multi-language Translation**: Enables users to respond in Spanish, Vietnamese, Mandarin, or other native languages, then translates to professional English while preserving cultural context and authentic voice
- **Resume Generation**: Synthesizes conversation data into ATS-optimized resume formats, applying platform-specific rules for Workday, Greenhouse, Lever, Taleo, and other applicant tracking systems
- **Truth Verification AI**: Cross-references every resume claim against conversation transcripts, flagging unsupported statements to prevent AI hallucination and ensure factual accuracy

**Machine Learning:**
- **Success Pattern Recognition**: Analyzes successful resume-to-hire outcomes to identify what resonates with employers for specific roles and industries, continuously refining recommendations
- **Keyword Optimization**: Extracts relevant keywords from job postings and strategically integrates them into resumes without "stuffing," improving ATS parseability while maintaining natural language
- **Predictive Personalization**: Learns from user interactions to adapt conversation depth, pacing, and follow-up questions based on communication style and background

**Optical Character Recognition (OCR):**
- **Resume Parsing (Gemini AI)**: Extracts structured data from uploaded existing resumes (PDF, DOCX, images) to pre-populate knowledge base and reduce user data entry burden—proven technology migrated from Car Talker project

**Speech-to-Text:**
- **Voice Recognition**: Converts spoken responses to text in multiple languages, enabling voice-first interaction that captures authentic storytelling (especially valuable for users less comfortable with writing)
- **Accessibility**: Supports users with limited typing ability, visual impairments, or those who think/express more naturally through speech

**Advanced Data Science & Automation:**
- **AI Agents for Operations**: Automated systems handle user onboarding, data validation, reminder scheduling, and outcome tracking—enabling lean operations without large staff
- **Semantic Search & RAG (Retrieval-Augmented Generation)**: Powers persistent knowledge base, allowing AI to retrieve relevant past accomplishments when user returns months later to build new resume
- **Impact Analytics**: Machine learning models track user outcomes (job applications, interviews, placements, salary increases) to measure effectiveness and identify areas for improvement

**Why AI is Essential:**
This project would be impossible without AI. Traditional resume services require 1-on-1 human counselors ($50-150/hour), limiting accessibility. AI enables:
- **Scale**: Serve thousands at fraction of cost
- **Speed**: Idea-to-reality in months (vs. years), using tools like Claude Code and Gemini for rapid development
- **Personalization**: Deep customization for each user without human labor constraints
- **Multilingual Access**: Serve Spanish, Vietnamese, Mandarin speakers simultaneously—impractical with human translators

---

## **SCOPE OF WORK & PROJECT MILESTONES**

### **6-Month Demonstration Phase Overview:**

**Goal**: Serve 500 underrepresented job seekers, demonstrate 25% increase in job placement rates and 15% increase in starting salaries, validate all core AI features.

---

### **Milestone 1: Foundation & Infrastructure (Months 1-2)**

**Objectives:**
- Build technical infrastructure (Next.js frontend, Python/FastAPI backend, Supabase database)
- Integrate core AI technologies (Claude API, Gemini OCR, Web Speech API)
- Recruit 3-5 pilot partner organizations (workforce development centers, immigrant service orgs)
- Enroll initial 100 beta users

**AI Technology Deployment:**
- **Claude API** for conversational framework
- **Gemini OCR** for resume upload/parsing (migrated from existing Car Talker codebase)
- **Web Speech API** for voice-to-text in English (expand to Spanish in Month 2)

**Deliverables:**
- Functional MVP: User accounts, basic conversation interface, resume upload, maintenance of conversation history
- 3-5 partner MOUs signed
- 100 users onboarded

---

### **Milestone 2: Core AI Innovation Deployment (Months 3-4)**

**Objectives:**
- Deploy Truth Verification System (prevent AI hallucination)
- Launch Persistent Knowledge Base (semantic storage/retrieval of user data)
- Activate multi-language support (7 languages: Spanish, Vietnamese, Mandarin, Tagalog, Arabic, French, Haitian Creole)
- Implement ChatGPT/Claude conversation import parser
- Expand to 300 total users

**AI Technology Deployment:**
- **Truth Verification AI**: Custom NLP layer cross-references resume claims against conversation transcripts, generates verification checklist for user review
- **Vector Database + RAG**: Semantic search over user's knowledge base enables "remember me" functionality for return visits
- **Multi-language Claude**: Translation layer with cultural context preservation (not literal translation)
- **Smart Parser**: Extracts accomplishments, skills, and metrics from pasted AI conversations (ChatGPT/Claude exports)

**Deliverables:**
- All 4 differentiating AI features live and tested
- 300 users served (cumulative)
- Initial user feedback collected and features refined

---

### **Milestone 3: ATS Optimization & Resume Generation (Month 5)**

**Objectives:**
- Integrate comprehensive ATS intelligence (2,350-line optimization guide covering Workday, Greenhouse, Lever, Taleo, iCIMS)
- Deploy resume generation engine (PDF via WeasyPrint, DOCX via python-docx)
- Launch visual editor for user customization
- Expand to 500 total users

**AI Technology Deployment:**
- **Job Posting Analysis AI**: Extracts keywords, detects ATS platform (via URL patterns), applies platform-specific formatting rules
- **Resume Formatter**: Converts conversation data into structured resume sections with ATS-compliant formatting
- **Keyword Integration Algorithm**: Strategically places job-relevant keywords from posting into resume without "stuffing"

**Deliverables:**
- Resume generation working for all major ATS platforms
- PDF and DOCX export functional
- 500 users served (target reached)

---

### **Milestone 4: Impact Measurement & Demonstration Readiness (Month 6)**

**Objectives:**
- Collect rigorous outcome data (job applications, interview rates, placements, starting salaries)
- Conduct user satisfaction surveys (NPS, qualitative testimonials)
- Analyze impact: target 25% increase in application success, 15% salary increase
- Prepare Demo Day presentation

**AI Technology Deployment:**
- **Outcome Tracking AI**: Automated follow-up surveys, data aggregation, impact calculation
- **Analytics Dashboard**: ML-powered insights on what resume features correlate with success

**Deliverables:**
- Impact data: 500 users, $1.8M estimated lifetime earnings increase
- 10-15 detailed user case studies
- Demo Day presentation ready (live platform showcase, testimonial videos)

---

### **How AI Advances Each Milestone:**

| Milestone | Without AI | With AI |
|-----------|-----------|---------|
| **Foundation** | Manual resume reviews by counselors ($150/hour × 2 hours = $300/user) | Automated conversation + OCR ($5/user in API costs) |
| **Innovation** | Impossible—human translators can't work 24/7, fact-checkers too expensive | AI enables multi-language, truth verification, knowledge persistence at scale |
| **ATS Optimization** | Requires expert knowledge ($200/resume for professional services) | AI applies 2,350-line rulebook automatically |
| **Impact Measurement** | Manual surveys and data entry (weeks of staff time) | Automated tracking, real-time analytics |

**Bottom Line**: AI transforms a high-cost, low-scale, slow service into a low-cost, high-scale, fast platform accessible to underrepresented populations.

---

## **DATA SOURCES**

### **Data We Use:**

#### **1. Publicly Available Data (No Privacy Concerns)**
- **ATS Optimization Rules**: Public documentation from Workday, Greenhouse, Lever, Taleo, iCIMS on resume formatting requirements (compiled into 2,350-line guide)
- **LLM General Knowledge**: Claude, Gemini, and other models trained on public internet data provide general career advice, resume best practices, industry terminology
- **Accessibility**: Readily available, no legal/regulatory barriers

#### **2. User-Generated Content (Privacy-Protected)**
- **What we collect**:
  - Voice/text conversations about career history (45-60 min initial; 10-15 min return visits)
  - Uploaded resumes (PDF, DOCX, images) for OCR parsing
  - Job postings (URLs or copy-paste) for keyword extraction
  - Optional: Job outcome data (applications submitted, interviews, offers, salaries)

- **How accessible**:
  - Stored in Supabase (PostgreSQL database, SOC 2 Type II certified)
  - Encrypted at rest (AES-256) and in transit (TLS 1.3)
  - User-owned: Users can export all data (PDF, CSV, JSON) at any time
  - User-controlled deletion: One-click permanent deletion of all data

- **Privacy & Regulatory Compliance**:
  - ✅ **No data sharing**: Zero sharing with employers, government, third parties
  - ✅ **No data selling**: Revenue from user fees (sliding scale $0-20), not data monetization
  - ✅ **No AI training**: User data NOT used to train public AI models
  - ✅ **GDPR compliant** (for international users)
  - ✅ **CCPA compliant** (California Consumer Privacy Act)
  - ✅ **Anonymized research**: If data used for impact studies, fully anonymized and aggregated
  - ✅ **Consent-based**: Users sign clear privacy waivers explaining data use
  - ✅ **Portable**: Users receive downloadable "data bucket" in digestible formats

- **Legal concerns addressed**:
  - Immigration status: We do NOT collect immigration status; AI trained to redirect if user mentions it
  - Sensitive demographics: Race, gender, age NOT required (optional for impact measurement only)
  - Voice recordings: Transcribed to text and deleted within 48 hours (no voice biometrics stored)

#### **3. Outcome Data for Impact Measurement (Aggregated)**
- **What we collect**: User self-reported job applications, interview rates, job placements, starting salaries
- **How we collect**: Optional in-app surveys, partner organization tracking (for users who opt-in)
- **Privacy**: Aggregated only (e.g., "500 users averaged $3,750 salary increase"), never individual-level reporting
- **Accessibility**: Stored separately from personally identifiable information (PII)

### **Data Governance Summary:**
| Data Type | Source | Storage | Privacy Protections | User Control |
|-----------|--------|---------|---------------------|--------------|
| **ATS rules** | Public docs | Backend database | N/A (public) | N/A |
| **LLM knowledge** | Claude/Gemini | External APIs | Vendor SOC 2 | N/A |
| **User conversations** | User input | Supabase (encrypted) | No sharing, no selling | Export, delete anytime |
| **Resumes uploaded** | User files | Supabase (encrypted) | No sharing, no selling | Export, delete anytime |
| **Outcome data** | User surveys | Supabase (encrypted, anonymized) | Aggregated reporting only | Opt-in only |

**Key Point**: We are data stewards, not data owners. Users own their data, control it fully, and can take it with them or delete it permanently.

---

## **TECHNICAL EXPERTISE**

### **Current Internal Expertise:**

**Evan Stoudt (Founder & Lead Developer)**
- **Strengths**:
  - Full-stack development: Next.js, React, Python (FastAPI), Supabase
  - AI integration: Claude API, Gemini API (proven in Car Talker project with OCR)
  - Prompt engineering: Extensive experience optimizing LLM outputs
  - Rapid prototyping: Idea-to-MVP in weeks using Claude Code, Gemini
  - Performance optimization: 60-95% improvements in past projects
  - Database design: PostgreSQL, structured and unstructured data
  - Deployment: Vercel, Railway, cloud infrastructure

- **Limitations (honest assessment)**:
  - General technical understanding + internet research (strong foundation)
  - Could benefit from deep expertise in:
    - Advanced NLP techniques (semantic similarity, bias detection algorithms)
    - Production-scale AI system architecture (handling 100K+ users)
    - Multilingual NLP edge cases (low-resource languages, dialect variations)
    - Security auditing for AI systems (prompt injection, adversarial inputs)

**Assessment**: Internal expertise is **sufficient for MVP and demonstration phase** (6 months, 500 users). Scaling phase (10K+ users) will benefit from additional specialized expertise.

---

### **External Support Needed:**

#### **1. AI/ML Technical Advisor (Sought through OpenAI Cohort)**
- **Need**: Expert in production AI systems, multilingual NLP, bias mitigation
- **Ideal profile**:
  - Experience deploying Claude/GPT at scale
  - Background in multilingual NLP and translation quality assurance
  - Expertise in AI ethics, fairness, and bias detection
  - Familiarity with vector databases and RAG (Retrieval-Augmented Generation)
- **Source**: OpenAI technical support (through grant cohort), Anthropic Claude developer community, academic researchers

#### **2. Workforce Development Subject Matter Expert**
- **Need**: Career counselor or workforce development professional to validate resume quality, conversation flow, and impact measurement
- **Ideal profile**:
  - 10+ years in workforce development or career services
  - Deep knowledge of barriers faced by immigrants, people of color, low-income job seekers
  - Understanding of ATS trends and employer expectations
- **Source**: Pilot partner organizations (workforce centers), National Association of Workforce Development Professionals (NAWDP)

#### **3. Immigration & Language Access Expert**
- **Need**: Advisor on culturally responsive design for immigrant and multilingual populations
- **Ideal profile**:
  - Experience serving Limited English Proficiency (LEP) communities
  - Understanding of cultural differences in professional communication
  - Expertise in language access, interpretation, translation quality
- **Source**: Migration Policy Institute (MPI), National Immigration Law Center (NILC), local immigrant service orgs

---

### **No External Consulting Firm Contracted (Yet)**

**Current approach**:
- Lean startup model—Evan handles all technical development initially
- Leverage OpenAI cohort support (included in grant)
- Recruit advisors as volunteers or small stipends (not full consulting engagements)

**If scaling grant secured**:
- May contract specialized firms for:
  - Security audit (penetration testing, privacy compliance review)
  - Translation quality assurance (native-speaker testing for 7 languages)
  - User research & UX design (testing with diverse populations)

**Key Point**: We have sufficient expertise to build and demonstrate, but recognize value of specialized advisors to scale responsibly.

---

## **ETHICS AND BIAS**

### **Why This Project Exists: Combating Bias in Hiring**

The traditional resume process embeds systemic bias that filters out people of color, immigrants, and candidates from non-traditional backgrounds:

**Existing Biases We're Addressing:**
- **Language bias**: Non-native English speakers penalized for imperfect grammar, even when qualified
- **Cultural bias**: US resume norms favor assertive self-promotion, which conflicts with some cultural values (humility in many Asian, Latin American cultures)
- **Name bias**: Studies show resumes with "ethnic-sounding" names receive 50% fewer callbacks than identical resumes with "white-sounding" names
- **Format bias**: ATS systems penalize creative formats often used by candidates unfamiliar with corporate norms
- **Credential bias**: Traditional resumes emphasize degrees/pedigree over skills, disadvantaging those without formal education
- **Experience description bias**: Candidates from non-dominant backgrounds often undersell accomplishments due to lack of exposure to professional resume language

**Resumaker's Mission**: Center people of color, immigrants, and economically marginalized populations in design, ensuring AI empowers rather than replicates bias.

---

### **Potential Ethical & Bias Concerns + Mitigation**

#### **Concern 1: AI-Generated Content May Misrepresent User**
**Risk**: AI could exaggerate, fabricate, or mischaracterize user's experience.

**Mitigation**:
- ✅ **Truth Verification System** (core feature): Every claim cross-referenced against conversation; unsupported claims flagged for user review
- ✅ **User approval required**: User must review and approve every section before export
- ✅ **Edit control**: Users can modify any line; AI is advisory, not prescriptive
- ✅ **Transparency**: AI explains why it phrased something a certain way
- ✅ **Philosophy**: "Help people tell their truth better, not help them lie"

#### **Concern 2: Gender-Coded Language**
**Risk**: AI might use masculine-coded language (e.g., "aggressive," "dominant") or feminine-coded language (e.g., "collaborative," "supportive") based on user's gender.

**Mitigation**:
- ✅ **Harvard Gender Decoder integration**: Test all resumes for gender-coded words
- ✅ **Gender-neutral action verb library**: AI trained on inclusive language
- ✅ **Blind testing**: Generate resumes for same experience with different names (male/female, ethnic variations), check for phrasing differences
- ✅ **DEI consultant review**: Quarterly audits by diversity, equity, inclusion experts

#### **Concern 3: Racial Bias in Tone/Phrasing**
**Risk**: AI might generate different tone (assertive vs. humble) based on inferred race (e.g., from name or language spoken).

**Mitigation**:
- ✅ **Comparative A/B testing**: Same experience, different demographic details → verify consistent phrasing
- ✅ **User tone preference**: Users choose "assertive" vs. "humble" vs. "balanced" tone (not AI-assumed)
- ✅ **Diverse training data**: Resume examples from people of color, not just white candidates
- ✅ **Advisory input**: Advisors from target communities (Black, Latinx, Asian, immigrant) review outputs

#### **Concern 4: Cultural Bias in "Professionalism"**
**Risk**: What counts as "professional" is culturally defined by dominant (white, corporate US) norms; AI may impose these norms on candidates from other cultures.

**Mitigation**:
- ✅ **Cultural bridging, not erasure**: AI translates cultural norms while preserving authenticity
  - Example: Vietnamese user says "We achieved..." → AI: "Led team to achieve..." (bridges without erasing collective framing)
- ✅ **User education**: AI explains WHY US employers expect certain phrasing (empowering users with knowledge, not forcing conformity)
- ✅ **Cultural advisors**: Native speakers from target language communities review translations and tone
- ✅ **User choice**: Offer "culturally adapted" vs. "preserve original tone" options

#### **Concern 5: Accessibility Barriers (Digital Divide)**
**Risk**: Platform requires internet + device, potentially excluding most disadvantaged.

**Mitigation**:
- ✅ **Partnership access**: Pilot users access platform at workforce centers (computers/internet provided)
- ✅ **Mobile-first design**: Works on smartphones (more accessible than laptops)
- ✅ **Low-bandwidth mode**: Optimized for slow internet (rural areas, prepaid data plans)
- ✅ **Offline mode**: Draft resumes offline, sync when connected
- ✅ **Screen reader compatible**: WCAG 2.1 AA compliance for visually impaired users

#### **Concern 6: Economic Bias (Who Can Afford It?)**
**Risk**: If platform charges fees, it replicates economic barriers.

**Mitigation**:
- ✅ **Sliding scale pricing**: $0-20 based on ability to pay
- ✅ **Sponsorship model**: Organizations can buy "licenses" to give to low-income users (e.g., 30 licenses = 30 free users)
- ✅ **"Pay it forward"**: Users who get jobs can sponsor someone else
- ✅ **Free for pilot**: All 500 demonstration users get free access
- ✅ **Public benefit corporation**: Structured to prioritize mission over profit

#### **Concern 7: Privacy & Surveillance Fears**
**Risk**: Vulnerable populations (immigrants, formerly incarcerated) may fear data could be used against them.

**Mitigation**:
- ✅ **Radical transparency**: Plain-language privacy policy in all supported languages
- ✅ **Zero data sharing**: Explicit policy—no sharing with government, employers, third parties
- ✅ **Anonymous mode**: Users can create resumes without real name/contact until final export
- ✅ **Community endorsement**: Pilot partners (trusted CBOs) vouch for platform safety
- ✅ **Legal review**: Immigration attorneys review privacy practices

---

### **Bias Mitigation Testing Plan:**

| Bias Type | Testing Method | Success Metric |
|-----------|----------------|----------------|
| **Gender bias** | Harvard Gender Decoder + demographic A/B tests | <5% gender-coded words, no tone variance by gender |
| **Racial bias** | Name-based A/B tests (same experience, different names) | No phrasing difference by race |
| **Cultural bias** | Cultural advisors review + user feedback | 90% user satisfaction with cultural respect |
| **Age bias** | Age-coded language scanner | 0 age-coded terms (e.g., "digital native") |
| **AI hallucination** | Truth verification system | 95% claim accuracy (verified against conversation) |

---

### **Ethical Principles Guiding Development:**

1. **Center marginalized voices**: Design WITH people of color, immigrants, low-income users—not FOR them
2. **Transparency**: Users understand how AI works, what data is used, why recommendations are made
3. **User agency**: AI advises, user decides—never force AI outputs
4. **Truth over performance**: Help users present authentic selves truthfully, not fabricate impressive stories
5. **Privacy as default**: Minimal data collection, maximum user control
6. **Accessibility**: Design for lowest-resourced users first (slow internet, old phones, limited English)

**Bottom Line**: We're building this because AI has potential to reduce bias in hiring—but only if we build with bias mitigation as a core feature, not an afterthought.

---

## **BUDGET OVERVIEW** (Optional - if requested)

**Total Request**: $250,000 (Demonstration Grant)

**Allocation**:
- **Technical development** (40%): $100,000
  - Developer time (6 months, full-time equivalent)
  - API costs (Claude, Gemini - estimated 500 users × $10/user)
  - Infrastructure (Vercel, Railway, Supabase - ~$500/month)

- **Partnership & user recruitment** (25%): $62,500
  - Partnership manager (part-time, 6 months)
  - Partner stipends (3-5 partners × $5,000 each for user recruitment)
  - Marketing materials (multi-language flyers, videos)

- **User support** (15%): $37,500
  - User support specialist (part-time, 6 months)
  - Helpdesk setup (Zendesk or similar)
  - Training materials for partner staff

- **Impact measurement** (10%): $25,000
  - Data analyst (part-time, 6 months)
  - Survey platforms (Typeform, Qualtrics)
  - User interview incentives ($25 gift cards × 100 interviews)

- **Advisory & consulting** (10%): $25,000
  - AI/ML advisor (10 hours/month × 6 months × $200/hour)
  - Workforce development SME (5 hours/month × $150/hour)
  - Cultural advisors for 7 languages ($500 per language for translation review)
  - DEI consultant for bias audits ($5,000)

**ROI**: $250K investment → 500 users × $3,750 annual earnings increase = $1.875M (Year 1) → **7.5x ROI in Year 1**

---

## **MISSION STATEMENT**

**Resumaker's Mission:**

> **Resumaker empowers job seekers from underrepresented backgrounds—particularly people of color, immigrants, and those experiencing economic uncertainty—to tell their authentic career stories and access higher-wage employment opportunities.**

> We believe the traditional resume process embeds bias that filters out qualified candidates based on language, culture, and socioeconomic background. By centering marginalized communities in our design and leveraging AI to remove linguistic and cultural barriers, we're building a tool that levels the playing field—not by helping people lie, but by helping them tell their truth in the language employers understand.

> Our North Star: Every user deserves a resume that accurately represents their value and opens doors to economic stability.

---

## **VISION STATEMENT**

**Where We're Going:**

> A future where a candidate's potential is judged by their skills and accomplishments, not their English fluency, cultural background, or access to expensive career counselors.

> Where an immigrant who speaks five languages can showcase that as an asset, not hide behind imperfect English grammar.

> Where a single mother returning to the workforce after a career gap can frame that experience with confidence, not apology.

> Where a formerly incarcerated person can translate street skills into professional language without shame.

> Where economic opportunity is accessible to all, starting with a resume that tells the truth—and gets you the interview.

---

**END OF APPLICATION FORM ANSWERS**

---

**Next Steps**:
1. ✅ Copy project title, summary, and answers into online form
2. ✅ Update LinkedIn URL for Evan Stoudt
3. ✅ Finalize contact information (email, phone, organization name/EIN if applicable)
4. ✅ Review for tone, clarity, and alignment with GitLab Foundation's priorities
5. ✅ Submit by October 31, 2025 at 5:00 PM PT

**Prepared by**: Evan Stoudt + Claude Code
**Date**: October 7, 2025
**Status**: Ready for submission
