# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 060

> [⬅️ Volver a la clase 060](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

El mayor de dos números. El ejercicio elegido porque la diferencia entre resolverlo con una
**sentencia** y resolverlo con una **expresión** se ve en una línea: `if` decide *qué se ejecuta*,
mientras que una expresión condicional decide *qué valor tiene esto*. Y de esa distinción depende que
puedas escribir `const` en la variable que recibe el resultado.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **la diferencia entre sentencia y expresión**, y estos lenguajes lo enseñan
> porque están en los dos bandos. En **Lisp** y **Smalltalk** la distinción **no existe**: todo es una
> expresión y todo devuelve un valor, así que el condicional siempre ha sido asignable. En **COBOL**,
> **PL/I** y **RPG** no hay ternario en absoluto: hay que declarar la variable y asignarla dentro de
> cada rama.
>
> Y en medio, **Ada** y **Fortran** ilustran la vía alternativa: en vez de un operador ternario,
> **funciones y atributos** —`Integer'Max`, `max()`, `merge()`— que resuelven el caso concreto sin
> necesidad de sintaxis condicional.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a b` (dos enteros) → stdout: `max=<el mayor>`
- **Regla:** `max = (a > b) ? a : b`

| stdin | esperado |
|---|---|
| `3 7` | `max=7` |
| `9 2` | `max=9` |
| `5 5` | `max=5` |

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
PROGRAM-ID. MAXIMO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TXT-A   PIC X(20).
01  TXT-B   PIC X(20).
01  A       PIC S9(9) COMP-3.
01  B       PIC S9(9) COMP-3.
01  MAYOR   PIC S9(9) COMP-3.
01  ED-M    PIC -(9)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    COMPUTE MAYOR = FUNCTION MAX(A, B)

    MOVE MAYOR TO ED-M
    DISPLAY "max=" FUNCTION TRIM(ED-M)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** **COBOL no tiene operador ternario ni `if` como expresión.**
Un `IF` es una sentencia que ejecuta cosas; no devuelve nada. Sin las funciones intrínsecas habría
que escribir:

```cobol
IF A > B
    MOVE A TO MAYOR
ELSE
    MOVE B TO MAYOR
END-IF
```

Cuatro líneas, una variable declarada antes sin valor, y ninguna garantía de que todas las ramas la
asignen.

Lo que COBOL ofrece en su lugar son las **funciones intrínsecas**, incorporadas en COBOL-85, y son
más de las que la gente recuerda:

```cobol
FUNCTION MAX(A, B, C)          *> acepta CUALQUIER número de argumentos
FUNCTION MIN(TABLA(ALL))       *> ¡y una tabla entera con ALL!
FUNCTION SUM(VENTAS(ALL))
FUNCTION MEAN(NOTAS(ALL))
FUNCTION ORD-MAX(A, B, C)      *> la POSICIÓN del mayor, no su valor
```

`FUNCTION MAX(TABLA(ALL))` sobre un array completo es notable: es una operación sobre una colección
entera, sin bucle, en un lenguaje de 1985. Es la misma idea que `max()` de Fortran sobre arrays y que
`inject:into:` de Smalltalk, y la razón es la misma — el dominio del lenguaje está lleno de
totalizar, promediar y buscar máximos sobre tablas.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program maximo
   implicit none
   integer :: a, b

   read(*, *) a, b

   write(*, '(A,I0)') 'max=', max(a, b)
end program maximo
```

**Lo que esta clase enseña en Fortran.** Fortran **tampoco tiene ternario**, y su respuesta es la más
característica del lenguaje: **funciones elementales**.

`max(a, b)` no es una función normal. Es **elemental**, lo que significa que se aplica igual a
escalares y a arrays, elemento a elemento:

```fortran
max(3, 7)                 ! 7
max(a, b, c, d)           ! cualquier número de argumentos
max(vector1, vector2)     ! un ARRAY con el mayor de cada posición
max(matriz, 0.0)          ! pone a cero todos los negativos de una matriz
```

Esa última línea es el idioma que hace innecesario el condicional: en vez de recorrer y comparar,
aplicas la operación a la estructura entera. Es la mentalidad vectorizada de la clase 043, aplicada
al control de flujo.

Y para el caso general, Fortran tiene **`merge`**, que es lo más parecido a un ternario que ofrece:

```fortran
merge(a, b, a > b)              ! el ternario de Fortran
merge(v, 0.0, v > 0.0)          ! sobre un array: pone a cero los no positivos
```

`merge` es también elemental, así que la condición puede ser **un array de lógicos** y la selección se
hace posición a posición. Es una operación sin ramas, que el compilador puede vectorizar — que es
exactamente por lo que existe. En un bucle de mil millones de vueltas, un `if` rompe la
segmentación del procesador y `merge` no.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Maximo is
   A, B : Integer;
begin
   Get (A);
   Get (B);

   --  Integer'Max es un ATRIBUTO del tipo. También valdría la expresión
   --  condicional de Ada 2012:  (if A > B then A else B)
   Put ("max=");
   Put (Integer'Max (A, B), Width => 1);
   New_Line;
end Maximo;
```

**Lo que esta clase enseña en Ada.** Ada tiene **las dos** respuestas, y compararlas es instructivo.

La primera es `Integer'Max (A, B)`: un **atributo del tipo**, no una función de biblioteca. Cada tipo
escalar trae `'Max`, `'Min`, `'Succ`, `'Pred`, `'First`, `'Last`, `'Image`, `'Value`, `'Range`… Si
defines `type Metros is new Float`, `Metros'Max` existe automáticamente y **devuelve un `Metros`**, no
un `Float`. Los atributos se heredan con el tipo, cosa que una función genérica tendría que
instanciar.

La segunda llegó con **Ada 2012**: las **expresiones condicionales**, que exigen paréntesis
obligatorios.

```ada
M : constant Integer := (if A > B then A else B);
X : constant String  := (case Dia is when Sabado | Domingo => "finde",
                                     when others           => "laborable");
```

Los paréntesis no son opcionales, y esa exigencia es muy propia de Ada: **hacen imposible confundir
la expresión con la sentencia** al leer, y evitan cualquier ambigüedad de precedencia.

Lo importante es lo que habilitó esa incorporación: **poder declarar `constant`**. Antes de 2012, una
variable cuyo valor dependía de una condición tenía que declararse sin valor y asignarse en un `if`,
así que no podía ser constante. La expresión condicional no se añadió por brevedad — se añadió para
que más cosas pudieran ser inmutables.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Maximo;
{$MODE OBJFPC}{$H+}
uses SysUtils, Math;

var
  A, B: Integer;

begin
  Read(A, B);

  WriteLn('max=', IntToStr(Max(A, B)));
end.
```

**Lo que esta clase enseña en Pascal.** El Pascal ISO **no tiene ternario**, y Free Pascal y Delphi
añadieron `Max` y `Min` en la unidad `Math`, además de una función `IfThen` que parece un ternario y
**no lo es**:

```pascal
uses Math, StrUtils;

X := IfThen(A > B, A, B);              { versión de Math, para enteros }
S := IfThen(Cond, 'sí', 'no');         { versión de StrUtils, para cadenas }
```

Y aquí está la trampa que esta clase debe señalar: **`IfThen` es una función normal, así que evalúa
sus tres argumentos siempre**. Un ternario de verdad no evalúa la rama que no se toma.

```pascal
X := IfThen(Divisor <> 0, Dividendo div Divisor, 0);   { ¡DIVISIÓN POR CERO! }
```

Esa línea **falla** cuando `Divisor` es cero, porque la división se evalúa antes de llamar a
`IfThen`. En C, `d != 0 ? n / d : 0` es correcto. Es exactamente la diferencia entre una función y
una construcción de control, y es la misma razón por la que `and:` de Smalltalk necesita un bloque y
por la que `and` de Lisp es una macro.

Delphi 10.4 añadió por fin la expresión condicional real —`var m := if a > b then a else b`—, y Free
Pascal la ofrece con el modificador de modo correspondiente. Pero el `IfThen` de la biblioteca sigue
ahí, y sigue siendo una trampa para quien lo confunde con un ternario.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((a (read))
       (b (read)))
  (format t "max=~D~%" (max a b)))
```

**Lo que esta clase enseña en Common Lisp.** En Lisp **la distinción entre sentencia y expresión no
existe**. Todo es una expresión, todo devuelve un valor, y por tanto `if` **siempre** ha sido
asignable:

```lisp
(let ((m (if (> a b) a b))) ...)          ; el if devuelve un valor
(setf x (cond (c1 v1) (c2 v2) (t v3)))    ; cond también
(setf y (case k (1 'uno) (t 'otro)))      ; y case
(setf z (progn (log "hola") 42))          ; incluso un bloque: vale su última forma
```

No hay un `if` que ejecute y otro que devuelva: hay uno solo. Y `when` y `unless`, que son `if` sin
la rama contraria, devuelven `nil` cuando no se cumplen — así que también son expresiones.

Esa uniformidad es lo que Rust, Kotlin, Scala y Ruby adoptaron después, y viene de aquí. La razón por
la que casi todos los lenguajes de los 70 y 80 separaron sentencia de expresión es la máquina: una
sentencia se compilaba a un salto y una expresión a un valor en un registro, y unificarlas costaba.
Lisp lo hizo desde el principio porque su modelo era el cálculo lambda, no la máquina.

`max` en Lisp acepta cualquier número de argumentos y **funciona sobre toda la torre numérica** de la
clase 043: `(max 1/2 0.3 7)` compara una fracción, un real y un entero y devuelve el 7.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [split [string trim $linea]] a b

puts "max=[expr {max($a, $b)}]"
```

**Lo que esta clase enseña en Tcl.** Dentro de `expr`, Tcl **sí tiene el ternario de C** —`c ? a : b`—
y desde la versión 8.5 también las funciones `max()` y `min()` con cualquier número de argumentos.

Fuera de `expr` no hay ninguna de las dos cosas, porque fuera de `expr` no hay operadores. Y eso
produce una asimetría que conviene tener clara:

```tcl
set m [expr {$a > $b ? $a : $b}]     ;# ternario: dentro de expr
set m [expr {max($a, $b)}]           ;# función: dentro de expr
if {$a > $b} { set m $a } else { set m $b }   ;# comando: fuera
```

Las tres formas hacen lo mismo. La primera y la segunda son **expresiones** y se pueden usar donde se
espera un valor; la tercera es un comando que además **devuelve un valor** —el de la última sentencia
del cuerpo ejecutado—, así que en Tcl incluso el `if` es asignable:

```tcl
set m [if {$a > $b} { set _ $a } else { set _ $b }]
```

Funciona, aunque nadie lo escribe así. La razón de que funcione es la misma de siempre: **en Tcl todo
comando devuelve una cadena**, incluido `if`, `while` y `proc`. La distinción sentencia/expresión no
existe porque no hay más que comandos, cada uno con su resultado.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($x, $y) = split ' ', $linea;

my $mayor = $x > $y ? $x : $y;

print "max=$mayor\n";
```

**Lo que esta clase enseña en Perl.** Perl tiene el ternario de C y, además, algo que casi ningún
lenguaje de esta página ofrece: **el ternario es asignable**.

```perl
($x > $y ? $x : $y) = 0;      # pone a cero la MAYOR de las dos variables
```

Eso funciona porque en Perl el ternario devuelve un **lvalue** —una referencia al sitio, no una
copia— cuando ambas ramas lo son. Es la misma capacidad que tiene `substr` en la clase 048, y muestra
una idea de fondo de Perl: las construcciones devuelven *lugares*, no solo valores.

Perl también tiene una versión de esta clase que es más idiomática para más de dos elementos, y viene
de la biblioteca estándar:

```perl
use List::Util qw(max min sum first reduce any all none);

my $mayor = max @numeros;
my $total = sum @numeros;
my $primero = first { $_ > 100 } @numeros;
my $hay = any { $_ < 0 } @numeros;
```

`List::Util` está en el núcleo desde 2001 y sus funciones están escritas en C, así que son rápidas.
`first`, `any`, `all` y `none` **cortocircuitan**: paran en cuanto tienen la respuesta. Es la
biblioteca de orden superior que la clase 068 estudiará a fondo, disponible aquí para resolver el
caso concreto sin escribir un condicional.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <algorithm>
#include <iostream>

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    const int mayor = std::max(a, b);

    std::cout << "max=" << mayor << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** La palabra clave de este programa es **`const`**. `const int
mayor = std::max(a, b);` declara, calcula y **sella** en una sola línea. Con un `if` habría que
escribir `int mayor;` sin valor y asignarlo en las ramas, perdiendo la constancia y abriendo la
posibilidad de que alguna rama no asigne.

Esa es la razón práctica por la que las expresiones condicionales importan, y explica por qué el C++
moderno prefiere el ternario o una lambda inmediatamente invocada cuando la lógica es más compleja:

```cpp
const int mayor = a > b ? a : b;

const auto categoria = [&] {          // lambda invocada al vuelo
    if (score >= 90) return "A";
    if (score >= 80) return "B";
    return "F";
}();                                   // <- se llama aquí mismo
```

Ese patrón —conocido como *IIFE*— convierte una cadena de `if` en una expresión, permitiendo
`const`. Es el sustituto del `if` como expresión en un lenguaje que no lo tiene.

Y un aviso sobre `std::max`: **devuelve una referencia constante**, así que
`const auto& m = std::max(f(), g());` deja una referencia colgante si los argumentos son temporales.
Con `auto` a secas —copiando— no hay problema. Es un caso clásico y sutil que aparece en cuanto se
mezcla `auto&` con funciones que devuelven referencias.

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

dcl-pi MAXIMO;
  a int(10) const;
  b int(10) const;
end-pi;

dcl-s mayor  int(10);
dcl-s salida char(30);

if a > b;
  mayor = a;
else;
  mayor = b;
endif;

salida = 'max=' + %char(mayor);
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** **RPG no tiene ternario ni `if` como expresión**, así que hay
que declarar la variable y asignarla en las ramas. Es la misma situación que COBOL y PL/I, y por el
mismo motivo: los tres nacieron cuando la sentencia y la expresión eran cosas distintas también en la
máquina.

Lo que RPG sí tiene, y viene al caso, son funciones incorporadas sobre **matrices**:

```rpgle
dcl-s ventas packed(11:2) dim(12);

total = %sum(ventas);            // suma de todos los elementos
mayor = %max(ventas);            // el mayor
posicion = %lookup(buscado : ventas);   // búsqueda, devuelve el índice
```

`%sum`, `%max`, `%min` y `%lookup` sobre matrices completas son la misma idea que
`FUNCTION SUM(TABLA(ALL))` de COBOL y `max(array)` de Fortran: **operar sobre la colección entera sin
escribir el bucle**. Los tres lenguajes de negocio y cálculo de esta página llegaron a la misma
solución, porque totalizar tablas es lo que hacen todo el día.

Y para elegir entre dos valores, el idioma de RPG es `%max(a : b)` con la forma de dos argumentos,
que evita el `if` de este programa — aunque sigue sin ser una expresión condicional general.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 maximo: procedure options(main);

    declare (a, b) fixed binary(31);

    get list (a, b);

    put skip list ('max=' || trim(char(max(a, b))));

 end maximo;
```

**Lo que esta clase enseña en PL/I.** PL/I **no tiene ternario**, pero su catálogo de funciones
incorporadas es enorme y cubre este caso y muchos más: `max`, `min`, `abs`, `sign`, `sum`, `prod`,
`any`, `all`, `poly`…

Dos de ellas merecen atención en esta clase porque operan sobre **cadenas de bits**, que es la forma
que PL/I tiene de trabajar con varias condiciones a la vez:

```pli
declare condiciones bit(8);

if any(condiciones) then ...     /* ¿alguno de los 8 bits está a 1? */
if all(condiciones) then ...     /* ¿todos? */
```

`any` y `all` sobre una cadena de bits son el equivalente de los cuantificadores `for all` y
`for some` de Ada de la clase 057, y de `any`/`all` de List::Util en Perl. Con 32 condiciones
empaquetadas en un `bit(32)`, comprobarlas todas es una sola instrucción.

Es un ejemplo del patrón que recorre toda esta sección: **PL/I no tenía la construcción de control,
tenía la operación sobre datos**. Y en muchos casos la operación sobre datos es mejor, porque
paraleliza; en otros, obliga a evaluarlo todo cuando bastaría con lo primero. Esa es exactamente la
frontera entre `any` de PL/I y `first` de Perl, que cortocircuita.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
MAXIMO ; Maximo -- clase 060
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 set mayor = $select(a > b : a, 1 : b)
 write "max=", mayor, !
 quit
```

**Lo que esta clase enseña en M.** **`$select` es el ternario de M**, y es más general que el `?:` de
C porque admite cualquier número de pares:

```mumps
set nivel = $select(x>90 : "alto", x>50 : "medio", x>0 : "bajo", 1 : "nulo")
```

Es una expresión, devuelve un valor, evalúa perezosamente y encadena tantos casos como quieras. En un
lenguaje sin ternario ni `if` asignable, `$select` cubre las dos necesidades.

Y M tiene una segunda pieza que resuelve esta clase de otra manera, y que es muy suya: **`$order` y
la ordenación de las claves**. Como los subíndices de un array se guardan en orden, el máximo de un
conjunto no se calcula, **se consulta**:

```mumps
 set ^TMP(3)="", ^TMP(7)="", ^TMP(5)=""
 write $order(^TMP(""), -1)      ; 7 -- el ÚLTIMO subíndice: el máximo
 write $order(^TMP(""))          ; 3 -- el PRIMERO: el mínimo
```

El `-1` recorre en orden inverso. En una base de datos con un millón de nodos, obtener el máximo es
una operación de índice, no un recorrido. Es la misma ventaja que da un índice B-tree en SQL, con la
diferencia de que aquí no hay que declararlo: **el orden es una propiedad del almacenamiento**.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| partes a b |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

Transcript show: 'max=', (a max: b) printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** `a max: b` es **un mensaje enviado al número**, y como todo
mensaje devuelve un valor, la distinción de esta clase sencillamente no se plantea: en Smalltalk
**todo es una expresión**.

`ifTrue:ifFalse:` devuelve el valor del bloque que se evaluó, así que es asignable sin ninguna
sintaxis especial:

```smalltalk
mayor := a > b ifTrue: [ a ] ifFalse: [ b ].
etiqueta := score > 50 ifTrue: [ 'apto' ] ifFalse: [ 'no apto' ].
```

Y lo mismo vale para el resto de estructuras de control: `whileTrue:` devuelve `nil`, `to:do:`
devuelve el receptor, `detect:ifNone:` devuelve el elemento encontrado. **No hay ninguna construcción
del lenguaje que no devuelva algo**, porque todas son envíos de mensajes y un mensaje siempre
responde.

La implementación de `max:` es, como cabe esperar, una línea que puedes abrir y leer:

```smalltalk
Magnitude >> max: unaMagnitud
    ^ self > unaMagnitud ifTrue: [ self ] ifFalse: [ unaMagnitud ]
```

Está en `Magnitude`, la superclase abstracta de todo lo que se puede comparar —números, caracteres,
fechas, cadenas—. Basta con implementar `<` en una clase nueva para heredar `max:`, `min:`,
`between:and:` y el resto del protocolo de comparación. Es la misma economía que el `Comparable` de
Java, veinte años antes.

---

## Y de vuelta a la clase

Lo transferible es que **una expresión condicional permite inicializar y sellar en una sola
sentencia**. `const int m = a > b ? a : b;` declara, calcula y prohíbe futuras modificaciones a la
vez; la versión con `if` obliga a declarar sin valor y confiar en que todas las ramas asignen. Por
eso Rust, Kotlin y Scala convirtieron `if` en expresión, y por eso Python añadió `a if c else b`. Los
lenguajes de esta página muestran de dónde venía la necesidad.

⏮️ [Volver a la clase 060](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
