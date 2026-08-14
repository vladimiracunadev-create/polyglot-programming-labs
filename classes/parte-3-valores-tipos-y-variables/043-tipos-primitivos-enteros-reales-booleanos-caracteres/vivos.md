# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 043

> [⬅️ Volver a la clase 043](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Un entero, ese mismo entero visto como real, y una pregunta de sí o no sobre él. Tres tipos
primitivos en una línea de salida, y tres preguntas incómodas detrás: **¿cuántos tipos numéricos
tiene realmente este lenguaje?**, **¿la conversión de entero a real es automática o hay que
pedirla?** y **¿existe siquiera un tipo booleano, o se finge con números?**

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **el catálogo de tipos que un lenguaje considera fundamentales**, y estos
> lenguajes lo muestran mejor que el núcleo porque **no coinciden entre sí**. COBOL no tiene tipo
> booleano y lo resuelve con una construcción que no existe en ningún lenguaje moderno —los **nombres
> de condición de nivel 88**—. Fortran tiene `logical` desde 1957 pero parametriza el ancho con `kind`
> en vez de dar `int` y `long`. PL/I separa la **base** de la **escala**: cuatro combinaciones donde
> casi todos ofrecen dos. Y Tcl y MUMPS no tienen tipos en absoluto.
>
> Ver que "los tipos primitivos" no son una lista universal sino una decisión de cada lenguaje es
> exactamente lo que esta clase quiere dejar claro.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `n` (un entero) → stdout: `entero=<n> real=<n con 1 decimal> par=<true|false>`
- **Regla:** `real = (double) n ; par = (n módulo 2 == 0)`

| stdin | esperado |
|---|---|
| `4` | `entero=4 real=4.0 par=true` |
| `7` | `entero=7 real=7.0 par=false` |
| `0` | `entero=0 real=0.0 par=true` |

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
PROGRAM-ID. PRIMITIVOS.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA     PIC X(80).
01  N         PIC S9(9)   COMP-3.
01  REAL-N    PIC S9(9)V9 COMP-3.
01  ED-N      PIC -(9)9.
01  ED-REAL   PIC -(9)9.9.
01  PAR-TXT   PIC X(5).

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N
    MOVE N TO REAL-N

    IF FUNCTION MOD(N, 2) = 0
        MOVE "true"  TO PAR-TXT
    ELSE
        MOVE "false" TO PAR-TXT
    END-IF

    MOVE N      TO ED-N
    MOVE REAL-N TO ED-REAL
    DISPLAY "entero=" FUNCTION TRIM(ED-N)
            " real="  FUNCTION TRIM(ED-REAL)
            " par="   FUNCTION TRIM(PAR-TXT)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** **COBOL no tiene tipo booleano.** No es un olvido: hasta
COBOL 2002 no existió nada parecido, y aun hoy casi ningún código lo usa. Lo que tiene en su lugar
es más interesante de lo que parece — el **nombre de condición de nivel 88**:

```cobol
01  ESTADO-PEDIDO  PIC X.
    88  PENDIENTE   VALUE "P".
    88  ENVIADO     VALUE "E".
    88  ANULADO     VALUE "A".
    88  ACTIVO      VALUE "P" "E".      *> varios valores a la vez
```

`ESTADO-PEDIDO` es un carácter; `PENDIENTE` es un **predicado con nombre** sobre él. Se escribe
`IF PENDIENTE` —sin comparar con nada— y se asigna con `SET PENDIENTE TO TRUE`. Lo valioso es que el
nivel 88 **da nombre a un conjunto de valores**, incluidos rangos (`VALUE 1 THRU 9`). En un lenguaje
moderno eso exige un enumerado más una función; aquí es una línea de declaración pegada al dato.

Y sobre los numéricos: COBOL no distingue `int` de `long`. Distingue **cuántos dígitos**
(`PIC 9(9)`) y **cómo se guardan** (`COMP-3` decimal empaquetado, `COMP` binario, sin cláusula un
carácter por dígito). La pregunta no es el ancho de la máquina, es la forma del dato.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program primitivos
   implicit none
   integer :: n
   real(kind=8) :: r
   character(len=5) :: par
   character(len=32) :: buf

   read(*, *) n
   r = real(n, kind=8)

   if (mod(n, 2) == 0) then
      par = 'true'
   else
      par = 'false'
   end if

   write(buf, '(F20.1)') r
   write(*, '(A,I0,A,A,A,A)') 'entero=', n, ' real=', trim(adjustl(buf)), &
                              ' par=', trim(par)
end program primitivos
```

**Lo que esta clase enseña en Fortran.** Fortran tiene **cinco tipos intrínsecos** —`integer`,
`real`, `complex`, `logical` y `character`— y dos rarezas que esta clase saca a la luz.

La primera: **`complex` es un tipo primitivo**. Los números complejos no son una biblioteca: se
escriben `(1.0, 2.0)`, se suman y se multiplican con los operadores normales, y `sqrt` de un negativo
funciona si el argumento es complejo. Fortran nació para física, y en física los complejos son tan
básicos como los reales.

La segunda: en vez de `int`/`long`/`float`/`double`, Fortran parametriza el tipo con un **`kind`**:

```fortran
use iso_fortran_env, only: int32, int64, real32, real64
integer(int64) :: grande
real(real64)   :: preciso

! O mejor: pide lo que NECESITAS y que el compilador elija.
integer, parameter :: dp = selected_real_kind(15, 300)
```

`selected_real_kind(15, 300)` significa "dame la representación que soporte 15 dígitos significativos
y exponentes hasta 300". Es más portable que fijar bits, porque describe **el requisito** en lugar
de la máquina. Es la misma pregunta que resuelven el `PIC` de COBOL y el `int32_t` de C++, con tres
respuestas distintas.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;            use Ada.Text_IO;
with Ada.Integer_Text_IO;    use Ada.Integer_Text_IO;
with Ada.Long_Float_Text_IO; use Ada.Long_Float_Text_IO;

procedure Primitivos is

   function Tf (Cond : Boolean) return String is
     (if Cond then "true" else "false");

   N : Integer;
begin
   Get (N);

   Put ("entero="); Put (N, Width => 1);
   Put (" real=");  Put (Long_Float (N), Fore => 1, Aft => 1, Exp => 0);
   Put (" par=" & Tf (N mod 2 = 0));
   New_Line;
end Primitivos;
```

**Lo que esta clase enseña en Ada.** `Long_Float (N)` **no es un molde ni un adorno**: es una
**conversión de tipo explícita, y es obligatoria**. En Ada no existe la promoción automática de
entero a real que hacen C, Java o Python. Mezclar un `Integer` y un `Long_Float` en la misma
expresión **no compila**.

Suena incómodo hasta que se ve el motivo: Ada considera que una conversión es una operación con
consecuencias —puede perder precisión, puede desbordar— y por tanto debe estar **escrita**, no
supuesta. El contraste completo con los lenguajes que promocionan solos se ve en la clase 050.

Sobre los booleanos: `Boolean` **no es un entero disfrazado**, es un enumerado normal
—`type Boolean is (False, True)`— con la misma naturaleza que cualquiera que definas tú. Por eso
tiene los atributos de los enumerados: `Boolean'Image (True)` da `"TRUE"`, `Boolean'Pos (True)` da
`1`, `Boolean'First` da `False`. Y no hay conversión implícita a número: `if N` no compila, hay que
escribir `if N /= 0`.

`Tf` es una **función de expresión** (Ada 2012): un cuerpo que es una sola expresión, escrito entre
paréntesis. Es la forma corta de las funciones triviales y, además, el compilador puede usarla en
contratos y comprobarla estáticamente.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Primitivos;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N: Integer;
  R: Double;
  Par: Boolean;

begin
  Read(N);
  R := N;                       { entero -> real: Pascal SÍ promociona }

  Par := (N mod 2) = 0;

  WriteLn('entero=', IntToStr(N),
          ' real=', R:0:1,
          ' par=', LowerCase(BoolToStr(Par, True)));
end.
```

**Lo que esta clase enseña en Pascal.** Pascal fue **de los primeros lenguajes con un tipo booleano
de verdad**, y lo hizo como Ada heredaría después: `Boolean` es un **enumerado** predefinido,
`(False, True)`, con `Ord(False) = 0`. En C, en cambio, el booleano no existió hasta C99 y se fingía
con enteros, con la secuela conocida de que cualquier valor distinto de cero cuenta como verdadero.

Su catálogo es corto y ortogonal —`Integer`, `Real`, `Boolean`, `Char`— más los tipos **ordinales**
derivados. Y esa palabra, *ordinal*, es una idea propia de Pascal que merece la pena llevarse: un
tipo es ordinal si sus valores tienen **sucesor y predecesor**, lo que habilita `Succ`, `Pred`,
`Ord`, los rangos en un `case` y el uso como índice de array. `Char` es ordinal; `Real` no lo es.
Es una clasificación transversal a "primitivo" que casi ningún lenguaje moderno hace explícita.

Fíjate en la dirección de la promoción: `R := N` compila (entero a real, no se pierde nada) pero
`N := R` **no** compila y exige `Trunc` o `Round`. La conversión implícita solo va hacia donde es
segura, que es justo la política que C no tiene.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((n (read))
       (par (if (evenp n) "true" "false")))
  (format t "entero=~D real=~,1F par=~A~%" n (float n 1.0d0) par))
```

**Lo que esta clase enseña en Common Lisp.** La **torre numérica**. Lisp no tiene "tipos numéricos
primitivos": tiene una jerarquía matemática en la que los valores se promueven solos y sin pérdida.

```text
integer  ⊂  ratio  ⊂  rational  ⊂  real  ⊂  complex  ⊂  number
```

Un `integer` **no tiene tamaño máximo** —crece mientras quepa en memoria—, un `ratio` es una fracción
exacta, y las operaciones suben por la torre automáticamente: `(+ 1/3 1/6)` da `1/2`, exacto. Es el
diseño contrario al de C, donde los tipos numéricos son cajas de ancho fijo que desbordan en
silencio.

Los booleanos son la otra sorpresa: **no hay tipo booleano**. Hay `nil`, que es falso, y **todo lo
demás**, que es verdadero. `t` es la convención para el verdadero explícito. Y ojo con la trampa:
**`0` es verdadero en Lisp**, al contrario que en C, Python o JavaScript. También lo son la cadena
vacía y el carácter nulo. El único falso es `nil` — que además es la lista vacía y el símbolo `nil`,
tres papeles en un único objeto.

`(float n 1.0d0)` convierte a real usando el segundo argumento como **prototipo de precisión**: "haz
un real del mismo tipo que este". Es una forma de pedir doble precisión sin nombrar el tipo.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

set par [expr {$n % 2 == 0 ? "true" : "false"}]

puts "entero=$n real=[format %.1f $n] par=$par"
```

**Lo que esta clase enseña en Tcl.** El caso límite: **no hay tipos primitivos, porque no hay
tipos**. `$n` contiene la cadena `"4"`. Cuando `expr` la usa en aritmética la lee como número; cuando
`format %.1f` la recibe la lee como real; cuando `string length` la mira cuenta caracteres. **El tipo
lo aporta la operación, no el dato.**

Internamente Tcl guarda además una representación numérica en caché para no reconvertir dentro de un
bucle —los llamados *objetos de doble representación*—, pero eso es una optimización invisible que no
cambia la semántica: si imprimes el valor, sale la cadena.

Los booleanos siguen la misma lógica. `expr` acepta como verdadero `1`, `true`, `yes`, `on` y
cualquier número distinto de cero; como falso, `0`, `false`, `no`, `off` y la cadena vacía. Pero
**devuelve `1` o `0`**, no `true` o `false`. Por eso este programa tiene que traducir a mano lo que
en C++ hace `std::boolalpha` y en Pascal `BoolToStr`.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

my $par = ($n % 2 == 0) ? 'true' : 'false';

printf "entero=%d real=%.1f par=%s\n", $n, $n, $par;
```

**Lo que esta clase enseña en Perl.** Perl tiene **un solo tipo escalar**. No hay `int`, no hay
`float`, no hay `string` y no hay `bool`: hay **escalar**, y dentro de él Perl mantiene a la vez las
representaciones que hagan falta, usando la que pida el contexto. Por eso la misma variable `$n` va
como `%d` y como `%.1f` en el mismo `printf` sin ninguna conversión.

El booleano tampoco existe como tipo. Perl considera **falsos** exactamente cinco valores: `0`,
`"0"`, `""`, `undef` y la lista vacía. Todo lo demás es verdadero — incluidas las cadenas `"0.0"` y
`"00"`, que son verdaderas y desconciertan a todo el mundo la primera vez, porque no son *la* cadena
`"0"`.

Ese diseño de escalar único es lo que hace a Perl tan cómodo con texto y, a la vez, lo que le obliga
a tener **dos juegos de operadores de comparación**: `==`, `<`, `>` comparan como número y `eq`,
`lt`, `gt` comparan como cadena. En la clase 051 esa distinción se convierte en el tema central.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iomanip>
#include <iostream>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    const double r = n;              // promoción implícita entero -> real
    const bool par = (n % 2 == 0);

    std::cout << "entero=" << n
              << " real=" << std::fixed << std::setprecision(1) << r
              << " par=" << std::boolalpha << par << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** `std::boolalpha` es un **manipulador de flujo**: cambia el
estado de `std::cout` para que los `bool` salgan como `true`/`false` en vez de `1`/`0`. Y ese detalle
revela el fondo — en C++ un `bool` **se convierte a entero sin protestar**, porque el lenguaje hereda
de C la idea de que la verdad es un número. `bool` existe como tipo propio desde el principio de C++
(en C hubo que esperar a C99), pero la conversión sigue ahí.

El catálogo de primitivos de C++ es el más detallado de esta página y, paradójicamente, el menos
preciso: `char`, `short`, `int`, `long`, `long long`, con variantes `signed`/`unsigned`, más `float`,
`double` y `long double`. El estándar solo garantiza **anchos mínimos y un orden**, no tamaños
exactos: un `int` puede medir 16, 32 o 64 bits según la plataforma.

Por eso el C++ moderno usa tipos de ancho fijo cuando importa:

```cpp
#include <cstdint>
std::int32_t      exacto;   // exactamente 32 bits, o no compila
std::int_fast32_t rapido;   // al menos 32, el más rápido de esta máquina
std::int_least8_t compacto; // al menos 8, el más pequeño que sirva
```

Es la misma pregunta que Fortran resuelve con `kind` y COBOL con `PIC`: **¿describes la máquina o
describes tu necesidad?** C++ te deja hacer las dos cosas, y por eso hay que elegir a conciencia.

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

dcl-pi PRIMITIV;
  n int(10) const;
end-pi;

dcl-s r      packed(11:1);
dcl-s par    char(5);
dcl-s salida char(60);

r = n;

if %rem(n : 2) = 0;
  par = 'true';
else;
  par = 'false';
endif;

salida = 'entero=' + %char(n)
       + ' real='  + %char(r)
       + ' par='   + %trimr(par);
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** El catálogo de RPG está pensado para **negocio**, y se nota en
qué considera primitivo: `packed` y `zoned` (decimal exacto, empaquetado o no), `int` y `uns`
(binarios), `float`, `char`, `varchar`, `date`, `time`, `timestamp` e `indicator`.

Dos cosas llaman la atención. La primera es que **la fecha es un tipo primitivo del lenguaje**, con
aritmética propia (`fecha + %days(30)`), comprobación de validez y formatos declarados. En todos los
lenguajes del núcleo es una biblioteca; para un ERP, es tan fundamental como el entero.

La segunda es `indicator`, el booleano de RPG, que vale `*on` o `*off` — y que desciende
directamente de los indicadores numerados `*IN01`…`*IN99` del ciclo del programa. Es un booleano
nacido del hardware de las tarjetas perforadas que acabó convirtiéndose en un tipo con nombre.

`%rem` es el resto y `%div` la división entera. Existen como funciones separadas porque el operador
`/` sobre decimales **redondea** según los decimales del destino, así que RPG obliga a decir cuándo
quieres aritmética entera de verdad.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 primitivos: procedure options(main);

    declare n     fixed binary(31);
    declare r     fixed decimal(11,1);
    declare par   character(5) varying;
    declare pres  picture 'ZZZZZZZZ9V.9';

    get list (n);
    r = n;

    if mod(n, 2) = 0 then par = 'true';
    else par = 'false';

    pres = r;
    put skip list ('entero=' || trim(char(n)) ||
                   ' real='  || trim(pres) ||
                   ' par='   || par);

 end primitivos;
```

**Lo que esta clase enseña en PL/I.** Es el único lenguaje de esta página que separa explícitamente
las **dos dimensiones** de un número en vez de dar una lista cerrada de tipos:

| | **Escala fija** | **Escala flotante** |
|---|---|---|
| **Base decimal** | `fixed decimal(11,2)` — dinero, exacto | `float decimal(15)` |
| **Base binaria** | `fixed binary(31)` — el `int` de siempre | `float binary(53)` — el `double` |

Cuatro casillas. Casi todos los lenguajes modernos ofrecen dos —`int` y `double`— y **ocultan que son
solo dos esquinas de esa matriz**. Cuando en Java escribes `BigDecimal` o en C# `decimal`, estás
recuperando a mano la casilla de arriba a la izquierda, que PL/I tenía en 1964.

PL/I tampoco tiene booleano: usa `bit(1)`, con literales `'1'b` y `'0'b`, y los operadores `&`, `|` y
`¬` sirven a la vez para bits y para lógica. Es coherente con su época, y explica por qué C
—diseñado poco después— tomó exactamente la misma decisión.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
PRIM ; Tipos primitivos -- clase 043
 read n
 set par = $select(n#2 = 0 : "true", 1 : "false")
 write "entero=", n
 write " real=", $justify(n, 0, 1)
 write " par=", par, !
 quit
```

**Lo que esta clase enseña en M.** **M tiene exactamente un tipo: la cadena.** No hay entero, no hay
real, no hay booleano y no hay carácter. Todo lo demás es una interpretación que impone el operador:
`+` lee la cadena como número, `_` la concatena, `'` la niega como booleano.

Y esa interpretación tiene una regla propia que conviene conocer: al convertir texto a número, M
**lee el prefijo numérico y descarta el resto, sin error**. `"12ABC" + 1` da `13`; `"hola" + 1` da
`1`. Es tipado débil llevado más lejos que en JavaScript, y fue deliberado: en un sistema clínico de
1966 con datos irregulares, un error de conversión que detiene el proceso se consideraba peor que un
valor degradado.

`$select` es el condicional **en forma de expresión**: pares `condición : valor`, se evalúa el
primero que se cumple, y el `1` final hace de `else` porque `1` siempre es cierto. Y `#` es el
módulo. Que el módulo sea `#` y no `%` es solo otra convención, pero es la clase de detalle que hace
que leer M exija aprender primero el vocabulario y después la lógica.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n |

n := stdin nextLine trimBoth asNumber.

Transcript
    show: 'entero=', n printString;
    show: ' real=', (n asFloat printShowingDecimalPlaces: 1);
    show: ' par=', (n even ifTrue: [ 'true' ] ifFalse: [ 'false' ]);
    cr.
```

**Lo que esta clase enseña en Smalltalk.** **No hay tipos primitivos. Ninguno.** `4` es una instancia
de `SmallInteger`, `4.0` de `Float`, `true` de `True` y `$a` de `Character`. Todos son objetos, todos
tienen clase, y a todos se les pueden enviar mensajes: `4 even`, `4 factorial`, `4 printString`,
`4 class` —que responde `SmallInteger`—.

La consecuencia práctica es enorme: Java y C# tuvieron que inventar el *autoboxing* —esa costura
entre `int` e `Integer` que todavía produce `NullPointerException`— para resolver un problema que en
Smalltalk nunca existió.

La jerarquía numérica es matemática, no de máquina: `Integer` se divide en `SmallInteger` y
`LargePositiveInteger`, y **el paso de uno a otro es automático e invisible**. `1000 factorial`
funciona y devuelve un número de 2568 dígitos. `Fraction` guarda razones exactas y `ScaledDecimal`
decimales exactos.

Pero la joya de esta clase son los booleanos: `true` y `false` son las **únicas instancias** de las
clases `True` y `False`, ambas subclases de `Boolean`. `ifTrue:ifFalse:` está **implementado como
método en cada una** —`True` evalúa el primer bloque, `False` el segundo— y puedes abrir el navegador
de clases y leer ese código. El condicional no es sintaxis: es polimorfismo.

---

## Y de vuelta a la clase

La conclusión es que **no existe "el" conjunto de tipos primitivos**. Existen decisiones: COBOL
eligió el decimal exacto y prescindió del booleano, Fortran eligió el `kind` parametrizable y metió
los complejos en el lenguaje, C++ eligió una jerarquía de anchos sin tamaños garantizados, Smalltalk
eligió que no hubiera primitivos, y Tcl y MUMPS eligieron no elegir. Lo transferible no es la lista
de tipos de tu lenguaje: es saber **qué preguntas responde esa lista**.

⏮️ [Volver a la clase 043](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
