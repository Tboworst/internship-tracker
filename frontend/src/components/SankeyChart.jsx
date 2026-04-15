// SankeyChart.jsx
// ─────────────────────────────────────────────────────────────────
// Renders a Sankey diagram showing the application funnel:
//   Applied → OA | Rejected | No Response | Interview 1
//   Interview 1 → Interview 2 → Offer
//
// WHAT IS A SANKEY DIAGRAM?
//   A flow diagram where the width of each arrow represents
//   the quantity flowing through it. Perfect for funnels.
//
// NIVO SANKEY:
//   Nivo is a React chart library. The <ResponsiveSankey> component
//   takes `data` with two arrays: nodes and links.
//   Nodes = the boxes, Links = the arrows between them.
// ─────────────────────────────────────────────────────────────────

import { ResponsiveSankey } from "@nivo/sankey";

export default function SankeyChart({ emails }) {
  const counts = {
    no_response: emails.filter((e) => e.status === "no_response").length,
    rejected:    emails.filter((e) => e.status === "rejected").length,
    oa:          emails.filter((e) => e.status === "oa").length,
    interview_1: emails.filter((e) => e.status === "interview_1").length,
    interview_2: emails.filter((e) => e.status === "interview_2").length,
    offer:       emails.filter((e) => e.status === "offer").length,
  };

  // NOTE: nivo will crash if any link has value: 0, so we filter those out.
  const allLinks = [
    { source: "Applied",     target: "No Response", value: counts.no_response },
    { source: "Applied",     target: "Rejected",    value: counts.rejected },
    { source: "Applied",     target: "OA",          value: counts.oa },
    { source: "Applied",     target: "Interview 1", value: counts.interview_1 },
    { source: "Interview 1", target: "Interview 2", value: counts.interview_2 },
    { source: "Interview 1", target: "Offer",       value: counts.offer },
  ].filter((link) => link.value > 0);

  // Only include nodes that actually appear in at least one link
  const activeNodeIds = new Set(allLinks.flatMap((l) => [l.source, l.target]));
  const allNodes = [
    { id: "Applied" },
    { id: "No Response" },
    { id: "Rejected" },
    { id: "OA" },
    { id: "Interview 1" },
    { id: "Interview 2" },
    { id: "Offer" },
  ];

  const data = {
    nodes: allNodes.filter((n) => activeNodeIds.has(n.id)),
    links: allLinks,
  };

  if (data.links.length === 0) {
    return <p>No data to display yet.</p>;
  }

  return (
    <div style={{ height: "300px", marginBottom: "2rem" }}>
      <h2>Application Funnel</h2>
      <ResponsiveSankey
        data={data}
        margin={{ top: 10, right: 160, bottom: 10, left: 50 }}
        colors={{ scheme: "category10" }}
        nodeOpacity={1}
        linkOpacity={0.4}
        enableLinkGradient={true}
        labelPosition="outside"
        labelOrientation="horizontal"
      />
    </div>
  );
}
