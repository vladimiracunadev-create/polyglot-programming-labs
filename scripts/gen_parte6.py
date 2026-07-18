"""Parte 6 — Datos y estructuras (clases 089-106). Reutiliza gen_parte3.write_class."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_parte3 as g3  # noqa: E402

S = {}

S[89] = {
    "descripcion": "Dado un arreglo fijo de tres enteros, calcular su suma y su máximo.",
    "objetivo": "Usar un **arreglo de tamaño fijo**: una secuencia contigua con un número de elementos conocido. Es la estructura más básica y la más cercana a la memoria.",
    "resultados": ["Declarar y recorrer un arreglo fijo.", "Acumular suma y máximo.", "Reconocer el acceso por índice."],
    "temas": [("Arreglo fijo", "Tamaño conocido, memoria contigua"), ("Índice", "Acceso por posición (base 0)"), ("Recorrido", "Visitar cada posición")],
    "definiciones": [("Arreglo", "colección de elementos contiguos indexados. Clave: acceso O(1) por índice."), ("Tamaño fijo", "número de elementos definido al crear. Clave: no crece."), ("Índice", "posición de un elemento, empezando en 0. Clave: `arr[0]` es el primero.")],
    "situacion": "Un arreglo fijo de 3 sensores, 12 meses, 7 días: cuando el tamaño se conoce, el arreglo fijo es la estructura más eficiente.",
    "entrada": "una línea `a b c` (tres enteros)",
    "salida": "`suma=<a+b+c> max=<el mayor>`",
    "formula": "suma y máximo de los tres elementos",
    "algoritmo": "LEER arr[3]\nsuma <- Σ arr ; max <- MAX(arr)\nESCRIBIR suma, max",
    "casos": [("3 1 4", "suma=8 max=4"), ("10 5 2", "suma=17 max=10"), ("1 1 1", "suma=3 max=1")],
    "comparacion": [("Sintáctica", "`[a, b, c]` (Python/JS), `int[]` (Java/C#), `[i64; 3]` (Rust), `long[3]` (C)."), ("Semántica", "En C el tamaño es parte del tipo; en Python/JS el arreglo es dinámico."), ("Paradigmática", "SQL agrega sobre filas, no índices.")],
    "familia": "En Go `[3]int` es fijo y `[]int` es slice dinámico. En C++ `std::array<int,3>`.",
    "errores": [("Salirse del índice", "acceso fuera de rango", "recorrer solo dentro del tamaño"), ("Confundir fijo con dinámico", "esperar que crezca", "usar lista/vector si el tamaño cambia")],
    "faq": [("¿Por qué base 0?", "El índice es un desplazamiento desde el inicio; el primero está a distancia 0."), ("¿Arreglo o lista?", "Arreglo fijo si el tamaño es constante; lista si varía (siguiente clase).")],
    "reto": "Calcula también el mínimo y resuélvelo en **Rust** con `[i64; 3]`.",
    "impls": {
        "python": r"""import sys

a, b, c = map(int, sys.stdin.readline().split())
arr = [a, b, c]
print(f"suma={sum(arr)} max={max(arr)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const arr = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${arr.reduce((a, b) => a + b, 0)} max=${Math.max(...arr)}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const arr: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${arr.reduce((a, b) => a + b, 0)} max=${Math.max(...arr)}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int[] arr = new int[3];
        for (int i = 0; i < 3; i++) arr[i] = Integer.parseInt(p[i]);
        int suma = 0, max = arr[0];
        for (int x : arr) {
            suma += x;
            if (x > max) max = x;
        }
        System.out.println("suma=" + suma + " max=" + max);
    }
}
""",
        "csharp": r"""using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int[] arr = p.Take(3).Select(int.Parse).ToArray();
Console.WriteLine($"suma={arr.Sum()} max={arr.Max()}");
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
	var arr [3]int
	for i := 0; i < 3; i++ {
		arr[i], _ = strconv.Atoi(f[i])
	}
	suma, max := 0, arr[0]
	for _, x := range arr {
		suma += x
		if x > max {
			max = x
		}
	}
	fmt.Printf("suma=%d max=%d\n", suma, max)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let arr: [i64; 3] = [v[0], v[1], v[2]];
    let suma: i64 = arr.iter().sum();
    let max = *arr.iter().max().unwrap();
    println!("suma={suma} max={max}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long arr[3];
    if (scanf("%ld %ld %ld", &arr[0], &arr[1], &arr[2]) != 3) return 1;
    long suma = 0, max = arr[0];
    for (int i = 0; i < 3; i++) {
        suma += arr[i];
        if (arr[i] > max) max = arr[i];
    }
    printf("suma=%ld max=%ld\n", suma, max);
    return 0;
}
""",
        "php": r"""<?php
[$a, $b, $c] = preg_split('/\s+/', trim(fgets(STDIN)));
$arr = [(int) $a, (int) $b, (int) $c];
echo "suma=" . array_sum($arr) . " max=" . max($arr) . "\n";
""",
        "sql": r"""-- SQL: agrega sobre filas, no índices.
WITH arr(x) AS (VALUES (3), (1), (4))
SELECT printf('suma=%d max=%d', sum(x), max(x)) AS resultado FROM arr;
""",
    },
}

S[90] = {
    "descripcion": "Invertir una lista dinámica de enteros.",
    "objetivo": "Usar una **lista/vector dinámico**: una secuencia que crece y encoge. Invertirla ejercita el recorrido y la construcción de una nueva secuencia.",
    "resultados": ["Construir y recorrer una lista dinámica.", "Invertir el orden de los elementos.", "Distinguir lista dinámica de arreglo fijo."],
    "temas": [("Lista dinámica", "Crece según haga falta"), ("Invertir", "Recorrer al revés"), ("Redimensionar", "Añadir/quitar elementos")],
    "definiciones": [("Lista/vector dinámico", "arreglo que cambia de tamaño (list, Vec, ArrayList). Clave: flexible."), ("append", "añadir un elemento al final. Clave: operación base."), ("Inversión", "producir la secuencia en orden contrario. Clave: primero pasa a último.")],
    "situacion": "Cuando no sabes cuántos elementos habrá (líneas de un archivo, respuestas de un usuario), la lista dinámica es la elección natural.",
    "entrada": "una línea con enteros separados por espacio",
    "salida": "`invertido=<elementos en orden inverso unidos por ->`",
    "formula": "invertido = reverse(lista)",
    "algoritmo": "LEER lista ; invertir ; ESCRIBIR unidos por -",
    "casos": [("1 2 3", "invertido=3-2-1"), ("5", "invertido=5"), ("10 20 30 40", "invertido=40-30-20-10")],
    "comparacion": [("Sintáctica", "`list[::-1]` (Python), `.reverse()` (JS/Rust), `Collections.reverse` (Java)."), ("Semántica", "Algunos invierten en sitio (mutando); otros crean una lista nueva."), ("Paradigmática", "SQL invierte con ORDER BY descendente sobre una posición.")],
    "familia": "En Ruby `lista.reverse`. En Go se invierte con un bucle de índices intercambiando extremos.",
    "errores": [("Confundir invertir en sitio con crear copia", "modificar el original sin querer", "elegir según necesites conservar el original"), ("Bucle de intercambio mal", "invertir de más y volver al inicio", "intercambiar solo hasta la mitad")],
    "faq": [("¿Lista o arreglo?", "Lista si el tamaño varía; arreglo fijo si es constante."), ("¿Invertir es caro?", "Es O(n): hay que tocar cada elemento una vez.")],
    "reto": "Invierte solo los elementos en posiciones pares y resuélvelo en **Go**.",
    "impls": {
        "python": r"""import sys

nums = [int(x) for x in sys.stdin.read().split()]
nums.reverse()
print("invertido=" + "-".join(str(x) for x in nums))
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
nums.reverse();
console.log(`invertido=${nums.join("-")}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
nums.reverse();
console.log(`invertido=${nums.join("-")}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        List<Integer> nums = new ArrayList<>();
        for (String s : p) nums.add(Integer.parseInt(s));
        Collections.reverse(nums);
        System.out.println("invertido=" + nums.stream().map(String::valueOf).collect(Collectors.joining("-")));
    }
}
""",
        "csharp": r"""using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var nums = p.Select(int.Parse).Reverse();
Console.WriteLine($"invertido={string.Join("-", nums)}");
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
	for i, j := 0, len(f)-1; i < j; i, j = i+1, j-1 {
		f[i], f[j] = f[j], f[i]
	}
	fmt.Printf("invertido=%s\n", strings.Join(f, "-"))
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut nums: Vec<&str> = s.split_whitespace().collect();
    nums.reverse();
    println!("invertido={}", nums.join("-"));
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    printf("invertido=");
    for (int i = n - 1; i >= 0; i--) {
        if (i < n - 1) printf("-");
        printf("%ld", v[i]);
    }
    printf("\n");
    return 0;
}
""",
        "php": r"""<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$nums = array_reverse($nums);
echo "invertido=" . implode("-", $nums) . "\n";
""",
        "sql": r"""-- SQL: invierte con ORDER BY sobre la posición.
WITH nums(pos, x) AS (VALUES (1, 1), (2, 2), (3, 3))
SELECT 'invertido=' || group_concat(x, '-') AS resultado
FROM (SELECT x FROM nums ORDER BY pos DESC);
""",
    },
}

S[91] = {
    "descripcion": "Recibir dos enteros como una tupla e intercambiar sus componentes.",
    "objetivo": "Usar **tuplas**: agrupar un número fijo de valores, posiblemente de tipos distintos, sin definir una clase. Se accede por posición y se desestructuran fácilmente.",
    "resultados": ["Crear y desestructurar una tupla.", "Acceder a los componentes por posición.", "Distinguir tupla de lista."],
    "temas": [("Tupla", "Grupo fijo y ordenado"), ("Componentes", "Acceso por posición"), ("Desestructuración", "Repartir en variables")],
    "definiciones": [("Tupla", "grupo ordenado de valores de tamaño fijo. Clave: liviana, sin definir un tipo."), ("Componente", "cada elemento de la tupla, por posición. Clave: `.0`, `[0]`."), ("Registro posicional", "estructura cuyos campos se identifican por orden. Clave: la tupla lo es.")],
    "situacion": "Devolver coordenadas `(x, y)`, un par clave/valor, o un resultado con dos partes: la tupla agrupa sin la ceremonia de una clase.",
    "entrada": "una línea `a b` (dos enteros)",
    "salida": "`tupla=(<b>, <a>)` (componentes intercambiados)",
    "formula": "(a, b) → (b, a)",
    "algoritmo": "LEER (a, b) ; intercambiar ; ESCRIBIR (b, a)",
    "casos": [("3 4", "tupla=(4, 3)"), ("0 -2", "tupla=(-2, 0)"), ("5 5", "tupla=(5, 5)")],
    "comparacion": [("Sintáctica", "`(a, b)` (Python/Rust/Go pares), arreglo (JS), record (Java)."), ("Semántica", "Rust/Python tienen tuplas nativas; Java usa records/objetos."), ("Paradigmática", "SQL: una fila con varias columnas es una tupla.")],
    "familia": "En Ruby `[a, b]` funciona como tupla. En Haskell `(a, b)` es una tupla nativa con `fst`/`snd`.",
    "errores": [("Confundir tupla con lista", "esperar que crezca", "la tupla tiene tamaño fijo"), ("Acceder a un índice inexistente", "error de posición", "respetar el número de componentes")],
    "faq": [("¿Tupla o clase?", "Tupla para agrupaciones pequeñas y anónimas; clase cuando los campos merecen nombre."), ("¿Las tuplas son inmutables?", "En muchos lenguajes sí (Python, Rust): no se cambian tras crearlas.")],
    "reto": "Añade un tercer componente y rótalos (a,b,c)→(c,a,b); resuélvelo en **Rust**.",
    "impls": {
        "python": r"""import sys

a, b = map(int, sys.stdin.readline().split())
t = (a, b)
t = (t[1], t[0])
print(f"tupla=({t[0]}, {t[1]})")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const t = [b, a];
console.log(`tupla=(${t[0]}, ${t[1]})`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const t: [number, number] = [b, a];
console.log(`tupla=(${t[0]}, ${t[1]})`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    record Par(int a, int b) {}

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        Par t = new Par(Integer.parseInt(p[0]), Integer.parseInt(p[1]));
        Par s = new Par(t.b(), t.a());
        System.out.println("tupla=(" + s.a() + ", " + s.b() + ")");
    }
}
""",
        "csharp": r"""using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
(int a, int b) t = (int.Parse(p[0]), int.Parse(p[1]));
t = (t.b, t.a);
Console.WriteLine($"tupla=({t.a}, {t.b})");
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
	a, b = b, a
	fmt.Printf("tupla=(%d, %d)\n", a, b)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let t: (i64, i64) = (v[0], v[1]);
    let t = (t.1, t.0);
    println!("tupla=({}, {})", t.0, t.1);
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    /* C no tiene tuplas: se usa una struct. */
    struct Par { long a, b; } t = { b, a };
    printf("tupla=(%ld, %ld)\n", t.a, t.b);
    return 0;
}
""",
        "php": r"""<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$t = [(int) $b, (int) $a];
echo "tupla=({$t[0]}, {$t[1]})\n";
""",
        "sql": r"""-- SQL: una fila con varias columnas es una tupla.
WITH pares(a, b) AS (VALUES (3, 4), (0, -2), (5, 5))
SELECT printf('tupla=(%d, %d)', b, a) AS resultado FROM pares;
""",
    },
}

S[92] = {
    "descripcion": "Generar el rango de enteros de a hasta b (inclusive) y su suma.",
    "objetivo": "Usar **rangos y secuencias**: describir una serie de valores consecutivos sin listarlos. Los rangos alimentan bucles y comprensiones de forma expresiva.",
    "resultados": ["Generar un rango inclusivo.", "Sumar los valores del rango.", "Reconocer rangos inclusivos vs. exclusivos."],
    "temas": [("Rango", "Serie de valores consecutivos"), ("Inclusivo/exclusivo", "Si incluye el extremo"), ("Secuencia perezosa", "No se materializa entera")],
    "definiciones": [("Rango", "intervalo de valores consecutivos (`2..5`). Clave: describe sin enumerar."), ("Inclusivo", "incluye el extremo final. Clave: `1..=n` en Rust, `range` en Python es exclusivo."), ("Secuencia", "serie ordenada de valores. Clave: puede ser perezosa.")],
    "situacion": "`for i in 1..=100` recorre cien valores sin crear una lista de cien. Los rangos son la forma idiomática de iterar por posiciones.",
    "entrada": "una línea `a b` (enteros, a <= b)",
    "salida": "`rango=<a-...-b> suma=<suma del rango>`",
    "formula": "rango [a..b] y su suma",
    "algoritmo": "LEER a, b ; generar a..b ; sumar",
    "casos": [("2 5", "rango=2-3-4-5 suma=14"), ("1 1", "rango=1 suma=1"), ("3 6", "rango=3-4-5-6 suma=18")],
    "comparacion": [("Sintáctica", "`range(a, b+1)` (Python), `a..=b` (Rust), bucle (C/Java/Go)."), ("Semántica", "Python `range` es exclusivo del final; Rust distingue `..` y `..=`."), ("Paradigmática", "SQL genera rangos con CTE recursivo.")],
    "familia": "En Ruby `(a..b)` es inclusivo, `(a...b)` exclusivo. En Kotlin `a..b` es inclusivo.",
    "errores": [("Error por el extremo (off-by-one)", "incluir o excluir de más", "tener claro si el rango incluye el final"), ("Materializar rangos enormes", "gasto de memoria", "iterar perezosamente cuando se pueda")],
    "faq": [("¿Rango inclusivo o exclusivo?", "Depende del lenguaje; conócelo para no equivocar el extremo."), ("¿Rango consume memoria?", "En Python/Rust es perezoso; no crea la lista completa.")],
    "reto": "Genera solo los pares del rango y resuélvelo en **Rust** con `(a..=b).step_by(2)`.",
    "impls": {
        "python": r"""import sys

a, b = map(int, sys.stdin.readline().split())
r = list(range(a, b + 1))
print(f"rango={'-'.join(str(x) for x in r)} suma={sum(r)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const r = [];
for (let i = a; i <= b; i++) r.push(i);
console.log(`rango=${r.join("-")} suma=${r.reduce((x, y) => x + y, 0)}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const r: number[] = [];
for (let i = a; i <= b; i++) r.push(i);
console.log(`rango=${r.join("-")} suma=${r.reduce((x, y) => x + y, 0)}`);
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
        StringBuilder sb = new StringBuilder();
        long suma = 0;
        for (int i = a; i <= b; i++) {
            if (i > a) sb.append("-");
            sb.append(i);
            suma += i;
        }
        System.out.println("rango=" + sb + " suma=" + suma);
    }
}
""",
        "csharp": r"""using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
var r = Enumerable.Range(a, b - a + 1).ToList();
Console.WriteLine($"rango={string.Join("-", r)} suma={r.Sum()}");
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
	var parts []string
	suma := 0
	for i := a; i <= b; i++ {
		parts = append(parts, strconv.Itoa(i))
		suma += i
	}
	fmt.Printf("rango=%s suma=%d\n", strings.Join(parts, "-"), suma)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let r: Vec<i64> = (v[0]..=v[1]).collect();
    let suma: i64 = r.iter().sum();
    let texto: Vec<String> = r.iter().map(|x| x.to_string()).collect();
    println!("rango={} suma={}", texto.join("-"), suma);
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    long suma = 0;
    printf("rango=");
    for (long i = a; i <= b; i++) {
        if (i > a) printf("-");
        printf("%ld", i);
        suma += i;
    }
    printf(" suma=%ld\n", suma);
    return 0;
}
""",
        "php": r"""<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$r = range((int) $a, (int) $b);
echo "rango=" . implode("-", $r) . " suma=" . array_sum($r) . "\n";
""",
        "sql": r"""-- SQL: rango con CTE recursivo (ilustrativo, 2..5).
WITH RECURSIVE r(i) AS (VALUES (2) UNION ALL SELECT i + 1 FROM r WHERE i < 5)
SELECT 'rango=' || group_concat(i, '-') || printf(' suma=%d', sum(i)) AS resultado FROM r;
""",
    },
}

S[93] = {
    "descripcion": "Invertir una cadena de texto.",
    "objetivo": "Tratar una **cadena como estructura de datos**: una secuencia de caracteres que se puede recorrer, indexar e invertir. Verás que la inmutabilidad obliga a construir una nueva cadena.",
    "resultados": ["Recorrer una cadena carácter a carácter.", "Construir una cadena invertida.", "Reconocer la inmutabilidad de las cadenas."],
    "temas": [("Cadena como secuencia", "Caracteres indexados"), ("Inversión", "Del último al primero"), ("Inmutabilidad", "Se crea una nueva cadena")],
    "definiciones": [("Cadena", "secuencia de caracteres. Clave: se recorre como una colección."), ("Inmutable", "no se modifica en sitio (Java/Python/C#). Clave: invertir crea otra."), ("Índice de carácter", "posición dentro de la cadena. Clave: base 0.")],
    "situacion": "Invertir texto, comprobar palíndromos, procesar entradas: tratar la cadena como una secuencia de caracteres es constante en programación.",
    "entrada": "una palabra (ASCII, sin espacios)",
    "salida": "`invertido=<la palabra al revés>`",
    "formula": "invertir la secuencia de caracteres",
    "algoritmo": "LEER w ; recorrer del final al inicio ; ESCRIBIR invertido",
    "casos": [("hola", "invertido=aloh"), ("Ada", "invertido=adA"), ("abc", "invertido=cba")],
    "comparacion": [("Sintáctica", "`w[::-1]` (Python), `.reverse()` sobre arreglo de chars (JS/Rust)."), ("Semántica", "En Rust hay que iterar por `chars()` (UTF-8); en C es por bytes."), ("Paradigmática", "SQL tiene la función `reverse` en algunos motores; sqlite no de serie.")],
    "familia": "En Ruby `w.reverse`. En C se intercambian los caracteres por índices, sin función incorporada.",
    "errores": [("Invertir por bytes con Unicode", "romper caracteres multibyte", "iterar por caracteres (aquí ASCII, sin problema)"), ("Intentar mutar la cadena", "es inmutable en varios lenguajes", "construir una nueva")],
    "faq": [("¿Por qué invertir crea otra cadena?", "Porque en muchos lenguajes las cadenas son inmutables."), ("¿ASCII o Unicode?", "Aquí ASCII; con Unicode hay que respetar los límites de carácter.")],
    "reto": "Comprueba si la palabra es un palíndromo y resuélvelo en **Python**.",
    "impls": {
        "python": r"""import sys

w = sys.stdin.readline().strip()
print(f"invertido={w[::-1]}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const w = readFileSync(0, "utf8").trim();
console.log(`invertido=${[...w].reverse().join("")}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const w: string = readFileSync(0, "utf8").trim();
console.log(`invertido=${[...w].reverse().join("")}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String w = br.readLine().trim();
        System.out.println("invertido=" + new StringBuilder(w).reverse());
    }
}
""",
        "csharp": r"""using System;
using System.Linq;

string w = Console.In.ReadToEnd().Trim();
Console.WriteLine($"invertido={new string(w.Reverse().ToArray())}");
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
	r := []rune(w)
	for i, j := 0, len(r)-1; i < j; i, j = i+1, j-1 {
		r[i], r[j] = r[j], r[i]
	}
	fmt.Printf("invertido=%s\n", string(r))
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let w = s.trim();
    let inv: String = w.chars().rev().collect();
    println!("invertido={inv}");
}
""",
        "c": r"""#include <stdio.h>
#include <string.h>

int main(void) {
    char w[256];
    if (scanf("%255s", w) != 1) return 1;
    int n = (int) strlen(w);
    printf("invertido=");
    for (int i = n - 1; i >= 0; i--) putchar(w[i]);
    printf("\n");
    return 0;
}
""",
        "php": r"""<?php
$w = trim(fgets(STDIN));
echo "invertido=" . strrev($w) . "\n";
""",
        "sql": r"""-- SQL: sqlite no trae reverse; se invierte con un CTE recursivo (ilustrativo).
WITH RECURSIVE r(i, acc, s) AS (
    SELECT length('hola'), '', 'hola'
    UNION ALL SELECT i - 1, acc || substr(s, i, 1), s FROM r WHERE i > 0
)
SELECT 'invertido=' || acc AS resultado FROM r WHERE i = 0;
""",
    },
}

S[94] = {
    "descripcion": "Contar cuántos valores distintos hay en una lista de enteros.",
    "objetivo": "Usar un **conjunto (set)**: una colección sin duplicados. Contar los valores únicos es la operación natural del conjunto.",
    "resultados": ["Eliminar duplicados con un conjunto.", "Contar elementos distintos.", "Reconocer que el conjunto no tiene orden garantizado."],
    "temas": [("Conjunto", "Colección sin duplicados"), ("Unicidad", "Cada valor una vez"), ("Pertenencia", "Comprobar si algo está")],
    "definiciones": [("Conjunto", "colección de elementos únicos (set, HashSet). Clave: sin duplicados."), ("Unicidad", "propiedad de no repetir. Clave: añadir un existente no hace nada."), ("Pertenencia", "comprobar si un elemento está, en O(1) típico. Clave: uso habitual del set.")],
    "situacion": "¿Cuántos usuarios distintos entraron? ¿Cuántas etiquetas únicas hay? El conjunto elimina duplicados y responde al instante.",
    "entrada": "una línea con enteros separados por espacio",
    "salida": "`unicos=<cantidad de valores distintos>`",
    "formula": "unicos = |conjunto(lista)|",
    "algoritmo": "LEER lista ; conjunto <- SET(lista) ; ESCRIBIR |conjunto|",
    "casos": [("1 2 2 3 3 3", "unicos=3"), ("5 5 5", "unicos=1"), ("1 2 3 4", "unicos=4")],
    "comparacion": [("Sintáctica", "`set(x)` (Python), `new Set` (JS), `HashSet` (Java/Rust/C#)."), ("Semántica", "El conjunto no garantiza orden; C lo simula con un bucle."), ("Paradigmática", "SQL usa `COUNT(DISTINCT x)`.")],
    "familia": "En Ruby `lista.uniq.size`. En Go, un `map[int]struct{}` hace de conjunto.",
    "errores": [("Asumir orden en un conjunto", "esperar los elementos ordenados", "usar una lista/ordenar si necesitas orden"), ("Contar con bucles O(n²) sin necesidad", "lento en listas grandes", "usar un conjunto con pertenencia O(1)")],
    "faq": [("¿El conjunto conserva el orden?", "En general no; algunos lenguajes tienen variantes ordenadas."), ("¿Conjunto o lista?", "Conjunto si te importa la unicidad y la pertenencia rápida.")],
    "reto": "Muestra además los elementos únicos ordenados y resuélvelo en **Python**.",
    "impls": {
        "python": r"""import sys

nums = [int(x) for x in sys.stdin.read().split()]
print(f"unicos={len(set(nums))}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`unicos=${new Set(nums).size}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`unicos=${new Set(nums).size}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashSet;
import java.util.Set;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        Set<Integer> s = new HashSet<>();
        for (String x : p) s.add(Integer.parseInt(x));
        System.out.println("unicos=" + s.size());
    }
}
""",
        "csharp": r"""using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"unicos={p.Select(int.Parse).Distinct().Count()}");
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
	set := make(map[int]struct{})
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		set[n] = struct{}{}
	}
	fmt.Printf("unicos=%d\n", len(set))
}
""",
        "rust": r"""use std::collections::HashSet;
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let set: HashSet<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("unicos={}", set.len());
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    int unicos = 0;
    for (int i = 0; i < n; i++) {
        int repetido = 0;
        for (int j = 0; j < i; j++) {
            if (v[j] == v[i]) { repetido = 1; break; }
        }
        if (!repetido) unicos++;
    }
    printf("unicos=%d\n", unicos);
    return 0;
}
""",
        "php": r"""<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
echo "unicos=" . count(array_unique($nums)) . "\n";
""",
        "sql": r"""-- SQL: COUNT(DISTINCT x).
WITH nums(x) AS (VALUES (1), (2), (2), (3), (3), (3))
SELECT printf('unicos=%d', count(DISTINCT x)) AS resultado FROM nums;
""",
    },
}

S[95] = {
    "descripcion": "Contar cuántas veces aparece el primer elemento de la lista dentro de toda la lista.",
    "objetivo": "Usar un **mapa (diccionario)**: asociar claves con valores. Contar frecuencias es el uso más común: la clave es el número y el valor, cuántas veces aparece.",
    "resultados": ["Construir un mapa de frecuencias.", "Consultar el valor de una clave.", "Reconocer el acceso por clave en O(1)."],
    "temas": [("Mapa/diccionario", "Clave → valor"), ("Frecuencias", "Contar apariciones"), ("Acceso por clave", "Búsqueda rápida")],
    "definiciones": [("Mapa", "colección de pares clave→valor (dict, HashMap). Clave: búsqueda por clave en O(1)."), ("Clave", "identificador único de una entrada. Clave: no se repite."), ("Frecuencia", "cuántas veces aparece un valor. Clave: uso típico del mapa.")],
    "situacion": "Contar palabras, votos, visitas por página: el mapa asocia cada cosa con su cuenta y la actualiza al instante.",
    "entrada": "una línea con enteros separados por espacio",
    "salida": "`cuenta=<veces que aparece el primer elemento>`",
    "formula": "cuenta = frecuencia[lista[0]]",
    "algoritmo": "LEER lista ; construir mapa de frecuencias ; ESCRIBIR frecuencia del primero",
    "casos": [("3 1 3 3", "cuenta=3"), ("5 5", "cuenta=2"), ("7 1 2", "cuenta=1")],
    "comparacion": [("Sintáctica", "`dict` (Python), `{}`/Map (JS), `HashMap` (Java/Rust), `Dictionary` (C#)."), ("Semántica", "El mapa no garantiza orden de claves; C lo simula con arreglos."), ("Paradigmática", "SQL agrupa con GROUP BY.")],
    "familia": "En Ruby `Hash.new(0)` para contar. En Go `map[int]int` es idiomático.",
    "errores": [("Leer una clave inexistente sin defecto", "error o valor nulo", "inicializar con 0 o comprobar la existencia"), ("Asumir orden de inserción", "no siempre garantizado", "usar mapas ordenados si lo necesitas")],
    "faq": [("¿Mapa o lista de pares?", "Mapa para búsqueda rápida por clave; lista de pares si el orden importa."), ("¿Las claves pueden ser cualquier cosa?", "Suelen requerir ser hashables/comparables; números y cadenas siempre valen.")],
    "reto": "Devuelve el elemento más frecuente (la moda) y resuélvelo en **Go**.",
    "impls": {
        "python": r"""import sys

nums = [int(x) for x in sys.stdin.read().split()]
freq = {}
for x in nums:
    freq[x] = freq.get(x, 0) + 1
print(f"cuenta={freq[nums[0]]}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const freq = new Map();
for (const x of nums) freq.set(x, (freq.get(x) || 0) + 1);
console.log(`cuenta=${freq.get(nums[0])}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const freq = new Map<number, number>();
for (const x of nums) freq.set(x, (freq.get(x) || 0) + 1);
console.log(`cuenta=${freq.get(nums[0])}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        Map<Integer, Integer> freq = new HashMap<>();
        for (String s : p) {
            int x = Integer.parseInt(s);
            freq.merge(x, 1, Integer::sum);
        }
        System.out.println("cuenta=" + freq.get(Integer.parseInt(p[0])));
    }
}
""",
        "csharp": r"""using System;
using System.Collections.Generic;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var freq = new Dictionary<int, int>();
foreach (string s in p) {
    int x = int.Parse(s);
    freq[x] = freq.GetValueOrDefault(x, 0) + 1;
}
Console.WriteLine($"cuenta={freq[int.Parse(p[0])]}");
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
	fields := strings.Fields(line)
	freq := make(map[int]int)
	var nums []int
	for _, s := range fields {
		n, _ := strconv.Atoi(s)
		nums = append(nums, n)
		freq[n]++
	}
	fmt.Printf("cuenta=%d\n", freq[nums[0]])
}
""",
        "rust": r"""use std::collections::HashMap;
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let mut freq: HashMap<i64, i64> = HashMap::new();
    for &x in &nums {
        *freq.entry(x).or_insert(0) += 1;
    }
    println!("cuenta={}", freq[&nums[0]]);
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    int cuenta = 0;
    for (int i = 0; i < n; i++) {
        if (v[i] == v[0]) cuenta++;
    }
    printf("cuenta=%d\n", cuenta);
    return 0;
}
""",
        "php": r"""<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$freq = array_count_values($nums);
echo "cuenta=" . $freq[$nums[0]] . "\n";
""",
        "sql": r"""-- SQL: GROUP BY para frecuencias.
WITH nums(x) AS (VALUES (3), (1), (3), (3))
SELECT printf('cuenta=%d', count(*)) AS resultado
FROM nums WHERE x = (SELECT x FROM nums LIMIT 1);
""",
    },
}

S[96] = {
    "descripcion": "Procesar una lista como pila (LIFO) y como cola (FIFO), mostrando el orden de salida de cada una.",
    "objetivo": "Distinguir **pila (LIFO)** de **cola (FIFO)**: dos formas de ordenar la salida. La pila devuelve el último que entró; la cola, el primero.",
    "resultados": ["Simular una pila y una cola.", "Explicar LIFO frente a FIFO.", "Reconocer sus usos típicos."],
    "temas": [("Pila (LIFO)", "Último en entrar, primero en salir"), ("Cola (FIFO)", "Primero en entrar, primero en salir"), ("push/pop, enqueue/dequeue", "Sus operaciones")],
    "definiciones": [("Pila", "estructura LIFO: se saca el último añadido. Clave: deshacer, llamadas."), ("Cola", "estructura FIFO: se saca el primero añadido. Clave: turnos, tareas."), ("LIFO/FIFO", "orden de salida. Clave: define la estructura.")],
    "situacion": "La pila modela el 'deshacer' y la pila de llamadas; la cola modela una fila de impresión o de tareas. La misma entrada sale en orden opuesto según la estructura.",
    "entrada": "una línea con enteros separados por espacio",
    "salida": "`pila=<orden LIFO> cola=<orden FIFO>`",
    "formula": "pila = inverso(lista); cola = lista",
    "algoritmo": "LEER lista ; pila <- sacar en LIFO ; cola <- sacar en FIFO",
    "casos": [("1 2 3", "pila=3-2-1 cola=1-2-3"), ("5", "pila=5 cola=5"), ("1 2 3 4", "pila=4-3-2-1 cola=1-2-3-4")],
    "comparacion": [("Sintáctica", "`append`/`pop` (Python), `push`/`shift` (JS), `Deque` (Java)."), ("Semántica", "La pila saca por el final; la cola por el frente."), ("Paradigmática", "SQL ordena por la posición ascendente o descendente.")],
    "familia": "En Go una pila/cola se hace con un slice. En C++ `std::stack` y `std::queue`.",
    "errores": [("Confundir el extremo de salida", "pila y cola invertidas", "pila saca por el final; cola por el frente"), ("Usar shift/remove(0) en listas grandes", "coste O(n)", "usar una estructura de cola eficiente (deque)")],
    "faq": [("¿Pila o cola?", "Pila para LIFO (deshacer, recursión); cola para FIFO (turnos, tareas)."), ("¿La recursión usa pila?", "Sí: la pila de llamadas es una pila real del programa.")],
    "reto": "Añade una cola de prioridad (saca el menor primero) y resuélvelo en **Python** con `heapq`.",
    "impls": {
        "python": r"""import sys

nums = [int(x) for x in sys.stdin.read().split()]
pila = "-".join(str(x) for x in reversed(nums))
cola = "-".join(str(x) for x in nums)
print(f"pila={pila} cola={cola}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const pila = [...nums].reverse().join("-");
const cola = nums.join("-");
console.log(`pila=${pila} cola=${cola}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const pila = [...nums].reverse().join("-");
const cola = nums.join("-");
console.log(`pila=${pila} cola=${cola}`);
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
        String[] p = br.readLine().trim().split("\\s+");
        List<String> l = new ArrayList<>();
        for (String s : p) l.add(s);
        List<String> rev = new ArrayList<>(l);
        java.util.Collections.reverse(rev);
        System.out.println("pila=" + String.join("-", rev) + " cola=" + String.join("-", l));
    }
}
""",
        "csharp": r"""using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
string pila = string.Join("-", p.Reverse());
string cola = string.Join("-", p);
Console.WriteLine($"pila={pila} cola={cola}");
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
	rev := make([]string, len(f))
	for i, x := range f {
		rev[len(f)-1-i] = x
	}
	fmt.Printf("pila=%s cola=%s\n", strings.Join(rev, "-"), strings.Join(f, "-"))
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<&str> = s.split_whitespace().collect();
    let mut rev = nums.clone();
    rev.reverse();
    println!("pila={} cola={}", rev.join("-"), nums.join("-"));
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    printf("pila=");
    for (int i = n - 1; i >= 0; i--) {
        if (i < n - 1) printf("-");
        printf("%ld", v[i]);
    }
    printf(" cola=");
    for (int i = 0; i < n; i++) {
        if (i > 0) printf("-");
        printf("%ld", v[i]);
    }
    printf("\n");
    return 0;
}
""",
        "php": r"""<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$pila = implode("-", array_reverse($nums));
$cola = implode("-", $nums);
echo "pila=$pila cola=$cola\n";
""",
        "sql": r"""-- SQL: orden descendente (pila) y ascendente (cola) por posición.
WITH nums(pos, x) AS (VALUES (1, 1), (2, 2), (3, 3))
SELECT 'pila=' || (SELECT group_concat(x, '-') FROM (SELECT x FROM nums ORDER BY pos DESC))
     || ' cola=' || (SELECT group_concat(x, '-') FROM (SELECT x FROM nums ORDER BY pos ASC)) AS resultado;
""",
    },
}

S[97] = {
    "descripcion": "Insertar enteros en un árbol binario de búsqueda y recorrerlo en orden (in-order), que produce la secuencia ordenada.",
    "objetivo": "Conocer los **árboles**: estructuras jerárquicas. En un árbol binario de búsqueda (BST), el recorrido in-order devuelve los elementos ordenados. Aquí el efecto observable es la ordenación.",
    "resultados": ["Entender la propiedad del BST.", "Reconocer el recorrido in-order.", "Relacionar el árbol con el orden."],
    "temas": [("Árbol", "Nodos con hijos, jerárquico"), ("BST", "Menores a la izquierda, mayores a la derecha"), ("Recorrido in-order", "Produce el orden ascendente")],
    "definiciones": [("Árbol", "estructura jerárquica de nodos con hijos. Clave: sin ciclos, una raíz."), ("BST", "árbol binario ordenado: izquierda < nodo < derecha. Clave: búsqueda O(log n) equilibrado."), ("In-order", "recorrido izquierda-raíz-derecha. Clave: en un BST da los valores ordenados.")],
    "situacion": "Índices de bases de datos, sistemas de archivos, autocompletado: los árboles organizan datos jerárquicos y permiten búsquedas rápidas. En un BST, recorrer in-order ordena.",
    "entrada": "una línea con enteros distintos separados por espacio",
    "salida": "`inorden=<los valores ordenados ascendente unidos por ->`",
    "formula": "in-order de un BST = orden ascendente",
    "algoritmo": "LEER lista ; insertar en BST ; recorrer in-order",
    "casos": [("3 1 4", "inorden=1-3-4"), ("5 2 8 1", "inorden=1-2-5-8"), ("9 7", "inorden=7-9")],
    "comparacion": [("Sintáctica", "Ordenar (`sorted`) equivale al in-order del BST en esta clase."), ("Semántica", "El BST mantiene el orden al insertar; ordenar lo hace de una vez."), ("Paradigmática", "SQL usa ORDER BY, que el motor implementa con árboles/índices.")],
    "familia": "En muchos lenguajes se usa un TreeSet/TreeMap (árbol equilibrado) que ya mantiene el orden.",
    "errores": [("Confundir in-order con otros recorridos", "pre/post-order no ordenan", "usar in-order para obtener el orden"), ("Insertar duplicados sin política", "árbol ambiguo", "aquí los valores son distintos")],
    "faq": [("¿Por qué in-order ordena?", "Porque visita izquierda (menores), raíz, derecha (mayores) recursivamente."), ("¿BST o array ordenado?", "El BST permite inserciones/borrados eficientes manteniendo el orden.")],
    "reto": "Implementa un BST real con nodos y recorrido recursivo, y resuélvelo en **Rust**.",
    "impls": {
        "python": r"""import sys

nums = [int(x) for x in sys.stdin.read().split()]
nums.sort()  # in-order de un BST equivale al orden ascendente
print("inorden=" + "-".join(str(x) for x in nums))
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
nums.sort((a, b) => a - b);
console.log(`inorden=${nums.join("-")}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
nums.sort((a, b) => a - b);
console.log(`inorden=${nums.join("-")}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.TreeSet;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        TreeSet<Integer> t = new TreeSet<>();
        for (String s : p) t.add(Integer.parseInt(s));
        System.out.println("inorden=" + t.stream().map(String::valueOf).collect(Collectors.joining("-")));
    }
}
""",
        "csharp": r"""using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var nums = p.Select(int.Parse).OrderBy(x => x);
Console.WriteLine($"inorden={string.Join("-", nums)}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	var nums []int
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		nums = append(nums, n)
	}
	sort.Ints(nums)
	parts := make([]string, len(nums))
	for i, n := range nums {
		parts[i] = strconv.Itoa(n)
	}
	fmt.Printf("inorden=%s\n", strings.Join(parts, "-"))
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    nums.sort();
    let texto: Vec<String> = nums.iter().map(|x| x.to_string()).collect();
    println!("inorden={}", texto.join("-"));
}
""",
        "c": r"""#include <stdio.h>
#include <stdlib.h>

int cmp(const void *a, const void *b) {
    long x = *(const long *) a, y = *(const long *) b;
    return (x > y) - (x < y);
}

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    qsort(v, n, sizeof(long), cmp);
    printf("inorden=");
    for (int i = 0; i < n; i++) {
        if (i > 0) printf("-");
        printf("%ld", v[i]);
    }
    printf("\n");
    return 0;
}
""",
        "php": r"""<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
sort($nums);
echo "inorden=" . implode("-", $nums) . "\n";
""",
        "sql": r"""-- SQL: ORDER BY equivale al in-order del BST.
WITH nums(x) AS (VALUES (3), (1), (4))
SELECT 'inorden=' || group_concat(x, '-') AS resultado
FROM (SELECT x FROM nums ORDER BY x);
""",
    },
}

S[98] = {
    "descripcion": "Dado un grafo como lista de aristas (pares de nodos), contar las aristas y los nodos distintos.",
    "objetivo": "Conocer los **grafos**: nodos conectados por aristas. Representarlos como lista de aristas y contar nodos y aristas es el primer paso para modelar redes, mapas y dependencias.",
    "resultados": ["Representar un grafo por sus aristas.", "Contar aristas y nodos distintos.", "Reconocer dónde aparecen los grafos."],
    "temas": [("Grafo", "Nodos y aristas"), ("Arista", "Conexión entre dos nodos"), ("Nodos distintos", "El conjunto de vértices")],
    "definiciones": [("Grafo", "conjunto de nodos conectados por aristas. Clave: modela relaciones."), ("Arista", "conexión entre dos nodos. Clave: aquí, un par de números."), ("Nodo (vértice)", "una entidad del grafo. Clave: contar los distintos = tamaño del conjunto.")],
    "situacion": "Redes sociales, mapas de carreteras, dependencias de paquetes: todo son grafos. Contar nodos y aristas es la medida básica de su tamaño.",
    "entrada": "una línea con pares de enteros (cada par es una arista)",
    "salida": "`aristas=<número de pares> nodos=<nodos distintos>`",
    "formula": "aristas = tokens/2 ; nodos = |conjunto de todos los números|",
    "algoritmo": "LEER pares ; aristas <- pares ; nodos <- distintos",
    "casos": [("1 2 2 3", "aristas=2 nodos=3"), ("1 2", "aristas=1 nodos=2"), ("1 2 2 3 3 1", "aristas=3 nodos=3")],
    "comparacion": [("Sintáctica", "Conjunto de nodos + conteo de pares en cada lenguaje."), ("Semántica", "El grafo puede guardarse como lista de aristas o de adyacencia."), ("Paradigmática", "SQL modela grafos con tablas de nodos y aristas (relaciones).")],
    "familia": "En muchos lenguajes se usa un mapa de adyacencia `nodo → vecinos`. Aquí basta un conjunto para los nodos.",
    "errores": [("Contar nodos con repetición", "sobreestimar los vértices", "usar un conjunto de nodos distintos"), ("Suponer número impar de tokens", "arista incompleta", "asumir pares completos (grafo bien formado)")],
    "faq": [("¿Lista de aristas o adyacencia?", "Aristas es simple para contar; adyacencia es mejor para recorrer vecinos."), ("¿Dirigido o no?", "Aquí solo contamos; la dirección importaría para recorridos.")],
    "reto": "Calcula el grado de cada nodo (número de aristas que lo tocan) y resuélvelo en **Python**.",
    "impls": {
        "python": r"""import sys

nums = [int(x) for x in sys.stdin.read().split()]
aristas = len(nums) // 2
nodos = len(set(nums))
print(f"aristas={aristas} nodos={nodos}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const aristas = Math.floor(nums.length / 2);
const nodos = new Set(nums).size;
console.log(`aristas=${aristas} nodos=${nodos}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const aristas = Math.floor(nums.length / 2);
const nodos = new Set(nums).size;
console.log(`aristas=${aristas} nodos=${nodos}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashSet;
import java.util.Set;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        Set<Integer> nodos = new HashSet<>();
        for (String s : p) nodos.add(Integer.parseInt(s));
        System.out.println("aristas=" + (p.length / 2) + " nodos=" + nodos.size());
    }
}
""",
        "csharp": r"""using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int aristas = p.Length / 2;
int nodos = p.Select(int.Parse).Distinct().Count();
Console.WriteLine($"aristas={aristas} nodos={nodos}");
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
	set := make(map[int]struct{})
	for _, s := range f {
		n, _ := strconv.Atoi(s)
		set[n] = struct{}{}
	}
	fmt.Printf("aristas=%d nodos=%d\n", len(f)/2, len(set))
}
""",
        "rust": r"""use std::collections::HashSet;
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let aristas = nums.len() / 2;
    let nodos: HashSet<i64> = nums.iter().copied().collect();
    println!("aristas={} nodos={}", aristas, nodos.len());
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long v[2048];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    int nodos = 0;
    for (int i = 0; i < n; i++) {
        int repetido = 0;
        for (int j = 0; j < i; j++) {
            if (v[j] == v[i]) { repetido = 1; break; }
        }
        if (!repetido) nodos++;
    }
    printf("aristas=%d nodos=%d\n", n / 2, nodos);
    return 0;
}
""",
        "php": r"""<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$aristas = intdiv(count($nums), 2);
$nodos = count(array_unique($nums));
echo "aristas=$aristas nodos=$nodos\n";
""",
        "sql": r"""-- SQL: aristas = filas de pares; nodos = valores distintos.
WITH nums(x) AS (VALUES (1), (2), (2), (3))
SELECT printf('aristas=%d nodos=%d', count(*) / 2, count(DISTINCT x)) AS resultado FROM nums;
""",
    },
}

S[99] = {
    "descripcion": "Crear un registro Persona con nombre y edad, y mostrarlo formateado.",
    "objetivo": "Agrupar datos relacionados en un **registro/struct/clase** con campos nombrados. En vez de variables sueltas, un tipo compuesto con significado.",
    "resultados": ["Definir un tipo con campos nombrados.", "Crear una instancia y acceder a sus campos.", "Distinguir struct de clase donde aplique."],
    "temas": [("Registro/struct", "Campos nombrados juntos"), ("Instancia", "Un valor del tipo"), ("Acceso a campos", "`.nombre`, `.edad`")],
    "definiciones": [("Registro/struct", "tipo con campos nombrados. Clave: agrupa datos relacionados."), ("Campo", "cada dato con nombre dentro del registro. Clave: `persona.edad`."), ("Instancia", "un valor concreto del tipo. Clave: `Persona(\"Ada\", 36)`.")],
    "situacion": "En vez de pasar `nombre` y `edad` sueltos por todas partes, un `Persona` los agrupa con significado y viaja como una sola cosa.",
    "entrada": "una línea `nombre edad` (una palabra y un entero)",
    "salida": "`Persona(nombre=<nombre>, edad=<edad>)`",
    "formula": "registro con campos nombre y edad",
    "algoritmo": "LEER nombre, edad ; crear Persona ; ESCRIBIR formateado",
    "casos": [("Ada 36", "Persona(nombre=Ada, edad=36)"), ("Bo 5", "Persona(nombre=Bo, edad=5)"), ("Cy 99", "Persona(nombre=Cy, edad=99)")],
    "comparacion": [("Sintáctica", "`class`/`@dataclass` (Python), `record` (Java), `struct` (Go/Rust/C), objeto (JS)."), ("Semántica", "Struct suele ser por valor; clase por referencia (Java/C#)."), ("Paradigmática", "SQL: una fila de una tabla es un registro.")],
    "familia": "En Kotlin `data class Persona(val nombre: String, val edad: Int)`. En C++ `struct Persona`.",
    "errores": [("Usar variables sueltas en vez de agrupar", "datos que se desincronizan", "agruparlos en un registro con significado"), ("Confundir struct (valor) con clase (referencia)", "copias inesperadas", "conocer la semántica del lenguaje")],
    "faq": [("¿Struct o clase?", "Struct para datos por valor; clase para identidad y comportamiento (según el lenguaje)."), ("¿Registro inmutable?", "A menudo conviene: un record de Java o una data class con val.")],
    "reto": "Añade un método `saludo()` que use los campos y resuélvelo en **Rust**.",
    "impls": {
        "python": r"""import sys
from dataclasses import dataclass


@dataclass
class Persona:
    nombre: str
    edad: int


t = sys.stdin.readline().split()
p = Persona(t[0], int(t[1]))
print(f"Persona(nombre={p.nombre}, edad={p.edad})")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const t = readFileSync(0, "utf8").trim().split(/\s+/);
const persona = { nombre: t[0], edad: parseInt(t[1], 10) };
console.log(`Persona(nombre=${persona.nombre}, edad=${persona.edad})`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

interface Persona {
  nombre: string;
  edad: number;
}

const t: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
const p: Persona = { nombre: t[0], edad: parseInt(t[1], 10) };
console.log(`Persona(nombre=${p.nombre}, edad=${p.edad})`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    record Persona(String nombre, int edad) {}

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        Persona p = new Persona(t[0], Integer.parseInt(t[1]));
        System.out.println("Persona(nombre=" + p.nombre() + ", edad=" + p.edad() + ")");
    }
}
""",
        "csharp": r"""using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var p = new Persona(t[0], int.Parse(t[1]));
Console.WriteLine($"Persona(nombre={p.Nombre}, edad={p.Edad})");

record Persona(string Nombre, int Edad);
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Persona struct {
	Nombre string
	Edad   int
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	t := strings.Fields(line)
	edad, _ := strconv.Atoi(t[1])
	p := Persona{Nombre: t[0], Edad: edad}
	fmt.Printf("Persona(nombre=%s, edad=%d)\n", p.Nombre, p.Edad)
}
""",
        "rust": r"""use std::io::Read;

struct Persona {
    nombre: String,
    edad: i64,
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let p = Persona {
        nombre: t[0].to_string(),
        edad: t[1].parse().unwrap(),
    };
    println!("Persona(nombre={}, edad={})", p.nombre, p.edad);
}
""",
        "c": r"""#include <stdio.h>

struct Persona {
    char nombre[64];
    long edad;
};

int main(void) {
    struct Persona p;
    if (scanf("%63s %ld", p.nombre, &p.edad) != 2) return 1;
    printf("Persona(nombre=%s, edad=%ld)\n", p.nombre, p.edad);
    return 0;
}
""",
        "php": r"""<?php
class Persona {
    public function __construct(public string $nombre, public int $edad) {}
}

$t = preg_split('/\s+/', trim(fgets(STDIN)));
$p = new Persona($t[0], (int) $t[1]);
echo "Persona(nombre={$p->nombre}, edad={$p->edad})\n";
""",
        "sql": r"""-- SQL: una fila de una tabla es un registro.
WITH personas(nombre, edad) AS (VALUES ('Ada', 36))
SELECT printf('Persona(nombre=%s, edad=%d)', nombre, edad) AS resultado FROM personas;
""",
    },
}

S[100] = {
    "descripcion": "Calcular el área de una figura descrita por un tipo algebraico: cuadrado(lado) o rectangulo(ancho, alto).",
    "objetivo": "Usar **tipos algebraicos (suma)**: un valor que es una de varias alternativas, cada una con sus datos. `Forma = Cuadrado | Rectangulo`. El `match` decide y calcula según la variante.",
    "resultados": ["Modelar alternativas con un tipo suma.", "Decidir por variante con match/switch.", "Reconocer la exhaustividad del tipo algebraico."],
    "temas": [("Tipo suma (ADT)", "Una de varias alternativas"), ("Variante", "Cada caso con sus datos"), ("Match por variante", "Decidir según la forma")],
    "definiciones": [("Tipo algebraico (suma)", "valor que es una de varias alternativas (Cuadrado o Rectangulo). Clave: modela 'o esto o lo otro'."), ("Variante", "cada alternativa del tipo suma, con sus propios datos. Clave: `Cuadrado(lado)`."), ("Exhaustividad", "cubrir todas las variantes. Clave: Rust lo exige al compilar.")],
    "situacion": "Un pago es efectivo, tarjeta o transferencia; una figura es círculo, cuadrado o rectángulo. Los tipos suma modelan estas alternativas con seguridad, y el match obliga a considerarlas todas.",
    "entrada": "una línea: `cuadrado <lado>` o `rectangulo <ancho> <alto>`",
    "salida": "`area=<área calculada>`",
    "formula": "cuadrado→lado²; rectangulo→ancho·alto",
    "algoritmo": "LEER tipo y datos ; COINCIDIR tipo: cuadrado->l*l ; rectangulo->a*b",
    "casos": [("cuadrado 5", "area=25"), ("rectangulo 3 4", "area=12"), ("cuadrado 7", "area=49")],
    "comparacion": [("Sintáctica", "`enum` con datos (Rust), sealed/record (Java/C#), etiqueta + campos (Go/C)."), ("Semántica", "Rust/Haskell garantizan exhaustividad; C usa una etiqueta manual."), ("Paradigmática", "SQL usa una columna 'tipo' + CASE.")],
    "familia": "En Haskell `data Forma = Cuadrado Int | Rectangulo Int Int`. En Kotlin, una `sealed class`.",
    "errores": [("Olvidar una variante", "caso sin manejar", "en Rust el compilador avisa; en otros, incluir el default"), ("Leer los datos de la variante equivocada", "usar campos que no existen", "extraer solo los datos de la variante correcta")],
    "faq": [("¿Tipo suma o herencia?", "El tipo suma es cerrado y exhaustivo; la herencia es abierta. Distintas garantías."), ("¿Por qué 'algebraico'?", "Combina 'sumas' (alternativas) y 'productos' (campos) de tipos.")],
    "reto": "Añade la variante `triangulo <base> <altura>` (área = base·altura/2) y resuélvelo en **Rust** con `enum`.",
    "impls": {
        "python": r"""import sys

t = sys.stdin.readline().split()
if t[0] == "cuadrado":
    area = int(t[1]) ** 2
else:  # rectangulo
    area = int(t[1]) * int(t[2])
print(f"area={area}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const t = readFileSync(0, "utf8").trim().split(/\s+/);
let area;
if (t[0] === "cuadrado") area = Number(t[1]) ** 2;
else area = Number(t[1]) * Number(t[2]);
console.log(`area=${area}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const t: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
let area: number;
if (t[0] === "cuadrado") area = Number(t[1]) ** 2;
else area = Number(t[1]) * Number(t[2]);
console.log(`area=${area}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        long area;
        if (t[0].equals("cuadrado")) {
            long l = Long.parseLong(t[1]);
            area = l * l;
        } else {
            area = Long.parseLong(t[1]) * Long.parseLong(t[2]);
        }
        System.out.println("area=" + area);
    }
}
""",
        "csharp": r"""using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long area = t[0] switch {
    "cuadrado" => long.Parse(t[1]) * long.Parse(t[1]),
    _ => long.Parse(t[1]) * long.Parse(t[2]),
};
Console.WriteLine($"area={area}");
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
	var area int64
	if t[0] == "cuadrado" {
		l, _ := strconv.ParseInt(t[1], 10, 64)
		area = l * l
	} else {
		a, _ := strconv.ParseInt(t[1], 10, 64)
		b, _ := strconv.ParseInt(t[2], 10, 64)
		area = a * b
	}
	fmt.Printf("area=%d\n", area)
}
""",
        "rust": r"""use std::io::Read;

enum Forma {
    Cuadrado(i64),
    Rectangulo(i64, i64),
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let forma = if t[0] == "cuadrado" {
        Forma::Cuadrado(t[1].parse().unwrap())
    } else {
        Forma::Rectangulo(t[1].parse().unwrap(), t[2].parse().unwrap())
    };
    let area = match forma {
        Forma::Cuadrado(l) => l * l,
        Forma::Rectangulo(a, b) => a * b,
    };
    println!("area={area}");
}
""",
        "c": r"""#include <stdio.h>
#include <string.h>

int main(void) {
    char tipo[32];
    if (scanf("%31s", tipo) != 1) return 1;
    long area;
    if (strcmp(tipo, "cuadrado") == 0) {
        long l;
        if (scanf("%ld", &l) != 1) return 1;
        area = l * l;
    } else {
        long a, b;
        if (scanf("%ld %ld", &a, &b) != 2) return 1;
        area = a * b;
    }
    printf("area=%ld\n", area);
    return 0;
}
""",
        "php": r"""<?php
$t = preg_split('/\s+/', trim(fgets(STDIN)));
if ($t[0] === "cuadrado") {
    $area = (int) $t[1] * (int) $t[1];
} else {
    $area = (int) $t[1] * (int) $t[2];
}
echo "area=$area\n";
""",
        "sql": r"""-- SQL: una columna 'tipo' + CASE modela las variantes.
WITH formas(tipo, a, b) AS (VALUES ('cuadrado', 5, 0))
SELECT printf('area=%d', CASE WHEN tipo = 'cuadrado' THEN a * a ELSE a * b END) AS resultado
FROM formas;
""",
    },
}

S[101] = {
    "descripcion": "Comparar dos enteros e indicar si son iguales.",
    "objetivo": "Distinguir **igualdad** (mismo valor) de **identidad** (mismo objeto en memoria). Con valores primitivos coinciden; con objetos no siempre, y cada lenguaje ofrece operadores distintos (`==` vs. `is`/`===`).",
    "resultados": ["Comparar por valor.", "Explicar la diferencia entre igualdad e identidad.", "Reconocer los operadores de cada lenguaje."],
    "temas": [("Igualdad", "Mismo valor"), ("Identidad", "Mismo objeto en memoria"), ("Operadores", "==, is, ===, equals")],
    "definiciones": [("Igualdad", "dos valores son iguales si representan lo mismo. Clave: `a == b`."), ("Identidad", "dos referencias apuntan al mismo objeto. Clave: `is` (Python), `===` no es exactamente eso en JS."), ("equals vs. ==", "en Java `==` compara referencias de objetos; `equals` compara valor. Clave: fuente de bugs.")],
    "situacion": "En Java, dos cadenas con el mismo texto pueden ser `equals` pero no `==` (distintos objetos). Confundir igualdad con identidad es un error clásico.",
    "entrada": "una línea `a b` (dos enteros)",
    "salida": "`iguales=<true|false>`",
    "formula": "iguales = (a == b)",
    "algoritmo": "LEER a, b ; ESCRIBIR iguales=(a==b)",
    "casos": [("5 5", "iguales=true"), ("3 7", "iguales=false"), ("0 0", "iguales=true")],
    "comparacion": [("Sintáctica", "`==` en todos para valor; identidad con `is` (Python), `===` (JS), `equals`/`==` (Java)."), ("Semántica", "Con primitivos, igualdad e identidad coinciden; con objetos no."), ("Paradigmática", "SQL compara valores con `=`; NULL requiere `IS`.")],
    "familia": "En Ruby `==` es valor y `equal?` es identidad. En C#, `==` puede sobrecargarse; `ReferenceEquals` da identidad.",
    "errores": [("Usar `==` para objetos en Java", "compara referencias, no valor", "usar `equals` para comparar contenido"), ("Comparar reales con `==`", "imprecisión", "aquí son enteros; con reales usar tolerancia")],
    "faq": [("¿`==` compara valor o referencia?", "Depende del lenguaje y del tipo; con primitivos, valor."), ("¿Qué es `is` en Python?", "Compara identidad (mismo objeto), no valor.")],
    "reto": "Compara dos cadenas por valor y por identidad y resuélvelo en **Python** con `==` e `is`.",
    "impls": {
        "python": r"""import sys

a, b = map(int, sys.stdin.readline().split())
print(f"iguales={'true' if a == b else 'false'}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`iguales=${a === b ? "true" : "false"}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`iguales=${a === b ? "true" : "false"}`);
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
        System.out.println("iguales=" + (a == b ? "true" : "false"));
    }
}
""",
        "csharp": r"""using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
Console.WriteLine($"iguales={(a == b ? "true" : "false")}");
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
	res := "false"
	if a == b {
		res = "true"
	}
	fmt.Printf("iguales=%s\n", res)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let res = if v[0] == v[1] { "true" } else { "false" };
    println!("iguales={res}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("iguales=%s\n", a == b ? "true" : "false");
    return 0;
}
""",
        "php": r"""<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "iguales=" . ((int) $a === (int) $b ? "true" : "false") . "\n";
""",
        "sql": r"""-- SQL: compara valores con =.
WITH pares(a, b) AS (VALUES (5, 5), (3, 7), (0, 0))
SELECT printf('iguales=%s', CASE WHEN a = b THEN 'true' ELSE 'false' END) AS resultado FROM pares;
""",
    },
}

S[102] = {
    "descripcion": "Copiar una lista, modificar el último elemento de la copia y mostrar que el original no cambia.",
    "objetivo": "Distinguir **copia** de **referencia compartida**, y **copia superficial** de **profunda**. Copiar una lista de valores y modificar la copia no altera el original; con referencias compartidas, sí.",
    "resultados": ["Copiar una colección.", "Comprobar que el original no cambia.", "Distinguir copia superficial de profunda."],
    "temas": [("Copia vs. referencia", "Duplicar o compartir"), ("Copia superficial", "Copia el primer nivel"), ("Copia profunda", "Copia todo recursivamente")],
    "definiciones": [("Copia", "duplicado independiente. Clave: modificarlo no afecta al original."), ("Referencia compartida", "dos nombres para el mismo dato. Clave: cambiar uno cambia el otro."), ("Superficial vs. profunda", "copiar solo el nivel externo o todo el contenido. Clave: importa con datos anidados.")],
    "situacion": "Asignar `b = a` en muchos lenguajes comparte la lista: cambiar `b` cambia `a`. Copiarla de verdad evita esa sorpresa. Con estructuras anidadas, la copia debe ser profunda.",
    "entrada": "una línea con enteros separados por espacio",
    "salida": "`original=<lista> copia=<lista con el último cambiado a 99>` (unidos por -)",
    "formula": "copiar; copia[último] = 99; original intacto",
    "algoritmo": "LEER lista ; copia <- COPIA(lista) ; copia[fin] <- 99 ; ESCRIBIR original y copia",
    "casos": [("1 2 3", "original=1-2-3 copia=1-2-99"), ("5 5", "original=5-5 copia=5-99"), ("7", "original=7 copia=99")],
    "comparacion": [("Sintáctica", "`list(x)`/`x[:]` (Python), `[...x]` (JS), `clone()` (Rust/Java)."), ("Semántica", "Sin copiar, `b=a` comparte; hay que copiar explícitamente."), ("Paradigmática", "SQL trabaja con conjuntos; no comparte referencias mutables.")],
    "familia": "En Ruby `dup` copia superficial; en muchos lenguajes la copia profunda requiere recorrer.",
    "errores": [("Creer que asignar copia", "`b=a` comparte la referencia", "copiar explícitamente si necesitas independencia"), ("Copia superficial con datos anidados", "los niveles internos siguen compartidos", "hacer copia profunda cuando haya anidamiento")],
    "faq": [("¿Copia superficial o profunda?", "Superficial si no hay anidamiento; profunda si hay estructuras dentro de estructuras."), ("¿Los primitivos se comparten?", "No: los valores se copian; las colecciones/objetos se comparten por referencia.")],
    "reto": "Haz una copia profunda de una lista de listas y modifícala; resuélvelo en **Python** con `copy.deepcopy`.",
    "impls": {
        "python": r"""import sys

nums = [int(x) for x in sys.stdin.read().split()]
copia = list(nums)  # copia superficial (aquí basta, son enteros)
copia[-1] = 99
print(f"original={'-'.join(map(str, nums))} copia={'-'.join(map(str, copia))}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const copia = [...nums];
copia[copia.length - 1] = 99;
console.log(`original=${nums.join("-")} copia=${copia.join("-")}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const copia: number[] = [...nums];
copia[copia.length - 1] = 99;
console.log(`original=${nums.join("-")} copia=${copia.join("-")}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int[] nums = new int[p.length];
        for (int i = 0; i < p.length; i++) nums[i] = Integer.parseInt(p[i]);
        int[] copia = Arrays.copyOf(nums, nums.length);
        copia[copia.length - 1] = 99;
        System.out.println("original=" + join(nums) + " copia=" + join(copia));
    }

    static String join(int[] a) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < a.length; i++) {
            if (i > 0) sb.append("-");
            sb.append(a[i]);
        }
        return sb.toString();
    }
}
""",
        "csharp": r"""using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int[] nums = p.Select(int.Parse).ToArray();
int[] copia = (int[]) nums.Clone();
copia[copia.Length - 1] = 99;
Console.WriteLine($"original={string.Join("-", nums)} copia={string.Join("-", copia)}");
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
	nums := make([]int, len(f))
	for i, s := range f {
		nums[i], _ = strconv.Atoi(s)
	}
	copia := make([]int, len(nums))
	copy(copia, nums)
	copia[len(copia)-1] = 99
	fmt.Printf("original=%s copia=%s\n", join(nums), join(copia))
}

func join(a []int) string {
	parts := make([]string, len(a))
	for i, n := range a {
		parts[i] = strconv.Itoa(n)
	}
	return strings.Join(parts, "-")
}
""",
        "rust": r"""use std::io::Read;

fn join(a: &[i64]) -> String {
    a.iter().map(|x| x.to_string()).collect::<Vec<_>>().join("-")
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let mut copia = nums.clone();
    let n = copia.len();
    copia[n - 1] = 99;
    println!("original={} copia={}", join(&nums), join(&copia));
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    long copia[1024];
    for (int i = 0; i < n; i++) copia[i] = v[i];
    copia[n - 1] = 99;
    printf("original=");
    for (int i = 0; i < n; i++) { if (i) printf("-"); printf("%ld", v[i]); }
    printf(" copia=");
    for (int i = 0; i < n; i++) { if (i) printf("-"); printf("%ld", copia[i]); }
    printf("\n");
    return 0;
}
""",
        "php": r"""<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$copia = $nums; // PHP copia los arreglos por valor
$copia[count($copia) - 1] = 99;
echo "original=" . implode("-", $nums) . " copia=" . implode("-", $copia) . "\n";
""",
        "sql": r"""-- SQL: los conjuntos no comparten referencias mutables; se ilustra el cambio.
WITH nums(pos, x) AS (VALUES (1, 1), (2, 2), (3, 3))
SELECT 'original=' || (SELECT group_concat(x, '-') FROM (SELECT x FROM nums ORDER BY pos))
     || ' copia=' || (SELECT group_concat(CASE WHEN pos = (SELECT max(pos) FROM nums) THEN 99 ELSE x END, '-')
                       FROM (SELECT pos, x FROM nums ORDER BY pos)) AS resultado;
""",
    },
}

S[103] = {
    "descripcion": "Crear un recurso con un valor, usarlo y liberarlo automáticamente al salir del ámbito.",
    "objetivo": "Entender la **propiedad y el ciclo de vida** de los datos: cuándo se crea y cuándo se libera un recurso. RAII (Rust/C++), `defer` (Go), `try-with-resources` (Java) y `using` (C#) atan la liberación al ámbito.",
    "resultados": ["Explicar el ciclo de vida de un recurso.", "Liberar automáticamente al salir del ámbito.", "Comparar RAII, defer y GC."],
    "temas": [("Ciclo de vida", "Crear → usar → liberar"), ("RAII", "La liberación va atada al ámbito"), ("Liberación automática", "defer, using, destructor")],
    "definiciones": [("Ciclo de vida", "el tiempo entre que un recurso se crea y se libera. Clave: gestionarlo evita fugas."), ("RAII", "Resource Acquisition Is Initialization: el recurso se libera al destruirse el dueño. Clave: Rust/C++."), ("defer/using", "mecanismos que garantizan la liberación al salir del ámbito. Clave: Go, C#, Java.")],
    "situacion": "Un archivo abierto debe cerrarse; una conexión, liberarse. RAII y defer garantizan que ocurra aunque haya un error, atando la liberación al fin del ámbito.",
    "entrada": "un entero `n` (valor del recurso)",
    "salida": "`valor=<n> estado=liberado`",
    "formula": "crear recurso(n), usarlo, liberarlo al salir",
    "algoritmo": "LEER n ; crear recurso ; usar ; liberar al salir del ámbito",
    "casos": [("5", "valor=5 estado=liberado"), ("0", "valor=0 estado=liberado"), ("9", "valor=9 estado=liberado")],
    "comparacion": [("Sintáctica", "`Drop` (Rust), `defer` (Go), `using`/`try-with-resources` (C#/Java)."), ("Semántica", "Rust/C++ liberan determinísticamente; Java/Python dependen del GC salvo cierre explícito."), ("Paradigmática", "SQL gestiona transacciones (COMMIT/ROLLBACK) como ciclo de vida.")],
    "familia": "En C++ el destructor libera al salir del ámbito, como el `Drop` de Rust. En Python, el `with` (context manager).",
    "errores": [("No liberar recursos", "fugas de memoria/handles", "usar RAII/defer/using para atarlo al ámbito"), ("Confiar solo en el GC para recursos no-memoria", "archivos abiertos demasiado tiempo", "cerrar explícitamente archivos y conexiones")],
    "faq": [("¿GC libera todo?", "Libera memoria, pero no siempre a tiempo ni otros recursos (archivos): ciérralos tú."), ("¿RAII o defer?", "RAII ata la liberación al tipo; defer, a la función. Ambos garantizan el cierre.")],
    "reto": "Simula abrir y cerrar dos recursos en orden inverso y resuélvelo en **Go** con `defer`.",
    "impls": {
        "python": r"""import sys


class Recurso:
    def __init__(self, valor):
        self.valor = valor

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass  # aquí se liberaría


n = int(sys.stdin.readline())
with Recurso(n) as r:
    valor = r.valor
print(f"valor={valor} estado=liberado")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let valor;
{
  const recurso = { valor: n };
  valor = recurso.valor;
  // en JS el GC libera; aquí el ámbito marca el fin de uso
}
console.log(`valor=${valor} estado=liberado`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let valor: number;
{
  const recurso = { valor: n };
  valor = recurso.valor;
}
console.log(`valor=${valor} estado=liberado`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static class Recurso implements AutoCloseable {
        final int valor;
        Recurso(int v) { this.valor = v; }
        public void close() { /* se libera aquí */ }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int valor;
        try (Recurso r = new Recurso(n)) {
            valor = r.valor;
        }
        System.out.println("valor=" + valor + " estado=liberado");
    }
}
""",
        "csharp": r"""using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int valor;
using (var r = new Recurso(n)) {
    valor = r.Valor;
}
Console.WriteLine($"valor={valor} estado=liberado");

class Recurso : IDisposable {
    public int Valor { get; }
    public Recurso(int v) { Valor = v; }
    public void Dispose() { /* se libera aquí */ }
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
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	valor := 0
	func() {
		defer func() { /* se libera al salir */ }()
		valor = n
	}()
	fmt.Printf("valor=%d estado=liberado\n", valor)
}
""",
        "rust": r"""use std::io::Read;

struct Recurso {
    valor: i64,
}

impl Drop for Recurso {
    fn drop(&mut self) {
        // se libera automáticamente al salir del ámbito
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let valor;
    {
        let r = Recurso { valor: n };
        valor = r.valor;
    } // aquí se ejecuta Drop
    println!("valor={valor} estado=liberado");
}
""",
        "c": r"""#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long *recurso = malloc(sizeof(long));
    *recurso = n;
    long valor = *recurso;
    free(recurso); /* liberación manual */
    printf("valor=%ld estado=liberado\n", valor);
    return 0;
}
""",
        "php": r"""<?php
class Recurso {
    public function __construct(public int $valor) {}
    public function __destruct() { /* se libera aquí */ }
}

$n = (int) trim(fgets(STDIN));
$r = new Recurso($n);
$valor = $r->valor;
unset($r); // libera el recurso
echo "valor=$valor estado=liberado\n";
""",
        "sql": r"""-- SQL: el ciclo de vida se gestiona con transacciones; aquí se ilustra el valor.
WITH nums(n) AS (VALUES (5), (0), (9))
SELECT printf('valor=%d estado=liberado', n) AS resultado FROM nums;
""",
    },
}

S[104] = {
    "descripcion": "Dada una línea de texto (como el contenido de un archivo), contar sus palabras y sus caracteres.",
    "objetivo": "Procesar **contenido textual** como el de un archivo: leer una línea y extraer información (palabras, caracteres). Es el modelo de la lectura de archivos, aquí por la entrada estándar para poder verificarlo.",
    "resultados": ["Leer una línea completa con espacios.", "Contar palabras y caracteres.", "Relacionarlo con la lectura de archivos."],
    "temas": [("Leer contenido", "Una línea con espacios"), ("Contar palabras", "Separar por espacios"), ("Contar caracteres", "Longitud del texto")],
    "definiciones": [("Contenido de texto", "los caracteres de un archivo o entrada. Clave: se procesa línea a línea."), ("Palabra", "secuencia separada por espacios. Clave: se cuenta partiendo por espacios."), ("Carácter", "cada símbolo, incluidos los espacios. Clave: la longitud total.")],
    "situacion": "Contar líneas, palabras o caracteres (como `wc`) es el 'hola mundo' del procesamiento de archivos. Aquí el contenido llega por stdin para poder verificar el resultado.",
    "entrada": "una línea de texto (puede contener espacios)",
    "salida": "`palabras=<número de palabras> caracteres=<longitud incluyendo espacios>`",
    "formula": "palabras = partes por espacio; caracteres = longitud de la línea",
    "algoritmo": "LEER linea ; palabras <- partir por espacios ; caracteres <- longitud",
    "casos": [("hola mundo", "palabras=2 caracteres=10"), ("abc", "palabras=1 caracteres=3"), ("a b c d", "palabras=4 caracteres=7")],
    "comparacion": [("Sintáctica", "`split()` y `len()` (Python) vs. equivalentes por lenguaje."), ("Semántica", "La longitud incluye los espacios; las palabras no."), ("Paradigmática", "SQL cuenta con funciones de texto y agregación.")],
    "familia": "En Ruby `linea.split.size` y `linea.length`. El comando Unix `wc` hace justo esto.",
    "errores": [("Contar espacios como palabras", "palabras vacías", "partir por uno o más espacios"), ("Olvidar quitar el salto de línea", "un carácter de más", "recortar el `\\n` final antes de contar")],
    "faq": [("¿Por qué stdin y no un archivo?", "Para poder verificar el resultado con casos; un archivo se leería igual, línea a línea."), ("¿Los caracteres incluyen espacios?", "Sí: son parte del contenido; las palabras no.")],
    "reto": "Cuenta también las vocales de la línea y resuélvelo en **Python**.",
    "impls": {
        "python": r"""import sys

linea = sys.stdin.readline().rstrip("\n")
palabras = len(linea.split())
print(f"palabras={palabras} caracteres={len(linea)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const linea = readFileSync(0, "utf8").replace(/\r?\n$/, "");
const palabras = linea.split(/\s+/).filter((w) => w.length > 0).length;
console.log(`palabras=${palabras} caracteres=${linea.length}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const linea: string = readFileSync(0, "utf8").replace(/\r?\n$/, "");
const palabras = linea.split(/\s+/).filter((w) => w.length > 0).length;
console.log(`palabras=${palabras} caracteres=${linea.length}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String linea = br.readLine();
        int palabras = linea.trim().isEmpty() ? 0 : linea.trim().split("\\s+").length;
        System.out.println("palabras=" + palabras + " caracteres=" + linea.length());
    }
}
""",
        "csharp": r"""using System;

string linea = Console.In.ReadToEnd().TrimEnd('\r', '\n');
int palabras = linea.Split(new[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries).Length;
Console.WriteLine($"palabras={palabras} caracteres={linea.Length}");
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
	linea := strings.TrimRight(line, "\r\n")
	palabras := len(strings.Fields(linea))
	fmt.Printf("palabras=%d caracteres=%d\n", palabras, len(linea))
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let linea = s.trim_end_matches(['\r', '\n']);
    let palabras = linea.split_whitespace().count();
    println!("palabras={} caracteres={}", palabras, linea.len());
}
""",
        "c": r"""#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void) {
    char buf[4096];
    if (fgets(buf, sizeof buf, stdin) == NULL) return 1;
    buf[strcspn(buf, "\r\n")] = '\0';
    int caracteres = (int) strlen(buf);
    int palabras = 0, dentro = 0;
    for (int i = 0; buf[i]; i++) {
        if (isspace((unsigned char) buf[i])) {
            dentro = 0;
        } else if (!dentro) {
            dentro = 1;
            palabras++;
        }
    }
    printf("palabras=%d caracteres=%d\n", palabras, caracteres);
    return 0;
}
""",
        "php": r"""<?php
$linea = rtrim(fgets(STDIN), "\r\n");
$palabras = $linea === "" ? 0 : count(preg_split('/\s+/', trim($linea)));
echo "palabras=$palabras caracteres=" . strlen($linea) . "\n";
""",
        "sql": r"""-- SQL: longitud con length(); palabras con funciones de texto (ilustrativo).
WITH t(linea) AS (VALUES ('hola mundo'))
SELECT printf('palabras=%d caracteres=%d',
       length(linea) - length(replace(linea, ' ', '')) + 1, length(linea)) AS resultado
FROM t;
""",
    },
}

S[105] = {
    "descripcion": "Producir un objeto JSON con nombre y edad a partir de la entrada.",
    "objetivo": "Trabajar con **JSON**: el formato universal de intercambio de datos. Aquí se **serializa** (construye) un objeto JSON con un formato fijo; en la práctica también se deserializa (parsea).",
    "resultados": ["Serializar datos a JSON.", "Respetar el formato (comillas, dos puntos).", "Reconocer JSON como formato de intercambio."],
    "temas": [("JSON", "Formato de intercambio de datos"), ("Serializar", "De datos a texto JSON"), ("Deserializar", "De texto JSON a datos")],
    "definiciones": [("JSON", "formato de texto para datos estructurados (objetos, arreglos). Clave: universal entre lenguajes."), ("Serializar", "convertir datos en su representación de texto (JSON). Clave: para enviarlos o guardarlos."), ("Deserializar", "reconstruir datos desde el texto JSON. Clave: la operación inversa.")],
    "situacion": "Las APIs web hablan JSON. Un objeto `{\"nombre\": \"Ada\", \"edad\": 36}` viaja entre un servidor en Go y un cliente en JavaScript sin problema: JSON es el idioma común.",
    "entrada": "una línea `nombre edad` (una palabra y un entero)",
    "salida": '`{"nombre": "<nombre>", "edad": <edad>}`',
    "formula": "objeto JSON con las claves nombre y edad",
    "algoritmo": "LEER nombre, edad ; construir objeto ; serializar a JSON",
    "casos": [("Ada 36", '{"nombre": "Ada", "edad": 36}'), ("Bo 5", '{"nombre": "Bo", "edad": 5}'), ("Cy 99", '{"nombre": "Cy", "edad": 99}')],
    "comparacion": [("Sintáctica", "Librerías `json` (Python), `JSON.stringify` (JS), pero el formato es idéntico."), ("Semántica", "Las cadenas van entre comillas dobles; los números sin comillas."), ("Paradigmática", "SQL genera JSON con funciones `json_object` (aquí, con printf).")],
    "familia": "En Ruby `to_json`. En casi todos hay una librería estándar o popular para JSON; el formato no cambia.",
    "errores": [("Comillas simples en JSON", "JSON exige comillas dobles", "usar comillas dobles siempre"), ("Poner comillas a los números", "tipo incorrecto", "los números van sin comillas")],
    "faq": [("¿Construir JSON a mano o con librería?", "En la práctica, librería (escapa bien); aquí a mano para fijar el formato exacto."), ("¿JSON solo para web?", "No: también para configuración, logs y almacenamiento.")],
    "reto": "Añade un campo booleano `activo` y resuélvelo en **JavaScript** con `JSON.stringify`.",
    "impls": {
        "python": r"""import sys

t = sys.stdin.readline().split()
nombre, edad = t[0], int(t[1])
print(f'{{"nombre": "{nombre}", "edad": {edad}}}')
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const t = readFileSync(0, "utf8").trim().split(/\s+/);
const nombre = t[0];
const edad = parseInt(t[1], 10);
console.log(`{"nombre": "${nombre}", "edad": ${edad}}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const t: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
const nombre: string = t[0];
const edad: number = parseInt(t[1], 10);
console.log(`{"nombre": "${nombre}", "edad": ${edad}}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        String nombre = t[0];
        int edad = Integer.parseInt(t[1]);
        System.out.println("{\"nombre\": \"" + nombre + "\", \"edad\": " + edad + "}");
    }
}
""",
        "csharp": r"""using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
string nombre = t[0];
int edad = int.Parse(t[1]);
Console.WriteLine($"{{\"nombre\": \"{nombre}\", \"edad\": {edad}}}");
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
	nombre := t[0]
	edad, _ := strconv.Atoi(t[1])
	fmt.Printf("{\"nombre\": \"%s\", \"edad\": %d}\n", nombre, edad)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let nombre = t[0];
    let edad: i64 = t[1].parse().unwrap();
    println!("{{\"nombre\": \"{nombre}\", \"edad\": {edad}}}");
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    char nombre[64];
    long edad;
    if (scanf("%63s %ld", nombre, &edad) != 2) return 1;
    printf("{\"nombre\": \"%s\", \"edad\": %ld}\n", nombre, edad);
    return 0;
}
""",
        "php": r"""<?php
$t = preg_split('/\s+/', trim(fgets(STDIN)));
$nombre = $t[0];
$edad = (int) $t[1];
echo "{\"nombre\": \"$nombre\", \"edad\": $edad}\n";
""",
        "sql": r"""-- SQL: construye JSON con printf (o json_object en motores con la extensión).
WITH personas(nombre, edad) AS (VALUES ('Ada', 36))
SELECT printf('{"nombre": "%s", "edad": %d}', nombre, edad) AS resultado FROM personas;
""",
    },
}

S[106] = {
    "descripcion": "Convertir una lista de valores a una línea CSV e informar cuántos campos tiene.",
    "objetivo": "Cerrar la parte con **persistencia y formatos tabulares**: CSV (valores separados por comas) es el formato más simple para guardar y compartir datos en tabla. Aquí se serializa una fila y se cuentan sus campos.",
    "resultados": ["Serializar valores a una línea CSV.", "Contar los campos.", "Reconocer CSV frente a JSON."],
    "temas": [("CSV", "Valores separados por comas"), ("Campo", "Cada valor de la fila"), ("Persistencia", "Guardar datos en formato de texto")],
    "definiciones": [("CSV", "formato tabular: filas de valores separados por comas. Clave: simple y universal."), ("Campo", "cada valor de una fila CSV. Clave: separado por el delimitador."), ("Persistencia", "guardar datos para recuperarlos después. Clave: archivos, bases de datos.")],
    "situacion": "Exportar a Excel, cargar datos en una base, intercambiar tablas: el CSV es el mínimo común denominador. Una fila `1,2,3` con 3 campos es su unidad.",
    "entrada": "una línea con enteros separados por espacio",
    "salida": "`csv=<valores separados por coma> campos=<cantidad>`",
    "formula": "csv = unir con coma ; campos = cantidad de valores",
    "algoritmo": "LEER lista ; csv <- unir con , ; campos <- longitud",
    "casos": [("1 2 3", "csv=1,2,3 campos=3"), ("5", "csv=5 campos=1"), ("10 20", "csv=10,20 campos=2")],
    "comparacion": [("Sintáctica", "`','.join(...)` (Python), `.join(',')` (JS), bucle (C)."), ("Semántica", "CSV real necesita escapar comas y comillas; aquí los datos son simples."), ("Paradigmática", "SQL exporta/importa CSV con comandos del motor.")],
    "familia": "En Ruby `arr.join(',')`. Casi todos tienen una librería CSV que maneja comillas y saltos correctamente.",
    "errores": [("No escapar comas dentro de un campo", "CSV corrupto", "usar una librería CSV para datos reales"), ("Confundir campos con caracteres", "contar mal", "los campos se separan por el delimitador")],
    "faq": [("¿CSV o JSON?", "CSV para tablas simples y planas; JSON para datos anidados y estructurados."), ("¿CSV siempre usa comas?", "Casi siempre; algunos usan punto y coma o tabuladores según la configuración regional.")],
    "reto": "Convierte de CSV de vuelta a lista (parsear) y resuélvelo en **Python** con el módulo `csv`.",
    "impls": {
        "python": r"""import sys

nums = sys.stdin.read().split()
csv = ",".join(nums)
print(f"csv={csv} campos={len(nums)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`csv=${nums.join(",")} campos=${nums.length}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const nums: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`csv=${nums.join(",")} campos=${nums.length}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] nums = br.readLine().trim().split("\\s+");
        System.out.println("csv=" + String.join(",", nums) + " campos=" + nums.length);
    }
}
""",
        "csharp": r"""using System;

string[] nums = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"csv={string.Join(",", nums)} campos={nums.Length}");
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
	nums := strings.Fields(line)
	fmt.Printf("csv=%s campos=%d\n", strings.Join(nums, ","), len(nums))
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<&str> = s.split_whitespace().collect();
    println!("csv={} campos={}", nums.join(","), nums.len());
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    char tok[64];
    int campos = 0;
    printf("csv=");
    while (scanf("%63s", tok) == 1) {
        if (campos > 0) printf(",");
        printf("%s", tok);
        campos++;
    }
    printf(" campos=%d\n", campos);
    return 0;
}
""",
        "php": r"""<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
echo "csv=" . implode(",", $nums) . " campos=" . count($nums) . "\n";
""",
        "sql": r"""-- SQL: group_concat produce una fila CSV.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT 'csv=' || group_concat(x, ',') || printf(' campos=%d', count(*)) AS resultado FROM nums;
""",
    },
}


def main():
    for num, spec in S.items():
        g3.write_class(num, spec)
        print(f"Clase {num:03d} generada.")


if __name__ == "__main__":
    main()
