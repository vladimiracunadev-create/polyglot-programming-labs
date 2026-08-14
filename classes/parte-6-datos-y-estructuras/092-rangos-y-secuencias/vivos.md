# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 092

> [⬅️ Volver a la clase 092](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Los enteros de `a` hasta `b`, listados y sumados. Parece la clase más inocente de la parte, y esconde
una de las ideas mejor pensadas del diseño de lenguajes: **en Ada y en Pascal el rango es un tipo**,
no un bucle. `1 .. 10` sirve para declarar un arreglo, para acotar una variable, para elegir en un
`case` y para recorrer — **la misma notación en los cuatro sitios**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **secuencia definida por sus extremos**, y estos lenguajes lo enseñan porque
> Pascal y Ada lo elevaron a categoría de tipo. Un `subtype Dia is Integer range 1 .. 31` no es
> documentación: **el compilador rechaza asignarle 32**, y en Ada lo comprueba también en ejecución.
>
> Enfrente, **COBOL, Fortran, Tcl y M no tienen rangos**: tienen bucles. Y **Perl** tiene el operador
> `..`, que además esconde el *flip-flop*, uno de los operadores más extraños que existen. **C++**
> tardó hasta C++20 en tener `views::iota`, y hasta entonces el rango se escribía como dos iteradores.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a b` (enteros, a <= b) → stdout: `rango=<a-...-b> suma=<suma del rango>`
- **Regla:** `rango [a..b] y su suma`

| stdin | esperado |
|---|---|
| `2 5` | `rango=2-3-4-5 suma=14` |
| `1 1` | `rango=1 suma=1` |
| `3 6` | `rango=3-4-5-6 suma=18` |

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
PROGRAM-ID. RANGO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TXT-A   PIC X(20).
01  TXT-B   PIC X(20).
01  A       PIC S9(9)  COMP-3.
01  B       PIC S9(9)  COMP-3.
01  I       PIC S9(9)  COMP-3.
01  SUMA    PIC S9(18) COMP-3 VALUE 0.
01  SALIDA  PIC X(200) VALUE SPACES.
01  SPOS    PIC 9(4) COMP VALUE 1.
01  L       PIC 9(4) COMP.
01  ED      PIC -(8)9.
01  TXT     PIC X(10).
01  ED-S    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    COMPUTE A = FUNCTION NUMVAL(TXT-A)
    COMPUTE B = FUNCTION NUMVAL(TXT-B)

    PERFORM VARYING I FROM A BY 1 UNTIL I > B
        ADD I TO SUMA
        MOVE I TO ED
        MOVE FUNCTION TRIM(ED) TO TXT
        MOVE 0 TO L
        INSPECT FUNCTION REVERSE(TXT) TALLYING L FOR LEADING SPACE
        COMPUTE L = 10 - L
        MOVE TXT(1:L) TO SALIDA(SPOS:L)
        ADD L TO SPOS
        IF I < B
            MOVE "-" TO SALIDA(SPOS:1)
            ADD 1 TO SPOS
        END-IF
    END-PERFORM

    COMPUTE L = SPOS - 1
    MOVE SUMA TO ED-S
    DISPLAY "rango=" SALIDA(1:L) " suma=" FUNCTION TRIM(ED-S)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** COBOL **no tiene rangos como valores**: tiene `PERFORM
VARYING`, que es un bucle con inicio, paso y condición de salida.

Donde sí aparece la idea de rango es en dos sitios, y los dos son característicos.

**En `EVALUATE`**, con la palabra `THRU`:

```cobol
EVALUATE EDAD
    WHEN 0  THRU 17  DISPLAY "menor"
    WHEN 18 THRU 64  DISPLAY "adulto"
    WHEN 65 THRU 199 DISPLAY "jubilado"
    WHEN OTHER       DISPLAY "revisar"
END-EVALUATE
```

**Y en los nombres de condición de nivel 88**, que es la construcción más elegante de COBOL y la que
más se echa de menos en otros lenguajes:

```cobol
01  EDAD  PIC 9(3).
    88  ES-MENOR      VALUE 0 THRU 17.
    88  ES-ADULTO     VALUE 18 THRU 64.
    88  ES-JUBILADO   VALUE 65 THRU 199.
    88  EDAD-VALIDA   VALUE 0 THRU 199.

IF ES-JUBILADO
    PERFORM CALCULAR-PENSION
END-IF
```

Un nivel 88 **da nombre a un conjunto de valores** y se usa como un booleano. El rango vive en la
declaración del dato, junto al dato, y no se repite en cada `IF`. Cambiar la edad de jubilación es
tocar una línea.

Y funciona en las dos direcciones: `SET ES-JUBILADO TO TRUE` **asigna el primer valor del rango** a
la variable.

Es lo más cerca que llega COBOL del subtipo con rango de Pascal y Ada, y para lo que se usa —reglas
de negocio con umbrales— resulta sorprendentemente adecuado.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program rango
   implicit none
   integer :: a, b, i, j
   character(len=400) :: salida
   character(len=20)  :: buf

   read(*, *) a, b

   salida = ''
   do i = a, b
      write(buf, '(I0)') i
      if (i == a) then
         salida = trim(buf)
      else
         salida = trim(salida) // '-' // trim(buf)
      end if
   end do

   write(*, '(A,I0)') 'rango=' // trim(salida) // ' suma=', &
                      sum([(j, j = a, b)])      ! constructor con do implícito
end program rango
```

**Lo que esta clase enseña en Fortran.** La expresión `[(j, j = a, b)]` es un **constructor de arreglo
con `do` implícito**, y es la forma que tiene Fortran de escribir un rango como valor.

```fortran
[(j, j = 1, 10)]              ! 1, 2, ..., 10
[(j, j = 10, 1, -1)]          ! al revés
[(j*j, j = 1, 5)]             ! 1, 4, 9, 16, 25 -- una comprensión de lista
[(v(j), j = 1, n, 2)]         ! los elementos impares de v
```

Esa última forma —**el `do` implícito con paso**— es la comprensión de listas de Fortran, y existe
desde 1957 en la entrada/salida:

```fortran
      WRITE (6, 100) (V(J), J = 1, N)
```

Escribir los `n` primeros elementos con un `do` dentro de la lista de salida es Fortran original, y
sobrevive intacto.

Fortran tiene además **secciones de arreglo**, que son rangos aplicados a la indexación:

```fortran
v(2:5)        ! los elementos del 2 al 5
v(2:10:2)     ! del 2 al 10, de dos en dos
v(:)          ! todos
a(3, :)       ! la fila 3 completa
a(:, 3)       ! la columna 3
```

Una sección **es un arreglo**: se puede asignar, pasar a una función y operar con ella. `v(2:5) = 0`
pone cuatro elementos a cero en una línea, y `a(:, 3) = a(:, 3) * 2` duplica una columna entera.

Ese es el corte por rebanadas que hoy usan NumPy, MATLAB, Julia y R — todos lo tomaron de aquí.

Y en la entrada/salida, el `do` implícito se combina con secciones para leer y escribir estructuras
complejas en una sola sentencia, sin bucle explícito.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Rango is
   A, B : Integer;
   Suma : Integer := 0;
begin
   Get (A);
   Get (B);

   Put ("rango=");
   for I in A .. B loop        --  A .. B es un RANGO, no una construcción del for
      Put (I, Width => 1);
      Suma := Suma + I;
      if I < B then
         Put ("-");
      end if;
   end loop;

   Put (" suma=");
   Put (Suma, Width => 1);
   New_Line;
end Rango;
```

**Lo que esta clase enseña en Ada.** En Ada, `A .. B` es un **rango**, y la palabra clave está en que
sirve en cuatro sitios distintos con la misma notación:

```ada
subtype Dia_Mes is Integer range 1 .. 31;      --  declarar un SUBTIPO
type Tabla is array (1 .. 12) of Float;         --  el índice de un arreglo
for I in 1 .. 10 loop ... end loop;             --  recorrer
case N is
   when 1 .. 9   => ...                          --  elegir
   when 10 .. 99 => ...
end case;
```

El **subtipo con rango** es la pieza importante, y es lo que Pascal inventó y Ada llevó al final:

```ada
subtype Dia_Mes is Integer range 1 .. 31;
D : Dia_Mes := 15;

D := 32;              --  NO COMPILA: el compilador lo ve
D := Leer_Numero;     --  compila, y lanza Constraint_Error en ejecución si no cabe
```

Ada comprueba el rango **en las dos fases**: lo que puede decidir al compilar, lo decide; lo que
depende de un dato de entrada, lo comprueba al asignar. Un `Dia_Mes` **nunca contiene 32**, en ningún
punto del programa.

Eso cambia dónde está la validación: en lugar de un `if` en cada función que recibe un día, hay una
línea en la declaración del tipo. Es la idea que hoy se llama *hacer que los estados inválidos sean
irrepresentables*, escrita en 1983.

Y los atributos completan el cuadro: `Dia_Mes'First`, `Dia_Mes'Last`, `Dia_Mes'Range`,
`Dia_Mes'Succ (D)`, `Dia_Mes'Pred (D)`, `Dia_Mes'Image (D)`. El tipo sabe hablar de sí mismo.

Ada 2012 añadió los **predicados**, que generalizan el rango a cualquier condición:

```ada
subtype Par is Integer with Dynamic_Predicate => Par mod 2 = 0;
```

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Rango;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  A, B, I, Suma: Integer;
  Salida: string;

begin
  Read(A, B);

  Salida := '';
  Suma := 0;
  for I := A to B do
  begin
    if Salida <> '' then Salida := Salida + '-';
    Salida := Salida + IntToStr(I);
    Suma := Suma + I;
  end;

  WriteLn('rango=', Salida, ' suma=', IntToStr(Suma));
end.
```

**Lo que esta clase enseña en Pascal.** **Pascal inventó el tipo subrango**, en 1970, y de ahí lo tomó
Ada.

```pascal
type
  TDiaMes = 1..31;
  TLetra  = 'a'..'z';
  TDia    = (Lun, Mar, Mie, Jue, Vie);
  TLaboral = Lun..Vie;          { subrango de una ENUMERACIÓN }
```

Un subrango es un tipo nuevo, y sirve para lo mismo que en Ada: declarar variables acotadas, indexar
arreglos y elegir en un `case`. Con `{$RANGECHECKS ON}`, asignarle un valor fuera de rango **lanza un
error en ejecución**; sin él, no se comprueba nada.

Ese "sin él, no se comprueba nada" es la diferencia práctica con Ada, y explica por qué la reputación
de seguridad de los dos lenguajes es distinta pese a tener la misma característica.

Pascal tiene además dos construcciones que dependen del subrango y que Ada escribió después:

**El `case` con rangos y conjuntos:**

```pascal
case C of
  'a'..'z', 'A'..'Z': WriteLn('letra');
  '0'..'9':           WriteLn('dígito');
else                  WriteLn('otro');
end;
```

**Y el tipo conjunto, limitado precisamente por el subrango** (clase 094):

```pascal
type TDigitos = set of '0'..'9';
```

Sobre el bucle, hay un detalle de diseño que merece mención: **el `for` de Pascal solo cuenta de uno
en uno**, hacia arriba (`to`) o hacia abajo (`downto`). No hay paso. Wirth lo decidió así
deliberadamente —un `for` con paso arbitrario es un `while` disfrazado— y para todo lo demás está
`while`. Es la misma austeridad que dejó fuera el `return` anticipado y el `break` en el Pascal
original.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((a (read))
       (b (read))
       (r (loop for i from a to b collect i)))
  (format t "rango=~{~D~^-~} suma=~D~%" r (reduce #'+ r)))
```

**Lo que esta clase enseña en Common Lisp.** `loop` es, con diferencia, la macro más grande del
estándar, y una de las más discutidas: **tiene su propia sintaxis, con palabras clave en inglés, que
no se parece en nada al resto de Lisp**.

```lisp
(loop for i from a to b collect i)
(loop for i from 10 downto 1 by 2 collect i)
(loop for x in lista when (evenp x) sum x)
(loop for (clave . valor) in alista do (print clave))
(loop for i from 0 for x across vector collect (cons i x))
(loop repeat 5 collect (random 100))
```

Que un lenguaje famoso por su uniformidad —todo son paréntesis— incorpore un minilenguaje con
`for`, `while`, `collect`, `sum`, `maximize`, `when`, `into` y `finally` fue polémico en el comité de
Common Lisp, y ganó por una razón práctica: **el código con `loop` se lee mejor** que el equivalente
con `do` y acumuladores explícitos.

Y `loop` es una **macro**: se expande a código Lisp normal en tiempo de compilación. Es decir, esa
sintaxis ajena **está escrita en el propio lenguaje**, sin tocar el compilador. Ese es el argumento
más fuerte a favor de las macros de Lisp, y esta clase lo muestra sin necesidad de explicarlo.

Para rangos como valor, Common Lisp no tiene un tipo `Range` —el rango se materializa como lista o
vector— pero sí tiene **especificadores de tipo con rango**, que son el subrango de Pascal:

```lisp
(deftype dia-mes () '(integer 1 31))
(declare (type (integer 0 255) b))
```

Con `(optimize (safety 3))`, SBCL **comprueba esas declaraciones en ejecución**; con `(speed 3)` las
usa para generar aritmética de máquina sin comprobaciones. La misma declaración sirve para verificar
o para optimizar, según lo que se pida.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [split [string trim $linea]] a b

set r {}
set suma 0
for {set i $a} {$i <= $b} {incr i} {
    lappend r $i
    incr suma $i
}

puts "rango=[join $r -] suma=$suma"
```

**Lo que esta clase enseña en Tcl.** **Tcl no tiene rangos**, y su `for` es el de C, con las cuatro
partes entre llaves:

```tcl
for {set i 0} {$i < 10} {incr i} { ... }
```

Y aquí conviene ver lo que realmente pasa, porque explica el lenguaje entero: **`for` es un comando
normal que recibe cuatro cadenas** —inicialización, condición, incremento y cuerpo— y las evalúa como
guiones. No hay sintaxis de bucle; hay un comando con cuatro argumentos.

Por eso las llaves importan tanto: `{$i < 10}` se pasa **sin sustituir**, para que `for` la evalúe en
cada vuelta. Si se escribieran comillas, `$i` se sustituiría **una sola vez** y el bucle sería infinito.

Tcl 8.7 añadió por fin el generador de secuencias:

```tcl
lseq 1 10           ;# {1 2 3 4 5 6 7 8 9 10}
lseq 10 1 -1        ;# al revés
lseq 0 100 5        ;# con paso
```

Y `lseq` tiene un detalle interesante: **devuelve una lista perezosa**. La representación interna es
"desde, hasta, paso", y los elementos se generan al pedirlos, así que `lseq 1 1000000` no reserva un
millón de enteros. Es el `range` de Python 3, con veinte años de diferencia.

`incr` merece una nota: es un comando dedicado a incrementar una variable entera **en el sitio**, sin
pasar por `expr`. Es notablemente más rápido que `set i [expr {$i + 1}]` porque no reconstruye el
valor, y es uno de los pocos casos en que Tcl optimiza un caso particular por rendimiento.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;
use List::Util qw(sum);

my $linea = <STDIN>;
chomp $linea;
my ($a, $b) = split ' ', $linea;

my @r = ($a .. $b);            # el operador de rango

print "rango=", join('-', @r), " suma=", sum(@r), "\n";
```

**Lo que esta clase enseña en Perl.** El operador **`..`** construye la lista completa, y funciona
también sobre cadenas con una regla de incremento propia:

```perl
(1 .. 10)          # 1, 2, ..., 10
('a' .. 'e')       # a, b, c, d, e
('aa' .. 'ad')     # aa, ab, ac, ad
('Aa' .. 'Zz')     # sí, también
```

Ese incremento mágico de cadenas —`'az'` seguido de `'ba'`— es una rareza deliberada de Perl que
resulta útil para generar identificadores y columnas de hoja de cálculo.

Y hay que saber que **`..` construye la lista entera en memoria**: `(1 .. 10_000_000)` reserva diez
millones de escalares. Para recorrer sin materializar está el `for` de estilo C, y Perl optimiza
específicamente el caso `foreach my $i (1 .. $n)` para no construir la lista.

Ahora la parte extraña, y es una de las de mayor personalidad del lenguaje: **`..` en contexto escalar
NO es un rango, es el operador *flip-flop***.

```perl
while (<>) {
    print if /INICIO/ .. /FIN/;     # imprime DESDE la línea que casa INICIO
}                                    # HASTA la que casa FIN
```

Es un operador con **estado interno**: devuelve falso hasta que el lado izquierdo es cierto, entonces
devuelve cierto hasta que el derecho lo sea. Viene directamente de `sed` y `awk`, y sirve para
extraer secciones de un fichero en una línea.

Perl es el único lenguaje de esta página con un operador que **recuerda** lo que pasó en llamadas
anteriores. Es brillante para procesar texto y es exactamente el tipo de cosa que hace que el
lenguaje divida opiniones.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <cstddef>
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::vector<int> r(static_cast<std::size_t>(b - a + 1));
    std::iota(r.begin(), r.end(), a);      // rellena a, a+1, ..., b

    std::cout << "rango=";
    for (std::size_t i = 0; i < r.size(); ++i) {
        if (i != 0) std::cout << '-';
        std::cout << r[i];
    }
    std::cout << " suma=" << std::accumulate(r.begin(), r.end(), 0) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** Durante veintidós años, **un rango en C++ eran dos iteradores**:

```cpp
std::sort(v.begin(), v.end());
std::accumulate(v.begin(), v.end(), 0);
```

Ese diseño —el de la STL de Stepanov, 1994— es potentísimo y tiene un problema evidente que todo el
mundo ha sufrido: **nada impide mezclar iteradores de dos contenedores distintos**, y el resultado es
comportamiento indefinido sin ningún aviso.

`std::iota` rellena un rango con valores consecutivos, y su nombre viene de APL, donde la letra griega
iota generaba exactamente eso. Es probablemente el nombre más críptico de la biblioteca estándar.

**C++20 arregló el diseño con las *ranges*:**

```cpp
#include <ranges>

for (int i : std::views::iota(a, b + 1)) { ... }     // rango PEREZOSO, sin memoria
std::ranges::sort(v);                                 // el contenedor, no dos iteradores

auto pares = v | std::views::filter([](int x) { return x % 2 == 0; })
               | std::views::transform([](int x) { return x * x; });
```

Tres mejoras a la vez: **un rango es un objeto** —imposible mezclar extremos—, **las vistas son
perezosas** —`views::iota(1, 1'000'000)` no reserva nada— y **se componen con `|`**, que es la tubería
de Unix aplicada a los datos.

Es el cambio más grande en la biblioteca estándar desde 1998, y llegó a una conclusión a la que Ada
había llegado en 1983 por otro camino: **el rango merece ser un valor**.

Este programa usa el estilo clásico porque el curso compila con `-std=c++17`, que es lo que todavía
usan la mayoría de los proyectos en producción.

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

dcl-pi RANGO;
  a int(10) const;
  b int(10) const;
end-pi;

dcl-s i      int(10);
dcl-s suma   int(20) inz(0);
dcl-s salida varchar(200) inz('');

for i = a to b;
  if salida <> '';
    salida += '-';
  endif;
  salida += %char(i);
  suma += i;
endfor;

dsply ('rango=' + salida + ' suma=' + %char(suma));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG **no tiene rangos como valores**, y su `for` es el habitual,
con `by` para el paso y `downto` para bajar:

```rpgle
for i = 1 to 10;
for i = 10 downto 1;
for i = 0 to 100 by 5;
```

Donde sí aparece la idea de rango en RPG es en la operación que da nombre al lenguaje: **el ciclo de
proceso de informes**. En el RPG de columnas, un programa no tenía bucle principal escrito: el
compilador generaba uno que leía el fichero primario, evaluaba los **niveles de ruptura** (`L1` a
`L9`) y ejecutaba automáticamente los totales al cambiar de grupo.

```text
        Al cambiar el código de cliente  -> imprimir el total del cliente
        Al cambiar la provincia          -> imprimir el total de la provincia
```

Ese "rango de registros que comparten una clave" era el concepto central del lenguaje, y estaba
**integrado en el ciclo**, no escrito por el programador. Es agrupación declarativa, y es la razón de
que RPG generara informes con una fracción del código de COBOL.

El RPG libre moderno **no usa el ciclo**: se escribe `main()` y bucles explícitos, como en este
programa. Pero el ciclo sigue existiendo por compatibilidad, y sigue habiendo programas de los años
ochenta corriendo con él en producción.

Para trabajar con rangos de datos, RPG moderno delega en SQL incrustado, que es lo idiomático hoy:

```rpgle
exec sql select sum(importe) into :total
         from ventas where fecha between :desde and :hasta;
```

`between` es el rango de SQL, y en IBM i es lo que se usa para casi todo lo que esta clase plantea.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 rango: procedure options(main);

    declare (a, b, i) fixed binary(31);
    declare suma fixed binary(31) initial(0);
    declare salida char(200) varying initial('');

    get list (a, b);

    do i = a to b;
       if salida ^= '' then salida = salida || '-';
       salida = salida || trim(char(i));
       suma = suma + i;
    end;

    put skip list ('rango=' || salida || ' suma=' || trim(char(suma)));

 end rango;
```

**Lo que esta clase enseña en PL/I.** El `do` de PL/I es el bucle más completo de esta página, porque
**combina en una sola sentencia lo que otros lenguajes reparten en tres**:

```pli
 do i = 1 to 10;                          /* contado */
 do i = 1 to 10 by 2;                      /* con paso */
 do i = 10 to 1 by -1;                     /* descendente */
 do while (x > 0);                          /* condicional */
 do until (x = 0);                          /* al menos una vez */
 do i = 1 to 10 while (encontrado = '0'b);  /* CONTADO Y CONDICIONAL a la vez */
 do i = 1, 3, 7, 11;                        /* una LISTA de valores */
 do i = 1 to 5, 10 to 15;                   /* VARIOS rangos */
```

Las tres últimas no las tiene ningún lenguaje del núcleo. `do i = 1 to 10 while (...)` recorre un
rango **y** se detiene si deja de cumplirse una condición, sin `break` ni bandera. Y
`do i = 1 to 5, 10 to 15` recorre dos tramos con una sola cabecera.

PL/I añade además una construcción que hoy tiene otro nombre: el **grupo `do` con `repeat`**, que es
la iteración por transformación sucesiva.

```pli
 do p = raiz repeat (p -> siguiente) while (p ^= null());
```

`repeat` dice **cómo pasar del elemento actual al siguiente**, así que ese bucle recorre una lista
enlazada sin índice. Es el iterador escrito en la cabecera del bucle.

Y en cuanto a rangos como tipo, PL/I **no tiene subrangos**: las variables se declaran por precisión
—`fixed decimal(5,2)`— no por rango de valores. Es la carencia que Pascal cubrió seis años después y
que Ada convirtió en el centro de su diseño.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
RANGO ; Rangos y secuencias -- clase 092
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 set salida = "", suma = 0
 for i=a:1:b do
 . if salida '= "" set salida = salida _ "-"
 . set salida = salida _ i
 . set suma = suma + i
 write "rango=", salida, " suma=", suma, !
 quit
```

**Lo que esta clase enseña en M.** El `for` de M se escribe con dos puntos y es de una concisión
extrema: **`for i=a:1:b`** es inicio, paso y límite.

Y tiene tres formas que conviene distinguir, porque la tercera es la que de verdad usa el código real:

```mumps
 for i=1:1:10 ...           ; contado, con límite
 for i=1:1 ...              ; SIN límite -- infinito hasta un quit
 for i="a","b","c" ...      ; una lista de valores
 for  set i=$order(v(i)) quit:i=""  ...    ; recorrer un ÁRBOL
```

La última no lleva variable de control en el `for` —fíjate en los **dos espacios**, que es la sintaxis
de "for sin argumentos"— y es el idioma universal de M para recorrer una estructura de datos.
`$order` devuelve el siguiente subíndice existente en orden, y la cadena vacía cuando se acaban.

Eso es un iterador, y es más potente que un rango por una razón concreta: **funciona igual sobre una
variable local y sobre un global en disco de diez millones de registros**.

```mumps
 for  set id=$order(^PAC(id))  quit:id=""  do procesar(id)
```

Ese bucle recorre una base de datos entera, ordenada, sin cargarla en memoria y sin SQL. Es un
recorrido de índice B-árbol expresado como bucle del lenguaje, y es exactamente lo que hace un cursor
en una base de datos relacional — con la diferencia de que aquí es una construcción del lenguaje, no
de una API.

Y `quit:i=""` es el **postcondicional** de la clase 060: `quit` se ejecuta solo si la condición se
cumple. Sin él, el bucle sin argumentos no terminaría nunca.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| partes a b r |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

r := (a to: b) asOrderedCollection.

Transcript
    show: 'rango=', ((r collect: [ :cada | cada printString ])
                        inject: '' into: [ :acc :cada |
                            acc isEmpty ifTrue: [ cada ] ifFalse: [ acc, '-', cada ] ]);
    show: ' suma=', (r inject: 0 into: [ :acc :cada | acc + cada ]) printString;
    cr.
```

**Lo que esta clase enseña en Smalltalk.** `a to: b` **no es sintaxis de bucle: es un mensaje enviado
a un número**, y devuelve un objeto de la clase **`Interval`**.

```smalltalk
(1 to: 10)              "un Interval, que ES una colección"
(1 to: 10 by: 2)
(10 to: 1 by: -1)
(1 to: 10) asArray
(1 to: 10) inject: 0 into: [ :a :b | a + b ]
(1 to: 10) select: [ :x | x even ]
```

Que el rango sea **una colección de pleno derecho** significa que responde a todo el protocolo de la
clase 089: `collect:`, `select:`, `detect:`, `includes:`, `reverse`. Es la misma conclusión a la que
llegó C++20 con las *ranges*, cuarenta y cinco años antes.

Y `Interval` es **perezoso**: guarda inicio, fin y paso, y calcula los elementos al pedirlos. `1 to:
1000000` es un objeto de tres campos.

El bucle habitual se escribe igualmente como un mensaje:

```smalltalk
1 to: 10 do: [ :i | ... ]           "optimizado por el compilador"
10 timesRepeat: [ ... ]
[ x > 0 ] whileTrue: [ ... ]
```

`to:do:` y `whileTrue:` son mensajes con bloques, no construcciones del lenguaje — y ese es el punto
de la clase 062: **Smalltalk no tiene sentencias de control**. El compilador los reconoce e integra en
línea por rendimiento, pero **si los envías a un objeto que no sea un número, funcionan igualmente**
como envíos normales.

Esa es la diferencia entre optimizar un caso frecuente y añadir sintaxis: el modelo sigue siendo
uniforme.

---

## Y de vuelta a la clase

Lo transferible: **cuando un lenguaje convierte el rango en un tipo, el error se detecta en la
declaración y no en el bucle**. Escribir `range 1 .. 31` una vez evita comprobar `if dia > 31` en
veinte sitios. La versión moderna de esa idea son los tipos refinados y las precondiciones; la versión
de 1970 era una línea de Pascal, y en muchos casos sigue siendo suficiente.

⏮️ [Volver a la clase 092](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
