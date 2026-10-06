"""Build the catalogue page and the deployable site.

python build_index.py            -> writes _site/ with index.html + every published figure
python build_index.py --all      -> include drafts too (for local preview only)
"""
import html, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).parent
FIG = ROOT / "figures"
OUT = ROOT / "_site"
include_drafts = "--all" in sys.argv

def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    meta, key = {}, None
    if not m:
        return meta
    for line in m.group(1).splitlines():
        line = line.split(" #")[0].rstrip()
        if re.match(r"^\s+-\s", line) and key:
            meta.setdefault(key, []).append(line.strip()[2:].strip().strip('"'))
        elif ":" in line and not line.startswith(" "):
            key, val = line.split(":", 1)
            key, val = key.strip(), val.strip().strip('"')
            meta[key] = val if val else []
    return meta

figs = []
for d in sorted(FIG.iterdir()):
    readme = d / "README.md"
    if not (d.is_dir() and readme.exists() and (d / "index.html").exists()):
        continue
    meta = front_matter(readme.read_text(encoding="utf-8"))
    if meta.get("status") != "published" and not include_drafts:
        continue
    meta["slug"] = d.name
    figs.append(meta)

figs.sort(key=lambda m: m.get("date", ""), reverse=True)

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
for m in figs:
    shutil.copytree(FIG / m["slug"], OUT / m["slug"],
                    ignore=shutil.ignore_patterns("*.py", "template.html", "__pycache__"))

def card(m):
    used = m.get("used_in") or []
    used = used if isinstance(used, list) else [used]
    used_html = "".join(f"<li>{html.escape(u)}</li>" for u in used)
    status = "" if m.get("status") == "published" else f' <span class="draft">{html.escape(m.get("status","draft"))}</span>'
    thumb = f'<img src="{m["slug"]}/static.png" alt="">' if (FIG / m["slug"] / "static.png").exists() else ""
    return (f'<article><a class="thumb" href="{m["slug"]}/">{thumb}</a><div>'
            f'<h2><a href="{m["slug"]}/">{html.escape(m.get("title", m["slug"]))}</a>{status}</h2>'
            f'<p class="meta">{html.escape(m.get("date",""))}</p>'
            f'<p>{html.escape(m.get("description",""))}</p>'
            f'{"<ul>"+used_html+"</ul>" if used_html else ""}</div></article>')

page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Interactive figures</title>
<style>
:root{{--bg:#fcfcfb;--t1:#0b0b0b;--t2:#52514e;--rule:#e4e3df;--link:#2a78d6}}
@media (prefers-color-scheme:dark){{:root{{--bg:#1a1a19;--t1:#fff;--t2:#c3c2b7;--rule:#3a3a37;--link:#6da7ec}}}}
body{{margin:0;background:var(--bg);color:var(--t1);font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}}
main{{max-width:900px;margin:0 auto;padding:32px 16px}}
h1{{font-size:26px;margin:0 0 6px}} .lead{{color:var(--t2);margin:0 0 28px}}
article{{display:grid;grid-template-columns:200px 1fr;gap:20px;padding:20px 0;border-top:1px solid var(--rule)}}
@media (max-width:600px){{article{{grid-template-columns:1fr}}}}
.thumb img{{width:100%;border-radius:6px;border:1px solid var(--rule)}}
h2{{font-size:18px;margin:0 0 4px}} a{{color:var(--link)}} .meta{{color:var(--t2);font-size:13px;margin:0 0 8px}}
p,li{{font-size:15px;line-height:1.45}} ul{{padding-left:18px;color:var(--t2)}}
.draft{{font-size:12px;background:#eda100;color:#000;border-radius:4px;padding:1px 6px;margin-left:6px}}
</style></head><body><main>
<h1>Interactive figures</h1>
<p class="lead">Figures by Oliver Harman and co-authors. Each figure page lists its sources.</p>
{"".join(card(m) for m in figs) or "<p>No published figures yet.</p>"}
</main></body></html>"""
(OUT / "index.html").write_text(page, encoding="utf-8")
print(f"Built _site/ with {len(figs)} figure(s): " + ", ".join(m["slug"] for m in figs))
