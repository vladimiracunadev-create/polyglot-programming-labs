# -*- coding: utf-8 -*-
"""Parte 6, lote D — clase 094. Ver `vivos_parte6.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 094 — Conjuntos (sets) y unicidad
# ---------------------------------------------------------------------------
SPECS["094"] = dict(
    gancho="""
Contar cuántos valores distintos hay. La operación es de una línea en los lenguajes que tienen
conjuntos, y de veinte en los que no — y aquí está el reparto exacto: **Pascal tuvo el tipo `set` en
1970, antes que nadie, y con una limitación que lo explica todo: como máximo 256 elementos**, porque
era una máscara de bits. COBOL, Fortran, RPG, PL/I y M no tienen conjuntos en absoluto.
""",
    porque="""
Aquí el concepto es la **colección sin orden ni repetición**, y estos lenguajes lo enseñan porque
muestran las dos implementaciones posibles y cuándo se inventó cada una. **La máscara de bits** de
Pascal: instantánea, con unión e intersección en una instrucción de máquina, y limitada a un universo
pequeño y conocido. **La tabla asociativa o el árbol**: Ada con `Ordered_Sets` y `Hashed_Sets`, C++
con `set` y `unordered_set`, Perl con un hash, Smalltalk con `Set`.

Y **Perl** aporta el idioma más citado de la historia del lenguaje: **un hash usado como conjunto**,
que resuelve la unicidad, el conteo y la pertenencia con la misma estructura.
""",
    cierre="""
Lo transferible: **antes de elegir un conjunto, pregunta cuál es el universo**. Si los valores
posibles son pocos y conocidos —días de la semana, códigos de estado, banderas— una máscara de bits
gana por varios órdenes de magnitud, y por eso Pascal la eligió y por eso `std::bitset`, `EnumSet` de
Java y los `flags` de C siguen existiendo. Si el universo es abierto, hace falta una tabla o un árbol,
y entonces la pregunta pasa a ser si necesitas orden. **Las dos respuestas siguen siendo correctas
según el caso, cincuenta y seis años después.**
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. UNICOS.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(2) COMP VALUE 0.
01  I       PIC 9(4) COMP.
01  J       PIC 9(4) COMP.
01  N       PIC 9(4) COMP VALUE 0.
01  VALOR   PIC S9(9) COMP-3.
01  NUEVO   PIC X VALUE "S".
01  TABLA.
    05  ELEM  PIC S9(9) COMP-3 OCCURS 100 TIMES.
01  ED-N    PIC Z(3)9.

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

    MOVE N TO ED-N
    DISPLAY "unicos=" FUNCTION TRIM(ED-N)
    STOP RUN.

CERRAR-TOKEN.
    IF TLEN > 0
        COMPUTE VALOR = FUNCTION NUMVAL(TOKEN)
        MOVE "S" TO NUEVO
        PERFORM VARYING J FROM 1 BY 1 UNTIL J > N
            IF ELEM(J) = VALOR
                MOVE "N" TO NUEVO
            END-IF
        END-PERFORM
        IF NUEVO = "S"
            ADD 1 TO N
            MOVE VALOR TO ELEM(N)
        END-IF
        MOVE SPACES TO TOKEN
        MOVE 0 TO TLEN
    END-IF.
""", """
**Lo que esta clase enseña en COBOL.** **COBOL no tiene conjuntos**, y la respuesta es la de este
programa: una tabla y una búsqueda lineal por cada elemento. Es O(n²), y para las tablas pequeñas de
un programa de negocio no importa.

Cuando sí importa, COBOL ofrece **`SEARCH ALL`**, que es búsqueda binaria integrada en el lenguaje:

```cobol
01  TABLA.
    05  ENTRADA OCCURS 1000 TIMES
        ASCENDING KEY IS COD-CLIENTE
        INDEXED BY IDX.
        10  COD-CLIENTE  PIC X(10).
        10  NOMBRE       PIC X(40).

SEARCH ALL ENTRADA
    AT END      DISPLAY "no encontrado"
    WHEN COD-CLIENTE(IDX) = BUSCADO
        DISPLAY NOMBRE(IDX)
END-SEARCH
```

`ASCENDING KEY` declara que la tabla está ordenada por ese campo, y **el compilador genera la búsqueda
binaria**. Con `SEARCH` a secas es lineal. Es la única estructura de datos con complejidad garantizada
que trae COBOL, y muy poca gente la conoce — se ve más el bucle escrito a mano.

Para la unicidad de verdad, la respuesta idiomática en un sistema COBOL no está en el lenguaje: está
**fuera**.

```text
SORT ENTRADA UNIQUE FIELDS=(1,10,CH,A)     -- la utilidad SORT de z/OS
```

O un índice único en DB2, o un fichero VSAM con clave. En un mainframe, **eliminar duplicados de un
fichero de cien millones de registros se hace con DFSORT o SyncSort, no con un programa**, y esas
utilidades están tan optimizadas que competir con ellas desde COBOL no tiene sentido.

Es una lección de arquitectura que sigue vigente: la estructura de datos correcta a veces no está en
el lenguaje sino en la plataforma.
"""),
        "fortran": ("""
program unicos
   implicit none
   integer :: v(100), n, ios, i, j, cuenta
   character(len=400) :: linea
   logical :: repetido

   read(*, '(A)') linea

   n = 0
   do i = 1, 100
      read(linea, *, iostat=ios) v(1:i)
      if (ios /= 0) exit
      n = i
   end do

   cuenta = 0
   do i = 1, n
      repetido = .false.
      do j = 1, i - 1
         if (v(j) == v(i)) repetido = .true.
      end do
      if (.not. repetido) cuenta = cuenta + 1
   end do

   write(*, '(A,I0)') 'unicos=', cuenta
end program unicos
""", """
**Lo que esta clase enseña en Fortran.** **Fortran no tiene conjuntos ni tablas asociativas**, y no
por descuido: el lenguaje se diseñó para álgebra sobre arreglos densos, no para estructuras de datos
generales, y esa sigue siendo su especialidad.

Lo que sí tiene, y resuelve muchos casos de esta clase sin bucle, son las **funciones sobre máscaras
lógicas**:

```fortran
count(v == 3)              ! cuántos elementos valen 3
any(v > 100)               ! ¿hay alguno?
all(v >= 0)                ! ¿todos?
pack(v, v > 0)             ! los que cumplen, en un arreglo nuevo -- FILTRAR
count(v(1:n) == v(i))      ! frecuencia de un valor
```

`v == 3` sobre un arreglo produce **un arreglo de logicals**, y `count`, `any`, `all` y `pack`
trabajan sobre él. Es programación vectorial aplicada a predicados, y es la misma idea que las
máscaras booleanas de NumPy — que vinieron de aquí.

Con eso, contar valores distintos se puede escribir sin bucle interior:

```fortran
cuenta = count([(count(v(1:i-1) == v(i)) == 0, i = 1, n)])
```

Compacto, y sigue siendo O(n²). Para volúmenes reales, el idioma en Fortran es **ordenar y contar
cambios**, que es O(n log n), y la ordenación viene de una biblioteca — el estándar no trae `sort`.

El ecosistema moderno lo cubre: **`stdlib`**, la biblioteca estándar comunitaria iniciada en 2019,
trae `stdlib_sorting` con `sort` y `sort_index`, tablas *hash* en `stdlib_hashmaps` y conjuntos de
bits en `stdlib_bitsets`.

Que un lenguaje de 1957 obtuviera su primera biblioteca estándar de estructuras de datos en 2020 —y
que lo hiciera la comunidad, no el comité— es una de las señales más claras de que sigue vivo.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Containers.Ordered_Sets;

procedure Unicos is
   package Conjuntos is new Ada.Containers.Ordered_Sets (Element_Type => Integer);
   use Conjuntos;

   S      : Set;
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
      S.Include (Valor);            --  Include: si ya está, no hace nada
      Pos := Fin + 1;
   end loop;

   Put ("unicos=");
   Put (Integer (S.Length), Width => 1);
   New_Line;
end Unicos;
""", """
**Lo que esta clase enseña en Ada.** Ada tiene **dos** conjuntos en `Ada.Containers`, y la elección
entre ellos es explícita:

```ada
package P is new Ada.Containers.Ordered_Sets (Integer);   --  árbol: ORDENADO, O(log n)
package Q is new Ada.Containers.Hashed_Sets (...);         --  tabla hash: O(1), sin orden
```

`Hashed_Sets` exige además dar la función *hash* y la de igualdad al instanciar. Ada no elige por ti,
y ese es el patrón del lenguaje entero.

Y hay una distinción de nombres que conviene copiar a cualquier lenguaje:

```ada
S.Insert (X);       --  lanza Constraint_Error si YA ESTÁ
S.Include (X);      --  si ya está, no hace nada
```

Dos operaciones con nombres distintos para dos intenciones distintas. En la mayoría de las
bibliotecas, `add` hace lo segundo y no hay forma de expresar la primera sin comprobar antes — con lo
que se pierde la posibilidad de detectar un duplicado inesperado.

Ada tiene además **el otro conjunto**, el que hereda de Pascal y que sigue siendo el idiomático para
universos pequeños:

```ada
type Dia is (Lun, Mar, Mie, Jue, Vie, Sab, Dom);
type Conjunto_Dias is array (Dia) of Boolean;
pragma Pack (Conjunto_Dias);          --  un BIT por día

Laborables : constant Conjunto_Dias := (Lun .. Vie => True, others => False);

if Laborables (Hoy) then ...
Union := A or B;                       --  los operadores lógicos funcionan
Interseccion := A and B;
```

Un arreglo de booleanos indexado por una enumeración, con `pragma Pack`, **es** el `set of` de Pascal:
ocupa un bit por elemento y los operadores `and`, `or`, `xor` y `not` funcionan sobre él como
operaciones de conjuntos.

Es más verboso que `set of Dia` y consigue lo mismo con piezas generales del lenguaje en lugar de una
construcción dedicada. Es, en miniatura, la diferencia de filosofía entre Ada y Pascal.
"""),
        "pascal": ("""
program Unicos;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  V: array of Integer;
  Linea, Tok: string;
  I, J, Cuenta: Integer;
  C: Char;
  Repetido: Boolean;

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
        SetLength(V, Length(V) + 1);
        V[High(V)] := StrToInt(Tok);
        Tok := '';
      end;
    end
    else
      Tok := Tok + C;
  end;

  Cuenta := 0;
  for I := 0 to High(V) do
  begin
    Repetido := False;
    for J := 0 to I - 1 do
      if V[J] = V[I] then Repetido := True;
    if not Repetido then Inc(Cuenta);
  end;

  WriteLn('unicos=', IntToStr(Cuenta));
end.
""", """
**Lo que esta clase enseña en Pascal.** **Pascal fue el primer lenguaje mayoritario con un tipo
conjunto integrado**, en 1970, y es una de las ideas por las que se le recuerda.

```pascal
type
  TDia = (Lun, Mar, Mie, Jue, Vie, Sab, Dom);
  TDias = set of TDia;

var
  Laborables, Finde, Todos: TDias;

begin
  Laborables := [Lun, Mar, Mie, Jue, Vie];
  Finde      := [Sab, Dom];
  Todos      := Laborables + Finde;        { UNIÓN }
  if Hoy in Laborables then ...             { PERTENENCIA }
  Comunes := A * B;                          { INTERSECCIÓN }
  Solo_A  := A - B;                          { DIFERENCIA }
end;
```

`+`, `*`, `-` e `in` como operadores de conjuntos, con notación matemática. Es elegante, se lee solo, y
la implementación explica su límite: **un `set` de Pascal es una máscara de bits**, un bit por posible
elemento.

De ahí la restricción que este programa no puede sortear: **el tipo base no puede tener más de 256
valores**. `set of Byte` y `set of Char` funcionan; `set of Integer` **no compila**. Por eso el
programa usa una búsqueda lineal sobre un arreglo: los enteros de la entrada no caben en un universo
acotado.

La contrapartida es la velocidad: unión, intersección y pertenencia son **una o dos instrucciones de
máquina**, sin bucles ni tablas *hash*. Para banderas y opciones no hay nada mejor, y por eso el tipo
sigue usándose masivamente en Delphi:

```pascal
Formulario.BorderIcons := [biSystemMenu, biMaximize];
```

Ese idioma —un conjunto de opciones como parámetro— es marca de la casa, y es más legible que el
`|` de banderas de C con la misma eficiencia.

Para conjuntos de universo abierto, Free Pascal moderno trae `Generics.Collections` con
`THashSet<T>` y `TDictionary<K,V>`, que son lo esperable hoy.
"""),
        "lisp": ("""
(let ((v '()))
  (loop for x = (read *standard-input* nil nil)
        while x
        do (push x v))
  (format t "unicos=~D~%" (length (remove-duplicates v))))
""", """
**Lo que esta clase enseña en Common Lisp.** Common Lisp **no tiene un tipo conjunto**, y tiene en
cambio **operaciones de conjunto sobre listas**, que es una decisión coherente con su origen:

```lisp
(remove-duplicates lista)
(union a b)          (intersection a b)     (set-difference a b)
(member x lista)     (subsetp a b)          (adjoin x lista)
```

Todas trabajan sobre listas normales y **todas aceptan `:test`**, lo que las hace más generales de lo
que parece:

```lisp
(remove-duplicates '("Ada" "ADA") :test #'string-equal)   ; sin distinguir mayúsculas
(union a b :key #'nombre :test #'string=)                  ; comparar por un campo
```

`:key` extrae lo que hay que comparar y `:test` dice cómo compararlo. Ese par de argumentos aparece en
docenas de funciones de la biblioteca, y es una uniformidad que muy pocos lenguajes alcanzan.

Y son **O(n·m)**, porque una lista es una lista. Para volumen, la respuesta es la tabla *hash*:

```lisp
(let ((tabla (make-hash-table :test #'eql)))
  (dolist (x lista) (setf (gethash x tabla) t))
  (hash-table-count tabla))
```

Aquí aparece uno de los rasgos más característicos —y más confusos— de Common Lisp: **hay cuatro
predicados de igualdad**, y hay que elegir el correcto (clase 101).

| Predicado | Compara |
|---|---|
| `eq` | identidad de puntero |
| `eql` | identidad, y números y caracteres por valor |
| `equal` | estructura: listas y cadenas elemento a elemento |
| `equalp` | como `equal`, ignorando mayúsculas y tipo numérico |

`make-hash-table` solo admite los cuatro predicados estándar como `:test` — no una función
arbitraria— porque necesita una función *hash* compatible. Es la restricción que en Ada se resuelve
pidiendo las dos funciones al instanciar.
"""),
        "tcl": ("""
gets stdin linea
set v [split [string trim $linea]]

puts "unicos=[llength [lsort -unique $v]]"
""", """
**Lo que esta clase enseña en Tcl.** **Tcl no tiene conjuntos**, y resuelve esta clase con una opción
de `lsort`: **`-unique`**, que ordena y elimina duplicados en una pasada.

`lsort` es un buen ejemplo de la densidad de la biblioteca de Tcl:

```tcl
lsort -integer $v                 ;# comparación NUMÉRICA, no textual
lsort -decreasing $v
lsort -unique $v
lsort -index 2 $registros         ;# ordenar por el TERCER campo de cada elemento
lsort -command miComparador $v    ;# con un comparador propio
lsort -dictionary $v              ;# orden "de diccionario": a10 después de a9
```

`-dictionary` merece mención: ordena los números dentro del texto por valor, así que `archivo10` va
después de `archivo9` en lugar de antes. Es lo que hace el explorador de ficheros de Windows y lo que
casi ningún lenguaje trae de serie.

Un detalle importante en este programa: **`lsort -unique` sin `-integer` compara como texto**, así que
`007` y `7` serían distintos. Para la entrada de esta clase da igual, y en código real es una fuente
de sorpresas.

Para conjuntos de verdad, lo idiomático es usar un **array o un `dict` con las claves**:

```tcl
foreach x $v { set visto($x) 1 }
array size visto                   ;# el número de elementos distintos
info exists visto($x)              ;# pertenencia, O(1)
array unset visto $x
```

Es el mismo idioma que en Perl y en Python: **el conjunto es un diccionario del que solo importan las
claves**. Y Tcllib incluye el paquete `struct::set`, con `union`, `intersect`, `difference` y
`subsetof` escritos sobre listas.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my @v = split ' ', $linea;

my %vistos;
@vistos{@v} = ();                   # rebanada de hash: el idioma clásico

print "unicos=", scalar(keys %vistos), "\\n";
""", """
**Lo que esta clase enseña en Perl.** La línea `@vistos{@v} = ();` es una **rebanada de hash**, y es
uno de los idiomas más citados del lenguaje. Merece desmontarse despacio:

- `@vistos{...}` es una **rebanada**: varias claves del hash `%vistos` a la vez.
- `@v` da la lista de claves.
- `= ()` asigna la lista vacía, así que **todos los valores quedan `undef`**.

El resultado es que cada elemento de `@v` **existe como clave**, sin importar cuántas veces aparezca.
Contar las claves es contar los distintos.

Perl no tiene tipo conjunto porque **el hash lo cubre**, y con él se escriben las cuatro operaciones:

```perl
my %conjunto = map { $_ => 1 } @v;              # construir
exists $conjunto{$x}                             # pertenencia -- O(1)
my @union = keys %{{ %a, %b }};                  # unión
my @inter = grep { $b{$_} } keys %a;             # intersección
my @dif   = grep { !$b{$_} } keys %a;            # diferencia
my @unicos_en_orden = grep { !$visto{$_}++ } @v; # ÚNICOS conservando el orden
```

La última línea es probablemente el idioma más famoso de Perl. `$visto{$_}++` **devuelve el valor
anterior y luego incrementa**: la primera vez devuelve `undef` —falso—, así que `!` lo hace cierto y
el elemento pasa; las siguientes devuelve un número mayor que cero y el elemento se descarta. Filtra
duplicados **conservando el orden de aparición**, en una línea y en O(n).

Es denso, es perfectamente legible una vez que se entiende el post-incremento, y es exactamente el
tipo de expresión que hace que Perl divida opiniones.

Para conjuntos con interfaz explícita, CPAN tiene `Set::Scalar` y `Set::Object`, pero el hash sigue
siendo la respuesta idiomática.
"""),
        "cpp": ("""
#include <iostream>
#include <iterator>
#include <set>

int main() {
    std::set<int> s{std::istream_iterator<int>(std::cin),
                    std::istream_iterator<int>()};

    std::cout << "unicos=" << s.size() << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** Cuatro líneas, porque `std::set` **rechaza los duplicados por
definición** y se puede construir directamente desde un par de iteradores de entrada.

C++ tiene **dos** conjuntos, y la diferencia importa:

| | `std::set` | `std::unordered_set` |
|---|---|---|
| Estructura | árbol rojo-negro | tabla *hash* |
| Complejidad | O(log n) | **O(1)** promedio |
| Orden al recorrer | **ordenado** | arbitrario |
| Requisito | `operator<` | `std::hash` + `operator==` |
| Desde | C++98 | C++11 |

`unordered_set` llegó **trece años más tarde**, y ese retraso tiene una historia: la STL original de
Stepanov se construyó sobre el orden —todo lo que necesita es `operator<`— y las tablas *hash*
quedaron fuera del estándar de 1998 por falta de tiempo del comité. Durante una década, todo el mundo
usó `hash_set` de SGI o de Boost, con nombres y comportamientos distintos según la implementación.

Y hay una recomendación práctica que va contra la intuición: **`std::set` con pocos elementos suele
perder frente a un `std::vector` ordenado**. Un árbol reserva un nodo por elemento, con dos punteros y
un color, esparcidos por el montón; recorrerlo salta por toda la memoria. Un vector ordenado con
`std::sort` + `std::unique` + `std::binary_search` es contiguo y, por debajo de unos cientos de
elementos, más rápido. Es la misma lección de caché de la clase 090.

```cpp
std::sort(v.begin(), v.end());
v.erase(std::unique(v.begin(), v.end()), v.end());   // el idioma erase-remove
```

Ese `erase(unique(...), end())` es el equivalente en C++ del `lsort -unique` de Tcl, y es otro idioma
que hay que reconocer: `std::unique` **no borra**, mueve los duplicados al final y devuelve el nuevo
final lógico; el borrado real lo hace el contenedor.

Y para universos pequeños, C++ tiene el `set of` de Pascal: **`std::bitset<N>`**, con `&`, `|`, `^`,
`test` y `count`.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi UNICOS;
  entrada char(200) const;
end-pi;

dcl-s elem  int(10) dim(100);
dcl-s n     int(10) inz(0);
dcl-s i     int(10);
dcl-s tok   varchar(20) inz('');
dcl-s c     char(1);
dcl-s valor int(10);

for i = 1 to %len(%trimr(entrada)) + 1;
  if i <= %len(%trimr(entrada));
    c = %subst(entrada : i : 1);
  else;
    c = ' ';
  endif;
  if c = ' ';
    if tok <> '';
      valor = %int(tok);
      // %lookup devuelve 0 si no lo encuentra
      if n = 0 or %lookup(valor : elem : 1 : n) = 0;
        n += 1;
        elem(n) = valor;
      endif;
      tok = '';
    endif;
  else;
    tok += c;
  endif;
endfor;

dsply ('unicos=' + %char(n));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG **no tiene conjuntos**, y aporta en cambio **`%lookup`**, una
búsqueda en tabla integrada en el lenguaje que evita escribir el bucle:

```rpgle
%lookup(valor : tabla)                    // búsqueda desde el principio
%lookup(valor : tabla : inicio : nelem)   // en un tramo
%lookupgt(valor : tabla)                  // el primero MAYOR
%lookuple(valor : tabla)                  // el mayor MENOR O IGUAL
%lookupge  %lookuplt
```

Las variantes con comparación —`gt`, `ge`, `lt`, `le`— **requieren que la tabla esté ordenada** y son
binarias; la exacta es lineal salvo que la tabla se declare con `ascend` o `descend`. Es el mismo
diseño que el `SEARCH ALL` de COBOL, con más variantes.

Y `sorta` ordena una tabla en el sitio, así que el idioma "ordenar y contar cambios" se escribe sin
biblioteca:

```rpgle
sorta %subarr(elem : 1 : n);
```

Donde RPG resuelve de verdad esta clase, como COBOL, es **fuera del lenguaje**: con SQL incrustado,
que es lo idiomático en IBM i desde hace veinte años.

```rpgle
exec sql select count(distinct codigo) into :cuenta from movimientos;
```

Esa línea hace en una sentencia lo que el programa de arriba hace en cuarenta, y la ejecuta el motor
de la base de datos integrado en el sistema operativo. La plataforma IBM i **lleva Db2 dentro del
sistema**, no como producto aparte, y por eso la frontera entre "programa" y "consulta" es mucho más
difusa que en otros entornos.

Es el mismo argumento del final de la página de COBOL: **la estructura de datos correcta a veces está
en la plataforma, no en el lenguaje**.
"""),
        "pli": ("""
 unicos: procedure options(main);

    declare linea char(200) varying;
    declare v(100) fixed binary(31);
    declare (n, i, j) fixed binary(31);
    declare nuevo bit(1);
    declare tok char(20) varying initial('');
    declare c char(1);

    get edit (linea) (a(200));
    n = 0;

    do i = 1 to length(linea) + 1;
       if i <= length(linea) then c = substr(linea, i, 1); else c = ' ';
       if c = ' ' then do;
          if tok ^= '' then do;
             nuevo = '1'b;
             do j = 1 to n;
                if v(j) = tok then nuevo = '0'b;
             end;
             if nuevo then do;
                n = n + 1;
                v(n) = tok;
             end;
             tok = '';
          end;
       end;
       else tok = tok || c;
    end;

    put skip list ('unicos=' || trim(char(n)));

 end unicos;
""", """
**Lo que esta clase enseña en PL/I.** **PL/I no tiene conjuntos**, y sí tiene el tipo que hace las
veces en la práctica: **`bit(n)`**, una cadena de bits de longitud arbitraria con operaciones lógicas.

```pli
declare marcas bit(256);
declare (a, b) bit(64);

marcas = '0'b;                     /* todo a cero */
substr(marcas, 42, 1) = '1'b;      /* "añadir" el elemento 42 */
if substr(marcas, 42, 1) then ...  /* pertenencia */

union        = a | b;               /* unión */
interseccion = a & b;               /* intersección */
solo_a       = a & ^b;              /* diferencia */
```

Eso es exactamente el `set of` de Pascal, construido con piezas generales en lugar de un tipo
dedicado, y **con la longitud que se quiera** —`bit(1000)` es legal— en lugar del límite de 256.

Es un caso curioso: PL/I, de 1964, **no tiene el tipo conjunto pero sí tiene el mecanismo que lo
implementa, y sin la limitación de Pascal**.

Y `bit` es un tipo de primera clase en PL/I: se puede declarar, pasar, guardar en una estructura y
escribir en un fichero. Los booleanos del lenguaje **son** `bit(1)` —de ahí el `'1'b` y el `'0'b` que
aparecen en todos los programas de esta serie— así que la lógica booleana y la de conjuntos son la
misma cosa.

Para volumen, un programa PL/I hace lo que hace un programa COBOL: **delega en DB2 o en la utilidad
SORT**, con un `SELECT DISTINCT` incrustado.

```pli
 exec sql select count(distinct codigo) into :cuenta from movimientos;
```

Otra vez la misma conclusión, y en un lenguaje distinto: en el mainframe, **la estructura de datos
vive en la plataforma**.
"""),
        "mumps": ("""
UNICOS ; Conjuntos y unicidad -- clase 094
 read linea
 kill visto
 set n = $length(linea, " ")
 for i=1:1:n set visto($piece(linea, " ", i)) = ""
 set cuenta = 0, k = ""
 for  set k = $order(visto(k))  quit:k=""  set cuenta = cuenta + 1
 write "unicos=", cuenta, !
 quit
""", """
**Lo que esta clase enseña en M.** M **no tiene un tipo conjunto**, y **tiene la estructura que hace
de conjunto mejor que ninguna otra de esta página**: el array disperso indexado por el propio valor.

```mumps
 set visto(x) = ""        ; "añadir" -- si ya está, no pasa nada
 if $data(visto(x)) ...    ; pertenencia
 kill visto(x)             ; quitar
```

`set visto(x) = ""` **es idempotente**: repetirlo no cambia nada. Y como los subíndices de un array de
M se mantienen **ordenados automáticamente**, el conjunto no solo elimina duplicados: **queda
ordenado gratis**.

Eso significa que un array de M es a la vez lo que en otros lenguajes son cuatro estructuras
distintas: **conjunto, diccionario, lista ordenada y árbol**. No hay que elegir, porque solo hay una.

`$data` es la función de pertenencia, y devuelve más información de la que parece:

```mumps
 $data(v(x))    ; 0 = no existe
                ; 1 = tiene valor, sin hijos
                ; 10 = NO tiene valor, pero SÍ tiene hijos
                ; 11 = tiene valor Y tiene hijos
```

Un nodo puede existir **solo como rama**, sin valor propio. Esa distinción no la tiene ningún
diccionario de los lenguajes del núcleo, y es lo que permite que la misma estructura sea un árbol.

Y la propiedad que lo hace único sigue siendo la de la clase 089: **poner `^` delante lo convierte en
un conjunto persistente**.

```mumps
 set ^INDICE("apellido", "GARCIA", id) = ""
```

Eso es un índice secundario de base de datos, escrito con la sintaxis de un conjunto, transaccional y
compartido entre procesos. Recorrerlo con `$order` da los pacientes apellidados García en orden
alfabético. **Es un índice B-árbol expresado como estructura de datos del lenguaje**, y es la razón de
que M compita en rendimiento con motores relacionales mucho más modernos.
"""),
        "smalltalk": ("""
| v |

v := stdin nextLine substrings collect: [ :cada | cada asNumber ].

Transcript show: 'unicos=', v asSet size printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** `asSet` y ya está: **la conversión entre colecciones es un
mensaje** (clase 090), y `Set` elimina duplicados por definición.

`Set` es una `HashedCollection`, con pertenencia en O(1), y viene con tres parientes que conviene
distinguir porque cubren casos distintos:

```smalltalk
Set new              "sin repetición, sin orden -- compara con ="
IdentitySet new      "compara con == : IDENTIDAD, no igualdad (clase 101)"
Bag new              "permite repetición y CUENTA cuántas veces (clase 095)"
Dictionary new       "claves y valores"
```

`Bag` es la que menos gente conoce y la que más se echa de menos en otros lenguajes: **un conjunto que
cuenta**. `unaBag occurrencesOf: x` da la frecuencia, y `asBag` sobre una colección es un contador de
frecuencias en una palabra — lo que en Python es `collections.Counter`, aquí desde 1980.

Y aquí aparece la decisión de diseño que hay que entender: **para que un `Set` funcione, la clase de
sus elementos tiene que implementar `=` y `hash` de forma coherente**.

```smalltalk
Punto >> = otro
    ^(otro isKindOf: Punto) and: [ x = otro x and: [ y = otro y ] ]

Punto >> hash
    ^x hash bitXor: y hash        "OBLIGATORIO si se redefine ="
```

La regla —**si dos objetos son iguales, sus `hash` deben ser iguales**— es la misma que en Java con
`equals`/`hashCode` y en C++ con `operator==`/`std::hash`, y viene de aquí. Olvidar `hash` al
redefinir `=` produce el mismo error en los tres lenguajes: el objeto se "pierde" dentro del conjunto,
y se encuentra a veces sí y a veces no.

Es uno de los pocos contratos del diseño de bibliotecas que ha sobrevivido intacto cuarenta y seis
años.
"""),
    },
)
