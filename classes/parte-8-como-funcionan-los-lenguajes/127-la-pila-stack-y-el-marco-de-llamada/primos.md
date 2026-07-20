# 🧬 El mismo programa en las familias de lenguajes — Clase 127

> [⬅️ Volver a la clase 127](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —una suma recursiva que apila un marco por cada
llamada— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo
por los diez lenguajes del núcleo.

Si entendiste la versión de C, la de Zig te resultará familiar aunque no la hayas visto nunca. Ese
reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n` (1 ≤ n ≤ 1000)
- **Salida** (stdout): `suma=<1+...+n> profundidad=<n>`
- **Regla:** la suma se calcula **recursivamente**; la profundidad es el número de marcos apilados,
  que coincide con `n`

| stdin | esperado |
|---|---|
| `5` | `suma=15 profundidad=5` |
| `3` | `suma=6 profundidad=3` |
| `1` | `suma=1 profundidad=1` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La pila de estos lenguajes es la del **intérprete**, no la del procesador: cada marco es un objeto
del runtime, y por eso el límite de recursión es una **política configurable** y no un tamaño de
memoria fijo.

### Ruby

```ruby
def sumar(n)
  n.zero? ? 0 : n + sumar(n - 1)
end

n = STDIN.gets.to_i
puts "suma=#{sumar(n)} profundidad=#{n}"
```

### Perl

```perl
no warnings 'recursion';   # Perl avisa a partir de 100 marcos; aquí es esperado

sub sumar {
    my ($n) = @_;
    return $n == 0 ? 0 : $n + sumar($n - 1);
}

my $n = <STDIN>;
chomp $n;
printf "suma=%d profundidad=%d\n", sumar($n), $n;
```

### Lua

```lua
local function sumar(n)
  if n == 0 then return 0 end
  return n + sumar(n - 1)
end

local n = io.read("n")
print(string.format("suma=%d profundidad=%d", sumar(n), n))
```

### Tcl

```tcl
interp recursionlimit {} 2000   ;# el límite por defecto es 1000 marcos

proc sumar {n} {
    if {$n == 0} { return 0 }
    return [expr {$n + [sumar [expr {$n - 1}]]}]
}

gets stdin n
puts "suma=[sumar $n] profundidad=$n"
```

### R

```r
options(expressions = 5000)   # R cuenta expresiones anidadas, no marcos

sumar <- function(n) if (n == 0) 0 else n + sumar(n - 1)

n <- as.integer(readLines("stdin", n = 1))
cat(sprintf("suma=%d profundidad=%d\n", sumar(n), n))
```

**Qué reconocer:** los cinco definen la función igual y confían en que el intérprete apile un marco
por llamada, pero **ninguno deja tocar esa pila**: se ajusta con una perilla (`interp
recursionlimit` en Tcl, `options(expressions=)` en R, `sys.setrecursionlimit` en el Python de la
clase) en vez de con un tamaño en bytes. Perl es el más elocuente: emite un aviso a los 100 marcos
porque históricamente su marco es caro. Lua es el único de la familia que implementa **llamadas de
cola propias** —un `return f(x)` reutiliza el marco—, pero aquí la suma no es de cola: el `n +`
pendiente obliga a conservar el marco hasta la vuelta.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

int sumar(int n) => n == 0 ? 0 : n + sumar(n - 1);

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  print('suma=${sumar(n)} profundidad=$n');
}
```

### ActionScript 3

```actionscript
package {
    // El reproductor Flash no tiene stdin: se ilustra la recursión sobre un n dado.
    public class Pila {
        public static function sumar(n:int):int {
            return n == 0 ? 0 : n + sumar(n - 1);
        }

        public static function reporte(n:int):String {
            return "suma=" + sumar(n) + " profundidad=" + n;
        }
    }
}
```

**Qué reconocer:** ambos heredan el modelo de pila de ECMAScript: un solo hilo, una sola pila, y el
desbordamiento se manifiesta como una **excepción** (`Stack Overflow` / `RangeError`) que el programa
puede capturar, no como el fallo de segmentación que produciría C. Dart añade tipos estáticos sobre
ese mismo esqueleto; ActionScript, que congeló ECMAScript 4, ya traía `:int` mucho antes que
TypeScript.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos comparten la misma pila de la máquina
virtual, con un tamaño por hilo fijado al arrancar (`-Xss`) y la misma `StackOverflowError`.

### Kotlin

```kotlin
fun sumar(n: Long): Long = if (n == 0L) 0 else n + sumar(n - 1)

fun main() {
    val n = readLine()!!.trim().toLong()
    println("suma=${sumar(n)} profundidad=$n")
}
```

### Scala

```scala
object Pila {
  def sumar(n: Long): Long = if (n == 0) 0 else n + sumar(n - 1)

  def main(args: Array[String]): Unit = {
    val n = scala.io.StdIn.readLine().trim.toLong
    println(s"suma=${sumar(n)} profundidad=$n")
  }
}
```

### Groovy

```groovy
long sumar(long n) { n == 0 ? 0L : n + sumar(n - 1) }

def n = System.in.newReader().readLine().trim() as long
println "suma=${sumar(n)} profundidad=$n"
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; La JVM no elimina llamadas de cola: `recur` es la salida explícita de Clojure,
;; pero esta suma no es de cola y sí apila un marco por llamada.
(defn sumar [n]
  (if (zero? n) 0 (+ n (sumar (dec n)))))

(let [n (Long/parseLong (str/trim (read-line)))]
  (println (str "suma=" (sumar n) " profundidad=" n)))
```

**Qué reconocer:** los cuatro compilan a la misma instrucción `invokestatic`/`invokevirtual` y por
tanto **comparten el mismo marco de la JVM**: operandos, variables locales y dirección de retorno.
La diferencia está en qué ofrece cada lenguaje para no apilar: Scala aplica `@tailrec` cuando la
llamada es de cola, Clojure obliga a escribir `recur` porque la JVM no lo hace sola, y Kotlin y
Groovy simplemente apilan. Ninguno puede fijar el tamaño de pila desde el código: eso es un
argumento de arranque de la máquina virtual.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let rec sumar n = if n = 0L then 0L else n + sumar (n - 1L)

let n = int64 (stdin.ReadLine().Trim())
printfn "suma=%d profundidad=%d" (sumar n) n
```

### VB.NET

```vbnet
Module Pila
    Function Sumar(n As Long) As Long
        If n = 0 Then Return 0
        Return n + Sumar(n - 1)
    End Function

    Sub Main()
        Dim n As Long = Long.Parse(Console.ReadLine().Trim())
        Console.WriteLine($"suma={Sumar(n)} profundidad={n}")
    End Sub
End Module
```

**Qué reconocer:** el CLR es el único de los grandes runtimes que tiene una instrucción explícita
para llamadas de cola (`tail.`), y el compilador de F# la emite cuando la recursión lo permite —esta
no lo permite, porque el `n +` queda pendiente—. En .NET el desbordamiento es especialmente brusco:
`StackOverflowException` **no se puede capturar** desde .NET 2.0, el proceso muere. Fíjate también en
que F# exige la palabra `rec` para que un nombre pueda referirse a sí mismo: la recursión es opt-in,
no un accidente.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Aquí la pila **es** la del procesador: un registro
apuntador de pila, un marco por llamada con parámetros, locales y dirección de retorno.

### C++

```cpp
#include <iostream>

long sumar(long n) { return n == 0 ? 0 : n + sumar(n - 1); }

int main() {
    long n;
    std::cin >> n;
    std::cout << "suma=" << sumar(n) << " profundidad=" << n << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

static long sumar(long n) { return n == 0 ? 0 : n + sumar(n - 1); }

int main(void) {
    @autoreleasepool {
        long n;
        if (scanf("%ld", &n) != 1) return 1;
        printf("suma=%ld profundidad=%ld\n", sumar(n), n);
    }
    return 0;
}
```

**Qué reconocer:** los dos son **superconjuntos de C** y la función recursiva de la clase compila tal
cual en ambos. Lo que se apila es idéntico: cada marco reserva espacio para `n` y para la dirección
de retorno, y el desbordamiento no produce excepción sino **fallo de segmentación**, porque nadie
está vigilando. C++ añade sobre ese marco el desenrollado (*unwinding*) que destruye los objetos
locales cuando sube una excepción; Objective-C conserva `printf` y el marco de C intactos y solo
envuelve el cuerpo en el bloque `@autoreleasepool`, que es gestión de **heap**, no de pila.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin máquina
virtual, con la pila a la vista y el coste de cada llamada a cuenta del programador.

### Zig

```zig
const std = @import("std");

fn sumar(n: i64) i64 {
    return if (n == 0) 0 else n + sumar(n - 1);
}

pub fn main() !void {
    var buf: [32]u8 = undefined;   // este búfer vive en el marco de main
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r"), 10);
    try std.io.getStdOut().writer().print("suma={d} profundidad={d}\n", .{ sumar(n), n });
}
```

### Nim

```nim
import std/strutils

proc sumar(n: int): int =
  if n == 0: 0 else: n + sumar(n - 1)

let n = stdin.readLine().strip().parseInt()
echo "suma=", sumar(n), " profundidad=", n
```

### D

```d
import std.stdio, std.string, std.conv;

long sumar(long n) { return n == 0 ? 0 : n + sumar(n - 1); }

void main() {
    const n = readln().strip().to!long;
    writefln("suma=%d profundidad=%d", sumar(n), n);
}
```

**Qué reconocer:** los tres compilan a la misma secuencia de `call`/`ret` que C, pero cada uno mide
la pila a su manera. Zig es el más literal: el `var buf: [32]u8` está diciendo *reserva 32 bytes en
este marco*, y el compilador puede calcular el uso máximo de pila de una función —algo que importa
en sistemas embebidos—. Nim reconoce las llamadas de cola cuando el backend de C las optimiza, y D
ofrece `pragma(inline)` para eliminar el marco del todo. Compara esto con Go, cuyo representante en
la clase crece la pila **dinámicamente** copiándola a un bloque mayor: es la excepción de la familia,
y por eso una recursión profunda en Go no desborda donde sí desbordaría en C.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** se quiere, no **cómo**
recorrerlo; la pila, si existe, es un detalle del motor.

### Prolog

```prolog
:- initialization(main, main).

sumar(0, 0) :- !.
sumar(N, S) :-
    N > 0,
    M is N - 1,
    sumar(M, S0),
    S is S0 + N.

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    sumar(N, S),
    format("suma=~d profundidad=~d~n", [S, N]).
```

### Datalog

```datalog
% Datalog no tiene E/S ni pila de llamadas observable: no "llama", deriva hechos
% por punto fijo. La recursión es una propiedad de la regla, no una secuencia de
% marcos. Se escribe aquí con la aritmética de un motor tipo Soufflé.
num(1). num(2). num(3). num(4). num(5).

suma_hasta(1, 1).
suma_hasta(N, S) :- num(N), suma_hasta(N - 1, S0), S = S0 + N.

profundidad(N, N) :- num(N).
```

**Qué reconocer:** Prolog sí tiene pila —de hecho tiene **dos**: la de entornos y la de puntos de
elección para el retroceso—, y el corte (`!`) de la primera cláusula existe justamente para no dejar
un punto de elección colgando en cada nivel. Datalog está en el otro extremo: no hay llamada ni
retorno, el motor calcula el **punto fijo** de las reglas y el orden de evaluación es asunto suyo.
Es la misma renuncia que hace SQL —incluso en su `WITH RECURSIVE`— al no decirte si la recursión se
resuelve apilando marcos o iterando sobre una tabla temporal.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y la misma pregunta debajo: *¿quién paga el marco de llamada?*
En C, Zig o D lo paga el procesador y el precio es el fallo de segmentación. En la JVM y el CLR lo
paga la máquina virtual y el precio es una excepción. En los intérpretes lo paga una estructura del
runtime y el precio es un límite ajustable. En Datalog nadie lo paga porque no hay llamada. Eso es lo
transferible.

⏮️ [Volver a la clase 127](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
