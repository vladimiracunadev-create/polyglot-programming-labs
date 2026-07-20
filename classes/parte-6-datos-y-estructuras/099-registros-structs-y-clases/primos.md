# 🧬 El mismo programa en las familias de lenguajes — Clase 099

> [⬅️ Volver a la clase 099](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —construir un registro `Persona` con nombre y edad y
mostrarlo formateado— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Agrupar dos campos bajo un nombre parece el concepto más inocente del curso, y sin embargo es donde
cada familia enseña su decisión más profunda: si un registro es un **valor** que se copia o una
**referencia** que se comparte, si los campos son parte del tipo o solo claves de un diccionario, y
quién escribe el texto que representa el objeto.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `nombre edad` (una palabra y un entero)
- **Salida** (stdout): `Persona(nombre=<nombre>, edad=<edad>)`
- **Regla:** un registro con dos campos, `nombre` y `edad`

| stdin | esperado |
|---|---|
| `Ada 36` | `Persona(nombre=Ada, edad=36)` |
| `Bo 5` | `Persona(nombre=Bo, edad=5)` |
| `Cy 99` | `Persona(nombre=Cy, edad=99)` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
En esta familia el registro es opcional: siempre puedes usar un diccionario y seguir adelante. Lo
interesante es qué ofrece cada lenguaje a quien prefiere declarar la forma del dato.

### Ruby

```ruby
# Struct genera constructor, lectores y comparación por valor.
Persona = Struct.new(:nombre, :edad)

nombre, edad = STDIN.gets.split
persona = Persona.new(nombre, edad.to_i)
puts "Persona(nombre=#{persona.nombre}, edad=#{persona.edad})"
```

### Perl

```perl
# El registro de Perl es una referencia a hash; -> es el acceso a campo.
my ($nombre, $edad) = split ' ', <STDIN>;
my $persona = { nombre => $nombre, edad => 0 + $edad };
printf "Persona(nombre=%s, edad=%d)\n", $persona->{nombre}, $persona->{edad};
```

### Lua

```lua
-- Una tabla más una metatabla: eso es todo lo que Lua ofrece como "clase".
local Persona = {}
Persona.__index = Persona

function Persona.new(nombre, edad)
  return setmetatable({ nombre = nombre, edad = edad }, Persona)
end

function Persona:__tostring()
  return string.format("Persona(nombre=%s, edad=%d)", self.nombre, self.edad)
end

local nombre, edad = io.read("l"):match("(%S+)%s+(%d+)")
print(tostring(Persona.new(nombre, tonumber(edad))))
```

### Tcl

```tcl
gets stdin linea
lassign [split [string trim $linea]] nombre edad
set persona [dict create nombre $nombre edad $edad]
puts "Persona(nombre=[dict get $persona nombre], edad=[dict get $persona edad])"
```

### R

```r
partes <- strsplit(trimws(readLines("stdin", n = 1)), "\\s+")[[1]]
persona <- list(nombre = partes[1], edad = as.integer(partes[2]))
cat(sprintf("Persona(nombre=%s, edad=%d)\n", persona$nombre, persona$edad))
```

**Qué reconocer:** los cinco guardan pares clave-valor, pero solo Ruby tiene un **registro de
verdad**: `Struct.new(:nombre, :edad)` fabrica una clase con constructor, lectores y comparación por
valor, y en Ruby 3.2 en adelante `Data.define` hace lo mismo pero inmutable. Perl no tiene registro
alguno: usa una **referencia a hash**, y por eso `$persona->{apelido}` con una errata no falla, solo
devuelve `undef`. Lua enseña su mecanismo más característico, la **metatabla**: `Persona.__index`
convierte una tabla cualquiera en el "molde" al que la instancia pregunta cuando no encuentra un
campo, y `__tostring` es el gancho que `print` consulta para imprimir el objeto —una clase en Lua no
es una construcción del lenguaje, es un patrón que el programador arma—. Tcl y R usan sus
diccionarios genéricos (`dict`, `list` con nombres) sin ceremonia; en R el propio `list` con nombres
es la base sobre la que se construyen `data.frame` y las clases S3.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

class Persona {
  final String nombre;
  final int edad;
  const Persona(this.nombre, this.edad);

  @override
  String toString() => 'Persona(nombre=$nombre, edad=$edad)';
}

void main() {
  final campos = stdin.readLineSync()!.trim().split(RegExp(r'\s+'));
  print(Persona(campos[0], int.parse(campos[1])));
}
```

### ActionScript 3

```actionscript
// Sin stdin en el reproductor Flash: se ilustran los campos tipados y su formato.
package {
    public class Persona {
        public var nombre:String;
        public var edad:int;

        public function Persona(nombre:String, edad:int) {
            this.nombre = nombre;
            this.edad = edad;
        }

        public function toString():String {
            return "Persona(nombre=" + nombre + ", edad=" + edad + ")";
        }
    }
}
```

**Qué reconocer:** los dos declaran los campos con tipo, como haría TypeScript con una `interface`,
pero con una diferencia que el núcleo no muestra: en TypeScript los tipos **desaparecen al
compilar**, mientras que aquí `edad:int` en ActionScript y `final int edad` en Dart existen en tiempo
de ejecución. El azúcar de Dart es `const Persona(this.nombre, this.edad)`: el `this.` en el
parámetro asigna el campo directamente, evitando las tres líneas de asignación que ActionScript
escribe a mano. Y en ambos el texto del registro sale de sobrescribir `toString`, el mismo contrato
que `print` y la concatenación consultan, igual que en JavaScript.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Java tardó veinte años en tener `record`; los
primos llegaron antes y por caminos distintos.

### Kotlin

```kotlin
data class Persona(val nombre: String, val edad: Int)

fun main() {
    val (nombre, edad) = readLine()!!.trim().split(Regex("\\s+"))
    // El toString generado por `data class` produce literalmente el formato pedido.
    println(Persona(nombre, edad.toInt()))
}
```

### Scala

```scala
case class Persona(nombre: String, edad: Int)

object Registro extends App {
  val Array(nombre, edad) = scala.io.StdIn.readLine().trim.split("\\s+")
  val persona = Persona(nombre, edad.toInt)
  // Ojo: el toString de una case class es "Persona(Ada,36)", sin nombres de campo.
  println(s"Persona(nombre=${persona.nombre}, edad=${persona.edad})")
}
```

### Groovy

```groovy
@groovy.transform.Canonical
class Persona {
    String nombre
    int edad
}

def (nombre, edad) = System.in.newReader().readLine().trim().split(/\s+/)
def persona = new Persona(nombre: nombre, edad: edad as int)
println "Persona(nombre=${persona.nombre}, edad=${persona.edad})"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(defrecord Persona [nombre edad])

(let [[nombre edad] (str/split (str/trim (read-line)) #"\s+")
      persona (->Persona nombre (Integer/parseInt edad))]
  (println (format "Persona(nombre=%s, edad=%d)" (:nombre persona) (:edad persona))))
```

**Qué reconocer:** los cuatro generan por ti el constructor, los accesores, `equals`, `hashCode` y
`toString` —eso es lo que significa "registro" en la JVM—, pero el texto generado **no coincide**
entre ellos. Kotlin escribe `Persona(nombre=Ada, edad=36)`, que da la casualidad de ser exactamente
el contrato de esta clase; Scala escribe `Persona(Ada,36)`, sin nombres de campo, así que hay que
formatear a mano; Groovy con `@Canonical` produce `Persona(Ada, 36)`. La lección es que "el registro
sabe imprimirse" es cierto en los cuatro y **portable en ninguno**. Clojure va por otro lado:
`defrecord` crea un tipo real de la JVM que además sigue comportándose como un mapa, de modo que
`(:nombre persona)` es la misma operación que usarías con `{:nombre "Ada"}` —el registro es una
optimización del mapa, no una categoría distinta—.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
// Un record de F# es inmutable y se compara por valor, sin escribir nada más.
type Persona = { Nombre: string; Edad: int }

let campos =
    stdin.ReadLine().Trim().Split(' ')
    |> Array.filter (fun s -> s <> "")

let persona = { Nombre = campos.[0]; Edad = int campos.[1] }
printfn "Persona(nombre=%s, edad=%d)" persona.Nombre persona.Edad
```

### VB.NET

```vbnet
Imports System

Module Registro
    ' Structure es tipo por valor: al asignarla se copia entera.
    Structure Persona
        Public Nombre As String
        Public Edad As Integer
    End Structure

    Sub Main()
        Dim campos = Console.ReadLine().Trim().Split(" "c, StringSplitOptions.RemoveEmptyEntries)
        Dim persona As Persona
        persona.Nombre = campos(0)
        persona.Edad = Integer.Parse(campos(1))
        Console.WriteLine($"Persona(nombre={persona.Nombre}, edad={persona.Edad})")
    End Sub
End Module
```

**Qué reconocer:** el CLR distingue desde siempre entre **tipos por valor** (`Structure`) y **tipos
por referencia** (`Class`), y esa elección cambia el comportamiento del programa, no solo el
rendimiento: asignar una `Persona` declarada como `Structure` copia los dos campos, mientras que con
`Class` ambas variables apuntarían al mismo objeto. VB.NET además no exige constructor —`Dim persona
As Persona` ya deja los campos con su valor por defecto—, lo que es imposible con una clase. F#
añade encima lo que el CLR no da: su `record` es inmutable por defecto, se compara por valor aunque
viva en el montón, y se copia con cambios usando `{ persona with Edad = 37 }`. Es la misma idea que
los `record` de C# 9 tomaron prestada de aquí.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). El `struct` de C es memoria contigua y nada más: sin
métodos, sin constructor y sin forma de imprimirse.

### C++

```cpp
#include <iostream>
#include <string>

// struct y class son la misma construcción: solo cambia la visibilidad por
// defecto (public en struct, private en class).
struct Persona {
    std::string nombre;
    int edad;
};

std::ostream& operator<<(std::ostream& os, const Persona& p) {
    return os << "Persona(nombre=" << p.nombre << ", edad=" << p.edad << ")";
}

int main() {
    Persona persona;
    std::cin >> persona.nombre >> persona.edad;
    std::cout << persona << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

// @interface declara qué se ve desde fuera; @implementation, cómo funciona.
@interface Persona : NSObject
@property (copy) NSString *nombre;
@property (assign) NSInteger edad;
@end

@implementation Persona
- (NSString *)description {
    return [NSString stringWithFormat:@"Persona(nombre=%@, edad=%ld)", self.nombre, (long)self.edad];
}
@end

int main(void) {
    @autoreleasepool {
        char buf[128];
        long edad;
        scanf("%127s %ld", buf, &edad);

        Persona *persona = [Persona new];
        persona.nombre = [NSString stringWithUTF8String:buf];
        persona.edad = edad;

        printf("%s\n", [[persona description] UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** C++ conserva el `struct` de C intacto —el código de la clase compila tal cual— y
le añade la posibilidad de tener métodos, constructores y operadores. El detalle que sorprende a
quien viene de Java es que en C++ **`struct` y `class` son la misma palabra con distinto ajuste por
defecto**: los miembros de un `struct` son públicos, los de un `class` privados, y ahí acaba la
diferencia; la convención dice usar `struct` para agregados de datos y `class` cuando hay invariantes
que proteger. Objective-C parte el tipo en dos bloques —`@interface` con lo que el resto del programa
puede usar, `@implementation` con el cuerpo—, herencia directa de los archivos `.h` y `.c` de C, y
sustituye los campos por `@property`, que genera los accesores y declara la política de memoria:
`(copy)` para la cadena, porque `NSString` puede ser mutable y conviene quedarse con una copia
propia. El texto del registro no sale de un `toString` sino de `description`, el método que todo
`NSObject` hereda.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Aquí el registro es la
unidad básica de diseño y su disposición en memoria importa.

### Zig

```zig
const std = @import("std");

const Persona = struct {
    nombre: []const u8,
    edad: u32,
};

pub fn main() !void {
    var buf: [128]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \t\r");

    const persona = Persona{
        .nombre = it.next().?,
        .edad = try std.fmt.parseInt(u32, it.next().?, 10),
    };

    try std.io.getStdOut().writer().print(
        "Persona(nombre={s}, edad={d})\n",
        .{ persona.nombre, persona.edad },
    );
}
```

### Nim

```nim
import std/strutils

type Persona = object
  nombre: string
  edad: int

let campos = stdin.readLine().splitWhitespace()
let persona = Persona(nombre: campos[0], edad: parseInt(campos[1]))
echo "Persona(nombre=", persona.nombre, ", edad=", persona.edad, ")"
```

### D

```d
import std.stdio, std.conv, std.array, std.string;

struct Persona {
    string nombre;
    int edad;

    string toString() const {
        return format("Persona(nombre=%s, edad=%d)", nombre, edad);
    }
}

void main() {
    auto campos = readln().strip().split();
    auto persona = Persona(campos[0], campos[1].to!int);
    writeln(persona);
}
```

**Qué reconocer:** en los tres el registro es un **valor**: ocupa el sitio donde lo declaras, se copia
al asignarlo y no hay puntero escondido, exactamente como el `struct` de Go y Rust. La construcción
por campos nombrados —`Persona{ .nombre = ..., .edad = ... }` en Zig, `Persona(nombre: ..., edad: ...)`
en Nim— es el mismo gesto que `Persona{nombre: "Ada"}` en Go, y sirve para lo mismo: que añadir un
campo no rompa el orden de los argumentos. La separación clave la marca D, que tiene **`struct` y
`class` como cosas distintas de verdad** —`struct` por valor sin herencia, `class` por referencia con
recolector de basura y polimorfismo—, justo lo contrario de C++, donde ambas palabras significan casi
lo mismo. Y fíjate en el `[]const u8` de Zig: el nombre no es una cadena propia sino una **vista** al
búfer de entrada, así que la persona no sobrevive a `buf`; ese tipo de detalle es lo que Rust obliga
a declarar con tiempos de vida y Zig te deja llevar en la cabeza.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Una fila de una tabla es el registro original:
columnas con nombre y tipo, y ninguna operación asociada.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", [Nombre, EdadS]),
    number_string(Edad, EdadS),
    Persona = persona(Nombre, Edad),
    % El "acceso a campo" es unificar contra la forma del término.
    persona(N, E) = Persona,
    format("Persona(nombre=~w, edad=~w)~n", [N, E]).
```

### Datalog

```datalog
% Datalog no tiene E/S: el registro es una fila de una relación y los campos
% son sus posiciones, sin nombre propio.
persona("Ada", 36).

adulta(N) :- persona(N, E), E >= 18.
```

**Qué reconocer:** en Prolog el registro es un **término compuesto**: `persona(Nombre, Edad)` tiene
un functor y dos argumentos, y leer un campo no es una operación sino **unificar** el término contra
un patrón con variables donde quieres los valores. No hay accesores porque no hacen falta, y no hay
tipo declarado: `persona/2` y `persona/3` serían functores distintos sin ninguna relación entre sí.
Datalog reduce todavía más: un registro es una fila de una relación, los campos son posiciones, y
como no hay símbolos de función tampoco pueden anidarse registros dentro de registros —no existe una
`persona` que contenga una `direccion`—. Esa limitación es la misma que empuja a SQL a normalizar en
varias tablas con claves ajenas en lugar de anidar estructuras.

---

## Y de vuelta a la clase

Veinte lenguajes, dos campos, y la misma idea repetida: dar nombre a un grupo de datos para poder
hablar de ellos como una unidad. Lo que cambia es cuánto trabajo hace el lenguaje por ti —constructor,
comparación, texto— y si el registro se copia o se comparte. Eso es lo transferible.

⏮️ [Volver a la clase 099](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
