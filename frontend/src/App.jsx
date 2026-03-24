// App.jsx — Root component with Google OAuth + JWT session

import { useState, useEffect } from "react";
import SummaryCards from "./components/SummaryCards";
import SankeyChart from "./components/SankeyChart";
import EmailTable from "./components/EmailTable";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

// ── Token helpers ─────────────────────────────────────────────────
const getToken  = ()        => localStorage.getItem("session_token");
const saveToken = (t)       => localStorage.setItem("session_token", t);
const clearToken = ()       => localStorage.removeItem("session_token");

// ── Login page ────────────────────────────────────────────────────
function LoginPage({ authError }) {
  return (
    <div style={{
      display: "flex", flexDirection: "column", alignItems: "center",
      justifyContent: "center", height: "100vh", gap: "1.5rem",
      fontFamily: "sans-serif", background: "#f9fafb",
    }}>
      <div style={{ textAlign: "center" }}>
        <h1 style={{ fontSize: "1.75rem", fontWeight: "700", color: "#111827", margin: 0 }}>
          Internship Tracker
        </h1>
        <p style={{ color: "#6b7280", marginTop: "0.5rem", fontSize: "0.95rem" }}>
          Connect your Gmail to track your applications
        </p>
      </div>

      <a
        href={`${API}/auth/google/start`}
        style={{
          display: "flex", alignItems: "center", gap: "0.75rem",
          padding: "0.75rem 1.5rem", borderRadius: "8px",
          border: "1px solid #d1d5db", background: "#fff",
          color: "#111827", fontWeight: "600", fontSize: "0.95rem",
          textDecoration: "none", boxShadow: "0 1px 3px rgba(0,0,0,0.08)",
        }}
      >
        {/* Google G logo */}
        <svg width="20" height="20" viewBox="0 0 48 48">
          <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
          <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
          <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
          <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.18 1.48-4.97 2.31-8.16 2.31-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
        </svg>
        Sign in with Google
      </a>

      {authError && (
        <p style={{ color: "#ef4444", fontSize: "0.85rem" }}>
          Sign-in failed ({authError}). Please try again.
        </p>
      )}

      <p style={{ color: "#9ca3af", fontSize: "0.8rem", maxWidth: "320px", textAlign: "center" }}>
        We only read your emails — we never send, delete, or modify anything.
      </p>
    </div>
  );
}

// ── Root component ────────────────────────────────────────────────
export default function App() {
  const [token, setToken]       = useState(() => getToken());
  const [authError, setAuthError] = useState(null);
  const [emails, setEmails]     = useState([]);
  const [loading, setLoading]   = useState(false);
  const [error, setError]       = useState(null);

  // Pick up the JWT token that the backend passes back in the URL after OAuth
  useEffect(() => {
    const params    = new URLSearchParams(window.location.search);
    const urlToken  = params.get("token");
    const authParam = params.get("auth");

    if (urlToken) {
      saveToken(urlToken);
      setToken(urlToken);
      window.history.replaceState({}, "", "/");     // clean the URL
    } else if (authParam === "error") {
      setAuthError(params.get("reason") || "unknown");
      window.history.replaceState({}, "", "/");
    }
  }, []);

  // Fetch emails whenever we have a valid session token
  useEffect(() => {
    if (!token) return;
    setLoading(true);
    setError(null);

    fetch(`${API}/emails`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(async (res) => {
        const payload = await res.json();

        if (res.status === 401) {
          // Token expired or invalid — send the user back to login
          clearToken();
          setToken(null);
          return;
        }

        if (!res.ok) throw new Error(payload?.detail || `Error ${res.status}`);
        if (!Array.isArray(payload)) throw new Error("Unexpected response from server.");

        setEmails(payload);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [token]);

  // Not logged in
  if (!token) return <LoginPage authError={authError} />;

  // Loading spinner
  if (loading) return (
    <div style={{
      display: "flex", flexDirection: "column", alignItems: "center",
      justifyContent: "center", height: "100vh", gap: "1.25rem",
      fontFamily: "sans-serif", background: "#f9fafb",
    }}>
      <div style={{
        width: "48px", height: "48px", borderRadius: "50%",
        border: "4px solid #e5e7eb", borderTopColor: "#4f46e5",
        animation: "spin 0.8s linear infinite",
      }} />
      <p style={{ color: "#6b7280", fontSize: "0.95rem" }}>Loading your emails…</p>
    </div>
  );

  // Error state
  if (error) return (
    <div style={{
      display: "flex", flexDirection: "column", alignItems: "center",
      justifyContent: "center", height: "100vh", gap: "0.75rem",
      fontFamily: "sans-serif",
    }}>
      <span style={{ fontSize: "2rem" }}>⚠️</span>
      <p style={{ color: "#ef4444", fontWeight: "600" }}>Failed to load emails</p>
      <p style={{ color: "#6b7280", fontSize: "0.85rem" }}>{error}</p>
      <button
        onClick={() => { clearToken(); setToken(null); }}
        style={{ marginTop: "0.5rem", color: "#4f46e5", background: "none", border: "none", cursor: "pointer", fontSize: "0.9rem" }}
      >
        Sign out and try again
      </button>
    </div>
  );

  // Dashboard
  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif", maxWidth: "1100px", margin: "0 auto" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
        <h1 style={{ margin: 0 }}>Internship Application Tracker</h1>
        <button
          onClick={() => { clearToken(); setToken(null); }}
          style={{
            padding: "0.4rem 1rem", borderRadius: "6px",
            border: "1px solid #d1d5db", background: "#fff",
            color: "#374151", cursor: "pointer", fontSize: "0.85rem",
          }}
        >
          Sign out
        </button>
      </div>

      <SummaryCards emails={emails} />
      <SankeyChart emails={emails} />
      <EmailTable emails={emails} />
    </div>
  );
}
