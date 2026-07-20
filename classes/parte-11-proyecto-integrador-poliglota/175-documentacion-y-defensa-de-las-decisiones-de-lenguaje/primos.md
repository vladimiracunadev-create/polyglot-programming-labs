# 🧬 El mismo programa en las familias de lenguajes — Clase 175

> [⬅️ Volver a la clase 175](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —informar cuántas secciones tiene la documentación—
resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los
diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`, las secciones documentadas
- **Salida** (stdout): `documentado=<n> secciones`
- **Regla:** informar el número de secciones

| stdin | esperado |
|---|---|
| `5` | `documentado=5 secciones` |
| `1` | `documentado=1 secciones` |
| `8` | `documentado=8 secciones` |

Cada programa lleva además el **comentario de documentación nativo** de su lenguaje, porque esa es la
mitad visible de esta clase. La otra mitad es la que de verdad se examina: **cómo se argumenta la
elección de un lenguaje ante un equipo**. Los "Qué reconocer" de abajo no describen sintaxis; ponen,
familia por familia, los criterios **verificables** con los que se defiende una decisión y los que
solo son preferencia disfrazada.

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Todos generan documentación a partir de comentarios del propio fuente, siguiendo la idea del
`docstring`.

### Ruby

```ruby
# Informa cuantas secciones tiene la documentacion del proyecto.
# El comentario previo a la definicion es lo que recogen RDoc y YARD.
n = STDIN.gets.strip
puts "documentado=#{n} secciones"
```

### Perl

```perl
=head1 NAME

secciones - informa cuantas secciones tiene la documentacion

=cut

chomp(my $n = <STDIN>);
print "documentado=$n secciones\n";
```

### Lua

```lua
--- Informa cuantas secciones tiene la documentacion del proyecto.
-- @param n numero de secciones documentadas
local n = io.read("l")
print("documentado=" .. n .. " secciones")
```

### Tcl

```tcl
# Tcl no tiene formato de doc-comment estandar. La documentacion canonica se
# escribe aparte, en paginas doctools que se convierten a nroff y a HTML.
gets stdin n
puts "documentado=[string trim $n] secciones"
```

### R

```r
#' Informa cuantas secciones tiene la documentacion
#'
#' @param n numero de secciones documentadas
#' @export
n <- readLines("stdin", n = 1)
cat(sprintf("documentado=%s secciones\n", n))
```

**Qué reconocer:** el argumento defendible de esta familia es **la velocidad hasta el primer
resultado**, y se mide: líneas de código para el mismo componente, tiempo desde el repositorio vacío
hasta un servicio que responde, número de bibliotecas que evitan escribir integración. El argumento
en contra también es medible, y hay que llevarlo escrito antes de que lo saque otro: los errores de
tipo aparecen **en ejecución**, así que la red de seguridad hay que comprarla en cobertura de
pruebas y en anotaciones de tipos. Nótese que el ecosistema respondió a eso con herramientas —Sorbet
y RBS en Ruby, mypy en Python—, y "vamos a activar el comprobador de tipos" es exactamente el tipo de
compromiso concreto que convierte una discusión de gustos en un acuerdo. **Perl** merece una nota
aparte: **POD** es documentación *incrustada en el fuente pero legible como texto*, y **R** con
`roxygen2` genera los ficheros `.Rd` que CRAN **exige** para aceptar un paquete. Ahí la documentación
no es virtud, es requisito de publicación: un criterio verificable de los buenos.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

/// Informa cuantas secciones tiene la documentacion del proyecto.
void main() {
  final n = stdin.readLineSync()!.trim();
  print('documentado=$n secciones');
}
```

### ActionScript 3

```actionscript
// ActionScript no tiene stdin; se ilustra la funcion con su ASDoc.
package {
    public class Documentacion {
        /**
         * Informa cuantas secciones tiene la documentacion.
         * @param n secciones documentadas
         * @return la linea de informe
         */
        public static function informe(n:int):String {
            return "documentado=" + n + " secciones";
        }
    }
}
```

**Qué reconocer:** esta familia da el mejor ejemplo de una defensa bien construida y de una mal
construida. La bien construida es la de TypeScript sobre JavaScript: *el mismo runtime, el mismo
ecosistema, cero coste de migración de dependencias, y un compilador que detecta antes lo que antes
detectaba el usuario*. Todo eso se verifica. La mal construida es "es más moderno". **Dart** obliga a
un argumento del mismo tipo, y el suyo es organizativo: se elige cuando **el mismo equipo** mantiene
la app Flutter y el servicio, porque comparten modelo de dominio y herramientas —y el criterio
verificable no es la sintaxis, es cuántas veces hay que definir la misma estructura de datos en dos
sitios—. **ActionScript** es la advertencia final de la familia, y por eso está aquí: fue la elección
correcta durante quince años y hoy no compila en ningún navegador. Ningún criterio que valga puede
ignorar **la trayectoria del lenguaje**: quién lo mantiene, con qué cadencia publica, y qué pasa con
tu código si esa organización deja de invertir.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Javadoc fijó el formato que copiaron casi
todos: comentario de bloque, `@param`, `@return`.

### Kotlin

```kotlin
/** Informa cuantas secciones tiene la documentacion del proyecto. */
fun main() {
    val n = readLine()!!.trim()
    println("documentado=$n secciones")
}
```

### Scala

```scala
/** Informa cuantas secciones tiene la documentacion del proyecto. */
object Documentacion extends App {
  val n = scala.io.StdIn.readLine().trim
  println(s"documentado=$n secciones")
}
```

### Groovy

```groovy
/** Informa cuantas secciones tiene la documentacion del proyecto. */
def n = System.in.newReader().readLine().trim()
println "documentado=$n secciones"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(defn informe
  "Compone la linea de informe con el numero de secciones documentadas."
  [n]
  (str "documentado=" n " secciones"))

(println (informe (str/trim (read-line))))
```

**Qué reconocer:** esta es la familia donde la defensa es **más fácil de ganar y más fácil de
perder**. Fácil de ganar porque el riesgo de plataforma es cero: mismo bytecode, mismas bibliotecas,
mismo despliegue, mismas herramientas de diagnóstico, y si el lenguaje elegido decayera el código
sigue interoperando con Java. Fácil de perder porque el criterio que decide no es técnico sino de
equipo: cuánta gente lo escribe hoy, cuánto tarda alguien nuevo en ser productivo, cuánto sube el
tiempo de compilación —en Scala eso es un número real que se mide en el CI y que la gente sí
nota—. Fíjate en **Clojure**: su docstring va **dentro** de la definición, es un valor accesible en
tiempo de ejecución con `(doc informe)`, no un comentario que un generador rasca del fuente. Es una
diferencia pequeña con una consecuencia grande —la documentación es un dato del programa— y es
justamente el tipo de detalle que hay que saber explicar sin decir "es más elegante".

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). Documentación en **XML** dentro del fuente, que
el compilador extrae a un `.xml` y consume el editor.

### F\#

```fsharp
/// Informa cuantas secciones tiene la documentacion del proyecto.
let informe (n: string) = sprintf "documentado=%s secciones" n

printfn "%s" (informe (stdin.ReadLine().Trim()))
```

### VB.NET

```vbnet
Module Documentacion
    ''' <summary>Informa cuantas secciones tiene la documentacion.</summary>
    ''' <param name="n">Secciones documentadas.</param>
    Function Informe(n As String) As String
        Return "documentado=" & n & " secciones"
    End Function

    Sub Main()
        Console.WriteLine(Informe(Console.ReadLine().Trim()))
    End Sub
End Module
```

**Qué reconocer:** el argumento de esta familia casi nunca es el lenguaje: es **el proveedor**.
Soporte comercial, ciclo de vida publicado con fechas de fin de soporte, integración con el resto de
la pila de Microsoft y una herramienta que ya está aprobada por la organización. Eso es todo
verificable y pesa más en una sala de decisión que cualquier característica de sintaxis. Dentro de
la familia, **F#** se defiende con una promesa concreta y comprobable —modelar los estados válidos
como uniones discriminadas para que un estado imposible no compile— y con un coste igual de
concreto: menos gente lo conoce y las plantillas y ejemplos vienen en C#. **VB.NET** obliga a la
parte más incómoda de esta clase: reconocer cuándo el argumento correcto es *"no lo elegimos, lo
heredamos"*. Microsoft lo mantiene soportado pero **sin nuevas características**; defender su uso
para código existente es razonable y defenderlo para un componente nuevo, no. Saber decir eso con
datos —fechas de soporte, tamaño de la base heredada, coste estimado de reescritura— es la clase
entera.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). La familia donde la documentación de referencia
sigue siendo la **página de manual** y la cabecera `.h`.

### C++

```cpp
#include <iostream>
#include <string>

/// Informa cuantas secciones tiene la documentacion del proyecto.
/// Formato Doxygen, el generador de facto de la familia.
int main() {
    std::string n;
    std::cin >> n;
    std::cout << "documentado=" << n << " secciones\n";
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

/** Informa cuantas secciones tiene la documentacion del proyecto. */
int main(void) {
    @autoreleasepool {
        char buf[64];
        scanf("%63s", buf);
        printf("documentado=%s secciones\n", buf);
    }
    return 0;
}
```

**Qué reconocer:** aquí los criterios verificables son los más duros de todo el sistema porque son
**números con unidades**: latencia de cola en microsegundos, bytes de memoria residente, ausencia de
pausas de recolección de basura, capacidad de correr sin sistema operativo. Si el requisito está
escrito así, la discusión se acaba sola. Si no lo está, elegir esta familia es adquirir una deuda que
también se mide: proporción de vulnerabilidades de memoria en el histórico del proyecto, tiempo de
compilación, coste de un *sanitizer* en el CI. Un detalle que conviene llevar preparado: cuando el
componente ha de ser **consumido desde otros lenguajes**, C gana sin discusión, porque su ABI es el
idioma común al que todas las familias saben llamar —lo que viste en la parte 10—. Eso no es
preferencia, es una propiedad del ecosistema entero.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Documentación integrada
en la herramienta oficial: `go doc` y `cargo doc` vienen con el lenguaje, no aparte.

### Zig

```zig
const std = @import("std");

/// Informa cuantas secciones tiene la documentacion del proyecto.
pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = std.mem.trim(u8, linea, " \r");
    try std.io.getStdOut().writer().print("documentado={s} secciones\n", .{n});
}
```

### Nim

```nim
import std/strutils

## Informa cuantas secciones tiene la documentacion del proyecto.
## Los comentarios `##` los recoge `nim doc` directamente.
let n = stdin.readLine().strip()
echo "documentado=" & n & " secciones"
```

### D

```d
import std.stdio, std.string;

/** Informa cuantas secciones tiene la documentacion del proyecto. */
void main() {
    const n = readln().strip();
    writefln("documentado=%s secciones", n);
}
```

**Qué reconocer:** el criterio decisivo de esta familia no es el rendimiento —eso lo dan los cinco—
sino la **madurez**, y se verifica con preguntas que tienen respuesta objetiva: ¿ha llegado a 1.0?,
¿rompe la API entre versiones?, ¿cuántos mantenedores tiene el paquete del que dependerías?, ¿existe
soporte comercial? Con eso, Go y Rust pasan y **Zig** no —sigue antes de 1.0 y cada versión cambia
cosas—, por muy bueno que sea el lenguaje. **Nim** y **D** aprueban en el lenguaje y suspenden en el
tamaño de comunidad, que es un riesgo de *bus factor* perfectamente cuantificable mirando los
repositorios de los que dependerías. Y hay un criterio que se olvida siempre y que en esta familia
manda: **de quién puedes contratar**. Un lenguaje excelente que solo entiende una persona del equipo
es un punto único de fallo, y decirlo en voz alta es parte de defender bien una decisión.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). La documentación vive en el propio esquema:
nombres de tablas, restricciones y `COMMENT ON`.

### Prolog

```prolog
:- initialization(main, main).

%!  main is det.
%
%   Informa cuantas secciones tiene la documentacion del proyecto.
%   El formato `%!` es PlDoc, el generador de SWI-Prolog.
main :-
    read_line_to_string(user_input, Linea),
    normalize_space(string(N), Linea),
    format("documentado=~w secciones~n", [N]).
```

### Datalog

```datalog
% Datalog no lee entrada ni imprime: el numero de secciones es un hecho y el
% informe una relacion derivada. Su documentacion son los nombres de las
% relaciones y sus tipos, que ya declaran el significado del programa.
secciones(5).

documentado(N) :- secciones(N).
```

**Qué reconocer:** esta familia se defiende con el argumento más limpio del sistema y también con el
más malinterpretado. El limpio: **cuando la lógica del dominio ya está escrita como reglas o como
relaciones, expresarla en un lenguaje declarativo elimina la traducción**, y eso se verifica contando
cuántas líneas imperativas desaparecen y cuántos errores de sincronización entre la regla del negocio
y el código dejan de ser posibles. El malinterpretado: nadie construye el sistema entero aquí. La
decisión honesta es de **frontera** —qué parte es declarativa y qué parte no—, y ese es exactamente el
razonamiento que sostiene el proyecto de esta parte: cada componente en la familia cuya forma
coincide con la forma del problema. Fíjate por último en Datalog: al no tener efectos, su
documentación *es* su código; el programa no puede hacer nada que sus relaciones no digan. Ese es el
techo al que aspira toda la documentación que escribas.

---

## Y de vuelta a la clase

Veinte lenguajes, una línea de informe, y el mismo examen para todos: no *cuál es mejor*, sino **qué
puedes verificar**. Trayectoria y soporte del lenguaje, madurez del ecosistema del componente,
disponibilidad de gente que lo escriba, coste de integración con el resto del sistema y qué se rompe
si la decisión resulta equivocada. Una defensa que se apoya en esas cinco cosas sobrevive a la
reunión; una que se apoya en "me gusta más" pierde ante el primero que traiga un número. Ya tienes
los números repartidos por las clases 167 a 174: esta clase solo te pide ordenarlos.

⏮️ [Volver a la clase 175](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
