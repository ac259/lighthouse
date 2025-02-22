// FakeNewsDetection.jsx
import React, { useState } from 'react';
import Layout from '../components/Layout';
import { analyzeFakeNews } from '../api';

const FakeNewsDetection = () => {
  const [text, setText] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    if (!text.trim()) {
      setError('Please enter text for analysis.');
      return;
    }
    setLoading(true);
    setError(null);
    setResult('');

    try {
      const data = await analyzeFakeNews(text);
      if (data) {
        setResult(data);
      } else {
        setError('No data returned from server.');
      }
    } catch (err) {
      setError('Error connecting to the server.');
    }
    setLoading(false);
  };

  return (
    <Layout
      title="Fake News Detection"
      subtitle="Examine content for misinformation and verify claims"
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
            loading ? 'bg-gray-600 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700 text-white'
          }`}
          disabled={loading}
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
        <div className="mt-6">
          <h2 className="text-xl font-semibold text-gray-200 mb-2">Analysis Results:</h2>
          <div className="bg-gray-700 p-4 rounded-lg shadow-inner">
            {loading ? (
              <div className="text-center text-gray-400">Analysing...</div>
            ) : result ? (
              <p className="whitespace-pre-wrap text-gray-200">{result}</p>
            ) : (
              <p className="text-gray-400">No analysis performed yet.</p>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default FakeNewsDetection;
