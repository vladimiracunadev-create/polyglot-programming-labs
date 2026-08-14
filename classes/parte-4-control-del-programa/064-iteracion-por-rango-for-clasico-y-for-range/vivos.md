# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 064

> [⬅️ Volver a la clase 064](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

El factorial: multiplicar todos los enteros de 1 a *n*. Un bucle de rango puro, elegido porque además
desborda enseguida —`20!` ya son diecinueve dígitos— y eso separa a los lenguajes en dos grupos: los
que fallan en silencio al pasarse y los que **simplemente siguen contando**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **bucle sobre un rango conocido**, y estos lenguajes aportan dos cosas. La
> primera es la **variable de control y su ámbito**: en Ada es una **constante que solo existe dentro
> del bucle** y no hace falta declararla, mientras que en C es una variable normal que se puede
> modificar dentro del cuerpo. Pascal prohíbe modificarla y deja su valor final **indefinido** al
> salir.
>
> La segunda es el desbordamiento: `20!` cabe en 64 bits por poco, y `21!` ya no. **Lisp, Smalltalk y
> Tcl no desbordan nunca**; COBOL, RPG y PL/I tienen decimales de decenas de dígitos; y C++, Fortran,
> Ada y Pascal se quedan sin sitio.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (0 <= n <= 20) → stdout: `factorial=<n!>`
- **Regla:** `n! = 1·2·…·n ; 0! = 1`

| stdin | esperado |
|---|---|
| `5` | `factorial=120` |
| `1` | `factorial=1` |
| `0` | `factorial=1` |

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
```

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

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
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
```

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

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
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
```

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

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
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
```

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

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((n (read))
      (f 1))
  (loop for i from 1 to n do (setf f (* f i)))
  (format t "factorial=~D~%" f))
```

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

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

set f 1
for {set i 1} {$i <= $n} {incr i} {
    set f [expr {$f * $i}]
}

puts "factorial=$f"
```

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

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

my $f = 1;
$f *= $_ for 1 .. $n;

print "factorial=$f\n";
```

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

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    unsigned long long f = 1;
    for (int i = 1; i <= n; ++i) {
        f *= static_cast<unsigned long long>(i);
    }

    std::cout << "factorial=" << f << '\n';
    return 0;
}
```

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
```

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

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
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
```

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

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
FACT ; Factorial -- clase 064
 read n
 set f = 1
 for i = 1:1:n set f = f * i
 write "factorial=", f, !
 quit
```

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

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n f |

n := stdin nextLine trimBoth asNumber.

f := 1.
1 to: n do: [ :i | f := f * i ].

Transcript show: 'factorial=', f printString; cr.
```

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

---

## Y de vuelta a la clase

La regla que deja esta clase: **antes de escribir un bucle de acumulación, pregúntate cuánto puede
crecer el acumulador**. Es la misma comprobación que en la clase 044 con las bases, y aquí es más
urgente porque un producto crece factorialmente. Y la segunda: **no toques la variable de control
dentro del cuerpo**. Ada y Pascal lo prohíben; C, Fortran y Tcl lo permiten, y hacerlo produce bucles
que ningún lector espera.

⏮️ [Volver a la clase 064](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
