# 🧬 El mismo programa en las familias de lenguajes — Clase 110

> [⬅️ Volver a la clase 110](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —crear un `Contador`, incrementarlo `n` veces y
mostrar su estado— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Un contador es el objeto más pequeño que existe: un dato que solo se toca a través de un método. Y
precisamente por ser tan pequeño deja al descubierto lo que cada familia entiende por "objeto". Aquí
verás clases nativas, clases fabricadas con tablas, clases añadidas veinte años tarde, envío de
mensajes en lugar de llamada a método, y dos lenguajes que directamente no tienen estado que
guardar.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`, el número de incrementos
- **Salida** (stdout): `cuenta=<n>`
- **Regla:** un contador que arranca en 0 y se incrementa `n` veces

| stdin | esperado |
|---|---|
| `5` | `cuenta=5` |
| `0` | `cuenta=0` |
| `3` | `cuenta=3` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La familia donde más se nota la diferencia entre nacer orientado a objetos y añadirlo después.

### Ruby

```ruby
class Contador
  attr_reader :cuenta

  def initialize
    @cuenta = 0
  end

  def incrementar
    @cuenta += 1
  end
end

n = STDIN.gets.to_i
c = Contador.new
n.times { c.incrementar }
puts "cuenta=#{c.cuenta}"
```

### Perl

```perl
package Contador;

sub new {
    my ($class) = @_;
    my $self = { cuenta => 0 };
    return bless $self, $class;
}

sub incrementar { $_[0]{cuenta}++ }
sub cuenta      { $_[0]{cuenta} }

package main;

my $n = <STDIN>;
my $c = Contador->new;
$c->incrementar for 1 .. $n;
print "cuenta=", $c->cuenta, "\n";
```

### Lua

```lua
-- Lua no tiene clases: una tabla hace de plantilla y `__index` redirige a ella
-- las búsquedas de método que fallan en la instancia.
local Contador = {}
Contador.__index = Contador

function Contador.new()
  return setmetatable({ cuenta = 0 }, Contador)
end

function Contador:incrementar()
  self.cuenta = self.cuenta + 1
end

local n = tonumber(io.read("l"))
local c = Contador.new()
for _ = 1, n do
  c:incrementar()
end
print("cuenta=" .. c.cuenta)
```

### Tcl

```tcl
oo::class create Contador {
    variable cuenta
    constructor {} { set cuenta 0 }
    method incrementar {} { incr cuenta }
    method cuenta {} { return $cuenta }
}

gets stdin n
set c [Contador new]
for {set i 0} {$i < $n} {incr i} { $c incrementar }
puts "cuenta=[$c cuenta]"
```

### R

```r
Contador <- setRefClass("Contador",
  fields = list(cuenta = "numeric"),
  methods = list(
    initialize = function() {
      cuenta <<- 0
    },
    incrementar = function() {
      cuenta <<- cuenta + 1
    }
  )
)

n <- as.integer(readLines("stdin", n = 1))
c <- Contador$new()
for (i in seq_len(n)) c$incrementar()
cat(sprintf("cuenta=%d\n", as.integer(c$cuenta)))
```

**Qué reconocer:** aquí está el reparto completo de posturas ante los objetos. Ruby es **orientado a
objetos puro**, al estilo de Smalltalk: no hay tipos primitivos, todo es objeto, y `n.times` funciona
porque `n` —un entero— también lo es y tiene métodos. Perl añadió los objetos tarde y sin cambiar el
lenguaje: un objeto es una **referencia bendecida** con `bless`, es decir, un hash normal al que se le
marca a qué paquete pertenece para que `->` sepa dónde buscar la subrutina. Se ve la costura. Lua es
el caso más instructivo: **no tiene clases en absoluto**; hay tablas y metatablas, y el mecanismo de
objetos se construye a mano con `__index`, que es lo que convierte `c:incrementar()` en
`Contador.incrementar(c)`. Tcl tuvo el mismo problema y lo resolvió al revés, añadiendo TclOO al
núcleo del lenguaje en la versión 8.6. Y R arrastra tres sistemas de objetos incompatibles: S3, S4 y
las *reference classes* de este ejemplo, las únicas con **estado mutable compartido**, porque en las
otras dos modificar un objeto devuelve una copia.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

class Contador {
  int cuenta = 0;
  void incrementar() => cuenta++;
}

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  final c = Contador();
  for (var i = 0; i < n; i++) c.incrementar();
  print('cuenta=${c.cuenta}');
}
```

### ActionScript 3

```actionscript
// Sin stdin en el reproductor Flash: se ilustra la clase y su estado.
package {
    public class Contador {
        private var _cuenta:int = 0;

        public function incrementar():void {
            _cuenta++;
        }

        public function get cuenta():int {
            return _cuenta;
        }
    }
}
```

**Qué reconocer:** los dos escriben `class` con campos y métodos, igual que el JavaScript moderno de
la clase. La diferencia con su representante es de **fondo, no de forma**: en JavaScript esa `class`
es azúcar sobre prototipos, y en Dart y ActionScript 3 es una clase real con su tipo comprobado en
compilación. ActionScript 3 añade lo que JavaScript nunca tuvo: `private` de verdad y propiedades con
`get`, que dejan leer `c.cuenta` mientras el campo `_cuenta` sigue siendo inaccesible desde fuera. Ese
control de acceso —encapsulación aplicada por el lenguaje— es una de las piezas que esta clase pone
sobre la mesa.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La plataforma que hizo de las clases la unidad
obligatoria de todo, y los primos que se apartaron de ella.

### Kotlin

```kotlin
class Contador {
    var cuenta = 0
        private set

    fun incrementar() {
        cuenta++
    }
}

fun main() {
    val n = readLine()!!.trim().toInt()
    val c = Contador()
    repeat(n) { c.incrementar() }
    println("cuenta=${c.cuenta}")
}
```

### Scala

```scala
class Contador {
  private var estado = 0
  def incrementar(): Unit = estado += 1
  def cuenta: Int = estado
}

object Main extends App {
  val n = scala.io.StdIn.readLine().trim.toInt
  val c = new Contador
  (1 to n).foreach(_ => c.incrementar())
  println(s"cuenta=${c.cuenta}")
}
```

### Groovy

```groovy
class Contador {
    int cuenta = 0

    void incrementar() { cuenta++ }
}

def n = System.in.newReader().readLine().trim() as int
def c = new Contador()
n.times { c.incrementar() }
println "cuenta=${c.cuenta}"
```

### Clojure

```clojure
;; Clojure no tiene clases con estado mutable. Lo más cercano es un átomo:
;; una referencia identificada cuyo valor solo cambia mediante `swap!`.
(let [n (Integer/parseInt (.trim (read-line)))
      contador (atom 0)]
  (dotimes [_ n] (swap! contador inc))
  (println (str "cuenta=" @contador)))
```

**Qué reconocer:** Kotlin, Scala y Groovy escriben la clase de Java con menos ceremonia —Groovy genera
el *getter* solo, Kotlin lo declara con `private set`— pero el modelo es idéntico: un objeto es un
paquete de estado con métodos que lo modifican. Clojure, en la misma máquina virtual, **se niega**:
no hay campo que reasignar. Lo que ofrece es un átomo, una caja que separa la **identidad** (el
contador) del **valor** (0, 1, 2...), y cada cambio produce un valor nuevo aplicando una función. El
resultado impreso es el mismo `cuenta=5`, pero el concepto central de esta clase —el estado que un
objeto guarda y muta— no existe en el programa de Clojure. Es la diferencia paradigmática en su forma
más clara: no se trata de escribir distinto, se trata de que el objeto no es la herramienta.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
// F# tiene las clases del CLR, pero el campo hay que declararlo `mutable`
// y la reasignación se escribe con `<-`, no con `=`.
type Contador() =
    let mutable cuenta = 0
    member _.Incrementar() = cuenta <- cuenta + 1
    member _.Cuenta = cuenta

let n = stdin.ReadLine().Trim() |> int
let c = Contador()
for _ in 1 .. n do
    c.Incrementar()
printfn "cuenta=%d" c.Cuenta
```

### VB.NET

```vbnet
Class Contador
    Private _cuenta As Integer = 0

    Public Sub Incrementar()
        _cuenta += 1
    End Sub

    Public ReadOnly Property Cuenta As Integer
        Get
            Return _cuenta
        End Get
    End Property
End Class

Module Programa
    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Dim c As New Contador()
        For i = 1 To n
            c.Incrementar()
        Next
        Console.WriteLine("cuenta=" & c.Cuenta)
    End Sub
End Module
```

**Qué reconocer:** los dos producen la misma clase del CLR, con su campo privado y su propiedad de
solo lectura, y en tiempo de ejecución son indistinguibles. La diferencia está en qué considera cada
uno el caso normal. VB.NET presenta la clase con estado como el modo natural de programar. F# la
admite, pero pone dos avisos por escrito —`mutable` y `<-`— para que quede claro que estás saliendo
del terreno inmutable; su equivalente idiomático sería un valor y una función, sin objeto ninguno.
Cuando dos lenguajes comparten runtime y biblioteca, lo único que los separa es qué hacen fácil.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). C no tiene objetos: un `struct` y funciones que lo
reciben por puntero. Sus dos descendientes añadieron objetos por caminos opuestos.

### C++

```cpp
#include <iostream>

class Contador {
public:
    void incrementar() { ++cuenta_; }
    int cuenta() const { return cuenta_; }

private:
    int cuenta_ = 0;
};

int main() {
    int n = 0;
    std::cin >> n;
    Contador c;
    for (int i = 0; i < n; ++i) c.incrementar();
    std::cout << "cuenta=" << c.cuenta() << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

@interface Contador : NSObject
@property (nonatomic, readonly) NSInteger cuenta;
- (void)incrementar;
@end

@implementation Contador
- (void)incrementar {
    _cuenta += 1;
}
@end

int main(void) {
    @autoreleasepool {
        long n = 0;
        scanf("%ld", &n);
        Contador *c = [Contador new];
        for (long i = 0; i < n; i++) [c incrementar];
        printf("cuenta=%ld\n", (long)c.cuenta);
    }
    return 0;
}
```

**Qué reconocer:** C++ tomó los objetos de Simula: la llamada `c.incrementar()` se resuelve en
compilación, el objeto vive en la pila y el compilador sabe exactamente qué código va a ejecutarse.
Objective-C tomó los de Smalltalk, y `[c incrementar]` **no es una llamada a método**: es el **envío
de un mensaje**, resuelto en ejecución por `objc_msgSend`, que busca el selector en la tabla de la
clase. La consecuencia es visible: un objeto de Objective-C puede recibir un mensaje que nadie
implementó y decidir en ese momento qué hacer con él —reenviarlo a otro objeto, responder que no lo
entiende— y sobre ese mecanismo se construyeron las categorías, el *key-value observing* y buena parte
de Cocoa. Dos lenguajes con la misma base C y dos linajes de orientación a objetos que nunca se
tocaron.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Ninguno de los dos tiene
clases: tienen datos y métodos asociados a un tipo.

### Zig

```zig
const std = @import("std");

// Zig no tiene clases ni herencia: un struct y funciones que reciben `*Contador`.
// El `self` es un parámetro explícito, no algo que el lenguaje pase por detrás.
const Contador = struct {
    cuenta: u64 = 0,

    fn incrementar(self: *Contador) void {
        self.cuenta += 1;
    }
};

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(u64, std.mem.trim(u8, linea, " \r"), 10);
    var c = Contador{};
    var i: u64 = 0;
    while (i < n) : (i += 1) c.incrementar();
    try std.io.getStdOut().writer().print("cuenta={d}\n", .{c.cuenta});
}
```

### Nim

```nim
import std/strutils

type Contador = object
  cuenta: int

proc incrementar(c: var Contador) =
  c.cuenta += 1

let n = stdin.readLine().strip().parseInt()
var c = Contador(cuenta: 0)
for _ in 1 .. n:
  c.incrementar()
echo "cuenta=", c.cuenta
```

### D

```d
import std.stdio, std.string, std.conv;

class Contador {
    private int cuenta_ = 0;

    void incrementar() { cuenta_++; }

    int cuenta() const { return cuenta_; }
}

void main() {
    const n = readln().strip().to!int;
    auto c = new Contador();
    foreach (_; 0 .. n) c.incrementar();
    writefln("cuenta=%d", c.cuenta);
}
```

**Qué reconocer:** D sí tiene clases completas, con herencia y recolección de basura, porque nació
como "un C++ mejor"; sus objetos se crean con `new` y viven en el montón. Zig y Nim se quedan en el
`struct` con funciones asociadas, igual que Go y Rust: en Nim, `c.incrementar()` es puro azúcar para
`incrementar(c)` —cualquier función cuyo primer parámetro sea del tipo puede escribirse así— y en Zig
el `self` aparece escrito como parámetro, sin nada implícito. La lección es que "método" y "función
que recibe el dato" pueden ser lo mismo, y que la encapsulación no exige una palabra `class`.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Ni objetos, ni métodos, ni estado.

### Prolog

```prolog
:- initialization(main, main).

% Prolog no tiene objetos ni estado que mutar: no existe un "contador" que
% guarde su valor. El estado viaja como argumento, y cada paso liga una
% variable nueva en vez de modificar la anterior.
contar(0, C, C).
contar(N, C0, C) :- N > 0, M is N - 1, C1 is C0 + 1, contar(M, C1, C).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    contar(N, 0, C),
    format("cuenta=~d~n", [C]).
```

### Datalog

```datalog
// Datalog no tiene objetos, ni estado, ni E/S. Lo más cercano a "contar" es
// derivar los pasos como hechos y quedarse con el mayor.
.decl paso(i:number)
paso(0).
paso(i + 1) :- paso(i), i < 5.

.decl cuenta(c:number)
cuenta(c) :- c = max i : { paso(i) }.
```

**Qué reconocer:** este es el contraste más fuerte de toda la parte, y conviene decirlo sin rodeos:
en Prolog y Datalog **no hay objetos porque no hay estado**. Una variable se liga una vez y no vuelve
a cambiar, así que un contador no puede existir como cosa que se guarda y se modifica; lo que hay es
`contar(N, C0, C)`, donde el valor actual entra por un argumento y el siguiente sale por otro. Todo
lo que esta clase enseña —encapsular un dato, exponerlo por métodos, mutarlo de forma controlada— se
desvanece. Datalog lo lleva al límite: ni siquiera puede leer un `n`, y el `5` está escrito en la
regla. Ver un paradigma donde el concepto central de la clase simplemente no aplica es la mejor
manera de entender que las clases son **una** solución al problema de organizar estado, no *la*
solución.

---

## Y de vuelta a la clase

Veinte lenguajes y un contador de dos líneas conceptuales. Casi todos lo resuelven con un objeto que
guarda su estado, pero por caminos que no se parecen: clases nativas, tablas con metatablas,
referencias bendecidas, mensajes resueltos en ejecución. Tres se salen del molde —Clojure con un
valor que se sustituye, Prolog y Datalog sin estado ninguno— y F# se queda en la frontera, admitiendo
la clase pero obligándote a firmar la mutación. Eso es lo que hay que llevarse: la orientación a
objetos es una decisión de diseño con alternativas reales.

⏮️ [Volver a la clase 110](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
