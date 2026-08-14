# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 085

> [⬅️ Volver a la clase 085](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Dos operaciones guardadas **en variables** y aplicadas después. Que una función se pueda meter en una
variable, en una lista o en una tabla parece básico, y de estos doce lenguajes **solo cinco lo hacen
del todo**. Los demás ofrecen algo más limitado: **elegir entre funciones que ya existen**, que no es
lo mismo que tratarlas como valores.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto son las **funciones como valores**, y estos lenguajes lo enseñan porque muestran la
> escala completa. **Primera clase de verdad**: Lisp, Smalltalk, Perl, C++ y Tcl, donde una función se
> crea, se guarda, se pasa y se devuelve. **Puntero a función con firma comprobada**: Fortran 2003, Ada
> 95, Pascal y PL/I — se puede seleccionar y pasar, no fabricar. Y **selección por nombre en una
> cadena**: COBOL con `CALL` dinámico, RPG con `%paddr`, M con indirección.
>
> Ese tercer nivel es más antiguo y más peligroso: **el destino se decide con texto**, así que ninguna
> herramienta puede analizar qué se ejecuta.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a b` (dos enteros) → stdout: `suma=<a+b> producto=<a*b>`
- **Regla:** `aplicar(f, a, b) = f(a, b); con f = suma y f = producto`

| stdin | esperado |
|---|---|
| `3 4` | `suma=7 producto=12` |
| `5 5` | `suma=10 producto=25` |
| `0 9` | `suma=9 producto=0` |

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
PROGRAM-ID. PRIMERA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA      PIC X(80).
01  TXT-A      PIC X(20).
01  TXT-B      PIC X(20).
01  A          PIC S9(9)  COMP-3.
01  B          PIC S9(9)  COMP-3.
01  R          PIC S9(18) COMP-3.
01  OPERACION  PIC X(10).
01  ED-S       PIC -(17)9.
01  ED-P       PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    MOVE "SUMA" TO OPERACION
    PERFORM APLICAR
    MOVE R TO ED-S

    MOVE "PRODUCTO" TO OPERACION
    PERFORM APLICAR
    MOVE R TO ED-P

    DISPLAY "suma=" FUNCTION TRIM(ED-S)
            " producto=" FUNCTION TRIM(ED-P)
    STOP RUN.

APLICAR.
    EVALUATE OPERACION
        WHEN "SUMA"      COMPUTE R = A + B
        WHEN "PRODUCTO"  COMPUTE R = A * B
        WHEN OTHER       MOVE 0 TO R
    END-EVALUATE.
```

**Lo que esta clase enseña en COBOL.** **COBOL no tiene funciones como valores**, y lo que hace este
programa es lo que hace COBOL en su lugar: **guardar el NOMBRE de la operación en una variable** y
decidir con un `EVALUATE`.

Es una tabla de despacho hecha a mano, y funciona hasta que hay veinte operaciones y el `EVALUATE`
ocupa una pantalla.

Lo que sí tiene COBOL, y es genuinamente potente, es la **llamada dinámica**:

```cobol
01  NOMBRE-PROGRAMA  PIC X(8).
...
MOVE "CALCIVA" TO NOMBRE-PROGRAMA
CALL NOMBRE-PROGRAMA USING IMPORTE, RESULTADO
    ON EXCEPTION DISPLAY "no existe " NOMBRE-PROGRAMA
END-CALL
```

`CALL` con una **variable** en lugar de un literal resuelve el programa **en tiempo de ejecución**,
buscándolo por nombre en la biblioteca de carga. Con eso se construyen las tablas de despacho reales
de los sistemas transaccionales: una tabla en base de datos que asigna un código de operación a un
nombre de programa, y un solo `CALL` dinámico que ejecuta cualquiera.

Es enormemente flexible y tiene el coste que cabe esperar: **el nombre es una cadena, así que nadie
comprueba que el programa exista ni que su firma coincida** hasta que se ejecuta. De ahí la cláusula
`ON EXCEPTION`, que es obligatoria en código serio.

Y hay un matiz de rendimiento que importa en producción: `CALL` dinámico **resuelve en cada llamada**
salvo que se declare `CANCEL`/`INITIAL` con cuidado, así que en un bucle caliente se prefiere el
`CALL` literal, que se enlaza al compilar.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program primera
   implicit none

   abstract interface
      pure function binaria(x, y) result(r)
         integer, intent(in) :: x, y
         integer :: r
      end function binaria
   end interface

   procedure(binaria), pointer :: f, g
   integer :: a, b

   read(*, *) a, b

   f => suma          ! un PUNTERO A PROCEDIMIENTO
   g => producto

   write(*, '(A,I0,A,I0)') 'suma=', f(a, b), ' producto=', g(a, b)

contains

   pure function suma(x, y) result(r)
      integer, intent(in) :: x, y
      integer :: r
      r = x + y
   end function suma

   pure function producto(x, y) result(r)
      integer, intent(in) :: x, y
      integer :: r
      r = x * y
   end function producto

end program primera
```

**Lo que esta clase enseña en Fortran.** Los **punteros a procedimiento** llegaron con **Fortran
2003**, y su declaración exige algo que ningún lenguaje dinámico pide: **una interfaz abstracta**.

```fortran
abstract interface
   pure function binaria(x, y) result(r)
      integer, intent(in) :: x, y
      integer :: r
   end function
end interface

procedure(binaria), pointer :: f
```

`abstract interface` declara **la firma completa** —tipos, modos, pureza— y `procedure(binaria)` es un
puntero que solo puede apuntar a algo que la cumpla. **El compilador lo comprueba en la asignación**,
no en la llamada.

Compara con un puntero a función de C, donde una conversión mal hecha compila y revienta en ejecución.
Aquí, `f => otra_cosa` con firma distinta **no compila**.

Y fíjate en que la interfaz incluye **`pure`**: un puntero declarado sobre una interfaz pura solo
acepta procedimientos puros, lo que preserva la garantía de la clase 084 a través de la indirección.
Es un detalle notable — la pureza sobrevive al puntero.

Lo que Fortran **no** tiene son clausuras (clase 083), así que un puntero a un procedimiento interno
solo es válido mientras el anfitrión esté activo.

Y `procedure(interfaz)` sirve también para declarar **parámetros** que son procedimientos, que es como
se pasan las funciones objetivo a los algoritmos de integración y optimización de las bibliotecas
numéricas.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Primera is

   type Binaria is access function (X, Y : Integer) return Integer;

   function Suma     (X, Y : Integer) return Integer is (X + Y);
   function Producto (X, Y : Integer) return Integer is (X * Y);

   F : constant Binaria := Suma'Access;
   G : constant Binaria := Producto'Access;

   A, B : Integer;
begin
   Get (A);
   Get (B);

   Put ("suma=");       Put (F (A, B), Width => 1);
   Put (" producto=");  Put (G (A, B), Width => 1);
   New_Line;
end Primera;
```

**Lo que esta clase enseña en Ada.** `access function (X, Y : Integer) return Integer` es un **tipo de
acceso a subprograma**, y es un tipo de verdad: se puede declarar, poner en un array, pasar como
parámetro y comparar.

Ada 95 lo introdujo, y con dos comprobaciones que lo distinguen de un puntero a función de C:

1. **La firma forma parte del tipo.** Asignar un subprograma con otra firma no compila.
2. **La comprobación de accesibilidad** de la clase 083: no se puede guardar en una variable de vida
   más larga que el subprograma apuntado.

Fíjate también en la sintaxis `is (X + Y)`: son **funciones de expresión** (Ada 2012), cuerpos de una
sola expresión sin `begin`/`end`. Además de ser breves, el compilador puede usarlas en contratos y
demostrarlas con SPARK.

Ada tiene además un mecanismo relacionado que se usa más que los punteros: el **despacho dinámico**
sobre tipos etiquetados.

```ada
type Operacion is tagged null record;
function Aplicar (Op : Operacion; X, Y : Integer) return Integer is abstract;

type Suma_Op is new Operacion with null record;
overriding function Aplicar (Op : Suma_Op; X, Y : Integer) return Integer is (X + Y);
```

Eso es un objeto función, y en Ada se prefiere a los punteros porque **conserva las comprobaciones de
tipo** y permite añadir estado. Es la misma elección que en C++ entre un puntero a función y un
functor.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Primera;
{$MODE OBJFPC}{$H+}
uses SysUtils;

type
  TBinaria = function(X, Y: Integer): Integer;   { un TIPO procedimental }

function Suma(X, Y: Integer): Integer;
begin
  Result := X + Y;
end;

function Producto(X, Y: Integer): Integer;
begin
  Result := X * Y;
end;

var
  F, G: TBinaria;
  A, B: Integer;

begin
  Read(A, B);

  F := @Suma;
  G := @Producto;

  WriteLn('suma=', IntToStr(F(A, B)), ' producto=', IntToStr(G(A, B)));
end.
```

**Lo que esta clase enseña en Pascal.** Los **tipos procedimentales** —`type T = function(...)`— están
en Pascal desde Turbo Pascal 5.5 (1989) y en el ISO Extended Pascal. Una variable de ese tipo guarda
una función y se llama como tal.

El `@` de `F := @Suma` es el **operador de dirección**, y en modo ObjFPC es obligatorio; en modo
Delphi se puede omitir. Esa diferencia entre modos es una de las incompatibilidades molestas del
ecosistema, y viene de una ambigüedad real: sin `@`, `F := Suma` podría significar "asigna la función"
o "llámala y asigna su resultado".

Object Pascal tiene **tres** tipos de valor invocable, y la diferencia importa:

```pascal
type
  TSimple   = function(X: Integer): Integer;                    { función suelta }
  TMetodo   = function(X: Integer): Integer of object;          { MÉTODO: guarda también el objeto }
  TAnonima  = reference to function(X: Integer): Integer;       { CLAUSURA (clase 083) }
```

**`of object`** es la clave del modelo de eventos de Delphi: guarda **dos** punteros —el método y la
instancia—, así que `Boton.OnClick := Formulario.BotonClick;` recuerda a qué formulario pertenece. Es
lo que en C# se llama *delegate* y en C++ exige `std::bind` o una lambda con captura.

Ese tipo `of object` es, probablemente, la aportación de Delphi que más se copió: todo el modelo de
eventos de .NET viene de ahí, con el mismo autor detrás (clase 073).

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((a (read))
       (b (read))
       (f #'+)                 ; la función + COMO VALOR
       (g #'*))
  (format t "suma=~D producto=~D~%" (funcall f a b) (funcall g a b)))
```

**Lo que esta clase enseña en Common Lisp.** `#'+` obtiene **el objeto función** asociado al símbolo
`+`. No es una cadena ni un nombre: es el objeto, y se puede guardar, comparar e invocar.

`#'` es la abreviatura de `(function +)`, y `funcall` es lo que llama a una función guardada en una
variable. Los dos hacen falta porque Common Lisp es un **Lisp-2** (clase 068): tiene espacios de
nombres separados para funciones y variables, así que `(f a b)` busca `f` **como función** y `(funcall
f a b)` busca `f` **como variable**.

En Scheme, que es Lisp-1, `#'` y `funcall` no existen: `(f a b)` funciona directamente. Es la
diferencia de diseño más antigua entre los dos dialectos.

Y una **tabla de despacho** en Lisp es una estructura de datos normal:

```lisp
(defparameter *ops*
  (list (cons "suma" #'+) (cons "producto" #'*) (cons "resta" #'-)))

(funcall (cdr (assoc entrada *ops* :test #'string=)) a b)
```

Una lista de asociaciones de cadena a función, construida en ejecución, ampliable desde otro fichero.
Es el `switch` de la clase 061 convertido en dato.

Y como las funciones son objetos, se pueden **inspeccionar y redefinir en caliente**:

```lisp
(function-lambda-expression #'suma)   ; el código fuente, si se conservó
(setf (symbol-function 'suma) #'*)     ; redefinir sobre la marcha
(trace suma)                            ; instrumentar sin tocar el código
```

`trace` es un ejemplo perfecto: envuelve la función para registrar cada llamada, y funciona sobre
cualquier función del sistema. Es lo mismo que `rename` en Tcl y `memoize` en Perl.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [split [string trim $linea]] a b

#  Los operadores están disponibles COMO COMANDOS desde Tcl 8.5.
set f ::tcl::mathop::+
set g ::tcl::mathop::*

puts "suma=[$f $a $b] producto=[$g $a $b]"
```

**Lo que esta clase enseña en Tcl.** En Tcl, **una "función como valor" es el NOMBRE de un comando
guardado en una variable**. `set f ::tcl::mathop::+` guarda una cadena; `[$f $a $b]` la usa como
primera palabra de un comando.

Que eso funcione es consecuencia directa de la regla básica del lenguaje: **la primera palabra de un
comando es su nombre, y viene de la sustitución como cualquier otra**.

Y `::tcl::mathop::+` merece atención: Tcl 8.5 expuso **todos los operadores aritméticos como
comandos**, precisamente para que se pudieran pasar como valores.

```tcl
::tcl::mathop::+ 1 2 3        ;# 6 -- acepta varios argumentos
::tcl::mathop::* {*}$lista    ;# el producto de una lista entera
```

Como en Tcl no hay operadores (clase 055), exponerlos como comandos no es una excepción: es lo
coherente.

Un "valor invocable" en Tcl puede ser tres cosas, y todas son listas:

```tcl
set f puts                                    ;# el nombre de un comando
set f [list apply {{x} {expr {$x * 2}}}]      ;# una lambda con apply (clase 083)
set f [list miObjeto metodo]                  ;# un método de un objeto TclOO
{*}$f $arg                                     ;# se invocan todas igual
```

Ese **prefijo de comando** —una lista cuyo primer elemento es un comando y el resto argumentos ya
fijados— es el idioma universal de Tcl para las retrollamadas, y es aplicación parcial hecha con
datos.

La contrapartida es la de siempre: **si el comando no existe, el error aparece al invocarlo**.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($x, $y) = split ' ', $linea;

my $f = sub { return $_[0] + $_[1] };     # referencia a subrutina
my $g = sub { return $_[0] * $_[1] };

printf "suma=%d producto=%d\n", $f->($x, $y), $g->($x, $y);
```

**Lo que esta clase enseña en Perl.** Una **referencia a subrutina** —`sub { ... }` sin nombre, o
`\&nombre` para una que ya existe— es un valor escalar como cualquier otro, y se invoca con `->()`.

```perl
my $f = sub { ... };        # anónima
my $g = \&suma;             # referencia a una con nombre
$f->(1, 2);
&$f(1, 2);                   # sintaxis antigua, todavía se ve
```

Y con eso, la **tabla de despacho** es un hash:

```perl
my %ops = (
    suma     => sub { $_[0] + $_[1] },
    producto => sub { $_[0] * $_[1] },
);
$ops{$operacion}->($a, $b);
```

Ese patrón sustituye al `switch` que Perl nunca tuvo (clase 061), y es la razón de que su ausencia no
se echara de menos: **un hash de referencias es más flexible que cualquier `switch`**, porque se
construye en ejecución y se puede ampliar desde un módulo externo.

Perl tiene además la **tabla de símbolos accesible**, lo que permite manipular funciones por nombre:

```perl
no strict 'refs';
*{"main::doblar"} = sub { $_[0] * 2 };     # DEFINIR una función en ejecución
my $f = \&{"main::$nombre"};                # obtenerla por su nombre
defined &{"main::$nombre"};                  # ¿existe?
```

Esa manipulación de *globs* es la base de los generadores de accesores, de los objetos dinámicos y de
media biblioteca de CPAN. Es potente, es peligrosa, y exige `no strict 'refs'` — que es la forma que
tiene Perl de decir "sé lo que hago".

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <functional>
#include <iostream>

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    const std::function<int(int, int)> f = [](int x, int y) { return x + y; };
    const std::function<int(int, int)> g = [](int x, int y) { return x * y; };

    std::cout << "suma=" << f(a, b)
              << " producto=" << g(a, b) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ tiene **cuatro cosas invocables** distintas, y elegir entre
ellas es una decisión de rendimiento:

```cpp
int (*p)(int, int) = &suma;                    // puntero a función: sin estado
auto lam = [k](int x) { return x + k; };       // lambda: tipo ÚNICO, con captura
struct F { int operator()(int) const; };       // functor: un objeto con ()
std::function<int(int)> f = lam;               // envoltura genérica: BORRA el tipo
```

`std::function` es la que parece más cómoda y **la que hay que evitar cuando importa el
rendimiento**: borra el tipo, lo que implica **una llamada indirecta** y, si la lambda captura
demasiado, **una reserva de memoria dinámica**. No se puede integrar en línea.

La alternativa moderna es `auto` para guardar la lambda con su tipo concreto, y **plantillas** para
recibirla:

```cpp
template <typename F>
int aplicar(F f, int a, int b) { return f(a, b); }   // se INTEGRA en línea, coste cero
```

Esa es la diferencia entre el diseño de la STL —plantillas, coste cero— y `std::function`, que existe
para cuando el tipo tiene que ser uniforme: guardar retrollamadas heterogéneas en un contenedor, o
cruzar una frontera de biblioteca.

C++23 añadió `std::function_ref` y `std::move_only_function` para cubrir los casos intermedios: una
vista no propietaria y una versión que acepta lambdas que solo se pueden mover.

Y hay una guía práctica: **plantilla si la función es un parámetro, `std::function` si hay que
guardarla**.

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

dcl-pi PRIMERA;
  a int(10) const;
  b int(10) const;
end-pi;

dcl-s operacion char(10);
dcl-s salida    char(60);
dcl-s s         int(20);
dcl-s p         int(20);

operacion = 'SUMA';
s = aplicar(operacion : a : b);
operacion = 'PRODUCTO';
p = aplicar(operacion : a : b);

salida = 'suma=' + %char(s) + ' producto=' + %char(p);
dsply salida;

*inlr = *on;
return;

dcl-proc aplicar;
  dcl-pi *n int(20);
    op char(10) const;
    x  int(10) const;
    y  int(10) const;
  end-pi;

  select;
    when %trim(op) = 'SUMA';     return x + y;
    when %trim(op) = 'PRODUCTO'; return x * y;
    other;                       return 0;
  endsl;
end-proc;
```

**Lo que esta clase enseña en RPG.** RPG **no tiene funciones de primera clase**, y este programa hace
lo mismo que COBOL: guarda el **nombre de la operación** y decide con un `select`.

Lo que sí tiene es el equivalente exacto de un puntero a función de C, con `%paddr`:

```rpgle
dcl-pr calcular int(20) extproc(punteroOp);
  x int(10) const;
  y int(10) const;
end-pr;

dcl-s punteroOp pointer;

punteroOp = %paddr('SUMA');       // la DIRECCIÓN de un procedimiento, por NOMBRE
resultado = calcular(a : b);       // llamada indirecta
```

`%paddr` acepta el nombre como **literal o como variable**, así que se puede construir una tabla de
punteros y despachar dinámicamente. `extproc(puntero)` en el prototipo es lo que declara que la
llamada es indirecta.

Y tiene el mismo problema que el `CALL` dinámico de COBOL: **el nombre es una cadena y la firma no se
comprueba**. Si el procedimiento apuntado tiene otra firma, el resultado es corrupción de memoria.

En la práctica, `%paddr` se usa casi solo para dos cosas: **registrar manejadores en APIs del
sistema** —un manejador de excepciones, una salida de usuario— y **llamar a código C**. Para la
lógica de negocio, la tabla de despacho de este programa, o un módulo de servicio por operación.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 primera: procedure options(main);

    declare (a, b) fixed binary(31);
    declare f entry (fixed binary(31), fixed binary(31))
                    returns (fixed binary(31)) variable;

    get list (a, b);

    f = suma;          /* una VARIABLE de tipo ENTRY */
    put skip list ('suma=' || trim(char(f(a, b))));

    f = producto;
    put skip list (' producto=' || trim(char(f(a, b))));

 suma: procedure (x, y) returns (fixed binary(31));
    declare (x, y) fixed binary(31);
    return (x + y);
 end suma;

 producto: procedure (x, y) returns (fixed binary(31));
    declare (x, y) fixed binary(31);
    return (x * y);
 end producto;

 end primera;
```

**Lo que esta clase enseña en PL/I.** El atributo **`entry ... variable`** declara una **variable que
contiene un procedimiento**, con su firma completa. PL/I lo tenía en **1964**, antes que Pascal,
Fortran y Ada.

```pli
declare f entry (fixed binary(31)) returns (fixed binary(31)) variable;
f = mi_procedimiento;
resultado = f(10);
```

Sin `variable`, `entry` declara un prototipo —"existe un procedimiento con esta firma"—. Con
`variable`, declara un lugar donde guardar uno. Es la misma distinción que en C entre declarar
`int f(int);` y `int (*f)(int);`.

Y PL/I tiene además las **variables de etiqueta** de la clase 070, que guardan un punto del programa
en lugar de un procedimiento:

```pli
declare destino label;
destino = fin;
go to destino;         /* salto indirecto */
```

Entre las dos, PL/I permite guardar en variables **tanto qué se llama como a dónde se salta**. Es una
capacidad que no tiene ningún lenguaje del núcleo, y explica por qué el código PL/I de los 70 podía
ser tan difícil de seguir: **el flujo de control se decide con datos**.

Lo que falta, como en Fortran y Ada, son las clausuras: una `entry variable` guarda el procedimiento,
no su entorno. Si apunta a un procedimiento anidado cuyo anfitrión ya terminó, el resultado es
indefinido — y PL/I no lo comprueba.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
PRIMERA ; Funciones como valores -- clase 085
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 set op = "suma"
 set s = @("$$" _ op _ "(a,b)")        ; INDIRECCIÓN: construye la llamada
 set op = "producto"
 set p = @("$$" _ op _ "(a,b)")
 write "suma=", s, " producto=", p, !
 quit
 ;
suma(x, y) ;
 quit x + y
 ;
producto(x, y) ;
 quit x * y
```

**Lo que esta clase enseña en M.** M **no tiene funciones como valores**, y lo que tiene es más
radical: **la indirección**, que permite construir la llamada **como una cadena de texto** y
ejecutarla.

```mumps
 set nombre = "suma"
 set r = @("$$" _ nombre _ "(a,b)")
```

`@` toma la cadena `"$$suma(a,b)"` y **la evalúa como código**. No hay puntero, no hay tipo y no hay
firma: hay texto que se interpreta.

Es el mecanismo más flexible de esta página y el menos analizable. Con él se puede:

```mumps
 do @rutina                          ; llamar a una rutina por nombre
 set @variable = valor               ; asignar a una variable por nombre
 set @("^DATOS(" _ id _ ")") = x     ; construir la referencia al global
 goto @etiqueta                      ; saltar a una etiqueta por nombre
```

La cuarta forma es el `GO TO` asignado de FORTRAN que Dijkstra denunció y que el estándar de Fortran
eliminó en 1995. En M sigue disponible y se usa.

Y la consecuencia práctica es la que ya se apuntó en las clases 068 y 083: **ninguna herramienta puede
analizar estáticamente un programa M**. No se puede saber qué rutinas llama, qué variables toca ni qué
globales escribe, porque todo puede decidirse en ejecución construyendo cadenas.

Es la misma capacidad —y el mismo problema— que `eval` en JavaScript, con la diferencia de que aquí no
es un recurso excepcional: **es el idioma normal para el despacho dinámico**.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| partes a b f g |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

f := [ :x :y | x + y ].       "un bloque: valor de primera clase"
g := [ :x :y | x * y ].

Transcript
    show: 'suma=', (f value: a value: b) printString;
    show: ' producto=', (g value: a value: b) printString;
    cr.
```

**Lo que esta clase enseña en Smalltalk.** Un **bloque es un objeto**, instancia de `BlockClosure`, y
por tanto un valor de primera clase completo: se guarda, se pasa, se devuelve y se mete en
colecciones.

Se invoca con `value`, `value:`, `value:value:` y `valueWithArguments:` — **el número de argumentos
está en el selector**, coherente con la clase 073.

Y Smalltalk tiene una segunda forma de "función como valor" que no tiene ningún otro lenguaje de esta
página: **el símbolo como mensaje**.

```smalltalk
#(3 1 2) collect: [ :x | x squared ]     "con un bloque"
#(3 1 2) collect: #squared                "con un SÍMBOLO: el nombre del mensaje"
coleccion do: [ :x | x imprimir ]
receptor perform: #suma:con: with: 1 with: 2
```

`#squared` es un símbolo, y muchas operaciones aceptan uno donde esperan un bloque, enviándolo como
mensaje a cada elemento. Es más corto y más rápido que crear un bloque, y es lo que en otros lenguajes
se llama *referencia a método*.

`perform:` es la forma general: **envía un mensaje cuyo nombre se decide en ejecución**. Es lo mismo
que la indirección de M, con una diferencia importante: **el símbolo es un objeto internado, no una
cadena arbitraria**, y el sistema puede responder si alguien lo implementa.

Con `perform:withArguments:` y `doesNotUnderstand:` (clase 051) se construyen proxies, objetos
remotos y envoltorios dinámicos — toda la reflexión del lenguaje, con dos mensajes.

---

## Y de vuelta a la clase

Lo transferible: **una tabla de despacho es la estructura que sustituye a un `switch` cuando las
opciones crecen**, y todos estos lenguajes la construyen, con o sin funciones de primera clase. En
Lisp es una lista de asociaciones; en Perl, un hash de referencias; en C++, un `map` de
`std::function`; en COBOL, una tabla de nombres de programa; en M, un array de nombres de rutina. La
diferencia no está en si se puede, sino en **si alguien comprueba que el nombre existe y que la firma
encaja**.

⏮️ [Volver a la clase 085](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
