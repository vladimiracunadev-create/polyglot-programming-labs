# 🧬 El mismo programa en las familias de lenguajes — Clase 140

> [⬅️ Volver a la clase 140](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —decidir si dos resultados son equivalentes, que es
justo lo que hace el verificador de este curso— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `x y`, los dos resultados a comparar
- **Salida** (stdout): `equivalente=true` o `equivalente=false`
- **Regla:** son equivalentes si `x` e `y` coinciden como texto, byte a byte

| stdin | esperado |
|---|---|
| `6 6` | `equivalente=true` |
| `5 7` | `equivalente=false` |
| `0 0` | `equivalente=true` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La prueba de integración compara **salidas**, no valores internos, y por eso la comparación se hace
sobre el texto tal como salió del proceso.

### Ruby

```ruby
x, y = STDIN.gets.split
puts "equivalente=#{x == y}"
```

### Perl

```perl
my ($x, $y) = split ' ', <STDIN>;
print "equivalente=", ($x eq $y ? "true" : "false"), "\n";
```

### Lua

```lua
local x, y = io.read("l"):match("(%S+)%s+(%S+)")
print("equivalente=" .. tostring(x == y))
```

### Tcl

```tcl
lassign [split [gets stdin]] x y
set r [expr {$x eq $y ? "true" : "false"}]
puts "equivalente=$r"
```

### R

```r
v <- strsplit(readLines("stdin", n = 1), " ")[[1]]
cat(sprintf("equivalente=%s\n", if (identical(v[1], v[2])) "true" else "false"))
```

**Qué reconocer:** Perl separa la comparación de textos (`eq`) de la de números (`==`), y Tcl hace lo
mismo con `eq` frente a `==`; en Ruby, Lua y R el mismo `==` sirve para ambos y decide según el tipo
del valor. Esa distinción es exactamente la que tiene que tomar un verificador de equivalencia:
`6` y `6.0` son iguales como números y distintos como texto. R lo lleva más lejos que nadie, con
`identical()` para la igualdad estricta y `all.equal()` para la igualdad **con tolerancia**, la
herramienta que necesitas cuando comparas cálculos en coma flotante. En cuanto al andamiaje, aquí
integrar significa arrancar procesos: Ruby lo hace desde **Minitest** o **RSpec**, Perl con
**`Test::More`** emitiendo **TAP** —un protocolo de texto plano nacido en Perl, y precisamente por
ser texto plano es capaz de agregar resultados de pruebas escritas en lenguajes distintos, que es el
problema que resuelve este curso—, Lua con **busted**, R con **testthat** y Tcl con **tcltest**.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final v = stdin.readLineSync()!.trim().split(RegExp(r'\s+'));
  print('equivalente=${v[0] == v[1]}');
}
```

### ActionScript 3

```actionscript
// Sin stdin en el reproductor Flash: la comparación se expone como función pura.
package {
    public class Equivalencia {
        public static function comparar(x:String, y:String):String {
            return "equivalente=" + (x === y);
        }
    }
}
```

**Qué reconocer:** en Dart `==` sobre `String` compara **contenido**, no identidad, y por eso no hace
falta el `===` que ActionScript hereda de la misma tradición de JavaScript. Ese `===` es el aviso de
que en la familia web conviven dos igualdades: la que convierte tipos y la que no. Para integrar,
Dart ofrece `Process.run` dentro de `package:test`, así que arrancar el binario de otro lenguaje y
comparar su stdout se escribe con el mismo corredor que las pruebas unitarias. ActionScript no tiene
entrada estándar: su versión no puede ser una prueba de integración de verdad, solo la función que
compararía los dos resultados.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La igualdad es el ejemplo clásico de la
plataforma: hay dos, y confundirlas es el error de principiante.

### Kotlin

```kotlin
fun main() {
    val (x, y) = readLine()!!.trim().split(Regex("\\s+"))
    println("equivalente=${x == y}")
}
```

### Scala

```scala
object Equivalencia {
  def main(args: Array[String]): Unit = {
    val Array(x, y) = scala.io.StdIn.readLine().trim.split("\\s+")
    println(s"equivalente=${x == y}")
  }
}
```

### Groovy

```groovy
def (x, y) = System.in.newReader().readLine().trim().split(/\s+/)
println "equivalente=${x == y}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [[x y] (str/split (str/trim (read-line)) #"\s+")]
  (println (str "equivalente=" (= x y))))
```

**Qué reconocer:** en Java `==` sobre dos `String` compara **referencias** y hay que escribir
`equals`; Kotlin, Scala y Groovy redefinen `==` para que llame a `equals` por debajo, y Clojure usa
`=`, que compara por valor estructural. Cuatro lenguajes sobre la misma máquina, y la trampa de Java
desactivada en los cuatro. Para la integración vuelve a mandar la plataforma: **JUnit** conduce las
pruebas de Java y Kotlin, Scala usa **ScalaTest** o **MUnit**, Groovy tiene **Spock** —cuyos bloques
`when`/`then` describen un escenario completo, que es justo la forma de una prueba de integración— y
Clojure trae **`clojure.test`** en la estándar. Todos acaban lanzando el proceso con `ProcessBuilder`
de Java y comparando el `String` resultante.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let [| x; y |] = stdin.ReadLine().Trim().Split(' ')
printfn "equivalente=%b" (x = y)
```

### VB.NET

```vbnet
Module Equivalencia
    Sub Main()
        Dim v = Console.ReadLine().Trim().Split(" "c)
        Console.WriteLine("equivalente=" & If(v(0) = v(1), "true", "false"))
    End Sub
End Module
```

**Qué reconocer:** hay un detalle que muerde a cualquiera que escriba un verificador en .NET: el
`Boolean.ToString()` del CLR produce `True` y `False` **con mayúscula inicial**, así que la
concatenación directa rompería el contrato y por eso VB.NET escribe los literales a mano. F# esquiva
el problema con `%b` de `printfn`, que sí emite minúsculas. En cuanto a las herramientas, **NUnit** y
**xUnit** sirven a los tres lenguajes del CLR sin cambios, porque el corredor solo ve atributos sobre
métodos del ensamblado. F# añade **FsCheck**: para una prueba de equivalencia es la pieza ideal,
porque en vez de tres casos fijos declaras la propiedad *"para toda entrada, núcleo y primo dan lo
mismo"* y la herramienta busca el contraejemplo por ti.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Donde una cadena es un puntero, comparar es la
operación con más trampas del lenguaje.

### C++

```cpp
#include <iostream>
#include <string>

int main() {
    std::string x, y;
    std::cin >> x >> y;
    std::cout << "equivalente=" << (x == y ? "true" : "false") << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        char bx[64], by[64];
        scanf("%63s %63s", bx, by);
        NSString *x = @(bx), *y = @(by);
        BOOL igual = [x isEqualToString:y];
        printf("equivalente=%s\n", igual ? "true" : "false");
    }
    return 0;
}
```

**Qué reconocer:** en C hay que llamar a `strcmp` porque `==` compararía direcciones de memoria. C++
arregla eso envolviendo el búfer en `std::string`, cuyo `operator==` compara contenido; Objective-C
**no** lo arregla —`x == y` sobre dos `NSString *` sigue comparando punteros— y obliga a escribir
`isEqualToString:`, un recordatorio de que su capa de objetos está encima de C, no en lugar de C.
Fíjate también en la salida: C++ imprimiría `1` y `0` si se pasara el `bool` directo a `cout`, y hace
falta `std::boolalpha` para obtener `true`/`false`. Para integrar, C++ recurre otra vez a bibliotecas
externas —**Catch2** o **GoogleTest**— mientras que Objective-C usa **XCTest**, que en Xcode ya trae
soporte para pruebas que arrancan la aplicación entera.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilan a binario, así
que la prueba de integración natural es ejecutar el binario y mirar su stdout.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [128]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \r\t");
    const x = it.next().?;
    const y = it.next().?;
    const igual = std.mem.eql(u8, x, y);
    try std.io.getStdOut().writer().print("equivalente={}\n", .{igual});
}
```

### Nim

```nim
import std/strutils

let v = stdin.readLine().splitWhitespace()
echo "equivalente=", v[0] == v[1]
```

### D

```d
import std.stdio, std.array;

void main() {
    auto v = readln().split();
    writeln("equivalente=", v[0] == v[1]);
}
```

**Qué reconocer:** Zig no tiene operador de igualdad para porciones de memoria —`==` sobre dos
`[]const u8` compararía puntero y longitud—, así que la comparación de contenido se pide
explícitamente con `std.mem.eql`, igual de explícito que reservar el búfer a mano. Nim y D sí
sobrecargan `==` para cadenas y, además, imprimen `true`/`false` en minúscula sin ayuda, algo que
casualmente encaja con este contrato. Lo importante de la familia sigue siendo lo mismo de la clase
anterior: **las pruebas vienen integradas en el lenguaje** —`test` en Zig, `unittest` en D,
`unittest` en Nim—, de modo que la prueba de integración que lanza un subproceso se escribe en el
mismo archivo que el programa, sin instalar nada.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Comparar dos resultados es, aquí, una consulta
sobre relaciones.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", [X, Y]),
    (   X == Y
    ->  R = true
    ;   R = false
    ),
    format("equivalente=~w~n", [R]).
```

### Datalog

```datalog
% Datalog no tiene E/S: los dos resultados entran como hechos y la
% equivalencia es una regla que solo se deriva si ambos unifican.
resultado(nucleo, 6).
resultado(primo, 6).

equivalente :- resultado(nucleo, V), resultado(primo, V).
```

**Qué reconocer:** el caso de Datalog no es una limitación, es el **verificador de equivalencia
escrito en su forma más pura**: dos hechos, una regla, y la equivalencia se deriva sola porque la
misma variable `V` tiene que unificar con ambos resultados. No hay comparación explícita ni
condicional; la unificación *es* la comparación. Prolog añade la ejecución y con ella la distinción
entre `==` (idénticos como términos) y `=:=` (iguales al evaluarlos como números), la misma
disyuntiva de texto contra número que aparecía en la primera familia. Y es lo mismo que hace SQL con
un `EXCEPT` entre dos consultas: si el resultado viene vacío, son equivalentes.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una única pregunta debajo: **¿qué significa que dos cosas sean
iguales?** Igual como punteros, como bytes, como números con tolerancia, o como términos que
unifican. El verificador de este curso escoge la respuesta más burda a propósito —comparar el stdout
byte a byte— porque es la única que veinte lenguajes distintos pueden cumplir sin ponerse de acuerdo
en nada más. Eso es lo transferible.

⏮️ [Volver a la clase 140](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
