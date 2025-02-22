import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LandingPage from './components/LandingPage';
import FakeNewsDetection from './components/FakeNewsDetection'; // Fake News Detection
import AnalysisPage from "./pages/AnalysisPage"; // Hate Speech Detection
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <Routes>
      {/* LandingPage allows users to choose the tool */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/hate-speech-detection" element={<AnalysisPage />} />
      <Route path="/fake-news-detection" element={<FakeNewsDetection />} />
    </Routes>
  </BrowserRouter>
);
