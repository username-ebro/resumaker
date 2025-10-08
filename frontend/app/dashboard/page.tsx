'use client';

import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';
import { useRouter } from 'next/navigation';
import UploadResume from '@/components/UploadResume';
import ImportConversation from '@/components/ImportConversation';
import ConversationInterface from '@/components/ConversationInterface';

export default function DashboardPage() {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'conversation' | 'upload' | 'import'>('conversation');
  const router = useRouter();

  useEffect(() => {
    const checkUser = async () => {
      const { data: { user } } = await supabase.auth.getUser();

      if (!user) {
        router.push('/auth/login');
        return;
      }

      setUser(user);
      setLoading(false);
    };

    checkUser();
  }, [router]);

  const handleLogout = async () => {
    await supabase.auth.signOut();
    router.push('/');
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold">Resumaker</h1>
          <button
            onClick={handleLogout}
            className="px-4 py-2 text-sm border rounded hover:bg-gray-50"
          >
            Logout
          </button>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <h2 className="text-2xl font-bold mb-6">Welcome, {user?.email}</h2>

        <div className="mb-6 flex gap-4">
          <button
            onClick={() => setActiveTab('conversation')}
            className={`px-4 py-2 rounded ${
              activeTab === 'conversation' ? 'bg-blue-600 text-white' : 'bg-white border'
            }`}
          >
            Conversation
          </button>
          <button
            onClick={() => setActiveTab('upload')}
            className={`px-4 py-2 rounded ${
              activeTab === 'upload' ? 'bg-blue-600 text-white' : 'bg-white border'
            }`}
          >
            Upload
          </button>
          <button
            onClick={() => setActiveTab('import')}
            className={`px-4 py-2 rounded ${
              activeTab === 'import' ? 'bg-blue-600 text-white' : 'bg-white border'
            }`}
          >
            Import
          </button>
        </div>

        <div>
          {activeTab === 'conversation' && <ConversationInterface userId={user.id} />}
          {activeTab === 'upload' && <UploadResume />}
          {activeTab === 'import' && <ImportConversation />}
        </div>
      </main>
    </div>
  );
}
