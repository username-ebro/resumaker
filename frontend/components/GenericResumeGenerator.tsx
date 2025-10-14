'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

interface GenericResumeGeneratorProps {
  userId: string;
}

type InputMode = 'voice' | 'text';

export default function GenericResumeGenerator({ userId }: GenericResumeGeneratorProps) {
  const router = useRouter();

  const [inputMode, setInputMode] = useState<InputMode>('text');
  const [userRequest, setUserRequest] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [transcribing, setTranscribing] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Voice recording state
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);

  const placeholderExamples = [
    "I'm applying for a concession stand role. I don't have much experience but I ran a lemonade stand as a kid and I'm good with people.",
    "Create a resume for a software engineering internship focusing on my Python and React skills from my coursework.",
    "I need a resume highlighting my customer service experience for retail positions.",
    "Make me a general resume for entry-level marketing roles, emphasizing my social media experience."
  ];

  const [currentPlaceholder] = useState(
    placeholderExamples[Math.floor(Math.random() * placeholderExamples.length)]
  );

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
        await transcribeAudio(audioBlob);

        // Stop all tracks to turn off microphone
        stream.getTracks().forEach(track => track.stop());
      };

      setMediaRecorder(recorder);
      recorder.start();
      setIsRecording(true);
      setError(null);
    } catch (err) {
      console.error('Microphone access denied:', err);
      setError('Please allow microphone access to use voice input');
    }
  };

  const stopVoiceRecording = () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
      mediaRecorder.stop();
      setIsRecording(false);
    }
  };

  const transcribeAudio = async (audioBlob: Blob) => {
    setTranscribing(true);
    setError(null);

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const formData = new FormData();
      formData.append('audio', audioBlob, 'recording.webm');

      const response = await fetch(`${API_URL}/conversation/transcribe`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Transcription failed');
      }

      const data = await response.json();

      if (data.success && data.transcript) {
        setUserRequest(data.transcript);
      } else {
        throw new Error(data.error || 'Failed to transcribe audio');
      }
    } catch (err) {
      console.error('Transcription failed:', err);
      setError('Failed to transcribe audio. Please try again or use text input.');
    } finally {
      setTranscribing(false);
    }
  };

  const handleGenerate = async () => {
    if (!userRequest.trim()) {
      setError('Please describe what kind of resume you want');
      return;
    }

    setGenerating(true);
    setError(null);

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

      // Generate generic resume using the new endpoint
      const response = await fetch(`${API_URL}/resumes/generate-generic`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          prompt: userRequest, // User's description of what they need
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate resume');
      }

      const data = await response.json();

      if (data.success) {
        // Redirect to resumes list
        router.push('/resumes');
      } else {
        throw new Error(data.error || 'Resume generation failed');
      }
    } catch (err) {
      console.error('Error generating resume:', err);
      setError(err instanceof Error ? err.message : 'Failed to generate resume. Please try again.');
    } finally {
      setGenerating(false);
    }
  };

  const handleRetry = () => {
    setError(null);
    setUserRequest('');
  };

  return (
    <div className="space-y-6">
      <div className="brutal-box-seafoam brutal-shadow-seafoam p-6">
        <h3 className="text-xl mb-2">Quick Generic Resume</h3>
        <p className="text-sm">
          Tell me what kind of resume you need, and I'll create one from your knowledge base
        </p>
      </div>

      <div className="brutal-box brutal-shadow p-6">
        <h4 className="text-sm font-bold mb-4 uppercase">What Kind of Resume Do You Need?</h4>

        {/* Error Display */}
        {error && (
          <div className="brutal-box bg-red-50 border-red-600 p-4 mb-4">
            <p className="text-sm font-bold uppercase mb-1">Error</p>
            <p className="text-sm">{error}</p>
            <button
              onClick={handleRetry}
              className="brutal-btn text-xs px-3 py-1 mt-2"
            >
              Try Again
            </button>
          </div>
        )}

        {/* Input Mode Toggle */}
        <div className="mb-6">
          <p className="text-xs font-bold mb-3 uppercase">Input Method</p>
          <div className="flex gap-3">
            <button
              onClick={() => setInputMode('text')}
              className={`brutal-btn ${inputMode === 'text' ? 'brutal-btn-primary' : 'brutal-btn-seafoam'} brutal-shadow flex-1`}
            >
              ⌨️ Text
            </button>
            <button
              onClick={() => setInputMode('voice')}
              className={`brutal-btn ${inputMode === 'voice' ? 'brutal-btn-primary' : 'brutal-btn-seafoam'} brutal-shadow flex-1`}
            >
              🎤 Voice
            </button>
          </div>
        </div>

        {/* Text Input */}
        {inputMode === 'text' && (
          <div className="space-y-4">
            <div>
              <label className="block text-xs font-bold mb-2 uppercase">Your Request</label>
              <textarea
                value={userRequest}
                onChange={(e) => setUserRequest(e.target.value)}
                placeholder={currentPlaceholder}
                className="brutal-input w-full h-32"
                disabled={generating}
              />
              <p className="text-xs text-gray-600 mt-2">
                💡 Describe the type of role, industry, or skills you want to highlight
              </p>
            </div>

            <button
              onClick={handleGenerate}
              disabled={!userRequest.trim() || generating}
              className="brutal-btn brutal-btn-primary brutal-shadow w-full disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {generating && (
                <div className="cool-spinner h-5 w-5 border-2 border-white border-t-transparent rounded-full"></div>
              )}
              {generating ? 'Generating Resume...' : '✨ Generate Resume'}
            </button>
          </div>
        )}

        {/* Voice Input */}
        {inputMode === 'voice' && (
          <div className="space-y-4">
            <div className="text-center py-8">
              <button
                onClick={isRecording ? stopVoiceRecording : startVoiceRecording}
                disabled={generating || transcribing}
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
                    ? 'Recording... Click to stop'
                    : 'Click to record your resume request'}
              </p>
            </div>

            {/* Show transcribed text */}
            {userRequest && (
              <div>
                <label className="block text-xs font-bold mb-2 uppercase">Transcribed Request</label>
                <textarea
                  value={userRequest}
                  onChange={(e) => setUserRequest(e.target.value)}
                  className="brutal-input w-full h-32"
                  disabled={generating}
                />
                <p className="text-xs text-gray-600 mt-2">
                  You can edit the text above before generating
                </p>

                <button
                  onClick={handleGenerate}
                  disabled={!userRequest.trim() || generating}
                  className="brutal-btn brutal-btn-primary brutal-shadow w-full disabled:opacity-50 flex items-center justify-center gap-2 mt-4"
                >
                  {generating && (
                    <div className="cool-spinner h-5 w-5 border-2 border-white border-t-transparent rounded-full"></div>
                  )}
                  {generating ? 'Generating Resume...' : '✨ Generate Resume'}
                </button>
              </div>
            )}
          </div>
        )}

        {/* Examples */}
        <div className="mt-6 pt-6 border-t-2 border-black border-dashed">
          <p className="text-xs font-bold mb-2 uppercase">Example Requests</p>
          <div className="space-y-2">
            {placeholderExamples.slice(0, 3).map((example, idx) => (
              <div
                key={idx}
                onClick={() => !generating && setUserRequest(example)}
                className="brutal-box p-2 cursor-pointer hover:bg-gray-50 transition-colors"
              >
                <p className="text-xs text-gray-700">{example}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
