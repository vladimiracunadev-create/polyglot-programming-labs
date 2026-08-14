# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 059

> [⬅️ Volver a la clase 059](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Cuatro tramos de nota a partir de una puntuación. Una cadena de comparaciones ordenadas, que es la
estructura de decisión más común de todo el software de negocio. Y es también la que más se escribe
mal: **si los tramos se comprueban en el orden equivocado, el programa compila, se ejecuta y da un
resultado incorrecto sin ninguna señal**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **anidamiento y el orden de las condiciones**, y estos lenguajes lo enseñan
> porque cargan con la cicatriz más famosa de la historia de la sintaxis: **el `else` colgante**.
>
> En COBOL, el `.` de más dentro de un `IF` cambia el flujo del programa sin dar error —de ahí que
> COBOL-85 tuviera que inventar `END-IF`—. En Fortran clásico, un `IF` sin `THEN` solo abarca una
> sentencia. Y en Pascal, el punto y coma antes del `else` no compila. Tres lenguajes, tres formas
> distintas de que el anidamiento se rompa en silencio o casi.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `score` (0-100) → stdout: `nota=<A|B|C|F>`
- **Regla:** `score>=90→A; >=80→B; >=70→C; si no→F`

| stdin | esperado |
|---|---|
| `95` | `nota=A` |
| `72` | `nota=C` |
| `40` | `nota=F` |

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
PROGRAM-ID. NOTAS.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  SCORE   PIC S9(9) COMP-3.
01  NOTA    PIC X.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO SCORE

    EVALUATE TRUE
        WHEN SCORE >= 90   MOVE "A" TO NOTA
        WHEN SCORE >= 80   MOVE "B" TO NOTA
        WHEN SCORE >= 70   MOVE "C" TO NOTA
        WHEN OTHER         MOVE "F" TO NOTA
    END-EVALUATE

    DISPLAY "nota=" NOTA
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** Aquí está **el defecto sintáctico más caro de COBOL**: hasta
COBOL-85 no existía `END-IF`, y el alcance de un `IF` lo delimitaba **el punto**.

```cobol
IF SALDO > 0
    DISPLAY "positivo".
    DISPLAY "siempre se ejecuta".      *> el punto anterior CERRÓ el IF
```

Esa segunda línea parece estar dentro del `IF` —está indentada— y **no lo está**. El punto de la
línea anterior cerró la sentencia. El programa compila, se ejecuta y hace algo distinto de lo que
aparenta, sin un solo aviso. Con `IF` anidados, un punto de más colapsa varios niveles a la vez.

COBOL-85 introdujo los **terminadores de ámbito** —`END-IF`, `END-PERFORM`, `END-EVALUATE`,
`END-READ`, `END-COMPUTE`— precisamente para eliminar esa dependencia del punto. La regla de estilo
moderna es tajante: **un punto por párrafo, al final, y terminadores explícitos en todo lo demás**.

Y para el caso de esta clase, `EVALUATE TRUE` evita el anidamiento por completo, con una ventaja
sobre el `else if` que conviene ver: los tramos quedan **alineados en columna**, así que revisar que
el orden es correcto —de mayor a menor— es una lectura vertical. En una cadena de `if` anidados, esa
misma comprobación exige seguir la indentación.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program notas
   implicit none
   integer :: score
   character(len=1) :: nota

   read(*, *) score

   if (score >= 90) then
      nota = 'A'
   else if (score >= 80) then
      nota = 'B'
   else if (score >= 70) then
      nota = 'C'
   else
      nota = 'F'
   end if

   write(*, '(A,A)') 'nota=', nota
end program notas
```

**Lo que esta clase enseña en Fortran.** El `if` de Fortran tiene **dos formas**, y confundirlas es
un error clásico:

```fortran
if (x > 0) y = 1                 ! IF LÓGICO: una sola sentencia, sin then ni end if
if (x > 0) then                  ! IF de BLOQUE: varias sentencias
   y = 1
   z = 2
end if
```

La primera forma no lleva `then` y **solo abarca la sentencia que va en la misma línea**. Escribir
una segunda línea debajo, indentada, no la mete dentro del `if`. Es exactamente el mismo problema que
el punto de COBOL y que el `if` sin llaves de C, con la diferencia de que en Fortran la ausencia de
`then` lo hace algo más visible.

Fortran moderno añadió además **nombres de construcción**, que ayudan mucho con el anidamiento
profundo:

```fortran
clasificar: if (score >= 90) then
   nota = 'A'
else if (score >= 80) then clasificar
   nota = 'B'
end if clasificar
```

Poder nombrar un `if`, un `do` o un `select case` y repetir el nombre al cerrarlo hace que un bloque
de doscientas líneas siga siendo legible, y que el compilador detecte un cierre mal emparejado. Ada
hace lo mismo con `end Nombre_Del_Procedimiento`, y por la misma razón: **el código de larga vida lo
lee alguien que no lo escribió**.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Notas is
   Score : Integer;
   Nota  : Character;
begin
   Get (Score);

   if Score >= 90 then
      Nota := 'A';
   elsif Score >= 80 then
      Nota := 'B';
   elsif Score >= 70 then
      Nota := 'C';
   else
      Nota := 'F';
   end if;

   Put_Line ("nota=" & Nota);
end Notas;
```

**Lo que esta clase enseña en Ada.** En Ada **el `else` colgante no existe**, y no por convención:
porque la gramática lo impide. Cada `if` termina obligatoriamente en `end if;`, así que no hay
ninguna ambigüedad posible sobre a qué `if` pertenece un `else`.

```ada
if A then
   if B then
      X := 1;
   end if;        --  este end if cierra el interior...
else
   X := 2;        --  ...y por tanto ESTE else es del exterior. Sin duda.
end if;
```

En C, en Java y en JavaScript esa misma estructura sin llaves es ambigua para el lector —el
compilador la resuelve asociando el `else` al `if` más cercano— y ha producido errores reales.

Y `elsif` en lugar de `else if` es lo que evita la cascada de `end if`: con `else if` harían falta
tres cierres para tres tramos.

Ada añade a esta clase algo que resuelve el problema de fondo —**el orden equivocado de los
tramos**— mediante los subtipos:

```ada
subtype Puntuacion is Integer range 0 .. 100;
Score : Puntuacion;                      --  leer 150 levanta Constraint_Error
```

Los tramos mal ordenados siguen siendo posibles, pero **el rango de entrada queda garantizado por el
tipo**, así que desaparece toda una familia de casos límite que en otros lenguajes hay que comprobar
a mano al principio de la cadena.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Notas;
{$MODE OBJFPC}{$H+}

var
  Score: Integer;
  Nota: Char;

begin
  Read(Score);

  if Score >= 90 then
    Nota := 'A'
  else if Score >= 80 then
    Nota := 'B'
  else if Score >= 70 then
    Nota := 'C'
  else
    Nota := 'F';

  WriteLn('nota=', Nota);
end.
```

**Lo que esta clase enseña en Pascal.** Fíjate en los punto y coma de este programa: **no hay ninguno
antes de un `else`**, y solo aparece uno al final de toda la cadena. Es la regla que más tropiezos
causa en Pascal, y tiene una explicación precisa.

En Pascal, **el `;` es un separador entre sentencias, no un terminador**. `if ... then A else B` es
**una sola sentencia**, así que poner `;` después de `A` la daría por terminada y dejaría el `else`
sin dueño: error de compilación.

```pascal
if C then A;  else B;      { NO COMPILA }
if C then A   else B;      { correcto }
```

En C ocurre lo contrario —el `;` termina, y `if (c) a; else b;` es correcto— y por eso quien viene de
C escribe mal el primer `if` de Pascal que le toca.

La ventaja es que **el error se detecta al compilar**. Compara con el punto de COBOL, que no da
error y cambia el significado; o con el `if` sin llaves de C, que compila y hace otra cosa. De las
tres formas de equivocarse con el anidamiento que aparecen en esta página, la de Pascal es la única
que el compilador atrapa siempre.

Y a Pascal, al no tener terminador de `if`, le pasa lo mismo que a C con el anidamiento: la solución
es usar `begin`/`end` incluso cuando hay una sola sentencia, que es la versión Pascal de "pon siempre
las llaves".

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((score (read)))
  (format t "nota=~A~%"
          (cond ((>= score 90) "A")
                ((>= score 80) "B")
                ((>= score 70) "C")
                (t             "F"))))
```

**Lo que esta clase enseña en Common Lisp.** **En Lisp el anidamiento no puede ser ambiguo, porque
los paréntesis lo delimitan todo.** No hay `else` colgante, no hay punto que cierre de más, no hay
`;` que termine antes de tiempo. La estructura del código **es** la estructura del árbol sintáctico,
literalmente.

Ese es el argumento que la comunidad Lisp lleva sesenta años haciendo: los paréntesis que tanto
critican desde fuera son lo que elimina una familia entera de errores de sintaxis. Y como el editor
los empareja y los reindenta solo, la molestia práctica es mucho menor de lo que parece.

Para esta clase concreta, Lisp ofrece además una variante de `cond` que casi nadie conoce y que viene
justo al caso:

```lisp
(cond ((< score 0) :invalido)
      ((find score '(90 100)) ...))

;; Y la forma "=>" que pasa el VALOR de la condición al resultado:
(cond ((assoc score tabla) => cdr)     ; si la búsqueda encuentra algo, aplica cdr
      (t "F"))                          ; sin repetir la búsqueda
```

La forma `=>` —estándar en Scheme y disponible en varias bibliotecas de Common Lisp— evita el patrón
de "comprobar y volver a calcular" que en otros lenguajes obliga a una variable temporal. Es el mismo
problema que C++17 resolvió con `if (auto x = f(); x)`.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set score [string trim $linea]

if {$score >= 90} {
    set nota A
} elseif {$score >= 80} {
    set nota B
} elseif {$score >= 70} {
    set nota C
} else {
    set nota F
}

puts "nota=$nota"
```

**Lo que esta clase enseña en Tcl.** Las llaves son **obligatorias** en Tcl, y no por estilo: el
comando `if` recibe el cuerpo como **un argumento**, así que tiene que ser una sola palabra —y en Tcl
una "palabra" con espacios se escribe entre llaves—. No existe la forma sin llaves que causa
problemas en C.

Esa obligación elimina de raíz el problema del anidamiento: **cada rama está delimitada porque tiene
que estarlo para poder pasarse como argumento**.

Y hay una consecuencia menos obvia que esta clase es el sitio para ver. Como `if` es un comando y
`elseif` es literalmente el texto `"elseif"` en la posición correcta, escribir `elsif` o `else if`
(separado) **no es un error de sintaxis**: es pasarle a `if` un argumento que no espera, y el error
sale en ejecución.

```tcl
if {$a} { ... } else if {$b} { ... }    ;# ERROR: "else if" no es "elseif"
```

Para una cadena larga de tramos, la forma idiomática de Tcl no es `if`/`elseif` sino `switch` con el
patrón `-` para condiciones, o directamente una estructura de datos:

```tcl
foreach {umbral letra} {90 A 80 B 70 C 0 F} {
    if {$score >= $umbral} { set nota $letra ; break }
}
```

Convertir la cadena de condiciones en **datos recorridos por un bucle** es una técnica que funciona en
cualquier lenguaje y que en Tcl resulta especialmente natural, porque la lista y el código son la
misma cosa.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $score = <STDIN>;
chomp $score;

my $nota = $score >= 90 ? 'A'
         : $score >= 80 ? 'B'
         : $score >= 70 ? 'C'
         :                'F';

print "nota=$nota\n";
```

**Lo que esta clase enseña en Perl.** Este programa usa la **cadena de ternarios**, alineada en
columna, que es un idioma muy extendido en Perl y que merece explicación porque parece más raro de lo
que es.

`?:` es **asociativo por la derecha**, así que `a ? b : c ? d : e` se agrupa como
`a ? b : (c ? d : e)`. Encadenados y alineados con los `:` en la misma columna, se leen como una
tabla de tramos — que es exactamente lo que son.

La ventaja sobre `if`/`elsif` no es la brevedad: es que **es una expresión**. `my $nota = ...` asigna
una sola vez, en una sola sentencia. Con `if`/`elsif` habría que declarar `$nota` antes y asignarla
en cada rama, y el compilador no puede comprobar que todas las ramas asignan. Es el mismo argumento
que hace que Rust y Kotlin conviertan `if` en expresión.

Perl tiene además los `if` y `unless` como **modificadores** al final, que ya aparecieron en la 058, y
un detalle de esta clase: **las llaves son obligatorias**.

```perl
if ($a) print "x";        # NO COMPILA en Perl
if ($a) { print "x" }     # correcto
print "x" if $a;          # o el modificador
```

Perl, igual que Tcl, eliminó el `if` sin llaves. Es una decisión de 1987 que C nunca tomó y que le
habría ahorrado a la industria unos cuantos incidentes.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    int score{};
    if (!(std::cin >> score)) return 1;

    char nota{};
    if (score >= 90) {
        nota = 'A';
    } else if (score >= 80) {
        nota = 'B';
    } else if (score >= 70) {
        nota = 'C';
    } else {
        nota = 'F';
    }

    std::cout << "nota=" << nota << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ **permite omitir las llaves** cuando la rama tiene una sola
sentencia, y esa permisividad tiene el historial de fallos más caro de esta página.

El caso documentado es **`goto fail`**, de Apple, en 2014:

```c
if (algo)
    goto fail;
    goto fail;          // línea duplicada; NO está dentro del if
...
fail:
    return err;
```

La segunda línea está indentada como si perteneciera al `if`, y no pertenece: se ejecuta siempre. El
resultado fue que la validación de la firma en el intercambio TLS **se saltaba por completo**, en
iOS y macOS, durante meses. Una llave habría hecho imposible el error.

Por eso todas las guías modernas —*Core Guidelines* incluidas— dicen: **llaves siempre, aunque haya
una sola sentencia**. Y los compiladores ayudan: `-Wmisleading-indentation` en GCC y Clang avisa
exactamente de este patrón.

Para el caso concreto de esta clase, C++ ofrece además dos alternativas que evitan la cadena:

```cpp
const char nota = score >= 90 ? 'A' : score >= 80 ? 'B' : score >= 70 ? 'C' : 'F';

// O, con un contenedor ordenado, buscando el tramo:
static const std::map<int, char> tramos{{90,'A'},{80,'B'},{70,'C'},{0,'F'}};
auto it = tramos.lower_bound(score);   // la estructura de datos hace la decisión
```

Convertir la cadena de condiciones en datos es la misma técnica que en Tcl, y escala mucho mejor
cuando los tramos son quince y no cuatro.

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

dcl-pi NOTAS;
  score int(10) const;
end-pi;

dcl-s nota   char(1);
dcl-s salida char(20);

select;
  when score >= 90;
    nota = 'A';
  when score >= 80;
    nota = 'B';
  when score >= 70;
    nota = 'C';
  other;
    nota = 'F';
endsl;

salida = 'nota=' + nota;
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** `select`/`when`/`other`/`endsl` mantiene los cuatro tramos
**alineados en columna**, sin anidar. Es el mismo argumento que el `EVALUATE TRUE` de COBOL: una
decisión entre casos excluyentes se lee mejor como una tabla que como una escalera.

RPG tiene también `if`/`elseif`/`else`/`endif`, y la elección entre las dos formas es una convención
de estilo con criterio: `if` para una o dos ramas, `select` a partir de tres.

Lo que hace peculiar a RPG en esta clase es lo que había antes del formato libre. En el RPG de
columnas, el anidamiento se marcaba con **niveles de indicadores**, y un `IF` se cerraba con `END`
sin ninguna pista de cuál cerraba:

```text
     C                   IF        SCORE >= 90
     C                   MOVE      'A'           NOTA
     C                   ELSE
     C                   IF        SCORE >= 80
     C                   MOVE      'B'           NOTA
     C                   END
     C                   END
```

Dos `END` seguidos, sin nombre y sin indentación obligatoria. En un programa de mil líneas, emparejar
esos `END` a mano era una tarea real. Los terminadores con nombre —`endif`, `endsl`, `endfor`,
`enddo`— del formato libre resolvieron exactamente ese problema, igual que `END-IF` lo resolvió en
COBOL-85.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 notas: procedure options(main);

    declare score fixed binary(31);
    declare nota  character(1);

    get list (score);

    select;
       when (score >= 90) nota = 'A';
       when (score >= 80) nota = 'B';
       when (score >= 70) nota = 'C';
       otherwise          nota = 'F';
    end;

    put skip list ('nota=' || nota);

 end notas;
```

**Lo que esta clase enseña en PL/I.** `select` sin expresión evalúa las condiciones en orden, igual
que el `EVALUATE TRUE` de COBOL y el `select` de RPG. PL/I la tuvo primero, y de aquí la tomaron los
otros dos.

Sobre el anidamiento, PL/I resolvió el problema del `else` colgante con **`do`/`end` como bloque
genérico**:

```pli
if a then do;
   x = 1;
   y = 2;
end;
else do;
   x = 3;
end;
```

`do; ... end;` agrupa sentencias sin ser un bucle, que es exactamente lo que hacen `begin`/`end` en
Pascal y las llaves en C. Que la misma palabra sirva para el bucle y para el bloque es económico y
confunde al principio.

Y PL/I tiene una construcción propia que conviene conocer al leer código antiguo: **`begin` block**,
que además de agrupar **crea un ámbito nuevo** con su propio almacenamiento automático, y puede
llevar sus propias declaraciones y manejadores `ON`. Es el `declare` block de Ada y el bloque de C++,
con la diferencia de que en PL/I es más pesado —implica activar un marco de pila— y por eso se
prefería `do; end;` para el agrupamiento simple.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
NOTAS ; Notas -- clase 059
 read score
 set nota = $select(score>=90 : "A", score>=80 : "B", score>=70 : "C", 1 : "F")
 write "nota=", nota, !
 quit
```

**Lo que esta clase enseña en M.** `$select` resuelve la cadena entera **en una expresión**, sin
`if`, sin bloques y sin anidamiento. Recorre los pares `condición : valor` de izquierda a derecha,
devuelve el primero cuya condición sea cierta, y el `1 :` final hace de `else` porque `1` siempre es
verdadero.

Y —esto es lo importante— **evalúa perezosamente**: no calcula los valores de las ramas que no gana.
Es `cond` de Lisp con forma de función, y cubre el 90 % de los usos del `if` en código M real.

Si ninguna condición se cumple y no hay rama final, `$select` **levanta un error**, no devuelve vacío.
Es una de las pocas cosas en M que fallan ruidosamente, y es deliberado: un `$select` sin caso por
defecto significa que el programador afirmaba que uno de los casos siempre se daría.

Para el anidamiento con bloques, M usa el **nivel de puntos**, que es único entre los lenguajes de
esta página:

```mumps
 if score>0 do
 . write "positivo",!
 . if score>100 do
 . . write "fuera de rango",!
 . write "fin del bloque",!
```

Un punto por nivel, al principio de la línea. No hay llaves ni `end`: la profundidad **es** la
indentación, hecha obligatoria y contada por el intérprete. Es la misma idea que Python adoptaría
treinta años después, con una notación mucho más difícil de leer.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| score nota |

score := stdin nextLine trimBoth asNumber.

nota := score >= 90
    ifTrue:  [ 'A' ]
    ifFalse: [ score >= 80
        ifTrue:  [ 'B' ]
        ifFalse: [ score >= 70 ifTrue: [ 'C' ] ifFalse: [ 'F' ] ] ].

Transcript show: 'nota=', nota; cr.
```

**Lo que esta clase enseña en Smalltalk.** El anidamiento de tres niveles de este programa es
**incómodo a propósito**, y la comunidad lo lee como una señal. Cuando un método acumula
condicionales anidados, la respuesta idiomática no es aplanarlos: es **quitarlos**.

Y para una tabla de tramos, la forma que un programador Smalltalk escribiría de verdad convierte las
condiciones en **datos**:

```smalltalk
| tramos |
tramos := { 90 -> 'A'. 80 -> 'B'. 70 -> 'C'. 0 -> 'F' }.
nota := (tramos detect: [ :par | score >= par key ]) value.
```

`{ ... }` es un array construido en ejecución, `->` crea una **asociación** clave-valor, y `detect:`
devuelve el primer elemento que cumple el bloque. La cadena de condiciones desaparece: queda una
tabla y una búsqueda.

Es exactamente la misma técnica que aparece en las versiones de Tcl y C++ de esta clase, y aquí es
especialmente natural porque los bloques y las colecciones son el vocabulario básico del lenguaje.

Y `detect:` tiene un pariente que conviene conocer: `detect:ifNone:`, que recibe un bloque para el
caso de que ninguno cumpla. Sin él, `detect:` **levanta una excepción** si no encuentra nada — la
misma decisión que `$select` en M: la ausencia de caso por defecto se considera un error del
programador, no un resultado.

---

## Y de vuelta a la clase

La lección: **el terminador explícito no es burocracia**. `END-IF`, `end if`, `endif`, `fi`,
`END-EVALUATE` existen porque los lenguajes que no los tenían acumularon defectos reales — el más
caro documentado es el fallo de `goto fail` de Apple en 2014, donde una línea duplicada bajo un `if`
sin llaves desactivó la validación de certificados TLS. Poner siempre las llaves, o el terminador, no
es estilo: es la mitigación de un error que ya ha ocurrido.

⏮️ [Volver a la clase 059](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
