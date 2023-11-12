// Use this directive at the top of your file to indicate this is a Client Component
"use client";
import React, { useState } from 'react';

const MyComponent = () => {
    const [file, setFile] = useState(null);
    const [newDifficulty, setNewDifficulty] = useState(null);
    const [pdfUrl, setPdfUrl] = useState(null); // Assuming you have a state for PDF URL

    const handleFileChange = async (event) => {
        // Update the state with the selected file
        const selectedFile = event.target.files[0];
        setFile(selectedFile);
        
        // Prepare the formData for sending the file
        const formData = new FormData();
        formData.append('audio', selectedFile);

        try {
            // Make the API call to the Flask backend
            const uploadResponse = await fetch('http://127.0.0.1:5000/process-audio', {
                method: 'POST',
                body: formData,
            });
            const uploadData = await uploadResponse.json();
            console.log('Server response from upload:', uploadData);

            // Update the state with the new difficulty value from the response
            setNewDifficulty(uploadData.newDifficulty);

            // If you need to update the PDF URL state
            // setPdfUrl(uploadData.pdfUrl); // Assuming the response contains a pdfUrl
        } catch (error) {
            console.error('Error during the file upload process:', error);
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
                {/* Textbox to display the new difficulty score */}
                {newDifficulty && (
                    <input 
                        type="text" 
                        value={`Score: ${newDifficulty}`} 
                        readOnly 
                        className="mt-2 text-center border-2 border-blue-500 rounded"
                    />
                )}
            </div>
        </div>
    );
};

export default MyComponent;
