"""Parte 9 — Ingeniería de software políglota (clases 139-154)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_parte3 as g3  # noqa: E402

S = {}

S[139] = {
    "descripcion": "Ejecutar una prueba unitaria: verificar que a + b es igual al valor esperado.",
    "objetivo": "Escribir una **prueba unitaria**: código que comprueba automáticamente que otro código produce el resultado esperado. Es la base de la calidad y el corazón del verificador de este curso.",
    "resultados": ["Escribir una aserción.", "Distinguir prueba que pasa de la que falla.", "Reconocer el runner de cada lenguaje."],
    "temas": [("Prueba unitaria", "Verifica una unidad de código"), ("Aserción", "Comprobar el valor esperado"), ("Pasa/falla", "Verde o rojo")],
    "definiciones": [("Prueba unitaria", "código que verifica una unidad (función) de forma automática. Clave: repetible."), ("Aserción", "comprobación de que un valor es el esperado. Clave: si falla, la prueba se pone en rojo."), ("Runner", "herramienta que ejecuta las pruebas (pytest, cargo test). Clave: un comando corre todas.")],
    "situacion": "Antes de confiar en una función, se escribe una prueba: 'sumar(3,4) debe dar 7'. Si un cambio la rompe, la prueba lo detecta al instante.",
    "entrada": "una línea `a b esperado`",
    "salida": "`test=<pasa|falla>`",
    "formula": "pasa si a + b == esperado",
    "algoritmo": "LEER a, b, esperado ; SI a+b == esperado: pasa SINO falla",
    "casos": [("3 4 7", "test=pasa"), ("2 2 5", "test=falla"), ("10 5 15", "test=pasa")],
    "comparacion": [("Sintáctica", "assert (Python), expect (JS), assertEquals (Java)."), ("Semántica", "La aserción compara y decide el estado de la prueba."), ("Paradigmática", "SQL prueba con consultas de comprobación.")],
    "familia": "pytest (Python), JUnit (Java), cargo test (Rust), phpunit (PHP): mismo concepto.",
    "errores": [("No probar los casos límite", "bugs en los extremos", "incluir 0, vacío y negativos"), ("Pruebas frágiles", "fallan por cambios irrelevantes", "probar el comportamiento, no la implementación")],
    "faq": [("¿Cuántas pruebas?", "Al menos una por comportamiento y por caso límite."), ("¿casos.json es una prueba?", "Sí: compara la salida real con la esperada.")],
    "reto": "Añade una prueba para la resta y resuélvelo en **Python** con pytest.",
    "impls": {
        "python": r"""import sys

a, b, esperado = map(int, sys.stdin.readline().split())
print(f"test={'pasa' if a + b == esperado else 'falla'}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const [a, b, esperado] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`test=${a + b === esperado ? "pasa" : "falla"}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const [a, b, esperado] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`test=${a + b === esperado ? "pasa" : "falla"}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]), b = Integer.parseInt(p[1]), esperado = Integer.parseInt(p[2]);
        System.out.println("test=" + (a + b == esperado ? "pasa" : "falla"));
    }
}
""",
        "csharp": r"""using System;

int[] p = Array.ConvertAll(Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries), int.Parse);
Console.WriteLine($"test={(p[0] + p[1] == p[2] ? "pasa" : "falla")}");
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
	esperado, _ := strconv.Atoi(f[2])
	res := "falla"
	if a+b == esperado {
		res = "pasa"
	}
	fmt.Printf("test=%s\n", res)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let res = if v[0] + v[1] == v[2] { "pasa" } else { "falla" };
    println!("test={res}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long a, b, esperado;
    if (scanf("%ld %ld %ld", &a, &b, &esperado) != 3) return 1;
    printf("test=%s\n", a + b == esperado ? "pasa" : "falla");
    return 0;
}
""",
        "php": r"""<?php
[$a, $b, $esperado] = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "test=" . ($a + $b === $esperado ? "pasa" : "falla") . "\n";
""",
        "sql": r"""-- SQL: una consulta de comprobación.
WITH t(a, b, esperado) AS (VALUES (3, 4, 7))
SELECT printf('test=%s', CASE WHEN a + b = esperado THEN 'pasa' ELSE 'falla' END) AS resultado FROM t;
""",
    },
}

S[140] = {
    "descripcion": "Comprobar si dos resultados son equivalentes (prueba de integración/equivalencia).",
    "objetivo": "Entender las **pruebas de integración** y el **verificador de equivalencia**: en vez de una unidad aislada, se comprueba que dos partes (o dos implementaciones) producen el mismo resultado. Es exactamente lo que hace el CI de este curso.",
    "resultados": ["Comparar dos salidas.", "Explicar prueba de integración vs. unitaria.", "Relacionarlo con el verificador del curso."],
    "temas": [("Integración", "Varias partes juntas"), ("Equivalencia", "Mismos resultados"), ("Verificador", "Compara implementaciones")],
    "definiciones": [("Prueba de integración", "verifica que varias partes funcionan juntas. Clave: más allá de la unidad."), ("Equivalencia", "dos implementaciones dan el mismo resultado. Clave: base del verificador."), ("Regresión", "un cambio rompe algo que funcionaba. Clave: las pruebas la detectan.")],
    "situacion": "El verificador de este curso comprueba que las 10 implementaciones de una clase dan la misma salida. Aquí, en pequeño, se comparan dos resultados y se declara si son equivalentes.",
    "entrada": "una línea `x y` (dos resultados a comparar)",
    "salida": "`equivalente=<true|false>`",
    "formula": "equivalente si x == y",
    "algoritmo": "LEER x, y ; ESCRIBIR equivalente=(x==y)",
    "casos": [("6 6", "equivalente=true"), ("5 7", "equivalente=false"), ("0 0", "equivalente=true")],
    "comparacion": [("Sintáctica", "Comparación de igualdad en cada lenguaje."), ("Semántica", "Se compara la salida observable, no la implementación."), ("Paradigmática", "SQL compara con =.")],
    "familia": "El patrón 'mismas entradas → misma salida' es universal en pruebas de equivalencia.",
    "errores": [("Comparar implementaciones en vez de salidas", "acoplamiento a detalles", "comparar el resultado observable"), ("No fijar el formato", "diferencias espurias", "normalizar la salida antes de comparar")],
    "faq": [("¿Unitaria o integración?", "Unitaria prueba una función; integración, varias juntas."), ("¿Qué garantiza el verificador?", "Que las implementaciones son equivalentes, no que la prosa sea correcta.")],
    "reto": "Compara con una tolerancia para reales y resuélvelo en **Go**.",
    "impls": {
        "python": r"""import sys

x, y = sys.stdin.readline().split()
print(f"equivalente={'true' if x == y else 'false'}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const [x, y] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`equivalente=${x === y ? "true" : "false"}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const [x, y] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`equivalente=${x === y ? "true" : "false"}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        System.out.println("equivalente=" + (p[0].equals(p[1]) ? "true" : "false"));
    }
}
""",
        "csharp": r"""using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"equivalente={(p[0] == p[1] ? "true" : "false")}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	res := "false"
	if f[0] == f[1] {
		res = "true"
	}
	fmt.Printf("equivalente=%s\n", res)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<&str> = s.split_whitespace().collect();
    let res = if v[0] == v[1] { "true" } else { "false" };
    println!("equivalente={res}");
}
""",
        "c": r"""#include <stdio.h>
#include <string.h>

int main(void) {
    char x[64], y[64];
    if (scanf("%63s %63s", x, y) != 2) return 1;
    printf("equivalente=%s\n", strcmp(x, y) == 0 ? "true" : "false");
    return 0;
}
""",
        "php": r"""<?php
[$x, $y] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "equivalente=" . ($x === $y ? "true" : "false") . "\n";
""",
        "sql": r"""-- SQL: compara dos valores.
WITH t(x, y) AS (VALUES (6, 6))
SELECT printf('equivalente=%s', CASE WHEN x = y THEN 'true' ELSE 'false' END) AS resultado FROM t;
""",
    },
}

S[141] = {
    "descripcion": "Mostrar la traza de sumas acumuladas de 1 a n, como al avanzar paso a paso en un depurador.",
    "objetivo": "Usar la idea de un **depurador**: avanzar paso a paso viendo cómo evoluciona el estado. La traza de sumas acumuladas (1, 3, 6, …) muestra el valor del acumulador en cada paso, como haría un depurador.",
    "resultados": ["Producir una traza de estados.", "Explicar el avance paso a paso.", "Nombrar los depuradores por runtime."],
    "temas": [("Traza", "Estado en cada paso"), ("Paso a paso", "Avanzar controladamente"), ("Punto de ruptura", "Pausar para inspeccionar")],
    "definiciones": [("Depurador", "herramienta para pausar y avanzar viendo el estado (gdb, pdb). Clave: diagnóstico."), ("Traza", "secuencia de estados por los que pasa el programa. Clave: revela dónde se desvía."), ("Paso a paso (step)", "avanzar una instrucción a la vez. Clave: inspeccionar cada cambio.")],
    "situacion": "Cuando un resultado sorprende, se avanza paso a paso viendo el acumulador. La traza 1-3-6 muestra la suma acumulada tras cada elemento, como el panel de variables de un depurador.",
    "entrada": "un entero `n` (n >= 1)",
    "salida": "`traza=<sumas acumuladas 1..n unidas por ->`",
    "formula": "traza[i] = 1 + 2 + ... + i",
    "algoritmo": "acc <- 0 ; PARA i de 1 a n: acc <- acc+i ; emitir acc",
    "casos": [("3", "traza=1-3-6"), ("1", "traza=1"), ("4", "traza=1-3-6-10")],
    "comparacion": [("Sintáctica", "Bucle con acumulador en cada lenguaje."), ("Semántica", "La traza expone el estado intermedio."), ("Paradigmática", "SQL usa sumas acumuladas con funciones de ventana.")],
    "familia": "gdb/lldb, pdb, y los depuradores de la JVM/.NET y los IDE ofrecen este avance paso a paso.",
    "errores": [("Depurar sin observar el estado", "cambios al azar", "trazar el acumulador en cada paso"), ("Olvidar reiniciar el acumulador", "traza incorrecta", "empezar el acumulador en 0")],
    "faq": [("¿print o depurador?", "El depurador evita recompilar y permite avanzar paso a paso."), ("¿Qué es un watch?", "Una expresión que el depurador reevalúa en cada pausa.")],
    "reto": "Muestra también la traza de productos acumulados y resuélvelo en **Python**.",
    "impls": {
        "python": r"""import sys

n = int(sys.stdin.readline())
acc = 0
pasos = []
for i in range(1, n + 1):
    acc += i
    pasos.append(acc)
print("traza=" + "-".join(str(x) for x in pasos))
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let acc = 0;
const pasos = [];
for (let i = 1; i <= n; i++) {
  acc += i;
  pasos.push(acc);
}
console.log(`traza=${pasos.join("-")}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let acc = 0;
const pasos: number[] = [];
for (let i = 1; i <= n; i++) {
  acc += i;
  pasos.push(acc);
}
console.log(`traza=${pasos.join("-")}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        long acc = 0;
        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= n; i++) {
            acc += i;
            if (i > 1) sb.append("-");
            sb.append(acc);
        }
        System.out.println("traza=" + sb);
    }
}
""",
        "csharp": r"""using System;
using System.Text;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long acc = 0;
var sb = new StringBuilder();
for (int i = 1; i <= n; i++) {
    acc += i;
    if (i > 1) sb.Append("-");
    sb.Append(acc);
}
Console.WriteLine($"traza={sb}");
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
	acc := 0
	var pasos []string
	for i := 1; i <= n; i++ {
		acc += i
		pasos = append(pasos, strconv.Itoa(acc))
	}
	fmt.Printf("traza=%s\n", strings.Join(pasos, "-"))
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut acc = 0i64;
    let mut pasos: Vec<String> = Vec::new();
    for i in 1..=n {
        acc += i;
        pasos.push(acc.to_string());
    }
    println!("traza={}", pasos.join("-"));
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long acc = 0;
    printf("traza=");
    for (long i = 1; i <= n; i++) {
        acc += i;
        if (i > 1) printf("-");
        printf("%ld", acc);
    }
    printf("\n");
    return 0;
}
""",
        "php": r"""<?php
$n = (int) trim(fgets(STDIN));
$acc = 0;
$pasos = [];
for ($i = 1; $i <= $n; $i++) {
    $acc += $i;
    $pasos[] = $acc;
}
echo "traza=" . implode("-", $pasos) . "\n";
""",
        "sql": r"""-- SQL: sumas acumuladas con función de ventana (ilustrativo, n=3).
WITH RECURSIVE r(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM r WHERE i < 3)
SELECT 'traza=' || group_concat(s, '-') AS resultado
FROM (SELECT sum(i) OVER (ORDER BY i) AS s FROM r);
""",
    },
}

S[142] = {
    "descripcion": "Emitir un registro (log) informando cuántos elementos se procesaron.",
    "objetivo": "Practicar el **registro (logging) y la observabilidad**: dejar rastros de lo que hace el programa para poder diagnosticarlo en producción, donde no hay depurador. Un log con nivel y datos es la unidad básica.",
    "resultados": ["Emitir un registro con nivel.", "Explicar la observabilidad.", "Distinguir niveles de log."],
    "temas": [("Logging", "Dejar rastros de la ejecución"), ("Nivel", "INFO, WARN, ERROR"), ("Observabilidad", "Entender el sistema desde fuera")],
    "definiciones": [("Log", "mensaje que registra un evento del programa. Clave: diagnóstico en producción."), ("Nivel de log", "gravedad del mensaje (DEBUG, INFO, WARN, ERROR). Clave: filtrar el ruido."), ("Observabilidad", "capacidad de entender el estado interno desde las salidas (logs, métricas, trazas). Clave: operar en producción.")],
    "situacion": "En producción no puedes pausar el programa; te guías por los logs. Un registro estructurado ('[INFO] procesados=5') permite saber qué pasó sin estar delante.",
    "entrada": "un entero `n` (elementos procesados)",
    "salida": "`log=[INFO] procesados=<n>`",
    "formula": "emitir un registro de nivel INFO con el conteo",
    "algoritmo": "LEER n ; ESCRIBIR log de nivel INFO con procesados=n",
    "casos": [("5", "log=[INFO] procesados=5"), ("0", "log=[INFO] procesados=0"), ("3", "log=[INFO] procesados=3")],
    "comparacion": [("Sintáctica", "logging (Python), console/log4j (JS/Java), slog (Go)."), ("Semántica", "El nivel permite filtrar; el formato estructurado facilita el análisis."), ("Paradigmática", "SQL registra con tablas de auditoría.")],
    "familia": "log4j/SLF4J (Java), logging (Python), Serilog (.NET), zap/slog (Go): mismo concepto de niveles.",
    "errores": [("Loggear demasiado", "ruido que oculta lo importante", "usar niveles y registrar lo relevante"), ("Loggear datos sensibles", "fuga de información", "no registrar contraseñas ni datos personales")],
    "faq": [("¿Log o depurador?", "El depurador para desarrollo; el log para producción."), ("¿Qué es observabilidad?", "Logs, métricas y trazas que permiten entender el sistema en marcha.")],
    "reto": "Añade un nivel WARN si n es 0 y resuélvelo en **Go** con slog.",
    "impls": {
        "python": r"""import sys

n = int(sys.stdin.readline())
print(f"log=[INFO] procesados={n}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`log=[INFO] procesados=${n}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`log=[INFO] procesados=${n}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        System.out.println("log=[INFO] procesados=" + n);
    }
}
""",
        "csharp": r"""using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"log=[INFO] procesados={n}");
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
	fmt.Printf("log=[INFO] procesados=%d\n", n)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("log=[INFO] procesados={n}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("log=[INFO] procesados=%ld\n", n);
    return 0;
}
""",
        "php": r"""<?php
$n = (int) trim(fgets(STDIN));
echo "log=[INFO] procesados=$n\n";
""",
        "sql": r"""-- SQL: registro con una tabla/consulta de auditoría.
WITH t(n) AS (VALUES (5))
SELECT printf('log=[INFO] procesados=%d', n) AS resultado FROM t;
""",
    },
}

S[143] = {
    "descripcion": "Descomponer una versión semántica 'mayor.menor.parche' en sus tres números.",
    "objetivo": "Entender **dependencias, versiones y lockfiles**: el versionado semántico (SemVer) 'mayor.menor.parche' comunica compatibilidad. Descomponerlo es el primer paso para gestionar dependencias con criterio.",
    "resultados": ["Parsear una versión semántica.", "Explicar qué significa cada componente.", "Reconocer el papel del lockfile."],
    "temas": [("SemVer", "mayor.menor.parche"), ("Compatibilidad", "Qué implica cada número"), ("Lockfile", "Versiones exactas fijadas")],
    "definiciones": [("Versionado semántico", "esquema mayor.menor.parche donde cada número señala el tipo de cambio. Clave: comunica compatibilidad."), ("Mayor/menor/parche", "cambios incompatibles / nuevas features / correcciones. Clave: guían las actualizaciones."), ("Lockfile", "archivo con las versiones exactas resueltas. Clave: builds reproducibles.")],
    "situacion": "Al depender de una librería '^1.4.2', importa si sube a 1.5.0 (compatible) o a 2.0.0 (posible ruptura). El lockfile fija la versión exacta para que todos obtengan lo mismo.",
    "entrada": "una línea con una versión `mayor.menor.parche`",
    "salida": "`mayor=<M> menor=<m> parche=<p>`",
    "formula": "separar la versión por puntos",
    "algoritmo": "LEER version ; separar por '.' ; ESCRIBIR componentes",
    "casos": [("1.2.3", "mayor=1 menor=2 parche=3"), ("0.5.10", "mayor=0 menor=5 parche=10"), ("2.0.0", "mayor=2 menor=0 parche=0")],
    "comparacion": [("Sintáctica", "split por '.' en cada lenguaje."), ("Semántica", "Cada número tiene un significado de compatibilidad."), ("Paradigmática", "SQL separa con funciones de texto.")],
    "familia": "npm, cargo, pip, composer usan SemVer y lockfiles (package-lock.json, Cargo.lock).",
    "errores": [("No commitear el lockfile", "builds distintos por máquina", "versionar el lockfile"), ("Fijar a 'latest'", "roturas por actualizaciones", "acotar rangos y confiar en el lock")],
    "faq": [("¿Qué sube en un parche?", "Solo correcciones compatibles; no rompe nada."), ("¿Por qué el lockfile?", "Garantiza que todos instalen exactamente las mismas versiones.")],
    "reto": "Compara dos versiones y di cuál es mayor; resuélvelo en **Go**.",
    "impls": {
        "python": r"""import sys

mayor, menor, parche = sys.stdin.readline().strip().split(".")
print(f"mayor={int(mayor)} menor={int(menor)} parche={int(parche)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const [mayor, menor, parche] = readFileSync(0, "utf8").trim().split(".").map(Number);
console.log(`mayor=${mayor} menor=${menor} parche=${parche}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const [mayor, menor, parche] = readFileSync(0, "utf8").trim().split(".").map(Number);
console.log(`mayor=${mayor} menor=${menor} parche=${parche}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] v = br.readLine().trim().split("\\.");
        System.out.println("mayor=" + Integer.parseInt(v[0]) + " menor=" + Integer.parseInt(v[1]) + " parche=" + Integer.parseInt(v[2]));
    }
}
""",
        "csharp": r"""using System;

string[] v = Console.In.ReadToEnd().Trim().Split('.');
Console.WriteLine($"mayor={int.Parse(v[0])} menor={int.Parse(v[1])} parche={int.Parse(v[2])}");
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
	v := strings.Split(strings.TrimSpace(line), ".")
	ma, _ := strconv.Atoi(v[0])
	me, _ := strconv.Atoi(v[1])
	pa, _ := strconv.Atoi(v[2])
	fmt.Printf("mayor=%d menor=%d parche=%d\n", ma, me, pa)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.trim().split('.').map(|x| x.parse().unwrap()).collect();
    println!("mayor={} menor={} parche={}", v[0], v[1], v[2]);
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long ma, me, pa;
    if (scanf("%ld.%ld.%ld", &ma, &me, &pa) != 3) return 1;
    printf("mayor=%ld menor=%ld parche=%ld\n", ma, me, pa);
    return 0;
}
""",
        "php": r"""<?php
[$ma, $me, $pa] = explode(".", trim(fgets(STDIN)));
echo "mayor=" . (int) $ma . " menor=" . (int) $me . " parche=" . (int) $pa . "\n";
""",
        "sql": r"""-- SQL: separa la versión con funciones de texto (ilustrativo).
WITH v(s) AS (VALUES ('1.2.3'))
SELECT printf('mayor=%d menor=%d parche=%d',
       CAST(substr(s, 1, instr(s, '.') - 1) AS INTEGER),
       CAST(substr(s, instr(s, '.') + 1, instr(substr(s, instr(s, '.') + 1), '.') - 1) AS INTEGER),
       CAST(substr(s, length(s) - instr(reverse(s), '.') + 2) AS INTEGER)) AS resultado
FROM v;
""",
    },
}

S[144] = {
    "descripcion": "Calcular una suma de comprobación (checksum) sumando los valores de una lista.",
    "objetivo": "Entender la **compilación reproducible y el empaquetado**: una build reproducible produce siempre el mismo artefacto para la misma entrada, comprobable con una suma de verificación (checksum). Aquí el checksum es la suma de los valores.",
    "resultados": ["Calcular una suma de comprobación.", "Explicar la reproducibilidad.", "Relacionar el checksum con la verificación de artefactos."],
    "temas": [("Reproducibilidad", "Misma entrada, mismo artefacto"), ("Checksum", "Huella de los datos"), ("Verificación", "Detectar cambios")],
    "definiciones": [("Compilación reproducible", "produce un artefacto idéntico byte a byte para la misma entrada. Clave: confianza y auditoría."), ("Checksum", "valor derivado de los datos que cambia si estos cambian. Clave: detecta alteraciones."), ("Artefacto", "salida de la build (binario, paquete). Clave: se verifica con su checksum.")],
    "situacion": "Al descargar un binario, su checksum publicado permite verificar que no fue alterado. Una build reproducible da siempre el mismo checksum, lo que hace auditable la cadena de suministro.",
    "entrada": "una línea con enteros separados por espacio",
    "salida": "`checksum=<suma de los valores>`",
    "formula": "checksum = suma de los valores",
    "algoritmo": "LEER lista ; checksum <- suma ; ESCRIBIR checksum",
    "casos": [("1 2 3", "checksum=6"), ("5", "checksum=5"), ("10 20 30", "checksum=60")],
    "comparacion": [("Sintáctica", "Suma en cada lenguaje (un checksum real usaría un hash)."), ("Semántica", "La misma entrada da el mismo checksum: reproducibilidad."), ("Paradigmática", "SQL suma con SUM.")],
    "familia": "Los gestores de paquetes verifican con SHA-256; aquí una suma simple ilustra el concepto.",
    "errores": [("Confiar en un checksum débil", "colisiones", "usar hashes criptográficos para seguridad real"), ("Builds no reproducibles", "checksums que cambian sin motivo", "eliminar fuentes de no-determinismo (fechas, orden)")],
    "faq": [("¿Suma o hash?", "Para integridad real se usa un hash (SHA-256); la suma solo ilustra."), ("¿Por qué builds reproducibles?", "Auditar que el binario proviene del código y no fue manipulado.")],
    "reto": "Usa un hash simple (suma ponderada por posición) y resuélvelo en **Python**.",
    "impls": {
        "python": r"""import sys

nums = [int(x) for x in sys.stdin.read().split()]
print(f"checksum={sum(nums)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`checksum=${nums.reduce((a, b) => a + b, 0)}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`checksum=${nums.reduce((a, b) => a + b, 0)}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        long c = 0;
        for (String s : p) c += Integer.parseInt(s);
        System.out.println("checksum=" + c);
    }
}
""",
        "csharp": r"""using System;
using System.Linq;

long c = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
    .Sum(x => (long) int.Parse(x));
Console.WriteLine($"checksum={c}");
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
	c := 0
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		c += n
	}
	fmt.Printf("checksum=%d\n", c)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let c: i64 = s.split_whitespace().map(|x| x.parse::<i64>().unwrap()).sum();
    println!("checksum={c}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long c = 0, x;
    while (scanf("%ld", &x) == 1) c += x;
    printf("checksum=%ld\n", c);
    return 0;
}
""",
        "php": r"""<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "checksum=" . array_sum($nums) . "\n";
""",
        "sql": r"""-- SQL: SUM como checksum simple.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT printf('checksum=%d', sum(x)) AS resultado FROM nums;
""",
    },
}

S[145] = {
    "descripcion": "Contar cuántos commits (mensajes) hay en un historial.",
    "objetivo": "Introducir **Git y el control de versiones**: el historial es una secuencia de commits (instantáneas con mensaje). Contar los commits es la operación básica sobre ese historial.",
    "resultados": ["Contar los commits de un historial.", "Explicar qué es un commit.", "Reconocer el valor del versionado."],
    "temas": [("Commit", "Instantánea con mensaje"), ("Historial", "Secuencia de commits"), ("Ramas", "Líneas de desarrollo")],
    "definiciones": [("Git", "sistema de control de versiones distribuido. Clave: historial completo en cada copia."), ("Commit", "instantánea del proyecto con un mensaje. Clave: unidad del historial."), ("Rama", "línea de desarrollo paralela. Clave: trabajar sin pisar la principal.")],
    "situacion": "Cada cambio importante se registra como un commit con su mensaje. El historial permite volver atrás, ver quién cambió qué y colaborar sin sobrescribir el trabajo ajeno.",
    "entrada": "una línea con mensajes de commit (palabras separadas por espacio)",
    "salida": "`commits=<cantidad>`",
    "formula": "contar los mensajes",
    "algoritmo": "LEER mensajes ; ESCRIBIR cantidad",
    "casos": [("fix add refactor", "commits=3"), ("init", "commits=1"), ("a b c d", "commits=4")],
    "comparacion": [("Sintáctica", "Contar palabras en cada lenguaje."), ("Semántica", "Cada commit es una instantánea inmutable."), ("Paradigmática", "SQL cuenta filas.")],
    "familia": "Git es el estándar; Mercurial y otros comparten el modelo de instantáneas versionadas.",
    "errores": [("Commits enormes y sin mensaje claro", "historial ilegible", "commits pequeños con mensajes descriptivos"), ("Commitear archivos generados", "ruido en el repo", "usar .gitignore")],
    "faq": [("¿Cada cuánto commitear?", "Cuando tienes un cambio coherente y funcional."), ("¿Git es solo para código?", "No: sirve para cualquier texto versionable (docs, configuración).")],
    "reto": "Cuenta solo los commits que empiezan por 'fix' y resuélvelo en **Python**.",
    "impls": {
        "python": r"""import sys

msgs = sys.stdin.read().split()
print(f"commits={len(msgs)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const msgs = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`commits=${msgs.length}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const msgs: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`commits=${msgs.length}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] msgs = br.readLine().trim().split("\\s+");
        System.out.println("commits=" + msgs.length);
    }
}
""",
        "csharp": r"""using System;

string[] msgs = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"commits={msgs.Length}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	msgs := strings.Fields(line)
	fmt.Printf("commits=%d\n", len(msgs))
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n = s.split_whitespace().count();
    println!("commits={n}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    char tok[256];
    int c = 0;
    while (scanf("%255s", tok) == 1) c++;
    printf("commits=%d\n", c);
    return 0;
}
""",
        "php": r"""<?php
$msgs = preg_split('/\s+/', trim(fgets(STDIN)));
echo "commits=" . count($msgs) . "\n";
""",
        "sql": r"""-- SQL: cuenta las filas (commits).
WITH commits(msg) AS (VALUES ('fix'), ('add'), ('refactor'))
SELECT printf('commits=%d', count(*)) AS resultado FROM commits;
""",
    },
}

S[146] = {
    "descripcion": "Verificar si un identificador cumple el estándar de estar en minúsculas (revisión de estilo).",
    "objetivo": "Practicar la **revisión de código y los estándares**: un linter comprueba automáticamente convenciones (nombres, formato). Aquí se valida que un identificador esté en minúsculas, como haría una regla de estilo.",
    "resultados": ["Validar una convención de nombres.", "Explicar el papel del linter.", "Reconocer el valor de los estándares."],
    "temas": [("Estándar de estilo", "Reglas compartidas"), ("Linter", "Verifica automáticamente"), ("Revisión de código", "Segundo par de ojos")],
    "definiciones": [("Estándar de código", "convenciones acordadas (nombres, formato). Clave: consistencia en el equipo."), ("Linter", "herramienta que detecta violaciones de estilo y errores probables. Clave: automatiza la revisión."), ("Revisión de código", "otra persona revisa el cambio antes de integrarlo. Clave: calidad y difusión de conocimiento.")],
    "situacion": "En muchos proyectos, los identificadores van en minúsculas. Un linter marca 'Total' como violación. Automatizar estas reglas evita discusiones y mantiene el código uniforme.",
    "entrada": "una palabra (identificador, solo letras)",
    "salida": "`valido=<true|false>` (true si está todo en minúsculas)",
    "formula": "valido si todos los caracteres son minúsculas",
    "algoritmo": "LEER palabra ; valido <- todos los caracteres en minúscula",
    "casos": [("total", "valido=true"), ("Total", "valido=false"), ("abc", "valido=true")],
    "comparacion": [("Sintáctica", "islower/comparación de caracteres en cada lenguaje."), ("Semántica", "La regla se comprueba carácter a carácter."), ("Paradigmática", "SQL compara con lower().")],
    "familia": "ESLint, Ruff, Clippy, gofmt/govet aplican reglas de estilo automáticamente.",
    "errores": [("Reglas de estilo manuales", "inconsistencia", "delegar en el linter"), ("Ignorar los avisos del linter", "bugs latentes", "resolverlos o justificarlos")],
    "faq": [("¿Linter o revisión humana?", "Ambos: el linter automatiza lo mecánico; la revisión, el criterio."), ("¿Por qué estándares?", "Un código uniforme se lee y mantiene mejor.")],
    "reto": "Valida también que empiece por letra y resuélvelo en **Rust**.",
    "impls": {
        "python": r"""import sys

w = sys.stdin.readline().strip()
valido = all("a" <= c <= "z" for c in w)
print(f"valido={'true' if valido else 'false'}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const w = readFileSync(0, "utf8").trim();
const valido = /^[a-z]+$/.test(w);
console.log(`valido=${valido ? "true" : "false"}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const w: string = readFileSync(0, "utf8").trim();
const valido = /^[a-z]+$/.test(w);
console.log(`valido=${valido ? "true" : "false"}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String w = br.readLine().trim();
        boolean valido = w.matches("[a-z]+");
        System.out.println("valido=" + (valido ? "true" : "false"));
    }
}
""",
        "csharp": r"""using System;
using System.Linq;

string w = Console.In.ReadToEnd().Trim();
bool valido = w.Length > 0 && w.All(c => c >= 'a' && c <= 'z');
Console.WriteLine($"valido={(valido ? "true" : "false")}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	w := strings.TrimSpace(line)
	valido := len(w) > 0
	for _, c := range w {
		if c < 'a' || c > 'z' {
			valido = false
		}
	}
	res := "false"
	if valido {
		res = "true"
	}
	fmt.Printf("valido=%s\n", res)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let w = s.trim();
    let valido = !w.is_empty() && w.chars().all(|c| c.is_ascii_lowercase());
    println!("valido={}", if valido { "true" } else { "false" });
}
""",
        "c": r"""#include <stdio.h>
#include <string.h>

int main(void) {
    char w[256];
    if (scanf("%255s", w) != 1) return 1;
    int valido = 1;
    for (int i = 0; w[i]; i++) {
        if (w[i] < 'a' || w[i] > 'z') valido = 0;
    }
    printf("valido=%s\n", valido ? "true" : "false");
    return 0;
}
""",
        "php": r"""<?php
$w = trim(fgets(STDIN));
$valido = preg_match('/^[a-z]+$/', $w) === 1;
echo "valido=" . ($valido ? "true" : "false") . "\n";
""",
        "sql": r"""-- SQL: compara con la versión en minúsculas.
WITH t(w) AS (VALUES ('total'))
SELECT printf('valido=%s', CASE WHEN w = lower(w) THEN 'true' ELSE 'false' END) AS resultado FROM t;
""",
    },
}

S[147] = {
    "descripcion": "Determinar si un pipeline de CI está verde: todos los pasos (0 o 1) deben ser 1.",
    "objetivo": "Entender la **integración continua (CI)**: cada cambio dispara un pipeline de pasos (compilar, probar, lint); si todos pasan, el resultado es 'verde'. Si uno falla, es 'rojo' y el cambio se bloquea.",
    "resultados": ["Combinar el resultado de varios pasos.", "Explicar el pipeline de CI.", "Reconocer el valor de bloquear en rojo."],
    "temas": [("CI", "Verificar cada cambio"), ("Pipeline", "Pasos encadenados"), ("Verde/rojo", "Todo pasa o algo falla")],
    "definiciones": [("Integración continua", "ejecutar automáticamente pruebas y checks en cada cambio. Clave: detecta errores pronto."), ("Pipeline", "secuencia de pasos (build, test, lint). Clave: todos deben pasar."), ("Verde/rojo", "estado del pipeline: todo pasa (verde) o algo falla (rojo). Clave: bloquea lo roto.")],
    "situacion": "Al subir un cambio, el CI compila, prueba y revisa el estilo. Si algún paso falla, el pipeline se pone rojo y el cambio no se integra. Es lo que mantiene verde este repositorio.",
    "entrada": "una línea con 0 y 1 (resultado de cada paso; 1 = pasó)",
    "salida": "`ci=<verde|rojo>`",
    "formula": "verde si todos los pasos son 1",
    "algoritmo": "LEER pasos ; verde <- todos == 1",
    "casos": [("1 1 1", "ci=verde"), ("1 0 1", "ci=rojo"), ("1 1", "ci=verde")],
    "comparacion": [("Sintáctica", "all/every/reduce en cada lenguaje."), ("Semántica", "Basta un paso en rojo para que el pipeline falle."), ("Paradigmática", "SQL usa MIN sobre los pasos.")],
    "familia": "GitHub Actions, GitLab CI, Jenkins ejecutan pipelines que bloquean en rojo.",
    "errores": [("Ignorar el rojo del CI", "integrar código roto", "no fusionar hasta que esté verde"), ("Pipelines lentísimos", "el equipo los evita", "optimizar con caché y paralelismo")],
    "faq": [("¿Qué pasos debe tener?", "Al menos compilar, probar y lint; según el proyecto, más."), ("¿CI y CD?", "CI verifica; CD (entrega/despliegue continuos) automatiza la publicación.")],
    "reto": "Reporta cuál paso falló (índice) y resuélvelo en **Go**.",
    "impls": {
        "python": r"""import sys

pasos = [int(x) for x in sys.stdin.read().split()]
print(f"ci={'verde' if all(p == 1 for p in pasos) else 'rojo'}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const pasos = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`ci=${pasos.every((p) => p === 1) ? "verde" : "rojo"}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const pasos: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`ci=${pasos.every((p) => p === 1) ? "verde" : "rojo"}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        boolean verde = true;
        for (String s : p) if (Integer.parseInt(s) != 1) verde = false;
        System.out.println("ci=" + (verde ? "verde" : "rojo"));
    }
}
""",
        "csharp": r"""using System;
using System.Linq;

bool verde = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
    .All(x => int.Parse(x) == 1);
Console.WriteLine($"ci={(verde ? "verde" : "rojo")}");
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
	verde := true
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		if n != 1 {
			verde = false
		}
	}
	res := "rojo"
	if verde {
		res = "verde"
	}
	fmt.Printf("ci=%s\n", res)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let verde = s.split_whitespace().all(|x| x.parse::<i64>().unwrap() == 1);
    println!("ci={}", if verde { "verde" } else { "rojo" });
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long x;
    int verde = 1;
    while (scanf("%ld", &x) == 1) {
        if (x != 1) verde = 0;
    }
    printf("ci=%s\n", verde ? "verde" : "rojo");
    return 0;
}
""",
        "php": r"""<?php
$pasos = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$verde = !in_array(0, $pasos, true);
echo "ci=" . ($verde ? "verde" : "rojo") . "\n";
""",
        "sql": r"""-- SQL: verde si el mínimo de los pasos es 1.
WITH pasos(x) AS (VALUES (1), (1), (1))
SELECT printf('ci=%s', CASE WHEN min(x) = 1 THEN 'verde' ELSE 'rojo' END) AS resultado FROM pasos;
""",
    },
}

S[148] = {
    "descripcion": "Preparar el despliegue de una versión, prefijándola con 'v'.",
    "objetivo": "Introducir la **entrega y el despliegue**: llevar el artefacto probado a producción. Etiquetar la versión (p. ej. `v1.2.3`) es parte de una entrega ordenada y trazable.",
    "resultados": ["Etiquetar una versión para desplegar.", "Explicar entrega vs. despliegue.", "Reconocer el valor de la trazabilidad."],
    "temas": [("Entrega", "Preparar para publicar"), ("Despliegue", "Poner en producción"), ("Etiqueta de versión", "Trazabilidad")],
    "definiciones": [("Entrega continua", "mantener el software siempre listo para desplegar. Clave: releases frecuentes y seguras."), ("Despliegue", "poner una versión en producción. Clave: puede ser manual o automático (CD)."), ("Etiqueta (tag)", "marca de una versión en el historial (v1.2.3). Clave: trazabilidad.")],
    "situacion": "Tras pasar el CI, se etiqueta la versión (`v1.2.3`) y se despliega. La etiqueta permite saber exactamente qué código está en producción y volver atrás si hace falta.",
    "entrada": "una línea con una versión `mayor.menor.parche`",
    "salida": "`desplegado=v<versión>`",
    "formula": "prefijar la versión con 'v'",
    "algoritmo": "LEER version ; ESCRIBIR 'desplegado=v' + version",
    "casos": [("1.2.3", "desplegado=v1.2.3"), ("0.9.0", "desplegado=v0.9.0"), ("2.1.5", "desplegado=v2.1.5")],
    "comparacion": [("Sintáctica", "Concatenación en cada lenguaje."), ("Semántica", "La etiqueta identifica la versión desplegada."), ("Paradigmática", "SQL concatena con ||.")],
    "familia": "Git tags, releases de GitHub, y las herramientas de CD (Argo, Spinnaker) gestionan despliegues versionados.",
    "errores": [("Desplegar sin etiquetar", "no saber qué hay en producción", "etiquetar cada release"), ("Desplegar sin pasar el CI", "romper producción", "desplegar solo lo que está verde")],
    "faq": [("¿Entrega o despliegue continuo?", "Entrega deja el software listo; despliegue continuo lo publica automáticamente."), ("¿Por qué el prefijo 'v'?", "Convención común para distinguir etiquetas de versión.")],
    "reto": "Añade el entorno (`v1.2.3-prod`) y resuélvelo en **Python**.",
    "impls": {
        "python": r"""import sys

version = sys.stdin.readline().strip()
print(f"desplegado=v{version}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const version = readFileSync(0, "utf8").trim();
console.log(`desplegado=v${version}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const version: string = readFileSync(0, "utf8").trim();
console.log(`desplegado=v${version}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String version = br.readLine().trim();
        System.out.println("desplegado=v" + version);
    }
}
""",
        "csharp": r"""using System;

string version = Console.In.ReadToEnd().Trim();
Console.WriteLine($"desplegado=v{version}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	version := strings.TrimSpace(line)
	fmt.Printf("desplegado=v%s\n", version)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let version = s.trim();
    println!("desplegado=v{version}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    char version[64];
    if (scanf("%63s", version) != 1) return 1;
    printf("desplegado=v%s\n", version);
    return 0;
}
""",
        "php": r"""<?php
$version = trim(fgets(STDIN));
echo "desplegado=v$version\n";
""",
        "sql": r"""-- SQL: concatena el prefijo con ||.
WITH t(v) AS (VALUES ('1.2.3'))
SELECT 'desplegado=v' || v AS resultado FROM t;
""",
    },
}

S[149] = {
    "descripcion": "Contar las capas (componentes) de una arquitectura descrita por sus nombres.",
    "objetivo": "Introducir el **diseño y la arquitectura**: un sistema se organiza en capas o componentes con responsabilidades claras. Contar las capas es la medida más básica de su estructura.",
    "resultados": ["Contar las capas de una arquitectura.", "Explicar la separación de responsabilidades.", "Reconocer estilos arquitectónicos."],
    "temas": [("Arquitectura", "Estructura de alto nivel"), ("Capa/componente", "Responsabilidad definida"), ("Separación de responsabilidades", "Cada parte hace una cosa")],
    "definiciones": [("Arquitectura", "estructura de alto nivel de un sistema y sus componentes. Clave: guía las decisiones grandes."), ("Capa", "grupo de componentes con una responsabilidad (presentación, lógica, datos). Clave: separa preocupaciones."), ("Acoplamiento", "grado de dependencia entre componentes. Clave: bajo acoplamiento facilita el cambio.")],
    "situacion": "Un sistema típico tiene capas: web (interfaz), api (lógica), datos (persistencia). Nombrar y contar las capas es el primer paso para razonar sobre su arquitectura.",
    "entrada": "una línea con nombres de capas (palabras separadas por espacio)",
    "salida": "`capas=<cantidad>`",
    "formula": "contar los nombres de capa",
    "algoritmo": "LEER capas ; ESCRIBIR cantidad",
    "casos": [("web api datos", "capas=3"), ("cli", "capas=1"), ("web api datos cache", "capas=4")],
    "comparacion": [("Sintáctica", "Contar palabras en cada lenguaje."), ("Semántica", "Cada capa aísla una responsabilidad."), ("Paradigmática", "SQL cuenta filas.")],
    "familia": "Arquitecturas en capas, hexagonal, microservicios: todas organizan componentes con responsabilidades.",
    "errores": [("Capas con responsabilidades mezcladas", "difícil de mantener", "una responsabilidad por capa"), ("Alto acoplamiento", "un cambio propaga a todo", "definir contratos claros entre capas")],
    "faq": [("¿Cuántas capas?", "Las que el problema justifique; ni de más ni de menos."), ("¿Capas o microservicios?", "Capas dentro de un proceso; microservicios los separan en servicios.")],
    "reto": "Marca si la capa 'datos' está presente y resuélvelo en **Python**.",
    "impls": {
        "python": r"""import sys

capas = sys.stdin.read().split()
print(f"capas={len(capas)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const capas = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`capas=${capas.length}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const capas: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`capas=${capas.length}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] capas = br.readLine().trim().split("\\s+");
        System.out.println("capas=" + capas.length);
    }
}
""",
        "csharp": r"""using System;

string[] capas = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"capas={capas.Length}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	capas := strings.Fields(line)
	fmt.Printf("capas=%d\n", len(capas))
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n = s.split_whitespace().count();
    println!("capas={n}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    char tok[256];
    int c = 0;
    while (scanf("%255s", tok) == 1) c++;
    printf("capas=%d\n", c);
    return 0;
}
""",
        "php": r"""<?php
$capas = preg_split('/\s+/', trim(fgets(STDIN)));
echo "capas=" . count($capas) . "\n";
""",
        "sql": r"""-- SQL: cuenta las filas (capas).
WITH capas(nombre) AS (VALUES ('web'), ('api'), ('datos'))
SELECT printf('capas=%d', count(*)) AS resultado FROM capas;
""",
    },
}

S[150] = {
    "descripcion": "Refactorizar el cálculo del doble (de n*2 a n+n) y verificar que el comportamiento no cambia.",
    "objetivo": "Practicar la **refactorización segura**: mejorar la estructura interna del código sin cambiar su comportamiento observable, respaldado por pruebas. Cambiar `n*2` por `n+n` es una refactorización que las pruebas confirman equivalente.",
    "resultados": ["Refactorizar sin cambiar el resultado.", "Verificar la equivalencia con una prueba.", "Explicar por qué las pruebas habilitan refactorizar."],
    "temas": [("Refactorización", "Mejorar sin cambiar comportamiento"), ("Comportamiento observable", "Lo que se mantiene"), ("Red de pruebas", "Habilita el cambio seguro")],
    "definiciones": [("Refactorización", "reestructurar el código sin alterar su comportamiento observable. Clave: mejora interna."), ("Comportamiento observable", "lo que el usuario/prueba percibe. Clave: no debe cambiar al refactorizar."), ("Red de seguridad", "las pruebas que confirman que la refactorización no rompió nada. Clave: sin ellas, refactorizar es arriesgado.")],
    "situacion": "Quieres simplificar una función. Con pruebas que fijan su comportamiento, refactorizas con confianza: si las pruebas siguen verdes, el comportamiento se mantuvo. Aquí `n*2` y `n+n` son equivalentes.",
    "entrada": "un entero `n`",
    "salida": "`equivalente=<true|false> resultado=<2n>`",
    "formula": "viejo = n*2 ; nuevo = n+n ; equivalente si coinciden",
    "algoritmo": "viejo <- n*2 ; nuevo <- n+n ; equivalente <- (viejo==nuevo) ; ESCRIBIR",
    "casos": [("5", "equivalente=true resultado=10"), ("0", "equivalente=true resultado=0"), ("7", "equivalente=true resultado=14")],
    "comparacion": [("Sintáctica", "Dos expresiones equivalentes en cada lenguaje."), ("Semántica", "La refactorización preserva el resultado observable."), ("Paradigmática", "SQL refactoriza consultas manteniendo el resultado.")],
    "familia": "Todos los IDE ofrecen refactorizaciones automáticas (renombrar, extraer) respaldadas por el análisis.",
    "errores": [("Refactorizar sin pruebas", "romper comportamiento sin darte cuenta", "asegurar la red de pruebas primero"), ("Cambiar comportamiento 'de paso'", "no es refactorizar, es modificar", "separar refactorización de cambio funcional")],
    "faq": [("¿Refactorizar cambia el comportamiento?", "No: por definición lo preserva; solo mejora la estructura."), ("¿Cuándo refactorizar?", "Continuamente, en pequeños pasos, con las pruebas en verde.")],
    "reto": "Refactoriza una función más compleja y verifica con varios casos; resuélvelo en **Go**.",
    "impls": {
        "python": r"""import sys

n = int(sys.stdin.readline())
viejo = n * 2
nuevo = n + n
eq = "true" if viejo == nuevo else "false"
print(f"equivalente={eq} resultado={nuevo}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const viejo = n * 2, nuevo = n + n;
console.log(`equivalente=${viejo === nuevo ? "true" : "false"} resultado=${nuevo}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const viejo = n * 2, nuevo = n + n;
console.log(`equivalente=${viejo === nuevo ? "true" : "false"} resultado=${nuevo}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        long viejo = n * 2, nuevo = n + n;
        System.out.println("equivalente=" + (viejo == nuevo ? "true" : "false") + " resultado=" + nuevo);
    }
}
""",
        "csharp": r"""using System;

long n = long.Parse(Console.In.ReadToEnd().Trim());
long viejo = n * 2, nuevo = n + n;
Console.WriteLine($"equivalente={(viejo == nuevo ? "true" : "false")} resultado={nuevo}");
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
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	viejo, nuevo := n*2, n+n
	res := "false"
	if viejo == nuevo {
		res = "true"
	}
	fmt.Printf("equivalente=%s resultado=%d\n", res, nuevo)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let (viejo, nuevo) = (n * 2, n + n);
    let eq = if viejo == nuevo { "true" } else { "false" };
    println!("equivalente={eq} resultado={nuevo}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long viejo = n * 2, nuevo = n + n;
    printf("equivalente=%s resultado=%ld\n", viejo == nuevo ? "true" : "false", nuevo);
    return 0;
}
""",
        "php": r"""<?php
$n = (int) trim(fgets(STDIN));
$viejo = $n * 2;
$nuevo = $n + $n;
echo "equivalente=" . ($viejo === $nuevo ? "true" : "false") . " resultado=$nuevo\n";
""",
        "sql": r"""-- SQL: dos expresiones equivalentes.
WITH nums(n) AS (VALUES (5))
SELECT printf('equivalente=%s resultado=%d', CASE WHEN n * 2 = n + n THEN 'true' ELSE 'false' END, n + n) AS resultado FROM nums;
""",
    },
}

S[151] = {
    "descripcion": "Aplicar una operación (suma, resta o producto) elegida por nombre: el patrón Estrategia.",
    "objetivo": "Practicar los **patrones de diseño comparados**: el patrón **Estrategia** encapsula algoritmos intercambiables tras una interfaz común. Elegir la operación por su nombre selecciona la estrategia a aplicar.",
    "resultados": ["Aplicar el patrón Estrategia.", "Seleccionar un algoritmo en ejecución.", "Reconocer patrones en cada lenguaje."],
    "temas": [("Patrón de diseño", "Solución reutilizable a un problema común"), ("Estrategia", "Algoritmos intercambiables"), ("Selección en ejecución", "Elegir el comportamiento al vuelo")],
    "definiciones": [("Patrón de diseño", "solución probada y reutilizable a un problema de diseño recurrente. Clave: vocabulario común."), ("Estrategia", "patrón que encapsula algoritmos intercambiables tras una interfaz. Clave: cambiar el comportamiento sin condicionales dispersos."), ("Despacho", "seleccionar qué código ejecutar según un valor. Clave: aquí, por el nombre de la operación.")],
    "situacion": "Un sistema de cobro puede usar distintas estrategias (tarjeta, transferencia). El patrón Estrategia las hace intercambiables. Aquí, la operación se elige por su nombre y se aplica.",
    "entrada": "una línea `estrategia a b` (estrategia ∈ {suma, resta, producto})",
    "salida": "`resultado=<a estrategia b>`",
    "formula": "aplicar la estrategia elegida a a y b",
    "algoritmo": "LEER estrategia, a, b ; seleccionar operación ; aplicar",
    "casos": [("suma 3 4", "resultado=7"), ("resta 10 3", "resultado=7"), ("producto 5 6", "resultado=30")],
    "comparacion": [("Sintáctica", "map de funciones, interfaz o switch en cada lenguaje."), ("Semántica", "La estrategia se elige en ejecución."), ("Paradigmática", "SQL usa CASE.")],
    "familia": "Estrategia, Observer, Factory, Singleton son patrones clásicos (GoF) presentes en todos los lenguajes OO.",
    "errores": [("Condicionales gigantes en vez de estrategias", "código rígido", "encapsular cada algoritmo tras una interfaz común"), ("Sobre-aplicar patrones", "complejidad innecesaria", "usar el patrón solo cuando aporta")],
    "faq": [("¿Estrategia o if/else?", "Estrategia cuando los algoritmos cambian o crecen; if/else para casos simples y fijos."), ("¿Los patrones son obligatorios?", "No: son herramientas; aplícalos cuando resuelven un problema real.")],
    "reto": "Añade la estrategia 'division' y resuélvelo en **Go** con un mapa de funciones.",
    "impls": {
        "python": r"""import sys

estrategia, a, b = sys.stdin.readline().split()
a, b = int(a), int(b)
ops = {"suma": a + b, "resta": a - b, "producto": a * b}
print(f"resultado={ops[estrategia]}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const [estrategia, a, b] = readFileSync(0, "utf8").trim().split(/\s+/);
const x = Number(a), y = Number(b);
const ops = { suma: x + y, resta: x - y, producto: x * y };
console.log(`resultado=${ops[estrategia]}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const [estrategia, a, b] = readFileSync(0, "utf8").trim().split(/\s+/);
const x = Number(a), y = Number(b);
const ops: Record<string, number> = { suma: x + y, resta: x - y, producto: x * y };
console.log(`resultado=${ops[estrategia]}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        long a = Long.parseLong(t[1]), b = Long.parseLong(t[2]);
        long r;
        switch (t[0]) {
            case "suma": r = a + b; break;
            case "resta": r = a - b; break;
            default: r = a * b;
        }
        System.out.println("resultado=" + r);
    }
}
""",
        "csharp": r"""using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long a = long.Parse(t[1]), b = long.Parse(t[2]);
long r = t[0] switch { "suma" => a + b, "resta" => a - b, _ => a * b };
Console.WriteLine($"resultado={r}");
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
	t := strings.Fields(line)
	a, _ := strconv.Atoi(t[1])
	b, _ := strconv.Atoi(t[2])
	ops := map[string]int{"suma": a + b, "resta": a - b, "producto": a * b}
	fmt.Printf("resultado=%d\n", ops[t[0]])
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let a: i64 = t[1].parse().unwrap();
    let b: i64 = t[2].parse().unwrap();
    let r = match t[0] {
        "suma" => a + b,
        "resta" => a - b,
        _ => a * b,
    };
    println!("resultado={r}");
}
""",
        "c": r"""#include <stdio.h>
#include <string.h>

int main(void) {
    char e[32];
    long a, b;
    if (scanf("%31s %ld %ld", e, &a, &b) != 3) return 1;
    long r;
    if (strcmp(e, "suma") == 0) r = a + b;
    else if (strcmp(e, "resta") == 0) r = a - b;
    else r = a * b;
    printf("resultado=%ld\n", r);
    return 0;
}
""",
        "php": r"""<?php
[$e, $a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;
$ops = ["suma" => $a + $b, "resta" => $a - $b, "producto" => $a * $b];
echo "resultado=" . $ops[$e] . "\n";
""",
        "sql": r"""-- SQL: selecciona la estrategia con CASE.
WITH t(e, a, b) AS (VALUES ('suma', 3, 4))
SELECT printf('resultado=%d', CASE e WHEN 'suma' THEN a + b WHEN 'resta' THEN a - b ELSE a * b END) AS resultado FROM t;
""",
    },
}

S[152] = {
    "descripcion": "Sumar 1 a n contando cuántas operaciones se realizan, como en un perfilado.",
    "objetivo": "Introducir el **rendimiento y el perfilado (profiling)**: medir dónde se gasta el tiempo o cuántas operaciones se hacen para optimizar con datos, no por intuición. Contar las operaciones de una suma es un perfilado en miniatura.",
    "resultados": ["Contar las operaciones de un algoritmo.", "Explicar el perfilado.", "Relacionar operaciones con complejidad."],
    "temas": [("Perfilado", "Medir dónde se gasta el coste"), ("Conteo de operaciones", "Cuánto trabajo se hace"), ("Optimizar con datos", "No por intuición")],
    "definiciones": [("Perfilado", "medir el uso de tiempo/recursos de un programa. Clave: optimizar con evidencia."), ("Operación", "unidad de trabajo (una suma, una comparación). Clave: contarlas estima el coste."), ("Cuello de botella", "la parte que domina el coste. Clave: optimizar ahí primero.")],
    "situacion": "Antes de optimizar, se perfila: ¿dónde se gasta el tiempo? Contar operaciones (aquí, n sumas para sumar 1..n) revela la complejidad y guía las mejoras hacia donde importan.",
    "entrada": "un entero `n` (n >= 1)",
    "salida": "`operaciones=<n> resultado=<1+...+n>`",
    "formula": "sumar 1..n contando cada suma",
    "algoritmo": "ops <- 0 ; suma <- 0 ; PARA i de 1 a n: suma+=i ; ops++",
    "casos": [("5", "operaciones=5 resultado=15"), ("1", "operaciones=1 resultado=1"), ("3", "operaciones=3 resultado=6")],
    "comparacion": [("Sintáctica", "Contador de operaciones en el bucle."), ("Semántica", "El conteo estima el coste (O(n) aquí)."), ("Paradigmática", "SQL se perfila con EXPLAIN.")],
    "familia": "perf, valgrind (C), cProfile (Python), pprof (Go), el profiler de la JVM/.NET miden el rendimiento real.",
    "errores": [("Optimizar sin medir", "atacar lo que no es el cuello de botella", "perfilar primero"), ("Micro-optimizar lo irrelevante", "esfuerzo desperdiciado", "optimizar el cuello de botella real")],
    "faq": [("¿Contar operaciones o cronometrar?", "El conteo estima la complejidad; el cronómetro mide el tiempo real."), ("¿Perfilar en desarrollo o producción?", "Ambos: en desarrollo para iterar; en producción para casos reales.")],
    "reto": "Compara las operaciones de la suma con bucle vs. la fórmula n(n+1)/2 y resuélvelo en **Python**.",
    "impls": {
        "python": r"""import sys

n = int(sys.stdin.readline())
ops = 0
suma = 0
for i in range(1, n + 1):
    suma += i
    ops += 1
print(f"operaciones={ops} resultado={suma}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let ops = 0, suma = 0;
for (let i = 1; i <= n; i++) {
  suma += i;
  ops += 1;
}
console.log(`operaciones=${ops} resultado=${suma}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let ops = 0, suma = 0;
for (let i = 1; i <= n; i++) {
  suma += i;
  ops += 1;
}
console.log(`operaciones=${ops} resultado=${suma}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        long ops = 0, suma = 0;
        for (int i = 1; i <= n; i++) {
            suma += i;
            ops += 1;
        }
        System.out.println("operaciones=" + ops + " resultado=" + suma);
    }
}
""",
        "csharp": r"""using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long ops = 0, suma = 0;
for (int i = 1; i <= n; i++) {
    suma += i;
    ops += 1;
}
Console.WriteLine($"operaciones={ops} resultado={suma}");
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
	ops, suma := 0, 0
	for i := 1; i <= n; i++ {
		suma += i
		ops++
	}
	fmt.Printf("operaciones=%d resultado=%d\n", ops, suma)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut ops = 0i64;
    let mut suma = 0i64;
    for i in 1..=n {
        suma += i;
        ops += 1;
    }
    println!("operaciones={ops} resultado={suma}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long ops = 0, suma = 0;
    for (long i = 1; i <= n; i++) {
        suma += i;
        ops++;
    }
    printf("operaciones=%ld resultado=%ld\n", ops, suma);
    return 0;
}
""",
        "php": r"""<?php
$n = (int) trim(fgets(STDIN));
$ops = 0;
$suma = 0;
for ($i = 1; $i <= $n; $i++) {
    $suma += $i;
    $ops++;
}
echo "operaciones=$ops resultado=$suma\n";
""",
        "sql": r"""-- SQL: se perfila con EXPLAIN; aquí, conteo y suma.
WITH RECURSIVE r(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM r WHERE i < 5)
SELECT printf('operaciones=%d resultado=%d', count(*), sum(i)) AS resultado FROM r;
""",
    },
}

S[153] = {
    "descripcion": "Validar que una entrada solo contiene caracteres alfanuméricos (seguridad de entradas).",
    "objetivo": "Introducir la **seguridad**: validar y sanear las entradas para evitar inyecciones y datos maliciosos. Comprobar que una entrada es alfanumérica es una validación básica que cierra muchos ataques.",
    "resultados": ["Validar una entrada contra un conjunto permitido.", "Explicar por qué no confiar en la entrada.", "Reconocer riesgos de seguridad comunes."],
    "temas": [("Validación de entrada", "No confiar en lo externo"), ("Saneamiento", "Limpiar datos peligrosos"), ("Inyección", "Datos que se ejecutan como código")],
    "definiciones": [("Validación de entrada", "comprobar que los datos cumplen lo esperado antes de usarlos. Clave: primera defensa."), ("Saneamiento", "eliminar o escapar caracteres peligrosos. Clave: evita inyecciones."), ("Inyección", "datos maliciosos que el programa interpreta como comando (SQL, shell). Clave: causa frecuente de brechas.")],
    "situacion": "Un campo que debería ser un nombre recibe `'; DROP TABLE`. Validar que solo contiene caracteres alfanuméricos rechaza la entrada maliciosa antes de que cause daño.",
    "entrada": "una palabra (entrada a validar)",
    "salida": "`seguro=<true|false>` (true si es alfanumérica)",
    "formula": "seguro si todos los caracteres son letras o dígitos",
    "algoritmo": "LEER entrada ; seguro <- todos los caracteres alfanuméricos",
    "casos": [("abc", "seguro=true"), ("a;b", "seguro=false"), ("hola123", "seguro=true")],
    "comparacion": [("Sintáctica", "isalnum/regex en cada lenguaje."), ("Semántica", "Se valida contra una lista blanca (más seguro que una negra)."), ("Paradigmática", "SQL usa consultas parametrizadas para evitar inyección.")],
    "familia": "Toda plataforma web valida entradas; las consultas parametrizadas evitan la inyección SQL.",
    "errores": [("Confiar en la entrada del usuario", "inyecciones y corrupción", "validar y sanear siempre"), ("Lista negra en vez de blanca", "olvidar un caso peligroso", "permitir solo lo conocido (lista blanca)")],
    "faq": [("¿Validar en cliente o servidor?", "En ambos, pero la validación del servidor es la que cuenta."), ("¿Cómo evitar inyección SQL?", "Con consultas parametrizadas, nunca concatenando la entrada.")],
    "reto": "Permite también el guion bajo y resuélvelo en **Rust**.",
    "impls": {
        "python": r"""import sys

w = sys.stdin.readline().strip()
seguro = w.isalnum()
print(f"seguro={'true' if seguro else 'false'}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const w = readFileSync(0, "utf8").trim();
const seguro = /^[A-Za-z0-9]+$/.test(w);
console.log(`seguro=${seguro ? "true" : "false"}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const w: string = readFileSync(0, "utf8").trim();
const seguro = /^[A-Za-z0-9]+$/.test(w);
console.log(`seguro=${seguro ? "true" : "false"}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String w = br.readLine().trim();
        boolean seguro = w.matches("[A-Za-z0-9]+");
        System.out.println("seguro=" + (seguro ? "true" : "false"));
    }
}
""",
        "csharp": r"""using System;
using System.Linq;

string w = Console.In.ReadToEnd().Trim();
bool seguro = w.Length > 0 && w.All(char.IsLetterOrDigit);
Console.WriteLine($"seguro={(seguro ? "true" : "false")}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"unicode"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	w := strings.TrimSpace(line)
	seguro := len(w) > 0
	for _, c := range w {
		if !unicode.IsLetter(c) && !unicode.IsDigit(c) {
			seguro = false
		}
	}
	res := "false"
	if seguro {
		res = "true"
	}
	fmt.Printf("seguro=%s\n", res)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let w = s.trim();
    let seguro = !w.is_empty() && w.chars().all(|c| c.is_ascii_alphanumeric());
    println!("seguro={}", if seguro { "true" } else { "false" });
}
""",
        "c": r"""#include <stdio.h>
#include <ctype.h>

int main(void) {
    char w[256];
    if (scanf("%255s", w) != 1) return 1;
    int seguro = 1;
    for (int i = 0; w[i]; i++) {
        if (!isalnum((unsigned char) w[i])) seguro = 0;
    }
    printf("seguro=%s\n", seguro ? "true" : "false");
    return 0;
}
""",
        "php": r"""<?php
$w = trim(fgets(STDIN));
$seguro = ctype_alnum($w);
echo "seguro=" . ($seguro ? "true" : "false") . "\n";
""",
        "sql": r"""-- SQL: se evita la inyección con consultas parametrizadas; aquí, validación por patrón.
WITH t(w) AS (VALUES ('abc'))
SELECT printf('seguro=%s', CASE WHEN w GLOB '*[^A-Za-z0-9]*' THEN 'false' ELSE 'true' END) AS resultado FROM t;
""",
    },
}

S[154] = {
    "descripcion": "Calcular una métrica de mantenibilidad simple: el número de módulos de un sistema.",
    "objetivo": "Cerrar la parte con la **mantenibilidad, la documentación y la deuda técnica**: medir la complejidad ayuda a mantener el código sano. Contar los módulos es una métrica básica; la deuda técnica crece cuando se ignora.",
    "resultados": ["Calcular una métrica simple de estructura.", "Explicar la deuda técnica.", "Reconocer el valor de la documentación."],
    "temas": [("Mantenibilidad", "Facilidad de cambiar el código"), ("Deuda técnica", "El coste de los atajos"), ("Métricas", "Medir para gestionar")],
    "definiciones": [("Mantenibilidad", "facilidad con que el código se entiende y modifica. Clave: reduce el coste futuro."), ("Deuda técnica", "coste acumulado de decisiones rápidas que habrá que pagar. Clave: crece si se ignora."), ("Documentación", "explicar el porqué del código. Clave: baja la barrera para mantenerlo.")],
    "situacion": "Un sistema con muchos módulos poco documentados acumula deuda técnica: cada cambio cuesta más. Medir su estructura y documentar el porqué mantiene el proyecto sano a largo plazo.",
    "entrada": "una línea con nombres de módulos (palabras separadas por espacio)",
    "salida": "`complejidad=<número de módulos>`",
    "formula": "contar los módulos",
    "algoritmo": "LEER módulos ; ESCRIBIR cantidad",
    "casos": [("a b c", "complejidad=3"), ("x", "complejidad=1"), ("a b c d e", "complejidad=5")],
    "comparacion": [("Sintáctica", "Contar palabras en cada lenguaje."), ("Semántica", "La métrica estima la complejidad estructural."), ("Paradigmática", "SQL cuenta filas.")],
    "familia": "SonarQube y linters miden complejidad ciclomática, duplicación y deuda técnica automáticamente.",
    "errores": [("Ignorar la deuda técnica", "el código se vuelve inmantenible", "pagarla en pequeñas dosis continuas"), ("Documentar el qué en vez del porqué", "comentarios redundantes", "explicar las decisiones, no repetir el código")],
    "faq": [("¿Deuda técnica es siempre mala?", "No: a veces es un préstamo consciente; el problema es no pagarla."), ("¿Qué documentar?", "El porqué de las decisiones; el qué suele leerse en el código.")],
    "reto": "Marca 'alta' si hay más de 4 módulos y resuélvelo en **Python**.",
    "impls": {
        "python": r"""import sys

mods = sys.stdin.read().split()
print(f"complejidad={len(mods)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const mods = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`complejidad=${mods.length}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const mods: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`complejidad=${mods.length}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] mods = br.readLine().trim().split("\\s+");
        System.out.println("complejidad=" + mods.length);
    }
}
""",
        "csharp": r"""using System;

string[] mods = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"complejidad={mods.Length}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	mods := strings.Fields(line)
	fmt.Printf("complejidad=%d\n", len(mods))
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n = s.split_whitespace().count();
    println!("complejidad={n}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    char tok[256];
    int c = 0;
    while (scanf("%255s", tok) == 1) c++;
    printf("complejidad=%d\n", c);
    return 0;
}
""",
        "php": r"""<?php
$mods = preg_split('/\s+/', trim(fgets(STDIN)));
echo "complejidad=" . count($mods) . "\n";
""",
        "sql": r"""-- SQL: cuenta las filas (módulos).
WITH mods(nombre) AS (VALUES ('a'), ('b'), ('c'))
SELECT printf('complejidad=%d', count(*)) AS resultado FROM mods;
""",
    },
}


def main():
    for num, spec in S.items():
        g3.write_class(num, spec)
        print(f"Clase {num:03d} generada.")


if __name__ == "__main__":
    main()
