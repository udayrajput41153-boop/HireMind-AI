"""
HireMind AI — Multi-Agent Resume Screening & Job Matching Platform
FastAPI backend: 5 cooperating agents + static React build.

Agents:
  1. Resume Agent    — extract candidate profile
  2. Job Agent       — extract job requirements
  3. Matching Agent  — deterministic weighted fit score (explainable)
  4. Skill Gap Agent — missing skills + upskilling recommendations
  5. Recruiter Agent — candidate summary + hire recommendation
"""
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from store import store
from agents import ResumeAgent, JobAgent, MatchingAgent, SkillGapAgent, RecruiterAgent

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
STATIC_DIR = BASE_DIR / "static"

resume_agent = ResumeAgent()
job_agent = JobAgent()
matching_agent = MatchingAgent()
skill_gap_agent = SkillGapAgent()
recruiter_agent = RecruiterAgent()

app = FastAPI(title="HireMind AI", version="1.0.0")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)


# ---------------- helpers ----------------
def _read_upload_bytes(filename: str, raw: bytes) -> str:
    name = (filename or "").lower()
    if name.endswith(".pdf"):
        try:
            from pypdf import PdfReader
            import io
            reader = PdfReader(io.BytesIO(raw))
            return "\n".join((p.extract_text() or "") for p in reader.pages)
        except Exception as e:
            raise HTTPException(400, f"Could not parse PDF '{filename}': {e}")
    if name.endswith(".docx"):
        try:
            import io
            from docx import Document
            doc = Document(io.BytesIO(raw))
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception as e:
            raise HTTPException(400, f"Could not parse DOCX '{filename}': {e}")
    return raw.decode("utf-8", errors="ignore")


def _key_from_request(request: Request):
    return request.headers.get("x-gemini-key") or store.settings.get("gemini_key")


def _model_from_request(request: Request):
    return request.headers.get("x-gemini-model") or store.settings.get("model") or None


def _public_resume(rec):
    return {k: rec[k] for k in ("id", "filename", "profile", "engine", "created_at")}


def _public_job(rec):
    return {k: rec[k] for k in ("id", "filename", "requirements", "engine", "created_at")}


# ---------------- metadata ----------------
@app.get("/api/health")
def health():
    return {"status": "ok", "resumes": len(store.resumes), "jobs": len(store.jobs),
            "llm_configured": bool(store.settings.get("gemini_key"))}


@app.get("/api/agents")
def list_agents():
    return [
        {"id": 1, "name": resume_agent.name, "role": resume_agent.description},
        {"id": 2, "name": job_agent.name, "role": job_agent.description},
        {"id": 3, "name": matching_agent.name, "role": matching_agent.description},
        {"id": 4, "name": skill_gap_agent.name, "role": skill_gap_agent.description},
        {"id": 5, "name": recruiter_agent.name, "role": recruiter_agent.description},
    ]


# ---------------- settings ----------------
class SettingsIn(BaseModel):
    gemini_key: str | None = None
    model: str | None = None


@app.post("/api/settings")
def save_settings(body: SettingsIn):
    if body.gemini_key is not None:
        store.settings["gemini_key"] = body.gemini_key.strip() or None
    if body.model is not None:
        store.settings["model"] = body.model.strip() or None
    return {"llm_configured": bool(store.settings.get("gemini_key")), "model": store.settings.get("model")}


@app.get("/api/settings")
def get_settings():
    key = store.settings.get("gemini_key")
    return {"llm_configured": bool(key), "masked_key": (key[:4] + "…" + key[-4:]) if key else None,
            "model": store.settings.get("model")}


# ---------------- resumes ----------------
class ResumeTextIn(BaseModel):
    filename: str = "pasted-resume.txt"
    text: str


@app.post("/api/resumes/upload")
async def upload_resumes(request: Request, files: list[UploadFile] = File(...)):
    api_key, model = _key_from_request(request), _model_from_request(request)
    created = []
    for f in files:
        raw = await f.read()
        if not raw.strip():
            continue
        text = _read_upload_bytes(f.filename, raw)
        out = resume_agent.run(text, api_key, model)
        created.append(_public_resume(store.add_resume(f.filename, text, out["profile"], out["engine"])))
    return {"added": created, "total": len(store.resumes)}


@app.post("/api/resumes")
async def add_resume(request: Request, body: ResumeTextIn):
    api_key, model = _key_from_request(request), _model_from_request(request)
    text = body.text.strip()
    if not text:
        raise HTTPException(400, "Empty resume text")
    out = resume_agent.run(text, api_key, model)
    rec = store.add_resume(body.filename or "pasted-resume.txt", text, out["profile"], out["engine"])
    return {"added": [_public_resume(rec)], "total": len(store.resumes)}


@app.get("/api/resumes")
def get_resumes():
    return {"resumes": [_public_resume(r) for r in store.resumes.values()]}


@app.delete("/api/resumes/{rid}")
def del_resume(rid):
    if not store.delete_resume(rid):
        raise HTTPException(404, "Resume not found")
    return {"total": len(store.resumes)}


# ---------------- jobs ----------------
class JobIn(BaseModel):
    filename: str = "job-description.txt"
    text: str


@app.post("/api/jobs")
async def add_job(request: Request, body: JobIn):
    text = body.text.strip()
    if not text:
        raise HTTPException(400, "Empty job description")
    api_key, model = _key_from_request(request), _model_from_request(request)
    out = job_agent.run(text, api_key, model)
    rec = store.add_job(body.filename, text, out["requirements"], out["engine"])
    return {"job": _public_job(rec), "errors": out.get("errors", [])}


@app.get("/api/jobs")
def get_jobs():
    return {"jobs": [_public_job(j) for j in store.jobs.values()]}


@app.delete("/api/jobs/{jid}")
def del_job(jid):
    if not store.delete_job(jid):
        raise HTTPException(404, "Job not found")
    return {"total": len(store.jobs)}


# ---------------- matching ----------------
class MatchIn(BaseModel):
    job_id: str


@app.post("/api/match")
def match(request: Request, body: MatchIn):
    job = store.jobs.get(body.job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    if not store.resumes:
        raise HTTPException(400, "No resumes loaded")

    api_key = _key_from_request(request)
    model = _model_from_request(request)
    requirements = job["requirements"]

    rows = []
    for rec in store.resumes.values():
        profile = rec["profile"]
        m = matching_agent.score(profile, requirements, rec.get("raw_text", ""))
        gaps = skill_gap_agent.analyze(profile, requirements, m)
        rows.append({"rec": rec, "match": m, "gaps": gaps})

    rows.sort(key=lambda r: r["match"]["total"], reverse=True)

    # Recruiter summaries — parallel when using the LLM
    def summarize(row):
        return recruiter_agent.summarize(row["rec"]["profile"], requirements, row["match"], api_key, model)

    with ThreadPoolExecutor(max_workers=5) as ex:
        summaries = list(ex.map(summarize, rows))

    ranked = []
    for i, (row, summ) in enumerate(zip(rows, summaries), start=1):
        rec, m, g = row["rec"], row["match"], row["gaps"]
        ranked.append({
            "rank": i,
            "candidate_id": rec["id"],
            "name": rec["profile"].get("name"),
            "title": rec["profile"].get("title"),
            "years_experience": rec["profile"].get("years_experience"),
            "education": rec["profile"].get("education"),
            "profile": rec["profile"],
            "total": m["total"],
            "verdict": m["verdict"],
            "components": m["components"],
            "must_matched": m["must_matched"], "must_missing": m["must_missing"],
            "nice_matched": m["nice_matched"], "nice_missing": m["nice_missing"],
            "gaps": g,
            "summary": summ["summary"], "summary_engine": summ["engine"],
            "trace": {
                "resume_agent": {"engine": rec["engine"], "output": rec["profile"]},
                "job_agent": {"engine": job["engine"], "output": requirements},
                "matching_agent": {"weights": {"must_have": 45, "nice_to_have": 15, "experience": 20, "education": 10, "keywords": 10}, "output": m},
                "skill_gap_agent": {"output": g},
                "recruiter_agent": {"engine": summ["engine"], "output": summ["summary"]},
            },
        })

    result = {
        "job_id": body.job_id,
        "job": requirements,
        "job_engine": job["engine"],
        "match_engine": "deterministic-weighted",
        "summary_engine": summaries[0]["engine"] if summaries else "offline",
        "ranked": ranked,
    }
    store.results[body.job_id] = result
    return result


# ---------------- demo data ----------------
@app.post("/api/demo/load")
def load_demo(request: Request):
    api_key, model = _key_from_request(request), _model_from_request(request)
    resume_dir, job_dir = DATA_DIR / "resumes", DATA_DIR / "jobs"
    if not resume_dir.exists():
        raise HTTPException(500, "Demo data directory missing")
    store.clear_all()
    added_r, added_j = [], []
    for p in sorted(resume_dir.glob("*.txt")):
        text = p.read_text(encoding="utf-8")
        out = resume_agent.run(text, api_key, model)
        added_r.append(_public_resume(store.add_resume(p.name, text, out["profile"], out["engine"])))
    for p in sorted(job_dir.glob("*.txt")):
        text = p.read_text(encoding="utf-8")
        out = job_agent.run(text, api_key, model)
        added_j.append(_public_job(store.add_job(p.name, text, out["requirements"], out["engine"])))
    return {"resumes": added_r, "jobs": added_j}


@app.delete("/api/reset")
def reset():
    store.clear_all()
    return {"ok": True}


# ---------------- re-extract (after adding an API key) ----------------
@app.post("/api/reextract")
def reextract(request: Request):
    api_key, model = _key_from_request(request), _model_from_request(request)
    n_r = n_j = 0
    for rec in store.resumes.values():
        out = resume_agent.run(rec["raw_text"], api_key, model)
        rec["profile"], rec["engine"] = out["profile"], out["engine"]
        n_r += 1
    for rec in store.jobs.values():
        out = job_agent.run(rec["raw_text"], api_key, model)
        rec["requirements"], rec["engine"] = out["requirements"], out["engine"]
        n_j += 1
    return {"resumes": n_r, "jobs": n_j}


# ---------------- static frontend (production build) ----------------
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
