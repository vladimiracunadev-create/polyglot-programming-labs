# 🧬 El mismo programa en las familias de lenguajes — Clase 174

> [⬅️ Volver a la clase 174](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —etiquetar el artefacto que se va a desplegar con su
versión— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo
por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): una versión `mayor.menor.parche`
- **Salida** (stdout): `imagen=app:<versión>`
- **Regla:** componer el nombre de imagen `app:` seguido de la versión leída

| stdin | esperado |
|---|---|
| `1.2.3` | `imagen=app:1.2.3` |
| `0.9.0` | `imagen=app:0.9.0` |
| `2.1.5` | `imagen=app:2.1.5` |

El programa es de una línea a propósito. Lo interesante de esta clase no es el código: es **lo que
hay que meter en la imagen para que ese código arranque en destino**, y eso cambia de forma radical
de una familia a otra. Cada apartado lo dice con cifras de orden de magnitud.

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Nada que compilar, todo que instalar: el artefacto es el fuente, y el intérprete viaja con él.

### Ruby

```ruby
version = STDIN.gets.strip
puts "imagen=app:#{version}"
```

### Perl

```perl
chomp(my $version = <STDIN>);
print "imagen=app:$version\n";
```

### Lua

```lua
local version = io.read("l")
print("imagen=app:" .. version)
```

### Tcl

```tcl
gets stdin version
puts "imagen=app:[string trim $version]"
```

### R

```r
version <- trimws(readLines("stdin", n = 1))
cat(sprintf("imagen=app:%s\n", version))
```

**Qué reconocer:** los cinco *fuentes* pesan menos de un kilobyte y ninguno de los cinco se despliega
solo. La imagen tiene que llevar el intérprete: una base *slim* de Python o Ruby ronda las **decenas
de megabytes**, la imagen completa con toolchain de compilación de extensiones nativas se va a
**cientos de megabytes**, y una imagen de R con su pila estadística habitual es de las más pesadas
del ecosistema. Lua es el extremo opuesto **dentro de la misma familia**: su intérprete completo cabe
en unos pocos cientos de kilobytes, que es justamente por lo que se empotra en routers, juegos y
firmware. Misma familia, tres órdenes de magnitud de diferencia en lo que hay que desplegar.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final version = stdin.readLineSync()!.trim();
  print('imagen=app:$version');
}
```

### ActionScript 3

```actionscript
// ActionScript no lee stdin ni se despliega como proceso: el artefacto es un SWF,
// y la version se incrusta en tiempo de compilacion (mxmlc -define), no se lee al
// arrancar. Lo mas cercano al contrato es componer la etiqueta como funcion pura.
package {
    public class Empaquetado {
        public static function nombreImagen(version:String):String {
            return "imagen=app:" + version;
        }
    }
}
```

**Qué reconocer:** Dart es el caso más instructivo de la página, porque **puede empaquetarse de las
dos maneras**: interpretado sobre su VM, como Node, o compilado a un ejecutable nativo autocontenido
con `dart compile exe`, del orden de unos pocos megabytes y sin nada que instalar en destino. La
misma lógica de negocio, dos artefactos de tamaños incomparables, decidido por una bandera del
compilador. En la rama JavaScript, el `node_modules` de un proyecto real es casi siempre más pesado
que el propio runtime, y ese es el argumento que hay que llevar a la defensa del diseño. ActionScript
enseña el otro final: un artefacto que **necesita un anfitrión que ya no existe** —el reproductor
Flash— es un artefacto no desplegable, por muy pequeño que sea.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Un mismo `.jar` corre en cualquier sitio donde
haya una JVM; el precio es que tiene que haber una JVM.

### Kotlin

```kotlin
fun main() {
    val version = readLine()!!.trim()
    println("imagen=app:$version")
}
```

### Scala

```scala
object Empaquetado extends App {
  val version = scala.io.StdIn.readLine().trim
  println(s"imagen=app:$version")
}
```

### Groovy

```groovy
def version = System.in.newReader().readLine().trim()
println "imagen=app:$version"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(println (str "imagen=app:" (str/trim (read-line))))
```

**Qué reconocer:** los cuatro producen bytecode intercambiable, pero **no producen artefactos del
mismo tamaño**. Kotlin añade su pequeña biblioteca de runtime; Scala y Clojure arrastran una
biblioteca estándar propia de **varios megabytes** que hay que empaquetar en cada *fat jar*, porque
la JVM no la trae. Y por debajo de todos ellos está la imagen base: una imagen con JDK completo se
mide en **cientos de megabytes**, un JRE recortado con `jlink` baja a unas **decenas**, y GraalVM
Native Image puede llegar a un binario nativo de pocas decenas de megabytes a costa de perder la
carga dinámica de clases. Elegir Scala en vez de Java no cambia el orden de magnitud del despliegue;
elegir JVM en vez de un lenguaje de sistemas, sí.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let version = stdin.ReadLine().Trim()
printfn "imagen=app:%s" version
```

### VB.NET

```vbnet
Module Empaquetado
    Sub Main()
        Dim version = Console.ReadLine().Trim()
        Console.WriteLine("imagen=app:" & version)
    End Sub
End Module
```

**Qué reconocer:** los tres lenguajes del CLR comparten exactamente la misma historia de
empaquetado, y es una historia con tres puertas. La publicación *dependiente del framework* deja un
artefacto diminuto pero exige el runtime .NET instalado en destino —del orden de las decenas a
cientos de megabytes en la imagen base—. La publicación *autocontenida* mete el runtime dentro y
produce algo de **decenas de megabytes**. Y la compilación **AOT nativa** recorta el resultado a un
binario de pocos megabytes, sin JIT y sin reflexión dinámica. F# hereda las tres sin escribir una
línea distinta de las de C#: la decisión de despliegue es del ecosistema, no del lenguaje.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). El artefacto es un binario y punto.

### C++

```cpp
#include <iostream>
#include <string>

int main() {
    std::string version;
    std::cin >> version;
    std::cout << "imagen=app:" << version << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        char buf[64];
        if (scanf("%63s", buf) != 1) return 1;
        NSString *imagen = [NSString stringWithFormat:@"imagen=app:%s", buf];
        printf("%s\n", [imagen UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** un binario de C enlazado estáticamente cabe en **cientos de kilobytes** y se
despliega sobre una imagen `scratch`, literalmente vacía: la imagen final *es* el ejecutable. C++
paga un sobrecoste real por su biblioteca estándar —`<iostream>` es notoriamente pesado, y un
binario estático típico se va a **unos pocos megabytes**—, pero sigue en el mismo orden de magnitud.
Objective-C rompe la regla: aunque el código sea C, `Foundation` es un framework de plataforma, así
que fuera del ecosistema de Apple el despliegue exige GNUstep y deja de ser autocontenido. La lección
transferible es la trampa clásica: enlazar contra glibc dinámicamente y luego construir la imagen
sobre Alpine, que usa musl, produce un binario que compila y no arranca.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). La familia que hizo del
binario único su argumento de venta.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const version = std.mem.trim(u8, linea, " \r\t");
    try std.io.getStdOut().writer().print("imagen=app:{s}\n", .{version});
}
```

### Nim

```nim
import std/strutils

let version = stdin.readLine().strip()
echo "imagen=app:", version
```

### D

```d
import std.stdio, std.string;

void main() {
    // `version` es palabra reservada en D: nombra la compilacion condicional
    // (version = release), asi que la variable se llama distinto.
    const etiqueta = readln().strip();
    writeln("imagen=app:", etiqueta);
}
```

**Qué reconocer:** este es el argumento de ingeniería más medible de toda la clase. Un binario
estático de Zig, Nim, D, Go o Rust se cuenta en **megabytes** —a menudo uno o dos— y **no necesita
absolutamente nada instalado en destino**: la imagen de contenedor puede ser `FROM scratch` con un
solo fichero dentro. Frente a eso, una imagen con JVM o con intérprete arrastra **cientos de
megabytes** de runtime que no es tuyo, que hay que parchear cuando sale un CVE y que se descarga en
cada despliegue. Dos órdenes de magnitud de diferencia, y se nota en el tiempo de arranque, en la
factura del registro de imágenes y en la superficie de ataque. Zig lleva la idea más lejos que nadie:
su toolchain compila para otras plataformas sin instalar nada extra, con `-target`, y de hecho se usa
como compilador cruzado de proyectos C ajenos. D, por su parte, te recuerda desde la primera línea
que en esta familia **la versión es una construcción del lenguaje**: `version` es palabra reservada y
gobierna qué código entra en el binario.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). No se despliega un ejecutable, se despliega un
motor que ya está ahí y un conjunto de sentencias que se le envían.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    normalize_space(string(Version), Linea),
    format("imagen=app:~w~n", [Version]).
```

### Datalog

```datalog
% Datalog no lee entrada ni compone salida con formato: la version es un hecho del
% programa y la etiqueta se deriva como una relacion. `cat` es la concatenacion de
% cadenas del dialecto Souffle; el Datalog puro no manipula cadenas en absoluto.
version("1.2.3").

imagen(N) :- version(V), N = cat("app:", V).
```

**Qué reconocer:** el empaquetado de esta familia invierte la pregunta. En SQL el artefacto
desplegable es la **migración**: un fichero de texto versionado que transforma el esquema, y el
"runtime" es un motor que administra otro equipo. Prolog está a medio camino —SWI-Prolog puede
guardar un estado compilado autocontenido con `qsave_program`, del orden de decenas de megabytes
porque incluye el motor entero— y Datalog directamente no produce artefacto ejecutable: se compila
a un programa que otro sistema hospeda. Cuando el componente de tu proyecto es declarativo, la
pregunta de despliegue deja de ser "cuánto pesa el binario" y pasa a ser "quién opera el motor".

---

## Y de vuelta a la clase

Veinte lenguajes, una etiqueta de imagen de una línea, y artefactos que van del **kilobyte a los
cientos de megabytes** para hacer exactamente lo mismo. Esa distancia no es trivia: decide el tiempo
de arranque en frío, el coste de almacenamiento y transferencia, la frecuencia con la que te obligan
a reconstruir por vulnerabilidades ajenas y si puedes desplegar en un dispositivo pequeño. Es
también el mejor material que tendrás para la clase siguiente, donde hay que **defender** por qué
cada componente está escrito en el lenguaje en que está.

⏮️ [Volver a la clase 174](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
