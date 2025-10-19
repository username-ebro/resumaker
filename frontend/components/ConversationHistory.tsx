'use client';

import { useState } from 'react';
import { useToast } from './Toast';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ConversationHistoryProps {
  messages: Message[];
  onAddMore: () => void;
  onEdit: (editInstructions: string) => void;
}

export default function ConversationHistory({
  messages,
  onAddMore,
  onEdit
}: ConversationHistoryProps) {
  const { showToast } = useToast();
  const [isExpanded, setIsExpanded] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editInstructions, setEditInstructions] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);

  const copyToClipboard = () => {
    const transcript = messages
      .map(msg => {
        const speaker = msg.role === 'assistant' ? 'AI' : 'You';
        return `${speaker}: ${msg.content}`;
      })
      .join('\n\n');

    navigator.clipboard.writeText(transcript);
    showToast('Conversation copied to clipboard!', 'success');
  };

  const startVoiceRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      const chunks: Blob[] = [];

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunks.push(e.data);
        }
      };

      recorder.onstop = async () => {
        const audioBlob = new Blob(chunks, { type: 'audio/webm' });
        await transcribeAndSubmit(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };

      setMediaRecorder(recorder);
      recorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error('Microphone access denied:', err);
      showToast('Please allow microphone access to use voice input', 'error');
    }
  };

  const stopVoiceRecording = () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
      mediaRecorder.stop();
      setIsRecording(false);
    }
  };

  const transcribeAndSubmit = async (audioBlob: Blob) => {
    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const formData = new FormData();
      formData.append('audio', audioBlob, 'recording.webm');

      const response = await fetch(`${API_URL}/conversation/transcribe`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (data.success && data.transcript) {
        setEditInstructions(data.transcript);
      }
    } catch (err) {
      console.error('Transcription failed:', err);
      showToast('Failed to transcribe audio. Please try typing instead.', 'error');
    }
  };

  const handleSubmitEdit = () => {
    if (editInstructions.trim()) {
      onEdit(editInstructions);
      setEditInstructions('');
      setIsEditing(false);
    }
  };

  if (messages.length === 0) return null;

  return (
    <div className="mt-6 pt-6 border-t-4 border-black">
      <div className="brutal-box brutal-shadow p-4">
        {/* Header */}
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-sm font-bold uppercase">📝 Conversation History</h3>
          <div className="flex gap-2">
            <button
              onClick={copyToClipboard}
              className="brutal-btn text-xs px-3 py-1"
            >
              📋 Copy All
            </button>
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="brutal-btn brutal-btn-seafoam text-xs px-3 py-1"
            >
              {isExpanded ? '▲ Collapse' : '▼ Expand'}
            </button>
          </div>
        </div>

        {/* Messages (collapsible) */}
        {isExpanded && (
          <div className="space-y-3 mb-4 max-h-96 overflow-y-auto">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`p-3 brutal-box text-sm ${
                  msg.role === 'assistant'
                    ? 'brutal-box-seafoam'
                    : 'bg-white'
                }`}
              >
                <p className="text-xs font-bold mb-1 uppercase">
                  {msg.role === 'assistant' ? '🤖 AI' : '👤 You'}
                </p>
                <p className="whitespace-pre-wrap">{msg.content}</p>
              </div>
            ))}
          </div>
        )}

        {/* Action buttons */}
        {!isEditing ? (
          <div className="flex gap-2">
            <button
              onClick={onAddMore}
              className="brutal-btn brutal-btn-primary brutal-shadow flex-1"
            >
              ➕ Add More Details
            </button>
            <button
              onClick={() => setIsEditing(true)}
              className="brutal-btn brutal-btn-seafoam brutal-shadow flex-1"
            >
              ✏️ Edit/Fix Something
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            <div className="brutal-box-seafoam p-3">
              <p className="text-xs font-bold uppercase mb-2">
                What would you like to change?
              </p>
              <p className="text-xs mb-3">
                Tell me what needs to be added, edited, or corrected
              </p>
            </div>

            {/* Voice or text input */}
            <div className="flex gap-2 items-center mb-2">
              <button
                onClick={isRecording ? stopVoiceRecording : startVoiceRecording}
                className={`brutal-btn ${isRecording ? 'bg-red-500 text-white border-red-500' : 'brutal-btn-seafoam'} brutal-shadow px-4 py-2`}
              >
                {isRecording ? (
                  <>
                    <span className="inline-block animate-pulse mr-2">🔴</span>
                    Stop Recording
                  </>
                ) : (
                  <>🎤 Voice</>
                )}
              </button>
              <span className="text-xs text-gray-600">or type below:</span>
            </div>

            <textarea
              value={editInstructions}
              onChange={(e) => setEditInstructions(e.target.value)}
              placeholder="E.g., 'I actually worked there from 2020-2023, not 2021' or 'Add that I also used Python and SQL'"
              className="brutal-input w-full h-24"
            />

            <div className="flex gap-2">
              <button
                onClick={() => {
                  setIsEditing(false);
                  setEditInstructions('');
                }}
                className="brutal-btn flex-1"
              >
                Cancel
              </button>
              <button
                onClick={handleSubmitEdit}
                disabled={!editInstructions.trim()}
                className="brutal-btn brutal-btn-primary brutal-shadow flex-1 disabled:opacity-50"
              >
                ✅ Submit Changes
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
