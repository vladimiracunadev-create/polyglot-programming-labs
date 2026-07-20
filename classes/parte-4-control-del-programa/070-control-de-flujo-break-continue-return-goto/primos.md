# 🧬 El mismo programa en las familias de lenguajes — Clase 070

> [⬅️ Volver a la clase 070](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —el menor divisor de `n` mayor que 1, saliendo del
bucle en cuanto aparece— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

El interés aquí no es el algoritmo, que es trivial, sino el **gesto de salida**: `break`, `last`,
`Exit For`, `goto`, un corte, una etiqueta, o directamente ninguna palabra porque el lenguaje no
tiene bucles de los que salir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n` con `n >= 2`
- **Salida** (stdout): `primer_divisor=<el menor divisor > 1>`
- **Regla:** el menor `d` en `[2..n]` tal que `n % d == 0` (para un primo, ese `d` es el propio `n`)

| stdin | esperado |
|---|---|
| `15` | `primer_divisor=3` |
| `7` | `primer_divisor=7` |
| `12` | `primer_divisor=2` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Bucles con `break` y `continue` de toda la vida; lo que cambia entre primos es si existe `continue`
como palabra y si `break` puede saltar más de un nivel.

### Ruby

```ruby
n = STDIN.gets.to_i
d = n
(2..n).each do |k|
  next if n % k != 0
  d = k
  break
end
puts "primer_divisor=#{d}"
```

### Perl

```perl
my $n = <STDIN>;
chomp $n;
my $d = $n;
BUSCA: for my $k (2 .. $n) {
    next BUSCA if $n % $k;   # `next` es el continue de Perl
    $d = $k;
    last BUSCA;              # `last` es el break, y admite etiqueta
}
print "primer_divisor=$d\n";
```

### Lua

```lua
local n = math.tointeger(io.read("n"))
local d = n
for k = 2, n do
  if n % k == 0 then
    d = k
    -- Lua no tiene `continue`; su goto sí puede salir de varios bucles a la vez.
    goto fin
  end
end
::fin::
print(string.format("primer_divisor=%d", d))
```

### Tcl

```tcl
gets stdin n
set d $n
for {set k 2} {$k <= $n} {incr k} {
    if {$n % $k != 0} { continue }
    set d $k
    break
}
puts "primer_divisor=$d"
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))
d <- n
for (k in 2:n) {
  if (n %% k != 0) next
  d <- k
  break
}
cat(sprintf("primer_divisor=%d\n", d))
```

**Qué reconocer:** el esqueleto es idéntico —recorrer, descartar, salir— pero el vocabulario no.
**Perl** llama `last` y `next` a lo que Python llama `break` y `continue`, y además etiqueta bucles,
algo que Python no permite. **R** dice `next` como Perl. **Lua** es el caso interesante: **no tiene
`continue`** en absoluto, y por eso incorporó `goto` en la 5.2 —el idioma habitual es `goto continua`
con una etiqueta al final del cuerpo—; aquí se usa para lo contrario, salir del bucle *y* seguir
después, que es justo lo que un `break` no sabe hacer cuando hay varios niveles. En **Ruby**, ojo:
`break` funciona porque `each` recibe un bloque, no una lambda; dentro de una lambda `break` querría
decir otra cosa.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
Toda la familia heredó de Java las etiquetas de bucle, y ninguna heredó el `goto`.

### Dart

```dart
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  var d = n;
  busca:
  for (var k = 2; k <= n; k++) {
    if (n % k != 0) continue busca;
    d = k;
    break busca;
  }
  print('primer_divisor=$d');
}
```

### ActionScript 3

```actionscript
// Sin stdin en el reproductor Flash: la función recibe n y devuelve la línea.
package {
    public class Divisor {
        public static function primerDivisor(n:int):String {
            var d:int = n;
            busca: for (var k:int = 2; k <= n; k++) {
                if (n % k != 0) continue busca;
                d = k;
                break busca;
            }
            return "primer_divisor=" + d;
        }
    }
}
```

**Qué reconocer:** `busca:` delante del `for` es exactamente la etiqueta de JavaScript, y
`break busca` / `continue busca` son las mismas dos palabras del núcleo con un destino explícito.
Con un solo bucle la etiqueta sobra; su valor aparece cuando hay dos anidados y quieres salir del
externo, que en un lenguaje sin `goto` es la única manera de hacerlo sin una bandera booleana.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Java tiene `break`, `continue` y etiquetas —y
reserva `goto` como palabra clave sin usarla, un guiño a la mala fama que arrastraba en 1995—.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toInt()
    var d = n
    busca@ for (k in 2..n) {
        if (n % k != 0) continue@busca
        d = k
        break@busca
    }
    println("primer_divisor=$d")
}
```

### Scala

```scala
object Divisor {
  def main(args: Array[String]): Unit = {
    val n = scala.io.StdIn.readLine().trim.toInt
    // Scala no tiene break: la secuencia se detiene sola en el primer acierto.
    val d = (2 to n).find(k => n % k == 0).getOrElse(n)
    println(s"primer_divisor=$d")
  }
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim() as int
def d = n
// `break` solo vale en un bucle de verdad: dentro de un `each { }` sería un error.
for (k in 2..n) {
    if (n % k != 0) continue
    d = k
    break
}
println "primer_divisor=$d"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [n (Long/parseLong (str/trim (read-line)))
      ;; No hay break: la secuencia es perezosa y `first` deja de pedir elementos.
      d (first (filter #(zero? (mod n %)) (range 2 (inc n))))]
  (println (str "primer_divisor=" d)))
```

**Qué reconocer:** cuatro lenguajes sobre la misma máquina, y solo dos conservan la palabra `break`.
**Kotlin** mantiene el modelo de Java y solo cambia la sintaxis de la etiqueta (`busca@` en vez de
`busca:`). **Groovy** es Java casi literal, con una trampa muy citada: en un `each { }` el cuerpo es
una *clausura*, no un bucle, y ahí `break` no compila. **Scala** eliminó `break` del lenguaje —existe
`scala.util.control.Breaks`, pero está implementado lanzando una excepción, y por eso casi nadie lo
usa— y lo sustituye por `find`, que expresa la intención en vez del mecanismo. **Clojure** llega al
mismo sitio por la pereza: `filter` no evalúa lo que nadie pide, así que `first` detiene el cálculo
sin ninguna palabra de control. Salir del bucle y no entrar en él acaban costando lo mismo.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). C# sí tiene `goto`, y es de los pocos lenguajes
modernos donde se usa sin escándalo: para saltar entre casos de un `switch`.

### F\#

```fsharp
let n = stdin.ReadLine().Trim() |> int
// F# no tiene break ni continue: la secuencia perezosa para en el primer acierto.
let d = seq { 2 .. n } |> Seq.find (fun k -> n % k = 0)
printfn "primer_divisor=%d" d
```

### VB.NET

```vbnet
Module Divisor
    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Dim d = n
        For k = 2 To n
            If n Mod k <> 0 Then Continue For
            d = k
            Exit For
        Next
        Console.WriteLine("primer_divisor=" & d)
    End Sub
End Module
```

**Qué reconocer:** el mismo CLR sostiene los dos extremos. **VB.NET** nombra las cosas con dos
palabras (`Exit For`, `Continue For`, y también `Exit Sub`, `Exit While`, `Exit Do`): la salida dice
siempre de **qué** sale, lo que hace innecesarias las etiquetas. **F#**, en cambio, no tiene ninguna
de las dos construcciones —igual que Scala, prefiere la expresión que se detiene sola— y responde
con `Seq.find`. Si el elemento pudiera no existir, el idioma sería `Seq.tryFind`, que devuelve una
opción en vez de fallar: la misma idea de la clase 072 asomando aquí.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Es la familia donde `goto` sigue siendo idiomático,
sobre todo para el patrón de liberar recursos antes de salir de una función.

### C++

```cpp
#include <iostream>

int main() {
    long n;
    std::cin >> n;
    long d = n;
    for (long k = 2; k <= n; ++k) {
        if (n % k != 0) continue;
        d = k;
        break;
    }
    std::cout << "primer_divisor=" << d << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        long n;
        if (scanf("%ld", &n) != 1) return 1;
        long d = n;
        for (long k = 2; k <= n; k++) {
            if (n % k != 0) continue;
            d = k;
            break;
        }
        printf("primer_divisor=%ld\n", d);
    }
    return 0;
}
```

**Qué reconocer:** el bucle es carácter por carácter el de la implementación de C de la clase: ambos
lenguajes son superconjuntos y no cambiaron nada del control de flujo heredado. Lo que sí añadieron
es **cuándo el salto tiene consecuencias**: en C++, un `goto` que cruce hacia dentro del ámbito de
una variable con constructor no compila, y un `break` que abandone un bloque ejecuta los destructores
de lo que había vivo. En C saltar es barato porque no hay nada que destruir; en C++ el salto arrastra
trabajo invisible.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Go conserva `goto` y
etiquetas; Rust las tiene con la sintaxis `'nombre:` y, además, su `break` puede **devolver un valor**
desde el bucle.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(u64, std.mem.trim(u8, linea, " \r"), 10);

    // En Zig el break devuelve un valor desde el bloque etiquetado.
    const d = busca: {
        var k: u64 = 2;
        while (k <= n) : (k += 1) {
            if (n % k == 0) break :busca k;
        }
        break :busca n;
    };

    try std.io.getStdOut().writer().print("primer_divisor={d}\n", .{d});
}
```

### Nim

```nim
import std/strutils

let n = stdin.readLine().strip().parseInt()
var d = n
block busca:
  for k in 2 .. n:
    if n mod k != 0: continue
    d = k
    break busca
echo "primer_divisor=", d
```

### D

```d
import std.stdio, std.string, std.conv;

void main() {
    const n = readln().strip().to!long;
    long d = n;
    busca: foreach (k; 2 .. n + 1) {
        if (n % k != 0) continue busca;
        d = k;
        break busca;
    }
    writefln("primer_divisor=%d", d);
}
```

**Qué reconocer:** **Zig** eliminó `goto` del lenguaje —no existe— y a cambio hizo del `break` una
expresión: `break :busca k` sale del bloque *y* lo evalúa a `k`, igual que el `break valor` de Rust.
El bloque etiquetado sustituye a la variable mutable que los demás necesitan. **Nim** separa las dos
ideas: `block busca:` declara el ámbito del que se sale y `break busca` lo abandona, además de
conservar un `continue` normal. **D** mantiene el paquete completo de C —etiquetas, `break`,
`continue` y también `goto`— porque su compatibilidad con C era un objetivo declarado. Tres
lenguajes de sistemas y tres respuestas a la misma pregunta: ¿es el salto una instrucción o una
expresión?

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). En SQL no hay bucle del que salir: se describe
el conjunto de divisores y se pide el mínimo.

### Prolog

```prolog
:- initialization(main, main).

% El corte (!) es el "break": descarta los puntos de elección pendientes,
% así que `between` no vuelve a probar valores mayores.
divisor(N, D) :- between(2, N, D), 0 is N mod D, !.

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    divisor(N, D),
    format("primer_divisor=~d~n", [D]).
```

### Datalog

```datalog
// Datalog no tiene bucles, ni break, ni E/S: no hay recorrido que interrumpir.
// Se declara la relación "d divide a n" y el menor sale de una agregación.
.decl entrada(n: number)
.decl divide(n: number, d: number)
.decl primer_divisor(n: number, d: number)

entrada(15).
divide(n, d) :- entrada(n), d = range(2, n + 1), n % d = 0.
primer_divisor(n, d) :- entrada(n), d = min x : { divide(n, x) }.

.output primer_divisor
```

**Qué reconocer:** **Prolog** sí tiene algo parecido a un bucle —`between` genera candidatos por
retroceso— y el corte `!` es literalmente su `break`: le dice al motor que no guarde los puntos de
elección restantes. La diferencia con `break` es que el corte no interrumpe una repetición, sino que
**poda el árbol de búsqueda**, y por eso su posición dentro de la cláusula cambia el resultado.
**Datalog** ni siquiera tiene esa noción: deriva todos los divisores a la vez y el "menor" se pide
con `min`, la misma renuncia que hace SQL cuando le pides `MIN(k)` sin decirle en qué orden mirar las
filas. Cuando no describes un recorrido, no hay nada de lo que salir.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y tres respuestas distintas a "¿cómo salgo de aquí?": la
**instrucción** (`break`, `last`, `Exit For`, el corte de Prolog), la **expresión** que se detiene
sola (`find`, `first`, `Seq.find`, la secuencia perezosa) y el **salto con valor** de Zig y Rust. La
tercera es la más reciente, y no por casualidad: convierte en un dato lo que antes era un efecto
sobre una variable mutable.

⏮️ [Volver a la clase 070](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
