"""Project banners styled as Night City gigs -> assets/gig-*.svg"""
from pathlib import Path

import random

from cyber import (BG, BG2, CYAN, DIM, MAGENTA, RED, TEXT, YELLOW, T,
                   frame, glow_filter, panel_clip, runglow, runner, svg,
                   text_width)

W, H = 1200, 476
ASSETS = Path(__file__).resolve().parent.parent / "assets"

STYLE = """
.blink{animation:blink 1.4s steps(1) infinite}
@keyframes blink{0%,55%{opacity:1}56%,100%{opacity:.15}}
.bar{animation:bar 2.6s ease-in-out infinite}
@keyframes bar{0%{transform:translateX(-120px)}100%{transform:translateX(300px)}}
.scan{animation:scan 4s linear infinite}
@keyframes scan{from{transform:translateY(0)}to{transform:translateY(476px)}}
.flk{animation:flk 5s infinite}
@keyframes flk{0%,40%,44%,100%{opacity:1}42%{opacity:.3}}
.hx{animation:hx 2.2s steps(1) infinite}
@keyframes hx{0%,49%{opacity:.25}50%,100%{opacity:1}}
.d1{animation-delay:-.3s}.d2{animation-delay:-.7s}.d3{animation-delay:-1.1s}.d4{animation-delay:-1.6s}
.pulse{animation:pulse 2s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes pulse{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.06);opacity:.75}}
.flow{stroke-dasharray:6 8;animation:flow 1.2s linear infinite}
@keyframes flow{to{stroke-dashoffset:-28}}
.draw{stroke-dasharray:100 100;animation:draw 6s ease-in-out infinite}
@keyframes draw{0%{stroke-dashoffset:100}35%,85%{stroke-dashoffset:0}100%{stroke-dashoffset:-100}}
.gl{opacity:0}.gl1{animation:g1 4.5s infinite}.gl2{animation:g2 4.5s infinite}
@keyframes g1{0%,88%,100%{opacity:0;transform:none}89%{opacity:.85;transform:translate(-4px,0);clip-path:inset(0 0 60% 0)}
 91%{opacity:.85;transform:translate(5px,0);clip-path:inset(55% 0 0 0)}93%{opacity:0}}
@keyframes g2{0%,88%,100%{opacity:0;transform:none}89%{opacity:.85;transform:translate(4px,0);clip-path:inset(50% 0 10% 0)}
 91%{opacity:.85;transform:translate(-5px,0);clip-path:inset(10% 0 55% 0)}93%{opacity:0}}
.pkt{animation:pkt 3.2s linear infinite}
@keyframes pkt{from{transform:translateX(0)}to{transform:translateX(426px)}}
.shscan{animation:shscan 2.8s ease-in-out infinite}
@keyframes shscan{0%{transform:translateY(-90px);opacity:0}10%{opacity:1}90%{opacity:1}100%{transform:translateY(90px);opacity:0}}
.bsweep{animation:bsweep 6s ease-in-out infinite}
@keyframes bsweep{0%,45%{transform:translateX(0)}85%,100%{transform:translateX(960px)}}
.mut{opacity:0;animation:mut 1.5s steps(1) infinite}
@keyframes mut{0%,32%{opacity:1}33%,100%{opacity:0}}
.sweep{animation:sweep 5s ease-in-out infinite}
@keyframes sweep{0%,60%{transform:translateX(-80px)}80%,100%{transform:translateX(420px)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""


def objectives(items, x, y, step=30):
    """CP2077 journal-style objective list. state: done | active | todo"""
    out = []
    for i, (state, label, note) in enumerate(items):
        yy = y + i * step
        if state == "done":
            out.append(f'<rect x="{x}" y="{yy-13}" width="14" height="14" fill="{YELLOW}"/>'
                       f'<path d="M{x+3} {yy-6} l3 3 l6 -7" stroke="{BG}" stroke-width="2.4" fill="none"/>')
            col = DIM
        elif state == "active":
            out.append(f'<rect x="{x}" y="{yy-13}" width="14" height="14" fill="none" stroke="{CYAN}" stroke-width="2"/>'
                       f'<rect x="{x+4}" y="{yy-9}" width="6" height="6" fill="{CYAN}" class="blink"/>')
            col = TEXT
        else:
            out.append(f'<rect x="{x}" y="{yy-13}" width="14" height="14" fill="none" stroke="{DIM}" stroke-width="2"/>')
            col = DIM
        out.append(T(label, x + 26, yy, "rajdhani-700", 18, col, 0.6))
        if note:
            lw = text_width(label, "rajdhani-700", 18, 0.6)
            out.append(T(note, x + 26 + lw + 12, yy, "sharetechmono", 15,
                         YELLOW if state == "done" else DIM, 0.3))
    return "".join(out)


def rich(segs, x, y, font="rajdhani-600", size=21, spacing=0.4):
    """Render [(text, color), ...] on one baseline."""
    out, cx = [], x
    for txt, col in segs:
        out.append(T(txt, cx, y, font, size, col, spacing))
        cx += text_width(txt, font, size, spacing) + spacing + (size * 0.0)
    return "".join(out)


def brief(lines, accent, y0=352):
    x0, x1 = 148, W - 34
    h = 96
    lab = "BRIEF"
    return (
        f'<polygon points="{x0},{y0} {x1},{y0} {x1},{y0+h-14} {x1-14},{y0+h} {x0},{y0+h}" '
        f'fill="#05050a" fill-opacity=".85" stroke="{accent}" stroke-opacity=".45"/>'
        f'<rect x="{x0}" y="{y0}" width="4" height="{h}" fill="{accent}"/>'
        # speaker tag, CP2077 dialogue style
        + T("WHITEKING", x0 + 22, y0 + 30, "rajdhani-700", 16, YELLOW, 3)
        + T("// " + lab, x0 + 22, y0 + 52, "sharetechmono", 14, DIM, 2)
        + f'<rect x="{x0+22}" y="{y0+64}" width="28" height="3" fill="{accent}" class="blink"/>'
        + f'<rect x="{x0+150}" y="{y0+16}" width="1.5" height="{h-32}" fill="{accent}" opacity=".4"/>'
        + rich(lines[0], x0 + 172, y0 + 40)
        + rich(lines[1], x0 + 172, y0 + 72)
        # light sweep over the message
        + f'<clipPath id="bc"><rect x="{x0+160}" y="{y0+8}" width="{x1-x0-180}" height="{h-16}"/></clipPath>'
        + f'<g clip-path="url(#bc)"><rect class="bsweep" x="{x0+60}" y="{y0}" width="90" height="{h}" '
          f'fill="url(#bsg)"/></g>'
    )


def card(num, kind, kind_color, title, subtitle, objs, art, accent, link_label, title_size=40, lines=None):
    cid = f"clip{num}"
    defs = ("<defs>" + panel_clip(cid, W, H, 28)
            + glow_filter("gy", YELLOW, 5, 1) + glow_filter("gc", CYAN, 3, 2)
            + glow_filter("gm", MAGENTA, 3, 2)
            + '<pattern id="sl" width="4" height="4" patternUnits="userSpaceOnUse">'
              '<rect width="4" height="1" fill="#000" opacity=".3"/></pattern>'
            + '<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">'
              f'<path d="M28 0H0V28" fill="none" stroke="{accent}" stroke-opacity=".07"/></pattern>'
            + f'<clipPath id="chip{num}"><polygon points="148,30 {148+text_width(kind,"rajdhani-700",15,2.5)+30:.0f},30 '
              f'{148+text_width(kind,"rajdhani-700",15,2.5)+20:.0f},54 148,54"/></clipPath>'
            + runglow(accent)
            + f'<linearGradient id="bsg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{accent}" stop-opacity="0"/>'
              f'<stop offset=".5" stop-color="{accent}" stop-opacity=".22"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></linearGradient>'
            + f'<linearGradient id="bgg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG2}"/>'
              f'<stop offset="1" stop-color="{BG}"/></linearGradient>'
            + "</defs>")

    big = f"{num:02d}"
    body = (
        defs + f'<g clip-path="url(#{cid})">'
        f'<rect width="{W}" height="{H}" fill="url(#bgg)"/>'
        f'<rect width="{W}" height="{H}" fill="url(#grid)"/>'
        # left rail
        f'<rect x="0" y="0" width="118" height="{H}" fill="{accent}" opacity=".08"/>'
        f'<rect x="118" y="0" width="2" height="{H}" fill="{accent}" opacity=".5"/>'
        + T(big, 59, 120, "orbitron-900", 64, "none", 0, "middle",
            f'stroke="{accent}" stroke-width="1.6" stroke-opacity=".25"')
        + T(big, 59, 120, "orbitron-900", 64, "none", 0, "middle",
            f'stroke="{accent}" stroke-width="1.8" pathLength="100" class="draw"')
        + T("GIG", 59, 156, "rajdhani-700", 22, accent, 8, "middle")
        + "".join(f'<rect x="38" y="{190+i*16}" width="42" height="8" fill="{accent}" '
                  f'opacity="{0.8-i*0.15:.2f}" class="hx d{i}"/>' for i in range(5))
        # art panel (right)
        + art
        # header
        + f'<polygon points="148,30 {148+text_width(kind,"rajdhani-700",15,2.5)+30:.0f},30 '
          f'{148+text_width(kind,"rajdhani-700",15,2.5)+20:.0f},54 148,54" fill="{kind_color}"/>'
        + T(kind, 160, 48, "rajdhani-700", 15, BG, 2.5)
        + f'<g clip-path="url(#chip{num})"><rect class="sweep" x="140" y="20" width="26" height="44" '
          f'fill="#fff" opacity=".45" transform="skewX(-20)"/></g>'
        + '<g class="gl gl1">' + T(title, 148, 102, "orbitron-900", title_size, CYAN, 1.5) + '</g>'
        + '<g class="gl gl2">' + T(title, 148, 102, "orbitron-900", title_size, RED, 1.5) + '</g>'
        + T(title, 148, 102, "orbitron-900", title_size, YELLOW, 1.5, extra='filter="url(#gy)"')
        + T(subtitle, 150, 132, "rajdhani-600", 20, CYAN, 1.2)
        + f'<rect x="150" y="146" width="520" height="1.5" fill="{TEXT}" opacity=".15"/>'
        + T("OBJECTIVES", 150, 172, "sharetechmono", 14, DIM, 3)
        + objectives(objs, 150, 202)
        + brief(lines, accent)
        # link hint
        + T(link_label, 150, H - 16, "sharetechmono", 15, accent, 0.5, extra='opacity=".8"')
        # fx
        + f'<rect width="{W}" height="{H}" fill="url(#sl)"/>'
        + f'<rect class="scan" x="0" y="-8" width="{W}" height="8" fill="{accent}" opacity=".05"/>'
        + "</g>"
        + frame(W, H, accent, 28, extra='stroke-opacity=".55"')
        + runner(W, H, accent, 28, sw=3, dur=6, length=180)
        + f'<rect x="{W-120}" y="0" width="90" height="4" fill="{accent}"/>'
        + f'<rect x="30" y="{H-4}" width="160" height="4" fill="{accent}"/>'
    )
    return svg(W, H, body, f"Gig {big}: {title}", STYLE)


# ---------------------------------------------------------------- intensive
def intensive():
    ax, ay = 730, 50  # art origin
    stages = ["CODE", "SAST", "SCA", "DAST", "SHIP"]
    pipe = []
    for i, s in enumerate(stages):
        x = ax + 20 + i * 88
        y = ay + 210
        col = CYAN if i < 4 else YELLOW
        pipe.append(f'<polygon points="{x},{y} {x+66},{y} {x+74},{y+14} {x+66},{y+28} {x},{y+28} {x+8},{y+14}" '
                    f'fill="{BG}" stroke="{col}" stroke-width="1.5"/>')
        pipe.append(T(s, x + 38, y + 20, "rajdhani-700", 14, col, 1.5, "middle"))
    shield_cx, shield_cy = ax + 230, ay + 105
    sh = (f'M{shield_cx} {shield_cy-78} L{shield_cx+66} {shield_cy-52} L{shield_cx+60} {shield_cy+20} '
          f'Q{shield_cx+44} {shield_cy+62} {shield_cx} {shield_cy+82} '
          f'Q{shield_cx-44} {shield_cy+62} {shield_cx-60} {shield_cy+20} L{shield_cx-66} {shield_cy-52} Z')
    art = (
        f'<g>'
        # hex halo
        + "".join(f'<circle cx="{shield_cx}" cy="{shield_cy}" r="{r}" fill="none" stroke="{CYAN}" '
                  f'stroke-opacity="{o}" stroke-dasharray="{d}" class="flk"/>'
                  for r, o, d in [(108, .15, "2 6"), (124, .25, "40 10 4 10"), (140, .1, "1 4")])
        + f'<g class="pulse" filter="url(#gc)"><path d="{sh}" fill="{CYAN}" fill-opacity=".08" stroke="{CYAN}" stroke-width="2.5"/>'
        f'<path d="M{shield_cx-26} {shield_cy+2} l18 18 l36 -40" fill="none" stroke="{YELLOW}" stroke-width="7" stroke-linecap="square"/></g>'
        + T("OWASP TOP 10", shield_cx - 200, shield_cy - 60, "sharetechmono", 15, MAGENTA, 1)
        + T("API SECURITY", shield_cx + 110, shield_cy - 30, "sharetechmono", 15, MAGENTA, 1)
        + T("ACCESS CONTROL", shield_cx - 222, shield_cy + 40, "sharetechmono", 15, MAGENTA, 1)
        + T("SECURE SDLC", shield_cx + 110, shield_cy + 50, "sharetechmono", 15, MAGENTA, 1)
        + f'<path d="M{ax+20+5*88-14} {ay+224} H{ax+20+5*88}" stroke="{YELLOW}"/>'
        + f'<line x1="{ax+20}" y1="{ay+252}" x2="{ax+20+4*88+74}" y2="{ay+252}" stroke="{CYAN}" stroke-opacity=".6" class="flow"/>'
        + "".join(pipe)
        # data packet riding the pipeline
        + f'<g class="pkt"><circle cx="{ax+20}" cy="{ay+252}" r="4.5" fill="{YELLOW}" filter="url(#gy)"/>'
        f'<rect x="{ax-10}" y="{ay+251}" width="28" height="2" fill="{YELLOW}" opacity=".5"/></g>'
        # scanning beam inside the shield
        + f'<clipPath id="shc"><path d="{sh}"/></clipPath>'
        + f'<g clip-path="url(#shc)"><rect class="shscan" x="{shield_cx-70}" y="{shield_cy-3}" width="140" height="6" '
          f'fill="{CYAN}" opacity=".7" filter="url(#gc)"/></g>'
        + "</g>"
    )
    objs = [
        ("done", "Jacked in: 26-week AppSec / DevSecOps track", "OCT 2026"),
        ("active", "OWASP Top 10 - exploit it, then fix it", ""),
        ("active", "API security & broken access control", ""),
        ("todo", "Secure SDLC: SAST / SCA / DAST wired into CI", ""),
        ("todo", "Capstone + public write-ups", ""),
    ]
    return card(1, "MAIN JOB  //  IN PROGRESS", YELLOW, "APPSEC INTENSIVE",
                "OWASP Top 10  /  API security  /  Secure SDLC",
                objs, art, CYAN, "> github.com/GodFobos/Appsec-DevSecOps-Intensive", lines=[
                    [("A ", TEXT), ("26-week", YELLOW), (" track I started in ", TEXT), ("October 2026", YELLOW),
                     (": fundamentals > junior AppSec / DevSecOps.", TEXT)],
                    [("Every topic ends the same way: ", TEXT), ("break it, then fix it.", CYAN),
                     (" Labs and write-ups land in the repo.", TEXT)],
                ])


# ---------------------------------------------------------------- fuzzing
def fuzzing():
    ax, ay = 760, 34
    tw, th = 410, 292
    lines = [
        ("$ ./build.sh && ./run.sh", TEXT),
        ("target: benhoyt/inih", TEXT),
        ("engine: libFuzzer + ASan", DIM),
        ("#57453294 REDUCE cov: 82 ft: 539", CYAN),
        ("corp: 236/35Kb   lim: 4096", CYAN),
        ("exec/s: 135   rss: 520Mb", DIM),
        (None, DIM),
        ("crashes: 0   ASan: clean", "#39ff6a"),
    ]
    term = [f'<rect x="{ax}" y="{ay}" width="{tw}" height="{th}" fill="#05050a" stroke="{MAGENTA}" stroke-opacity=".7"/>'
            f'<rect x="{ax}" y="{ay}" width="{tw}" height="24" fill="{MAGENTA}" opacity=".18"/>'
            + T("FUZZ://SESSION-01", ax + 12, ay + 17, "rajdhani-700", 14, MAGENTA, 2)
            + "".join(f'<circle cx="{ax+tw-16-i*14}" cy="{ay+12}" r="4" fill="{c}"/>'
                      for i, c in enumerate([RED, YELLOW, "#39ff6a"]))]
    rnd = random.Random(1337)
    for i, (ln, col) in enumerate(lines):
        if ln is None:  # live mutation row: bytes flip between variants
            y = ay + 52 + i * 28
            row = [T("mutate:", ax + 14, y, "sharetechmono", 17, DIM, 0.1)]
            for b in range(8):
                bx = ax + 104 + b * 34
                for v in range(3):
                    val = rnd.randint(0, 255)
                    c = RED if rnd.random() < .15 else (YELLOW if rnd.random() < .3 else MAGENTA)
                    row.append(f'<g class="mut" style="animation-delay:-{(v*0.5 + b*0.13):.2f}s">'
                               + T(f"{val:02X}", bx, y, "sharetechmono", 17, c) + "</g>")
            term.append(f'<g class="line" style="animation-name:ln{i}">' + "".join(row) + "</g>")
            continue
        term.append(f'<g class="line" style="animation-name:ln{i}">'
                    + T(ln, ax + 14, ay + 52 + i * 28, "sharetechmono", 17, col, 0.1) + "</g>")
    # cursor
    term.append(f'<rect x="{ax+14}" y="{ay+52+len(lines)*28-15}" width="9" height="16" fill="{CYAN}" class="blink"/>')
    # per-line keyframes so lines appear one by one, hold, then reset
    kf = "".join(
        f"@keyframes ln{i}{{0%,{int((i+1)*8)}%{{opacity:0}}{int((i+1)*8)+1}%,100%{{opacity:1}}}}"
        for i in range(len(lines)))
    term.append(f"<style>.line{{animation-duration:9s;animation-timing-function:steps(1);"
                f"animation-iteration-count:infinite}}{kf}</style>")

    art = "".join(term)
    objs = [
        ("done", "Harness #1  benhoyt/inih", "57M+ execs  /  0 crashes"),
        ("active", "Harness #2  hsnborn22/C-json", ""),
        ("todo", "Harness #3  LloydLabs/librini", ""),
        ("todo", "Land a real bug -> responsible disclosure", ""),
    ]
    return card(2, "SIDE JOB  //  ACTIVE", MAGENTA, "FUZZING PLAYGROUND",
                "Coverage-guided fuzzing of C parsers: libFuzzer + ASan",
                objs, art, MAGENTA, "> github.com/GodFobos/fuzzing-playground", 38, lines=[
                    [("Every harness written by hand: ", TEXT), ("raw fuzzer bytes", MAGENTA),
                     (" > exactly the input the library expects.", TEXT)],
                    [("Millions of mutated inputs, ", TEXT), ("ASan", YELLOW), (" on watch. Goal: ", TEXT),
                     ("a real bug, reported responsibly.", MAGENTA)],
                ])


if __name__ == "__main__":
    for name, fn in [("gig-intensive", intensive), ("gig-fuzzing", fuzzing)]:
        p = ASSETS / f"{name}.svg"
        p.write_text(fn())
        print(p, p.stat().st_size)
