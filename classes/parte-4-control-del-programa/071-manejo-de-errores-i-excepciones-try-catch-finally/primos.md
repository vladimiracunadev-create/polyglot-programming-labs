# 🧬 El mismo programa en las familias de lenguajes — Clase 071

> [⬅️ Volver a la clase 071](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —dividir dos enteros y sobrevivir al divisor cero—
resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los
diez lenguajes del núcleo.

Y aquí aparece la pregunta incómoda que la clase deja planteada: **no todos los lenguajes fallan al
dividir por cero**, y varios de estos veinte ni siquiera tienen excepciones. Cuando eso pasa, el
código lo dice en un comentario en vez de fingir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b`, dos enteros
- **Salida** (stdout): `resultado=<a/b entera>`, o `error=division por cero` si `b` es 0
- **Regla:** si `b != 0` → división entera; si `b == 0` → el mensaje de error

| stdin | esperado |
|---|---|
| `10 2` | `resultado=5` |
| `7 0` | `error=division por cero` |
| `9 3` | `resultado=3` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
`try` / `except` / `finally` con nombres distintos en cada primo, y una excepción que a veces no
llega a lanzarse nunca.

### Ruby

```ruby
a, b = STDIN.gets.split.map(&:to_i)
begin
  puts "resultado=#{a / b}"
rescue ZeroDivisionError
  puts "error=division por cero"
end
```

### Perl

```perl
my ($a, $b) = split ' ', <STDIN>;
# Perl no tiene try/catch clásico: `die` lanza y `eval { }` atrapa en $@.
my $r = eval {
    die "div0\n" if $b == 0;
    int($a / $b);
};
if ($@) {
    print "error=division por cero\n";
} else {
    print "resultado=$r\n";
}
```

### Lua

```lua
local a, b = io.read("n", "n")
-- `pcall` (protected call) ejecuta y devuelve ok + valor o ok + mensaje.
local ok, r = pcall(function()
  if b == 0 then error("div0") end
  return a // b
end)
if ok then
  print(string.format("resultado=%d", r))
else
  print("error=division por cero")
end
```

### Tcl

```tcl
gets stdin linea
lassign [split $linea] a b
# `catch` devuelve 0 si todo fue bien y deja el resultado (o el mensaje) en la variable.
if {[catch {expr {$a / $b}} r]} {
    puts "error=division por cero"
} else {
    puts "resultado=$r"
}
```

### R

```r
v <- as.integer(strsplit(readLines("stdin", n = 1), " ")[[1]])
# En R dividir por cero NO es un error: 1/0 vale Inf y 1L %/% 0L vale NA.
# Hay que señalar la condición a mano con stop() para que tryCatch la vea.
res <- tryCatch({
  if (v[2] == 0) stop("division por cero")
  sprintf("resultado=%d", v[1] %/% v[2])
}, error = function(e) "error=division por cero")
cat(res, "\n", sep = "")
```

**Qué reconocer:** los cinco separan el camino feliz del camino de error, pero el mecanismo va de lo
familiar a lo ajeno. **Ruby** es Python con otros nombres (`begin` / `rescue` / `ensure`). **Perl** no
tiene una sintaxis de excepciones: `die` lanza cualquier cosa y `eval` la atrapa en `$@`, un patrón
tan incómodo que la comunidad escribió `Try::Tiny` para maquillarlo. **Lua** y **Tcl** ni siquiera
usan bloques: envuelven la llamada en una función (`pcall`, `catch`) que devuelve un booleano de
éxito —es decir, convierten la excepción en un **valor de retorno**, que es exactamente el tema de la
clase 072—. Y **R** revela el detalle más importante de la página: su división por cero **no falla**,
devuelve `Inf` o `NA`, así que la excepción hay que fabricarla.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
En JavaScript `10 / 0` es `Infinity`: no hay excepción que atrapar, porque todos los números son
coma flotante IEEE 754.

### Dart

```dart
import 'dart:io';

void main() {
  final v = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  try {
    print('resultado=${v[0] ~/ v[1]}');
  } on UnsupportedError {
    // Dart 3 sustituyó IntegerDivisionByZeroException por UnsupportedError.
    print('error=division por cero');
  }
}
```

### ActionScript 3

```actionscript
// AS3 no tiene stdin, y su división nunca lanza: 10/0 da Infinity porque
// Number es coma flotante. El error se lanza a mano para mostrar try/catch.
package {
    public class Division {
        public static function dividir(a:int, b:int):String {
            try {
                if (b == 0) throw new Error("division por cero");
                return "resultado=" + int(a / b);
            } catch (e:Error) {
                return "error=division por cero";
            } finally {
                // El bloque finally se ejecuta con o sin error.
            }
        }
    }
}
```

**Qué reconocer:** **Dart** rompe con su familia al recuperar la división entera (`~/`), y con ella
vuelve el error: dividir enteros por cero sí lanza, mientras que `10 / 0` con el operador normal
sigue dando `Infinity` como en JavaScript. **ActionScript** se quedó en el modelo original —un solo
tipo numérico, ningún error— y por eso su bloque `try` solo tiene sentido con un `throw` escrito a
mano. Cuando la operación no falla, `try` / `catch` no protege de nada.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La JVM lanza `ArithmeticException` al dividir
enteros por cero —y devuelve `Infinity` al dividir `double`—, así que las cuatro implementaciones
atrapan exactamente la misma clase.

### Kotlin

```kotlin
fun main() {
    val (a, b) = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    try {
        println("resultado=${a / b}")
    } catch (e: ArithmeticException) {
        println("error=division por cero")
    }
}
```

### Scala

```scala
object Division {
  def main(args: Array[String]): Unit = {
    val Array(a, b) = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
    // En Scala try/catch es una expresión: devuelve un valor.
    val salida =
      try s"resultado=${a / b}"
      catch { case _: ArithmeticException => "error=division por cero" }
    println(salida)
  }
}
```

### Groovy

```groovy
def (a, b) = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger()
try {
    // `/` sobre enteros daría un BigDecimal en Groovy: intdiv() es la división entera.
    println "resultado=${a.intdiv(b)}"
} catch (ArithmeticException e) {
    println "error=division por cero"
}
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [[a b] (map #(Long/parseLong %) (str/split (str/trim (read-line)) #"\s+"))]
  (println (try
             (str "resultado=" (quot a b))
             (catch ArithmeticException _ "error=division por cero"))))
```

**Qué reconocer:** misma excepción, cuatro actitudes. **Kotlin** eliminó las *checked exceptions* de
Java: ninguna función te obliga a declarar lo que puede lanzar, decisión deliberada tras años de
`throws IOException` decorativos. **Scala** y **Clojure** hacen de `try` una **expresión** que
produce un valor —fíjate en que el `println` está fuera, y que ambos brazos devuelven la línea
completa—, mientras que en Java el `try` es una instrucción y hace falta una variable mutable o un
`println` en cada rama. **Groovy** añade su propia trampa: `a / b` entre enteros **no** es
división entera —promociona a `BigDecimal`, así que `9 / 3` no da el mismo tipo que en Java—, y por
eso el idioma para este contrato es `intdiv`.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). El CLR lanza `DivideByZeroException` con enteros
y devuelve `Infinity` con `double`, igual que la JVM.

### F\#

```fsharp
let v = stdin.ReadLine().Trim().Split(' ') |> Array.map int

let salida =
    try
        sprintf "resultado=%d" (v.[0] / v.[1])
    with :? System.DivideByZeroException ->
        "error=division por cero"

printfn "%s" salida
```

### VB.NET

```vbnet
Module Division
    Sub Main()
        Dim v = Console.ReadLine().Trim().Split(" "c)
        Dim a = Integer.Parse(v(0))
        Dim b = Integer.Parse(v(1))
        Try
            ' El operador \ es la división entera; / daría un Double.
            Console.WriteLine("resultado=" & (a \ b))
        Catch ex As DivideByZeroException
            Console.WriteLine("error=division por cero")
        Finally
            ' Finally se ejecuta siempre, haya o no excepción.
        End Try
    End Sub
End Module
```

**Qué reconocer:** **VB.NET** es C# con palabras en vez de llaves —`Try` / `Catch` / `Finally`, y un
`When` opcional para filtrar—, y conserva el detalle de tener **dos operadores de división**: `\`
para enteros y `/` para coma flotante, con lo que el error depende de cuál escribas. **F#** vuelve a
convertir el manejo en una expresión con `try ... with`, y el `:?` es su prueba de tipo dinámica. Una
diferencia que no se ve aquí pero conviene saber: en F#, `try ... with` y `try ... finally` son
construcciones **separadas**, no se combinan en un solo bloque como en C#.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). C no tiene excepciones y dividir enteros por cero es
**comportamiento indefinido**: en x86 el procesador levanta una trampa y el proceso muere.

### C++

```cpp
#include <iostream>
#include <stdexcept>

int main() {
    long a, b;
    std::cin >> a >> b;
    try {
        // C++ SÍ tiene excepciones, pero la división entera por cero sigue siendo
        // comportamiento indefinido: no lanza nada. Hay que comprobar y lanzar.
        if (b == 0) throw std::domain_error("division por cero");
        std::cout << "resultado=" << a / b << '\n';
    } catch (const std::domain_error&) {
        std::cout << "error=division por cero\n";
    }
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        long a, b;
        if (scanf("%ld %ld", &a, &b) != 2) return 1;
        @try {
            if (b == 0) {
                @throw [NSException exceptionWithName:@"DivisionPorCero"
                                               reason:@"el divisor es 0"
                                             userInfo:nil];
            }
            printf("resultado=%ld\n", a / b);
        } @catch (NSException *e) {
            printf("error=division por cero\n");
        } @finally {
            fflush(stdout);
        }
    }
    return 0;
}
```

**Qué reconocer:** los dos añaden excepciones a C, y en los dos la excepción **no aparece sola**: la
división sigue siendo la operación cruda del procesador, así que el `throw` es tuyo. La diferencia de
cultura es enorme. En **C++** las excepciones son el mecanismo normal de error y se apoyan en RAII —al
propagarse se ejecutan los destructores de todo lo que quedaba vivo—. En **Objective-C**, `@throw` está
reservado a errores de programación irrecuperables; lo idiomático para un error esperado es devolver
`BOOL` y rellenar un `NSError **`, es decir, exactamente el patrón de la clase 072.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Ninguno de los dos usa
excepciones para errores esperados: Go comprueba antes de dividir y Rust ofrece `checked_div`.

### Zig

```zig
const std = @import("std");

const DivError = error{DivisionPorCero};

fn dividir(a: i64, b: i64) DivError!i64 {
    if (b == 0) return error.DivisionPorCero;
    return @divTrunc(a, b);
}

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, linea, " \r"), ' ');
    const a = try std.fmt.parseInt(i64, it.next().?, 10);
    const b = try std.fmt.parseInt(i64, it.next().?, 10);

    const w = std.io.getStdOut().writer();
    // Zig no tiene excepciones: el error viaja en el tipo de retorno (i64!error).
    if (dividir(a, b)) |r| {
        try w.print("resultado={d}\n", .{r});
    } else |_| {
        try w.print("error=division por cero\n", .{});
    }
}
```

### Nim

```nim
import std/[strutils, sequtils]

let v = stdin.readLine().splitWhitespace().map(parseInt)
try:
  echo "resultado=", v[0] div v[1]
except DivByZeroDefect:
  # Es un Defect, no un Error: compilado con --panics:on el programa aborta
  # sin pasar por este except. Nim distingue "bug" de "condición esperada".
  echo "error=division por cero"
```

### D

```d
import std.stdio, std.string, std.array, std.conv, std.algorithm;

class DivisionPorCero : Exception {
    this() { super("division por cero"); }
}

void main() {
    auto v = readln().split().map!(to!long).array;
    try {
        // En D la división entera por cero produce un Error del hardware, no una
        // Exception recuperable: se comprueba antes y se lanza una excepción propia.
        if (v[1] == 0) throw new DivisionPorCero();
        writefln("resultado=%d", v[0] / v[1]);
    } catch (DivisionPorCero) {
        writeln("error=division por cero");
    }
}
```

**Qué reconocer:** aquí la familia se parte en dos. **Zig no tiene excepciones en absoluto**: no hay
`try`/`catch` con desenrollado de pila, sino un tipo de retorno `!i64` que obliga a la persona que
llama a mirar el error —el `if (expr) |valor| ... else |err| ...` es la forma de abrirlo—. **Nim** y
**D** sí tienen excepciones, pero ambos las dividen en dos categorías: en Nim, `Defect` (bug del
programa, puede no ser atrapable) frente a `CatchableError` (condición esperada); en D, `Error`
frente a `Exception`, con la regla de que un `Error` no se atrapa porque el programa ya está roto. La
división por cero cae del lado "bug" en los dos, y por eso el código la comprueba antes.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). SQL no atrapa nada: distingue el caso con un
`CASE WHEN` antes de que el error pueda ocurrir.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", [SA, SB]),
    number_string(A, SA),
    number_string(B, SB),
    catch(
        ( R is A // B, format("resultado=~d~n", [R]) ),
        error(evaluation_error(zero_divisor), _),
        format("error=division por cero~n", [])
    ).
```

### Datalog

```datalog
// Datalog no tiene excepciones ni E/S: una regla cuyo cuerpo no se cumple
// simplemente no deriva nada. El "error" se modela como otra relación.
.decl par(a: number, b: number)
.decl resultado(v: number)
.decl error_division()

par(10, 2).
par(7, 0).

resultado(a / b) :- par(a, b), b != 0.
error_division() :- par(_, 0).

.output resultado
.output error_division
```

**Qué reconocer:** **Prolog** sí lanza —`X is 10 // 0` produce
`error(evaluation_error(zero_divisor), _)`— y su `catch/3` recibe **tres argumentos**: la meta, el
patrón de error que se quiere atrapar y la meta de recuperación. Que el patrón sea un término
unificable, y no una jerarquía de clases, es la diferencia de fondo con Java o C#: filtras por forma,
no por herencia. **Datalog** no tiene ningún mecanismo de error porque no tiene fallo: una regla que
no aplica no deriva hechos, y punto. Modelar el error como una relación aparte es la única salida, y
es precisamente lo que hace el `CASE WHEN` de SQL en la clase.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y tres capas de diferencia apiladas. Primero, **si la operación
falla siquiera**: en JavaScript, ActionScript y R no falla. Segundo, **si el lenguaje tiene
excepciones**: Zig y Datalog no las tienen, Lua y Tcl las convierten en un valor de retorno. Tercero,
**si el manejo es instrucción o expresión**: Scala, F# y Clojure devuelven un valor donde Java y C
ejecutan un efecto. Aplanar esas tres capas en "todos tienen try/catch" sería mentir.

⏮️ [Volver a la clase 071](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
