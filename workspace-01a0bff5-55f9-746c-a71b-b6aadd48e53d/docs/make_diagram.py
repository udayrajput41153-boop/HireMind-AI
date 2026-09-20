"""Generate the architecture diagram for the documentation report."""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1720, 1010
bg = (11, 16, 32)
panel = (26, 35, 64)
panel2 = (21, 28, 51)
line = (99, 102, 241)
cyan = (34, 211, 238)
emerald = (16, 185, 129)
amber = (245, 158, 11)
text = (231, 236, 247)
muted = (139, 150, 181)

img = Image.new("RGB", (W, H), bg)
d = ImageDraw.Draw(img)


def F(size, bold=False):
    name = "/usr/share/fonts/truetype/dejavu/DejaVuSans" + ("-Bold" if bold else "") + ".ttf"
    try:
        return ImageFont.truetype(name, size)
    except OSError:
        return ImageFont.load_default()


def box(x, y, w, h, fill=panel, border=line, r=18, width=3):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=border, width=width)


def text_c(x, y, w, s, font, fill=text):
    b = d.textbbox((0, 0), s, font=font)
    d.text((x + (w - (b[2] - b[0])) / 2 - b[0], y), s, font=font, fill=fill)


def arrow(x1, y1, x2, y2, color=cyan, w=4, size=13):
    d.line([x1, y1, x2 - 6 * (x2 - x1) / max(1, math.hypot(x2 - x1, y2 - y1)), y2 - 6 * (y2 - y1) / max(1, math.hypot(x2 - x1, y2 - y1))], fill=color, width=w)
    ang = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - size * math.cos(ang - 0.45), y2 - size * math.sin(ang - 0.45))
    p2 = (x2 - size * math.cos(ang + 0.45), y2 - size * math.sin(ang + 0.45))
    d.polygon([(x2, y2), p1, p2], fill=color)


title_f, h_f, s_f, l_f = F(34, True), F(22, True), F(15), F(16)

text_c(0, 26, W, "HireMind AI — Multi-Agent Recruitment Pipeline", title_f)
text_c(0, 72, W, "LLM-powered extraction  ·  deterministic explainable matching", s_f, muted)

# Inputs (left)
box(40, 190, 300, 120, panel2, muted)
text_c(40, 212, 300, "10 Resumes", h_f)
text_c(40, 248, 300, ".txt / .pdf / .docx", s_f, muted)

box(40, 640, 300, 120, panel2, muted)
text_c(40, 662, 300, "3 Job Descriptions", h_f)
text_c(40, 698, 300, "pasted text / file", s_f, muted)

# Extraction agents (column 2)
ax, aw, ah = 460, 300, 140
box(ax, 180, aw, ah, panel, line)
text_c(ax, 198, aw, "① Resume Agent", h_f, cyan)
text_c(ax, 232, aw, "extract skills · experience", s_f)
text_c(ax, 256, aw, "education · candidate profile", s_f)
text_c(ax, 284, aw, "Gemini ▸ offline fallback", s_f, amber)

box(ax, 630, aw, ah, panel, line)
text_c(ax, 648, aw, "② Job Agent", h_f, cyan)
text_c(ax, 682, aw, "must-have vs nice-to-have", s_f)
text_c(ax, 706, aw, "min. experience · education", s_f)
text_c(ax, 734, aw, "Gemini ▸ offline fallback", s_f, amber)

# Matching agent (center)
mx, mw, mh = 870, 330, 190
box(mx, 380, mw, mh, panel, emerald, width=4)
text_c(mx, 400, mw, "③ Matching Agent", h_f, emerald)
text_c(mx, 434, mw, "deterministic weighted score", s_f)
text_c(mx, 460, mw, "must 45% · nice 15% · exp 20%", s_f, muted)
text_c(mx, 484, mw, "education 10% · keywords 10%", s_f, muted)
text_c(mx, 516, mw, "fuzzy skill matching + taxonomy", s_f, muted)

# Post agents (right column)
gx, gw, gh = 1310, 330, 150
box(gx, 190, gw, gh, panel, line)
text_c(gx, 210, gw, "④ Skill Gap Agent", h_f, amber)
text_c(gx, 244, gw, "critical vs stretch gaps", s_f)
text_c(gx, 268, gw, "adjacent strengths", s_f)
text_c(gx, 292, gw, "upskilling recommendations", s_f, muted)

box(gx, 610, gw, gh, panel, line)
text_c(gx, 630, gw, "⑤ Recruiter Agent", h_f, amber)
text_c(gx, 664, gw, "candidate summary", s_f)
text_c(gx, 688, gw, "interview / hold / pass", s_f)
text_c(gx, 712, gw, "Gemini ▸ template fallback", s_f, muted)

# Output (bottom center)
box(610, 830, 500, 100, (5, 46, 34), emerald, width=4)
text_c(610, 848, 500, "Ranked Candidate List", h_f, (110, 231, 183))
text_c(610, 882, 500, "score breakdown · gaps · summary · agent trace", s_f, (110, 231, 183))

# Arrows — clean left-to-right flow
arrow(340, 250, ax, 250)                       # resumes -> resume agent
arrow(340, 700, ax, 700)                       # jobs -> job agent
arrow(ax + aw, 260, mx + 40, 380)              # resume agent -> matching
arrow(ax + aw, 690, mx + 40, 570)              # job agent -> matching
arrow(mx + mw - 60, 380, gx + 60, 340)         # matching -> skill gap
arrow(mx + mw - 60, 570, gx + 60, 610)         # matching -> recruiter
arrow(gx + gw / 2, 340, 1080, 830)             # skill gap -> output
arrow(gx + gw / 2, 760, 1090, 830)             # recruiter -> output
arrow(mx + mw / 2, 570, 860, 830, emerald)     # matching -> output

# Legend (wrapped, bottom-left, outside output box)
d.text((44, 848), "◆ Extraction agents run on Google Gemini (API key) with a", font=l_f, fill=muted)
d.text((44, 874), "   deterministic offline NLP fallback — demo never breaks.", font=l_f, fill=muted)
d.text((44, 912), "◆ Matching Agent is deliberately deterministic: the LLM extracts,", font=l_f, fill=muted)
d.text((44, 938), "   but never decides the ranking → auditable & reproducible.", font=l_f, fill=muted)

img.save("/home/user/docs/architecture.png")
print("diagram saved")
