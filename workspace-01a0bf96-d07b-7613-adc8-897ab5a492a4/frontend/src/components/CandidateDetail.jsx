import React from "react";
import { Chip, EngineBadge, VerdictBadge, Bar, scoreClass, fmtYears } from "./ui";

export default function CandidateDetail({ e, job, onClose }) {
  const c = e.components;
  const comps = [
    ["Must-have skills", c.must_have, `${c.must_have.matched}/${c.must_have.total} matched`],
    ["Nice-to-have skills", c.nice_to_have, `${c.nice_to_have.matched}/${c.nice_to_have.total} matched`],
    ["Experience", c.experience, c.experience.note],
    ["Education", c.education, c.education.note],
    ["Keyword affinity", c.keywords, c.keywords.hits.length ? c.keywords.hits.slice(0, 4).join(", ") : "—"],
  ];

  return (
    <div className="detail">
      <button className="x" onClick={onClose}>✕</button>
      <h2>
        <span className={`score ${scoreClass(e.total)}`} style={{ fontSize: 26 }}>{e.total}</span>
        {e.name} <VerdictBadge verdict={e.verdict} total={e.total} />
      </h2>
      <div className="sub">
        {e.title} · {fmtYears(e.years_experience)}
        {e.education?.degree && e.education.degree !== "Unknown" ? ` · ${e.education.degree}` : ""} · ranked #{e.rank} for “{job.title}”
      </div>

      <section>
        <h4>Recruiter summary <EngineBadge engine={e.summary_engine} /></h4>
        <div className="summary-card">{e.summary}</div>
      </section>

      <section>
        <h4>Must-have coverage</h4>
        <div className="chips">
          {e.must_matched.map((m) => (
            <Chip key={m.required} tone="green">✓ {m.required}</Chip>
          ))}
          {e.must_missing.map((m) => (
            <Chip key={m} tone="red">✗ {m}</Chip>
          ))}
          {e.must_matched.length + e.must_missing.length === 0 && <span className="muted">No must-haves listed</span>}
        </div>
      </section>

      {(e.nice_matched.length > 0 || e.nice_missing.length > 0) && (
        <section>
          <h4>Nice-to-have coverage</h4>
          <div className="chips">
            {e.nice_matched.map((m) => (
              <Chip key={m.required} tone="green">✓ {m.required}</Chip>
            ))}
            {e.nice_missing.map((m) => (
              <Chip key={m} tone="amber">○ {m}</Chip>
            ))}
          </div>
        </section>
      )}

      <section>
        <h4>Score breakdown (deterministic)</h4>
        {comps.map(([label, comp, note]) => (
          <div className="comp" key={label}>
            <div className="lbl">
              <span>{label} <span style={{ opacity: .6 }}>· weight {comp.weight}%</span></span>
              <span>{comp.score} — {note}</span>
            </div>
            <Bar value={comp.score} />
          </div>
        ))}
      </section>

      {(e.gaps.critical_gaps.length > 0 || e.gaps.stretch_gaps.length > 0) && (
        <section>
          <h4>Skill gaps &amp; upskilling plan</h4>
          {e.gaps.critical_gaps.map((g) => (
            <div className="gap-item" key={g.skill}>
              <b>✗ {g.skill}</b> <span className="muted">(critical)</span>
              <div className="rec">→ {g.recommendation}</div>
            </div>
          ))}
          {e.gaps.stretch_gaps.map((g) => (
            <div className="gap-item stretch" key={g.skill}>
              <b>○ {g.skill}</b> <span className="muted">(nice-to-have)</span>
              <div className="rec">→ {g.recommendation}</div>
            </div>
          ))}
          {e.gaps.adjacent_strengths.length > 0 && (
            <div className="gap-item" style={{ borderColor: "#065f46" }}>
              <b style={{ color: "#6ee7b7" }}>Adjacent strengths to build on</b>
              {e.gaps.adjacent_strengths.map((a) => (
                <div className="rec" key={a.gap}>
                  {a.gap} ← already knows {a.build_on.join(", ")} ({a.category})
                </div>
              ))}
            </div>
          )}
        </section>
      )}

      <details className="trace">
        <summary>🔍 Agent trace — see each agent's input/output (explainability)</summary>
        <pre>{JSON.stringify(e.trace, null, 2)}</pre>
      </details>
    </div>
  );
}
