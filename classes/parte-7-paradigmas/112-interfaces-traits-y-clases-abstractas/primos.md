# 🧬 El mismo programa en las familias de lenguajes — Clase 112

> [⬅️ Volver a la clase 112](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —calcular el área de una figura a través de un
contrato común— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

La pregunta que separa a estos veinte lenguajes es sencilla de formular y difícil de responder:
**¿el contrato puede traer código consigo?** Una interfaz pura solo promete firmas; una clase
abstracta puede además implementar; un trait está justo en medio y por eso se puede adoptar varias
veces sin romper nada.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `cuadrado <lado>` o `rectangulo <ancho> <alto>`
- **Salida** (stdout): `area=<área>`
- **Regla:** cada figura implementa `area()` a su manera; quien llama solo conoce el contrato

| stdin | esperado |
|---|---|
| `cuadrado 5` | `area=25` |
| `rectangulo 3 4` | `area=12` |
| `cuadrado 6` | `area=36` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
El contrato no se declara: se comprueba en ejecución preguntando si el objeto responde al método.
Es el *duck typing* llevado a su consecuencia — si tiene `area`, es una figura.

### Ruby

```ruby
module Forma
  def describir
    "area=#{area}"
  end
end

class Cuadrado
  include Forma

  def initialize(lado)
    @lado = lado
  end

  def area
    @lado * @lado
  end
end

class Rectangulo
  include Forma

  def initialize(ancho, alto)
    @ancho = ancho
    @alto = alto
  end

  def area
    @ancho * @alto
  end
end

t = STDIN.gets.split
figura = t[0] == "cuadrado" ? Cuadrado.new(t[1].to_i) : Rectangulo.new(t[1].to_i, t[2].to_i)
puts figura.describir
```

### Perl

```perl
use strict;
use warnings;

package Cuadrado;
sub new { my ($c, $l) = @_; return bless { l => $l }, $c }
sub area { my ($s) = @_; return $s->{l} * $s->{l} }

package Rectangulo;
sub new { my ($c, $a, $b) = @_; return bless { a => $a, b => $b }, $c }
sub area { my ($s) = @_; return $s->{a} * $s->{b} }

package main;
my @t = split ' ', <STDIN>;
my $figura = $t[0] eq 'cuadrado'
    ? Cuadrado->new($t[1])
    : Rectangulo->new($t[1], $t[2]);
die "no cumple el contrato\n" unless $figura->can('area');
printf "area=%d\n", $figura->area;
```

### Lua

```lua
-- Lua no declara interfaces: basta con que la tabla tenga el campo `area`.
local Cuadrado = {}
Cuadrado.__index = Cuadrado
function Cuadrado.nueva(l)
  return setmetatable({ l = l }, Cuadrado)
end
function Cuadrado:area()
  return self.l * self.l
end

local Rectangulo = {}
Rectangulo.__index = Rectangulo
function Rectangulo.nueva(a, b)
  return setmetatable({ a = a, b = b }, Rectangulo)
end
function Rectangulo:area()
  return self.a * self.b
end

local t = {}
for palabra in io.read("l"):gmatch("%S+") do
  t[#t + 1] = palabra
end

local figura
if t[1] == "cuadrado" then
  figura = Cuadrado.nueva(tonumber(t[2]))
else
  figura = Rectangulo.nueva(tonumber(t[2]), tonumber(t[3]))
end
print("area=" .. figura:area())
```

### Tcl

```tcl
package require TclOO

oo::class create Forma {
    method area {} { error "las subclases deben implementar area" }
    method describir {} { return "area=[my area]" }
}

oo::class create Cuadrado {
    superclass Forma
    variable l
    constructor {lado} { set l $lado }
    method area {} { expr {$l * $l} }
}

oo::class create Rectangulo {
    superclass Forma
    variable a b
    constructor {ancho alto} { set a $ancho; set b $alto }
    method area {} { expr {$a * $b} }
}

gets stdin linea
set t [split [string trim $linea]]
if {[lindex $t 0] eq "cuadrado"} {
    set figura [Cuadrado new [lindex $t 1]]
} else {
    set figura [Rectangulo new [lindex $t 1] [lindex $t 2]]
}
puts [$figura describir]
```

### R

```r
setClass("Forma", representation("VIRTUAL"))
setGeneric("area", function(f) standardGeneric("area"))

setClass("Cuadrado", contains = "Forma", representation(lado = "numeric"))
setMethod("area", "Cuadrado", function(f) f@lado * f@lado)

setClass("Rectangulo", contains = "Forma",
         representation(ancho = "numeric", alto = "numeric"))
setMethod("area", "Rectangulo", function(f) f@ancho * f@alto)

t <- strsplit(trimws(readLines("stdin", n = 1)), "\\s+")[[1]]
figura <- if (t[1] == "cuadrado") {
  new("Cuadrado", lado = as.numeric(t[2]))
} else {
  new("Rectangulo", ancho = as.numeric(t[2]), alto = as.numeric(t[3]))
}
cat(sprintf("area=%d\n", as.integer(area(figura))))
```

**Qué reconocer:** ninguno de los cinco necesita declarar el contrato para que el programa funcione,
pero cada uno decide cuánto quiere documentarlo. Ruby usa `module` como **trait**: `Forma` aporta
`describir`, que llama a un `area` que el módulo no define —el contrato es implícito, y si la clase
lo incumple el fallo llega en ejecución—. Perl lo hace explícito con `->can('area')`, una pregunta al
sistema de objetos sobre si el método existe. Tcl escribe la **clase abstracta clásica**: el método
base existe, pero solo para lanzar un error si nadie lo redefinió. R vuelve a ser el disidente:
declara `"VIRTUAL"` —una clase que no se puede instanciar— y define `area` como **genérico externo**,
de modo que el contrato pertenece a la operación y no a las figuras.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

abstract class Forma {
  int area();
}

class Cuadrado implements Forma {
  final int lado;
  Cuadrado(this.lado);

  @override
  int area() => lado * lado;
}

class Rectangulo implements Forma {
  final int ancho;
  final int alto;
  Rectangulo(this.ancho, this.alto);

  @override
  int area() => ancho * alto;
}

void main() {
  final t = stdin.readLineSync()!.trim().split(RegExp(r'\s+'));
  final Forma figura = t[0] == 'cuadrado'
      ? Cuadrado(int.parse(t[1]))
      : Rectangulo(int.parse(t[1]), int.parse(t[2]));
  print('area=${figura.area()}');
}
```

### ActionScript 3

```actionscript
// AS3 sí tiene la palabra `interface`, pero no tiene stdin: se ilustran el
// contrato y una de las dos implementaciones (irían en archivos separados).
package {
    public interface IForma {
        function area():int;
    }
}

package {
    public class Cuadrado implements IForma {
        private var lado:int;
        public function Cuadrado(lado:int) { this.lado = lado; }
        public function area():int { return lado * lado; }
    }
}
```

**Qué reconocer:** los dos hacen explícito lo que en JavaScript es solo una convención. ActionScript 3
tiene `interface` como palabra reservada, con la restricción clásica: **solo firmas, nada de cuerpo**,
y por eso una clase puede implementar tantas como quiera. Dart hace algo que casi ningún lenguaje se
atreve a hacer: **toda clase define una interfaz implícita**, así que `implements Cuadrado` es legal
aunque `Cuadrado` sea una clase normal —lo que se hereda con `implements` son las firmas, no el
código, mientras que `extends` sí trae la implementación—. Ese es exactamente el eje de la clase, con
las dos opciones disponibles sobre el mismo tipo.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Desde Java 8 las interfaces admiten métodos
`default` con cuerpo, lo que borró buena parte de la frontera con las clases abstractas.

### Kotlin

```kotlin
interface Forma {
    fun area(): Int
    fun describir(): String = "area=${area()}"
}

class Cuadrado(private val lado: Int) : Forma {
    override fun area() = lado * lado
}

class Rectangulo(private val ancho: Int, private val alto: Int) : Forma {
    override fun area() = ancho * alto
}

fun main() {
    val t = readLine()!!.trim().split(Regex("\\s+"))
    val figura: Forma =
        if (t[0] == "cuadrado") Cuadrado(t[1].toInt())
        else Rectangulo(t[1].toInt(), t[2].toInt())
    println(figura.describir())
}
```

### Scala

```scala
trait Forma {
  def area: Int
  def describir: String = s"area=$area"
}

class Cuadrado(lado: Int) extends Forma { def area = lado * lado }
class Rectangulo(ancho: Int, alto: Int) extends Forma { def area = ancho * alto }

object Areas extends App {
  val t = scala.io.StdIn.readLine().trim.split("\\s+")
  val figura: Forma =
    if (t(0) == "cuadrado") new Cuadrado(t(1).toInt)
    else new Rectangulo(t(1).toInt, t(2).toInt)
  println(figura.describir)
}
```

### Groovy

```groovy
trait Forma {
    abstract int area()
    String describir() { "area=${area()}" }
}

class Cuadrado implements Forma {
    int lado
    int area() { lado * lado }
}

class Rectangulo implements Forma {
    int ancho
    int alto
    int area() { ancho * alto }
}

def t = System.in.newReader().readLine().trim().split(/\s+/)
def figura = t[0] == 'cuadrado'
    ? new Cuadrado(lado: t[1] as int)
    : new Rectangulo(ancho: t[1] as int, alto: t[2] as int)
println figura.describir()
```

### Clojure

```clojure
(require '[clojure.string :as str])

(defprotocol Forma
  (area [f]))

(defrecord Cuadrado [lado]
  Forma
  (area [_] (* lado lado)))

(defrecord Rectangulo [ancho alto]
  Forma
  (area [_] (* ancho alto)))

(let [t (str/split (str/trim (read-line)) #"\s+")
      n (fn [i] (Integer/parseInt (nth t i)))
      figura (if (= (first t) "cuadrado")
               (->Cuadrado (n 1))
               (->Rectangulo (n 1) (n 2)))]
  (println (str "area=" (area figura))))
```

**Qué reconocer:** los cuatro traen implementación dentro del contrato, y ahí está la diferencia
fina. Kotlin escribe `interface` con un método de cuerpo —es el `default` de Java con otro nombre—,
pero una interfaz de Kotlin **no puede guardar estado**. El `trait` de Scala y el de Groovy sí:
pueden declarar campos, y por eso son casi una clase abstracta que se puede mezclar varias veces. Ese
"varias veces" es lo que obliga a Scala a definir la **linearización**, la regla que decide qué
implementación gana cuando dos traits aportan el mismo método. Clojure separa las dos cosas por
completo: `defprotocol` es un contrato **sin ninguna implementación** y `defrecord` es un dato
—ninguno de los dos hereda de nada, y añadir un protocolo a un tipo que ya existe no requiere
modificarlo—.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
type IForma =
    abstract member Area: unit -> int

type Cuadrado(lado: int) =
    interface IForma with
        member _.Area() = lado * lado

type Rectangulo(ancho: int, alto: int) =
    interface IForma with
        member _.Area() = ancho * alto

let t =
    stdin.ReadLine().Trim().Split([| ' ' |], System.StringSplitOptions.RemoveEmptyEntries)

let figura: IForma =
    if t.[0] = "cuadrado" then Cuadrado(int t.[1]) :> IForma
    else Rectangulo(int t.[1], int t.[2]) :> IForma

printfn "area=%d" (figura.Area())
```

### VB.NET

```vbnet
Interface IForma
    Function Area() As Integer
End Interface

Class Cuadrado
    Implements IForma
    Private ReadOnly lado As Integer

    Sub New(l As Integer)
        lado = l
    End Sub

    Public Function Area() As Integer Implements IForma.Area
        Return lado * lado
    End Function
End Class

Class Rectangulo
    Implements IForma
    Private ReadOnly ancho As Integer
    Private ReadOnly alto As Integer

    Sub New(a As Integer, b As Integer)
        ancho = a
        alto = b
    End Sub

    Public Function Area() As Integer Implements IForma.Area
        Return ancho * alto
    End Function
End Class

Module Programa
    Sub Main()
        Dim t = Console.ReadLine().Trim().Split(" "c)
        Dim figura As IForma
        If t(0) = "cuadrado" Then
            figura = New Cuadrado(Integer.Parse(t(1)))
        Else
            figura = New Rectangulo(Integer.Parse(t(1)), Integer.Parse(t(2)))
        End If
        Console.WriteLine("area=" & figura.Area())
    End Sub
End Module
```

**Qué reconocer:** el CLR admite **una sola clase base pero muchas interfaces**, y los dos primos lo
escriben con una franqueza que C# esconde. VB.NET obliga a decir a qué contrato responde cada método
con la cláusula `Implements IForma.Area`, así que el vínculo entre firma y contrato está escrito en
el propio método —eso permite además que un método con otro nombre cumpla el contrato—. F# va más
lejos: sus implementaciones de interfaz son **siempre explícitas**, el método no es accesible desde
el tipo concreto, y por eso hace falta el ascenso `:> IForma` antes de poder llamarlo. Un `Cuadrado`
de F# no tiene `Area`; solo la tiene visto *como* `IForma`.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). C no tiene contratos: lo más parecido es una
`struct` de punteros a función que cada tipo rellena.

### C++

```cpp
#include <iostream>
#include <memory>
#include <string>

// C++ no tiene la palabra `interface`: una clase con solo métodos virtuales
// puros hace ese papel, y de esas sí se puede heredar más de una.
struct Forma {
    virtual int area() const = 0;
    virtual ~Forma() = default;
};

struct Cuadrado : Forma {
    int lado;
    explicit Cuadrado(int l) : lado(l) {}
    int area() const override { return lado * lado; }
};

struct Rectangulo : Forma {
    int ancho, alto;
    Rectangulo(int a, int b) : ancho(a), alto(b) {}
    int area() const override { return ancho * alto; }
};

int main() {
    std::string tipo;
    std::cin >> tipo;
    std::unique_ptr<Forma> figura;
    if (tipo == "cuadrado") {
        int l;
        std::cin >> l;
        figura = std::make_unique<Cuadrado>(l);
    } else {
        int a, b;
        std::cin >> a >> b;
        figura = std::make_unique<Rectangulo>(a, b);
    }
    std::cout << "area=" << figura->area() << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

@protocol Forma <NSObject>
- (int)area;
@end

@interface Cuadrado : NSObject <Forma>
@property int lado;
@end
@implementation Cuadrado
- (int)area { return self.lado * self.lado; }
@end

@interface Rectangulo : NSObject <Forma>
@property int ancho;
@property int alto;
@end
@implementation Rectangulo
- (int)area { return self.ancho * self.alto; }
@end

int main(void) {
    @autoreleasepool {
        char tipo[32] = {0};
        int a = 0, b = 0;
        scanf("%31s %d", tipo, &a);
        id<Forma> figura;
        if (strcmp(tipo, "cuadrado") == 0) {
            Cuadrado *c = [Cuadrado new];
            c.lado = a;
            figura = c;
        } else {
            scanf("%d", &b);
            Rectangulo *r = [Rectangulo new];
            r.ancho = a;
            r.alto = b;
            figura = r;
        }
        printf("area=%d\n", [figura area]);
    }
    return 0;
}
```

**Qué reconocer:** la misma división de la clase, resuelta al revés en cada uno. C++ **no distingue**
interfaz de clase abstracta: la interfaz es una clase abstracta sin datos, y como el lenguaje permite
herencia múltiple no necesitó inventar una palabra aparte —el precio es el diamante y la herencia
`virtual`—. Objective-C sí separó las dos cosas desde el principio: `@protocol` es el contrato puro,
adoptable en cualquier número, mientras que la herencia de clase sigue siendo única. Fíjate además en
el tipo `id<Forma>`: no dice de qué clase es el objeto, solo qué contrato cumple. Es la misma idea que
`Box<dyn Forma>` en Rust o `interface{}` con métodos en Go.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Los dos rompieron con la
tradición: el tipo no declara qué contratos cumple —Go los satisface por forma, Rust los implementa
desde fuera—.

### Zig

```zig
const std = @import("std");

// Zig no tiene interfaces ni traits: un contrato cerrado se escribe como union
// etiquetada y el compilador exige que el `switch` cubra todos los casos.
const Forma = union(enum) {
    cuadrado: i64,
    rectangulo: struct { ancho: i64, alto: i64 },

    fn area(self: Forma) i64 {
        return switch (self) {
            .cuadrado => |l| l * l,
            .rectangulo => |r| r.ancho * r.alto,
        };
    }
};

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \r\n\t");
    const tipo = it.next().?;
    const a = try std.fmt.parseInt(i64, it.next().?, 10);
    const figura: Forma = if (std.mem.eql(u8, tipo, "cuadrado"))
        .{ .cuadrado = a }
    else
        .{ .rectangulo = .{ .ancho = a, .alto = try std.fmt.parseInt(i64, it.next().?, 10) } };
    try std.io.getStdOut().writer().print("area={d}\n", .{figura.area()});
}
```

### Nim

```nim
import std/strutils

# `concept` (experimental) describe el contrato por lo que el tipo sabe hacer,
# no por lo que declara: es el equivalente a las interfaces implícitas de Go.
type
  Forma = concept f
    area(f) is int

  Cuadrado = object
    lado: int

  Rectangulo = object
    ancho, alto: int

func area(c: Cuadrado): int = c.lado * c.lado
func area(r: Rectangulo): int = r.ancho * r.alto

func describir(f: Forma): string = "area=" & $area(f)

let t = stdin.readLine().splitWhitespace()
if t[0] == "cuadrado":
  echo describir(Cuadrado(lado: parseInt(t[1])))
else:
  echo describir(Rectangulo(ancho: parseInt(t[1]), alto: parseInt(t[2])))
```

### D

```d
import std.stdio, std.string, std.array, std.conv;

interface Forma {
    int area();
}

class Cuadrado : Forma {
    private int lado;
    this(int l) { lado = l; }
    int area() { return lado * lado; }
}

class Rectangulo : Forma {
    private int ancho, alto;
    this(int a, int b) { ancho = a; alto = b; }
    int area() { return ancho * alto; }
}

void main() {
    auto t = readln().strip().split();
    Forma figura = t[0] == "cuadrado"
        ? cast(Forma) new Cuadrado(t[1].to!int)
        : new Rectangulo(t[1].to!int, t[2].to!int);
    writeln("area=", figura.area());
}
```

**Qué reconocer:** tres formas de contrato sin una sola línea en común. Zig no tiene ninguna —cierra
el conjunto de figuras en una unión y confía en el `switch` exhaustivo, que es despacho decidido en
compilación, sin tabla virtual—. Nim se acerca a Go: un `concept` no se implementa, se **cumple**,
porque describe qué operaciones deben existir y el compilador comprueba si el tipo las tiene; la
diferencia con Go es que Nim lo resuelve en compilación por instanciación, sin indirección alguna. D
es el conservador del trío, con `interface` y `class` a la manera de Java, y con la misma regla:
herencia simple de clases, múltiple de interfaces.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). El "contrato" es el esquema: se declara qué
relaciona a los datos, no qué métodos tiene cada fila.

### Prolog

```prolog
:- initialization(main, main).

area(cuadrado, [L], A) :- A is L * L.
area(rectangulo, [W, H], A) :- A is W * H.

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", [T|Resto]),
    atom_string(Tipo, T),
    maplist([S, N]>>number_string(N, S), Resto, Nums),
    area(Tipo, Nums, A),
    format("area=~w~n", [A]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S: las figuras se declaran como hechos y el contrato
% `area/2` es una regla por cada forma, no un tipo con métodos.
cuadrado(f1, 5).
rectangulo(f2, 3, 4).

area(F, A) :- cuadrado(F, L), A = L * L.
area(F, A) :- rectangulo(F, W, H), A = W * H.
```

**Qué reconocer:** el contrato existe, pero no pertenece a ningún tipo. En Prolog, `area/3` es **un
solo predicado con dos cláusulas**: quien llama pide `area(Tipo, Nums, A)` sin saber cuál se
aplicará, y el motor prueba en orden hasta que una unifica —eso es precisamente lo que hace una
interfaz, solo que sin declarar nada—. Datalog lo lleva al mínimo: `area(F, A)` se define por reglas
independientes que nadie tuvo que registrar en una lista, y añadir un triángulo consiste en escribir
una regla más sin tocar las anteriores. Es la misma propiedad que hace valiosos los protocolos de
Clojure o los `impl` de Rust: el contrato se extiende **desde fuera** del tipo.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y un eje que los ordena a todos: **cuánto puede traer el contrato
además de la firma**. Nada en ActionScript o VB.NET; una implementación por defecto en Kotlin; estado
completo en un `trait` de Scala; y en Prolog, Clojure o Rust ni siquiera pertenece al tipo, sino que
se le añade desde fuera. Cuando abras un lenguaje nuevo, busca esa respuesta primero: te dice de
antemano si sus jerarquías serán profundas o planas.

⏮️ [Volver a la clase 112](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
