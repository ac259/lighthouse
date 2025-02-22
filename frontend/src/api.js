export async function analyzeHateSpeech(text) {
  console.log("📡 Sending request to API:", text);  // Debug log

  try {
    const response = await fetch("http://localhost:8000/api/analyze-hate-speech", {  // ✅ Ensure correct path
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    });

    console.log("🔄 API Status:", response.status);  // Log API status

    if (!response.ok) {
      throw new Error(`Failed to fetch results. Status: ${response.status}`);
    }

    // Use response.text() instead of response.json() to get plain text
    const data = await response.text();
    console.log("✅ API Data Received:", data);
    return data;
  } catch (error) {
    console.error("❌ API Request Failed:", error);
    return null;
  }
}
