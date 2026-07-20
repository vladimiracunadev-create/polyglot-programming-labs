# 🧬 El mismo programa en las familias de lenguajes — Clase 145

> [⬅️ Volver a la clase 145](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —contar cuántos commits hay en un historial—
resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los
diez lenguajes del núcleo.

Git es la única herramienta de esta parte del curso que **no** se fragmenta por lenguaje: el mismo
`git log` cuenta commits de Ruby, de Zig y de Prolog. Lo que sí se fragmenta es qué archivos entran
en ese historial, y ahí cada ecosistema arrastra su gestor de paquetes, su lockfile y su carpeta de
artefactos generados. De eso hablan los párrafos de cada familia.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): mensajes de commit separados por espacio
- **Salida** (stdout): `commits=<cantidad>`
- **Regla:** contar cuántos mensajes hay en la línea

| stdin | esperado |
|---|---|
| `fix add refactor` | `commits=3` |
| `init` | `commits=1` |
| `a b c d` | `commits=4` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Tipado dinámico y poca ceremonia: partir por espacios y contar cabe en una línea.

### Ruby

```ruby
puts "commits=#{STDIN.gets.split.size}"
```

### Perl

```perl
my @msgs = split ' ', <STDIN>;
printf "commits=%d\n", scalar @msgs;
```

### Lua

```lua
local n = 0
for _ in io.read("l"):gmatch("%S+") do
    n = n + 1
end
print(string.format("commits=%d", n))
```

### Tcl

```tcl
gets stdin linea
puts "commits=[llength $linea]"
```

### R

```r
msgs <- scan("stdin", what = character(), quiet = TRUE)
cat(sprintf("commits=%d\n", length(msgs)))
```

**Qué reconocer:** cuatro de los cinco tienen una operación que devuelve el tamaño de una colección
(`size`, `scalar`, `llength`, `length`); solo Lua obliga a contar a mano, porque su `gmatch` entrega
un **iterador** y el `#` de Lua mide tablas, no coincidencias. Tcl gana por goleada en brevedad
—`llength` sobre la línea sin partirla, porque en Tcl una cadena separada por espacios **ya es** una
lista—. En Git, esta familia comparte un dilema y lo resuelve distinto según el gestor. La regla que
casi todos siguen: **el lockfile se versiona en las aplicaciones y se discute en las bibliotecas**.
**Ruby** lo tiene zanjado desde hace más de una década — `Gemfile.lock`, uno de los primeros
lockfiles de la industria, va al repositorio en una aplicación y se ignora en una gema. **Perl**
versiona el `cpanfile` y, si usa Carton, también **`cpanfile.snapshot`**. **Lua** commitea el
`.rockspec` de **LuaRocks** pero no la carpeta `lua_modules/`. **R** vive el caso más incómodo:
además de `renv.lock`, el `.gitignore` tiene que excluir `.Rhistory` y `.RData`, que RStudio escribe
solos y que filtran datos del análisis al historial sin que nadie lo pida. **Tcl** con **teacup**
apenas genera artefactos que ignorar. En todos, la carpeta de dependencias descargadas se ignora y
el archivo que las describe se versiona: ese es el patrón transferible.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final msgs = stdin.readLineSync()!.trim().split(RegExp(r'\s+'));
  print('commits=${msgs.length}');
}
```

### ActionScript 3

```actionscript
// Sin stdin en el reproductor Flash: se ilustra el conteo sobre la línea ya recibida.
package {
    public class Historial {
        public static function contar(linea:String):String {
            return "commits=" + linea.split(/\s+/).length;
        }
    }
}
```

**Qué reconocer:** `.length` sobre el resultado de `split` es idéntico en los dos y en JavaScript;
Dart solo añade el `!` que afirma que la lectura no fue nula y el `RegExp` explícito. En Git, esta
familia es donde más ruido genera el gestor de paquetes: `node_modules/` y el `.dart_tool/` de Dart
se ignoran siempre, mientras `pubspec.lock` —el equivalente de `package-lock.json`— se versiona en
aplicaciones. El otro conflicto clásico es el **código generado**: TypeScript produce `.js`, Dart
produce `.g.dart` con `build_runner`, y meterlos en el repositorio convierte cada pull request en un
diff ilegible. La regla práctica que sale de aquí sirve para todo el curso: **si una herramienta lo
puede regenerar, no va al historial**; si describe *qué* regenerar, sí.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos compilan al mismo bytecode y comparten
repositorio de artefactos; lo que cambia es la herramienta de construcción que cada uno commitea.

### Kotlin

```kotlin
fun main() {
    val msgs = readLine()!!.trim().split(Regex("\\s+"))
    println("commits=${msgs.size}")
}
```

### Scala

```scala
object Historial extends App {
  val msgs = scala.io.StdIn.readLine().trim.split("\\s+")
  println(s"commits=${msgs.length}")
}
```

### Groovy

```groovy
def msgs = System.in.newReader().readLine().trim().split(/\s+/)
println "commits=${msgs.size()}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(println (str "commits=" (count (str/split (str/trim (read-line)) #"\s+"))))
```

**Qué reconocer:** Scala devuelve un `Array` de Java y por eso usa `.length`, mientras Kotlin y
Groovy exponen colecciones con `.size`; Clojure cambia de forma por completo y usa `count`, que
funciona sobre **cualquier** secuencia. En Git, lo que llega al repositorio depende de la
herramienta: **Maven** aporta `pom.xml`, **Gradle** —que sirve a **Kotlin** y **Groovy**— aporta
`build.gradle(.kts)`, `settings.gradle` y, muy importante, el **wrapper** (`gradlew`, `gradlew.bat`
y `gradle-wrapper.properties`), que se versiona precisamente para que todo el equipo construya con
la misma versión de Gradle. **Scala** versiona `build.sbt` y `project/build.properties`; **Clojure**
versiona **`deps.edn`** o el `project.clj` de **Leiningen**. Y todos ignoran lo mismo: `target/`,
`build/`, `out/`, `.gradle/`. Sobre el bloqueo de dependencias, la JVM es la familia menos rigurosa
de esta página — Maven no tiene lockfile y el de Gradle (`gradle.lockfile`) hay que activarlo, así
que el historial de Git suele guardar rangos, no versiones exactas.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let msgs = stdin.ReadLine().Split(' ', System.StringSplitOptions.RemoveEmptyEntries)
printfn "commits=%d" msgs.Length
```

### VB.NET

```vbnet
Imports System

Module Historial
    Sub Main()
        Dim msgs = Console.ReadLine().Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries)
        Console.WriteLine("commits={0}", msgs.Length)
    End Sub
End Module
```

**Qué reconocer:** los dos obtienen un array del CLR y leen `.Length`, la misma propiedad con la
misma mayúscula — que es exactamente lo que significa compartir plataforma. En Git, .NET es el caso
más ordenado: **NuGet** es el único gestor, el `.gitignore` estándar de Microsoft ignora `bin/`,
`obj/` y la carpeta `packages/`, y **`packages.lock.json`** se versiona cuando se ha activado
`RestorePackagesWithLockFile`. Hay dos peculiaridades históricas que conviene reconocer al abrir un
repositorio .NET antiguo: los archivos `.sln` y `.csproj`/`.fsproj`/`.vbproj` **son texto**, pero el
`.sln` tiene un formato con GUID que produce conflictos de fusión horribles cuando dos ramas añaden
proyectos a la vez; y en Windows el final de línea CRLF obliga a cuidar `.gitattributes` en cuanto
alguien del equipo trabaja en Linux.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Memoria explícita, tipos declarados y compilación
separada.

### C++

```cpp
#include <iostream>
#include <string>

int main() {
    std::string msg;
    int n = 0;
    while (std::cin >> msg) {
        ++n;
    }
    std::cout << "commits=" << n << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        char buf[512];
        fgets(buf, sizeof buf, stdin);
        NSCharacterSet *espacios = [NSCharacterSet whitespaceAndNewlineCharacterSet];
        NSArray<NSString *> *msgs = [[[NSString stringWithUTF8String:buf]
            stringByTrimmingCharactersInSet:espacios]
            componentsSeparatedByCharactersInSet:espacios];
        printf("commits=%lu\n", (unsigned long)msgs.count);
    }
    return 0;
}
```

**Qué reconocer:** C++ ni siquiera necesita partir la línea — el operador `>>` sobre `std::string`
ya salta espacios, así que contar es un bucle de lectura; Objective-C conserva `fgets` de C y añade
la capa de objetos para separar y contar. En Git, aquí está el caso más doloroso y más honesto de
la página: **C++ no tiene gestor de paquetes oficial**, así que el historial acaba cargando con la
decisión. **Conan** y **vcpkg** compiten —y cada uno versiona lo suyo: `conanfile.txt`/`conanfile.py`
y `conan.lock`, o `vcpkg.json` y `vcpkg-configuration.json`—, pero mucha gente sigue metiendo las
dependencias **dentro del repositorio**, como submódulos de Git o como carpetas `third_party/`
copiadas enteras. Por eso los repositorios C++ grandes son de los pocos donde `git submodule` es una
habilidad cotidiana en vez de una curiosidad. Objective-C tuvo más suerte: **CocoaPods** trajo
`Podfile` y **`Podfile.lock`** —ambos se versionan— y la carpeta `Pods/` es el debate perpetuo de esa
comunidad, con partidarios de commitearla para poder construir sin red.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin máquina
virtual, y con gestores de paquetes diseñados junto al lenguaje.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [512]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, linea, " \r"), ' ');
    var n: usize = 0;
    while (it.next()) |_| n += 1;
    try std.io.getStdOut().writer().print("commits={d}\n", .{n});
}
```

### Nim

```nim
import std/strutils

echo "commits=", stdin.readLine().splitWhitespace().len
```

### D

```d
import std.stdio, std.array, std.algorithm;

void main() {
    writefln("commits=%d", readln().split().length);
}
```

**Qué reconocer:** Zig no construye ninguna lista intermedia —recorre el iterador y descarta el
valor con `|_|`, así que nunca reserva memoria para contar—, mientras Nim y D crean el `seq` o el
array y preguntan por su longitud. Esa diferencia entre *contar* y *materializar* es la marca de la
familia. En Git, los tres versionan su manifiesto e ignoran los artefactos: **Zig** commitea
`build.zig` y **`build.zig.zon`** —que con sus hashes de contenido hace de lockfile— e ignora
`zig-out/` y `.zig-cache/`; **Nim** versiona el `.nimble` (y el `nimble.lock` si lo usa) e ignora
`nimcache/`, la carpeta donde deja el C intermedio que genera; **D** versiona `dub.json` y
**`dub.selections.json`** e ignora `.dub/`. Fíjate en que el archivo de resolución exacta sí entra
al historial en los tres: es la lección que estas comunidades jóvenes aprendieron de Bundler y de
Cargo sin tener que repetir el error.

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
    split_string(Linea, " ", " ", Partes),
    exclude(==(""), Partes, Mensajes),
    length(Mensajes, N),
    format("commits=~d~n", [N]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S: el historial se declara como hechos.
commit(1, "fix").
commit(2, "add").
commit(3, "refactor").

% Contar exige un dialecto con agregados, como Soufflé:
total(N) :- N = count : { commit(_, _) }.
```

**Qué reconocer:** `length/2` en Prolog es una **relación**, no una función: el mismo predicado
sirve para medir una lista y para generar una lista de longitud dada, según qué argumento venga sin
ligar. Datalog obliga a declarar el historial como hechos numerados, y esa forma resulta
sorprendentemente cercana a lo que Git guarda de verdad: un commit no es un texto, es un **objeto
identificado por su hash** que apunta a su padre, y el "historial" es el grafo dirigido acíclico que
forman esas relaciones. Consultar quién es ancestro de quién —lo que hace `git merge-base`— es
literalmente un **cierre transitivo**, la operación en la que Datalog es especialista. Es el mejor
argumento de esta página para que la familia declarativa no parezca una curiosidad académica: la
herramienta que usas todos los días guarda sus datos como ella los pediría.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo esqueleto en todos: partir por espacios y contar. Lo
que cambia es la **forma** —y qué arrastra cada ecosistema hasta el historial: el manifiesto y el
lockfile sí, la carpeta de dependencias y los artefactos generados no. Esa frontera es la misma en
los veinte, y es lo transferible.

⏮️ [Volver a la clase 145](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
