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
      const response = await fetch('${API_URL}/imports/parse', {
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
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">Import Conversation</h3>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">Source</label>
        <select
          value={platform}
          onChange={(e) => setPlatform(e.target.value)}
          className="w-full px-3 py-2 border rounded"
        >
          <option value="chatgpt">ChatGPT</option>
          <option value="claude">Claude</option>
          <option value="other">Other</option>
        </select>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">
          Paste your conversation
        </label>
        <textarea
          value={conversationText}
          onChange={(e) => setConversationText(e.target.value)}
          className="w-full px-3 py-2 border rounded h-48"
          placeholder="Paste your entire conversation here..."
        />
      </div>

      {error && (
        <div className="p-3 bg-red-50 border border-red-200 rounded text-red-600 mb-4">
          {error}
        </div>
      )}

      <button
        onClick={handleImport}
        disabled={!conversationText || parsing}
        className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {parsing ? 'Parsing...' : 'Import & Extract Data'}
      </button>

      {result && (
        <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded">
          <p className="font-semibold text-green-800 mb-2">✅ Imported!</p>
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
