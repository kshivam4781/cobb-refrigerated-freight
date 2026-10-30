"""Generates the COBB logo concepts as pure-vector SVGs (text converted to outlines).

Usage: python -I design/build_logos.py <fonts_dir>
Writes design/concepts/*.svg and design/concepts.html for side-by-side review.
"""
import math
import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

FONTS = Path(sys.argv[1])
OUT = Path(__file__).parent / "concepts"
OUT.mkdir(exist_ok=True)

NAVY = "#0B2A5B"
BLUE = "#1565D8"
ICE = "#38B6FF"

montserrat = instantiateVariableFont(TTFont(FONTS / "Montserrat.ttf"), {"wght": 800})
barlow = TTFont(FONTS / "BarlowCondensed-SemiBold.ttf")
barlow_xb = TTFont(FONTS / "BarlowCondensed-ExtraBold.ttf")


def text_path(font, text, x, y, size, tracking=0.0, anchor="start"):
    """Return (svg path d, advance width) for text with baseline at y."""
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    scale = size / font["head"].unitsPerEm
    names = [cmap[ord(ch)] for ch in text]
    width = sum(gs[n].width * scale for n in names) + tracking * size * (len(names) - 1)
    if anchor == "middle":
        x -= width / 2
    elif anchor == "end":
        x -= width
    pen = SVGPathPen(gs)
    cx = x
    for n in names:
        tp = TransformPen(pen, (scale, 0, 0, -scale, cx, y))
        gs[n].draw(tp)
        cx += gs[n].width * scale + tracking * size
    return pen.getCommands(), width


def snowflake(cx, cy, r, color, sw):
    """Six-armed snowflake made of round-capped strokes."""
    parts = []
    for i in range(6):
        a = math.radians(90 + i * 60)
        ex, ey = cx + r * math.cos(a), cy - r * math.sin(a)
        parts.append(f"M{cx:.2f} {cy:.2f}L{ex:.2f} {ey:.2f}")
        for t, blen in ((0.42, 0.34), (0.7, 0.24)):
            bx, by = cx + r * t * math.cos(a), cy - r * t * math.sin(a)
            for s in (-1, 1):
                ba = a + s * math.radians(45)
                parts.append(
                    f"M{bx:.2f} {by:.2f}L{bx + r * blen * math.cos(ba):.2f} {by - r * blen * math.sin(ba):.2f}"
                )
    return (f'<path d="{"".join(parts)}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')


def c_arc(cx, cy, r, w, gap_deg, color):
    """Thick 'C' ring segment opening to the right, as a filled path."""
    ro, ri = r + w / 2, r - w / 2
    a0, a1 = math.radians(gap_deg / 2), math.radians(360 - gap_deg / 2)
    p = lambda rad, a: (cx + rad * math.cos(a), cy - rad * math.sin(a))
    (x1, y1), (x2, y2) = p(ro, a0), p(ro, a1)
    (x3, y3), (x4, y4) = p(ri, a1), p(ri, a0)
    return (f'<path d="M{x1:.2f} {y1:.2f}A{ro} {ro} 0 1 0 {x2:.2f} {y2:.2f}'
            f'L{x3:.2f} {y3:.2f}A{ri} {ri} 0 1 1 {x4:.2f} {y4:.2f}Z" fill="{color}"/>')


def mark_a(x, y, s, navy=NAVY, ice=ICE):
    """Concept A mark: bold C wrapped around a snowflake. Box is s x s at (x, y)."""
    c = s / 2
    return (c_arc(x + c, y + c, s * 0.38, s * 0.22, 80, navy)
            + snowflake(x + c + s * 0.04, y + c, s * 0.225, ice, s * 0.034))


def svg(w, h, body, bg=None):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">{rect}{body}</svg>')


def concept_a(dark=False):
    navy = "#FFFFFF" if dark else NAVY
    sub = ICE
    body = mark_a(0, 0, 120, navy, ICE)
    d1, w1 = text_path(montserrat, "COBB", 138, 72, 64, 0.02)
    d2, w2 = text_path(barlow, "REFRIGERATED FREIGHT", 140, 104, 25.5, 0.14)
    body += f'<path d="{d1}" fill="{navy}"/><path d="{d2}" fill="{sub}"/>'
    return svg(int(140 + max(w1, w2)) + 4, 120, body)


def concept_b():
    w, h = 220, 250
    shield = (f'<path d="M110 6 L206 34 V118 C206 182 164 222 110 244 C56 222 14 182 14 118 V34 Z" '
              f'fill="{NAVY}"/>'
              f'<path d="M110 20 L192 44 V118 C192 172 157 206 110 226 C63 206 28 172 28 118 V44 Z" '
              f'fill="none" stroke="{ICE}" stroke-width="4"/>')
    d1, _ = text_path(montserrat, "COBB", 110, 92, 50, 0.02, "middle")
    d2, _ = text_path(barlow, "REFRIGERATED", 110, 198, 17, 0.16, "middle")
    d3, _ = text_path(barlow, "FREIGHT", 110, 217, 17, 0.2, "middle")
    body = (shield + f'<path d="{d1}" fill="#fff"/>'
            + f'<rect x="40" y="104" width="140" height="4" fill="{ICE}"/>'
            + snowflake(110, 148, 30, ICE, 5.5)
            + f'<path d="{d2}{d3}" fill="#fff"/>')
    return svg(w, h, body)


def concept_c():
    # Reefer truck silhouette with speed lines, wordmark below.
    t = []
    t.append(f'<rect x="70" y="10" width="190" height="70" rx="5" fill="{NAVY}"/>')  # trailer
    t.append(f'<rect x="58" y="22" width="14" height="40" rx="3" fill="{BLUE}"/>')  # reefer unit
    t.append(f'<path d="M10 80 V48 C10 40 14 34 22 32 L44 28 C50 27 54 30 54 36 V80 Z" fill="{NAVY}"/>')  # cab
    t.append(f'<path d="M18 46 L44 42 V54 H18 Z" fill="#fff"/>')  # window
    for cx in (30, 200, 232):
        t.append(f'<circle cx="{cx}" cy="86" r="10" fill="{NAVY}"/><circle cx="{cx}" cy="86" r="4" fill="#fff"/>')
    for i, (y, l) in enumerate(((24, 60), (40, 80), (56, 50))):
        t.append(f'<rect x="{285}" y="{y}" width="{l}" height="6" rx="3" fill="{ICE}" opacity="{1 - i * 0.2}"/>')
    t.append(snowflake(165, 45, 22, ICE, 4.5))
    d1, w1 = text_path(barlow_xb, "COBB", 180, 168, 78, 0.04, "middle")
    d2, _ = text_path(barlow, "REFRIGERATED FREIGHT", 180, 196, 22, 0.18, "middle")
    body = "".join(t) + f'<path d="{d1}" fill="{NAVY}"/><path d="{d2}" fill="{BLUE}"/>'
    return svg(370, 206, body)


def concept_d():
    # Wordmark with snowflake replacing the O.
    dc, wc = text_path(montserrat, "C", 0, 70, 80)
    o_r = 30
    o_cx = wc + 8 + o_r
    ring = (f'<circle cx="{o_cx}" cy="{70 - 29}" r="{o_r}" fill="none" stroke="{NAVY}" stroke-width="12"/>'
            + snowflake(o_cx, 70 - 29, 17, ICE, 4.5))
    dbb, wbb = text_path(montserrat, "BB", o_cx + o_r + 10, 70, 80)
    total = o_cx + o_r + 10 + wbb
    d2, _ = text_path(barlow, "REFRIGERATED FREIGHT", total / 2, 112, 25, 0.24, "middle")
    body = (f'<path d="{dc}{dbb}" fill="{NAVY}"/>' + ring
            + f'<rect x="0" y="84" width="{total}" height="5" fill="{ICE}"/>'
            + f'<path d="{d2}" fill="{NAVY}"/>')
    return svg(int(total) + 2, 120, body)


concepts = {
    "A — C + Snowflake": concept_a(),
    "B — Shield Badge": concept_b(),
    "C — Reefer Truck": concept_c(),
    "D — Snowflake Wordmark": concept_d(),
}
for i, (name, s) in enumerate(concepts.items()):
    (OUT / f"concept-{'abcd'[i]}.svg").write_text(s, encoding="utf-8")

cards = "".join(
    f'<figure><div class="box">{s}</div><figcaption>{n}</figcaption></figure>' for n, s in concepts.items()
)
(Path(__file__).parent / "concepts.html").write_text(
    "<!doctype html><meta charset=utf-8><title>COBB logo concepts</title><style>"
    "body{font-family:system-ui;margin:24px;background:#eef2f7}main{display:grid;grid-template-columns:1fr 1fr;gap:20px}"
    "figure{margin:0;background:#fff;border-radius:12px;padding:24px;box-shadow:0 2px 8px #0001}"
    ".box{height:220px;display:flex;align-items:center;justify-content:center}.box svg{max-width:100%;max-height:100%}"
    "figcaption{text-align:center;margin-top:12px;font-weight:600;color:#334}"
    ".dark{background:#0B2A5B}.dark figcaption{color:#cde}</style><main>" + cards
    + f'<figure class="dark"><div class="box">{concept_a(dark=True)}</div><figcaption>A on navy</figcaption></figure>'
    + "</main>",
    encoding="utf-8",
)
# Final brand files from the chosen concept (A).
BRAND = Path(__file__).parent.parent / "assets" / "brand"
BRAND.mkdir(parents=True, exist_ok=True)
(BRAND / "logo.svg").write_text(concept_a(), encoding="utf-8")
(BRAND / "logo-white.svg").write_text(concept_a(dark=True), encoding="utf-8")
(BRAND / "mark.svg").write_text(svg(120, 120, mark_a(0, 0, 120)), encoding="utf-8")
(BRAND / "mark-white.svg").write_text(svg(120, 120, mark_a(0, 0, 120, "#FFFFFF")), encoding="utf-8")
# App/favicon tile: white mark on a navy rounded square.
tile = f'<rect width="120" height="120" rx="26" fill="{NAVY}"/>' + mark_a(14, 14, 92, "#FFFFFF")
(BRAND / "favicon.svg").write_text(svg(120, 120, tile), encoding="utf-8")
print("ok")
