import React, { useState } from 'react';
import Layout from '../components/Layout';
import { analyzeHateSpeech } from '../api';

const AnalysisPage = () => {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    if (!text.trim()) {
      setError('Please enter text for analysis.');
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);
  
    try {
      const response = await analyzeHateSpeech(text);
      if (response) {
        // Parse the response string to get an object
        setResult(parsePlainTextResult(response));
      } else {
        setError('No data returned from server.');
      }
    } catch (err) {
      setError('Error connecting to the server.');
    }
    setLoading(false);
  };
  

  const parsePlainTextResult = (text) => {
    try {
      // Try to parse the text as JSON first.
      const jsonData = JSON.parse(text);
      return jsonData;
    } catch (err) {
      // If parsing as JSON fails, fall back to custom parsing.
      const lines = text.split('\n');
      const parsedResult = {};
      lines.forEach((line) => {
        if (line.includes('Roberta:')) {
          parsedResult.Roberta = line.replace('Roberta:', '').trim();
        } else if (line.includes('HateBERT:')) {
          parsedResult.HateBERT = line.replace('HateBERT:', '').trim();
        } else if (line.includes('GPT-4 Analysis:')) {
          parsedResult['GPT-4 Analysis'] = line.replace('GPT-4 Analysis:', '').trim();
        }
      });
      return parsedResult;
    }
  };
  

  return (
    <Layout
      title="Hate Speech Detection"
      subtitle="Analyze text for hateful language and derogatory expressions"
    >
      <div className="bg-gray-800 p-8 rounded-xl shadow-lg max-w-2xl w-full">
        <textarea
          className="w-full p-4 bg-gray-700 text-white border border-gray-600 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 transition-all resize-none"
          rows="5"
          placeholder="Type something here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        ></textarea>
        {error && <p className="text-red-400 mt-2">{error}</p>}
        <button
          onClick={handleSubmit}
          className={`mt-4 w-full px-6 py-3 text-lg font-semibold rounded-full shadow-md transition-all duration-300 ${
            loading ? 'bg-gray-600 cursor-not-allowed' : 'bg-red-600 hover:bg-red-700 text-white'
          }`}
          disabled={loading}
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
        <div className="mt-6">
          <h2 className="text-xl font-semibold text-gray-200 mb-2">Analysis Results:</h2>
          <div className="bg-gray-700 p-4 rounded-lg shadow-inner">
            {loading ? (
              <div className="text-center text-gray-400">Analyzing...</div>
            ) : result ? (
              <div>
                {result.Roberta && (
                  <div className="mb-4">
                    <h3 className="text-lg font-semibold text-blue-400 mb-1">Roberta:</h3>
                    {typeof result.Roberta === 'object' ? (
                      <p className="font-medium">
                        {result.Roberta.label} (Score: {result.Roberta.score})
                      </p>
                    ) : (
                      <p className="font-medium">{result.Roberta}</p>
                    )}
                  </div>
                )}

                {result.HateBERT && (
                  <div className="mb-4">
                    <h3 className="text-lg font-semibold text-blue-400 mb-1">HateBERT:</h3>
                    <p className="font-medium">{result.HateBERT}</p>
                  </div>
                )}
                {result['GPT-4 Analysis'] && (
                  <div>
                    <h3 className="text-lg font-semibold text-blue-400 mb-1">GPT-4 Analysis:</h3>
                    <p className="font-medium">{result['GPT-4 Analysis']}</p>
                  </div>
                )}
              </div>
            ) : (
              <p className="text-gray-400">No analysis performed yet.</p>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default AnalysisPage;