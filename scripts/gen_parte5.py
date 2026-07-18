"""Parte 5 — Funciones y modularidad (clases 073-088). Reutiliza gen_parte3.write_class."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_parte3 as g3  # noqa: E402

S = {}

S[73] = {
    "descripcion": "Definir una función suma(a, b) y usarla para sumar dos enteros.",
    "objetivo": "Entender la anatomía de una función: **firma** (nombre + parámetros + tipo de retorno), **argumentos** (los valores que se pasan) y **retorno** (el valor que devuelve). Es la unidad de reutilización de todo programa.",
    "resultados": ["Definir una función con parámetros y retorno.", "Distinguir parámetro de argumento.", "Invocar la función y usar su valor."],
    "temas": [("Firma", "Nombre, parámetros y tipo de retorno"), ("Parámetro vs. argumento", "El hueco vs. el valor real"), ("Retorno", "El valor que produce"), ("Reutilización", "Llamar en vez de repetir")],
    "definiciones": [("Función", "bloque con nombre que recibe parámetros y devuelve un valor. Clave: la unidad de reutilización."), ("Firma", "nombre + parámetros + tipo de retorno. Clave: define cómo se usa."), ("Parámetro", "variable del hueco en la definición. Clave: recibe el argumento."), ("Argumento", "valor concreto que se pasa al llamar. Clave: llena el parámetro.")],
    "situacion": "En vez de repetir `a + b` por todas partes, se define `suma(a, b)` una vez y se llama. La firma es el contrato: qué recibe y qué devuelve.",
    "entrada": "una línea `a b` (dos enteros)",
    "salida": "`suma=<a+b>`",
    "formula": "suma(a, b) = a + b",
    "algoritmo": "FUNCION suma(a, b): DEVOLVER a+b\nLEER a, b ; ESCRIBIR \"suma=\" suma(a,b)",
    "casos": [("3 4", "suma=7"), ("10 20", "suma=30"), ("-5 5", "suma=0")],
    "comparacion": [("Sintáctica", "`def` (Python), `func` (Go), `fn` (Rust), tipo de retorno explícito (Java/C)."), ("Semántica", "Estáticos declaran los tipos de parámetros y retorno; dinámicos no."), ("Paradigmática", "SQL define la operación en la propia consulta.")],
    "familia": "En Ruby `def suma(a, b)`. En Haskell `suma a b = a + b`, con la firma inferida.",
    "errores": [("Confundir parámetro con argumento", "usar mal los términos y el orden", "recordar: parámetro en la definición, argumento en la llamada"), ("Olvidar el return", "la función no devuelve nada", "asegurar que la función retorna el valor")],
    "faq": [("¿Función o procedimiento?", "Una función devuelve valor; un procedimiento solo actúa. Aquí devolvemos."), ("¿Por qué reutilizar?", "Menos repetición, menos errores, un solo lugar que cambiar.")],
    "reto": "Añade una función `resta(a, b)` y muestra ambos resultados; resuélvelo en **Go**.",
    "impls": {
        "python": r"""import sys


def suma(a, b):
    return a + b


a, b = map(int, sys.stdin.readline().split())
print(f"suma={suma(a, b)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

function suma(a, b) {
  return a + b;
}

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${suma(a, b)}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

function suma(a: number, b: number): number {
  return a + b;
}

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${suma(a, b)}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static int suma(int a, int b) {
        return a + b;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        System.out.println("suma=" + suma(Integer.parseInt(p[0]), Integer.parseInt(p[1])));
    }
}
""",
        "csharp": r"""using System;

int Suma(int a, int b) => a + b;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"suma={Suma(int.Parse(p[0]), int.Parse(p[1]))}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func suma(a, b int) int {
	return a + b
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	fmt.Printf("suma=%d\n", suma(a, b))
}
""",
        "rust": r"""use std::io::Read;

fn suma(a: i64, b: i64) -> i64 {
    a + b
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("suma={}", suma(v[0], v[1]));
}
""",
        "c": r"""#include <stdio.h>

long suma(long a, long b) {
    return a + b;
}

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("suma=%ld\n", suma(a, b));
    return 0;
}
""",
        "php": r"""<?php
function suma($a, $b) {
    return $a + $b;
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "suma=" . suma((int) $a, (int) $b) . "\n";
""",
        "sql": r"""-- SQL: la operación se expresa en la propia consulta.
WITH pares(a, b) AS (VALUES (3, 4), (10, 20), (-5, 5))
SELECT printf('suma=%d', a + b) AS resultado FROM pares;
""",
    },
}

S[74] = {
    "descripcion": "Calcular una potencia con exponente por defecto 2: si solo llega la base, se eleva al cuadrado.",
    "objetivo": "Usar **parámetros por defecto**: un parámetro que toma un valor predefinido si no se pasa. Permite funciones flexibles sin sobrecargarlas. C y Go no los tienen; se simula.",
    "resultados": ["Definir un parámetro con valor por defecto.", "Llamar la función con y sin ese argumento.", "Reconocer lenguajes sin parámetros por defecto."],
    "temas": [("Parámetro por defecto", "Valor usado si no se pasa"), ("Argumento opcional", "Se puede omitir"), ("Flexibilidad", "Una función, varios usos"), ("Sin soporte nativo", "C y Go lo simulan")],
    "definiciones": [("Parámetro por defecto", "toma un valor predefinido si el argumento se omite. Clave: `exp=2`."), ("Argumento opcional", "el que se puede no pasar. Clave: cae en el valor por defecto."), ("Sobrecarga", "varias funciones con el mismo nombre y distinta firma. Clave: alternativa en Java/C."), ("Simular defecto", "en C/Go, con dos funciones o comprobando la ausencia. Clave: no es nativo.")],
    "situacion": "`potencia(base, exp=2)` permite `potencia(3)` = 9 y `potencia(2, 3)` = 8 con una sola definición. Sin defectos habría que escribir dos funciones o pasar siempre el exponente.",
    "entrada": "una línea: `base` (exp por defecto 2) o `base exp`",
    "salida": "`resultado=<base^exp>`",
    "formula": "potencia(base, exp=2) = base^exp",
    "algoritmo": "LEER tokens\nbase <- tokens[0] ; exp <- tokens[1] SI EXISTE SINO 2\nESCRIBIR \"resultado=\" base^exp",
    "casos": [("3", "resultado=9"), ("2 3", "resultado=8"), ("5", "resultado=25")],
    "comparacion": [("Sintáctica", "`def f(base, exp=2)` (Python) vs. simulación con comprobación (C/Go)."), ("Semántica", "Python/JS/C#/PHP tienen defectos nativos; C/Go no."), ("Paradigmática", "SQL usa COALESCE para valores por defecto.")],
    "familia": "En Ruby `def potencia(base, exp = 2)`. En Kotlin `fun potencia(base: Int, exp: Int = 2)`.",
    "errores": [("Poner el parámetro con defecto antes de uno obligatorio", "error de definición", "los parámetros con defecto van al final"), ("Asumir defectos en C/Go", "no existen", "simular con dos funciones o comprobando argumentos")],
    "faq": [("¿Todos los lenguajes tienen defectos?", "No: C y Go no; se simulan con sobrecarga o comprobación."), ("¿El defecto se evalúa una vez?", "Cuidado en Python con defectos mutables (lista): se comparten entre llamadas.")],
    "reto": "Añade un tercer parámetro `signo` con defecto '+' y resuélvelo en **Kotlin**.",
    "impls": {
        "python": r"""import sys


def potencia(base, exp=2):
    r = 1
    for _ in range(exp):
        r *= base
    return r


t = sys.stdin.readline().split()
base = int(t[0])
if len(t) > 1:
    print(f"resultado={potencia(base, int(t[1]))}")
else:
    print(f"resultado={potencia(base)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

function potencia(base, exp = 2) {
  let r = 1;
  for (let i = 0; i < exp; i++) r *= base;
  return r;
}

const t = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`resultado=${t.length > 1 ? potencia(t[0], t[1]) : potencia(t[0])}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

function potencia(base: number, exp = 2): number {
  let r = 1;
  for (let i = 0; i < exp; i++) r *= base;
  return r;
}

const t: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`resultado=${t.length > 1 ? potencia(t[0], t[1]) : potencia(t[0])}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // Java no tiene defectos: se simula con sobrecarga.
    static long potencia(long base) {
        return potencia(base, 2);
    }

    static long potencia(long base, int exp) {
        long r = 1;
        for (int i = 0; i < exp; i++) r *= base;
        return r;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        long base = Long.parseLong(t[0]);
        long r = t.length > 1 ? potencia(base, Integer.parseInt(t[1])) : potencia(base);
        System.out.println("resultado=" + r);
    }
}
""",
        "csharp": r"""using System;

long Potencia(long baseN, int exp = 2) {
    long r = 1;
    for (int i = 0; i < exp; i++) r *= baseN;
    return r;
}

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long b = long.Parse(t[0]);
long res = t.Length > 1 ? Potencia(b, int.Parse(t[1])) : Potencia(b);
Console.WriteLine($"resultado={res}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// Go no tiene defectos: se simula con la lógica de llamada.
func potencia(base int64, exp int) int64 {
	var r int64 = 1
	for i := 0; i < exp; i++ {
		r *= base
	}
	return r
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	t := strings.Fields(line)
	base, _ := strconv.ParseInt(t[0], 10, 64)
	exp := 2
	if len(t) > 1 {
		exp, _ = strconv.Atoi(t[1])
	}
	fmt.Printf("resultado=%d\n", potencia(base, exp))
}
""",
        "rust": r"""use std::io::Read;

fn potencia(base: i64, exp: u32) -> i64 {
    base.pow(exp)
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let base: i64 = t[0].parse().unwrap();
    let exp: u32 = if t.len() > 1 { t[1].parse().unwrap() } else { 2 };
    println!("resultado={}", potencia(base, exp));
}
""",
        "c": r"""#include <stdio.h>

/* C no tiene defectos: se simula pasando siempre el exponente. */
long potencia(long base, int exp) {
    long r = 1;
    for (int i = 0; i < exp; i++) r *= base;
    return r;
}

int main(void) {
    long base;
    int exp;
    int leidos = scanf("%ld %d", &base, &exp);
    if (leidos < 1) return 1;
    if (leidos < 2) exp = 2;
    printf("resultado=%ld\n", potencia(base, exp));
    return 0;
}
""",
        "php": r"""<?php
function potencia($base, $exp = 2) {
    $r = 1;
    for ($i = 0; $i < $exp; $i++) {
        $r *= $base;
    }
    return $r;
}

$t = preg_split('/\s+/', trim(fgets(STDIN)));
$base = (int) $t[0];
$res = count($t) > 1 ? potencia($base, (int) $t[1]) : potencia($base);
echo "resultado=$res\n";
""",
        "sql": r"""-- SQL: COALESCE simula el valor por defecto (aquí, exponente 2 mediante base*base).
WITH datos(base) AS (VALUES (3), (5))
SELECT printf('resultado=%d', base * base) AS resultado FROM datos;
""",
    },
}

S[75] = {
    "descripcion": "Construir la representación de un punto con argumentos por nombre (x, y).",
    "objetivo": "Usar **argumentos nombrados** (por palabra clave): pasar los valores indicando a qué parámetro corresponden, mejorando la legibilidad y permitiendo cualquier orden. No todos los lenguajes los tienen.",
    "resultados": ["Pasar argumentos por nombre.", "Explicar la ventaja de legibilidad y orden libre.", "Reconocer lenguajes sin argumentos nombrados."],
    "temas": [("Argumento nombrado", "Se indica el parámetro por su nombre"), ("Orden libre", "No depende de la posición"), ("Legibilidad", "Queda claro qué es cada valor"), ("Soporte por lenguaje", "Python/C# sí; Java/Go no")],
    "definiciones": [("Argumento nombrado", "se pasa indicando el parámetro (`y=4`). Clave: claridad y orden libre."), ("Argumento posicional", "se pasa por su posición. Clave: depende del orden."), ("Palabra clave", "el nombre del parámetro usado al llamar (Python `**kwargs`). Clave: base de los nombrados."), ("Legibilidad de la llamada", "entender qué es cada valor sin ver la firma. Clave: menos errores.")],
    "situacion": "`crear(ancho=800, alto=600)` se lee mejor que `crear(800, 600)`: nadie se pregunta cuál es cuál. Los argumentos nombrados evitan confundir el orden de parámetros parecidos.",
    "entrada": "una línea `a b` (dos enteros: x, y)",
    "salida": "`punto(x=<a>, y=<b>)`",
    "formula": "punto(x=a, y=b)",
    "algoritmo": "LEER a, b\nESCRIBIR punto(x=a, y=b)",
    "casos": [("3 4", "punto(x=3, y=4)"), ("0 -2", "punto(x=0, y=-2)"), ("5 5", "punto(x=5, y=5)")],
    "comparacion": [("Sintáctica", "`punto(x=a, y=b)` (Python/C#) vs. posicional (Java/Go/C)."), ("Semántica", "Con nombres el orden es libre; sin ellos, importa la posición."), ("Paradigmática", "SQL nombra las columnas, algo análogo a nombrar argumentos.")],
    "familia": "En Ruby con argumentos de palabra clave: `punto(x: a, y: b)`. Kotlin permite `punto(x = a, y = b)`.",
    "errores": [("Confiar en el orden con parámetros parecidos", "intercambiar x e y", "usar argumentos nombrados donde el lenguaje los ofrezca"), ("Asumir nombres en Java/Go", "no existen", "documentar bien o usar objetos/structs con campos nombrados")],
    "faq": [("¿Qué lenguajes tienen nombrados?", "Python, C#, Kotlin, Ruby, Swift. Java y Go no de forma nativa."), ("¿Y si no los hay?", "Se usan structs/objetos con campos nombrados para lograr claridad.")],
    "reto": "Añade un tercer campo `z` con defecto 0 y resuélvelo en **Python** con argumentos de palabra clave.",
    "impls": {
        "python": r"""import sys


def punto(x, y):
    return f"punto(x={x}, y={y})"


a, b = map(int, sys.stdin.readline().split())
print(punto(x=a, y=b))
""",
        "javascript": r"""import { readFileSync } from "node:fs";

// JS simula argumentos nombrados con un objeto.
function punto({ x, y }) {
  return `punto(x=${x}, y=${y})`;
}

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(punto({ x: a, y: b }));
""",
        "typescript": r"""import { readFileSync } from "node:fs";

function punto({ x, y }: { x: number; y: number }): string {
  return `punto(x=${x}, y=${y})`;
}

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(punto({ x: a, y: b }));
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // Java no tiene argumentos nombrados: se pasan por posición.
    static String punto(int x, int y) {
        return "punto(x=" + x + ", y=" + y + ")";
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        System.out.println(punto(Integer.parseInt(p[0]), Integer.parseInt(p[1])));
    }
}
""",
        "csharp": r"""using System;

string Punto(int x, int y) => $"punto(x={x}, y={y})";

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine(Punto(x: int.Parse(p[0]), y: int.Parse(p[1])));
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// Go no tiene argumentos nombrados: se usan structs con campos nombrados.
type Punto struct {
	X, Y int
}

func (p Punto) String() string {
	return fmt.Sprintf("punto(x=%d, y=%d)", p.X, p.Y)
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	fmt.Println(Punto{X: a, Y: b})
}
""",
        "rust": r"""use std::io::Read;

fn punto(x: i64, y: i64) -> String {
    format!("punto(x={x}, y={y})")
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("{}", punto(v[0], v[1]));
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    /* C no tiene argumentos nombrados: posicionales. */
    printf("punto(x=%ld, y=%ld)\n", a, b);
    return 0;
}
""",
        "php": r"""<?php
function punto($x, $y) {
    return "punto(x=$x, y=$y)";
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
// PHP 8 admite argumentos nombrados.
echo punto(x: (int) $a, y: (int) $b) . "\n";
""",
        "sql": r"""-- SQL nombra columnas, análogo a nombrar argumentos.
WITH puntos(x, y) AS (VALUES (3, 4), (0, -2), (5, 5))
SELECT printf('punto(x=%d, y=%d)', x, y) AS resultado FROM puntos;
""",
    },
}

S[76] = {
    "descripcion": "Sumar una cantidad variable de enteros con una función variádica.",
    "objetivo": "Definir una función **variádica**: acepta un número variable de argumentos. Es lo que hay detrás de `print(...)` o `sum(...)`. Cada lenguaje lo expresa con `*args`, `...`, `params` o slices.",
    "resultados": ["Definir una función que acepta N argumentos.", "Recorrer los argumentos variádicos.", "Reconocer la sintaxis de cada lenguaje."],
    "temas": [("Función variádica", "Número variable de argumentos"), ("Recolectar en una colección", "Los argumentos llegan como lista/slice"), ("Sintaxis por lenguaje", "*args, ..., params[]"), ("Usos comunes", "print, sum, format")],
    "definiciones": [("Función variádica", "acepta un número variable de argumentos. Clave: `sum(1,2,3,...)`."), ("*args / ...", "sintaxis para recolectar argumentos variables. Clave: llegan como colección."), ("Empaquetar", "reunir los argumentos sueltos en una lista. Clave: dentro de la función."), ("Desempaquetar", "expandir una lista en argumentos sueltos. Clave: la operación inversa.")],
    "situacion": "`printf`, `sum`, `max` aceptan cuantos argumentos quieras. Una función variádica los recibe como una colección y los procesa; es la base de muchas utilidades.",
    "entrada": "una línea con enteros separados por espacio",
    "salida": "`suma=<suma de todos>`",
    "formula": "suma(...nums) = Σ nums",
    "algoritmo": "FUNCION suma(...nums): DEVOLVER Σ nums\nLEER lista ; ESCRIBIR \"suma=\" suma(lista)",
    "casos": [("1 2 3", "suma=6"), ("5", "suma=5"), ("10 20 30 40", "suma=100")],
    "comparacion": [("Sintáctica", "`*nums` (Python), `...nums` (JS/Java), `nums ...int` (Go), `&[i64]` (Rust)."), ("Semántica", "Los argumentos se recolectan en una colección dentro de la función."), ("Paradigmática", "SQL agrega filas con SUM(), no argumentos.")],
    "familia": "En Ruby `def suma(*nums)`. En C, `stdarg.h` con `va_list` (más manual).",
    "errores": [("Confundir empaquetar con desempaquetar", "pasar una lista donde se esperan sueltos", "usar el operador de expansión (`*`, `...`) al desempaquetar"), ("Olvidar el caso de cero argumentos", "error o suma indefinida", "que la función maneje la lista vacía (suma 0)")],
    "faq": [("¿Variádica o pasar una lista?", "Variádica para llamadas cómodas; lista cuando ya la tienes construida."), ("¿C tiene variádicas?", "Sí, con `stdarg.h`, pero es más manual y propenso a errores.")],
    "reto": "Haz una función variádica `max(...)` y resuélvelo en **Go** con `nums ...int`.",
    "impls": {
        "python": r"""import sys


def suma(*nums):
    total = 0
    for n in nums:
        total += n
    return total


nums = [int(x) for x in sys.stdin.read().split()]
print(f"suma={suma(*nums)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

function suma(...nums) {
  return nums.reduce((a, b) => a + b, 0);
}

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${suma(...nums)}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

function suma(...nums: number[]): number {
  return nums.reduce((a, b) => a + b, 0);
}

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${suma(...nums)}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static long suma(int... nums) {
        long total = 0;
        for (int n : nums) total += n;
        return total;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int[] nums = new int[p.length];
        for (int i = 0; i < p.length; i++) nums[i] = Integer.parseInt(p[i]);
        System.out.println("suma=" + suma(nums));
    }
}
""",
        "csharp": r"""using System;
using System.Linq;

long Suma(params int[] nums) => nums.Sum(x => (long) x);

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"suma={Suma(p.Select(int.Parse).ToArray())}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func suma(nums ...int) int {
	total := 0
	for _, n := range nums {
		total += n
	}
	return total
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	var nums []int
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		nums = append(nums, n)
	}
	fmt.Printf("suma=%d\n", suma(nums...))
}
""",
        "rust": r"""use std::io::Read;

fn suma(nums: &[i64]) -> i64 {
    nums.iter().sum()
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("suma={}", suma(&nums));
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    /* C variádico real usa stdarg.h; aquí sumamos leyendo la entrada. */
    long suma = 0, x;
    while (scanf("%ld", &x) == 1) {
        suma += x;
    }
    printf("suma=%ld\n", suma);
    return 0;
}
""",
        "php": r"""<?php
function suma(...$nums) {
    return array_sum($nums);
}

$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "suma=" . suma(...$nums) . "\n";
""",
        "sql": r"""-- SQL: SUM() agrega filas, no argumentos variádicos.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT printf('suma=%d', sum(x)) AS resultado FROM nums;
""",
    },
}

S[77] = {
    "descripcion": "Dividir dos enteros devolviendo a la vez el cociente y el resto (múltiples valores).",
    "objetivo": "Devolver **más de un valor** de una función y **desestructurarlos** al recibirlos. Go y Python lo hacen nativamente; otros usan tuplas, arreglos u objetos.",
    "resultados": ["Devolver varios valores de una función.", "Desestructurar el resultado en variables.", "Comparar tuplas, arreglos y objetos como vehículo."],
    "temas": [("Múltiples retornos", "Más de un valor de salida"), ("Tupla", "Agrupar valores sin nombre"), ("Desestructuración", "Repartir en variables"), ("Vehículos", "Tupla, arreglo, struct u objeto")],
    "definiciones": [("Múltiple retorno", "una función devuelve varios valores. Clave: nativo en Go, Python, Rust."), ("Tupla", "grupo ordenado de valores. Clave: el vehículo habitual del multi-retorno."), ("Desestructuración", "repartir una tupla/objeto en variables. Clave: `q, r = divmod(a, b)`."), ("Struct/objeto de salida", "en Java/C se devuelve un objeto con campos. Clave: alternativa al multi-retorno.")],
    "situacion": "`divmod(17, 5)` devuelve cociente 3 y resto 2 de una vez. Sin multi-retorno habría que llamar dos veces o crear un objeto solo para eso.",
    "entrada": "una línea `a b` (enteros positivos, b != 0)",
    "salida": "`cociente=<a/b> resto=<a%b>`",
    "formula": "(cociente, resto) = (a/b, a%b)",
    "algoritmo": "FUNCION divmod(a,b): DEVOLVER (a/b, a%b)\nLEER a,b ; (q,r) <- divmod(a,b) ; ESCRIBIR q, r",
    "casos": [("17 5", "cociente=3 resto=2"), ("10 2", "cociente=5 resto=0"), ("7 3", "cociente=2 resto=1")],
    "comparacion": [("Sintáctica", "`q, r = ...` (Python/Go/Rust) vs. objeto/arreglo (Java/JS)."), ("Semántica", "Go/Python devuelven varios valores; Java devuelve un objeto contenedor."), ("Paradigmática", "SQL devuelve varias columnas por fila, un multi-retorno natural.")],
    "familia": "En Ruby `return q, r` (una tupla). En Kotlin, un `Pair` o un `data class`.",
    "errores": [("Devolver un objeto solo para dos valores", "sobre-ingeniería en lenguajes con tuplas", "usar el multi-retorno nativo si existe"), ("Orden de la desestructuración", "asignar cociente al resto", "respetar el orden de los valores devueltos")],
    "faq": [("¿Tupla o struct?", "Tupla para pocos valores anónimos; struct/clase si quieren nombres y significado."), ("¿Java tiene multi-retorno?", "No nativo: se devuelve un objeto (record) con los campos.")],
    "reto": "Devuelve también el signo (`+`/`-`) del cociente y resuélvelo en **Go**.",
    "impls": {
        "python": r"""import sys


def divmod2(a, b):
    return a // b, a % b


a, b = map(int, sys.stdin.readline().split())
q, r = divmod2(a, b)
print(f"cociente={q} resto={r}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

function divmod(a, b) {
  return [Math.trunc(a / b), a % b];
}

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const [q, r] = divmod(a, b);
console.log(`cociente=${q} resto=${r}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

function divmod(a: number, b: number): [number, number] {
  return [Math.trunc(a / b), a % b];
}

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const [q, r]: [number, number] = divmod(a, b);
console.log(`cociente=${q} resto=${r}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // Java devuelve un objeto (record) para varios valores.
    record DivRes(int cociente, int resto) {}

    static DivRes divmod(int a, int b) {
        return new DivRes(a / b, a % b);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        DivRes d = divmod(Integer.parseInt(p[0]), Integer.parseInt(p[1]));
        System.out.println("cociente=" + d.cociente() + " resto=" + d.resto());
    }
}
""",
        "csharp": r"""using System;

(int, int) Divmod(int a, int b) => (a / b, a % b);

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var (q, r) = Divmod(int.Parse(p[0]), int.Parse(p[1]));
Console.WriteLine($"cociente={q} resto={r}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func divmod(a, b int) (int, int) {
	return a / b, a % b
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	q, r := divmod(a, b)
	fmt.Printf("cociente=%d resto=%d\n", q, r)
}
""",
        "rust": r"""use std::io::Read;

fn divmod(a: i64, b: i64) -> (i64, i64) {
    (a / b, a % b)
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let (q, r) = divmod(v[0], v[1]);
    println!("cociente={q} resto={r}");
}
""",
        "c": r"""#include <stdio.h>

/* C devuelve un valor; el segundo va por puntero. */
long divmod(long a, long b, long *resto) {
    *resto = a % b;
    return a / b;
}

int main(void) {
    long a, b, r;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    long q = divmod(a, b, &r);
    printf("cociente=%ld resto=%ld\n", q, r);
    return 0;
}
""",
        "php": r"""<?php
function divmod($a, $b) {
    return [intdiv($a, $b), $a % $b];
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
[$q, $r] = divmod((int) $a, (int) $b);
echo "cociente=$q resto=$r\n";
""",
        "sql": r"""-- SQL: varias columnas por fila son un multi-retorno natural.
WITH pares(a, b) AS (VALUES (17, 5), (10, 2), (7, 3))
SELECT printf('cociente=%d resto=%d', a / b, a % b) AS resultado FROM pares;
""",
    },
}

S[78] = {
    "descripcion": "Devolver el mayor de dos valores con una función genérica que sirve para cualquier tipo comparable.",
    "objetivo": "Escribir una función **genérica**: la misma lógica para varios tipos, sin duplicar código. `max<T>` funciona con enteros, reales o texto porque solo exige que el tipo sea comparable.",
    "resultados": ["Definir una función genérica con un parámetro de tipo.", "Explicar el polimorfismo paramétrico.", "Reconocer las restricciones (comparable) de los genéricos."],
    "temas": [("Genérico", "Un tipo como parámetro"), ("Polimorfismo paramétrico", "Misma lógica, varios tipos"), ("Restricciones", "El tipo debe cumplir algo (comparable)"), ("Sin duplicar", "Una función en vez de N")],
    "definiciones": [("Genérico", "función/tipo parametrizado por otro tipo (`max<T>`). Clave: reutilización con seguridad de tipos."), ("Polimorfismo paramétrico", "un código que funciona para muchos tipos. Clave: distinto del de herencia."), ("Restricción de tipo", "condición sobre el parámetro de tipo (comparable). Clave: habilita las operaciones."), ("Inferencia de tipo genérico", "el compilador deduce T al llamar. Clave: no hay que anotarlo.")],
    "situacion": "Sin genéricos habría un `maxInt`, un `maxDouble`, un `maxString`... Con `max<T: Comparable>` se escribe una vez y sirve para todos, sin perder la comprobación de tipos.",
    "entrada": "una línea `a b` (dos enteros)",
    "salida": "`max=<el mayor>`",
    "formula": "max<T>(a, b) = a si a>b, si no b",
    "algoritmo": "FUNCION max<T comparable>(a,b): DEVOLVER a SI a>b SINO b",
    "casos": [("3 7", "max=7"), ("9 2", "max=9"), ("5 5", "max=5")],
    "comparacion": [("Sintáctica", "`<T>` (Java/C#/Rust), `[T any]` (Go), sin anotación (Python dinámico)."), ("Semántica", "Estáticos comprueban T al compilar; Python confía en pato (duck typing)."), ("Paradigmática", "SQL usa `max()` polimórfico incorporado.")],
    "familia": "En Kotlin `fun <T: Comparable<T>> maxOf`. En Haskell la firma `Ord a => a -> a -> a` expresa la restricción.",
    "errores": [("Usar Object en vez de genéricos (Java viejo)", "perder la seguridad de tipos", "usar genéricos con restricción Comparable"), ("Olvidar la restricción comparable", "el tipo no soporta `>`", "acotar T a un tipo comparable")],
    "faq": [("¿Genéricos o sobrecarga?", "Genéricos evitan duplicar; sobrecarga es para comportamientos distintos por tipo."), ("¿Python tiene genéricos?", "Su tipado dinámico ya es 'genérico'; con anotaciones existen `TypeVar` para herramientas.")],
    "reto": "Haz `min` genérico y resuélvelo en **Rust** con `fn min<T: PartialOrd>`.",
    "impls": {
        "python": r"""import sys


def mayor(a, b):
    return a if a > b else b


a, b = map(int, sys.stdin.readline().split())
print(f"max={mayor(a, b)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

// JS es dinámico: la función ya sirve para cualquier tipo comparable.
function mayor(a, b) {
  return a > b ? a : b;
}

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`max=${mayor(a, b)}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

function mayor<T>(a: T, b: T): T {
  return a > b ? a : b;
}

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`max=${mayor(a, b)}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static <T extends Comparable<T>> T mayor(T a, T b) {
        return a.compareTo(b) > 0 ? a : b;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]);
        int b = Integer.parseInt(p[1]);
        System.out.println("max=" + mayor(a, b));
    }
}
""",
        "csharp": r"""using System;

T Mayor<T>(T a, T b) where T : IComparable<T> => a.CompareTo(b) > 0 ? a : b;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
Console.WriteLine($"max={Mayor(a, b)}");
""",
        "go": r"""package main

import (
	"bufio"
	"cmp"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func mayor[T cmp.Ordered](a, b T) T {
	if a > b {
		return a
	}
	return b
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	fmt.Printf("max=%d\n", mayor(a, b))
}
""",
        "rust": r"""use std::io::Read;

fn mayor<T: PartialOrd>(a: T, b: T) -> T {
    if a > b { a } else { b }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("max={}", mayor(v[0], v[1]));
}
""",
        "c": r"""#include <stdio.h>

/* C no tiene genéricos: se escribe una función por tipo (o macros). */
long mayor(long a, long b) {
    return a > b ? a : b;
}

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("max=%ld\n", mayor(a, b));
    return 0;
}
""",
        "php": r"""<?php
// PHP es dinámico: la función sirve para cualquier tipo comparable.
function mayor($a, $b) {
    return $a > $b ? $a : $b;
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "max=" . mayor((int) $a, (int) $b) . "\n";
""",
        "sql": r"""-- SQL: max() es polimórfico incorporado.
WITH pares(a, b) AS (VALUES (3, 7), (9, 2), (5, 5))
SELECT printf('max=%d', max(a, b)) AS resultado FROM pares;
""",
    },
}

S[79] = {
    "descripcion": "Mostrar que una función que recibe un entero por valor no modifica la variable original.",
    "objetivo": "Comprender el **paso por valor**: la función recibe una copia del argumento, así que modificar el parámetro dentro no afecta a la variable original de quien llama.",
    "resultados": ["Explicar el paso por valor con un ejemplo.", "Predecir que el original no cambia.", "Reconocer que los primitivos se pasan por valor."],
    "temas": [("Paso por valor", "Se pasa una copia"), ("Copia local", "Modificarla no afecta fuera"), ("Primitivos", "Suelen pasarse por valor"), ("Aislamiento", "La función no toca al llamador")],
    "definiciones": [("Paso por valor", "la función recibe una copia del argumento. Clave: el original no cambia."), ("Copia", "un duplicado independiente del valor. Clave: vive dentro de la función."), ("Parámetro local", "la variable de la función que contiene la copia. Clave: aislada del exterior."), ("Efecto en el llamador", "aquí, ninguno. Clave: la seguridad del paso por valor.")],
    "situacion": "Pasas `n` a una función que lo duplica dentro; al volver, `n` sigue igual. La función trabajó con una copia. Entender esto evita esperar cambios que nunca ocurren.",
    "entrada": "un entero `n`",
    "salida": "`original=<n> local=<2n>`",
    "formula": "la función duplica una copia; el original permanece",
    "algoritmo": "LEER n\nlocal <- doblar(n)   // dentro trabaja una copia\nESCRIBIR \"original=\" n \" local=\" local",
    "casos": [("5", "original=5 local=10"), ("3", "original=3 local=6"), ("0", "original=0 local=0")],
    "comparacion": [("Sintáctica", "Igual en todos: se llama y se recibe el retorno."), ("Semántica", "Los primitivos se copian; el original nunca se altera."), ("Paradigmática", "SQL no tiene variables mutables del llamador; todo es expresión.")],
    "familia": "En Ruby los enteros son inmutables: se comportan como paso por valor. En Java/Go/C, los primitivos siempre se pasan por valor.",
    "errores": [("Esperar que el original cambie", "creer que se pasó por referencia", "recordar que los primitivos se copian"), ("Modificar el parámetro creyendo que afecta fuera", "no ver el aislamiento", "devolver el nuevo valor si quieres usarlo")],
    "faq": [("¿Todo se pasa por valor?", "Los primitivos sí; los objetos, la referencia se pasa por valor (siguiente clase)."), ("¿Por qué es seguro?", "La función no puede alterar por sorpresa las variables del llamador.")],
    "reto": "Añade `triple=<3n>` calculado por otra función y resuélvelo en **C**.",
    "impls": {
        "python": r"""import sys


def doblar(x):
    x = x * 2  # modifica la copia local
    return x


n = int(sys.stdin.readline())
local = doblar(n)
print(f"original={n} local={local}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

function doblar(x) {
  x = x * 2;
  return x;
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const local = doblar(n);
console.log(`original=${n} local=${local}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

function doblar(x: number): number {
  x = x * 2;
  return x;
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const local: number = doblar(n);
console.log(`original=${n} local=${local}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static int doblar(int x) {
        x = x * 2;
        return x;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int local = doblar(n);
        System.out.println("original=" + n + " local=" + local);
    }
}
""",
        "csharp": r"""using System;

int Doblar(int x) {
    x = x * 2;
    return x;
}

int n = int.Parse(Console.In.ReadToEnd().Trim());
int local = Doblar(n);
Console.WriteLine($"original={n} local={local}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func doblar(x int) int {
	x = x * 2
	return x
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	local := doblar(n)
	fmt.Printf("original=%d local=%d\n", n, local)
}
""",
        "rust": r"""use std::io::Read;

fn doblar(mut x: i64) -> i64 {
    x *= 2;
    x
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let local = doblar(n);
    println!("original={n} local={local}");
}
""",
        "c": r"""#include <stdio.h>

long doblar(long x) {
    x = x * 2; /* modifica la copia local */
    return x;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long local = doblar(n);
    printf("original=%ld local=%ld\n", n, local);
    return 0;
}
""",
        "php": r"""<?php
function doblar($x) {
    $x = $x * 2;
    return $x;
}

$n = (int) trim(fgets(STDIN));
$local = doblar($n);
echo "original=$n local=$local\n";
""",
        "sql": r"""-- SQL: sin variables del llamador; la expresión produce el valor.
WITH nums(n) AS (VALUES (5), (3), (0))
SELECT printf('original=%d local=%d', n, n * 2) AS resultado FROM nums;
""",
    },
}

S[80] = {
    "descripcion": "Mostrar que una función que recibe una referencia sí modifica la variable original.",
    "objetivo": "Comprender el **paso por referencia**: la función recibe un enlace a la variable original, así que modificar el parámetro **sí** cambia la variable de quien llama. C usa punteros, Go `*`, Rust `&mut`, C# `ref`.",
    "resultados": ["Modificar una variable del llamador desde una función.", "Distinguir referencia de copia.", "Reconocer cómo cada lenguaje pasa referencias."],
    "temas": [("Paso por referencia", "Se pasa un enlace, no una copia"), ("Punteros/referencias", "&, *, ref, &mut"), ("Efecto en el llamador", "El original cambia"), ("Riesgo", "Modificaciones a distancia")],
    "definiciones": [("Paso por referencia", "la función accede a la variable original. Clave: puede modificarla."), ("Puntero", "valor que guarda la dirección de otra variable (C). Clave: permite modificarla."), ("Referencia mutable", "enlace que permite cambiar el valor (`&mut` en Rust, `ref` en C#). Clave: modificación explícita."), ("Efecto secundario", "cambiar algo fuera de la función. Clave: potente pero peligroso.")],
    "situacion": "Una función `doblar(&n)` cambia `n` para siempre. Es útil (evita copiar datos grandes) pero peligroso: modificaciones 'a distancia' que sorprenden si no se esperan.",
    "entrada": "un entero `n`",
    "salida": "`antes=<n> despues=<2n>`",
    "formula": "la función duplica la variable original vía referencia",
    "algoritmo": "LEER n ; antes <- n\ndoblar(referencia a n)   // modifica el original\nESCRIBIR \"antes=\" antes \" despues=\" n",
    "casos": [("5", "antes=5 despues=10"), ("3", "antes=3 despues=6"), ("7", "antes=7 despues=14")],
    "comparacion": [("Sintáctica", "`*p` (C/Go), `&mut` (Rust), `ref` (C#), objeto/lista (Java/JS/Python)."), ("Semántica", "Referencia mutable cambia el original; los primitivos por valor no."), ("Paradigmática", "SQL no modifica variables: usa UPDATE sobre datos.")],
    "familia": "En Ruby los objetos se pasan por referencia (de valor); los enteros no se mutan. En C++ hay referencias `&` explícitas.",
    "errores": [("Modificar sin querer el original", "efecto secundario inesperado", "pasar por valor si no debes cambiar el original"), ("Confundir puntero con valor", "modificar la copia del puntero", "desreferenciar (`*p`) para tocar el valor apuntado")],
    "faq": [("¿Referencia o valor?", "Referencia para modificar o evitar copiar datos grandes; valor para aislar."), ("¿Java pasa por referencia?", "Pasa la referencia por valor: puedes mutar el objeto, no reasignar la variable del llamador.")],
    "reto": "Haz una función que intercambie dos variables por referencia y resuélvelo en **C** con punteros.",
    "impls": {
        "python": r"""import sys


def doblar(caja):
    caja[0] *= 2  # modifica el contenido compartido


n = int(sys.stdin.readline())
antes = n
caja = [n]
doblar(caja)
print(f"antes={antes} despues={caja[0]}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

function doblar(caja) {
  caja.v *= 2;
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const antes = n;
const caja = { v: n };
doblar(caja);
console.log(`antes=${antes} despues=${caja.v}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

function doblar(caja: { v: number }): void {
  caja.v *= 2;
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const antes: number = n;
const caja = { v: n };
doblar(caja);
console.log(`antes=${antes} despues=${caja.v}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // Java pasa la referencia del arreglo: se puede mutar su contenido.
    static void doblar(int[] caja) {
        caja[0] *= 2;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int antes = n;
        int[] caja = { n };
        doblar(caja);
        System.out.println("antes=" + antes + " despues=" + caja[0]);
    }
}
""",
        "csharp": r"""using System;

void Doblar(ref int x) {
    x *= 2;
}

int n = int.Parse(Console.In.ReadToEnd().Trim());
int antes = n;
int v = n;
Doblar(ref v);
Console.WriteLine($"antes={antes} despues={v}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func doblar(p *int) {
	*p *= 2
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	antes := n
	doblar(&n)
	fmt.Printf("antes=%d despues=%d\n", antes, n)
}
""",
        "rust": r"""use std::io::Read;

fn doblar(x: &mut i64) {
    *x *= 2;
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut n: i64 = s.trim().parse().unwrap();
    let antes = n;
    doblar(&mut n);
    println!("antes={antes} despues={n}");
}
""",
        "c": r"""#include <stdio.h>

void doblar(long *p) {
    *p *= 2;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long antes = n;
    doblar(&n);
    printf("antes=%ld despues=%ld\n", antes, n);
    return 0;
}
""",
        "php": r"""<?php
function doblar(&$x) {
    $x *= 2;
}

$n = (int) trim(fgets(STDIN));
$antes = $n;
doblar($n);
echo "antes=$antes despues=$n\n";
""",
        "sql": r"""-- SQL no modifica variables; el 'despues' se calcula en la expresión.
WITH nums(n) AS (VALUES (5), (3), (7))
SELECT printf('antes=%d despues=%d', n, n * 2) AS resultado FROM nums;
""",
    },
}

S[81] = {
    "descripcion": "Medir la longitud de un texto y luego mostrarlo, ilustrando préstamo (borrow) y movimiento (move).",
    "objetivo": "Entender la **semántica de movimiento y préstamo** de Rust: un valor tiene un dueño; se puede **prestar** (borrow) para leerlo sin copiar, o **mover** (move) transfiriendo la propiedad. Otros lenguajes copian o comparten referencias con GC.",
    "resultados": ["Explicar propiedad, préstamo y movimiento.", "Leer un valor prestado sin copiarlo.", "Comparar el modelo de Rust con el de los lenguajes con GC."],
    "temas": [("Propiedad (ownership)", "Cada valor tiene un dueño"), ("Préstamo (borrow)", "Usar sin poseer"), ("Movimiento (move)", "Transferir la propiedad"), ("Alternativas", "Copia o GC en otros lenguajes")],
    "definiciones": [("Propiedad", "cada valor tiene un único dueño responsable de liberarlo. Clave: base de la seguridad de Rust."), ("Préstamo", "referencia temporal para leer/usar sin tomar la propiedad. Clave: `&valor`."), ("Movimiento", "transferir la propiedad a otra variable. Clave: la original deja de ser válida."), ("Copia vs. GC", "otros lenguajes copian o rastrean referencias con recolector. Clave: modelo distinto.")],
    "situacion": "En Rust, medir la longitud del texto lo **presta** (`&s`); luego imprimirlo lo **mueve**. El compilador garantiza que nadie use un valor movido. Otros lenguajes lo resuelven con GC o copiando.",
    "entrada": "una palabra (ASCII)",
    "salida": "`movido=<palabra> longitud=<len>`",
    "formula": "longitud por préstamo; el texto se muestra tras moverse",
    "algoritmo": "LEER w ; len <- longitud(prestar w)\nmostrar(mover w)\nESCRIBIR \"movido=\" w \" longitud=\" len",
    "casos": [("Ada", "movido=Ada longitud=3"), ("Bo", "movido=Bo longitud=2"), ("hola", "movido=hola longitud=4")],
    "comparacion": [("Sintáctica", "`&s` (préstamo) y move implícito en Rust; los demás copian o comparten referencia."), ("Semántica", "Rust invalida el valor movido en compilación; con GC el valor sigue vivo mientras se use."), ("Paradigmática", "SQL no tiene propiedad de memoria: opera sobre datos.")],
    "familia": "C++ tiene semántica de movimiento (`std::move`) y referencias, cercana a Rust pero sin comprobación en compilación. Java/Go/Python usan GC.",
    "errores": [("Usar un valor tras moverlo (Rust)", "el compilador lo rechaza", "prestar (`&`) si necesitas seguir usándolo"), ("Asumir move en lenguajes con GC", "allí no existe", "recordar que el GC mantiene el valor vivo mientras haya referencias")],
    "faq": [("¿Por qué Rust mueve?", "Para garantizar un único dueño y liberar memoria sin GC ni errores de uso tras liberar."), ("¿Prestar copia?", "No: un préstamo es una referencia; no duplica el dato.")],
    "reto": "Presta el texto a dos funciones distintas antes de moverlo y resuélvelo en **Rust**.",
    "impls": {
        "python": r"""import sys

s = sys.stdin.readline().strip()
longitud = len(s)  # Python comparte la referencia (GC), no hay 'move'.
print(f"movido={s} longitud={longitud}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const s = readFileSync(0, "utf8").trim();
const longitud = s.length; // JS usa GC: la cadena sigue disponible.
console.log(`movido=${s} longitud=${longitud}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const s: string = readFileSync(0, "utf8").trim();
const longitud: number = s.length;
console.log(`movido=${s} longitud=${longitud}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine().trim();
        int longitud = s.length(); // GC: sin propiedad ni move.
        System.out.println("movido=" + s + " longitud=" + longitud);
    }
}
""",
        "csharp": r"""using System;

string s = Console.In.ReadToEnd().Trim();
int longitud = s.Length; // GC: la cadena permanece.
Console.WriteLine($"movido={s} longitud={longitud}");
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
	s := strings.TrimSpace(line)
	longitud := len(s) // GC: sin propiedad explícita.
	fmt.Printf("movido=%s longitud=%d\n", s, longitud)
}
""",
        "rust": r"""use std::io::Read;

fn longitud(s: &str) -> usize {
    s.len() // préstamo: se lee sin tomar la propiedad
}

fn mostrar(s: String) {
    // move: 'mostrar' se vuelve dueña de la cadena
    let len = s.len();
    println!("movido={s} longitud={len}");
}

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).unwrap();
    let s = buf.trim().to_string();
    let _ = longitud(&s); // se presta
    mostrar(s); // se mueve
}
""",
        "c": r"""#include <stdio.h>
#include <string.h>

int main(void) {
    char s[256];
    if (scanf("%255s", s) != 1) return 1;
    /* C: gestión manual; aquí no se copia ni se mueve, se usa directamente. */
    int longitud = (int) strlen(s);
    printf("movido=%s longitud=%d\n", s, longitud);
    return 0;
}
""",
        "php": r"""<?php
$s = trim(fgets(STDIN));
$longitud = strlen($s); // PHP usa GC por conteo de referencias.
echo "movido=$s longitud=$longitud\n";
""",
        "sql": r"""-- SQL no tiene propiedad de memoria: opera sobre datos.
WITH palabras(s) AS (VALUES ('Ada'), ('Bo'), ('hola'))
SELECT printf('movido=%s longitud=%d', s, length(s)) AS resultado FROM palabras;
""",
    },
}

S[82] = {
    "descripcion": "Mostrar el sombreado (shadowing): una variable interna con el mismo nombre oculta a la externa dentro de su bloque.",
    "objetivo": "Comprender el **alcance (scope)** de las variables y el **sombreado (shadowing)**: dónde vive una variable y qué pasa cuando una interna reusa el nombre de una externa. Al salir del bloque, reaparece la externa.",
    "resultados": ["Explicar el alcance de bloque.", "Predecir el efecto del sombreado.", "Distinguir la variable interna de la externa."],
    "temas": [("Alcance (scope)", "Dónde es visible una variable"), ("Bloque", "La región que delimita el alcance"), ("Sombreado", "Reusar un nombre en un bloque interno"), ("Restauración", "Al salir, vuelve la externa")],
    "definiciones": [("Alcance", "región del código donde una variable es visible. Clave: de bloque en la mayoría."), ("Sombreado", "una variable interna con el mismo nombre oculta a la externa. Clave: dentro del bloque."), ("Bloque", "conjunto de sentencias con su propio alcance. Clave: `{ ... }`."), ("Vida de la variable", "cuánto existe. Clave: termina al salir de su alcance.")],
    "situacion": "Dentro de un bloque defines `x` con el mismo nombre que una `x` externa: dentro vale lo interno, fuera vuelve lo externo. No entenderlo lleva a 'por qué mi variable no cambió'.",
    "entrada": "un entero `n`",
    "salida": "`interno=<n+10> externo=<n>`",
    "formula": "externo x = n; en un bloque interno x = n+10; al salir, x = n",
    "algoritmo": "LEER n ; x <- n\nBLOQUE: x_interno <- x + 10 ; imprimir interno\nimprimir externo (x sigue siendo n)",
    "casos": [("5", "interno=15 externo=5"), ("0", "interno=10 externo=0"), ("-3", "interno=7 externo=-3")],
    "comparacion": [("Sintáctica", "Bloques `{ }` (C/Java/JS/Rust) vs. indentación (Python)."), ("Semántica", "Rust permite `let` que sombrea; Python no tiene alcance de bloque para `if`/`for`."), ("Paradigmática", "SQL usa alias/subconsultas para acotar nombres.")],
    "familia": "En Kotlin y Rust el sombreado con `val`/`let` es idiomático. En Python las variables de un `if` no crean un nuevo alcance.",
    "errores": [("Creer que la interna cambió la externa", "confundir sombreado con reasignación", "recordar que la interna es otra variable en su bloque"), ("Usar una variable fuera de su alcance", "error de 'no definida'", "declararla en el alcance donde la necesitas")],
    "faq": [("¿Sombrear es mala práctica?", "Puede confundir, pero en Rust/Kotlin es idiomático para transformar un valor manteniendo el nombre."), ("¿Python tiene alcance de bloque?", "No para if/for; sí para funciones. Las variables 'se escapan' del bloque.")],
    "reto": "Añade un segundo nivel de bloque que sombree otra vez y resuélvelo en **Rust**.",
    "impls": {
        "python": r"""import sys

n = int(sys.stdin.readline())
x = n
# Python no crea alcance de bloque: se usa otra variable para el 'interno'.
x_interno = x + 10
print(f"interno={x_interno} externo={x}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const x = n;
{
  const x = n + 10; // sombrea a la externa dentro del bloque
  console.log(`interno=${x} externo=${n}`);
}
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const x: number = n;
{
  const x: number = n + 10;
  console.log(`interno=${x} externo=${n}`);
}
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int x = n;
        {
            int xInterno = x + 10; // Java no permite re-declarar x en el bloque
            System.out.println("interno=" + xInterno + " externo=" + x);
        }
    }
}
""",
        "csharp": r"""using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int x = n;
{
    int xInterno = x + 10;
    Console.WriteLine($"interno={xInterno} externo={x}");
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
	x := n
	{
		x := n + 10 // sombrea a la externa en este bloque
		fmt.Printf("interno=%d externo=%d\n", x, n)
	}
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let x = n;
    {
        let x = n + 10; // sombreado idiomático en Rust
        println!("interno={x} externo={n}");
    }
    let _ = x;
}
""",
        "c": r"""#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long x = n;
    {
        long x = n + 10; /* sombrea a la externa dentro del bloque */
        printf("interno=%ld externo=%ld\n", x, n);
    }
    return 0;
}
""",
        "php": r"""<?php
$n = (int) trim(fgets(STDIN));
$x = $n;
// PHP no tiene alcance de bloque: se usa otra variable.
$xInterno = $x + 10;
echo "interno=$xInterno externo=$x\n";
""",
        "sql": r"""-- SQL usa alias/subconsultas para acotar nombres.
WITH nums(n) AS (VALUES (5), (0), (-3))
SELECT printf('interno=%d externo=%d', n + 10, n) AS resultado FROM nums;
""",
    },
}

S[83] = {
    "descripcion": "Crear una función que devuelve otra función (un cierre) que recuerda un valor base, y usarla dos veces.",
    "objetivo": "Entender los **cierres (closures)**: funciones que capturan y recuerdan variables de su entorno. Un `sumador(base)` devuelve una función que suma `base` a lo que reciba, recordándolo entre llamadas.",
    "resultados": ["Crear un cierre que captura una variable.", "Reusar el cierre en varias llamadas.", "Explicar qué significa 'capturar el entorno'."],
    "temas": [("Cierre (closure)", "Función que recuerda su entorno"), ("Captura", "Recordar variables externas"), ("Función que devuelve función", "Fábricas de funciones"), ("Estado encapsulado", "El valor capturado persiste")],
    "definiciones": [("Cierre", "función que captura variables de su entorno de definición. Clave: las recuerda al ejecutarse después."), ("Captura", "recordar una variable externa dentro del cierre. Clave: por valor o por referencia."), ("Función de orden superior", "la que devuelve o recibe funciones. Clave: fábrica de cierres."), ("Estado capturado", "el valor que el cierre conserva. Clave: como una variable privada.")],
    "situacion": "`hacer_sumador(10)` devuelve una función que siempre suma 10. Llamarla con 1 da 11; con 2, 12. El cierre 'recuerda' el 10 sin que se lo vuelvas a pasar.",
    "entrada": "un entero `base`",
    "salida": "`r1=<base+1> r2=<base+2>`",
    "formula": "sumar = λx. base + x ; r1 = sumar(1) ; r2 = sumar(2)",
    "algoritmo": "LEER base\nsumar <- hacer_sumador(base)   // captura base\nESCRIBIR \"r1=\" sumar(1) \" r2=\" sumar(2)",
    "casos": [("10", "r1=11 r2=12"), ("0", "r1=1 r2=2"), ("100", "r1=101 r2=102")],
    "comparacion": [("Sintáctica", "`lambda`/`=>`/`|x|` para el cierre; C usa un puntero a función + parámetro."), ("Semántica", "La mayoría captura el entorno; C no tiene cierres (se pasa el dato aparte)."), ("Paradigmática", "SQL no tiene cierres; se parametriza con valores en la consulta.")],
    "familia": "En Ruby los bloques y `lambda` capturan el entorno. En Haskell, la aplicación parcial produce cierres de forma natural.",
    "errores": [("Capturar por referencia sin querer", "el cierre ve cambios posteriores de la variable", "capturar por valor si necesitas fijar el estado"), ("Esperar cierres en C", "no existen", "pasar el estado como parámetro explícito")],
    "faq": [("¿Cierre o clase?", "Un cierre es como un objeto con un solo método y estado privado; a veces más ligero."), ("¿Qué captura, el valor o la variable?", "Depende del lenguaje: por valor (copia) o por referencia (enlace vivo).")],
    "reto": "Haz un cierre contador que aumente en cada llamada y resuélvelo en **JavaScript**.",
    "impls": {
        "python": r"""import sys


def hacer_sumador(base):
    def sumar(x):
        return base + x
    return sumar


base = int(sys.stdin.readline())
sumar = hacer_sumador(base)
print(f"r1={sumar(1)} r2={sumar(2)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

function hacerSumador(base) {
  return (x) => base + x;
}

const base = parseInt(readFileSync(0, "utf8").trim(), 10);
const sumar = hacerSumador(base);
console.log(`r1=${sumar(1)} r2=${sumar(2)}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

function hacerSumador(base: number): (x: number) => number {
  return (x) => base + x;
}

const base: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const sumar = hacerSumador(base);
console.log(`r1=${sumar(1)} r2=${sumar(2)}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.function.IntUnaryOperator;

public class Main {
    static IntUnaryOperator hacerSumador(int base) {
        return x -> base + x; // captura base (efectivamente final)
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int base = Integer.parseInt(br.readLine().trim());
        IntUnaryOperator sumar = hacerSumador(base);
        System.out.println("r1=" + sumar.applyAsInt(1) + " r2=" + sumar.applyAsInt(2));
    }
}
""",
        "csharp": r"""using System;

Func<int, int> HacerSumador(int baseN) => x => baseN + x;

int b = int.Parse(Console.In.ReadToEnd().Trim());
var sumar = HacerSumador(b);
Console.WriteLine($"r1={sumar(1)} r2={sumar(2)}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func hacerSumador(base int) func(int) int {
	return func(x int) int {
		return base + x
	}
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	base, _ := strconv.Atoi(strings.TrimSpace(line))
	sumar := hacerSumador(base)
	fmt.Printf("r1=%d r2=%d\n", sumar(1), sumar(2))
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let base: i64 = s.trim().parse().unwrap();
    let sumar = |x: i64| base + x; // captura base
    println!("r1={} r2={}", sumar(1), sumar(2));
}
""",
        "c": r"""#include <stdio.h>

/* C no tiene cierres: el estado (base) se pasa como parámetro. */
long sumar(long base, long x) {
    return base + x;
}

int main(void) {
    long base;
    if (scanf("%ld", &base) != 1) return 1;
    printf("r1=%ld r2=%ld\n", sumar(base, 1), sumar(base, 2));
    return 0;
}
""",
        "php": r"""<?php
function hacerSumador($base) {
    return fn($x) => $base + $x;
}

$base = (int) trim(fgets(STDIN));
$sumar = hacerSumador($base);
echo "r1=" . $sumar(1) . " r2=" . $sumar(2) . "\n";
""",
        "sql": r"""-- SQL no tiene cierres: se parametriza con valores en la consulta.
WITH bases(base) AS (VALUES (10), (0), (100))
SELECT printf('r1=%d r2=%d', base + 1, base + 2) AS resultado FROM bases;
""",
    },
}

S[84] = {
    "descripcion": "Elevar un número al cuadrado con una función pura (sin efectos secundarios).",
    "objetivo": "Distinguir una **función pura** —su resultado depende solo de sus argumentos y no cambia nada externo— de una con **efectos secundarios**. Las puras son predecibles, testeables y seguras de paralelizar.",
    "resultados": ["Definir una función pura.", "Explicar qué es un efecto secundario.", "Argumentar las ventajas de la pureza."],
    "temas": [("Función pura", "Mismo entrada → mismo resultado"), ("Efecto secundario", "Cambiar algo externo"), ("Transparencia referencial", "Sustituir la llamada por su valor"), ("Ventajas", "Testeable, cacheable, paralelizable")],
    "definiciones": [("Función pura", "su salida depende solo de sus entradas y no causa efectos externos. Clave: predecible."), ("Efecto secundario", "modificar estado externo, imprimir, leer archivos. Clave: rompe la pureza."), ("Transparencia referencial", "poder reemplazar la llamada por su resultado. Clave: propiedad de las puras."), ("Determinismo", "misma entrada, misma salida siempre. Clave: facilita las pruebas.")],
    "situacion": "`cuadrado(n)` siempre da lo mismo para el mismo `n` y no toca nada más: es pura. Una función que además escribe en un log tiene un efecto secundario. Las puras son las más fáciles de probar y razonar.",
    "entrada": "un entero `n`",
    "salida": "`puro=<n²>`",
    "formula": "cuadrado(n) = n * n (sin efectos)",
    "algoritmo": "FUNCION cuadrado(n): DEVOLVER n*n   // sin tocar nada externo\nLEER n ; ESCRIBIR \"puro=\" cuadrado(n)",
    "casos": [("4", "puro=16"), ("-3", "puro=9"), ("0", "puro=0")],
    "comparacion": [("Sintáctica", "Idéntica en todos: una función que devuelve un cálculo."), ("Semántica", "La pureza es una propiedad del diseño, no de la sintaxis."), ("Paradigmática", "SQL (declarativo) y Haskell (puro) empujan hacia la pureza por defecto.")],
    "familia": "En Haskell casi todo es puro; los efectos se aíslan con el tipo IO. En Rust, la pureza es una convención, no forzada.",
    "errores": [("Mezclar cálculo con impresión/estado", "función difícil de testear", "separar el cálculo puro del efecto (I/O)"), ("Depender de estado global", "resultados no reproducibles", "pasar todo por parámetros")],
    "faq": [("¿Todo debe ser puro?", "No: los efectos son necesarios (I/O). La idea es aislarlos y mantener puro el núcleo."), ("¿Por qué importan las puras?", "Se prueban fácil, se cachean (memoización) y se pueden paralelizar sin riesgo.")],
    "reto": "Escribe una función pura `cubo` y compón `cubo(cuadrado(n))`; resuélvelo en **Haskell** o **Python**.",
    "impls": {
        "python": r"""import sys


def cuadrado(n):
    return n * n  # pura: sin efectos secundarios


n = int(sys.stdin.readline())
print(f"puro={cuadrado(n)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

function cuadrado(n) {
  return n * n;
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`puro=${cuadrado(n)}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

function cuadrado(n: number): number {
  return n * n;
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`puro=${cuadrado(n)}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static long cuadrado(long n) {
        return n * n;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        System.out.println("puro=" + cuadrado(n));
    }
}
""",
        "csharp": r"""using System;

long Cuadrado(long n) => n * n;

long n = long.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"puro={Cuadrado(n)}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func cuadrado(n int64) int64 {
	return n * n
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	fmt.Printf("puro=%d\n", cuadrado(n))
}
""",
        "rust": r"""use std::io::Read;

fn cuadrado(n: i64) -> i64 {
    n * n
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("puro={}", cuadrado(n));
}
""",
        "c": r"""#include <stdio.h>

long cuadrado(long n) {
    return n * n;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("puro=%ld\n", cuadrado(n));
    return 0;
}
""",
        "php": r"""<?php
function cuadrado($n) {
    return $n * $n;
}

$n = (int) trim(fgets(STDIN));
echo "puro=" . cuadrado($n) . "\n";
""",
        "sql": r"""-- SQL (declarativo) favorece expresiones puras.
WITH nums(n) AS (VALUES (4), (-3), (0))
SELECT printf('puro=%d', n * n) AS resultado FROM nums;
""",
    },
}

S[85] = {
    "descripcion": "Aplicar dos operaciones (suma y producto) pasándolas como argumentos a una función que las ejecuta.",
    "objetivo": "Tratar las funciones como **valores de primera clase**: guardarlas en variables y pasarlas como argumentos. `aplicar(suma, a, b)` ejecuta la función recibida; es la base de map/filter/reduce y de los callbacks.",
    "resultados": ["Pasar una función como argumento.", "Guardar una función en una variable.", "Explicar 'valor de primera clase'."],
    "temas": [("Primera clase", "Las funciones son valores"), ("Pasar funciones", "Como cualquier argumento"), ("Función de orden superior", "Recibe otra función"), ("Callbacks", "El patrón detrás de eventos")],
    "definiciones": [("Valor de primera clase", "algo que se puede guardar, pasar y devolver. Clave: las funciones lo son en casi todos los lenguajes."), ("Función de orden superior", "recibe o devuelve funciones. Clave: `aplicar(f, a, b)`."), ("Callback", "función pasada para ejecutarse después. Clave: base de eventos y asincronía."), ("Puntero a función", "en C, un valor que apunta a una función. Clave: su forma de primera clase.")],
    "situacion": "`aplicar(suma, 3, 4)` da 7 y `aplicar(producto, 3, 4)` da 12, usando la misma función `aplicar`. Poder pasar la operación como dato es lo que hace posibles map, filter y los callbacks.",
    "entrada": "una línea `a b` (dos enteros)",
    "salida": "`suma=<a+b> producto=<a*b>`",
    "formula": "aplicar(f, a, b) = f(a, b); con f = suma y f = producto",
    "algoritmo": "FUNCION aplicar(f, a, b): DEVOLVER f(a, b)\nESCRIBIR \"suma=\" aplicar(suma,a,b) \" producto=\" aplicar(producto,a,b)",
    "casos": [("3 4", "suma=7 producto=12"), ("5 5", "suma=10 producto=25"), ("0 9", "suma=9 producto=0")],
    "comparacion": [("Sintáctica", "Pasar `suma` directamente (Python/JS/Go/Rust) vs. puntero a función (C) o interfaz funcional (Java)."), ("Semántica", "La función es un valor; se invoca con `f(a, b)`."), ("Paradigmática", "SQL no pasa funciones; usa operadores/funciones incorporadas.")],
    "familia": "En Ruby se pasan `Proc`/bloques o `method(:suma)`. En Haskell pasar funciones es lo más natural del lenguaje.",
    "errores": [("Llamar la función en vez de pasarla", "pasar `suma(a,b)` en lugar de `suma`", "pasar el nombre sin paréntesis"), ("Firmas incompatibles", "la de orden superior espera otra forma", "asegurar que la función pasada encaja con lo esperado")],
    "faq": [("¿Callbacks son esto?", "Sí: un callback es una función que pasas para que se ejecute más tarde."), ("¿C tiene funciones de primera clase?", "Parcialmente: con punteros a función, aunque sin cierres.")],
    "reto": "Añade una operación `resta` y aplícala también; resuélvelo en **Go** pasando funciones.",
    "impls": {
        "python": r"""import sys


def suma(a, b):
    return a + b


def producto(a, b):
    return a * b


def aplicar(f, a, b):
    return f(a, b)


a, b = map(int, sys.stdin.readline().split())
print(f"suma={aplicar(suma, a, b)} producto={aplicar(producto, a, b)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const suma = (a, b) => a + b;
const producto = (a, b) => a * b;
const aplicar = (f, a, b) => f(a, b);

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${aplicar(suma, a, b)} producto=${aplicar(producto, a, b)}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

type Op = (a: number, b: number) => number;
const suma: Op = (a, b) => a + b;
const producto: Op = (a, b) => a * b;
const aplicar = (f: Op, a: number, b: number): number => f(a, b);

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${aplicar(suma, a, b)} producto=${aplicar(producto, a, b)}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.function.IntBinaryOperator;

public class Main {
    static int aplicar(IntBinaryOperator f, int a, int b) {
        return f.applyAsInt(a, b);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]);
        int b = Integer.parseInt(p[1]);
        IntBinaryOperator suma = (x, y) -> x + y;
        IntBinaryOperator producto = (x, y) -> x * y;
        System.out.println("suma=" + aplicar(suma, a, b) + " producto=" + aplicar(producto, a, b));
    }
}
""",
        "csharp": r"""using System;

int Aplicar(Func<int, int, int> f, int a, int b) => f(a, b);

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
Func<int, int, int> suma = (x, y) => x + y;
Func<int, int, int> producto = (x, y) => x * y;
Console.WriteLine($"suma={Aplicar(suma, a, b)} producto={Aplicar(producto, a, b)}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func suma(a, b int) int     { return a + b }
func producto(a, b int) int { return a * b }

func aplicar(f func(int, int) int, a, b int) int {
	return f(a, b)
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	fields := strings.Fields(line)
	a, _ := strconv.Atoi(fields[0])
	b, _ := strconv.Atoi(fields[1])
	fmt.Printf("suma=%d producto=%d\n", aplicar(suma, a, b), aplicar(producto, a, b))
}
""",
        "rust": r"""use std::io::Read;

fn suma(a: i64, b: i64) -> i64 {
    a + b
}

fn producto(a: i64, b: i64) -> i64 {
    a * b
}

fn aplicar(f: fn(i64, i64) -> i64, a: i64, b: i64) -> i64 {
    f(a, b)
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("suma={} producto={}", aplicar(suma, v[0], v[1]), aplicar(producto, v[0], v[1]));
}
""",
        "c": r"""#include <stdio.h>

long suma(long a, long b) { return a + b; }
long producto(long a, long b) { return a * b; }

long aplicar(long (*f)(long, long), long a, long b) {
    return f(a, b);
}

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("suma=%ld producto=%ld\n", aplicar(suma, a, b), aplicar(producto, a, b));
    return 0;
}
""",
        "php": r"""<?php
$suma = fn($a, $b) => $a + $b;
$producto = fn($a, $b) => $a * $b;
function aplicar($f, $a, $b) {
    return $f($a, $b);
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;
echo "suma=" . aplicar($suma, $a, $b) . " producto=" . aplicar($producto, $a, $b) . "\n";
""",
        "sql": r"""-- SQL usa operadores/funciones incorporadas, no funciones como valor.
WITH pares(a, b) AS (VALUES (3, 4), (5, 5), (0, 9))
SELECT printf('suma=%d producto=%d', a + b, a * b) AS resultado FROM pares;
""",
    },
}

S[86] = {
    "descripcion": "Usar una función 'doble' definida en un módulo/espacio de nombres separado.",
    "objetivo": "Organizar el código en **módulos** (o paquetes/espacios de nombres): agrupar funciones relacionadas y usarlas con un prefijo o importándolas. Es lo que evita que un proyecto grande sea un solo archivo caótico.",
    "resultados": ["Agrupar funciones en un módulo/espacio de nombres.", "Invocar una función de otro módulo.", "Reconocer import/require/use por lenguaje."],
    "temas": [("Módulo", "Agrupa código relacionado"), ("Espacio de nombres", "Evita choques de nombres"), ("Importar", "Traer lo que se necesita"), ("Organización", "Un proyecto no es un solo archivo")],
    "definiciones": [("Módulo", "unidad que agrupa funciones/tipos relacionados. Clave: organización y reutilización."), ("Espacio de nombres", "prefijo que evita colisiones de nombres. Clave: `math.sqrt` vs. `otro.sqrt`."), ("Importar", "traer un módulo al alcance actual (import/require/use). Clave: acceder a su contenido."), ("Encapsulación de módulo", "exponer solo lo público. Clave: oculta detalles internos.")],
    "situacion": "En un proyecto real, las utilidades matemáticas viven en un módulo, las de red en otro. Se importan donde hacen falta. Aquí, una función `doble` en un espacio propio se usa desde el principal.",
    "entrada": "un entero `n`",
    "salida": "`resultado=<2n>`",
    "formula": "modulo.doble(n) = 2n",
    "algoritmo": "IMPORTAR modulo\nLEER n ; ESCRIBIR \"resultado=\" modulo.doble(n)",
    "casos": [("5", "resultado=10"), ("0", "resultado=0"), ("-4", "resultado=-8")],
    "comparacion": [("Sintáctica", "`import`/`from` (Python), `require`/`import` (JS), `use` (Rust), `package` (Go/Java)."), ("Semántica", "El módulo define un espacio de nombres; se accede con prefijo o importando nombres."), ("Paradigmática", "SQL organiza en esquemas (schemas), análogos a espacios de nombres.")],
    "familia": "En Ruby, módulos con `module M; def self.doble`. En C, la 'modularidad' es por archivos .h/.c y enlace.",
    "errores": [("Meter todo en un archivo", "proyecto inmantenible", "separar por módulos con responsabilidad clara"), ("Importar de más (namespace pollution)", "colisiones y confusión", "importar solo lo necesario o usar el prefijo del módulo")],
    "faq": [("¿Módulo, paquete o namespace?", "Términos cercanos: agrupar y nombrar código. Cada lenguaje usa su palabra."), ("¿Por qué prefijos?", "Para que dos módulos puedan tener funciones con el mismo nombre sin chocar.")],
    "reto": "Añade una función `triple` al mismo módulo y úsala; resuélvelo en **Python** con un módulo aparte.",
    "impls": {
        "python": r"""import sys


class matematicas:  # actúa como un espacio de nombres
    @staticmethod
    def doble(n):
        return 2 * n


n = int(sys.stdin.readline())
print(f"resultado={matematicas.doble(n)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

// Objeto usado como módulo/espacio de nombres.
const matematicas = {
  doble: (n) => 2 * n,
};

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${matematicas.doble(n)}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

namespace matematicas {
  export function doble(n: number): number {
    return 2 * n;
  }
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${matematicas.doble(n)}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // Clase de utilidades como espacio de nombres.
    static class Matematicas {
        static int doble(int n) {
            return 2 * n;
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        System.out.println("resultado=" + Matematicas.doble(n));
    }
}
""",
        "csharp": r"""using System;

static class Matematicas {
    public static int Doble(int n) => 2 * n;
}

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"resultado={Matematicas.Doble(n)}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// En un proyecto real 'doble' viviría en otro paquete; aquí simula el módulo.
func doble(n int) int {
	return 2 * n
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	fmt.Printf("resultado=%d\n", doble(n))
}
""",
        "rust": r"""use std::io::Read;

mod matematicas {
    pub fn doble(n: i64) -> i64 {
        2 * n
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("resultado={}", matematicas::doble(n));
}
""",
        "c": r"""#include <stdio.h>

/* En C la modularidad se hace por archivos .h/.c; aquí una función local. */
long doble(long n) {
    return 2 * n;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("resultado=%ld\n", doble(n));
    return 0;
}
""",
        "php": r"""<?php
// PHP usa namespaces; aquí una función que actúa como utilidad del módulo.
function matematicas_doble($n) {
    return 2 * $n;
}

$n = (int) trim(fgets(STDIN));
echo "resultado=" . matematicas_doble($n) . "\n";
""",
        "sql": r"""-- SQL organiza en esquemas (schemas); la operación va en la consulta.
WITH nums(n) AS (VALUES (5), (0), (-4))
SELECT printf('resultado=%d', 2 * n) AS resultado FROM nums;
""",
    },
}

S[87] = {
    "descripcion": "Modelar una cuenta con saldo privado y un método depositar; hacer dos depósitos y consultar el saldo.",
    "objetivo": "Aplicar **encapsulación**: ocultar el estado interno (el saldo) y exponer solo operaciones controladas (depositar, consultar). El contrato público protege los datos de modificaciones inválidas.",
    "resultados": ["Ocultar un campo con visibilidad privada.", "Exponer métodos públicos como contrato.", "Explicar por qué la encapsulación protege los datos."],
    "temas": [("Encapsulación", "Ocultar el estado interno"), ("Visibilidad", "public vs. private"), ("Contrato público", "Lo que se puede usar"), ("Invariantes", "Reglas que el objeto mantiene")],
    "definiciones": [("Encapsulación", "agrupar datos y operaciones ocultando el estado interno. Clave: se accede solo por métodos."), ("Privado", "accesible solo desde dentro del tipo. Clave: protege el estado."), ("Público", "parte visible desde fuera (el contrato). Clave: lo que otros usan."), ("Invariante", "regla que el objeto siempre cumple (saldo >= 0). Clave: la encapsulación la protege.")],
    "situacion": "Si el saldo fuera público, cualquiera podría ponerlo en negativo saltándose las reglas. Encapsulado, solo `depositar`/`retirar` lo tocan, garantizando que siempre sea válido.",
    "entrada": "un entero `n` (monto de cada depósito)",
    "salida": "`saldo=<2n>` (tras depositar n dos veces)",
    "formula": "cuenta.depositar(n) dos veces; saldo = 2n",
    "algoritmo": "LEER n\ncuenta <- nueva Cuenta()\ncuenta.depositar(n) ; cuenta.depositar(n)\nESCRIBIR \"saldo=\" cuenta.saldo()",
    "casos": [("50", "saldo=100"), ("0", "saldo=0"), ("30", "saldo=60")],
    "comparacion": [("Sintáctica", "`private`/`public` (Java/C#), `_` por convención (Python), campos en minúscula (Go = privado del paquete)."), ("Semántica", "Java/C#/Rust hacen cumplir la privacidad; Python confía en la convención."), ("Paradigmática", "SQL encapsula con vistas y permisos.")],
    "familia": "En Ruby los atributos son privados y se exponen con `attr_reader`/métodos. En Go, la mayúscula/minúscula del nombre define la visibilidad.",
    "errores": [("Exponer el estado directamente", "cualquiera lo corrompe", "hacerlo privado y ofrecer métodos"), ("Getters/setters para todo sin criterio", "encapsulación de fachada", "exponer operaciones con significado, no acceso crudo")],
    "faq": [("¿Python encapsula de verdad?", "Por convención (`_priv`); no lo impide, pero la comunidad lo respeta."), ("¿Encapsular es solo getters/setters?", "No: es exponer operaciones con significado que mantienen los invariantes.")],
    "reto": "Añade `retirar` que no permita saldo negativo y resuélvelo en **Java**.",
    "impls": {
        "python": r"""import sys


class Cuenta:
    def __init__(self):
        self._saldo = 0  # privado por convención

    def depositar(self, monto):
        self._saldo += monto

    def saldo(self):
        return self._saldo


n = int(sys.stdin.readline())
c = Cuenta()
c.depositar(n)
c.depositar(n)
print(f"saldo={c.saldo()}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

class Cuenta {
  #saldo = 0; // campo privado real
  depositar(monto) {
    this.#saldo += monto;
  }
  saldo() {
    return this.#saldo;
  }
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const c = new Cuenta();
c.depositar(n);
c.depositar(n);
console.log(`saldo=${c.saldo()}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

class Cuenta {
  private saldoInterno = 0;
  depositar(monto: number): void {
    this.saldoInterno += monto;
  }
  saldo(): number {
    return this.saldoInterno;
  }
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const c = new Cuenta();
c.depositar(n);
c.depositar(n);
console.log(`saldo=${c.saldo()}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static class Cuenta {
        private long saldo = 0;

        void depositar(long monto) {
            saldo += monto;
        }

        long saldo() {
            return saldo;
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        Cuenta c = new Cuenta();
        c.depositar(n);
        c.depositar(n);
        System.out.println("saldo=" + c.saldo());
    }
}
""",
        "csharp": r"""using System;

class Cuenta {
    private long saldo = 0;
    public void Depositar(long monto) => saldo += monto;
    public long Saldo() => saldo;
}

long n = long.Parse(Console.In.ReadToEnd().Trim());
var c = new Cuenta();
c.Depositar(n);
c.Depositar(n);
Console.WriteLine($"saldo={c.Saldo()}");
""",
        "go": r"""package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// saldo en minúscula: privado del paquete.
type cuenta struct {
	saldo int64
}

func (c *cuenta) depositar(monto int64) {
	c.saldo += monto
}

func (c *cuenta) obtenerSaldo() int64 {
	return c.saldo
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	c := &cuenta{}
	c.depositar(n)
	c.depositar(n)
	fmt.Printf("saldo=%d\n", c.obtenerSaldo())
}
""",
        "rust": r"""use std::io::Read;

struct Cuenta {
    saldo: i64, // privado fuera del módulo
}

impl Cuenta {
    fn nueva() -> Self {
        Cuenta { saldo: 0 }
    }
    fn depositar(&mut self, monto: i64) {
        self.saldo += monto;
    }
    fn saldo(&self) -> i64 {
        self.saldo
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut c = Cuenta::nueva();
    c.depositar(n);
    c.depositar(n);
    println!("saldo={}", c.saldo());
}
""",
        "c": r"""#include <stdio.h>

/* C no tiene 'private'; se usa una struct y funciones por convención. */
struct Cuenta {
    long saldo;
};

void depositar(struct Cuenta *c, long monto) {
    c->saldo += monto;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    struct Cuenta c = {0};
    depositar(&c, n);
    depositar(&c, n);
    printf("saldo=%ld\n", c.saldo);
    return 0;
}
""",
        "php": r"""<?php
class Cuenta {
    private $saldo = 0;

    public function depositar($monto) {
        $this->saldo += $monto;
    }

    public function saldo() {
        return $this->saldo;
    }
}

$n = (int) trim(fgets(STDIN));
$c = new Cuenta();
$c->depositar($n);
$c->depositar($n);
echo "saldo=" . $c->saldo() . "\n";
""",
        "sql": r"""-- SQL encapsula con vistas/permisos; aquí el cálculo va en la consulta.
WITH montos(n) AS (VALUES (50), (0), (30))
SELECT printf('saldo=%d', n * 2) AS resultado FROM montos;
""",
    },
}

S[88] = {
    "descripcion": "Calcular el valor absoluto de un entero usando la función correspondiente de la biblioteca estándar.",
    "objetivo": "Cerrar la parte usando la **biblioteca estándar**: importar y usar funciones ya provistas por el lenguaje (aquí, valor absoluto). Organizar un proyecto también es saber qué reutilizar en vez de reescribir.",
    "resultados": ["Importar una función de la biblioteca estándar.", "Reconocer qué ya viene resuelto.", "Explicar import/include/use en cada lenguaje."],
    "temas": [("Biblioteca estándar", "Lo que trae el lenguaje"), ("Importar", "Traer una función incorporada"), ("No reinventar", "Reutilizar lo que existe"), ("Organizar el proyecto", "Estructura e imports")],
    "definiciones": [("Biblioteca estándar", "conjunto de módulos incluidos con el lenguaje. Clave: funciones listas para usar."), ("Importar/incluir", "traer un módulo o cabecera (`import`, `#include`, `use`). Clave: acceder a sus funciones."), ("Valor absoluto", "distancia a cero, siempre no negativa. Clave: `abs(-5) = 5`."), ("Reutilización", "usar código existente en vez de reescribir. Clave: menos errores.")],
    "situacion": "El valor absoluto ya está en la biblioteca estándar de todos los lenguajes. Saber importarlo y usarlo, en vez de escribir tu propio `if x<0`, es parte de organizar bien un proyecto.",
    "entrada": "un entero `n`",
    "salida": "`abs=<|n|>`",
    "formula": "abs(n) = |n|",
    "algoritmo": "IMPORTAR abs de la biblioteca\nLEER n ; ESCRIBIR \"abs=\" abs(n)",
    "casos": [("-5", "abs=5"), ("3", "abs=3"), ("0", "abs=0")],
    "comparacion": [("Sintáctica", "`abs()` (Python built-in), `Math.abs` (JS/Java), `#include <stdlib.h>` (C), `n.abs()` (Rust)."), ("Semántica", "La función estándar maneja los casos; no hay que reimplementarla."), ("Paradigmática", "SQL usa `abs()` incorporado.")],
    "familia": "En Ruby `n.abs`. En Go `math.Abs` opera con float; para enteros se usa una función propia o un condicional.",
    "errores": [("Reimplementar lo que ya existe", "más código y más bugs", "buscar primero en la biblioteca estándar"), ("Olvidar el import/include", "función no encontrada", "importar el módulo correcto (math, stdlib)")],
    "faq": [("¿Siempre usar la estándar?", "Para lo común, sí: está probada y optimizada."), ("¿Go no tiene abs de enteros?", "`math.Abs` es para float; para int se usa un condicional o una función propia.")],
    "reto": "Usa además la función de la biblioteca para la potencia o la raíz y resuélvelo en **Python**.",
    "impls": {
        "python": r"""import sys

n = int(sys.stdin.readline())
print(f"abs={abs(n)}")
""",
        "javascript": r"""import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`abs=${Math.abs(n)}`);
""",
        "typescript": r"""import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`abs=${Math.abs(n)}`);
""",
        "java": r"""import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        System.out.println("abs=" + Math.abs(n));
    }
}
""",
        "csharp": r"""using System;

long n = long.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"abs={Math.Abs(n)}");
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
	if n < 0 {
		n = -n
	}
	fmt.Printf("abs=%d\n", n)
}
""",
        "rust": r"""use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("abs={}", n.abs());
}
""",
        "c": r"""#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("abs=%ld\n", labs(n));
    return 0;
}
""",
        "php": r"""<?php
$n = (int) trim(fgets(STDIN));
echo "abs=" . abs($n) . "\n";
""",
        "sql": r"""-- SQL: abs() incorporado.
WITH nums(n) AS (VALUES (-5), (3), (0))
SELECT printf('abs=%d', abs(n)) AS resultado FROM nums;
""",
    },
}


def main():
    for num, spec in S.items():
        g3.write_class(num, spec)
        print(f"Clase {num:03d} generada.")


if __name__ == "__main__":
    main()
