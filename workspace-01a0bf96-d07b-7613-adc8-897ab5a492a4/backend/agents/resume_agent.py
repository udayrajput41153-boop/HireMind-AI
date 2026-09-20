"""
AGENT 1 — Resume Agent
Extracts a structured candidate profile from raw resume text.
Uses Gemini when an API key is available; otherwise deterministic heuristics.
Output is always normalized against the shared skill taxonomy.
"""
from skills_taxonomy import canonicalize, category_of
import offline_extract
from .llm import gemini_json, LLMError

SYSTEM = "You are the Resume Agent in a multi-agent recruitment platform. You convert unstructured resumes into clean structured data. Always respond with valid JSON only."

PROMPT = """Extract structured candidate information from the resume below.
Return ONLY JSON with exactly these keys:
{
  "name": "string",
  "title": "string (current/most recent role)",
  "email": "string or null",
  "phone": "string or null",
  "skills": ["short skill labels, technical and notable soft skills"],
  "years_experience": number or null (TOTAL years of professional experience),
  "education": {"degree": "highest degree e.g. B.Tech / M.S. / MBA / PhD or null", "field": "string or null"},
  "highlights": ["up to 3 short achievement bullets"]
}

RESUME:
\"\"\"{text}\"\"\""""


def normalize_skills(skills):
    """Map arbitrary skill labels to canonical taxonomy names (unknown kept lowercase)."""
    out, seen = [], set()
    for s in skills or []:
        if not isinstance(s, str):
            continue
        canon = canonicalize(s) or s.strip().lower()
        if canon and canon not in seen:
            seen.add(canon)
            out.append({"name": canon, "category": category_of(canon)})
    return out


class ResumeAgent:
    name = "Resume Agent"
    description = "Parses resume text into a structured candidate profile (skills, experience, education)."

    def run(self, raw_text, api_key=None, model=None):
        errors = []
        if api_key:
            try:
                data = gemini_json(PROMPT.format(text=raw_text[:12000]), api_key, model, system=SYSTEM)
                edu = data.get("education") or {}
                if isinstance(edu, str):
                    edu = {"degree": edu, "field": None}
                profile = {
                    "name": (data.get("name") or "Unknown Candidate").strip(),
                    "title": (data.get("title") or "Professional").strip(),
                    "email": data.get("email"),
                    "phone": data.get("phone"),
                    "skills": normalize_skills(data.get("skills") or []),
                    "years_experience": data.get("years_experience"),
                    "education": {"degree": edu.get("degree") or "Unknown",
                                  "field": edu.get("field"),
                                  "rank": offline_extract._detect_education(str(edu.get("degree") or ""))["rank"]},
                    "highlights": [str(h) for h in (data.get("highlights") or [])][:3],
                }
                # heuristic backfill for anything the model missed
                if not profile["skills"]:
                    profile["skills"] = offline_extract.extract_resume(raw_text)["skills"]
                return {"profile": profile, "engine": "gemini", "errors": errors}
            except LLMError as e:
                errors.append(str(e))
        profile = offline_extract.extract_resume(raw_text)
        profile["highlights"] = []
        return {"profile": profile, "engine": "offline", "errors": errors}
