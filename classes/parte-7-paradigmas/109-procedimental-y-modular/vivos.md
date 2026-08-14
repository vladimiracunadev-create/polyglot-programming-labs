# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 109

> [⬅️ Volver a la clase 109](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Un promedio calculado por un procedimiento reutilizable. Aquí aparece la distinción que estos
lenguajes hacen y los modernos han borrado: **procedimiento frente a función**. COBOL, Fortran, Ada,
Pascal, PL/I y RPG **tienen las dos cosas con nombres distintos** —lo que devuelve un valor y lo que
hace algo— y esa separación, que hoy parece burocrática, dice más de lo que parece sobre la intención
del código.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **descomposición en unidades con nombre**, y estos lenguajes lo enseñan porque
> recorrieron el camino entero. **COBOL empezó con párrafos** —trozos de código sin parámetros ni
> variables propias, invocados con `PERFORM`— y tardó hasta 1985 en tener algo parecido a una función
> local. **Fortran tenía subrutinas desde 1957** pero con variables estáticas y sin recursión.
> **Pascal y Ada** llegaron con procedimientos anidados, parámetros por valor y por referencia
> declarados, y ámbito léxico completo.
>
> Y el paso siguiente —**agrupar procedimientos en módulos**— es la clase 086, que estos mismos
> lenguajes resolvieron con cuarenta años de diferencia entre ellos.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con enteros separados por espacio → stdout: `promedio=<suma dividida entre la cantidad, entera>`
- **Regla:** `promedio = suma / cantidad (división entera)`

| stdin | esperado |
|---|---|
| `2 4 6` | `promedio=4` |
| `10` | `promedio=10` |
| `3 5` | `promedio=4` |

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
PROGRAM-ID. PROMEDIO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA  PIC X(200).
01  TOKEN  PIC X(20).
01  TLEN   PIC 9(2)  COMP VALUE 0.
01  I      PIC 9(4)  COMP.
01  N      PIC 9(4)  COMP VALUE 0.
01  SUMA   PIC S9(18) COMP-3 VALUE 0.
01  PROM   PIC S9(18) COMP-3.
01  ED-P   PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE SPACES TO TOKEN

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        IF LINEA(I:1) = SPACE
            PERFORM ACUMULAR
        ELSE
            ADD 1 TO TLEN
            MOVE LINEA(I:1) TO TOKEN(TLEN:1)
        END-IF
    END-PERFORM
    PERFORM ACUMULAR

    PERFORM CALCULAR-PROMEDIO

    MOVE PROM TO ED-P
    DISPLAY "promedio=" FUNCTION TRIM(ED-P)
    STOP RUN.

ACUMULAR.
    IF TLEN > 0
        ADD 1 TO N
        COMPUTE SUMA = SUMA + FUNCTION NUMVAL(TOKEN)
        MOVE SPACES TO TOKEN
        MOVE 0 TO TLEN
    END-IF.

CALCULAR-PROMEDIO.
    IF N > 0
        COMPUTE PROM = SUMA / N
    ELSE
        MOVE 0 TO PROM
    END-IF.
```

**Lo que esta clase enseña en COBOL.** El `PERFORM CALCULAR-PROMEDIO` de este programa **no es una
llamada a función**: es un salto a un párrafo, y esa diferencia es la carencia histórica de COBOL en
esta clase.

Un **párrafo** no tiene parámetros, no tiene valor de retorno y no tiene variables locales: opera
sobre las variables globales del programa (clase 082). Es un trozo de código con nombre, y nada más.

Eso obliga a un estilo concreto: **el párrafo se comunica por variables globales**, y hay que saber
cuáles lee y cuáles escribe. En un programa de cinco mil líneas con doscientos párrafos, esa
información no está escrita en ninguna parte.

De ahí sale la convención universal de prefijos por función —`WS-CALC-IMPORTE`, `WS-VAL-ENTRADA`— y de
ahí sale también el `PERFORM THRU`, que merece mención por lo frágil:

```cobol
PERFORM PARRAFO-A THRU PARRAFO-C
```

Eso ejecuta **todo lo que haya entre los dos párrafos**, en el orden físico del fuente. Insertar un
párrafo nuevo entre A y C **cambia el comportamiento** de esa línea, que está a mil líneas de
distancia. Es una dependencia del orden del texto, y es una de las cosas que más miedo dan al
modificar código COBOL antiguo.

COBOL sí ofrece funciones de verdad, por dos vías:

```cobol
*> 1. Otro PROGRAMA, con LINKAGE SECTION y RETURNING
CALL "CALCPROM" USING BY REFERENCE TABLA RETURNING RESULTADO

*> 2. COBOL-2002: una FUNCTION de usuario, invocable como las intrínsecas
IDENTIFICATION DIVISION.
FUNCTION-ID. PROMEDIO.
DATA DIVISION.
LINKAGE SECTION.
01  ENTRADA  PIC S9(18) COMP-3.
01  CUANTOS  PIC 9(4) COMP.
01  RESULTADO PIC S9(18) COMP-3.
PROCEDURE DIVISION USING ENTRADA CUANTOS RETURNING RESULTADO.
```

La **`FUNCTION-ID` de COBOL-2002** es lo que faltaba: una función con parámetros, valor de retorno y
`LOCAL-STORAGE` propio, invocable con `FUNCTION PROMEDIO(...)` igual que las intrínsecas.

Existe desde hace más de veinte años y sigue siendo minoritaria, por la razón de siempre: **el código
que hay escrito no la usa, y el estilo se hereda del código que hay**.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program prom
   implicit none
   integer :: v(100), n, ios, i

   character(len=400) :: linea

   read(*, '(A)') linea

   n = 0
   do i = 1, 100
      read(linea, *, iostat=ios) v(1:i)
      if (ios /= 0) exit
      n = i
   end do

   write(*, '(A,I0)') 'promedio=', promedio(v(1:n))

contains

   pure function promedio(x) result(r)      ! una FUNCIÓN, con interfaz explícita
      integer, intent(in) :: x(:)            ! arreglo de tamaño ASUMIDO
      integer :: r
      if (size(x) == 0) then
         r = 0
      else
         r = sum(x) / size(x)
      end if
   end function promedio

end program prom
```

**Lo que esta clase enseña en Fortran.** La distinción del gancho de esta clase es explícita en
Fortran y estructural:

```fortran
subroutine hacer_algo(x, y)     ! PROCEDIMIENTO: se invoca con CALL, no devuelve
function calcular(x) result(r)   ! FUNCIÓN: se usa en una expresión
```

Y esa separación tiene consecuencias reales: una `function` puede aparecer dentro de una expresión y
por tanto **el compilador puede reordenar o eliminar su llamada** si no la necesita — de ahí la
importancia de `pure` (clase 084). Una `subroutine` es una sentencia y se ejecuta siempre.

Lo que muestra este programa es el Fortran moderno, y cada palabra clave importa:

- **`contains`** mete el procedimiento **dentro** del programa, lo que da **interfaz explícita
  automática**: el compilador comprueba los argumentos. Un procedimiento externo suelto, al estilo
  clásico, **no se comprueba**.
- **`intent(in)`** declara el modo del parámetro (clase 079), y el compilador impide modificarlo.
- **`x(:)`** es un **arreglo de forma asumida**: recibe el tamaño con el argumento, sin pasarlo
  aparte. Es el `range <>` de Ada (clase 089), y llegó en Fortran 90.
- **`pure`** garantiza que no hay efectos.

Compara con el Fortran clásico, donde nada de eso existía:

```fortran
      SUBROUTINE PROM(X, N, R)
      INTEGER X(N)
      ...
      END
```

Sin `intent`, sin interfaz comprobada, con el tamaño pasado a mano y con **variables locales
estáticas** —una sola copia, sin recursión (clase 097)—. Llamar con los argumentos en otro orden o de
otro tipo **compilaba sin avisar**, y el error aparecía como datos corruptos.

Ese es el motivo real de que "modernizar Fortran" signifique, sobre todo, **meter los procedimientos
en módulos** (clase 086): no por elegancia, sino porque **el módulo es lo que activa la comprobación
de las llamadas**.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Prom is
   type Vector is array (Positive range <>) of Integer;

   function Promedio (V : Vector) return Integer is
      Suma : Integer := 0;
   begin
      if V'Length = 0 then
         return 0;
      end if;
      for I in V'Range loop
         Suma := Suma + V (I);
      end loop;
      return Suma / V'Length;
   end Promedio;

   Datos  : Vector (1 .. 100);
   N      : Natural := 0;
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
      N := N + 1;
      Datos (N) := Valor;
      Pos := Fin + 1;
   end loop;

   Put ("promedio=");
   Put (Promedio (Datos (1 .. N)), Width => 1);
   New_Line;
end Prom;
```

**Lo que esta clase enseña en Ada.** Ada distingue `procedure` de `function` como Fortran, y añade una
regla que ningún otro lenguaje de esta página tiene: **hasta Ada 2012, una función NO podía tener
parámetros modificables**.

```ada
function F (X : in out Integer) return Integer;   --  ILEGAL antes de Ada 2012
```

Solo `in`. La intención era clara: **si algo devuelve un valor, no debería cambiar el mundo**. Es
pureza impuesta por la gramática, veinte años antes de que la programación funcional se pusiera de
moda.

Ada 2012 lo relajó —permite `in out` en funciones— y a cambio introdujo algo mejor: **los aspectos de
contrato**.

```ada
function Promedio (V : Vector) return Integer
   with Pre  => V'Length > 0,
        Post => Promedio'Result * V'Length <= Suma_De (V);
```

`Pre` es lo que el llamante debe garantizar; `Post`, lo que la función promete. Se comprueban en
ejecución, y **con SPARK se demuestran en compilación** (clase 107).

Fíjate además en la declaración del tipo:

```ada
type Vector is array (Positive range <>) of Integer;
```

`range <>` (clase 089) permite que `Promedio` reciba **cualquier tamaño**, y `V'Length` y `V'Range`
vienen con el argumento. Y la llamada `Promedio (Datos (1 .. N))` **pasa una sección del arreglo**,
con sus límites, sin copiar y sin pasar `N` aparte.

Y hay un rasgo de Ada que esta clase es el sitio para nombrar: **los parámetros con nombre en la
llamada**.

```ada
Dibujar (Ancho => 10, Alto => 5, Color => Rojo);
Dibujar (Alto => 5, Ancho => 10, Color => Rojo);    --  el mismo efecto
```

Con valores por defecto y asociación por nombre, **el orden deja de importar** y la llamada documenta
qué es cada cosa. Es lo que Python tiene con los argumentos por palabra clave, y en Ada está desde
1983 — y en C++ sigue sin estar.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Prom;
{$MODE OBJFPC}{$H+}
uses SysUtils;

type
  TVector = array of Integer;

function Promedio(const V: TVector): Integer;
var
  I, Suma: Integer;
begin
  if Length(V) = 0 then
    Exit(0);
  Suma := 0;
  for I := 0 to High(V) do
    Suma := Suma + V[I];
  Result := Suma div Length(V);
end;

var
  V: TVector;
  Linea, Tok: string;
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
        SetLength(V, Length(V) + 1);
        V[High(V)] := StrToInt(Tok);
        Tok := '';
      end;
    end
    else
      Tok := Tok + C;
  end;

  WriteLn('promedio=', IntToStr(Promedio(V)));
end.
```

**Lo que esta clase enseña en Pascal.** Pascal es donde la distinción del gancho está más marcada, y
donde tiene la consecuencia sintáctica más visible:

```pascal
procedure Hacer(X: Integer);              { no devuelve nada }
function Calcular(X: Integer): Integer;    { devuelve, y se usa en una expresión }
```

Y el valor de retorno se asigna **al nombre de la función**, no con `return`:

```pascal
function Doble(X: Integer): Integer;
begin
  Doble := X * 2;        { Pascal estándar }
  Result := X * 2;       { Delphi y Free Pascal: la variable implícita Result }
end;
```

La forma original —asignar al nombre— tiene una peculiaridad que confunde: **leer el nombre dentro de
la función es una llamada recursiva**, no una lectura del valor. Delphi introdujo `Result` para
resolverlo, y hoy es lo idiomático.

`Exit(0)` en este programa es la salida anticipada con valor, que Free Pascal y Delphi añadieron —el
Pascal original no la tenía (clase 108).

Y los **modos de parámetro** de Pascal son de los más completos y explícitos:

```pascal
procedure P(X: Integer);            { por VALOR: copia }
procedure P(var X: Integer);         { por REFERENCIA: puede modificar }
procedure P(const X: TRegistro);     { constante: NO copia y NO puede modificar }
procedure P(out X: Integer);          { solo salida: no lee el valor entrante }
```

**`const` es el importante y el más olvidado.** Sin él, pasar un registro grande o una cadena **copia
todos sus bytes en cada llamada** (clase 096). Con `const`, se pasa la dirección y el compilador
prohíbe modificarlo. En código Pascal con estructuras grandes, **poner `const` es la optimización más
rentable que existe**.

Y `out` es una precisión que casi nadie tiene: dice que el parámetro **es solo de salida**, así que el
compilador no avisa de que se usa sin inicializar y el llamante sabe que su valor previo se descarta.
Es el `intent(out)` de Fortran y el `out` de Ada, y C# lo copió de aquí.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(defun promedio (lista)
  (if (null lista)
      0
      (floor (reduce #'+ lista) (length lista))))

(let ((v '()))
  (loop for x = (read *standard-input* nil nil)
        while x
        do (push x v))
  (format t "promedio=~D~%" (promedio v)))
```

**Lo que esta clase enseña en Common Lisp.** Lisp **no distingue procedimiento de función**: todo es
una función y todo devuelve un valor. Un `defun` que solo imprime devuelve el valor de su última
forma, y nadie está obligado a usarlo.

Lo que Lisp tiene en esta clase, y es único, es una lista de parámetros extraordinariamente rica
(clase 077):

```lisp
(defun f (a b                       ; obligatorios
          &optional (c 10)           ; opcional CON VALOR POR DEFECTO
          &rest resto                ; los demás, en una lista
          &key (modo :rapido) nivel  ; por PALABRA CLAVE
          &aux (tmp (* a b)))        ; variables locales en la propia firma
  ...)

(f 1 2 :modo :lento :nivel 3)
```

**`&key` es lo que en Ada son los parámetros con nombre y en Python los argumentos por palabra
clave**, y Common Lisp lo tenía en 1984. `&aux` no lo tiene casi nadie: declara variables auxiliares
en la firma, evitando un `let` anidado.

Y hay una capacidad que va más allá de todo lo anterior: **las funciones se pueden redefinir en
ejecución**, y con `defmethod` de CLOS, **especializar por tipo sin tocar la función original**.

```lisp
(defgeneric describir (x))
(defmethod describir ((x integer)) "un entero")
(defmethod describir ((x string))  "una cadena")
(defmethod describir ((x persona)) "una persona")
```

Añadir un caso es escribir un `defmethod` **en otro fichero, cargado después, sin recompilar nada**.
Es la solución de Lisp al *expression problem* de la clase 100.

Y `floor` con dos argumentos merece una nota, porque resuelve algo que en otros lenguajes es una
trampa: **devuelve el cociente entero y el resto, y redondea siempre hacia abajo**. En C, C++, Java y
Fortran, la división entera de un negativo **trunca hacia cero**, así que `-7 / 2` da −3 y no −4.
Common Lisp ofrece las cuatro políticas con nombre —`floor`, `ceiling`, `truncate`, `round`— y obliga
a elegir. Es más honesto que tener una y llamarla "la división".

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
proc promedio {lista} {
    if {[llength $lista] == 0} {
        return 0
    }
    set suma 0
    foreach x $lista {
        incr suma $x
    }
    return [expr {$suma / [llength $lista]}]
}

gets stdin linea
puts "promedio=[promedio [split [string trim $linea]]]"
```

**Lo que esta clase enseña en Tcl.** `proc` define un comando, y **un comando definido por el usuario
es indistinguible de uno del núcleo**: se invoca igual, se puede renombrar, se puede envolver y se
puede borrar.

```tcl
rename puts puts_original          ;# RENOMBRAR un comando del núcleo
proc puts {args} {                  ;# y sustituirlo por el tuyo
    puts_original "[clock format [clock seconds]]: $args"
}
```

Eso es interceptación total, en cuatro líneas y sobre el sistema en marcha. Es lo mismo que `trace` de
Lisp y `filter` de TclOO (clase 099), y se usa para depuración, registro de trazas y pruebas.

Las listas de parámetros de Tcl tienen tres formas:

```tcl
proc f {a b} { ... }               ;# obligatorios
proc f {a {b 10}} { ... }           ;# con VALOR POR DEFECTO
proc f {a args} { ... }              ;# `args` recoge el resto, por convención de nombre
```

Fíjate en `args`: **no es una palabra clave, es un nombre convenido**. Si el último parámetro se llama
exactamente `args`, recibe una lista con todo lo que sobre. Es la clase de decisión que caracteriza a
Tcl: **una convención en lugar de una regla sintáctica**.

Y hay una consecuencia de la clase 080 que aquí importa: **Tcl pasa todo por valor**, así que para
modificar una variable del llamante hay que pasar **su nombre** y usar `upvar`:

```tcl
proc incrementar {nombreVar} {
    upvar 1 $nombreVar v
    incr v
}
set contador 0
incrementar contador               ;# SIN el $
```

Esa ausencia del `$` en la llamada es la señal visible de que se pasa un nombre, no un valor, y es una
convención que hay que reconocer al leer código Tcl.

Sobre modularidad, `namespace` y `package` (clase 086) completan el cuadro, y **`namespace ensemble`**
merece una mención final: convierte un espacio de nombres en un **comando con subcomandos**, que es
como están hechos `string`, `dict` y `file`.

```tcl
namespace eval geometria {
    namespace export area perimetro
    namespace ensemble create
}
geometria area $figura            ;# se usa como los comandos del núcleo
```

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;
use List::Util qw(sum);

sub promedio {
    my @lista = @_;
    return 0 unless @lista;
    return int(sum(@lista) / scalar(@lista));
}

my $linea = <STDIN>;
chomp $linea;

print "promedio=", promedio(split ' ', $linea), "\n";
```

**Lo que esta clase enseña en Perl.** Perl tiene la lista de parámetros más peculiar de esta página:
**no hay ninguna**.

```perl
sub promedio {
    my @lista = @_;        # los argumentos llegan en @_, y hay que sacarlos
}
```

`@_` es la lista de argumentos, y **la firma no declara nada**: no hay nombres, no hay tipos, no hay
aridad y no hay comprobación. Llamar con dos argumentos una función que espera tres **no es un
error**: el tercero vale `undef`.

De ahí los idiomas universales de Perl:

```perl
my ($a, $b, $c) = @_;              # posicional
my $yo = shift;                     # el primero -- así se lee $self en un método
my %args = @_;                       # por NOMBRE, con una lista par
my ($x, %opciones) = @_;
```

El tercero —**una lista par interpretada como pares clave-valor**— es cómo Perl consigue los
argumentos con nombre sin tenerlos en el lenguaje:

```perl
crear(nombre => 'Ada', edad => 36);
```

Ese `=>` es simplemente **una coma que además entrecomilla lo de su izquierda**, así que la llamada es
una lista de cuatro elementos que la función mete en un hash. Toda la comodidad viene de una
convención, no de una característica.

Y como se vio en la clase 079, **`@_` contiene ALIAS a los argumentos del llamante**, así que
`$_[0] = 5` modifica la variable original. Es el único paso por referencia implícito de Perl, y por
eso la primera línea de casi toda subrutina copia `@_` a variables locales.

Perl 5.20 introdujo **firmas de subrutina**, estables desde 5.36:

```perl
use v5.36;
sub promedio ($primero, $segundo = 0, @resto) { ... }
```

Con nombres, valores por defecto y comprobación de aridad. Llegaron **treinta y cinco años después** de
la primera versión del lenguaje, y su adopción es lenta porque `@_` está en todo el código existente y
en toda la documentación.

Es un caso claro de lo que decía la clase 107: **el estilo lo fija el código que ya hay, no lo que el
lenguaje permita**.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <iterator>
#include <numeric>
#include <vector>

int promedio(const std::vector<int>& v) {
    if (v.empty()) return 0;
    return std::accumulate(v.begin(), v.end(), 0) / static_cast<int>(v.size());
}

int main() {
    std::vector<int> v{std::istream_iterator<int>(std::cin),
                       std::istream_iterator<int>()};

    std::cout << "promedio=" << promedio(v) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** `const std::vector<int>&` en la firma es la decisión más
importante del programa, y condensa lo que C++ pide entender en esta clase:

```cpp
void f(std::vector<int> v);          // por VALOR: copia el vector entero
void f(std::vector<int>& v);          // por referencia: puede modificarlo
void f(const std::vector<int>& v);    // por referencia CONSTANTE: sin copia, sin modificar
void f(std::vector<int>&& v);          // por referencia de VALOR-R: para mover (clase 081)
void f(std::span<int> v);               // C++20: vista, sin propiedad
```

**Cinco formas de recibir lo mismo**, cada una con distinto coste y distinto contrato. Ningún otro
lenguaje de esta página obliga a decidir tanto, y esa es a la vez la fuerza y la carga de C++.

La regla práctica que usan las guías modernas: **`const&` para leer, valor para tipos pequeños o
cuando vayas a quedarte una copia, `&&` para transferir, `span`/`string_view` para vistas**.

C++ añade además la **sobrecarga**, que Ada tiene y casi ningún lenguaje dinámico:

```cpp
int  promedio(const std::vector<int>&);
double promedio(const std::vector<double>&);
```

Dos funciones con el mismo nombre y distinta firma. El compilador elige por los tipos de los
argumentos, en compilación — despacho estático, coste cero. Y con plantillas, una sola definición
sirve para todos los tipos:

```cpp
template <typename T>
T promedio(const std::vector<T>& v) { ... }
```

Esa es la programación genérica de la clase 078, y en C++ **sustituye a la sobrecarga en la mayoría de
los casos**.

Y hay una carencia que conviene decir porque contrasta con Ada, Lisp y Python: **C++ no tiene
argumentos con nombre**. `f(true, false, true)` en el sitio de la llamada no dice nada, y la propuesta
de añadirlos lleva años discutiéndose. El apaño idiomático es pasar una `struct` de opciones con
inicializadores designados (clase 091):

```cpp
struct Opciones { bool recursivo = false; bool seguir_enlaces = false; };
copiar(origen, destino, {.recursivo = true});
```

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
ctl-opt dftactgrp(*no) actgrp(*caller) main(Principal);

dcl-proc Principal;
  dcl-pi *n;
    entrada char(200) const;
  end-pi;

  dcl-s texto varchar(200);
  dcl-s tok   varchar(20) inz('');
  dcl-s c     char(1);
  dcl-s i     int(10);
  dcl-s v     int(10) dim(100);
  dcl-s n     int(10) inz(0);

  texto = %trimr(entrada);

  for i = 1 to %len(texto) + 1;
    if i <= %len(texto);
      c = %subst(texto : i : 1);
    else;
      c = ' ';
    endif;
    if c = ' ';
      if tok <> '';
        n += 1;
        v(n) = %int(tok);
        tok = '';
      endif;
    else;
      tok += c;
    endif;
  endfor;

  dsply ('promedio=' + %char(promedio(v : n)));
end-proc;

dcl-proc promedio;
  dcl-pi *n int(20);
    x int(10) dim(100) const;
    cuantos int(10) const;
  end-pi;

  dcl-s i int(10);
  dcl-s s int(20) inz(0);

  if cuantos = 0;
    return 0;
  endif;
  for i = 1 to cuantos;
    s += x(i);
  endfor;
  return s / cuantos;
end-proc;
```

**Lo que esta clase enseña en RPG.** Este programa muestra la transformación más importante de la
historia del lenguaje: **RPG no tuvo procedimientos con parámetros hasta 1994**.

Antes de ILE, RPG tenía **subrutinas** con `BEGSR` y `ENDSR`, y eran exactamente el párrafo de COBOL:
sin parámetros, sin valor de retorno y sin variables locales, operando sobre los campos globales del
programa.

```text
C     CALCULO       BEGSR
C                   EVAL      TOTAL = SUMA / CUENTA
C                   ENDSR
```

Todo era global. Un programa RPG clásico de tres mil líneas tenía un solo espacio de nombres con
cientos de campos, y saber qué escribía cada subrutina era trabajo de arqueología.

**ILE lo cambió por completo en 1994**, y merece ver todo lo que llegó de golpe:

```rpgle
dcl-proc promedio;
  dcl-pi *n int(20);           // el PROTOTIPO: tipos y valor de retorno
    x int(10) dim(100) const;   // parámetro CONSTANTE
    cuantos int(10) const;
  end-pi;
  dcl-s s int(20);              // variable LOCAL, automática
  return s / cuantos;            // valor de retorno
end-proc;
```

- **Procedimientos con parámetros tipados** y prototipo comprobado por el compilador.
- **Valor de retorno** con `return`.
- **Variables locales automáticas**, lo que habilita la **recursión**.
- **`const`**, `value` y `options(*nopass : *omit)` como modos de paso.
- **Exportables o privados** al módulo (clase 087).

`options(*nopass)` merece mención: declara que **un parámetro se puede omitir en la llamada**, y
`%parms()` dice cuántos llegaron. Es la forma de RPG de tener parámetros opcionales, y es una de las
razones por las que las APIs del sistema, escritas hace décadas, siguen siendo compatibles: **se
añaden parámetros al final con `*nopass` y los programas antiguos no se enteran**.

Esa preocupación por la compatibilidad hacia atrás —visible en el prototipo, en la firma de los
programas de servicio (clase 086) y aquí— es la seña de identidad de la plataforma.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 prom: procedure options(main);

    declare linea char(200) varying;
    declare tok   char(20)  varying initial('');
    declare c     char(1);
    declare v(100) fixed binary(31);
    declare (i, n) fixed binary(31);

    get edit (linea) (a(200));
    linea = trim(linea);
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

    put skip list ('promedio=' || trim(char(promedio(n))));

 promedio: procedure (cuantos) returns (fixed binary(31));
    declare cuantos fixed binary(31);
    declare (j, s) fixed binary(31);
    if cuantos = 0 then return (0);
    s = 0;
    do j = 1 to cuantos;
       s = s + v(j);          /* ve `v` por ANIDAMIENTO LÉXICO */
    end;
    return (s / cuantos);
 end promedio;

 end prom;
```

**Lo que esta clase enseña en PL/I.** El `promedio` de este programa **no recibe el arreglo**: lo ve
por **anidamiento léxico** (clase 083). Está declarado dentro de `prom`, así que `v` está en su
ámbito.

Esa capacidad —**procedimientos anidados con ámbito léxico completo**— la tenía PL/I en 1964, tomada
de Algol 60, y es de las cosas que C no tiene ni ha tenido nunca. En C todo procedimiento está al
nivel superior, y por eso el estado compartido va en variables globales o en estructuras pasadas a
mano.

PL/I ofrece además el juego de modos de parámetro más completo de su época:

```pli
 sub: procedure (x);                   /* por REFERENCIA: el defecto */
 call sub((x));                         /* los paréntesis fuerzan una COPIA (clase 102) */
 declare x fixed binary(31) byvalue;    /* por valor, en PL/I moderno */
```

Y tres capacidades que conviene conocer:

**Procedimientos recursivos**, declarados explícitamente (clase 097):

```pli
 factorial: procedure (n) returns (fixed decimal(15)) recursive;
```

**Entradas múltiples** con `entry`, que da a un mismo procedimiento **varios puntos de entrada** con
firmas distintas:

```pli
 abrir: procedure (nombre);
    ...
 cerrar: entry;                  /* OTRA entrada al MISMO procedimiento */
    ...
 end abrir;
```

Comparten las variables locales, así que es una forma primitiva de módulo con estado — el mismo
patrón que los `ENTRY` de Fortran, que se declararon obsoletos en Fortran 2008 precisamente por lo
confusos que resultan.

**Y `generic`**, que es sobrecarga:

```pli
 declare calcular generic (calc_fijo when (fixed), calc_flot when (float));
```

Un nombre que despacha a un procedimiento u otro **según el tipo del argumento**, resuelto en
compilación. Es la sobrecarga de Ada y C++, en un lenguaje de 1964, y una muestra más de por qué PL/I
aparece constantemente en las historias del diseño de lenguajes pese a su declive comercial.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
PROM ; Procedimental y modular -- clase 109
 read linea
 write "promedio=", $$promedio(linea), !
 quit
 ;
promedio(txt) ; devuelve el promedio entero de una linea de numeros
 new i, n, s
 set n = $length(txt, " ")
 quit:n=0 0
 set s = 0
 for i=1:1:n set s = s + $piece(txt, " ", i)
 quit s \ n
```

**Lo que esta clase enseña en M.** M sí tiene procedimientos con parámetros y valor de retorno, y su
sintaxis es de una concisión notable:

```mumps
promedio(txt) ;                  ; una ETIQUETA con lista de parámetros
 quit s \ n                       ; QUIT con valor = return
```

Se invocan de dos formas, y la distinción es la del gancho de esta clase:

```mumps
 do procesar^RUTINA(x)           ; PROCEDIMIENTO: no devuelve nada
 set y = $$calcular^RUTINA(x)     ; FUNCIÓN: los DOS dólares indican valor de retorno
```

**`$$`** es la marca sintáctica de "esto devuelve algo", y es la única forma de distinguirlo — no hay
declaración de tipo de retorno.

Y aquí aparece la carencia central de M, que ya se vio en las clases 082 y 087: **los parámetros son
por referencia si se pasan con un punto delante, y las variables locales son GLOBALES al proceso salvo
que se declaren con `new`**.

```mumps
 do sub(x)          ; por VALOR
 do sub(.x)         ; por REFERENCIA -- el punto es toda la diferencia
```

Sin ese punto, se copia; con él, la rutina puede modificar la variable del llamante. Un carácter.

Y **`new i, n, s`** en el cuerpo de `promedio` es obligatorio, no opcional: sin él, esas tres
variables pisarían las del llamante y las de cualquier rutina de la pila. Es el mecanismo de la clase
096 —una pila de valores— y en un sistema de un millón de líneas es lo único que hace viable componer
rutinas.

Olvidar un `new` es el error clásico de M, y produce fallos a distancia: una rutina profunda machaca
la variable `i` de un bucle que está tres niveles más arriba. No hay compilador que lo detecte.

Sobre modularidad, la unidad es la rutina y no hay espacios de nombres (clase 086): el prefijo
administrado por humanos es todo lo que hay. Es la parte del lenguaje que peor ha envejecido, y la que
las implementaciones modernas —IRIS con clases y paquetes— han sustituido por completo.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| numeros |

numeros := stdin nextLine substrings collect: [ :cada | cada asNumber ].

Transcript
    show: 'promedio=', (numeros isEmpty
        ifTrue: [ 0 ]
        ifFalse: [ (numeros inject: 0 into: [ :a :b | a + b ]) // numeros size ]) printString;
    cr.
```

**Lo que esta clase enseña en Smalltalk.** En Smalltalk **no hay procedimientos ni funciones sueltas**:
hay **métodos**, y un método pertenece siempre a una clase. No se puede escribir una función global.

Esa restricción es deliberada y tiene una consecuencia de diseño: **para escribir `promedio`, hay que
decidir de quién es**. Y la respuesta idiomática sorprende a quien viene de fuera: **se añade a la
clase `Collection`**.

```smalltalk
Collection >> promedio
    self isEmpty ifTrue: [ ^0 ].
    ^(self inject: 0 into: [ :a :b | a + b ]) // self size
```

A partir de ese momento, **cualquier colección del sistema responde a `promedio`**: arreglos,
conjuntos, listas ordenadas, intervalos. Incluidas las que ya existían antes de escribirlo.

Eso son las **extensiones de clase**, y son una de las capacidades más potentes y más discutidas de
Smalltalk: **puedes añadir métodos a clases que no son tuyas**, incluidas las del sistema.

```smalltalk
Integer >> factorial          "añadir un método a Integer"
String >> esPalindromo         "y a String"
```

Ruby lo copió con el nombre de *monkey patching*, Objective-C con las categorías, C# con los métodos
de extensión, Kotlin y Swift con las suyas.

Y tiene el problema que cabe esperar y que la comunidad conoce bien: **si dos paquetes añaden el mismo
método a la misma clase, uno pisa al otro** — sin espacios de nombres que los separen (clase 086), no
hay defensa. Pharo lo mitiga marcando las extensiones con el nombre del paquete que las aporta, de
modo que las herramientas puedan avisar.

Sobre los parámetros, la sintaxis de mensajes con palabras clave hace algo que esta clase valora:
**la llamada documenta sus argumentos**.

```smalltalk
coleccion copyFrom: 2 to: 5
ventana abrirEn: punto conTitulo: 'Hola' modal: true
```

No hace falta la característica "argumentos con nombre" que Ada, Lisp y Python tienen: **en Smalltalk
el nombre del mensaje ES la lista de nombres de los parámetros**, y no puede omitirse.

---

## Y de vuelta a la clase

Lo transferible: **un procedimiento no se extrae para no repetir código, se extrae para poder darle un
nombre**. Repetir tres líneas cuesta poco; no poder decir qué hacen esas tres líneas cuesta cada vez
que alguien las lee. Por eso una función de una línea con buen nombre suele valer la pena, y por eso
la métrica útil no es cuántas veces se llama sino **si el nombre ahorra leer el cuerpo**. Los
lenguajes de esta página lo aprendieron por la vía dura: sus programas de diez mil líneas sin
descomponer siguen ahí.

⏮️ [Volver a la clase 109](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
