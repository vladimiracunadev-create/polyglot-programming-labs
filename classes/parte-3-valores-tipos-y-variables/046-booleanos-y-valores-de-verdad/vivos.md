# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 046

> [⬅️ Volver a la clase 046](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Tres operaciones lógicas —y, o, no— sobre dos valores de verdad. Parece la clase más simple del
programa y es, de largo, la que más desacuerdo produce entre lenguajes: **la mitad de ellos ni
siquiera tiene un tipo booleano**, y los que lo tienen no se ponen de acuerdo en qué cuenta como
verdadero ni en si un booleano es o no un número.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **la verdad como tipo**, y estos lenguajes son el mejor muestrario que existe.
> COBOL no tiene booleano y lo sustituye por **predicados con nombre** pegados al dato. PL/I usa
> `bit(1)` y comparte los operadores con la manipulación de bits. M y Tcl no tienen tipo y aceptan
> cualquier cosa. Y Smalltalk lleva la idea al extremo contrario: `true` y `false` son **objetos de dos
> clases distintas**, y `ifTrue:` es un método implementado en cada una — el condicional resuelto por
> polimorfismo, no por sintaxis.
>
> Ver esas cinco posturas juntas es lo que convierte "usa booleanos" en una pregunta de diseño.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a b` (cada uno 0 o 1) → stdout: `and=<true|false> or=<true|false> not_a=<true|false>`
- **Regla:** `and = a ∧ b ; or = a ∨ b ; not_a = ¬a (con a,b interpretados como booleanos)`

| stdin | esperado |
|---|---|
| `1 0` | `and=false or=true not_a=false` |
| `1 1` | `and=true or=true not_a=false` |
| `0 0` | `and=false or=false not_a=true` |

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
PROGRAM-ID. BOOLEANOS.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA      PIC X(80).
01  TXT-A      PIC X(20).
01  TXT-B      PIC X(20).
01  A          PIC 9.
    88  A-CIERTO   VALUE 1.
01  B          PIC 9.
    88  B-CIERTO   VALUE 1.
01  R-AND      PIC X(5).
01  R-OR       PIC X(5).
01  R-NOT      PIC X(5).

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    IF A-CIERTO AND B-CIERTO
        MOVE "true"  TO R-AND
    ELSE
        MOVE "false" TO R-AND
    END-IF

    IF A-CIERTO OR B-CIERTO
        MOVE "true"  TO R-OR
    ELSE
        MOVE "false" TO R-OR
    END-IF

    IF NOT A-CIERTO
        MOVE "true"  TO R-NOT
    ELSE
        MOVE "false" TO R-NOT
    END-IF

    DISPLAY "and=" FUNCTION TRIM(R-AND)
            " or=" FUNCTION TRIM(R-OR)
            " not_a=" FUNCTION TRIM(R-NOT)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** Los **niveles 88** en acción. `A` es un dígito; `A-CIERTO` es
un **nombre de condición**: un predicado declarado junto al dato, que se usa sin comparar con nada.
`IF A-CIERTO` en lugar de `IF A = 1`.

La idea es mejor de lo que parece y no tiene equivalente directo en el núcleo. El nivel 88 **da
nombre a un conjunto de valores**, no a uno solo:

```cobol
01  CODIGO-PAIS  PIC X(2).
    88  UNION-EUROPEA  VALUE "ES" "FR" "DE" "IT" "PT" "NL".
    88  DESCONOCIDO    VALUE SPACES.

01  EDAD  PIC 9(3).
    88  MENOR-DE-EDAD  VALUE 0 THRU 17.
    88  JUBILADO       VALUE 65 THRU 999.
```

`IF UNION-EUROPEA` se lee como el negocio lo diría, la lista de países está **pegada al campo** en la
`DATA DIVISION` en lugar de dispersa por el código, y cambiarla es tocar una línea de declaración. En
un lenguaje moderno esto exige un enumerado, un conjunto y una función de pertenencia.

Además se puede asignar: `SET JUBILADO TO TRUE` pone en `EDAD` el primer valor de la lista. Es un
predicado que funciona en las dos direcciones.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program booleanos
   implicit none
   integer :: ia, ib
   logical :: a, b

   read(*, *) ia, ib
   a = (ia /= 0)
   b = (ib /= 0)

   write(*, '(A,A,A,A,A,A)') 'and=', trim(tf(a .and. b)), &
                             ' or=',  trim(tf(a .or. b)),  &
                             ' not_a=', trim(tf(.not. a))
contains

   function tf(v) result(s)
      logical, intent(in) :: v
      character(len=5) :: s
      s = merge('true ', 'false', v)
   end function tf

end program booleanos
```

**Lo que esta clase enseña en Fortran.** Fortran tiene `logical` como tipo intrínseco **desde 1957**,
antes que casi nadie, y con una decisión que hoy sigue siendo suya: **los operadores lógicos van
entre puntos**. `.and.`, `.or.`, `.not.`, `.eqv.` (equivalencia) y `.neqv.` (o exclusivo), y los
literales son `.true.` y `.false.`.

Los puntos no son estética: en el Fortran original **los espacios no eran significativos**, así que
`AND` como palabra suelta se habría confundido con una variable llamada `AND`. Los puntos delimitan
el operador sin ambigüedad. Es un rasgo de sintaxis que existe por una restricción del lector de
tarjetas de 1957 y que sigue ahí.

Fíjate también en `.eqv.` y `.neqv.`: pocos lenguajes tienen operadores lógicos de equivalencia y o
exclusivo. En C escribirías `!a == !b`, con la doble negación necesaria para normalizar.

Y `merge(a, b, cond)` es la joya escondida de esta clase: una función que devuelve `a` si la
condición es cierta y `b` si no. Sobre escalares es un ternario; **sobre arrays es elemento a
elemento**, y esa es su razón de ser: `merge(x, 0.0, x > 0.0)` pone a cero los negativos de un array
completo sin escribir un bucle ni un `if`. Es programación vectorizada aplicada a la lógica.

Y `a = (ia /= 0)` es explícito porque hace falta: en Fortran **un entero no se convierte a `logical`**.
`if (ia)` no compila.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Booleanos is

   function Tf (V : Boolean) return String is
     (if V then "true" else "false");

   Ia, Ib : Integer;
   A, B   : Boolean;
begin
   Get (Ia);
   Get (Ib);
   A := Ia /= 0;
   B := Ib /= 0;

   Put_Line ("and=" & Tf (A and B) &
             " or=" & Tf (A or B) &
             " not_a=" & Tf (not A));
end Booleanos;
```

**Lo que esta clase enseña en Ada.** Ada distingue **cuatro** operadores donde casi todos tienen dos,
y la distinción es deliberada:

| Operador | Evaluación |
|---|---|
| `and` | **Ambos operandos, siempre** |
| `or` | **Ambos operandos, siempre** |
| `and then` | Cortocircuito: si el primero es falso, no evalúa el segundo |
| `or else` | Cortocircuito: si el primero es cierto, no evalúa el segundo |

En C, en Java o en Python, `&&` **siempre** cortocircuita y no tienes elección. En Ada eliges, y
elegir importa por dos motivos opuestos. Si el segundo operando tiene un efecto lateral que debe
ocurrir, quieres `and`. Y si el segundo operando **solo es válido cuando el primero es cierto**,
necesitas `and then`:

```ada
if Indice <= Ultimo and then Tabla (Indice) = Buscado then   --  correcto
if Indice <= Ultimo and      Tabla (Indice) = Buscado then   --  Constraint_Error
```

La segunda línea evalúa el acceso a la tabla aunque el índice esté fuera de rango. En Ada eso no es
un valor basura: es una excepción. Que el lenguaje te obligue a escribir `and then` cuando dependes
del orden hace visible una dependencia que en C queda implícita en la elección de `&&` frente a `&`.

Y `A := Ia /= 0` es obligatorio: en Ada un `Integer` **no** se convierte a `Boolean`. Nunca.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Booleanos;
{$MODE OBJFPC}{$H+}

function Tf(V: Boolean): string;
begin
  if V then Result := 'true' else Result := 'false';
end;

var
  Ia, Ib: Integer;
  A, B: Boolean;

begin
  Read(Ia, Ib);
  A := Ia <> 0;
  B := Ib <> 0;

  WriteLn('and=', Tf(A and B), ' or=', Tf(A or B), ' not_a=', Tf(not A));
end.
```

**Lo que esta clase enseña en Pascal.** Pascal usa **las mismas palabras** —`and`, `or`, `not`— para
la lógica booleana y para las operaciones bit a bit sobre enteros. `5 and 3` da `1` (bits) y
`True and False` da `False` (lógica). El operador se comporta según el tipo de los operandos, que es
posible precisamente porque el tipado es fuerte y el compilador sabe cuál es cuál.

Y aquí está la trampa más famosa del lenguaje, consecuencia de esa decisión: **la precedencia**. En
Pascal, `and` y `or` tienen precedencia **más alta que los operadores de comparación**, porque se
diseñaron pensando en los bits. Por eso esto **no compila**:

```pascal
if a > 0 and b > 0 then      { se lee como:  a > (0 and b) > 0 }
if (a > 0) and (b > 0) then  { correcto: los paréntesis son obligatorios }
```

En C, en Java y en Python la comparación va antes que el `&&`, y los paréntesis sobran. En Pascal son
obligatorios, y ese es el motivo de que el código Pascal esté lleno de paréntesis que parecen
redundantes y no lo son.

Sobre el cortocircuito, Free Pascal y Delphi lo controlan con directivas: `{$B-}` es evaluación
**perezosa** (la habitual, equivalente a `and then` de Ada) y `{$B+}` fuerza a evaluar los dos
operandos. El ISO no lo garantiza, así que en código portable no conviene depender de él.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(flet ((tf (v) (if v "true" "false")))
  (let* ((ia (read))
         (ib (read))
         (a (/= ia 0))
         (b (/= ib 0)))
    (format t "and=~A or=~A not_a=~A~%"
            (tf (and a b)) (tf (or a b)) (tf (not a)))))
```

**Lo que esta clase enseña en Common Lisp.** `and` y `or` **no son funciones: son macros**, y esa
diferencia es exactamente el tema del cortocircuito. Una función evalúa todos sus argumentos antes de
recibirlos; una macro recibe el código sin evaluar y decide qué hacer con él. Por eso `and` puede
parar en cuanto encuentra un `nil`: no le llegaron valores, le llegaron expresiones.

Y devuelven algo más útil que un booleano: **`and` devuelve el último valor si todos son verdaderos,
y `or` devuelve el primero verdadero**.

```lisp
(and 1 2 3)          ; => 3
(and 1 nil 3)        ; => nil
(or nil nil "hola")  ; => "hola"
(or (buscar-cache) (buscar-disco) "por-defecto")
```

Esa última línea es el idioma clásico: una cadena de alternativas donde gana la primera que dé algo.
JavaScript, Python y Ruby copiaron después este comportamiento —`a || b` devuelve un valor, no un
booleano— y viene de aquí.

`flet` define funciones **locales** al bloque, la contrapartida de `let` para funciones. Su pariente
`labels` permite además que la función se llame a sí misma, y existen las dos por la misma razón que
existen `let` y `let*`: Lisp prefiere que el ámbito se declare en vez de suponerse.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
proc tf {v} { return [expr {$v ? "true" : "false"}] }

gets stdin linea
lassign [split [string trim $linea]] ia ib

set a [expr {$ia != 0}]
set b [expr {$ib != 0}]

puts "and=[tf [expr {$a && $b}]] or=[tf [expr {$a || $b}]] not_a=[tf [expr {!$a}]]"
```

**Lo que esta clase enseña en Tcl.** Tcl acepta como verdaderos `1`, `true`, `yes`, `on` y cualquier
número distinto de cero; como falsos, `0`, `false`, `no`, `off` y la cadena vacía. Cualquier otra
cadena —`"quizá"`— **provoca un error**, no un valor por defecto. Es más estricto que Perl, que
simplemente la consideraría verdadera.

Pero **devuelve `1` o `0`**, nunca `true` o `false`. Por eso este programa necesita `tf`: la salida
de `expr` es un número, aunque acepte palabras a la entrada.

Los operadores lógicos solo existen **dentro de `expr`**, que es su propio mini-lenguaje con
precedencia estilo C. Fuera de `expr` no hay `&&` ni `||` porque no hay operadores en Tcl, solo
comandos. Y `if` es un comando que recibe la condición como una cadena y la pasa a `expr`, lo que
explica una regla que confunde a todo el mundo:

```tcl
if {$a && $b} { ... }     ;# correcto: llaves, se evalúa una vez y compilado
if "$a && $b" { ... }     ;# funciona, es más lento y permite inyección
```

Las llaves impiden la sustitución previa de variables. Es la misma regla de `expr` de la clase 041, y
por el mismo motivo.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

sub tf { return $_[0] ? 'true' : 'false' }

my $linea = <STDIN>;
chomp $linea;
my ($ia, $ib) = split ' ', $linea;

my $a = ($ia != 0);
my $b = ($ib != 0);

printf "and=%s or=%s not_a=%s\n", tf($a && $b), tf($a || $b), tf(!$a);
```

**Lo que esta clase enseña en Perl.** La lista de valores falsos de Perl es **exactamente cinco**, y
conviene memorizarla porque no coincide con la de ningún otro lenguaje: `0`, `"0"`, `""`, `undef` y
la lista vacía. Todo lo demás es verdadero — incluidas `"0.0"`, `"00"` y `" "`, que sorprenden
siempre.

Y Perl tiene **dos juegos de operadores lógicos** que hacen lo mismo con distinta precedencia:

```perl
my $x = $a || 'por defecto';    # || tiene precedencia ALTA
my $x = $a or 'por defecto';    # or tiene precedencia BAJÍSIMA — ¡asigna $a!

open(my $fh, '<', $f) or die "no puedo abrir: $!";   # el idioma correcto
```

`or` y `and` están pensados para **control de flujo al final de una sentencia**, con precedencia
menor que la asignación, y `||` y `&&` para expresiones. Usar el equivocado es un error clásico que
`use warnings` no siempre atrapa.

Perl añadió después `//`, el operador de **coalescencia de nulos**: devuelve el lado derecho solo si
el izquierdo es `undef`, no si es falso. Es la diferencia entre "no tiene valor" y "vale cero", y
`$contador // 10` hace lo correcto donde `$contador || 10` fallaría con un contador a cero.
JavaScript adoptó `??` con la misma semántica veinte años después.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    int ia{}, ib{};
    if (!(std::cin >> ia >> ib)) return 1;

    const bool a = ia != 0;
    const bool b = ib != 0;

    std::cout << std::boolalpha
              << "and=" << (a && b)
              << " or=" << (a || b)
              << " not_a=" << (!a) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ tiene `bool` como tipo propio desde el principio —C tuvo
que esperar a C99 y su `_Bool`— pero **conserva la conversión implícita a y desde entero**, y ahí
está toda la enseñanza de esta clase.

La distinción que hay que tener clara es entre los operadores **lógicos** y los **de bits**:

| | Lógico | Bits |
|---|---|---|
| Y | `&&` — cortocircuita | `&` — no cortocircuita |
| O | `\|\|` — cortocircuita | `\|` — no cortocircuita |
| No | `!` | `~` |

Escribir `&` donde iba `&&` compila sin avisar y casi siempre da el mismo resultado con booleanos,
así que el error sobrevive a las pruebas… hasta que el segundo operando tiene un efecto lateral o
desreferencia un puntero que no debía evaluarse. Es un error real y difícil de ver en revisión.

C++11 añadió `explicit operator bool()` para que una clase pueda usarse en un `if` **sin** convertirse
accidentalmente a entero. Es lo que hace `std::cin` y lo que permite escribir
`if (!(std::cin >> a))` como en este programa: el flujo se convierte a booleano solo donde se espera
un booleano, no en una suma.

Y `std::boolalpha` imprime `true`/`false`; sin él saldrían `1` y `0`.

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

dcl-pi BOOLEANOS;
  ia int(10) const;
  ib int(10) const;
end-pi;

dcl-s a      ind;
dcl-s b      ind;
dcl-s salida char(60);

a = (ia <> 0);
b = (ib <> 0);

salida = 'and=' + tf(a and b)
       + ' or=' + tf(a or b)
       + ' not_a=' + tf(not a);
dsply salida;

*inlr = *on;
return;

dcl-proc tf;
  dcl-pi *n varchar(5);
    v ind const;
  end-pi;
  if v = *on;
    return 'true';
  endif;
  return 'false';
end-proc;
```

**Lo que esta clase enseña en RPG.** El tipo booleano de RPG se llama **`ind`** (*indicator*) y sus
valores son **`*on` y `*off`**, no `true` y `false`. Ese vocabulario no es un capricho: viene
directamente de los **indicadores del ciclo del programa**, las variables globales numeradas
`*IN01`…`*IN99` que en el RPG clásico controlaban absolutamente todo.

En aquel modelo, un indicador se encendía al leer el último registro, otro al cambiar un nivel de
control, otro al fallar una comparación. El código estaba lleno de `IF *IN37` sin ninguna pista de
qué significaba el 37. La deuda técnica característica de RPG es un programa de tres mil líneas donde
los indicadores son la única lógica y nadie recuerda su significado.

`dcl-s a ind` es la respuesta moderna: **un booleano con nombre**, con tipo, local a su procedimiento.
Es exactamente el mismo movimiento que hizo COBOL con los niveles 88 —dar nombre a la condición— pero
llegando desde el otro extremo.

Los operadores son palabras: `and`, `or`, `not`, y las comparaciones `=`, `<>`, `>=`. RPG **no**
convierte números a indicadores: `a = ia` no compila, hay que escribir la comparación.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 booleanos: procedure options(main);

    declare (ia, ib) fixed binary(31);
    declare (a, b)   bit(1);

    get list (ia, ib);
    a = (ia ^= 0);
    b = (ib ^= 0);

    put skip list ('and='   || tf(a & b)  ||
                   ' or='   || tf(a | b)  ||
                   ' not_a='|| tf(^a));

 tf: procedure (v) returns (character(5) varying);
    declare v bit(1);
    if v then return ('true');
    return ('false');
 end tf;

 end booleanos;
```

**Lo que esta clase enseña en PL/I.** El booleano de PL/I es **`bit(1)`**: una cadena de bits de
longitud uno. No hay tipo `boolean`; hay cadenas de bits de longitud arbitraria, y la de longitud 1
hace de valor de verdad. Los literales son `'1'b` y `'0'b`.

La consecuencia es que **los operadores lógicos y los de bits son los mismos**: `&`, `|` y `^` (o `¬`
en teclados que lo tengan) operan bit a bit sobre cadenas de cualquier longitud, y sobre `bit(1)`
resultan ser la lógica booleana. `'1100'b & '1010'b` da `'1000'b`.

Es elegante y unifica dos conceptos que casi todos los lenguajes separan. También significa que **no
hay cortocircuito**: `&` es una operación sobre datos, no una estructura de control, así que evalúa
siempre los dos lados. Para el cortocircuito hay que escribir `if` anidados. C —diseñado poco
después, con la misma idea de la verdad como número— sí separó `&` de `&&` precisamente por esto.

Y ojo con la conversión: PL/I convierte casi cualquier cosa a `bit`, incluidos los caracteres y los
números. Es cómodo y es la razón de que sus errores se manifiesten tarde, como se vio en la clase 041.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
BOOL ; Booleanos -- clase 046
 read linea
 set ia = $piece(linea, " ", 1)
 set ib = $piece(linea, " ", 2)
 set a = ''ia
 set b = ''ib
 write "and=", $$tf(a & b)
 write " or=", $$tf(a ! b)
 write " not_a=", $$tf('a), !
 quit
 ;
tf(v) ; booleano a texto
 quit $select(v : "true", 1 : "false")
```

**Lo que esta clase enseña en M.** M no tiene tipo booleano, y su regla de verdad es **la más simple
de toda la página y la más peligrosa**: un valor es verdadero si su **interpretación numérica** es
distinta de cero.

Como M convierte texto a número leyendo el prefijo y descartando el resto, eso significa que
`"0abc"` es **falso** —su valor numérico es 0— y `"1abc"` es **verdadero**. La cadena `"hola"` vale 0
y por tanto es falsa. Es tipado débil llevado al límite.

Los operadores son símbolos de un carácter, y esta es la lista que hay que conocer:

| Operador | Significado |
|---|---|
| `&` | Y lógico |
| `!` | **O lógico** — no "no", como en C |
| `'` | **No** — el apóstrofo |
| `'=` | Distinto (el `'` niega el operador siguiente) |

Que `!` sea el **or** y no la negación es la confusión número uno para quien llega de C. Y `'` como
negación se puede pegar delante de cualquier operador de comparación: `'=`, `'<`, `'>`.

`set a = ''ia` no es un error tipográfico: es la **doble negación**, el idioma de M para normalizar
cualquier valor a exactamente `1` o `0`. El mismo truco que `!!x` en C y JavaScript.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| partes ia ib a b tf |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
ia := partes first.
ib := partes second.

a := ia ~= 0.
b := ib ~= 0.

tf := [ :v | v ifTrue: [ 'true' ] ifFalse: [ 'false' ] ].

Transcript
    show: 'and=', (tf value: (a and: [ b ]));
    show: ' or=', (tf value: (a or: [ b ]));
    show: ' not_a=', (tf value: a not);
    cr.
```

**Lo que esta clase enseña en Smalltalk.** Esta es **la** clase de Smalltalk. `true` y `false` no son
literales de un tipo primitivo: son las **únicas instancias** de las clases `True` y `False`, ambas
subclases de `Boolean`. Y los operadores lógicos son **métodos implementados en cada una de las dos
clases**. El código real, que puedes abrir en el navegador de clases, es esencialmente este:

```smalltalk
True >> ifTrue: bloqueV ifFalse: bloqueF     ^ bloqueV value
False >> ifTrue: bloqueV ifFalse: bloqueF    ^ bloqueF value

True >> not     ^ false
False >> not    ^ true

True >> and: unBloque     ^ unBloque value
False >> and: unBloque    ^ false
```

**No hay ninguna estructura de control.** El condicional es despacho de mensajes: se envía
`ifTrue:ifFalse:` al objeto, y el objeto —según sea `true` o `false`— evalúa un bloque u otro. Es la
demostración más limpia que existe de que "todo es un objeto" no era un eslogan.

Y ahí está la razón de los corchetes en `a and: [ b ]`: **`and:` recibe un bloque, no un valor**. Si
recibiera un valor, `b` ya se habría evaluado y no habría cortocircuito. Al recibir un bloque, `False`
simplemente no lo evalúa. **El cortocircuito no es una regla del lenguaje: es una consecuencia de
pasar código en vez de datos.** Existen además `&` y `|`, que sí evalúan los dos lados porque reciben
valores — la misma distinción que `&&` y `&` en C++, obtenida sin sintaxis especial.

---

## Y de vuelta a la clase

La pregunta que deja esta clase no es "¿tiene booleanos mi lenguaje?" sino **"¿qué considera
verdadero mi lenguaje, y qué pasa si le doy algo que no es un booleano?"**. Ada y Pascal responden
"no compila". C++ responde "lo convierto a número". Perl, Tcl y M responden con una lista de valores
falsos que hay que memorizar —y que **no coincide entre ellos**: `"0"` es falso en Perl y verdadero
en Python—. Esa lista es la primera que conviene aprender de cualquier lenguaje nuevo.

⏮️ [Volver a la clase 046](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
