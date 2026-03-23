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
  // Count how many emails have each status
  // TODO: replace these with real counts using .filter()
  // Example: const rejected = emails.filter(e => e.status === "rejected").length
  const total      = emails.length;
  const noResponse = emails.filter((e) => e.status === "no_response").length;
  const rejected   = emails.filter((e) => e.status === "rejected").length;
  const oas        = emails.filter((e) => e.status === "oa").length;

  // An array of card data — makes it easy to render them all with .map()
  const cards = [
    { label: "Total Applied",  value: total,      color: "#4f46e5" },
    { label: "No Response",    value: noResponse,  color: "#6b7280" },
    { label: "Rejected",       value: rejected,    color: "#ef4444" },
    { label: "Online Assessments", value: oas,     color: "#f59e0b" },
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
