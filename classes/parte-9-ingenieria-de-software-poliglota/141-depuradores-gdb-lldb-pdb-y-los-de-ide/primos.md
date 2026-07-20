# 🧬 El mismo programa en las familias de lenguajes — Clase 141

> [⬅️ Volver a la clase 141](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —imprimir la traza de sumas acumuladas, lo que verías
avanzando paso a paso en un depurador— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n` (n ≥ 1)
- **Salida** (stdout): `traza=<sumas acumuladas de 1 a n, unidas por guiones>`
- **Regla:** `traza[i] = 1 + 2 + ... + i`

| stdin | esperado |
|---|---|
| `3` | `traza=1-3-6` |
| `1` | `traza=1` |
| `4` | `traza=1-3-6-10` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La traza a mano es lo que se escribe cuando no se quiere abrir un depurador; en esta familia,
además, casi siempre hay uno esperando en la propia distribución.

### Ruby

```ruby
n = STDIN.gets.to_i
acc = 0
pasos = (1..n).map { |i| acc += i }
puts "traza=#{pasos.join('-')}"
```

### Perl

```perl
my $n = <STDIN>;
my ($acc, @pasos) = (0);
for my $i (1 .. $n) {
    $acc += $i;
    push @pasos, $acc;
}
print "traza=", join('-', @pasos), "\n";
```

### Lua

```lua
local n = io.read("n")
local acc, pasos = 0, {}
for i = 1, n do
  acc = acc + i
  pasos[#pasos + 1] = acc
end
print("traza=" .. table.concat(pasos, "-"))
```

### Tcl

```tcl
set n [gets stdin]
set acc 0
set pasos {}
for {set i 1} {$i <= $n} {incr i} {
    incr acc $i
    lappend pasos $acc
}
puts "traza=[join $pasos -]"
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))
cat(sprintf("traza=%s\n", paste(cumsum(1:n), collapse = "-")))
```

**Qué reconocer:** el bucle acumulador es idéntico en cuatro de los cinco, y R rompe la forma porque
`cumsum` **ya es** la traza: en un lenguaje vectorial el estado intermedio no se construye a mano,
se pide como valor. Eso tiene una consecuencia directa al depurar: cuando el paso a paso no existe
como bucle, el punto de ruptura tiene poco que interrumpir, y por eso R depura con `browser()`,
`debug()` y `traceback()` —inspección del entorno— más que con avance de instrucción. Perl es el
contrario: lleva un depurador completo **dentro del intérprete**, y basta `perl -d guion.pl` para
tenerlo. Ruby trae `debug` en la distribución desde la 3.1, con `byebug` como alternativa clásica;
Lua expone la biblioteca `debug` con enganches por línea y llamada, que es la materia prima con la
que se construyeron depuradores externos como el de ZeroBrane; Tcl vigila el estado con
`trace add variable`, que dispara un procedimiento cada vez que una variable cambia. Cinco maneras
distintas de contestar a la misma pregunta: *¿cuánto valía `acc` en el paso 3?*

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  var acc = 0;
  final pasos = <int>[];
  for (var i = 1; i <= n; i++) {
    acc += i;
    pasos.add(acc);
  }
  print("traza=${pasos.join("-")}");
}
```

### ActionScript 3

```actionscript
// Sin stdin en el reproductor Flash: se ilustra la traza que vería el depurador.
package {
    public class Traza {
        public static function traza(n:int):String {
            var acc:int = 0;
            var pasos:Array = [];
            for (var i:int = 1; i <= n; i++) {
                acc += i;
                pasos.push(acc);
            }
            return "traza=" + pasos.join("-");
        }
    }
}
```

**Qué reconocer:** los dos son la familia donde el depurador vive **dentro de la herramienta de
desarrollo**, no en la línea de órdenes. Dart expone `dart:developer` con una función `debugger()`
que detiene la ejecución, y su VM habla el *Dart VM Service Protocol*, el mismo canal que usan tanto
el IDE como las herramientas de Flutter. ActionScript tenía `fdb`, el depurador del reproductor
Flash. La lección transferible es que aquí el depurador es un **servicio al que el editor se
conecta**, no un programa que envuelve al tuyo, y es exactamente el modelo que hoy generalizó el
*Debug Adapter Protocol* de los IDE.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Un solo depurador para todos, porque todos
producen el mismo bytecode.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toInt()
    var acc = 0
    val pasos = (1..n).map { acc += it; acc }
    println("traza=" + pasos.joinToString("-"))
}
```

### Scala

```scala
object Traza {
  def main(args: Array[String]): Unit = {
    val n = scala.io.StdIn.readLine().trim.toInt
    val pasos = (1 to n).scanLeft(0)(_ + _).tail
    println("traza=" + pasos.mkString("-"))
  }
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim().toInteger()
def acc = 0
def pasos = (1..n).collect { acc += it }
println "traza=" + pasos.join('-')
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [n (parse-long (str/trim (read-line)))
      pasos (reductions + (range 1 (inc n)))]
  (println (str "traza=" (str/join "-" pasos))))
```

**Qué reconocer:** Scala y Clojure no acumulan en una variable: `scanLeft` y `reductions` producen la
traza como secuencia de estados intermedios, que es la versión funcional de "avanzar paso a paso".
Los cuatro se depuran con el **mismo** mecanismo —**JDWP**, el protocolo de cableado de la JVM, y su
cliente de línea de órdenes `jdb`— porque el depurador trabaja sobre bytecode y no sabe en qué
lenguaje se escribió el original. Ahí aparece la grieta: el punto de ruptura que pones en una línea
de Scala o de Groovy cae sobre bytecode generado, con nombres sintéticos y clases anónimas que no
escribiste, y el paso a paso salta de forma sorprendente. Clojure prefiere por eso otra vía —el
**REPL**, que permite inspeccionar y redefinir en caliente sin detener el proceso—, y esa es una
manera legítima de depurar que Java no tiene por costumbre.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let n = stdin.ReadLine().Trim() |> int
let pasos = [ 1 .. n ] |> List.scan (+) 0 |> List.tail
printfn "traza=%s" (pasos |> List.map string |> String.concat "-")
```

### VB.NET

```vbnet
Module Traza
    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Dim acc = 0
        Dim pasos As New List(Of String)
        For i = 1 To n
            acc += i
            pasos.Add(acc.ToString())
        Next
        Console.WriteLine("traza=" & String.Join("-", pasos))
    End Sub
End Module
```

**Qué reconocer:** el paralelo con la JVM es exacto —un depurador para toda la plataforma, guiado por
los archivos de símbolos `.pdb`— y también lo es el problema: `List.scan` de F# genera cierres y
funciones internas que el paso a paso muestra con nombres que no están en tu código, mientras que el
bucle explícito de VB.NET se recorre línea a línea sin sorpresas. Es el precio recurrente de las
abstracciones de alto nivel al depurar. F# ofrece a cambio algo distinto: `dotnet fsi`, un intérprete
interactivo donde se evalúa la expresión sospechosa suelta, en la misma línea de lo que hace el REPL
de Clojure.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). El territorio nativo de **gdb** y **lldb**.

### C++

```cpp
#include <iostream>

int main() {
    int n;
    std::cin >> n;
    long acc = 0;
    for (int i = 1; i <= n; ++i) {
        acc += i;
        std::cout << (i == 1 ? "traza=" : "-") << acc;
    }
    std::cout << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        int n;
        scanf("%d", &n);
        NSMutableArray<NSString *> *pasos = [NSMutableArray array];
        long acc = 0;
        for (int i = 1; i <= n; i++) {
            acc += i;
            [pasos addObject:[NSString stringWithFormat:@"%ld", acc]];
        }
        printf("traza=%s\n", [[pasos componentsJoinedByString:@"-"] UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** ambos compilan a código máquina con símbolos **DWARF**, así que `gdb` y `lldb`
funcionan sin adaptación: `break main`, `next`, `print acc`. Esta familia es la que **define** lo que
significa depurar —punto de ruptura, marco de pila, inspección de memoria— y el resto de la industria
copió el vocabulario. La diferencia práctica está en que aquí el depurador es la herramienta de
primera línea y no el último recurso, porque sin él un fallo de segmentación no te dice nada. Y ojo
con la optimización: compilado con `-O2` el bucle puede desaparecer y el depurador enseñará
variables "optimizadas fuera"; por eso se depura con `-g -O0`.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Binario nativo, sin
máquina virtual, y sin depurador propio del lenguaje.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(u32, std.mem.trim(u8, linea, " \r\t"), 10);
    const out = std.io.getStdOut().writer();
    try out.writeAll("traza=");
    var acc: u64 = 0;
    var i: u32 = 1;
    while (i <= n) : (i += 1) {
        acc += i;
        if (i > 1) try out.writeByte('-');
        try out.print("{d}", .{acc});
    }
    try out.writeByte('\n');
}
```

### Nim

```nim
import std/strutils

let n = stdin.readLine().strip().parseInt()
var acc = 0
var pasos: seq[string]
for i in 1 .. n:
  acc += i
  pasos.add($acc)
echo "traza=", pasos.join("-")
```

### D

```d
import std.stdio, std.conv, std.string, std.array;

void main() {
    const n = readln().strip().to!int;
    long acc = 0;
    string[] pasos;
    foreach (i; 1 .. n + 1) {
        acc += i;
        pasos ~= acc.to!string;
    }
    writeln("traza=", pasos.join("-"));
}
```

**Qué reconocer:** los tres emiten **DWARF** y se depuran con `gdb` o `lldb`, los mismos de C, igual
que Rust —que además distribuye los envoltorios `rust-gdb` y `rust-lldb` para imprimir sus tipos de
forma legible— y que Go, el único de la familia con depurador propio, **Delve**, escrito porque el
planificador de gorutinas confundía a los depuradores generales. Nim tiene el caso más curioso: su
compilador **genera C** y luego lo compila, así que sin cuidado el depurador te enseña el C
intermedio en vez de tu fuente; por eso Nim inserta directivas de línea para que `gdb` sepa volver al
`.nim` original. Es el mismo problema de los nombres sintéticos de la JVM, pero un piso más abajo:
**el depurador siempre ve el código generado, no el que escribiste**, y todo lo demás es maquinaria
para disimularlo.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Sin bucle explícito, la traza tampoco es una
sucesión de líneas.

### Prolog

```prolog
:- initialization(main, main).

acumuladas(N, Pasos) :-
    numlist(1, N, Xs),
    findall(S, (member(I, Xs), numlist(1, I, Ys), sum_list(Ys, S)), Pasos).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    acumuladas(N, Pasos),
    atomic_list_concat(Pasos, '-', Texto),
    format("traza=~w~n", [Texto]).
```

### Datalog

```datalog
% Datalog no tiene E/S ni acumuladores: la traza se declara como relación
% recursiva. La aritmética la añaden dialectos como Soufflé.
paso(1, 1).
paso(I, S) :- paso(J, T), I = J + 1, I <= 4, S = T + I.
```

**Qué reconocer:** aquí el depurador cambia de modelo por completo. SWI-Prolog tiene `trace/0`, que
no avanza por líneas sino por los **cuatro puertos** de cada objetivo —`call`, `exit`, `redo`,
`fail`—, y ese `redo` es lo que no existe en ningún lenguaje imperativo: es el motor volviendo atrás
para probar otra alternativa. Depurar Prolog es seguir el árbol de búsqueda, no la pila. Datalog ni
siquiera tiene eso: al no haber orden de ejecución, lo que se inspecciona es la relación derivada
—qué tuplas aparecieron y por qué regla—, que es lo mismo que hace un `EXPLAIN` en SQL cuando quieres
entender la consulta. En las dos, el "paso a paso" es una explicación de la derivación, no un avance
de instrucción.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y la misma pregunta debajo: *¿cómo veo el estado intermedio?*
Compilados a nativo lo enseña `gdb` sobre DWARF; en la JVM y el CLR lo enseña un protocolo de
depuración sobre bytecode; en los dinámicos lo enseña el propio intérprete; en Prolog lo enseñan los
puertos del motor de búsqueda; y en Datalog no hay estado intermedio que enseñar. La traza impresa a
mano, en cambio, funciona en los veinte. Eso es lo transferible.

⏮️ [Volver a la clase 141](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
