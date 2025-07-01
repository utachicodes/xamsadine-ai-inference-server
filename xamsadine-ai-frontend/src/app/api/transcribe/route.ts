import { NextRequest, NextResponse } from 'next/server';
import formidable from 'formidable'; // Using formidable for robust multipart/form-data parsing
import fs from 'fs';

// Disable Next.js body parsing to allow formidable to handle it
export const config = {
  api: {
    bodyParser: false,
  },
};

const FLASK_BACKEND_URL = process.env.FLASK_BACKEND_URL || 'http://localhost:8080/predict';

export async function POST(req: NextRequest) {
  try {
    const formData = await req.formData();
    const file = formData.get('file') as File | null;

    if (!file) {
      return NextResponse.json({ message: 'No file uploaded.' }, { status: 400 });
    }

    // We need to send this file to the Flask backend.
    // Next.js API routes can also use FormData to send files.
    const backendFormData = new FormData();
    backendFormData.append('file', file, file.name);

    console.log(`Forwarding file to Flask backend at ${FLASK_BACKEND_URL}`);

    const flaskResponse = await fetch(FLASK_BACKEND_URL, {
      method: 'POST',
      body: backendFormData,
      // Headers might not be strictly necessary if Flask is expecting multipart/form-data
      // and can infer it, but it's good practice for some backends.
      // However, when sending FormData with fetch, the browser/Node usually sets
      // the Content-Type header correctly with the boundary.
      // headers: {
      //   // 'Content-Type': 'multipart/form-data' // This is often set automatically by fetch for FormData
      // },
    });

    console.log(`Flask backend responded with status: ${flaskResponse.status}`);

    if (!flaskResponse.ok) {
      const errorText = await flaskResponse.text();
      console.error('Flask backend error:', errorText);
      return NextResponse.json({ message: `Error from transcription service: ${flaskResponse.statusText} - ${errorText}` }, { status: flaskResponse.status });
    }

    const flaskResult = await flaskResponse.json();

    // Assuming the flask backend returns something like:
    // {'predictions': [{'filename': '...', 'transcription': {'text': '...'}}]}
    // Or if it's a single file upload from our previous flask modification:
    // {'filename': '...', 'transcription': '...'}
    // The current frontend expects: { transcription: "text" } or { error: "message" }

    if (flaskResult.predictions && flaskResult.predictions.length > 0 && flaskResult.predictions[0].transcription && flaskResult.predictions[0].transcription.text) {
      return NextResponse.json({ transcription: flaskResult.predictions[0].transcription.text });
    } else if (flaskResult.transcription && typeof flaskResult.transcription === 'string') { // For simplified Flask output
        return NextResponse.json({ transcription: flaskResult.transcription });
    }
     else if (flaskResult.predictions && flaskResult.predictions.length > 0 && typeof flaskResult.predictions[0].transcription === 'string') { // if transcription is already a string
        return NextResponse.json({ transcription: flaskResult.predictions[0].transcription });
    }

    else {
      console.error('Unexpected response structure from Flask backend:', flaskResult);
      return NextResponse.json({ message: 'Unexpected response structure from transcription service.' }, { status: 500 });
    }

  } catch (error: any) {
    console.error('Error in /api/transcribe:', error);
    return NextResponse.json({ message: error.message || 'Internal server error in Next.js API route.' }, { status: 500 });
  }
}
