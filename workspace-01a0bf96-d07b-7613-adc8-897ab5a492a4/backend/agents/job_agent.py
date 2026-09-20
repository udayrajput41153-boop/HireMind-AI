"""
AGENT 2 — Job Agent
Extracts structured requirements from a job description.
Gemini when available, deterministic heuristics otherwise.
"""
from skills_taxonomy import category_of, canonicalize
import offline_extract
from .llm import gemini_json, LLMError
from .resume_agent import normalize_skills

SYSTEM = "You are the Job Agent in a multi-agent recruitment platform. You convert job descriptions into clean structured requirements. Always respond with valid JSON only."

PROMPT = """Extract structured requirements from the job description below.
Return ONLY JSON with exactly these keys:
{
  "title": "string (job title)",
  "must_have_skills": ["skills explicitly required"],
  "nice_to_have_skills": ["preferred / bonus / nice-to-have skills"],
  "min_years_experience": number or null,
  "education_required": "minimum degree e.g. Bachelor's / Master's or null",
  "responsibilities": ["up to 6 short responsibility bullets"],
  "keywords": ["5-10 important domain keywords from the JD"]
}

JOB DESCRIPTION:
\"\"\"{text}\"\"\""""


class JobAgent:
    name = "Job Agent"
    description = "Parses a job description into must-have skills, nice-to-haves, experience and education requirements."

    def run(self, raw_text, api_key=None, model=None):
        errors = []
        if api_key:
            try:
                data = gemini_json(PROMPT.format(text=raw_text[:12000]), api_key, model, system=SYSTEM)
                req = {
                    "title": (data.get("title") or "Untitled Role").strip(),
                    "must_have_skills": normalize_skills(data.get("must_have_skills") or []),
                    "nice_to_have_skills": normalize_skills(data.get("nice_to_have_skills") or []),
                    "min_years_experience": data.get("min_years_experience"),
                    "education_required": data.get("education_required"),
                    "responsibilities": [str(r) for r in (data.get("responsibilities") or [])][:6],
                    "keywords": [str(k).lower() for k in (data.get("keywords") or [])][:10],
                }
                # remove nice-to-haves duplicated in must-haves
                must_names = {s["name"] for s in req["must_have_skills"]}
                req["nice_to_have_skills"] = [s for s in req["nice_to_have_skills"] if s["name"] not in must_names]
                if not req["must_have_skills"] and not req["nice_to_have_skills"]:
                    req = offline_extract.extract_job(raw_text)
                    req.setdefault("keywords", [])
                    return {"requirements": req, "engine": "offline", "errors": errors + ["LLM returned no skills; used heuristics"]}
                return {"requirements": req, "engine": "gemini", "errors": errors}
            except LLMError as e:
                errors.append(str(e))
        req = offline_extract.extract_job(raw_text)
        req["keywords"] = []
        return {"requirements": req, "engine": "offline", "errors": errors}
