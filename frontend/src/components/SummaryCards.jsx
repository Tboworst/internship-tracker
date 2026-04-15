// SummaryCards.jsx
// ─────────────────────────────────────────────────────────────────
// Displays 4 stat boxes: Total, No Response, Rejected, OAs.
//
// REACT CONCEPT — PROPS:
//   This component receives `emails` from App.jsx as a prop.
//   Props are read-only — you use them but don't change them here.
//   Access them via the `{ emails }` parameter (destructuring).
// ─────────────────────────────────────────────────────────────────

export default function SummaryCards({ emails }) {
  const total       = emails.length;
  const noResponse  = emails.filter((e) => e.status === "no_response").length;
  const rejected    = emails.filter((e) => e.status === "rejected").length;
  const oas         = emails.filter((e) => e.status === "oa").length;
  const interview1  = emails.filter((e) => e.status === "interview_1").length;
  const interview2  = emails.filter((e) => e.status === "interview_2").length;
  const offers      = emails.filter((e) => e.status === "offer").length;

  const cards = [
    { label: "Total Applied",    value: total,       color: "#4f46e5" },
    { label: "No Response",      value: noResponse,  color: "#6e7880" },
    { label: "Rejected",         value: rejected,    color: "#ef4444" },
    { label: "Online Assessments", value: oas,       color: "#f59e0b" },
    { label: "1st Interviews",   value: interview1,  color: "#3b82f6" },
    { label: "2nd Interviews",   value: interview2,  color: "#8b5cf6" },
    { label: "Offers",           value: offers,      color: "#10b981" },
  ];

  return (
    <div style={{ display: "flex", gap: "1rem", marginBottom: "2rem", flexWrap: "wrap" }}>
      {/*
        .map() loops over the array and returns a card for each item.
        The `key` prop is required by React to track list items — use
        something unique like the label.
      */}
      {cards.map((card) => (
        <div
          key={card.label}
          style={{
            flex: "1",
            minWidth: "150px",
            padding: "1.5rem",
            borderRadius: "8px",
            background: card.color,
            color: "white",
            textAlign: "center",
          }}
        >
          <div style={{ fontSize: "2rem", fontWeight: "bold" }}>{card.value}</div>
          <div style={{ fontSize: "0.9rem", marginTop: "0.25rem" }}>{card.label}</div>
        </div>
      ))}
    </div>
  );
}
