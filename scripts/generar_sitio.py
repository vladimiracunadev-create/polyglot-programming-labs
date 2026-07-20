#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el sitio estático (`site/`) para GitHub Pages a partir de los Markdown
del repositorio.

Produce:
  site/index.html         portada: hero, cifras, qué incluye y las 12 partes
  site/buscar.html        buscador sobre las 176 clases (+ busqueda.json)
  site/**/*.html          cada README renderizado, con los enlaces .md -> .html
  site/autoevaluaciones/  quiz.html y progreso.html (interactivos)
  site/manual/MANUAL.pdf  el manual, si está generado

Uso:  python scripts/generar_sitio.py
Requiere: pip install "markdown>=3.6"
"""
from __future__ import annotations

import glob
import html as htmllib
import json
import os
import re
import shutil
import sys
import unicodedata

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site")
REPO_URL = "https://github.com/vladimiracunadev-create/polyglot-programming-labs"

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Markdown del nivel superior que se publican.
INCLUIR_TOP = [
    "README.md", "ROADMAP.md", "CONTRIBUTING.md", "SECURITY.md",
    "atlas/README.md", "rutas/README.md", "labs/README.md",
    "glosario/README.md", "autoevaluaciones/README.md",
    "docs/CURRICULO.md", "docs/METODOLOGIA.md", "docs/EXTENDER.md",
    "docs/syllabus.md", "docs/rubrica-evaluacion.md", "docs/examen-final-por-perfil.md",
]

# Enlaces internos: .md -> .html (conservando el ancla).
LINK_MD = re.compile(r"\]\(([^)]+?)\.md((?:#[^)]*)?)\)")

CSS_PAGINA = """
:root{--acento:#7c5cff;--acento2:#22d3ee;
  --bg:#fff;--bg2:#f7f6fc;--txt:#1b1f24;--muted:#5b6670;--card:#fff;--borde:#e6e2f2}
@media (prefers-color-scheme:dark){:root{--bg:#0d1117;--bg2:#12111c;--txt:#e6edf3;--muted:#9aa7b2;--card:#161b22;--borde:#272138}}
*{box-sizing:border-box}
body{font-family:system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  line-height:1.65;max-width:940px;margin:0 auto;padding:1.2rem 1.2rem 5rem;
  color:var(--txt);background:var(--bg)}
a{color:var(--acento);text-decoration:none}
a:hover{text-decoration:underline}
h1,h2,h3{line-height:1.25}
h1{border-bottom:1px solid var(--borde);padding-bottom:.3em}
h2{border-bottom:1px solid var(--borde);padding-bottom:.25em;margin-top:2rem}
code{background:var(--bg2);padding:.15em .35em;border-radius:4px;font-size:.9em}
pre{background:var(--bg2);border:1px solid var(--borde);border-radius:8px;padding:.9rem 1rem;overflow:auto}
pre code{background:none;padding:0}
blockquote{border-left:4px solid var(--acento);margin:1rem 0;padding:.2rem 1rem;color:var(--muted)}
table{border-collapse:collapse;width:100%;margin:1rem 0;display:block;overflow-x:auto}
th,td{border:1px solid var(--borde);padding:.45rem .6rem;text-align:left;vertical-align:top}
thead th{background:var(--bg2)}
img{max-width:100%}
.nav{background:var(--bg2);border:1px solid var(--borde);border-radius:10px;
  padding:.6rem .9rem;margin-bottom:1.4rem;font-size:.92rem}
footer{margin-top:3rem;border-top:1px solid var(--borde);padding-top:1rem;
  color:var(--muted);font-size:.87rem;text-align:center}
"""

PLANTILLA = """<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · Polyglot Programming Labs</title>
<style>{css}</style></head><body>
<div class="nav"><a href="{home}">🌐 Inicio</a> · <a href="{clases}">📚 Clases</a> ·
<a href="{atlas}">🧬 Atlas</a> · <a href="{rutas}">🧭 Rutas</a> ·
<a href="{quiz}">📝 Autoevaluación</a> · <a href="{buscar}">🔎 Buscar</a></div>
{body}
<footer>Polyglot Programming Labs · 176 clases · 12 partes ·
<a href="{repo}">Ver en GitHub</a> · MIT</footer>
</body></html>
"""

LANDING_CSS = """
:root{--acento:#7c5cff;--acento2:#22d3ee;
  --bg:#fff;--bg2:#f7f6fc;--txt:#12181d;--muted:#5b6670;--card:#fff;--borde:#e6e2f2}
@media (prefers-color-scheme:dark){:root{--bg:#0d1117;--bg2:#12111c;--txt:#e6edf3;--muted:#9aa7b2;--card:#161b22;--borde:#272138}}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  background:var(--bg);color:var(--txt);line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.wrap{max-width:1040px;margin:0 auto;padding:0 1.1rem}
/* Hero */
.hero{position:relative;overflow:hidden;color:#fff;text-align:center;padding:4.5rem 1.1rem 3.2rem;
  background:radial-gradient(1200px 520px at 50% -10%,#8b5cf6 0%,#5b21b6 45%,#1e1b4b 100%)}
.hero::after{content:"";position:absolute;inset:0;opacity:.12;
  background-image:linear-gradient(#fff 1px,transparent 1px),linear-gradient(90deg,#fff 1px,transparent 1px);
  background-size:32px 32px;mask-image:radial-gradient(circle at 50% 0,#000,transparent 72%)}
.hero>*{position:relative;z-index:1}
.hero .escudo{font-size:3.4rem;line-height:1;filter:drop-shadow(0 4px 16px rgba(0,0,0,.35))}
.hero h1{font-size:clamp(1.8rem,4.5vw,3rem);margin:.4rem 0 .3rem;font-weight:800;letter-spacing:-.5px}
.hero .sub{font-size:clamp(1rem,2.2vw,1.25rem);opacity:.94;max-width:680px;margin:0 auto 1.4rem}
.chips{display:flex;flex-wrap:wrap;gap:.5rem;justify-content:center;margin-bottom:1.6rem}
.chip{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.28);border-radius:999px;
  padding:.28rem .8rem;font-size:.85rem;font-weight:600;backdrop-filter:blur(4px)}
.cta{display:flex;flex-wrap:wrap;gap:.7rem;justify-content:center}
.btn{display:inline-block;padding:.7rem 1.3rem;border-radius:10px;font-weight:700;font-size:1rem;
  transition:transform .08s ease,box-shadow .2s}
.btn:hover{transform:translateY(-2px)}
.btn-1{background:#fff;color:#5b21b6;box-shadow:0 6px 22px rgba(0,0,0,.28)}
.btn-2{background:rgba(255,255,255,.14);color:#fff;border:1px solid rgba(255,255,255,.55)}
/* Aviso */
.aviso{background:var(--bg2);border-bottom:1px solid var(--borde);font-size:.9rem;color:var(--muted)}
.aviso .wrap{padding:.7rem 1.1rem;text-align:center}
/* Cifras */
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:1rem;margin:2.6rem 0}
.stat{background:var(--card);border:1px solid var(--borde);border-radius:14px;padding:1.1rem;text-align:center}
.stat b{display:block;font-size:1.9rem;color:var(--acento);font-weight:800;line-height:1}
.stat span{font-size:.85rem;color:var(--muted)}
/* Secciones */
h2.sec{font-size:1.5rem;margin:2.6rem 0 1.1rem;font-weight:800}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:1rem}
.feat{background:var(--card);border:1px solid var(--borde);border-radius:14px;padding:1.2rem;
  transition:border-color .2s,transform .08s;display:block}
.feat:hover{border-color:var(--acento);transform:translateY(-2px)}
.feat .ic{font-size:1.7rem}
.feat h3{margin:.5rem 0 .3rem;font-size:1.08rem}
.feat p{margin:0;color:var(--muted);font-size:.92rem}
/* Núcleo */
.langs{display:flex;flex-wrap:wrap;gap:.5rem;margin:.4rem 0 .2rem}
.lang{background:var(--card);border:1px solid var(--borde);border-radius:999px;
  padding:.3rem .85rem;font-size:.88rem;font-weight:600}
.lang.atlas{border-style:dashed;color:var(--muted);font-weight:500}
/* Partes */
.parts{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:.8rem}
.part{position:relative;display:flex;gap:.75rem;align-items:center;background:var(--card);
  border:1px solid var(--borde);border-radius:12px;padding:.8rem .9rem;
  transition:border-color .2s,transform .08s}
.part:hover{border-color:var(--acento);transform:translateY(-2px)}
.part .num{flex:0 0 auto;width:38px;height:38px;border-radius:10px;display:grid;place-items:center;
  font-weight:800;color:#fff;background:linear-gradient(135deg,var(--acento),#5b21b6)}
.part .t{font-size:.92rem;font-weight:600;line-height:1.25}
.part .c{font-size:.78rem;color:var(--muted)}
.part .estado{position:absolute;top:.5rem;right:.6rem;font-size:.7rem}
/* Footer */
footer{margin-top:3rem;border-top:1px solid var(--borde);background:var(--bg2)}
footer .wrap{padding:2rem 1.1rem;text-align:center;color:var(--muted);font-size:.9rem}
footer a{color:var(--acento);font-weight:600}
"""


# ---------------------------------------------------------------- utilidades

def leer(ruta: str) -> str:
    with open(ruta, encoding="utf-8") as f:
        return f.read()


def sin_acentos(texto: str) -> str:
    """Quita las tildes para que la búsqueda no dependa de escribirlas."""
    return "".join(c for c in unicodedata.normalize("NFD", texto)
                   if unicodedata.category(c) != "Mn")


def titulo_de(md: str, por_defecto: str) -> str:
    m = re.search(r"^#\s+(.+)$", md, re.M)
    return re.sub(r"[#*`]", "", m.group(1)).strip() if m else por_defecto


def render(md_texto: str, destino_rel: str) -> str:
    """Markdown -> HTML, con los enlaces internos .md reescritos a .html."""
    md_texto = LINK_MD.sub(lambda m: f"]({m.group(1)}.html{m.group(2)})", md_texto)
    cuerpo = markdown.markdown(
        md_texto, extensions=["tables", "fenced_code", "sane_lists", "toc", "attr_list"])
    subir = "../" * destino_rel.count("/")
    return PLANTILLA.format(
        title=titulo_de(md_texto, "Polyglot Programming Labs"),
        css=CSS_PAGINA, body=cuerpo, repo=REPO_URL,
        home=f"{subir}index.html",
        clases=f"{subir}classes/README.html",
        atlas=f"{subir}atlas/README.html",
        rutas=f"{subir}rutas/README.html",
        quiz=f"{subir}autoevaluaciones/quiz.html",
        buscar=f"{subir}buscar.html",
    )


def escribir(rel: str, contenido: str) -> None:
    destino = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(contenido)


# ---------------------------------------------------------------- portada

def partes_info() -> list[dict]:
    """Info real de cada parte, leída del disco."""
    out = []
    for pdir in sorted(glob.glob(os.path.join(ROOT, "classes", "parte-*")),
                       key=lambda p: int(re.search(r"parte-(\d+)", p).group(1))):
        idx = int(re.search(r"parte-(\d+)", os.path.basename(pdir)).group(1))
        titulo = titulo_de(leer(os.path.join(pdir, "README.md")), f"Parte {idx}")
        titulo = re.sub(r"^Parte\s+\d+\s*[—-]\s*", "", titulo).strip()
        nums = sorted(int(os.path.basename(c)[:3])
                      for c in glob.glob(os.path.join(pdir, "[0-9][0-9][0-9]-*"))
                      if os.path.isdir(c))
        if nums:
            out.append({"idx": idx, "slug": os.path.basename(pdir), "titulo": titulo,
                        "n": len(nums), "ini": nums[0], "fin": nums[-1]})
    return out


def escribir_landing(partes: list[dict], n_primos: int, n_terminos: int, n_preguntas: int) -> None:
    total = sum(p["n"] for p in partes)
    hay_manual = os.path.isfile(os.path.join(ROOT, "manual", "MANUAL.pdf"))

    nucleo = ["Python", "JavaScript", "TypeScript", "Java", "C#", "Go", "Rust", "C", "SQL", "PHP"]
    primos = ["Ruby", "Perl", "Lua", "Tcl", "R", "Kotlin", "Scala", "Clojure", "F#",
              "C++", "Zig", "Nim", "Prolog", "…"]

    stats = [
        (str(total), "clases"),
        (str(len(partes)), "partes"),
        ("10", "lenguajes del núcleo"),
        (f"{n_primos:,}".replace(",", " "), "programas primos"),
        (str(n_terminos), "términos de glosario"),
    ]
    stats_html = "".join(f'<div class="stat"><b>{v}</b><span>{k}</span></div>' for v, k in stats)

    feats = [
        ("📚", "Currículo paso a paso",
         f"{total} clases, cada una con el concepto, el algoritmo neutral y el código a la vista "
         "en los 10 lenguajes del núcleo.", "classes/README.html"),
        ("🧪", "Equivalencia verificada",
         "Cada clase define un casos.json y CI ejecuta las 10 implementaciones para comprobar "
         "que producen la misma salida. No es teoría: es equivalencia demostrada.", "labs/README.html"),
        ("🧬", "Atlas de familias",
         "39 cápsulas de ~40 lenguajes: historia, paradigma, memoria y toolchain. "
         "Aprende el representante, reconoce la familia entera.", "atlas/README.html"),
        ("🧭", "Rutas por perfil",
         "Recorridos para quien viene de Python, quiere sistemas, web, backend de empresa o datos.",
         "rutas/README.html"),
        ("📝", "Autoevaluación",
         f"{n_preguntas} preguntas (una batería por parte) con la explicación de cada respuesta.",
         "autoevaluaciones/quiz.html"),
        ("✅", "Tu progreso",
         f"Marca las {total} clases y sigue tu avance (se guarda en tu navegador).",
         "autoevaluaciones/progreso.html"),
        ("🔎", "Buscador",
         f"Encuentra cualquier tema entre las {total} clases: closures, ownership, GC, ABI, mónadas…",
         "buscar.html"),
        ("📖", "Glosario",
         f"{n_terminos} términos enlazados a la clase donde se explican en contexto.",
         "glosario/README.html"),
    ]
    if hay_manual:
        feats.append(("📕", "Manual en PDF",
                      f"Las {total} clases en un único PDF, en orden y con el código, "
                      "para leer de corrido o estudiar sin conexión.", "manual/MANUAL.pdf"))
    feats_html = "".join(
        f'<a class="feat" href="{u}"><div class="ic">{i}</div><h3>{t}</h3><p>{d}</p></a>'
        for i, t, d, u in feats)

    langs_html = "".join(f'<span class="lang">{l}</span>' for l in nucleo)
    primos_html = "".join(f'<span class="lang atlas">{l}</span>' for l in primos)

    parts_html = "".join(
        f'<a class="part" href="classes/{p["slug"]}/README.html">'
        f'<div class="num">{p["idx"]}</div>'
        f'<div><div class="t">{htmllib.escape(p["titulo"])}</div>'
        f'<div class="c">{p["n"]} clases · {p["ini"]:03d}–{p["fin"]:03d}</div></div>'
        f'<span class="estado">✅</span></a>'
        for p in partes)

    cuerpo = f"""
<header class="hero">
  <div class="escudo">🌐</div>
  <h1>Polyglot Programming Labs</h1>
  <p class="sub">Aprende el concepto una vez. Reconócelo, compáralo y aplícalo en
  10 lenguajes y ~40 familias — en español, con el código a la vista.</p>
  <div class="chips">
    <span class="chip">{total} clases</span><span class="chip">{len(partes)} partes</span>
    <span class="chip">10 del núcleo · ~40 familias</span>
    <span class="chip">Equivalencia verificada en CI</span><span class="chip">MIT</span>
  </div>
  <div class="cta">
    <a class="btn btn-1" href="classes/README.html">📚 Empezar el curso</a>
    <a class="btn btn-2" href="rutas/README.html">🧭 Elegir mi ruta</a>
    <a class="btn btn-2" href="buscar.html">🔎 Buscar</a>
  </div>
</header>
<div class="aviso"><div class="wrap">🧪 Curso abierto (MIT) · <b>{total} clases en {len(partes)} partes</b> ·
las 10 implementaciones de cada clase se <a href="labs/README.html">ejecutan en CI</a> y deben dar la misma salida.</div></div>
<main class="wrap">
  <div class="stats">{stats_html}</div>

  <h2 class="sec">Qué incluye</h2>
  <div class="grid">{feats_html}</div>

  <h2 class="sec">El núcleo que se implementa</h2>
  <div class="langs">{langs_html}</div>
  <p style="color:var(--muted);font-size:.92rem;margin:.9rem 0 .3rem">
    Y sus <b>primos</b>, que se comprenden por características en el
    <a href="atlas/README.html" style="color:var(--acento)">Atlas</a> y aparecen resolviendo
    el mismo problema bajo cada bloque de código:</p>
  <div class="langs">{primos_html}</div>

  <h2 class="sec">Las {len(partes)} partes</h2>
  <div class="parts">{parts_html}</div>
</main>
<footer><div class="wrap">
  Polyglot Programming Labs · {total} clases · licencia
  <a href="{REPO_URL}">MIT en GitHub</a><br>
  <a href="classes/README.html">Índice de clases</a> ·
  <a href="ROADMAP.html">Roadmap</a> ·
  <a href="CONTRIBUTING.html">Contribuir</a>
</div></footer>
"""
    doc = ("<!doctype html><html lang='es'><head><meta charset='utf-8'>"
           "<meta name='viewport' content='width=device-width,initial-scale=1'>"
           "<title>Polyglot Programming Labs · un concepto, 10 lenguajes</title>"
           f"<style>{LANDING_CSS}</style></head><body>{cuerpo}</body></html>")
    escribir("index.html", doc)


# ---------------------------------------------------------------- buscador

BUSCAR_HTML = """<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Buscar · Polyglot Programming Labs</title>
<style>
:root{--acento:#7c5cff;--bg:#fff;--bg2:#f7f6fc;--txt:#12181d;--muted:#5b6670;--card:#fff;--borde:#e6e2f2}
@media (prefers-color-scheme:dark){:root{--bg:#0d1117;--bg2:#12111c;--txt:#e6edf3;--muted:#9aa7b2;--card:#161b22;--borde:#272138}}
*{box-sizing:border-box}
body{margin:0;font-family:system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  background:var(--bg);color:var(--txt);line-height:1.6}
a{color:var(--acento);text-decoration:none}
header{background:linear-gradient(135deg,#7c5cff,#5b21b6);color:#fff;padding:2rem 1.1rem;text-align:center}
header h1{margin:.2rem 0;font-size:1.6rem}
.wrap{max-width:820px;margin:0 auto;padding:0 1.1rem 4rem}
.nav{font-size:.9rem;margin:1rem 0;opacity:.85}
#q{width:100%;padding:.8rem 1rem;font-size:1.05rem;border-radius:10px;
  border:1px solid var(--borde);background:var(--card);color:var(--txt)}
.r{background:var(--card);border:1px solid var(--borde);border-radius:10px;
  padding:.7rem .9rem;margin:.55rem 0}
.r .n{color:var(--muted);font-variant-numeric:tabular-nums;margin-right:.5rem}
.r .p{font-size:.8rem;color:var(--muted)}
mark{background:color-mix(in srgb,var(--acento) 30%,transparent);color:inherit;border-radius:3px}
.cnt{color:var(--muted);font-size:.9rem;margin:.8rem 0}
footer{text-align:center;color:var(--muted);font-size:.85rem;padding:2rem 1rem}
</style></head><body>
<header><div style="font-size:2rem">🔎</div><h1>Buscar en el curso</h1></header>
<div class="wrap">
  <div class="nav"><a href="index.html">🌐 Inicio</a> · <a href="classes/README.html">📚 Clases</a> ·
  <a href="atlas/README.html">🧬 Atlas</a> · <a href="glosario/README.html">📖 Glosario</a></div>
  <input id="q" placeholder="closures, ownership, recolección de basura, ABI, mónadas…" autofocus>
  <div class="cnt" id="cnt"></div>
  <div id="res"></div>
</div>
<footer><a href="__REPO__">Polyglot Programming Labs</a> · MIT</footer>
<script>
let D = [];
const $ = id => document.getElementById(id);
fetch('busqueda.json').then(r => r.json()).then(d => { D = d; buscar(); })
  .catch(() => { $('res').innerHTML = '<p>No se pudo cargar el índice.</p>'; });

$('q').oninput = buscar;

// El índice se guarda sin acentos: la consulta se normaliza igual.
const norm = s => s.normalize('NFD').replace(/[\\u0300-\\u036f]/g, '');

function buscar() {
  const t = norm($('q').value.trim().toLowerCase());
  if (!t) { $('res').innerHTML = ''; $('cnt').textContent = D.length + ' clases indexadas'; return; }
  const pals = t.split(/\\s+/);
  const hits = D.filter(c => pals.every(p => c.b.includes(p))).slice(0, 60);
  $('cnt').textContent = hits.length ? hits.length + ' resultado(s)' : 'Sin resultados';
  $('res').innerHTML = hits.map(c => `
    <div class="r">
      <a href="${c.u}"><span class="n">${String(c.n).padStart(3,'0')}</span>${res(c.t, pals)}</a>
      <div class="p">Parte ${c.p} — ${esc(c.pt)}</div>
    </div>`).join('');
}
function esc(s){return String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
function res(s, pals){
  let h = esc(s);
  pals.forEach(p => { if (p) h = h.replace(new RegExp('(' + p.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&') + ')','gi'), '<mark>$1</mark>'); });
  return h;
}
</script></body></html>
"""


def escribir_buscador(partes: list[dict]) -> int:
    """Índice de búsqueda: número, título, parte y un blob de texto normalizado."""
    idx = []
    for p in partes:
        pdir = os.path.join(ROOT, "classes", p["slug"])
        for cdir in sorted(glob.glob(os.path.join(pdir, "[0-9][0-9][0-9]-*"))):
            rm = os.path.join(cdir, "README.md")
            if not os.path.isfile(rm):
                continue
            md = leer(rm)
            num = int(os.path.basename(cdir)[:3])
            titulo = re.sub(r"^Clase\s+\d+\s*[—-]\s*", "", titulo_de(md, f"Clase {num}"))
            # Se indexan título, objetivo, temas y definiciones: bastante para
            # encontrar una clase sin inflar el JSON con el curso entero.
            trozos = [titulo]
            for sec in ("🎯 Objetivo", "🗺️ Temas", "📖 Definiciones"):
                m = re.search(r"^##\s+" + sec + r"[^\n]*\n(.*?)(?=^##\s)", md, re.M | re.S)
                if m:
                    trozos.append(m.group(1))
            blob = re.sub(r"[`*#|>\[\]()]", " ", " ".join(trozos))
            # Sin acentos: quien busca "recursion" debe encontrar "Recursión".
            blob = sin_acentos(re.sub(r"\s+", " ", blob).lower())[:1400]
            idx.append({"n": num, "t": titulo, "p": p["idx"], "pt": p["titulo"],
                        "u": f'classes/{p["slug"]}/{os.path.basename(cdir)}/README.html',
                        "b": blob})
    escribir("busqueda.json", json.dumps(idx, ensure_ascii=False, separators=(",", ":")))
    escribir("buscar.html", BUSCAR_HTML.replace("__REPO__", REPO_URL))
    return len(idx)


# ---------------------------------------------------------------- main

def main() -> int:
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)

    generados = 0

    # 1) Markdown del nivel superior y del portal.
    for rel in INCLUIR_TOP:
        origen = os.path.join(ROOT, rel)
        if not os.path.isfile(origen):
            print(f"  aviso: falta {rel}, se omite")
            continue
        destino = rel[:-3] + ".html"
        escribir(destino, render(leer(origen), destino))
        generados += 1

    # 2) Índice de clases, README de parte, clases y sus primos.
    escribir("classes/README.html",
             render(leer(os.path.join(ROOT, "classes", "README.md")), "classes/README.html"))
    generados += 1
    partes = partes_info()
    for p in partes:
        pdir = os.path.join(ROOT, "classes", p["slug"])
        rel = f'classes/{p["slug"]}/README.html'
        escribir(rel, render(leer(os.path.join(pdir, "README.md")), rel))
        generados += 1
        for cdir in sorted(glob.glob(os.path.join(pdir, "[0-9][0-9][0-9]-*"))):
            base = os.path.basename(cdir)
            for nombre in ("README", "primos"):
                origen = os.path.join(cdir, nombre + ".md")
                if os.path.isfile(origen):
                    rel = f'classes/{p["slug"]}/{base}/{nombre}.html'
                    escribir(rel, render(leer(origen), rel))
                    generados += 1

    # 3) Datos y páginas interactivas que se copian tal cual.
    copias = [
        ("classes/_manifest.json", "classes/_manifest.json"),
        ("autoevaluaciones/preguntas.json", "autoevaluaciones/preguntas.json"),
        ("autoevaluaciones/quiz.html", "autoevaluaciones/quiz.html"),
        ("autoevaluaciones/progreso.html", "autoevaluaciones/progreso.html"),
        ("manual/MANUAL.pdf", "manual/MANUAL.pdf"),
        ("languages.json", "languages.json"),
    ]
    for origen_rel, destino_rel in copias:
        origen = os.path.join(ROOT, origen_rel)
        if not os.path.isfile(origen):
            print(f"  aviso: falta {origen_rel}, se omite")
            continue
        destino = os.path.join(OUT, destino_rel)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        shutil.copy2(origen, destino)

    # 4) Buscador y portada.
    n_indexadas = escribir_buscador(partes)

    n_primos = sum(len(re.findall(r"^```[a-z+#]", leer(f), re.M))
                   for f in glob.glob(os.path.join(ROOT, "classes", "parte-*",
                                                   "[0-9][0-9][0-9]-*", "primos.md")))
    glosario = os.path.join(ROOT, "glosario", "README.md")
    n_terminos = len(re.findall(r"^- \*\*", leer(glosario), re.M)) if os.path.isfile(glosario) else 0
    preguntas = os.path.join(ROOT, "autoevaluaciones", "preguntas.json")
    n_preguntas = 0
    if os.path.isfile(preguntas):
        d = json.loads(leer(preguntas))
        n_preguntas = sum(len(p["preguntas"]) for p in d["partes"])

    escribir_landing(partes, n_primos, n_terminos, n_preguntas)

    # GitHub Pages con Jekyll ignora lo que empieza por guion bajo (_manifest.json).
    escribir(".nojekyll", "")

    print(f"Sitio generado en site/ ({generados} páginas HTML + portada + buscador)")
    print(f"  {len(partes)} partes · {n_indexadas} clases indexadas · {n_primos} programas primos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
