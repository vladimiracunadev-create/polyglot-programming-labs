# -*- coding: utf-8 -*-
"""Parte 4, lote C — clases 069 a 072. Ver `vivos_parte4.py` y `gen_vivos.py`.

El código de los ocho lenguajes de la sección 🟢 se ejecuta en CI contra el
`casos.json` de la clase (`scripts/verificar_vivos.py`).
"""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 069 — Recursión y recursión de cola
# ---------------------------------------------------------------------------
SPECS["069"] = dict(
    gancho="""
Fibonacci, el ejemplo canónico de recursión. Y también el canónico de **por qué la recursión ingenua
es una mala idea**: `fib(30)` hace más de dos millones de llamadas para calcular un número que un
bucle obtiene en treinta pasos. Pero la pregunta de esta página es anterior a la eficiencia:
**¿puede este lenguaje llamarse a sí mismo?** Y en dos de ellos, la respuesta original fue *no*.
""",
    porque="""
Aquí el concepto es la **recursión y el coste de la pila**, y estos lenguajes lo enseñan porque
muestran **de dónde vino la prohibición**. En COBOL clásico el `WORKING-STORAGE` es estático: hay un
solo juego de variables por programa, así que una segunda llamada pisaría las de la primera.
**FORTRAN 77 prohibía explícitamente la recursión** por el mismo motivo. No era una omisión: era una
consecuencia de no tener pila de activación.

Enfrente, Lisp y Pascal se diseñaron **alrededor** de la recursión, y M la consigue con `new`, que
es ámbito dinámico en lugar de una pila léxica.
""",
    cierre="""
Dos ideas. La primera: **la recursión necesita almacenamiento automático**, y por eso los lenguajes
que nacieron sin pila no la tenían. Cuando veas `RECURSIVE` en COBOL, `recursive` en Fortran o PL/I,
o `LOCAL-STORAGE`, estás viendo la palabra que activa la pila.

La segunda: **la recursión de cola no es magia, es una optimización que el compilador puede hacer o
no**. Scheme la garantiza en el estándar; Common Lisp **no**; C++, Ada y Fortran la hacen si
optimizan; Python la rechaza por decisión de diseño. Escribir una función recursiva de cola no la
convierte en un bucle salvo que alguien te lo prometa por escrito.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. FIBONACCI.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC 9(4)  COMP-3.
01  I       PIC 9(4)  COMP-3.
01  A       PIC 9(18) COMP-3.
01  B       PIC 9(18) COMP-3.
01  T       PIC 9(18) COMP-3.
01  ED-F    PIC Z(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N
    MOVE 0 TO A
    MOVE 1 TO B

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        COMPUTE T = A + B
        MOVE B TO A
        MOVE T TO B
    END-PERFORM

    MOVE A TO ED-F
    DISPLAY "fib=" FUNCTION TRIM(ED-F)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** Este programa es **iterativo, y es lo correcto**, porque el
COBOL clásico **no puede recurrir**. La razón es la de la clase 042: `WORKING-STORAGE` es
**estático**. Existe un solo juego de variables por programa, creado al cargarlo. Si un programa se
llamara a sí mismo, la segunda invocación escribiría encima de las variables de la primera.

No es una limitación arbitraria: es la consecuencia directa de un modelo de memoria sin pila de
activación. Lo mismo pasaba en FORTRAN 77 y en el PL/I sin el atributo `recursive`.

**COBOL 2002 lo resolvió** con dos piezas que hay que declarar juntas:

```cobol
IDENTIFICATION DIVISION.
PROGRAM-ID. FIB RECURSIVE.          *> 1) el programa se declara recursivo

DATA DIVISION.
LOCAL-STORAGE SECTION.              *> 2) almacenamiento por INVOCACIÓN
01  TEMPORAL  PIC 9(9) COMP-3.
WORKING-STORAGE SECTION.
01  CONTADOR  PIC 9(9) COMP-3.      *> esto sigue siendo compartido
```

`LOCAL-STORAGE` se crea **al entrar y se destruye al salir**, como una variable local de C. Es
literalmente la pila que COBOL no tenía. Y la coexistencia de las dos secciones en el mismo programa
es reveladora: puedes elegir, campo a campo, qué es compartido y qué es por invocación.

Aun así, el COBOL de producción es iterativo casi siempre — y para Fibonacci, la versión iterativa de
arriba hace **30 pasos** donde la recursiva ingenua haría 2,7 millones.
"""),
        "fortran": ("""
program fibonacci
   implicit none
   integer :: n

   read(*, *) n

   write(*, '(A,I0)') 'fib=', fib(n)

contains

   recursive function fib(k) result(f)
      integer, intent(in) :: k
      integer :: f
      if (k < 2) then
         f = k
      else
         f = fib(k - 1) + fib(k - 2)
      end if
   end function fib

end program fibonacci
""", """
**Lo que esta clase enseña en Fortran.** La palabra **`recursive`** de la línea de la función no es
decorativa: **hasta Fortran 90, la recursión estaba prohibida por el estándar**.

El motivo es idéntico al de COBOL. En FORTRAN 77, las variables locales de una subrutina eran
**estáticas**: se asignaban una vez, al cargar el programa. Muchos compiladores incluso guardaban la
dirección de retorno en una posición fija dentro de la propia subrutina — así que una segunda llamada
la sobrescribía y el `RETURN` volvía al sitio equivocado.

Fortran 90 introdujo `recursive` como palabra que **activa el almacenamiento automático** para esa
función. Y `result(f)` es obligatorio en las funciones recursivas del F90/F95: sin él, el nombre de
la función designaría a la vez el resultado y la llamada recursiva, y sería ambiguo.

**Fortran 2018 invirtió la regla**: ahora los procedimientos son recursivos **por defecto** y existe
`non_recursive` para declarar lo contrario. Un lenguaje de 1957 cambiando su valor por defecto en
2018 es exactamente lo que esta sección quiere mostrar.

Y `contains` merece una nota: los procedimientos internos declarados ahí **ven las variables del
programa que los contiene**, como una clausura. Es el mecanismo de anidamiento de Pascal y de Ada,
que C nunca tuvo.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Fibonacci is

   function Fib (K : Natural) return Natural is
   begin
      if K < 2 then
         return K;
      else
         return Fib (K - 1) + Fib (K - 2);
      end if;
   end Fib;

   N : Integer;
begin
   Get (N);
   Put ("fib="); Put (Fib (N), Width => 1); New_Line;
end Fibonacci;
""", """
**Lo que esta clase enseña en Ada.** La recursión funciona sin declarar nada: Ada nació con
almacenamiento automático, porque venía de la tradición ALGOL/Pascal y no de la de FORTRAN.

Fíjate en el tipo del parámetro: **`Natural`**, no `Integer`. `Natural` es un subtipo predefinido
—`subtype Natural is Integer range 0 .. Integer'Last`— y eso significa que **llamar a `Fib (-1)`
levanta `Constraint_Error` en el punto de la llamada**, no dentro de la función.

Es una guarda que no hay que escribir. En C, en Java o en Python, la protección contra el argumento
negativo es un `if` al principio de la función que alguien tiene que recordar poner, y que se
comprueba en cada llamada aunque el llamante ya supiera que el valor era válido.

Ada tiene además la pieza que hace de esto una garantía y no solo una comprobación: los **contratos**.

```ada
function Fib (K : Natural) return Natural
  with Pre  => K <= 30,
       Post => Fib'Result >= 0;
```

Con SPARK, esas condiciones **se demuestran estáticamente**: el analizador verifica que ninguna
llamada del programa puede violar la precondición, y entonces la comprobación en ejecución se
elimina. Seguridad sin coste.

Y sobre la pila: en sistemas embebidos con memoria limitada, la recursión se **prohíbe por norma de
proyecto** —el perfil Ravenscar y las guías de aviónica lo exigen— porque el consumo de pila debe ser
analizable antes de volar. Ahí, la versión iterativa no es una optimización: es un requisito.
"""),
        "pascal": ("""
program Fibonacci;
{$MODE OBJFPC}{$H+}
uses SysUtils;

function Fib(K: Integer): Int64;
begin
  if K < 2 then
    Result := K
  else
    Result := Fib(K - 1) + Fib(K - 2);
end;

var
  N: Integer;

begin
  Read(N);
  WriteLn('fib=', IntToStr(Fib(N)));
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal se diseñó **alrededor de la recursión**: Wirth venía de
ALGOL, donde el almacenamiento automático y la pila de activación eran el modelo desde el principio.
No hay ninguna palabra que activar.

Y Pascal permite algo que ni C ni Java tienen: **procedimientos anidados dentro de procedimientos**,
que ven las variables del que los contiene.

```pascal
function Fib(K: Integer): Int64;

  function Auxiliar(A, B, Cuenta: Int64): Int64;   { anidada: ve K }
  begin
    if Cuenta = 0 then Auxiliar := A
    else Auxiliar := Auxiliar(B, A + B, Cuenta - 1);
  end;

begin
  Result := Auxiliar(0, 1, K);
end;
```

Esa `Auxiliar` es **recursiva de cola**: la llamada recursiva es lo último que hace, así que no hay
nada pendiente en el marco de pila y un compilador puede convertirla en un salto. FPC lo hace con
`-O2` en muchos casos, aunque **no está garantizado por el estándar**.

Y Pascal tiene una construcción para la recursión mutua que hoy casi nadie usa pero que fue
influyente: **`forward`**.

```pascal
function Par(N: Integer): Boolean; forward;      { se declara ahora, se define luego }
function Impar(N: Integer): Boolean;
begin ... Par(N - 1) ... end;
function Par(N: Integer): Boolean;
begin ... Impar(N - 1) ... end;
```

`forward` existe porque Pascal compila en **una sola pasada** —la razón de su velocidad, vista en la
clase 042— y necesita conocer la firma antes del uso. Es el antepasado directo de los prototipos de C.
"""),
        "lisp": ("""
(defun fib (k)
  (if (< k 2)
      k
      (+ (fib (- k 1)) (fib (- k 2)))))

(let ((n (read)))
  (format t "fib=~D~%" (fib n)))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp **nació recursivo**. La definición original de
McCarthy en 1958 no tenía bucles: `car`, `cdr`, `cons`, `cond` y la recursión eran todo el lenguaje.
Los bucles llegaron después, como conveniencia.

Y aquí hay una advertencia que sorprende a mucha gente: **el estándar de Common Lisp NO garantiza la
optimización de llamadas de cola.**

```lisp
(defun fib-cola (k &optional (a 0) (b 1))
  (if (zerop k) a (fib-cola (1- k) b (+ a b))))   ; recursiva de COLA
```

Esa función **no consume pila en SBCL** con `(optimize (debug 1))`, y **sí la consume** con
`(debug 3)`, porque en modo depuración el compilador conserva los marcos para poder mostrarlos. El
mismo código, dos comportamientos, según una declaración.

**Scheme sí lo garantiza en el estándar**, y esa es una de las diferencias de diseño más importantes
entre los dos dialectos: en Scheme se puede escribir un bucle infinito como recursión de cola y es
correcto por definición; en Common Lisp hay que confiar en el compilador o usar `loop`.

Y para Fibonacci, la solución idiomática de Lisp no es ninguna de las dos: es **memorizar**.

```lisp
(defvar *memo* (make-hash-table))
(defun fib (k)
  (or (gethash k *memo*)
      (setf (gethash k *memo*)
            (if (< k 2) k (+ (fib (- k 1)) (fib (- k 2)))))))
```

Con eso, `fib(100)` es instantáneo y exacto —los enteros no desbordan—, y la estructura recursiva se
conserva. Es la técnica que convierte el ejemplo canónico de "recursión ineficiente" en un algoritmo
lineal sin dejar de ser recursivo.
"""),
        "tcl": ("""
proc fib {k} {
    if {$k < 2} { return $k }
    return [expr {[fib [expr {$k - 1}]] + [fib [expr {$k - 2}]]}]
}

gets stdin linea
set n [string trim $linea]

puts "fib=[fib $n]"
""", """
**Lo que esta clase enseña en Tcl.** La recursión funciona, y Tcl tiene un límite explícito y
consultable que casi ningún lenguaje expone así:

```tcl
interp recursionlimit {} 1000        ;# consultar y fijar la profundidad máxima
```

Por defecto son 1000 niveles. Superarlo da un error capturable —"too many nested evaluations"— en
lugar de un desbordamiento de pila que revienta el proceso. Es una decisión típica de un lenguaje de
guion incrustado: **fallar de forma controlada dentro de una aplicación anfitriona** importa más que
apurar la pila.

Y Tcl 8.6 añadió **`tailcall`**, que es la optimización de llamada de cola **explícita**:

```tcl
proc fib-cola {k {a 0} {b 1}} {
    if {$k == 0} { return $a }
    tailcall fib-cola [expr {$k - 1}] $b [expr {$a + $b}]
}
```

`tailcall` **reemplaza el marco de pila actual** en lugar de apilar uno nuevo. Con él, la recursión de
cola es un bucle de verdad y no hay límite de profundidad.

Que sea un comando explícito en vez de una optimización automática es coherente con todo el diseño de
Tcl: **si algo cambia el comportamiento, se escribe**. Y tiene una ventaja sobre la optimización
implícita — no depende del nivel de optimización ni del compilador, así que se puede confiar en ella.

Junto a `coroutine` de la clase 066, `tailcall` forma parte del paquete de control de flujo avanzado
que Tcl añadió en 8.6, todo construido sobre la máquina de ejecución sin pila (*NRE*) que reescribió
el intérprete en 2008.
"""),
        "perl": ("""
use strict;
use warnings;

sub fib {
    my ($k) = @_;
    return $k if $k < 2;
    return fib($k - 1) + fib($k - 2);
}

my $n = <STDIN>;
chomp $n;

print "fib=", fib($n), "\\n";
""", """
**Lo que esta clase enseña en Perl.** La recursión funciona sin ceremonia, y Perl avisa si se pasa:
con `use warnings`, más de 100 niveles produce *"Deep recursion on subroutine"*. Es un aviso, no un
error, y se puede silenciar — pero por defecto te dice que algo puede estar mal.

Perl tiene además una forma **explícita** de llamada de cola, con una sintaxis que sorprende:

```perl
sub fib_cola {
    my ($k, $a, $b) = @_;
    return $a if $k == 0;
    @_ = ($k - 1, $b, $a + $b);
    goto &fib_cola;              # reemplaza el marco actual: NO apila
}
```

`goto &subrutina` **no es un salto**: sustituye el marco de la llamada actual por el de la nueva, con
los argumentos que haya en `@_`. Es exactamente `tailcall` de Tcl, con un nombre desafortunado
heredado de la época en que `goto` no tenía mala prensa.

Se usa poco para recursión y mucho para **delegación**: una función que decide a quién llamar y le
cede su propio marco, de modo que el llamante original ni se entera. Es la base de varias técnicas de
`AUTOLOAD` y de despacho dinámico en CPAN.

Y para Fibonacci, la solución idiomática de Perl es memorizar con un hash, exactamente como en Lisp:

```perl
my %memo;
sub fib { my ($k) = @_; $memo{$k} //= $k < 2 ? $k : fib($k-1) + fib($k-2) }
```

Una línea, gracias a `//=` —el operador de coalescencia de la clase 053— que asigna solo si el valor
no estaba definido.
"""),
        "cpp": ("""
#include <iostream>

long long fib(int k) {
    if (k < 2) return k;
    return fib(k - 1) + fib(k - 2);
}

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "fib=" << fib(n) << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** La recursión funciona, y el **desbordamiento de pila es
comportamiento indefinido**: no hay excepción, no hay error controlado, el proceso muere con una
violación de segmento. Es una de las diferencias más prácticas con Tcl, Perl o Java.

C++ aplica la optimización de llamada de cola con `-O2` cuando puede, pero **no está garantizada por
el estándar**, así que no se puede escribir un bucle infinito como recursión de cola y confiar en
ello.

Lo que sí tiene C++ es algo que ningún otro lenguaje de esta página ofrece: **recursión en tiempo de
compilación**.

```cpp
constexpr long long fib(int k) {
    return k < 2 ? k : fib(k - 1) + fib(k - 2);
}

constexpr long long f10 = fib(10);      // 55, calculado AL COMPILAR
static_assert(f10 == 55);               // y comprobado también al compilar
```

Con `constexpr` (C++11, ampliado en C++14 y C++20), la misma función sirve para las dos cosas: si los
argumentos se conocen al compilar, **el resultado se incrusta como una constante** y no queda ninguna
llamada en el binario; si no, se ejecuta normalmente.

Antes de `constexpr`, esto se hacía con **metaprogramación de plantillas**:

```cpp
template<int N> struct Fib { static const long long v = Fib<N-1>::v + Fib<N-2>::v; };
template<> struct Fib<0> { static const long long v = 0; };
template<> struct Fib<1> { static const long long v = 1; };
```

Ese estilo —descubierto casi por accidente en los 90, cuando alguien se dio cuenta de que las
plantillas de C++ eran accidentalmente Turing-completas— es el antepasado de todo el cálculo en
tiempo de compilación moderno. Y la recursión era su única forma de iterar.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller) main(Principal);

dcl-proc Principal;
  dcl-pi *n;
    n int(10) const;
  end-pi;

  dcl-s salida char(40);

  salida = 'fib=' + %char(fib(n));
  dsply salida;
end-proc;

dcl-proc fib;
  dcl-pi *n int(20);
    k int(10) const;
  end-pi;

  if k < 2;
    return k;
  endif;
  return fib(k - 1) + fib(k - 2);
end-proc;
""", """
**Lo que esta clase enseña en RPG.** **El RPG clásico no podía recurrir**, por la misma razón que
COBOL: el almacenamiento del programa era estático y el ciclo del programa no contemplaba una segunda
activación.

**ILE lo cambió.** Los **subprocedimientos** (`dcl-proc`) tienen **almacenamiento automático por
defecto**: sus variables se crean al entrar y se destruyen al salir, en la pila. Con eso, la recursión
funciona sin declarar nada, como en este programa.

La diferencia se ve en la declaración:

```rpgle
dcl-proc fib;
  dcl-s temporal int(10);              // AUTOMÁTICA: una por invocación
  dcl-s contador int(10) static;       // ESTÁTICA: compartida entre invocaciones
```

`static` es la palabra que devuelve el comportamiento antiguo, y se usa deliberadamente para
contadores y cachés que deben sobrevivir entre llamadas. Es la misma pareja que `LOCAL-STORAGE` y
`WORKING-STORAGE` en COBOL 2002, y que `automatic` y `static` en PL/I desde 1964.

Que los tres lenguajes de negocio de esta página tengan **exactamente la misma distinción con
nombres distintos** no es casualidad: es la consecuencia de haber nacido sin pila y haberla añadido
después.

Y el `main()` en `ctl-opt` de este programa es lo que desactiva el ciclo, como se vio en la clase 044:
sin él, el ciclo intentaría gobernar la ejecución y los subprocedimientos convivirían con él de forma
confusa.
"""),
        "pli": ("""
 fibonacci: procedure options(main);

    declare n fixed binary(31);

    get list (n);
    put skip list ('fib=' || trim(char(fib(n))));

 fib: procedure (k) returns (fixed binary(31)) recursive;
    declare k fixed binary(31);
    if k < 2 then return (k);
    return (fib(k - 1) + fib(k - 2));
 end fib;

 end fibonacci;
""", """
**Lo que esta clase enseña en PL/I.** La palabra **`recursive`** al final de la cabecera es
obligatoria, y es la misma historia que en COBOL y Fortran: **sin ella, el almacenamiento del
procedimiento es estático** y la segunda invocación pisaría la primera.

Lo que hace distinto a PL/I es que la relación entre recursión y almacenamiento está **explícita en
el vocabulario del lenguaje** desde 1964, con las cuatro clases de la clase 042:

| Clase | Comportamiento |
|---|---|
| `automatic` | Por invocación — es lo que la recursión necesita |
| `static` | Una sola copia para todo el programa |
| `controlled` | Una **pila de asignaciones** que tú manejas con `allocate`/`free` |
| `based` | Donde apunte un puntero |

`controlled` merece atención en esta clase porque **es una pila explícita**: cada `allocate` de una
variable `controlled` **apila** una instancia nueva, y `free` desapila la anterior. Con eso se puede
implementar recursión a mano, guardando el estado sin depender de la pila del procesador.

En 1964, cuando muchas máquinas no tenían instrucciones de pila y la recursión era cara, poder
gestionar una pila de datos desde el lenguaje era una herramienta seria. Hoy es una curiosidad — pero
explica cómo se escribían algoritmos recursivos antes de que la recursión fuera barata.
"""),
        "mumps": ("""
FIB ; Fibonacci -- clase 069
 read n
 write "fib=", $$fib(n), !
 quit
 ;
fib(k) ; el k-esimo numero de Fibonacci
 quit:k<2 k
 quit $$fib(k-1) + $$fib(k-2)
""", """
**Lo que esta clase enseña en M.** La recursión funciona, y la razón es la pieza más peculiar del
lenguaje: **`new`**.

En M **todas las variables son globales al proceso** por defecto. Una rutina que se llame a sí misma
compartiría las variables con su propia invocación anterior, exactamente el problema de COBOL. La
solución es declarar explícitamente qué se quiere salvar:

```mumps
fib(k) ;
 new a, b                ; guarda los valores ACTUALES de a y b...
 set a = $$fib(k-1)
 set b = $$fib(k-2)
 quit a + b              ; ...y al salir, se restauran
```

`new` no crea variables locales en el sentido léxico: **guarda el valor que la variable tuviera —sea
de quien sea— y lo restaura al salir de la rutina**. Es **ámbito dinámico**, el mismo mecanismo que
`local` en Perl y que las variables especiales de Common Lisp.

La consecuencia es sutil y hay que conocerla: si `fib` llamara a otra rutina que usara `a`, **esa
rutina vería la `a` de `fib`**, no la suya. Con ámbito léxico eso sería imposible. Es más frágil y a
la vez permite cosas que el ámbito léxico no: una rutina puede fijar un valor "para todo lo que llame
desde aquí", que es el patrón que en otros lenguajes se resuelve con un parámetro de contexto pasado
por toda la cadena de llamadas.

Este programa no necesita `new` porque los parámetros de una función extrínseca ya son automáticos.
Pero cualquier variable temporal declarada dentro sí lo necesitaría, y olvidarlo es el error clásico
de la recursión en M.
"""),
        "smalltalk": ("""
| n fib |

n := stdin nextLine trimBoth asNumber.

fib := nil.
fib := [ :k | k < 2 ifTrue: [ k ] ifFalse: [ (fib value: k - 1) + (fib value: k - 2) ] ].

Transcript show: 'fib=', (fib value: n) printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Fíjate en las dos líneas de `fib`: primero se declara
`nil` y **después** se le asigna el bloque. Eso es necesario porque el bloque **se refiere a `fib`
desde dentro**, y la variable tiene que existir antes de que el bloque la capture.

Es el problema clásico de la **recursión anónima**: un bloque sin nombre no puede llamarse a sí mismo.
La solución de este programa —una variable capturada por la clausura— es la que usan JavaScript,
Python y cualquier lenguaje con lambdas. La solución teórica elegante es el **combinador Y**, que
existe y que en la práctica nadie escribe.

Lo normal en Smalltalk, claro, es que la recursión sea entre **métodos**, donde el nombre existe:

```smalltalk
Integer >> fib
    self < 2 ifTrue: [ ^self ].
    ^(self - 1) fib + (self - 2) fib
```

Y ahí aparece algo notable: **acabas de añadir un método a la clase `Integer`**, la del sistema. En
Smalltalk las clases están abiertas y se pueden extender desde tu código; `10 fib` funcionaría en toda
la imagen. Ruby heredó esa capacidad —y el debate sobre si conviene, que allí se llama *monkey
patching*—.

Sobre la pila: `thisContext` de la clase 066 **es** el marco de activación como objeto, así que en
Smalltalk se puede **inspeccionar la pila de recursión desde el propio programa**, contar su
profundidad o modificarla. No hay optimización de llamada de cola en el estándar, y el desbordamiento
levanta una excepción capturable en lugar de matar el proceso.
"""),
    },
)

# ---------------------------------------------------------------------------
# 070 — Control de flujo: break, continue, return, goto
# ---------------------------------------------------------------------------
SPECS["070"] = dict(
    gancho="""
El menor divisor mayor que 1. Un bucle que **para en cuanto encuentra**, que es la forma más común de
salir de un bucle antes de tiempo. Y el motivo de que esta clase exista: durante veinte años, salir
de un bucle por el medio se consideró tan mala práctica como el `goto`, y algunos de estos lenguajes
**se diseñaron sin ninguna forma de hacerlo**.
""",
    porque="""
Aquí el concepto es la **salida anticipada**, y estos lenguajes lo enseñan porque son los que vivieron
la polémica. **El Pascal ISO no tiene `break` ni `continue`**: Wirth los consideró incompatibles con
la programación estructurada, y el resultado es que el código Pascal clásico está lleno de banderas
booleanas. **COBOL no tuvo `EXIT PERFORM` hasta 2002.** Y Fortran cargaba con el `GO TO` calculado y
el asignado, que fueron el detonante de la carta de Dijkstra en 1968.

Enfrente, Ada, PL/I y Perl resolvieron el problema real —salir de un bucle **anidado concreto**— con
**bucles con nombre**, que es lo que hoy tienen Java, Rust y Kotlin.
""",
    cierre="""
Lo transferible: **el problema nunca fue `break`, fue el salto arbitrario**. Un `break` sale de una
estructura por su borde y el flujo sigue siendo local; un `goto` puede aterrizar en cualquier sitio y
obliga a leer el programa entero para saber cómo se llegó ahí. Por eso todos los lenguajes acabaron
adoptando la salida etiquetada —`exit Bucle when`, `last EXTERIOR`, `leave bucle`— que da la potencia
del salto **acotada a una estructura visible**. Y por eso el `goto` sigue vivo exactamente en un
caso: **liberar recursos en C**, donde no hay destructores.
""",
    langs={
        "cobol": ("""
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
""", """
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
"""),
        "fortran": ("""
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
""", """
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
"""),
        "ada": ("""
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
""", """
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
"""),
        "pascal": ("""
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
""", """
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
"""),
        "lisp": ("""
(let* ((n (read))
       (res (or (loop for d from 2 to n
                      when (zerop (mod n d))
                      return d)
                n)))
  (format t "primer_divisor=~D~%" res))
""", """
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
"""),
        "tcl": ("""
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
""", """
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
"""),
        "perl": ("""
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

print "primer_divisor=$res\\n";
""", """
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
"""),
        "cpp": ("""
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

    std::cout << "primer_divisor=" << res << '\\n';
    return 0;
}
""", """
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
"""),
        "rpg": ("""
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
""", """
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
"""),
        "pli": ("""
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
""", """
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
"""),
        "mumps": ("""
DIVISOR ; Primer divisor -- clase 070
 read n
 set res = n
 for d = 2:1:n do  quit:res'=n
 . quit:n#d'=0
 . set res = d
 write "primer_divisor=", res, !
 quit
""", """
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
"""),
        "smalltalk": ("""
| n res |

n := stdin nextLine trimBoth asNumber.

res := (2 to: n) detect: [ :d | n \\\\ d = 0 ] ifNone: [ n ].

Transcript show: 'primer_divisor=', res printString; cr.
""", """
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
    2 to: n do: [ :d | n \\\\ d = 0 ifTrue: [ ^d ] ].    "^ sale del MÉTODO"
    ^n
```

Ese `^` dentro del bloque de `to:do:` es un salto no local que atraviesa la llamada al método
`to:do:`. Está implementado con `thisContext` y es, funcionalmente, el `return-from` de Lisp. Es la
única forma de salida anticipada del lenguaje, y es potente: **un bloque pasado a otro objeto puede
terminar el método que lo creó**, aunque se evalúe muy lejos.
"""),
    },
)

# ---------------------------------------------------------------------------
# 071 — Manejo de errores I: excepciones (try / catch / finally)
# ---------------------------------------------------------------------------
SPECS["071"] = dict(
    gancho="""
Dividir dos enteros, y que dividir por cero no reviente el programa. El caso más simple de manejo de
errores, y el que separa a estos lenguajes de forma más nítida de toda la Parte 4: **cuatro de ellos
tienen excepciones, cuatro no tienen ninguna forma de excepción, y tres tienen algo MEJOR que las
excepciones** — condiciones que se pueden manejar **sin destruir el contexto en que ocurrió el
error**.
""",
    porque="""
Aquí el concepto es la **señalización y el manejo de errores**, y estos lenguajes lo enseñan porque
contienen tanto el origen como el camino no tomado. **PL/I inventó el manejo estructurado de errores
en 1964** con las condiciones `ON`, y su modelo permitía **reparar y continuar**, no solo capturar y
abortar. **Common Lisp** llevó esa idea a su forma más completa con el sistema de condiciones y
reinicios. Y **Smalltalk** tiene excepciones **reanudables**.

Enfrente, **Fortran no tiene excepciones en absoluto**, y COBOL tiene manejo por sentencia —`ON SIZE
ERROR`— en lugar de por bloque.
""",
    cierre="""
La idea que hay que llevarse: **el `try/catch` moderno desenrolla la pila ANTES de ejecutar el
manejador**, y con ella se destruye el contexto donde ocurrió el error. Cuando el manejador decide
que se puede continuar, ya es tarde: hay que reintentar la operación entera desde fuera.

PL/I, Common Lisp y Smalltalk hacen lo contrario: **el manejador se ejecuta encima del punto que
falló**, con todo vivo, y puede decidir reparar y reanudar. Es estrictamente más potente, casi nadie
lo copió, y saber que existe cambia cómo se leen las limitaciones del `catch` que usas a diario.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. DIVSEG.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TXT-A   PIC X(20).
01  TXT-B   PIC X(20).
01  A       PIC S9(9) COMP-3.
01  B       PIC S9(9) COMP-3.
01  R       PIC S9(9) COMP-3.
01  ED-R    PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    DIVIDE A BY B GIVING R
        ON SIZE ERROR
            DISPLAY "error=division por cero"
        NOT ON SIZE ERROR
            MOVE R TO ED-R
            DISPLAY "resultado=" FUNCTION TRIM(ED-R)
    END-DIVIDE

    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** **COBOL no tiene `try`/`catch`. Tiene manejo de condiciones
por SENTENCIA**, y esa es una diferencia de diseño con consecuencias.

`ON SIZE ERROR` es una cláusula del propio `DIVIDE`, no un bloque que envuelva código. La rama de
error está **pegada a la operación que puede fallar**, y `NOT ON SIZE ERROR` es la rama de éxito. No
hay forma de "envolver veinte líneas" y capturar lo que sea que falle dentro.

La familia completa sigue el mismo patrón, y cubre lo que puede fallar en cada verbo:

```cobol
DIVIDE ... ON SIZE ERROR ...          *> desbordamiento o división por cero
READ ... AT END ...                   *> fin de fichero
READ ... INVALID KEY ...              *> clave no encontrada
STRING ... ON OVERFLOW ...            *> no cabe
CALL ... ON EXCEPTION ...             *> el programa no existe
```

La ventaja es que **es imposible olvidar dónde puede fallar algo**: la posibilidad está escrita en la
sentencia. La desventaja es la verbosidad, y que no hay propagación: cada nivel maneja lo suyo.

Para los errores que no pertenecen a una sentencia concreta, COBOL tiene las **DECLARATIVES**, que sí
son un manejador global:

```cobol
PROCEDURE DIVISION.
DECLARATIVES.
ERROR-FICHERO SECTION.
    USE AFTER STANDARD ERROR PROCEDURE ON CLIENTES.
MANEJAR.
    DISPLAY "fallo de E/S: " FILE-STATUS-CLIENTES.
END DECLARATIVES.
```

`USE AFTER ERROR` instala un manejador para un fichero, que se ejecuta automáticamente ante cualquier
fallo de E/S sobre él. Es exactamente el `ON` de PL/I, con otro nombre.
"""),
        "fortran": ("""
program divseg
   implicit none
   integer :: a, b

   read(*, *) a, b

   !  Fortran NO tiene excepciones: la comprobación es explícita, y punto.
   if (b == 0) then
      write(*, '(A)') 'error=division por cero'
   else
      write(*, '(A,I0)') 'resultado=', a / b
   end if
end program divseg
""", """
**Lo que esta clase enseña en Fortran.** **Fortran no tiene excepciones. Ninguna.** Ni `try`, ni
`catch`, ni `raise`, ni condiciones. En 2026, con el estándar de 2023, sigue sin tenerlas.

No es un olvido: es coherente con su dominio. Un manejador de excepciones implica un salto no local y
un desenrollado de pila, y las dos cosas **impiden vectorizar y reordenar**. En un bucle que se
ejecuta mil millones de veces, la mera posibilidad de que algo salte fuera limita al optimizador.

Lo que Fortran tiene son **códigos de estado**, que es el modelo de la clase siguiente:

```fortran
read(unidad, *, iostat=ios, iomsg=mensaje) valor
if (ios /= 0) then ...

allocate(v(n), stat=err, errmsg=mensaje)
if (err /= 0) then ...
```

`iostat`, `stat`, `iomsg` y `errmsg` son **argumentos opcionales**: si los pones, el error se te
devuelve; si no los pones, **el programa aborta**. Esa elección por llamada es muy característica.

Y para la aritmética, Fortran 2003 añadió el módulo **`ieee_arithmetic`**, que da acceso a las
banderas del procesador definidas por IEEE 754:

```fortran
use ieee_arithmetic
if (ieee_support_flag(ieee_divide_by_zero, x)) then
   call ieee_set_halting_mode(ieee_divide_by_zero, .false.)   ! no abortar
   ...
   call ieee_get_flag(ieee_divide_by_zero, ocurrio)           ! ¿pasó?
end if
```

Es manejo de errores **consultando banderas después**, no interrumpiendo el flujo. Encaja perfectamente
con el cálculo vectorizado: se procesan mil millones de elementos y al final se pregunta si alguno dio
problemas.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Divseg is
   A, B, R : Integer;
begin
   Get (A);
   Get (B);

   begin
      R := A / B;               --  B = 0 levanta Constraint_Error
      Put ("resultado="); Put (R, Width => 1); New_Line;
   exception
      when Constraint_Error =>
         Put_Line ("error=division por cero");
   end;
end Divseg;
""", """
**Lo que esta clase enseña en Ada.** Ada tiene excepciones desde 1983, con una diferencia importante
frente a Java o C++: **las excepciones de Ada no son objetos, son nombres**. No llevan datos ni
jerarquía de clases; son etiquetas de una situación.

```ada
Saldo_Insuficiente : exception;        --  se DECLARA como una constante
raise Saldo_Insuficiente with "faltan 20 euros";   --  Ada 2005: con mensaje
```

Eso las hace baratísimas y analizables. Y las cuatro predefinidas cubren la mayoría de los casos:
`Constraint_Error` (rango, índice, división por cero, nulo), `Program_Error`, `Storage_Error`
(memoria o pila agotada) y `Tasking_Error`.

Fíjate en que este programa **no comprueba `B = 0`**: la división levanta `Constraint_Error` por sí
sola. Es la misma filosofía de los subtipos de la clase 041 — el error se detecta en la operación, no
en una comprobación previa que alguien podría olvidar.

Y hay algo de fondo que conviene saber: **en aviónica y sistemas críticos, las excepciones suelen
prohibirse**. El perfil Ravenscar y las guías de certificación las restringen porque **el tiempo de
propagación de una excepción es difícil de acotar**, y en un sistema de tiempo real duro todo tiene
que tener un límite superior demostrable.

Ahí se usa el modelo de la clase siguiente: parámetros de estado, contratos que garantizan que el
error no puede ocurrir, y SPARK demostrándolo estáticamente. **La mejor excepción es la que se
demuestra imposible.**
"""),
        "pascal": ("""
program Divseg;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  A, B, R: Integer;

begin
  Read(A, B);

  try
    R := A div B;
    WriteLn('resultado=', IntToStr(R));
  except
    on E: EDivByZero do
      WriteLn('error=division por cero');
  end;
end.
""", """
**Lo que esta clase enseña en Pascal.** **El Pascal ISO no tiene excepciones.** `try`/`except` y
`try`/`finally` son de Delphi, incorporados en 1995 junto con la jerarquía de clases `Exception`, y
Free Pascal los adoptó.

Y hay una particularidad sintáctica que distingue a Object Pascal de casi todos los demás: **son dos
construcciones separadas que no se combinan**.

```pascal
try
  try
    ...
  except
    on E: EDivByZero do ...;
  end;
finally
  Recurso.Free;        { hay que ANIDAR: no existe try..except..finally }
end;
```

En Java, C# y Python se escribe `try/catch/finally` en un solo bloque. En Object Pascal hay que
anidar uno dentro de otro. Es más verboso y tiene una lógica: separa **manejar un error** de
**garantizar una limpieza**, que son dos preocupaciones distintas.

Y `try..finally` es, en la práctica, **la construcción más usada del lenguaje**, mucho más que
`try..except`. La razón es la clase 042: sin recolector de basura, cada objeto creado necesita su
`Free` garantizado.

```pascal
Lista := TStringList.Create;
try
  ...
finally
  Lista.Free;      { el idioma más repetido de todo el código Delphi }
end;
```

Es el mismo problema que C++ resuelve con RAII y Go con `defer`. Object Pascal eligió la
construcción explícita, con la ventaja de que se ve y el inconveniente de que se puede olvidar.
"""),
        "lisp": ("""
(let* ((a (read))
       (b (read)))
  (handler-case
      (format t "resultado=~D~%" (truncate a b))
    (division-by-zero ()
      (format t "error=division por cero~%"))))
""", """
**Lo que esta clase enseña en Common Lisp.** `handler-case` **es** el `try/catch`, y funciona como se
espera. Pero es la parte aburrida: Lisp tiene además un **sistema de condiciones y reinicios** que es
estrictamente más potente y que casi ningún lenguaje copió.

La diferencia clave: **`handler-bind` ejecuta el manejador ANTES de desenrollar la pila**.

```lisp
(defun leer-registro (linea)
  (restart-case (parsear linea)
    (usar-valor (v) :report "Usar otro valor" v)      ; REINICIOS ofrecidos
    (saltar ()     :report "Ignorar esta línea" nil)))

(handler-bind ((error (lambda (c)
                        (invoke-restart 'saltar))))   ; el manejador ELIGE
  (dolist (l lineas) (leer-registro l)))
```

`parsear` no sabe qué hacer con un error, así que **ofrece opciones** con `restart-case`. Quien llama
—que sí conoce el contexto— elige una con `invoke-restart`. Y el manejador se ejecuta **encima del
punto que falló**, con toda la pila viva, así que puede reparar y continuar **en el sitio exacto**.

Con `try/catch` eso es imposible: para cuando el `catch` se ejecuta, los marcos entre medias ya se
destruyeron y solo queda reintentar todo desde fuera.

Ese diseño tiene una consecuencia práctica que se ve a diario: **cuando un programa Lisp falla en el
REPL, el depurador te ofrece una lista de reinicios** —reintentar, usar otro valor, definir la función
que faltaba, abortar— y puedes arreglar el problema y **continuar la ejecución** sin reiniciar.

Es la misma idea que las condiciones `ON` de PL/I de 1964, llevada a su forma completa. Dylan la
heredó; el resto de la industria eligió `try/catch`.
"""),
        "tcl": ("""
gets stdin linea
lassign [split [string trim $linea]] a b

if {[catch {expr {$a / $b}} r]} {
    puts "error=division por cero"
} else {
    puts "resultado=$r"
}
""", """
**Lo que esta clase enseña en Tcl.** **`catch` no es una construcción de excepciones: es un comando
que devuelve un número.** Ejecuta el cuerpo y devuelve el código de resultado —0 si todo fue bien, 1
si hubo error— dejando el valor o el mensaje en la variable que le des.

Eso lo convierte, literalmente, en el modelo de "errores como valores" de la clase siguiente, con
sintaxis de excepción. Y encaja con lo que se vio en la clase 070: **en Tcl todo comando devuelve uno
de cinco códigos**, y `catch` simplemente los expone en lugar de propagarlos.

Tcl 8.6 añadió `try`, que es azúcar sobre `catch` con mejor legibilidad:

```tcl
try {
    expr {$a / $b}
} trap {ARITH DIVZERO} {msg opciones} {
    puts "error=division por cero"
} on error {msg opciones} {
    puts "otro error: $msg"
} finally {
    puts "esto se ejecuta siempre"
}
```

`trap` casa contra el **código de error**, que en Tcl es una **lista** —`ARITH DIVZERO {divide by
zero}`— y no una clase. Casar por prefijo de lista da una jerarquía sin necesidad de herencia:
`trap {POSIX ENOENT}` o `trap {POSIX}` para cualquier error POSIX.

Y `error` lanza, con tres argumentos: mensaje, información de pila y **código estructurado**.

```tcl
error "saldo insuficiente" "" {BANCO SALDO 42}
```

Que el código de error sea un dato estructurado y no un tipo es muy propio de Tcl, y resulta
sorprendentemente práctico: se puede construir, comparar y serializar sin definir ninguna clase.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($x, $y) = split ' ', $linea;

my $r = eval { int($x / $y) };

if ($@) {
    print "error=division por cero\\n";
} else {
    print "resultado=$r\\n";
}
""", """
**Lo que esta clase enseña en Perl.** El manejo de errores clásico de Perl es **`eval` con bloque**, y
es de las partes del lenguaje que peor han envejecido:

```perl
eval { ... };          # ejecuta y captura lo que muera
if ($@) { ... }        # $@ contiene el error, o cadena vacía
```

Funciona y tiene **tres trampas** conocidas, que conviene conocer porque explican por qué existe
`Try::Tiny`:

1. **`$@` es global** y cualquier cosa puede pisarlo — incluido un destructor que se ejecute al salir
   del `eval`.
2. **Hay que comprobar `$@` inmediatamente**, antes de cualquier otra operación.
3. **`$@` puede quedar vacío aunque haya habido error**, en casos límite documentados.

Por eso el módulo `Try::Tiny` fue durante quince años prácticamente obligatorio:

```perl
use Try::Tiny;
try   { ... }
catch { warn "error: $_" }
finally { ... };
```

Y **Perl 5.34 incorporó `try`/`catch` al lenguaje**, estabilizado en 5.40:

```perl
use v5.36;
use feature 'try';

try {
    my $r = $x / $y;
} catch ($e) {
    say "error: $e";
}
```

Que un lenguaje de 1987 añadiera manejo de errores con sintaxis moderna en 2021 es, otra vez, el
argumento de esta sección. Y `die` puede lanzar **cualquier referencia**, no solo cadenas, así que las
excepciones como objetos existen desde siempre: `die Mi::Error->new(...)`.
"""),
        "cpp": ("""
#include <iostream>
#include <stdexcept>

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    try {
        //  OJO: en C++ la división entera por cero NO lanza: es comportamiento
        //  indefinido. Hay que comprobarlo y lanzar explícitamente.
        if (b == 0) {
            throw std::domain_error("division por cero");
        }
        std::cout << "resultado=" << (a / b) << '\\n';
    } catch (const std::domain_error&) {
        std::cout << "error=division por cero\\n";
    }
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** El comentario del código es el contenido de la clase: **la
división entera por cero en C++ NO lanza una excepción. Es comportamiento indefinido.** El programa
puede abortar, dar basura o —lo peor— hacer que el compilador asuma que nunca ocurre y elimine el
código que lo comprueba.

Es una diferencia real con Ada, Pascal, Lisp, Perl y Smalltalk, donde sí es un error definido. En C++
hay que comprobarlo a mano.

Y lo que C++ aporta de verdad a esta clase no es `try/catch`: es **RAII**, que resuelve el problema
del `finally` sin necesidad de `finally`.

```cpp
{
    std::lock_guard<std::mutex> cierre(m);     // se bloquea
    std::ifstream f("datos.txt");              // se abre
    procesar(f);                               // si esto lanza...
}   // ...el mutex se libera y el fichero se cierra IGUAL
```

**C++ es el único lenguaje mayoritario sin `finally`, y es a propósito.** Stroustrup ha argumentado
repetidamente que `finally` es la solución equivocada: obliga a escribir la limpieza en cada sitio
donde se usa el recurso, mientras que el destructor la escribe **una vez, en la clase del recurso**.

La contrapartida es una regla estricta: **un destructor no debe lanzar nunca**. Si lanza durante el
desenrollado de otra excepción, el programa llama a `std::terminate`. Por eso los destructores se
marcan `noexcept` por defecto desde C++11.

Y `noexcept` en una función es una promesa comprobada: si algo escapa, `terminate`. Permite al
compilador generar código mejor —sin tablas de desenrollado— y es la base de que `std::vector` pueda
mover elementos en lugar de copiarlos al crecer.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi DIVSEG;
  a int(10) const;
  b int(10) const;
end-pi;

dcl-s r      int(10);
dcl-s salida char(40);

monitor;
  r = %div(a : b);
  salida = 'resultado=' + %char(r);
on-error;
  salida = 'error=division por cero';
endmon;

dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** **`monitor` / `on-error` / `endmon` es el `try`/`catch` de RPG**,
y llegó con la versión 5 en 2001. Antes de eso, el manejo de errores era… los indicadores.

En el RPG clásico, cada operación que podía fallar llevaba un indicador en una columna concreta:

```text
     C     CLAVE         CHAIN     CLIENTES                           50
```

Ese `50` significa: "si la operación falla, enciende `*IN50`". El código de después consultaba
`*IN50` para saber si había ido bien. **El manejo de errores eran variables globales numeradas**, con
todos los problemas que eso implica: nadie recuerda qué indicador es cuál, y olvidar comprobarlo no
da ningún aviso.

`monitor` también acepta filtrar por **rango de códigos de error**, lo que da una jerarquía sin
clases:

```rpgle
monitor;
  ...
on-error 00121;          // índice de matriz fuera de rango
  ...
on-error *file;          // cualquier error de fichero
on-error *all;           // cualquiera
endmon;
```

Y RPG tiene además el manejador global heredado del ciclo: el subprocedimiento **`*PSSR`**, que se
ejecuta ante cualquier error no capturado y puede decidir si continuar o terminar. Es el equivalente
de las DECLARATIVES de COBOL y del `ON ERROR` de PL/I.

Lo que no tiene RPG es `finally`. La limpieza se escribe en `*PSSR` o se repite.
"""),
        "pli": ("""
 divseg: procedure options(main);

    declare (a, b, r) fixed binary(31);

    on zerodivide begin;
       put skip list ('error=division por cero');
       stop;
    end;

    get list (a, b);

    r = divide(a, b, 31);
    put skip list ('resultado=' || trim(char(r)));

 end divseg;
""", """
**Lo que esta clase enseña en PL/I.** **Aquí nació el manejo estructurado de errores.** En 1964, cuando
FORTRAN comprobaba códigos y COBOL tenía cláusulas por sentencia, PL/I introdujo las **condiciones
`ON`**: un manejador que se **instala** y queda activo, y al que el sistema salta cuando ocurre la
condición.

```pli
on zerodivide   ...      /* división por cero */
on overflow     ...      /* desbordamiento en punto flotante */
on fixedoverflow ...     /* desbordamiento decimal */
on conversion   ...      /* texto no numérico */
on endfile(f)   ...      /* fin de fichero */
on subscriptrange ...    /* índice fuera de rango */
on error        ...      /* cualquier cosa */
```

Fíjate en la diferencia con `try/catch`: **no hay bloque**. `on` no envuelve código; declara que a
partir de ahí, y hasta que se salga del ámbito, esa condición tiene ese manejador. Es **ámbito
dinámico** aplicado al manejo de errores — el mismo mecanismo que `handler-bind` de Common Lisp y que
las variables `new` de M.

Y esa es la clave de por qué el modelo de PL/I es más potente que el `try/catch` que heredamos: **el
manejador se ejecuta encima del punto que falló, sin desenrollar la pila**. Si no hace `goto` ni
`stop`, la ejecución **continúa donde estaba**.

```pli
on conversion begin;
   onsource() = '0';     /* CORRIGE el dato que falló... */
end;                      /* ...y la conversión se REINTENTA con el valor nuevo */
```

`onsource()` es una **pseudovariable**: representa el dato que provocó el error y se le puede
asignar. Junto a `oncode()`, `onchar()` y `onloc()`, forman un conjunto de introspección del error que
ningún lenguaje moderno tiene.

Dijkstra criticó a PL/I por su tamaño. Esta parte, sin embargo, era mejor que lo que vino después.
"""),
        "mumps": ("""
DIVSEG ; Excepciones -- clase 071
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 if b = 0 write "error=division por cero",! quit
 write "resultado=", a\\b, !
 quit
""", """
**Lo que esta clase enseña en M.** El M estándar de 1977 **no tenía manejo de errores**: un error
abortaba la rutina y devolvía el control al nivel superior, y punto. La comprobación previa —como en
este programa— era la única forma.

Las implementaciones añadieron cada una la suya, y eso produjo la fragmentación más visible del
lenguaje:

```mumps
 set $ztrap = "MANEJADOR^RUTINA"     ; GT.M, YottaDB, Caché: manejador global
 set $etrap = "do ERROR^UTIL"        ; el estándar posterior
```

`$ztrap` y `$etrap` son **variables especiales que contienen código**: cuando ocurre un error, M
ejecuta lo que haya en esa cadena. Es la indirección de la clase 068 aplicada al manejo de errores, con
la misma potencia y la misma imposibilidad de análisis estático.

El estándar **M95** incorporó por fin una estructura moderna, y las implementaciones actuales la
tienen:

```mumps
 try {
   set r = a/b
 } catch e {
   write "error: ", e.Name, !
 }
```

Esa sintaxis con llaves es de **InterSystems ObjectScript**, el descendiente de M de la clase 043, y
convive con el M clásico en el mismo sistema.

Y hay una variable que conviene conocer: **`$ecode`**, que contiene la lista de errores activos según
el estándar, y **`$stack`**, que da acceso a la pila de llamadas. Con ellas se puede escribir un
manejador portable — aunque en la práctica casi todo el código M usa las extensiones de su
implementación.
"""),
        "smalltalk": ("""
| partes a b |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

[ Transcript show: 'resultado=', (a // b) printString; cr ]
    on: ZeroDivide
    do: [ :e | Transcript show: 'error=division por cero'; cr ].
""", """
**Lo que esta clase enseña en Smalltalk.** **`on:do:` es un mensaje enviado a un bloque.** No hay
`try`, no hay `catch` y no hay sintaxis: el bloque protegido es el receptor, la clase de excepción y
el manejador son los argumentos.

```smalltalk
BlockClosure >> on: unaClaseDeExcepcion do: unManejador
```

Y las excepciones son **objetos con protocolo propio**, lo que da al manejador opciones que el
`catch` de Java o C++ no tienen:

```smalltalk
[ ... ] on: Error do: [ :e |
    e return: 0.       "termina el bloque protegido devolviendo 0"
    e retry.           "vuelve a EJECUTAR el bloque protegido desde el principio"
    e resume: 42.      "CONTINÚA donde saltó, como si la expresión valiera 42"
    e pass.            "delega en el manejador de más afuera"
    e signal.          "vuelve a lanzarla"
].
```

**`resume:` es la que importa.** Reanuda la ejecución **en el punto exacto donde se señaló el error**,
sustituyendo el valor de la expresión que falló. Eso solo es posible porque, igual que en PL/I y en
CommonLisp, **el manejador se ejecuta antes de desenrollar la pila**.

No todas las excepciones son reanudables: `Error` no lo es, `Warning` sí. La clase declara si lo es
con `isResumable`, y el sistema lo comprueba.

Y `ensure:` es el `finally`, también como mensaje:

```smalltalk
[ ... ] ensure: [ recurso close ].         "pase lo que pase"
[ ... ] ifCurtailed: [ registrar ].        "SOLO si termina anormalmente"
```

`ifCurtailed:` no tiene equivalente en el núcleo: distingue "termina" de "termina mal", que son
cosas distintas y en Java hay que averiguar con una bandera.
"""),
    },
)

# ---------------------------------------------------------------------------
# 072 — Manejo de errores II: resultados y valores
# ---------------------------------------------------------------------------
SPECS["072"] = dict(
    gancho="""
El mismo problema que la clase anterior, con la estrategia opuesta: **el error no interrumpe nada, se
devuelve como un valor**. Es el modelo de Go, de Rust y de `std::expected`, y la revolución de la
última década en manejo de errores. Y también, casi exactamente, **lo que COBOL lleva haciendo desde
1968 con el `FILE STATUS`**.
""",
    porque="""
Aquí el concepto es **el error como dato en lugar de como salto**, y estos lenguajes lo enseñan
porque **es su modelo nativo**. COBOL comprueba un código de dos caracteres después de cada operación
de fichero; Fortran devuelve `iostat`; Ada usa parámetros `out`; M devuelve un valor de estado. Ninguno
de ellos "adoptó" el modelo de Go: **es el modelo del que Go partió**.

Y Lisp aporta la variante más elegante: **valores múltiples**, donde el segundo valor lleva el error
y **ignorarlo es gratis** — sin `_` obligatorio, sin construir una tupla, sin envolver nada.
""",
    cierre="""
La comparación que cierra la Parte 4: **una excepción es difícil de ignorar y fácil de olvidar
manejar; un valor de error es fácil de ignorar y difícil de olvidar que existe**, porque está en la
firma. Ninguno de los dos modelos gana: por eso Rust puso el error en el tipo **y** obligó a
tratarlo con `#[must_use]`, y por eso C++23 añadió `std::expected` sin quitar las excepciones.

Lo que sí es cierto es que este modelo, presentado como novedad en 2012, tiene sesenta años de
producción detrás en los lenguajes de esta página. Conviene saberlo antes de creer que algo se acaba
de inventar.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. DIVVAL.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TXT-A   PIC X(20).
01  TXT-B   PIC X(20).
01  A       PIC S9(9) COMP-3.
01  B       PIC S9(9) COMP-3.
01  R       PIC S9(9) COMP-3.
01  ESTADO  PIC 9.
    88  TODO-BIEN  VALUE 0.
    88  ERR-DIV    VALUE 1.
01  ED-R    PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    PERFORM DIVIDIR

    IF ERR-DIV
        DISPLAY "err=division"
    ELSE
        MOVE R TO ED-R
        DISPLAY "ok=" FUNCTION TRIM(ED-R)
    END-IF

    STOP RUN.

DIVIDIR.
    IF B = 0
        SET ERR-DIV TO TRUE
        MOVE 0 TO R
    ELSE
        SET TODO-BIEN TO TRUE
        DIVIDE A BY B GIVING R
    END-IF.
""", """
**Lo que esta clase enseña en COBOL.** **Este es el modelo nativo de COBOL, y es de 1968.** El
`FILE STATUS` es exactamente "errores como valores", con una convención que sigue vigente:

```cobol
SELECT CLIENTES ASSIGN TO ENTRADA
    FILE STATUS IS WS-ESTADO.

01  WS-ESTADO  PIC XX.
    88  OK              VALUE "00".
    88  FIN-FICHERO     VALUE "10".
    88  NO-ENCONTRADO   VALUE "23".
    88  DUPLICADO       VALUE "22".

READ CLIENTES
EVALUATE TRUE
    WHEN OK             PERFORM PROCESAR
    WHEN FIN-FICHERO    SET TERMINADO TO TRUE
    WHEN NO-ENCONTRADO  PERFORM AVISAR
    WHEN OTHER          PERFORM ERROR-GRAVE
END-EVALUATE
```

Un **código de dos caracteres** después de cada operación, comprobado con `EVALUATE`. Compáralo con
`if err != nil` de Go: es la misma disciplina, con nombres de condición en lugar de un tipo de error,
y **cincuenta años antes**.

Y COBOL tiene el mismo problema que Go: **nadie te obliga a comprobarlo**. Un `READ` cuyo estado no
se mira es un error silencioso, y las guías de estilo COBOL llevan décadas insistiendo en que se
compruebe siempre. Es exactamente el mismo debate que hoy se tiene sobre Go y su `err`.

La diferencia con la clase anterior es de reparto de responsabilidad: `ON SIZE ERROR` obliga a decidir
en el sitio; `FILE STATUS` deja el resultado disponible y confía en que lo mires.
"""),
        "fortran": ("""
program divval
   implicit none
   integer :: a, b, r, estado

   read(*, *) a, b
   call dividir(a, b, r, estado)

   if (estado /= 0) then
      write(*, '(A)') 'err=division'
   else
      write(*, '(A,I0)') 'ok=', r
   end if

contains

   subroutine dividir(x, y, res, stat)
      integer, intent(in)  :: x, y
      integer, intent(out) :: res, stat
      if (y == 0) then
         res  = 0
         stat = 1
      else
         res  = x / y
         stat = 0
      end if
   end subroutine dividir

end program divval
""", """
**Lo que esta clase enseña en Fortran.** Este **es** el modelo de Fortran, y no tiene alternativa: sin
excepciones, un error solo puede viajar como dato.

La convención del lenguaje está estandarizada y es muy uniforme —el argumento se llama `stat` o
`iostat`, y siempre vale **cero si todo fue bien**:

```fortran
read(u, *, iostat=ios, iomsg=msg) v
allocate(v(n), stat=err, errmsg=msg)
deallocate(v, stat=err)
close(u, iostat=ios)
```

Y hay un detalle de diseño que Fortran hace mejor que Go y que conviene señalar: **el argumento de
estado es OPCIONAL, y su ausencia significa "aborta"**.

```fortran
read(u, *) v                    ! si falla, el programa TERMINA
read(u, *, iostat=ios) v        ! si falla, me lo dices y yo decido
```

Esa elección por llamada resuelve la queja más común contra los errores como valores —que obligan a
escribir `if err != nil` incluso cuando no vas a hacer nada útil con él—. En Fortran, si no vas a
manejarlo, **no pides el código y el programa falla ruidosamente**, que suele ser lo correcto.

Es una tercera vía entre la excepción y el valor: **el error es un valor si lo pides, y una parada si
no**. Rust hace algo parecido con `unwrap()`, pero al revés: allí hay que escribir algo para que
falle.

`intent(in)` e `intent(out)` en los parámetros son obligatorios en código moderno, y el compilador
comprueba que un `out` se asigne antes de salir.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Divval is

   procedure Dividir (A, B : Integer; R : out Integer; Ok : out Boolean) is
   begin
      if B = 0 then
         R  := 0;
         Ok := False;
      else
         R  := A / B;
         Ok := True;
      end if;
   end Dividir;

   A, B, R : Integer;
   Ok      : Boolean;
begin
   Get (A);
   Get (B);
   Dividir (A, B, R, Ok);

   if Ok then
      Put ("ok="); Put (R, Width => 1); New_Line;
   else
      Put_Line ("err=division");
   end if;
end Divval;
""", """
**Lo que esta clase enseña en Ada.** Los **parámetros `out`** son el mecanismo de Ada, y tienen una
propiedad que casi ningún lenguaje comparte: **el compilador comprueba que se asignen antes de salir
del procedimiento**, y avisa si se leen antes de asignarlos.

Ada distingue tres modos, y escribirlos es obligatorio en código serio:

| Modo | Significado |
|---|---|
| `in` | Solo lectura — es el valor por defecto |
| `out` | Solo escritura: el valor de entrada no existe |
| `in out` | Se lee y se modifica |

Esa distinción está **en la firma**, así que quien llama sabe qué se va a modificar sin leer el
cuerpo. En C hay que mirar si el parámetro es un puntero y confiar; en C++ ayuda el `const&`, pero un
`T&` no distingue si se lee o se escribe.

Y en sistemas críticos, este modelo **se prefiere a las excepciones**, por la razón de la clase 071:
el tiempo de propagación de una excepción es difícil de acotar, y el `if` sobre un booleano es
predecible.

Ada tiene además una variante que va más allá y que es lo más parecido a Rust de esta página: los
**contratos**.

```ada
procedure Dividir (A, B : Integer; R : out Integer)
  with Pre => B /= 0;      --  el error NO PUEDE OCURRIR: es responsabilidad del que llama
```

Con SPARK, esa precondición **se demuestra estáticamente** en todas las llamadas del programa. No hay
que devolver un error porque **se ha probado que la situación es imposible**. Es el nivel al que
aspira el manejo de errores cuando el fallo no es una opción.
"""),
        "pascal": ("""
program Divval;
{$MODE OBJFPC}{$H+}
uses SysUtils;

function TryDividir(A, B: Integer; out R: Integer): Boolean;
begin
  if B = 0 then
  begin
    R := 0;
    Result := False;
  end
  else
  begin
    R := A div B;
    Result := True;
  end;
end;

var
  A, B, R: Integer;

begin
  Read(A, B);

  if TryDividir(A, B, R) then
    WriteLn('ok=', IntToStr(R))
  else
    WriteLn('err=division');
end.
""", """
**Lo que esta clase enseña en Pascal.** El prefijo **`Try`** de `TryDividir` no es una elección
arbitraria: es una **convención establecida de la biblioteca de Delphi y Free Pascal**, y merece
conocerse porque resuelve muy bien el problema de esta clase.

La biblioteca ofrece cada conversión en **tres variantes**:

```pascal
StrToInt('42')              { lanza EConvertError si falla }
StrToIntDef('x', 0)         { devuelve un valor por defecto }
TryStrToInt('x', N)         { devuelve False y no toca N  <- errores como valores }
```

Las tres existen porque **las tres situaciones son legítimas**: si el dato viene de tu propio código y
un fallo indica un bug, quieres la excepción; si viene de una configuración con valor por defecto
razonable, quieres `Def`; y si viene de un usuario y hay que reaccionar, quieres `Try`.

Que la biblioteca ofrezca las tres, con nombres sistemáticos, es una lección de diseño de API mejor
que la de casi cualquier lenguaje moderno — donde normalmente hay una sola forma y el resto se
construye a mano.

Y `out` en Pascal significa lo mismo que en Ada: **el valor de entrada no importa** y el compilador lo
sabe. Se distingue de `var` (que es `in out`) y del paso por valor. Es la misma tríada, con otros
nombres.

Delphi moderno añadió además genéricos, con los que la comunidad ha construido tipos `TResult<T>` y
`TOption<T>` al estilo de Rust — pero sin comprobación obligatoria del compilador, así que son una
convención más.
"""),
        "lisp": ("""
(defun dividir (a b)
  (if (zerop b)
      (values nil :division)
      (values (truncate a b) nil)))

(let* ((a (read))
       (b (read)))
  (multiple-value-bind (r err) (dividir a b)
    (if err
        (format t "err=division~%")
        (format t "ok=~D~%" r))))
""", """
**Lo que esta clase enseña en Common Lisp.** Los **valores múltiples** son la aportación de Lisp a
esta clase, y son mejores que la tupla de Go y que el `Result` de Rust en un aspecto concreto:
**ignorarlos es gratis**.

```lisp
(dividir 10 2)                                  ; en contexto normal, solo el PRIMERO
(multiple-value-bind (r err) (dividir 10 0) ...)  ; los dos, si los quieres
(multiple-value-list (dividir 10 2))            ; como lista, si te hace falta
(nth-value 1 (dividir 10 0))                    ; solo el segundo
```

No se construye ninguna estructura. Si el llamante no pide el segundo valor, **no existe coste**: no
hay tupla que asignar ni objeto que descartar. En Go hay que escribir `_` para ignorar el error; en
Rust hay que hacer algo con el `Result` o el compilador avisa.

El estándar usa este mecanismo por todas partes, y los ejemplos son elocuentes:

```lisp
(gethash clave tabla)      ; => valor, ¿estaba?   (la clase 053)
(truncate 17 5)            ; => 3, 2             (cociente y resto, clase 049)
(floor -7 3)               ; => -3, 2
(parse-integer "42x" :junk-allowed t)  ; => 42, 2  (valor y dónde paró)
(read-line f nil)          ; => línea, ¿fue por EOF?
(round 2.5)                ; => 2, 0.5
```

En todos, **el primer valor es lo que casi siempre quieres y el segundo es la información
adicional**. Esa asimetría es el diseño: el caso común es corto, y el caso completo está disponible.

La contrapartida honesta: **el compilador no obliga a mirar el segundo valor**. Es el mismo problema
que COBOL con `FILE STATUS` y Go con `err`. Solo Rust lo resolvió, y a costa de obligar siempre.
"""),
        "tcl": ("""
proc dividir {a b} {
    if {$b == 0} {
        return [list 0 "division"]
    }
    return [list [expr {$a / $b}] ""]
}

gets stdin linea
lassign [split [string trim $linea]] a b
lassign [dividir $a $b] r err

if {$err ne ""} {
    puts "err=$err"
} else {
    puts "ok=$r"
}
""", """
**Lo que esta clase enseña en Tcl.** Devolver una **lista de dos elementos** —resultado y error— es el
idioma directo, y `lassign` la desempaqueta en una línea. Es exactamente la tupla de Go, construida
con las piezas normales del lenguaje.

Pero lo interesante es que **Tcl ya tiene errores como valores integrados**, y es `catch` de la clase
anterior:

```tcl
set codigo [catch { operacion } resultado opciones]
```

`catch` **devuelve un número**: 0 si fue bien, 1 si hubo error, y 2, 3 o 4 para `return`, `break` y
`continue`. El resultado o el mensaje van a la segunda variable, y el diccionario de opciones a la
tercera.

Es decir: en Tcl **la excepción y el valor de error son el mismo mecanismo visto de dos maneras**. Un
error se propaga si nadie lo captura, y se convierte en un valor en cuanto alguien pone `catch`. No
hay dos modelos que elegir.

El diccionario de opciones lleva la información estructurada:

```tcl
catch { error "fallo" "" {BANCO SALDO 42} } msg opciones
dict get $opciones -errorcode      ;# {BANCO SALDO 42}
dict get $opciones -errorinfo      ;# la pila
return -options $opciones $msg     ;# RE-LANZAR conservándolo todo
```

Ese último idioma —`return -options` para relanzar sin perder la pila original— resuelve un problema
que en Java exige `throw e;` con cuidado y en Python el `raise ... from ...`. En Tcl es pasar un
diccionario.
"""),
        "perl": ("""
use strict;
use warnings;

sub dividir {
    my ($x, $y) = @_;
    return (undef, 'division') if $y == 0;
    return (int($x / $y), undef);
}

my $linea = <STDIN>;
chomp $linea;
my ($p, $q) = split ' ', $linea;

my ($r, $err) = dividir($p, $q);

if (defined $err) {
    print "err=$err\\n";
} else {
    print "ok=$r\\n";
}
""", """
**Lo que esta clase enseña en Perl.** Devolver una lista de dos elementos es natural porque **las
subrutinas de Perl devuelven listas por defecto**, sin necesidad de construir una tupla ni un objeto.

Y Perl tiene una capacidad que ningún otro lenguaje de esta página comparte: **una función puede saber
en qué contexto la están llamando**, y devolver cosas distintas.

```perl
sub dividir {
    my ($x, $y) = @_;
    return wantarray ? (undef, 'division') : undef  if $y == 0;
    my $r = int($x / $y);
    return wantarray ? ($r, undef) : $r;
}

my $r = dividir(10, 2);              # contexto ESCALAR: solo el resultado
my ($r, $e) = dividir(10, 0);        # contexto de LISTA: resultado y error
```

`wantarray` devuelve verdadero en contexto de lista, falso en contexto escalar y `undef` si el valor
se descarta. Con eso se consigue el mismo efecto que los valores múltiples de Lisp: **el caso común es
corto y el completo está disponible**, sin coste para quien no lo pide.

El modelo clásico de Unix también está presente y es el que usan las funciones del sistema:

```perl
open(my $fh, '<', $f) or die "no puedo: $!";   # falso + $! con el motivo
```

Devolver **falso** y dejar el motivo en la variable global `$!` es el modelo de `errno` de C, y en
Perl convive con las excepciones de la clase 071 y con las listas de este programa. Tres modelos a la
vez, que es muy TMTOWTDI y también una fuente de inconsistencia entre bibliotecas.
"""),
        "cpp": ("""
#include <iostream>
#include <optional>

std::optional<int> dividir(int a, int b) {
    if (b == 0) return std::nullopt;
    return a / b;
}

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    if (const auto r = dividir(a, b)) {
        std::cout << "ok=" << *r << '\\n';
    } else {
        std::cout << "err=division\\n";
    }
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** `std::optional<int>` (C++17) expresa "puede que no haya
resultado", y `if (const auto r = ...)` combina la llamada, la declaración y la comprobación en una
línea. Es el mismo `if err != nil` de Go, con el error dentro del tipo en lugar de al lado.

Lo que le falta a `optional` es **decir por qué falló**, y eso llegó con **C++23**:

```cpp
enum class ErrorDiv { division_por_cero };

std::expected<int, ErrorDiv> dividir(int a, int b) {
    if (b == 0) return std::unexpected(ErrorDiv::division_por_cero);
    return a / b;
}

auto r = dividir(a, b);
if (r) { usar(*r); } else { informar(r.error()); }
```

`std::expected<T, E>` es literalmente el `Result<T, E>` de Rust, adoptado en 2023. Y trae las
operaciones **monádicas** que permiten encadenar sin anidar `if`:

```cpp
auto salida = dividir(a, b)
                .and_then(validar)
                .transform(formatear)
                .value_or("desconocido");
```

Y hay una nota histórica que cierra esta clase: **C++ ya tuvo un modelo de errores como valores y lo
descartó**. `std::error_code` y `std::system_error` (C++11) ofrecían las dos vías, y la biblioteca de
sistema de archivos las expone en pares —`fs::remove(p)` lanza, `fs::remove(p, ec)` devuelve—.

Que un lenguaje con excepciones de treinta años haya añadido `expected` no es que las excepciones
fueran un error: es que **cada modelo sirve para una clase distinta de fallo**. El fallo esperable
—fichero que no está, entrada mal formada— es un valor; el inesperado —memoria agotada, invariante
roto— es una excepción.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi DIVVAL;
  a int(10) const;
  b int(10) const;
end-pi;

dcl-s r      int(10);
dcl-s estado int(10);
dcl-s salida char(40);

if b = 0;
  estado = 1;
  r = 0;
else;
  estado = 0;
  r = %div(a : b);
endif;

if estado <> 0;
  salida = 'err=division';
else;
  salida = 'ok=' + %char(r);
endif;

dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** Este es el modelo nativo de la plataforma, y en IBM i tiene una
forma muy reconocible: **funciones incorporadas que consultan el resultado de la última operación**.

```rpgle
chain (clave) CLIENTES;
if not %found(CLIENTES);       // ¿encontró el registro?
  ...
endif;
if %error;                      // ¿hubo un error de verdad?
  ...
endif;

read CLIENTES;
dow not %eof(CLIENTES);        // ¿fin de fichero?
```

`%found`, `%eof`, `%error`, `%status` y `%equal` **no reciben el resultado como valor de retorno**:
consultan el **estado de la última operación** sobre ese fichero. Es el modelo de `errno` de C, con
funciones en lugar de una variable global.

Tiene la ventaja de que la operación se lee limpia —`chain` no devuelve nada— y el inconveniente
clásico: **hay que preguntar antes de hacer otra cosa**, porque la siguiente operación pisa el estado.

Y RPG tiene una tercera vía, la que se usa cuando el error tiene que cruzar módulos: la **estructura
de datos de estado del programa**, declarada con `psds`, que expone el código de error, el nombre del
programa, la sentencia que falló y la hora. Es introspección del fallo sin excepciones.

En la práctica, un RPG moderno mezcla los tres: `%found`/`%error` para la E/S, `monitor` de la clase
071 para lo excepcional, y códigos de retorno propios entre subprocedimientos.
"""),
        "pli": ("""
 divval: procedure options(main);

    declare (a, b, r) fixed binary(31);
    declare estado    fixed binary(31);

    get list (a, b);
    call dividir(a, b, r, estado);

    if estado ^= 0 then
       put skip list ('err=division');
    else
       put skip list ('ok=' || trim(char(r)));

 dividir: procedure (x, y, res, stat);
    declare (x, y) fixed binary(31);
    declare (res, stat) fixed binary(31);
    if y = 0 then do;
       res = 0;
       stat = 1;
       return;
    end;
    res = divide(x, y, 31);
    stat = 0;
 end dividir;

 end divval;
""", """
**Lo que esta clase enseña en PL/I.** PL/I tiene los dos modelos —las condiciones `ON` de la clase 071
y los códigos de estado de este programa— y su biblioteca los combina de una forma que conviene
conocer: **la condición ocurre igualmente, pero puedes consultarla como dato**.

```pli
on error begin;
   put skip list ('código: ' || oncode());       /* NÚMERO del error */
   put skip list ('en: '     || onloc());        /* dónde ocurrió */
   put skip list ('dato: '   || onsource());     /* el valor que falló */
end;
```

`oncode()` devuelve el código numérico de la condición activa, y con él el manejador puede decidir. Es
introspección del error **dentro** del mecanismo de excepciones — algo que en Java se consigue con
`instanceof` sobre la jerarquía de clases y en Go directamente comprobando el valor.

Y para la E/S, PL/I usa códigos como todos los de esta página:

```pli
declare f file record input;
on undefinedfile(f) ...
on endfile(f) ...
read file(f) into(registro);
```

Fíjate en que las condiciones se declaran **por fichero**, igual que las DECLARATIVES de COBOL. Es el
patrón de la época: cada recurso lleva su manejador.

Y hay una decisión de diseño que PL/I hizo y que conviene señalar: **algunas condiciones están
desactivadas por defecto por rendimiento**, y hay que encenderlas.

```pli
(subscriptrange, stringrange): procedure options(main);   /* prefijos de condición */
```

`SUBSCRIPTRANGE` comprueba los índices de array y **está apagada salvo que la pidas**, porque cuesta.
Es exactamente la misma decisión que `{$R+}` en Pascal y `-fcheck=bounds` en Fortran: la seguridad
disponible, y desactivada por defecto.
"""),
        "mumps": ("""
DIVVAL ; Errores como valores -- clase 072
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 set res = $$dividir(a, b)
 if $piece(res, "^", 1) = "err" write "err=division",! quit
 write "ok=", $piece(res, "^", 2), !
 quit
 ;
dividir(x, y) ; devuelve "ok^valor" o "err^0"
 quit:y=0 "err^0"
 quit "ok^" _ (x\\y)
""", """
**Lo que esta clase enseña en M.** Devolver **`"ok^valor"` o `"err^0"`** —una cadena con delimitador—
es el idioma real de M para los resultados compuestos, y es coherente con todo lo visto en las clases
048 y 065: **la cadena delimitada es la estructura de datos ligera del lenguaje**.

No hay tuplas, no hay registros de retorno y no hay tipos suma. Hay una cadena con `^` en medio, y
`$piece` para leerla. Es exactamente lo mismo que devolver `(valor, error)` en Go, con la diferencia
de que aquí no hay nada que declarar y la comprobación es textual.

Y en los sistemas M de verdad, este patrón está estandarizado por el marco de trabajo. En **VistA**,
la convención de FileMan es devolver el error en un array con estructura fija:

```mumps
 do UPDATE^DIE(.FDA, , , .ERR)
 if $data(ERR) do        ; el array de errores tiene contenido
 . write ERR("DIERR", 1, "TEXT", 1), !
```

Un **array local con subíndices convenidos** que el llamante inspecciona con `$data`. Es la clase 053
aplicada al manejo de errores: no hay `null`, hay un nodo que existe o no existe.

Que un sistema de la escala de VistA —millones de líneas, décadas de mantenimiento— funcione con esta
convención dice algo importante para cerrar la Parte 4: **la disciplina del equipo puede sustituir a
las garantías del lenguaje, y funciona… mientras la disciplina se mantenga**. Ese es exactamente el
argumento que Rust vino a resolver poniendo la comprobación en el compilador.
"""),
        "smalltalk": ("""
| partes a b r |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

r := b = 0 ifTrue: [ nil ] ifFalse: [ a // b ].

Transcript
    show: (r ifNil: [ 'err=division' ] ifNotNil: [ :v | 'ok=', v printString ]);
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Devolver `nil` y comprobarlo con `ifNil:ifNotNil:` es el
modelo directo, y es la clase 053 aplicada aquí. Pero la respuesta idiomática de Smalltalk a esta
clase es otra, y es una de las mejores ideas de la biblioteca: **pasar un bloque para el caso de
fallo**.

```smalltalk
diccionario at: clave ifAbsent: [ 0 ]
coleccion detect: [ :x | ... ] ifNone: [ nil ]
coleccion first ifEmpty: [ 'vacía' ]
numero / cero ifError: [ 0 ]
```

El patrón **`...ifAusente:`** recorre toda la biblioteca, y resuelve el problema de esta clase sin
excepciones, sin códigos de estado y sin tipos suma: **el llamante entrega, en el sitio de la llamada,
qué hacer si no se puede**.

Es más expresivo que devolver `nil` por tres motivos. Primero, **el bloque solo se evalúa si hace
falta**, así que el valor por defecto puede ser caro de calcular. Segundo, puede hacer cualquier cosa
—registrar, lanzar, devolver otro valor— no solo aportar un sustituto. Y tercero, **no hay que
comprobar nada después**: el resultado ya es válido.

Y para la operación sin bloque, la biblioteca ofrece las dos variantes:

```smalltalk
diccionario at: clave                    "lanza si no está"
diccionario at: clave ifAbsent: [ 0 ]    "devuelve el valor por defecto"
```

Es la misma tríada de Delphi —lanzar, valor por defecto, comprobar— que apareció en la ficha de
Pascal, resuelta con bloques en lugar de con tres nombres de función. En un lenguaje donde pasar
código es gratis, la API se diseña así.
"""),
    },
)
