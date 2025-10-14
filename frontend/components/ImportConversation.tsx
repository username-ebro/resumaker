'use client';

import { useState } from 'react';

export default function ImportConversation() {
  const [conversationText, setConversationText] = useState('');
  const [platform, setPlatform] = useState('chatgpt');
  const [parsing, setParsing] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  const handleImport = async () => {
    setParsing(true);
    setError('');

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/imports/parse`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          conversation_text: conversationText,
          source_platform: platform,
        }),
      });

      const data = await response.json();

      if (data.success) {
        setResult(data.extracted_data);
      } else {
        setError('Parsing failed');
      }
    } catch (err: any) {
      setError(err.message || 'Import failed');
    } finally {
      setParsing(false);
    }
  };

  return (
    <div className="brutal-box brutal-shadow p-6">
      <h3 className="text-lg mb-4">Import Conversation</h3>

      <div className="mb-4">
        <label className="block text-xs font-bold mb-2 uppercase">Source</label>
        <select
          value={platform}
          onChange={(e) => setPlatform(e.target.value)}
          className="brutal-input"
        >
          <option value="chatgpt">ChatGPT</option>
          <option value="claude">Claude</option>
          <option value="other">Other</option>
        </select>
      </div>

      <div className="mb-4">
        <label className="block text-xs font-bold mb-2 uppercase">
          Paste Conversation
        </label>
        <textarea
          value={conversationText}
          onChange={(e) => setConversationText(e.target.value)}
          className="brutal-input h-48"
          placeholder="Paste entire conversation..."
        />
      </div>

      {error && (
        <div className="p-3 brutal-box bg-red-50 mb-4">
          <span className="font-bold">ERROR:</span> {error}
        </div>
      )}

      <button
        onClick={handleImport}
        disabled={!conversationText || parsing}
        className="brutal-btn brutal-btn-primary brutal-shadow w-full disabled:opacity-50 flex items-center justify-center gap-2"
      >
        {parsing && (
          <div className="cool-spinner h-5 w-5 border-2 border-white border-t-transparent rounded-full"></div>
        )}
        {parsing ? 'Parsing...' : 'Import & Extract'}
      </button>

      {result && (
        <div className="mt-4 p-4 brutal-box-seafoam brutal-shadow-seafoam">
          <p className="font-bold mb-2">✓ IMPORTED</p>
          <div className="text-sm">
            <p>Accomplishments: {result.accomplishments?.length || 0}</p>
            <p>Skills: {result.skills?.technical?.length || 0} technical</p>
            <p>Experience entries: {result.experience?.length || 0}</p>
          </div>
        </div>
      )}
    </div>
  );
}
