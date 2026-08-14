# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 098

> [⬅️ Volver a la clase 098](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Una lista de aristas, y dos preguntas sobre ella. El grafo es la estructura que ningún lenguaje trae
hecha —**ninguno de estos doce tiene un tipo grafo**, y los modernos tampoco— porque no hay una sola
representación correcta: lista de adyacencia, matriz de adyacencia o lista de aristas, y la elección
depende de la densidad. Lo que sí cambia entre estos lenguajes es **cuál de las tres es natural
escribir**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **representación de relaciones**, y estos lenguajes lo enseñan por lo que
> empujan. **Fortran** empuja hacia la **matriz de adyacencia**, porque su estructura natural es el
> arreglo denso y sus operaciones de matriz resuelven caminos y componentes con álgebra lineal.
> **M** empuja hacia la **lista de adyacencia**, porque su array multinivel es exactamente eso.
> **COBOL y RPG** empujan hacia la **lista de aristas**, porque es lo que cabe en un fichero.
>
> Y **M** aporta el hecho más llamativo de la página: un grafo en M **es una base de datos de grafos**,
> persistente y transaccional, sin ninguna capa intermedia.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con pares de enteros (cada par es una arista) → stdout: `aristas=<número de pares> nodos=<nodos distintos>`
- **Regla:** `aristas = tokens/2 ; nodos = |conjunto de todos los números|`

| stdin | esperado |
|---|---|
| `1 2 2 3` | `aristas=2 nodos=3` |
| `1 2` | `aristas=1 nodos=2` |
| `1 2 2 3 3 1` | `aristas=3 nodos=3` |

> **Qué está verificado en esta página.** Los lenguajes de la sección 🟢 se **ejecutan en CI**
> contra este mismo `casos.json`, igual que las diez implementaciones del núcleo
> ([workflow Labs](../../../labs/README.md)). Los de la sección 🟡 **no pueden** cumplir este
> contrato sin falsear el lenguaje, y se explica por qué. Los de la sección ⚪ sí podrían, pero
> su cadena de herramientas no está en los *runners*: son correctos, sin sello de máquina.

---

## 🟢 Se ejecutan en CI

### COBOL

[Ficha completa](../../../atlas/cobol.md) · Banca, seguros, gobierno, medios de pago · `cobc -x -free prog.cob`

```cobol
IDENTIFICATION DIVISION.
PROGRAM-ID. GRAFO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(2) COMP VALUE 0.
01  I       PIC 9(4) COMP.
01  J       PIC 9(4) COMP.
01  NT      PIC 9(4) COMP VALUE 0.
01  NN      PIC 9(4) COMP VALUE 0.
01  VALOR   PIC S9(9) COMP-3.
01  NUEVO   PIC X VALUE "S".
01  NODOS.
    05  NODO  PIC S9(9) COMP-3 OCCURS 200 TIMES.
01  ED-A    PIC Z(3)9.
01  ED-N    PIC Z(3)9.
01  ARISTAS PIC 9(4) COMP.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE SPACES TO TOKEN
    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        IF LINEA(I:1) = SPACE
            PERFORM CERRAR-TOKEN
        ELSE
            ADD 1 TO TLEN
            MOVE LINEA(I:1) TO TOKEN(TLEN:1)
        END-IF
    END-PERFORM
    PERFORM CERRAR-TOKEN

    COMPUTE ARISTAS = NT / 2
    MOVE ARISTAS TO ED-A
    MOVE NN      TO ED-N
    DISPLAY "aristas=" FUNCTION TRIM(ED-A)
            " nodos="  FUNCTION TRIM(ED-N)
    STOP RUN.

CERRAR-TOKEN.
    IF TLEN > 0
        ADD 1 TO NT
        COMPUTE VALOR = FUNCTION NUMVAL(TOKEN)
        MOVE "S" TO NUEVO
        PERFORM VARYING J FROM 1 BY 1 UNTIL J > NN
            IF NODO(J) = VALOR
                MOVE "N" TO NUEVO
            END-IF
        END-PERFORM
        IF NUEVO = "S"
            ADD 1 TO NN
            MOVE VALOR TO NODO(NN)
        END-IF
        MOVE SPACES TO TOKEN
        MOVE 0 TO TLEN
    END-IF.
```

**Lo que esta clase enseña en COBOL.** La representación natural en COBOL es **la lista de aristas**,
y no es una limitación: es **exactamente el formato de un fichero de relaciones**.

```cobol
01  ARISTA.
    05  ORIGEN   PIC 9(9).
    05  DESTINO  PIC 9(9).
    05  PESO     PIC S9(7)V99 COMP-3.
```

Un fichero con esa estructura, ordenado por origen, **es una lista de adyacencia en disco**: leer
secuencialmente da todos los vecinos de cada nodo agrupados. Y ordenarlo es una llamada a la utilidad
SORT.

Ese patrón —**ordenar por clave y procesar por grupos**— es la técnica fundamental del procesamiento
por lotes, y resuelve en mainframe cosas que parecen exigir un grafo en memoria:

```text
SORT por ORIGEN → leer secuencial → al cambiar ORIGEN, cerrar el grupo anterior
```

Es lo que en COBOL se llama **proceso por ruptura de control**, y RPG lo tenía automatizado en su
ciclo (clase 092). Con dos ficheros ordenados y un recorrido simultáneo —el *balanced line
algorithm*— se hacen uniones, intersecciones y recorridos que en memoria requerirían estructuras
complejas.

Y hay una razón por la que esto sigue siendo relevante: **funciona con datos que no caben en
memoria**. Un grafo de mil millones de aristas se procesa así, en un solo pase, con memoria constante.
Es el mismo principio que hay detrás de MapReduce, y por eso los algoritmos de grafos a gran escala
—PageRank incluido— se expresan como series de ordenaciones y recorridos.

Para grafos que sí caben, COBOL usa una tabla de adyacencia con `OCCURS` anidados:

```cobol
01  ADYACENCIA.
    05  VECINO-DE OCCURS 1000 TIMES.
        10  CUANTOS  PIC 9(4) COMP.
        10  VECINO   PIC 9(9) OCCURS 1 TO 100 DEPENDING ON CUANTOS.
```

Un `OCCURS DEPENDING ON` dentro de un `OCCURS` (clase 090): la lista de adyacencia, escrita en COBOL.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program grafo
   implicit none
   integer :: v(200), n, ios, i, j, nodos
   character(len=400) :: linea
   logical :: repetido

   read(*, '(A)') linea

   n = 0
   do i = 1, 200
      read(linea, *, iostat=ios) v(1:i)
      if (ios /= 0) exit
      n = i
   end do

   nodos = 0
   do i = 1, n
      repetido = .false.
      do j = 1, i - 1
         if (v(j) == v(i)) repetido = .true.
      end do
      if (.not. repetido) nodos = nodos + 1
   end do

   write(*, '(A,I0,A,I0)') 'aristas=', n / 2, ' nodos=', nodos
end program grafo
```

**Lo que esta clase enseña en Fortran.** Fortran empuja hacia **la matriz de adyacencia**, y esa
inclinación no es casual: cuando el grafo es una matriz, **los algoritmos de grafos se convierten en
álgebra lineal**, que es lo que Fortran hace mejor que nadie.

```fortran
logical :: a(n, n)          ! adyacencia
integer :: g(n, n)          ! con pesos

a(i, j) = .true.
grado = count(a(i, :))                       ! el grado de i, sin bucle
alcanzable_en_2 = matmul(a, a)               ! caminos de longitud 2
```

Esa última línea es el hecho central: **la potencia k-ésima de la matriz de adyacencia cuenta los
caminos de longitud k**. Con eso se resuelven alcanzabilidad, componentes conexas y cierre transitivo
con multiplicaciones de matrices — y multiplicar matrices es exactamente donde Fortran y sus
bibliotecas son imbatibles.

Sobre esa idea está construido **GraphBLAS**, el estándar moderno para algoritmos de grafos como
álgebra lineal sobre semianillos: BFS, camino más corto, triángulos y PageRank expresados como
productos matriz-vector. Es una formulación de los años setenta que volvió con fuerza al llegar las
GPU, porque **una multiplicación de matrices se paraleliza y un recorrido con punteros no**.

Y hay una advertencia de rendimiento que esta clase es buen sitio para dar: **una matriz de
adyacencia de un grafo disperso es un desperdicio brutal**. Un millón de nodos con diez aristas cada
uno ocupa 10⁷ aristas y una matriz de 10¹² celdas.

Por eso el formato real en cálculo científico no es la matriz densa sino **CSR** (*Compressed Sparse
Row*): tres arreglos —valores, índices de columna y punteros de fila— que son, en el fondo, **una
lista de adyacencia empaquetada en arreglos contiguos**.

```fortran
integer :: fila(n+1), columna(nnz)
real    :: valor(nnz)
```

Ese formato lo inventó la comunidad Fortran para matrices dispersas en los años setenta, y hoy es el
formato interno de SciPy, de cuSPARSE y de la mitad de las bibliotecas de grafos que existen.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Containers.Ordered_Sets;

procedure Grafo is
   package Conjuntos is new Ada.Containers.Ordered_Sets (Element_Type => Integer);
   use Conjuntos;

   Nodos  : Set;
   Tokens : Natural := 0;

   Linea  : String (1 .. 400);
   Ultimo : Natural;
   Pos    : Integer := 1;
   Valor  : Integer;
   Fin    : Positive;
begin
   Get_Line (Linea, Ultimo);

   loop
      while Pos <= Ultimo and then Linea (Pos) = ' ' loop
         Pos := Pos + 1;
      end loop;
      exit when Pos > Ultimo;

      Get (Linea (Pos .. Ultimo), Valor, Fin);
      Tokens := Tokens + 1;
      Nodos.Include (Valor);
      Pos := Fin + 1;
   end loop;

   Put ("aristas=");
   Put (Tokens / 2, Width => 1);
   Put (" nodos=");
   Put (Integer (Nodos.Length), Width => 1);
   New_Line;
end Grafo;
```

**Lo que esta clase enseña en Ada.** Ada no tiene grafos en `Ada.Containers`, y sí tiene las piezas:
`Vectors` de `Vectors` para la lista de adyacencia, `Hashed_Maps` cuando los nodos no son enteros
densos, y arreglos bidimensionales para la matriz.

Lo interesante en Ada es que **el tipo del nodo puede ser un tipo propio**, no un entero suelto:

```ada
type Id_Nodo is new Positive range 1 .. 10_000;
type Matriz is array (Id_Nodo, Id_Nodo) of Boolean;
package Adyacencia is new Ada.Containers.Vectors (Positive, Id_Nodo);
```

`Id_Nodo` **no es intercambiable con `Integer`**: sumarle un contador sin conversión explícita no
compila. En un programa con identificadores de nodo, de arista y de componente, esa distinción evita
la clase entera de errores en que se pasa el índice equivocado — que en C, donde todos son `int`, es
invisible hasta que falla.

Y hay una construcción de Ada especialmente adecuada para grafos y poco conocida: **el arreglo
bidimensional con índices de tipos distintos**.

```ada
type Origen  is (A, B, C);
type Destino is (X, Y, Z);
type Coste is array (Origen, Destino) of Natural;
```

Un grafo bipartito donde **es imposible confundir un lado con el otro**, comprobado en compilación.

Sobre el rendimiento, Ada permite empaquetar la matriz de adyacencia a un bit por celda con
`pragma Pack`, igual que el conjunto de la clase 094:

```ada
type Fila is array (Id_Nodo) of Boolean;
pragma Pack (Fila);
```

Con eso, una matriz de 10 000 × 10 000 ocupa 12 MB en lugar de 100, y las operaciones de fila se hacen
con `and`, `or` y `xor` sobre palabras completas. Es la representación de conjunto de bits aplicada a
grafos, que es exactamente lo que hacen las bibliotecas de análisis de programas para calcular
alcanzabilidad.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Grafo;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Nodos: array of Integer;
  Linea, Tok: string;
  I, J, Tokens, Valor: Integer;
  C: Char;
  Repetido: Boolean;

begin
  ReadLn(Linea);

  SetLength(Nodos, 0);
  Tokens := 0;
  Tok := '';

  for I := 1 to Length(Linea) + 1 do
  begin
    if I <= Length(Linea) then C := Linea[I] else C := ' ';
    if C = ' ' then
    begin
      if Tok <> '' then
      begin
        Inc(Tokens);
        Valor := StrToInt(Tok);
        Repetido := False;
        for J := 0 to High(Nodos) do
          if Nodos[J] = Valor then Repetido := True;
        if not Repetido then
        begin
          SetLength(Nodos, Length(Nodos) + 1);
          Nodos[High(Nodos)] := Valor;
        end;
        Tok := '';
      end;
    end
    else
      Tok := Tok + C;
  end;

  WriteLn('aristas=', IntToStr(Tokens div 2),
          ' nodos=', IntToStr(Length(Nodos)));
end.
```

**Lo que esta clase enseña en Pascal.** Pascal tiene una representación de grafos que es propia y que
aprovecha el tipo conjunto de la clase 094: **un arreglo de conjuntos**.

```pascal
type
  TNodo = 0..255;
  TVecinos = set of TNodo;
  TGrafo = array[TNodo] of TVecinos;

var
  G: TGrafo;
begin
  G[3] := G[3] + [7];              { añadir la arista 3→7 }
  if 7 in G[3] then ...             { ¿existe la arista? -- O(1) }
  Comunes := G[3] * G[5];           { vecinos COMUNES: intersección }
  Grado := 0;
  for N := Low(TNodo) to High(TNodo) do
    if N in G[3] then Inc(Grado);
end;
```

Cada fila es una máscara de bits de 256 bits —32 bytes—, así que el grafo entero de 256 nodos ocupa
**8 KB** y la pregunta "¿son vecinos?" es una comprobación de bit.

Y `G[3] * G[5]` —los vecinos comunes de dos nodos— es una operación de máscara de bits sobre cuatro
palabras. Ese cálculo es el núcleo del **conteo de triángulos** y del coeficiente de agrupamiento, y
aquí sale en una línea.

Es una representación excelente para grafos pequeños y densos, y **el límite de 256 elementos** es
otra vez el techo del `set` de Pascal.

Para grafos generales, Free Pascal moderno usa `Generics.Collections`:

```pascal
type
  TAdyacencia = specialize TDictionary<Integer, specialize TList<Integer>>;
```

Esa palabra **`specialize`** es la sintaxis de genéricos del modo ObjFPC —Delphi usa `<>` a secas— y
es una de las divergencias más visibles entre los dos dialectos. Anidar genéricos con `specialize`
resulta francamente verboso, y es una de las críticas habituales al modo ObjFPC frente al modo Delphi.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((tokens '()))
  (loop for x = (read *standard-input* nil nil)
        while x
        do (push x tokens))
  (format t "aristas=~D nodos=~D~%"
          (floor (length tokens) 2)
          (length (remove-duplicates tokens))))
```

**Lo que esta clase enseña en Common Lisp.** La representación idiomática en Lisp es **la lista de
adyacencia como lista de asociación** (clase 095), y es directa hasta el punto de que el grafo se
escribe como un literal:

```lisp
(defparameter *grafo*
  '((a b c)          ; a es vecino de b y c
    (b c)
    (c a)))

(cdr (assoc 'a *grafo*))          ; los vecinos de a
```

Ese literal **es** el grafo: se escribe, se imprime, se guarda en un fichero y se lee de vuelta, igual
que el árbol de la clase 097. Otra vez la homoiconicidad haciendo innecesaria la serialización.

Para grafos grandes, lo idiomático es una tabla *hash* de nodo a lista de vecinos, con el idioma de
`push` sobre un lugar:

```lisp
(push destino (gethash origen grafo))
```

Una línea que **crea la entrada si no existe** —`gethash` devuelve `nil`, y `push` sobre `nil`
construye la lista— y añade el vecino en O(1). Es la autovivificación de Perl conseguida con `setf` y
lugares.

Y esta clase es buen sitio para mencionar una tradición de Lisp: **los grafos y la inteligencia
artificial simbólica**. Las redes semánticas, los grafos de restricciones, los sistemas de producción
y la unificación de Prolog se implementaron en Lisp durante décadas, y de ahí salieron ideas que hoy
son cotidianas: la propagación de restricciones, la memoización de subgrafos y los grafos de
dependencias para la recompilación incremental.

Lo notable, y por lo que conviene decirlo aquí, es que **casi todas esas implementaciones usaban listas
de asociación y símbolos**, no estructuras optimizadas. El símbolo internado de Lisp (clase 093) es
una clave perfecta: comparar dos nodos es comparar punteros, y `(get 'nodo 'vecinos)` —la lista de
propiedades de un símbolo— convierte cualquier símbolo en un registro extensible sin declarar nada.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set t [split [string trim $linea]]

puts "aristas=[expr {[llength $t] / 2}] nodos=[llength [lsort -unique $t]]"
```

**Lo que esta clase enseña en Tcl.** Una línea, porque las dos preguntas son `llength` sobre la lista
y sobre su versión sin duplicados.

Para el grafo real, Tcl tiene dos representaciones idiomáticas.

**El array con clave compuesta**, que es el idioma clásico:

```tcl
set arista(1,2) 1
set arista(2,3) 1
info exists arista(1,2)              ;# ¿hay arista? -- O(1)
array names arista 1,*                ;# los vecinos de 1
```

`array names` con un patrón hace de consulta de adyacencia. Es sorprendentemente práctico y depende de
que las claves sean cadenas — el mismo truco que en M.

**El `dict` anidado**, que es lo recomendado desde 8.5:

```tcl
dict set g 1 2 1
dict exists $g 1 2
dict keys [dict get $g 1]            ;# los vecinos de 1
dict for {origen vecinos} $g { ... }
```

`dict set g 1 2 1` **crea los niveles intermedios**, como la autovivificación de Perl, y `dict get`
con varias claves navega la jerarquía en una llamada.

Y **Tcllib incluye `struct::graph`**, que es un paquete completo y poco conocido: nodos y aristas con
atributos arbitrarios, aristas dirigidas y no dirigidas, recorridos, ordenación topológica,
componentes conexas, camino más corto y serialización.

```tcl
package require struct::graph
struct::graph g
g node insert 1 2 3
g arc insert 1 2
g walk 1 -order pre -type dfs -command procesar
```

Que un lenguaje de 1988 con fama de "solo para pegar cosas" traiga en su biblioteca estándar
comunitaria un grafo con atributos y recorridos configurables es uno de los datos que mejor explican
por qué Tcl sigue en uso: **la biblioteca es mucho más profunda que la reputación del lenguaje**.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my @t = split ' ', $linea;

my %nodos;
@nodos{@t} = ();

printf "aristas=%d nodos=%d\n", scalar(@t) / 2, scalar(keys %nodos);
```

**Lo que esta clase enseña en Perl.** La representación idiomática es **el hash de hashes**, y la
autovivificación (clase 095) hace que construirlo no necesite ninguna inicialización:

```perl
my %g;
$g{$origen}{$destino} = 1;            # crea AMBOS niveles

exists $g{1}{2}                        # ¿hay arista?
keys %{ $g{1} }                        # los vecinos de 1
scalar keys %{ $g{1} }                 # el grado
```

Esa línea `$g{$origen}{$destino} = 1;` construye el grafo entero sin declarar nada, y es
probablemente la forma más corta de representar un grafo etiquetado en cualquier lenguaje de esta
página.

Con la trampa correspondiente, que aquí muerde de verdad: **consultar `$g{5}{7}` en un nodo 5 que no
existe CREA `$g{5}` como hash vacío**. Recorrer el grafo preguntando por aristas inexistentes lo va
llenando de nodos fantasma, y el recuento de nodos sale mal. La defensa es preguntar por niveles:

```perl
if (exists $g{5} && exists $g{5}{7}) { ... }
```

Y CPAN, como es habitual, tiene la respuesta completa: **`Graph`**, de Jarkko Hietaniemi —uno de los
mantenedores históricos de Perl—, es una de las bibliotecas de grafos más completas de cualquier
lenguaje:

```perl
use Graph;
my $g = Graph->new(directed => 1);
$g->add_edge(1, 2);
$g->SPT_Dijkstra(1);           # camino más corto
$g->strongly_connected_components;
$g->topological_sort;
$g->is_cyclic;
```

Camino más corto, componentes fuertemente conexas, ordenación topológica, árbol de expansión mínima,
detección de ciclos y flujo máximo. Publicada en los años noventa, cuando la mayoría de los lenguajes
no tenía nada equivalente.

Es el patrón que se repite en esta sección: **el lenguaje base es mínimo, el ecosistema es enorme**.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <iterator>
#include <set>
#include <vector>

int main() {
    std::vector<int> t{std::istream_iterator<int>(std::cin),
                       std::istream_iterator<int>()};

    std::set<int> nodos(t.begin(), t.end());

    std::cout << "aristas=" << t.size() / 2
              << " nodos="  << nodos.size() << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** La biblioteca estándar **no tiene grafos**, y esa ausencia es
deliberada: el comité ha rechazado propuestas repetidamente porque **no hay una representación que
sirva para todos los casos**, y estandarizar la equivocada sería peor que no tener ninguna.

La representación idiomática en C++ para grafos densos en índices es el **vector de vectores**:

```cpp
std::vector<std::vector<int>> ady(n);
ady[origen].push_back(destino);
for (int v : ady[u]) { ... }
```

Es lo que se usa en programación competitiva y en la mayoría del código real: contiguo, sin
indirecciones extra por nodo, y con la caché a favor.

Y hay una biblioteca que merece una nota histórica: la **Boost Graph Library** (BGL), de 2001, es uno
de los diseños genéricos más ambiciosos que se han escrito.

```cpp
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/dijkstra_shortest_paths.hpp>

typedef boost::adjacency_list<boost::vecS, boost::vecS, boost::directedS> Grafo;
```

Su idea central es que **los algoritmos no conocen la representación**: se escriben contra unos
*conceptos* —`VertexListGraph`, `IncidenceGraph`, `EdgeListGraph`— y funcionan sobre cualquier
estructura que los cumpla, **incluida una tuya**. Adaptando tu propio grafo a los conceptos, los
algoritmos de Boost funcionan sobre él sin copiarlo.

Es la misma filosofía que la STL aplicada a grafos, llevada hasta el final. También es célebre por su
dificultad: los mensajes de error de plantillas de la BGL son legendarios, y son uno de los motivos
por los que C++20 introdujo los **conceptos** como característica del lenguaje.

Hoy las alternativas prácticas son `igraph`, `LEMON` y `SNAP`, y la representación CSR de la página de
Fortran es la habitual cuando el grafo es grande.

---

## 🟡 Contrato adaptado, y declarado

Estos lenguajes **no pueden** leer de `stdin` y escribir en `stdout` sin dejar de ser ellos
mismos. No es una limitación del material: es su naturaleza. El cálculo es el mismo y la forma
de entrar y salir es la de su anfitrión. **No pasan por el verificador**, y se dice.

### RPG

[Ficha completa](../../../atlas/rpg.md) · IBM i: ERP, retail, logística, manufactura · `CRTBNDRPG sobre IBM i`

> En IBM i un programa recibe sus datos por **parámetros**, por un **fichero** o por una **pantalla**, nunca por la entrada estándar.

```rpgle
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi GRAFO;
  entrada char(200) const;
end-pi;

dcl-s nodo  int(10) dim(200);
dcl-s nn    int(10) inz(0);
dcl-s nt    int(10) inz(0);
dcl-s i     int(10);
dcl-s valor int(10);
dcl-s tok   varchar(20) inz('');
dcl-s c     char(1);

for i = 1 to %len(%trimr(entrada)) + 1;
  if i <= %len(%trimr(entrada));
    c = %subst(entrada : i : 1);
  else;
    c = ' ';
  endif;
  if c = ' ';
    if tok <> '';
      nt += 1;
      valor = %int(tok);
      if nn = 0 or %lookup(valor : nodo : 1 : nn) = 0;
        nn += 1;
        nodo(nn) = valor;
      endif;
      tok = '';
    endif;
  else;
    tok += c;
  endif;
endfor;

dsply ('aristas=' + %char(nt / 2) + ' nodos=' + %char(nn));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG comparte la conclusión de COBOL: la representación natural es
**la lista de aristas como fichero**, y el procesamiento es por ruptura de control sobre un fichero
ordenado.

Lo que RPG añade, y es lo idiomático hoy en IBM i, es que **ese recorrido lo hace SQL**:

```sql
with recursive alcanzables (nodo, nivel) as (
    select origen, 0 from aristas where origen = 1
  union all
    select a.destino, r.nivel + 1
      from aristas a join alcanzables r on a.origen = r.nodo
     where r.nivel < 10
)
select distinct nodo from alcanzables;
```

Una **consulta recursiva** (`WITH RECURSIVE`, SQL:1999) es un recorrido en anchura sobre un grafo
almacenado como tabla de aristas, y Db2 for i la soporta. Con eso se resuelven explosión de materiales,
jerarquías de organización, dependencias entre piezas y alcanzabilidad — que son **los grafos reales
de un sistema de gestión**.

La explosión de materiales merece mención porque es el caso canónico: un producto se compone de
piezas, que se componen de piezas, hasta llegar a la materia prima. Eso es un grafo dirigido acíclico,
y calcular cuántos tornillos hacen falta para mil bicicletas es un recorrido con acumulación de
multiplicadores.

Los sistemas MRP —planificación de necesidades de material— llevan resolviendo ese problema desde los
años setenta, en RPG y COBOL, sobre ficheros indexados. **Es probablemente el algoritmo de grafos que
más dinero ha movido en la historia**, y casi nadie lo llama así.

Y en RPG clásico se escribe con `chain` recursivo o con una pila explícita sobre una tabla, como en la
clase 097 — un recorrido en profundidad escrito a mano, sin llamarlo nunca DFS.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 grafo: procedure options(main);

    declare linea char(200) varying;
    declare nodo(200) fixed binary(31);
    declare (nn, nt, i, j, valor) fixed binary(31);
    declare nuevo bit(1);
    declare tok char(20) varying initial('');
    declare c char(1);

    get edit (linea) (a(200));
    nn = 0; nt = 0;

    do i = 1 to length(linea) + 1;
       if i <= length(linea) then c = substr(linea, i, 1); else c = ' ';
       if c = ' ' then do;
          if tok ^= '' then do;
             nt = nt + 1;
             valor = tok;
             nuevo = '1'b;
             do j = 1 to nn;
                if nodo(j) = valor then nuevo = '0'b;
             end;
             if nuevo then do;
                nn = nn + 1;
                nodo(nn) = valor;
             end;
             tok = '';
          end;
       end;
       else tok = tok || c;
    end;

    put skip list ('aristas=' || trim(char(nt / 2)) ||
                   ' nodos='  || trim(char(nn)));

 end grafo;
```

**Lo que esta clase enseña en PL/I.** PL/I tiene, en un solo lenguaje, **las tres representaciones de
un grafo escritas de forma natural**, que es algo que ningún otro de esta página consigue:

**La matriz de adyacencia**, con la aritmética de arreglos de la clase 089:

```pli
declare a(100, 100) bit(1);
a = '0'b;                      /* poner a cero las diez mil celdas */
a(i, j) = '1'b;
```

**La lista de aristas como arreglo de estructuras**:

```pli
declare 1 arista(1000),
          2 origen  fixed binary(31),
          2 destino fixed binary(31),
          2 peso    fixed decimal(9,2);

peso = 0;                       /* poner a cero LOS MIL pesos */
```

**Y la lista de adyacencia enlazada**, con `based` y punteros:

```pli
declare 1 vecino based(p),
          2 nodo fixed binary(31),
          2 siguiente pointer;
declare cabeza(100) pointer;
```

Esa combinación —arreglos con aritmética, estructuras con campos como columnas, y punteros con reserva
dinámica— es exactamente lo que PL/I pretendía ser: **un lenguaje que sirviera igual para lo que hacía
Fortran y para lo que hacía COBOL**.

Y es también la razón por la que fracasó como lenguaje universal: el estándar completo era enorme, los
compiladores costaban años y **casi nadie usaba más de un tercio del lenguaje**. Los programadores
científicos escribían PL/I con estilo Fortran; los de gestión, con estilo COBOL.

Es una lección de diseño que se ha repetido después: **la unión de dos lenguajes no produce un
lenguaje que guste a los dos públicos**, produce uno que ambos usan a medias. Ada, veinte años
después, tuvo cuidado de no caer en lo mismo — y aun así se le reprochó ser demasiado grande.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
GRAFO ; Grafos -- clase 098
 read linea
 kill nodos
 set nt = $length(linea, " ")
 for i=1:1:nt set nodos($piece(linea, " ", i)) = ""
 set nn = 0, k = ""
 for  set k = $order(nodos(k))  quit:k=""  set nn = nn + 1
 write "aristas=", nt \ 2, " nodos=", nn, !
 quit
```

**Lo que esta clase enseña en M.** Aquí M tiene la mejor historia de la clase, y merece contarse
entera: **un grafo en M es, literalmente, una base de datos de grafos**.

La lista de adyacencia es un array de dos niveles:

```mumps
 set ^G(origen, destino) = peso
 set ^G(1, 2) = 5
```

Y con eso ya están todas las operaciones:

```mumps
 if $data(^G(1,2))                                    ; ¿hay arista?
 for  set d=$order(^G(1,d))  quit:d=""  ...           ; los VECINOS de 1, en orden
 kill ^G(1,2)                                          ; borrar la arista
 kill ^G(1)                                            ; borrar el nodo y todas sus salidas
```

Recorrer los vecinos de un nodo es `$order` sobre el segundo subíndice. Un recorrido en anchura es un
bucle con una cola; uno en profundidad, con una pila.

Y lo que hace esto distinto de cualquier otro lenguaje de la página es el **`^`**: ese grafo **está en
disco**, es transaccional, lo comparten todos los procesos y **no cabe en memoria sin problema**. Un
grafo de mil millones de aristas se recorre igual que uno de diez.

No es teoría. **YottaDB y InterSystems IRIS se venden explícitamente como bases de datos
multimodelo**, y el modelo de grafo es uno de los que ofrecen — sobre exactamente esta estructura.
FIS-GT.M ha sostenido durante décadas el sistema bancario de varios países con grafos de transacciones
almacenados así.

Y hay un detalle que lo redondea: **el orden de `$order` significa que los vecinos salen ordenados**,
así que un recorrido en anchura por orden de identificador es gratis, y un índice inverso es otro
global:

```mumps
 set ^GINV(destino, origen) = ""      ; las aristas ENTRANTES
```

Dos líneas para mantener el grafo en las dos direcciones, con índices persistentes y consistentes
dentro de la misma transacción. Es lo que hacen Neo4j y Dgraph, con sesenta años menos de historia.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| t nodos |

t := stdin nextLine substrings collect: [ :cada | cada asNumber ].
nodos := t asSet.

Transcript
    show: 'aristas=', (t size // 2) printString;
    show: ' nodos=', nodos size printString;
    cr.
```

**Lo que esta clase enseña en Smalltalk.** La representación idiomática es un `Dictionary` de nodo a
`Set` de vecinos, y el mensaje que lo hace cómodo es el de la clase 095:

```smalltalk
| g |
g := Dictionary new.
(g at: origen ifAbsentPut: [ Set new ]) add: destino.

(g at: 1 ifAbsent: [ Set new ]) size.        "el grado"
(g at: 1) includes: 2.                        "¿hay arista?"
```

`at:ifAbsentPut:` resuelve en un mensaje lo que en otros lenguajes son tres líneas, y **el bloque solo
se evalúa si hace falta**, así que no se crea un `Set` por consulta.

Y esta clase es un buen sitio para señalar algo sobre Smalltalk que no se ve en las demás: **el propio
sistema es un grafo, y está permanentemente disponible para inspección**.

```smalltalk
Integer allSuperclasses            "la cadena de herencia"
Integer subclasses
Integer allSubclasses
Integer selectors                   "los mensajes que entiende"
SystemNavigation default allCallsOn: #printString      "QUIÉN llama a este mensaje"
Integer allInstVarNames
```

`allCallsOn:` recorre **todos los métodos compilados de la imagen** buscando quién envía un mensaje
concreto. Es análisis de grafos de llamadas sobre el sistema vivo, en un mensaje, y es lo que hacen
por dentro el navegador de código y las herramientas de refactorización.

Ese es el origen del **Refactoring Browser**, escrito en Smalltalk en 1997 por John Brant y Don
Roberts: **la primera herramienta de refactorización automática de la historia**, y el trabajo del que
salió el libro de Martin Fowler. Renombrar un método, extraer una variable, subir un método a la
superclase — todo lo que hoy hace un IDE en cualquier lenguaje empezó ahí.

Y pudo empezar ahí por lo que esta clase enseña: **cuando el programa es un grafo de objetos vivos y
consultables, refactorizar es recorrer ese grafo**. En un lenguaje compilado hay que reconstruirlo
analizando texto.

---

## Y de vuelta a la clase

Lo transferible: **la representación de un grafo es una decisión de densidad, no de gusto**. Con V
nodos y E aristas, la matriz ocupa V² siempre y responde "¿hay arista?" en O(1); la lista de
adyacencia ocupa V+E y responde en O(grado). Para un grafo social —millones de nodos, decenas de
aristas cada uno— la matriz es imposible; para una malla de elementos finitos densa, es lo correcto.
La pregunta que hay que hacerse siempre es la misma: **¿cuántas aristas hay respecto a V²?**

⏮️ [Volver a la clase 098](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
