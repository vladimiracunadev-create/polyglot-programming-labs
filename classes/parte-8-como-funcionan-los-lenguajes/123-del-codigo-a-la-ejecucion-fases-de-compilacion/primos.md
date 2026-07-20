# 🧬 El mismo programa en las familias de lenguajes — Clase 123

> [⬅️ Volver a la clase 123](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —evaluar `a op b` recorriendo a mano las fases
léxico → sintaxis → evaluación— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Aquí la comparación tiene un premio extra: el programa simula las fases que **el propio runtime de
cada lenguaje aplicó a este archivo** antes de ejecutarlo. Leer los veinte es ver veinte veces el
mismo circuito, una vez en el código y otra en la máquina que lo corre.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a op b` (dos enteros y un operador `+`, `-`, `*`)
- **Salida** (stdout): `resultado=<a op b>`
- **Regla:** aplicar el operador a los dos operandos

| stdin | esperado |
|---|---|
| `3 + 4` | `resultado=7` |
| `10 - 2` | `resultado=8` |
| `5 * 6` | `resultado=30` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Ninguno de estos lenguajes ejecuta el texto fuente directamente: todos lo analizan y lo traducen a
una forma interna antes de dar el primer paso. Nuestro programa hace lo mismo en miniatura.

### Ruby

```ruby
tokens = STDIN.gets.split                 # fase léxica: texto -> tokens
izq, op, der = tokens                     # fase sintáctica: la forma es a-op-b
r = izq.to_i.send(op, der.to_i)           # fase de evaluación
puts "resultado=#{r}"

# Ruby sí deja observar su propia fase desde el programa:
#   puts RubyVM::InstructionSequence.compile("1 + 2").disasm
```

### Perl

```perl
my ($izq, $op, $der) = split ' ', <STDIN>;   # fase léxica y sintáctica
my %tabla = (
    '+' => sub { $_[0] + $_[1] },
    '-' => sub { $_[0] - $_[1] },
    '*' => sub { $_[0] * $_[1] },
);
printf "resultado=%d\n", $tabla{$op}->($izq, $der);   # fase de evaluación

# Perl no expone su optree al propio programa; se mira desde fuera:
#   perl -MO=Concise main.pl
```

### Lua

```lua
local izq, op, der = io.read("l"):match("^%s*(%-?%d+)%s+([%+%-%*])%s+(%-?%d+)%s*$")
local tabla = {
  ["+"] = function(x, y) return x + y end,
  ["-"] = function(x, y) return x - y end,
  ["*"] = function(x, y) return x * y end,
}
print("resultado=" .. tabla[op](tonumber(izq), tonumber(der)))

-- string.dump(f) devuelve el bytecode de una función; para leerlo: luac -l main.lua
```

### Tcl

```tcl
gets stdin linea
lassign [split $linea] izq op der
# expr SIN llaves: la expresión se arma como texto y Tcl la compila en cada ejecución.
set r [expr "$izq $op $der"]
puts "resultado=$r"

# Ver el bytecode desde el propio programa:
#   puts [::tcl::unsupported::disassemble script {expr {1 + 2}}]
```

### R

```r
tokens <- scan("stdin", what = "", n = 3, quiet = TRUE)   # fase léxica
arbol <- parse(text = paste(tokens, collapse = " "))[[1]] # fase sintáctica: R devuelve el AST
cat(sprintf("resultado=%d\n", as.integer(eval(arbol))))   # fase de evaluación
```

**Qué reconocer:** los cinco hacen a mano lo que su runtime ya hizo con este mismo archivo. Ruby,
Perl y Lua resuelven el operador buscándolo en una **tabla**, que es exactamente lo que hace un
despachador de instrucciones: el token deja de ser texto y pasa a ser un índice. R y Tcl van más
lejos y **prestan su propio compilador al programa**: `parse` en R entrega el árbol sintáctico como
un dato manipulable, y `expr` sin llaves obliga a Tcl a recompilar la expresión en cada vuelta —el
motivo por el que la guía de estilo de Tcl pide siempre `expr {...}` con llaves—. Ruby y Tcl dejan
inspeccionar la fase desde dentro del programa; Perl no, y hay que salir a `perl -MO=Concise`.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
En esta familia el fuente viaja como texto y el analizador vive dentro del navegador o del motor.

### Dart

```dart
import 'dart:io';

void main() {
  final t = stdin.readLineSync()!.trim().split(RegExp(r'\s+'));  // fase léxica
  final izq = int.parse(t[0]), der = int.parse(t[2]);            // fase sintáctica
  final r = switch (t[1]) {                                      // fase de evaluación
    '+' => izq + der,
    '-' => izq - der,
    _ => izq * der,
  };
  print('resultado=$r');
}
```

### ActionScript 3

```actionscript
// AVM2 no da acceso a stdin: la entrada llega ya analizada como argumentos.
// El compilador (mxmlc) produce bytecode ABC dentro de un .swf; no hay fase de enlace nativo.
package {
    public class Calc {
        public static function evaluar(izq:int, op:String, der:int):String {
            var r:int = op == "+" ? izq + der : op == "-" ? izq - der : izq * der;
            return "resultado=" + r;
        }
    }
}
```

**Qué reconocer:** Dart parte el fuente en un **kernel** intermedio (`.dill`) antes de ejecutarlo o
de compilarlo a nativo, así que su tubería tiene una fase más que la de JavaScript, donde V8 analiza
el texto en cada carga. ActionScript es el caso contrario y el más antiguo: la compilación a
bytecode ABC ocurre **entera antes de publicar**, y lo que se distribuye ya no es fuente. Ninguno de
los dos permite ver su forma intermedia desde el propio programa; se saca con `dart compile kernel`
o con un desensamblador de ABC como `swfdump -a`.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Cuatro compiladores distintos, un solo formato
de salida: el archivo `.class`.

### Kotlin

```kotlin
fun main() {
    val (izq, op, der) = readLine()!!.trim().split(Regex("\\s+"))
    val r = when (op) {
        "+" -> izq.toLong() + der.toLong()
        "-" -> izq.toLong() - der.toLong()
        else -> izq.toLong() * der.toLong()
    }
    println("resultado=$r")
}
```

### Scala

```scala
object Calc {
  def main(args: Array[String]): Unit = {
    val Array(izq, op, der) = scala.io.StdIn.readLine().trim.split("\\s+")
    val (x, y) = (izq.toLong, der.toLong)
    val r = op match {
      case "+" => x + y
      case "-" => x - y
      case _   => x * y
    }
    println(s"resultado=$r")
  }
}
```

### Groovy

```groovy
@groovy.transform.CompileStatic
class Calc {
    static void main(String[] args) {
        String[] t = System.in.newReader().readLine().trim().split(/\s+/)
        long x = t[0] as long
        long y = t[2] as long
        long r = t[1] == '+' ? x + y : t[1] == '-' ? x - y : x * y
        println "resultado=$r"
    }
}
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [[izq op der] (str/split (str/trim (read-line)) #"\s+")
      f ({"+" + "-" - "*" *} op)]          ; el token se resuelve a una función
  (println (str "resultado=" (f (Long/parseLong izq) (Long/parseLong der)))))
```

**Qué reconocer:** los cuatro terminan en el mismo `.class`, pero **cuándo** ocurre la compilación
los separa. Kotlin y Scala compilan antes de ejecutar, igual que `javac`. Groovy compila también,
solo que sin `@CompileStatic` deja las llamadas sin resolver y las decide en ejecución; la
anotación de arriba mueve esa decisión a la fase de compilación y hace el `.class` casi idéntico al
de Java. Clojure es el extremo: **compila en tiempo de carga**, forma por forma, mientras lee el
archivo. En los cuatro casos el resultado se inspecciona igual, con `javap -c Calc.class`.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). Distintos compiladores frontales, un mismo
lenguaje intermedio: CIL.

### F\#

```fsharp
let [| izq; op; der |] =
    stdin.ReadLine().Trim().Split([| ' ' |], System.StringSplitOptions.RemoveEmptyEntries)
let x, y = int64 izq, int64 der
let r =
    match op with
    | "+" -> x + y
    | "-" -> x - y
    | _   -> x * y
printfn "resultado=%d" r
```

### VB.NET

```vbnet
Imports System

Module Calc
    Sub Main()
        Dim t = Console.ReadLine().Trim().Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries)
        Dim x = Long.Parse(t(0))
        Dim y = Long.Parse(t(2))
        Dim r As Long
        Select Case t(1)
            Case "+" : r = x + y
            Case "-" : r = x - y
            Case Else : r = x * y
        End Select
        Console.WriteLine("resultado=" & r)
    End Sub
End Module
```

**Qué reconocer:** el `.dll` que sale de F# y el que sale de VB.NET son intercambiables porque ambos
frontales terminan escribiendo CIL contra la misma biblioteca base. La fase que sigue —CIL a código
máquina— no la hace ninguno de los dos compiladores, sino RyuJIT en ejecución. Ni F# ni VB.NET
muestran su CIL desde el propio programa: se lee con `ildasm` o con `dotnet-ildasm` sobre el
ensamblado ya generado.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). La familia donde las fases tienen nombres propios y
archivos propios: preprocesado, compilación, ensamblado y enlace.

### C++

```cpp
#include <iostream>

int main() {
    long long izq, der;
    char op;
    std::cin >> izq >> op >> der;
    const long long r = op == '+' ? izq + der : op == '-' ? izq - der : izq * der;
    std::cout << "resultado=" << r << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        long long izq = 0, der = 0;
        char op = '+';
        scanf("%lld %c %lld", &izq, &op, &der);
        long long r = op == '+' ? izq + der : op == '-' ? izq - der : izq * der;
        printf("resultado=%lld\n", r);
    }
    return 0;
}
```

**Qué reconocer:** en los dos, el programa **no puede** observar sus propias fases —cuando corre, ya
no queda nada del fuente—, pero el compilador las expone una por una desde fuera: `g++ -E` deja el
resultado del preprocesador, `-S` el ensamblador y `-c` el objeto sin enlazar. C++ añade una fase
que C no tiene: la **instanciación de plantillas**, que ocurre en compilación y explica sus tiempos
largos. Objective-C conserva las cuatro fases de C intactas y solo cambia el nombre de la primera,
porque `#import` es un `#include` con guarda automática.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilan a nativo antes
de ejecutar, pero no todos por el mismo camino.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, linea, " \r"), ' ');
    const izq = try std.fmt.parseInt(i64, it.next().?, 10);
    const op = it.next().?[0];
    const der = try std.fmt.parseInt(i64, it.next().?, 10);
    const r = switch (op) {
        '+' => izq + der,
        '-' => izq - der,
        else => izq * der,
    };
    try std.io.getStdOut().writer().print("resultado={d}\n", .{r});
}
```

### Nim

```nim
import std/strutils

let t = stdin.readLine().splitWhitespace()
let izq = t[0].parseInt
let der = t[2].parseInt
let r = case t[1]
        of "+": izq + der
        of "-": izq - der
        else:   izq * der
echo "resultado=", r

# Nim tiene una fase extra visible: genera C en ~/.cache/nim/ y luego llama a gcc.
#   nim c --nimcache:salida main.nim
```

### D

```d
import std.stdio, std.array, std.conv, std.string;

void main() {
    auto t = readln().strip().split();
    const izq = t[0].to!long;
    const der = t[2].to!long;
    long r;
    switch (t[1]) {
        case "+": r = izq + der; break;
        case "-": r = izq - der; break;
        default:  r = izq * der; break;
    }
    writeln("resultado=", r);
}
```

**Qué reconocer:** los tres producen un binario, pero la tubería intermedia es distinta y eso se
nota. Zig lleva su propio backend y además puede emitir C (`zig build-exe -ofmt=c`), así que se
mueve entre los dos mundos a voluntad. **Nim transpila a C** y delega en `gcc` o `clang` la
compilación de verdad: su carpeta de caché contiene los `.c` generados, y leerlos es la forma más
directa de entender qué hace una plantilla de Nim. D es el más convencional de los tres —`dmd`,
`ldc` o `gdc` van del fuente al objeto sin paso por C— y su fase distintiva es `static if` y la
evaluación en tiempo de compilación (`CTFE`), donde parte del programa **se ejecuta durante la fase
de compilación**.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Aquí la "compilación" produce un plan, no
instrucciones de máquina.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", [I, OpS, D]),
    number_string(X, I), number_string(Y, D),
    atom_string(Op, OpS),
    Expr =.. [Op, X, Y],              % fase sintáctica: se construye el término +(X, Y)
    R is Expr,                        % fase de evaluación: is/2 es el evaluador aritmético
    format("resultado=~d~n", [R]).
```

### Datalog

```datalog
% Datalog no tiene lexer ni E/S: la entrada llega ya analizada, como hechos.
entrada(3, "+", 4).

resultado(R) :- entrada(X, "+", Y), R = X + Y.
resultado(R) :- entrada(X, "-", Y), R = X - Y.
resultado(R) :- entrada(X, "*", Y), R = X * Y.
```

**Qué reconocer:** Prolog borra la frontera entre las fases. `Expr =.. [Op, X, Y]` construye en
ejecución el mismo término que el analizador habría construido al leer `3 + 4` en el fuente —código
y datos tienen la misma forma—, y `is/2` es literalmente el evaluador. Por debajo, SWI-Prolog sí
compila: traduce cada cláusula a instrucciones de la **WAM**, visibles con `vm_list(main/0)`.
Datalog renuncia a todo eso: no hay entrada, no hay operadores dinámicos y no hay orden de
ejecución que observar, solo un motor que satura las reglas hasta el punto fijo. Es la misma
renuncia de SQL, donde lo único parecido a "ver la fase" es `EXPLAIN`.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y en todos el mismo circuito: separar tokens, reconocer la
forma, evaluar. La diferencia real no está en la sintaxis sino en **dónde vive cada fase**: en el
compilador, en el cargador, en el runtime, o repartida entre los tres. Eso es lo transferible.

⏮️ [Volver a la clase 123](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
