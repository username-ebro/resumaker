'use client';

import { useState } from 'react';
import { Button, Card, Input, Badge, Navigation } from '@/components/ui';

export default function ComponentsDemo() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  const handleTestAction = () => {
    setLoading(true);
    setTimeout(() => setLoading(false), 2000);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation
        user={{ email: 'demo@resumaker.com', name: 'Demo User' }}
        onLogout={() => alert('Logout clicked')}
        links={[
          { label: 'Dashboard', href: '/dashboard', icon: '🏠' },
          { label: 'Resumes', href: '/resumes', icon: '📄' },
        ]}
        badge={{ count: 5, href: '/knowledge' }}
      />

      <main className="max-w-7xl mx-auto px-6 py-8 space-y-12">
        {/* Header */}
        <div className="brutal-box-seafoam brutal-shadow-seafoam p-8">
          <h1 className="text-4xl mb-3">Component Library Demo</h1>
          <p className="text-sm text-gray-700">
            A showcase of all reusable components in the Resumaker design system
          </p>
        </div>

        {/* Buttons Section */}
        <section>
          <Card variant="seafoam" padding="lg">
            <h2 className="text-2xl mb-6">Buttons</h2>

            <div className="space-y-6">
              {/* Variants */}
              <div>
                <h3 className="text-sm font-bold uppercase mb-3 text-gray-600">Variants</h3>
                <div className="flex flex-wrap gap-3">
                  <Button variant="primary">Primary Button</Button>
                  <Button variant="secondary">Secondary Button</Button>
                  <Button variant="danger">Danger Button</Button>
                  <Button variant="ghost">Ghost Button</Button>
                </div>
              </div>

              {/* Sizes */}
              <div>
                <h3 className="text-sm font-bold uppercase mb-3 text-gray-600">Sizes</h3>
                <div className="flex flex-wrap items-center gap-3">
                  <Button variant="primary" size="sm">Small</Button>
                  <Button variant="primary" size="md">Medium</Button>
                  <Button variant="primary" size="lg">Large</Button>
                </div>
              </div>

              {/* States */}
              <div>
                <h3 className="text-sm font-bold uppercase mb-3 text-gray-600">States</h3>
                <div className="flex flex-wrap gap-3">
                  <Button variant="primary" loading={loading} onClick={handleTestAction}>
                    {loading ? 'Loading...' : 'Click to Load'}
                  </Button>
                  <Button variant="secondary" disabled>Disabled Button</Button>
                </div>
              </div>

              {/* With Icons */}
              <div>
                <h3 className="text-sm font-bold uppercase mb-3 text-gray-600">With Icons</h3>
                <div className="flex flex-wrap gap-3">
                  <Button variant="primary" icon="✨">Generate Resume</Button>
                  <Button variant="danger" icon="🗑️">Delete</Button>
                  <Button variant="secondary" icon="📄">View Resumes</Button>
                  <Button variant="ghost" icon="⚙️">Settings</Button>
                </div>
              </div>
            </div>
          </Card>
        </section>

        {/* Cards Section */}
        <section>
          <Card variant="seafoam" padding="lg">
            <h2 className="text-2xl mb-6">Cards</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <Card variant="default" padding="md">
                <h3 className="text-lg font-bold mb-2">Default Card</h3>
                <p className="text-sm text-gray-600">
                  White background with 6px shadow
                </p>
              </Card>

              <Card variant="elevated" padding="md">
                <h3 className="text-lg font-bold mb-2">Elevated Card</h3>
                <p className="text-sm text-gray-600">
                  10px shadow for prominence
                </p>
              </Card>

              <Card variant="dark" padding="md">
                <h3 className="text-lg font-bold mb-2">Dark Card</h3>
                <p className="text-sm text-gray-300">
                  Dark gradient background
                </p>
              </Card>

              <Card variant="outline" padding="md">
                <h3 className="text-lg font-bold mb-2">Outline Card</h3>
                <p className="text-sm text-gray-600">
                  Just border, no shadow
                </p>
              </Card>

              <Card variant="seafoam" padding="md">
                <h3 className="text-lg font-bold mb-2">Seafoam Card</h3>
                <p className="text-sm text-gray-700">
                  Seafoam background with shadow
                </p>
              </Card>

              <Card variant="default" padding="md" hover onClick={() => alert('Card clicked!')}>
                <h3 className="text-lg font-bold mb-2">Hoverable Card</h3>
                <p className="text-sm text-gray-600">
                  Lifts on hover (click me!)
                </p>
              </Card>
            </div>

            <div className="mt-6">
              <h3 className="text-sm font-bold uppercase mb-3 text-gray-600">Padding Options</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card variant="outline" padding="sm">
                  <p className="text-xs font-bold">Small Padding (p-4)</p>
                </Card>
                <Card variant="outline" padding="md">
                  <p className="text-xs font-bold">Medium Padding (p-6)</p>
                </Card>
                <Card variant="outline" padding="lg">
                  <p className="text-xs font-bold">Large Padding (p-8)</p>
                </Card>
              </div>
            </div>
          </Card>
        </section>

        {/* Inputs Section */}
        <section>
          <Card variant="seafoam" padding="lg">
            <h2 className="text-2xl mb-6">Inputs</h2>

            <div className="max-w-2xl space-y-6">
              {/* Text Input */}
              <Input
                label="Email Address"
                type="email"
                value={email}
                onChange={setEmail}
                placeholder="you@example.com"
                helperText="We'll never share your email"
              />

              {/* Password Input */}
              <Input
                label="Password"
                type="password"
                value={password}
                onChange={setPassword}
                placeholder="Enter your password"
                required
              />

              {/* Textarea */}
              <Input
                label="Description"
                type="textarea"
                value={description}
                onChange={setDescription}
                placeholder="Enter a detailed description..."
                rows={4}
                helperText="Maximum 500 characters"
              />

              {/* Error State */}
              <Input
                label="Email with Error"
                type="email"
                value=""
                onChange={() => {}}
                error="This field is required"
                required
              />

              {/* Disabled State */}
              <Input
                label="Disabled Input"
                type="text"
                value="Cannot edit this"
                onChange={() => {}}
                disabled
              />
            </div>
          </Card>
        </section>

        {/* Badges Section */}
        <section>
          <Card variant="seafoam" padding="lg">
            <h2 className="text-2xl mb-6">Badges</h2>

            <div className="space-y-6">
              {/* Variants */}
              <div>
                <h3 className="text-sm font-bold uppercase mb-3 text-gray-600">Variants</h3>
                <div className="flex flex-wrap gap-3">
                  <Badge variant="default">Default</Badge>
                  <Badge variant="success">Success</Badge>
                  <Badge variant="warning">Warning</Badge>
                  <Badge variant="error">Error</Badge>
                  <Badge variant="info">Info</Badge>
                </div>
              </div>

              {/* Sizes */}
              <div>
                <h3 className="text-sm font-bold uppercase mb-3 text-gray-600">Sizes</h3>
                <div className="flex flex-wrap items-center gap-3">
                  <Badge variant="success" size="sm">Small</Badge>
                  <Badge variant="success" size="md">Medium</Badge>
                  <Badge variant="success" size="lg">Large</Badge>
                </div>
              </div>

              {/* Use Cases */}
              <div>
                <h3 className="text-sm font-bold uppercase mb-3 text-gray-600">Common Use Cases</h3>
                <div className="space-y-3">
                  <div className="flex items-center gap-3">
                    <span className="text-sm font-medium">Resume Status:</span>
                    <Badge variant="success">Verified</Badge>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-sm font-medium">Job Application:</span>
                    <Badge variant="warning">Pending Review</Badge>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-sm font-medium">Processing:</span>
                    <Badge variant="error">Failed</Badge>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-sm font-medium">Knowledge Base:</span>
                    <Badge variant="info">5 Facts Pending</Badge>
                  </div>
                </div>
              </div>
            </div>
          </Card>
        </section>

        {/* Navigation Section */}
        <section>
          <Card variant="seafoam" padding="lg">
            <h2 className="text-2xl mb-6">Navigation</h2>
            <p className="text-sm text-gray-700 mb-4">
              The navigation component is shown at the top of this page. It includes:
            </p>
            <ul className="list-disc list-inside space-y-2 text-sm text-gray-700">
              <li>Responsive design (hamburger menu on mobile)</li>
              <li>Active state highlighting</li>
              <li>User dropdown menu</li>
              <li>Badge support for notifications</li>
              <li>Icon support for links</li>
              <li>Sticky positioning</li>
            </ul>
          </Card>
        </section>

        {/* Combined Example */}
        <section>
          <Card variant="seafoam" padding="lg">
            <h2 className="text-2xl mb-6">Combined Example</h2>
            <p className="text-sm text-gray-700 mb-6">
              Real-world example using multiple components together
            </p>

            <Card variant="elevated" padding="lg">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-bold mb-1">Senior Product Manager</h3>
                  <div className="flex gap-2 mb-2">
                    <Badge variant="success">ATS Optimized</Badge>
                    <Badge variant="info">Updated Today</Badge>
                  </div>
                </div>
                <Button variant="primary" icon="📄">
                  View Resume
                </Button>
              </div>

              <div className="space-y-4 mb-6">
                <div>
                  <p className="text-sm font-bold mb-1">Company</p>
                  <p className="text-sm text-gray-600">MagicSchool AI</p>
                </div>
                <div>
                  <p className="text-sm font-bold mb-1">Match Score</p>
                  <div className="flex items-center gap-2">
                    <div className="flex-1 bg-gray-200 h-3 brutal-box">
                      <div className="bg-green-500 h-full" style={{ width: '87%' }} />
                    </div>
                    <span className="text-sm font-bold">87%</span>
                  </div>
                </div>
              </div>

              <div className="flex gap-3">
                <Button variant="primary" className="flex-1">
                  Download PDF
                </Button>
                <Button variant="secondary">Edit</Button>
                <Button variant="danger" icon="🗑️">Delete</Button>
              </div>
            </Card>
          </Card>
        </section>

        {/* Code Examples */}
        <section>
          <Card variant="dark" padding="lg">
            <h2 className="text-2xl mb-6">Import & Usage</h2>

            <div className="space-y-4">
              <div>
                <p className="text-sm font-bold mb-2 text-seafoam-solid">1. Import Components</p>
                <pre className="bg-black p-4 rounded text-xs overflow-x-auto border-2 border-white">
                  <code className="text-white">
{`import { Button, Card, Input, Badge, Navigation } from '@/components/ui';`}
                  </code>
                </pre>
              </div>

              <div>
                <p className="text-sm font-bold mb-2 text-seafoam-solid">2. Use in Your Components</p>
                <pre className="bg-black p-4 rounded text-xs overflow-x-auto border-2 border-white">
                  <code className="text-white">
{`<Card variant="elevated" padding="lg">
  <h3>My Card Title</h3>
  <Input
    label="Email"
    type="email"
    value={email}
    onChange={setEmail}
  />
  <Button variant="primary" onClick={handleSubmit}>
    Submit
  </Button>
</Card>`}
                  </code>
                </pre>
              </div>
            </div>
          </Card>
        </section>
      </main>
    </div>
  );
}
