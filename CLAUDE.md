# CLAUDE.md - Resumaker

This file provides guidance to Claude when working with the Resumaker project.

## Project Overview

**Client**: Personal/Portfolio
**Type**: Full-Stack Web Application (Python + Next.js)
**Status**: Active Development
**Started**: October 6, 2025

**Purpose**: AI-powered resume builder helping job seekers create professional resumes through intelligent automation and structured data management.

## Technology Stack

- **Backend**: Python (FastAPI)
- **Frontend**: Next.js, React, TypeScript
- **Database**: Supabase (PostgreSQL)
- **AI/ML**: Resume generation, job matching
- **PDF Generation**: WeasyPrint
- **Deployment**: Railway (backend), Vercel (frontend)
- **Testing**: Python pytest, integration tests
- **Time Zone**: America/Chicago
- **Version Control**: Git

## 🎯 Your Development Team

You have a specialized multi-agent team ready to help with complex development tasks:

| Agent | Role | Call When You Need... |
|-------|------|----------------------|
| **Theo** | CTO | Architecture, code review, technical decisions |
| **Xavier** | UX Lead | User flows, design specs, wireframes |
| **Brian** | Brand Director | Copy, messaging, content |
| **Randy** | Researcher | Deep research, documentation, best practices |
| **Bailey** | Backend Dev | APIs, databases, server logic |
| **Finn** | Frontend Dev | UI components, client-side code |

### Quick Usage Patterns

**Simple task (single agent):**
```
"Randy, research the best resume parsing libraries for Python"
"Xavier, design the resume template selection UI"
"Brian, write compelling copy for the landing page"
```

**Complex feature (multiple agents):**
```
"Build a resume preview feature:
Randy - research best practices for resume formatting
Theo - design the PDF generation architecture
Xavier - design the preview interface
Bailey - implement the PDF generation API
Finn - build the preview UI component"
```

**Common workflow:**
1. Randy researches → Theo designs architecture → Xavier designs UI → Bailey/Finn implement in parallel → Theo reviews

All agent configs are in `.claude/agents/` directory.

See `AGENTS_QUICK_REFERENCE.md` for detailed usage patterns.

---

## Core Features

### Current Implementation
- Resume creation and management
- AI-powered resume generation
- Job matching and recommendations
- Resume upload and parsing
- PDF generation (WeasyPrint)
- User authentication (Supabase)
- Database migrations

### Key Capabilities
- Intelligent resume assistance
- Structured data management
- Professional formatting
- Job application tracking
- Reference preview system

## Development Workflow

### Backend Development
```bash
cd resumaker/backend

# Start backend server
python main.py
# or
./start.sh

# Run migrations
python run_migrations.py

# Run tests
pytest
```

### Frontend Development
```bash
cd resumaker/frontend

# Install dependencies
npm install

# Start dev server
npm run dev

# Run tests
npm test
```

### Testing
```bash
# Integration tests
python test_integration.py
python test_knowledge_flow.py
python test_resume_generation_complete.py
```

## Key Files & Directories

```
backend/
├── app/              # FastAPI application
├── migrations/       # Database migrations
├── data/             # Data files
├── main.py           # Entry point
└── requirements.txt  # Python dependencies

frontend/
├── src/              # Next.js source
├── components/       # React components
└── package.json      # Node dependencies

testing/              # Test files
validation_tests/     # Validation scripts
```

## Important Patterns

### Database
- Supabase for PostgreSQL database
- Migration system for schema changes
- User authentication and authorization

### AI/ML
- Resume generation using AI
- Job matching algorithms
- Knowledge system integration

### PDF Generation
- WeasyPrint for professional PDFs
- Multiple resume templates
- Custom formatting options

## Testing Procedures

### Before Deploying
1. Run backend tests: `pytest`
2. Run integration tests
3. Test PDF generation
4. Verify Supabase connection
5. Check Railway deployment health

## Key Documentation

- `CONTEXT.md` - Architecture overview
- `PROJECT_VISION.md` - Product vision and goals
- `PROJECT_STATUS.md` - Current status
- `DEPLOYMENT_GUIDE_CREATED.md` - Deployment process
- `DATABASE_DEPLOYMENT_CHECKLIST.md` - Database setup
- `API_DOCUMENTATION.md` - API reference
- `USER_GUIDE.md` - End-user documentation

## Session Logging

### When User Says "Log Session"
1. Check for SESSION_CURRENT.json
2. Run finalize-session.sh
3. Document work completed
4. Update CHANGELOG.md

**⚠️ TIME TRACKING**: Mark as personal/portfolio project time appropriately.

## Available Tools & Integrations

### Supabase
- Authentication
- Database (PostgreSQL)
- Real-time subscriptions
- Storage

### Railway
- Backend deployment
- Environment variables
- Database hosting
- Monitoring

## Communication Styles

### Documentation
- **Code comments**: Clear and professional
- **User-facing messages**: Helpful and encouraging
- **Technical docs**: Comprehensive with examples

## Known Limits & Prevention

### Platform Limits
- Railway build time limits
- Supabase free tier limits
- PDF generation memory constraints
- WeasyPrint rendering complexity

## Important Notes

- Always use Chicago timezone
- Document all API endpoints
- Keep frontend/backend in sync
- Test PDF generation thoroughly
- Monitor deployment health

## Deployment

### Backend (Railway)
- Deployed automatically on push
- Check `railway.json` for config
- Monitor logs for errors

### Frontend (Vercel)
- Deployed automatically on push
- Check environment variables
- Test production build locally first

## Contact & Support

For patterns and guidance, check:
- `/project_kickoff/README.md` - Knowledge base overview
- `/project_kickoff/AGENTS_QUICK_REFERENCE.md` - Agent team usage
- Local docs in project root

---

*Last Updated: October 19, 2025*
*Version: 1.0.0*
