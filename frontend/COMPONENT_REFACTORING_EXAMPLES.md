# Component Library Refactoring Examples

This document shows how to refactor existing code to use the new reusable component library.

## Example 1: LoginForm.tsx - Before & After

### Before (Custom Implementation)
```tsx
// LoginForm.tsx - OLD
<form onSubmit={handleLogin} className="space-y-6">
  {error && (
    <div className="form-error">
      <strong>Error:</strong> {error}
    </div>
  )}

  <div className="form-group">
    <label htmlFor="email" className="form-label">Email Address</label>
    <input
      id="email"
      type="email"
      value={email}
      onChange={(e) => setEmail(e.target.value)}
      className="form-input"
      placeholder="you@example.com"
      autoComplete="email"
      required
    />
  </div>

  <div className="form-group">
    <label htmlFor="password" className="form-label">Password</label>
    <div className="password-input-wrapper">
      <input
        id="password"
        type={showPassword ? 'text' : 'password'}
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="form-input"
        placeholder="Enter your password"
        autoComplete="current-password"
        required
      />
      <button
        type="button"
        onClick={() => setShowPassword(!showPassword)}
        className="password-toggle"
        aria-label={showPassword ? 'Hide password' : 'Show password'}
      >
        {showPassword ? '🙈' : '👁️'}
      </button>
    </div>
  </div>

  <button
    type="submit"
    disabled={loading}
    className={`brutal-btn brutal-btn-primary brutal-shadow w-full ${loading ? 'btn-loading' : ''}`}
  >
    {loading ? 'Logging in...' : 'Login'}
  </button>
</form>
```

### After (Using Component Library)
```tsx
// LoginForm.tsx - NEW
import { Input, Button, Card } from '@/components/ui';

<form onSubmit={handleLogin} className="space-y-6">
  {error && (
    <Card variant="outline" padding="sm" className="bg-red-50 border-red-600">
      <strong>Error:</strong> {error}
    </Card>
  )}

  <Input
    label="Email Address"
    type="email"
    value={email}
    onChange={setEmail}
    placeholder="you@example.com"
    required
  />

  <Input
    label="Password"
    type="password"
    value={password}
    onChange={setPassword}
    placeholder="Enter your password"
    required
  />

  <Button
    type="submit"
    variant="primary"
    size="lg"
    loading={loading}
    className="w-full"
  >
    Login
  </Button>
</form>
```

**Benefits:**
- 40% less code
- Built-in password toggle
- Consistent styling
- Error states handled automatically
- Better accessibility

---

## Example 2: Dashboard Navigation - Before & After

### Before (Custom Implementation)
```tsx
// dashboard/page.tsx - OLD
<nav className="brutal-box border-b-4 border-black bg-white sticky top-0 z-50">
  <div className="max-w-7xl mx-auto px-6 py-6 flex justify-between items-center">
    <div className="flex items-center gap-4">
      <h1 className="text-3xl font-black tracking-tight">RESUMAKER</h1>
      <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">Dashboard</span>
    </div>
    <div className="flex items-center gap-4">
      <button
        onClick={() => router.push('/resumes')}
        className="brutal-btn brutal-btn-seafoam brutal-shadow text-sm"
      >
        📄 My Resumes
      </button>
      <button
        onClick={() => router.push('/dashboard/knowledge')}
        className="brutal-btn brutal-btn-seafoam brutal-shadow relative text-sm"
      >
        📚 Knowledge Base
        {pendingCount > 0 && (
          <span className="absolute -top-2 -right-2 bg-black text-white text-xs font-bold px-2 py-1 border-2 border-black">
            {pendingCount}
          </span>
        )}
      </button>
      <button
        onClick={handleLogout}
        className="brutal-btn brutal-shadow text-sm"
      >
        Logout
      </button>
    </div>
  </div>
</nav>
```

### After (Using Component Library)
```tsx
// dashboard/page.tsx - NEW
import { Navigation } from '@/components/ui';

<Navigation
  user={{ email: user?.email || '', name: user?.user_metadata?.name }}
  onLogout={handleLogout}
  links={[
    { label: 'Dashboard', href: '/dashboard', icon: '🏠' },
    { label: 'My Resumes', href: '/resumes', icon: '📄' },
  ]}
  badge={{ count: pendingCount, href: '/dashboard/knowledge' }}
/>
```

**Benefits:**
- 80% less code
- Responsive design built-in
- Active state highlighting
- Mobile menu automatically
- Reusable across app

---

## Example 3: Card Grid - Before & After

### Before (Custom Implementation)
```tsx
// dashboard/page.tsx - OLD
<div className="grid grid-cols-1 md:grid-cols-3 gap-6">
  <div className="brutal-box brutal-shadow bg-white p-6">
    <h3 className="text-lg font-bold mb-2">Total Resumes</h3>
    <p className="text-3xl font-black">{resumeCount}</p>
  </div>

  <div className="brutal-box brutal-shadow bg-white p-6 hover:-translate-y-1 cursor-pointer"
       onClick={() => router.push('/knowledge')}>
    <h3 className="text-lg font-bold mb-2">Knowledge Facts</h3>
    <p className="text-3xl font-black">{factCount}</p>
  </div>

  <div className="brutal-box bg-gradient-to-br from-black to-gray-800 text-white p-6">
    <h3 className="text-lg font-bold mb-2">Applications</h3>
    <p className="text-3xl font-black">{appCount}</p>
  </div>
</div>
```

### After (Using Component Library)
```tsx
// dashboard/page.tsx - NEW
import { Card, Badge } from '@/components/ui';

<div className="grid grid-cols-1 md:grid-cols-3 gap-6">
  <Card variant="default" padding="md">
    <h3 className="text-lg font-bold mb-2">Total Resumes</h3>
    <p className="text-3xl font-black">{resumeCount}</p>
  </Card>

  <Card variant="default" padding="md" hover onClick={() => router.push('/knowledge')}>
    <h3 className="text-lg font-bold mb-2">Knowledge Facts</h3>
    <p className="text-3xl font-black">{factCount}</p>
    <Badge variant="info">Updated Today</Badge>
  </Card>

  <Card variant="dark" padding="md">
    <h3 className="text-lg font-bold mb-2">Applications</h3>
    <p className="text-3xl font-black">{appCount}</p>
  </Card>
</div>
```

**Benefits:**
- Cleaner code
- Hover effects built-in
- Consistent padding/shadows
- Easy variant switching

---

## Example 4: Form with Validation - Before & After

### Before (Custom Implementation)
```tsx
// components/JobForm.tsx - OLD
<div className="space-y-4">
  <div>
    <label className="block text-xs font-bold mb-2 uppercase">Job Title</label>
    <input
      type="text"
      value={jobTitle}
      onChange={(e) => setJobTitle(e.target.value)}
      placeholder="e.g., Senior Product Manager"
      className="brutal-input w-full"
    />
  </div>

  <div>
    <label className="block text-xs font-bold mb-2 uppercase">Job Description</label>
    <textarea
      value={jobDescription}
      onChange={(e) => setJobDescription(e.target.value)}
      placeholder="Paste the full job description here..."
      className="brutal-input w-full h-48 resize-y"
    />
    {error && <p className="text-xs text-red-600 mt-1">{error}</p>}
  </div>

  <button
    onClick={handleSubmit}
    disabled={!jobDescription.trim() || loading}
    className={`brutal-btn brutal-shadow w-full disabled:opacity-50 ${
      loading ? 'bg-[#2d5f5d] text-white' : 'brutal-btn-primary'
    }`}
  >
    {loading && <div className="spinner" />}
    {loading ? 'Analyzing...' : 'Analyze Job'}
  </button>
</div>
```

### After (Using Component Library)
```tsx
// components/JobForm.tsx - NEW
import { Input, Button } from '@/components/ui';

<div className="space-y-4">
  <Input
    label="Job Title"
    type="text"
    value={jobTitle}
    onChange={setJobTitle}
    placeholder="e.g., Senior Product Manager"
    required
  />

  <Input
    label="Job Description"
    type="textarea"
    value={jobDescription}
    onChange={setJobDescription}
    placeholder="Paste the full job description here..."
    rows={8}
    error={error}
    helperText="We'll extract key requirements and company info"
  />

  <Button
    variant="primary"
    size="lg"
    loading={loading}
    disabled={!jobDescription.trim()}
    onClick={handleSubmit}
    className="w-full"
    icon="🔍"
  >
    Analyze Job
  </Button>
</div>
```

**Benefits:**
- Input validation built-in
- Helper text support
- Loading states automatic
- Consistent error styling
- Required field indicators

---

## Example 5: Status Badges - Before & After

### Before (Custom Implementation)
```tsx
// resumes/page.tsx - OLD
<div className="flex gap-2">
  {resume.ats_optimized && (
    <span className="bg-green-100 text-green-800 text-xs font-bold px-3 py-1 border-2 border-green-600 uppercase">
      ATS Optimized
    </span>
  )}
  {resume.pending && (
    <span className="bg-yellow-100 text-yellow-800 text-xs font-bold px-3 py-1 border-2 border-yellow-600 uppercase">
      Pending Review
    </span>
  )}
  {resume.failed && (
    <span className="bg-red-100 text-red-800 text-xs font-bold px-3 py-1 border-2 border-red-600 uppercase">
      Generation Failed
    </span>
  )}
</div>
```

### After (Using Component Library)
```tsx
// resumes/page.tsx - NEW
import { Badge } from '@/components/ui';

<div className="flex gap-2">
  {resume.ats_optimized && <Badge variant="success">ATS Optimized</Badge>}
  {resume.pending && <Badge variant="warning">Pending Review</Badge>}
  {resume.failed && <Badge variant="error">Generation Failed</Badge>}
</div>
```

**Benefits:**
- 70% less code
- Consistent badge styling
- Easy to read/maintain
- Variant system prevents errors

---

## Migration Checklist

### Phase 1: Low-Risk Components (Start Here)
- [ ] Replace `<button>` with `<Button>` in all forms
- [ ] Replace custom card `div`s with `<Card>` component
- [ ] Replace status indicators with `<Badge>` component

### Phase 2: Medium Complexity
- [ ] Replace form inputs with `<Input>` component
- [ ] Update error displays to use Card component
- [ ] Consolidate loading states to use Button's loading prop

### Phase 3: Navigation
- [ ] Replace navigation bar with `<Navigation>` component
- [ ] Test responsive behavior on mobile
- [ ] Verify active state highlighting works

### Phase 4: Testing
- [ ] Run build to check for TypeScript errors
- [ ] Test all interactive components (buttons, inputs, etc.)
- [ ] Verify accessibility (keyboard navigation, ARIA labels)
- [ ] Check mobile responsiveness

---

## Import Patterns

### Individual Imports
```tsx
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';
```

### Grouped Import (Recommended)
```tsx
import { Button, Card, Input, Badge, Navigation } from '@/components/ui';
```

---

## Common Customizations

### Extending Button Styles
```tsx
<Button
  variant="primary"
  className="w-full md:w-auto shadow-xl"
>
  Custom Button
</Button>
```

### Card with Custom Background
```tsx
<Card
  variant="default"
  padding="lg"
  className="bg-gradient-to-br from-purple-50 to-blue-50"
>
  Gradient card
</Card>
```

### Input with Icon
```tsx
<div className="relative">
  <Input
    type="text"
    value={search}
    onChange={setSearch}
    className="pl-10"
  />
  <span className="absolute left-3 top-1/2 -translate-y-1/2">🔍</span>
</div>
```

---

## Performance Benefits

- **Bundle Size**: Shared components reduce duplication
- **Consistency**: Design tokens from globals.css used everywhere
- **Maintenance**: Update once, changes propagate everywhere
- **Type Safety**: Full TypeScript support with IntelliSense
- **Accessibility**: ARIA labels and keyboard navigation built-in

---

## Next Steps

1. **Refactor LoginForm.tsx** - Replace custom inputs with Input component
2. **Refactor Dashboard navigation** - Use Navigation component
3. **Update resume cards** - Use Card component with Badge for status
4. **Standardize buttons** - Replace all custom buttons with Button component
5. **Test everything** - Ensure no regressions

File locations:
- Button: `/Users/evanstoudt/Documents/File Cabinet/Coding/resumaker/frontend/components/ui/Button.tsx`
- Card: `/Users/evanstoudt/Documents/File Cabinet/Coding/resumaker/frontend/components/ui/Card.tsx`
- Input: `/Users/evanstoudt/Documents/File Cabinet/Coding/resumaker/frontend/components/ui/Input.tsx`
- Badge: `/Users/evanstoudt/Documents/File Cabinet/Coding/resumaker/frontend/components/ui/Badge.tsx`
- Navigation: `/Users/evanstoudt/Documents/File Cabinet/Coding/resumaker/frontend/components/ui/Navigation.tsx`
