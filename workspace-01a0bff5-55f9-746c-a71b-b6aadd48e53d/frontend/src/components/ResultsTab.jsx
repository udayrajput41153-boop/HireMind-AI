import React, { useState } from "react";
import { Bar, Empty, VerdictBadge, fmtYears, scoreClass } from "./ui";
import CandidateDetail from "./CandidateDetail";

const STEP_NAMES = ["Resume Agent", "Job Agent", "Matching Agent", "Skill Gap Agent", "Recruiter Agent"];

function AgentSteps({ step }) {
  return (
    <div className="agent-steps">
      {STEP_NAMES.map((n, i) => {
        const s = i + 1 < step ? "done" : i + 1 === step ? "active" : "";
        return (
          <div className={`step ${s}`} key={n}>
            {s === "done" ? "✓" : s === "active" ? <span className="spinner" /> : "•"} {n}
          </div>
        );
      })}
    </div>
  );
}

function RankRow({ e, open, onToggle }) {
  const c = e.components;
  return (
    <div className={`rankrow ${open ? "open" : ""}`} onClick={onToggle}>
      <div className="l1">
        <span className="ranknum">{e.rank}</span>
        <div className="who">
          <b>{e.name}</b>
          <span>
            {e.title} · {fmtYears(e.years_experience)}
            {e.education?.degree && e.education.degree !== "Unknown" ? ` · ${e.education.degree}` : ""}
          </span>
        </div>
        <VerdictBadge verdict={e.verdict} total={e.total} />
        <span className={`score ${scoreClass(e.total)}`}>{e.total}</span>
      </div>
      <div className="minibars">
        {[
          ["Must-have", c.must_have.score],
          ["Nice-to-have", c.nice_to_have.score],
          ["Experience", c.experience.score],
          ["Education", c.education.score],
          ["Keywords", c.keywords.score],
        ].map(([lbl, v]) => (
          <div className="minibar" key={lbl}>
            <label>{lbl} {v}</label>
            <Bar value={v} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default function ResultsTab({ jobs, resumes, results, activeJobId, setActiveJobId, onRun, running, runningStep }) {
  const [selectedId, setSelectedId] = useState(null);
  const result = results[activeJobId];
  const selected = result?.ranked.find((r) => r.candidate_id === selectedId) || null;

  if (jobs.length === 0) {
    return <Empty title="No jobs to match against" text="Add job descriptions in tab 2 (or load the demo dataset), then run the matching pipeline here." />;
  }

  return (
    <div>
      <div className="jobpick">
        {jobs.map((j) => (
          <button key={j.id} className={`pill ${j.id === activeJobId ? "active" : ""}`} onClick={() => { setActiveJobId(j.id); setSelectedId(null); }}>
            {j.requirements.title}
          </button>
        ))}
      </div>

      {activeJobId ? (
        <button className="run" onClick={() => onRun(activeJobId)} disabled={running || resumes.length === 0}>
          {running ? "⏳ Agent pipeline running…" : "▶ Run Matching Pipeline"}
          <span className="hint">{resumes.length} candidate(s) × 5 agents</span>
        </button>
      ) : (
        <p className="muted">Select a job above, then run the matching pipeline.</p>
      )}

      {running && <AgentSteps step={runningStep} />}

      {result && !running && (
        <>
          <p className="muted mt" style={{ fontSize: 13 }}>
            Ranked {result.ranked.length} candidates for <b style={{ color: "var(--text)" }}>{result.job.title}</b> ·
            Matching Agent: deterministic weighted scoring · Recruiter summaries by {result.summary_engine === "gemini" ? "Gemini" : "template engine"}
          </p>
          <div className="rankwrap mt">
            <div className="ranklist">
              {result.ranked.map((e) => (
                <RankRow key={e.candidate_id} e={e} open={selectedId === e.candidate_id} onToggle={() => setSelectedId(selectedId === e.candidate_id ? null : e.candidate_id)} />
              ))}
            </div>
            {selected ? (
              <CandidateDetail e={selected} job={result.job} onClose={() => setSelectedId(null)} />
            ) : (
              <div className="empty">
                <b>Select a candidate</b>
                Click any ranked card to open the explainable match report: score breakdown, skill gaps and recruiter summary.
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}
