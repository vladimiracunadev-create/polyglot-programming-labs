# -*- coding: utf-8 -*-
"""Parte 3, lote C — clases 052 a 056. Ver `vivos_parte3.py` y `gen_vivos.py`.

El código de los ocho lenguajes de la sección 🟢 se ejecuta en CI contra el
`casos.json` de la clase (`scripts/verificar_vivos.py`).
"""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 052 — Inferencia de tipos
# ---------------------------------------------------------------------------
SPECS["052"] = dict(
    gancho="""
Multiplicar dos enteros. El programa más corto de la Parte 3, elegido a propósito: lo único que hay
que mirar aquí es **cuánto hay que escribir antes de poder multiplicar**. Y la respuesta separa a
estos doce lenguajes en tres grupos — los que exigen declararlo todo, los que no exigen nada, y los
que deducen el tipo sin que lo digas.
""",
    porque="""
Aquí el concepto es **la inferencia de tipos**, y estos lenguajes son valiosos porque muestran el
mundo **anterior** a ella y por qué se inventó. COBOL, Fortran, Ada y Pascal obligan a declarar cada
variable con su tipo completo: la inferencia moderna existe como reacción a esa verbosidad.

Pero hay dos sorpresas. La primera: **Fortran tuvo inferencia en 1957 y la comunidad se pasó
cuarenta años apagándola**, porque adivinar el tipo por la inicial del nombre resultó ser inferencia
hecha mal. La segunda: **SBCL infiere tipos en Common Lisp**, un lenguaje dinámico, y avisa en
compilación de incompatibilidades que puede demostrar. Inferir y declarar no son opuestos.
""",
    cierre="""
La lección es que **inferencia no significa "sin tipos"**. En C++ y en Rust el tipo existe, es
estricto y lo deduce el compilador; en Fortran del 57 el tipo se adivinaba por una regla tipográfica,
que es otra cosa muy distinta; y en Tcl o M no hay nada que inferir. Cuando alguien dice "mi lenguaje
tiene inferencia", la pregunta útil es **qué pasa cuando la deducción sale mal** — si es un error de
compilación o un valor basura.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. INFERENCIA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA     PIC X(80).
01  TXT-A     PIC X(20).
01  TXT-B     PIC X(20).
01  A         PIC S9(9)  COMP-3.
01  B         PIC S9(9)  COMP-3.
01  PRODUCTO  PIC S9(18) COMP-3.
01  ED-P      PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    COMPUTE PRODUCTO = A * B

    MOVE PRODUCTO TO ED-P
    DISPLAY "producto=" FUNCTION TRIM(ED-P)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** **Inferencia cero.** Cada dato lleva su `PIC` completo, y el
programa dedica más líneas a describir la forma de los datos que a calcular. Es la verbosidad contra
la que reaccionó todo lo que vino después.

Pero COBOL resolvió el problema real que hay detrás —**repetir la misma declaración en veinte
programas**— con un mecanismo que se adelantó a su tiempo: el **copybook**.

```cobol
*> En un miembro llamado CLIENTE:
01  REG-CLIENTE.
    05  CLI-CODIGO   PIC 9(8).
    05  CLI-NOMBRE   PIC X(40).
    05  CLI-SALDO    PIC S9(11)V99 COMP-3.

*> En cualquier programa que lo necesite:
COPY CLIENTE.
```

`COPY` inserta el texto en tiempo de compilación, y con `REPLACING` permite renombrar los campos al
insertarlos. Todos los programas que tocan el fichero de clientes comparten **una sola definición**,
y cambiar un campo es cambiar un fichero. Es el antepasado directo de los ficheros de cabecera, de
los esquemas compartidos y de los tipos generados a partir de un contrato — el mismo problema, con
una solución de 1968.

Y fíjate en `PIC S9(18)` para el producto: al no haber inferencia, **el programador tiene que
calcular a mano cuántos dígitos puede necesitar el resultado**. Si se queda corto, la clase 049 ya
avisó de lo que pasa.
"""),
        "fortran": ("""
program inferencia
   implicit none
   integer :: a, b

   read(*, *) a, b

   write(*, '(A,I0)') 'producto=', a * b
end program inferencia
""", """
**Lo que esta clase enseña en Fortran.** La historia más instructiva de toda la página: **Fortran
tuvo inferencia de tipos desde 1957, y su comunidad se pasó cuarenta años desactivándola**.

La regla era tipográfica: una variable no declarada cuyo nombre empieza por `I`, `J`, `K`, `L`, `M`
o `N` es un **entero**; cualquier otra inicial, un **real**. De ahí el chiste clásico —*God is real,
unless declared integer*— y de ahí también que los bucles de todo el código Fortran del mundo usen
`i`, `j`, `k`: no era estilo, era la única forma de que el contador fuera entero sin declararlo.

Y de ahí, sobre todo, el defecto característico:

```fortran
program mal
   velocidad = 100.0
   velocidda = velocidad * 2.0   ! erratas: crea una variable NUEVA
   print *, velocidad            ! imprime 100.0, y nadie sabe por qué
end program
```

Sin declaraciones, una errata **no es un error**: es una variable nueva. Se dice que un error de este
tipo contribuyó a la pérdida de la sonda Mariner 1 en 1962 —la anécdota exacta se cuenta de varias
maneras y conviene tomarla con cuidado— pero el mecanismo es real y costó incontables horas de
depuración.

`implicit none` apaga la regla y convierte cada errata en un error de compilación. Es la lección de
esta clase: **inferir el tipo a partir del nombre no es inferencia, es adivinación**. La inferencia de
verdad, la de C++ o Rust, deduce del **valor**, y por eso una errata sigue siendo un error.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Inferencia is
   A, B : Integer;
begin
   Get (A);
   Get (B);

   Put ("producto=");
   Put (A * B, Width => 1);
   New_Line;
end Inferencia;
""", """
**Lo que esta clase enseña en Ada.** Ada **no tiene inferencia general** y es deliberado: si el tipo
es la herramienta principal para expresar la intención, escribirlo no es ruido, es documentación
comprobada.

Pero sí tiene inferencia en tres sitios muy concretos, y elegirlos dice mucho:

```ada
--  1) Números con nombre: sin tipo, valor exacto (ya vistos en la clase 041)
Maximo : constant := 1_000_000;

--  2) La variable de un bucle for: su tipo se DEDUCE del rango
for I in 1 .. 10 loop ... end loop;              --  I es Integer, y es constante
for Dia in Lunes .. Viernes loop ... end loop;   --  Dia es del tipo enumerado

--  3) Agregados y literales, que toman el tipo del contexto
V : Vector := (others => 0.0);
```

Los tres tienen algo en común: **el tipo se deduce de algo que ya está escrito al lado**. No hay que
buscarlo lejos.

Y el caso del bucle merece subrayarse porque resuelve un error clásico: en Ada, la variable de un
`for` **es una constante local al bucle**. No se puede modificar dentro, no existe fuera, y no hace
falta declararla. En C se declara, se puede modificar dentro del cuerpo y sobrevive si la declaraste
fuera — tres oportunidades de error que Ada simplemente elimina.
"""),
        "pascal": ("""
program Inferencia;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  A, B: Integer;

begin
  Read(A, B);

  WriteLn('producto=', IntToStr(A * B));
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal exige declararlo todo en la sección `var`, con la
misma lógica de una sola pasada que ya apareció en la clase 042. Pero tiene un caso de inferencia
desde el principio, y es el mismo que Ada: **las constantes sin tipo**.

```pascal
const
  MAXIMO = 1000;        { el compilador deduce el tipo en cada uso }
  PI     = 3.14159;
  SALUDO = 'hola';
```

Una constante sin tipo se adapta al contexto: `MAXIMO` puede usarse donde se espera un `Byte`, un
`Integer` o un `Int64`, y solo se comprueba el rango en el punto de uso. Es exactamente el concepto
del **número con nombre** de Ada, y también el de las constantes sin tipo de Go.

Y la rama moderna sí llegó: **Delphi 10.3, en 2019**, añadió la declaración de variables en línea con
inferencia, y Free Pascal tiene su equivalente:

```pascal
var Total := A * B;            { Delphi 10.3+: el tipo se deduce }
for var I := 1 to 10 do ...    { y también en el bucle }
```

Sesenta años después de ALGOL W, el lenguaje que definió "declara todo arriba" adoptó lo contrario.
Es una buena muestra de que estas decisiones no son permanentes: la restricción de la pasada única
dejó de importar cuando los compiladores dejaron de estar limitados por la memoria.
"""),
        "lisp": ("""
(let* ((a (read))
       (b (read)))
  (format t "producto=~D~%" (* a b)))
""", """
**Lo que esta clase enseña en Common Lisp.** La sorpresa de esta clase: **SBCL infiere tipos, y
avisa en tiempo de compilación**, en un lenguaje que todo el mundo clasifica como dinámico.

```lisp
(defun mal (x)
  (declare (type integer x))
  (concatenate 'string x "hola"))

; SBCL al compilar:
;   caught WARNING: Derived type of X is (INTEGER), conflicting with its asserted type SEQUENCE.
```

SBCL propaga los tipos por el flujo de datos, deduce el tipo de cada expresión y **señala las
contradicciones que puede demostrar**, sin ejecutar nada. Es la misma técnica que usan los
compiladores estáticos, aplicada a un lenguaje sin declaraciones obligatorias.

Y el sistema de tipos que infiere es más expresivo que el de la mayoría de los estáticos, porque
incluye **rangos y uniones**:

```lisp
(declare (type (integer 0 100) porcentaje))     ; un entero ENTRE 0 y 100
(declare (type (or null string) nombre))        ; nulable, explícito
(declare (type (simple-array double-float (*)) datos))
```

`(integer 0 100)` es exactamente el subrango de Ada y Pascal, aquí como tipo de primera clase. Con
`(safety 0)` SBCL confía y genera código sin comprobaciones; con `(safety 3)` las comprueba todas en
ejecución. **El mismo código, con o sin red, según una declaración.** Eso es tipado gradual, y estaba
en el estándar de 1994.
"""),
        "tcl": ("""
gets stdin linea
lassign [split [string trim $linea]] a b

puts "producto=[expr {$a * $b}]"
""", """
**Lo que esta clase enseña en Tcl.** No hay nada que inferir: no hay declaraciones y no hay tipos.
`lassign` crea `a` y `b` en el acto, y `expr` decide qué son en el momento de multiplicar.

Lo interesante es que **el compilador de bytecode de Tcl sí infiere**, aunque el lenguaje no lo
exponga. Cuando `expr` recibe una expresión entre llaves —y por eso siempre se escribe entre
llaves—, Tcl la compila **una sola vez** a bytecode y, si detecta que los operandos han sido enteros
en las últimas vueltas, genera una ruta rápida que opera directamente sobre la representación
numérica en caché, sin volver a analizar el texto.

Si en alguna iteración el valor deja de ser un entero, la ruta rápida se abandona y se vuelve a la
genérica. Ese patrón —especular sobre el tipo, comprobarlo barato y desespecializar si falla— es
**exactamente** lo que hacen hoy V8, JavaScriptCore y PyPy con sus clases ocultas y su compilación
por trazas. Tcl lo hacía en 1997.

La lección: en los lenguajes dinámicos rápidos, la inferencia no desapareció, **se movió del
programador al motor y del compilado al tiempo de ejecución**.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($x, $y) = split ' ', $linea;

printf "producto=%d\\n", $x * $y;
""", """
**Lo que esta clase enseña en Perl.** `my` declara la **existencia** y el **ámbito** de una variable,
pero no su tipo — porque no hay tipo que declarar. Lo único que el sigilo indica es la **forma del
acceso**: escalar, lista o hash.

Y aquí hay una distinción que esta clase deja clara y que se confunde a menudo: `use strict` **no
añade tipos**. Lo que hace es obligar a **declarar el nombre**, que es un problema distinto —el de
la errata de Fortran— y se resuelve por separado del tipado.

Perl moderno ha ido añadiendo declaración donde importa. Las **firmas de subrutina**, estables desde
5.36, declaran cuántos parámetros hay y con qué nombre, aunque no de qué tipo:

```perl
use v5.36;

sub producto ($a_val, $b_val) {    # firma: nombre y aridad declarados
    return $a_val * $b_val;
}
```

Antes de eso, los argumentos llegaban en el array `@_` y una llamada con el número equivocado de
argumentos **no daba error**. La firma convierte eso en un fallo en tiempo de compilación. Es la
misma dirección que ha tomado Python con las anotaciones y Ruby con RBS: **añadir declaración
opcional a un lenguaje dinámico, empezando por lo que más errores causa**.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    const auto producto = a * b;      // auto: el tipo lo deduce el compilador

    std::cout << "producto=" << producto << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** `auto` es la inferencia de verdad: el tipo **existe**, es
`int`, es estricto, y lo deduce el compilador a partir del valor. No se pierde ninguna comprobación
— es exactamente lo mismo que escribir `int`, con menos teclas.

Y hay tres motivos por los que se usa que van más allá de la comodidad:

```cpp
auto it = mapa.begin();     // en vez de std::map<std::string, std::vector<int>>::iterator
auto lambda = [](int x) { return x * 2; };   // el tipo de una lambda NO SE PUEDE escribir
for (const auto& [clave, valor] : mapa) { }  // C++17: descomposición estructurada
```

El segundo es el decisivo: **el tipo de una lambda es único, generado por el compilador y sin
nombre**. Sin `auto` no habría forma de declarar la variable. Cuando un lenguaje introduce valores
cuyo tipo no se puede escribir, la inferencia deja de ser azúcar y pasa a ser necesaria.

C++ tiene además `decltype` —"el tipo de esta expresión, sin evaluarla"— y, desde C++17, la
**deducción de argumentos de plantilla en el constructor**: `std::pair p{1, "a"};` en lugar de
`std::pair<int, const char*>`.

Y el aviso habitual: `auto` **descarta las referencias y los `const`** salvo que los pidas.
`auto x = vec[0];` copia; `auto& x = vec[0];` no. Esa distinción de un carácter es la causa de
copias silenciosas en bucles sobre contenedores grandes.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi INFEREN;
  a int(10) const;
  b int(10) const;
end-pi;

dcl-s producto like(a);       // LIKE: hereda el tipo de otra variable
dcl-s salida   char(40);

producto = a * b;

salida = 'producto=' + %char(producto);
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** `like(a)` es la inferencia de RPG, y resuelve un problema muy
concreto del mundo empresarial: **que el tipo de una variable siga al del campo de la base de datos
sin repetirlo**.

```rpgle
dcl-s importe   like(FACTURA.TOTAL);   // el tipo del campo, sea cual sea
dcl-s copia     likeds(cabecera);      // la misma estructura de datos
dcl-s texto     like(nombre) inz('');
```

Si mañana el campo `TOTAL` pasa de `packed(11:2)` a `packed(13:2)`, **todos los programas que usan
`like` se ajustan al recompilar**. Sin él habría que buscar y cambiar cada declaración, con el riesgo
de olvidar una y truncar importes en silencio —el fallo de la clase 049—.

Es inferencia con un propósito distinto de la de C++: no ahorra teclas, **elimina una duplicación
que se desincroniza**. El mismo motivo por el que en TypeScript se escribe `typeof config` o en Rust
se derivan tipos de un esquema.

RPG añadió después **`likefile`** para prototipos de ficheros y las **plantillas** (`template`), que
permiten declarar un tipo que solo existe para ser copiado con `like` y que nunca ocupa memoria. Es
el equivalente de un `typedef` en un lenguaje que no tenía ninguno.
"""),
        "pli": ("""
 inferencia: procedure options(main);

    declare (a, b)   fixed binary(31);
    declare producto fixed binary(31);

    get list (a, b);
    producto = a * b;

    put skip list ('producto=' || trim(char(producto)));

 end inferencia;
""", """
**Lo que esta clase enseña en PL/I.** PL/I tenía **declaración implícita**, como Fortran: una
variable sin declarar recibía atributos según su inicial —`I` a `N` binaria fija, el resto flotante
decimal—. Con los mismos problemas y por los mismos motivos.

Pero PL/I hizo algo que ningún otro lenguaje de esta página: dejó que **el programador redefiniera
las reglas de inferencia**, con la sentencia `DEFAULT`:

```pli
default range(*) fixed binary(31);        /* todo lo no declarado es entero */
default range(a:h) character(20) varying; /* salvo a..h, que son texto */
default (constant) value(fixed binary(31));
```

Es decir: la convención de nombres deja de ser una regla del lenguaje y pasa a ser **configuración
del programa**. Visto hoy suena a mala idea —dos ficheros del mismo sistema podrían tener reglas
distintas— y probablemente lo era. Pero es un ejemplo notable de la filosofía de PL/I: si hay una
regla, que sea parametrizable.

La práctica moderna en PL/I es la contraria, y se parece a `implicit none`:

```pli
default range(*) ;    /* sin atributos: obliga a declararlo TODO */
```

Otra vez el mismo arco que en Fortran — el lenguaje ofrece la adivinación y la comunidad acaba
apagándola.
"""),
        "mumps": ("""
INFER ; Inferencia -- clase 052
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 write "producto=", a * b, !
 quit
""", """
**Lo que esta clase enseña en M.** No hay tipos, no hay declaraciones y no hay inferencia: **hay
`set`**. Una variable existe desde que se le asigna y su contenido es siempre una cadena.

Lo que sí tiene M, y conviene no confundir con una declaración, es **`new`**:

```mumps
rutina ;
 new a, b, temporal      ; NO declara: guarda el valor anterior y lo restaura al salir
 set a = 1
 quit                    ; aquí a, b y temporal recuperan lo que valieran antes
```

`new` no crea variables locales en el sentido léxico de casi todos los lenguajes: **intercepta las
globales durante la llamada**. Es ámbito **dinámico**, el mismo mecanismo que `local` en Perl y que
las variables especiales de Common Lisp. Si una rutina llamada desde aquí lee `a`, ve la de este
ámbito, no la del llamante — cosa que con ámbito léxico sería imposible.

Ese modelo es más frágil y más flexible a la vez, y explica un idioma muy visto en código M
heredado: rutinas que se comunican por variables acordadas en vez de por parámetros. Funciona, es
rapidísimo, y hace que entender un programa exija leer toda la cadena de llamadas.
"""),
        "smalltalk": ("""
| partes a b |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

Transcript show: 'producto=', (a * b) printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Las temporales se declaran entre barras y **nunca llevan
tipo**, porque el tipo pertenece al objeto. `a` puede referirse hoy a un entero y mañana a una
ventana; lo único que decide qué se le puede hacer es **a qué mensajes responde**.

Y aquí está la aportación de Smalltalk a esta clase, que no es sobre el lenguaje sino sobre las
**herramientas**: como no hay tipos escritos, el entorno los **descubre en ejecución**. El navegador
de Pharo puede responder a preguntas que un compilador estático respondería en compilación:

- *¿quién envía este mensaje?* — buscando en todos los métodos de la imagen;
- *¿qué clases lo implementan?* — el conjunto real de receptores posibles;
- *¿qué valores ha tomado esta variable?* — instrumentando y observando.

Es **inferencia por observación** en lugar de por deducción. Y llevada al extremo produce algo que
ningún lenguaje estático puede: el depurador de Smalltalk, ante un método que no existe, te ofrece
crearlo **en el momento**, con los argumentos reales delante y la pila viva, y continuar.

La contrapartida es honesta y hay que decirla: sin tipos declarados, **el compilador no puede
demostrar nada antes de ejecutar**. Un error de tipo aparece cuando se recorre esa rama, no antes.
Por eso los proyectos Smalltalk grandes se apoyan tanto en pruebas — no es casualidad que SUnit,
el antepasado de JUnit, naciera aquí.
"""),
    },
)

# ---------------------------------------------------------------------------
# 053 — Nulabilidad: null, nil, None, Option y valores ausentes
# ---------------------------------------------------------------------------
SPECS["053"] = dict(
    gancho="""
Distinguir "el valor es cero" de "no hay valor". Tony Hoare llamó a la referencia nula *su error de
mil millones de dólares*, y esta clase es donde se ve por qué: en la mitad de estos lenguajes **la
ausencia no se puede representar**, así que se finge con un valor especial —un cero, un espacio, una
fecha imposible— y tarde o temprano alguien lo confunde con un dato real.
""",
    porque="""
Aquí el concepto es **cómo se representa lo que no está**, y estos lenguajes lo cubren mejor que el
núcleo porque incluyen las dos épocas. COBOL, Fortran clásico y RPG **no tienen null**: usan valores
centinela, y de ahí vienen las fechas `9999-12-31` y los códigos `-1` que siguen apareciendo en
bases de datos de todo el mundo.

Y luego está M, que tiene la respuesta más sofisticada de toda la página y la más desconocida:
**`$data` devuelve cuatro valores distintos**, porque en M una variable puede no existir, existir con
valor, existir solo con descendientes, o las dos cosas. Es un modelo de ausencia con más matices que
el `Option` de Rust.
""",
    cierre="""
Dos lecciones. La primera: **un valor centinela es una bomba de relojería**. `0` significa ausente
hasta el día en que cero es un dato legítimo; `-1` funciona hasta que llega un saldo negativo. Si el
lenguaje no distingue, la distinción hay que llevarla aparte —una bandera, un indicador, un
`has_value`—, y eso es exactamente lo que hacen `std::optional`, el `not null access` de Ada y los
indicadores de nulo de RPG.

La segunda: **`nil` no es una cosa, son varias**. En Lisp es a la vez falso, lista vacía y ausencia;
en Smalltalk es un objeto con métodos; en Perl `undef` se distingue de `0` con `//` pero no con `||`.
Saber cuál de esas es la de tu lenguaje evita la clase de error que Hoare lamentaba.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. NULABLE.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9) COMP-3.
    88  AUSENTE   VALUE 0.
01  ED-N    PIC -(9)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N

    IF AUSENTE
        DISPLAY "valor=ausente"
    ELSE
        MOVE N TO ED-N
        DISPLAY "valor=" FUNCTION TRIM(ED-N)
    END-IF
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** **COBOL no tiene null.** Un `PIC S9(9)` siempre contiene un
número; no hay ningún estado que signifique "vacío". La ausencia se representa con un **valor
centinela**, y el nivel 88 sirve al menos para **darle nombre**: `AUSENTE` documenta que el cero
tiene un significado especial, en lugar de dejar un `IF N = 0` sin explicación.

Esa es la respuesta pragmática, y es el origen de convenciones que siguen vivas en bases de datos de
medio mundo:

- fechas `00000000` o `99991231` para "sin fecha" y "sin caducidad";
- códigos `-1` o `999` para "desconocido";
- campos alfanuméricos a `SPACES` para "no informado";
- `HIGH-VALUES` y `LOW-VALUES` como centinelas de ordenación.

Todas funcionan hasta que el valor centinela se convierte en un dato legítimo, y entonces el fallo es
silencioso y muy caro de encontrar.

Donde COBOL **sí** tiene nulos de verdad es al hablar con **Db2**, porque SQL sí los tiene. Y la
solución es exactamente la de RPG y la de `std::optional`: **llevar la ausencia en una variable
aparte**.

```cobol
EXEC SQL
    SELECT SALDO INTO :WS-SALDO :WS-SALDO-IND FROM CUENTAS WHERE ID = :WS-ID
END-EXEC

IF WS-SALDO-IND < 0     *> el indicador negativo significa NULL
    DISPLAY "sin saldo informado"
END-IF
```
"""),
        "fortran": ("""
program nulable
   implicit none
   integer, allocatable :: valor
   integer :: n

   read(*, *) n
   if (n /= 0) allocate(valor, source=n)

   if (allocated(valor)) then
      write(*, '(A,I0)') 'valor=', valor
   else
      write(*, '(A)') 'valor=ausente'
   end if
end program nulable
""", """
**Lo que esta clase enseña en Fortran.** El Fortran clásico tampoco tenía forma de expresar la
ausencia, y usaba los mismos centinelas que COBOL —el `-999` de los ficheros de datos científicos es
una institución—. El Fortran moderno tiene **dos** mecanismos, y los dos son buenos.

El primero es el de este programa: **un escalar `allocatable`**. Una variable que puede estar
asignada o no, y `allocated()` lo pregunta. No es un puntero: no puede apuntar a otra cosa, no se
puede desreferenciar por error y **se libera sola al salir del ámbito**. Es, en la práctica, un
`Option` sin sintaxis especial.

El segundo es para argumentos, y es el que se usa a diario:

```fortran
subroutine dibujar(x, y, color)
   integer, intent(in) :: x, y
   integer, intent(in), optional :: color      ! puede no venir
   if (present(color)) then
      ...
   end if
end subroutine
```

`optional` más `present()` resuelve el argumento ausente **sin necesidad de un valor centinela ni de
sobrecargas**. Java, C y Go no lo tienen; C++ lo aproxima con valores por defecto, que no distinguen
"no lo pasó" de "pasó justo el valor por defecto".

Y hay un tercer estado en Fortran que conviene conocer: los **punteros** (`pointer`) tienen tres
situaciones —asociado, no asociado e **indefinido**—, y `associated()` sobre uno indefinido es
comportamiento indeterminado. De ahí que la guía moderna sea usar `allocatable` siempre que se pueda
y `pointer` solo cuando haga falta apuntar de verdad.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Nulable is
   type Acceso_Entero is access Integer;

   Valor : Acceso_Entero := null;
   N     : Integer;
begin
   Get (N);
   if N /= 0 then
      Valor := new Integer'(N);
   end if;

   if Valor = null then
      Put_Line ("valor=ausente");
   else
      Put ("valor="); Put (Valor.all, Width => 1); New_Line;
   end if;
end Nulable;
""", """
**Lo que esta clase enseña en Ada.** Ada tiene `null`, pero **solo para los tipos de acceso**
(punteros). Un `Integer` nunca puede ser nulo, así que el error de Hoare está acotado a los sitios
donde escribiste `access`.

Y desde **Ada 2005** hay algo que casi ningún lenguaje de esta lista ofrece: un tipo de puntero que
**no puede ser nulo**, comprobado por el compilador.

```ada
type Acceso_Entero      is access Integer;             --  puede ser null
subtype Acceso_Seguro   is not null Acceso_Entero;     --  NO puede ser null

procedure Procesar (P : not null Acceso_Entero);       --  el parámetro tampoco
```

Con `not null`, el compilador rechaza asignarle `null` y **elimina la comprobación en el punto de
uso**, porque ya la hizo antes. Es la misma idea que `&T` frente a `Option<&T>` en Rust y que los
tipos no nulos de Kotlin, disponible en 2005.

Ada tiene además una segunda respuesta, más idiomática y sin memoria dinámica:

```ada
type Valor_Opcional (Presente : Boolean := False) is record
   case Presente is
      when True  => Dato : Integer;
      when False => null;
   end case;
end record;
```

Es un **registro con discriminante**, es decir, un tipo suma comprobado por el compilador: si accedes
a `Dato` sin que `Presente` sea cierto, salta `Constraint_Error`. Es el `Option` de Rust y el
`sealed interface` de Java, escrito en 1983 y sin tocar el montículo — que es justo lo que un sistema
de aviónica necesita.
"""),
        "pascal": ("""
program Nulable;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N: Integer;
  Valor: ^Integer;

begin
  Read(N);

  Valor := nil;
  if N <> 0 then
  begin
    New(Valor);
    Valor^ := N;
  end;

  if Valor = nil then
    WriteLn('valor=ausente')
  else
    WriteLn('valor=', IntToStr(Valor^));

  if Valor <> nil then Dispose(Valor);
end.
""", """
**Lo que esta clase enseña en Pascal.** `nil` existe **solo para punteros**, igual que en Ada. Un
`Integer` no puede ser `nil`, así que el problema queda acotado.

Lo que Pascal aporta a esta clase es que **el puntero tiene tipo**, y en 1970 eso no era evidente.
`^Integer` apunta a un entero y a nada más: no se puede asignar a un `^Real` sin conversión, ni hacer
aritmética sobre él, ni desreferenciar a otro tipo. Compara con C, donde un `void*` va a cualquier
sitio y `p + 1` mueve el puntero según un tamaño que hay que recordar.

Fíjate también en el par **`New`/`Dispose`**, que es el `malloc`/`free` de Pascal con una diferencia
importante: **`New` conoce el tipo**, así que reserva el tamaño correcto sin que se lo digas. En C,
`malloc(sizeof(int))` con el `sizeof` equivocado compila perfectamente.

Y la trampa clásica: **`Dispose` no pone el puntero a `nil`**. Tras liberarlo, `Valor` sigue
apuntando a memoria que ya no es tuya —un *dangling pointer*— y `Valor = nil` da falso. El idioma
correcto es `Dispose(Valor); Valor := nil;`, y la razón de que Object Pascal añadiera `FreeAndNil`
para los objetos, que hace las dos cosas.
"""),
        "lisp": ("""
(let* ((n (read))
       (valor (if (zerop n) nil n)))
  (if valor
      (format t "valor=~D~%" valor)
      (format t "valor=ausente~%")))
""", """
**Lo que esta clase enseña en Common Lisp.** `nil` es la ausencia… y también el falso lógico, y
también la lista vacía, y también el símbolo `nil`. **Cuatro papeles en un solo objeto**, y esa
sobrecarga es una de las decisiones más discutidas de la historia del lenguaje.

Es cómoda —`(if lista ...)` funciona para "¿hay elementos?"— y es ambigua, porque no se puede
distinguir "no hay valor" de "el valor es la lista vacía" ni de "el valor es falso". Scheme lo
resolvió separándolos: allí `'()` y `#f` son objetos distintos.

Cuando la distinción importa, el idioma de Common Lisp es devolver **dos valores**, el mismo
mecanismo de la clase 049:

```lisp
(gethash 'clave tabla)
; => NIL, NIL     la clave no está
; => NIL, T       la clave SÍ está, y su valor es NIL

(multiple-value-bind (valor encontrado) (gethash 'clave tabla)
  (if encontrado ...))
```

El segundo valor separa "no está" de "está y vale `nil`". Es exactamente el patrón `value, ok :=` de
Go, treinta años antes, y con la ventaja de que ignorarlo es gratis y no obliga a escribir `_`.

Y una nota sobre `(if valor ...)`: funciona aquí porque el contrato dice que 0 significa ausente,
pero **en Lisp `0` es verdadero**. En un caso general habría que escribir `(if (null valor) ...)` en
vez de confiar en la falsedad — la trampa que ya apareció en la clase 043.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

if {$n != 0} { set valor $n }

if {[info exists valor]} {
    puts "valor=$valor"
} else {
    puts "valor=ausente"
}
""", """
**Lo que esta clase enseña en Tcl.** No hay `null`, no hay `nil` y no hay `undef`. La cadena vacía es
un valor perfectamente normal, así que no puede hacer de ausencia. Lo que Tcl tiene en su lugar es
**la variable que no existe**, y `info exists` es cómo se pregunta.

Es una distinción más limpia de lo que parece: en vez de un valor especial dentro de la variable, la
ausencia está **fuera** de ella. `unset valor` la devuelve al estado de no existir. Y leer una
variable inexistente **no da `nil`: da un error**, lo que evita que la ausencia se propague en
silencio como ocurre con `undefined` en JavaScript.

Lo mismo se aplica a los diccionarios y a los arrays asociativos:

```tcl
info exists arr(clave)      ;# ¿existe ese elemento?
dict exists $d clave        ;# lo mismo para un dict
dict get $d clave           ;# ERROR si no existe -- no devuelve vacío
```

Que el acceso falle en vez de devolver un valor por defecto es la decisión contraria a la de PHP y a
la de M, y significa que un error de escritura en el nombre de una clave se detecta al instante.

El contrapunto honesto: como las variables se crean al asignarlas, **una errata en un `set` crea una
variable nueva** en silencio, igual que en Perl sin `use strict`. Tcl no tiene un `strict` que lo
impida.
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

my $valor = $n != 0 ? $n : undef;

printf "valor=%s\\n", defined($valor) ? $valor : 'ausente';
""", """
**Lo que esta clase enseña en Perl.** `undef` es un valor de primera clase que significa "sin
definir", y `defined()` es cómo se pregunta. Lo importante es que **`defined` y "verdadero" son
cosas distintas**, porque `0` y `""` son falsos pero están perfectamente definidos.

Esa distinción es la que Perl resolvió con un operador propio, y merece conocerse porque es la
respuesta a un error muy común:

```perl
my $reintentos = $config{reintentos} || 3;   # MAL: si vale 0, pone 3
my $reintentos = $config{reintentos} // 3;   # BIEN: solo si es undef
```

`||` mira la **verdad**; `//` mira la **definición**. Un contador configurado a cero es un valor
legítimo que `||` destruye. JavaScript adoptó exactamente el mismo operador —`??`— en 2020 por
exactamente el mismo motivo, y le añadió `??=` igual que Perl tiene `//=`.

Perl distingue además **tres estados** donde otros ven dos, y esta clase es el sitio para verlos:

```perl
exists $h{clave}     # ¿existe la clave?
defined $h{clave}    # ¿tiene valor?  (existe pero puede ser undef)
$h{clave}            # ¿es verdadero? (puede ser 0 o "")
```

Los tres son preguntas diferentes y confundirlos es la fuente de errores más común con hashes. Es el
mismo trío que en Tcl (`info exists`) y en M (`$data`), y una vez que se ve en tres lenguajes
distintos deja de parecer una rareza para parecer lo que es: **la forma correcta de modelar la
ausencia**.
"""),
        "cpp": ("""
#include <iostream>
#include <optional>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    std::optional<int> valor;          // vacío por defecto
    if (n != 0) valor = n;

    if (valor.has_value()) {
        std::cout << "valor=" << *valor << '\\n';
    } else {
        std::cout << "valor=ausente\\n";
    }
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** `std::optional<int>` (C++17) es la respuesta moderna, y su valor
está en lo que **no** hace: no reserva memoria dinámica, no es un puntero y **no se puede
desreferenciar por accidente sin que el código lo diga**. El objeto contiene el entero y un booleano,
en la pila.

Compara con la alternativa antigua, `int*`, que arrastra tres significados a la vez —"no hay valor",
"apunta a un entero", "apunta a un array de enteros"— y no dice cuál.

Las formas de sacar el valor están graduadas a propósito:

```cpp
*valor                      // rápido; UB si está vacío -- tú garantizas que hay
valor.value()               // lanza std::bad_optional_access si está vacío
valor.value_or(0)           // valor por defecto
if (valor) { ... }          // conversión a bool explícita
```

Que existan las cuatro es la filosofía de C++: la insegura y rápida disponible, pero **con un nombre
distinto** para que se vea en la revisión de código.

Y C++23 añadió las operaciones **monádicas** —`and_then`, `transform`, `or_else`— que permiten
encadenar sin escribir `if` anidados, tomando prestado directamente de Rust y de Haskell:

```cpp
auto r = buscar(id).and_then(validar).transform(formatear).value_or("desconocido");
```

Los punteros crudos, claro, siguen ahí. `nullptr` (C++11) al menos sustituyó al `NULL` de C, que era
literalmente `0` y se colaba en sobrecargas que esperaban un entero.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi NULABLE;
  n int(10) const;
end-pi;

dcl-s valor  int(10);
dcl-s hay    ind inz(*off);
dcl-s salida char(40);

if n <> 0;
  valor = n;
  hay = *on;
endif;

if hay;
  salida = 'valor=' + %char(valor);
else;
  salida = 'valor=ausente';
endif;
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** Como COBOL, RPG **no tiene null en sus tipos**: un `int(10)`
siempre vale algo. La ausencia se lleva en una **variable aparte** —aquí el indicador `hay`—, que es
exactamente la estructura interna de `std::optional`, escrita a mano.

Pero RPG tiene una respuesta de primera clase para el sitio donde esto importa de verdad, que es la
base de datos. **Db2 for i sí tiene nulos**, y RPG los maneja con `%nullind`:

```rpgle
dcl-f CLIENTES usage(*input) alwnull(*usrctl);

read CLIENTES;
if %nullind(CLI_SALDO);          // ¿el campo es NULL en la fila leída?
  // no informado
else;
  total += CLI_SALDO;
endif;

%nullind(CLI_FECHA) = *on;       // y se puede ESCRIBIR: marcar el campo como nulo
```

`%nullind(campo)` es un booleano **asociado al campo** que se lee y se escribe. La ausencia no viaja
dentro del dato: viaja **en paralelo**, exactamente como los indicadores de nulo del SQL embebido en
COBOL.

Y `alwnull(*usrctl)` es la palabra clave que hay que recordar: **sin ella, RPG lee un campo nulo como
su valor por defecto —cero o blancos— sin avisar**. El comportamiento por defecto de la plataforma
es el centinela silencioso; hay que pedir explícitamente que te dejen ver la diferencia.
"""),
        "pli": ("""
 nulable: procedure options(main);

    declare n     fixed binary(31);
    declare p     pointer initial(null());
    declare valor fixed binary(31) based(p);

    get list (n);
    if n ^= 0 then do;
       allocate valor set(p);
       valor = n;
    end;

    if p = null() then
       put skip list ('valor=ausente');
    else
       put skip list ('valor=' || trim(char(valor)));

 end nulable;
""", """
**Lo que esta clase enseña en PL/I.** `null()` es una **función incorporada** que devuelve el puntero
nulo, no una palabra clave. Y las variables `based(p)` son la construcción característica: `valor`
**no tiene almacenamiento propio**, vive donde apunte `p`. Cambiar `p` cambia a qué mira `valor`, sin
tocar ninguna sintaxis de desreferencia.

Es potente y es exactamente lo que hoy se considera peligroso: el mismo nombre puede referirse a
memoria distinta en cada momento, y si `p` es nulo, **usar `valor` es comportamiento indefinido sin
ninguna marca visible en el punto de uso**. En C al menos hay que escribir `*p`.

PL/I ofrece a cambio algo que compensa parcialmente: la condición `ON` puede capturar el error.

```pli
on error begin;
   put skip list ('acceso invalido');
end;
```

Y para el caso de esta clase, el mundo PL/I real usa el mismo recurso que COBOL: **campos indicadores
en paralelo** al hablar con Db2, y valores centinela documentados dentro del programa.

La lección de diseño que deja aquí, y que enlaza con la clase 050, es la misma: PL/I da mecanismos
muy potentes y **ninguna barandilla**. `based` es la abstracción que permitió escribir Multics en un
lenguaje de alto nivel; también es la que hace que revisar un PL/I ajeno cueste tanto.
"""),
        "mumps": ("""
NULABLE ; Nulabilidad -- clase 053
 read n
 if n'=0 set valor = n
 if $data(valor) write "valor=", valor, ! quit
 write "valor=ausente", !
 quit
""", """
**Lo que esta clase enseña en M.** La mejor respuesta de toda la página, y la menos conocida.
**`$data(x)` no devuelve un booleano: devuelve cuatro valores posibles**, porque en M una variable no
es una casilla, es un **nodo de un árbol**:

| `$data` | Significado |
|---|---|
| **0** | No existe: ni valor ni descendientes |
| **1** | Tiene valor y **no** tiene descendientes |
| **10** | **No tiene valor** pero sí tiene descendientes |
| **11** | Tiene valor **y** descendientes |

El estado **10** es el que no existe en ningún otro lenguaje de esta lista. Significa: `^PACIENTE(7)`
no tiene ningún dato propio, pero `^PACIENTE(7,"nombre")` sí existe. Es un nodo intermedio de un árbol
disperso — algo que en un modelo de objetos se representaría con un objeto vacío, y que aquí es un
estado del propio dato.

Y es útil de verdad. Recorrer una estructura clínica exige distinguir "este paciente no está" de
"este paciente existe pero no tiene alergias registradas" de "tiene alergias y además una nota". Un
booleano no daría para eso.

M añade `$get(x)` como atajo —devuelve el valor o la cadena vacía si no existe, con un valor por
defecto opcional: `$get(x, "sin datos")`— que es el `value_or` de C++ y el `//` de Perl.

La ironía de esta página: el lenguaje sin tipos y sin declaraciones tiene el modelo de ausencia más
matizado de los doce.
"""),
        "smalltalk": ("""
| n valor |

n := stdin nextLine trimBoth asNumber.
valor := n = 0 ifTrue: [ nil ] ifFalse: [ n ].

Transcript
    show: 'valor=', (valor ifNil: [ 'ausente' ] ifNotNil: [ :v | v printString ]);
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** `nil` **es un objeto**: la única instancia de la clase
`UndefinedObject`. No es una palabra clave ni un puntero nulo — tiene clase, responde a mensajes, y
puedes abrir su implementación en el navegador.

Eso cambia por completo la ergonomía de la ausencia, porque los métodos de manejo están **en el
propio `nil`**:

```smalltalk
nil isNil            "true"
nil ifNil: [ 0 ]     "0 -- implementado en UndefinedObject como: ^unBloque value"
5   ifNil: [ 0 ]     "5 -- implementado en Object como: ^self"
valor ifNil: [ 'ausente' ] ifNotNil: [ :v | v printString ]
```

`ifNil:` está implementado dos veces: en `UndefinedObject` evalúa el bloque, y en `Object` devuelve
`self`. **Otra vez el condicional resuelto por polimorfismo**, igual que `ifTrue:` en la clase 046.
No hay ninguna comprobación de nulo en el lenguaje; hay dos métodos.

Y `ifNotNil:` recibe un bloque **con parámetro**, así que el valor no nulo llega ya desempaquetado.
Es el `map` de un `Option`, disponible con esa sintaxis desde hace décadas.

La contrapartida honesta: como cualquier variable puede valer `nil`, Smalltalk **no** tiene la
garantía estática que dan `not null` de Ada o los tipos no nulos de Kotlin. El error de Hoare sigue
siendo posible; lo que cambia es que enviar un mensaje a `nil` no revienta el proceso, **abre el
depurador con la pila viva** y permite arreglarlo y continuar.
"""),
    },
)

# ---------------------------------------------------------------------------
# 054 — Mutabilidad e inmutabilidad
# ---------------------------------------------------------------------------
SPECS["054"] = dict(
    gancho="""
Construir `1-2-3-4-5` juntando trozos. Es el ejercicio que convierte la mutabilidad en algo
observable: **¿cada `+=` crea una cadena nueva y tira la anterior, o modifica la que ya había?** La
respuesta no cambia el resultado, cambia el rendimiento — y en un bucle de cien mil vueltas la
diferencia entre las dos es la diferencia entre un segundo y un minuto.
""",
    porque="""
Aquí el concepto es **quién puede cambiar un valor y qué cuesta**, y estos lenguajes lo enseñan
porque cubren el arco entero. En COBOL una cadena es un **campo de posiciones fijas** que se modifica
en el sitio: no hay asignación que copie, hay escritura sobre bytes concretos. En Fortran hasta 2003
**no se podía** hacer crecer una cadena, así que este programa era imposible de escribir tal cual.
Y en Smalltalk y Lisp la respuesta es un **flujo de escritura**, que es la misma solución que hoy
llamamos `StringBuilder`.

Además aparece un concepto que casi ningún lenguaje moderno tiene explícito: la **copia al escribir**
de Pascal y Delphi, donde asignar una cadena no copia nada hasta que alguien la modifica.
""",
    cierre="""
La regla transferible es la del **acumulador**: concatenar dentro de un bucle con el operador normal
es cuadrático en los lenguajes de cadenas inmutables —Java, C#, Python, y también Lisp y Smalltalk si
usas `,`— porque cada vuelta copia todo lo acumulado. La solución tiene el mismo nombre en todas
partes aunque se escriba distinto: **un búfer que crece** — `WriteStream`, `with-output-to-string`,
`StringBuilder`, `std::string::reserve`, `Unbounded_String`. Reconocer ese patrón es lo que se lleva
uno de esta clase.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. SECUENCIA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC 9(4) COMP-3.
01  I       PIC 9(4) COMP-3.
01  ED-I    PIC Z(3)9.
01  TROZO   PIC X(10).
01  LON-T   PIC 9(4) COMP-3.
01  SEC     PIC X(200).
01  LARGO   PIC 9(4) COMP-3.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N
    MOVE SPACES TO SEC
    MOVE 1 TO LARGO

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        MOVE I TO ED-I
        MOVE FUNCTION TRIM(ED-I) TO TROZO
        COMPUTE LON-T = FUNCTION LENGTH(FUNCTION TRIM(TROZO))
        IF I > 1
            MOVE "-" TO SEC(LARGO:1)
            ADD 1 TO LARGO
        END-IF
        MOVE TROZO(1:LON-T) TO SEC(LARGO:LON-T)
        ADD LON-T TO LARGO
    END-PERFORM

    DISPLAY "sec=" FUNCTION TRIM(SEC)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** En COBOL **todo es mutable y nada se copia de más**. `SEC` es
un bloque de 200 bytes que existe desde que arranca el programa, y `MOVE ... TO SEC(LARGO:LON-T)`
escribe **directamente sobre las posiciones indicadas**. No hay asignación que construya una cadena
nueva, no hay memoria que reservar, no hay recolector que despertar.

Por eso este bucle es lineal por construcción: cada vuelta escribe sus dos o tres bytes y avanza el
puntero `LARGO`. El problema del acumulador cuadrático —el que sufren Java, Python y C# al concatenar
en un bucle— **no puede ocurrir aquí**, porque no hay una operación de concatenación que copie.

El precio está en la otra columna: `SEC` mide 200 bytes tanto si guarda `"1"` como si guarda la
secuencia completa, hay que **calcular a mano si cabe**, y escribir más allá del final es
comportamiento indefinido —COBOL no comprueba los límites de la modificación de referencia salvo que
se compile con `-fec=bound-ref-mod` en GnuCOBOL o con `SSRANGE` en el compilador de IBM—.

Es exactamente el mismo intercambio que hace C: control total y coste predecible, a cambio de que la
seguridad la ponga el programador. Y la lección de esta clase es que **la inmutabilidad no es
gratuita ni obviamente superior**: es una decisión que cambia dónde se paga.
"""),
        "fortran": ("""
program secuencia
   implicit none
   integer :: n, i
   character(len=:), allocatable :: sec
   character(len=16) :: buf

   read(*, *) n

   sec = ''
   do i = 1, n
      write(buf, '(I0)') i
      if (i > 1) sec = sec // '-'
      sec = sec // trim(buf)
   end do

   write(*, '(A,A)') 'sec=', sec
end program secuencia
""", """
**Lo que esta clase enseña en Fortran.** **Este programa no se podía escribir en Fortran antes de
2003.** Una cadena tenía longitud fija decidida al declararla, y no había forma de hacerla crecer: la
única salida era declarar un búfer enorme y llevar un contador a mano, exactamente como hace COBOL.

Lo que lo hace posible es `character(len=:), allocatable`, la **longitud diferida**: al asignar,
Fortran **reasigna** la variable con el tamaño exacto del valor nuevo. `sec = sec // '-'` libera la
anterior, reserva una mayor y copia.

Y eso es justo lo que hay que ver en esta clase: **es cómodo y es cuadrático**. Cada vuelta copia
todo lo acumulado. Con `n` de cinco no importa; con un millón, sí. La versión rápida vuelve a
parecerse a COBOL:

```fortran
character(len=8*n) :: buffer      ! reserva de una vez
integer :: pos
pos = 1
do i = 1, n
   write(buffer(pos:), '(I0)') i
   pos = pos + len_trim(...)
end do
```

Fortran ofrece las dos y no oculta la diferencia, que es lo mejor que puede hacer un lenguaje
orientado al rendimiento. La comodidad de 2003 no borró la herramienta de 1977: la puso al lado.
"""),
        "ada": ("""
with Ada.Text_IO;           use Ada.Text_IO;
with Ada.Integer_Text_IO;   use Ada.Integer_Text_IO;
with Ada.Strings;           use Ada.Strings;
with Ada.Strings.Fixed;
with Ada.Strings.Unbounded; use Ada.Strings.Unbounded;

procedure Secuencia is
   N   : Integer;
   Sec : Unbounded_String := Null_Unbounded_String;
begin
   Get (N);

   for I in 1 .. N loop
      if I > 1 then
         Append (Sec, "-");
      end if;
      Append (Sec, Ada.Strings.Fixed.Trim (Integer'Image (I), Both));
   end loop;

   Put_Line ("sec=" & To_String (Sec));
end Secuencia;
""", """
**Lo que esta clase enseña en Ada.** Ada obliga a **elegir el modelo de cadena en la declaración**, y
esa elección es una decisión de ingeniería con consecuencias que el lenguaje deja a la vista:

| Tipo | Longitud | Memoria dinámica | Dónde se usa |
|---|---|---|---|
| `String` | Fija al crear | No | Lo normal; porciones y arrays |
| `Bounded_String` | Variable, con **máximo declarado** | **No** | Sistemas críticos |
| `Unbounded_String` | Libre | Sí | Aplicaciones normales |

`Unbounded_String` es lo que este programa usa, y `Append` **modifica en el sitio** en lugar de
construir una cadena nueva, así que el bucle es amortizadamente lineal — no cuadrático como la
versión de Fortran.

Lo interesante es la fila del medio. En aviónica y ferrocarril se usa `Bounded_String` precisamente
**porque no toca el montículo**: el tamaño máximo se conoce al compilar, así que no hay fragmentación,
no hay fallos de asignación imprevisibles y el consumo de memoria del programa entero es analizable
antes de ejecutarlo. Si el texto no cabe, se levanta una excepción o se trunca según la política que
elijas — pero **nunca se pide memoria en vuelo**.

Es la mejor ilustración de esta clase: la mutabilidad y la asignación dinámica no son un detalle de
estilo, son una propiedad certificable del sistema.
"""),
        "pascal": ("""
program Secuencia;
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
    Sec := Sec + IntToStr(I);
  end;

  WriteLn('sec=', Sec);
end.
""", """
**Lo que esta clase enseña en Pascal.** Con `{$H+}`, `string` es un `AnsiString`: longitud variable,
**conteo de referencias** y **copia al escribir** (*copy-on-write*). Y eso hace de Pascal el mejor
ejemplo de esta clase, porque su modelo no es "mutable" ni "inmutable": es **las dos cosas según el
momento**.

```pascal
A := 'hola';
B := A;          { NO copia el texto: copia un puntero y suma 1 al contador }
B := B + '!';    { AHORA sí copia, porque el contador era 2 y hay que separar }
```

Asignar es O(1). Modificar cuando alguien más comparte el dato provoca la copia; modificar cuando
eres el único dueño se hace **en el sitio**. El programador no ve nada de esto: obtiene la semántica
de valor —nadie te cambia tu cadena por detrás— con el coste de la referencia mientras no haga falta
copiar.

Es el mismo mecanismo que usan PHP, Swift y las cadenas de Delphi, y explica por qué en Pascal se
pueden pasar cadenas grandes por valor sin pensárselo.

El bucle de este programa **sigue siendo cuadrático**, porque `Sec + IntToStr(I)` crea un resultado
nuevo cada vuelta. La versión lineal usa `SetLength` para reservar y escribir por índice, o
`TStringBuilder` en Delphi — el mismo patrón del acumulador que aparece en todos los lenguajes de
cadenas con semántica de valor.
"""),
        "lisp": ("""
(let ((n (read)))
  (format t "sec=~{~D~^-~}~%" (loop for i from 1 to n collect i)))
""", """
**Lo que esta clase enseña en Common Lisp.** La solución no construye ninguna cadena: construye
**una lista** y deja que `format` la recorra. `~{` … `~}` itera sobre los elementos, `~D` imprime
cada uno, y **`~^` corta la iteración si no quedan más**, lo que hace que el guion aparezca *entre*
los elementos y no al final. Es el problema del separador resuelto en cuatro caracteres.

Y esta clase toca el corazón de la distinción de Lisp entre **funciones destructivas y no
destructivas**, que el lenguaje marca por convención en el nombre:

| No destructiva | Destructiva | Qué hace la destructiva |
|---|---|---|
| `append` | `nconc` | Reutiliza las celdas en vez de copiar |
| `remove` | `delete` | Modifica la lista original |
| `reverse` | `nreverse` | Invierte los punteros en el sitio |
| `sort` (copia) | `sort` sobre la propia lista | Puede destruir el original |

Las destructivas empiezan por `n` —de *non-consing*, "sin reservar memoria"— y son mucho más
rápidas. También son la fuente de los errores más difíciles del lenguaje, porque **el argumento
original queda en un estado indeterminado** y seguir usándolo produce comportamientos imposibles de
reproducir.

La regla de la comunidad es clara y vale para cualquier lenguaje: **usa la versión no destructiva
hasta que midas que importa**, y cuando uses la destructiva, no vuelvas a tocar el original.
Para acumular texto, el idioma es `with-output-to-string`, que es un `StringBuilder` con otra cara.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

set sec {}
for {set i 1} {$i <= $n} {incr i} {
    lappend sec $i
}

puts "sec=[join $sec -]"
""", """
**Lo que esta clase enseña en Tcl.** `lappend` y `join` en lugar de concatenar en el bucle, y esa
elección es exactamente el tema de la clase.

En Tcl todo valor es **inmutable a nivel semántico**: `set b $a` no copia, comparte la representación
interna y sube un contador de referencias —igual que el `AnsiString` de Pascal—. Y aquí está la
optimización que hay que conocer, porque es la razón de escribir `lappend` y no `set sec "$sec $i"`:

**`lappend` está especializado para modificar en el sitio cuando el contador de referencias es 1.**
Si nadie más comparte la lista, la amplía sin copiar. `set sec "$sec-$i"` construiría una cadena
nueva cada vuelta, y el bucle sería cuadrático.

La misma optimización existe en `append` para cadenas:

```tcl
append sec "-$i"      ;# modifica en el sitio si es posible: LINEAL
set sec "$sec-$i"     ;# construye una cadena nueva: CUADRÁTICO
```

Dos líneas que hacen lo mismo con complejidades distintas. Es el detalle de rendimiento más citado en
la comunidad Tcl, y es la versión de este lenguaje del `StringBuilder` de Java: el mecanismo está
ahí, pero hay que usar el comando correcto para activarlo.

`join $sec -` une la lista con el separador, resolviendo el problema del guion sin ningún `if`.
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

print "sec=", join('-', 1 .. $n), "\\n";
""", """
**Lo que esta clase enseña en Perl.** Una línea, y sin bucle. `1 .. $n` es el **operador de rango**,
que en contexto de lista genera todos los enteros, y `join` los une con el separador. El problema del
guion intercalado desaparece porque nunca se construye la cadena a mano.

Sobre la mutabilidad, Perl es el más permisivo de esta página: **las cadenas son mutables y se pueden
modificar en el sitio de formas que en Java o Python no existen**.

```perl
my $s = "hola mundo";
substr($s, 0, 4) = "HOLA";     # substr como DESTINO de una asignación
substr($s, 0, 4, "adio");      # o con cuatro argumentos, misma idea
$s =~ tr/a-z/A-Z/;             # transliteración EN EL SITIO
$s =~ s/mundo/planeta/;        # sustitución EN EL SITIO
chop $s;  chomp $s;            # recortan la variable, no devuelven copia
```

Y el acumulador es lineal sin trucos: `$sec .= "-$i"` en un bucle **modifica el escalar**, ampliando
su búfer cuando hace falta. No hay `StringBuilder` en Perl porque no hace falta — la cadena ya es un
búfer que crece.

Ese es el intercambio de Perl en esta clase: máxima eficiencia al modificar y **ninguna garantía de
que nadie te cambie una cadena por debajo**. Si pasas un escalar a una función, esa función puede
modificarlo, porque `@_` contiene **alias** de los argumentos originales, no copias. Es un detalle que
sorprende y que conviene conocer antes de leer código ajeno.
"""),
        "cpp": ("""
#include <iostream>
#include <string>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    std::string sec;
    sec.reserve(static_cast<std::size_t>(n) * 4);   // reserva: evita realojos

    for (int i = 1; i <= n; ++i) {
        if (i > 1) sec += '-';
        sec += std::to_string(i);
    }

    std::cout << "sec=" << sec << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** `std::string` es **mutable** y `+=` modifica en el sitio: amplía
el búfer interno cuando se queda corto, duplicando su capacidad. Por eso este bucle es amortizadamente
lineal y no cuadrático, al contrario que el equivalente en Java con `String`.

Y `reserve()` es la línea que hay que entender. Sin ella, la cadena crece a saltos y cada salto
**copia todo lo acumulado** a un búfer nuevo; con ella, se reserva una vez y no hay ningún realojo.
Es el mismo concepto que `ArrayList.ensureCapacity` en Java o `Vec::with_capacity` en Rust, y es la
optimización más rentable que existe cuando se conoce el tamaño aproximado de antemano.

C++ separa además **capacidad** de **tamaño**, y las expone las dos: `size()` es cuánto hay,
`capacity()` es cuánto cabe sin volver a reservar. Casi ningún lenguaje de esta página deja ver esa
diferencia; en C++ es parte de la interfaz porque el control de la memoria es el punto.

Y el contrapunto: la mutabilidad tiene un coste de corrección que C++ gestiona con `const`.

```cpp
void mostrar(const std::string& s);   // promete no modificar: se pasa sin copiar
void modificar(std::string& s);       // puede modificar: el llamante lo ve en la firma
void copiar(std::string s);           // copia entera
```

Esas tres firmas son tres contratos distintos, visibles en el punto de llamada. Es la respuesta de
C++ al problema que Perl deja abierto con los alias de `@_`.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi SECUENC;
  n int(10) const;
end-pi;

dcl-s sec    varchar(500) inz('');
dcl-s i      int(10);
dcl-s salida char(520);

for i = 1 to n;
  if i > 1;
    sec += '-';
  endif;
  sec += %char(i);
endfor;

salida = 'sec=' + sec;
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** `varchar(500)` es un búfer de 500 bytes con un contador de
longitud delante, y `+=` **escribe sobre él y actualiza el contador**. No hay reserva, no hay realojo
y no hay recolector: el bucle es lineal y el consumo de memoria está decidido en la declaración.

Es el mismo modelo de COBOL —memoria estática, escritura en el sitio— pero con la longitud
gestionada por el lenguaje en vez de por un contador a mano. Ese es el salto que RPG dio con
`varchar` y que COBOL solo ofrece desde 2002.

El límite es real y hay que dimensionarlo: si la secuencia pasa de 500 caracteres, **se trunca**.
En RPG moderno el máximo de un `varchar` es de 16 MB, así que sobra margen, pero la decisión sigue
siendo del programador. Y para tamaños de verdad grandes existen los campos `CLOB`.

Fíjate en el operador `+=`, que RPG incorporó en la versión 7.1 junto a `-=`, `*=` y `/=`. Antes se
escribía `sec = sec + '-'`, con el mismo efecto: el compilador ya reconocía el patrón y escribía en
el sitio. La novedad fue sintáctica, no semántica — pero cambió cómo se lee el código, que en un
lenguaje que se mantiene durante treinta años no es poco.
"""),
        "pli": ("""
 secuencia: procedure options(main);

    declare n   fixed binary(31);
    declare i   fixed binary(31);
    declare sec character(500) varying initial('');

    get list (n);

    do i = 1 to n;
       if i > 1 then sec = sec || '-';
       sec = sec || trim(char(i));
    end;

    put skip list ('sec=' || sec);

 end secuencia;
""", """
**Lo que esta clase enseña en PL/I.** `character(500) varying` es el mismo modelo que el `varchar` de
RPG: un búfer de tamaño máximo declarado, con la longitud actual guardada delante. La asignación
`sec = sec || '-'` **escribe sobre el mismo almacenamiento**, así que el bucle es lineal.

Lo que PL/I añade a esta clase es un concepto que no tiene ningún otro lenguaje de la página: la
**variable `DEFINED`**, que da un nombre alternativo a un almacenamiento que ya existe.

```pli
declare buffer  character(500);
declare cabecera character(10) defined(buffer);              /* los 10 primeros */
declare cuerpo   character(490) defined(buffer) position(11);/* del 11 en adelante */
```

`cabecera` y `cuerpo` **no son copias**: son ventanas sobre `buffer`. Modificar una modifica el otro,
porque son la misma memoria vista con otro nombre y otro tipo. Es una `union` de C con sintaxis de
declaración, y en su día era la forma de descomponer un registro leído de un fichero sin copiarlo.

Visto hoy es exactamente lo que hace `std::string_view` en C++ o un *slice* en Go y Rust: **una vista
sobre memoria ajena**. Con el mismo peligro, que en PL/I no está mitigado por nada: si `buffer` se
reasigna, las ventanas siguen apuntando ahí.
"""),
        "mumps": ("""
SECUEN ; Secuencia -- clase 054
 read n
 set sec = ""
 for i = 1:1:n do
 . set:i>1 sec = sec _ "-"
 . set sec = sec _ i
 write "sec=", sec, !
 quit
""", """
**Lo que esta clase enseña en M.** Tres cosas de sintaxis y una de fondo.

De sintaxis: **`for i = 1:1:n`** es "desde 1, de 1 en 1, hasta n" —los dos puntos separan inicio,
incremento y final—. El **punto al principio de línea** marca el nivel de anidamiento del bloque que
abre `do`. Y **`set:i>1`** es el postcondicional: el comando se ejecuta solo si la condición se
cumple, sin necesidad de un `if`.

De fondo: en M las cadenas son mutables y `_` concatena sobre el mismo valor, así que el bucle es
eficiente. Pero **la verdadera lección de mutabilidad en M está en los *globals***.

```mumps
set ^LISTA(1) = "uno"      ; esto YA está en disco
set ^LISTA(1) = "UNO"      ; y esto lo ha modificado, para todos los procesos
```

No hay una operación de guardado. **La asignación es la escritura.** Y es visible inmediatamente para
cualquier otro proceso que lea ese nodo, sin caché que invalidar ni sesión que sincronizar.

Eso convierte la mutabilidad en un asunto de **concurrencia**, no de rendimiento, y por eso M tiene
`lock` —bloqueos por nodo, cooperativos— y `tstart`/`tcommit` para transacciones. En un lenguaje donde
asignar una variable puede modificar el historial clínico que otro terminal está leyendo, la pregunta
"¿esto es mutable?" tiene una respuesta con consecuencias muy distintas de las de un `String` en Java.
"""),
        "smalltalk": ("""
| n sec |

n := stdin nextLine trimBoth asNumber.

sec := String streamContents: [ :flujo |
    (1 to: n)
        do:           [ :i | flujo print: i ]
        separatedBy:  [ flujo nextPut: $- ] ].

Transcript show: 'sec=', sec; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** `String streamContents:` es el `StringBuilder` de
Smalltalk, y existe desde mucho antes de que Java lo necesitara. Crea un `WriteStream` sobre un búfer
que crece, ejecuta el bloque escribiendo en él, y devuelve la cadena final. **Una sola reserva
amortizada, en vez de una cadena nueva por vuelta.**

Si el bucle usara `sec := sec , i printString`, cada `,` construiría una colección nueva copiando
todo lo anterior: cuadrático. La distinción entre las dos formas es exactamente el contenido de esta
clase.

Y **`do:separatedBy:`** merece atención propia: es un mensaje de `Collection` que ejecuta el primer
bloque por cada elemento y el segundo **solo entre elementos**. El problema del separador —que en
COBOL, C++ y RPG exige un `if i > 1`— aquí es un método de la biblioteca. Es la misma solución que el
`~^` de Lisp y el `join` de Perl y Tcl, obtenida sin sintaxis especial: solo un método más en
`Collection` que alguien escribió una vez.

Sobre la mutabilidad en general, Smalltalk es mutable por defecto y ofrece la inmutabilidad como
propiedad del objeto: `unObjeto beReadOnlyObject` marca cualquier instancia como de solo lectura, y
cualquier intento de modificarla dispara una excepción capturable. Los literales de cadena de los
métodos compilados están marcados así en Pharo — porque, como se vio en la clase 048, son parte del
propio código.
"""),
    },
)

# ---------------------------------------------------------------------------
# 055 — Operadores y expresiones
# ---------------------------------------------------------------------------
SPECS["055"] = dict(
    gancho="""
Las cinco operaciones de la escuela: suma, resta, multiplicación, división entera y resto. Con
números positivos todos los lenguajes coinciden. Cambia el signo de uno de ellos y **dejan de
coincidir**: `-7 mod 3` vale `-1` en C, C++, Java y Go, y vale `2` en Python, Ruby y Tcl. Los dos
resultados son correctos; responden a definiciones distintas de qué es dividir.
""",
    porque="""
Aquí el concepto es **la semántica exacta de los operadores**, y estos lenguajes son los que mejor la
exponen porque **algunos ofrecen las dos definiciones a la vez y te obligan a elegir**. Ada tiene
`mod` y `rem`; Fortran tiene `modulo` y `mod`; Lisp tiene `mod` y `rem`; Smalltalk tiene `\\\\` y
`rem:`. En cada pareja, la primera sigue el signo del divisor y la segunda el del dividendo.

Y COBOL enseña algo distinto: **no tiene operador de resto**. Tiene una cláusula del verbo
`DIVIDE`, lo que obliga a escribir la división y el resto en la misma sentencia — que es, de hecho,
lo que hace el procesador.
""",
    cierre="""
Dos cosas que conviene comprobar de cualquier lenguaje nuevo, y que esta clase enseña a preguntar.
**Primera: qué hace el resto con negativos.** Si el lenguaje tiene un solo operador, busca en su
manual si sigue el signo del dividendo (truncada) o del divisor (suelo). **Segunda: qué pasa al
dividir por cero.** Excepción en Ada, Pascal, Lisp, Smalltalk y Perl; comportamiento **indefinido**
en C y C++ para enteros; `Inf` o `NaN` en punto flotante IEEE. Tres respuestas distintas al mismo
error, y solo una de ellas es silenciosa.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. OPERADORES.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TXT-A   PIC X(20).
01  TXT-B   PIC X(20).
01  A       PIC S9(9)  COMP-3.
01  B       PIC S9(9)  COMP-3.
01  SUMA    PIC S9(18) COMP-3.
01  RESTA   PIC S9(18) COMP-3.
01  MULT    PIC S9(18) COMP-3.
01  DIVI    PIC S9(18) COMP-3.
01  RESTO   PIC S9(18) COMP-3.
01  ED-S    PIC -(17)9.
01  ED-R    PIC -(17)9.
01  ED-M    PIC -(17)9.
01  ED-D    PIC -(17)9.
01  ED-MO   PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    COMPUTE SUMA  = A + B
    COMPUTE RESTA = A - B
    COMPUTE MULT  = A * B
    DIVIDE A BY B GIVING DIVI REMAINDER RESTO

    MOVE SUMA  TO ED-S
    MOVE RESTA TO ED-R
    MOVE MULT  TO ED-M
    MOVE DIVI  TO ED-D
    MOVE RESTO TO ED-MO
    DISPLAY "suma=" FUNCTION TRIM(ED-S)
            " resta=" FUNCTION TRIM(ED-R)
            " mult=" FUNCTION TRIM(ED-M)
            " div=" FUNCTION TRIM(ED-D)
            " mod=" FUNCTION TRIM(ED-MO)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** **COBOL no tiene operador de resto.** Ni `%`, ni `mod`. Lo que
tiene es una **cláusula del verbo `DIVIDE`**:

```cobol
DIVIDE A BY B GIVING DIVI REMAINDER RESTO
```

Una sola sentencia produce el cociente **y** el resto. Y eso no es una limitación: es lo que hace de
verdad el procesador, que en una única instrucción de división devuelve las dos cosas. En C hay que
escribir `a / b` y `a % b` por separado y confiar en que el compilador reconozca el patrón y no
divida dos veces —cosa que hace, pero es una optimización, no una garantía—.

Ese detalle explica también por qué la biblioteca de C tiene `div()` y `ldiv()`, que devuelven una
estructura con cociente y resto: alguien se dio cuenta del mismo problema.

Y esta clase deja ver la otra herencia de COBOL: **los verbos aritméticos** anteriores a `COMPUTE`,
que siguen siendo válidos y aparecen en todo el código antiguo:

```cobol
ADD IVA TO TOTAL
SUBTRACT DESCUENTO FROM PRECIO GIVING NETO
MULTIPLY CANTIDAD BY PRECIO GIVING IMPORTE ROUNDED
```

Se leen en voz alta como una instrucción a un administrativo, que era exactamente el objetivo de 1959.
`COMPUTE` llegó después para escribir expresiones completas, y hoy es lo que se usa — pero conocer los
verbos es imprescindible para leer los millones de líneas escritas antes.
"""),
        "fortran": ("""
program operadores
   implicit none
   integer :: a, b

   read(*, *) a, b

   write(*, '(A,I0,A,I0,A,I0,A,I0,A,I0)') &
      'suma=', a + b, ' resta=', a - b, ' mult=', a * b, &
      ' div=', a / b, ' mod=', mod(a, b)
end program operadores
""", """
**Lo que esta clase enseña en Fortran.** Fortran tiene **dos funciones de resto**, y la diferencia
solo se ve con negativos:

```fortran
mod(-7, 3)      ! -1  -- sigue el signo del DIVIDENDO (división truncada)
modulo(-7, 3)   !  2  -- sigue el signo del DIVISOR   (división al suelo)
```

`mod` es la de C, C++ y Java; `modulo` es la de Python, Ruby y las matemáticas. Tener las dos con
nombres distintos evita la discusión: eliges la que necesitas y queda escrito cuál era.

Para índices cíclicos —"el siguiente de la lista, dando la vuelta"— la correcta es casi siempre
`modulo`, porque nunca devuelve negativos. Usar `mod` ahí produce un índice fuera de rango cuando el
valor es negativo, y es un error clásico.

Y Fortran tiene un operador que ningún otro lenguaje de esta página ofrece con sintaxis propia:
**`**` para la potencia**.

```fortran
2 ** 10        ! 1024
x ** 0.5       ! raíz cuadrada
matriz ** 2    ! ojo: elemento a elemento, NO producto matricial
```

En C y en Java hay que llamar a `pow()`. En Fortran es un operador con su precedencia —la más alta— y
además está **asociado a la derecha**, como en matemáticas: `2 ** 3 ** 2` es `2 ** 9`, no `8 ** 2`.
Python y Ada tomaron el mismo operador; C nunca lo tuvo.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Operadores is
   A, B : Integer;
begin
   Get (A);
   Get (B);

   Put ("suma=");   Put (A + B,   Width => 1);
   Put (" resta="); Put (A - B,   Width => 1);
   Put (" mult=");  Put (A * B,   Width => 1);
   Put (" div=");   Put (A / B,   Width => 1);
   Put (" mod=");   Put (A rem B, Width => 1);
   New_Line;
end Operadores;
""", """
**Lo que esta clase enseña en Ada.** Ada tiene **`mod` y `rem` como dos operadores distintos**, y
—esto es lo importante— la elección está ligada a la definición de la división:

```ada
 7 rem  3  =  1     -7 rem  3  = -1     --  rem acompaña a "/", que TRUNCA
 7 mod  3  =  1     -7 mod  3  =  2     --  mod sigue el signo del DIVISOR
```

`A / B` en Ada trunca hacia cero, y `rem` es su resto coherente: se cumple siempre
`A = (A / B) * B + (A rem B)`. `mod` corresponde a la división al suelo. Que el lenguaje tenga las
dos con nombres distintos y documente la identidad que cumple cada una es exactamente el nivel de
precisión que se espera de un lenguaje para sistemas críticos.

Y hay dos cosas más de esta clase que Ada hace de forma característica.

La primera: **`**` solo acepta exponente entero no negativo** para operandos enteros. `2 ** (-1)`
levanta `Constraint_Error` en lugar de devolver 0 silenciosamente, porque el resultado no es
representable como entero.

La segunda: **dividir por cero levanta `Constraint_Error`**, siempre, sin excepción. En C y C++ la
división entera por cero es **comportamiento indefinido** —el compilador puede asumir que no ocurre y
optimizar en consecuencia—, lo que significa que el programa puede hacer cualquier cosa. En Ada es un
suceso previsto, con nombre, capturable y sin coste cuando el compilador puede demostrar que no pasa.
"""),
        "pascal": ("""
program Operadores;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  A, B: Integer;

begin
  Read(A, B);

  WriteLn('suma=', IntToStr(A + B),
          ' resta=', IntToStr(A - B),
          ' mult=', IntToStr(A * B),
          ' div=', IntToStr(A div B),
          ' mod=', IntToStr(A mod B));
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal separa **dos operadores de división** con nombres
distintos, y es una de sus mejores decisiones:

```pascal
7 div 2     { 3    -- división ENTERA; solo acepta enteros }
7 / 2       { 3.5  -- división REAL; SIEMPRE da un Real }
```

`/` en Pascal **nunca** da un entero, ni aunque los dos operandos lo sean. `X := 7 / 2` con `X`
entero **no compila**. Compara con C, Java, Go y Rust, donde `7 / 2` da `3` porque los operandos son
enteros y hay que recordarlo: es el mismo símbolo con dos significados según los tipos, y la causa de
un error clásico que Pascal hace imposible.

Sobre el resto: `mod` en Pascal sigue el signo del **dividendo**, como el `%` de C. `-7 mod 3` da
`-1`. Free Pascal no ofrece la variante al suelo, así que hay que escribirla —`((a mod b) + b) mod b`—
si se necesita para índices cíclicos.

Y esta clase es donde reaparece la trampa de precedencia de la clase 046, ahora con `div` y `mod`:
**tienen la misma precedencia que `*` y `/`**, que es lo esperable, pero **`and` también**, y `or`
está al nivel de `+`. Por eso los paréntesis en `(a > 0) and (b > 0)` no son opcionales. Es una
consecuencia de haber unificado los operadores lógicos con los de bits en 1970, y el lenguaje la
arrastra desde entonces.
"""),
        "lisp": ("""
(let* ((a (read))
       (b (read)))
  (format t "suma=~D resta=~D mult=~D div=~D mod=~D~%"
          (+ a b) (- a b) (* a b) (truncate a b) (rem a b)))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp es el lenguaje de esta página con la aritmética más
cuidadosa, y esta clase deja ver por qué. Para dividir enteros hay **cuatro funciones**, una por cada
forma de redondear el cociente, y **cada una devuelve el cociente y el resto**:

| Función | Cociente | Resto asociado |
|---|---|---|
| `truncate` | Hacia cero | `rem` |
| `floor` | Hacia abajo | `mod` |
| `ceiling` | Hacia arriba | — |
| `round` | Al más cercano (bancario) | — |

```lisp
(truncate -7 3)   ; => -2 y -1     (rem -7 3) => -1
(floor    -7 3)   ; => -3 y  2     (mod -7 3) =>  2
```

La correspondencia está garantizada por el estándar: `rem` acompaña a `truncate` y `mod` a `floor`.
Ninguna ambigüedad, ninguna nota al pie.

Y **`/` en Lisp no es ninguna de las cuatro**: da el resultado **exacto**. `(/ 7 2)` devuelve la
fracción `7/2`, no `3` ni `3.5`. Para obtener un entero hay que decir **cuál** de los cuatro
redondeos quieres, y para obtener un real hay que pedirlo con `(/ 7.0 2)`.

Es la postura más coherente de toda la página: si la división de dos enteros no es un entero, el
lenguaje no elige por ti. La contrapartida es que `(/ 1 3)` produce un objeto `ratio` y no el
`0.333` que muchos esperan — que es, en realidad, la respuesta correcta.
"""),
        "tcl": ("""
gets stdin linea
lassign [split [string trim $linea]] a b

puts "suma=[expr {$a + $b}] resta=[expr {$a - $b}] mult=[expr {$a * $b}]\\
 div=[expr {$a / $b}] mod=[expr {$a % $b}]"
""", """
**Lo que esta clase enseña en Tcl.** Toda la aritmética vive **dentro de `expr`**, porque fuera de él
no hay operadores: hay comandos. `expr` es un mini-lenguaje empotrado con su propia gramática y su
propia tabla de precedencias, tomada de C.

Y Tcl tomó una decisión que lo separa de C: **`%` sigue el signo del divisor**, como Python.

```tcl
expr {-7 % 3}       ;# 2   -- en C sería -1
expr {-7 / 3}       ;# -3  -- división AL SUELO, no truncada
```

Es coherente —el cociente y el resto van a juego— y es lo contrario de lo que espera quien viene de
C. Está documentado, y es exactamente el tipo de detalle que hay que comprobar al portar un algoritmo.

Esta clase también recuerda **por qué `expr` va siempre entre llaves**. Sin ellas, Tcl sustituye las
variables antes de que `expr` vea la expresión, y entonces el contenido de una variable se
**reinterpreta como código**:

```tcl
set b "1; exec rm -rf /"
expr $a / $b        ;# sustitución antes de evaluar: agujero de inyección
expr {$a / $b}      ;# correcto: expr recibe los NOMBRES y los resuelve él
```

Es la misma clase de vulnerabilidad que la inyección SQL, con el mismo remedio: **no construyas la
expresión concatenando texto**. Y además, con llaves `expr` compila la expresión una sola vez a
bytecode; sin ellas, la reanaliza en cada vuelta del bucle.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($x, $y) = split ' ', $linea;

printf "suma=%d resta=%d mult=%d div=%d mod=%d\\n",
       $x + $y, $x - $y, $x * $y, int($x / $y), $x % $y;
""", """
**Lo que esta clase enseña en Perl.** **`/` en Perl siempre es división real.** `7 / 2` da `3.5`, no
`3`, porque no hay tipo entero que fuerce la división entera. Por eso el programa usa `int($x / $y)`
para obtener el cociente entero — la división entera de Perl es una división real más un truncado.

Y `%` tiene una particularidad que sorprende: **convierte los operandos a entero primero y sigue el
signo del divisor**, como Python.

```perl
print  7 % 3;      # 1
print -7 % 3;      # 2     -- en C sería -1
print  7 % -3;     # -2
print 7.9 % 3;     # 1     -- 7.9 se trunca a 7 ANTES de operar
```

Ese último caso es el que muerde: `%` no es una operación sobre reales, así que descarta los
decimales sin avisar. Con `use integer` activado en el ámbito, el comportamiento cambia al de C.

Perl tiene además dos operadores que casi ningún lenguaje de esta página ofrece:

```perl
2 ** 10        # 1024 -- potencia, asociativa a la derecha
'-' x 40       # repetición de cadena (clase 051)
10 <=> 3       # 1  -- comparación de TRES vías: -1, 0 o 1
'a' cmp 'b'    # -1 -- lo mismo para cadenas
```

`<=>` —la "nave espacial"— devuelve el orden en un solo valor y es lo que se pasa a `sort`. C++20 la
adoptó veinte años después con el mismo símbolo y el nombre de *operador de comparación de tres vías*.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::cout << "suma=" << (a + b)
              << " resta=" << (a - b)
              << " mult=" << (a * b)
              << " div=" << (a / b)
              << " mod=" << (a % b) << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** `/` entre enteros **trunca hacia cero** y `%` sigue el signo del
**dividendo**, comportamiento que quedó garantizado en C++11 y C99 —antes de eso el estándar lo
dejaba a criterio de la implementación, y había compiladores que hacían lo contrario—.

```cpp
-7 / 3      // -2
-7 % 3      // -1
```

Pero lo que esta clase debe subrayar de C++ es otra cosa, y es seria: **la división entera por cero
es comportamiento indefinido**, no una excepción. No es que dé un valor raro: es que el compilador
tiene derecho a asumir que nunca ocurre y **eliminar el código que la rodea**.

```cpp
int f(int a, int b) {
    int r = a / b;        // el compilador deduce: b != 0
    if (b == 0) return -1;// ...y puede BORRAR esta comprobación por inalcanzable
    return r;
}
```

Ese razonamiento es legal y los compiladores lo aplican. La comprobación tiene que ir **antes** de la
división, siempre. Es la diferencia con Ada, donde es `Constraint_Error`, y con Perl o Pascal, donde
es una excepción.

Y hay un segundo caso indefinido que conviene conocer: `INT_MIN / -1` desborda, porque el resultado no
cabe en un `int`. Los dos casos se detectan con `-fsanitize=undefined` en desarrollo.

C++20 añadió `std::div` y, sobre todo, el **operador de tres vías `<=>`**, que genera automáticamente
los seis comparadores a partir de una sola definición.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi OPERAD;
  a int(10) const;
  b int(10) const;
end-pi;

dcl-s salida char(100);

salida = 'suma='   + %char(a + b)
       + ' resta=' + %char(a - b)
       + ' mult='  + %char(a * b)
       + ' div='   + %char(%div(a : b))
       + ' mod='   + %char(%rem(a : b));
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** Aquí está la trampa más peligrosa de RPG para quien llega de
otro lenguaje, y ya se apuntó en las clases 044 y 049: **el operador `/` redondea, no trunca.**

```rpgle
dcl-s r int(10);
r = 7 / 2;            // 4  -- ¡redondea!  En C, Java y Go sería 3
r = %div(7 : 2);      // 3  -- división entera de verdad
```

RPG define el resultado de `/` según los decimales del **destino**, aplicando redondeo comercial. Con
un destino entero, `7 / 2` da 4. Es aritmética de contable, coherente con un lenguaje de facturación,
y produce errores silenciosos en cualquier algoritmo portado de otro sitio.

Por eso existen **`%div` y `%rem`**, que son la división entera y el resto de verdad, con la
semántica de C —truncan hacia cero, el resto sigue el signo del dividendo—.

Y hay una operación que RPG tiene y casi nadie más: **`%rem` funciona sobre decimales empaquetados**,
no solo sobre enteros. `%rem(10.5 : 3)` es legal. En un lenguaje donde el tipo natural es el decimal
exacto, eso tiene sentido; en C ni siquiera se plantea, porque `%` sobre `double` no compila y hay que
llamar a `fmod`.
"""),
        "pli": ("""
 operadores: procedure options(main);

    declare (a, b) fixed binary(31);

    get list (a, b);

    put skip list ('suma='   || trim(char(a + b))            ||
                   ' resta=' || trim(char(a - b))            ||
                   ' mult='  || trim(char(a * b))            ||
                   ' div='   || trim(char(divide(a, b, 31))) ||
                   ' mod='   || trim(char(mod(a, b))));

 end operadores;
""", """
**Lo que esta clase enseña en PL/I.** `divide(a, b, 31)` en lugar de `a / b`, y ese tercer argumento
es toda la lección: **en PL/I hay que declarar la precisión del resultado de una división**.

La razón vuelve a la matriz base × escala de la clase 043. Al dividir dos `fixed decimal`, ¿cuántos
dígitos y cuántos decimales tiene el resultado? El estándar define una regla, y esa regla suele
producir un resultado con **muchos** decimales que luego se trunca al asignarlo. `divide(a, b, p, q)`
permite decirlo explícitamente: `p` dígitos totales, `q` decimales.

```pli
x = divide(10, 3, 15, 2);     /* 3.33, controlado */
x = 10 / 3;                   /* la regla del estándar decide, y sorprende */
```

Es verboso y es exacto, y es una de las pocas construcciones de PL/I que hoy se echa de menos: en la
mayoría de los lenguajes, el resultado de dividir dos decimales es una sorpresa que se descubre
probando.

Y `mod(a, b)` en PL/I sigue el signo del **divisor**, como Python y Tcl, mientras que la división
trunca — así que **`mod` y `/` no son coherentes entre sí**, al contrario que en Ada. Es un detalle
menor y muy propio del lenguaje: cada pieza es defendible por separado y el conjunto exige leer el
manual.
"""),
        "mumps": ("""
OPERAD ; Operadores -- clase 055
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 write "suma=", a + b
 write " resta=", a - b
 write " mult=", a * b
 write " div=", a\\b
 write " mod=", a#b, !
 quit
""", """
**Lo que esta clase enseña en M.** La tabla de operadores de M es la más compacta de esta página, y
la que más se aparta de la convención:

| M | Significado | En casi todos los demás |
|---|---|---|
| `+` `-` `*` | Suma, resta, producto | Igual |
| `/` | División **real** | Igual que Perl |
| `\\` | División **entera** | `//`, `div`, `%div` |
| `#` | **Módulo** | `%`, `mod` |
| `**` | Potencia | `**`, `pow()` |
| `_` | **Concatenación** | `+`, `.`, `&`, `\\|\\|` |
| `!` | **O lógico** | `\\|\\|` |
| `&` | Y lógico | `&&` |
| `'` | **Negación** | `!` |

Tres de ellos están asignados a símbolos que en otros lenguajes significan cosas distintas —`!` es
*or*, `'` es *not*, `\\` es división entera— y esa es la razón principal de que leer M sin conocerlo
sea imposible aunque se sepa programar.

Y hay una regla que sorprende a todo el mundo: **M no tiene precedencia de operadores**. Todas las
expresiones se evalúan **estrictamente de izquierda a derecha**.

```mumps
write 2 + 3 * 4       ; 20, no 14 -- se hace (2+3)*4
write 2 + (3 * 4)     ; 14 -- con paréntesis, lo esperado
```

Es la misma decisión que tomó Smalltalk con sus mensajes binarios, y por un motivo parecido:
simplicidad del analizador. En un lenguaje diseñado para caber en la memoria de un PDP-7, no
implementar una tabla de precedencias era una economía real. Hoy es una trampa que obliga a
parentizar todo.
"""),
        "smalltalk": ("""
| partes a b |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

Transcript
    show: 'suma=', (a + b) printString;
    show: ' resta=', (a - b) printString;
    show: ' mult=', (a * b) printString;
    show: ' div=', (a // b) printString;
    show: ' mod=', (a \\\\ b) printString;
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Los operadores **no existen**: `+`, `-`, `*`, `//` y `\\\\`
son **mensajes binarios** enviados al número de la izquierda. Están implementados en `Number` y sus
subclases, y se pueden leer en el navegador. Definir `+` en una clase propia no requiere ninguna
sintaxis de "sobrecarga de operadores": basta con implementar un método que se llame `+`.

Smalltalk tiene las dos familias de división, con nombres coherentes:

```smalltalk
7 // 2      "3   -- división AL SUELO"
7 \\\\ 2      "1   -- resto al suelo, va con //"
-7 // 2     "-4  -- al suelo, no truncado"
-7 \\\\ 2     "1   -- sigue el signo del DIVISOR"
-7 quo: 2   "-3  -- truncada, como C"
-7 rem: 2   "-1  -- resto truncado, va con quo:"
7 / 2       "7/2 -- ¡una Fraction EXACTA!, como en Lisp"
```

Fíjate en `/`: igual que en Lisp, la división de dos enteros que no dividen exactamente **produce una
fracción**, no un real aproximado ni un entero truncado.

Y la trampa de esta clase, que ya apareció en la 041: **no hay precedencia aritmética**. Los mensajes
binarios se evalúan de izquierda a derecha, así que `2 + 3 * 4` da **20**. Igual que en M, y por la
misma razón de simplicidad — aquí, además, obligada: si `*` es un mensaje como cualquier otro, no
puede tener una precedencia especial sin romper la uniformidad del lenguaje. Los paréntesis de este
programa no son estilo.
"""),
    },
)

# ---------------------------------------------------------------------------
# 056 — Entrada y salida básica
# ---------------------------------------------------------------------------
SPECS["056"] = dict(
    gancho="""
Leer una línea y devolverla. El programa más simple posible, y el que cierra la Parte 3 con la
pregunta que la atraviesa entera: **¿de dónde vienen los datos y quién decide de dónde?** Porque en
la mitad de estos lenguajes el programa **no sabe** si lee de un teclado, de un fichero o de una
cinta — y esa ignorancia deliberada es una de las mejores ideas de la informática.
""",
    porque="""
Aquí el concepto es **la abstracción del canal de entrada y salida**, y estos lenguajes lo enseñan
mejor que el núcleo por un motivo histórico: **inventaron la idea**. Fortran habla con **unidades
numeradas**, no con ficheros. COBOL declara nombres lógicos que alguien conecta fuera. M escribe al
**dispositivo actual**, sea el que sea. Y [JCL](../../../atlas/jcl.md) —que por eso aparece en esta
clase y no en otras— es literalmente el lenguaje de **conectar los nombres lógicos de un programa a
ficheros reales en el momento de ejecutar**.

Eso que hoy llamamos inyección de dependencias, configuración por entorno o volúmenes montados es
esto, y estaba resuelto en 1964.
""",
    cierre="""
La idea que cierra la Parte 3 es la **independencia del dispositivo**: un programa bien escrito no
nombra ficheros, nombra **canales**, y alguien de fuera decide qué hay al otro lado. Unix lo llamó
después *entrada estándar* y lo convirtió en cultura con las tuberías; el mainframe lo llamó *ddname*
veinte años antes. Cuando escribes un programa que lee de `stdin` en lugar de abrir `datos.txt`,
estás heredando esta decisión — y por eso todas las implementaciones de este curso pueden verificarse
con el mismo `casos.json`.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. ECO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).

PROCEDURE DIVISION.
    ACCEPT LINEA
    DISPLAY "eco: " FUNCTION TRIM(LINEA)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** `ACCEPT` y `DISPLAY` son la E/S **de conversación**: rápida de
escribir y pensada para mensajes al operador, no para datos. La E/S de verdad en COBOL es la de
ficheros, y es donde aparece la idea que importa:

```cobol
ENVIRONMENT DIVISION.
INPUT-OUTPUT SECTION.
FILE-CONTROL.
    SELECT CLIENTES ASSIGN TO ENTRADA
        ORGANIZATION IS SEQUENTIAL.

DATA DIVISION.
FILE SECTION.
FD  CLIENTES.
01  REG-CLIENTE   PIC X(200).
```

**`ASSIGN TO ENTRADA` no nombra ningún fichero.** `ENTRADA` es un **nombre lógico** —un *ddname*—, y
quién sea de verdad lo decide el [JCL](../../../atlas/jcl.md) en el momento de ejecutar. El mismo
programa, sin recompilar, lee hoy un fichero de pruebas de cien registros y mañana el de producción
de diez millones.

Eso es **independencia del dispositivo**, y en 1959 era revolucionario: el programa deja de saber
dónde están sus datos. Es la misma idea que hoy se implementa con variables de entorno, con
inyección de dependencias o montando un volumen en un contenedor.

Y `ORGANIZATION` declara la estructura —`SEQUENTIAL`, `INDEXED`, `RELATIVE`—, así que un fichero
indexado se lee por clave (`READ ... KEY IS`) con la misma sintaxis con la que se recorre uno
secuencial. COBOL tenía acceso por clave en el lenguaje décadas antes de que existieran las bases de
datos relacionales.
"""),
        "fortran": ("""
program eco
   implicit none
   character(len=200) :: linea

   read(*, '(A)') linea

   write(*, '(A,A)') 'eco: ', trim(linea)
end program eco
""", """
**Lo que esta clase enseña en Fortran.** El asterisco de `read(*, ...)` y `write(*, ...)` no significa
"la consola": significa **la unidad por defecto**. Y ahí está la idea de Fortran para esta clase — la
E/S va contra **unidades numeradas**, no contra ficheros.

```fortran
open(unit=10, file='datos.txt', status='old', action='read')
read(10, '(A)') linea
close(10)

write(6, *) 'a la salida estándar'    ! 6 y 5 son las unidades históricas
```

Un número entero identifica un canal abierto. Cambiar de dónde lee un procedimiento es pasarle otro
número, sin tocar su código:

```fortran
subroutine procesar(unidad)
   integer, intent(in) :: unidad
   read(unidad, '(A)') linea      ! le da igual si es un fichero o el teclado
end subroutine
```

Es exactamente la misma abstracción que el *ddname* de COBOL y el descriptor de fichero de Unix,
expresada como un número que se pasa por parámetro. Fortran moderno añadió `newunit=` para que el
sistema asigne un número libre y no haya colisiones —el problema clásico de los números fijos—, y las
constantes con nombre `input_unit`, `output_unit` y `error_unit` en `iso_fortran_env`.

Y `read(*, '(A)')` con formato `A` lee la línea **tal cual**; con formato `*` —lista— la interpretaría
buscando valores separados, que es lo que hacen el resto de programas de este curso.
"""),
        "ada": ("""
with Ada.Text_IO; use Ada.Text_IO;

procedure Eco is
   Linea  : String (1 .. 200);
   Ultimo : Natural;
begin
   Get_Line (Linea, Ultimo);

   Put_Line ("eco: " & Linea (1 .. Ultimo));
end Eco;
""", """
**Lo que esta clase enseña en Ada.** `Ada.Text_IO` opera sobre un **fichero actual** implícito, y las
versiones sin argumento de `Get_Line` y `Put_Line` lo usan. Cambiar el destino de un programa entero
es una línea:

```ada
Set_Output (Mi_Fichero);      --  a partir de aquí, todo Put_Line va ahí
Put_Line ("esto va al fichero");
Set_Output (Standard_Output); --  y de vuelta
```

Es el mismo mecanismo que el dispositivo actual de M y que la redirección del shell, dentro del
lenguaje.

Lo que Ada aporta de propio es que **la E/S está fuertemente tipada y es genérica**. No hay un `Put`
que sirva para todo: hay un paquete por tipo, y los de los tipos numéricos son **instancias de un
genérico**:

```ada
package Ada.Integer_Text_IO is new Ada.Text_IO.Integer_IO (Integer);
package Mi_IO is new Ada.Text_IO.Integer_IO (Mi_Tipo_Entero);   --  para TU tipo
```

Por eso los programas de este curso importan `Ada.Integer_Text_IO` y `Ada.Long_Float_Text_IO` por
separado. Es más verboso que un `print` universal y a cambio **la lectura valida el tipo**: leer un
`Descuento_T` con rango `0.0 .. 1.0` —como en la clase 041— rechaza un 1.5 en el propio `Get`, sin
ninguna comprobación escrita.

Y `Get_Line` devuelve la longitud en `Ultimo` porque `String` es de tamaño fijo, como se vio en la
clase 048.
"""),
        "pascal": ("""
program Eco;
{$MODE OBJFPC}{$H+}

var
  Linea: string;

begin
  ReadLn(Linea);

  WriteLn('eco: ', Linea);
end.
""", """
**Lo que esta clase enseña en Pascal.** `Read`, `ReadLn`, `Write` y `WriteLn` no son funciones
normales: son **construcciones del compilador**. Aceptan cualquier número de argumentos, de tipos
distintos, y con los especificadores `:ancho:decimales` que se vieron en la clase 041. Ninguna función
de Pascal escrita por un usuario puede hacer eso.

Esa es una decisión de diseño interesante: Wirth prefirió **incorporar la E/S al lenguaje** en vez de
darle a los usuarios variadicidad y polimorfismo. Es coherente con su idea de mantener el lenguaje
pequeño, y es la razón de que Pascal no tenga sobrecarga de funciones en su forma original.

El fichero es un **tipo del lenguaje**, no un objeto de biblioteca:

```pascal
var
  F: TextFile;              { fichero de texto }
  D: file of TRegistro;     { fichero TIPADO: registros de TRegistro }
begin
  AssignFile(F, 'datos.txt');
  Reset(F);                 { abrir para leer }
  ReadLn(F, Linea);         { la misma ReadLn, con el fichero delante }
  CloseFile(F);
```

`file of TRegistro` es un fichero **con tipo**: cada `Read` devuelve un registro completo, y el
compilador conoce su tamaño. Es el equivalente del `FD` de COBOL, y no existe en C ni en Java, donde
un fichero es una secuencia de bytes y la estructura la pone el programador.

Y `ReadLn(F, X)` es la misma `ReadLn` con un argumento más: el canal por defecto es `Input` y se puede
sustituir. La misma idea que `Set_Output` en Ada.
"""),
        "lisp": ("""
(let ((linea (read-line)))
  (format t "eco: ~A~%" linea))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp tiene **flujos** (*streams*) como objetos de primera
clase, y las funciones de E/S aceptan uno como argumento opcional. Sin él usan `*standard-input*` y
`*standard-output*`, que son **variables especiales** — y ahí está lo interesante.

Al ser variables, se pueden **reenlazar dinámicamente** para un fragmento de código:

```lisp
(with-open-file (f "salida.txt" :direction :output)
  (let ((*standard-output* f))
    (imprimir-informe)))     ; TODO lo que imprima esta función va al fichero
```

`imprimir-informe` no sabe nada de ficheros: escribe con `format t`, y el `t` significa
"`*standard-output*`". Al reenlazar la variable, **todo el árbol de llamadas** cambia de destino sin
que ninguna función lo sepa. Es la redirección del shell, dentro del lenguaje y con ámbito dinámico.

Ese mismo mecanismo da uno de los idiomas más útiles de Lisp:

```lisp
(with-output-to-string (s)
  (dotimes (i 5) (format s "~D-" i)))    ; => "0-1-2-3-4-"
```

Capturar en una cadena la salida de un código que cree estar imprimiendo. Es el `StringBuilder` de la
clase 054 y a la vez la forma de probar código que imprime, sin tocarlo.

Y `read-line` devuelve además **un segundo valor** que indica si la línea terminó por fin de fichero
en vez de por salto de línea — otra vez el patrón de los valores múltiples.
"""),
        "tcl": ("""
gets stdin linea

puts "eco: $linea"
""", """
**Lo que esta clase enseña en Tcl.** `stdin`, `stdout` y `stderr` son **canales**, y un canal es
simplemente una cadena que identifica un flujo abierto. `open` devuelve otra, y todos los comandos de
E/S aceptan cualquiera:

```tcl
set canal [open "datos.txt" r]
gets $canal linea
close $canal

set canal [open "|comando externo" r]     ;# una TUBERÍA, con el mismo comando
set canal [socket www.ejemplo.com 80]     ;# un SOCKET, con el mismo comando
```

Ficheros, tuberías y sockets son **el mismo tipo de cosa** y se manejan con `gets`, `puts`, `read`,
`flush` y `close` sin distinción. Es la abstracción de Unix llevada al lenguaje de guion, y explica
por qué Tcl fue durante años tan popular para automatizar sistemas.

Y `fconfigure` es donde se ajusta todo lo que en otros lenguajes exige clases distintas:

```tcl
fconfigure $canal -translation binary    ;# sin traducir saltos de línea
fconfigure $canal -encoding utf-8        ;# codificación del canal
fconfigure $canal -blocking 0            ;# lectura no bloqueante
```

Ese último es el que importa: con `-blocking 0` más `fileevent`, Tcl hace **E/S asíncrona dirigida
por eventos** — un bucle de eventos con retrollamadas, en 1990. Es el modelo que Node.js popularizó
quince años después, disponible aquí desde el principio y por la misma razón: un lenguaje de guion
que tiene que atender varias cosas a la vez sin hilos.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

print "eco: $linea\\n";
""", """
**Lo que esta clase enseña en Perl.** `<STDIN>` es el **operador de diamante** aplicado a un manejador
de fichero, y su comportamiento depende del contexto: en contexto escalar da una línea, en contexto de
lista da todas. Es la misma dualidad de la clase 041.

Pero lo que hay que llevarse de Perl en esta clase es `<>` **a secas**, el diamante mágico:

```perl
while (my $linea = <>) {
    print "eco: $linea";
}
```

`<>` lee de **los ficheros nombrados en la línea de comandos**, uno tras otro, y si no hay ninguno lee
de la entrada estándar. Con esas cinco líneas el programa se comporta exactamente como `cat`, `grep`
o `sort`: `programa.pl a.txt b.txt` o `cat a.txt | programa.pl` funcionan igual, sin escribir una sola
línea de gestión de argumentos.

Ese comportamiento es **la convención de las herramientas de Unix**, incorporada al lenguaje. Es la
razón de que Perl desplazara a `awk` y `sed` en los 90: escribir un filtro correcto costaba una línea.

Y las opciones de línea de comandos llevan la idea al extremo:

```bash
perl -ne 'print if /ERROR/' registro.log       # -n envuelve en el bucle <>
perl -pe 's/viejo/nuevo/' fichero              # -p además imprime cada línea
perl -i.bak -pe 's/a/b/g' *.conf               # -i edita EN EL SITIO con copia
```

`-n` y `-p` generan el bucle de lectura por ti. Es E/S como parte de la invocación del programa, no
del programa.
"""),
        "cpp": ("""
#include <iostream>
#include <string>

int main() {
    std::string linea;
    if (!std::getline(std::cin, linea)) return 1;

    std::cout << "eco: " << linea << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** `std::cin` y `std::cout` son **flujos**, y `>>` y `<<` son
operadores sobrecargados sobre ellos. Que la E/S se escriba con los operadores de desplazamiento de
bits fue una decisión discutida en su día y hoy es la marca de la casa.

La ventaja real es la **seguridad de tipos**: `std::cout << x` elige la sobrecarga correcta según el
tipo de `x`, mientras que `printf("%d", x)` con `x` de otro tipo compila y lee la pila mal. Y funciona
con tipos propios sin tocar nada del sistema:

```cpp
std::ostream& operator<<(std::ostream& os, const Punto& p) {
    return os << '(' << p.x << ", " << p.y << ')';
}
std::cout << mi_punto << '\\n';     // ya funciona
```

Y como todos los flujos comparten interfaz, una función que reciba `std::ostream&` escribe
indistintamente en la consola, en un fichero (`std::ofstream`) o en una cadena
(`std::ostringstream`) — que es el `with-output-to-string` de Lisp y la clave para poder **probar**
código que imprime.

Dos avisos prácticos de esta clase. Primero: `std::getline` lee la línea entera **incluidos los
espacios**, mientras que `std::cin >> s` se detiene en el primer espacio; mezclarlos deja el salto de
línea pendiente en el búfer y produce una lectura vacía inesperada. Segundo: para E/S masiva,
`std::ios::sync_with_stdio(false)` desactiva la sincronización con `printf` y multiplica la velocidad
— el detalle que todo el mundo descubre en su primer problema de programación competitiva.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi ECO;
  linea varchar(200) const;
end-pi;

dcl-s salida char(220);

salida = 'eco: ' + %trim(linea);
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** `dsply` es el equivalente de `ACCEPT`/`DISPLAY` de COBOL: una
línea de conversación, útil para depurar y nada más. La E/S real de RPG es la que define la
plataforma, y tiene tres formas que conviene distinguir:

```rpgle
dcl-f CLIENTES  usage(*input);              // fichero de base de datos
dcl-f PANTALLA  workstn;                    // fichero de PANTALLA (display file)
dcl-f INFORME   printer oflind(*in90);      // fichero de IMPRESORA
```

Las tres se declaran igual y se leen y escriben con los mismos verbos —`read`, `chain`, `write`,
`exfmt`—. Un fichero de pantalla se describe **fuera del programa**, en DDS o en un diseñador visual,
y `exfmt` (*execute format*) escribe la pantalla y lee la respuesta del usuario en una sola operación.

Ese es el rasgo distintivo: **en IBM i la pantalla es un fichero**. La misma abstracción que COBOL
aplica a las cintas y Unix a los dispositivos, llevada a la interfaz de usuario. Un programa RPG no
"pinta" una pantalla: escribe un registro en un fichero que resulta ser un terminal.

Y el fichero de base de datos aparece como **variables del programa**: al declarar `dcl-f CLIENTES`,
los campos de la tabla son nombres directamente utilizables. Sin ORM, sin mapeo y sin serialización —
la distancia entre el registro en disco y la variable en memoria es cero, como en
[M](../../../atlas/mumps.md).
"""),
        "jcl": ("""
//ECO      JOB (CONTAB),'ECO DE UNA LINEA',CLASS=A,MSGCLASS=X,
//             NOTIFY=&SYSUID
//*
//* El programa COBOL de esta clase lee de SYSIN y escribe en SYSOUT.
//* NO SABE que hay al otro lado: lo decide este JCL, al ejecutar.
//*
//EJECUTA  EXEC PGM=ECO
//STEPLIB  DD DSN=VLAD.LOADLIB,DISP=SHR
//SYSOUT   DD SYSOUT=*
//SYSIN    DD *
hola
/*
//
""", """
**Lo que esta clase enseña en JCL.** Esta es la clase para la que JCL existe, y por eso aparece aquí
y no en las anteriores.

El programa COBOL de más arriba dice `ACCEPT` y `DISPLAY`, o —en un programa de verdad— declara
`SELECT ENTRADA ASSIGN TO SYSIN`. **En ningún sitio nombra un fichero.** Las sentencias `DD` de este
JCL son las que conectan esos nombres lógicos con algo real, **en el momento de ejecutar**:

```text
//SYSIN    DD *                                   <- los datos van aquí mismo
//SYSIN    DD DSN=VLAD.PRUEBAS.PEQUENO,DISP=SHR   <- un fichero de pruebas
//SYSIN    DD DSN=PROD.CLIENTES.DIARIO,DISP=SHR   <- diez millones de registros
//SYSIN    DD DUMMY                               <- nada, fichero vacío
```

**Cuatro orígenes distintos, cero cambios en el programa y cero recompilaciones.** Ese es el concepto
completo de esta clase, y está resuelto desde 1964.

Es exactamente lo que hoy se consigue con una variable de entorno, con un volumen montado en un
contenedor o con inyección de dependencias, y el vocabulario ha cambiado más que la idea. Cuando el
manifiesto de los doce factores dice *"guarda la configuración en el entorno"*, está redescubriendo
la sentencia `DD`.

`DD SYSOUT=*` envía la salida al *spool*, de donde se recoge después; `DD DUMMY` conecta el nombre a
la nada, que es el `/dev/null` del mainframe. Y `//SYSIN DD *` con los datos en línea es lo que hace
que este trabajo sea autocontenido — el equivalente exacto del *here-document* de un shell.
"""),
        "pli": ("""
 eco: procedure options(main);

    declare linea character(200) varying;

    on endfile(sysin) stop;

    get edit (linea) (a(200));

    put skip list ('eco: ' || trim(linea));

 end eco;
""", """
**Lo que esta clase enseña en PL/I.** PL/I distingue **tres modos de E/S**, y tener los tres con
sintaxis propia es muy característico del lenguaje:

| Modo | Sintaxis | Para qué |
|---|---|---|
| **Dirigida por lista** | `get list (a, b);` | Valores separados; lo más cómodo |
| **Dirigida por edición** | `get edit (x) (a(20));` | Posiciones y formatos exactos |
| **Dirigida por datos** | `get data;` | El **dato trae su propio nombre** |

La tercera es la que no tiene equivalente. Con `get data`, la entrada es `A=5, B=7;` y PL/I **asigna
a las variables `A` y `B` del programa por su nombre**. Es autodescriptiva: el fichero de entrada
lleva las claves, como un JSON o un `.ini`, en 1964. Y `put data;` hace lo inverso, volcando el valor
de las variables con su nombre — que es exactamente lo que se necesita para depurar.

Y `on endfile(sysin) stop;` es el manejo del fin de fichero mediante el mecanismo `ON` de la clase
041: se **instala** un manejador y queda activo, en vez de comprobar el resultado de cada lectura.
Comparado con el `if (!getline(...))` de C++ o el `while (my $l = <>)` de Perl, es un modelo
distinto: **el fin de fichero es una condición, no un valor de retorno**.

Ese enfoque —condiciones instaladas en lugar de códigos comprobados— es el antepasado directo de las
excepciones, y la razón de que PL/I aparezca en cualquier historia del manejo de errores.
"""),
        "mumps": ("""
ECO ; Eco de una linea -- clase 056
 read linea
 write "eco: ", linea, !
 quit
""", """
**Lo que esta clase enseña en M.** M no tiene `stdin` ni `stdout`: tiene **el dispositivo actual**.
`read` y `write` operan sobre él, sea el que sea, y `use` lo cambia:

```mumps
 open "/tmp/salida.txt":("NEW"):10       ; abrir con tiempo de espera
 use "/tmp/salida.txt"                   ; a partir de aquí, write va ahí
 write "esto va al fichero",!
 use $principal                          ; de vuelta al dispositivo original
 close "/tmp/salida.txt"
```

`$principal` es la variable del sistema que guarda el dispositivo con el que arrancó el proceso. La
idea es la misma que `Set_Output` en Ada y que reenlazar `*standard-output*` en Lisp: **el destino es
estado del proceso, no un argumento de cada escritura**.

Y `write` tiene un mini-lenguaje de control propio que conviene reconocer al leer código M:

```mumps
 write "hola",!          ; ! = nueva línea
 write "hola",#          ; # = nueva página (form feed)
 write ?20,"columna 20"  ; ?n = tabular a la columna n
 write *65               ; *n = escribe el carácter con ese código
```

`?20` para tabular a una columna concreta delata para qué se diseñó esto: **informes impresos en
terminales de ancho fijo**. Es el mismo problema que resuelven los campos editados de COBOL y los
descriptores de formato de Fortran, con una tercera sintaxis distinta — tres respuestas de la misma
época a la misma necesidad.
"""),
        "smalltalk": ("""
| linea |

linea := stdin nextLine.

Transcript show: 'eco: ', linea; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** La E/S es **un objeto más**, y por eso apenas hay sintaxis
que aprender: `stdin` responde a `nextLine`, `Transcript` responde a `show:`. Los dos son flujos, y
los flujos son colecciones que se recorren.

Lo que hace distinto a Smalltalk en esta clase es que **el concepto de "salida estándar" apenas
existe**, porque el entorno no es una terminal: es una imagen viva con ventanas. `Transcript` es la
ventana de registro del propio sistema, no un descriptor de fichero. Un programa Smalltalk típico no
imprime — **inspecciona**.

```smalltalk
unObjeto inspect.        "abre un inspector sobre el objeto, navegable"
unaColeccion explore.    "abre un explorador del árbol de referencias"
self halt.               "detiene y abre el depurador AQUÍ"
```

Esa es la diferencia cultural que esta clase deja ver. En un lenguaje de terminal, la forma de saber
qué pasa es imprimir; en Smalltalk, es **abrir el objeto y mirarlo**, con su estado real delante y la
posibilidad de modificarlo y continuar. La depuración por `printf` —que el resto de esta página da por
supuesta— es aquí el último recurso, no el primero.

Y para leer y escribir de verdad están `ReadStream`, `WriteStream` y `ReadWriteStream`, que funcionan
igual sobre un fichero, sobre un socket o sobre una colección en memoria. El mismo protocolo, el
mismo código: la abstracción de canal de esta clase, obtenida por polimorfismo en lugar de por
descriptores numerados.
"""),
    },
)
