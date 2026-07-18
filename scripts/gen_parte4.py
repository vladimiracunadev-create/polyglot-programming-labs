"""Parte 4 — Control del programa (clases 057-072). Reutiliza gen_parte3.write_class."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_parte3 as g3  # noqa: E402

S = {}

S[57] = {
    "descripcion": "Dado un entero, informar si es positivo, si es par, y si cumple ambas condiciones (AND con cortocircuito).",
    "objetivo": "Producir booleanos con operadores de comparación y combinarlos con **AND cortocircuitado**. El cortocircuito evita evaluar la segunda condición si la primera ya decide el resultado.",
    "resultados": ["Producir booleanos a partir de comparaciones.", "Combinar condiciones con AND/OR.", "Explicar el cortocircuito y por qué importa."],
    "temas": [("Comparaciones", "Producen valores de verdad"), ("Operadores lógicos", "AND, OR y su cortocircuito"), ("Cortocircuito", "No evalúa lo que no hace falta"), ("Normalizar booleanos", "true/false consistente entre lenguajes")],
    "definiciones": [("Condición", "expresión que da verdadero o falso. Clave: gobierna las decisiones."), ("Cortocircuito", "en `a && b`, si `a` es falso no se evalúa `b`. Clave: evita trabajo y errores."), ("Operador relacional", "compara valores (>, <, ==). Clave: produce booleanos."), ("Predicado", "condición sobre un valor (es positivo, es par). Clave: bloque de la lógica.")],
    "situacion": "Validar `if (usuario != null && usuario.activo)` depende del cortocircuito: sin él, se accedería a `usuario.activo` con `usuario` nulo y reventaría. El orden de las condiciones importa.",
    "entrada": "un entero `n`",
    "salida": "`positivo=<true|false> par=<true|false> ambos=<true|false>`",
    "formula": "positivo = n>0 ; par = n%2==0 ; ambos = positivo && par",
    "algoritmo": "LEER n\nESCRIBIR positivo=(n>0), par=(n%2==0), ambos=((n>0) Y (n%2==0))",
    "casos": [("4", "positivo=true par=true ambos=true"), ("-3", "positivo=false par=false ambos=false"), ("7", "positivo=true par=false ambos=false")],
    "comparacion": [("Sintáctica", "`and` (Python) vs. `&&` (C/Java/JS/Go/Rust/PHP)."), ("Semántica", "Todos cortocircuitan `&&`/`and`; C# imprime True/False (normalizar)."), ("Paradigmática", "SQL usa AND en la expresión y CASE WHEN para el texto.")],
    "familia": "En Ruby `n > 0 && n.even?`. En Haskell `n > 0 && even n`, con el mismo cortocircuito.",
    "errores": [("Ordenar mal las condiciones", "evaluar algo inválido antes de la guarda", "poner primero la condición que protege a la segunda"), ("Imprimir True/False", "formato por defecto de C#", "normalizar a minúsculas con un ayudante")],
    "faq": [("¿`&` y `&&` son iguales?", "No: `&` es bit a bit y evalúa ambos lados; `&&` cortocircuita."), ("¿El cortocircuito cambia el resultado?", "No el valor lógico, pero sí si el segundo lado tiene efectos o puede fallar.")],
    "reto": "Añade `alguno=<positivo OR par>` y resuélvelo en **Kotlin**.",
    "impls": {
        "python": r"""import sys

n = int(sys.stdin.readline())
tf = lambda x: "true" if x else "false"
pos = n > 0
par = n % 2 == 0
print(f"positivo={tf(pos)} par={tf(par)} ambos={tf(pos and par)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const tf = (x) => (x ? "true" : "false");
const pos = n > 0;
const par = n % 2 === 0;
console.log(`positivo=${tf(pos)} par=${tf(par)} ambos=${tf(pos && par)}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const tf = (x: boolean): string => (x ? "true" : "false");
const pos: boolean = n > 0;
const par: boolean = n % 2 === 0;
console.log(`positivo=${tf(pos)} par=${tf(par)} ambos=${tf(pos && par)}`);
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
        int n = Integer.parseInt(br.readLine().trim());
        boolean pos = n > 0;
        boolean par = n % 2 == 0;
        System.out.printf("positivo=%s par=%s ambos=%s%n", tf(pos), tf(par), tf(pos && par));
    }
}
""",
        "csharp": r"""using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
string Tf(bool x) => x ? "true" : "false";
bool pos = n > 0;
bool par = n % 2 == 0;
Console.WriteLine($"positivo={Tf(pos)} par={Tf(par)} ambos={Tf(pos && par)}");
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
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	pos := n > 0
	par := n%2 == 0
	fmt.Printf("positivo=%s par=%s ambos=%s\n", tf(pos), tf(par), tf(pos && par))
}
""",
        "rust": r"""use std::io::Read;

fn tf(x: bool) -> &'static str {
    if x { "true" } else { "false" }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let pos = n > 0;
    let par = n % 2 == 0;
    println!("positivo={} par={} ambos={}", tf(pos), tf(par), tf(pos && par));
}
""",
        "c": r"""#include <stdio.h>

static const char *tf(int x) {
    return x ? "true" : "false";
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    int pos = n > 0;
    int par = n % 2 == 0;
    printf("positivo=%s par=%s ambos=%s\n", tf(pos), tf(par), tf(pos && par));
    return 0;
}
""",
        "php": r"""<?php
$n = (int) trim(fgets(STDIN));
$tf = fn($x) => $x ? "true" : "false";
$pos = $n > 0;
$par = $n % 2 === 0;
printf("positivo=%s par=%s ambos=%s\n", $tf($pos), $tf($par), $tf($pos && $par));
""",
        "sql": r"""-- SQL: condiciones con AND dentro de CASE WHEN.
WITH nums(n) AS (VALUES (4), (-3), (7))
SELECT printf('positivo=%s par=%s ambos=%s',
       CASE WHEN n > 0 THEN 'true' ELSE 'false' END,
       CASE WHEN n % 2 = 0 THEN 'true' ELSE 'false' END,
       CASE WHEN n > 0 AND n % 2 = 0 THEN 'true' ELSE 'false' END) AS resultado
FROM nums;
""",
    },
}

S[58] = {
    "descripcion": "Clasificar una edad con validación temprana: negativa es inválida, menor de 18 es 'menor', y el resto 'adulto'.",
    "objetivo": "Aplicar **guardas** (validación temprana): comprobar primero los casos inválidos o especiales y salir cuanto antes, dejando el camino principal limpio. Reduce el anidamiento y hace el código más legible.",
    "resultados": ["Escribir guardas que validan y salen temprano.", "Evitar el anidamiento profundo de if.", "Ordenar las comprobaciones de más restrictiva a menos."],
    "temas": [("Validación temprana", "Comprobar lo inválido primero"), ("Guarda", "Un if que corta el flujo pronto"), ("Retorno temprano", "Salir en cuanto se decide"), ("Legibilidad", "Menos anidamiento, más claridad")],
    "definiciones": [("Guarda", "condición al inicio que corta el flujo si no se cumple. Clave: evita anidar."), ("Validación temprana", "rechazar entradas inválidas antes del cálculo. Clave: el camino feliz queda limpio."), ("Retorno temprano", "salir de la función en cuanto hay respuesta. Clave: menos ramas abiertas."), ("Camino feliz", "el flujo principal sin errores. Clave: se lee de corrido tras las guardas.")],
    "situacion": "Con guardas, `if edad < 0: return invalido` al principio evita envolver todo el resto en un `else`. El código baja en escalera en vez de anidarse hacia la derecha.",
    "entrada": "un entero `edad`",
    "salida": "`invalido` si edad<0, `menor` si edad<18, `adulto` en otro caso",
    "formula": "guardas: edad<0 → invalido; edad<18 → menor; si no → adulto",
    "algoritmo": "LEER edad\nSI edad < 0: ESCRIBIR \"invalido\" ; FIN\nSI edad < 18: ESCRIBIR \"menor\" ; FIN\nESCRIBIR \"adulto\"",
    "casos": [("-5", "invalido"), ("10", "menor"), ("20", "adulto")],
    "comparacion": [("Sintáctica", "`if ...: return` (Python) vs. `if (...) { return; }` (C/Java)."), ("Semántica", "El orden de las guardas define la clasificación; cambiarlo cambia el resultado."), ("Paradigmática", "SQL encadena condiciones con CASE WHEN en orden.")],
    "familia": "En Ruby `return 'invalido' if edad < 0`. En Go es común la guarda con `if ...{ return }` al inicio de la función.",
    "errores": [("Anidar en vez de usar guardas", "escalera de if/else hacia la derecha", "sacar los casos especiales como guardas al inicio"), ("Ordenar mal las guardas", "clasificar mal por comprobar tarde", "ir de la condición más restrictiva a la más general")],
    "faq": [("¿Guarda o if/else anidado?", "La guarda suele ser más legible: aplana el código y deja claro el camino feliz."), ("¿Varios return son mala práctica?", "No con guardas: hacen el flujo más claro, no más confuso.")],
    "reto": "Añade la categoría `senior` para edad >= 65 y resuélvelo en **Go** con guardas.",
    "impls": {
        "python": r"""import sys

edad = int(sys.stdin.readline())
if edad < 0:
    print("invalido")
elif edad < 18:
    print("menor")
else:
    print("adulto")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const edad = parseInt(readFileSync(0, "utf8").trim(), 10);
if (edad < 0) console.log("invalido");
else if (edad < 18) console.log("menor");
else console.log("adulto");
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const edad: number = parseInt(readFileSync(0, "utf8").trim(), 10);
if (edad < 0) console.log("invalido");
else if (edad < 18) console.log("menor");
else console.log("adulto");
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int edad = Integer.parseInt(br.readLine().trim());
        if (edad < 0) {
            System.out.println("invalido");
        } else if (edad < 18) {
            System.out.println("menor");
        } else {
            System.out.println("adulto");
        }
    }
}
""",
        "csharp": r"""using System;

int edad = int.Parse(Console.In.ReadToEnd().Trim());
if (edad < 0)
    Console.WriteLine("invalido");
else if (edad < 18)
    Console.WriteLine("menor");
else
    Console.WriteLine("adulto");
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
	edad, _ := strconv.Atoi(strings.TrimSpace(line))
	if edad < 0 {
		fmt.Println("invalido")
		return
	}
	if edad < 18 {
		fmt.Println("menor")
		return
	}
	fmt.Println("adulto")
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let edad: i64 = s.trim().parse().unwrap();
    if edad < 0 {
        println!("invalido");
    } else if edad < 18 {
        println!("menor");
    } else {
        println!("adulto");
    }
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long edad;
    if (scanf("%ld", &edad) != 1) return 1;
    if (edad < 0) {
        printf("invalido\n");
    } else if (edad < 18) {
        printf("menor\n");
    } else {
        printf("adulto\n");
    }
    return 0;
}
""",
        "php": r"""<?php
$edad = (int) trim(fgets(STDIN));
if ($edad < 0) {
    echo "invalido\n";
} elseif ($edad < 18) {
    echo "menor\n";
} else {
    echo "adulto\n";
}
""",
        "sql": r"""-- SQL: clasificación con CASE WHEN en orden.
WITH edades(edad) AS (VALUES (-5), (10), (20))
SELECT CASE WHEN edad < 0 THEN 'invalido'
            WHEN edad < 18 THEN 'menor'
            ELSE 'adulto' END AS resultado
FROM edades;
""",
    },
}

S[59] = {
    "descripcion": "Convertir una calificación numérica (0-100) en una letra: A (>=90), B (>=80), C (>=70), F en otro caso.",
    "objetivo": "Practicar `if` / `else if` encadenados para clasificar en varios rangos. Es la estructura de decisión más común y la base de toda ramificación.",
    "resultados": ["Encadenar if/else para varios rangos.", "Ordenar los umbrales correctamente.", "Cubrir el caso por defecto (else)."],
    "temas": [("if / else if / else", "Elegir entre varias ramas"), ("Rangos ordenados", "De mayor a menor umbral"), ("Caso por defecto", "El else que recoge lo demás"), ("Exclusividad", "Solo una rama se ejecuta")],
    "definiciones": [("if", "ejecuta un bloque si la condición es verdadera. Clave: la decisión básica."), ("else if", "condición alternativa si la anterior falló. Clave: encadena rangos."), ("else", "rama por defecto si ninguna condición se cumple. Clave: cubre el resto."), ("Umbral", "valor límite que separa dos categorías. Clave: su orden importa.")],
    "situacion": "Asignar una nota por tramos aparece en todas partes: descuentos por volumen, niveles de riesgo, categorías. Si los umbrales se comprueban en mal orden, la clasificación falla.",
    "entrada": "un entero `score` (0-100)",
    "salida": "`nota=<A|B|C|F>`",
    "formula": "score>=90→A; >=80→B; >=70→C; si no→F",
    "algoritmo": "LEER score\nSI score>=90: A\nSINO SI score>=80: B\nSINO SI score>=70: C\nSINO: F",
    "casos": [("95", "nota=A"), ("72", "nota=C"), ("40", "nota=F")],
    "comparacion": [("Sintáctica", "`elif` (Python) vs. `else if` (C/Java/JS) vs. `else if` con llaves."), ("Semántica", "Solo se ejecuta la primera rama verdadera; el orden descendente es clave."), ("Paradigmática", "SQL usa CASE WHEN con los umbrales en orden.")],
    "familia": "En Ruby se usa `if/elsif/else` o un `case` con rangos (`when 90..100`). En Kotlin, `when` con rangos es idiomático.",
    "errores": [("Comprobar los umbrales de menor a mayor", "todo cae en la primera rama", "ordenar de mayor a menor umbral"), ("Olvidar el else", "no clasificar algunos valores", "incluir siempre un caso por defecto")],
    "faq": [("¿Puedo usar switch aquí?", "Para rangos, if/else o `when`/`match` con rangos; el switch clásico es para valores exactos."), ("¿Importa el orden?", "Mucho: la primera condición verdadera gana, así que van de más a menos exigente.")],
    "reto": "Añade el tramo `D` para >=60 y resuélvelo en **Kotlin** con `when`.",
    "impls": {
        "python": r"""import sys

score = int(sys.stdin.readline())
if score >= 90:
    nota = "A"
elif score >= 80:
    nota = "B"
elif score >= 70:
    nota = "C"
else:
    nota = "F"
print(f"nota={nota}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const score = parseInt(readFileSync(0, "utf8").trim(), 10);
let nota;
if (score >= 90) nota = "A";
else if (score >= 80) nota = "B";
else if (score >= 70) nota = "C";
else nota = "F";
console.log(`nota=${nota}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const score: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let nota: string;
if (score >= 90) nota = "A";
else if (score >= 80) nota = "B";
else if (score >= 70) nota = "C";
else nota = "F";
console.log(`nota=${nota}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int score = Integer.parseInt(br.readLine().trim());
        String nota;
        if (score >= 90) nota = "A";
        else if (score >= 80) nota = "B";
        else if (score >= 70) nota = "C";
        else nota = "F";
        System.out.println("nota=" + nota);
    }
}
""",
        "csharp": r"""using System;

int score = int.Parse(Console.In.ReadToEnd().Trim());
string nota;
if (score >= 90) nota = "A";
else if (score >= 80) nota = "B";
else if (score >= 70) nota = "C";
else nota = "F";
Console.WriteLine($"nota={nota}");
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
	score, _ := strconv.Atoi(strings.TrimSpace(line))
	var nota string
	if score >= 90 {
		nota = "A"
	} else if score >= 80 {
		nota = "B"
	} else if score >= 70 {
		nota = "C"
	} else {
		nota = "F"
	}
	fmt.Printf("nota=%s\n", nota)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let score: i64 = s.trim().parse().unwrap();
    let nota = if score >= 90 {
        "A"
    } else if score >= 80 {
        "B"
    } else if score >= 70 {
        "C"
    } else {
        "F"
    };
    println!("nota={nota}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long score;
    if (scanf("%ld", &score) != 1) return 1;
    char nota;
    if (score >= 90) nota = 'A';
    else if (score >= 80) nota = 'B';
    else if (score >= 70) nota = 'C';
    else nota = 'F';
    printf("nota=%c\n", nota);
    return 0;
}
""",
        "php": r"""<?php
$score = (int) trim(fgets(STDIN));
if ($score >= 90) {
    $nota = "A";
} elseif ($score >= 80) {
    $nota = "B";
} elseif ($score >= 70) {
    $nota = "C";
} else {
    $nota = "F";
}
echo "nota=$nota\n";
""",
        "sql": r"""-- SQL: rangos con CASE WHEN en orden descendente.
WITH scores(score) AS (VALUES (95), (72), (40))
SELECT printf('nota=%s',
       CASE WHEN score >= 90 THEN 'A'
            WHEN score >= 80 THEN 'B'
            WHEN score >= 70 THEN 'C'
            ELSE 'F' END) AS resultado
FROM scores;
""",
    },
}

S[60] = {
    "descripcion": "Devolver el mayor de dos enteros usando una expresión condicional (ternario).",
    "objetivo": "Usar el **operador ternario** o el `if` como expresión: elegir un valor en una sola línea. En Rust y Kotlin el propio `if` devuelve valor; en C/Java/JS/PHP se usa `?:`.",
    "resultados": ["Elegir un valor con el operador ternario.", "Distinguir if-sentencia de if-expresión.", "Escribir código conciso sin perder claridad."],
    "temas": [("Ternario ?:", "Elegir un valor en una expresión"), ("if como expresión", "En Rust/Kotlin el if devuelve valor"), ("Expresión vs. sentencia", "Producir un valor vs. ejecutar una acción"), ("Concisión", "Una línea en vez de cuatro")],
    "definiciones": [("Operador ternario", "`cond ? a : b`: elige a o b según la condición. Clave: expresión, no sentencia."), ("Expresión", "código que produce un valor. Clave: se puede asignar."), ("Sentencia", "código que ejecuta una acción. Clave: no siempre produce valor."), ("if-expresión", "un if que devuelve un valor (Rust, Kotlin). Clave: no necesita ternario aparte.")],
    "situacion": "`max = a > b ? a : b` dice en una línea lo que un if/else diría en cuatro. Bien usado, el ternario es claro; abusado (anidado), se vuelve ilegible.",
    "entrada": "una línea `a b` (dos enteros)",
    "salida": "`max=<el mayor>`",
    "formula": "max = (a > b) ? a : b",
    "algoritmo": "LEER a, b\nmax <- SI a > b ENTONCES a SINO b\nESCRIBIR \"max=\" max",
    "casos": [("3 7", "max=7"), ("9 2", "max=9"), ("5 5", "max=5")],
    "comparacion": [("Sintáctica", "`a if a>b else b` (Python) vs. `a>b ? a : b` (C/Java/JS) vs. `if a>b {a} else {b}` (Rust)."), ("Semántica", "Python invierte el orden; Rust/Kotlin no tienen ternario porque el if ya es expresión."), ("Paradigmática", "SQL usa `CASE WHEN` o `max(a,b)` directamente.")],
    "familia": "En Ruby `a > b ? a : b`. En Kotlin `if (a > b) a else b`, como Rust: el if es una expresión.",
    "errores": [("Anidar ternarios en exceso", "código ilegible", "usar if/else cuando hay más de dos ramas"), ("Confundir el orden en Python", "`a if cond else b` no es `cond ? a : b`", "recordar que la condición va en el medio en Python")],
    "faq": [("¿Rust no tiene `?:`?", "No: su `if` ya es una expresión que devuelve valor, así que no hace falta."), ("¿El ternario es más rápido?", "No: es equivalente al if/else; es cuestión de concisión, no de velocidad.")],
    "reto": "Devuelve el **mínimo** en vez del máximo y resuélvelo en **Rust** con `if` como expresión.",
    "impls": {
        "python": r"""import sys

a, b = map(int, sys.stdin.readline().split())
mx = a if a > b else b
print(f"max={mx}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const mx = a > b ? a : b;
console.log(`max=${mx}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const mx: number = a > b ? a : b;
console.log(`max=${mx}`);
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
        int mx = a > b ? a : b;
        System.out.println("max=" + mx);
    }
}
""",
        "csharp": r"""using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
int mx = a > b ? a : b;
Console.WriteLine($"max={mx}");
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
	mx := b
	if a > b {
		mx = a
	}
	fmt.Printf("max=%d\n", mx)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let mx = if v[0] > v[1] { v[0] } else { v[1] };
    println!("max={mx}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    long mx = a > b ? a : b;
    printf("max=%ld\n", mx);
    return 0;
}
""",
        "php": r"""<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;
$mx = $a > $b ? $a : $b;
echo "max=$mx\n";
""",
        "sql": r"""-- SQL: la función max() elige el mayor directamente.
WITH pares(a, b) AS (VALUES (3, 7), (9, 2), (5, 5))
SELECT printf('max=%d', max(a, b)) AS resultado
FROM pares;
""",
    },
}

S[61] = {
    "descripcion": "Dado el número de día (1-7), devolver su nombre; cualquier otro número es 'invalido'.",
    "objetivo": "Usar `switch` / `case` (o su equivalente) para elegir entre valores exactos, con un caso por defecto. Verás el `fallthrough` (caída) de C/Java y cómo otros lenguajes lo evitan.",
    "resultados": ["Seleccionar por valor exacto con switch/case.", "Usar el caso por defecto.", "Explicar el fallthrough y cómo lo maneja cada lenguaje."],
    "temas": [("switch/case", "Elegir por valor exacto"), ("default", "El caso por defecto"), ("Fallthrough", "Caída de un caso al siguiente (C/Java)"), ("Alternativas", "match/when sin caída")],
    "definiciones": [("switch", "estructura que elige una rama según el valor exacto. Clave: para muchos valores concretos."), ("case", "una de las ramas del switch. Clave: coincide con un valor."), ("fallthrough", "en C/Java, un case sigue al siguiente si falta `break`. Clave: fuente de bugs."), ("default", "rama que se ejecuta si ningún case coincide. Clave: cubre lo inesperado.")],
    "situacion": "Traducir un código a un nombre (día, mes, estado) es el caso típico de switch. Olvidar un `break` en C/Java hace 'caer' al siguiente case: un error clásico que otros lenguajes evitan por diseño.",
    "entrada": "un entero `d` (día)",
    "salida": "`dia=<nombre>` o `dia=invalido`",
    "formula": "1→lunes … 7→domingo; otro→invalido",
    "algoritmo": "LEER d\nSEGUN d: 1..7 -> nombre ; otro -> invalido",
    "casos": [("1", "dia=lunes"), ("6", "dia=sabado"), ("8", "dia=invalido")],
    "comparacion": [("Sintáctica", "`switch` con `break` (C/Java/JS) vs. `match` (Rust) vs. `when` (Kotlin)."), ("Semántica", "C/Java caen sin `break`; Go, Rust y el switch de Python (match) no caen."), ("Paradigmática", "SQL usa CASE WHEN valor.")],
    "familia": "En Ruby `case d; when 1 then 'lunes'`. En Kotlin `when (d) { 1 -> ... }`. Ninguno cae como C.",
    "errores": [("Olvidar `break` en C/Java", "el flujo cae al siguiente case", "poner `break` en cada case o usar match/when"), ("No manejar valores fuera de rango", "salida vacía o error", "incluir siempre el caso por defecto")],
    "faq": [("¿Por qué existe el fallthrough?", "Herencia de C; a veces útil, pero suele ser un error olvidar el break."), ("¿Go tiene fallthrough?", "No por defecto: hay que pedirlo con la palabra `fallthrough` explícita.")],
    "reto": "Agrupa sábado y domingo como `finde` y resuélvelo en **Go** con un `switch`.",
    "impls": {
        "python": r"""import sys

d = int(sys.stdin.readline())
nombres = {1: "lunes", 2: "martes", 3: "miercoles", 4: "jueves",
           5: "viernes", 6: "sabado", 7: "domingo"}
print(f"dia={nombres.get(d, 'invalido')}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const d = parseInt(readFileSync(0, "utf8").trim(), 10);
let dia;
switch (d) {
  case 1: dia = "lunes"; break;
  case 2: dia = "martes"; break;
  case 3: dia = "miercoles"; break;
  case 4: dia = "jueves"; break;
  case 5: dia = "viernes"; break;
  case 6: dia = "sabado"; break;
  case 7: dia = "domingo"; break;
  default: dia = "invalido";
}
console.log(`dia=${dia}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const d: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let dia: string;
switch (d) {
  case 1: dia = "lunes"; break;
  case 2: dia = "martes"; break;
  case 3: dia = "miercoles"; break;
  case 4: dia = "jueves"; break;
  case 5: dia = "viernes"; break;
  case 6: dia = "sabado"; break;
  case 7: dia = "domingo"; break;
  default: dia = "invalido";
}
console.log(`dia=${dia}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int d = Integer.parseInt(br.readLine().trim());
        String dia;
        switch (d) {
            case 1: dia = "lunes"; break;
            case 2: dia = "martes"; break;
            case 3: dia = "miercoles"; break;
            case 4: dia = "jueves"; break;
            case 5: dia = "viernes"; break;
            case 6: dia = "sabado"; break;
            case 7: dia = "domingo"; break;
            default: dia = "invalido";
        }
        System.out.println("dia=" + dia);
    }
}
""",
        "csharp": r"""using System;

int d = int.Parse(Console.In.ReadToEnd().Trim());
string dia = d switch {
    1 => "lunes",
    2 => "martes",
    3 => "miercoles",
    4 => "jueves",
    5 => "viernes",
    6 => "sabado",
    7 => "domingo",
    _ => "invalido",
};
Console.WriteLine($"dia={dia}");
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
	d, _ := strconv.Atoi(strings.TrimSpace(line))
	var dia string
	switch d {
	case 1:
		dia = "lunes"
	case 2:
		dia = "martes"
	case 3:
		dia = "miercoles"
	case 4:
		dia = "jueves"
	case 5:
		dia = "viernes"
	case 6:
		dia = "sabado"
	case 7:
		dia = "domingo"
	default:
		dia = "invalido"
	}
	fmt.Printf("dia=%s\n", dia)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let d: i64 = s.trim().parse().unwrap();
    let dia = match d {
        1 => "lunes",
        2 => "martes",
        3 => "miercoles",
        4 => "jueves",
        5 => "viernes",
        6 => "sabado",
        7 => "domingo",
        _ => "invalido",
    };
    println!("dia={dia}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long d;
    if (scanf("%ld", &d) != 1) return 1;
    const char *dia;
    switch (d) {
        case 1: dia = "lunes"; break;
        case 2: dia = "martes"; break;
        case 3: dia = "miercoles"; break;
        case 4: dia = "jueves"; break;
        case 5: dia = "viernes"; break;
        case 6: dia = "sabado"; break;
        case 7: dia = "domingo"; break;
        default: dia = "invalido";
    }
    printf("dia=%s\n", dia);
    return 0;
}
""",
        "php": r"""<?php
$d = (int) trim(fgets(STDIN));
switch ($d) {
    case 1: $dia = "lunes"; break;
    case 2: $dia = "martes"; break;
    case 3: $dia = "miercoles"; break;
    case 4: $dia = "jueves"; break;
    case 5: $dia = "viernes"; break;
    case 6: $dia = "sabado"; break;
    case 7: $dia = "domingo"; break;
    default: $dia = "invalido";
}
echo "dia=$dia\n";
""",
        "sql": r"""-- SQL: selección por valor con CASE WHEN.
WITH dias(d) AS (VALUES (1), (6), (8))
SELECT printf('dia=%s',
       CASE d WHEN 1 THEN 'lunes' WHEN 2 THEN 'martes' WHEN 3 THEN 'miercoles'
              WHEN 4 THEN 'jueves' WHEN 5 THEN 'viernes' WHEN 6 THEN 'sabado'
              WHEN 7 THEN 'domingo' ELSE 'invalido' END) AS resultado
FROM dias;
""",
    },
}

S[62] = {
    "descripcion": "Clasificar el signo de un entero (positivo, negativo o cero) usando coincidencia de patrones.",
    "objetivo": "Usar **coincidencia de patrones** (`match`/`when`) para decidir según la forma o el rango de un valor. Es más expresiva y segura que el switch clásico: obliga a cubrir todos los casos.",
    "resultados": ["Clasificar con match/when o su equivalente.", "Usar guardas dentro de los patrones.", "Explicar por qué el match exhaustivo es más seguro."],
    "temas": [("Coincidencia de patrones", "Decidir por la forma del valor"), ("Guardas en patrones", "Condiciones dentro del caso"), ("Exhaustividad", "Cubrir todos los casos, obligatorio en Rust"), ("match vs. switch", "Más expresivo y sin caída")],
    "definiciones": [("Coincidencia de patrones", "elegir una rama según la estructura o el rango de un valor. Clave: más potente que el switch."), ("Exhaustividad", "el compilador exige cubrir todos los casos (Rust). Clave: evita olvidos."), ("Guarda de patrón", "condición extra dentro de un caso (`n if n>0`). Clave: refina el patrón."), ("match", "construcción de coincidencia de patrones (Rust, Python 3.10+). Clave: sin fallthrough.")],
    "situacion": "Clasificar el signo con `match` deja explícitos los tres casos (positivo, negativo, cero). En Rust, si olvidas uno, el programa no compila: la exhaustividad te protege.",
    "entrada": "un entero `n`",
    "salida": "`signo=<positivo|negativo|cero>`",
    "formula": "n>0→positivo; n<0→negativo; n==0→cero",
    "algoritmo": "LEER n\nCOINCIDIR n: (>0)->positivo ; (<0)->negativo ; (0)->cero",
    "casos": [("5", "signo=positivo"), ("-3", "signo=negativo"), ("0", "signo=cero")],
    "comparacion": [("Sintáctica", "`match` con guardas (Rust/Python) vs. if/else (C/Java) que no tienen match nativo clásico."), ("Semántica", "Rust exige exhaustividad; C/Java no avisan si falta un caso."), ("Paradigmática", "SQL expresa la clasificación con CASE WHEN.")],
    "familia": "En Kotlin `when { n > 0 -> ... }`. En Haskell se usan guardas: `signo n | n > 0 = ...`. Todos favorecen cubrir cada caso.",
    "errores": [("Dejar un caso sin cubrir", "comportamiento indefinido o error", "en Rust el compilador obliga; en otros, añadir el caso por defecto"), ("Usar == con reales para 'cero'", "imprecisión del punto flotante", "aquí son enteros; con reales, comparar con tolerancia")],
    "faq": [("¿match es solo de Rust?", "No: Python 3.10+ tiene `match`, Kotlin `when`, Scala `match`, Haskell guardas/patrones."), ("¿Por qué es más seguro que switch?", "Puede exigir exhaustividad y no tiene fallthrough accidental.")],
    "reto": "Añade el caso `n` par/impar dentro del positivo (con guarda) y resuélvelo en **Rust** con `match` y guardas.",
    "impls": {
        "python": r"""import sys

n = int(sys.stdin.readline())
match n:
    case _ if n > 0:
        signo = "positivo"
    case _ if n < 0:
        signo = "negativo"
    case _:
        signo = "cero"
print(f"signo={signo}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const signo = n > 0 ? "positivo" : n < 0 ? "negativo" : "cero";
console.log(`signo=${signo}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const signo: string = n > 0 ? "positivo" : n < 0 ? "negativo" : "cero";
console.log(`signo=${signo}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        String signo = n > 0 ? "positivo" : (n < 0 ? "negativo" : "cero");
        System.out.println("signo=" + signo);
    }
}
""",
        "csharp": r"""using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
string signo = n switch {
    > 0 => "positivo",
    < 0 => "negativo",
    _ => "cero",
};
Console.WriteLine($"signo={signo}");
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
	var signo string
	switch {
	case n > 0:
		signo = "positivo"
	case n < 0:
		signo = "negativo"
	default:
		signo = "cero"
	}
	fmt.Printf("signo=%s\n", signo)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let signo = match n {
        n if n > 0 => "positivo",
        n if n < 0 => "negativo",
        _ => "cero",
    };
    println!("signo={signo}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    const char *signo = n > 0 ? "positivo" : (n < 0 ? "negativo" : "cero");
    printf("signo=%s\n", signo);
    return 0;
}
""",
        "php": r"""<?php
$n = (int) trim(fgets(STDIN));
$signo = match (true) {
    $n > 0 => "positivo",
    $n < 0 => "negativo",
    default => "cero",
};
echo "signo=$signo\n";
""",
        "sql": r"""-- SQL: coincidencia por rango con CASE WHEN.
WITH nums(n) AS (VALUES (5), (-3), (0))
SELECT printf('signo=%s',
       CASE WHEN n > 0 THEN 'positivo' WHEN n < 0 THEN 'negativo' ELSE 'cero' END) AS resultado
FROM nums;
""",
    },
}

S[63] = {
    "descripcion": "Sumar los enteros de 1 a n usando un bucle por condición (while).",
    "objetivo": "Usar el bucle `while`: repetir mientras una condición sea verdadera. Es el bucle más básico y el que subyace a todos los demás.",
    "resultados": ["Escribir un bucle while con una condición de parada.", "Actualizar el estado en cada vuelta.", "Evitar el bucle infinito."],
    "temas": [("while", "Repetir mientras se cumpla una condición"), ("Condición de parada", "Cuándo termina el bucle"), ("Acumulador", "Sumar en cada vuelta"), ("Bucle infinito", "El peligro de no avanzar")],
    "definiciones": [("while", "bucle que repite mientras la condición sea verdadera. Clave: comprueba antes de cada vuelta."), ("do-while", "variante que ejecuta al menos una vez (comprueba al final). Clave: no en todos los lenguajes."), ("Condición de parada", "lo que hace terminar el bucle. Clave: algo debe acercarse a ella."), ("Acumulador", "variable que reúne el resultado. Clave: se actualiza cada vuelta.")],
    "situacion": "Sumar 1..n con while obliga a manejar el contador y la condición a mano. Si el contador no avanza, el bucle no termina: el error más clásico de los bucles.",
    "entrada": "un entero `n` (n >= 1)",
    "salida": "`suma=<1+2+...+n>`",
    "formula": "suma = 1 + 2 + ... + n",
    "algoritmo": "LEER n\nsuma <- 0 ; i <- 1\nMIENTRAS i <= n: suma <- suma+i ; i <- i+1\nESCRIBIR \"suma=\" suma",
    "casos": [("5", "suma=15"), ("1", "suma=1"), ("10", "suma=55")],
    "comparacion": [("Sintáctica", "`while cond:` (Python) vs. `while (cond) {}` (C/Java/JS)."), ("Semántica", "El while comprueba antes; el do-while (C/Java/JS) al menos una vez."), ("Paradigmática", "SQL evita el bucle: suma con un CTE recursivo o una fórmula.")],
    "familia": "En Ruby `while i <= n`. En Go solo hay `for` (que hace de while): `for i <= n`. Rust `while i <= n`.",
    "errores": [("No avanzar el contador", "bucle infinito", "asegurar que algo cambia hacia la condición de parada"), ("Condición mal puesta", "una vuelta de más o de menos (off-by-one)", "verificar los límites con un caso pequeño")],
    "faq": [("¿while o for?", "El for es más compacto cuando el número de vueltas se conoce; el while, cuando depende de una condición."), ("¿Go no tiene while?", "No como palabra: usa `for cond {}`, que es lo mismo.")],
    "reto": "Suma solo los pares de 1 a n y resuélvelo en **Go** con `for` en modo while.",
    "impls": {
        "python": r"""import sys

n = int(sys.stdin.readline())
suma = 0
i = 1
while i <= n:
    suma += i
    i += 1
print(f"suma={suma}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let suma = 0;
let i = 1;
while (i <= n) {
  suma += i;
  i++;
}
console.log(`suma=${suma}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let suma = 0;
let i = 1;
while (i <= n) {
  suma += i;
  i++;
}
console.log(`suma=${suma}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        long suma = 0;
        int i = 1;
        while (i <= n) {
            suma += i;
            i++;
        }
        System.out.println("suma=" + suma);
    }
}
""",
        "csharp": r"""using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long suma = 0;
int i = 1;
while (i <= n) {
    suma += i;
    i++;
}
Console.WriteLine($"suma={suma}");
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
	suma := 0
	i := 1
	for i <= n {
		suma += i
		i++
	}
	fmt.Printf("suma=%d\n", suma)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut suma = 0i64;
    let mut i = 1i64;
    while i <= n {
        suma += i;
        i += 1;
    }
    println!("suma={suma}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long suma = 0;
    long i = 1;
    while (i <= n) {
        suma += i;
        i++;
    }
    printf("suma=%ld\n", suma);
    return 0;
}
""",
        "php": r"""<?php
$n = (int) trim(fgets(STDIN));
$suma = 0;
$i = 1;
while ($i <= $n) {
    $suma += $i;
    $i++;
}
echo "suma=$suma\n";
""",
        "sql": r"""-- SQL: suma 1..n con un CTE recursivo (ilustrativo, n=10).
WITH RECURSIVE seq(i) AS (
    VALUES (1)
    UNION ALL SELECT i + 1 FROM seq WHERE i < 10
)
SELECT printf('suma=%d', sum(i)) AS resultado FROM seq;
""",
    },
}

S[64] = {
    "descripcion": "Calcular el factorial de n (n!) con un bucle for.",
    "objetivo": "Usar el bucle `for` cuando el número de vueltas se conoce. El factorial multiplica de 1 a n y muestra el `for` clásico y el `for`-range de cada lenguaje.",
    "resultados": ["Escribir un bucle for con contador.", "Acumular un producto.", "Reconocer el for-range frente al for clásico."],
    "temas": [("for clásico", "init; condición; incremento"), ("for-range", "Recorrer un rango directamente"), ("Acumular un producto", "Multiplicar en cada vuelta"), ("Caso base 0! = 1", "El bucle no se ejecuta y queda 1")],
    "definiciones": [("for", "bucle con inicialización, condición e incremento. Clave: para un número conocido de vueltas."), ("for-range", "recorrer un rango o colección sin gestionar el índice (Python, Rust, Go). Clave: menos errores."), ("Factorial", "n! = 1·2·…·n. Clave: 0! = 1 por definición."), ("Acumulador de producto", "variable que empieza en 1 y se multiplica. Clave: 1 es el neutro del producto.")],
    "situacion": "El factorial aparece en combinatoria y probabilidad. Con un for de 1 a n se calcula directo; el caso `0! = 1` sale gratis porque el bucle no se ejecuta y el acumulador queda en 1.",
    "entrada": "un entero `n` (0 <= n <= 20)",
    "salida": "`factorial=<n!>`",
    "formula": "n! = 1·2·…·n ; 0! = 1",
    "algoritmo": "LEER n\nf <- 1\nPARA i de 1 a n: f <- f*i\nESCRIBIR \"factorial=\" f",
    "casos": [("5", "factorial=120"), ("1", "factorial=1"), ("0", "factorial=1")],
    "comparacion": [("Sintáctica", "`for i in range(1,n+1)` (Python) vs. `for(i=1;i<=n;i++)` (C/Java) vs. `for i in 1..=n` (Rust)."), ("Semántica", "El for-range evita el error de límites; el for clásico lo deja en tus manos."), ("Paradigmática", "SQL usa un CTE recursivo o una agregación, no un for.")],
    "familia": "En Ruby `(1..n).reduce(1, :*)`. En Go `for i := 1; i <= n; i++`. Kotlin `for (i in 1..n)`.",
    "errores": [("Empezar el acumulador en 0", "el producto siempre da 0", "iniciar el acumulador de producto en 1"), ("Límites del rango mal", "un factor de más o de menos", "verificar con 0! y 1! que el rango es correcto")],
    "faq": [("¿Por qué long y no int?", "El factorial crece muy rápido; 21! ya desborda 64 bits. Aquí n<=20."), ("¿0! por qué es 1?", "Es el producto vacío: el neutro de la multiplicación es 1.")],
    "reto": "Calcula la suma de factoriales de 1 a n y resuélvelo en **Rust** con `for i in 1..=n`.",
    "impls": {
        "python": r"""import sys

n = int(sys.stdin.readline())
f = 1
for i in range(1, n + 1):
    f *= i
print(f"factorial={f}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let f = 1;
for (let i = 1; i <= n; i++) {
  f *= i;
}
console.log(`factorial=${f}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let f = 1;
for (let i = 1; i <= n; i++) {
  f *= i;
}
console.log(`factorial=${f}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        long f = 1;
        for (int i = 1; i <= n; i++) {
            f *= i;
        }
        System.out.println("factorial=" + f);
    }
}
""",
        "csharp": r"""using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long f = 1;
for (int i = 1; i <= n; i++) {
    f *= i;
}
Console.WriteLine($"factorial={f}");
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
	var f int64 = 1
	for i := 1; i <= n; i++ {
		f *= int64(i)
	}
	fmt.Printf("factorial=%d\n", f)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut f: i64 = 1;
    for i in 1..=n {
        f *= i;
    }
    println!("factorial={f}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long f = 1;
    for (long i = 1; i <= n; i++) {
        f *= i;
    }
    printf("factorial=%ld\n", f);
    return 0;
}
""",
        "php": r"""<?php
$n = (int) trim(fgets(STDIN));
$f = 1;
for ($i = 1; $i <= $n; $i++) {
    $f *= $i;
}
echo "factorial=$f\n";
""",
        "sql": r"""-- SQL: factorial con CTE recursivo (ilustrativo, n=5).
WITH RECURSIVE fact(i, f) AS (
    VALUES (1, 1)
    UNION ALL SELECT i + 1, f * (i + 1) FROM fact WHERE i < 5
)
SELECT printf('factorial=%d', f) AS resultado FROM fact ORDER BY i DESC LIMIT 1;
""",
    },
}

S[65] = {
    "descripcion": "Sumar todos los enteros de una lista recibida por la entrada.",
    "objetivo": "Recorrer una colección con `for-each` (para cada elemento), sin gestionar índices. Es la forma idiomática de procesar listas en casi todos los lenguajes.",
    "resultados": ["Recorrer una colección con for-each.", "Acumular un resultado sobre todos los elementos.", "Leer una lista de longitud variable."],
    "temas": [("for-each", "Para cada elemento, sin índice"), ("Colección", "Una secuencia de valores"), ("Acumulación", "Sumar recorriendo"), ("Longitud variable", "No se sabe cuántos hay de antemano")],
    "definiciones": [("for-each", "bucle que recorre cada elemento de una colección. Clave: sin índice manual."), ("Colección", "estructura que agrupa varios valores (lista, arreglo). Clave: se recorre en orden."), ("Iterar", "visitar cada elemento una vez. Clave: base del procesamiento de datos."), ("Acumulación", "reunir un resultado (suma) recorriendo. Clave: patrón universal.")],
    "situacion": "Sumar una lista de precios, contar elementos, buscar un máximo: todo empieza recorriendo la colección. El for-each expresa 'para cada elemento' sin el ruido del índice.",
    "entrada": "una línea con enteros separados por espacio",
    "salida": "`suma=<suma de todos>`",
    "formula": "suma = Σ elementos",
    "algoritmo": "LEER lista\nsuma <- 0\nPARA CADA x EN lista: suma <- suma + x\nESCRIBIR \"suma=\" suma",
    "casos": [("3 1 4", "suma=8"), ("10 20 30", "suma=60"), ("5", "suma=5")],
    "comparacion": [("Sintáctica", "`for x in lista` (Python) vs. `for (int x : arr)` (Java) vs. `for x in &v` (Rust)."), ("Semántica", "Todos recorren sin índice; C aún usa índice o puntero."), ("Paradigmática", "SQL suma con `SUM()` sobre filas, sin bucle explícito.")],
    "familia": "En Ruby `lista.each` o `lista.sum`. En Go `for _, x := range xs`. Kotlin `for (x in xs)`.",
    "errores": [("Usar índice cuando no hace falta", "código más largo y con más errores", "usar for-each cuando solo necesitas el valor"), ("Olvidar inicializar el acumulador", "resultado incorrecto", "empezar la suma en 0")],
    "faq": [("¿for-each o for con índice?", "for-each si solo necesitas el valor; con índice si también necesitas la posición."), ("¿Cómo leo una lista de tamaño desconocido?", "Leyendo toda la línea/entrada y separando por espacios.")],
    "reto": "Calcula también el promedio y resuélvelo en **Go** con `range`.",
    "impls": {
        "python": r"""import sys

nums = [int(x) for x in sys.stdin.read().split()]
suma = 0
for x in nums:
    suma += x
print(f"suma={suma}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let suma = 0;
for (const x of nums) {
  suma += x;
}
console.log(`suma=${suma}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let suma = 0;
for (const x of nums) {
  suma += x;
}
console.log(`suma=${suma}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        long suma = 0;
        for (String s : p) {
            suma += Integer.parseInt(s);
        }
        System.out.println("suma=" + suma);
    }
}
""",
        "csharp": r"""using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long suma = 0;
foreach (string s in p) {
    suma += int.Parse(s);
}
Console.WriteLine($"suma={suma}");
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
	data, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	suma := 0
	for _, s := range strings.Fields(data) {
		n, _ := strconv.Atoi(s)
		suma += n
	}
	fmt.Printf("suma=%d\n", suma)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let mut suma = 0i64;
    for x in &nums {
        suma += x;
    }
    println!("suma={suma}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long suma = 0, x;
    while (scanf("%ld", &x) == 1) {
        suma += x;
    }
    printf("suma=%ld\n", suma);
    return 0;
}
""",
        "php": r"""<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$suma = 0;
foreach ($nums as $x) {
    $suma += (int) $x;
}
echo "suma=$suma\n";
""",
        "sql": r"""-- SQL: SUM() agrega sobre las filas, sin bucle.
WITH nums(x) AS (VALUES (3), (1), (4))
SELECT printf('suma=%d', sum(x)) AS resultado FROM nums;
""",
    },
}

S[66] = {
    "descripcion": "Generar los primeros n números pares positivos (2, 4, 6, ...).",
    "objetivo": "Producir una secuencia bajo demanda, la idea detrás de los **iteradores y generadores perezosos**: calcular los valores uno a uno en lugar de tener toda la lista de antemano.",
    "resultados": ["Generar una secuencia de longitud n.", "Reconocer la evaluación perezosa (lazy).", "Distinguir generar de tener ya calculado."],
    "temas": [("Generar bajo demanda", "Producir valores al pedirlos"), ("Perezoso (lazy)", "No calcular hasta que se necesita"), ("Iterador", "Objeto que entrega el siguiente valor"), ("take n", "Tomar solo los primeros n")],
    "definiciones": [("Iterador", "objeto que produce valores uno a uno. Clave: no necesita toda la colección en memoria."), ("Generador", "función que produce una secuencia perezosa (yield). Clave: calcula al vuelo."), ("Evaluación perezosa", "calcular un valor solo cuando se pide. Clave: permite secuencias infinitas."), ("take", "tomar los primeros n de una secuencia. Clave: corta lo infinito.")],
    "situacion": "Los pares no tienen fin. Con un generador perezoso pides 'los primeros n' sin construir una lista infinita: cada valor se calcula cuando lo necesitas. Es como abrir el grifo solo lo justo.",
    "entrada": "un entero `n` (n >= 1)",
    "salida": "`pares=<2-4-...-2n>`",
    "formula": "pares_i = 2·i para i de 1 a n",
    "algoritmo": "LEER n\nPARA i de 1 a n: emitir 2*i\nESCRIBIR \"pares=\" UNIR(emitidos, \"-\")",
    "casos": [("3", "pares=2-4-6"), ("1", "pares=2"), ("5", "pares=2-4-6-8-10")],
    "comparacion": [("Sintáctica", "`(2*i for i in ...)` (Python) vs. `(1..=n).map(...)` (Rust) vs. bucle (C/Java)."), ("Semántica", "Python/Rust generan perezosamente; C/Java construyen la lista al vuelo."), ("Paradigmática", "SQL genera con un CTE recursivo.")],
    "familia": "En Ruby `(1..n).map { |i| i*2 }` o un `Enumerator` perezoso. En Haskell `take n [2,4..]` sobre una lista infinita.",
    "errores": [("Construir una lista infinita entera", "memoria agotada", "generar perezosamente y tomar solo n"), ("Olvidar el separador en n=1", "un guion sobrante", "unir con el separador, no anteponerlo")],
    "faq": [("¿Qué gana la pereza?", "Trabajar con secuencias enormes o infinitas usando solo lo que consumes."), ("¿Python genera perezoso?", "Sí, con generadores (`yield`) y expresiones generadoras `( ... for ... )`.")],
    "reto": "Genera los primeros n múltiplos de 3 y resuélvelo en **Python** con un generador (`yield`).",
    "impls": {
        "python": r"""import sys

n = int(sys.stdin.readline())
pares = (2 * i for i in range(1, n + 1))
print("pares=" + "-".join(str(x) for x in pares))
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const pares = [];
for (let i = 1; i <= n; i++) pares.push(2 * i);
console.log(`pares=${pares.join("-")}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const pares: number[] = [];
for (let i = 1; i <= n; i++) pares.push(2 * i);
console.log(`pares=${pares.join("-")}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= n; i++) {
            if (i > 1) sb.append("-");
            sb.append(2 * i);
        }
        System.out.println("pares=" + sb);
    }
}
""",
        "csharp": r"""using System;
using System.Linq;

int n = int.Parse(Console.In.ReadToEnd().Trim());
var pares = Enumerable.Range(1, n).Select(i => 2 * i);
Console.WriteLine($"pares={string.Join("-", pares)}");
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
	var sb strings.Builder
	for i := 1; i <= n; i++ {
		if i > 1 {
			sb.WriteString("-")
		}
		sb.WriteString(strconv.Itoa(2 * i))
	}
	fmt.Printf("pares=%s\n", sb.String())
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let pares: Vec<String> = (1..=n).map(|i| (2 * i).to_string()).collect();
    println!("pares={}", pares.join("-"));
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("pares=");
    for (long i = 1; i <= n; i++) {
        if (i > 1) printf("-");
        printf("%ld", 2 * i);
    }
    printf("\n");
    return 0;
}
""",
        "php": r"""<?php
$n = (int) trim(fgets(STDIN));
$pares = [];
for ($i = 1; $i <= $n; $i++) {
    $pares[] = 2 * $i;
}
echo "pares=" . implode("-", $pares) . "\n";
""",
        "sql": r"""-- SQL: genera los pares con un CTE recursivo (ilustrativo, n=5).
WITH RECURSIVE pares(i, v) AS (
    VALUES (1, 2)
    UNION ALL SELECT i + 1, (i + 1) * 2 FROM pares WHERE i < 5
)
SELECT 'pares=' || group_concat(v, '-') AS resultado FROM pares;
""",
    },
}

S[67] = {
    "descripcion": "De una lista de enteros, quedarse solo con los pares.",
    "objetivo": "Filtrar una colección con una **comprensión** (list comprehension): construir una nueva lista seleccionando elementos que cumplen una condición, de forma declarativa y compacta.",
    "resultados": ["Filtrar una colección con una comprensión.", "Expresar 'los que cumplen X' de forma declarativa.", "Comparar la comprensión con el bucle equivalente."],
    "temas": [("Comprensión", "Construir una lista describiéndola"), ("Filtro", "Quedarse con los que cumplen"), ("Declarativo", "Decir qué, no cómo"), ("Comprensión vs. bucle", "Más compacto y legible")],
    "definiciones": [("Comprensión de lista", "expresión que construye una lista filtrando/transformando otra. Clave: declarativa y compacta."), ("Filtro", "condición que decide qué elementos entran. Clave: `if x % 2 == 0`."), ("Predicado", "condición booleana sobre cada elemento. Clave: define el filtro."), ("Estilo declarativo", "describir el resultado, no los pasos. Clave: menos ruido que el bucle.")],
    "situacion": "Quedarse con los pedidos pagados, los usuarios activos, los números pares: filtrar es constante. La comprensión `[x for x in lista if x%2==0]` dice justo eso en una línea.",
    "entrada": "una línea con enteros separados por espacio (al menos un par)",
    "salida": "`pares=<los pares unidos por -, en orden>`",
    "formula": "pares = [x ∈ lista : x par]",
    "algoritmo": "LEER lista\npares <- [x EN lista SI x es par]\nESCRIBIR \"pares=\" UNIR(pares, \"-\")",
    "casos": [("1 2 3 4", "pares=2-4"), ("10 15 20", "pares=10-20"), ("6 7 8", "pares=6-8")],
    "comparacion": [("Sintáctica", "`[x for x in l if x%2==0]` (Python) vs. `l.filter(...)` (JS/Rust) vs. bucle (C)."), ("Semántica", "La comprensión crea una lista nueva; el original no cambia."), ("Paradigmática", "SQL filtra con `WHERE x % 2 = 0`.")],
    "familia": "En Ruby `lista.select { |x| x.even? }`. En Haskell `[x | x <- xs, even x]`, de donde Python tomó la idea.",
    "errores": [("Modificar la lista mientras la recorres", "resultados imprevisibles", "construir una lista nueva con la comprensión"), ("Confundir filtrar con transformar", "cambiar valores en vez de seleccionarlos", "filtrar mantiene los elementos; map los transforma")],
    "faq": [("¿Comprensión o filter?", "Equivalentes; la comprensión es más legible en Python, `filter` en JS/Rust."), ("¿Es más lento que un bucle?", "No de forma significativa; suele ser igual o más rápido y más claro.")],
    "reto": "Quédate con los impares mayores que 5 y resuélvelo en **JavaScript** con `filter`.",
    "impls": {
        "python": r"""import sys

nums = [int(x) for x in sys.stdin.read().split()]
pares = [x for x in nums if x % 2 == 0]
print("pares=" + "-".join(str(x) for x in pares))
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const pares = nums.filter((x) => x % 2 === 0);
console.log(`pares=${pares.join("-")}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const pares: number[] = nums.filter((x) => x % 2 === 0);
console.log(`pares=${pares.join("-")}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        String pares = Arrays.stream(p)
                .map(Integer::parseInt)
                .filter(x -> x % 2 == 0)
                .map(String::valueOf)
                .collect(Collectors.joining("-"));
        System.out.println("pares=" + pares);
    }
}
""",
        "csharp": r"""using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var pares = p.Select(int.Parse).Where(x => x % 2 == 0);
Console.WriteLine($"pares={string.Join("-", pares)}");
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
	var pares []string
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		if n%2 == 0 {
			pares = append(pares, strconv.Itoa(n))
		}
	}
	fmt.Printf("pares=%s\n", strings.Join(pares, "-"))
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let pares: Vec<String> = s
        .split_whitespace()
        .map(|x| x.parse::<i64>().unwrap())
        .filter(|x| x % 2 == 0)
        .map(|x| x.to_string())
        .collect();
    println!("pares={}", pares.join("-"));
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long x;
    int primero = 1;
    printf("pares=");
    while (scanf("%ld", &x) == 1) {
        if (x % 2 == 0) {
            if (!primero) printf("-");
            printf("%ld", x);
            primero = 0;
        }
    }
    printf("\n");
    return 0;
}
""",
        "php": r"""<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$pares = array_filter($nums, fn($x) => (int) $x % 2 === 0);
echo "pares=" . implode("-", $pares) . "\n";
""",
        "sql": r"""-- SQL: filtra con WHERE.
WITH nums(x) AS (VALUES (1), (2), (3), (4))
SELECT 'pares=' || group_concat(x, '-') AS resultado FROM nums WHERE x % 2 = 0;
""",
    },
}

S[68] = {
    "descripcion": "De una lista de enteros, duplicar cada uno (map) y sumar los resultados (reduce).",
    "objetivo": "Combinar las tres funciones de orden superior clásicas: **map** (transformar cada elemento), **filter** (seleccionar) y **reduce** (combinar en un valor). Aquí se usan map y reduce sobre una lista.",
    "resultados": ["Transformar una colección con map.", "Combinar una colección con reduce.", "Encadenar operaciones de orden superior."],
    "temas": [("map", "Transformar cada elemento"), ("reduce", "Combinar en un solo valor"), ("Funciones de orden superior", "Reciben otra función"), ("Encadenar", "map y luego reduce")],
    "definiciones": [("map", "aplica una función a cada elemento y devuelve una colección nueva. Clave: transforma sin mutar."), ("reduce", "combina todos los elementos en un valor (suma, producto). Clave: acumula."), ("Función de orden superior", "recibe o devuelve otra función. Clave: base del estilo funcional."), ("Encadenamiento", "conectar operaciones (map → reduce). Clave: pipeline de datos.")],
    "situacion": "Calcular el total de una factura con IVA: `map` aplica el IVA a cada línea y `reduce` las suma. map/filter/reduce son el lenguaje común del procesamiento de datos.",
    "entrada": "una línea con enteros separados por espacio",
    "salida": "`doblados=<cada x·2 unidos por -> total=<suma de los doblados>`",
    "formula": "doblados = map(x→2x) ; total = reduce(+, doblados)",
    "algoritmo": "LEER lista\ndoblados <- MAP(x -> 2x, lista)\ntotal <- REDUCE(+, doblados)\nESCRIBIR \"doblados=\" UNIR(doblados,\"-\") \" total=\" total",
    "casos": [("1 2 3", "doblados=2-4-6 total=12"), ("5", "doblados=10 total=10"), ("2 4", "doblados=4-8 total=12")],
    "comparacion": [("Sintáctica", "`map`/`sum` (Python) vs. `.map().reduce()` (JS) vs. `.iter().map().sum()` (Rust)."), ("Semántica", "map/reduce no mutan la lista original; devuelven valores nuevos."), ("Paradigmática", "SQL hace el 'map' en el SELECT y el 'reduce' con SUM().")],
    "familia": "En Ruby `lista.map { |x| x*2 }.sum`. En Haskell `sum (map (*2) xs)`, el origen de este estilo.",
    "errores": [("Mutar dentro del map", "efectos secundarios inesperados", "usar map para transformar, sin cambiar estado externo"), ("Confundir map con for-each", "map devuelve una colección; for-each no", "usar map cuando quieres el resultado transformado")],
    "faq": [("¿reduce es lo mismo que un bucle de suma?", "Sí en esencia; reduce lo expresa de forma declarativa y reutilizable."), ("¿Y filter?", "Selecciona elementos; aquí no se usó, pero completa el trío map/filter/reduce.")],
    "reto": "Filtra los pares, dóblalos y súmalos (map+filter+reduce) y resuélvelo en **Rust** con iteradores.",
    "impls": {
        "python": r"""import sys

nums = [int(x) for x in sys.stdin.read().split()]
doblados = [x * 2 for x in nums]
total = sum(doblados)
print(f"doblados={'-'.join(str(x) for x in doblados)} total={total}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const doblados = nums.map((x) => x * 2);
const total = doblados.reduce((a, b) => a + b, 0);
console.log(`doblados=${doblados.join("-")} total=${total}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const doblados: number[] = nums.map((x) => x * 2);
const total: number = doblados.reduce((a, b) => a + b, 0);
console.log(`doblados=${doblados.join("-")} total=${total}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        List<Integer> doblados = Arrays.stream(p)
                .map(Integer::parseInt)
                .map(x -> x * 2)
                .collect(Collectors.toList());
        int total = doblados.stream().mapToInt(Integer::intValue).sum();
        String s = doblados.stream().map(String::valueOf).collect(Collectors.joining("-"));
        System.out.println("doblados=" + s + " total=" + total);
    }
}
""",
        "csharp": r"""using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var doblados = p.Select(int.Parse).Select(x => x * 2).ToList();
int total = doblados.Sum();
Console.WriteLine($"doblados={string.Join("-", doblados)} total={total}");
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
	var doblados []string
	total := 0
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		d := n * 2
		doblados = append(doblados, strconv.Itoa(d))
		total += d
	}
	fmt.Printf("doblados=%s total=%d\n", strings.Join(doblados, "-"), total)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let doblados: Vec<i64> = s
        .split_whitespace()
        .map(|x| x.parse::<i64>().unwrap() * 2)
        .collect();
    let total: i64 = doblados.iter().sum();
    let texto: Vec<String> = doblados.iter().map(|x| x.to_string()).collect();
    println!("doblados={} total={}", texto.join("-"), total);
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long x, total = 0;
    int primero = 1;
    printf("doblados=");
    long primeros[1024];
    int k = 0;
    while (scanf("%ld", &x) == 1) {
        primeros[k++] = x * 2;
    }
    for (int i = 0; i < k; i++) {
        if (!primero) printf("-");
        printf("%ld", primeros[i]);
        total += primeros[i];
        primero = 0;
    }
    printf(" total=%ld\n", total);
    return 0;
}
""",
        "php": r"""<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$doblados = array_map(fn($x) => (int) $x * 2, $nums);
$total = array_reduce($doblados, fn($a, $b) => $a + $b, 0);
echo "doblados=" . implode("-", $doblados) . " total=$total\n";
""",
        "sql": r"""-- SQL: el 'map' va en el SELECT y el 'reduce' con SUM().
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT 'doblados=' || group_concat(x * 2, '-') || printf(' total=%d', sum(x * 2)) AS resultado
FROM nums;
""",
    },
}

S[69] = {
    "descripcion": "Calcular el n-ésimo número de Fibonacci con una función recursiva.",
    "objetivo": "Escribir una función **recursiva**: que se llama a sí misma con un caso base y un caso recursivo. Fibonacci es el ejemplo clásico; también sirve para hablar de eficiencia y de recursión de cola.",
    "resultados": ["Escribir una función recursiva con caso base.", "Traducir una definición recursiva a código.", "Reconocer el coste de la recursión ingenua."],
    "temas": [("Recursión", "Una función que se llama a sí misma"), ("Caso base", "Dónde para la recursión"), ("Caso recursivo", "Reducir hacia el caso base"), ("Coste", "Fibonacci ingenuo es exponencial")],
    "definiciones": [("Recursión", "técnica en que una función se invoca a sí misma. Clave: necesita un caso base."), ("Caso base", "el que se resuelve sin recursión. Clave: evita la recursión infinita."), ("Caso recursivo", "reduce el problema hacia el caso base. Clave: debe acercarse a él."), ("Recursión de cola", "la llamada recursiva es lo último que se hace. Clave: algunos lenguajes la optimizan.")],
    "situacion": "Fibonacci se define recursivamente: F(n)=F(n-1)+F(n-2). Traducirlo a código es directo, pero la versión ingenua repite cálculos: un buen punto para hablar de eficiencia (Parte 3, clase 045 de complejidad).",
    "entrada": "un entero `n` (0 <= n <= 30)",
    "salida": "`fib=<F(n)>`",
    "formula": "F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)",
    "algoritmo": "FUNCION fib(n): SI n<2 DEVOLVER n ; SINO DEVOLVER fib(n-1)+fib(n-2)",
    "casos": [("10", "fib=55"), ("1", "fib=1"), ("0", "fib=0")],
    "comparacion": [("Sintáctica", "`def fib` (Python), `func fib` (Go), `fn fib` (Rust) — todas se auto-invocan igual."), ("Semántica", "La pila de llamadas crece con la profundidad; ojo con el desbordamiento en recursiones profundas."), ("Paradigmática", "SQL expresa la recursión con un CTE recursivo, no con funciones.")],
    "familia": "En Ruby `def fib(n); n < 2 ? n : fib(n-1)+fib(n-2); end`. En Haskell la recursión es el modo natural de iterar.",
    "errores": [("Olvidar el caso base", "recursión infinita → desbordamiento de pila", "definir siempre el caso que corta la recursión"), ("Recursión ingenua para n grande", "coste exponencial", "usar memoización o una versión iterativa (aquí n<=30)")],
    "faq": [("¿La recursión es peor que el bucle?", "No en general; para Fibonacci ingenuo sí. Con memoización o cola, es eficiente."), ("¿Qué es la recursión de cola?", "Cuando la llamada recursiva es la última operación; permite optimizarla como un bucle.")],
    "reto": "Escribe una versión iterativa (sin recursión) y compárala; resuélvelo en **Go**.",
    "impls": {
        "python": r"""import sys


def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


n = int(sys.stdin.readline())
print(f"fib={fib(n)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

function fib(n) {
  return n < 2 ? n : fib(n - 1) + fib(n - 2);
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`fib=${fib(n)}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

function fib(n: number): number {
  return n < 2 ? n : fib(n - 1) + fib(n - 2);
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`fib=${fib(n)}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static long fib(int n) {
        return n < 2 ? n : fib(n - 1) + fib(n - 2);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        System.out.println("fib=" + fib(n));
    }
}
""",
        "csharp": r"""using System;

long Fib(int n) => n < 2 ? n : Fib(n - 1) + Fib(n - 2);

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"fib={Fib(n)}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func fib(n int) int64 {
	if n < 2 {
		return int64(n)
	}
	return fib(n-1) + fib(n-2)
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	fmt.Printf("fib=%d\n", fib(n))
}
""",
        "rust": r"""use std::io::Read;

fn fib(n: i64) -> i64 {
    if n < 2 {
        n
    } else {
        fib(n - 1) + fib(n - 2)
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("fib={}", fib(n));
}
""",
        "c": r"""#include <stdio.h>

long fib(long n) {
    return n < 2 ? n : fib(n - 1) + fib(n - 2);
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("fib=%ld\n", fib(n));
    return 0;
}
""",
        "php": r"""<?php
function fib($n) {
    return $n < 2 ? $n : fib($n - 1) + fib($n - 2);
}

$n = (int) trim(fgets(STDIN));
echo "fib=" . fib($n) . "\n";
""",
        "sql": r"""-- SQL: Fibonacci con un CTE recursivo (ilustrativo, n=10).
WITH RECURSIVE fib(i, a, b) AS (
    VALUES (0, 0, 1)
    UNION ALL SELECT i + 1, b, a + b FROM fib WHERE i < 10
)
SELECT printf('fib=%d', a) AS resultado FROM fib WHERE i = 10;
""",
    },
}

S[70] = {
    "descripcion": "Encontrar el menor divisor de n mayor que 1, deteniendo el bucle al encontrarlo (break).",
    "objetivo": "Usar `break` para salir de un bucle en cuanto se cumple una condición. Buscar el primer divisor es el caso típico: no hace falta seguir una vez encontrado.",
    "resultados": ["Salir de un bucle con break.", "Reconocer cuándo continue u otras salidas ayudan.", "Evitar trabajo innecesario tras encontrar lo buscado."],
    "temas": [("break", "Salir del bucle inmediatamente"), ("continue", "Saltar a la siguiente vuelta"), ("Búsqueda con parada", "Detenerse al encontrar"), ("return dentro del bucle", "Otra forma de salir")],
    "definiciones": [("break", "termina el bucle inmediatamente. Clave: no sigue iterando."), ("continue", "salta al siguiente ciclo del bucle. Clave: ignora el resto de la vuelta."), ("Divisor", "número que divide a otro sin resto. Clave: el menor >1 revela si es primo."), ("goto", "salto incondicional (existe en C, desaconsejado). Clave: break/continue lo sustituyen.")],
    "situacion": "Para saber si un número es primo, buscas su primer divisor >1: si es él mismo, es primo. En cuanto lo encuentras, `break` evita seguir dividiendo en vano.",
    "entrada": "un entero `n` (n >= 2)",
    "salida": "`primer_divisor=<el menor divisor > 1>`",
    "formula": "el menor d en [2..n] tal que n % d == 0",
    "algoritmo": "LEER n\nPARA d de 2 a n: SI n%d==0: guardar d ; ROMPER\nESCRIBIR \"primer_divisor=\" d",
    "casos": [("15", "primer_divisor=3"), ("7", "primer_divisor=7"), ("12", "primer_divisor=2")],
    "comparacion": [("Sintáctica", "`break` es igual en casi todos; C mantiene `goto` (evitar)."), ("Semántica", "break sale del bucle más interno; algunos lenguajes tienen break etiquetado."), ("Paradigmática", "SQL evita el bucle: usa MIN sobre los divisores o una consulta.")],
    "familia": "En Ruby `break`. En Go `break` (y `break label` para bucles anidados). Rust tiene `break` que incluso puede devolver un valor.",
    "errores": [("Seguir iterando tras encontrar", "trabajo desperdiciado", "usar break en cuanto se cumple la condición"), ("Confundir break con continue", "no salir cuando debías", "break termina el bucle; continue solo salta una vuelta")],
    "faq": [("¿break sale de todos los bucles?", "Solo del más interno; para varios, usa etiquetas (Java/Go) o reestructura."), ("¿Y goto?", "Existe en C pero se evita; break/continue/return cubren casi todo de forma clara.")],
    "reto": "Determina además si n es primo (`primo=true/false`) y resuélvelo en **Rust** con `break`.",
    "impls": {
        "python": r"""import sys

n = int(sys.stdin.readline())
d = 2
while d <= n:
    if n % d == 0:
        break
    d += 1
print(f"primer_divisor={d}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let d = 2;
for (; d <= n; d++) {
  if (n % d === 0) break;
}
console.log(`primer_divisor=${d}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let d = 2;
for (; d <= n; d++) {
  if (n % d === 0) break;
}
console.log(`primer_divisor=${d}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int d = 2;
        for (; d <= n; d++) {
            if (n % d == 0) break;
        }
        System.out.println("primer_divisor=" + d);
    }
}
""",
        "csharp": r"""using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int d = 2;
for (; d <= n; d++) {
    if (n % d == 0) break;
}
Console.WriteLine($"primer_divisor={d}");
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
	d := 2
	for ; d <= n; d++ {
		if n%d == 0 {
			break
		}
	}
	fmt.Printf("primer_divisor=%d\n", d)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut d = 2;
    while d <= n {
        if n % d == 0 {
            break;
        }
        d += 1;
    }
    println!("primer_divisor={d}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long d = 2;
    for (; d <= n; d++) {
        if (n % d == 0) break;
    }
    printf("primer_divisor=%ld\n", d);
    return 0;
}
""",
        "php": r"""<?php
$n = (int) trim(fgets(STDIN));
$d = 2;
for (; $d <= $n; $d++) {
    if ($n % $d === 0) {
        break;
    }
}
echo "primer_divisor=$d\n";
""",
        "sql": r"""-- SQL: el menor divisor > 1 con MIN sobre un rango (ilustrativo).
WITH RECURSIVE d(k) AS (VALUES (2) UNION ALL SELECT k + 1 FROM d WHERE k < 15)
SELECT printf('primer_divisor=%d', min(k)) AS resultado
FROM d WHERE 15 % k = 0;
""",
    },
}

S[71] = {
    "descripcion": "Dividir dos enteros y manejar la división por cero con una excepción.",
    "objetivo": "Manejar errores con **excepciones** (`try`/`catch`/`finally`): separar el camino feliz del manejo del error. Dividir por cero es el caso clásico que dispara una excepción en varios lenguajes.",
    "resultados": ["Capturar una excepción con try/catch.", "Distinguir el flujo normal del de error.", "Reconocer qué lenguajes lanzan y cuáles no."],
    "temas": [("Excepción", "Un error que interrumpe el flujo"), ("try/catch", "Intentar y capturar el fallo"), ("finally", "Código que corre pase lo que pase"), ("Lanzar vs. comprobar", "No todos lanzan en /0")],
    "definiciones": [("Excepción", "objeto que representa un error y desvía el flujo. Clave: se captura con try/catch."), ("try", "bloque que puede fallar. Clave: envuelve la operación arriesgada."), ("catch", "bloque que maneja la excepción. Clave: el plan B ante el error."), ("finally", "bloque que se ejecuta siempre (haya error o no). Clave: liberar recursos.")],
    "situacion": "Dividir entre cero es un error clásico. En Java, C#, Python y PHP la división entera por cero lanza una excepción; capturarla evita que el programa termine abruptamente.",
    "entrada": "una línea `a b` (dos enteros)",
    "salida": "`resultado=<a/b entera>` o `error=division por cero` si b es 0",
    "formula": "si b != 0 → a/b (entera); si b == 0 → mensaje de error",
    "algoritmo": "LEER a, b\nINTENTAR: r <- a/b ; ESCRIBIR \"resultado=\" r\nCAPTURAR division_por_cero: ESCRIBIR \"error=division por cero\"",
    "casos": [("10 2", "resultado=5"), ("7 0", "error=division por cero"), ("9 3", "resultado=3")],
    "comparacion": [("Sintáctica", "`try/except` (Python), `try/catch` (Java/C#/JS/PHP)."), ("Semántica", "Java/C#/Python/PHP lanzan en /0 entero; JS da Infinity (hay que comprobar); Go/Rust no usan excepciones."), ("Paradigmática", "SQL evita el error con CASE WHEN b=0.")],
    "familia": "En Ruby `begin/rescue/ensure`. En Kotlin `try/catch/finally`, como Java. Go y Rust prefieren valores de error (siguiente clase).",
    "errores": [("Capturar todo con un catch vacío", "ocultar errores reales", "capturar solo lo esperado y actuar"), ("Asumir que /0 siempre lanza", "en JS da Infinity, no excepción", "comprobar el divisor o el resultado según el lenguaje")],
    "faq": [("¿Excepciones o valores de error?", "Excepciones para lo excepcional; valores (Result) para errores esperables. La siguiente clase compara."), ("¿Para qué el finally?", "Para liberar recursos (archivos, conexiones) ocurra o no un error.")],
    "reto": "Añade un `finally` que imprima 'fin' siempre y resuélvelo en **Python** con try/except/finally.",
    "impls": {
        "python": r"""import sys

a, b = map(int, sys.stdin.readline().split())
try:
    r = a // b
    print(f"resultado={r}")
except ZeroDivisionError:
    print("error=division por cero")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
try {
  if (b === 0) throw new Error("div");
  console.log(`resultado=${Math.trunc(a / b)}`);
} catch {
  console.log("error=division por cero");
}
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
try {
  if (b === 0) throw new Error("div");
  console.log(`resultado=${Math.trunc(a / b)}`);
} catch {
  console.log("error=division por cero");
}
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
        try {
            int r = a / b;
            System.out.println("resultado=" + r);
        } catch (ArithmeticException e) {
            System.out.println("error=division por cero");
        }
    }
}
""",
        "csharp": r"""using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
try {
    int r = a / b;
    Console.WriteLine($"resultado={r}");
} catch (DivideByZeroException) {
    Console.WriteLine("error=division por cero");
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
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	// Go no usa excepciones: comprueba antes de dividir.
	if b == 0 {
		fmt.Println("error=division por cero")
	} else {
		fmt.Printf("resultado=%d\n", a/b)
	}
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let (a, b) = (v[0], v[1]);
    // Rust no usa excepciones: checked_div devuelve Option.
    match a.checked_div(b) {
        Some(r) => println!("resultado={r}"),
        None => println!("error=division por cero"),
    }
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    /* C no tiene excepciones: comprobar antes de dividir. */
    if (b == 0) {
        printf("error=division por cero\n");
    } else {
        printf("resultado=%ld\n", a / b);
    }
    return 0;
}
""",
        "php": r"""<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;
try {
    $r = intdiv($a, $b);
    echo "resultado=$r\n";
} catch (DivisionByZeroError $e) {
    echo "error=division por cero\n";
}
""",
        "sql": r"""-- SQL: evita el error comprobando el divisor con CASE WHEN.
WITH pares(a, b) AS (VALUES (10, 2), (7, 0), (9, 3))
SELECT CASE WHEN b = 0 THEN 'error=division por cero'
            ELSE printf('resultado=%d', a / b) END AS resultado
FROM pares;
""",
    },
}

S[72] = {
    "descripcion": "Dividir dos enteros devolviendo un resultado tipo Result/Either en lugar de lanzar una excepción.",
    "objetivo": "Manejar errores con **valores** en vez de excepciones: `Result`/`Either` (Rust, Haskell), el par `(valor, error)` de Go, u `Option`. El error deja de ser un salto de flujo y pasa a ser un dato que se maneja explícitamente.",
    "resultados": ["Representar el error como un valor de retorno.", "Manejar el resultado con match o comprobación.", "Comparar excepciones con valores de error."],
    "temas": [("Errores como valores", "El error es un dato, no un salto"), ("Result / Either", "Éxito o fallo tipado"), ("El par (valor, error) de Go", "Convención idiomática"), ("Manejo explícito", "No se puede ignorar por accidente")],
    "definiciones": [("Result/Either", "tipo que contiene un valor de éxito o uno de error (Rust, Haskell). Clave: obliga a manejar ambos."), ("Valor de error", "devolver el error como dato en lugar de lanzarlo. Clave: flujo explícito."), ("Convención de Go", "devolver `(valor, error)` y comprobar `if err != nil`. Clave: errores visibles."), ("Manejo explícito", "el compilador o el estilo obligan a tratar el error. Clave: menos fallos silenciosos.")],
    "situacion": "En Go y Rust el error no se lanza: se devuelve. `func div(a,b) (int, error)` obliga a comprobar `err` antes de usar el valor. El error se vuelve visible en la firma, no una sorpresa.",
    "entrada": "una línea `a b` (dos enteros)",
    "salida": "`ok=<a/b entera>` o `err=division` si b es 0",
    "formula": "si b != 0 → Ok(a/b); si b == 0 → Err(division)",
    "algoritmo": "LEER a, b\nres <- dividir(a,b)  // devuelve Ok(v) o Err\nSEGUN res: Ok(v)->\"ok=\"v ; Err->\"err=division\"",
    "casos": [("10 2", "ok=5"), ("7 0", "err=division"), ("8 4", "ok=2")],
    "comparacion": [("Sintáctica", "`Result`/`match` (Rust) vs. `(v, err)` (Go) vs. if/else (otros)."), ("Semántica", "Rust/Go obligan a manejar el error; ignorarlo es visible o imposible."), ("Paradigmática", "SQL usa CASE WHEN, sin tipo de error.")],
    "familia": "En Haskell `Either String Int` con `case`. En Kotlin, un `sealed class` o `Result`. Es el estilo opuesto a las excepciones de la clase anterior.",
    "errores": [("Ignorar el error devuelto", "usar un valor inválido", "comprobar siempre el error antes del valor (Go) o usar match (Rust)"), ("Mezclar excepciones y valores sin criterio", "manejo de errores inconsistente", "elegir un estilo por proyecto y ser coherente")],
    "faq": [("¿Result o excepciones?", "Result para errores esperables y explícitos; excepciones para lo verdaderamente excepcional."), ("¿Por qué Go no tiene excepciones?", "Prefiere errores como valores para que el manejo sea explícito y visible.")],
    "reto": "Haz que `div` devuelva también el resto (`ok=<coc> resto=<r>`) y resuélvelo en **Go** con `(int, int, error)`.",
    "impls": {
        "python": r"""import sys


def dividir(a, b):
    if b == 0:
        return (None, "division")
    return (a // b, None)


a, b = map(int, sys.stdin.readline().split())
valor, err = dividir(a, b)
if err is not None:
    print(f"err={err}")
else:
    print(f"ok={valor}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

function dividir(a, b) {
  if (b === 0) return { err: "division" };
  return { ok: Math.trunc(a / b) };
}

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const r = dividir(a, b);
console.log(r.err ? `err=${r.err}` : `ok=${r.ok}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

type Res = { ok: number } | { err: string };

function dividir(a: number, b: number): Res {
  if (b === 0) return { err: "division" };
  return { ok: Math.trunc(a / b) };
}

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const r = dividir(a, b);
console.log("err" in r ? `err=${r.err}` : `ok=${r.ok}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Optional;

public class Main {
    static Optional<Integer> dividir(int a, int b) {
        return b == 0 ? Optional.empty() : Optional.of(a / b);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]);
        int b = Integer.parseInt(p[1]);
        Optional<Integer> r = dividir(a, b);
        System.out.println(r.isPresent() ? "ok=" + r.get() : "err=division");
    }
}
""",
        "csharp": r"""using System;

(int? ok, string err) Dividir(int a, int b) =>
    b == 0 ? (null, "division") : (a / b, null);

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
var (ok, err) = Dividir(a, b);
Console.WriteLine(err != null ? $"err={err}" : $"ok={ok}");
""",
        "go": r"""package main

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func dividir(a, b int) (int, error) {
	if b == 0 {
		return 0, errors.New("division")
	}
	return a / b, nil
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	res, err := dividir(a, b)
	if err != nil {
		fmt.Printf("err=%s\n", err)
	} else {
		fmt.Printf("ok=%d\n", res)
	}
}
""",
        "rust": r"""use std::io::Read;

fn dividir(a: i64, b: i64) -> Result<i64, String> {
    if b == 0 {
        Err("division".to_string())
    } else {
        Ok(a / b)
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    match dividir(v[0], v[1]) {
        Ok(r) => println!("ok={r}"),
        Err(e) => println!("err={e}"),
    }
}
""",
        "c": r"""#include <stdio.h>

/* C: se usa un valor de retorno para señalar el error (0 = ok, 1 = error). */
int dividir(long a, long b, long *out) {
    if (b == 0) return 1;
    *out = a / b;
    return 0;
}

int main(void) {
    long a, b, r;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    if (dividir(a, b, &r) != 0) {
        printf("err=division\n");
    } else {
        printf("ok=%ld\n", r);
    }
    return 0;
}
""",
        "php": r"""<?php
function dividir($a, $b) {
    if ($b === 0) {
        return ["err" => "division"];
    }
    return ["ok" => intdiv($a, $b)];
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$r = dividir((int) $a, (int) $b);
echo isset($r["err"]) ? "err={$r['err']}\n" : "ok={$r['ok']}\n";
""",
        "sql": r"""-- SQL: sin tipo de error; se distingue el caso con CASE WHEN.
WITH pares(a, b) AS (VALUES (10, 2), (7, 0), (8, 4))
SELECT CASE WHEN b = 0 THEN 'err=division'
            ELSE printf('ok=%d', a / b) END AS resultado
FROM pares;
""",
    },
}


def main():
    for num, spec in S.items():
        g3.write_class(num, spec)
        print(f"Clase {num:03d} generada.")


if __name__ == "__main__":
    main()
