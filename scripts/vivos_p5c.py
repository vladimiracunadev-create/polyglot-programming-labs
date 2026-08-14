# -*- coding: utf-8 -*-
"""Parte 5, lote C — clases 085 a 088. Ver `vivos_parte5.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 085 — Funciones de primera clase y como valores
# ---------------------------------------------------------------------------
SPECS["085"] = dict(
    gancho="""
Dos operaciones guardadas **en variables** y aplicadas después. Que una función se pueda meter en una
variable, en una lista o en una tabla parece básico, y de estos doce lenguajes **solo cinco lo hacen
del todo**. Los demás ofrecen algo más limitado: **elegir entre funciones que ya existen**, que no es
lo mismo que tratarlas como valores.
""",
    porque="""
Aquí el concepto son las **funciones como valores**, y estos lenguajes lo enseñan porque muestran la
escala completa. **Primera clase de verdad**: Lisp, Smalltalk, Perl, C++ y Tcl, donde una función se
crea, se guarda, se pasa y se devuelve. **Puntero a función con firma comprobada**: Fortran 2003, Ada
95, Pascal y PL/I — se puede seleccionar y pasar, no fabricar. Y **selección por nombre en una
cadena**: COBOL con `CALL` dinámico, RPG con `%paddr`, M con indirección.

Ese tercer nivel es más antiguo y más peligroso: **el destino se decide con texto**, así que ninguna
herramienta puede analizar qué se ejecuta.
""",
    cierre="""
Lo transferible: **una tabla de despacho es la estructura que sustituye a un `switch` cuando las
opciones crecen**, y todos estos lenguajes la construyen, con o sin funciones de primera clase. En
Lisp es una lista de asociaciones; en Perl, un hash de referencias; en C++, un `map` de
`std::function`; en COBOL, una tabla de nombres de programa; en M, un array de nombres de rutina. La
diferencia no está en si se puede, sino en **si alguien comprueba que el nombre existe y que la firma
encaja**.
""",
    langs={
        "cobol": ("""
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
""", """
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
"""),
        "fortran": ("""
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
""", """
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
"""),
        "ada": ("""
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
""", """
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
"""),
        "pascal": ("""
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
""", """
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
"""),
        "lisp": ("""
(let* ((a (read))
       (b (read))
       (f #'+)                 ; la función + COMO VALOR
       (g #'*))
  (format t "suma=~D producto=~D~%" (funcall f a b) (funcall g a b)))
""", """
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
"""),
        "tcl": ("""
gets stdin linea
lassign [split [string trim $linea]] a b

#  Los operadores están disponibles COMO COMANDOS desde Tcl 8.5.
set f ::tcl::mathop::+
set g ::tcl::mathop::*

puts "suma=[$f $a $b] producto=[$g $a $b]"
""", """
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
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($x, $y) = split ' ', $linea;

my $f = sub { return $_[0] + $_[1] };     # referencia a subrutina
my $g = sub { return $_[0] * $_[1] };

printf "suma=%d producto=%d\\n", $f->($x, $y), $g->($x, $y);
""", """
**Lo que esta clase enseña en Perl.** Una **referencia a subrutina** —`sub { ... }` sin nombre, o
`\\&nombre` para una que ya existe— es un valor escalar como cualquier otro, y se invoca con `->()`.

```perl
my $f = sub { ... };        # anónima
my $g = \\&suma;             # referencia a una con nombre
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
my $f = \\&{"main::$nombre"};                # obtenerla por su nombre
defined &{"main::$nombre"};                  # ¿existe?
```

Esa manipulación de *globs* es la base de los generadores de accesores, de los objetos dinámicos y de
media biblioteca de CPAN. Es potente, es peligrosa, y exige `no strict 'refs'` — que es la forma que
tiene Perl de decir "sé lo que hago".
"""),
        "cpp": ("""
#include <functional>
#include <iostream>

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    const std::function<int(int, int)> f = [](int x, int y) { return x + y; };
    const std::function<int(int, int)> g = [](int x, int y) { return x * y; };

    std::cout << "suma=" << f(a, b)
              << " producto=" << g(a, b) << '\\n';
    return 0;
}
""", """
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
"""),
        "rpg": ("""
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
""", """
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
"""),
        "pli": ("""
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
""", """
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
"""),
        "mumps": ("""
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
""", """
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
"""),
        "smalltalk": ("""
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
""", """
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
"""),
    },
)

# ---------------------------------------------------------------------------
# 086 — Módulos, paquetes y espacios de nombres
# ---------------------------------------------------------------------------
SPECS["086"] = dict(
    gancho="""
Una función `doblar` que vive **dentro de algo**. La pregunta de esta clase es cómo evita un lenguaje
que dos personas que nunca se han visto elijan el mismo nombre. Y aquí hay un hallazgo importante:
**el paquete de Ada, de 1983, es el antepasado directo del módulo moderno**, y su separación entre
especificación e implementación es la que copiaron Modula-2, C++ y todos los demás.
""",
    porque="""
Aquí el concepto es el **espacio de nombres y la unidad de compilación**, y estos lenguajes lo enseñan
porque uno de ellos lo inventó. El **`package` de Ada** separa *qué ofrece* de *cómo lo hace*, con
compilación separada y comprobación entre unidades — algo que C no tuvo nunca y que C++ solo consiguió
con los módulos de C++20.

Y en el otro extremo, **COBOL y M no tienen espacios de nombres en absoluto**: el nombre de una rutina
de M es global a todo el sistema, y los prefijos de tres letras —`DIC`, `DIE`, `ZZ`— son un registro
de nombres administrado por convención humana desde hace cincuenta años.
""",
    cierre="""
Lo transferible: **un módulo resuelve dos problemas distintos, y conviene no confundirlos**. Uno es la
**colisión de nombres**, que se resuelve con cualificación. El otro es la **compilación separada con
comprobación**: poder compilar A y B por separado y que el enlazador garantice que encajan. Los
lenguajes con `#include` textual —C, C++ hasta 2020, COBOL con `COPY`— resuelven el segundo mal, y por
eso sus tiempos de compilación y sus errores de enlace son lo que son.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. MODULOS.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9)  COMP-3.
01  R       PIC S9(18) COMP-3.
01  ED-R    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N

    PERFORM DOBLAR

    MOVE R TO ED-R
    DISPLAY "resultado=" FUNCTION TRIM(ED-R)
    STOP RUN.

DOBLAR.
    COMPUTE R = N * 2.
""", """
**Lo que esta clase enseña en COBOL.** **COBOL no tiene espacios de nombres.** Los nombres de programa
son globales a toda la instalación —una biblioteca de carga con miles de miembros de ocho caracteres—
y los nombres de datos son globales al programa (clase 082).

De ahí las dos convenciones que sostienen los sistemas grandes:

1. **Prefijos de nombre de programa por aplicación**: `CLI0100`, `CLI0200`, `FAC0100`. Los tres o
   cuatro primeros caracteres identifican el subsistema, y hay un registro documentado de quién posee
   cada prefijo. Es un espacio de nombres administrado por un ser humano.
2. **Copybooks** para compartir definiciones (clase 052), con `REPLACING` para parametrizarlos.

Y la limitación de ocho caracteres para el nombre de programa no es de COBOL: es del **sistema de
bibliotecas de z/OS**, y ha condicionado la nomenclatura de la industria durante sesenta años.

COBOL sí tiene una forma de módulo, y es la de la clase 082: los **programas anidados** con `GLOBAL` y
`COMMON`.

```cobol
    IDENTIFICATION DIVISION.
    PROGRAM-ID. UTILES IS COMMON.      *> visible para los HERMANOS anidados
```

Un programa `COMMON` es visible desde los demás programas anidados del mismo padre, pero no desde
fuera. Es encapsulación real y **muy poco usada**, porque llegó en 1985 cuando ya había millones de
líneas escritas con prefijos.
"""),
        "fortran": ("""
module utiles
   implicit none
   private                       ! todo privado por defecto
   public :: doblar

contains

   pure function doblar(x) result(r)
      integer, intent(in) :: x
      integer :: r
      r = 2 * x
   end function doblar

end module utiles


program modulos
   use utiles, only: doblar      ! importa SOLO lo que necesita
   implicit none
   integer :: n

   read(*, *) n
   write(*, '(A,I0)') 'resultado=', doblar(n)
end program modulos
""", """
**Lo que esta clase enseña en Fortran.** El **`module`** llegó con **Fortran 90** y fue el cambio más
importante del lenguaje después del formato libre. Antes, todo era subrutinas externas sueltas y
bloques `COMMON`:

```fortran
      COMMON /DATOS/ X, Y, Z      ! memoria compartida por POSICIÓN
```

Un `COMMON` empareja variables **por posición, no por nombre**, y **cada fichero declara su propia
versión**. Si dos ficheros lo declaraban distinto —un `REAL` donde otro ponía `INTEGER`— el programa
compilaba y los datos se corrompían en silencio. Era la mayor fuente de errores del Fortran clásico.

El módulo lo resuelve todo de golpe:

- **Interfaces explícitas**: el compilador comprueba las llamadas entre unidades.
- **`private` / `public`**: encapsulación real (clase 087).
- **`use ... only:`**: importación selectiva, que evita colisiones.
- Y permite **argumentos opcionales, palabras clave y genéricos**, que necesitan interfaz explícita.

Fíjate en `private` como primera línea del módulo: **invierte el defecto** para que todo sea privado
salvo lo que se declare `public`. Es la práctica recomendada, y es la misma política que Rust, RPG y
los módulos de C++20.

Y `use utiles, only: doblar` es importación explícita: sin `only`, se importa todo y aumenta el riesgo
de colisión. Con él, la dependencia queda documentada en la línea.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Modulos is

   --  ESPECIFICACIÓN: qué ofrece el paquete.
   package Utiles is
      function Doblar (X : Integer) return Integer;
   end Utiles;

   --  CUERPO: cómo lo hace. En un proyecto real, en otro fichero.
   package body Utiles is
      function Doblar (X : Integer) return Integer is (2 * X);
   end Utiles;

   N : Integer;
begin
   Get (N);

   Put ("resultado=");
   Put (Utiles.Doblar (N), Width => 1);
   New_Line;
end Modulos;
""", """
**Lo que esta clase enseña en Ada.** **El paquete de Ada es el antepasado directo del módulo
moderno**, y su aportación decisiva es la separación en **dos unidades de compilación**:

```ada
--  utiles.ads : la ESPECIFICACIÓN. Es el contrato.
package Utiles is
   function Doblar (X : Integer) return Integer;
end Utiles;

--  utiles.adb : el CUERPO. Es la implementación.
package body Utiles is
   function Doblar (X : Integer) return Integer is (2 * X);
end Utiles;
```

Quien usa el paquete **solo necesita la especificación**, y el compilador **comprueba que el cuerpo la
cumpla**. Si cambia la implementación sin cambiar la especificación, **no hay que recompilar a los
clientes**.

Compara con C y C++ hasta 2020: el `.h` es **texto que se copia** en cada unidad, sin ninguna
comprobación de que el `.c` lo respete, y cambiar una cabecera obliga a recompilar todo lo que la
incluya. Ada resolvió eso en 1983.

Modula-2 (1978, Wirth) tuvo la misma idea casi a la vez, y de ahí la tomaron Turbo Pascal con las
`unit`, C++ con los módulos de C++20 y Rust con `mod`.

Ada añade además tres cosas que la mayoría no tiene: la **parte privada** (clase 087), los
**subpaquetes jerárquicos** —`Utiles.Texto`, `Utiles.Fechas`— que permiten extender un paquete sin
tocarlo, y los **paquetes genéricos** (clase 078), que se instancian con parámetros.
"""),
        "pascal": ("""
program Modulos;
{$MODE OBJFPC}{$H+}
uses SysUtils;

{  En un proyecto real esto iría en una UNIT aparte:
   unit Utiles;  interface  function Doblar(...)  implementation ...  }
function Doblar(X: Integer): Integer;
begin
  Result := X * 2;
end;

var
  N: Integer;

begin
  Read(N);
  WriteLn('resultado=', IntToStr(Doblar(N)));
end.
""", """
**Lo que esta clase enseña en Pascal.** La **`unit`** de Turbo Pascal (1987) tomó la idea de Modula-2
y la hizo popular, con una estructura que se lee sola:

```pascal
unit Utiles;

interface                    { lo PÚBLICO: lo que ven los demás }
function Doblar(X: Integer): Integer;

implementation               { lo PRIVADO: nadie de fuera lo ve }
function Doblar(X: Integer): Integer;
begin
  Result := X * 2;
end;

initialization               { código que se ejecuta al CARGAR la unidad }
finalization                 { y al DESCARGARLA }
end.
```

Cuatro secciones con nombres que dicen exactamente qué hacen. Y la sección `interface` es lo único
que necesita quien haga `uses Utiles`.

`initialization` y `finalization` no tienen equivalente en Ada ni en C++: son bloques que el runtime
ejecuta al cargar y descargar la unidad, en orden de dependencias. Se usan para registrar clases,
abrir recursos y liberarlos, y son la razón de que muchas bibliotecas de Delphi funcionen con solo
añadirlas a la cláusula `uses`.

La compilación de Pascal aprovecha esto al máximo: **el compilador genera un fichero `.ppu` con la
interfaz ya analizada**, así que compilar un programa que usa cien unidades no reanaliza cien
cabeceras. Es la razón principal de la velocidad legendaria de Turbo Pascal y Free Pascal frente a
C++.

Lo que Pascal **no** tiene son espacios de nombres anidados de verdad. Delphi añadió los *namespaces
con puntos* —`Sistema.Utiles.Texto`— pero son un prefijo en el nombre de la unidad, no una jerarquía
real como los subpaquetes de Ada.
"""),
        "lisp": ("""
(defpackage :utiles
  (:use :cl)
  (:export #:doblar))

(in-package :utiles)

(defun doblar (x) (* 2 x))

(in-package :cl-user)

(let ((n (read)))
  (format t "resultado=~D~%" (utiles:doblar n)))
""", """
**Lo que esta clase enseña en Common Lisp.** Los **paquetes de Lisp no son módulos: son espacios de
nombres de SÍMBOLOS**, y esa diferencia es la clave para entenderlos.

Un paquete es una tabla que asocia **nombres a símbolos**. Cuando el lector encuentra `doblar`, busca
en el paquete actual el símbolo con ese nombre; si no está, lo crea. `utiles:doblar` es "el símbolo
`doblar` del paquete `utiles`".

De ahí salen dos notaciones que hay que distinguir:

```lisp
utiles:doblar      ; símbolo EXPORTADO: parte de la interfaz
utiles::interno    ; DOS puntos: acceso a un símbolo NO exportado
```

El doble dos puntos **funciona siempre** — se puede acceder a cualquier símbolo interno de cualquier
paquete. No es una barrera, es una señal: escribir `::` es declarar por escrito que estás usando algo
privado. Es la misma filosofía que el guion bajo en Python.

Y como los paquetes agrupan **símbolos**, no funciones, agrupan a la vez funciones, variables, clases,
macros y tipos — todo lo que tenga nombre.

Lo que Lisp **no** tiene en el estándar es un sistema de ficheros ni de compilación: `defpackage` dice
qué nombres hay, no de dónde salen. Eso lo aporta **ASDF**, el sistema de construcción de facto, con
`Quicklisp` encima para la distribución. Es la misma separación que en Python entre el `import` del
lenguaje y `pip`.
"""),
        "tcl": ("""
namespace eval ::utiles {
    namespace export doblar

    proc doblar {x} {
        return [expr {$x * 2}]
    }
}

gets stdin linea
set n [string trim $linea]

puts "resultado=[::utiles::doblar $n]"
""", """
**Lo que esta clase enseña en Tcl.** Los **espacios de nombres** llegaron en **Tcl 8.0 (1997)**, y son
jerárquicos con separador `::`, igual que C++.

```tcl
namespace eval ::miapp::datos {
    variable cache          ;# variable del ESPACIO (clase 082)
    proc cargar {} { ... }
}
::miapp::datos::cargar
```

Y son **contenedores de tres cosas**: procedimientos, variables y otros espacios anidados.

Lo que hace peculiar a Tcl es que la **resolución de nombres es dinámica y por reglas de búsqueda**,
no estática:

```tcl
namespace eval ::miapp {
    proc f {} { g }       ;# ¿qué g?  Se busca en ::miapp, y si no, en ::
}
```

Un comando no cualificado se busca **primero en el espacio actual y después en el global**. Eso es
cómodo y produce sorpresas: definir un `::miapp::puts` cambia el significado de `puts` dentro de ese
espacio.

Y hay una separación que conviene conocer, porque Tcl tiene **dos** mecanismos donde otros tienen uno:

- **`namespace`** resuelve la **colisión de nombres**.
- **`package`** resuelve la **carga y las versiones**: `package require http 2.9` busca, carga y
  comprueba la versión.

Los dos son independientes: un paquete puede definir varios espacios, y un espacio puede montarse a
mano sin paquete. En Java, Python o Rust las dos cosas van juntas; en Tcl, como en Lisp con ASDF,
están separadas — y esa separación es la que permite `namespace import` selectivo.
"""),
        "perl": ("""
use strict;
use warnings;

package Utiles;

sub doblar { return $_[0] * 2 }

package main;

my $n = <STDIN>;
chomp $n;

print "resultado=", Utiles::doblar($n), "\\n";
""", """
**Lo que esta clase enseña en Perl.** `package` cambia **el espacio de nombres actual**, y todo lo
declarado a partir de ahí pertenece a él. `Utiles::doblar` es la cualificación completa, con `::` como
separador.

Y un paquete de Perl **no es un fichero ni una unidad de compilación**: es una entrada en la tabla de
símbolos global. Un fichero puede definir varios paquetes —como este programa— y un paquete puede
estar repartido en varios ficheros.

La convención —**un paquete por fichero, con la ruta del nombre**— es solo eso, una convención, y es lo
que `use` da por supuesto:

```perl
use Mi::Modulo;        # busca Mi/Modulo.pm en @INC
```

Perl separa además con claridad **tres cosas** que en otros lenguajes van juntas:

| Mecanismo | Qué hace |
|---|---|
| `package` | Declara el espacio de nombres |
| `require` | **Carga** el fichero, una sola vez, en ejecución |
| `use` | `require` en tiempo de compilación **+ `import`** |

`use` es literalmente `BEGIN { require X; X->import(...) }`, y esa tercera pieza —`import`— es un
**método normal** que el módulo define. Por eso `Exporter` es un módulo y no una característica del
lenguaje: exportar nombres es código que se ejecuta.

Eso permite módulos que hacen cosas muy distintas al importarse —`use strict` cambia el compilador,
`use constant` define constantes, `use parent` establece herencia— y es una de las capacidades más
características de Perl. También es la razón de que `use` no sea inocuo: **ejecuta código**.
"""),
        "cpp": ("""
#include <iostream>

namespace utiles {
    int doblar(int x) { return x * 2; }
}

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "resultado=" << utiles::doblar(n) << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** Los **espacios de nombres** (1998) resolvieron la colisión de
nombres, y **no** resolvieron la compilación separada — que era el otro problema de la clase.

Durante veintidós años, C++ compartió código con **`#include`**, que es **sustitución textual**: el
preprocesador copia el fichero entero en cada unidad de traducción. Las consecuencias son conocidas:

- Un `.cpp` de cien líneas que incluye `<iostream>` compila **decenas de miles** de líneas.
- Cambiar una cabecera obliga a recompilar todo lo que la incluya.
- El orden de los `#include` puede cambiar el significado del programa.
- Hacen falta guardas —`#pragma once`— para no incluir dos veces.

**C++20 introdujo los módulos**, que son por fin lo que Ada tenía en 1983:

```cpp
export module utiles;
export int doblar(int x) { return x * 2; }

// y en el cliente:
import utiles;
```

Un módulo se compila **una vez** a una representación binaria, y quien lo importa la lee ya analizada
—como el `.ppu` de Pascal—. Además, **lo no exportado es realmente invisible**, no solo por
convención.

La adopción va despacio por el ecosistema de sistemas de construcción, pero es el cambio estructural
más importante del lenguaje en décadas.

Y sobre los espacios: `using namespace std;` **en una cabecera** es el error clásico, porque contamina
a todo el que la incluya. En un `.cpp` es discutible; en un `.h`, no.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi MODULOS;
  n int(10) const;
end-pi;

dcl-s salida char(40);

salida = 'resultado=' + %char(doblar(n));
dsply salida;

*inlr = *on;
return;

// En un proyecto real, esto estaría en OTRO módulo, con export,
// y se enlazaría en un PROGRAMA DE SERVICIO.
dcl-proc doblar;
  dcl-pi *n int(20);
    x int(10) const;
  end-pi;
  return x * 2;
end-proc;
""", """
**Lo que esta clase enseña en RPG.** El sistema de módulos de RPG llegó con **ILE** (1993) y es de los
más elaborados de esta página, con cuatro piezas:

1. **Módulo** (`*MODULE`): el resultado de compilar un fuente. Sus procedimientos son privados salvo
   que lleven `export`.
2. **Programa de servicio** (`*SRVPGM`): varios módulos enlazados en una unidad **compartida y
   cargada dinámicamente**, como una biblioteca dinámica.
3. **Directorio de enlace** (`*BNDDIR`): la lista de dónde buscar lo que falte al enlazar.
4. **Fuente de exportación de enlace**: **la lista ordenada de qué exporta un programa de servicio**.

La cuarta es la interesante y no tiene equivalente en el núcleo. Es un fichero que enumera los
procedimientos exportados **en orden**, y ese orden determina el número que usa el enlazador:

```text
STRPGMEXP PGMLVL(*CURRENT) SIGNATURE('UTILES V1')
  EXPORT SYMBOL("DOBLAR")
  EXPORT SYMBOL("TRIPLICAR")
ENDPGMEXP
```

La **firma** (`SIGNATURE`) permite versionar la interfaz: si se añade un procedimiento **al final**,
los programas antiguos siguen funcionando sin recompilar. Si se cambia el orden o se quita algo, la
firma cambia y **los clientes fallan al arrancar** con un mensaje claro.

Es control de versiones de ABI en el enlazador, exactamente el problema que en Linux resuelven los
`soname` y los scripts de versión de `ld`, integrado en la plataforma desde 1993.
"""),
        "pli": ("""
 modulos: procedure options(main);

    declare n fixed binary(31);

    get list (n);
    put skip list ('resultado=' || trim(char(doblar(n))));

 doblar: procedure (x) returns (fixed binary(31));
    declare x fixed binary(31);
    return (x * 2);
 end doblar;

 end modulos;
""", """
**Lo que esta clase enseña en PL/I.** **PL/I no tiene módulos ni espacios de nombres.** Tiene
**procedimientos externos**, compilados por separado y enlazados por nombre, exactamente como C antes
de los módulos.

```pli
 doblar: procedure (x) returns (fixed binary(31)) external;
```

`external` declara que el nombre es visible para el enlazador. Y de ahí viene el problema clásico:
**los nombres externos son globales a todo el ejecutable**, y el enlazador los empareja por texto sin
comprobar firmas.

El sustituto de los módulos en PL/I es **`%INCLUDE`**, que es inclusión textual como el `COPY` de
COBOL y el `#include` de C:

```pli
%include declaraciones;
```

Con los mismos inconvenientes: sin comprobación entre unidades, con recompilación en cascada y con el
orden importando.

Lo que PL/I sí ofrece, y es lo que se usa en su lugar, es el **anidamiento léxico ilimitado** de la
clase 083: un procedimiento externo grande con procedimientos internos anidados **es** una forma de
módulo — lo interno es privado y lo externo es la interfaz.

```pli
 utiles: procedure external;
    declare estado fixed binary(31) static;   /* privado del "módulo" */

    doblar: procedure (x) returns (fixed binary(31));  /* privado también */
    ...
 end utiles;
```

Es encapsulación por anidamiento, la misma técnica que se usa en JavaScript con las funciones
inmediatamente invocadas, y era lo mejor disponible en 1964.
"""),
        "mumps": ("""
MODULOS ; Modulos y espacios de nombres -- clase 086
 read n
 write "resultado=", $$doblar^MODULOS(n), !
 quit
 ;
doblar(x) ; devuelve el doble
 quit x * 2
""", """
**Lo que esta clase enseña en M.** **M no tiene espacios de nombres.** La unidad es la **rutina**, y su
nombre es **global a todo el sistema**: `$$doblar^UTILES` significa "la etiqueta `doblar` de la rutina
`UTILES`", y solo puede haber una `UTILES` en el entorno.

Peor aún: **los nombres de rutina están limitados a ocho caracteres** en el estándar, igual que los
nombres de programa de z/OS.

La solución que inventó la comunidad es la más artesanal de esta página: **un registro de prefijos
administrado por humanos**. En **VistA**, cada paquete tiene asignado un prefijo de dos o tres letras
por la oficina que coordina el proyecto:

```text
DI   -> FileMan (diccionario)
DIC  -> FileMan, búsquedas
LR   -> Laboratorio
PS   -> Farmacia
ZZ   -> reservado para código LOCAL de cada hospital
```

Todas las rutinas y todos los *globals* de Farmacia empiezan por `PS`. El prefijo `ZZ` está reservado
para las modificaciones locales de cada centro, de modo que **no colisionen con las actualizaciones
nacionales**.

Eso es un espacio de nombres implementado con documentación y disciplina, funcionando en un sistema de
millones de líneas desde los años 80. Es exactamente lo mismo que los prefijos `WS-` de COBOL y los
nombres `CLI0100`, escalado a nivel nacional.

Las implementaciones modernas sí lo resolvieron: **InterSystems IRIS tiene *namespaces* de verdad** —
entornos separados con sus propias rutinas y globals, y mapeos entre ellos—, y **YottaDB** permite
separar la configuración de globals por entorno. Pero el lenguaje base sigue sin ellos.
"""),
        "smalltalk": ("""
| n |

n := stdin nextLine trimBoth asNumber.

Transcript show: 'resultado=', (n * 2) printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** **El Smalltalk-80 clásico no tiene espacios de nombres.**
Hay **un único diccionario global**, llamado `Smalltalk`, donde viven todas las clases del sistema. Dos
paquetes que definan una clase `Punto` colisionan.

La solución de la comunidad es la misma de M y COBOL: **prefijos**.

```smalltalk
RBParser         "Refactoring Browser"
GLMorphic        "Glamorous Toolkit"
ZnClient         "Zinc HTTP"
SUnitTest        "SUnit"
```

Dos o tres letras al principio de cada clase, por convención. Es un registro de prefijos exactamente
como el de VistA.

Lo que Smalltalk sí tiene, y es distinto, son dos mecanismos de **organización** que no son espacios
de nombres:

- **Categorías**: agrupan clases y métodos para el navegador. Son puramente organizativas.
- **Paquetes** (Monticello, Metacello): unidades de versionado y carga, con dependencias.

Un paquete decide **qué se carga y en qué orden**; una categoría decide **cómo se ve en la
herramienta**. Ninguno de los dos evita una colisión de nombres.

Los intentos de añadir espacios de nombres reales —VisualWorks los tiene, y hubo propuestas para
Pharo— chocaron con una dificultad de fondo: **en un sistema vivo con objetos ya instanciados**,
cambiar cómo se resuelven los nombres afecta a código en ejecución. Es un problema que un lenguaje
compilado no tiene.

Es el precio de la imagen viva de la clase 041, y una de las pocas cosas en las que el modelo de
Smalltalk sale claramente perdiendo.
"""),
    },
)

# ---------------------------------------------------------------------------
# 087 — Visibilidad, encapsulación y contratos
# ---------------------------------------------------------------------------
SPECS["087"] = dict(
    gancho="""
Un saldo que solo se puede cambiar depositando. La encapsulación en su forma mínima: **un dato que
nadie de fuera puede tocar directamente**. Y aquí hay dos posturas radicalmente distintas: **Ada tiene
una "parte privada" en la especificación** —visible para leer, inaccesible para usar— y **Smalltalk
hace todos los campos privados y todos los métodos públicos, sin excepción y sin palabras clave**.
""",
    porque="""
Aquí el concepto es la **ocultación de información**, formulada por David Parnas en 1972, y estos
lenguajes la implementan de formas muy distintas. **Ada** separa la especificación en parte pública y
**parte privada**, que el cliente puede leer pero no usar — una idea que ningún lenguaje del núcleo
copió y que resuelve el problema de que el compilador necesita saber el tamaño de un tipo aunque el
programador no deba conocerlo.

**Fortran** lo hace con `private` a nivel de módulo, **RPG** con `export`, y **COBOL, PL/I y M** no
tienen nada: la encapsulación es convención.
""",
    cierre="""
Lo transferible: **la encapsulación no es esconder, es prometer poco**. Un campo público es una
promesa de que ese campo existirá para siempre con ese nombre y ese tipo; uno privado deja libertad
para cambiarlo. Por eso los lenguajes modernos hacen **privado el defecto** —Rust, los módulos de
C++20, `private` en Fortran, `export` en RPG— y por eso el consejo práctico es el mismo en todos:
**exporta lo mínimo, y lo que exportes, no lo cambies**.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. ENCAPSULA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9)  COMP-3.
01  SALDO   PIC S9(18) COMP-3 VALUE 0.
01  IMPORTE PIC S9(9)  COMP-3.
01  ED-S    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N

    MOVE N TO IMPORTE
    PERFORM DEPOSITAR
    PERFORM DEPOSITAR

    MOVE SALDO TO ED-S
    DISPLAY "saldo=" FUNCTION TRIM(ED-S)
    STOP RUN.

DEPOSITAR.
    COMPUTE SALDO = SALDO + IMPORTE.
""", """
**Lo que esta clase enseña en COBOL.** **En COBOL no hay encapsulación posible dentro de un
programa**: `SALDO` es global y cualquier párrafo puede escribirlo. La disciplina de "solo se toca
desde `DEPOSITAR`" es una convención que nada comprueba.

Donde COBOL sí tiene ocultación de verdad es **entre programas**, y de la forma más fuerte posible:
**el `WORKING-STORAGE` de un programa es completamente inaccesible desde otro**. No hay forma de leer
las variables de un programa llamado; solo lo que viaje por `USING` y `RETURNING`.

Eso es encapsulación total por unidad de compilación, y es la razón de que la arquitectura típica de
un sistema COBOL sea **muchos programas pequeños** en lugar de uno grande: **el programa es la unidad
de encapsulación**.

Y los **programas anidados** de COBOL-85 (clase 082) dan un nivel intermedio:

```cobol
    IDENTIFICATION DIVISION.
    PROGRAM-ID. CUENTA IS COMMON.
    DATA DIVISION.
    WORKING-STORAGE SECTION.
    01  SALDO  PIC S9(18) COMP-3 VALUE 0.    *> PRIVADO
    ...
```

`SALDO` no es visible para el programa padre, y `CUENTA` sí lo es para sus hermanos anidados. Es un
objeto con estado privado y métodos públicos, escrito en COBOL de 1985.

Y en el padre, la palabra clave `GLOBAL` en una declaración la hace visible para los anidados:
`01 CONFIG PIC X(40) GLOBAL.` — encapsulación con excepciones declaradas, que es exactamente lo que
hace `protected` en un lenguaje de objetos.
"""),
        "fortran": ("""
module cuenta
   implicit none
   private                          ! todo privado por defecto
   public :: depositar, saldo_actual

   integer :: saldo = 0             ! PRIVADO: invisible desde fuera del módulo

contains

   subroutine depositar(x)
      integer, intent(in) :: x
      saldo = saldo + x
   end subroutine depositar

   function saldo_actual() result(s)
      integer :: s
      s = saldo
   end function saldo_actual

end module cuenta


program encapsula
   use cuenta
   implicit none
   integer :: n

   read(*, *) n
   call depositar(n)
   call depositar(n)

   write(*, '(A,I0)') 'saldo=', saldo_actual()
end program encapsula
""", """
**Lo que esta clase enseña en Fortran.** La línea **`private`** suelta al principio del módulo
**invierte el defecto**: todo es privado salvo lo que se declare `public`. Es la política que hoy
recomiendan todas las guías y que Rust adoptó como norma del lenguaje.

Y es un cambio enorme respecto al Fortran clásico, donde los bloques `COMMON` eran **memoria
compartida sin ninguna protección**: cualquier subrutina que declarara el mismo `COMMON` podía leer y
escribir esas variables.

```fortran
      COMMON /CUENTA/ SALDO      ! cualquiera que escriba esto ve SALDO
```

El módulo con `private` es la respuesta directa a ese problema, y es la razón principal de que la
migración a módulos sea la recomendación número uno para modernizar código Fortran.

Fortran 2003 añadió además el **`protected`**, que no tiene equivalente en el núcleo:

```fortran
integer, public, protected :: version = 3
```

`protected` significa **público para leer, privado para escribir**. Desde fuera del módulo se puede
consultar `version` pero no asignarla. Es exactamente un `readonly` público, y evita el par
`private` + función de acceso que en otros lenguajes hay que escribir a mano.

Y a nivel de tipos derivados, los componentes también pueden ser `private`:

```fortran
type :: Cuenta
   private
   integer :: saldo = 0        ! invisible incluso teniendo el objeto
end type
```
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Encapsula is

   package Cuenta is
      procedure Depositar (X : Integer);
      function Saldo return Integer;
   private
      --  PARTE PRIVADA: el cliente la ve al leer, pero NO puede usarla.
      Total : Integer := 0;
   end Cuenta;

   package body Cuenta is
      procedure Depositar (X : Integer) is
      begin
         Total := Total + X;
      end Depositar;

      function Saldo return Integer is (Total);
   end Cuenta;

   N : Integer;
begin
   Get (N);
   Cuenta.Depositar (N);
   Cuenta.Depositar (N);

   Put ("saldo=");
   Put (Cuenta.Saldo, Width => 1);
   New_Line;
end Encapsula;
""", """
**Lo que esta clase enseña en Ada.** La **parte privada de una especificación** es una idea de Ada que
casi nadie copió y que resuelve un problema real de diseño de lenguajes.

El problema es este: para declarar una variable de un tipo, **el compilador necesita saber cuánto
ocupa**. Pero el programador **no debería** conocer su estructura interna. Las dos cosas parecen
incompatibles.

La solución de Ada es partir la especificación en dos:

```ada
package Cuentas is
   type Cuenta is private;                    --  el cliente sabe que existe...
   procedure Depositar (C : in out Cuenta; X : Integer);
   function Saldo (C : Cuenta) return Integer;
private
   type Cuenta is record                       --  ...y NO puede usar esto
      Total : Integer := 0;
      Historial : ...;
   end record;
end Cuentas;
```

El cliente **compila** contra la parte privada —así el compilador conoce el tamaño— pero **el lenguaje
le prohíbe acceder a sus campos**. Si escribe `C.Total`, no compila.

C++ resuelve lo mismo poniendo los campos privados en la clase, con el mismo efecto: están en la
cabecera, se ven al leer, no se pueden usar. La diferencia es que Ada **lo dice explícitamente con una
sección llamada `private`**, mientras que en C++ hay que entender por qué los campos privados están en
el `.h`.

Y la alternativa —ocultarlos de verdad— es el modismo *pimpl* en C++ y los **tipos incompletos**
(`limited private`) en Ada, a costa de una indirección.
"""),
        "pascal": ("""
program Encapsula;
{$MODE OBJFPC}{$H+}
uses SysUtils;

type
  TCuenta = class
  private
    FSaldo: Integer;          { PRIVADO }
  public
    procedure Depositar(X: Integer);
    property Saldo: Integer read FSaldo;    { solo lectura desde fuera }
  end;

procedure TCuenta.Depositar(X: Integer);
begin
  FSaldo := FSaldo + X;
end;

var
  N: Integer;
  C: TCuenta;

begin
  Read(N);
  C := TCuenta.Create;
  try
    C.Depositar(N);
    C.Depositar(N);
    WriteLn('saldo=', IntToStr(C.Saldo));
  finally
    C.Free;
  end;
end.
""", """
**Lo que esta clase enseña en Pascal.** Object Pascal tiene **cinco niveles de visibilidad**, más que
casi cualquier lenguaje de esta página:

| Nivel | Quién accede |
|---|---|
| `strict private` | **Solo** la propia clase |
| `private` | La clase **y cualquier código de la misma unidad** |
| `protected` | La clase y sus descendientes |
| `public` | Todos |
| `published` | Como `public`, **y además genera RTTI** para el inspector |

Las dos peculiares son la segunda y la quinta. **`private` en Delphi NO es estrictamente privado**:
cualquier código del mismo fichero puede acceder. Es una decisión pragmática —permite que clases
relacionadas cooperen— y sorprende a quien viene de Java. Por eso Delphi 2005 añadió `strict private`.

**`published`** no existe en ningún otro lenguaje: marca los miembros que el **inspector de objetos**
del IDE puede ver y editar, y que se guardan en el fichero `.dfm` del formulario. Es visibilidad al
servicio de la herramienta, y es lo que hace posible el diseño visual de la clase 073.

Y `property Saldo: Integer read FSaldo;` sin `write` es una **propiedad de solo lectura**: desde fuera
se lee como un campo y no se puede asignar. Es el `protected` de Fortran con otra sintaxis, y el
mecanismo que .NET copió literalmente.
"""),
        "lisp": ("""
(let* ((n (read))
       (saldo 0)
       (depositar (lambda (x) (incf saldo x))))
  (funcall depositar n)
  (funcall depositar n)
  (format t "saldo=~D~%" saldo))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp tiene **dos formas de encapsular**, y son muy
distintas.

La primera es la de este programa: **la clausura** de la clase 083. `saldo` es una variable léxica que
**solo la lambda puede tocar**. Es privacidad real —no hay forma de acceder a `saldo` desde fuera— y
no necesita ninguna palabra clave.

```lisp
(defun crear-cuenta ()
  (let ((saldo 0))
    (list :depositar (lambda (x) (incf saldo x))
          :saldo     (lambda () saldo))))
```

Eso es un objeto con estado **verdaderamente privado**, más privado que cualquier campo de CLOS.

La segunda es la de los **paquetes** (clase 086): exportar o no exportar un símbolo. Y ahí Lisp toma
una postura característica: **`utiles::interno` con dos puntos accede a cualquier símbolo no
exportado**. No hay barrera técnica.

Esa decisión es deliberada y refleja una filosofía: **la privacidad es una indicación de diseño, no
una cerradura**. El autor dice "esto es interno"; quien lo use asume el riesgo de que cambie. Es la
misma postura que Python con el guion bajo, y la contraria a Java y C++.

En CLOS, los campos (*slots*) **no tienen niveles de visibilidad**: se controla el acceso decidiendo
qué accesores se generan y cuáles se exportan.

```lisp
(defclass cuenta ()
  ((saldo :initform 0 :reader saldo)))    ; solo LECTOR, no escritor
```

Sin `:accessor` ni `:writer`, no hay forma pública de asignar — el mismo `protected` de Fortran, otra
vez.
"""),
        "tcl": ("""
namespace eval ::cuenta {
    variable saldo 0                  ;# no se exporta: "privado" por convención
    namespace export depositar saldo_actual

    proc depositar {x} {
        variable saldo
        set saldo [expr {$saldo + $x}]
    }

    proc saldo_actual {} {
        variable saldo
        return $saldo
    }
}

gets stdin linea
set n [string trim $linea]

::cuenta::depositar $n
::cuenta::depositar $n

puts "saldo=[::cuenta::saldo_actual]"
""", """
**Lo que esta clase enseña en Tcl.** Los espacios de nombres de Tcl **no tienen privacidad real**:
`namespace export` decide qué se puede importar con `namespace import`, pero **cualquiera puede
escribir `::cuenta::saldo` y acceder directamente**.

Es la misma postura que Lisp con `::` y Python con el guion bajo: **una indicación, no una cerradura**.

Donde Tcl sí tiene encapsulación de verdad es en **TclOO**, el sistema de objetos que entró en el
núcleo con Tcl 8.6:

```tcl
oo::class create Cuenta {
    variable saldo                     ;# variable de INSTANCIA, privada
    constructor {} { set saldo 0 }
    method depositar {x} { incr saldo $x }
    method saldo {} { return $saldo }
}

set c [Cuenta new]
$c depositar 50
```

Las variables declaradas con `variable` dentro de una clase TclOO son **de instancia y privadas**: no
hay sintaxis para acceder a ellas desde fuera del objeto.

Y TclOO tiene un rasgo poco común: **las clases se pueden modificar en ejecución**, añadiendo métodos
y cambiando la jerarquía sobre objetos que ya existen. Es el modelo de Smalltalk, y viene del mismo
sitio — el diseño de TclOO se inspiró explícitamente en él y en el sistema de metaobjetos de CLOS.

Además tiene `oo::mixin` y filtros de método, que permiten componer comportamiento sin herencia, y
`unexport` para retirar un método de la interfaz pública.
"""),
        "perl": ("""
use strict;
use warnings;

{
    package Cuenta;

    my $saldo = 0;                     # léxica del bloque: VERDADERAMENTE privada

    sub depositar { $saldo += $_[0] }
    sub saldo     { return $saldo }
}

my $n = <STDIN>;
chomp $n;

Cuenta::depositar($n);
Cuenta::depositar($n);

print "saldo=", Cuenta::saldo(), "\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl tiene **dos niveles de privacidad muy distintos**, y este
programa usa el fuerte.

**El débil** es la convención: una subrutina o variable de paquete cuyo nombre empieza por guion bajo
—`_ayudante`— se considera privada, y **nada lo impide**. `Cuenta::_ayudante()` funciona.

**El fuerte** es el de este programa: una variable **léxica** (`my`) declarada en el ámbito del
fichero o de un bloque. `$saldo` **no está en la tabla de símbolos**, así que **no hay ninguna forma
de acceder a ella desde fuera**, ni siquiera con manipulación de *globs*.

```perl
my $secreto = 42;              # invisible desde cualquier otro sitio
our $publico = 42;             # accesible como $Cuenta::publico
```

Esa privacidad es más fuerte que la de Java —donde la reflexión rompe `private`— y es la razón de que
el patrón de la clase 083, los objetos hechos con clausuras, se use en Perl cuando los datos deben ser
realmente inaccesibles.

Para los objetos normales, Perl usa `bless` sobre un hash, y **todos sus campos son accesibles**:
`$obj->{saldo}` funciona desde cualquier sitio. Es la crítica clásica al modelo de objetos de Perl 5.

Las alternativas de CPAN lo resuelven: **`Moose`** y **`Moo`** dan atributos con `is => 'ro'`,
constructores y validación; y los **campos de instancia** de la nueva palabra clave `class`
(experimental desde 5.38) son léxicos y por tanto privados de verdad.
"""),
        "cpp": ("""
#include <iostream>

class Cuenta {
    int saldo_ = 0;                 // PRIVADO por defecto en una class
public:
    void depositar(int x) { saldo_ += x; }
    int saldo() const { return saldo_; }
};

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    Cuenta c;
    c.depositar(n);
    c.depositar(n);

    std::cout << "saldo=" << c.saldo() << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** La única diferencia entre `class` y `struct` en C++ es el
**defecto**: `class` empieza en `private`, `struct` en `public`. Todo lo demás es idéntico — una
`struct` puede tener métodos, herencia y constructores.

Y hay tres niveles —`private`, `protected`, `public`— más el mecanismo que más discusión ha generado:
**`friend`**.

```cpp
class Cuenta {
    int saldo_ = 0;
    friend class Auditor;                       // Auditor ve mis privados
    friend std::ostream& operator<<(std::ostream&, const Cuenta&);
};
```

`friend` **rompe la encapsulación de forma declarada**: la clase decide quién puede mirar dentro. Se
critica como un agujero, y su defensa es sólida: es la propia clase quien concede el permiso, así que
la lista de quién ve sus privados **está escrita en la clase**. Es más honesto que hacer todo público.

El caso canónico es el `operator<<` de la primera línea: una función libre que necesita acceder a los
campos para imprimirlos, y que no puede ser un método porque el receptor es el flujo.

Fíjate también en `int saldo() const`: el **`const` al final** promete que el método no modifica el
objeto, y el compilador lo comprueba. Es la mitad de la pureza de la clase 084, aplicada a los
métodos, y no tiene equivalente en Java ni en Python.

Y el subrayado final en `saldo_` es una convención muy extendida para distinguir el campo del método
que lo devuelve.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller) main(Principal);

dcl-s saldo int(20) static;      // global del MÓDULO: sin export, es privada

dcl-proc Principal;
  dcl-pi *n;
    n int(10) const;
  end-pi;

  dcl-s salida char(40);

  depositar(n);
  depositar(n);

  salida = 'saldo=' + %char(saldoActual());
  dsply salida;
end-proc;

dcl-proc depositar export;       // EXPORT: parte de la interfaz del módulo
  dcl-pi *n;
    x int(10) const;
  end-pi;
  saldo += x;
end-proc;

dcl-proc saldoActual export;
  dcl-pi *n int(20); end-pi;
  return saldo;
end-proc;
""", """
**Lo que esta clase enseña en RPG.** La palabra **`export`** en un `dcl-proc` es todo el mecanismo de
visibilidad de RPG, y tiene la polaridad correcta: **sin ella, el procedimiento es privado del
módulo**.

```rpgle
dcl-proc publico export;   // visible desde otros módulos
dcl-proc privado;          // solo desde este módulo
```

Es el `static` de C invertido: en C hay que escribir `static` para **ocultar**; en RPG hay que
escribir `export` para **mostrar**. La segunda opción es mejor, y es la que eligieron después Rust,
los módulos de C++20 y Java con los paquetes.

Y las **variables globales del módulo** —como `saldo` en este programa— son **siempre privadas**: no
hay forma de exportar una variable en RPG. Solo se exportan procedimientos.

Eso fuerza el patrón que se vio en la clase 083: **un módulo con estado privado y procedimientos de
acceso** es, exactamente, un objeto con un solo ejemplar. Y es la arquitectura recomendada de la
plataforma para el código reutilizable.

Hay además una advertencia de seguridad propia de IBM i que conviene conocer: si el módulo se enlaza
en un **programa de servicio** con activación compartida, **el estado `static` se comparte entre
trabajos**. Un dato de un usuario puede quedar visible para otro. Por eso la guía es que los módulos
de servicio sean **sin estado**, y que el estado viva en el programa que los usa.
"""),
        "pli": ("""
 encapsula: procedure options(main);

    declare n     fixed binary(31);
    declare saldo fixed binary(31) static initial(0);   /* "privado" del bloque */

    get list (n);

    call depositar(n);
    call depositar(n);

    put skip list ('saldo=' || trim(char(saldo)));

 depositar: procedure (x);
    declare x fixed binary(31);
    saldo = saldo + x;        /* ve `saldo` por anidamiento léxico */
 end depositar;

 end encapsula;
""", """
**Lo que esta clase enseña en PL/I.** **PL/I no tiene ninguna palabra clave de visibilidad**: no hay
`private`, `public` ni `export`. Lo único que controla el acceso es el **anidamiento léxico** de la
clase 083.

Una variable declarada en un procedimiento **es invisible desde fuera** y visible para todo lo anidado
dentro. Con eso se construye encapsulación:

```pli
 modulo: procedure external;
    declare estado fixed binary(31) static;    /* privado: nadie de fuera lo ve */

    publico: procedure external;                /* pero ESTE sí es visible */
       ...
    end publico;
 end modulo;
```

El `external` en un procedimiento interno lo hace visible al enlazador, así que la combinación
—estado en el ámbito exterior, procedimientos `external` anidados dentro— da un módulo con estado
privado.

Es exactamente el patrón que en JavaScript se llamó **expresión de función inmediatamente invocada**
(*IIFE*) y que durante quince años fue la única forma de tener privacidad en ese lenguaje. En PL/I
funciona desde 1964.

Lo que falta es lo que Ada añadió: **una declaración explícita de qué es interfaz y qué es
implementación**, comprobada por el compilador y legible por el cliente. En PL/I hay que deducirlo del
anidamiento, y en un procedimiento de dos mil líneas eso no es trivial.
"""),
        "mumps": ("""
ENCAPSULA ; Encapsulacion -- clase 087
 read n
 kill ^SALDO
 set ^SALDO = 0
 do depositar(n)
 do depositar(n)
 write "saldo=", ^SALDO, !
 quit
 ;
depositar(x) ;
 set ^SALDO = ^SALDO + x
 quit
""", """
**Lo que esta clase enseña en M.** **M no tiene encapsulación de ninguna clase.** Todas las variables
locales son globales al proceso (clase 082) y todos los ***globals*** son visibles para todos los
procesos del entorno. `^SALDO` lo puede leer y escribir cualquier rutina del sistema.

No hay `private`, no hay módulos y no hay barreras. Y esa ausencia total es, seguramente, la
diferencia más grande entre M y cualquier otro lenguaje de esta página.

Lo que hay en su lugar es lo de la clase 086: **convención de prefijos** más una capa construida
encima. En **VistA**, esa capa es **FileMan**, y es la respuesta seria al problema:

```mumps
 do FILE^DICN(...)        ; crear un registro
 do UPDATE^DIE(...)       ; actualizar
 set x = $$GET1^DIQ(...)  ; consultar un campo
```

La regla de la plataforma es que **el código de aplicación NO toca los globals directamente**: los
toca a través de las APIs de FileMan, que validan los datos, respetan la seguridad, mantienen los
índices y registran la auditoría.

Eso es encapsulación implementada **como una biblioteca y una norma**, no como una característica del
lenguaje. Y funciona: VistA lleva cuarenta años y millones de líneas con ese contrato.

También falla exactamente como cabría esperar: **hay código antiguo que accede directamente a los
globals**, saltándose la validación, y localizarlo es un problema recurrente de mantenimiento. Cuando
la barrera es una norma, alguien acaba cruzándola.
"""),
        "smalltalk": ("""
| n saldo |

n := stdin nextLine trimBoth asNumber.

saldo := 0.
saldo := saldo + n.
saldo := saldo + n.

Transcript show: 'saldo=', saldo printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk tiene la regla más simple y más tajante de toda
esta página, y **no hace falta ninguna palabra clave para expresarla**:

> **Todas las variables de instancia son privadas. Todos los métodos son públicos. Siempre.**

No hay `private`, no hay `public`, no hay `protected`. Un objeto **no puede** acceder a las variables
de otro, ni siquiera de la misma clase: tiene que enviarle un mensaje.

```smalltalk
Cuenta >> depositar: x
    saldo := saldo + x.          "saldo es MÍO"

Cuenta >> sumarA: otraCuenta
    otraCuenta saldo             "tengo que PREGUNTARLE, no puedo mirar"
```

Compara con Java o C++, donde un método puede acceder a los campos privados **de otra instancia de su
misma clase**. En Smalltalk eso es imposible, y esa restricción refuerza el paso de mensajes como
único mecanismo de comunicación — la idea de Alan Kay de la clase 043.

Que **todos los métodos sean públicos** parece una carencia y es coherente: si la privacidad de un
método fuera una barrera, sería una barrera al envío de mensajes, que es lo único que hay. La
convención es marcar los internos poniéndolos en una **categoría llamada `private`** en el navegador —
organización, no protección.

Y es la misma postura que Python y Lisp: **la privacidad es una indicación de diseño**. Ese consenso
entre tres lenguajes muy distintos, frente al de Java y C++, es una de las divisiones más nítidas del
diseño de lenguajes.
"""),
    },
)

# ---------------------------------------------------------------------------
# 088 — Importar, exportar y organizar un proyecto
# ---------------------------------------------------------------------------
SPECS["088"] = dict(
    gancho="""
El valor absoluto, calculado por algo que vive en otro sitio. La última clase de la Parte 5 cierra el
recorrido: **cómo se junta el trabajo de varias personas en un solo programa**. Y la respuesta separa
a estos lenguajes en dos épocas: los que **copian texto** —`COPY`, `%INCLUDE`, `#include`— y los que
**enlazan unidades compiladas con su interfaz comprobada**.
""",
    porque="""
Aquí el concepto es la **organización de un proyecto**, y estos lenguajes lo enseñan porque cargan con
la solución antigua y con la moderna a la vez. **COBOL con `COPY`**, **PL/I con `%INCLUDE`** y **C++
con `#include`** son sustitución textual: sin comprobación entre unidades, con recompilación en
cascada y con el orden importando.

Enfrente, **Ada con `with`**, **Fortran con `use`**, **Pascal con `uses`** y **RPG con los directorios
de enlace** compilan cada unidad por separado y **comprueban que encajen**. Ada lo hacía en 1983 y
C++ lo consiguió en 2020.
""",
    cierre="""
Lo transferible: **la unidad de reutilización determina la arquitectura**. Si compartir código es
copiar texto, la unidad natural es el fichero y los proyectos acaban con cientos de cabeceras
interdependientes. Si es una unidad compilada con interfaz, la unidad natural es el módulo y las
dependencias se ven. Y si además hay un gestor de paquetes —`fpm`, Alire, Quicklisp, CPAN, vcpkg— la
unidad pasa a ser la **biblioteca versionada**. Los tres niveles conviven hoy en casi todos estos
lenguajes, y saber en cuál estás explica por qué tu compilación tarda lo que tarda.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. ABSOLUTO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9) COMP-3.
01  R       PIC 9(9)  COMP-3.
01  ED-R    PIC Z(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N

    COMPUTE R = FUNCTION ABS(N)

    MOVE R TO ED-R
    DISPLAY "abs=" FUNCTION TRIM(ED-R)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** COBOL tiene **dos formas de reutilizar**, y son de naturalezas
opuestas.

**`COPY`** es **inclusión textual** en tiempo de compilación, como el `#include` de C:

```cobol
COPY CLIENTE.
COPY CLIENTE REPLACING ==:PRE:== BY ==CLI==.
```

Comparte **definiciones de datos**, y su versión con `REPLACING` es el genérico de los pobres de la
clase 078. Sus problemas son los conocidos: cambiar un copybook obliga a **recompilar todos los
programas que lo usan**, y nadie garantiza que se haga.

Ese es un problema operativo serio en un sistema con miles de programas, y la solución es una
herramienta de gestión de dependencias —IBM Dependency Based Build, Endevor, Changeman— que mantiene
un **grafo de qué programa usa qué copybook** y decide qué recompilar. Es un `make` para mainframe, y
lleva funcionando décadas.

**`CALL`** es lo contrario: enlaza con un programa **compilado por separado**, y puede ser estático
—resuelto al enlazar— o dinámico —resuelto al ejecutar, clase 085—. Cambiar un subprograma llamado
dinámicamente **no obliga a recompilar a sus clientes**.

Esa distinción define la arquitectura de un sistema COBOL: **los datos se comparten por texto y el
código por enlace**. Y explica por qué los copybooks se tratan con tanto cuidado: son la única
dependencia que se propaga a la compilación.
"""),
        "fortran": ("""
module matematicas
   implicit none
   private
   public :: valor_absoluto

contains

   pure function valor_absoluto(x) result(r)
      integer, intent(in) :: x
      integer :: r
      r = abs(x)
   end function valor_absoluto

end module matematicas


program absoluto
   use matematicas, only: valor_absoluto     ! importación SELECTIVA
   implicit none
   integer :: n

   read(*, *) n
   write(*, '(A,I0)') 'abs=', valor_absoluto(n)
end program absoluto
""", """
**Lo que esta clase enseña en Fortran.** `use modulo, only: nombre` es la importación de Fortran, y la
cláusula **`only`** es la práctica recomendada: importa **solo lo que se usa**, y la dependencia queda
documentada en la propia línea.

Y hay una forma más, para resolver colisiones:

```fortran
use matematicas, only: mi_abs => valor_absoluto    ! RENOMBRA al importar
use otro_modulo, only: valor_absoluto
```

El operador `=>` renombra, así que dos módulos con el mismo nombre pueden convivir. Es lo mismo que
`as` en Python y `use x as y` en Rust.

Lo que distingue a Fortran en esta clase es una consecuencia práctica de los módulos: **el orden de
compilación importa**. Un módulo tiene que estar compilado antes que quien lo usa, porque el
compilador genera un fichero `.mod` con su interfaz que el cliente necesita leer.

En un proyecto con cien módulos, calcular ese orden a mano es inviable, y de ahí que Fortran tenga un
ecosistema entero de herramientas para deducir el grafo de dependencias —`makedepf90`, y hoy
**`fpm`**, el gestor de paquetes oficial—:

```toml
name = "mi_proyecto"
[dependencies]
stdlib = { git = "https://github.com/fortran-lang/stdlib" }
```

`fpm` deduce el orden solo, compila y gestiona dependencias externas. Que un lenguaje de 1957
consiguiera su gestor de paquetes en 2020 es tarde, y es exactamente el tipo de modernización que esta
sección quiere mostrar.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Absoluto is

   package Matematicas is
      function Valor_Absoluto (X : Integer) return Integer;
   end Matematicas;

   package body Matematicas is
      function Valor_Absoluto (X : Integer) return Integer is
        (if X < 0 then -X else X);
   end Matematicas;

   N : Integer;
begin
   Get (N);

   Put ("abs=");
   Put (Matematicas.Valor_Absoluto (N), Width => 1);
   New_Line;
end Absoluto;
""", """
**Lo que esta clase enseña en Ada.** Ada separa **dos cosas** que en casi todos los lenguajes van
juntas, y esa separación es de las mejores decisiones de su diseño:

```ada
with Ada.Text_IO;        --  DEPENDENCIA: "necesito compilar contra esto"
use  Ada.Text_IO;        --  VISIBILIDAD: "y quiero sus nombres sin cualificar"
```

`with` declara la dependencia y **es lo único que necesita el compilador**. `use` es opcional y solo
afecta a la comodidad de escritura. Se puede tener `with` sin `use` y escribir
`Ada.Text_IO.Put_Line (...)` completo, que es lo que hacen las guías de estilo para código crítico —
porque el sitio de la llamada dice de dónde viene cada cosa.

Compara con `#include` de C++, que hace las dos cosas a la vez y sin control, o con `import` de
Python, donde `from x import *` es la opción desaconsejada.

Y Ada tiene una regla que evita el problema clásico de `use`: **si dos paquetes usados exportan el
mismo nombre, ninguno de los dos es visible** y hay que cualificar. El compilador **se niega** en
lugar de elegir por ti, que es lo contrario de la resolución de sobrecarga de C++.

Sobre la organización, Ada impone una correspondencia estricta que GNAT convierte en regla de
ficheros: `paquete.ads` para la especificación, `paquete.adb` para el cuerpo, y los subpaquetes
jerárquicos con guion — `matematicas-vectores.ads` para `Matematicas.Vectores`.

Y **Alire** (`alr`), el gestor de paquetes moderno, completa el cuadro: `alr with aws` añade una
dependencia, resuelve versiones y compila. Llegó en 2018.
"""),
        "pascal": ("""
program Absoluto;
{$MODE OBJFPC}{$H+}
uses SysUtils, Math;      { unidades: SysUtils para IntToStr, Math para Abs }

var
  N: Integer;

begin
  Read(N);
  WriteLn('abs=', IntToStr(Abs(N)));
end.
""", """
**Lo que esta clase enseña en Pascal.** La cláusula **`uses`** es la importación, y tiene una
propiedad que la distingue de casi todas las demás: **importa TODO lo público de la unidad, sin
selección**.

No hay `uses Math only (Abs)`. Y como consecuencia, **el orden importa**: si dos unidades declaran el
mismo nombre, **gana la última** de la lista.

```pascal
uses UnidadA, UnidadB;    { si las dos declaran Doblar, se usa la de UnidadB }
```

Esa regla —"gana la última"— es sencilla y es una fuente real de errores al añadir una unidad a un
programa grande. La solución es cualificar: `UnidadA.Doblar(x)`.

Y Pascal distingue **dos secciones `uses`**, lo que sí es un acierto:

```pascal
unit Mi;
interface
uses A;          { A es visible para QUIEN USE Mi }
implementation
uses B;          { B es un detalle interno; nadie más lo ve }
```

Poner una dependencia en `implementation` la mantiene privada y **rompe las dependencias circulares**:
dos unidades pueden usarse mutuamente si al menos una lo hace desde `implementation`. Es un mecanismo
que Ada resuelve con `limited with` y que C++ resuelve con declaraciones adelantadas.

El ecosistema moderno lo completa con el **Online Package Manager** de Lazarus y con **fpcupdeluxe**,
y Delphi con **GetIt** — gestores de paquetes que llegaron tarde, como en casi todos los lenguajes de
esta página.
"""),
        "lisp": ("""
(let ((n (read)))
  (format t "abs=~D~%" (abs n)))
""", """
**Lo que esta clase enseña en Common Lisp.** El estándar de Common Lisp **no dice nada sobre ficheros,
compilación ni proyectos**: define `defpackage` para los nombres (clase 086) y nada más. Cómo se
carga el código es problema del entorno.

Esa laguna la llenó **ASDF** (*Another System Definition Facility*), que es el `make` del mundo Lisp:

```lisp
(defsystem "mi-proyecto"
  :depends-on ("alexandria" "cl-ppcre")
  :components ((:file "paquetes")
               (:file "utiles" :depends-on ("paquetes"))
               (:file "principal" :depends-on ("utiles"))))
```

Un fichero `.asd` declara los componentes, sus dependencias y el orden. ASDF calcula el grafo,
recompila lo necesario y lo carga.

Y encima está **Quicklisp**, que resuelve la distribución: `(ql:quickload "cl-ppcre")` descarga,
compila y carga una biblioteca y todas sus dependencias.

Lo interesante es la separación en tres capas, que Lisp hace más explícita que nadie:

| Capa | Qué resuelve | En Lisp |
|---|---|---|
| Espacio de nombres | Colisión de nombres | `defpackage` (en el lenguaje) |
| Sistema de construcción | Orden y compilación | ASDF (biblioteca) |
| Gestor de paquetes | Distribución y versiones | Quicklisp (externo) |

En Python son `import`, `setuptools` y `pip`; en Rust, `mod`, `cargo build` y `crates.io`. Lo que en
Rust es una sola herramienta, en Lisp son tres piezas independientes — con la ventaja de que se pueden
sustituir por separado, y el inconveniente de que hay que conocer las tres.
"""),
        "tcl": ("""
namespace eval ::matematicas {
    namespace export valor_absoluto
    proc valor_absoluto {x} { return [expr {abs($x)}] }
}

namespace import ::matematicas::valor_absoluto     ;# importar al espacio actual

gets stdin linea
set n [string trim $linea]

puts "abs=[valor_absoluto $n]"
""", """
**Lo que esta clase enseña en Tcl.** Tcl separa con claridad **la carga** de **la visibilidad**, igual
que Ada separa `with` de `use`:

```tcl
package require http 2.9          ;# CARGAR, con requisito de VERSIÓN
namespace import ::http::*        ;# hacer visibles sus nombres aquí
```

`package require` busca el paquete en la ruta de bibliotecas, comprueba la versión y lo carga **una
sola vez**. Y el mecanismo que lo hace posible es el **índice de paquetes**:

```tcl
# pkgIndex.tcl -- generado automáticamente
package ifneeded http 2.9.5 [list source [file join $dir http.tcl]]
```

`package ifneeded` registra **cómo cargar** un paquete sin cargarlo. Tcl solo ejecuta ese guion si
alguien lo pide, así que un directorio con doscientos paquetes se indexa sin cargar ninguno. Es carga
perezosa a nivel de proyecto, y funciona desde 1996.

Y `namespace import` copia **los nombres exportados** al espacio actual, con la posibilidad de
renombrar:

```tcl
namespace import ::matematicas::valor_absoluto
namespace import {*}[namespace children ::plugins]
namespace forget ::matematicas::*                  ;# deshacer la importación
```

`namespace forget` no tiene equivalente en la mayoría de los lenguajes: **retira** una importación. En
un intérprete vivo, donde el estado persiste entre cargas, poder deshacer importa.

Para la distribución, el ecosistema tiene **teapot** y **TEA** (*Tcl Extension Architecture*), y los
**Starkits** de la clase 041 permiten empaquetar aplicación, intérprete y paquetes en un solo fichero
ejecutable.
"""),
        "perl": ("""
use strict;
use warnings;

package Matematicas;
sub valor_absoluto { return abs($_[0]) }

package main;

my $n = <STDIN>;
chomp $n;

print "abs=", Matematicas::valor_absoluto($n), "\\n";
""", """
**Lo que esta clase enseña en Perl.** Como se vio en la clase 086, **`use` es `require` más `import`**,
y esa segunda mitad es lo que hace peculiar a Perl: **`import` es un método normal que el módulo
define**.

```perl
use Mi::Modulo qw(foo bar);
#  equivale a:
#  BEGIN { require Mi::Modulo; Mi::Modulo->import('foo', 'bar'); }
```

El módulo decide qué hacer con esos argumentos. Casi todos heredan de **`Exporter`**:

```perl
package Matematicas;
use Exporter 'import';
our @EXPORT_OK = qw(valor_absoluto);      # se exportan si se piden
our @EXPORT    = qw();                     # se exportan SIEMPRE (desaconsejado)
our %EXPORT_TAGS = (todo => [@EXPORT_OK]); # grupos: use X qw(:todo)
```

La distinción entre `@EXPORT` y `@EXPORT_OK` es la lección: **`@EXPORT` contamina el espacio del
cliente sin que lo pida**, y la práctica moderna es dejarlo vacío y usar solo `@EXPORT_OK`.

Y el ecosistema es la aportación histórica de Perl a esta clase: **CPAN**, de 1995, fue **el primer
gran repositorio de módulos de la historia**, y el modelo del que salieron PyPI, npm, RubyGems y
crates.io.

Lo que CPAN tiene y casi ningún otro ecosistema ha replicado es **CPAN Testers**: una red de
voluntarios que ejecuta automáticamente la batería de pruebas de cada módulo en **decenas de
combinaciones** de sistema operativo y versión de Perl, y publica los resultados. Antes de instalar
algo se puede consultar si pasa en tu plataforma exacta.

Para fijar versiones por proyecto están `cpanfile` y **Carton**, el equivalente de un *lockfile*.
"""),
        "cpp": ("""
#include <cstdlib>
#include <iostream>

namespace matematicas {
    int valor_absoluto(int x) { return std::abs(x); }
}

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "abs=" << matematicas::valor_absoluto(n) << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** `#include` es **sustitución textual**, y durante cuarenta años ha
sido la única forma de compartir código en C y C++. Sus consecuencias, ya apuntadas en la clase 086,
son medibles: un `.cpp` que incluya `<iostream>` compila decenas de miles de líneas.

De ahí una colección entera de técnicas que existen **solo** para mitigar el `#include`:

```cpp
#pragma once                     // guardas de inclusión
class Widget;                    // declaración adelantada: evita incluir la cabecera
class Impl;                      // modismo PIMPL: ocultar la implementación
// unity builds, cabeceras precompiladas, include-what-you-use...
```

**Los módulos de C++20** resuelven el problema de raíz —una unidad compilada, importada ya
analizada— y su adopción avanza despacio porque exige que el sistema de construcción entienda el
grafo de dependencias entre módulos, que no se puede deducir del texto tan fácilmente.

Y el ecosistema es la otra mitad de esta clase. C++ estuvo **treinta años sin gestor de paquetes**, y
hoy hay dos que compiten:

```bash
vcpkg install fmt          # Microsoft, orientado a bibliotecas del sistema
conan install .            # con perfiles y binarios precompilados
```

Que llegaran tan tarde explica una peculiaridad cultural del mundo C++: **la costumbre de incluir las
dependencias como submódulos de Git o de copiarlas al repositorio**, que en Rust o Node sería
impensable.

Y `std::abs` para enteros está en `<cstdlib>`, no en `<cmath>` — un detalle heredado de C que sigue
sorprendiendo.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi ABSOLUTO;
  n int(10) const;
end-pi;

dcl-s salida char(30);

salida = 'abs=' + %char(valorAbsoluto(n));
dsply salida;

*inlr = *on;
return;

// En un proyecto real: otro módulo con `export`, enlazado en un
// PROGRAMA DE SERVICIO y localizado por un DIRECTORIO DE ENLACE.
dcl-proc valorAbsoluto;
  dcl-pi *n int(10);
    x int(10) const;
  end-pi;
  return %abs(x);
end-proc;
""", """
**Lo que esta clase enseña en RPG.** La organización de un proyecto en IBM i tiene cuatro piezas que
ya aparecieron en la clase 086, y aquí se ven en su papel de "importar":

1. **`/COPY` o `/INCLUDE`** — inclusión **textual** de prototipos, como el `COPY` de COBOL. Es como se
   comparten las declaraciones `dcl-pr`.
2. **Módulo** — la unidad compilada.
3. **Programa de servicio** — la biblioteca dinámica.
4. **Directorio de enlace** (`*BNDDIR`) — **dónde buscar** lo que falte al enlazar.

La cuarta es la que hace de "ruta de búsqueda": se declara en el propio fuente y el enlazador la
consulta.

```rpgle
ctl-opt bnddir('MIAPP/UTILES');
/include qrpgleref,prototipos
```

Con eso, `valorAbsoluto` se resuelve automáticamente en el programa de servicio correspondiente, sin
enumerar módulos.

Y hay una diferencia importante con casi todos los lenguajes de esta página: **el enlace por defecto
es dinámico**. Un programa de servicio se carga en tiempo de ejecución y se **comparte entre todos los
trabajos** que lo usen. Corregir un error es recompilar el programa de servicio; **los programas que
lo llaman no se tocan**, siempre que la firma de la clase 086 no cambie.

Esa propiedad —actualizar una biblioteca sin recompilar a sus clientes, con verificación de firma al
cargar— es exactamente lo que en Linux dan los `soname`, y en IBM i está integrada en el sistema desde
1993.

El ecosistema moderno añade Git, **`bob`** para construcción reproducible y **`iproj.json`** para
declarar la estructura del proyecto desde VS Code.
"""),
        "pli": ("""
 absoluto: procedure options(main);

    declare n fixed binary(31);

    get list (n);
    put skip list ('abs=' || trim(char(valor_absoluto(n))));

 valor_absoluto: procedure (x) returns (fixed binary(31));
    declare x fixed binary(31);
    return (abs(x));
 end valor_absoluto;

 end absoluto;
""", """
**Lo que esta clase enseña en PL/I.** PL/I organiza un proyecto con las dos herramientas de su época,
y las dos son las antiguas:

**`%INCLUDE`** para las declaraciones —inclusión textual, con todos los problemas del `COPY` de COBOL
y del `#include` de C—:

```pli
%include declaraciones;
%include registro_cliente;
```

Y **procedimientos externos** enlazados por nombre, sin comprobación de firma entre unidades. Si un
programa declara `entry (fixed binary(31))` y el procedimiento real espera `fixed decimal(15,2)`, el
enlazador **empareja los nombres igualmente** y el resultado es corrupción de datos.

Esa es la carencia que Ada resolvió en 1983 con la comprobación entre unidades de compilación, y es
uno de los argumentos más fuertes a favor de los módulos.

Lo que sí tiene el mundo PL/I, y compensa parte del problema, es la infraestructura del mainframe: los
**gestores de cambio** —Endevor, Changeman, IBM DBB— mantienen el grafo de dependencias entre fuentes
e includes, y recompilan en cascada lo que haga falta. Es un sistema de construcción externo al
lenguaje, y lleva funcionando desde los 80.

El preprocesador de PL/I merece una nota final, porque va mucho más allá de `%INCLUDE`: tiene
**variables, condicionales, bucles y procedimientos propios**, ejecutados en tiempo de compilación.

```pli
%declare depurar fixed;
%depurar = 1;
%if depurar = 1 %then %do;
   put skip list ('traza');
%end;
```

Es un lenguaje completo dentro del lenguaje, y es el antepasado directo de la metaprogramación por
preprocesador — con las mismas virtudes y los mismos abusos que hoy se le reprochan al de C.
"""),
        "mumps": ("""
ABSOLUTO ; Importar y organizar -- clase 088
 read n
 write "abs=", $$abs^ABSOLUTO(n), !
 quit
 ;
abs(x) ; valor absoluto
 quit $select(x<0 : -x, 1 : x)
""", """
**Lo que esta clase enseña en M.** **M no tiene importación.** No hay `import`, `use`, `require` ni
`with`: **todas las rutinas del entorno son visibles desde cualquier rutina**, y se invocan con
`ETIQUETA^RUTINA`.

```mumps
 do PROCESAR^FACTURA(id)
 set x = $$CALCULAR^UTIL(a, b)
```

El `^` separa la etiqueta del nombre de la rutina, y no hace falta declarar nada. Es el modelo más
simple posible, y tiene el problema de la clase 086: **un único espacio de nombres global** para todo
el sistema.

Y sin embargo hay una propiedad que compensa parcialmente y que conviene entender: **la carga es
automática y perezosa**. La primera vez que se ejecuta `do X^Y`, el sistema busca `Y`, la carga en el
área de rutinas del proceso y la ejecuta. No hay fase de enlace, no hay ejecutable y **no hay
recompilación en cascada**: corregir una rutina afecta a todo el sistema **en la siguiente llamada**.

Eso hace que el despliegue en M sea trivial —copiar una rutina y ya está— y explica que los sistemas
de M lleven décadas sin reiniciarse.

El ecosistema moderno ha añadido lo que faltaba: **YottaDB tiene un gestor de paquetes** y una
estructura de proyecto con directorios de rutinas y variables de entorno (`$ZROUTINES`) que definen la
ruta de búsqueda — algo parecido a un `PATH` para código.

Y en **VistA**, la distribución tiene su propio nombre y su propio formato: los **KIDS builds**
(*Kernel Installation and Distribution System*), que empaquetan rutinas, definiciones de FileMan y
guiones de instalación en un fichero que se despliega en cientos de hospitales. Es un gestor de
paquetes de dominio específico, construido sobre un lenguaje que no tiene ninguno.
"""),
        "smalltalk": ("""
| n |

n := stdin nextLine trimBoth asNumber.

Transcript show: 'abs=', n abs printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** **En Smalltalk no se importa nada.** Todas las clases del
sistema están siempre disponibles en el diccionario `Smalltalk`, así que `n abs` funciona sin
declarar ninguna dependencia.

Eso es consecuencia directa del modelo de **imagen** de la clase 041: no hay ficheros que enlazar
porque **todo el sistema ya está cargado y vivo**. La pregunta "¿de dónde viene esta clase?" se
responde con una herramienta, no con una línea de código.

Y ahí está el problema que la comunidad tardó veinte años en resolver: **si no hay dependencias
declaradas, ¿cómo se distribuye un proyecto?** La imagen es un binario de cientos de megas con todo
mezclado.

La respuesta es una pila de herramientas que hoy funciona bien:

| Herramienta | Qué resuelve |
|---|---|
| **Monticello** | Versionado de paquetes; el "commit" de Smalltalk |
| **Metacello** | **Declaración de dependencias y versiones**, el `package.json` |
| **Tonel** | Guardar el código como **ficheros de texto** legibles por Git |
| **Iceberg** | Integración con Git y GitHub desde dentro de la imagen |

Una especificación de Metacello se parece bastante a lo que se espera hoy:

```smalltalk
spec baseline: 'MiProyecto' with: [
    spec repository: 'github://usuario/proyecto:main/src' ].
```

Y **Tonel** es la pieza decisiva: convirtió el código de Smalltalk en ficheros de texto, uno por
clase, y con eso lo hizo compatible con Git, con las revisiones por *pull request* y con la
integración continua.

Es la respuesta a la crítica más justificada que recibió Smalltalk durante décadas —"no encaja en un
flujo moderno"— y llegó, como tantas cosas de esta sección, mucho después de que el lenguaje se diera
por muerto.
"""),
    },
)
