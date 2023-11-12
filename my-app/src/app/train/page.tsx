'use client'
import React, { useState } from 'react';

const AudioUploadButton = () => {
    const [file, setFile] = useState(null);
    // The PDF URL is now a path that is relative to the public directory
    const [pdfUrl, setPdfUrl] = useState('http://localhost:3000/my_music.pdf');

    const handleFileChange = async (event: any) => {
        const uploadedFile = event.target.files[0];
        if (uploadedFile) {
            setFile(uploadedFile);
            console.log('Audio file uploaded:', uploadedFile.name);

            // Create FormData for the first POST request
            const formData = new FormData();
            formData.append('audio', uploadedFile);

            // POST request with FormData to upload the audio file
            try {
                const uploadResponse = await fetch('YOUR_UPLOAD_ENDPOINT_URL', {
                    method: 'POST',
                    body: formData,
                });
                const uploadData = await uploadResponse.json();
                console.log('Server response from upload:', uploadData);

                // Set score from the upload response if it's included
                if (uploadData.score) {
                    setScore(uploadData.score);

                    // Create a JSON object for the second POST request
                    const proficiencyData = {
                        score: uploadData.score,
                        // Include any other data required by your endpoint
                    };

                    // Second POST request to updateProficiency
                    const updateResponse = await fetch('YOUR_UPDATE_PROFICIENCY_ENDPOINT_URL', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(proficiencyData),
                    });

                    if (updateResponse.ok) {
                        console.log('Proficiency score updated successfully');
                        // Additional logic for a successful update can go here
                    } else {
                        console.error('Failed to update proficiency score', updateResponse.statusText);
                    }
                }
            } catch (error) {
                console.error('Error during the process:', error);
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
                {file && <p>File selected: {file.name}</p>}
                {/* Textbox to display the score */}
                {score && (
                    <input 
                        type="text" 
                        value={`Score: ${score}`} 
                        readOnly 
                        className="mt-2 text-center border-2 border-blue-500 rounded"
                    />
                )}
            </div>
        </div>
    );
};

export default AudioUploadButton;
