"""Night City hero banner -> assets/hero.svg"""
import base64
import random
from pathlib import Path

from cyber import (BG, CYAN, DIM, MAGENTA, RED, TEXT, YELLOW, T, glow_filter,
                   svg, text_width)

W, H = 1200, 400
ART = Path(__file__).resolve().parent.parent / "art" / "crown.jpg"
rnd = random.Random(2077)
WHITE_ICE = "#eefcff"


def skyline(layer, base_y, count, wmin, wmax, hmin, hmax, fill, windows, x0=-20):
    out, x = [], x0
    lit = []
    while x < W + 20:
        w = rnd.randint(wmin, wmax)
        h = rnd.randint(hmin, hmax)
        top = base_y - h
        # building body with an occasional stepped crown / antenna
        out.append(f'<rect x="{x}" y="{top}" width="{w}" height="{H-top}" fill="{fill}"/>')
        if rnd.random() < 0.35:
            cw = w * rnd.uniform(0.3, 0.6)
            ch = rnd.randint(8, 26)
            out.append(f'<rect x="{x + (w-cw)/2:.0f}" y="{top-ch}" width="{cw:.0f}" height="{ch}" fill="{fill}"/>')
            if rnd.random() < 0.5:
                ax = x + w / 2
                out.append(f'<line x1="{ax:.0f}" y1="{top-ch}" x2="{ax:.0f}" y2="{top-ch-rnd.randint(14,40)}" stroke="{fill}" stroke-width="2"/>')
                out.append(f'<circle cx="{ax:.0f}" cy="{top-ch-40}" r="1.6" fill="{RED}" class="blink b{rnd.randint(1,4)}"/>')
        if windows:
            cols = max(1, (w - 6) // 7)
            for r in range(int(h // 9)):
                for c in range(cols):
                    if rnd.random() < windows:
                        color = rnd.choice([YELLOW, YELLOW, CYAN, MAGENTA, "#ffb36b"])
                        op = rnd.uniform(0.25, 0.85)
                        cls = f' class="win w{rnd.randint(1,5)}"' if rnd.random() < 0.08 else ""
                        lit.append(f'<rect x="{x+4+c*7}" y="{top+6+r*9}" width="3" height="4" '
                                   f'fill="{color}" opacity="{op:.2f}"{cls}/>')
        x += w + rnd.randint(0, 6)
    return f'<g id="{layer}">' + "".join(out) + "".join(lit) + "</g>"


def rain(n):
    drops = []
    for _ in range(n):
        x = rnd.uniform(0, W + 200)
        y = rnd.uniform(-H, H)
        ln = rnd.uniform(10, 26)
        op = rnd.uniform(0.08, 0.35)
        drops.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x-ln*0.35:.0f}" y2="{y+ln:.0f}" '
                     f'stroke="#9fb6ff" stroke-opacity="{op:.2f}" stroke-width="1"/>')
    d = "".join(drops)
    # two copies stacked so the loop is seamless
    return (f'<g class="rain"><g>{d}</g><g transform="translate(-160 -{H})">{d}</g></g>')


def neon_vertical(x, y, word, color, size=22, cls="flk1"):
    parts = [f'<rect x="{x-16}" y="{y-26}" width="32" height="{len(word)*size*1.05+18:.0f}" '
             f'rx="3" fill="#0b0b14" stroke="{color}" stroke-width="1.5" opacity="0.95"/>']
    for i, ch in enumerate(word):
        parts.append(T(ch, x, y + i * size * 1.05, "orbitron-900", size, color, anchor="middle"))
    return f'<g class="{cls}" filter="url(#g-{"m" if color == MAGENTA else "c"})">' + "".join(parts) + "</g>"


def build():
    defs = (
        '<defs>'
        '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#05050a"/><stop offset=".6" stop-color="#0c0b18"/>'
        '<stop offset=".9" stop-color="#1a1030"/><stop offset="1" stop-color="#0b0812"/></linearGradient>'
        '<radialGradient id="haze" cx=".72" cy=".78" r=".55">'
        '<stop offset="0" stop-color="#00f0ff" stop-opacity=".10"/>'
        '<stop offset=".5" stop-color="#00f0ff" stop-opacity=".03"/>'
        '<stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="fadeL" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{BG}" stop-opacity=".97"/>'
        f'<stop offset=".42" stop-color="{BG}" stop-opacity=".82"/>'
        f'<stop offset=".62" stop-color="{BG}" stop-opacity="0"/></linearGradient>'
        '<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">'
        '<rect width="4" height="1" fill="#000" opacity=".35"/></pattern>'
        '<pattern id="hazard" width="22" height="22" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
        f'<rect width="11" height="22" fill="{YELLOW}"/></pattern>'
        + glow_filter("g-y", YELLOW, 6, 1)
        + glow_filter("g-c", CYAN, 3, 2)
        + glow_filter("g-m", MAGENTA, 3, 2)
        + glow_filter("g-r", RED, 3, 1)
        + glow_filter("g-w", "#7fe9ff", 5, 2)
        + '<clipPath id="clipAll"><rect width="1200" height="400"/></clipPath>'
        # hologram: crown -> cyan light with alpha = brightness
        + '<filter id="holo-f" x="-10%" y="-10%" width="120%" height="120%" color-interpolation-filters="sRGB">'
          '<feColorMatrix type="matrix" values="0 0 0 0 .55  0 0 0 0 .95  0 0 0 0 1  .9 .9 .9 0 -.18" result="h"/>'
          '<feGaussianBlur in="h" stdDeviation="5" result="b"/>'
          '<feMerge><feMergeNode in="b"/><feMergeNode in="h"/><feMergeNode in="h"/></feMerge></filter>'
        + '<filter id="holo-f2" x="-10%" y="-10%" width="120%" height="120%" color-interpolation-filters="sRGB">'
          '<feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 .17  0 0 0 0 .84  .9 .9 .9 0 -.2"/></filter>'
        + '<pattern id="holo-scan" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".55"/></pattern>'
        + f'<linearGradient id="cone" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity=".45"/>'
          f'<stop offset="1" stop-color="{CYAN}" stop-opacity=".02"/></linearGradient>'
        '</defs>'
    )

    city = (
        f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
        f'<rect width="{W}" height="{H}" fill="url(#haze)"/>'
        # far / mid / near skylines
        + skyline("far", 330, 0, 22, 50, 50, 150, "#121024", 0.05)
        + skyline("near", 400, 0, 40, 90, 20, 110, "#07060c", 0.02)
    )

    # hologram of the White King's crown, projected from a rooftop
    data = base64.b64encode(ART.read_bytes()).decode()
    cw = 270
    ch = cw * 910 / 1174
    cx0, cy0 = 960 - cw / 2, 46
    px, py = 960, 318                      # projector on the rooftop
    holo = (
        f'<polygon class="cone" points="{px-6},{py} {px+6},{py} {cx0+cw-30:.0f},{cy0+ch-6:.0f} {cx0+30:.0f},{cy0+ch-6:.0f}" fill="url(#cone)"/>'
        f'<rect x="{px-16}" y="{py}" width="32" height="8" fill="#0b0b14" stroke="{CYAN}" stroke-opacity=".8"/>'
        f'<circle cx="{px}" cy="{py}" r="3" fill="{CYAN}" class="blink b4" filter="url(#g-c)"/>'
        f'<defs><image id="crw" x="{cx0:.0f}" y="{cy0}" width="{cw}" height="{ch:.0f}" href="data:image/jpeg;base64,{data}"/>'
        f'<mask id="crm" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><g class="spin"><use href="#crw"/></g></mask>'
        f'<linearGradient id="spinsheen" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="#eaffff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>'
        f'<g class="holo">'
        f'<g class="spin"><g filter="url(#holo-f)"><use href="#crw"/></g>'
        f'<g class="hglitch"><g filter="url(#holo-f2)"><use href="#crw"/></g></g></g>'
        # a band of light crossing the turning crown from right to left
        f'<g mask="url(#crm)"><rect class="rsheen" x="{cx0 + cw:.0f}" y="{cy0}" width="70" height="{ch:.0f}" fill="url(#spinsheen)"/></g>'
        f'</g>'
        + T("WHITEKING.HOLO", 960, cy0 + ch + 22, "sharetechmono", 13, CYAN, 2, "middle", 'opacity=".75" class="holo"')
    )

    # left text block
    name = "KIRILL ALIMOV"
    nx, ny, nsize = 64, 186, 62
    name_d = T(name, nx, ny, "orbitron-900", nsize, YELLOW, 3)
    glitch = (
        '<g class="gl gl1">' + T(name, nx, ny, "orbitron-900", nsize, CYAN, 3) + '</g>'
        '<g class="gl gl2">' + T(name, nx, ny, "orbitron-900", nsize, RED, 3) + '</g>'
        f'<g filter="url(#g-y)">{name_d}</g>'
    )
    nw = text_width(name, "orbitron-900", nsize, 3)

    tag = "NETRUNNER  ·  APPSEC  ·  DEVSECOPS"
    tw = text_width(tag, "rajdhani-700", 24, 3)
    nchar = len(tag)
    chip1 = "RTU MIREA  ·  INFOSEC  ·  YEAR 4"
    chip2 = "STATUS: OPEN TO APPSEC INTERNSHIP"
    c1w = text_width(chip1, "rajdhani-700", 15, 1.5) + 36
    c2w = text_width(chip2, "rajdhani-700", 15, 1.5) + 50
    cy = 300
    motto = "I'M THE ONLY KING"
    left = (
        f'<rect width="{W}" height="{H}" fill="url(#fadeL)"/>'
        # kicker line
        + T("// NIGHT CITY NET  ·  NETRUNNER ID:", nx, 104, "sharetechmono", 17, DIM, 1)
        + T("WHITEKING", nx + text_width("// NIGHT CITY NET  ·  NETRUNNER ID: ", "sharetechmono", 17, 1), 104,
            "sharetechmono", 17, WHITE_ICE, 1, extra='filter="url(#g-c)"')
        + f'<rect x="{nx}" y="114" width="46" height="4" fill="{RED}"/>'
        + f'<rect x="{nx+52}" y="114" width="12" height="4" fill="{RED}" class="blink b2"/>'
        + glitch
        + f'<rect x="{nx}" y="{ny+16}" width="{nw:.0f}" height="2" fill="{YELLOW}" opacity=".35"/>'
        # the motto as a white neon sign
        + f'<g class="neon">' + T(motto, nx, ny + 54, "orbitron-900", 30, WHITE_ICE, 4, extra='filter="url(#g-w)"') + '</g>'
        + T(tag, nx, ny + 94, "rajdhani-700", 24, CYAN, 3, extra='filter="url(#g-c)"')
    )

    # HUD bits
    hud = (
        f'<path d="M18 46 V18 H46" fill="none" stroke="{YELLOW}" stroke-width="2" opacity=".8"/>'
        f'<path d="M{W-46} {H-18} H{W-18} V{H-46}" fill="none" stroke="{YELLOW}" stroke-width="2" opacity=".8"/>'
    )

    fx = (
        f'<rect width="{W}" height="{H}" fill="url(#scan)" opacity=".5" pointer-events="none"/>'
    )

    style = """
    .rain{animation:rain 1.1s linear infinite}
    @keyframes rain{from{transform:translate(0,0)}to{transform:translate(160px,480px)}}
    .blink{animation:blink 1.6s steps(1) infinite}
    .b2{animation-duration:2.3s}.b3{animation-duration:3.1s}.b4{animation-duration:1.2s}
    @keyframes blink{0%,60%{opacity:1}61%,100%{opacity:.15}}
    .win{animation:win 7s steps(1) infinite}
    .w2{animation-delay:-1.3s}.w3{animation-delay:-2.9s}.w4{animation-delay:-4.1s}.w5{animation-delay:-5.6s}
    @keyframes win{0%,70%{opacity:.8}71%,100%{opacity:.05}}
    .flk1{animation:flk 4s infinite}.flk2{animation:flk 5.3s infinite -2s}
    @keyframes flk{0%,18%,22%,62%,64%,100%{opacity:1}20%,63%{opacity:.25}}
    .holo{animation:holo 3s ease-in-out infinite}
    .neon{animation:neon 5s infinite}@keyframes neon{0%,40%,43%,46%,100%{opacity:1}41%,45%{opacity:.25}}
    .cone{animation:cone 3s ease-in-out infinite}@keyframes cone{0%,100%{opacity:.7}50%{opacity:1}}
    .spin{transform-box:view-box;transform-origin:960px 150px;animation:spin 9s linear infinite}
    @keyframes spin{0.00%{transform:scaleX(1.000)}4.17%{transform:scaleX(0.966)}8.33%{transform:scaleX(0.866)}12.50%{transform:scaleX(0.707)}16.67%{transform:scaleX(0.500)}20.83%{transform:scaleX(0.259)}25.00%{transform:scaleX(0.000)}29.17%{transform:scaleX(-0.259)}33.33%{transform:scaleX(-0.500)}37.50%{transform:scaleX(-0.707)}41.67%{transform:scaleX(-0.866)}45.83%{transform:scaleX(-0.966)}50.00%{transform:scaleX(-1.000)}54.17%{transform:scaleX(-0.966)}58.33%{transform:scaleX(-0.866)}62.50%{transform:scaleX(-0.707)}66.67%{transform:scaleX(-0.500)}70.83%{transform:scaleX(-0.259)}75.00%{transform:scaleX(-0.000)}79.17%{transform:scaleX(0.259)}83.33%{transform:scaleX(0.500)}87.50%{transform:scaleX(0.707)}91.67%{transform:scaleX(0.866)}95.83%{transform:scaleX(0.966)}100.00%{transform:scaleX(1.000)}}
    .rsheen{animation:rsheen 4.5s linear infinite}@keyframes rsheen{from{transform:translateX(0)}to{transform:translateX(-340px)}}
    .hglitch{opacity:0;animation:hg 4.5s steps(1) infinite;mix-blend-mode:screen}
    @keyframes hg{0%,84%,100%{opacity:0;transform:none}85%{opacity:.8;transform:translate(-6px,0);clip-path:inset(20% 0 55% 0)}
      87%{opacity:.8;transform:translate(5px,0);clip-path:inset(60% 0 15% 0)}89%{opacity:0}}
    @keyframes holo{0%,100%{opacity:.9}50%{opacity:.6}93%{opacity:.9}95%{opacity:.2}97%{opacity:.85}}
    .gl{opacity:0;mix-blend-mode:screen}
    .gl1{animation:g1 7s infinite}.gl2{animation:g2 7s infinite}
    @keyframes g1{0%,86%,100%{opacity:0;transform:none}
      87%{opacity:.9;transform:translate(-5px,0);clip-path:inset(10% 0 55% 0)}
      89%{opacity:.9;transform:translate(4px,0);clip-path:inset(60% 0 10% 0)}
      91%{opacity:.9;transform:translate(-3px,0);clip-path:inset(35% 0 40% 0)}
      92%{opacity:0}}
    @keyframes g2{0%,86%,100%{opacity:0;transform:none}
      87%{opacity:.9;transform:translate(5px,0);clip-path:inset(55% 0 15% 0)}
      89%{opacity:.9;transform:translate(-4px,0);clip-path:inset(5% 0 70% 0)}
      91%{opacity:.9;transform:translate(3px,0);clip-path:inset(40% 0 30% 0)}
      92%{opacity:0}}
    .beam{transform-box:fill-box;transform-origin:50% 100%}
    .bm1{animation:sw 9s ease-in-out infinite alternate}
    .bm2{animation:sw 11s ease-in-out infinite alternate-reverse}
    @keyframes sw{from{transform:rotate(-14deg)}to{transform:rotate(12deg)}}
    .av{animation:av 16s linear infinite}
    @keyframes av{from{transform:translate(1260px,92px)}to{transform:translate(560px,140px)}}
    .slice{animation:slice 5s linear infinite}
    @keyframes slice{0%{transform:translateY(-10px)}100%{transform:translateY(450px)}}
    .type{animation:type 6s steps(1) infinite}
    @keyframes type{0%,100%{opacity:1}50%{opacity:.4}}
    @media (prefers-reduced-motion:reduce){*{animation:none!important}}
    """
    style += (
        ".typer{transform-box:fill-box;transform-origin:0 0;animation:typer 9s infinite}"
        f"@keyframes typer{{0%{{transform:scaleX(0);animation-timing-function:steps({nchar})}}"
        "30%,88%{transform:scaleX(1);animation-timing-function:steps(12)}100%{transform:scaleX(0)}}"
        ".caret{animation:caret 9s infinite,cblink .8s steps(1) infinite}"
        f"@keyframes caret{{0%{{transform:translateX(0);animation-timing-function:steps({nchar})}}"
        f"30%,88%{{transform:translateX({tw+6:.0f}px);animation-timing-function:steps(12)}}100%{{transform:translateX(0)}}}}"
        "@keyframes cblink{0%,50%{opacity:1}51%,100%{opacity:0}}"
        # screen tear: copies of the whole scene, shifted in thin bands
        ".tear{opacity:0;animation:tear 7s steps(1) infinite}"
        ".t2{animation-delay:-.12s}.t3{animation-delay:-.25s}"
        "@keyframes tear{0%,79%{opacity:0;transform:none}80%{opacity:1;transform:translateX(-18px)}"
        "81%{opacity:1;transform:translateX(14px)}82%{opacity:0;transform:none}"
        "93%{opacity:1;transform:translateX(9px)}94%{opacity:0}}"
        ".flash{opacity:0;animation:flash 7s steps(1) infinite}"
        "@keyframes flash{0%,79%{opacity:0}80%{opacity:.18}81%{opacity:0}93%{opacity:.1}94%{opacity:0}}"
    )
    bands = [(150, 26, "t1"), (238, 14, "t2"), (322, 34, "t3")]
    tears = "".join(
        f'<clipPath id="band{i}"><rect x="0" y="{y}" width="{W}" height="{h}"/></clipPath>'
        f'<g clip-path="url(#band{i})"><g class="tear {cls}"><use href="#scene"/>'
        f'<rect x="0" y="{y}" width="{W}" height="2" fill="{CYAN if i % 2 else RED}"/></g></g>'
        for i, (y, h, cls) in enumerate(bands))
    flash = f'<rect class="flash" width="{W}" height="{H}" fill="{CYAN}"/>'
    scene = '<g id="scene">' + city + holo + left + hud + '</g>'
    body = defs + '<g clip-path="url(#clipAll)">' + scene + fx + "</g>"
    return svg(W, H, body, "Kirill Alimov, netrunner WhiteKing - I\'m the only king. AppSec / DevSecOps", style)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "hero.svg"
    out.write_text(build())
    print(out, out.stat().st_size)
