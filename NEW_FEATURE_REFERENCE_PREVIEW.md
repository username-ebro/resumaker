# New Feature: Reference Preview System

**Date**: October 6, 2025
**Priority**: P1 (Post-Core MVP, Pre-Launch)
**Status**: Documented, Ready for Implementation

---

## Feature Overview

**What It Does**: Generate a shareable prompt/link for friends, colleagues, and former managers to provide feedback about the user's work, which gets incorporated into the resume.

**User Value**:
- Gets external validation of accomplishments
- Discovers achievements they forgot or downplayed
- Adds credibility with third-party perspectives
- Enriches knowledge base with reference stories

---

## User Flow

### Step 1: User Initiates Reference Request

**From Dashboard/Knowledge Base**:
```
User clicks: "Get Input from References"

System prompts:
- What role are you applying for?
- Who should we ask? (colleague, manager, client, etc.)
- What aspects do you want feedback on?
  □ Accomplishments
  □ Skills
  □ Work style
  □ Leadership
  □ Technical expertise
  □ Specific projects
```

### Step 2: System Generates Shareable Prompt

**Two Options Generated**:

#### Option A: Copy-Paste Text (No Login Required)
```
Hey [Name],

I'm using an app called Resumaker to put together a new resume. I'm
trying to get [target role] and would really value your input.

Could you answer these questions about working with me?

1. What accomplishments of mine stand out to you?
2. What skills did you see me demonstrate effectively?
3. Can you describe a specific project or moment where I made an impact?
4. What would you say are my professional strengths?
5. [Custom question based on user's target role]

You can either:
- Reply to this message with your thoughts
- Use this link to submit directly: [short link]

Thanks so much!
[User's name]
```

#### Option B: Direct Link (Guided Form)
```
https://resumaker.app/r/abc123

Opens to:
- Brief intro: "Evan asked for your input on their resume"
- 5-7 targeted questions
- Optional: Record audio response (like Storyworth)
- Submit → Data goes to Evan's knowledge base
```

### Step 3: Reference Provides Input

**Via Copy-Paste**:
- Reference replies to message/email
- User pastes response into Resumaker
- System parses and extracts key points

**Via Link**:
- Reference clicks link
- No login required (public, temporary link)
- Fills out form (text or voice)
- Submits
- User gets notification

### Step 4: System Processes Reference Data

**Extraction**:
- Parse reference response
- Identify:
  - Specific accomplishments mentioned
  - Skills validated by third party
  - Stories/anecdotes
  - Quantifiable results the user forgot
  - Strengths/qualities noted
- Tag as `source: reference`
- Store in `user_knowledge_base`

**Truth Check Enhancement**:
- Reference data = strong evidence
- Claims validated by references get higher confidence scores
- Can cite references in resume: "Recognized by leadership for..."

### Step 5: User Reviews & Incorporates

**Dashboard View**:
```
📬 New Reference Input from Sarah Johnson (Former Manager)

Highlights extracted:
✅ "Evan consistently exceeded quarterly targets by 30-40%"
✅ "One of the best project managers I've worked with"
✅ "Led the migration to microservices - saved us $500K annually"
✅ "Excellent at explaining technical concepts to non-technical stakeholders"

[Add to Resume] [Save to Knowledge Base] [Edit]
```

**User Actions**:
- Accept extracted points
- Edit for clarity/fit
- Add to specific resume sections
- Save for future use

---

## Technical Implementation

### Database Schema Addition

```sql
-- Reference Requests
CREATE TYPE reference_request_status AS ENUM (
  'pending',
  'partially_complete',
  'complete',
  'expired'
);

CREATE TABLE reference_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,

  -- Request Details
  target_role TEXT, -- What job user is applying for
  reference_type TEXT, -- colleague, manager, client, etc.
  custom_questions JSONB, -- User-selected or custom questions

  -- Sharing
  share_token TEXT UNIQUE, -- Short code for link (e.g., 'abc123')
  share_url TEXT, -- Full shareable URL
  copy_paste_template TEXT, -- Pre-formatted message

  -- Status
  status reference_request_status DEFAULT 'pending',
  responses_received INT DEFAULT 0,

  -- Tracking
  created_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ, -- Links expire after 30 days
  last_reminder_sent TIMESTAMPTZ,

  CONSTRAINT valid_token CHECK (LENGTH(share_token) = 8)
);

CREATE INDEX idx_ref_requests_user ON reference_requests(user_id);
CREATE INDEX idx_ref_requests_token ON reference_requests(share_token);

-- Reference Responses
CREATE TYPE response_method AS ENUM (
  'link_text',
  'link_audio',
  'copy_paste',
  'manual_entry'
);

CREATE TABLE reference_responses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  request_id UUID REFERENCES reference_requests(id) ON DELETE CASCADE,
  user_id UUID REFERENCES auth.users(id), -- Owner of the resume

  -- Reference Info
  reference_name TEXT,
  reference_email TEXT,
  reference_relationship TEXT, -- manager, colleague, client, etc.

  -- Response Content
  response_method response_method NOT NULL,
  raw_response TEXT NOT NULL, -- Original text/transcript
  audio_url TEXT, -- If voice response

  -- Extracted Data
  extracted_data JSONB, -- Parsed accomplishments, skills, stories
  items_extracted INT DEFAULT 0,

  -- Processing
  processed BOOLEAN DEFAULT FALSE,
  added_to_knowledge_base BOOLEAN DEFAULT FALSE,

  -- Metadata
  submitted_at TIMESTAMPTZ DEFAULT NOW(),
  ip_address TEXT,
  user_agent TEXT
);

CREATE INDEX idx_ref_responses_request ON reference_responses(request_id);
CREATE INDEX idx_ref_responses_user ON reference_responses(user_id);

-- Add to user_knowledge_base (extend existing table)
ALTER TABLE user_knowledge_base
  ADD COLUMN reference_response_id UUID REFERENCES reference_responses(id),
  ADD COLUMN reference_name TEXT,
  ADD COLUMN reference_relationship TEXT;

-- Update knowledge_source enum
ALTER TYPE knowledge_source ADD VALUE 'reference';
```

### API Endpoints

```python
# backend/api/references.py

@router.post("/references/create")
async def create_reference_request(
    user_id: str,
    target_role: str,
    reference_type: str,
    custom_questions: List[str] = None
):
    """
    Create new reference request
    Returns: share_token, share_url, copy_paste_template
    """
    pass

@router.get("/references/{share_token}")
async def get_reference_form(share_token: str):
    """
    Public endpoint (no auth required)
    Returns: Form questions for reference to fill out
    """
    pass

@router.post("/references/{share_token}/submit")
async def submit_reference_response(
    share_token: str,
    reference_name: str,
    reference_email: str,
    reference_relationship: str,
    responses: Dict[str, str]
):
    """
    Public endpoint (no auth required)
    Submit reference response via link
    """
    pass

@router.post("/references/parse-paste")
async def parse_pasted_reference(
    user_id: str,
    reference_name: str,
    reference_relationship: str,
    raw_text: str
):
    """
    Parse copy-pasted reference response
    Extract key points, add to knowledge base
    """
    pass

@router.get("/references/responses/{user_id}")
async def get_user_references(user_id: str):
    """
    Get all reference responses for user
    Returns: List of parsed responses with extracted data
    """
    pass
```

### Frontend Components

```typescript
// src/components/References/
// - ReferenceRequestWizard.tsx (create request flow)
// - ShareablePromptDisplay.tsx (show copy-paste text + link)
// - ReferenceForm.tsx (public form for references to fill)
// - ReferenceResponsesList.tsx (view received responses)
// - ExtractedDataReview.tsx (review & incorporate into resume)
// - ReferencePasteParser.tsx (paste text, parse, review)
```

### Question Bank for References

**General Questions** (always included):
1. What accomplishments of [User]'s stand out to you from your time working together?
2. What professional skills did you see [User] demonstrate most effectively?
3. Can you describe a specific project or moment where [User] made an impact?
4. What would you say are [User]'s greatest professional strengths?

**Role-Specific Questions** (based on target job):

**For Technical Roles**:
5. What technical skills or expertise did [User] bring to the team?
6. Can you describe [User]'s problem-solving approach?

**For Leadership Roles**:
5. How did [User] lead or manage projects/people?
6. What was [User]'s approach to stakeholder communication?

**For Creative Roles**:
5. What creative solutions or innovative ideas did [User] contribute?
6. How did [User] approach complex design/content challenges?

**For Sales/Business Roles**:
5. What business results or metrics stand out from [User]'s work?
6. How did [User] build relationships with clients/customers?

**Custom Question Option**:
- User can add 1-2 custom questions specific to their situation

---

## Smart Parsing Algorithm

### Reference Response Parser

**Input**: Raw text from reference (either pasted or submitted via form)

**Process**:

```python
def parse_reference_response(raw_text: str, user_id: str, reference_name: str) -> Dict:
    """
    Parse reference response and extract key data points
    """

    # Use Claude to extract structured data
    prompt = f"""
    Parse this professional reference about a job candidate:

    Reference text:
    {raw_text}

    Extract the following as structured JSON:

    1. accomplishments: List of specific achievements mentioned
       - Include any quantifiable results (%, $, numbers)
       - Include project names or initiatives

    2. skills: List of skills/competencies mentioned or implied
       - Technical skills
       - Soft skills
       - Domain expertise

    3. stories: Notable anecdotes or specific examples
       - What happened
       - What the candidate did
       - What the result was

    4. strengths: Professional qualities or traits highlighted

    5. impact_metrics: Any numbers, percentages, or quantifiable results
       - Extract the exact figures mentioned
       - Context for each metric

    6. quotes: Direct quotes that could be used in resume
       - Powerful phrases like "one of the best..." or "consistently exceeded..."

    7. themes: 3-5 word summary of major themes in the reference

    Return ONLY valid JSON.
    """

    claude_response = call_claude_api(prompt)
    extracted = json.loads(claude_response)

    # Assign confidence scores
    for accomplishment in extracted['accomplishments']:
        accomplishment['confidence'] = 0.9  # Reference = high confidence
        accomplishment['source'] = 'reference'
        accomplishment['reference_name'] = reference_name

    # Store in knowledge base
    for item_type, items in extracted.items():
        if item_type in ['accomplishments', 'skills', 'stories']:
            for item in items:
                store_in_knowledge_base(
                    user_id=user_id,
                    knowledge_type=item_type,
                    content=item,
                    source='reference',
                    verified=True,  # Reference = verified
                    confidence_score=0.9,
                    reference_name=reference_name
                )

    return extracted
```

**Example Input**:
```
Reference from Sarah Johnson (Manager):

"Evan was one of my best employees during his time at TechCorp. He
consistently exceeded quarterly targets by 30-40% and was instrumental
in our migration to microservices architecture, which saved the company
approximately $500K annually.

One specific example: Evan led a cross-functional team of 12 engineers
to deliver our largest client project 3 weeks ahead of schedule, which
helped us close a $2M renewal.

His ability to explain complex technical concepts to non-technical
stakeholders was exceptional. I'd hire him again in a heartbeat."
```

**Parsed Output**:
```json
{
  "accomplishments": [
    {
      "description": "Consistently exceeded quarterly targets",
      "metric": "30-40% above target",
      "confidence": 0.9,
      "source": "reference",
      "reference_name": "Sarah Johnson"
    },
    {
      "description": "Led microservices migration",
      "metric": "$500K annual savings",
      "impact": "Company cost reduction",
      "confidence": 0.9
    },
    {
      "description": "Led cross-functional team to deliver major client project",
      "metric": "3 weeks ahead of schedule",
      "team_size": "12 engineers",
      "business_impact": "Secured $2M renewal",
      "confidence": 0.9
    }
  ],
  "skills": [
    "Cross-functional team leadership",
    "Microservices architecture",
    "Technical communication",
    "Stakeholder management",
    "Project delivery"
  ],
  "stories": [
    {
      "situation": "Largest client project at risk",
      "action": "Led team of 12 engineers",
      "result": "Delivered 3 weeks early, secured $2M renewal",
      "theme": "Leadership under pressure"
    }
  ],
  "strengths": [
    "Consistently exceeds targets",
    "Technical leadership",
    "Communication (technical to non-technical)",
    "Project management"
  ],
  "impact_metrics": [
    "30-40% above quarterly targets",
    "$500K annual cost savings",
    "$2M client renewal secured",
    "3 weeks ahead of schedule"
  ],
  "quotes": [
    "One of my best employees",
    "I'd hire him again in a heartbeat",
    "Exceptional ability to explain complex technical concepts"
  ],
  "themes": [
    "Exceeds expectations",
    "Technical leadership",
    "Business impact",
    "Communication excellence",
    "Project delivery"
  ]
}
```

---

## Integration with Existing Features

### Truth Check Enhancement

**Before** (no references):
```
❌ "Increased revenue by 40%"
   ⚠️ You mentioned growth but didn't specify this percentage
   Confidence: LOW
```

**After** (with reference validation):
```
✅ "Exceeded quarterly targets by 30-40%"
   ✓ Validated by Sarah Johnson (Former Manager)
   Evidence: Reference response + conversation
   Confidence: HIGH
```

### Knowledge Base Display

**New Tab: "References" in Knowledge Base**:
```
📬 Reference Insights (3)

From Sarah Johnson (Manager at TechCorp):
  • "Consistently exceeded targets by 30-40%"
  • Led microservices migration → $500K savings
  • Delivered major project 3 weeks early
  [View Full Response] [Add to Resume]

From Mike Chen (Colleague):
  • "Best collaborator I've worked with"
  • Expert at Python and system design
  • Mentored 5 junior engineers
  [View Full Response] [Add to Resume]

[+ Request More References]
```

### Resume Generation

**Using Reference Data**:
- Quotes can be used in summary: "Recognized by leadership as..."
- Accomplishments get stronger wording (validated)
- Skills section can note: "Validated by former managers"
- Bullet points can incorporate reference stories

**Example Resume Bullet** (reference-enhanced):
```
Before:
• Led team to deliver client project

After (with reference data):
• Led cross-functional team of 12 engineers to deliver $2M client
  project 3 weeks ahead of schedule, recognized by management as
  instrumental to client retention
```

---

## UX Flow (Step-by-Step)

### 1. User Initiates Request

**Dashboard → References Tab → "Request Reference Input"**

**Wizard Step 1**: Who are you asking?
- [ ] Current/Former Manager
- [ ] Colleague/Peer
- [ ] Direct Report
- [ ] Client/Customer
- [ ] Other: _______

**Wizard Step 2**: What role are you targeting?
- Input: [Target job title]
- System suggests role-specific questions

**Wizard Step 3**: Choose questions (5-7 total)
- [x] What accomplishments stand out? (always included)
- [x] What skills did they demonstrate? (always included)
- [x] Specific project or moment of impact? (always included)
- [ ] Leadership approach? (optional)
- [ ] Technical expertise? (optional)
- [ ] Custom: _____________ (user can add)

**Wizard Step 4**: How will they respond?
- [ ] Send them a link (easiest for them)
- [ ] I'll copy-paste a message template

### 2. System Generates Shareable Assets

**Output Screen**:

**Option A: Copy-Paste Message**
```
[Copy to Clipboard]

Hey Sarah,

I'm using an app called Resumaker to put together a new resume
for Senior Product Manager roles and would really value your input.

Could you answer these questions about our time working together
at TechCorp?

1. What accomplishments of mine stand out to you?
2. What skills did you see me demonstrate effectively?
3. Can you describe a specific project where I made an impact?
4. How would you describe my leadership approach?
5. What are my greatest professional strengths?

You can reply here, or use this link: resumaker.app/r/xy7k2m9p

Thanks so much!
Evan
```

**Option B: Direct Link**
```
🔗 resumaker.app/r/xy7k2m9p

[Copy Link] [Send via Email] [Share]

This link is active for 30 days and doesn't require the reference
to create an account.
```

### 3. Reference Fills Out Form

**Public Page** (no login):

```
📝 Input Request from Evan Stoudt

Evan is putting together a resume for Senior Product Manager
roles and has asked for your input.

Your responses will help Evan highlight their experience and
accomplishments accurately. This should take about 5-10 minutes.

─────────────────────────────────

Your Information:
Name: [____________]
Email: [____________] (optional)
Relationship: [ Manager ▼ ]

─────────────────────────────────

Questions:

1. What accomplishments of Evan's stand out to you?
   [Text area - can also record audio ▶️ ]

2. What professional skills did you see Evan demonstrate effectively?
   [Text area]

3. Can you describe a specific project or moment where Evan made an impact?
   [Text area]

4. How would you describe Evan's leadership approach?
   [Text area]

5. What would you say are Evan's greatest professional strengths?
   [Text area]

─────────────────────────────────

[Submit] [Save Draft]
```

### 4. User Reviews Response

**Notification**: "📬 New reference response from Sarah Johnson"

**Dashboard → References → New Response**:

```
Reference Response from Sarah Johnson
Submitted: Oct 6, 2025 | Relationship: Former Manager

─────────────────────────────────

✨ AI-Extracted Highlights:

Accomplishments:
  ✅ "Consistently exceeded quarterly targets by 30-40%"
  ✅ "Led microservices migration saving $500K annually"
  ✅ "Delivered major client project 3 weeks early → $2M renewal"

Skills Mentioned:
  ✅ Cross-functional team leadership
  ✅ Microservices architecture
  ✅ Technical communication
  ✅ Stakeholder management

Powerful Quotes:
  💬 "One of my best employees"
  💬 "I'd hire him again in a heartbeat"
  💬 "Exceptional at explaining technical concepts to non-technical stakeholders"

─────────────────────────────────

[View Full Response] [Add All to Knowledge Base] [Select Items to Add]
```

### 5. Incorporate into Resume

**Knowledge Base → References Tab → Select Items**:

```
☑️ "Exceeded quarterly targets by 30-40%"
   → Add to: [Work Experience - TechCorp ▼]

☑️ "Led microservices migration → $500K savings"
   → Add to: [Work Experience - TechCorp ▼]

☑️ "Exceptional technical communication"
   → Add to: [Skills Section ▼]

[Add Selected to Resume] [Save to Knowledge Base for Later]
```

---

## Analytics & Insights

**For User**:
- Number of references requested vs. received
- Response rate
- Average time to response
- Most commonly mentioned skills/accomplishments
- Themes across multiple references

**Dashboard Widget**:
```
📊 Reference Insights

3 responses received from 4 requests (75% response rate)

Most Mentioned Strengths:
  1. Technical Leadership (3 mentions)
  2. Communication Skills (3 mentions)
  3. Exceeding Targets (2 mentions)

Top Validated Accomplishments:
  • Microservices migration
  • Project delivery excellence
  • Team leadership

[View All Responses]
```

---

## Implementation Priority

**Phase 1** (Core Feature):
- Reference request creation
- Shareable link generation
- Public response form
- Basic parsing & storage

**Phase 2** (Enhancement):
- Copy-paste template
- Audio responses
- Advanced parsing with Claude
- Truth check integration

**Phase 3** (Polish):
- Email reminders
- Response analytics
- Multi-reference comparison
- Auto-incorporation into resume

---

## Questions to Resolve

1. **Expiration**: How long should reference links be active?
   - Recommendation: 30 days (can extend if needed)

2. **Privacy**: What data do we show references about the user?
   - Recommendation: Only target role, their name, and questions (no resume preview)

3. **Anonymity**: Can references submit anonymously?
   - Recommendation: Name required, email optional

4. **Reminders**: Should we auto-remind references who haven't responded?
   - Recommendation: Yes, after 7 days (user can disable)

5. **Multiple References**: How many references can user request?
   - Recommendation: Unlimited for MVP, could limit to 5-10 for free tier later

---

## Success Metrics

**Adoption**:
- % of users who request at least 1 reference
- Average # of reference requests per user

**Engagement**:
- Reference response rate (target: 60%+)
- Average response time
- % of users who incorporate reference data into resume

**Quality**:
- # of knowledge base items added from references
- % of reference-sourced claims that pass truth check
- User satisfaction with reference feature

---

**Status**: Fully documented, ready for implementation after core MVP
**Build Time Estimate**: 12-15 hours (end-to-end)
**Value Proposition**: Transforms resume from self-reported to validated by others
