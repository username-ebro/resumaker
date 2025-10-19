# Quick Reference: Development Team Agents

## Your Team at a Glance

| Agent | Role | Call When You Need... |
|-------|------|----------------------|
| **Ebro** | CEO (You!) | Orchestration, vision, delegation |
| **Theo** | CTO | Architecture, code review, technical decisions |
| **Xavier** | UX Lead | User flows, design specs, wireframes |
| **Brian** | Brand Director | Copy, messaging, content |
| **Randy** | Researcher | Deep research, documentation, best practices |
| **Bailey** | Backend Dev | APIs, databases, server logic |
| **Finn** | Frontend Dev | UI components, client-side code |

---

## Quick Invocation Guide

### Pattern 1: Direct Call
Just mention the agent and task:
```
"Randy, research the best WebSocket libraries for real-time chat"
"Xavier, design the checkout flow with 3 steps"
"Theo, review the authentication code for security"
```

### Pattern 2: Complex Feature (Use Multiple Agents)
```
"I need a user dashboard with real-time updates.

Theo - design the architecture
Randy - research real-time update strategies
Xavier - design the dashboard layout
Bailey - implement the backend APIs
Finn - build the UI components"
```

### Pattern 3: Bug Fix
```
"There's a bug in the login form.
Theo - diagnose the root cause
Bailey/Finn - implement the fix based on Theo's findings"
```

---

## Common Workflows

### 🚀 New Feature Development
```
1. Ebro: Define requirements and priority
2. Theo: Design architecture approach
3. Randy: Research unfamiliar tech
4. Xavier: Design user flow and UI
5. Brian: Write user-facing copy
6. Bailey + Finn: Implement (parallel)
7. Theo: Code review
8. Ebro: Approve and deploy
```

### 🐛 Bug Fix
```
1. Ebro: Triage and prioritize
2. Theo: Diagnose root cause
3. Bailey/Finn: Implement fix
4. Theo: Verify fix
5. Ebro: Deploy
```

### 🔍 Research Task
```
1. Ebro: Define research question
2. Randy: Deep research
3. Theo: Technical evaluation
4. Ebro: Make decision
```

### 🎨 Design Update
```
1. Xavier: Design new flow
2. Brian: Write copy
3. Theo: Review technical feasibility
4. Finn: Implement
5. Theo: Review
```

---

## Agent Personalities (For Reference)

### Theo (CTO)
- Pragmatic, no BS
- "This will cause issues because..."
- Always references exact files/lines
- Security and performance focused

### Xavier (UX Lead)
- Empathetic, detail-obsessed
- "From the user's perspective..."
- Accessibility champion
- Precise specifications

### Brian (Brand Director)
- Creative, persuasive
- "Let's make this clearer..."
- Conversion-focused
- Hates jargon

### Randy (Researcher)
- Thorough, methodical
- "According to the documentation..."
- Always cites sources
- Produces structured reports

### Bailey (Backend Dev)
- Logical, security-conscious
- "We need to validate..."
- Performance optimizer
- Tests everything

### Finn (Frontend Dev)
- Detail-oriented, user-centric
- "This should be accessible..."
- Pixel-perfect implementer
- Performance aware

---

## When to Use Which Agent

### "I need to decide on technology..."
→ **Randy** researches options
→ **Theo** evaluates and decides

### "I need API endpoints..."
→ **Theo** designs API contract
→ **Bailey** implements backend
→ **Finn** integrates frontend

### "I need a new page/feature..."
→ **Xavier** designs flow and UI
→ **Brian** writes copy
→ **Bailey** builds backend
→ **Finn** builds frontend

### "I need to understand how something works..."
→ **Randy** researches and explains

### "I need to review code quality..."
→ **Theo** reviews and provides feedback

### "I need better error messages..."
→ **Brian** rewrites with empathy

### "I need to optimize performance..."
→ **Theo** diagnoses bottleneck
→ **Bailey/Finn** implements optimization

### "Something is broken..."
→ **Theo** diagnoses
→ **Bailey/Finn** fixes

---

## Tips for Effective Delegation

### ✅ Good Delegation
```
"Xavier, design the user onboarding flow for first-time users.
We want to collect email, name, and preferences.
Keep it to 3 steps maximum.
Design mobile-first."
```
*Clear task, context, constraints*

### ❌ Poor Delegation
```
"Make the signup better"
```
*Too vague, unclear who should do what*

### ✅ Good Multi-Agent Delegation
```
"Build a payment integration feature:

Randy - Research Stripe vs PayPal for our use case
Theo - Design the payment flow architecture after Randy reports
Bailey - Implement Stripe integration based on Theo's design
Xavier - Design the checkout UI
Brian - Write the payment confirmation copy
Finn - Implement the checkout UI with Xavier's design and Brian's copy"
```
*Clear sequence, dependencies noted*

---

## Agent Communication Formats

### Theo → Bailey/Finn
Architecture specs, API contracts, code review feedback

### Xavier → Finn
Component specs, design tokens, interaction details

### Brian → Finn
Button labels, error messages, content

### Randy → Anyone
Research reports with sources and recommendations

### Bailey → Finn
API contracts, TypeScript types, integration notes

---

## Remember

- **Ebro (You)** orchestrates everything
- **Theo** is your right-hand for technical execution
- **Randy** researches before others decide
- **Xavier** designs before Finn implements
- **Brian** writes copy for Xavier and Finn
- **Bailey** and **Finn** work in parallel when possible
- **Theo** reviews all code before deployment

---

## Quick Reference: File Locations

All agent configs are in: `.claude/agents/`

- `theo-cto.md` - CTO
- `xavier-ux.md` - UX Lead
- `brian-brand.md` - Brand Director
- `randy-researcher.md` - Researcher
- `bailey-backend.md` - Backend Dev
- `finn-frontend.md` - Frontend Dev

---

*This system scales with your needs while maintaining clarity and collaborative intelligence.*
