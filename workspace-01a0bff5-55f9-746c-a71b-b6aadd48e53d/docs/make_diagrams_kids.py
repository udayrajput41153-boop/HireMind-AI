"""Kid-friendly diagrams for the simple PDF report. Light theme, big shapes."""
import math
from PIL import Image, ImageDraw, ImageFont

W = 1600
BG = (250, 251, 255)
INK = (31, 41, 55)
MUT = (107, 114, 128)
INDIGO = (99, 102, 241)
CYAN = (6, 182, 212)
EMERALD = (16, 185, 129)
AMBER = (245, 158, 11)
ROSE = (244, 63, 94)
VIOLET = (139, 92, 246)
WHITE = (255, 255, 255)


def F(size, bold=True):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans" + ("-Bold" if bold else "") + ".ttf", size)


def new(h):
    img = Image.new("RGB", (W, h), BG)
    return img, ImageDraw.Draw(img)


def tc(d, y, s, size, fill=INK):
    f = F(size)
    b = d.textbbox((0, 0), s, font=f)
    d.text(((W - (b[2] - b[0])) / 2, y), s, font=f, fill=fill)


def rbox(d, x, y, w, h, fill, border=None, r=24, bw=4):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=border, width=bw)


def txt(d, x, y, s, size, fill=INK, bold=True):
    d.text((x, y), s, font=F(size, bold), fill=fill)


def ctxt(d, cx, y, s, size, fill=INK, bold=True):
    f = F(size, bold)
    b = d.textbbox((0, 0), s, font=f)
    d.text((cx - (b[2] - b[0]) / 2, y), s, font=f, fill=fill)


def arrow(d, x1, y1, x2, y2, color=INK, w=6, size=18):
    d.line([x1, y1, x2, y2], fill=color, width=w)
    ang = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - size * math.cos(ang - 0.45), y2 - size * math.sin(ang - 0.45))
    p2 = (x2 - size * math.cos(ang + 0.45), y2 - size * math.sin(ang + 0.45))
    d.polygon([(x2, y2), p1, p2], fill=color)


def person(d, cx, cy, color):
    d.ellipse([cx - 45, cy - 95, cx + 45, cy - 5], fill=color)
    d.rounded_rectangle([cx - 70, cy, cx + 70, cy + 130], radius=40, fill=color)


def briefcase(d, cx, cy, color):
    d.rounded_rectangle([cx - 35, cy - 55, cx + 35, cy - 25], radius=10, fill=color)
    d.rounded_rectangle([cx - 90, cy - 30, cx + 90, cy + 90], radius=16, fill=color)
    d.rectangle([cx - 90, cy + 10, cx + 90, cy + 26], fill=WHITE)


# ============ D1: THE BIG IDEA ============
img, d = new(760)
tc(d, 30, "The Big Idea: match the right person to the right job!", 40)
tc(d, 95, "Like fitting puzzle pieces together — automatically, fairly, and in seconds.", 22, MUT)
rbox(d, 70, 190, 430, 420, WHITE, INDIGO)
person(d, 285, 300, INDIGO)
ctxt(d, 285, 450, "PERSON", 26, INDIGO)
ctxt(d, 285, 490, "skills: Python · SQL · Docker", 20, MUT)
rbox(d, 1100, 190, 430, 420, WHITE, CYAN)
briefcase(d, 1315, 300, CYAN)
ctxt(d, 1315, 450, "JOB", 26, CYAN)
ctxt(d, 1315, 490, "needs: Python · SQL · Docker", 20, MUT)
rbox(d, 620, 250, 360, 300, INDIGO, None, r=30)
ctxt(d, 800, 290, "HireMind AI", 34, WHITE)
ctxt(d, 800, 350, "5 helper bots", 24, (199, 210, 254))
ctxt(d, 800, 400, "read both sides &", 22, (199, 210, 254))
ctxt(d, 800, 435, "score the fit 0–100", 22, (199, 210, 254))
arrow(d, 500, 400, 612, 400, INDIGO)
arrow(d, 1100, 400, 988, 400, CYAN)
rbox(d, 560, 630, 480, 90, EMERALD, None, r=20)
ctxt(d, 800, 655, "★  Ranked list: best person first!", 26, WHITE)
arrow(d, 800, 552, 800, 622, EMERALD)
img.save("/home/user/docs/shots/k1_idea.png")

# ============ D2: THE 5 HELPER BOTS ============
img, d = new(700)
tc(d, 30, "Meet the Team: 5 Helper Bots (agents)", 40)
tc(d, 95, "Each bot does ONE job, then passes the work to the next — like a relay race.", 22, MUT)
bots = [
    ("1", "Reader Bot", "reads the resume\n& lists skills", INDIGO),
    ("2", "Job Bot", "reads the job ad\n& lists needs", CYAN),
    ("3", "Score Bot", "gives a fair\nscore 0–100", EMERALD),
    ("4", "Gap Bot", "finds missing\nskills", AMBER),
    ("5", "Writer Bot", "writes a summary\nfor the recruiter", ROSE),
]
x = 60
for i, (n, name, job, col) in enumerate(bots):
    rbox(d, x, 200, 260, 300, WHITE, col)
    d.ellipse([x + 100, 225, x + 160, 285], fill=col)
    ctxt(d, x + 130, 240, n, 30, WHITE)
    ctxt(d, x + 130, 305, name, 24, col)
    for j, line in enumerate(job.split("\n")):
        ctxt(d, x + 130, 350 + j * 32, line, 19, MUT)
    if i < 4:
        arrow(d, x + 268, 350, x + 300, 350, INK)
    x += 300
rbox(d, 380, 560, 840, 90, VIOLET, None, r=20)
ctxt(d, 800, 585, "Output: ranked candidates + reasons for every score!", 26, WHITE)
img.save("/home/user/docs/shots/k2_bots.png")

# ============ D3: SCORING PIE ============
img, d = new(760)
tc(d, 30, "How Score Bot grades — like a test with clear rules", 40)
cx, cy, r = 430, 430, 260
slices = [
    (45, "Must-have skills", INDIGO),
    (20, "Experience", EMERALD),
    (15, "Nice-to-have skills", CYAN),
    (10, "School / degree", AMBER),
    (10, "Bonus keywords", ROSE),
]
start = -90
for val, label, col in slices:
    ext = start + val * 3.6
    d.pieslice([cx - r, cy - r, cx + r, cy + r], start, ext, fill=col, outline=WHITE, width=4)
    mid = math.radians((start + ext) / 2)
    lx, ly = cx + (r * 0.62) * math.cos(mid), cy + (r * 0.62) * math.sin(mid)
    ctxt(d, lx, ly - 14, f"{val}", 30, WHITE)
    start = ext
lx0 = 800
txt(d, lx0, 200, "The score pie:", 28, INK)
y = 260
for val, label, col in slices:
    d.rounded_rectangle([lx0, y, lx0 + 46, y + 46], radius=10, fill=col)
    txt(d, lx0 + 66, y + 8, f"{label}  —  {val}% of the score", 24, INK)
    y += 76
txt(d, lx0, y + 20, "Same resume + same job =", 24, MUT)
txt(d, lx0, y + 56, "same score. ALWAYS. (fair!)", 26, EMERALD)
img.save("/home/user/docs/shots/k3_pie.png")

# ============ D4: EXAMPLE CHECKLIST (real verified data: Priya vs ML job) ============
img, d = new(760)
tc(d, 30, "Example: does Priya fit the Senior ML Engineer job?", 40)
rbox(d, 120, 170, 700, 520, WHITE, INDIGO)
ctxt(d, 470, 200, "Job must-haves", 28, INDIGO)
checks = [("Python", True), ("Machine Learning", True), ("SQL", True), ("Docker", False), ("PyTorch", False)]
y = 268
for skill, ok in checks:
    col = EMERALD if ok else ROSE
    d.rounded_rectangle([180, y, 250, y + 66], radius=14, fill=col)
    ctxt(d, 215, y + 12, "✓" if ok else "✗", 36, WHITE)
    txt(d, 280, y + 16, skill + ("  — she has it!" if ok else "  — missing!"), 26, INK)
    y += 84
ctxt(d, 470, y + 16, "(+2 more matched, not shown)", 18, MUT)

rbox(d, 900, 170, 580, 520, WHITE, EMERALD)
ctxt(d, 1190, 210, "Priya's score", 28, EMERALD)
ctxt(d, 1190, 290, "69", 110, AMBER)
ctxt(d, 1190, 440, "out of 100 = GOOD MATCH", 24, INK)
for i in range(5):
    sx = 1010 + i * 80
    ctxt(d, sx, 500, "★", 44, AMBER if i < 3 else (209, 213, 219))
ctxt(d, 1190, 590, "Gap Bot: learn Docker & PyTorch", 22, MUT)
ctxt(d, 1190, 625, "→ strong candidate in ~1 month!", 22, MUT)
img.save("/home/user/docs/shots/k4_example.png")

# ============ D5: TWO BRAINS (fair) ============
img, d = new(640)
tc(d, 30, "Why is it fair? Two brains, two jobs.", 40)
rbox(d, 120, 170, 560, 330, WHITE, VIOLET)
ctxt(d, 400, 210, "AI (Gemini)", 34, VIOLET)
ctxt(d, 400, 275, "READS messy text &", 24, MUT)
ctxt(d, 400, 315, "WRITES nice summaries", 24, MUT)
ctxt(d, 400, 380, "(like a helpful reader)", 20, MUT)
rbox(d, 920, 170, 560, 330, WHITE, EMERALD)
ctxt(d, 1200, 210, "MATH ENGINE", 34, EMERALD)
ctxt(d, 1200, 275, "DECIDES the score", 24, MUT)
ctxt(d, 1200, 315, "with fixed, public rules", 24, MUT)
ctxt(d, 1200, 380, "(never changes its mood)", 20, MUT)
arrow(d, 685, 335, 912, 335, INK)
ctxt(d, 800, 285, "clean facts", 20, MUT)
rbox(d, 360, 540, 880, 70, AMBER, None, r=16)
ctxt(d, 800, 558, "It never looks at names, photos, age or gender!", 24, WHITE)
img.save("/home/user/docs/shots/k5_fair.png")

# ============ D6: HOW TO USE THE APP (3 clicks) ============
img, d = new(680)
tc(d, 30, "Try it in 3 clicks!", 40)
steps = [
    ("1", "Click  Load Demo", "10 resumes + 3 jobs\nappear as neat cards", INDIGO),
    ("2", "Click  Run Pipeline", "the 5 bots read, score\n& write — watch them go!", EMERALD),
    ("3", "Click  a person", "see the WHY: scores,\ngreen/red skills, plan", ROSE),
]
x = 80
for i, (n, name, body, col) in enumerate(steps):
    rbox(d, x, 170, 440, 330, WHITE, col)
    d.ellipse([x + 180, 195, x + 260, 275], fill=col)
    ctxt(d, x + 220, 212, n, 40, WHITE)
    ctxt(d, x + 220, 300, name, 28, col)
    for j, line in enumerate(body.split("\n")):
        ctxt(d, x + 220, 355 + j * 34, line, 21, MUT)
    if i < 2:
        arrow(d, x + 448, 335, x + 492, 335, INK)
    x += 492
rbox(d, 330, 555, 940, 80, CYAN, None, r=18)
ctxt(d, 800, 577, "That's the whole demo — under 30 seconds!", 26, WHITE)
img.save("/home/user/docs/shots/k6_clicks.png")

# ============ D7: WHO IS HAPPY ============
img, d = new(640)
tc(d, 30, "Who wins? Everybody!", 40)
rbox(d, 100, 160, 660, 420, WHITE, INDIGO)
person(d, 430, 260, INDIGO)
ctxt(d, 430, 410, "THE RECRUITER", 26, INDIGO)
ctxt(d, 430, 455, "hours of reading → seconds", 20, MUT)
ctxt(d, 430, 490, "same rules for everyone", 20, MUT)
ctxt(d, 430, 525, "a reason for every score", 20, MUT)
rbox(d, 840, 160, 660, 420, WHITE, EMERALD)
person(d, 1170, 260, EMERALD)
ctxt(d, 1170, 410, "THE CANDIDATE", 26, EMERALD)
ctxt(d, 1170, 455, "knows exactly what to learn", 20, MUT)
ctxt(d, 1170, 490, "no hidden bias possible", 20, MUT)
ctxt(d, 1170, 525, "gets a fair, equal chance", 20, MUT)
img.save("/home/user/docs/shots/k7_happy.png")

print("kid diagrams saved (7)")
