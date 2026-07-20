# 🧬 El mismo programa en las familias de lenguajes — Clase 066

> [⬅️ Volver a la clase 066](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —producir los primeros `n` números pares sin
construir de golpe la secuencia— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Esta es, de todas las clases, donde más se separan las familias: hay lenguajes con generadores de
verdad, lenguajes donde **todo** es perezoso por defecto y lenguajes que no tienen nada de esto y
tienen que fabricarlo con un objeto o una función con memoria.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n` (con `n >= 1`)
- **Salida** (stdout): `pares=<2-4-...-2n>`
- **Regla:** `pares_i = 2·i` para `i` de `1` a `n`

| stdin | esperado |
|---|---|
| `3` | `pares=2-4-6` |
| `1` | `pares=2` |
| `5` | `pares=2-4-6-8-10` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Aquí la familia se rompe por dentro: Python y Ruby tienen generadores explícitos, Perl no tiene
ninguno y Lua resuelve el problema con una herramienta mucho más general que un generador.

### Ruby

```ruby
n = STDIN.gets.to_i

pares = Enumerator.new do |y|
  i = 1
  loop do
    y << 2 * i
    i += 1
  end
end

puts "pares=#{pares.take(n).join('-')}"
```

### Perl

```perl
# Perl no tiene generadores: el estado vive en una clausura.
sub generador_pares {
    my $i = 0;
    return sub { $i++; return 2 * $i };
}

my $n = <STDIN>;
chomp $n;

my $siguiente = generador_pares();
my @pares = map { $siguiente->() } 1 .. $n;

print "pares=", join('-', @pares), "\n";
```

### Lua

```lua
local n = tonumber(io.read("l"))

-- coroutine.wrap convierte una corrutina en una función que devuelve el siguiente valor.
local siguiente = coroutine.wrap(function()
  local i = 1
  while true do
    coroutine.yield(2 * i)
    i = i + 1
  end
end)

local salida = {}
for _ = 1, n do
  salida[#salida + 1] = siguiente()
end
print("pares=" .. table.concat(salida, "-"))
```

### Tcl

```tcl
set n [gets stdin]

# El `yield` inicial hace que la creación no consuma el primer valor.
coroutine pares apply {{} {
    yield
    set i 1
    while 1 {
        yield [expr {2 * $i}]
        incr i
    }
}}

set salida {}
for {set k 0} {$k < $n} {incr k} {
    lappend salida [pares]
}
puts "pares=[join $salida -]"
```

### R

```r
# R no tiene generadores: la pereza de R está en los argumentos (promesas), no en las secuencias.
n <- as.integer(readLines("stdin", n = 1))
pares <- 2L * seq_len(n)
cat(sprintf("pares=%s\n", paste(pares, collapse = "-")))
```

**Qué reconocer:** el `Enumerator` de Ruby con su *yielder* (`y <<`) es el equivalente exacto del
`yield` de Python, y `take(n)` corta un bucle **infinito** sin colgarse. Perl no tiene nada
parecido, así que el estado se guarda en una clausura: una función que recuerda su `$i` entre
llamadas —que es, literalmente, lo que un generador hace por dentro—. Lua es el caso más
interesante: sus **corrutinas** son más potentes que un generador (pueden ceder el control desde
cualquier profundidad de llamada), y `coroutine.wrap` las disfraza de generador. Tcl copió ese
diseño en la versión 8.6. R se queda fuera del concepto: construye el vector completo de golpe,
porque su modelo mental no es "producir uno a uno" sino "operar sobre todo a la vez".

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

Iterable<int> paresInfinitos() sync* {
  var i = 1;
  while (true) {
    yield 2 * i;
    i++;
  }
}

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  print('pares=${paresInfinitos().take(n).join('-')}');
}
```

### ActionScript 3

```actionscript
// AS3 no tiene generadores ni stdin: el iterador se escribe como objeto con estado.
package {
    public class Pares {
        private var i:int = 0;

        public function siguiente():int {
            i++;
            return 2 * i;
        }

        public static function primeros(n:int):String {
            var p:Pares = new Pares();
            var salida:Array = [];
            for (var k:int = 0; k < n; k++) {
                salida.push(p.siguiente());
            }
            return "pares=" + salida.join("-");
        }
    }
}
```

**Qué reconocer:** Dart marca la función con `sync*` —el asterisco es la marca de generador, igual
que el `function*` de JavaScript— y `yield` la suspende hasta que alguien pida el siguiente valor.
ActionScript 3 se quedó congelado en ECMAScript 4, antes de que llegaran los generadores, así que
muestra el estado del arte anterior: un objeto que guarda `i` y expone `siguiente()`. Comparar los
dos deja a la vista qué hace el compilador cuando ve un `yield`: exactamente esa clase, escrita
por ti.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La JVM no tiene corrutinas en el bytecode, así
que cada lenguaje se inventa su forma de aplazar el cálculo.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toInt()

    val pares = sequence {
        var i = 1
        while (true) {
            yield(2 * i)
            i++
        }
    }

    println("pares=" + pares.take(n).joinToString("-"))
}
```

### Scala

```scala
object Pares extends App {
  val n = scala.io.StdIn.readLine().trim.toInt
  val pares: LazyList[Int] = LazyList.from(1).map(_ * 2)
  println("pares=" + pares.take(n).mkString("-"))
}
```

### Groovy

```groovy
// Groovy no trae secuencias perezosas en el núcleo: el rango se acota antes de recorrerlo.
def n = System.in.text.trim() as int
def pares = (1..n).collect { it * 2 }
println "pares=${pares.join('-')}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [n     (Integer/parseInt (str/trim (read-line)))
      pares (map #(* 2 %) (iterate inc 1))]
  (println (str "pares=" (str/join "-" (take n pares)))))
```

**Qué reconocer:** los cuatro corren sobre la misma máquina y llegan a cuatro respuestas distintas.
Kotlin implementa `sequence { yield(...) }` con corrutinas: el compilador trocea la función en una
máquina de estados. Scala distingue explícitamente `Iterator` (se consume una vez) de `LazyList`
(recuerda lo ya calculado), y aquí usa la segunda. Clojure es el extremo: `(iterate inc 1)` es una
secuencia **infinita** y `map` sobre ella tampoco calcula nada —en Clojure lo perezoso es el
comportamiento por defecto de las secuencias, no una opción que se activa—. Groovy es el único que
no puede: por eso su versión tiene que conocer `n` antes de generar.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). El CLR sí tiene generadores en el lenguaje:
`yield return` genera una máquina de estados que implementa `IEnumerator`.

### F\#

```fsharp
let n = int (stdin.ReadLine().Trim())

// Seq.initInfinite no calcula nada hasta que alguien pide elementos.
let pares = Seq.initInfinite (fun i -> 2 * (i + 1))

pares
|> Seq.take n
|> Seq.map string
|> String.concat "-"
|> printfn "pares=%s"
```

### VB.NET

```vbnet
Imports System
Imports System.Collections.Generic
Imports System.Linq

Module Pares
    Iterator Function ParesInfinitos() As IEnumerable(Of Integer)
        Dim i As Integer = 1
        Do
            Yield 2 * i
            i += 1
        Loop
    End Function

    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Console.WriteLine("pares=" & String.Join("-", ParesInfinitos().Take(n)))
    End Sub
End Module
```

**Qué reconocer:** VB.NET necesita marcar la función con la palabra `Iterator` para que `Yield` sea
legal, mientras C# lo deduce de la presencia de `yield return`; el resultado compilado es el mismo.
F# no usa `yield` aquí porque no le hace falta: `seq` es perezoso de serie y `Seq.initInfinite`
describe una secuencia sin fin que solo se materializa en el `Seq.take`. Fíjate en que en los tres
el bucle es infinito y **nadie se cuelga**: quien decide cuándo parar es el consumidor.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). En C no hay pereza: si quieres producir bajo demanda,
la escribes tú con una variable estática o un puntero a función.

### C++

```cpp
#include <iostream>
#include <ranges>
#include <string>

int main() {
    int n = 0;
    std::cin >> n;

    std::string salida;
    // views::iota(1) es una secuencia infinita perezosa: nada se materializa.
    for (int x : std::views::iota(1)
                     | std::views::transform([](int i) { return 2 * i; })
                     | std::views::take(n)) {
        if (!salida.empty()) salida += '-';
        salida += std::to_string(x);
    }

    std::cout << "pares=" << salida << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        int n = 0;
        scanf("%d", &n);

        // Objective-C no tiene generadores: el estado vive en un bloque con __block.
        __block int i = 0;
        int (^siguiente)(void) = ^int(void) {
            i++;
            return 2 * i;
        };

        NSMutableArray<NSString *> *salida = [NSMutableArray array];
        for (int k = 0; k < n; k++) {
            [salida addObject:[NSString stringWithFormat:@"%d", siguiente()]];
        }
        printf("pares=%s\n", [[salida componentsJoinedByString:@"-"] UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** C++20 introdujo *ranges* y con ellos la pereza que Python tenía desde siempre:
`views::iota(1)` es infinito y la tubería `|` no calcula nada hasta que el `for` tira de ella.
Objective-C se queda en la solución anterior —un bloque con `__block` para que la variable capturada
sea compartida y no copiada—, que es la misma clausura de Perl escrita con corchetes. Los dos
compilan a código sin sorpresas: no hay hilos ni saltos, solo una función que recuerda dónde iba.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Aquí la pereza tiene que
ser gratis: un iterador no puede costar una asignación de memoria por elemento.

### Zig

```zig
const std = @import("std");

// En Zig un iterador es un struct con un método `next()`. No hay azúcar.
const Pares = struct {
    i: u32 = 0,

    fn next(self: *Pares) u32 {
        self.i += 1;
        return 2 * self.i;
    }
};

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(u32, std.mem.trim(u8, linea, " \t\r"), 10);

    const out = std.io.getStdOut().writer();
    var it = Pares{};
    try out.writeAll("pares=");
    var k: u32 = 0;
    while (k < n) : (k += 1) {
        if (k > 0) try out.writeByte('-');
        try out.print("{d}", .{it.next()});
    }
    try out.writeByte('\n');
}
```

### Nim

```nim
import std/strutils

iterator pares(): int {.closure.} =
  var i = 1
  while true:
    yield 2 * i
    inc i

let n = parseInt(stdin.readLine().strip())
var salida: seq[string] = @[]
for p in pares():
  salida.add($p)
  if salida.len == n:
    break
echo "pares=", salida.join("-")
```

### D

```d
import std.stdio, std.range, std.algorithm, std.array, std.conv, std.string;

void main() {
    const n = readln().strip().to!int;
    // iota y map son ranges perezosos: take corta antes de que se calcule nada de más.
    auto pares = iota(1, int.max).map!(i => 2 * i);
    writeln("pares=", pares.take(n).map!(to!string).join("-"));
}
```

**Qué reconocer:** Zig no tiene `yield` ni azúcar de iteradores, y aun así todo su ecosistema itera
igual: un `struct` con `next()`, exactamente el mismo contrato que el trait `Iterator` de Rust, pero
escrito a mano cada vez. Nim sí tiene `yield` real; el `{.closure.}` es lo que permite pasarse el
iterador como valor en vez de que el compilador lo funda con el bucle. D vuelve a su modelo de
*ranges*: `iota` y `map!` no calculan nada, y `take` decide cuántos elementos llegan a existir. En
los tres el coste de la pereza es cero en tiempo de ejecución porque se resuelve al compilar.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Un cursor entrega filas bajo demanda, pero nadie
describe *cómo* se generan.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    % between/3 genera bajo demanda: es el generador perezoso de Prolog.
    findall(P, (between(1, N, I), P is 2 * I), Pares),
    atomic_list_concat(Pares, '-', Salida),
    format("pares=~w~n", [Salida]).
```

### Datalog

```datalog
% Datalog evalúa *bottom-up*: deriva todo lo derivable, nunca bajo demanda.
% Una secuencia infinita no termina, así que hay que acotarla en las propias reglas.
limite(3).

par(2).
par(P) :- par(Q), limite(N), Q < 2 * N, P = Q + 2.
```

**Qué reconocer:** `between(1, N, I)` es el generador perezoso más puro de esta página: no devuelve
una lista, **liga `I` a un valor y, si le pides otra solución, lo reintenta con el siguiente**. Esa
es la pereza de Prolog: backtracking, no secuencias. `findall` es justo lo contrario —fuerza todas
las soluciones a la vez—, igual que hacer `list()` de un generador en Python. Datalog no puede ni
eso: su motor deriva hechos hasta el punto fijo, así que un conjunto infinito no termina y la cota
tiene que estar dentro de la regla.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y tres respuestas distintas a la misma pregunta: quién decide
cuándo se calcula el siguiente valor. Unos tienen `yield` y el compilador construye la máquina de
estados; otros no lo tienen y el estado se guarda a mano en una clausura o un `struct`; unos pocos
—Clojure, Prolog— hacen que aplazar sea el comportamiento por defecto y calcular ya la excepción.
Reconocer cuál de los tres tienes delante es lo transferible.

⏮️ [Volver a la clase 066](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
