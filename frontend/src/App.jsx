// App.jsx
// ─────────────────────────────────────────────────────────────────
// This is the ROOT component — the top of the component tree.
// It fetches data from your Python backend and passes it down
// to child components as "props" (like function arguments).
//
// REACT CONCEPTS HERE:
//   useState  — stores data that can change (like a variable that
//               re-renders the page when updated)
//   useEffect — runs code when the component first loads
//               (perfect for fetching data from an API)
// ─────────────────────────────────────────────────────────────────

import { useState, useEffect } from "react";
import SummaryCards from "./components/SummaryCards";
import SankeyChart from "./components/SankeyChart";
import EmailTable from "./components/EmailTable";

export default function App() {
  // useState gives you [currentValue, functionToUpdateIt]
  const [emails, setEmails] = useState([]);       // all email data
  const [loading, setLoading] = useState(true);   // show loading state
  const [error, setError] = useState(null);       // store any errors

  // useEffect runs once when the component loads (the [] means "only once")
  useEffect(() => {
    fetch("http://localhost:8000/emails")
      .then((res) => res.json())
      .then((data) => {
        setEmails(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p style={{ padding: "2rem" }}>Loading your emails...</p>;
  if (error)   return <p style={{ padding: "2rem", color: "red" }}>Error: {error}</p>;

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif", maxWidth: "1100px", margin: "0 auto" }}>
      <h1>Internship Application Tracker</h1>

      {/* Pass emails down to each component as a prop */}
      <SummaryCards emails={emails} />
      <SankeyChart emails={emails} />
      <EmailTable emails={emails} />
    </div>
  );
}
