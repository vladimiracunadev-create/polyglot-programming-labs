# 🧬 El mismo programa en las familias de lenguajes — Clase 113

> [⬅️ Volver a la clase 113](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —un objeto con un método `doble()`— resuelto por los
**primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez lenguajes del
núcleo.

Esta es la clase donde la comparación paga mejor, porque el modelo de prototipos de JavaScript se
suele contar como una rareza suya. No lo es: **Lua hace exactamente lo mismo** con la metatabla
`__index`, aunque su sintaxis no se parezca en nada. Ver los dos juntos convierte "el prototipo" de
peculiaridad histórica en lo que realmente es —una forma general de resolver métodos por delegación
en ejecución—.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`
- **Salida** (stdout): `resultado=<2n>`
- **Regla:** el objeto guarda `n` y su método `doble()` devuelve `n · 2`

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `7` | `resultado=14` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
El objeto se construye en ejecución y sus miembros se buscan por nombre. Aquí es donde vive el primo
más importante de esta clase.

### Ruby

```ruby
# Ruby no tiene prototipos, pero sí clase singleton: cada objeto puede tener
# métodos propios, y `clone` copia también esa clase singleton (`dup` no).
prototipo = Object.new
prototipo.define_singleton_method(:doble) { @valor * 2 }

obj = prototipo.clone
obj.instance_variable_set(:@valor, STDIN.gets.to_i)
puts "resultado=#{obj.doble}"
```

### Perl

```perl
use strict;
use warnings;

# En Perl la "clase" es solo el nombre del paquete donde se buscan los métodos,
# y @ISA es la cadena por la que se sigue buscando: delegación, no copia.
package Prototipo;
sub doble { my ($s) = @_; return $s->{valor} * 2 }

package main;
chomp(my $n = <STDIN>);
my $obj = bless { valor => $n }, 'Prototipo';
printf "resultado=%d\n", $obj->doble;
```

### Lua

```lua
-- Este ES el modelo de prototipos de JavaScript, con otra sintaxis: `__index`
-- apunta al objeto del que se heredan los métodos, igual que el enlace interno
-- que devuelve `Object.getPrototypeOf` en JS. Y `self` es el mismo `this`.
local prototipo = {}
function prototipo:doble()
  return self.valor * 2
end

local obj = setmetatable({ valor = tonumber(io.read("l")) }, { __index = prototipo })
print("resultado=" .. obj:doble())
```

### Tcl

```tcl
package require TclOO

# `oo::objdefine` da métodos a un objeto concreto sin tocar ninguna clase: es lo
# más cerca que llega Tcl de un objeto con miembros propios.
oo::object create obj
oo::objdefine obj {
    variable valor
    method fijar {v} { set valor $v }
    method doble {} { expr {$valor * 2} }
}

gets stdin n
obj fijar [string trim $n]
puts "resultado=[obj doble]"
```

### R

```r
# Los entornos de R delegan al entorno padre igual que un objeto delega a su
# prototipo: `obj` no tiene `doble`, así que la búsqueda sube a `prototipo`.
prototipo <- new.env()
prototipo$doble <- function(o) o$valor * 2

obj <- new.env(parent = prototipo)
obj$valor <- as.integer(readLines("stdin", n = 1))
cat(sprintf("resultado=%d\n", get("doble", envir = obj)(obj)))
```

**Qué reconocer:** aquí está la comparación que da sentido a la clase. **Lua es prototípico en el
mismo sentido exacto que JavaScript**: `obj` no contiene `doble`, y cuando se pide, la búsqueda
falla en la tabla y salta a `__index` —el mismo salto que hace JavaScript al prototipo interno—; los
dos pasan el receptor como `self`/`this`, y en los dos se puede cambiar el prototipo de un objeto ya
creado. R es el segundo caso genuino: sus entornos forman una cadena de padres, y `get` con
`inherits = TRUE` la recorre. Ruby y Tcl llegan por otra vía —métodos que pertenecen a *un* objeto y
no a su clase—, que es la mitad de la idea; les falta la otra mitad, la delegación en cadena. Perl
es el más engañoso: `@ISA` parece herencia clásica, pero la búsqueda se hace **en ejecución**, así
que reasignar `@ISA` en mitad del programa cambia de dónde vienen los métodos.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

// Dart nació para reemplazar a JavaScript y descartó los prototipos a propósito:
// solo clases, resueltas en compilación.
class Obj {
  final int valor;
  Obj(this.valor);
  int doble() => valor * 2;
}

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  print('resultado=${Obj(n).doble()}');
}
```

### ActionScript 3

```actionscript
// AS3 desciende de ECMAScript: hasta AS2 la herencia era por `prototype`, igual
// que en JavaScript. AS3 pasó a clases; `dynamic` conserva el resto de la idea,
// permitir campos nuevos en ejecución. No hay stdin: se ilustra el objeto.
package {
    public dynamic class Obj {
        public var valor:int;
        public function Obj(valor:int) { this.valor = valor; }
        public function doble():int { return valor * 2; }
    }
}
```

**Qué reconocer:** los dos son parientes directos de JavaScript y los dos **abandonaron el
prototipo**, lo que dice mucho sobre cómo se juzgó el modelo desde dentro de su propia familia.
ActionScript 3 es el testimonio más claro: AS1 y AS2 eran prototípicos por ser dialectos de
ECMAScript, y AS3 los convirtió en clases selladas por rendimiento y comprobación estática, dejando
solo `dynamic` como resto de la flexibilidad antigua. Dart hizo lo mismo desde el primer día. La
lección para el alumno es que `class` en JavaScript es **azúcar sobre el prototipo** —sigue habiendo
delegación debajo—, mientras que en Dart y AS3 la clase es real y no hay cadena que recorrer.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La JVM resuelve los métodos por la clase del
objeto; no existe forma de dar un método a una instancia concreta.

### Kotlin

```kotlin
// Sin prototipos: lo más cercano es un objeto anónimo, que declara miembros
// propios sin necesidad de una clase con nombre.
fun main() {
    val n = readLine()!!.trim().toInt()
    val obj = object {
        val valor = n
        fun doble() = valor * 2
    }
    println("resultado=${obj.doble()}")
}
```

### Scala

```scala
import scala.language.reflectiveCalls

object Prototipos extends App {
  val n = scala.io.StdIn.readLine().trim.toInt
  // Tipo estructural: el tipo del objeto es "algo que tiene `doble`".
  val obj = new {
    val valor = n
    def doble: Int = valor * 2
  }
  println(s"resultado=${obj.doble}")
}
```

### Groovy

```groovy
// `Expando` construye un objeto sin clase, con propiedades y closures como
// métodos: es lo más parecido a un objeto de JavaScript en toda la JVM.
def obj = new Expando(valor: System.in.newReader().readLine().trim() as int)
obj.doble = { -> obj.valor * 2 }
println "resultado=${obj.doble()}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; No hay objetos con métodos: un mapa guarda la función junto al dato, y
;; `(:doble obj)` la recupera igual que se recupera un campo cualquiera.
(let [n (Integer/parseInt (str/trim (read-line)))
      prototipo {:doble (fn [o] (* (:valor o) 2))}
      obj (assoc prototipo :valor n)]
  (println (str "resultado=" ((:doble obj) obj))))
```

**Qué reconocer:** los cuatro rodean la limitación de la JVM por caminos distintos y ninguno consigue
un prototipo de verdad. Kotlin y Scala crean un tipo **anónimo pero fijo**: el objeto tiene miembros
propios, sí, pero se decidieron en compilación y no pueden cambiar después —la diferencia esencial
con JavaScript—. Groovy es el que más se acerca: un `Expando` acepta propiedades nuevas en cualquier
momento y una closure guardada en una propiedad se invoca como método, que es literalmente cómo se
comporta un objeto JS. Clojure enseña el mecanismo desnudo: si un objeto es un mapa y un método es
un valor guardado en él, entonces `(:doble obj)` **es** la búsqueda de propiedad de JavaScript, y
`assoc` sobre el prototipo es la delegación hecha copia explícita.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
// .NET no tiene prototipos. Las expresiones de objeto de F# implementan un tipo
// al vuelo, pero ese tipo debe estar declarado de antemano.
type IObj =
    abstract member Doble: unit -> int

let n = int (stdin.ReadLine().Trim())

let obj =
    { new IObj with
        member _.Doble() = n * 2 }

printfn "resultado=%d" (obj.Doble())
```

### VB.NET

```vbnet
' Un tipo anónimo de VB.NET es una clase real que genera el compilador: puede
' llevar datos, pero no métodos, y no admite miembros nuevos después.
Module Programa
    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Dim obj = New With {.Valor = n}
        Console.WriteLine("resultado=" & (obj.Valor * 2))
    End Sub
End Module
```

**Qué reconocer:** el CLR es el entorno más hostil de los siete al modelo de prototipos, porque cada
objeto lleva un puntero a una tabla de tipo fija desde su creación. La expresión de objeto de F# se
parece mucho a un literal de JavaScript, pero la semejanza es superficial: **necesita una interfaz
declarada antes** y no puede inventar el método `Doble` sobre la marcha. El tipo anónimo de VB.NET es
todavía más limitado —solo propiedades, y de solo lectura—. Lo que .NET ofrece a cambio es lo
contrario de un prototipo: comprobación estática total y llamadas sin ninguna búsqueda en ejecución.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). En C un "objeto" es una `struct` y un "método" un
puntero a función guardado dentro: la búsqueda dinámica hay que escribirla a mano.

### C++

```cpp
#include <iostream>

// C++ resuelve los miembros en compilación: no hay cadena que consultar en
// ejecución, y no se le puede añadir un método a un objeto concreto.
struct Obj {
    int valor;
    int doble() const { return valor * 2; }
};

int main() {
    int n;
    std::cin >> n;
    const Obj obj{n};
    std::cout << "resultado=" << obj.doble() << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>
#import <objc/runtime.h>

// Objective-C busca el método en ejecución, no en compilación: `class_addMethod`
// añade `doble` a la clase con el programa ya arrancado.
static int doble(id self, SEL _cmd) {
    return [[self valueForKey:@"valor"] intValue] * 2;
}

@interface Obj : NSObject
@property int valor;
@end
@implementation Obj
@end

int main(void) {
    @autoreleasepool {
        int n = 0;
        scanf("%d", &n);
        class_addMethod([Obj class], @selector(doble), (IMP)doble, "i@:");
        Obj *obj = [Obj new];
        obj.valor = n;
        int r = ((int (*)(id, SEL))objc_msgSend)(obj, @selector(doble));
        printf("resultado=%d\n", r);
    }
    return 0;
}
```

**Qué reconocer:** dos lenguajes que compilan a código nativo y que están en extremos opuestos de
esta clase. C++ decide en compilación quién responde a `doble()`, y ni siquiera `virtual` cambia eso
—la tabla existe, pero se construye al compilar y nadie la modifica después—. Objective-C hace lo que
JavaScript: envía un **mensaje** y busca el método en ejecución, con la posibilidad de añadirlo,
sustituirlo (`method_swizzling`) o redirigirlo a otro objeto si no existe (`forwardingTargetFor`).
Ese último mecanismo es delegación pura, la misma idea que el prototipo, y explica por qué la
comunidad de Objective-C entiende de inmediato el modelo de JS aunque venga de la familia de C.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). El coste de cada
operación es visible, y una búsqueda de método por nombre en ejecución tiene un coste que estos
lenguajes prefieren no pagar.

### Zig

```zig
const std = @import("std");

// Zig no tiene despacho dinámico implícito ni prototipos: tipos y funciones se
// resuelven por completo en tiempo de compilación.
const Obj = struct {
    valor: i64,

    fn doble(self: Obj) i64 {
        return self.valor * 2;
    }
};

pub fn main() !void {
    var buf: [32]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r\n"), 10);
    const obj = Obj{ .valor = n };
    try std.io.getStdOut().writer().print("resultado={d}\n", .{obj.doble()});
}
```

### Nim

```nim
import std/strutils

# Nim usa UFCS: `obj.doble` es azúcar para `doble(obj)`. El método no vive dentro
# del objeto, así que no hay nada de lo que heredarlo por delegación.
type Obj = object
  valor: int

func doble(o: Obj): int = o.valor * 2

let obj = Obj(valor: parseInt(stdin.readLine().strip()))
echo "resultado=", obj.doble
```

### D

```d
import std.stdio, std.string, std.conv;

// `opDispatch` intercepta cualquier nombre de miembro que no exista: es la vía
// de D para imitar la búsqueda dinámica de un prototipo, pero resuelta en
// compilación, así que un nombre desconocido es un error de compilación.
struct Obj {
    int valor;

    int opDispatch(string nombre)() {
        static assert(nombre == "doble", "el prototipo no define ese método");
        return valor * 2;
    }
}

void main() {
    auto obj = Obj(readln().strip().to!int);
    writeln("resultado=", obj.doble);
}
```

**Qué reconocer:** los tres demuestran que se puede tener la **sintaxis** de un objeto con métodos
sin nada del mecanismo. Nim lo enseña mejor que ninguno: `obj.doble` es solo otra forma de escribir
`doble(obj)`, así que el punto no significa "busca dentro del objeto" sino "busca una función que
acepte este tipo" —y por eso no hay prototipo que consultar—. D es el más ingenioso: `opDispatch`
atrapa nombres inexistentes igual que el `Proxy` de JavaScript, pero se resuelve al compilar, de modo
que un nombre inesperado no falla en ejecución sino en la compilación. Zig ni lo intenta: sin
metaprogramación de nombres, sin búsqueda, sin coste oculto.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). No hay objetos: hay hechos y reglas, y la
delegación se escribe como una relación más entre ellos.

### Prolog

```prolog
:- initialization(main, main).

% No hay objetos ni métodos: el objeto es un término y la delegación al prototipo
% es una regla que consulta otro hecho.
factor(prototipo, 2).
delega(obj, prototipo).

doble(Objeto, Valor, R) :- delega(Objeto, P), factor(P, F), R is Valor * F.

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    doble(obj, N, R),
    format("resultado=~w~n", [R]).
```

### Datalog

```datalog
% Datalog no tiene E/S ni objetos: se declara el valor como hecho y la regla que
% "hereda" el comportamiento del prototipo por delegación explícita.
valor(obj, 5).
delega(obj, prototipo).
factor(prototipo, 2).

resultado(O, R) :- valor(O, V), delega(O, P), factor(P, F), R = V * F.
```

**Qué reconocer:** este es el cierre honesto de la clase, porque aquí la delegación deja de ser un
mecanismo del lenguaje y pasa a ser **un dato que tú escribes**. El hecho `delega(obj, prototipo)` es
literalmente lo que JavaScript guarda en el enlace interno del prototipo y Lua en `__index`, solo que
visible y consultable. Y la regla que sube de `obj` a `prototipo` para encontrar `factor` es el mismo
recorrido que hace el motor de JS cuando no encuentra una propiedad en el objeto. Que la cadena de
prototipos se pueda escribir en tres líneas de Datalog dice algo importante: no es magia del
lenguaje, es una relación entre objetos que alguien decidió resolver automáticamente.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una lección que solo se ve comparando: el prototipo **no es una
rareza de JavaScript**. Lua lo tiene idéntico con `__index`, R lo tiene en sus entornos, Objective-C
lo alcanza por la vía del mensaje en ejecución y Datalog lo escribe como un hecho. Lo que sí es raro
es la combinación de JavaScript —prototipos *y* sintaxis de clases encima—, y por eso sus propios
descendientes, Dart y ActionScript 3, prefirieron quedarse solo con las clases.

⏮️ [Volver a la clase 113](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
