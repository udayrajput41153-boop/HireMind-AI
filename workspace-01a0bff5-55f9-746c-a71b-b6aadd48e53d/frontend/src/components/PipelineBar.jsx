import React from "react";

export default function PipelineBar({ agents, runningStep }) {
  return (
    <div className="pipeline">
      {agents.map((a, i) => {
        const n = i + 1;
        const state = runningStep ? (n < runningStep ? "done" : n === runningStep ? "active" : "") : "";
        return (
          <React.Fragment key={a.id}>
            {i > 0 && <span className="pipe-arrow">→</span>}
            <div className={`agent-node ${state}`} title={a.role}>
              <span className="num">{state === "done" ? "✓" : n}</span>
              <span className="nm">{a.name}</span>
            </div>
          </React.Fragment>
        );
      })}
    </div>
  );
}
