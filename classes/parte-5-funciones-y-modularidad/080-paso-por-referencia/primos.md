# 🧬 El mismo programa en las familias de lenguajes — Clase 080

> [⬅️ Volver a la clase 080](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —una función que **sí** modifica la variable del
llamador— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo
por los diez lenguajes del núcleo.

Este es el programa que más divide de toda la parte 5, porque la mitad de los lenguajes **no puede
escribirlo tal cual**: no tienen parámetros por referencia y hay que meter el valor en una caja
mutable. La otra mitad ofrece tres mecanismos distintos —puntero, referencia y alias por nombre— que
conviene no confundir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`
- **Salida** (stdout): `antes=<n> despues=<2n>`
- **Regla:** la función duplica la variable original a través de una referencia

| stdin | esperado |
|---|---|
| `5` | `antes=5 despues=10` |
| `3` | `antes=3 despues=6` |
| `7` | `antes=7 despues=14` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
PHP es el raro de la familia: tiene `&$x` de verdad. Los demás mutan un **contenedor** compartido,
que es el truco que ya viste en la versión Python de la clase.

### Ruby

```ruby
def doblar(caja)
  caja[0] *= 2   # se muta el Array, que sí es compartido; el Integer es inmutable
end

n = STDIN.gets.to_i
antes = n
caja = [n]
doblar(caja)
puts "antes=#{antes} despues=#{caja[0]}"
```

### Perl

```perl
# Perl sí tiene referencias reales: \$n crea una, $$ref la desreferencia.
sub doblar {
    my ($ref) = @_;
    $$ref *= 2;
}

my $n = <STDIN>;
chomp $n;
my $antes = $n;
doblar(\$n);
print "antes=$antes despues=$n\n";
```

### Lua

```lua
local function doblar(caja)
  caja.v = caja.v * 2   -- las tablas se comparten; los números, no
end

local n = io.read("n")
local antes = n
local caja = {v = n}
doblar(caja)
print(string.format("antes=%d despues=%d", antes, caja.v))
```

### Tcl

```tcl
proc doblar {nombre} {
    upvar 1 $nombre v   ;# v pasa a ser un ALIAS de la variable del llamador
    set v [expr {$v * 2}]
}

gets stdin n
set antes $n
doblar n          ;# se pasa el NOMBRE de la variable, no su valor
puts "antes=$antes despues=$n"
```

### R

```r
doblar <- function(e) {
  e$v <- e$v * 2  # los entornos son lo único que R no copia al pasarlo
}

n <- as.integer(readLines("stdin", n = 1))
antes <- n
e <- new.env()
e$v <- n
doblar(e)
cat(sprintf("antes=%d despues=%d\n", antes, e$v))
```

**Qué reconocer:** tres soluciones distintas para el mismo apuro. Ruby, Lua y R usan la **caja**:
como los números son inmutables o se copian, se envuelven en algo que sí se comparte —Array, table,
`environment`—. Perl tiene **referencias de primera clase**: `\$n` es un valor que apunta a la
variable y `$$ref` escribe en ella. Y Tcl hace lo que ningún otro lenguaje de la página: `upvar` no
recibe un valor ni una dirección, recibe el **nombre** de la variable y la enlaza al ámbito del
llamador — paso por nombre, la técnica de Algol 60 viva en un lenguaje de 2024. Fíjate en la llamada:
`doblar n`, sin `$`.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

class Caja {
  int v;
  Caja(this.v);
}

// Dart no tiene parámetros por referencia: se muta el objeto recibido.
void doblar(Caja c) {
  c.v *= 2;
}

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  final c = Caja(n);
  doblar(c);
  print('antes=$n despues=${c.v}');
}
```

### ActionScript 3

```actionscript
package {
    public class Referencia {
        // Sin stdin y sin parámetros por referencia: los objetos, en cambio,
        // llegan como referencia y sus campos sí se pueden modificar.
        public static function doblar(caja:Object):void {
            caja.v = caja.v * 2;
        }

        public static function informe(n:int):String {
            var caja:Object = {v: n};
            doblar(caja);
            return "antes=" + n + " despues=" + caja.v;
        }
    }
}
```

**Qué reconocer:** ninguno de los cuatro lenguajes de esta familia —JS, TS, Dart, AS3— tiene
parámetros por referencia, y no es un olvido: es la consecuencia directa de que **todo se pase por
valor** y de que ese valor sea una referencia cuando el argumento es un objeto. Por eso el patrón
del objeto-caja aparece idéntico en los cuatro. La diferencia entre Dart y AS3 es solo de rigor: AS3
usa un `Object` dinámico con campos improvisados, Dart declara una clase con un campo `int v`
tipado, y el compilador comprueba que existe.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La JVM **no tiene** paso por referencia: no
existe ningún bytecode que reciba la dirección de una variable local.

### Kotlin

```kotlin
class Caja(var v: Int)

fun doblar(c: Caja) {   // Kotlin no tiene `ref`: se muta una propiedad `var`
    c.v *= 2
}

fun main() {
    val n = readLine()!!.trim().toInt()
    val c = Caja(n)
    doblar(c)
    println("antes=$n despues=${c.v}")
}
```

### Scala

```scala
object Referencia {
  class Caja(var v: Int)

  def doblar(c: Caja): Unit = c.v *= 2

  def main(args: Array[String]): Unit = {
    val n = scala.io.StdIn.readLine().trim.toInt
    val c = new Caja(n)
    doblar(c)
    println(s"antes=$n despues=${c.v}")
  }
}
```

### Groovy

```groovy
class Caja { int v }

def doblar(Caja c) { c.v *= 2 }

def n = System.in.newReader().readLine().trim().toInteger()
def c = new Caja(v: n)
doblar(c)
println "antes=$n despues=${c.v}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

; El estado mutable no vive en una variable sino en un atom, y se cambia
; con swap!, que además es seguro entre hilos.
(defn doblar! [a] (swap! a * 2))

(let [n (Integer/parseInt (str/trim (read-line)))
      caja (atom n)]
  (doblar! caja)
  (println (str "antes=" n " despues=" @caja)))
```

**Qué reconocer:** los cuatro repiten la caja, porque la limitación no es del lenguaje sino de la
**máquina virtual**. Kotlin y Scala añaden un detalle importante: el campo tiene que declararse `var`
—si fuera `val`, la caja tampoco serviría—, así que la mutabilidad se ve escrita en el tipo. Clojure
es el que más enseña: no niega la mutación, la **aísla** en un `atom`, y el `swap!` con `!` final
avisa al lector de que hay efecto. Donde los demás disfrazan la referencia de objeto, Clojure la
llama por su nombre: una identidad con estado, separada del valor que contiene.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). El CLR **sí** admite referencias gestionadas
(`&` en IL), así que aquí el paso por referencia es de verdad, no un objeto disfrazado.

### F\#

```fsharp
let doblar (x: byref<int>) = x <- x * 2

[<EntryPoint>]
let main _ =
    let mutable n = int (stdin.ReadLine().Trim())   // `mutable` es obligatorio
    let antes = n
    doblar &n
    printfn "antes=%d despues=%d" antes n
    0
```

### VB.NET

```vbnet
Module Referencia
    Sub Doblar(ByRef x As Integer)
        x = x * 2
    End Sub

    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Dim antes = n
        Doblar(n)   ' sin marca en la llamada: no se ve que sea por referencia
        Console.WriteLine($"antes={antes} despues={n}")
    End Sub
End Module
```

**Qué reconocer:** los tres generan el mismo IL con una referencia gestionada, pero difieren en algo
que importa al leer código ajeno: **si la llamada avisa**. C# obliga a escribir `Doblar(ref n)` y F#
exige `&n`, de modo que en el punto de llamada se ve que la variable puede cambiar. VB.NET no marca
nada —`Doblar(n)` es idéntico a una llamada por valor—, herencia de VB6, donde `ByRef` era el
defecto. F# añade su propia fricción: el paso por referencia solo funciona sobre una variable
declarada `mutable`, y el lenguaje prefiere que devuelvas un valor nuevo en vez de esto.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). C **no tiene** paso por referencia: tiene punteros, y
el `&n` de la llamada es el propio programador tomando la dirección.

### C++

```cpp
#include <iostream>

void doblar(long& x) {   // referencia: un ALIAS de la variable, no un puntero
    x *= 2;              // sin `*` para desreferenciar y sin posibilidad de ser nula
}

int main() {
    long n;
    std::cin >> n;
    const long antes = n;
    doblar(n);           // la llamada no lleva marca: no se ve que n vaya a cambiar
    std::cout << "antes=" << antes << " despues=" << n << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

// Objective-C no añadió las referencias de C++: solo punteros, como en C.
// Y un objeto siempre se recibe por puntero, así que sus métodos mutadores
// (por ejemplo sobre NSMutableArray) ya afectan al original.
static void doblar(long *p) {
    *p *= 2;
}

int main(void) {
    @autoreleasepool {
        long n;
        if (scanf("%ld", &n) != 1) return 1;
        long antes = n;
        doblar(&n);
        printf("antes=%ld despues=%ld\n", antes, n);
    }
    return 0;
}
```

**Qué reconocer:** aquí está la distinción más fina de la página. C++ es el único lenguaje del núcleo
y de sus primos que tiene **las dos cosas**: el puntero heredado de C (`long*`, reasignable, puede
ser nulo, se desreferencia con `*`) y la **referencia** (`long&`, alias permanente, nunca nula, se
usa como si fuera la variable). A eso añade una tercera vía que no existe en C: `const long&`, que
evita la copia **sin** conceder permiso de escritura — la forma normal de pasar objetos grandes.
Objective-C se quedó exactamente donde estaba C, y por eso su código pasa direcciones con `&` a la
vista.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Go usa punteros
explícitos; Rust convierte la referencia mutable en el centro de su sistema de tipos (clase 081).

### Zig

```zig
const std = @import("std");

fn doblar(p: *i64) void {   // Zig no tiene referencias: puntero explícito, como Go
    p.* *= 2;
}

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r"), 10);
    const antes = n;
    doblar(&n);
    try std.io.getStdOut().writer().print("antes={d} despues={d}\n", .{ antes, n });
}
```

### Nim

```nim
import std/[strutils, strformat]

proc doblar(x: var int) =   # `var` en el parámetro = paso por referencia
  x = x * 2

var n = stdin.readLine().strip().parseInt()
let antes = n
doblar(n)   # la llamada no cambia: la marca está en la firma
echo &"antes={antes} despues={n}"
```

### D

```d
import std.stdio, std.conv, std.string;

void doblar(ref long x) {
    x *= 2;
}

void main() {
    long n = readln().strip().to!long;
    const antes = n;
    doblar(n);
    writefln("antes=%d despues=%d", antes, n);
}
```

**Qué reconocer:** Zig se planta con Go y C: **solo punteros**, `p.*` para desreferenciar y `&n` en
la llamada, porque prefiere que cada indirección se vea. Nim y D sí tienen paso por referencia de
verdad (`var` y `ref`), y comparten con VB.NET el mismo inconveniente: la llamada es
`doblar(n)`, indistinguible de una por valor, así que hay que ir a la firma para saber si la
variable sobrevive intacta. El caso de Nim es doblemente interesante porque `var` es exactamente la
misma palabra que usa para declarar variables mutables — el lenguaje trata "mutable" y "por
referencia" como el mismo permiso.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). No hay variables del llamador, así que no hay
nada a lo que apuntar.

### Prolog

```prolog
:- initialization(main, main).

% Aquí NO hay parámetros de entrada y de salida: hay argumentos que se unifican.
% Despues no se "escribe": se liga. Y el mismo predicado se podría consultar al
% revés, dando Despues y preguntando por Antes.
doblar(Antes, Despues) :- Despues is Antes * 2.

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    doblar(N, Despues),
    format("antes=~d despues=~d~n", [N, Despues]).
```

### Datalog

```datalog
% Sin mutación, sin efectos y sin E/S: 'despues' es otra columna del hecho derivado.
num(5).

doblado(N, D) :- num(N), D = N * 2.
```

**Qué reconocer:** esta familia responde a la clase negando la pregunta. En Prolog un argumento **no
es de entrada ni de salida**: es un hueco que se unifica, y su dirección la decide qué variables
llegan ya ligadas en cada llamada. Eso da algo que ningún lenguaje imperativo tiene —el mismo
predicado sirve para calcular y para comprobar—, a cambio de perder por completo la idea de "la
variable del llamador cambió". Datalog llega al final del camino: relaciones puras, sin estado que
modificar, igual que un `SELECT` que jamás toca la fila que lee.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y cuatro respuestas: **puntero** (C, Objective-C, Go, Zig),
**referencia o `ByRef`** (C++, C#, F#, VB.NET, Nim, D, Rust), **alias por nombre** (Tcl con `upvar`)
y **caja mutable** para todos los que no tienen ninguno de los tres (JS, Dart, Java, Kotlin, Scala,
Ruby, Lua, Python). Y una pregunta práctica que conviene hacerse siempre al leer código ajeno: ¿la
**llamada** avisa de que la variable puede cambiar, o hay que ir a mirar la firma? Eso es lo
transferible.

⏮️ [Volver a la clase 080](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
