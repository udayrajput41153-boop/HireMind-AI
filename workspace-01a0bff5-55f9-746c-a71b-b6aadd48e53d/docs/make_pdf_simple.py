"""Simple, kid-friendly PDF project report for PS03 — v2: fixed image ratios,
page numbers, new diagrams, checked layout."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                Table, TableStyle, PageBreak, HRFlowable)
from reportlab.pdfbase import pdfmetrics
from PIL import Image as PILImage

styles = getSampleStyleSheet()
INDIGO = colors.HexColor("#4F46E5")
CYAN = colors.HexColor("#0891B2")
EMERALD = colors.HexColor("#059669")
AMBER = colors.HexColor("#D97706")
ROSE = colors.HexColor("#E11D48")
DARK = colors.HexColor("#1F2937")
GRAY = colors.HexColor("#6B7280")
LIGHT = colors.HexColor("#EEF2FF")
LIGHTG = colors.HexColor("#F9FAFB")

st_title = ParagraphStyle("ct", parent=styles["Title"], fontSize=30, textColor=INDIGO, spaceAfter=6)
st_sub = ParagraphStyle("cs", parent=styles["Normal"], fontSize=14, textColor=DARK, alignment=TA_CENTER)
st_h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontSize=17, textColor=INDIGO, spaceBefore=12, spaceAfter=6)
st_body = ParagraphStyle("body", parent=styles["Normal"], fontSize=11.5, leading=17, textColor=DARK, spaceAfter=8, alignment=TA_JUSTIFY)
st_bul = ParagraphStyle("bul", parent=st_body, leftIndent=16, bulletIndent=4, spaceAfter=5)
st_cap = ParagraphStyle("cap", parent=styles["Normal"], fontSize=9, textColor=GRAY, alignment=TA_CENTER, spaceBefore=4, spaceAfter=12)
st_code = ParagraphStyle("code", parent=styles["Code"], fontSize=7.5, leading=10, textColor=DARK, backColor=LIGHTG, borderPadding=6, spaceAfter=8)

story = []
B = lambda t: story.append(Paragraph(t, st_body))
BUL = lambda t: story.append(Paragraph("•  " + t, st_bul))
H1 = lambda t: (story.append(Paragraph(t, st_h1)), story.append(HRFlowable(width="100%", thickness=2, color=LIGHT, spaceAfter=8)))
CAP = lambda t: story.append(Paragraph(t, st_cap))


def IMG(path, w=6.7):
    """Insert image preserving true aspect ratio."""
    iw, ih = PILImage.open(path).size
    story.append(Image(path, width=w * inch, height=w * inch * ih / iw))


def table(rows, widths, header=True):
    data = []
    for i, r in enumerate(rows):
        data.append([Paragraph(str(c), ParagraphStyle("c", parent=styles["Normal"], fontSize=9.5,
                       textColor=(colors.white if (i == 0 and header) else DARK), bold=(i == 0 and header))) for c in r])
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INDIGO if header else LIGHT),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#C7D2FE")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHTG]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5)]))
    story.append(t)
    story.append(Spacer(1, 8))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRAY)
    canvas.drawString(0.7 * inch, 0.42 * inch, "HireMind AI · PS03 Project Report (simple edition)")
    canvas.drawRightString(A4[0] - 0.7 * inch, 0.42 * inch, f"page {doc.page}")
    canvas.setStrokeColor(LIGHT)
    canvas.line(0.7 * inch, 0.55 * inch, A4[0] - 0.7 * inch, 0.55 * inch)
    canvas.restoreState()


S = "/home/user/docs/shots/"

# ============ COVER ============
story.append(Spacer(1, 0.55 * inch))
story.append(Paragraph("HireMind AI", st_title))
story.append(Paragraph("The Robot Team that Matches People to Jobs", st_sub))
story.append(Paragraph("Project Report · Hackathon Problem PS03 · explained so simply a 10-year-old gets it",
                       ParagraphStyle("p", parent=st_sub, fontSize=11, textColor=CYAN)))
story.append(Spacer(1, 0.12 * inch))
IMG(S + "k1_idea.png")
CAP("A person's skills and a job's needs are like two puzzle pieces — HireMind AI measures how well they fit.")
table([
    ["Team", "[YOUR TEAM NAME] — [MEMBERS]"],
    ["Hackathon", "[HACKATHON NAME]"],
    ["Category", "NLP + LLM + Agentic AI"],
    ["Date", "20 Sept 2026"],
], [1.4 * inch, 5.1 * inch], header=False)
story.append(PageBreak())

# ============ CONTENTS ============
H1("What's inside")
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
    BUL(line)
IMG(S + "k2_bots.png")
CAP("The five agents, one after another — the heart of the whole project.")

story.append(PageBreak())

# ============ 1 PROBLEM ============
H1("1. The Problem (imagine this!)")
B("Imagine a teacher who must check <b>300 homework sheets in one night</b>. That is a recruiter: one job ad can bring hundreds of resumes, and they can look at each for only about <b>7 seconds</b>.")
B("So three bad things happen:")
BUL("Good people get missed just because they wrote a skill differently (\"React.js\" vs \"React\").")
BUL("Two recruiters can judge the same resume differently — not fair, not consistent.")
BUL("Nobody explains <i>why</i> someone was rejected.")
B("<b>Our mission:</b> build a computer team that reads every resume carefully, scores it with clear public rules, and always explains why.")

# ============ 2 SOLUTION ============
H1("2. Our Solution: 5 Helper Bots")
B("We built <b>HireMind AI</b>: five small programs called <b>agents</b> (think helper robots). Each does one job and passes the work on, like a relay race:")
BUL("<b>Reader Bot</b> reads a resume → tidy list of skills, years of practice, school.")
BUL("<b>Job Bot</b> reads the job ad → what the job MUST have vs what is extra-nice.")
BUL("<b>Score Bot</b> compares both lists → score 0–100 with fixed rules.")
BUL("<b>Gap Bot</b> finds missing skills → suggests what to learn next, like a game skill tree.")
BUL("<b>Writer Bot</b> writes a friendly summary for the recruiter.")
IMG(S + "k3_pie.png")
CAP("The score is a pie with fixed slices — everyone can see exactly how points are earned.")

story.append(PageBreak())

# ============ 4 EXAMPLE ============
H1("3. A Real Example from Our Demo")
B("We tested with 10 made-up resumes and 3 made-up job ads. Here is one real match, exactly as the bots computed it:")
IMG(S + "k4_example.png")
CAP("Priya has Python, ML and SQL but no Docker/PyTorch → 69/100 = Good match, plus a learning plan from Gap Bot.")
B("See the magic? A “no” becomes a <b>to-do list</b>: learn Docker and PyTorch, and she becomes a strong candidate.")

# ============ 5 FAIR ============
H1("4. Why It Is Fair and Trustworthy")
IMG(S + "k5_fair.png")
CAP("The AI reads and writes. The math decides. Nobody can argue with public, fixed rules.")
BUL("It <b>never looks</b> at names, photos, age or gender — only skills, practice and school.")
BUL("\"React.js\", \"ReactJS\" and \"React\" count as the <b>same skill</b> (dictionary of 130+ skills).")
BUL("Every score shows its <b>working</b>: ✓ matched skills, ✗ missing ones, points per slice.")
BUL("Even if the internet or the AI dies, the app still works — a built-in “no-AI” mode.")

story.append(PageBreak())

# ============ 6 CLICKS + HAPPY ============
H1("5. Try It in 3 Clicks — and Who Wins? Everybody!")
IMG(S + "k6_clicks.png")
CAP("The whole live demo takes under 30 seconds — perfect for judging.")
IMG(S + "k7_happy.png")
CAP("Recruiters save hours and stay fair; candidates get reasons and a learning path.")

# ============ 7 SCREENSHOTS ============
H1("6. The Real App (actual screenshots)")
B("Everything above is a real working website: a React screen in front, a Python brain behind.")
IMG(S + "01_resumes.png")
CAP("Reader Bot finished: 10 resumes turned into neat cards with skills, years and school.")

story.append(PageBreak())
IMG(S + "03_ranked.png")
CAP("Ranked list for “Senior ML Engineer”: best match on top, mini score bars on every card.")
IMG(S + "04_detail.png")
CAP("Click a person → the full WHY: green ✓ skills, red ✗ gaps, recruiter note, every bot's work.")

story.append(PageBreak())

# ============ 8 RESULTS ============
H1("7. Demo Results (10 resumes × 3 jobs)")
table([
    ["Job", "#1 (best)", "#2", "#3"],
    ["Senior ML Engineer", "Aarav — 95 Strong", "Priya — 69 Good", "Divya — 59 Partial"],
    ["Full-Stack Developer", "Sneha — 100 Strong", "Rohan — 81 Strong", "Vikram — 66 Good"],
    ["Data Analyst", "Karan — 80.7 Strong", "Priya — 78 Good", "Aarav — 46.7 Partial"],
], [1.7 * inch, 1.8 * inch, 1.5 * inch, 1.5 * inch])
B("Common sense wins: the ML person tops the ML job, the web person tops the web job, the analyst tops the analyst job. A brand-new graduate scores lower on the <i>senior</i> job because practice years count — just like real life.")

# ============ 9 TECH ============
H1("8. What We Built It With (tech stack)")
table([
    ["Part", "Tool", "In kid words"],
    ["Front screen", "React + Vite", "The colorful website you click"],
    ["Back brain", "Python + FastAPI", "The kitchen where bots cook"],
    ["AI reader/writer", "Google Gemini 2.5 Flash", "Smart helper for messy text (optional)"],
    ["No-AI mode", "Rules + skill dictionary", "Backup brain so the demo never breaks"],
    ["File readers", "pypdf · python-docx", "Opens PDF and Word resumes"],
], [1.4 * inch, 2.1 * inch, 3.0 * inch])
BUL("Folders: <b>backend/</b> the 5 bots · <b>frontend/</b> React screens · <b>data/</b> 10 resumes + 3 jobs · <b>docs/</b> report, slides, pictures.")

# ============ 10 NEXT/HONESTY ============
H1("9. What's Next & Honesty Box")
BUL("Next: save results in a database, compare jobs side-by-side, export PDF lists for recruiters.")
BUL("Honesty: demo data is 100% made-up (no real people). Gemini is used only when a key is added. An AI coding assistant helped us type faster — the team chose every rule and checked every result.")
BUL("Judges: the grown-up details (weights, API, references) are in the appendix.")

story.append(PageBreak())

# ============ APPENDIX ============
H1("Appendix — Technical Details (for judges)")
B("<b>Scoring weights:</b> must-have 45% · nice-to-have 15% · experience 20% · education 10% · keywords 10% (renormalised when a dimension is absent). Fuzzy skill match = alias dictionary + containment + difflib ratio ≥ 0.85. Verdicts: ≥80 Strong, 60–79 Good, 40–59 Partial, &lt;40 Weak. Deterministic ⇒ reproducible.")
IMG("/home/user/docs/architecture.png")
CAP("Full technical architecture: Gemini/offline extraction feeds deterministic Matching, Skill Gap and Recruiter agents.")
table([
    ["API", "What it does"],
    ["POST /api/resumes[/upload] · /api/jobs", "Register documents → Agents 1 & 2"],
    ["POST /api/demo/load", "Load the 10 + 3 demo dataset"],
    ["POST /api/match {job_id}", "Agents 3–5 → ranked list + traces"],
    ["POST /api/reextract", "Re-run extraction after adding a Gemini key"],
], [2.7 * inch, 3.8 * inch])
B("<b>References:</b> [1] Gemini API — ai.google.dev · [2] FastAPI — fastapi.tiangolo.com · [3] React — react.dev · [4] Vite — vite.dev · [5] python-docx / pypdf docs · [6] Python difflib · [7] Kaggle &amp; Hugging Face resume/JD datasets (surveyed; verify licenses before use).")
story.append(Paragraph("<b>Run it:</b> cd backend &amp;&amp; pip install -r requirements.txt &amp;&amp; uvicorn main:app --host 0.0.0.0 --port 8000 → open http://localhost:8000 → Load demo dataset → Run Matching Pipeline.", st_code))

doc = SimpleDocTemplate(
    "/home/user/docs/HireMind_AI_Report_Simple.pdf", pagesize=A4,
    title="HireMind AI — Simple Project Report", author="[YOUR TEAM NAME]",
    leftMargin=0.7 * inch, rightMargin=0.7 * inch, topMargin=0.65 * inch, bottomMargin=0.75 * inch,
)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("simple PDF v2 saved")
