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
    const [errorMessage, setErrorMessage] = useState<string | null>(null);

    const handleFileSelect = (file: File[]) => {
        setSelectedFile(file[0]);
        setErrorMessage(null);
        setMLResult(null);
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
        } catch (error: any) {
            console.error(error);
            if (error.response.status === 400) {
                setErrorMessage(error.response.data.error);
            } else {
                setErrorMessage('An error occurred while uploading the file.');
            }
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
            {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
            <div>
                {mlResult && (
                    <>
                        <p>Prediction: {mlResult.prediction}</p>
                        <p>Random Forest Probability: {mlResult.rf_probability}</p>
                        <p>Neural Network Prediction: {mlResult.nn_prediction}</p>
                        <p>If the probability and prediction values are close to 100%, 
                            it indicates that the file is a malware.<br/>
                            Conversely, if the probability and prediction values are below 85%, 
                            it indicates that the file is not a malware and is a legitimate file.</p>
                    </>
                )}
            </div>
        </div>
    );
};

export default FileUpload;
