"""
AGENT 3 — Matching Agent (deterministic core)
Scores candidate ↔ job compatibility from 0-100 with a fully explainable
per-dimension breakdown. Deterministic by design so results are auditable.

Weights (renormalized when a dimension is not applicable):
  must-have skills 45% · nice-to-have skills 15% · experience 20% · education 10% · keyword affinity 10%
"""
import difflib
import re

WEIGHTS = {"must": 0.45, "nice": 0.15, "experience": 0.20, "education": 0.10, "keywords": 0.10}

EDU_RANK = [
    ("phd", 5), ("doctorate", 5),
    ("master", 4), ("m.tech", 4), ("mtech", 4), ("m.sc", 4), ("msc", 4), ("m.s", 4), ("postgraduat", 4), ("pgdm", 4),
    ("mba", 3.5),
    ("bachelor", 3), ("b.tech", 3), ("btech", 3), ("b.e", 3), ("undergraduat", 3), ("bca", 3), ("b.sc", 3), ("b.com", 3), ("bba", 3),
    ("diploma", 1.5),
]


def edu_rank(label):
    if not label:
        return None
    low = str(label).lower()
    for kw, rank in EDU_RANK:
        if kw in low:
            return rank
    return None


def skill_match(a, b):
    """Fuzzy equality between two skill names (both may already be canonical)."""
    if not a or not b:
        return False
    a, b = a.lower().strip(), b.lower().strip()
    if a == b:
        return True
    if a in b or b in a:
        return True
    return difflib.SequenceMatcher(None, a, b).ratio() >= 0.85


def find_matches(required, candidate_skills):
    """Return (matched_reqs, missing_reqs, matched_candidate_names)."""
    cand_names = [s["name"] if isinstance(s, dict) else s for s in candidate_skills]
    matched, missing = [], []
    used = set()
    for req in required:
        req_name = req["name"] if isinstance(req, dict) else req
        hit = None
        for i, cn in enumerate(cand_names):
            if i not in used and skill_match(req_name, cn):
                hit = cn
                used.add(i)
                break
        if hit:
            matched.append({"required": req_name, "found": hit})
        else:
            missing.append(req_name)
    return matched, missing


class MatchingAgent:
    name = "Matching Agent"
    description = "Deterministic weighted scoring (skills, experience, education, keywords) producing a 0-100 fit score."

    def score(self, profile, requirements, raw_resume_text=""):
        cand_skills = profile.get("skills") or []
        must = requirements.get("must_have_skills") or []
        nice = requirements.get("nice_to_have_skills") or []

        must_matched, must_missing = find_matches(must, cand_skills)
        nice_matched, nice_missing = find_matches(nice, cand_skills)

        # ---- dimension scores (each 0..1) ----
        dims = {}
        must_score = (len(must_matched) / len(must)) if must else None
        nice_score = (len(nice_matched) / len(nice)) if nice else None
        dims["must"] = must_score
        dims["nice"] = nice_score

        # experience
        min_y = requirements.get("min_years_experience")
        cand_y = profile.get("years_experience")
        if min_y is None:
            exp_score, exp_note = 0.75, "No experience requirement stated"
        elif cand_y is None:
            exp_score, exp_note = 0.5, "Candidate experience unknown"
        elif cand_y >= min_y:
            exp_score = 1.0
            exp_note = f"{cand_y:g} yrs ≥ {min_y:g} yrs required"
        else:
            exp_score = 0.6 * (cand_y / min_y)
            exp_note = f"{cand_y:g} yrs < {min_y:g} yrs required"
        dims["experience"] = exp_score

        # education
        req_edu = edu_rank(requirements.get("education_required"))
        cand_edu = edu_rank((profile.get("education") or {}).get("degree"))
        if req_edu is None:
            edu_score, edu_note = 0.8, "No education requirement stated"
        elif cand_edu is None:
            edu_score, edu_note = 0.5, "Candidate education unknown"
        elif cand_edu >= req_edu:
            edu_score, edu_note = 1.0, "Meets education requirement"
        else:
            edu_score, edu_note = 0.4, "Below required education level"
        dims["education"] = edu_score

        # keyword affinity: JD keywords/titles found in raw resume text
        keywords = set(requirements.get("keywords") or [])
        keywords |= {re.sub(r"\..*", "", s["name"].lower()) for s in must[:6]}
        hay = raw_resume_text.lower()
        hits = [k for k in keywords if k and k.lower() in hay]
        kw_score = min(1.0, len(hits) / max(3, len(keywords) * 0.6)) if keywords else 0.7
        dims["keywords"] = kw_score

        # ---- weighted total with weight renormalization ----
        active = {k: v for k, v in dims.items() if v is not None}
        if must_score is None and nice_score is not None:
            active["nice"] = nice_score
        wsum = sum(WEIGHTS[k] for k in active)
        total = 100.0 * sum(WEIGHTS[k] * active[k] for k in active) / (wsum or 1)

        if total >= 80:
            verdict = "Strong match"
        elif total >= 60:
            verdict = "Good match"
        elif total >= 40:
            verdict = "Partial match"
        else:
            verdict = "Weak match"

        return {
            "total": round(total, 1),
            "verdict": verdict,
            "components": {
                "must_have": {"score": round((must_score if must_score is not None else 0) * 100), "weight": int(WEIGHTS["must"] * 100), "matched": len(must_matched), "total": len(must)},
                "nice_to_have": {"score": round((nice_score if nice_score is not None else 0) * 100), "weight": int(WEIGHTS["nice"] * 100), "matched": len(nice_matched), "total": len(nice)},
                "experience": {"score": round(exp_score * 100), "weight": int(WEIGHTS["experience"] * 100), "note": exp_note,
                               "candidate_years": cand_y, "required_years": min_y},
                "education": {"score": round(edu_score * 100), "weight": int(WEIGHTS["education"] * 100), "note": edu_note,
                              "candidate_degree": (profile.get("education") or {}).get("degree"), "required": requirements.get("education_required")},
                "keywords": {"score": round(kw_score * 100), "weight": int(WEIGHTS["keywords"] * 100), "hits": hits[:8]},
            },
            "must_matched": must_matched, "must_missing": must_missing,
            "nice_matched": nice_matched, "nice_missing": nice_missing,
        }
