# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 050

> [⬅️ Volver a la clase 050](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Sumar un entero y un real. La operación más inocente del programa, y la que obliga a cada lenguaje a
declarar su postura: **¿cuándo se decide que esto es una suma de reales?** ¿Al compilar, mirando las
declaraciones? ¿Al ejecutar, mirando los valores? ¿O no se decide nunca, porque no hay tipos que
mirar?

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **el momento en que se resuelve el tipo**, y estos lenguajes cubren el espectro
> entero con posturas más nítidas que el núcleo. **Ada** representa el extremo estático absoluto: la
> suma **no compila** sin una conversión escrita, aunque sea evidente lo que quieres. **COBOL** decide
> al compilar, pero la conversión la esconde en el `MOVE`. **Fortran, Pascal y C++** promocionan solos
> en la dirección segura. Y **Tcl, M, Perl y Smalltalk** no deciden nada hasta que la operación se
> ejecuta.
>
> Lo interesante es que estático y dinámico **no es una escala de rigor**: Smalltalk es dinámico y
> fuertemente tipado, Tcl es dinámico y débil, y C++ es estático y permite conversiones que pierden
> datos. Son dos ejes distintos, y esta clase junto con la 051 los separa.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a b` (a entero, b real) → stdout: `suma=<a+b con 2 decimales>`
- **Regla:** `suma = a + b (a entero promovido a real)`

| stdin | esperado |
|---|---|
| `2 3.5` | `suma=5.50` |
| `10 0.25` | `suma=10.25` |
| `0 0` | `suma=0.00` |

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
PROGRAM-ID. MIXTO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TXT-A   PIC X(20).
01  TXT-B   PIC X(20).
01  A       PIC S9(9)    COMP-3.
01  B       PIC S9(9)V99 COMP-3.
01  S       PIC S9(9)V99 COMP-3.
01  ED-S    PIC -(9)9.99.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    COMPUTE S = A + B

    MOVE S TO ED-S
    DISPLAY "suma=" FUNCTION TRIM(ED-S)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** COBOL es **estático hasta el extremo**: el tipo, el número de
dígitos, la posición de la coma decimal y la representación física de cada dato están decididos
**antes de compilar**, y no pueden cambiar. Una variable no puede contener a veces un número y a
veces un texto; ni siquiera puede contener un número con más dígitos de los declarados.

Pero —y esta es la parte interesante— **la conversión entre tipos numéricos es totalmente
implícita**. `COMPUTE S = A + B` con `A` sin decimales y `B` con dos funciona sin decir nada: el
compilador alinea las comas decimales, hace la suma y ajusta al destino. COBOL sabe exactamente qué
está pasando porque todo está declarado, así que no necesita preguntar.

Eso lo sitúa en una casilla que casi ningún lenguaje moderno ocupa: **estático, fuerte en cuanto a la
forma del dato, y permisivo en la aritmética**. La comprobación no está en prohibir la mezcla, está
en que la mezcla se resuelve con reglas deterministas y documentadas.

El precio es el de la clase 049: cuando el destino no da de sí, el resultado se trunca en silencio.
COBOL confía en que declaraste bien.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program mixto
   implicit none
   integer :: a
   real(kind=8) :: b, s
   character(len=32) :: buf

   read(*, *) a, b
   s = a + b            ! promoción implícita: a se convierte a real

   write(buf, '(F20.2)') s
   write(*, '(A,A)') 'suma=', trim(adjustl(buf))
end program mixto
```

**Lo que esta clase enseña en Fortran.** Fortran es estático y **promociona en la dirección segura**:
en `a + b` con `a` entero y `b` real, el entero se convierte a real y la suma es real. La regla se
llama *conversión aritmética* y está en el estándar; no hay ambigüedad.

Lo que hay que vigilar es que **la promoción ocurre en la expresión, no en la asignación**, y esa
distinción es la fuente del error más clásico del lenguaje:

```fortran
real(kind=8) :: x
x = 1 / 2          ! x vale 0.0  -- la división es ENTERA, y luego se promociona
x = 1.0d0 / 2      ! x vale 0.5  -- ahora la división ya es real
```

El destino no influye en cómo se evalúa la expresión. Es el mismo comportamiento de C, Java y Go, y
el mismo error.

Y `implicit none` vuelve a ser decisivo en esta clase: **sin él, Fortran es estático pero con tipos
adivinados**. Una variable sin declarar recibe tipo según su inicial, así que `total = a + b` podría
estar sumando en entero sin que aparezca ninguna declaración que lo delate. Es tipado estático con la
mitad de las garantías, y es la razón de que esa línea sea obligatoria en cualquier Fortran serio.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;            use Ada.Text_IO;
with Ada.Integer_Text_IO;    use Ada.Integer_Text_IO;
with Ada.Long_Float_Text_IO; use Ada.Long_Float_Text_IO;

procedure Mixto is
   A    : Integer;
   B, S : Long_Float;
begin
   Get (A);
   Get (B);

   --  S := A + B;  NO COMPILA. La conversión es obligatoria y visible.
   S := Long_Float (A) + B;

   Put ("suma="); Put (S, Fore => 1, Aft => 2, Exp => 0);
   New_Line;
end Mixto;
```

**Lo que esta clase enseña en Ada.** La línea comentada es el contenido entero de la clase: **`A + B`
no compila**. Ada no promociona nada, nunca, entre tipos numéricos distintos. Ni siquiera en la
dirección segura que Fortran, Pascal, C++ y Java permiten sin decir nada.

Y va más lejos de lo que parece, porque en Ada **dos tipos con la misma representación siguen siendo
distintos**:

```ada
type Metros is new Float;
type Pies   is new Float;

M : Metros := 100.0;
P : Pies   := 50.0;
--  X := M + P;          NO COMPILA: son tipos distintos
X : Metros := M + Metros (Float (P) * 0.3048);   --  la conversión declara la intención
```

Eso es **tipado nominal fuerte**: el nombre del tipo importa, no solo su forma. Es la característica
que habría evitado la pérdida de la sonda Mars Climate Orbiter, y la razón de que Ada siga en
aviónica.

El coste es real y conviene reconocerlo: el código es más largo y hay conversiones por todas partes.
La apuesta de Ada es que **escribir la conversión obliga a pensarla**, y que en un sistema donde un
fallo cuesta vidas, ese coste sale barato. En un guion de cinco líneas, no.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Mixto;
{$MODE OBJFPC}{$H+}

var
  A: Integer;
  B, S: Double;

begin
  Read(A, B);
  S := A + B;          { Pascal promociona en la dirección segura }

  WriteLn('suma=', S:0:2);
end.
```

**Lo que esta clase enseña en Pascal.** Pascal ocupa la casilla intermedia con una regla explícita y
fácil de recordar: **promociona hacia donde no se pierde información, y prohíbe lo demás**.

```pascal
S := A + B;      { Integer + Double -> Double.  Correcto. }
A := S;          { NO COMPILA: hay que escribir Trunc(S) o Round(S) }
```

Es la misma política que Fortran, con la diferencia de que Pascal la aplica también a los tipos
definidos por el usuario. Un subrango `1..10` se asigna a un `Integer` sin problema, pero al revés
requiere comprobación de rango en ejecución con `{$R+}`.

Y esta clase toca un punto donde Pascal fue **más estricto que casi todos**: los **tipos
incompatibles por nombre**. `type Metros = Integer` crea un alias compatible, pero
`type Metros = type Integer` —con la palabra `type` repetida— crea un tipo **distinto** que no se
mezcla, exactamente como el `new` de Ada. Delphi lo usa mucho para que el compilador distinga
identificadores que son todos enteros pero significan cosas distintas.

Es una capacidad que muy pocos lenguajes tienen y que hoy se pide constantemente con el nombre de
*newtype* o *branded types*: TypeScript la simula con trucos, Rust la tiene con `struct Metros(f64)`,
y Pascal la tenía en 1970.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(setf *read-default-float-format* 'double-float)

(let* ((a (read))
       (b (read))
       (s (+ a b)))
  (format t "suma=~,2F~%" s))
```

**Lo que esta clase enseña en Common Lisp.** Lisp es **dinámico y fuertemente tipado**, y esta
combinación es la que más cuesta ver desde fuera. Dinámico: el tipo pertenece al **valor**, y `a`
puede contener hoy un entero y mañana una lista. Fuerte: `(+ 1 "dos")` **no** convierte nada, levanta
un error de tipo en ejecución.

Y la aritmética aplica la **regla de contagio** de la torre numérica que apareció en la clase 043: al
mezclar un entero exacto con un real inexacto, el resultado es inexacto. `(+ 2 3.5d0)` da `5.5d0`, y
`(+ 1/2 1/3)` da `5/6` porque los dos son exactos.

Lo que Lisp añade y que casi ningún dinámico tiene es la posibilidad de **declarar tipos cuando
interesa**, sin dejar de ser dinámico:

```lisp
(defun suma (a b)
  (declare (type double-float a b)
           (optimize (speed 3) (safety 0)))
  (+ a b))
```

Con esa declaración, SBCL genera código nativo tan rápido como el de C, sin comprobaciones. Sin ella,
la misma función acepta cualquier número. Es **tipado gradual** —lo que hoy hacen TypeScript, Python
con anotaciones o Sorbet en Ruby— disponible en el estándar de 1994. Y SBCL va más lejos: **infiere y
avisa en tiempo de compilación** de incompatibilidades que puede demostrar, aunque no hayas declarado
nada.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [split [string trim $linea]] a b

set s [expr {$a + $b}]

puts "suma=[format %.2f $s]"
```

**Lo que esta clase enseña en Tcl.** No hay tipos, así que no hay nada que decidir al compilar. La
pregunta "¿esto es una suma de enteros o de reales?" la responde **`expr`, en el momento de
ejecutar**, mirando el aspecto del texto:

```tcl
expr {2 + 3}        ;# 5      -- los dos parecen enteros
expr {2 + 3.5}      ;# 5.5    -- uno parece real, promociona
expr {"2" + "3"}    ;# 5      -- las comillas no cambian nada
expr {2 + "hola"}   ;# ERROR  -- Tcl SÍ falla aquí
```

Esa última línea importa: Tcl es de tipado débil, pero **no es JavaScript**. No inventa un resultado;
lanza un error. La debilidad de Tcl consiste en aceptar que cualquier cadena *que parezca un número*
lo sea, no en convertir cualquier cosa a cualquier cosa.

Y hay un detalle de implementación que explica por qué esto no es lento: Tcl guarda junto a la cadena
una **representación interna** con su tipo real —entero, real, lista, comando compilado—, y solo la
regenera si el valor cambia. Un bucle que sume un millón de veces no reanaliza el texto un millón de
veces. La semántica es "todo es cadena"; la implementación es otra cosa.

Ese truco —conocido como *dual-ported object*— es de 1997 y es el antepasado directo de las clases
ocultas de los motores de JavaScript modernos.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($a_val, $b_val) = split ' ', $linea;

printf "suma=%.2f\n", $a_val + $b_val;
```

**Lo que esta clase enseña en Perl.** Perl es dinámico y **débil**, y aquí ni siquiera hay una
decisión que tomar: `$a_val` y `$b_val` contienen texto leído de la entrada, y el operador `+` los
lee como números porque eso es lo que hace `+`. No hay promoción de entero a real porque **no hay
entero ni real**: hay un escalar que sabe comportarse como ambos.

Internamente, un escalar de Perl (una estructura `SV`) tiene ranuras para el valor entero (`IV`), el
real (`NV`) y la cadena (`PV`), y va rellenando la que haga falta. Por eso `$x = "3.5"; $y = $x + 0;`
no "convierte": simplemente materializa la ranura numérica y la conserva para la próxima vez.

La consecuencia práctica es que **el tipo lo elige el operador, no el dato**, y de ahí que Perl
necesite dos juegos de operadores —tema de la clase 051—. Y también que la única forma de comprobar
algo sea preguntar explícitamente:

```perl
use Scalar::Util qw(looks_like_number);
die "no es un número" unless looks_like_number($b_val);
```

Nota sobre el estilo: las variables se llaman `$a_val` y `$b_val` y no `$a` y `$b` a propósito.
`$a` y `$b` son **variables especiales** que Perl usa internamente en `sort`, y aunque `use strict`
las deja pasar, usarlas para otra cosa es una de esas trampas que solo muerden mucho después.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iomanip>
#include <iostream>

int main() {
    int a{};
    double b{};
    if (!(std::cin >> a >> b)) return 1;

    const double s = a + b;      // promoción aritmética implícita

    std::cout << "suma=" << std::fixed << std::setprecision(2) << s << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ es estático y con **conversiones aritméticas implícitas**
definidas por un conjunto de reglas —las *usual arithmetic conversions*— que casi nadie ha leído
entero y que producen sorpresas genuinas:

```cpp
int a = -1;
unsigned int b = 1;
if (a < b) { }          // FALSO: a se convierte a unsigned y vale 4294967295

short x = 30000, y = 30000;
int z = x + y;          // ambos se promocionan a int: 60000, correcto
short w = x + y;        // desbordamiento al volver a short
```

La regla de fondo es que los operandos se promocionan al tipo "más grande" de la expresión, y que
`unsigned` gana a `signed` del mismo rango. Ese último punto es el origen de una familia entera de
errores, y la razón de que las guías modernas recomienden no usar `unsigned` para cantidades que solo
son "no negativas".

Lo que C++ ofrece a cambio es que **todas esas conversiones se pueden hacer visibles**: compilar con
`-Wconversion -Wsign-conversion` convierte cada promoción con pérdida en un aviso. Y desde C++11, la
**inicialización con llaves** las prohíbe donde importa:

```cpp
int  n1 = 3.7;    // compila, n1 vale 3
int  n2 {3.7};    // NO COMPILA: narrowing conversion
```

Es la misma política de Ada, disponible como opción en vez de como norma.

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

dcl-pi MIXTO;
  a int(10)      const;
  b packed(15:2) const;
end-pi;

dcl-s s      packed(15:2);
dcl-s salida char(40);

s = a + b;          // entero + decimal: RPG alinea y suma

salida = 'suma=' + %char(s);
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG es estático y, como COBOL, **resuelve la mezcla numérica sin
protestar**: alinea las comas decimales y ajusta al destino. El compilador lo puede hacer porque
conoce exactamente los dígitos y decimales de cada operando.

Lo que RPG añade y que conviene conocer es que **el resultado intermedio también tiene precisión
declarada**, y ahí está el riesgo. Al multiplicar dos `packed(15:2)`, el resultado natural tendría 30
dígitos con 4 decimales, que excede el máximo del tipo (63 dígitos en versiones recientes, 31 en las
antiguas). Si el destino no da de sí, se trunca.

Por eso existe la palabra clave **`eval-corr`** para estructuras y, sobre todo, la posibilidad de
forzar la precisión intermedia:

```rpgle
s = %dech(a * b : 15 : 2);   // decide TÚ los dígitos y el redondeo
```

Y hay una diferencia con COBOL que salta a la vista en el tipado: RPG **sí** distingue `int` de
`packed`, es decir, binario de decimal, mientras que COBOL lo trata como una cláusula de
almacenamiento (`COMP` frente a `COMP-3`) sobre el mismo `PIC`. Dos formas de decir lo mismo, con
consecuencias distintas al leer el código: en RPG el tipo lo dices, en COBOL lo dice la forma.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 mixto: procedure options(main);

    declare a    fixed binary(31);
    declare b    fixed decimal(15,2);
    declare s    fixed decimal(15,2);
    declare pres picture 'ZZZZZZZZZ9V.99';

    get list (a, b);

    s = a + b;      /* binaria + decimal: PL/I convierte segun sus reglas */

    pres = s;
    put skip list ('suma=' || trim(pres));

 end mixto;
```

**Lo que esta clase enseña en PL/I.** PL/I es estático y **el campeón absoluto de la conversión
implícita**. Aquí se suman un `fixed binary` y un `fixed decimal` —bases distintas, no solo tipos
distintos— y el lenguaje lo resuelve sin decir nada: convierte el binario a decimal según una regla
del estándar y opera.

Esa regla existe, está documentada y ocupa varias páginas. Define la precisión del resultado
intermedio a partir de la de los operandos, para cada combinación de base y escala. Es **determinista
y prácticamente imposible de recordar**, y ese es exactamente el problema que Dijkstra señalaba: un
lenguaje puede ser completamente especificado y aun así inmanejable, si nadie puede predecir su
comportamiento sin consultar el manual.

La lección de diseño que deja PL/I para esta clase es la más valiosa del programa: **hay una
diferencia entre "el lenguaje sabe qué hacer" y "el programador sabe qué va a pasar"**. COBOL acierta
porque sus reglas son pocas; Ada acierta porque no tiene ninguna; PL/I falla porque tiene demasiadas.

Cuando en un lenguaje moderno alguien discute si añadir una conversión implícita más, este es el
precedente que hay que citar.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
MIXTO ; Estatico vs dinamico -- clase 050
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 set s = a + b
 write "suma=", $justify(s, 0, 2), !
 quit
```

**Lo que esta clase enseña en M.** M es el caso más puro de tipado dinámico y débil: **no hay tipos
que resolver ni al compilar ni al ejecutar**. `a` y `b` son cadenas, `+` las lee como números, y el
resultado es una cadena que representa un número.

Y aquí conviene mirar algo que no se ve en ningún otro lenguaje de esta página: **la ausencia de tipos
llega también a la base de datos**. Un *global* de M no tiene esquema, así que el mismo nodo puede
contener hoy un número y mañana un texto, y las claves del árbol se ordenan con una regla mixta —
primero la cadena vacía, luego los números en orden numérico, luego el resto en orden de colación—.

Esa regla de ordenación *numérica antes que alfabética* es una decisión de diseño con cincuenta años
que hoy resulta familiar: es lo que hacen los índices de una base de datos documental. M era NoSQL
sin esquema en 1966, con las mismas ventajas —flexibilidad ante datos irregulares— y los mismos
inconvenientes —ninguna garantía, validación siempre por cuenta del programador—.

Por eso VistA construyó **FileMan** encima: un diccionario que define, para cada campo, su tipo, su
rango, su obligatoriedad y sus reglas. Es literalmente el sistema de tipos que el lenguaje no tiene,
implementado como datos dentro de la propia base de datos.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| partes a b |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

Transcript
    show: 'suma=', ((a + b) asFloat printShowingDecimalPlaces: 2);
    cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk es **dinámico y fuertemente tipado**, y es el
mejor ejemplo de que esos dos ejes son independientes. No hay declaraciones de tipo en ninguna parte,
pero `3 + 'hola'` **no** produce un resultado raro: produce un error, porque `SmallInteger` no sabe
sumar una cadena.

Y la forma en que ocurre la suma mixta es lo específico de esta clase. `a + b` con `a` entero y `b`
real no es una regla del lenguaje: es **doble despacho**. `SmallInteger>>+` recibe un argumento que no
sabe manejar y hace lo único sensato — le pregunta al argumento:

```smalltalk
Number >> + aNumber
    ^ self generality < aNumber generality
        ifTrue:  [ (aNumber coerce: self) + aNumber ]
        ifFalse: [ self + (self coerce: aNumber) ]
```

Cada clase numérica declara su **generalidad** —entero < fracción < real < complejo— y la de menor
generalidad se convierte a la de mayor. La torre numérica de Lisp existe aquí también, pero
implementada **como código de biblioteca que puedes leer y extender**, no como una regla del
compilador.

La consecuencia es notable: si defines una clase `Dinero` y le das `generality` y `coerce:`, se
integra en la aritmética existente y `3 + unDinero` funciona. Añadir un tipo numérico al lenguaje no
requiere tocar el lenguaje.

---

## Y de vuelta a la clase

La pregunta que deja esta página no es "¿estático o dinámico?" sino **"¿cuánto sabe el compilador
antes de ejecutar, y qué hace con lo que no sabe?"**. Ada lo sabe todo y se niega a suponer. C++ lo
sabe casi todo y supone en silencio. Smalltalk no sabe nada hasta que llega el objeto, pero cuando
llega comprueba de verdad. Y Tcl y M no comprueban nunca. Las cuatro posturas tienen sistemas en
producción desde hace décadas, así que ninguna es simplemente incorrecta.

⏮️ [Volver a la clase 050](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
