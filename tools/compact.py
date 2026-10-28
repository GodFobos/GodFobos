"""Calm, compact graphics: section labels, project banners, footer -> assets/

One idea per image; the details live in plain Markdown under each banner.
"""
from pathlib import Path

from cyber import BG, BG2, CYAN, DIM, MAGENTA, TEXT, YELLOW, T, glow_filter, svg, text_width

ASSETS = Path(__file__).resolve().parent.parent / "assets"
W = 1200
REDUCED = ""


def section(num, label, color=YELLOW):
    """Thin section label: '01 // PROJECTS' and a hairline."""
    H = 64
    n = f"{num:02d}"
    nw = text_width(n, "orbitron-900", 22, 2)
    lw = text_width(label, "orbitron-900", 22, 6)
    x = 8
    body = (T(n, x, 42, "orbitron-900", 22, color, 2)
            + T("//", x + nw + 14, 42, "sharetechmono", 20, DIM, 1)
            + T(label, x + nw + 44, 42, "orbitron-900", 22, TEXT, 6)
            + f'<line x1="{x + nw + 44 + lw + 24:.0f}" y1="34" x2="{W - 8}" y2="34" stroke="{color}" stroke-opacity=".35"/>'
            + f'<rect class="tick" x="{W - 40}" y="30" width="32" height="8" fill="{color}"/>')
    style = ".tick{animation:tick 2.4s steps(1) infinite}@keyframes tick{0%,60%{opacity:1}61%,100%{opacity:.2}}"
    return svg(W, H, body, f"{n} {label.title()}", style)


def project(num, title, sub, accent, art):
    H = 220
    defs = ("<defs>" + glow_filter("gy", YELLOW, 4, 1) + glow_filter("ga", accent, 3, 1)
            + f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BG2}"/>'
              f'<stop offset="1" stop-color="{BG}"/></linearGradient></defs>')
    n = f"{num:02d}"
    body = (defs + f'<rect width="{W}" height="{H}" rx="6" fill="url(#bg)"/>'
            + f'<rect x="0" y="0" width="5" height="{H}" fill="{accent}"/>'
            + T(n, 44, 92, "orbitron-900", 54, "none", 0, "start", f'stroke="{accent}" stroke-width="1.4" opacity=".8"')
            + T(title, 44, 152, "orbitron-900", 40, YELLOW, 1.5, extra='filter="url(#gy)"')
            + T(sub, 46, 186, "rajdhani-600", 22, TEXT, 1, extra='opacity=".85"')
            + art
            + f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="6" fill="none" stroke="{accent}" stroke-opacity=".35"/>')
    style = """
    .pkt{animation:pkt 3s linear infinite}@keyframes pkt{from{transform:translateX(0)}to{transform:translateX(300px)}}
    .blink{animation:blink 1.2s steps(1) infinite}@keyframes blink{0%,50%{opacity:1}51%,100%{opacity:0}}
    .line{opacity:0;animation-duration:8s;animation-timing-function:steps(1);animation-iteration-count:infinite}
    @keyframes l0{0%,10%{opacity:0}11%,100%{opacity:1}}@keyframes l1{0%,25%{opacity:0}26%,100%{opacity:1}}
    @keyframes l2{0%,40%{opacity:0}41%,100%{opacity:1}}
    @media (prefers-reduced-motion:reduce){*{animation:none!important}.line{opacity:1}}
    """
    return svg(W, H, body, f"{n} {title}", style)


def art_pipeline(accent):
    """A five-stage security pipeline with one packet travelling through it."""
    x0, y = 760, 110
    stages = ["CODE", "SAST", "SCA", "DAST", "SHIP"]
    out = [f'<line x1="{x0}" y1="{y}" x2="{x0 + 4*84 + 60}" y2="{y}" stroke="{accent}" stroke-opacity=".4"/>']
    for i, st in enumerate(stages):
        x = x0 + i * 84
        col = YELLOW if st == "SHIP" else accent
        out.append(f'<rect x="{x}" y="{y-16}" width="60" height="32" rx="3" fill="{BG}" stroke="{col}" stroke-opacity=".8"/>')
        out.append(T(st, x + 30, y + 6, "rajdhani-700", 15, col, 1.5, "middle"))
    out.append(f'<g class="pkt"><circle cx="{x0 + 30}" cy="{y - 26}" r="4" fill="{YELLOW}" filter="url(#gy)"/></g>')
    return "".join(out)


def art_terminal(accent):
    """Three log lines that type in, then a blinking cursor."""
    x0, y0 = 760, 62
    lines = [("$ ./run.sh  # benhoyt/inih", TEXT), ("#57453294  cov: 82  ft: 539", CYAN), ("crashes: 0   ASan: clean", "#39ff6a")]
    out = [f'<rect x="{x0 - 16}" y="{y0 - 30}" width="420" height="150" rx="4" fill="#06060b" stroke="{accent}" stroke-opacity=".45"/>']
    for i, (ln, col) in enumerate(lines):
        out.append(f'<g class="line" style="animation-name:l{i}">' + T(ln, x0, y0 + i * 32, "sharetechmono", 19, col) + "</g>")
    out.append(f'<rect class="blink" x="{x0}" y="{y0 + 3*32 - 17}" width="10" height="19" fill="{accent}"/>')
    return "".join(out)


def footer():
    H = 90
    msg = "WAKE UP, SAMURAI. THE KING HAS BUGS TO FIX."
    body = (f'<line x1="8" y1="20" x2="{W-8}" y2="20" stroke="{YELLOW}" stroke-opacity=".35"/>'
            + T(msg, W / 2, 62, "orbitron-900", 18, TEXT, 4, "middle", 'class="flk"'))
    style = (".flk{animation:flk 6s infinite}@keyframes flk{0%,40%,43%,100%{opacity:.85}41%{opacity:.3}}"
             "@media (prefers-reduced-motion:reduce){*{animation:none!important}}")
    return svg(W, H, body, "Wake up, samurai. The King has bugs to fix.", style)


if __name__ == "__main__":
    files = {
        "section-projects.svg": section(1, "PROJECTS"),
        "section-activity.svg": section(2, "ACTIVITY", CYAN),
        "section-stack.svg": section(3, "STACK", MAGENTA),
        "project-intensive.svg": project(1, "APPSEC INTENSIVE", "26-week AppSec / DevSecOps track  ·  in progress", CYAN, art_pipeline(CYAN)),
        "project-fuzzing.svg": project(2, "FUZZING PLAYGROUND", "Coverage-guided fuzzing of C parsers  ·  active", MAGENTA, art_terminal(MAGENTA)),
        "footer.svg": footer(),
    }
    for name, data in files.items():
        (ASSETS / name).write_text(data)
        print(name, len(data))
