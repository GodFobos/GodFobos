"""Netrunner biomonitor: live GitHub stats rendered as Night City.

Runs daily in GitHub Actions (see .github/workflows/stats.yml):
  python tools/stats.py --user GodFobos --out out/stats.svg
Needs GITHUB_TOKEN (or STATS_TOKEN) in the environment.
`--demo` renders made-up numbers for local previews.
"""
import argparse
import datetime as dt
import json
import os
import random
import urllib.request
from collections import defaultdict

from cyber import (BG, BG2, CYAN, DIM, MAGENTA, RED, TEXT, YELLOW, T, frame,
                   glow_filter, panel_clip, runglow, runner, svg, text_width)

W, H = 1200, 400
API = "https://api.github.com/graphql"


# ------------------------------------------------------------------ data
def gql(query, variables, token):
    req = urllib.request.Request(
        API, data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "netrunner-stats"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if data.get("errors"):
        raise SystemExit(f"GraphQL error: {data['errors']}")
    return data["data"]


Q_YEAR = """query($login:String!,$from:DateTime!,$to:DateTime!){
 user(login:$login){contributionsCollection(from:$from,to:$to){
  contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}"""

Q_USER = """query($login:String!){user(login:$login){createdAt
 contributionsCollection{totalCommitContributions contributionCalendar{totalContributions}}
 repositories(ownerAffiliations:OWNER,isFork:false,first:100,privacy:PUBLIC){totalCount
  nodes{languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}}}"""


def fetch(login, token):
    u = gql(Q_USER, {"login": login}, token)["user"]
    today = dt.date.today()
    start_year = int(u["createdAt"][:4])
    days = {}
    for y in range(start_year, today.year + 1):
        frm = f"{y}-01-01T00:00:00Z"
        to = f"{y}-12-31T23:59:59Z" if y < today.year else today.strftime("%Y-%m-%dT23:59:59Z")
        cal = gql(Q_YEAR, {"login": login, "from": frm, "to": to}, token)
        for w in cal["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]:
            for d in w["contributionDays"]:
                days[d["date"]] = d["contributionCount"]
    langs = defaultdict(int)
    colors = {}
    for repo in u["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]] += e["size"]
            colors[e["node"]["name"]] = e["node"]["color"]
    cc = u["contributionsCollection"]
    return {
        "days": days,
        "year_total": cc["contributionCalendar"]["totalContributions"],
        "commits": cc["totalCommitContributions"],
        "repos": u["repositories"]["totalCount"],
        "langs": sorted(langs.items(), key=lambda kv: -kv[1]),
        "since": u["createdAt"][:10],
    }


def demo():
    rnd = random.Random(7)
    today = dt.date.today()
    days = {}
    for i in range(400):
        d = today - dt.timedelta(days=i)
        active = rnd.random() < (0.85 if i < 23 else 0.42)
        days[d.isoformat()] = rnd.choice([1, 1, 2, 3, 4, 6, 9]) if active else 0
    for i in range(23):  # guarantee a visible current streak
        days[(today - dt.timedelta(days=i)).isoformat()] = max(1, days[(today - dt.timedelta(days=i)).isoformat()])
    return {"days": days, "year_total": sum(list(days.values())[:365]), "commits": 412, "repos": 6,
            "langs": [("Python", 61000), ("C", 23000), ("Shell", 9000), ("PowerShell", 3000), ("HTML", 2000)],
            "since": "2024-05-01"}


def streaks(days):
    today = dt.date.today()
    seq = sorted(days)
    longest = run = 0
    prev = None
    for ds in seq:
        d = dt.date.fromisoformat(ds)
        if days[ds] > 0:
            run = run + 1 if prev and (d - prev).days == 1 and days[prev.isoformat()] > 0 else 1
            longest = max(longest, run)
        else:
            run = 0
        prev = d
    # current streak: today counts if active, otherwise start from yesterday
    cur = 0
    d = today if days.get(today.isoformat(), 0) > 0 else today - dt.timedelta(days=1)
    while days.get(d.isoformat(), 0) > 0:
        cur += 1
        d -= dt.timedelta(days=1)
    return cur, longest


def weeks_last_year(days):
    today = dt.date.today()
    start = today - dt.timedelta(days=today.weekday() + 7 * 51)
    out = []
    for w in range(52):
        tot = sum(days.get((start + dt.timedelta(days=w * 7 + i)).isoformat(), 0) for i in range(7))
        out.append(tot)
    return out


# ---------------------------------------------------------------- render
def render(data, is_demo=False):
    cur, longest = streaks(data["days"])
    weeks = weeks_last_year(data["days"])
    active_days = sum(1 for v in list(data["days"].values()) if v > 0)
    cid = "sc"
    defs = ("<defs>" + panel_clip(cid, W, H, 28)
            + glow_filter("gy", YELLOW, 6, 1) + glow_filter("gc", CYAN, 3, 2) + glow_filter("gm", MAGENTA, 3, 1)
            + '<pattern id="sl" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".3"/></pattern>'
            + f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG}"/>'
              '<stop offset=".7" stop-color="#1a0b2e"/><stop offset="1" stop-color="#3a0d3f"/></linearGradient>'
            + f'<linearGradient id="beamg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/>'
              f'<stop offset="1" stop-color="{CYAN}" stop-opacity=".25"/></linearGradient>'
            + runglow(YELLOW)
            + "</defs>")

    # ---- left: streak gauge
    gx, gy, r = 150, 196, 92
    circ = 2 * 3.14159 * r
    frac = min(1.0, cur / max(longest, 1)) if longest else 0
    gauge = (
        f'<circle cx="{gx}" cy="{gy}" r="{r+16}" fill="none" stroke="{YELLOW}" stroke-opacity=".12" stroke-dasharray="2 5"/>'
        f'<circle cx="{gx}" cy="{gy}" r="{r}" fill="none" stroke="{DIM}" stroke-opacity=".35" stroke-width="10"/>'
        f'<circle cx="{gx}" cy="{gy}" r="{r}" fill="none" stroke="{YELLOW}" stroke-width="10" '
        f'stroke-dasharray="{circ*frac:.1f} {circ:.1f}" transform="rotate(-90 {gx} {gy})" filter="url(#gy)" class="arc"/>'
        + f'<circle cx="{gx}" cy="{gy}" r="{r-18}" fill="none" stroke="{CYAN}" stroke-opacity=".35" stroke-dasharray="30 8 3 8" class="spin"/>'
        + T(str(cur), gx, gy + 22, "orbitron-900", 64 if cur < 100 else 50, YELLOW, 0, "middle", 'filter="url(#gy)" class="num"')
        + T("DAY STREAK", gx, gy + 50, "rajdhani-700", 16, CYAN, 4, "middle")
        + T("CURRENT", gx, gy - 46, "sharetechmono", 14, DIM, 3, "middle")
    )

    # ---- stat chips under/next to gauge
    def stat(x, y, label, value, col):
        return (f'<rect x="{x}" y="{y}" width="3" height="40" fill="{col}"/>'
                + T(value, x + 14, y + 24, "orbitron-700", 24, col)
                + T(label, x + 14, y + 42, "sharetechmono", 13, DIM, 1.2))

    stats_col = (
        stat(300, 92, "LONGEST STREAK", f"{longest}d", MAGENTA)
        + stat(300, 156, "CONTRIBS / 12 MO", f"{data['year_total']}", CYAN)
        + stat(300, 220, "COMMITS / 12 MO", f"{data['commits']}", YELLOW)
        + stat(300, 284, "ACTIVE DAYS", f"{active_days}", TEXT)
    )

    # ---- middle: the year as a skyline
    sx, sy, sw, shh = 480, 92, 420, 228  # area
    bw = sw / 52
    mx = max(max(weeks), 1)
    rnd = random.Random(sum(weeks) + 3)
    city = [f'<rect x="{sx}" y="{sy}" width="{sw}" height="{shh}" fill="url(#sky)" opacity=".9"/>']
    for i, v in enumerate(weeks):
        h = 14 + (shh - 40) * (v / mx) ** 0.75 if v else 8
        x = sx + i * bw
        top = sy + shh - h
        fill = "#26163f" if v else "#120c1e"
        city.append(f'<g class="rise" style="animation-delay:{i*0.035:.2f}s">')
        city.append(f'<rect x="{x+0.6:.1f}" y="{top:.1f}" width="{bw-1.2:.1f}" height="{h:.1f}" fill="{fill}"/>'
                    f'<rect x="{x+0.6:.1f}" y="{top:.1f}" width="{bw-1.2:.1f}" height="1.5" fill="{MAGENTA}" opacity=".45"/>')
        # lit windows ~ contributions
        slots = int(h // 7)
        lit = min(slots, v)
        for k in range(lit):
            wy = sy + shh - 6 - k * 7 - rnd.randint(0, 1)
            col = YELLOW if v >= mx * 0.6 else (CYAN if v >= mx * 0.25 else MAGENTA)
            tw = f' class="tw" style="animation-delay:-{rnd.uniform(0,6):.1f}s"' if rnd.random() < .12 else ""
            city.append(f'<rect x="{x+bw/2-1.6:.1f}" y="{wy:.1f}" width="3.2" height="3" fill="{col}" opacity="{rnd.uniform(.5,.95):.2f}"{tw}/>')
        if v == mx:
            city.append(f'<circle cx="{x+bw/2:.1f}" cy="{top-6:.1f}" r="2.2" fill="{RED}" class="blink" filter="url(#gm)"/>')
        city.append("</g>")
    city.append(f'<rect x="{sx}" y="{sy+shh}" width="{sw}" height="2" fill="{YELLOW}" opacity=".7"/>')
    # scanner beam sweeping across the year
    city.append(f'<clipPath id="cityclip"><rect x="{sx}" y="{sy}" width="{sw}" height="{shh}"/></clipPath>'
                f'<g clip-path="url(#cityclip)"><g class="beam">'
                f'<rect x="{sx-40}" y="{sy}" width="40" height="{shh}" fill="url(#beamg)"/>'
                f'<rect x="{sx-2}" y="{sy}" width="2" height="{shh}" fill="{CYAN}" opacity=".9"/></g></g>')
    city.append(T("52 WEEKS  //  1 BUILDING = 1 WEEK  //  1 LIGHT = 1 CONTRIBUTION",
                  sx + sw / 2, sy + shh + 24, "sharetechmono", 12, DIM, 0.4, "middle"))
    months = []
    today = dt.date.today()
    for i in range(0, 52, 13):
        d = today - dt.timedelta(weeks=51 - i)
        months.append(T(d.strftime("%b").upper(), sx + i * bw + 2, sy - 8, "sharetechmono", 13, DIM, 1))
    city += months

    # ---- right: languages as cyberware load
    lx, ly = 940, 92
    langs = data["langs"][:5]
    total = sum(v for _, v in langs) or 1
    palette = [YELLOW, CYAN, MAGENTA, "#39ff6a", "#ff8a3d"]
    lang_rows = [T("CYBERWARE LOAD", lx, ly - 18, "sharetechmono", 14, DIM, 3)]
    for i, (name, size) in enumerate(langs):
        y = ly + i * 52
        pct = size / total
        col = palette[i]
        lang_rows.append(T(name.upper(), lx, y + 14, "rajdhani-700", 19, TEXT, 1.5))
        lang_rows.append(T(f"{pct*100:.0f}%", lx + 220, y + 14, "orbitron-700", 14, col, 0, "end"))
        segs = 20
        on = max(1, round(pct * segs))
        lang_rows.append(f'<g class="bar" style="animation-delay:{0.4+i*0.15:.2f}s">')
        for s in range(segs):
            lang_rows.append(f'<rect x="{lx + s*11}" y="{y+22}" width="8" height="10" fill="{col if s < on else DIM}" '
                             f'opacity="{1 if s < on else .25}"/>')
        lang_rows.append("</g>")

    title = (T("BIOMONITOR", 40, 52, "orbitron-900", 26, YELLOW, 2, extra='filter="url(#gy)"')
             + T(f"//  NETRUNNER WHITEKING  //  UPDATED {today.isoformat()}", 268, 50, "sharetechmono", 15, DIM, 1))
    watermark = ((f'<rect x="{W-260}" y="{H-50}" width="210" height="28" fill="none" stroke="{RED}" stroke-width="2"/>'
                  + T("DEMO DATA // PREVIEW", W - 155, H - 30, "rajdhani-700", 16, RED, 2, "middle"))
                 if is_demo else "")
    style = """
    .blink{animation:blink 1.3s steps(1) infinite}@keyframes blink{0%,55%{opacity:1}56%,100%{opacity:.2}}
    .spin{transform-origin:150px 196px;animation:spin 14s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}
    .arc{animation:arc 2.2s ease-out}@keyframes arc{from{stroke-dasharray:0 600}}
    .rise{transform-box:fill-box;transform-origin:50% 100%;animation:rise 1.1s cubic-bezier(.2,.9,.3,1.2) both}
    @keyframes rise{from{transform:scaleY(0)}to{transform:scaleY(1)}}
    .tw{animation:tw 6s steps(1) infinite}@keyframes tw{0%,80%{opacity:.9}81%,100%{opacity:.05}}
    .beam{animation:beam 6s ease-in-out infinite}@keyframes beam{0%{transform:translateX(0)}70%,100%{transform:translateX(460px)}}
    .bar{transform-box:fill-box;transform-origin:0 50%;animation:bar 1.4s ease-out both}@keyframes bar{from{transform:scaleX(0)}}
    .num{animation:num 3s steps(1) infinite}@keyframes num{0%,92%{opacity:1}93%{opacity:.3}95%{opacity:1}96%{opacity:.4}97%,100%{opacity:1}}
    @media (prefers-reduced-motion:reduce){*{animation:none!important}}
    """
    body = (defs + f'<g clip-path="url(#{cid})"><rect width="{W}" height="{H}" fill="{BG2}"/>'
            + title + gauge + stats_col + "".join(city) + "".join(lang_rows) + watermark
            + f'<rect width="{W}" height="{H}" fill="url(#sl)"/></g>'
            + frame(W, H, YELLOW, 28, extra='stroke-opacity=".55"')
            + runner(W, H, YELLOW, 28, sw=3, dur=7, length=200)
            + f'<rect x="{W-140}" y="0" width="110" height="4" fill="{YELLOW}"/>')
    return svg(W, H, body, f"GitHub stats: current streak {cur} days, longest {longest} days", style)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default="GodFobos")
    ap.add_argument("--out", default="out/stats.svg")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        data = demo()
    else:
        token = os.environ.get("STATS_TOKEN") or os.environ["GITHUB_TOKEN"]
        data = fetch(a.user, token)
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w") as f:
        f.write(render(data, a.demo))
    print("wrote", a.out)
