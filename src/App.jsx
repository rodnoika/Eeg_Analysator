import React, { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState("");
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/analyze-eeg/', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorResponse = await response.json();
        throw new Error(errorResponse.error || `HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setAnalysis(result.analysis);
      setError(""); 
    } catch (error) {
      console.error('Error:', error);
      setError(error.message); 
    }
  };

  return (
    <>
      <div>
        <p>Привет друг! Я твой анализатор мозгового спектра ЭЭГ, загрузи диаграмму мозгового спектра в формате jpg формате и я аннализирую тебе его!</p>
        <input type='file' onChange={handleFileChange} />
        <button onClick={handleUpload}>Загрузить и анализировать</button>
        {error && (
          <div style={{ color: 'red' }}>
            <h2>Ошибка</h2>
            <p>{error}</p>
          </div>
        )}
        {analysis && (
          <div>
            <h2>Анализ ЭЭГ</h2>
            <p>{analysis}</p>
          </div>
        )}
      </div>
    </>
  );
}

export default App;
