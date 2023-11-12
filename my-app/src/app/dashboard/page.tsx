'use client'
import React, { useState } from 'react';

const AudioUploadButton = () => {
    const [file, setFile] = useState(null);

    const handleFileChange = (event: any) => {
        const uploadedFile = event.target.files[0];
        if (uploadedFile) {
            setFile(uploadedFile);
            console.log('Audio file uploaded:', uploadedFile.name);
            // You can handle the file upload logic here
        }
    };

    return (
        <div>
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
            {file && <p>File selected: {file.name}</p>}
        </div>
    );
};

export default AudioUploadButton;
