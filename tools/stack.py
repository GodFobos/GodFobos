"""Stack panel: one image, every chip the same height, every row on one line -> assets/stack.svg

Brand icons come from simple-icons (CC0), stored in tools/icons.json.
"""
import json
from pathlib import Path

from cyber import BG, BG2, CYAN, DIM, MAGENTA, TEXT, YELLOW, T, svg, text_width

ROOT = Path(__file__).resolve().parent
ICONS = json.loads((ROOT / "icons.json").read_text())
GREEN = "#39ff6a"
ORANGE = "#ff6633"

GROUPS = [
    ("APPSEC", YELLOW, [("OWASP Top 10", "owasp", TEXT), ("Burp Suite", "burpsuite", ORANGE), ("OWASP ZAP", "zap", CYAN),
                        ("PortSwigger", "portswigger", ORANGE), ("SAST / DAST", None, None), ("API security", "swagger", GREEN)]),
    ("DEVSECOPS", CYAN, [("Docker", "docker", CYAN), ("Linux", "linux", YELLOW), ("GitHub Actions", "githubactions", TEXT),
                         ("CI/CD", None, None), ("Container security", "docker", MAGENTA), ("Git", "git", ORANGE)]),
    ("DETECTION", MAGENTA, [("SIEM · ELK", "elastic", YELLOW), ("OpenSearch", "opensearch", CYAN), ("Zeek", None, None),
                            ("Vuln management", None, None), ("YARA", None, None)]),
    ("CODE & RESEARCH", GREEN, [("Python", "python", YELLOW), ("SQL", "postgresql", CYAN), ("C", "c", CYAN),
                                ("libFuzzer + ASan", "llvm", MAGENTA), ("LLM × AppSec", "openai", TEXT)]),
]

W = 1200
LABEL_W = 236            # every row's chips start at the same x
ROW_H = 54
CHIP_H = 34
GAP = 10
FONT, FS, SP = "rajdhani-700", 16, 1.4


def chip(x, y, label, icon, color, accent):
    tw = text_width(label.upper(), FONT, FS, SP)
    pad = 14
    iw = 18 if icon else 0
    w = pad + (iw + 9 if icon else 0) + tw + pad
    out = [f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{CHIP_H}" rx="3" fill="{BG2}" stroke="{accent}" stroke-opacity=".28"/>']
    tx = x + pad
    if icon:
        s = iw / 24
        out.append(f'<path transform="translate({tx:.1f} {y + (CHIP_H - iw)/2:.1f}) scale({s:.3f})" d="{ICONS[icon]}" fill="{color}"/>')
        tx += iw + 9
    out.append(T(label.upper(), tx, y + CHIP_H / 2 + FS * .34, FONT, FS, TEXT, SP))
    return "".join(out), w


def build():
    rows = []
    y0 = 6
    widest = 0
    for gi, (name, accent, items) in enumerate(GROUPS):
        y = y0 + gi * ROW_H
        cy = y + CHIP_H / 2
        rows.append(f'<rect x="0" y="{y}" width="4" height="{CHIP_H}" fill="{accent}"/>')
        rows.append(T(name, 16, cy + 6, "orbitron-900", 14, accent, 2))
        x = LABEL_W
        for label, icon, color in items:
            c, w = chip(x, y, label, icon, color, accent)
            rows.append(c)
            x += w + GAP
        widest = max(widest, x - GAP)
    assert widest <= W, f"row too wide: {widest:.0f}px"
    H = y0 + len(GROUPS) * ROW_H - (ROW_H - CHIP_H) + 6
    title = "Stack: " + "; ".join(f"{g}: " + ", ".join(i[0] for i in items) for g, _, items in GROUPS)
    return svg(W, H, "".join(rows), title.replace("&", "and"))


if __name__ == "__main__":
    out = ROOT.parent / "assets" / "stack.svg"
    out.write_text(build())
    print(out, out.stat().st_size)
