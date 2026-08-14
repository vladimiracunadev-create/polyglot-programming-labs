# -*- coding: utf-8 -*-
"""Parte 6, lote C — clases 092 y 093. Ver `vivos_parte6.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 092 — Rangos y secuencias
# ---------------------------------------------------------------------------
SPECS["092"] = dict(
    gancho="""
Los enteros de `a` hasta `b`, listados y sumados. Parece la clase más inocente de la parte, y esconde
una de las ideas mejor pensadas del diseño de lenguajes: **en Ada y en Pascal el rango es un tipo**,
no un bucle. `1 .. 10` sirve para declarar un arreglo, para acotar una variable, para elegir en un
`case` y para recorrer — **la misma notación en los cuatro sitios**.
""",
    porque="""
Aquí el concepto es la **secuencia definida por sus extremos**, y estos lenguajes lo enseñan porque
Pascal y Ada lo elevaron a categoría de tipo. Un `subtype Dia is Integer range 1 .. 31` no es
documentación: **el compilador rechaza asignarle 32**, y en Ada lo comprueba también en ejecución.

Enfrente, **COBOL, Fortran, Tcl y M no tienen rangos**: tienen bucles. Y **Perl** tiene el operador
`..`, que además esconde el *flip-flop*, uno de los operadores más extraños que existen. **C++**
tardó hasta C++20 en tener `views::iota`, y hasta entonces el rango se escribía como dos iteradores.
""",
    cierre="""
Lo transferible: **cuando un lenguaje convierte el rango en un tipo, el error se detecta en la
declaración y no en el bucle**. Escribir `range 1 .. 31` una vez evita comprobar `if dia > 31` en
veinte sitios. La versión moderna de esa idea son los tipos refinados y las precondiciones; la versión
de 1970 era una línea de Pascal, y en muchos casos sigue siendo suficiente.
""",
    langs={
        "cobol": ("""
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
""", """
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
"""),
        "fortran": ("""
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
""", """
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
"""),
        "ada": ("""
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
""", """
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
"""),
        "pascal": ("""
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
""", """
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
"""),
        "lisp": ("""
(let* ((a (read))
       (b (read))
       (r (loop for i from a to b collect i)))
  (format t "rango=~{~D~^-~} suma=~D~%" r (reduce #'+ r)))
""", """
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
"""),
        "tcl": ("""
gets stdin linea
lassign [split [string trim $linea]] a b

set r {}
set suma 0
for {set i $a} {$i <= $b} {incr i} {
    lappend r $i
    incr suma $i
}

puts "rango=[join $r -] suma=$suma"
""", """
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
"""),
        "perl": ("""
use strict;
use warnings;
use List::Util qw(sum);

my $linea = <STDIN>;
chomp $linea;
my ($a, $b) = split ' ', $linea;

my @r = ($a .. $b);            # el operador de rango

print "rango=", join('-', @r), " suma=", sum(@r), "\\n";
""", """
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
"""),
        "cpp": ("""
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
    std::cout << " suma=" << std::accumulate(r.begin(), r.end(), 0) << '\\n';
    return 0;
}
""", """
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
"""),
        "rpg": ("""
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
""", """
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
"""),
        "pli": ("""
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
""", """
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
"""),
        "mumps": ("""
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
""", """
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
"""),
        "smalltalk": ("""
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
""", """
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
"""),
    },
)

# ---------------------------------------------------------------------------
# 093 — Cadenas como estructura de datos
# ---------------------------------------------------------------------------
SPECS["093"] = dict(
    gancho="""
Invertir una palabra. La operación más trivial de la parte, y la que destapa la diferencia más grande
entre estos lenguajes: **para COBOL, Fortran, RPG y PL/I una cadena es un campo de longitud fija
rellenado con espacios**, y esa decisión —tomada cuando los datos vivían en tarjetas de ochenta
columnas— sigue condicionando cómo se escribe el código sesenta años después.
""",
    porque="""
Aquí el concepto es **qué es una cadena realmente**, y estos lenguajes lo enseñan porque cubren las
tres respuestas posibles. **Longitud fija con relleno**: COBOL, Fortran, PL/I con `char(n)`, RPG con
`char`. **Longitud variable con prefijo**: PL/I `varying`, RPG `varchar`, Pascal `ShortString`.
**Puntero a bloque contado**: C++, Perl, Tcl, Lisp, Pascal moderno.

Y de ahí sale el detalle que más código ha generado en la historia: **si una cadena es de longitud
fija, comparar "ADA" con "ADA   " requiere decidir qué hacer con los espacios**, y cada lenguaje
decidió distinto.
""",
    cierre="""
Lo transferible: **el relleno con espacios no es una torpeza antigua, es lo que exige un fichero de
registros de longitud fija**, y ese formato sigue moviendo la mayor parte de los datos bancarios del
mundo. Cuando veas `TRIM` en cada línea de un programa COBOL o RPG, no estás viendo código
descuidado: estás viendo la frontera entre un modelo de datos posicional y uno de longitud variable.
La misma frontera aparece hoy al leer un fichero de ancho fijo con Pandas.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. CADENA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  N       PIC 9(4) COMP.
01  INVER   PIC X(200).

PROCEDURE DIVISION.
    ACCEPT LINEA

    MOVE 0 TO N
    INSPECT FUNCTION REVERSE(LINEA) TALLYING N FOR LEADING SPACE
    COMPUTE N = 200 - N

    MOVE FUNCTION REVERSE(LINEA(1:N)) TO INVER

    DISPLAY "invertido=" INVER(1:N)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** `PIC X(200)` es **siempre** doscientos caracteres. Al mover
`"hola"` a ese campo, COBOL guarda `hola` seguido de **196 espacios**, y no hay ninguna forma de que
el campo "sepa" que solo cuatro son significativos.

De ahí la línea más rara de este programa:

```cobol
INSPECT FUNCTION REVERSE(LINEA) TALLYING N FOR LEADING SPACE
COMPUTE N = 200 - N
```

Se invierte la cadena, se cuentan los espacios que quedan **delante**, y se restan del total. Ese es
el idioma canónico para averiguar la longitud útil de un campo COBOL, y aparece en millones de líneas
de código. COBOL 2002 añadió `FUNCTION LENGTH` con `TRAILING`, y muchos compiladores ofrecen
`FUNCTION STORED-CHAR-LENGTH`, pero el truco del `REVERSE` es lo que se encuentra en el código
existente.

El manejo de cadenas de COBOL es sorprendentemente completo para su fama, y todo gira alrededor de
posiciones fijas:

```cobol
MOVE LINEA(5:10) TO TROZO           *> "referencia modificada": desde 5, 10 chars
STRING A DELIMITED SIZE B DELIMITED SPACE INTO C
UNSTRING C DELIMITED BY "," INTO P1 P2 P3
INSPECT T REPLACING ALL "a" BY "A"
INSPECT T TALLYING N FOR ALL ","
FUNCTION UPPER-CASE(T)   FUNCTION TRIM(T)   FUNCTION REVERSE(T)
```

`STRING` y `UNSTRING` son concatenación y división con delimitadores, y llevan cláusulas
`POINTER` y `OVERFLOW` para controlar dónde escriben y qué pasa si no cabe. Es verboso y es
**explícito sobre el desbordamiento**, que es más de lo que ofrecía C durante treinta años.

Y la comparación ignora los espacios finales: `IF NOMBRE = "ADA"` es cierto para `"ADA      "`, porque
COBOL rellena el operando corto antes de comparar. Es una decisión sensata para su modelo de datos, y
sorprende a todo el que llega de otro lenguaje.
"""),
        "fortran": ("""
program cadena
   implicit none
   character(len=200) :: linea
   integer :: n, i

   read(*, '(A)') linea
   n = len_trim(linea)              ! longitud SIN los espacios finales

   write(*, '(A)', advance='no') 'invertido='
   do i = n, 1, -1
      write(*, '(A)', advance='no') linea(i:i)
   end do
   write(*, '(A)') ''
end program cadena
""", """
**Lo que esta clase enseña en Fortran.** Como en COBOL, `character(len=200)` es **siempre** doscientos
caracteres rellenos de espacios, y de ahí que `len_trim` —la longitud sin los espacios finales— sea
una de las funciones más usadas del lenguaje.

```fortran
len(s)              ! la longitud DECLARADA: siempre 200
len_trim(s)         ! la longitud ÚTIL
trim(s)             ! la cadena sin espacios finales
adjustl(s)          ! desplaza a la izquierda
s(3:7)              ! subcadena: los caracteres 3 a 7
s(i:i)              ! UN carácter -- Fortran no tiene tipo carácter suelto
```

Fíjate en `s(i:i)`: en Fortran **no existe el "carácter" como tipo distinto de la cadena**. Un
carácter es una cadena de longitud 1, y por eso el índice se escribe dos veces. Es coherente y
desconcierta la primera vez.

El operador de concatenación es **`//`**, elegido porque `+` estaba reservado para la aritmética y el
lenguaje no tiene sobrecarga en su versión original.

Fortran 2003 trajo la mejora que faltaba: **las cadenas de longitud diferida**.

```fortran
character(len=:), allocatable :: s
s = 'hola'                    ! toma la longitud exacta: 4
s = s // ' mundo'             ! se REASIGNA a 10
```

Con `len=:` y `allocatable`, la cadena se ajusta sola al asignarla, y por fin se puede escribir código
de manipulación de texto sin declarar tamaños máximos. Es la diferencia entre el Fortran que se ve en
los códigos científicos antiguos —lleno de `character(len=256)`— y el moderno.

Y la lectura con `read(*, '(A)')` sobre un `character(len=200)` rellena con espacios lo que sobra:
otra vez el modelo de la tarjeta perforada, funcionando en 2026.
"""),
        "ada": ("""
with Ada.Text_IO; use Ada.Text_IO;

procedure Cadena is
   Linea  : String (1 .. 200);
   Ultimo : Natural;
begin
   Get_Line (Linea, Ultimo);

   Put ("invertido=");
   for I in reverse 1 .. Ultimo loop
      Put (Linea (I));
   end loop;
   New_Line;
end Cadena;
""", """
**Lo que esta clase enseña en Ada.** El `String` de Ada **es un arreglo de caracteres**, literalmente:
`type String is array (Positive range <>) of Character`. No es un tipo especial, y por eso hereda todo
lo de la clase 089 — `S'Length`, `S'First`, `S'Last`, secciones, comparación, concatenación con `&`.

Y trae la consecuencia incómoda del arreglo no restringido: **la longitud forma parte del valor**, así
que una variable `String` tiene un tamaño fijo desde que se crea. `Get_Line` devuelve por eso **dos**
cosas: el búfer y hasta dónde llenó.

Ada resuelve el resto con **tres tipos de cadena**, y elegir entre ellos es una decisión de diseño
real:

| Tipo | Paquete | Cuándo |
|---|---|---|
| `String` | integrado | longitud conocida y fija |
| `Bounded_String` | `Ada.Strings.Bounded` | **máximo conocido, sin memoria dinámica** |
| `Unbounded_String` | `Ada.Strings.Unbounded` | longitud arbitraria |

`Bounded_String` es el que no tiene equivalente en el núcleo, y existe por la misma razón que los
contenedores llegaron tarde (clase 090): **en sistemas empotrados certificados no se puede reservar
memoria**. Una cadena acotada guarda un búfer de tamaño máximo y una longitud, todo en la pila, y
ofrece el mismo interfaz que la ilimitada.

```ada
package Nombres is new Ada.Strings.Bounded.Generic_Bounded_Length (Max => 80);
```

Ada tiene además `Ada.Strings.Fixed` con `Index`, `Trim`, `Replace_Slice` y `Head`/`Tail`, y desde
Ada 2012 el soporte completo de Unicode con `Wide_Wide_String` (UTF-32) y `Ada.Strings.UTF_Encoding`.

Tres tipos donde otros lenguajes tienen uno es más trabajo, y es exactamente el tipo de decisión que
Ada obliga a tomar explícitamente en lugar de esconderla.
"""),
        "pascal": ("""
program Cadena;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  S, R: string;
  I: Integer;

begin
  ReadLn(S);
  S := Trim(S);

  R := '';
  for I := Length(S) downto 1 do
    R := R + S[I];

  WriteLn('invertido=', R);
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal tiene la historia de cadenas más accidentada de esta
página, y merece contarse porque explica la directiva `{$H+}` que aparece en todos los programas de
este curso.

**El Pascal original de Wirth no tenía cadenas.** Solo `packed array[1..n] of Char`, con las mismas
limitaciones que Fortran y COBOL.

**Turbo Pascal inventó la `ShortString`**: un arreglo de 256 bytes donde **el byte 0 guarda la
longitud**. De ahí el límite de 255 caracteres, y de ahí que `Length(S)` sea instantáneo — es leer un
byte. Fue una solución brillante para 1983 y una restricción severa después.

**Delphi 2 (1996) trajo la `AnsiString`**, que es lo que hoy se llama `string`: puntero a un bloque
con longitud y **contador de referencias**, gestionada automáticamente, sin límite práctico.

```pascal
{$H+}      { string = AnsiString, larga }
{$H-}      { string = ShortString, 255 caracteres }
```

Esa directiva sigue existiendo por compatibilidad, y es la razón de que todo código Free Pascal
moderno empiece con `{$H+}`.

Y hay un detalle que sorprende a quien viene de C: **las cadenas de Pascal empiezan en el índice 1**.
`S[1]` es el primer carácter. Es coherente con los arreglos del lenguaje, y es una de las
incompatibilidades más molestas al portar código.

Las cadenas modernas son **contadas por referencia y con copia al escribir**: asignar no copia, y la
copia solo ocurre al modificar una cadena compartida. Concatenar en un bucle —como hace este
programa— es por tanto O(n²), y para volúmenes grandes lo idiomático es `TStringBuilder`.

Hoy conviven además `UnicodeString` (UTF-16) y `UTF8String`, con conversión automática entre ellas —
cómodo, y una fuente conocida de conversiones invisibles que cuestan rendimiento.
"""),
        "lisp": ("""
(let ((s (string-trim '(#\\Space #\\Return #\\Tab) (read-line))))
  (format t "invertido=~A~%" (reverse s)))
""", """
**Lo que esta clase enseña en Common Lisp.** En Common Lisp, **una cadena es un vector de
caracteres**, igual que en Ada: `string` es un subtipo de `vector`, que a su vez lo es de `array` y
de `sequence`.

Y de ahí sale lo que hace elegante a esta implementación: **`reverse` no es una función de cadenas**.
Es la función de secuencias, y funciona igual sobre una lista, un vector o una cadena. Lo mismo vale
para `length`, `subseq`, `position`, `find`, `remove`, `sort`, `count` y `map`.

```lisp
(reverse "hola")          ; "aloh"
(reverse '(1 2 3))        ; (3 2 1)
(subseq "hola mundo" 5)   ; "mundo"
(position #\\a "hola")     ; 3
(count #\\a "banana")      ; 3
(map 'string #'char-upcase "hola")   ; "HOLA"
```

Un solo juego de funciones para todas las secuencias: eso es lo que consiguió Common Lisp al unificar
la biblioteca en 1984, y es más de lo que tienen la mayoría de los lenguajes de esta página.

El carácter **sí es un tipo propio** —`#\\a`, `#\\Space`, `#\\Newline`— al contrario que en Fortran.

Y las cadenas son **mutables** si se crean como tales, lo que sorprende a quien viene de Java o
Python:

```lisp
(let ((s (copy-seq "hola")))
  (setf (aref s 0) #\\H)
  s)                             ; "Hola"
```

Modificar un literal de cadena, en cambio, es comportamiento indefinido: el compilador puede
colocarlo en memoria de solo lectura o compartir literales iguales. Es la misma trampa que en C.

Para construir texto por trozos, el idioma eficiente es `with-output-to-string`, que evita el
`concatenate` cuadrático:

```lisp
(with-output-to-string (s) (dolist (x lista) (format s "~A-" x)))
```
"""),
        "tcl": ("""
gets stdin linea
puts "invertido=[string reverse [string trim $linea]]"
""", """
**Lo que esta clase enseña en Tcl.** Tcl es **el lenguaje de esta página cuya cadena es el tipo
fundamental**: su lema fundacional es *everything is a string*, y de ahí viene todo lo demás.

`string` es un comando con más de treinta subcomandos, que cubren esta clase entera:

```tcl
string reverse $s        string length $s       string index $s 0
string range $s 2 5      string toupper $s      string trim $s
string map {a A b B} $s  string first "x" $s    string repeat "ab" 3
string match "*.txt" $s  string is integer $s   string cat $a $b
```

`string map` es especialmente potente: sustituye **varios pares a la vez, en una pasada**, sin
solaparse. `string is` es el validador de tipos del lenguaje —`string is integer`, `is double`, `is
alnum`, `is boolean`— y es la forma idiomática de comprobar un dato de entrada.

Debajo, la realidad es mucho más elaborada que "todo es una cadena": desde Tcl 8.1 **las cadenas son
UTF-8 internamente y se indexan por carácter**, no por byte. `string length "ñandú"` devuelve 5. Tcl
tuvo soporte Unicode correcto **en 1999**, antes que casi todos los lenguajes de esta página.

Y desde Tcl 9.0 (2024), el soporte se completó con cadenas de longitud arbitraria por encima de 2 GB y
manejo pleno de los caracteres fuera del plano básico —emoji incluidos—, que era la última laguna.

La contrapartida del modelo es la de la clase 090: **si todo puede ser una cadena, cualquier valor
puede convertirse a texto y volver**, y esas conversiones cuestan. El *shimmering* aparece aquí
también, y `string is` sobre un valor que ya es un entero es más barato que sobre uno textual.
"""),
        "perl": ("""
use strict;
use warnings;

my $s = <STDIN>;
chomp $s;

print "invertido=", scalar reverse($s), "\\n";
""", """
**Lo que esta clase enseña en Perl.** `scalar reverse($s)` necesita el `scalar` por lo que ya se vio
en la clase 090: **`reverse` invierte la lista en contexto de lista y la cadena en contexto escalar**.
Sin él, se invertiría una lista de un solo elemento y saldría la cadena original.

Perl es el lenguaje de esta página construido **alrededor** del texto, y su aportación no son las
funciones de cadena —que las tiene todas— sino **las expresiones regulares integradas en la
sintaxis**:

```perl
$s =~ s/viejo/nuevo/g;             # sustituir
$s =~ tr/a-z/A-Z/;                  # transliterar, carácter a carácter
my @campos = split /\\s*,\\s*/, $s;   # dividir con un patrón
if ($s =~ /^(\\d{4})-(\\d{2})$/) { ... }   # capturar en $1, $2
```

Que `=~`, `s///` y `//` sean **operadores del lenguaje** y no llamadas a una biblioteca es lo que hizo
a Perl dominar el procesamiento de texto durante veinte años, y es lo que copió después todo el mundo:
la sintaxis de expresiones regulares de Python, Java, JavaScript, PHP, Ruby y .NET es **PCRE**, es
decir, *Perl Compatible Regular Expressions*.

Es probablemente la contribución más duradera de Perl a la informática, y sobrevive en lenguajes cuyos
usuarios no han escrito una línea de Perl.

Sobre Unicode, Perl tiene el modelo más explícito y también el más confuso: hay que declarar la
intención con `use utf8` para el código fuente y capas de entrada/salida para los datos.

```perl
use utf8;                              # el FUENTE está en UTF-8
binmode(STDOUT, ':encoding(UTF-8)');   # la SALIDA se codifica en UTF-8
```

Sin eso, Perl trata los datos como bytes. Es riguroso —distingue cadena de caracteres de cadena de
bytes, que es la distinción correcta— y exige entenderlo, a diferencia de Tcl, donde es automático.
"""),
        "cpp": ("""
#include <algorithm>
#include <iostream>
#include <string>

int main() {
    std::string s;
    if (!(std::cin >> s)) return 1;

    std::reverse(s.begin(), s.end());

    std::cout << "invertido=" << s << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** `std::reverse` no es una función de cadenas: es **un algoritmo
genérico que funciona sobre cualquier par de iteradores bidireccionales**. Sirve igual para un
`vector`, un `array`, un `deque` o una `string`, porque `std::string` es, a efectos de la STL, un
contenedor de caracteres.

Esa unificación es la misma idea que en Lisp y en Ada, con otra tecnología: en Lisp la da el tipo
`sequence`, en Ada el arreglo, en C++ el concepto de iterador.

`std::string` arregló el problema histórico de C —cadenas terminadas en `\\0`, sin longitud, con
`strcpy` como fuente inagotable de desbordamientos— y sus operaciones son las esperables:
`size()`, `substr()`, `find()`, `+`, `==`, `starts_with()` desde C++20.

Tres cosas que conviene saber y que no son evidentes:

**La optimización de cadena corta.** Casi todas las implementaciones guardan las cadenas de hasta 15
o 22 caracteres **dentro del propio objeto**, sin reservar memoria. Por eso `std::string` ocupa 32
bytes y no 8, y por eso las cadenas cortas son mucho más rápidas de lo que su interfaz sugiere.

**`std::string_view` (C++17)** es la pieza que faltaba: una **vista no propietaria** —puntero y
longitud— que evita copiar al pasar subcadenas.

```cpp
void procesar(std::string_view s);      // acepta string, const char*, literal: sin copiar
```

Con la trampa que le corresponde: **no prolonga la vida de lo que apunta**. Una `string_view` sobre
una `string` temporal queda colgando, y es un error frecuente.

**Y Unicode: `std::string` es una secuencia de bytes, no de caracteres.** `s.size()` sobre `"ñ"` en
UTF-8 devuelve 2, y `std::reverse` sobre texto no ASCII **rompe la codificación**. C++ sigue sin
soporte Unicode real en la biblioteca estándar en 2026, y la respuesta práctica es ICU o utf8cpp. Es
la carencia más señalada del lenguaje en este terreno, y la razón de que este programa se limite a
ASCII.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi CADENA;
  entrada char(200) const;
end-pi;

dcl-s s varchar(200);
dcl-s r varchar(200) inz('');
dcl-s i int(10);

s = %trimr(entrada);

for i = %len(s) downto 1;
  r += %subst(s : i : 1);
endfor;

dsply ('invertido=' + r);

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG comparte el modelo de COBOL —`char(n)` es siempre `n`
posiciones rellenas de espacios— y por eso `%trim`, `%trimr` y `%triml` aparecen por todas partes en
el código real.

La familia de funciones integradas cubre lo esperable, con el prefijo `%` que caracteriza al RPG
libre:

```rpgle
%subst(s : inicio : longitud)      // subcadena; TAMBIÉN a la izquierda del =
%scan('abc' : s)                    // buscar, devuelve posición o 0
%scanrpl('a' : 'A' : s)             // buscar y reemplazar (RPG 7.1)
%replace('X' : s : 3 : 1)           // sustituir en una posición
%len(s)  %trim(s)  %char(n)  %int(s)  %upper(s)  %lower(s)
%split(s : ' ')                     // dividir en una lista (RPG 7.5, 2022)
```

Dos de esas merecen atención.

**`%subst` funciona como destino de asignación**, no solo como fuente:

```rpgle
%subst(fecha : 5 : 2) = '12';       // escribir EN una posición concreta
```

Es la reference modification de COBOL y el `set $piece` de M: modificar una porción de la cadena en el
sitio, sin reconstruirla.

**Y `%split`, de 2022**, es un ejemplo perfecto de lo que documenta esta sección: un lenguaje de 1959
que en 2022 incorpora la división de cadenas en una lista porque el trabajo real —consumir APIs,
procesar JSON— lo pide.

En la misma línea, RPG 7.2+ añadió `DATA-INTO` y `DATA-GEN`, que **analizan y generan JSON y XML
directamente hacia una estructura de datos**, sin escribir el analizador. Eso, en un lenguaje cuyo
tipo de cadena sigue siendo de longitud fija por defecto, dice bastante de cómo se están modernizando
estas plataformas.
"""),
        "pli": ("""
 cadena: procedure options(main);

    declare s char(200) varying;
    declare r char(200) varying initial('');
    declare i fixed binary(31);

    get edit (s) (a(200));
    s = trim(s);

    do i = length(s) to 1 by -1;
       r = r || substr(s, i, 1);
    end;

    put skip list ('invertido=' || r);

 end cadena;
""", """
**Lo que esta clase enseña en PL/I.** PL/I fue **el primer lenguaje mayoritario con cadenas de
longitud variable**, con el atributo **`varying`**, en 1964.

```pli
declare fijo   char(20);           /* siempre 20, rellenado con espacios */
declare varia  char(20) varying;    /* hasta 20, con longitud REAL guardada */
declare libre  char(20) varyingz;   /* variante terminada en nulo, para C */
```

Una `varying` guarda un prefijo de dos bytes con la longitud actual — exactamente el mismo diseño que
la `ShortString` de Turbo Pascal veinte años después, y que el `varchar` de RPG y de SQL. El `VARCHAR`
de todas las bases de datos del mundo desciende de aquí.

Y PL/I trae una batería de funciones de cadena que en 1964 no tenía nadie:

```pli
substr(s, i, n)      index(s, 'abc')     length(s)     trim(s)
translate(s, 'ABC', 'abc')               verify(s, '0123456789')
repeat('ab', 3)      reverse(s)          string(estructura)
```

**`verify`** es la joya olvidada: devuelve la posición del primer carácter **que NO está** en el
conjunto dado, y con eso se valida un campo entero sin bucle.

```pli
 if verify(codigo, '0123456789') ^= 0 then ...   /* hay algo que no es dígito */
```

Es una operación de conjuntos sobre caracteres, resuelta por el compilador, y sigue sin tener
equivalente directo en la mayoría de los lenguajes del núcleo.

**Y `substr` funciona como pseudovariable**, es decir, a la izquierda del signo igual:

```pli
 substr(fecha, 5, 2) = '12';
```

Ese patrón —modificar un trozo de cadena en el sitio— lo comparten PL/I, COBOL, RPG y M, y es
consecuencia directa del modelo de datos posicional que los cuatro comparten.
"""),
        "mumps": ("""
CADENA ; Cadenas -- clase 093
 read s
 set r = ""
 for i=$length(s):-1:1 set r = r _ $extract(s, i)
 write "invertido=", r, !
 quit
""", """
**Lo que esta clase enseña en M.** En M **todo es una cadena**, como en Tcl, y por la misma razón
histórica: el lenguaje se diseñó para manipular texto médico en máquinas pequeñas.

No hay tipos, así que `1 + "2"` vale 3 y `"abc" + 1` vale 1 —M convierte el prefijo numérico, o 0 si
no hay— sin ningún error. Es la conversión más permisiva de esta página.

Las funciones de cadena de M son pocas y están extraordinariamente bien elegidas:

```mumps
 $extract(s, i, j)         ; subcadena por POSICIÓN
 $length(s)                 ; longitud
 $length(s, ",")            ; número de PIEZAS con ese delimitador
 $piece(s, ",", n)          ; la pieza n
 $find(s, "abc")            ; buscar
 $translate(s, "abc", "ABC"); traducir carácter a carácter
 $justify(s, 10)            ; alinear
 $reverse(s)                 ; invertir
```

Las dos que definen el lenguaje son **`$piece` y `$extract`**, y **las dos funcionan como
pseudovariables**:

```mumps
 set $extract(s, 3) = "x"          ; cambiar el tercer carácter
 set $piece(s, "^", 4) = "nuevo"   ; cambiar la cuarta pieza
```

Poder asignar a `$piece` es lo que hace viable el modelo de datos de VistA (clase 090): un registro es
una cadena con piezas, y actualizar un campo es una sola sentencia sobre el *global*, sin leer,
descomponer, modificar y recomponer.

```mumps
 set $piece(^PAC(id, 0), "^", 3) = "M"
```

Esa línea actualiza un campo de un registro en disco, dentro de una transacción, sin SQL y sin capa de
persistencia. Es fea, es frágil ante cambios de esquema y es **muy rápida** — y es exactamente por lo
que M sigue moviendo los historiales clínicos de decenas de millones de personas.
"""),
        "smalltalk": ("""
| s |

s := stdin nextLine trimBoth.

Transcript show: 'invertido=', s reversed; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** `String` es una subclase de `ArrayedCollection`, así que
—como en Lisp, Ada y C++— **una cadena es una colección**, y responde a todo el protocolo de la clase
089.

```smalltalk
'hola' reversed                        "aloh"
'hola' size                             "4"
'hola' asUppercase
'hola mundo' substrings: ' '
'hola' , ' mundo'                       "la coma es CONCATENAR"
('hola' collect: [ :c | c asUppercase ])   "map sobre caracteres"
('hola' select: [ :c | c isVowel ])         "filter: 'oa'"
```

Que `select:` y `collect:` funcionen sobre una cadena y devuelvan una cadena es la regla *species* de
la clase 090 en acción.

Y Smalltalk tiene una distinción que ningún otro lenguaje de esta página hace de forma tan explícita:
**`String` frente a `Symbol`**.

```smalltalk
'hola' == 'hola'      "false: son DOS objetos distintos con el mismo contenido"
#hola  == #hola       "true: un símbolo es ÚNICO en el sistema"
```

Un `Symbol` está **internado**: solo existe uno por cada texto, así que comparar dos símbolos es
comparar punteros, en tiempo constante. Por eso los nombres de mensaje son símbolos (clase 085), y por
eso las claves de un diccionario suelen serlo.

Es la misma idea que los símbolos de Lisp, los átomos de Erlang y los `Symbol` de Ruby, y viene del
mismo sitio.

Las cadenas de Smalltalk son **mutables** —`s at: 1 put: $H`— lo que las diferencia de Java y Python,
y para construir texto por trozos lo idiomático es `WriteStream`:

```smalltalk
String streamContents: [ :flujo |
    coleccion do: [ :cada | flujo print: cada ] separatedBy: [ flujo nextPut: $- ] ]
```

`do:separatedBy:` resuelve en un mensaje el problema del separador que no va al final — el mismo que
en Lisp resuelve `~^` y en el resto de lenguajes obliga a un `if` dentro del bucle.
"""),
    },
)
