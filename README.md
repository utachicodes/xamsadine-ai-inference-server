# Xamsadine AI - Transcription Service

## Overview
This project provides a web interface for transcribing audio files using the Xamsadine AI inference capabilities. It consists of two main parts:

1.  **Next.js Frontend (`xamsadine-ai-frontend` directory):** A modern web application built with Next.js, React, and Tailwind CSS. It provides the user interface for uploading audio files and displaying transcriptions.
2.  **Python Flask Backend (original `app.py` and related files):** The original inference server that handles the actual speech-to-text processing using Hugging Face Transformers.

The Next.js frontend communicates with the Python backend via an API proxy.

## Features
- **User-friendly web interface** for audio file uploads (supports WAV, MP3, OGG, M4A).
- **Displays transcription results** directly in the browser.
- **Powered by Hugging Face Transformers** for speech recognition via the Python backend.

## Project Structure
```
.
├── xamsadine-ai-frontend/  # Next.js frontend application
│   ├── src/
│   │   ├── app/            # App Router pages, layouts, API routes
│   │   ├── components/     # React components
│   │   └── ...
│   ├── public/
│   ├── package.json
│   └── ...
├── app.py                  # Python Flask backend server
├── requirements.txt        # Python dependencies
├── les-conditions-du-tawhid-0_out_1.wav # Sample audio
└── ...                     # Other original backend files & samples
```

## Setup & Usage

### Prerequisites
- **Node.js** (version 18.x or later recommended for Next.js)
- **npm** (comes with Node.js)
- **Python** (version 3.8 or later recommended)
- **pip** (Python package installer)
- **Hugging Face Token** (if the backend model `CAYTU/whosper-large-v2` or any other model used by `app.py` requires it. Set as `HF_TOKEN` environment variable for the Python backend).

### 1. Running the Python Flask Backend

The backend is responsible for the actual audio transcription.

1.  **Navigate to the root project directory** (where `app.py` is located).
    ```bash
    # cd /path/to/your/project-root
    ```
2.  **Create and activate a Python virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: If you encounter issues with `torch` or `torchaudio`, you might need to install them separately first. Visit the [PyTorch website](https://pytorch.org/get-started/locally/) for instructions specific to your OS and CUDA version (if applicable).*
4.  **Set your Hugging Face Token (if your model needs it):**
    ```bash
    export HF_TOKEN="your_hf_token" # On Windows: set HF_TOKEN=your_hf_token
    ```
5.  **Run the Flask backend server:**
    ```bash
    python app.py
    ```
    The backend server will typically start on `http://localhost:8080`. Keep this terminal window open.

### 2. Running the Next.js Frontend

The frontend provides the web interface.

1.  **Open a new terminal window/tab.**
2.  **Navigate to the frontend directory:**
    ```bash
    cd xamsadine-ai-frontend
    ```
3.  **Install frontend dependencies:**
    ```bash
    npm install
    ```
4.  **Run the Next.js development server:**
    ```bash
    npm run dev
    ```
    The frontend development server will typically start on `http://localhost:3000`.
5.  **Access the application:**
    Open your web browser and go to `http://localhost:3000`.

### Using the Application
- Once both backend and frontend servers are running, open `http://localhost:3000` in your browser.
- Use the "Choose File" button to select an audio file (WAV, MP3, OGG, M4A).
- Click "Upload & Transcribe".
- The server will process the audio, and the transcription text will be displayed on the page.

### Environment Variables for Frontend (Optional)
- `FLASK_BACKEND_URL`: If your Flask backend is running on a different URL than the default `http://localhost:8080/predict`, you can set this environment variable for the Next.js app (e.g., in a `.env.local` file in the `xamsadine-ai-frontend` directory).
  ```
  # xamsadine-ai-frontend/.env.local
  FLASK_BACKEND_URL=http://your-backend-url/predict
  ```

## License
This project is licensed under the MIT License.

## Contact
For any inquiries:
- **Email:** abdoullahaljersi@gmail.com
- **GitHub:** [utachicodes](https://github.com/utachicodes)
