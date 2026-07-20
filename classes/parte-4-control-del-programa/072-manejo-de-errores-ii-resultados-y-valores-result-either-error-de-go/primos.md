# 🧬 El mismo programa en las familias de lenguajes — Clase 072

> [⬅️ Volver a la clase 072](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —dividir devolviendo un resultado en vez de lanzar
una excepción— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no
solo por los diez lenguajes del núcleo.

La clase anterior mostró el error como **salto**; esta lo muestra como **dato**. La pregunta que
separa a los veinte lenguajes de abajo no es sintáctica: es si el lenguaje puede expresar "o un
entero o un error" en un solo tipo, o si hay que apañarlo con una tupla, un diccionario o una
convención.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b`, dos enteros
- **Salida** (stdout): `ok=<a/b entera>`, o `err=division` si `b` es 0
- **Regla:** si `b != 0` → `Ok(a/b)`; si `b == 0` → `Err(division)`

| stdin | esperado |
|---|---|
| `10 2` | `ok=5` |
| `7 0` | `err=division` |
| `8 4` | `ok=2` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Sin tipos suma, el resultado se representa con una tupla o un diccionario y la disciplina la pone
quien escribe, no el compilador.

### Ruby

```ruby
Resultado = Struct.new(:ok, :valor, :error)

def dividir(a, b)
  return Resultado.new(false, nil, "division") if b.zero?
  Resultado.new(true, a / b, nil)
end

a, b = STDIN.gets.split.map(&:to_i)
r = dividir(a, b)
puts r.ok ? "ok=#{r.valor}" : "err=#{r.error}"
```

### Perl

```perl
sub dividir {
    my ($a, $b) = @_;
    return (undef, 'division') if $b == 0;   # convención: (valor, error)
    return (int($a / $b), undef);
}

my ($a, $b) = split ' ', <STDIN>;
my ($valor, $err) = dividir($a, $b);
print defined $err ? "err=$err\n" : "ok=$valor\n";
```

### Lua

```lua
-- El idioma de Lua: en caso de fallo se devuelve nil seguido del mensaje.
local function dividir(a, b)
  if b == 0 then return nil, "division" end
  return a // b
end

local a, b = io.read("n", "n")
local valor, err = dividir(a, b)
if valor then
  print(string.format("ok=%d", valor))
else
  print("err=" .. err)
end
```

### Tcl

```tcl
proc dividir {a b} {
    if {$b == 0} { return [dict create ok 0 err division] }
    return [dict create ok 1 valor [expr {$a / $b}]]
}

gets stdin linea
lassign [split $linea] a b
set r [dividir $a $b]
if {[dict get $r ok]} {
    puts "ok=[dict get $r valor]"
} else {
    puts "err=[dict get $r err]"
}
```

### R

```r
dividir <- function(a, b) {
  if (b == 0) list(ok = FALSE, err = "division") else list(ok = TRUE, valor = a %/% b)
}

v <- as.integer(strsplit(readLines("stdin", n = 1), " ")[[1]])
r <- dividir(v[1], v[2])
cat(if (r$ok) sprintf("ok=%d\n", r$valor) else sprintf("err=%s\n", r$err))
```

**Qué reconocer:** los cinco devuelven el error **como dato**, igual que la tupla `(valor, err)` de
Python en la clase, y en los cinco nada impide ignorarlo: si no lees el segundo valor, el programa
sigue. **Lua** es el que más lejos llegó con la convención —`nil, mensaje` es la firma de media
biblioteca estándar, incluida `io.open`—, y tiene el mismo agujero que Go: quien llama puede no
mirar. **Ruby** y **Tcl** empaquetan los dos campos en una estructura para no depender del orden.
Sin tipo suma, la garantía es cultural, no del lenguaje.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
TypeScript sí puede escribir el tipo suma con una unión discriminada; JavaScript solo tiene el objeto
que hay debajo.

### Dart

```dart
import 'dart:io';

sealed class Resultado {}

class Ok extends Resultado {
  final int valor;
  Ok(this.valor);
}

class Err extends Resultado {
  final String mensaje;
  Err(this.mensaje);
}

Resultado dividir(int a, int b) => b == 0 ? Err('division') : Ok(a ~/ b);

void main() {
  final v = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  // El switch sobre una jerarquía sealed es exhaustivo: falta un caso, no compila.
  print(switch (dividir(v[0], v[1])) {
    Ok(valor: final x) => 'ok=$x',
    Err(mensaje: final m) => 'err=$m',
  });
}
```

### ActionScript 3

```actionscript
// AS3 no tiene stdin, ni tipos suma, ni comprobación de exhaustividad:
// el resultado se modela como un objeto con un campo discriminante.
package {
    public class Division {
        public static function dividir(a:int, b:int):Object {
            if (b == 0) return { ok: false, err: "division" };
            return { ok: true, valor: int(a / b) };
        }

        public static function salida(a:int, b:int):String {
            var r:Object = dividir(a, b);
            return r.ok ? "ok=" + r.valor : "err=" + r.err;
        }
    }
}
```

**Qué reconocer:** la distancia entre los dos primos mide veinte años de evolución de la familia.
**ActionScript** hace lo que haría JavaScript: un objeto con un campo `ok` que hay que acordarse de
mirar. **Dart 3** añadió clases `sealed` y patrones, y con ellos la pieza que faltaba: el `switch` es
una **expresión exhaustiva**, así que olvidarse del caso `Err` es un error de compilación, no un bug
en producción. Es la misma idea del `match` de Rust, aterrizada en un lenguaje de la familia de JS.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Java tardó en tener esto: solo con las
`sealed interface` y el *pattern matching* de `switch` puede expresar hoy lo que Scala hacía en 2004.

### Kotlin

```kotlin
fun dividir(a: Int, b: Int): Result<Int> =
    if (b == 0) Result.failure(IllegalArgumentException("division"))
    else Result.success(a / b)

fun main() {
    val (a, b) = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    dividir(a, b).fold(
        onSuccess = { println("ok=$it") },
        onFailure = { println("err=${it.message}") }
    )
}
```

### Scala

```scala
object Division {
  def dividir(a: Int, b: Int): Either[String, Int] =
    if (b == 0) Left("division") else Right(a / b)

  def main(args: Array[String]): Unit = {
    val Array(a, b) = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
    println(dividir(a, b) match {
      case Right(v) => s"ok=$v"
      case Left(e)  => s"err=$e"
    })
  }
}
```

### Groovy

```groovy
// Groovy no trae un tipo Result: se usa un mapa con campo discriminante.
def dividir(int a, int b) {
    b == 0 ? [ok: false, err: 'division'] : [ok: true, valor: a.intdiv(b)]
}

def (a, b) = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger()
def r = dividir(a, b)
println r.ok ? "ok=${r.valor}" : "err=${r.err}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; Sin tipos: el resultado es un mapa con una clave u otra.
(defn dividir [a b]
  (if (zero? b) {:err "division"} {:ok (quot a b)}))

(let [[a b] (map #(Long/parseLong %) (str/split (str/trim (read-line)) #"\s+"))
      r (dividir a b)]
  (println (if (contains? r :err)
             (str "err=" (:err r))
             (str "ok=" (:ok r)))))
```

**Qué reconocer:** **Scala** tiene el tipo canónico, `Either[Izquierda, Derecha]`, con la convención
—no la regla— de poner el error a la izquierda; encadenar operaciones que pueden fallar es
`flatMap`, sin un solo `if`. **Kotlin** trae `Result<T>` en la biblioteca estándar, pero con una
restricción reveladora: su lado de error es siempre un `Throwable`, es decir, sigue atado a la
jerarquía de excepciones de la JVM. **Groovy** y **Clojure** renuncian al tipo y usan un mapa; en
Clojure eso es coherente con todo el lenguaje —los datos son mapas—, y el precio es que nadie te
avisa si olvidas comprobar `:err`.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). C# no tiene un `Result` en la biblioteca estándar;
la comunidad usa paquetes de terceros o tuplas `(bool ok, T valor)`.

### F\#

```fsharp
let dividir a b =
    if b = 0 then Error "division" else Ok (a / b)

let v = stdin.ReadLine().Trim().Split(' ') |> Array.map int

match dividir v.[0] v.[1] with
| Ok r -> printfn "ok=%d" r
| Error e -> printfn "err=%s" e
```

### VB.NET

```vbnet
Module Division
    ' Sin tipo suma: una tupla con nombre y la convención de err = Nothing.
    Function Dividir(a As Integer, b As Integer) As (valor As Integer, err As String)
        If b = 0 Then Return (0, "division")
        Return (a \ b, Nothing)
    End Function

    Sub Main()
        Dim v = Console.ReadLine().Trim().Split(" "c)
        Dim r = Dividir(Integer.Parse(v(0)), Integer.Parse(v(1)))
        If r.err IsNot Nothing Then
            Console.WriteLine("err=" & r.err)
        Else
            Console.WriteLine("ok=" & r.valor)
        End If
    End Sub
End Module
```

**Qué reconocer:** **F#** trae `Result<'T,'TError>` en el lenguaje base, con `Ok` y `Error` como
constructores —los mismos nombres que Rust, y no por casualidad: ambos beben de ML— y con un `match`
exhaustivo que el compilador verifica. **VB.NET** no tiene nada de eso y aterriza en el patrón de Go:
devolver dos valores y confiar en que quien llama mire el segundo. Dos lenguajes sobre el mismo CLR,
y la diferencia no es de rendimiento sino de **quién comprueba**: el compilador o tú.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). El idioma clásico de C es devolver un código de
estado y escribir el valor real por un puntero de salida.

### C++

```cpp
#include <expected>
#include <iostream>
#include <string>

std::expected<long, std::string> dividir(long a, long b) {
    if (b == 0) return std::unexpected("division");
    return a / b;
}

int main() {
    long a, b;
    std::cin >> a >> b;
    if (auto r = dividir(a, b)) {
        std::cout << "ok=" << *r << '\n';
    } else {
        std::cout << "err=" << r.error() << '\n';
    }
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

// El idioma de Cocoa: BOOL de éxito + NSError** de salida.
static BOOL dividir(long a, long b, long *out, NSError **error) {
    if (b == 0) {
        if (error != NULL) {
            *error = [NSError errorWithDomain:@"Division" code:1 userInfo:nil];
        }
        return NO;
    }
    *out = a / b;
    return YES;
}

int main(void) {
    @autoreleasepool {
        long a, b, r = 0;
        if (scanf("%ld %ld", &a, &b) != 2) return 1;
        NSError *error = nil;
        if (dividir(a, b, &r, &error)) {
            printf("ok=%ld\n", r);
        } else {
            printf("err=division\n");
        }
    }
    return 0;
}
```

**Qué reconocer:** **C++23** incorporó `std::expected<T, E>`, que es el `Result` de Rust con otro
nombre: el objeto se convierte a `bool` en el `if`, `*r` saca el valor y `r.error()` el fallo. Es la
misma historia de `std::optional`, otra idea funcional adoptada décadas después.
**Objective-C** conserva el patrón de Cocoa: `BOOL` de retorno, valor por puntero y `NSError **` que
solo se rellena si fallaste. Fíjate en la comprobación `error != NULL`: la convención permite pasar
`nil` cuando no te interesa el detalle, y omitirla es un fallo de segmentación clásico. Frente a
`expected`, el error aquí no está *en* el tipo de retorno, va al lado.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Los dos representantes de
la clase: `(valor, error)` sin obligación de mirarlo, frente a `Result<T, E>` que el compilador te
obliga a abrir.

### Zig

```zig
const std = @import("std");

const DivError = error{Division};

fn dividir(a: i64, b: i64) DivError!i64 {
    if (b == 0) return error.Division;
    return @divTrunc(a, b);
}

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, linea, " \r"), ' ');
    const a = try std.fmt.parseInt(i64, it.next().?, 10);
    const b = try std.fmt.parseInt(i64, it.next().?, 10);

    const w = std.io.getStdOut().writer();
    const r = dividir(a, b) catch {
        try w.print("err=division\n", .{});
        return;
    };
    try w.print("ok={d}\n", .{r});
}
```

### Nim

```nim
import std/[strutils, sequtils, options]

func dividir(a, b: int): Option[int] =
  if b == 0: none(int) else: some(a div b)

let v = stdin.readLine().splitWhitespace().map(parseInt)
let r = dividir(v[0], v[1])
if r.isSome:
  echo "ok=", r.get()
else:
  # Option solo dice "no hay valor", no por qué. Para el motivo se usa el
  # paquete `results` (Result[T, E]) o una excepción.
  echo "err=division"
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm, std.typecons;

Nullable!long dividir(long a, long b) {
    return b == 0 ? Nullable!long.init : nullable(a / b);
}

void main() {
    auto v = readln().split().map!(to!long).array;
    auto r = dividir(v[0], v[1]);
    if (r.isNull) {
        writeln("err=division");
    } else {
        writefln("ok=%d", r.get);
    }
}
```

**Qué reconocer:** **Zig** es el más cercano al núcleo: `DivError!i64` es un **tipo unión de error**,
el error forma parte del tipo de retorno y el compilador no te deja ignorarlo —o lo abres con
`catch`, o lo propagas con `try`, o no compila—. La diferencia con Rust es que el conjunto de errores
se **infiere** a partir de los `return error.X` del cuerpo, así que no hay que declararlo a mano.
**Nim** y **D** usan aquí `Option` y `Nullable`, que expresan "puede no haber valor" pero **no el
motivo**: bastan para este contrato de un solo error, y dejan de bastar en cuanto hay dos motivos
distintos de fallo. Esa es exactamente la frontera entre `Option` y `Result`.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Sin tipos suma, SQL distingue los dos casos con
un `CASE WHEN` y devuelve la fila ya formateada.

### Prolog

```prolog
:- initialization(main, main).

% El "Result" es un término: ok(V) o err(E). Prolog no tiene tipos, pero los
% términos hacen de constructores igual que Ok y Err.
dividir(_, 0, err(division)).
dividir(A, B, ok(R)) :- B =\= 0, R is A // B.

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", [SA, SB]),
    number_string(A, SA),
    number_string(B, SB),
    dividir(A, B, Resultado),
    (   Resultado = ok(V)
    ->  format("ok=~d~n", [V])
    ;   Resultado = err(E),
        format("err=~w~n", [E])
    ).
```

### Datalog

```datalog
// Datalog no tiene tipos suma ni E/S. La distinción Ok/Err se modela con dos
// relaciones distintas: la regla que no aplica simplemente no deriva nada.
.decl par(a: number, b: number)
.decl ok(v: number)
.decl err(motivo: symbol)

par(10, 2).
par(7, 0).

ok(a / b) :- par(a, b), b != 0.
err("division") :- par(_, 0).

.output ok
.output err
```

**Qué reconocer:** **Prolog** es, sin tipos y sin haberlo pretendido, el más parecido a Rust de esta
página: `ok(V)` y `err(E)` son términos con functor distinto, y el `Resultado = ok(V)` del final es
*pattern matching* puro —unificación, la operación básica del lenguaje—. Lo que le falta es el
compilador que compruebe que cubriste los dos casos. **Datalog** disuelve el problema: no hay un
valor que sea "o esto o aquello", hay dos relaciones y cada regla deriva en la suya. Es la misma
solución que da SQL, y explica por qué en el mundo declarativo el error rara vez se modela: una
consulta que no encuentra nada no ha fallado, simplemente no devuelve filas.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una escala clara entre dos extremos. En un lado, la
**convención**: una tupla, un mapa, un `nil` seguido de un mensaje, un puntero de salida —funciona
si todo el mundo recuerda mirarlo—. En el otro, el **tipo**: `Either`, `Result`, `expected`, la unión
de error de Zig, la jerarquía `sealed` de Dart, donde el compilador se niega a seguir si dejas un
caso sin tratar. Reconocer en qué punto de esa escala está un lenguaje te dice más sobre cómo se
programa en él que cualquier detalle de su sintaxis.

⏮️ [Volver a la clase 072](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
