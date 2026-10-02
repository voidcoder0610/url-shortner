import React, { useState } from "react";

export default function App() {
  // State for Section 1: Creating a short link
  const [longUrl, setLongUrl] = useState("");
  const [shortUrlResult, setShortUrlResult] = useState(null);
  const [isShortening, setIsShortening] = useState(false);

  // State for Section 2: Analytics
  const [analyticsCode, setAnalyticsCode] = useState("");
  const [analyticsData, setAnalyticsData] = useState(null);
  const [analyticsError, setAnalyticsError] = useState("");

  const API_BASE = "http://localhost:8000";

  // Handles submitting a new long URL to FastAPI
  const handleShorten = async (e) => {
    e.preventDefault();
    if (!longUrl) return;

    setIsShortening(true);
    try {
      const response = await fetch(`${API_BASE}/shorten`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ long_url: longUrl }),
      });
      const data = await response.json();
      setShortUrlResult(data);
      setAnalyticsCode(data.short_code); // Pre-fill analytics box
    } catch (err) {
      alert("Failed to shorten link. Is FastAPI running on port 8000?");
    } finally {
      setIsShortening(false);
    }
  };

  // Handles fetching analytics for a short code
  const handleFetchAnalytics = async (e) => {
    e.preventDefault();
    if (!analyticsCode) return;

    setAnalyticsError("");
    try {
      const response = await fetch(`${API_BASE}/analytics/${analyticsCode}`);
      if (!response.ok) {
        throw new Error("Short link not found");
      }
      const data = await response.json();
      setAnalyticsData(data);
    } catch (err) {
      setAnalyticsData(null);
      setAnalyticsError(err.message);
    }
  };

  return (
    <div style={{ fontFamily: "sans-serif", maxWidth: "700px", margin: "40px auto", padding: "20px" }}>
      <header style={{ textAlign: "center", marginBottom: "30px" }}>
        <h1>🔗 URL Shortener & Analytics</h1>
        <p style={{ color: "#666" }}>FastAPI + PostgreSQL + Redis + React</p>
      </header>

      {/* SECTION 1: CREATE SHORT URL */}
      <section style={{ background: "#f8f9fa", padding: "20px", borderRadius: "8px", marginBottom: "30px", border: "1px solid #ddd" }}>
        <h2>1. Shorten a Link</h2>
        <form onSubmit={handleShorten} style={{ display: "flex", gap: "10px" }}>
          <input
            type="url"
            required
            placeholder="Paste your long URL here (e.g. https://wikipedia.org)"
            value={longUrl}
            onChange={(e) => setLongUrl(e.target.value)}
            style={{ flex: 1, padding: "10px", fontSize: "16px", borderRadius: "4px", border: "1px solid #ccc" }}
          />
          <button
            type="submit"
            disabled={isShortening}
            style={{ padding: "10px 20px", background: "#007bff", color: "#fff", border: "none", borderRadius: "4px", cursor: "pointer", fontWeight: "bold" }}
          >
            {isShortening ? "Shortening..." : "Shorten"}
          </button>
        </form>

        {shortUrlResult && (
          <div style={{ marginTop: "15px", padding: "12px", background: "#e8f5e9", borderRadius: "4px", border: "1px solid #c8e6c9" }}>
            <p style={{ margin: "0 0 5px 0", color: "#2e7d32", fontWeight: "bold" }}>Your Short Link is Ready:</p>
            <a href={shortUrlResult.short_url} target="_blank" rel="noreferrer" style={{ fontSize: "18px", color: "#1565c0", fontWeight: "bold" }}>
              {shortUrlResult.short_url}
            </a>
          </div>
        )}
      </section>

      {/* SECTION 2: VIEW ANALYTICS */}
      <section style={{ background: "#f8f9fa", padding: "20px", borderRadius: "8px", border: "1px solid #ddd" }}>
        <h2>2. Link Analytics</h2>
        <form onSubmit={handleFetchAnalytics} style={{ display: "flex", gap: "10px", marginBottom: "15px" }}>
          <input
            type="text"
            required
            placeholder="Enter short code (e.g. 1)"
            value={analyticsCode}
            onChange={(e) => setAnalyticsCode(e.target.value)}
            style={{ flex: 1, padding: "10px", fontSize: "16px", borderRadius: "4px", border: "1px solid #ccc" }}
          />
          <button
            type="submit"
            style={{ padding: "10px 20px", background: "#28a745", color: "#fff", border: "none", borderRadius: "4px", cursor: "pointer", fontWeight: "bold" }}
          >
            Get Stats
          </button>
        </form>

        {analyticsError && <p style={{ color: "red" }}>{analyticsError}</p>}

        {analyticsData && (
          <div style={{ background: "#fff", padding: "15px", borderRadius: "4px", border: "1px solid #eee" }}>
            <p><strong>Original URL:</strong> {analyticsData.long_url}</p>
            <div style={{ padding: "15px", background: "#f1f8e9", borderRadius: "6px", textAlign: "center", margin: "15px 0" }}>
              <span style={{ fontSize: "14px", color: "#558b2f", display: "block" }}>TOTAL CLICKS</span>
              <span style={{ fontSize: "36px", fontWeight: "bold", color: "#2e7d32" }}>{analyticsData.total_clicks}</span>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px" }}>
              <div>
                <h4>Referrers</h4>
                <ul>
                  {Object.entries(analyticsData.referrers).map(([ref, count]) => (
                    <li key={ref}>{ref}: <strong>{count}</strong></li>
                  ))}
                </ul>
              </div>
              <div>
                <h4>Countries</h4>
                <ul>
                  {Object.entries(analyticsData.countries).map(([country, count]) => (
                    <li key={country}>{country}: <strong>{count}</strong></li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}
      </section>
    </div>
  );
}