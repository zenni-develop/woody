#!/usr/bin/env python3
"""Original illustrations for the Cafe Kosame page (SVG, no external assets).

Style: flat gouache-like shapes, soft grain, the page palette (leaf greens,
sage, blush, warm wood). Deterministic: the same seed draws the same picture.
    python3 tools/illustrations.py   → public/images/*.svg
"""
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "public" / "images"

C = dict(
    paper="#F7F9F4", wall="#EEF3EA", glass="#DCEAE4", glass2="#CFE2DA", frame="#A9BFA5",
    leaf_dk="#2F5A2B", leaf="#3B6A34", leaf_md="#5E8C4F", leaf_lt="#8DB570", sage="#BCD3AE",
    wood="#C99A6B", wood_dk="#A97C52", wood_lt="#E2C7A4", floor="#EADCC6",
    pot="#D98E6A", pot_dk="#BE7454", pot_w="#EFEDE6", pot_w2="#DCD8CD",
    blush="#F6E7DC", blush2="#EFD5C4", cream="#FBF6EC",
    matcha="#9DBB5E", matcha_dk="#7FA046", foam="#E8EDCB",
    hojicha="#9A6A45", hojicha_lt="#C79A72", milk="#F4ECDD",
    mitarashi="#B8743A", glaze="#D89648", dango_g="#A9C77A", dango_b="#EADBB9",
    fig="#6E3D5C", fig_lt="#8C5677", fig_in="#E58A78", fig_core="#F6D7C3", seed="#F3C7A6",
    linen="#EFE6DA", linen2="#E4D8C8", sun="#F2C75C", tomato="#E2674A", sky="#EAF3F4",
    ink="#1E3327",
)


def defs(extra=""):
    return f"""<defs>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7" stitchTiles="stitch"/>
    <feColorMatrix values="0 0 0 0 0.12  0 0 0 0 0.2  0 0 0 0 0.15  0 0 0 0.07 0"/>
  </filter>
  <symbol id="leaf" viewBox="-12 -50 24 52" overflow="visible">
    <path d="M0 0C11-12 11-34 0-48C-11-34-11-12 0 0Z"/>
  </symbol>
  <symbol id="heart" viewBox="-20 -36 40 38" overflow="visible">
    <path d="M0 0C12-6 18-22 8-32C4-36 0-34 0-30C0-34-4-36-8-32C-18-22-12-6 0 0Z"/>
  </symbol>
  {extra}
</defs>"""


def svg(w, h, body, title, extra_defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">'
            f"<title>{title}</title>{defs(extra_defs)}{body}"
            f'<rect width="{w}" height="{h}" filter="url(#grain)" pointer-events="none"/></svg>\n')


def leaf(x, y, ang, s, fill, vein=None):
    v = f'<path d="M0 -2L0 -44" stroke="{vein}" stroke-width="{1.4/s:.2f}" opacity=".55" fill="none"/>' if vein else ""
    return (f'<g transform="translate({x:.1f} {y:.1f}) rotate({ang:.1f}) scale({s:.2f})" fill="{fill}">'
            f'<path d="M0 0C11-12 11-34 0-48C-11-34-11-12 0 0Z"/>{v}</g>')


def heart(x, y, ang, s, fill):
    return (f'<g transform="translate({x:.1f} {y:.1f}) rotate({ang:.1f}) scale({s:.2f})" fill="{fill}">'
            f'<path d="M0 0C12-6 18-22 8-32C4-36 0-34 0-30C0-34-4-36-8-32C-18-22-12-6 0 0Z"/></g>')


def monstera(x, y, ang, s, fill, bg):
    """Big split leaf: heart shape with a few paper-coloured slits and a midrib."""
    slits = "".join(
        f'<path d="M{sx} {sy}L{sx*1.7:.0f} {sy-6}" stroke="{bg}" stroke-width="5" stroke-linecap="round"/>'
        for sx, sy in [(-22, -30), (-28, -55), (-22, -80), (22, -34), (28, -60), (20, -86)]
    )
    return (f'<g transform="translate({x:.1f} {y:.1f}) rotate({ang:.1f}) scale({s:.2f})">'
            f'<path fill="{fill}" d="M0 0C38-6 62-40 54-80C48-108 22-122 4-116C2-120-2-120-4-116C-22-122-48-108-54-80C-62-40-38-6 0 0Z"/>'
            f'{slits}<path d="M0 -4L0 -110" stroke="{bg}" stroke-width="3" opacity=".5"/></g>')


def vine(rng, x, y, length, sway, n, greens):
    pts, out = [], []
    for i in range(n + 1):
        t = i / n
        px = x + math.sin(t * math.pi * 1.4) * sway
        py = y + t * length
        pts.append((px, py))
    d = "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in pts)
    out.append(f'<path d="{d}" stroke="{C["leaf_md"]}" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
    for i, (px, py) in enumerate(pts[1:], 1):
        side = -1 if i % 2 else 1
        out.append(heart(px + side * 4, py, side * rng.uniform(40, 80) + 180, rng.uniform(0.55, 0.85), rng.choice(greens)))
    return "".join(out)


def pot(x, y, w, h, fill, rim):
    return (f'<path d="M{x-w/2} {y}L{x+w/2} {y}L{x+w*0.38} {y+h}L{x-w*0.38} {y+h}Z" fill="{fill}"/>'
            f'<rect x="{x-w/2-4}" y="{y-8}" width="{w+8}" height="12" rx="3" fill="{rim}"/>')


def bush(rng, cx, base, spread, height, n, greens, scale=(0.8, 1.3)):
    out = []
    for _ in range(n):
        a = rng.uniform(-70, 70)
        r = rng.uniform(0.3, 1.0)
        x = cx + math.sin(math.radians(a)) * spread * r * 0.6
        y = base - rng.uniform(0, height * 0.35)
        out.append(leaf(x, y, a, rng.uniform(*scale), rng.choice(greens), C["sage"]))
    return "".join(out)


def rain(rng, x0, y0, x1, y1, n, alpha=0.6, length=(14, 30)):
    dark, light = [], []
    for _ in range(n):
        x = rng.uniform(x0, x1); y = rng.uniform(y0, y1); L = rng.uniform(*length)
        dark.append(f'<path d="M{x:.0f} {y:.0f}l{-L*0.25:.1f} {L:.1f}"/>')
        light.append(f'<path d="M{x+1.5:.1f} {y:.0f}l{-L*0.25:.1f} {L:.1f}"/>')
    return (f'<g stroke="#9FBDB5" stroke-width="2.2" stroke-linecap="round" opacity="{alpha*0.8:.2f}">{"".join(dark)}</g>'
            f'<g stroke="#fff" stroke-width="1.6" stroke-linecap="round" opacity="{alpha}">{"".join(light)}</g>')


# --------------------------------------------------------------------------------------------
def hero():
    """Greenhouse tearoom: glass roof with light rain, hanging vines, a big monstera, a table set
    with matcha and dango. The left ~40% stays calm for the page title on desktop."""
    W, H = 1500, 1000
    rng = random.Random(3)
    g = [C["leaf_dk"], C["leaf"], C["leaf_md"], C["leaf_lt"]]
    b = [f'<rect width="{W}" height="{H}" fill="{C["wall"]}"/>']
    # glass roof + wall panes on the right
    panes = []
    for col in range(7):
        x = 560 + col * 140
        for row in range(4):
            y = 40 + row * 150
            panes.append(f'<rect x="{x}" y="{y}" width="132" height="142" rx="4"/>')
    b.append(f'<clipPath id="panes">{"".join(panes)}</clipPath>')
    b.append(f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["glass2"]}"/><stop offset="1" stop-color="{C["sky"]}"/></linearGradient>')
    b.append(f'<rect x="548" y="28" width="{W-548}" height="636" fill="{C["frame"]}" opacity=".55"/>')
    b.append(f'<g fill="url(#sky)">{"".join(panes)}</g>')
    # soft outside greenery seen through glass
    out_trees = "".join(f'<circle cx="{rng.uniform(560,1500):.0f}" cy="{rng.uniform(470,640):.0f}" r="{rng.uniform(50,110):.0f}" fill="{C["sage"]}" opacity=".7"/>' for _ in range(14))
    b.append(f'<g clip-path="url(#panes)">{out_trees}{rain(rng, 560, 30, 1500, 650, 230, 0.75)}</g>')
    # sunlight on the left wall
    b.append(f'<path d="M80 0L420 0L300 1000L0 1000L0 260Z" fill="#fff" opacity=".35"/>')
    b.append(f'<circle cx="190" cy="150" r="70" fill="{C["sun"]}" opacity=".18"/>')
    # beam with hanging plants
    b.append(f'<rect x="520" y="300" width="{W-520}" height="16" fill="{C["wood_dk"]}"/>')
    for hx, L, sway in [(640, 300, 18), (760, 220, -14), (900, 340, 20), (1040, 260, -16), (1190, 330, 14), (1330, 240, -12)]:
        b.append(f'<path d="M{hx} 316L{hx} 360" stroke="{C["wood_dk"]}" stroke-width="2"/>')
        b.append(vine(rng, hx, 380, L, sway, 9, g))
        b.append(f'<path d="M{hx-40} 350Q{hx} 410 {hx+40} 350Z" fill="{C["pot_w"]}"/>')
        b.append(bush(rng, hx, 360, 90, 60, 14, g, (0.6, 0.95)))
        b.append(vine(rng, hx - 22, 372, L * 0.6, -sway * 0.7, 6, g))
    # floor
    b.append(f'<rect y="820" width="{W}" height="180" fill="{C["floor"]}"/>')
    b.append(f'<rect y="816" width="{W}" height="8" fill="{C["wood_lt"]}"/>')
    # soft floor shadows
    b.append(f'<g fill="{C["ink"]}" opacity=".08"><ellipse cx="1340" cy="884" rx="150" ry="20"/><ellipse cx="975" cy="826" rx="250" ry="14"/><ellipse cx="610" cy="864" rx="90" ry="12"/><ellipse cx="830" cy="892" rx="70" ry="10"/></g>')
    # extra floor plants between table and monstera
    b.append(pot(830, 830, 90, 60, C["pot_w"], C["pot_w2"]) + bush(rng, 830, 820, 140, 120, 18, g, (0.9, 1.3)))
    b.append(pot(1205, 840, 80, 52, C["pot"], C["pot_dk"]))
    b.append("".join(f'<circle cx="{1205+math.cos(a)*36:.0f}" cy="{790+math.sin(a)*24:.0f}" r="17" fill="{C["leaf_lt"] if i%2 else C["leaf_md"]}"/>' for i, a in enumerate([i*0.8 for i in range(8)])))
    # big monstera (right) — sits under the vertical 小雨
    b.append(pot(1340, 760, 150, 120, C["pot"], C["pot_dk"]))
    for x, y, a, s, f in [(1340, 760, -10, 2.4, C["leaf_dk"]), (1290, 700, -42, 2.0, C["leaf"]), (1395, 690, 34, 2.1, C["leaf_dk"]),
                          (1250, 600, -24, 1.7, C["leaf_md"]), (1430, 600, 20, 1.8, C["leaf"]), (1340, 560, 4, 1.9, C["leaf_dk"]),
                          (1460, 760, 70, 1.5, C["leaf_md"])]:
        b.append(monstera(x, y, a, s, f, C["wall"]))
    # tall leafy plant mid-left of the scene
    b.append(pot(610, 770, 110, 90, C["pot_w"], C["pot_w2"]))
    b.append(f'<g stroke="{C["leaf_md"]}" stroke-width="3">' + "".join(f'<path d="M610 765Q{610+dx} {650} {610+dx*1.4} {520+abs(dx)}" fill="none"/>' for dx in (-40, -10, 25, 55)) + "</g>")
    b.append(bush(rng, 610, 640, 220, 260, 30, g, (1.0, 1.6)))
    # table, chairs, tea set
    b.append(f'<g fill="{C["wood"]}"><rect x="760" y="660" width="430" height="22" rx="6"/><rect x="800" y="682" width="14" height="140"/><rect x="1136" y="682" width="14" height="140"/></g>')
    for cx in (730, 1215):
        b.append(f'<g fill="none" stroke="{C["wood_dk"]}" stroke-width="7" stroke-linecap="round"><path d="M{cx-30} 822L{cx-30} 700Q{cx} 640 {cx+30} 700L{cx+30} 822"/><path d="M{cx-36} 740L{cx+36} 740"/></g>')
    # matcha bowl
    b.append(f'<path d="M860 660Q860 610 905 610L955 610Q1000 610 1000 660Z" fill="{C["pot_w"]}"/><ellipse cx="930" cy="612" rx="70" ry="10" fill="{C["matcha"]}"/>')
    # dango plate
    b.append(f'<ellipse cx="1090" cy="656" rx="72" ry="10" fill="#fff"/>')
    for i, (col, gl) in enumerate([(C["mitarashi"], C["glaze"]), (C["dango_g"], None), (C["dango_b"], None)]):
        x = 1040 + i * 34
        b.append(f'<path d="M{x-6} 652L{x+40} 600" stroke="{C["wood_lt"]}" stroke-width="3"/>')
        for k in range(3):
            b.append(f'<circle cx="{x+6+k*11}" cy="{640-k*12}" r="9" fill="{col}"/>')
            if gl:
                b.append(f'<circle cx="{x+4+k*11}" cy="{637-k*12}" r="3" fill="{gl}"/>')
    # teapot
    b.append(f'<ellipse cx="1150" cy="640" rx="34" ry="24" fill="{C["leaf_md"]}"/><rect x="1136" y="608" width="28" height="8" rx="3" fill="{C["leaf"]}"/><path d="M1116 636Q1096 630 1094 616" stroke="{C["leaf_md"]}" stroke-width="7" fill="none" stroke-linecap="round"/>')
    # small potted herbs on the table
    b.append(pot(800, 640, 44, 22, C["pot"], C["pot_dk"]))
    b.append(bush(rng, 800, 628, 40, 20, 7, g, (0.35, 0.55)))
    # leaves hanging into frame, top-right
    for _ in range(26):
        b.append(leaf(rng.uniform(1180, 1520), rng.uniform(-20, 120), rng.uniform(140, 220), rng.uniform(1.0, 1.8), rng.choice(g), C["sage"]))
    # foreground leaves bottom-right for depth
    for _ in range(14):
        b.append(leaf(rng.uniform(1100, 1520), rng.uniform(930, 1040), rng.uniform(-60, 60), rng.uniform(2.2, 3.4), rng.choice([C["leaf_dk"], C["leaf"]]), C["leaf_md"]))
    return svg(W, H, "".join(b), "Greenhouse tearoom illustration")


def room():
    """Sunlit window with plants on shelves and a wooden stool (portrait)."""
    W, H = 800, 1000
    rng = random.Random(11)
    g = [C["leaf_dk"], C["leaf"], C["leaf_md"], C["leaf_lt"]]
    b = [f'<rect width="{W}" height="{H}" fill="{C["wall"]}"/>']
    b.append(f'<rect x="120" y="80" width="560" height="560" rx="10" fill="{C["frame"]}"/>')
    for r in range(2):
        for c in range(2):
            b.append(f'<rect x="{134+c*276}" y="{94+r*266}" width="262" height="252" rx="4" fill="{C["sky"]}"/>')
    b.append(f'<g fill="{C["sage"]}" opacity=".8"><circle cx="230" cy="560" r="90"/><circle cx="560" cy="580" r="120"/><circle cx="400" cy="610" r="80"/></g>')
    b.append(f'<path d="M134 94L250 94L134 260Z" fill="#fff" opacity=".5"/>')
    # sunlight patch on floor/wall
    b.append(f'<path d="M150 900L520 900L640 1000L180 1000Z" fill="{C["sun"]}" opacity=".18"/>')
    b.append(f'<rect y="860" width="{W}" height="140" fill="{C["floor"]}"/>')
    # shelves
    for y in (330, 520):
        b.append(f'<rect x="96" y="{y}" width="608" height="14" rx="3" fill="{C["wood"]}"/>')
    # plants on shelves
    b.append(pot(200, 296, 60, 34, C["pot_w"], C["pot_w2"]) + bush(rng, 200, 288, 70, 60, 10, g, (0.6, 0.9)))
    b.append(pot(560, 300, 52, 30, C["pot"], C["pot_dk"]))
    b.append(f'<g fill="{C["leaf_md"]}">' + "".join(f'<path d="M{548+i*8} 296Q{540+i*9} {230-i*6} {552+i*7} {200-i*4}Q{560+i*7} {240} {556+i*8} 296Z"/>' for i in range(4)) + "</g>")
    b.append(pot(380, 300, 46, 28, C["pot_w"], C["pot_w2"]))
    b.append(f'<g>' + "".join(f'<circle cx="{380+math.cos(a)*24:.0f}" cy="{262+math.sin(a)*16:.0f}" r="11" fill="{C["leaf_lt"]}"/>' for a in [i*0.9 for i in range(7)]) + "</g>")
    b.append(pot(290, 488, 64, 36, C["pot"], C["pot_dk"]) + vine(rng, 300, 496, 200, 10, 8, g) + bush(rng, 290, 478, 80, 60, 10, g, (0.6, 0.9)))
    b.append(pot(560, 488, 70, 38, C["pot_w"], C["pot_w2"]) + bush(rng, 560, 478, 100, 100, 14, g, (0.8, 1.2)))
    # stool with a big plant
    b.append(f'<g fill="{C["wood_dk"]}"><rect x="430" y="760" width="200" height="16" rx="4"/><rect x="450" y="776" width="12" height="110"/><rect x="598" y="776" width="12" height="110"/></g>')
    b.append(pot(530, 690, 110, 70, C["pot"], C["pot_dk"]))
    for x, y, a, s, f in [(530, 690, -30, 1.2, C["leaf_dk"]), (530, 680, 25, 1.3, C["leaf"]), (520, 640, -5, 1.1, C["leaf_md"])]:
        b.append(monstera(x, y, a, s, f, C["wall"]))
    b.append(pot(200, 830, 90, 60, C["pot_w"], C["pot_w2"]))
    b.append(f'<g fill="{C["leaf"]}">' + "".join(f'<path d="M{186+i*7} 826Q{176+i*10} {700-i*10} {192+i*6} {660-i*12}Q{204+i*6} {720} {196+i*7} 826Z"/>' for i in range(5)) + "</g>")
    return svg(W, H, "".join(b), "Sunlit window with plants illustration")


def matcha():
    """Top-down matcha latte with leaf latte art on a wooden table."""
    W, H = 1200, 900
    b = [f'<rect width="{W}" height="{H}" fill="{C["wood_lt"]}"/>']
    for i in range(9):
        b.append(f'<rect x="-50" y="{i*104}" width="{W+100}" height="100" fill="{C["wood"] if i%2 else C["wood_lt"]}" opacity=".35" transform="rotate(-8 600 450)"/>')
    b.append(f'<ellipse cx="610" cy="470" rx="300" ry="300" fill="{C["ink"]}" opacity=".08"/>')
    b.append(f'<circle cx="590" cy="450" r="290" fill="{C["pot_w"]}"/><circle cx="590" cy="450" r="250" fill="{C["pot_w2"]}"/>')
    b.append(f'<path d="M800 300Q900 260 920 340Q930 410 830 420" fill="none" stroke="#fff" stroke-width="34" stroke-linecap="round"/>')
    b.append(f'<circle cx="590" cy="450" r="215" fill="#fff"/><circle cx="590" cy="450" r="190" fill="{C["matcha"]}"/>')
    # rosetta art
    art = []
    for i in range(7):
        y = 340 + i * 30
        w = 120 - i * 14
        art.append(f'<path d="M{590-w} {y+20}Q590 {y-28} {590+w} {y+20}Q590 {y} {590-w} {y+20}Z" fill="{C["foam"]}"/>')
    art.append(f'<path d="M590 330L590 600" stroke="{C["matcha_dk"]}" stroke-width="5" stroke-linecap="round"/>')
    art.append(f'<circle cx="590" cy="320" r="26" fill="{C["foam"]}"/>')
    b.append("".join(art))
    b.append(f'<path d="M140 760L360 640" stroke="{C["pot_w2"]}" stroke-width="18" stroke-linecap="round"/><ellipse cx="380" cy="628" rx="38" ry="26" fill="{C["pot_w2"]}" transform="rotate(-28 380 628)"/>')
    b.append(leaf(1030, 840, -30, 3.2, C["leaf"], C["leaf_lt"]) + leaf(1080, 860, 20, 2.6, C["leaf_md"], C["leaf_lt"]))
    return svg(W, H, "".join(b), "Matcha latte illustration")


def dango():
    """Three dango skewers on a plate with pickled tomatoes."""
    W, H = 1200, 800
    b = [f'<rect width="{W}" height="{H}" fill="{C["blush"]}"/>']
    b.append(f'<circle cx="980" cy="120" r="220" fill="{C["sun"]}" opacity=".18"/>')
    b.append(f'<ellipse cx="610" cy="470" rx="470" ry="230" fill="{C["blush2"]}"/>')
    b.append(f'<ellipse cx="600" cy="450" rx="440" ry="205" fill="#fff"/><ellipse cx="600" cy="450" rx="380" ry="165" fill="{C["cream"]}"/>')
    sk = [(C["mitarashi"], C["glaze"], 330), (C["dango_g"], None, 440), (C["dango_b"], None, 550)]
    for col, gl, y in sk:
        b.append(f'<path d="M230 {y+70}L980 {y-90}" stroke="{C["wood_lt"]}" stroke-width="10" stroke-linecap="round"/>')
        for k in range(4):
            cx, cy = 380 + k * 120, y + 38 - k * 26
            b.append(f'<circle cx="{cx+6}" cy="{cy+10}" r="54" fill="{C["ink"]}" opacity=".07"/>')
            b.append(f'<circle cx="{cx}" cy="{cy}" r="54" fill="{col}"/>')
            b.append(f'<ellipse cx="{cx-18}" cy="{cy-20}" rx="16" ry="10" fill="#fff" opacity=".45"/>')
            if gl:
                b.append(f'<path d="M{cx-50} {cy-6}Q{cx} {cy-62} {cx+50} {cy-6}Q{cx+36} {cy+20} {cx+20} {cy+6}Q{cx} {cy+30} {cx-18} {cy+8}Q{cx-36} {cy+22} {cx-50} {cy-6}Z" fill="{gl}" opacity=".9"/>')
        if col == C["dango_b"]:
            b.append(f'<g fill="{C["wood"]}" opacity=".55">' + "".join(f'<circle cx="{380+k*120+dx}" cy="{y+38-k*26+dy}" r="3"/>' for k in range(4) for dx, dy in [(-20, -8), (10, -26), (24, 12), (-6, 24), (30, -6)]) + "</g>")
    for x, y in [(900, 560), (960, 520)]:
        b.append(f'<circle cx="{x}" cy="{y}" r="30" fill="{C["tomato"]}"/><ellipse cx="{x-10}" cy="{y-10}" rx="8" ry="5" fill="#fff" opacity=".5"/><path d="M{x-10} {y-28}L{x} {y-34}L{x+10} {y-28}" stroke="{C["leaf_md"]}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    return svg(W, H, "".join(b), "Dango skewers illustration")


def fig():
    """Whole and halved figs on linen (autumn)."""
    W, H = 1280, 720
    b = [f'<rect width="{W}" height="{H}" fill="{C["linen"]}"/>']
    for i in range(6):
        b.append(f'<path d="M0 {120+i*110}Q640 {90+i*110} {W} {140+i*110}" stroke="{C["linen2"]}" stroke-width="3" fill="none"/>')
    def whole(x, y, s, ang):
        return (f'<g transform="translate({x} {y}) rotate({ang}) scale({s})">'
                f'<ellipse cx="8" cy="12" rx="90" ry="84" fill="{C["ink"]}" opacity=".08"/>'
                f'<path d="M0 -120C22-120 26-96 30-80C80-60 96-10 86 30C74 80 30 96 0 96C-30 96-74 80-86 30C-96-10-80-60-30-80C-26-96-22-120 0-120Z" fill="{C["fig"]}"/>'
                f'<path d="M-40 -40C-60 0-56 50-30 80" stroke="{C["fig_lt"]}" stroke-width="10" fill="none" stroke-linecap="round" opacity=".7"/>'
                f'<path d="M0 -120L4 -140" stroke="{C["leaf_md"]}" stroke-width="10" stroke-linecap="round"/></g>')
    def half(x, y, s, ang, rng):
        seeds = "".join(f'<ellipse cx="{rng.uniform(-44,44):.0f}" cy="{rng.uniform(-40,60):.0f}" rx="4" ry="2.6" fill="{C["seed"]}" transform="rotate({rng.uniform(0,180):.0f})"/>' for _ in range(46))
        return (f'<g transform="translate({x} {y}) rotate({ang}) scale({s})">'
                f'<ellipse cx="8" cy="12" rx="92" ry="98" fill="{C["ink"]}" opacity=".08"/>'
                f'<path d="M0 -118C24-118 30-92 34-78C82-58 96-10 86 32C74 84 30 100 0 100C-30 100-74 84-86 32C-96-10-82-58-34-78C-30-92-24-118 0-118Z" fill="{C["fig"]}"/>'
                f'<path d="M0 -100C18-100 22-80 26-68C68-50 78-8 70 28C60 72 26 84 0 84C-26 84-60 72-70 28C-78-8-68-50-26-68C-22-80-18-100 0-100Z" fill="{C["fig_core"]}"/>'
                f'<path d="M0 -70C40-56 56-16 50 22C44 56 20 66 0 66C-20 66-44 56-50 22C-56-16-40-56 0-70Z" fill="{C["fig_in"]}"/>'
                f'{seeds}</g>')
    rng = random.Random(5)
    b.append(whole(300, 380, 1.5, -14) + whole(1020, 330, 1.25, 18))
    b.append(half(620, 430, 1.55, 6, rng) + half(820, 520, 1.15, -24, rng))
    b.append(leaf(140, 690, 40, 3.4, C["leaf"], C["leaf_lt"]) + leaf(1190, 700, -30, 3.0, C["leaf_md"], C["leaf_lt"]))
    return svg(W, H, "".join(b), "Figs illustration")


def hojicha():
    """Layered hojicha latte in a glass on a wooden coaster (portrait)."""
    W, H = 900, 1200
    b = [f'<rect width="{W}" height="{H}" fill="{C["cream"]}"/>']
    b.append(f'<path d="M0 0L520 0L120 1200L0 1200Z" fill="{C["blush"]}"/>')
    b.append(f'<g opacity=".18" fill="{C["leaf_dk"]}">' + leaf(760, 260, -150, 7, C["leaf_dk"]) + leaf(690, 180, -120, 5, C["leaf_dk"]) + "</g>")
    b.append(f'<ellipse cx="450" cy="980" rx="250" ry="56" fill="{C["wood_dk"]}"/><ellipse cx="450" cy="966" rx="250" ry="56" fill="{C["wood"]}"/>')
    b.append(f'<ellipse cx="460" cy="960" rx="170" ry="34" fill="{C["ink"]}" opacity=".12"/>')
    b.append(f'<clipPath id="glass"><path d="M300 380L600 380L580 940Q450 970 320 940Z"/></clipPath>')
    b.append(f'<g clip-path="url(#glass)">'
             f'<rect x="280" y="380" width="340" height="600" fill="#fff" opacity=".6"/>'
             f'<rect x="280" y="660" width="340" height="320" fill="{C["milk"]}"/>'
             f'<path d="M280 470Q450 500 620 470L620 680Q450 640 280 690Z" fill="{C["hojicha"]}"/>'
             f'<path d="M280 640Q360 610 450 650Q540 690 620 650L620 700Q450 720 280 700Z" fill="{C["hojicha_lt"]}" opacity=".9"/>'
             f'<rect x="280" y="420" width="340" height="56" fill="{C["milk"]}"/>'
             f'<path d="M330 400L360 940" stroke="#fff" stroke-width="16" opacity=".5"/></g>')
    b.append(f'<path d="M300 380L600 380L580 940Q450 970 320 940Z" fill="none" stroke="{C["pot_w2"]}" stroke-width="6"/>')
    b.append(f'<ellipse cx="450" cy="380" rx="150" ry="16" fill="{C["milk"]}" stroke="{C["pot_w2"]}" stroke-width="6"/>')
    b.append(leaf(720, 1000, 60, 3.0, C["leaf"], C["leaf_lt"]))
    return svg(W, H, "".join(b), "Hojicha latte illustration")


def window():
    """Bright rainy window lined with potted plants (wide band)."""
    W, H = 1600, 1000
    rng = random.Random(21)
    g = [C["leaf_dk"], C["leaf"], C["leaf_md"], C["leaf_lt"]]
    b = [f'<rect width="{W}" height="{H}" fill="{C["wall"]}"/>']
    b.append(f'<rect x="160" y="60" width="1280" height="640" rx="10" fill="{C["frame"]}"/>')
    panes = "".join(f'<rect x="{176+c*316}" y="{76+r*306}" width="300" height="292" rx="4"/>' for r in range(2) for c in range(4))
    b.append(f'<clipPath id="wp">{panes}</clipPath>')
    b.append(f'<linearGradient id="wsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["glass2"]}"/><stop offset="1" stop-color="{C["sky"]}"/></linearGradient>')
    b.append(f'<g fill="url(#wsky)">{panes}</g>')
    city = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{700-y}" fill="#D2E2DC"/>' for x, y, w in [(180, 380, 160), (360, 300, 120), (520, 420, 180), (760, 340, 140), (930, 400, 200), (1160, 320, 150), (1320, 430, 120)])
    trees = "".join(f'<circle cx="{rng.uniform(170,1440):.0f}" cy="{rng.uniform(560,700):.0f}" r="{rng.uniform(40,90):.0f}" fill="{C["sage"]}"/>' for _ in range(12))
    drops = "".join(f'<circle cx="{rng.uniform(170,1440):.0f}" cy="{rng.uniform(70,690):.0f}" r="{rng.uniform(2,5):.1f}" fill="#fff" opacity=".85"/>' for _ in range(120))
    b.append(f'<g clip-path="url(#wp)">{city}{trees}{rain(rng, 170, 60, 1440, 700, 260, 0.8, (18, 40))}{drops}</g>')
    b.append(f'<rect x="120" y="690" width="1360" height="34" rx="6" fill="{C["wood"]}"/><rect x="120" y="720" width="1360" height="14" fill="{C["wood_dk"]}"/>')
    b.append(f'<rect y="734" width="{W}" height="266" fill="{C["paper"]}"/>')
    # potted plants along the sill
    b.append(pot(300, 640, 90, 52, C["pot"], C["pot_dk"]))
    b.append(f'<g fill="{C["leaf_md"]}"><rect x="286" y="520" width="28" height="122" rx="14"/><rect x="254" y="560" width="22" height="50" rx="11"/><rect x="324" y="545" width="22" height="60" rx="11"/></g>')
    b.append(pot(500, 650, 80, 42, C["pot_w"], C["pot_w2"]) + bush(rng, 500, 640, 120, 90, 14, g, (0.7, 1.1)))
    b.append(f'<g fill="#E79AAE">' + "".join(f'<circle cx="{500+dx}" cy="{575+dy}" r="11"/>' for dx, dy in [(-30, -6), (0, -24), (28, -4), (-8, 6), (16, -40)]) + "</g>")
    b.append(pot(720, 640, 96, 52, C["pot"], C["pot_dk"]))
    b.append("".join(f'<circle cx="{720+math.cos(a)*40:.0f}" cy="{580+math.sin(a)*26:.0f}" r="17" fill="{C["leaf_lt"] if i%2 else C["leaf_md"]}"/>' for i, a in enumerate([i*0.8 for i in range(8)])))
    b.append(pot(960, 630, 120, 62, C["pot_w"], C["pot_w2"]) + bush(rng, 960, 620, 200, 260, 26, g, (1.1, 1.7)))
    b.append(pot(1180, 650, 70, 40, C["pot"], C["pot_dk"]) + vine(rng, 1190, 660, 150, 10, 7, g) + bush(rng, 1180, 640, 70, 50, 9, g, (0.5, 0.8)))
    b.append(pot(1330, 648, 76, 44, C["pot_w"], C["pot_w2"]))
    b.append(f'<g fill="{C["sage"]}">' + "".join(f'<path d="M{1330+dx} 646Q{1330+dx*1.6} {600} {1330+dx*1.2} {590}Q{1330+dx*0.6} {610} {1330+dx*0.4} 646Z"/>' for dx in (-28, -14, 0, 14, 28)) + "</g>")
    return svg(W, H, "".join(b), "Rainy window with plants illustration")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in [("hero", hero), ("room", room), ("matcha", matcha), ("dango", dango), ("fig", fig), ("hojicha", hojicha), ("window", window)]:
        p = OUT / f"{name}.svg"
        p.write_text(fn(), "utf-8")
        print(f"{p.name}: {p.stat().st_size // 1024}KB")


if __name__ == "__main__":
    main()
