# Agent Usage Examples
## Real-World Scenarios with Your Development Team

**Last Updated:** October 12, 2025

---

## Example 1: Building a User Dashboard

### The Request
"I need a dashboard that shows user analytics with real-time updates"

### The Workflow

**Step 1: Architecture Planning**
```
User: "Theo, design the architecture for a real-time analytics dashboard"

Theo:
- Researches requirements
- Asks Randy to research WebSocket vs SSE options
- Designs data flow (client ↔ WebSocket ↔ server ↔ database)
- Creates API contracts for Bailey
- Defines state management approach for Finn
- Produces architecture document
```

**Step 2: Research Phase**
```
Theo: "Randy, research real-time update strategies. Compare WebSockets, SSE, and polling."

Randy:
- Researches WebSockets, Server-Sent Events, long polling
- Compares performance, browser support, complexity
- Finds implementation examples
- Recommends WebSockets with Socket.io (best for bi-directional)
- Provides structured research report with sources
```

**Step 3: Design Phase**
```
User: "Xavier, design the dashboard layout with real-time charts"

Xavier:
- Designs dashboard layout (sidebar + main area + widgets)
- Plans responsive behavior (mobile/tablet/desktop)
- Creates component hierarchy
- Designs loading states and empty states
- Specifies accessibility requirements (ARIA live regions)
- Produces design specification for Finn
```

**Step 4: Content Phase**
```
User: "Brian, write the copy for the dashboard"

Brian:
- Writes page title and section headings
- Creates empty state messages ("No data yet. Your first user will appear here.")
- Writes error messages ("Unable to load analytics. Retrying...")
- Creates tooltips for metrics
- Provides all copy to Finn for implementation
```

**Step 5: Implementation Phase (Parallel)**
```
User: "Bailey and Finn, implement the dashboard based on Theo's architecture,
Xavier's design, and Brian's copy"

Bailey (Backend):
- Implements WebSocket server with Socket.io
- Creates analytics API endpoints
- Builds database queries for metrics
- Implements real-time event broadcasting
- Writes API tests
- Provides API contract and TypeScript types to Finn

Finn (Frontend):
- Implements dashboard components from Xavier's specs
- Integrates Socket.io client
- Builds real-time chart components
- Implements Brian's copy throughout UI
- Adds accessibility features (ARIA live regions)
- Writes component tests
- Uses Bailey's API contract for integration
```

**Step 6: Code Review**
```
User: "Theo, review the dashboard implementation"

Theo:
- Reviews Bailey's backend code (security, performance, error handling)
- Reviews Finn's frontend code (accessibility, performance, state management)
- Verifies WebSocket connection handling
- Tests real-time updates
- Approves with minor suggestions
- Provides feedback for improvements
```

**Step 7: Deployment**
```
User: "Deploy the dashboard to production"

Ebro (You):
- Verifies all tests pass
- Coordinates deployment timing
- Monitors initial rollout
- Dashboard goes live successfully!
```

---

## Example 2: Fixing a Performance Bug

### The Problem
"The user list page is loading very slowly (15+ seconds)"

### The Workflow

**Step 1: Diagnosis**
```
User: "Theo, diagnose why the user list page is so slow"

Theo:
- Analyzes the page load waterfall
- Identifies that backend API call takes 12 seconds
- Finds N+1 query problem (loading user details one-by-one in loop)
- Pinpoints the issue in Bailey's code
- Creates diagnosis report with specific file/line numbers
```

**Step 2: Fix Implementation**
```
Theo: "Bailey, fix the N+1 query problem in users API endpoint"

Bailey:
- Rewrites query to use JOIN instead of loop
- Adds database index on foreign key
- Tests performance improvement (12s → 0.3s)
- Adds query comment explaining optimization
- Writes test to prevent regression
- Reports: "Fixed! Query now runs in 300ms (was 12s)"
```

**Step 3: Verification**
```
Theo:
- Reviews Bailey's fix
- Verifies query optimization
- Checks that tests prevent regression
- Approves deployment
```

**Result:** Page load time: 15s → 2s (87% improvement)

---

## Example 3: Adding Payment Processing

### The Request
"I need to add Stripe payment processing for subscriptions"

### The Workflow

**Step 1: Research Phase**
```
User: "Randy, research how to implement Stripe subscriptions with webhooks"

Randy:
- Reads Stripe API documentation
- Finds subscription lifecycle management best practices
- Researches webhook security and verification
- Discovers common pitfalls (idempotency, webhook replay attacks)
- Provides comprehensive report with code examples
```

**Step 2: Architecture Planning**
```
User: "Theo, design the Stripe integration architecture"

Theo (using Randy's research):
- Designs subscription flow (signup → Stripe → webhook → database)
- Plans database schema (customers, subscriptions, invoices)
- Defines API endpoints Bailey needs to build
- Plans frontend state management for Finn
- Creates security checklist (webhook signature verification, etc.)
- Produces architecture document
```

**Step 3: Implementation**
```
User: "Bailey, implement the Stripe backend integration"

Bailey (using Theo's architecture):
- Implements Stripe API client
- Creates subscription management endpoints
- Builds webhook handler with signature verification
- Implements idempotency for webhook processing
- Adds comprehensive error handling
- Writes integration tests (mocks Stripe API)
- Provides API contract to Finn
```

```
User: "Xavier, design the subscription checkout flow"

Xavier:
- Designs 3-step checkout (Plan → Payment → Confirmation)
- Creates payment form layout
- Designs success/error states
- Plans loading indicators
- Specifies accessibility requirements
- Provides component specs to Finn
```

```
User: "Brian, write the copy for the checkout flow"

Brian:
- Writes plan descriptions and pricing
- Creates payment form labels
- Writes success message ("Welcome! Your subscription is active.")
- Writes error messages ("Payment failed. Please check your card details.")
- Creates email templates for receipts
- Provides all copy to Finn
```

```
User: "Finn, implement the checkout UI"

Finn (using Xavier's design + Brian's copy + Bailey's API):
- Implements Stripe Elements for card input
- Builds 3-step checkout wizard
- Adds form validation
- Implements success/error handling
- Adds accessibility features
- Writes component tests
- Integrates with Bailey's subscription API
```

**Step 4: Security Review**
```
User: "Theo, review the Stripe integration for security"

Theo:
- Verifies webhook signature validation
- Checks API key storage (environment variables)
- Reviews error handling (no sensitive data leaked)
- Tests idempotency (duplicate webhooks handled)
- Verifies PCI compliance (no card data stored)
- Approves for production
```

**Result:** Secure, production-ready Stripe integration

---

## Example 4: Redesigning the Landing Page

### The Request
"Our landing page isn't converting. Let's redesign it."

### The Workflow

**Step 1: Research**
```
User: "Randy, research high-converting SaaS landing page patterns"

Randy:
- Analyzes competitor landing pages
- Finds best practices (hero, social proof, features, CTA)
- Researches conversion optimization techniques
- Collects examples of effective copy and layouts
- Provides structured report with recommendations
```

**Step 2: Content Strategy**
```
User: "Brian, write the landing page copy focused on conversion"

Brian (using Randy's research):
- Writes compelling headline ("Ship features faster without breaking production")
- Creates benefit-focused feature descriptions
- Writes strong CTAs ("Start Free Trial" not "Submit")
- Crafts social proof section with testimonials
- Writes trust elements ("No credit card required")
- Provides complete copy document
```

**Step 3: Design**
```
User: "Xavier, design the new landing page layout"

Xavier (using Brian's copy):
- Designs hero section with headline + CTA
- Creates visual hierarchy for features
- Designs social proof section layout
- Plans responsive behavior for mobile
- Adds micro-interactions (button hover states)
- Specifies animations (scroll reveals)
- Produces component specifications for Finn
```

**Step 4: Implementation**
```
User: "Finn, implement the new landing page"

Finn (using Xavier's design + Brian's copy):
- Builds responsive hero section
- Implements feature cards with icons
- Adds scroll-triggered animations
- Implements CTA buttons with Brian's copy
- Optimizes images for fast loading
- Ensures accessibility (semantic HTML, ARIA)
- Tests on mobile/tablet/desktop
```

**Step 5: Review**
```
User: "Theo, review the landing page for performance"

Theo:
- Runs Lighthouse audit (95+ score)
- Verifies image optimization
- Checks bundle size (<100KB)
- Tests load time (First Contentful Paint <1s)
- Approves for production
```

**Result:** New landing page live with improved conversion rate

---

## Example 5: Troubleshooting an Obscure Error

### The Problem
"Users are getting a 'TypeError: Cannot read property 'id' of undefined' error intermittently"

### The Workflow

**Step 1: Research the Error**
```
User: "Randy, research this error and common causes"

Randy:
- Searches StackOverflow and GitHub issues
- Finds common patterns (race conditions, null checks)
- Researches debugging techniques for intermittent issues
- Provides report with potential causes
```

**Step 2: Diagnosis**
```
User: "Theo, diagnose the root cause using Randy's research"

Theo:
- Reviews error logs and stack traces
- Identifies it happens when API returns empty response
- Finds missing null check in Finn's code
- Also finds Bailey's API sometimes returns null instead of 404
- Creates diagnosis: "Two issues - missing error handling (frontend) and
  inconsistent error responses (backend)"
```

**Step 3: Fix Both Issues**
```
Theo: "Bailey, fix the API to return consistent 404 errors"
Theo: "Finn, add null checks and error handling"

Bailey:
- Updates API to return 404 with error message (not null)
- Adds tests for error cases
- Reports: "API now returns proper error responses"

Finn:
- Adds null checks before accessing properties
- Implements error boundary to catch issues
- Shows user-friendly error message
- Adds tests for error scenarios
- Reports: "Error handling added with graceful fallback"
```

**Step 4: Verification**
```
Theo:
- Verifies both fixes
- Tests error scenarios
- Confirms error no longer occurs
- Approves deployment
```

**Result:** Error eliminated, users see helpful message instead of crash

---

## Example 6: Quick Content Update

### The Request
"The error message 'Error 404' is confusing users. Make it better."

### The Workflow

**Simple and Fast:**
```
User: "Brian, rewrite this error message to be more helpful"

Brian:
- Analyzes context (404 = page not found)
- Rewrites message:
  - Before: "Error 404"
  - After: "This page doesn't exist. Check the URL or return to the homepage."
- Provides updated copy

User: "Finn, update the 404 error message with Brian's copy"

Finn:
- Updates ErrorPage component
- Adds "Return Home" button
- Tests in browser
- Reports: "Error message updated!"
```

**Result:** Users get helpful guidance instead of technical error

---

## Key Patterns from These Examples

### 1. Research → Design → Implement
Most features follow this flow:
- Randy researches best approaches
- Theo designs architecture
- Bailey + Finn implement in parallel

### 2. Content Comes Before Design
For user-facing features:
- Brian writes copy first
- Xavier designs around the content
- Finn implements the complete experience

### 3. Always Review Before Deployment
- Theo reviews all code
- Checks security, performance, quality
- Catches issues before production

### 4. Parallel Work When Possible
- Bailey builds backend while Finn builds frontend
- Randy researches while Theo plans
- Xavier designs while Brian writes copy

### 5. Use Specialists for Specialists' Work
- Don't ask Finn to research libraries (Randy's job)
- Don't ask Bailey to design UX (Xavier's job)
- Don't ask Randy to implement code (Bailey/Finn's job)

---

## Quick Reference: Who to Call

| Task | Primary Agent | Support |
|------|---------------|---------|
| "Research this library" | Randy | → Theo (decision) |
| "Design this feature" | Xavier + Brian | → Finn (implementation) |
| "Build an API" | Bailey | Theo (review) |
| "Fix a bug" | Theo (diagnose) | → Bailey/Finn (fix) |
| "Improve performance" | Theo | → Bailey/Finn |
| "Review code" | Theo | - |
| "Write copy" | Brian | - |
| "Build a UI" | Finn | Xavier (spec), Brian (copy) |

---

*These patterns scale from small tasks (single agent) to complex features (entire team collaboration).*
