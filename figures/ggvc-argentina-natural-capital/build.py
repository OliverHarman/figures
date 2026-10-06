"""Build index.html for this figure from places.csv, wealth.csv, template.html and arg_prov.geojson.
Run:  python build.py
"""
import csv, html, json
from pathlib import Path
HERE = Path(__file__).parent

g = json.loads((HERE / "arg_prov.geojson").read_text(encoding="utf-8"))
minlon, maxlon, minlat, maxlat = -74.2, -53.3, -55.2, -21.6
K, AY = 14.0, 1.3                      # scale and vertical stretch (approximate cos-latitude correction)
W, H = (maxlon - minlon) * K, (maxlat - minlat) * K * AY
def P(lon, lat): return ((lon - minlon) * K, (maxlat - lat) * K * AY)

paths = []
for f in g["features"]:
    geom = f["geometry"]
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    d = ""
    for p in polys:
        pts = [P(*q) for q in p[0]]
        out = [pts[0]]
        for q in pts[1:]:
            if abs(q[0] - out[-1][0]) + abs(q[1] - out[-1][1]) > 0.8:
                out.append(q)
        if len(out) >= 4:
            d += "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in out) + "Z"
    paths.append(f'<path d="{d}"><title>{html.escape(f["properties"]["name"])}</title></path>')

places = list(csv.DictReader(open(HERE / "places.csv", encoding="utf-8")))
dots, data = [], {}
for r in places:
    x, y = P(float(r["lon"]), float(r["lat"]))
    cls = "ren" if r["type"] == "renewable" else "non"
    dots.append(f'<g class="pt {cls}" tabindex="0" role="button" data-id="{r["id"]}" '
                f'aria-label="{html.escape(r["name"])}: {html.escape(r["description"])}" '
                f'transform="translate({x:.1f},{y:.1f})"><circle r="16" class="hit"/><circle r="9" class="dot"/></g>')
    data[r["id"]] = dict(name=r["name"], desc=r["description"], src=r["source"], url=r["url"],
                         type="Renewable natural capital" if cls == "ren" else "Non-renewable natural capital")

wealth = list(csv.DictReader(open(HERE / "wealth.csv", encoding="utf-8")))
tot = sum(float(r["usd_per_person_2018"]) for r in wealth)
bar, x, BW = [], 0.0, 1000
for r in wealth:
    v = float(r["usd_per_person_2018"]); w = v / tot * BW
    bar.append(f'<rect class="seg {r["css_class"]}" x="{x+1:.1f}" y="0" width="{max(w-2,1.5):.1f}" height="36" rx="3" '
               f'tabindex="0" data-seg="{html.escape(r["component"])}" data-val="{v:,.0f}" '
               f'data-pct="{v/tot*100:.1f}" data-mob="{html.escape(r["mobility"])}"/>')
    x += w

rows = "".join(f'<tr><td>{i}</td><td>{html.escape(d["name"])}</td><td>{html.escape(d["type"].split()[0])}</td>'
               f'<td>{html.escape(d["desc"])} <a href="{d["url"]}" target="_blank" rel="noopener">{html.escape(d["src"])}</a></td></tr>'
               for i, d in data.items())
out = ((HERE / "template.html").read_text(encoding="utf-8")
       .replace("%%W2%%", f"{W+40:.0f}").replace("%%H2%%", f"{H+40:.0f}")
       .replace("%%PATHS%%", "\n".join(paths)).replace("%%DOTS%%", "\n".join(dots))
       .replace("%%BAR%%", "\n".join(bar)).replace("%%DATA%%", json.dumps(data, ensure_ascii=False))
       .replace("%%ROWS%%", rows))
(HERE / "index.html").write_text(out, encoding="utf-8")
print(f"Wrote index.html (total wealth per person US${tot:,.0f})")
