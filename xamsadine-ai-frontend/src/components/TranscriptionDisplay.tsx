"use client";

import React from 'react';

interface TranscriptionDisplayProps {
  transcription: string | null;
  error: string | null;
  isLoading: boolean;
}

const TranscriptionDisplay: React.FC<TranscriptionDisplayProps> = ({ transcription, error, isLoading }) => {
  if (isLoading) {
    return (
      <div className="mt-6 bg-white shadow-md rounded-lg p-6 w-full max-w-md text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto"></div>
        <p className="mt-4 text-gray-600">Processing audio...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mt-6 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg relative w-full max-w-md" role="alert">
        <strong className="font-bold">Error:</strong>
        <span className="block sm:inline"> {error}</span>
      </div>
    );
  }

  if (transcription) {
    return (
      <div className="mt-6 bg-white shadow-md rounded-lg p-6 w-full max-w-md">
        <h2 className="text-xl font-semibold mb-3 text-gray-700">Transcription Result:</h2>
        <div className="bg-gray-50 p-4 rounded-md whitespace-pre-wrap text-gray-800">
          {transcription}
        </div>
      </div>
    );
  }

  return null; // Don't render anything if no transcription, error, or loading state
};

export default TranscriptionDisplay;
