# CLAUDE.md - [PROJECT_NAME]

This file provides guidance to Claude when working with the [PROJECT_NAME] project.

## 🔴 CRITICAL RULES

### Never Push Without Permission
- **NEVER run `clasp push` without explicit permission**
- After ANY code changes, ask: "Should I push these files?"
- Wait for explicit approval: "yes", "y", "sure", or "please"
- Show what files will be pushed before asking

**EXCEPTION: Automatic Initial Project Setup**
When setting up a NEW time tracking project and .clasp.json has "YOUR_SCRIPT_ID_HERE":
- Can automatically run `clasp create` without asking
- Can automatically run initial `clasp push` without asking
- This ONLY applies to initial setup, not code changes

## Project Overview

**Client**: [CLIENT_NAME]
**Type**: [PROJECT_TYPE]
**Status**: Active Development
**Started**: [DATE]

**Purpose**: [PROJECT_PURPOSE]

## Technology Stack

- **Primary**: [PRIMARY_TECH]
- **UI**: [UI_LAYER]
- **Time Zone**: America/Chicago
- **Version Control**: Git + [ADDITIONAL]

## 🤖 Your Development Team (Multi-Agent System)

This project includes a specialized multi-agent development team. Use these agents for focused expertise:

### Team Roster

**Theo (CTO)** - `theo-cto`
- Architecture design and technical decisions
- Code review and quality assurance
- Use when: Planning architecture, reviewing code, technical trade-offs

**Xavier (UX Lead)** - `xavier-ux`
- User experience and interface design
- Wireframes, flows, and design systems
- Use when: Designing user flows, creating component specs, accessibility planning

**Brian (Brand Director)** - `brian-brand`
- Brand voice and messaging
- User-facing content and copy
- Use when: Writing landing pages, error messages, microcopy, marketing content

**Randy (Researcher)** - `randy-researcher`
- Deep research and documentation
- Best practices and competitive analysis
- Use when: Researching libraries, finding implementation patterns, technical investigation

**Bailey (Backend Dev)** - `bailey-backend`
- Server-side implementation
- APIs, databases, business logic
- Use when: Building APIs, database work, server-side features

**Finn (Frontend Dev)** - `finn-frontend`
- UI implementation
- Client-side code and interactions
- Use when: Implementing components, building UIs, frontend features

### Quick Usage Patterns

**New Feature:**
```
"I need user authentication:

Theo - design the auth architecture
Randy - research authentication best practices
Bailey - implement the backend auth system
Xavier - design the login/signup UI
Brian - write the copy for auth flows
Finn - implement the auth UI"
```

**Bug Fix:**
```
"There's a performance issue:

Theo - diagnose the bottleneck
Bailey/Finn - implement the fix"
```

**Research Question:**
```
"Randy, research real-time update strategies for dashboards"
```

See `AGENTS_QUICK_REFERENCE.md` for detailed usage patterns and workflows.
See `AGENT_TEAM_ARCHITECTURE.md` for complete system documentation.

## Available Tools & Integrations

### Gemini OCR (Universal Document Processing)
**Built-in and ready to use** - No setup required!

When user asks to OCR a document/image/PDF:
- See `GEMINI_OCR_GUIDE.md` for complete usage
- API key is built-in (no configuration needed)
- Supports: JPG, PNG, PDF, HEIC, WebP
- Use cases: receipts, invoices, contracts, forms, IDs, screenshots
- Fallback: Claude vision if Gemini fails

**Quick start:**
```bash
# Install once per project
npm install @google/generative-ai

# Copy template and run
cp templates/gemini-ocr/gemini-ocr-client.js .
node gemini-ocr-client.js document.jpg
```

**For technical patterns:**
- See `research_context/GEMINI_OCR_PATTERNS.md`
- Code templates in `templates/gemini-ocr/`

## Communication Styles

### Email Communication
When drafting emails, use appropriate style:
- **Casual/Quick**: See `EVAN_EMAIL_STYLE.md` - "Hiya," progressive disclosure
- **Formal/Professional**: See `FORMAL_WRITING_GUIDE.md` - structured proposals

### Documentation
- **README files**: Use formal guide for public projects
- **Code comments**: Direct and casual
- **Technical proposals**: Use formal guide with metrics

## Session Logging

### ⚠️ TIME TRACKING ACCURACY
**CRITICAL**: When logging sessions, ALWAYS:
- Ask for exact start/end times if not specified
- Never estimate or make up times
- If unsure, ask: "What time did this session run?"
- Be precise with duration calculations
- Note any personal/non-billable time explicitly

### When User Says "Log Session"
1. Check for SESSION_CURRENT.json
2. Run finalize-session.sh
3. Add to knownSessions array in menu-system.gs
4. Create dynamic function handler
5. Push to Google Apps Script
6. User refreshes spreadsheet menu

## Development Workflow

### Starting a Session
```bash
cd [PROJECT_DIR]
./start-session.sh "[PROJECT_NAME]" "Feature description"

# During work
log add "implemented feature X"
log fixed "resolved issue Y"
log pattern "used batch processing pattern"
log status
```

### Making Changes
1. Edit files locally
2. Test logic mentally or in comments
3. Ask: "Should I push these files?"
4. Upon approval: `[PUSH_COMMAND]`
5. Report: "✅ Pushed! Now you can run functionName() from filename.gs"

## Key Patterns to Use

### From Our Knowledge Base

#### 1. 3-Button Pattern (for long operations)
If any operation might take >2 minutes, break into steps

#### 2. Warehouse Pattern (if data >10k rows)
Implement 3-sheet pattern: [Historical], [Current], [All]

#### 3. BYROW/LAMBDA (for formula optimization)
Replace repeated formulas with array processing

#### 4. Batch Processing (for >1000 items)
Always wrap with timeout protection (5.5 minutes max)

## Known Limits & Prevention

### Platform Limits
- **6-minute timeout**: Use batch processing
- **50k row performance**: Implement archival
- **20 trigger max**: Consolidate triggers

## Testing Procedures

### After Changes
1. [TEST_STEP_1]
2. [TEST_STEP_2]
3. Verify data saves correctly

## Important Notes

- Always use Chicago timezone
- Document patterns discovered
- Update this file with learnings
- Give filename at end of reports

## Pattern Library Reference

### 📚 Master Index (START HERE)
**`/project_kickoff/README.md`** - Comprehensive catalog of ALL 33+ pattern files
- Complete knowledge base with descriptions
- Organized by category (Core Systems, Quick Reference, Revolutionary Discoveries)
- When you need a pattern, check README.md first

### 📂 Local Guides (Copied to This Project)
- `EVAN_EMAIL_STYLE.md` - Casual communication patterns
- `FORMAL_WRITING_GUIDE.md` - Professional documentation style
- `GEMINI_OCR_GUIDE.md` - Universal document OCR integration

### ⚡ Quick Links (Frequently Used Patterns)
- `/project_kickoff/QUICK_PATTERNS_CHEATSHEET.md` - One-page quick reference
- `/project_kickoff/BYROW_LAMBDA_REVOLUTION.md` - Formula optimization patterns
- `/project_kickoff/SCALE_DECISION_TREE.md` - Architecture decisions
- `/project_kickoff/ANTI_PATTERNS.md` - What NOT to do (learn from mistakes)
- `/project_kickoff/DEBUGGING_WORKFLOW.md` - Systematic debugging approach
- `/project_kickoff/FORM_GENERATION_PATTERN.md` - Dynamic form creation
- `/project_kickoff/PATTERN_AUTOMATION_SCRIPTS.md` - Automation tools
- `/project_kickoff/LIMITS_REPOSITORY.md` - Platform limits and workarounds
- `/project_kickoff/CLIENT_PATTERNS.md` - Client-specific requirements

**Note:** If you don't find what you need in Quick Links, the full library is in README.md

---

*Last Updated: [DATE]*
*Version: 1.0.0*