# 🧬 El mismo programa en las familias de lenguajes — Clase 103

> [⬅️ Volver a la clase 103](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —crear un recurso, usarlo y liberarlo al salir de su
ámbito— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo
por los diez lenguajes del núcleo.

Aquí el contrato es casi una excusa: lo interesante no es imprimir `estado=liberado`, sino **quién
decide cuándo se libera** y si esa decisión es determinista o queda en manos de un recolector que
pasará cuando le convenga.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin): un entero `n`, el valor del recurso
- **Salida** (stdout): `valor=<n> estado=liberado`
- **Regla:** crear el recurso con `n`, leer su valor y liberarlo al salir del ámbito

| stdin | esperado |
|---|---|
| `5` | `valor=5 estado=liberado` |
| `0` | `valor=0 estado=liberado` |
| `9` | `valor=9 estado=liberado` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Todos delegan la memoria en un recolector, así que el ciclo de vida del recurso se marca con un
bloque, no con la memoria.

### Ruby

```ruby
class Recurso
  attr_reader :valor

  def initialize(valor)
    @valor = valor
  end

  # Ruby no tiene destructores deterministas: el bloque con ensure es el sustituto idiomático
  def self.abrir(valor)
    r = new(valor)
    yield r
  ensure
    # aquí se libera
  end
end

n = STDIN.gets.to_i
valor = Recurso.abrir(n) { |r| r.valor }
puts "valor=#{valor} estado=liberado"
```

### Perl

```perl
package Recurso;
sub new { my ($clase, $valor) = @_; return bless { valor => $valor }, $clase; }
sub DESTROY { }   # Perl cuenta referencias: DESTROY sí es determinista

package main;
my $linea = <STDIN>;
chomp $linea;
my $valor;
{
    my $r = Recurso->new($linea);
    $valor = $r->{valor};
}   # el conteo llega a cero al cerrar el bloque y se llama a DESTROY
print "valor=$valor estado=liberado\n";
```

### Lua

```lua
local n = io.read("n")
local valor
do
  local recurso = setmetatable({ valor = n }, { __gc = function() end })
  valor = recurso.valor
end
collectgarbage()  -- __gc existe, pero el momento lo decide el recolector, no el ámbito
print("valor=" .. valor .. " estado=liberado")
```

### Tcl

```tcl
gets stdin linea
set n [string trim $linea]

proc usar {valor} {
    # las variables locales desaparecen al retornar; para recursos externos está `trace` o `close`
    return $valor
}

set valor [usar $n]
puts "valor=$valor estado=liberado"
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))
valor <- local({
  recurso <- list(valor = n)
  on.exit(rm(recurso))  # R no tiene destructores: on.exit marca el fin de uso, no la liberación
  recurso$valor
})
cat(sprintf("valor=%d estado=liberado\n", valor))
```

**Qué reconocer:** cuatro de los cinco **no pueden garantizar cuándo se libera nada**, y por eso los
cuatro sustituyen la garantía por una convención de ámbito: el bloque con `ensure` de Ruby, el
`local` con `on.exit` de R, el `do ... end` de Lua. Es el mismo gesto que el `with` de Python: no
libera memoria, delimita el uso. Ruby es explícito al respecto —tuvo un `ObjectSpace.define_finalizer`
y la comunidad recomienda no usarlo—, y Lua ofrece el metamétodo `__gc` pero avisa de que se ejecuta
cuando el recolector pase, no cuando cierres la llave. Perl es la excepción del grupo: usa **conteo
de referencias**, así que en cuanto la última referencia desaparece se llama a `DESTROY`
inmediatamente y de forma predecible —el mismo modelo que PHP en el núcleo, y la razón por la que
ambos sí pueden cerrar un fichero al salir del bloque sin decir nada—. El precio del conteo de
referencias son los ciclos: dos objetos que se apuntan mutuamente no se liberan nunca.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
Recolector obligatorio y ningún punto de enganche fiable para liberar.

### Dart

```dart
import 'dart:io';

class Recurso {
  final int valor;
  Recurso(this.valor);
  void liberar() {/* Dart no tiene destructores: la liberación es explícita */}
}

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  final r = Recurso(n);
  final valor = r.valor;
  r.liberar();
  print('valor=$valor estado=liberado');
}
```

### ActionScript 3

```actionscript
// ActionScript no tiene stdin ni destructores: soltar la referencia es lo único que se puede hacer.
package {
    public class CicloDeVida {
        public static function demo(n:int):String {
            var r:Object = { valor: n };
            var valor:int = r.valor;
            r = null;  // el reproductor recolectará cuando quiera; no hay garantía de momento
            return "valor=" + valor + " estado=liberado";
        }
    }
}
```

**Qué reconocer:** esta es la familia con **menos control de toda la página**, y conviene decirlo sin
adornos: ninguno de los dos tiene destructor, ni bloque de liberación, ni forma de saber cuándo se
recupera la memoria. ActionScript 3 solo puede asignar `null` y esperar; la práctica habitual en
Flash era añadir a mano un método `dispose()` y llamarlo por convención, porque el reproductor no
ayudaba. Dart hace exactamente lo mismo con mejor nombre —`liberar()`, `close()`, `dispose()` en
Flutter—, y su `Finalizer` solo garantiza que *quizá* se ejecute. Cuando el lenguaje no ofrece
garantías, la disciplina del programador es la única política de ciclo de vida que queda.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). `finalize()` está en desuso desde Java 9; lo
que quedó en pie es `AutoCloseable` con *try-with-resources*.

### Kotlin

```kotlin
class Recurso(val valor: Int) : AutoCloseable {
    override fun close() { /* se libera aquí */ }
}

fun main() {
    val n = readLine()!!.trim().toInt()
    val valor = Recurso(n).use { it.valor }  // use cierra al salir del bloque, incluso con excepción
    println("valor=$valor estado=liberado")
}
```

### Scala

```scala
import scala.util.Using

class Recurso(val valor: Int) extends AutoCloseable {
  def close(): Unit = ()  // se libera aquí
}

object CicloDeVida extends App {
  val n = scala.io.StdIn.readLine().trim.toInt
  val valor = Using.resource(new Recurso(n))(_.valor)
  println(s"valor=$valor estado=liberado")
}
```

### Groovy

```groovy
class Recurso implements Closeable {
    final int valor
    Recurso(int v) { valor = v }
    void close() { /* se libera aquí */ }
}

def n = System.in.newReader().readLine().trim().toInteger()
def valor = new Recurso(n).withCloseable { it.valor }
println("valor=$valor estado=liberado")
```

### Clojure

```clojure
(require '[clojure.string :as str])

(defrecord Recurso [valor]
  java.io.Closeable
  (close [_] nil))  ;; se libera aquí

(let [n (Long/parseLong (str/trim (read-line)))
      valor (with-open [r (->Recurso n)] (:valor r))]
  (println (str "valor=" valor " estado=liberado")))
```

**Qué reconocer:** los cuatro llegan a la **misma interfaz de Java**, `AutoCloseable` / `Closeable`, y
lo que cambia es solo cómo la envuelven: `use` en Kotlin, `Using.resource` en Scala, `withCloseable`
en Groovy, `with-open` en Clojure. Ninguno de los cuatro toca la memoria —de eso sigue encargándose
el recolector de la JVM, y ninguno sabe cuándo actuará—; lo que garantizan es que `close()` se llame
al salir del bloque **aunque salte una excepción**, que es la parte que de verdad importa para
ficheros, sockets y conexiones. Es la separación conceptual más limpia de la página: la **memoria**
la gestiona la máquina y los **recursos** los gestiona el ámbito, dos ciclos de vida distintos que
Java aprendió a separar por las malas cuando `finalize()` resultó ser inservible.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). Mismo diagnóstico que la JVM y misma cura:
`IDisposable` más un bloque que garantiza la llamada.

### F\#

```fsharp
type Recurso(valor: int) =
    member _.Valor = valor
    interface System.IDisposable with
        member _.Dispose() = ()  // se libera aquí

let n = int (stdin.ReadLine().Trim())
let valor =
    use r = new Recurso(n)  // `use` llama a Dispose al salir del ámbito, sin bloque explícito
    r.Valor
printfn "valor=%d estado=liberado" valor
```

### VB.NET

```vbnet
Module CicloDeVida
    Class Recurso
        Implements IDisposable

        Public ReadOnly Valor As Integer

        Public Sub New(v As Integer)
            Valor = v
        End Sub

        Public Sub Dispose() Implements IDisposable.Dispose
            ' se libera aquí
        End Sub
    End Class

    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Dim valor As Integer
        Using r As New Recurso(n)
            valor = r.Valor
        End Using
        Console.WriteLine("valor=" & valor & " estado=liberado")
    End Sub
End Module
```

**Qué reconocer:** VB.NET escribe con palabras lo que C# escribe con símbolos —`Using ... End Using`
es carácter por carácter el mismo `using` de C#, con la misma llamada garantizada a `Dispose`—, y su
`Implements IDisposable.Dispose` obliga a nombrar la interfaz en cada método, un rasgo de la familia
Basic que hace el contrato imposible de pasar por alto. F# introduce el matiz más interesante: su
`use` **no abre un bloque**, sino que ata la vida del recurso al resto del ámbito actual, igual que
una declaración normal. Es el gesto que más se acerca al `let` de Rust dentro de una plataforma con
recolector: se declara y el compilador se encarga del final. Pero la analogía termina ahí, porque
`Dispose` solo cierra el recurso; la memoria del objeto sigue esperando al recolector.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). `malloc` y `free` a mano: el programador *es* la
política de ciclo de vida, y cada fuga es suya.

### C++

```cpp
#include <iostream>
#include <memory>

struct Recurso {
    long valor;
    explicit Recurso(long v) : valor(v) {}
    ~Recurso() { /* RAII: el destructor corre al salir del ámbito, siempre */ }
};

int main() {
    long n;
    std::cin >> n;
    long valor;
    {
        auto r = std::make_unique<Recurso>(n);  // dueño único: no se puede copiar, solo mover
        valor = r->valor;
    }   // aquí se destruye y se libera la memoria
    std::cout << "valor=" << valor << " estado=liberado" << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

@interface Recurso : NSObject
@property (readonly) long valor;
- (instancetype)initConValor:(long)v;
@end

@implementation Recurso
- (instancetype)initConValor:(long)v {
    if ((self = [super init])) { _valor = v; }
    return self;
}
- (void)dealloc { /* ARC llama a dealloc cuando el conteo llega a cero */ }
@end

int main(void) {
    @autoreleasepool {
        long n;
        scanf("%ld", &n);
        long valor;
        @autoreleasepool {
            Recurso *r = [[Recurso alloc] initConValor:n];
            valor = r.valor;
        }   // al cerrar el pool se sueltan las referencias y se libera
        printf("valor=%ld estado=liberado\n", valor);
    }
    return 0;
}
```

**Qué reconocer:** C++ es, con diferencia, **el primo que más se acerca al modelo de Rust**, y no por
casualidad: Rust tomó de aquí la idea. RAII significa que la vida del objeto es la vida del ámbito y
que el destructor corre siempre —al final del bloque, al retornar, al propagarse una excepción—, sin
recolector y sin llamada explícita. `std::unique_ptr` añade la otra mitad: un **dueño único** que no
se puede copiar, solo mover, que es literalmente el `Box<T>` de Rust. Lo que C++ no tiene es el
verificador de préstamos: nada le impide guardar un puntero a algo que ya murió, y ese hueco es la
diferencia entera entre los dos lenguajes. Objective-C ocupa el escalón intermedio: ARC inserta las
llamadas de conteo de referencias en tiempo de compilación, así que `dealloc` es determinista como en
Perl, pero los ciclos siguen siendo fuga salvo que se marquen las referencias como `weak`.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Los dos polos de la
familia: Go recolecta y ordena la limpieza con `defer`; Rust codifica la propiedad en el tipo.

### Zig

```zig
const std = @import("std");

const Recurso = struct {
    valor: i64,
    fn deinit(self: *Recurso) void {
        _ = self;  // Zig no tiene destructores: deinit se llama a mano, por convención con defer
    }
};

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r\t"), 10);
    var valor: i64 = 0;
    {
        var r = Recurso{ .valor = n };
        defer r.deinit();
        valor = r.valor;
    }
    try std.io.getStdOut().writer().print("valor={d} estado=liberado\n", .{valor});
}
```

### Nim

```nim
import std/strutils

type Recurso = object
  valor: int

proc `=destroy`(r: var Recurso) =
  discard  ## con ARC/ORC, Nim sí destruye de forma determinista al salir del ámbito

let n = stdin.readLine().strip().parseInt()
var valor = 0
block:
  let r = Recurso(valor: n)
  valor = r.valor
echo "valor=", valor, " estado=liberado"
```

### D

```d
import std.stdio, std.string, std.conv;

struct Recurso {
    long valor;
    ~this() { /* los struct de D se destruyen al salir del ámbito, como en C++ */ }
}

void main() {
    long n = readln().strip().to!long;
    long valor;
    {
        scope Recurso r = Recurso(n);  // `scope` ata explícitamente la vida al ámbito
        valor = r.valor;
    }
    writeln("valor=", valor, " estado=liberado");
}
```

**Qué reconocer:** conviene decirlo con claridad en vez de fingir equivalencias: **ningún primo de
esta página tiene el modelo de Rust**. Nadie más rastrea la propiedad y los préstamos en el
compilador ni impide en tiempo de compilación usar un valor después de liberarlo. Lo que sí hay son
tres aproximaciones parciales. Zig renuncia a los destructores por completo —la limpieza es un
`deinit()` que tú escribes y un `defer` que tú colocas—; a cambio, no hay código oculto ejecutándose
al final de ningún bloque, que es justamente su principio de diseño. D es un híbrido raro: sus
`struct` se destruyen deterministamente al salir del ámbito como en C++, sus `class` van al
recolector, y `scope` es la palabra que fuerza la primera semántica donde el compilador no la
supondría. Nim es el que más terreno ha ganado: con ARC/ORC sus destructores `=destroy` son
deterministas y la propiedad se transfiere con `sink` y `move`, un eco reconocible de Rust, pero sin
verificador de préstamos que impida el error. En el resto del núcleo —Go, Java, C#, Python— el ciclo
de vida de la **memoria** simplemente no está en el código: lo decide el recolector.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). El ciclo de vida no lo marca el ámbito léxico
sino la transacción o el alcance de la consulta.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    setup_call_cleanup(crear(N, R), usar(R, Valor), liberar(R)),
    format("valor=~w estado=liberado~n", [Valor]).

crear(N, recurso(N)).
usar(recurso(N), N).
liberar(_).   % nada que liberar: los términos son inmutables y los gestiona el sistema
```

### Datalog

```datalog
% Datalog no tiene recursos, ámbitos ni efectos: los hechos viven mientras viva la base.
recurso(5).
recurso(0).
recurso(9).

valor(V) :- recurso(V).
```

**Qué reconocer:** Prolog tiene un equivalente exacto del `with` y del `using`:
`setup_call_cleanup/3` garantiza que la limpieza se ejecute pase lo que pase —incluso si el objetivo
del medio falla o se hace *backtracking*—, y ese predicado es el que usa la biblioteca estándar para
cerrar ficheros y flujos. Pero para los **datos** el problema no existe: los términos son inmutables
y no hay quien los libere a destiempo. Datalog lo lleva al límite y ni siquiera puede expresar el
enunciado: no hay ámbitos, no hay orden temporal, no hay creación ni destrucción; un hecho está en la
base o no está. Es la misma renuncia de SQL, donde el ciclo de vida de una tabla temporal lo decide
la sesión y no ninguna línea del `SELECT`.

---

## Y de vuelta a la clase

Veinte lenguajes y solo tres políticas reales de ciclo de vida: liberación **manual** (C, Zig),
liberación **determinista atada al ámbito** (C++, Rust, D, Nim, y el conteo de referencias de Perl,
PHP y Objective-C) y **recolector** (JVM, .NET, JavaScript, Dart, Ruby, Lua, Go, R). Los del tercer
grupo comparten además el mismo parche —`with`, `use`, `using`, `with-open`, `defer`— porque el
recolector arregla la memoria pero no cierra ficheros. Reconocer a cuál de los tres pertenece un
lenguaje nuevo te dice de antemano qué errores vas a poder cometer en él.

⏮️ [Volver a la clase 103](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
