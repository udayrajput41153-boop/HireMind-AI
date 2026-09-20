import React, { useState } from "react";
import { getKey, getModel, saveKeyModel } from "../api";

export default function Header({ llm, onSaveSettings, onReextract, onReset }) {
  const [open, setOpen] = useState(false);
  const [key, setKey] = useState(getKey());
  const [model, setModel] = useState(getModel() || "gemini-2.5-flash");
  const [saved, setSaved] = useState(false);

  const save = async () => {
    saveKeyModel(key.trim(), model.trim());
    await onSaveSettings(key.trim(), model.trim());
    setSaved(true);
    setTimeout(() => { setSaved(false); setOpen(false); }, 600);
  };

  return (
    <header className="top">
      <div className="brand">
        <div className="logo">🧠</div>
        <div>
          <h1>HireMind AI</h1>
          <p>Multi-Agent Resume Screening &amp; Job Matching · PS03</p>
        </div>
      </div>
      <div className="top-actions">
        <span className={`pill-status ${llm.configured ? "on" : ""}`}>
          {llm.configured ? `✦ Gemini connected${llm.model ? " · " + llm.model : ""}` : "⚙ Offline NLP mode — add a Gemini key for LLM agents"}
        </span>
        {llm.configured && (
          <button className="ghost" onClick={onReextract} title="Re-run Resume & Job agent extraction using Gemini">
            ↻ Re-extract with Gemini
          </button>
        )}
        <button className="primary" onClick={() => setOpen(true)}>⚙ Settings</button>
      </div>

      {open && (
        <div className="modal-bg" onClick={(e) => e.target === e.currentTarget && setOpen(false)}>
          <div className="modal">
            <h3>LLM Settings</h3>
            <div>
              <label>Google Gemini API key (stored in this browser only)</label>
              <input className="field" style={{ width: "100%" }} type="password" value={key} placeholder="AIza…" onChange={(e) => setKey(e.target.value)} />
            </div>
            <div>
              <label>Model</label>
              <input className="field" style={{ width: "100%" }} value={model} onChange={(e) => setModel(e.target.value)} />
            </div>
            <p className="muted" style={{ fontSize: 12.5 }}>
              Without a key the platform runs fully offline (deterministic NLP heuristics). With a key, the Resume Agent, Job Agent and Recruiter Agent use Gemini; the Matching Agent always stays deterministic for explainability.
            </p>
            <div className="row">
              <button className="danger ghost" onClick={async () => { await onReset(); setOpen(false); }}>Clear all data</button>
              <button onClick={() => setOpen(false)}>Cancel</button>
              <button className="primary" onClick={save}>{saved ? "✓ Saved" : "Save"}</button>
            </div>
          </div>
        </div>
      )}
    </header>
  );
}
