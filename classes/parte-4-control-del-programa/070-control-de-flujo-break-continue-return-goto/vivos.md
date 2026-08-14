# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 070

> [⬅️ Volver a la clase 070](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

El menor divisor mayor que 1. Un bucle que **para en cuanto encuentra**, que es la forma más común de
salir de un bucle antes de tiempo. Y el motivo de que esta clase exista: durante veinte años, salir
de un bucle por el medio se consideró tan mala práctica como el `goto`, y algunos de estos lenguajes
**se diseñaron sin ninguna forma de hacerlo**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **salida anticipada**, y estos lenguajes lo enseñan porque son los que vivieron
> la polémica. **El Pascal ISO no tiene `break` ni `continue`**: Wirth los consideró incompatibles con
> la programación estructurada, y el resultado es que el código Pascal clásico está lleno de banderas
> booleanas. **COBOL no tuvo `EXIT PERFORM` hasta 2002.** Y Fortran cargaba con el `GO TO` calculado y
> el asignado, que fueron el detonante de la carta de Dijkstra en 1968.
>
> Enfrente, Ada, PL/I y Perl resolvieron el problema real —salir de un bucle **anidado concreto**— con
> **bucles con nombre**, que es lo que hoy tienen Java, Rust y Kotlin.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (n >= 2) → stdout: `primer_divisor=<el menor divisor > 1>`
- **Regla:** `el menor d en [2..n] tal que n % d == 0`

| stdin | esperado |
|---|---|
| `15` | `primer_divisor=3` |
| `7` | `primer_divisor=7` |
| `12` | `primer_divisor=2` |

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
PROGRAM-ID. DIVISOR.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC 9(9) COMP-3.
01  D       PIC 9(9) COMP-3.
01  RES     PIC 9(9) COMP-3.
01  ED-R    PIC Z(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N
    MOVE N TO RES

    PERFORM VARYING D FROM 2 BY 1 UNTIL D > N
        IF FUNCTION MOD(N, D) = 0
            MOVE D TO RES
            EXIT PERFORM
        END-IF
    END-PERFORM

    MOVE RES TO ED-R
    DISPLAY "primer_divisor=" FUNCTION TRIM(ED-R)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** **`EXIT PERFORM` es de COBOL 2002.** Antes de eso no había
forma de salir de un bucle antes de tiempo, y el idioma universal era la **bandera**:

```cobol
01  ENCONTRADO  PIC X VALUE "N".
    88  SI-ENCONTRADO  VALUE "S".

PERFORM VARYING D FROM 2 BY 1
        UNTIL D > N OR SI-ENCONTRADO          *> la condición hace de break
    IF FUNCTION MOD(N, D) = 0
        MOVE D TO RES
        SET SI-ENCONTRADO TO TRUE
    END-IF
END-PERFORM
```

Ese patrón —una variable booleana en la condición del bucle— aparece en millones de líneas de COBOL y
es perfectamente legible. Tiene un coste real: la condición se comprueba dos veces por vuelta y el
lector tiene que reconstruir mentalmente que la bandera es un `break`.

COBOL 2002 añadió las tres formas modernas:

```cobol
EXIT PERFORM          *> break
EXIT PERFORM CYCLE    *> continue
EXIT PARAGRAPH        *> salir del párrafo
EXIT SECTION
GOBACK                *> salir del programa devolviendo el control
```

Y el `GO TO` sigue existiendo, con una variante que conviene conocer porque es característica:
**`GO TO ... DEPENDING ON`**, el salto calculado, hermano del de Fortran:

```cobol
GO TO PARRAFO-A PARRAFO-B PARRAFO-C DEPENDING ON OPCION
```

Está desaconsejado desde los años 80 y sigue apareciendo en código heredado, donde es una de las
principales causas de que un programa sea difícil de seguir.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program divisor
   implicit none
   integer :: n, d, res

   read(*, *) n

   res = n
   do d = 2, n
      if (mod(n, d) == 0) then
         res = d
         exit
      end if
   end do

   write(*, '(A,I0)') 'primer_divisor=', res
end program divisor
```

**Lo que esta clase enseña en Fortran.** `exit` sale del bucle y `cycle` salta a la siguiente vuelta,
y **los dos aceptan el nombre de un bucle**, que es la pieza importante:

```fortran
exterior: do i = 1, n
   interior: do j = 1, m
      if (encontrado) exit exterior       ! sale de LOS DOS
      if (v(j) < 0) cycle interior
   end do interior
end do exterior
```

Sin nombres, salir de un bucle exterior desde dentro de otro exige una bandera o un `goto`. Con ellos,
la intención está escrita.

Pero Fortran es también **el origen de la polémica entera**. El FORTRAN clásico tenía tres formas de
salto que hoy resultan increíbles:

```fortran
      GO TO 100                      ! incondicional
      GO TO (10, 20, 30), I          ! CALCULADO: salta a la I-ésima etiqueta
      ASSIGN 40 TO ETIQ              ! ASIGNADO: la etiqueta es un DATO
      GO TO ETIQ
```

El **`GO TO` asignado** es el peor: la etiqueta de destino se guarda en una variable, así que **a
dónde salta el programa se decide en ejecución** y no se puede saber leyendo el código. Es lo mismo
que la indirección de M vista en la clase 068, aplicada al control de flujo.

Contra eso escribió Dijkstra en 1968 su carta *"Go To Statement Considered Harmful"*, que abrió el
debate de la programación estructurada. El `GO TO` asignado quedó obsolescente en Fortran 90 y
**eliminado del estándar en Fortran 95**; el calculado, obsolescente desde el 90.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Divisor is
   N, Res : Integer;
begin
   Get (N);

   Res := N;
   for D in 2 .. N loop
      if N mod D = 0 then
         Res := D;
         exit;
      end if;
   end loop;

   Put ("primer_divisor="); Put (Res, Width => 1); New_Line;
end Divisor;
```

**Lo que esta clase enseña en Ada.** Ada tiene `exit`, `exit when` y **bucles con nombre**, y su forma
condicional evita el `if` de una línea:

```ada
Busqueda : for D in 2 .. N loop
   exit Busqueda when N mod D = 0;      --  condición Y salida en la misma línea
end loop Busqueda;
```

`exit when` es una construcción propia que hace visible en un solo sitio **la condición de salida**,
en lugar de esconderla dentro de un `if`. Es la misma economía que el `quit:condición` de M.

Y Ada tiene `goto`, con dos restricciones que lo hacen casi inofensivo:

```ada
goto Fin;
...
<<Fin>>          --  las etiquetas van entre << >>
```

**No se puede saltar hacia dentro de un bucle, de un `if` o de un bloque**: solo hacia fuera o dentro
del mismo nivel. Eso elimina de raíz el salto que aterriza en medio de una estructura, que es el que
hace ilegible un programa.

Lo interesante es que Ada **conservó `goto` a propósito**. El equipo de Ichbiah razonó que hay casos
—máquinas de estados generadas, salida de bucles muy anidados— donde el salto acotado es más claro que
las alternativas, y que prohibirlo empujaría a la gente hacia banderas peor legibles. La sintaxis
`<<Etiqueta>>` es deliberadamente llamativa: **si lo usas, se ve**.

Es la misma postura que tomó C con el `goto` que sobrevive hoy: el de liberar recursos.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Divisor;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N, D, Res: Integer;

begin
  Read(N);

  Res := N;
  for D := 2 to N do
    if (N mod D) = 0 then
    begin
      Res := D;
      Break;
    end;

  WriteLn('primer_divisor=', IntToStr(Res));
end.
```

**Lo que esta clase enseña en Pascal.** **`Break` y `Continue` NO existen en el Pascal ISO.** Son
extensiones de Turbo Pascal que Free Pascal y Delphi heredaron. Wirth los dejó fuera a propósito: los
consideraba una forma encubierta de `goto`, incompatible con el principio de una entrada y una salida
por estructura.

El resultado, en Pascal estándar, es la bandera:

```pascal
Res := N;
D := 2;
Encontrado := False;
while (D <= N) and not Encontrado do
begin
  if (N mod D) = 0 then
  begin
    Res := D;
    Encontrado := True;
  end;
  Inc(D);
end;
```

Comparado con el `Break` de este programa, hay una variable más, una condición compuesta y un
incremento manual. Es más largo y —esta es la parte discutible— **no es más claro**.

Y hay una ironía notable: **Pascal sí tiene `goto`**, con etiquetas numéricas declaradas en una
sección `label` propia. Wirth prohibió la salida estructurada de un bucle y conservó el salto
arbitrario, que es el que de verdad rompe la estructura. Es una de las decisiones de diseño de Pascal
que peor ha envejecido, y la evidencia es que **todas** las implementaciones prácticas añadieron
`Break` y `Continue` en cuanto tuvieron ocasión.

Free Pascal y Delphi añadieron además `Exit` y `Exit(valor)`, que es el `return` que el ISO tampoco
tenía, como se vio en la clase 058.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((n (read))
       (res (or (loop for d from 2 to n
                      when (zerop (mod n d))
                      return d)
                n)))
  (format t "primer_divisor=~D~%" res))
```

**Lo que esta clase enseña en Common Lisp.** `return` dentro de `loop` sale del bucle **devolviendo un
valor**, así que el bucle entero es una expresión. Si nunca se cumple, `loop` devuelve `nil` y el
`or` da el valor por defecto — el mismo idioma de la clase 057.

Y detrás de eso hay una construcción más general que es la respuesta de Lisp a toda esta clase:
**`block` y `return-from`**.

```lisp
(block busqueda
  (dolist (x lista)
    (dolist (y otra)
      (when (= x y)
        (return-from busqueda (list x y))))))   ; sale de los DOS bucles
```

`block` crea un punto de salida **con nombre**, y `return-from` salta a él devolviendo un valor. Es
exactamente el bucle etiquetado de Ada, Java y Rust, con dos diferencias: **cualquier expresión puede
ser un bloque**, no solo un bucle, y el salto puede cruzar límites de función si el bloque sigue vivo.

Toda la maquinaria de control de Lisp se apoya en esto:

```lisp
(defun f () ...)          ; crea implícitamente un BLOCK llamado f
(return-from f valor)     ; por eso return-from funciona en cualquier función
(loop ...)                ; crea un BLOCK llamado nil
(return valor)            ; = (return-from nil valor)
```

Y para saltos no locales de verdad —salir de varias funciones a la vez— están `catch` y `throw`, que
en Lisp **no** son manejo de errores sino **salto con etiqueta dinámica**. El manejo de errores es
otra cosa distinta, y se ve en la clase siguiente.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

set res $n
for {set d 2} {$d <= $n} {incr d} {
    if {$n % $d == 0} {
        set res $d
        break
    }
}

puts "primer_divisor=$res"
```

**Lo que esta clase enseña en Tcl.** `break` y `continue` son **comandos**, como todo lo demás. Y eso
tiene una consecuencia que ningún otro lenguaje de esta página comparte: **funcionan
atravesando llamadas a procedimiento**.

```tcl
proc comprobar {v} {
    if {$v < 0} { return -code break }    ;# ¡hace break en el bucle del LLAMANTE!
    return ok
}

foreach x $lista {
    comprobar $x                          ;# puede terminar este bucle
}
```

`return -code break` hace que la llamada al procedimiento se comporte como si fuera un `break`
escrito ahí mismo. Es potentísimo y es exactamente el mecanismo con el que se construyen estructuras
de control propias en Tcl, junto con `uplevel` de la clase 041.

Tcl modela el control de flujo como **códigos de retorno**, no como saltos: cada comando devuelve
`ok`, `error`, `return`, `break` o `continue`, y los comandos que contienen bloques —`for`, `while`,
`foreach`, `proc`— deciden qué hacer con cada código. `break` no es magia: es un valor de retorno que
`for` reconoce.

Ese diseño unifica el control de flujo y el manejo de errores en un solo mecanismo, y es lo que hace
que `catch` de la clase siguiente pueda capturar **cualquiera** de los cinco códigos:

```tcl
set codigo [catch { ... } resultado]     ;# 0=ok 1=error 2=return 3=break 4=continue
```

Y `goto` no existe en Tcl. Nunca lo tuvo, y nadie lo ha echado de menos.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

my $res = $n;
for my $d (2 .. $n) {
    if ($n % $d == 0) {
        $res = $d;
        last;
    }
}

print "primer_divisor=$res\n";
```

**Lo que esta clase enseña en Perl.** Perl no usa `break` y `continue`: usa **`last`, `next` y
`redo`**, y esa tercera no existe en casi ningún otro lenguaje.

| Perl | Qué hace |
|---|---|
| `last` | Sale del bucle (*break*) |
| `next` | Siguiente iteración (*continue*) |
| `redo` | **Repite la misma iteración sin reevaluar la condición** |

`redo` sirve para reintentar el elemento actual: leer una línea que estaba mal formada y volver a
procesarla, o repetir una petición de red que falló. Es raro y muy específico.

Los tres aceptan **etiqueta**, que es la solución a los bucles anidados:

```perl
EXTERIOR: for my $x (@a) {
    for my $y (@b) {
        next EXTERIOR if $x == $y;      # siguiente vuelta del bucle de FUERA
        last EXTERIOR if $x > 100;
    }
}
```

Perl tiene además un bloque `continue` —distinto del comando `continue` de C— que se ejecuta **al
final de cada vuelta, incluso si se usó `next`**:

```perl
while (mi_condicion()) {
    next if $saltar;
    ...
} continue {
    $contador++;       # se ejecuta SIEMPRE, incluso tras el next
}
```

Es el equivalente de la tercera parte de un `for` de C, disponible en un `while`. Resuelve el error
clásico de olvidar el incremento en la rama del `next`, que produce bucles infinitos.

Y `goto LABEL` existe, apenas se usa, y el `goto &subrutina` de la clase 069 es otra cosa distinta.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    int res = n;
    for (int d = 2; d <= n; ++d) {
        if (n % d == 0) {
            res = d;
            break;
        }
    }

    std::cout << "primer_divisor=" << res << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ tiene `break`, `continue`, `return` y `goto`, y **carece de
bucles con nombre**, que es la única forma limpia de salir de un anidamiento. Java, Perl, Ada, PL/I,
Fortran y Rust los tienen; C++ no.

Las alternativas son las tres clásicas, y ninguna es buena:

```cpp
// 1) Bandera
bool encontrado = false;
for (...) { for (...) { if (...) { encontrado = true; break; } } if (encontrado) break; }

// 2) goto  -- irónicamente, la más legible de las tres
for (...) { for (...) { if (...) goto fin; } }
fin:

// 3) Extraer a una función y usar return  -- la recomendada
auto buscar = [&]() -> std::optional<int> {
    for (...) for (...) if (...) return valor;
    return std::nullopt;
};
```

La tercera es la que recomiendan las *Core Guidelines*, y funciona porque una lambda es barata.

Y `goto` sobrevive en C++ y sobre todo en **C** por un motivo muy concreto que conviene entender:
**liberar recursos cuando no hay destructores**.

```c
FILE *f = fopen(...);  if (!f)  goto salir;
char *b = malloc(...); if (!b)  goto cerrar;
...
cerrar: fclose(f);
salir:  return err;
```

Ese patrón —la "escalera de limpieza"— está por todo el núcleo de Linux y es **la forma correcta de
escribirlo en C**. En C++ no hace falta porque **RAII** lo resuelve: el destructor se ejecuta al salir
del ámbito por cualquier camino. Es el mismo argumento de la clase 058, y la mejor demostración de
que `goto` no es un problema de estilo sino la señal de que falta una abstracción.

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

dcl-pi DIVISOR;
  n int(10) const;
end-pi;

dcl-s d      int(10);
dcl-s res    int(10);
dcl-s salida char(40);

res = n;
for d = 2 to n;
  if %rem(n : d) = 0;
    res = d;
    leave;
  endif;
endfor;

salida = 'primer_divisor=' + %char(res);
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG usa **`leave`** para salir del bucle e **`iter`** para pasar
a la siguiente vuelta. Los nombres son distintos de los de C, y el vocabulario completo del control
de flujo es:

```rpgle
leave;        // break
iter;         // continue
leavesr;      // salir de una subrutina
return;       // salir de un procedimiento
```

`leave` e `iter` **no aceptan etiqueta**, así que RPG tiene el mismo problema que C++ con los bucles
anidados, y la misma solución: extraer a un subprocedimiento y usar `return`.

Y hay una construcción propia de RPG que merece esta clase: **`goto` está prohibido dentro de
subprocedimientos**. En el ciclo clásico existía `GOTO` con etiquetas `TAG`, y era muy usado; al
introducir ILE, IBM decidió que los subprocedimientos son código estructurado y punto.

Eso deja una situación curiosa en la práctica: **en el mismo programa pueden convivir subrutinas
antiguas con `GOTO` y subprocedimientos modernos sin él**. Un fuente RPG real de una empresa con
treinta años de historia es una estratigrafía: se ve la capa de 1985 con indicadores y `GOTO`, la de
2001 con `/FREE`, y la de 2019 con `%split` y `for-each`.

Esa convivencia es, probablemente, la razón principal de que RPG siga vivo: **nunca hubo que
reescribir nada para poder usar lo nuevo**.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 divisor: procedure options(main);

    declare (n, d, res) fixed binary(31);

    get list (n);

    res = n;
    busqueda: do d = 2 to n;
       if mod(n, d) = 0 then do;
          res = d;
          leave busqueda;
       end;
    end busqueda;

    put skip list ('primer_divisor=' || trim(char(res)));

 end divisor;
```

**Lo que esta clase enseña en PL/I.** **`leave etiqueta`** sale de un bucle **con nombre**, y PL/I lo
tenía cuando C ni siquiera existía. Junto a `iterate etiqueta` —el `continue` etiquetado— cubre el
caso de los bucles anidados que C++ todavía no resuelve.

```pli
exterior: do i = 1 to n;
   interior: do j = 1 to m;
      if a(i,j) = 0 then leave exterior;      /* sale de los dos */
      if a(i,j) < 0 then iterate exterior;    /* siguiente i */
   end interior;
end exterior;
```

Nombrar los bucles y salir del que quieras es exactamente lo que Java añadió con etiquetas en 1995,
Rust con `'label` en 2015 y Kotlin con `@loop`. PL/I lo tenía en 1964.

Y PL/I tiene además el salto no local más potente de esta página: **`goto` a una etiqueta de un
procedimiento que está más arriba en la pila**.

```pli
declare fin label;      /* una VARIABLE de tipo etiqueta */
...
go to fin;              /* puede salir de VARIOS niveles de llamada a la vez */
```

Una **variable de etiqueta** guarda un punto de retorno de un procedimiento activo, y saltar a ella
**desenrolla la pila** hasta ese marco. Es funcionalmente una excepción sin manejador, y es la
construcción que hace que un PL/I mal escrito sea prácticamente imposible de seguir — porque el salto
puede cruzar cualquier número de llamadas.

Es, otra vez, el patrón de PL/I: potencia máxima, barandillas mínimas.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
DIVISOR ; Primer divisor -- clase 070
 read n
 set res = n
 for d = 2:1:n do  quit:res'=n
 . quit:n#d'=0
 . set res = d
 write "primer_divisor=", res, !
 quit
```

**Lo que esta clase enseña en M.** M **no tiene `break` ni `continue`**: tiene `quit`, y su
significado depende de **dónde esté**.

- `quit` dentro de un bloque `do` (con puntos) → termina **ese bloque**, es decir, la iteración
  actual: es el `continue`.
- `quit` en el argumento del `for` → termina **el bucle**: es el `break`.
- `quit` en el cuerpo de una rutina → **sale de la rutina**: es el `return`.

En este programa aparecen los dos primeros: el `quit:res'=n` que va **detrás del `do`** corta el
bucle cuando ya se encontró algo, y el `quit:n#d'=0` **dentro del bloque** salta a la siguiente
vuelta.

Que una sola palabra haga tres cosas según su posición es la economía extrema de M llevada al control
de flujo. Es compacto y exige leer con cuidado: la diferencia entre `for d=2:1:n do  quit:cond` y
`for d=2:1:n do` seguido de una línea `. quit:cond` es **dónde termina el programa**.

Y M **no tiene `goto` estructurado**, pero tiene algo más potente y más peligroso: **`do` con
indirección**, ya visto en la clase 068.

```mumps
 do @rutina        ; ejecuta la rutina cuyo NOMBRE está en la variable
 goto @etiqueta    ; y salta a la etiqueta cuyo nombre está en la variable
```

`goto @` es el `GO TO` asignado de FORTRAN, el que Dijkstra denunció y que Fortran eliminó del
estándar en 1995. En M sigue ahí, se usa, y es una de las razones de que analizar estáticamente un
sistema M sea imposible.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n res |

n := stdin nextLine trimBoth asNumber.

res := (2 to: n) detect: [ :d | n \\ d = 0 ] ifNone: [ n ].

Transcript show: 'primer_divisor=', res printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** **Smalltalk no tiene `break` ni `continue`, y no puede
tenerlos.** Como los bucles son mensajes con bloques —clase 063— no hay ninguna estructura sintáctica
de la que salir: `to:do:` es un método, y desde dentro de un bloque no se puede "romper" el método
que lo está ejecutando.

La respuesta idiomática es la de este programa: **usar el mensaje que ya expresa la intención**.
`detect:ifNone:` recorre y **para en cuanto encuentra**. No es un bucle con un `break`: es una
búsqueda, y se llama así.

El protocolo de `Collection` está lleno de estos:

```smalltalk
coleccion detect: [ :x | ... ] ifNone: [ ... ]      "el primero que cumpla"
coleccion anySatisfy: [ :x | ... ]                   "¿alguno?  cortocircuita"
coleccion allSatisfy: [ :x | ... ]                   "¿todos?   cortocircuita"
coleccion indexOf: elemento
```

Todos cortocircuitan, y todos dicen **qué** haces en lugar de **cómo**. Es el mismo argumento de la
clase 067 sobre las comprensiones.

Cuando de verdad hace falta salir, existe el **retorno no local**: un `^` dentro de un bloque
**termina el método que creó el bloque**, no solo el bloque.

```smalltalk
buscarDivisor: n
    2 to: n do: [ :d | n \\ d = 0 ifTrue: [ ^d ] ].    "^ sale del MÉTODO"
    ^n
```

Ese `^` dentro del bloque de `to:do:` es un salto no local que atraviesa la llamada al método
`to:do:`. Está implementado con `thisContext` y es, funcionalmente, el `return-from` de Lisp. Es la
única forma de salida anticipada del lenguaje, y es potente: **un bloque pasado a otro objeto puede
terminar el método que lo creó**, aunque se evalúe muy lejos.

---

## Y de vuelta a la clase

Lo transferible: **el problema nunca fue `break`, fue el salto arbitrario**. Un `break` sale de una
estructura por su borde y el flujo sigue siendo local; un `goto` puede aterrizar en cualquier sitio y
obliga a leer el programa entero para saber cómo se llegó ahí. Por eso todos los lenguajes acabaron
adoptando la salida etiquetada —`exit Bucle when`, `last EXTERIOR`, `leave bucle`— que da la potencia
del salto **acotada a una estructura visible**. Y por eso el `goto` sigue vivo exactamente en un
caso: **liberar recursos en C**, donde no hay destructores.

⏮️ [Volver a la clase 070](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
