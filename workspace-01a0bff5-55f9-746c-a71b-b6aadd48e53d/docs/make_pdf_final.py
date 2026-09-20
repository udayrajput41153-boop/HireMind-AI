"""FINAL comprehensive project report for PS03 — includes Django backend + QA results."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                Table, TableStyle, PageBreak, HRFlowable)
from PIL import Image as PILImage

styles = getSampleStyleSheet()
INDIGO = colors.HexColor("#4F46E5")
CYAN = colors.HexColor("#0E7490")
EMERALD = colors.HexColor("#047857")
DARK = colors.HexColor("#111827")
GRAY = colors.HexColor("#4B5563")
LIGHT = colors.HexColor("#EEF2FF")
LIGHTG = colors.HexColor("#F3F4F6")

st_title = ParagraphStyle("ct", parent=styles["Title"], fontSize=30, textColor=INDIGO, spaceAfter=6)
st_sub = ParagraphStyle("cs", parent=styles["Normal"], fontSize=14, textColor=DARK, alignment=TA_CENTER)
st_h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontSize=15, textColor=INDIGO, spaceBefore=12, spaceAfter=6)
st_h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontSize=12, textColor=CYAN, spaceBefore=10, spaceAfter=4)
st_body = ParagraphStyle("body", parent=styles["Normal"], fontSize=10, leading=15, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=6)
st_bul = ParagraphStyle("bul", parent=st_body, leftIndent=14, bulletIndent=4, spaceAfter=3)
st_cap = ParagraphStyle("cap", parent=styles["Normal"], fontSize=8.5, textColor=GRAY, alignment=TA_CENTER, spaceAfter=10)
st_code = ParagraphStyle("code", parent=styles["Code"], fontSize=7.5, leading=10, textColor=DARK, backColor=LIGHTG, borderPadding=6, spaceAfter=8)

story = []
B = lambda t: story.append(Paragraph(t, st_body))
BUL = lambda t: story.append(Paragraph("•  " + t, st_bul))
H1 = lambda t: (story.append(Paragraph(t, st_h1)), story.append(HRFlowable(width="100%", thickness=1, color=LIGHT, spaceAfter=6)))
H2 = lambda t: story.append(Paragraph(t, st_h2))
CAP = lambda t: story.append(Paragraph(t, st_cap))


def IMG(path, w=6.6):
    iw, ih = PILImage.open(path).size
    story.append(Image(path, width=w * inch, height=w * inch * ih / iw))


def table(rows, widths):
    t = Table([[Paragraph(str(c), ParagraphStyle("c", parent=styles["Normal"], fontSize=8.5,
                          textColor=(colors.white if i == 0 else DARK), bold=(i == 0))) for c in r] for i, r in enumerate(rows)], colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INDIGO),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#C7D2FE")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHTG]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5)]))
    story.append(t)
    story.append(Spacer(1, 8))


# ============ COVER ============
story.append(Spacer(1, 0.9 * inch))
story.append(Paragraph("HireMind AI", st_title))
story.append(Paragraph("Multi-Agent Resume Screening &amp; Job Matching Platform", st_sub))
story.append(Spacer(1, 0.12 * inch))
story.append(Paragraph("FINAL PROJECT REPORT — Hackathon Problem Statement PS03", ParagraphStyle("p", parent=st_sub, fontSize=12, textColor=CYAN)))
story.append(Spacer(1, 0.15 * inch))
IMG("/home/user/docs/architecture.png", 6.4)
CAP("Figure 0 — Five-agent pipeline: LLM-powered extraction around a deterministic, explainable matching core.")
story.append(Spacer(1, 0.12 * inch))
table([
    ["Field", "Details"],
    ["Problem Statement", "PS03 — Multi-Agent Resume Screening & Job Matching Platform"],
    ["Technology Category", "NLP + LLM + Agentic AI"],
    ["Team", "[YOUR TEAM NAME] — [MEMBERS]"],
    ["Hackathon", "[HACKATHON NAME]"],
    ["Date / Version", "20 Sept 2026 · v2.0 (final)"],
], [1.6 * inch, 4.9 * inch])
story.append(PageBreak())

# ============ 1 ============
H1("1. Executive Summary")
B("HireMind AI is a multi-agent recruitment platform that screens resumes against job descriptions and produces ranked, fully explainable candidate–role matches. Five cooperating agents — Resume, Job, Matching, Skill Gap and Recruiter — mirror a human recruiting team at machine speed.")
B("Architectural signature: <b>“LLM extracts, never decides.”</b> Google Gemini (optional, user-supplied key) performs information extraction and summarisation; the ranking decision is produced by a deterministic weighted engine, giving reproducible, auditable outcomes. A rule-based offline NLP layer makes the platform fully functional without any API key.")
B("The intelligence layer is framework-agnostic: the identical agent codebase is served by <b>two interchangeable backends</b> — Python FastAPI and Django — behind one REST contract, with a React 18 frontend on top. The PS03 required demonstration (10 resumes × 3 job descriptions → ranked lists) passes end-to-end on both, verified by a 72-check automated QA suite (72/72 passing).")

# ============ 2 ============
H1("2. Problem Analysis")
B("Manual resume screening is slow (≈7 seconds per resume at first pass), inconsistent between screeners, vocabulary-sensitive (“React.js” vs “React”), and opaque to candidates. We decomposed the problem into five sub-problems, each assigned to one agent:")
table([
    ["Sub-problem", "Agent responsible"],
    ["P1 Heterogeneous resume formats (txt/pdf/docx, free text)", "Resume Agent"],
    ["P2 Ambiguous JDs (must-have vs nice-to-have separation)", "Job Agent"],
    ["P3 Multi-dimensional compatibility measurement", "Matching Agent"],
    ["P4 Actionable feedback on missing skills", "Skill Gap Agent"],
    ["P5 Explainability, reproducibility & trust", "Deterministic core + Agent Trace"],
], [3.6 * inch, 2.9 * inch])

# ============ 3 ============
H1("3. Research")
H2("3.1 Approaches surveyed")
BUL("Keyword/ATS matching — fast, brittle to synonyms.")
BUL("Embedding similarity — synonym-tolerant but opaque single score.")
BUL("LLM-only screening — expressive but non-reproducible and hard to audit.")
BUL("Hybrid agentic systems (2025–26 SOTA) — specialised agents around a deterministic decision core; adopted.")
H2("3.2 Design conclusions")
BUL("Extraction = language task → Gemini with deterministic fallback; all outputs normalised through a shared ~130-skill taxonomy (aliases: js→javascript, k8s→kubernetes, sklearn→scikit-learn).")
BUL("Ranking = decision task → published fixed weights; fuzzy matching (containment + difflib ≥ 0.85) removes vocabulary false-negatives.")
H2("3.3 Datasets")
B("Kaggle/Hugging Face resume & JD corpora surveyed for scale-up; demonstration uses a fully synthetic 10+3 dataset (no participant data, per PS03). Any real dataset adopted later will have license/version/access conditions verified first, as the source note requires.")

# ============ 4 ============
H1("4. Proposed Solution")
table([
    ["#", "Agent", "Output", "Engine"],
    ["1", "Resume Agent", "Profile: canonical skills, experience, education, highlights", "Gemini JSON-mode / offline heuristics"],
    ["2", "Job Agent", "Must-have / nice-to-have skills, min experience, education", "Gemini JSON-mode / offline heuristics"],
    ["3", "Matching Agent", "0–100 score, verdict, per-dimension breakdown", "Deterministic (always)"],
    ["4", "Skill Gap Agent", "Critical & stretch gaps, adjacent strengths, learning plan", "Deterministic rules"],
    ["5", "Recruiter Agent", "Summary + interview/hold/pass recommendation (parallelised)", "Gemini / template"],
], [0.3 * inch, 1.2 * inch, 3.2 * inch, 1.8 * inch])
BUL("Dual-mode resilience: identical schema from Gemini or offline path — the demo never breaks on stage.")
BUL("Single REST contract implemented twice (FastAPI, Django) over one shared agent codebase.")
BUL("Agent Trace: every match carries each agent's engine + full JSON output for audit.")

# ============ 5 ============
H1("5. Technical Flow & Scoring Model")
BUL("Intake → Extraction (Agents 1–2) → Weighted scoring (Agent 3) → Gap analysis (Agent 4) → Summary (Agent 5) → Ranked list + trace.")
table([
    ["Dimension", "Weight", "Computation"],
    ["Must-have skills", "45%", "Fraction matched (fuzzy + taxonomy)"],
    ["Nice-to-have skills", "15%", "Fraction matched"],
    ["Experience", "20%", "1.0 if ≥ required; 0.6×(cand/req) below; 0.75 unspecified"],
    ["Education", "10%", "Degree-rank comparison (PhD &gt; Master &gt; Bachelor &gt; Diploma)"],
    ["Keyword affinity", "10%", "JD keywords found in resume text"],
], [1.5 * inch, 0.8 * inch, 4.2 * inch])
IMG("/home/user/docs/shots/k3_pie.png", 6.2)
CAP("Figure 1 — The score pie: fixed, public slices; same input ⇒ same score, always.")
B("Verdicts: ≥80 Strong · 60–79 Good · 40–59 Partial · &lt;40 Weak. Weights renormalise when a dimension is absent.")

story.append(PageBreak())

# ============ 6 ============
H1("6. Technology Stack")
table([
    ["Layer", "Technology", "Rationale"],
    ["Frontend", "React 18 + Vite", "Agent cards, ranked lists, explainable panels; HMR dev"],
    ["Backend A", "Python 3 + FastAPI (Uvicorn)", "Async REST, OpenAPI docs, serves React build"],
    ["Backend B", "Django 6 (runserver/WSGI)", "Same API contract; proves framework-agnostic agents"],
    ["LLM", "Google Gemini 2.5 Flash (REST)", "JSON-mode extraction/summaries; user-supplied key"],
    ["Offline NLP", "Regex + 130-skill taxonomy + difflib", "Deterministic fallback & alias normalisation"],
    ["Parsing", "pypdf · python-docx", "Real-world resume formats"],
    ["QA", "test_pipeline.py · test_everything.py (72 checks)", "Automated verification of both backends"],
], [1.2 * inch, 2.5 * inch, 2.8 * inch])
H2("6.1 Repository layout")
story.append(Paragraph(
    "backend/            FastAPI app + agents/{llm,resume,job,matching,skill_gap,recruiter} + skills_taxonomy + offline_extract + store + static/ (React build)<br/>"
    "backend_django/       Django project (manage.py, hiremind/{settings,urls,views}) reusing backend/ agents via sys.path<br/>"
    "frontend/             React + Vite source (src/components/*, api.js)<br/>"
    "data/resumes/ (10) · data/jobs/ (3)   synthetic demo dataset<br/>"
    "docs/                 reports (PDF/DOCX), pitch deck (PPTX), diagrams, screenshots<br/>"
    "test_pipeline.py · test_everything.py", st_code))

# ============ 7 ============
H1("7. REST API (identical on both backends)")
table([
    ["Endpoint", "Purpose"],
    ["POST /api/resumes · /api/resumes/upload", "Register resumes (paste or multipart files) → Agent 1"],
    ["POST /api/jobs", "Register JD → Agent 2"],
    ["POST /api/demo/load", "Load 10-resume / 3-JD demo set"],
    ["POST /api/match {job_id}", "Agents 3–5 over all candidates → ranked list + traces"],
    ["POST /api/reextract · POST /api/settings", "Re-extraction with Gemini · key/model config"],
    ["GET /api/agents · /api/health · /api/resumes · /api/jobs", "Metadata, health (reports backend flavour), listings"],
    ["DELETE /api/resumes/{id} · /api/jobs/{id} · /api/reset", "Housekeeping"],
], [2.8 * inch, 3.7 * inch])

# ============ 8 ============
H1("8. Application Screenshots (captured live)")
IMG("/home/user/docs/shots/01_resumes.png")
CAP("Figure 2 — Resume Agent output: 10 extracted candidate cards (skills, experience, education, engine badge).")
IMG("/home/user/docs/shots/03_ranked.png")
CAP("Figure 3 — Ranked list for Senior ML Engineer with verdict badges and per-dimension score bars.")

story.append(PageBreak())
IMG("/home/user/docs/shots/04_detail.png")
CAP("Figure 4 — Explainable match report: recruiter summary, ✓/✗ coverage, weighted breakdown, gap plan, agent trace.")

# ============ 9 ============
H1("9. Verification & QA (72/72 passing)")
B("Two suites run on <b>both</b> backends: test_pipeline.py (end-to-end demo) and test_everything.py (25 behaviour checks per backend + 22 deliverable-file checks). Latest run: <b>72 passed, 0 failed</b>.")
table([
    ["Job", "#1", "#2", "#3"],
    ["Senior ML Engineer", "Aarav Sharma — 95.0 Strong (7/7)", "Priya Nair — 69.0 Good", "Divya Reddy — 59.2 Partial"],
    ["Full-Stack Developer", "Sneha Kulkarni — 100.0 Strong (5/5)", "Rohan Mehta — 81.0 Strong", "Vikram Singh — 66.2 Good"],
    ["Data Analyst", "Karan Patel — 80.7 Strong", "Priya Nair — 78.0 Good", "Aarav Sharma — 46.7 Partial"],
], [1.7 * inch, 2.1 * inch, 1.5 * inch, 1.5 * inch])
BUL("Identical rankings on FastAPI and Django — the agent layer is provably framework-independent.")
BUL("Reproducibility: repeated runs produce byte-identical scores and ordering (deterministic core).")
BUL("Error paths verified: unknown job/resume → 404; empty inputs → 400; reset/reextract flows pass.")
BUL("UI verified by headless-Chromium screenshots; PDF report pages rendered and visually inspected.")

# ============ 10 ============
H1("10. Explainability, Fairness & Innovation")
BUL("Published weights + plain-language notes per dimension; Agent Trace exposes every agent's raw I/O.")
BUL("Scoring uses only skills/experience/education/keywords — never names, photos, ages, genders.")
BUL("Alias + fuzzy matching removes terminology bias; deterministic core removes run-to-run variance.")
BUL("Innovations: “LLM extracts, never decides”; dual-engine resilience; adjacency-aware gap analysis with learning plans; shared taxonomy as inter-agent contract; dual-backend portability; one-click PS03 demo.")

# ============ 11 ============
H1("11. Limitations & Roadmap")
BUL("Offline heuristics extract fewer skills from very unstructured resumes (mitigated by dual mode).")
BUL("In-memory persistence → roadmap: SQLite/Postgres, match history, accounts.")
BUL("Roadmap: embedding similarity as 6th signal; layout-aware PDF parsing; multi-job comparison board; CSV/PDF export; scheduled fairness audits.")

# ============ 12 ============
H1("12. External / AI Resources (Disclosure)")
BUL("Google Gemini 2.5 Flash — optional runtime extraction/summaries via official REST API (user key, never hard-coded).")
BUL("AI-assisted development — Arena.ai Agent Mode assisted scaffolding/drafting; all design decisions and verification team-reviewed.")
BUL("Open-source: React, Vite, FastAPI, Django, python-docx, pypdf, Pillow, reportlab, python-pptx, Playwright, difflib.")
BUL("Demo data 100% synthetic; no participant data collected (per PS03).")

# ============ 13 ============
H1("13. References")
for r in [
    "[1] Gemini API — ai.google.dev  ·  [2] FastAPI — fastapi.tiangolo.com  ·  [3] Django — djangoproject.com",
    "[4] React — react.dev  ·  [5] Vite — vite.dev  ·  [6] pypdf / python-docx docs",
    "[7] Python difflib — docs.python.org  ·  [8] Kaggle & Hugging Face resume/JD datasets (surveyed; verify licenses)",
]:
    BUL(r)
H1("Appendix A — Run & demo")
story.append(Paragraph(
    "# FastAPI:  cd backend &amp;&amp; pip install -r requirements.txt &amp;&amp; uvicorn main:app --host 0.0.0.0 --port 8000<br/>"
    "# Django:   pip install django &amp;&amp; cd backend_django &amp;&amp; python manage.py runserver 0.0.0.0 --port 8001<br/>"
    "# Frontend dev: cd frontend &amp;&amp; npm install &amp;&amp; npm run dev   # /api proxied to :8000<br/>"
    "# QA: python3 test_everything.py        # 72 checks across both backends<br/>"
    "Demo: open :8000 or :8001 → Load demo dataset → Tab 3 → Run Matching Pipeline → open any candidate → Agent Trace.", st_code))

doc = SimpleDocTemplate(
    "/home/user/docs/HireMind_AI_Final_ProjectReport.pdf", pagesize=A4,
    title="HireMind AI — Final Project Report (PS03)", author="[YOUR TEAM NAME]",
    leftMargin=0.75 * inch, rightMargin=0.75 * inch, topMargin=0.7 * inch, bottomMargin=0.7 * inch,
)


def footer(canvas, d):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRAY)
    canvas.drawString(0.75 * inch, 0.42 * inch, "HireMind AI · PS03 Final Project Report · v2.0")
    canvas.drawRightString(A4[0] - 0.75 * inch, 0.42 * inch, f"page {d.page}")
    canvas.restoreState()


doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("final PDF saved")
