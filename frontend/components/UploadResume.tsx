'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { supabase } from '@/lib/supabase';

export default function UploadResume() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const getUser = async () => {
      const {
        data: { user },
      } = await supabase.auth.getUser();
      setUser(user);
    };
    getUser();
  }, []);

  const handleUpload = async () => {
    if (!file || !user) return;

    setUploading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', user.id);

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/upload/resume`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      console.log('Upload response:', data);

      if (data.success) {
        setResult(data);

        // Check knowledge extraction status
        if (data.knowledge_extraction) {
          console.log('Knowledge extraction result:', data.knowledge_extraction);

          if (data.knowledge_extraction.success) {
            console.log(`✅ Extracted ${data.knowledge_extraction.entities_extracted} entities`);
          } else {
            console.log('❌ Knowledge extraction failed:', data.knowledge_extraction.error);
            setError(`Knowledge extraction failed: ${data.knowledge_extraction.error}`);
          }
        } else {
          console.log('⚠️ No knowledge extraction in response (user_id missing?)');
          setError('Knowledge extraction skipped - make sure you are logged in');
        }

        // If knowledge was extracted, redirect to confirmation screen after 2s
        if (data.knowledge_extraction?.success) {
          setTimeout(() => {
            router.push('/dashboard/knowledge/confirm');
          }, 2000);
        }
      } else {
        setError('Upload failed');
      }
    } catch (err: any) {
      setError(err.message || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="brutal-box brutal-shadow p-6">
      <h3 className="text-lg mb-4">Upload Resume</h3>

      <div className="brutal-box border-dashed p-8 text-center mb-4">
        <input
          type="file"
          accept=".pdf,.jpg,.jpeg,.png"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="hidden"
          id="file-upload"
        />
        <label htmlFor="file-upload" className="cursor-pointer">
          <div className="text-gray-600">
            {file ? (
              <p>{file.name}</p>
            ) : (
              <>
                <p className="text-lg mb-2">📄 Click to upload</p>
                <p className="text-sm">PDF, JPG, or PNG</p>
              </>
            )}
          </div>
        </label>
      </div>

      {error && (
        <div className="p-3 brutal-box bg-red-50 mb-4">
          <span className="font-bold">ERROR:</span> {error}
        </div>
      )}

      {file && (
        <button
          onClick={handleUpload}
          disabled={uploading}
          className="brutal-btn brutal-btn-primary brutal-shadow w-full disabled:opacity-50 flex items-center justify-center gap-2"
        >
          {uploading && (
            <div className="cool-spinner h-5 w-5 border-2 border-white border-t-transparent rounded-full"></div>
          )}
          {uploading ? 'Extracting...' : 'Upload & Extract'}
        </button>
      )}

      {result && (
        <div className="mt-4 p-4 brutal-box-seafoam brutal-shadow-seafoam">
          <p className="font-bold mb-2">✓ EXTRACTED</p>

          {/* Knowledge extraction results */}
          {result.knowledge_extraction?.success && (
            <div className="mb-4 p-3 brutal-box bg-green-50">
              <p className="font-bold text-green-800 mb-1">
                🎉 {result.knowledge_extraction.entities_extracted} facts extracted!
              </p>
              <p className="text-xs text-green-700">
                Redirecting to confirmation screen...
              </p>
            </div>
          )}

          {/* Raw extraction data (collapsed) */}
          <details className="mt-2">
            <summary className="cursor-pointer text-xs font-bold mb-2">
              View raw data
            </summary>
            <pre className="text-xs overflow-auto max-h-64">
              {JSON.stringify(result.extracted_data, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </div>
  );
}
