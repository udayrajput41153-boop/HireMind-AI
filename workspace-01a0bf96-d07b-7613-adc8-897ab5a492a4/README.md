# HireMind AI — Multi-Agent Resume Screening & Job Matching Platform

**Hackathon Problem Statement PS03** · NLP + LLM + Agentic AI

A multi-agent recruitment platform that evaluates resumes against job descriptions and
produces **explainable, ranked candidate-role matches** — with a per-agent trace so every
score can be audited.

---

## 🏗 Architecture — 5 cooperating agents

```
 Resume (.txt/.pdf/.docx)          Job Description (text)
        │                                   │
        ▼                                   ▼
┌───────────────┐                   ┌──────────────┐
│ 1. Resume     │                   │ 2. Job       │
│    Agent      │                   │    Agent     │
│ (Gemini or    │                   │ (Gemini or   │
│  heuristics)  │                   │  heuristics) │
└──────┬────────┘                   └──────┬───────┘
       │ structured profile                │ structured requirements
       │ skills · yoe · education          │ must-have · nice-to-have · yoe · edu
       └───────────────┬───────────────────┘
                       ▼
            ┌─────────────────────┐
            │ 3. Matching Agent   │  deterministic weighted score 0-100
            │ must 45% · nice 15% │  experience 20% · education 10% · keywords 10%
            └──────────┬──────────┘
                       ▼
            ┌─────────────────────┐
            │ 4. Skill Gap Agent  │  critical gaps · stretch gaps ·
            │                     │  adjacent strengths · upskilling plan
            └──────────┬──────────┘
                       ▼
            ┌─────────────────────┐
            │ 5. Recruiter Agent  │  human summary + interview/hold/pass
            └─────────────────────┘
```

**Design choices judges should know:**
- **Extraction agents are LLM-powered (Gemini) when a key is provided, with a
  deterministic offline NLP fallback** — the demo never breaks, even without internet/keys.
  All LLM outputs are re-normalized against a shared skill taxonomy (~130 skills, aliases,
  categories) so matching is consistent regardless of engine.
- **The Matching Agent is deliberately deterministic** (weighted scoring, fuzzy skill
  matching) — explainable, auditable, and reproducible. No LLM "black box" decides rankings.
- Every match carries a full **agent trace** (each agent's engine + output JSON), shown in the UI.
- Recruiter summaries run **in parallel** (thread pool) to keep matching fast.

## ✨ Features
- Upload resumes (`.txt`, `.pdf`, `.docx`) or paste text; add JDs by paste
- One-click **demo dataset: 10 resumes × 3 job descriptions**
- Ranked candidate list per job with verdict badges (Strong / Good / Partial / Weak)
- Per-dimension score bars, must-have ✓/✗ skill chips, nice-to-have coverage
- Skill-gap panel with severity + concrete upskilling recommendations + adjacent strengths
- Recruiter summary with hire recommendation per candidate
- Settings panel for Gemini API key + model; "Re-extract with Gemini" after adding a key

## 🚀 Run locally

```bash
# Backend (Python 3.10+)
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000   # serves API + built frontend

# Frontend (only needed for development)
cd frontend
npm install
npm run build        # builds into backend/static
# or: npm run dev    # vite dev server with /api proxy to :8000
```

Open **http://localhost:8000** → click **⚡ Load demo dataset** → tab 3 → **▶ Run Matching Pipeline**.

To enable Gemini agents: ⚙ Settings → paste your Google Gemini API key (browser-local) →
"Re-extract with Gemini". Default model `gemini-2.5-flash`.

## 📊 Demo script (2-minute pitch flow)
1. Click **Load demo dataset** — show the Resume/Job Agent cards with extracted skills
   (badge shows ✦ Gemini vs ⚙ offline).
2. Tab 3 → run the pipeline — the agent strip animates all 5 agents.
3. Show ranked list for the *Senior ML Engineer* JD → Aarav Sharma #1 (95/100).
4. Open a mid-rank candidate → explainable breakdown, red skill-gap chips, upskilling plan.
5. Open **Agent trace** — raw input/output of every agent (explainability requirement ✔).
6. Switch jobs — rankings reorder instantly (deterministic re-scoring).

## 📁 Repository layout
```
backend/
  main.py                  FastAPI app: REST API + serves React build
  store.py                 in-memory store (swap for DB in production)
  skills_taxonomy.py       canonical skill taxonomy + alias map
  offline_extract.py       deterministic extraction heuristics (fallback)
  agents/
    llm.py                 Gemini REST client (JSON mode)
    resume_agent.py        Agent 1 — candidate profile extraction
    job_agent.py           Agent 2 — job requirement extraction
    matching_agent.py      Agent 3 — weighted deterministic scoring
    skill_gap_agent.py     Agent 4 — gaps + upskilling recommendations
    recruiter_agent.py     Agent 5 — recruiter summary + recommendation
  static/                  built React frontend (vite build output)
frontend/                  React + Vite source
data/
  resumes/                 10 synthetic demo resumes
  jobs/                    3 synthetic demo job descriptions
test_pipeline.py           end-to-end smoke test
```

## 🗂 Datasets
- Bundled demo data is **synthetic** (no participant data collected, per PS03).
- For real-scale evaluation, public resume/JD datasets exist on Kaggle & Hugging Face
  (e.g., "Updated Resume Dataset", job-posting corpora). **Verify license, version and
  access conditions before use**, as the problem statement requires.

## ⚖️ Explainability & fairness notes
- Ranking math is public in `matching_agent.py` (weights are constants, easily tuned).
- No demographic attributes (name/gender/photo/age) are used in scoring — only skills,
  experience, education and JD keywords.
- Fuzzy skill matching (`skill_match`) prevents alias mismatches ("React.js" = "React").
