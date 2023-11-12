'use client'
import React, { useState } from 'react';

const AudioUploadButton = () => {
    const [file, setFile] = useState(null);
    // The PDF URL is now a path that is relative to the public directory
    const [pdfUrl, setPdfUrl] = useState('http://localhost:3000/my_music.pdf');

    const handleFileChange = (event : any) => {
        const uploadedFile = event.target.files[0];
        if (uploadedFile) {
            setFile(uploadedFile);
            console.log('Audio file uploaded:', uploadedFile.name);
            // Here you can handle the file upload logic
        }
    };

    return (
        <div>
            {pdfUrl && (
                <iframe
                    src={pdfUrl}
                    width="100%"
                    height="500px"
                    style={{ border: 'none' }}
                    title="PDF Viewer"
                ></iframe>
            )}

            <div className="mt-4 text-center">
                <input 
                    type="file" 
                    id="audio-upload" 
                    accept="audio/*" 
                    onChange={handleFileChange} 
                    hidden 
                />
                <label 
                    htmlFor="audio-upload" 
                    className="cursor-pointer bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                >
                    Upload Audio
                </label>
                {file && <p>File selected: {file}</p>}
            </div>
        </div>
    );
};

export default AudioUploadButton;
