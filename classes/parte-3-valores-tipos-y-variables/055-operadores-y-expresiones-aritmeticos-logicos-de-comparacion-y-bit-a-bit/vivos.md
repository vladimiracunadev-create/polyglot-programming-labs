# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 055

> [⬅️ Volver a la clase 055](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Las cinco operaciones de la escuela: suma, resta, multiplicación, división entera y resto. Con
números positivos todos los lenguajes coinciden. Cambia el signo de uno de ellos y **dejan de
coincidir**: `-7 mod 3` vale `-1` en C, C++, Java y Go, y vale `2` en Python, Ruby y Tcl. Los dos
resultados son correctos; responden a definiciones distintas de qué es dividir.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **la semántica exacta de los operadores**, y estos lenguajes son los que mejor la
> exponen porque **algunos ofrecen las dos definiciones a la vez y te obligan a elegir**. Ada tiene
> `mod` y `rem`; Fortran tiene `modulo` y `mod`; Lisp tiene `mod` y `rem`; Smalltalk tiene `\\` y
> `rem:`. En cada pareja, la primera sigue el signo del divisor y la segunda el del dividendo.
>
> Y COBOL enseña algo distinto: **no tiene operador de resto**. Tiene una cláusula del verbo
> `DIVIDE`, lo que obliga a escribir la división y el resto en la misma sentencia — que es, de hecho,
> lo que hace el procesador.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a b` (enteros positivos, b != 0) → stdout: `suma=<a+b> resta=<a-b> mult=<a*b> div=<a/b entera> mod=<a%b>`
- **Regla:** `las cinco operaciones aritméticas sobre a y b`

| stdin | esperado |
|---|---|
| `10 3` | `suma=13 resta=7 mult=30 div=3 mod=1` |
| `20 4` | `suma=24 resta=16 mult=80 div=5 mod=0` |
| `7 2` | `suma=9 resta=5 mult=14 div=3 mod=1` |

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
PROGRAM-ID. OPERADORES.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TXT-A   PIC X(20).
01  TXT-B   PIC X(20).
01  A       PIC S9(9)  COMP-3.
01  B       PIC S9(9)  COMP-3.
01  SUMA    PIC S9(18) COMP-3.
01  RESTA   PIC S9(18) COMP-3.
01  MULT    PIC S9(18) COMP-3.
01  DIVI    PIC S9(18) COMP-3.
01  RESTO   PIC S9(18) COMP-3.
01  ED-S    PIC -(17)9.
01  ED-R    PIC -(17)9.
01  ED-M    PIC -(17)9.
01  ED-D    PIC -(17)9.
01  ED-MO   PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    COMPUTE SUMA  = A + B
    COMPUTE RESTA = A - B
    COMPUTE MULT  = A * B
    DIVIDE A BY B GIVING DIVI REMAINDER RESTO

    MOVE SUMA  TO ED-S
    MOVE RESTA TO ED-R
    MOVE MULT  TO ED-M
    MOVE DIVI  TO ED-D
    MOVE RESTO TO ED-MO
    DISPLAY "suma=" FUNCTION TRIM(ED-S)
            " resta=" FUNCTION TRIM(ED-R)
            " mult=" FUNCTION TRIM(ED-M)
            " div=" FUNCTION TRIM(ED-D)
            " mod=" FUNCTION TRIM(ED-MO)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** **COBOL no tiene operador de resto.** Ni `%`, ni `mod`. Lo que
tiene es una **cláusula del verbo `DIVIDE`**:

```cobol
DIVIDE A BY B GIVING DIVI REMAINDER RESTO
```

Una sola sentencia produce el cociente **y** el resto. Y eso no es una limitación: es lo que hace de
verdad el procesador, que en una única instrucción de división devuelve las dos cosas. En C hay que
escribir `a / b` y `a % b` por separado y confiar en que el compilador reconozca el patrón y no
divida dos veces —cosa que hace, pero es una optimización, no una garantía—.

Ese detalle explica también por qué la biblioteca de C tiene `div()` y `ldiv()`, que devuelven una
estructura con cociente y resto: alguien se dio cuenta del mismo problema.

Y esta clase deja ver la otra herencia de COBOL: **los verbos aritméticos** anteriores a `COMPUTE`,
que siguen siendo válidos y aparecen en todo el código antiguo:

```cobol
ADD IVA TO TOTAL
SUBTRACT DESCUENTO FROM PRECIO GIVING NETO
MULTIPLY CANTIDAD BY PRECIO GIVING IMPORTE ROUNDED
```

Se leen en voz alta como una instrucción a un administrativo, que era exactamente el objetivo de 1959.
`COMPUTE` llegó después para escribir expresiones completas, y hoy es lo que se usa — pero conocer los
verbos es imprescindible para leer los millones de líneas escritas antes.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program operadores
   implicit none
   integer :: a, b

   read(*, *) a, b

   write(*, '(A,I0,A,I0,A,I0,A,I0,A,I0)') &
      'suma=', a + b, ' resta=', a - b, ' mult=', a * b, &
      ' div=', a / b, ' mod=', mod(a, b)
end program operadores
```

**Lo que esta clase enseña en Fortran.** Fortran tiene **dos funciones de resto**, y la diferencia
solo se ve con negativos:

```fortran
mod(-7, 3)      ! -1  -- sigue el signo del DIVIDENDO (división truncada)
modulo(-7, 3)   !  2  -- sigue el signo del DIVISOR   (división al suelo)
```

`mod` es la de C, C++ y Java; `modulo` es la de Python, Ruby y las matemáticas. Tener las dos con
nombres distintos evita la discusión: eliges la que necesitas y queda escrito cuál era.

Para índices cíclicos —"el siguiente de la lista, dando la vuelta"— la correcta es casi siempre
`modulo`, porque nunca devuelve negativos. Usar `mod` ahí produce un índice fuera de rango cuando el
valor es negativo, y es un error clásico.

Y Fortran tiene un operador que ningún otro lenguaje de esta página ofrece con sintaxis propia:
**`**` para la potencia**.

```fortran
2 ** 10        ! 1024
x ** 0.5       ! raíz cuadrada
matriz ** 2    ! ojo: elemento a elemento, NO producto matricial
```

En C y en Java hay que llamar a `pow()`. En Fortran es un operador con su precedencia —la más alta— y
además está **asociado a la derecha**, como en matemáticas: `2 ** 3 ** 2` es `2 ** 9`, no `8 ** 2`.
Python y Ada tomaron el mismo operador; C nunca lo tuvo.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Operadores is
   A, B : Integer;
begin
   Get (A);
   Get (B);

   Put ("suma=");   Put (A + B,   Width => 1);
   Put (" resta="); Put (A - B,   Width => 1);
   Put (" mult=");  Put (A * B,   Width => 1);
   Put (" div=");   Put (A / B,   Width => 1);
   Put (" mod=");   Put (A rem B, Width => 1);
   New_Line;
end Operadores;
```

**Lo que esta clase enseña en Ada.** Ada tiene **`mod` y `rem` como dos operadores distintos**, y
—esto es lo importante— la elección está ligada a la definición de la división:

```ada
 7 rem  3  =  1     -7 rem  3  = -1     --  rem acompaña a "/", que TRUNCA
 7 mod  3  =  1     -7 mod  3  =  2     --  mod sigue el signo del DIVISOR
```

`A / B` en Ada trunca hacia cero, y `rem` es su resto coherente: se cumple siempre
`A = (A / B) * B + (A rem B)`. `mod` corresponde a la división al suelo. Que el lenguaje tenga las
dos con nombres distintos y documente la identidad que cumple cada una es exactamente el nivel de
precisión que se espera de un lenguaje para sistemas críticos.

Y hay dos cosas más de esta clase que Ada hace de forma característica.

La primera: **`**` solo acepta exponente entero no negativo** para operandos enteros. `2 ** (-1)`
levanta `Constraint_Error` en lugar de devolver 0 silenciosamente, porque el resultado no es
representable como entero.

La segunda: **dividir por cero levanta `Constraint_Error`**, siempre, sin excepción. En C y C++ la
división entera por cero es **comportamiento indefinido** —el compilador puede asumir que no ocurre y
optimizar en consecuencia—, lo que significa que el programa puede hacer cualquier cosa. En Ada es un
suceso previsto, con nombre, capturable y sin coste cuando el compilador puede demostrar que no pasa.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Operadores;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  A, B: Integer;

begin
  Read(A, B);

  WriteLn('suma=', IntToStr(A + B),
          ' resta=', IntToStr(A - B),
          ' mult=', IntToStr(A * B),
          ' div=', IntToStr(A div B),
          ' mod=', IntToStr(A mod B));
end.
```

**Lo que esta clase enseña en Pascal.** Pascal separa **dos operadores de división** con nombres
distintos, y es una de sus mejores decisiones:

```pascal
7 div 2     { 3    -- división ENTERA; solo acepta enteros }
7 / 2       { 3.5  -- división REAL; SIEMPRE da un Real }
```

`/` en Pascal **nunca** da un entero, ni aunque los dos operandos lo sean. `X := 7 / 2` con `X`
entero **no compila**. Compara con C, Java, Go y Rust, donde `7 / 2` da `3` porque los operandos son
enteros y hay que recordarlo: es el mismo símbolo con dos significados según los tipos, y la causa de
un error clásico que Pascal hace imposible.

Sobre el resto: `mod` en Pascal sigue el signo del **dividendo**, como el `%` de C. `-7 mod 3` da
`-1`. Free Pascal no ofrece la variante al suelo, así que hay que escribirla —`((a mod b) + b) mod b`—
si se necesita para índices cíclicos.

Y esta clase es donde reaparece la trampa de precedencia de la clase 046, ahora con `div` y `mod`:
**tienen la misma precedencia que `*` y `/`**, que es lo esperable, pero **`and` también**, y `or`
está al nivel de `+`. Por eso los paréntesis en `(a > 0) and (b > 0)` no son opcionales. Es una
consecuencia de haber unificado los operadores lógicos con los de bits en 1970, y el lenguaje la
arrastra desde entonces.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((a (read))
       (b (read)))
  (format t "suma=~D resta=~D mult=~D div=~D mod=~D~%"
          (+ a b) (- a b) (* a b) (truncate a b) (rem a b)))
```

**Lo que esta clase enseña en Common Lisp.** Lisp es el lenguaje de esta página con la aritmética más
cuidadosa, y esta clase deja ver por qué. Para dividir enteros hay **cuatro funciones**, una por cada
forma de redondear el cociente, y **cada una devuelve el cociente y el resto**:

| Función | Cociente | Resto asociado |
|---|---|---|
| `truncate` | Hacia cero | `rem` |
| `floor` | Hacia abajo | `mod` |
| `ceiling` | Hacia arriba | — |
| `round` | Al más cercano (bancario) | — |

```lisp
(truncate -7 3)   ; => -2 y -1     (rem -7 3) => -1
(floor    -7 3)   ; => -3 y  2     (mod -7 3) =>  2
```

La correspondencia está garantizada por el estándar: `rem` acompaña a `truncate` y `mod` a `floor`.
Ninguna ambigüedad, ninguna nota al pie.

Y **`/` en Lisp no es ninguna de las cuatro**: da el resultado **exacto**. `(/ 7 2)` devuelve la
fracción `7/2`, no `3` ni `3.5`. Para obtener un entero hay que decir **cuál** de los cuatro
redondeos quieres, y para obtener un real hay que pedirlo con `(/ 7.0 2)`.

Es la postura más coherente de toda la página: si la división de dos enteros no es un entero, el
lenguaje no elige por ti. La contrapartida es que `(/ 1 3)` produce un objeto `ratio` y no el
`0.333` que muchos esperan — que es, en realidad, la respuesta correcta.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [split [string trim $linea]] a b

puts "suma=[expr {$a + $b}] resta=[expr {$a - $b}] mult=[expr {$a * $b}]\
 div=[expr {$a / $b}] mod=[expr {$a % $b}]"
```

**Lo que esta clase enseña en Tcl.** Toda la aritmética vive **dentro de `expr`**, porque fuera de él
no hay operadores: hay comandos. `expr` es un mini-lenguaje empotrado con su propia gramática y su
propia tabla de precedencias, tomada de C.

Y Tcl tomó una decisión que lo separa de C: **`%` sigue el signo del divisor**, como Python.

```tcl
expr {-7 % 3}       ;# 2   -- en C sería -1
expr {-7 / 3}       ;# -3  -- división AL SUELO, no truncada
```

Es coherente —el cociente y el resto van a juego— y es lo contrario de lo que espera quien viene de
C. Está documentado, y es exactamente el tipo de detalle que hay que comprobar al portar un algoritmo.

Esta clase también recuerda **por qué `expr` va siempre entre llaves**. Sin ellas, Tcl sustituye las
variables antes de que `expr` vea la expresión, y entonces el contenido de una variable se
**reinterpreta como código**:

```tcl
set b "1; exec rm -rf /"
expr $a / $b        ;# sustitución antes de evaluar: agujero de inyección
expr {$a / $b}      ;# correcto: expr recibe los NOMBRES y los resuelve él
```

Es la misma clase de vulnerabilidad que la inyección SQL, con el mismo remedio: **no construyas la
expresión concatenando texto**. Y además, con llaves `expr` compila la expresión una sola vez a
bytecode; sin ellas, la reanaliza en cada vuelta del bucle.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($x, $y) = split ' ', $linea;

printf "suma=%d resta=%d mult=%d div=%d mod=%d\n",
       $x + $y, $x - $y, $x * $y, int($x / $y), $x % $y;
```

**Lo que esta clase enseña en Perl.** **`/` en Perl siempre es división real.** `7 / 2` da `3.5`, no
`3`, porque no hay tipo entero que fuerce la división entera. Por eso el programa usa `int($x / $y)`
para obtener el cociente entero — la división entera de Perl es una división real más un truncado.

Y `%` tiene una particularidad que sorprende: **convierte los operandos a entero primero y sigue el
signo del divisor**, como Python.

```perl
print  7 % 3;      # 1
print -7 % 3;      # 2     -- en C sería -1
print  7 % -3;     # -2
print 7.9 % 3;     # 1     -- 7.9 se trunca a 7 ANTES de operar
```

Ese último caso es el que muerde: `%` no es una operación sobre reales, así que descarta los
decimales sin avisar. Con `use integer` activado en el ámbito, el comportamiento cambia al de C.

Perl tiene además dos operadores que casi ningún lenguaje de esta página ofrece:

```perl
2 ** 10        # 1024 -- potencia, asociativa a la derecha
'-' x 40       # repetición de cadena (clase 051)
10 <=> 3       # 1  -- comparación de TRES vías: -1, 0 o 1
'a' cmp 'b'    # -1 -- lo mismo para cadenas
```

`<=>` —la "nave espacial"— devuelve el orden en un solo valor y es lo que se pasa a `sort`. C++20 la
adoptó veinte años después con el mismo símbolo y el nombre de *operador de comparación de tres vías*.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::cout << "suma=" << (a + b)
              << " resta=" << (a - b)
              << " mult=" << (a * b)
              << " div=" << (a / b)
              << " mod=" << (a % b) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** `/` entre enteros **trunca hacia cero** y `%` sigue el signo del
**dividendo**, comportamiento que quedó garantizado en C++11 y C99 —antes de eso el estándar lo
dejaba a criterio de la implementación, y había compiladores que hacían lo contrario—.

```cpp
-7 / 3      // -2
-7 % 3      // -1
```

Pero lo que esta clase debe subrayar de C++ es otra cosa, y es seria: **la división entera por cero
es comportamiento indefinido**, no una excepción. No es que dé un valor raro: es que el compilador
tiene derecho a asumir que nunca ocurre y **eliminar el código que la rodea**.

```cpp
int f(int a, int b) {
    int r = a / b;        // el compilador deduce: b != 0
    if (b == 0) return -1;// ...y puede BORRAR esta comprobación por inalcanzable
    return r;
}
```

Ese razonamiento es legal y los compiladores lo aplican. La comprobación tiene que ir **antes** de la
división, siempre. Es la diferencia con Ada, donde es `Constraint_Error`, y con Perl o Pascal, donde
es una excepción.

Y hay un segundo caso indefinido que conviene conocer: `INT_MIN / -1` desborda, porque el resultado no
cabe en un `int`. Los dos casos se detectan con `-fsanitize=undefined` en desarrollo.

C++20 añadió `std::div` y, sobre todo, el **operador de tres vías `<=>`**, que genera automáticamente
los seis comparadores a partir de una sola definición.

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

dcl-pi OPERAD;
  a int(10) const;
  b int(10) const;
end-pi;

dcl-s salida char(100);

salida = 'suma='   + %char(a + b)
       + ' resta=' + %char(a - b)
       + ' mult='  + %char(a * b)
       + ' div='   + %char(%div(a : b))
       + ' mod='   + %char(%rem(a : b));
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** Aquí está la trampa más peligrosa de RPG para quien llega de
otro lenguaje, y ya se apuntó en las clases 044 y 049: **el operador `/` redondea, no trunca.**

```rpgle
dcl-s r int(10);
r = 7 / 2;            // 4  -- ¡redondea!  En C, Java y Go sería 3
r = %div(7 : 2);      // 3  -- división entera de verdad
```

RPG define el resultado de `/` según los decimales del **destino**, aplicando redondeo comercial. Con
un destino entero, `7 / 2` da 4. Es aritmética de contable, coherente con un lenguaje de facturación,
y produce errores silenciosos en cualquier algoritmo portado de otro sitio.

Por eso existen **`%div` y `%rem`**, que son la división entera y el resto de verdad, con la
semántica de C —truncan hacia cero, el resto sigue el signo del dividendo—.

Y hay una operación que RPG tiene y casi nadie más: **`%rem` funciona sobre decimales empaquetados**,
no solo sobre enteros. `%rem(10.5 : 3)` es legal. En un lenguaje donde el tipo natural es el decimal
exacto, eso tiene sentido; en C ni siquiera se plantea, porque `%` sobre `double` no compila y hay que
llamar a `fmod`.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 operadores: procedure options(main);

    declare (a, b) fixed binary(31);

    get list (a, b);

    put skip list ('suma='   || trim(char(a + b))            ||
                   ' resta=' || trim(char(a - b))            ||
                   ' mult='  || trim(char(a * b))            ||
                   ' div='   || trim(char(divide(a, b, 31))) ||
                   ' mod='   || trim(char(mod(a, b))));

 end operadores;
```

**Lo que esta clase enseña en PL/I.** `divide(a, b, 31)` en lugar de `a / b`, y ese tercer argumento
es toda la lección: **en PL/I hay que declarar la precisión del resultado de una división**.

La razón vuelve a la matriz base × escala de la clase 043. Al dividir dos `fixed decimal`, ¿cuántos
dígitos y cuántos decimales tiene el resultado? El estándar define una regla, y esa regla suele
producir un resultado con **muchos** decimales que luego se trunca al asignarlo. `divide(a, b, p, q)`
permite decirlo explícitamente: `p` dígitos totales, `q` decimales.

```pli
x = divide(10, 3, 15, 2);     /* 3.33, controlado */
x = 10 / 3;                   /* la regla del estándar decide, y sorprende */
```

Es verboso y es exacto, y es una de las pocas construcciones de PL/I que hoy se echa de menos: en la
mayoría de los lenguajes, el resultado de dividir dos decimales es una sorpresa que se descubre
probando.

Y `mod(a, b)` en PL/I sigue el signo del **divisor**, como Python y Tcl, mientras que la división
trunca — así que **`mod` y `/` no son coherentes entre sí**, al contrario que en Ada. Es un detalle
menor y muy propio del lenguaje: cada pieza es defendible por separado y el conjunto exige leer el
manual.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
OPERAD ; Operadores -- clase 055
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 write "suma=", a + b
 write " resta=", a - b
 write " mult=", a * b
 write " div=", a\b
 write " mod=", a#b, !
 quit
```

**Lo que esta clase enseña en M.** La tabla de operadores de M es la más compacta de esta página, y
la que más se aparta de la convención:

| M | Significado | En casi todos los demás |
|---|---|---|
| `+` `-` `*` | Suma, resta, producto | Igual |
| `/` | División **real** | Igual que Perl |
| `\` | División **entera** | `//`, `div`, `%div` |
| `#` | **Módulo** | `%`, `mod` |
| `**` | Potencia | `**`, `pow()` |
| `_` | **Concatenación** | `+`, `.`, `&`, `\|\|` |
| `!` | **O lógico** | `\|\|` |
| `&` | Y lógico | `&&` |
| `'` | **Negación** | `!` |

Tres de ellos están asignados a símbolos que en otros lenguajes significan cosas distintas —`!` es
*or*, `'` es *not*, `\` es división entera— y esa es la razón principal de que leer M sin conocerlo
sea imposible aunque se sepa programar.

Y hay una regla que sorprende a todo el mundo: **M no tiene precedencia de operadores**. Todas las
expresiones se evalúan **estrictamente de izquierda a derecha**.

```mumps
write 2 + 3 * 4       ; 20, no 14 -- se hace (2+3)*4
write 2 + (3 * 4)     ; 14 -- con paréntesis, lo esperado
```

Es la misma decisión que tomó Smalltalk con sus mensajes binarios, y por un motivo parecido:
simplicidad del analizador. En un lenguaje diseñado para caber en la memoria de un PDP-7, no
implementar una tabla de precedencias era una economía real. Hoy es una trampa que obliga a
parentizar todo.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| partes a b |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

Transcript
    show: 'suma=', (a + b) printString;
    show: ' resta=', (a - b) printString;
    show: ' mult=', (a * b) printString;
    show: ' div=', (a // b) printString;
    show: ' mod=', (a \\ b) printString;
    cr.
```

**Lo que esta clase enseña en Smalltalk.** Los operadores **no existen**: `+`, `-`, `*`, `//` y `\\`
son **mensajes binarios** enviados al número de la izquierda. Están implementados en `Number` y sus
subclases, y se pueden leer en el navegador. Definir `+` en una clase propia no requiere ninguna
sintaxis de "sobrecarga de operadores": basta con implementar un método que se llame `+`.

Smalltalk tiene las dos familias de división, con nombres coherentes:

```smalltalk
7 // 2      "3   -- división AL SUELO"
7 \\ 2      "1   -- resto al suelo, va con //"
-7 // 2     "-4  -- al suelo, no truncado"
-7 \\ 2     "1   -- sigue el signo del DIVISOR"
-7 quo: 2   "-3  -- truncada, como C"
-7 rem: 2   "-1  -- resto truncado, va con quo:"
7 / 2       "7/2 -- ¡una Fraction EXACTA!, como en Lisp"
```

Fíjate en `/`: igual que en Lisp, la división de dos enteros que no dividen exactamente **produce una
fracción**, no un real aproximado ni un entero truncado.

Y la trampa de esta clase, que ya apareció en la 041: **no hay precedencia aritmética**. Los mensajes
binarios se evalúan de izquierda a derecha, así que `2 + 3 * 4` da **20**. Igual que en M, y por la
misma razón de simplicidad — aquí, además, obligada: si `*` es un mensaje como cualquier otro, no
puede tener una precedencia especial sin romper la uniformidad del lenguaje. Los paréntesis de este
programa no son estilo.

---

## Y de vuelta a la clase

Dos cosas que conviene comprobar de cualquier lenguaje nuevo, y que esta clase enseña a preguntar.
**Primera: qué hace el resto con negativos.** Si el lenguaje tiene un solo operador, busca en su
manual si sigue el signo del dividendo (truncada) o del divisor (suelo). **Segunda: qué pasa al
dividir por cero.** Excepción en Ada, Pascal, Lisp, Smalltalk y Perl; comportamiento **indefinido**
en C y C++ para enteros; `Inf` o `NaN` en punto flotante IEEE. Tres respuestas distintas al mismo
error, y solo una de ellas es silenciosa.

⏮️ [Volver a la clase 055](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
