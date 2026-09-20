import React, { useState } from "react";
import { Chip, EngineBadge, Empty } from "./ui";

function JobCard({ j, onDelete }) {
  const q = j.requirements;
  return (
    <div className="card">
      <button className="x" title="Delete" onClick={() => onDelete(j.id)}>✕</button>
      <h3>
        <span>{q.title}</span>
        <EngineBadge engine={j.engine} />
      </h3>
      <div className="sub">
        {q.min_years_experience != null ? `${q.min_years_experience}+ yrs required · ` : ""}
        {q.education_required ? `Education: ${q.education_required}` : "No education requirement detected"}
      </div>
      <div>
        <div className="sub" style={{ marginBottom: 4 }}>Must-have ({(q.must_have_skills || []).length})</div>
        <div className="chips">
          {(q.must_have_skills || []).map((s) => (
            <Chip key={s.name} tone="green">{s.name}</Chip>
          ))}
          {(q.must_have_skills || []).length === 0 && <span className="muted" style={{ fontSize: 12.5 }}>none detected</span>}
        </div>
      </div>
      <div>
        <div className="sub" style={{ marginBottom: 4 }}>Nice-to-have ({(q.nice_to_have_skills || []).length})</div>
        <div className="chips">
          {(q.nice_to_have_skills || []).map((s) => (
            <Chip key={s.name} tone="amber">{s.name}</Chip>
          ))}
          {(q.nice_to_have_skills || []).length === 0 && <span className="muted" style={{ fontSize: 12.5 }}>none detected</span>}
        </div>
      </div>
    </div>
  );
}

export default function JobsTab({ jobs, onAdd, onDemo, onDelete, busy }) {
  const [text, setText] = useState("");

  return (
    <div>
      <div className="toolbar">
        <button onClick={onDemo} disabled={!!busy}>⚡ Load demo dataset (10 resumes + 3 JDs)</button>
        <span className="muted" style={{ fontSize: 13 }}>{jobs.length} job(s) in store</span>
      </div>

      <div className="card" style={{ marginBottom: 18 }}>
        <h3>Add a job description</h3>
        <p className="sub mt">Tip: include “Requirements” and “Nice to have” sections — the Job Agent splits must-have vs nice-to-have skills from them.</p>
        <textarea
          className="mt"
          style={{ minHeight: 180 }}
          placeholder={"Senior Data Engineer — Acme Corp\n\nRequirements (must have)\n- Strong Python and SQL\n- Spark\n- 3+ years of experience\n\nNice to have\n- AWS, Airflow…"}
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <div className="mt">
          <button className="primary" disabled={!text.trim() || !!busy} onClick={() => { onAdd(text); setText(""); }}>
            + Add job description
          </button>
        </div>
      </div>

      {jobs.length === 0 ? (
        <Empty title="No job descriptions yet" text="Paste a JD above or load the demo dataset." />
      ) : (
        <div className="grid">
          {jobs.map((j) => (
            <JobCard key={j.id} j={j} onDelete={onDelete} />
          ))}
        </div>
      )}
    </div>
  );
}
