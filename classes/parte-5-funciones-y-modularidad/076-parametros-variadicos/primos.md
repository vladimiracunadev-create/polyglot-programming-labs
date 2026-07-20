# 🧬 El mismo programa en las familias de lenguajes — Clase 076

> [⬅️ Volver a la clase 076](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —sumar una cantidad de enteros que no se conoce al
escribir la función— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): enteros separados por espacio
- **Salida** (stdout): `suma=<suma de todos>`
- **Regla:** `suma(...nums) = Σ nums`

| stdin | esperado |
|---|---|
| `1 2 3` | `suma=6` |
| `5` | `suma=5` |
| `10 20 30 40` | `suma=100` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
El paquete de argumentos sobrantes se convierte en una colección normal dentro del cuerpo, y en la
llamada hace falta el gesto inverso: **desparramar** una lista en argumentos sueltos.

### Ruby

```ruby
def suma(*nums)
  nums.sum
end

nums = STDIN.read.split.map(&:to_i)
puts "suma=#{suma(*nums)}"
```

### Perl

```perl
sub suma {
    my $total = 0;
    $total += $_ for @_;   # toda función de Perl es variádica: @_ lo recibe todo
    return $total;
}

my @nums = split ' ', <STDIN>;
printf "suma=%d\n", suma(@nums);
```

### Lua

```lua
local function suma(...)
  local total = 0
  for _, n in ipairs({ ... }) do total = total + n end
  return total
end

local nums = {}
for s in io.read("l"):gmatch("%S+") do nums[#nums + 1] = tonumber(s) end
print("suma=" .. suma(table.unpack(nums)))
```

### Tcl

```tcl
proc suma {args} {
    set total 0
    foreach n $args { incr total $n }
    return $total
}

gets stdin linea
puts "suma=[suma {*}[regexp -all -inline {\S+} $linea]]"
```

### R

```r
suma <- function(...) sum(...)

v <- scan("stdin", what = integer(), quiet = TRUE)
cat(sprintf("suma=%d\n", do.call(suma, as.list(v))))
```

**Qué reconocer:** cinco marcas distintas para la misma idea: `*nums` en Ruby (igual que Python),
`...` en Lua y R, `args` sin ningún símbolo en Tcl —un nombre de parámetro mágico, no sintaxis—, y en
Perl **nada**, porque `@_` ya contenía todo desde siempre y lo variádico no es una función especial
sino el caso normal. Fíjate también en el lado de la llamada, donde cada familia tiene su operador de
desparrame: `*nums` en Ruby, `table.unpack` en Lua, `{*}` en Tcl, `do.call` en R. Perl no necesita
ninguno: `suma(@nums)` aplana el array automáticamente, que es la misma razón por la que en Perl
cuesta pasar dos listas a una función.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

// Dart NO tiene parámetros variádicos: se recibe una lista explícita.
int suma(List<int> nums) => nums.fold(0, (a, b) => a + b);

void main() {
  final nums = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  print('suma=${suma(nums)}');
}
```

### ActionScript 3

```actionscript
// ActionScript 3 sí es variádico con `...`, pero no tiene stdin: se ilustra la firma.
package {
    public class Calculo {
        public static function suma(...nums):int {
            var total:int = 0;
            for each (var n:int in nums) total += n;
            return total;
        }
        // Llamada: Calculo.suma(1, 2, 3) devuelve 6.
    }
}
```

**Qué reconocer:** ActionScript escribe `...nums` igual que JavaScript moderno y TypeScript, y por el
mismo motivo: los tres vienen del borrador de ECMAScript 4, donde el viejo objeto `arguments` se
sustituyó por un parámetro rest de verdad. Dart es la excepción de la familia y lo es a propósito:
prefirió que el número de argumentos sea siempre visible en la firma, así que quien quiera cantidad
variable pasa una `List` y el punto de llamada lleva corchetes.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). En la JVM lo variádico **es un array**: el
compilador lo empaqueta en la llamada y dentro del método `nums` es un `int[]` corriente.

### Kotlin

```kotlin
fun suma(vararg nums: Int): Int = nums.sum()

fun main() {
    val nums = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }.toIntArray()
    println("suma=${suma(*nums)}")
}
```

### Scala

```scala
object Calculo {
  def suma(nums: Int*): Int = nums.sum

  def main(args: Array[String]): Unit = {
    val nums = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
    println(s"suma=${suma(nums: _*)}")
  }
}
```

### Groovy

```groovy
int suma(int... nums) {
    int total = 0
    for (n in nums) total += n
    return total
}

def nums = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger() as int[]
println "suma=${suma(nums)}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(defn suma [& nums] (reduce + 0 nums))

(let [nums (map parse-long (str/split (str/trim (read-line)) #"\s+"))]
  (println (str "suma=" (apply suma nums))))
```

**Qué reconocer:** Groovy usa los tres puntos de Java sin cambios; Kotlin lo escribe con la palabra
`vararg` y Scala con un asterisco detrás del tipo (`Int*`). La diferencia útil está en la **llamada
con una colección ya hecha**: Java y Groovy pasan el array tal cual, Kotlin exige el operador de
desparrame `*nums`, y Scala escribe la anotación `nums: _*` que le dice al compilador "esto no es un
argumento, es el paquete entero". Clojure no tiene arrays variádicos: `& nums` liga una **secuencia
perezosa**, y `apply` es el desparrame, que existe como función normal y no como sintaxis.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
open System

// En F# lo variádico solo existe como `ParamArray` en miembros de tipo;
// en funciones `let` lo idiomático es recibir una lista.
type Calculo =
    static member Suma([<ParamArray>] nums: int[]) = Array.sum nums

[<EntryPoint>]
let main _ =
    let nums = Console.ReadLine().Trim().Split(' ') |> Array.map int
    printfn "suma=%d" (Calculo.Suma(nums))
    0
```

### VB.NET

```vbnet
Module Programa
    Function Suma(ParamArray nums As Integer()) As Integer
        Dim total = 0
        For Each n In nums
            total += n
        Next
        Return total
    End Function

    Sub Main()
        Dim p = Console.ReadLine().Trim().Split(" "c)
        Dim nums = Array.ConvertAll(p, AddressOf Integer.Parse)
        Console.WriteLine("suma=" & Suma(nums))
    End Sub
End Module
```

**Qué reconocer:** los tres lenguajes del CLR comparten el mismo mecanismo con tres nombres: `params`
en C#, `ParamArray` en VB.NET y el atributo `[<ParamArray>]` en F#. No es casualidad —es un atributo
de metadatos del propio CLR, así que un método variádico escrito en VB.NET se llama como variádico
desde C#—. F# vuelve a marcar la frontera entre función y miembro: `let suma nums = ...` recibiría una
lista y punto; el paquete variádico solo aparece cuando se escribe un método de un tipo, para poder
interoperar con el resto de .NET.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). El `stdarg.h` de C es el variádico más peligroso de
esta página: la función no sabe cuántos argumentos recibió ni de qué tipo son.

### C++

```cpp
#include <iostream>
#include <numeric>
#include <vector>

// Variádico de plantilla: el paquete se expande en COMPILACIÓN (expresión de plegado).
template <typename... T>
long suma(T... nums) {
    return (static_cast<long>(nums) + ... + 0L);
}

int main() {
    // La cantidad de datos de stdin solo se conoce en ejecución: ahí toca un vector.
    std::vector<long> v;
    for (long x; std::cin >> x;) v.push_back(x);
    std::cout << "suma=" << std::accumulate(v.begin(), v.end(), 0L) << '\n';

    (void)suma(1, 2, 3);  // 6, con el paquete conocido al compilar
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

@interface Calculadora : NSObject
+ (long)sumaDe:(NSNumber *)primero, ... NS_REQUIRES_NIL_TERMINATION;
@end

@implementation Calculadora
+ (long)sumaDe:(NSNumber *)primero, ... {
    long total = 0;
    va_list args;
    va_start(args, primero);
    for (NSNumber *n = primero; n != nil; n = va_arg(args, NSNumber *)) {
        total += n.longValue;
    }
    va_end(args);
    return total;
}
@end

int main(void) {
    @autoreleasepool {
        // El variádico de Objective-C es el de C: exige un centinela `nil` para saber dónde acaba.
        long total = 0, x;
        while (scanf("%ld", &x) == 1) total += x;
        printf("suma=%ld\n", total);

        (void)[Calculadora sumaDe:@1, @2, @3, nil];  // 6, por la vía variádica
    }
    return 0;
}
```

**Qué reconocer:** C++ y Objective-C heredan el mismo `stdarg.h`, y cada uno se aleja de él por un
lado distinto. C++ añade los **paquetes de plantilla**, que son variádicos de compilación: se conocen
los tipos, el compilador genera una función por combinación y `(nums + ... + 0)` se expande a una
suma literal — pero por eso mismo **no** pueden recibir una cantidad decidida en ejecución, y la
lectura de stdin acaba en un `vector`. Objective-C se queda con el variádico de C y por eso necesita
el centinela `nil`: sin él la función no tiene forma de saber cuándo parar, que es exactamente la
razón por la que `NSArray arrayWithObjects:` termina siempre en `nil`.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Go tiene `nums ...int`
con su desparrame `nums...`; Rust **no tiene** variádicos y pasa un slice.

### Zig

```zig
const std = @import("std");

// Zig eliminó los variádicos de ejecución: el "paquete" es una tupla de comptime.
fn suma(nums: anytype) i64 {
    var total: i64 = 0;
    inline for (nums) |n| total += n;
    return total;
}

pub fn main() !void {
    var buf: [256]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \r");
    var total: i64 = 0;  // la cantidad de datos es de ejecución: se itera
    while (it.next()) |t| total += try std.fmt.parseInt(i64, t, 10);
    try std.io.getStdOut().writer().print("suma={d}\n", .{total});

    _ = suma(.{ 1, 2, 3 });  // 6, con la tupla conocida al compilar
}
```

### Nim

```nim
import std/strutils, std/sequtils

proc suma(nums: varargs[int]): int =
  for n in nums: result += n

let nums = stdin.readLine().splitWhitespace().map(parseInt)
echo "suma=", suma(nums)
```

### D

```d
import std.stdio, std.array, std.string, std.conv, std.algorithm;

// Variádico con seguridad de tipos: `long[] nums...` acepta tanto
// suma(1, 2, 3) como pasarle un array ya construido.
long suma(long[] nums...) {
    return nums.sum();
}

void main() {
    auto nums = readln().strip().split().map!(to!long).array;
    writefln("suma=%d", suma(nums));
}
```

**Qué reconocer:** Nim y D tienen variádicos con tipo (`varargs[int]`, `long[] nums...`) que aceptan
indistintamente argumentos sueltos o una colección ya hecha —sin operador de desparrame, a diferencia
de Go—, y dentro del cuerpo se comportan como un array. Zig es el más radical de toda la página:
**quitó** los variádicos de ejecución que heredaba de C precisamente porque ocultan tipos y tamaños,
y dejó solo el paquete `comptime` (`anytype` + `inline for`). Ese es el mecanismo detrás de
`print("{d}\n", .{x})`, donde el `.{...}` no es magia del formato sino una tupla anónima.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). `SUM()` sobre una columna es la respuesta
declarativa a "una cantidad desconocida de valores".

### Prolog

```prolog
:- initialization(main, main).

% Prolog no tiene variádicos: la aridad es parte del nombre del predicado,
% así que lo variable viaja dentro de UNA lista y suma/2 recorre esa lista.
suma([], 0).
suma([N|Resto], Total) :-
    suma(Resto, Parcial),
    Total is Parcial + N.

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes),
    exclude(==(""), Partes, Limpios),
    maplist([S, N]>>number_string(N, S), Limpios, Nums),
    suma(Nums, Total),
    format("suma=~d~n", [Total]).
```

### Datalog

```datalog
% Datalog puro no tiene variádicos, ni agregación, ni E/S: la aridad de cada
% predicado es fija y conocida. Los datos entran como hechos, uno por valor.
num(1, 1).
num(2, 2).
num(3, 3).

% Con la extensión de agregados (Soufflé, DLV) sí se puede totalizar:
% total(S) :- S = sum X : { num(_, X) }.
```

**Qué reconocer:** aquí la aridad es innegociable. `suma/2` no puede recibir "los que hagan falta"
porque `suma/2` y `suma/3` serían predicados distintos, sin ninguna relación entre ellos; lo variable
tiene que caber en un solo argumento, y por eso viaja en una lista que se recorre por recursión sobre
`[Cabeza|Resto]`. Datalog renuncia incluso a la recursión aritmética y necesita una extensión de
agregados para llegar a lo que SQL hace con `SUM(...)`: en ambos, "una cantidad desconocida de
valores" no es un problema de la firma de una función, sino una **columna con muchas filas**.

---

## Y de vuelta a la clase

Veinte lenguajes y una pregunta doble: quién empaqueta y quién desparrama. Casi todos convierten el
paquete en una colección normal dentro del cuerpo (array, lista, secuencia, tupla) y la diferencia
real está en el punto de llamada —`*`, `...`, `{*}`, `apply`, `: _*` o nada—. Y hay dos rebeldes que
merecen recordarse: Zig y C++, donde lo variádico ocurre **al compilar** y no puede depender de un
dato de ejecución; y Prolog, donde la aridad es tan parte del nombre que lo variable no cabe en la
firma. Eso es lo transferible.

⏮️ [Volver a la clase 076](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
