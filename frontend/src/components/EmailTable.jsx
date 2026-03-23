// EmailTable.jsx
// ─────────────────────────────────────────────────────────────────
// A filterable table of all your internship emails.
//
// REACT CONCEPT — LOCAL STATE:
//   This component has its own `filter` state (separate from App.jsx).
//   When the user picks a filter, only this component re-renders.
//   State that only one component needs should live in that component.
// ─────────────────────────────────────────────────────────────────

import { useState } from "react";

const STATUS_LABELS = {
  all:         "All",
  no_response: "No Response",
  rejected:    "Rejected",
  oa:          "OA",
};

const STATUS_COLORS = {
  no_response: "#6b7280",
  rejected:    "#ef4444",
  oa:          "#f59e0b",
};

export default function EmailTable({ emails }) {
  const [filter, setFilter] = useState("all");

  // TODO: filter the emails array based on the selected filter.
  // If filter === "all", show all emails.
  // Otherwise, show only emails where email.status === filter.
  // Hint: use .filter() on the emails array.
  const displayed = filter === "all"
    ? emails
    : emails.filter((e) => e.status === filter);

  return (
    <div>
      <h2>All Emails</h2>

      {/* Filter buttons */}
      <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem" }}>
        {Object.entries(STATUS_LABELS).map(([value, label]) => (
          <button
            key={value}
            onClick={() => setFilter(value)}
            style={{
              padding: "0.4rem 0.9rem",
              borderRadius: "999px",
              border: "none",
              cursor: "pointer",
              background: filter === value ? "#4f46e5" : "#e5e7eb",
              color: filter === value ? "white" : "black",
            }}
          >
            {label}
          </button>
        ))}
      </div>

      {/* Table */}
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.9rem" }}>
        <thead>
          <tr style={{ background: "#f3f4f6", textAlign: "left" }}>
            <th style={th}>Subject</th>
            <th style={th}>Sender</th>
            <th style={th}>Date</th>
            <th style={th}>Status</th>
          </tr>
        </thead>
        <tbody>
          {displayed.map((email) => (
            <tr key={email.id}>
              <td style={td}>{email.subject}</td>
              <td style={td}>{email.sender}</td>
              <td style={td}>{email.date}</td>
              <td style={td}>
                <span style={{ color: STATUS_COLORS[email.status], fontWeight: "600" }}>
                  {STATUS_LABELS[email.status]}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// Reusable cell styles
const th = { padding: "0.6rem 1rem", borderBottom: "2px solid #e5e7eb" };
const td = { padding: "0.6rem 1rem", borderBottom: "1px solid #f3f4f6" };
