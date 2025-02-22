import { useNavigate } from "react-router-dom";

function App() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-gray-50 to-gray-200 px-4">
      <div className="text-center">
        <h1 className="text-5xl font-extrabold text-gray-900 tracking-wide mb-4">
          Hate Speech Detection
        </h1>
        <p className="text-lg text-gray-700 mb-8">
          Analyze text for harmful speech using AI-powered models.
        </p>
        <button
          onClick={() => navigate("/analyze")}
          className="px-8 py-3 bg-indigo-600 text-white text-lg font-semibold rounded-full shadow-lg hover:bg-indigo-700 transition-all duration-300"
        >
          Start Analysis
        </button>
      </div>
    </div>
  );
}

export default App;
