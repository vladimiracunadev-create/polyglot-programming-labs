# 🧬 El mismo programa en las familias de lenguajes — Clase 069

> [⬅️ Volver a la clase 069](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —el n-ésimo número de Fibonacci por recursión—
resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los
diez lenguajes del núcleo.

Aquí la comparación tiene un filo extra: la recursión de cola **no** se comporta igual en todas
partes. Unos lenguajes garantizan que la llamada final reutiliza el marco de pila, otros lo hacen
solo si el optimizador quiere, y otros no lo hacen nunca. Ese es exactamente el tipo de garantía que
hay que aprender a preguntar antes de confiar en un algoritmo.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n` con `0 <= n <= 30`
- **Salida** (stdout): `fib=<F(n)>`
- **Regla:** `F(0)=0`, `F(1)=1`, `F(n)=F(n-1)+F(n-2)`

| stdin | esperado |
|---|---|
| `10` | `fib=55` |
| `1` | `fib=1` |
| `0` | `fib=0` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Ninguno de los dos optimiza la llamada de cola: Python incluso impone un límite de profundidad
(`sys.setrecursionlimit`). Los primos de la familia se separan justo en ese punto.

### Ruby

```ruby
def fib(n, a = 0, b = 1)
  n.zero? ? a : fib(n - 1, b, a + b)
end

n = STDIN.gets.to_i
puts "fib=#{fib(n)}"
```

### Perl

```perl
sub fib {
    my ($n, $a, $b) = @_;
    return $a if $n == 0;
    # `goto &sub` es la llamada de cola real de Perl: sustituye el marco actual.
    @_ = ($n - 1, $b, $a + $b);
    goto &fib;
}

my $n = <STDIN>;
chomp $n;
printf "fib=%d\n", fib($n, 0, 1);
```

### Lua

```lua
local function fib(n, a, b)
  if n == 0 then return a end
  -- `return f(...)` es una proper tail call: el manual de Lua la garantiza.
  return fib(n - 1, b, a + b)
end

local n = math.tointeger(io.read("n"))
print(string.format("fib=%d", fib(n, 0, 1)))
```

### Tcl

```tcl
proc fib {n a b} {
    if {$n == 0} { return $a }
    tailcall fib [expr {$n - 1}] $b [expr {$a + $b}]
}

gets stdin n
puts "fib=[fib $n 0 1]"
```

### R

```r
fib <- function(n, a = 0, b = 1) {
  if (n == 0) return(a)
  Recall(n - 1, b, a + b)
}

n <- as.integer(readLines("stdin", n = 1))
cat(sprintf("fib=%d\n", fib(n)))
```

**Qué reconocer:** los cinco escriben la misma función acumuladora, pero solo dos la ejecutan como
un bucle. **Lua** garantiza la *proper tail call* por especificación, y **Tcl** la pide de forma
explícita con `tailcall`; en cambio **Ruby** y **R** apilan un marco por llamada (R llega antes al
tope con `expressions`), y **Perl** necesita el rodeo de `goto &fib` —reasignar `@_` y saltar— para
conseguir lo que Lua da gratis. Que la sintaxis sea idéntica no significa que la garantía lo sea.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
ES2015 especificó las llamadas de cola propias, pero solo JavaScriptCore las implementó: en V8 y
SpiderMonkey siguen apilando.

### Dart

```dart
import 'dart:io';

int fib(int n, [int a = 0, int b = 1]) => n == 0 ? a : fib(n - 1, b, a + b);

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  print('fib=${fib(n)}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra la recursión.
package {
    public class Fibonacci {
        public static function fib(n:int, a:int = 0, b:int = 1):int {
            return n == 0 ? a : fib(n - 1, b, a + b);
        }

        public static function salida(n:int):String {
            return "fib=" + fib(n);
        }
    }
}
```

**Qué reconocer:** los parámetros con valor por defecto convierten la función en su propio
acumulador, un truco que se repite en toda esta página. Ni Dart ni AS3 eliminan la llamada de cola,
así que la profundidad sigue costando pila: la versión acumuladora aquí gana en **número de
operaciones** (lineal frente a exponencial), no en consumo de memoria.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La JVM **no** tiene una instrucción de llamada
de cola, así que cada lenguaje se inventa su forma de esquivarla; esta familia es el mejor ejemplo
del curso de cómo una limitación de la plataforma se filtra al lenguaje.

### Kotlin

```kotlin
tailrec fun fib(n: Int, a: Long = 0, b: Long = 1): Long =
    if (n == 0) a else fib(n - 1, b, a + b)

fun main() {
    val n = readLine()!!.trim().toInt()
    println("fib=${fib(n)}")
}
```

### Scala

```scala
import scala.annotation.tailrec

object Fibonacci {
  @tailrec
  def fib(n: Int, a: Long = 0, b: Long = 1): Long =
    if (n == 0) a else fib(n - 1, b, a + b)

  def main(args: Array[String]): Unit = {
    val n = scala.io.StdIn.readLine().trim.toInt
    println(s"fib=${fib(n)}")
  }
}
```

### Groovy

```groovy
def fib
fib = { int n, long a = 0, long b = 1 ->
    if (n == 0) return a
    fib.trampoline(n - 1, b, a + b)
}
fib = fib.trampoline()

def n = System.in.newReader().readLine().trim() as int
println "fib=${fib(n)}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(defn fib [n]
  ;; `recur` no es una llamada: es un salto al inicio del `loop`.
  (loop [k n, a 0, b 1]
    (if (zero? k) a (recur (dec k) b (+ a b)))))

(let [n (Long/parseLong (str/trim (read-line)))]
  (println (str "fib=" (fib n))))
```

**Qué reconocer:** las cuatro soluciones dicen lo mismo y las cuatro admiten que la JVM no ayuda.
**Kotlin** (`tailrec`) y **Scala** (`@tailrec`) marcan la función y el compilador la reescribe como
bucle —y **falla la compilación** si la llamada no estaba realmente en posición de cola, que es la
parte valiosa—. **Groovy** no toca el compilador: usa un *trampolín*, un objeto que devuelve la
siguiente llamada en vez de ejecutarla, y un bucle externo la va desenrollando. **Clojure** es el
más honesto de todos: `recur` es una forma especial distinta de la llamada normal, precisamente para
que quede escrito en el código que ahí no se apila nada.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). El CLR **sí** tiene el prefijo `.tail` en su
bytecode, pero no todos los compiladores lo emiten.

### F\#

```fsharp
let rec fib n (a: int64) (b: int64) =
    if n = 0 then a else fib (n - 1) b (a + b)

let n = stdin.ReadLine().Trim() |> int
printfn "fib=%d" (fib n 0L 1L)
```

### VB.NET

```vbnet
Module Fibonacci
    Function Fib(n As Integer, a As Long, b As Long) As Long
        If n = 0 Then Return a
        ' El compilador de VB no emite el prefijo .tail: esto apila un marco por llamada.
        Return Fib(n - 1, b, a + b)
    End Function

    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Console.WriteLine("fib=" & Fib(n, 0L, 1L))
    End Sub
End Module
```

**Qué reconocer:** misma máquina virtual, garantías opuestas. **F#** convierte la recursión de cola
simple en un bucle y, cuando no puede, emite `.tail` para que el CLR reutilice el marco: es un
lenguaje funcional que se apoyó en una plataforma que ya tenía la instrucción. **VB.NET** y C#
comparten runtime pero no emiten ese prefijo, así que su `Return Fib(...)` es una llamada normal.
La lección: la garantía vive en el **compilador**, no en la máquina.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). El estándar no promete nada sobre llamadas de cola;
el optimizador decide.

### C++

```cpp
#include <iostream>

long long fib(int n, long long a = 0, long long b = 1) {
    return n == 0 ? a : fib(n - 1, b, a + b);
}

int main() {
    int n;
    std::cin >> n;
    std::cout << "fib=" << fib(n) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

static long long fib(int n, long long a, long long b) {
    return n == 0 ? a : fib(n - 1, b, a + b);
}

int main(void) {
    @autoreleasepool {
        int n;
        if (scanf("%d", &n) != 1) return 1;
        printf("fib=%lld\n", fib(n, 0, 1));
    }
    return 0;
}
```

**Qué reconocer:** los dos son superconjuntos de C y el cuerpo de la función es el mismo ternario de
la implementación de la clase. La diferencia con Kotlin o F# es que aquí **nadie promete nada**: con
`-O2`, GCC y Clang suelen convertir esta llamada final en un salto (`jmp`), y sin optimizaciones la
apilan. Compilar el mismo código dos veces y obtener dos comportamientos de pila distintos es
normal en esta familia, y es la razón por la que en C no se escriben algoritmos que dependan de la
eliminación de la llamada de cola.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Go no optimiza la
llamada de cola (su pila crece dinámicamente, así que le importa menos); Rust tampoco la garantiza y
reserva `become` como palabra clave para el día que lo haga.

### Zig

```zig
const std = @import("std");

fn fib(n: u32, a: u64, b: u64) u64 {
    if (n == 0) return a;
    // @call con .always_tail obliga al backend a reutilizar el marco o a fallar al compilar.
    return @call(.always_tail, fib, .{ n - 1, b, a + b });
}

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(u32, std.mem.trim(u8, linea, " \r"), 10);
    try std.io.getStdOut().writer().print("fib={d}\n", .{fib(n, 0, 1)});
}
```

### Nim

```nim
import std/strutils

func fib(n: int, a: int64 = 0, b: int64 = 1): int64 =
  if n == 0: a else: fib(n - 1, b, a + b)

let n = stdin.readLine().strip().parseInt()
echo "fib=", fib(n)
```

### D

```d
import std.stdio, std.string, std.conv;

long fib(int n, long a = 0, long b = 1) {
    return n == 0 ? a : fib(n - 1, b, a + b);
}

void main() {
    const n = readln().strip().to!int;
    writefln("fib=%d", fib(n));
}
```

**Qué reconocer:** **Zig** es el único de los veinte que permite *exigir* la llamada de cola:
`@call(.always_tail, ...)` no es una sugerencia, es un error de compilación si el backend no puede
cumplirlo. Esa es la misma filosofía que ya viste en su manejo de errores: lo implícito se vuelve
explícito. **Nim** compila a C y hereda lo que haga el compilador de C (con `--passC:-O2` la llamada
suele desaparecer); **D** está en la misma situación. Tres lenguajes de sistemas, tres posturas: la
exigible, la heredada y la delegada al optimizador.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). El CTE `WITH RECURSIVE` de la clase es
recursión, aunque el motor la ejecute como una iteración sobre una tabla de trabajo.

### Prolog

```prolog
:- initialization(main, main).

fib(0, A, _, A).
fib(N, A, B, F) :-
    N > 0,
    N1 is N - 1,
    B1 is A + B,
    fib(N1, B, B1, F).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    fib(N, 0, 1, F),
    format("fib=~d~n", [F]).
```

### Datalog

```datalog
// Datalog puro no tiene E/S ni aritmética: no existe el caso "leer n de stdin".
// Los dialectos con números (Soufflé) sí permiten esta recursión sobre la relación.
.decl fib(i: number, f: number)

fib(0, 0).
fib(1, 1).
fib(i + 1, f1 + f2) :- fib(i, f1), fib(i - 1, f2), i < 30.

.output fib
```

**Qué reconocer:** **Prolog** no tiene bucles, así que la recursión no es una alternativa sino la
única forma de repetir; a cambio, su implementación clásica **sí** elimina la llamada de cola (*last
call optimization*) cuando la última meta del cuerpo es la llamada recursiva y no quedan puntos de
elección abiertos —por eso el `N > 0` del segundo caso importa tanto: sin él el motor guardaría un
punto de retroceso y la optimización no se aplicaría—. **Datalog** va un paso más allá: no hay
"llamada" que optimizar, porque el motor calcula el **punto fijo** de las reglas repitiendo la
derivación hasta que no aparecen hechos nuevos. Es la misma renuncia que hace SQL: describes la
relación, no el recorrido.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo esqueleto en todos: un caso base, un paso que se
acerca a él, y un acumulador que evita el árbol exponencial. Lo que **no** es igual son las
garantías: `tailrec`, `@tailrec`, `tailcall`, `recur`, `goto &sub`, `@call(.always_tail, ...)` o
nada en absoluto. Reconocer la forma es el primer paso; preguntar por la garantía es el segundo.

⏮️ [Volver a la clase 069](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
