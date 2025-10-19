# Component Architecture

## Component Hierarchy

```
Resumaker Application
│
├── Navigation (Top-level)
│   ├── Logo
│   ├── Links (Button components)
│   ├── Badge (notification count)
│   └── User Menu (Button + dropdown)
│
└── Page Content
    │
    ├── Card Components (containers)
    │   ├── Header (text + Badge)
    │   ├── Body (Input + text)
    │   └── Footer (Button components)
    │
    ├── Input Components (forms)
    │   ├── Label (with required indicator)
    │   ├── Input field (text/email/password/textarea)
    │   ├── Error message
    │   └── Helper text
    │
    ├── Button Components (actions)
    │   ├── Icon (optional)
    │   ├── Text
    │   └── Loading spinner (conditional)
    │
    └── Badge Components (status)
        └── Status text
```

## Component Dependencies

```
┌─────────────────────────────────────────────────────────┐
│                      globals.css                         │
│  (Design tokens: colors, spacing, shadows, animations)   │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ├──────────┬──────────┬──────────┬──────────┐
                        │          │          │          │          │
                    ┌───▼───┐  ┌──▼──┐  ┌───▼───┐  ┌───▼───┐  ┌───▼────────┐
                    │Button │  │Card │  │Input  │  │Badge  │  │Navigation  │
                    └───────┘  └─────┘  └───────┘  └───────┘  └─────┬──────┘
                        │                                            │
                        └──────────────┬─────────────────────────────┘
                                       │
                               ┌───────▼────────┐
                               │  Page Components│
                               │  (LoginForm,    │
                               │   Dashboard,    │
                               │   etc.)         │
                               └─────────────────┘
```

## Data Flow

```
User Action
    │
    ▼
Component Event Handler (onClick, onChange)
    │
    ▼
Parent Component State Update (useState, setState)
    │
    ▼
Component Re-render with New Props
    │
    ▼
Visual Feedback (loading spinner, error message, etc.)
```

## Example: Form Submission Flow

```
1. User types in Input component
   └─> onChange(value) called
       └─> Parent updates state: setEmail(value)

2. User clicks Button component
   └─> onClick() called
       └─> Parent sets loading: setLoading(true)
           └─> Button shows spinner
               └─> API call initiated
                   └─> Success/Error
                       └─> Parent updates state
                           └─> Input shows error OR Card shows success
```

## Component Composition Patterns

### Pattern 1: Login Form
```tsx
<Card variant="elevated" padding="lg">
  <Input type="email" />
  <Input type="password" />
  <Button variant="primary" />
</Card>
```

### Pattern 2: Resume Card
```tsx
<Card variant="default" hover onClick={...}>
  <div>
    <h3>Title</h3>
    <Badge variant="success" />
  </div>
  <Button variant="primary" />
</Card>
```

### Pattern 3: Dashboard Layout
```tsx
<Navigation user={...} links={...} />
<Card variant="seafoam">
  <Input type="textarea" />
  <Button variant="primary" loading={...} />
</Card>
```

### Pattern 4: Status Display
```tsx
<Card variant="outline">
  <Badge variant="warning" />
  <p>Status message</p>
  <Button variant="secondary" />
</Card>
```

## State Management

### Local Component State
```tsx
// Inside Input component
const [showPassword, setShowPassword] = useState(false);
```

### Parent Component State
```tsx
// Inside page component
const [email, setEmail] = useState('');
const [loading, setLoading] = useState(false);
const [error, setError] = useState('');
```

### Lifted State (passed as props)
```tsx
<Input
  value={email}          // from parent state
  onChange={setEmail}    // updates parent state
  error={emailError}     // from parent validation
/>
```

## Styling Architecture

```
Global Styles (globals.css)
    │
    ├── CSS Variables
    │   ├── Colors (--seafoam, --black, --white, etc.)
    │   ├── Spacing (--space-1 through --space-16)
    │   └── Shadows (brutal-shadow, brutal-shadow-seafoam)
    │
    ├── Utility Classes
    │   ├── .brutal-box (border + position)
    │   ├── .brutal-btn (button base styles)
    │   ├── .brutal-input (input base styles)
    │   ├── .brutal-shadow (6px offset shadow)
    │   └── .cool-spinner (loading animation)
    │
    └── Component-Specific Classes
        ├── .form-group (input wrapper)
        ├── .form-label (uppercase, bold)
        ├── .form-error (red background + border)
        └── .password-toggle (absolute positioned button)
```

## TypeScript Type System

```
HTMLAttributes (React base types)
    │
    ├── ButtonHTMLAttributes<HTMLButtonElement>
    │   └── ButtonProps (extends + custom props)
    │
    ├── InputHTMLAttributes<HTMLInputElement>
    │   └── TextInputProps (extends + custom props)
    │
    ├── TextareaHTMLAttributes<HTMLTextAreaElement>
    │   └── TextareaInputProps (extends + custom props)
    │
    └── HTMLAttributes<HTMLDivElement>
        └── CardProps (extends + custom props)
```

## Accessibility Tree

```
<Navigation>
  └─ <nav role="navigation">
      ├─ <button aria-label="Logo">
      ├─ <button aria-current="page">  (active link)
      └─ <button aria-expanded="true"> (user menu)

<Card>
  └─ <div role="button" tabindex="0"> (if onClick)

<Input>
  └─ <div>
      ├─ <label for="input-id">
      ├─ <input aria-invalid="false" aria-describedby="helper-id">
      └─ <p id="helper-id"> (helper text)

<Button>
  └─ <button disabled={...} aria-busy="true"> (if loading)
      ├─ <span> (loading spinner)
      └─ children
```

## File Size Breakdown

```
Component Files:
├── Button.tsx        - 60 lines  (variants, sizes, loading)
├── Card.tsx          - 55 lines  (variants, hover, padding)
├── Input.tsx         - 129 lines (types, password, textarea)
├── Badge.tsx         - 45 lines  (variants, sizes)
├── Navigation.tsx    - 237 lines (responsive, menu, mobile)
└── index.ts          - 5 lines   (exports)

Total: 531 lines of reusable component code

Demo & Docs:
├── components-demo/page.tsx              - 300+ lines
├── COMPONENT_REFACTORING_EXAMPLES.md     - 400+ lines
├── COMPONENT_LIBRARY_SUMMARY.md          - 600+ lines
└── components/ui/README.md               - 200+ lines

Total: 1,500+ lines of documentation
```

## Import Graph

```
Application Pages
    │
    ├─ /auth/login
    │   └─> imports { Input, Button, Card }
    │
    ├─ /dashboard
    │   └─> imports { Navigation, Card, Badge, Button }
    │
    ├─ /resumes
    │   └─> imports { Card, Button, Badge }
    │
    └─ /components-demo
        └─> imports { ALL components }

All imports resolve through:
    @/components/ui (index.ts)
        ├─> Button
        ├─> Card
        ├─> Input
        ├─> Badge
        └─> Navigation
```

## Performance Optimization

### Tree Shaking
```tsx
// Only imports used components
import { Button, Card } from '@/components/ui';

// Result: Badge, Input, Navigation NOT included in bundle
```

### Code Splitting
```tsx
// Next.js automatically code-splits by route
// /components-demo gets ALL components
// /auth/login only gets Input, Button, Card
```

### Component Memoization (Future)
```tsx
// Optional optimization for expensive renders
export default memo(Button);
export default memo(Card);
```

## Testing Strategy (Recommended)

```
Unit Tests (Jest + React Testing Library)
    │
    ├── Button.test.tsx
    │   ├─ renders all variants
    │   ├─ handles click events
    │   ├─ shows loading state
    │   └─ disables properly
    │
    ├── Input.test.tsx
    │   ├─ renders all types
    │   ├─ shows error states
    │   ├─ toggles password visibility
    │   └─ calls onChange handler
    │
    └── ... (other components)

Integration Tests
    │
    ├── LoginForm.test.tsx
    │   └─ uses Input + Button together
    │
    └── Dashboard.test.tsx
        └─ uses Navigation + Card + Badge

E2E Tests (Playwright/Cypress)
    │
    └─ Full user flows with real components
```

## Version History

### v1.0.0 (2025-10-19) - Initial Release
- ✅ Button component (4 variants, 3 sizes)
- ✅ Card component (5 variants, 3 padding sizes)
- ✅ Input component (4 types, error/helper text)
- ✅ Badge component (5 variants, 3 sizes)
- ✅ Navigation component (responsive, user menu)
- ✅ Complete TypeScript typing
- ✅ Accessibility features (ARIA, keyboard nav)
- ✅ Demo page with examples
- ✅ Comprehensive documentation

### Future Versions (Roadmap)
- v1.1.0 - Modal/Dialog component
- v1.2.0 - Dropdown/Select component
- v1.3.0 - Toast/Notification system
- v2.0.0 - Dark mode support
