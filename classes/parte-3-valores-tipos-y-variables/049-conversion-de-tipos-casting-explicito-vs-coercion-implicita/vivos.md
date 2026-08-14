# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 049

> [⬅️ Volver a la clase 049](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Tomar `3.7` y quedarse con `3`. Todo el mundo sabe hacerlo; casi nadie sabe qué hace su lenguaje
cuando **no** se lo pides. Esta clase separa la **conversión explícita** —la que escribes— de la
**coerción implícita** —la que el lenguaje hace por su cuenta—, y de paso descubre una trampa que
sorprende incluso a programadores veteranos: **no todos los lenguajes truncan al convertir a entero.
Ada redondea.**

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **quién decide una conversión y cuándo**, y estos lenguajes ocupan todo el
> espectro. En un extremo, **Ada**: no hay ninguna conversión implícita entre tipos numéricos, todas se
> escriben, y aun así `Integer(3.7)` da **4** y no 3 — porque la conversión *escrita* también tiene una
> semántica que hay que conocer. En el otro extremo, **M** y **Tcl**, donde no hay conversión porque no
> hay tipos, y el resultado depende del operador que toques.
>
> Y en medio, COBOL con algo que ningún lenguaje moderno tiene: **la conversión ocurre en el `MOVE`**,
> gobernada por la forma del destino, y trunca por la izquierda sin avisar si el destino es más corto.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un número real como texto → stdout: `entero=<parte entera truncada> real=<valor con 2 decimales>`
- **Regla:** `entero = truncar(real) ; real formateado a 2 decimales`

| stdin | esperado |
|---|---|
| `3.7` | `entero=3 real=3.70` |
| `5.0` | `entero=5 real=5.00` |
| `8.9` | `entero=8 real=8.90` |

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
PROGRAM-ID. CONVERSION.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  R       PIC S9(9)V99 COMP-3.
01  E       PIC S9(9)    COMP-3.
01  ED-E    PIC -(9)9.
01  ED-R    PIC -(9)9.99.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO R
    MOVE R TO E
    MOVE E TO ED-E
    MOVE R TO ED-R
    DISPLAY "entero=" FUNCTION TRIM(ED-E)
            " real=" FUNCTION TRIM(ED-R)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** `MOVE R TO E` es **la conversión implícita de COBOL**, y es la
razón de que `MOVE` no sea un simple `=`. El destino manda: `E` es `PIC S9(9)` sin decimales, así que
los decimales de `R` **se descartan** —truncados, no redondeados— y nadie avisa.

Y hay una segunda parte, mucho más peligrosa, que es el motivo de que esta clase importe en COBOL:
**la truncación también ocurre por la izquierda**.

```cobol
01  GRANDE  PIC 9(9)  VALUE 123456789.
01  CHICO   PIC 9(3).

MOVE GRANDE TO CHICO      *> CHICO vale 789.  Sin error. Sin aviso.
```

Se pierden los seis dígitos más significativos y el programa continúa. Es el fallo silencioso
característico del lenguaje, y la razón de que las revisiones de código COBOL se centren tanto en
comprobar que los `PIC` de origen y destino cuadran.

La forma de no sufrirlo es pedir el aviso explícitamente, que existe pero hay que escribirlo:

```cobol
COMPUTE CHICO = GRANDE
    ON SIZE ERROR DISPLAY "no cabe"
END-COMPUTE
```

`ON SIZE ERROR` funciona en `COMPUTE`, `ADD`, `SUBTRACT`, `MULTIPLY` y `DIVIDE` — pero **no en
`MOVE`**. Mover nunca avisa. Ese detalle explica muchos incidentes.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program conversion
   implicit none
   real(kind=8) :: r
   integer :: e
   character(len=32) :: buf

   read(*, *) r
   e = int(r)                    ! int() trunca HACIA CERO

   write(buf, '(F20.2)') r
   write(*, '(A,I0,A,A)') 'entero=', e, ' real=', trim(adjustl(buf))
end program conversion
```

**Lo que esta clase enseña en Fortran.** Fortran tiene **cuatro funciones distintas** para pasar de
real a entero, y esa es toda la lección: la conversión no es una operación, son cuatro decisiones
diferentes con nombre propio.

| Función | `3.7` | `-3.7` | Qué hace |
|---|---|---|---|
| `int(x)` | 3 | -3 | Trunca **hacia cero** |
| `nint(x)` | 4 | -4 | Redondea al **más cercano** |
| `floor(x)` | 3 | **-4** | Al entero **inferior** |
| `ceiling(x)` | 4 | -3 | Al entero **superior** |

Fíjate en la columna de los negativos, que es donde se ven las diferencias reales: `int(-3.7)` da
`-3` y `floor(-3.7)` da `-4`. Confundirlas produce errores que solo aparecen con datos negativos,
que suelen ser los que no están en las pruebas.

En cambio, la conversión **en el otro sentido sí es implícita**: `r = 5` promociona el entero a real
sin decir nada, porque no se pierde información. Fortran aplica la misma regla que Pascal — la
promoción segura es automática, la que pierde datos hay que escribirla.

Y hay una trampa clásica de la que esta clase debe advertir: **`1/2` en Fortran da `0`**. Si los dos
operandos son enteros, la división es entera, aunque el destino sea real. `r = 1/2` deja `r` a cero;
hay que escribir `r = 1.0/2.0`. El mismo error existe en C, Java y Go.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;            use Ada.Text_IO;
with Ada.Integer_Text_IO;    use Ada.Integer_Text_IO;
with Ada.Long_Float_Text_IO; use Ada.Long_Float_Text_IO;

procedure Conversion is
   R : Long_Float;
   E : Integer;
begin
   Get (R);

   --  ¡Integer (R) REDONDEA en Ada!  Para truncar hace falta el atributo.
   E := Integer (Long_Float'Truncation (R));

   Put ("entero="); Put (E, Width => 1);
   Put (" real=");  Put (R, Fore => 1, Aft => 2, Exp => 0);
   New_Line;
end Conversion;
```

**Lo que esta clase enseña en Ada.** Esta es la sorpresa más útil de toda la Parte 3: **en Ada,
`Integer (3.7)` da `4`, no `3`.** La conversión de real a entero **redondea al más cercano**, al
contrario que en C, C++, Java, Go, Rust, Python, Perl, Tcl y Pascal, donde trunca.

No es un capricho. Ada considera que convertir es *representar el mismo valor en otro tipo*, y la
representación más fiel de 3.7 como entero es 4. Truncar es una operación **distinta**, y por eso
tiene un nombre distinto: el atributo `'Truncation`. Junto a él están `'Rounding`, `'Floor` y
`'Ceiling`, la misma familia que las cuatro funciones de Fortran.

Es exactamente la clase de detalle que hace que portar un algoritmo entre lenguajes sin leer el
manual produzca resultados que difieren en uno. Y el motivo de que Ada obligue a escribir **todas**
las conversiones: si tienes que escribirla, tienes que pensar cuál.

```ada
E := Integer (R);                       --  redondea: 4
E := Integer (Long_Float'Truncation(R));--  trunca:   3
E := Integer (Long_Float'Floor (R));    --  hacia abajo
```

Y aún hay una segunda capa: si `E` fuera de un subtipo con rango —`subtype Nota is Integer range
1 .. 7`— la conversión además **comprobaría el rango** y levantaría `Constraint_Error`. La conversión
en Ada convierte, redondea y valida, todo en el mismo sitio visible.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Conversion;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  R: Double;
  E: Integer;

begin
  Read(R);
  E := Trunc(R);          { Trunc corta hacia cero; Round redondearía }

  WriteLn('entero=', IntToStr(E), ' real=', R:0:2);
end.
```

**Lo que esta clase enseña en Pascal.** Pascal fue de los primeros en separar las dos operaciones con
nombres distintos y obligatorios: **`Trunc`** corta hacia cero y **`Round`** redondea. No existe una
conversión implícita de real a entero — `E := R` **no compila**—, así que el programador tiene que
elegir una de las dos en cada sitio.

Esa obligación es la política que Ada heredaría después, y el contraste con C es claro: en C,
`int e = r;` compila, trunca, y nadie se entera de que hubo una decisión.

Hay un detalle de `Round` que conviene conocer porque contradice la intuición: en Delphi y Free
Pascal, `Round` usa **redondeo bancario** —al par más cercano— porque sigue el estándar IEEE 754. Así
que `Round(2.5)` da **2** y `Round(3.5)` da **4**. Quien espera 3 y 4 se lleva una sorpresa, y en un
cálculo de importes esa sorpresa es un descuadre. Para el redondeo "de toda la vida" hay que usar
`SimpleRoundTo` de `Math`.

La promoción en la dirección segura sí es automática: `R := E` funciona. Y la conversión desde texto
es explícita y con su propia familia de funciones —`StrToInt`, `StrToFloat`, `StrToIntDef`, `TryStrToInt`—
donde las dos últimas son las importantes: una devuelve un valor por defecto y la otra un booleano,
en lugar de lanzar una excepción con datos sucios.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(setf *read-default-float-format* 'double-float)

(let* ((r (read))
       (e (truncate r)))
  (format t "entero=~D real=~,2F~%" e r))
```

**Lo que esta clase enseña en Common Lisp.** Lisp tiene las cuatro operaciones con nombres claros
—`truncate`, `round`, `floor`, `ceiling`— y una peculiaridad que las hace mejores que sus
equivalentes en otros lenguajes: **devuelven dos valores**.

```lisp
(truncate 3.7)     ; => 3  y  0.7
(floor -3.7)       ; => -4 y  0.3
(round 2.5)        ; => 2  y  0.5    ¡redondeo bancario, como Pascal!
(multiple-value-bind (cociente resto) (truncate 17 5)
  (format t "~D con resto ~D" cociente resto))   ; 3 con resto 2
```

El segundo valor es **el resto**, es decir, lo que se perdió al convertir. Casi siempre se ignora
—`format` solo usa el primero—, pero está ahí sin coste si lo necesitas. Los valores múltiples de
Lisp son un mecanismo del lenguaje, no una tupla: no se construye ningún objeto, así que ignorarlos es
gratis. Muy pocos lenguajes lo tienen; Go lo aproxima con retornos múltiples, pero allí hay que
declarar que los ignoras.

Y `round` en Lisp también usa **redondeo bancario** —`(round 2.5)` es 2 y `(round 3.5)` es 4—, la
misma regla que Pascal y que el estándar IEEE. Que dos lenguajes tan distintos coincidan aquí y
difieran de C es un buen recordatorio de que "redondear" tampoco significa lo mismo en todas partes.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set r [string trim $linea]

set e [expr {int($r)}]

puts "entero=$e real=[format %.2f $r]"
```

**Lo que esta clase enseña en Tcl.** En un lenguaje sin tipos, la conversión **no existe como
concepto**: lo que existe es la interpretación que hace cada operación. `$r` contiene la cadena
`"3.7"` todo el tiempo; `int()` la lee como número y devuelve la parte entera, `format %.2f` la lee
como real, y `string length` la contaría como texto de tres caracteres.

Dentro de `expr`, Tcl ofrece las cuatro funciones habituales —`int()`, `round()`, `floor()`,
`ceil()`— con la semántica de C: `int()` trunca hacia cero.

Pero hay una trampa muy específica de Tcl que conviene conocer, porque contradice lo que la intuición
sugiere en un lenguaje de tipado débil: **la división de dos enteros es entera**.

```tcl
expr {7 / 2}        ;# 3     -- ¡ambos son enteros!
expr {7 / 2.0}      ;# 3.5
expr {double(7)/2}  ;# 3.5
```

Que un lenguaje sin tipos preserve la distinción entero/real en la división sorprende, y es
deliberado: Tcl mira el **texto** de los operandos para decidir. `"7"` parece entero, `"7.0"` parece
real. La forma en que escribes el literal cambia el resultado — que es, exactamente, lo que significa
que el tipo lo aporte la operación y no el dato.

Y desde Tcl 8.5 `int()` está limitado a la palabra de máquina; para valores grandes hay que usar
`entier()`, que respeta la precisión arbitraria.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $r = <STDIN>;
chomp $r;

my $e = int($r);          # int() trunca hacia cero, NO redondea

printf "entero=%d real=%.2f\n", $e, $r;
```

**Lo que esta clase enseña en Perl.** Perl es el extremo opuesto de Ada: **no hay conversión porque
no hay tipos que convertir**. Un escalar guarda a la vez su forma numérica y su forma textual, y cada
operador usa la que necesita. `"3.7" + 0` es 3.7 y `3.7 . ""` es `"3.7"`, sin que ocurra nada
especial.

`int()` trunca hacia cero, como en C. Para redondear no hay función incorporada, y el idioma clásico
es `int($x + 0.5)` —que falla con negativos— o `sprintf("%.0f", $x)`, que usa redondeo bancario.
Que Perl no traiga `round` es una de sus rarezas más comentadas; `POSIX::floor` y `POSIX::ceil` sí
están, importando el módulo.

Lo específico de esta clase en Perl es lo que ocurre cuando el texto **no** es un número:

```perl
my $x = "12abc" + 0;    # 12   -- lee el prefijo y descarta el resto
my $y = "abc" + 0;      # 0
```

Sin `use warnings`, eso pasa en silencio. **Con** `use warnings`, Perl emite
`Argument "12abc" isn't numeric in addition`, que es exactamente el aviso que M **no** da y que
convierte un tipado débil manejable en uno peligroso. Es el mejor argumento de esta página a favor
de activar los avisos: no cambian la semántica, hacen visible la coerción.

Y `looks_like_number` de `Scalar::Util` es la comprobación explícita, el equivalente de
`string is double` en Tcl.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iomanip>
#include <iostream>

int main() {
    double r{};
    if (!(std::cin >> r)) return 1;

    const int e = static_cast<int>(r);   // trunca hacia cero

    std::cout << "entero=" << e
              << " real=" << std::fixed << std::setprecision(2) << r << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** `static_cast<int>(r)` es deliberadamente **verboso**, y esa
verbosidad es la característica. En C bastaba `(int)r`, un molde que servía para todo: convertir
tipos numéricos, quitar `const`, reinterpretar punteros. C++ lo partió en cuatro operadores con
nombres largos y significados distintos:

| Operador | Para qué |
|---|---|
| `static_cast<T>` | Conversiones con sentido comprobadas al compilar |
| `dynamic_cast<T>` | Bajar en una jerarquía de clases, con comprobación en ejecución |
| `const_cast<T>` | Quitar o poner `const` — casi siempre una señal de alarma |
| `reinterpret_cast<T>` | Reinterpretar los bits; peligroso y a veces indefinido |

El motivo del nombre largo es explícito: **son fáciles de buscar**. `grep reinterpret_cast` encuentra
todos los sitios sospechosos de una base de código; `grep '(int)'` no encuentra nada útil. Es diseño
de lenguaje pensando en la revisión de código.

Y esta clase toca además la parte más oscura de C++: las **conversiones implícitas** que sí quedan.
`int` a `double` es segura; `double` a `int` trunca y **avisa solo con `-Wconversion`**; `int` a
`unsigned` convierte un negativo en un número enorme; y una comparación entre `signed` y `unsigned`
convierte el con signo, con el resultado clásico de que `-1 < 1u` es **falso**. Compilar con
`-Wall -Wextra -Wconversion` es lo que convierte esas trampas en avisos.

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

dcl-pi CONVERS;
  r packed(15:2) const;
end-pi;

dcl-s e      int(10);
dcl-s salida char(60);

e = %int(r);          // %int trunca; %inth redondea (half adjust)

salida = 'entero=' + %char(e) + ' real=' + %char(r);
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG tiene la distinción **en el nombre de la función**, con una
convención que recorre todo el lenguaje: la **`h` final significa *half adjust***, es decir,
redondeo.

| Función | Qué hace |
|---|---|
| `%int(x)` | Convierte a entero **truncando** |
| `%inth(x)` | Convierte a entero **redondeando** |
| `%dec(x : d : p)` | Convierte a decimal truncando |
| `%dech(x : d : p)` | Convierte a decimal redondeando |

Esa pareja sistemática es más honesta que tener una sola función y una nota en el manual. Y en un
lenguaje de facturación, la diferencia entre truncar y redondear un importe **es una decisión de
negocio**, así que exigir que se elija en cada llamada es lo correcto.

Hay además una trampa propia de RPG que ya apareció en la clase 044 y que aquí es central: **el
operador `/` redondea**, no trunca, según los decimales del destino. `e = 7 / 2` con `e` entero da
**4**, no 3. Quien llega de C o de Java escribe esa línea esperando 3 y obtiene otra cosa, sin ningún
aviso.

La forma correcta de la división entera es `%div(7 : 2)`, que da 3, con `%rem(7 : 2)` para el resto.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 conversion: procedure options(main);

    declare r    fixed decimal(15,2);
    declare e    fixed binary(31);
    declare pres picture 'ZZZZZZZZZ9V.99';

    get list (r);
    e = trunc(r);

    pres = r;
    put skip list ('entero=' || trim(char(e)) || ' real=' || trim(pres));

 end conversion;
```

**Lo que esta clase enseña en PL/I.** PL/I es, con diferencia, **el lenguaje con más conversiones
implícitas de esta página**, y esta clase es donde eso se vuelve un problema. Casi cualquier
asignación entre tipos distintos compila y hace algo:

```pli
declare n fixed decimal(5,2);
declare c character(10) varying;

n = '123.45';    /* texto a decimal: funciona */
c = n;           /* decimal a texto: funciona, con formato implícito */
n = '12abc';     /* ERROR EN EJECUCIÓN: condición CONVERSION */
```

Esa última línea es la clave: cuando la conversión implícita **no puede** hacerse, PL/I no devuelve
un valor degradado como M ni avisa como Perl: levanta la condición **`CONVERSION`**, que se puede
capturar con el mecanismo `ON` de la clase 041.

```pli
on conversion begin;
   put skip list ('dato no numérico: ' || onsource());
   onsource() = '0';       /* CORRIGE el dato y REANUDA */
end;
```

`onsource()` como pseudovariable permite **reemplazar el dato que falló y continuar la operación**.
No es capturar una excepción y abortar: es reparar y seguir. Es el mismo poder que los reinicios de
[Common Lisp](../../../atlas/common-lisp.md), y una capacidad que el `try/catch` moderno perdió por
el camino.

Y `trunc` frente a `round`: PL/I tiene las dos, y además `divide(a, b, p, q)` para controlar la
precisión exacta del resultado de una división.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
CONVER ; Conversion -- clase 049
 read r
 set e = r\1
 write "entero=", e, " real=", $justify(r, 0, 2), !
 quit
```

**Lo que esta clase enseña en M.** `r\1` es la conversión a entero, y merece explicación: `\` es la
**división entera** de M, así que dividir por uno y quedarse con la parte entera **es** truncar. No
hay función `int` porque no hace falta: el operador ya trunca.

Es un ejemplo perfecto de la economía del lenguaje —una operación que en otros sitios necesita una
función aquí es un efecto colateral de un operador— y también de por qué M es difícil de leer sin
conocerlo: `r\1` no dice "truncar" en ninguna parte.

Y esta clase es donde el tipado débil de M muestra su lado más peligroso, que ya se apuntó en la 043:
**la conversión de texto a número nunca falla**.

```mumps
write "12abc" + 0     ; 12   -- lee el prefijo
write "abc" + 0       ; 0    -- sin error, sin aviso
write "1.5e3" + 0     ; 1500 -- entiende notación científica
write "" + 0          ; 0
```

Perl hace lo mismo pero **avisa** con `use warnings`. PL/I hace lo mismo pero **levanta una
condición** capturable. M no hace ninguna de las dos cosas: devuelve 0 y sigue. En un sistema clínico
de 1966 eso se consideró preferible a detener el proceso, y sigue siendo el comportamiento hoy.

La consecuencia práctica es que **la validación en M es responsabilidad del programador, siempre**.
De ahí que VistA tenga FileMan, un diccionario de datos que valida cada campo antes de escribirlo: el
esquema y la validación que el lenguaje no da, construidos encima.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| r e |

r := stdin nextLine trimBoth asNumber.
e := r truncated.

Transcript
    show: 'entero=', e printString;
    show: ' real=', (r asFloat printShowingDecimalPlaces: 2);
    cr.
```

**Lo que esta clase enseña en Smalltalk.** La conversión es **un mensaje enviado al objeto**, y por
eso el catálogo está en la clase `Number` y se puede leer:

```smalltalk
3.7 truncated     "3   -- hacia cero"
3.7 rounded       "4"
3.7 floor         "3"
-3.7 floor        "-4"
3.7 ceiling       "4"
3.7 asInteger     "3   -- sinónimo de truncated"
'3.7' asNumber    "3.7 -- del texto al número"
3.7 printString   "'3.7' -- del número al texto"
```

Fíjate en la dirección de los mensajes: `asNumber` se envía a la **cadena** y `printString` al
**número**. Cada objeto sabe convertirse a lo demás, en lugar de existir una función externa que los
conozca a los dos. Añadir un tipo nuevo al sistema no obliga a modificar ninguna función de
conversión: basta con que implemente los mensajes.

Y hay una consecuencia de esta clase que solo se ve aquí y en Lisp: como los enteros no tienen
límite, `truncated` **nunca desborda**. `1e100 truncated` devuelve el entero de 101 dígitos completo.
En C++ eso sería comportamiento indefinido; en Java daría `Long.MAX_VALUE`; aquí simplemente
funciona.

`asNumber` sobre texto no numérico devuelve `nil` en lugar de cero, lo que obliga a comprobarlo —la
postura contraria a la de M— y enlaza con la clase 053.

---

## Y de vuelta a la clase

Dos reglas transferibles. La primera: **truncar y redondear no son lo mismo, y tu lenguaje ha elegido
uno por ti**. C, C++, Perl, Tcl y Pascal truncan hacia cero; Ada redondea; RPG redondea con `/` pero
trunca con `%int`. Comprueba cuál antes de escribir un cálculo con dinero.

La segunda: **una conversión implícita es una decisión que nadie revisó**. Ada la prohíbe entera y
paga verbosidad a cambio; COBOL la esconde en el `MOVE`; Perl y M ni siquiera la consideran una
conversión. Saber en qué punto del espectro está tu lenguaje es lo que evita el defecto silencioso.

⏮️ [Volver a la clase 049](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
