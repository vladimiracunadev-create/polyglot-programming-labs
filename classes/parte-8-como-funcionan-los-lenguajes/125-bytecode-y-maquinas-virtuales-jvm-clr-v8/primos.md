# 🧬 El mismo programa en las familias de lenguajes — Clase 125

> [⬅️ Volver a la clase 125](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —evaluar `a b op` en notación polaca inversa con una
pila— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por
los diez lenguajes del núcleo.

De todos los problemas del curso este es el que más se parece a su propio tema: la pila que
construyes a mano es, casi instrucción por instrucción, lo que la máquina virtual de la mitad de
estos lenguajes hace por debajo para calcular `3 + 4`.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b op` (dos enteros y un operador `+`, `-`, `*`)
- **Salida** (stdout): `resultado=<a op b>`
- **Regla:** apilar `a` y `b`; aplicar `op`; el tope de la pila es el resultado

| stdin | esperado |
|---|---|
| `3 4 +` | `resultado=7` |
| `5 6 *` | `resultado=30` |
| `10 2 -` | `resultado=8` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Casi todos estos lenguajes tienen su propia máquina virtual, y casi todas son máquinas de pila.

### Ruby

```ruby
pila = []
STDIN.gets.split.each do |t|
  if t.match?(/\A-?\d+\z/)
    pila.push(t.to_i)
  else
    y = pila.pop
    x = pila.pop
    pila.push(x.send(t, y))
  end
end
puts "resultado=#{pila.pop}"

# YARV es una máquina de pila y lo enseña:
#   puts RubyVM::InstructionSequence.compile("3 + 4").disasm
#   -> putobject 3 / putobject 4 / opt_plus / leave
```

### Perl

```perl
my @pila;
for my $t (split ' ', <STDIN>) {
    if ($t =~ /^-?\d+$/) { push @pila, $t; next }
    my $y = pop @pila;
    my $x = pop @pila;
    push @pila, $t eq '+' ? $x + $y : $t eq '-' ? $x - $y : $x * $y;
}
printf "resultado=%d\n", pop @pila;

# Perl no tiene bytecode ni pila de operandos: recorre un árbol de ops.
#   perl -MO=Concise -e '3 + 4'
```

### Lua

```lua
local pila = {}
for t in io.read("l"):gmatch("%S+") do
  if t:match("^%-?%d+$") then
    pila[#pila + 1] = tonumber(t)
  else
    local y = table.remove(pila)
    local x = table.remove(pila)
    if t == "+" then
      pila[#pila + 1] = x + y
    elseif t == "-" then
      pila[#pila + 1] = x - y
    else
      pila[#pila + 1] = x * y
    end
  end
end
print("resultado=" .. pila[#pila])

-- El bytecode de Lua NO es de pila, es de registros:
--   luac -l main.lua   -> ADD R2 R0 R1
```

### Tcl

```tcl
gets stdin linea
set pila {}
foreach t [split $linea] {
    if {[string is integer -strict $t]} {
        lappend pila $t
    } else {
        set y [lindex $pila end]
        set x [lindex $pila end-1]
        set pila [lrange $pila 0 end-2]
        lappend pila [expr "$x $t $y"]
    }
}
puts "resultado=[lindex $pila end]"

# La VM de Tcl también es de pila, y se puede ver desde el propio script:
#   puts [::tcl::unsupported::disassemble script {expr {3 + 4}}]
```

### R

```r
tokens <- scan("stdin", what = "", n = 3, quiet = TRUE)
pila <- integer(0)
for (t in tokens) {
  if (grepl("^-?[0-9]+$", t)) {
    pila <- c(pila, as.integer(t))
  } else {
    k <- length(pila)
    valor <- do.call(t, list(pila[k - 1], pila[k]))
    pila <- c(pila[seq_len(k - 2)], valor)
  }
}
cat(sprintf("resultado=%d\n", pila[length(pila)]))

# El compilador opcional de R emite bytecode de pila:
#   compiler::disassemble(compiler::cmpfun(function(x, y) x + y))
```

**Qué reconocer:** el bucle es el mismo en los cinco, pero solo tres de ellos tienen debajo una
máquina que hace literalmente esto. YARV (Ruby) y la VM de Tcl son **máquinas de pila**: `3 + 4` se
convierte en dos instrucciones que empujan y una que consume el tope, igual que arriba. R hace lo
mismo, pero solo si activas su compilador de bytecode, que es opcional. Lua rompe el patrón y es la
excepción más citada del mundo de las VM: su bytecode es de **registros**, `ADD R2 R0 R1`, sin
empujar nada —menos instrucciones por operación, a cambio de un compilador más complicado—. Y Perl
no tiene ni pila ni bytecode: salta de nodo en nodo por un árbol de operaciones, que es por lo que
no existe un formato de "Perl compilado" comparable a un `.class`.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final pila = <int>[];
  for (final t in stdin.readLineSync()!.trim().split(RegExp(r'\s+'))) {
    final n = int.tryParse(t);
    if (n != null) {
      pila.add(n);
    } else {
      final y = pila.removeLast();
      final x = pila.removeLast();
      pila.add(switch (t) { '+' => x + y, '-' => x - y, _ => x * y });
    }
  }
  print('resultado=${pila.last}');
}
```

### ActionScript 3

```actionscript
// AVM2 no expone stdin: los tokens llegan como argumento.
// Curiosidad del caso: el bytecode ABC que produce este archivo ES una máquina de pila.
package {
    public class Rpn {
        public static function evaluar(tokens:Array):String {
            var pila:Array = [];
            for each (var t:String in tokens) {
                if (t == "+" || t == "-" || t == "*") {
                    var y:int = pila.pop();
                    var x:int = pila.pop();
                    pila.push(t == "+" ? x + y : t == "-" ? x - y : x * y);
                } else {
                    pila.push(parseInt(t, 10));
                }
            }
            return "resultado=" + pila.pop();
        }
    }
}
```

**Qué reconocer:** ActionScript es el ejemplo más nítido de esta página porque su bytecode ABC se
distribuye tal cual dentro del `.swf`: las instrucciones `pushint`, `add_i` y `pop` son las mismas
que el programa de arriba escribe a mano. Dart no publica un formato equivalente al usuario —su
`.dill` es una representación de árbol, no de pila— y por eso su modelo se parece más al de Perl que
al de la JVM. Al otro lado, V8 sí interpreta bytecode de registros con Ignition antes de que
TurboFan compile: dentro de una misma familia conviven los dos diseños.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La máquina de pila más documentada que existe,
y el destino común de estos cuatro.

### Kotlin

```kotlin
fun main() {
    val pila = ArrayDeque<Long>()
    for (t in readLine()!!.trim().split(Regex("\\s+"))) {
        val n = t.toLongOrNull()
        if (n != null) {
            pila.addLast(n)
        } else {
            val y = pila.removeLast()
            val x = pila.removeLast()
            pila.addLast(when (t) { "+" -> x + y; "-" -> x - y; else -> x * y })
        }
    }
    println("resultado=${pila.last()}")
}
```

### Scala

```scala
import scala.collection.mutable

object Rpn {
  def main(args: Array[String]): Unit = {
    val pila = mutable.Stack[Long]()
    for (t <- scala.io.StdIn.readLine().trim.split("\\s+")) t match {
      case "+" | "-" | "*" =>
        val y = pila.pop()
        val x = pila.pop()
        pila.push(if (t == "+") x + y else if (t == "-") x - y else x * y)
      case n => pila.push(n.toLong)
    }
    println(s"resultado=${pila.top}")
  }
}
```

### Groovy

```groovy
def pila = []
System.in.newReader().readLine().trim().split(/\s+/).each { t ->
    if (t in ['+', '-', '*']) {
        long y = pila.pop()          // en Groovy, List.pop() saca el ÚLTIMO elemento
        long x = pila.pop()
        pila << (t == '+' ? x + y : t == '-' ? x - y : x * y)
    } else {
        pila << (t as long)
    }
}
println "resultado=${pila.last()}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; Un vector de Clojure ya es una pila: conj/peek/pop operan en el extremo derecho.
(let [ops {"+" + "-" - "*" *}
      pila (reduce (fn [p t]
                     (if-let [f (ops t)]
                       (let [y (peek p)
                             x (peek (pop p))]
                         (conj (pop (pop p)) (f x y)))
                       (conj p (Long/parseLong t))))
                   []
                   (str/split (str/trim (read-line)) #"\s+"))]
  (println (str "resultado=" (peek pila))))
```

**Qué reconocer:** los cuatro compilan al mismo bytecode y ese bytecode es exactamente lo que este
programa simula. `javap -c` sobre cualquiera de ellos muestra `ldc 3`, `ldc 4`, `ladd`: la JVM no
tiene registros de propósito general, solo una **pila de operandos por marco de llamada**, y por eso
sus instrucciones no llevan argumentos. La diferencia entre los cuatro está en el momento y en el
grosor de la traducción: Kotlin y Scala compilan antes de ejecutar y Scala genera bastante más
bytecode por línea de fuente; Clojure compila **al cargar**, generando una clase por función; y
Groovy, sin `@CompileStatic`, deja las llamadas como `invokedynamic` y decide en ejecución. La
máquina de pila es la misma para los cuatro; lo que cambia es cuánto se decide antes de llegar a
ella.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). Otro diseño de pila, con un detalle propio:
nadie ejecuta el CIL tal cual.

### F\#

```fsharp
open System.Collections.Generic

let pila = Stack<int64>()
for t in (stdin.ReadLine()).Trim().Split([| ' ' |], System.StringSplitOptions.RemoveEmptyEntries) do
    match t with
    | "+" | "-" | "*" ->
        let y = pila.Pop()
        let x = pila.Pop()
        pila.Push(match t with
                  | "+" -> x + y
                  | "-" -> x - y
                  | _   -> x * y)
    | n -> pila.Push(int64 n)
printfn "resultado=%d" (pila.Peek())
```

### VB.NET

```vbnet
Imports System
Imports System.Collections.Generic

Module Rpn
    Sub Main()
        Dim pila As New Stack(Of Long)()
        For Each t In Console.ReadLine().Trim().Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries)
            Select Case t
                Case "+", "-", "*"
                    Dim y = pila.Pop()
                    Dim x = pila.Pop()
                    Select Case t
                        Case "+" : pila.Push(x + y)
                        Case "-" : pila.Push(x - y)
                        Case Else : pila.Push(x * y)
                    End Select
                Case Else
                    pila.Push(Long.Parse(t))
            End Select
        Next
        Console.WriteLine("resultado=" & pila.Peek())
    End Sub
End Module
```

**Qué reconocer:** el CIL es tan de pila como el bytecode de la JVM —`ldc.i4.3`, `ldc.i4.4`, `add`—,
y ambos lenguajes usan aquí la misma clase `Stack<T>` porque comparten biblioteca base. La
diferencia con la JVM es que ese CIL **nunca se interpreta**: RyuJIT lo convierte a código máquina
de registros la primera vez que se llama al método, así que la pila del CIL es un formato de
transporte, no un modelo de ejecución. Ninguno de los dos lenguajes puede mostrar su propio CIL en
ejecución; se lee con `ildasm` sobre el ensamblado ya construido.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Sin máquina virtual: la única pila que hay es la del
procesador.

### C++

```cpp
#include <iostream>
#include <stack>
#include <string>

int main() {
    std::stack<long long> pila;
    std::string t;
    while (std::cin >> t) {
        if (t == "+" || t == "-" || t == "*") {
            long long y = pila.top(); pila.pop();
            long long x = pila.top(); pila.pop();
            pila.push(t == "+" ? x + y : t == "-" ? x - y : x * y);
        } else {
            pila.push(std::stoll(t));
        }
    }
    std::cout << "resultado=" << pila.top() << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSData *datos = [[NSFileHandle fileHandleWithStandardInput] availableData];
        NSString *linea = [[NSString alloc] initWithData:datos encoding:NSUTF8StringEncoding];
        NSCharacterSet *blancos = [NSCharacterSet whitespaceAndNewlineCharacterSet];
        NSMutableArray<NSNumber *> *pila = [NSMutableArray array];
        for (NSString *t in [[linea stringByTrimmingCharactersInSet:blancos]
                             componentsSeparatedByString:@" "]) {
            if ([@[@"+", @"-", @"*"] containsObject:t]) {
                long long y = [pila.lastObject longLongValue]; [pila removeLastObject];
                long long x = [pila.lastObject longLongValue]; [pila removeLastObject];
                long long r = [t isEqualToString:@"+"] ? x + y
                            : [t isEqualToString:@"-"] ? x - y : x * y;
                [pila addObject:@(r)];
            } else {
                [pila addObject:@([t longLongValue])];
            }
        }
        printf("resultado=%lld\n", [pila.lastObject longLongValue]);
    }
    return 0;
}
```

**Qué reconocer:** aquí la pila del programa es una **estructura de datos cualquiera**, no un espejo
del runtime, porque no hay runtime que espejar: `x86-64` y ARM son máquinas de registros y el
compilador reparte los valores entre ellos. La comparación honesta es al revés —la pila de operandos
de la JVM existe precisamente porque un formato de pila es más fácil de portar entre CPUs
distintas—. Objective-C conserva una capa de indirección que C++ no tiene: cada `[pila addObject:]`
pasa por `objc_msgSend`, resuelto en ejecución con una caché por clase, lo más cercano a un
despachador de VM que queda en esta familia.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Binario nativo, sin
máquina virtual entre el código y el procesador.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [128]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var pila: [16]i64 = undefined;
    var sp: usize = 0;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, linea, " \r"), ' ');
    while (it.next()) |t| {
        if (std.fmt.parseInt(i64, t, 10)) |n| {
            pila[sp] = n;
            sp += 1;
        } else |_| {
            const y = pila[sp - 1];
            const x = pila[sp - 2];
            sp -= 2;
            pila[sp] = switch (t[0]) {
                '+' => x + y,
                '-' => x - y,
                else => x * y,
            };
            sp += 1;
        }
    }
    try std.io.getStdOut().writer().print("resultado={d}\n", .{pila[sp - 1]});
}
```

### Nim

```nim
import std/strutils

var pila: seq[int]
for t in stdin.readLine().splitWhitespace():
  case t
  of "+", "-", "*":
    let y = pila.pop()
    let x = pila.pop()
    pila.add(case t
             of "+": x + y
             of "-": x - y
             else:   x * y)
  else:
    pila.add(t.parseInt)
echo "resultado=", pila[^1]
```

### D

```d
import std.stdio, std.array, std.conv, std.string;

void main() {
    long[] pila;
    foreach (t; readln().strip().split()) {
        switch (t) {
            case "+", "-", "*":
                const y = pila[$ - 1];
                const x = pila[$ - 2];
                pila = pila[0 .. $ - 2];
                pila ~= t == "+" ? x + y : t == "-" ? x - y : x * y;
                break;
            default:
                pila ~= t.to!long;
                break;
        }
    }
    writeln("resultado=", pila[$ - 1]);
}
```

**Qué reconocer:** ninguno de los tres tiene bytecode propio, pero los tres pasan por una
representación intermedia antes del binario, y ahí está la diferencia. Nim **genera C** y deja que
`gcc` produzca el código máquina; su "IR" es un lenguaje de programación completo que puedes abrir y
leer (`nim c --nimcache:salida`). D con `ldc` y Zig con su backend por omisión pasan por **LLVM IR**,
que sí es un formato intermedio de verdad —de registros infinitos, no de pila— y se puede volcar con
`zig build-obj -femit-llvm-ir`. Zig tiene además su propio bytecode interno para `comptime`, que
ejecuta parte del programa dentro del compilador. Un sistema puede tener representación intermedia
sin tener máquina virtual en ejecución: son cosas distintas.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Una máquina virtual sí hay, pero no es del
lenguaje: es del motor.

### Prolog

```prolog
:- initialization(main, main).

evaluar([], [R], R).
evaluar([T|Resto], Pila, R) :-
    (   number_string(N, T)
    ->  evaluar(Resto, [N|Pila], R)
    ;   Pila = [Y, X|Base],
        atom_string(Op, T),
        Expr =.. [Op, X, Y],
        V is Expr,
        evaluar(Resto, [V|Base], R)
    ).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Tokens),
    evaluar(Tokens, [], R),
    format("resultado=~d~n", [R]).
```

### Datalog

```datalog
% Datalog no tiene estado mutable: no se puede apilar ni desapilar nada.
% Lo más cercano es declarar la entrada ya desglosada y una regla por operador.
entrada(3, 4, "+").

resultado(R) :- entrada(X, Y, "+"), R = X + Y.
resultado(R) :- entrada(X, Y, "-"), R = X - Y.
resultado(R) :- entrada(X, Y, "*"), R = X * Y.
```

**Qué reconocer:** Prolog no tiene una pila mutable, así que la simula con una **lista que se pasa
como argumento** —apilar es poner un elemento en cabeza y la recursión hace de bucle—. Por debajo,
sin embargo, SWI-Prolog es tan de máquina virtual como Java: compila cada cláusula a instrucciones
de la **WAM**, con su pila de objetivos, su rastro y su montón, y `vm_list(evaluar/3)` las muestra.
Datalog es el único de los veinte que **no puede** expresar el problema: sin estado no hay pila. Su
motor tampoco ejecuta bytecode, sino que satura las reglas hasta el punto fijo, igual que SQLite
—que sí compila cada consulta a bytecode para su propia VM, visible con `EXPLAIN`— toma sus
decisiones sin que la consulta las mencione.

---

## Y de vuelta a la clase

Veinte programas empujando y sacando de una pila, y para más de la mitad de ellos eso no es una
metáfora: es lo que su máquina virtual hace con cada suma. Reconocer el patrón de pila en el propio
código es reconocer, de paso, la forma del bytecode que hay debajo.

⏮️ [Volver a la clase 125](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
