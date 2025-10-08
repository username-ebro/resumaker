# Build Autonomy Agreement

**Date**: October 6, 2025
**Status**: Awaiting Evan's approval
**Purpose**: Enable autonomous building without constant check-ins

---

## 🎯 The Goal

**Claude builds the entire MVP autonomously**, only stopping for:
1. Critical architectural decisions that change scope
2. Blocker issues that prevent progress
3. Completion milestones (end of each phase)

**NOT stopping for**:
- Minor code decisions
- Styling choices
- Error troubleshooting
- Dependency installation
- File structure adjustments
- Algorithm tweaks
- Bug fixes
- Refactoring

---

## ✅ Pre-Approved Decisions

### I Have Permission To:

**1. Make All Technical Decisions**
- ✅ Choose specific libraries/packages (as long as they fit the tech stack)
- ✅ Decide exact file/folder names
- ✅ Pick CSS frameworks/styling approaches
- ✅ Choose state management patterns
- ✅ Design API endpoint structures
- ✅ Select TypeScript vs JavaScript for specific files
- ✅ Pick testing frameworks
- ✅ Choose linting/formatting configs

**2. Fix Problems Independently**
- ✅ Debug and fix errors without asking
- ✅ Troubleshoot dependency conflicts
- ✅ Resolve merge conflicts
- ✅ Fix type errors
- ✅ Handle CORS issues
- ✅ Resolve database connection issues
- ✅ Fix authentication bugs
- ✅ Adjust environment configurations

**3. Refactor & Improve**
- ✅ Refactor code for clarity/performance
- ✅ Extract reusable components
- ✅ Add error handling
- ✅ Improve user experience (within scope)
- ✅ Add loading states
- ✅ Implement proper logging
- ✅ Optimize queries

**4. Make Minor Scope Adjustments**
- ✅ Add helpful utility functions
- ✅ Include reasonable validation
- ✅ Add sensible defaults
- ✅ Improve error messages
- ✅ Add basic accessibility features
- ✅ Include helpful UI feedback

**5. Manage Development Workflow**
- ✅ Install npm/pip packages as needed
- ✅ Run migrations
- ✅ Create seed data
- ✅ Write tests
- ✅ Use TodoWrite to track progress
- ✅ Update CHANGELOG.md
- ✅ Git commit with good messages (but DON'T push without asking)

---

## 🚫 What I CANNOT Do Without Asking

### I Must Stop and Ask For:

**1. Scope Changes**
- ❌ Adding major features not in MVP_SCOPE_FINAL.md
- ❌ Removing P0 features
- ❌ Changing core architecture (Next.js → something else)
- ❌ Switching databases (Supabase → something else)
- ❌ Major UX paradigm shifts

**2. Cost-Incurring Decisions**
- ❌ Purchasing paid services
- ❌ Upgrading to paid API tiers
- ❌ Adding paid dependencies
- ❌ Deploying to production (costs money)

**3. Security/Privacy Changes**
- ❌ Changing authentication approach fundamentally
- ❌ Storing sensitive data differently than planned
- ❌ Exposing API keys or credentials
- ❌ Changing data retention policies

**4. External Integrations**
- ❌ Adding new third-party services not in plan
- ❌ Integrating with external APIs not specified
- ❌ Adding analytics/tracking without approval

---

## 📋 Autonomous Build Protocol

### How I'll Work:

**1. Use TodoWrite Religiously**
- Create todo list at start of each phase
- Mark tasks in_progress when working
- Mark completed immediately when done
- You can check progress anytime

**2. Document As I Go**
- Update CHANGELOG.md with significant changes
- Comment code thoroughly
- Create README files for complex features
- Document any deviations from plan

**3. Communicate Progress at Milestones**
```
After each phase completion:
- "✅ Phase X Complete: [summary]"
- "Built: [features]"
- "Tested: [what works]"
- "Ready for Phase X+1"
```

**4. Ask Only When Blocked**
```
If truly stuck after trying:
- "🚨 BLOCKED: [issue]"
- "Tried: [solutions attempted]"
- "Need decision: [options]"
```

**5. Handle Errors Autonomously**
```
When error occurs:
1. Read error message
2. Try 2-3 solutions
3. If fixed → continue
4. If not fixed after 3 attempts → document and ask
```

---

## 🎯 Build Execution Plan (Autonomous)

### Phase 1: Foundation (8-10 hours)
**I will:**
- Create backend (FastAPI) and frontend (Next.js) projects
- Set up .env files with your credentials
- Configure Supabase client (MCP + direct connection)
- Create all 14 database tables via migrations
- Test database connections
- Build authentication (login/signup/logout)
- Create basic UI shell
- Set up routing

**I will NOT ask about:**
- Exact component names
- CSS approach (Tailwind assumed)
- Folder structure details
- Package versions

**I WILL ask if:**
- Database migrations fail completely (after trying fixes)
- Authentication approach needs fundamental change

**When done:**
- "✅ Phase 1 Complete: Auth working, DB connected, basic UI ready"

---

### Phase 2: Data Collection (18-22 hours)
**I will:**
- Build ChatGPT/Claude import parser
- Integrate Gemini OCR (from Car Talker)
- Create conversation system (text + voice)
- Build reference request system
- Create knowledge base UI
- Test all data collection flows

**I will NOT ask about:**
- Parsing algorithm details (I'll use Claude API intelligently)
- OCR prompt refinement (I'll iterate)
- UI component styling
- Form validation approaches

**I WILL ask if:**
- OCR accuracy is fundamentally broken (< 50%)
- Import parser can't extract data at all
- Voice recording doesn't work in any browser

**When done:**
- "✅ Phase 2 Complete: 4 data collection methods working, knowledge base populated"

---

### Phase 3: Resume Generation (12-15 hours)
**I will:**
- Build resume generator from knowledge base
- Implement job targeting + keyword extraction
- Create truth verification system
- Build ATS optimization using guide
- Test generation flow

**I will NOT ask about:**
- Resume template details (I'll use ATS guide)
- Truth check flagging thresholds (I'll use conservative)
- Keyword matching algorithms
- Formatting specifics

**I WILL ask if:**
- Truth check generates 50+ flags (broken)
- Resume generator produces gibberish
- ATS optimization can't parse job descriptions

**When done:**
- "✅ Phase 3 Complete: Resume generation working, truth check functional, ATS-optimized"

---

### Phase 4: Output (10-12 hours)
**I will:**
- Build basic visual editor
- Implement PDF export (WeasyPrint)
- Implement DOCX export (python-docx)
- Create download functionality
- Test all export formats

**I will NOT ask about:**
- Visual editor UI details
- PDF styling specifics
- DOCX formatting choices

**I WILL ask if:**
- WeasyPrint or python-docx won't install
- PDF/DOCX exports are completely broken
- Visual editor is unusable

**When done:**
- "✅ Phase 4 Complete: Editor working, PDF/DOCX export functional"

---

### Phase 5: Testing & Deploy (6-8 hours)
**I will:**
- Write integration tests
- Fix bugs found during testing
- Prepare deployment configs
- Create deployment documentation

**I will NOT ask about:**
- Test coverage percentages
- Specific test cases
- Bug fix approaches

**I WILL ask if:**
- Major architectural flaw discovered
- Deployment requires paid services
- Security vulnerability found

**When done:**
- "✅ Phase 5 Complete: Tested, deployment ready, documentation complete"

---

## 🤖 Autonomous Troubleshooting Protocol

### When I Hit an Error:

**Step 1: Analyze (30 seconds)**
- Read error message carefully
- Identify root cause
- Check if it's a known issue

**Step 2: Attempt Solutions (2-3 tries)**
```
Try in order:
1. Most obvious fix (typo, import, etc.)
2. Stack Overflow / documentation solution
3. Alternative approach
```

**Step 3: Document if Fixed**
```
# CHANGELOG.md
- Fixed: [issue] by [solution]
```

**Step 4: Ask Only if Still Blocked**
```
After 3 failed attempts:
"🚨 BLOCKED: [error]
Tried: [solution 1], [solution 2], [solution 3]
Need: [decision or help]"
```

### Examples:

**Error I Handle Autonomously:**
```
❌ "Module not found: 'fastapi'"
✅ Solution: pip install fastapi
✅ Action: Install and continue
✅ Document: Added fastapi to requirements.txt
```

**Error I Ask About:**
```
❌ "Supabase connection refused (tried 3 different approaches)"
🚨 BLOCKED: Cannot connect to Supabase
Tried: MCP, direct connection, different poolers
Need: Check if Supabase project is paused or credentials changed
```

---

## 📊 Progress Tracking (TodoWrite)

### I Will Maintain Todo List Like This:

**Start of Phase:**
```
TodoWrite:
- [ ] Setup FastAPI project (pending)
- [ ] Setup Next.js project (pending)
- [ ] Configure environment variables (pending)
- [ ] Create database migrations (pending)
- [ ] Build authentication (pending)
```

**During Work:**
```
TodoWrite:
- [x] Setup FastAPI project (completed)
- [x] Setup Next.js project (completed)
- [IN_PROGRESS] Configure environment variables
- [ ] Create database migrations (pending)
- [ ] Build authentication (pending)
```

**You Can Check Anytime:**
- Just ask "What's the progress?" or "Show me the todos"
- I'll show current todo list with statuses

---

## 🎯 What You Approve By Saying "YES"

By approving this agreement, you give me permission to:

1. ✅ **Build autonomously** through all 5 phases
2. ✅ **Make technical decisions** within scope
3. ✅ **Fix errors and bugs** without asking
4. ✅ **Refactor and improve** code quality
5. ✅ **Install packages** as needed
6. ✅ **Create files/folders** following best practices
7. ✅ **Write and run tests**
8. ✅ **Update documentation**
9. ✅ **Use TodoWrite** to track progress
10. ✅ **Commit to git** (but NOT push without approval)

**I will STOP and ASK only for:**
- ❌ Scope changes
- ❌ Cost decisions
- ❌ Security/privacy changes
- ❌ True blockers (after 3 fix attempts)
- ❌ Phase completions (milestone check-ins)

---

## 🚀 How To Activate Autonomous Mode

**Just say ONE of these:**

### Option 1 (Simple):
> "Approved. Build autonomously."

### Option 2 (Explicit):
> "I approve the Build Autonomy Agreement. Build all 5 phases autonomously, only stopping for blockers or phase completions."

### Option 3 (Custom):
> "Approved, but also stop for [specific thing I want to review]"

---

## 📝 What I'll Say When Done

**After Each Phase:**
```
✅ Phase X Complete

Built:
- [Feature 1] - working
- [Feature 2] - working
- [Feature 3] - working

Tested:
- [What I tested and confirmed]

Issues:
- [Any minor issues, if relevant]

Ready for Phase X+1? (or "Final Build Complete" for Phase 5)
```

---

## 🎯 TL;DR - What You're Approving

**You approve me to:**
- Build entire MVP (55-60 hours) autonomously
- Make all technical decisions within scope
- Fix errors/bugs without asking
- Only stop for: blockers, scope changes, or phase completions
- Track progress with TodoWrite
- Check in at end of each phase

**You'll know progress because:**
- Todo list always updated
- CHANGELOG.md tracks changes
- I report at phase completions
- You can ask "status?" anytime

---

## ✅ Activation Command

**To activate autonomous build mode, just say:**

**"APPROVED - Build autonomously following BUILD_AUTONOMY_AGREEMENT.md"**

**Or simply:**

**"Approved. Go build."**

---

**Ready when you are, Evan.** 🚀

Once you approve, I'll start Phase 1 and won't stop until it's done (or I hit a blocker).

**Your call!** 💪
