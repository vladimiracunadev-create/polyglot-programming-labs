# 🧬 El mismo programa en las familias de lenguajes — Clase 083

> [⬅️ Volver a la clase 083](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —una función que devuelve otra función que recuerda
un valor base— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

El cierre es donde más se nota la personalidad de cada lenguaje: no cambia *si* se captura, cambia
**qué** se captura —el valor o la variable— y cuánto hay que escribir para decirlo.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `base`
- **Salida** (stdout): `r1=<base+1> r2=<base+2>`
- **Regla:** `sumar = λx. base + x`; luego `r1 = sumar(1)` y `r2 = sumar(2)`

| stdin | esperado |
|---|---|
| `10` | `r1=11 r2=12` |
| `0` | `r1=1 r2=2` |
| `100` | `r1=101 r2=102` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Funciones anónimas baratas y captura automática del entorno léxico… casi siempre.

### Ruby

```ruby
base = STDIN.gets.to_i
sumar = ->(x) { base + x }   # lambda: aridad estricta y 'return' propio
puts "r1=#{sumar.call(1)} r2=#{sumar.(2)}"
```

### Perl

```perl
my $base = <STDIN>;
chomp $base;
my $sumar = sub { return $base + $_[0] };  # cierre sobre la léxica 'my $base'
printf "r1=%d r2=%d\n", $sumar->(1), $sumar->(2);
```

### Lua

```lua
local function hacer_sumador(b)
  return function(x) return b + x end   -- 'b' pasa a ser un upvalue del cierre
end

local base = io.read("n")
local sumar = hacer_sumador(base)
print(string.format("r1=%d r2=%d", sumar(1), sumar(2)))
```

### Tcl

```tcl
# Tcl no captura el entorno léxico: 'apply' recibe el valor ligado como argumento.
gets stdin base
set sumar [list apply {{b x} {expr {$b + $x}}} $base]
puts "r1=[{*}$sumar 1] r2=[{*}$sumar 2]"
```

### R

```r
hacer_sumador <- function(b) {
  force(b)                    # vence la evaluación perezosa: fija el valor ahora
  function(x) b + x
}

base <- as.integer(readLines("stdin", n = 1))
sumar <- hacer_sumador(base)
cat(sprintf("r1=%d r2=%d\n", sumar(1L), sumar(2L)))
```

**Qué reconocer:** Ruby es el que más vocabulario tiene: un **block** es un argumento implícito que
no es un objeto, un **proc** es un block cosificado con aridad laxa y `return` que sale del método
que lo creó, y una **lambda** es estricta con la aridad y devuelve solo de sí misma —tres cosas
parecidas con semánticas distintas—. Perl captura las **léxicas declaradas con `my`** y solo esas:
una `our` global no se congela en el cierre. Lua nombra explícitamente lo capturado, los
**upvalues**, y los comparte entre cierres creados en el mismo alcance. R esconde una trampa propia:
por su evaluación perezosa, sin `force(b)` el valor se resolvería al llamar y no al crear. Tcl es el
único que **no tiene cierres**: hay que empaquetar el valor a mano con `apply`.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

int Function(int) hacerSumador(int b) => (x) => b + x; // captura léxica

void main() {
  final base = int.parse(stdin.readLineSync()!.trim());
  final sumar = hacerSumador(base);
  print('r1=${sumar(1)} r2=${sumar(2)}');
}
```

### ActionScript 3

```actionscript
// Sin stdin en el reproductor Flash; el cierre sí es exactamente el de JavaScript.
package {
    public class Cierres {
        public static function hacerSumador(base:int):Function {
            return function(x:int):int { return base + x; }; // captura 'base'
        }
    }
}
```

**Qué reconocer:** la familia entera hereda el cierre de Scheme vía JavaScript, y por eso el gesto
es idéntico en los cuatro: una función devuelta que sigue viendo la variable de quien la creó. La
captura es **de la variable, no del valor**, y de ahí nace el error clásico de capturar el
contador de un bucle `var` y verlo terminado en todas las iteraciones. Dart evita ese caso porque
cada vuelta de su `for` crea un enlace nuevo, igual que `let` en JavaScript moderno. ActionScript 3
conserva la trampa completa: es ECMAScript 4, la misma máquina.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Aquí la diferencia entre primos es real y
visible, porque Java impone una restricción que los demás no.

### Kotlin

```kotlin
fun hacerSumador(base: Int): (Int) -> Int = { x -> base + x }

fun main() {
    val base = readLine()!!.trim().toInt()
    val sumar = hacerSumador(base)
    println("r1=${sumar(1)} r2=${sumar(2)}")
}
```

### Scala

```scala
object Cierres extends App {
  val base = scala.io.StdIn.readLine().trim.toInt
  val sumar: Int => Int = x => base + x
  println(s"r1=${sumar(1)} r2=${sumar(2)}")
}
```

### Groovy

```groovy
def base = System.in.newReader().readLine().trim() as int
def sumar = { x -> base + x }   // el cierre guarda 'owner' y 'delegate', no solo el valor
println "r1=${sumar(1)} r2=${sumar(2)}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(defn hacer-sumador [base]
  (fn [x] (+ base x)))     ; captura un valor inmutable, no una variable

(let [base (Integer/parseInt (str/trim (read-line)))
      sumar (hacer-sumador base)]
  (println (str "r1=" (sumar 1) " r2=" (sumar 2))))
```

**Qué reconocer:** **Java exige que la variable capturada sea `final` o efectivamente final**: la
lambda copia el valor en un campo sintético y por eso el compilador prohíbe modificarla después
—una restricción que se ve en la implementación de la clase—. **Kotlin no la tiene**: puede capturar
un `var` y modificarlo desde dentro, porque lo envuelve en un objeto `Ref` en el montón. **Groovy**
va aún más lejos: su `Closure` es un objeto con `owner`, `thisObject` y `delegate`, y ese
`delegate` reconfigurable es lo que hace posibles los DSL de Gradle. **Scala** captura como Java
pero su `val` por defecto hace que la restricción casi nunca se note. **Clojure** cambia el
problema: captura **valores inmutables, nunca variables**, así que la pregunta "¿y si cambia
después?" no puede plantearse; para estado mutable hace falta un `atom` explícito.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let hacerSumador b = fun x -> b + x   // aplicación parcial: 'hacerSumador b' ya es la función

let b = int (stdin.ReadLine().Trim())
let sumar = hacerSumador b
printfn "r1=%d r2=%d" (sumar 1) (sumar 2)
```

### VB.NET

```vbnet
Module Cierres
    Function HacerSumador(valorBase As Integer) As Func(Of Integer, Integer)
        Return Function(x) valorBase + x   ' captura la variable, no una copia
    End Function

    Sub Main()
        Dim b As Integer = Integer.Parse(Console.ReadLine().Trim())
        Dim sumar = HacerSumador(b)
        Console.WriteLine("r1=" & sumar(1) & " r2=" & sumar(2))
    End Sub
End Module
```

**Qué reconocer:** el CLR captura **por referencia a la variable**, no por valor: el compilador crea
una clase oculta con la variable como campo y la comparte entre el cierre y el código que lo creó,
justo lo contrario de la copia que hace Java. Eso permite que un cierre de VB.NET o C# modifique la
variable capturada y que el cambio se vea fuera. F# lo hace innecesario: sus enlaces son inmutables
por defecto y la **currificación** es nativa —`hacerSumador b` devuelve una función sin escribir
`fun` ni `return`—, que es la misma idea que la aplicación parcial de Prolog más abajo.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). C **no tiene cierres**: sus primos tuvieron que
inventárselos, y cada uno lo hizo distinto.

### C++

```cpp
#include <iostream>
#include <functional>

std::function<int(int)> hacer_sumador(int base) {
    return [base](int x) { return base + x; }; // [base] = captura por COPIA
    // Con [&base] capturaría por referencia y devolvería un puntero colgante.
}

int main() {
    int base;
    std::cin >> base;
    auto sumar = hacer_sumador(base);
    std::cout << "r1=" << sumar(1) << " r2=" << sumar(2) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

typedef int (^Sumador)(int);

int main(void) {
    @autoreleasepool {
        int base;
        scanf("%d", &base);
        // Un bloque captura por copia; con __block la variable sería compartida.
        Sumador sumar = ^(int x) { return base + x; };
        printf("r1=%d r2=%d\n", sumar(1), sumar(2));
    }
    return 0;
}
```

**Qué reconocer:** los dos hacen **explícita** la decisión que los demás toman por ti. En C++ la
lista de captura lo dice todo: `[base]` copia, `[&base]` toma referencia —y devolver ese cierre deja
un puntero colgante, un error que ningún recolector te va a perdonar—. Objective-C usa `^` para sus
**bloques**, que copian por defecto y necesitan `__block` para compartir la variable, además de
`Block_copy` para sobrevivir al alcance donde nacieron. Es la misma pregunta que Rust responde con
`move` y `Fn`/`FnMut`/`FnOnce`: quién es dueño de lo capturado y cuánto vive.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Donde no hay recolector,
capturar significa decidir dónde vive el estado capturado.

### Zig

```zig
const std = @import("std");

// Zig NO tiene cierres: el estado capturado se declara a mano en una estructura.
const Sumador = struct {
    base: i64,
    fn llamar(self: Sumador, x: i64) i64 {
        return self.base + x;
    }
};

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const base = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r\n"), 10);
    const sumar = Sumador{ .base = base };
    try std.io.getStdOut().writer().print(
        "r1={d} r2={d}\n",
        .{ sumar.llamar(1), sumar.llamar(2) },
    );
}
```

### Nim

```nim
import std/strutils

proc hacerSumador(base: int): proc (x: int): int =
  result = proc (x: int): int = base + x   # el entorno capturado va al montón

let base = stdin.readLine().strip().parseInt()
let sumar = hacerSumador(base)
echo "r1=", sumar(1), " r2=", sumar(2)
```

### D

```d
import std.stdio, std.string, std.conv;

int delegate(int) hacerSumador(int base) {
    return (int x) => base + x;   // 'delegate' = puntero a función + puntero al contexto
}

void main() {
    const base = readln().strip().to!int;
    auto sumar = hacerSumador(base);
    writefln("r1=%d r2=%d", sumar(1), sumar(2));
}
```

**Qué reconocer:** **Zig no tiene cierres en absoluto** y es coherente con su lema de "ninguna
asignación de memoria oculta": si el estado capturado tiene que sobrevivir a la función, tú declaras
la estructura y tú decides dónde guardarla. Nim y D sí los tienen y ambos delatan el coste en el
tipo: D distingue `function` (solo puntero, sin contexto) de **`delegate`** (puntero + contexto), y
Nim mueve el entorno capturado al montón salvo que el cierre no escape. Rust hace la misma
contabilidad con `move` y los tres rasgos `Fn`, y Go la esconde tras el análisis de escape del
compilador. Ninguno regala el cierre: solo cambia quién paga y si te lo cuenta.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Sin funciones de primera clase, la captura se
convierte en otra cosa.

### Prolog

```prolog
:- initialization(main, main).

sumar(Base, X, R) :- R is Base + X.

main :-
    read_line_to_string(user_input, Linea),
    number_string(Base, Linea),
    Sumar = sumar(Base),        % aplicación parcial: el término lleva Base dentro
    call(Sumar, 1, R1),         % call/3 completa los argumentos que faltaban
    call(Sumar, 2, R2),
    format("r1=~d r2=~d~n", [R1, R2]).
```

### Datalog

```datalog
% Datalog no tiene funciones de primera clase ni cierres: la "captura" consiste
% en ligar la base dentro de la propia regla, y la regla no es un valor.
base(10).

r1(R) :- base(B), R = B + 1.
r2(R) :- base(B), R = B + 2.
```

**Qué reconocer:** Prolog se acerca sorprendentemente al cierre sin tenerlo: `sumar(Base)` es un
**término parcialmente aplicado** que `call/N` completa después, y ese término lleva el valor dentro
igual que un cierre lleva su entorno. La diferencia es que `Base` **está ligada de una vez y para
siempre**: no existe la duda de si el cierre ve el valor o la variable, porque la variable no puede
cambiar. Datalog ni siquiera llega ahí —una regla no es un valor que se pueda pasar—, y como SQL,
sustituye la función por una relación con un parámetro más.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una pregunta que los separa a todos: **¿el cierre se lleva el
valor o la variable?** Java copia y por eso exige `final`; .NET comparte la variable; C++ y
Objective-C te obligan a elegir por escrito; Clojure elimina la pregunta haciendo inmutable todo; y
Zig, Tcl y Datalog contestan que no hay cierre que valga.

⏮️ [Volver a la clase 083](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
