"use client";

import React, "useRef", "useState";

interface FileUploadProps {
  onFileUpload: (file: File) => void;
  isUploading: boolean;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileUpload, isUploading }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleUploadClick = () => {
    if (selectedFile) {
      onFileUpload(selectedFile);
    } else {
      alert("Please select a file first.");
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-6 w-full max-w-md">
      <h2 className="text-xl font-semibold mb-4 text-gray-700">Upload Audio File</h2>
      <div className="mb-4">
        <input
          type="file"
          accept="audio/wav, audio/mpeg, audio/ogg, audio/mp4" // .m4a is audio/mp4
          onChange={handleFileChange}
          className="hidden" // Hide the default input
          ref={fileInputRef}
        />
        <button
          onClick={triggerFileInput}
          className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-md focus:outline-none focus:shadow-outline transition duration-150 ease-in-out mb-2"
          disabled={isUploading}
        >
          {selectedFile ? `Selected: ${selectedFile.name}` : "Choose File"}
        </button>
        {selectedFile && (
          <p className="text-sm text-gray-500 truncate">
            File: {selectedFile.name} ({(selectedFile.size / 1024).toFixed(2)} KB)
          </p>
        )}
      </div>
      <button
        onClick={handleUploadClick}
        disabled={!selectedFile || isUploading}
        className="w-full bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-md focus:outline-none focus:shadow-outline transition duration-150 ease-in-out disabled:bg-gray-300"
      >
        {isUploading ? "Uploading..." : "Upload & Transcribe"}
      </button>
    </div>
  );
};

export default FileUpload;
