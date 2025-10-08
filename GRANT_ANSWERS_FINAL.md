# RESUMAKER - Grant Application (Final - Formal Voice)
## AI for Economic Opportunity Fund - Oct 31, 2025

---

## **1. PROJECT TITLE**
Resumaker: AI-Powered Resume Builder for Underrepresented Job Seekers

---

## **2. PROJECT SUMMARY** (<150 words)

A resume should tell a person's story. But most people—especially those from underrepresented backgrounds—don't love writing resumes. They struggle to translate lived experience into the language employers understand.

Resumaker works like being interviewed for a biography. Over 10-minute conversations (voice or text, in Spanish, Vietnamese, Mandarin, or English), thoughtful questions draw out your authentic story: What did you build? What challenges did you overcome? Follow-up questions go deeper, like a journalist uncovering details.

The AI takes notes, captures the whole picture (like a thumbprint scanner—multiple touches to get it right), then translates your story into professional English. An AI fact-check helps you verify everything feels true to who you are and factually correct (no AI hallucinations). Canva-like design makes editing simple.

Time with Resumaker is about documenting your real accomplishments so you can show up as your best self and be a competitive applicant. The platform captures your career as it grows—some wins don't fit neatly on a traditional resume, but they matter to your story and shape who you become.

---

## **3. PROJECT LEADERSHIP**

**Evan Stoudt** - Founder & Lead Developer
- LinkedIn: [Your LinkedIn URL]
- **Technical Background**: 15+ production systems deployed, specializing in AI integration and performance optimization (proven 60-95% improvements across projects)
- **Relevant Experience**:
  - Car Talker (Gemini OCR implementation - proven technology ready for migration)
  - Implementation Tracker (serves 600+ users with optimized architecture)
  - Demonstrated ability to ship AI-integrated products from concept to production

---

## **4. HOW AI/ML/LLMs ADVANCE PROJECT GOALS**

### Challenge
Traditional resume services require 1-on-1 human counselors at $50-150/hour, limiting accessibility for low-wage workers. These services lack multilingual capacity and cultural competency to serve diverse populations effectively.

### Discovery
AI enables delivery of personalized, culturally-responsive resume assistance at scale, reducing per-user cost from $150 to approximately $5 while maintaining quality through specialized implementations.

### Technical Implementation

**Large Language Models (Claude/Anthropic)**
- **Conversational Interface**: Asks thoughtful questions and follows up based on what you share, adapting to how you naturally communicate
- **Multi-Language Translation**: Cultural context preservation (not literal translation)—example: Vietnamese collective framing ("We achieved") translated to US resume conventions ("Led team to achieve") while maintaining authentic meaning
- **Resume Generation**: Synthesis of conversation data into ATS-compliant formats with platform-specific rules (Workday, Greenhouse, Lever, Taleo, iCIMS)
- **AI Fact-Check**: Cross-references every claim against what you actually said, flags anything that doesn't match for you to review

**Machine Learning Applications**
- **Pattern Recognition**: Analysis of successful resume-to-hire outcomes to identify effective keyword integration and accomplishment framing for specific roles
- **Predictive Personalization**: Adaptive conversation pacing and depth based on user interaction patterns
- **Keyword Optimization**: Strategic integration without "stuffing," maintaining natural language flow

**Optical Character Recognition (Gemini AI)**
- **Resume Parsing**: Extraction of structured data from uploaded documents (PDF, DOCX, images)
- **Proven Technology**: Migrating existing Car Talker codebase (automotive receipt parsing with 90%+ accuracy)
- **Implementation**: Prompt adaptation from receipt parsing to resume data extraction

**Speech-to-Text (Web Speech API → Deepgram/Whisper upgrade path)**
- **Voice-First Interaction**: Multi-language voice recognition enabling hands-free resume creation
- **Accessibility**: Supports users with limited typing ability or visual impairments

**Advanced Data Science & Automation**
- **AI Agents**: Automated user onboarding, data validation, outcome tracking—enabling lean operations
- **Semantic Search (RAG)**: Vector database implementation for persistent knowledge base, enabling relevant accomplishment retrieval across sessions
- **Impact Analytics**: ML-driven outcome tracking (applications, interviews, placements, salary increases)

### Impact
This AI-driven approach enables:
- **95% cost reduction** vs. traditional counseling ($150/hour → $5/user in API costs)
- **Multilingual accessibility** (7 languages simultaneously—impractical with human translators)
- **Rapid deployment** (idea to working prototype in months using Claude Code and Gemini for development)

Without AI, this service model would be economically infeasible for the target population.

---

## **5. SCOPE OF WORK & MAJOR MILESTONES**

**6-Month Demonstration Goal**: Serve 500 underrepresented job seekers, demonstrate 25% increase in job placement rates and 15% increase in starting salaries.

### Milestone 1: Foundation & Infrastructure (Months 1-2)

**Deliverables:**
- Core technical stack deployment (Next.js frontend, Python/FastAPI backend, Supabase database)
- AI integration: Claude API (conversation), Gemini OCR (resume parsing), Web Speech API (voice input)
- Partnership establishment: 3-5 workforce development centers or immigrant service organizations
- User recruitment: 100 beta users enrolled

**AI Advancement:**
- Conversational framework with multi-turn context maintenance
- OCR implementation (migrating proven Car Talker code—existing technology requiring only prompt adaptation)
- Basic multi-language voice recognition (English, Spanish initial deployment)

**Measurable Outcome:** Functional MVP enabling user account creation, conversation initiation, resume upload with OCR extraction.

---

### Milestone 2: Core AI Innovation Deployment (Months 3-4)

**Deliverables:**
- **AI Fact-Check Process**: Cross-references resume claims against what you said in conversations, helps you verify everything feels true and accurate
- **Remembers Your Story**: System that stores your accomplishments, skills, and experiences—come back a year later, it knows you
- **Multi-Language Expansion**: Full 7-language rollout (Spanish, Vietnamese, Mandarin, Tagalog, Arabic, French, Haitian Creole)
- **Smart Import Parser**: Extraction of structured accomplishments/skills from pasted ChatGPT/Claude conversations
- User base expansion: 300 total users (cumulative)

**AI Advancement:**
- **AI Fact-Check**: Conservative flagging (only flags when something doesn't quite match), user-friendly verification interface
- **Story Persistence**: Remembers your career story, enables "you already know me" experience for return visits
- **Cultural Translation**: Context-aware translation layer preserving cultural authenticity while adapting to US professional norms
- **Conversation Parser**: NLP extraction of accomplishments, skills, metrics from unstructured AI conversation data

**Measurable Outcome:** All 4 differentiating features operational, validated through user testing, with initial feedback incorporated.

---

### Milestone 3: ATS Optimization & Resume Generation (Month 5)

**Deliverables:**
- Resume generation engine with platform-specific ATS rules (leveraging existing 2,350-line optimization guide)
- Job posting analysis AI (keyword extraction, ATS platform detection via URL patterns)
- Export functionality (PDF via WeasyPrint, DOCX via python-docx)
- Visual editor for user customization
- User base target achieved: 500 total users

**AI Advancement:**
- **Job Analysis AI**: Automated keyword extraction and strategic integration without "stuffing"
- **ATS Detection**: Platform identification enabling application of specific formatting rules
- **Format Optimization**: Automated application of Workday/Greenhouse/Lever/Taleo/iCIMS-specific requirements

**Measurable Outcome:** Resume generation functional for all major ATS platforms, validated through test submissions to real job postings.

---

### Milestone 4: Impact Measurement & Demonstration Readiness (Month 6)

**Deliverables:**
- Comprehensive outcome data collection (job applications, interview rates, placements, starting salaries)
- User satisfaction assessment (NPS, qualitative testimonials)
- Impact analysis validating 25% application success increase, 15% salary increase
- Demo Day presentation preparation (live platform demonstration, impact data visualization, user testimonial compilation)

**AI Advancement:**
- **Automated Outcome Tracking**: ML-powered follow-up surveys, data aggregation, impact calculation
- **Analytics Dashboard**: Correlation analysis between resume features and success outcomes

**Measurable Outcome:**
- 500 users served
- $1.875M estimated lifetime earnings increase (500 users × $3,750 average annual increase)
- 10-15 detailed user case studies
- Platform demonstration-ready

---

### Technology-Enabled Efficiency Comparison

| Milestone | Traditional Approach | AI-Enabled Approach | Efficiency Gain |
|-----------|---------------------|---------------------|-----------------|
| **Foundation** | Manual resume review by counselors ($150/hour × 2 hours = $300/user) | Automated conversation + OCR ($5/user in API costs) | **98% cost reduction** |
| **Innovation** | Impossible—human translators unavailable 24/7, fact-checkers cost-prohibitive | AI enables multi-language, truth verification, knowledge persistence at scale | **Unlocks new capabilities** |
| **ATS Optimization** | Expert knowledge required ($200/resume for professional services) | AI applies 2,350-line rulebook automatically | **99% cost reduction** |
| **Impact Measurement** | Manual surveys, weeks of data entry | Automated tracking, real-time analytics | **90% time reduction** |

**Bottom Line**: AI transforms a high-cost ($300/user), low-scale (limited by counselor availability), slow service (weeks turnaround) into a low-cost ($5/user), high-scale (thousands simultaneously), fast platform (hours turnaround) accessible to underrepresented populations.

---

## **6. DATA SOURCES**

### Publicly Available Data (No Privacy Concerns)

**ATS Optimization Rules**
- Source: Public documentation from Workday, Greenhouse, Lever, Taleo, iCIMS
- Format: Compiled into 2,350-line optimization guide covering formatting requirements, keyword strategies, platform-specific constraints
- Accessibility: Readily available, no legal/regulatory barriers

**LLM General Knowledge**
- Source: Claude, Gemini models trained on public internet data
- Application: Career advice, resume best practices, industry terminology
- Accessibility: API-based access via Anthropic (Claude), Google (Gemini)

---

### User-Generated Content (Privacy-Protected)

**Data Collected:**
- Conversations about your career story (10-15 minute sessions over time, like coffee break moments spread across a week)
- Uploaded resumes for OCR parsing (PDF, DOCX, images)
- Job postings (URLs or copy-paste) for keyword extraction
- Optional outcome data (applications submitted, interviews secured, job placements, starting salaries)

**Storage & Security:**
- Platform: Supabase (PostgreSQL database, SOC 2 Type II certified)
- Encryption: AES-256 at rest, TLS 1.3 in transit
- Backup: Daily automated backups with 30-day retention
- Location: US-based servers

**User Data Ownership:**
- Users retain 100% ownership of all data
- Export capability: All data downloadable in standard formats (PDF, CSV, JSON) at any time
- Deletion capability: One-click permanent deletion
- Data sharing: Zero sharing with employers, government entities, or third parties
- Data monetization: Revenue derived from user fees (sliding scale $0-20), not data sales
- AI training: User data NOT used to train public AI models

**Privacy & Regulatory Compliance:**
- ✅ GDPR compliant (European data protection regulation)
- ✅ CCPA compliant (California Consumer Privacy Act)
- ✅ Immigration status: Not collected (AI trained to redirect if mentioned)
- ✅ Voice recordings: Transcribed to text, original audio deleted within 48 hours
- ✅ Sensitive demographics: Optional for impact measurement only, never required
- ✅ Data portability: Users receive complete "data bucket" in digestible formats

---

### Outcome Data (Aggregated for Impact Measurement)

**Collection Method:**
- Optional in-app surveys (incentivized with gift cards)
- Partner organization tracking (workforce centers track placements for consenting users)
- Follow-up interviews 3-6 months post-resume creation

**Privacy Protection:**
- Aggregated reporting only (e.g., "500 users averaged $3,750 salary increase")
- Individual-level data never disclosed
- Stored separately from personally identifiable information (PII)
- Used exclusively for impact assessment and program improvement

---

### Legal & Ethical Considerations Addressed

**Immigration Status Concerns:**
- Explicit policy: Zero immigration status collection
- AI conversation redirection if user mentions immigration details
- No data sharing with government or immigration enforcement agencies
- Anonymous mode available (create resume without real name/contact until final export)

**Employer Access Concerns:**
- Users control all data sharing decisions
- Platform does not facilitate employer access
- Export-only model (user downloads, shares on their terms)

**Data Retention:**
- Active accounts: Data retained while account active
- Inactive accounts: Automated deletion after 1 year of inactivity
- User-initiated: Immediate permanent deletion upon request

---

### Data Governance Summary

| Data Type | Source | Storage | Privacy Protections | User Control |
|-----------|--------|---------|---------------------|--------------|
| **ATS rules** | Public docs | Backend database | N/A (public information) | N/A |
| **LLM knowledge** | Claude/Gemini APIs | External vendor | Vendor SOC 2 compliance | N/A |
| **User conversations** | User input | Supabase (encrypted) | Zero third-party sharing, no data sales | Export/delete anytime |
| **Resumes uploaded** | User files | Supabase (encrypted) | Zero third-party sharing, no data sales | Export/delete anytime |
| **Outcome data** | User surveys | Supabase (encrypted, anonymized) | Aggregated reporting only | Opt-in participation |

**Key Principle**: We function as data stewards, not data owners. Users maintain full ownership and control, with capability to export or permanently delete at any time.

---

## **7. TECHNICAL EXPERTISE**

### Internal Technical Capacity

**Evan Stoudt (Founder & Lead Developer)**

**Core Competencies:**
- Full-stack development: Next.js, React (frontend), Python/FastAPI (backend), Supabase (database)
- AI integration: Claude API, Gemini API (proven implementation in Car Talker project)
- Prompt engineering: Extensive experience optimizing LLM outputs for production use cases
- Rapid prototyping: Demonstrated ability to progress from concept to MVP in weeks (Car Talker, Implementation Tracker)
- Performance optimization: Track record of 60-95% improvements across multiple production systems
- Database design: PostgreSQL, structured/unstructured data modeling
- Cloud deployment: Vercel, Railway infrastructure management

**Capability Assessment:**
- **Demonstration Phase (6 months, 500 users)**: Internal expertise sufficient for MVP development and deployment
- **Scaling Phase (10K+ users)**: Will benefit from specialized advisory support in advanced NLP, production-scale architecture, security auditing

**Honest Limitations Acknowledged:**
- Advanced NLP techniques (semantic similarity algorithms, bias detection edge cases)
- Production-scale AI architecture (handling 100K+ concurrent users)
- Multilingual NLP edge cases (low-resource languages, dialect variations)
- AI security auditing (prompt injection prevention, adversarial input handling)

---

### External Advisory Support (Sought, Not Yet Contracted)

**1. AI/ML Technical Advisor**
- **Need**: Expert in production AI systems, multilingual NLP, bias mitigation
- **Ideal Profile**:
  - Experience deploying Claude/GPT at scale
  - Background in multilingual NLP and translation quality assurance
  - Expertise in AI ethics, fairness frameworks, bias detection
  - Familiarity with vector databases and RAG (Retrieval-Augmented Generation)
- **Source**: OpenAI technical support (through grant cohort), Anthropic Claude developer community, academic researchers
- **Engagement**: Advisory capacity (10 hours/month estimated)

**2. Workforce Development Subject Matter Expert**
- **Need**: Career counselor or workforce development professional to validate resume quality, conversation flow, impact measurement approach
- **Ideal Profile**:
  - 10+ years in workforce development or career services
  - Deep knowledge of barriers faced by immigrants, people of color, low-income job seekers
  - Understanding of ATS trends and employer expectations
  - Experience with outcome measurement in employment programs
- **Source**: Pilot partner organizations (workforce centers), National Association of Workforce Development Professionals (NAWDP)
- **Engagement**: Quarterly reviews, user testing participation

**3. Immigration & Language Access Expert**
- **Need**: Advisor on culturally responsive design for Limited English Proficiency (LEP) communities
- **Ideal Profile**:
  - Experience serving multilingual, immigrant populations
  - Understanding of cultural differences in professional communication norms
  - Expertise in language access, interpretation, translation quality standards
  - Knowledge of legal considerations (work authorization privacy, data protection)
- **Source**: Migration Policy Institute (MPI), National Immigration Law Center (NILC), local immigrant service organizations
- **Engagement**: Translation review (7 languages), cultural adaptation validation

---

### Approach: Lean Startup Model

**Current Structure:**
- Solo technical founder handles all development initially
- Leverage OpenAI cohort support (included in grant benefits)
- Recruit advisors as volunteers or via small stipends (not full consulting contracts)

**Scaling Phase Investment (if scaling grant secured):**
- Contract specialized firms for:
  - Security audit (penetration testing, privacy compliance review)
  - Translation quality assurance (native-speaker testing across 7 languages)
  - User research & UX design (testing with diverse demographic populations)

**No External Consulting Firm Currently Contracted**

**Key Point**: Internal expertise is sufficient for building and demonstrating the platform within the 6-month demonstration phase. We recognize the value of specialized advisors for scaling responsibly and are prepared to engage them as the project matures.

---

## **8. ETHICS AND BIAS**

### Core Problem: Systemic Bias in Traditional Resume Process

The existing resume and hiring system embeds structural bias that filters out qualified candidates from underrepresented backgrounds:

**Documented Bias Patterns:**
- **Language bias**: Non-native English speakers penalized for grammatical imperfections regardless of qualification level
- **Name bias**: Identical resumes with "ethnic-sounding" names receive 50% fewer callbacks than those with "white-sounding" names (field-tested research)
- **Cultural bias**: US resume conventions favor assertive self-promotion, conflicting with cultural values emphasizing humility (prevalent in many Asian, Latin American cultures)
- **Format bias**: ATS systems penalize creative layouts often used by candidates unfamiliar with corporate formatting norms
- **Credential bias**: "Degree required" filters exclude candidates with equivalent skills gained through alternative pathways

**Project Mission**: Center people of color, immigrants, and economically marginalized populations in design, ensuring AI empowers rather than replicates existing biases.

---

### Significant Ethical & Bias Concerns + Mitigation Strategies

#### **Concern 1: AI-Generated Content May Misrepresent User**

**Risk**: AI could exaggerate accomplishments, fabricate details, or mischaracterize user's experience, undermining truthfulness and user credibility.

**Mitigation:**
- ✅ **AI Fact-Check Process**: Cross-references every resume claim against what you actually said; flags anything that doesn't match for you to review and correct
- ✅ **User approval required**: All sections must be reviewed and explicitly approved before export
- ✅ **Edit control**: You can change any generated text; AI is your advisor, not the decision-maker
- ✅ **Transparency**: AI explains its phrasing choices ("I used 'led' because you mentioned managing the project")
- ✅ **Philosophy**: "Help people tell their truth better, not help them lie"

**Testing Approach**: Human reviewers compare sample resumes to conversation transcripts, verify claim accuracy, measure false positive rate.

---

#### **Concern 2: Gender-Coded Language**

**Risk**: AI might generate masculine-coded language (e.g., "aggressive," "dominant") or feminine-coded language (e.g., "collaborative," "supportive") based on perceived user gender, perpetuating stereotypes.

**Mitigation:**
- ✅ **Harvard Gender Decoder Integration**: All generated resumes tested for gender-coded words
- ✅ **Gender-neutral verb library**: AI trained on inclusive action verbs (leadership without gendered framing)
- ✅ **Blind demographic testing**: Generate resumes for identical experience with varied names (male/female, ethnic variations), verify consistent phrasing
- ✅ **DEI consultant review**: Quarterly audits by diversity, equity, inclusion experts

**Success Metric**: <5% gender-coded words in final resumes, zero statistical variance in tone by perceived gender.

---

#### **Concern 3: Racial Bias in Tone/Phrasing**

**Risk**: AI might generate different tones (assertive vs. humble) based on inferred race (e.g., from name or language spoken), perpetuating racial stereotypes.

**Mitigation:**
- ✅ **Comparative A/B testing**: Same experience data, different demographic indicators (names, languages) → verify phrasing consistency
- ✅ **User tone preference**: Users select preferred tone (assertive, humble, balanced)—not AI-assumed based on background
- ✅ **Diverse training data**: Resume examples from people of color, not exclusively dominant culture samples
- ✅ **Advisory board input**: Representatives from target communities (Black, Latinx, Asian, immigrant) review outputs, provide feedback

**Success Metric**: Zero statistically significant phrasing differences by race in controlled testing.

---

#### **Concern 4: Cultural Bias in "Professionalism" Standards**

**Risk**: "Professional" standards reflect dominant (white, corporate US) cultural norms; imposing these may erase authentic cultural identity or force assimilation.

**Mitigation:**
- ✅ **Cultural bridging approach** (not erasure):
  - Example: Vietnamese user states "We achieved X" (collective framing valued in Vietnamese culture)
  - AI translation: "Led team to achieve X" (individual leadership valued in US resumes)
  - Result: Bridges cultural gap while preserving authenticity of accomplishment
- ✅ **User education**: AI explains WHY US employers expect certain phrasing (empowering with knowledge, not forcing conformity)
- ✅ **Cultural advisors**: Native speakers from target language communities review translations for cultural authenticity
- ✅ **User choice**: "Culturally adapted" vs. "preserve original tone" option available

**Success Metric**: 90% user satisfaction with cultural respect in translations (measured via post-creation survey).

---

#### **Concern 5: Digital Divide & Accessibility Barriers**

**Risk**: Platform requiring internet access and devices may exclude most disadvantaged populations, replicating economic barriers.

**Mitigation:**
- ✅ **Partnership access model**: Pilot users access platform at workforce development centers (computers/internet provided by partner organizations)
- ✅ **Mobile-first design**: Optimized for smartphones (more accessible than laptops for low-income populations)
- ✅ **Low-bandwidth mode**: Functionality maintained on slow connections (rural areas, prepaid data plans)
- ✅ **Offline mode capability**: Draft resumes offline, sync when connectivity available
- ✅ **Screen reader compatibility**: WCAG 2.1 AA accessibility standards for visually impaired users
- ✅ **Keyboard navigation**: Full platform accessible without mouse

**Success Metric**: 95% of pilot users able to complete resume creation without technical barriers (tracked via partner feedback).

---

#### **Concern 6: Economic Access & Pricing Equity**

**Risk**: Fee structure may replicate economic barriers the project aims to address.

**Mitigation:**
- ✅ **Sliding scale pricing**: $0-20 based on self-reported ability to pay (honor system)
- ✅ **Organizational sponsorship**: Workforce centers, nonprofits can purchase "licenses" for clients (e.g., 30 licenses sponsor 30 users)
- ✅ **"Pay it forward" model**: Users who secure employment can sponsor another user
- ✅ **Free demonstration phase**: All 500 pilot users receive free access
- ✅ **Public benefit corporation structure**: Mission prioritization over profit maximization (legally binding)

**Philosophy**: "Getting a job is hard enough—don't make the tool a barrier."

---

#### **Concern 7: Privacy & Surveillance Fears (Vulnerable Populations)**

**Risk**: Immigrants, formerly incarcerated individuals, others with legitimate surveillance concerns may fear data misuse.

**Mitigation:**
- ✅ **Radical transparency**: Plain-language privacy policy available in all supported languages (not legal jargon)
- ✅ **Zero data sharing policy**: Explicit—no sharing with government, employers, immigration enforcement, any third parties
- ✅ **Anonymous mode**: Resume creation without real name/contact information until user-initiated export
- ✅ **Community endorsement**: Pilot partners (trusted community organizations) vouch for platform safety
- ✅ **Legal review**: Immigration attorneys review privacy practices, validate protections
- ✅ **User testimonials**: Early adopters from vulnerable populations share experiences (with permission)

**Success Metric**: >80% of users from vulnerable populations report feeling "safe" using platform (post-use survey).

---

### Bias Mitigation Testing Framework

| Bias Type | Testing Method | Success Metric | Verification Approach |
|-----------|----------------|----------------|----------------------|
| **Gender bias** | Harvard Gender Decoder + demographic A/B tests | <5% gender-coded words, no tone variance by gender | Quarterly automated testing + manual review |
| **Racial bias** | Name-based A/B testing (same experience, different names) | Zero phrasing variance by race | Statistical analysis of output consistency |
| **Cultural bias** | Cultural advisor review + user satisfaction surveys | 90% user satisfaction with cultural respect | Post-creation surveys, advisor feedback sessions |
| **Age bias** | Age-coded language scanner | Zero age-coded terms (e.g., "digital native," "seasoned") | Automated keyword scanning |
| **AI accuracy / no fabrication** | AI fact-check accuracy | 95% claim accuracy (verified against what you actually said) | Human review of flagged items, false positive tracking |

---

### Ethical Principles Guiding Development

1. **Center Marginalized Voices**: Design WITH people of color, immigrants, low-income users—not FOR them (participatory design approach)
2. **Transparency**: Users understand how AI works, what data is used, why recommendations are made
3. **User Agency**: AI advises, you decide—we never force AI outputs without your confirmation
4. **Authentic Over Impressive**: Help users present their authentic selves truthfully, not fabricate impressive-sounding narratives
5. **Privacy as Default**: Minimal data collection, maximum user control
6. **Accessibility First**: Design for lowest-resourced users (slow internet, older devices, limited English proficiency)

---

### Ongoing Bias Monitoring (Post-Launch)

- **Monthly bias audits**: Automated scanning of resume outputs for coded language
- **Quarterly diversity reviews**: External DEI consultant analyzes user outcomes by demographic
- **User feedback loop**: In-app bias reporting mechanism, weekly review of flagged instances
- **Advisory board meetings**: Quarterly sessions with community representatives to review concerns
- **Continuous improvement**: Bias findings immediately incorporated into prompt engineering, training data updates

---

**Bottom Line**: This project exists BECAUSE AI has potential to reduce bias in hiring—but only if bias mitigation is core architecture, not afterthought. We're intentional about preventing harm, transparent about limitations, and committed to centering the communities we aim to serve.

---

**END OF APPLICATION ANSWERS**

---

**Status**: Ready for submission
**Voice**: Formal technical writing (per FORMAL_WRITING_GUIDE.md)
**Compliance**: All answers match grant application requirements
**Contact Info Needed**: LinkedIn URL, email, phone, organization name/EIN

**Next Step**: Copy-paste into online application form by Oct 31, 5:00 PM PT
