# 🧬 El mismo programa en las familias de lenguajes — Clase 148

> [⬅️ Volver a la clase 148](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —etiquetar la versión que se despliega— resuelto por
los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez lenguajes
del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): una versión `mayor.menor.parche`
- **Salida** (stdout): `desplegado=v<versión>`
- **Regla:** prefijar la versión con `v`

| stdin | esperado |
|---|---|
| `1.2.3` | `desplegado=v1.2.3` |
| `0.9.0` | `desplegado=v0.9.0` |
| `2.1.5` | `desplegado=v2.1.5` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Lo que se despliega es el **código fuente tal cual**: no hay artefacto intermedio, y por eso la
máquina de destino necesita el intérprete instalado.

### Ruby

```ruby
version = STDIN.gets.strip
puts "desplegado=v#{version}"
```

### Perl

```perl
use strict;
use warnings;

chomp(my $version = <STDIN>);
print "desplegado=v$version\n";
```

### Lua

```lua
local version = io.read("l"):gsub("%s+$", "")
print("desplegado=v" .. version)
```

### Tcl

```tcl
gets stdin version
puts "desplegado=v[string trim $version]"
```

### R

```r
version <- trimws(readLines("stdin", n = 1))
cat(sprintf("desplegado=v%s\n", version))
```

**Qué reconocer:** los cinco son una interpolación de cadena y poco más —`#{}`, `$version`, `..`,
`[]`, `sprintf`—, la misma operación que hace el f-string de Python. La consecuencia para el
despliegue es lo que los une de verdad: **entregas archivos, no un programa**. El servidor de destino
tiene que traer Ruby, Perl, Lua, R o Tcl de la versión adecuada, y si no coincide con la de
desarrollo el fallo aparece en producción, no en el build. De ahí que estas comunidades vivan de
gestores de versión (rbenv, rvm, renv) y de contenedores: la imagen es la forma práctica de
**empaquetar el intérprete junto al código** y recuperar la propiedad de que lo que se prueba es lo
que se despliega.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final version = stdin.readLineSync()!.trim();
  print('desplegado=v$version');
}
```

### ActionScript 3

```actionscript
// ActionScript no tiene stdin: el artefacto era un .swf y el "despliegue" consistía
// en subirlo a un servidor web. Se ilustra solo la regla de etiquetado.
package {
    public class Despliegue {
        public static function etiqueta(version:String):String {
            return "desplegado=v" + version;
        }
    }
}
```

**Qué reconocer:** la interpolación `$version` de Dart es la misma plantilla de JavaScript con otro
delimitador. Lo interesante es que Dart **elige su artefacto según el destino**: `dart compile exe`
produce un binario nativo, `dart compile js` produce JavaScript para el navegador y Flutter produce
un paquete móvil, todo desde el mismo fuente. TypeScript hace algo parecido a menor escala: nunca se
despliega `.ts`, se despliega el `.js` transpilado. ActionScript ilustra el final del camino
contrario: su artefacto `.swf` dependía de un reproductor propietario, y cuando el reproductor
desapareció el código dejó de ser desplegable aunque siguiera siendo correcto.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). El artefacto es un `.jar` **portable**: el
mismo archivo corre en Linux, macOS y Windows, a cambio de exigir una JVM instalada en destino.

### Kotlin

```kotlin
fun main() {
    val version = readLine()!!.trim()
    println("desplegado=v$version")
}
```

### Scala

```scala
object Despliegue extends App {
  val version = scala.io.StdIn.readLine().trim
  println(s"desplegado=v$version")
}
```

### Groovy

```groovy
def version = System.in.newReader().readLine().trim()
println "desplegado=v$version"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(println (str "desplegado=v" (str/trim (read-line))))
```

**Qué reconocer:** los cuatro interpolan sobre el mismo `String` de Java —Clojure es el único que
renuncia a la plantilla y concatena con `str`, porque en un lenguaje de listas la función es más
natural que la sintaxis—. Para la entrega, la familia comparte una propiedad muy fuerte: se compila
**una vez** y el `.jar` resultante vale para todas las plataformas, así que la matriz de compilación
desaparece. El precio se paga en destino: hay que instalar una JVM compatible, y una versión mayor
equivocada hace fallar el arranque con un error de bytecode. Herramientas como `jlink` o los
*fat jars* existen precisamente para empaquetar el runtime dentro del artefacto y quitarse esa
dependencia de encima.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let version = stdin.ReadLine().Trim()
printfn "desplegado=v%s" version
```

### VB.NET

```vbnet
Imports System

Module Despliegue
    Sub Main()
        Dim version = Console.ReadLine().Trim()
        Console.WriteLine("desplegado=v" & version)
    End Sub
End Module
```

**Qué reconocer:** los tres compilan a la misma IL dentro de un `.dll`, que es el equivalente exacto
del `.jar`: **artefacto portable que exige la máquina virtual instalada**. Donde .NET se separa de la
JVM es en que ofrece las dos opciones de forma explícita: `dotnet publish` en modo *framework
dependent* entrega el `.dll` pequeño y confía en el runtime de destino, mientras que en modo
*self-contained* entrega un ejecutable por plataforma con el runtime dentro —y ahí reaparece la
matriz de compilación que la JVM había evitado—. Elegir entre un artefacto de 200 KB con
dependencia externa y otro de 70 MB autosuficiente es la decisión de entrega más concreta de esta
familia.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Lo que se entrega es un **binario por plataforma**,
sin runtime que instalar pero con una matriz de compilación que crece sola.

### C++

```cpp
#include <iostream>
#include <string>

int main() {
    std::string version;
    std::getline(std::cin, version);
    std::cout << "desplegado=v" << version << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        char buf[128];
        if (fgets(buf, sizeof buf, stdin)) {
            NSString *linea = [NSString stringWithUTF8String:buf];
            NSCharacterSet *espacios = [NSCharacterSet whitespaceAndNewlineCharacterSet];
            NSString *version = [linea stringByTrimmingCharactersInSet:espacios];
            printf("desplegado=v%s\n", version.UTF8String);
        }
    }
    return 0;
}
```

**Qué reconocer:** ambos son superconjuntos de C, y el `getline` de C++ o el `fgets` de Objective-C
son el mismo gesto que la versión en C de la clase. Para la entrega, la familia paga el precio
completo del compilado AOT: un binario por sistema operativo **y** por arquitectura, más la
dependencia de bibliotecas compartidas que tienen que existir en destino con la versión correcta
—el clásico fallo de `libstdc++` o de glibc demasiado antigua—. Objective-C lo agrava al depender de
Foundation, lo que en la práctica limita su despliegue al ecosistema de Apple. Aquí no hay runtime
que instalar, pero sí un sistema operativo que tiene que parecerse mucho al del build.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados a binario
estático: se copia un archivo al servidor y funciona, sin instalar nada alrededor.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [128]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const version = std.mem.trim(u8, linea, " \r\n");
    try std.io.getStdOut().writer().print("desplegado=v{s}\n", .{version});
}
```

### Nim

```nim
import std/strutils

let version = stdin.readLine().strip()
echo "desplegado=v" & version
```

### D

```d
import std.stdio, std.string;

void main() {
    auto version = readln().strip();
    writeln("desplegado=v", version);
}
```

**Qué reconocer:** los tres producen un ejecutable autosuficiente, igual que Go y Rust, y por eso el
despliegue se reduce a `scp` más un servicio que lo arranque: la imagen de contenedor puede partir de
`scratch` porque no hay intérprete ni runtime que copiar. **Zig destaca por su compilación cruzada
trivial**: un solo comando —`zig build-exe -target aarch64-linux`, `-target x86_64-windows`— genera
el binario de cualquier plataforma desde la máquina que sea, porque el compilador incluye las
bibliotecas de C de todos los objetivos. Eso colapsa la matriz de entrega de la familia AOT a un
único job de build, que es exactamente el problema que C++ no sabe resolver sin toolchains cruzados
montados a mano. Nim y D compilan pasando por C, lo que les da portabilidad de fuente pero les
devuelve la dependencia de un compilador de C en cada plataforma de destino.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). No hay binario que desplegar: lo que se entrega
es un **script que se aplica** sobre un motor que ya está corriendo.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    normalize_space(string(Version), Linea),
    format("desplegado=v~w~n", [Version]).
```

### Datalog

```datalog
% Datalog no tiene E/S ni concatenación de cadenas: la versión se declara como hecho
% y la etiqueta se modela como una relación entre versión y despliegue.
version("1.2.3").

desplegado(V, "v") :- version(V).
```

**Qué reconocer:** Prolog sí tiene entrada/salida y resuelve el contrato con `format`, pero fíjate en
que su unidad de despliegue no es un ejecutable sino una **base de conocimiento** que se carga en el
intérprete, igual que un `.sql` se aplica sobre una base de datos. Esa es la propiedad que comparte
toda la familia: el artefacto es declarativo y el motor ya vive en destino, así que la pregunta de
entrega deja de ser "¿qué binario copio?" y pasa a ser "¿cómo versiono y aplico este cambio sin
romper lo que ya está cargado?" —que es literalmente el problema de las migraciones de esquema—.
Datalog lo lleva al extremo: sin efectos ni cadenas, solo puede declarar la relación, no imprimirla.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo esqueleto en todos: leer la versión y prefijarla. Lo
que cambia es **qué se entrega**: fuente más intérprete en destino, un artefacto portable que exige
máquina virtual, o un binario por plataforma. Eso es lo transferible.

⏮️ [Volver a la clase 148](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
