# 🧬 El mismo programa en las familias de lenguajes — Clase 144

> [⬅️ Volver a la clase 144](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —calcular una suma de comprobación— resuelto por los
**primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez lenguajes del
núcleo.

El problema no podría estar mejor elegido para el tema: una compilación es **reproducible** cuando
dos personas distintas, en máquinas distintas, obtienen artefactos con el **mismo hash**. Así que
mientras el código suma enteros, el texto va contando cómo empaqueta cada familia y con qué gestor
consigue —o no— que ese hash coincida.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): enteros separados por espacio
- **Salida** (stdout): `checksum=<suma de los valores>`
- **Regla:** `checksum = suma de todos los valores`

| stdin | esperado |
|---|---|
| `1 2 3` | `checksum=6` |
| `5` | `checksum=5` |
| `10 20 30` | `checksum=60` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Tipado dinámico y poca ceremonia: partir la línea y acumular cabe en una o dos expresiones.

### Ruby

```ruby
puts "checksum=#{STDIN.read.split.map(&:to_i).sum}"
```

### Perl

```perl
use List::Util qw(sum0);

my @n = split ' ', <STDIN>;
printf "checksum=%d\n", sum0(@n);
```

### Lua

```lua
local suma = 0
for token in io.read("l"):gmatch("%S+") do
    suma = suma + tonumber(token)
end
print(string.format("checksum=%d", suma))
```

### Tcl

```tcl
gets stdin linea
set suma 0
foreach n $linea { incr suma $n }
puts "checksum=$suma"
```

### R

```r
v <- scan("stdin", what = integer(), quiet = TRUE)
cat(sprintf("checksum=%d\n", sum(v)))
```

**Qué reconocer:** los cinco parten de texto y acaban en un entero, pero solo tres tienen la suma en
la biblioteca estándar (`sum` de Ruby, `sum0` del módulo `List::Util` de Perl, `sum` vectorizado de
R); Lua y Tcl la escriben a mano porque su estándar es deliberadamente diminuto. Tcl vuelve a
enseñar su naturaleza: la línea leída **ya es una lista** sin necesidad de partirla, porque en Tcl
las listas y las cadenas son la misma cosa. En empaquetado, la familia comparte un problema y lo
resuelve de formas muy distintas. **Ruby** empaqueta con `gem build` a partir de un `.gemspec`, y
Bundler garantiza que quien instale reciba lo mismo que dice **`Gemfile.lock`** —uno de los primeros
lockfiles de la industria, y la razón de que "instalación reproducible" dejara de ser una aspiración
en este ecosistema—. **Perl** construye distribuciones con `Makefile.PL`/`Build.PL` y las sube a
**CPAN**; el congelado vive en **`cpanfile.snapshot`**. **Lua** empaqueta con **LuaRocks** a partir
de un `.rockspec`, que declara dependencias pero no fija el árbol completo. **R** usa `R CMD build`
sobre **CRAN**, cuyo talón de Aquiles es que solo sirve la última versión de cada paquete: sin
**renv** y su `renv.lock`, un análisis de hace tres años no se reconstruye. **Tcl** distribuye con
**teacup** y tiene el truco más peculiar de todos: el **starkit/starpack**, un ejecutable único que
lleva dentro el intérprete y todo el código.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final suma = stdin
      .readLineSync()!
      .trim()
      .split(RegExp(r'\s+'))
      .map(int.parse)
      .fold<int>(0, (a, b) => a + b);
  print('checksum=$suma');
}
```

### ActionScript 3

```actionscript
// Sin stdin en el reproductor Flash: se ilustra la suma sobre un vector ya cargado.
package {
    public class Checksum {
        public static function calcular(valores:Vector.<int>):String {
            var suma:int = 0;
            for each (var n:int in valores) {
                suma += n;
            }
            return "checksum=" + suma;
        }
    }
}
```

**Qué reconocer:** el `fold` de Dart es el `reduce` de JavaScript con el tipo del acumulador escrito
de forma explícita (`fold<int>`), y ese `<int>` es justo lo que TypeScript añadiría por encima de
JS. En empaquetado, Dart hace algo que su familia de origen nunca hizo: **compila a binario nativo**
con `dart compile exe`, además de a JavaScript o a la máquina virtual — un mismo `pubspec.yaml`, con
su **`pubspec.lock`** al lado, produce tres artefactos distintos. ActionScript compilaba a `.swf`
para el reproductor Flash, y su falta de gestor de paquetes es hoy irrelevante por una razón más
brutal: sin el runtime, el artefacto no se ejecuta en ningún sitio. Es el recordatorio de que
reproducir la **compilación** no sirve de nada si no se puede reproducir el **entorno de ejecución**.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos compilan al mismo bytecode; el artefacto
final es un `.jar` y el debate es siempre el mismo: qué se mete dentro y qué se deja fuera.

### Kotlin

```kotlin
fun main() {
    val suma = readLine()!!.trim().split(Regex("\\s+")).sumOf { it.toInt() }
    println("checksum=$suma")
}
```

### Scala

```scala
object Checksum extends App {
  val suma = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt).sum
  println(s"checksum=$suma")
}
```

### Groovy

```groovy
def suma = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger().sum()
println "checksum=$suma"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [suma (->> (str/split (str/trim (read-line)) #"\s+")
                (map parse-long)
                (reduce + 0))]
  (println (str "checksum=" suma)))
```

**Qué reconocer:** los cuatro llaman por debajo al mismo `String.split` de Java, que interpreta
`\s+` como expresión regular; lo que cambia es cómo se escribe el patrón (`Regex("\\s+")` en Kotlin,
la barra `/.../` de Groovy, el literal `#"\s+"` de Clojure) y cómo se suma —`sumOf`, `.sum`,
`reduce +`—. En empaquetado, la plataforma es una y las herramientas son cuatro: **Maven** y
**Gradle** dan servicio a **Kotlin** y **Groovy**, **Scala** usa **sbt**, y **Clojure** construye
desde **`deps.edn`** (con `tools.build`) o desde **Leiningen**. El artefacto también se bifurca: un
`.jar` normal necesita el classpath completo, así que casi todos acaban generando un **uber-jar**
—`shadowJar` en Gradle, `maven-shade-plugin`, `lein uberjar`, `sbt-assembly`— con las dependencias
dentro. Y sobre reproducibilidad hay un detalle concreto que merece nombre propio: un `.jar` es un
ZIP, y un ZIP guarda **marcas de tiempo**, así que dos compilaciones del mismo código dan hashes
distintos salvo que se desactiven explícitamente
(`preserveFileTimestamps = false` en Gradle, `project.build.outputTimestamp` en Maven).

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let suma =
    stdin.ReadLine().Split(' ', System.StringSplitOptions.RemoveEmptyEntries)
    |> Array.sumBy int
printfn "checksum=%d" suma
```

### VB.NET

```vbnet
Imports System
Imports System.Linq

Module Checksum
    Sub Main()
        Dim v = Console.ReadLine().Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries)
        Console.WriteLine("checksum={0}", v.Sum(Function(s) Integer.Parse(s)))
    End Sub
End Module
```

**Qué reconocer:** `RemoveEmptyEntries` aparece en los dos porque el `Split` del CLR, al partir por
carácter literal, deja cadenas vacías si hay espacios repetidos — es la misma llamada, escrita con
la sintaxis de cada lenguaje. En empaquetado comparten todo: **NuGet** como gestor, el mismo
`<PackageReference>` en `.fsproj` y `.vbproj`, y **`packages.lock.json`** cuando se activa
`RestorePackagesWithLockFile`. Y .NET es de los pocos ecosistemas que puso la reproducibilidad en el
compilador: `<Deterministic>` está **activado por defecto**, de modo que el mismo código y las
mismas referencias producen ensamblados byte a byte idénticos —siempre que se normalicen las rutas
de origen con `<DeterministicSourcePaths>`, que es la trampa que queda—. El empaquetado final es
`dotnet pack` (un `.nupkg`) o `dotnet publish`, con opciones de archivo único y recorte del runtime.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Memoria explícita, tipos declarados y el binario
como producto final.

### C++

```cpp
#include <iostream>
#include <iterator>
#include <numeric>
#include <vector>

int main() {
    const std::vector<long> v{std::istream_iterator<long>(std::cin),
                              std::istream_iterator<long>()};
    std::cout << "checksum=" << std::accumulate(v.begin(), v.end(), 0L) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        char buf[256];
        fgets(buf, sizeof buf, stdin);
        NSString *linea = [[NSString stringWithUTF8String:buf]
            stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]];
        NSInteger suma = 0;
        for (NSString *p in [linea componentsSeparatedByString:@" "]) {
            suma += [p integerValue];
        }
        printf("checksum=%ld\n", (long)suma);
    }
    return 0;
}
```

**Qué reconocer:** C++ resuelve la lectura y la suma con dos piezas de su biblioteca de algoritmos
—`istream_iterator` convierte el flujo en un rango, `accumulate` lo pliega— mientras Objective-C
mantiene el `fgets` de C y recorre objetos con `for in`. Y aquí está el caso más doloroso y más
honesto del empaquetado: **C++ no tiene gestor de paquetes oficial**. **Conan** y **vcpkg** llevan
años compitiendo sin que ninguno se imponga, y buena parte del mundo real sigue con submódulos de
Git, `FetchContent` de CMake o `third_party/` copiado a mano. La reproducibilidad, además, es
estructuralmente más difícil que en cualquier otra familia: el binario depende del compilador
exacto, de su versión, de las banderas de optimización, de las cabeceras del sistema y hasta de las
macros `__FILE__` y `__DATE__` que incrustan rutas y fechas en el ejecutable. Por eso el mundo C/C++
inventó `-ffile-prefix-map` y `SOURCE_DATE_EPOCH`, y por eso las distribuciones de Linux —que
compilan miles de paquetes C— fueron quienes empujaron el movimiento *Reproducible Builds*.
Objective-C, en cambio, hereda de **CocoaPods** su `Podfile` y su **`Podfile.lock`**, y del mundo
Apple un empaquetado muy cerrado: `.framework`, `.app` y firma de código.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin máquina
virtual, y con la compilación cruzada como característica de primera clase.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [256]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, linea, " \r"), ' ');
    var suma: i64 = 0;
    while (it.next()) |tok| suma += try std.fmt.parseInt(i64, tok, 10);
    try std.io.getStdOut().writer().print("checksum={d}\n", .{suma});
}
```

### Nim

```nim
import std/[strutils, sequtils, math]

echo "checksum=", stdin.readLine().splitWhitespace().map(parseInt).sum()
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm;

void main() {
    writefln("checksum=%d", readln().split().map!(to!long).sum());
}
```

**Qué reconocer:** Zig obliga a declarar el tipo del acumulador (`i64`) y a tratar cada posible
fallo con `try`, mientras Nim y D encadenan `split → map → sum` con la misma soltura que un lenguaje
de scripting, sin dejar de producir un binario nativo. En empaquetado, los tres son jóvenes y por
eso llegaron con las lecciones aprendidas. **Zig** es el más radical: su gestor declara cada
dependencia en **`build.zig.zon`** con **URL y hash del contenido**, así que el manifiesto *es* el
lockfile; y `zig build` compila para cualquier objetivo desde cualquier máquina, lo que convierte la
compilación cruzada reproducible en el caso normal en vez de la excepción. **Nim** empaqueta con
**Nimble** (`.nimble`, más un `nimble.lock` opcional), con la peculiaridad de que primero genera C y
luego lo compila —lo que le traslada la dependencia del compilador de C que arrastra esa familia—.
**D** usa **DUB**, que separa limpiamente lo declarado (`dub.json`) de lo resuelto
(**`dub.selections.json`**), exactamente como `Cargo.toml` y `Cargo.lock`.

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
    exclude(==(""), Partes, NoVacias),
    maplist([S, N]>>number_string(N, S), NoVacias, Numeros),
    sum_list(Numeros, Suma),
    format("checksum=~d~n", [Suma]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S ni agregación: solo puede declarar los valores.
valor(1, 1).
valor(2, 2).
valor(3, 3).

% Sumarlos exige un dialecto con agregados, como Soufflé:
checksum(S) :- S = sum V : { valor(_, V) }.
```

**Qué reconocer:** Prolog sí puede sumar —`sum_list/2` está en la biblioteca— pero fíjate en que
cada índice tiene que existir como término antes de plegar: no hay una variable acumuladora que se
reasigne, sino una lista que se unifica con un resultado. Datalog es más restrictivo todavía: la
agregación **no forma parte del lenguaje**, y por eso el bloque tiene que declarar explícitamente
que la última regla ya es sintaxis de Soufflé y no Datalog puro. Esa renuncia es la misma que hace
SQL cuando no te deja decir cómo recorrer las filas, y explica por qué esta familia es la más
reproducible de todas por construcción: sin efectos, sin estado y sin orden de ejecución observable,
el mismo conjunto de hechos da siempre el mismo resultado, en cualquier máquina y en cualquier año.
Ese es, literalmente, el objetivo que las otras seis familias persiguen a base de lockfiles y
banderas de compilador.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo esqueleto en todos: leer, convertir, acumular. Lo que
cambia es la **forma** —y lo que cuesta conseguir que dos compilaciones del mismo código produzcan
exactamente el mismo artefacto: desde el `<Deterministic>` que .NET trae activado hasta las marcas
de tiempo del `.jar`, el hash de contenido de Zig o el vacío que C++ todavía no ha llenado. Eso es
lo transferible.

⏮️ [Volver a la clase 144](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
