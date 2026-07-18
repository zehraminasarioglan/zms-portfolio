#!/usr/bin/env python3
"""
Portfolio PDF Generator — Zehra Mina Sarıoğlan
5 A3 landscape spreads (A3 = 420×297 mm, each half = A4 portrait)

Spread 1 — Exterior Covers:  Back Cover (L)  |  Front Cover (R)
Spread 2 — Interior Covers:  Inside Front (L) |  Inside Back (R)
Spread 3 — Introduction:     Visual/Label (L) |  Cover Letter (R)
Spread 4 — CV:               Left Column (L)  |  Right Column (R)
Spread 5 — Work Page:        Project Info (L) |  Project Image (R)
"""

import os, math
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

BASE   = '/Users/zeynebsarioglan/Desktop/All/Zehra/'
OUTPUT = BASE + 'ZehraMina_Portfolio.pdf'

# ── Colour system (from website) ──────────────────────────────────────────────
BG       = HexColor('#080808')
SURFACE  = HexColor('#111111')
SURFACE2 = HexColor('#1a1a1a')
ACCENT   = HexColor('#B8E01A')
ACCENT_D = HexColor('#96B915')        # darker accent for variety
TEXT     = HexColor('#F0F0F0')
MUTED    = HexColor('#888888')
BORDER   = HexColor('#222222')
WHITE    = HexColor('#ffffff')
BLACK    = HexColor('#000000')

# Semi-transparent helpers
def rgba(hex_str, a):
    c = HexColor(hex_str)
    return Color(c.red, c.green, c.blue, alpha=a)

ACCENT_LOW  = rgba('#B8E01A', 0.10)
ACCENT_MID  = rgba('#B8E01A', 0.25)
WHITE_LOW   = rgba('#ffffff', 0.06)
WHITE_FAINT = rgba('#ffffff', 0.03)

# ── Geometry ──────────────────────────────────────────────────────────────────
PW, PH = landscape(A3)   # 1190.55 × 841.89 pt  (420 × 297 mm)
HW     = PW / 2          # 595.28 pt = A4 width = 210 mm
M      = 14 * mm         # page margin
M2     = 10 * mm         # tighter inner margin

# ── Font registration ─────────────────────────────────────────────────────────
def register_fonts():
    for name, fname in [
        ('DM',      'DMSans-Regular.ttf'),
        ('DM-L',    'DMSans-Light.ttf'),
        ('DM-M',    'DMSans-Medium.ttf'),
        ('DM-B',    'DMSans-Bold.ttf'),
    ]:
        pdfmetrics.registerFont(TTFont(name, BASE + fname))

# ── Drawing primitives ────────────────────────────────────────────────────────
def rect(c, x, y, w, h, fill=None, stroke=None, sw=0.5):
    if fill:    c.setFillColor(fill)
    if stroke:  c.setStrokeColor(stroke); c.setLineWidth(sw)
    c.rect(x, y, w, h,
           stroke=1 if stroke else 0,
           fill=1   if fill   else 0)

def rule(c, x, y, w, h=0.75, color=ACCENT):
    c.setFillColor(color)
    c.rect(x, y, w, h, stroke=0, fill=1)

def label(c, txt, x, y, font='DM', size=8, color=MUTED, align='left'):
    c.setFont(font, size)
    c.setFillColor(color)
    if   align == 'center': c.drawCentredString(x, y, txt)
    elif align == 'right':  c.drawRightString(x, y, txt)
    else:                   c.drawString(x, y, txt)

def dot_grid(c, x, y, w, h, step=13*mm, r=0.55, alpha=0.055):
    c.saveState()
    c.setFillColor(Color(1, 1, 1, alpha=alpha))
    ix = int(w / step) + 2
    iy = int(h / step) + 2
    for i in range(ix):
        for j in range(iy):
            px = x + i * step
            py = y + j * step
            if x - 1 <= px <= x + w + 1 and y - 1 <= py <= y + h + 1:
                c.circle(px, py, r, stroke=0, fill=1)
    c.restoreState()

def wrap_text(c, text, x, y, font, size, color, max_w, leading=None):
    """Word-wrap text; return y after last line."""
    if leading is None:
        leading = size * 1.55
    c.setFont(font, size)
    c.setFillColor(color)
    words  = text.split()
    line   = ''
    for w in words:
        test = (line + ' ' + w).strip()
        if c.stringWidth(test, font, size) <= max_w:
            line = test
        else:
            if line:
                c.drawString(x, y, line)
                y -= leading
            line = w
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y

def section_header(c, title, x, y, width):
    """Accent-coloured section label with rule below."""
    label(c, title.upper(), x, y, 'DM-B', 7, ACCENT)
    rule(c, x, y - 3*mm, width, 0.5, rgba('#B8E01A', 0.4))
    return y - 6*mm

# ── SPREAD 1 ─  EXTERIOR COVERS  ─────────────────────────────────────────────
# Left = Back Cover   |   Right = Front Cover

def spread1(c):

    # ── BACK COVER (left half) ────────────────────────────────────────────────
    x0 = 0
    rect(c, x0, 0, HW, PH, fill=BG)
    dot_grid(c, x0, 0, HW, PH)

    # Large ghost monogram
    c.saveState()
    c.setFillColor(Color(0.722, 0.878, 0.102, alpha=0.07))
    c.setFont('DM-B', 230)
    c.drawCentredString(x0 + HW/2, PH/2 - 75, 'ZMS')
    c.restoreState()

    # Top rule + label
    rule(c, x0 + M, PH - M - 1.5*mm, HW - 2*M)
    label(c, 'GRAPHIC DESIGN PORTFOLIO', x0 + HW/2, PH - M - 8*mm,
          'DM-M', 7, MUTED, 'center')

    # Contact block
    cy = PH/2 + 22*mm
    label(c, 'Zehra Mina Sarıoğlan', x0 + HW/2, cy, 'DM-B', 13, TEXT, 'center')
    rule(c, x0 + HW/2 - 22*mm, cy - 5*mm, 44*mm, 1.0)

    contacts = [
        ('zehraminasarioglan@gmail.com',      9, MUTED),
        ('0553 456 1230',                      9, MUTED),
        ('in/zehraminasarioglan',              9, MUTED),
        ('zms-portfolio.onrender.com',         9, ACCENT),
        ('Ankara, Türkiye',                    9, MUTED),
    ]
    iy = cy - 12*mm
    for txt, sz, col in contacts:
        label(c, txt, x0 + HW/2, iy, 'DM', sz, col, 'center')
        iy -= 5.5*mm

    # Bottom rule + year
    rule(c, x0 + M, 13*mm, HW - 2*M)
    label(c, '© 2025 — Bilkent University  GRA 401',
          x0 + HW/2, 7.5*mm, 'DM-L', 7, MUTED, 'center')

    # Spine line
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.75)
    c.line(HW, 0, HW, PH)

    # ── FRONT COVER (right half) ──────────────────────────────────────────────
    x1 = HW
    rect(c, x1, 0, HW, PH, fill=BG)
    dot_grid(c, x1, 0, HW, PH)

    # Left accent stripe
    rect(c, x1, 0, 5*mm, PH, fill=ACCENT)

    # Top label
    label(c, 'GRA 401  —  PORTFOLIO', x1 + HW/2, PH - M - 8*mm,
          'DM-M', 7, MUTED, 'center')
    rule(c, x1 + M + 5*mm, PH - M - 12*mm, HW - 2*M - 5*mm, 0.5,
         rgba('#888888', 0.3))

    # Name block — vertically centred, left-padded
    nx = x1 + 14*mm
    ny = PH/2 + 42*mm

    c.setFillColor(TEXT)
    c.setFont('DM-B', 54)
    c.drawString(nx, ny, 'ZEHRA MINA')

    c.setFillColor(ACCENT)
    c.setFont('DM-B', 54)
    c.drawString(nx, ny - 60, 'SARIOĞLAN')

    rule(c, nx, ny - 74, 78*mm, 2.0)

    c.setFont('DM-L', 13)
    c.setFillColor(MUTED)
    c.drawString(nx, ny - 90, 'Graphic Design Portfolio')

    # Decorative accent rectangle (bottom-right corner)
    rect(c, x1 + HW - 30*mm, 0, 30*mm, 4*mm, fill=ACCENT)
    rect(c, x1 + HW - 4*mm, 0, 4*mm, 30*mm, fill=SURFACE2)

    # Bottom info row
    label(c, 'Bilkent University', x1 + 14*mm, 10*mm, 'DM', 8, MUTED)
    label(c, '2025', x1 + HW - M, 10*mm, 'DM-M', 8, ACCENT, 'right')


# ── SPREAD 2 ─  INTERIOR COVERS  ─────────────────────────────────────────────
# Left = Inside Front Cover   |   Right = Inside Back Cover

def spread2(c):

    # ── INSIDE FRONT COVER ───────────────────────────────────────────────────
    x0 = 0
    rect(c, x0, 0, HW, PH, fill=SURFACE)
    dot_grid(c, x0, 0, HW, PH, step=11*mm, alpha=0.04)

    # Large accent circle (centred, ghost)
    cx, cy_c = x0 + HW/2, PH/2
    c.saveState()
    c.setFillColor(Color(0.722, 0.878, 0.102, alpha=0.06))
    c.circle(cx, cy_c, 120*mm, stroke=0, fill=1)
    c.restoreState()

    # Thin concentric ring
    c.saveState()
    c.setStrokeColor(Color(0.722, 0.878, 0.102, alpha=0.18))
    c.setLineWidth(0.75)
    c.circle(cx, cy_c, 130*mm, stroke=1, fill=0)
    c.restoreState()

    # Centred statement
    label(c, '"Design is the art of', cx, cy_c + 14*mm, 'DM-L', 12, TEXT,   'center')
    label(c, 'making ideas visible."',  cx, cy_c - 2*mm,  'DM-L', 12, TEXT,   'center')
    rule(c, cx - 25*mm, cy_c - 10*mm, 50*mm, 1.0)

    # Corner accent squares
    rect(c, x0,             PH - 8*mm,  8*mm, 8*mm, fill=ACCENT)
    rect(c, x0 + HW - 8*mm, 0,          8*mm, 8*mm, fill=ACCENT)

    label(c, 'INSIDE FRONT COVER', cx, 10*mm, 'DM-L', 6.5, rgba('#ffffff', 0.2), 'center')

    # Spine line
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.75)
    c.line(HW, 0, HW, PH)

    # ── INSIDE BACK COVER ────────────────────────────────────────────────────
    x1 = HW
    rect(c, x1, 0, HW, PH, fill=SURFACE)
    dot_grid(c, x1, 0, HW, PH, step=11*mm, alpha=0.04)

    # Same geometry: matching circles
    cx2 = x1 + HW/2
    c.saveState()
    c.setFillColor(Color(0.722, 0.878, 0.102, alpha=0.06))
    c.circle(cx2, PH/2, 120*mm, stroke=0, fill=1)
    c.restoreState()
    c.saveState()
    c.setStrokeColor(Color(0.722, 0.878, 0.102, alpha=0.18))
    c.setLineWidth(0.75)
    c.circle(cx2, PH/2, 130*mm, stroke=1, fill=0)
    c.restoreState()

    # Skill chips
    skills = ['Adobe Illustrator', 'Photoshop', 'InDesign',
              'After Effects', 'Figma', 'Cinema 4D', 'Edius']

    sy = PH/2 + 35*mm
    for sk in skills:
        sw = c.stringWidth(sk, 'DM', 8) + 10*mm
        px = cx2 - sw/2
        rect(c, px, sy - 3.5*mm, sw, 7.5*mm, fill=SURFACE2)
        c.saveState()
        c.setStrokeColor(Color(0.722, 0.878, 0.102, alpha=0.25))
        c.setLineWidth(0.5)
        c.rect(px, sy - 3.5*mm, sw, 7.5*mm, stroke=1, fill=0)
        c.restoreState()
        label(c, sk, cx2, sy - 1*mm, 'DM', 8, TEXT, 'center')
        sy -= 11*mm

    # Corner accents (mirror)
    rect(c, x1,             PH - 8*mm,  8*mm, 8*mm, fill=ACCENT)
    rect(c, x1 + HW - 8*mm, 0,          8*mm, 8*mm, fill=ACCENT)

    label(c, 'INSIDE BACK COVER', cx2, 10*mm, 'DM-L', 6.5, rgba('#ffffff', 0.2), 'center')


# ── SPREAD 3 ─  INTRODUCTION  ────────────────────────────────────────────────
# Left = Visual / label   |   Right = Cover Letter

def spread3(c):

    # ── LEFT: decorative intro panel ─────────────────────────────────────────
    x0 = 0
    rect(c, x0, 0, HW, PH, fill=BG)
    dot_grid(c, x0, 0, HW, PH)

    # Full-width accent stripe at top
    rect(c, x0, PH - 18*mm, HW, 18*mm, fill=ACCENT)
    label(c, 'INTRODUCTION', x0 + M, PH - 11*mm, 'DM-B', 9, BLACK)

    # Large rotated section number
    c.saveState()
    c.setFillColor(Color(0.722, 0.878, 0.102, alpha=0.08))
    c.setFont('DM-B', 200)
    c.translate(x0 + HW/2, PH/2)
    c.rotate(90)
    c.drawCentredString(0, -35, '01')
    c.restoreState()

    # Central decorative accent lines
    for i, xoff in enumerate([0, 5*mm, 10*mm]):
        alpha = 0.7 - i * 0.2
        rule(c, x0 + M, PH/2 + 10*mm - i*7*mm,
             HW - 2*M - xoff, 1.5 - i*0.4,
             Color(0.722, 0.878, 0.102, alpha=alpha))

    # Label text
    label(c, 'Cover Letter', x0 + M, PH/2 - 8*mm, 'DM-L', 11, MUTED)
    label(c, '— Zehra Mina Sarıoğlan', x0 + M, PH/2 - 18*mm, 'DM-L', 9, MUTED)

    # Bottom contact line
    rule(c, x0 + M, 22*mm, HW - 2*M, 0.5, rgba('#888888', 0.3))
    label(c, 'zehraminasarioglan@gmail.com', x0 + M, 15*mm, 'DM', 8, MUTED)
    label(c, 'zms-portfolio.onrender.com',  x0 + HW - M, 15*mm, 'DM', 8, ACCENT, 'right')

    # Spine
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.75)
    c.line(HW, 0, HW, PH)

    # ── RIGHT: Cover Letter ───────────────────────────────────────────────────
    x1 = HW
    rect(c, x1, 0, HW, PH, fill=SURFACE)

    tx = x1 + M + 4*mm          # text x
    tw = HW - 2*M - 8*mm        # text width
    ty = PH - M - 18*mm         # starting y

    # Top accent rule under heading
    rect(c, x1, PH - 16*mm, HW, 16*mm, fill=ACCENT)
    label(c, 'COVER LETTER', x1 + M, PH - 9.5*mm, 'DM-B', 9, BLACK)
    label(c, '01', x1 + HW - M, PH - 9.5*mm, 'DM-B', 9, BLACK, 'right')

    # Date / addressee
    ty -= 2*mm
    label(c, 'May 2025', tx, ty, 'DM-L', 8, MUTED)
    ty -= 9*mm
    label(c, 'Dear Hiring Team,', tx, ty, 'DM-M', 10, TEXT)
    ty -= 12*mm

    # Letter paragraphs
    paras = [
        ("I am Zehra Mina Sarıoğlan, a senior Graphic Design student at Bilkent University "
         "with a growing focus on visual storytelling, creative direction, and UI/UX design. "
         "My work is shaped by an interest in how design can create atmosphere, communicate "
         "emotion, and transform ideas into memorable visual experiences."),

        ("Throughout my education I have explored a wide range of disciplines — branding, "
         "editorial design, motion graphics, interface design, and conceptual visual systems. "
         "Each project is built around a strong narrative structure: not only designing how "
         "something looks, but also how it feels, moves, and connects with its audience. "
         "Alongside academic work I have applied these skills professionally, including a "
         "motion graphics internship at ShowTV and design contributions to TÜBİTAK and "
         "several corporate identity projects."),

        ("This portfolio presents selected works that reflect my approach to design as both "
         "a visual and strategic practice. Every piece is guided by research, experimentation, "
         "and a deep attention to detail. I am particularly drawn to creating refined, "
         "experience-driven design systems that balance conceptual depth with clear "
         "visual communication."),

        ("I see design as a way of telling stories, shaping perception, and building "
         "meaningful connections between people and ideas. As I approach graduation I am "
         "eager to bring this perspective into a professional environment — contributing "
         "to teams that value thoughtful, intentional design."),
    ]

    for para in paras:
        ty = wrap_text(c, para, tx, ty, 'DM', 9.5, TEXT, tw, leading=14.5)
        ty -= 10*mm

    # Closing
    label(c, 'Sincerely,', tx, ty, 'DM', 9.5, TEXT)
    ty -= 10*mm
    label(c, 'Zehra Mina Sarıoğlan', tx, ty, 'DM-B', 10, ACCENT)
    rule(c, tx, ty - 3*mm, 55*mm, 1.0)

    # Bottom rule
    rule(c, x1 + M, 14*mm, HW - 2*M, 0.5, rgba('#888888', 0.3))
    label(c, 'zehraminasarioglan@gmail.com', x1 + M, 8*mm, 'DM', 7.5, MUTED)


# ── SPREAD 4 ─  CURRICULUM VITAE  ────────────────────────────────────────────
# Left = Contact + Summary + Education + Experience
# Right = Activities + Skills + Languages

def spread4(c):

    # ── LEFT COLUMN ───────────────────────────────────────────────────────────
    x0 = 0
    rect(c, x0, 0, HW, PH, fill=BG)
    dot_grid(c, x0, 0, HW, PH, step=16*mm, alpha=0.04)

    # Header band
    rect(c, x0, PH - 20*mm, HW, 20*mm, fill=ACCENT)
    label(c, 'CURRICULUM VITAE', x0 + M, PH - 12*mm, 'DM-B', 9, BLACK)
    label(c, '02', x0 + HW - M, PH - 12*mm, 'DM-B', 9, BLACK, 'right')

    tx = x0 + M
    tw = HW - 2*M
    ty = PH - 26*mm

    # Name
    c.setFont('DM-B', 22)
    c.setFillColor(TEXT)
    c.drawString(tx, ty, 'Zehra Mina Sarıoğlan')
    ty -= 7*mm
    label(c, 'Senior Graphic Design Student — Bilkent University', tx, ty, 'DM-L', 9, MUTED)
    ty -= 5*mm
    rule(c, tx, ty, tw, 0.5, rgba('#888888', 0.3))
    ty -= 8*mm

    # ── Contact ───────────────────────────────────────────────────────────────
    ty = section_header(c, 'Contact', tx, ty, tw)
    info = [
        ('Email',     'zehraminasarioglan@gmail.com'),
        ('Phone',     '0553 456 1230'),
        ('LinkedIn',  'in/zehraminasarioglan'),
        ('Portfolio', 'zms-portfolio.onrender.com'),
        ('Location',  'Ankara, Türkiye'),
    ]
    for key, val in info:
        label(c, key.upper(), tx, ty, 'DM-L', 7, MUTED)
        label(c, val, tx + 22*mm, ty, 'DM', 7.5, TEXT)
        ty -= 5.5*mm
    ty -= 4*mm

    # ── Summary ───────────────────────────────────────────────────────────────
    ty = section_header(c, 'Summary', tx, ty, tw)
    summary = ("Senior Graphic Design student at Bilkent University with a strong interest "
               "in visual communication and digital design. Passionate about creating "
               "meaningful visual experiences through creativity and strategic thinking. "
               "Aspiring to grow in UI/UX design. Seeking a full-time position after graduation.")
    ty = wrap_text(c, summary, tx, ty, 'DM', 8.5, TEXT, tw, leading=13)
    ty -= 7*mm

    # ── Education ─────────────────────────────────────────────────────────────
    ty = section_header(c, 'Education', tx, ty, tw)
    edu = [
        ('Bilkent University',        'Graphic Design (BFA)', '2021 — ongoing'),
        ('Okyanus College High School','',                    '2017 — 2021'),
    ]
    for inst, dept, years in edu:
        label(c, inst, tx, ty, 'DM-M', 9, TEXT)
        label(c, years, tx + tw, ty, 'DM-L', 8, MUTED, 'right')
        ty -= 5*mm
        if dept:
            label(c, dept, tx + 3*mm, ty, 'DM-L', 8, MUTED)
            ty -= 5*mm
        ty -= 2*mm
    ty -= 2*mm

    # ── Experience ────────────────────────────────────────────────────────────
    ty = section_header(c, 'Experience', tx, ty, tw)
    exp = [
        ('Motion Graphic Design Intern', 'ShowTV', '2025',
         'Editing and producing motion graphics for broadcast news.'),
        ('Summer Intern', 'TÜBİTAK', '2024',
         'Designing information templates and visual materials.'),
        ('Freelance Logo Designer', 'Corporate Clients', '2024 — 2025',
         'Brand identity and logo design for various corporate clients.'),
    ]
    for role, org, yr, desc in exp:
        label(c, role, tx, ty, 'DM-M', 9, TEXT)
        label(c, yr,   tx + tw, ty, 'DM-L', 8, MUTED, 'right')
        ty -= 5*mm
        label(c, org,  tx + 3*mm, ty, 'DM', 8, ACCENT)
        ty -= 5*mm
        ty = wrap_text(c, desc, tx + 3*mm, ty, 'DM-L', 8, MUTED, tw - 3*mm, leading=12)
        ty -= 4*mm

    # Bottom rule
    rule(c, tx, 14*mm, tw, 0.5, rgba('#888888', 0.3))
    label(c, 'Zehra Mina Sarıoğlan — CV', tx, 8*mm, 'DM-L', 7, MUTED)

    # Spine
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.75)
    c.line(HW, 0, HW, PH)

    # ── RIGHT COLUMN ──────────────────────────────────────────────────────────
    x1 = HW
    rect(c, x1, 0, HW, PH, fill=SURFACE)
    dot_grid(c, x1, 0, HW, PH, step=16*mm, alpha=0.04)

    # Header band (same height as left, continuation)
    rect(c, x1, PH - 20*mm, HW, 20*mm, fill=SURFACE2)
    rule(c, x1, PH - 20*mm, HW, 0.75, rgba('#B8E01A', 0.5))
    label(c, 'CURRICULUM VITAE (CONT\'D)', x1 + M, PH - 12*mm, 'DM-M', 8, MUTED)

    tx2 = x1 + M
    tw2 = HW - 2*M
    ty2 = PH - 28*mm

    # ── Activities & Societies ────────────────────────────────────────────────
    ty2 = section_header(c, 'Activities & Societies', tx2, ty2, tw2)
    acts = [
        ('Bilkent Tennis Team Captain',  '2025 — 2026', ''),
        ('Bilkent Winter Sports',        '2025',        'Managing club designs and social media.'),
        ('ACM Bilkent — Active Member',  '2023 — 2024', 'Managing club designs and social media.'),
        ('Guide Student',                '2024',        'Bilkent University campus guide.'),
        ('Tennis Instructor',            '2024',        'Ankara Tenis Kulübü.'),
        ('English Summer Camp Guide',    '2023',        'Guide for high school students.'),
    ]
    for title, yr, desc in acts:
        label(c, title, tx2, ty2, 'DM-M', 9, TEXT)
        label(c, yr,    tx2 + tw2, ty2, 'DM-L', 8, MUTED, 'right')
        ty2 -= 5*mm
        if desc:
            label(c, desc, tx2 + 3*mm, ty2, 'DM-L', 8, MUTED)
            ty2 -= 5*mm
        ty2 -= 1.5*mm
    ty2 -= 5*mm

    # ── Skills ────────────────────────────────────────────────────────────────
    ty2 = section_header(c, 'Skills & Tools', tx2, ty2, tw2)
    skills_list = [
        ('Adobe Illustrator', 'Vector & identity design'),
        ('Adobe Photoshop',   'Photo editing & compositing'),
        ('Adobe InDesign',    'Editorial & print layout'),
        ('Adobe After Effects','Motion graphics & animation'),
        ('Figma',             'UI/UX design & prototyping'),
        ('Maxon Cinema 4D',   '3D design & modelling'),
        ('Edius',             'Video editing'),
    ]
    for tool, desc in skills_list:
        label(c, tool, tx2, ty2, 'DM-M', 9, TEXT)
        label(c, desc, tx2 + 38*mm, ty2, 'DM-L', 8, MUTED)
        ty2 -= 6*mm
    ty2 -= 6*mm

    # ── Languages ─────────────────────────────────────────────────────────────
    ty2 = section_header(c, 'Languages', tx2, ty2, tw2)
    langs = [('Turkish', 'Native'), ('English', 'Advanced')]
    for lang, level in langs:
        label(c, lang,  tx2, ty2, 'DM-M', 9, TEXT)
        label(c, level, tx2 + tw2, ty2, 'DM', 8.5, ACCENT, 'right')
        ty2 -= 7*mm
    ty2 -= 5*mm

    # Accent rectangle decorative element (bottom-right)
    rect(c, x1 + HW - 30*mm, 0, 30*mm, 3.5*mm, fill=ACCENT)

    # Bottom rule
    rule(c, tx2, 14*mm, tw2, 0.5, rgba('#888888', 0.3))
    label(c, '2025', tx2 + tw2, 8*mm, 'DM-L', 7, MUTED, 'right')


# ── SPREAD 5 ─  WORK PAGE  ───────────────────────────────────────────────────
# Left = Project metadata   |   Right = Project image

def spread5(c):

    IMG_PATH = BASE + 'conceptual poster design/a convenient day mockup poster.png'

    # ── LEFT: Project info ────────────────────────────────────────────────────
    x0 = 0
    rect(c, x0, 0, HW, PH, fill=BG)
    dot_grid(c, x0, 0, HW, PH)

    # Header band
    rect(c, x0, PH - 20*mm, HW, 20*mm, fill=ACCENT)
    label(c, 'SELECTED WORK', x0 + M, PH - 12*mm, 'DM-B', 9, BLACK)
    label(c, '03', x0 + HW - M, PH - 12*mm, 'DM-B', 9, BLACK, 'right')

    tx = x0 + M
    tw = HW - 2*M
    ty = PH - 30*mm

    # Project label chip
    chip_w = 40*mm
    rect(c, tx, ty - 5.5*mm, chip_w, 7.5*mm, fill=SURFACE2)
    c.saveState()
    c.setStrokeColor(Color(0.722, 0.878, 0.102, alpha=0.3))
    c.setLineWidth(0.5)
    c.rect(tx, ty - 5.5*mm, chip_w, 7.5*mm, stroke=1, fill=0)
    c.restoreState()
    label(c, 'POSTER DESIGN', tx + chip_w/2, ty - 2*mm, 'DM-M', 7, ACCENT, 'center')
    ty -= 13*mm

    # Project title
    c.setFont('DM-B', 28)
    c.setFillColor(TEXT)
    c.drawString(tx, ty, 'A Convenient')
    ty -= 32
    c.drawString(tx, ty, 'Day')
    ty -= 10*mm

    rule(c, tx, ty, tw, 2.0)
    ty -= 8*mm

    # Meta info grid
    meta = [
        ('YEAR',     '2024'),
        ('MEDIUM',   'Digital — Adobe Illustrator\n& Photoshop'),
        ('CATEGORY', 'Conceptual Poster'),
        ('COURSE',   'GRA 401 — Portfolio'),
    ]
    for key, val in meta:
        label(c, key, tx, ty, 'DM-B', 7, MUTED)
        ty -= 5.5*mm
        for line in val.split('\n'):
            label(c, line, tx, ty, 'DM', 9, TEXT)
            ty -= 5.5*mm
        ty -= 3*mm

    ty -= 3*mm
    rule(c, tx, ty, tw, 0.5, rgba('#888888', 0.3))
    ty -= 10*mm

    # Description
    label(c, 'About the Project', tx, ty, 'DM-B', 9, TEXT)
    ty -= 8*mm
    description = (
        "A Convenient Day is a conceptual poster that examines the visual language "
        "of everyday routine — how ordinary moments accumulate into something "
        "meaningful. The composition uses layered imagery, restrained typography, "
        "and controlled negative space to create visual tension, inviting the viewer "
        "to pause and reconsider the familiar.\n\n"
        "The design explores atmosphere and narrative through a minimal formal "
        "vocabulary: repetition, scale contrast, and deliberate silence. It "
        "reflects a broader interest in designing not just what is seen, but "
        "what is felt."
    )
    for para in description.split('\n\n'):
        ty = wrap_text(c, para, tx, ty, 'DM-L', 9, TEXT, tw, leading=14)
        ty -= 8*mm

    # Bottom rule + credit
    rule(c, tx, 14*mm, tw, 0.5, rgba('#888888', 0.3))
    label(c, 'Zehra Mina Sarıoğlan — 2024', tx, 8*mm, 'DM-L', 7, MUTED)

    # Spine
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.75)
    c.line(HW, 0, HW, PH)

    # ── RIGHT: Full-bleed project image ───────────────────────────────────────
    x1 = HW
    rect(c, x1, 0, HW, PH, fill=BLACK)

    # Image sizing — square image, fill the right half maintaining aspect ratio
    # The image is 3333×3333 (square). Fit to HW × PH with cover behaviour.
    img_size = min(HW, PH)  # fit inside
    pad = 8*mm
    iw = HW - 2*pad
    ih = PH - 2*pad  # use full height with small padding

    # Since image is square, fit by height (PH is likely smaller than HW)
    # Available area: HW × PH
    avail_w = HW - 2*pad
    avail_h = PH - 2*pad
    # Image is square → scale by the smaller dimension
    side = min(avail_w, avail_h)
    ix = x1 + (HW - side) / 2
    iy = (PH - side) / 2

    c.drawImage(
        ImageReader(IMG_PATH),
        ix, iy, side, side,
        preserveAspectRatio=True,
        mask='auto'
    )

    # Subtle overlay caption bar
    rect(c, x1, 0, HW, 14*mm, fill=Color(0, 0, 0, alpha=0.72))
    label(c, 'A CONVENIENT DAY — CONCEPTUAL POSTER DESIGN — 2024',
          x1 + HW/2, 5.5*mm, 'DM-L', 6.5, rgba('#ffffff', 0.5), 'center')


# ── Main ──────────────────────────────────────────────────────────────────────

def build():
    register_fonts()
    c = Canvas(OUTPUT, pagesize=landscape(A3))
    c.setTitle("Zehra Mina Sarıoğlan — Graphic Design Portfolio")
    c.setAuthor("Zehra Mina Sarıoğlan")
    c.setSubject("GRA 401 Portfolio — Bilkent University 2025")

    spreads = [
        ('Spread 1 — Exterior Covers',  spread1),
        ('Spread 2 — Interior Covers',  spread2),
        ('Spread 3 — Introduction',     spread3),
        ('Spread 4 — CV',               spread4),
        ('Spread 5 — Work Page',        spread5),
    ]

    for name, fn in spreads:
        print(f'  Rendering {name}…')
        fn(c)
        c.showPage()

    c.save()
    import os
    size_kb = os.path.getsize(OUTPUT) // 1024
    print(f'\n✓  Saved → {OUTPUT}  ({size_kb} KB)')


if __name__ == '__main__':
    build()
