"""Genera el sitio estático (GitHub Pages) a partir del manifest.

Produce site/index.html: un portal con las 12 partes y las 176 clases, cada una
enlazada a su README en el repositorio. Autocontenido, sin dependencias externas.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
CLASSES = ROOT / "classes"
SITE = ROOT / "site"
REPO = "https://github.com/vladimiracunadev-create/polyglot-programming-labs/blob/main"

CSS = """
:root { --bg:#0d1117; --card:#161b22; --fg:#e6edf3; --mut:#8b949e; --acc:#7c5cff; --ok:#2e8b57; }
* { box-sizing:border-box; }
body { margin:0; font:16px/1.6 -apple-system,Segoe UI,Roboto,sans-serif; background:var(--bg); color:var(--fg); }
header { padding:3rem 1.5rem; text-align:center; background:linear-gradient(135deg,#1a1030,#0d1117); }
header h1 { font-size:2.4rem; margin:.2rem 0; }
header p { color:var(--mut); max-width:42rem; margin:.5rem auto; }
.badges { margin-top:1rem; }
.badge { display:inline-block; padding:.3rem .7rem; margin:.2rem; border-radius:1rem; font-size:.8rem; background:var(--card); color:var(--acc); border:1px solid #30363d; }
main { max-width:60rem; margin:0 auto; padding:1.5rem; }
.part { background:var(--card); border:1px solid #30363d; border-radius:.6rem; margin:1rem 0; padding:1rem 1.3rem; }
.part h2 { margin:.2rem 0; font-size:1.2rem; }
.part .sub { color:var(--mut); font-size:.9rem; margin:.2rem 0 .8rem; }
.cls { display:block; padding:.35rem 0; border-bottom:1px solid #21262d; color:var(--fg); text-decoration:none; }
.cls:hover { color:var(--acc); }
.cls .n { color:var(--mut); font-variant-numeric:tabular-nums; margin-right:.6rem; }
.st { font-size:.75rem; margin-left:.4rem; }
footer { text-align:center; color:var(--mut); padding:2rem; font-size:.85rem; }
a { color:var(--acc); }
"""


def main():
    manifest = json.loads((CLASSES / "_manifest.json").read_text(encoding="utf-8"))
    parts_html = []
    for p in manifest["parts"]:
        clases = []
        for c in p["classes"]:
            st = "✅" if c["built"] else "🚧"
            url = f"{REPO}/classes/{p['slug']}/{c['slug']}/README.md"
            clases.append(
                f'<a class="cls" href="{url}"><span class="n">{c["num"]:03d}</span>'
                f'{c["title"]}<span class="st">{st}</span></a>'
            )
        parts_html.append(
            f'<section class="part"><h2>Parte {p["idx"]} — {p["title"]}</h2>'
            f'<div class="sub">{p["subtitle"]}</div>{"".join(clases)}</section>'
        )

    built = manifest["total_built"]
    planned = manifest["total_planned"]
    html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Polyglot Programming Labs</title><style>{CSS}</style></head>
<body>
<header>
  <h1>🌐 Polyglot Programming Labs</h1>
  <p>Aprende el concepto una vez. Reconócelo, compáralo y aplícalo en cualquier lenguaje.</p>
  <div class="badges">
    <span class="badge">{planned} clases · {len(manifest['parts'])} partes</span>
    <span class="badge">núcleo de {len(manifest['nucleo'])} lenguajes</span>
    <span class="badge">{built} construidas</span>
  </div>
  <p><a href="{REPO}/README.md">Repositorio</a> ·
     <a href="{REPO}/atlas/README.md">Atlas</a> ·
     <a href="{REPO}/rutas/README.md">Rutas</a> ·
     <a href="{REPO}/autoevaluaciones/README.md">Autoevaluación</a></p>
</header>
<main>{"".join(parts_html)}</main>
<footer>Generado desde <code>classes/_manifest.json</code> · Leyenda: ✅ construida · 🚧 planificada · MIT</footer>
</body></html>
"""
    SITE.mkdir(exist_ok=True)
    (SITE / "index.html").write_text(html, encoding="utf-8")
    print(f"Sitio generado en {SITE / 'index.html'} ({planned} clases).")


if __name__ == "__main__":
    main()
