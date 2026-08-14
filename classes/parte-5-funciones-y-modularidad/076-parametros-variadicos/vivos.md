# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 076

> [⬅️ Volver a la clase 076](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Una función que suma **todos los números que le pases, sean los que sean**. Los parámetros variádicos
parecen imprescindibles hasta que se cuenta cuántos de estos lenguajes los tienen: **cuatro**. Los
otros ocho resuelven el problema con una idea distinta y, en varios casos, mejor — **pasar una
colección**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **aridad variable**, y estos lenguajes lo enseñan porque muestran que hay dos
> problemas distintos escondidos bajo el mismo nombre. Uno es **"no sé cuántos valores del mismo tipo
> vendrán"**, y para eso un array es mejor que un variádico: **Fortran** lo resuelve con arrays de
> forma supuesta, **Ada** con arrays no restringidos y **Pascal** con arrays abiertos, y los tres
> conservan el tipo y la comprobación.
>
> El otro es **"no sé cuántos ni de qué tipo"**, que es el caso de `printf`, y ahí sí hacen falta
> variádicos de verdad. En C es la fuente de una familia entera de vulnerabilidades; en C++ se resolvió
> con paquetes de plantilla comprobados al compilar.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con enteros separados por espacio → stdout: `suma=<suma de todos>`
- **Regla:** `suma(...nums) = Σ nums`

| stdin | esperado |
|---|---|
| `1 2 3` | `suma=6` |
| `5` | `suma=5` |
| `10 20 30 40` | `suma=100` |

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
PROGRAM-ID. SUMAVAR.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  I       PIC 9(4)  COMP-3.
01  LARGO   PIC 9(4)  COMP-3.
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(4)  COMP-3.
01  C       PIC X.
01  TOTAL   PIC S9(18) COMP-3.
01  ED-T    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE 0 TO TOTAL
    MOVE SPACES TO TOKEN
    MOVE 0 TO TLEN
    COMPUTE LARGO = FUNCTION LENGTH(FUNCTION TRIM(LINEA)) + 1

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > LARGO
        MOVE LINEA(I:1) TO C
        IF C = SPACE
            IF TLEN > 0
                COMPUTE TOTAL = TOTAL + FUNCTION NUMVAL(TOKEN(1:TLEN))
                MOVE SPACES TO TOKEN
                MOVE 0 TO TLEN
            END-IF
        ELSE
            ADD 1 TO TLEN
            MOVE C TO TOKEN(TLEN:1)
        END-IF
    END-PERFORM

    MOVE TOTAL TO ED-T
    DISPLAY "suma=" FUNCTION TRIM(ED-T)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** **COBOL no tiene parámetros variádicos**, y su respuesta es la
de la clase 065: una **tabla con `OCCURS DEPENDING ON`** y una variable que dice cuántos elementos
son válidos.

```cobol
01  LOTE.
    05  CUANTOS  PIC 9(4) COMP-3.
    05  VALOR    OCCURS 1 TO 500 TIMES
                 DEPENDING ON CUANTOS
                 PIC S9(9) COMP-3.

CALL "SUMAR" USING LOTE
```

Se pasa **un solo argumento** —la estructura entera— y dentro va el contador. Es exactamente lo que
esta clase recomienda: cuando todos los valores son del mismo tipo, una colección es mejor que una
lista variable de argumentos.

Y `OCCURS DEPENDING ON` tiene una propiedad que conviene señalar: **la longitud del registro cambia
con el contador**. Si `CUANTOS` vale 3, la estructura ocupa lo que ocupan tres elementos, no
quinientos. Al escribirla en un fichero, se escribe solo lo usado. Es un registro de longitud
variable declarado de forma declarativa, algo que en C exige el truco del *array flexible* al final
de un `struct`.

Lo que COBOL sí tiene, y es lo más parecido a un variádico, es el **`CALL` con lista variable** en el
sitio de la llamada, más la comprobación de cuántos llegaron con la extensión de IBM. Es incómodo y
apenas se usa: el bloque de parámetros de la clase 075 es la solución idiomática.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program suma_variadica
   implicit none
   character(len=1000) :: linea
   integer :: v(200), n, i, ios

   read(*, '(A)') linea

   n = 0
   do i = 1, 200
      read(linea, *, iostat=ios) v(1:i)
      if (ios /= 0) exit
      n = i
   end do

   write(*, '(A,I0)') 'suma=', suma_todos(v(1:n))

contains

   pure function suma_todos(valores) result(s)
      integer, intent(in) :: valores(:)      ! array de FORMA SUPUESTA
      integer :: s
      s = sum(valores)
   end function suma_todos

end program suma_variadica
```

**Lo que esta clase enseña en Fortran.** **Fortran no tiene variádicos**, y su respuesta —`valores(:)`,
un **array de forma supuesta**— es probablemente mejor que un variádico para este caso.

`integer, intent(in) :: valores(:)` significa "un array de una dimensión, del tamaño que sea". La
función recibe **el array y su forma**, así que `size(valores)`, `lbound` y `ubound` funcionan dentro
sin que nadie pase un contador.

```fortran
function f(v)
   real, intent(in) :: v(:)        ! forma supuesta: tamaño desconocido, forma conocida
   real, intent(in) :: m(:,:)      ! una matriz de cualquier tamaño
   ...
   n = size(v)                      ! el tamaño viaja CON el array
```

Compara con C, donde hay que pasar `int* v, size_t n` y confiar en que quien llama no se equivoque —
la causa de una parte enorme de los desbordamientos de búfer de la historia.

Fortran tiene además la **forma diferida** (`allocatable`, el tamaño se decide al asignar) y la
**forma explícita** (`v(n)`, con `n` como parámetro anterior), y elegir entre las tres es una decisión
de rendimiento: la forma supuesta pasa un descriptor y permite pasar porciones no contiguas; la
explícita garantiza memoria contigua y vectoriza mejor.

Y para el caso de "distintos tipos", Fortran no tiene nada: la interoperabilidad con `printf` de C se
hace con `iso_c_binding` y es incómoda a propósito.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Suma_Variadica is

   type Vector is array (Positive range <>) of Integer;   --  tamaño NO restringido

   function Suma_Todos (V : Vector) return Integer is
      S : Integer := 0;
   begin
      for E of V loop
         S := S + E;
      end loop;
      return S;
   end Suma_Todos;

   Linea  : String (1 .. 500);
   Ultimo : Natural;
   Pos    : Positive := 1;
   Fin    : Positive;
   Datos  : Vector (1 .. 200);
   N      : Natural := 0;
begin
   Get_Line (Linea, Ultimo);

   while Pos <= Ultimo loop
      N := N + 1;
      Get (Linea (Pos .. Ultimo), Datos (N), Fin);
      Pos := Fin + 1;
   end loop;

   Put ("suma=");
   Put (Suma_Todos (Datos (1 .. N)), Width => 1);
   New_Line;
end Suma_Variadica;
```

**Lo que esta clase enseña en Ada.** `array (Positive range <>)` es un **tipo de array no
restringido**: el tipo existe, pero el tamaño se fija al declarar cada objeto. El `<>` se lee "caja",
y es la forma de Ada de decir "aquí va un rango que decidirás luego".

```ada
type Vector is array (Positive range <>) of Integer;

V1 : Vector (1 .. 10);
V2 : Vector (1 .. N);              --  tamaño en EJECUCIÓN
V3 : constant Vector := (1, 2, 3); --  deducido del agregado
```

Y una función que recibe `V : Vector` acepta **cualquiera de los tres**, con sus límites reales
disponibles dentro: `V'First`, `V'Last`, `V'Length`, `V'Range`. **Los límites viajan con el array**,
igual que en Fortran.

Eso es lo que hace innecesarios los variádicos para el caso homogéneo, y además permite la
construcción de este programa: `Datos (1 .. N)` es una **porción**, y pasarla es pasar solo esa parte
sin copiar.

Fíjate también en que `String` en Ada **es exactamente eso**: `array (Positive range <>) of
Character`. Por eso las funciones sobre cadenas de la clase 048 son funciones sobre arrays, y por eso
`Trim` funciona con cualquier longitud.

Ada **no tiene variádicos heterogéneos**, y es deliberado: en un sistema que hay que certificar, una
función cuyo número y tipo de argumentos no se conoce al compilar es exactamente lo que no se quiere.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program SumaVariadica;
{$MODE OBJFPC}{$H+}
uses SysUtils;

function SumaTodos(const V: array of Integer): Integer;   { ARRAY ABIERTO }
var
  I: Integer;
begin
  Result := 0;
  for I := Low(V) to High(V) do
    Result := Result + V[I];
end;

var
  Linea, Token: string;
  I: Integer;
  Datos: array of Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea) + ' ';
  SetLength(Datos, 0);
  Token := '';

  for I := 1 to Length(Linea) do
  begin
    if Linea[I] = ' ' then
    begin
      if Token <> '' then
      begin
        SetLength(Datos, Length(Datos) + 1);
        Datos[High(Datos)] := StrToInt(Token);
        Token := '';
      end;
    end
    else
      Token := Token + Linea[I];
  end;

  WriteLn('suma=', IntToStr(SumaTodos(Datos)));
end.
```

**Lo que esta clase enseña en Pascal.** `array of Integer` **como tipo de parámetro** es un **array
abierto**: acepta un array de cualquier longitud, y dentro se usan `Low` y `High` para conocer sus
límites. Es la aportación de Turbo Pascal 7 y Delphi, y es el equivalente de la forma supuesta de
Fortran.

Hay un detalle importante: **dentro de la función, un array abierto SIEMPRE va de 0 a High(V)**, sin
importar los índices que tuviera el original. Por eso se escribe `Low(V)` y no `1`.

Y Object Pascal tiene además el **constructor de array en la llamada**, que es lo más parecido a un
variádico:

```pascal
WriteLn(SumaTodos([1, 2, 3, 4]));           { array abierto construido al vuelo }
```

Para el caso **heterogéneo** —el de `printf`— existe `array of const`, que es el mecanismo real de
`Format`:

```pascal
procedure Registrar(const Msg: string; const Args: array of const);
...
Registrar('%s tiene %d años', ['Ada', 36]);
```

`array of const` recibe un array de `TVarRec`, un registro con **una etiqueta de tipo y una unión**.
Es decir: Object Pascal implementa los variádicos heterogéneos **como datos con tipo comprobado en
ejecución**, no como una convención de llamada insegura.

Esa es la diferencia con el `...` de C: aquí el tipo de cada argumento **viaja con él**, así que
`Format` puede comprobar que `%d` recibe un entero en lugar de leer la pila a ciegas.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(defun suma-todos (&rest numeros)
  (reduce #'+ numeros :initial-value 0))

(let ((lista (loop for v = (read *standard-input* nil :fin)
                   until (eq v :fin)
                   collect v)))
  (format t "suma=~D~%" (apply #'suma-todos lista)))
```

**Lo que esta clase enseña en Common Lisp.** `&rest numeros` recoge **todos los argumentos restantes
en una lista**, y `apply` hace lo contrario: **convierte una lista en argumentos**.

```lisp
(suma-todos 1 2 3)              ; numeros vale (1 2 3)
(apply #'suma-todos '(1 2 3))   ; equivalente: la lista se DESPLIEGA
(apply #'suma-todos 1 2 '(3 4)) ; los primeros sueltos, el último desplegado
```

`&rest` y `apply` son las dos direcciones del mismo puente, y esa simetría es lo que hace cómodo
envolver funciones en Lisp:

```lisp
(defun con-registro (f &rest args)
  (format t "llamando con ~S~%" args)
  (apply f args))                       ; pasa TODO adelante, sin conocer la aridad
```

Esa función envuelve **cualquier** función, con cualquier número de argumentos, sin declarar nada. En
un lenguaje con firmas fijas eso exige plantillas variádicas o reflexión.

Lisp tiene además **`&body`**, que es idéntico a `&rest` pero le dice al editor que ese argumento es
un cuerpo de código y debe indentarlo como tal. Es metadatos para las herramientas dentro de la
firma — un detalle pequeño y muy revelador de una cultura donde el entorno importa tanto como el
lenguaje.

Y hay un límite práctico que conviene conocer: `call-arguments-limit` define cuántos argumentos admite
una llamada. En SBCL es enorme, pero `(apply #'+ lista-de-un-millón)` puede fallar. Para eso está
`reduce`, que es lo que usa este programa por dentro.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
proc sumaTodos {args} {
    set t 0
    foreach v $args { incr t $v }
    return $t
}

gets stdin linea

puts "suma=[sumaTodos {*}[split [string trim $linea]]]"
```

**Lo que esta clase enseña en Tcl.** **`args` es un nombre mágico**: si el último parámetro de un
`proc` se llama exactamente `args`, recibe **una lista con todos los argumentos sobrantes**.

```tcl
proc f {a b args} { ... }
f 1 2 3 4 5          ;# a=1, b=2, args={3 4 5}
```

No hay sintaxis especial —ni `...`, ni `&rest`, ni `*`—: es una **convención sobre el nombre**, lo
que encaja con que la lista de parámetros de `proc` sea una lista normal (clase 074).

Y **`{*}`** es el operador inverso, la **expansión**, añadido en Tcl 8.5:

```tcl
set lista {1 2 3}
sumaTodos $lista          ;# UN argumento: la lista entera como una cadena
sumaTodos {*}$lista       ;# TRES argumentos: 1, 2 y 3
```

Esa distinción es exactamente `f(lista)` frente a `f(*lista)` en Python, y su ausencia era una de las
quejas históricas de Tcl: antes de 8.5 había que usar `eval` con las comillas cuidadosamente puestas,
lo que era lento y una vía de inyección.

`{*}` es un ejemplo curioso de diseño: **no es un comando ni un operador**, es una marca que el
analizador reconoce delante de una palabra. Se eligió esa sintaxis rara precisamente para que no
pudiera chocar con ningún nombre de comando existente en treinta años de código.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

sub suma_todos {
    my $t = 0;
    $t += $_ for @_;
    return $t;
}

my $linea = <STDIN>;
chomp $linea;

print "suma=", suma_todos(split ' ', $linea), "\n";
```

**Lo que esta clase enseña en Perl.** En Perl **todas las subrutinas son variádicas por defecto**. No
hay que declarar nada: `@_` contiene lo que haya llegado, y punto. Es el extremo opuesto de Ada.

Y eso ocurre porque **las listas se aplanan al pasarlas**:

```perl
suma_todos(1, 2, 3);              # @_ = (1, 2, 3)
suma_todos(@lista);               # @_ = los elementos de @lista
suma_todos(@a, @b);               # @_ = los de @a Y los de @b, mezclados
```

Esa última línea es la trampa clásica: **no se pueden pasar dos arrays a una función y distinguirlos
dentro**, porque llegan aplanados en uno solo. La solución es pasar **referencias**:

```perl
procesar(\@a, \@b);              # dos referencias: dos argumentos
sub procesar { my ($ra, $rb) = @_; ... @$ra ... }
```

Ese aplanamiento es una decisión de diseño muy de Perl —cómoda el 90 % de las veces y sorprendente el
10 %— y es la razón de que las referencias sean tan centrales en el lenguaje.

Con las **firmas** de 5.36, el variádico se declara explícitamente y se puede combinar:

```perl
use v5.36;
sub log_msg ($nivel, @resto) { ... }        # uno fijo y el resto
sub config ($nombre, %opciones) { ... }     # uno fijo y pares nombrados
```

Y `$t += $_ for @_;` de este programa es el modificador de sentencia de la clase 064, con `$_` como
sujeto implícito.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <iterator>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>

int main() {
    std::string linea;
    if (!std::getline(std::cin, linea)) return 1;

    //  El número de valores se conoce en EJECUCIÓN, así que un paquete de
    //  plantilla no sirve: hay que usar un contenedor.
    std::istringstream iss(linea);
    const std::vector<int> v{std::istream_iterator<int>(iss),
                             std::istream_iterator<int>()};

    std::cout << "suma=" << std::accumulate(v.begin(), v.end(), 0) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** El comentario del código es la lección: **los variádicos de C++
son de tiempo de compilación**, así que no sirven cuando el número de valores se conoce en ejecución.
Para eso, un contenedor.

Cuando sí se conocen al compilar, C++11 trajo los **paquetes de plantilla** y C++17 las **expresiones
de plegado**, que los hacen legibles:

```cpp
template <typename... Args>
auto suma_todos(Args... args) {
    return (args + ... + 0);        // expresión de PLEGADO, C++17
}

suma_todos(1, 2, 3, 4);             // se genera una función para ESTA llamada
```

Y aquí está la diferencia decisiva con el `...` de C: **el paquete conserva los tipos**. El compilador
genera una función específica, comprueba cada argumento y puede integrarla en línea. No hay
`va_arg`, no hay que decir cuántos son y no se puede leer la pila a ciegas.

Ese `...` heredado de C sigue existiendo y es el mecanismo de `printf`, con toda su familia de
vulnerabilidades: si el formato no coincide con los argumentos, `printf` lee memoria arbitraria. Por
eso C++20 añadió **`std::format`**, que valida el formato **en tiempo de compilación**:

```cpp
std::format("{} tiene {} años", nombre, edad);     // comprobado al COMPILAR
std::print("{:.2f}\n", x);                         // C++23
```

Y para el caso homogéneo hay `std::initializer_list<T>`, que es lo que permite escribir
`f({1, 2, 3})` con tipo comprobado y sin plantillas.

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

dcl-pi SUMAVAR;
  linea varchar(200) const;
end-pi;

dcl-s trozos varchar(20) dim(50);
dcl-s i      int(10);
dcl-s total  int(20) inz(0);
dcl-s salida char(40);

trozos = %split(linea : ' ');

for i = 1 to %elem(trozos);
  total += %int(trozos(i));
endfor;

salida = 'suma=' + %char(total);
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG **no tiene variádicos de verdad**, y tiene dos aproximaciones
que conviene distinguir.

La primera es la de la clase 074: **varios `options(*nopass)` y `%parms`**.

```rpgle
dcl-pi *n int(20);
  a int(10) const;
  b int(10) const options(*nopass);
  c int(10) const options(*nopass);
  d int(10) const options(*nopass);
end-pi;

select;
  when %parms = 4; return a + b + c + d;
  when %parms = 3; return a + b + c;
  ...
```

Funciona hasta un máximo fijo y es tan incómodo como parece. Es exactamente lo que hacen las
bibliotecas de C antes de los variádicos: declarar `f2`, `f3`, `f4`.

La segunda, y la correcta, es la de este programa: **pasar una matriz**, con `%elem` para saber
cuántos elementos tiene. Es la misma conclusión que Fortran, Ada y COBOL — **para el caso homogéneo,
una colección**.

Y RPG tiene una tercera vía para el caso heterogéneo, que se usa al llamar a APIs del sistema:
`options(*varsize)` más un puntero y un descriptor de longitud. Es programación de bajo nivel, con las
mismas garantías que el `...` de C —ninguna—, y por eso se limita a las llamadas al sistema
operativo.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 sumavar: procedure options(main);

    declare linea character(200) varying;
    declare (i, p, total) fixed binary(31);

    get edit (linea) (a(200));
    linea = trim(linea) || ' ';

    total = 0;
    p = 1;
    do i = 1 to length(linea);
       if substr(linea, i, 1) = ' ' then do;
          if i > p then total = total + substr(linea, p, i - p);
          p = i + 1;
       end;
    end;

    put skip list ('suma=' || trim(char(total)));

 end sumavar;
```

**Lo que esta clase enseña en PL/I.** PL/I **no tiene variádicos**, y su respuesta es la de los demás
lenguajes de negocio: **arrays con límites consultables**.

```pli
declare v(*) fixed binary(31);          /* array de límites SUPUESTOS */

suma: procedure (v) returns (fixed binary(31));
   declare v(*) fixed binary(31);
   declare (i, t) fixed binary(31);
   t = 0;
   do i = lbound(v, 1) to hbound(v, 1);   /* los límites REALES */
      t = t + v(i);
   end;
   return (t);
end suma;
```

`v(*)` declara un parámetro array **cuyos límites se toman del argumento**, y `lbound`/`hbound` los
consultan dentro. Es exactamente la forma supuesta de Fortran y el array no restringido de Ada.

Y PL/I tiene una capacidad relacionada que no tiene ningún lenguaje del núcleo: **arrays de límites
ajustables en ejecución**, con expresiones que dependen de otros parámetros.

```pli
p: procedure (n, v);
   declare n fixed binary(31);
   declare v(n, n) fixed decimal(15,2);   /* ¡matriz n×n, con n del argumento! */
```

Una matriz cuadrada cuyo tamaño se decide al llamar, con toda la aritmética de arrays de la clase 067
disponible sobre ella. En C haría falta memoria dinámica y aritmética de punteros; en C++, un
`vector<vector<double>>` con su indirección.

Es otra muestra de lo que se repite en toda esta sección: PL/I tenía una cantidad notable de buenas
ideas, y su problema fue el conjunto, no las piezas.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
SUMAVAR ; Variadicos -- clase 076
 read linea
 write "suma=", $$suma(linea), !
 quit
 ;
suma(l) ; suma los enteros separados por espacio en l
 new i, t
 set t = 0
 for i = 1:1:$length(l, " ") set t = t + $piece(l, " ", i)
 quit t
```

**Lo que esta clase enseña en M.** M **sí acepta un número variable de argumentos**, y de la forma más
permisiva posible: **puedes llamar a cualquier rutina con menos o con más argumentos de los
declarados**, sin ninguna comprobación.

```mumps
suma(a, b, c) ;
 quit $get(a, 0) + $get(b, 0) + $get(c, 0)
 ;
 write $$suma(1)          ; b y c quedan indefinidas; $get las pone a 0
 write $$suma(1, 2, 3, 4) ; el cuarto se ignora
```

Es la misma uniformidad de la clase 074: **la ausencia de un parámetro es simplemente una variable no
definida**, y `$data`/`$get` la manejan igual que cualquier otra ausencia.

Para el caso verdaderamente variable, M usa las dos estructuras que ya conocemos:

```mumps
 do PROC^RUT(.datos)          ; un ARRAY por referencia: cualquier número de elementos
 set l = "1^2^3^4"            ; o una cadena con delimitadores
```

El array por referencia es la forma idiomática, y tiene una ventaja sobre los variádicos de otros
lenguajes: **puede ser jerárquico**. `datos("cliente","direccion","calle")` es un argumento tan válido
como `datos(1)`.

Y el M estándar tiene `$quit` y, en implementaciones modernas, formas de consultar cuántos argumentos
se pasaron. Pero el idioma dominante sigue siendo `$get` con valor por defecto, porque no distingue
"no vino" de "vino vacío" — y en M eso casi nunca importa.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| valores |

valores := stdin nextLine substrings collect: [ :cada | cada asNumber ].

Transcript
    show: 'suma=', (valores inject: 0 into: [ :a :b | a + b ]) printString;
    cr.
```

**Lo que esta clase enseña en Smalltalk.** **Smalltalk no tiene variádicos, y no puede tenerlos**: el
número de argumentos está fijado por el **selector**, como se vio en la clase 073. Un método llamado
`con:y:` recibe exactamente dos, siempre.

Su respuesta es la que esta clase recomienda: **pasar una colección**.

```smalltalk
coleccion sum
coleccion inject: 0 into: [ :a :b | a + b ]
(Array with: 1 with: 2 with: 3) sum
#(1 2 3 4) sum                        "literal de array"
{ 1. 2. base + 1 } sum                "array construido en EJECUCIÓN"
```

`{ ... }` con puntos es el constructor dinámico de arrays de Pharo, y `#( ... )` el literal. Los dos
producen una colección que se pasa como un único argumento.

Y para el caso en que **el número de argumentos se decide en ejecución** —envolver una llamada, un
proxy, un despachador— Smalltalk tiene el mecanismo de reflexión:

```smalltalk
receptor perform: #con:y: with: 1 with: 2
receptor perform: unSelector withArguments: unArray     "¡el apply de Lisp!"
```

`perform:withArguments:` es exactamente `apply`: toma un **selector** y un **array**, y envía el
mensaje. Con él se escriben proxies genéricos, y combinado con `doesNotUnderstand:` de la clase 051 se
construyen objetos que responden a mensajes que nadie implementó.

Es la misma capacidad que `apply` en Lisp y `{*}` en Tcl, obtenida por reflexión sobre el sistema de
objetos.

---

## Y de vuelta a la clase

La regla práctica: **si todos los argumentos son del mismo tipo, no quieres variádicos, quieres una
colección**. Es más seguro, se puede recorrer dos veces, se puede pasar adelante sin perder la aridad,
y el compilador conserva el tipo. Los variádicos solo son necesarios cuando el número **y los tipos**
varían — y entonces la pregunta es si el lenguaje los comprueba (C++, Lisp) o confía (C, PL/I).

⏮️ [Volver a la clase 076](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
