"use client";

import React, { useState } from 'react';
import FileUpload from '@/components/FileUpload';
import TranscriptionDisplay from '@/components/TranscriptionDisplay';

export default function HomePage() {
  const [transcription, setTranscription] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false); // Renamed from isUploading for clarity

  const handleFileUpload = async (file: File) => {
    setIsLoading(true);
    setTranscription(null);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/transcribe', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Unknown error occurred' }));
        throw new Error(errorData.message || `Server error: ${response.statusText}`);
      }

      const result = await response.json();
      if (result.transcription) {
        setTranscription(result.transcription);
      } else if (result.error) {
        setError(result.error);
      } else {
        setError('Received an unexpected response from the server.');
      }
    } catch (err: any) {
      setError(err.message || 'Failed to upload and transcribe the file.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center py-8">
      <FileUpload onFileUpload={handleFileUpload} isUploading={isLoading} />
      <TranscriptionDisplay transcription={transcription} error={error} isLoading={isLoading} />
    </div>
  );
}
