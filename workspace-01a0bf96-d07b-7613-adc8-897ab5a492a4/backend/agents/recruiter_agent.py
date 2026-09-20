"""
AGENT 5 — Recruiter Agent
Writes the human-readable candidate summary a recruiter would send to a
hiring manager. Template-based offline; Gemini-quality prose when a key is set.
"""
from .llm import gemini_generate, LLMError

SYSTEM = "You are the Recruiter Agent in a multi-agent recruitment platform. You write crisp, honest recruiter summaries for hiring managers. Be specific, never invent facts, keep it to 3-4 sentences, plain text only (no markdown)."

PROMPT = """Write a recruiter summary for this candidate against this role.

ROLE: {job_title}
REQUIREMENTS: must-have: {must}; nice-to-have: {nice}; experience: {exp}; education: {edu}

CANDIDATE: {name}, {ctitle}, {yoe} years experience, education: {edudeg}. Skills: {skills}
MATCH: overall {score}/100 ({verdict}). Must-have coverage: {mm}/{mt}. Missing must-haves: {missing}.

Cover in 3-4 sentences: overall fit, key strengths, main gap(s) and risk, and a clear recommendation (interview / hold / pass). Plain text only."""


class RecruiterAgent:
    name = "Recruiter Agent"
    description = "Generates the recruiter-style candidate summary and hire recommendation."

    def _template(self, profile, requirements, match):
        name = profile.get("name", "Candidate")
        yoe = profile.get("years_experience")
        yoe_txt = f"{yoe:g} years of experience" if isinstance(yoe, (int, float)) else "experience level unknown"
        strengths = [m["found"] for m in match.get("must_matched", [])][:4]
        missing = match.get("must_missing") or []
        score, verdict = match["total"], match["verdict"]

        if score >= 80:
            rec = "Recommend moving to interview — strong alignment with the role."
        elif score >= 60:
            rec = "Recommend a screening call — solid fit with a few gaps to probe."
        elif score >= 40:
            rec = "Hold for now — partial fit; revisit if requirements relax."
        else:
            rec = "Pass for this role — limited overlap with core requirements."

        parts = [f"{name} is a {profile.get('title', 'professional').lower()} with {yoe_txt}, scoring {score}/100 ({verdict.lower()}) for {requirements.get('title', 'this role')}."]
        if strengths:
            parts.append(f"Key strengths: {', '.join(strengths)}.")
        if missing:
            parts.append(f"Main gaps: {', '.join(missing[:4])}.")
        else:
            parts.append("All must-have requirements are covered.")
        parts.append(rec)
        return " ".join(parts)

    def summarize(self, profile, requirements, match, api_key=None, model=None):
        if api_key:
            try:
                must = ", ".join(s["name"] for s in requirements.get("must_have_skills") or []) or "none listed"
                nice = ", ".join(s["name"] for s in requirements.get("nice_to_have_skills") or []) or "none listed"
                yoe = profile.get("years_experience")
                text = gemini_generate(
                    PROMPT.format(
                        job_title=requirements.get("title", "Role"),
                        must=must, nice=nice,
                        exp=requirements.get("min_years_experience") or "unspecified",
                        edu=requirements.get("education_required") or "unspecified",
                        name=profile.get("name", "Candidate"),
                        ctitle=profile.get("title", "professional"),
                        yoe=yoe if yoe is not None else "unknown",
                        edudeg=(profile.get("education") or {}).get("degree", "unknown"),
                        skills=", ".join(s["name"] for s in (profile.get("skills") or [])[:14]),
                        score=match["total"], verdict=match["verdict"],
                        mm=match["components"]["must_have"]["matched"], mt=match["components"]["must_have"]["total"],
                        missing=", ".join(match.get("must_missing") or []) or "none",
                    ),
                    api_key, model, system=SYSTEM, temperature=0.4,
                )
                return {"summary": text.strip(), "engine": "gemini"}
            except LLMError:
                pass
        return {"summary": self._template(profile, requirements, match), "engine": "offline"}
