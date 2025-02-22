import { useState, useEffect } from "react";
import { analyzeHateSpeech } from "../api";

const LoadingAnimation = () => {
  const [dots, setDots] = useState("");
  
  useEffect(() => {
    const interval = setInterval(() => {
      setDots((prev) => (prev.length < 3 ? prev + "." : ""));
    }, 500);
    return () => clearInterval(interval);
  }, []);
  
  return <div className="text-center text-gray-600 text-lg">Analysing{dots}</div>;
};

const ResultDisplay = ({ result }) => {
  // Parse the JSON response
  let parsed;
  try {
    parsed = JSON.parse(result);
  } catch (err) {
    parsed = null;
  }
  
  if (parsed) {
    return (
      <div className="space-y-4">
        {parsed.Roberta && (
          <div className="p-4 bg-red-50 rounded-md">
            <h3 className="text-red-700 font-bold">RoBERTa</h3>
            <p>
              <span className="font-semibold">Label:</span> {parsed.Roberta.label}
            </p>
            <p>
              <span className="font-semibold">Score:</span> {parsed.Roberta.score}
            </p>
          </div>
        )}
        {parsed.HateBERT && (
          <div className="p-4 bg-blue-50 rounded-md">
            <h3 className="text-blue-700 font-bold">HateBERT</h3>
            <p>{parsed.HateBERT}</p>
          </div>
        )}
        {parsed["GPT-4 Analysis"] && (
          <div className="p-4 bg-green-50 rounded-md">
            <h3 className="text-green-700 font-bold">GPT-4 Analysis</h3>
            <p className="whitespace-pre-wrap">{parsed["GPT-4 Analysis"]}</p>
          </div>
        )}
      </div>
    );
  } else {
    // If parsing fails, display raw text.
    return <p className="p-2 bg-gray-50 rounded-md whitespace-pre-wrap">{result}</p>;
  }
};

const SearchPanel = ({
  text,
  setText,
  error,
  handleSubmit,
  loading,
  minimized,
  setMinimized,
}) => {
  return (
    <div
      className="transition-all duration-300 overflow-hidden border border-gray-200 rounded-lg"
      onMouseEnter={() => setMinimized(false)}
      onMouseLeave={() => {
        if (text.trim() === "" || text.trim() !== "") {
          // You can conditionally collapse only if results exist; here we always collapse on mouse leave.
          setMinimized(true);
        }
      }}
    >
      {minimized ? (
        <div className="h-10 flex items-center justify-center cursor-pointer text-gray-500">
          Hover to expand search options
        </div>
      ) : (
        <div className="p-4">
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
              loading
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-indigo-600 hover:bg-indigo-700 text-white"
            }`}
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </div>
      )}
    </div>
  );
};

function AnalysisPage() {
  const [text, setText] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchMinimized, setSearchMinimized] = useState(false);

  const handleSubmit = async () => {
    console.log("✅ Button clicked!");
    if (!text.trim()) {
      console.warn("⚠ No text entered!");
      setError("Please enter text for analysis.");
      return;
    }
    setLoading(true);
    setError(null);
    setResult("");
    console.log("⏳ Analyzing:", text);

    try {
      const data = await analyzeHateSpeech(text);
      console.log("✅ API Data Received:", data);
      if (data) {
        setResult(data);
        // Automatically minimize search panel when results are in
        setSearchMinimized(true);
      } else {
        console.warn("⚠ No valid response from API");
        setError("No data returned from server.");
      }
    } catch (err) {
      console.error("❌ API Error:", err);
      setError("Error connecting to the server.");
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-gray-100 to-gray-300 px-4">
      <div className="bg-white shadow-xl rounded-xl p-8 w-full max-w-2xl text-center transition-all duration-300">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Hate Speech Analysis</h1>
        <p className="text-gray-600 mb-4">Enter text below to analyze its sentiment.</p>
        <SearchPanel
          text={text}
          setText={setText}
          error={error}
          handleSubmit={handleSubmit}
          loading={loading}
          minimized={searchMinimized}
          setMinimized={setSearchMinimized}
        />
        <div className="mt-6 text-left transition-opacity duration-300">
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Analysis Results:</h2>
          <div className="space-y-3 bg-gray-100 p-4 rounded-lg shadow-inner">
            {loading ? (
              <LoadingAnimation />
            ) : result ? (
              <ResultDisplay result={result} />
            ) : (
              <p className="text-gray-500">No analysis performed yet.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default AnalysisPage;
