# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 067

> [⬅️ Volver a la clase 067](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Quedarse con los pares de una lista. Una **comprensión** dice *qué* quieres —"los elementos que
cumplen esto"— en lugar de *cómo* recorrerlos. Y la pregunta de esta página es cuántos de estos
lenguajes pueden expresarlo así, sin escribir el bucle. La respuesta sorprende: **Fortran sí, y desde
1990**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **describir una colección derivada en lugar de construirla paso a paso**, y estos
> lenguajes lo enseñan por dos motivos opuestos. El primero: **Fortran tiene `pack`**, una intrínseca
> que filtra un array con una máscara lógica, y constructores con bucle implícito `[(expr, i = 1, n)]`
> que son literalmente comprensiones. No fue un préstamo de los funcionales: llegó por la necesidad de
> vectorizar.
>
> El segundo: **COBOL, RPG y PL/I no tienen nada de esto**, y ver el bucle escrito a mano al lado de la
> versión de una línea es la mejor demostración de qué aporta la abstracción. Y Smalltalk enseña que
> `select:` no es sintaxis: es un método de `Collection` que cualquiera puede leer.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con enteros separados por espacio (al menos un par) → stdout: `pares=<los pares unidos por -, en orden>`
- **Regla:** `pares = [x ∈ lista : x par]`

| stdin | esperado |
|---|---|
| `1 2 3 4` | `pares=2-4` |
| `10 15 20` | `pares=10-20` |
| `6 7 8` | `pares=6-8` |

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
PROGRAM-ID. PARES.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  I       PIC 9(4)  COMP-3.
01  LARGO   PIC 9(4)  COMP-3.
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(4)  COMP-3.
01  C       PIC X.
01  V       PIC S9(9) COMP-3.
01  ED-V    PIC -(9)9.
01  TROZO   PIC X(20).
01  TROZO-L PIC 9(4)  COMP-3.
01  SEC     PIC X(400).
01  PTR     PIC 9(4)  COMP-3.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE SPACES TO SEC
    MOVE 1 TO PTR
    MOVE SPACES TO TOKEN
    MOVE 0 TO TLEN
    COMPUTE LARGO = FUNCTION LENGTH(FUNCTION TRIM(LINEA)) + 1

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > LARGO
        MOVE LINEA(I:1) TO C
        IF C = SPACE
            IF TLEN > 0
                MOVE FUNCTION NUMVAL(TOKEN(1:TLEN)) TO V
                IF FUNCTION MOD(V, 2) = 0
                    MOVE V TO ED-V
                    MOVE FUNCTION TRIM(ED-V) TO TROZO
                    COMPUTE TROZO-L = FUNCTION LENGTH(FUNCTION TRIM(TROZO))
                    IF PTR > 1
                        MOVE "-" TO SEC(PTR:1)
                        ADD 1 TO PTR
                    END-IF
                    MOVE TROZO(1:TROZO-L) TO SEC(PTR:TROZO-L)
                    ADD TROZO-L TO PTR
                END-IF
                MOVE SPACES TO TOKEN
                MOVE 0 TO TLEN
            END-IF
        ELSE
            ADD 1 TO TLEN
            MOVE C TO TOKEN(TLEN:1)
        END-IF
    END-PERFORM

    DISPLAY "pares=" FUNCTION TRIM(SEC)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** Treinta líneas para lo que en Perl es `grep { !($_ % 2) }`.
Y no es un defecto de COBOL: es **exactamente la medida de lo que aporta una comprensión**. Todo lo
que se ve aquí —el tokenizador, el índice del acumulador, el separador condicional— es *cómo*, y la
única línea que dice *qué* es la del `MOD`.

COBOL no tiene comprensiones, ni funciones de orden superior, ni colecciones de tamaño variable. Lo
más cerca que llega es **`SEARCH`** sobre una tabla, que expresa "encuentra el que cumpla" sin
escribir el bucle:

```cobol
SEARCH ELEMENTO VARYING I
    AT END      DISPLAY "ninguno"
    WHEN FUNCTION MOD(ELEMENTO(I), 2) = 0 DISPLAY "el primero par es " ELEMENTO(I)
END-SEARCH
```

Es un `find_if`, no un `filter`: devuelve el primero, no todos.

Y donde el COBOL de producción **sí** hace comprensiones es delegando en otro lenguaje:

```cobol
EXEC SQL
    SELECT IMPORTE INTO :WS-TABLA
      FROM MOVIMIENTOS
     WHERE MOD(IMPORTE, 2) = 0
END-EXEC
```

Ahí está el reparto real de trabajo en un sistema mainframe: **COBOL lleva la lógica de negocio y SQL
lleva las operaciones sobre conjuntos**. Es la misma división que en IBM i entre RPG y Db2, y explica
por qué a estos lenguajes nunca les hizo falta un `filter`.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program pares
   implicit none
   character(len=1000) :: linea
   integer :: v(200), n, i, ios
   integer, allocatable :: filtrados(:)
   character(len=:), allocatable :: sec
   character(len=16) :: buf

   read(*, '(A)') linea

   n = 0
   do i = 1, 200
      read(linea, *, iostat=ios) v(1:i)
      if (ios /= 0) exit
      n = i
   end do

   !  pack: se queda con los elementos donde la MÁSCARA es cierta.
   filtrados = pack(v(1:n), mod(v(1:n), 2) == 0)

   sec = ''
   do i = 1, size(filtrados)
      write(buf, '(I0)') filtrados(i)
      if (i > 1) sec = sec // '-'
      sec = sec // trim(buf)
   end do

   write(*, '(A,A)') 'pares=', sec
end program pares
```

**Lo que esta clase enseña en Fortran.** **`pack(v, mascara)` es un `filter`, y está en el lenguaje
desde Fortran 90.** `mod(v, 2) == 0` sobre un array no devuelve un booleano: devuelve **un array de
lógicos**, la máscara, y `pack` se queda con los elementos donde es cierta.

Y no llegó por influencia de los lenguajes funcionales, sino por la necesidad de **vectorizar**: una
operación sobre el array completo se compila a instrucciones SIMD, y un bucle con `if` dentro no.

La familia es amplia y merece conocerse aunque no se programe en Fortran:

```fortran
pack(v, v > 0)                  ! filter
unpack(comprimido, mascara, 0)  ! la operación inversa
merge(a, b, mascara)            ! elegir elemento a elemento
count(v > 0)                    ! cuántos cumplen
sum(v, mask = v > 0)            ! ¡sumar SOLO los que cumplen!
maxval(v, mask = v < 100)
```

Ese `mask =` opcional en `sum`, `product`, `maxval`, `minval` y `count` es la comprensión completa
—filtrar y agregar— en una sola llamada.

Y el constructor con bucle implícito es la otra mitad, el `map`:

```fortran
cuadrados = [(i * i, i = 1, 10)]
pares = [(2 * i, i = 1, n)]
filtrado = [(v(i), i = 1, n, 1)]     ! y con una condición, vía pack
```

`[(expresión, variable = inicio, fin)]` es sintácticamente **una comprensión de listas**, con la
sintaxis de 1990 y sin haber tomado nada prestado de Haskell ni de Python.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;           use Ada.Text_IO;
with Ada.Integer_Text_IO;   use Ada.Integer_Text_IO;
with Ada.Strings;           use Ada.Strings;
with Ada.Strings.Fixed;
with Ada.Strings.Unbounded; use Ada.Strings.Unbounded;

procedure Pares is
   Linea  : String (1 .. 500);
   Ultimo : Natural;
   Pos    : Positive := 1;
   Fin    : Positive;
   Valor  : Integer;
   Sec    : Unbounded_String := Null_Unbounded_String;
begin
   Get_Line (Linea, Ultimo);

   while Pos <= Ultimo loop
      Get (Linea (Pos .. Ultimo), Valor, Fin);
      if Valor mod 2 = 0 then
         if Length (Sec) > 0 then
            Append (Sec, "-");
         end if;
         Append (Sec, Ada.Strings.Fixed.Trim (Integer'Image (Valor), Both));
      end if;
      Pos := Fin + 1;
   end loop;

   Put_Line ("pares=" & To_String (Sec));
end Pares;
```

**Lo que esta clase enseña en Ada.** Ada 83, 95, 2005 y 2012 **no tienen comprensiones**: el bucle se
escribe. Pero **Ada 2022 sí las añadió**, y su forma es notablemente limpia:

```ada
--  Comprensión con filtro (Ada 2022)
Pares : constant Vector := [for E of Datos when E mod 2 = 0 => E];

--  Con transformación
Cuadrados : constant Vector := [for I in 1 .. 10 => I * I];

--  Y sobre un mapa
Nombres : constant Map := [for C of Clientes => C.Id => C.Nombre];
```

`[for ... when ... => ...]` es exactamente la comprensión de Python con otra puntuación, y llegó a un
lenguaje de 1983 **en 2022**.

Fíjate en el `constant`: eso es lo que hace valiosa la comprensión en Ada, y es el mismo argumento de
la clase 060. Con un bucle, la colección se declara vacía y se rellena, así que **no puede ser
constante**. Con la comprensión, se construye completa en la declaración y queda sellada. La
expresividad no es el objetivo principal — lo es poder declarar más cosas inmutables.

Mientras tanto, la biblioteca estándar ofrece los contenedores genéricos —`Ada.Containers.Vectors`,
`Doubly_Linked_Lists`, `Hashed_Maps`, `Ordered_Sets`— con operaciones como `Iterate` y `Query_Element`
que cubren el recorrido, y con `Ada.Containers.Generic_Array_Sort` para ordenar.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Pares;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, Token, Sec: string;
  I, V: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea) + ' ';

  Sec := '';
  Token := '';
  for I := 1 to Length(Linea) do
  begin
    if Linea[I] = ' ' then
    begin
      if Token <> '' then
      begin
        V := StrToInt(Token);
        if (V mod 2) = 0 then
        begin
          if Sec <> '' then Sec := Sec + '-';
          Sec := Sec + IntToStr(V);
        end;
        Token := '';
      end;
    end
    else
      Token := Token + Linea[I];
  end;

  WriteLn('pares=', Sec);
end.
```

**Lo que esta clase enseña en Pascal.** Pascal **no tiene comprensiones ni funciones de orden
superior** en su forma clásica, y este bucle es el resultado. Es el mismo trabajo manual que en
COBOL, con menos ceremonia.

Lo que sí tiene, y lleva desde 1970, son los **conjuntos** de la clase 062:

```pascal
if C in ['a'..'z', 'A'..'Z'] then ...
```

Un conjunto es la mitad de una comprensión: expresa **la pertenencia** sin bucle, aunque no permite
derivar una colección de otra. Y está limitado a tipos ordinales pequeños, porque se implementa como
máscara de bits.

Delphi y Free Pascal modernos añadieron genéricos y métodos anónimos, y con ellos aparecieron
bibliotecas que sí traen el vocabulario funcional:

```pascal
uses Spring.Collections;      { biblioteca de la comunidad }

Pares := Datos.Where(function(const X: Integer): Boolean
                     begin Result := X mod 2 = 0; end);
```

La verbosidad de esa lambda —`function(const X: Integer): Boolean begin ... end`— explica por qué el
estilo funcional nunca arraigó en el mundo Pascal: **sin sintaxis ligera para las funciones anónimas,
el bucle explícito sale más corto**. Es la misma razón por la que Java tardó hasta la versión 8 en
adoptarlo y C++ hasta C++11: la comprensión necesita que pasar código sea barato de escribir.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((lista (loop for v = (read *standard-input* nil :fin)
                   until (eq v :fin)
                   collect v)))
  (format t "pares=~{~D~^-~}~%" (remove-if-not #'evenp lista)))
```

**Lo que esta clase enseña en Common Lisp.** Lisp tiene **dos formas** de expresar esta clase, y las
dos son de biblioteca, no de sintaxis.

La primera son las **funciones de secuencia**, que funcionan sobre listas, vectores y cadenas por
igual:

```lisp
(remove-if-not #'evenp lista)      ; los que cumplen
(remove-if #'evenp lista)          ; los que NO
(mapcar #'1+ lista)                ; map
(count-if #'plusp lista)
(find-if #'zerop lista)
(sort (copy-seq lista) #'<)
```

La convención `-if` / `-if-not` recorre toda la biblioteca y es muy uniforme: `remove-if`,
`delete-if`, `count-if`, `find-if`, `position-if`, `substitute-if`.

La segunda es **`loop` con `collect` y `when`**, que es literalmente una comprensión:

```lisp
(loop for x in lista when (evenp x) collect x)
(loop for x in lista collect (* x x))
(loop for x in lista for y in otra collect (+ x y))    ; dos listas a la vez
(loop for x in lista when (plusp x) sum x)             ; filtrar Y agregar
```

`for ... when ... collect` es exactamente `[x for x in lista if x % 2 == 0]` de Python, con otra
puntuación y quince años antes.

Y —esto es lo importante— **`loop` es una macro**. Alguien implementó un lenguaje de comprensión
entero como biblioteca, sin tocar el compilador. Es la respuesta de Lisp a por qué nunca necesitó que
el comité añadiera comprensiones: **cuando aparecen, se escriben**.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea

set pares {}
foreach v [split [string trim $linea]] {
    if {$v % 2 == 0} {
        lappend pares $v
    }
}

puts "pares=[join $pares -]"
```

**Lo que esta clase enseña en Tcl.** Tcl 8.6 añadió **`lmap`**, que es el `map` con sintaxis de
bucle, y con él la comprensión se escribe en una línea:

```tcl
set pares [lmap v [split [string trim $linea]] {
    expr {$v % 2 == 0 ? $v : [continue]}
}]
```

Ese `[continue]` dentro de `lmap` es el truco idiomático para **filtrar**: `continue` salta la
iteración y **no añade nada al resultado**. Es feo y es la única forma, porque `lmap` es un `map` y
Tcl no tiene `lfilter`.

Para filtrar de verdad, la biblioteca **Tcllib** trae `struct::list`:

```tcl
package require struct::list
set pares [struct::list filter $lista {apply {{v} {expr {$v % 2 == 0}}}}]
set dobles [struct::list map $lista {apply {{v} {expr {$v * 2}}}}]
set total [struct::list fold $lista 0 {apply {{a b} {expr {$a + $b}}}}]
```

La verbosidad de `{apply {{v} {...}}}` es la misma barrera que en Pascal: **sin sintaxis ligera para
las funciones anónimas, el bucle explícito gana**. Por eso el `foreach` de este programa es lo que un
programador de Tcl escribiría de verdad.

Y hay una tercera vía muy propia del lenguaje, que aprovecha que las listas son cadenas: para
operaciones sobre listas grandes, `lsearch -all -inline` con `-regexp` filtra sin bucle y en C.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

my @pares = grep { $_ % 2 == 0 } split ' ', $linea;

print "pares=", join('-', @pares), "\n";
```

**Lo que esta clase enseña en Perl.** `grep { condición } lista` es el filtro, y su nombre viene
directamente de la herramienta de Unix. Junto a `map` forma el vocabulario básico, y las dos se
encadenan de derecha a izquierda como las tuberías del shell:

```perl
my @resultado = map { $_ * 2 }
                grep { $_ % 2 == 0 }
                split ' ', $linea;
```

Se lee de abajo arriba: parte, filtra, transforma. Es una comprensión sin sintaxis especial, porque
en Perl **un bloque es un argumento normal** y no hace falta escribir `sub { }`.

Dos detalles importantes de esta clase. El primero: **`$_` en `grep` y `map` es un alias, no una
copia**, igual que en el `foreach` de la clase 064. Modificarlo dentro del bloque **cambia la lista
original**:

```perl
my @x = map { $_ * 2 } @lista;      # correcto: no toca @lista
my @y = map { $_ *= 2 } @lista;     # ¡MODIFICA @lista!
```

El segundo: **`map` puede devolver cualquier número de elementos por entrada**, no solo uno. Ese es
su superpoder frente al `map` de otros lenguajes:

```perl
my @pares = map { $_ % 2 == 0 ? ($_) : () } @lista;   # map haciendo de filtro
my %h = map { $_ => 1 } @lista;                        # lista -> hash
my @dobles = map { ($_, $_) } @lista;                  # cada uno DOS veces
```

Devolver la lista vacía elimina el elemento; devolver dos lo duplica. `map` de Perl es en realidad un
`flatMap`, y por eso puede hacer de `filter` y de constructor de hash a la vez.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <iterator>
#include <sstream>
#include <string>
#include <vector>

int main() {
    std::string linea;
    if (!std::getline(std::cin, linea)) return 1;

    std::istringstream iss(linea);
    const std::vector<int> v{std::istream_iterator<int>(iss),
                             std::istream_iterator<int>()};

    std::string sec;
    for (int x : v) {
        if (x % 2 != 0) continue;
        if (!sec.empty()) sec += '-';
        sec += std::to_string(x);
    }

    std::cout << "pares=" << sec << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** Hasta C++20 no había comprensiones, y la forma de la STL era
`std::copy_if` con un iterador de inserción:

```cpp
std::vector<int> pares;
std::copy_if(v.begin(), v.end(), std::back_inserter(pares),
             [](int x) { return x % 2 == 0; });
```

Funciona y es genérico, y tiene un problema: **cada paso materializa un vector**. Encadenar filtrar,
transformar y volver a filtrar crea tres vectores intermedios.

C++20 lo resolvió con los **rangos** y su operador de tubería, que es la comprensión de C++:

```cpp
#include <ranges>
auto pares = v | std::views::filter([](int x) { return x % 2 == 0; })
               | std::views::transform([](int x) { return x * 2; });

for (int x : pares) { ... }     // NADA se ha calculado hasta aquí
```

Esas vistas son **perezosas y componibles**: no construyen ningún contenedor intermedio, y el
recorrido final aplica las dos operaciones en una sola pasada. Es la fusión de bucles de la ficha de
Fortran, obtenida en la biblioteca mediante plantillas.

Y esa es la razón de que los rangos se consideren el cambio más importante de C++20: no añaden
capacidad —`copy_if` ya filtraba— sino que **eliminan el coste de componer**, que es lo que hacía que
en la práctica la gente escribiera bucles a mano.

Compilado con `-std=c++17`, este programa usa el bucle. Es exactamente la diferencia.

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

dcl-pi PARES;
  linea varchar(200) const;
end-pi;

dcl-s trozos varchar(20) dim(50);
dcl-s i      int(10);
dcl-s v      int(10);
dcl-s sec    varchar(500) inz('');
dcl-s salida char(520);

trozos = %split(linea : ' ');

for i = 1 to %elem(trozos);
  v = %int(trozos(i));
  if %rem(v : 2) = 0;
    if sec <> '';
      sec += '-';
    endif;
    sec += %char(v);
  endif;
endfor;

salida = 'pares=' + sec;
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG no tiene comprensiones ni funciones de orden superior: no
hay forma de pasar un bloque de código como argumento. El filtro se escribe.

Y como en COBOL, **el filtrado de verdad en IBM i se delega en SQL**:

```rpgle
exec sql
  declare c1 cursor for
    select importe from movimientos
     where mod(importe, 2) = 0
     order by fecha;

exec sql open c1;
dow sqlcode = 0;
  exec sql fetch c1 into :importe;
  ...
enddo;
```

Ese reparto —RPG para la lógica, SQL para los conjuntos— es la arquitectura estándar de la plataforma
desde hace veinte años, y es el motivo de que a RPG nunca le hiciera falta un `filter`: **cuando los
datos están en una base de datos integrada en el sistema operativo, la comprensión la escribe el
motor**.

Y ahí hay una idea que va más allá de RPG: **SQL es una comprensión de listas**. `SELECT x FROM t
WHERE p` es exactamente `[x for x in t if p]`, y la cláusula `SELECT` es el `map`. La diferencia es
que el optimizador puede elegir la estrategia —índice, recorrido, orden de los filtros—, que es justo
el argumento de esta clase sobre separar el qué del cómo.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 pares: procedure options(main);

    declare linea character(200) varying;
    declare trozo character(20)  varying;
    declare sec   character(500) varying initial('');
    declare (i, p, v) fixed binary(31);

    get edit (linea) (a(200));
    linea = trim(linea) || ' ';

    p = 1;
    do i = 1 to length(linea);
       if substr(linea, i, 1) = ' ' then do;
          if i > p then do;
             trozo = substr(linea, p, i - p);
             v = trozo;
             if mod(v, 2) = 0 then do;
                if sec ^= '' then sec = sec || '-';
                sec = sec || trim(char(v));
             end;
          end;
          p = i + 1;
       end;
    end;

    put skip list ('pares=' || sec);

 end pares;
```

**Lo que esta clase enseña en PL/I.** PL/I no tiene comprensiones, pero **sí tiene operaciones sobre
arrays completos**, heredadas de FORTRAN, y con ellas se puede expresar buena parte de esta clase sin
bucle:

```pli
declare v(100) fixed binary(31);
declare mascara(100) bit(1);

v = v * 2;                    /* map sobre todo el array */
mascara = (mod(v, 2) = 0);    /* la máscara, elemento a elemento */
total = sum(v);
if any(mascara) then ...
cuantos = sum(binary(mascara));   /* contar los ciertos */
```

Lo que falta es **`pack`**: PL/I puede calcular la máscara pero no comprimir el array quedándose solo
con los seleccionados. Esa intrínseca es específica de Fortran 90, y es justo la pieza que convierte
las operaciones de array en un `filter` de verdad.

PL/I tiene además una construcción para arrays que casi nadie recuerda y que viene al caso:

```pli
declare v(10) fixed binary(31) initial((10) 0);      /* factor de repetición */
declare w(5)  fixed binary(31) initial(1, 2, 3, 4, 5);
```

`(10) 0` significa "diez ceros". Es un constructor de array con repetición, la mitad de un
constructor por comprensión.

Y sobre `v = trozo` en el programa: es otra vez la conversión implícita de texto a número de la clase
050, funcionando en silencio hasta que el texto no es numérico.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
PARES ; Comprension -- clase 067
 read linea
 set sec = ""
 for i = 1:1:$length(linea, " ") do
 . set v = $piece(linea, " ", i)
 . quit:v#2'=0
 . set:sec'="" sec = sec _ "-"
 . set sec = sec _ v
 write "pares=", sec, !
 quit
```

**Lo que esta clase enseña en M.** Fíjate en **`quit:v#2'=0`** dentro del bloque `do`: ese `quit`
**no sale de la rutina, sale de la iteración actual**. Es el `continue` de M, escrito como un
postcondicional.

Esa es la forma idiomática de filtrar en M: no hay `filter`, hay un `quit` condicional al principio
del cuerpo del bucle que descarta lo que no interesa. Se lee como una guarda —tema de la clase 058—
aplicada a cada vuelta.

M no tiene funciones de orden superior en el sentido habitual, **pero tiene indirección**, que da algo
parecido:

```mumps
 set filtro = "v#2=0"
 for i = 1:1:n do
 . set v = $piece(linea, " ", i)
 . quit:'@filtro          ; @ EVALÚA la cadena como código
 . ...
```

`@` es el operador de **indirección**: toma una cadena y la ejecuta como si fuera código. Con él se
puede pasar una condición —o un nombre de rutina— **como dato**, que es la mitad de lo que hace una
función de orden superior.

Es enormemente flexible y tiene el coste que cabe esperar: **un programa con indirección no se puede
analizar estáticamente**, porque qué se ejecuta se decide en tiempo de ejecución. Es el `eval` de
JavaScript con cincuenta años más, y con los mismos problemas de seguridad si la cadena viene de
fuera.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| pares |

pares := (stdin nextLine substrings collect: [ :cada | cada asNumber ])
    select: [ :cada | cada even ].

Transcript
    show: 'pares=', ((pares collect: [ :c | c printString ])
        inject: '' into: [ :acc :s | acc isEmpty ifTrue: [ s ] ifFalse: [ acc , '-' , s ] ]);
    cr.
```

**Lo que esta clase enseña en Smalltalk.** `select:` es el filtro y `collect:` el `map`, y los dos son
**métodos de `Collection`** que puedes abrir y leer:

```smalltalk
Collection >> select: unBloque
    | resultado |
    resultado := self species new.
    self do: [ :cada | (unBloque value: cada) ifTrue: [ resultado add: cada ] ].
    ^ resultado
```

Ocho líneas. **No hay sintaxis de comprensión porque no hace falta**: con bloques baratos de escribir
y `do:` implementado, todo el vocabulario funcional es biblioteca.

El protocolo completo es amplio y muy uniforme:

```smalltalk
coleccion select: [ :x | ... ]           "filter"
coleccion reject: [ :x | ... ]           "filter negado"
coleccion collect: [ :x | ... ]          "map"
coleccion detect: [ :x | ... ] ifNone: [ ... ]
coleccion inject: 0 into: [ :a :b | ... ]  "reduce"
coleccion count: [ :x | ... ]
coleccion anySatisfy: [ :x | ... ]
coleccion groupedBy: [ :x | ... ]        "agrupar en un diccionario"
coleccion sorted: [ :a :b | a < b ]
```

Y `self species new` en la implementación es un detalle elegante: **el resultado es del mismo tipo que
el receptor**. `select:` sobre un `Set` devuelve un `Set`, sobre una `OrderedCollection` devuelve una
`OrderedCollection`, y sobre un `String` devuelve un `String`. Es lo que en C++ se consigue con
plantillas y en Java no se consigue del todo.

---

## Y de vuelta a la clase

Lo transferible: **una comprensión separa el qué del cómo, y eso permite que el "cómo" cambie sin
tocar tu código**. `pack` de Fortran puede vectorizarse, `select:` de Smalltalk puede estar
implementado con un índice, y un `filter` perezoso puede no materializar nada. Cuando escribes el
bucle a mano, congelas la estrategia. Es la misma razón por la que se prefiere SQL a recorrer una
tabla: **declarar deja margen a quien ejecuta**.

⏮️ [Volver a la clase 067](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
