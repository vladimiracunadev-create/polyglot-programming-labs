# 🧬 El mismo programa en las familias de lenguajes — Clase 111

> [⬅️ Volver a la clase 111](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —elegir el sonido de un animal sin preguntar de qué
tipo es— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo
por los diez lenguajes del núcleo.

Aquí la comparación separa a la familia en dos bandos que rara vez se ven juntos: los lenguajes que
permiten **heredar de varios padres a la vez** —con el problema del diamante detrás— y los que lo
prohibieron a propósito y ofrecen a cambio módulos, mixins o traits. Y un tercer bando, el de los
lenguajes sin herencia ninguna, que resuelve exactamente lo mismo con uniones etiquetadas o reglas.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): una palabra, `perro`, `gato` o `vaca`
- **Salida** (stdout): `sonido=<guau|miau|muu>`
- **Regla:** cada tipo devuelve su propio sonido; quien llama no consulta el tipo

| stdin | esperado |
|---|---|
| `perro` | `sonido=guau` |
| `gato` | `sonido=miau` |
| `vaca` | `sonido=muu` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
El despacho se resuelve en ejecución buscando el método por su nombre. Si el objeto responde, sirve:
no hace falta que ninguna declaración lo prometa de antemano.

### Ruby

```ruby
module Sonoro
  def describir
    "sonido=#{sonido}"
  end
end

class Animal
  include Sonoro
end

class Perro < Animal
  def sonido
    "guau"
  end
end

class Gato < Animal
  def sonido
    "miau"
  end
end

class Vaca < Animal
  def sonido
    "muu"
  end
end

animales = { "perro" => Perro.new, "gato" => Gato.new, "vaca" => Vaca.new }
puts animales[STDIN.gets.strip].describir
```

### Perl

```perl
use strict;
use warnings;

package Animal;
sub new { my ($clase) = @_; return bless {}, $clase }

package Perro;
our @ISA = ('Animal');
sub sonido { "guau" }

package Gato;
our @ISA = ('Animal');
sub sonido { "miau" }

package Vaca;
our @ISA = ('Animal');
sub sonido { "muu" }

package main;
chomp(my $tipo = <STDIN>);
my %animales = (perro => Perro->new, gato => Gato->new, vaca => Vaca->new);
printf "sonido=%s\n", $animales{$tipo}->sonido;
```

### Lua

```lua
-- La herencia es delegación: si la tabla no tiene el campo, se busca en `__index`.
local Animal = {}
Animal.__index = Animal
function Animal:describir()
  return "sonido=" .. self:sonido()
end

local function derivar(voz)
  local T = setmetatable({}, { __index = Animal })
  T.__index = T
  function T:sonido()
    return voz
  end
  return T
end

local animales = { perro = derivar("guau"), gato = derivar("miau"), vaca = derivar("muu") }
local tipo = io.read("l")
local a = setmetatable({}, animales[tipo])
print(a:describir())
```

### Tcl

```tcl
package require TclOO

oo::class create Animal {
    method describir {} { return "sonido=[my sonido]" }
}

oo::class create Perro {
    superclass Animal
    method sonido {} { return "guau" }
}

oo::class create Gato {
    superclass Animal
    method sonido {} { return "miau" }
}

oo::class create Vaca {
    superclass Animal
    method sonido {} { return "muu" }
}

gets stdin tipo
set animales [dict create perro [Perro new] gato [Gato new] vaca [Vaca new]]
puts [[dict get $animales [string trim $tipo]] describir]
```

### R

```r
setClass("Animal", representation("VIRTUAL"))
setClass("Perro", contains = "Animal")
setClass("Gato", contains = "Animal")
setClass("Vaca", contains = "Animal")

setGeneric("sonido", function(a) standardGeneric("sonido"))
setMethod("sonido", "Perro", function(a) "guau")
setMethod("sonido", "Gato", function(a) "miau")
setMethod("sonido", "Vaca", function(a) "muu")

tipo <- trimws(readLines("stdin", n = 1))
clases <- c(perro = "Perro", gato = "Gato", vaca = "Vaca")
cat(sprintf("sonido=%s\n", sonido(new(clases[[tipo]]))))
```

**Qué reconocer:** los cinco despachan por el objeto, no por una declaración previa, pero el
mecanismo interno es distinto en cada uno. Ruby **prohíbe la herencia múltiple** y la sustituye por
`module` + `include`: `Sonoro` aporta comportamiento sin ser un padre, y por eso puede mezclarse en
jerarquías que no tienen nada que ver. Perl hace lo contrario: `@ISA` es un **array**, admite varios
padres y deja al programador la responsabilidad del orden de búsqueda. Lua no tiene clases en
absoluto —`__index` encadena tablas y la "herencia" es la delegación de un objeto a otro—. R es el
más raro de la tanda: `sonido` es un **genérico que vive fuera de las clases**, así que el método no
pertenece al animal sino a la operación, y añadir un tipo nuevo no obliga a tocar clase alguna.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

abstract class Animal {
  String sonido();
}

class Perro extends Animal {
  @override
  String sonido() => 'guau';
}

class Gato extends Animal {
  @override
  String sonido() => 'miau';
}

class Vaca extends Animal {
  @override
  String sonido() => 'muu';
}

void main() {
  final animales = <String, Animal>{
    'perro': Perro(),
    'gato': Gato(),
    'vaca': Vaca(),
  };
  final tipo = stdin.readLineSync()!.trim();
  print('sonido=${animales[tipo]!.sonido()}');
}
```

### ActionScript 3

```actionscript
// AS3 exige una clase pública por archivo y no tiene stdin: aquí van dos de los
// tres ficheros seguidos para poder leer la jerarquía de un vistazo.
package {
    public class Animal {
        public function sonido():String { return ""; }
        public function describir():String { return "sonido=" + sonido(); }
    }
}

package {
    public class Perro extends Animal {
        override public function sonido():String { return "guau"; }
    }
}
```

**Qué reconocer:** los dos heredan de **un solo padre**, igual que `class ... extends` en JavaScript,
y los dos exigen marcar la redefinición con `@override` / `override` —una palabra que JavaScript no
tiene y que convierte en error de compilación el clásico fallo de escribir mal el nombre del método
que se creía estar redefiniendo—. Dart añade `abstract`: `Animal` declara `sonido()` sin cuerpo y el
compilador rechaza cualquier subclase que lo olvide, mientras que en JavaScript la clase base tendría
que lanzar el error a mano en ejecución.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Una sola superclase por tipo, decisión de
diseño explícita de la plataforma para evitar el diamante; lo que cambia entre estos primos es qué
ofrecen a cambio.

### Kotlin

```kotlin
sealed class Animal {
    abstract fun sonido(): String
}

class Perro : Animal() {
    override fun sonido() = "guau"
}

class Gato : Animal() {
    override fun sonido() = "miau"
}

class Vaca : Animal() {
    override fun sonido() = "muu"
}

fun main() {
    val animales = mapOf("perro" to Perro(), "gato" to Gato(), "vaca" to Vaca())
    println("sonido=${animales.getValue(readLine()!!.trim()).sonido()}")
}
```

### Scala

```scala
trait Animal { def sonido: String }
trait Ladra extends Animal { def sonido = "guau" }
trait Maulla extends Animal { def sonido = "miau" }
trait Muge extends Animal { def sonido = "muu" }

class Perro extends Ladra
class Gato extends Maulla
class Vaca extends Muge

object Sonidos extends App {
  val animales = Map[String, Animal](
    "perro" -> new Perro, "gato" -> new Gato, "vaca" -> new Vaca)
  println(s"sonido=${animales(scala.io.StdIn.readLine().trim).sonido}")
}
```

### Groovy

```groovy
class Animal { String sonido() { '' } }
class Perro extends Animal { String sonido() { 'guau' } }
class Gato extends Animal { String sonido() { 'miau' } }
class Vaca extends Animal { String sonido() { 'muu' } }

def animales = [perro: new Perro(), gato: new Gato(), vaca: new Vaca()]
def tipo = System.in.newReader().readLine().trim()
println "sonido=${animales[tipo].sonido()}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(defmulti sonido :tipo)
(defmethod sonido "perro" [_] "guau")
(defmethod sonido "gato" [_] "miau")
(defmethod sonido "vaca" [_] "muu")

(println (str "sonido=" (sonido {:tipo (str/trim (read-line))})))
```

**Qué reconocer:** los cuatro corren sobre una máquina que **no admite herencia múltiple de clases**,
y cada uno inventa su salida. Kotlin cierra la jerarquía con `sealed`: el compilador sabe qué
subtipos existen y puede exigir que un `when` los cubra todos. Scala apila **traits**: `Perro`
hereda de `Ladra`, que hereda de `Animal`, y si mezclara varios traits con el mismo método la
**linearización** decidiría cuál gana según un orden definido —esa regla es exactamente lo que Java
evitó prohibiendo el diamante—. Groovy renuncia a declarar nada: la llamada se resuelve por nombre en
ejecución, como en Python. Clojure descarta la jerarquía entera: `defmulti` despacha por el valor que
devuelve una función arbitraria, así que la "clase" del animal es solo un dato en un mapa.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
type Animal =
    | Perro
    | Gato
    | Vaca

let sonido animal =
    match animal with
    | Perro -> "guau"
    | Gato -> "miau"
    | Vaca -> "muu"

let animal =
    match stdin.ReadLine().Trim() with
    | "perro" -> Perro
    | "gato" -> Gato
    | _ -> Vaca

printfn "sonido=%s" (sonido animal)
```

### VB.NET

```vbnet
Imports System.Collections.Generic

MustInherit Class Animal
    Public MustOverride Function Sonido() As String
End Class

Class Perro
    Inherits Animal
    Public Overrides Function Sonido() As String
        Return "guau"
    End Function
End Class

Class Gato
    Inherits Animal
    Public Overrides Function Sonido() As String
        Return "miau"
    End Function
End Class

Class Vaca
    Inherits Animal
    Public Overrides Function Sonido() As String
        Return "muu"
    End Function
End Class

Module Programa
    Sub Main()
        Dim animales As New Dictionary(Of String, Animal) From {
            {"perro", New Perro()}, {"gato", New Gato()}, {"vaca", New Vaca()}
        }
        Console.WriteLine("sonido=" & animales(Console.ReadLine().Trim()).Sonido())
    End Sub
End Module
```

**Qué reconocer:** VB.NET escribe la herencia clásica del CLR con palabras en vez de símbolos
—`MustInherit` es `abstract`, `MustOverride` es el método sin cuerpo, `Overrides` es `override`— y
sufre la misma restricción de una sola clase base que C#. F# da la vuelta al problema: en lugar de
tres tipos que redefinen un método, declara **un tipo con tres formas** y una función que las
distingue. El polimorfismo sigue ahí, pero se ha movido de las clases a la función: añadir un animal
en VB.NET significa escribir una clase y no tocar nada más, mientras que en F# significa editar la
unión y el `match` —y el compilador avisará de cada `match` que se quedó incompleto—.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). En C el polimorfismo se escribe a mano con punteros
a función; estos dos primos lo trajeron al lenguaje.

### C++

```cpp
#include <iostream>
#include <map>
#include <memory>
#include <string>

struct Animal {
    virtual std::string sonido() const = 0;
    virtual ~Animal() = default;
};

struct Perro : Animal {
    std::string sonido() const override { return "guau"; }
};

struct Gato : Animal {
    std::string sonido() const override { return "miau"; }
};

struct Vaca : Animal {
    std::string sonido() const override { return "muu"; }
};

int main() {
    std::map<std::string, std::unique_ptr<Animal>> animales;
    animales["perro"] = std::make_unique<Perro>();
    animales["gato"] = std::make_unique<Gato>();
    animales["vaca"] = std::make_unique<Vaca>();

    std::string tipo;
    std::cin >> tipo;
    std::cout << "sonido=" << animales[tipo]->sonido() << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

@interface Animal : NSObject
- (NSString *)sonido;
@end
@implementation Animal
- (NSString *)sonido { return @""; }
@end

@interface Perro : Animal @end
@implementation Perro
- (NSString *)sonido { return @"guau"; }
@end

@interface Gato : Animal @end
@implementation Gato
- (NSString *)sonido { return @"miau"; }
@end

@interface Vaca : Animal @end
@implementation Vaca
- (NSString *)sonido { return @"muu"; }
@end

int main(void) {
    @autoreleasepool {
        char buf[32] = {0};
        scanf("%31s", buf);
        NSDictionary *animales = @{
            @"perro": [Perro new], @"gato": [Gato new], @"vaca": [Vaca new]
        };
        Animal *a = animales[[NSString stringWithUTF8String:buf]];
        printf("sonido=%s\n", [[a sonido] UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** aquí está la frontera más marcada de esta clase. **C++ sí permite heredar de
varias clases**, y con ello importó el problema del diamante: si `Perro` heredase de dos bases que a
su vez heredan de `Animal`, el objeto llevaría **dos copias** del subobjeto `Animal` salvo que las
bases se declaren `virtual`. Objective-C tomó la decisión opuesta —una sola superclase, y punto— y
compensa con **protocolos** (contratos sin implementación, que sí se pueden adoptar varios) y
**categorías** (añadir métodos a una clase existente sin heredar de ella). La `vtable` está en los
dos: `virtual` en C++ y el envío de mensajes de Objective-C hacen el mismo trabajo que la tabla de
punteros a función que en C se escribe a mano.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Ninguno de los dos tiene
herencia; el polimorfismo se obtiene por interfaces o traits, sin jerarquía de tipos.

### Zig

```zig
const std = @import("std");

// Zig no tiene clases ni herencia: el polimorfismo cerrado se escribe como
// union etiquetada, y el `switch` debe cubrir todos los casos o no compila.
const Animal = union(enum) {
    perro,
    gato,
    vaca,

    fn sonido(self: Animal) []const u8 {
        return switch (self) {
            .perro => "guau",
            .gato => "miau",
            .vaca => "muu",
        };
    }
};

pub fn main() !void {
    var buf: [32]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const tipo = std.mem.trim(u8, linea, " \r\n");
    const animal: Animal = if (std.mem.eql(u8, tipo, "perro"))
        .perro
    else if (std.mem.eql(u8, tipo, "gato"))
        .gato
    else
        .vaca;
    try std.io.getStdOut().writer().print("sonido={s}\n", .{animal.sonido()});
}
```

### Nim

```nim
import std/strutils

type
  Animal = ref object of RootObj
  Perro = ref object of Animal
  Gato = ref object of Animal
  Vaca = ref object of Animal

method sonido(a: Animal): string {.base.} = ""
method sonido(a: Perro): string = "guau"
method sonido(a: Gato): string = "miau"
method sonido(a: Vaca): string = "muu"

let tipo = stdin.readLine().strip()
let animal: Animal =
  case tipo
  of "perro": Perro()
  of "gato": Gato()
  else: Vaca()
echo "sonido=", animal.sonido()
```

### D

```d
import std.stdio, std.string;

abstract class Animal { string sonido(); }
class Perro : Animal { override string sonido() { return "guau"; } }
class Gato : Animal { override string sonido() { return "miau"; } }
class Vaca : Animal { override string sonido() { return "muu"; } }

void main() {
    Animal[string] animales = [
        "perro": cast(Animal) new Perro,
        "gato": new Gato,
        "vaca": new Vaca
    ];
    auto tipo = readln().strip();
    writeln("sonido=", animales[tipo].sonido());
}
```

**Qué reconocer:** los tres compilan a binario nativo y aun así eligen tres posturas distintas. Zig
es el más cercano a Rust: sin herencia, con una unión etiquetada cuyo `switch` el compilador exige
completo —el mismo `match` exhaustivo de Rust, sin `dyn` ni tabla virtual—. Nim y D sí tienen clases
y herencia **simple**, pero Nim obliga a escribir `method` en vez de `proc` para pedir despacho
dinámico: si escribes `proc`, la llamada se resuelve por el tipo estático y `Perro` nunca se
consulta. D es el más parecido a Java —`abstract class`, `override` obligatorio, una sola base— y
resuelve la herencia múltiple igual que Java: con interfaces.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). No hay objetos ni métodos: se declara la relación
entre los datos y el motor elige el camino.

### Prolog

```prolog
:- initialization(main, main).

sonido_propio(perro, "guau").
sonido_propio(gato, "miau").
sonido_propio(vaca, "muu").

main :-
    read_line_to_string(user_input, Linea),
    atom_string(Tipo, Linea),
    sonido_propio(Tipo, S),
    format("sonido=~w~n", [S]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S ni objetos: la herencia se escribe como una regla
% recursiva que sube por la relación `es_un`.
sonido_propio(perro, guau).
sonido_propio(gato, miau).
sonido_propio(vaca, muu).

es_un(bulldog, perro).

sonido(A, S) :- sonido_propio(A, S).
sonido(A, S) :- es_un(A, Padre), sonido(Padre, S).
```

**Qué reconocer:** aquí el polimorfismo se ve en su forma más desnuda. En Prolog, `sonido_propio` son
tres cláusulas del **mismo predicado**: el motor prueba una tras otra y se queda con la que unifica
—eso *es* despacho por el valor, sin clases, sin `vtable` y sin declarar tipo alguno—. Datalog añade
lo más revelador de esta clase: la regla `sonido(A, S) :- es_un(A, Padre), sonido(Padre, S)` **es**
la herencia, escrita como recursión sobre una relación. Un bulldog no tiene sonido propio, pero
hereda el del perro porque la regla sube por la cadena `es_un`, exactamente lo que hace la búsqueda
de método de Ruby o de Lua, solo que aquí está a la vista en dos líneas.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una pregunta que los divide de verdad: **qué se hace cuando un
tipo necesita comportamiento de dos sitios distintos**. C++ y Perl dicen "hereda de los dos y arregla
tú los conflictos"; Ruby, Java, Objective-C, Nim y D lo prohíben y ofrecen módulos, interfaces,
protocolos o categorías; Scala lo permite pero con una regla de linearización que decide por ti; y
Clojure, F#, Zig y Datalog sacan el despacho fuera de los tipos. Reconocer en qué bando está un
lenguaje nuevo te dice de antemano cómo se organizará su código.

⏮️ [Volver a la clase 111](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
