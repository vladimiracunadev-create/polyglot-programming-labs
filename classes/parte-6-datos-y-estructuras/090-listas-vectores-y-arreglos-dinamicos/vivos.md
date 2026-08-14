# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 090

> [⬅️ Volver a la clase 090](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Una lista que no sabe cuántos elementos tendrá hasta que llega la entrada. Aquí aparece la costura
entre dos épocas: los lenguajes nacidos cuando **la memoria se reservaba entera al arrancar** —COBOL,
Fortran hasta 1990, RPG— y los que dan una estructura que crece sola. Y hay un dato incómodo:
**COBOL sí tiene tablas de tamaño variable desde 1974**, con `OCCURS DEPENDING ON`, y casi nadie lo
sabe.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **crecimiento en tiempo de ejecución**, y estos lenguajes lo enseñan porque
> enseñan lo que cuesta. **Fortran 90** trajo `allocatable`, y con él la pregunta de cuándo se libera;
> **Ada 95** trajo los contenedores estándar en 2005; **C++** tiene `std::vector`, que es el ejemplo
> canónico de crecimiento amortizado; y **COBOL** tiene `OCCURS DEPENDING ON`, que no reserva memoria
> sino que **describe cuánto del registro es válido**.
>
> Esa última distinción —crecer frente a describir— es la que separa el pensamiento de los años sesenta
> del actual, y merece entenderse bien.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con enteros separados por espacio → stdout: `invertido=<elementos en orden inverso unidos por ->`
- **Regla:** `invertido = reverse(lista)`

| stdin | esperado |
|---|---|
| `1 2 3` | `invertido=3-2-1` |
| `5` | `invertido=5` |
| `10 20 30 40` | `invertido=40-30-20-10` |

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
```

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

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
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
```

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

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
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
```

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

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
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
```

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

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((v (make-array 0 :adjustable t :fill-pointer t)))
  (loop for x = (read *standard-input* nil nil)
        while x
        do (vector-push-extend x v))          ; crece sola

  (format t "invertido=~{~D~^-~}~%"
          (coerce (reverse v) 'list)))
```

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

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set v [split [string trim $linea]]

puts "invertido=[join [lreverse $v] -]"
```

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

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my @v = split ' ', $linea;

print "invertido=", join('-', reverse @v), "\n";
```

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

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
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
    std::cout << '\n';
    return 0;
}
```

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
```

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

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
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
```

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

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
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
```

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

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| v salida |

v := stdin nextLine substrings collect: [ :cada | cada asNumber ].

salida := ((v reverse) collect: [ :cada | cada printString ])
              inject: '' into: [ :acc :cada |
                  acc isEmpty ifTrue: [ cada ] ifFalse: [ acc, '-', cada ] ].

Transcript show: 'invertido=', salida; cr.
```

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

---

## Y de vuelta a la clase

Lo transferible: **"dinámico" significa cosas distintas y conviene saber cuál tienes**. Un
`std::vector` reserva de más y duplica su capacidad; una lista enlazada reserva un nodo por elemento;
un `OCCURS DEPENDING ON` no reserva nada, solo declara cuánto del espacio ya reservado cuenta; y una
lista de Lisp o de Tcl esconde una representación interna que cambia según el uso. El coste de añadir
un elemento —constante amortizado, constante real o lineal— depende de cuál sea, y es la primera
pregunta que hay que hacerse al elegir.

⏮️ [Volver a la clase 090](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
