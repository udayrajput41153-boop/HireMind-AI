"""Convert the simple kid-friendly report into an editable Word document."""
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
st = doc.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(11)

INDIGO = RGBColor(0x4F, 0x46, 0xE5)
CYAN = RGBColor(0x08, 0x91, 0xB2)
GRAY = RGBColor(0x6B, 0x72, 0x80)
S = "/home/user/docs/shots/"


def title(t, size=26, color=INDIGO, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6):
    p = doc.add_paragraph()
    p.alignment = align
    r = p.add_run(t)
    r.bold = True
    r.font.size = Pt(size)
    r.font.color.rgb = color
    p.paragraph_format.space_after = Pt(space_after)
    return p


def h1(t):
    p = doc.add_paragraph()
    r = p.add_run(t)
    r.bold = True
    r.font.size = Pt(16)
    r.font.color.rgb = INDIGO
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)


def body(t):
    p = doc.add_paragraph()
    p.add_run(t)
    p.paragraph_format.space_after = Pt(6)
    return p


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
    return t


# ---------- COVER ----------
doc.add_paragraph()
title("HireMind AI", 30, INDIGO, WD_ALIGN_PARAGRAPH.CENTER)
title("The Robot Team that Matches People to Jobs", 15, RGBColor(0x1F, 0x29, 0x37), WD_ALIGN_PARAGRAPH.CENTER)
title("Project Report · Hackathon Problem PS03 · explained so simply a 10-year-old gets it", 11, CYAN, WD_ALIGN_PARAGRAPH.CENTER, 12)
img(S + "k1_idea.png", 6.3)
cap("A person's skills and a job's needs are like two puzzle pieces — HireMind AI measures how well they fit.")
table([
    ["Team", "[YOUR TEAM NAME] — [MEMBERS]"],
    ["Hackathon", "[HACKATHON NAME]"],
    ["Category", "NLP + LLM + Agentic AI"],
    ["Date", "20 Sept 2026"],
])
doc.add_page_break()

# ---------- CONTENTS ----------
h1("What's inside")
for line in [
    "1. The Problem — imagine a teacher with 300 homework sheets",
    "2. Our Solution — 5 helper bots working like a relay race",
    "3. The Score Pie — grading with fixed, visible rules",
    "4. A Real Example — Priya vs the ML Engineer job",
    "5. Why It Is Fair — two brains: AI reads, math decides",
    "6. Try It in 3 Clicks + Who Wins? Everybody!",
    "7. The Real App — actual screenshots",
    "8. Demo Results — 10 resumes × 3 jobs, ranked",
    "9. Tech Stack, What's Next & Honesty Box",
    "Appendix — the grown-up technical details for judges",
]:
    bul(line)
img(S + "k2_bots.png")
cap("The five agents, one after another — the heart of the whole project.")
doc.add_page_break()

# ---------- 1 ----------
h1("1. The Problem (imagine this!)")
body("Imagine a teacher who must check 300 homework sheets in one night. That is a recruiter: one job ad can bring hundreds of resumes, and they can look at each for only about 7 seconds.")
body("So three bad things happen:")
bul("Good people get missed just because they wrote a skill differently (\"React.js\" vs \"React\").")
bul("Two recruiters can judge the same resume differently — not fair, not consistent.")
bul("Nobody explains why someone was rejected.")
body("Our mission: build a computer team that reads every resume carefully, scores it with clear public rules, and always explains why.")

# ---------- 2 ----------
h1("2. Our Solution: 5 Helper Bots")
body("We built HireMind AI: five small programs called agents (think helper robots). Each does one job and passes the work on, like a relay race:")
bul("Reader Bot reads a resume → tidy list of skills, years of practice, school.")
bul("Job Bot reads the job ad → what the job MUST have vs what is extra-nice.")
bul("Score Bot compares both lists → score 0–100 with fixed rules.")
bul("Gap Bot finds missing skills → suggests what to learn next, like a game skill tree.")
bul("Writer Bot writes a friendly summary for the recruiter.")
img(S + "k3_pie.png")
cap("The score is a pie with fixed slices — everyone can see exactly how points are earned.")
doc.add_page_break()

# ---------- 3 ----------
h1("3. A Real Example from Our Demo")
body("We tested with 10 made-up resumes and 3 made-up job ads. Here is one real match, exactly as the bots computed it:")
img(S + "k4_example.png")
cap("Priya has Python, ML and SQL but no Docker/PyTorch → 69/100 = Good match, plus a learning plan from Gap Bot.")
body("See the magic? A “no” becomes a to-do list: learn Docker and PyTorch, and she becomes a strong candidate.")

# ---------- 4 ----------
h1("4. Why It Is Fair and Trustworthy")
img(S + "k5_fair.png")
cap("The AI reads and writes. The math decides. Nobody can argue with public, fixed rules.")
bul("It never looks at names, photos, age or gender — only skills, practice and school.")
bul("\"React.js\", \"ReactJS\" and \"React\" count as the same skill (dictionary of 130+ skills).")
bul("Every score shows its working: ✓ matched skills, ✗ missing ones, points per slice.")
bul("Even if the internet or the AI dies, the app still works — a built-in “no-AI” mode.")
doc.add_page_break()

# ---------- 5 ----------
h1("5. Try It in 3 Clicks — and Who Wins? Everybody!")
img(S + "k6_clicks.png")
cap("The whole live demo takes under 30 seconds — perfect for judging.")
img(S + "k7_happy.png")
cap("Recruiters save hours and stay fair; candidates get reasons and a learning path.")

# ---------- 6 ----------
h1("6. The Real App (actual screenshots)")
body("Everything above is a real working website: a React screen in front, a Python brain behind.")
img(S + "01_resumes.png")
cap("Reader Bot finished: 10 resumes turned into neat cards with skills, years and school.")
doc.add_page_break()
img(S + "03_ranked.png")
cap("Ranked list for “Senior ML Engineer”: best match on top, mini score bars on every card.")
img(S + "04_detail.png")
cap("Click a person → the full WHY: green ✓ skills, red ✗ gaps, recruiter note, every bot's work.")
doc.add_page_break()

# ---------- 7 ----------
h1("7. Demo Results (10 resumes × 3 jobs)")
table([
    ["Job", "#1 (best)", "#2", "#3"],
    ["Senior ML Engineer", "Aarav — 95 Strong", "Priya — 69 Good", "Divya — 59 Partial"],
    ["Full-Stack Developer", "Sneha — 100 Strong", "Rohan — 81 Strong", "Vikram — 66 Good"],
    ["Data Analyst", "Karan — 80.7 Strong", "Priya — 78 Good", "Aarav — 46.7 Partial"],
])
body("Common sense wins: the ML person tops the ML job, the web person tops the web job, the analyst tops the analyst job. A brand-new graduate scores lower on the senior job because practice years count — just like real life.")

# ---------- 8 ----------
h1("8. What We Built It With (tech stack)")
table([
    ["Part", "Tool", "In kid words"],
    ["Front screen", "React + Vite", "The colorful website you click"],
    ["Back brain", "Python + FastAPI", "The kitchen where bots cook"],
    ["AI reader/writer", "Google Gemini 2.5 Flash", "Smart helper for messy text (optional)"],
    ["No-AI mode", "Rules + skill dictionary", "Backup brain so the demo never breaks"],
    ["File readers", "pypdf · python-docx", "Opens PDF and Word resumes"],
])
bul("Folders: backend/ the 5 bots · frontend/ React screens · data/ 10 resumes + 3 jobs · docs/ report, slides, pictures.")

# ---------- 9 ----------
h1("9. What's Next & Honesty Box")
bul("Next: save results in a database, compare jobs side-by-side, export PDF lists for recruiters.")
bul("Honesty: demo data is 100% made-up (no real people). Gemini is used only when a key is added. An AI coding assistant helped us type faster — the team chose every rule and checked every result.")
bul("Judges: the grown-up details (weights, API, references) are in the appendix.")
doc.add_page_break()

# ---------- APPENDIX ----------
h1("Appendix — Technical Details (for judges)")
body("Scoring weights: must-have 45% · nice-to-have 15% · experience 20% · education 10% · keywords 10% (renormalised when a dimension is absent). Fuzzy skill match = alias dictionary + containment + difflib ratio ≥ 0.85. Verdicts: ≥80 Strong, 60–79 Good, 40–59 Partial, <40 Weak. Deterministic ⇒ reproducible.")
img("/home/user/docs/architecture.png", 6.4)
cap("Full technical architecture: Gemini/offline extraction feeds deterministic Matching, Skill Gap and Recruiter agents.")
table([
    ["API", "What it does"],
    ["POST /api/resumes[/upload] · /api/jobs", "Register documents → Agents 1 & 2"],
    ["POST /api/demo/load", "Load the 10 + 3 demo dataset"],
    ["POST /api/match {job_id}", "Agents 3–5 → ranked list + traces"],
    ["POST /api/reextract", "Re-run extraction after adding a Gemini key"],
])
body("References: [1] Gemini API — ai.google.dev · [2] FastAPI — fastapi.tiangolo.com · [3] React — react.dev · [4] Vite — vite.dev · [5] python-docx / pypdf docs · [6] Python difflib · [7] Kaggle & Hugging Face resume/JD datasets (surveyed; verify licenses before use).")
p = doc.add_paragraph()
r = p.add_run("Run it: cd backend && pip install -r requirements.txt && uvicorn main:app --host 0.0.0.0 --port 8000 → open http://localhost:8000 → Load demo dataset → Run Matching Pipeline.")
r.font.name = "Consolas"
r.font.size = Pt(9)

doc.save("/home/user/docs/HireMind_AI_Report_Simple.docx")
print("simple DOCX saved")
