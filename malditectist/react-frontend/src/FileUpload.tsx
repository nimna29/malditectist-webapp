import React, { useState } from 'react';
import axios from 'axios';
import Dropzone from 'react-dropzone';

interface MlResult {
    prediction: string;
    rf_probability: string;
    nn_prediction: string;
}

const FileUpload = () => {
    const [selectedFile, setSelectedFile] = useState<File | undefined>(undefined);
    const [mlResult, setMLResult] = useState<MlResult | null>(null);

    const handleFileSelect = (file: File[]) => {
        setSelectedFile(file[0]);
    };

    const handleFileUpload = async () => {
        const formData = new FormData();
        formData.append('file', selectedFile as File);
        try {
            const response = await axios.post(
                'http://localhost:8000/api/upload_file/',
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                }
            );
            setMLResult({
                prediction: response.data.prediction,
                rf_probability: response.data.rf_probability,
                nn_prediction: response.data.nn_prediction,
            });
            console.log(response.data);
        } catch (error) {
            console.error(error);
        }
    };


    return (
        <div>
            <Dropzone onDrop={handleFileSelect}>
                {({ getRootProps, getInputProps }) => (
                    <div {...getRootProps()}>
                        <input {...getInputProps()} />
                        {selectedFile ? (
                            <p>Selected file: {selectedFile.name}</p>
                        ) : (
                            <p>Drag and drop a file here, or click to select a file</p>
                        )}
                    </div>
                )}
            </Dropzone>
            <button onClick={handleFileUpload} disabled={!selectedFile}>
                Upload
            </button>
            <div>
                {mlResult && (
                    <>
                        <p>Prediction: {mlResult.prediction}</p>
                        <p>Random Forest probability: {mlResult.rf_probability}</p>
                        <p>Neural Network prediction: {mlResult.nn_prediction}</p>
                    </>
                )}
            </div>

        </div>
    );
};

export default FileUpload;
