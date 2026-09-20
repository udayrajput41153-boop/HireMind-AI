import React from "react";

export function Chip({ children, tone = "" }) {
  return <span className={`chip ${tone}`}>{children}</span>;
}

export function EngineBadge({ engine }) {
  const isGemini = engine === "gemini";
  return <span className={`badge ${isGemini ? "gemini" : "offline"}`}>{isGemini ? "✦ Gemini" : "⚙ offline"}</span>;
}

export function VerdictBadge({ verdict, total }) {
  const cls = total >= 80 ? "v-hi" : total >= 60 ? "v-mid" : total >= 40 ? "v-low" : "v-bad";
  return <span className={`verdict ${cls}`}>{verdict}</span>;
}

export function scoreClass(t) {
  return t >= 80 ? "s-hi" : t >= 60 ? "s-mid" : t >= 40 ? "s-low" : "s-bad";
}

export function Bar({ value }) {
  return (
    <div className="bar">
      <i style={{ width: `${Math.max(0, Math.min(100, value))}%` }} />
    </div>
  );
}

export function Empty({ title, text }) {
  return (
    <div className="empty">
      <b>{title}</b>
      {text}
    </div>
  );
}

export function fmtYears(y) {
  if (y === null || y === undefined) return "exp. unknown";
  return `${y} yr${y === 1 ? "" : "s"} exp`;
}
