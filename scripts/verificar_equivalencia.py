"""Verificador de equivalencia políglota.

Dado el número o slug de una clase, ejecuta cada implementación del núcleo
alimentando los casos de `casos.json` por stdin y comprueba que todas producen
la misma salida esperada. Los lenguajes cuyo toolchain no esté instalado se
omiten (degradación silenciosa), y se informa qué se verificó y qué no.

Uso:
    python scripts/verificar_equivalencia.py 041
    python scripts/verificar_equivalencia.py 041-literales-valores-variables-y-constantes
    python scripts/verificar_equivalencia.py --all
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
CLASSES = ROOT / "classes"
EXE = ".exe" if os.name == "nt" else ""


def resolve(cmd):
    """Resuelve el ejecutable a su ruta completa (necesario en Windows para .cmd/.bat)."""
    cmd = list(cmd)
    head = cmd[0]
    if os.sep not in head and (os.altsep is None or os.altsep not in head):
        cmd[0] = shutil.which(head) or head
    return cmd


def run(cmd, cwd, stdin, timeout=120):
    return subprocess.run(resolve(cmd), cwd=cwd, input=stdin, capture_output=True,
                          text=True, timeout=timeout)


# Cada lenguaje: binario requerido, (opcional) paso de compilación, y ejecución.
def lang_runner(lang, impl_dir):
    """Devuelve (tool, compilar_fn|None, ejecutar_cmd) o None si no aplica."""
    tsx = shutil.which("tsx") or shutil.which("npx")
    specs = {
        "python":     ("python", None, [sys.executable or "python", "main.py"]),
        "javascript": ("node", None, ["node", "main.mjs"]),
        "typescript": ("npx", None, ["npx", "--yes", "tsx", "main.ts"]),
        "java":       ("java", None, ["java", "Main.java"]),
        "csharp":     ("dotnet", None, ["dotnet", "run", "-v", "q", "--nologo"]),
        "go":         ("go", None, ["go", "run", "main.go"]),
        "rust":       ("rustc", ["rustc", "main.rs", "-o", f"_bin{EXE}"], [f".{os.sep}_bin{EXE}"]),
        "c":          (shutil.which("cc") and "cc" or "gcc",
                       [shutil.which("cc") and "cc" or "gcc", "main.c", "-o", f"_bin{EXE}"],
                       [f".{os.sep}_bin{EXE}"]),
        "php":        ("php", None, ["php", "main.php"]),
    }
    return specs.get(lang)


def verificar_clase(cdir: Path) -> tuple[int, int, list[str]]:
    casos_path = cdir / "casos.json"
    if not casos_path.exists():
        return (0, 0, [f"  (sin casos.json — clase en construcción)"])
    data = json.loads(casos_path.read_text(encoding="utf-8"))
    casos = data.get("casos", [])
    impl_root = cdir / "implementaciones"
    lineas = []
    ok = 0
    fail = 0

    for lang in ["python", "javascript", "typescript", "java", "csharp",
                 "go", "rust", "c", "php"]:
        impl_dir = impl_root / lang
        if not impl_dir.is_dir() or not any(impl_dir.iterdir()):
            continue
        spec = lang_runner(lang, impl_dir)
        if spec is None:
            continue
        tool, compilar, ejecutar = spec
        if not tool or not shutil.which(tool):
            lineas.append(f"  ⏭️  {lang:<11} omitido (toolchain '{tool}' no disponible)")
            continue
        try:
            if compilar:
                c = run(compilar, impl_dir, None)
                if c.returncode != 0:
                    fail += 1
                    lineas.append(f"  ❌ {lang:<11} no compila: {c.stderr.strip()[:120]}")
                    continue
            todos_ok = True
            detalle = ""
            for caso in casos:
                r = run(ejecutar, impl_dir, caso["stdin"] + "\n")
                # El contrato define la salida como la última línea no vacía
                # (tolera warnings de arranque del runtime local).
                salida = [ln for ln in r.stdout.splitlines() if ln.strip()]
                got = salida[-1].strip() if salida else ""
                esperado = caso["esperado"].strip()
                if got != esperado:
                    todos_ok = False
                    detalle = f" (esperaba '{esperado}', obtuvo '{got}')"
                    break
            if todos_ok:
                ok += 1
                lineas.append(f"  ✅ {lang:<11} {len(casos)}/{len(casos)} casos")
            else:
                fail += 1
                lineas.append(f"  ❌ {lang:<11} falla{detalle}")
        except subprocess.TimeoutExpired:
            fail += 1
            lineas.append(f"  ❌ {lang:<11} timeout")
        finally:
            for res in (impl_dir / f"_bin{EXE}",):
                if res.exists():
                    res.unlink()

    # SQL: ilustrativa, no participa en la comparación por stdin.
    sql_dir = impl_root / "sql"
    if (sql_dir / "main.sql").exists():
        if shutil.which("sqlite3"):
            try:
                r = run(["sqlite3", ":memory:"], sql_dir,
                        (sql_dir / "main.sql").read_text(encoding="utf-8"))
                estado = "ejecuta" if r.returncode == 0 else "error"
                lineas.append(f"  ℹ️  {'sql':<11} ilustrativa ({estado}, declarativa, sin stdin)")
            except Exception:
                lineas.append(f"  ℹ️  {'sql':<11} ilustrativa (no verificada)")
        else:
            lineas.append(f"  ⏭️  {'sql':<11} omitido (sqlite3 no disponible)")

    return (ok, fail, lineas)


def find_class_dir(arg: str) -> Path | None:
    manifest = json.loads((CLASSES / "_manifest.json").read_text(encoding="utf-8"))
    num = None
    try:
        num = int(arg)
    except ValueError:
        pass
    for p in manifest["parts"]:
        for c in p["classes"]:
            if (num is not None and c["num"] == num) or c["slug"] == arg or c["slug"].endswith(arg):
                return CLASSES / p["slug"] / c["slug"]
    return None


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)

    if args[0] == "--all":
        manifest = json.loads((CLASSES / "_manifest.json").read_text(encoding="utf-8"))
        total_ok = total_fail = 0
        for p in manifest["parts"]:
            for c in p["classes"]:
                cdir = CLASSES / p["slug"] / c["slug"]
                if not (cdir / "casos.json").exists():
                    continue
                ok, fail, lineas = verificar_clase(cdir)
                total_ok += ok
                total_fail += fail
                if ok or fail:
                    print(f"\n📦 {c['num']:03d} {c['title']}")
                    print("\n".join(lineas))
        print(f"\n== Total: {total_ok} implementaciones OK, {total_fail} con fallo ==")
        sys.exit(1 if total_fail else 0)

    cdir = find_class_dir(args[0])
    if cdir is None or not cdir.exists():
        print(f"No encuentro la clase '{args[0]}'.")
        sys.exit(2)
    print(f"📦 Verificando: {cdir.name}\n")
    ok, fail, lineas = verificar_clase(cdir)
    print("\n".join(lineas))
    print(f"\n== {ok} implementaciones equivalentes, {fail} con fallo ==")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
