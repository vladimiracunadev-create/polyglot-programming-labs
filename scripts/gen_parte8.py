"""Parte 8 — Cómo funcionan los lenguajes (clases 123-138). Reutiliza gen_parte3.write_class."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_parte3 as g3  # noqa: E402

S = {}

S[123] = {
    "descripcion": "Evaluar una expresión 'a op b' (op = +, -, *), simulando las fases lexer → parser → evaluador.",
    "objetivo": "Ver las **fases de compilación** en miniatura: separar la entrada en tokens (léxico), reconocer su estructura (sintáctico) y calcular el resultado (evaluación). Todo compilador o intérprete hace esto a mayor escala.",
    "resultados": ["Separar una entrada en tokens.", "Interpretar la estructura de una expresión.", "Nombrar las fases de compilación."],
    "temas": [("Análisis léxico", "De texto a tokens"), ("Análisis sintáctico", "Reconocer la estructura"), ("Evaluación", "Producir el resultado")],
    "definiciones": [("Análisis léxico (lexer)", "divide el texto en tokens. Clave: '3 + 4' → [3, +, 4]."), ("Análisis sintáctico (parser)", "reconoce la estructura de los tokens. Clave: expresión = número op número."), ("Evaluación", "calcula el resultado a partir de la estructura. Clave: aplica el operador.")],
    "situacion": "Cuando compilas o ejecutas código, el lenguaje primero lo tokeniza, luego lo parsea y por fin lo evalúa o traduce. Este mini-evaluador muestra esas fases con una operación simple.",
    "entrada": "una línea `a op b` (dos enteros y un operador +, -, *)",
    "salida": "`resultado=<a op b>`",
    "formula": "aplicar el operador a los dos operandos",
    "algoritmo": "TOKENIZAR ; RECONOCER (num op num) ; EVALUAR",
    "casos": [("3 + 4", "resultado=7"), ("10 - 2", "resultado=8"), ("5 * 6", "resultado=30")],
    "comparacion": [("Sintáctica", "Cada lenguaje tokeniza y evalúa a su manera."), ("Semántica", "Las fases son universales: lexer, parser, evaluador."), ("Paradigmática", "SQL evalúa expresiones en la consulta.")],
    "familia": "Todo compilador (gcc, javac, rustc) y todo intérprete (CPython, V8) sigue estas fases.",
    "errores": [("Mezclar léxico con sintaxis", "confundir tokens con estructura", "separar las fases mentalmente"), ("Operador no soportado", "caso sin manejar", "cubrir los operadores esperados")],
    "faq": [("¿Compilar es solo estas fases?", "Son el núcleo; hay más (optimización, generación de código)."), ("¿Un intérprete parsea?", "Sí: también tokeniza y parsea antes de ejecutar.")],
    "reto": "Añade la división entera y resuélvelo en **Python**.",
    "impls": {
        "python": r"""import sys

a, op, b = sys.stdin.readline().split()
a, b = int(a), int(b)
if op == "+":
    r = a + b
elif op == "-":
    r = a - b
else:
    r = a * b
print(f"resultado={r}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const [a, op, b] = readFileSync(0, "utf8").trim().split(/\s+/);
const x = Number(a), y = Number(b);
const r = op === "+" ? x + y : op === "-" ? x - y : x * y;
console.log(`resultado=${r}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const [a, op, b] = readFileSync(0, "utf8").trim().split(/\s+/);
const x = Number(a), y = Number(b);
const r = op === "+" ? x + y : op === "-" ? x - y : x * y;
console.log(`resultado=${r}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        long a = Long.parseLong(t[0]), b = Long.parseLong(t[2]);
        long r = t[1].equals("+") ? a + b : t[1].equals("-") ? a - b : a * b;
        System.out.println("resultado=" + r);
    }
}
""",
        "csharp": r"""using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long a = long.Parse(t[0]), b = long.Parse(t[2]);
long r = t[1] switch { "+" => a + b, "-" => a - b, _ => a * b };
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
	a, _ := strconv.Atoi(t[0])
	b, _ := strconv.Atoi(t[2])
	var r int
	switch t[1] {
	case "+":
		r = a + b
	case "-":
		r = a - b
	default:
		r = a * b
	}
	fmt.Printf("resultado=%d\n", r)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let a: i64 = t[0].parse().unwrap();
    let b: i64 = t[2].parse().unwrap();
    let r = match t[1] {
        "+" => a + b,
        "-" => a - b,
        _ => a * b,
    };
    println!("resultado={r}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long a, b;
    char op;
    if (scanf("%ld %c %ld", &a, &op, &b) != 3) return 1;
    long r = op == '+' ? a + b : op == '-' ? a - b : a * b;
    printf("resultado=%ld\n", r);
    return 0;
}
""",
        "php": r"""<?php
[$a, $op, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;
$r = $op === "+" ? $a + $b : ($op === "-" ? $a - $b : $a * $b);
echo "resultado=$r\n";
""",
        "sql": r"""-- SQL evalúa la expresión según el operador con CASE.
WITH e(a, op, b) AS (VALUES (3, '+', 4))
SELECT printf('resultado=%d', CASE op WHEN '+' THEN a + b WHEN '-' THEN a - b ELSE a * b END) AS resultado
FROM e;
""",
    },
}

S[124] = {
    "descripcion": "Contar cuántos dígitos tiene un entero no negativo.",
    "objetivo": "Diferenciar **compilador, intérprete y JIT** por su forma de ejecutar. El programa (contar dígitos) es el mismo; lo que cambia entre modelos es cuándo y cómo se traduce a instrucciones de la máquina.",
    "resultados": ["Contar dígitos recorriendo el número.", "Explicar compilado, interpretado y JIT.", "Relacionar el modelo con el rendimiento."],
    "temas": [("Compilador", "Traduce antes de ejecutar"), ("Intérprete", "Ejecuta la fuente al vuelo"), ("JIT", "Compila durante la ejecución")],
    "definiciones": [("Compilador", "traduce todo el programa a código máquina antes de ejecutar. Clave: rápido, errores antes."), ("Intérprete", "ejecuta la fuente instrucción a instrucción. Clave: flexible, más lento."), ("JIT", "compila a máquina las partes calientes durante la ejecución. Clave: combina ambos (V8, JVM).")],
    "situacion": "Contar dígitos corre igual en C (compilado), Python (interpretado) y JavaScript (JIT); lo que cambia es el rendimiento y cuándo aparecen los errores, no el resultado.",
    "entrada": "un entero `n` (n >= 0)",
    "salida": "`digitos=<cantidad de dígitos>`",
    "formula": "contar los dígitos de n (0 tiene 1)",
    "algoritmo": "contar dígitos dividiendo por 10 hasta 0 (o longitud del texto)",
    "casos": [("12345", "digitos=5"), ("7", "digitos=1"), ("100", "digitos=3")],
    "comparacion": [("Sintáctica", "Igual en todos: recorrer o medir el número."), ("Semántica", "El modelo de ejecución no cambia el resultado."), ("Paradigmática", "SQL usa length sobre el texto del número.")],
    "familia": "C compila; CPython interpreta bytecode; V8 y la JVM usan JIT. El programa es idéntico.",
    "errores": [("Contar 0 como 0 dígitos", "el 0 tiene un dígito", "tratar el caso n=0"), ("Dividir sin parar", "bucle infinito", "parar cuando el número llega a 0")],
    "faq": [("¿Cuál es más rápido?", "Compilado suele ganar en ejecución; interpretado gana en iteración; JIT busca ambos."), ("¿Python compila?", "A bytecode internamente; luego lo interpreta.")],
    "reto": "Cuenta también la suma de los dígitos y resuélvelo en **Go**.",
    "impls": {
        "python": r"""import sys

n = int(sys.stdin.readline())
print(f"digitos={len(str(n))}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const n = readFileSync(0, "utf8").trim();
console.log(`digitos=${n.length}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const n: string = readFileSync(0, "utf8").trim();
console.log(`digitos=${n.length}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String n = br.readLine().trim();
        System.out.println("digitos=" + n.length());
    }
}
""",
        "csharp": r"""using System;

string n = Console.In.ReadToEnd().Trim();
Console.WriteLine($"digitos={n.Length}");
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
	n := strings.TrimSpace(line)
	fmt.Printf("digitos=%d\n", len(n))
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n = s.trim();
    println!("digitos={}", n.len());
}
""",
        "c": r"""#include <stdio.h>
#include <string.h>

int main(void) {
    char n[64];
    if (scanf("%63s", n) != 1) return 1;
    printf("digitos=%d\n", (int) strlen(n));
    return 0;
}
""",
        "php": r"""<?php
$n = trim(fgets(STDIN));
echo "digitos=" . strlen($n) . "\n";
""",
        "sql": r"""-- SQL: length sobre el texto del número.
WITH nums(n) AS (VALUES ('12345'))
SELECT printf('digitos=%d', length(n)) AS resultado FROM nums;
""",
    },
}

S[125] = {
    "descripcion": "Evaluar una expresión en notación polaca inversa (RPN) 'a b op' con una pila.",
    "objetivo": "Entender el **bytecode y las máquinas virtuales**: una VM ejecuta instրucciones simples sobre una pila. La notación polaca inversa (RPN) es exactamente cómo trabaja una VM de pila: apila operandos y aplica operadores.",
    "resultados": ["Evaluar RPN con una pila.", "Relacionar RPN con las VM de pila.", "Explicar qué es el bytecode."],
    "temas": [("Máquina de pila", "Opera sobre una pila de valores"), ("RPN", "Operandos primero, operador después"), ("Bytecode", "Instrucciones simples para la VM")],
    "definiciones": [("Bytecode", "código intermedio de instrucciones simples que ejecuta una VM. Clave: portable (JVM, CLR)."), ("Máquina virtual de pila", "VM que opera apilando y desapilando valores. Clave: `push 3, push 4, add`."), ("RPN", "notación donde el operador va tras los operandos. Clave: `3 4 +` = 7.")],
    "situacion": "La JVM y el CLR ejecutan bytecode sobre una pila: apilan operandos y aplican operadores. Evaluar '3 4 +' con una pila reproduce ese mecanismo en pequeño.",
    "entrada": "una línea `a b op` (dos enteros y un operador +, -, *)",
    "salida": "`resultado=<a op b>`",
    "formula": "apilar a y b; aplicar op; el tope es el resultado",
    "algoritmo": "PARA cada token: SI número, apilar; SI operador, desapilar 2, aplicar, apilar",
    "casos": [("3 4 +", "resultado=7"), ("5 6 *", "resultado=30"), ("10 2 -", "resultado=8")],
    "comparacion": [("Sintáctica", "Una pila (lista) en cada lenguaje."), ("Semántica", "La VM de pila es el mismo modelo que la JVM/CLR."), ("Paradigmática", "SQL no tiene pila explícita; evalúa la expresión.")],
    "familia": "La JVM (bytecode Java) y el CLR (.NET) son máquinas de pila. Python también usa una VM de pila.",
    "errores": [("Desapilar en orden equivocado", "resta/división invertidas", "el primero desapilado es el segundo operando"), ("Pila vacía al operar", "expresión mal formada", "asumir RPN bien formada")],
    "faq": [("¿Por qué VM de pila?", "Simplicidad y portabilidad: las instrucciones no nombran registros."), ("¿RPN se usa de verdad?", "Sí: calculadoras HP, PostScript y muchas VM internamente.")],
    "reto": "Evalúa una RPN de más operadores (p. ej. '3 4 + 5 *') y resuélvelo en **Python**.",
    "impls": {
        "python": r"""import sys

a, b, op = sys.stdin.readline().split()
pila = [int(a), int(b)]
y = pila.pop()
x = pila.pop()
r = x + y if op == "+" else x - y if op == "-" else x * y
print(f"resultado={r}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const [a, b, op] = readFileSync(0, "utf8").trim().split(/\s+/);
const pila = [Number(a), Number(b)];
const y = pila.pop(), x = pila.pop();
const r = op === "+" ? x + y : op === "-" ? x - y : x * y;
console.log(`resultado=${r}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const [a, b, op] = readFileSync(0, "utf8").trim().split(/\s+/);
const pila: number[] = [Number(a), Number(b)];
const y = pila.pop()!, x = pila.pop()!;
const r = op === "+" ? x + y : op === "-" ? x - y : x * y;
console.log(`resultado=${r}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayDeque;
import java.util.Deque;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        Deque<Long> pila = new ArrayDeque<>();
        pila.push(Long.parseLong(t[0]));
        pila.push(Long.parseLong(t[1]));
        long y = pila.pop(), x = pila.pop();
        long r = t[2].equals("+") ? x + y : t[2].equals("-") ? x - y : x * y;
        System.out.println("resultado=" + r);
    }
}
""",
        "csharp": r"""using System;
using System.Collections.Generic;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var pila = new Stack<long>();
pila.Push(long.Parse(t[0]));
pila.Push(long.Parse(t[1]));
long y = pila.Pop(), x = pila.Pop();
long r = t[2] switch { "+" => x + y, "-" => x - y, _ => x * y };
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
	x, _ := strconv.Atoi(t[0])
	y, _ := strconv.Atoi(t[1])
	var r int
	switch t[2] {
	case "+":
		r = x + y
	case "-":
		r = x - y
	default:
		r = x * y
	}
	fmt.Printf("resultado=%d\n", r)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let mut pila: Vec<i64> = vec![t[0].parse().unwrap(), t[1].parse().unwrap()];
    let y = pila.pop().unwrap();
    let x = pila.pop().unwrap();
    let r = match t[2] {
        "+" => x + y,
        "-" => x - y,
        _ => x * y,
    };
    println!("resultado={r}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long x, y;
    char op;
    if (scanf("%ld %ld %c", &x, &y, &op) != 3) return 1;
    long r = op == '+' ? x + y : op == '-' ? x - y : x * y;
    printf("resultado=%ld\n", r);
    return 0;
}
""",
        "php": r"""<?php
[$a, $b, $op] = preg_split('/\s+/', trim(fgets(STDIN)));
$pila = [(int) $a, (int) $b];
$y = array_pop($pila);
$x = array_pop($pila);
$r = $op === "+" ? $x + $y : ($op === "-" ? $x - $y : $x * $y);
echo "resultado=$r\n";
""",
        "sql": r"""-- SQL: sin pila explícita; evalúa la expresión.
WITH e(x, y, op) AS (VALUES (3, 4, '+'))
SELECT printf('resultado=%d', CASE op WHEN '+' THEN x + y WHEN '-' THEN x - y ELSE x * y END) AS resultado
FROM e;
""",
    },
}

S[126] = {
    "descripcion": "Calcular 2 elevado a n.",
    "objetivo": "Comparar **AOT (compilación anticipada)** con **JIT (compilación en tiempo de ejecución)**. AOT compila todo antes de arrancar (rápido al iniciar); JIT compila sobre la marcha las partes calientes (arranque más lento, luego rápido).",
    "resultados": ["Calcular una potencia de dos.", "Explicar AOT vs. JIT.", "Relacionar el modelo con arranque y rendimiento."],
    "temas": [("AOT", "Compilar todo antes de ejecutar"), ("JIT", "Compilar las partes calientes al vuelo"), ("Arranque vs. pico", "Compromiso entre ambos")],
    "definiciones": [("AOT", "compilación anticipada a código máquina (C, Rust, Go). Clave: arranque instantáneo."), ("JIT", "compilación durante la ejecución de lo más usado (JVM, V8). Clave: se calienta y acelera."), ("Código caliente", "el que se ejecuta muchas veces. Clave: el JIT lo optimiza.")],
    "situacion": "Una herramienta de línea de comandos AOT arranca al instante; un servidor JIT tarda en calentar pero luego es muy rápido. El cálculo (2^n) es el mismo; cambia cuándo se compila.",
    "entrada": "un entero `n` (0 <= n <= 60)",
    "salida": "`resultado=<2^n>`",
    "formula": "2 elevado a n",
    "algoritmo": "multiplicar 2 por sí mismo n veces (o desplazar bits)",
    "casos": [("3", "resultado=8"), ("0", "resultado=1"), ("5", "resultado=32")],
    "comparacion": [("Sintáctica", "Bucle o desplazamiento de bits en cada lenguaje."), ("Semántica", "El resultado no depende del modelo de compilación."), ("Paradigmática", "SQL calcula con una expresión.")],
    "familia": "Go/Rust/C son AOT; la JVM y V8 son JIT; GraalVM ofrece AOT para la JVM.",
    "errores": [("Desbordar con n grande", "2^64 no cabe", "aquí n <= 60"), ("Empezar el acumulador en 0", "siempre daría 0", "iniciar el acumulador de producto en 1")],
    "faq": [("¿AOT o JIT es mejor?", "AOT para arranque rápido y binarios; JIT para procesos largos que se benefician del calentamiento."), ("¿Se pueden combinar?", "Sí: GraalVM y otros ofrecen AOT sobre plataformas JIT.")],
    "reto": "Calcula 2^n con desplazamiento de bits y resuélvelo en **C**.",
    "impls": {
        "python": r"""import sys

n = int(sys.stdin.readline())
print(f"resultado={2 ** n}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let r = 1;
for (let i = 0; i < n; i++) r *= 2;
console.log(`resultado=${r}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let r = 1;
for (let i = 0; i < n; i++) r *= 2;
console.log(`resultado=${r}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        long r = 1;
        for (int i = 0; i < n; i++) r *= 2;
        System.out.println("resultado=" + r);
    }
}
""",
        "csharp": r"""using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long r = 1;
for (int i = 0; i < n; i++) r *= 2;
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
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	var r int64 = 1
	for i := 0; i < n; i++ {
		r *= 2
	}
	fmt.Printf("resultado=%d\n", r)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: u32 = s.trim().parse().unwrap();
    let r: i64 = 2i64.pow(n);
    println!("resultado={r}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 1;
    long r = 1;
    for (int i = 0; i < n; i++) r *= 2;
    printf("resultado=%ld\n", r);
    return 0;
}
""",
        "php": r"""<?php
$n = (int) trim(fgets(STDIN));
$r = 1;
for ($i = 0; $i < $n; $i++) {
    $r *= 2;
}
echo "resultado=$r\n";
""",
        "sql": r"""-- SQL: potencia con un CTE recursivo (ilustrativo, n=3).
WITH RECURSIVE p(i, v) AS (VALUES (0, 1) UNION ALL SELECT i + 1, v * 2 FROM p WHERE i < 3)
SELECT printf('resultado=%d', v) AS resultado FROM p ORDER BY i DESC LIMIT 1;
""",
    },
}

S[127] = {
    "descripcion": "Sumar 1 a n con una función recursiva y reportar la profundidad de la recursión.",
    "objetivo": "Entender la **pila (stack) y el marco de llamada**: cada llamada a función crea un marco con sus variables; la recursión los apila. La profundidad de la recursión es cuántos marcos hay a la vez.",
    "resultados": ["Reconocer la pila de llamadas.", "Relacionar recursión con marcos apilados.", "Explicar el desbordamiento de pila."],
    "temas": [("Pila de llamadas", "Marcos de las funciones activas"), ("Marco de llamada", "Variables y retorno de una llamada"), ("Profundidad", "Cuántos marcos hay a la vez")],
    "definiciones": [("Pila (stack)", "región de memoria para los marcos de llamada. Clave: LIFO, rápida."), ("Marco de llamada", "espacio de una llamada: parámetros, locales, dirección de retorno. Clave: se apila al llamar."), ("Desbordamiento de pila", "cuando hay demasiados marcos. Clave: recursión muy profunda lo causa.")],
    "situacion": "Cada llamada recursiva apila un marco; sumar 1..n con recursión usa n marcos a la vez. Si n es enorme, la pila se desborda. La pila explica cómo el programa recuerda dónde volver.",
    "entrada": "un entero `n` (1 <= n <= 1000)",
    "salida": "`suma=<1+...+n> profundidad=<n>`",
    "formula": "suma recursiva; profundidad = número de marcos = n",
    "algoritmo": "sumar(n) = n + sumar(n-1) ; sumar(0) = 0 ; profundidad = n",
    "casos": [("5", "suma=15 profundidad=5"), ("3", "suma=6 profundidad=3"), ("1", "suma=1 profundidad=1")],
    "comparacion": [("Sintáctica", "Función recursiva en cada lenguaje."), ("Semántica", "Cada llamada apila un marco; el retorno lo desapila."), ("Paradigmática", "SQL usa recursión con CTE, sin pila visible.")],
    "familia": "En Haskell la recursión es el modo natural de iterar; la recursión de cola puede optimizarse a un bucle.",
    "errores": [("Recursión sin caso base", "desbordamiento de pila", "definir el caso base"), ("Recursión demasiado profunda", "límite de pila", "usar iteración o recursión de cola para n enorme")],
    "faq": [("¿Por qué existe la pila?", "Para recordar dónde volver y los datos locales de cada llamada."), ("¿Stack o heap?", "La pila guarda marcos (rápida, automática); el heap, datos de vida flexible.")],
    "reto": "Convierte la suma recursiva en recursión de cola y resuélvelo en **Rust**.",
    "impls": {
        "python": r"""import sys

sys.setrecursionlimit(5000)


def sumar(n):
    return 0 if n == 0 else n + sumar(n - 1)


n = int(sys.stdin.readline())
print(f"suma={sumar(n)} profundidad={n}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

function sumar(n) {
  return n === 0 ? 0 : n + sumar(n - 1);
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`suma=${sumar(n)} profundidad=${n}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

function sumar(n: number): number {
  return n === 0 ? 0 : n + sumar(n - 1);
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`suma=${sumar(n)} profundidad=${n}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static long sumar(int n) {
        return n == 0 ? 0 : n + sumar(n - 1);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        System.out.println("suma=" + sumar(n) + " profundidad=" + n);
    }
}
""",
        "csharp": r"""using System;

long Sumar(int n) => n == 0 ? 0 : n + Sumar(n - 1);

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"suma={Sumar(n)} profundidad={n}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func sumar(n int) int64 {
	if n == 0 {
		return 0
	}
	return int64(n) + sumar(n-1)
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	fmt.Printf("suma=%d profundidad=%d\n", sumar(n), n)
}
""",
        "rust": r"""use std::io::Read;

fn sumar(n: i64) -> i64 {
    if n == 0 {
        0
    } else {
        n + sumar(n - 1)
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("suma={} profundidad={}", sumar(n), n);
}
""",
        "c": r"""#include <stdio.h>

long sumar(long n) {
    return n == 0 ? 0 : n + sumar(n - 1);
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("suma=%ld profundidad=%ld\n", sumar(n), n);
    return 0;
}
""",
        "php": r"""<?php
function sumar($n) {
    return $n === 0 ? 0 : $n + sumar($n - 1);
}

$n = (int) trim(fgets(STDIN));
echo "suma=" . sumar($n) . " profundidad=$n\n";
""",
        "sql": r"""-- SQL: recursión con CTE (ilustrativo, n=5).
WITH RECURSIVE r(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM r WHERE i < 5)
SELECT printf('suma=%d profundidad=%d', sum(i), max(i)) AS resultado FROM r;
""",
    },
}

S[128] = {
    "descripcion": "Construir dinámicamente una lista descendente de n a 1.",
    "objetivo": "Entender el **heap y la asignación dinámica**: cuando el tamaño de los datos no se conoce en compilación, se reservan en el heap. Una lista dinámica que crece con n vive en el heap.",
    "resultados": ["Construir una estructura de tamaño dinámico.", "Distinguir stack de heap.", "Reconocer la asignación dinámica."],
    "temas": [("Heap", "Memoria de vida y tamaño flexibles"), ("Asignación dinámica", "Reservar en ejecución"), ("Stack vs. heap", "Automático vs. gestionado")],
    "definiciones": [("Heap", "región de memoria para datos de tamaño/vida no conocidos en compilación. Clave: más flexible que la pila."), ("Asignación dinámica", "reservar memoria en ejecución (una lista que crece). Clave: heap."), ("Stack vs. heap", "la pila es automática y rápida; el heap es flexible pero requiere gestión. Clave: distinto uso.")],
    "situacion": "Una lista cuyo tamaño depende de la entrada (n) no cabe en la pila con tamaño fijo: se asigna en el heap. Casi todas las colecciones dinámicas viven ahí.",
    "entrada": "un entero `n` (n >= 1)",
    "salida": "`lista=<n-(n-1)-...-1>`",
    "formula": "lista dinámica con los valores de n a 1",
    "algoritmo": "reservar lista ; añadir n, n-1, ..., 1 ; unir por -",
    "casos": [("3", "lista=3-2-1"), ("1", "lista=1"), ("5", "lista=5-4-3-2-1")],
    "comparacion": [("Sintáctica", "list/Vec/ArrayList (heap) en cada lenguaje."), ("Semántica", "El tamaño dinámico obliga al heap; C usa malloc."), ("Paradigmática", "SQL genera la secuencia con un CTE.")],
    "familia": "En C la lista dinámica se hace con malloc/realloc; en los demás, las colecciones ya viven en el heap.",
    "errores": [("Asumir tamaño fijo", "no cabe en la pila", "usar una estructura dinámica"), ("Fugas al no liberar (C)", "memoria perdida", "liberar con free lo asignado")],
    "faq": [("¿Todo va al heap?", "No: los locales pequeños van a la pila; lo dinámico o grande, al heap."), ("¿El heap es más lento?", "Su asignación cuesta más que la pila, pero permite tamaños flexibles.")],
    "reto": "Construye la lista ascendente y descendente a la vez y resuélvelo en **Go**.",
    "impls": {
        "python": r"""import sys

n = int(sys.stdin.readline())
lista = []
for i in range(n, 0, -1):
    lista.append(i)
print("lista=" + "-".join(str(x) for x in lista))
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const lista = [];
for (let i = n; i >= 1; i--) lista.push(i);
console.log(`lista=${lista.join("-")}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const lista: number[] = [];
for (let i = n; i >= 1; i--) lista.push(i);
console.log(`lista=${lista.join("-")}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        List<Integer> lista = new ArrayList<>();
        for (int i = n; i >= 1; i--) lista.add(i);
        System.out.println("lista=" + lista.stream().map(String::valueOf).collect(Collectors.joining("-")));
    }
}
""",
        "csharp": r"""using System;
using System.Collections.Generic;

int n = int.Parse(Console.In.ReadToEnd().Trim());
var lista = new List<int>();
for (int i = n; i >= 1; i--) lista.Add(i);
Console.WriteLine($"lista={string.Join("-", lista)}");
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
	var lista []string
	for i := n; i >= 1; i-- {
		lista = append(lista, strconv.Itoa(i))
	}
	fmt.Printf("lista=%s\n", strings.Join(lista, "-"))
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let lista: Vec<String> = (1..=n).rev().map(|x| x.to_string()).collect();
    println!("lista={}", lista.join("-"));
}
""",
        "c": r"""#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long *lista = malloc(n * sizeof(long));
    for (long i = 0; i < n; i++) lista[i] = n - i;
    printf("lista=");
    for (long i = 0; i < n; i++) {
        if (i > 0) printf("-");
        printf("%ld", lista[i]);
    }
    printf("\n");
    free(lista);
    return 0;
}
""",
        "php": r"""<?php
$n = (int) trim(fgets(STDIN));
$lista = [];
for ($i = $n; $i >= 1; $i--) {
    $lista[] = $i;
}
echo "lista=" . implode("-", $lista) . "\n";
""",
        "sql": r"""-- SQL: genera la secuencia descendente con un CTE (ilustrativo, n=3).
WITH RECURSIVE r(i) AS (VALUES (3) UNION ALL SELECT i - 1 FROM r WHERE i > 1)
SELECT 'lista=' || group_concat(i, '-') AS resultado FROM r;
""",
    },
}

S[129] = {
    "descripcion": "Dado un índice y una lista, devolver el elemento en esa posición (acceso indirecto).",
    "objetivo": "Entender **referencias, apuntadores y direcciones**: acceder a un dato a través de su posición o dirección, no directamente. Indexar una lista es aritmética de direcciones: base + índice.",
    "resultados": ["Acceder a un elemento por su índice.", "Explicar la indirección (referencia/puntero).", "Relacionar el índice con la dirección."],
    "temas": [("Indirección", "Acceder a través de una posición"), ("Índice como dirección", "base + desplazamiento"), ("Referencia vs. puntero", "Ambos apuntan a un dato")],
    "definiciones": [("Referencia", "un valor que designa a otro dato. Clave: acceso indirecto."), ("Puntero", "referencia explícita que guarda una dirección (C). Clave: `arr + i` = dirección del elemento i."), ("Índice", "posición dentro de una secuencia. Clave: equivale a un desplazamiento desde la base.")],
    "situacion": "`arr[i]` en el fondo es 've a la dirección base más i posiciones'. Los punteros de C hacen esa aritmética explícita; los índices la esconden. Ambos son indirección.",
    "entrada": "una línea `indice v0 v1 v2 ...` (el primero es el índice, base 0)",
    "salida": "`valor=<elemento en esa posición>`",
    "formula": "valor = lista[indice]",
    "algoritmo": "LEER indice y lista ; ESCRIBIR lista[indice]",
    "casos": [("1 10 20 30", "valor=20"), ("0 5 6 7", "valor=5"), ("2 100 200 300", "valor=300")],
    "comparacion": [("Sintáctica", "`arr[i]` en casi todos; en C, también `*(arr + i)`."), ("Semántica", "El índice se traduce a una dirección de memoria."), ("Paradigmática", "SQL accede por condición, no por índice.")],
    "familia": "En C `arr[i]` y `*(arr+i)` son equivalentes: puro puntero. En los demás, el índice abstrae la dirección.",
    "errores": [("Índice fuera de rango", "acceso inválido", "verificar que 0 <= i < tamaño"), ("Confundir el valor con su dirección", "usar el puntero como valor", "desreferenciar para obtener el valor")],
    "faq": [("¿Referencia o puntero?", "El puntero es una referencia explícita con aritmética; la referencia suele ser más segura."), ("¿arr[i] es un puntero?", "En C sí, por debajo; en otros lenguajes el índice abstrae la dirección.")],
    "reto": "Devuelve el elemento y su vecino derecho y resuélvelo en **C** con aritmética de punteros.",
    "impls": {
        "python": r"""import sys

t = sys.stdin.read().split()
indice = int(t[0])
lista = [int(x) for x in t[1:]]
print(f"valor={lista[indice]}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const t = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const indice = t[0];
const lista = t.slice(1);
console.log(`valor=${lista[indice]}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const t: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const indice = t[0];
const lista = t.slice(1);
console.log(`valor=${lista[indice]}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        int indice = Integer.parseInt(t[0]);
        System.out.println("valor=" + Integer.parseInt(t[indice + 1]));
    }
}
""",
        "csharp": r"""using System;
using System.Linq;

int[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
    .Select(int.Parse).ToArray();
int indice = t[0];
Console.WriteLine($"valor={t[indice + 1]}");
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
	indice, _ := strconv.Atoi(t[0])
	lista := t[1:]
	fmt.Printf("valor=%s\n", lista[indice])
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let indice: usize = t[0].parse().unwrap();
    let lista = &t[1..];
    println!("valor={}", lista[indice]);
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    long indice = v[0];
    long *lista = v + 1; /* aritmética de punteros */
    printf("valor=%ld\n", *(lista + indice));
    return 0;
}
""",
        "php": r"""<?php
$t = preg_split('/\s+/', trim(fgets(STDIN)));
$indice = (int) $t[0];
$lista = array_slice($t, 1);
echo "valor={$lista[$indice]}\n";
""",
        "sql": r"""-- SQL: acceso por posición con una subconsulta ordenada (ilustrativo).
WITH datos(pos, x) AS (VALUES (0, 10), (1, 20), (2, 30))
SELECT printf('valor=%d', x) AS resultado FROM datos WHERE pos = 1;
""",
    },
}

S[130] = {
    "descripcion": "Reservar dinámicamente un arreglo de n enteros, llenarlo de 1 a n, sumarlo y liberarlo.",
    "objetivo": "Practicar la **gestión manual de memoria** de C: reservar con malloc, usar y liberar con free. En los lenguajes con recolector esto es automático; en C es responsabilidad del programador.",
    "resultados": ["Reservar y liberar memoria (concepto).", "Explicar malloc/free.", "Contrastar con la gestión automática."],
    "temas": [("malloc/free", "Reservar y liberar a mano"), ("Responsabilidad", "Liberar lo que reservas"), ("Fugas y dobles liberaciones", "Los peligros")],
    "definiciones": [("malloc", "reserva un bloque de memoria en el heap (C). Clave: devuelve un puntero."), ("free", "libera un bloque previamente reservado. Clave: olvidarlo causa fugas."), ("Fuga de memoria", "memoria reservada que nunca se libera. Clave: el programa la va acumulando.")],
    "situacion": "En C, cada malloc necesita su free; olvidarlo es una fuga, liberar dos veces es un error grave. Los lenguajes con GC hacen esto por ti, a cambio de menos control.",
    "entrada": "un entero `n` (n >= 1)",
    "salida": "`reservado=<n> suma=<1+...+n>`",
    "formula": "reservar n enteros, llenarlos 1..n, sumar, liberar",
    "algoritmo": "reservar(n) ; llenar 1..n ; sumar ; liberar",
    "casos": [("5", "reservado=5 suma=15"), ("1", "reservado=1 suma=1"), ("3", "reservado=3 suma=6")],
    "comparacion": [("Sintáctica", "malloc/free (C); las colecciones automáticas en los demás."), ("Semántica", "C libera a mano; GC/ownership liberan por ti."), ("Paradigmática", "SQL no expone gestión de memoria.")],
    "familia": "C y C++ (con new/delete) gestionan a mano; Rust automatiza vía ownership sin GC; el resto usa GC.",
    "errores": [("Olvidar free", "fuga de memoria", "liberar todo lo reservado"), ("Usar tras liberar", "use-after-free", "no acceder a memoria ya liberada")],
    "faq": [("¿Por qué gestionar a mano?", "Control fino y rendimiento predecible, a cambio de responsabilidad."), ("¿El GC elimina las fugas?", "Las de memoria en gran medida, pero no las de otros recursos (archivos, sockets).")],
    "reto": "Reserva, redimensiona con realloc y libera; resuélvelo en **C**.",
    "impls": {
        "python": r"""import sys

n = int(sys.stdin.readline())
arr = [0] * n  # el runtime gestiona la memoria
for i in range(n):
    arr[i] = i + 1
print(f"reservado={n} suma={sum(arr)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const arr = new Array(n);
for (let i = 0; i < n; i++) arr[i] = i + 1;
console.log(`reservado=${n} suma=${arr.reduce((a, b) => a + b, 0)}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const arr: number[] = new Array(n);
for (let i = 0; i < n; i++) arr[i] = i + 1;
console.log(`reservado=${n} suma=${arr.reduce((a, b) => a + b, 0)}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int[] arr = new int[n];
        long suma = 0;
        for (int i = 0; i < n; i++) {
            arr[i] = i + 1;
            suma += arr[i];
        }
        System.out.println("reservado=" + n + " suma=" + suma);
    }
}
""",
        "csharp": r"""using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int[] arr = new int[n];
long suma = 0;
for (int i = 0; i < n; i++) {
    arr[i] = i + 1;
    suma += arr[i];
}
Console.WriteLine($"reservado={n} suma={suma}");
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
	arr := make([]int, n)
	suma := 0
	for i := 0; i < n; i++ {
		arr[i] = i + 1
		suma += arr[i]
	}
	fmt.Printf("reservado=%d suma=%d\n", n, suma)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let arr: Vec<i64> = (1..=n).collect(); // Vec libera al salir del ámbito
    let suma: i64 = arr.iter().sum();
    println!("reservado={n} suma={suma}");
}
""",
        "c": r"""#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long *arr = malloc(n * sizeof(long));
    long suma = 0;
    for (long i = 0; i < n; i++) {
        arr[i] = i + 1;
        suma += arr[i];
    }
    printf("reservado=%ld suma=%ld\n", n, suma);
    free(arr);
    return 0;
}
""",
        "php": r"""<?php
$n = (int) trim(fgets(STDIN));
$arr = array_fill(0, $n, 0);
for ($i = 0; $i < $n; $i++) {
    $arr[$i] = $i + 1;
}
echo "reservado=$n suma=" . array_sum($arr) . "\n";
""",
        "sql": r"""-- SQL no expone la gestión de memoria; se calcula la suma.
WITH RECURSIVE r(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM r WHERE i < 5)
SELECT printf('reservado=%d suma=%d', max(i), sum(i)) AS resultado FROM r;
""",
    },
}

S[131] = {
    "descripcion": "Crear n objetos temporales y confirmar que, al no quedar referencias, la memoria se recolecta.",
    "objetivo": "Entender la **recolección de basura (GC)**: el runtime libera automáticamente la memoria de los objetos que ya no son alcanzables. El programador no llama a free; el GC lo hace.",
    "resultados": ["Explicar qué es la recolección de basura.", "Reconocer objetos inalcanzables.", "Contrastar GC con gestión manual."],
    "temas": [("Recolector de basura", "Libera lo inalcanzable"), ("Alcanzabilidad", "Si algo aún se puede usar"), ("Pausas del GC", "Coste del automatismo")],
    "definiciones": [("Recolección de basura", "liberación automática de objetos ya inalcanzables. Clave: sin free manual."), ("Alcanzable", "objeto accesible desde una variable viva. Clave: lo inalcanzable es basura."), ("Pausa del GC", "momento en que el recolector trabaja. Clave: puede introducir latencia.")],
    "situacion": "En Java, Python o Go creas objetos y los olvidas: el GC recupera su memoria cuando ya nadie los referencia. Cómodo, pero introduce pausas impredecibles.",
    "entrada": "un entero `n` (número de objetos temporales)",
    "salida": "`creados=<n> estado=recolectado`",
    "formula": "crear n objetos temporales; al perder la referencia, se recolectan",
    "algoritmo": "crear n objetos ; descartar referencias ; el GC recolecta",
    "casos": [("5", "creados=5 estado=recolectado"), ("0", "creados=0 estado=recolectado"), ("3", "creados=3 estado=recolectado")],
    "comparacion": [("Sintáctica", "No hay free: se crean objetos y se olvidan."), ("Semántica", "GC (Java/Python/Go) vs. ownership (Rust) vs. manual (C)."), ("Paradigmática", "SQL no expone memoria.")],
    "familia": "Java, C#, Go, Python, JS usan GC. Rust evita el GC con ownership; C es manual.",
    "errores": [("Confiar en el GC para recursos no-memoria", "archivos/sockets sin cerrar", "cerrar explícitamente esos recursos"), ("Retener referencias sin querer", "fuga lógica: el GC no libera lo aún referenciado", "soltar las referencias que ya no usas")],
    "faq": [("¿El GC elimina toda fuga?", "Las de memoria en su mayoría; no las lógicas (referencias retenidas) ni otros recursos."), ("¿GC o sin GC?", "GC da comodidad; sin GC (Rust/C) da control y latencia predecible.")],
    "reto": "Retén una referencia a un objeto e ilustra por qué el GC no lo libera; resuélvelo en **Python**.",
    "impls": {
        "python": r"""import sys

n = int(sys.stdin.readline())
for _ in range(n):
    _tmp = object()  # temporal; sin referencia persistente, se recolecta
print(f"creados={n} estado=recolectado")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
for (let i = 0; i < n; i++) {
  const tmp = {}; // sin referencia persistente, será recolectado
  void tmp;
}
console.log(`creados=${n} estado=recolectado`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
for (let i = 0; i < n; i++) {
  const tmp: Record<string, unknown> = {};
  void tmp;
}
console.log(`creados=${n} estado=recolectado`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        for (int i = 0; i < n; i++) {
            Object tmp = new Object(); // el GC lo recolectará
            if (tmp == null) return;
        }
        System.out.println("creados=" + n + " estado=recolectado");
    }
}
""",
        "csharp": r"""using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
for (int i = 0; i < n; i++) {
    var tmp = new object(); // el GC lo recolectará
    if (tmp == null) return;
}
Console.WriteLine($"creados={n} estado=recolectado");
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
	for i := 0; i < n; i++ {
		tmp := new(int) // sin referencia persistente, el GC lo recolecta
		_ = tmp
	}
	fmt.Printf("creados=%d estado=recolectado\n", n)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    for _ in 0..n {
        let _tmp = Box::new(0); // se libera al salir del ámbito (sin GC)
    }
    println!("creados={n} estado=recolectado");
}
""",
        "c": r"""#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    for (long i = 0; i < n; i++) {
        long *tmp = malloc(sizeof(long)); /* en C se libera a mano */
        free(tmp);
    }
    printf("creados=%ld estado=recolectado\n", n);
    return 0;
}
""",
        "php": r"""<?php
$n = (int) trim(fgets(STDIN));
for ($i = 0; $i < $n; $i++) {
    $tmp = new stdClass(); // recolectado por conteo de referencias
    unset($tmp);
}
echo "creados=$n estado=recolectado\n";
""",
        "sql": r"""-- SQL no expone la memoria; se informa el conteo.
WITH nums(n) AS (VALUES (5), (0), (3))
SELECT printf('creados=%d estado=recolectado', n) AS resultado FROM nums;
""",
    },
}

S[132] = {
    "descripcion": "Calcular el doble de un valor prestándolo (borrow) sin tomar su propiedad, ilustrando RAII y préstamos.",
    "objetivo": "Entender **RAII, propiedad y préstamos** como alternativa al GC. En Rust, un valor tiene un dueño y puede prestarse para leerlo sin copiarlo ni transferir la propiedad; se libera determinísticamente al salir del ámbito.",
    "resultados": ["Explicar propiedad y préstamo.", "Leer un valor prestado sin poseerlo.", "Contrastar RAII con el GC."],
    "temas": [("Propiedad", "Un dueño por valor"), ("Préstamo", "Usar sin poseer"), ("RAII", "Liberar al salir del ámbito")],
    "definiciones": [("RAII", "la vida del recurso se ata a la del objeto dueño. Clave: liberación determinista, sin GC."), ("Propiedad", "cada valor tiene un dueño responsable de liberarlo. Clave: base de Rust."), ("Préstamo", "referencia temporal para leer/usar sin tomar la propiedad. Clave: `&valor`.")],
    "situacion": "Rust libera memoria sin recolector: el dueño la libera al salir del ámbito (RAII) y los préstamos permiten leer sin copiar. El resultado es memoria segura sin pausas de GC.",
    "entrada": "un entero `n`",
    "salida": "`resultado=<2n>`",
    "formula": "prestar n a una función que devuelve 2n",
    "algoritmo": "prestar n (referencia) a doble(&n) ; ESCRIBIR resultado",
    "casos": [("5", "resultado=10"), ("0", "resultado=0"), ("7", "resultado=14")],
    "comparacion": [("Sintáctica", "`&valor` (Rust/C++) vs. paso normal en los demás."), ("Semántica", "Rust libera determinísticamente sin GC; el préstamo no copia."), ("Paradigmática", "SQL no expone propiedad de memoria.")],
    "familia": "C++ tiene RAII y referencias; Rust lo lleva más lejos comprobando los préstamos en compilación.",
    "errores": [("Prestar y mover a la vez (Rust)", "conflicto de préstamos", "elegir prestar o mover, no ambos a la vez"), ("Depender del GC donde hay RAII", "esperar pausas donde no las hay", "aprovechar la liberación determinista")],
    "faq": [("¿RAII o GC?", "RAII da liberación predecible sin pausas; el GC da comodidad. Distintos compromisos."), ("¿Prestar copia el dato?", "No: un préstamo es una referencia; no duplica.")],
    "reto": "Presta el valor a dos funciones distintas y resuélvelo en **Rust**.",
    "impls": {
        "python": r"""import sys


def doble(x):
    return x * 2


n = int(sys.stdin.readline())
print(f"resultado={doble(n)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const doble = (x) => x * 2;
const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${doble(n)}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const doble = (x: number): number => x * 2;
const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${doble(n)}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static long doble(long x) { return x * 2; }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        System.out.println("resultado=" + doble(n));
    }
}
""",
        "csharp": r"""using System;

long Doble(long x) => x * 2;

long n = long.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"resultado={Doble(n)}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func doble(x int64) int64 { return x * 2 }

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	fmt.Printf("resultado=%d\n", doble(n))
}
""",
        "rust": r"""use std::io::Read;

fn doble(x: &i64) -> i64 {
    *x * 2 // préstamo: se lee sin tomar la propiedad
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("resultado={}", doble(&n));
}
""",
        "c": r"""#include <stdio.h>

long doble(const long *x) {
    return *x * 2; /* se accede por referencia sin copiar */
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("resultado=%ld\n", doble(&n));
    return 0;
}
""",
        "php": r"""<?php
function doble($x) {
    return $x * 2;
}

$n = (int) trim(fgets(STDIN));
echo "resultado=" . doble($n) . "\n";
""",
        "sql": r"""-- SQL no expone propiedad de memoria; se calcula el resultado.
WITH nums(n) AS (VALUES (5), (0), (7))
SELECT printf('resultado=%d', n * 2) AS resultado FROM nums;
""",
    },
}

S[133] = {
    "descripcion": "Contar los elementos de una lista usando un acumulador compartido, como visión de la memoria compartida.",
    "objetivo": "Introducir la **concurrencia con memoria compartida**: varios hilos acceden a los mismos datos. Contar con un acumulador compartido ilustra el modelo; en concurrencia real, ese acceso debe protegerse.",
    "resultados": ["Contar con un acumulador compartido.", "Explicar procesos, hilos y memoria compartida.", "Reconocer el riesgo de acceso concurrente."],
    "temas": [("Proceso vs. hilo", "Aislado vs. comparte memoria"), ("Memoria compartida", "Varios hilos, mismos datos"), ("Protección", "Evitar el acceso simultáneo inseguro")],
    "definiciones": [("Proceso", "programa en ejecución con su propia memoria aislada. Clave: no comparte por defecto."), ("Hilo", "línea de ejecución dentro de un proceso; comparte su memoria. Clave: acceso concurrente a los datos."), ("Memoria compartida", "datos accesibles por varios hilos. Clave: requiere sincronización para ser segura.")],
    "situacion": "Los hilos de un proceso comparten memoria: es rápido comunicar, pero peligroso si dos escriben a la vez el mismo dato. Contar con un acumulador es el ejemplo de un estado compartido.",
    "entrada": "una línea con enteros separados por espacio",
    "salida": "`cuenta=<número de elementos>`",
    "formula": "acumulador compartido que cuenta los elementos",
    "algoritmo": "cuenta <- 0 ; PARA CADA elemento: cuenta <- cuenta + 1",
    "casos": [("1 2 3", "cuenta=3"), ("5", "cuenta=1"), ("10 20 30 40", "cuenta=4")],
    "comparacion": [("Sintáctica", "Un contador compartido en cada lenguaje."), ("Semántica", "Con hilos reales haría falta un mutex; aquí es secuencial."), ("Paradigmática", "SQL delega el paralelismo al motor.")],
    "familia": "Java/C#/C++ comparten memoria entre hilos (con locks); Go y Erlang prefieren comunicar en vez de compartir.",
    "errores": [("Compartir sin sincronizar", "condiciones de carrera", "proteger el acceso con mutex o preferir mensajes"), ("Sobre-sincronizar", "cuellos de botella", "minimizar la sección crítica")],
    "faq": [("¿Compartir memoria o comunicar?", "'No comuniques compartiendo memoria; comparte comunicando' (lema de Go)."), ("¿Proceso o hilo?", "Hilo para compartir datos rápido; proceso para aislar y ser robusto.")],
    "reto": "Cuenta en dos hilos y combina con un mutex; resuélvelo en **Go** con canales.",
    "impls": {
        "python": r"""import sys

nums = sys.stdin.read().split()
cuenta = 0
for _ in nums:
    cuenta += 1  # acumulador compartido
print(f"cuenta={cuenta}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/);
let cuenta = 0;
for (const _ of nums) cuenta += 1;
console.log(`cuenta=${cuenta}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const nums: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
let cuenta = 0;
for (const _ of nums) cuenta += 1;
console.log(`cuenta=${cuenta}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] nums = br.readLine().trim().split("\\s+");
        int cuenta = 0;
        for (String s : nums) cuenta += 1;
        System.out.println("cuenta=" + cuenta);
    }
}
""",
        "csharp": r"""using System;

string[] nums = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int cuenta = 0;
foreach (var s in nums) cuenta += 1;
Console.WriteLine($"cuenta={cuenta}");
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
	cuenta := 0
	for range strings.Fields(line) {
		cuenta++
	}
	fmt.Printf("cuenta=%d\n", cuenta)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut cuenta = 0;
    for _ in s.split_whitespace() {
        cuenta += 1;
    }
    println!("cuenta={cuenta}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long x;
    int cuenta = 0;
    while (scanf("%ld", &x) == 1) cuenta++;
    printf("cuenta=%d\n", cuenta);
    return 0;
}
""",
        "php": r"""<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$cuenta = 0;
foreach ($nums as $_) {
    $cuenta += 1;
}
echo "cuenta=$cuenta\n";
""",
        "sql": r"""-- SQL: COUNT sobre las filas.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT printf('cuenta=%d', count(*)) AS resultado FROM nums;
""",
    },
}

S[134] = {
    "descripcion": "Encontrar el máximo de una lista pasando los valores por un canal (productor/consumidor).",
    "objetivo": "Introducir **tareas, corrutinas y canales**: en vez de compartir memoria, las tareas se comunican enviando datos por canales. Un productor envía los valores y un consumidor calcula el máximo.",
    "resultados": ["Comunicar datos por un canal (concepto).", "Separar productor de consumidor.", "Contrastar canales con memoria compartida."],
    "temas": [("Canal", "Tubería entre tareas"), ("Productor/consumidor", "Uno envía, otro recibe"), ("Corrutina/goroutine", "Tarea ligera")],
    "definiciones": [("Canal", "conducto para enviar datos entre tareas concurrentes. Clave: comunicar sin compartir memoria."), ("Corrutina/goroutine", "tarea ligera que el runtime planifica. Clave: miles a bajo coste (Go)."), ("Productor/consumidor", "un patrón: una tarea produce datos, otra los consume. Clave: se coordinan por el canal.")],
    "situacion": "En Go, un productor manda los números por un canal y un consumidor los procesa; no comparten variables, se comunican. Calcular el máximo así modela ese flujo.",
    "entrada": "una línea con enteros separados por espacio",
    "salida": "`max=<el mayor>`",
    "formula": "enviar los valores por un canal; el consumidor guarda el máximo",
    "algoritmo": "productor envía cada valor ; consumidor actualiza el máximo",
    "casos": [("3 1 4", "max=4"), ("5", "max=5"), ("10 20 5", "max=20")],
    "comparacion": [("Sintáctica", "canales (Go), colas/streams (otros), simple recorrido aquí."), ("Semántica", "Comunicar por canal evita compartir estado mutable."), ("Paradigmática", "SQL usa MAX; el motor decide el cómo.")],
    "familia": "Go (canales) y Kotlin (corrutinas + channels) son referentes; también las colas concurrentes en Java.",
    "errores": [("Bloquearse esperando un canal", "deadlock", "cerrar el canal o usar tamaño/estructura adecuada"), ("Compartir estado además del canal", "condiciones de carrera", "comunicar solo por el canal")],
    "faq": [("¿Canal o memoria compartida?", "El canal evita muchos errores de concurrencia al no compartir estado."), ("¿Corrutina es un hilo?", "Es más ligera: muchas corrutinas se multiplexan sobre pocos hilos.")],
    "reto": "Usa un canal real con una goroutine productora y resuélvelo en **Go**.",
    "impls": {
        "python": r"""import sys

nums = [int(x) for x in sys.stdin.read().split()]
maximo = nums[0]
for x in nums:  # consumidor
    if x > maximo:
        maximo = x
print(f"max={maximo}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let maximo = nums[0];
for (const x of nums) if (x > maximo) maximo = x;
console.log(`max=${maximo}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let maximo = nums[0];
for (const x of nums) if (x > maximo) maximo = x;
console.log(`max=${maximo}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int maximo = Integer.parseInt(p[0]);
        for (String s : p) maximo = Math.max(maximo, Integer.parseInt(s));
        System.out.println("max=" + maximo);
    }
}
""",
        "csharp": r"""using System;
using System.Linq;

int[] nums = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
    .Select(int.Parse).ToArray();
Console.WriteLine($"max={nums.Max()}");
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
	ch := make(chan int, len(f))
	go func() { // productor
		for _, s := range f {
			n, _ := strconv.Atoi(s)
			ch <- n
		}
		close(ch)
	}()
	primero := true
	maximo := 0
	for x := range ch { // consumidor
		if primero || x > maximo {
			maximo = x
			primero = false
		}
	}
	fmt.Printf("max=%d\n", maximo)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let maximo = *nums.iter().max().unwrap();
    println!("max={maximo}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long x, maximo;
    if (scanf("%ld", &maximo) != 1) return 1;
    while (scanf("%ld", &x) == 1) {
        if (x > maximo) maximo = x;
    }
    printf("max=%ld\n", maximo);
    return 0;
}
""",
        "php": r"""<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "max=" . max($nums) . "\n";
""",
        "sql": r"""-- SQL: MAX agrega sobre las filas.
WITH nums(x) AS (VALUES (3), (1), (4))
SELECT printf('max=%d', max(x)) AS resultado FROM nums;
""",
    },
}

S[135] = {
    "descripcion": "Sumar una lista enviando cada número como mensaje a un actor acumulador.",
    "objetivo": "Introducir el **modelo de actores y el paso de mensajes** (la máquina BEAM de Erlang/Elixir): actores aislados sin memoria compartida que se comunican por mensajes. Un actor acumula la suma recibiendo un mensaje por número.",
    "resultados": ["Explicar el modelo de actores.", "Simular el paso de mensajes.", "Contrastar actores con memoria compartida."],
    "temas": [("Actor", "Proceso aislado con estado propio"), ("Mensaje", "Única forma de comunicarse"), ("Sin memoria compartida", "No hay condiciones de carrera")],
    "definiciones": [("Actor", "unidad concurrente con estado propio que solo se comunica por mensajes. Clave: aislamiento."), ("Paso de mensajes", "enviar datos a un actor en vez de compartir memoria. Clave: sin carreras."), ("BEAM", "la máquina virtual de Erlang/Elixir, optimizada para millones de actores. Clave: tolerancia a fallos.")],
    "situacion": "En Erlang/Elixir no hay memoria compartida: cada actor tiene su estado y recibe mensajes. Un actor 'acumulador' suma cada número que le llega, sin riesgo de condiciones de carrera.",
    "entrada": "una línea con enteros separados por espacio",
    "salida": "`total=<suma de todos>`",
    "formula": "cada número es un mensaje al actor; el actor acumula",
    "algoritmo": "PARA CADA número: enviar mensaje al actor ; el actor suma a su estado",
    "casos": [("1 2 3", "total=6"), ("5", "total=5"), ("10 20", "total=30")],
    "comparacion": [("Sintáctica", "En el núcleo se simula con una función que acumula; en Elixir, un proceso real."), ("Semántica", "El actor no comparte estado: recibe mensajes uno a uno."), ("Paradigmática", "SQL agrega sin actores.")],
    "familia": "Erlang y Elixir (BEAM) son los referentes; también Akka (JVM) y el modelo de actores en muchos frameworks.",
    "errores": [("Compartir estado entre actores", "rompe el aislamiento", "comunicar solo por mensajes"), ("Buzón que crece sin control", "actor saturado", "procesar los mensajes a ritmo suficiente")],
    "faq": [("¿Actor o hilo?", "El actor no comparte memoria: se comunica por mensajes, evitando muchos errores."), ("¿Qué es 'let it crash'?", "Dejar morir un actor con error y reiniciarlo desde un supervisor.")],
    "reto": "Añade un segundo actor que cuente los mensajes y resuélvelo conceptualmente en **Elixir**.",
    "impls": {
        "python": r"""import sys


class Acumulador:  # actor con estado propio
    def __init__(self):
        self.total = 0

    def recibir(self, mensaje):
        self.total += mensaje


nums = [int(x) for x in sys.stdin.read().split()]
actor = Acumulador()
for m in nums:
    actor.recibir(m)
print(f"total={actor.total}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const actor = { total: 0, recibir(m) { this.total += m; } };
const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
for (const m of nums) actor.recibir(m);
console.log(`total=${actor.total}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const actor = { total: 0, recibir(m: number) { this.total += m; } };
const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
for (const m of nums) actor.recibir(m);
console.log(`total=${actor.total}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static class Acumulador {
        long total = 0;
        void recibir(int m) { total += m; }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        Acumulador actor = new Acumulador();
        for (String s : p) actor.recibir(Integer.parseInt(s));
        System.out.println("total=" + actor.total);
    }
}
""",
        "csharp": r"""using System;

var actor = new Acumulador();
foreach (string s in Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries))
    actor.Recibir(int.Parse(s));
Console.WriteLine($"total={actor.Total}");

class Acumulador {
    public long Total { get; private set; }
    public void Recibir(int m) => Total += m;
}
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
	buzon := make(chan int, 64)
	done := make(chan int64)
	go func() { // actor: acumula los mensajes de su buzón
		var total int64
		for m := range buzon {
			total += int64(m)
		}
		done <- total
	}()
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		buzon <- n
	}
	close(buzon)
	fmt.Printf("total=%d\n", <-done)
}
""",
        "rust": r"""use std::io::Read;

struct Acumulador {
    total: i64,
}

impl Acumulador {
    fn recibir(&mut self, mensaje: i64) {
        self.total += mensaje;
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut actor = Acumulador { total: 0 };
    for x in s.split_whitespace() {
        actor.recibir(x.parse().unwrap());
    }
    println!("total={}", actor.total);
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long total = 0, m;
    while (scanf("%ld", &m) == 1) {
        total += m; /* el 'actor' acumula cada mensaje */
    }
    printf("total=%ld\n", total);
    return 0;
}
""",
        "php": r"""<?php
class Acumulador {
    public int $total = 0;
    public function recibir($m) { $this->total += $m; }
}

$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$actor = new Acumulador();
foreach ($nums as $m) {
    $actor->recibir($m);
}
echo "total={$actor->total}\n";
""",
        "sql": r"""-- SQL agrega sin actores; SUM sobre las filas.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT printf('total=%d', sum(x)) AS resultado FROM nums;
""",
    },
}

S[136] = {
    "descripcion": "Incrementar un contador n veces de forma segura, mostrando el resultado correcto.",
    "objetivo": "Entender el **modelo de memoria y las condiciones de carrera**: cuando dos hilos actualizan el mismo dato sin coordinación, el resultado puede corromperse. Incrementar de forma segura garantiza el valor correcto.",
    "resultados": ["Explicar qué es una condición de carrera.", "Reconocer la necesidad de sincronización.", "Producir un conteo correcto."],
    "temas": [("Condición de carrera", "Dos hilos, un dato, sin orden"), ("Sección crítica", "Código que solo un hilo debe ejecutar a la vez"), ("Atomicidad", "Operación indivisible")],
    "definiciones": [("Condición de carrera", "el resultado depende del orden imprevisible de dos accesos concurrentes. Clave: corrompe datos."), ("Sección crítica", "código que accede a un recurso compartido y debe ejecutarse en exclusión. Clave: se protege con un lock."), ("Operación atómica", "indivisible: ocurre entera o nada. Clave: evita la carrera en incrementos.")],
    "situacion": "Si dos hilos hacen `contador++` a la vez sin protección, pueden leer el mismo valor y perder un incremento. Un lock o una operación atómica garantiza el conteo correcto.",
    "entrada": "un entero `n` (número de incrementos)",
    "salida": "`cuenta=<n>`",
    "formula": "incrementar un contador n veces, con exclusión",
    "algoritmo": "cuenta <- 0 ; REPETIR n veces (protegido): cuenta <- cuenta + 1",
    "casos": [("5", "cuenta=5"), ("0", "cuenta=0"), ("3", "cuenta=3")],
    "comparacion": [("Sintáctica", "lock/mutex (Java/C#/Go), atómicos, o secuencial (aquí)."), ("Semántica", "Sin protección el resultado sería imprevisible con hilos reales."), ("Paradigmática", "SQL usa transacciones para la consistencia.")],
    "familia": "Java (synchronized/AtomicInteger), Go (sync.Mutex/atomic), Rust (Mutex/Atomic) protegen la sección crítica.",
    "errores": [("Incrementar sin proteger", "condición de carrera, conteo incorrecto", "usar lock o atómicos"), ("Bloquear de más", "cuello de botella", "minimizar la sección crítica")],
    "faq": [("¿Toda variable compartida necesita lock?", "Si más de un hilo la modifica, sí (o un tipo atómico)."), ("¿Atómico o lock?", "Atómico para operaciones simples; lock para secciones más complejas.")],
    "reto": "Incrementa desde dos hilos con un mutex y verifica el total; resuélvelo en **Go**.",
    "impls": {
        "python": r"""import sys

n = int(sys.stdin.readline())
cuenta = 0
for _ in range(n):  # sección crítica protegida (aquí, secuencial)
    cuenta += 1
print(f"cuenta={cuenta}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let cuenta = 0;
for (let i = 0; i < n; i++) cuenta += 1;
console.log(`cuenta=${cuenta}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let cuenta = 0;
for (let i = 0; i < n; i++) cuenta += 1;
console.log(`cuenta=${cuenta}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.concurrent.atomic.AtomicInteger;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        AtomicInteger cuenta = new AtomicInteger(0);
        for (int i = 0; i < n; i++) cuenta.incrementAndGet();
        System.out.println("cuenta=" + cuenta.get());
    }
}
""",
        "csharp": r"""using System;
using System.Threading;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int cuenta = 0;
for (int i = 0; i < n; i++) Interlocked.Increment(ref cuenta);
Console.WriteLine($"cuenta={cuenta}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"sync"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	var mu sync.Mutex
	cuenta := 0
	for i := 0; i < n; i++ {
		mu.Lock()
		cuenta++
		mu.Unlock()
	}
	fmt.Printf("cuenta=%d\n", cuenta)
}
""",
        "rust": r"""use std::io::Read;
use std::sync::Mutex;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let cuenta = Mutex::new(0i64);
    for _ in 0..n {
        *cuenta.lock().unwrap() += 1;
    }
    println!("cuenta={}", *cuenta.lock().unwrap());
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long cuenta = 0;
    for (long i = 0; i < n; i++) cuenta++;
    printf("cuenta=%ld\n", cuenta);
    return 0;
}
""",
        "php": r"""<?php
$n = (int) trim(fgets(STDIN));
$cuenta = 0;
for ($i = 0; $i < $n; $i++) {
    $cuenta += 1;
}
echo "cuenta=$cuenta\n";
""",
        "sql": r"""-- SQL usa transacciones para la consistencia; aquí, el conteo.
WITH nums(n) AS (VALUES (5), (0), (3))
SELECT printf('cuenta=%d', n) AS resultado FROM nums;
""",
    },
}

S[137] = {
    "descripcion": "Dado un código de 1 a 4, indicar la clase de error correspondiente.",
    "objetivo": "Clasificar los **tipos de error** por el momento en que aparecen: de sintaxis (al parsear), de tipos (al comprobar tipos), de enlace (al unir con librerías) y de ejecución (al correr). Saber cuándo ocurre cada uno acelera el diagnóstico.",
    "resultados": ["Nombrar las cuatro clases de error.", "Asociar cada error a su fase.", "Diagnosticar según cuándo aparece."],
    "temas": [("Error de sintaxis", "El código no se puede parsear"), ("Error de tipos", "Operación inválida para los tipos"), ("Error de enlace y de ejecución", "Al unir librerías o al correr")],
    "definiciones": [("Error de sintaxis", "el código viola las reglas gramaticales. Clave: se detecta al parsear."), ("Error de tipos", "operación no válida para los tipos implicados. Clave: en compilación (estáticos) o ejecución (dinámicos)."), ("Error de enlace", "no se encuentra una función/símbolo al unir con librerías. Clave: entre compilar y ejecutar."), ("Error de ejecución", "ocurre al correr (división por cero, índice fuera de rango). Clave: en tiempo de ejecución.")],
    "situacion": "Un `;` olvidado es de sintaxis; sumar texto y número, de tipos; una librería ausente, de enlace; dividir por cero, de ejecución. Saber la fase reduce el tiempo de búsqueda del fallo.",
    "entrada": "un entero `codigo` (1 a 4)",
    "salida": "`error=<sintaxis|tipos|enlace|ejecucion>`",
    "formula": "1→sintaxis, 2→tipos, 3→enlace, 4→ejecucion",
    "algoritmo": "LEER codigo ; SEGUN codigo: 1..4 -> nombre del error",
    "casos": [("1", "error=sintaxis"), ("3", "error=enlace"), ("4", "error=ejecucion")],
    "comparacion": [("Sintáctica", "switch/match sobre el código en cada lenguaje."), ("Semántica", "En estáticos, los de tipos salen al compilar; en dinámicos, al ejecutar."), ("Paradigmática", "SQL usa CASE.")],
    "familia": "Los compilados detectan sintaxis, tipos y enlace antes de ejecutar; los interpretados, muchos al correr.",
    "errores": [("Confundir error de tipos con de ejecución", "buscar en la fase equivocada", "recordar cuándo comprueba tipos tu lenguaje"), ("Ignorar el error de enlace", "'símbolo no encontrado'", "verificar librerías y su enlazado")],
    "faq": [("¿Cuándo salen los errores de tipos?", "En compilación (estáticos) o en ejecución (dinámicos)."), ("¿Qué es un error de enlace?", "Cuando el enlazador no encuentra una función/símbolo referenciado.")],
    "reto": "Añade el código 5 para 'error de lógica' y resuélvelo en **Rust** con `match`.",
    "impls": {
        "python": r"""import sys

codigo = int(sys.stdin.readline())
nombres = {1: "sintaxis", 2: "tipos", 3: "enlace", 4: "ejecucion"}
print(f"error={nombres.get(codigo, 'desconocido')}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const codigo = parseInt(readFileSync(0, "utf8").trim(), 10);
const nombres = { 1: "sintaxis", 2: "tipos", 3: "enlace", 4: "ejecucion" };
console.log(`error=${nombres[codigo] ?? "desconocido"}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const codigo: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const nombres: Record<number, string> = { 1: "sintaxis", 2: "tipos", 3: "enlace", 4: "ejecucion" };
console.log(`error=${nombres[codigo] ?? "desconocido"}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int codigo = Integer.parseInt(br.readLine().trim());
        String e;
        switch (codigo) {
            case 1: e = "sintaxis"; break;
            case 2: e = "tipos"; break;
            case 3: e = "enlace"; break;
            case 4: e = "ejecucion"; break;
            default: e = "desconocido";
        }
        System.out.println("error=" + e);
    }
}
""",
        "csharp": r"""using System;

int codigo = int.Parse(Console.In.ReadToEnd().Trim());
string e = codigo switch {
    1 => "sintaxis",
    2 => "tipos",
    3 => "enlace",
    4 => "ejecucion",
    _ => "desconocido",
};
Console.WriteLine($"error={e}");
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
	codigo, _ := strconv.Atoi(strings.TrimSpace(line))
	var e string
	switch codigo {
	case 1:
		e = "sintaxis"
	case 2:
		e = "tipos"
	case 3:
		e = "enlace"
	case 4:
		e = "ejecucion"
	default:
		e = "desconocido"
	}
	fmt.Printf("error=%s\n", e)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let codigo: i64 = s.trim().parse().unwrap();
    let e = match codigo {
        1 => "sintaxis",
        2 => "tipos",
        3 => "enlace",
        4 => "ejecucion",
        _ => "desconocido",
    };
    println!("error={e}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    int codigo;
    if (scanf("%d", &codigo) != 1) return 1;
    const char *e;
    switch (codigo) {
        case 1: e = "sintaxis"; break;
        case 2: e = "tipos"; break;
        case 3: e = "enlace"; break;
        case 4: e = "ejecucion"; break;
        default: e = "desconocido";
    }
    printf("error=%s\n", e);
    return 0;
}
""",
        "php": r"""<?php
$codigo = (int) trim(fgets(STDIN));
$nombres = [1 => "sintaxis", 2 => "tipos", 3 => "enlace", 4 => "ejecucion"];
echo "error=" . ($nombres[$codigo] ?? "desconocido") . "\n";
""",
        "sql": r"""-- SQL: selección por código con CASE.
WITH c(codigo) AS (VALUES (1))
SELECT printf('error=%s', CASE codigo WHEN 1 THEN 'sintaxis' WHEN 2 THEN 'tipos' WHEN 3 THEN 'enlace' WHEN 4 THEN 'ejecucion' ELSE 'desconocido' END) AS resultado
FROM c;
""",
    },
}

S[138] = {
    "descripcion": "Inspeccionar un valor mostrando el número, su cuadrado y su cubo, como al examinar variables en un depurador.",
    "objetivo": "Cerrar la parte con la **depuración**: cómo se diagnostica un programa. Inspeccionar el valor de las variables (aquí, el número y sus potencias) es lo que hace un depurador al pausar la ejecución.",
    "resultados": ["Inspeccionar el estado de un cálculo.", "Explicar qué hace un depurador.", "Nombrar los depuradores por runtime."],
    "temas": [("Depuración", "Encontrar y entender fallos"), ("Inspección de variables", "Ver los valores en un punto"), ("Puntos de ruptura", "Pausar la ejecución")],
    "definiciones": [("Depurador", "herramienta para pausar, inspeccionar y avanzar un programa (gdb, lldb, pdb). Clave: ver el estado real."), ("Punto de ruptura", "lugar donde el depurador pausa la ejecución. Clave: para inspeccionar ahí."), ("Inspección", "examinar el valor de las variables en un momento. Clave: la base del diagnóstico.")],
    "situacion": "Cuando un resultado sorprende, se pausa en un punto de ruptura y se inspeccionan las variables. Mostrar el número, su cuadrado y su cubo simula esa inspección del estado.",
    "entrada": "un entero `n`",
    "salida": "`valor=<n> cuadrado=<n²> cubo=<n³>`",
    "formula": "inspeccionar n, n² y n³",
    "algoritmo": "LEER n ; ESCRIBIR n, n*n, n*n*n",
    "casos": [("3", "valor=3 cuadrado=9 cubo=27"), ("2", "valor=2 cuadrado=4 cubo=8"), ("5", "valor=5 cuadrado=25 cubo=125")],
    "comparacion": [("Sintáctica", "Idéntica: calcular potencias."), ("Semántica", "Cada runtime tiene su depurador (pdb, gdb, lldb, el del IDE)."), ("Paradigmática", "SQL se depura con EXPLAIN y consultas de prueba.")],
    "familia": "gdb/lldb (C/C++/Rust), pdb (Python), el depurador de la JVM y de .NET, y los integrados en los IDE.",
    "errores": [("Depurar cambiando al azar", "no observar el estado", "inspeccionar variables en puntos clave"), ("Llenar el código de prints y olvidarlos", "ruido y regresiones", "preferir el depurador o quitar los prints al terminar")],
    "faq": [("¿print o depurador?", "El print es rápido; el depurador permite inspeccionar sin recompilar y avanzar paso a paso."), ("¿Cómo se depura SQL?", "Con EXPLAIN (plan de ejecución) y consultas de prueba sobre subconjuntos.")],
    "reto": "Añade la raíz cuadrada entera y resuélvelo en **Python** con `pdb` como práctica.",
    "impls": {
        "python": r"""import sys

n = int(sys.stdin.readline())
print(f"valor={n} cuadrado={n * n} cubo={n * n * n}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`valor=${n} cuadrado=${n * n} cubo=${n * n * n}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`valor=${n} cuadrado=${n * n} cubo=${n * n * n}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        System.out.println("valor=" + n + " cuadrado=" + (n * n) + " cubo=" + (n * n * n));
    }
}
""",
        "csharp": r"""using System;

long n = long.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"valor={n} cuadrado={n * n} cubo={n * n * n}");
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
	fmt.Printf("valor=%d cuadrado=%d cubo=%d\n", n, n*n, n*n*n)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("valor={} cuadrado={} cubo={}", n, n * n, n * n * n);
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("valor=%ld cuadrado=%ld cubo=%ld\n", n, n * n, n * n * n);
    return 0;
}
""",
        "php": r"""<?php
$n = (int) trim(fgets(STDIN));
echo "valor=$n cuadrado=" . ($n * $n) . " cubo=" . ($n * $n * $n) . "\n";
""",
        "sql": r"""-- SQL: se inspeccionan los valores calculados.
WITH nums(n) AS (VALUES (3), (2), (5))
SELECT printf('valor=%d cuadrado=%d cubo=%d', n, n * n, n * n * n) AS resultado FROM nums;
""",
    },
}


def main():
    for num, spec in S.items():
        g3.write_class(num, spec)
        print(f"Clase {num:03d} generada.")


if __name__ == "__main__":
    main()
