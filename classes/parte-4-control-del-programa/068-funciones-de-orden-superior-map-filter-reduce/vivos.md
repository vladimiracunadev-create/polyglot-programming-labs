# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 068

> [⬅️ Volver a la clase 068](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Doblar cada elemento y sumar los resultados. Un `map` seguido de un `reduce`, la pareja que sostiene
media programación moderna. Y la pregunta que reparte a estos lenguajes es más profunda de lo que
parece: **¿se puede pasar una función como argumento?** Porque si no se puede, `map` y `reduce`
sencillamente no existen.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto son las **funciones de orden superior**, y estos lenguajes lo enseñan porque cubren
> las tres épocas. **Lisp las tiene desde 1958** —`mapcar` y `reduce` son la definición del
> paradigma— y **Smalltalk desde los 70** con los bloques. En el otro extremo, **COBOL y RPG no pueden
> pasar código como dato**, y por eso el bucle se escribe siempre.
>
> Y en medio están los que las obtuvieron después: **Fortran 2003 con procedimientos como argumento**,
> **Ada con genéricos y punteros a subprograma**, y **C++ con plantillas y lambdas** — tres formas
> distintas de resolver el mismo problema, con y sin coste en ejecución.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con enteros separados por espacio → stdout: `doblados=<cada x·2 unidos por -> total=<suma de los doblados>`
- **Regla:** `doblados = map(x→2x) ; total = reduce(+, doblados)`

| stdin | esperado |
|---|---|
| `1 2 3` | `doblados=2-4-6 total=12` |
| `5` | `doblados=10 total=10` |
| `2 4` | `doblados=4-8 total=12` |

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
PROGRAM-ID. MAPRED.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  I       PIC 9(4)  COMP-3.
01  LARGO   PIC 9(4)  COMP-3.
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(4)  COMP-3.
01  C       PIC X.
01  V       PIC S9(9)  COMP-3.
01  D       PIC S9(9)  COMP-3.
01  ED-D    PIC -(9)9.
01  TROZO   PIC X(20).
01  TROZO-L PIC 9(4)  COMP-3.
01  SEC     PIC X(400).
01  PTR     PIC 9(4)  COMP-3.
01  TOTAL   PIC S9(18) COMP-3.
01  ED-T    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE SPACES TO SEC
    MOVE 1 TO PTR
    MOVE 0 TO TOTAL
    MOVE SPACES TO TOKEN
    MOVE 0 TO TLEN
    COMPUTE LARGO = FUNCTION LENGTH(FUNCTION TRIM(LINEA)) + 1

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > LARGO
        MOVE LINEA(I:1) TO C
        IF C = SPACE
            IF TLEN > 0
                MOVE FUNCTION NUMVAL(TOKEN(1:TLEN)) TO V
                COMPUTE D = V * 2
                ADD D TO TOTAL
                MOVE D TO ED-D
                MOVE FUNCTION TRIM(ED-D) TO TROZO
                COMPUTE TROZO-L = FUNCTION LENGTH(FUNCTION TRIM(TROZO))
                IF PTR > 1
                    MOVE "-" TO SEC(PTR:1)
                    ADD 1 TO PTR
                END-IF
                MOVE TROZO(1:TROZO-L) TO SEC(PTR:TROZO-L)
                ADD TROZO-L TO PTR
                MOVE SPACES TO TOKEN
                MOVE 0 TO TLEN
            END-IF
        ELSE
            ADD 1 TO TLEN
            MOVE C TO TOKEN(TLEN:1)
        END-IF
    END-PERFORM

    MOVE TOTAL TO ED-T
    DISPLAY "doblados=" FUNCTION TRIM(SEC)
            " total=" FUNCTION TRIM(ED-T)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** **En COBOL no se puede pasar una función como argumento**, y
por eso `map` y `reduce` no existen ni pueden escribirse. El bucle es la única forma.

Lo más cerca que llega es la llamada dinámica por nombre, que es potente y muy distinta:

```cobol
01  NOMBRE-PROGRAMA  PIC X(8) VALUE "CALCIVA".
...
CALL NOMBRE-PROGRAMA USING IMPORTE, RESULTADO
```

`CALL` con una **variable** en lugar de un literal resuelve el programa **en tiempo de ejecución**.
Cambiando el contenido de `NOMBRE-PROGRAMA` se llama a otra cosa. Eso permite tablas de despacho como
las de la clase 061 —una tabla de nombres de programa indexada por código de operación— y es la base
de la arquitectura de muchos sistemas transaccionales.

Es *casi* una función de primer orden: puedes elegir qué código ejecutar, guardándolo como dato. Lo
que no puedes es **crear** una función nueva, ni capturar variables del entorno, que es lo que
convierte a las clausuras en lo que son.

Y COBOL 2002 añadió `FUNCTION-ID` para definir funciones de usuario con valor de retorno, con lo que
al menos se pueden componer expresiones. Pero seguir sin poder pasarlas como argumento deja fuera
todo este paradigma.

Lo que hace COBOL en la práctica es lo de la clase anterior: **delegar en SQL** las operaciones sobre
conjuntos, donde `SUM`, `AVG` y `GROUP BY` son el `reduce` que el lenguaje no tiene.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program mapred
   implicit none
   character(len=1000) :: linea
   integer :: v(200), n, i, ios, total
   integer, allocatable :: doblados(:)
   character(len=:), allocatable :: sec
   character(len=16) :: buf

   read(*, '(A)') linea

   n = 0
   do i = 1, 200
      read(linea, *, iostat=ios) v(1:i)
      if (ios /= 0) exit
      n = i
   end do

   doblados = v(1:n) * 2      ! map: sobre el array completo
   total = sum(doblados)      ! reduce: intrínseca

   sec = ''
   do i = 1, size(doblados)
      write(buf, '(I0)') doblados(i)
      if (i > 1) sec = sec // '-'
      sec = sec // trim(buf)
   end do

   write(*, '(A,A,A,I0)') 'doblados=', sec, ' total=', total
end program mapred
```

**Lo que esta clase enseña en Fortran.** `doblados = v(1:n) * 2` es el `map` y `sum(doblados)` es el
`reduce`, **sin ninguna función de orden superior**. Fortran llegó al mismo destino por otro camino:
en vez de pasar una función a un recorrido, **hace que la operación se aplique al array entero**.

La diferencia es importante y sutil. Un `map` con función es **general**: acepta cualquier
transformación. La aritmética de arrays de Fortran solo cubre las operaciones que el lenguaje conoce.
A cambio, **se vectoriza**, cosa que una llamada indirecta a una función no puede hacer.

Y Fortran **sí** tiene funciones de orden superior desde F2003, aunque casi nadie las use:

```fortran
abstract interface
   pure function transformacion(x) result(y)
      integer, intent(in) :: x
      integer :: y
   end function
end interface

subroutine aplicar(v, f)
   integer, intent(inout) :: v(:)
   procedure(transformacion) :: f      ! ¡una FUNCIÓN como argumento!
   integer :: i
   do i = 1, size(v)
      v(i) = f(v(i))
   end do
end subroutine
```

`procedure(interfaz)` declara un parámetro que es un procedimiento, con su firma comprobada. Existe,
funciona, y **no se usa en código numérico** por una razón concreta: la llamada indirecta impide
integrar el cuerpo en línea y mata la vectorización. En un bucle de mil millones de vueltas, eso es
un factor de diez.

Es un buen recordatorio de que la elegancia y el rendimiento a veces apuntan en direcciones
distintas, y de que cada lenguaje elige.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;           use Ada.Text_IO;
with Ada.Integer_Text_IO;   use Ada.Integer_Text_IO;
with Ada.Strings;           use Ada.Strings;
with Ada.Strings.Fixed;
with Ada.Strings.Unbounded; use Ada.Strings.Unbounded;

procedure Mapred is
   Linea  : String (1 .. 500);
   Ultimo : Natural;
   Pos    : Positive := 1;
   Fin    : Positive;
   Valor  : Integer;
   Doblado : Integer;
   Total  : Integer := 0;
   Sec    : Unbounded_String := Null_Unbounded_String;
begin
   Get_Line (Linea, Ultimo);

   while Pos <= Ultimo loop
      Get (Linea (Pos .. Ultimo), Valor, Fin);
      Doblado := Valor * 2;
      Total := Total + Doblado;
      if Length (Sec) > 0 then
         Append (Sec, "-");
      end if;
      Append (Sec, Ada.Strings.Fixed.Trim (Integer'Image (Doblado), Both));
      Pos := Fin + 1;
   end loop;

   Put ("doblados=" & To_String (Sec) & " total=");
   Put (Total, Width => 1);
   New_Line;
end Mapred;
```

**Lo que esta clase enseña en Ada.** Ada tiene funciones de orden superior desde el principio, pero
por una vía distinta de la habitual: **los genéricos**.

```ada
generic
   type Elemento is private;
   with function Transformar (X : Elemento) return Elemento;   --  ¡parámetro FUNCIÓN!
procedure Aplicar (V : in out Array_De (Elemento));
```

`with function` declara que el genérico recibe una función como parámetro, y la instanciación la fija
**en tiempo de compilación**:

```ada
procedure Doblar is new Aplicar (Integer, Por_Dos);   --  se resuelve al compilar
```

Es la misma técnica que las plantillas de C++, y tiene la misma propiedad: **coste cero en
ejecución**, porque no hay llamada indirecta. La función se integra en línea.

Ada 95 añadió además los **punteros a subprograma** —`access function (X : Integer) return Integer`—
que sí resuelven en ejecución, y Ada 2012 las **expresiones lambda**… bueno, casi: tiene funciones de
expresión, que son cuerpos de una sola expresión, pero **no clausuras anónimas**.

Esa ausencia es deliberada. Una clausura captura variables del entorno y las mantiene vivas más allá
del ámbito, lo que exige memoria dinámica y un tiempo de vida difícil de analizar. En un sistema que
debe certificarse, **eso es exactamente lo que no se quiere**. Ada prefiere el genérico, que se
resuelve al compilar y no reserva nada.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Mapred;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, Token, Sec: string;
  I, V, D, Total: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea) + ' ';

  Sec := '';
  Token := '';
  Total := 0;
  for I := 1 to Length(Linea) do
  begin
    if Linea[I] = ' ' then
    begin
      if Token <> '' then
      begin
        V := StrToInt(Token);
        D := V * 2;
        Total := Total + D;
        if Sec <> '' then Sec := Sec + '-';
        Sec := Sec + IntToStr(D);
        Token := '';
      end;
    end
    else
      Token := Token + Linea[I];
  end;

  WriteLn('doblados=', Sec, ' total=', IntToStr(Total));
end.
```

**Lo que esta clase enseña en Pascal.** El Pascal ISO **sí permite pasar procedimientos y funciones
como parámetros** —fue de los primeros lenguajes imperativos en hacerlo— con una sintaxis que declara
la firma completa:

```pascal
function Aplicar(F: TTransformacion; X: Integer): Integer;

type
  TTransformacion = function(X: Integer): Integer;
```

Lo que **no** tiene el Pascal clásico son **funciones anónimas ni clausuras**: hay que declarar la
función con nombre en otro sitio y pasar su dirección. Y esa es precisamente la barrera que impide el
estilo funcional, como se vio en la clase 067: si escribir la función cuesta cinco líneas y un
nombre, el bucle sale más corto.

Delphi 2009 añadió los **métodos anónimos**, que sí son clausuras de verdad:

```pascal
type
  TFunc = reference to function(X: Integer): Integer;

var
  Factor: Integer;
  Multiplicar: TFunc;
begin
  Factor := 3;
  Multiplicar := function(X: Integer): Integer
                 begin Result := X * Factor; end;   { CAPTURA Factor }
```

`reference to function` es la palabra clave que lo distingue de un puntero a función normal: implica
**conteo de referencias y captura del entorno**. Con eso, Delphi tiene clausuras completas.

Free Pascal las soporta también, con `{$modeswitch functionreferences}`. Pero llegaron cuarenta años
después que en Lisp, y el ecosistema ya estaba escrito con bucles.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((lista (loop for v = (read *standard-input* nil :fin)
                    until (eq v :fin)
                    collect v))
       (doblados (mapcar (lambda (x) (* 2 x)) lista)))
  (format t "doblados=~{~D~^-~} total=~D~%"
          doblados (reduce #'+ doblados)))
```

**Lo que esta clase enseña en Common Lisp.** **`mapcar` y `reduce` son de 1958**, y no son una
biblioteca añadida: son la definición del paradigma. Este programa es, esencialmente, cómo se
escribiría hoy en cualquier lenguaje funcional.

`(lambda (x) (* 2 x))` es una **función anónima**, y `#'+` es la función `+` **como valor** — el
`#'` es la abreviatura de `function`, que obtiene el objeto función asociado a un nombre.

Y aquí aparece una peculiaridad de Common Lisp que hay que conocer: es un **Lisp-2**, es decir, tiene
**dos espacios de nombres separados**, uno para funciones y otro para variables.

```lisp
(defun lista (x) ...)      ; una FUNCIÓN llamada lista
(let ((lista '(1 2 3)))    ; y una VARIABLE llamada lista: no chocan
  (lista lista))           ; la primera posición es función, la segunda variable
(funcall f x)              ; para llamar a una función guardada en una VARIABLE
(mapcar #'coche lista)     ; y #' para OBTENERLA de su nombre
```

Scheme es un **Lisp-1**: un solo espacio de nombres, así que no hacen falta `#'` ni `funcall`. La
discusión entre los dos diseños es una de las más antiguas de la comunidad, y el argumento a favor
del Lisp-2 es práctico: **puedes llamar a una variable `lista` sin ocultar la función `lista`**.

`reduce` acepta `:initial-value`, `:from-end` y `:key`, lo que cubre todos los pliegues. Y
`mapcar` recorre **varias listas a la vez**: `(mapcar #'+ '(1 2) '(10 20))` da `(11 22)`.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea

set doblados {}
set total 0
foreach v [split [string trim $linea]] {
    set d [expr {$v * 2}]
    lappend doblados $d
    incr total $d
}

puts "doblados=[join $doblados -] total=$total"
```

**Lo que esta clase enseña en Tcl.** En Tcl **el código es una cadena**, así que pasar una función es
pasar texto — y eso da funciones de orden superior sin necesidad de que el lenguaje las contemple:

```tcl
proc aplicar {lista cuerpo} {
    set r {}
    foreach x $lista { lappend r [eval $cuerpo] }    ;# $x visible en el cuerpo
    return $r
}
aplicar {1 2 3} {expr {$x * 2}}
```

Funciona, y es peligroso: el cuerpo se evalúa en un ámbito que el llamante no controla, y una cadena
que venga de fuera es una inyección.

La forma moderna y correcta es **`apply`**, que llegó en Tcl 8.5 y es una **lambda de verdad**:

```tcl
set doblar {{x} {expr {$x * 2}}}          ;# una lambda: argumentos y cuerpo
apply $doblar 5                            ;# -> 10

set doblados [lmap x $lista {expr {$x * 2}}]           ;# map, Tcl 8.6
set total [::tcl::mathop::+ {*}$doblados]              ;# suma con expansión
```

`{*}$lista` es el **operador de expansión**, que convierte una lista en argumentos separados — el
`*args` de Python, añadido en 8.5. Y `::tcl::mathop::+` expone los operadores aritméticos **como
comandos**, así que `+` puede pasarse como argumento igual que `#'+` en Lisp.

Que los operadores se puedan usar como comandos es coherente con todo lo demás: en Tcl no hay
operadores, así que exponerlos como comandos no es una excepción, es la regla.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;
use List::Util qw(sum0);

my $linea = <STDIN>;
chomp $linea;

my @doblados = map { $_ * 2 } split ' ', $linea;
my $total = sum0(@doblados);

print "doblados=", join('-', @doblados), " total=$total\n";
```

**Lo que esta clase enseña en Perl.** `map`, `grep` y `sort` son **operadores del lenguaje**, no
funciones de biblioteca, y por eso reciben un bloque sin necesidad de escribir `sub { }`. Esa
ligereza sintáctica es lo que hizo que el estilo funcional se adoptara en Perl mucho antes que en
Java o C++.

Y Perl tiene funciones de primera clase completas, con clausuras:

```perl
my $doblar = sub { $_[0] * 2 };           # función anónima
my @r = map { $doblar->($_) } @lista;     # -> para llamar por referencia
my $sumador = do { my $t = 0; sub { $t += shift } };   # clausura con estado
```

`reduce` no es un operador sino una función de `List::Util`, y usa una convención propia:

```perl
use List::Util qw(reduce);
my $total = reduce { $a + $b } @doblados;
```

**`$a` y `$b` no son parámetros declarados**: son las variables globales del paquete que `reduce`
—y `sort`— rellenan en cada paso. Es la misma pareja que usa `sort { $a <=> $b }`, y es la razón por
la que en toda esta sección las variables se han llamado `$x` e `$y` en lugar de `$a` y `$b`: usarlas
para otra cosa interfiere con estas funciones.

Es una decisión de diseño discutible —variables globales implícitas en lugar de parámetros— que
existe por rendimiento: evitar crear un marco de llamada por elemento. En una lista de un millón, se
nota.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <algorithm>
#include <iostream>
#include <iterator>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>

int main() {
    std::string linea;
    if (!std::getline(std::cin, linea)) return 1;

    std::istringstream iss(linea);
    const std::vector<int> v{std::istream_iterator<int>(iss),
                             std::istream_iterator<int>()};

    std::vector<int> doblados(v.size());
    std::transform(v.begin(), v.end(), doblados.begin(),
                   [](int x) { return x * 2; });

    const int total = std::accumulate(doblados.begin(), doblados.end(), 0);

    std::string sec;
    for (std::size_t i = 0; i < doblados.size(); ++i) {
        if (i > 0) sec += '-';
        sec += std::to_string(doblados[i]);
    }

    std::cout << "doblados=" << sec << " total=" << total << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** `std::transform` es el `map` y `std::accumulate` es el `reduce`,
y los dos existen desde la STL original de 1994. Lo que faltaba —y llegó con **C++11**— eran las
**lambdas**, sin las cuales había que declarar un objeto función aparte:

```cpp
// Antes de C++11:
struct Doblar { int operator()(int x) const { return x * 2; } };
std::transform(v.begin(), v.end(), d.begin(), Doblar{});

// Desde C++11:
std::transform(v.begin(), v.end(), d.begin(), [](int x) { return x * 2; });
```

Es la misma barrera que en Pascal y en Tcl: **la capacidad ya estaba; lo que faltaba era que
escribirla fuera barato**.

Y hay una propiedad que distingue a C++ de casi todos los demás lenguajes de esta página: **la lambda
no cuesta nada en ejecución**. Cada lambda tiene un tipo único generado por el compilador, así que
`std::transform` se instancia para ese tipo concreto y **el cuerpo se integra en línea**. No hay
llamada indirecta, no hay puntero a función, no hay asignación de memoria.

Compara con `std::function`, que sí borra el tipo y sí tiene coste:

```cpp
std::function<int(int)> f = [](int x) { return x * 2; };   // llamada indirecta
auto g = [](int x) { return x * 2; };                       // tipo concreto: gratis
```

Esa es la abstracción de coste cero de la clase 043, aplicada a las funciones de orden superior. Y la
captura —`[&]`, `[=]`, `[x]`— convierte la lambda en una clausura con las mismas reglas de tiempo de
vida que cualquier objeto: **capturar por referencia algo que muere antes deja una referencia
colgante**.

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

dcl-pi MAPRED;
  linea varchar(200) const;
end-pi;

dcl-s trozos varchar(20) dim(50);
dcl-s i      int(10);
dcl-s d      int(10);
dcl-s sec    varchar(500) inz('');
dcl-s total  int(20) inz(0);
dcl-s salida char(560);

trozos = %split(linea : ' ');

for i = 1 to %elem(trozos);
  d = %int(trozos(i)) * 2;
  total += d;
  if sec <> '';
    sec += '-';
  endif;
  sec += %char(d);
endfor;

salida = 'doblados=' + sec + ' total=' + %char(total);
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG **no tiene funciones de orden superior**: no hay lambdas, no
hay punteros a función con firma comprobada y no se puede pasar un procedimiento como argumento.

Lo que sí tiene, y es lo más cercano, son los **punteros a procedimiento**:

```rpgle
dcl-pr calcular int(10) extproc(pPtr);
  valor int(10) const;
end-pr;

dcl-s pPtr pointer;

pPtr = %paddr('DOBLAR');       // la DIRECCIÓN de un procedimiento
resultado = calcular(5);        // llamada indirecta
```

`%paddr` obtiene la dirección de un procedimiento y `extproc(puntero)` declara un prototipo que la
usa. Funciona, y es exactamente un puntero a función de C: **sin captura de entorno, sin
comprobación de tipos en la asignación y sin gestión de tiempo de vida**. Nadie lo escribe salvo para
interoperar con C o para tablas de despacho.

Y como en COBOL, el `reduce` real de un programa RPG está en otra parte:

```rpgle
exec sql
  select sum(importe * 2), count(*)
    into :total, :cuantos
    from movimientos;
```

`SUM`, `AVG`, `MAX`, `COUNT` y `GROUP BY` son las funciones de agregación de SQL, y son el pliegue que
el lenguaje no tiene. En una plataforma donde la base de datos es parte del sistema operativo, esa
delegación no es un rodeo: es la arquitectura.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 mapred: procedure options(main);

    declare linea character(200) varying;
    declare trozo character(20)  varying;
    declare sec   character(500) varying initial('');
    declare (i, p, v, d) fixed binary(31);
    declare total fixed binary(31) initial(0);

    get edit (linea) (a(200));
    linea = trim(linea) || ' ';

    p = 1;
    do i = 1 to length(linea);
       if substr(linea, i, 1) = ' ' then do;
          if i > p then do;
             trozo = substr(linea, p, i - p);
             v = trozo;
             d = v * 2;
             total = total + d;
             if sec ^= '' then sec = sec || '-';
             sec = sec || trim(char(d));
          end;
          p = i + 1;
       end;
    end;

    put skip list ('doblados=' || sec || ' total=' || trim(char(total)));

 end mapred;
```

**Lo que esta clase enseña en PL/I.** PL/I **sí puede pasar procedimientos como argumento**, con el
atributo `entry`:

```pli
declare aplicar entry (entry, fixed binary(31));

aplicar: procedure (f, x);
   declare f entry returns (fixed binary(31));
   declare x fixed binary(31);
   return (f(x));
end aplicar;
```

Un parámetro declarado `entry` es una referencia a un procedimiento. Está en el lenguaje desde 1964,
antes que en Pascal.

Lo que no tiene son **funciones anónimas ni clausuras**, así que aplica la misma barrera de siempre:
sin sintaxis ligera, no se usa.

Y PL/I tiene la agregación sobre arrays, que ya apareció en la clase 067:

```pli
declare v(100) fixed binary(31);

v = v * 2;                 /* map */
total = sum(v);            /* reduce */
p = prod(v);               /* producto */
```

`sum`, `prod`, `max`, `min`, `any`, `all`, `poly` son intrínsecas sobre arrays. Cubren los pliegues
frecuentes sin necesidad de un `reduce` general, que es la misma solución que Fortran y COBOL.

La conclusión de esta clase para los tres lenguajes de negocio es la misma: **cuando el lenguaje trae
las agregaciones que su dominio necesita, la abstracción general se echa menos de menos de lo que
parece**. Y cuando aparece un caso nuevo, hay que escribir el bucle.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
MAPRED ; Map y reduce -- clase 068
 read linea
 set sec = "", total = 0
 for i = 1:1:$length(linea, " ") do
 . set d = $piece(linea, " ", i) * 2
 . set total = total + d
 . set:sec'="" sec = sec _ "-"
 . set sec = sec _ d
 write "doblados=", sec, " total=", total, !
 quit
```

**Lo que esta clase enseña en M.** M no tiene funciones de orden superior en el sentido habitual,
pero tiene **indirección**, que da algo funcionalmente equivalente y mucho más peligroso:

```mumps
 set transformacion = "v*2"
 for i = 1:1:n do
 . set v = $piece(linea, " ", i)
 . set d = @transformacion         ; @ EVALÚA la cadena como una expresión
 . ...
```

`@` es el operador de indirección, y admite tres formas:

```mumps
 set x = @nombreVariable       ; indirección de NOMBRE
 do @nombreRutina              ; indirección de RUTINA
 set y = @expresion            ; indirección de EXPRESIÓN
 set @("^DATOS(" _ id _ ")") = valor   ; construir la referencia como TEXTO
```

Con eso, "la función" que se aplica puede venir de una variable, de un fichero de configuración o de
un *global* de la base de datos. Es enormemente flexible y es la razón de que muchos sistemas M
tengan tablas de reglas almacenadas como datos, que se ejecutan sin recompilar.

Y es la razón de que **no se pueda analizar estáticamente un programa M**: ninguna herramienta puede
decir qué se ejecuta, porque se decide en el momento. Es el `eval` de JavaScript con cincuenta años
más de historia, con la misma potencia y los mismos problemas de seguridad y mantenimiento.

Es un buen cierre para esta parte: **el código como dato aparece en muchos lenguajes, y la diferencia
entre que sea una virtud o un problema está en si hay comprobación de por medio**. En Lisp, una macro
opera sobre una estructura y el compilador la verifica; en M, sobre una cadena y nadie la verifica.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| valores doblados total sec |

valores := stdin nextLine substrings collect: [ :cada | cada asNumber ].
doblados := valores collect: [ :cada | cada * 2 ].
total := doblados inject: 0 into: [ :a :b | a + b ].

sec := String streamContents: [ :flujo |
    doblados do: [ :d | flujo print: d ] separatedBy: [ flujo nextPut: $- ] ].

Transcript
    show: 'doblados=', sec;
    show: ' total=', total printString;
    cr.
```

**Lo que esta clase enseña en Smalltalk.** `collect:` es el `map` e `inject:into:` es el `reduce`, y
los dos reciben **bloques** — que en Smalltalk son objetos de primera clase con clausura completa.

Y aquí está el punto de fondo de toda la Parte 4: **en Smalltalk no hay ninguna estructura de control
en el lenguaje**. `ifTrue:`, `whileTrue:`, `to:do:`, `and:`, `select:`, `collect:`, `inject:into:` son
**todos métodos que reciben bloques**. Las decisiones, los bucles, el cortocircuito y las funciones de
orden superior son **la misma cosa**: enviar un mensaje con un trozo de código dentro.

Eso significa que puedes añadir tus propias estructuras de control sin tocar el lenguaje:

```smalltalk
Number >> vecesConIndice: unBloque
    1 to: self do: [ :i | unBloque value: i ]

5 vecesConIndice: [ :i | Transcript show: i printString ]
```

Ningún otro lenguaje de esta página lo consigue con tan poca maquinaria: Lisp necesita macros, Tcl
necesita `uplevel`, C++ necesita plantillas, y Ada, Fortran, COBOL, PL/I y RPG no lo consiguen.

Y `inject:into:` merece su nombre: el valor inicial se "inyecta" y el bloque recibe **el acumulado y
el elemento**, en ese orden. Con él se escriben `sum`, `max`, `count`, `detect` y prácticamente todo
lo demás — de hecho, así están escritos en `Collection`, y puedes leerlos.

---

## Y de vuelta a la clase

Lo transferible es que **`map`/`filter`/`reduce` no son tres funciones: son la prueba de que el
lenguaje trata el código como un valor**. Cuando existen, aparecen solas todas las demás —`any`,
`all`, `count`, `sort` con comparador, `groupBy`— porque todas son la misma idea. Y cuando no
existen, no es que falten funciones: es que falta la capacidad, y ninguna biblioteca puede añadirla.
Es la diferencia entre COBOL y Lisp, y explica por qué Java tuvo que esperar a la versión 8.

⏮️ [Volver a la clase 068](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
