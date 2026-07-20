# 🧬 El mismo programa en las familias de lenguajes — Clase 130

> [⬅️ Volver a la clase 130](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —reservar un arreglo, llenarlo, sumarlo y
liberarlo— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no
solo por los diez lenguajes del núcleo.

Si entendiste la versión de C, la de Zig te resultará familiar aunque no la hayas visto nunca. Ese
reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n` (n ≥ 1)
- **Salida** (stdout): `reservado=<n> suma=<1+...+n>`
- **Regla:** reservar `n` enteros, llenarlos de `1` a `n`, sumarlos y liberar la reserva

| stdin | esperado |
|---|---|
| `5` | `reservado=5 suma=15` |
| `1` | `reservado=1 suma=1` |
| `3` | `reservado=3 suma=6` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Ninguno de los cinco tiene `free`. La liberación ocurre, pero el programa no la manda: como mucho la
sugiere.

### Ruby

```ruby
n = STDIN.gets.to_i
arr = Array.new(n) { |i| i + 1 }   # el recolector de Ruby reserva y libera
puts "reservado=#{n} suma=#{arr.sum}"
```

### Perl

```perl
my $n = <STDIN>;
chomp $n;
{
    my @arr = (1 .. $n);   # conteo de referencias: al cerrar el bloque, se libera
    my $suma = 0;
    $suma += $_ for @arr;
    print "reservado=$n suma=$suma\n";
}
```

### Lua

```lua
local n = io.read("n")
local arr = {}
local suma = 0
for i = 1, n do
  arr[i] = i
  suma = suma + i
end
arr = nil            -- soltar la referencia es todo lo que puedes hacer
collectgarbage()     -- y esto solo SUGIERE una pasada del recolector
print(string.format("reservado=%d suma=%d", n, suma))
```

### Tcl

```tcl
gets stdin n
set arr {}
set suma 0
for {set i 1} {$i <= $n} {incr i} {
    lappend arr $i
    incr suma $i
}
unset arr   ;# borra el nombre; el valor muere cuando su contador llega a cero
puts "reservado=$n suma=$suma"
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))
arr <- integer(n)     # reserva de golpe; crecer en bucle copiaría el vector entero
arr[] <- seq_len(n)
cat(sprintf("reservado=%d suma=%d\n", n, sum(arr)))
rm(arr)               # rm() quita el nombre; gc() solo sugiere recoger
```

**Qué reconocer:** los cinco resuelven el problema sin nombrar la memoria, y el gesto de "liberar" se
degrada a **soltar el nombre**: `arr = nil`, `unset`, `rm()`, cerrar el bloque. Bajo el capó hay dos
mecanismos distintos y conviene distinguirlos: Perl y Tcl usan **conteo de referencias**, así que la
liberación es inmediata y determinista salvo con ciclos; Ruby, Lua y R usan **recolector con
marcado**, donde el momento exacto es cosa del runtime. Por eso `collectgarbage()` y `gc()` son
peticiones, no órdenes: es la diferencia más honesta que se puede trazar frente al `free` de la
clase.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  final arr = List<int>.filled(n, 0);   // reserva fija; no hay forma de liberarla a mano
  var suma = 0;
  for (var i = 0; i < n; i++) {
    arr[i] = i + 1;
    suma += arr[i];
  }
  print('reservado=$n suma=$suma');
}
```

### ActionScript 3

```actionscript
package {
    // El reproductor Flash no tiene stdin ni System.gc() en la versión de producción:
    // solo se puede soltar la referencia y esperar.
    public class Manual {
        public static function reporte(n:int):String {
            var arr:Vector.<int> = new Vector.<int>(n, true);
            var suma:int = 0;
            for (var i:int = 0; i < n; i++) {
                arr[i] = i + 1;
                suma += arr[i];
            }
            arr = null;
            return "reservado=" + n + " suma=" + suma;
        }
    }
}
```

**Qué reconocer:** esta familia es la que menos control ofrece de las siete. No existe `free`, no
existe `delete` de memoria —el `delete` de JavaScript borra una propiedad, no un bloque— y ni
siquiera hay una forma estándar de forzar el recolector. La única herramienta real es **soltar la
referencia**, y de ahí que la fuga típica en la web no sea memoria sin liberar sino memoria que sigue
alcanzable: un escuchador de eventos que nadie quitó. `WeakMap`, `WeakRef` y el `Vector` de tamaño
fijo de ActionScript son los únicos gestos que quedan para influir en el recolector.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Reservar cuesta casi nada —mover un puntero en
la generación joven—; liberar no está en el catálogo de operaciones del lenguaje.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toInt()
    val arr = IntArray(n) { it + 1 }   // arreglo primitivo: n enteros contiguos, sin cajas
    println("reservado=$n suma=${arr.sum()}")
}
```

### Scala

```scala
object Manual {
  def main(args: Array[String]): Unit = {
    val n = scala.io.StdIn.readLine().trim.toInt
    val arr = Array.tabulate(n)(_ + 1)
    println(s"reservado=$n suma=${arr.sum}")
  }
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim() as int
def arr = (1..n).toList()
println "reservado=$n suma=${arr.sum()}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [n (Long/parseLong (str/trim (read-line)))
      arr (int-array (range 1 (inc n)))]   ; arreglo Java real, liberado por el GC
  (println (str "reservado=" n " suma=" (reduce + arr))))
```

**Qué reconocer:** los cuatro reservan lo mismo y ninguno libera, porque **la JVM no tiene una
instrucción para liberar**: `System.gc()` es una sugerencia que la máquina puede ignorar y los
finalizadores llevan años desaconsejados. El control que sí existe es sobre la **forma** de la
reserva: `IntArray` en Kotlin y `int-array` en Clojure producen n enteros contiguos, mientras que la
lista de Groovy guarda n objetos `Integer` con su cabecera cada uno. Esa elección —primitivo o
envuelto— es lo más parecido a gestionar memoria que ofrece la plataforma, y explica por qué el
equivalente honesto del `free` de C aquí no es una llamada sino una decisión de tipos.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let n = int (stdin.ReadLine().Trim())
let arr = Array.init n (fun i -> i + 1)
printfn "reservado=%d suma=%d" n (Array.sum arr)
```

### VB.NET

```vbnet
Module Manual
    Sub Main()
        Dim n As Integer = Integer.Parse(Console.ReadLine().Trim())
        Dim arr(n - 1) As Integer    ' el CLR reserva; el GC decide cuándo liberar
        Dim suma As Integer = 0
        For i As Integer = 0 To n - 1
            arr(i) = i + 1
            suma += arr(i)
        Next
        Console.WriteLine($"reservado={n} suma={suma}")
    End Sub
End Module
```

**Qué reconocer:** el CLR tampoco deja liberar, pero es la única de las plataformas gestionadas que
formalizó la **liberación determinista de recursos** con `IDisposable` y `Using`: no libera memoria,
libera lo que la memoria representa —archivos, conexiones, manejadores del sistema—. Ese matiz es
importante porque es exactamente la mitad del problema que `free` resuelve en C. La otra herramienta
propia de .NET es `stackalloc`, que reserva en la **pila** y desaparece al volver de la función: un
bloque contiguo sin recolector, la vía de escape cuando el coste del heap importa.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). `malloc` pide, `free` devuelve, y entre ambos hay un
contrato que solo tú puedes cumplir.

### C++

```cpp
#include <iostream>
#include <memory>

int main() {
    long n;
    std::cin >> n;

    // `new long[n]` ... `delete[] arr` sería el eco literal de malloc/free, pero
    // lo idiomático hoy es un puntero inteligente: el destructor libera aunque
    // salte una excepción por el medio.
    auto arr = std::make_unique<long[]>(n);
    long suma = 0;
    for (long i = 0; i < n; i++) {
        arr[i] = i + 1;
        suma += arr[i];
    }
    std::cout << "reservado=" << n << " suma=" << suma << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        long n;
        if (scanf("%ld", &n) != 1) return 1;

        /* malloc/free de C siguen ahí para memoria plana... */
        long *arr = calloc(n, sizeof(long));
        long suma = 0;
        for (long i = 0; i < n; i++) {
            arr[i] = i + 1;
            suma += arr[i];
        }
        free(arr);

        /* ...pero los objetos se gestionan por conteo de referencias, y con ARC
           el compilador inserta retain/release: nunca los escribes a mano. */
        printf("reservado=%ld suma=%ld\n", n, suma);
    }
    return 0;
}
```

**Qué reconocer:** los dos **pueden** escribir el `malloc`/`free` de la clase palabra por palabra, y
esa capacidad es justamente lo que hace interesante que no lo hagan. C++ tiene `new`/`delete` como
pareja propia, pero la práctica moderna los considera un olor a código: se prefiere **RAII** y
punteros inteligentes (`unique_ptr`, `shared_ptr`), donde el destructor libera de forma determinista
y a prueba de excepciones. Objective-C conserva `calloc`/`free` para memoria plana y usa **conteo
automático de referencias (ARC)** para los objetos: el compilador escribe los `retain`/`release` que
antes escribía el programador, así que la liberación sigue siendo determinista, pero los ciclos
requieren romperlos a mano con `__weak`.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Aquí está la variedad
más rica de respuestas: recolector, propiedad, conteo de referencias y asignadores explícitos.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    // El rasgo más distintivo de Zig: no hay malloc global. El asignador es un
    // valor que se pasa como argumento, así que quien reserva elige la política
    // y una biblioteca no puede reservar a tus espaldas.
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer std.debug.assert(gpa.deinit() == .ok);   // avisa si quedó memoria sin liberar
    const allocator = gpa.allocator();

    var buf: [32]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(usize, std.mem.trim(u8, linea, " \r"), 10);

    const arr = try allocator.alloc(usize, n);
    defer allocator.free(arr);   // `defer` empareja la liberación con la reserva

    var suma: usize = 0;
    for (arr, 0..) |*x, i| {
        x.* = i + 1;
        suma += x.*;
    }
    try std.io.getStdOut().writer().print("reservado={d} suma={d}\n", .{ n, suma });
}
```

### Nim

```nim
import std/strutils

let n = stdin.readLine().strip().parseInt()
var arr = newSeq[int](n)   # con ARC/ORC el compilador inserta el destructor: sin GC ni free
var suma = 0
for i in 0 ..< n:
  arr[i] = i + 1
  suma += arr[i]
echo "reservado=", n, " suma=", suma
```

### D

```d
import std.stdio, std.string, std.conv;
import core.stdc.stdlib : malloc, free;

@nogc void llenar(long[] arr) {
    foreach (i, ref x; arr) x = cast(long)(i + 1);
}

void main() {
    const n = readln().strip().to!long;
    // D tiene recolector por defecto, pero `@nogc` más malloc/free devuelven
    // el modo manual de C cuando el coste de las pausas importa.
    auto p = cast(long*) malloc(long.sizeof * n);
    scope (exit) free(p);
    auto arr = p[0 .. n];

    llenar(arr);
    long suma = 0;
    foreach (x; arr) suma += x;
    writefln("reservado=%d suma=%d", n, suma);
}
```

**Qué reconocer:** las tres respuestas de esta familia son distintas entre sí y las tres son
legítimas. Zig hace la asignación **explícita mediante un asignador que se pasa como argumento**: no
existe un heap global implícito, `alloc` y `free` van emparejados con `defer`, y el
`GeneralPurposeAllocator` te dice al salir si dejaste una fuga —es el `malloc`/`free` de C con la
política convertida en un parámetro—. Nim ocupa el punto medio: desde la versión 2 usa **ARC/ORC**,
conteo de referencias insertado por el compilador con un recolector de ciclos opcional, así que no
escribes `free` ni sufres pausas globales. D es el más flexible y el más incómodo de clasificar:
recolector por defecto, `@nogc` para prohibirlo en una función, y `malloc`/`free` de C a un `import`
de distancia. Compara con los representantes: Go elige recolector sin excepciones, Rust elige
**propiedad** y libera al final del ámbito sin recolector ni contador.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). No hay reserva ni liberación en el modelo: hay
hechos y consultas.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    numlist(1, N, Arr),
    sum_list(Arr, Suma),
    format("reservado=~d suma=~d~n", [N, Suma]).
```

### Datalog

```datalog
% Datalog no reserva ni libera: los hechos derivados existen mientras dura la
% evaluación y desaparecen con ella. No hay E/S ni memoria en el modelo.
% Se escribe con la aritmética y los agregados de un motor tipo Soufflé.
n(5).

celda(1).
celda(I) :- celda(J), I = J + 1, n(N), I <= N.

reservado(N) :- n(N).
suma(S) :- S = sum I : { celda(I) }.
```

**Qué reconocer:** Prolog **no expone la memoria en absoluto**: `numlist` reserva N celdas en su
heap de términos sin que aparezca ninguna palabra al respecto, y la recuperación la hace el
**retroceso**, que al deshacer una alternativa recorta el heap hasta la marca anterior de una vez —un
mecanismo que no se parece ni al `free` de C ni al recolector de la JVM—. Datalog va más allá: no hay
estructuras, no hay tiempo de vida y no hay operación de liberación, porque el conjunto de hechos
derivados vive y muere con la evaluación completa. Es la misma renuncia de SQL, donde nadie te
pregunta si la tabla temporal cabe en memoria.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y todas las estrategias conocidas para responder *¿quién libera?*
Tú con `free` en C, D en modo `@nogc` y Objective-C para memoria plana. El destructor, en C++ y en
Nim. El contador de referencias, en Perl, Tcl y los objetos de Objective-C. El recolector, en Ruby,
Lua, R, la web entera, la JVM, el CLR y D por defecto. Un asignador que tú elegiste y pasaste como
argumento, en Zig. Y nadie, en Prolog y Datalog. Eso es lo transferible.

⏮️ [Volver a la clase 130](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
