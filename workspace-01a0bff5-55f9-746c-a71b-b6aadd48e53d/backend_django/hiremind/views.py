"""
HireMind AI — Django views.
Implements the SAME REST API as the FastAPI backend by reusing the exact same
agent code from ../backend (single source of truth for the 5 agents).
"""
import io
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from django.http import FileResponse, JsonResponse
from django.views.static import serve as static_serve

BACKEND = Path(__file__).resolve().parent.parent.parent / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from store import store                                  # noqa: E402
from agents import (ResumeAgent, JobAgent, MatchingAgent,  # noqa: E402
                    SkillGapAgent, RecruiterAgent)

STATIC_DIR = BACKEND / "static"
DATA_DIR = BACKEND.parent / "data"

resume_agent = ResumeAgent()
job_agent = JobAgent()
matching_agent = MatchingAgent()
skill_gap_agent = SkillGapAgent()
recruiter_agent = RecruiterAgent()


# ---------------- helpers ----------------
def _body(request):
    try:
        return json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        return {}


def _key(request):
    return request.headers.get("x-gemini-key") or store.settings.get("gemini_key")


def _model(request):
    return request.headers.get("x-gemini-model") or store.settings.get("model") or None


def _err(msg, status=400):
    return JsonResponse({"detail": msg}, status=status)


def _public_resume(rec):
    return {k: rec[k] for k in ("id", "filename", "profile", "engine", "created_at")}


def _public_job(rec):
    return {k: rec[k] for k in ("id", "filename", "requirements", "engine", "created_at")}


def _read_upload(filename, raw):
    name = (filename or "").lower()
    if name.endswith(".pdf"):
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(raw))
            return "\n".join((p.extract_text() or "") for p in reader.pages)
        except Exception as e:
            raise ValueError(f"Could not parse PDF '{filename}': {e}")
    if name.endswith(".docx"):
        try:
            from docx import Document
            d = Document(io.BytesIO(raw))
            return "\n".join(p.text for p in d.paragraphs)
        except Exception as e:
            raise ValueError(f"Could not parse DOCX '{filename}': {e}")
    return raw.decode("utf-8", errors="ignore")


# ---------------- static / index ----------------
def index(request):
    return FileResponse(open(STATIC_DIR / "index.html", "rb"), content_type="text/html")


def serve_assets(request, path):
    return static_serve(request, path, document_root=str(STATIC_DIR / "assets"))


# ---------------- metadata ----------------
def health(request):
    return JsonResponse({"status": "ok", "resumes": len(store.resumes), "jobs": len(store.jobs),
                         "llm_configured": bool(store.settings.get("gemini_key")),
                         "backend": "django"})


def agents_list(request):
    return JsonResponse([
        {"id": 1, "name": resume_agent.name, "role": resume_agent.description},
        {"id": 2, "name": job_agent.name, "role": job_agent.description},
        {"id": 3, "name": matching_agent.name, "role": matching_agent.description},
        {"id": 4, "name": skill_gap_agent.name, "role": skill_gap_agent.description},
        {"id": 5, "name": recruiter_agent.name, "role": recruiter_agent.description},
    ], safe=False)


def settings_view(request):
    if request.method == "POST":
        body = _body(request)
        if body.get("gemini_key") is not None:
            store.settings["gemini_key"] = (body.get("gemini_key") or "").strip() or None
        if body.get("model") is not None:
            store.settings["model"] = (body.get("model") or "").strip() or None
    key = store.settings.get("gemini_key")
    return JsonResponse({"llm_configured": bool(key),
                         "masked_key": (key[:4] + "…" + key[-4:]) if key else None,
                         "model": store.settings.get("model")})


# ---------------- resumes ----------------
def resumes_upload(request):
    if request.method != "POST":
        return _err("POST required", 405)
    key, model = _key(request), _model(request)
    added = []
    files = request.FILES.getlist("files")
    if not files:
        return _err("No files uploaded")
    for f in files:
        raw = f.read()
        if not raw.strip():
            continue
        try:
            text = _read_upload(f.name, raw)
        except ValueError as e:
            return _err(str(e))
        out = resume_agent.run(text, key, model)
        added.append(_public_resume(store.add_resume(f.name, text, out["profile"], out["engine"])))
    return JsonResponse({"added": added, "total": len(store.resumes)})


def resumes_view(request):
    if request.method == "POST":
        body = _body(request)
        text = (body.get("text") or "").strip()
        if not text:
            return _err("Empty resume text")
        out = resume_agent.run(text, _key(request), _model(request))
        rec = store.add_resume(body.get("filename") or "pasted-resume.txt", text, out["profile"], out["engine"])
        return JsonResponse({"added": [_public_resume(rec)], "total": len(store.resumes)})
    return JsonResponse({"resumes": [_public_resume(r) for r in store.resumes.values()]})


def resume_delete(request, rid):
    if not store.delete_resume(rid):
        return _err("Resume not found", 404)
    return JsonResponse({"total": len(store.resumes)})


# ---------------- jobs ----------------
def jobs_view(request):
    if request.method == "POST":
        body = _body(request)
        text = (body.get("text") or "").strip()
        if not text:
            return _err("Empty job description")
        out = job_agent.run(text, _key(request), _model(request))
        rec = store.add_job(body.get("filename") or "job-description.txt", text, out["requirements"], out["engine"])
        return JsonResponse({"job": _public_job(rec), "errors": out.get("errors", [])})
    return JsonResponse({"jobs": [_public_job(j) for j in store.jobs.values()]})


def job_delete(request, jid):
    if not store.delete_job(jid):
        return _err("Job not found", 404)
    return JsonResponse({"total": len(store.jobs)})


# ---------------- matching ----------------
def match(request):
    if request.method != "POST":
        return _err("POST required", 405)
    body = _body(request)
    job = store.jobs.get(body.get("job_id"))
    if not job:
        return _err("Job not found", 404)
    if not store.resumes:
        return _err("No resumes loaded")

    api_key, model = _key(request), _model(request)
    requirements = job["requirements"]

    rows = []
    for rec in store.resumes.values():
        m = matching_agent.score(rec["profile"], requirements, rec.get("raw_text", ""))
        gaps = skill_gap_agent.analyze(rec["profile"], requirements, m)
        rows.append({"rec": rec, "match": m, "gaps": gaps})
    rows.sort(key=lambda r: r["match"]["total"], reverse=True)

    def summarize(row):
        return recruiter_agent.summarize(row["rec"]["profile"], requirements, row["match"], api_key, model)

    with ThreadPoolExecutor(max_workers=5) as ex:
        summaries = list(ex.map(summarize, rows))

    ranked = []
    for i, (row, summ) in enumerate(zip(rows, summaries), start=1):
        rec, m, g = row["rec"], row["match"], row["gaps"]
        ranked.append({
            "rank": i, "candidate_id": rec["id"],
            "name": rec["profile"].get("name"), "title": rec["profile"].get("title"),
            "years_experience": rec["profile"].get("years_experience"),
            "education": rec["profile"].get("education"), "profile": rec["profile"],
            "total": m["total"], "verdict": m["verdict"], "components": m["components"],
            "must_matched": m["must_matched"], "must_missing": m["must_missing"],
            "nice_matched": m["nice_matched"], "nice_missing": m["nice_missing"],
            "gaps": g, "summary": summ["summary"], "summary_engine": summ["engine"],
            "trace": {
                "resume_agent": {"engine": rec["engine"], "output": rec["profile"]},
                "job_agent": {"engine": job["engine"], "output": requirements},
                "matching_agent": {"weights": {"must_have": 45, "nice_to_have": 15, "experience": 20, "education": 10, "keywords": 10}, "output": m},
                "skill_gap_agent": {"output": g},
                "recruiter_agent": {"engine": summ["engine"], "output": summ["summary"]},
            },
        })

    result = {"job_id": body.get("job_id"), "job": requirements, "job_engine": job["engine"],
              "match_engine": "deterministic-weighted",
              "summary_engine": summaries[0]["engine"] if summaries else "offline",
              "ranked": ranked, "backend": "django"}
    store.results[job["id"]] = result
    return JsonResponse(result)


# ---------------- demo / reset / reextract ----------------
def demo_load(request):
    if request.method != "POST":
        return _err("POST required", 405)
    key, model = _key(request), _model(request)
    resume_dir, job_dir = DATA_DIR / "resumes", DATA_DIR / "jobs"
    if not resume_dir.exists():
        return _err("Demo data directory missing", 500)
    store.clear_all()
    added_r, added_j = [], []
    for p in sorted(resume_dir.glob("*.txt")):
        text = p.read_text(encoding="utf-8")
        out = resume_agent.run(text, key, model)
        added_r.append(_public_resume(store.add_resume(p.name, text, out["profile"], out["engine"])))
    for p in sorted(job_dir.glob("*.txt")):
        text = p.read_text(encoding="utf-8")
        out = job_agent.run(text, key, model)
        added_j.append(_public_job(store.add_job(p.name, text, out["requirements"], out["engine"])))
    return JsonResponse({"resumes": added_r, "jobs": added_j})


def reset(request):
    store.clear_all()
    return JsonResponse({"ok": True})


def reextract(request):
    if request.method != "POST":
        return _err("POST required", 405)
    key, model = _key(request), _model(request)
    for rec in store.resumes.values():
        out = resume_agent.run(rec["raw_text"], key, model)
        rec["profile"], rec["engine"] = out["profile"], out["engine"]
    for rec in store.jobs.values():
        out = job_agent.run(rec["raw_text"], key, model)
        rec["requirements"], rec["engine"] = out["requirements"], out["engine"]
    return JsonResponse({"resumes": len(store.resumes), "jobs": len(store.jobs)})
