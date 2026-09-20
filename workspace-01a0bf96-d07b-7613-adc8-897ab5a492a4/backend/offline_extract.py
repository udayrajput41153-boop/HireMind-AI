"""
Offline (no-LLM) extraction heuristics used as a fallback by the
Resume Agent and Job Agent. Regex + taxonomy scanning. Deterministic.
"""
import re
from skills_taxonomy import all_terms, canonicalize, category_of

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(r"(?:\+?\d{1,3}[\s-]?)?(?:\(\d{2,4}\)[\s-]?)?\d{3,4}[\s-]?\d{4,6}")
YEARS_EXP_RE = re.compile(
    r"(\d{1,2}(?:\.\d)?)\s*\+?\s*(?:years?|yrs?)\s*(?:\+\s*)?(?:of\s+)?(?:overall\s+|total\s+|professional\s+|relevant\s+)?(?:experience|exp\b|work\s+experience)?",
    re.IGNORECASE,
)
MIN_EXP_RE = re.compile(r"(\d{1,2})\s*\+?\s*(?:to\s*\d{1,2}\s*)?(?:years?|yrs?)\s*(?:\+\s*)?(?:of\s+)?(?:experience)?", re.IGNORECASE)

EDU_LEVELS = [
    ("phd", 5), ("doctorate", 5), ("ph.d", 5),
    ("m.tech", 4), ("mtech", 4), ("m.tech", 4), ("master of technology", 4),
    ("m.s.", 4), ("m.sc", 4), ("msc", 4), ("master of science", 4), ("masters", 4), ("master's", 4), ("postgraduat", 4), ("pgdm", 4),
    ("mba", 3.5),
    ("b.tech", 3), ("btech", 3), ("bachelor of technology", 3),
    ("b.e", 3), ("bachelor of engineering", 3), ("bca", 3), ("b.sc", 3), ("bsc", 3),
    ("bachelor", 3), ("b.a", 3), ("b.com", 3), ("bba", 3), ("undergraduat", 3),
    ("diploma", 1.5),
]

ROLE_KEYWORDS = [
    "machine learning engineer", "ml engineer", "ai engineer", "data scientist",
    "data analyst", "data engineer", "full stack", "full-stack", "fullstack",
    "front end", "front-end", "frontend", "back end", "back-end", "backend",
    "software engineer", "software developer", "devops", "sre", "site reliability",
    "qa engineer", "test engineer", "android developer", "ios developer",
    "mobile developer", "product manager", "cloud engineer", "solution architect",
    "web developer", "researcher", "intern",
]

SECTION_SPLIT = re.compile(r"^\s*(?:#{1,3}\s*)?(summary|professional summary|objective|skills|technical skills|core competencies|work experience|professional experience|experience|employment|employment history|education|academic|academics|projects|certifications|certificates|achievements|awards|languages|interests)\s*:?\s*$", re.IGNORECASE | re.MULTILINE)

NICE_SECTION_RE = re.compile(r"(nice\s*to\s*have|preferred|bonus|good\s*to\s*have|plus|desirable|optional)", re.IGNORECASE)
MUST_SECTION_RE = re.compile(r"(must\s*have|required|requirements|mandatory|essential|you\s*will\s*need|what\s*you.?ll\s*need|qualifications)", re.IGNORECASE)


def _scan_skills(text):
    """Find known skills in text via alias substring scan. Returns list of canonical names."""
    low = " " + text.lower().replace("\u2022", " ").replace("•", " ") + " "
    low = re.sub(r"[/,|;]", " ", low)
    found = {}
    for term, canon in all_terms().items():
        # word-boundary match so e.g. "java" doesn't fire inside "javascript"
        pattern = r"(?<![a-z0-9+#.])" + re.escape(term) + r"(?![a-z0-9+#])"
        if re.search(pattern, low):
            if canon not in found:
                found[canon] = len(term)  # prefer longest alias match
    # dedupe canonical
    return sorted(found.keys())


def _detect_name(text):
    for line in text.splitlines()[:6]:
        line = line.strip().strip("-•·").strip()
        if not line or "@" in line or any(c.isdigit() for c in line):
            continue
        if re.match(r"(?i)^(resume|curriculum|cv|profile)\b", line):
            continue
        words = line.split()
        if 2 <= len(words) <= 4 and all(w.isalpha() or w[0] == "." for w in words):
            return line.title()
    return "Unknown Candidate"


def _detect_title(text):
    low = text.lower()
    for kw in ROLE_KEYWORDS:
        if kw in low:
            return kw.title().replace("Front End", "Frontend").replace("Back End", "Backend").replace("Full Stack", "Full-Stack")
    return "Professional"


def _detect_experience_years(text):
    vals = []
    for m in YEARS_EXP_RE.finditer(text):
        v = float(m.group(1))
        if 0 <= v <= 45:
            vals.append(v)
    # Prefer statements explicitly about "experience"
    explicit = []
    for m in re.finditer(r"(\d{1,2}(?:\.\d)?)\s*\+?\s*(?:years?|yrs?)\s*(?:\+\s*)?of\s+.*?experience", text, re.IGNORECASE):
        explicit.append(float(m.group(1)))
    if explicit:
        return max(explicit)
    return max(vals) if vals else None


def _detect_education(text):
    low = text.lower()
    best_label, best_rank = None, 0
    for kw, rank in EDU_LEVELS:
        if kw in low and rank > best_rank:
            best_label, best_rank = kw, rank
    return {"degree": best_label.upper() if best_label else "Unknown", "rank": best_rank}


def extract_resume(text):
    name = _detect_name(text)
    skills = _scan_skills(text)
    edu = _detect_education(text)
    email_m = EMAIL_RE.search(text)
    phone_m = PHONE_RE.search(text.replace("\n", " "))
    return {
        "name": name,
        "title": _detect_title(text),
        "email": email_m.group(0) if email_m else None,
        "phone": phone_m.group(0).strip() if phone_m else None,
        "skills": [{"name": s, "category": category_of(s)} for s in skills],
        "years_experience": _detect_experience_years(text),
        "education": edu,
        "raw_length": len(text),
    }


def _split_skills_list(block):
    items = re.split(r"[•,;|\n]", block)
    out = []
    for it in items:
        it = it.strip(" -–\t.")
        if 1 < len(it) < 60 and not it.endswith(":"):
            out.append(it)
    return out


def extract_job(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    title = lines[0].strip("#").strip() if lines else "Untitled Role"
    if len(title) > 90:
        title = title[:90] + "…"

    # Experience requirement
    m = MIN_EXP_RE.search(text)
    min_years = int(m.group(1)) if m else None

    edu = _detect_education(text)
    # JDs: education mentioned as requirement; if nothing found mark unknown
    if edu["degree"] == "Unknown":
        edu_req = None
    else:
        edu_req = edu["degree"]

    # Split text into "must" region and "nice" region
    nice_start = NICE_SECTION_RE.search(text)
    must_region = text[: nice_start.start()] if nice_start else text
    nice_region = text[nice_start.start():] if nice_start else ""

    must_skills = _scan_skills(must_region)
    nice_skills = [s for s in _scan_skills(nice_region) if s not in must_skills]

    # If no section split worked, treat common soft framing: keep all as must
    if not nice_start:
        nice_skills = []

    # Responsibilities: naive - take bullet lines mentioning verbs
    resp = []
    for l in lines:
        if re.match(r"^\s*(?:[-•*]|\d+\.)\s+", l) and re.search(r"(design|develop|build|own|lead|collaborate|work|analyze|analyse|deploy|maintain|create|implement|drive|partner|mentor|write|optimize|optimise)", l, re.IGNORECASE):
            resp.append(re.sub(r"^\s*(?:[-•*]|\d+\.)\s+", "", l))
    return {
        "title": title,
        "must_have_skills": [{"name": s, "category": category_of(s)} for s in must_skills],
        "nice_to_have_skills": [{"name": s, "category": category_of(s)} for s in nice_skills],
        "min_years_experience": min_years,
        "education_required": edu_req,
        "responsibilities": resp[:8],
        "raw_length": len(text),
    }
