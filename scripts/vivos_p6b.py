# -*- coding: utf-8 -*-
"""Parte 6, lote B — clases 090 y 091. Ver `vivos_parte6.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 090 — Listas, vectores y arreglos dinámicos
# ---------------------------------------------------------------------------
SPECS["090"] = dict(
    gancho="""
Una lista que no sabe cuántos elementos tendrá hasta que llega la entrada. Aquí aparece la costura
entre dos épocas: los lenguajes nacidos cuando **la memoria se reservaba entera al arrancar** —COBOL,
Fortran hasta 1990, RPG— y los que dan una estructura que crece sola. Y hay un dato incómodo:
**COBOL sí tiene tablas de tamaño variable desde 1974**, con `OCCURS DEPENDING ON`, y casi nadie lo
sabe.
""",
    porque="""
Aquí el concepto es el **crecimiento en tiempo de ejecución**, y estos lenguajes lo enseñan porque
enseñan lo que cuesta. **Fortran 90** trajo `allocatable`, y con él la pregunta de cuándo se libera;
**Ada 95** trajo los contenedores estándar en 2005; **C++** tiene `std::vector`, que es el ejemplo
canónico de crecimiento amortizado; y **COBOL** tiene `OCCURS DEPENDING ON`, que no reserva memoria
sino que **describe cuánto del registro es válido**.

Esa última distinción —crecer frente a describir— es la que separa el pensamiento de los años sesenta
del actual, y merece entenderse bien.
""",
    cierre="""
Lo transferible: **"dinámico" significa cosas distintas y conviene saber cuál tienes**. Un
`std::vector` reserva de más y duplica su capacidad; una lista enlazada reserva un nodo por elemento;
un `OCCURS DEPENDING ON` no reserva nada, solo declara cuánto del espacio ya reservado cuenta; y una
lista de Lisp o de Tcl esconde una representación interna que cambia según el uso. El coste de añadir
un elemento —constante amortizado, constante real o lineal— depende de cuál sea, y es la primera
pregunta que hay que hacerse al elegir.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. LISTA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(2)  COMP VALUE 0.
01  I       PIC 9(4)  COMP.
01  L       PIC 9(4)  COMP.
01  N       PIC 9(4)  COMP VALUE 0.
01  SPOS    PIC 9(4)  COMP VALUE 1.
01  TABLA.
    05  ELEM  PIC S9(9) COMP-3 OCCURS 1 TO 100 TIMES DEPENDING ON N.
01  SALIDA  PIC X(200) VALUE SPACES.
01  ED      PIC -(8)9.
01  TXT     PIC X(10).

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

    PERFORM VARYING I FROM N BY -1 UNTIL I < 1
        MOVE ELEM(I) TO ED
        MOVE FUNCTION TRIM(ED) TO TXT
        MOVE 0 TO L
        INSPECT FUNCTION REVERSE(TXT) TALLYING L FOR LEADING SPACE
        COMPUTE L = 10 - L
        MOVE TXT(1:L) TO SALIDA(SPOS:L)
        ADD L TO SPOS
        IF I > 1
            MOVE "-" TO SALIDA(SPOS:1)
            ADD 1 TO SPOS
        END-IF
    END-PERFORM

    COMPUTE L = SPOS - 1
    DISPLAY "invertido=" SALIDA(1:L)
    STOP RUN.

CERRAR-TOKEN.
    IF TLEN > 0
        ADD 1 TO N
        COMPUTE ELEM(N) = FUNCTION NUMVAL(TOKEN)
        MOVE SPACES TO TOKEN
        MOVE 0 TO TLEN
    END-IF.
""", """
**Lo que esta clase enseña en COBOL.** La línea decisiva es esta:

```cobol
05  ELEM  PIC S9(9) COMP-3 OCCURS 1 TO 100 TIMES DEPENDING ON N.
```

Es **`OCCURS DEPENDING ON`**, y está en COBOL desde el estándar de 1974. Pero **no es un arreglo
dinámico en el sentido moderno**, y confundirlo es el error clásico.

`ODO` **no reserva memoria**: el compilador reserva siempre el máximo —cien elementos— y la variable
`N` dice **cuántos de ellos son válidos ahora mismo**. No crece nada; se declara cuánto cuenta.

¿Y para qué sirve entonces? Para lo que COBOL hace realmente: **registros de longitud variable**.

```cobol
01  PEDIDO.
    05  CABECERA.
        10  NUM-LINEAS  PIC 9(3).
    05  LINEA-PEDIDO OCCURS 1 TO 500 TIMES DEPENDING ON NUM-LINEAS.
        10  ARTICULO    PIC X(15).
        10  CANTIDAD    PIC 9(5).
```

Al escribir ese registro en un fichero, **la longitud escrita depende de `NUM-LINEAS`**: un pedido de
tres líneas ocupa mucho menos que uno de quinientas. Eso es lo que resuelve `ODO`, y lo resuelve bien
desde hace cincuenta años.

Las reglas que lo acompañan son estrictas: la variable de control debe estar **antes** en el registro,
solo puede haber **un `ODO` por grupo**, y tiene que ser **el último elemento**. Y hay una trampa
conocida: si `N` vale 0 y la cláusula empieza en 1, el comportamiento es indefinido en varios
compiladores.

Para memoria realmente dinámica, COBOL moderno tiene `ALLOCATE` y `FREE` sobre `BASED`, que llegaron
en el estándar de 2002 y siguen siendo raros en producción.
"""),
        "fortran": ("""
program lista
   implicit none
   integer, allocatable :: v(:)
   integer :: n, ios, i
   character(len=400) :: linea, salida
   character(len=20)  :: buf

   read(*, '(A)') linea

   n = 0
   do i = 1, 100
      if (allocated(v)) deallocate(v)
      allocate(v(i))                       ! reserva EN EJECUCIÓN
      read(linea, *, iostat=ios) v
      if (ios /= 0) exit
      n = i
   end do

   if (allocated(v)) deallocate(v)
   allocate(v(n))
   read(linea, *) v

   salida = ''
   do i = n, 1, -1
      write(buf, '(I0)') v(i)
      if (i == n) then
         salida = trim(buf)
      else
         salida = trim(salida) // '-' // trim(buf)
      end if
   end do

   write(*, '(A)') 'invertido=' // trim(salida)
end program lista
""", """
**Lo que esta clase enseña en Fortran.** **`allocatable`** llegó con Fortran 90 y es una de las
mejores decisiones del lenguaje, porque resuelve la memoria dinámica **sin punteros**.

```fortran
integer, allocatable :: v(:)
allocate(v(n))
deallocate(v)
```

Y la propiedad clave es esta: **un `allocatable` se libera solo al salir de su ámbito**. No hay fugas
posibles por olvido, no hace falta un destructor y no hay que escribir `deallocate` en cada camino de
salida.

Fortran tiene además **punteros** (`pointer`), y la comparación explica por qué se prefiere
`allocatable`:

| | `allocatable` | `pointer` |
|---|---|---|
| Puede tener alias | No | Sí |
| Se libera al salir del ámbito | **Sí** | No |
| Puede quedar colgado | No | Sí |
| El compilador puede optimizar | **Sí** | Menos |

Como un `allocatable` **no puede tener alias**, el compilador sabe que nadie más escribe en esa
memoria y puede vectorizar con libertad. Es la misma información que en C hay que prometer a mano con
`restrict`.

Fortran 2003 añadió dos comodidades que hoy son idiomáticas:

```fortran
v = [1, 2, 3]                    ! asignación con REASIGNACIÓN automática
w = [v, 4]                       ! crece copiando; simple, pero O(n)
call move_alloc(nuevo, v)        ! TRANSFIERE la reserva, sin copiar
```

`move_alloc` es la operación de movimiento de la clase 081, y llegó en 2003 — ocho años antes que
`std::move`.

El programa de arriba usa el idioma de "probar tamaños crecientes" porque **Fortran no tiene una forma
directa de saber cuántos números hay en una línea**: la lectura con formato libre falla cuando pide
más de los que hay, y ese fallo es la señal.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Containers.Vectors;

procedure Lista is
   package Vectores is new Ada.Containers.Vectors
     (Index_Type => Positive, Element_Type => Integer);
   use Vectores;

   V      : Vector;
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
      V.Append (Valor);
      Pos := Fin + 1;
   end loop;

   Put ("invertido=");
   for I in reverse 1 .. Integer (V.Length) loop
      Put (V.Element (I), Width => 1);
      if I > 1 then
         Put ("-");
      end if;
   end loop;
   New_Line;
end Lista;
""", """
**Lo que esta clase enseña en Ada.** Ada tardó **veintidós años** en tener contenedores estándar: el
lenguaje es de 1983 y `Ada.Containers` llegó con Ada 2005. Hasta entonces, cada proyecto escribía los
suyos o compraba una biblioteca.

Ese retraso tiene una explicación coherente con el resto del lenguaje: Ada nació para sistemas
empotrados y de tiempo real, donde **la reserva dinámica de memoria está prohibida por norma**. En
aviónica certificada bajo DO-178C, un `new` en pleno vuelo es inaceptable porque no se puede acotar su
tiempo ni garantizar que haya memoria.

Por eso el idioma dominante en Ada crítico sigue siendo **reservar todo al arrancar**, con arreglos de
tamaño máximo. Y por eso el perfil **`pragma Restrictions (No_Implicit_Heap_Allocations)`** existe:
para que el compilador **rechace** cualquier reserva no declarada.

Cuando sí se puede usar memoria dinámica, `Ada.Containers` es completo —`Vectors`, `Doubly_Linked_
Lists`, `Ordered_Maps`, `Hashed_Sets`, `Indefinite_*` para elementos de tamaño variable— y tiene un
rasgo poco común: **casi todo el paquete lleva contratos formales** (`Pre`, `Post`) y existe una
variante `Formal_*` verificable con SPARK.

Fíjate en la instanciación:

```ada
package Vectores is new Ada.Containers.Vectors
  (Index_Type => Positive, Element_Type => Integer);
```

Es el genérico de la clase 078: **hay que instanciarlo explícitamente y darle un nombre**. Más
verboso que `vector<int>` de C++, y con una ventaja concreta — el nombre `Vectores` aparece en los
mensajes de error en lugar de una plantilla expandida de diez líneas.
"""),
        "pascal": ("""
program Lista;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  V: array of Integer;              { arreglo dinámico }
  Linea, Salida, Tok: string;
  I: Integer;
  C: Char;

begin
  ReadLn(Linea);

  SetLength(V, 0);
  Tok := '';
  for I := 1 to Length(Linea) + 1 do
  begin
    if I <= Length(Linea) then C := Linea[I] else C := ' ';
    if C = ' ' then
    begin
      if Tok <> '' then
      begin
        SetLength(V, Length(V) + 1);      { crece en tiempo de ejecución }
        V[High(V)] := StrToInt(Tok);
        Tok := '';
      end;
    end
    else
      Tok := Tok + C;
  end;

  Salida := '';
  for I := High(V) downto 0 do
  begin
    if Salida <> '' then Salida := Salida + '-';
    Salida := Salida + IntToStr(V[I]);
  end;

  WriteLn('invertido=', Salida);
end.
""", """
**Lo que esta clase enseña en Pascal.** Los **arreglos dinámicos** —`array of T` sin límites— llegaron
con Delphi 4 (1998), y tienen una propiedad que hay que conocer porque sorprende: **empiezan en 0**,
mientras que los estáticos empiezan donde diga su declaración.

```pascal
var
  A: array[1..3] of Integer;   { índices 1, 2, 3 }
  B: array of Integer;          { índices 0 .. Length(B)-1 }
```

Por eso `Low(B)` siempre vale 0 y el bucle correcto es `for I := 0 to High(B)`.

Y son **contados por referencia**, como las cadenas largas: asignar `B := A` **no copia**, comparte;
la copia solo ocurre al escribir, o si se pide con `Copy(A)` o `SetLength` sobre una referencia
compartida. Es *copy-on-write*, con la ventaja de que pasar un arreglo grande a una función es
gratis, y la trampa de que modificarlo puede afectar a otro.

`SetLength` **conserva el contenido** al crecer o encoger, así que el idioma de este programa
—`SetLength(V, Length(V) + 1)` en cada elemento— funciona. Y es **cuadrático**: cada crecimiento
puede copiar todo el arreglo. Para volúmenes grandes, el idioma correcto es reservar de más y ajustar
al final, o usar `TList<T>` de `Generics.Collections`, que duplica la capacidad como `std::vector`.

Pascal tiene además la estructura de datos que Wirth puso en el centro de su libro: **el registro con
puntero**, que es la lista enlazada.

```pascal
type
  PNodo = ^TNodo;
  TNodo = record
    Valor: Integer;
    Siguiente: PNodo;
  end;
```

*Algorithms + Data Structures = Programs* (1976) enseñó a una generación entera a construir listas,
árboles y grafos exactamente así, y esa notación `^` sigue siendo la más clara para explicarlo.
"""),
        "lisp": ("""
(let ((v (make-array 0 :adjustable t :fill-pointer t)))
  (loop for x = (read *standard-input* nil nil)
        while x
        do (vector-push-extend x v))          ; crece sola

  (format t "invertido=~{~D~^-~}~%"
          (coerce (reverse v) 'list)))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp tiene **las dos** estructuras de esta clase, y la
elección entre ellas es una de las decisiones de rendimiento más importantes del lenguaje.

**La lista enlazada** es la estructura fundacional, de 1958. Cada elemento es un *cons*: un par de
dos punteros, el elemento y el resto.

```lisp
(list 1 2 3)          ; tres conses encadenados
(car lista)           ; el primero -- O(1)
(cdr lista)           ; el resto -- O(1)
(nth 500 lista)       ; el elemento 500 -- O(n), recorre 500 punteros
(push x lista)        ; añadir POR DELANTE -- O(1)
```

Añadir al principio es gratis; acceder por índice es lineal. **Y ese es el motivo de que tantos
algoritmos clásicos de Lisp construyan la lista al revés y la inviertan al final** — un idioma que
sorprende hasta que se entiende el coste.

**El vector ajustable** es la otra opción, y es lo que usa este programa:

```lisp
(make-array 0 :adjustable t :fill-pointer t)
(vector-push-extend x v)      ; O(1) amortizado, como std::vector
```

`:fill-pointer` es la idea elegante: el vector tiene una **capacidad** y un **relleno**, y
`vector-push-extend` incrementa el segundo y amplía la primera cuando hace falta. Es exactamente el
modelo de `std::vector`, con nombres de 1984.

Y una advertencia de rendimiento: **un vector ajustable no puede ser un vector simple**, así que
`aref` sobre él pasa por una indirección extra. Cuando el tamaño final se conoce, `make-array` de
tamaño fijo es notablemente más rápido.

`~{~D~^-~}` en el `format` es la directiva de iteración sobre una lista, con `~^` como separador que
**no se imprime tras el último elemento**. Resuelve el problema del `join` en una sola directiva.
"""),
        "tcl": ("""
gets stdin linea
set v [split [string trim $linea]]

puts "invertido=[join [lreverse $v] -]"
""", """
**Lo que esta clase enseña en Tcl.** Tres líneas, porque **la lista de Tcl ya es dinámica** y el
lenguaje trae `lreverse` y `join` como comandos.

Lo interesante está debajo. Una lista de Tcl **parece una cadena** —se puede imprimir, comparar y
pasar como texto— y **se almacena como un vector de punteros a objetos**. Desde Tcl 8.0, cada valor
lleva las dos representaciones y el intérprete convierte entre ellas cuando hace falta, guardando el
resultado.

```tcl
set v {1 2 3}          ;# nace como cadena
lindex $v 1            ;# se convierte a lista y SE QUEDA así
llength $v             ;# ya no reanaliza nada
```

Esa conversión perezosa con memoria —*shimmering*, la llaman— es lo que hace que Tcl sea mucho más
rápido de lo que su sintaxis sugiere. Y también es su trampa de rendimiento más conocida: **alternar
usos hace que el valor se reconvierta una y otra vez**.

```tcl
foreach x $v { append texto $x }     ;# lista → cadena → lista → ... en cada vuelta
```

Sobre el crecimiento, `lappend` es **O(1) amortizado** porque escribe sobre la representación interna
sin regenerar la cadena — siempre que el nombre de la variable se pase sin `$`:

```tcl
lappend v 4            ;# rápido: modifica en el sitio
set v [concat $v 4]    ;# lento: copia la lista entera
```

Y desde Tcl 8.5 existe **`dict`** como estructura hermana, y desde 8.6 los **`lmap`**, `lreverse` y
`lsearch -sorted`. La lista sigue siendo el caballo de batalla: en Tcl, un comando *es* una lista, así
que la estructura de datos y la estructura del programa son la misma cosa.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my @v = split ' ', $linea;

print "invertido=", join('-', reverse @v), "\\n";
""", """
**Lo que esta clase enseña en Perl.** En Perl **no existe el arreglo estático**: `@v` es siempre
dinámica, y crece y encoge con cuatro operaciones que cubren pila y cola a la vez.

```perl
push    @v, $x;     # añadir al final     -- O(1) amortizado
pop     @v;         # quitar del final    -- O(1)
unshift @v, $x;     # añadir al principio -- O(n) en general
shift   @v;         # quitar del principio -- O(1), está OPTIMIZADO
splice  @v, 2, 1;   # quitar/insertar en cualquier posición
```

`shift` siendo O(1) es un detalle de implementación deliberado: Perl guarda un desplazamiento al
inicio del bloque reservado, así que quitar el primer elemento no mueve nada. Por eso el idioma
`while (my $x = shift @cola)` es eficiente, y por eso `shift` sin argumentos —que saca de `@_`— es la
forma canónica de leer los parámetros de una función (clase 077).

Y hay una decisión de diseño que hay que tener presente: **`reverse` cambia de significado según el
contexto**.

```perl
reverse @v              # en contexto de lista: invierte la LISTA
scalar reverse $texto   # en contexto escalar: invierte la CADENA
```

Es el contexto de la clase 059 aplicado a una función, y es una de las cosas que más se le reprochan
al lenguaje. También es una de las que lo hacen conciso.

Sobre la memoria: los arreglos de Perl guardan **punteros a escalares**, no valores, así que un
arreglo de un millón de enteros ocupa bastante más que en C. Cuando eso importa, la respuesta del
ecosistema es **PDL** (*Perl Data Language*), que da arreglos numéricos compactos con operaciones
vectorizadas — el NumPy de Perl, y anterior a él.
"""),
        "cpp": ("""
#include <iostream>
#include <iterator>
#include <vector>

int main() {
    std::vector<int> v{std::istream_iterator<int>(std::cin),
                       std::istream_iterator<int>()};

    std::cout << "invertido=";
    for (auto it = v.rbegin(); it != v.rend(); ++it) {
        if (it != v.rbegin()) std::cout << '-';
        std::cout << *it;
    }
    std::cout << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** `std::vector` es el contenedor por defecto de C++ y **el ejemplo
canónico de crecimiento amortizado**: cuando se llena, reserva el doble, copia —o mueve, desde
C++11— y libera lo viejo. Añadir un elemento es O(1) en promedio aunque una vuelta de cada n cueste
O(n).

De ahí salen dos conceptos que hay que distinguir y que casi todo el mundo confunde al principio:

```cpp
v.size()        // cuántos elementos HAY
v.capacity()    // para cuántos hay SITIO reservado
v.reserve(1000) // reserva sitio sin crear elementos -- evita las recopias
v.shrink_to_fit()
```

`reserve` antes de un bucle de inserciones es la optimización más rentable y más olvidada de C++.

Y la propiedad que hace a `vector` ganar casi siempre frente a `std::list` es la **contigüidad**: sus
elementos están pegados en memoria, así que recorrerlo aprovecha la caché al máximo. Una lista
enlazada, con un salto de puntero por elemento, puede ser **diez veces más lenta de recorrer** aunque
insertar en medio sea teóricamente más barato. Es la lección práctica más repetida de la última
década: *la complejidad asintótica no es el único coste*.

Cuidado con la trampa clásica: **las referencias, punteros e iteradores a un `vector` se invalidan
cuando crece**.

```cpp
int& r = v[0];
v.push_back(42);      // puede REUBICAR todo
r = 7;                //  <-- comportamiento indefinido
```

Y una nota que sorprende a todo el mundo: **`std::vector<bool>` no es un vector de `bool`**. Es una
especialización que empaqueta bits, no cumple los requisitos de contenedor y `operator[]` no devuelve
una referencia de verdad. Es el error de diseño más famoso de la biblioteca estándar; la alternativa
es `std::deque<bool>` o `std::vector<char>`.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi LISTA;
  entrada char(200) const;
end-pi;

dcl-s elem   int(10) dim(100);
dcl-s n      int(10) inz(0);
dcl-s i      int(10);
dcl-s tok    varchar(20) inz('');
dcl-s c      char(1);
dcl-s salida varchar(200) inz('');

for i = 1 to %len(%trimr(entrada)) + 1;
  if i <= %len(%trimr(entrada));
    c = %subst(entrada : i : 1);
  else;
    c = ' ';
  endif;
  if c = ' ';
    if tok <> '';
      n += 1;
      elem(n) = %int(tok);
      tok = '';
    endif;
  else;
    tok += c;
  endif;
endfor;

for i = n downto 1;
  if salida <> '';
    salida += '-';
  endif;
  salida += %char(elem(i));
endfor;

dsply ('invertido=' + salida);

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG es de la misma generación que COBOL y comparte su punto de
partida: **la tabla se declara con un tamaño máximo y se lleva un contador aparte**.

Lo que sí aportó ILE es el **`varchar`** que usa este programa, y que resuelve el problema equivalente
para el texto:

```rpgle
dcl-s tok varchar(20);      // longitud VARIABLE, con prefijo de 2 bytes
dcl-s fijo char(20);        // siempre 20, rellenado con espacios
```

Un `char(20)` **siempre ocupa veinte posiciones rellenas de espacios**, de ahí que todo el código RPG
y COBOL clásico esté lleno de `%trim`. Un `varchar` guarda su longitud real, así que `tok += c`
funciona como en cualquier lenguaje moderno. Es una diferencia pequeña que cambia por completo cómo se
escribe el manejo de cadenas.

Para tamaño realmente dinámico, RPG tiene desde ILE la reserva explícita, heredada de C:

```rpgle
dcl-s p pointer;
dcl-s tabla int(10) dim(32767) based(p);   // la tabla vive DONDE APUNTE p

p = %alloc(n * 4);            // reservar
p = %realloc(p : m * 4);      // redimensionar
dealloc p;                     // liberar
```

`based(p)` declara una estructura **sin memoria propia**: se superpone a donde apunte el puntero. Es
el `BASED` de PL/I y de COBOL, y es cómo se hacen tablas verdaderamente dinámicas en RPG.

El `dim(32767)` de la declaración no reserva nada: solo dice al compilador cómo calcular los
desplazamientos. Y eso significa que **el índice no se comprueba contra `n`**, así que aquí RPG pierde
la seguridad que tenía con las tablas normales.
"""),
        "pli": ("""
 lista: procedure options(main);

    declare linea char(200) varying;
    declare v(100) fixed binary(31);
    declare (n, i) fixed binary(31);
    declare salida char(200) varying initial('');
    declare tok char(20) varying initial('');
    declare c char(1);

    get edit (linea) (a(200));
    n = 0;

    do i = 1 to length(linea) + 1;
       if i <= length(linea) then c = substr(linea, i, 1); else c = ' ';
       if c = ' ' then do;
          if tok ^= '' then do;
             n = n + 1;
             v(n) = tok;
             tok = '';
          end;
       end;
       else tok = tok || c;
    end;

    do i = n to 1 by -1;
       if salida ^= '' then salida = salida || '-';
       salida = salida || trim(char(v(i)));
    end;

    put skip list ('invertido=' || salida);

 end lista;
""", """
**Lo que esta clase enseña en PL/I.** PL/I tuvo memoria dinámica **en 1964**, con una sofisticación
que Fortran no alcanzó hasta 1990 y C hasta 1972.

```pli
declare v(100) fixed binary(31) controlled;   /* pila de reservas */
allocate v;
free v;
```

**`controlled`** no es solo "reservable": es una **pila**. Cada `allocate` sobre la misma variable
apila una nueva reserva y **oculta la anterior**; cada `free` desapila y **recupera la de debajo**.

```pli
allocate v;        /* v es la primera */
allocate v;        /* v es la segunda; la primera sigue viva, tapada */
free v;            /* v vuelve a ser la primera */
```

Es una estructura que ningún lenguaje del núcleo tiene, y que resuelve la recursión con estado sin
pasar parámetros. También es una fuente de confusión notable al leer código ajeno.

Y hay una segunda forma, la que se usa para listas enlazadas y árboles:

```pli
declare 1 nodo based(p),
          2 valor fixed binary(31),
          2 siguiente pointer;

allocate nodo set(p);          /* reserva y deja el puntero en p */
```

**`based`** es la declaración de una plantilla **sin memoria**: describe cómo interpretar lo que haya
donde apunte `p`. Es de donde lo tomaron COBOL, RPG y, en espíritu, el `struct` + `malloc` de C.

Además, `allocate` puede tener un **tamaño decidido en ejecución** mediante `refer`, que es el
`OCCURS DEPENDING ON` de COBOL pero sobre memoria reservada de verdad:

```pli
declare 1 tabla based(q),
          2 n fixed binary(31),
          2 elem(m refer(n)) fixed binary(31);
```

Reserva exactamente `m` elementos y guarda ese tamaño **dentro de la propia estructura**. Es un
arreglo dinámico autodescriptivo, de 1964.
"""),
        "mumps": ("""
LISTA ; Listas dinamicas -- clase 090
 read linea
 set n = $length(linea, " ")
 for i=1:1:n set v(i) = $piece(linea, " ", i)
 set salida = ""
 for i=n:-1:1 do
 . if salida '= "" set salida = salida _ "-"
 . set salida = salida _ v(i)
 write "invertido=", salida, !
 quit
""", """
**Lo que esta clase enseña en M.** En M **no hay nada que declarar y nada que reservar**: `set v(i)=x`
crea el elemento, y el árbol crece solo. No existe `allocate`, no existe `SetLength` y no existe
`push_back`.

Y hay una función que resuelve esta clase entera y que conviene conocer, porque explica por qué M
manipula texto tan bien: **`$piece`**.

```mumps
 set $piece(linea, " ", 3) = "nuevo"     ; ASIGNAR a la tercera pieza
 write $piece(linea, " ", 2)              ; leer la segunda
 write $length(linea, " ")                ; cuántas piezas hay
 write $piece(linea, " ", 2, 4)           ; un TRAMO de piezas
```

`$piece` trata una cadena como una lista delimitada, con acceso por posición **y asignación en el
sitio**. Que se pueda escribir `set $piece(...)` —una función a la izquierda del `=`— es
característico de M y no lo tiene ningún otro lenguaje de esta página.

Ese mecanismo es el que sostiene el formato de datos de VistA: un registro se guarda como una cadena
con piezas separadas por `^`, y los campos se leen y escriben con `$piece`.

```mumps
 set ^PAC(id, 0) = nombre_"^"_fecha_"^"_sexo
 set nombre = $piece(^PAC(id, 0), "^", 1)
```

Es serialización sin biblioteca: **la estructura y su representación en disco son la misma cadena**.
Es frágil —cambiar el orden de las piezas rompe todo el código que las lee— y es extraordinariamente
compacto y rápido, y por eso lleva cuarenta años en producción.

Para listas que necesitan orden y recorrido, lo natural es el subíndice numérico con `$order`, que ya
mantiene el orden sin coste añadido.
"""),
        "smalltalk": ("""
| v salida |

v := stdin nextLine substrings collect: [ :cada | cada asNumber ].

salida := ((v reverse) collect: [ :cada | cada printString ])
              inject: '' into: [ :acc :cada |
                  acc isEmpty ifTrue: [ cada ] ifFalse: [ acc, '-', cada ] ].

Transcript show: 'invertido=', salida; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** La colección dinámica de Smalltalk es
**`OrderedCollection`**, y su nombre dice exactamente lo que es: una colección con orden que crece
sola.

```smalltalk
| c |
c := OrderedCollection new.
c add: 1; add: 2.
c addFirst: 0.          "insertar al principio -- barato"
c removeLast.
c addAll: otraColeccion.
```

Internamente es un arreglo con **hueco por los dos extremos**, así que `addFirst:` y `add:` son ambas
O(1) amortizado — a diferencia de `std::vector`, donde insertar al principio es lineal. Es el mismo
diseño que `std::deque`.

Lo que hace distinta a esta clase en Smalltalk es que **la conversión entre colecciones es un
mensaje**:

```smalltalk
coleccion asArray
coleccion asOrderedCollection
coleccion asSet              "elimina duplicados (clase 094)"
coleccion asBag              "cuenta repeticiones (clase 095)"
coleccion asSortedCollection "ordena"
```

Cambiar de estructura de datos es una palabra. Y como el protocolo es común (clase 089), el resto del
código no cambia.

`collect:` es el `map`, y **devuelve una colección de la misma especie que la receptora** —un `Array`
devuelve `Array`, un `Set` devuelve `Set`—. Esa regla, llamada *species*, es la que hace que las
cadenas de mensajes se compongan sin sorpresas.

Y `substrings` sobre una cadena, sin argumentos, parte por espacios en blanco. Es un ejemplo de la
filosofía de la biblioteca: **el caso más común no lleva parámetros**.
"""),
    },
)

# ---------------------------------------------------------------------------
# 091 — Tuplas y registros posicionales
# ---------------------------------------------------------------------------
SPECS["091"] = dict(
    gancho="""
Dos valores que viajan juntos y se intercambian. Es la estructura de datos más pequeña que existe, y
la que mejor muestra un cambio de mentalidad: **ninguno de estos doce lenguajes tiene tuplas
anónimas**, y todos resuelven el problema declarando un tipo con nombre. Que hoy nos parezca pesado
dice más de nuestra época que de la suya — porque el tipo con nombre **documenta qué es cada
componente**.
""",
    porque="""
Aquí el concepto es el **agregado posicional**, y estos lenguajes lo enseñan por contraste. La tupla
moderna —`(a, b)` sin declarar nada— es cómoda y **anónima**: `p.0` y `p.1` no dicen qué son. El
**registro** de COBOL, Fortran, Ada, Pascal y PL/I obliga a declarar el tipo y a nombrar los campos, y
a cambio el compilador comprueba que no confundas dos pares distintos.

**Ada** añade algo que ningún lenguaje moderno tiene: **el agregado con nombres**, `(A => X, B => Y)`,
que hace imposible construir el registro con los campos cambiados de orden.
""",
    cierre="""
Lo transferible: **la tupla es cómoda para lo efímero y mala para lo que dura**. Devolver dos valores
de una función es un uso legítimo; guardar una tupla en una estructura que vivirá años significa que
dentro de seis meses alguien leerá `p.1` sin saber qué es. La regla práctica que se deduce de esta
página es la que aplican los lenguajes viejos por obligación y los nuevos por disciplina: **en cuanto
el par cruza una frontera de módulo, dale nombre a los campos**.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. TUPLA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TXT-A   PIC X(20).
01  TXT-B   PIC X(20).
01  PAR.
    05  PRIMERO  PIC S9(9) COMP-3.
    05  SEGUNDO  PIC S9(9) COMP-3.
01  TMP     PIC S9(9) COMP-3.
01  ED-1    PIC -(8)9.
01  ED-2    PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    COMPUTE PRIMERO = FUNCTION NUMVAL(TXT-A)
    COMPUTE SEGUNDO = FUNCTION NUMVAL(TXT-B)

    MOVE PRIMERO TO TMP
    MOVE SEGUNDO TO PRIMERO
    MOVE TMP     TO SEGUNDO

    MOVE PRIMERO TO ED-1
    MOVE SEGUNDO TO ED-2
    DISPLAY "tupla=(" FUNCTION TRIM(ED-1)
            ", " FUNCTION TRIM(ED-2) ")"
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** El **grupo** —un `01` con campos `05` debajo— es el registro de
COBOL, y es la estructura sobre la que está construido todo el lenguaje.

Tiene una propiedad que los lenguajes modernos perdieron y que aquí importa: **un grupo es a la vez
una estructura y una cadena de caracteres**.

```cobol
01  PAR.
    05  PRIMERO  PIC S9(9) COMP-3.
    05  SEGUNDO  PIC S9(9) COMP-3.

MOVE PAR TO OTRO-GRUPO      *> copia los bytes, sin mirar los campos
DISPLAY PAR                  *> muestra la representación cruda
WRITE REGISTRO FROM PAR      *> escribe en fichero tal cual
```

Un `MOVE` de grupo a grupo es una **copia de bytes**, no una asignación campo a campo. Si los dos
grupos tienen distinta estructura, COBOL **no se queja**: copia y el resultado es basura. Es la
contrapartida de que el registro sea, literalmente, el formato del fichero.

Y de ahí sale **`REDEFINES`**, que es ver los mismos bytes con dos estructuras distintas:

```cobol
01  FECHA-TEXTO  PIC X(8).
01  FECHA-PARTES REDEFINES FECHA-TEXTO.
    05  ANIO  PIC 9(4).
    05  MES   PIC 9(2).
    05  DIA   PIC 9(2).
```

Es la unión de C y el `equivalence` de Fortran, con una diferencia importante: **es lo normal en
COBOL, no un recurso excepcional**, porque los ficheros de longitud fija con campos posicionales son
el pan de cada día.

COBOL-2002 añadió `TYPEDEF`, que permite declarar la estructura una vez y reutilizarla, pero el
copybook (clase 088) sigue siendo la forma habitual de compartir un registro entre programas.
"""),
        "fortran": ("""
program tuplas
   implicit none

   type :: par
      integer :: a, b
   end type par

   type(par) :: p, q

   read(*, *) p%a, p%b

   q = par(p%b, p%a)          ! constructor posicional del tipo

   write(*, '(A,I0,A,I0,A)') 'tupla=(', q%a, ', ', q%b, ')'
end program tuplas
""", """
**Lo que esta clase enseña en Fortran.** Los **tipos derivados** llegaron con Fortran 90, y con ellos
el **constructor** que se ve en la línea `q = par(p%b, p%a)`: el nombre del tipo usado como función.

Antes de 1990, Fortran **no tenía registros**. La forma de agrupar datos era `COMMON` (clase 086) o
arreglos paralelos:

```fortran
      REAL X(1000), Y(1000), Z(1000)      ! tres arreglos "en paralelo"
```

Ese idioma no ha desaparecido, y no por pereza: es lo que hoy se llama **estructura de arreglos**
(SoA) frente a **arreglo de estructuras** (AoS), y en cálculo numérico **suele ser más rápido**,
porque permite cargar 8 o 16 valores contiguos en un registro vectorial. Con un arreglo de
estructuras, los valores están intercalados y la vectorización se pierde.

Es un caso en el que la técnica "anticuada" sigue siendo la correcta, y merece decirlo con claridad.

El acceso con `%` en lugar de `.` tiene una explicación histórica: **`.` ya estaba ocupado** por los
operadores `.and.`, `.or.`, `.eq.`, herencia del Fortran de tarjetas, donde no había símbolos para
ellos.

Fortran 2003 añadió el constructor **con nombres de componente**, que es más legible y evita el error
de orden:

```fortran
q = par(a = p%b, b = p%a)
```

Y añadió `sequence`, `bind(c)` para interoperar con `struct` de C, componentes `allocatable` y
`pointer`, y tipos extensibles con `extends` — es decir, herencia. El tipo derivado dejó de ser un
agregado y pasó a ser una clase.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Tupla is
   type Par is record
      A, B : Integer;
   end record;

   P, Q : Par;
begin
   Get (P.A);
   Get (P.B);

   Q := (A => P.B, B => P.A);      --  agregado CON NOMBRES

   Put ("tupla=(");
   Put (Q.A, Width => 1);
   Put (", ");
   Put (Q.B, Width => 1);
   Put (")");
   New_Line;
end Tupla;
""", """
**Lo que esta clase enseña en Ada.** La línea `Q := (A => P.B, B => P.A);` es un **agregado con
asociación por nombre**, y es una de las mejores ideas de Ada que ningún lenguaje mayoritario copió.

Compara las dos formas:

```ada
Q := (P.B, P.A);                 --  posicional: hay que recordar el orden
Q := (A => P.B, B => P.A);       --  con nombres: imposible equivocarse
```

Con la segunda, **añadir un campo al registro o reordenarlo no rompe silenciosamente el código**: si
falta un campo, no compila. Con la primera —que es la única que ofrecen C, C++ hasta 2020, Fortran
hasta 2003 y casi todos los lenguajes de tuplas— reordenar dos campos del mismo tipo compila y cambia
el significado.

Y el agregado de Ada tiene más:

```ada
Q := (A => 0, others => 1);      --  "todos los demás"
Q := (P with delta A => 5);      --  Ada 2022: copia cambiando un campo
```

`others` obliga a cubrir todos los campos, y `with delta` es la actualización funcional que en otros
lenguajes se escribe con un *spread*.

Ada tiene además **registros variantes**, que son la unión discriminada de la clase 100 y llevan una
comprobación que C nunca tuvo:

```ada
type Figura (Clase : Tipo_Figura) is record
   case Clase is
      when Circulo    => Radio : Float;
      when Rectangulo => Ancho, Alto : Float;
   end case;
end record;
```

Acceder a `Radio` cuando `Clase` es `Rectangulo` lanza `Constraint_Error`. En C, la misma `union`
devuelve basura sin avisar. Cuarenta años de diferencia entre las dos aproximaciones.
"""),
        "pascal": ("""
program Tupla;
{$MODE OBJFPC}{$H+}
uses SysUtils;

type
  TPar = record
    A, B: Integer;
  end;

var
  P, Q: TPar;

begin
  Read(P.A, P.B);

  Q.A := P.B;
  Q.B := P.A;

  WriteLn('tupla=(', IntToStr(Q.A), ', ', IntToStr(Q.B), ')');
end.
""", """
**Lo que esta clase enseña en Pascal.** El **`record`** de Pascal es directamente el antepasado del
`struct` de C — Wirth lo tomó de Algol W y Ritchie lo tomó de ahí— y viene con una construcción que
Pascal tuvo y C nunca: **`with`**.

```pascal
with Q do
begin
  A := P.B;
  B := P.A;
end;
```

`with` abre el ámbito del registro para no repetir el nombre. Es cómodo y es **la característica más
discutida del lenguaje**: si el registro tiene un campo `A` y hay una variable `A` en el ámbito, gana
el campo, en silencio, y el código deja de hacer lo que parece. Delphi mantuvo `with` y las guías de
estilo modernas desaconsejan usarlo.

Pascal tiene también el **registro variante**, con la misma sintaxis que Ada pero **sin comprobación**:

```pascal
type
  TFigura = record
    case Clase: TTipoFigura of
      Circulo:    (Radio: Double);
      Rectangulo: (Ancho, Alto: Double);
  end;
```

Aquí el `case` es la unión de C con etiqueta, y **nada impide leer `Radio` de un rectángulo**. De
hecho, durante décadas fue la manera idiomática de reinterpretar bytes en Pascal, el equivalente del
`REDEFINES` de COBOL.

Free Pascal y Delphi modernos añadieron dos cosas que acercan el registro a la tupla:

```pascal
type
  TPunto = record
    X, Y: Integer;
    function Longitud: Double;                  { MÉTODOS en un record }
    class operator + (const A, B: TPunto): TPunto;  { operadores }
  end;
```

Un `record` con métodos y operadores, **con semántica de valor** —se copia al asignar, no hay
punteros, no hay `Create`/`Free`—. Es exactamente el `struct` de C# y el tipo valor de Swift.
"""),
        "lisp": ("""
(let* ((a (read))
       (b (read))
       (p (cons a b)))                 ; un CONS: el par original de Lisp
  (format t "tupla=(~D, ~D)~%" (cdr p) (car p)))
""", """
**Lo que esta clase enseña en Common Lisp.** El **cons** es la tupla de Lisp, y es la estructura de
datos más antigua del lenguaje: un par de dos punteros, `car` y `cdr`.

Los nombres son un fósil precioso: vienen del IBM 704 de 1958, donde `CAR` era *Contents of the
Address part of Register* y `CDR` *Contents of the Decrement part of Register* — dos mitades de una
palabra máquina. Sesenta y ocho años después, la nomenclatura sigue.

Con el cons se construye todo: **una lista es una cadena de conses cuyo `cdr` apunta al siguiente**. Y
un par suelto —`(cons 1 2)`, que se imprime `(1 . 2)`— es una tupla de dos.

Para más de dos componentes, Common Lisp ofrece cuatro opciones, en orden de disciplina creciente:

```lisp
(list a b c)                         ; lista: flexible, sin nombres, sin comprobación
(vector a b c)                       ; vector: acceso O(1)
(defstruct punto x y)                ; ESTRUCTURA: campos con nombre y tipo
(defclass punto () ((x) (y)))        ; clase CLOS: todo lo anterior más herencia
```

**`defstruct`** es la respuesta idiomática y genera mucho de una sola línea: el constructor
`make-punto`, los accesores `punto-x` y `punto-y` —usables con `setf`—, el predicado de tipo
`punto-p`, una función de copia y una impresión legible. Con `:type list` o `:type vector` incluso se
elige la representación subyacente.

Y `destructuring-bind` da la comodidad de la tupla moderna sobre cualquier lista:

```lisp
(destructuring-bind (a b &optional (c 0)) datos
  ...)
```

Es desestructuración con valores por defecto y parámetros con nombre — de 1984.
"""),
        "tcl": ("""
gets stdin linea
lassign [split [string trim $linea]] a b      ;# desestructuración

puts "tupla=($b, $a)"
""", """
**Lo que esta clase enseña en Tcl.** En Tcl **una tupla es una lista de dos elementos**, y `lassign`
la desmonta en variables — es la desestructuración de los lenguajes modernos, disponible desde Tcl
8.5.

```tcl
lassign {3 4} a b            ;# a=3, b=4
lassign {3} a b              ;# a=3, b="" -- los que faltan quedan VACÍOS
set sobrantes [lassign {1 2 3} a]   ;# devuelve lo que no se asignó
```

Que los elementos que faltan queden vacíos en lugar de fallar es la actitud de Tcl con los errores:
**no hay aridad que comprobar porque no hay tipo que comprobar**.

Para un registro con campos con nombre, la respuesta moderna es el **`dict`**, incorporado en 8.5:

```tcl
set p [dict create x 3 y 4]
dict get $p x
dict set p x 10
dict with p { puts "$x,$y" }      ;# expone las claves como VARIABLES
```

`dict with` es el `with` de Pascal, con el mismo riesgo y la misma comodidad — y con una ventaja: al
salir del bloque, los cambios en las variables **se escriben de vuelta al diccionario**.

Y un `dict` de Tcl **conserva el orden de inserción** y es un valor inmutable como todo en el
lenguaje: `dict set` devuelve un diccionario nuevo, aunque la implementación lo modifica en el sitio
cuando solo hay una referencia. Es el mismo truco de copia-al-escribir que las cadenas.

Para estructuras con comportamiento, TclOO (clase 087). Y para leer datos externos, `struct` del
paquete Tcllib y `binary scan`, que desmonta un búfer binario en campos con una cadena de formato.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($a, $b) = split ' ', $linea;

($a, $b) = ($b, $a);           # intercambio SIN variable temporal

print "tupla=($a, $b)\\n";
""", """
**Lo que esta clase enseña en Perl.** `($a, $b) = ($b, $a)` es una **asignación de lista**, y es
correcta por una razón concreta: **Perl evalúa por completo el lado derecho antes de asignar nada**.
No hace falta variable temporal, y no hay orden de asignación que pueda estropearlo.

Ese mismo mecanismo cubre casi todos los usos de tupla del lenguaje:

```perl
my ($x, $y, @resto) = @lista;      # desestructurar, con "el resto"
my ($nombre, $edad) = obtener();   # devolver DOS valores de una función
sub obtener { return ('Ada', 36) } # devolver una lista
```

Devolver varios valores es natural en Perl porque **una función devuelve una lista, no un valor**. Es
lo mismo que hace Lua y lo contrario que C, Java o C++ antes de `std::tuple`.

Y para el registro con nombres, el idioma dominante es el **hash**:

```perl
my %punto = (x => 3, y => 4);
my $ref   = { x => 3, y => 4 };      # una REFERENCIA a hash: eso es un objeto Perl
$ref->{x};
```

Un objeto de Perl 5 es, literalmente, una referencia a hash con el nombre de la clase pegado (`bless`).
Por eso los campos son accesibles desde fuera (clase 087) y por eso `Moose`, `Moo` y la nueva palabra
clave `class` existen.

Para tuplas con estructura fija y comprobada, CPAN tiene `Class::Struct` en el núcleo, y `Type::Tiny`
para validación. Pero el par suelto se resuelve con una lista, y esa es la respuesta idiomática.
"""),
        "cpp": ("""
#include <iostream>
#include <utility>

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::pair<int, int> p{a, b};
    auto [x, y] = p;                   // enlace estructurado (C++17)

    std::cout << "tupla=(" << y << ", " << x << ")\\n";
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ es el único lenguaje de esta página con **tuplas anónimas de
verdad**, y llegó a ellas por el camino largo.

```cpp
std::pair<int, int> p{1, 2};          // C++98: dos elementos, .first y .second
std::tuple<int, char, double> t{...}; // C++11: N elementos, std::get<0>(t)
auto [x, y] = p;                       // C++17: enlace estructurado
```

Los nombres `first` y `second` son exactamente el problema que esta clase quiere señalar: **no dicen
qué es cada componente**. `std::get<2>(t)` es todavía peor. Por eso la guía práctica es la del cierre:
pares y tuplas para lo efímero —devolver dos valores, una clave y su valor— y `struct` con nombres
para lo que dura.

El **enlace estructurado** de C++17 es la mejor pieza de este conjunto, porque funciona sobre las tres
cosas:

```cpp
auto [x, y] = p;                       // sobre un pair
auto [a, b, c] = t;                    // sobre un tuple
auto [nombre, edad] = persona;         // sobre un STRUCT propio, sin declarar nada
for (const auto& [clave, valor] : mapa) { ... }   // el uso más común
```

Ese último bucle sustituyó a `it->first` e `it->second`, y es probablemente la mejora de legibilidad
más agradecida de C++17.

Y C++20 añadió los **inicializadores designados**, que son el agregado con nombres de Ada... cuarenta
y dos años después, y con una restricción: **deben ir en el orden de declaración**.

```cpp
struct Punto { int x, y; };
Punto p{.x = 1, .y = 2};        // legal
Punto q{.y = 2, .x = 1};        // NO compila en C++, sí en C
```
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi TUPLA;
  a int(10) const;
  b int(10) const;
end-pi;

dcl-ds par qualified;         // estructura de datos con campos con nombre
  primero int(10);
  segundo int(10);
end-ds;

dcl-s tmp int(10);

par.primero = a;
par.segundo = b;

tmp = par.primero;
par.primero = par.segundo;
par.segundo = tmp;

dsply ('tupla=(' + %char(par.primero) + ', ' + %char(par.segundo) + ')');

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** La **estructura de datos** (`dcl-ds`) es el registro de RPG, y
lleva la misma dualidad que el grupo de COBOL: **es a la vez una estructura con campos y un bloque
contiguo de bytes**.

La palabra clave **`qualified`** es la que hay que mirar. Sin ella, los subcampos se declaran como
variables sueltas en el programa entero:

```rpgle
dcl-ds par;              // SIN qualified
  primero int(10);       //   -> se usa como `primero`, a secas
end-ds;

dcl-ds par qualified;    // CON qualified
  primero int(10);       //   -> se usa como `par.primero`
end-ds;
```

El comportamiento sin `qualified` es el heredado del RPG de tarjetas, donde todos los nombres eran
globales, y sigue siendo el defecto por compatibilidad. **La práctica moderna es poner `qualified`
siempre**, y es un buen ejemplo de cómo un lenguaje arrastra su historia en los valores por defecto.

RPG tiene además dos capacidades sobre estructuras que no tiene el núcleo:

```rpgle
dcl-ds fecha;
  completa char(8);
  anio     char(4) overlay(completa : 1);   // SOLAPAR campos: el REDEFINES
  mes      char(2) overlay(completa : 5);
  dia      char(2) overlay(completa : 7);
end-ds;

dcl-ds cliente likerec(CLIREG : *input);    // la estructura del REGISTRO DE FICHERO
```

`overlay` es el `REDEFINES` de COBOL. Y **`likerec`** es notable: declara una estructura **con la
forma exacta de un registro de la base de datos**, tomada del catálogo del sistema al compilar. Si
alguien añade una columna a la tabla, la estructura cambia sola al recompilar.

Es esquema-como-tipo, integrado en el lenguaje y en la base de datos a la vez — algo que hoy se
consigue con generadores de código.
"""),
        "pli": ("""
 tupla: procedure options(main);

    declare 1 par,
              2 primero fixed binary(31),
              2 segundo fixed binary(31);
    declare tmp fixed binary(31);

    get list (par.primero, par.segundo);

    tmp = par.primero;
    par.primero = par.segundo;
    par.segundo = tmp;

    put skip list ('tupla=(' || trim(char(par.primero)) ||
                   ', ' || trim(char(par.segundo)) || ')');

 end tupla;
""", """
**Lo que esta clase enseña en PL/I.** La estructura de PL/I se escribe con **números de nivel**, igual
que COBOL —los dos son de mediados de los sesenta y comparten esa herencia—:

```pli
declare 1 cliente,
          2 nombre char(30),
          2 direccion,
            3 calle char(40),
            3 ciudad char(20),
          2 saldo fixed decimal(11,2);
```

Y PL/I añade dos operaciones sobre estructuras que COBOL no tiene, y que son sorprendentemente
modernas.

**La asignación por nombre (`by name`)**, que copia **solo los campos que existen en ambas
estructuras**:

```pli
resumen = cliente, by name;
```

Si `resumen` tiene `nombre` y `saldo` pero no `direccion`, copia esos dos y ya. Es una proyección
estructural resuelta por el compilador, y es exactamente lo que hoy se hace a mano con un DTO o con
una biblioteca de mapeo.

**Las operaciones sobre estructuras completas**:

```pli
totales = totales + movimientos;    /* suma CAMPO A CAMPO, si las formas coinciden */
```

Que una suma se propague por toda una estructura no lo tiene ningún lenguaje del núcleo. Requiere que
las dos estructuras tengan la misma forma, y el compilador lo comprueba.

PL/I combina además estructuras y arreglos en las dos direcciones —arreglos de estructuras y
estructuras con campos que son arreglos— con la misma notación, algo que en 1964 no tenía nadie.

Lo que no tiene, como COBOL, es la tupla anónima: **hay que declarar la estructura**. Y como en COBOL,
esa obligación resulta ser una virtud cuando el dato dura veinte años.
"""),
        "mumps": ("""
TUPLA ; Tuplas y registros -- clase 091
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 set par = b _ "^" _ a                      ; la "tupla": una cadena con piezas
 write "tupla=(", $piece(par, "^", 1), ", ", $piece(par, "^", 2), ")", !
 quit
""", """
**Lo que esta clase enseña en M.** M no tiene registros, ni estructuras, ni tuplas, ni tipos. Tiene
**dos** formas de agrupar datos, y las dos son idiomáticas.

**La primera es la de este programa: una cadena con piezas separadas por `^`**, manipulada con
`$piece`.

```mumps
 set registro = nombre_"^"_fecha_"^"_sexo
 set nombre = $piece(registro, "^", 1)
```

Es la forma canónica de guardar un registro en VistA, y su ventaja es brutal en el contexto: **el
registro completo es un solo valor**, así que se escribe en un *global* con un `set`, se lee con un
acceso y se transmite sin serializar. Su inconveniente también es evidente: el significado de la
pieza 7 está en la documentación, no en el código.

**La segunda es el subíndice con nombre**, que es más legible y cuesta más accesos:

```mumps
 set paciente("nombre") = "Ada"
 set paciente("fecha")  = 18151210
```

Como los subíndices pueden ser cadenas, un array local de M **es** un registro con campos con nombre
— y además es un diccionario, un árbol y un conjunto, según cómo se use.

La capa que pone nombres encima es **FileMan**, el diccionario de datos de VistA (clase 087): define
qué campo es cada pieza de cada global, con su tipo, su validación y su ayuda. Es un catálogo de
esquemas construido sobre un lenguaje sin tipos, y lleva funcionando desde 1982.

Ese patrón —datos sin estructura en el lenguaje, esquema en una capa de metadatos— es exactamente lo
que hacen hoy las bases de datos documentales. M llegó cuarenta años antes.
"""),
        "smalltalk": ("""
| partes a b |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

Transcript
    show: 'tupla=(', b printString, ', ', a printString, ')';
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk **no tiene tuplas ni registros**, y no por
olvido: **tiene objetos**, y un objeto con dos variables de instancia es la respuesta a todo lo que
esta clase plantea.

```smalltalk
Object subclass: #Par
    instanceVariableNames: 'primero segundo'
    classVariableNames: ''
    package: 'Ejemplo'.

Par >> primero          ^primero
Par >> primero: unValor  primero := unValor
```

Para lo efímero, un `Array` de dos elementos hace las veces, y `first`/`second` son mensajes de la
biblioteca —también `third`, `fourth`... hasta `ninth`, que existen porque leen mejor que `at: 4`.

Y hay una construcción propia de Smalltalk que cubre el caso "par clave-valor" y que conviene conocer,
porque aparece por todas partes: **la asociación**.

```smalltalk
| a |
a := #nombre -> 'Ada'.       "la flecha crea una Association"
a key.                        "#nombre"
a value.                      "'Ada'"
```

`->` es un mensaje binario normal, no sintaxis especial, y devuelve un objeto `Association`. Es lo que
guarda un `Dictionary` en cada entrada, y por eso `dic associationsDo:` recorre pares.

Que el par clave-valor sea **un objeto con identidad propia**, y no una estructura anónima, es
coherente con el resto: en Smalltalk, si algo merece un nombre, merece una clase. Y la contrapartida
es la que se ve al principio de este programa — para dos números sueltos hay que decidir si valen un
`Array`, una `Association` o una clase nueva, y esa decisión no se puede posponer con una tupla
anónima.
"""),
    },
)
