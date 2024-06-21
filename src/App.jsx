import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    setError("");

    try {
      const response = await fetch('http://157.230.23.55:8000/analyze-eeg/', { 
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorResponse = await response.json();
        throw new Error(errorResponse.error || `HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setAnalysis(result.analysis);
    } catch (error) {
      console.error('Error:', error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div>
        <p>Привет друг! Я твой анализатор мозгового спектра ЭЭГ, загрузи диаграмму мозгового спектра в формате jpg формате и я аннализирую тебе его!</p>
        <input type='file' onChange={handleFileChange} />
        <button onClick={handleUpload}>Загрузить и анализировать</button>
        {loading && (
          <div className="loader">
            Загрузка...
          </div>
        )}
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
            {analysis.substring(0, 4) === "True" ? (
              <iframe style={{borderRadius: "12px"}} src="https://open.spotify.com/embed/playlist/0VvrPqgAmdHcyvAz9Tk6rZ?utm_source=generator" width="100%" height="352" frameBorder="0" allowFullScreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
            ) : (
              <iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/37i9dQZF1DX202JSvpwCfe?utm_source=generator" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
            )}
          </div>
        )}
      </div>
    </>
  );
}

export default App;
