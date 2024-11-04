import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [data, setData] = useState(null);
    const [error, setError] = useState('');

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
        setData(null);  // Reset previous data
        setError('');    // Reset previous error
    };

    const handleUpload = async () => {
        if (!file) {
            setError('Please select a file to upload.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://127.0.0.1:5002/extract', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setData(response.data);  // Update state with the response data
            setError('');  // Reset error if upload is successful
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to extract data');
        }
    };

    return (
        <div style={{ padding: '20px', maxWidth: '500px', margin: 'auto' }}>
            <h2>Upload Document for Data Extraction</h2>
            <input type="file" accept="image/*" onChange={handleFileChange} />
            <button onClick={handleUpload} style={{ marginTop: '10px' }}>Upload and Extract</button>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {data && (
                <div style={{ marginTop: '20px' }}>
                    <h3>Extracted Data:</h3>
                    <p><strong>Name:</strong> {data.name || 'Not found'}</p>
                    <p><strong>Document Number:</strong> {data.document_number || 'Not found'}</p>
                    <p><strong>Expiration Date:</strong> {data.expiration_date || 'Not found'}</p>
                </div>
            )}
        </div>
    );
};

export default FileUpload;
