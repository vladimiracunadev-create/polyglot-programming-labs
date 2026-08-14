# -*- coding: utf-8 -*-
"""Contenido de `vivos.md` para la Parte 3 — Valores, tipos y variables.

Cada entrada de SPECS lleva la prosa de encuadre de la clase y, por lenguaje,
el par (código, explicación). La explicación **no es una plantilla**: responde a
qué enseña *esa* clase en *ese* lenguaje. Ver `scripts/gen_vivos.py`.

El código de los ocho lenguajes de la sección 🟢 se ejecuta en CI contra el
`casos.json` de la clase (`scripts/verificar_vivos.py`).
"""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 042 — Declaración, asignación e inicialización
# ---------------------------------------------------------------------------
SPECS["042"] = dict(
    gancho="""
Intercambiar dos valores es el ejercicio mínimo que obliga a distinguir tres cosas que en el uso
diario se confunden: **declarar** (anunciar que un nombre existe y con qué forma), **inicializar**
(darle su primer valor) y **asignar** (darle otro después). Esta página lo resuelve en doce
lenguajes que llevan décadas en producción, y en cada uno la pregunta interesante es la misma:
*¿qué vale una variable en el instante en que nace?*
""",
    porque="""
Aquí el concepto es **el ciclo de vida del enlace nombre→valor**, y estos lenguajes lo enseñan
porque toman decisiones opuestas: en COBOL toda la memoria se dimensiona **antes de arrancar** y no
existe declarar dentro de un bloque; en Fortran inicializar en la declaración tiene un efecto
lateral que sorprende hasta a quien lleva años usándolo; en MUMPS **no hay declaración en absoluto**;
y en Ada puedes abrir un ámbito nuevo en mitad del código solo para nombrar un valor temporal.

Ninguna de esas cuatro respuestas es la de Python. Verlas juntas es lo que convierte "declara tus
variables" en una decisión de diseño con consecuencias.
""",
    cierre="""
Doce formas de intercambiar dos números, y en ninguna el intercambio es lo interesante. Lo
interesante es lo que cada lenguaje exige **antes** de poder hacerlo: COBOL exige la forma exacta y
el sitio, Fortran exige el tipo y castiga el atajo, Ada exige un ámbito para el temporal, Tcl y
MUMPS no exigen nada, y C++ y Perl te dan el intercambio ya resuelto. Esa gradación —de la
ceremonia total a la ausencia total— es el eje que recorre toda esta parte del programa.
""",
    langs={
        "cobol": ("""
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
""", """
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
"""),
        "fortran": ("""
program intercambio
   implicit none
   integer :: a, b, temp

   read(*, *) a, b

   temp = a
   a = b
   b = temp

   write(*, '(A,I0,A,I0)') 'a=', a, ' b=', b
end program intercambio
""", """
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
"""),
        "ada": ("""
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
""", """
**Lo que esta clase enseña en Ada.** El bloque **`declare … begin … end`** es la respuesta de Ada a
esta clase: puedes abrir un ámbito **en cualquier punto del código** solo para nombrar algo, y ese
nombre deja de existir al cerrar el bloque. `Viejo_A` no contamina el resto del procedimiento.

Y está declarado **`constant`**, que es la parte deliberada: el valor temporal de un intercambio
nunca debe reasignarse, así que se dice, y el compilador lo comprueba. Es el hábito que Ada intenta
inculcar — *declara la intención más restrictiva que sea cierta*.

Ada además distingue con precisión inicialización de asignación: `A : Integer := 0` inicializa en la
declaración, `A := 0` asigna después, y una variable sin inicializar tiene un valor **inválido** que
el compilador puede detectar con `pragma Normalize_Scalars` o con las comprobaciones activadas.
"""),
        "pascal": ("""
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
""", """
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
"""),
        "lisp": ("""
(let* ((a (read))
       (b (read)))
  ;; rotatef intercambia "en su sitio": no hace falta temporal.
  (rotatef a b)
  (format t "a=~D b=~D~%" a b))
""", """
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
"""),
        "tcl": ("""
gets stdin linea
lassign [split [string trim $linea]] a b

lassign [list $b $a] a b

puts "a=$a b=$b"
""", """
**Lo que esta clase enseña en Tcl.** **No hay declaración.** Ninguna. Una variable existe desde que
`set` le da un valor y deja de existir con `unset`; para preguntar si existe está `info exists`. No
hay tipo que declarar porque todo valor es una cadena, y no hay ámbito que declarar porque el ámbito
lo determina el procedimiento donde estás.

Eso convierte la asignación en el único acto que importa, y por eso `set` es un **comando** y no un
operador: `set a 5` son tres palabras separadas por espacios, como cualquier otra línea de Tcl.

El intercambio de aquí usa el idioma de listas —`lassign [list $b $a] a b`— que construye una lista
con los valores en el orden nuevo y la reparte. Es la versión Tcl de la asignación múltiple, y
funciona precisamente porque una lista **es** una cadena con los elementos separados por espacios.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

my ($p, $q) = split ' ', $linea;

($p, $q) = ($q, $p);          # intercambio sin variable temporal

print "a=$p b=$q\\n";
""", """
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
"""),
        "cpp": ("""
#include <iostream>
#include <utility>

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::swap(a, b);

    std::cout << "a=" << a << " b=" << b << '\\n';
    return 0;
}
""", """
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
"""),
        "rpg": ("""
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
""", """
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
"""),
        "pli": ("""
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
""", """
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
"""),
        "mumps": ("""
INTERC ; Intercambio -- clase 042
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 set temp = a, a = b, b = temp
 write "a=", a, " b=", b, !
 quit
""", """
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
"""),
        "smalltalk": ("""
| partes a b temp |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

temp := a.
a := b.
b := temp.

Transcript show: 'a=', a printString, ' b=', b printString; cr.
""", """
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
"""),
    },
)

# ---------------------------------------------------------------------------
# 043 — Tipos primitivos: enteros, reales, booleanos, caracteres
# ---------------------------------------------------------------------------
SPECS["043"] = dict(
    gancho="""
Un entero, ese mismo entero visto como real, y una pregunta de sí o no sobre él. Tres tipos
primitivos en una línea de salida, y tres preguntas incómodas detrás: **¿cuántos tipos numéricos
tiene realmente este lenguaje?**, **¿la conversión de entero a real es automática o hay que
pedirla?** y **¿existe siquiera un tipo booleano, o se finge con números?**
""",
    porque="""
Aquí el concepto es **el catálogo de tipos que un lenguaje considera fundamentales**, y estos
lenguajes lo muestran mejor que el núcleo porque **no coinciden entre sí**. COBOL no tiene tipo
booleano y lo resuelve con una construcción que no existe en ningún lenguaje moderno —los **nombres
de condición de nivel 88**—. Fortran tiene `logical` desde 1957 pero parametriza el ancho con `kind`
en vez de dar `int` y `long`. PL/I separa la **base** de la **escala**: cuatro combinaciones donde
casi todos ofrecen dos. Y Tcl y MUMPS no tienen tipos en absoluto.

Ver que "los tipos primitivos" no son una lista universal sino una decisión de cada lenguaje es
exactamente lo que esta clase quiere dejar claro.
""",
    cierre="""
La conclusión es que **no existe "el" conjunto de tipos primitivos**. Existen decisiones: COBOL
eligió el decimal exacto y prescindió del booleano, Fortran eligió el `kind` parametrizable y metió
los complejos en el lenguaje, C++ eligió una jerarquía de anchos sin tamaños garantizados, Smalltalk
eligió que no hubiera primitivos, y Tcl y MUMPS eligieron no elegir. Lo transferible no es la lista
de tipos de tu lenguaje: es saber **qué preguntas responde esa lista**.
""",
    langs={
        "cobol": ("""
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
""", """
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
"""),
        "fortran": ("""
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
""", """
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
"""),
        "ada": ("""
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
""", """
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
"""),
        "pascal": ("""
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
""", """
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
"""),
        "lisp": ("""
(let* ((n (read))
       (par (if (evenp n) "true" "false")))
  (format t "entero=~D real=~,1F par=~A~%" n (float n 1.0d0) par))
""", """
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
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

set par [expr {$n % 2 == 0 ? "true" : "false"}]

puts "entero=$n real=[format %.1f $n] par=$par"
""", """
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
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

my $par = ($n % 2 == 0) ? 'true' : 'false';

printf "entero=%d real=%.1f par=%s\\n", $n, $n, $par;
""", """
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
"""),
        "cpp": ("""
#include <iomanip>
#include <iostream>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    const double r = n;              // promoción implícita entero -> real
    const bool par = (n % 2 == 0);

    std::cout << "entero=" << n
              << " real=" << std::fixed << std::setprecision(1) << r
              << " par=" << std::boolalpha << par << '\\n';
    return 0;
}
""", """
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
"""),
        "rpg": ("""
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
""", """
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
"""),
        "pli": ("""
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
""", """
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
"""),
        "mumps": ("""
PRIM ; Tipos primitivos -- clase 043
 read n
 set par = $select(n#2 = 0 : "true", 1 : "false")
 write "entero=", n
 write " real=", $justify(n, 0, 1)
 write " par=", par, !
 quit
""", """
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
"""),
        "smalltalk": ("""
| n |

n := stdin nextLine trimBoth asNumber.

Transcript
    show: 'entero=', n printString;
    show: ' real=', (n asFloat printShowingDecimalPlaces: 1);
    show: ' par=', (n even ifTrue: [ 'true' ] ifFalse: [ 'false' ]);
    cr.
""", """
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
"""),
    },
)

# ---------------------------------------------------------------------------
# 044 — Enteros: tamaño, signo, desbordamiento y bases
# ---------------------------------------------------------------------------
SPECS["044"] = dict(
    gancho="""
Escribir el mismo número en base 10, 16, 8 y 2 parece un ejercicio de formato. No lo es: es la
prueba más rápida para descubrir **qué considera cada lenguaje que es un entero**. Si un lenguaje
piensa en el entero como un patrón de bits, la conversión a hexadecimal viene de fábrica. Si piensa
en él como una cantidad decimal de negocio, no viene — y hay que escribirla.
""",
    porque="""
Esta es la clase donde la lista se parte en dos mitades limpias. **Fortran, Lisp, Perl y C++ te dan
las bases hechas**, porque su entero es una palabra de máquina o un objeto matemático. **COBOL, Ada,
Pascal, RPG y PL/I no**, y hay que escribir la conversión a mano — no por descuido de sus
diseñadores, sino porque en banca, seguros y aviónica *no existe* la necesidad de imprimir un saldo
en octal. La herramienta refleja el dominio.

Y en medio queda Tcl, que tiene `%x` y `%o` pero **no `%b`**: un recordatorio de que estas
capacidades se añaden una a una, cuando alguien las necesita, y no en bloque.
""",
    cierre="""
La lección es que **"pasar a hexadecimal" no es una operación universal**: es una facilidad que un
lenguaje ofrece si su idea de entero es el patrón de bits. Cuando la escribes a mano —en COBOL, en
Ada, en Pascal— redescubres el algoritmo de división sucesiva que hay debajo de `%x`, y esa es
precisamente la parte transferible. La otra lección, la incómoda, es que el desbordamiento sigue
esperando: `PIC 9(9)` desborda a los mil millones, un `int` de C++ a los 2147483647, y solo Lisp y
Smalltalk se niegan a desbordar.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. BASES.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA     PIC X(80).
01  N         PIC 9(9) COMP-3.
01  ED-N      PIC Z(8)9.
01  DIGITOS   PIC X(16) VALUE "0123456789abcdef".
01  VALOR     PIC 9(9) COMP-3.
01  BASE      PIC 9(2) COMP-3.
01  RESTO     PIC 9(2) COMP-3.
01  IDX       PIC 9(2) COMP-3.
01  POS       PIC 9(2) COMP-3.
01  BUFFER    PIC X(40).
01  HEX-TXT   PIC X(40).
01  OCT-TXT   PIC X(40).
01  BIN-TXT   PIC X(40).

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N

    MOVE 16 TO BASE
    PERFORM CONVERTIR
    MOVE BUFFER TO HEX-TXT

    MOVE 8 TO BASE
    PERFORM CONVERTIR
    MOVE BUFFER TO OCT-TXT

    MOVE 2 TO BASE
    PERFORM CONVERTIR
    MOVE BUFFER TO BIN-TXT

    MOVE N TO ED-N
    DISPLAY "dec=" FUNCTION TRIM(ED-N)
            " hex=" FUNCTION TRIM(HEX-TXT)
            " oct=" FUNCTION TRIM(OCT-TXT)
            " bin=" FUNCTION TRIM(BIN-TXT)
    STOP RUN.

CONVERTIR.
    MOVE SPACES TO BUFFER
    MOVE N TO VALOR
    MOVE 40 TO POS
    IF VALOR = 0
        MOVE "0" TO BUFFER(40:1)
    ELSE
        PERFORM UNTIL VALOR = 0
            COMPUTE RESTO = FUNCTION MOD(VALOR, BASE)
            COMPUTE IDX = RESTO + 1
            MOVE DIGITOS(IDX:1) TO BUFFER(POS:1)
            SUBTRACT 1 FROM POS
            COMPUTE VALOR = VALOR / BASE
        END-PERFORM
    END-IF.
""", """
**Lo que esta clase enseña en COBOL.** **COBOL no sabe imprimir en hexadecimal**, y la razón es
coherente con todo lo demás: su entero no es un patrón de bits, es **una cantidad decimal con un
número de dígitos declarado**. `PIC 9(9)` no significa "32 bits", significa "nueve dígitos". La
pregunta "¿cómo se ve esto en base 16?" simplemente no se plantea cuando el dato es el saldo de una
cuenta.

Así que el algoritmo hay que escribirlo, y al escribirlo se ve lo que `%x` esconde: **divisiones
sucesivas quedándose con el resto**, llenando el resultado de derecha a izquierda. `BUFFER(POS:1)` es
**modificación de referencia**, la forma de COBOL de indexar dentro de un campo: `campo(inicio:largo)`.

Y hay un detalle de esta clase que COBOL trata mejor que casi nadie: **el desbordamiento**. Un
`PIC 9(9)` que recibe mil millones **trunca por la izquierda en silencio** —igual que C—, salvo que
lo pidas explícitamente:

```cobol
COMPUTE TOTAL = A * B
    ON SIZE ERROR DISPLAY "desbordamiento"
END-COMPUTE
```

`ON SIZE ERROR` es una cláusula del propio verbo aritmético. No es una excepción global ni un flag
del compilador: es una rama del `COMPUTE`, escrita al lado de la operación que puede desbordar.
"""),
        "fortran": ("""
program bases
   implicit none
   integer :: n, i
   character(len=40) :: hex, oct, bin

   read(*, *) n

   write(hex, '(Z0)') n
   write(oct, '(O0)') n
   write(bin, '(B0)') n

   do i = 1, len_trim(hex)
      if (iachar(hex(i:i)) >= iachar('A') .and. &
          iachar(hex(i:i)) <= iachar('F')) then
         hex(i:i) = achar(iachar(hex(i:i)) + 32)
      end if
   end do

   write(*, '(A,I0,A,A,A,A,A,A)') 'dec=', n, ' hex=', trim(hex), &
        ' oct=', trim(oct), ' bin=', trim(bin)
end program bases
""", """
**Lo que esta clase enseña en Fortran.** Fortran **sí** trae las bases, y de una forma que no tiene
ningún otro lenguaje de esta página: como **descriptores de edición** dentro del formato, junto a `I`
para decimal y `F` para real.

| Descriptor | Base |
|---|---|
| `I` | 10 |
| `Z` | 16 |
| `O` | 8 |
| `B` | 2 |

El `0` de `'(Z0)'` pide **ancho mínimo**: sin él habría que decir cuántas columnas ocupa. Que las
cuatro bases sean descriptores del sistema de formato, y no funciones de biblioteca, es muy propio
de Fortran: el formato es un mini-lenguaje con entidad propia, igual que el `format` de Lisp.

Lo único que falta es minúsculas —`Z` produce `FF`, no `ff`—, y por eso el bucle de conversión.
`achar` e `iachar` son las funciones que van de código ASCII a carácter y al revés; existen también
`char` e `ichar`, que usan el juego de caracteres del procesador. Que haya dos parejas es una
concesión a las máquinas que no eran ASCII, un rastro más de 1957.

Sobre el desbordamiento: un `integer` por defecto son 32 bits y **desborda en silencio**. Con
`gfortran -fcheck=all` se detecta en ejecución, y con `integer(int64)` se pospone.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Bases is

   Digitos : constant String := "0123456789abcdef";

   --  Recursiva: divisiones sucesivas, de la más significativa a la última.
   function En_Base (N : Natural; B : Positive) return String is
   begin
      if N < B then
         return (1 => Digitos (N + 1));
      else
         return En_Base (N / B, B) & Digitos (N rem B + 1);
      end if;
   end En_Base;

   N : Integer;
begin
   Get (N);

   Put ("dec=");  Put (N, Width => 1);
   Put (" hex=" & En_Base (N, 16));
   Put (" oct=" & En_Base (N, 8));
   Put (" bin=" & En_Base (N, 2));
   New_Line;
end Bases;
""", """
**Lo que esta clase enseña en Ada.** Ada **sí** tiene salida en otras bases —`Put (N, Base => 16)`—
pero produce `16#FF#`, que es el **literal basado** del propio lenguaje, con la base delante y el
número entre almohadillas. Es coherente y es inutilizable aquí, así que el programa escribe la
conversión.

Y esa notación es lo que hay que llevarse de esta clase: en Ada puedes **escribir** literales en
cualquier base de 2 a 16, en el código fuente:

```ada
Mascara  : constant := 2#1111_0000#;   --  binario, con subrayados
Color    : constant := 16#FF_A0_20#;   --  hexadecimal
Permisos : constant := 8#755#;         --  octal
```

Compara con C y sus prefijos `0x`, `0` y `0b`: en Ada la base es un número explícito delante, así que
funciona para **cualquier** base, no solo para tres privilegiadas. Es un caso claro de generalidad
por diseño.

Sobre el desbordamiento, aquí Ada se separa de casi todos: **no desborda en silencio**. Superar
`Integer'Last` levanta `Constraint_Error` en el punto exacto. Y los atributos `Integer'First`,
`Integer'Last`, `Integer'Size` permiten preguntar los límites al propio tipo en vez de consultarlos
en un manual.
"""),
        "pascal": ("""
program Bases;
{$MODE OBJFPC}{$H+}
uses SysUtils;

function EnBase(N, B: Integer): string;
const
  DIGITOS = '0123456789abcdef';
begin
  if N < B then
    Result := DIGITOS[N + 1]
  else
    Result := EnBase(N div B, B) + DIGITOS[N mod B + 1];
end;

var
  N: Integer;

begin
  Read(N);
  WriteLn('dec=', IntToStr(N),
          ' hex=', EnBase(N, 16),
          ' oct=', EnBase(N, 8),
          ' bin=', EnBase(N, 2));
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal distingue **dos operadores de división**, y esta clase
es donde se nota: `div` es división entera y `/` **siempre** da un `Real`, incluso entre enteros.
`7 div 2` es `3`; `7 / 2` es `3.5` y no puede asignarse a un `Integer`. En C, en Java y en Go, `7/2`
da `3` y hay que recordar que el tipo decide; en Pascal el operador lo dice.

Sobre las bases: el Pascal ISO no tiene conversión, y Free Pascal añade `IntToHex` y `BinStr`/`OctStr`
—que rellenan con ceros a la izquierda hasta el ancho que pidas—. Escribir `EnBase` a mano evita esa
asimetría y muestra el algoritmo.

Los literales sí traen notación de base, heredada de Turbo Pascal, con un símbolo distinto por base:

```pascal
const
  Mascara = %11110000;   { binario }
  Color   = $FFA020;     { hexadecimal }
  Permiso = &755;        { octal }
```

Y sobre el desbordamiento, Free Pascal tiene una directiva que casi nadie activa y debería:
`{$Q+}` comprueba el desbordamiento aritmético en ejecución y `{$R+}` comprueba los rangos de índices
y subrangos. Con ellas, Pascal se comporta como Ada; sin ellas, como C.
"""),
        "lisp": ("""
(let ((n (read)))
  (format t "dec=~D hex=~(~X~) oct=~O bin=~B~%" n n n n))
""", """
**Lo que esta clase enseña en Common Lisp.** Una línea. `format` trae las cuatro bases como
directivas —`~D`, `~X`, `~O`, `~B`— y además `~R`, que imprime en **cualquier** base:
`(format nil "~3R" 255)` da `"100110"` en base 3. Y `~R` sin argumento numérico escribe el número
**en palabras**: `(format nil "~R" 255)` da `"two hundred fifty-five"`.

El `~(` … `~)` que envuelve al `~X` es una **directiva de conversión de mayúsculas y minúsculas**:
todo lo que se produzca dentro sale en minúsculas. `format` no es una función de formateo: es un
lenguaje completo empotrado, con condicionales (`~[`), iteración sobre listas (`~{`), pluralización
(`~P`) y recursión (`~?`).

Los literales también admiten cualquier base con `#<base>r`:

```lisp
#b1111        ; binario   -> 15
#o755         ; octal     -> 493
#xFF          ; hexa      -> 255
#3r210        ; base 3    -> 21
```

Y la parte que hace único a Lisp en esta clase: **sus enteros no desbordan**. `(expt 2 200)` devuelve
el número completo, de 61 dígitos. No hay tamaño, no hay signo que se voltee, no hay
comportamiento indefinido. El desbordamiento —el tema central de esta clase en casi todos los demás
lenguajes— sencillamente no existe aquí.
"""),
        "tcl": ("""
proc enBase {n b} {
    set digitos "0123456789abcdef"
    if {$n < $b} { return [string index $digitos $n] }
    return "[enBase [expr {$n / $b}] $b][string index $digitos [expr {$n % $b}]]"
}

gets stdin linea
set n [string trim $linea]

puts "dec=$n hex=[format %x $n] oct=[format %o $n] bin=[enBase $n 2]"
""", """
**Lo que esta clase enseña en Tcl.** Un ejemplo perfecto de que estas capacidades **se añaden de una
en una**: `format` de Tcl tiene `%x` y `%o`, heredados de `printf` de C, pero **no tiene `%b`**,
porque `printf` de C tampoco lo tiene. Nadie lo echó de menos lo suficiente durante décadas. Así que
el binario hay que escribirlo, mientras que hexadecimal y octal vienen hechos — una asimetría que no
responde a ninguna lógica del lenguaje, solo a su historia.

Para la dirección contraria, Tcl tiene `scan`, que es el `sscanf` de C: `scan ff %x valor` deja 255
en `valor`. Y desde Tcl 8.5 los literales aceptan `0x`, `0o` y `0b`.

Fíjate también en cómo se construye el resultado recursivo: `"[enBase ...][string index ...]"` —dos
sustituciones de comando **pegadas dentro de una cadena entre comillas**. En Tcl no hace falta
operador de concatenación porque la interpolación de cadenas ya concatena. Es el mismo principio de
siempre: todo es texto, así que juntar dos cosas es escribirlas seguidas.

Y sobre el desbordamiento: desde Tcl 8.5, **los enteros son de precisión arbitraria**, como en Lisp.
`expr {2**200}` funciona.
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

printf "dec=%d hex=%x oct=%o bin=%b\\n", $n, $n, $n, $n;
""", """
**Lo que esta clase enseña en Perl.** Perl es el único de esta página que trae las **cuatro** bases
en `printf` sin excepciones: `%d`, `%x`, `%o` y `%b`. El `%b` que le falta a C y a Tcl aquí sí está,
porque Perl añadió lo que la gente pedía en vez de limitarse a envolver la biblioteca de C.

La dirección contraria también es de una línea, con `oct`, que a pesar del nombre entiende los tres
prefijos:

```perl
my $x = hex("ff");      # 255
my $y = oct("0xff");    # 255  — oct reconoce 0x, 0b y 0
my $z = oct("0b1010");  # 10
```

Y los literales admiten **subrayados como separadores**, en cualquier base:
`0xFF_A0_20`, `0b1111_0000`, `1_000_000`.

Sobre el desbordamiento, Perl hace algo característico suyo y discutible: cuando un entero no cabe
en la palabra de máquina, **lo convierte a real en silencio** y sigue. No falla y no avisa; empiezas
a perder precisión sin enterarte. Si necesitas exactitud sin límite, el módulo `bigint` de la
biblioteca estándar cambia el comportamiento del programa entero con una sola línea `use bigint;`.
"""),
        "cpp": ("""
#include <iostream>
#include <string>

std::string en_base(unsigned long n, unsigned base) {
    static const char* digitos = "0123456789abcdef";
    if (n < base) return std::string(1, digitos[n]);
    return en_base(n / base, base) + digitos[n % base];
}

int main() {
    unsigned long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "dec=" << n
              << " hex=" << en_base(n, 16)
              << " oct=" << en_base(n, 8)
              << " bin=" << en_base(n, 2) << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ tiene `std::hex` y `std::oct` como manipuladores de flujo,
pero **no tiene `std::bin`**: la misma laguna que Tcl y por el mismo motivo, la herencia de `printf`.
Para binario está `std::bitset`, que rellena con ceros hasta un ancho fijo, o —desde C++20—
`std::format("{:b}", n)`, que por fin lo resuelve bien.

Y hay una trampa clásica que conviene conocer: **`std::hex` es pegajoso**. Cambia el estado del flujo
y **sigue activo** para todo lo que se escriba después, hasta que alguien ponga `std::dec`. Más de un
número decimal ha salido en hexadecimal por esto. Es el mismo defecto de diseño que `std::fixed` y
`std::setprecision`, y es la razón por la que `std::format` y `std::print` los sustituyen.

Fíjate en que este programa usa `unsigned long`, no `int`. Es deliberado: **el desplazamiento y el
desbordamiento de un entero con signo son comportamiento indefinido en C++**, no un valor
sorprendente sino una licencia para que el compilador asuma que nunca ocurre y optimice en
consecuencia. Con `unsigned`, el estándar sí define la aritmética modular. Cuando se manipulan
patrones de bits, `unsigned` no es una preferencia: es lo correcto.

Los literales llevan las tres bases —`0xFF`, `0755`, `0b1111` (C++14)— y desde C++14 la comilla
simple separa: `0b1111'0000`.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller) main(Bases);

dcl-c DIGITOS '0123456789abcdef';

dcl-proc Bases;
  dcl-pi *n;
    n int(10) const;
  end-pi;

  dcl-s salida char(80);

  salida = 'dec=' + %char(n)
         + ' hex=' + enBase(n : 16)
         + ' oct=' + enBase(n : 8)
         + ' bin=' + enBase(n : 2);
  dsply salida;
end-proc;

dcl-proc enBase;
  dcl-pi *n varchar(64);
    v int(10) const;
    b int(10) const;
  end-pi;

  if v < b;
    return %subst(DIGITOS : v + 1 : 1);
  endif;
  return enBase(%div(v : b) : b) + %subst(DIGITOS : %rem(v : b) + 1 : 1);
end-proc;
""", """
**Lo que esta clase enseña en RPG.** Igual que COBOL: **no hay conversión de base**, porque el dato
de un ERP es una cantidad, no un patrón de bits. Lo más cercano son las APIs del sistema `CVTHC` y
`CVTCH` (*convert hex to char* y viceversa), que se llaman como programas del sistema operativo, no
como funciones del lenguaje.

Lo interesante de esta versión es otra cosa: **`main()` en `ctl-opt`**. Al declarar un procedimiento
principal, el programa deja de usar el **ciclo de RPG** y se comporta como un `main` de C — sin
indicadores, sin `*inlr`, con variables locales de verdad en cada `dcl-proc`. Es el RPG moderno, y
convive en la misma plataforma con programas que siguen usando el ciclo de 1959.

`%div` y `%rem` son las funciones de división entera y resto. Existen aparte porque el operador `/`
en RPG **redondea** al número de decimales del destino: `7 / 2` guardado en un entero da **4**, no 3.
Es una de las diferencias más peligrosas al portar código desde C o Java, y la razón de que RPG
obligue a pedir la división entera por su nombre.
"""),
        "pli": ("""
 bases: procedure options(main);

    declare n       fixed binary(31);
    declare digitos character(16) initial('0123456789abcdef');

    declare en_base entry (fixed binary(31), fixed binary(31))
                    returns (character(64) varying) recursive;

    get list (n);

    put skip list ('dec='  || trim(char(n))     ||
                   ' hex=' || en_base(n, 16)    ||
                   ' oct=' || en_base(n, 8)     ||
                   ' bin=' || en_base(n, 2));

 en_base: procedure (v, b) returns (character(64) varying) recursive;
    declare (v, b) fixed binary(31);
    if v < b then
       return (substr(digitos, v + 1, 1));
    return (en_base(divide(v, b, 31), b) || substr(digitos, mod(v, b) + 1, 1));
 end en_base;

 end bases;
""", """
**Lo que esta clase enseña en PL/I.** Tampoco tiene conversión de base para presentación, pero sí
tiene algo que ningún otro lenguaje de esta página ofrece: **`unspec`**, que devuelve la
representación **en bits** de cualquier variable, del tipo que sea.

```pli
declare patron bit(32);
patron = unspec(n);        /* los bits crudos del entero */
```

Y funciona al revés: `unspec(x) = patron` reinterpreta los bits como el tipo de `x`. Es el
antepasado de `reinterpret_cast` de C++ y de `std::bit_cast`, disponible en 1964 y aplicable a
cualquier tipo, incluidas estructuras completas.

Fíjate también en `divide(v, b, 31)`: la división en PL/I es una **función con la precisión del
resultado como argumento**. `divide(a, b, 15, 2)` significa "divide y dame el resultado con 15
dígitos, 2 de ellos decimales". En un lenguaje que distingue base y escala, el resultado de una
división no se puede deducir de los operandos: hay que decirlo. Es verboso y es exacto.

Y `recursive` es una palabra que hay que escribir: en PL/I, como en el COBOL clásico, un
procedimiento **no es recursivo por defecto**, porque su almacenamiento es estático salvo que se
diga otra cosa.
"""),
        "mumps": ("""
BASES ; Bases numericas -- clase 044
 read n
 write "dec=", n
 write " hex=", $$base(n, 16)
 write " oct=", $$base(n, 8)
 write " bin=", $$base(n, 2), !
 quit
 ;
base(v, b) ; v escrito en base b
 new d
 set d = "0123456789abcdef"
 quit:v<b $extract(d, v + 1)
 quit $$base(v\\b, b) _ $extract(d, (v#b) + 1)
""", """
**Lo que esta clase enseña en M.** M no tiene bases —previsible, en un lenguaje sin tipos
numéricos—, pero la implementación muestra tres rasgos que definen el lenguaje.

El primero es **`$$etiqueta(args)`**, la llamada a una *función extrínseca*: una etiqueta normal que
devuelve un valor con `quit <valor>`. El doble dólar la distingue de las funciones incorporadas, que
llevan uno solo (`$piece`, `$extract`, `$select`).

El segundo son los **operadores de una sola letra o símbolo**: `\\` es división entera —no una barra
invertida de escape—, `#` es módulo y `_` es concatenación. Que la concatenación sea el subrayado
sorprende siempre, y es la razón de que en M los nombres de variable no lleven subrayados.

El tercero es **`quit:v<b <valor>`**, el postcondicional. Casi cualquier comando admite `:condición`
pegada detrás para ejecutarse solo si se cumple. `quit:v<b ...` es el caso base de la recursión
escrito en once caracteres, sin `if` y sin bloque. Es a la vez la mayor virtud y el mayor obstáculo
del lenguaje: densidad extrema, legible solo cuando ya lo conoces.

Y `new d` da **ámbito dinámico** a `d` durante la llamada, que es la única forma de variable local
que existe en M.
"""),
        "smalltalk": ("""
| n |

n := stdin nextLine trimBoth asInteger.

Transcript
    show: 'dec=', n printString;
    show: ' hex=', (n printStringBase: 16) asLowercase;
    show: ' oct=', (n printStringBase: 8);
    show: ' bin=', (n printStringBase: 2);
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** `printStringBase:` es un **mensaje enviado al número**, y
acepta cualquier base entre 2 y 36. No es una función de biblioteca ni una directiva de formato: es
un método de la clase `Integer`, que puedes abrir, leer y —si quisieras— redefinir.

Los literales usan la misma idea, con la base delante y una `r` de *radix*:

```smalltalk
16rFF        "255"
2r1111_0000  "240, con subrayados desde Pharo 8"
36rZZ        "1295 — base 36, dígitos 0-9 y A-Z"
```

Que funcione hasta base 36 no es un adorno: es consecuencia de que la conversión sea código normal en
vez de una tabla privilegiada del compilador.

Y aquí, como en Lisp, **el desbordamiento no existe**. `SmallInteger` se convierte en
`LargePositiveInteger` de forma automática e invisible cuando el valor no cabe, y
`(2 raisedTo: 1000) printStringBase: 16` devuelve la cadena completa. En un lenguaje donde el entero
es un objeto y no una palabra de máquina, el tamaño deja de ser una propiedad del tipo y pasa a ser
un detalle de implementación.
"""),
    },
)

# ---------------------------------------------------------------------------
# 045 — Números reales: punto flotante, precisión y decimales
# ---------------------------------------------------------------------------
SPECS["045"] = dict(
    gancho="""
Sumar `0.1` y `0.2`. El caso de prueba más famoso de la informática, y el que separa a los lenguajes
en dos familias: los que calculan en **binario** —donde `0.1` no existe exactamente y la suma da
`0.30000000000000004`— y los que calculan en **decimal**, donde da `0.30` y punto. Esta página tiene
representantes de las dos, y la diferencia no es académica: es la razón de que la banca no use
`double`.
""",
    porque="""
Aquí el concepto es **la representación de los reales y su error acumulado**, y estos lenguajes lo
enseñan porque **algunos eligieron no tener el problema**. COBOL, RPG y PL/I usan aritmética decimal
de coma fija: `0.1 + 0.2` da exactamente `0.30` porque nunca pasan por binario. Fortran y Ada
eligieron lo contrario —binario IEEE— porque su dominio es el cálculo científico, donde el error
relativo importa más que el céntimo exacto.

Que dos familias de lenguajes tomaran decisiones opuestas **por buenas razones** es la lección de
esta clase. No hay una representación correcta: hay una correcta *para tu dominio*.
""",
    cierre="""
Si te llevas una sola cosa de esta página, que sea esta: **`double` no es el tipo de los números con
decimales, es el tipo de las magnitudes físicas**. Para dinero, para porcentajes contractuales y para
cualquier cifra que alguien vaya a cuadrar a mano, el tipo correcto es el decimal exacto — y esos
lenguajes de sesenta años lo tienen de serie, mientras que Java, C# y Python tuvieron que añadirlo
después con `BigDecimal`, `decimal` y `Decimal`.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. REALES.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA     PIC X(80).
01  TXT-A     PIC X(20).
01  TXT-B     PIC X(20).
01  A         PIC S9(9)V9(4) COMP-3.
01  B         PIC S9(9)V9(4) COMP-3.
01  SUMA      PIC S9(9)V99   COMP-3.
01  PRODUCTO  PIC S9(9)V99   COMP-3.
01  ED-S      PIC -(9)9.99.
01  ED-P      PIC -(9)9.99.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    COMPUTE SUMA     ROUNDED = A + B
    COMPUTE PRODUCTO ROUNDED = A * B

    MOVE SUMA     TO ED-S
    MOVE PRODUCTO TO ED-P
    DISPLAY "suma=" FUNCTION TRIM(ED-S)
            " producto=" FUNCTION TRIM(ED-P)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** **En COBOL, `0.1 + 0.2` da `0.30`. Exactamente.** No por
suerte ni por redondeo al imprimir: porque `PIC S9(9)V9(4) COMP-3` **no es punto flotante**. Es
decimal empaquetado —cada dígito decimal en medio byte— y la aritmética es decimal de principio a
fin. El número `0.1` se guarda como el dígito 1 en la primera posición decimal, no como la
aproximación binaria más cercana.

Esa es la respuesta de COBOL a esta clase, y explica su supervivencia mejor que ningún argumento
sobre coste de migración.

COBOL **sí** tiene punto flotante binario si lo quieres —`COMP-1` es de 32 bits y `COMP-2` de 64—,
y son los tipos correctos para cálculo científico. Lo que COBOL hace bien es **obligarte a elegir**:
el tipo se declara, así que la decisión "esto es dinero, esto es una magnitud" queda escrita.

Y `ROUNDED` no es opcional por descuido: sin él, `COMPUTE` **trunca** al guardar. En dinero, decidir
entre truncar y redondear es una decisión de negocio, y COBOL la pone en la sentencia. Además admite
la política: `ROUNDED MODE IS NEAREST-EVEN`, `TOWARD-GREATER`, `PROHIBITED`…
"""),
        "fortran": ("""
program reales
   implicit none
   real(kind=8) :: a, b
   character(len=32) :: bs, bp

   read(*, *) a, b

   write(bs, '(F20.2)') a + b
   write(bp, '(F20.2)') a * b

   write(*, '(A,A,A,A)') 'suma=', trim(adjustl(bs)), &
                         ' producto=', trim(adjustl(bp))
end program reales
""", """
**Lo que esta clase enseña en Fortran.** Fortran es el lado opuesto de COBOL, y con la misma buena
razón: en simulación climática o en dinámica de fluidos **no existe el valor exacto**. Los datos
vienen de sensores con error, el modelo es una aproximación, y lo que importa es el **error relativo
acumulado a lo largo de mil millones de operaciones**. El punto flotante binario IEEE 754 es la
herramienta correcta para eso, y aquí `0.1 + 0.2` da `0.30000000000000004`, como debe ser.

Por eso Fortran trae herramientas para **preguntar por la precisión** que casi ningún lenguaje ofrece:

```fortran
epsilon(1.0d0)   ! el menor x tal que 1+x /= 1  -> ~2.2e-16
huge(1.0d0)      ! el mayor representable
tiny(1.0d0)      ! el menor positivo normalizado
precision(1.0d0) ! dígitos decimales significativos -> 15
nearest(x, 1.0)  ! el siguiente representable hacia arriba
```

Estas funciones son la razón de que el código numérico serio se escriba en Fortran: permiten
comparar con tolerancia de forma disciplinada —`abs(a - b) < epsilon(a) * abs(a)`— en vez del `==`
que nunca hay que usar con reales.

Y el detalle del programa: `F20.2` en un buffer y luego `trim(adjustl(...))`, en lugar de `F0.2`
directo. `F0.2` pide ancho mínimo, pero **su comportamiento con el cero varía entre compiladores**
—algunos escriben `.00` sin el cero inicial—, y el contrato de la clase exige la misma salida en
todas partes.
"""),
        "ada": ("""
with Ada.Text_IO;            use Ada.Text_IO;
with Ada.Long_Float_Text_IO; use Ada.Long_Float_Text_IO;

procedure Reales is
   A, B : Long_Float;
begin
   Get (A);
   Get (B);

   Put ("suma=");      Put (A + B, Fore => 1, Aft => 2, Exp => 0);
   Put (" producto="); Put (A * B, Fore => 1, Aft => 2, Exp => 0);
   New_Line;
end Reales;
""", """
**Lo que esta clase enseña en Ada.** Ada es el único lenguaje de esta página que te deja **declarar
la precisión que necesitas y hacer que el compilador la garantice**, en lugar de elegir entre `float`
y `double` y esperar que baste:

```ada
type Temperatura is digits 6  range -273.15 .. 1000.0;   --  coma flotante
type Euros       is delta 0.01 range 0.0 .. 1.0e9;       --  COMA FIJA
```

`digits 6` pide **al menos** seis dígitos significativos: si la máquina no puede, **no compila**.
Nada de descubrir en producción que `float` no daba para tanto.

Y `delta 0.01` es lo importante para esta clase: declara un **tipo de coma fija**, con incrementos
exactos de un céntimo. Ada tiene aritmética decimal exacta **en el sistema de tipos**, igual que
COBOL, pero expresada como una propiedad del tipo en lugar de como una plantilla de dígitos. Existe
además `type Dinero is delta 0.01 digits 12` —coma fija **decimal**— pensada explícitamente para
interoperar con COBOL en sistemas mixtos.

Así que Ada no elige bando en el debate de esta clase: te da las dos representaciones y te obliga a
decir cuál usas y con qué garantías.
"""),
        "pascal": ("""
program Reales;
{$MODE OBJFPC}{$H+}

var
  A, B: Double;

begin
  Read(A, B);

  WriteLn('suma=', (A + B):0:2, ' producto=', (A * B):0:2);
end.
""", """
**Lo que esta clase enseña en Pascal.** El formateo `valor:ancho:decimales` está **en la sintaxis del
`Write`**, no en una cadena de plantilla, y eso tiene una consecuencia que se agradece: **no depende
de la configuración regional**. En un equipo configurado en español, `Format('%.2f', [x])` de Delphi
produce `0,30` con coma; `x:0:2` produce siempre `0.30` con punto.

Ese detalle ha roto más integraciones de las que parece: un fichero CSV generado en un servidor
español que el sistema receptor no puede leer. Cuando el destino es una máquina y no una persona,
el formateo independiente de la configuración regional no es una preferencia estética.

Sobre la representación, Free Pascal y Delphi ofrecen la escala completa —`Single` (32 bits), `Double`
(64), `Extended` (80 en x86)— y, para esta clase, lo importante: **`Currency`**, un entero de 64 bits
escalado con **cuatro decimales fijos**, es decir, decimal exacto para dinero. Es el mismo tipo que
tiene [VBA](../../../atlas/vba.md), y por el mismo motivo: los dos vienen del mundo de las
aplicaciones de gestión.

`Extended` de 80 bits merece una nota: es un tipo real del x87 que ya casi nadie usa y que **no
existe en x86-64 con SSE ni en ARM**. Código antiguo que dependía de esos bits de más da resultados
distintos al recompilarlo hoy.
"""),
        "lisp": ("""
(setf *read-default-float-format* 'double-float)

(let* ((a (read))
       (b (read)))
  (format t "suma=~,2F producto=~,2F~%" (+ a b) (* a b)))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp tiene una tercera respuesta, distinta de la de
COBOL y de la de Fortran: **los racionales exactos**.

```lisp
(+ 1/10 2/10)     ; => 3/10     exacto, sin error
(+ 0.1d0 0.2d0)   ; => 0.30000000000000004d0
(rationalize 0.1) ; => 1/10     la fracción "que el humano quería decir"
(rational 0.1)    ; => 3602879701896397/36028797018963968  el valor REAL del double
```

Esas dos últimas líneas son la mejor demostración pedagógica que existe del problema de esta clase.
`rational` te enseña **qué número guarda de verdad un `double` cuando escribiste `0.1`**: no es una
décima, es una fracción de denominador 2⁵⁵. `rationalize` devuelve la fracción simple más probable.
Ver los dos resultados juntos explica el punto flotante mejor que cualquier párrafo.

Y la aritmética se comporta en consecuencia: mientras trabajas con racionales, todo es exacto; en
cuanto entra un `float`, el resultado se **contagia** y pasa a ser aproximado. La regla de contagio
está en el estándar y es predecible.

`*read-default-float-format*` en la primera línea es necesario porque, sin ella, `0.1` se leería como
precisión simple y los errores serían mucho mayores.
"""),
        "tcl": ("""
gets stdin linea
lassign [split [string trim $linea]] a b

set suma     [expr {$a + $b}]
set producto [expr {$a * $b}]

puts "suma=[format %.2f $suma] producto=[format %.2f $producto]"
""", """
**Lo que esta clase enseña en Tcl.** Tcl usa `double` IEEE para todo lo que no sea entero, así que
hereda el problema entero de esta clase. Pero tiene una peculiaridad interesante: como **el valor
canónico es la cadena**, la representación textual de un real importa mucho más que en otros
lenguajes.

Por eso Tcl 8.5 cambió a un algoritmo que garantiza el **viaje de ida y vuelta**: la cadena que
produce Tcl para un `double` es la más corta que, al volver a leerse, da **exactamente el mismo
double**. `expr {0.1 + 0.2}` muestra `0.30000000000000004` — no redondea para que quede bonito,
porque hacerlo rompería la identidad entre el valor y su texto.

Es la misma decisión que tomaron después JavaScript, Python 3 y Go, y en Tcl era obligatoria en vez
de deseable.

Para dinero, la comunidad recomienda dos caminos: trabajar en **enteros de céntimos** —posible
porque los enteros de Tcl son de precisión arbitraria— o usar el paquete `math::bignum` de Tcllib.
Nunca `double`.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($x, $y) = split ' ', $linea;

printf "suma=%.2f producto=%.2f\\n", $x + $y, $x * $y;
""", """
**Lo que esta clase enseña en Perl.** Perl guarda los reales como `double` de C, con el mismo
comportamiento, y añade un matiz propio: como su escalar mantiene a la vez la representación
numérica y la textual, **`0.1 + 0.2` impreso con `print` da `0.3`**, no `0.30000000000000004`.

Eso no es que Perl calcule mejor: es que su conversión a texto por defecto usa **15 dígitos
significativos** en vez de los 17 necesarios para el viaje de ida y vuelta, y el error queda escondido
justo debajo del corte. El bug sigue ahí:

```perl
printf "%.17g\\n", 0.1 + 0.2;   # 0.30000000000000004
print 0.1 + 0.2 == 0.3 ? "sí" : "no";   # no
```

Es un buen recordatorio de que **"se imprime bien" no significa "es exacto"**, y de que la
comparación de reales con `==` es un error en cualquier lenguaje.

Para dinero, CPAN ofrece las dos soluciones clásicas: `Math::BigFloat` para precisión arbitraria y
`bignum` como pragma que cambia el comportamiento de todo el ámbito. Y para saber qué está pasando
de verdad, `Data::Float` expone las piezas del IEEE 754.
"""),
        "cpp": ("""
#include <iomanip>
#include <iostream>

int main() {
    double a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::cout << std::fixed << std::setprecision(2)
              << "suma=" << (a + b)
              << " producto=" << (a * b) << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ hereda el punto flotante de C y expone sus propiedades a
través de `std::numeric_limits`, que es la versión con tipos de las funciones `epsilon`, `huge` y
`tiny` de Fortran:

```cpp
#include <limits>
std::numeric_limits<double>::epsilon();        // 2.22045e-16
std::numeric_limits<double>::max();
std::numeric_limits<double>::infinity();
std::numeric_limits<double>::quiet_NaN();
std::numeric_limits<double>::is_iec559;        // ¿cumple IEEE 754?
```

Esa última línea es la que importa en código serio: **el estándar de C++ no obliga a que `double` sea
IEEE 754**. Casi siempre lo es, y `is_iec559` lo dice.

Y hay dos trampas de esta clase que C++ enseña bien. La primera: `std::setprecision` **cambia de
significado** según haya o no `std::fixed`. Con `std::fixed` son decimales después del punto; sin él,
son **dígitos significativos totales**. La segunda: las dos son **pegajosas** —afectan a todo lo que
se escriba después en ese flujo—, igual que `std::hex`.

Para dinero, C++ no trae decimal en la biblioteca estándar. Se usa `boost::multiprecision`, una clase
propia sobre enteros de céntimos, o el tipo decimal de la propuesta ISO TR 24733, que sigue sin
adoptarse. Es una carencia real frente a COBOL, RPG y PL/I.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi REALES;
  a packed(15:4) const;
  b packed(15:4) const;
end-pi;

dcl-s suma     packed(15:2);
dcl-s producto packed(15:2);
dcl-s salida   char(80);

suma     = a + b;
producto = a * b;

salida = 'suma=' + %char(suma) + ' producto=' + %char(producto);
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** Como COBOL: `packed(15:4)` es **decimal exacto**, así que
`0.1 + 0.2` da `0.30` sin discusión. RPG tiene `float(4)` y `float(8)` para punto flotante binario,
y la guía de estilo de la plataforma es tajante — **no se usan para importes**.

Lo específico de RPG en esta clase es cómo trata el **redondeo**, que es lo que más sorprende al
llegar desde otro lenguaje. En RPG, `/` sobre decimales **redondea a la mitad hacia arriba** según los
decimales del destino, en lugar de truncar. `10 / 3` guardado en un `packed(5:2)` da `3.33`, y
guardado en un entero da **3**, pero `10 / 4` en un entero da **3**, no 2. Es aritmética de contable,
no de máquina.

Y cuando eso no basta, RPG tiene un operador propio: **`%dech`**, `%decp`, `%dec` con modo de
redondeo, y la palabra clave `half adjust` (`h` en formato fijo) que fuerza el redondeo comercial en
una operación concreta. Como el `ROUNDED` de COBOL: la política de redondeo es una decisión que se
escribe al lado de la operación, no un ajuste global.
"""),
        "pli": ("""
 reales: procedure options(main);

    declare (a, b)   fixed decimal(15,4);
    declare suma     fixed decimal(15,2);
    declare producto fixed decimal(15,2);
    declare (ps, pp) picture 'ZZZZZZZZZ9V.99';

    get list (a, b);

    suma     = a + b;
    producto = a * b;

    ps = suma;
    pp = producto;
    put skip list ('suma=' || trim(ps) || ' producto=' || trim(pp));

 end reales;
""", """
**Lo que esta clase enseña en PL/I.** PL/I es donde esta clase se ve con más claridad, porque el
lenguaje **te obliga a decir en qué base calculas**. `fixed decimal(15,4)` es decimal exacto;
`float binary(53)` es el `double` de siempre. La misma expresión da resultados distintos según cómo
declaraste los operandos, y eso está a la vista en la declaración.

El precio de esa potencia son las **reglas de precisión del resultado**, que son famosas por lo poco
intuitivas. Al multiplicar `fixed decimal(15,4)` por `fixed decimal(15,4)`, el estándar define
exactamente cuántos dígitos y decimales tiene el resultado intermedio, y ese cálculo puede exceder la
precisión máxima del compilador y **truncar en silencio**. La condición `FIXEDOVERFLOW` existe
precisamente para atrapar eso:

```pli
on fixedoverflow put skip list ('desbordamiento decimal');
```

Es el mismo mecanismo `ON` de la clase 041: se instala un manejador para la condición y queda activo.
Un programa PL/I bien escrito para banca instala `FIXEDOVERFLOW`, `ZERODIVIDE` y `SIZE` al principio y
no vuelve a preocuparse.
"""),
        "mumps": ("""
REALES ; Reales -- clase 045
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 set suma = a + b
 set producto = a * b
 write "suma=", $justify(suma, 0, 2)
 write " producto=", $justify(producto, 0, 2), !
 quit
""", """
**Lo que esta clase enseña en M.** M no tiene tipos, pero **sí tiene una decisión tomada sobre los
reales**, y es poco conocida: el estándar exige **al menos 15 dígitos decimales significativos** y la
aritmética de las implementaciones principales es **decimal**, no binaria. En YottaDB y en IRIS,
`0.1 + 0.2` da `0.3`.

No es casualidad: M nació en un hospital para manejar dosis, resultados de laboratorio y facturación
sanitaria. Un error de representación en una dosis no es un redondeo desafortunado.

`$justify(x, ancho, decimales)` es la función de formateo: con `ancho` 0 no rellena, y con el tercer
argumento **redondea** al número de decimales indicado. Con dos argumentos solo justifica a la
derecha. Es la misma función haciendo dos trabajos distintos según cuántos argumentos reciba, algo
muy propio de la economía de M.

Y una advertencia al leer código M antiguo: como todo es cadena, es habitual encontrar importes
guardados como texto con formato ya aplicado. Comparar `"10.50"` con `"10.5"` da falso como cadenas y
verdadero como números, y en M **el operador decide**: `=` compara como cadena, así que hay que
forzar el contexto numérico con `+` delante.
"""),
        "smalltalk": ("""
| partes a b |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

Transcript
    show: 'suma=', ((a + b) asFloat printShowingDecimalPlaces: 2);
    show: ' producto=', ((a * b) asFloat printShowingDecimalPlaces: 2);
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk tiene **tres respuestas** a esta clase, todas en
el mismo sistema de clases y todas con literal propio:

```smalltalk
0.1 + 0.2            "Float:         0.30000000000000004  — IEEE 754"
(1/10) + (2/10)      "Fraction:      3/10                 — exacto"
0.1s2 + 0.2s2        "ScaledDecimal: 0.30s2               — decimal exacto"
```

`ScaledDecimal` es el equivalente del `COMP-3` de COBOL: **decimal exacto, con el número de decimales
en el propio literal** (`s2` = dos decimales). Guarda internamente una fracción, así que las
operaciones intermedias no pierden precisión y solo se redondea al presentar.

Y `Fraction` aparece **sola**, sin pedirla: `1/3` en Smalltalk **no** es `0.333…`, es el objeto
`Fraction` con numerador 1 y denominador 3. `(1/3) * 3` da exactamente `1`. La división de dos
enteros que no dividen exactamente produce una fracción, no un real truncado ni un real aproximado —
una decisión que solo comparte con Lisp en esta página.

`printShowingDecimalPlaces:` es un mensaje al número. Como todo lo demás.
"""),
    },
)

# ---------------------------------------------------------------------------
# 046 — Booleanos y valores de verdad
# ---------------------------------------------------------------------------
SPECS["046"] = dict(
    gancho="""
Tres operaciones lógicas —y, o, no— sobre dos valores de verdad. Parece la clase más simple del
programa y es, de largo, la que más desacuerdo produce entre lenguajes: **la mitad de ellos ni
siquiera tiene un tipo booleano**, y los que lo tienen no se ponen de acuerdo en qué cuenta como
verdadero ni en si un booleano es o no un número.
""",
    porque="""
Aquí el concepto es **la verdad como tipo**, y estos lenguajes son el mejor muestrario que existe.
COBOL no tiene booleano y lo sustituye por **predicados con nombre** pegados al dato. PL/I usa
`bit(1)` y comparte los operadores con la manipulación de bits. M y Tcl no tienen tipo y aceptan
cualquier cosa. Y Smalltalk lleva la idea al extremo contrario: `true` y `false` son **objetos de dos
clases distintas**, y `ifTrue:` es un método implementado en cada una — el condicional resuelto por
polimorfismo, no por sintaxis.

Ver esas cinco posturas juntas es lo que convierte "usa booleanos" en una pregunta de diseño.
""",
    cierre="""
La pregunta que deja esta clase no es "¿tiene booleanos mi lenguaje?" sino **"¿qué considera
verdadero mi lenguaje, y qué pasa si le doy algo que no es un booleano?"**. Ada y Pascal responden
"no compila". C++ responde "lo convierto a número". Perl, Tcl y M responden con una lista de valores
falsos que hay que memorizar —y que **no coincide entre ellos**: `"0"` es falso en Perl y verdadero
en Python—. Esa lista es la primera que conviene aprender de cualquier lenguaje nuevo.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. BOOLEANOS.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA      PIC X(80).
01  TXT-A      PIC X(20).
01  TXT-B      PIC X(20).
01  A          PIC 9.
    88  A-CIERTO   VALUE 1.
01  B          PIC 9.
    88  B-CIERTO   VALUE 1.
01  R-AND      PIC X(5).
01  R-OR       PIC X(5).
01  R-NOT      PIC X(5).

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    IF A-CIERTO AND B-CIERTO
        MOVE "true"  TO R-AND
    ELSE
        MOVE "false" TO R-AND
    END-IF

    IF A-CIERTO OR B-CIERTO
        MOVE "true"  TO R-OR
    ELSE
        MOVE "false" TO R-OR
    END-IF

    IF NOT A-CIERTO
        MOVE "true"  TO R-NOT
    ELSE
        MOVE "false" TO R-NOT
    END-IF

    DISPLAY "and=" FUNCTION TRIM(R-AND)
            " or=" FUNCTION TRIM(R-OR)
            " not_a=" FUNCTION TRIM(R-NOT)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** Los **niveles 88** en acción. `A` es un dígito; `A-CIERTO` es
un **nombre de condición**: un predicado declarado junto al dato, que se usa sin comparar con nada.
`IF A-CIERTO` en lugar de `IF A = 1`.

La idea es mejor de lo que parece y no tiene equivalente directo en el núcleo. El nivel 88 **da
nombre a un conjunto de valores**, no a uno solo:

```cobol
01  CODIGO-PAIS  PIC X(2).
    88  UNION-EUROPEA  VALUE "ES" "FR" "DE" "IT" "PT" "NL".
    88  DESCONOCIDO    VALUE SPACES.

01  EDAD  PIC 9(3).
    88  MENOR-DE-EDAD  VALUE 0 THRU 17.
    88  JUBILADO       VALUE 65 THRU 999.
```

`IF UNION-EUROPEA` se lee como el negocio lo diría, la lista de países está **pegada al campo** en la
`DATA DIVISION` en lugar de dispersa por el código, y cambiarla es tocar una línea de declaración. En
un lenguaje moderno esto exige un enumerado, un conjunto y una función de pertenencia.

Además se puede asignar: `SET JUBILADO TO TRUE` pone en `EDAD` el primer valor de la lista. Es un
predicado que funciona en las dos direcciones.
"""),
        "fortran": ("""
program booleanos
   implicit none
   integer :: ia, ib
   logical :: a, b

   read(*, *) ia, ib
   a = (ia /= 0)
   b = (ib /= 0)

   write(*, '(A,A,A,A,A,A)') 'and=', trim(tf(a .and. b)), &
                             ' or=',  trim(tf(a .or. b)),  &
                             ' not_a=', trim(tf(.not. a))
contains

   function tf(v) result(s)
      logical, intent(in) :: v
      character(len=5) :: s
      s = merge('true ', 'false', v)
   end function tf

end program booleanos
""", """
**Lo que esta clase enseña en Fortran.** Fortran tiene `logical` como tipo intrínseco **desde 1957**,
antes que casi nadie, y con una decisión que hoy sigue siendo suya: **los operadores lógicos van
entre puntos**. `.and.`, `.or.`, `.not.`, `.eqv.` (equivalencia) y `.neqv.` (o exclusivo), y los
literales son `.true.` y `.false.`.

Los puntos no son estética: en el Fortran original **los espacios no eran significativos**, así que
`AND` como palabra suelta se habría confundido con una variable llamada `AND`. Los puntos delimitan
el operador sin ambigüedad. Es un rasgo de sintaxis que existe por una restricción del lector de
tarjetas de 1957 y que sigue ahí.

Fíjate también en `.eqv.` y `.neqv.`: pocos lenguajes tienen operadores lógicos de equivalencia y o
exclusivo. En C escribirías `!a == !b`, con la doble negación necesaria para normalizar.

Y `merge(a, b, cond)` es la joya escondida de esta clase: una función que devuelve `a` si la
condición es cierta y `b` si no. Sobre escalares es un ternario; **sobre arrays es elemento a
elemento**, y esa es su razón de ser: `merge(x, 0.0, x > 0.0)` pone a cero los negativos de un array
completo sin escribir un bucle ni un `if`. Es programación vectorizada aplicada a la lógica.

Y `a = (ia /= 0)` es explícito porque hace falta: en Fortran **un entero no se convierte a `logical`**.
`if (ia)` no compila.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Booleanos is

   function Tf (V : Boolean) return String is
     (if V then "true" else "false");

   Ia, Ib : Integer;
   A, B   : Boolean;
begin
   Get (Ia);
   Get (Ib);
   A := Ia /= 0;
   B := Ib /= 0;

   Put_Line ("and=" & Tf (A and B) &
             " or=" & Tf (A or B) &
             " not_a=" & Tf (not A));
end Booleanos;
""", """
**Lo que esta clase enseña en Ada.** Ada distingue **cuatro** operadores donde casi todos tienen dos,
y la distinción es deliberada:

| Operador | Evaluación |
|---|---|
| `and` | **Ambos operandos, siempre** |
| `or` | **Ambos operandos, siempre** |
| `and then` | Cortocircuito: si el primero es falso, no evalúa el segundo |
| `or else` | Cortocircuito: si el primero es cierto, no evalúa el segundo |

En C, en Java o en Python, `&&` **siempre** cortocircuita y no tienes elección. En Ada eliges, y
elegir importa por dos motivos opuestos. Si el segundo operando tiene un efecto lateral que debe
ocurrir, quieres `and`. Y si el segundo operando **solo es válido cuando el primero es cierto**,
necesitas `and then`:

```ada
if Indice <= Ultimo and then Tabla (Indice) = Buscado then   --  correcto
if Indice <= Ultimo and      Tabla (Indice) = Buscado then   --  Constraint_Error
```

La segunda línea evalúa el acceso a la tabla aunque el índice esté fuera de rango. En Ada eso no es
un valor basura: es una excepción. Que el lenguaje te obligue a escribir `and then` cuando dependes
del orden hace visible una dependencia que en C queda implícita en la elección de `&&` frente a `&`.

Y `A := Ia /= 0` es obligatorio: en Ada un `Integer` **no** se convierte a `Boolean`. Nunca.
"""),
        "pascal": ("""
program Booleanos;
{$MODE OBJFPC}{$H+}

function Tf(V: Boolean): string;
begin
  if V then Result := 'true' else Result := 'false';
end;

var
  Ia, Ib: Integer;
  A, B: Boolean;

begin
  Read(Ia, Ib);
  A := Ia <> 0;
  B := Ib <> 0;

  WriteLn('and=', Tf(A and B), ' or=', Tf(A or B), ' not_a=', Tf(not A));
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal usa **las mismas palabras** —`and`, `or`, `not`— para
la lógica booleana y para las operaciones bit a bit sobre enteros. `5 and 3` da `1` (bits) y
`True and False` da `False` (lógica). El operador se comporta según el tipo de los operandos, que es
posible precisamente porque el tipado es fuerte y el compilador sabe cuál es cuál.

Y aquí está la trampa más famosa del lenguaje, consecuencia de esa decisión: **la precedencia**. En
Pascal, `and` y `or` tienen precedencia **más alta que los operadores de comparación**, porque se
diseñaron pensando en los bits. Por eso esto **no compila**:

```pascal
if a > 0 and b > 0 then      { se lee como:  a > (0 and b) > 0 }
if (a > 0) and (b > 0) then  { correcto: los paréntesis son obligatorios }
```

En C, en Java y en Python la comparación va antes que el `&&`, y los paréntesis sobran. En Pascal son
obligatorios, y ese es el motivo de que el código Pascal esté lleno de paréntesis que parecen
redundantes y no lo son.

Sobre el cortocircuito, Free Pascal y Delphi lo controlan con directivas: `{$B-}` es evaluación
**perezosa** (la habitual, equivalente a `and then` de Ada) y `{$B+}` fuerza a evaluar los dos
operandos. El ISO no lo garantiza, así que en código portable no conviene depender de él.
"""),
        "lisp": ("""
(flet ((tf (v) (if v "true" "false")))
  (let* ((ia (read))
         (ib (read))
         (a (/= ia 0))
         (b (/= ib 0)))
    (format t "and=~A or=~A not_a=~A~%"
            (tf (and a b)) (tf (or a b)) (tf (not a)))))
""", """
**Lo que esta clase enseña en Common Lisp.** `and` y `or` **no son funciones: son macros**, y esa
diferencia es exactamente el tema del cortocircuito. Una función evalúa todos sus argumentos antes de
recibirlos; una macro recibe el código sin evaluar y decide qué hacer con él. Por eso `and` puede
parar en cuanto encuentra un `nil`: no le llegaron valores, le llegaron expresiones.

Y devuelven algo más útil que un booleano: **`and` devuelve el último valor si todos son verdaderos,
y `or` devuelve el primero verdadero**.

```lisp
(and 1 2 3)          ; => 3
(and 1 nil 3)        ; => nil
(or nil nil "hola")  ; => "hola"
(or (buscar-cache) (buscar-disco) "por-defecto")
```

Esa última línea es el idioma clásico: una cadena de alternativas donde gana la primera que dé algo.
JavaScript, Python y Ruby copiaron después este comportamiento —`a || b` devuelve un valor, no un
booleano— y viene de aquí.

`flet` define funciones **locales** al bloque, la contrapartida de `let` para funciones. Su pariente
`labels` permite además que la función se llame a sí misma, y existen las dos por la misma razón que
existen `let` y `let*`: Lisp prefiere que el ámbito se declare en vez de suponerse.
"""),
        "tcl": ("""
proc tf {v} { return [expr {$v ? "true" : "false"}] }

gets stdin linea
lassign [split [string trim $linea]] ia ib

set a [expr {$ia != 0}]
set b [expr {$ib != 0}]

puts "and=[tf [expr {$a && $b}]] or=[tf [expr {$a || $b}]] not_a=[tf [expr {!$a}]]"
""", """
**Lo que esta clase enseña en Tcl.** Tcl acepta como verdaderos `1`, `true`, `yes`, `on` y cualquier
número distinto de cero; como falsos, `0`, `false`, `no`, `off` y la cadena vacía. Cualquier otra
cadena —`"quizá"`— **provoca un error**, no un valor por defecto. Es más estricto que Perl, que
simplemente la consideraría verdadera.

Pero **devuelve `1` o `0`**, nunca `true` o `false`. Por eso este programa necesita `tf`: la salida
de `expr` es un número, aunque acepte palabras a la entrada.

Los operadores lógicos solo existen **dentro de `expr`**, que es su propio mini-lenguaje con
precedencia estilo C. Fuera de `expr` no hay `&&` ni `||` porque no hay operadores en Tcl, solo
comandos. Y `if` es un comando que recibe la condición como una cadena y la pasa a `expr`, lo que
explica una regla que confunde a todo el mundo:

```tcl
if {$a && $b} { ... }     ;# correcto: llaves, se evalúa una vez y compilado
if "$a && $b" { ... }     ;# funciona, es más lento y permite inyección
```

Las llaves impiden la sustitución previa de variables. Es la misma regla de `expr` de la clase 041, y
por el mismo motivo.
"""),
        "perl": ("""
use strict;
use warnings;

sub tf { return $_[0] ? 'true' : 'false' }

my $linea = <STDIN>;
chomp $linea;
my ($ia, $ib) = split ' ', $linea;

my $a = ($ia != 0);
my $b = ($ib != 0);

printf "and=%s or=%s not_a=%s\\n", tf($a && $b), tf($a || $b), tf(!$a);
""", """
**Lo que esta clase enseña en Perl.** La lista de valores falsos de Perl es **exactamente cinco**, y
conviene memorizarla porque no coincide con la de ningún otro lenguaje: `0`, `"0"`, `""`, `undef` y
la lista vacía. Todo lo demás es verdadero — incluidas `"0.0"`, `"00"` y `" "`, que sorprenden
siempre.

Y Perl tiene **dos juegos de operadores lógicos** que hacen lo mismo con distinta precedencia:

```perl
my $x = $a || 'por defecto';    # || tiene precedencia ALTA
my $x = $a or 'por defecto';    # or tiene precedencia BAJÍSIMA — ¡asigna $a!

open(my $fh, '<', $f) or die "no puedo abrir: $!";   # el idioma correcto
```

`or` y `and` están pensados para **control de flujo al final de una sentencia**, con precedencia
menor que la asignación, y `||` y `&&` para expresiones. Usar el equivocado es un error clásico que
`use warnings` no siempre atrapa.

Perl añadió después `//`, el operador de **coalescencia de nulos**: devuelve el lado derecho solo si
el izquierdo es `undef`, no si es falso. Es la diferencia entre "no tiene valor" y "vale cero", y
`$contador // 10` hace lo correcto donde `$contador || 10` fallaría con un contador a cero.
JavaScript adoptó `??` con la misma semántica veinte años después.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    int ia{}, ib{};
    if (!(std::cin >> ia >> ib)) return 1;

    const bool a = ia != 0;
    const bool b = ib != 0;

    std::cout << std::boolalpha
              << "and=" << (a && b)
              << " or=" << (a || b)
              << " not_a=" << (!a) << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ tiene `bool` como tipo propio desde el principio —C tuvo
que esperar a C99 y su `_Bool`— pero **conserva la conversión implícita a y desde entero**, y ahí
está toda la enseñanza de esta clase.

La distinción que hay que tener clara es entre los operadores **lógicos** y los **de bits**:

| | Lógico | Bits |
|---|---|---|
| Y | `&&` — cortocircuita | `&` — no cortocircuita |
| O | `\\|\\|` — cortocircuita | `\\|` — no cortocircuita |
| No | `!` | `~` |

Escribir `&` donde iba `&&` compila sin avisar y casi siempre da el mismo resultado con booleanos,
así que el error sobrevive a las pruebas… hasta que el segundo operando tiene un efecto lateral o
desreferencia un puntero que no debía evaluarse. Es un error real y difícil de ver en revisión.

C++11 añadió `explicit operator bool()` para que una clase pueda usarse en un `if` **sin** convertirse
accidentalmente a entero. Es lo que hace `std::cin` y lo que permite escribir
`if (!(std::cin >> a))` como en este programa: el flujo se convierte a booleano solo donde se espera
un booleano, no en una suma.

Y `std::boolalpha` imprime `true`/`false`; sin él saldrían `1` y `0`.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi BOOLEANOS;
  ia int(10) const;
  ib int(10) const;
end-pi;

dcl-s a      ind;
dcl-s b      ind;
dcl-s salida char(60);

a = (ia <> 0);
b = (ib <> 0);

salida = 'and=' + tf(a and b)
       + ' or=' + tf(a or b)
       + ' not_a=' + tf(not a);
dsply salida;

*inlr = *on;
return;

dcl-proc tf;
  dcl-pi *n varchar(5);
    v ind const;
  end-pi;
  if v = *on;
    return 'true';
  endif;
  return 'false';
end-proc;
""", """
**Lo que esta clase enseña en RPG.** El tipo booleano de RPG se llama **`ind`** (*indicator*) y sus
valores son **`*on` y `*off`**, no `true` y `false`. Ese vocabulario no es un capricho: viene
directamente de los **indicadores del ciclo del programa**, las variables globales numeradas
`*IN01`…`*IN99` que en el RPG clásico controlaban absolutamente todo.

En aquel modelo, un indicador se encendía al leer el último registro, otro al cambiar un nivel de
control, otro al fallar una comparación. El código estaba lleno de `IF *IN37` sin ninguna pista de
qué significaba el 37. La deuda técnica característica de RPG es un programa de tres mil líneas donde
los indicadores son la única lógica y nadie recuerda su significado.

`dcl-s a ind` es la respuesta moderna: **un booleano con nombre**, con tipo, local a su procedimiento.
Es exactamente el mismo movimiento que hizo COBOL con los niveles 88 —dar nombre a la condición— pero
llegando desde el otro extremo.

Los operadores son palabras: `and`, `or`, `not`, y las comparaciones `=`, `<>`, `>=`. RPG **no**
convierte números a indicadores: `a = ia` no compila, hay que escribir la comparación.
"""),
        "pli": ("""
 booleanos: procedure options(main);

    declare (ia, ib) fixed binary(31);
    declare (a, b)   bit(1);

    get list (ia, ib);
    a = (ia ^= 0);
    b = (ib ^= 0);

    put skip list ('and='   || tf(a & b)  ||
                   ' or='   || tf(a | b)  ||
                   ' not_a='|| tf(^a));

 tf: procedure (v) returns (character(5) varying);
    declare v bit(1);
    if v then return ('true');
    return ('false');
 end tf;

 end booleanos;
""", """
**Lo que esta clase enseña en PL/I.** El booleano de PL/I es **`bit(1)`**: una cadena de bits de
longitud uno. No hay tipo `boolean`; hay cadenas de bits de longitud arbitraria, y la de longitud 1
hace de valor de verdad. Los literales son `'1'b` y `'0'b`.

La consecuencia es que **los operadores lógicos y los de bits son los mismos**: `&`, `|` y `^` (o `¬`
en teclados que lo tengan) operan bit a bit sobre cadenas de cualquier longitud, y sobre `bit(1)`
resultan ser la lógica booleana. `'1100'b & '1010'b` da `'1000'b`.

Es elegante y unifica dos conceptos que casi todos los lenguajes separan. También significa que **no
hay cortocircuito**: `&` es una operación sobre datos, no una estructura de control, así que evalúa
siempre los dos lados. Para el cortocircuito hay que escribir `if` anidados. C —diseñado poco
después, con la misma idea de la verdad como número— sí separó `&` de `&&` precisamente por esto.

Y ojo con la conversión: PL/I convierte casi cualquier cosa a `bit`, incluidos los caracteres y los
números. Es cómodo y es la razón de que sus errores se manifiesten tarde, como se vio en la clase 041.
"""),
        "mumps": ("""
BOOL ; Booleanos -- clase 046
 read linea
 set ia = $piece(linea, " ", 1)
 set ib = $piece(linea, " ", 2)
 set a = ''ia
 set b = ''ib
 write "and=", $$tf(a & b)
 write " or=", $$tf(a ! b)
 write " not_a=", $$tf('a), !
 quit
 ;
tf(v) ; booleano a texto
 quit $select(v : "true", 1 : "false")
""", """
**Lo que esta clase enseña en M.** M no tiene tipo booleano, y su regla de verdad es **la más simple
de toda la página y la más peligrosa**: un valor es verdadero si su **interpretación numérica** es
distinta de cero.

Como M convierte texto a número leyendo el prefijo y descartando el resto, eso significa que
`"0abc"` es **falso** —su valor numérico es 0— y `"1abc"` es **verdadero**. La cadena `"hola"` vale 0
y por tanto es falsa. Es tipado débil llevado al límite.

Los operadores son símbolos de un carácter, y esta es la lista que hay que conocer:

| Operador | Significado |
|---|---|
| `&` | Y lógico |
| `!` | **O lógico** — no "no", como en C |
| `'` | **No** — el apóstrofo |
| `'=` | Distinto (el `'` niega el operador siguiente) |

Que `!` sea el **or** y no la negación es la confusión número uno para quien llega de C. Y `'` como
negación se puede pegar delante de cualquier operador de comparación: `'=`, `'<`, `'>`.

`set a = ''ia` no es un error tipográfico: es la **doble negación**, el idioma de M para normalizar
cualquier valor a exactamente `1` o `0`. El mismo truco que `!!x` en C y JavaScript.
"""),
        "smalltalk": ("""
| partes ia ib a b tf |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
ia := partes first.
ib := partes second.

a := ia ~= 0.
b := ib ~= 0.

tf := [ :v | v ifTrue: [ 'true' ] ifFalse: [ 'false' ] ].

Transcript
    show: 'and=', (tf value: (a and: [ b ]));
    show: ' or=', (tf value: (a or: [ b ]));
    show: ' not_a=', (tf value: a not);
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Esta es **la** clase de Smalltalk. `true` y `false` no son
literales de un tipo primitivo: son las **únicas instancias** de las clases `True` y `False`, ambas
subclases de `Boolean`. Y los operadores lógicos son **métodos implementados en cada una de las dos
clases**. El código real, que puedes abrir en el navegador de clases, es esencialmente este:

```smalltalk
True >> ifTrue: bloqueV ifFalse: bloqueF     ^ bloqueV value
False >> ifTrue: bloqueV ifFalse: bloqueF    ^ bloqueF value

True >> not     ^ false
False >> not    ^ true

True >> and: unBloque     ^ unBloque value
False >> and: unBloque    ^ false
```

**No hay ninguna estructura de control.** El condicional es despacho de mensajes: se envía
`ifTrue:ifFalse:` al objeto, y el objeto —según sea `true` o `false`— evalúa un bloque u otro. Es la
demostración más limpia que existe de que "todo es un objeto" no era un eslogan.

Y ahí está la razón de los corchetes en `a and: [ b ]`: **`and:` recibe un bloque, no un valor**. Si
recibiera un valor, `b` ya se habría evaluado y no habría cortocircuito. Al recibir un bloque, `False`
simplemente no lo evalúa. **El cortocircuito no es una regla del lenguaje: es una consecuencia de
pasar código en vez de datos.** Existen además `&` y `|`, que sí evalúan los dos lados porque reciben
valores — la misma distinción que `&&` y `&` en C++, obtenida sin sintaxis especial.
"""),
    },
)
