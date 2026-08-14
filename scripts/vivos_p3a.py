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
