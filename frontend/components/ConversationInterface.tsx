'use client';

import { useState } from 'react';
import ConversationHistory from './ConversationHistory';

type Message = {
  role: 'user' | 'assistant';
  content: string;
};

type InputMode = 'voice' | 'text';

export default function ConversationInterface({ userId }: { userId: string }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [userInput, setUserInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [started, setStarted] = useState(false);
  const [inputMode, setInputMode] = useState<InputMode>('voice');
  const [isRecording, setIsRecording] = useState(false);

  // Voice recording
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
  const [audioChunks, setAudioChunks] = useState<Blob[]>([]);
  const [transcribing, setTranscribing] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [endingConversation, setEndingConversation] = useState(false);

  // Job posting state - NOT shown by default, only for resume generation
  const [showJobInput, setShowJobInput] = useState(false);
  const [jobTitle, setJobTitle] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [jobUrl, setJobUrl] = useState('');
  const [analyzingJob, setAnalyzingJob] = useState(false);

  const startConversation = async () => {
    setLoading(true);

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/conversation/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId }),
      });

      const data = await response.json();

      if (data.success) {
        setCurrentQuestion(data.question);
        setMessages([{ role: 'assistant', content: data.question }]);
        setStarted(true);
        setConversationId(data.conversation_id || userId); // Store conversation ID
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
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/conversation/continue`, {
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

  const analyzeJobPosting = async () => {
    if (!jobDescription.trim()) return;

    setAnalyzingJob(true);
    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/jobs/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          job_title: jobTitle,
          job_description: jobDescription,
          job_url: jobUrl,
        }),
      });

      const data = await response.json();
      if (data.success) {
        setShowJobInput(false);
        startConversation();
      }
    } catch (err) {
      console.error(err);
    } finally {
      setAnalyzingJob(false);
    }
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
        await transcribeAndSend(audioBlob);

        // Stop all tracks to turn off microphone
        stream.getTracks().forEach(track => track.stop());
      };

      setAudioChunks(chunks);
      setMediaRecorder(recorder);
      recorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error('Microphone access denied:', err);
      alert('Please allow microphone access to use voice input');
    }
  };

  const stopVoiceRecording = () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
      mediaRecorder.stop();
      setIsRecording(false);
    }
  };

  const transcribeAndSend = async (audioBlob: Blob) => {
    setTranscribing(true);

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
        // Set the transcribed text and send it
        setUserInput(data.transcript);

        // Send the transcribed text as response
        const newMessages = [...messages, { role: 'user' as const, content: data.transcript }];
        setMessages(newMessages);
        setUserInput('');
        setLoading(true);

        try {
          const conversationResponse = await fetch(`${API_URL}/conversation/continue`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              conversation_id: userId,
              user_response: data.transcript,
              conversation_history: newMessages,
            }),
          });

          const conversationData = await conversationResponse.json();

          if (conversationData.success && conversationData.next_question) {
            setMessages([...newMessages, { role: 'assistant', content: conversationData.next_question }]);
            setCurrentQuestion(conversationData.next_question);
          }
        } catch (err) {
          console.error(err);
        } finally {
          setLoading(false);
        }
      }
    } catch (err) {
      console.error('Transcription failed:', err);
      alert('Failed to transcribe audio. Please try again or use text input.');
    } finally {
      setTranscribing(false);
    }
  };

  const endConversation = async () => {
    if (!conversationId) return;

    setEndingConversation(true);

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/conversation/end`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          conversation_id: conversationId,
          user_id: userId,
          conversation_history: messages,
        }),
      });

      const data = await response.json();

      if (data.success) {
        // Redirect to confirmation screen
        window.location.href = '/dashboard/knowledge/confirm';
      }
    } catch (err) {
      console.error('Error ending conversation:', err);
      alert('Failed to process conversation. Please try again.');
    } finally {
      setEndingConversation(false);
    }
  };

  const handleAddMore = () => {
    // Switch to text input mode for easier editing
    setInputMode('text');
    setUserInput('');
    // Scroll to input
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
  };

  const handleEditConversation = async (editInstructions: string) => {
    // Add the edit instructions as a new user message
    const newMessages = [...messages, { role: 'user' as const, content: editInstructions }];
    setMessages(newMessages);
    setLoading(true);

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/conversation/continue`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          conversation_id: conversationId || userId,
          user_response: editInstructions,
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

  // Show job posting input first
  if (showJobInput) {
    return (
      <div className="space-y-6">
        <div className="brutal-box-seafoam brutal-shadow-seafoam p-6">
          <h3 className="text-xl mb-2">New Resume</h3>
          <p className="text-sm">Let's start by understanding the job you're applying for</p>
        </div>

        <div className="brutal-box brutal-shadow p-6">
          <h4 className="text-sm font-bold mb-4 uppercase">Job Details</h4>

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
              <label className="block text-xs font-bold mb-2 uppercase">Job Posting URL (Optional)</label>
              <input
                type="text"
                value={jobUrl}
                onChange={(e) => setJobUrl(e.target.value)}
                placeholder="https://..."
                className="brutal-input w-full"
              />
            </div>

            <div>
              <label className="block text-xs font-bold mb-2 uppercase">Job Description</label>
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the full job description here..."
                className="brutal-input w-full h-48"
              />
            </div>

            <button
              onClick={analyzeJobPosting}
              disabled={!jobDescription.trim() || analyzingJob}
              className="brutal-btn brutal-btn-primary brutal-shadow w-full disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {analyzingJob && (
                <div className="cool-spinner h-5 w-5 border-2 border-white border-t-transparent rounded-full"></div>
              )}
              {analyzingJob ? 'Analyzing Job...' : 'Analyze & Start Conversation'}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Show conversation start screen
  if (!started) {
    return (
      <div className="brutal-box brutal-shadow p-6">
        <h3 className="text-lg mb-4">AI Conversation</h3>
        <p className="mb-6">
          I'll ask questions about your experience to build your resume.
        </p>

        <div className="mb-6">
          <p className="text-xs font-bold mb-3 uppercase">Choose Input Method</p>
          <div className="flex gap-3">
            <button
              onClick={() => setInputMode('voice')}
              className={`brutal-btn ${inputMode === 'voice' ? 'brutal-btn-primary' : 'brutal-btn-seafoam'} brutal-shadow flex-1`}
            >
              🎤 Voice
            </button>
            <button
              onClick={() => setInputMode('text')}
              className={`brutal-btn ${inputMode === 'text' ? 'brutal-btn-primary' : 'brutal-btn-seafoam'} brutal-shadow flex-1`}
            >
              ⌨️ Text
            </button>
          </div>
        </div>

        <button
          onClick={startConversation}
          disabled={loading}
          className="brutal-btn brutal-btn-primary brutal-shadow w-full disabled:opacity-50 flex items-center justify-center gap-2"
        >
          {loading && (
            <div className="cool-spinner h-5 w-5 border-2 border-white border-t-transparent rounded-full"></div>
          )}
          {loading ? 'Starting...' : 'Start Conversation'}
        </button>
      </div>
    );
  }

  return (
    <div className="brutal-box brutal-shadow p-6">
      <h3 className="text-lg mb-6">AI Conversation</h3>

      <div className="space-y-4 mb-6 max-h-96 overflow-y-auto">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`p-4 brutal-box ${
              msg.role === 'assistant'
                ? 'brutal-box-seafoam'
                : 'bg-white'
            }`}
          >
            <p className="text-xs font-bold mb-2 uppercase">
              {msg.role === 'assistant' ? '🤖 Resumaker' : '👤 You'}
            </p>
            <p>{msg.content}</p>
          </div>
        ))}
      </div>

      {/* Input method toggle */}
      <div className="mb-4 flex gap-2 justify-center">
        <button
          onClick={() => setInputMode('voice')}
          className={`brutal-btn ${inputMode === 'voice' ? 'brutal-btn-primary' : 'brutal-btn-seafoam'} text-xs px-3 py-1`}
        >
          🎤 Voice
        </button>
        <button
          onClick={() => setInputMode('text')}
          className={`brutal-btn ${inputMode === 'text' ? 'brutal-btn-primary' : 'brutal-btn-seafoam'} text-xs px-3 py-1`}
        >
          ⌨️ Text
        </button>
      </div>

      {/* Voice input */}
      {inputMode === 'voice' && (
        <div className="text-center">
          <button
            onClick={isRecording ? stopVoiceRecording : startVoiceRecording}
            disabled={loading || transcribing}
            className={`brutal-btn ${isRecording ? 'bg-red-500 text-white border-red-500' : 'brutal-btn-primary'} brutal-shadow disabled:opacity-50 px-12 py-4 transition-all`}
          >
            {transcribing ? (
              <>
                <div className="cool-spinner h-5 w-5 border-2 border-white border-t-transparent rounded-full inline-block mr-2"></div>
                Transcribing...
              </>
            ) : isRecording ? (
              <>
                <span className="inline-block animate-pulse mr-2">🔴</span>
                Stop Recording
              </>
            ) : (
              <>🎤 Start Recording</>
            )}
          </button>
          <p className="text-xs mt-3 text-gray-600">
            {transcribing
              ? 'Converting speech to text...'
              : isRecording
                ? 'Recording... Click to stop and send'
                : 'Click to record your answer'}
          </p>
        </div>
      )}

      {/* Text input */}
      {inputMode === 'text' && (
        <div className="flex gap-2">
          <input
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendResponse()}
            placeholder="Type your answer..."
            className="brutal-input flex-1"
            disabled={loading}
          />
          <button
            onClick={sendResponse}
            disabled={loading || !userInput.trim()}
            className="brutal-btn brutal-btn-primary brutal-shadow disabled:opacity-50 flex items-center gap-2"
          >
            {loading && (
              <div className="cool-spinner h-5 w-5 border-2 border-white border-t-transparent rounded-full"></div>
            )}
            {loading ? 'Sending...' : 'Send'}
          </button>
        </div>
      )}

      {/* Conversation History */}
      {messages.length > 2 && (
        <ConversationHistory
          messages={messages}
          onAddMore={handleAddMore}
          onEdit={handleEditConversation}
        />
      )}

      {/* End Conversation Button */}
      {messages.length > 2 && (
        <div className="mt-6 pt-6 border-t-4 border-black">
          <button
            onClick={endConversation}
            disabled={endingConversation}
            className="brutal-btn brutal-btn-seafoam brutal-shadow w-full disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {endingConversation && (
              <div className="cool-spinner h-5 w-5 border-2 border-black border-t-transparent rounded-full"></div>
            )}
            {endingConversation ? 'Processing...' : '✅ Finish & Review Facts'}
          </button>
          <p className="text-xs text-center mt-2 text-gray-600">
            Extract knowledge and review what I learned about you
          </p>
        </div>
      )}
    </div>
  );
}
