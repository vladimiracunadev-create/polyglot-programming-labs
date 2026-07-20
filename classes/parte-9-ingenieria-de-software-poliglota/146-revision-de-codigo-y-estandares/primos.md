# 🧬 El mismo programa en las familias de lenguajes — Clase 146

> [⬅️ Volver a la clase 146](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —comprobar si un identificador cumple el estándar de
estar todo en minúsculas— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

El programa valida una regla de estilo, así que la comparación interesante no está en el código sino
en **quién decide el estilo** de cada lenguaje. Hay tres respuestas posibles y las tres aparecen aquí:
una herramienta oficial que no se puede configurar (`zig fmt`, `dart format`), una herramienta
configurable donde cada equipo discute sus reglas (`rubocop`, `clang-format`), o ninguna herramienta y
solo una guía escrita. Cada bloque lleva en un comentario el linter o el formateador real de esa
comunidad.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): una palabra, un identificador de solo letras
- **Salida** (stdout): `valido=<true|false>`
- **Regla:** `true` si todos los caracteres están en minúsculas

| stdin | esperado |
|---|---|
| `total` | `valido=true` |
| `Total` | `valido=false` |
| `abc` | `valido=true` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Sin compilador que rechace nada, esta familia depende por completo de herramientas externas para
sostener un estándar: si el linter no lo caza, nadie lo caza.

### Ruby

```ruby
# `rubocop` es el estándar de facto: reúne linter y formateador en un binario y
# su configuración vive en `.rubocop.yml`, discutible regla a regla. Trae
# además `--auto-gen-config`, que congela las infracciones existentes para que
# un proyecto viejo pueda adoptarlo sin arreglarlo todo el primer día.
palabra = STDIN.gets.strip
puts "valido=#{palabra == palabra.downcase}"
```

### Perl

```perl
use strict;
use warnings;

# `perlcritic` aplica las reglas del libro *Perl Best Practices* graduadas por
# SEVERIDAD, de 5 (crítico) a 1 (quisquilloso): el equipo elige hasta qué nivel
# quiere que le griten. `perltidy` es el formateador, y es una herramienta
# distinta: en Perl, analizar y formatear no van juntos.
chomp(my $palabra = <STDIN>);
printf "valido=%s\n", ($palabra eq lc $palabra) ? 'true' : 'false';
```

### Lua

```lua
-- `luacheck` es el analizador de la comunidad, y su regla más valiosa es la
-- que avisa de globales accidentales: en Lua, olvidar un `local` no es un
-- error, es una variable global silenciosa. No hay formateador oficial.
local palabra = io.read("l")
print("valido=" .. tostring(palabra == palabra:lower()))
```

### Tcl

```tcl
# El analizador estático de Tcl es `nagelfar`, externo al núcleo. La
# distribución incluye una guía de estilo escrita, pero ninguna herramienta
# oficial la impone: el estándar es un documento, no un binario.
set palabra [string trim [gets stdin]]
if {$palabra eq [string tolower $palabra]} {
    puts "valido=true"
} else {
    puts "valido=false"
}
```

### R

```r
# `lintr` comprueba y `styler` reformatea — dos paquetes de CRAN, no del core.
# El estilo de referencia no es del lenguaje sino de una comunidad dentro de
# él: la guía del tidyverse, que ni siquiera todos los usuarios de R siguen.
palabra <- trimws(readLines("stdin", n = 1))
cat(sprintf("valido=%s\n", if (palabra == tolower(palabra)) "true" else "false"))
```

**Qué reconocer:** aquí el estándar siempre llega **después** del lenguaje y desde fuera, y eso deja
dos huellas visibles. La primera es que analizar y formatear suelen ser herramientas separadas
—`perlcritic` y `perltidy`, `lintr` y `styler`—, mientras que los lenguajes que se ocuparon del tema
desde el diseño lo unifican. La segunda es que la regla más valiosa de cada linter revela el punto
débil de su lenguaje: `luacheck` existe sobre todo para cazar globales accidentales, porque en Lua
olvidar `local` no da ningún error. Y `rubocop` aporta la lección práctica más transferible de la
familia — `--auto-gen-config`, que permite adoptar un estándar en un proyecto existente sin tener que
arreglar diez mil avisos antes de empezar.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
Es la familia donde más se ha discutido el formato, y de donde salió la idea que hoy domina: dejar
de discutirlo y aceptar lo que decida la herramienta.

### Dart

```dart
import 'dart:io';

// `dart format` viene en el SDK y NO tiene opciones de estilo: solo el ancho de
// línea. Es la misma decisión de `gofmt`. `dart analyze` sí es configurable,
// con las reglas de `analysis_options.yaml`, porque ahí no se discute estética
// sino corrección.
void main() {
  final palabra = stdin.readLineSync()!.trim();
  print('valido=${palabra == palabra.toLowerCase()}');
}
```

### ActionScript 3

```actionscript
// ActionScript nunca tuvo formateador oficial: el estándar de facto fueron las
// convenciones de Adobe y lo que hiciera el IDE al guardar. El lenguaje no
// tiene stdin, así que la validación se muestra aislada en un método.
package {
    public class Estandar {
        public static function esValido(palabra:String):String {
            return "valido=" + (palabra == palabra.toLowerCase()).toString();
        }
    }
}
```

**Qué reconocer:** la separación que hace Dart es la más útil de toda esta página y conviene
quedársela: **el formato no se configura, el análisis sí**. Un formateador sin opciones elimina de la
revisión de código toda una categoría de comentarios que nunca aportaron nada; un analizador
configurable, en cambio, tiene que serlo, porque lo que en un proyecto es un error grave en otro es
una decisión deliberada. ActionScript ilustra el mundo anterior a esa idea, cuando el estilo lo fijaba
el IDE de cada quien y las revisiones se llenaban de discusiones sobre llaves — exactamente el
problema que `gofmt` vino a matar.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Con décadas de código heredado, esta familia
inventó los conjuntos de reglas configurables y las herramientas que además **reescriben** el código.

### Kotlin

```kotlin
// `ktlint` aplica la guía oficial de estilo de Kotlin y además REESCRIBE con
// `-F`: comprobar y arreglar son el mismo binario. `detekt` cubre lo que
// ktlint no toca —complejidad ciclomática, funciones demasiado largas, olores
// de diseño—, que es análisis, no formato.
fun main() {
    val palabra = readLine()!!.trim()
    println("valido=${palabra == palabra.lowercase()}")
}
```

### Scala

```scala
object Estandar extends App {
  // `scalafmt` fija su PROPIA VERSIÓN dentro de `.scalafmt.conf`: el fichero
  // dice qué scalafmt debe usarse, así que el mismo repositorio produce el
  // mismo formato en cualquier máquina y en CI. `scalafix` hace aparte las
  // reescrituras semánticas, como migrar una API deprecada.
  val palabra = scala.io.StdIn.readLine().trim
  println(s"valido=${palabra == palabra.toLowerCase}")
}
```

### Groovy

```groovy
// `codenarc` es el analizador de Groovy, con las reglas agrupadas en conjuntos
// temáticos ("basic", "unused", "design", "security") que se activan por
// bloques en vez de una a una.
def palabra = System.in.newReader().readLine().trim()
println "valido=${palabra == palabra.toLowerCase()}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; `clj-kondo` analiza el código LEYÉNDOLO, sin evaluarlo — importante en un
;; lenguaje donde cargar un espacio de nombres ejecuta su contenido. `cljfmt`
;; formatea. La guía de estilo de la comunidad es un documento en GitHub.
(let [palabra (str/trim (read-line))]
  (println (str "valido=" (= palabra (str/lower-case palabra)))))
```

**Qué reconocer:** dos ideas que esta familia aporta y que conviene robar. La primera es la de
`ktlint`: comprobar y arreglar deben ser el mismo binario, porque un aviso que la máquina sabe
corregir no merece el tiempo de un revisor humano. La segunda es la de `scalafmt`, más sutil y muy
subestimada: el fichero de configuración **fija la versión de la herramienta**, de modo que un
formateador actualizado no puede reescribir medio repositorio y llenar de ruido el siguiente diff. Y
`clj-kondo` resuelve un problema propio de los lenguajes homoicónicos: como cargar código en Clojure
lo ejecuta, un analizador que evaluara para analizar sería peligroso, así que se limita a leer las
formas.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). Aquí el análisis se metió **dentro del
compilador**: las reglas de estilo no son un paso aparte de CI, son avisos de compilación.

### F\#

```fsharp
// `fantomas` es el formateador de F# y `FSharpLint` el analizador. Pero el
// mecanismo común de .NET es `.editorconfig`, que el propio compilador lee:
// una regla de estilo se convierte en un aviso o un error del build.
let palabra = stdin.ReadLine().Trim()
printfn "valido=%b" (palabra = palabra.ToLowerInvariant())
```

### VB.NET

```vbnet
Module Estandar
    Sub Main()
        ' Los analizadores de Roslyn se distribuyen como paquetes NuGet y corren
        ' DENTRO del compilador. Cualquiera puede escribir el suyo con la misma
        ' API que usa el compilador, y una regla violada puede configurarse como
        ' error de compilación, no como un informe que nadie lee.
        Dim palabra = Console.ReadLine().Trim()
        Console.WriteLine($"valido={If(palabra = palabra.ToLowerInvariant(), "true", "false")}")
    End Sub
End Module
```

**Qué reconocer:** la diferencia de .NET con todo lo anterior es **dónde vive el análisis**. En el
resto de la página el linter es un programa que lee tu código desde fuera y lo vuelve a analizar por
su cuenta; en Roslyn, el analizador es un complemento del compilador y trabaja sobre el mismo árbol
sintáctico y la misma información de tipos que la compilación. Las consecuencias son concretas: el
análisis no puede desincronizarse de la versión del lenguaje, un aviso de estilo puede promoverse a
error y romper el build, y el IDE ofrece el arreglo automático porque es el compilador quien lo
propone. Es el mismo movimiento que hicieron Rust con `clippy` y Go con `go vet`: acercar el estándar
a la herramienta que ya entiende el código.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). La familia más antigua es también la única que nunca
acordó un estilo: aquí conviven guías incompatibles y la herramienta las trae todas como presets.

### C++

```cpp
#include <algorithm>
#include <cctype>
#include <iostream>
#include <string>

// `clang-format` se configura con un `.clang-format` de decenas de opciones, y
// las guías históricas —LLVM, Google, Mozilla, WebKit— vienen como PRESETS que
// se pueden heredar y retocar. Que existan varios presets oficiales es el
// reconocimiento de que la familia C nunca acordó un solo estilo.
// `clang-tidy` es el analizador, con su propio catálogo de comprobaciones.
int main() {
    std::string palabra;
    std::cin >> palabra;
    const bool valido = std::none_of(palabra.begin(), palabra.end(),
                                     [](unsigned char c) { return std::isupper(c) != 0; });
    std::cout << "valido=" << (valido ? "true" : "false") << "\n";
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    // El estilo de Objective-C lo fijó Apple con sus convenciones de
    // nomenclatura, deliberadamente largas y explícitas
    // (`stringByAppendingPathComponent:`), sostenidas por documentación y
    // revisión humana, no por una herramienta. `clang-format` también lo formatea.
    char buf[128] = {0};
    scanf("%127s", buf);
    NSString *palabra = @(buf);
    BOOL valido = [palabra isEqualToString:palabra.lowercaseString];
    printf("valido=%s\n", valido ? "true" : "false");
}
```

**Qué reconocer:** que `clang-format` traiga presets con nombre propio —LLVM, Google, Mozilla— es la
prueba documental de que en C y C++ el estándar es **del proyecto**, no del lenguaje. Cambiar de
proyecto significa cambiar de estilo, y por eso el fichero `.clang-format` en la raíz es un artefacto
tan importante: sin él, cada editor formatea a su manera y los diffs se llenan de ruido. Objective-C
enseña el otro tipo de estándar, el que ninguna herramienta puede aplicar: sus nombres larguísimos y
autoexplicativos son una convención **semántica**, y comprobar que un método se llama como debe
llamarse sigue siendo trabajo de un revisor humano. Todo linter tiene ese techo.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Go impuso `gofmt` sin
opciones y Rust `rustfmt` con muy pocas: los dos decidieron que el formato no se discute.

### Zig

```zig
const std = @import("std");

// `zig fmt` NO ES CONFIGURABLE: no admite ninguna opción de estilo, igual que
// `gofmt`. La decisión es deliberada y tiene un argumento explícito — elimina
// del proceso de revisión una categoría entera de comentarios inútiles, a
// cambio de que nadie, ni siquiera con razón, pueda imponer su preferencia.
pub fn main() !void {
    var buf: [128]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const palabra = std.mem.trim(u8, linea, " \t\r");

    var valido = true;
    for (palabra) |c| {
        if (std.ascii.isUpper(c)) valido = false;
    }

    try std.io.getStdOut().writer().print("valido={}\n", .{valido});
}
```

### Nim

```nim
import std/strutils

# El manual de Nim fija el estilo (`camelCase` para procs, `PascalCase` para
# tipos), y el compilador aplica algo único: los identificadores son
# INSENSIBLES a mayúsculas y guiones bajos después de la primera letra, así que
# `dosCosas` y `dos_cosas` son el MISMO identificador. `nph` es el formateador
# de la comunidad, inspirado en la idea de no ofrecer opciones.
let palabra = stdin.readLine().strip()
echo "valido=", palabra == palabra.toLowerAscii()
```

### D

```d
import std.stdio, std.string;

// `dfmt` formatea y `d-scanner` analiza; los dos salieron de la comunidad y no
// de la distribución oficial del compilador, así que su adopción es desigual
// —el problema clásico de un estándar que llega tarde.
void main() {
    immutable palabra = readln().strip();
    writefln("valido=%s", palabra == palabra.toLower());
}
```

**Qué reconocer:** el bloque de Zig es el que hay que leer dos veces. `zig fmt` **no tiene opciones**,
y eso no es una carencia sino la misma tesis de `gofmt` llevada a su conclusión: si el formato no se
puede configurar, no se puede discutir, y una discusión que no existe no consume revisiones de código
ni provoca reformateos masivos entre equipos. El precio también es real y honesto — cuando la
herramienta toma una decisión que no te gusta, no hay recurso. Nim resuelve el mismo problema por una
vía que no tiene paralelo en esta página: en lugar de una herramienta que unifica el estilo de los
nombres, hace que el **lenguaje** trate `dos_cosas` y `dosCosas` como el mismo identificador, así que
la discrepancia deja de existir a nivel semántico. Y D recuerda el escenario más común de todos: buenas
herramientas que llegaron después de que el ecosistema ya tuviera costumbres.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). El caso extremo: SQL tiene tantos dialectos y
tantos estilos —¿palabras clave en mayúsculas o no?— que el linter (`sqlfluff`) empieza preguntando
para qué motor.

### Prolog

```prolog
:- initialization(main, main).

% El "linter" más útil de Prolog viene con el compilador: el aviso de variables
% SINGLETON, las que aparecen una sola vez en una cláusula. Casi siempre son un
% nombre mal tecleado, y como el error no produciría una excepción sino un
% silencioso fallo lógico, ese aviso salva más tiempo que cualquier regla de
% estilo. `library(check)` añade el análisis de predicados no definidos.
main :-
    read_line_to_string(user_input, Palabra),
    string_lower(Palabra, Minuscula),
    (   Palabra == Minuscula
    ->  Valido = true
    ;   Valido = false
    ),
    format("valido=~w~n", [Valido]).
```

### Datalog

```datalog
% El Datalog puro no manipula cadenas ni compara mayúsculas: no hay funciones,
% solo predicados sobre hechos. Así que la validación no se CALCULA, se
% DECLARA — se enumeran los identificadores conocidos y los que cumplen la
% norma, y la regla deriva el resultado. El "estándar de estilo" de un programa
% Datalog es su propio esquema de relaciones.
identificador("total").
minuscula("total").

valido(I) :- identificador(I), minuscula(I).
```

**Qué reconocer:** Prolog aporta el ejemplo más claro de toda la página de que **la mejor regla de un
linter es la que ataca el modo de fallo del lenguaje**. En Prolog, escribir mal el nombre de una
variable no da un error: da una variable nueva, sin ligar, y un predicado que falla en silencio sin
imprimir nada — el fallo más difícil de diagnosticar que hay. Por eso el aviso de singleton, que en
otro lenguaje sería una quisquillosidad de estilo, aquí es la comprobación más valiosa que existe. Y
Datalog cierra recordando el límite: sin funciones ni comparación de cadenas, una regla de estilo no
se puede evaluar, solo declarar como hecho — que es, en el fondo, lo que hace cualquier norma de
equipo antes de que alguien la programe en un linter.

---

## Y de vuelta a la clase

Veinte lenguajes y tres respuestas a la misma pregunta: ¿quién decide el estándar? La herramienta sin
opciones (`zig fmt`, `gofmt`, `dart format`), que gana quitando la discusión de en medio; la
herramienta configurable (`rubocop`, `clang-format`, `scalafmt`), que gana adaptándose a proyectos
que ya existen; o nadie, solo un documento, como en Tcl y Objective-C. La segunda lección es de dónde
vive el análisis: cuanto más cerca del compilador —Roslyn, `clippy`, el aviso de singleton de
Prolog—, más difícil es ignorarlo y menos puede desincronizarse. Y la tercera la dan Objective-C y
Prolog juntos: ninguna herramienta comprueba si un nombre significa lo que dice, y ese es
exactamente el trabajo que queda para la revisión humana.

⏮️ [Volver a la clase 146](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
