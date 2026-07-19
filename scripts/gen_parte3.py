"""Generador de las clases de CÓDIGO de la Parte 3 (Valores, tipos y variables).

Cada clase define su contrato (casos.json), sus 10 implementaciones del núcleo
y el contenido del README/fichas. Reutiliza los patrones de E/S ya verificados
en la clase 041. Ejecuta:

    python scripts/gen_parte3.py          # genera las clases definidas aquí
    python scripts/verificar_equivalencia.py 042   # verifica una

Idempotente: sobrescribe los archivos de las clases que define.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import nav_footer, LANG_META  # noqa: E402
from curriculo import NUCLEO, BIBLIO, LIBROS_NUCLEO, PARTES  # noqa: E402

# Lenguaje para el resaltado del bloque de código embebido.
FENCE = {
    "python": "python", "javascript": "javascript", "typescript": "typescript",
    "java": "java", "csharp": "csharp", "go": "go", "rust": "rust",
    "c": "c", "sql": "sql", "php": "php",
}


def codigo_a_la_vista(spec):
    """Embebe el código de cada lenguaje del núcleo dentro de la clase (a la vista)."""
    bloques = []
    for l in NUCLEO:
        code = spec["impls"].get(l)
        if not code:
            continue
        nombre, _archivo, run = LANG_META[l]
        bloques.append(
            f"### {nombre} · `{run}`\n\n```{FENCE[l]}\n{code.rstrip()}\n```"
        )
    return "\n\n".join(bloques)


def refs_libros(idx, extra=None):
    """Fuentes: libros de la parte + libros de los lenguajes del núcleo."""
    lineas = ["**Libros de la parte:**", ""]
    lineas += [f"- {b}" for b in BIBLIO.get(idx, [])]
    lineas += ["", "**Libros de los lenguajes del núcleo:**", ""]
    lineas += [f"- {LIBROS_NUCLEO[l]}" for l in NUCLEO if l in LIBROS_NUCLEO]
    if extra:
        lineas += ["", *[f"- {e}" for e in extra]]
    return "\n".join(lineas)

ROOT = Path(__file__).resolve().parent.parent
CLASSES = ROOT / "classes"
MAN = json.loads((CLASSES / "_manifest.json").read_text(encoding="utf-8"))

# num -> (part_slug, class_slug, title, idx)
INFO = {}
for _p in MAN["parts"]:
    for _c in _p["classes"]:
        INFO[_c["num"]] = (_p["slug"], _c["slug"], _c["title"], _p["idx"])

CSPROJ = """<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>disable</ImplicitUsings>
    <Nullable>disable</Nullable>
    <AssemblyName>prog</AssemblyName>
  </PropertyGroup>

</Project>
"""


def bullets(items):
    return "\n".join(f"{i+1}. {x}" for i, x in enumerate(items))


def temas(items):
    return "\n".join(f"| {i+1} | {t} | {p} |" for i, (t, p) in enumerate(items))


def defs(items):
    return "\n".join(f"- **{t}** — {d}" for t, d in items)


def comp_rows(items):
    # Escapar '|' dentro de las celdas para no romper la tabla Markdown.
    esc = lambda x: x.replace("|", "\\|")
    return "\n".join(f"| {esc(a)} | {esc(b)} |" for a, b in items)


def errores(items):
    return "\n".join(f"- **{s}** → causa: {c} → solución: {so}" for s, c, so in items)


def faq(items):
    return "\n".join(f"- **{q}** {a}" for q, a in items)


def impl_table():
    rows = []
    for l in NUCLEO:
        nombre, archivo, run = LANG_META[l]
        rows.append(f"| {nombre} | `implementaciones/{l}/{archivo}` | `{run}` |")
    return "\n".join(rows)


def render_readme(num, spec):
    pslug, cslug, title, idx = INFO[num]
    casos_tabla = "\n".join(f"| `{c[0]}` | `{c[1]}` |" for c in spec["casos"])
    return f"""# Clase {num:03d} — {title}

> Parte **{idx} — {PARTES[idx][0]}** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

{spec['objetivo']}

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

{bullets(spec['resultados'])}

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
{temas(spec['temas'])}

## 📖 Definiciones y características

{defs(spec['definiciones'])}

## 🧩 Situación

{spec['situacion']}

## 🧮 Modelo

- **Entrada** (stdin): {spec['entrada']}
- **Salida** (stdout): {spec['salida']}
- **Regla:** {spec['formula']}

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
{casos_tabla}

## 📐 Algoritmo (pseudocódigo neutral)

```text
{spec['algoritmo']}
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

{codigo_a_la_vista(spec)}

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
{comp_rows(spec['comparacion'])}

## 🧬 El concepto en la familia

{spec['familia']}

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py {num:03d}
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

{errores(spec['errores'])}

## ❓ Preguntas frecuentes

{faq(spec['faq'])}

## 🔗 Referencias

{refs_libros(idx)}

---

> {nav_footer(num, idx)}
"""


def render_concepto(num, spec):
    _p, _c, title, _i = INFO[num]
    return f"""# Concepto — {title}

Conocimiento independiente del lenguaje.

{spec['objetivo']}

## Definiciones

{defs(spec['definiciones'])}

## Forma neutral

```text
{spec['algoritmo']}
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
"""


def render_comparacion(num, spec):
    _p, _c, title, _i = INFO[num]
    return f"""# Comparación — {title}

| Clase de diferencia | Observación entre lenguajes |
|---|---|
{comp_rows(spec['comparacion'])}

## El concepto en la familia

{spec['familia']}
"""


def render_reto(num, spec):
    _p, _c, title, _i = INFO[num]
    return f"""# Reto de transferencia — {title}

{spec['reto']}

## Criterio de aceptación

- ✅ La salida coincide exactamente con el formato del contrato.
- ✅ Se usa la forma idiomática del lenguaje elegido.
- ✅ Explicas en un comentario qué diferencia (sintáctica/semántica) observaste.
"""


def write_class(num, spec):
    pslug, cslug, title, idx = INFO[num]
    cdir = CLASSES / pslug / cslug
    cdir.mkdir(parents=True, exist_ok=True)
    (cdir / "README.md").write_text(render_readme(num, spec), encoding="utf-8")
    (cdir / "concepto.md").write_text(render_concepto(num, spec), encoding="utf-8")
    (cdir / "comparacion.md").write_text(render_comparacion(num, spec), encoding="utf-8")
    (cdir / "reto.md").write_text(render_reto(num, spec), encoding="utf-8")
    casos = {
        "descripcion": spec["descripcion"],
        "contrato": f"stdin: {spec['entrada']} → stdout: {spec['salida']}",
        "formula": spec["formula"],
        "casos": [{"stdin": s, "esperado": e} for s, e in spec["casos"]],
    }
    (cdir / "casos.json").write_text(json.dumps(casos, ensure_ascii=False, indent=2), encoding="utf-8")
    for lang, code in spec["impls"].items():
        nombre, archivo, _run = LANG_META[lang]
        ldir = cdir / "implementaciones" / lang
        ldir.mkdir(parents=True, exist_ok=True)
        (ldir / archivo).write_text(code, encoding="utf-8")
        if lang == "csharp":
            (ldir / "prog.csproj").write_text(CSPROJ, encoding="utf-8")


# --------------------------------------------------------------------------- #
# Definición de las clases 042–046
# --------------------------------------------------------------------------- #

SPECS = {}

# ---- 042 Declaración, asignación e inicialización (intercambio) ----
SPECS[42] = {
    "descripcion": "Intercambiar el valor de dos variables enteras. Es el ejemplo mínimo para estudiar declaración, asignación e inicialización.",
    "objetivo": "Distinguir tres actos que a menudo se confunden: **declarar** (introducir un nombre), **inicializar** (darle su primer valor) y **asignar** (cambiarlo después). El intercambio de dos variables los ejercita todos y revela cómo cada lenguaje los expresa (variable temporal vs. asignación múltiple).",
    "resultados": [
        "Diferenciar declaración, inicialización y (re)asignación.",
        "Intercambiar dos variables con y sin temporal según el lenguaje.",
        "Reconocer la asignación múltiple (desestructuración) donde existe.",
    ],
    "temas": [
        ("Declarar vs. inicializar", "Introducir un nombre no es lo mismo que darle valor"),
        ("Reasignación", "Cambiar el valor de una variable ya inicializada"),
        ("Variable temporal", "El patrón clásico para intercambiar"),
        ("Asignación múltiple", "a, b = b, a donde el lenguaje lo permite"),
    ],
    "definiciones": [
        ("Declaración", "introducir un nombre en un ámbito. Clave: en lenguajes estáticos fija el tipo."),
        ("Inicialización", "dar el primer valor a una variable. Clave: usarla sin inicializar es un error clásico."),
        ("Asignación", "cambiar el valor de una variable existente. Clave: solo posible si es mutable."),
        ("Asignación múltiple", "asignar varias variables a la vez (a, b = b, a). Clave: evita la temporal en Python, JS, Go, Rust."),
    ],
    "situacion": "Intercambiar dos valores parece trivial, pero es donde se ve si un lenguaje ofrece asignación múltiple (Python, Go, Rust, JS) o exige la variable temporal de toda la vida (C, Java).",
    "entrada": "una línea `a b` (dos enteros)",
    "salida": "`a=<nuevo a> b=<nuevo b>` tras intercambiar",
    "formula": "intercambiar a y b",
    "algoritmo": "LEER a, b\ntmp <- a ; a <- b ; b <- tmp   (o bien: a, b <- b, a)\nESCRIBIR \"a=\" a \" b=\" b",
    "casos": [("3 7", "a=7 b=3"), ("0 5", "a=5 b=0"), ("-2 9", "a=9 b=-2")],
    "comparacion": [
        ("Sintáctica", "`a, b = b, a` (Python/JS/Go/Rust) vs. `tmp=a;a=b;b=tmp;` (C/Java)."),
        ("Semántica", "La asignación múltiple evalúa el lado derecho antes de asignar; la temporal es manual."),
        ("Paradigmática", "SQL no reasigna variables: se describe la salida intercambiando columnas."),
    ],
    "familia": "En Ruby (scripting dinámico) es `a, b = b, a`, igual que Python. En Kotlin (JVM) se usa `also` o una temporal; en Haskell no hay reasignación: se define un nuevo valor.",
    "errores": [
        ("Perder un valor al intercambiar sin temporal", "asignar a=b antes de guardar a", "usar una temporal o la asignación múltiple del lenguaje"),
        ("Usar una variable sin inicializar", "declararla y no darle valor (C)", "inicializar siempre en la declaración"),
    ],
    "faq": [
        ("¿La asignación múltiple es más lenta?", "No de forma apreciable; es más legible y evita el error de la temporal."),
        ("¿Por qué C no la tiene?", "Es un lenguaje minimalista; el patrón con temporal es explícito y suficiente."),
    ],
    "reto": "Intercambia **tres** variables en ciclo (a←b, b←c, c←a) y resuélvelo en **Kotlin** (no explicado paso a paso), apoyándote en Java.",
    "impls": {
        "python": r"""import sys

# Declaración e inicialización a partir de la entrada.
a, b = sys.stdin.readline().split()
a, b = int(a), int(b)

# Asignación múltiple: intercambio sin variable temporal.
a, b = b, a

print(f"a={a} b={b}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

let [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);

// Desestructuración: intercambio en una sola línea.
[a, b] = [b, a];

console.log(`a=${a} b=${b}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

let [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);

[a, b] = [b, a];

console.log(`a=${a} b=${b}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]);
        int b = Integer.parseInt(p[1]);

        // Java no tiene asignación múltiple: variable temporal.
        int tmp = a;
        a = b;
        b = tmp;

        System.out.println("a=" + a + " b=" + b);
    }
}
""",
        "csharp": r"""using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);

// C# sí ofrece asignación por tuplas.
(a, b) = (b, a);

Console.WriteLine($"a={a} b={b}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])

	// Go permite intercambio con asignación múltiple.
	a, b = b, a

	fmt.Printf("a=%d b=%d\n", a, b)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();

    // Intercambio por desestructuración de tupla.
    let (a, b) = (v[1], v[0]);

    println!("a={a} b={b}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;

    /* C exige una variable temporal para intercambiar. */
    long tmp = a;
    a = b;
    b = tmp;

    printf("a=%ld b=%ld\n", a, b);
    return 0;
}
""",
        "php": r"""<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;

// PHP admite intercambio por lista.
[$a, $b] = [$b, $a];

printf("a=%d b=%d\n", $a, $b);
""",
        "sql": r"""-- SQL no reasigna variables: se describe la salida intercambiando columnas.
WITH pares(a, b) AS (VALUES (3, 7), (0, 5), (-2, 9))
SELECT printf('a=%d b=%d', b, a) AS resultado
FROM pares;
""",
    },
}

# ---- 043 Tipos primitivos: enteros, reales, booleanos ----
SPECS[43] = {
    "descripcion": "A partir de un entero, mostrar su valor como entero, como real y una propiedad booleana (si es par).",
    "objetivo": "Ver los tipos primitivos en acción: el mismo número tratado como **entero**, convertido a **real** y evaluado como **booleano**. Cada lenguaje formatea y convierte de forma propia, pero el concepto de 'tipo primitivo' es universal.",
    "resultados": [
        "Distinguir entero, real y booleano como tipos primitivos.",
        "Convertir un entero a real y formatearlo con decimales.",
        "Producir un valor booleano a partir de una condición.",
    ],
    "temas": [
        ("Entero", "Número sin parte fraccionaria"),
        ("Real (punto flotante)", "Número con decimales; se formatea explícitamente"),
        ("Booleano", "Verdadero o falso, resultado de una condición"),
        ("Formato de salida", "true/false y decimales difieren entre lenguajes"),
    ],
    "definiciones": [
        ("Tipo primitivo", "tipo básico incorporado al lenguaje (entero, real, booleano, carácter). Clave: bloque elemental de todo dato."),
        ("Entero", "número sin decimales, de tamaño fijo en los estáticos. Clave: aritmética exacta."),
        ("Real", "número en coma flotante. Clave: aproximado; se formatea con un número de decimales."),
        ("Booleano", "valor de verdad (verdadero/falso). Clave: gobierna las decisiones del programa."),
    ],
    "situacion": "Un mismo `4` puede verse como entero (`4`), como real (`4.0`) o dar lugar a un booleano (`4 es par → true`). Reconocer que el valor es uno y los tipos son lentes distintas es clave.",
    "entrada": "una línea `n` (un entero)",
    "salida": "`entero=<n> real=<n con 1 decimal> par=<true|false>`",
    "formula": "real = (double) n ; par = (n módulo 2 == 0)",
    "algoritmo": "LEER n\nreal <- CONVERTIR_A_REAL(n)\npar <- (n MOD 2 == 0)\nESCRIBIR \"entero=\" n \" real=\" FORMATEAR(real,1) \" par=\" par",
    "casos": [("4", "entero=4 real=4.0 par=true"), ("7", "entero=7 real=7.0 par=false"), ("0", "entero=0 real=0.0 par=true")],
    "comparacion": [
        ("Sintáctica", "El formato de real (`%.1f`, `toFixed(1)`, `F1`) y de booleano varían."),
        ("Semántica", "C#/Go escriben `True`/`true` distinto: hay que forzar minúsculas para igualar."),
        ("Paradigmática", "SQL expresa el booleano con `CASE WHEN`, no con un tipo booleano nativo universal."),
    ],
    "familia": "En Ruby `4.to_f` da el real y `4.even?` el booleano. En Haskell los tipos son explícitos (`Int`, `Double`, `Bool`) y la conversión es una función (`fromIntegral`).",
    "errores": [
        ("Imprimir `True` con mayúscula", "el `ToString` de C# capitaliza los booleanos", "formatear el booleano a minúsculas manualmente"),
        ("Esperar `4` en vez de `4.0`", "olvidar el formato de real", "formatear con el número de decimales fijado por el contrato"),
    ],
    "faq": [
        ("¿`4` y `4.0` son el mismo valor?", "Matemáticamente sí; para el tipo del lenguaje, no: uno es entero y otro real."),
        ("¿Por qué C# escribe True/False?", "Su `bool.ToString()` capitaliza; por eso se formatea a minúsculas para el contrato."),
    ],
    "reto": "Añade una cuarta salida `caracter=<c>` con el carácter cuyo código es `n` (por ejemplo 65→'A') y resuélvelo en **Ruby**.",
    "impls": {
        "python": r"""import sys

n = int(sys.stdin.readline())
real = float(n)
par = "true" if n % 2 == 0 else "false"
print(f"entero={n} real={real:.1f} par={par}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const par = n % 2 === 0 ? "true" : "false";
console.log(`entero=${n} real=${n.toFixed(1)} par=${par}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const par: string = n % 2 === 0 ? "true" : "false";
console.log(`entero=${n} real=${n.toFixed(1)} par=${par}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Locale;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        String par = (n % 2 == 0) ? "true" : "false";
        System.out.printf(Locale.US, "entero=%d real=%.1f par=%s%n", n, (double) n, par);
    }
}
""",
        "csharp": r"""using System;
using System.Globalization;

var inv = CultureInfo.InvariantCulture;
int n = int.Parse(Console.In.ReadToEnd().Trim(), inv);
string par = (n % 2 == 0) ? "true" : "false";
Console.WriteLine($"entero={n} real={((double)n).ToString("F1", inv)} par={par}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	par := "false"
	if n%2 == 0 {
		par = "true"
	}
	fmt.Printf("entero=%d real=%.1f par=%s\n", n, float64(n), par)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let par = if n % 2 == 0 { "true" } else { "false" };
    println!("entero={n} real={:.1} par={par}", n as f64);
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    const char *par = (n % 2 == 0) ? "true" : "false";
    printf("entero=%ld real=%.1f par=%s\n", n, (double) n, par);
    return 0;
}
""",
        "php": r"""<?php
$n = (int) trim(fgets(STDIN));
$par = ($n % 2 === 0) ? "true" : "false";
printf("entero=%d real=%.1f par=%s\n", $n, (float) $n, $par);
""",
        "sql": r"""-- SQL no tiene un tipo booleano nativo universal: se usa CASE WHEN.
WITH nums(n) AS (VALUES (4), (7), (0))
SELECT printf('entero=%d real=%.1f par=%s', n, n,
       CASE WHEN n % 2 = 0 THEN 'true' ELSE 'false' END) AS resultado
FROM nums;
""",
    },
}

# ---- 044 Enteros: bases ----
SPECS[44] = {
    "descripcion": "Mostrar un entero no negativo en cuatro bases: decimal, hexadecimal, octal y binario.",
    "objetivo": "Entender que un entero es un valor único que puede **representarse** en varias bases. La conversión revela diferencias reales: casi todos tienen formateo de hex/octal/binario, pero **C carece de especificador para binario** (hay que construirlo) y SQL solo formatea hex.",
    "resultados": [
        "Representar un mismo entero en decimal, hexadecimal, octal y binario.",
        "Usar el formateo de bases de cada lenguaje.",
        "Explicar por qué C no tiene `%b` y cómo se resuelve.",
    ],
    "temas": [
        ("Valor vs. representación", "El número es uno; las bases son formas de escribirlo"),
        ("Hex, octal, binario", "Bases 16, 8 y 2, comunes en programación"),
        ("Formateo por lenguaje", "Especificadores y funciones de conversión"),
        ("El hueco de C", "No hay `%b`: el binario se construye a mano"),
    ],
    "definiciones": [
        ("Base numérica", "sistema para escribir un número (10, 16, 8, 2). Clave: cambia la representación, no el valor."),
        ("Hexadecimal", "base 16 (0-9, a-f). Clave: compacta y común en memoria/colores."),
        ("Octal", "base 8. Clave: usada en permisos de archivos Unix."),
        ("Binario", "base 2 (0 y 1). Clave: la representación real en la máquina."),
    ],
    "situacion": "El color `#ff0000` es rojo: `ff` es 255 en hexadecimal. Convertir entre bases es cotidiano en programación de bajo nivel, gráficos y permisos. Cada lenguaje lo formatea a su manera, y C obliga a construir el binario.",
    "entrada": "una línea `n` (entero no negativo)",
    "salida": "`dec=<n> hex=<hex minúscula> oct=<octal> bin=<binario>`",
    "formula": "misma n en base 10, 16, 8 y 2 (sin prefijos ni ceros a la izquierda)",
    "algoritmo": "LEER n\nESCRIBIR \"dec=\" n \" hex=\" BASE(n,16) \" oct=\" BASE(n,8) \" bin=\" BASE(n,2)",
    "casos": [("255", "dec=255 hex=ff oct=377 bin=11111111"), ("10", "dec=10 hex=a oct=12 bin=1010"), ("1", "dec=1 hex=1 oct=1 bin=1")],
    "comparacion": [
        ("Sintáctica", "`f\"{n:x}\"` (Python), `n.toString(16)` (JS), `%x/%o/%b` (Go/Rust)."),
        ("Semántica", "C **no** tiene `%b`: el binario se genera con un bucle sobre los bits."),
        ("Paradigmática", "SQL (sqlite) solo formatea hex con `%x`; octal y binario no son nativos."),
    ],
    "familia": "En Ruby: `n.to_s(16)`, `to_s(8)`, `to_s(2)`. En C++ se usa `std::hex`/`std::oct` con streams, pero el binario también requiere ayuda (`std::bitset`).",
    "errores": [
        ("Buscar `%b` en C", "asumir que existe como en Go/Rust", "construir el binario con un bucle de desplazamientos"),
        ("Obtener hex en mayúscula", "usar `%X` en vez de `%x`", "elegir el especificador de minúsculas que pide el contrato"),
    ],
    "faq": [
        ("¿Por qué C no tiene binario en printf?", "El estándar nunca lo incluyó; hex y octal sí. Se implementa a mano fácilmente."),
        ("¿El valor cambia entre bases?", "No: `255`, `ff`, `377` y `11111111` son el mismo número escrito distinto."),
    ],
    "reto": "Añade la base 36 (`base36=<...>`) a la salida y resuélvelo en **Kotlin** (`Integer.toString(n, 36)`).",
    "impls": {
        "python": r"""import sys

n = int(sys.stdin.readline())
print(f"dec={n} hex={n:x} oct={n:o} bin={n:b}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`dec=${n} hex=${n.toString(16)} oct=${n.toString(8)} bin=${n.toString(2)}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`dec=${n} hex=${n.toString(16)} oct=${n.toString(8)} bin=${n.toString(2)}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        System.out.printf("dec=%d hex=%s oct=%s bin=%s%n", n,
                Integer.toHexString(n), Integer.toOctalString(n), Integer.toBinaryString(n));
    }
}
""",
        "csharp": r"""using System;
using System.Globalization;

int n = int.Parse(Console.In.ReadToEnd().Trim(), CultureInfo.InvariantCulture);
Console.WriteLine($"dec={n} hex={Convert.ToString(n, 16)} oct={Convert.ToString(n, 8)} bin={Convert.ToString(n, 2)}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	fmt.Printf("dec=%d hex=%x oct=%o bin=%b\n", n, n, n, n)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: u64 = s.trim().parse().unwrap();
    println!("dec={n} hex={:x} oct={:o} bin={:b}", n, n, n);
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    unsigned long n;
    if (scanf("%lu", &n) != 1) return 1;

    /* C no tiene especificador para binario: se construye a mano. */
    char bin[65];
    int i = 0;
    if (n == 0) {
        bin[i++] = '0';
    } else {
        char tmp[65];
        int j = 0;
        unsigned long t = n;
        while (t > 0) {
            tmp[j++] = (char) ('0' + (t & 1UL));
            t >>= 1;
        }
        while (j > 0) {
            bin[i++] = tmp[--j];
        }
    }
    bin[i] = '\0';

    printf("dec=%lu hex=%lx oct=%lo bin=%s\n", n, n, n, bin);
    return 0;
}
""",
        "php": r"""<?php
$n = (int) trim(fgets(STDIN));
printf("dec=%d hex=%s oct=%s bin=%s\n", $n, dechex($n), decoct($n), decbin($n));
""",
        "sql": r"""-- SQL (sqlite) solo formatea hexadecimal con %x; octal y binario no son nativos.
WITH nums(n) AS (VALUES (255), (10), (1))
SELECT printf('dec=%d hex=%x', n, n) AS resultado
FROM nums;
""",
    },
}

# ---- 045 Números reales: precisión y decimales ----
SPECS[45] = {
    "descripcion": "Sumar y multiplicar dos números reales y mostrar ambos resultados con dos decimales.",
    "objetivo": "Trabajar con números de punto flotante y su formateo. El foco: los reales son **aproximados** (`0.1 + 0.2` no es exactamente `0.3`), y por eso casi siempre se muestran con un número fijo de decimales usando un formato que fuerza la cultura (punto, no coma).",
    "resultados": [
        "Operar con reales (suma y producto).",
        "Formatear un real con un número fijo de decimales.",
        "Explicar por qué el punto flotante es aproximado.",
    ],
    "temas": [
        ("Punto flotante", "Representación aproximada de los reales"),
        ("Formateo con decimales", "Mostrar 2 decimales de forma consistente"),
        ("Cultura/locale", "Punto vs. coma decimal según el sistema"),
        ("Redondeo", "El formateo redondea; cuidado con los empates"),
    ],
    "definiciones": [
        ("Punto flotante", "representación binaria aproximada de números reales (IEEE 754). Clave: no todos los decimales son exactos."),
        ("Precisión", "cuántos dígitos significativos conserva un real. Clave: limitada; genera pequeños errores."),
        ("Formateo", "convertir el real a texto con N decimales. Clave: cómo se presenta el resultado."),
        ("Cultura invariante", "formato que usa el punto decimal sin importar el idioma del sistema. Clave: evita la coma decimal."),
    ],
    "situacion": "`0.1 + 0.2` da `0.30000000000000004` en casi todos los lenguajes. No es un bug: es cómo el hardware representa los reales. Por eso el dinero y los resultados se muestran con decimales fijos y formato controlado.",
    "entrada": "una línea `a b` (dos reales)",
    "salida": "`suma=<a+b con 2 decimales> producto=<a*b con 2 decimales>`",
    "formula": "suma = a + b ; producto = a * b (ambos a 2 decimales)",
    "algoritmo": "LEER a, b\nESCRIBIR \"suma=\" FORMATEAR(a+b,2) \" producto=\" FORMATEAR(a*b,2)",
    "casos": [("1.5 2.5", "suma=4.00 producto=3.75"), ("0.1 0.2", "suma=0.30 producto=0.02"), ("10 3", "suma=13.00 producto=30.00")],
    "comparacion": [
        ("Sintáctica", "`%.2f` (Python/C/Go), `toFixed(2)` (JS), `F2` (C#), `{:.2}` (Rust)."),
        ("Semántica", "El locale puede imprimir coma; se fuerza el punto (Locale.US, InvariantCulture)."),
        ("Paradigmática", "SQL formatea con `printf('%.2f', ...)` dentro de la consulta."),
    ],
    "familia": "En Ruby: `format('%.2f', x)`. En Haskell: `printf \"%.2f\" x` (de Text.Printf). El problema del punto flotante es idéntico en toda la familia porque todos usan IEEE 754.",
    "errores": [
        ("Ver `4,00` en vez de `4.00`", "el locale usa coma decimal", "forzar cultura invariante (Locale.US / InvariantCulture)"),
        ("Comparar reales con `==`", "esperar igualdad exacta", "comparar con una tolerancia, o formatear antes de comparar"),
    ],
    "faq": [
        ("¿Por qué 0.1+0.2 no es 0.3?", "0.1 y 0.2 no tienen representación binaria exacta; el error se arrastra a la suma."),
        ("¿Cómo manejo dinero entonces?", "Con decimales fijos y formateo, o con tipos decimales exactos donde el lenguaje los ofrezca."),
    ],
    "reto": "Añade `promedio=<(a+b)/2 con 2 decimales>` y resuélvelo en **Kotlin** con `String.format`.",
    "impls": {
        "python": r"""import sys

a, b = map(float, sys.stdin.readline().split())
print(f"suma={a + b:.2f} producto={a * b:.2f}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${(a + b).toFixed(2)} producto=${(a * b).toFixed(2)}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${(a + b).toFixed(2)} producto=${(a * b).toFixed(2)}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Locale;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        double a = Double.parseDouble(p[0]);
        double b = Double.parseDouble(p[1]);
        System.out.printf(Locale.US, "suma=%.2f producto=%.2f%n", a + b, a * b);
    }
}
""",
        "csharp": r"""using System;
using System.Globalization;

var inv = CultureInfo.InvariantCulture;
string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
double a = double.Parse(p[0], inv);
double b = double.Parse(p[1], inv);
Console.WriteLine($"suma={(a + b).ToString("F2", inv)} producto={(a * b).ToString("F2", inv)}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	a, _ := strconv.ParseFloat(f[0], 64)
	b, _ := strconv.ParseFloat(f[1], 64)
	fmt.Printf("suma=%.2f producto=%.2f\n", a+b, a*b)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<f64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("suma={:.2} producto={:.2}", v[0] + v[1], v[0] * v[1]);
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    double a, b;
    if (scanf("%lf %lf", &a, &b) != 2) return 1;
    printf("suma=%.2f producto=%.2f\n", a + b, a * b);
    return 0;
}
""",
        "php": r"""<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (float) $a;
$b = (float) $b;
printf("suma=%.2f producto=%.2f\n", $a + $b, $a * $b);
""",
        "sql": r"""-- SQL formatea reales con printf dentro de la consulta.
WITH pares(a, b) AS (VALUES (1.5, 2.5), (0.1, 0.2), (10, 3))
SELECT printf('suma=%.2f producto=%.2f', a + b, a * b) AS resultado
FROM pares;
""",
    },
}

# ---- 046 Booleanos y valores de verdad ----
SPECS[46] = {
    "descripcion": "Dadas dos entradas booleanas (0 o 1), calcular su AND, su OR y la negación de la primera.",
    "objetivo": "Dominar el álgebra booleana básica: **AND** (ambos), **OR** (alguno) y **NOT** (negación). Es la base de toda condición y decisión. Cada lenguaje representa e imprime los booleanos de forma propia (`true`/`True`), lo que obliga a normalizar la salida.",
    "resultados": [
        "Calcular AND, OR y NOT sobre valores booleanos.",
        "Construir un booleano a partir de una entrada (0/1).",
        "Normalizar la impresión de booleanos entre lenguajes.",
    ],
    "temas": [
        ("AND, OR, NOT", "Las tres operaciones lógicas fundamentales"),
        ("Representar la verdad", "0/1, true/false, según el lenguaje"),
        ("Impresión de booleanos", "true vs. True: hay que normalizar"),
        ("Base de las condiciones", "Todo if depende de un booleano"),
    ],
    "definiciones": [
        ("Booleano", "valor de verdad: verdadero o falso. Clave: resultado de comparaciones y condiciones."),
        ("AND (∧)", "verdadero solo si ambos lo son. Clave: conjunción."),
        ("OR (∨)", "verdadero si al menos uno lo es. Clave: disyunción."),
        ("NOT (¬)", "invierte el valor de verdad. Clave: negación."),
    ],
    "situacion": "\"Si es fin de semana Y no llueve, salgo\": toda decisión combina booleanos con AND/OR/NOT. Verlos aislados, con su tabla de verdad, prepara para las condiciones de la Parte 4.",
    "entrada": "una línea `a b` (cada uno 0 o 1)",
    "salida": "`and=<true|false> or=<true|false> not_a=<true|false>`",
    "formula": "and = a ∧ b ; or = a ∨ b ; not_a = ¬a (con a,b interpretados como booleanos)",
    "algoritmo": "LEER a, b\nba <- (a != 0) ; bb <- (b != 0)\nESCRIBIR \"and=\" (ba Y bb) \" or=\" (ba O bb) \" not_a=\" (NO ba)",
    "casos": [("1 0", "and=false or=true not_a=false"), ("1 1", "and=true or=true not_a=false"), ("0 0", "and=false or=false not_a=true")],
    "comparacion": [
        ("Sintáctica", "`and/or/not` (Python) vs. `&&/||/!` (C/Java/JS/Go/Rust/PHP)."),
        ("Semántica", "C# imprime `True`/`False`; C no tiene tipo bool nativo hasta C99; se normaliza a minúsculas."),
        ("Paradigmática", "SQL usa `CASE WHEN a<>0 AND b<>0 ...` en vez de un tipo booleano nativo."),
    ],
    "familia": "En Ruby `a && b`, y `true`/`false` en minúscula por defecto. En Haskell son `&&`, `||`, `not`, con el tipo `Bool` explícito y valores `True`/`False`.",
    "errores": [
        ("Imprimir `True`/`False`", "usar el formato por defecto de C#/Python", "normalizar a minúsculas con un ayudante `tf`"),
        ("Confundir cortocircuito con bit a bit", "usar `&`/`|` en vez de `&&`/`||`", "usar los operadores lógicos, no los de bits"),
    ],
    "faq": [
        ("¿`&&` y `&` son lo mismo?", "No: `&&` es lógico con cortocircuito; `&` es bit a bit. Para booleanos, usa `&&`."),
        ("¿Qué es el cortocircuito?", "En `a && b`, si `a` es falso no se evalúa `b`. Importa cuando `b` tiene efectos."),
    ],
    "reto": "Añade `xor=<...>` (verdadero si son distintos) y resuélvelo en **Go** usando `!=` sobre booleanos.",
    "impls": {
        "python": r"""import sys

a, b = map(int, sys.stdin.readline().split())
ba, bb = a != 0, b != 0
tf = lambda x: "true" if x else "false"
print(f"and={tf(ba and bb)} or={tf(ba or bb)} not_a={tf(not ba)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const [ai, bi] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const a = ai !== 0;
const b = bi !== 0;
const tf = (x) => (x ? "true" : "false");
console.log(`and=${tf(a && b)} or=${tf(a || b)} not_a=${tf(!a)}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const [ai, bi]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const a: boolean = ai !== 0;
const b: boolean = bi !== 0;
const tf = (x: boolean): string => (x ? "true" : "false");
console.log(`and=${tf(a && b)} or=${tf(a || b)} not_a=${tf(!a)}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static String tf(boolean x) {
        return x ? "true" : "false";
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        boolean a = Integer.parseInt(p[0]) != 0;
        boolean b = Integer.parseInt(p[1]) != 0;
        System.out.printf("and=%s or=%s not_a=%s%n", tf(a && b), tf(a || b), tf(!a));
    }
}
""",
        "csharp": r"""using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
bool a = int.Parse(p[0]) != 0;
bool b = int.Parse(p[1]) != 0;
string Tf(bool x) => x ? "true" : "false";
Console.WriteLine($"and={Tf(a && b)} or={Tf(a || b)} not_a={Tf(!a)}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func tf(x bool) string {
	if x {
		return "true"
	}
	return "false"
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	ai, _ := strconv.Atoi(f[0])
	bi, _ := strconv.Atoi(f[1])
	a, b := ai != 0, bi != 0
	fmt.Printf("and=%s or=%s not_a=%s\n", tf(a && b), tf(a || b), tf(!a))
}
""",
        "rust": r"""use std::io::Read;

fn tf(x: bool) -> &'static str {
    if x { "true" } else { "false" }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let (a, b) = (v[0] != 0, v[1] != 0);
    println!("and={} or={} not_a={}", tf(a && b), tf(a || b), tf(!a));
}
""",
        "c": r"""#include <stdio.h>

static const char *tf(int x) {
    return x ? "true" : "false";
}

int main(void) {
    int a, b;
    if (scanf("%d %d", &a, &b) != 2) return 1;
    a = a != 0;
    b = b != 0;
    printf("and=%s or=%s not_a=%s\n", tf(a && b), tf(a || b), tf(!a));
    return 0;
}
""",
        "php": r"""<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = ((int) $a) !== 0;
$b = ((int) $b) !== 0;
$tf = fn($x) => $x ? "true" : "false";
printf("and=%s or=%s not_a=%s\n", $tf($a && $b), $tf($a || $b), $tf(!$a));
""",
        "sql": r"""-- SQL no tiene tipo booleano nativo: se expresa con CASE WHEN.
WITH pares(a, b) AS (VALUES (1, 0), (1, 1), (0, 0))
SELECT printf('and=%s or=%s not_a=%s',
       CASE WHEN a <> 0 AND b <> 0 THEN 'true' ELSE 'false' END,
       CASE WHEN a <> 0 OR b <> 0 THEN 'true' ELSE 'false' END,
       CASE WHEN NOT (a <> 0) THEN 'true' ELSE 'false' END) AS resultado
FROM pares;
""",
    },
}


def main():
    for num, spec in SPECS.items():
        write_class(num, spec)
        print(f"Clase {num:03d} generada.")


if __name__ == "__main__":
    main()
