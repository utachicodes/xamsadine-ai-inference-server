import React from 'react';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center">
      <header className="w-full bg-blue-600 text-white p-4 text-center">
        <h1 className="text-2xl font-bold">Xamsadine AI Voice Transcription</h1>
      </header>
      <main className="flex-grow container mx-auto p-4">
        {children}
      </main>
      <footer className="w-full bg-gray-800 text-white p-4 text-center text-sm">
        &copy; {new Date().getFullYear()} Xamsadine AI
      </footer>
    </div>
  );
};

export default Layout;
