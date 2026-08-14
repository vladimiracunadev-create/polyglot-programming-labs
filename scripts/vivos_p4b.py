# -*- coding: utf-8 -*-
"""Parte 4, lote B — clases 063 a 068. Ver `vivos_parte4.py` y `gen_vivos.py`.

El código de los ocho lenguajes de la sección 🟢 se ejecuta en CI contra el
`casos.json` de la clase (`scripts/verificar_vivos.py`).
"""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 063 — Iteración por condición: while y do-while
# ---------------------------------------------------------------------------
SPECS["063"] = dict(
    gancho="""
Sumar de 1 a *n* con un bucle que pregunta antes de cada vuelta. El `while` es la forma más básica de
repetir, y la pregunta que reparte a estos lenguajes es cuántas variantes ofrecen: **¿se puede
comprobar la condición al final en vez de al principio? ¿se puede repetir un número fijo de veces sin
llevar contador? ¿se puede salir por el medio?**
""",
    porque="""
Aquí el concepto es la **iteración gobernada por una condición**, y estos lenguajes lo enseñan porque
tienen construcciones que el núcleo perdió por el camino. COBOL tiene un `PERFORM` que hace **seis
cosas distintas** según cómo se escriba, incluida la ejecución de un párrafo remoto *n* veces. Ada
tiene un `loop` desnudo con `exit when`, que es el bucle de salida por el medio sin `break`. Y
Smalltalk no tiene bucle en absoluto: **`whileTrue:` es un método del bloque**.

Y M enseña la versión extrema: un `for` **sin argumentos** es un bucle infinito, y se sale con un
`quit` postcondicional.
""",
    cierre="""
Lo transferible es la distinción entre **comprobar antes** y **comprobar después**: `while` puede no
ejecutar el cuerpo ni una vez, y `repeat/until`, `do-while` o `PERFORM WITH TEST AFTER` lo ejecutan
siempre al menos una. Y ojo con el sentido de la condición, que es donde todo el mundo se equivoca al
cambiar de lenguaje: el `until` de Pascal y el `UNTIL` de COBOL dicen **cuándo parar**, mientras que
el `while` de C y el `dow` de RPG dicen **cuándo seguir**. La misma palabra en dos lenguajes puede
significar lo contrario.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. SUMA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC 9(9)  COMP-3.
01  I       PIC 9(9)  COMP-3.
01  TOTAL   PIC 9(18) COMP-3.
01  ED-T    PIC Z(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N
    MOVE 0 TO TOTAL
    MOVE 1 TO I

    PERFORM UNTIL I > N
        ADD I TO TOTAL
        ADD 1 TO I
    END-PERFORM

    MOVE TOTAL TO ED-T
    DISPLAY "suma=" FUNCTION TRIM(ED-T)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** **La condición de `PERFORM` es `UNTIL`, no `WHILE`: dice
cuándo PARAR, no cuándo seguir.** Es el error número uno de quien llega desde C, y produce bucles
infinitos o bucles que no entran nunca.

Y `PERFORM` es, con diferencia, la construcción más versátil del lenguaje. Hace seis cosas distintas
según cómo se escriba:

```cobol
PERFORM PARRAFO                            *> 1. ejecuta un párrafo y vuelve
PERFORM PARRAFO 10 TIMES                   *> 2. lo ejecuta 10 veces
PERFORM PARRAFO UNTIL FIN-FICHERO          *> 3. hasta que se cumpla
PERFORM PARRAFO VARYING I FROM 1 BY 1 UNTIL I > 100
PERFORM UNTIL FIN ... END-PERFORM          *> 5. en línea, sin párrafo
PERFORM PARRAFO-A THRU PARRAFO-Z           *> 6. un RANGO de párrafos
```

Las formas 1 a 4 son **fuera de línea**: el cuerpo está en otro sitio del programa. Eso hace que el
código antiguo se lea saltando de párrafo en párrafo, y es la razón de que COBOL-85 añadiera la forma
5, **en línea**, que es la que se usa hoy y la que aparece en este programa.

La forma 6, `THRU`, es la peligrosa: ejecuta todos los párrafos entre dos etiquetas, así que
**insertar un párrafo nuevo en medio cambia el comportamiento de un `PERFORM` que está en otro
sitio**. Está desaconsejada en todas las guías modernas y sigue apareciendo en código de los 70.

Y la variante de prueba posterior existe: `PERFORM WITH TEST AFTER UNTIL ...` es el `do-while`.
"""),
        "fortran": ("""
program suma
   implicit none
   integer :: n, i, total

   read(*, *) n

   total = 0
   i = 1
   do while (i <= n)
      total = total + i
      i = i + 1
   end do

   write(*, '(A,I0)') 'suma=', total
end program suma
""", """
**Lo que esta clase enseña en Fortran.** `do while` llegó con **Fortran 77** y antes no existía: los
bucles condicionales se escribían con `IF` y `GO TO`.

```fortran
   10 IF (I .GT. N) GO TO 20
      TOTAL = TOTAL + I
      I = I + 1
      GO TO 10
   20 CONTINUE
```

Ese patrón —comprobar, saltar al final, y saltar atrás— es literalmente lo que el compilador genera
hoy para un `while`. Verlo escrito a mano explica por qué la programación estructurada se sintió como
una liberación.

Fortran moderno añadió además el bucle **sin condición** con salida por el medio, que es el más
flexible:

```fortran
do
   read(unidad, *, iostat=ios) valor
   if (ios /= 0) exit          ! sale del bucle
   if (valor < 0) cycle        ! salta a la siguiente vuelta
   total = total + valor
end do
```

`exit` y `cycle` son el `break` y el `continue` de la clase 070, y con nombres de construcción
—`exterior: do ... end do exterior`— pueden salir de un bucle **anidado concreto**, que en C exige un
`goto`.

Y hay una forma que hoy es la importante y que no es un bucle condicional: **`do concurrent`**, en la
que el programador **garantiza** que las iteraciones son independientes, y el compilador puede
vectorizarlas o mandarlas a la GPU. Es la razón de que Fortran siga siendo competitivo.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Suma is
   N, I, Total : Integer;
begin
   Get (N);

   Total := 0;
   I := 1;
   while I <= N loop
      Total := Total + I;
      I := I + 1;
   end loop;

   Put ("suma="); Put (Total, Width => 1); New_Line;
end Suma;
""", """
**Lo que esta clase enseña en Ada.** Ada tiene **una sola palabra para todos los bucles** —`loop`— y
las variantes se construyen poniéndole algo delante:

```ada
loop ... end loop;                          --  infinito
while C loop ... end loop;                  --  condición al principio
for I in 1 .. 10 loop ... end loop;         --  rango
for E of Coleccion loop ... end loop;       --  cada elemento (Ada 2012)
```

Esa uniformidad tiene una consecuencia práctica: **el bucle sin condición no es un caso raro, es el
caso base**, y con `exit when` da la forma que en C hay que simular con `while (true)` y `break`:

```ada
loop
   Leer (Dato);
   exit when Fin_De_Fichero;      --  la condición está DONDE se comprueba
   Procesar (Dato);
end loop;
```

Ese patrón —el bucle "y medio", donde la condición no está ni al principio ni al final sino en
medio— es extremadamente común al leer ficheros, y Ada lo expresa directamente. En Pascal, que no
tiene `break` en el ISO, hay que duplicar la lectura antes del bucle.

Y los bucles se pueden **nombrar**, lo que permite salir de uno exterior desde dentro de otro:

```ada
Exterior : loop
   for I in 1 .. N loop
      exit Exterior when Encontrado;    --  sale de los DOS
   end loop;
end loop Exterior;
```

Es el mismo mecanismo que las etiquetas de Java y el `'label` de Rust, y evita la bandera booleana o
el `goto` que C necesita.
"""),
        "pascal": ("""
program Suma;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N, I, Total: Integer;

begin
  Read(N);

  Total := 0;
  I := 1;
  while I <= N do
  begin
    Total := Total + I;
    Inc(I);
  end;

  WriteLn('suma=', IntToStr(Total));
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal tiene los **dos** bucles condicionales, y la diferencia
entre ellos es exactamente el tema de esta clase:

```pascal
while C do begin ... end;      { comprueba ANTES: puede no entrar nunca }
repeat ... until C;            { comprueba DESPUÉS: entra siempre al menos una vez }
```

Y hay dos detalles que conviene fijar. El primero: **`repeat`/`until` no necesita `begin`/`end`**,
porque `repeat` y `until` ya delimitan el bloque. Es la única construcción de Pascal con esa
propiedad, y por eso `while` lleva `begin`/`end` y `repeat` no.

El segundo, y es el que causa errores al cambiar de lenguaje: **`until` dice cuándo parar**, igual que
el `UNTIL` de COBOL y al revés que el `while` de C. `repeat ... until I > N` es `do ... while (i <=
n)`. La condición está **negada** respecto a la que escribirías en C.

`Inc(I)` en lugar de `I := I + 1` es la forma idiomática, y también existe `Dec`. No son operadores
—Pascal no tiene `++`— sino procedimientos incorporados que el compilador convierte en una sola
instrucción. `Inc(I, 5)` incrementa de cinco en cinco.

Y una advertencia sobre el bucle `for`, que aparece en la clase siguiente: **en Pascal la variable de
control no se puede modificar dentro del cuerpo** y su valor **al salir es indefinido** según el
estándar. Free Pascal avisa si intentas lo primero.
"""),
        "lisp": ("""
(let ((n (read))
      (total 0)
      (i 1))
  (loop while (<= i n) do
    (incf total i)
    (incf i))
  (format t "suma=~D~%" total))
""", """
**Lo que esta clase enseña en Common Lisp.** `loop` es, de largo, **la macro más grande del
estándar**: un lenguaje de iteración completo, con su propia sintaxis casi en inglés, incrustado
dentro de Lisp.

```lisp
(loop while (< i n) do ...)
(loop until (>= i n) do ...)
(loop for i from 1 to 10 by 2 collect (* i i))
(loop for x in lista when (evenp x) sum x)
(loop for (clave valor) on plist by #'cddr do ...)
(loop for linea = (read-line f nil) while linea count t)
(loop repeat 5 do ...)
```

Fíjate en que **no lleva paréntesis alrededor de cada cláusula**: `for i from 1 to 10` son cuatro
símbolos sueltos. Eso rompe la uniformidad de las s-expresiones que la clase 041 presentaba como el
rasgo definitorio del lenguaje, y es la razón de que `loop` sea la construcción **más discutida** de
Common Lisp: unos la consideran indispensable y otros, una traición al diseño.

Quien está en el segundo bando usa `do`, que sí es homogéneo, o `iterate`, una biblioteca alternativa
con sintaxis en paréntesis. Y para los casos simples están `dotimes` y `dolist`.

Lo interesante para esta clase es lo que demuestra: **`loop` es una macro escrita en Lisp**, no una
construcción del compilador. Alguien implementó un lenguaje de iteración entero como biblioteca. Es la
prueba más contundente de para qué sirven las macros de la clase 041 — cuando un lenguaje permite
extender su sintaxis, la discusión sobre qué construcciones debe tener el núcleo cambia de naturaleza.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

set total 0
set i 1
while {$i <= $n} {
    incr total $i
    incr i
}

puts "suma=$total"
""", """
**Lo que esta clase enseña en Tcl.** `while` es **un comando** que recibe dos argumentos: la condición
y el cuerpo, ambos como cadenas. Y eso explica la regla más importante del rendimiento en Tcl:

```tcl
while {$i <= $n} { ... }      ;# LLAVES: la condición se compila UNA vez
while "$i <= $n" { ... }      ;# comillas: se sustituye antes -> ¡bucle infinito!
```

Con comillas, `$i` se sustituye **una sola vez, antes de entrar**, así que la condición queda
congelada con el valor inicial y el bucle nunca termina. Es el error clásico, y es el mismo motivo de
las llaves de `expr` de las clases 041 y 055 — cuarta razón para la misma regla.

`incr total $i` es la forma idiomática de acumular: `incr` con dos argumentos suma el segundo. Es más
rápido que `set total [expr {$total + $i}]` porque está especializado para enteros.

Y Tcl tiene una forma de iteración que casi nadie más ofrece, y que conviene conocer aunque no
aparezca aquí: **`time`**, que ejecuta un cuerpo *n* veces y devuelve el tiempo medio por
iteración.

```tcl
puts [time { set x [expr {$a * $b}] } 10000]    ;# "0.34 microseconds per iteration"
```

Medir es un comando del lenguaje, no una biblioteca. En un lenguaje pensado para conducir
herramientas de ingeniería, tiene sentido.
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

my $total = 0;
my $i = 1;
while ($i <= $n) {
    $total += $i;
    $i++;
}

print "suma=$total\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl tiene **cuatro formas** de escribir este bucle, y todas se
usan:

```perl
while ($i <= $n) { ... }            # condición al principio
until ($i > $n)  { ... }            # la negación, con nombre propio
do { ... } while ($i <= $n);        # condición al final
$total += $_ for 1 .. $n;           # modificador: sin bucle explícito
```

`until` existe por la misma razón que `unless`: **evitar la doble negación**, que cuesta leer. Es una
decisión lingüística, no técnica.

Y hay una trampa que conviene conocer, porque sorprende: **`do { } while` no es un bucle de verdad**.
`do BLOQUE` es una expresión, y el `while` de detrás es un **modificador de sentencia**. La
consecuencia práctica es que **`last`, `next` y `redo` no funcionan dentro**:

```perl
do {
    next if $x;      # ERROR: "Can't 'next' outside a loop block"
} while ($c);
```

Para tener un `do-while` con control de flujo hay que envolverlo en un bloque desnudo, que en Perl
**sí es un bucle que se ejecuta una vez**:

```perl
LOOP: { do { ... last LOOP if $x; ... } while ($c); }
```

Ese detalle —que un bloque `{ }` suelto en Perl cuenta como bucle de una sola vuelta, y por tanto
admite `last`— es de las rarezas más útiles del lenguaje: permite usar `last` como una salida
temprana de un bloque cualquiera.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    long long total = 0;
    int i = 1;
    while (i <= n) {
        total += i;
        ++i;
    }

    std::cout << "suma=" << total << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** `++i` en lugar de `i++` no es una manía: con un `int` el
compilador genera lo mismo, pero con un **iterador** o un objeto con operador sobrecargado, `i++` debe
**devolver una copia del valor anterior**, así que construye un objeto temporal que se descarta. La
guía es preincrementar siempre salvo que necesites el valor previo.

Y `long long total` frente a `int i` es deliberado: la suma de 1 a *n* crece mucho más rápido que
*n*. Con `int`, el desbordamiento de un entero con signo es **comportamiento indefinido** en C++, no
un valor grande y raro — el compilador puede asumir que no ocurre y optimizar en consecuencia.

C++ tiene una peculiaridad en esta clase que casi ningún lenguaje comparte: **se puede declarar la
variable en la condición del `while`**.

```cpp
while (const auto linea = leer_siguiente()) { ... }   // termina cuando sea "falsa"
while (std::getline(std::cin, linea)) { ... }         // el idioma habitual
```

La segunda línea es el patrón canónico de lectura: `getline` devuelve el flujo, el flujo se convierte
a `bool`, y el bucle termina en el fin de fichero. Compara con el `read(unidad, iostat=ios)` de
Fortran o el `<STDIN>` de Perl: **cada lenguaje tiene su forma de decir "sigue mientras haya
datos"**, y reconocerla es lo primero que hay que buscar en un lenguaje nuevo.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi SUMA;
  n int(10) const;
end-pi;

dcl-s i      int(10) inz(1);
dcl-s total  int(20) inz(0);
dcl-s salida char(40);

dow i <= n;
  total += i;
  i += 1;
enddo;

salida = 'suma=' + %char(total);
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG tiene los dos bucles condicionales con nombres que dicen
exactamente lo que hacen: **`dow`** (*do while*, mientras se cumpla) y **`dou`** (*do until*, hasta
que se cumpla, comprobando al final). Junto a `for`, cubren las tres formas.

Pero lo interesante de RPG en esta clase es lo que ya no hace falta escribir. En el RPG clásico, **el
bucle principal de un programa por lotes no se escribía**: lo ponía el **ciclo del programa**.

```text
     FCLIENTES  IP   E             DISK        <- fichero de ENTRADA PRIMARIA
```

Esa `IP` —*input primary*— le decía al runtime: lee un registro, ejecuta la lógica de detalle,
comprueba los cambios de nivel de control, imprime totales, y vuelve a empezar. **El programador solo
escribía qué hacer con cada registro.**

Es inversión de control, exactamente la misma idea que hoy tienen un manejador de eventos, un
*framework* web o un `map` sobre un flujo: **tú no llamas al bucle, el bucle te llama a ti**. Y estaba
en un lenguaje de 1959.

El RPG moderno prescinde del ciclo —de ahí `dftactgrp(*no)` y `main()`— y escribe sus bucles a mano.
Pero millones de líneas en producción siguen dependiendo de él, y entender un programa RPG antiguo
exige saber que hay un bucle que no está escrito en ninguna parte.
"""),
        "pli": ("""
 suma: procedure options(main);

    declare n     fixed binary(31);
    declare i     fixed binary(31);
    declare total fixed binary(31) initial(0);

    get list (n);

    i = 1;
    do while (i <= n);
       total = total + i;
       i = i + 1;
    end;

    put skip list ('suma=' || trim(char(total)));

 end suma;
""", """
**Lo que esta clase enseña en PL/I.** `do` en PL/I es **una sola palabra que cubre todas las formas de
iteración y además el bloque simple**, y la lista de variantes es notable:

```pli
do;                          /* solo agrupa; no itera */
do while (c);                /* condición al principio */
do until (c);                /* condición al final */
do i = 1 to 10;              /* rango */
do i = 1 to 10 by 2 while (c);        /* rango Y condición a la vez */
do i = 1 to 5, 10 to 15, 20;          /* VARIAS especificaciones */
do i = 1 repeat i * 2 while (i < 1000);  /* progresión arbitraria */
```

Las tres últimas no tienen equivalente en ningún lenguaje del núcleo. `do i = 1 to 5, 10 to 15, 20`
recorre tres tramos discontinuos en un solo bucle. Y `repeat` define **cómo se calcula el siguiente
valor** —aquí, duplicando—, lo que permite progresiones geométricas sin aritmética dentro del cuerpo.

Es un buen ejemplo del patrón que recorre toda esta sección sobre PL/I: **cada característica por
separado es razonable y útil, y el conjunto es difícil de conocer entero**. Un programador que domine
`do` de PL/I escribe bucles más expresivos que en casi cualquier lenguaje moderno; uno que no lo
domine no entiende el código del primero.
"""),
        "mumps": ("""
SUMA ; Suma 1..n -- clase 063
 read n
 set total = 0
 set i = 1
 for  quit:i>n  set total = total + i, i = i + 1
 write "suma=", total, !
 quit
""", """
**Lo que esta clase enseña en M.** Fíjate en `for  quit:i>n  set ...` y en los **dos espacios** tras
`for`. No son un descuido de formato: **un `for` sin argumentos es un bucle infinito**, y el espacio
doble es lo que marca que no lleva argumentos. Un espacio de más o de menos cambia el significado del
programa.

Esa es la construcción de bucle condicional de M: **un bucle infinito más un `quit` postcondicional**.
No hay `while`. Y como el `quit` puede ir en cualquier punto del cuerpo, cubre de un golpe el `while`,
el `do-while` y el bucle "y medio" que Ada resuelve con `exit when`.

```mumps
 for  quit:i>n  do algo          ; while
 for  do algo quit:i>n           ; do-while: el quit va DESPUÉS
 for  read x quit:x=""  do algo  ; bucle y medio: leer, salir, procesar
```

M tiene además el `for` con rango, con la sintaxis de dos puntos: `for i=1:1:n` es "desde 1, de 1 en
1, hasta n", y `for i=1:1` sin límite es infinito ascendente. Y admite **varias especificaciones
separadas por comas**, como PL/I: `for i=1:1:5,10,20:5:40`.

Y la que no tiene equivalente: **`for i=""` combinado con `$order`**, que es cómo se recorre un árbol
de la base de datos. Se verá en la clase 065.
"""),
        "smalltalk": ("""
| n total i |

n := stdin nextLine trimBoth asNumber.

total := 0.
i := 1.
[ i <= n ] whileTrue: [
    total := total + i.
    i := i + 1 ].

Transcript show: 'suma=', total printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** **`whileTrue:` no es una palabra clave: es un método de la
clase `BlockClosure`.** El receptor es el bloque de la condición y el argumento es el bloque del
cuerpo:

```smalltalk
BlockClosure >> whileTrue: unBloque
    ^ self value
        ifTrue: [ unBloque value. self whileTrue: unBloque ]
        ifFalse: [ nil ]
```

Es decir: **el bucle está implementado por recursión sobre el envío de mensajes**, sin ninguna
construcción de iteración en el lenguaje. Puedes abrirlo en el navegador y leerlo.

Eso plantea una pregunta legítima —¿no desborda la pila con un millón de vueltas?— y la respuesta es
la parte interesante: **el compilador de Smalltalk trata `whileTrue:`, `ifTrue:`, `and:` y `to:do:`
como casos especiales** y los compila **en línea**, generando saltos en el bytecode en lugar de
envíos de mensajes reales. La semántica es la del método; el código generado es el de un bucle.

Es un compromiso muy elegante: **la definición conceptual sigue siendo un mensaje** —y por tanto
puedes definir tus propias estructuras de control con bloques—, y el coste es el de un bucle
tradicional en los casos habituales.

La familia completa es `whileTrue:`, `whileFalse:`, `whileTrue`, `whileFalse` (sin argumento, con la
condición y el cuerpo en el mismo bloque) y `repeat`, que es el bucle infinito.
"""),
    },
)

# ---------------------------------------------------------------------------
# 064 — Iteración por rango: for clásico y for-range
# ---------------------------------------------------------------------------
SPECS["064"] = dict(
    gancho="""
El factorial: multiplicar todos los enteros de 1 a *n*. Un bucle de rango puro, elegido porque además
desborda enseguida —`20!` ya son diecinueve dígitos— y eso separa a los lenguajes en dos grupos: los
que fallan en silencio al pasarse y los que **simplemente siguen contando**.
""",
    porque="""
Aquí el concepto es el **bucle sobre un rango conocido**, y estos lenguajes aportan dos cosas. La
primera es la **variable de control y su ámbito**: en Ada es una **constante que solo existe dentro
del bucle** y no hace falta declararla, mientras que en C es una variable normal que se puede
modificar dentro del cuerpo. Pascal prohíbe modificarla y deja su valor final **indefinido** al
salir.

La segunda es el desbordamiento: `20!` cabe en 64 bits por poco, y `21!` ya no. **Lisp, Smalltalk y
Tcl no desbordan nunca**; COBOL, RPG y PL/I tienen decimales de decenas de dígitos; y C++, Fortran,
Ada y Pascal se quedan sin sitio.
""",
    cierre="""
La regla que deja esta clase: **antes de escribir un bucle de acumulación, pregúntate cuánto puede
crecer el acumulador**. Es la misma comprobación que en la clase 044 con las bases, y aquí es más
urgente porque un producto crece factorialmente. Y la segunda: **no toques la variable de control
dentro del cuerpo**. Ada y Pascal lo prohíben; C, Fortran y Tcl lo permiten, y hacerlo produce bucles
que ningún lector espera.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. FACTORIAL.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC 9(4)  COMP-3.
01  I       PIC 9(4)  COMP-3.
01  F       PIC 9(20) COMP-3.
01  ED-F    PIC Z(19)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N
    MOVE 1 TO F

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        COMPUTE F = F * I
    END-PERFORM

    MOVE F TO ED-F
    DISPLAY "factorial=" FUNCTION TRIM(ED-F)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** `PERFORM VARYING I FROM 1 BY 1 UNTIL I > N` es el bucle de
rango, y su sintaxis dice **las tres cosas por separado**: de dónde parte, cuánto avanza y cuándo
para. El `BY` admite negativos —`BY -1`— para contar hacia atrás.

Y `PIC 9(20)` es la razón de que COBOL esté cómodo aquí: **veinte dígitos decimales**, así que `20!`
—que son 2 432 902 008 176 640 000, diecinueve dígitos— cabe sin problema. En C++, Ada, Fortran y
Pascal hay que usar el entero de 64 bits y `21!` ya desborda; aquí basta con declarar más dígitos.
El estándar llega a 31 y GnuCOBOL admite más.

`PERFORM VARYING` tiene además una forma anidada que no tiene equivalente directo en el núcleo:

```cobol
PERFORM VARYING I FROM 1 BY 1 UNTIL I > 10
    AFTER J FROM 1 BY 1 UNTIL J > 10
    AFTER K FROM 1 BY 1 UNTIL K > 10
        COMPUTE CUBO(I, J, K) = I * J * K
END-PERFORM
```

**Tres bucles anidados en una sola sentencia**, con `AFTER`. El orden de anidamiento es el de
escritura, y el compilador genera los bucles. Es la forma natural de recorrer una tabla
multidimensional, que en COBOL es el caso frecuente.
"""),
        "fortran": ("""
program factorial
   implicit none
   integer :: n, i
   integer(kind=8) :: f

   read(*, *) n

   f = 1
   do i = 1, n
      f = f * i
   end do

   write(*, '(A,I0)') 'factorial=', f
end program factorial
""", """
**Lo que esta clase enseña en Fortran.** `do i = 1, n` es el bucle más antiguo que sigue vivo:
apareció en el FORTRAN de 1957 y su sintaxis no ha cambiado. La forma completa es
`do i = inicio, fin, paso`, con el paso opcional y admitiendo negativos.

Y tiene una propiedad que conviene conocer: **el número de vueltas se calcula ANTES de empezar**, con
la fórmula `max(0, (fin - inicio + paso) / paso)`. Eso significa que modificar `n` dentro del cuerpo
**no afecta al bucle**, al contrario que en C. Es un requisito para poder vectorizar: el compilador
necesita saber cuántas iteraciones habrá.

De ahí también que `do i = 1, 0` no se ejecute ninguna vez —lo que hace que este programa dé `1` para
`n = 0`, como pide el contrato— sin ninguna comprobación especial.

El Fortran clásico escribía el bucle con una etiqueta de cierre, y aún se ve en código antiguo:

```fortran
      DO 100 I = 1, N
         F = F * I
  100 CONTINUE
```

Peor aún: **varios bucles podían compartir la misma etiqueta de cierre**, lo que producía anidamientos
imposibles de seguir. `end do` llegó con Fortran 90 y esa forma quedó obsolescente.

Sobre el desbordamiento: `integer(kind=8)` llega hasta `20!` justo. `21!` desborda **en silencio**,
salvo que se compile con `-ftrapv` o `-fcheck=all`.
"""),
        "ada": ("""
with Ada.Text_IO;                   use Ada.Text_IO;
with Ada.Integer_Text_IO;           use Ada.Integer_Text_IO;
with Ada.Long_Long_Integer_Text_IO; use Ada.Long_Long_Integer_Text_IO;

procedure Factorial is
   N : Integer;
   F : Long_Long_Integer := 1;
begin
   Get (N);

   --  I no se declara: el bucle la crea, y es CONSTANTE dentro del cuerpo.
   for I in 1 .. N loop
      F := F * Long_Long_Integer (I);
   end loop;

   Put ("factorial="); Put (F, Width => 1); New_Line;
end Factorial;
""", """
**Lo que esta clase enseña en Ada.** **`I` no está declarada en ninguna parte, y no se puede
modificar.** El bucle `for` de Ada crea su propia variable de control, deduce su tipo del rango, la
hace **constante** dentro del cuerpo y la destruye al salir.

Eso elimina tres errores de un golpe:

```ada
for I in 1 .. N loop
   I := I + 1;        --  NO COMPILA: I es constante
end loop;
Put (I);              --  NO COMPILA: I no existe fuera del bucle
```

En C las tres cosas son legales, y modificar el contador dentro del cuerpo es una fuente clásica de
bucles que nadie entiende.

Si `N` es 0, el rango `1 .. 0` está **vacío** y el bucle no se ejecuta: por eso este programa da `1`
sin ninguna comprobación. Y `for I in reverse 1 .. N loop` recorre al revés, sin tocar los límites.

Ada 2012 añadió además el bucle **sobre contenedores**, con dos formas que se distinguen por una
palabra:

```ada
for I of Coleccion loop ... end loop;    --  el ELEMENTO
for C in Coleccion loop ... end loop;    --  el CURSOR (posición)
```

`of` da el valor, `in` da la posición. Es la misma distinción que `for x in v` frente a
`for i in 0..v.len()` en Rust, y tenerla en la sintaxis evita la confusión que en C++ se resuelve con
iteradores.
"""),
        "pascal": ("""
program Factorial;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N, I: Integer;
  F: Int64;

begin
  Read(N);

  F := 1;
  for I := 1 to N do
    F := F * I;

  WriteLn('factorial=', IntToStr(F));
end.
""", """
**Lo que esta clase enseña en Pascal.** El `for` de Pascal es **deliberadamente rígido**, y sus
restricciones son las mismas que Ada adoptaría después:

- El paso es **siempre 1**: `to` sube de uno en uno, `downto` baja de uno en uno. **No hay `by`.**
  Para otro incremento hay que usar `while`.
- La variable de control **no se puede modificar dentro del cuerpo** — Free Pascal da error.
- Su valor **al salir del bucle es indefinido** según el estándar, así que no se puede usar después.
- Los límites se evalúan **una sola vez, al empezar**, igual que en Fortran.

Wirth eliminó el paso arbitrario a propósito: un `for` con paso variable y contador modificable no es
un bucle de rango, es un `while` disfrazado, y prefirió que se escribiera como tal.

Para recorrer colecciones, Free Pascal y Delphi añadieron `for..in`:

```pascal
for Elemento in Coleccion do ...
for C in 'hola' do ...              { carácter a carácter }
for I in [1..10] do ...             { sobre un CONJUNTO }
```

Y sobre el desbordamiento: `Int64` llega justo a `20!`. Free Pascal tiene la directiva `{$Q+}` que
**comprueba el desbordamiento aritmético en ejecución** y lanza una excepción — desactivada por
defecto, y de las que conviene activar en desarrollo, junto con `{$R+}` para los rangos.
"""),
        "lisp": ("""
(let ((n (read))
      (f 1))
  (loop for i from 1 to n do (setf f (* f i)))
  (format t "factorial=~D~%" f))
""", """
**Lo que esta clase enseña en Common Lisp.** **En Lisp el factorial no desborda nunca.** `(loop for i
from 1 to 100 do ...)` calcula `100!` completo —158 dígitos— sin ninguna precaución, porque los
enteros crecen mientras quepan en memoria.

Compara con este mismo programa en C++, Ada, Fortran o Pascal, donde `21!` ya no cabe. Aquí el
problema de esta clase sencillamente no existe.

`loop for i from 1 to n` es la forma de rango de la macro `loop`, y admite `by`, `downto`, `below` y
`above`:

```lisp
(loop for i from 1 to 10 by 2 ...)      ; 1 3 5 7 9
(loop for i from 10 downto 1 ...)
(loop for i from 0 below n ...)         ; sin incluir n: como range(n) de Python
(loop repeat 5 ...)                     ; cinco veces, sin contador
```

`below` merece atención: evita el `n - 1` que todo el mundo escribe mal alguna vez.

Y para este caso concreto, un programador de Lisp escribiría el factorial **sin bucle**:

```lisp
(reduce #'* (loop for i from 1 to n collect i) :initial-value 1)
(apply #'* (loop for i from 1 to n collect i))      ; ojo: límite de argumentos
```

`reduce` con `:initial-value 1` devuelve 1 para la lista vacía, que es exactamente `0!`. Es la clase
068 aplicada aquí: cuando el bucle solo acumula, hay una función que lo dice mejor.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

set f 1
for {set i 1} {$i <= $n} {incr i} {
    set f [expr {$f * $i}]
}

puts "factorial=$f"
""", """
**Lo que esta clase enseña en Tcl.** El `for` de Tcl recibe **cuatro argumentos**: inicialización,
condición, incremento y cuerpo. Es la forma de C, y como todo en Tcl, son cuatro cadenas que el
comando evalúa cuando le toca.

Eso significa que la inicialización y el incremento pueden ser **cualquier código**, no solo
asignaciones:

```tcl
for {set i 1; set j 10} {$i < $j} {incr i; incr j -1} { ... }
```

Y como los enteros de Tcl son de **precisión arbitraria** desde la versión 8.5, aquí tampoco hay
desbordamiento: `expr {2**200}` funciona y el factorial de 100 sale entero. Es el mismo
comportamiento de Lisp y Smalltalk.

Para recorrer, Tcl tiene además `foreach`, que es sorprendentemente potente:

```tcl
foreach x $lista { ... }
foreach {clave valor} $lista { ... }        ;# de dos en dos
foreach a $lista1 b $lista2 { ... }         ;# DOS listas EN PARALELO
```

La última forma —recorrer varias listas a la vez— no la tienen ni C++ ni Java sin bibliotecas
auxiliares; en Python hace falta `zip`. En Tcl es un argumento más de `foreach`.

Y `lmap`, añadido en 8.6, es igual pero **recoge el resultado** de cada vuelta: es el `map` de la
clase 068 con sintaxis de bucle.
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

my $f = 1;
$f *= $_ for 1 .. $n;

print "factorial=$f\\n";
""", """
**Lo que esta clase enseña en Perl.** `$f *= $_ for 1 .. $n;` es un **modificador de sentencia** con
un bucle detrás: se lee "multiplica f por cada uno, para uno hasta n". No hay llaves, no hay variable
de control declarada y no hay cuerpo.

`$_` es la **variable por defecto** de Perl, el sujeto implícito. En un `for` sin variable declarada,
cada elemento se asigna a `$_`, y muchísimas funciones —`print`, `chomp`, `lc`, `length`, y las
expresiones regulares— operan sobre `$_` si no se les da argumento. Es lo que permite escribir
`print for @lista`.

Y `1 .. $n` es el **operador de rango**, que en contexto de lista genera todos los valores. Perl lo
optimiza: en un `foreach`, el rango **no construye la lista en memoria**, sino que itera perezosamente.
`for (1 .. 1_000_000_000)` no reserva mil millones de elementos.

Un detalle importante de esta clase: **`$_` en un `foreach` es un alias, no una copia**.

```perl
$_ *= 2 for @numeros;     # MODIFICA @numeros en el sitio
```

Esa línea duplica todos los elementos del array original. Es potentísimo y sorprende: en Python o
Java, la variable del bucle es una copia y modificarla no toca la colección. En Perl —y en Ada con
`for E of`— es una referencia al elemento real.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    unsigned long long f = 1;
    for (int i = 1; i <= n; ++i) {
        f *= static_cast<unsigned long long>(i);
    }

    std::cout << "factorial=" << f << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** El `for` de C es **tres expresiones separadas por punto y coma**,
y esa generalidad es a la vez su fuerza y su problema: no es un bucle de rango, es un `while` con
azúcar. Nada obliga a que la variable de control se incremente, ni a que la condición la use.

C++11 añadió el bucle de rango de verdad, que es lo que se usa hoy siempre que se puede:

```cpp
for (const auto& x : coleccion) { ... }        // por referencia constante: sin copias
for (auto& x : coleccion) { x *= 2; }          // modificando
for (auto x : coleccion) { ... }               // COPIA cada elemento: ojo con los grandes
```

Ese `const auto&` es la forma correcta por defecto: `auto` a secas **copia**, y con objetos grandes
eso es coste puro. Es el mismo aviso que en la clase 052.

C++20 completó la idea con los **rangos**, que traen por fin el equivalente de `1 .. n`:

```cpp
#include <ranges>
for (int i : std::views::iota(1, n + 1)) { f *= i; }
```

Y sobre el desbordamiento: se usa `unsigned long long` **a propósito**. El desbordamiento de un entero
**con signo** es comportamiento indefinido; el de un **sin signo** está definido como aritmética
modular. Ninguno de los dos da el resultado correcto para `21!`, pero solo uno de ellos permite al
compilador asumir que nunca ocurre y borrar código que lo comprueba.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi FACT;
  n int(10) const;
end-pi;

dcl-s i      int(10);
dcl-s f      packed(30:0) inz(1);
dcl-s salida char(50);

for i = 1 to n;
  f *= i;
endfor;

salida = 'factorial=' + %char(f);
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** `packed(30:0)` son **treinta dígitos decimales**, así que el
factorial de 20 —diecinueve dígitos— cabe con margen y el de 29 también. Igual que COBOL, RPG
resuelve el problema de esta clase **declarando más dígitos**, porque su aritmética es decimal y no
está atada al tamaño de la palabra de máquina. El máximo actual son 63 dígitos.

`for i = 1 to n` admite `by` y `downto`:

```rpgle
for i = 1 to 100 by 5;
for i = 10 downto 1;
for i = 1 by 2 to 99;
```

Y RPG tiene una variante que conviene conocer al leer código de gestión: **`for-each`**, añadida en
7.5, que recorre una matriz sin índice:

```rpgle
for-each elemento in ventas;
  total += elemento;
endfor;
```

Antes de eso, recorrer una matriz exigía `for i = 1 to %elem(ventas)`, con `%elem` devolviendo el
número de elementos declarados. Que `for-each` sea de 2022 en un lenguaje de 1959 es un buen
recordatorio de que estos lenguajes **siguen recibiendo características**, que es justo lo que la
sección de lenguajes vivos quiere dejar claro.
"""),
        "pli": ("""
 factorial: procedure options(main);

    declare n fixed binary(31);
    declare i fixed binary(31);
    declare f fixed decimal(31,0) initial(1);

    get list (n);

    do i = 1 to n;
       f = f * i;
    end;

    put skip list ('factorial=' || trim(char(f)));

 end factorial;
""", """
**Lo que esta clase enseña en PL/I.** `fixed decimal(31,0)` son **treinta y un dígitos**, el máximo
del estándar, así que `20!` cabe holgadamente. Es la misma solución que COBOL y RPG: **aritmética
decimal con la precisión declarada**, no un entero atado a la palabra de máquina.

Y el `do i = 1 to n` de PL/I es la forma más rica de bucle de rango de esta página, como ya se apuntó
en la clase 063:

```pli
do i = 1 to n by 2;
do i = 1 to n while (encontrado = '0'b);      /* rango Y condición */
do i = 1 to 5, 10 to 15, 20;                   /* tramos discontinuos */
do i = 1 repeat i * 3 until (i > 1000);        /* progresión geométrica */
```

La combinación `to ... while ...` es especialmente útil y no la tiene ningún lenguaje del núcleo:
recorre un rango **y** para antes si se cumple una condición, sin necesidad de `break`. Expresa
directamente "busca entre las 100 primeras posiciones hasta encontrarlo".

Y si el resultado no cabe en los dígitos declarados, PL/I levanta la condición **`FIXEDOVERFLOW`**,
capturable con el mecanismo `ON` de la clase 041. No es truncación silenciosa: es un suceso con
nombre. Es la diferencia con el `MOVE` de COBOL de la clase 049, y una de las cosas que PL/I hizo
mejor.
"""),
        "mumps": ("""
FACT ; Factorial -- clase 064
 read n
 set f = 1
 for i = 1:1:n set f = f * i
 write "factorial=", f, !
 quit
""", """
**Lo que esta clase enseña en M.** `for i = 1:1:n` es el bucle de rango, con la sintaxis
**inicio:incremento:final** separada por dos puntos. Sin el tercer valor —`for i = 1:1`— es infinito
ascendente, y se sale con un `quit` postcondicional.

Y aquí hay que decir algo incómodo sobre M, porque es una limitación real: **su aritmética tiene una
precisión de unos 18 o 19 dígitos significativos**. `20!` son diecinueve dígitos, así que está justo
en el límite; `21!` ya perdería precisión, y lo haría **en silencio**, porque M nunca falla al
calcular.

No es un descuido del diseño: M nació para manejar dosis, resultados de laboratorio e importes de
facturación sanitaria, donde 18 dígitos sobran. Nadie calcula factoriales grandes en un sistema
clínico.

Cuando hace falta más, las implementaciones modernas ofrecen extensiones —YottaDB e IRIS tienen
soporte de precisión ampliada— pero el lenguaje base no lo garantiza.

Es un buen ejemplo del criterio con el que hay que leer toda esta sección: **cada uno de estos
lenguajes es excelente en su dominio y mediocre fuera de él**. M es imbatible recorriendo un árbol de
un millón de pacientes y no es la herramienta para cálculo numérico. Fortran es lo contrario.
"""),
        "smalltalk": ("""
| n f |

n := stdin nextLine trimBoth asNumber.

f := 1.
1 to: n do: [ :i | f := f * i ].

Transcript show: 'factorial=', f printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** `1 to: n do: [ :i | ... ]` es **un mensaje enviado al
número 1**, con dos argumentos: el límite y un bloque. No hay palabra clave `for`; hay un método de
`Number`:

```smalltalk
Number >> to: limite do: unBloque
    | i |
    i := self.
    [ i <= limite ] whileTrue: [ unBloque value: i. i := i + 1 ].
    ^ self
```

La familia completa es `to:do:`, `to:by:do:` (con paso, que admite negativos), `timesRepeat:` (sin
contador) y, para colecciones, `do:`, `collect:`, `select:`, `detect:`, `inject:into:`.

Y aquí ocurre lo mismo que con `whileTrue:` en la clase 063: **el compilador lo compila en línea**,
generando un bucle real en el bytecode en lugar de un envío de mensaje por vuelta. La semántica es la
de un método; el rendimiento es el de un bucle.

Sobre el desbordamiento: **no existe**. `1000 factorial` devuelve un número de 2568 dígitos, porque
`SmallInteger` se convierte en `LargePositiveInteger` de forma automática e invisible. Y de hecho
Smalltalk tiene el método:

```smalltalk
Integer >> factorial
    "está en la biblioteca; puedes leerlo y ver que usa productoria por bloques"
```

Así que un programador de Smalltalk escribiría `n factorial` y ya está — y sabría que la
implementación de la biblioteca es más lista que el bucle ingenuo de este programa.
"""),
    },
)
