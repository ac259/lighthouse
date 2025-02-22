import { useState } from "react";
import { analyzeHateSpeech } from "../api";

function AnalysisPage() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    console.log("✅ Button clicked!");

    if (!text.trim()) {
      console.warn("⚠ No text entered!");
      setError("Please enter text for analysis.");
      return;
    }

    setLoading(true);
    setError(null);
    console.log("⏳ Analyzing:", text);

    try {
      const response = await analyzeHateSpeech(text);
      console.log("✅ API Response:", response);

      if (response && Object.keys(response).length > 0) {
        setResult(response);
      } else {
        console.warn("⚠ No valid response from API");
        setError("No data returned from server.");
      }
    } catch (error) {
      console.error("❌ API Error:", error);
      setError("Error connecting to the server.");
    }

    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-gray-100 to-gray-300 px-4">
      <div className="bg-white shadow-xl rounded-xl p-8 w-full max-w-2xl text-center transition-all duration-300">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Hate Speech Analysis</h1>
        <p className="text-gray-600 mb-4">Enter text below to analyze its sentiment.</p>

        <textarea
          className="w-full p-4 border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 transition-all resize-none"
          rows="5"
          placeholder="Type something here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        ></textarea>

        {error && <p className="text-red-600 mt-2">{error}</p>}

        <button
          onClick={handleSubmit}
          className={`mt-4 w-full px-6 py-3 text-lg font-semibold rounded-full shadow-md transition-all duration-300 ${
            loading ? "bg-gray-400 cursor-not-allowed" : "bg-indigo-600 hover:bg-indigo-700 text-white"
          }`}
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Analyze"}
        </button>

        {result && Object.keys(result).length > 0 && (
          <div className="mt-6 text-left transition-opacity duration-300">
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Analysis Results:</h2>
            <div className="space-y-3 bg-gray-100 p-4 rounded-lg shadow-inner">
              {result["RoBERTa Model"] && (
                <p className="p-2 bg-gray-50 rounded-md">
                  <strong>🧠 RoBERTa:</strong> {result["RoBERTa Model"].label} (Confidence: {result["RoBERTa Model"].score.toFixed(2)})
                </p>
              )}
              {result["HateBERT Model"] && (
                <p className="p-2 bg-gray-50 rounded-md">
                  <strong>🤖 HateBERT:</strong> {result["HateBERT Model"]}
                </p>
              )}
              {result["GPT4All (Llama 3)"] && (
                <p className="p-2 bg-gray-50 rounded-md">
                  <strong>🔥 GPT4All (Llama 3):</strong> {result["GPT4All (Llama 3)"]}
                </p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default AnalysisPage;
