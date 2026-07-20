# 🧬 El mismo programa en las familias de lenguajes — Clase 100

> [⬅️ Volver a la clase 100](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —calcular el área de una figura que puede ser un
cuadrado o un rectángulo— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

De todas las clases del programa, esta es donde las familias **más se separan**. La pregunta "¿puede
mi tipo tener varias formas posibles, y me obliga el compilador a tratarlas todas?" divide a los
veinte lenguajes en tres grupos muy distintos: los que tienen tipo suma de verdad, los que lo emulan
con una etiqueta y disciplina, y los que ni siquiera pueden representar el tipo.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `cuadrado <lado>` o `rectangulo <ancho> <alto>`
- **Salida** (stdout): `area=<área calculada>`
- **Regla:** cuadrado → lado²; rectangulo → ancho · alto

| stdin | esperado |
|---|---|
| `cuadrado 5` | `area=25` |
| `rectangulo 3 4` | `area=12` |
| `cuadrado 7` | `area=49` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Ninguno tiene tipos suma. La variante se guarda en un campo `tipo` y el programador se compromete a
mirarlo antes de leer los demás campos; nada del lenguaje comprueba ese compromiso.

### Ruby

```ruby
Cuadrado = Struct.new(:lado)
Rectangulo = Struct.new(:ancho, :alto)

campos = STDIN.gets.split
figura = if campos[0] == "cuadrado"
           Cuadrado.new(campos[1].to_i)
         else
           Rectangulo.new(campos[1].to_i, campos[2].to_i)
         end

# case/in de Ruby 3 desestructura el Struct; si nada casa, lanza
# NoMatchingPatternError en tiempo de ejecución, no antes.
area = case figura
       in Cuadrado[lado] then lado * lado
       in Rectangulo[ancho, alto] then ancho * alto
       end

puts "area=#{area}"
```

### Perl

```perl
my @campos = split ' ', <STDIN>;
my $figura = $campos[0] eq 'cuadrado'
    ? { tipo => 'cuadrado', lado => $campos[1] }
    : { tipo => 'rectangulo', ancho => $campos[1], alto => $campos[2] };

my $area = $figura->{tipo} eq 'cuadrado'
    ? $figura->{lado} ** 2
    : $figura->{ancho} * $figura->{alto};

print "area=$area\n";
```

### Lua

```lua
local campos = {}
for w in io.read("l"):gmatch("%S+") do campos[#campos + 1] = w end

local figura
if campos[1] == "cuadrado" then
  figura = { tipo = "cuadrado", lado = tonumber(campos[2]) }
else
  figura = { tipo = "rectangulo", ancho = tonumber(campos[2]), alto = tonumber(campos[3]) }
end

-- Leer figura.ancho en un cuadrado devuelve nil, no un error.
local area
if figura.tipo == "cuadrado" then
  area = figura.lado * figura.lado
else
  area = figura.ancho * figura.alto
end

print(string.format("area=%d", area))
```

### Tcl

```tcl
gets stdin linea
set campos [split [string trim $linea]]
set resto [lassign $campos tipo]

switch -- $tipo {
    cuadrado   { set area [expr {[lindex $resto 0] ** 2}] }
    rectangulo { set area [expr {[lindex $resto 0] * [lindex $resto 1]}] }
    default    { error "figura desconocida: $tipo" }
}

puts "area=$area"
```

### R

```r
campos <- strsplit(trimws(readLines("stdin", n = 1)), "\\s+")[[1]]

figura <- switch(campos[1],
  cuadrado   = list(tipo = "cuadrado", lado = as.integer(campos[2])),
  rectangulo = list(tipo = "rectangulo",
                    ancho = as.integer(campos[2]),
                    alto = as.integer(campos[3]))
)

area <- switch(figura$tipo,
  cuadrado   = figura$lado^2,
  rectangulo = figura$ancho * figura$alto
)

cat(sprintf("area=%d\n", as.integer(area)))
```

**Qué reconocer:** los cinco escriben el mismo patrón —una etiqueta de texto y un `if` o `switch` que
la mira— y ninguno tiene forma de comprobar que las etiquetas están cubiertas. Si mañana añades
`circulo`, Perl y Lua calcularán el área de un rectángulo con campos `nil` y no dirán nada; R y Tcl
al menos fallan porque su `switch` sin rama coincidente devuelve `NULL` o entra en `default`. Ruby
es el que más cerca llega: `case/in`, añadido en Ruby 3, **desestructura** el `Struct` igual que
Scala desestructura una `case class`, y si ninguna rama casa lanza `NoMatchingPatternError` en vez de
seguir en silencio. Sigue siendo una comprobación en tiempo de ejecución —el programa ya está
corriendo cuando descubres el hueco—, y esa es exactamente la línea que separa a esta familia de la
siguiente.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

sealed class Figura {}

class Cuadrado extends Figura {
  final int lado;
  Cuadrado(this.lado);
}

class Rectangulo extends Figura {
  final int ancho;
  final int alto;
  Rectangulo(this.ancho, this.alto);
}

void main() {
  final campos = stdin.readLineSync()!.trim().split(RegExp(r'\s+'));
  final Figura figura = campos[0] == 'cuadrado'
      ? Cuadrado(int.parse(campos[1]))
      : Rectangulo(int.parse(campos[1]), int.parse(campos[2]));

  // Con una clase sealed, el switch-expresión es exhaustivo: si añades una
  // variante y no la cubres, el programa no compila.
  final area = switch (figura) {
    Cuadrado(:final lado) => lado * lado,
    Rectangulo(:final ancho, :final alto) => ancho * alto,
  };

  print('area=$area');
}
```

### ActionScript 3

```actionscript
// AS3 no tiene uniones ni clases selladas ni stdin: la variante se codifica con
// una constante y los campos sobrantes quedan sin usar.
package {
    public class Figura {
        public static const CUADRADO:String = "cuadrado";
        public static const RECTANGULO:String = "rectangulo";

        public var tipo:String;
        public var a:int;
        public var b:int;

        public function Figura(tipo:String, a:int, b:int = 0) {
            this.tipo = tipo;
            this.a = a;
            this.b = b;
        }

        public function area():int {
            return tipo == CUADRADO ? a * a : a * b;
        }
    }
}
```

**Qué reconocer:** aquí la familia se parte en dos épocas. ActionScript 3 es la solución de siempre:
una constante como etiqueta y una clase con todos los campos posibles, de los cuales unos sobran
según el caso —`b` no significa nada en un cuadrado, pero existe y vale cero—. Dart 3 trajo `sealed`:
al declarar que solo esas dos clases pueden extender `Figura`, el compilador **sabe la lista completa
de variantes** y exige que el `switch` las cubra todas. Es el mismo mecanismo que TypeScript logra
con uniones discriminadas (`{tipo: 'cuadrado', lado: number} | {tipo: 'rectangulo', ...}`) y el
estrechamiento por el campo `tipo`, salvo que TypeScript lo comprueba y luego lo borra, mientras que
en Dart las clases siguen ahí en tiempo de ejecución.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Java tuvo enumeraciones desde 2004 y clases
selladas solo desde la versión 17; sus primos llevaban una década de ventaja.

### Kotlin

```kotlin
sealed class Figura {
    data class Cuadrado(val lado: Int) : Figura()
    data class Rectangulo(val ancho: Int, val alto: Int) : Figura()
}

fun main() {
    val campos = readLine()!!.trim().split(Regex("\\s+"))
    val figura: Figura = if (campos[0] == "cuadrado") {
        Figura.Cuadrado(campos[1].toInt())
    } else {
        Figura.Rectangulo(campos[1].toInt(), campos[2].toInt())
    }

    // `when` usado como expresión sobre una sealed class exige cubrir todo.
    val area = when (figura) {
        is Figura.Cuadrado -> figura.lado * figura.lado
        is Figura.Rectangulo -> figura.ancho * figura.alto
    }

    println("area=$area")
}
```

### Scala

```scala
object Figuras extends App {
  sealed trait Figura
  case class Cuadrado(lado: Int) extends Figura
  case class Rectangulo(ancho: Int, alto: Int) extends Figura

  val campos = scala.io.StdIn.readLine().trim.split("\\s+")
  val figura: Figura =
    if (campos(0) == "cuadrado") Cuadrado(campos(1).toInt)
    else Rectangulo(campos(1).toInt, campos(2).toInt)

  val area = figura match {
    case Cuadrado(lado) => lado * lado
    case Rectangulo(ancho, alto) => ancho * alto
  }

  println(s"area=$area")
}
```

### Groovy

```groovy
// Groovy no tiene tipos suma ni comprobación exhaustiva: se emula con clases
// sueltas y despacho dinámico por sobrecarga.
class Cuadrado { int lado }
class Rectangulo { int ancho; int alto }

def area(Cuadrado c) { c.lado * c.lado }
def area(Rectangulo r) { r.ancho * r.alto }

def campos = System.in.newReader().readLine().trim().split(/\s+/)
def figura = campos[0] == 'cuadrado'
    ? new Cuadrado(lado: campos[1] as int)
    : new Rectangulo(ancho: campos[1] as int, alto: campos[2] as int)

// Si llegara una figura sin sobrecarga, falla con MissingMethodException al ejecutar.
println "area=${area(figura)}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; Clojure no tiene tipos algebraicos: un mapa con una clave-etiqueta y un
;; multimétodo que despacha sobre ella cumplen el mismo papel.
(defmulti area :tipo)
(defmethod area :cuadrado [f] (* (:lado f) (:lado f)))
(defmethod area :rectangulo [f] (* (:ancho f) (:alto f)))

(let [[tipo & nums] (str/split (str/trim (read-line)) #"\s+")
      [a b] (map #(Integer/parseInt %) nums)
      figura (if (= tipo "cuadrado")
               {:tipo :cuadrado :lado a}
               {:tipo :rectangulo :ancho a :alto b})]
  (println (str "area=" (area figura))))
```

**Qué reconocer:** cuatro lenguajes, la misma máquina virtual, y la separación más grande de toda
esta página. Scala inventó la fórmula que hoy copian todos: `sealed trait` más `case class` por
variante, y un `match` que el compilador comprueba avisándote si dejas un caso fuera. Kotlin la
adoptó con `sealed class` y `when`, con un matiz que conviene saber: `when` solo **exige**
exhaustividad cuando se usa como expresión —si lo escribes como sentencia, el compilador se conforma
con lo que haya—. Groovy y Clojure renuncian a la idea entera. Groovy usa dos clases sin ancestro
común y deja que el despacho dinámico elija la sobrecarga al ejecutar; Clojure prefiere el mapa
etiquetado con `:tipo` y un **multimétodo**, que es más abierto que un tipo suma —cualquiera puede
añadir un `defmethod` para `:circulo` desde otro archivo, sin tocar el original— y por eso mismo
imposible de comprobar: la lista de variantes nunca está cerrada. Ese intercambio, extensibilidad
contra exhaustividad, es el fondo del problema y no un capricho de sintaxis.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
// Unión discriminada: la definición completa del tipo cabe en tres líneas.
type Figura =
    | Cuadrado of lado: int
    | Rectangulo of ancho: int * alto: int

let campos =
    stdin.ReadLine().Trim().Split(' ')
    |> Array.filter (fun s -> s <> "")

let figura =
    match campos.[0] with
    | "cuadrado" -> Cuadrado(int campos.[1])
    | _ -> Rectangulo(int campos.[1], int campos.[2])

// Si faltara un caso, el compilador avisa: "incomplete pattern matches".
let area =
    match figura with
    | Cuadrado lado -> lado * lado
    | Rectangulo(ancho, alto) -> ancho * alto

printfn "area=%d" area
```

### VB.NET

```vbnet
Imports System

Module Figuras
    ' VB.NET no tiene uniones discriminadas: Enum para la variante y una
    ' Structure con todos los campos posibles, sobren o no.
    Enum Clase
        Cuadrado
        Rectangulo
    End Enum

    Structure Figura
        Public Tipo As Clase
        Public A As Integer
        Public B As Integer
    End Structure

    Sub Main()
        Dim campos = Console.ReadLine().Trim().Split(" "c, StringSplitOptions.RemoveEmptyEntries)
        Dim figura As Figura

        If campos(0) = "cuadrado" Then
            figura.Tipo = Clase.Cuadrado
            figura.A = Integer.Parse(campos(1))
        Else
            figura.Tipo = Clase.Rectangulo
            figura.A = Integer.Parse(campos(1))
            figura.B = Integer.Parse(campos(2))
        End If

        Dim area As Integer
        Select Case figura.Tipo
            Case Clase.Cuadrado
                area = figura.A * figura.A
            Case Else
                area = figura.A * figura.B
        End Select

        Console.WriteLine($"area={area}")
    End Sub
End Module
```

**Qué reconocer:** el contraste más nítido de la página, y sobre la misma plataforma. F# define el
tipo entero en tres líneas: `Cuadrado of lado: int` dice a la vez que existe una variante llamada
`Cuadrado` y que lleva un entero dentro; construir un `Cuadrado` sin lado no compila, y leer el
`alto` de un cuadrado ni siquiera se puede escribir. VB.NET no tiene nada de eso: un `Enum` marca la
variante, una `Structure` guarda todos los campos posibles, y `figura.B` en un cuadrado vale cero
—un valor perfectamente legal que el compilador no cuestiona—. La diferencia práctica aparece al
añadir una tercera figura: F# marca con un aviso cada `match` que se quedó corto, mientras que en
VB.NET el `Case Else` se traga la figura nueva y devuelve un área equivocada. Nótese además que en
F# la unión es un tipo por referencia con comparación por valor, sin `null`: no existe la "figura
vacía".

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). El `union` de C es un tipo suma **sin la etiqueta**:
el lenguaje te deja leer cualquier miembro y confía en que sepas cuál escribiste.

### C++

```cpp
#include <iostream>
#include <string>
#include <type_traits>
#include <variant>

struct Cuadrado { int lado; };
struct Rectangulo { int ancho, alto; };

// std::variant es la union de C con la etiqueta puesta y comprobada.
using Figura = std::variant<Cuadrado, Rectangulo>;

int main() {
    std::string tipo;
    std::cin >> tipo;

    Figura figura;
    if (tipo == "cuadrado") {
        int lado;
        std::cin >> lado;
        figura = Cuadrado{lado};
    } else {
        int ancho, alto;
        std::cin >> ancho >> alto;
        figura = Rectangulo{ancho, alto};
    }

    const int area = std::visit([](auto&& f) {
        using T = std::decay_t<decltype(f)>;
        if constexpr (std::is_same_v<T, Cuadrado>) return f.lado * f.lado;
        else return f.ancho * f.alto;
    }, figura);

    std::cout << "area=" << area << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

// Sin uniones etiquetadas: la variante se expresa con herencia y polimorfismo.
@interface Figura : NSObject
- (NSInteger)area;
@end

@implementation Figura
- (NSInteger)area { return 0; }
@end

@interface Cuadrado : Figura
@property (assign) NSInteger lado;
@end

@implementation Cuadrado
- (NSInteger)area { return self.lado * self.lado; }
@end

@interface Rectangulo : Figura
@property (assign) NSInteger ancho;
@property (assign) NSInteger alto;
@end

@implementation Rectangulo
- (NSInteger)area { return self.ancho * self.alto; }
@end

int main(void) {
    @autoreleasepool {
        char tipo[32];
        long a = 0, b = 0;
        scanf("%31s", tipo);

        Figura *figura;
        if (strcmp(tipo, "cuadrado") == 0) {
            scanf("%ld", &a);
            Cuadrado *c = [Cuadrado new];
            c.lado = a;
            figura = c;
        } else {
            scanf("%ld %ld", &a, &b);
            Rectangulo *r = [Rectangulo new];
            r.ancho = a;
            r.alto = b;
            figura = r;
        }

        printf("area=%ld\n", (long)[figura area]);
    }
    return 0;
}
```

**Qué reconocer:** C++ toma el `union` heredado de C y le añade lo que le faltaba: `std::variant`
recuerda cuál de las alternativas está activa y **falla si pides la otra**, en vez de reinterpretar
los bytes como hace un `union` desnudo. `std::visit` es su coincidencia de patrones, y su aspecto
incómodo —una lambda genérica con `if constexpr`— explica por qué la comunidad de C++ pide desde
hace años un `match` de verdad. Objective-C toma el camino opuesto, el de Smalltalk: no hay tipo
suma, hay una jerarquía de clases y **cada figura sabe calcular su propia área**. La comprobación de
exhaustividad desaparece, pero la extensibilidad crece: añadir `Circulo` no obliga a tocar el código
existente. Es la misma tensión que separaba a Clojure de Scala, repetida aquí entre polimorfismo y
tipo suma.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Rust es el lenguaje que
llevó los tipos suma al terreno de los sistemas; Go, notablemente, sigue sin tenerlos.

### Zig

```zig
const std = @import("std");

// union(enum): la etiqueta es un enum generado por el compilador.
const Figura = union(enum) {
    cuadrado: struct { lado: i64 },
    rectangulo: struct { ancho: i64, alto: i64 },
};

pub fn main() !void {
    var buf: [128]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \t\r");
    const tipo = it.next().?;

    const figura: Figura = if (std.mem.eql(u8, tipo, "cuadrado"))
        .{ .cuadrado = .{ .lado = try std.fmt.parseInt(i64, it.next().?, 10) } }
    else
        .{ .rectangulo = .{
            .ancho = try std.fmt.parseInt(i64, it.next().?, 10),
            .alto = try std.fmt.parseInt(i64, it.next().?, 10),
        } };

    // El switch sobre union(enum) debe cubrir todas las etiquetas o no compila.
    const area = switch (figura) {
        .cuadrado => |c| c.lado * c.lado,
        .rectangulo => |r| r.ancho * r.alto,
    };

    try std.io.getStdOut().writer().print("area={d}\n", .{area});
}
```

### Nim

```nim
import std/strutils

type
  Clase = enum
    cuadrado, rectangulo

  # Object variant: el campo discriminante decide qué otros campos existen.
  Figura = object
    case clase: Clase
    of cuadrado:
      lado: int
    of rectangulo:
      ancho, alto: int

let campos = stdin.readLine().splitWhitespace()
let figura =
  if campos[0] == "cuadrado": Figura(clase: cuadrado, lado: parseInt(campos[1]))
  else: Figura(clase: rectangulo, ancho: parseInt(campos[1]), alto: parseInt(campos[2]))

let area =
  case figura.clase
  of cuadrado: figura.lado * figura.lado
  of rectangulo: figura.ancho * figura.alto

echo "area=", area
```

### D

```d
import std.stdio, std.conv, std.array, std.string, std.sumtype;

struct Cuadrado { int lado; }
struct Rectangulo { int ancho, alto; }

// SumType vive en la biblioteca (std.sumtype), no en el lenguaje.
alias Figura = SumType!(Cuadrado, Rectangulo);

void main() {
    auto campos = readln().strip().split();
    Figura figura = campos[0] == "cuadrado"
        ? Figura(Cuadrado(campos[1].to!int))
        : Figura(Rectangulo(campos[1].to!int, campos[2].to!int));

    // match! no compila si algún miembro del SumType queda sin manejar.
    const area = figura.match!(
        (Cuadrado c) => c.lado * c.lado,
        (Rectangulo r) => r.ancho * r.alto
    );

    writeln("area=", area);
}
```

**Qué reconocer:** los tres tienen tipo suma y los tres lo colocan en un sitio distinto. Zig lo pone
**en el lenguaje**: `union(enum)` genera la etiqueta automáticamente, el `switch` desempaqueta el
contenido con `|c|`, y omitir una etiqueta es un error de compilación —la misma garantía que el
`enum` con `match` de Rust, en un lenguaje sin recolector de basura ni excepciones—. Nim lo pone
también en el lenguaje pero con una vuelta de tuerca: en un *object variant* el discriminante es un
campo normal y los demás campos dependen de él, así que acceder a `figura.ancho` en un cuadrado
compila y falla al ejecutar con `FieldDefect`; la comprobación existe, pero es en tiempo de ejecución.
D lo pone **en la biblioteca**: `SumType` es una plantilla de `std.sumtype`, y `match!` consigue la
exhaustividad usando metaprogramación en tiempo de compilación —la garantía es igual de fuerte, pero
el error que te da el compilador es el de una plantilla, no el de una construcción del lenguaje—.
Tres niveles de integración para la misma idea, y el más pobre de todos sigue siendo el de Go, que
obliga a usar una interfaz vacía y aserciones de tipo.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). En SQL las variantes se modelan con columnas
anulables o con una tabla por tipo, y ninguna de las dos opciones impide una fila incoherente.

### Prolog

```prolog
:- initialization(main, main).

% En Prolog el término compuesto ES el tipo algebraico: cuadrado/1 y
% rectangulo/2 son dos constructores distintos del mismo dato, y la
% coincidencia de patrones es, literalmente, la unificación.
area(cuadrado(Lado), A) :- A is Lado * Lado.
area(rectangulo(Ancho, Alto), A) :- A is Ancho * Alto.

leer_figura(["cuadrado", L], cuadrado(Lado)) :-
    number_string(Lado, L).
leer_figura(["rectangulo", An, Al], rectangulo(Ancho, Alto)) :-
    number_string(Ancho, An),
    number_string(Alto, Al).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes),
    exclude(==(""), Partes, Campos),
    leer_figura(Campos, Figura),
    area(Figura, A),
    format("area=~w~n", [A]).
```

### Datalog

```datalog
% Datalog no tiene símbolos de función: no puede construir cuadrado(5) como
% término, ni leer stdin. Cada constructor se codifica como una relación
% distinta, y el "tipo suma" es la unión de las dos reglas de area/2.
cuadrado(f1, 5).
rectangulo(f2, 3, 4).

area(F, A) :- cuadrado(F, L), A = L * L.
area(F, A) :- rectangulo(F, An, Al), A = An * Al.
```

**Qué reconocer:** Prolog llega a esta clase sin necesitar ninguna construcción nueva, y ese es el
hallazgo. Un **término compuesto es un tipo algebraico**: `cuadrado(5)` y `rectangulo(3, 4)` son dos
valores del mismo dominio con functor distinto, exactamente lo que F# escribe como
`Cuadrado of int | Rectangulo of int * int`, salvo que en Prolog no hay que declararlo. Y la
coincidencia de patrones que Scala, F#, Rust o Zig implementan como una construcción del compilador
aquí **es el motor mismo del lenguaje**: escribir `area(cuadrado(Lado), A)` en la cabeza de la regla
no es sintaxis de despacho, es unificación, la misma operación con la que Prolog resuelve todo lo
demás. El precio es que no hay comprobación de exhaustividad ni de tipos: si llega
`triangulo(3, 4, 5)`, `area/2` simplemente **falla**, sin error y sin aviso previo. Datalog marca el
límite exacto: al prohibir los símbolos de función pierde la capacidad de tener `cuadrado(5)` como
valor, y solo puede repartir las variantes en relaciones separadas; el tipo suma sobrevive como las
dos reglas de `area/2`, que es la definición por casos vista desde el otro lado.

---

## Y de vuelta a la clase

Veinte lenguajes, dos figuras, y tres respuestas distintas a la misma pregunta. Unos definen el tipo
por sus formas posibles y el compilador te obliga a tratarlas todas; otros ponen una etiqueta y
confían en tu disciplina; Prolog no necesita definir nada porque su dato ya era un tipo algebraico.
Lo transferible es la pregunta: cuando añadas una variante mañana, ¿te avisará alguien de los sitios
que se quedaron sin actualizar?

⏮️ [Volver a la clase 100](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
