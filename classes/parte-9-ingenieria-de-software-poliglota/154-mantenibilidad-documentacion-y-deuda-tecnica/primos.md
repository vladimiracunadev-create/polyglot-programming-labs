# 🧬 El mismo programa en las familias de lenguajes — Clase 154

> [⬅️ Volver a la clase 154](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —contar los módulos de un sistema como métrica simple
de complejidad— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Contar palabras es una excusa: lo que de verdad se compara aquí es **cómo documenta cada familia**, y
por eso cada bloque lleva su documentación escrita en el formato real de su comunidad. Las diferencias
son mayores de lo que parece. Hay lenguajes donde la documentación es un comentario que una
herramienta externa recoge, otros donde es un dato del propio programa que se consulta en ejecución,
y uno —Perl— donde el manual entero del lenguaje vive **dentro de sus ficheros fuente**. Hay incluso
compiladores que compilan y ejecutan los ejemplos de la documentación.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): nombres de módulos separados por espacio
- **Salida** (stdout): `complejidad=<número de módulos>`
- **Regla:** contar los módulos

| stdin | esperado |
|---|---|
| `a b c` | `complejidad=3` |
| `x` | `complejidad=1` |
| `a b c d e` | `complejidad=5` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Python puso la docstring dentro del objeto y PHP la dejó en un comentario que lee phpDocumentor. Esa
misma división —dato del programa o comentario para una herramienta— parte también a los primos.

### Ruby

```ruby
# RDoc viene en la distribución y lee los comentarios que PRECEDEN a cada
# definición, sin marcador especial. Genera el HTML y, sobre todo, alimenta a
# `ri`: la misma documentación se consulta desde la terminal sin navegador.

# Cuenta los módulos que componen un sistema.
modulos = STDIN.gets.split
puts "complejidad=#{modulos.size}"
```

### Perl

```perl
use strict;
use warnings;

=head1 DESCRIPCIÓN

POD (Plain Old Documentation) va DENTRO del propio fuente, intercalado con el
código: el intérprete se salta estos bloques y `perldoc` los extrae. No es una
curiosidad — la documentación de Perl entera, el lenguaje y su biblioteca, está
escrita así, en el código de sus propios módulos. El fuente ES el manual.

=cut

chomp(my $linea = <STDIN>);
my @modulos = split ' ', $linea;
printf "complejidad=%d\n", scalar @modulos;
```

### Lua

```lua
--- Cuenta los módulos que componen un sistema.
-- LuaDoc, y su sucesor LDoc, marcan el bloque documentado con `---` y usan
-- etiquetas `@param` / `@return`. Ninguno viene con Lua: el lenguaje se
-- mantiene minúsculo a propósito y deja fuera hasta esto.
-- @param linea la línea con los nombres de módulo
local linea = io.read("l")
local n = 0
for _ in linea:gmatch("%S+") do
    n = n + 1
end
print("complejidad=" .. n)
```

### Tcl

```tcl
# Tcl documenta con `doctools`, un paquete de Tcllib con formato propio que se
# convierte a manpage, HTML o texto plano. La documentación vive en FICHEROS
# APARTE, no junto al código: es el modelo opuesto al de POD.
set modulos [regexp -all -inline {\S+} [gets stdin]]
puts "complejidad=[llength $modulos]"
```

### R

```r
#' Cuenta los módulos que componen un sistema.
#'
#' El formato oficial de R es el `.Rd`, un dialecto de LaTeX que R exige para
#' cada función exportada de un paquete. roxygen2 lee estos comentarios `#'` y
#' GENERA esos `.Rd`: existe porque nadie quiere escribir el formato oficial a
#' mano, y hoy es lo que usa prácticamente todo CRAN.
#' @param linea nombres de módulo separados por espacio
modulos <- strsplit(trimws(readLines("stdin", n = 1)), "\\s+")[[1]]
cat(sprintf("complejidad=%d\n", length(modulos)))
```

**Qué reconocer:** los cinco colocan la documentación en un sitio distinto y eso predice cuánto se
pudre. Perl está en un extremo que no tiene igual en toda la página: POD se escribe **dentro del
fuente**, mezclado con el código, y el manual completo del lenguaje se distribuye así — cuando lees
`perldoc` estás leyendo comentarios de los módulos instalados en tu máquina. Tcl está en el otro
extremo, con `doctools` en ficheros separados, que es el modelo más fácil de dejar desactualizado.
R aporta una lección de ingeniería distinta: su formato oficial resultó tan incómodo que la comunidad
construyó una capa encima, roxygen2, y hoy casi nadie escribe el formato que el lenguaje realmente
exige. Ocurre a menudo: el estándar oficial sobrevive como *formato de salida* de la herramienta que
la gente sí usa.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
JSDoc empezó como comentarios y acabó siendo casi un sistema de tipos; TypeScript resolvió lo mismo
llevándose los tipos al lenguaje y dejando el comentario para la prosa.

### Dart

```dart
import 'dart:io';

/// Cuenta los módulos que componen un sistema.
///
/// Dart documenta con `///` y admite Markdown. Lo interesante es que el
/// analizador COMPRUEBA la documentación: una referencia entre corchetes a un
/// símbolo que no existe produce un aviso, igual que un error de código.
void main() {
  final modulos = stdin.readLineSync()!.trim().split(RegExp(r'\s+'));
  print('complejidad=${modulos.length}');
}
```

### ActionScript 3

```actionscript
package {
    /**
     * ASDoc copió la sintaxis de javadoc, etiquetas incluidas, y era parte del
     * SDK de Flex. El lenguaje no tiene stdin: aquí se recibe la lista ya hecha.
     * @param modulos los módulos del sistema
     */
    public class Metrica {
        public static function complejidad(modulos:Array):String {
            return "complejidad=" + modulos.length;
        }
    }
}
```

**Qué reconocer:** lo que Dart añade es que la documentación **se comprueba**. En casi todos los
lenguajes de esta página un comentario puede mencionar un parámetro que ya no existe y nadie protesta
nunca; el analizador de Dart avisa cuando una referencia entre corchetes apunta a un símbolo
inexistente, y con eso convierte una parte de la documentación en algo que el compilador puede
mantener honesto. Es la única defensa real contra la deuda de documentación, y la volveremos a ver en
Nim y en D con los ejemplos ejecutables. ActionScript, mientras tanto, muestra el destino habitual:
javadoc copiado tal cual, tres veces, en tres familias distintas.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Javadoc fue el formato que ganó — lo copiaron
JSDoc, ASDoc, phpDocumentor y medio mundo— y sus primos lo heredan con retoques.

### Kotlin

```kotlin
/**
 * Cuenta los módulos que componen un sistema.
 *
 * KDoc mantiene las etiquetas de javadoc (`@param`, `@return`) pero admite
 * Markdown en el cuerpo en lugar de HTML. `dokka` es el generador, y sabe
 * emitir también en formato javadoc para quien consuma la biblioteca desde Java.
 *
 * @param args no se usan; la entrada llega por stdin
 */
fun main(args: Array<String>) {
    val modulos = readLine()!!.trim().split(Regex("\\s+"))
    println("complejidad=${modulos.size}")
}
```

### Scala

```scala
/** Cuenta los módulos que componen un sistema.
  *
  * Scaladoc lo genera el PROPIO compilador (`scaladoc` comparte frontend con
  * `scalac`), así que conoce los tipos inferidos y puede documentar una firma
  * que en el fuente no está escrita.
  */
object Metrica extends App {
  val modulos = scala.io.StdIn.readLine().trim.split("\\s+")
  println(s"complejidad=${modulos.length}")
}
```

### Groovy

```groovy
/**
 * Groovydoc es javadoc adaptado a Groovy y se genera desde Gradle con la tarea
 * `groovydoc`. En un lenguaje dinámico documenta menos de lo que parece: los
 * tipos no están, así que el texto carga con todo el peso.
 */
def modulos = System.in.newReader().readLine().trim().split(/\s+/)
println "complejidad=${modulos.length}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(defn complejidad
  "Cuenta los módulos que componen un sistema.

  En Clojure la docstring es un ARGUMENTO de `defn`, no un comentario: se
  guarda en los metadatos del var y se consulta en EJECUCIÓN con
  `(doc complejidad)`. La documentación es un dato del programa vivo."
  [linea]
  (count (str/split (str/trim linea) #"\s+")))

(println (str "complejidad=" (complejidad (read-line))))
```

**Qué reconocer:** cuatro lenguajes sobre la misma máquina y dos filosofías incompatibles. Kotlin,
Scala y Groovy tratan la documentación como **comentario**: un texto que el compilador ignora y que
una herramienta externa recoge después para producir HTML. Clojure la trata como **dato**: la
docstring es un argumento de `defn`, vive en los metadatos del var y se consulta desde el REPL con
`(doc ...)` sin generar nada. La consecuencia práctica es grande — en Clojure puedes preguntarle a un
programa en marcha qué hace una función, y puedes recorrer programáticamente la documentación de un
espacio de nombres, porque es una estructura de datos más. Scala aporta otro matiz que se agradece en
un lenguaje con inferencia agresiva: como el generador es el compilador, la documentación muestra la
firma completa aunque el fuente no la escriba.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). La rareza de .NET es que la documentación es un
**artefacto del build**: el compilador la extrae a un XML que luego consumen el IDE y NuGet.

### F\#

```fsharp
/// Cuenta los módulos que componen un sistema.
/// Los comentarios `///` de .NET se compilan a un fichero XML aparte que se
/// publica JUNTO al ensamblado: por eso el IDE muestra la documentación de una
/// biblioteca de terceros para la que no tienes el código fuente.
let complejidad (linea: string) =
    linea.Split([| ' '; '\t' |], System.StringSplitOptions.RemoveEmptyEntries).Length

printfn "complejidad=%d" (complejidad (stdin.ReadLine()))
```

### VB.NET

```vbnet
Module Metrica
    ''' <summary>Cuenta los módulos que componen un sistema.</summary>
    ''' <remarks>VB.NET documenta con `'''` y etiquetas XML. El compilador
    ''' valida esas etiquetas: nombrar un parámetro que no existe produce un
    ''' aviso de compilación, no un comentario mentiroso silencioso.</remarks>
    Sub Main()
        Dim modulos = Console.ReadLine().Split(New Char() {" "c, ControlChars.Tab},
                                               StringSplitOptions.RemoveEmptyEntries)
        Console.WriteLine($"complejidad={modulos.Length}")
    End Sub
End Module
```

**Qué reconocer:** aquí la documentación deja de ser prosa para desarrolladores y se convierte en un
**fichero que se distribuye**. El XML viaja empaquetado junto al `.dll` en el paquete NuGet, y eso
explica algo que se da por hecho: que al escribir el nombre de un método de una biblioteca ajena
aparezca la descripción de sus parámetros aunque no tengas ni una línea de su código. La otra pieza
importante es que el compilador **valida** las etiquetas —documentar un parámetro que no existe da un
aviso—, la misma defensa contra la deuda que veíamos en Dart. En una página llena de comentarios que
nadie comprueba, .NET y Dart son las excepciones que convierten la documentación en algo que el build
puede vigilar.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). C nunca tuvo formato de documentación, y ese vacío lo
llenó una herramienta externa que acabó sirviendo a media industria: Doxygen.

### C++

```cpp
#include <iostream>
#include <string>

//! @brief Cuenta los módulos que componen un sistema.
//!
//! Doxygen es la herramienta común de toda la familia C: no pertenece a ningún
//! lenguaje y los sirve a todos —C, C++, Objective-C, y de propina Java, PHP o
//! Python. Su ventaja es que también extrae la estructura del código
//! (jerarquías, grafos de llamadas) sin que nadie la documente.
int main() {
    std::string modulo;
    int n = 0;
    while (std::cin >> modulo) {
        ++n;
    }
    std::cout << "complejidad=" << n << "\n";
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

/// Cuenta los módulos que componen un sistema.
/// Apple usó HeaderDoc durante años; hoy la convención es documentar con `///`
/// en el HEADER, y Xcode lo muestra en el Quick Help. Que la documentación viva
/// en el `.h` no es casual: el header ya era la interfaz pública del módulo.
int main(void) {
    char buf[512] = {0};
    fgets(buf, sizeof buf, stdin);
    NSArray<NSString *> *piezas = [@(buf) componentsSeparatedByCharactersInSet:
        NSCharacterSet.whitespaceAndNewlineCharacterSet];
    NSUInteger n = 0;
    for (NSString *pieza in piezas) {
        if (pieza.length > 0) {
            n++;
        }
    }
    printf("complejidad=%lu\n", (unsigned long)n);
}
```

**Qué reconocer:** esta familia aporta las dos ideas menos obvias de la página. La primera es que
Doxygen, al ser externo a todos los lenguajes, hace algo que ninguna herramienta integrada se molesta
en hacer: **documentar lo que nadie documentó**, extrayendo jerarquías de clases, dependencias entre
ficheros y grafos de llamadas directamente del código. Contra la deuda técnica eso vale más que
cualquier `@param`, porque no requiere disciplina de nadie. La segunda la da Objective-C: cuando el
lenguaje separa header e implementación, la documentación tiene un sitio natural y evidente —la
interfaz pública— y la distinción entre lo que se documenta y lo que se oculta viene dada por la
estructura del proyecto, no por la buena voluntad de quien escribe.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Los dos hicieron el mismo
descubrimiento: si los **ejemplos de la documentación se compilan y se ejecutan** con las pruebas, no
pueden quedarse obsoletos.

### Zig

```zig
const std = @import("std");

/// Cuenta los módulos que componen un sistema.
/// `zig doc` genera la documentación desde los comentarios `///`, y el
/// compilador RECHAZA un `///` que no preceda a una declaración: no se puede
/// dejar documentación huérfana apuntando a nada. Los comentarios normales
/// usan `//` y no entran nunca en la documentación.
pub fn main() !void {
    var buf: [512]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;

    var n: usize = 0;
    var it = std.mem.tokenizeAny(u8, linea, " \t\r");
    while (it.next()) |_| {
        n += 1;
    }

    try std.io.getStdOut().writer().print("complejidad={d}\n", .{n});
}
```

### Nim

```nim
import std/strutils

proc complejidad(linea: string): int =
  ## Cuenta los módulos que componen un sistema.
  ##
  ## Los comentarios `##` son parte del AST, no texto ignorado, y `nim doc` los
  ## extrae. Además, un bloque `runnableExamples` dentro de una docstring SE
  ## COMPILA Y SE EJECUTA con las pruebas: un ejemplo roto rompe el build.
  linea.splitWhitespace().len

echo "complejidad=", complejidad(stdin.readLine())
```

### D

```d
import std.stdio, std.string, std.array;

/++
 + Cuenta los módulos que componen un sistema.
 +
 + DDoc está integrado EN EL COMPILADOR: `dmd -D` genera el HTML sin ninguna
 + herramienta externa, y los `unittest` marcados como documentados aparecen en
 + la página como ejemplos — ejemplos que además se ejecutan al probar.
 +/
void main() {
    immutable modulos = readln().strip().split();
    writefln("complejidad=%d", modulos.length);
}
```

**Qué reconocer:** esta familia da la única respuesta estructural a la deuda de documentación que
aparece en toda la página: **hacer que el ejemplo sea código de verdad**. `runnableExamples` de Nim
se compila y se ejecuta con las pruebas; los `unittest` documentados de D salen en la página generada
y a la vez corren en el build; y en el núcleo, los doctests de Rust y los `Example` de Go hacen
exactamente lo mismo. La diferencia con un `@param` es que aquí la documentación **no puede** mentir
sin romper el build. Zig aporta una variante más pequeña pero del mismo espíritu: distingue `//` de
`///` a nivel de gramática y rechaza documentación que no documenta nada, con lo que impide que el
formato se use como comentario suelto. Y D vuelve a demostrar su preferencia por integrar en el
compilador lo que otros dejan fuera.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). En SQL la documentación mínima es el propio
esquema —nombres de tabla y columna, restricciones— y lo demás vive en `COMMENT ON`, que casi nadie
usa.

### Prolog

```prolog
:- initialization(main, main).

%!  complejidad(+Linea:string, -N:integer) is det.
%
%   Cuenta los módulos que componen un sistema. PlDoc usa `%!` y documenta algo
%   que ningún otro formato de esta página nombra: el MODO de cada argumento
%   (`+` entrada, `-` salida) y el DETERMINISMO (`is det`, `is nondet`,
%   `is semidet`). En un lenguaje donde un predicado puede devolver varias
%   soluciones o ninguna, eso es más informativo que el tipo.
complejidad(Linea, N) :-
    split_string(Linea, " ", " ", Piezas0),
    exclude(==(""), Piezas0, Piezas),
    length(Piezas, N).

main :-
    read_line_to_string(user_input, Linea),
    complejidad(Linea, N),
    format("complejidad=~w~n", [N]).
```

### Datalog

```datalog
% La documentación de un programa Datalog es su propio esquema de relaciones:
% sin control de flujo, sin estado y sin orden de ejecución, no queda un "cómo
% funciona" que explicar aparte del "qué significa cada tupla". La agregación
% de abajo usa la sintaxis de Soufflé; el Datalog puro clásico no agrega.
modulo("a").
modulo("b").
modulo("c").

complejidad(N) :- N = count : { modulo(_) }.
```

**Qué reconocer:** PlDoc documenta la dimensión que el resto de la página ni siquiera tiene nombre
para describir. En un lenguaje imperativo basta con decir qué tipos entran y qué tipo sale; en Prolog
el mismo predicado puede usarse **al derecho y al revés** —dando la entrada y pidiendo la salida, o
al contrario— y puede tener una solución, ninguna o infinitas. Por eso su documentación anota modos y
determinismo: sin esa información, saber los tipos no te dice cómo llamarlo. Datalog cierra con la
conclusión más limpia sobre mantenibilidad de toda la serie: cuando un programa no tiene estado ni
orden de ejecución, **la documentación y el programa tienden a converger**, porque las reglas ya se
leen como la especificación. Toda la deuda técnica que hemos ido nombrando vive en la distancia entre
lo que el código hace y lo que dice hacer, y esa distancia se encoge cuando el código deja de decir
*cómo*.

---

## Y de vuelta a la clase

Veinte lenguajes y una pregunta que ordena a todos: **quién impide que la documentación mienta**. En
la mayoría, nadie —un comentario obsoleto no rompe nada, y ahí nace la deuda. Unos pocos ponen al
compilador a vigilar: Dart avisa de referencias inexistentes, .NET valida las etiquetas XML, Zig
rechaza un `///` huérfano. Y la familia de sistemas da la respuesta más completa al hacer que los
ejemplos sean pruebas reales —`runnableExamples` de Nim, los `unittest` documentados de D, los
doctests de Rust—, con lo que un ejemplo desactualizado deja de ser un despiste y pasa a ser un build
roto. Entre medias queda POD de Perl como el recordatorio más elegante de todos: si el manual del
lenguaje vive dentro del código del lenguaje, nadie puede actualizar uno y olvidarse del otro.

⏮️ [Volver a la clase 154](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
