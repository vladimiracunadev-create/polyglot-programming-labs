# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 041

> [⬅️ Volver a la clase 041](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Esta página resuelve **el problema de esta clase** —el total de una venta— en los lenguajes antiguos
que **siguen ejecutándose hoy en producción**. Y lo hace preguntando, en cada uno, lo que pregunta
esta clase: **¿cómo se escribe un literal, cómo se nombra un valor y cómo se promete que un nombre
no cambiará?**

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md): que **se
> ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a la vista un
> concepto que los diez del núcleo esconden**.
>
> Aquí ese concepto es el **enlace entre un nombre y un valor**, que es exactamente el tema de la
> clase. Y resulta que estos lenguajes lo resuelven de formas que el núcleo ya no muestra: COBOL
> declara la **forma exacta** del literal antes de usarlo, Ada tiene **números con nombre** sin tipo
> y de precisión ilimitada, Smalltalk escribe literales **decimales exactos**, y MUMPS directamente
> **no tiene declaraciones ni constantes**. Ver cuatro respuestas distintas a la misma pregunta es lo
> que convierte `const` de palabra memorizada en decisión comprendida.
>
> Y ninguno de ellos es una foto fija: casi todos han incorporado en los últimos años JSON, REST,
> GPU, Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `precio_unitario cantidad descuento`
- **Salida** (stdout): `Total: <total con 2 decimales>`
- **Regla:** `total = precio_unitario * cantidad * (1 - descuento)`

| stdin | esperado |
|---|---|
| `15000 2 0.10` | `Total: 27000.00` |
| `999.9 3 0` | `Total: 2999.70` |
| `5000 0 0.20` | `Total: 0.00` |

> **Qué está verificado en esta página.** Los ocho lenguajes de la sección 🟢 se **ejecutan en CI**
> contra este mismo `casos.json`, igual que las diez implementaciones del núcleo
> ([workflow Labs](../../../labs/README.md)). Los de la sección 🟡 **no pueden** cumplir este
> contrato sin falsear el lenguaje, y se explica por qué. Los de la sección ⚪ sí podrían, pero su
> cadena de herramientas no está en los *runners*: son correctos, sin sello de máquina.

---

## 🟢 Se ejecutan en CI

### COBOL

[Ficha completa](../../../atlas/cobol.md) · Banca, seguros, gobierno, medios de pago ·
`cobc -x -free total.cob`

```cobol
IDENTIFICATION DIVISION.
PROGRAM-ID. TOTAL-VENTA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA           PIC X(80).
01  TXT-PRECIO      PIC X(20).
01  TXT-CANTIDAD    PIC X(20).
01  TXT-DESCUENTO   PIC X(20).
01  PRECIO          PIC 9(9)V99   COMP-3.
01  CANTIDAD        PIC 9(9)V99   COMP-3.
01  DESCUENTO       PIC 9V9(4)    COMP-3.
01  TOTAL-CALC      PIC 9(12)V99  COMP-3.
01  TOTAL-EDITADO   PIC ZZZZZZZZZ9.99.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES
        INTO TXT-PRECIO TXT-CANTIDAD TXT-DESCUENTO
    END-UNSTRING
    MOVE FUNCTION NUMVAL(TXT-PRECIO)    TO PRECIO
    MOVE FUNCTION NUMVAL(TXT-CANTIDAD)  TO CANTIDAD
    MOVE FUNCTION NUMVAL(TXT-DESCUENTO) TO DESCUENTO
    COMPUTE TOTAL-CALC ROUNDED = PRECIO * CANTIDAD * (1 - DESCUENTO)
    MOVE TOTAL-CALC TO TOTAL-EDITADO
    DISPLAY "Total: " FUNCTION TRIM(TOTAL-EDITADO)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** Aquí **la variable se declara antes que nada y con su forma
exacta**: `PIC 9(9)V99 COMP-3` no dice "un número", dice nueve dígitos enteros, dos decimales, coma
implícita y representación decimal empaquetada. No hay inferencia de tipo, no hay literal que decida
por ti, no hay conversión silenciosa. En Python escribes `precio = 15000` y el lenguaje elige; en
COBOL eliges tú, y esa elección queda escrita para quien audite el programa dentro de treinta años.

Y la **constante** existe desde el primer día, en la propia declaración:

```cobol
01  IVA          PIC 9V99  VALUE 0.19.
01  MAX-DESC     PIC 9V99  VALUE 0.50.
78  NOMBRE-APP   VALUE "Facturación".   *> nivel 78: constante de verdad
```

La cláusula `VALUE` da el valor inicial; el **nivel 78** (y `CONSTANT` desde COBOL 2002) declara algo
que **no se puede modificar**. COBOL tiene además **constantes figurativas** —`ZERO`, `SPACES`,
`HIGH-VALUES`, `LOW-VALUES`— que son literales con nombre incorporados al lenguaje: `MOVE SPACES TO
LINEA` rellena de espacios sin importar cuánto mida el campo.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK ·
`gfortran -O2 total.f90`

```fortran
program total_venta
   implicit none
   real(kind=8) :: precio, cantidad, descuento, total
   character(len=32) :: buffer

   read(*, *) precio, cantidad, descuento
   total = precio * cantidad * (1.0d0 - descuento)

   write(buffer, '(F20.2)') total
   write(*, '(A)') 'Total: ' // trim(adjustl(buffer))
end program total_venta
```

**Lo que esta clase enseña en Fortran.** Dos lecciones sobre literales, y las dos son trampas reales.

La primera: **`implicit none`**. Sin esa línea, una variable no declarada **no es un error**: Fortran
le asigna tipo según su inicial (`i`–`n` enteros, el resto reales), herencia directa de 1957. Un
`totl` mal tecleado se convertiría en un real nuevo con valor basura, en silencio. Es el mismo
problema que resuelven `use strict` en Perl y `Option Explicit` en VBA, y es la razón de que la
primera línea de todo Fortran serio sea siempre la misma.

La segunda: **el literal lleva su precisión encima**. `1.0` es precisión simple; `1.0d0` es doble.
Escribir `1.0` en una expresión de dobles introduce una conversión y puede perder dígitos. La forma
portable y moderna es declarar el *kind* y usarlo en el literal:

```fortran
use iso_fortran_env, only: real64
real(real64) :: total
real(real64), parameter :: IVA = 0.19_real64   ! constante: valor fijado al compilar
```

`parameter` es la constante de Fortran: se evalúa **en tiempo de compilación** y no puede aparecer a
la izquierda de una asignación. El sufijo `_real64` en el literal es lo que garantiza que la
constante nazca ya con la precisión correcta.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa ·
`gnatmake total_venta.adb`

```ada
with Ada.Text_IO;            use Ada.Text_IO;
with Ada.Long_Float_Text_IO; use Ada.Long_Float_Text_IO;

procedure Total_Venta is

   --  El tipo dice lo que el negocio permite, no solo lo que la máquina guarda.
   subtype Descuento_T is Long_Float range 0.0 .. 1.0;

   Precio, Cantidad : Long_Float;
   Descuento        : Descuento_T;
   Total            : Long_Float;

begin
   Get (Precio);
   Get (Cantidad);
   Get (Descuento);          --  un 1.5 aquí levanta Constraint_Error

   Total := Precio * Cantidad * (1.0 - Descuento);

   Put ("Total: ");
   Put (Total, Fore => 1, Aft => 2, Exp => 0);
   New_Line;
end Total_Venta;
```

**Lo que esta clase enseña en Ada.** Ada tiene **dos clases de constante distintas**, y la segunda no
existe en ningún lenguaje del núcleo:

```ada
--  1) Constante con tipo: como el `const` que ya conoces.
IVA : constant Long_Float := 0.19;

--  2) NÚMERO CON NOMBRE: sin tipo, exacto, evaluado con precisión ilimitada.
Pi         : constant := 3.14159_26535_89793_23846;
Un_Millon  : constant := 1_000_000;
Tercio     : constant := 1.0 / 3.0;   --  se guarda como fracción exacta
```

Un **número con nombre** (`constant` sin tipo) no es un `Float` ni un `Integer`: es un valor
matemático que el compilador manipula con precisión arbitraria y **solo convierte al tipo concreto en
el punto donde se usa**. `Tercio` no arrastra el error de redondeo de un `Float`; ese error aparece —
si aparece— al final. Es una separación entre *el valor* y *su representación* que casi ningún
lenguaje hace, y es exactamente la distinción que esta clase intenta enseñar.

Fíjate también en el **subrayado como separador** en `3.14159_26535` y `1_000_000`: Ada lo introdujo
en 1983, y hoy lo han copiado Java, C#, Python, Rust, Ruby, C++ y Go. Y en que `Descuento` no es un
`Long_Float` cualquiera: su tipo lleva escrito el rango legal, así que un descuento de 1.5 **detiene
el programa en el punto exacto** en lugar de producir un total negativo.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · [Object Pascal / Delphi](../../../atlas/delphi.md):
escritorio empresarial, TPV, industria · `fpc -Mobjfpc total_venta.pas`

```pascal
program TotalVenta;
{$MODE OBJFPC}{$H+}

var
  Precio, Cantidad, Descuento, Total: Double;

begin
  Read(Precio, Cantidad, Descuento);

  Total := Precio * Cantidad * (1 - Descuento);

  WriteLn('Total: ', Total:0:2);
end.
```

**Lo que esta clase enseña en Pascal.** Wirth diseñó este lenguaje precisamente alrededor del tema de
esta clase, y se nota en dos decisiones.

La primera: **`:=` asigna y `=` compara.** No es cosmética. En C, `if (x = 5)` compila, asigna y
evalúa como verdadero; es uno de los errores más caros de la historia del lenguaje. En Pascal es
**imposible de escribir**. La distinción entre "ligar un nombre a un valor" y "preguntar si dos
valores son iguales" está en la sintaxis, no en la disciplina del programador.

La segunda: **las constantes tienen sección propia**, y las hay de dos clases:

```pascal
const
  IVA        = 0.19;          { sin tipo: el compilador lo deduce en cada uso }
  MAX_DESC: Double = 0.50;    { con tipo: en Delphi/FPC es una variable de solo lectura }
  EMPRESA    = 'Ferretería';
```

Una constante **sin tipo** es un literal con nombre: se sustituye donde se usa y se adapta al
contexto. Una constante **con tipo** ocupa memoria de verdad y —detalle histórico que sorprende— con
la directiva `{$J+}` heredada de Turbo Pascal **podía modificarse**. Es un buen recordatorio de que
"constante" significa cosas distintas en lenguajes distintos, que es justo lo que esta clase quiere
que compruebes.

Y `Total:0:2` es formateo **en la propia sintaxis** del `Write`: ancho mínimo 0, dos decimales, sin
cadena de plantilla y sin depender de la configuración regional.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación ·
`sbcl --script total-venta.lisp`

```lisp
;;; total-venta.lisp — clase 041
(setf *read-default-float-format* 'double-float)

(let* ((precio    (read))
       (cantidad  (read))
       (descuento (read))
       (total     (* precio cantidad (- 1 descuento))))
  (format t "Total: ~,2F~%" total))
```

**Lo que esta clase enseña en Common Lisp.** Aquí el literal es un concepto **más profundo** que en
cualquier otro lenguaje de esta página, por dos motivos.

Primero: **`(read)` no analiza una cadena, lee un objeto de Lisp.** El mismo lector que interpreta el
código fuente interpreta la entrada del usuario. `15000` llega como entero, `0.10` como real, y si
escribieras `(1 2 3)` llegaría como una lista. No hay `split`, ni `parseFloat`, ni conversión: **los
literales del programa y los datos de entrada son la misma cosa**. Esa identidad es la
homoiconicidad, y esta clase es donde primero se puede tocar.

Segundo: Lisp tiene **literales que otros lenguajes no tienen**, incluidos los números racionales
exactos:

```lisp
(/ 1 3)          ; => 1/3      un racional EXACTO, no 0.3333333
(* 3 (/ 1 3))    ; => 1        sin error de redondeo
(expt 2 200)     ; => 1606938044258990275541962092341162602522202993782792835301376
```

Un entero de Lisp no tiene tamaño máximo y una fracción no se convierte a decimal salvo que lo pidas.
Compara con el `int` de 32 bits de la mayoría del núcleo.

Y para nombrar valores hay **tres formas, con significados distintos**:

```lisp
(defconstant  +iva+  0.19)      ; constante: redefinirla es un error
(defparameter *tasa* 0.19)      ; global pensada para cambiarse a mano
(defvar       *log*  nil)       ; global que NO se pisa si ya tenía valor
(let ((x 1)) ...)               ; ligadura local
```

Las convenciones tipográficas —`+constantes+`, `*especiales*`— no las impone el compilador: las
impone la comunidad, y son universales. Que el lenguaje distinga `defparameter` de `defvar` (una se
reinicia al recargar el fichero, la otra no) muestra hasta qué punto Lisp se toma en serio el
**momento** en que un nombre se liga a un valor, que es el *binding time* del que habla esta clase.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing ·
`tclsh total.tcl`

```tcl
gets stdin linea
lassign [split [string trim $linea]] precio cantidad descuento
set total [expr {$precio * $cantidad * (1 - $descuento)}]
puts [format "Total: %.2f" $total]
```

**Lo que esta clase enseña en Tcl.** Es el caso límite y por eso vale la pena verlo: **en Tcl todos
los valores son cadenas.** `15000` no es un entero que se imprime como texto; es el texto `"15000"`
que `expr` decide leer como número. No hay literales numéricos, no hay literales booleanos, no hay
tipos: hay cadenas y comandos que las interpretan.

Eso responde de golpe a la pregunta de la clase sobre tipado débil. Cuando en JavaScript te
sorprende que `"5" * 2` dé `10`, estás viendo una versión atenuada de lo que Tcl hace como principio
de diseño declarado (*Everything Is A String*).

Sobre **constantes**: durante treinta años Tcl no tuvo ninguna, y la convención era el nombre en
mayúsculas y la disciplina del equipo. **Tcl 9.0 (2024) añadió `const`**:

```tcl
const IVA 0.19
set IVA 0.21    ;# error: can't set "IVA": variable is a constant
```

Que un lenguaje de 1988 incorpore constantes en 2024 dice dos cosas: que sigue en desarrollo, y que
esta clase trata de un problema que nunca deja de ser relevante.

Y el detalle crítico: **`expr` siempre con llaves**. Sin ellas, Tcl sustituye las variables *antes*
de pasar el texto a `expr`, lo que es más lento y —si una variable contiene texto arbitrario— abre
una vía de inyección. Es la regla número uno del lenguaje.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl total.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

my ($precio, $cantidad, $descuento) = split ' ', $linea;
my $total = $precio * $cantidad * (1 - $descuento);

printf "Total: %.2f\n", $total;
```

**Lo que esta clase enseña en Perl.** Los **sigilos** son una respuesta distinta a la pregunta de qué
declara un nombre: `$` no dice "esto es un número" ni "esto es una cadena", dice **"esto se está
usando como un valor único"**. `@lista` es la lista entera y `$lista[0]` es un elemento —con `$`,
porque un elemento suelto es un escalar—. El sigilo describe **la forma del acceso**, no el tipo del
dato. Es un eje que ningún lenguaje del núcleo tiene.

Y por eso `$precio` puede contener `"15000"` y multiplicarse sin conversión explícita: el escalar de
Perl guarda a la vez una representación numérica y una textual, y usa la que pida el contexto.

Las constantes se declaran con un módulo, no con sintaxis:

```perl
use constant IVA      => 0.19;
use constant MAX_DESC => 0.50;
use constant COLORES  => ('rojo', 'verde');   # también listas

print IVA;      # 0.19  — es una subrutina en línea, no una variable: sin sigilo
```

Que `use constant` sea un **módulo** y no una palabra clave es muy representativo de Perl: la
constante se implementa como una subrutina que devuelve siempre lo mismo y que el compilador
sustituye en línea. El lenguaje prefiere dar herramientas para construir la característica antes que
incorporarla.

Y `use strict` es aquí lo mismo que `implicit none` en Fortran: sin él, `$totl` mal tecleado crea una
variable global nueva con valor indefinido y el programa imprime `Total: 0.00` sin quejarse.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC ·
`g++ -std=c++17 total.cpp`

```cpp
#include <iomanip>
#include <iostream>

int main() {
    double precio{}, cantidad{}, descuento{};

    if (!(std::cin >> precio >> cantidad >> descuento)) {
        return 1;
    }

    const double total = precio * cantidad * (1 - descuento);

    std::cout << "Total: " << std::fixed << std::setprecision(2) << total << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** Es el lenguaje con **más grados de constancia** de todos, y
compararlos aclara qué significa realmente "constante":

```cpp
const     double IVA   = 0.19;              // no se puede modificar
constexpr double IVA2  = 0.19;              // además, se conoce AL COMPILAR
consteval double doble(double x){return 2*x;} // OBLIGA a evaluarse al compilar
constinit double tabla = calcular();         // inicializada antes de main()

constexpr int TAM = 10;
int datos[TAM];        // solo compila porque TAM es constexpr, no solo const
```

`const` es una promesa sobre **quién puede escribir**; `constexpr` es una afirmación sobre **cuándo se
conoce el valor**. Son ejes independientes, y esa distinción —que en Python o JavaScript ni siquiera
se puede expresar— es la versión más precisa del *binding time* que estudia esta clase: `constexpr`
liga el valor en tiempo de compilación, `const` solo restringe la mutación en ejecución.

Los literales también llevan información: `27000.0` es `double`, `27000.0f` es `float`, `27000ULL` es
un entero largo sin signo, `0b1101` es binario y `1'000'000` usa la comilla simple como separador
(C++14, la misma idea que Ada popularizó). Y `double precio{}` con llaves inicializa a cero **y**
prohíbe las conversiones que pierden información, algo que `=` permitiría en silencio.

---

## 🟡 Contrato adaptado, y declarado

Estos lenguajes **no pueden** leer de `stdin` y escribir en `stdout` sin dejar de ser ellos mismos.
No es una limitación del material: es su naturaleza. Aquí el cálculo es el mismo y la forma de entrar
y salir es la de su anfitrión. **No pasan por el verificador**, y se dice.

### RPG

[Ficha completa](../../../atlas/rpg.md) · IBM i: ERP, retail, logística, manufactura ·
`CRTBNDRPG` sobre IBM i

> En IBM i un programa recibe sus datos por **parámetros**, por un **fichero** o por una **pantalla**,
> nunca por la entrada estándar.

```rpgle
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi TOTVTA;
  precio    packed(11:2) const;
  cantidad  packed(11:2) const;
  descuento packed(5:4)  const;
end-pi;

dcl-c IVA       0.19;             // constante con nombre
dcl-c MAX_DESC  0.50;

dcl-s total  packed(15:2) inz(0); // variable, con valor inicial explícito
dcl-s salida char(40);

total = precio * cantidad * (1 - descuento);

salida = 'Total: ' + %char(total);
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** La distinción entre constante y variable es **sintáctica y
tajante**: `dcl-c` declara una constante con nombre —no ocupa memoria, no puede aparecer a la
izquierda de una asignación— y `dcl-s` declara una variable independiente, con su valor inicial en
`inz()`. Son dos palabras clave distintas, no un modificador.

Y el tipo del dinero es `packed(11:2)`: **decimal empaquetado**, aritmética exacta, la misma decisión
que toma COBOL. Cuando esta clase pregunta "¿qué tipo tiene el literal `15000`?", la respuesta en un
ERP no es "un entero": es "once dígitos con dos decimales, en decimal, porque es dinero".

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · IBM Enterprise PL/I

```pli
 total_venta: procedure options(main);

    declare precio     fixed decimal(11,2);
    declare cantidad   fixed decimal(11,2);
    declare descuento  fixed decimal(5,4);
    declare total      fixed decimal(15,2);
    declare presenta   picture 'ZZZZZZZZZ9V.99';

    declare IVA        fixed decimal(3,2) value (0.19);   /* constante */

    on endfile(sysin) stop;

    get list (precio, cantidad, descuento);

    total = precio * cantidad * (1 - descuento);

    presenta = total;
    put skip list ('Total: ' || trim(presenta));

 end total_venta;
```

**Lo que esta clase enseña en PL/I.** Es el único lenguaje de esta página que separa explícitamente
las **dos dimensiones** de un número: la **base** (decimal o binaria) y la **escala** (fija o
flotante). Existen las cuatro combinaciones:

```pli
declare a fixed decimal(11,2);   /* dinero: exacto, base 10 */
declare b fixed binary(31);      /* entero de máquina */
declare c float decimal(15);     /* real con precisión decimal */
declare d float binary(53);      /* el `double` de siempre */
```

Casi todos los lenguajes modernos te dan `int` y `double` y ocultan que esas son solo dos casillas de
una matriz de cuatro. PL/I las pone las cuatro sobre la mesa porque nació para unir el mundo
científico de Fortran con el empresarial de COBOL. El atributo `value` declara la constante, y la
`picture` es un dato numérico de imagen: la misma idea que el campo editado de COBOL.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · YottaDB

```mumps
TOTVTA ; Total de una venta -- clase 041
 read linea
 set precio    = $piece(linea, " ", 1)
 set cantidad  = $piece(linea, " ", 2)
 set descuento = $piece(linea, " ", 3)
 set total     = precio * cantidad * (1 - descuento)
 write "Total: ", $justify(total, 0, 2), !
 quit
```

**Lo que esta clase enseña en M.** Es la respuesta más radical de toda la página: **no hay
declaraciones, no hay tipos y no hay constantes.** Ninguna de las tres cosas. Una variable existe
desde que se le asigna algo, todo valor es una cadena, y si quieres una constante la escribes en
mayúsculas y confías en el equipo.

Suena primitivo hasta que aparece la línea que hace único a M:

```mumps
 set ^VENTAS($horolog, "total") = total
```

El circunflejo cambia todo: `^VENTAS` es un **global**, es decir, **una variable persistente**. Eso
ya está en disco, es transaccional y lo ven todos los procesos, con la misma sintaxis con la que
escribirías una variable local. La pregunta de esta clase —qué es una variable, cuánto vive el enlace
entre un nombre y un valor— tiene en M una tercera respuesta que el núcleo no contempla: **el enlace
puede sobrevivir al programa**. Sin ORM, sin `INSERT`, sin serializar. Un carácter de diferencia.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · Pharo

```smalltalk
| linea partes precio cantidad descuento total |

linea := stdin nextLine.
partes := linea substrings collect: [ :cada | cada asNumber ].

precio    := partes first.
cantidad  := partes second.
descuento := partes third.

total := precio * cantidad * (1 - descuento).

Transcript
    show: 'Total: ', (total printShowingDecimalPlaces: 2);
    cr.
```

**Lo que esta clase enseña en Smalltalk.** Aquí **el literal es un objeto**, sin excepción. `15000`
no es un valor primitivo: es una instancia de `SmallInteger` a la que puedes enviarle mensajes, y
`15000 factorial` funciona (y devuelve un número de más de cincuenta mil dígitos, porque los enteros
crecen sin límite). No hay tipos primitivos fuera del sistema de objetos, y por tanto no hay
autoboxing, ni `Integer` frente a `int`, ni ninguna de las costuras que Java arrastra.

La sintaxis de literales es notablemente rica, e incluye uno que resuelve el problema del dinero:

```smalltalk
27000.00s2      "ScaledDecimal: DECIMAL EXACTO con 2 decimales, no punto flotante"
3/4             "una fracción exacta"
16r1F           "31 en base 16 — la base se escribe delante"
#unSimbolo      "símbolo: cadena única e inmutable"
#(1 2 'tres')   "array literal"
$a              "un carácter"
```

`27000.00s2` es un **ScaledDecimal**: aritmética decimal exacta como el `COMP-3` de COBOL, pero
escrita como un literal del lenguaje. Y `16r1F` invierte la convención que conoces —en vez de `0x1F`,
la base va delante y funciona para cualquier base entre 2 y 36.

Sobre constantes: Smalltalk **no tiene** una palabra clave para ellas. La forma idiomática es un
método de clase que devuelve el valor, porque en un lenguaje donde todo es un mensaje, **una
constante es simplemente un método que siempre responde lo mismo**:

```smalltalk
Impuestos class >> iva
    ^ 0.19s2
```

---

## Y de vuelta a la clase

Doce lenguajes con una media de cuarenta años cada uno, un solo problema, y **doce respuestas
distintas a la pregunta de esta clase**: COBOL declara la forma del dato antes de calcular, Ada
separa el valor de su representación, C++ separa quién puede escribir de cuándo se conoce el valor,
Lisp borra la frontera entre literal y dato, Smalltalk convierte el literal en objeto, Tcl lo
convierte todo en texto, y MUMPS deja que el enlace sobreviva al programa.

Ninguna de esas respuestas es la que da Python. Y ese es el motivo de que estén aquí.

⏮️ [Volver a la clase 041](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
