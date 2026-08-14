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

# ---------------------------------------------------------------------------
# 065 — Iteración por colección: for-each e iteradores
# ---------------------------------------------------------------------------
SPECS["065"] = dict(
    gancho="""
Sumar una lista de enteros cuya longitud **no se sabe de antemano**. Ahí está la diferencia con la
clase anterior: un bucle de rango necesita saber cuántas vueltas dará; recorrer una colección
necesita otra cosa — **preguntarle a la propia colección si queda algo**. Esa inversión es el
concepto del iterador.
""",
    porque="""
Aquí el concepto es el **recorrido de una colección**, y estos lenguajes lo enseñan porque muestran
lo que había **antes de que existiera el iterador como abstracción**. En COBOL y Fortran clásico hay
que llevar el contador a mano, y por eso el idioma es "una tabla y una variable con cuántos elementos
tiene ocupados". En RPG, el bucle ni siquiera se escribe: **lo pone el ciclo del programa**.

Y M enseña la versión más potente y menos conocida: **`$order` recorre un árbol persistente de un
millón de nodos sin cargarlo en memoria**, que es exactamente lo que hoy llamamos un iterador
perezoso sobre una base de datos.
""",
    cierre="""
Lo transferible es la pregunta **"¿quién sabe cuándo termina el recorrido?"**. Si la respuesta es "una
variable contador que llevo yo", el código es frágil: basta con que alguien inserte un elemento sin
actualizarla. Si la respuesta es "la colección", el recorrido es correcto por construcción. Toda la
evolución que va del `DO 100 I = 1, N` de Fortran al `for x of coleccion` de Ada 2012 y al
`for (auto& x : v)` de C++11 es el traslado de esa responsabilidad del programador a la estructura.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. SUMALISTA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  I       PIC 9(4)  COMP-3.
01  LARGO   PIC 9(4)  COMP-3.
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(4)  COMP-3.
01  C       PIC X.
01  TOTAL   PIC S9(18) COMP-3.
01  ED-T    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE 0 TO TOTAL
    MOVE SPACES TO TOKEN
    MOVE 0 TO TLEN
    COMPUTE LARGO = FUNCTION LENGTH(FUNCTION TRIM(LINEA)) + 1

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > LARGO
        MOVE LINEA(I:1) TO C
        IF C = SPACE
            IF TLEN > 0
                COMPUTE TOTAL = TOTAL + FUNCTION NUMVAL(TOKEN(1:TLEN))
                MOVE SPACES TO TOKEN
                MOVE 0 TO TLEN
            END-IF
        ELSE
            ADD 1 TO TLEN
            MOVE C TO TOKEN(TLEN:1)
        END-IF
    END-PERFORM

    MOVE TOTAL TO ED-T
    DISPLAY "suma=" FUNCTION TRIM(ED-T)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** **COBOL no tiene iteradores ni colecciones de tamaño
variable.** Tiene **tablas** con `OCCURS`, que son arrays de tamaño fijo declarado, y el número de
elementos ocupados lo lleva el programador en una variable aparte:

```cobol
01  TABLA-VENTAS.
    05  NUM-VENTAS  PIC 9(4) COMP-3.
    05  VENTA       OCCURS 1 TO 1000 TIMES
                    DEPENDING ON NUM-VENTAS
                    PIC S9(9)V99 COMP-3.

PERFORM VARYING I FROM 1 BY 1 UNTIL I > NUM-VENTAS
    ADD VENTA(I) TO TOTAL
END-PERFORM
```

`OCCURS DEPENDING ON` es lo más cerca que llega COBOL de una colección de tamaño variable: la tabla
declara un máximo y **una variable dice cuántos elementos son válidos ahora**. Es exactamente el
patrón "array más contador" que C usa, con la ventaja de que aquí la relación está **declarada** y el
compilador puede comprobar los límites con `SSRANGE`.

Y COBOL tiene una operación sobre tablas que sí es de alto nivel y conviene conocer:

```cobol
SEARCH VENTA VARYING I
    AT END DISPLAY "no encontrado"
    WHEN VENTA(I) > LIMITE DISPLAY "encontrado en " I
END-SEARCH

SEARCH ALL VENTA                    *> búsqueda BINARIA, si la tabla está ordenada
    WHEN CLAVE(I) = BUSCADA ...
```

`SEARCH ALL` hace una búsqueda binaria sobre una tabla declarada con `ASCENDING KEY`. Es un algoritmo
completo dentro del lenguaje, en 1968.
"""),
        "fortran": ("""
program suma_lista
   implicit none
   character(len=1000) :: linea
   integer :: valores(200), n, i, total, ios

   read(*, '(A)') linea

   !  Cuántos valores hay en la línea: se prueba a leer 1, 2, 3... hasta fallar.
   n = 0
   do i = 1, 200
      read(linea, *, iostat=ios) valores(1:i)
      if (ios /= 0) exit
      n = i
   end do

   total = 0
   do i = 1, n
      total = total + valores(i)
   end do

   write(*, '(A,I0)') 'suma=', total
end program suma_lista
""", """
**Lo que esta clase enseña en Fortran.** El bucle que cuenta los valores es el **idioma clásico de
Fortran para "no sé cuántos hay en esta línea"**, y merece explicación porque es raro visto desde
fuera: se intenta leer 1 valor, luego 2, luego 3, y se para cuando la lectura falla. `iostat=ios`
captura el error en lugar de abortar.

Es O(n²) y nadie lo defendería hoy, y sin embargo aparece en código científico real, porque el
sistema de E/S de Fortran está diseñado para **registros de forma conocida**, no para líneas de
longitud arbitraria. Cuando el fichero tiene una cabecera que dice cuántos valores vienen —que es lo
normal en los formatos científicos— el problema no existe.

Lo que Fortran sí tiene, y es su gran aportación a esta clase, es que **el bucle sobre la colección
casi nunca hace falta**:

```fortran
total = sum(valores(1:n))              ! sin bucle
media = sum(v) / size(v)
mayor = maxval(v)
donde = maxloc(v)                      ! la POSICIÓN del máximo
cuantos = count(v > 0)                 ! cuántos cumplen
todos = all(v > 0)                     ! ¿todos?
alguno = any(v < 0)                    ! ¿alguno?
```

`sum`, `product`, `maxval`, `minval`, `maxloc`, `count`, `all`, `any`, `dot_product`, `matmul` —
todas operan sobre arrays completos y todas se vectorizan. En Fortran, **recorrer un array a mano es
casi siempre un síntoma de que no conoces la intrínseca que hace eso**.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Suma_Lista is
   Linea  : String (1 .. 500);
   Ultimo : Natural;
   Pos    : Positive := 1;
   Fin    : Positive;
   Valor  : Integer;
   Total  : Integer := 0;
begin
   Get_Line (Linea, Ultimo);

   while Pos <= Ultimo loop
      --  Get sobre una PORCIÓN de cadena: devuelve el valor y hasta dónde leyó.
      Get (Linea (Pos .. Ultimo), Valor, Fin);
      Total := Total + Valor;
      Pos := Fin + 1;
   end loop;

   Put ("suma="); Put (Total, Width => 1); New_Line;
end Suma_Lista;
""", """
**Lo que esta clase enseña en Ada.** `Get (From : String; Item : out Integer; Last : out Positive)`
es una forma de lectura que casi ningún lenguaje ofrece: **analiza un valor a partir de una cadena y
devuelve hasta dónde ha llegado**. Con eso, recorrer una línea de valores es avanzar `Pos` hasta el
final, sin partir la cadena ni reservar memoria.

Es el mismo mecanismo que `std::from_chars` de C++17, disponible desde 1983.

Pero la aportación de Ada a esta clase llegó con **Ada 2012** y sus **interfaces de iterador**, que
permiten que **cualquier tipo tuyo** se recorra con `for ... of`:

```ada
for Elemento of Mi_Coleccion loop ... end loop;
```

Para que eso funcione, el tipo declara el aspecto `Iterable` o implementa `Ada.Iterator_Interfaces`,
con `First`, `Next` y `Has_Element`. Es exactamente el mismo contrato que `IEnumerable` en C#,
`Iterator` en Java o `begin`/`end` en C++.

Y Ada 2022 fue más lejos con las **expresiones de agregado iteradas**, que son comprensiones de
listas:

```ada
Cuadrados : constant Vector := [for I in 1 .. 10 => I * I];
```

Un lenguaje de 1983 incorporando comprensiones en 2022 es, otra vez, el argumento de esta sección
entera: **no son fotos fijas**.
"""),
        "pascal": ("""
program SumaLista;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, Token: string;
  I, Total: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea) + ' ';

  Total := 0;
  Token := '';
  for I := 1 to Length(Linea) do
  begin
    if Linea[I] = ' ' then
    begin
      if Token <> '' then
      begin
        Total := Total + StrToInt(Token);
        Token := '';
      end;
    end
    else
      Token := Token + Linea[I];
  end;

  WriteLn('suma=', IntToStr(Total));
end.
""", """
**Lo que esta clase enseña en Pascal.** El Pascal ISO **no tiene función de partir cadenas**, así que
el tokenizador se escribe a mano. Es una carencia real y muy visible en cuanto se procesa texto.

Free Pascal y Delphi lo resolvieron por dos vías distintas, y conviene conocer las dos porque
aparecen en código de épocas diferentes:

```pascal
{ 1) TStringList con delimitador: la forma clásica de Delphi }
Lista := TStringList.Create;
try
  Lista.Delimiter := ' ';
  Lista.DelimitedText := Linea;
  for I := 0 to Lista.Count - 1 do
    Total := Total + StrToInt(Lista[I]);
finally
  Lista.Free;
end;

{ 2) Ayudantes de tipo, en Delphi moderno }
for S in Linea.Split([' ']) do ...
```

Fíjate en el `try..finally` de la primera: **`TStringList` es un objeto y hay que liberarlo**, con la
disciplina de la clase 042. Ese bloque es el idioma más repetido del código Delphi del mundo.

Y `for..in` sobre colecciones llegó a Free Pascal y Delphi en 2005, con el mismo contrato que los
demás: el tipo implementa `GetEnumerator` y devuelve un objeto con `MoveNext` y `Current`. Es el
patrón que C# había estrenado poco antes, y que Ada, C++ y Java tienen con otros nombres. **Los cinco
llegaron a la misma solución.**
"""),
        "lisp": ("""
(let ((total 0))
  (loop for valor = (read *standard-input* nil :fin)
        until (eq valor :fin)
        do (incf total valor))
  (format t "suma=~D~%" total))
""", """
**Lo que esta clase enseña en Common Lisp.** `(read stream nil :fin)` es la lectura con **valor
centinela**: en lugar de señalar un error al llegar al final, devuelve el objeto que le indiques.
Aquí, la palabra clave `:fin`, que no puede confundirse con ningún número.

Es el mismo patrón que `iostat` en Fortran y que comprobar el flujo en C++, y es la primera pieza de
esta clase: **cómo sabe el bucle que ya no hay más**.

La segunda pieza es que Lisp tiene **funciones de secuencia genéricas** que funcionan igual sobre
listas, vectores y cadenas —lo que ya se vio en la clase 048—:

```lisp
(reduce #'+ lista)                    ; suma
(count-if #'evenp lista)              ; cuántos pares
(find-if (lambda (x) (> x 100)) lista)
(position 42 lista)
(some #'minusp lista)                 ; ¿alguno negativo?  cortocircuita
(every #'plusp lista)
(map 'vector #'1+ lista)              ; el TIPO del resultado como argumento
```

`some` y `every` **cortocircuitan**, al contrario que `any`/`all` de PL/I sobre cadenas de bits.

Y `loop` tiene cláusulas de acumulación que hacen innecesaria la variable manual de este programa:

```lisp
(loop for x in lista sum x)
(loop for x in lista when (evenp x) collect x)
(loop for x in lista maximize x)
(loop for x in lista count (plusp x))
```

`sum`, `collect`, `maximize`, `minimize`, `count`, `append` y `nconc` son parte del mini-lenguaje de
`loop`, y cubren casi todo lo que en otros lenguajes exige `map`/`filter`/`reduce`.
"""),
        "tcl": ("""
gets stdin linea

set total 0
foreach v [split [string trim $linea]] {
    incr total $v
}

puts "suma=$total"
""", """
**Lo que esta clase enseña en Tcl.** `foreach` es el recorrido de colección de Tcl, y tiene dos
formas que casi ningún lenguaje ofrece:

```tcl
foreach {clave valor} $lista { ... }        ;# de DOS en dos
foreach a $lista1 b $lista2 { ... }         ;# dos listas EN PARALELO
foreach a $l1 {b c} $l2 { ... }             ;# ¡y con tamaños de grupo distintos!
```

Recorrer una lista de pares clave-valor de dos en dos, o dos listas a la vez, son operaciones que en
C++ exigen iteradores manuales y en Python el `zip`. Aquí son argumentos adicionales del mismo
comando.

Y `split` es la contrapartida de `join`: convierte una cadena en lista partiendo por los caracteres
que indiques. **Sin argumento, parte por espacios en blanco**, que es lo que hace este programa.

Un aviso que conviene tener presente: `split` **con** un delimitador explícito produce elementos
vacíos si hay separadores consecutivos:

```tcl
split "a,,b" ","          ;# -> {a {} b}   -- tres elementos, uno vacío
split "a  b"              ;# -> {a {} b}   -- ¡también!
split [string trim "a  b"] " "  ;# sigue dando el vacío
```

Por eso este programa usa `split` **sin argumento** sobre la cadena recortada, que colapsa las rachas
de espacios. Es la misma diferencia que en COBOL entre `DELIMITED BY SPACE` y `DELIMITED BY ALL
SPACES`, y en Perl entre `split /,/` y `split ' '`.
"""),
        "perl": ("""
use strict;
use warnings;
use List::Util qw(sum0);

my $linea = <STDIN>;
chomp $linea;

my $total = sum0(split ' ', $linea);

print "suma=$total\\n";
""", """
**Lo que esta clase enseña en Perl.** `sum0(split ' ', $linea)` es toda la solución: partir y sumar,
sin bucle y sin variable acumuladora.

`List::Util` está en el núcleo desde 2001 y sus funciones están escritas en C:

```perl
use List::Util qw(sum sum0 max min first any all none reduce shuffle uniq);

sum @v            # undef si la lista está vacía
sum0 @v           # 0 si está vacía  <- casi siempre lo que quieres
first { $_ > 100 } @v      # cortocircuita
reduce { $a + $b } @v      # el plegado general
```

La distinción entre `sum` y `sum0` es la clase 053 aplicada aquí: **"no hay elementos" y "la suma es
cero" son cosas distintas**, y Perl te deja elegir cuál devuelve.

Y el recorrido idiomático es `foreach`, con la propiedad que ya apareció en la clase 064 y que
conviene recordar porque es peligrosa y útil a partes iguales:

```perl
for my $x (@lista) { $x *= 2 }      # MODIFICA @lista: $x es un ALIAS
for my $x (@lista) { my $y = $x * 2 }   # sin tocar el original
```

La variable del bucle **no es una copia**, es una referencia al elemento real. En Python o Java eso
no ocurre. Ada lo hace igual con `for E of` cuando el elemento no es constante, y C++ solo si escribes
`auto&`.
"""),
        "cpp": ("""
#include <iostream>
#include <iterator>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>

int main() {
    std::string linea;
    if (!std::getline(std::cin, linea)) return 1;

    std::istringstream iss(linea);
    const std::vector<int> valores{std::istream_iterator<int>(iss),
                                   std::istream_iterator<int>()};

    const int total = std::accumulate(valores.begin(), valores.end(), 0);

    std::cout << "suma=" << total << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** Este programa construye el vector **directamente desde un par de
iteradores de flujo**, sin bucle de lectura. `std::istream_iterator<int>(iss)` es un iterador que, al
avanzar, lee el siguiente entero; el construido sin argumentos representa el final.

Ese es el diseño de la **STL** de Alexander Stepanov, y es la aportación conceptual de C++ a esta
clase: **los algoritmos no conocen los contenedores, conocen iteradores**.

```cpp
std::accumulate(v.begin(), v.end(), 0);        // sobre un vector
std::accumulate(l.begin(), l.end(), 0);        // sobre una lista enlazada
std::accumulate(s.begin(), s.end(), 0);        // sobre un conjunto
std::accumulate(it_flujo, it_fin, 0);          // ¡sobre un FLUJO de entrada!
```

**El mismo algoritmo, sin recompilar nada distinto, sobre cuatro estructuras que no se parecen en
nada.** Un contenedor solo tiene que ofrecer iteradores; un algoritmo solo tiene que pedirlos. Esa
separación en tres piezas —contenedores, iteradores, algoritmos— es la idea que después copiaron los
`Stream` de Java, los `IEnumerable` de C# y los `Iterator` de Rust.

C++20 la refinó con los **rangos**, que evitan tener que escribir `begin()` y `end()`:

```cpp
#include <ranges>
const int total = std::ranges::fold_left(valores, 0, std::plus{});
```
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi SUMALIS;
  linea varchar(200) const;
end-pi;

dcl-s trozos varchar(20) dim(50);
dcl-s cuantos int(10);
dcl-s i       int(10);
dcl-s total   int(20) inz(0);
dcl-s salida  char(40);

trozos = %split(linea : ' ');
cuantos = %elem(trozos);

for i = 1 to cuantos;
  total += %int(trozos(i));
endfor;

salida = 'suma=' + %char(total);
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** `%split` —que parte una cadena y devuelve una **matriz**— se
añadió en **IBM i 7.4, en 2019**. Durante cincuenta años, partir una cadena en RPG se hacía con un
bucle y `%scan`. Es otro recordatorio de que estos lenguajes siguen recibiendo funcionalidad.

Pero el recorrido de colecciones **de verdad** en RPG no es sobre matrices: es sobre **ficheros de
base de datos**, y ahí está la aportación de esta clase.

```rpgle
dcl-f CLIENTES usage(*input) keyed;

setll *loval CLIENTES;        // posicionarse al principio
read CLIENTES;
dow not %eof(CLIENTES);
  total += CLI_SALDO;         // los campos son VARIABLES del programa
  read CLIENTES;
enddo;
```

`setll` (*set lower limit*), `read`, `reade` (leer mientras la clave coincida), `chain` (búsqueda
directa) y `%eof` son el vocabulario de recorrido, y operan sobre **millones de registros sin
cargarlos en memoria**. Es un iterador perezoso sobre una base de datos, integrado en el lenguaje.

Y en el RPG clásico ni siquiera eso se escribía: con un fichero declarado como **entrada primaria**,
el **ciclo del programa** hacía el `read` y el `dow` por ti. Tú solo escribías qué hacer con cada
registro. Es exactamente la inversión de control de la clase 063.
"""),
        "pli": ("""
 suma_lista: procedure options(main);

    declare linea  character(200) varying;
    declare trozo  character(20)  varying;
    declare total  fixed binary(31) initial(0);
    declare (i, p) fixed binary(31);

    get edit (linea) (a(200));
    linea = trim(linea) || ' ';

    p = 1;
    do i = 1 to length(linea);
       if substr(linea, i, 1) = ' ' then do;
          if i > p then do;
             trozo = substr(linea, p, i - p);
             total = total + trozo;      /* conversión implícita texto->número */
          end;
          p = i + 1;
       end;
    end;

    put skip list ('suma=' || trim(char(total)));

 end suma_lista;
""", """
**Lo que esta clase enseña en PL/I.** Fíjate en `total = total + trozo`: **`trozo` es una cadena de
caracteres y se suma a un entero sin ninguna conversión escrita**. Es la conversión implícita de la
clase 050, aquí en su versión más cómoda y más peligrosa: funciona perfectamente hasta que el texto
no es un número, y entonces levanta la condición `CONVERSION`.

Sobre el recorrido de colecciones, PL/I tiene arrays de primera clase con operaciones sobre el
conjunto, igual que Fortran:

```pli
declare v(100) fixed binary(31);

total = sum(v);              /* sin bucle */
mayor = max(v);
v = v * 2;                   /* opera sobre TODO el array */
v(10:20) = 0;                /* una PORCIÓN */
if any(v > 100) then ...
```

Que un lenguaje de negocio de 1964 tuviera aritmética de arrays completos es notable, y es la
influencia directa de FORTRAN en su diseño — recuerda que PL/I nació para unir los dos mundos.

Lo que no tiene es un iterador abstracto: no hay forma de recorrer una estructura definida por el
usuario con una construcción genérica. Para eso hay que esperar a los lenguajes con tipos abstractos
de datos, que es lo que trajo Ada en 1983 y CLU un poco antes.
"""),
        "mumps": ("""
SUMA ; Suma de una lista -- clase 065
 read linea
 set total = 0
 for i = 1:1:$length(linea, " ") do
 . set total = total + $piece(linea, " ", i)
 write "suma=", total, !
 quit
""", """
**Lo que esta clase enseña en M.** `$length(linea, " ")` cuenta **cuántos trozos** hay, y `$piece`
extrae el *i*-ésimo. Es el recorrido de la "colección ligera" de M: una cadena con delimitadores.

Pero la aportación real de M a esta clase es **`$order`**, que recorre un árbol de la base de datos
**sin cargarlo en memoria**:

```mumps
 set clave = ""
 for  set clave = $order(^VENTAS(clave))  quit:clave = ""  do
 . set total = total + ^VENTAS(clave)
```

`$order(^VENTAS(clave))` devuelve **la siguiente clave existente en orden**, y la cadena vacía cuando
no queda ninguna. Con eso se recorre un *global* de **diez millones de nodos** consumiendo memoria
constante, porque cada llamada es una búsqueda en el índice del árbol B en disco.

Eso es un **iterador perezoso sobre una base de datos**, con una sola función y sin cursor que abrir
ni cerrar. Y funciona en cualquier nivel de subíndice y en cualquier dirección:

```mumps
 set fecha = $order(^CITAS(pac, fecha), -1)     ; la ANTERIOR: recorrido inverso
 set sig = $query(^CITAS(pac))                  ; el siguiente nodo con VALOR, a cualquier profundidad
```

`$query` recorre el árbol entero en profundidad, saltando de nodo a nodo con independencia del número
de subíndices. Es el recorrido completo de una estructura jerárquica en una llamada — y es la razón
de que un sistema clínico en M pueda listar el historial de un paciente sin ningún ORM.
"""),
        "smalltalk": ("""
| total |

total := (stdin nextLine substrings collect: [ :cada | cada asNumber ])
    inject: 0 into: [ :acc :cada | acc + cada ].

Transcript show: 'suma=', total printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** `inject:into:` es el **plegado** —el `reduce` de la clase
068— y aquí resuelve la suma sin bucle ni acumulador visible: `0` es el valor inicial y el bloque
recibe el acumulado y el elemento.

Pero lo que hay que ver en esta clase es de dónde sale: **`inject:into:` está implementado en
`Collection`, en términos de `do:`**, y `do:` es lo único que una colección tiene que saber hacer:

```smalltalk
Collection >> inject: valorInicial into: unBloque
    | acumulado |
    acumulado := valorInicial.
    self do: [ :cada | acumulado := unBloque value: acumulado value: cada ].
    ^ acumulado
```

Y con `do:` implementado, una subclase hereda **gratis** todo el protocolo: `collect:`, `select:`,
`reject:`, `detect:`, `inject:into:`, `anySatisfy:`, `allSatisfy:`, `sum`, `max`, `sorted`,
`asOrderedCollection`, `groupedBy:`, `count:`… más de cien métodos.

Ese es el patrón del **método plantilla** en su forma más pura: define una operación primitiva y
recibe el resto. Es la misma economía que la STL de C++ obtiene con iteradores y que Rust obtiene con
el *trait* `Iterator` y sus métodos por defecto — tres soluciones distintas al mismo problema de
diseño, y esta es la más antigua.

Para colecciones grandes o infinitas, Pharo tiene además `ReadStream` y `Generator`, que se ven en la
clase siguiente.
"""),
    },
)

# ---------------------------------------------------------------------------
# 066 — Iteradores y generadores perezosos (lazy)
# ---------------------------------------------------------------------------
SPECS["066"] = dict(
    gancho="""
Producir los *n* primeros números pares. El programa es trivial; lo interesante es **quién decide
cuándo se calcula cada valor**. Un generador perezoso no construye la lista entera: fabrica un valor,
lo entrega, **se queda parado a mitad de su bucle** y espera a que le pidan el siguiente. Es control
de flujo suspendido y reanudado, y muy pocos lenguajes de esta página lo tienen.
""",
    porque="""
Aquí el concepto es la **evaluación perezosa y la suspensión de la ejecución**, y estos lenguajes
aportan tres cosas que el núcleo no muestra. La primera: **Tcl tiene corrutinas de verdad** desde
2012 —`yield` y reanudación—, y este programa las usa. La segunda: **la clausura como generador**, que
es lo que hace Perl y lo que hacía Lisp antes de que existiera `yield` en ningún sitio.

Y la tercera, la más interesante: en **M** el recorrido perezoso no es una construcción del lenguaje,
es **`$order` sobre un árbol de disco**, y en **RPG** es el ciclo del programa empujándote los
registros. Dos modelos de pereza —tirar y empujar— que preceden en décadas a los generadores.
""",
    cierre="""
La distinción que deja esta clase es entre **tirar** (*pull*) y **empujar** (*push*). Un iterador o un
generador es *pull*: tú pides el siguiente y el productor se despierta. El ciclo de RPG, un manejador
de eventos o un `Observer` son *push*: el productor manda y tú reaccionas. Las dos formas recorren lo
mismo y ponen el bucle en sitios opuestos, y reconocer cuál tienes delante explica por qué unas APIs
se componen con facilidad y otras te obligan a llevar el estado a mano.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. PARES.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC 9(4)  COMP-3.
01  I       PIC 9(4)  COMP-3.
01  V       PIC 9(9)  COMP-3.
01  ED-V    PIC Z(8)9.
01  TROZO   PIC X(20).
01  TLEN    PIC 9(4)  COMP-3.
01  SEC     PIC X(400).
01  PTR     PIC 9(4)  COMP-3.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N
    MOVE SPACES TO SEC
    MOVE 1 TO PTR

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        COMPUTE V = 2 * I
        MOVE V TO ED-V
        MOVE FUNCTION TRIM(ED-V) TO TROZO
        COMPUTE TLEN = FUNCTION LENGTH(FUNCTION TRIM(TROZO))
        IF PTR > 1
            MOVE "-" TO SEC(PTR:1)
            ADD 1 TO PTR
        END-IF
        MOVE TROZO(1:TLEN) TO SEC(PTR:TLEN)
        ADD TLEN TO PTR
    END-PERFORM

    DISPLAY "pares=" FUNCTION TRIM(SEC)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** **COBOL no tiene generadores, ni corrutinas, ni evaluación
perezosa.** Un `PERFORM` se ejecuta entero; no hay forma de suspenderlo a mitad y reanudarlo después.

Y sin embargo, el modelo *pull* que esta clase describe es **exactamente cómo COBOL lee ficheros**:

```cobol
PERFORM UNTIL FIN-FICHERO
    READ CLIENTES
        AT END SET FIN-FICHERO TO TRUE
        NOT AT END PERFORM PROCESAR-CLIENTE
    END-READ
END-PERFORM
```

`READ` entrega **un registro cada vez**, sin cargar el fichero en memoria, y el bucle pide el
siguiente cuando ha terminado con el anterior. Es un iterador perezoso sobre diez millones de
registros — con la diferencia de que el productor no es código de usuario suspendido, sino el
subsistema de acceso a ficheros del sistema operativo.

Esa es la observación de fondo de esta clase: **la pereza no llegó con los generadores; llegó con la
E/S**. Todo el proceso por lotes desde los años 60 está construido sobre "lee un registro, procésalo,
olvídalo", porque **la cinta no cabía en memoria**. Los generadores de los lenguajes modernos
generalizan a cualquier cálculo lo que la E/S secuencial hacía desde el principio.
"""),
        "fortran": ("""
program pares
   implicit none
   integer :: n, i
   character(len=:), allocatable :: sec
   character(len=16) :: buf

   read(*, *) n

   sec = ''
   do i = 1, n
      write(buf, '(I0)') 2 * i
      if (i > 1) sec = sec // '-'
      sec = sec // trim(buf)
   end do

   write(*, '(A,A)') 'pares=', sec
end program pares
""", """
**Lo que esta clase enseña en Fortran.** Fortran **no tiene generadores ni corrutinas**, y es
coherente con su propósito: en cálculo numérico se opera sobre **arrays completos que ya están en
memoria**, no sobre secuencias potencialmente infinitas.

Su forma de generar una secuencia es construir el array de una vez, y para eso tiene una construcción
que sí conviene conocer, el **constructor de array con bucle implícito**:

```fortran
integer :: pares(n)
pares = [(2 * i, i = 1, n)]                 ! el array ENTERO, en una expresión
impares = [(i, i = 1, 100, 2)]
matriz = reshape([(i, i = 1, 12)], [3, 4])  ! y se le da forma
```

`[(expresión, variable = inicio, fin, paso)]` es una **comprensión de lista** —tema de la clase 067—
con sintaxis de 1990. Se evalúa entera, no perezosamente.

Y donde Fortran sí tiene algo parecido a la pereza es en un sitio inesperado: **la evaluación de
expresiones de array**. Cuando escribes `c = a + b * 2`, un compilador optimizador **no** construye el
array intermedio `b * 2`: fusiona las dos operaciones en un solo recorrido. Es *fusión de bucles*, y
tiene el mismo efecto que la pereza —evitar materializar resultados intermedios— pero obtenido por el
compilador en lugar de por el programador.

Es lo mismo que buscan los *ranges* de C++20 y los iteradores encadenados de Rust: **componer sin
materializar**.
"""),
        "ada": ("""
with Ada.Text_IO;           use Ada.Text_IO;
with Ada.Integer_Text_IO;   use Ada.Integer_Text_IO;
with Ada.Strings;           use Ada.Strings;
with Ada.Strings.Fixed;
with Ada.Strings.Unbounded; use Ada.Strings.Unbounded;

procedure Pares is
   N   : Integer;
   Sec : Unbounded_String := Null_Unbounded_String;
begin
   Get (N);

   for I in 1 .. N loop
      if I > 1 then
         Append (Sec, "-");
      end if;
      Append (Sec, Ada.Strings.Fixed.Trim (Integer'Image (2 * I), Both));
   end loop;

   Put_Line ("pares=" & To_String (Sec));
end Pares;
""", """
**Lo que esta clase enseña en Ada.** Ada no tiene `yield`, pero tiene algo que ningún otro lenguaje de
esta página ofrece y que resuelve el mismo problema desde otro ángulo: **las tareas y las citas**.

```ada
task Generador is
   entry Siguiente (V : out Integer);
end Generador;

task body Generador is
begin
   for I in 1 .. 1000 loop
      accept Siguiente (V : out Integer) do    --  se BLOQUEA hasta que alguien pida
         V := 2 * I;
      end Siguiente;
   end loop;
end Generador;

--  Y en el consumidor:
Generador.Siguiente (Valor);
```

La tarea se queda **detenida en el `accept`** hasta que alguien llama a `Siguiente`, entrega el valor
y continúa su bucle hasta el siguiente `accept`. **Es exactamente la semántica de un generador**:
producción suspendida y reanudada bajo demanda.

La diferencia con `yield` es que aquí hay un **hilo de verdad** y una sincronización real, con su
coste. Un generador de Python o una corrutina de Tcl se suspenden dentro del mismo hilo. Ada eligió
resolverlo con concurrencia porque la concurrencia estaba en el lenguaje desde 1983, y en un sistema
de tiempo real la cita tiene garantías temporales analizables que un generador no da.

Ada 2012 añadió además las **interfaces de iterador**, que permiten `for X of Coleccion loop` sobre
tipos propios, y con ellas se puede construir un iterador perezoso sin tareas.
"""),
        "pascal": ("""
program Pares;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N, I: Integer;
  Sec: string;

begin
  Read(N);

  Sec := '';
  for I := 1 to N do
  begin
    if I > 1 then Sec := Sec + '-';
    Sec := Sec + IntToStr(2 * I);
  end;

  WriteLn('pares=', Sec);
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal **no tiene generadores**, y su respuesta a esta clase
es el patrón **enumerador**: un objeto con estado que sabe avanzar y entregar el actual.

```pascal
type
  TParesEnumerador = class
  private
    FActual, FLimite: Integer;
  public
    constructor Create(Limite: Integer);
    function MoveNext: Boolean;
    property Current: Integer read FActual;
  end;

function TParesEnumerador.MoveNext: Boolean;
begin
  Inc(FActual, 2);
  Result := FActual <= FLimite * 2;
end;
```

Con `MoveNext` y `Current`, y una función `GetEnumerator` en la clase contenedora, **`for..in`
funciona sobre tu tipo**. Es el mismo contrato de C#, de Java y de Ada 2012.

La diferencia con un generador de verdad está en quién guarda el estado: aquí, **campos de un objeto
que tú declaras**; con `yield`, la **posición dentro del bucle**, que el compilador guarda por ti.
Cuando la lógica de producción es un bucle anidado con condiciones, escribir el enumerador a mano es
considerablemente más difícil que poner `yield` en medio.

Free Pascal tiene además **hilos ligeros y corrutinas** en bibliotecas de la comunidad, pero no en el
lenguaje. Delphi introdujo `TEnumerator<T>` genérico, que es el mismo patrón con tipos.
"""),
        "lisp": ("""
(let ((n (read)))
  (format t "pares=~{~D~^-~}~%" (loop for i from 1 to n collect (* 2 i))))
""", """
**Lo que esta clase enseña en Common Lisp.** El estándar **no tiene generadores**, y la comunidad
resolvió la pereza de tres maneras distintas, todas **sin cambiar el lenguaje**:

**1) La clausura con estado**, que es el generador manual y funciona en cualquier Lisp:

```lisp
(defun generador-pares (n)
  (let ((i 0))
    (lambda ()
      (when (< i n)
        (incf i)
        (* 2 i)))))

(let ((sig (generador-pares 5)))
  (loop for v = (funcall sig) while v collect v))   ; (2 4 6 8 10)
```

**2) Las listas perezosas** al estilo de Scheme, con `delay` y `force` implementados como macros. La
biblioteca `SERIES` llega a compilar expresiones sobre secuencias perezosas **a bucles sin estructuras
intermedias**, que es la fusión de bucles de Fortran obtenida en tiempo de macroexpansión.

**3) Las corrutinas**, disponibles en bibliotecas como `cl-cont` mediante **transformación a estilo de
paso de continuaciones** — otra vez, macros reescribiendo el código.

Que las tres sean bibliotecas y no características del lenguaje es la tesis de la clase 041 llevada
hasta el final: **cuando el lenguaje permite extender su propia sintaxis, la frontera entre "lo que
trae el lenguaje" y "lo que trae una biblioteca" deja de ser interesante**.

Y `~{~D~^-~}` resuelve el separador: itera sobre la lista y `~^` corta antes del último guion.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

coroutine pares apply {{n} {
    yield
    for {set i 1} {$i <= $n} {incr i} {
        yield [expr {2 * $i}]
    }
    return ""
}} $n

set salida {}
for {set k 1} {$k <= $n} {incr k} {
    lappend salida [pares]
}

puts "pares=[join $salida -]"
""", """
**Lo que esta clase enseña en Tcl.** **Esta es la única implementación de esta página con un generador
de verdad, y funciona: se ejecuta en CI.**

`coroutine pares apply {...} $n` crea una corrutina: el cuerpo empieza a ejecutarse **hasta el primer
`yield`**, que lo suspende y devuelve el control. A partir de ahí, cada vez que se invoca `pares`
—como si fuera un comando— la corrutina **se reanuda exactamente donde estaba**, dentro del `for`,
produce el siguiente valor con `yield` y vuelve a suspenderse.

Es la misma semántica que `yield` en Python, `yield return` en C# o las corrutinas de Kotlin. Tcl las
tiene desde la **versión 8.6, de 2012**.

Y lo notable es cómo están implementadas: **una corrutina de Tcl es una pila de ejecución
independiente** gestionada por el intérprete, no un hilo del sistema operativo. Crear una cuesta
microsegundos y hay quien mantiene decenas de miles vivas a la vez.

De ahí sale el uso real: combinadas con `fileevent` y la E/S no bloqueante de la clase 056, permiten
escribir código **asíncrono con forma secuencial** —sin el infierno de retrollamadas— quince años
antes de que `async`/`await` llegara a JavaScript, C# o Python:

```tcl
coroutine cliente apply {{sock} {
    set linea [yieldto gets $sock]   ;# parece bloqueante, no lo es
    ...
}} $canal
```
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

#  Un generador: una clausura que guarda su estado entre llamadas.
my $i = 0;
my $siguiente = sub { return ++$i <= $n ? 2 * $i : undef };

my @salida;
while (defined(my $v = $siguiente->())) {
    push @salida, $v;
}

print "pares=", join('-', @salida), "\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl no tiene `yield`, y su respuesta es la **clausura con
estado**: una función anónima que **captura** las variables de su entorno y las conserva entre
llamadas.

`$i` está declarada fuera de `sub { }`, pero la subrutina la **captura por referencia**, así que
sobrevive mientras la clausura exista y mantiene su valor de una invocación a otra. Es un generador
con todas las letras: estado privado, producción bajo demanda, sin construir la lista completa.

La forma canónica encapsula el estado dentro:

```perl
sub generador_pares {
    my ($n) = @_;
    my $i = 0;
    return sub { return ++$i <= $n ? 2 * $i : undef };   # $i queda ATRAPADA aquí
}

my $sig = generador_pares(5);
while (defined(my $v = $sig->())) { ... }
```

Cada llamada a `generador_pares` crea **un `$i` nuevo**, así que dos generadores no se pisan. Ese es
el mecanismo con el que se construyen iteradores, contadores, cachés y objetos sin clases en
cualquier lenguaje con clausuras — JavaScript vive de esto.

Y Perl tiene pereza integrada en un sitio muy usado: **el operador de rango en un `foreach` no
materializa la lista**. `for (1 .. 1_000_000_000)` no reserva mil millones de elementos; itera. Es la
misma optimización que `range` de Python 3.
"""),
        "cpp": ("""
#include <iostream>
#include <string>

//  Un generador escrito a mano: un objeto que guarda su estado.
struct Pares {
    int i = 0;
    int n;
    explicit Pares(int limite) : n(limite) {}

    bool siguiente(int& v) {
        if (i >= n) return false;
        ++i;
        v = 2 * i;
        return true;
    }
};

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    Pares gen(n);
    std::string salida;
    int v{};
    while (gen.siguiente(v)) {
        if (!salida.empty()) salida += '-';
        salida += std::to_string(v);
    }

    std::cout << "pares=" << salida << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** Hasta C++20, la única forma era la de este programa: **un objeto
que guarda su estado a mano**, con un método para avanzar. Es el patrón enumerador de Pascal y de C#,
escrito explícitamente.

C++20 añadió las **corrutinas** de verdad, con `co_yield`, y el resultado es mucho más directo:

```cpp
std::generator<int> pares(int n) {          // std::generator es de C++23
    for (int i = 1; i <= n; ++i) {
        co_yield 2 * i;                     // suspende aquí y devuelve el valor
    }
}

for (int v : pares(5)) { ... }
```

Y los **rangos** de C++20 dan pereza componible sin escribir ninguna corrutina:

```cpp
#include <ranges>
auto pares = std::views::iota(1, n + 1)
           | std::views::transform([](int i) { return 2 * i; });
```

Ese `|` encadena **vistas perezosas**: nada se calcula hasta que alguien recorre el resultado, y **no
se construye ningún vector intermedio**. Es la fusión de bucles de la que hablaba la ficha de Fortran,
obtenida en la biblioteca mediante plantillas.

Compilar este programa con `-std=c++17` obliga a la versión manual, y esa es justamente la lección:
**la diferencia entre las dos formas es enteramente de expresividad**. Las dos hacen lo mismo y una se
lee.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi PARES;
  n int(10) const;
end-pi;

dcl-s i      int(10);
dcl-s sec    varchar(500) inz('');
dcl-s salida char(520);

for i = 1 to n;
  if i > 1;
    sec += '-';
  endif;
  sec += %char(2 * i);
endfor;

salida = 'pares=' + sec;
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG no tiene generadores ni corrutinas. Pero es el lenguaje de
esta página que mejor ilustra **el otro modelo de pereza**, el de *empujar*.

Con un fichero declarado como **entrada primaria**, el **ciclo del programa** hace el bucle: lee un
registro, ejecuta tu lógica, comprueba los cambios de nivel de control, imprime totales y vuelve a
empezar. **Tú no pides el siguiente registro: el runtime te lo entrega.**

```text
     FVENTAS    IP   E             DISK
     FINFORME   O    E             PRINTER
```

Eso es **inversión de control**, y la diferencia con un iterador es dónde vive el bucle:

| | Quién tiene el bucle | Ejemplos |
|---|---|---|
| **Tirar** (*pull*) | El **consumidor** | Iteradores, generadores, `$order` de M, `READ` de COBOL |
| **Empujar** (*push*) | El **productor** | Ciclo de RPG, eventos, `Observer`, flujos reactivos |

El modelo *push* es el de todos los marcos de trabajo modernos —tú escribes el manejador y el
framework llama— y el de la programación reactiva. Que RPG lo tuviera en 1959, con el nombre de
"ciclo del programa", es de las cosas más sorprendentes de toda esta sección.

Su inconveniente es el mismo que hoy: **si el bucle no es tuyo, salirte de él es difícil**. De ahí los
indicadores `*INLR` y `*INRT`, que existen precisamente para decirle al ciclo qué hacer, y de ahí que
el RPG moderno con `main()` prescinda de él.
"""),
        "pli": ("""
 pares: procedure options(main);

    declare n   fixed binary(31);
    declare i   fixed binary(31);
    declare sec character(500) varying initial('');

    get list (n);

    do i = 1 to n;
       if i > 1 then sec = sec || '-';
       sec = sec || trim(char(2 * i));
    end;

    put skip list ('pares=' || sec);

 end pares;
""", """
**Lo que esta clase enseña en PL/I.** PL/I no tiene generadores, pero tiene **multitarea desde 1964**,
y con ella se puede construir el mismo esquema productor-consumidor que Ada resuelve con tareas y
citas:

```pli
declare productor entry;

call productor task(t1) event(listo);   /* arranca una TAREA */
wait(listo);                            /* espera al suceso */
```

`task`, `event` y `wait` son parte del lenguaje. Es concurrencia con sincronización por sucesos,
veinte años antes que Ada y treinta antes que Java.

Y hay una construcción de PL/I que se acerca todavía más a la suspensión y reanudación de un
generador: **las condiciones `ON` con reanudación**, que ya aparecieron en la clase 049.

```pli
on conversion begin;
   onsource() = '0';   /* CORRIGE el dato... */
end;                    /* ...y la operación CONTINÚA donde estaba */
```

El manejador se ejecuta **encima de la pila del punto que falló**, arregla la situación y devuelve el
control ahí mismo. Eso es exactamente lo que hace un `yield` visto al revés: el control salta a otro
sitio y **vuelve al punto exacto**.

Es la misma capacidad que el sistema de condiciones y reinicios de Common Lisp, y la razón de que
ambos aparezcan citados cuando se habla de que el `try/catch` moderno perdió algo por el camino: al
desenrollar la pila antes de manejar el error, se pierde la posibilidad de reanudar.
"""),
        "mumps": ("""
PARES ; Pares -- clase 066
 read n
 set sec = ""
 for i = 1:1:n do
 . set:sec'="" sec = sec _ "-"
 . set sec = sec _ (2 * i)
 write "pares=", sec, !
 quit
""", """
**Lo que esta clase enseña en M.** M no tiene generadores como construcción, pero **`$order` es un
iterador perezoso de verdad** y merece verse en esta clase, porque su comportamiento es idéntico al de
un generador:

```mumps
 set clave = ""
 for  set clave = $order(^PACIENTE(clave))  quit:clave = ""  do
 . ; procesar UN paciente
```

Cada llamada a `$order` **devuelve la siguiente clave existente** y nada más. No hay lista, no hay
cursor que abrir, no hay conjunto de resultados en memoria. Sobre un *global* de diez millones de
nodos, el consumo de memoria es constante y el coste de cada paso es una búsqueda en el índice.

Y tiene una propiedad que los generadores de los lenguajes modernos **no** tienen: **es reanudable
entre procesos y entre ejecuciones**. La "posición" del iterador es simplemente el valor de `clave`,
un dato normal. Se puede guardar en disco, apagar el programa, y continuar el recorrido tres días
después desde otro proceso:

```mumps
 set ^ESTADO("ultimo") = clave      ; guardar por dónde iba
 ; ... y en otra ejecución:
 set clave = $get(^ESTADO("ultimo"))
```

Eso es imposible con un generador de Python o una corrutina de Tcl, cuyo estado es una pila viva en
memoria. Aquí el estado del recorrido es **un valor**, no una continuación — y por eso los procesos
por lotes de un sistema clínico pueden reanudarse tras una caída sin perder el sitio.
"""),
        "smalltalk": ("""
| n sec |

n := stdin nextLine trimBoth asNumber.

sec := String streamContents: [ :flujo |
    (1 to: n)
        do:          [ :i | flujo print: 2 * i ]
        separatedBy: [ flujo nextPut: $- ] ].

Transcript show: 'pares=', sec; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Pharo **sí tiene generadores**, y su implementación es una
de las cosas más elegantes de esta página. La clase `Generator` permite escribir:

```smalltalk
| gen |
gen := Generator on: [ :productor |
    1 to: n do: [ :i | productor yield: 2 * i ] ].

gen next.        "2"
gen next.        "4"
gen upToEnd.     "el resto"
```

`yield:` suspende el bloque y devuelve el valor; `next` lo reanuda donde estaba. Es la misma
semántica que la corrutina de Tcl o el `yield` de Python.

Y lo notable es **cómo está implementado**: usando **continuaciones**, que en Smalltalk se obtienen
manipulando el objeto `thisContext` —la pila de ejecución, que **es un objeto normal e
inspeccionable**—. `Generator` no es una característica del compilador ni una palabra clave: es una
clase de biblioteca de unas cien líneas que reifica la pila.

Ese es el techo de lo que permite un lenguaje donde todo es un objeto, **incluida la propia
ejecución**. Con `thisContext` se pueden construir generadores, corrutinas, continuaciones,
depuradores que reanudan y —el caso famoso— el framework web **Seaside**, que usa continuaciones para
que un flujo de varias páginas se escriba como una función secuencial, sin máquina de estados.

Y `String streamContents:` de este programa es el `WriteStream` de la clase 054: un flujo de
escritura, la contrapartida del de lectura.
"""),
    },
)

# ---------------------------------------------------------------------------
# 067 — Comprensiones de listas y colecciones
# ---------------------------------------------------------------------------
SPECS["067"] = dict(
    gancho="""
Quedarse con los pares de una lista. Una **comprensión** dice *qué* quieres —"los elementos que
cumplen esto"— en lugar de *cómo* recorrerlos. Y la pregunta de esta página es cuántos de estos
lenguajes pueden expresarlo así, sin escribir el bucle. La respuesta sorprende: **Fortran sí, y desde
1990**.
""",
    porque="""
Aquí el concepto es **describir una colección derivada en lugar de construirla paso a paso**, y estos
lenguajes lo enseñan por dos motivos opuestos. El primero: **Fortran tiene `pack`**, una intrínseca
que filtra un array con una máscara lógica, y constructores con bucle implícito `[(expr, i = 1, n)]`
que son literalmente comprensiones. No fue un préstamo de los funcionales: llegó por la necesidad de
vectorizar.

El segundo: **COBOL, RPG y PL/I no tienen nada de esto**, y ver el bucle escrito a mano al lado de la
versión de una línea es la mejor demostración de qué aporta la abstracción. Y Smalltalk enseña que
`select:` no es sintaxis: es un método de `Collection` que cualquiera puede leer.
""",
    cierre="""
Lo transferible: **una comprensión separa el qué del cómo, y eso permite que el "cómo" cambie sin
tocar tu código**. `pack` de Fortran puede vectorizarse, `select:` de Smalltalk puede estar
implementado con un índice, y un `filter` perezoso puede no materializar nada. Cuando escribes el
bucle a mano, congelas la estrategia. Es la misma razón por la que se prefiere SQL a recorrer una
tabla: **declarar deja margen a quien ejecuta**.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. PARES.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  I       PIC 9(4)  COMP-3.
01  LARGO   PIC 9(4)  COMP-3.
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(4)  COMP-3.
01  C       PIC X.
01  V       PIC S9(9) COMP-3.
01  ED-V    PIC -(9)9.
01  TROZO   PIC X(20).
01  TROZO-L PIC 9(4)  COMP-3.
01  SEC     PIC X(400).
01  PTR     PIC 9(4)  COMP-3.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE SPACES TO SEC
    MOVE 1 TO PTR
    MOVE SPACES TO TOKEN
    MOVE 0 TO TLEN
    COMPUTE LARGO = FUNCTION LENGTH(FUNCTION TRIM(LINEA)) + 1

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > LARGO
        MOVE LINEA(I:1) TO C
        IF C = SPACE
            IF TLEN > 0
                MOVE FUNCTION NUMVAL(TOKEN(1:TLEN)) TO V
                IF FUNCTION MOD(V, 2) = 0
                    MOVE V TO ED-V
                    MOVE FUNCTION TRIM(ED-V) TO TROZO
                    COMPUTE TROZO-L = FUNCTION LENGTH(FUNCTION TRIM(TROZO))
                    IF PTR > 1
                        MOVE "-" TO SEC(PTR:1)
                        ADD 1 TO PTR
                    END-IF
                    MOVE TROZO(1:TROZO-L) TO SEC(PTR:TROZO-L)
                    ADD TROZO-L TO PTR
                END-IF
                MOVE SPACES TO TOKEN
                MOVE 0 TO TLEN
            END-IF
        ELSE
            ADD 1 TO TLEN
            MOVE C TO TOKEN(TLEN:1)
        END-IF
    END-PERFORM

    DISPLAY "pares=" FUNCTION TRIM(SEC)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** Treinta líneas para lo que en Perl es `grep { !($_ % 2) }`.
Y no es un defecto de COBOL: es **exactamente la medida de lo que aporta una comprensión**. Todo lo
que se ve aquí —el tokenizador, el índice del acumulador, el separador condicional— es *cómo*, y la
única línea que dice *qué* es la del `MOD`.

COBOL no tiene comprensiones, ni funciones de orden superior, ni colecciones de tamaño variable. Lo
más cerca que llega es **`SEARCH`** sobre una tabla, que expresa "encuentra el que cumpla" sin
escribir el bucle:

```cobol
SEARCH ELEMENTO VARYING I
    AT END      DISPLAY "ninguno"
    WHEN FUNCTION MOD(ELEMENTO(I), 2) = 0 DISPLAY "el primero par es " ELEMENTO(I)
END-SEARCH
```

Es un `find_if`, no un `filter`: devuelve el primero, no todos.

Y donde el COBOL de producción **sí** hace comprensiones es delegando en otro lenguaje:

```cobol
EXEC SQL
    SELECT IMPORTE INTO :WS-TABLA
      FROM MOVIMIENTOS
     WHERE MOD(IMPORTE, 2) = 0
END-EXEC
```

Ahí está el reparto real de trabajo en un sistema mainframe: **COBOL lleva la lógica de negocio y SQL
lleva las operaciones sobre conjuntos**. Es la misma división que en IBM i entre RPG y Db2, y explica
por qué a estos lenguajes nunca les hizo falta un `filter`.
"""),
        "fortran": ("""
program pares
   implicit none
   character(len=1000) :: linea
   integer :: v(200), n, i, ios
   integer, allocatable :: filtrados(:)
   character(len=:), allocatable :: sec
   character(len=16) :: buf

   read(*, '(A)') linea

   n = 0
   do i = 1, 200
      read(linea, *, iostat=ios) v(1:i)
      if (ios /= 0) exit
      n = i
   end do

   !  pack: se queda con los elementos donde la MÁSCARA es cierta.
   filtrados = pack(v(1:n), mod(v(1:n), 2) == 0)

   sec = ''
   do i = 1, size(filtrados)
      write(buf, '(I0)') filtrados(i)
      if (i > 1) sec = sec // '-'
      sec = sec // trim(buf)
   end do

   write(*, '(A,A)') 'pares=', sec
end program pares
""", """
**Lo que esta clase enseña en Fortran.** **`pack(v, mascara)` es un `filter`, y está en el lenguaje
desde Fortran 90.** `mod(v, 2) == 0` sobre un array no devuelve un booleano: devuelve **un array de
lógicos**, la máscara, y `pack` se queda con los elementos donde es cierta.

Y no llegó por influencia de los lenguajes funcionales, sino por la necesidad de **vectorizar**: una
operación sobre el array completo se compila a instrucciones SIMD, y un bucle con `if` dentro no.

La familia es amplia y merece conocerse aunque no se programe en Fortran:

```fortran
pack(v, v > 0)                  ! filter
unpack(comprimido, mascara, 0)  ! la operación inversa
merge(a, b, mascara)            ! elegir elemento a elemento
count(v > 0)                    ! cuántos cumplen
sum(v, mask = v > 0)            ! ¡sumar SOLO los que cumplen!
maxval(v, mask = v < 100)
```

Ese `mask =` opcional en `sum`, `product`, `maxval`, `minval` y `count` es la comprensión completa
—filtrar y agregar— en una sola llamada.

Y el constructor con bucle implícito es la otra mitad, el `map`:

```fortran
cuadrados = [(i * i, i = 1, 10)]
pares = [(2 * i, i = 1, n)]
filtrado = [(v(i), i = 1, n, 1)]     ! y con una condición, vía pack
```

`[(expresión, variable = inicio, fin)]` es sintácticamente **una comprensión de listas**, con la
sintaxis de 1990 y sin haber tomado nada prestado de Haskell ni de Python.
"""),
        "ada": ("""
with Ada.Text_IO;           use Ada.Text_IO;
with Ada.Integer_Text_IO;   use Ada.Integer_Text_IO;
with Ada.Strings;           use Ada.Strings;
with Ada.Strings.Fixed;
with Ada.Strings.Unbounded; use Ada.Strings.Unbounded;

procedure Pares is
   Linea  : String (1 .. 500);
   Ultimo : Natural;
   Pos    : Positive := 1;
   Fin    : Positive;
   Valor  : Integer;
   Sec    : Unbounded_String := Null_Unbounded_String;
begin
   Get_Line (Linea, Ultimo);

   while Pos <= Ultimo loop
      Get (Linea (Pos .. Ultimo), Valor, Fin);
      if Valor mod 2 = 0 then
         if Length (Sec) > 0 then
            Append (Sec, "-");
         end if;
         Append (Sec, Ada.Strings.Fixed.Trim (Integer'Image (Valor), Both));
      end if;
      Pos := Fin + 1;
   end loop;

   Put_Line ("pares=" & To_String (Sec));
end Pares;
""", """
**Lo que esta clase enseña en Ada.** Ada 83, 95, 2005 y 2012 **no tienen comprensiones**: el bucle se
escribe. Pero **Ada 2022 sí las añadió**, y su forma es notablemente limpia:

```ada
--  Comprensión con filtro (Ada 2022)
Pares : constant Vector := [for E of Datos when E mod 2 = 0 => E];

--  Con transformación
Cuadrados : constant Vector := [for I in 1 .. 10 => I * I];

--  Y sobre un mapa
Nombres : constant Map := [for C of Clientes => C.Id => C.Nombre];
```

`[for ... when ... => ...]` es exactamente la comprensión de Python con otra puntuación, y llegó a un
lenguaje de 1983 **en 2022**.

Fíjate en el `constant`: eso es lo que hace valiosa la comprensión en Ada, y es el mismo argumento de
la clase 060. Con un bucle, la colección se declara vacía y se rellena, así que **no puede ser
constante**. Con la comprensión, se construye completa en la declaración y queda sellada. La
expresividad no es el objetivo principal — lo es poder declarar más cosas inmutables.

Mientras tanto, la biblioteca estándar ofrece los contenedores genéricos —`Ada.Containers.Vectors`,
`Doubly_Linked_Lists`, `Hashed_Maps`, `Ordered_Sets`— con operaciones como `Iterate` y `Query_Element`
que cubren el recorrido, y con `Ada.Containers.Generic_Array_Sort` para ordenar.
"""),
        "pascal": ("""
program Pares;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, Token, Sec: string;
  I, V: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea) + ' ';

  Sec := '';
  Token := '';
  for I := 1 to Length(Linea) do
  begin
    if Linea[I] = ' ' then
    begin
      if Token <> '' then
      begin
        V := StrToInt(Token);
        if (V mod 2) = 0 then
        begin
          if Sec <> '' then Sec := Sec + '-';
          Sec := Sec + IntToStr(V);
        end;
        Token := '';
      end;
    end
    else
      Token := Token + Linea[I];
  end;

  WriteLn('pares=', Sec);
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal **no tiene comprensiones ni funciones de orden
superior** en su forma clásica, y este bucle es el resultado. Es el mismo trabajo manual que en
COBOL, con menos ceremonia.

Lo que sí tiene, y lleva desde 1970, son los **conjuntos** de la clase 062:

```pascal
if C in ['a'..'z', 'A'..'Z'] then ...
```

Un conjunto es la mitad de una comprensión: expresa **la pertenencia** sin bucle, aunque no permite
derivar una colección de otra. Y está limitado a tipos ordinales pequeños, porque se implementa como
máscara de bits.

Delphi y Free Pascal modernos añadieron genéricos y métodos anónimos, y con ellos aparecieron
bibliotecas que sí traen el vocabulario funcional:

```pascal
uses Spring.Collections;      { biblioteca de la comunidad }

Pares := Datos.Where(function(const X: Integer): Boolean
                     begin Result := X mod 2 = 0; end);
```

La verbosidad de esa lambda —`function(const X: Integer): Boolean begin ... end`— explica por qué el
estilo funcional nunca arraigó en el mundo Pascal: **sin sintaxis ligera para las funciones anónimas,
el bucle explícito sale más corto**. Es la misma razón por la que Java tardó hasta la versión 8 en
adoptarlo y C++ hasta C++11: la comprensión necesita que pasar código sea barato de escribir.
"""),
        "lisp": ("""
(let ((lista (loop for v = (read *standard-input* nil :fin)
                   until (eq v :fin)
                   collect v)))
  (format t "pares=~{~D~^-~}~%" (remove-if-not #'evenp lista)))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp tiene **dos formas** de expresar esta clase, y las
dos son de biblioteca, no de sintaxis.

La primera son las **funciones de secuencia**, que funcionan sobre listas, vectores y cadenas por
igual:

```lisp
(remove-if-not #'evenp lista)      ; los que cumplen
(remove-if #'evenp lista)          ; los que NO
(mapcar #'1+ lista)                ; map
(count-if #'plusp lista)
(find-if #'zerop lista)
(sort (copy-seq lista) #'<)
```

La convención `-if` / `-if-not` recorre toda la biblioteca y es muy uniforme: `remove-if`,
`delete-if`, `count-if`, `find-if`, `position-if`, `substitute-if`.

La segunda es **`loop` con `collect` y `when`**, que es literalmente una comprensión:

```lisp
(loop for x in lista when (evenp x) collect x)
(loop for x in lista collect (* x x))
(loop for x in lista for y in otra collect (+ x y))    ; dos listas a la vez
(loop for x in lista when (plusp x) sum x)             ; filtrar Y agregar
```

`for ... when ... collect` es exactamente `[x for x in lista if x % 2 == 0]` de Python, con otra
puntuación y quince años antes.

Y —esto es lo importante— **`loop` es una macro**. Alguien implementó un lenguaje de comprensión
entero como biblioteca, sin tocar el compilador. Es la respuesta de Lisp a por qué nunca necesitó que
el comité añadiera comprensiones: **cuando aparecen, se escriben**.
"""),
        "tcl": ("""
gets stdin linea

set pares {}
foreach v [split [string trim $linea]] {
    if {$v % 2 == 0} {
        lappend pares $v
    }
}

puts "pares=[join $pares -]"
""", """
**Lo que esta clase enseña en Tcl.** Tcl 8.6 añadió **`lmap`**, que es el `map` con sintaxis de
bucle, y con él la comprensión se escribe en una línea:

```tcl
set pares [lmap v [split [string trim $linea]] {
    expr {$v % 2 == 0 ? $v : [continue]}
}]
```

Ese `[continue]` dentro de `lmap` es el truco idiomático para **filtrar**: `continue` salta la
iteración y **no añade nada al resultado**. Es feo y es la única forma, porque `lmap` es un `map` y
Tcl no tiene `lfilter`.

Para filtrar de verdad, la biblioteca **Tcllib** trae `struct::list`:

```tcl
package require struct::list
set pares [struct::list filter $lista {apply {{v} {expr {$v % 2 == 0}}}}]
set dobles [struct::list map $lista {apply {{v} {expr {$v * 2}}}}]
set total [struct::list fold $lista 0 {apply {{a b} {expr {$a + $b}}}}]
```

La verbosidad de `{apply {{v} {...}}}` es la misma barrera que en Pascal: **sin sintaxis ligera para
las funciones anónimas, el bucle explícito gana**. Por eso el `foreach` de este programa es lo que un
programador de Tcl escribiría de verdad.

Y hay una tercera vía muy propia del lenguaje, que aprovecha que las listas son cadenas: para
operaciones sobre listas grandes, `lsearch -all -inline` con `-regexp` filtra sin bucle y en C.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

my @pares = grep { $_ % 2 == 0 } split ' ', $linea;

print "pares=", join('-', @pares), "\\n";
""", """
**Lo que esta clase enseña en Perl.** `grep { condición } lista` es el filtro, y su nombre viene
directamente de la herramienta de Unix. Junto a `map` forma el vocabulario básico, y las dos se
encadenan de derecha a izquierda como las tuberías del shell:

```perl
my @resultado = map { $_ * 2 }
                grep { $_ % 2 == 0 }
                split ' ', $linea;
```

Se lee de abajo arriba: parte, filtra, transforma. Es una comprensión sin sintaxis especial, porque
en Perl **un bloque es un argumento normal** y no hace falta escribir `sub { }`.

Dos detalles importantes de esta clase. El primero: **`$_` en `grep` y `map` es un alias, no una
copia**, igual que en el `foreach` de la clase 064. Modificarlo dentro del bloque **cambia la lista
original**:

```perl
my @x = map { $_ * 2 } @lista;      # correcto: no toca @lista
my @y = map { $_ *= 2 } @lista;     # ¡MODIFICA @lista!
```

El segundo: **`map` puede devolver cualquier número de elementos por entrada**, no solo uno. Ese es
su superpoder frente al `map` de otros lenguajes:

```perl
my @pares = map { $_ % 2 == 0 ? ($_) : () } @lista;   # map haciendo de filtro
my %h = map { $_ => 1 } @lista;                        # lista -> hash
my @dobles = map { ($_, $_) } @lista;                  # cada uno DOS veces
```

Devolver la lista vacía elimina el elemento; devolver dos lo duplica. `map` de Perl es en realidad un
`flatMap`, y por eso puede hacer de `filter` y de constructor de hash a la vez.
"""),
        "cpp": ("""
#include <iostream>
#include <iterator>
#include <sstream>
#include <string>
#include <vector>

int main() {
    std::string linea;
    if (!std::getline(std::cin, linea)) return 1;

    std::istringstream iss(linea);
    const std::vector<int> v{std::istream_iterator<int>(iss),
                             std::istream_iterator<int>()};

    std::string sec;
    for (int x : v) {
        if (x % 2 != 0) continue;
        if (!sec.empty()) sec += '-';
        sec += std::to_string(x);
    }

    std::cout << "pares=" << sec << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** Hasta C++20 no había comprensiones, y la forma de la STL era
`std::copy_if` con un iterador de inserción:

```cpp
std::vector<int> pares;
std::copy_if(v.begin(), v.end(), std::back_inserter(pares),
             [](int x) { return x % 2 == 0; });
```

Funciona y es genérico, y tiene un problema: **cada paso materializa un vector**. Encadenar filtrar,
transformar y volver a filtrar crea tres vectores intermedios.

C++20 lo resolvió con los **rangos** y su operador de tubería, que es la comprensión de C++:

```cpp
#include <ranges>
auto pares = v | std::views::filter([](int x) { return x % 2 == 0; })
               | std::views::transform([](int x) { return x * 2; });

for (int x : pares) { ... }     // NADA se ha calculado hasta aquí
```

Esas vistas son **perezosas y componibles**: no construyen ningún contenedor intermedio, y el
recorrido final aplica las dos operaciones en una sola pasada. Es la fusión de bucles de la ficha de
Fortran, obtenida en la biblioteca mediante plantillas.

Y esa es la razón de que los rangos se consideren el cambio más importante de C++20: no añaden
capacidad —`copy_if` ya filtraba— sino que **eliminan el coste de componer**, que es lo que hacía que
en la práctica la gente escribiera bucles a mano.

Compilado con `-std=c++17`, este programa usa el bucle. Es exactamente la diferencia.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi PARES;
  linea varchar(200) const;
end-pi;

dcl-s trozos varchar(20) dim(50);
dcl-s i      int(10);
dcl-s v      int(10);
dcl-s sec    varchar(500) inz('');
dcl-s salida char(520);

trozos = %split(linea : ' ');

for i = 1 to %elem(trozos);
  v = %int(trozos(i));
  if %rem(v : 2) = 0;
    if sec <> '';
      sec += '-';
    endif;
    sec += %char(v);
  endif;
endfor;

salida = 'pares=' + sec;
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG no tiene comprensiones ni funciones de orden superior: no
hay forma de pasar un bloque de código como argumento. El filtro se escribe.

Y como en COBOL, **el filtrado de verdad en IBM i se delega en SQL**:

```rpgle
exec sql
  declare c1 cursor for
    select importe from movimientos
     where mod(importe, 2) = 0
     order by fecha;

exec sql open c1;
dow sqlcode = 0;
  exec sql fetch c1 into :importe;
  ...
enddo;
```

Ese reparto —RPG para la lógica, SQL para los conjuntos— es la arquitectura estándar de la plataforma
desde hace veinte años, y es el motivo de que a RPG nunca le hiciera falta un `filter`: **cuando los
datos están en una base de datos integrada en el sistema operativo, la comprensión la escribe el
motor**.

Y ahí hay una idea que va más allá de RPG: **SQL es una comprensión de listas**. `SELECT x FROM t
WHERE p` es exactamente `[x for x in t if p]`, y la cláusula `SELECT` es el `map`. La diferencia es
que el optimizador puede elegir la estrategia —índice, recorrido, orden de los filtros—, que es justo
el argumento de esta clase sobre separar el qué del cómo.
"""),
        "pli": ("""
 pares: procedure options(main);

    declare linea character(200) varying;
    declare trozo character(20)  varying;
    declare sec   character(500) varying initial('');
    declare (i, p, v) fixed binary(31);

    get edit (linea) (a(200));
    linea = trim(linea) || ' ';

    p = 1;
    do i = 1 to length(linea);
       if substr(linea, i, 1) = ' ' then do;
          if i > p then do;
             trozo = substr(linea, p, i - p);
             v = trozo;
             if mod(v, 2) = 0 then do;
                if sec ^= '' then sec = sec || '-';
                sec = sec || trim(char(v));
             end;
          end;
          p = i + 1;
       end;
    end;

    put skip list ('pares=' || sec);

 end pares;
""", """
**Lo que esta clase enseña en PL/I.** PL/I no tiene comprensiones, pero **sí tiene operaciones sobre
arrays completos**, heredadas de FORTRAN, y con ellas se puede expresar buena parte de esta clase sin
bucle:

```pli
declare v(100) fixed binary(31);
declare mascara(100) bit(1);

v = v * 2;                    /* map sobre todo el array */
mascara = (mod(v, 2) = 0);    /* la máscara, elemento a elemento */
total = sum(v);
if any(mascara) then ...
cuantos = sum(binary(mascara));   /* contar los ciertos */
```

Lo que falta es **`pack`**: PL/I puede calcular la máscara pero no comprimir el array quedándose solo
con los seleccionados. Esa intrínseca es específica de Fortran 90, y es justo la pieza que convierte
las operaciones de array en un `filter` de verdad.

PL/I tiene además una construcción para arrays que casi nadie recuerda y que viene al caso:

```pli
declare v(10) fixed binary(31) initial((10) 0);      /* factor de repetición */
declare w(5)  fixed binary(31) initial(1, 2, 3, 4, 5);
```

`(10) 0` significa "diez ceros". Es un constructor de array con repetición, la mitad de un
constructor por comprensión.

Y sobre `v = trozo` en el programa: es otra vez la conversión implícita de texto a número de la clase
050, funcionando en silencio hasta que el texto no es numérico.
"""),
        "mumps": ("""
PARES ; Comprension -- clase 067
 read linea
 set sec = ""
 for i = 1:1:$length(linea, " ") do
 . set v = $piece(linea, " ", i)
 . quit:v#2'=0
 . set:sec'="" sec = sec _ "-"
 . set sec = sec _ v
 write "pares=", sec, !
 quit
""", """
**Lo que esta clase enseña en M.** Fíjate en **`quit:v#2'=0`** dentro del bloque `do`: ese `quit`
**no sale de la rutina, sale de la iteración actual**. Es el `continue` de M, escrito como un
postcondicional.

Esa es la forma idiomática de filtrar en M: no hay `filter`, hay un `quit` condicional al principio
del cuerpo del bucle que descarta lo que no interesa. Se lee como una guarda —tema de la clase 058—
aplicada a cada vuelta.

M no tiene funciones de orden superior en el sentido habitual, **pero tiene indirección**, que da algo
parecido:

```mumps
 set filtro = "v#2=0"
 for i = 1:1:n do
 . set v = $piece(linea, " ", i)
 . quit:'@filtro          ; @ EVALÚA la cadena como código
 . ...
```

`@` es el operador de **indirección**: toma una cadena y la ejecuta como si fuera código. Con él se
puede pasar una condición —o un nombre de rutina— **como dato**, que es la mitad de lo que hace una
función de orden superior.

Es enormemente flexible y tiene el coste que cabe esperar: **un programa con indirección no se puede
analizar estáticamente**, porque qué se ejecuta se decide en tiempo de ejecución. Es el `eval` de
JavaScript con cincuenta años más, y con los mismos problemas de seguridad si la cadena viene de
fuera.
"""),
        "smalltalk": ("""
| pares |

pares := (stdin nextLine substrings collect: [ :cada | cada asNumber ])
    select: [ :cada | cada even ].

Transcript
    show: 'pares=', ((pares collect: [ :c | c printString ])
        inject: '' into: [ :acc :s | acc isEmpty ifTrue: [ s ] ifFalse: [ acc , '-' , s ] ]);
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** `select:` es el filtro y `collect:` el `map`, y los dos son
**métodos de `Collection`** que puedes abrir y leer:

```smalltalk
Collection >> select: unBloque
    | resultado |
    resultado := self species new.
    self do: [ :cada | (unBloque value: cada) ifTrue: [ resultado add: cada ] ].
    ^ resultado
```

Ocho líneas. **No hay sintaxis de comprensión porque no hace falta**: con bloques baratos de escribir
y `do:` implementado, todo el vocabulario funcional es biblioteca.

El protocolo completo es amplio y muy uniforme:

```smalltalk
coleccion select: [ :x | ... ]           "filter"
coleccion reject: [ :x | ... ]           "filter negado"
coleccion collect: [ :x | ... ]          "map"
coleccion detect: [ :x | ... ] ifNone: [ ... ]
coleccion inject: 0 into: [ :a :b | ... ]  "reduce"
coleccion count: [ :x | ... ]
coleccion anySatisfy: [ :x | ... ]
coleccion groupedBy: [ :x | ... ]        "agrupar en un diccionario"
coleccion sorted: [ :a :b | a < b ]
```

Y `self species new` en la implementación es un detalle elegante: **el resultado es del mismo tipo que
el receptor**. `select:` sobre un `Set` devuelve un `Set`, sobre una `OrderedCollection` devuelve una
`OrderedCollection`, y sobre un `String` devuelve un `String`. Es lo que en C++ se consigue con
plantillas y en Java no se consigue del todo.
"""),
    },
)

# ---------------------------------------------------------------------------
# 068 — Funciones de orden superior: map, filter, reduce
# ---------------------------------------------------------------------------
SPECS["068"] = dict(
    gancho="""
Doblar cada elemento y sumar los resultados. Un `map` seguido de un `reduce`, la pareja que sostiene
media programación moderna. Y la pregunta que reparte a estos lenguajes es más profunda de lo que
parece: **¿se puede pasar una función como argumento?** Porque si no se puede, `map` y `reduce`
sencillamente no existen.
""",
    porque="""
Aquí el concepto son las **funciones de orden superior**, y estos lenguajes lo enseñan porque cubren
las tres épocas. **Lisp las tiene desde 1958** —`mapcar` y `reduce` son la definición del
paradigma— y **Smalltalk desde los 70** con los bloques. En el otro extremo, **COBOL y RPG no pueden
pasar código como dato**, y por eso el bucle se escribe siempre.

Y en medio están los que las obtuvieron después: **Fortran 2003 con procedimientos como argumento**,
**Ada con genéricos y punteros a subprograma**, y **C++ con plantillas y lambdas** — tres formas
distintas de resolver el mismo problema, con y sin coste en ejecución.
""",
    cierre="""
Lo transferible es que **`map`/`filter`/`reduce` no son tres funciones: son la prueba de que el
lenguaje trata el código como un valor**. Cuando existen, aparecen solas todas las demás —`any`,
`all`, `count`, `sort` con comparador, `groupBy`— porque todas son la misma idea. Y cuando no
existen, no es que falten funciones: es que falta la capacidad, y ninguna biblioteca puede añadirla.
Es la diferencia entre COBOL y Lisp, y explica por qué Java tuvo que esperar a la versión 8.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. MAPRED.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  I       PIC 9(4)  COMP-3.
01  LARGO   PIC 9(4)  COMP-3.
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(4)  COMP-3.
01  C       PIC X.
01  V       PIC S9(9)  COMP-3.
01  D       PIC S9(9)  COMP-3.
01  ED-D    PIC -(9)9.
01  TROZO   PIC X(20).
01  TROZO-L PIC 9(4)  COMP-3.
01  SEC     PIC X(400).
01  PTR     PIC 9(4)  COMP-3.
01  TOTAL   PIC S9(18) COMP-3.
01  ED-T    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE SPACES TO SEC
    MOVE 1 TO PTR
    MOVE 0 TO TOTAL
    MOVE SPACES TO TOKEN
    MOVE 0 TO TLEN
    COMPUTE LARGO = FUNCTION LENGTH(FUNCTION TRIM(LINEA)) + 1

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > LARGO
        MOVE LINEA(I:1) TO C
        IF C = SPACE
            IF TLEN > 0
                MOVE FUNCTION NUMVAL(TOKEN(1:TLEN)) TO V
                COMPUTE D = V * 2
                ADD D TO TOTAL
                MOVE D TO ED-D
                MOVE FUNCTION TRIM(ED-D) TO TROZO
                COMPUTE TROZO-L = FUNCTION LENGTH(FUNCTION TRIM(TROZO))
                IF PTR > 1
                    MOVE "-" TO SEC(PTR:1)
                    ADD 1 TO PTR
                END-IF
                MOVE TROZO(1:TROZO-L) TO SEC(PTR:TROZO-L)
                ADD TROZO-L TO PTR
                MOVE SPACES TO TOKEN
                MOVE 0 TO TLEN
            END-IF
        ELSE
            ADD 1 TO TLEN
            MOVE C TO TOKEN(TLEN:1)
        END-IF
    END-PERFORM

    MOVE TOTAL TO ED-T
    DISPLAY "doblados=" FUNCTION TRIM(SEC)
            " total=" FUNCTION TRIM(ED-T)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** **En COBOL no se puede pasar una función como argumento**, y
por eso `map` y `reduce` no existen ni pueden escribirse. El bucle es la única forma.

Lo más cerca que llega es la llamada dinámica por nombre, que es potente y muy distinta:

```cobol
01  NOMBRE-PROGRAMA  PIC X(8) VALUE "CALCIVA".
...
CALL NOMBRE-PROGRAMA USING IMPORTE, RESULTADO
```

`CALL` con una **variable** en lugar de un literal resuelve el programa **en tiempo de ejecución**.
Cambiando el contenido de `NOMBRE-PROGRAMA` se llama a otra cosa. Eso permite tablas de despacho como
las de la clase 061 —una tabla de nombres de programa indexada por código de operación— y es la base
de la arquitectura de muchos sistemas transaccionales.

Es *casi* una función de primer orden: puedes elegir qué código ejecutar, guardándolo como dato. Lo
que no puedes es **crear** una función nueva, ni capturar variables del entorno, que es lo que
convierte a las clausuras en lo que son.

Y COBOL 2002 añadió `FUNCTION-ID` para definir funciones de usuario con valor de retorno, con lo que
al menos se pueden componer expresiones. Pero seguir sin poder pasarlas como argumento deja fuera
todo este paradigma.

Lo que hace COBOL en la práctica es lo de la clase anterior: **delegar en SQL** las operaciones sobre
conjuntos, donde `SUM`, `AVG` y `GROUP BY` son el `reduce` que el lenguaje no tiene.
"""),
        "fortran": ("""
program mapred
   implicit none
   character(len=1000) :: linea
   integer :: v(200), n, i, ios, total
   integer, allocatable :: doblados(:)
   character(len=:), allocatable :: sec
   character(len=16) :: buf

   read(*, '(A)') linea

   n = 0
   do i = 1, 200
      read(linea, *, iostat=ios) v(1:i)
      if (ios /= 0) exit
      n = i
   end do

   doblados = v(1:n) * 2      ! map: sobre el array completo
   total = sum(doblados)      ! reduce: intrínseca

   sec = ''
   do i = 1, size(doblados)
      write(buf, '(I0)') doblados(i)
      if (i > 1) sec = sec // '-'
      sec = sec // trim(buf)
   end do

   write(*, '(A,A,A,I0)') 'doblados=', sec, ' total=', total
end program mapred
""", """
**Lo que esta clase enseña en Fortran.** `doblados = v(1:n) * 2` es el `map` y `sum(doblados)` es el
`reduce`, **sin ninguna función de orden superior**. Fortran llegó al mismo destino por otro camino:
en vez de pasar una función a un recorrido, **hace que la operación se aplique al array entero**.

La diferencia es importante y sutil. Un `map` con función es **general**: acepta cualquier
transformación. La aritmética de arrays de Fortran solo cubre las operaciones que el lenguaje conoce.
A cambio, **se vectoriza**, cosa que una llamada indirecta a una función no puede hacer.

Y Fortran **sí** tiene funciones de orden superior desde F2003, aunque casi nadie las use:

```fortran
abstract interface
   pure function transformacion(x) result(y)
      integer, intent(in) :: x
      integer :: y
   end function
end interface

subroutine aplicar(v, f)
   integer, intent(inout) :: v(:)
   procedure(transformacion) :: f      ! ¡una FUNCIÓN como argumento!
   integer :: i
   do i = 1, size(v)
      v(i) = f(v(i))
   end do
end subroutine
```

`procedure(interfaz)` declara un parámetro que es un procedimiento, con su firma comprobada. Existe,
funciona, y **no se usa en código numérico** por una razón concreta: la llamada indirecta impide
integrar el cuerpo en línea y mata la vectorización. En un bucle de mil millones de vueltas, eso es
un factor de diez.

Es un buen recordatorio de que la elegancia y el rendimiento a veces apuntan en direcciones
distintas, y de que cada lenguaje elige.
"""),
        "ada": ("""
with Ada.Text_IO;           use Ada.Text_IO;
with Ada.Integer_Text_IO;   use Ada.Integer_Text_IO;
with Ada.Strings;           use Ada.Strings;
with Ada.Strings.Fixed;
with Ada.Strings.Unbounded; use Ada.Strings.Unbounded;

procedure Mapred is
   Linea  : String (1 .. 500);
   Ultimo : Natural;
   Pos    : Positive := 1;
   Fin    : Positive;
   Valor  : Integer;
   Doblado : Integer;
   Total  : Integer := 0;
   Sec    : Unbounded_String := Null_Unbounded_String;
begin
   Get_Line (Linea, Ultimo);

   while Pos <= Ultimo loop
      Get (Linea (Pos .. Ultimo), Valor, Fin);
      Doblado := Valor * 2;
      Total := Total + Doblado;
      if Length (Sec) > 0 then
         Append (Sec, "-");
      end if;
      Append (Sec, Ada.Strings.Fixed.Trim (Integer'Image (Doblado), Both));
      Pos := Fin + 1;
   end loop;

   Put ("doblados=" & To_String (Sec) & " total=");
   Put (Total, Width => 1);
   New_Line;
end Mapred;
""", """
**Lo que esta clase enseña en Ada.** Ada tiene funciones de orden superior desde el principio, pero
por una vía distinta de la habitual: **los genéricos**.

```ada
generic
   type Elemento is private;
   with function Transformar (X : Elemento) return Elemento;   --  ¡parámetro FUNCIÓN!
procedure Aplicar (V : in out Array_De (Elemento));
```

`with function` declara que el genérico recibe una función como parámetro, y la instanciación la fija
**en tiempo de compilación**:

```ada
procedure Doblar is new Aplicar (Integer, Por_Dos);   --  se resuelve al compilar
```

Es la misma técnica que las plantillas de C++, y tiene la misma propiedad: **coste cero en
ejecución**, porque no hay llamada indirecta. La función se integra en línea.

Ada 95 añadió además los **punteros a subprograma** —`access function (X : Integer) return Integer`—
que sí resuelven en ejecución, y Ada 2012 las **expresiones lambda**… bueno, casi: tiene funciones de
expresión, que son cuerpos de una sola expresión, pero **no clausuras anónimas**.

Esa ausencia es deliberada. Una clausura captura variables del entorno y las mantiene vivas más allá
del ámbito, lo que exige memoria dinámica y un tiempo de vida difícil de analizar. En un sistema que
debe certificarse, **eso es exactamente lo que no se quiere**. Ada prefiere el genérico, que se
resuelve al compilar y no reserva nada.
"""),
        "pascal": ("""
program Mapred;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, Token, Sec: string;
  I, V, D, Total: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea) + ' ';

  Sec := '';
  Token := '';
  Total := 0;
  for I := 1 to Length(Linea) do
  begin
    if Linea[I] = ' ' then
    begin
      if Token <> '' then
      begin
        V := StrToInt(Token);
        D := V * 2;
        Total := Total + D;
        if Sec <> '' then Sec := Sec + '-';
        Sec := Sec + IntToStr(D);
        Token := '';
      end;
    end
    else
      Token := Token + Linea[I];
  end;

  WriteLn('doblados=', Sec, ' total=', IntToStr(Total));
end.
""", """
**Lo que esta clase enseña en Pascal.** El Pascal ISO **sí permite pasar procedimientos y funciones
como parámetros** —fue de los primeros lenguajes imperativos en hacerlo— con una sintaxis que declara
la firma completa:

```pascal
function Aplicar(F: TTransformacion; X: Integer): Integer;

type
  TTransformacion = function(X: Integer): Integer;
```

Lo que **no** tiene el Pascal clásico son **funciones anónimas ni clausuras**: hay que declarar la
función con nombre en otro sitio y pasar su dirección. Y esa es precisamente la barrera que impide el
estilo funcional, como se vio en la clase 067: si escribir la función cuesta cinco líneas y un
nombre, el bucle sale más corto.

Delphi 2009 añadió los **métodos anónimos**, que sí son clausuras de verdad:

```pascal
type
  TFunc = reference to function(X: Integer): Integer;

var
  Factor: Integer;
  Multiplicar: TFunc;
begin
  Factor := 3;
  Multiplicar := function(X: Integer): Integer
                 begin Result := X * Factor; end;   { CAPTURA Factor }
```

`reference to function` es la palabra clave que lo distingue de un puntero a función normal: implica
**conteo de referencias y captura del entorno**. Con eso, Delphi tiene clausuras completas.

Free Pascal las soporta también, con `{$modeswitch functionreferences}`. Pero llegaron cuarenta años
después que en Lisp, y el ecosistema ya estaba escrito con bucles.
"""),
        "lisp": ("""
(let* ((lista (loop for v = (read *standard-input* nil :fin)
                    until (eq v :fin)
                    collect v))
       (doblados (mapcar (lambda (x) (* 2 x)) lista)))
  (format t "doblados=~{~D~^-~} total=~D~%"
          doblados (reduce #'+ doblados)))
""", """
**Lo que esta clase enseña en Common Lisp.** **`mapcar` y `reduce` son de 1958**, y no son una
biblioteca añadida: son la definición del paradigma. Este programa es, esencialmente, cómo se
escribiría hoy en cualquier lenguaje funcional.

`(lambda (x) (* 2 x))` es una **función anónima**, y `#'+` es la función `+` **como valor** — el
`#'` es la abreviatura de `function`, que obtiene el objeto función asociado a un nombre.

Y aquí aparece una peculiaridad de Common Lisp que hay que conocer: es un **Lisp-2**, es decir, tiene
**dos espacios de nombres separados**, uno para funciones y otro para variables.

```lisp
(defun lista (x) ...)      ; una FUNCIÓN llamada lista
(let ((lista '(1 2 3)))    ; y una VARIABLE llamada lista: no chocan
  (lista lista))           ; la primera posición es función, la segunda variable
(funcall f x)              ; para llamar a una función guardada en una VARIABLE
(mapcar #'coche lista)     ; y #' para OBTENERLA de su nombre
```

Scheme es un **Lisp-1**: un solo espacio de nombres, así que no hacen falta `#'` ni `funcall`. La
discusión entre los dos diseños es una de las más antiguas de la comunidad, y el argumento a favor
del Lisp-2 es práctico: **puedes llamar a una variable `lista` sin ocultar la función `lista`**.

`reduce` acepta `:initial-value`, `:from-end` y `:key`, lo que cubre todos los pliegues. Y
`mapcar` recorre **varias listas a la vez**: `(mapcar #'+ '(1 2) '(10 20))` da `(11 22)`.
"""),
        "tcl": ("""
gets stdin linea

set doblados {}
set total 0
foreach v [split [string trim $linea]] {
    set d [expr {$v * 2}]
    lappend doblados $d
    incr total $d
}

puts "doblados=[join $doblados -] total=$total"
""", """
**Lo que esta clase enseña en Tcl.** En Tcl **el código es una cadena**, así que pasar una función es
pasar texto — y eso da funciones de orden superior sin necesidad de que el lenguaje las contemple:

```tcl
proc aplicar {lista cuerpo} {
    set r {}
    foreach x $lista { lappend r [eval $cuerpo] }    ;# $x visible en el cuerpo
    return $r
}
aplicar {1 2 3} {expr {$x * 2}}
```

Funciona, y es peligroso: el cuerpo se evalúa en un ámbito que el llamante no controla, y una cadena
que venga de fuera es una inyección.

La forma moderna y correcta es **`apply`**, que llegó en Tcl 8.5 y es una **lambda de verdad**:

```tcl
set doblar {{x} {expr {$x * 2}}}          ;# una lambda: argumentos y cuerpo
apply $doblar 5                            ;# -> 10

set doblados [lmap x $lista {expr {$x * 2}}]           ;# map, Tcl 8.6
set total [::tcl::mathop::+ {*}$doblados]              ;# suma con expansión
```

`{*}$lista` es el **operador de expansión**, que convierte una lista en argumentos separados — el
`*args` de Python, añadido en 8.5. Y `::tcl::mathop::+` expone los operadores aritméticos **como
comandos**, así que `+` puede pasarse como argumento igual que `#'+` en Lisp.

Que los operadores se puedan usar como comandos es coherente con todo lo demás: en Tcl no hay
operadores, así que exponerlos como comandos no es una excepción, es la regla.
"""),
        "perl": ("""
use strict;
use warnings;
use List::Util qw(sum0);

my $linea = <STDIN>;
chomp $linea;

my @doblados = map { $_ * 2 } split ' ', $linea;
my $total = sum0(@doblados);

print "doblados=", join('-', @doblados), " total=$total\\n";
""", """
**Lo que esta clase enseña en Perl.** `map`, `grep` y `sort` son **operadores del lenguaje**, no
funciones de biblioteca, y por eso reciben un bloque sin necesidad de escribir `sub { }`. Esa
ligereza sintáctica es lo que hizo que el estilo funcional se adoptara en Perl mucho antes que en
Java o C++.

Y Perl tiene funciones de primera clase completas, con clausuras:

```perl
my $doblar = sub { $_[0] * 2 };           # función anónima
my @r = map { $doblar->($_) } @lista;     # -> para llamar por referencia
my $sumador = do { my $t = 0; sub { $t += shift } };   # clausura con estado
```

`reduce` no es un operador sino una función de `List::Util`, y usa una convención propia:

```perl
use List::Util qw(reduce);
my $total = reduce { $a + $b } @doblados;
```

**`$a` y `$b` no son parámetros declarados**: son las variables globales del paquete que `reduce`
—y `sort`— rellenan en cada paso. Es la misma pareja que usa `sort { $a <=> $b }`, y es la razón por
la que en toda esta sección las variables se han llamado `$x` e `$y` en lugar de `$a` y `$b`: usarlas
para otra cosa interfiere con estas funciones.

Es una decisión de diseño discutible —variables globales implícitas en lugar de parámetros— que
existe por rendimiento: evitar crear un marco de llamada por elemento. En una lista de un millón, se
nota.
"""),
        "cpp": ("""
#include <algorithm>
#include <iostream>
#include <iterator>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>

int main() {
    std::string linea;
    if (!std::getline(std::cin, linea)) return 1;

    std::istringstream iss(linea);
    const std::vector<int> v{std::istream_iterator<int>(iss),
                             std::istream_iterator<int>()};

    std::vector<int> doblados(v.size());
    std::transform(v.begin(), v.end(), doblados.begin(),
                   [](int x) { return x * 2; });

    const int total = std::accumulate(doblados.begin(), doblados.end(), 0);

    std::string sec;
    for (std::size_t i = 0; i < doblados.size(); ++i) {
        if (i > 0) sec += '-';
        sec += std::to_string(doblados[i]);
    }

    std::cout << "doblados=" << sec << " total=" << total << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** `std::transform` es el `map` y `std::accumulate` es el `reduce`,
y los dos existen desde la STL original de 1994. Lo que faltaba —y llegó con **C++11**— eran las
**lambdas**, sin las cuales había que declarar un objeto función aparte:

```cpp
// Antes de C++11:
struct Doblar { int operator()(int x) const { return x * 2; } };
std::transform(v.begin(), v.end(), d.begin(), Doblar{});

// Desde C++11:
std::transform(v.begin(), v.end(), d.begin(), [](int x) { return x * 2; });
```

Es la misma barrera que en Pascal y en Tcl: **la capacidad ya estaba; lo que faltaba era que
escribirla fuera barato**.

Y hay una propiedad que distingue a C++ de casi todos los demás lenguajes de esta página: **la lambda
no cuesta nada en ejecución**. Cada lambda tiene un tipo único generado por el compilador, así que
`std::transform` se instancia para ese tipo concreto y **el cuerpo se integra en línea**. No hay
llamada indirecta, no hay puntero a función, no hay asignación de memoria.

Compara con `std::function`, que sí borra el tipo y sí tiene coste:

```cpp
std::function<int(int)> f = [](int x) { return x * 2; };   // llamada indirecta
auto g = [](int x) { return x * 2; };                       // tipo concreto: gratis
```

Esa es la abstracción de coste cero de la clase 043, aplicada a las funciones de orden superior. Y la
captura —`[&]`, `[=]`, `[x]`— convierte la lambda en una clausura con las mismas reglas de tiempo de
vida que cualquier objeto: **capturar por referencia algo que muere antes deja una referencia
colgante**.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi MAPRED;
  linea varchar(200) const;
end-pi;

dcl-s trozos varchar(20) dim(50);
dcl-s i      int(10);
dcl-s d      int(10);
dcl-s sec    varchar(500) inz('');
dcl-s total  int(20) inz(0);
dcl-s salida char(560);

trozos = %split(linea : ' ');

for i = 1 to %elem(trozos);
  d = %int(trozos(i)) * 2;
  total += d;
  if sec <> '';
    sec += '-';
  endif;
  sec += %char(d);
endfor;

salida = 'doblados=' + sec + ' total=' + %char(total);
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG **no tiene funciones de orden superior**: no hay lambdas, no
hay punteros a función con firma comprobada y no se puede pasar un procedimiento como argumento.

Lo que sí tiene, y es lo más cercano, son los **punteros a procedimiento**:

```rpgle
dcl-pr calcular int(10) extproc(pPtr);
  valor int(10) const;
end-pr;

dcl-s pPtr pointer;

pPtr = %paddr('DOBLAR');       // la DIRECCIÓN de un procedimiento
resultado = calcular(5);        // llamada indirecta
```

`%paddr` obtiene la dirección de un procedimiento y `extproc(puntero)` declara un prototipo que la
usa. Funciona, y es exactamente un puntero a función de C: **sin captura de entorno, sin
comprobación de tipos en la asignación y sin gestión de tiempo de vida**. Nadie lo escribe salvo para
interoperar con C o para tablas de despacho.

Y como en COBOL, el `reduce` real de un programa RPG está en otra parte:

```rpgle
exec sql
  select sum(importe * 2), count(*)
    into :total, :cuantos
    from movimientos;
```

`SUM`, `AVG`, `MAX`, `COUNT` y `GROUP BY` son las funciones de agregación de SQL, y son el pliegue que
el lenguaje no tiene. En una plataforma donde la base de datos es parte del sistema operativo, esa
delegación no es un rodeo: es la arquitectura.
"""),
        "pli": ("""
 mapred: procedure options(main);

    declare linea character(200) varying;
    declare trozo character(20)  varying;
    declare sec   character(500) varying initial('');
    declare (i, p, v, d) fixed binary(31);
    declare total fixed binary(31) initial(0);

    get edit (linea) (a(200));
    linea = trim(linea) || ' ';

    p = 1;
    do i = 1 to length(linea);
       if substr(linea, i, 1) = ' ' then do;
          if i > p then do;
             trozo = substr(linea, p, i - p);
             v = trozo;
             d = v * 2;
             total = total + d;
             if sec ^= '' then sec = sec || '-';
             sec = sec || trim(char(d));
          end;
          p = i + 1;
       end;
    end;

    put skip list ('doblados=' || sec || ' total=' || trim(char(total)));

 end mapred;
""", """
**Lo que esta clase enseña en PL/I.** PL/I **sí puede pasar procedimientos como argumento**, con el
atributo `entry`:

```pli
declare aplicar entry (entry, fixed binary(31));

aplicar: procedure (f, x);
   declare f entry returns (fixed binary(31));
   declare x fixed binary(31);
   return (f(x));
end aplicar;
```

Un parámetro declarado `entry` es una referencia a un procedimiento. Está en el lenguaje desde 1964,
antes que en Pascal.

Lo que no tiene son **funciones anónimas ni clausuras**, así que aplica la misma barrera de siempre:
sin sintaxis ligera, no se usa.

Y PL/I tiene la agregación sobre arrays, que ya apareció en la clase 067:

```pli
declare v(100) fixed binary(31);

v = v * 2;                 /* map */
total = sum(v);            /* reduce */
p = prod(v);               /* producto */
```

`sum`, `prod`, `max`, `min`, `any`, `all`, `poly` son intrínsecas sobre arrays. Cubren los pliegues
frecuentes sin necesidad de un `reduce` general, que es la misma solución que Fortran y COBOL.

La conclusión de esta clase para los tres lenguajes de negocio es la misma: **cuando el lenguaje trae
las agregaciones que su dominio necesita, la abstracción general se echa menos de menos de lo que
parece**. Y cuando aparece un caso nuevo, hay que escribir el bucle.
"""),
        "mumps": ("""
MAPRED ; Map y reduce -- clase 068
 read linea
 set sec = "", total = 0
 for i = 1:1:$length(linea, " ") do
 . set d = $piece(linea, " ", i) * 2
 . set total = total + d
 . set:sec'="" sec = sec _ "-"
 . set sec = sec _ d
 write "doblados=", sec, " total=", total, !
 quit
""", """
**Lo que esta clase enseña en M.** M no tiene funciones de orden superior en el sentido habitual,
pero tiene **indirección**, que da algo funcionalmente equivalente y mucho más peligroso:

```mumps
 set transformacion = "v*2"
 for i = 1:1:n do
 . set v = $piece(linea, " ", i)
 . set d = @transformacion         ; @ EVALÚA la cadena como una expresión
 . ...
```

`@` es el operador de indirección, y admite tres formas:

```mumps
 set x = @nombreVariable       ; indirección de NOMBRE
 do @nombreRutina              ; indirección de RUTINA
 set y = @expresion            ; indirección de EXPRESIÓN
 set @("^DATOS(" _ id _ ")") = valor   ; construir la referencia como TEXTO
```

Con eso, "la función" que se aplica puede venir de una variable, de un fichero de configuración o de
un *global* de la base de datos. Es enormemente flexible y es la razón de que muchos sistemas M
tengan tablas de reglas almacenadas como datos, que se ejecutan sin recompilar.

Y es la razón de que **no se pueda analizar estáticamente un programa M**: ninguna herramienta puede
decir qué se ejecuta, porque se decide en el momento. Es el `eval` de JavaScript con cincuenta años
más de historia, con la misma potencia y los mismos problemas de seguridad y mantenimiento.

Es un buen cierre para esta parte: **el código como dato aparece en muchos lenguajes, y la diferencia
entre que sea una virtud o un problema está en si hay comprobación de por medio**. En Lisp, una macro
opera sobre una estructura y el compilador la verifica; en M, sobre una cadena y nadie la verifica.
"""),
        "smalltalk": ("""
| valores doblados total sec |

valores := stdin nextLine substrings collect: [ :cada | cada asNumber ].
doblados := valores collect: [ :cada | cada * 2 ].
total := doblados inject: 0 into: [ :a :b | a + b ].

sec := String streamContents: [ :flujo |
    doblados do: [ :d | flujo print: d ] separatedBy: [ flujo nextPut: $- ] ].

Transcript
    show: 'doblados=', sec;
    show: ' total=', total printString;
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** `collect:` es el `map` e `inject:into:` es el `reduce`, y
los dos reciben **bloques** — que en Smalltalk son objetos de primera clase con clausura completa.

Y aquí está el punto de fondo de toda la Parte 4: **en Smalltalk no hay ninguna estructura de control
en el lenguaje**. `ifTrue:`, `whileTrue:`, `to:do:`, `and:`, `select:`, `collect:`, `inject:into:` son
**todos métodos que reciben bloques**. Las decisiones, los bucles, el cortocircuito y las funciones de
orden superior son **la misma cosa**: enviar un mensaje con un trozo de código dentro.

Eso significa que puedes añadir tus propias estructuras de control sin tocar el lenguaje:

```smalltalk
Number >> vecesConIndice: unBloque
    1 to: self do: [ :i | unBloque value: i ]

5 vecesConIndice: [ :i | Transcript show: i printString ]
```

Ningún otro lenguaje de esta página lo consigue con tan poca maquinaria: Lisp necesita macros, Tcl
necesita `uplevel`, C++ necesita plantillas, y Ada, Fortran, COBOL, PL/I y RPG no lo consiguen.

Y `inject:into:` merece su nombre: el valor inicial se "inyecta" y el bloque recibe **el acumulado y
el elemento**, en ese orden. Con él se escriben `sum`, `max`, `count`, `detect` y prácticamente todo
lo demás — de hecho, así están escritos en `Collection`, y puedes leerlos.
"""),
    },
)

