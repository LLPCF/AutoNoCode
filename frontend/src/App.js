import React, { useState } from 'react';
import axios from 'axios';

function App() {
    const [photos, setPhotos] = useState([]);
    const [videoPath, setVideoPath] = useState('');

    const handleFileChange = (e) => {
        setPhotos(e.target.files);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        for (let i = 0; i < photos.length; i++) {
            formData.append('photos', photos[i]);
        }

        try {
            const response = await axios.post('http://localhost:5000/api/uploads', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setVideoPath(response.data.videoPath);
        } catch (error) {
            console.error('Error uploading photos:', error);
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input type="file" multiple onChange={handleFileChange} />
                <button type="submit">Upload and Create Video</button>
            </form>
            {videoPath && (
                <div>
                    <h2>Video created at:</h2>
                    <a href={`http://localhost:5000/${videoPath}`} target="_blank" rel="noopener noreferrer">Download Video</a>
                </div>
            )}
        </div>
    );
}

export default App;
