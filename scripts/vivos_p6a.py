# -*- coding: utf-8 -*-
"""Parte 6, lote A — clases 089 a 091. Ver `vivos_parte6.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 089 — Arreglos de tamaño fijo
# ---------------------------------------------------------------------------
SPECS["089"] = dict(
    gancho="""
Tres enteros en un arreglo, su suma y su máximo. Es la estructura de datos más antigua que existe, y
la que mejor separa a estos lenguajes: **Fortran lleva el arreglo en el centro del lenguaje desde
1957**, con operaciones que trabajan sobre el arreglo entero; **COBOL lo llama tabla y lo escribe con
`OCCURS`**; y **Ada es el único que comprueba el índice en cada acceso, siempre, por defecto**.
""",
    porque="""
Aquí el concepto es el **arreglo de tamaño conocido en compilación**, y estos lenguajes lo enseñan
porque cada uno tomó una decisión distinta sobre lo que más importa: **quién comprueba los límites**.

**Ada** los comprueba siempre y hay que desactivarlo explícitamente. **Fortran** los comprueba solo si
se lo pides (`-fcheck=bounds`). **C++** no los comprueba nunca con `[]`, y ahí está el origen de una
fracción enorme de los fallos de seguridad de los últimos treinta años. **COBOL** ofrece `SSRANGE`
como opción de compilación y muchas instalaciones lo desactivan en producción por rendimiento.

Y **Fortran** aporta algo que ningún otro tiene aquí: **el arreglo como valor**, con `sum(v)`,
`maxval(v)` y `v = v * 2` sin escribir un bucle.
""",
    cierre="""
Lo transferible: **un arreglo son dos cosas —los datos y sus límites— y los lenguajes se diferencian
en dónde guardan la segunda**. En C y C++ los límites no viajan con el arreglo, y por eso hay que
pasar el tamaño aparte. En Ada, Fortran y Pascal el tipo los incluye, y por eso `V'Range`, `size(v)` y
`High(V)` existen. Cuando leas una firma con un puntero y un entero al lado —`f(int* v, int n)`— estás
viendo un arreglo al que le arrancaron la mitad de su información.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. ARREGLO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  PARTES.
    05  TXT   PIC X(20) OCCURS 3 TIMES.
01  TABLA.
    05  ELEM  PIC S9(9) COMP-3 OCCURS 3 TIMES.
01  I       PIC 9(2)  COMP.
01  SUMA    PIC S9(18) COMP-3 VALUE 0.
01  MAXIMO  PIC S9(9)  COMP-3.
01  ED-S    PIC -(17)9.
01  ED-M    PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES
        INTO TXT(1) TXT(2) TXT(3)

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 3
        COMPUTE ELEM(I) = FUNCTION NUMVAL(TXT(I))
    END-PERFORM

    MOVE ELEM(1) TO MAXIMO
    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 3
        ADD ELEM(I) TO SUMA
        IF ELEM(I) > MAXIMO
            MOVE ELEM(I) TO MAXIMO
        END-IF
    END-PERFORM

    MOVE SUMA   TO ED-S
    MOVE MAXIMO TO ED-M
    DISPLAY "suma=" FUNCTION TRIM(ED-S)
            " max="  FUNCTION TRIM(ED-M)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** En COBOL no se dice "arreglo": se dice **tabla**, y se declara
con **`OCCURS`** dentro de una estructura, nunca en el nivel 01.

```cobol
01  TABLA.
    05  ELEM  PIC S9(9) COMP-3 OCCURS 3 TIMES.
```

Y hay dos rasgos que sorprenden a quien viene de otro sitio.

**El primero: los índices empiezan en 1.** `ELEM(1)` es el primero. Coincide con Fortran, Ada, Lisp
—no, Lisp empieza en 0— y con la intuición de quien no ha programado nunca; discrepa de C, C++,
Perl y Python.

**El segundo: `OCCURS` no crea un objeto nuevo, describe una repetición dentro de un registro.** Una
tabla COBOL es, literalmente, un trozo de memoria contiguo con el mismo formato repetido, que es
exactamente cómo llegan los datos de un fichero de longitud fija. Por eso una tabla se puede
redefinir, mover entera con un solo `MOVE` y escribir en un fichero tal cual.

Sobre los límites, COBOL tiene la comprobación y la deja como opción del compilador:

```bash
cobc -x -fssrange arreglo.cob      # comprueba los índices en ejecución
```

**Muchas instalaciones compilan producción sin `SSRANGE`** por rendimiento, y ahí un índice fuera de
rango **escribe silenciosamente en el campo de al lado**. Es el equivalente COBOL del desbordamiento
de C, y una de las causas clásicas de corrupción de datos difícil de diagnosticar.

Para tablas grandes existe además `INDEXED BY`, que declara un índice del tipo interno del compilador
—más rápido que una variable numérica— y habilita `SEARCH` y `SEARCH ALL`, la búsqueda binaria
integrada en el lenguaje.
"""),
        "fortran": ("""
program arreglo
   implicit none
   integer :: v(3)          ! tamaño fijo, conocido al compilar

   read(*, *) v             ! lee los TRES de una vez

   write(*, '(A,I0,A,I0)') 'suma=', sum(v), ' max=', maxval(v)
end program arreglo
""", """
**Lo que esta clase enseña en Fortran.** Este programa es de cuatro líneas por una razón: **en Fortran
el arreglo es un valor de primera clase, y las operaciones se aplican al arreglo entero**.

`read(*, *) v` lee tres números sin bucle. `sum(v)` y `maxval(v)` son funciones intrínsecas del
lenguaje, no de una biblioteca. Y lo mismo vale para el cálculo:

```fortran
v = v * 2                    ! sin bucle
w = v + u                    ! suma elemento a elemento
donde: where (v < 0) v = 0   ! asignación condicional sobre todo el arreglo
print *, dot_product(v, u), matmul(a, b)
```

Esa notación —**la aritmética de arreglos**, incorporada en Fortran 90— es la razón de que Fortran
siga siendo el lenguaje del cálculo numérico. No es azúcar sintáctico: **el compilador ve la operación
completa**, así que puede vectorizarla con instrucciones SIMD, paralelizarla o enviarla a una GPU. Un
bucle en C con punteros no le da esa información.

Fortran también fue el primero en tener **arreglos multidimensionales de verdad**: `a(i, j)` es una
sola operación de indexación, no `a[i][j]` con dos indirecciones.

Y guarda una peculiaridad que hay que conocer al mezclarlo con C: **el orden de almacenamiento es por
columnas** (*column-major*). En Fortran, `a(1,1)` y `a(2,1)` son contiguos; en C, `a[0][0]` y `a[0][1]`
lo son. Recorrer una matriz en el orden equivocado multiplica el tiempo por diez por fallos de caché,
y es el error de rendimiento más común al portar código entre los dos lenguajes.

Los límites se comprueban con `-fcheck=bounds`, y la práctica recomendada es compilar así en
desarrollo.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Arreglo is
   type Vector is array (1 .. 3) of Integer;

   V      : Vector;
   Suma   : Integer := 0;
   Maximo : Integer;
begin
   for I in V'Range loop        --  el arreglo SABE cuál es su rango
      Get (V (I));
   end loop;

   Maximo := V (V'First);
   for I in V'Range loop
      Suma := Suma + V (I);
      if V (I) > Maximo then
         Maximo := V (I);
      end if;
   end loop;

   Put ("suma=");  Put (Suma,   Width => 1);
   Put (" max=");  Put (Maximo, Width => 1);
   New_Line;
end Arreglo;
""", """
**Lo que esta clase enseña en Ada.** Dos cosas que Ada hace y casi nadie más.

**Primera: el índice puede ser de cualquier tipo discreto, no solo un entero.**

```ada
type Dia is (Lun, Mar, Mie, Jue, Vie);
type Horas is array (Dia) of Natural;
H : Horas;
H (Mie) := 8;                  --  indexar por un valor de enumeración
```

El arreglo se indexa con el tipo que corresponde al problema, y **no se puede indexar con otra cosa**.
Es imposible confundir un índice de días con uno de meses, porque son tipos distintos. En C, ambos
son `int`.

**Segunda: los atributos del arreglo viajan con él.** `V'Range`, `V'First`, `V'Last`, `V'Length` están
disponibles siempre, también dentro de un subprograma que reciba el arreglo. De ahí sale el
**arreglo no restringido**, que es la pieza clave:

```ada
type Vector is array (Positive range <>) of Integer;    --  tamaño SIN fijar

function Suma (V : Vector) return Integer is
   Total : Integer := 0;
begin
   for I in V'Range loop        --  el rango viene con el parámetro
      Total := Total + V (I);
   end loop;
   return Total;
end Suma;
```

`range <>` declara el tipo sin fijar los límites; cada valor concreto los lleva consigo. Eso permite
escribir una función que acepta arreglos de cualquier tamaño **sin pasar la longitud aparte**, que es
justo lo que C no puede hacer.

Y la comprobación de índices está **activada por defecto**: un acceso fuera de rango lanza
`Constraint_Error` con fichero y línea. Se puede desactivar con `pragma Suppress`, y la cultura del
lenguaje es no hacerlo salvo con medidas en la mano.
"""),
        "pascal": ("""
program Arreglo;
{$MODE OBJFPC}{$H+}
{$RANGECHECKS ON}
uses SysUtils;

type
  TVector = array[1..3] of Integer;

var
  V: TVector;
  I, Suma, Maximo: Integer;

begin
  for I := Low(V) to High(V) do
    Read(V[I]);

  Suma := 0;
  Maximo := V[Low(V)];
  for I := Low(V) to High(V) do
  begin
    Suma := Suma + V[I];
    if V[I] > Maximo then
      Maximo := V[I];
  end;

  WriteLn('suma=', IntToStr(Suma), ' max=', IntToStr(Maximo));
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal tomó de Algol la idea de que **el rango del índice
forma parte del tipo**, y la escribe de la forma más legible de esta página:

```pascal
type
  TVector    = array[1..3] of Integer;
  TPorDia    = array[Lun..Vie] of Integer;      { indexado por enumeración }
  TMatriz    = array[1..3, 1..4] of Real;       { dos dimensiones }
  TTablaAscii = array[Char] of Byte;             { indexado por CARACTER }
```

`Low(V)` y `High(V)` son funciones de compilación que devuelven los límites, así que un bucle escrito
con ellas **sigue siendo correcto si se cambia la declaración**. Escribir `for I := 1 to 3` y luego
ampliar el arreglo a 5 es el error clásico que `Low`/`High` eliminan.

Y **`{$RANGECHECKS ON}`** —o `-Cr` en la línea de órdenes— activa la comprobación de índices. Free
Pascal la trae **desactivada por defecto** en modo de publicación y activada en la configuración de
depuración de Lazarus.

Hay una consecuencia de la tipificación estricta de Pascal que conviene conocer, porque es la crítica
histórica más citada al lenguaje: **dos arreglos de tamaños distintos son tipos incompatibles**, así
que una función que reciba `array[1..3] of Integer` **no acepta** un `array[1..4]`. Ese fue el
problema que hizo a Kernighan escribir *Why Pascal Is Not My Favorite Programming Language* (1981).

La respuesta llegó después: los **arreglos abiertos** (`array of Integer` como parámetro), con `Low`,
`High` y `Length` disponibles dentro. Es exactamente el `range <>` de Ada, y hoy es lo normal.
"""),
        "lisp": ("""
(let ((v (make-array 3)))
  (dotimes (i 3)
    (setf (aref v i) (read)))       ; los índices empiezan en 0
  (format t "suma=~D max=~D~%"
          (reduce #'+ v)
          (reduce #'max v)))
""", """
**Lo que esta clase enseña en Common Lisp.** Que Lisp tenga arreglos de verdad sorprende a quien lo
asocia solo con listas enlazadas, y es una de las diferencias más grandes entre el Lisp de 1960 y el
Common Lisp de 1984.

`make-array` crea un **vector contiguo**, con acceso en tiempo constante, y `aref` lo indexa. **Los
índices empiezan en 0**, al contrario que COBOL, Fortran, Ada y Pascal.

Y `make-array` acepta una batería de opciones que cubre casi todos los casos de esta parte del curso:

```lisp
(make-array 3)                                    ; vector general
(make-array '(3 4))                               ; MATRIZ de 3x4
(make-array 3 :element-type 'double-float)        ; especializado: compacto y rápido
(make-array 3 :initial-element 0)
(make-array 0 :adjustable t :fill-pointer t)      ; DINÁMICO (clase 090)
```

`:element-type` es la clave del rendimiento: un vector de `double-float` se almacena como memoria
contigua de dobles, sin punteros ni etiquetas, y `(aref v i)` compila a una carga directa. Es lo mismo
que un `array` de NumPy frente a una lista de Python.

Y `reduce` funciona sobre **cualquier secuencia** —vector o lista— igual que `map`, `find`, `sort` y
`position`. Common Lisp unificó las dos familias bajo el concepto de *secuencia*, lo que evita tener
dos juegos de funciones.

Sobre los límites: `aref` los comprueba, salvo que se declare `(optimize (safety 0))`, que es la forma
que tiene Lisp de decir "confía en mí" — y entonces se comporta como C.
"""),
        "tcl": ("""
gets stdin linea
set v [split [string trim $linea]]

set suma 0
set maximo [lindex $v 0]
foreach x $v {
    set suma [expr {$suma + $x}]
    if {$x > $maximo} { set maximo $x }
}

puts "suma=$suma max=$maximo"
""", """
**Lo que esta clase enseña en Tcl.** **Tcl no tiene arreglos de tamaño fijo.** No hay declaración de
tamaño, no hay tipo de elemento y no hay comprobación de límites: `lindex` fuera de rango **devuelve
la cadena vacía** en lugar de fallar.

Lo que hay es la **lista**, que es la estructura universal del lenguaje, y aquí conviene deshacer un
malentendido de nombre: **lo que Tcl llama `array` NO es un arreglo, es una tabla asociativa**
(clase 095).

```tcl
set lista {1 2 3}          ;# esto es una LISTA (secuencia)
set arr(clave) valor       ;# esto es un ARRAY de Tcl: un DICCIONARIO
```

Esa colisión de nombres viene de 1988 y confunde a todo el mundo la primera vez.

Y bajo la apariencia de que "todo es una cadena", la implementación es seria: desde Tcl 8.0, un valor
lleva una **representación interna** además de la textual, y una lista se almacena como un **vector de
punteros a objetos**, con `lindex` en tiempo constante. La cadena solo se genera si alguien la pide.

Para datos numéricos masivos, donde un vector de punteros es caro, Tcl 8.6 añadió los **`bytearray`** y
el paquete `tcl::binary`, y las extensiones como **NAP** o **tclvec** dan arreglos numéricos
compactos. Pero la lista sigue siendo la respuesta por defecto, y es más rápida de lo que su sintaxis
sugiere.
"""),
        "perl": ("""
use strict;
use warnings;
use List::Util qw(sum max);

my $linea = <STDIN>;
chomp $linea;
my @v = split ' ', $linea;

printf "suma=%d max=%d\\n", sum(@v), max(@v);
""", """
**Lo que esta clase enseña en Perl.** **Perl no tiene arreglos de tamaño fijo.** `@v` crece y encoge
sola, y **acceder fuera de rango no es un error**: devuelve `undef`.

Peor —o mejor, según se mire—: **asignar fuera de rango extiende el arreglo**.

```perl
my @v = (1, 2, 3);
$v[10] = 99;          # ahora tiene 11 elementos, del 3 al 9 son undef
print scalar(@v);     # 11
```

Eso es lo contrario de todo lo demás en esta página, y refleja la filosofía del lenguaje: el
programador sabe lo que hace.

Hay tres formas de preguntar por el tamaño, y las tres aparecen en código real:

```perl
scalar(@v)      # el número de elementos
$#v             # el ÚLTIMO ÍNDICE, que es scalar(@v) - 1
if (@v) { }     # en contexto booleano: ¿tiene algo?
```

`$#v` es una fuente clásica de errores por confundirlo con la longitud, y también permite algo
peculiar: **asignarle un valor cambia el tamaño del arreglo**. `$#v = -1` lo vacía.

Y una decisión de diseño con consecuencias: **los arreglos se aplanan al pasarlos**. `f(@a, @b)`
llega como una sola lista, y por eso las estructuras anidadas se construyen con **referencias**
(`\\@a`, `[1, 2, 3]`), que es lo que se verá en la clase 097.

`sum` y `max` vienen de `List::Util`, un módulo **del núcleo** escrito en C — no hace falta instalar
nada.
"""),
        "cpp": ("""
#include <algorithm>
#include <array>
#include <iostream>
#include <numeric>

int main() {
    std::array<int, 3> v{};        // tamaño en el TIPO, sin coste de puntero

    for (auto& x : v) {
        if (!(std::cin >> x)) return 1;
    }

    std::cout << "suma=" << std::accumulate(v.begin(), v.end(), 0)
              << " max="  << *std::max_element(v.begin(), v.end()) << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ tiene **dos** arreglos de tamaño fijo, y elegir el moderno no
es cuestión de estilo.

```cpp
int v[3];                  // el arreglo de C: se DEGRADA a puntero
std::array<int, 3> w{};    // C++11: es un tipo normal
```

El arreglo de C **pierde su tamaño en cuanto se pasa a una función**: `void f(int v[3])` es
exactamente `void f(int* v)`, y el `3` se ignora. Por eso toda la API de C lleva un `size_t n` al
lado.

`std::array` conserva el tamaño en el tipo: se puede copiar, devolver, comparar con `==`, meter en un
contenedor, y `w.size()` es una constante de compilación. **No añade ningún coste**: ocupa lo mismo y
compila a lo mismo.

Sobre los límites, es donde C++ carga con su historia: **`v[i]` no comprueba nada, nunca**. El acceso
fuera de rango es comportamiento indefinido, y es el origen directo de una fracción enorme de los
fallos de seguridad de los últimos treinta años — hasta el punto de que la agencia estadounidense
CISA recomienda desde 2023 abandonar los lenguajes sin seguridad de memoria para software nuevo.

Las herramientas para mitigarlo existen y son buenas:

```cpp
v.at(i)                              // comprueba y lanza std::out_of_range
```

```bash
g++ -fsanitize=address,undefined     # detecta el desbordamiento en ejecución
g++ -D_GLIBCXX_ASSERTIONS            # comprueba los índices de la biblioteca estándar
```

Y C++20 añadió **`std::span`**, que es por fin el "puntero + tamaño" convertido en un tipo: pasa un
arreglo sin copiarlo y **sin perder su longitud**. Es el `range <>` de Ada, cuarenta años después.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi ARREGLO;
  a int(10) const;
  b int(10) const;
  c int(10) const;
end-pi;

dcl-s elem  int(10) dim(3);       // DIM: la tabla de RPG
dcl-s i     int(10);
dcl-s suma  int(20) inz(0);
dcl-s maximo int(10);
dcl-s salida char(50);

elem(1) = a;
elem(2) = b;
elem(3) = c;

maximo = elem(1);
for i = 1 to %elem(elem);
  suma += elem(i);
  if elem(i) > maximo;
    maximo = elem(i);
  endif;
endfor;

salida = 'suma=' + %char(suma) + ' max=' + %char(maximo);
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** La palabra clave **`dim(n)`** declara una tabla, y **los índices
empiezan en 1**, como en COBOL. `%elem()` devuelve el número de elementos declarado.

Lo característico de RPG es que las tablas tienen **operaciones que trabajan sobre la tabla entera**,
como en Fortran:

```rpgle
dcl-s v int(10) dim(100);

%subarr(v : 1 : 10)              // una "rebanada" de la tabla
suma = %sum(%subarr(v : 1 : n)); // suma de un tramo
sorta v;                          // ORDENA la tabla, en el lenguaje
%lookup(clave : v);               // búsqueda; %lookupgt, %lookuple...
```

`sorta` y `%lookup` en el lenguaje base, sin biblioteca, son un vestigio del origen de RPG como
generador de informes: ordenar y buscar en una tabla eran las dos operaciones que todo programa
necesitaba.

Y hay una construcción propia de RPG que no tiene equivalente en el núcleo: la **estructura de datos
con `dim`**, que es una tabla de registros mapeada sobre memoria contigua.

```rpgle
dcl-ds lineas qualified dim(50);
  codigo char(10);
  cantidad packed(5);
end-ds;

lineas(3).cantidad = 7;
```

Eso es exactamente el `OCCURS` de COBOL sobre un grupo, y sirve para lo mismo: **leer un registro de
fichero de longitud fija y acceder a sus repeticiones sin copiar nada**.

Sobre los límites, RPG **sí comprueba** los índices y lanza el error `RNQ0121` con el número de
sentencia, sin necesidad de opciones de compilación. Es más seguro que C, C++ y el COBOL sin `SSRANGE`.
"""),
        "pli": ("""
 arreglo: procedure options(main);

    declare v(3) fixed binary(31);
    declare (i, suma, maximo) fixed binary(31);

    get list (v);            /* lee los TRES */

    suma = sum(v);           /* funciones sobre el arreglo ENTERO */
    maximo = max(v(1), v(2), v(3));

    put skip list ('suma=' || trim(char(suma)) ||
                   ' max='  || trim(char(maximo)));

 end arreglo;
""", """
**Lo que esta clase enseña en PL/I.** PL/I fue diseñado en 1964 para unir Fortran y COBOL, y en los
arreglos se ve mejor que en ninguna otra parte: **tiene la aritmética de arreglos de Fortran
veintiséis años antes que Fortran 90**.

```pli
declare v(3) fixed binary(31);
declare w(3) fixed binary(31);

v = 0;              /* asigna a TODOS los elementos */
v = w * 2;          /* elemento a elemento, sin bucle */
suma = sum(v);      /* funciones sobre el arreglo entero */
put list (v);       /* imprime el arreglo completo */
```

Y añade dos cosas que Fortran no tuvo hasta mucho después:

**Límites arbitrarios**, incluidos negativos, como en Ada y Pascal:

```pli
declare temperaturas(-40:50) fixed decimal(5,1);
```

**Arreglos de estructuras y estructuras de arreglos**, con la misma notación:

```pli
declare 1 cliente(100),
          2 nombre char(30),
          2 saldo  fixed decimal(11,2);

cliente.saldo = 0;              /* pone a cero LOS CIEN saldos */
```

Esa última línea —una asignación que recorre un campo de cien registros— no tiene equivalente directo
en ningún lenguaje del núcleo, y es exactamente el tipo de operación que hoy se llama *columnar*.

PL/I comprueba los límites con la condición **`SUBSCRIPTRANGE`**, que se activa con un prefijo en el
propio código:

```pli
 (subscriptrange): arreglo: procedure options(main);
```

Está **desactivada por defecto** por rendimiento, y esa decisión —seguridad opcional, activada por el
programador— es la misma que tomaron Fortran, COBOL y C, y la contraria a la de Ada.
"""),
        "mumps": ("""
ARREGLO ; Arreglos de tamano fijo -- clase 089
 read linea
 for i=1:1:3 set v(i) = $piece(linea, " ", i)
 set suma = 0
 set maximo = v(1)
 for i=1:1:3 do
 . set suma = suma + v(i)
 . if v(i) > maximo set maximo = v(i)
 write "suma=", suma, " max=", maximo, !
 quit
""", """
**Lo que esta clase enseña en M.** **En M no existen los arreglos de tamaño fijo.** No hay
declaración, no hay tamaño y no hay tipo de elemento: `set v(1)=3` crea el "arreglo" y el elemento a
la vez.

Y lo que parece un arreglo **no lo es**: es un **árbol disperso ordenado**, que es la única estructura
de datos que tiene el lenguaje y la que cubre todos los papeles.

```mumps
 set v(1) = 3
 set v("hola") = 7          ; el índice puede ser una CADENA
 set v(1, 2, "x") = 9       ; y puede haber varios niveles, sin declarar nada
 set v(3.14159) = 1         ; o un decimal
```

Los índices se mantienen **ordenados automáticamente** —numéricos primero, después alfabéticos— y se
recorren con `$order`, sin saber cuáles existen:

```mumps
 set i = ""
 for  set i = $order(v(i))  quit:i=""  write i, "=", v(i), !
```

No hay huecos que ocupen memoria: `v(1)` y `v(1000000)` pueden existir sin nada entre medias. Por eso
se llama **disperso**.

Y aquí está lo importante, que es lo que hace a M seguir vivo: **la misma sintaxis con `^` delante
significa que la estructura está en disco**.

```mumps
 set ^PACIENTE(id, "nombre") = "Ada"
```

`^PACIENTE` es un **global**: un árbol persistente, transaccional y compartido entre procesos, con la
misma sintaxis que la variable local. **No hay capa de acceso a datos, no hay serialización y no hay
correspondencia objeto-relacional**, porque la estructura de datos del lenguaje *es* la de la base de
datos.

Ese es el motivo real de que M siga en producción en 2026: no el lenguaje, sino esa fusión.
"""),
        "smalltalk": ("""
| partes v suma maximo |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].

v := Array new: 3.
1 to: 3 do: [ :i | v at: i put: (partes at: i) ].

suma   := v inject: 0 into: [ :acc :cada | acc + cada ].
maximo := v inject: (v at: 1) into: [ :acc :cada | acc max: cada ].

Transcript
    show: 'suma=', suma printString;
    show: ' max=', maximo printString;
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** `Array new: 3` crea un arreglo de tamaño fijo, se indexa
con `at:` y `at:put:`, y **los índices empiezan en 1**.

Pero lo que enseña esta clase en Smalltalk no es el arreglo: es que **el arreglo es solo una clase
más dentro de una jerarquía de colecciones cuidadosamente diseñada**, que fue la primera de la
historia y el modelo del que salieron las de Java, C# y Ruby.

```text
Collection
├── SequenceableCollection      "tiene orden"
│   ├── ArrayedCollection → Array, String, Symbol, ByteArray
│   ├── OrderedCollection       "dinámica (clase 090)"
│   ├── SortedCollection        "se mantiene ordenada sola"
│   └── Interval                "un rango (clase 092)"
├── HashedCollection → Set, Bag, Dictionary
└── ...
```

Todo lo que hereda de `Collection` responde a `do:`, `collect:`, `select:`, `reject:`, `detect:`,
`inject:into:` e `includes:`. **Cambiar un `Array` por un `Set` o por un `OrderedCollection` no
obliga a tocar el código que lo recorre.**

Esa es la aportación duradera: no la clase concreta, sino **el protocolo común**, que es el
antepasado directo de los `Iterable` y los `IEnumerable` de todos los lenguajes modernos.

`inject:into:` es el `reduce` o el `fold` de otros lenguajes, con un nombre que dice qué hace:
inyectar un valor inicial en la colección.

Y sobre los límites, Smalltalk es tajante: `at:` fuera de rango **lanza un error siempre**, sin
opción de desactivarlo. En un sistema donde el error abre un depurador sobre el proceso vivo, no
tiene sentido no comprobar.
"""),
    },
)
