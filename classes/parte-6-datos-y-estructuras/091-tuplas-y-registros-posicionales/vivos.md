# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 091

> [⬅️ Volver a la clase 091](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Dos valores que viajan juntos y se intercambian. Es la estructura de datos más pequeña que existe, y
la que mejor muestra un cambio de mentalidad: **ninguno de estos doce lenguajes tiene tuplas
anónimas**, y todos resuelven el problema declarando un tipo con nombre. Que hoy nos parezca pesado
dice más de nuestra época que de la suya — porque el tipo con nombre **documenta qué es cada
componente**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **agregado posicional**, y estos lenguajes lo enseñan por contraste. La tupla
> moderna —`(a, b)` sin declarar nada— es cómoda y **anónima**: `p.0` y `p.1` no dicen qué son. El
> **registro** de COBOL, Fortran, Ada, Pascal y PL/I obliga a declarar el tipo y a nombrar los campos, y
> a cambio el compilador comprueba que no confundas dos pares distintos.
>
> **Ada** añade algo que ningún lenguaje moderno tiene: **el agregado con nombres**, `(A => X, B => Y)`,
> que hace imposible construir el registro con los campos cambiados de orden.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a b` (dos enteros) → stdout: `tupla=(<b>, <a>)` (componentes intercambiados)
- **Regla:** `(a, b) → (b, a)`

| stdin | esperado |
|---|---|
| `3 4` | `tupla=(4, 3)` |
| `0 -2` | `tupla=(-2, 0)` |
| `5 5` | `tupla=(5, 5)` |

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
```

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

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
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
```

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

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
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
```

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

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
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
```

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

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((a (read))
       (b (read))
       (p (cons a b)))                 ; un CONS: el par original de Lisp
  (format t "tupla=(~D, ~D)~%" (cdr p) (car p)))
```

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

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [split [string trim $linea]] a b      ;# desestructuración

puts "tupla=($b, $a)"
```

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

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($a, $b) = split ' ', $linea;

($a, $b) = ($b, $a);           # intercambio SIN variable temporal

print "tupla=($a, $b)\n";
```

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

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <utility>

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::pair<int, int> p{a, b};
    auto [x, y] = p;                   // enlace estructurado (C++17)

    std::cout << "tupla=(" << y << ", " << x << ")\n";
    return 0;
}
```

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
```

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

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
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
```

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

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
TUPLA ; Tuplas y registros -- clase 091
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 set par = b _ "^" _ a                      ; la "tupla": una cadena con piezas
 write "tupla=(", $piece(par, "^", 1), ", ", $piece(par, "^", 2), ")", !
 quit
```

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

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| partes a b |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

Transcript
    show: 'tupla=(', b printString, ', ', a printString, ')';
    cr.
```

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

---

## Y de vuelta a la clase

Lo transferible: **la tupla es cómoda para lo efímero y mala para lo que dura**. Devolver dos valores
de una función es un uso legítimo; guardar una tupla en una estructura que vivirá años significa que
dentro de seis meses alguien leerá `p.1` sin saber qué es. La regla práctica que se deduce de esta
página es la que aplican los lenguajes viejos por obligación y los nuevos por disciplina: **en cuanto
el par cruza una frontera de módulo, dale nombre a los campos**.

⏮️ [Volver a la clase 091](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
