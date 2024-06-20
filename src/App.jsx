import React, { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/analyze-eeg/', {
      method: 'POST',
      body: formData,
    });

    const result = await response.json();
    setAnalysis(result.analysis);
  };

  return (
    <>
      <div>
        <p>Привет друг! Я твой анализатор мозгового спектра ЭЭГ, загрузи диаграмму мозгового спектра в формате jpg формате и я аннализирую тебе его!</p>
        <input type='file' onChange={handleFileChange} />
        <button onClick={handleUpload}>Загрузить и анализировать</button>
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
