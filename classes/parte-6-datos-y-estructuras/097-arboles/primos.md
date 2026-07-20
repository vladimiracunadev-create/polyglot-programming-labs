# 🧬 El mismo programa en las familias de lenguajes — Clase 097

> [⬅️ Volver a la clase 097](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —insertar enteros en un árbol binario de búsqueda y
recorrerlo en orden— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Un árbol es la primera estructura **recursiva** del curso: un nodo que contiene otros nodos del
mismo tipo. Lo interesante no es el algoritmo, que es idéntico en los veinte, sino cómo cada familia
dice "aquí puede no haber nada" y quién se hace cargo de la memoria de los nodos.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): enteros distintos separados por espacio
- **Salida** (stdout): `inorden=<los valores ordenados ascendente unidos por ->`
- **Regla:** el recorrido in-order de un árbol binario de búsqueda produce el orden ascendente

| stdin | esperado |
|---|---|
| `3 1 4` | `inorden=1-3-4` |
| `5 2 8 1` | `inorden=1-2-5-8` |
| `9 7` | `inorden=7-9` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Ninguno tiene un tipo "árbol": el nodo se improvisa con la estructura genérica que la familia ya
tiene a mano —diccionario, tabla, lista— y la forma del árbol vive en la convención, no en el tipo.

### Ruby

```ruby
Nodo = Struct.new(:valor, :izq, :der)

def insertar(nodo, v)
  return Nodo.new(v) if nodo.nil?
  if v < nodo.valor
    nodo.izq = insertar(nodo.izq, v)
  else
    nodo.der = insertar(nodo.der, v)
  end
  nodo
end

def inorden(nodo)
  return [] if nodo.nil?
  inorden(nodo.izq) + [nodo.valor] + inorden(nodo.der)
end

raiz = nil
STDIN.read.split.each { |t| raiz = insertar(raiz, t.to_i) }
puts "inorden=" + inorden(raiz).join("-")
```

### Perl

```perl
sub insertar {
    my ($nodo, $v) = @_;
    return { valor => $v, izq => undef, der => undef } unless defined $nodo;
    my $rama = $v < $nodo->{valor} ? 'izq' : 'der';
    $nodo->{$rama} = insertar($nodo->{$rama}, $v);
    return $nodo;
}

sub inorden {
    my ($nodo) = @_;
    return () unless defined $nodo;
    return (inorden($nodo->{izq}), $nodo->{valor}, inorden($nodo->{der}));
}

my @nums = split ' ', do { local $/; <STDIN> };
my $raiz;
$raiz = insertar($raiz, $_) for @nums;
print "inorden=", join('-', inorden($raiz)), "\n";
```

### Lua

```lua
local function insertar(nodo, v)
  if nodo == nil then return { valor = v } end
  if v < nodo.valor then
    nodo.izq = insertar(nodo.izq, v)
  else
    nodo.der = insertar(nodo.der, v)
  end
  return nodo
end

local salida = {}

local function inorden(nodo)
  if nodo == nil then return end
  inorden(nodo.izq)
  salida[#salida + 1] = nodo.valor
  inorden(nodo.der)
end

local raiz = nil
for t in io.read("a"):gmatch("%-?%d+") do
  raiz = insertar(raiz, tonumber(t))
end

inorden(raiz)
print("inorden=" .. table.concat(salida, "-"))
```

### Tcl

```tcl
proc insertar {nodo v} {
    if {$nodo eq ""} { return [list $v "" ""] }
    lassign $nodo valor izq der
    if {$v < $valor} {
        return [list $valor [insertar $izq $v] $der]
    }
    return [list $valor $izq [insertar $der $v]]
}

proc inorden {nodo} {
    if {$nodo eq ""} { return {} }
    lassign $nodo valor izq der
    return [concat [inorden $izq] [list $valor] [inorden $der]]
}

set raiz ""
foreach v [split [string trim [read stdin]]] {
    if {$v ne ""} { set raiz [insertar $raiz $v] }
}
puts "inorden=[join [inorden $raiz] -]"
```

### R

```r
insertar <- function(nodo, v) {
  if (is.null(nodo)) return(list(valor = v, izq = NULL, der = NULL))
  if (v < nodo$valor) nodo$izq <- insertar(nodo$izq, v) else nodo$der <- insertar(nodo$der, v)
  nodo
}

inorden <- function(nodo) {
  if (is.null(nodo)) return(integer(0))
  c(inorden(nodo$izq), nodo$valor, inorden(nodo$der))
}

nums <- scan("stdin", what = integer(), quiet = TRUE)
raiz <- NULL
for (v in nums) raiz <- insertar(raiz, v)
cat(paste0("inorden=", paste(inorden(raiz), collapse = "-"), "\n"))
```

**Qué reconocer:** el nodo es siempre "una bolsa con tres casillas", pero la bolsa cambia de familia:
`Struct` en Ruby, referencia a hash en Perl, tabla en Lua, **lista de tres elementos** en Tcl y lista
con nombres en R. Tcl y R son además **inmutables de hecho**: al no poder mutar el nodo cómodamente,
`insertar` devuelve un árbol nuevo en vez de reescribir el viejo, que es justo lo que hacen Scala y
F# más abajo por convicción y no por comodidad. En los cinco, "no hay nodo" se dice con el valor
vacío del lenguaje (`nil`, `undef`, `""`, `NULL`) y nada impide pasar un número donde iba un nodo:
el error aparecería en tiempo de ejecución.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

class Nodo {
  final int valor;
  Nodo? izq;
  Nodo? der;
  Nodo(this.valor);
}

Nodo insertar(Nodo? n, int v) {
  if (n == null) return Nodo(v);
  if (v < n.valor) {
    n.izq = insertar(n.izq, v);
  } else {
    n.der = insertar(n.der, v);
  }
  return n;
}

void inorden(Nodo? n, List<int> salida) {
  if (n == null) return;
  inorden(n.izq, salida);
  salida.add(n.valor);
  inorden(n.der, salida);
}

void main() {
  final nums = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse);
  Nodo? raiz;
  for (final v in nums) {
    raiz = insertar(raiz, v);
  }
  final salida = <int>[];
  inorden(raiz, salida);
  print('inorden=${salida.join('-')}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra el nodo y el recorrido.
// Uso: var raiz:Nodo = new Nodo(3); raiz.insertar(1); raiz.insertar(4);
//      var s:Array = []; raiz.inorden(s); trace("inorden=" + s.join("-"));
package {
    public class Nodo {
        public var valor:int;
        public var izq:Nodo;
        public var der:Nodo;

        public function Nodo(v:int) {
            valor = v;
        }

        public function insertar(v:int):void {
            if (v < valor) {
                if (izq == null) { izq = new Nodo(v); } else { izq.insertar(v); }
            } else {
                if (der == null) { der = new Nodo(v); } else { der.insertar(v); }
            }
        }

        public function inorden(salida:Array):void {
            if (izq != null) izq.inorden(salida);
            salida.push(valor);
            if (der != null) der.inorden(salida);
        }
    }
}
```

**Qué reconocer:** Dart es el único de los veinte que marca la ausencia **en el tipo**: `Nodo?` es un
tipo distinto de `Nodo`, y el compilador no te deja leer `n.valor` sin comprobar antes que `n` no es
nulo. Es exactamente la garantía que TypeScript ofrece con `Nodo | null` y `strictNullChecks`.
ActionScript 3 es la foto previa a esa idea: los campos `izq` y `der` son `Nodo` a secas y valen
`null` mientras el árbol está incompleto, sin que el tipo lo diga. Nótese también el cambio de
sitio del algoritmo: aquí `insertar` es un **método del nodo** en vez de una función que recibe el
nodo, y el árbol vacío deja de poder representarse (no hay objeto sobre el que llamar al método).

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos comparten el recolector de basura —nadie
libera nodos a mano— y la misma biblioteca estándar, que trae `TreeMap` pero no un árbol binario
que puedas recorrer nodo a nodo.

### Kotlin

```kotlin
class Nodo(val valor: Int) {
    var izq: Nodo? = null
    var der: Nodo? = null
}

fun insertar(n: Nodo?, v: Int): Nodo {
    if (n == null) return Nodo(v)
    if (v < n.valor) n.izq = insertar(n.izq, v) else n.der = insertar(n.der, v)
    return n
}

fun inorden(n: Nodo?): List<Int> =
    if (n == null) emptyList() else inorden(n.izq) + n.valor + inorden(n.der)

fun main() {
    var raiz: Nodo? = null
    for (v in readLine()!!.trim().split(Regex("\\s+")).map(String::toInt)) {
        raiz = insertar(raiz, v)
    }
    println("inorden=" + inorden(raiz).joinToString("-"))
}
```

### Scala

```scala
object Arbol extends App {
  sealed trait Nodo
  case object Vacio extends Nodo
  case class Rama(izq: Nodo, valor: Int, der: Nodo) extends Nodo

  def insertar(n: Nodo, v: Int): Nodo = n match {
    case Vacio => Rama(Vacio, v, Vacio)
    case Rama(i, x, d) if v < x => Rama(insertar(i, v), x, d)
    case Rama(i, x, d) => Rama(i, x, insertar(d, v))
  }

  def inorden(n: Nodo): List[Int] = n match {
    case Vacio => Nil
    case Rama(i, x, d) => inorden(i) ::: x :: inorden(d)
  }

  val nums = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
  val raiz = nums.foldLeft[Nodo](Vacio)(insertar)
  println("inorden=" + inorden(raiz).mkString("-"))
}
```

### Groovy

```groovy
def insertar(nodo, v) {
    if (nodo == null) return [valor: v, izq: null, der: null]
    if (v < nodo.valor) nodo.izq = insertar(nodo.izq, v) else nodo.der = insertar(nodo.der, v)
    nodo
}

def inorden(nodo) {
    nodo == null ? [] : inorden(nodo.izq) + [nodo.valor] + inorden(nodo.der)
}

def raiz = null
System.in.text.split(/\s+/).findAll { it }.each { raiz = insertar(raiz, it as int) }
println "inorden=" + inorden(raiz).join('-')
```

### Clojure

```clojure
(defn insertar [nodo v]
  (cond
    (nil? nodo) {:valor v :izq nil :der nil}
    (< v (:valor nodo)) (update nodo :izq insertar v)
    :else (update nodo :der insertar v)))

(defn inorden [nodo]
  (when nodo
    (concat (inorden (:izq nodo)) [(:valor nodo)] (inorden (:der nodo)))))

(let [nums (map #(Integer/parseInt %) (re-seq #"-?\d+" (slurp *in*)))
      raiz (reduce insertar nil nums)]
  (println (str "inorden=" (clojure.string/join "-" (inorden raiz)))))
```

**Qué reconocer:** cuatro lenguajes sobre la misma máquina virtual y cuatro ideas distintas de qué
**es** un nodo. Kotlin sigue a Java —una clase con dos referencias mutables— pero añade `Nodo?` para
que el compilador exija la comprobación de nulo. Scala da el salto conceptual: el árbol vacío deja
de ser `null` y pasa a ser `Vacio`, un **constructor más del tipo**, así que `match` cubre los dos
casos y el compilador avisa si te dejas uno; a cambio, insertar devuelve un árbol nuevo que comparte
la mayor parte de los nodos con el anterior. Groovy y Clojure renuncian al tipo por completo y usan
mapas: en Clojure `update` recorre y reconstruye el camino sin mutar nada, y `nil` funciona como
árbol vacío porque `(update nil :izq ...)` simplemente crea el mapa que falta.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
type Arbol =
    | Vacio
    | Rama of Arbol * int * Arbol

let rec insertar arbol v =
    match arbol with
    | Vacio -> Rama(Vacio, v, Vacio)
    | Rama(i, x, d) when v < x -> Rama(insertar i v, x, d)
    | Rama(i, x, d) -> Rama(i, x, insertar d v)

let rec inorden arbol =
    match arbol with
    | Vacio -> []
    | Rama(i, x, d) -> inorden i @ [x] @ inorden d

let nums =
    stdin.ReadLine().Split(' ')
    |> Array.filter (fun s -> s <> "")
    |> Array.map int

let raiz = Array.fold insertar Vacio nums
printfn "inorden=%s" (inorden raiz |> List.map string |> String.concat "-")
```

### VB.NET

```vbnet
Imports System
Imports System.Collections.Generic

Module Arbol
    Class Nodo
        Public Valor As Integer
        Public Izq As Nodo
        Public Der As Nodo

        Public Sub New(v As Integer)
            Valor = v
        End Sub
    End Class

    Function Insertar(n As Nodo, v As Integer) As Nodo
        If n Is Nothing Then Return New Nodo(v)
        If v < n.Valor Then
            n.Izq = Insertar(n.Izq, v)
        Else
            n.Der = Insertar(n.Der, v)
        End If
        Return n
    End Function

    Sub Inorden(n As Nodo, salida As List(Of Integer))
        If n Is Nothing Then Return
        Inorden(n.Izq, salida)
        salida.Add(n.Valor)
        Inorden(n.Der, salida)
    End Sub

    Sub Main()
        Dim raiz As Nodo = Nothing
        For Each t In Console.ReadLine().Split(" "c, StringSplitOptions.RemoveEmptyEntries)
            raiz = Insertar(raiz, Integer.Parse(t))
        Next
        Dim salida As New List(Of Integer)
        Inorden(raiz, salida)
        Console.WriteLine("inorden=" & String.Join("-", salida))
    End Sub
End Module
```

**Qué reconocer:** el mismo CLR y la misma distancia que había entre Kotlin y Scala. VB.NET escribe
el árbol como C#: una clase con campos que se reasignan y `Nothing` para el hueco. F# lo escribe como
un **tipo definido por sus dos formas posibles** (`Vacio` y `Rama`), sin `null` en ninguna parte;
`Rama of Arbol * int * Arbol` es la definición recursiva leída en voz alta. El detalle que delata la
plataforma es que ambos tipos acaban siendo objetos en el montón gestionado: nadie escribe un
`Dispose` para liberar el árbol.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Aquí aparece la pregunta que las familias anteriores
no se hacen: **quién libera los nodos**.

### C++

```cpp
#include <iostream>
#include <memory>
#include <string>

struct Nodo {
    int valor;
    std::unique_ptr<Nodo> izq;
    std::unique_ptr<Nodo> der;
    explicit Nodo(int v) : valor(v) {}
};

void insertar(std::unique_ptr<Nodo>& n, int v) {
    if (!n) {
        n = std::make_unique<Nodo>(v);
        return;
    }
    insertar(v < n->valor ? n->izq : n->der, v);
}

void inorden(const std::unique_ptr<Nodo>& n, std::string& salida) {
    if (!n) return;
    inorden(n->izq, salida);
    if (!salida.empty()) salida += '-';
    salida += std::to_string(n->valor);
    inorden(n->der, salida);
}

int main() {
    std::unique_ptr<Nodo> raiz;
    for (int v; std::cin >> v; ) insertar(raiz, v);
    std::string salida;
    inorden(raiz, salida);
    std::cout << "inorden=" << salida << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

@interface Nodo : NSObject
@property (assign) int valor;
@property (strong) Nodo *izq;
@property (strong) Nodo *der;
@end

@implementation Nodo
@end

static Nodo *insertar(Nodo *n, int v) {
    if (n == nil) {
        Nodo *nuevo = [Nodo new];
        nuevo.valor = v;
        return nuevo;
    }
    if (v < n.valor) {
        n.izq = insertar(n.izq, v);
    } else {
        n.der = insertar(n.der, v);
    }
    return n;
}

static void inorden(Nodo *n, NSMutableArray *salida) {
    if (n == nil) return;
    inorden(n.izq, salida);
    [salida addObject:@(n.valor)];
    inorden(n.der, salida);
}

int main(void) {
    @autoreleasepool {
        Nodo *raiz = nil;
        int v;
        while (scanf("%d", &v) == 1) raiz = insertar(raiz, v);
        NSMutableArray *salida = [NSMutableArray array];
        inorden(raiz, salida);
        printf("inorden=%s\n", [[salida componentsJoinedByString:@"-"] UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** en C la versión de la clase reserva cada nodo con `malloc` y el árbol entero
queda sin liberar hasta que el proceso termina. Los dos primos resuelven eso sin recolector de
basura y por caminos distintos: C++ pone la propiedad **en el tipo** —`unique_ptr<Nodo>` dice "este
nodo es mío", y al destruirse la raíz se destruye el árbol completo en cascada— y Objective-C la
pone en el **atributo** —`(strong)` hace que ARC cuente referencias y suelte el nodo cuando el padre
desaparece—. Fíjate en que `insertar` de C++ recibe la referencia al puntero (`&`) porque tiene que
poder rellenar el hueco donde antes no había nada; ese detalle es el mismo `Nodo **` de C, solo que
con el propietario declarado.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Un árbol es la prueba
más dura para un lenguaje de sistemas: son muchas reservas pequeñas y enlazadas.

### Zig

```zig
const std = @import("std");

const Nodo = struct {
    valor: i64,
    izq: ?*Nodo = null,
    der: ?*Nodo = null,
};

fn insertar(alloc: std.mem.Allocator, n: ?*Nodo, v: i64) !*Nodo {
    if (n) |nodo| {
        if (v < nodo.valor) {
            nodo.izq = try insertar(alloc, nodo.izq, v);
        } else {
            nodo.der = try insertar(alloc, nodo.der, v);
        }
        return nodo;
    }
    const nuevo = try alloc.create(Nodo);
    nuevo.* = .{ .valor = v };
    return nuevo;
}

fn inorden(n: ?*Nodo, salida: *std.ArrayList(i64)) !void {
    const nodo = n orelse return;
    try inorden(nodo.izq, salida);
    try salida.append(nodo.valor);
    try inorden(nodo.der, salida);
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const alloc = arena.allocator();

    const entrada = try std.io.getStdIn().reader().readAllAlloc(alloc, 1 << 16);
    var raiz: ?*Nodo = null;
    var it = std.mem.tokenizeAny(u8, entrada, " \t\r\n");
    while (it.next()) |t| {
        raiz = try insertar(alloc, raiz, try std.fmt.parseInt(i64, t, 10));
    }

    var salida = std.ArrayList(i64).init(alloc);
    try inorden(raiz, &salida);

    const out = std.io.getStdOut().writer();
    try out.writeAll("inorden=");
    for (salida.items, 0..) |v, i| {
        if (i > 0) try out.writeByte('-');
        try out.print("{d}", .{v});
    }
    try out.writeByte('\n');
}
```

### Nim

```nim
import std/[strutils, sequtils]

type Nodo = ref object
  valor: int
  izq, der: Nodo

proc insertar(n: Nodo, v: int): Nodo =
  if n == nil: return Nodo(valor: v)
  if v < n.valor: n.izq = insertar(n.izq, v)
  else: n.der = insertar(n.der, v)
  n

proc inorden(n: Nodo): seq[int] =
  if n == nil: return @[]
  inorden(n.izq) & n.valor & inorden(n.der)

var raiz: Nodo
for t in stdin.readAll().splitWhitespace():
  raiz = insertar(raiz, parseInt(t))

echo "inorden=", inorden(raiz).mapIt($it).join("-")
```

### D

```d
import std.stdio, std.conv, std.array, std.algorithm, std.string;

class Nodo {
    int valor;
    Nodo izq, der;
    this(int v) { valor = v; }
}

Nodo insertar(Nodo n, int v) {
    if (n is null) return new Nodo(v);
    if (v < n.valor) n.izq = insertar(n.izq, v);
    else n.der = insertar(n.der, v);
    return n;
}

int[] inorden(Nodo n) {
    if (n is null) return [];
    return inorden(n.izq) ~ n.valor ~ inorden(n.der);
}

void main() {
    Nodo raiz;
    foreach (linea; stdin.byLine)
        foreach (t; linea.split)
            raiz = insertar(raiz, t.to!int);
    writeln("inorden=", inorden(raiz).map!(to!string).join("-"));
}
```

**Qué reconocer:** los tres compilan a binario nativo y los tres tratan la memoria de forma
distinta. Zig es el extremo explícito: el asignador **viaja como parámetro** hasta la función que
crea el nodo, y aquí se elige una *arena* —se libera todo de golpe con `arena.deinit()`, que es la
estrategia natural para un árbol que vive hasta el final del programa—. Además `?*Nodo` obliga a
desempaquetar con `if (n) |nodo|` antes de tocar el nodo, la misma disciplina que `Option<Box<Nodo>>`
en Rust. Nim y D esconden el asunto tras un recolector de basura: `ref object` en Nim y `class` en D
son referencias gestionadas, y por eso su código se parece más al de Java que al de C. El precio de
esa comodidad es el que Rust y Zig se niegan a pagar.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Un árbol en SQL es una tabla con la columna
`padre`, y el recorrido, un `WITH RECURSIVE`.

### Prolog

```prolog
:- initialization(main, main).

% El árbol es un término: vacio, o nodo(Izquierdo, Valor, Derecho).
insertar(vacio, V, nodo(vacio, V, vacio)).
insertar(nodo(I, X, D), V, nodo(I2, X, D)) :- V < X, !, insertar(I, V, I2).
insertar(nodo(I, X, D), V, nodo(I, X, D2)) :- insertar(D, V, D2).

inorden(vacio, []).
inorden(nodo(I, X, D), L) :-
    inorden(I, LI),
    inorden(D, LD),
    append(LI, [X|LD], L).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes),
    exclude(==(""), Partes, Limpias),
    maplist([S, N]>>number_string(N, S), Limpias, Nums),
    foldl([V, A, B]>>insertar(A, V, B), Nums, vacio, Raiz),
    inorden(Raiz, Orden),
    atomic_list_concat(Orden, '-', Texto),
    format("inorden=~w~n", [Texto]).
```

### Datalog

```datalog
% Datalog no tiene símbolos de función: no puede construir nodo(I, V, D) como
% término, ni leer stdin. El árbol se declara como hechos y las relaciones
% derivadas (descendencia) sí se calculan con reglas.
raiz(3).
hijo_izq(3, 1).
hijo_der(3, 4).

hijo(P, H) :- hijo_izq(P, H).
hijo(P, H) :- hijo_der(P, H).

descendiente(P, H) :- hijo(P, H).
descendiente(P, N) :- hijo(P, H), descendiente(H, N).
```

**Qué reconocer:** Prolog es el único de los veinte donde el árbol **es literalmente el dato**:
`nodo(vacio, 3, vacio)` es un término compuesto, y `insertar(nodo(I, X, D), V, ...)` no accede a
campos sino que **unifica** la cabeza de la regla con la forma del árbol. Es el mismo mecanismo que
Scala y F# llaman "coincidencia de patrones", pero aquí es el motor del lenguaje, no una
construcción añadida. Datalog marca el límite exacto: al prohibir los símbolos de función para
garantizar que toda consulta termina, pierde la capacidad de tener un árbol como valor, y solo puede
hablar de él como relación padre-hijo. Esa renuncia es la misma que hace SQL cuando modela una
jerarquía con una columna `padre` en vez de con estructuras anidadas.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo árbol, y el mismo algoritmo recursivo en todos: comparar con la raíz, bajar
por una rama, recorrer izquierda-raíz-derecha. Lo que separa a las familias es qué garantías te da el
tipo antes de ejecutar —si el hueco vacío está declarado o es un `null` silencioso— y quién se hace
cargo de la memoria de los nodos. Eso es lo transferible.

⏮️ [Volver a la clase 097](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
