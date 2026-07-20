# 🧬 El mismo programa en las familias de lenguajes — Clase 082

> [⬅️ Volver a la clase 082](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —una variable interna que oculta a la externa dentro
de su bloque— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no
solo por los diez lenguajes del núcleo.

Es una clase donde los primos **no coinciden**: unos permiten el sombreado, otros lo prohíben con un
error de compilación, y otros ni siquiera tienen alcance de bloque en el que sombrear.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`
- **Salida** (stdout): `interno=<n+10> externo=<n>`
- **Regla:** `x = n` en el exterior; en un bloque interno `x = n + 10`; al salir, `x` vuelve a `n`

| stdin | esperado |
|---|---|
| `5` | `interno=15 externo=5` |
| `0` | `interno=10 externo=0` |
| `-3` | `interno=7 externo=-3` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La familia donde el alcance suele ser **de función**, no de bloque: un `if` o un `while` no crean un
espacio de nombres nuevo.

### Ruby

```ruby
n = STDIN.gets.to_i
x = n
[1].each do |_; x|        # el `; x` declara una x local al bloque: sombrea a la externa
  x = n + 10
  print "interno=#{x} "
end
puts "externo=#{x}"
```

### Perl

```perl
my $n = <STDIN>;
chomp $n;
my $x = $n;
{
    my $x = $n + 10;      # 'my' dentro del bloque crea una léxica nueva
    print "interno=$x ";
}
print "externo=$x\n";
```

### Lua

```lua
local n = io.read("n")
local x = n
do
  local x = n + 10        -- nuevo 'local': sombrea, no reasigna
  io.write(string.format("interno=%d ", x))
end
print(string.format("externo=%d", x))
```

### Tcl

```tcl
# Tcl no tiene alcance de bloque: el único alcance nuevo lo crea un 'proc'.
gets stdin n

proc interno {n} {
    set x [expr {$n + 10}]   ;# x es local al proc y no toca la del llamador
    return $x
}

set x $n
puts "interno=[interno $n] externo=$x"
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))
x <- n
local({
  x <- n + 10             # 'local' crea un entorno nuevo: sombrea sin tocar la externa
  cat(sprintf("interno=%d ", x))
})
cat(sprintf("externo=%d\n", x))
```

**Qué reconocer:** aquí se ve que "alcance de bloque" no es universal dentro de la misma familia.
Perl y Lua sí lo tienen, y `my` / `local` son la marca explícita de *nueva variable*, no de
asignación —esa palabra es la que decide si sombreas o pisas—. Ruby, como Python, no crea alcance
con `if` ni `while`: solo los bloques lo crean, y hace falta la sintaxis poco conocida `|; x|` para
declarar una variable local al bloque. Tcl es el extremo opuesto: sin bloques léxicos, el alcance se
fabrica con un `proc`, y hasta ver la global hay que pedirlo con `global` o `upvar`. R sombrea
creando un **entorno** nuevo, que es la misma idea vista desde su modelo de entornos encadenados.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  final x = n;
  {
    final x = n + 10; // bloque anidado: sombrea a la externa
    stdout.write('interno=$x ');
  }
  print('externo=$x');
}
```

### ActionScript 3

```actionscript
// ActionScript 3 no tiene stdin ni alcance de bloque: 'var' se eleva a la función,
// así que para sombrear hay que abrir otra función.
package {
    public class Sombra {
        public static function describir(n:int):String {
            var x:int = n;
            return "interno=" + interno(n) + " externo=" + x;
        }
        private static function interno(n:int):int {
            var x:int = n + 10; // x local a esta función: aquí sí oculta a la otra
            return x;
        }
    }
}
```

**Qué reconocer:** este es el corte histórico exacto de la familia. ActionScript 3 y el JavaScript
anterior a ES6 comparten `var` **con elevación a la función**: escribir `var x` dentro de un `if` no
crea nada nuevo, solo reutiliza la misma ranura, y por eso hay que refactorizar a una función para
conseguir el sombreado. Dart nació después de esa lección y trae alcance de bloque desde el primer
día, igual que `let` y `const` en JavaScript moderno o TypeScript. Reconocer `var` frente a `let` en
esta familia es reconocer de qué década es el código que estás leyendo.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos tienen alcance de bloque, pero difieren
en si te dejan reutilizar un nombre ya ocupado.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toInt()
    val x = n
    run {
        val x = n + 10 // Kotlin lo permite (avisa con "name shadowed")
        print("interno=$x ")
    }
    println("externo=$x")
}
```

### Scala

```scala
object Sombra extends App {
  val n = scala.io.StdIn.readLine().trim.toInt
  val x = n
  {
    val x = n + 10 // bloque anidado: sombreado legal y silencioso
    print(s"interno=$x ")
  }
  println(s"externo=$x")
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim() as int
def x = n
def bloque = {
    def x = n + 10        // el cuerpo del cierre sí crea alcance propio
    print "interno=$x "
}
bloque()
println "externo=$x"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [n (Integer/parseInt (str/trim (read-line)))
      x n]
  (let [x (+ n 10)]        ; un 'let' interno crea un enlace nuevo que oculta al externo
    (print (str "interno=" x " ")))
  (println (str "externo=" x)))
```

**Qué reconocer:** los cuatro compilan al mismo bytecode y aun así no coinciden. **Java prohíbe**
redeclarar una variable local dentro de un bloque anidado del mismo método —por eso la
implementación de la clase usa otro nombre—, mientras que Kotlin, Scala y Groovy sí lo permiten;
Kotlin lo señala con un aviso, Scala ni eso. Clojure cambia el vocabulario: no hay variables que
sombrear, hay **enlaces léxicos**, y un `let` anidado simplemente crea un enlace nuevo que tapa al
anterior mientras dura su forma. Es sombreado en su versión más pura, porque nada se reasigna nunca.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let n = int (stdin.ReadLine().Trim())
let x = n

let interno =
    let x = n + 10   // 'let' anidado: sombreado idiomático y sin aviso
    x

printfn "interno=%d externo=%d" interno x
```

### VB.NET

```vbnet
Module Sombra
    Sub Main()
        Dim n As Integer = Integer.Parse(Console.ReadLine().Trim())
        Dim x As Integer = n
        ' VB.NET rechaza re-declarar 'x' en un bloque anidado
        ' ("hides a variable in an enclosing block"): hay que usar otro nombre.
        Dim xInterno As Integer = n + 10
        Console.WriteLine("interno=" & xInterno & " externo=" & x)
    End Sub
End Module
```

**Qué reconocer:** dos lenguajes sobre el mismo CLR y posturas opuestas. En **F# el sombreado es el
estilo normal**: como los enlaces son inmutables, encadenar `let x = ...` es la forma habitual de
transformar un valor paso a paso sin mutarlo, exactamente el gesto que Rust tomó prestado. **VB.NET
es el más estricto de las veinte**: no solo prohíbe redeclarar en un bloque anidado, sino que
además el alcance de un `Dim` dentro de un `If` se extiende a todo el bloque contenedor. C#, en el
medio, permite bloques anidados pero no sombrear una local del mismo método.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). La familia que **inventó** el alcance de bloque con
llaves, y donde el sombreado es legal desde siempre.

### C++

```cpp
#include <iostream>

int main() {
    int n;
    std::cin >> n;
    const int x = n;
    {
        const int x = n + 10; // sombrea a la externa mientras dure el bloque
        std::cout << "interno=" << x << ' ';
    }
    std::cout << "externo=" << x << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        int n;
        scanf("%d", &n);
        const int x = n;
        {
            const int x = n + 10; // herencia directa de C: bloque anidado, nombre reutilizado
            printf("interno=%d ", x);
        }
        printf("externo=%d\n", x);
    }
    return 0;
}
```

**Qué reconocer:** ambos heredan de C la regla más antigua del asunto: **cada par de llaves abre un
alcance** y un nombre declarado dentro tapa al de fuera hasta la llave de cierre. No hay aviso ni
error porque en C era una característica deseada, no un accidente. Los compiladores modernos sí
ofrecen `-Wshadow`, pero está desactivado por defecto: es la diferencia entre un lenguaje que confía
en el programador y uno que lo verifica. Objective-C, superconjunto de C, no cambia una coma de esta
regla; solo `@autoreleasepool` añade un alcance con semántica extra, la de liberar objetos al salir.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Dos que sombrean con
gusto, frente a primos que lo consideran una fuente de errores.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r\n"), 10);
    const x = n;
    {
        // Zig PROHÍBE el sombreado: escribir 'const x' aquí es error de compilación
        // ("local shadows declaration"). Hay que elegir otro nombre.
        const interno = n + 10;
        try std.io.getStdOut().writer().print("interno={d} ", .{interno});
    }
    try std.io.getStdOut().writer().print("externo={d}\n", .{x});
}
```

### Nim

```nim
import std/strutils

let n = stdin.readLine().strip().parseInt()
let x = n
block:
  let x = n + 10          # 'block' abre alcance nuevo: sombreado permitido
  stdout.write("interno=" & $x & " ")
echo "externo=", x
```

### D

```d
import std.stdio, std.string, std.conv;

void main() {
    const n = readln().strip().to!int;
    const x = n;
    {
        // D también lo prohíbe: declarar 'x' aquí da "shadows another local".
        const interno = n + 10;
        writef("interno=%d ", interno);
    }
    writefln("externo=%d", x);
}
```

**Qué reconocer:** la familia de sistemas es la que más se pelea con esta decisión. **Zig y D lo
prohíben por diseño** —ambos consideran que reutilizar un nombre esconde errores de refactorización,
y el compilador te obliga a inventar `interno`—, justo lo contrario que Rust, donde `let x = ...`
repetido es el idioma recomendado para convertir un valor sin mutarlo. Nim se queda en medio: lo
permite en un `block` nuevo, con un aviso opcional. Que dos lenguajes con objetivos casi idénticos
lleguen a reglas opuestas te dice que el sombreado no es una cuestión técnica sino de **filosofía de
legibilidad**.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Donde no hay asignación, el sombreado cambia de
naturaleza.

### Prolog

```prolog
:- initialization(main, main).

interno(N, X) :- X is N + 10.   % esta X es local a esta cláusula y no existe fuera

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    X = N,                      % se liga una sola vez: no se puede reasignar ni sombrear
    interno(N, XInterno),
    format("interno=~d externo=~d~n", [XInterno, X]).
```

### Datalog

```datalog
% Datalog no tiene bloques ni variables mutables: el alcance de una variable
% es la regla donde aparece, y muere con ella. No hay nada que sombrear.
n(5).

interno(X) :- n(N), X = N + 10.
externo(X) :- n(X).
```

**Qué reconocer:** en Prolog y Datalog el alcance de una variable es **la cláusula**, ni más ni
menos: la `X` de `interno/2` y la `X` de `main/0` no se ven ni se estorban aunque se llamen igual,
porque cada cláusula se renombra internamente al ejecutarse. Y como una variable **se liga una sola
vez**, no hay forma de escribir "la misma variable con otro valor dentro de un bloque": lo que en
Ruby sería sombreado, aquí es sencillamente otra variable con otro nombre. Es la misma renuncia que
hace SQL, donde el alias de una subconsulta vive solo dentro de ella.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y tres respuestas distintas: los que sombrean con naturalidad
(Rust, F#, Clojure, Perl, Lua), los que te lo prohíben para protegerte (Zig, D, VB.NET, Java) y los
que no tienen dónde sombrear (Tcl, ActionScript, Prolog, Datalog). La palabra que declara —`my`,
`local`, `let`, `Dim`— es siempre la pista.

⏮️ [Volver a la clase 082](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
