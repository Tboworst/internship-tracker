// SankeyChart.jsx
// ─────────────────────────────────────────────────────────────────
// Renders a Sankey diagram showing the application funnel:
//   Applied → OA
//   Applied → Rejected
//   Applied → No Response
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
  // Count emails per status
  const counts = {
    no_response: emails.filter((e) => e.status === "no_response").length,
    rejected:    emails.filter((e) => e.status === "rejected").length,
    oa:          emails.filter((e) => e.status === "oa").length,
  };

  // TODO: Build the Sankey data object.
  //
  // `nodes` is an array of objects with an `id` — each box in the diagram.
  // `links` is an array of { source, target, value } — each arrow.
  //
  // Example structure:
  //   nodes: [
  //     { id: "Applied" },
  //     { id: "No Response" },
  //     { id: "Rejected" },
  //     { id: "OA" },
  //   ],
  //   links: [
  //     { source: "Applied", target: "No Response", value: counts.no_response },
  //     { source: "Applied", target: "Rejected",    value: counts.rejected },
  //     { source: "Applied", target: "OA",          value: counts.oa },
  //   ]
  //
  // NOTE: nivo will crash if any link has value: 0, so filter those out.
  // Hint: build the links array then do .filter(link => link.value > 0)

  const allLinks = [
    { source: "Applied", target: "No Response", value: counts.no_response },
    { source: "Applied", target: "Rejected",    value: counts.rejected },
    { source: "Applied", target: "OA",          value: counts.oa },
  ].filter((link) => link.value > 0);

  const data = {
    nodes: [
      { id: "Applied" },
      { id: "No Response" },
      { id: "Rejected" },
      { id: "OA" },
    ],
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
