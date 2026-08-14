# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 042

> [⬅️ Volver a la clase 042](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Intercambiar dos valores es el ejercicio mínimo que obliga a distinguir tres cosas que en el uso
diario se confunden: **declarar** (anunciar que un nombre existe y con qué forma), **inicializar**
(darle su primer valor) y **asignar** (darle otro después). Esta página lo resuelve en doce
lenguajes que llevan décadas en producción, y en cada uno la pregunta interesante es la misma:
*¿qué vale una variable en el instante en que nace?*

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **el ciclo de vida del enlace nombre→valor**, y estos lenguajes lo enseñan
> porque toman decisiones opuestas: en COBOL toda la memoria se dimensiona **antes de arrancar** y no
> existe declarar dentro de un bloque; en Fortran inicializar en la declaración tiene un efecto
> lateral que sorprende hasta a quien lleva años usándolo; en MUMPS **no hay declaración en absoluto**;
> y en Ada puedes abrir un ámbito nuevo en mitad del código solo para nombrar un valor temporal.
>
> Ninguna de esas cuatro respuestas es la de Python. Verlas juntas es lo que convierte "declara tus
> variables" en una decisión de diseño con consecuencias.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a b` (dos enteros) → stdout: `a=<nuevo a> b=<nuevo b>` tras intercambiar
- **Regla:** `intercambiar a y b`

| stdin | esperado |
|---|---|
| `3 7` | `a=7 b=3` |
| `0 5` | `a=5 b=0` |
| `-2 9` | `a=9 b=-2` |

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
PROGRAM-ID. INTERCAMBIO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TXT-A   PIC X(20).
01  TXT-B   PIC X(20).
01  A       PIC S9(9) COMP-3.
01  B       PIC S9(9) COMP-3.
01  TEMP    PIC S9(9) COMP-3.
01  ED-A    PIC -(9)9.
01  ED-B    PIC -(9)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    MOVE A TO TEMP
    MOVE B TO A
    MOVE TEMP TO B

    MOVE A TO ED-A
    MOVE B TO ED-B
    DISPLAY "a=" FUNCTION TRIM(ED-A) " b=" FUNCTION TRIM(ED-B)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** Aquí **declarar e inicializar son el mismo acto, y ocurren
antes de que el programa arranque**. Todo lo que hay en `WORKING-STORAGE` se dimensiona al compilar
y existe durante toda la ejecución: no hay "declarar dentro de un bucle", no hay ámbito de bloque, y
`TEMP` no nace cuando se usa sino cuando arranca el programa.

Y el verbo importa: **`MOVE` no es `=`**. `MOVE A TO TEMP` se lee en el orden en que ocurre —origen
primero, destino después— y además **convierte según la forma del destino**: mover un `PIC 9(9)` a
un `PIC 9(3)` trunca por la izquierda sin avisar. La asignación de COBOL lleva una conversión
implícita dentro, y esa es la parte que hay que vigilar al leer código ajeno.

El valor inicial se da con `VALUE`, y solo ahí: `01 CONTADOR PIC 9(4) VALUE 0.` Sin `VALUE`, el
contenido es indeterminado, igual que en C.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program intercambio
   implicit none
   integer :: a, b, temp

   read(*, *) a, b

   temp = a
   a = b
   b = temp

   write(*, '(A,I0,A,I0)') 'a=', a, ' b=', b
end program intercambio
```

**Lo que esta clase enseña en Fortran.** Fortran esconde aquí una de las trampas más caras del
lenguaje, y tiene que ver exactamente con inicializar en la declaración:

```fortran
subroutine contar()
   integer :: n = 0      ! ¡ESTO NO HACE LO QUE PARECE!
   n = n + 1
   print *, n
end subroutine
```

En C o en Java, esa línea significa "cada vez que entres, `n` empieza en 0". En **Fortran significa
otra cosa**: inicializar en la declaración le da implícitamente el atributo **`save`**, es decir,
la variable **conserva su valor entre llamadas**. Ese `print` mostrará 1, 2, 3, 4… La inicialización
ocurre **una sola vez, al cargar el programa**, no en cada entrada.

Por eso este programa declara `temp` sin valor y lo asigna dentro del cuerpo. Y por eso, cuando de
verdad quieres un valor fijo, se usa `parameter`, que es una constante evaluada al compilar:

```fortran
integer, parameter :: MAX_ITEMS = 100
```

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Intercambio is
   A, B : Integer;
begin
   Get (A);
   Get (B);

   --  Un bloque `declare` abre un ámbito solo para el valor temporal,
   --  y lo declara `constant`: no puede reasignarse por accidente.
   declare
      Viejo_A : constant Integer := A;
   begin
      A := B;
      B := Viejo_A;
   end;

   Put ("a=");  Put (A, Width => 1);
   Put (" b="); Put (B, Width => 1);
   New_Line;
end Intercambio;
```

**Lo que esta clase enseña en Ada.** El bloque **`declare … begin … end`** es la respuesta de Ada a
esta clase: puedes abrir un ámbito **en cualquier punto del código** solo para nombrar algo, y ese
nombre deja de existir al cerrar el bloque. `Viejo_A` no contamina el resto del procedimiento.

Y está declarado **`constant`**, que es la parte deliberada: el valor temporal de un intercambio
nunca debe reasignarse, así que se dice, y el compilador lo comprueba. Es el hábito que Ada intenta
inculcar — *declara la intención más restrictiva que sea cierta*.

Ada además distingue con precisión inicialización de asignación: `A : Integer := 0` inicializa en la
declaración, `A := 0` asigna después, y una variable sin inicializar tiene un valor **inválido** que
el compilador puede detectar con `pragma Normalize_Scalars` o con las comprobaciones activadas.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Intercambio;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  A, B, Temp: Integer;

begin
  Read(A, B);

  Temp := A;
  A := B;
  B := Temp;

  WriteLn('a=', IntToStr(A), ' b=', IntToStr(B));
end.
```

**Lo que esta clase enseña en Pascal.** La **sección `var` va antes del cuerpo y no es negociable**.
Wirth lo diseñó así a propósito: si todas las declaraciones están juntas y arriba, el compilador
puede trabajar en una sola pasada —de ahí su famosa velocidad— y el lector tiene el inventario
completo de la memoria del procedimiento antes de leer la primera sentencia.

El precio es que no puedes declarar donde usas, algo que hoy se considera buena práctica. El
beneficio, menos obvio, es que **no puedes declarar una variable a mitad de una función larga y
olvidarte de para qué era**.

En Pascal clásico **no se puede inicializar en la declaración**: `var i: Integer = 0;` solo es legal
para variables globales en Free Pascal y Delphi, y técnicamente es una constante con tipo, no una
inicialización. La forma correcta de un valor fijo es la sección `const`.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((a (read))
       (b (read)))
  ;; rotatef intercambia "en su sitio": no hace falta temporal.
  (rotatef a b)
  (format t "a=~D b=~D~%" a b))
```

**Lo que esta clase enseña en Common Lisp.** Lisp separa con una nitidez poco común **ligar** un
nombre de **asignar** a un nombre, y tiene sintaxis distinta para cada cosa:

```lisp
(let  ((a 1) (b 2)) ...)   ; LIGA: crea nombres nuevos, en paralelo
(let* ((a 1) (b (* a 2))) ...) ; LIGA en secuencia: b puede ver a
(setf a 99)                ; ASIGNA: cambia lo que ya estaba ligado
```

`let` crea un enlace nuevo que desaparece al cerrar el paréntesis; `setf` modifica uno existente.
Que existan `let` y `let*` como formas separadas —paralelo frente a secuencial— muestra hasta qué
punto el lenguaje se toma en serio *cuándo* se resuelve cada enlace.

Y `rotatef` merece atención: no es una función, es una **macro** que se expande a las asignaciones
necesarias. Funciona sobre cualquier "lugar" —una variable, un elemento de un array, un campo de una
estructura—, porque `setf` y compañía operan sobre lugares y no sobre valores. Esa generalidad es
gratis: la escribió alguien con `defmacro`, no el compilador.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [split [string trim $linea]] a b

lassign [list $b $a] a b

puts "a=$a b=$b"
```

**Lo que esta clase enseña en Tcl.** **No hay declaración.** Ninguna. Una variable existe desde que
`set` le da un valor y deja de existir con `unset`; para preguntar si existe está `info exists`. No
hay tipo que declarar porque todo valor es una cadena, y no hay ámbito que declarar porque el ámbito
lo determina el procedimiento donde estás.

Eso convierte la asignación en el único acto que importa, y por eso `set` es un **comando** y no un
operador: `set a 5` son tres palabras separadas por espacios, como cualquier otra línea de Tcl.

El intercambio de aquí usa el idioma de listas —`lassign [list $b $a] a b`— que construye una lista
con los valores en el orden nuevo y la reparte. Es la versión Tcl de la asignación múltiple, y
funciona precisamente porque una lista **es** una cadena con los elementos separados por espacios.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

my ($p, $q) = split ' ', $linea;

($p, $q) = ($q, $p);          # intercambio sin variable temporal

print "a=$p b=$q\n";
```

**Lo que esta clase enseña en Perl.** `my` es la declaración, y su ausencia es el problema: **sin
`use strict`, escribir `$totl` en vez de `$total` crea una variable global nueva con valor
indefinido**, y el programa sigue tan tranquilo. Por eso las dos primeras líneas de todo Perl
escrito después de 1995 son siempre las mismas.

`my` declara con **ámbito léxico** —el bloque que lo contiene—, igual que `let` en JavaScript. Su
pariente `our` declara una global del paquete y `local` hace algo distinto y más raro: guarda
temporalmente el valor de una variable **global** y lo restaura al salir del bloque, que es **ámbito
dinámico**. Tener las tres en el mismo lenguaje es una lección completa sobre ámbitos.

Y `($p, $q) = ($q, $p)` funciona porque Perl **evalúa el lado derecho por completo antes de asignar**.
No es un truco del intercambio: es la semántica de la asignación de listas, y por eso no hace falta
temporal.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <utility>

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::swap(a, b);

    std::cout << "a=" << a << " b=" << b << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** `int a{}` con llaves vacías es **inicialización de valor**: deja
`a` en cero. Escribir `int a;` a secas lo dejaría **indeterminado**, y leerlo sería comportamiento
indefinido. Son dos líneas casi idénticas con consecuencias muy distintas, y esa es la parte de esta
clase que C++ enseña mejor que nadie.

Las llaves además **prohíben las conversiones que pierden información**: `int x{3.7};` no compila,
mientras que `int x = 3.7;` compila en silencio y guarda 3. La *inicialización uniforme* de C++11
existe precisamente para cerrar esa puerta.

Y `std::swap` no es una función cualquiera: desde C++11 usa **semántica de movimiento**, así que
intercambiar dos objetos grandes —dos `std::vector` de un millón de elementos— no copia nada,
intercambia punteros internos. La misma línea de código sirve para dos `int` y para dos estructuras
enormes, con el coste adecuado en cada caso. Eso es la abstracción de coste cero del lenguaje.

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

dcl-pi INTERCAM;
  a int(10);
  b int(10);
end-pi;

dcl-s temp   int(10) inz(0);
dcl-s salida char(50);

temp = a;
a = b;
b = temp;

salida = 'a=' + %char(a) + ' b=' + %char(b);
dsply salida;

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** `dcl-s temp int(10) inz(0)` separa las tres nociones con tres
piezas visibles: `dcl-s` declara, `int(10)` es la forma, `inz(0)` es el valor inicial. Y si omites
`inz`, RPG **no deja basura**: inicializa por tipo —numéricos a cero, caracteres a blancos, fechas a
la fecha por defecto—, al contrario que C o COBOL.

Fíjate también en que los parámetros de esta interfaz **no llevan `const`**, mientras que en la
clase 041 sí. Es deliberado: `const` promete que el parámetro no se modifica, y aquí se modifican.
En RPG esa palabra no es decoración —con `const` el compilador acepta expresiones como argumento y
prohíbe la escritura; sin ella, el parámetro se pasa por referencia y el cambio **se ve fuera**.

Y `*inlr = *on` sigue ahí: sin él, el programa queda residente y `temp` conservaría su valor en la
siguiente llamada, exactamente la misma trampa que el `save` implícito de Fortran.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 intercambio: procedure options(main);

    declare (a, b, temp) fixed binary(31) automatic;
    declare veces        fixed binary(31) static initial(0);

    get list (a, b);

    temp = a;
    a    = b;
    b    = temp;

    veces = veces + 1;   /* static: sobrevive entre invocaciones */

    put skip list ('a=' || trim(char(a)) || ' b=' || trim(char(b)));

 end intercambio;
```

**Lo que esta clase enseña en PL/I.** Es el lenguaje de esta página que hace **más explícito el
tiempo de vida** de una variable, porque tiene cuatro clases de almacenamiento con nombre propio:

| Clase | Cuándo existe |
|---|---|
| `automatic` | Al entrar al bloque; desaparece al salir (es la de por defecto) |
| `static` | Toda la ejecución del programa; conserva su valor entre llamadas |
| `controlled` | Cuando tú lo pides con `allocate`, en una pila de asignaciones |
| `based` | Donde apunte un puntero; tú controlas la dirección |

Casi todos los lenguajes modernos tienen estas mismas categorías, pero **ocultas**: una variable
local es automática, una `static` de C es estática, y el montículo es controlado. PL/I las obliga a
escribirse. Y el atributo `initial` es la inicialización, con la misma sutileza que en Fortran: sobre
una `static` ocurre **una sola vez**, no en cada entrada.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
INTERC ; Intercambio -- clase 042
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 set temp = a, a = b, b = temp
 write "a=", a, " b=", b, !
 quit
```

**Lo que esta clase enseña en M.** La respuesta más extrema de toda la página: **no hay declaración,
no hay tipo y no hay inicialización**. Una variable empieza a existir cuando `set` le asigna algo, y
`$data(x)` es la forma de preguntar si existe. `kill x` la destruye.

Fíjate en `set temp = a, a = b, b = temp`: un solo comando `set` con varias parejas separadas por
comas, evaluadas **de izquierda a derecha**. Ese orden es lo que hace correcto el intercambio, y es
una decisión del lenguaje que hay que conocer, no suponer.

Y M tiene una pieza que casi ningún lenguaje moderno ofrece: **`new`**, que da **ámbito dinámico**.
`new x` guarda el valor actual de `x` —sea de quien sea— y lo restaura al salir de la rutina. No
crea una variable local en el sentido léxico: intercepta la global durante un rato. Es el mismo
mecanismo que `local` en Perl, y en M es la única forma de ámbito que existe.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| partes a b temp |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

temp := a.
a := b.
b := temp.

Transcript show: 'a=', a printString, ' b=', b printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** Las variables temporales se declaran entre **barras
verticales** al principio del método o del bloque —`| partes a b temp |`— y **todas nacen valiendo
`nil`**. No hay valor indeterminado ni basura: `nil` es un objeto real, la única instancia de la
clase `UndefinedObject`, al que puedes enviarle mensajes (`nil isNil` responde `true`).

Eso resuelve de un plumazo el problema que C y COBOL dejan abierto, y lo hace sin coste conceptual:
una variable sin inicializar no es un agujero, es una referencia a un objeto concreto que significa
"nada todavía".

Las temporales **no llevan tipo**, porque en Smalltalk el tipo pertenece al objeto y no al nombre.
Una misma variable puede referirse sucesivamente a un número, a una cadena y a una ventana. Lo que
determina qué se le puede hacer es **a qué mensajes responde el objeto**, no lo que prometió el
nombre — el *duck typing* en su formulación original.

---

## Y de vuelta a la clase

Doce formas de intercambiar dos números, y en ninguna el intercambio es lo interesante. Lo
interesante es lo que cada lenguaje exige **antes** de poder hacerlo: COBOL exige la forma exacta y
el sitio, Fortran exige el tipo y castiga el atajo, Ada exige un ámbito para el temporal, Tcl y
MUMPS no exigen nada, y C++ y Perl te dan el intercambio ya resuelto. Esa gradación —de la
ceremonia total a la ausencia total— es el eje que recorre toda esta parte del programa.

⏮️ [Volver a la clase 042](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
