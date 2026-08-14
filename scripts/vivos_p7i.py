# -*- coding: utf-8 -*-
"""Parte 7, lote I — clase 115. Ver `vivos_parte7.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 115 — Funcional II: composición, currying y aplicación parcial
# ---------------------------------------------------------------------------
SPECS["115"] = dict(
    gancho="""
Doblar y luego sumar uno, pero **construyendo una función nueva** en lugar de llamarlas en fila. Aquí
se separa de verdad quién tiene funciones de primera clase y quién no, porque componer exige algo más
que pasarlas: **exige poder DEVOLVER una función**. Y ahí caen cinco de estos doce: **Fortran, Ada,
Pascal, PL/I y RPG pueden pasar procedimientos y no pueden fabricar uno nuevo**.
""",
    porque="""
Aquí el concepto es la **función como resultado**, y estos lenguajes lo enseñan porque marcan la
frontera exacta. Para componer hace falta una **clausura**: una función que capture `f` y `g` y viva
después de que termine quien la creó (clase 083). **Lisp, Perl, Tcl, C++11 y Smalltalk la tienen**;
Fortran, Ada, Pascal y PL/I tienen punteros a procedimiento **sin entorno capturado**, y con eso se
puede seleccionar una función, no construirla.

Y el *currying* lleva la idea al final: **una función de dos argumentos es una función que devuelve
una función de uno**. Es la idea de Schönfinkel (1924) y Curry (1930), anterior a todos estos
lenguajes.
""",
    cierre="""
Lo transferible: **componer y aplicar parcialmente son la forma funcional de crear abstracciones sin
escribir código nuevo**. `filtrar(mayor_que(100))` dice más que un bucle con un `if`, y no hay que
declarar nada. El límite práctico es el de siempre: **una cadena de cinco composiciones es elegante
para quien la escribió y un jeroglífico a los seis meses**. La regla que funciona es dar nombre a las
composiciones intermedias — que es exactamente lo que dice la clase 109 sobre extraer funciones.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. FUNC2.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9)  COMP-3.
01  X       PIC S9(18) COMP-3.
01  ED-R    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    MOVE N TO X
    PERFORM DOBLAR
    PERFORM INCREMENTAR

    MOVE X TO ED-R
    DISPLAY "resultado=" FUNCTION TRIM(ED-R)
    STOP RUN.

DOBLAR.
    COMPUTE X = X * 2.

INCREMENTAR.
    COMPUTE X = X + 1.
""", """
**Lo que esta clase enseña en COBOL.** COBOL **no puede componer funciones**, y la razón es la de la
clase 085: no tiene funciones de primera clase, así que menos aún puede devolver una.

Lo que hace este programa es lo único posible: **encadenar dos párrafos sobre una variable
compartida**. Y esa es una diferencia conceptual, no de sintaxis: `PERFORM DOBLAR` seguido de
`PERFORM INCREMENTAR` **no construye nada nuevo** — ejecuta dos efectos sobre `X` en orden.

La composición de COBOL existe, y está un nivel más arriba: **en la cadena de trabajos**.

```text
//PASO1 EXEC PGM=DOBLAR
//SALIDA DD DSN=TMP.PASO1,DISP=(NEW,PASS)
//PASO2 EXEC PGM=INCREM,COND=(0,NE,PASO1)
//ENTRADA DD DSN=TMP.PASO1,DISP=(OLD,DELETE)
```

Eso es JCL, y es **composición de funciones a escala de proceso**: la salida del primer programa es la
entrada del segundo, con `COND` decidiendo si el segundo se ejecuta según cómo terminara el primero.

Y merece verse por lo que es: **cada paso es una función pura sobre ficheros** (clase 114), y el
trabajo entero es su composición. Un planificador —Control-M, IBM Workload Scheduler— compone cientos
de esos pasos en grafos de dependencias.

Quien conozca las tuberías de Unix, los *pipelines* de CI o los grafos de tareas de Airflow reconocerá
la estructura. **El mainframe compone en la capa de trabajos lo que un lenguaje funcional compone en
la capa de expresiones**, y por la misma razón: para que cada pieza se pueda razonar y repetir por
separado.

Dentro del lenguaje, lo más cercano a la aplicación parcial es el `CALL` con una tabla de parámetros
preparada de antemano, y es forzar mucho la comparación. **COBOL compone procesos, no funciones**, y
en su dominio eso ha resultado ser lo útil.
"""),
        "fortran": ("""
program func2
   implicit none

   abstract interface
      pure function unaria(x) result(r)
         integer, intent(in) :: x
         integer :: r
      end function unaria
   end interface

   procedure(unaria), pointer :: f, g
   integer :: n

   read(*, *) n

   g => doblar             ! seleccionar, no construir
   f => incrementar

   write(*, '(A,I0)') 'resultado=', f(g(n))

contains

   pure function doblar(x) result(r)
      integer, intent(in) :: x
      integer :: r
      r = x * 2
   end function doblar

   pure function incrementar(x) result(r)
      integer, intent(in) :: x
      integer :: r
      r = x + 1
   end function incrementar

end program func2
""", """
**Lo que esta clase enseña en Fortran.** Este programa **selecciona** dos funciones y las aplica en
fila. Lo que **no** puede hacer es escribir esto:

```fortran
h => componer(f, g)          ! IMPOSIBLE en Fortran
```

**Fortran no puede devolver un procedimiento**, y no puede porque no tiene clausuras: un puntero a
procedimiento apunta a **código estático**, no a código más un entorno capturado. Una función
`componer` tendría que fabricar una función nueva que recuerde `f` y `g`, y en Fortran no existe
ningún objeto que pueda hacer eso.

Es la misma frontera que se describió en la clase 083, y aquí es donde muerde.

Lo que sí puede hacer Fortran, y cubre buena parte de los usos, es **pasar procedimientos como
argumentos**:

```fortran
subroutine aplicar(v, f)
   integer, intent(inout) :: v(:)
   procedure(unaria) :: f
   integer :: i
   do i = 1, size(v)
      v(i) = f(v(i))
   end do
end subroutine
```

Ese es el mecanismo con el que las bibliotecas numéricas reciben la función objetivo: **los
integradores, los optimizadores y los solucionadores de ecuaciones diferenciales toman el
procedimiento del usuario como argumento**.

```fortran
call dqags(mi_funcion, a, b, ...)      ! QUADPACK: integración numérica
call lbfgs(n, x, f, g, ...)             ! optimización
```

Y ahí aparece un problema clásico de Fortran que la aplicación parcial resolvería y que hay que
resolver de otra forma: **cómo pasarle datos extra a esa función**.

La respuesta histórica fue un `COMMON` con los parámetros —lo que impedía usar la biblioteca desde dos
sitios a la vez—. La moderna es más limpia:

```fortran
module problema
   real :: parametros(10)          ! estado del módulo
contains
   pure function objetivo(x) result(r) ... end function
end module
```

O, desde Fortran 2003, un argumento `class(*)` que la biblioteca pasa de vuelta sin mirarlo —el
`void*` de contexto de las APIs de C—.

Es exactamente el problema que una clausura resuelve sola, y en Fortran cuesta un módulo.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Func2 is
   type Unaria is access function (X : Integer) return Integer;

   function Doblar (X : Integer) return Integer is (X * 2);
   function Incrementar (X : Integer) return Integer is (X + 1);

   F : constant Unaria := Incrementar'Access;
   G : constant Unaria := Doblar'Access;

   N : Integer;
begin
   Get (N);

   Put ("resultado=");
   Put (F (G (N)), Width => 1);     --  composición a mano: Ada no la fabrica
   New_Line;
end Func2;
""", """
**Lo que esta clase enseña en Ada.** Como Fortran, **Ada puede seleccionar funciones y no puede
fabricarlas**. Un `access function` apunta a un subprograma que existe en el código; no hay forma de
crear uno nuevo en ejecución.

Y la razón, ya explicada en la clase 083, es la **comprobación de accesibilidad**: Ada garantiza que
un acceso a subprograma nunca sobrevive al ámbito donde ese subprograma vive. Una clausura devuelta
por `componer` **violaría exactamente esa garantía**, y el lenguaje lo rechaza en compilación.

Es una decisión coherente: Ada prefiere prohibir algo útil antes que permitir un puntero colgante.

Lo que Ada ofrece en su lugar, y es el patrón idiomático, son los **genéricos con parámetros formales
de subprograma** (clase 078):

```ada
generic
   with function F (X : Integer) return Integer;
   with function G (X : Integer) return Integer;
function Componer (X : Integer) return Integer;

function Componer (X : Integer) return Integer is (F (G (X)));

function Doblar_Y_Sumar is new Componer (F => Incrementar, G => Doblar);
```

Eso **es** composición: `Doblar_Y_Sumar` es una función nueva construida a partir de dos. La
diferencia es decisiva y merece verla clara:

- **Se resuelve en compilación**, no en ejecución.
- **No hay indirección**: el compilador puede integrar todo en línea.
- **Las combinaciones posibles están todas escritas en el código.**

Es composición estática, y para lo que Ada hace —sistemas donde todo debe ser predecible y acotado— es
lo correcto: **no se puede fabricar una función que nadie previó, y eso es una propiedad, no una
carencia**.

Y para la aplicación parcial, Ada tiene los **valores por defecto de parámetro** con asociación por
nombre (clase 109), que cubren muchos de sus usos prácticos:

```ada
procedure Dibujar (X, Y : Integer; Color : Tipo_Color := Negro; Grosor : Natural := 1);
Dibujar (10, 20, Grosor => 3);
```

No es aplicación parcial —no crea una función nueva— y resuelve el mismo problema cotidiano: **fijar
unos argumentos y dejar otros**.
"""),
        "pascal": ("""
program Func2;
{$MODE OBJFPC}{$H+}
uses SysUtils;

type
  TUnaria = function(X: Integer): Integer;

function Doblar(X: Integer): Integer;
begin
  Result := X * 2;
end;

function Incrementar(X: Integer): Integer;
begin
  Result := X + 1;
end;

var
  F, G: TUnaria;
  N: Integer;

begin
  Read(N);

  G := @Doblar;
  F := @Incrementar;

  WriteLn('resultado=', IntToStr(F(G(N))));
end.
""", """
**Lo que esta clase enseña en Pascal.** Con **tipos procedimentales sueltos**, Pascal está donde
Fortran y Ada: selecciona funciones, no las fabrica.

Con **`reference to function`** —las funciones anónimas de Delphi 2009 y Free Pascal 3.2— la cosa
cambia por completo, porque eso **sí es una clausura**:

```pascal
type
  TUnaria = reference to function(X: Integer): Integer;

function Componer(F, G: TUnaria): TUnaria;
begin
  Result := function(X: Integer): Integer
            begin
              Result := F(G(X));      { CAPTURA F y G }
            end;
end;

var H: TUnaria;
begin
  H := Componer(Incrementar, Doblar);
  WriteLn(H(5));                        { 11 }
end;
```

Eso es composición de verdad: `Componer` **devuelve una función nueva** que recuerda `F` y `G`.

Y el detalle de implementación importa, porque explica por qué llegó tan tarde: **una `reference to
function` es un objeto con conteo de referencias** (clase 103). El compilador genera una clase oculta
con los valores capturados como campos y el cuerpo como método. Es exactamente lo que hacen C#, Java
con las clases anónimas y C++ con el tipo de la lambda.

Es decir: **Pascal tuvo que tener objetos con conteo de referencias antes de poder tener clausuras**.
Los tipos procedimentales de 1989 no podían llegar ahí.

Y la aplicación parcial se escribe igual de directa:

```pascal
function Sumar(A: Integer): TUnaria;
begin
  Result := function(B: Integer): Integer
            begin Result := A + B end;
end;

Incrementar := Sumar(1);
```

`Sumar(1)` devuelve **una función que suma uno**. Eso es *currying*, en Pascal.

Merece señalar el contraste con las otras dos filas de esta página: **Pascal es el único de la familia
Wirth-Ada que cruzó la frontera**, y lo hizo por presión del ecosistema Delphi, que necesitaba
manejadores de eventos y programación asíncrona con estado capturado.
"""),
        "lisp": ("""
(defun componer (f g)
  (lambda (x) (funcall f (funcall g x))))      ; DEVUELVE una función nueva

(let* ((doblar      (lambda (x) (* 2 x)))
       (incrementar (lambda (x) (+ x 1)))
       (h (componer incrementar doblar))
       (n (read)))
  (format t "resultado=~D~%" (funcall h n)))
""", """
**Lo que esta clase enseña en Common Lisp.** `componer` **devuelve una lambda que captura `f` y `g`**,
y esa capacidad —crear funciones en ejecución— está en Lisp desde 1958. Es la definición misma de
lenguaje funcional.

Common Lisp tiene además una familia de constructores de funciones en el estándar, y merece verse
porque muchos lenguajes no la tienen:

```lisp
(complement #'evenp)            ; la función NEGADA
(constantly 42)                  ; siempre devuelve 42
(identity x)
(apply #'+ lista)                 ; aplicar a una LISTA de argumentos
(multiple-value-call #'+ (floor 7 2))   ; encadenar VALORES MÚLTIPLES
```

Y lo que Common Lisp **no** trae, y sorprende, es `compose` y `curry`. Están en **Alexandria**, la
biblioteca de utilidades de facto:

```lisp
(ql:quickload :alexandria)
(alexandria:compose #'1+ (lambda (x) (* 2 x)))
(alexandria:curry #'+ 10)          ; una función que suma 10
(alexandria:rcurry #'- 3)           ; que RESTA 3 (fija el argumento derecho)
```

`rcurry` —fijar los argumentos por la derecha— es una distinción que casi ningún lenguaje hace y que
importa cuando el orden de los parámetros no ayuda.

Y esta clase es el sitio para nombrar la idea original: el ***currying*** se llama así por **Haskell
Curry**, y quien lo describió primero fue **Moses Schönfinkel en 1924** — antes de que existieran los
ordenadores. La demostración es que **cualquier función de n argumentos equivale a n funciones de un
argumento**, y de ahí que en Haskell y ML **todas** las funciones sean de un argumento.

En Lisp no es así: una función tiene su aridad, y currificar es explícito. Es una elección
pragmática, y tiene una ventaja concreta: **`(+ 1 2 3)` con aridad variable es imposible en un
lenguaje currificado por defecto**.

Y con macros, componer se puede hacer sin coste en ejecución:

```lisp
(defmacro -> (x &rest formas)          ; el "threading macro" de Clojure
  (reduce (lambda (acc f) `(,(car f) ,acc ,@(cdr f))) formas :initial-value x))

(-> n (* 2) (+ 1))                      ; se EXPANDE a (+ (* n 2) 1)
```

Eso genera el código compuesto **en tiempo de compilación**: la elegancia de la composición sin la
indirección. Es lo que Clojure popularizó con `->` y `->>`, y en Common Lisp son cinco líneas.
"""),
        "tcl": ("""
proc componer {f g} {
    #  devuelve un PREFIJO DE COMANDO con f y g ya fijados
    return [list apply {{f g x} { {*}$f [{*}$g $x] }} $f $g]
}

set doblar      [list apply {{x} { expr {$x * 2} }}]
set incrementar [list apply {{x} { expr {$x + 1} }}]

set h [componer $incrementar $doblar]

gets stdin linea
set n [string trim $linea]

puts "resultado=[{*}$h $n]"
""", """
**Lo que esta clase enseña en Tcl.** El programa usa el idioma más característico de Tcl para esto: el
**prefijo de comando** de la clase 085.

```tcl
return [list apply {{f g x} { ... }} $f $g]
```

Eso construye **una lista** cuyo primer elemento es `apply`, seguido de la lambda y de `$f` y `$g` ya
fijados. Al invocarla con `{*}$h $n`, la lista se expande y `$n` va al final: **los dos primeros
argumentos ya estaban puestos**.

Eso **es aplicación parcial**, y en Tcl no necesita ninguna característica del lenguaje: **basta con
que un comando sea una lista y que se pueda expandir con `{*}`**.

`{*}` merece un momento, porque es de las adiciones más importantes de Tcl 8.5 (2007): **expande una
lista en argumentos separados**. Antes había que usar `eval` con las comillas correctas, que era
frágil y una fuente clásica de fallos de citación.

```tcl
{*}$cmd $arg              ;# expande: cada elemento es un argumento
eval $cmd [list $arg]      ;# el idioma antiguo, delicado
```

Y con eso, la aplicación parcial es simplemente **añadir elementos a una lista**:

```tcl
set sumar10 [list ::tcl::mathop::+ 10]
{*}$sumar10 5                            ;# 15
lappend sumar10 5                         ;# ir acumulando argumentos
```

Es tan directo que en Tcl no hay una función `curry`: **no hace falta**.

Tcl tiene además `interp alias`, que crea un comando nuevo con argumentos prefijados **a nivel del
intérprete**:

```tcl
interp alias {} sumar10 {} ::tcl::mathop::+ 10
sumar10 5                                 ;# 15
```

Eso crea un comando de verdad, invocable por nombre, con parte de sus argumentos fijados. Es
aplicación parcial que produce **una entrada en la tabla de comandos**, no un valor — y por eso
sobrevive y se puede usar desde cualquier sitio.

Es un ejemplo más de la coherencia del modelo: en Tcl, componer funciones es manipular listas, y
registrar una composición es crear un comando.
"""),
        "perl": ("""
use strict;
use warnings;

sub componer {
    my ($f, $g) = @_;
    return sub { return $f->($g->(@_)) };      # CLAUSURA sobre $f y $g
}

my $doblar      = sub { $_[0] * 2 };
my $incrementar = sub { $_[0] + 1 };

my $h = componer($incrementar, $doblar);

my $n = <STDIN>;
chomp $n;

print "resultado=", $h->($n), "\\n";
""", """
**Lo que esta clase enseña en Perl.** `componer` devuelve una clausura que captura `$f` y `$g`, y eso
funciona en Perl **desde 1994**, cuando llegaron las referencias (clase 097).

La aplicación parcial se escribe igual de directa:

```perl
sub sumar { my $a = shift; return sub { $a + shift } }
my $incrementar = sumar(1);
print $incrementar->(5);          # 6
```

Y Perl tiene una construcción para esto que es peculiar y muy suya: **los prototipos de subrutina con
`&`**, que permiten escribir funciones que **parecen sintaxis del lenguaje**.

```perl
sub aplicar_dos_veces (&$) {
    my ($f, $x) = @_;
    return $f->($f->($x));
}

aplicar_dos_veces { $_[0] * 2 } 5;      # 20  -- SIN sub, sin coma
```

El prototipo `(&$)` dice "el primer argumento es un bloque". Con eso, la llamada se escribe con la
misma forma que `map`, `grep` y `sort`, y esa es la razón de que existan: **permitir que las funciones
de biblioteca se lean como construcciones del lenguaje**.

Es lo que hacen `List::Util` con `first { ... } @lista` y `Try::Tiny` con `try { ... } catch { ... }`.

Y CPAN cubre el resto con módulos que son de los más elegantes del ecosistema:

```perl
use Sub::Curried;
use List::Util qw(reduce);
use Function::Parameters;

curry add ($x, $y) { $x + $y }
my $inc = add(1);
```

Perl tiene además una función poco conocida que encaja aquí: **`reduce`** de `List::Util`, que usa
`$a` y `$b` como las variables del bloque — las mismas que `sort`:

```perl
my $compuesta = reduce { my ($f, $g) = ($a, $b); sub { $f->($g->(@_)) } } @funciones;
```

Componer una lista arbitraria de funciones en una expresión. Es denso, es correcto, y es exactamente
lo que el cierre de esta clase advierte: **ponle nombre antes de que pasen seis meses**.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    auto doblar      = [](int x) { return x * 2; };
    auto incrementar = [](int x) { return x + 1; };

    //  componer DEVUELVE una lambda que captura f y g
    auto componer = [](auto f, auto g) {
        return [f, g](int x) { return f(g(x)); };
    };

    auto h = componer(incrementar, doblar);

    std::cout << "resultado=" << h(n) << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** Este programa **compone funciones sin coste en ejecución**, y eso
merece explicarse porque es donde C++ gana a casi todos.

`componer` es una lambda genérica (C++14) que **devuelve otra lambda**. Cada lambda tiene un **tipo
único generado por el compilador**, así que `h` tiene un tipo concreto conocido en compilación, y el
compilador **puede integrar todo en línea**: `h(n)` se compila exactamente igual que `n * 2 + 1`.

**Cero indirecciones, cero reservas de memoria, cero coste.**

Si en lugar de `auto` se usara `std::function`, se perdería todo eso (clase 085): habría borrado de
tipo, llamada indirecta y posiblemente una reserva. La palabra `auto` es la que hace que esto sea
gratis.

C++ tiene además herramientas específicas para la aplicación parcial:

```cpp
#include <functional>
auto sumar10 = std::bind(std::plus<int>{}, 10, std::placeholders::_1);
auto sumar10 = [](int x) { return 10 + x; };      // preferido: más claro y más rápido
auto f = std::bind_front(&Clase::metodo, &obj);    // C++20: fijar los PRIMEROS argumentos
```

**`std::bind` es de 2011 y hoy se desaconseja**: los marcadores `_1`, `_2` son crípticos, sus reglas
de captura son sutiles y genera código peor que una lambda. La recomendación universal es usar
lambdas, y `bind_front` para el caso concreto de fijar los primeros argumentos.

Y esta clase conecta con lo que en C++ moderno es una técnica central: **componer con *ranges***
(clase 092).

```cpp
auto resultado = v
    | std::views::filter([](int x) { return x > 0; })
    | std::views::transform([](int x) { return x * 2; })
    | std::views::take(5);
```

El operador `|` **compone vistas perezosas**, y el resultado es un objeto cuyo tipo el compilador
conoce por completo. **No hay contenedores intermedios y no hay indirección**: el bucle final que
recorre `resultado` compila a lo mismo que un bucle escrito a mano con dos `if`.

Es composición funcional con el rendimiento de C, y es probablemente el mejor argumento a favor de las
*ranges* de C++20.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi FUNC2;
  n int(10) const;
end-pi;

// RPG no puede devolver un procedimiento: se encadenan las llamadas
dsply ('resultado=' + %char(incrementar(doblar(n))));

*inlr = *on;
return;

dcl-proc doblar;
  dcl-pi *n int(20);
    x int(10) const;
  end-pi;
  return x * 2;
end-proc;

dcl-proc incrementar;
  dcl-pi *n int(20);
    x int(20) const;
  end-pi;
  return x + 1;
end-proc;
""", """
**Lo que esta clase enseña en RPG.** RPG **no tiene clausuras**, así que no puede fabricar funciones:
`%paddr` (clase 085) selecciona un procedimiento existente, y ya está.

Lo que sí se puede es **componer llamadas anidadas**, como en este programa, y **construir cadenas de
procesamiento con punteros a procedimiento en una tabla**:

```rpgle
dcl-s etapas pointer dim(10);
dcl-s n int(10) inz(0);

etapas(1) = %paddr('DOBLAR');
etapas(2) = %paddr('INCREMENTAR');

valor = entrada;
for i = 1 to n;
  puntero = etapas(i);
  valor = aplicar(valor);       // extproc(puntero)
endfor;
```

Eso es una **tubería configurable en ejecución**: la secuencia de transformaciones está en una tabla y
se puede cambiar sin recompilar. Es lo que la composición de funciones consigue con clausuras, hecho
con datos.

Y donde IBM i compone de verdad es en la capa que ya apareció en las clases 106 y 114: **SQL**.

```sql
select round(avg(importe * 1.21), 2)
  from movimientos
 where estado in (select codigo from estados_validos)
```

Funciones anidadas, subconsultas y agregación compuestas en una expresión declarativa. Y con las
**funciones definidas por el usuario** de Db2 for i, un procedimiento RPG **se convierte en una
función SQL**:

```sql
CREATE FUNCTION calcular_iva(importe DECIMAL(11,2))
  RETURNS DECIMAL(11,2)
  LANGUAGE RPGLE
  EXTERNAL NAME 'MIBIB/CALCIVA'
```

A partir de ahí, `select calcular_iva(total) from facturas` **compone la lógica de negocio escrita en
RPG dentro de una consulta SQL**, y el optimizador la aplica fila a fila.

Es composición entre dos lenguajes y dos paradigmas, y es una de las integraciones más útiles de la
plataforma: **la lógica se escribe una vez en RPG y se usa desde SQL, desde Java y desde cualquier
programa**.
"""),
        "pli": ("""
 func2: procedure options(main);

    declare n fixed binary(31);
    declare f entry (fixed binary(31)) returns (fixed binary(31)) variable;
    declare g entry (fixed binary(31)) returns (fixed binary(31)) variable;

    get list (n);

    g = doblar;              /* seleccionar, no construir */
    f = incrementar;

    put skip list ('resultado=' || trim(char(f(g(n)))));

 doblar: procedure (x) returns (fixed binary(31));
    declare x fixed binary(31);
    return (x * 2);
 end doblar;

 incrementar: procedure (x) returns (fixed binary(31));
    declare x fixed binary(31);
    return (x + 1);
 end incrementar;

 end func2;
""", """
**Lo que esta clase enseña en PL/I.** Las **variables `entry`** de PL/I (clase 085) permiten guardar y
pasar procedimientos desde 1964, y **no permiten crear uno nuevo**: no hay clausuras, así que una
función `componer` no tiene con qué fabricar el resultado.

Lo que PL/I sí tiene, y merece nombrarse en esta clase, es algo que se acerca por un camino
inesperado: **el preprocesador**.

```pli
 %declare componer entry;
 %componer: procedure (f, g) returns (character);
    return ('(' || f || '(' || g || '(X)))');
 %end componer;

 resultado = componer('incrementar', 'doblar');
```

El preprocesador de PL/I —ya mencionado en la clase 088— es **un lenguaje completo con variables,
bucles y procedimientos que se ejecuta en tiempo de compilación** y **genera texto fuente**. Con él se
puede escribir una "función" que construya la composición **como código**, que después el compilador
compila.

Eso es metaprogramación generativa, y consigue el efecto de la composición **sin coste en ejecución**,
igual que la macro `->` de Lisp de esta misma página y que los genéricos de Ada.

Es un patrón real: en los sistemas PL/I grandes, el preprocesador se usa para generar código repetitivo
a partir de definiciones —validaciones de campo, accesos a tablas, conversiones— y es la razón de que
un fuente de 500 líneas pueda compilar 5.000.

Con los mismos problemas que tiene el preprocesador de C, que descienden de aquí: **el código que se
depura no es el que se escribió**, los errores señalan a líneas generadas y las herramientas ven el
texto expandido.

Y merece la observación de fondo, que vale para toda esta clase: **hay dos formas de construir código
nuevo — en ejecución con clausuras, o en compilación con macros**. Lisp tiene las dos, C++ tiene las
dos, PL/I solo la segunda, y Fortran, Ada y RPG ninguna de forma general.
"""),
        "mumps": ("""
FUNC2 ; Funcional II -- clase 115
 read n
 ; composicion por indireccion: los nombres de las etiquetas son datos
 set etapas = "doblar,incrementar"
 set x = n
 for i=1:1:$length(etapas, ",") do
 . set x = $$@($piece(etapas, ",", i)_"^FUNC2")(x)
 write "resultado=", x, !
 quit
 ;
doblar(v)      quit v * 2
incrementar(v) quit v + 1
""", """
**Lo que esta clase enseña en M.** M **no tiene clausuras ni funciones de primera clase**, y este
programa hace la composición de la única forma que puede: **una lista de nombres de etiqueta,
recorrida e invocada por indirección**.

```mumps
 set etapas = "doblar,incrementar"
 for i=1:1:$length(etapas, ",") set x = $$@($piece(etapas,",",i)_"^FUNC2")(x)
```

**La composición es un dato**: una cadena con nombres separados por comas. Y eso tiene una propiedad
que ninguna clausura da: **se puede guardar en un *global*, leer de la base de datos y cambiar sin
tocar el programa**.

```mumps
 set ^CONFIG("tuberia", "facturas") = "validar,calcular,redondear"
```

Eso es una **tubería configurable y persistente**, definida en la base de datos y ejecutada por
indirección. Cambiar el proceso de facturación de un hospital es un `set`.

Es exactamente lo que hace FileMan con los `INPUT TRANSFORM` (clase 113) y lo que hacen los motores de
reglas de negocio modernos, y es la forma que tiene M de conseguir lo que las clausuras consiguen: **el
comportamiento como dato**.

Con las contrapartidas de siempre, que en esta clase son especialmente serias:

- **Ninguna herramienta puede analizar qué se ejecuta** (clases 086 y 100).
- **Nada comprueba que las etiquetas existan** hasta que se intenta llamarlas — de ahí `$text` (clase
  111).
- **Y un valor mal escrito en la base de datos es un fallo en producción**, no un error de
  compilación.

Y aquí conviene una precisión histórica que evita la caricatura: **eso no es un accidente de un
lenguaje pobre, es una arquitectura**. Los sistemas M grandes se diseñaron para que **la lógica
específica de cada hospital viviera en datos**, de modo que una instalación pudiera adaptarse sin
tocar el código nacional. Con cientos de centros y una sola base de código, esa decisión resolvió un
problema real.

Es la misma tensión que hoy existe entre configuración y código, con cincuenta años de recorrido.
"""),
        "smalltalk": ("""
| n doblar incrementar h |

n := stdin nextLine trimBoth asNumber.

doblar := [ :x | x * 2 ].
incrementar := [ :x | x + 1 ].

"componer: un bloque que devuelve otro bloque"
h := [ :f :g | [ :x | f value: (g value: x) ] ] value: incrementar value: doblar.

Transcript show: 'resultado=', (h value: n) printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Un bloque **captura su entorno y es un objeto de primera
clase** (clase 083), así que componer es escribir un bloque que devuelve otro bloque. Sin
características especiales: solo objetos y mensajes.

Y Smalltalk tiene en su biblioteca algo que resuelve esta clase con más elegancia que casi cualquier
otro lenguaje de la página: **`inject:into:` combinado con bloques**, y sobre todo **las cascadas y
`yourself`**.

Pero lo que de verdad hay que contar aquí es otra cosa: **en Smalltalk la aplicación parcial casi no
hace falta**, y merece entender por qué.

```smalltalk
coleccion select: [ :cada | cada > 100 ]
coleccion detect: [ :cada | cada nombre = buscado ] ifNone: [ nil ]
```

El bloque **ya captura el entorno**, así que `buscado` y `100` están disponibles sin fijarlos. Lo que
en un lenguaje currificado se resuelve con `filtrar(mayorQue(100))`, aquí se resuelve escribiendo el
bloque con la variable dentro.

**La clausura hace innecesaria la aplicación parcial en la mayoría de los casos**, y esa es una
observación que se aplica igual a Perl, Tcl, Lisp y C++ con lambdas: el *currying* es imprescindible
en Haskell y en ML **porque allí todas las funciones son de un argumento**, no porque sea la mejor
forma de fijar parámetros.

Pharo trae además `Symbol` como bloque (clase 085), que es aplicación parcial disfrazada:

```smalltalk
coleccion collect: #printString          "en vez de [ :x | x printString ]"
coleccion detect: #isVowel
```

Y para composición explícita, la biblioteca ofrece:

```smalltalk
(doblar , incrementar) value: 5          "en algunos dialectos: composición con coma"
[ :x | x * 2 ] asMessageSend
```

Y hay una construcción que sí es única y que conecta con la clase 116: **`MessageSend`**, un objeto
que **guarda un receptor, un selector y unos argumentos, sin enviarlo todavía**.

```smalltalk
ms := MessageSend receiver: 5 selector: #+ arguments: #(3).
ms value.                                 "8 -- se envía AHORA"
```

Es una llamada convertida en dato: se puede guardar, pasar, poner en una cola y ejecutar más tarde. Es
el objeto Comando del libro de patrones, y es lo que hace posible el sistema de deshacer, las colas de
tareas y la comunicación entre procesos en Smalltalk.
"""),
    },
)
