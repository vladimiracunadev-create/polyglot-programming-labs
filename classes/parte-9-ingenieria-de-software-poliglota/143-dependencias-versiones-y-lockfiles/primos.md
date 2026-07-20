# 🧬 El mismo programa en las familias de lenguajes — Clase 143

> [⬅️ Volver a la clase 143](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —descomponer una versión semántica en sus tres
números— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo
por los diez lenguajes del núcleo.

Aquí el ejercicio tiene un premio extra: partir `mayor.menor.parche` es exactamente lo que hace el
resolutor de dependencias de cada ecosistema antes de escribir una línea en el lockfile. Así que
cada primo llega acompañado del gestor de paquetes y del archivo donde ese gestor congela lo que
resolvió.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): una versión `mayor.menor.parche`
- **Salida** (stdout): `mayor=<M> menor=<m> parche=<p>`
- **Regla:** separar la versión por puntos y convertir cada parte a entero

| stdin | esperado |
|---|---|
| `1.2.3` | `mayor=1 menor=2 parche=3` |
| `0.5.10` | `mayor=0 menor=5 parche=10` |
| `2.0.0` | `mayor=2 menor=0 parche=0` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Tipado dinámico y poca ceremonia: la línea llega como texto y el lenguaje no obliga a declarar que
esas tres piezas son números.

### Ruby

```ruby
mayor, menor, parche = STDIN.gets.strip.split(".").map(&:to_i)
puts "mayor=#{mayor} menor=#{menor} parche=#{parche}"
```

### Perl

```perl
chomp(my $v = <STDIN>);
my ($mayor, $menor, $parche) = split /\./, $v;
printf "mayor=%d menor=%d parche=%d\n", $mayor, $menor, $parche;
```

### Lua

```lua
local v = io.read("l")
local mayor, menor, parche = v:match("^(%d+)%.(%d+)%.(%d+)$")
print(string.format("mayor=%d menor=%d parche=%d",
    tonumber(mayor), tonumber(menor), tonumber(parche)))
```

### Tcl

```tcl
gets stdin v
lassign [split [string trim $v] .] mayor menor parche
puts "mayor=$mayor menor=$menor parche=$parche"
```

### R

```r
v <- as.integer(strsplit(readLines("stdin", n = 1), ".", fixed = TRUE)[[1]])
cat(sprintf("mayor=%d menor=%d parche=%d\n", v[1], v[2], v[3]))
```

**Qué reconocer:** el punto es un carácter especial en las expresiones regulares, y aquí se ve quién
lo trata como regex y quién no: Perl escribe `/\./`, R desactiva el motor con `fixed = TRUE`, Lua lo
escapa como `%.` y Tcl —donde `split` recibe caracteres literales, no un patrón— no necesita escapar
nada. Esa misma división atraviesa los gestores de paquetes de la familia. **Ruby** fue de los
primeros en resolver el problema completo: **Bundler** lee el `Gemfile` con sus restricciones
(`~> 1.2`, `>= 0.5.10`) y escribe **`Gemfile.lock`** con la versión exacta de cada gema y de sus
dependencias transitivas — uno de los primeros lockfiles de la industria, y el modelo que después
copiaron media docena de ecosistemas. **Perl** llega al mismo sitio con **CPAN/cpanm** y un
`cpanfile` cuyo congelado se guarda en **`cpanfile.snapshot`** (vía Carton). **Lua** usa
**LuaRocks**, donde el `.rockspec` declara las dependencias pero no hay un lockfile canónico
equivalente. **R** vive sobre **CRAN**, que históricamente solo sirve la última versión de cada
paquete —de ahí que **renv** tuviera que inventar `renv.lock` para poder reconstruir un proyecto
años después—. Y **Tcl** distribuye con **teacup** sobre repositorios TEApot. Cinco lenguajes de la
misma familia, cinco grados distintos de reproducibilidad.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final p = stdin.readLineSync()!.trim().split('.').map(int.parse).toList();
  print('mayor=${p[0]} menor=${p[1]} parche=${p[2]}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra la descomposición.
package {
    public class Version {
        public static function descomponer(v:String):String {
            var p:Array = v.split(".");
            return "mayor=" + int(p[0]) + " menor=" + int(p[1]) + " parche=" + int(p[2]);
        }
    }
}
```

**Qué reconocer:** `split('.')` es idéntico al de JavaScript porque ambos heredan la API de cadenas
de ECMAScript; lo que Dart añade es el tipo estático y el `!` que afirma que la lectura no fue nula.
En dependencias, Dart es el pariente que se tomó en serio la lección de npm: **pub** lee
`pubspec.yaml` y escribe **`pubspec.lock`**, con la misma separación entre *rango declarado* y
*versión resuelta* que hay entre `package.json` y `package-lock.json`. ActionScript, en cambio, es
el recordatorio de qué pasa cuando un ecosistema muere sin un gestor central: las bibliotecas se
distribuían como `.swc` copiados a mano, y no existe ningún archivo que permita reconstruir hoy la
compilación de 2009.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos compilan al mismo bytecode y comparten
biblioteca estándar; lo que cambia es cuánta ceremonia exigen y qué herramienta de construcción
adoptan.

### Kotlin

```kotlin
fun main() {
    val (mayor, menor, parche) = readLine()!!.trim().split(".").map { it.toInt() }
    println("mayor=$mayor menor=$menor parche=$parche")
}
```

### Scala

```scala
object Version extends App {
  val Array(mayor, menor, parche) =
    scala.io.StdIn.readLine().trim.split("\\.").map(_.toInt)
  println(s"mayor=$mayor menor=$menor parche=$parche")
}
```

### Groovy

```groovy
def (mayor, menor, parche) = System.in.newReader().readLine().trim().split('\\.')*.toInteger()
println "mayor=$mayor menor=$menor parche=$parche"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [[mayor menor parche] (map parse-long (str/split (str/trim (read-line)) #"\."))]
  (println (str "mayor=" mayor " menor=" menor " parche=" parche)))
```

**Qué reconocer:** Scala y Groovy escriben `"\\."` y Clojure `#"\."` porque acaban llamando a
`String.split` de Java, que interpreta su argumento como **expresión regular** — la trampa más
clásica de la plataforma. Kotlin es la excepción: su `split(".")` con `String` literal *no* es
regex, y por eso funciona sin escapar. La misma convergencia se repite en las dependencias:
**Maven** impuso las coordenadas `groupId:artifactId:version` y el repositorio central, y **Gradle**
las heredó; entre los dos dan servicio a **Kotlin** y **Groovy** (que además es el lenguaje del
`build.gradle` clásico), mientras **Scala** prefiere **sbt** y **Clojure** se sale del molde con
**`deps.edn`** o **Leiningen** (`project.clj`). El detalle que duele: Maven **no tiene lockfile** —
resuelve conflictos con la regla de "la declaración más cercana gana", así que dos `mvn install` en
fechas distintas pueden producir árboles distintos si alguien usó un rango. Gradle sí ofrece
bloqueo, pero es opcional (`gradle.lockfile`) y hay que activarlo a mano.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let [| mayor; menor; parche |] =
    stdin.ReadLine().Trim().Split('.') |> Array.map int
printfn "mayor=%d menor=%d parche=%d" mayor menor parche
```

### VB.NET

```vbnet
Imports System

Module Version
    Sub Main()
        Dim p = Console.ReadLine().Trim().Split("."c)
        Console.WriteLine("mayor={0} menor={1} parche={2}",
                          Integer.Parse(p(0)), Integer.Parse(p(1)), Integer.Parse(p(2)))
    End Sub
End Module
```

**Qué reconocer:** los dos llaman al mismo `String.Split` del CLR, que a diferencia del de Java
recibe **caracteres literales** — de ahí `'.'` en F# y `"."c` en VB, sin escapes ni regex. F# muestra
el otro extremo estilístico con `|>` encadenando en vez de anidar. En dependencias comparten
**NuGet** hasta el último detalle: el `<PackageReference Include="..." Version="..." />` del
`.csproj`, `.fsproj` o `.vbproj` es idéntico, y el bloqueo se activa con
`RestorePackagesWithLockFile`, que genera **`packages.lock.json`**. Es el caso más limpio de esta
página: tres lenguajes distintos, un solo gestor, un solo formato de lockfile, cero fragmentación.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Memoria explícita, tipos declarados y `printf`.

### C++

```cpp
#include <iostream>
#include <sstream>
#include <string>

int main() {
    std::string linea;
    std::getline(std::cin, linea);
    std::istringstream in(linea);
    std::string mayor, menor, parche;
    std::getline(in, mayor, '.');
    std::getline(in, menor, '.');
    std::getline(in, parche, '.');
    std::cout << "mayor=" << std::stoi(mayor)
              << " menor=" << std::stoi(menor)
              << " parche=" << std::stoi(parche) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        char buf[64];
        fgets(buf, sizeof buf, stdin);
        NSString *v = [[NSString stringWithUTF8String:buf]
            stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]];
        NSArray<NSString *> *p = [v componentsSeparatedByString:@"."];
        printf("mayor=%d menor=%d parche=%d\n",
               [p[0] intValue], [p[1] intValue], [p[2] intValue]);
    }
    return 0;
}
```

**Qué reconocer:** ambos son **superconjuntos de C** —`fgets` y `printf` siguen ahí intactos en
Objective-C— y ambos tienen que construir a mano el "partir por puntos" que en la familia de
scripting es una sola llamada: C++ reutiliza `std::getline` con delimitador sobre un
`istringstream`, Objective-C recurre a la capa de objetos con `componentsSeparatedByString:`. Y aquí
está el caso más doloroso y más honesto de toda la página: **C++ no tiene gestor de paquetes
oficial**. **Conan** y **vcpkg** compiten sin que ninguno haya ganado, y una parte enorme del mundo
real sigue resolviendo dependencias con submódulos de Git, `FetchContent` de CMake o carpetas
`third_party/` copiadas a mano. Decirlo así es más útil que fingir uniformidad: cuando leas un
proyecto C++ no busques el lockfile, busca **cuál** de los cinco mecanismos eligieron. Objective-C
tuvo más suerte precisamente por venir después — **CocoaPods** trajo `Podfile` y **`Podfile.lock`**,
y fue uno de los gestores que consolidó la idea del lockfile fuera de Ruby (no por casualidad:
CocoaPods está escrito en Ruby).

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin máquina
virtual, y con gestores de paquetes diseñados desde el primer día en vez de añadidos veinte años
después.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.splitScalar(u8, std.mem.trim(u8, linea, " \r"), '.');
    const mayor = try std.fmt.parseInt(u32, it.next().?, 10);
    const menor = try std.fmt.parseInt(u32, it.next().?, 10);
    const parche = try std.fmt.parseInt(u32, it.next().?, 10);
    try std.io.getStdOut().writer().print(
        "mayor={d} menor={d} parche={d}\n", .{ mayor, menor, parche });
}
```

### Nim

```nim
import std/[strutils, sequtils]

let p = stdin.readLine().strip().split('.').map(parseInt)
echo "mayor=", p[0], " menor=", p[1], " parche=", p[2]
```

### D

```d
import std.stdio, std.string, std.array, std.conv, std.algorithm;

void main() {
    auto p = readln().strip().split('.').map!(to!int).array;
    writefln("mayor=%d menor=%d parche=%d", p[0], p[1], p[2]);
}
```

**Qué reconocer:** Zig es el más explícito —reserva el búfer a mano y cada operación que puede
fallar lleva `try`, igual que Rust obliga a tratar el error—, mientras Nim y D esconden esa
maquinaria tras una sintaxis de scripting sin dejar de compilar a binario nativo. En dependencias
los tres son jóvenes y se nota. **Zig** no tiene registro central: su gestor declara las
dependencias en **`build.zig.zon`** con la **URL y el hash del contenido** de cada una, de modo que
el propio manifiesto *es* el lockfile — si el archivo remoto cambia un solo byte, la construcción
falla. **Nim** usa **Nimble**, con un archivo `.nimble` y un `nimble.lock` opcional. **D** distribuye
con **DUB**, que sí separa las dos mitades del problema: `dub.json` declara los rangos y
**`dub.selections.json`** guarda la versión exacta elegida — el mismo par declaración/resolución que
`Cargo.toml` y `Cargo.lock`.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** se quiere, no **cómo**
calcularlo paso a paso.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, ".", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, [Mayor, Menor, Parche]),
    format("mayor=~d menor=~d parche=~d~n", [Mayor, Menor, Parche]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S ni funciones de cadena: la versión no se puede
% "partir", solo declarar ya descompuesta como hecho.
version(1, 2, 3).

componentes(M, N, P) :- version(M, N, P).
```

**Qué reconocer:** en Prolog la descomposición se escribe como **unificación**: `maplist` no
"devuelve" tres valores, sino que liga `[Mayor, Menor, Parche]` con la lista resultante, y por eso
el patrón de tres elementos también actúa como validación —si la versión trajera cuatro números, el
objetivo simplemente fallaría—. Datalog lleva la renuncia al extremo y resulta útil justamente por
eso: sin cadenas ni efectos, una versión solo puede existir como **hecho** `version(1, 2, 3)`, que
es exactamente la forma que tiene una entrada de lockfile una vez resuelta. Y no es una analogía
gratuita: los resolutores modernos de dependencias (el de Cargo, el de PubGrub, el de Dart) están
construidos como **solucionadores SAT** sobre restricciones declaradas, la misma familia de motores
que hay detrás de Prolog. La versión en Prolog se distribuye, por cierto, con los `packs` de SWI
(`pack_install/1`); Datalog no tiene ecosistema que gestionar.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo esqueleto en todos: leer, partir por puntos,
convertir. Lo que cambia es la **forma** —y, sobre todo, lo que cada ecosistema hace con esos tres
números cuando se los toma en serio: desde el `Gemfile.lock` de Bundler hasta el hash de contenido
de Zig, pasando por el hueco que C++ todavía no ha llenado. Eso es lo transferible.

⏮️ [Volver a la clase 143](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
