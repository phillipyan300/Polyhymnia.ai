'use client'
import React, { useState } from 'react';

const AudioUploadButton = () => {
    const [file, setFile] = useState(null);
    const [pdfUrl, setPdfUrl] = useState('http://localhost:3000/my_music.pdf');

    const handleFileChange = async (event: any) => {
        const uploadedFile = event.target.files[0];
        if (uploadedFile) {
            setFile(uploadedFile.name);
            console.log('Audio file uploaded:', uploadedFile.name);

            // Create FormData
            const formData = new FormData();
            formData.append('audio', uploadedFile);

            // POST request with FormData
            try {
                const response = await fetch('YOUR_ENDPOINT_URL', {
                    method: 'POST',
                    body: formData,
                });
                const data = await response.json();
                console.log('Server response:', data);
            } catch (error) {
                console.error('Error uploading file:', error);
            }
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
