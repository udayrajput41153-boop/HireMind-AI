"""Generate the PDF project report for PS03 with UI screenshots."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                Table, TableStyle, PageBreak, HRFlowable)

W, H = A4
styles = getSampleStyleSheet()

INDIGO = colors.HexColor("#4F46E5")
CYAN = colors.HexColor("#0E7490")
EMERALD = colors.HexColor("#047857")
AMBER = colors.HexColor("#B45309")
DARK = colors.HexColor("#111827")
GRAY = colors.HexColor("#4B5563")
LIGHT = colors.HexColor("#EEF2FF")
LIGHTG = colors.HexColor("#F3F4F6")

st_title = ParagraphStyle("ct", parent=styles["Title"], fontSize=30, textColor=INDIGO, spaceAfter=6)
st_sub = ParagraphStyle("cs", parent=styles["Normal"], fontSize=14, textColor=DARK, alignment=TA_CENTER)
st_h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontSize=15, textColor=INDIGO, spaceBefore=14, spaceAfter=6)
st_h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontSize=12, textColor=CYAN, spaceBefore=10, spaceAfter=4)
st_body = ParagraphStyle("body", parent=styles["Normal"], fontSize=10, leading=15, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=6)
st_bul = ParagraphStyle("bul", parent=st_body, leftIndent=14, bulletIndent=4, spaceAfter=3)
st_cap = ParagraphStyle("cap", parent=styles["Normal"], fontSize=8.5, textColor=GRAY, alignment=TA_CENTER, spaceAfter=10)
st_code = ParagraphStyle("code", parent=styles["Code"], fontSize=7.5, leading=10, textColor=DARK, backColor=LIGHTG, borderPadding=6, spaceAfter=8)

story = []
B = lambda t: Paragraph(t, st_body)
BUL = lambda t: Paragraph("•  " + t, st_bul)
H1 = lambda t: story.append(Paragraph(t, st_h1)) or story.append(HRFlowable(width="100%", thickness=1, color=LIGHT, spaceAfter=6))
H2 = lambda t: story.append(Paragraph(t, st_h2))
CAP = lambda t: story.append(Paragraph(t, st_cap))
IMG = lambda path, w=6.6: story.append(Image(path, width=w * inch, height=w * inch * 0.625))


def table(rows, widths, header=True):
    t = Table([[Paragraph(c, ParagraphStyle("c", parent=styles["Normal"], fontSize=8.5, textColor=(colors.white if header and i == 0 else DARK), bold=(i == 0))) for c in r] for i, r in enumerate(rows)], colWidths=widths)
    style = [("BACKGROUND", (0, 0), (-1, 0), INDIGO),
             ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#C7D2FE")),
             ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHTG]),
             ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
             ("LEFTPADDING", (0, 0), (-1, -1), 5)]
    t.setStyle(TableStyle(style))
    story.append(t)
    story.append(Spacer(1, 8))


# ================= COVER =================
story.append(Spacer(1, 1.4 * inch))
story.append(Paragraph("HireMind AI", st_title))
story.append(Paragraph("Multi-Agent Resume Screening &amp; Job Matching Platform", st_sub))
story.append(Spacer(1, 0.25 * inch))
story.append(Paragraph("PROJECT REPORT — Hackathon Problem Statement PS03", ParagraphStyle("p", parent=st_sub, fontSize=12, textColor=CYAN)))
story.append(Spacer(1, 0.2 * inch))
story.append(Image("/home/user/docs/architecture.png", width=6.4 * inch, height=6.4 * inch * 0.585))
CAP("Figure 0 — Five-agent pipeline: LLM-powered extraction, deterministic explainable matching")
story.append(Spacer(1, 0.2 * inch))
table([
    ["Field", "Details"],
    ["Problem Statement", "PS03 — Multi-Agent Resume Screening & Job Matching Platform"],
    ["Technology Category", "NLP + LLM + Agentic AI"],
    ["Team", "[YOUR TEAM NAME] — [MEMBERS]"],
    ["Hackathon", "[HACKATHON NAME]"],
    ["Date / Version", "20 Sept 2026 · v1.0"],
], [1.6 * inch, 4.9 * inch])

story.append(PageBreak())

# ================= 1 SUMMARY =================
H1("1. Executive Summary")
B("HireMind AI is a multi-agent recruitment platform that screens resumes against job descriptions and produces a ranked, fully explainable list of candidate-role matches. Five cooperating software agents — Resume, Job, Matching, Skill Gap and Recruiter — mirror the stages of a human recruiting team at machine speed.")
B("A defining architectural decision separates this solution from typical LLM-only screeners: Google Gemini is used only for information extraction and natural-language summarisation, while the ranking decision is produced by a deterministic weighted scoring engine. This yields rich semantic understanding of unstructured resumes together with reproducible, auditable rankings. A deterministic offline NLP layer lets the platform run end-to-end without any API key, making live judging fail-safe.")
B("The deliverable is a complete web application (React 18 frontend, Python FastAPI backend) satisfying the PS03 expected demonstration — 10 resumes and 3 job descriptions producing ranked candidate lists — extended with per-candidate explainability reports and a raw agent trace of every decision.")

# ================= 2 PROBLEM =================
H1("2. Problem Analysis")
B("Recruiters spend seconds on an initial resume scan while high-volume roles attract hundreds of applications. Manual screening is slow, inconsistent and misses strong candidates whose phrasing differs from the job description. We decomposed the problem into five sub-problems, each mapped to one agent:")
BUL("P1 Heterogeneous input — resumes arrive as free text, PDF or Word with wildly different formats (Resume Agent).")
BUL("P2 Requirement ambiguity — JDs mix hard requirements, preferences and marketing language (Job Agent).")
BUL("P3 Compatibility measurement — skill overlap alone is insufficient; experience, education and domain keywords matter with different importance per role (Matching Agent).")
BUL("P4 Actionable feedback — recruiters need to know which skills are missing and how close a candidate is (Skill Gap Agent).")
BUL("P5 Explainability &amp; trust — automated ranking must justify every decision and be reproducible (deterministic core + Agent Trace).")

# ================= 3 RESEARCH =================
H1("3. Research")
H2("3.1 Existing approaches surveyed")
BUL("Keyword / ATS matching: fast but brittle — fails on synonyms and formatting variance.")
BUL("Semantic embedding similarity: handles synonyms but yields an opaque single number.")
BUL("LLM-only screening: expressive but non-reproducible, expensive and hard to audit for bias.")
BUL("Hybrid agentic systems (2025–26 state of the art): specialised agents around a deterministic decision core — the pattern we adopted.")
H2("3.2 Design conclusions")
BUL("Extraction is a language task → LLM (Gemini) with rule-based fallback for reliability.")
BUL("Ranking is a decision task → deterministic, weighted, inspectable; weights are published constants.")
BUL("A curated ~130-skill taxonomy with aliases plus fuzzy matching neutralises vocabulary mismatch — the largest source of false negatives in keyword ATS systems.")
H2("3.3 Open datasets")
B("Public resume/JD datasets on Kaggle and Hugging Face were surveyed for scale-up. The demonstration ships a fully synthetic dataset (10 resumes, 3 JDs), satisfying the 'no participant data collection' requirement. Any real dataset adopted later will have its license, version and access conditions verified first, per the problem statement's source note.")

# ================= 4 SOLUTION =================
H1("4. Proposed Solution")
B("Resumes and job descriptions are normalised into a shared schema (canonical skills, years of experience, education rank). The Matching Agent computes a deterministic 0–100 fit score per candidate–job pair; the Skill Gap Agent converts misses into prioritised gaps with upskilling advice; the Recruiter Agent writes the human summary and recommendation. Every intermediate artifact is exposed in the UI via an Agent Trace panel.")
table([
    ["#", "Agent", "Output", "Engine"],
    ["1", "Resume Agent", "Candidate profile: canonical skills, experience, education, highlights", "Gemini JSON-mode / offline heuristics"],
    ["2", "Job Agent", "Must-have vs nice-to-have skills, min experience, education", "Gemini JSON-mode / offline heuristics"],
    ["3", "Matching Agent", "0–100 score, verdict, per-dimension breakdown, matched/missing skills", "Deterministic (always)"],
    ["4", "Skill Gap Agent", "Critical & stretch gaps, adjacent strengths, upskilling plan", "Deterministic rules"],
    ["5", "Recruiter Agent", "Recruiter-style summary + interview / hold / pass recommendation", "Gemini / template"],
], [0.3 * inch, 1.25 * inch, 3.15 * inch, 1.8 * inch])
BUL("Core principle: “LLM extracts, never decides” — models parse and write; a transparent engine ranks.")
BUL("Dual-mode operation — every LLM agent has a deterministic fallback; the demo works offline and keyless.")
BUL("Concurrency — recruiter summaries for all candidates are generated in parallel (thread pool).")

story.append(PageBreak())

# ================= 5 FLOW =================
H1("5. Technical Flow & Scoring Model")
BUL("Intake — upload resumes (.txt/.pdf/.docx via pypdf / python-docx) or paste text; add or load job descriptions.")
BUL("Extraction (Agents 1–2) — Gemini JSON-mode when a key is configured, otherwise offline heuristics (section scanning, taxonomy alias matching, regex experience/education extraction).")
BUL("Scoring (Agent 3) — dimensions scored 0–1, combined with published weights; fuzzy matching links 'React.js' to 'react' (containment + difflib ≥ 0.85).")
BUL("Gap analysis (Agent 4) — missing must-haves become critical gaps with learning paths; same-category skills surface as adjacent strengths.")
BUL("Summarisation (Agent 5) — recruiter paragraph with strengths, risks and recommendation.")
BUL("Presentation — ranked list; every match carries its full agent trace.")
H2("5.1 Scoring model")
table([
    ["Dimension", "Weight", "Computation"],
    ["Must-have skills", "45%", "Fraction of required must-haves matched (fuzzy)"],
    ["Nice-to-have skills", "15%", "Fraction matched"],
    ["Experience", "20%", "1.0 if candidate ≥ required years; 0.6×(cand/req) below; 0.75 if unspecified"],
    ["Education", "10%", "Degree-rank comparison (PhD &gt; Master &gt; Bachelor &gt; Diploma)"],
    ["Keyword affinity", "10%", "JD keywords / titles found in resume text"],
], [1.5 * inch, 0.8 * inch, 4.2 * inch])
B("Verdict bands: ≥80 Strong · 60–79 Good · 40–59 Partial · &lt;40 Weak. Weights renormalise when a dimension is not applicable; identical inputs always reproduce identical outputs.")
H2("5.2 REST API")
table([
    ["Endpoint", "Purpose"],
    ["POST /api/resumes[/upload] · POST /api/jobs", "Register documents → Agents 1 & 2 run"],
    ["POST /api/demo/load", "Load bundled 10-resume / 3-JD demo set"],
    ["POST /api/match {job_id}", "Agents 3–5 over all candidates → ranked list + traces"],
    ["POST /api/reextract · GET /api/agents · /api/settings", "Re-extraction after adding a key · metadata · LLM config"],
], [2.7 * inch, 3.8 * inch])

# ================= 6 STACK =================
H1("6. Technology Stack")
table([
    ["Layer", "Technology", "Rationale"],
    ["Frontend", "React 18 + Vite", "Agent cards, ranked lists, explainable detail panels; fast HMR"],
    ["Backend", "Python 3 + FastAPI (Uvicorn)", "Async REST API, OpenAPI docs, serves the built React app"],
    ["LLM", "Google Gemini 2.5 Flash (REST)", "JSON-mode extraction & summarisation; user-supplied key"],
    ["Offline NLP", "Regex + 130-skill taxonomy + difflib", "Deterministic fallback, alias normalisation"],
    ["Parsing", "pypdf · python-docx", "Real-world resume formats"],
    ["State", "In-memory store", "Zero-setup demo; repository pattern ready for SQLite/Postgres"],
], [1.2 * inch, 2.3 * inch, 3.0 * inch])
H2("6.1 Repository layout")
story.append(Paragraph(
    "backend/ main.py · store.py · skills_taxonomy.py · offline_extract.py · agents/{llm,resume_agent,job_agent,"
    "matching_agent,skill_gap_agent,recruiter_agent}.py · static/ (React build) — frontend/ React+Vite source — "
    "data/resumes (10) · data/jobs (3) — docs/ report, deck, diagram, screenshots — test_pipeline.py", st_code))

story.append(PageBreak())

# ================= 7 SCREENSHOTS =================
H1("7. Implementation — Application Screenshots")
B("All screenshots were captured live from the running application (headless Chromium) with the demo dataset loaded.")
IMG("/home/user/docs/shots/01_resumes.png")
CAP("Figure 1 — Resume Agent output: 10 extracted candidate cards (skills, experience, education, engine badge).")
IMG("/home/user/docs/shots/02_jobs.png")
CAP("Figure 2 — Job Agent output: must-have (green) vs nice-to-have (amber) requirement chips per JD.")

story.append(PageBreak())
IMG("/home/user/docs/shots/03_ranked.png")
CAP("Figure 3 — Ranked candidate list with verdict badges and per-dimension score bars for the Senior ML Engineer role.")
IMG("/home/user/docs/shots/04_detail.png")
CAP("Figure 4 — Explainable match report: recruiter summary, ✓/✗ must-have coverage, nice-to-have coverage, weighted score breakdown.")

story.append(PageBreak())

# ================= 8 RESULTS =================
H1("8. Verified Demonstration Results")
B("The required PS03 demonstration — 10 resumes × 3 job descriptions → ranked lists — was executed end-to-end (test_pipeline.py). Rankings behave as a recruiter would expect:")
table([
    ["Job", "#1", "#2", "#3"],
    ["Senior ML Engineer", "Aarav Sharma — 95.0 Strong (7/7 must)", "Priya Nair — 69.0 Good", "Divya Reddy — 59.2 Partial"],
    ["Full-Stack Developer", "Sneha Kulkarni — 100.0 Strong (5/5)", "Rohan Mehta — 81.0 Strong", "Vikram Singh — 66.2 Good"],
    ["Data Analyst", "Karan Patel — 80.7 Strong", "Priya Nair — 78.0 Good", "Aarav Sharma — 46.7 Partial"],
], [1.7 * inch, 2.1 * inch, 1.5 * inch, 1.5 * inch])
BUL("Domain specialists top their own role; a fresh M.Tech graduate ranks below experienced peers on the senior role (experience dimension).")
BUL("The offline and Gemini extraction paths normalise to the same schema, so rankings are engine-consistent.")
BUL("Runs are fully reproducible: identical inputs ⇒ identical scores and ordering.")

# ================= 9 EXPLAIN/INNOV =================
H1("9. Explainability, Fairness & Innovation")
H2("9.1 Explainability & fairness")
BUL("Every score decomposes into five published weighted components with plain-language notes (e.g. “3.5 yrs &lt; 4 yrs required”).")
BUL("Agent Trace exposes each agent's engine and full JSON output — any decision is auditable end-to-end.")
BUL("Scoring uses only skills, experience, education and JD keywords — no names, photos, genders, ages or addresses.")
BUL("Deterministic core removes run-to-run variance; fuzzy/alias matching removes terminology bias.")
H2("9.2 Innovation highlights")
BUL("Hybrid “LLM extracts, never decides” architecture — explainability by construction.")
BUL("Dual-engine resilience: identical schema whether Gemini or offline heuristics ran; demo cannot fail on stage.")
BUL("Adjacency-aware gap analysis: surfaces same-category strengths and concrete learning paths, not just missing skills.")
BUL("Shared 130-skill taxonomy as the contract between all agents.")
BUL("Recruiter-grade deliverables: verdict bands, prose summary, interview/hold/pass recommendation.")

# ================= 10 ROADMAP =================
H1("10. Limitations & Future Work")
BUL("Heuristic offline extraction finds fewer skills on very unstructured resumes (mitigated by dual mode).")
BUL("In-memory persistence today → roadmap: SQLite/Postgres, saved match history, accounts.")
BUL("Roadmap: embedding-based semantic similarity as a sixth signal; layout-aware PDF parsing; multi-job comparison board; CSV/PDF export; periodic fairness audits.")

# ================= 11 AI RESOURCES =================
H1("11. Use of External / AI Resources (Disclosure)")
BUL("Google Gemini 2.5 Flash — optional runtime engine for extraction & summaries via official REST API (key supplied by user, never hard-coded).")
BUL("AI-assisted development — an agentic coding assistant (Arena.ai Agent Mode) scaffolded code and drafted documentation; all architecture, scoring design and verification were reviewed by the team.")
BUL("Open-source libraries — React, Vite, FastAPI, python-docx, pypdf, Pillow, difflib.")
BUL("Demo data — 100% synthetic; no participant or personal data collected (per PS03).")

# ================= 12 REFERENCES =================
H1("12. References")
refs = [
    "[1] Google AI for Developers — Gemini API. https://ai.google.dev",
    "[2] FastAPI documentation. https://fastapi.tiangolo.com",
    "[3] React documentation. https://react.dev",
    "[4] Vite documentation. https://vite.dev",
    "[5] python-docx. https://python-docx.readthedocs.io",
    "[6] pypdf. https://pypdf.readthedocs.io",
    "[7] Python difflib. https://docs.python.org/3/library/difflib.html",
    "[8] Kaggle / Hugging Face resume & JD datasets — surveyed; verify license before use.",
]
for r in refs:
    BUL(r)
H1("Appendix A — Run instructions")
story.append(Paragraph(
    "cd backend &amp;&amp; pip install -r requirements.txt &amp;&amp; uvicorn main:app --host 0.0.0.0 --port 8000  "
    "# serves API + React build ·  cd frontend &amp;&amp; npm install &amp;&amp; npm run dev  # hot-reload UI, /api proxied ·  "
    "python3 test_pipeline.py  # end-to-end smoke test ·  Open http://localhost:8000 → Load demo dataset → "
    "Tab 3 → Run Matching Pipeline. Optionally add a Gemini key under ⚙ Settings.", st_code))

doc = SimpleDocTemplate(
    "/home/user/docs/HireMind_AI_ProjectReport_PS03.pdf", pagesize=A4,
    title="HireMind AI — PS03 Project Report", author="[YOUR TEAM NAME]",
    leftMargin=0.75 * inch, rightMargin=0.75 * inch, topMargin=0.7 * inch, bottomMargin=0.7 * inch,
)
doc.build(story)
print("PDF saved")
