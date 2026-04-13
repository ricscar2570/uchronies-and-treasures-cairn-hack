"""
Uchronies & Treasures — Complete KDP Manual
A5 two-column, premium layout
All content from repository, edited and formatted
"""

import os
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    NextPageTemplate, Table, TableStyle, HRFlowable, KeepTogether, CondPageBreak
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re

# Font path — Linux default. On macOS change to your Liberation fonts directory.
# Install on Ubuntu/Debian: sudo apt install fonts-liberation
BASE = "/usr/share/fonts/truetype/liberation/"
import os as _os
if not _os.path.isdir(BASE):
    # Try common macOS Homebrew path
    _mac = "/opt/homebrew/share/fonts/liberation-fonts/"
    if _os.path.isdir(_mac):
        BASE = _mac
    else:
        raise FileNotFoundError(
            f"Liberation fonts not found at {BASE}\n"
            "Install with: sudo apt install fonts-liberation\n"
            "Or set BASE manually at the top of this script."
        )
pdfmetrics.registerFont(TTFont("Ser",    BASE+"LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("SerB",   BASE+"LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("SerI",   BASE+"LiberationSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("SerBI",  BASE+"LiberationSerif-BoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("San",    BASE+"LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("SanB",   BASE+"LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("SanI",   BASE+"LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Mono",   BASE+"LiberationMono-Bold.ttf"))
pdfmetrics.registerFontFamily("Ser", normal="Ser", bold="SerB",
    italic="SerI", boldItalic="SerBI")

# ── COLORS ───────────────────────────────────────────────────────────────────
CRIMSON  = colors.HexColor("#8B0000")
AMBER    = colors.HexColor("#C0392B")
NAVY     = colors.HexColor("#1a1a2e")
GOLD     = colors.HexColor("#C9A96E")
CREAM    = colors.HexColor("#FDF6EC")
LGREY    = colors.HexColor("#F5F5F0")
SLATE    = colors.HexColor("#2C3E50")
MGREY    = colors.HexColor("#CCCCCC")
WHITE    = colors.white
BLACK    = colors.black

# ── GEOMETRY ─────────────────────────────────────────────────────────────────
PW, PH = A5
ML, MR, MT, MB = 14*mm, 12*mm, 16*mm, 16*mm
GAP  = 4*mm
CW   = (PW - ML - MR - GAP) / 2   # ~59mm per column
FW   = PW - ML - MR               # ~122mm full width

# ── STYLES ───────────────────────────────────────────────────────────────────
S = ParagraphStyle

STYLES = {
  "h1":  S("h1",  fontName="SanB",  fontSize=13, textColor=CRIMSON,
           spaceBefore=8, spaceAfter=4, leading=17, keepWithNext=1),
  "h2":  S("h2",  fontName="SanB",  fontSize=10, textColor=NAVY,
           spaceBefore=6, spaceAfter=3, leading=13, keepWithNext=1),
  "h3":  S("h3",  fontName="SanB",  fontSize=8.5, textColor=SLATE,
           spaceBefore=4, spaceAfter=2, leading=12, keepWithNext=1),
  "body":S("body",fontName="Ser",   fontSize=8,  textColor=BLACK,
           alignment=TA_JUSTIFY, spaceBefore=2, spaceAfter=2, leading=11.5),
  "bi":  S("bi",  fontName="SerI",  fontSize=8,  textColor=BLACK,
           alignment=TA_JUSTIFY, spaceBefore=2, spaceAfter=2, leading=11.5),
  "bul": S("bul", fontName="Ser",   fontSize=8,  textColor=BLACK,
           leftIndent=9, firstLineIndent=-6,
           spaceBefore=1, spaceAfter=1, leading=11),
  "note":S("note",fontName="SerI",  fontSize=7.5, textColor=NAVY,
           leftIndent=5, rightIndent=3, alignment=TA_JUSTIFY,
           spaceBefore=3, spaceAfter=3, leading=10.5),
  "th":  S("th",  fontName="SanB",  fontSize=7,  textColor=WHITE,
           alignment=TA_CENTER, leading=9),
  "td":  S("td",  fontName="Ser",   fontSize=7.5, textColor=BLACK,
           alignment=TA_LEFT,   leading=10),
  "tdc": S("tdc", fontName="Ser",   fontSize=7.5, textColor=BLACK,
           alignment=TA_CENTER, leading=10),
  "stat":S("stat",fontName="SerB",  fontSize=8,  textColor=NAVY,
           spaceBefore=1, spaceAfter=1, leading=11),
  "foot":S("foot",fontName="San",   fontSize=6.5, textColor=GOLD,
           alignment=TA_CENTER),
  "hdr": S("hdr", fontName="SanI",  fontSize=6.5, textColor=GOLD),
  "toc0":S("toc0",fontName="SanB",  fontSize=8.5, textColor=NAVY,
           leftIndent=0,  spaceAfter=3,  leading=12),
  "toc1":S("toc1",fontName="Ser",   fontSize=7.5, textColor=SLATE,
           leftIndent=9,  spaceAfter=2,  leading=11),
  "toc2":S("toc2",fontName="SerI",  fontSize=7,   textColor=SLATE,
           leftIndent=16, spaceAfter=1,  leading=10),
  "covertitle": S("covertitle", fontName="SanB", fontSize=22,
           textColor=WHITE, alignment=TA_CENTER, leading=28),
  "coversub":   S("coversub",   fontName="SanI", fontSize=9.5,
           textColor=GOLD,  alignment=TA_CENTER, leading=14),
  "covertag":   S("covertag",   fontName="SerI", fontSize=8.5,
           textColor=WHITE, alignment=TA_CENTER, leading=13),
}

# ── HELPERS ──────────────────────────────────────────────────────────────────

def sp(h=3): return Spacer(1, h*mm)
def pb():    return PageBreak()
def npb():   return NextPageTemplate("TwoCol")
def nfull(): return NextPageTemplate("Full")

def rule(c=GOLD, t=0.5):
    return HRFlowable(width="100%", thickness=t, color=c,
                      spaceBefore=2*mm, spaceAfter=2*mm)

def md(text):
    """Convert basic markdown to ReportLab XML."""
    text = str(text)
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    text = re.sub(r'\*\*(.+?)\*\*',     r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*',         r'<i>\1</i>', text)
    text = re.sub(r'`(.+?)`',           r'<font name="Mono">\1</font>', text)
    # em dash cleanup
    text = text.replace('\u2014', ',').replace(' -- ', ', ').replace('--', ',')
    return text

def p(text, style="body"):
    return Paragraph(md(text), STYLES[style])

def b(text):
    return Paragraph("<bullet>&bull;</bullet>" + md(text), STYLES["bul"])

def note(text):
    return KeepTogether([
        Table([[Paragraph(md(text), STYLES["note"])]],
            colWidths=[CW-3*mm],
            style=TableStyle([
                ("BOX",         (0,0),(-1,-1), 0.5, GOLD),
                ("LEFTPADDING", (0,0),(-1,-1), 5),
                ("RIGHTPADDING",(0,0),(-1,-1), 5),
                ("TOPPADDING",  (0,0),(-1,-1), 4),
                ("BOTTOMPADDING",(0,0),(-1,-1),4),
                ("BACKGROUND",  (0,0),(-1,-1), CREAM),
            ]))
    ])

def fullnote(text):
    return KeepTogether([
        Table([[Paragraph(md(text), STYLES["note"])]],
            colWidths=[FW-3*mm],
            style=TableStyle([
                ("BOX",         (0,0),(-1,-1), 0.5, GOLD),
                ("LEFTPADDING", (0,0),(-1,-1), 6),
                ("RIGHTPADDING",(0,0),(-1,-1), 6),
                ("TOPPADDING",  (0,0),(-1,-1), 5),
                ("BOTTOMPADDING",(0,0),(-1,-1),5),
                ("BACKGROUND",  (0,0),(-1,-1), CREAM),
            ]))
    ])

def T(headers, rows, widths, full=False):
    """Build a styled table."""
    base = FW if full else CW
    data = [[Paragraph(md(h), STYLES["th"]) for h in headers]]
    for row in rows:
        data.append([Paragraph(md(str(c)), STYLES["td"]) for c in row])
    ts = TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  SLATE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LGREY]),
        ("GRID",          (0,0),(-1,-1), 0.25, MGREY),
        ("TOPPADDING",    (0,0),(-1,-1), 2),
        ("BOTTOMPADDING", (0,0),(-1,-1), 2),
        ("LEFTPADDING",   (0,0),(-1,-1), 3),
        ("RIGHTPADDING",  (0,0),(-1,-1), 3),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ])
    return KeepTogether([Table(data, colWidths=widths, style=ts, hAlign="LEFT")])

def statblock(text):
    return Paragraph(md(text), STYLES["stat"])

def h1(t): return Paragraph(md(t), STYLES["h1"])
def h2(t): return Paragraph(md(t), STYLES["h2"])
def h3(t): return Paragraph(md(t), STYLES["h3"])

# ── DOC CLASS ────────────────────────────────────────────────────────────────

class UeTDoc(BaseDocTemplate):
    def __init__(self, fn):
        super().__init__(fn, pagesize=A5,
            leftMargin=ML, rightMargin=MR,
            topMargin=MT, bottomMargin=MB)
        self._chapter = ""
        self.toc = TableOfContents()
        self.toc.levelStyles = [STYLES["toc0"], STYLES["toc1"], STYLES["toc2"]]
        self._setup()

    def _setup(self):
        cov = Frame(0, 0, PW, PH, leftPadding=0, rightPadding=0,
                    topPadding=0, bottomPadding=0, id="cov")
        blk = Frame(ML, MB, FW, PH-MT-MB, id="blk")
        toc = Frame(ML, MB, FW, PH-MT-MB, id="toc")
        L   = Frame(ML,           MB, CW, PH-MT-MB, id="L")
        R   = Frame(ML+CW+GAP,    MB, CW, PH-MT-MB, id="R")
        F   = Frame(ML,           MB, FW, PH-MT-MB, id="F")

        self.addPageTemplates([
            PageTemplate(id="Cover", frames=[cov]),
            PageTemplate(id="Blank", frames=[blk], onPage=self._pg_blank),
            PageTemplate(id="TOC",   frames=[toc],  onPage=self._pg_toc),
            PageTemplate(id="TwoCol",frames=[L,R],   onPage=self._pg_run),
            PageTemplate(id="Full",  frames=[F],     onPage=self._pg_run),
        ])

    def afterFlowable(self, f):
        if isinstance(f, Paragraph):
            txt = f.getPlainText()
            sn  = f.style.name
            if sn == "h1":
                self._chapter = txt
                self.notify("TOCEntry", (0, txt, self.page))
            elif sn == "h2":
                self.notify("TOCEntry", (1, txt, self.page))

    def _pg_blank(self, c, d): pass

    def _pg_toc(self, c, d):
        self._footer(c, d, show=False)

    def _pg_run(self, c, d):
        self._footer(c, d, show=True)

    def _footer(self, c, d, show=True):
        c.saveState()
        c.setStrokeColor(GOLD); c.setLineWidth(0.4)
        c.line(ML, MB-3.5*mm, PW-MR, MB-3.5*mm)
        c.setFont("San", 6.5); c.setFillColor(GOLD)
        c.drawCentredString(PW/2, MB-7*mm, str(d.page))
        if show and self._chapter:
            c.setFont("SanI", 6)
            c.drawString(ML, MB-7*mm, self._chapter[:45])
            c.drawRightString(PW-MR, MB-7*mm, "Uchronies & Treasures")
        c.restoreState()


# ── COVER BUILDER ────────────────────────────────────────────────────────────

def make_cover_pdf():
    from reportlab.pdfgen import canvas as cv
    import io
    buf = io.BytesIO()
    c = cv.Canvas(buf, pagesize=A5)
    mm_pt = 72/25.4

    # Background: cover image stretched to full A5 page
    import os as _os
    _cover_path = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "img", "cover.png")
    if _os.path.exists(_cover_path):
        c.drawImage(_cover_path, 0, 0, PW, PH, preserveAspectRatio=False, mask="auto")
    else:
        c.setFillColor(NAVY); c.rect(0,0,PW,PH,fill=1,stroke=0)
    # Dark overlay on top band for readability
    from reportlab.lib.colors import Color as _Color
    _overlay = _Color(0, 0, 0, alpha=0.62)
    c.setFillColor(_overlay); c.rect(0, PH-34*mm_pt, PW, 34*mm_pt, fill=1, stroke=0)
    # Dark overlay on bottom band
    c.setFillColor(_overlay); c.rect(0, 0, PW, 20*mm_pt, fill=1, stroke=0)
    # Separator lines
    c.setStrokeColor(GOLD); c.setLineWidth(0.8)
    c.line(14*mm_pt, PH-34*mm_pt, PW-12*mm_pt, PH-34*mm_pt)
    c.line(14*mm_pt, 20*mm_pt,    PW-12*mm_pt, 20*mm_pt)
    c.setLineWidth(0.3)
    c.line(14*mm_pt, PH-36.5*mm_pt, PW-12*mm_pt, PH-36.5*mm_pt)
    c.line(14*mm_pt, 22.5*mm_pt,    PW-12*mm_pt, 22.5*mm_pt)

    # Titles
    c.setFont("SanB", 21); c.setFillColor(WHITE)
    c.drawCentredString(PW/2, PH-19*mm_pt, "UCHRONIES")
    c.drawCentredString(PW/2, PH-27*mm_pt, "& TREASURES")
    c.setFont("SanI", 9.5); c.setFillColor(GOLD)
    c.drawCentredString(PW/2, PH-40*mm_pt, "A Cairn Hack by Riccardo Scaringi")

    # Rule
    c.setStrokeColor(GOLD); c.setLineWidth(0.4)
    c.line(PW/2-28*mm_pt, PH-45*mm_pt, PW/2+28*mm_pt, PH-45*mm_pt)

    # Genre label
    c.setFont("SanB", 7); c.setFillColor(GOLD)
    c.drawCentredString(PW/2, PH-49*mm_pt, "TEMPORAL NOIR  RPG")

    # Taglines
    c.setFont("SerI", 8.5); c.setFillColor(WHITE)
    lines = [
        "Las Vegas, 2080.",
        "",
        "You work for the Temporal Division.",
        "Pay: $800 a week.",
        "Expenses: $900 a week.",
        "The math does not add up.",
        "",
        "Madame Zhou is waiting.",
    ]
    y = PH - 62*mm_pt
    for ln in lines:
        if ln: c.drawCentredString(PW/2, y, ln)
        y -= 10.5

    # Separator
    c.setStrokeColor(GOLD); c.setLineWidth(0.3)
    c.line(PW/2-20*mm_pt, y-4*mm_pt, PW/2+20*mm_pt, y-4*mm_pt)

    # Three pillars
    c.setFont("SanB", 6.5); c.setFillColor(GOLD)
    px = [PW/2-34*mm_pt, PW/2, PW/2+34*mm_pt]
    for txt, x in zip(["ECONOMIC PRESSURE","MORAL CORRUPTION","CONTAMINATION"], px):
        c.drawCentredString(x, y-10*mm_pt, txt)

    # Description block - positioned in middle section
    y2 = y - 24*mm_pt
    c.setFont("SerI", 7.5); c.setFillColor(colors.HexColor("#8899BB"))
    lower_lines = [
        "A game about desperate people in impossible situations.",
        "About the slow math of debt and the faster math of corruption.",
        "About the permanent cost of every choice you make.",
        "",
        "Requires: 2-5 players, one Warden, polyhedral dice,",
        "and a willingness to ask hard questions.",
        "",
        "15 minutes to create a character.",
        "One session to feel the pressure.",
        "Ten sessions to see who you have become.",
    ]
    for ln in lower_lines:
        if ln: c.drawCentredString(PW/2, y2, ln)
        y2 -= 9.5

    # Bottom decorative border box with final tagline
    box_y = 30*mm_pt
    box_h = 20*mm_pt
    box_x = 18*mm_pt
    box_w = PW - 36*mm_pt
    c.setStrokeColor(GOLD); c.setLineWidth(0.5)
    c.rect(box_x, box_y, box_w, box_h, fill=0, stroke=1)
    # thin inner rule
    c.setLineWidth(0.2)
    c.rect(box_x+1.5*mm_pt, box_y+1.5*mm_pt,
           box_w-3*mm_pt, box_h-3*mm_pt, fill=0, stroke=1)
    # quote text
    c.setFont("SerI", 7); c.setFillColor(GOLD)
    c.drawCentredString(PW/2, box_y + box_h*0.62,
        "\"Vegas was never an honest city.")
    c.drawCentredString(PW/2, box_y + box_h*0.35,
        "But at least before, the rules were clear. Now? Time itself is rigged.\"")

    # Bottom rule and credits
    c.setStrokeColor(GOLD); c.setLineWidth(0.4)
    c.line(14*mm_pt, 24*mm_pt, PW-12*mm_pt, 24*mm_pt)
    c.setFont("San", 6.5); c.setFillColor(WHITE)
    c.drawCentredString(PW/2, 11*mm_pt, "Based on Cairn by Yochai Gal  |  CC BY-SA 4.0")
    c.drawCentredString(PW/2, 7*mm_pt, "ilgiocointavolo.it")

    c.showPage(); c.save()
    buf.seek(0)
    return buf


# ── CONTENT ──────────────────────────────────────────────────────────────────

def story():
    s = []

    # ── BLANK ──
    s += [NextPageTemplate("Blank"), pb(), p(""), NextPageTemplate("TOC"), pb()]

    # ── TOC ──
    toc_title_style = ParagraphStyle("toc_page_title",
        fontName="SanB", fontSize=13, textColor=CRIMSON,
        spaceBefore=8, spaceAfter=6, leading=17)
    s += [
        Paragraph("Contents", toc_title_style),
        HRFlowable(width="100%", thickness=0.5, color=GOLD,
                   spaceBefore=2*mm, spaceAfter=3*mm),
        sp(2),
        TableOfContents(),
    ]
    s += [NextPageTemplate("TwoCol"), pb()]

    # ════════════════════════════════
    # OVERVIEW & PRINCIPLES
    # ════════════════════════════════
    s += [h1("Overview & Principles"), rule(),
    p("**Uchronies & Treasures** is a tabletop RPG for one Warden and 2-5 players. You are agents of the Temporal Division, a government agency that sends expendable operatives into unstable time zones to recover artifacts, neutralize threats, and maintain the timeline. The pay is terrible. The rent is worse. And Madame Zhou is always ready with an offer you cannot refuse."),
    sp(1),
    p("The game uses the **Cairn** engine by Yochai Gal. Character creation takes 15 minutes. Combat is fast and deadly. The real danger is not the bullets. It is the debt."),
    sp(2),
    h2("The 5 Design Pillars"),
    h3("1. Grey Choices"),
    p("No choice is perfect. Every decision has a cost. You are not a hero saving the world. You are a desperate person trying to survive an impossible situation. The game does not judge. It records. After 10 sessions, look at your character sheet and see who you have become."),
    sp(1),
    note("Example choices: *deliver the fragment to the Division* (loyal, poor, +1 Loyalty). *Sell it to Zhou* (rich, +2 Corruption, fired if caught). *Keep it* (+5 Corruption, everyone hunts you). All valid. All costly."),
    sp(2),
    h3("2. Economic Pressure"),
    p("**Corruption is not a moral choice. It is a mathematical necessity.** The economic system is calibrated to be *unsustainable*. Base pay: $800/week. Mandatory expenses: $900/week. After 10 weeks without cutting corners, you have accumulated a deficit of $1,000. Zhou offers $5,000 for a small piece of information. What do you do?"),
    sp(1),
    p("The game pushes you toward corruption. Not by force. With math."),
    sp(2),
    h3("3. Temporal Contamination"),
    p("Time corrodes you. Slowly. Permanently. Every 6 hours in a temporal zone, make a **WIL save**. Failure means direct damage to your willpower and, if significant, a permanent **Temporal Quirk**. Accumulate 5 Quirks and you become a **temporal echo**: a hostile NPC. Your character is lost forever."),
    sp(2),
    h3("4. Speed"),
    p("Ready to play in 30 minutes. Comfortable with the system in two sessions."),
    sp(1),
    b("**Character creation:** 15 minutes"),
    b("**Rules explanation:** 10 minutes (d20 under attribute, roll damage, track money)"),
    b("**Start playing:** 5 minutes (Warden reads the opening scene)"),
    sp(1),
    p("This game has six trackers per character. It is not minimal-rules: it has few resolution mechanics but many narrative variables in play at once. Two sessions is enough to internalize them. The trackers become interesting exactly when they start to bite."),
    sp(2),
    h3("5. The Curiosity Machine"),
    p("Five questions every player should be asking at session's end:"),
    sp(1),
    b("I made a decision that had real weight."),
    b("Every decision had real consequences."),
    b("I did things I did not think I would do. And I justified them."),
    b("I chose survival over principles. Would I do it again?"),
    b("What happens next? How far can I push before I break?"),
    sp(2),
    p("If you achieve this at the table, the game works. The rest is details."),
    sp(3),
    h2("Principles for the Warden"),
    b("**Information.** Provide useful information freely. Players do not need to roll dice to learn about their circumstances. When in doubt, give more, not less."),
    b("**Danger.** Telegraph serious danger clearly. The more lethal the situation, the more obvious the warning signs. Never kill a character without warning."),
    b("**The Economy is the Engine.** Track money carefully. The deficit is the game's heartbeat. If players are not worried about rent, something has gone wrong."),
    b("**NPCs Want Things.** Hayes wants order. Zhou wants profit. Every NPC has goals that may align or conflict with the players. Let them pursue those goals."),
    b("**Let Them Choose.** Never force a moral decision. Present the situation clearly. Whatever they choose, there will be consequences."),
    b("**Time Pressure.** Every week costs money. Every delay increases the debt. Do not let the pace slacken."),
    sp(3),
    h2("Principles for Players"),
    b("**You Are Expendable.** The Division considers you replaceable. Caution keeps you alive longer than bravery."),
    b("**The Math is Real.** Track every dollar. Know your weekly deficit. The moment you stop tracking money, the game loses its teeth."),
    b("**Fighting is Expensive.** Bullets, injuries, and downtime all cost money you do not have. Avoid combat when possible."),
    b("**Corruption is a Spectrum.** The game will not punish you for accepting Zhou's offers. Every choice has a price. Pay attention to what you are becoming."),
    b("**Ask Questions.** Ask the Warden what your character would know. Ask NPCs what they want. Ask yourself how far you are willing to go."),
    pb(),
    ]

    # ════════════════════════════════
    # CHARACTER CREATION
    # ════════════════════════════════
    s += [h1("Character Creation"), rule(),
    note("**Target time: 15 minutes.** You do not build an optimal character after 2 hours of analysis. You generate a desperate person ready to play immediately. Each tracker becomes interesting at the moment it starts to bite."),
    sp(2),
    h2("Overview (7 Steps)"),
    b("**Step 1:** Roll Ability Scores (1 min)"),
    b("**Step 2:** Roll Hit Protection (30 sec)"),
    b("**Step 3:** Choose Background (2 min)"),
    b("**Step 4:** Note Starting Gear (2 min)"),
    b("**Step 5:** Set Trackers (1 min)"),
    b("**Step 6:** Roll Traits (2 min)"),
    b("**Step 7:** Narrative Details (3 min)"),
    sp(3),
    h2("1. Ability Scores"),
    p("Characters have three attributes. **Roll 3d6 for each, in order.** You may then swap any two results."),
    sp(1),
    b("**Strength (STR):** Physical power, endurance, resistance to poison and pain."),
    b("**Dexterity (DEX):** Agility, reflexes, precision, stealth."),
    b("**Willpower (WIL):** Mental resilience, perception, social influence. Resisting contamination, persuading, deceiving, commanding."),
    sp(2),
    h2("2. Hit Protection (HP)"),
    p("**Roll 1d6** for starting HP. HP reflects your ability to avoid serious harm: luck, reflexes, instinct for cover. It does not represent physical toughness. When HP reaches 0, the next hit goes directly to your body (STR damage). HP recovers quickly with rest and water. Attribute damage takes a week of medical care."),
    sp(3),
    h2("3. Background"),
    p("Choose or roll 1d6. Backgrounds do not grant mechanical skills. They inform what your character plausibly knows and what actions do not require a save."),
    sp(1),
    nfull(), pb(),
    T(["d6", "Background", "You were..."],
      [["1","Ex-Military","A soldier, marine, or private contractor. You know weapons, tactics, and survival."],
       ["2","Failed Academic","A doctoral candidate in history, physics, or archaeology. You know languages, epochs, and artifacts."],
       ["3","Reformed Criminal","A burglar, forger, or worse. The Division offered a job instead of prison. 'Reformed' is a strong word."],
       ["4","Corrupt Cop","A detective who took bribes. The Division hires people who already know the grey zone."],
       ["5","Disbarred Medic","You had a medical license. A mistake took it away. The Division asks for competence, not references."],
       ["6","Con Artist","You sold air, false promises, worthless investments. Good with words, better with lies."]],
      [8*mm, 28*mm, FW-36*mm], full=True),
    sp(3),
    h2("Starting Gear"),
    p("**Standard Division issue (5 slots):** Glock 17 pistol (d6, 1 slot), 2 extra magazines (1 slot), basic first aid kit (3 uses, heals d4 STR, 1 slot), anti-rejection medicine 4 weeks supply (1 slot), 3 days rations (1 slot)."),
    sp(1),
    p("**Worn (not counted):** Light tactical vest, kevlar II (1 Armor). Temporal protection suit (reduces WIL contamination damage by 1, worn under clothes). Civilian clothes."),
    sp(1),
    p("**Pockets (0 slots):** Encrypted cellphone, Division badge, $500 cash."),
    sp(2),
    T(["Ex-Military", "Failed Academic", "Reformed Criminal"],
      [["Combat knife (d6, 1 slot)", "3 rare books (bulky)", "Lockpick set (1 slot)"],
       ["Compass (0 slots)", "Magnifying lens (0 slots)", "1 criminal contact"],
       ["Zippo lighter (0 slots)", "Half-filled notebook (0 slots)", "Burner phone (0 slots)"]],
      [FW/3, FW/3, FW/3], full=True),
    sp(2),
    T(["Corrupt Cop", "Disbarred Medic", "Con Artist"],
      [["Fake detective badge (0 slots)", "Field med kit (5 uses, d4 STR, 1 slot)", "3 fake IDs (1 slot)"],
       ["Handcuffs (1 slot)", "Morphine, 3 vials (1 slot)", "$500 extra cash (0 slots)"],
       ["Pepper spray (d4, 0 slots)", "Surgical scalpel (d6, 0 slots)", "Fake Rolex (0 slots)"]],
      [FW/3, FW/3, FW/3], full=True),
    sp(3),
    h2("Inventory"),
    p("Characters have **10 inventory slots**: a backpack with six slots, one slot per hand, two slots on the body. Most items take one slot. Small items can be bundled. **Bulky** items take two slots."),
    sp(1),
    fullnote("Tension by design: the anti-rejection medicine takes 1 slot. Your gun takes 1 slot. Every piece of loot you carry is a slot you cannot use for something else. Inventory management *is* the resource pressure alongside money."),
    sp(2),
    p("**A character with a full inventory (all 10 slots occupied) is reduced to 0 HP.** You cannot carry more than your inventory allows."),
    sp(3),
    h2("4. Trackers"),
    T(["Tracker","Start","Meaning"],
      [["Loyalty","5","Trust with the Division. Neither hero nor traitor."],
       ["Corruption","0","Depth in Zhou's network. Clean, for now."],
       ["Certificates","0","Black market currency. 1 cert = ~$1,000."],
       ["Debt","-$500","The Division advances training costs. Welcome to debt."],
       ["Temporal Quirks","0","Permanent mutations. Limit 5. At 6th, you become an echo."],
       ["Tier","Recruit","Affects pay only: Recruit $800, Agent $1,200, Veteran $1,800."]],
      [FW*0.24, FW*0.14, FW*0.62], full=True),
    sp(2),
    fullnote("**Critical:** Anti-rejection medicine ($250/week) is not optional. Missing a dose makes you **Deprived** (cannot recover HP or attributes) and your WIL degrades by 1 per week."),
    npb(), pb(),
    ]

    # Traits section
    s += [h2("5. Traits"),
    p("Roll on each table to flesh out your character."),
    sp(2),
    T(["d10","Physique"],
      [["1","Athletic"],["2","Brawny"],["3","Gaunt"],["4","Lanky"],["5","Wiry"],
       ["6","Scrawny"],["7","Short"],["8","Scarred"],["9","Stocky"],["10","Towering"]],
      [CW*0.18, CW*0.82]),
    sp(2),
    T(["d10","Face"],
      [["1","Bony"],["2","Broken nose"],["3","Chiseled"],["4","Exhausted"],["5","Pale"],
       ["6","Weathered"],["7","Rat-like"],["8","Sharp"],["9","Square"],["10","Sunken eyes"]],
      [CW*0.18, CW*0.82]),
    sp(2),
    T(["d10","Speech"],
      [["1","Blunt"],["2","Mumbling"],["3","Clipped"],["4","Droning"],["5","Flat"],
       ["6","Gravelly"],["7","Precise"],["8","Raspy"],["9","Stuttering"],["10","Whispery"]],
      [CW*0.18, CW*0.82]),
    sp(2),
    T(["d10","Vice"],
      [["1","Gambling"],["2","Drinking"],["3","Drugs"],["4","Lying"],["5","Violence"],
       ["6","Paranoia"],["7","Rage"],["8","Vanity"],["9","Greed"],["10","Lust"]],
      [CW*0.18, CW*0.82]),
    sp(2),
    T(["d10","Virtue"],
      [["1","Cautious"],["2","Courageous"],["3","Disciplined"],["4","Honest"],["5","Humble"],
       ["6","Loyal"],["7","Patient"],["8","Merciful"],["9","Resourceful"],["10","Stoic"]],
      [CW*0.18, CW*0.82]),
    sp(3),
    h2("6. Narrative Details"),
    p("Answer each in 1-2 sentences."),
    sp(1),
    b("**Why did you join the Division?** (I owed money to the wrong people. My brother died in a temporal zone. I was unemployed for 8 months.)"),
    b("**What debt or problem keeps you desperate?** (I owe $15,000 to a loan shark. Three months behind on rent. My mother's medicine costs $300 a week.)"),
    b("**One person you care about (alive or dead)?** (My ex-wife Sarah. My mentor Martinez, dead 2 years. Nobody. I burned every bridge.)"),
    sp(2),
    note("Your character sheet is complete. A background that defines who you were. Attributes that define what you can do. Trackers that will show who you become."),
    pb(),
    ]

    # ════════════════════════════════
    # CORE RULES
    # ════════════════════════════════
    s += [h1("Core Rules"), rule(),
    h2("Saves"),
    p("A **save** is a roll to avoid bad outcomes from risky choices. Roll a **d20**. If you roll **equal to or under** the relevant attribute, you succeed. A **1** is always a success. A **20** is always a failure."),
    sp(1),
    p("With **advantage**: roll 2d20 and keep the lower. With **disadvantage**: roll 2d20 and keep the higher."),
    sp(1),
    b("**STR saves:** Resisting poison, enduring pain, forcing a door, absorbing a physical impact."),
    b("**DEX saves:** Dodging an explosion, acting before an enemy, sneaking past guards."),
    b("**WIL saves:** Resisting temporal contamination, seeing through a lie, maintaining composure under interrogation."),
    sp(1),
    note("When no save is needed, the Warden decides based on fiction. If your background as ex-military means you know how to field-strip a weapon, you just do it."),
    sp(3),
    h2("Healing"),
    p("**HP** recovers after a few moments of rest and water. **Attribute damage** (STR, DEX, or WIL loss) requires a week of rest with medical care. Division medical services take 1 week (3 days at Loyalty 7+). Black market healing is faster but costs $200-$500."),
    sp(1),
    p("A character lacking a crucial need (food, water, rest, medicine) is **Deprived** and cannot recover HP or attributes."),
    sp(3),
    h2("Fatigue"),
    p("Anyone Deprived for more than a day adds **Fatigue** to their inventory, one per day. Each Fatigue occupies one slot and lasts until the character recovers in a safe place. Temporal contamination and certain Quirk effects can also cause Fatigue."),
    sp(3),
    h2("Armor"),
    T(["Protection","Armor","Cost","Notes"],
      [["Light tactical vest (kevlar II)","1","Division issue","Standard"],
       ["Ballistic vest","2","$1,500","Black market, bulky"],
       ["Heavy tactical armor","3","$3,000","Zhou only, bulky"],
       ["Helmet","+1","$200","Stacks with vest (max 3)"]],
      [CW*0.40, CW*0.12, CW*0.20, CW*0.28]),
    sp(1),
    p("No one can have more than **3 Armor** total."),
    sp(3),
    h2("Reactions"),
    p("When PCs encounter an NPC whose reaction is not obvious, the Warden rolls **2d6**:"),
    sp(1),
    T(["2","3-5","6-8","9-11","12"],
      [["Hostile","Wary","Cautious","Cooperative","Helpful"]],
      [CW*0.10, CW*0.16, CW*0.22, CW*0.26, CW*0.26]),
    sp(3),
    h2("Morale"),
    p("Enemies must make a **WIL save** to avoid fleeing when they take their **first casualty** and again when they lose **half their number**. Groups use their leader's WIL. Lone foes save when reduced to 0 HP. Morale does not apply to PCs."),
    pb(),
    ]

    # ════════════════════════════════
    # COMBAT
    # ════════════════════════════════
    s += [h1("Combat"), rule(),
    h2("Rounds & Initiative"),
    p("When timing matters, use **rounds** (roughly 10 seconds). Each character may move up to 40 feet and take **one action** per round."),
    sp(1),
    p("At the start of combat, each PC makes a **DEX save** to act before opponents. PCs who fail lose their first turn. After the first round, turns alternate: PCs then enemies. Special circumstances (ambush, superior position) may let one side act automatically first."),
    sp(3),
    h2("Attacking and Damage"),
    p("**Attacks automatically hit.** The attacker rolls their weapon's damage die and subtracts the target's Armor. The remainder is applied to the target's HP. Unarmed attacks deal **d4** damage."),
    sp(1),
    note("Example: Reyes fires her Glock 17 (d6) at a scavenger (1 Armor). She rolls a 5. Minus 1 Armor = 4 damage to HP."),
    sp(2),
    b("**Multiple attackers (same target):** Roll all damage dice, keep the single highest result."),
    b("**Dual weapons:** Roll both dice, keep the single highest result."),
    b("**Impaired:** Fighting from weakness (restrained, blinded). Roll **d4** regardless of weapon."),
    b("**Enhanced:** Fighting from advantage (point-blank, ambush). Roll **d12** regardless of weapon."),
    b("**Blast:** Affects all targets in the noted area. Roll damage separately for each."),
    sp(3),
    h2("Critical Damage"),
    p("Damage that reduces a target's HP **below zero** applies the remainder to **STR**. The target then makes a **STR save** to avoid critical damage. On failure: they collapse and will die within one hour without aid."),
    sp(1),
    note("Example: Chen has 2 HP. A guard rolls d8 (result: 6). Minus 1 Armor = 5 damage. 2 HP absorbed, 3 goes to STR. Chen fails the STR save. His teammates have one hour."),
    sp(3),
    h2("Attribute Loss"),
    b("**STR 0:** Death."),
    b("**DEX 0:** Paralysis."),
    b("**WIL 0 (contamination):** Temporal echo. Character lost forever."),
    b("**WIL 0 (other):** Catatonia. Requires a week of medical care."),
    sp(3),
    h2("Detachments"),
    p("Large groups fight as a single **detachment**. Critical damage routes them; 0 STR destroys them. Attacks against detachments by individuals are **impaired** (d4, unless blast). Attacks by detachments against individuals are **enhanced** (d12) and deal **blast** damage."),
    sp(3),
    h2("Retreat"),
    p("Running from danger requires a successful **DEX save** and a safe destination to run to."),
    nfull(), pb(),
    h2("Death and Replacement"),
    p("When a character dies, the player creates a new character or takes control of a hireling. The new character joins the party immediately. The Warden and player decide how: a Division replacement, a scavenger who joins, or a prisoner freed during the mission. The new PC starts at Recruit tier with Loyalty 5 and Corruption 0."),
    sp(3),
    h2("Weapons"),
    T(["Weapon","Damage","Cost","Notes"],
      [["Knife, baton, brass knuckles","d6","$50","Concealable"],
       ["Glock 17 (pistol)","d6","Division issue","1 slot"],
       ["Revolver","d6","$300","Reliable, loud"],
       ["Shotgun","d8","$500","Bulky, devastating close range"],
       ["Submachine gun","d6","$800","Blast (close range), bulky"],
       ["Assault rifle","d8","$1,500","Bulky, black market only"],
       ["Sniper rifle","d10","$2,500","Enhanced at range, impaired close"],
       ["Molotov cocktail","d6","$10","Blast, fire, one use"],
       ["Frag grenade","d8","$200","Blast, one use"],
       ["Stun grenade","0","$150","DEX save or lose next turn"],
       ["Taser","d4","$100","STR save or incapacitated"],
       ["Unarmed","d4","Free","Always available"]],
      [FW*0.36, FW*0.11, FW*0.15, FW*0.38], full=True),
    sp(2),
    fullnote("**Ammunition:** Do not track individual bullets. After any intense firefight, roll a **d6 usage die**. On a 1: out entirely. On a 2: running low, resupply needed ($50 per reload)."),
    sp(3),
    h2("Scars"),
    p("When damage reduces HP to **exactly 0**, roll on the Scars table (d12, based on total damage taken). Results range from lasting wounds to mortal injuries."),
    sp(1),
    T(["Roll","Scar"],
      [["1","**Lasting Scar.** Roll d6 for location."],
       ["2","**Rattling Blow.** Disoriented and shaken. Roll d6 vs max HP."],
       ["3","**Winded.** Deprived until rest. Roll d6, add to max HP."],
       ["4","**Broken Limb.** Once mended, roll 2d6 vs max HP."],
       ["5","**Infected.** On recovery, roll 2d6 vs max HP."],
       ["6","**Head Wound.** Roll d6: 1-2 STR, 3-4 DEX, 5-6 WIL affected."],
       ["7","**Hamstrung.** Can barely move. Roll 3d6 vs max DEX on recovery."],
       ["8","**Deafened.** WIL save: pass = max WIL +d4."],
       ["9","**Concussed.** Roll 3d6 vs max WIL."],
       ["10","**Dismembered.** WIL save: pass = max WIL +d6."],
       ["11","**Mortal Wound.** Die in one hour unless healed."],
       ["12","**Doomed.** Next critical damage save failure = hideous death."]],
      [FW*0.10, FW*0.90], full=True),
    npb(), pb(),
    ]

    # ════════════════════════════════
    # ECONOMY
    # ════════════════════════════════
    s += [h1("The Economy of Desperation"), rule(),
    note("The economic system is designed to be **unsustainable**. This is not a bug. It is the beating heart of the game. The Division pays you *just enough* to survive. But life costs more. And when you are desperate, Zhou is waiting."),
    sp(2),
    h2("Division Base Pay"),
    T(["Tier","Weekly Pay","Notes"],
      [["Recruit","$800/week","The bare minimum. You start here."],
       ["Agent","$1,200/week","Confirmed agent. Slightly better."],
       ["Veteran","$1,800/week","Finally breathing. But debts remain."]],
      [CW*0.25, CW*0.27, CW*0.48]),
    sp(2),
    p("**Mission bonuses:** Guaranteed base: +$50 per completed mission (not subject to deductions). Successful completion: +$200. Secondary objective: +$100. No civilian casualties: +$150. Artifact recovery: +$300-1,000."),
    sp(1),
    note("Bonuses (except the guaranteed $50) are subject to administrative deductions. A $500 bonus becomes $350 after deductions. This fuels resentment toward the Division."),
    sp(3),
    h2("Mandatory Weekly Expenses"),
    T(["Expense","Cost/Week","If you skip"],
      [["Rent","$500","Eviction in 4 weeks"],
       ["Food and necessities","$150","Deprived, cannot recover HP"],
       ["Anti-rejection medicine","$250","Deprived, WIL degrades 1/week"],
       ["**TOTAL**","**$900**",""]],
      [CW*0.40, CW*0.22, CW*0.38]),
    sp(2),
    p("**Guaranteed deficit at Recruit tier: -$50 per week** (pay $800 + guaranteed $50 bonus - expenses $900 = -$50). Miss the mission success bonus and the deficit doubles."),
    sp(3),
    h2("Weekly Cash Flow by Tier"),
    T(["Tier","Pay","Expenses","Balance","After 10 Weeks"],
      [["Recruit","$800","$900","**-$100**","-$1,000 (desperate)"],
       ["Agent","$1,200","$900","**+$300**","Paying off Recruit debts"],
       ["Veteran","$1,800","$900","**+$900**","Comfortable (damage is done)"]],
      [CW*0.20, CW*0.15, CW*0.18, CW*0.18, CW*0.29]),
    sp(1),
    note("At Agent and Veteran tiers, expenses may rise to $1,100-1,300 due to lifestyle inflation, Quirk-related medical costs, and Zhou's voluntary payments for past favors."),
    sp(3),
    h2("The Black Market: Zhou's Economy"),
    p("Madame Zhou's currency is **certificates** (1 cert = approximately $1,000)."),
    sp(1),
    b("**Earning:** Sell artifacts (1-15 certs), sell Division intel (2-10 certs), complete side jobs (1-5 certs)."),
    b("**Spending:** Ballistic vest (2 certs), heavy containment suit (3 certs), assault weapons (1-3 certs), fake IDs (1 cert), temporal surgery to remove a Quirk (50 certs), safe house 1 month (3 certs), bribes (1-3 certs)."),
    b("**Every transaction with Zhou costs +1 or +2 Corruption.**"),
    sp(3),
    h2("The Debt Trap"),
    p("**Starting debt: -$500.** Grows each week at Recruit tier. **Interest: 5% per week on negative balance.** The debt accelerates. Monthly clemency of $300 available on request, but costs -1 Loyalty."),
    sp(1),
    note("Week 1: Pay $800, expenses $900, bonus $50. Balance: -$50. Debt: -$550. Week 3: Mission fails. Only guaranteed $50. Broken phone: -$50. Balance: -$100. Debt: -$560. Week 4: Zhou offers $2,000 for a small piece of information. Rent is due. Medicine runs out in 3 days. *What do you do?*"),
    sp(3),
    h2("What Happens When You Don't Pay"),
    b("**Rent arrears (3 weeks):** Eviction starts. Social interactions are impaired. Sleep in Division barracks (Loyalty 6+) or Zhou's safe house (+1 Corruption)."),
    b("**No food (2 weeks):** Deprived. After 4 weeks: -2 STR permanent."),
    b("**No medicine (1 week):** Deprived. WIL degrades 1/week. After 2 weeks: WIL save at disadvantage or gain new Quirk."),
    sp(3),
    h2("Side Gigs"),
    nfull(), pb(),
    T(["Side Gig","Pay","Risk","Corruption"],
      [["Security guard","$100-200/week","Low","None"],
       ["Manual labor","$80-150/week","Low","None"],
       ["Division Consulting","$150-250/week","None","None (Loyalty 5+)"],
       ["Temporal info market","$200-600/info","WIL save","None direct"],
       ["Gambling","-$200 to +$400","Medium","+1 after 3 wins"],
       ["Street fighting","$200-500/fight","High (d6 STR)","None"],
       ["Drug courier","$300-600/run","High","+1 Corruption"],
       ["Info sale to Zhou","$500-2,000","Very high","+2 Corruption"]],
      [FW*0.27, FW*0.20, FW*0.18, FW*0.35], full=True),
    sp(2),
    fullnote("**Division Consulting (Loyalty 5+ only):** Pay $150-250/week. Costs 2 full days of downtime. During those days, no other actions are possible. Consulting replaces mission performance bonuses for that week. Makes the honest path survivable, not comfortable."),
    sp(2),
    fullnote("**Temporal Information Market:** Researchers and journalists pay for intelligence on temporal zones. After each sale, make a WIL save. On failure: the information reaches the Division (-2 Loyalty). No Corruption cost, no safety."),
    sp(2),
    fullnote("**Gambling:** Three consecutive weeks of wins trigger +1 Corruption (compulsive behavior, visible to NPCs). The Corruption reflects deteriorating self-control."),
    sp(3),
    h2("Unexpected Weekly Expenses"),
    p("Each week the Warden rolls **d6**:"),
    sp(1),
    T(["d6","Expense","Cost"],
      [["1","Nothing extra this week","$0"],
       ["2","Phone broken, laundry, toiletries","$50"],
       ["3","Transport breakdown (car repair, taxi)","$100"],
       ["4","Medical copay (non-Division injury)","$150"],
       ["5","Equipment replacement (lost or damaged)","$200"],
       ["6","Warden's choice (debt collector, bribe, emergency)","$100-500"]],
      [FW*0.08, FW*0.52, FW*0.40], full=True),
    sp(3),
    h2("Mission Absence"),
    T(["Consecutive Absences","Consequence"],
      [["1","No consequence. Once."],
       ["2","Rodriguez has an informal chat. Narrative warning."],
       ["3","Formal reprimand. -1 Loyalty."],
       ["4","Disciplinary probation. -2 Loyalty. Pay halved."],
       ["5+","Terminated. No pay, no housing, no Division protection."]],
      [FW*0.30, FW*0.70], full=True),
    sp(3),
    h2("Zhou's Contact Thresholds"),
    T(["PC's Total Debt","Zhou's Offer"],
      [["-$700+","First contact: $1,500 for a simple courier job."],
       ["-$1,300+","Second offer: $2,000-3,000 for Division intel."],
       ["-$2,200+","Third offer: $5,000 for sabotage or theft."],
       ["-$4,000+","Final offer: Full employment with Zhou. All debts cleared. Total corruption."]],
      [FW*0.22, FW*0.78], full=True),
    sp(3),
    h2("Tier Advancement"),
    p("**Recruit to Agent:** Complete 5 successful missions AND Loyalty 4+."),
    sp(1),
    p("**Agent to Veteran:** Complete a significant narrative milestone (Warden decides): survive a Black Zone, expose a mole, recover a critical artifact."),
    sp(1),
    note("Tiers only affect pay and narrative standing. Your character does not get mechanically stronger. They get financially stable, which in this game is the same thing."),
    npb(), pb(),
    ]

    # ════════════════════════════════
    # LOYALTY & CORRUPTION
    # ════════════════════════════════
    s += [h1("Loyalty & Corruption"), rule(),
    p("Loyalty and Corruption are two independent trackers, scale 0-10. They are **not** opposites. You can have both high. You can have both low."),
    sp(1),
    b("**Loyalty** measures how much the Division trusts you."),
    b("**Corruption** measures how deep you are in Zhou's network."),
    sp(1),
    note("Loyalty is not 'good.' Corruption is not 'evil.' They are measures of allegiance. The system records. It does not judge."),
    sp(3),
    h2("The Loyalty Scale"),
    T(["Value","Status","Consequences"],
      [["0-1","Traitor","Division hunting you. Shoot-on-sight."],
       ["2-3","Suspect","Constant surveillance. Colleagues avoid you."],
       ["4-6","Neutral","Standard agent. No special treatment."],
       ["7-8","Trusted","Better missions (+$200). Priority medics (3 days instead of 1 week)."],
       ["9-10","Division Hero","Pay +50%. Military-grade equipment free."]],
      [CW*0.14, CW*0.22, CW*0.64]),
    sp(3),
    h2("The Corruption Scale"),
    T(["Value","Status","Consequences"],
      [["0","Clean","Zhou does not know your name."],
       ["1-2","Dabbling","First offers arrive. Small favors."],
       ["3","Asset","Zhou shifts from offers to requests."],
       ["4","Entangled","Regular customer. Refusing has costs."],
       ["5","Watched","The Division suspects. See below."],
       ["6","Deep In","Automatic weekly offers. Side jobs expected."],
       ["7","Leveraged","Zhou has documentation on you. See below."],
       ["8","Committed","Zhou provides everything. Hard to exit."],
       ["9-10","Zhou's Property","You are not free. Arrest order imminent."]],
      [CW*0.12, CW*0.22, CW*0.66]),
    sp(3),
    h2("Corruption Threshold: 3"),
    p("Zhou considers the agent a confirmed asset. She stops making offers and starts making **requests**. The first is small: surveil a location for one night, carry a sealed package. Pay is $300. Refusal costs $500 in withheld past payments."),
    sp(1),
    note("This is the moment where the agent realizes the relationship has changed. They are no longer a client. They are a resource."),
    sp(3),
    h2("Corruption Threshold: 5"),
    p("The Division has enough to act on suspicion, not enough for evidence. **A second agent appears on every Division mission.** Professional, competent, says little. The agent does not know with certainty whether this person reports to Hayes. Every grey action in the field is now a gamble."),
    sp(1),
    note("The Warden should play this ambiguity honestly. Sometimes the second agent is just a second agent. Sometimes they report back. Players should never be able to reliably determine which. The uncertainty is the mechanic."),
    sp(3),
    h2("Corruption Threshold: 7"),
    p("Zhou possesses documentation: a recording, a document, a witness. She does not use it immediately. She uses the *fact* that she has it. Each time the agent refuses a job, the Warden rolls d6. On 1-2, Zhou makes the threat explicit. The agent must make a **WIL save** or be **Deprived for one week** from stress."),
    sp(3),
    h2("Instability"),
    p("When **|Loyalty - Corruption| is 2 or less**, you enter **INSTABILITY**."),
    sp(1),
    b("**Social Penalty.** All social interactions are impaired."),
    b("**Weekly Suspicion.** Each downtime week, roll d20: 1-5 Hayes suspects (WIL save or -2 Loyalty), 6-10 Zhou doubts (next mission is a loyalty test), 11-15 tension grows, 16-20 no consequence."),
    b("**Benefit Lock.** Cannot receive Loyalty 8+ or Corruption 8+ benefits."),
    b("**Forced Resolution.** After 3 consecutive unstable weeks, the Warden triggers a narrative event forcing a choice."),
    sp(2),
    note("You want to play both sides? Both sides will be watching."),
    pb(),
    ]

    # ════════════════════════════════
    # TEMPORAL CONTAMINATION
    # ════════════════════════════════
    s += [h1("Temporal Contamination"), rule(),
    p("**Time corrodes you. Slowly. Permanently.** Every 6 hours in a temporal zone, make a **WIL save**. This represents your mental and biological resistance to temporal forces."),
    sp(3),
    h2("The Contamination Save"),
    p("On a failed save, roll the zone's damage die for WIL damage. The temporal protection suit reduces damage by 1 (minimum 1). A heavy containment suit (black market, $2,000, bulky) reduces by 2. **Damage cannot exceed half your current WIL, rounded up.** This prevents the death spiral from accelerating uncontrollably."),
    sp(1),
    note("Example: Jin has WIL 13. He fails in an Orange Zone. Rolls d4: 3. Suit absorbs 1. Net damage: 2. WIL drops to 11. At WIL 2, the cap means he can never take more than 1 damage per check."),
    sp(2),
    p("This creates a gradual decline, not a sudden crash. The spiral is real but it decelerates. Characters degrade over sessions, not in a single bad run."),
    sp(3),
    h2("Quirk Acquisition"),
    p("When contamination damage (after suit and cap) is **3 or more**, roll d12 on the Quirk table. Minor exposure (1-2 damage) erodes willpower without mutating. Only significant exposure triggers a Quirk. If you already have that Quirk, reroll. At 5 Quirks, gaining a sixth means you become a **temporal echo**: character lost."),
    sp(3),
    h2("Zone Intensity"),
    T(["Zone","Frequency","Damage","Example"],
      [["Stable (green)","No checks","None","Division HQ, Vegas Strip"],
       ["Low (yellow)","Every 8 hours","d4","Outskirts, buffer zones"],
       ["Standard (orange)","Every 6 hours","d4","Most mission areas"],
       ["High (red)","Every 3 hours","d4","Deep zones, Oculus sites"],
       ["Critical (black)","Every hour","d6","Oculus core, temporal rifts"]],
      [CW*0.22, CW*0.26, CW*0.14, CW*0.38]),
    sp(3),
    h2("Recovery"),
    b("**Division treatment** (1 week; 3 days at Loyalty 7+): restores d6 WIL (d8 at Loyalty 7+)."),
    b("**Black market temporal therapy** ($500/session): restores d6 WIL, takes 2 days."),
    b("**Anti-rejection medicine** ($250/week): prevents WIL from degrading further between missions."),
    sp(2),
    note("WIL damage from contamination does *not* heal normally. Time zones change your biology, not just injure it. A bullet wound heals. A temporal mutation does not."),
    sp(3),
    h2("Temporal Echoes"),
    p("When WIL reaches 0 from contamination, or when a character acquires their 6th Quirk, they become a **temporal echo**. This is permanent and irreversible. The character becomes an NPC controlled by the Warden: hostile to living beings, existing simultaneously across multiple time periods, retaining fragmented memories of their former life."),
    sp(1),
    p("**For the player:** Create a new character. The replacement joins the party immediately. The Warden may use your echo as a future encounter."),
    sp(1),
    note("What makes this different from death: death is quick. Becoming an echo is a slow, visible process. The other players watch as your character accumulates Quirks. They know what is coming. The question is whether they can finish the campaign before it happens."),
    ]

    # ════════════════════════════════
    # TEMPORAL QUIRKS
    # ════════════════════════════════
    s += [nfull(), pb(),
    h1("Temporal Quirks"), rule(),
    p("Temporal Quirks are permanent mutations caused by contamination exposure. They are not powers. They are **biological scars**: your body and mind breaking under the weight of too many overlapping timelines. **Limit: 5 different Quirks.** At the 6th, you become an echo."),
    sp(3),
    h2("Quirk Table (roll d12)"),
    T(["d12","Quirk","Effect Summary"],
      [["1","Accelerated Aging","Age 1d10 years instantly"],
       ["2","Memories of Unlived Lives","Paralyzing flashbacks, always lose initiative"],
       ["3","Vision of Future Deaths","See how people die, +1 Armor, social interactions impaired"],
       ["4","Partial Phase Shift","Body part becomes translucent, passes through walls"],
       ["5","Vocal Echo","Voice overlaps in 3 time streams, verbal stealth impossible"],
       ["6","Inverse Scars","Future wounds appear before they happen"],
       ["7","Cursed Prescience","See 10 seconds ahead, always win initiative, cannot change outcome"],
       ["8","Delayed Shadow","Shadow moves 3 seconds behind"],
       ["9","Personal Loop","Every 10 min, repeat same 6 involuntary words"],
       ["10","Temporal Fragmentation","Occasionally vanish for 1d6 seconds, +1 Armor"],
       ["11","Eyes of the Past","See past events overlaid on present, enhanced investigation"],
       ["12","Spontaneous Rewind","Occasionally rewind 1d6 seconds, 1 voluntary rewind per session"]],
      [FW*0.10, FW*0.30, FW*0.60], full=True),
    npb(),
    h2("Quirk Descriptions"),
    h3("[1] Accelerated Aging"),
    p("You age 1d10 years instantly. No immediate penalty. At 60+ years total: -1 STR, -1 DEX. At 70+: -2 STR, -2 DEX. At 80+: mandatory retirement or imminent death."),
    p("*At the table: documents no longer match your face. Relationships collapse.*"),
    sp(2),
    h3("[2] Memories of Unlived Lives"),
    p("You always **lose initiative** (automatically fail DEX save in round 1). Once per session: 'I remember this from another life' (Warden gives a clue or temporary competence for 1 scene). On important dilemmas: WIL save or freeze for 1 round."),
    p("*At the table: paralyzing flashbacks, identity confusion, constant nightmares.*"),
    sp(2),
    h3("[3] Vision of Future Deaths"),
    p("**+1 Armor** permanently (you see attacks before they land). **All social interactions are impaired** (people see death in your eyes). Once per session: the Warden reveals approximately how an NPC will die."),
    p("*At the table: children cry, animals flee, every conversation is a memento mori.*"),
    sp(2),
    h3("[4] Partial Phase Shift"),
    p("One body part (roll d6: 1-2 arm, 3-4 leg, 5 torso, 6 head) becomes translucent and semi-intangible. The phased part passes through walls (WIL save to control). Cannot hold objects with it. Arm: attacks with that hand are impaired. Head: social interactions impaired. Torso: +1 permanent Fatigue."),
    p("*At the table: visibly mutated. Impossible to hide.*"),
    sp(2),
    h3("[5] Vocal Echo"),
    p("Your voice overlaps in 3 time streams: 1 second before, now, 1 second after. Verbal stealth impossible. Enhanced intimidation against anyone hearing you for the first time. Once per session: someone hears your words 10 seconds early."),
    p("*At the table: phone calls impossible. Recorders corrupt.*"),
    sp(2),
    h3("[6] Inverse Scars"),
    p("Wounds you have not yet received appear on your body. When hit where a scar matches: STR save to take half damage. Each week, roll d6: on a 1, a scar 'realizes' (d6 spontaneous STR damage)."),
    p("*At the table: a mosaic of impossible wounds. Anxious waiting for each one to arrive.*"),
    sp(2),
    h3("[7] Cursed Prescience"),
    p("Always win initiative (automatic DEX save success). Never surprised. In combat, describe what the enemy does next round. Curse: when you fail a critical damage save, you must describe having seen it coming."),
    p("*At the table: answer before questions. Watch deaths approach helplessly.*"),
    sp(2),
    h3("[8] Delayed Shadow"),
    p("Your shadow moves 3 seconds behind your body. Stealth is impaired in light. Once per session: leave your shadow as a decoy, fooling enemies for 1 round."),
    p("*At the table: photos and video show your shadow in the wrong place.*"),
    sp(2),
    h3("[9] Personal Loop"),
    p("Every 10 minutes, you involuntarily repeat the same 6 words. The loop ruins stealth operations. Benefit: perfect internal timer. Roll d6 or choose with the Warden for the specific words."),
    p("*At the table: serious conversations interrupted mid-sentence. Some NPCs think the words are prophecies.*"),
    sp(2),
    h3("[10] Temporal Fragmentation"),
    p("Every hour (game time), roll d6: on a 1, you vanish for 1d6 seconds. In combat: lose your turn but cannot be targeted. **+1 Armor** permanently (slightly out of focus)."),
    p("*At the table: cannot drive. Intimate relationships become impossible.*"),
    sp(2),
    h3("[11] Eyes of the Past"),
    p("You see past events overlaid on the present: 10, 50, 100 years ago. Enhanced investigation in any location. Impaired perception of the present. Always lose initiative in unfamiliar locations. Once per session: concentrate for 10 min + WIL save to visually rewind a location up to 1 week."),
    p("*At the table: every place is crowded with temporal ghosts.*"),
    sp(2),
    h3("[12] Spontaneous Rewind"),
    p("Every hour, roll d6: on a 1, you rewind 1d6 seconds. In combat: lose your turn but can change your action in the second iteration. Once per session: voluntary rewind to undo a mistake (max 6 seconds). Others do not remember the first loop."),
    p("*At the table: constant deja vu. Allies learn to wait for the loop to end.*"),
    sp(3),
    h2("Removing Quirks"),
    b("**Experimental temporal surgery:** $50,000 (50 certs). 3 weeks. WIL save. Success: removed. Failure: gain new Quirk. Either way: +2 Corruption."),
    b("**Division protocol (Loyalty 8+):** Free. 1 month. WIL save with advantage. Success: removed. Failure: desk duty or forced leave."),
    b("**Acceptance:** Free. The Quirk stays. The Warden may reduce social penalties if you roleplay the acceptance with conviction."),
    pb(),
    ]

    # ════════════════════════════════
    # EXPLORATION & TIME
    # ════════════════════════════════
    s += [h1("Exploration & Time"), rule(),
    h2("Time Structure"),
    b("**Rounds** (10 seconds): Combat and tense sequences. Move 40 feet and take one action per round."),
    b("**Turns** (10 minutes): Exploration of temporal zones. Searching a room, picking a lock, administering aid."),
    b("**Weeks**: The fundamental unit of campaign time. One mission phase (1-3 days in zone), downtime (rest, side gigs), and administrative time (pay, expenses, tracker updates)."),
    sp(3),
    h2("Exploration Procedure"),
    p("When the party enters a temporal zone, the Warden describes the environment. Players declare their actions. The Warden determines results, calling for saves only when the outcome is uncertain and the stakes are meaningful."),
    sp(1),
    p("**Every 3 turns (30 minutes of exploration)**, the Warden rolls on the encounter table or advances the zone's clock. Temporal zones are active: anomalies shift, echoes patrol, scavengers hunt."),
    sp(2),
    T(["d6","Encounter"],
      [["1","**Quiet.** Tension builds but nothing happens. Describe an unsettling sensory detail."],
       ["2","**Environmental hazard.** Structural collapse, gravity anomaly, or temporal rift. DEX or WIL save."],
       ["3","**Signs of passage.** Footprints, discarded equipment, blood trail. Someone else is here."],
       ["4","**Temporal echo** (hostile). 4 HP, 8 STR, 12 DEX, 6 WIL, temporal claw (d6)."],
       ["5","**Scavengers** (d4). Reaction roll. Armed with knives (d6) and pistols (d6)."],
       ["6","**Temporal event.** Time stutters. Everyone makes a WIL save or loses their next turn."]],
      [CW*0.10, CW*0.90]),
    sp(3),
    h2("Hazards"),
    b("**Temporal rifts:** Patches of unstable time. DEX save to avoid. Failure may teleport you elsewhere or damage your gear."),
    b("**Echo patrols:** Former agents who became temporal echoes. Hostile and unpredictable."),
    b("**Scavengers:** Unaffiliated humans entering zones illegally. Reaction roll determines attitude."),
    b("**Structural collapse:** Buildings in temporal zones decay at different rates. DEX save to react."),
    b("**Light and darkness:** Working in darkness means all actions are **impaired**. Flashlights last 3 hours (1 slot)."),
    sp(3),
    h2("Rest in the Zone"),
    p("Resting in a temporal zone restores HP but does **not** stop the contamination clock. Every 6 hours of presence counts, whether you are moving or resting. Safe rooms (rare, marked on Division maps) reduce checks to every 12 hours."),
    pb(),
    ]

    # ════════════════════════════════
    # TEMPORAL RELICS
    # ════════════════════════════════
    s += [h1("Temporal Relics"), rule(),
    p("Temporal relics are artifacts recovered from the zones. They are not weapons or tools in the ordinary sense. They are fragments of broken time made solid. Each bends reality in a specific way, costs something to use, and is worth a fortune on the black market. Relics take up 1 inventory slot unless noted."),
    sp(3),
    p("**Stillwatch.** *3 charges.* A cracked pocket watch that freezes time in a 10-foot radius for 6 seconds. Everything inside stops: bullets, people, falling debris. You are frozen too. Useful for stopping a bleeding wound long enough to apply pressure. *Recharge: submerge in running water for 1 hour.*"),
    sp(2),
    p("**Rewind Syringe.** *1 charge.* A glass syringe of shimmering blue liquid. Inject into yourself or a willing target. The target's body resets to its state 6 hours ago: wounds heal (restore all HP and STR), contamination damage is undone, but memories of those 6 hours are lost completely. One use. Worth $8,000 to Zhou. The Division wants it for research."),
    sp(2),
    p("**Echo Lantern.** *3 charges.* A battered oil lantern revealing temporal echoes within 50 feet, even invisible or phased ones. Also reveals hidden temporal rifts. Does not make echoes hostile. *Recharge: leave lit in complete darkness for 24 hours.*"),
    sp(2),
    p("**Gravity Glove.** *2 charges.* Touch an object (up to 200 lbs). For one minute, its gravity reverses: it falls upward. Does not work on living creatures. *Recharge: drop the glove from at least 30 feet.*"),
    sp(2),
    p("**Chrono Grenade.** *1 charge.* Looks like a frag grenade with an amber crystal core. On detonation, everything in a 20-foot radius ages 10 years: metal rusts, wood rots, concrete crumbles. Living creatures: STR save or take d8 STR damage. Does not affect temporal echoes. Worth $3,000 to Zhou. *Cannot be recharged.*"),
    sp(2),
    p("**The Listener.** *3 charges.* A small earpiece of bone-white material. When activated, you hear conversations from your current location in the past 72 hours. Choose which window to listen to. Useful for intelligence, discovering missing squads, or learning what Zhou discussed in a room she used recently. *Recharge: 1 hour of complete silence.*"),
    sp(2),
    p("**Phase Ring.** *2 charges.* A plain iron ring. When worn and activated, your hand becomes intangible for 10 seconds. Reach through walls, locked doors, or sealed containers to pull one object through. Cannot reach more than 1 foot of material. If the charge runs out while your hand is inside a solid object: d10 STR damage. *Recharge: leave inside a locked container overnight.*"),
    sp(2),
    p("**Deja Vu Engine.** *1 charge.* A fist-sized brass device covered in tiny gears. Rewinds the last 10 seconds for everyone in a 30-foot radius. Everyone except the user forgets those 10 seconds happened. Effectively a save point: if a fight goes badly, activate and try a different approach. *Recharge: the user must experience a genuine surprise while carrying it.*"),
    sp(2),
    p("**Temporal Compass.** *No charges (passive).* A compass whose needle points toward the nearest Oculus fragment instead of north. Pocket-sized (0 slots). Worth $5,000 to Zhou, $2,000 to the Division. Warning: carrying it in a Red Zone draws echoes. Encounter checks are rolled with disadvantage."),
    sp(2),
    p("**Dr. Voss's Injector.** *3 charges.* Labeled TEMPORAL STABILIZATION, PROTOTYPE, NOT FOR HUMAN USE. Reduces contamination damage by 2 (stacks with suit) for 6 hours after injection. Side effect: vivid hallucinations for 1 hour after the effect ends (WIL save or lose next turn during hallucinations). *Recharge: refill with 1 week of anti-rejection medicine ($250).*"),
    sp(2),
    p("**The Black Mirror.** *1 charge.* A hand mirror with a dark metal frame. Look into it and speak a person's name. Shows that person's current location and situation for 30 seconds. Works across any distance. Does not work on echoes or the dead. Zhou uses one to monitor her agents. *Recharge: break the mirror. It reassembles itself over 7 days.*"),
    sp(2),
    p("**Anchor Spike.** *2 charges.* A foot-long iron spike covered in etched symbols. Drive it into the ground: for the next hour, temporal anomalies within 20 feet are suppressed. Contamination checks still apply. Useful for safe camps in Red Zones. If an echo touches the spike, it becomes fully tangible and targetable for 1 round. *Recharge: leave at the epicenter of a temporal event for 1 hour.*"),
    pb(),
    ]

    # ════════════════════════════════
    # SETTING: LAS VEGAS 2080
    # ════════════════════════════════
    s += [h1("Las Vegas, 2080"), rule(),
    h2("The Oculus Event (2025)"),
    p("August 15, 2025. 3:47 AM. A US government experiment code-named Project Oculus, an attempt to manipulate time for military applications, went catastrophically out of control. The secret laboratory under the Nevada desert imploded, not outward but *inward*, through time itself. The epicenter: the Luxor Hotel, Las Vegas Strip."),
    sp(1),
    b("**0-5 km from the epicenter (the Strip):** Temporal annihilation. The Luxor now exists simultaneously as itself in 1920, 1950, 2025, and 2080."),
    b("**5-20 km (downtown):** Severe instability. Buildings jump between eras. People age or de-age randomly."),
    b("**20-50 km (outskirts):** Minor but persistent anomalies. Safe to inhabit but unsettling."),
    sp(1),
    p("Estimated deaths: 400,000 in the first week. Another 200,000 in the following five years from contamination effects."),
    sp(3),
    h2("City Geography (2080)"),
    h3("Red Zone: The Epicenter (0-5 km)"),
    p("**The Strip and the Luxor.** Completely temporally unstable. Forbidden to civilians. WIL save every 3 hours, d4 damage. Zero permanent population. Only temporary recovery teams. The greatest treasures are here."),
    sp(2),
    h3("Yellow Zone: The Intermediate Ring (5-20 km)"),
    p("**Downtown and old neighborhoods.** Unstable but habitable with precautions. Permitted with Division badge or temporary pass ($500/day). WIL save every 8 hours, d4. Population: approximately 50,000. Division workers, black market merchants, desperate people with nowhere else to go."),
    sp(2),
    h3("Green Zone: The Safe Outskirts (20-50 km)"),
    p("**The stabilized suburbs.** Almost normal life. No pass needed. No contamination. Population: approximately 300,000. **This is where agents live**, working in the red and yellow zones, sleeping in relative safety."),
    sp(3),
    h2("Atmosphere and Tone"),
    p("Vegas is a city of violent contrasts: extreme wealth against desperate poverty, futuristic technology against ruins of the past, the Division's rigid legality against the black market's anarchy, hope (is stabilization possible?) against nihilism (is collapse inevitable?)."),
    sp(1),
    note("\"Vegas was never an honest city. But at least before, the rules were clear. Now? Time itself is rigged.\""),
    sp(2),
    p("*Visual inspirations: Blade Runner 2049 (decay, contrasts), Fallout New Vegas (post-apocalyptic desert, abandoned casinos), The Expanse (dirty realism, grey factions), Dark on Netflix (temporal loops, consequences of choices).*"),
    sp(3),
    h2("The Temporal Division"),
    p("**Structure:** Director Hayes (executive), squad captains (tactical, coordinate 5-10 agents), field agents (you, enter zones, recover artifacts, survive), support staff (analysts, medics, techs, never enter dangerous zones)."),
    sp(1),
    p("**Philosophy:** 'Stabilize, contain, recover.' Officially, the Division protects the world. Unofficially, it is a government bureaucracy that underpays you, sends you on suicide missions, and expects blind loyalty. Headquarters: the former Aria Casino, 35 km from the epicenter."),
    sp(3),
    h2("Madame Zhou and the Black Market"),
    p("**Madame Zhou.** A woman of about 60 (she looks 40, illegal temporal surgery). Elegant, ruthless, pragmatic. Built a criminal empire on the ruins of Vegas. The Crimson Palace, a former hotel in downtown, is her fortress. Nobody enters without invitation."),
    sp(1),
    p("She controls 80% of illegal temporal artifact trade, has at least 30 Division agents on her payroll, and 200+ armed mercenaries as guards. She knows everything about everyone. She is patient. She uses you, then she waits to see what you become."),
    sp(1),
    p("**Her secret goal:** Access to the original Project Oculus files in the Division's basement archives. She believes she can use that technology to reset the disaster, or to create a monopoly on time itself."),
    pb(),
    ]

    # ════════════════════════════════
    # KEY NPCs
    # ════════════════════════════════
    s += [h1("Key NPCs"), rule(),
    h2("Director Elena Hayes"),
    statblock("6 HP, 8 STR, 10 DEX, 16 WIL, concealed pistol (d6)"),
    p("52 years old. Pragmatic, cold, efficient. Believes in the mission but is cynical about bureaucracy. Sees PCs as necessary tools. Respects the loyal. Eliminates the corrupt."),
    sp(1),
    p("**Secret:** Was present during the Oculus event. Lost her daughter at the epicenter. Works for the Division as penance. One photo on her desk, face down."),
    sp(3),
    h2("Dr. Marcus Chen"),
    statblock("3 HP, 6 STR, 8 DEX, 14 WIL, no weapons"),
    p("38 years old. Head of medical research. Studies contamination. Idealistic, naive, genuinely wants to help. Treats PCs for free if they are kind."),
    sp(1),
    p("**Secret:** Has 3 Quirks himself (aging, memories of unlived lives, phase shift). Destroying himself to find a cure."),
    sp(3),
    h2("Captain 'Ironside' Rodriguez"),
    statblock("8 HP, 1 Armor, 14 STR, 12 DEX, 10 WIL, assault rifle (d8), combat knife (d6)"),
    p("45 years old. Scars everywhere. Missing left eye. 20 years in the Division. Tough, loyal, protective. 'Bring everyone home.' Refused promotion five times. Gruff mentor who covers for your mistakes. If you betray the squad, he kills you personally."),
    sp(3),
    h2("Victor Raines"),
    statblock("6 HP, 1 Armor, 10 STR, 12 DEX, 14 WIL, concealed pistol (d6)"),
    p("Ex-Division analyst, now independent. Brokers temporal artifacts for private clients: collectors, foreign research institutes, at least one foreign government. Not criminal in the sense of Zhou. Deals in information and artifacts. Pays well."),
    sp(1),
    p("Raines pays 40% more than the Division per completed mission, but no guaranteed floor. Failure pays nothing."),
    sp(1),
    note("Every Raines mission costs -1 Loyalty (every 2 missions) and +1 Corruption (every 2 missions). After 3 missions, Hayes knows. He says nothing, but your assignments become harder: Red zones instead of Orange, tighter timing windows."),
    sp(3),
    h2("'Whisper' Sofia Kovalenko"),
    statblock("6 HP, 1 Armor, 10 STR, 15 DEX, 12 WIL, suppressed pistol (d6), knife (d6)"),
    p("29 years old. Former Division agent at Veteran tier. Left after Hayes let her team die on a 'sacrificial' mission. Now freelance for Zhou. Loyal only to herself. Potential ally or enemy, depending entirely on payment."),
    sp(3),
    h2("Tommy 'Dice' Martinez"),
    statblock("4 HP, 8 STR, 10 DEX, 14 WIL, hidden derringer (d4)"),
    p("52 years old. Manager of the Lucky 38 bar in the Yellow Zone. Friendly, talkative, professional informant. Triple agent: spies for Zhou, Hayes, and anyone who pays. No loyalty. Too useful to eliminate. Sells PCs information ($100-$500). Will not betray you directly but sells your information to others."),
    sp(3),
    h2("'Double' Danny Chen"),
    statblock("4 HP, 8 STR, 8 DEX, 6 WIL"),
    p("Former private investigator, transformed into a Sentient Echo with an identity mutation. Convinced he is the brother, cousin, or relative of anyone he meets. Perfectly remembers every building and street of pre-Oculus Las Vegas, but knows nothing post-2027. Location: Danny's Corner, Fremont Street, stuck in a 1958 loop."),
    sp(3),
    h2("Sergeant Benson 'The Bureaucrat'"),
    statblock("5 HP, 10 STR, 6 DEX, 12 WIL"),
    p("50 years old. Division administrative sergeant. Genuinely believes bureaucracy is the only defense against temporal chaos. Any request requires a specific form. Ways to earn his favors: fill forms perfectly (1 hour downtime + WIL save), find a regulatory loophole, or bribe him with vintage forms from Red Zones. He collects them."),
    sp(1),
    note("Heartbreaking moment: PCs return injured. Benson puts away his forms. 'The forms can wait. Come, I have a first aid kit. Don't get killed out there. The paperwork for agent death is terrible.' He lost his son in the Oculus Event."),
    sp(3),
    h2("'Lucky' Lorenzo Vitale"),
    statblock("3 HP, 8 STR, 12 DEX, 10 WIL"),
    p("30 years old. Former Bellagio croupier. During the Oculus Event, everyone at Ground Zero died. He tripped into an open manhole, emerged 3 days later unscathed. His luck became supernatural and inverted: he cannot perceive danger. Buildings collapse behind him. Best scavenger in Las Vegas."),
    sp(1),
    p("If Lorenzo accompanies PCs in a Red Zone, the group gains **advantage on saves** against temporal hazards (rifts, gravity anomalies, time loops), but not against contamination checks. Also trades artifacts and has intel on Zhou."),
    pb(),
    ]

    # ════════════════════════════════
    # ADVENTURE SITES
    # ════════════════════════════════
    s += [h1("Adventure Sites"), rule(),
    p("Four locations ready to explore. Each has a node map, keyed locations, and embedded dilemmas."),
    sp(3),
    h2("The Crimson Palace (Zhou's HQ)"),
    p("**Zone:** Yellow. WIL save every 8 hours, d4. Why PCs go here: buy from Zhou, sell to Zhou, infiltrate for Hayes, or attend an 'invitation.'"),
    sp(2),
    h3("Rooms"),
    p("**A. The Gate.** Two mercenaries (6 HP, 1 Armor, 12 STR, 10 DEX, 8 WIL, SMG d6 blast) check visitors. No weapons allowed inside. DEX save to palm something small."),
    sp(1),
    p("**B. The Courtyard.** Open-air atrium. Neon signs from three decades flicker simultaneously: 1950s cocktail lounge, 2020s holographic billboard, 2080s price ticker. 20-30 people milling. Reaction roll for anyone you approach."),
    sp(1),
    p("**C. The Market.** Three stalls. Guns (all weapons at 150% standard price). Medicine (anti-rejection at $200, +1 Corruption per purchase). Information (rumors about Division ops, $100-500, WIL save to determine if real or planted)."),
    sp(1),
    p("**D. The Lounge.** Red velvet, dim amber lighting, 1942 jazz on a temporal loop. Where Zhou meets new clients. Tommy Martinez works the bar (info: $200). One table is rigged (DEX save to notice)."),
    sp(1),
    note("Dilemma at the table: a Division agent you recognize is clearly making a deal. Do you report them to Hayes (+1 Loyalty, but the agent will know) or ignore it (leverage for later)?"),
    sp(1),
    p("**E. The Fighting Pit.** Underground cage fights. $200-500 per match. Win 3 fights: Zhou invites you upstairs. Lose: you owe Zhou for medical costs."),
    sp(1),
    p("**F. The Vault.** Behind the market. DEX save to pick the lock (or bribe a guard: $500). Contains 2d6 temporal artifacts worth $1,000-10,000 each. If PCs steal: Zhou finds out within 48 hours. Consequence: mercenaries sent, or she cuts off medicine supply."),
    sp(1),
    p("**G. Zhou's Office.** Top floor suite. Mahogany desk, calligraphy scrolls, a single orchid. Two bodyguards (8 HP, 2 Armor, 14 STR, 12 DEX, 10 WIL, assault rifle d8). Zhou never threatens directly. She offers. She waits. She smiles."),
    sp(1),
    p("**H. Private Rooms.** Sound-dampened. No windows. If you are invited here, the offer is large and the price is permanent. This is where agents sign away their loyalty."),
    sp(3),
    h2("Division HQ (The Aria)"),
    p("**Zone:** Green. No contamination. Why PCs go here: briefings, medical treatment, equipment, internal politics."),
    sp(2),
    h3("Rooms"),
    p("**A. Checkpoint.** Badge scanners, two guards. At Corruption 4+: guards give a longer look. At Corruption 7+: pulled aside for a 'random' inspection (WIL save or they find something compromising)."),
    sp(1),
    p("**B. Lobby.** Sterile, corporate. A wall of photos: 47 agents killed in action. Notice board: mission postings, Benson's announcements, a handwritten note ('If anyone finds my left shoe in the Yellow Zone, it's a size 10. Thanks. Rodriguez')."),
    sp(1),
    p("**C. Armory.** Sergeant Willis. Standard equipment free. Anything beyond standard requires Loyalty 7+ or a form from Benson. Does not contain assault weapons, heavy armor, or explosives."),
    sp(1),
    p("**D. Briefing Room.** Where Hayes assigns missions. The coffee machine has not worked since 2078. Nobody fixes it. It is a running joke and a metaphor."),
    sp(1),
    p("**E. Infirmary.** Dr. Chen's domain. He treats everyone regardless of faction or status. If PCs befriend Chen, he shares contamination research. He is also the only person who can tell a PC exactly how many Quirks they can sustain before echo transformation."),
    sp(1),
    note("Dilemma: Chen asks a PC to volunteer for an experimental anti-contamination treatment. If it works: +1 permanent bonus to WIL contamination saves. If it fails (50/50): gain 1 permanent Fatigue. Chen is honest about the odds."),
    sp(1),
    p("**F. Offices (Floors 2-5).** Rodriguez's office on Floor 3: messy, personal, bottle of whiskey in the drawer. If PCs visit him off-duty, he will warn them about dangerous upcoming missions before the official briefing."),
    sp(1),
    p("**G. Hayes' Office (Floor 6).** Panoramic windows facing the epicenter. The Strip always visible, shimmering and broken. Hayes sits with her back to the view. She does not look at it anymore. This is where promotions happen, ultimatums are delivered, and careers end."),
    sp(1),
    p("**H. Basement (Restricted).** Requires Loyalty 8+ or a stolen access card. Contains: cells for compromised agents, classified archives (heavily redacted mission reports from the first 10 years after Oculus), and the artifact vault with recovered Oculus fragments. The archives contain proof that Hayes authorized 'expendable' missions that killed 14 agents in 2076. Zhou would pay $10,000 for this."),
    sp(3),
    nfull(), pb(),
    h2("The Meridian Hotel (Chicago, 1934)"),
    p("**Zone:** Orange, deteriorating to Red after 4 hours. WIL save every 6 hours initially, every 3 hours after the first 4."),
    sp(2),
    T(["Floors","Era","What's Here"],
      [["Basement","Mixed","Flooded corridors, old casino vault"],
       ["1-2 (Lobby)","1934+2080","4 civilians, reception desk, restaurant"],
       ["3-5 (Service)","1934","Kitchens, laundry, staff quarters"],
       ["6-10","1934","Luxury hotel rooms, ballroom on floor 8"],
       ["11-14","Transitional","Architecture shifts mid-corridor"],
       ["15-24","2080","Empty apartments, gravity anomalies"],
       ["25-26","Mixed","Corridors shift between eras every 10 min"],
       ["27 (Suite 2701)","Frozen","Time nearly stopped. Light bends."],
       ["Roof","2080","Helicopter extraction point"]],
      [FW*0.18, FW*0.18, FW*0.64], full=True),
    sp(2),
    T(["Floors","Danger","Treasure"],
      [["Basement","1 echo in vault, strong currents","Pre-Oculus cash (d6 x $500), gold chips"],
       ["1-2 (Lobby)","Social dilemma: evacuate or leave?","Cash register, guest ledger (historical value)"],
       ["3-5 (Service)","1 temporal ghost (harmless, confusing)","Chef's knife (d6), wine collection ($300)"],
       ["6-10","1 echo on floor 7, time loop on floor 9","Jewelry ($500), temporal device on floor 8"],
       ["11-14","STR save at each era interface or d6 dmg","Anti-rejection cache, 8 weeks supply"],
       ["15-24","2-3 echoes patrol, structural instability","Electronics ($200), Division field notes"],
       ["25-26","Forced contamination check per floor","Oculus fragment shard (class-C, $2,000)"],
       ["27 (Suite 2701)","Zhou's 3 mercenaries inside","The objective: class-A Oculus fragment"],
       ["Roof","Final contamination check, exposed","Extraction point"]],
      [FW*0.18, FW*0.42, FW*0.40], full=True),
    npb(), sp(3),
    h2("The Sunken Strip (Red Zone Crawl)"),
    p("**Zone:** Red. WIL save every 3 hours, d4. Why PCs go here: high-value artifact recovery, missing agent search, or Hayes orders it."),
    sp(2),
    h3("Nodes"),
    p("**A. Perimeter.** The air tastes metallic. Shadows move wrong. A scavenger camp offers to sell 'safe routes' for $300. The routes are 70% accurate (WIL save to judge reliability)."),
    sp(1),
    p("**B. The Boulevard.** The former Las Vegas Boulevard. Buildings exist in 2-3 eras simultaneously. The road surface changes every 20 meters: asphalt, cobblestone, bare earth, smooth future-material. 1 echo patrols here on a loop, walking the same 200 meters endlessly."),
    sp(1),
    p("**C. The Luxor Shell.** The black pyramid. The interior shifts eras every 30 minutes. Three echoes inside (one wearing a lab coat, probably a former researcher). The lab contains Division files from 2027: early Oculus containment protocols. Worth $5,000 to Hayes, $8,000 to Zhou."),
    sp(1),
    note("Dilemma: the lab coat echo responds to its name (Dr. Sarah Voss). It says 'Help me' repeatedly and points at a terminal. The terminal contains Voss's final research notes: a theoretical cure for echo transformation, incomplete. Removing the terminal triggers structural collapse (DEX save, d8 damage). Leave it, or lose the cure forever."),
    sp(1),
    p("**D. The MGM Crater.** A 50-meter crater where the MGM Grand stood. Looking down: different time periods layered like geological strata. At the bottom: an intact Oculus fragment, class-A, worth $15,000+. Each 'layer' requires a WIL save against contamination on the way down."),
    sp(1),
    p("**E. The Bellagio Fountain.** The famous fountains still run, but spray temporal energy instead of water. Standing in the mist: WIL save or age d10 years permanently. Echoes avoid the fountain, making it a potential rest point, though contamination checks still apply."),
    sp(1),
    p("**F. The Seam.** The boundary between Red and Black zones. Crossing requires a STR save. Failure: d8 STR damage. Success: you are in the Black Zone. Sound arrives late. Your movements leave afterimages. Contamination check immediately, d6 damage die."),
    sp(1),
    p("**G. Ground Zero.** Directly beneath the original Oculus laboratory. A crater within the crater, 20 meters deep. Perfect stillness. At the center: the original Oculus device. Still running. Still breaking time. It hums at a frequency you feel in your teeth."),
    sp(1),
    note("This is the endgame location. The final choice: **destroy it** (Vegas begins stabilizing, the Division loses its purpose, Zhou loses her market). **Take it** (unimaginable power, total corruption, everyone hunts you). **Leave it** (nothing changes, the zones keep expanding, more people die every year). There is no right answer."),
    pb(),
    ]

    # ════════════════════════════════
    # WARDEN'S GUIDE
    # ════════════════════════════════
    s += [h1("Warden's Guide"), rule(),
    p("Your role as Warden: you are not a storyteller, a neutral arbiter, or the players' enemy. You are a **facilitator of emergent stories**. Present interesting situations, not solutions. Interpret rules quickly and fairly. React to player choices logically. Create tension through scarcity. Celebrate successes. Make failures meaningful."),
    sp(3),
    h2("Core Philosophy"),
    h3("Rulings, Not Rules"),
    p("When a player proposes an action not covered by the rules, ask: 'Is it reasonable in context?' If yes, decide quickly on a mechanism. Apply difficulty if needed. Move on."),
    sp(1),
    note("Example: 'I want to use my Phase Shift Quirk to reach through the wall and unlock the door from inside.' Warden: 'WIL save to control the phasing. The wall is thick, so impaired if you fail.' Player rolls, succeeds. 'Your hand passes through the concrete. Click. Your hand is numb for 1 round.'"),
    sp(2),
    h3("Player Skill, Not Character Skill"),
    p("Reward creativity, planning, and cunning. If players find a clever solution (avoid combat with a smart plan, negotiate instead of fighting, use the environment), do not require a dice roll. Success is automatic if the solution is good."),
    sp(1),
    note("Example: 10 guards watching a warehouse. Brute force: combat, lethal. Smart: 'We trigger a false fire alarm on the other side of the complex. While they run, we enter from the back.' Warden: 'No roll needed. Guards leave. You have 10 minutes. Go.'"),
    sp(2),
    h3("Danger Is Real"),
    p("Do not balance encounters to the party's strength. If players enter a Red Zone unprepared, they meet lethal enemies. This is not cruelty. It is honesty. Players learn fast: combat is the last resort."),
    sp(1),
    p("Do not save players from stupid choices. But warn them before suicidal ones: 'You see 8 armed mercenaries behind sandbags. They have not noticed you yet. What do you do?' If after the warning they charge in, let the dice fall."),
    sp(2),
    h3("Give Them Information"),
    p("Information is free. Players do not roll to notice obvious things. Tell them: 'The corridor smells of ozone and decay. The lights flicker: 3 seconds on, 2 off. You hear footsteps, at least three people, coming from the left.' Let them make informed decisions."),
    sp(3),
    h2("Session Preparation"),
    h3("What to Prepare"),
    b("1 mission with a clear objective and 2-3 possible complications"),
    b("2-3 NPCs with names, motivations, and one secret each"),
    b("1 moral dilemma with no right answer"),
    b("The weekly accounting (pay, expenses, debt update for each PC)"),
    b("1 Zhou offer (if applicable based on debt levels)"),
    sp(2),
    h3("What NOT to Prepare"),
    b("Complete dungeon maps (sketch rough layouts, improvise details)"),
    b("Predetermined outcomes (the story goes where players take it)"),
    b("Balanced encounters (the world does not scale to the PCs)"),
    b("NPC dialogue scripts (know their motivation, improvise the words)"),
    sp(2),
    h3("The Diamond Method"),
    p("Prepare 3 things: **a starting situation, a crisis point, and 2-3 possible endings.** Between these, the players fill the space. The session flows like a diamond: starts narrow (briefing), expands (exploration, choices), then narrows again (climax, consequences)."),
    sp(3),
    h2("Session Structure (3-4 hours)"),
    T(["Time","Phase","Content"],
      [["0:00-0:20","**Opening**","Recap, weekly accounting, Hayes briefing"],
       ["0:20-1:30","**Mission**","Exploration, encounters, complications"],
       ["1:30-1:45","**Break**","Real-world pause, Warden reviews notes"],
       ["1:45-2:45","**Climax**","The central dilemma, combat if needed"],
       ["2:45-3:15","**Consequences**","Debriefing, Zhou contact, downtime"],
       ["3:15-3:30","**Closing**","Update trackers, tease next session"]],
      [CW*0.22, CW*0.20, CW*0.58]),
    sp(3),
    h2("Creating Moral Dilemmas"),
    p("A good dilemma has: **two options, both costly, both defensible, with permanent consequences.** Avoid false dilemmas (one option clearly better) and moralizing (do not lecture players on their choices, let the numbers speak)."),
    sp(1),
    note("**The Informant:** A Division contact inside Zhou's organization has been compromised. Hayes orders extraction. Zhou offers $5,000 to delay 2 hours. The informant has a family."),
    sp(1),
    note("**The Medicine:** You find a stash of anti-rejection medicine for your team, 3 months' worth. A civilian camp nearby desperately needs it. If you keep it, you save on expenses. If you give it away, you go broke."),
    sp(1),
    note("**The Echo:** A temporal echo is blocking your path. But it was once Agent Reyes, a colleague you knew. It recognizes you. It says your name. It asks for help. Your orders are to neutralize all echoes."),
    sp(3),
    h2("Campaign Difficulty Curve"),
    h3("Act I: Introduction (Sessions 1-6)"),
    p("Yellow Zone missions. Economy pressure builds slowly. First Zhou contact around session 3-4. First Quirk around session 4-5. PCs learn the systems. Tone: tense but manageable."),
    sp(2),
    h3("Act II: Transition (Sessions 7-9)"),
    p("Red Zone missions begin. Economy becomes critical. Instability possible for PCs who played both sides. First PC death likely. Tone: desperate."),
    sp(2),
    h3("Act III: Climax (Sessions 10-15)"),
    p("Red and Black Zone missions. The central conspiracy emerges (who is deliberately destabilizing the zones?). PCs must commit to a faction. Multiple Quirks per character. Echo transformation is a real threat. Tone: no way out."),
    sp(3),
    h2("Managing the Raines Relationship"),
    p("After an agent completes 3 missions for Raines, Hayes knows. He says nothing. From that point forward, missions assigned to that agent become harder: Red zones instead of Orange, tighter timing windows, steeper secondary objectives. If the agent reaches 5 missions for Raines, Hayes files a formal surveillance request and a second NPC agent joins every Division mission."),
    sp(1),
    p("When the threshold approaches, present the math explicitly at session start: 'You have completed 2 missions for Raines. The third will push you past the point where Hayes starts adjusting your assignments. Do you take the mission?' This is not a spoiler. It is information the character would reasonably calculate."),
    sp(3),
    h2("Managing PC Death"),
    p("At the table: acknowledge the loss, keep the pace. The new PC inherits the team's shared debt proportionally. Loyalty starts at 5, Corruption at 0. Arrives with standard equipment. Do not punish the player for their character's death. Replacement should feel seamless."),
    pb(),
    ]

    # ════════════════════════════════
    # ENEMIES
    # ════════════════════════════════
    s += [h1("Enemies"), rule(),
    p("Format: **Name.** HP, Armor, STR, DEX, WIL, weapon (damage). Special ability or critical damage effect. Morale note."),
    sp(2),
    h2("Common Threats"),
    p("**Street Thug.** 3 HP, 8 STR, 10 DEX, 6 WIL, knife (d6) or pistol (d6). *Flees at first casualty.*"),
    sp(1),
    p("**Armed Scavenger.** 4 HP, 10 STR, 12 DEX, 8 WIL, pistol (d6). Wants loot, not fights. Reaction roll to see if they parley. *Flees if outnumbered or if a serious threat emerges.*"),
    sp(1),
    p("**Scavenger Pack (Detachment).** 12 HP, 1 Armor, 12 STR, 10 DEX, 8 WIL, mixed weapons (d6, blast). *Routed at critical damage.*"),
    sp(1),
    p("**Zhou's Courier.** 4 HP, 8 STR, 14 DEX, 10 WIL, concealed pistol (d6). Runs rather than fights. If cornered: offers bribe ($500). Carries a sealed package worth $2,000 to Zhou."),
    sp(3),
    h2("Division and Military"),
    p("**Division Security Guard.** 5 HP, 1 Armor, 12 STR, 10 DEX, 10 WIL, pistol (d6), baton (d6). Follows orders. *Holds unless outnumbered 3:1.*"),
    sp(1),
    p("**Division Field Agent.** 6 HP, 1 Armor, 12 STR, 12 DEX, 12 WIL, Glock (d6), knife (d6). Trained, professional. *Critical damage: target is disarmed.*"),
    sp(1),
    p("**Zhou's Mercenary.** 6 HP, 1 Armor, 12 STR, 12 DEX, 8 WIL, assault rifle (d8). Well-equipped, low loyalty. *Flees if leader falls.*"),
    sp(1),
    p("**Zhou's Elite.** 8 HP, 2 Armor, 14 STR, 14 DEX, 10 WIL, assault rifle (d8), frag grenade. *Critical damage: target is pinned. Does not flee.*"),
    sp(1),
    p("**Armored Vehicle.** Treat as detachment. 10 HP, 3 Armor, machine gun (d8, blast). Immune to pistol fire (impaired). Vulnerable to explosives and temporal relics."),
    sp(3),
    h2("Temporal Threats"),
    p("**Temporal Echo (Standard).** 4 HP, 8 STR, 12 DEX, 6 WIL, temporal claw (d6). *Critical damage: WIL save or accelerated aging (1 round). Flees at 50% casualties.* Appears translucent, moves in stuttering jumps."),
    sp(1),
    p("**Temporal Echo (Aggressive).** 8 HP, 14 STR, 10 DEX, 4 WIL, temporal slam (d8). *Critical damage: oldest item in inventory aged to dust. Never flees.* Charges directly, no tactics."),
    sp(1),
    p("**Temporal Echo (Sentient).** 6 HP, 10 STR, 10 DEX, 14 WIL, temporal grasp (d6). Can speak in fragments from multiple time periods. Reaction roll possible before attacking. *Critical damage: WIL save or target sees a vision of their own death, stunned 1 round.*"),
    sp(1),
    p("**Phase Stalker.** 6 HP, 8 STR, 16 DEX, 8 WIL, phase strike (d8, ignores Armor). Partially intangible: only damaged by enhanced attacks, blast, or temporal relics. Always acts first."),
    sp(1),
    p("**Temporal Swarm (Detachment).** 15 HP, 6 STR, 14 DEX, 4 WIL, temporal erosion (d6, blast). Immune to single-target attacks. *Critical damage: d4 WIL damage to target.* Vulnerable to Anchor Spikes and area effects."),
    sp(3),
    h2("Quick Conversion Rule"),
    p("Adapt any modern or sci-fi enemy: Hit Dice become HP (roughly 1:1 for humanoids, add 2-4 for tougher creatures). Armor Class becomes Armor (light=1, medium=2, heavy=3, max 3). Ignore attack bonuses (attacks auto-hit in Cairn). Damage stays roughly the same die. Give it **one memorable behavior** and **one critical damage effect**. Set morale based on motivation."),
    pb(),
    ]

    # ════════════════════════════════
    # TABLES & GENERATORS
    # ════════════════════════════════
    s += [h1("Tables & Generators"), rule(),
    h2("Mission Generator (3 rolls)"),
    T(["d6","Mission Type"],
      [["1","Recovery (retrieve an artifact or data)"],
       ["2","Escort (protect a person or cargo through a zone)"],
       ["3","Reconnaissance (map or assess a new zone)"],
       ["4","Rescue (find and extract trapped civilians or agents)"],
       ["5","Sabotage (disable a rival operation or anomaly)"],
       ["6","Elimination (neutralize a specific threat or echo)"]],
      [CW*0.15, CW*0.85]),
    sp(2),
    T(["d6","Location"],
      [["1","Abandoned hotel, half in the 1930s"],
       ["2","Underground lab complex, flickering between eras"],
       ["3","Collapsed casino, structural hazards throughout"],
       ["4","Residential block, civilians present"],
       ["5","Strip plaza, maximally unstable"],
       ["6","Subway tunnels, complete darkness"]],
      [CW*0.15, CW*0.85]),
    sp(2),
    T(["d6","Complication"],
      [["1","Zhou's mercenaries are already there"],
       ["2","Zone stability deteriorating (collapse in d6 hours)"],
       ["3","A previous Division team went missing here"],
       ["4","The objective is not what Hayes described"],
       ["5","A civilian group refuses to evacuate"],
       ["6","A sentient echo is guarding the objective"]],
      [CW*0.15, CW*0.85]),
    sp(2),
    note("Example: Recovery (1) + Subway tunnels (6) + Zhou's mercenaries already there (1) = Recover a class-B Oculus fragment from the collapsed metro station under Fremont Street. Problem: Zhou sent a team 3 hours ago."),
    sp(3),
    h2("NPC Generator (d6 per category)"),
    T(["d6","Appearance","Occupation","Motivation","Secret"],
      [["1","Scarred, military bearing","Division agent (current or former)","Money (debts, greed, survival)","Works for opposite faction"],
       ["2","Young, nervous, talks fast","Zhou's operative (muscle or courier)","Revenge (against Division or Zhou)","Has a terminal Quirk"],
       ["3","Elderly, calm, knows too much","Scavenger (freelance zone looter)","Family (protecting someone)","Knows a valuable artifact location"],
       ["4","Well-dressed, hiding something","Civilian refugee (trapped)","Curiosity (temporal research)","Murdered someone, hiding it"],
       ["5","Injured, desperate","Merchant (legal or black market)","Power (climbing ranks)","Related to a key NPC"],
       ["6","Temporal-touched, wrong-era clothes","Temporal ghost (1920s-1950s echo)","Escape (leaving Vegas)","Has no secret (suspicious)"]],
      [FW*0.06, FW*0.22, FW*0.22, FW*0.25, FW*0.25], full=True),
    sp(3),
    h2("Zone Characteristics (d6 each)"),
    T(["d6","Stability","Visual Phenomenon","Unique Risk"],
      [["1-2","Stable (check every 8h)","Time layers: multiple eras visible","Gravity anomaly (DEX save)"],
       ["3-4","Deteriorating (check every 6h)","Temporal rain: water falls upward","Aging field (STR save or age d10 yrs)"],
       ["5","Unstable (check every 3h)","Ghost crowd: translucent thousands","Memory echo (WIL save or confused d6 rds)"],
       ["6","Collapsing (check hourly)","Frozen moments: objects suspended","Loop trap (WIL save or repeat 10 sec)"]],
      [FW*0.08, FW*0.22, FW*0.35, FW*0.35], full=True),
    sp(3),
    h2("Treasures and Artifacts (d6 + d6)"),
    T(["First d6","Second d6","Artifact","Value"],
      [["1","1-3","Pre-Oculus personal item (photo, letter, jewelry)","$50-200"],
       ["1","4-6","Vintage weapon in perfect condition","$300-800"],
       ["2","1-3","Future-tech medical supplies","$500-1,500"],
       ["2","4-6","Encrypted Division data chip","$1,000-3,000"],
       ["3","1-3","Oculus fragment, class-C (minor)","$2,000-5,000"],
       ["3","4-6","Temporal artifact (unusual properties)","$3,000-10,000"],
       ["4","1-3","Pre-Oculus cash stash (d6 x $500)","Variable"],
       ["4","4-6","Black market contraband (drugs, weapons)","$1,000-4,000"],
       ["5","1-3","Functional future-tech device","$5,000+"],
       ["5","4-6","Oculus fragment, class-B (significant)","$5,000-15,000"],
       ["6","1-6","Oculus fragment, class-A (major)","$15,000+"]],
      [FW*0.12, FW*0.12, FW*0.46, FW*0.30], full=True),
    sp(3),
    h2("Sudden Complications (d6)"),
    T(["d6","What Happens"],
      [["1","Radio goes dead. No contact with base for d6 hours."],
       ["2","Zone stability drops one level. Contamination checks accelerate."],
       ["3","A teammate's Quirk activates at the worst possible moment."],
       ["4","Unexpected expense back home: d6 x $100 (landlord, medical, car)."],
       ["5","Zhou's courier finds you in the field. She has an offer. Now."],
       ["6","You find a dead Division agent. Their badge says they are from next week."]],
      [FW*0.10, FW*0.90], full=True),
    sp(3),
    h2("Quick NPC Names"),
    p("**Male:** Marcus, Jin, Alejandro, Viktor, Tommy, Darnell. **Female:** Elena, Sofia, Maya, Anya, Grace, Yuki. **Surnames:** Chen, Volkov, Martinez, O'Brien, Tanaka, Greene. **Codenames:** Viper, Ghost, Tank, Whisper, Lucky, Double."),
    pb(),
    ]

    # ════════════════════════════════
    # CAMPAIGN MANAGEMENT
    # ════════════════════════════════
    s += [h1("Campaign Management"), rule(),
    h2("Narrative Arcs (10-15 Sessions)"),
    h3("Act I: Survival and Discovery (Sessions 1-5)"),
    p("PCs are fresh recruits. They learn the systems: first Yellow Zone missions, first paychecks, first deficits, first Zhou contact. The economy tightens slowly. The first Quirk appears. Players discover that honest play leads to debt."),
    sp(1),
    p("**Warden focus:** Teach mechanics through play. Show the economic spiral. Introduce Hayes as fair-but-cold, Zhou as friendly-but-dangerous. Do not rush the dilemmas."),
    sp(2),
    h3("Act II: Corruption and Choices (Sessions 6-10)"),
    p("Red Zone missions begin. Economy becomes critical. PCs have 1-3 Quirks. At least one has dealt with Zhou. Instability becomes possible. The first PC death is likely. The big questions emerge: who are you becoming?"),
    sp(1),
    p("**Warden focus:** Increase pressure on all fronts simultaneously. Money, contamination, loyalty, and corruption should all be in play every session."),
    sp(2),
    h3("Act III: Consequences and Resolution (Sessions 11-15)"),
    p("Red and Black Zone missions. The conspiracy emerges: someone is deliberately destabilizing temporal zones. PCs must commit to a faction. Multiple Quirks per character. Echo transformation is a real threat."),
    sp(1),
    p("**Warden focus:** Bring all threads together. Every past choice has consequences now. Zhou calls in favors. Hayes demands results. The endgame approaches."),
    sp(3),
    h2("Factions and Their Agendas"),
    T(["Faction","Wants","Methods","Weakness"],
      [["The Division (Hayes)","Stabilize zones, recover Oculus tech, government control","Bureaucracy, hierarchy, expendable agents","Underfunds agents, creating the desperation Zhou exploits"],
       ["Zhou's Network","Monopoly on temporal tech, Oculus files, profit","Bribery, patience, leverage, selective violence","Depends on corrupted Division agents"],
       ["The Refugees","Safety, medicine, a way out of Vegas","Community, mutual aid, occasional desperation","No power or resources"],
       ["The Sentient Echoes","Unknown. Some seem to communicate, some organize","Hostile action, occasional apparent communication","Unknown. Possibly unknowable."]],
      [FW*0.18, FW*0.24, FW*0.28, FW*0.30], full=True),
    sp(3),
    h2("Long-Term Consequences"),
    p("Keep a simple session log: 'Session 3: PCs accepted Zhou's first offer. Marco carried the package.' These notes become plot hooks. The package Marco carried? It contained plans for a Division raid. Zhou used the intel. People died. This comes back at session 10."),
    sp(2),
    T(["Original Choice","Delayed Consequence (Sessions Later)"],
      [["Kept a small unregistered artifact (Session 2)","By session 8, Zhou mentions she knows about it. Leverage."],
       ["Helped civilians instead of completing objective (Session 4)","By session 6, those civilians help PCs. Or one was a Zhou spy."],
       ["Lied to Hayes about a fragment (Session 6)","By session 10, Internal Affairs investigation."]],
      [FW*0.38, FW*0.62], full=True),
    sp(3),
    h2("Possible Campaign Endings"),
    h3("Ending A: Loyalty Redeemed"),
    p("PCs stayed loyal despite the cost. Debt is massive but Hayes promotes them. They uncover the conspiracy. Vegas begins to stabilize. They are heroes. But at what cost? Quirks, dead friends, permanent contamination. They won, but they are not the same people who started."),
    sp(2),
    h3("Ending B: The Corruption Kingdom"),
    p("PCs went all-in with Zhou. She now controls temporal technology. The Division collapses. Vegas becomes Zhou's kingdom. PCs are rich, powerful, and damned. The contamination continues. The zones expand. But hey, the rent is paid."),
    sp(2),
    h3("Ending C: The Precarious Balance"),
    p("PCs played both sides. Neither Hayes nor Zhou fully trusts them. The conspiracy is partially uncovered. Vegas is neither saved nor doomed. The most realistic ending. The most unsatisfying. The most human."),
    sp(2),
    h3("Ending D: The Final Sacrifice"),
    p("One or more PCs sacrifice themselves to destroy the original Oculus device under the Luxor. Vegas is saved. The surviving PCs walk away from everything. The dead are remembered. Sometimes heroes are just desperate people who ran out of options."),
    sp(2),
    h3("Ending E: The Escape"),
    p("PCs realize Vegas is doomed and leave. They flee with whatever money and artifacts they can carry. The Division marks them as deserters. Zhou marks them as assets who escaped. They start over somewhere else, with Quirks and nightmares. The zones continue expanding. Someone else's problem now."),
    pb(),
    ]

    # ════════════════════════════════
    # DESIGN NOTES & FAQ
    # ════════════════════════════════
    s += [h1("Design Notes"), rule(),
    p("These notes explain the reasoning behind key decisions. They were originally embedded throughout the Italian edition as designer commentary boxes."),
    sp(3),
    h2("Why the Economy Is Unsustainable"),
    p("The deficit at Recruit tier is not a balance error. It is the single most important number in the game. Without it, corruption is a free choice (why not?). With it, corruption is a survival mechanism (I have to). The difference between 'I chose to be corrupt' and 'the system forced me to choose' is the entire moral weight of the game."),
    sp(3),
    h2("Why Contamination Is Permanent"),
    p("WIL damage from contamination does not heal normally because the time zones are changing your biology, not injuring it. A bullet wound heals. A temporal mutation does not. The progressive degradation creates a natural campaign timer. Every mission brings characters closer to becoming echoes. This urgency drives the pace."),
    sp(3),
    h2("Why Combat Should Be Avoided"),
    p("In the Cairn engine, a Glock 17 does d6 damage. Average starting HP is 3.5. One good roll drops a PC to 0 and triggers critical damage. Two hits kill. This is intentional. Combat should feel like combat in a crime thriller: terrifying, brief, and something you plan your way around. The game's real challenges are economic and moral, not tactical."),
    sp(3),
    h2("Why Cairn Instead of Traditional OSR"),
    p("The original UeT had 6 attributes, roll-under to-hit, 10 levels, and a skill list. The problem: all of this competed for cognitive space with the game's original systems (economy, contamination, loyalty/corruption, Quirks, instability). Players spent mental energy on 'do I hit?' instead of 'do I accept Zhou's offer?' Cairn strips the overhead to near-zero. Three attributes. No attack rolls. No levels. This frees the table's attention for the systems that make UeT unique."),
    sp(3),
    h2("Why 3 Tiers Instead of 10 Levels"),
    p("Tiers strip mechanical progression entirely. The only thing that changes is pay. Advancement in Uchronies & Treasures is purely financial: you get better at paying your bills. You do not get stronger. You get more stable. And stability, in a world designed to destabilize you, is power."),
    sp(3),
    h2("The Quirk Design Philosophy"),
    p("Each Quirk has a permanent mechanical effect (both benefit and cost), a narrative trigger (what it looks like at the table), and a social consequence (how NPCs react). The benefits are intentional. Prescience gives automatic initiative. Phase shift lets you pass through walls. These are real powers. But each comes with a social cost more significant than the mechanical one. You see how people die. Your hand passes through objects you try to hold. The game does not take away your agency. It makes your agency uncomfortable."),
    sp(3),
    h2("Frequently Asked Questions"),
    h3("Rules"),
    p("**How does combat work without attack rolls?** You roll your weapon's damage die, subtract the target's Armor, and apply the remainder to HP. Attacks always hit. The question is not 'do I hit?' but 'how much damage do I take in return?'"),
    sp(1),
    p("**When should I call for a save?** Only when the outcome is uncertain AND the stakes are meaningful. An ex-military background means field-stripping a gun requires no roll. Disarming a bomb while a building collapses requires a DEX save."),
    sp(1),
    p("**Can PCs have more than 3 Armor?** No. 3 is the absolute maximum."),
    sp(1),
    p("**What happens when WIL reaches 0 from contamination?** Temporal echo. Permanent. The player creates a new character."),
    sp(1),
    p("**What happens when WIL reaches 0 from other causes?** Catatonia. Requires a week of medical care."),
    sp(2),
    h3("Setting"),
    p("**Can PCs leave Las Vegas?** Yes, but why? Their Division contract binds them financially. Their medicine dependency binds them medically. Their Quirks bind them socially (try explaining accelerated aging to airport security). Vegas is a cage with open doors."),
    sp(1),
    p("**Is Zhou evil?** No. Zhou is pragmatic. She exploits desperate people, but so does the Division. The difference is that Zhou is honest about the transaction. Hayes pretends it is patriotism. Neither is 'good.'"),
    sp(2),
    h3("Balance"),
    p("**The economy seems impossible. Is this intentional?** Yes. The deficit at Recruit tier is the game's engine. Without it, there is no pressure toward corruption. If your players are comfortable financially, something has gone wrong."),
    sp(1),
    p("**How fast do Quirks accumulate?** In a typical 10-session campaign, a PC doing mostly Yellow Zone missions will accumulate 1-2 Quirks. A PC who regularly enters Red Zones will get 3-4. Reaching the echo threshold of 5 should be rare but possible."),
    sp(1),
    p("**How do I handle players who want to be 'good guys'?** Let them try. The system does not punish goodness. It makes it expensive. A loyal PC will have more debt, more stress, fewer resources, but Hayes' trust, better missions, and their self-respect. Whether that is worth it is the entire point of the game."),
    pb(),
    ]

    # ════════════════════════════════
    # EXAMPLE OF PLAY
    # ════════════════════════════════
    s += [h1("Example of Play"), rule(),
    p("The following scene shows a typical session opening: weekly accounting, a briefing, short exploration, combat, and Zhou's offer. Players are **Reyes** (Ex-Military, STR 12, DEX 14, WIL 9, 4 HP) and **Marco** (Con Artist, STR 8, DEX 11, WIL 13, 3 HP). It is Week 4. Both are Recruits."),
    sp(3),
    p("**Warden:** 'Monday morning. Payday. Let us do the books.'"),
    sp(1),
    p("**Warden** *(writing on the whiteboard):* 'Reyes: $800 pay. Expenses $900 out. Balance: minus $100. Debt was $420 last week. Now $520. Marco, same math. Debt was $380. Now $480.'"),
    sp(1),
    p("**Marco:** 'Every week. Every single week. Can we at least get some overtime?'"),
    sp(1),
    p("**Warden:** 'Hayes does not do overtime. But she does have a mission. Briefing room, 07:00.'"),
    sp(3),
    p("**Warden** *(as Hayes):* 'Agents. A warehouse in the Yellow Zone. We lost contact with a sensor team yesterday. Objective: find the team, recover their data chip, get out. Bonus: $50 base plus $200 if the data comes back intact.'"),
    sp(1),
    p("**Reyes:** 'Any hostile contacts?'"),
    sp(1),
    p("**Warden:** 'Hayes checks her tablet: Scavenger activity in the area. No confirmed echoes. Yellow Zone, contamination checks every 8 hours. You should be in and out in 4. Questions? No? Move out.'"),
    sp(3),
    p("**Warden:** 'You arrive at the warehouse complex. Building A has its doors open. Building B is sealed shut. Inside A: Division equipment on the ground, two tactical vests, a smashed radio. A blood trail leading toward Building B. Enough blood that someone walked away badly hurt.'"),
    sp(1),
    p("**Reyes:** 'I follow the trail. Moving carefully.'"),
    sp(1),
    p("**Marco:** 'I try the shutters on Building B.'"),
    sp(1),
    p("**Warden:** 'Locked from inside. Building B interior flickers. One moment a modern warehouse. Next, a 1950s storage facility with wooden crates. The temporal overlap is active.'"),
    sp(1),
    p("**Marco:** 'I find another way in. There must be a vent.'"),
    sp(1),
    p("**Warden:** 'A ventilation grate on the side of the walkway. Big enough to crawl through. It leads into Building B's ceiling space.'"),
    sp(1),
    p("**Marco:** 'Through the vent. Quietly.'"),
    sp(1),
    p("**Warden:** 'The building is flickering between eras. Make a DEX save to time your movement between the flickers.'"),
    sp(1),
    p("**Marco** *(rolls d20: 8, under DEX 11):* 'Made it.'"),
    sp(1),
    p("**Warden:** 'You emerge on a catwalk above the floor. Below: two scavengers, armed, going through Division supply crates. Between them, on the floor: Agent Dominguez, hands zip-tied, bruised face. Alive. She sees you. Her eyes go wide. She does not make a sound.'"),
    sp(3),
    p("**Reyes** *(having circled to the loading dock):* 'I step in, gun raised. Division. Drop your weapons.'"),
    sp(1),
    p("**Warden:** 'The scavengers spin around. Initiative. Reyes, DEX save.'"),
    sp(1),
    p("**Reyes** *(rolls d20: 6, under DEX 14):* 'I go first.'"),
    sp(1),
    p("**Marco** *(rolls d20: 15, over DEX 11):* 'Failed. I lose my first turn.'"),
    sp(1),
    p("**Reyes:** 'I shoot the one with the pistol.'"),
    sp(1),
    p("**Reyes** *(rolls d6: 5):* 'Five damage.'"),
    sp(1),
    p("**Warden:** 'No armor. Five damage to his 4 HP, drops below zero. One point carries to STR. He makes a STR save' *(rolls 17, over STR 10)* 'Failed. Critical damage. He collapses. The other scavenger sees his partner go down. Morale check' *(rolls 14, over WIL 8)* 'Failed. He drops the crowbar and runs.'"),
    sp(1),
    p("**Marco:** 'I shout from the catwalk: There are Division agents everywhere! You are surrounded!'"),
    sp(1),
    p("**Warden:** 'He does not need convincing. He is gone. Dominguez is on the floor, looking up at you.'"),
    sp(3),
    p("**Warden:** 'Back at base. Debriefing with Hayes. Bonus: $50 base plus $200 for the chip. Your deficit was $100. Net gain: $250. Reyes, your debt goes from $520 to $270. Marco, $480 to $230.'"),
    sp(1),
    p("**Marco:** 'Finally breathing.'"),
    sp(1),
    p("**Warden:** 'That evening, a note in your mailbox. Perfumed paper, handwritten.'"),
    sp(1),
    p("**Marco:** 'Oh no.'"),
    sp(1),
    p("**Warden** *(reading):* 'Dear Agent Marco. I understand you encountered some of my associates today in the Yellow Zone. No hard feelings. Business is business. I notice your financial situation remains challenging. I have a small task. $1,500 for one evening. Nothing dangerous. My address is the Crimson Palace. You know where it is. With regards, M. Zhou.'"),
    sp(1),
    p("**Marco** *(long pause):* 'What is my debt again?'"),
    sp(1),
    p("**Warden:** '$230. Next week's deficit: $100. By next Monday you are at $330, unless you do a mission.'"),
    sp(1),
    p("**Marco** *(to Reyes):* 'What would you do?'"),
    sp(1),
    p("**Reyes:** 'I would tell Zhou to go to hell.'"),
    sp(1),
    p("**Marco:** 'Easy for you to say. Your Loyalty is 7. Mine is 5. And my mother's medicine costs $300 a week on top of everything else.'"),
    sp(1),
    p("**Warden:** 'Zhou's note is sitting on your kitchen table. The rent bill is next to it. What do you do?'"),
    sp(2),
    p("*(End of scene)*"),
    pb(),
    ]

    # ════════════════════════════════
    # ADVENTURES
    # ════════════════════════════════
    s += [h1("The Chicago Loop"), rule(),
    p("**Overview.** A one-shot adventure for 3-5 players, lasting 3-4 hours. Introduces all core mechanics: combat, exploration, contamination, and the central loyalty-vs-corruption dilemma. **Structure:** Act 1 The Briefing (20 min), Act 2 The Infiltration (60 min), Act 3 The Climax (45 min), Act 4 Consequences (30 min)."),
    sp(3),
    h2("Act 1: The Briefing"),
    p("Hayes enters the briefing room at 06:00. 'Agents. Critical situation in Chicago. A temporal zone opened 72 hours ago, downtown. Stability: declining. We have 24 hours before total collapse.'"),
    sp(1),
    p("She projects a holographic image of the Meridian Hotel: half 1930s art deco, half 2080 brutalism, the boundary between them blurred and vibrating. 'Sensors indicate a class-A Oculus fragment inside. Suite 2701, 27th floor. Mission: recover the fragment, extract, deliver. Maximum time in zone: 8 hours.'"),
    sp(2),
    p("**If PCs ask:** Zone stability is Phase 2 (deteriorating), WIL save every 6 hours initially, every 3 hours after the first 4. Between 30 and 50 civilians trapped. At least 5-10 hostile echoes confirmed. No support: helicopter drops you and returns in 8 hours. Mission bonus: $500 each if completed plus $200 per civilian evacuated alive."),
    sp(1),
    p("**Special equipment provided:** Advanced temporal protection suit (reduces contamination damage by 2), encrypted radio, field med kit (3 uses, d4 STR), extra ammo, shielded container for the Oculus fragment."),
    sp(1),
    note("The hidden complication: Zhou has already sent 3 mercenaries, 2 hours ahead of the Division. Their goal: steal the fragment and vanish before you arrive. Hayes may suspect this. She does not warn you. She wants to see how you react."),
    sp(3),
    h2("Act 2: The Infiltration"),
    p("The helicopter drops you on a rooftop 200 meters from the Meridian Hotel. It takes off immediately. 'Eight hours! Not a minute more!'"),
    sp(1),
    p("The Meridian is wrong in a way you feel before you can articulate it. The right half is 1930s art deco: marble, stained glass, decayed elegance. The left half is 2080 brutalism: concrete, glass, geometric lines. The boundary between them is blurred, vibrating, like looking through water."),
    sp(2),
    h3("The Lobby"),
    p("The lobby superimposes two eras. Four NPCs are here: **Margaret O'Brien** (65, 2080 resident, terrified, hiding behind the desk), **Thomas Harker** (28, 1934 temporal ghost, confused, looking for his wife Dorothy), and **two children** (brother and sister, 8 and 10, crying, looking for their parents)."),
    sp(1),
    note("Choices: evacuate civilians now (costs 2 turns, humane), promise to return after getting the fragment (faster, risky), bring them along (slow, safe), ignore them completely (fastest, morally terrible)."),
    sp(2),
    h3("The Stairs"),
    p("Elevators do not work. Every 5 floors: a temporal interface. **STR save** or d6 damage from temporal shock."),
    sp(1),
    p("**Random encounters (d6 every 2 turns):** 1-Nothing, 2-Wounded civilian (asks for help), 3-1 temporal echo (hostile), 4-Temporal event: local loop (repeat next 2 turns), 5-2 temporal echoes, 6-Zhou's mercenaries."),
    sp(3),
    h2("Act 3: The Climax, 27th Floor"),
    p("The door to Suite 2701 is ajar. Through the crack: the pulsing blue-violet light of the Oculus fragment on the central table. And three figures in black tactical gear, one of them reaching for the fragment with a shielded container identical to yours. 'Shit. Division.' She raises her rifle."),
    sp(2),
    h3("Zhou's Mercenaries"),
    p("**Anya 'Viper' Volkov** (leader): 8 HP, 2 Armor, 10 STR, 14 DEX, 12 WIL, sniper rifle (d10), knife (d6). *Critical damage: target is pinned.*"),
    sp(1),
    p("**Marcus 'Tank' Greene:** 10 HP, 3 Armor, 16 STR, 8 DEX, 8 WIL, shotgun (d8). *Attacks enhanced at close range.*"),
    sp(1),
    p("**Jin 'Ghost' Tanaka:** 6 HP, 1 Armor, 8 STR, 16 DEX, 10 WIL, suppressed pistol (d6), knife (d6). *Always wins initiative. Will flee with the fragment if combat turns bad.*"),
    sp(2),
    h3("Player Options"),
    b("**Direct combat:** High difficulty. Mercenaries are veterans with cover. Win: +1 Loyalty. Zhou is angry (future vendetta). Lose: mercenaries flee with fragment, -2 Loyalty."),
    b("**Negotiate:** Anya is pragmatic. Deals include: 50/50 split (+1 Corruption), let them go and lie to Hayes (+2 Corruption, -1 Loyalty if discovered), or work together for Zhou (+2 Corruption). WIL save to persuade."),
    b("**Deception:** 'The Division has surrounded the building' (WIL save, difficulty). 'Steal the fragment while they are distracted' (DEX save + coordination)."),
    sp(2),
    note("The radio crackles: 'Zone has entered phase 3. Estimated collapse in 2 hours, not 8. Repeat: you have 2 hours to extract.' Now combat costs precious time. What do you prioritize: mission, survival, or wealth?"),
    sp(3),
    h2("Act 4: Consequences"),
    p("Call the helicopter, reach the roof. Final WIL save against contamination (4-6 hours of exposure). Watch the Meridian Hotel implode behind you."),
    sp(2),
    h3("Debriefing with Hayes"),
    p("**Mission completed, loyal:** Hayes takes the fragment. 'Good work.' Almost a compliment. Full bonuses."),
    sp(1),
    p("**Negotiated with mercenaries:** Hayes examines half a fragment. 'Only half. Where is the rest?' You must lie (WIL save, hard) or tell a partial truth. If the lie fails: 'Whatever deal you made with Zhou ends here. Clear?' No immediate penalty but you are under observation."),
    sp(1),
    p("**Mission failed:** Hayes says nothing for 10 seconds. Then: 'Get out. Now.' Formal hearing tomorrow. -2 Loyalty. Pay suspended 1 week."),
    sp(2),
    h3("Campaign Hook"),
    p("Hayes says: 'Chicago was not random. Temporal zones are increasing. Five new zones in the last month. Someone is deliberately activating this instability. Someone with access to Oculus fragments. Zhou? A hostile government? Something inside the Division itself? Find out. Before Vegas becomes like Chicago.'"),
    pb(),
    ]

    # ════════════════════════════════
    # ADVENTURE 2: THE FIRST FOUR WEEKS
    # ════════════════════════════════
    s += [h1("The First Four Weeks"), rule(),
    p("A **4-session mini-campaign** (2-3 hours each) showing how all systems interact: economy, contamination, loyalty, corruption, and moral choices. Unlike the Chicago Loop (a single action-focused adventure), this campaign makes you *feel time passing*. Debt grows. Zhou knocks. Contamination accumulates. Characters change, literally."),
    sp(1),
    note("The Warden keeps an accounting sheet for each PC: pay, expenses, debt, loyalty, corruption, contamination, Quirks. Update between sessions. Players must see the numbers. The spiral is more effective when it is transparent."),
    sp(3),
    h2("Session 1: The Arrival (Weeks 1-2)"),
    h3("Scene 1: Welcome Briefing"),
    p("Hayes receives the PCs in her office. Efficient, cold, professional. She explains pay ($800/week), expenses ($900/week total), and standard equipment. The deficit of $100/week is never mentioned. The PCs discover it when they do the math."),
    sp(1),
    note("Hayes is not evil. She is a bureaucrat doing her job. When a PC asks 'how do you survive on $800 a week?', Hayes answers: 'With discipline and priorities, agent.' She is not lying. It simply is not her problem."),
    sp(2),
    h3("Scene 2: First Mission (Yellow Zone)"),
    p("**Objective:** Recover a crate of biological samples from a warehouse 12 km from base. WIL save after 8 hours in zone. With suit, risk is low but real."),
    sp(1),
    p("**Complication (Warden's choice):**"),
    b("**Social:** Inside the warehouse is a civilian family taking shelter. The crate is under their belongings. Taking it leaves them without shelter."),
    b("**Tactical:** The warehouse is watched by 2 armed scavengers (4 HP, 10 STR, 12 DEX, 8 WIL, pistol d6). Fight is risky. Negotiate is possible. Flanking costs time."),
    b("**Moral:** The crate also contains an unregistered Oculus fragment. Nobody knows it is there. Worth $3,000 on the black market."),
    sp(1),
    p("**Week 1 accounting:** If mission completed, $800 pay + $290 bonus = $1,090 income. Expenses $900. Balance: +$190. Debt drops from -$500 to -$310. PCs feel almost good. Almost."),
    sp(1),
    p("**Week 2:** No mission. Pay $800. Expenses $900. Unexpected expense (roll d6). Week balance: around -$200. Debt back to -$510. PCs realize that one week without a mission digs the hole deeper."),
    sp(3),
    h2("Session 2: The Pressure (Weeks 3-4)"),
    h3("Scene 1: Two Missions Offered"),
    p("Hayes offers two missions. PCs can only choose one."),
    sp(1),
    p("**Mission A: Yellow Zone, routine.** Escort a tech installing sensors. Low risk. Base $50 + bonus $100."),
    sp(1),
    p("**Mission B: Red Zone, dangerous.** Data recovery from a collapsed lab on the Strip. 3 confirmed echoes. Base $50 + bonus $400 + red zone bonus $200. But contamination is severe: WIL save every 3 hours, d4 damage, 2 checks guaranteed. A Quirk is nearly certain."),
    sp(2),
    h3("Scene 2: Zhou's First Offer"),
    p("If any PC's debt exceeds -$700 (it will by week 4 without extra missions), Zhou makes contact. A handwritten note on perfumed paper in their mailbox."),
    sp(1),
    p("*'Dear Agent [name]. I have noticed the Division does not sufficiently appreciate your services. I have a small assignment that could solve your financial problems. Nothing dangerous. $1,500 for one hour of your time. You know my address. Regards, M. Zhou.'*"),
    sp(1),
    p("If the PC goes: carry a sealed package from point A to B. Do not open it, do not ask questions. Pay: $1,500 cash. Corruption: +1. If they refuse, Zhou does not insist. She waits. The offers get worse as debt grows."),
    sp(3),
    h2("Session 3: The Fall (Weeks 5-7)"),
    p("This is the session where the game bares its teeth."),
    sp(2),
    h3("Scene 1: The Mission Goes Wrong"),
    p("Hayes sends the group to a Red Zone. No choice: it is an order. A previous squad did not come back. The Division wants to know why. Underground laboratory beneath the Luxor. Severe contamination. 4-6 temporal echoes. A corridor where time flows backward."),
    sp(1),
    p("What they find: bodies of 2 agents from the previous squad. 1 surviving agent, hidden, traumatized, with 2 visible Quirks. The data, intact, in an armored briefcase. A class-B Oculus fragment Hayes did not mention."),
    sp(1),
    p("**The combat:** 4 temporal echoes (4 HP, 8 STR, 12 DEX, 6 WIL, temporal claw d6, WIL save on critical damage or accelerated aging). This is the hardest fight yet."),
    sp(1),
    note("To the Warden: this is the scene where a PC probably dies. Do not force it, but do not protect them either. Death has weight because it is real."),
    sp(2),
    h3("Scene 2: The Fragment Dilemma"),
    p("Hayes asks for the data. She gets it. The Oculus fragment is not in any report. If PCs mention it, Hayes takes it without comment. If they do not mention it, they have an unregistered class-B fragment. Zhou would pay $5,000. The Division does not know it exists. +1 Loyalty if they hand over everything. +2 Corruption if they keep the fragment."),
    sp(3),
    h2("Session 4: Who Are You? (Weeks 8-10)"),
    h3("Scene 1: Zhou Collects"),
    p("If anyone worked for Zhou previously, she asks a second, bigger favor. The PC who said yes the first time is in a weak position: Zhou knows things. If nobody worked for Zhou, she raises the offer to $3,000-5,000. For a PC with $1,500 in debt and eviction imminent, that changes everything."),
    sp(1),
    p("**Zhou's job (if accepted):** Sabotage a Division convoy. Do not kill anyone, just delay it. Zhou wants to reach an Oculus fragment first. Corruption: +3. If discovered: fired from the Division."),
    sp(2),
    h3("Scene 2: The Division Demands"),
    p("Hayes convenes the group. Monthly results are below expectations. The Division spent more on them than they recovered. Hayes offers a final bonus mission: Red Zone, high risk, $600 bonus. If they succeed, the month breaks even. If they refuse, the Division 'reevaluates their contract.'"),
    sp(1),
    p("Not a threat of death. A threat of termination. And a fired Division agent with Quirks and medicine dependency has nowhere to go."),
    sp(2),
    h3("Scene 3: The Final Choice"),
    b("**Division mission + refuse Zhou:** Loyal, poor, contaminated, but employed."),
    b("**Division mission + work for Zhou:** Playing both sides. Enormous risk, enormous potential gain."),
    b("**Zhou only:** High corruption, money, but no safety net."),
    b("**Neither:** Fired by the Division, ignored by Zhou. Alone in Vegas with Quirks and no medicine."),
    sp(2),
    p("There is no right ending. There is the ending the PCs choose, and the consequences that follow."),
    sp(3),
    h2("Final Accounting (Example)"),
    p("For a PC who did all Division missions and refused Zhou:"),
    sp(1),
    T(["Week","Income","Expenses","Balance","Debt"],
      [["Start","","","","-$500"],
       ["1","$1,090","$900","+$190","-$310"],
       ["2","$800","$1,000","-$200","-$510"],
       ["3","$950","$900","+$50","-$460"],
       ["4","$800","$950","-$150","-$610"],
       ["5-6","$1,350","$1,800","-$450","-$1,060"],
       ["7","$800","$900","-$100","-$1,160"],
       ["8","$1,400","$900","+$500","-$660"]],
      [FW*0.10, FW*0.14, FW*0.14, FW*0.14, FW*0.14], full=True),
    sp(2),
    note("After 8 weeks: debt -$660, 1-2 Quirks, Loyalty 7-8, Corruption 0. Loyal, poor, contaminated. Two months of doing everything right and you are still $660 in the hole. Zhou watches. Waits. *This is the question the game asks every table: how much is your soul worth when rent is three weeks overdue?*"),
    pb(),
    ]

    # ════════════════════════════════
    # REFERENCE
    # ════════════════════════════════
    s += [h1("Reference"), rule(),
    h2("Character Creation Checklist"),
    b("Roll 3d6 for STR, DEX, WIL (may swap two)"),
    b("Roll 1d6 for HP"),
    b("Choose or roll background (d6)"),
    b("Note standard gear + background package (10 slots total)"),
    b("Set trackers: Loyalty 5, Corruption 0, Debt -$500, Tier: Recruit"),
    b("Roll traits: Physique, Face, Speech, Vice, Virtue (d10 each)"),
    b("Answer three narrative questions"),
    sp(3),
    h2("Weekly Accounting Checklist"),
    b("Receive weekly pay (by tier)"),
    b("Add guaranteed mission bonus (+$50)"),
    b("Add performance bonuses if applicable"),
    b("Add any side gig income"),
    b("Subtract mandatory expenses ($900 total)"),
    b("Apply 5% interest on negative debt balance"),
    b("Warden rolls d6 for unexpected expenses"),
    b("Record final balance and update debt"),
    sp(3),
    KeepTogether([
    h2("Quick Combat Reference"),
    T(["Situation","Rule"],
      [["Initiative","DEX save. Fail: lose first turn."],
       ["Attack","Auto-hit. Roll damage minus Armor = HP loss."],
       ["Multiple attackers same target","Roll all dice, keep single highest."],
       ["Impaired","d4 regardless of weapon."],
       ["Enhanced","d12 regardless of weapon."],
       ["HP exactly 0","Roll Scars table."],
       ["HP below 0","Overflow to STR. STR save vs critical damage."],
       ["STR 0","Death."],
       ["WIL 0 (contamination)","Temporal echo. Character lost."],
       ["WIL 0 (other)","Catatonia. 1 week medical care."],
       ["Retreat","DEX save + safe destination."],
       ["Morale","WIL save: 1st casualty, then half strength."]],
      [CW*0.40, CW*0.60]),
    ]),
    sp(3),
    KeepTogether([
    h2("Key Numbers"),
    T(["What","Value"],
      [["Save","d20 equal to or under attribute"],
       ["Max Armor","3"],
       ["HP recovery","Rest + water (minutes)"],
       ["Attribute recovery","1 week + medical care"],
       ["WIL recovery (contamination)","d6 per week Division care (d8 at Loyalty 7+)"],
       ["Advantage","Roll 2d20, keep lower"],
       ["Disadvantage","Roll 2d20, keep higher"],
       ["Contamination (orange)","WIL save every 6 hours"],
       ["Max Quirks","5 (6th = echo)"],
       ["Recruit pay","$800/week"],
       ["Fixed expenses","$900/week"],
       ["Starting debt","-$500"],
       ["Starting Loyalty","5"],
       ["Starting Corruption","0"],
       ["Instability threshold","|Loyalty - Corruption| <= 2"]],
      [CW*0.50, CW*0.50]),
    ]),
    sp(3),
    h2("Hack This Hack"),
    p("To move the system to any other setting, redefine five elements. Everything else transfers unchanged."),
    sp(1),
    T(["Variable","In Las Vegas 2080","What to Redefine"],
      [["The employer","The Division / Hayes","Who pays, what currency, hierarchy, power to punish"],
       ["The corruptor","Madame Zhou / certificates","Who offers the shortcut, at what cost, what they want"],
       ["Corrosive force","Temporal exposure / WIL","What degrades characters, which attribute, how it manifests"],
       ["The deficit","-$50-100/week at Recruit","Which resource is structurally insufficient and why"],
       ["The echo","Temporal echo (hostile NPC)","What a character becomes when corruption fully consumes them"]],
      [CW*0.22, CW*0.30, CW*0.48]),
    sp(2),
    note("What does NOT need to change: the save system (d20 under attribute), the Cairn combat engine, the Quirk structure, the Loyalty/Corruption dual tracker with intermediate thresholds, the inventory system, the contamination mechanic, the tier progression."),
    sp(3),
    p("*Based on Cairn by Yochai Gal (cairnrpg.com), used under CC BY-SA 4.0. Uchronies & Treasures is released under CC BY-SA 4.0. Original Italian edition: Ucronie e Tesori, by Riccardo Scaringi, ilgiocointavolo.it.*"),
    ]

    return s


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    from pypdf import PdfReader, PdfWriter
    import io

    import pathlib
    here = pathlib.Path.cwd()
    outpath = str(here / "UeT_Complete.pdf")
    doc = UeTDoc(outpath)

    # Build TOC correctly
    doc.toc = doc.toc  # reference stored in doc

    content = story()

    # Insert TOC object into story at position 2 (after blank and before content)
    # Replace the placeholder
    for i, item in enumerate(content):
        if isinstance(item, TableOfContents):
            content[i] = doc.toc

    doc.multiBuild(content)
    print(f"Main content built: {outpath}")

    # Build and merge cover
    cover_buf = make_cover_pdf()
    cover_r = PdfReader(cover_buf)
    main_r  = PdfReader(outpath)

    writer = PdfWriter()
    writer.add_page(cover_r.pages[0])
    for i, pg in enumerate(main_r.pages):
        if i == 0: continue  # skip blank cover placeholder
        writer.add_page(pg)

    final = str(here / "UeT_Final_Complete.pdf")
    with open(final, "wb") as f:
        writer.write(f)

    r = PdfReader(final)
    import os
    print(f"\nFinal PDF: {len(r.pages)} pages")
    print(f"Size: {os.path.getsize(final)/1024:.0f} KB")
    print(f"File: {final}")

if __name__ == "__main__":
    main()
