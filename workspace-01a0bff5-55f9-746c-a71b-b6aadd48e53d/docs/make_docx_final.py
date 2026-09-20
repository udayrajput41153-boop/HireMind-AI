"""Final comprehensive project report as Word (.docx) — with PROJECT FEATURES
and VIRTUAL ENVIRONMENT sections."""
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
st = doc.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(11)

INDIGO = RGBColor(0x4F, 0x46, 0xE5)
CYAN = RGBColor(0x08, 0x91, 0xB2)
EMERALD = RGBColor(0x04, 0x78, 0x57)
GRAY = RGBColor(0x6B, 0x72, 0x80)
DARK = RGBColor(0x1F, 0x29, 0x37)
S = "/home/user/docs/shots/"


def para(t, size=11, color=DARK, bold=False, align=None, after=6):
    p = doc.add_paragraph()
    if align:
        p.alignment = align
    r = p.add_run(t)
    r.font.size = Pt(size)
    r.font.color.rgb = color
    r.bold = bold
    p.paragraph_format.space_after = Pt(after)
    return p


def title(t, size=28, color=INDIGO, align=WD_ALIGN_PARAGRAPH.CENTER):
    return para(t, size, color, True, align, 6)


def h1(t):
    p = doc.add_paragraph()
    r = p.add_run(t)
    r.bold = True
    r.font.size = Pt(16)
    r.font.color.rgb = INDIGO
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)


def h2(t):
    p = doc.add_paragraph()
    r = p.add_run(t)
    r.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = CYAN
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)


def body(t):
    return para(t, 11, DARK, False, None, 6)


def bul(t):
    p = doc.add_paragraph(style="List Bullet")
    p.clear()
    p.add_run(t)
    p.paragraph_format.space_after = Pt(4)


def img(path, w=6.4):
    doc.add_picture(path, width=Inches(w))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER


def cap(t):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(t)
    r.italic = True
    r.font.size = Pt(9)
    r.font.color.rgb = GRAY
    p.paragraph_format.space_after = Pt(10)


def code(t):
    p = doc.add_paragraph()
    r = p.add_run(t)
    r.font.name = "Consolas"
    r.font.size = Pt(9)
    p.paragraph_format.space_after = Pt(8)


def table(rows):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = "Light Grid Accent 1"
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j)
            c.text = str(val)
            if i == 0:
                for p in c.paragraphs:
                    for r in p.runs:
                        r.bold = True
    doc.add_paragraph()


# ================= COVER =================
doc.add_paragraph()
title("HireMind AI", 30)
title("Multi-Agent Resume Screening & Job Matching Platform", 14, DARK)
title("FINAL PROJECT REPORT — Hackathon Problem Statement PS03", 12, CYAN, WD_ALIGN_PARAGRAPH.CENTER)
doc.add_paragraph()
img("/home/user/docs/architecture.png", 6.3)
cap("Figure 0 — Five-agent pipeline: LLM-powered extraction around a deterministic, explainable matching core.")
table([
    ["Field", "Details"],
    ["Problem Statement", "PS03 — Multi-Agent Resume Screening & Job Matching Platform"],
    ["Technology Category", "NLP + LLM + Agentic AI"],
    ["Team", "[YOUR TEAM NAME] — [MEMBERS]"],
    ["Hackathon", "[HACKATHON NAME]"],
    ["Date / Version", "20 Sept 2026 · v2.0 (final)"],
])
doc.add_page_break()

# ================= 1 =================
h1("1. Executive Summary")
body("HireMind AI is a multi-agent recruitment platform that screens resumes against job descriptions and produces ranked, fully explainable candidate–role matches. Five cooperating agents — Resume, Job, Matching, Skill Gap and Recruiter — mirror a human recruiting team at machine speed.")
body("Architectural signature: “LLM extracts, never decides.” Google Gemini (optional, user-supplied key) performs information extraction and summarisation; the ranking decision is produced by a deterministic weighted engine, giving reproducible, auditable outcomes. A rule-based offline NLP layer makes the platform fully functional without any API key.")
body("The intelligence layer is framework-agnostic: the identical agent codebase is served by two interchangeable backends — Python FastAPI and Django — behind one REST contract, with a React 18 frontend on top. The PS03 required demonstration (10 resumes × 3 job descriptions → ranked lists) passes end-to-end on both, verified by a 72-check automated QA suite (72/72 passing).")

# ================= 2 =================
h1("2. Problem Analysis")
body("Manual resume screening is slow (≈7 seconds per resume at first pass), inconsistent between screeners, vocabulary-sensitive (“React.js” vs “React”), and opaque to candidates. We decomposed the problem into five sub-problems, each assigned to one agent:")
table([
    ["Sub-problem", "Agent responsible"],
    ["P1 Heterogeneous resume formats (txt/pdf/docx, free text)", "Resume Agent"],
    ["P2 Ambiguous JDs (must-have vs nice-to-have separation)", "Job Agent"],
    ["P3 Multi-dimensional compatibility measurement", "Matching Agent"],
    ["P4 Actionable feedback on missing skills", "Skill Gap Agent"],
    ["P5 Explainability, reproducibility & trust", "Deterministic core + Agent Trace"],
])

# ================= 3 =================
h1("3. Research")
h2("3.1 Approaches surveyed")
bul("Keyword/ATS matching — fast, brittle to synonyms.")
bul("Embedding similarity — synonym-tolerant but opaque single score.")
bul("LLM-only screening — expressive but non-reproducible and hard to audit.")
bul("Hybrid agentic systems (2025–26 SOTA) — specialised agents around a deterministic decision core; adopted.")
h2("3.2 Design conclusions")
bul("Extraction = language task → Gemini with deterministic fallback; all outputs normalised through a shared ~130-skill taxonomy (aliases: js→javascript, k8s→kubernetes, sklearn→scikit-learn).")
bul("Ranking = decision task → published fixed weights; fuzzy matching (containment + difflib ≥ 0.85) removes vocabulary false-negatives.")
h2("3.3 Datasets")
body("Kaggle/Hugging Face resume & JD corpora surveyed for scale-up; demonstration uses a fully synthetic 10+3 dataset (no participant data, per PS03). Any real dataset adopted later will have license/version/access conditions verified first, as the source note requires.")

# ================= 4 =================
h1("4. Proposed Solution")
table([
    ["#", "Agent", "Output", "Engine"],
    ["1", "Resume Agent", "Profile: canonical skills, experience, education, highlights", "Gemini JSON-mode / offline heuristics"],
    ["2", "Job Agent", "Must-have / nice-to-have skills, min experience, education", "Gemini JSON-mode / offline heuristics"],
    ["3", "Matching Agent", "0–100 score, verdict, per-dimension breakdown", "Deterministic (always)"],
    ["4", "Skill Gap Agent", "Critical & stretch gaps, adjacent strengths, learning plan", "Deterministic rules"],
    ["5", "Recruiter Agent", "Summary + interview/hold/pass recommendation (parallelised)", "Gemini / template"],
])
bul("Dual-mode resilience: identical schema from Gemini or offline path — the demo never breaks on stage.")
bul("Single REST contract implemented twice (FastAPI, Django) over one shared agent codebase.")
bul("Agent Trace: every match carries each agent's engine + full JSON output for audit.")

# ================= 5 =================
h1("5. Technical Flow & Scoring Model")
bul("Intake → Extraction (Agents 1–2) → Weighted scoring (Agent 3) → Gap analysis (Agent 4) → Summary (Agent 5) → Ranked list + trace.")
table([
    ["Dimension", "Weight", "Computation"],
    ["Must-have skills", "45%", "Fraction matched (fuzzy + taxonomy)"],
    ["Nice-to-have skills", "15%", "Fraction matched"],
    ["Experience", "20%", "1.0 if ≥ required; 0.6×(cand/req) below; 0.75 unspecified"],
    ["Education", "10%", "Degree-rank comparison (PhD > Master > Bachelor > Diploma)"],
    ["Keyword affinity", "10%", "JD keywords found in resume text"],
])
img(S + "k3_pie.png", 6.2)
cap("Figure 1 — The score pie: fixed, public slices; same input ⇒ same score, always.")
body("Verdicts: ≥80 Strong · 60–79 Good · 40–59 Partial · <40 Weak. Weights renormalise when a dimension is absent.")

# ================= 6 FEATURES (NEW) =================
h1("6. PROJECT FEATURES")
h2("6.1 Core platform features")
bul("Multi-agent AI pipeline — 5 specialised agents (Resume, Job, Matching, Skill Gap, Recruiter) working in sequence.")
bul("Ranked candidate lists — 10 resumes × 3 job descriptions produce sorted, verdict-badged rankings (Strong/Good/Partial/Weak).")
bul("Explainable scores — every 0–100 score decomposes into 5 published weighted dimensions with plain-language notes.")
bul("Skill-gap analysis — critical vs nice-to-have gaps, adjacent strengths, and a concrete upskilling plan per candidate.")
bul("Recruiter summaries — human-readable notes with interview / hold / pass recommendations.")
bul("Agent Trace panel — raw input/output JSON of every agent for any match (full auditability).")
bul("Resume intake — upload .txt / .pdf / .docx or paste text; JDs by paste; per-document engine badge.")
bul("One-click demo dataset — loads the exact PS03 demonstration (10 resumes + 3 JDs) instantly.")
bul("Gemini integration — optional Google Gemini 2.5 Flash extraction/summaries via Settings (key stays in the browser, never hard-coded).")
bul("Offline / no-AI mode — deterministic fallback so the app works with zero keys and zero internet.")
h2("6.2 Engineering features")
bul("Dual backend — the same agents + same REST API run on FastAPI (:8000) and Django (:8001); health endpoint reports the flavour.")
bul("Deterministic & reproducible — identical inputs ⇒ identical scores/ordering, every run.")
bul("Fairness by design — scoring never sees names, photos, ages or genders; alias + fuzzy matching removes terminology bias.")
bul("Shared 130-skill taxonomy — single contract normalising LLM output and heuristic scans.")
bul("Parallel recruiter summaries — thread pool keeps matching fast.")
bul("Automated QA — test_pipeline.py + test_everything.py = 72 checks across both backends, all passing.")
bul("Dark, judge-ready React dashboard — tabs, animated pipeline strip, score bars, ✓/✗ chips.")
bul("Production-style delivery — FastAPI/Django serve the built React app; Vite dev proxy for hot reload.")

# ================= 7 =================
h1("7. Technology Stack")
table([
    ["Layer", "Technology", "Rationale"],
    ["Frontend", "React 18 + Vite", "Agent cards, ranked lists, explainable panels; HMR dev"],
    ["Backend A", "Python 3 + FastAPI (Uvicorn)", "Async REST, OpenAPI docs, serves React build"],
    ["Backend B", "Django 6 (runserver/WSGI)", "Same API contract; proves framework-agnostic agents"],
    ["LLM", "Google Gemini 2.5 Flash (REST)", "JSON-mode extraction/summaries; user-supplied key"],
    ["Offline NLP", "Regex + 130-skill taxonomy + difflib", "Deterministic fallback & alias normalisation"],
    ["Parsing", "pypdf · python-docx", "Real-world resume formats"],
    ["QA", "test_pipeline.py · test_everything.py (72 checks)", "Automated verification of both backends"],
])
h2("7.1 Repository layout")
code(
    "backend/            FastAPI app + agents/* + skills_taxonomy + offline_extract + store + static/ (React build)\n"
    "backend_django/       Django project (manage.py, hiremind/{settings,urls,views}) reusing backend/ agents\n"
    "frontend/             React + Vite source (src/components/*, api.js)\n"
    "data/resumes/ (10) · data/jobs/ (3)   synthetic demo dataset\n"
    "docs/                 reports (PDF/DOCX), pitch deck (PPTX), diagrams, screenshots\n"
    "test_pipeline.py · test_everything.py"
)

# ================= 8 =================
h1("8. REST API (identical on both backends)")
table([
    ["Endpoint", "Purpose"],
    ["POST /api/resumes · /api/resumes/upload", "Register resumes (paste or multipart files) → Agent 1"],
    ["POST /api/jobs", "Register JD → Agent 2"],
    ["POST /api/demo/load", "Load 10-resume / 3-JD demo set"],
    ["POST /api/match {job_id}", "Agents 3–5 over all candidates → ranked list + traces"],
    ["POST /api/reextract · POST /api/settings", "Re-extraction with Gemini · key/model config"],
    ["GET /api/agents · /api/health · /api/resumes · /api/jobs", "Metadata, health (reports backend), listings"],
    ["DELETE /api/resumes/{id} · /api/jobs/{id} · /api/reset", "Housekeeping"],
])

# ================= 9 =================
h1("9. Application Screenshots (captured live)")
img(S + "01_resumes.png")
cap("Figure 2 — Resume Agent output: 10 extracted candidate cards.")
doc.add_page_break()
img(S + "03_ranked.png")
cap("Figure 3 — Ranked list for Senior ML Engineer with verdict badges and score bars.")
img(S + "04_detail.png")
cap("Figure 4 — Explainable match report: summary, ✓/✗ coverage, breakdown, gap plan, trace.")

# ================= 10 =================
h1("10. Verification & QA (72/72 passing)")
body("Two suites run on both backends. Latest run: 72 passed, 0 failed.")
table([
    ["Job", "#1", "#2", "#3"],
    ["Senior ML Engineer", "Aarav Sharma — 95.0 Strong (7/7)", "Priya Nair — 69.0 Good", "Divya Reddy — 59.2 Partial"],
    ["Full-Stack Developer", "Sneha Kulkarni — 100.0 Strong (5/5)", "Rohan Mehta — 81.0 Strong", "Vikram Singh — 66.2 Good"],
    ["Data Analyst", "Karan Patel — 80.7 Strong", "Priya Nair — 78.0 Good", "Aarav Sharma — 46.7 Partial"],
])
bul("Identical rankings on FastAPI and Django — the agent layer is provably framework-independent.")
bul("Error paths verified: unknown job/resume → 404; empty inputs → 400; reset/reextract flows pass.")
bul("UI verified by headless-Chromium screenshots; report pages rendered and visually inspected.")

# ================= 11 =================
h1("11. Explainability, Fairness & Innovation")
bul("Published weights + plain-language notes per dimension; Agent Trace exposes every agent's raw I/O.")
bul("Scoring uses only skills/experience/education/keywords — never names, photos, ages, genders.")
bul("Innovations: “LLM extracts, never decides”; dual-engine resilience; adjacency-aware gap analysis; shared taxonomy contract; dual-backend portability; one-click PS03 demo.")

# ================= 12 =================
h1("12. Limitations & Roadmap")
bul("Offline heuristics extract fewer skills from very unstructured resumes (mitigated by dual mode).")
bul("In-memory persistence → roadmap: SQLite/Postgres, match history, accounts.")
bul("Roadmap: embedding similarity as 6th signal; layout-aware PDF parsing; multi-job comparison board; CSV/PDF export; fairness audits.")

# ================= 13 VENV (NEW) =================
h1("13. VIRTUAL ENVIRONMENT & SETUP")
body("A Python virtual environment (venv) keeps all project dependencies isolated from your system Python. Follow these steps exactly:")
h2("13.1 Create the virtual environment (once)")
code(
    "# from the project root\n"
    "python3 -m venv venv            # Linux / macOS\n"
    "python -m venv venv             # Windows"
)
h2("13.2 Activate it (every new terminal)")
code(
    "source venv/bin/activate        # Linux / macOS\n"
    "venv\\Scripts\\activate           # Windows (Command Prompt)\n"
    "# you should see (venv) at the start of your prompt"
)
h2("13.3 Install dependencies inside (venv)")
code(
    "pip install -r backend/requirements.txt     # fastapi, uvicorn, pypdf, python-docx, requests…\n"
    "pip install django                          # for the Django backend"
)
h2("13.4 Run the servers (with venv active)")
code(
    "# FastAPI backend + React UI\n"
    "cd backend && uvicorn main:app --host 0.0.0.0 --port 8000\n\n"
    "# OR Django backend + same React UI (separate terminal)\n"
    "cd backend_django && python manage.py runserver 0.0.0.0 --port 8001"
)
h2("13.5 Frontend development (Node — separate from venv)")
code("cd frontend && npm install && npm run dev   # Vite, /api proxied to :8000")
h2("13.6 Run the QA suite")
code(
    "python3 test_pipeline.py                     # end-to-end demo on :8000\n"
    "python3 test_pipeline.py http://localhost:8001   # same on Django\n"
    "python3 test_everything.py                   # full 72-check suite"
)
h2("13.7 When finished")
code("deactivate        # leaves the virtual environment")
body("Tip for judging day: activate the venv, start one backend, open the shown URL, click “Load demo dataset”, then “Run Matching Pipeline”.")

# ================= 14 =================
h1("14. External / AI Resources (Disclosure)")
bul("Google Gemini 2.5 Flash — optional runtime extraction/summaries via official REST API (user key, never hard-coded).")
bul("AI-assisted development — Arena.ai Agent Mode assisted scaffolding/drafting; all design decisions and verification team-reviewed.")
bul("Open-source: React, Vite, FastAPI, Django, python-docx, pypdf, Pillow, reportlab, python-pptx, Playwright, difflib.")
bul("Demo data 100% synthetic; no participant data collected (per PS03).")

# ================= 15 =================
h1("15. References")
bul("[1] Gemini API — ai.google.dev · [2] FastAPI — fastapi.tiangolo.com · [3] Django — djangoproject.com")
bul("[4] React — react.dev · [5] Vite — vite.dev · [6] pypdf / python-docx docs")
bul("[7] Python difflib — docs.python.org · [8] Python venv docs — docs.python.org/3/library/venv.html")
bul("[9] Kaggle & Hugging Face resume/JD datasets (surveyed; verify licenses before use)")

doc.save("/home/user/docs/HireMind_AI_Final_ProjectReport.docx")
print("final DOCX saved")
