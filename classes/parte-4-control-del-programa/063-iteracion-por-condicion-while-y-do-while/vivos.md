# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 063

> [⬅️ Volver a la clase 063](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Sumar de 1 a *n* con un bucle que pregunta antes de cada vuelta. El `while` es la forma más básica de
repetir, y la pregunta que reparte a estos lenguajes es cuántas variantes ofrecen: **¿se puede
comprobar la condición al final en vez de al principio? ¿se puede repetir un número fijo de veces sin
llevar contador? ¿se puede salir por el medio?**

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **iteración gobernada por una condición**, y estos lenguajes lo enseñan porque
> tienen construcciones que el núcleo perdió por el camino. COBOL tiene un `PERFORM` que hace **seis
> cosas distintas** según cómo se escriba, incluida la ejecución de un párrafo remoto *n* veces. Ada
> tiene un `loop` desnudo con `exit when`, que es el bucle de salida por el medio sin `break`. Y
> Smalltalk no tiene bucle en absoluto: **`whileTrue:` es un método del bloque**.
>
> Y M enseña la versión extrema: un `for` **sin argumentos** es un bucle infinito, y se sale con un
> `quit` postcondicional.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (n >= 1) → stdout: `suma=<1+2+...+n>`
- **Regla:** `suma = 1 + 2 + ... + n`

| stdin | esperado |
|---|---|
| `5` | `suma=15` |
| `1` | `suma=1` |
| `10` | `suma=55` |

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
```

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

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
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
```

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

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
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
```

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

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
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
```

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

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((n (read))
      (total 0)
      (i 1))
  (loop while (<= i n) do
    (incf total i)
    (incf i))
  (format t "suma=~D~%" total))
```

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

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

set total 0
set i 1
while {$i <= $n} {
    incr total $i
    incr i
}

puts "suma=$total"
```

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

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
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

print "suma=$total\n";
```

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

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
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

    std::cout << "suma=" << total << '\n';
    return 0;
}
```

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
```

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

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
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
```

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

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
SUMA ; Suma 1..n -- clase 063
 read n
 set total = 0
 set i = 1
 for  quit:i>n  set total = total + i, i = i + 1
 write "suma=", total, !
 quit
```

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

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n total i |

n := stdin nextLine trimBoth asNumber.

total := 0.
i := 1.
[ i <= n ] whileTrue: [
    total := total + i.
    i := i + 1 ].

Transcript show: 'suma=', total printString; cr.
```

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

---

## Y de vuelta a la clase

Lo transferible es la distinción entre **comprobar antes** y **comprobar después**: `while` puede no
ejecutar el cuerpo ni una vez, y `repeat/until`, `do-while` o `PERFORM WITH TEST AFTER` lo ejecutan
siempre al menos una. Y ojo con el sentido de la condición, que es donde todo el mundo se equivoca al
cambiar de lenguaje: el `until` de Pascal y el `UNTIL` de COBOL dicen **cuándo parar**, mientras que
el `while` de C y el `dow` de RPG dicen **cuándo seguir**. La misma palabra en dos lenguajes puede
significar lo contrario.

⏮️ [Volver a la clase 063](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
