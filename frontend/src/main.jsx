import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from "./App";
import AnalysisPage from "./pages/AnalysisPage"; // Make sure this file exists
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/analyze" element={<AnalysisPage />} />
    </Routes>
  </BrowserRouter>
);
