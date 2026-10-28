"""Night City hero banner -> assets/hero.svg"""
import base64
import random
from pathlib import Path

from cyber import (BG, CYAN, DIM, MAGENTA, RED, TEXT, YELLOW, T, glow_filter,
                   svg, text_width)

W, H = 1200, 480
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
        '<stop offset="0" stop-color="#05050a"/><stop offset=".55" stop-color="#1a0b2e"/>'
        '<stop offset=".8" stop-color="#3a0d3f"/><stop offset="1" stop-color="#12060f"/></linearGradient>'
        '<radialGradient id="haze" cx=".72" cy=".78" r=".55">'
        '<stop offset="0" stop-color="#ff2bd6" stop-opacity=".35"/>'
        '<stop offset=".5" stop-color="#7a1fff" stop-opacity=".12"/>'
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
        + '<clipPath id="clipAll"><rect width="1200" height="480"/></clipPath>'
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
        # searchlights
        + f'<g opacity=".16"><polygon class="beam bm1" points="760,360 700,-20 760,-20" fill="{CYAN}"/>'
        f'<polygon class="beam bm2" points="1040,360 1080,-20 1130,-20" fill="{MAGENTA}"/></g>'
        # megatower
        + '<g fill="#160d27"><polygon points="790,330 812,40 836,40 858,330"/>'
        '<rect x="818" y="18" width="12" height="24"/></g>'
        + f'<rect x="815" y="60" width="18" height="3" fill="{YELLOW}" opacity=".8" class="blink b3"/>'
        + f'<circle cx="824" cy="16" r="2.4" fill="{RED}" class="blink b1" filter="url(#g-r)"/>'
        # flying AV
        + f'<g class="av"><path d="M0 0 L26 -4 L40 0 L26 5 Z" fill="#0b0b14" stroke="{CYAN}" stroke-opacity=".7"/>'
        f'<circle cx="2" cy="0" r="1.8" fill="{RED}"/><circle cx="38" cy="0" r="1.8" fill="{YELLOW}"/>'
        f'<line x1="40" y1="0" x2="120" y2="2" stroke="{YELLOW}" stroke-opacity=".25"/></g>'
        # far / mid / near skylines
        + skyline("far", 330, 0, 20, 46, 60, 170, "#1d1233", 0.10)
        + skyline("mid", 360, 0, 26, 60, 50, 210, "#120a20", 0.16)
        + neon_vertical(1162, 168, "24/7", CYAN, 19, "flk2")
        + skyline("near", 410, 0, 40, 90, 20, 120, "#07040c", 0.05)
    )

    # hologram of the White King's crown, projected from a rooftop
    data = base64.b64encode(ART.read_bytes()).decode()
    cw = 290
    ch = cw * 910 / 1174
    cx0, cy0 = 990 - cw / 2, 44
    px, py = 990, 352                      # projector on the rooftop
    holo = (
        f'<polygon class="cone" points="{px-6},{py} {px+6},{py} {cx0+cw-30:.0f},{cy0+ch-6:.0f} {cx0+30:.0f},{cy0+ch-6:.0f}" fill="url(#cone)"/>'
        f'<rect x="{px-16}" y="{py}" width="32" height="8" fill="#0b0b14" stroke="{CYAN}" stroke-opacity=".8"/>'
        f'<circle cx="{px}" cy="{py}" r="3" fill="{CYAN}" class="blink b4" filter="url(#g-c)"/>'
        f'<g class="holo"><g filter="url(#holo-f)">'
        f'<image x="{cx0:.0f}" y="{cy0}" width="{cw}" height="{ch:.0f}" href="data:image/jpeg;base64,{data}"/></g>'
        f'<rect x="{cx0:.0f}" y="{cy0}" width="{cw}" height="{ch:.0f}" fill="url(#holo-scan)"/>'
        f'<g class="hglitch"><g filter="url(#holo-f2)"><image x="{cx0:.0f}" y="{cy0}" width="{cw}" height="{ch:.0f}" '
        f'href="data:image/jpeg;base64,{data}"/></g></g></g>'
        + T("WHITEKING.HOLO  //  LIVE", 990, cy0 + ch + 22, "sharetechmono", 13, CYAN, 2, "middle", 'opacity=".75" class="holo"')
    )

    # left text block
    name = "KIRILL ALIMOV"
    nx, ny, nsize = 56, 196, 66
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
        + f'<clipPath id="tagclip"><rect class="typer" x="{nx-4}" y="{ny+68}" width="{tw+14:.0f}" height="36"/></clipPath>'
        + f'<g clip-path="url(#tagclip)">' + T(tag, nx, ny + 94, "rajdhani-700", 24, CYAN, 3, extra='filter="url(#g-c)"') + '</g>'
        + f'<rect class="caret" x="{nx}" y="{ny+74}" width="12" height="24" fill="{CYAN}"/>'
        # chips: text centred in both axes, clean cut corners
        + f'<g transform="translate({nx} {cy + 22})">'
        f'<polygon points="0,0 {c1w:.0f},0 {c1w:.0f},32 10,32 0,22" fill="#0b0b14" stroke="{TEXT}" stroke-opacity=".5"/>'
        + T(chip1, c1w / 2 + 2, 21.5, "rajdhani-700", 15, TEXT, 1.5, "middle")
        + '</g>'
        + f'<g transform="translate({nx + c1w + 14} {cy + 22})">'
        f'<polygon points="0,0 {c2w:.0f},0 {c2w:.0f},22 {c2w-10:.0f},32 0,32" fill="#0d1a0d" stroke="#39ff6a" stroke-opacity=".8"/>'
        f'<circle cx="17" cy="16" r="4.5" fill="#39ff6a" class="blink b1"/>'
        + T(chip2, 30 + (c2w - 30) / 2 - 2, 21.5, "rajdhani-700", 15, "#39ff6a", 1.5, "middle")
        + '</g>'
    )

    # HUD bits
    hud = (
        # corner brackets
        f'<path d="M14 40 V14 H40" fill="none" stroke="{YELLOW}" stroke-width="3"/>'
        f'<path d="M{W-40} 14 H{W-14} V40" fill="none" stroke="{YELLOW}" stroke-width="3"/>'
        # top right readout
        + T("SYS 2.0.77", W - 56, 36, "sharetechmono", 14, YELLOW, 1, "end")
        + T("NET: SECURE", W - 56, 54, "sharetechmono", 14, DIM, 1, "end")
        # bottom bar
        + f'<rect x="0" y="{H-34}" width="{W}" height="34" fill="#0a0a0f"/>'
        f'<rect x="0" y="{H-34}" width="{W}" height="2" fill="{YELLOW}"/>'
        f'<rect x="0" y="{H-32}" width="150" height="32" fill="url(#hazard)" opacity=".9"/>'
        f'<rect x="{W-150}" y="{H-32}" width="150" height="32" fill="url(#hazard)" opacity=".9"/>'
        + T("BUILD  >  BREAK  >  FIX  >  REPEAT", W / 2, H - 11, "rajdhani-700", 16, YELLOW, 4, "middle")
        + f'<g class="type">' + T("> jack-in --as=whiteking", 170, H - 11, "sharetechmono", 14, DIM)
        + '</g>'
    )

    fx = (
        f'<rect width="{W}" height="{H}" fill="url(#scan)" pointer-events="none"/>'
        # sweeping glitch slice
        f'<rect class="slice" x="0" y="0" width="{W}" height="6" fill="{CYAN}" opacity=".08"/>'
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
    .hglitch{opacity:0;animation:hg 4.5s steps(1) infinite;mix-blend-mode:screen}
    @keyframes hg{0%,84%,100%{opacity:0;transform:none}85%{opacity:.8;transform:translate(-6px,0);clip-path:inset(20% 0 55% 0)}
      87%{opacity:.8;transform:translate(5px,0);clip-path:inset(60% 0 15% 0)}89%{opacity:0}}
    @keyframes holo{0%,100%{opacity:.9}50%{opacity:.6}93%{opacity:.9}95%{opacity:.2}97%{opacity:.85}}
    .gl{opacity:0;mix-blend-mode:screen}
    .gl1{animation:g1 3.2s infinite}.gl2{animation:g2 3.2s infinite}
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
    scene = '<g id="scene">' + city + holo + rain(170) + left + hud + '</g>'
    body = defs + '<g clip-path="url(#clipAll)">' + scene + tears + flash + fx + "</g>"
    return svg(W, H, body, "Kirill Alimov, netrunner WhiteKing - I\'m the only king. AppSec / DevSecOps", style)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "hero.svg"
    out.write_text(build())
    print(out, out.stat().st_size)
