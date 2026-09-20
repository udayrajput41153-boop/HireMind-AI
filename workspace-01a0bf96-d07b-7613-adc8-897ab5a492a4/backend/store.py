"""In-memory store. Fine for a hackathon demo; swap for a DB in production."""
import uuid
from datetime import datetime


class Store:
    def __init__(self):
        self.resumes = {}   # id -> {id, filename, raw_text, profile, engine, created_at}
        self.jobs = {}      # id -> {id, filename, raw_text, requirements, engine, created_at}
        self.results = {}   # job_id -> last match run
        self.settings = {"gemini_key": None, "model": None}

    # ---- resumes ----
    def add_resume(self, filename, raw_text, profile, engine):
        rid = uuid.uuid4().hex[:8]
        rec = {
            "id": rid, "filename": filename, "raw_text": raw_text,
            "profile": profile, "engine": engine,
            "created_at": datetime.utcnow().isoformat() + "Z",
        }
        self.resumes[rid] = rec
        return rec

    def delete_resume(self, rid):
        return self.resumes.pop(rid, None)

    # ---- jobs ----
    def add_job(self, filename, raw_text, requirements, engine):
        jid = uuid.uuid4().hex[:8]
        rec = {
            "id": jid, "filename": filename, "raw_text": raw_text,
            "requirements": requirements, "engine": engine,
            "created_at": datetime.utcnow().isoformat() + "Z",
        }
        self.jobs[jid] = rec
        return rec

    def delete_job(self, jid):
        self.results.pop(jid, None)
        return self.jobs.pop(jid, None)

    def clear_all(self):
        self.resumes.clear()
        self.jobs.clear()
        self.results.clear()


store = Store()
