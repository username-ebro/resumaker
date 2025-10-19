# Resumaker UI Component Library

A comprehensive, brutalist-styled component library for the Resumaker application.

## Quick Start

```tsx
import { Button, Card, Input, Badge, Navigation } from '@/components/ui';

function MyComponent() {
  return (
    <Card variant="elevated" padding="lg">
      <h2>My Card</h2>
      <Input
        label="Email"
        type="email"
        value={email}
        onChange={setEmail}
      />
      <Button variant="primary" icon="✨">
        Submit
      </Button>
      <Badge variant="success">Verified</Badge>
    </Card>
  );
}
```

## Components

### Button
Primary action component with loading states and variants.

**Variants:** primary, secondary, danger, ghost
**Sizes:** sm, md, lg
**Features:** Loading spinner, icon support, disabled state

```tsx
<Button variant="primary" size="lg" loading={loading} icon="🚀">
  Launch
</Button>
```

---

### Card
Container component with brutalist shadows and borders.

**Variants:** default, elevated, dark, outline, seafoam
**Padding:** sm (p-4), md (p-6), lg (p-8)
**Features:** Hover lift, clickable, keyboard accessible

```tsx
<Card variant="elevated" hover padding="lg" onClick={handleClick}>
  Content here
</Card>
```

---

### Input
Form input with label, error states, and password toggle.

**Types:** text, email, password, textarea
**Features:** Error/helper text, required indicator, ARIA labels

```tsx
<Input
  label="Password"
  type="password"
  value={password}
  onChange={setPassword}
  error={passwordError}
  required
/>

<Input
  label="Bio"
  type="textarea"
  value={bio}
  onChange={setBio}
  rows={4}
  helperText="Tell us about yourself"
/>
```

---

### Badge
Status indicator with color-coded variants.

**Variants:** default, success, warning, error, info
**Sizes:** sm, md, lg

```tsx
<Badge variant="success">Verified</Badge>
<Badge variant="error" size="lg">Failed</Badge>
```

---

### Navigation
Responsive navigation bar with user menu and badge support.

**Features:** Sticky header, active states, mobile menu, notifications

```tsx
<Navigation
  user={{ email: 'user@example.com' }}
  onLogout={handleLogout}
  links={[
    { label: 'Dashboard', href: '/dashboard', icon: '🏠' },
    { label: 'Resumes', href: '/resumes', icon: '📄' },
  ]}
  badge={{ count: 5, href: '/knowledge' }}
/>
```

---

## Design Principles

1. **Brutalist Aesthetic** - Thick borders, bold typography, high contrast
2. **Accessibility First** - ARIA labels, keyboard navigation, semantic HTML
3. **TypeScript Strict** - Full type safety with IntelliSense
4. **Composable** - Mix and match components freely
5. **Extensible** - All components accept `className` prop

## Color System

Components use CSS variables from `globals.css`:

- `--seafoam` - Focus states, accents
- `--black` - Borders, primary text
- `--white` - Backgrounds
- `--error` - Error states (#dc2626)
- `--success` - Success states (#16a34a)
- `--warning` - Warning states (#ea580c)

## Spacing Scale

- `sm` padding = 1rem (p-4)
- `md` padding = 1.5rem (p-6)
- `lg` padding = 2rem (p-8)

## Examples

### Login Form
```tsx
<Card variant="elevated" padding="lg">
  <h2>Login</h2>
  <Input
    label="Email"
    type="email"
    value={email}
    onChange={setEmail}
    required
  />
  <Input
    label="Password"
    type="password"
    value={password}
    onChange={setPassword}
    required
  />
  <Button variant="primary" size="lg" type="submit">
    Login
  </Button>
</Card>
```

### Resume Card with Badge
```tsx
<Card variant="default" hover padding="md" onClick={handleView}>
  <div className="flex justify-between items-start">
    <div>
      <h3>Senior Product Manager</h3>
      <Badge variant="success">ATS Optimized</Badge>
    </div>
    <Button variant="primary" size="sm" icon="📄">
      View
    </Button>
  </div>
</Card>
```

### Status Dashboard
```tsx
<div className="grid grid-cols-3 gap-4">
  <Card variant="seafoam" padding="md">
    <h4>Total Resumes</h4>
    <p className="text-3xl font-bold">{count}</p>
    <Badge variant="info">Updated Today</Badge>
  </Card>
</div>
```

## Demo

Visit `/components-demo` to see all components in action.

## File Structure

```
components/ui/
├── Button.tsx      - Primary action component
├── Card.tsx        - Container component
├── Input.tsx       - Form input component
├── Badge.tsx       - Status indicator
├── Navigation.tsx  - Nav bar component
├── index.ts        - Exports all components
└── README.md       - This file
```

## TypeScript

All components are fully typed. Use IntelliSense to explore available props:

```tsx
// Hover over Button to see all props
<Button variant="..." size="..." loading={...} />
```

## Contributing

When creating new components:

1. Follow brutalist design system
2. Use CSS variables from `globals.css`
3. Add full TypeScript types
4. Include ARIA attributes
5. Support `className` prop
6. Add JSDoc comments
7. Export from `index.ts`

## Support

See documentation:
- `COMPONENT_LIBRARY_SUMMARY.md` - Full overview
- `COMPONENT_REFACTORING_EXAMPLES.md` - Migration guide
- `/components-demo` page - Live examples
