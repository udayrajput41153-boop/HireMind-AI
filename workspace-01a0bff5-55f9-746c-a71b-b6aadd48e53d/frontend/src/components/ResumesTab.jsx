import React, { useState } from "react";
import { Chip, EngineBadge, Empty, fmtYears } from "./ui";

function ResumeCard({ r, onDelete }) {
  const p = r.profile;
  const skills = p.skills || [];
  const shown = skills.slice(0, 8);
  return (
    <div className="card">
      <button className="x" title="Delete" onClick={() => onDelete(r.id)}>✕</button>
      <h3>
        <span>{p.name}</span>
        <EngineBadge engine={r.engine} />
      </h3>
      <div className="sub">
        {p.title} · {fmtYears(p.years_experience)}
        {p.education?.degree && p.education.degree !== "Unknown" ? ` · ${p.education.degree}` : ""}
      </div>
      {p.email && <div className="sub">✉ {p.email}</div>}
      <div className="chips">
        {shown.map((s) => (
          <Chip key={s.name}>{s.name}</Chip>
        ))}
        {skills.length > shown.length && <Chip tone="more">+{skills.length - shown.length} more</Chip>}
        {skills.length === 0 && <span className="muted" style={{ fontSize: 12.5 }}>No known skills detected</span>}
      </div>
    </div>
  );
}

export default function ResumesTab({ resumes, onUpload, onPaste, onDemo, onDelete, busy }) {
  const [text, setText] = useState("");
  const [name, setName] = useState("");

  return (
    <div>
      <div className="toolbar">
        <label className="filebtn">
          <button className="primary" disabled={!!busy}>📄 Upload resumes (.txt / .pdf / .docx)</button>
          <input
            type="file"
            multiple
            accept=".txt,.md,.pdf,.docx"
            onChange={(e) => {
              if (e.target.files?.length) {
                onUpload([...e.target.files]);
                e.target.value = "";
              }
            }}
          />
        </label>
        <button onClick={onDemo} disabled={!!busy}>⚡ Load demo dataset (10 resumes + 3 JDs)</button>
        <span className="muted" style={{ fontSize: 13 }}>{resumes.length} resume(s) in store</span>
      </div>

      <div className="card" style={{ marginBottom: 18 }}>
        <h3>Paste resume text</h3>
        <input
          className="field mt"
          style={{ width: "100%" }}
          placeholder="filename (optional), e.g. riya_resume.txt"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <textarea
          className="mt"
          placeholder={"Priya Verma\nData Engineer\npriya@example.com\n\nSKILLS\nPython, SQL, Airflow, Spark…\n\nEXPERIENCE\n…"}
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <div className="mt">
          <button
            className="primary"
            disabled={!text.trim() || !!busy}
            onClick={() => {
              onPaste(text, name || "pasted-resume.txt");
              setText("");
              setName("");
            }}
          >
            + Add resume
          </button>
        </div>
      </div>

      {resumes.length === 0 ? (
        <Empty title="No resumes yet" text="Upload files, paste text, or load the demo dataset to see the Resume Agent at work." />
      ) : (
        <div className="grid">
          {resumes.map((r) => (
            <ResumeCard key={r.id} r={r} onDelete={onDelete} />
          ))}
        </div>
      )}
    </div>
  );
}
