"""Skills panel styled as installed cyberware -> assets/cyberdeck.svg
Also builds the section dividers and footer."""
from pathlib import Path

from cyber import (BG, BG2, CYAN, DIM, MAGENTA, RED, TEXT, YELLOW, T, frame,
                   glow_filter, panel_clip, runglow, runner, svg, text_width)

ASSETS = Path(__file__).resolve().parent.parent / "assets"
GREEN = "#39ff6a"

SLOTS = [
    ("NETRUNNING", "web offense", RED,
     [("BRP", "Burp Suite"), ("ZAP", "OWASP ZAP"), ("NMP", "Nmap")]),
    ("CODE", "languages", YELLOW,
     [("PY", "Python"), ("C", "C / C++"), ("SH", "Bash"), ("SQL", "SQL")]),
    ("OPS", "devsecops", CYAN,
     [("LNX", "Linux"), ("DKR", "Docker"), ("GIT", "Git"), ("GHA", "GitHub Actions"), ("CI", "CI / CD")]),
    ("RESEARCH", "find the bug", MAGENTA,
     [("FZ", "libFuzzer"), ("ASN", "AddressSanitizer"), ("LLM", "LLM x AppSec")]),
]

STYLE = """
.led{animation:led 1.8s steps(1) infinite}@keyframes led{0%,70%{opacity:1}71%,100%{opacity:.25}}
.l1{animation-delay:-.4s}.l2{animation-delay:-.9s}.l3{animation-delay:-1.3s}
.slot{animation:slot .6s ease-out both}@keyframes slot{from{opacity:0;transform:translateY(12px)}}
.load{animation:load 5s ease-in-out infinite}@keyframes load{0%{transform:translateX(-60px)}40%,100%{transform:translateX(320px)}}
.hexr{stroke-dasharray:14 6;animation:hexr 3s linear infinite}@keyframes hexr{to{stroke-dashoffset:-40}}
.scan{animation:scan 5s linear infinite}@keyframes scan{from{transform:translateY(0)}to{transform:translateY(420px)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""


def hexagon(cx, cy, r):
    import math
    pts = " ".join(f"{cx + r*math.cos(math.radians(60*i+30)):.1f},{cy + r*math.sin(math.radians(60*i+30)):.1f}"
                   for i in range(6))
    return pts


def cyberdeck():
    W, H = 1200, 400
    colw = (W - 80 - 3 * 20) / 4
    defs = ("<defs>" + panel_clip("dk", W, H, 28) + glow_filter("gy", YELLOW, 5, 1) + runglow(YELLOW)
            + '<pattern id="sl" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".3"/></pattern>'
            + "</defs>")
    parts = [defs, f'<g clip-path="url(#dk)"><rect width="{W}" height="{H}" fill="{BG2}"/>',
             T("CYBERDECK", 40, 52, "orbitron-900", 26, YELLOW, 2, extra='filter="url(#gy)"'),
             T("//  INSTALLED  //  WHAT I WORK WITH", 262, 50, "sharetechmono", 15, DIM, 1)]
    for ci, (name, sub, col, items) in enumerate(SLOTS):
        x = 40 + ci * (colw + 20)
        y = 82
        ph = H - y - 30
        parts.append(f'<polygon points="{x},{y} {x+colw-18},{y} {x+colw},{y+18} {x+colw},{y+ph} {x},{y+ph}" '
                     f'fill="{BG}" stroke="{col}" stroke-opacity=".55"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="{colw-18}" height="34" fill="{col}" opacity=".12"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="4" height="34" fill="{col}"/>')
        parts.append(f'<clipPath id="hdr{ci}"><rect x="{x}" y="{y}" width="{colw-18}" height="34"/></clipPath>'
                     f'<g clip-path="url(#hdr{ci})"><rect class="load" style="animation-delay:-{ci*1.1:.1f}s" '
                     f'x="{x}" y="{y}" width="50" height="34" fill="{col}" opacity=".25"/></g>')
        parts.append(T(name, x + 16, y + 24, "rajdhani-700", 20, col, 3))
        
        for ii, (code, label) in enumerate(items):
            iy = y + 66 + ii * 50
            cx = x + 34
            parts.append(f'<g class="slot" style="animation-delay:{0.15*ci+0.1*ii:.2f}s">')
            parts.append(f'<polygon points="{hexagon(cx, iy, 19)}" fill="{col}" fill-opacity=".1" stroke="{col}" stroke-width="1.5"/>')
            parts.append(f'<polygon points="{hexagon(cx, iy, 24)}" fill="none" stroke="{col}" stroke-opacity=".5" class="hexr"/>')
            fs = 13 if len(code) <= 2 else 11
            parts.append(T(code, cx, iy + 4.5, "orbitron-700", fs, col, 0.5, "middle"))
            parts.append(T(label, x + 66, iy + 7, "rajdhani-700", 21, TEXT, 0.8))
            parts.append(f'<circle cx="{x + colw - 18}" cy="{iy}" r="3.5" fill="{GREEN}" class="led l{(ci+ii)%4}"/>')
            parts.append("</g>")
    parts.append(f'<rect class="scan" x="0" y="-6" width="{W}" height="6" fill="{CYAN}" opacity=".05"/>')
    parts.append(f'<rect width="{W}" height="{H}" fill="url(#sl)"/></g>')
    parts.append(frame(W, H, YELLOW, 28, extra='stroke-opacity=".55"'))
    parts.append(runner(W, H, YELLOW, 28, sw=3, dur=8, length=200))
    parts.append(f'<rect x="{W-140}" y="0" width="110" height="4" fill="{YELLOW}"/>')
    return svg(W, H, "".join(parts), "Cyberdeck: Burp Suite, OWASP ZAP, Nmap, Python, C/C++, Bash, SQL, "
               "Linux, Docker, Git, GitHub Actions, CI/CD, libFuzzer, AddressSanitizer, LLM", STYLE)


def divider(label, color):
    W, H = 1200, 70
    lw = text_width(label, "orbitron-900", 22, 4)
    x0 = 60
    body = (
        f'<rect x="0" y="34" width="{W}" height="1.5" fill="{color}" opacity=".35"/>'
        f'<polygon points="{x0-14},14 {x0+lw+30},14 {x0+lw+46},34 {x0+lw+30},54 {x0-14},54" fill="{BG}" stroke="{color}" stroke-width="2"/>'
        f'<rect x="{x0-26}" y="14" width="6" height="40" fill="{color}"/>'
        + T(label, x0 + 8, 43, "orbitron-900", 22, color, 4)
        + "".join(f'<rect x="{W-60-i*18}" y="28" width="10" height="12" fill="{color}" class="sq" '
                  f'style="animation-delay:-{i*0.2:.1f}s"/>' for i in range(4))
        + f'<rect class="zip" x="{x0+lw+46}" y="33" width="120" height="3.5" fill="{color}" opacity=".9"/>'
    )
    style = (f".zip{{animation:zip 2.8s ease-in infinite}}@keyframes zip{{from{{transform:translateX(0);opacity:1}}"
             f"to{{transform:translateX({W-x0-lw-200:.0f}px);opacity:0}}}}"
             ".sq{animation:sq 1.2s steps(1) infinite}@keyframes sq{0%,49%{opacity:1}50%,100%{opacity:.2}}"
             "@media (prefers-reduced-motion:reduce){*{animation:none!important}}")
    return svg(W, H, body, label, style)


def footer():
    W, H = 1200, 120
    body = (
        '<defs>' + glow_filter("gm", MAGENTA, 4, 1) + '</defs>'
        f'<rect x="0" y="40" width="{W}" height="2" fill="{YELLOW}"/>'
        + "".join(f'<rect x="{i*24}" y="46" width="12" height="8" fill="{YELLOW}" opacity=".85"/>' for i in range(50))
        + '<g class="gl g1">' + T("WAKE UP, SAMURAI. THE KING HAS BUGS TO FIX.", W / 2, 92, "orbitron-900", 20, CYAN, 3, "middle") + '</g>'
        + '<g class="gl g2">' + T("WAKE UP, SAMURAI. THE KING HAS BUGS TO FIX.", W / 2, 92, "orbitron-900", 20, YELLOW, 3, "middle") + '</g>'
        + T("WAKE UP, SAMURAI. THE KING HAS BUGS TO FIX.", W / 2, 92, "orbitron-900", 20, MAGENTA, 3, "middle",
            'filter="url(#gm)" class="flk"')
        + f'<rect class="dash" x="0" y="46" width="60" height="8" fill="#fff" opacity=".6"/>'
        + T("// END OF TRANSMISSION", W / 2, 114, "sharetechmono", 12, DIM, 3, "middle")
    )
    style = (".flk{animation:flk 4s infinite}@keyframes flk{0%,30%,34%,70%,72%,100%{opacity:1}32%,71%{opacity:.3}}"
             ".gl{opacity:0}.g1{animation:g1 4s infinite}.g2{animation:g2 4s infinite}"
             "@keyframes g1{0%,30%,36%,100%{opacity:0;transform:none}31%{opacity:.9;transform:translate(-6px,1px)}"
             "33%{opacity:.9;transform:translate(4px,-1px)}35%{opacity:.8;transform:translate(-2px,0)}}"
             "@keyframes g2{0%,30%,36%,100%{opacity:0;transform:none}31%{opacity:.9;transform:translate(6px,-1px)}"
             "33%{opacity:.9;transform:translate(-4px,1px)}35%{opacity:.8;transform:translate(3px,0)}}"
             ".dash{animation:dash 3s linear infinite}@keyframes dash{from{transform:translateX(-60px)}to{transform:translateX(1260px)}}"
             "@media (prefers-reduced-motion:reduce){*{animation:none!important}}")
    return svg(W, H, body, "Wake up, samurai. The King has bugs to fix.", style)


if __name__ == "__main__":
    out = {
        "cyberdeck.svg": cyberdeck(),
        "div-gigs.svg": divider("ACTIVE GIGS", YELLOW),
        "footer.svg": footer(),
    }
    for k, v in out.items():
        (ASSETS / k).write_text(v)
        print(k, len(v))
