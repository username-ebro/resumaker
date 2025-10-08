'use client';

import { useState } from 'react';

type Message = {
  role: 'user' | 'assistant';
  content: string;
};

export default function ConversationInterface({ userId }: { userId: string }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [userInput, setUserInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [started, setStarted] = useState(false);

  const startConversation = async () => {
    setLoading(true);

    try {
      const response = await fetch('${API_URL}/conversation/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId }),
      });

      const data = await response.json();

      if (data.success) {
        setCurrentQuestion(data.question);
        setMessages([{ role: 'assistant', content: data.question }]);
        setStarted(true);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const sendResponse = async () => {
    if (!userInput.trim()) return;

    const newMessages = [...messages, { role: 'user' as const, content: userInput }];
    setMessages(newMessages);
    setUserInput('');
    setLoading(true);

    try {
      const response = await fetch('${API_URL}/conversation/continue', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          conversation_id: userId,
          user_response: userInput,
          conversation_history: newMessages,
        }),
      });

      const data = await response.json();

      if (data.success && data.next_question) {
        setMessages([...newMessages, { role: 'assistant', content: data.next_question }]);
        setCurrentQuestion(data.next_question);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (!started) {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">AI Conversation</h3>
        <p className="text-gray-600 mb-4">
          I'll ask you questions about your experience to build your resume.
        </p>
        <button
          onClick={startConversation}
          disabled={loading}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Starting...' : 'Start Conversation'}
        </button>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">AI Conversation</h3>

      <div className="space-y-4 mb-4 max-h-96 overflow-y-auto">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`p-3 rounded ${
              msg.role === 'assistant'
                ? 'bg-blue-50 border-l-4 border-blue-500'
                : 'bg-gray-50 border-l-4 border-gray-500'
            }`}
          >
            <p className="text-sm font-semibold mb-1">
              {msg.role === 'assistant' ? 'Resumaker' : 'You'}
            </p>
            <p>{msg.content}</p>
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendResponse()}
          placeholder="Type your answer..."
          className="flex-1 px-4 py-2 border rounded"
          disabled={loading}
        />
        <button
          onClick={sendResponse}
          disabled={loading || !userInput.trim()}
          className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? '...' : 'Send'}
        </button>
      </div>
    </div>
  );
}
