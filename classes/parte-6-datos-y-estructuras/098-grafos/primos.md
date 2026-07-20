# 🧬 El mismo programa en las familias de lenguajes — Clase 098

> [⬅️ Volver a la clase 098](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —leer un grafo como lista de aristas y contar
aristas y nodos distintos— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Hay un dato que conviene decir de entrada: **ninguno de los veinte lenguajes trae un tipo grafo en
su biblioteca estándar**. Ni uno. Todos construyen el grafo con las dos piezas que sí tienen —un
diccionario y una lista— y la decisión real no es de lenguaje sino de representación: lista de
aristas o lista de adyacencia.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): pares de enteros; cada par es una arista
- **Salida** (stdout): `aristas=<número de pares> nodos=<nodos distintos>`
- **Regla:** `aristas = tokens / 2` y `nodos = |conjunto de todos los números|`

| stdin | esperado |
|---|---|
| `1 2 2 3` | `aristas=2 nodos=3` |
| `1 2` | `aristas=1 nodos=2` |
| `1 2 2 3 3 1` | `aristas=3 nodos=3` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
El diccionario es la estructura reina de esta familia, así que la lista de adyacencia sale casi
sola: la clave es el nodo, el valor es la lista de vecinos, y el número de claves ya es el número de
nodos distintos.

### Ruby

```ruby
tokens = STDIN.read.split.map(&:to_i)
aristas = tokens.each_slice(2).select { |par| par.size == 2 }

ady = Hash.new { |h, k| h[k] = [] }
aristas.each do |a, b|
  ady[a] << b
  ady[b] << a
end

puts "aristas=#{aristas.size} nodos=#{ady.size}"
```

### Perl

```perl
my @tokens = split ' ', do { local $/; <STDIN> };
my %ady;
my $aristas = 0;

while (my ($a, $b) = splice(@tokens, 0, 2)) {
    last unless defined $b;
    push @{ $ady{$a} }, $b;
    push @{ $ady{$b} }, $a;
    $aristas++;
}

printf "aristas=%d nodos=%d\n", $aristas, scalar keys %ady;
```

### Lua

```lua
local ady, nodos, aristas = {}, 0, 0
local pendiente = nil

for t in io.read("a"):gmatch("%-?%d+") do
  local n = tonumber(t)
  -- Lua no sabe contar las claves de una tabla asociativa: se cuenta a mano.
  if ady[n] == nil then
    ady[n] = {}
    nodos = nodos + 1
  end
  if pendiente == nil then
    pendiente = n
  else
    table.insert(ady[pendiente], n)
    table.insert(ady[n], pendiente)
    aristas = aristas + 1
    pendiente = nil
  end
end

print(string.format("aristas=%d nodos=%d", aristas, nodos))
```

### Tcl

```tcl
set tokens [regexp -all -inline {-?\d+} [read stdin]]
set ady [dict create]
set aristas 0

foreach {a b} $tokens {
    dict lappend ady $a $b
    dict lappend ady $b $a
    incr aristas
}

puts "aristas=$aristas nodos=[dict size $ady]"
```

### R

```r
nums <- scan("stdin", what = integer(), quiet = TRUE)
# En R la lista de aristas es, literalmente, una matriz de dos columnas.
aristas <- matrix(nums, ncol = 2, byrow = TRUE)
cat(sprintf("aristas=%d nodos=%d\n", nrow(aristas), length(unique(nums))))
```

**Qué reconocer:** Ruby, Perl y Tcl escriben la misma frase con distinto acento —`Hash.new` con
bloque por defecto, `push @{ $ady{$a} }` que **autovivifica** el array si no existía, y
`dict lappend` que hace lo mismo en una palabra—. Lua delata su minimalismo: sus tablas no llevan
cuenta de cuántas claves no numéricas tienen (`#ady` solo funciona sobre secuencias), así que hay
que contar los nodos a mano, y esa incomodidad es la que empuja a la comunidad de Lua a preferir
listas de aristas. R cambia de representación por completo: no construye adyacencia, sino una
**matriz de dos columnas**, porque en R la unidad natural es la tabla y no el diccionario. Es el
mismo grafo con otra forma, y el conteo sale de `nrow` y `unique` sin bucle alguno.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final nums = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  final ady = <int, List<int>>{};
  var aristas = 0;

  for (var i = 0; i + 1 < nums.length; i += 2) {
    ady.putIfAbsent(nums[i], () => []).add(nums[i + 1]);
    ady.putIfAbsent(nums[i + 1], () => []).add(nums[i]);
    aristas++;
  }

  print('aristas=$aristas nodos=${ady.length}');
}
```

### ActionScript 3

```actionscript
// Sin stdin en el reproductor Flash: la lista de aristas llega ya como Array.
package {
    public class Grafo {
        public static function resumen(tokens:Array):String {
            // Object como diccionario: las claves se convierten a String.
            var ady:Object = {};
            var nodos:int = 0;
            var aristas:int = 0;

            for (var i:int = 0; i + 1 < tokens.length; i += 2) {
                var a:int = tokens[i];
                var b:int = tokens[i + 1];
                if (ady[a] == null) { ady[a] = []; nodos++; }
                if (ady[b] == null) { ady[b] = []; nodos++; }
                ady[a].push(b);
                ady[b].push(a);
                aristas++;
            }

            return "aristas=" + aristas + " nodos=" + nodos;
        }
    }
}
```

**Qué reconocer:** Dart usa un `Map<int, List<int>>` con clave entera de verdad, igual que el `Map`
de JavaScript moderno. ActionScript 3 conserva el objeto-como-diccionario de la era pre-`Map`, donde
**toda clave se convierte a cadena** por debajo: `ady[1]` y `ady["1"]` son la misma casilla. Ese
detalle es exactamente la trampa del objeto plano en JavaScript que la clase del núcleo evita usando
`Set` y `Map`. Fíjate también en `putIfAbsent` de Dart: es el mismo gesto de "dame la lista, y si no
existe créala" que en Ruby resolvía el bloque por defecto del `Hash`.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La biblioteca de Java trae `HashMap`,
`HashSet` y `TreeMap`, pero ningún grafo: quien quiere uno de verdad recurre a JGraphT, que es una
biblioteca externa.

### Kotlin

```kotlin
fun main() {
    val nums = readLine()!!.trim().split(Regex("\\s+")).map(String::toInt)
    val aristas = nums.chunked(2).filter { it.size == 2 }
    val ady = mutableMapOf<Int, MutableList<Int>>()

    for (par in aristas) {
        val (a, b) = par
        ady.getOrPut(a) { mutableListOf() }.add(b)
        ady.getOrPut(b) { mutableListOf() }.add(a)
    }

    println("aristas=${aristas.size} nodos=${ady.size}")
}
```

### Scala

```scala
object Grafo extends App {
  val nums = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
  val aristas = nums.grouped(2).collect { case Array(a, b) => (a, b) }.toList

  val ady = aristas.foldLeft(Map.empty[Int, List[Int]]) { case (m, (a, b)) =>
    val con_a = m.updated(a, b :: m.getOrElse(a, Nil))
    con_a.updated(b, a :: con_a.getOrElse(b, Nil))
  }

  println(s"aristas=${aristas.size} nodos=${ady.size}")
}
```

### Groovy

```groovy
def nums = System.in.text.split(/\s+/).findAll { it }*.toInteger()
def aristas = nums.collate(2).findAll { it.size() == 2 }
def ady = [:].withDefault { [] }

aristas.each { a, b ->
    ady[a] << b
    ady[b] << a
}

println "aristas=${aristas.size()} nodos=${ady.size()}"
```

### Clojure

```clojure
(let [nums (map #(Integer/parseInt %) (re-seq #"-?\d+" (slurp *in*)))
      aristas (partition 2 nums)
      ady (reduce (fn [m [a b]]
                    (-> m
                        (update a conj b)
                        (update b conj a)))
                  {} aristas)]
  (println (str "aristas=" (count aristas) " nodos=" (count ady))))
```

**Qué reconocer:** los cuatro parten la entrada en pares con la misma operación bajo cuatro nombres
—`chunked`, `grouped`, `collate`, `partition`— y esa es la señal de que estás ante la misma familia
de colecciones. La diferencia de fondo es la mutabilidad: Kotlin y Groovy **mutan** un mapa que ya
existe (`getOrPut`, `withDefault`), mientras que Scala y Clojure **reconstruyen** el mapa en cada
arista con `foldLeft` y `reduce`, y aun así no copian nada, porque sus mapas persistentes comparten
la estructura interna. Nótese el truco de Clojure: `(update m a conj b)` sobre una clave ausente
aplica `conj` a `nil`, que devuelve una lista de un elemento, así que no hace falta inicializar nada.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let nums =
    stdin.ReadLine().Split(' ')
    |> Array.filter (fun s -> s <> "")
    |> Array.map int

let aristas =
    nums
    |> Array.chunkBySize 2
    |> Array.filter (fun par -> par.Length = 2)
    |> Array.map (fun par -> (par.[0], par.[1]))

let agregar (m: Map<int, int list>) k v =
    m.Add(k, v :: (m.TryFind k |> Option.defaultValue []))

let ady =
    aristas
    |> Array.fold (fun m (a, b) -> agregar (agregar m a b) b a) Map.empty

printfn "aristas=%d nodos=%d" aristas.Length ady.Count
```

### VB.NET

```vbnet
Imports System
Imports System.Collections.Generic
Imports System.Linq

Module Grafo
    Sub Main()
        Dim nums = Console.ReadLine().Split(" "c, StringSplitOptions.RemoveEmptyEntries).
            Select(Function(s) Integer.Parse(s)).ToArray()

        Dim ady As New Dictionary(Of Integer, List(Of Integer))
        Dim aristas = 0

        For i = 0 To nums.Length - 2 Step 2
            For Each n In {nums(i), nums(i + 1)}
                If Not ady.ContainsKey(n) Then ady(n) = New List(Of Integer)
            Next
            ady(nums(i)).Add(nums(i + 1))
            ady(nums(i + 1)).Add(nums(i))
            aristas += 1
        Next

        Console.WriteLine($"aristas={aristas} nodos={ady.Count}")
    End Sub
End Module
```

**Qué reconocer:** `Dictionary(Of Integer, List(Of Integer))` de VB.NET y el `Map<int, int list>` de
F# son el mismo concepto con garantías opuestas: el primero se modifica en el sitio y admite que
otro hilo lo toque a la vez; el segundo devuelve un mapa nuevo en cada `Add` y nunca cambia. En
VB.NET destaca la ausencia de un "dame o crea" —hay que preguntar con `ContainsKey` antes de
insertar, tres líneas donde Kotlin tenía una—, y en F# esa carencia se cubre escribiendo la función
`agregar` a mano. Ninguno de los dos tiene grafo en la biblioteca; `System.Collections.Generic` llega
hasta el diccionario y ahí se detiene.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). En C no hay ni diccionario: la versión de la clase
tiene que contar los nodos distintos recorriendo un array a mano.

### C++

```cpp
#include <iostream>
#include <map>
#include <vector>

int main() {
    // std::map es un árbol equilibrado (clase 097): las claves quedan ordenadas.
    std::map<int, std::vector<int>> ady;
    int a, b, aristas = 0;

    while (std::cin >> a >> b) {
        ady[a].push_back(b);
        ady[b].push_back(a);
        ++aristas;
    }

    std::cout << "aristas=" << aristas << " nodos=" << ady.size() << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSMutableDictionary<NSNumber *, NSMutableArray *> *ady = [NSMutableDictionary dictionary];
        int a, b, aristas = 0;

        while (scanf("%d %d", &a, &b) == 2) {
            for (NSNumber *n in @[@(a), @(b)]) {
                if (ady[n] == nil) ady[n] = [NSMutableArray array];
            }
            [ady[@(a)] addObject:@(b)];
            [ady[@(b)] addObject:@(a)];
            aristas++;
        }

        printf("aristas=%d nodos=%lu\n", aristas, (unsigned long)ady.count);
    }
    return 0;
}
```

**Qué reconocer:** lo que en C costaba un bucle de búsqueda lineal, aquí lo resuelve una línea,
porque ambos primos sí traen diccionario. La diferencia entre ellos es reveladora: `ady[a]` en C++
**crea el vector vacío si la clave no existía** —el `operator[]` de `std::map` inserta por
defecto—, mientras que `NSMutableDictionary` devuelve `nil` y hay que crear el array
explícitamente; y como `nil` en Objective-C acepta mensajes sin fallar, olvidarlo no da error, solo
pierde datos en silencio. Otro detalle de familia: el diccionario de Objective-C no puede guardar un
`int`, hay que **envolverlo** en `NSNumber` con `@(a)`, porque las colecciones de Foundation solo
almacenan objetos.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Aquí el grafo obliga a
decidir dónde vive cada lista de vecinos.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const alloc = arena.allocator();

    const entrada = try std.io.getStdIn().reader().readAllAlloc(alloc, 1 << 16);
    var ady = std.AutoHashMap(i64, std.ArrayList(i64)).init(alloc);
    var aristas: usize = 0;

    var it = std.mem.tokenizeAny(u8, entrada, " \t\r\n");
    while (it.next()) |ta| {
        const tb = it.next() orelse break;
        const a = try std.fmt.parseInt(i64, ta, 10);
        const b = try std.fmt.parseInt(i64, tb, 10);

        for ([_][2]i64{ .{ a, b }, .{ b, a } }) |par| {
            const gop = try ady.getOrPut(par[0]);
            if (!gop.found_existing) gop.value_ptr.* = std.ArrayList(i64).init(alloc);
            try gop.value_ptr.append(par[1]);
        }
        aristas += 1;
    }

    try std.io.getStdOut().writer().print("aristas={d} nodos={d}\n", .{ aristas, ady.count() });
}
```

### Nim

```nim
import std/[strutils, sequtils, tables]

let nums = stdin.readAll().splitWhitespace().map(parseInt)
var ady = initTable[int, seq[int]]()
var aristas = 0

for i in countup(0, nums.len - 2, 2):
  ady.mgetOrPut(nums[i], @[]).add(nums[i + 1])
  ady.mgetOrPut(nums[i + 1], @[]).add(nums[i])
  inc aristas

echo "aristas=", aristas, " nodos=", ady.len
```

### D

```d
import std.stdio, std.conv, std.array, std.algorithm, std.string, std.range;

void main() {
    int[] nums;
    foreach (linea; stdin.byLine)
        foreach (t; linea.split)
            nums ~= t.to!int;

    // int[][int]: array asociativo de int a array de int, sintaxis nativa de D.
    int[][int] ady;
    size_t aristas;

    foreach (par; nums.chunks(2)) {
        if (par.length < 2) break;
        ady[par[0]] ~= par[1];
        ady[par[1]] ~= par[0];
        aristas++;
    }

    writefln("aristas=%d nodos=%d", aristas, ady.length);
}
```

**Qué reconocer:** el asociativo está en el lenguaje mismo en D (`int[][int]` es sintaxis, no
biblioteca) y en la biblioteca estándar en Nim y Zig, pero el gesto es el mismo que en Go con
`map[int][]int`. Zig vuelve a ser el más explícito: `getOrPut` devuelve un puntero a la casilla y un
booleano que dice si ya existía, así que **tú** decides qué poner cuando no existía —una sola
consulta a la tabla, sin buscar dos veces—; `mgetOrPut` de Nim es la misma idea con el valor por
defecto ya dado. Y como todas las listas de vecinos se reservan del mismo asignador de arena, aquí
tampoco hace falta liberar una por una: se sueltan todas al final. Ninguno de los tres, otra vez,
tiene grafo en la biblioteca estándar.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Una tabla `arista(origen, destino)` es
exactamente una lista de aristas, y contar nodos distintos es un `COUNT(DISTINCT ...)`.

### Prolog

```prolog
:- initialization(main, main).
:- dynamic arista/2.

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes),
    exclude(==(""), Partes, Limpias),
    maplist([S, N]>>number_string(N, S), Limpias, Nums),
    afirmar_aristas(Nums),
    aggregate_all(count, arista(_, _), Aristas),
    setof(N, A^B^(arista(A, B), (N = A ; N = B)), Nodos),
    length(Nodos, Cuantos),
    format("aristas=~w nodos=~w~n", [Aristas, Cuantos]).

afirmar_aristas([]).
afirmar_aristas([A, B | Resto]) :-
    assertz(arista(A, B)),
    afirmar_aristas(Resto).

% Con las aristas como hechos, la conectividad son dos líneas más:
conecta(A, B) :- arista(A, B).
conecta(A, B) :- arista(B, A).
alcanza(A, B) :- conecta(A, B).
alcanza(A, C) :- conecta(A, B), alcanza(B, C).
```

### Datalog

```datalog
% Datalog no lee stdin y no agrega: contar no es una operación del lenguaje puro,
% hace falta una extensión. Lo que sí es nativo es la clausura transitiva.
arista(1, 2).
arista(2, 3).

nodo(X) :- arista(X, _).
nodo(Y) :- arista(_, Y).

conecta(A, B) :- arista(A, B).
conecta(A, B) :- arista(B, A).

alcanza(A, B) :- conecta(A, B).
alcanza(A, C) :- conecta(A, B), alcanza(B, C).
```

**Qué reconocer:** aquí se invierte el reparto. Los dieciocho lenguajes anteriores tenían fácil
contar y difícil consultar; estos dos tienen difícil contar —Prolog necesita `aggregate_all` y
Datalog puro directamente no puede— y trivial lo demás. Un grafo en Prolog **son hechos**:
`arista(1, 2)` no es una estructura de datos que tú recorres, es una afirmación en la base de
conocimiento, y el motor la indexa y la busca por ti. Por eso la alcanzabilidad cabe en dos reglas
recursivas, sin cola, sin visitados y sin bucle, mientras que en Go o en Rust sería un BFS de treinta
líneas. Esa es también la razón de que `WITH RECURSIVE` exista en SQL: es el mismo cálculo de punto
fijo que Datalog hace por defecto.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo grafo, y ni una sola biblioteca estándar que lo traiga hecho. Lo que
cambia no es el algoritmo sino la **representación** que cada comunidad considera natural —matriz en
R, diccionario de listas en casi todos, hechos en Prolog— y hasta dónde llega el diccionario que el
lenguaje te da gratis. Eso es lo transferible.

⏮️ [Volver a la clase 098](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
