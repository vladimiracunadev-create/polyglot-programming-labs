# -*- coding: utf-8 -*-
"""Parte 5, lote B — clases 079 a 084. Ver `vivos_parte5.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 079 — Paso por valor
# ---------------------------------------------------------------------------
SPECS["079"] = dict(
    gancho="""
Una función que dobla lo que recibe, y una variable del llamante que **no cambia**. Eso es el paso
por valor, y parece la opción evidente hasta que se descubre que **la mitad de estos lenguajes hacen
lo contrario por defecto**: en Fortran, PL/I, RPG y COBOL el paso es **por referencia** salvo que se
diga otra cosa, y esa decisión de los años 50 tiene consecuencias que todavía muerden.
""",
    porque="""
Aquí el concepto es **qué recibe realmente una función**, y estos lenguajes lo enseñan porque
representan la época en que **copiar era caro**. En una máquina de 1957, pasar una copia de un array
de mil elementos era impensable, así que se pasaba la dirección. Por eso Fortran, COBOL, PL/I y RPG
son por referencia por defecto.

Y de ahí sale la trampa histórica más famosa de la informática: en el FORTRAN antiguo se podía pasar
la constante `2` a una subrutina, la subrutina la modificaba, y **a partir de ese momento el literal
`2` valía otra cosa en todo el programa**. No es una leyenda: era el comportamiento real de varios
compiladores.
""",
    cierre="""
Lo transferible: **el defecto de tu lenguaje no es neutral, es una decisión histórica**. Los
lenguajes nacidos cuando la memoria era cara pasan por referencia; los nacidos después pasan por
valor. Y en los modernos con objetos, la respuesta correcta es la tercera: **se pasa por valor una
referencia**, así que reasignar el parámetro no afecta al llamante pero **mutar el objeto sí**. Esa
distinción —valor frente a referencia frente a "valor de una referencia"— explica casi todas las
sorpresas al cambiar de lenguaje.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. PORVALOR.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA    PIC X(80).
01  N        PIC S9(9) COMP-3.
01  LOCAL-N  PIC S9(9) COMP-3.
01  ED-N     PIC -(8)9.
01  ED-L     PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N

    MOVE N TO LOCAL-N          *> la COPIA explícita
    PERFORM DOBLAR-LOCAL

    MOVE N       TO ED-N
    MOVE LOCAL-N TO ED-L
    DISPLAY "original=" FUNCTION TRIM(ED-N)
            " local=" FUNCTION TRIM(ED-L)
    STOP RUN.

DOBLAR-LOCAL.
    COMPUTE LOCAL-N = LOCAL-N * 2.
""", """
**Lo que esta clase enseña en COBOL.** Como los párrafos no tienen parámetros (clase 073), **la copia
hay que hacerla a mano**: `MOVE N TO LOCAL-N`. No hay mecanismo de paso; hay dos variables globales y
una asignación.

Donde COBOL sí decide el mecanismo es en `CALL`, y lo hace **en el sitio de la llamada**, que es
inusual:

```cobol
CALL "SUB" USING BY REFERENCE A     *> el DEFECTO: la dirección
CALL "SUB" USING BY CONTENT   B     *> una COPIA: el llamado no puede tocar B
CALL "SUB" USING BY VALUE     C     *> el valor en sí (COBOL 2002)
```

Que la decisión esté en la llamada y no en la firma tiene una consecuencia interesante: **el mismo
subprograma puede recibir por referencia desde un sitio y por copia desde otro**. Es flexible y hace
imposible saber, leyendo el subprograma, si sus parámetros son seguros.

`BY CONTENT` es la que resuelve esta clase, y existe desde COBOL-85 precisamente porque `BY
REFERENCE` a secas causaba demasiados accidentes: un subprograma que modificaba un campo de entrada
por error corrompía datos del llamante sin ninguna señal.

La regla de estilo moderna es explícita: **poner siempre `BY CONTENT` salvo que se quiera modificar**,
igual que en C++ se pone `const&` salvo que se quiera modificar.
"""),
        "fortran": ("""
program porvalor
   implicit none
   integer :: n

   read(*, *) n

   write(*, '(A,I0,A,I0)') 'original=', n, ' local=', doblar(n)

contains

   pure function doblar(x) result(r)
      integer, value :: x        ! VALUE: copia explícita (el defecto es referencia)
      integer :: r
      r = x * 2
   end function doblar

end program porvalor
""", """
**Lo que esta clase enseña en Fortran.** **En Fortran el paso es por referencia**, siempre lo ha sido,
y el atributo `value` —que fuerza la copia— **no llegó hasta Fortran 2003**.

Esa decisión de 1957 produjo la trampa más citada de la historia de los lenguajes. En los primeros
compiladores, los literales se guardaban en una posición de memoria y **se pasaban por referencia como
cualquier otra cosa**:

```fortran
      CALL DOBLAR(2)      ! se pasa la DIRECCIÓN donde está el literal 2
```

Si `DOBLAR` modificaba su parámetro, **modificaba el literal**. A partir de ahí, `2` valía 4 en todo
el programa, y cualquier `X = 2` posterior asignaba 4. Los compiladores modernos pasan copias
temporales de los literales, pero el mecanismo explica por qué el estándar dice que **modificar un
argumento asociado a una constante es comportamiento indefinido**.

De ahí viene también la obligación práctica de `intent`, de la clase 073: sin él, no hay forma de
saber si una subrutina va a escribir en lo que le pasas.

Y hay un detalle que sigue vivo: **`value` implica que la copia se hace en la entrada**, lo que para
un array grande es carísimo. Por eso `value` se usa casi solo con escalares y para interoperar con C,
donde el paso por valor es el defecto y hay que decirlo:

```fortran
subroutine f(x) bind(c)
   integer(c_int), value :: x      ! obligatorio para que la ABI coincida con C
```
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Porvalor is

   --  `in` es de SOLO LECTURA. Si se pasa por copia o por referencia
   --  lo decide el compilador: no es asunto del programador.
   function Doblar (X : Integer) return Integer is
   begin
      return X * 2;
   end Doblar;

   N : Integer;
begin
   Get (N);

   Put ("original="); Put (N, Width => 1);
   Put (" local=");   Put (Doblar (N), Width => 1);
   New_Line;
end Porvalor;
""", """
**Lo que esta clase enseña en Ada.** Ada hace algo que ningún otro lenguaje de esta página: **separa
la intención del mecanismo**.

`X : Integer` con modo `in` significa **"esta función lee X y no lo modifica"**. Y punto. **El
estándar NO dice si se pasa por copia o por dirección**: lo decide el compilador según el tamaño y el
tipo. Un `Integer` viajará en un registro; un registro de dos kilobytes, por dirección.

Compara con C++, donde hay que elegir a mano:

```cpp
void f(int x);                 // copia -- correcto para un int
void f(const Registro& r);     // referencia constante -- correcto para algo grande
void f(Registro r);            // ¡copia de dos kilobytes!
```

En C++ el programador **tiene que saber** qué es barato de copiar, y equivocarse es una copia
silenciosa. En Ada, esa decisión es del compilador, que la conoce mejor.

El precio es que **Ada no garantiza si dos parámetros pueden ser el mismo objeto**. Si pasas la misma
variable como `in` y como `out`, el resultado es indefinido, porque depende de si el compilador eligió
copia o referencia. El estándar lo dice explícitamente y la práctica es no hacerlo.

Ada 2012 añadió `aliased` y modos de acceso explícitos para los casos en que el mecanismo sí importa
—interoperar con C, o memoria compartida—, pero el modo por defecto sigue siendo declarar la
intención y callarse el resto.
"""),
        "pascal": ("""
program PorValor;
{$MODE OBJFPC}{$H+}
uses SysUtils;

function Doblar(X: Integer): Integer;   { por VALOR: X es una copia }
begin
  X := X * 2;                           { modificar la copia no afecta al llamante }
  Result := X;
end;

var
  N: Integer;

begin
  Read(N);
  WriteLn('original=', IntToStr(N), ' local=', IntToStr(Doblar(N)));
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal **pasa por valor por defecto**, y fue de los primeros
lenguajes en hacerlo — ALGOL 60 y Pascal frente a FORTRAN y COBOL. Wirth consideró que la seguridad
valía la copia.

Y por eso este programa puede escribir `X := X * 2` dentro de la función: **`X` es una copia local**,
modificarla es legal y no afecta a `N`.

El problema del coste llegó con los registros grandes, y Object Pascal lo resolvió con `const`:

```pascal
procedure P(R: TRegistroGrande);        { COPIA todos los bytes }
procedure P(const R: TRegistroGrande);  { por referencia, pero de SOLO LECTURA }
procedure P(var R: TRegistroGrande);    { por referencia, modificable }
```

`const` da exactamente lo que Ada consigue con `in`: la semántica de valor con el coste de la
referencia. La diferencia es que en Pascal lo decide el programador y en Ada el compilador.

Y hay un detalle que conviene conocer: para las **cadenas** (`AnsiString`) el paso por valor **no
copia el texto**, porque son de conteo de referencias con copia al escribir, como se vio en la clase
048. Así que `procedure P(S: string)` es barato, y solo copia si `P` modifica `S`.

Es un caso claro de que "por valor" y "copia" no son sinónimos: **la semántica es de valor y el
mecanismo es de referencia**, con la copia diferida al momento en que hace falta.
"""),
        "lisp": ("""
(defun doblar (x)
  (* x 2))

(let ((n (read)))
  (format t "original=~D local=~D~%" n (doblar n)))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp pasa **por valor**, siempre. Pero el valor de una
variable en Lisp es **una referencia a un objeto**, así que la frase completa es la que importa:
**se pasa por valor una referencia**.

La consecuencia práctica es la que sorprende a todo el mundo la primera vez, y es la misma en Python,
Java, Ruby y JavaScript:

```lisp
(defun reasignar (x) (setf x 99))       ; NO afecta al llamante
(defun mutar (lista) (setf (car lista) 99))  ; SÍ afecta: modifica el OBJETO

(let ((v 1) (l (list 1 2 3)))
  (reasignar v)   ; v sigue valiendo 1
  (mutar l)       ; l ahora es (99 2 3)
  ...)
```

**Reasignar el parámetro no se ve fuera; mutar el objeto apuntado sí.** No es paso por referencia: es
que ambos nombres apuntan al mismo objeto.

Esa distinción es la fuente de la mitad de las discusiones sobre "¿Java pasa por valor o por
referencia?" —la respuesta es por valor, de referencias— y Lisp la hace especialmente visible porque
sus estructuras son mutables por defecto.

Los números y los caracteres en Lisp son **inmutables**, así que con ellos la distinción no se nota:
no hay forma de mutar el 5. Es exactamente lo que hace que en Python `int` y `str` "parezcan" por
valor y las listas no.
"""),
        "tcl": ("""
proc doblar {x} {
    set x [expr {$x * 2}]      ;# x es una COPIA local
    return $x
}

gets stdin linea
set n [string trim $linea]

puts "original=$n local=[doblar $n]"
""", """
**Lo que esta clase enseña en Tcl.** Tcl pasa **por valor**, y con una particularidad: como todos los
valores son inmutables a nivel semántico, **el paso por valor es barato aunque el valor sea enorme**.

Internamente, Tcl no copia: comparte la representación y **incrementa un contador de referencias**.
Solo se copia si alguien modifica el valor y hay más de una referencia — la **copia al escribir** que
ya apareció en Pascal y en PHP.

```tcl
set grande [lrepeat 1000000 x]
doblar $grande        ;# NO copia un millón de elementos: comparte y cuenta
```

Eso permite que Tcl tenga semántica de valor pura —nadie te cambia un dato por detrás— sin el coste
que eso tendría en C++.

Y es la razón de que la optimización de la clase 054 funcione: `lappend lista x` modifica **en el
sitio** cuando el contador de referencias es 1, y copia cuando es mayor. El programador ve siempre
semántica de valor; la implementación decide.

Cuando de verdad hace falta modificar la variable del llamante, Tcl no cambia el mecanismo de paso:
usa **`upvar`**, que liga un nombre local a una variable del llamante por su **nombre**. Es la clase
080.
"""),
        "perl": ("""
use strict;
use warnings;

sub doblar {
    my ($x) = @_;              # la COPIA: sin esta línea, @_ sería un alias
    $x = $x * 2;
    return $x;
}

my $n = <STDIN>;
chomp $n;

print "original=$n local=", doblar($n), "\\n";
""", """
**Lo que esta clase enseña en Perl.** El comentario del código es la clase entera: **`@_` NO es una
copia de los argumentos, son alias de las variables originales**.

```perl
sub doblar_mal { $_[0] *= 2 }      # MODIFICA la variable del llamante
my $n = 5;
doblar_mal($n);                     # ¡$n ahora vale 10!
```

Perl es, por tanto, **por referencia por defecto**, como Fortran y COBOL — y casi nadie lo sabe,
porque el idioma universal `my ($x) = @_;` **hace la copia en la primera línea** y borra el efecto.

Esa línea, que parece burocracia, es lo único que separa a Perl del comportamiento de Fortran.

El aliasing tiene usos legítimos, y algunas funciones del núcleo lo aprovechan: `chomp` y `chop` sobre
`$_[0]`, o las funciones que modifican en el sitio para evitar copias en bucles muy calientes.

Y con las **firmas** de 5.36, el problema desaparece: los parámetros de una firma **son copias**.

```perl
use v5.36;
sub doblar ($x) { $x *= 2; return $x }     # $x es una copia; @_ ni se usa
```

Ese es uno de los argumentos más fuertes a favor de usar firmas en Perl moderno: además de comprobar
la aridad, **eliminan el aliasing accidental**, que era una de las trampas más difíciles de depurar
del lenguaje.
"""),
        "cpp": ("""
#include <iostream>

int doblar(int x) {       // por VALOR: x es una copia
    x *= 2;
    return x;
}

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "original=" << n << " local=" << doblar(n) << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ pasa **por valor por defecto**, heredado de C, y toda la
dificultad está en decidir cuándo eso es correcto. La guía moderna cabe en una tabla:

| Firma | Cuándo |
|---|---|
| `void f(int x)` | Tipos pequeños: enteros, punteros, `std::string_view` |
| `void f(const T& x)` | Solo lectura de algo grande |
| `void f(T& x)` | Se va a modificar, y el llamante debe verlo |
| `void f(T&& x)` | Se va a **consumir** — clase 081 |
| `void f(T x)` | Se va a **quedar** con una copia propia |

Esa última fila es la sutil, y es la que cambió con C++11: **si la función va a guardar el argumento,
tomarlo por valor es lo correcto**, porque el llamante puede pasarlo con `std::move` y entonces no hay
copia ninguna.

```cpp
class Persona {
    std::string nombre;
public:
    explicit Persona(std::string n) : nombre(std::move(n)) {}   // por VALOR + move
};
Persona p{"Ada"};                     // el temporal se MUEVE, cero copias
```

Antes de C++11, ese constructor habría necesitado dos versiones —`const&` y otra—. Con la semántica de
movimiento, una sola firma cubre los dos casos de forma óptima.

Y el aviso de siempre: **`void f(std::vector<int> v)` copia el vector entero**, en silencio, y el
compilador no avisa. Es el error de rendimiento más común en C++, y `-Wall` no lo detecta porque no
es un error: es una decisión.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi PORVALOR;
  n int(10) const;
end-pi;

dcl-s salida char(50);

salida = 'original=' + %char(n)
       + ' local='   + %char(doblar(n));
dsply salida;

*inlr = *on;
return;

dcl-proc doblar;
  dcl-pi *n int(10);
    x int(10) value;      // VALUE: copia. Sin esto sería por referencia.
  end-pi;
  x = x * 2;              // modifica la copia
  return x;
end-proc;
""", """
**Lo que esta clase enseña en RPG.** **RPG pasa por referencia por defecto**, como COBOL, Fortran y
PL/I, y por la misma razón histórica.

Las tres formas se declaran en la firma:

```rpgle
dcl-pi *n;
  a int(10);          // POR REFERENCIA (el defecto): se puede modificar
  b int(10) const;    // por referencia, pero de SOLO LECTURA
  c int(10) value;    // por VALOR: una copia
end-pi;
```

`const` es la que se recomienda para casi todo, y tiene una ventaja que va más allá de la seguridad:
**permite pasar expresiones**.

```rpgle
resultado = calcular(a + b);     // solo compila si el parámetro es const o value
resultado = calcular(a);         // sin const, hay que pasar una VARIABLE
```

Sin `const`, RPG necesita una dirección de memoria que modificar, así que `a + b` no vale. Con `const`
o `value`, el compilador crea el temporal. Es exactamente el mismo motivo por el que en C++ solo se
puede ligar un temporal a un `const&` y no a un `&`.

Y hay un caso peligroso propio de RPG: **si los tipos no coinciden exactamente y el parámetro no es
`const`, el compilador puede crear un temporal sin avisar**, así que la modificación se pierde. Es la
misma trampa que el *dummy argument* de PL/I y Fortran, y la razón de que la guía sea declarar
siempre el modo.
"""),
        "pli": ("""
 porvalor: procedure options(main);

    declare n fixed binary(31);

    get list (n);

    put skip list ('original=' || trim(char(n)) ||
                   ' local='   || trim(char(doblar((n)))));   /* ((n)) fuerza la COPIA */

 doblar: procedure (x) returns (fixed binary(31));
    declare x fixed binary(31);
    x = x * 2;
    return (x);
 end doblar;

 end porvalor;
""", """
**Lo que esta clase enseña en PL/I.** Los **dobles paréntesis** de `doblar((n))` no son un error
tipográfico: son **el idioma de PL/I para forzar el paso por valor**, y merecen explicación.

PL/I pasa **por referencia** por defecto. Pero cuando el argumento es una **expresión** en lugar de
una variable, el compilador tiene que evaluarla en algún sitio, así que crea una variable temporal
—un *dummy argument*— y pasa **su** dirección.

Y `(n)` con paréntesis extra **es una expresión**, no una variable. Así que:

```pli
call p(n);      /* por referencia: p puede modificar n */
call p((n));    /* por VALOR: se pasa una copia temporal */
```

Un par de paréntesis cambia el mecanismo de paso. Es de las cosas menos evidentes de PL/I y aparece
en código real sin ningún comentario.

Fortran tiene **exactamente el mismo truco** y por el mismo motivo, lo que no es casualidad: los dos
lenguajes vienen de la misma época y del mismo razonamiento sobre el coste de copiar.

La lección de diseño es la que ya apuntaba la ficha de Ada: **cuando el mecanismo de paso depende de
la forma sintáctica del argumento en el sitio de la llamada, nadie puede saber qué pasa leyendo solo
la declaración**. Por eso todos los lenguajes posteriores movieron esa decisión a la firma.
"""),
        "mumps": ("""
PORVALOR ; Paso por valor -- clase 079
 read n
 write "original=", n, " local=", $$doblar(n), !
 quit
 ;
doblar(x) ; devuelve el doble; x es una COPIA
 set x = x * 2
 quit x
""", """
**Lo que esta clase enseña en M.** M pasa **por valor por defecto**, lo que sorprende en un lenguaje
de 1966: la mayoría de sus contemporáneos hacían lo contrario.

Y el paso por referencia existe, pero hay que **pedirlo en el sitio de la llamada, con un punto**:

```mumps
 do PROC^RUT(a)       ; por VALOR
 do PROC^RUT(.a)      ; por REFERENCIA
```

Ese punto delante del nombre es la marca. Es la misma decisión que COBOL con `BY REFERENCE` —el
mecanismo lo elige quien llama— y tiene la misma consecuencia: **leyendo la rutina llamada no se sabe
si sus parámetros son seguros**.

Lo interesante es lo que M puede pasar por referencia: **arrays completos con toda su jerarquía de
subíndices**.

```mumps
 do CARGAR^DATOS(.pacientes)
 ; y ahora pacientes(1,"nombre"), pacientes(2,"alergias",1)... están rellenos
```

Eso no es un puntero a una estructura: es acceso al **árbol local completo**, que la rutina llamada
puede recorrer con `$order`, ampliar y borrar. Es el mecanismo con el que están escritas todas las
APIs de VistA y FileMan, y la razón de que M no necesite tipos de retorno complejos.

Y como se vio en la clase 069, dentro de la rutina hay que usar `new` para las temporales: sin él,
serían globales y se pisarían entre llamadas.
"""),
        "smalltalk": ("""
| n |

n := stdin nextLine trimBoth asNumber.

Transcript
    show: 'original=', n printString;
    show: ' local=', (n * 2) printString;
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk pasa **por valor**, y como en Lisp la frase
completa es: **por valor de una referencia**. Todo argumento es un puntero a un objeto, copiado al
pasarlo.

```smalltalk
metodo: unObjeto
    unObjeto := OtraCosa new.     "solo cambia la variable LOCAL"
    unObjeto add: 42.              "MODIFICA el objeto que ve el llamante"
```

La primera línea no se ve fuera; la segunda sí. Es exactamente la distinción de la ficha de Lisp.

Y hay una regla del lenguaje que refuerza esto y que no tiene equivalente: **los parámetros de un
método son constantes**. Asignar a un parámetro **no compila**:

```smalltalk
metodo: x
    x := x + 1.       "ERROR de compilación: no se puede asignar a un argumento"
```

Es una decisión deliberada y muy sensata: reasignar un parámetro es una fuente clásica de confusión
—el nombre deja de significar lo que decía la firma— y Smalltalk simplemente lo prohíbe. Hay que
declarar una temporal.

Java añadió `final` en los parámetros para conseguir lo mismo, opcionalmente. C++ tiene `const T x`.
Smalltalk lo hizo obligatorio en los años 70.

Y los números son **inmutables**, así que con ellos la distinción valor/referencia es invisible: no
existe forma de mutar el objeto `5`.
"""),
    },
)

# ---------------------------------------------------------------------------
# 080 — Paso por referencia
# ---------------------------------------------------------------------------
SPECS["080"] = dict(
    gancho="""
Ahora al revés: una función que **modifica la variable del llamante**. Es lo contrario de la clase
anterior y, en la mitad de estos lenguajes, **es lo que pasa si no haces nada**. La pregunta
interesante no es cómo se consigue, sino **dónde se declara**: ¿en la firma, donde lo ve quien
implementa, o en la llamada, donde lo ve quien usa?
""",
    porque="""
Aquí el concepto es la **mutación del argumento**, y estos lenguajes se reparten en dos escuelas.
**En la firma**: Fortran con `intent(inout)`, Ada con `in out`, Pascal con `var`, C++ con `&`. **En la
llamada**: COBOL con `BY REFERENCE` y M con el punto delante del argumento.

La segunda escuela es hoy minoritaria y tiene una consecuencia grave: **leyendo el subprograma no se
sabe si sus parámetros son seguros**, porque depende de cómo lo invoquen. Y leyendo la llamada tampoco
se sabe si el subprograma va a modificar algo. La información está partida en dos sitios.
""",
    cierre="""
Lo transferible: **si el lenguaje permite mutar argumentos, la firma debe decirlo**. Es la misma
regla que la clase 073 sobre los modos, y la razón de que Fortran y Ada insistan tanto en `intent` y
en `in out`. Y en los lenguajes sin paso por referencia —Lisp, Smalltalk, Java, Python— el sustituto
es siempre el mismo: **envolver el valor en un objeto mutable**, que es exactamente lo que hace este
programa en Lisp con una lista de un elemento.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. PORREF.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9) COMP-3.
01  ANTES   PIC S9(9) COMP-3.
01  ED-A    PIC -(8)9.
01  ED-D    PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N
    MOVE N TO ANTES

    PERFORM DOBLAR             *> modifica N: los párrafos comparten TODO

    MOVE ANTES TO ED-A
    MOVE N     TO ED-D
    DISPLAY "antes=" FUNCTION TRIM(ED-A)
            " despues=" FUNCTION TRIM(ED-D)
    STOP RUN.

DOBLAR.
    COMPUTE N = N * 2.
""", """
**Lo que esta clase enseña en COBOL.** Un párrafo **siempre** trabaja sobre las variables globales, así
que en cierto sentido **todo COBOL es paso por referencia llevado al extremo**: no hay parámetros que
pasar porque no hay nada privado.

Para los subprogramas, COBOL declara el mecanismo **en la llamada**:

```cobol
CALL "SUB" USING BY REFERENCE A     *> el DEFECTO: SUB puede modificar A
```

Y el subprograma recibe las direcciones en su **`LINKAGE SECTION`**, que es una sección de datos
especial: **declara la forma de algo que vive en otro programa**.

```cobol
DATA DIVISION.
LINKAGE SECTION.
01  PARAM-A  PIC S9(9) COMP-3.

PROCEDURE DIVISION USING PARAM-A.
    COMPUTE PARAM-A = PARAM-A * 2.     *> escribe en la memoria del LLAMANTE
```

La `LINKAGE SECTION` **no reserva memoria**: describe la forma de un dato ajeno. Si el llamante pasa
un campo con otra `PIC`, el subprograma lo interpreta con la suya y el resultado es basura, **sin
ningún error**. No hay comprobación de tipos entre programas compilados por separado.

Ese es uno de los fallos más difíciles de diagnosticar del mundo COBOL, y la razón de que los
copybooks de la clase 052 sean tan importantes: **compartir la definición es la única garantía de que
los dos lados coincidan**.
"""),
        "fortran": ("""
program porref
   implicit none
   integer :: n, antes

   read(*, *) n
   antes = n

   call doblar(n)          ! por referencia: modifica n

   write(*, '(A,I0,A,I0)') 'antes=', antes, ' despues=', n

contains

   pure subroutine doblar(x)
      integer, intent(inout) :: x     ! ENTRADA Y SALIDA, declarado
      x = x * 2
   end subroutine doblar

end program porref
""", """
**Lo que esta clase enseña en Fortran.** El paso por referencia es **el defecto**, así que `intent`
no cambia el mecanismo: **cambia lo que está permitido hacer**.

| `intent` | Se puede leer | Se puede escribir | El compilador… |
|---|---|---|---|
| `in` | Sí | **No** | Rechaza la escritura |
| `out` | **No** (el valor entrante no cuenta) | Sí | Avisa si se lee antes de asignar |
| `inout` | Sí | Sí | |

Es documentación **comprobada**, y es lo único que hace legible una interfaz en un lenguaje donde
todo se pasa por dirección.

Y hay una regla de Fortran que no tiene ningún lenguaje del núcleo y que es la razón de su
rendimiento: **está prohibido que dos argumentos de una subrutina se solapen en memoria**.

```fortran
call procesar(v, v)        ! ILEGAL si procesar modifica alguno
call procesar(v(1:50), v(40:90))   ! ILEGAL: se solapan
```

El estándar lo prohíbe y **el compilador puede asumir que no ocurre**, lo que le permite reordenar y
vectorizar libremente. En C, dos punteros pueden apuntar a lo mismo y el compilador debe suponer lo
peor — de ahí que C99 tuviera que inventar `restrict` para recuperar a mano lo que Fortran tiene de
serie.

Es exactamente lo que la ficha de la clase 043 anunciaba, aquí en su forma concreta: **la ausencia de
solapamiento es una obligación del programador y una licencia para el optimizador**.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Porref is

   procedure Doblar (X : in out Integer) is
   begin
      X := X * 2;
   end Doblar;

   N, Antes : Integer;
begin
   Get (N);
   Antes := N;

   Doblar (N);

   Put ("antes=");     Put (Antes, Width => 1);
   Put (" despues=");  Put (N, Width => 1);
   New_Line;
end Porref;
""", """
**Lo que esta clase enseña en Ada.** `in out` declara la intención, y el compilador sigue eligiendo el
mecanismo — copia de entrada y salida, o dirección — como se vio en la clase 079.

Eso tiene una consecuencia que conviene conocer y que Ada documenta explícitamente: **si el mismo
objeto se pasa dos veces, el resultado no está definido**.

```ada
Intercambiar (A, A);        --  el estándar NO dice qué pasa
```

Con paso por dirección, las dos referencias son la misma. Con copia de entrada y salida, la segunda
copia de vuelta pisa a la primera. Como el estándar no fija el mecanismo, no puede fijar el
resultado. Es el mismo problema del solapamiento de Fortran, expresado a nivel de parámetros.

Y **`out` en Ada no es lo mismo que en Pascal o C#**: en Ada, un parámetro `out` de un tipo escalar
**entra sin valor definido**, y leerlo antes de asignarlo es un error que el compilador detecta. Para
tipos compuestos con partes discriminantes, sí conserva parte de la información — un matiz que está en
el manual de referencia y que casi nadie conoce.

Ada 2012 permite además `in out` en **funciones**, cosa prohibida hasta entonces. Fue una concesión
discutida: la restricción original empujaba hacia funciones puras, y levantarla facilitó la
interoperabilidad a cambio de perder esa garantía.
"""),
        "pascal": ("""
program PorRef;
{$MODE OBJFPC}{$H+}
uses SysUtils;

procedure Doblar(var X: Integer);      { VAR: por referencia }
begin
  X := X * 2;
end;

var
  N, Antes: Integer;

begin
  Read(N);
  Antes := N;

  Doblar(N);

  WriteLn('antes=', IntToStr(Antes), ' despues=', IntToStr(N));
end.
""", """
**Lo que esta clase enseña en Pascal.** **`var` es la palabra que inventó el paso por referencia
declarado en la firma**, y de ahí la copiaron C# (`ref`), Object Pascal, Modula-2 y Ada (con otro
nombre).

Antes de Pascal, la elección estaba en la llamada —COBOL— o no había elección —FORTRAN—. ALGOL 60
tenía el paso por **nombre**, que era aún más raro: el argumento se reevaluaba en cada uso, lo que
producía el célebre *dispositivo de Jensen* y una cantidad notable de confusión.

Wirth simplificó a dos modos, y ese par —por valor o `var`— es el que ha sobrevivido.

Object Pascal añadió después `const` y `out`, con lo que quedan cuatro:

```pascal
procedure P(A: Integer);          { valor }
procedure P(var A: Integer);      { referencia, lectura y escritura }
procedure P(const A: TGrande);    { referencia, solo lectura }
procedure P(out A: Integer);      { referencia, solo escritura }
```

Y hay una restricción de `var` que conviene conocer: **el argumento debe ser una variable, no una
expresión**, y **su tipo debe coincidir exactamente**. `Doblar(N + 0)` no compila, y `Doblar(B)` con
`B: Byte` tampoco, aunque `Byte` quepa en `Integer`.

Esa rigidez es deliberada: si el compilador aceptara una conversión, tendría que crear un temporal, y
entonces la modificación se perdería — el *dummy argument* de PL/I y Fortran. Pascal lo prohíbe en
lugar de permitirlo en silencio.
"""),
        "lisp": ("""
(defun doblar (celda)
  (setf (car celda) (* 2 (car celda))))   ; muta el OBJETO, no la variable

(let* ((n (read))
       (caja (list n)))                   ; una "caja": lista de un elemento
  (doblar caja)
  (format t "antes=~D despues=~D~%" n (car caja)))
""", """
**Lo que esta clase enseña en Common Lisp.** **Lisp no tiene paso por referencia**, y este programa
muestra el sustituto universal: **envolver el valor en un objeto mutable**.

`(list n)` crea una caja de un elemento. La función recibe la caja —por valor, como siempre— y muta su
contenido con `(setf (car celda) ...)`. El llamante ve el cambio porque **ambos apuntan al mismo
objeto**.

Es exactamente lo que se hace en Java con un array de un elemento, en Python con una lista, en Go con
un puntero y en JavaScript con un objeto. **Cuando un lenguaje no tiene referencias, la caja es el
patrón.**

Y `setf` merece un apunte, porque es una de las mejores ideas de Common Lisp: **funciona sobre
cualquier "lugar"**, no solo sobre variables.

```lisp
(setf x 1)                       ; una variable
(setf (car lista) 1)             ; el primer elemento
(setf (aref v 3) 1)              ; un elemento de array
(setf (gethash k tabla) 1)       ; una entrada de tabla hash
(setf (slot-value obj 'campo) 1) ; un campo de objeto
(setf (symbol-function 'f) g)    ; ¡la definición de una función!
```

Todos son "lugares" que se pueden leer y escribir, y `setf` es la macro que sabe cómo escribir en cada
uno. Se pueden definir lugares nuevos con `defsetf` y `define-setf-expander`, así que **una estructura
propia puede participar en `setf`** como si fuera nativa.

Es generalización llevada al límite: en vez de un operador de asignación, un protocolo de asignación
extensible.
"""),
        "tcl": ("""
proc doblar {nombreVar} {
    upvar 1 $nombreVar x        ;# liga x a la variable del LLAMANTE
    set x [expr {$x * 2}]
}

gets stdin linea
set n [string trim $linea]
set antes $n

doblar n                        ;# se pasa el NOMBRE, no el valor

puts "antes=$antes despues=$n"
""", """
**Lo que esta clase enseña en Tcl.** Fíjate en la llamada: **`doblar n`, sin el `$`**. No se pasa el
valor: se pasa **el nombre de la variable**, como una cadena.

`upvar 1 $nombreVar x` liga la variable local `x` a la variable llamada así en el nivel de pila
indicado —`1` es el llamante, `2` el llamante del llamante, `#0` el nivel global—. A partir de ahí,
`x` **es** la variable del otro.

Es paso por referencia obtenido **sin punteros y sin referencias**: en Tcl las variables se resuelven
por nombre en tiempo de ejecución, así que basta con pasar el nombre.

Y ese mecanismo es la base de toda la extensibilidad del lenguaje. Los comandos del propio Tcl que
dejan resultados en variables —`scan`, `regexp`, `binary scan`, `lassign`, `catch`— están
implementados así, y por eso un procedimiento de usuario puede imitarlos exactamente.

Su hermano es **`uplevel`**, que ya apareció en la clase 041: **evalúa código en el ámbito del
llamante**. Con `upvar` y `uplevel` juntos se pueden escribir estructuras de control propias que se
comportan como las nativas:

```tcl
proc repetir {n cuerpo} {
    for {set i 1} {$i <= $n} {incr i} { uplevel 1 $cuerpo }
}
```

La contrapartida es la de siempre: **el nombre viaja como una cadena, así que nadie comprueba nada**.
Un error de escritura en el nombre crea una variable nueva en el ámbito del llamante.
"""),
        "perl": ("""
use strict;
use warnings;

sub doblar {
    $_[0] *= 2;              # @_ contiene ALIAS: esto modifica al llamante
}

my $n = <STDIN>;
chomp $n;
my $antes = $n;

doblar($n);

print "antes=$antes despues=$n\\n";
""", """
**Lo que esta clase enseña en Perl.** Esta es la cara oculta de la clase 079: **`@_` contiene alias de
los argumentos originales**, así que modificar `$_[0]` **modifica la variable del llamante**.

Perl es, por tanto, **por referencia por defecto**, y la copia es opt-in con `my ($x) = @_;`.

Ese comportamiento tiene usos legítimos y muy usados en el propio núcleo:

```perl
chomp($linea);      # modifica $linea en el sitio
chop($s);
s/a/b/ for @lista;  # modifica CADA elemento de @lista
```

Y `for` y `map` tienen el mismo aliasing, como se vio en las clases 064 y 067.

La forma **explícita** de pasar por referencia, y la que se usa cuando la intención debe verse, son
las referencias:

```perl
doblar(\\$n);                    # se pasa una REFERENCIA
sub doblar { my ($ref) = @_; $$ref *= 2 }
```

`\\$n` crea la referencia y `$$ref` la desreferencia. Es más verboso y **se ve en el sitio de la
llamada**, que es exactamente la ventaja: quien lee `doblar(\\$n)` sabe que `$n` puede cambiar, y quien
lee `doblar($n)` supone que no — aunque técnicamente pueda.

Con **firmas** (5.36) el aliasing desaparece: los parámetros de una firma son copias, así que la única
forma de modificar al llamante pasa a ser la referencia explícita. Es una mejora de legibilidad
importante.
"""),
        "cpp": ("""
#include <iostream>

void doblar(int& x) {      // REFERENCIA: modifica la variable del llamante
    x *= 2;
}

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    const int antes = n;
    doblar(n);

    std::cout << "antes=" << antes << " despues=" << n << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** `int&` es una **referencia**, y su diferencia con el puntero de C
es la que da la lección:

| | Puntero `int*` | Referencia `int&` |
|---|---|---|
| Puede ser nulo | Sí | **No** |
| Se puede reasignar | Sí | **No**: se liga una vez |
| Sintaxis en el uso | `*p = 1` | `x = 1` |
| Sintaxis en la llamada | `f(&n)` | `f(n)` |

La última fila es la discutida: **en el sitio de la llamada, `doblar(n)` no revela que `n` puede
cambiar**. En C había que escribir `doblar(&n)`, y esa marca era información. C++ la perdió a cambio
de sintaxis limpia.

Por eso las *Core Guidelines* recomiendan: **si una función modifica un argumento, pásalo por puntero
o devuélvelo**, precisamente para que se vea en la llamada. Google llegó a prohibir las referencias no
constantes en su guía de estilo por este motivo, y años después relajó la norma.

Es el mismo debate de COBOL y M —¿la marca va en la firma o en la llamada?— con la respuesta de que lo
ideal sería en las dos.

Y C++11 añadió un tercer tipo de referencia, `int&&`, que es la clase siguiente: no significa
"modificable", significa **"consumible"**.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi PORREF;
  n int(10);          // SIN const ni value: por referencia (el defecto)
end-pi;

dcl-s antes  int(10);
dcl-s salida char(50);

antes = n;
doblar(n);            // modifica n

salida = 'antes=' + %char(antes) + ' despues=' + %char(n);
dsply salida;

*inlr = *on;
return;

dcl-proc doblar;
  dcl-pi *n;
    x int(10);        // por referencia
  end-pi;
  x = x * 2;
end-proc;
""", """
**Lo que esta clase enseña en RPG.** El paso por referencia es **el defecto**, y basta con **no
escribir nada**: un parámetro sin `const` ni `value` es modificable y el cambio se ve fuera.

Ese defecto es el origen de un problema real de mantenimiento en RPG: **un subprocedimiento que
modifica un parámetro por error corrompe datos del llamante sin ninguna señal**, igual que en COBOL y
Fortran antes de `intent`.

Por eso la guía de estilo de la plataforma es tajante: **`const` en todo lo que sea de entrada**,
siempre, aunque sea más largo de escribir.

RPG tiene además dos cosas relacionadas que conviene conocer. La primera, **`options(*varsize)`**, que
permite pasar un campo más corto que el declarado:

```rpgle
dcl-pi *n;
  texto char(1000) options(*varsize);
  largo int(10) const;                  // y el llamante dice cuánto mide de verdad
end-pi;
```

Sin `*varsize`, RPG exige que el argumento mida exactamente lo declarado. Con él, se pasa la dirección
y el tamaño real viaja aparte — el mismo `char* + size_t` de C, con los mismos riesgos.

La segunda: **`%addr()`**, que da la dirección de una variable, y las variables `based(puntero)` de la
clase 078. Con ellas se puede hacer aritmética de punteros en RPG, y se usa para las APIs del sistema.
"""),
        "pli": ("""
 porref: procedure options(main);

    declare (n, antes) fixed binary(31);

    get list (n);
    antes = n;

    call doblar(n);        /* por REFERENCIA: es el defecto */

    put skip list ('antes=' || trim(char(antes)) ||
                   ' despues=' || trim(char(n)));

 doblar: procedure (x);
    declare x fixed binary(31);
    x = x * 2;
 end doblar;

 end porref;
""", """
**Lo que esta clase enseña en PL/I.** El paso por referencia es el defecto y **no hay forma de
declararlo en la firma**: cualquier parámetro es modificable, y lo único que fuerza la copia son los
paréntesis extra en el sitio de la llamada, como se vio en la clase 079.

Esa ausencia —no poder decir "este parámetro es de entrada"— es una de las carencias más claras de
PL/I frente a Fortran 90 y Ada, y se nota en el mantenimiento: **para saber qué modifica un
procedimiento hay que leer su cuerpo entero**.

Lo que PL/I sí tiene, y es donde el paso por referencia se vuelve realmente potente, es la
combinación con las **variables `based`** de la clase 053:

```pli
declare p pointer;
declare v(1000) fixed binary(31) based(p);

p = addr(datos);          /* apunta a otra cosa */
v(5) = 99;                /* escribe en datos, con OTRA forma */
```

`based` permite **reinterpretar cualquier zona de memoria con la forma que quieras**, y `addr` da la
dirección de cualquier variable. Con eso se escribió Multics, y con eso se puede corromper cualquier
cosa.

Es coherente con el resto del lenguaje: PL/I da las herramientas de un lenguaje de sistemas y las
comodidades de uno de aplicación, sin separar las dos cosas. Fue una decisión valiente para 1964 y es
la razón de que hoy se cite como ejemplo de lo que no hay que hacer.
"""),
        "mumps": ("""
PORREF ; Paso por referencia -- clase 080
 read n
 set antes = n
 do doblar(.n)                 ; el PUNTO: por referencia
 write "antes=", antes, " despues=", n, !
 quit
 ;
doblar(x) ; dobla x en el sitio
 set x = x * 2
 quit
""", """
**Lo que esta clase enseña en M.** **El punto delante del argumento —`.n`— es todo el mecanismo.** Sin
él, por valor; con él, por referencia. La decisión está **en el sitio de la llamada**, como en COBOL.

Y lo que hace único a M es **qué** se puede pasar así: no una variable, sino **un árbol local
completo**.

```mumps
 kill pacientes
 do CARGAR^DATOS(.pacientes)
 ;
CARGAR(res) ;
 set res(1,"nombre") = "Ada"
 set res(1,"edad") = 36
 set res(2,"nombre") = "Grace"
 quit
```

La rutina llamada **crea la estructura entera** en el array del llamante: subíndices, niveles y todo.
Al volver, `pacientes(1,"nombre")` existe.

Eso convierte el paso por referencia en el mecanismo de retorno de estructuras del lenguaje, y explica
la forma de todas las APIs de VistA: **no devuelven objetos, rellenan arrays**.

Hay un detalle que conviene conocer y que causa errores: **el punto solo se puede poner sobre un
nombre de variable simple**, no sobre un subíndice ni una expresión. `do P(.a(1))` no es legal. Para
pasar un subárbol hay que copiarlo primero con `merge`:

```mumps
 merge temporal = pacientes(1)      ; MERGE copia un subárbol completo
 do P(.temporal)
```

`merge` es otro comando propio de M sin equivalente directo: copia un nodo **y todos sus
descendientes** de una estructura a otra, local o global, en una sola operación.
"""),
        "smalltalk": ("""
| n caja |

n := stdin nextLine trimBoth asNumber.
caja := OrderedCollection with: n.        "una 'caja' mutable"

caja at: 1 put: (caja first * 2).

Transcript
    show: 'antes=', n printString;
    show: ' despues=', caja first printString;
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** **Smalltalk no tiene paso por referencia**, y no puede
tenerlo: los parámetros son constantes (clase 079) y los números son inmutables.

El sustituto es el mismo que en Lisp: **una caja**, un objeto mutable que contiene el valor. Aquí una
`OrderedCollection`; en código real sería una instancia de `ValueHolder`, una clase de la biblioteca
pensada exactamente para esto.

```smalltalk
| holder |
holder := ValueHolder new.
holder value: 5.
modificar: holder.          "el método puede hacer holder value: 10"
holder value.                "10"
```

`ValueHolder` es más que un truco: es la pieza central del patrón **Observador** en Smalltalk. Un
`ValueHolder` puede **notificar a quien esté escuchando** cuando su contenido cambia, y sobre eso se
construyó toda la capa de enlace de datos de VisualWorks — el antepasado del *data binding* que hoy
tienen Angular, Vue y SwiftUI.

Es un buen cierre para esta clase: **la carencia de paso por referencia empujó a Smalltalk a
convertir "un valor que cambia" en un objeto de primera clase**, y de ahí salió una idea que la
industria adoptó cuarenta años después con otro nombre.

Y en la práctica, la pregunta rara vez se plantea: como los objetos son referencias, un método que
recibe una colección o un modelo **ya puede modificarlo**. La caja solo hace falta para los
inmutables.
"""),
    },
)

# ---------------------------------------------------------------------------
# 081 — Semántica de movimiento y préstamo (Rust)
# ---------------------------------------------------------------------------
SPECS["081"] = dict(
    gancho="""
Una palabra, su longitud, y la pregunta que Rust puso en el centro de la conversación en la última
década: **¿quién es el dueño de este dato y cuándo se libera?** La respuesta de Rust —propiedad,
movimiento y préstamo comprobados por el compilador— parece nueva. Y sin embargo **Fortran tiene una
operación de movimiento desde 2003** y **C++ construyó la suya en 2011**.
""",
    porque="""
Aquí el concepto es la **propiedad de un recurso**, y estos lenguajes lo enseñan porque muestran las
tres estrategias históricas. **Gestión manual**: C++ antes de 2011, donde copiar era la única forma
segura y el rendimiento se pagaba en copias. **Recolección de basura**: Lisp, Smalltalk, Tcl, Perl y
M, donde la pregunta desaparece a cambio de pausas impredecibles. Y **conteo de referencias con copia
al escribir**: Pascal, Tcl y Perl, donde el dato se comparte hasta que alguien lo toca.

Y hay dos hallazgos concretos: **`move_alloc` de Fortran 2003 es literalmente un movimiento**, y
**Ada tiene tipos controlados** con `Adjust` y `Finalize`, que son los constructores de copia y
destructores de C++ con otro nombre.
""",
    cierre="""
Lo transferible: **"quién libera esto" es una pregunta que todo programa responde, explícita o
implícitamente**. Rust la puso en el sistema de tipos; C++ la puso en los destructores y la semántica
de movimiento; los lenguajes con recolector la delegaron en el runtime; y COBOL, RPG y Fortran clásico
la evitaron **no teniendo memoria dinámica**. Esa última opción, que parece primitiva, es la razón de
que un programa COBOL de 1980 no tenga fugas: **no hay nada que liberar**.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. MOVIDO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA     PIC X(80).
01  PALABRA   PIC X(80).
01  LARGO     PIC 9(4) COMP-3.
01  ED-L      PIC Z(3)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION TRIM(LINEA) TO PALABRA
    COMPUTE LARGO = FUNCTION LENGTH(FUNCTION TRIM(PALABRA))

    MOVE LARGO TO ED-L
    DISPLAY "movido=" FUNCTION TRIM(PALABRA)
            " longitud=" FUNCTION TRIM(ED-L)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** **En COBOL clásico la pregunta de esta clase no existe, porque
no hay memoria dinámica.** Todo el `WORKING-STORAGE` se reserva al cargar el programa y se libera al
terminar. No hay `new`, no hay `free`, no hay punteros colgantes y **no hay fugas**.

Esa es una propiedad notable de la que se habla poco: **un programa COBOL de 1980 no puede tener una
fuga de memoria**. Tampoco puede tener corrupción del montículo, ni doble liberación, ni referencia a
memoria liberada. La clase entera de errores que Rust vino a eliminar **es imposible por
construcción**.

El precio es la rigidez: el tamaño máximo de cada tabla se decide al compilar, y si mañana hay más
clientes de los previstos hay que recompilar.

COBOL sí añadió memoria dinámica cuando hizo falta, y su vocabulario delata la época:

```cobol
ALLOCATE 1000 CHARACTERS RETURNING PUNTERO
SET DIRECCION OF REGISTRO TO PUNTERO
FREE PUNTERO
```

`ALLOCATE` y `FREE` (COBOL 2002) son `malloc` y `free`, con los mismos riesgos. Se usan sobre todo
para hablar con servicios del sistema y con programas C, no en la lógica de negocio.

Y `MOVE`, a pesar de su nombre, **no es un movimiento en el sentido de esta clase**: es una copia. El
origen queda intacto. Es una coincidencia de vocabulario que conviene no confundir.
"""),
        "fortran": ("""
program movido
   implicit none
   character(len=:), allocatable :: palabra, destino
   character(len=200) :: buf

   read(*, '(A)') buf
   palabra = trim(buf)

   !  move_alloc: TRANSFIERE la asignación. `palabra` queda DESASIGNADA.
   call move_alloc(palabra, destino)

   write(*, '(A,A,A,I0)') 'movido=', destino, ' longitud=', len(destino)
end program movido
""", """
**Lo que esta clase enseña en Fortran.** **`move_alloc` es una operación de movimiento de verdad**, y
está en el estándar desde **Fortran 2003** — ocho años antes que la de C++ y doce antes de Rust.

```fortran
call move_alloc(origen, destino)
!  destino pasa a ser dueño de la memoria de origen
!  origen queda DESASIGNADO (allocated(origen) es .false.)
!  NO se copia ni un byte
```

Es exactamente `std::move` seguido de dejar el origen vacío: **transferencia de propiedad, coste
constante, y el origen queda inutilizable**.

Y no se inventó por elegancia: se inventó porque en cálculo científico **los arrays son enormes**.
Redimensionar un array de diez gigabytes copiando sería imposible; con `move_alloc` se reserva el
nuevo, se copia lo necesario y se transfiere la propiedad en una operación de coste cero:

```fortran
allocate(temporal(2 * n))
temporal(1:n) = v
call move_alloc(temporal, v)      ! v ahora es el grande; temporal, nada
```

Ese es el idioma para hacer crecer un array en Fortran, y es literalmente cómo está implementado
`std::vector` por dentro.

La diferencia con Rust es que **Fortran no lo comprueba**: usar `palabra` después del `move_alloc` es
un error en ejecución, no de compilación. El compilador puede avisar con `-fcheck=all`, pero la
garantía la pone el programador. Rust puso esa misma operación en el sistema de tipos, y esa es toda
la diferencia.
"""),
        "ada": ("""
with Ada.Text_IO;           use Ada.Text_IO;
with Ada.Integer_Text_IO;   use Ada.Integer_Text_IO;
with Ada.Strings.Unbounded; use Ada.Strings.Unbounded;

procedure Movido is
   Buf      : String (1 .. 200);
   Ultimo   : Natural;
   Palabra  : Unbounded_String;
begin
   Get_Line (Buf, Ultimo);
   Palabra := To_Unbounded_String (Buf (1 .. Ultimo));

   Put ("movido=" & To_String (Palabra) & " longitud=");
   Put (Length (Palabra), Width => 1);
   New_Line;
end Movido;
""", """
**Lo que esta clase enseña en Ada.** `Unbounded_String` gestiona su propia memoria, y lo hace con un
mecanismo que Ada 95 introdujo y que es **el equivalente exacto de los constructores y destructores
de C++**: los **tipos controlados**.

```ada
type Recurso is new Ada.Finalization.Controlled with record
   Datos : Acceso_Array;
end record;

overriding procedure Initialize (R : in out Recurso);   --  constructor
overriding procedure Adjust     (R : in out Recurso);   --  tras COPIAR
overriding procedure Finalize   (R : in out Recurso);   --  destructor
```

Un tipo que hereda de `Controlled` recibe esas tres llamadas **automáticamente**: al crearse, después
de cada asignación, y al salir del ámbito. Con ellas se implementa RAII completo, conteo de
referencias, copia profunda o lo que haga falta.

`Finalize` **se ejecuta siempre**, incluso si una excepción desenrolla la pila — la garantía que en
C++ dan los destructores y que Java tuvo que suplir con `try-with-resources`.

Lo que Ada **no** tiene en el estándar es la semántica de movimiento: `Adjust` siempre copia. Para
transferir sin copiar hay que implementarlo a mano con punteros y una bandera de propiedad.

Y para el mundo crítico hay una respuesta más radical, la de la ficha de COBOL: **en aviónica la
memoria dinámica se prohíbe**. Sin `new`, no hay propiedad que gestionar, y el consumo de memoria del
programa es analizable antes de volar. SPARK va más lejos y tiene un sistema de **propiedad y préstamo
comprobado estáticamente**, muy parecido al de Rust, añadido en 2019.
"""),
        "pascal": ("""
program Movido;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Palabra, Destino: string;

begin
  ReadLn(Palabra);
  Palabra := Trim(Palabra);

  Destino := Palabra;      { NO copia el texto: comparte y suma 1 al contador }

  WriteLn('movido=', Destino, ' longitud=', IntToStr(Length(Destino)));
end.
""", """
**Lo que esta clase enseña en Pascal.** `Destino := Palabra` **no copia el texto**. Copia un puntero e
incrementa un contador de referencias. La copia real solo ocurre si alguno de los dos se modifica —la
**copia al escribir** de la clase 048.

Ese modelo, que Delphi introdujo en 1996 con `AnsiString`, resuelve el problema de esta clase de una
tercera manera: **ni gestión manual ni recolector, sino conteo de referencias con copia diferida**.

```pascal
A := 'texto largo';
B := A;              { contador = 2, un solo texto en memoria }
B := B + '!';        { AHORA se copia, porque hay dos dueños }
```

Las propiedades son buenas: liberación **determinista** (cuando el contador llega a cero, se libera al
instante, sin esperar a un recolector), semántica de valor, y coste de copia solo cuando hace falta.

Y las limitaciones también son conocidas: **los ciclos no se liberan nunca** —dos objetos que se
apuntan mutuamente mantienen el contador en 1— y el conteo tiene un coste en cada asignación, que en
código multihilo exige operaciones atómicas.

Es el mismo modelo que usan PHP, Swift y los `shared_ptr` de C++, con los mismos compromisos. Swift
resolvió el problema de los ciclos obligando a declarar referencias `weak`; Delphi no, y las fugas por
ciclos entre interfaces son un problema real de sus aplicaciones grandes.

Para los **objetos** (`TObject`), Object Pascal no cuenta referencias: hay que llamar a `Free`, con el
`try..finally` de la clase 071.
"""),
        "lisp": ("""
(let ((palabra (string-trim '(#\\Space #\\Tab #\\Return) (read-line))))
  (format t "movido=~A longitud=~D~%" palabra (length palabra)))
""", """
**Lo que esta clase enseña en Common Lisp.** **En Lisp la pregunta de esta clase no se plantea: hay un
recolector de basura**, y de hecho **Lisp es donde se inventó**, en 1959, para este mismo problema.

McCarthy necesitaba manipular estructuras de listas que se creaban y descartaban continuamente, y
llevar la cuenta a mano era inviable. La solución —recorrer periódicamente lo alcanzable y liberar el
resto— es el primer recolector de la historia, y de ahí viene el nombre *garbage collection*.

Los recolectores modernos de Lisp son generacionales y con compactación: SBCL usa uno que separa los
objetos jóvenes de los viejos, porque la observación empírica es que **la mayoría de los objetos
mueren jóvenes**. Es el mismo diseño que la JVM y el CLR.

Y hay un matiz de esta clase que Lisp sí hace explícito: **la diferencia entre compartir y copiar**.

```lisp
(setf b a)              ; b y a apuntan al MISMO objeto
(setf b (copy-seq a))   ; una copia SUPERFICIAL
(setf b (copy-tree a))  ; una copia PROFUNDA, recursiva
```

Tener las tres con nombres distintos evita la ambigüedad de "¿esto copia?" que en otros lenguajes hay
que averiguar leyendo la documentación.

Lo que un recolector no elimina son las **fugas lógicas**: una estructura global que sigue apuntando a
datos que ya no se necesitan. El recolector no puede saber que ya no te interesan. Es la fuga que sí
existe en Java, Lisp y Smalltalk, y la más difícil de encontrar.
"""),
        "tcl": ("""
gets stdin linea
set palabra [string trim $linea]
set destino $palabra          ;# comparte la representación; NO copia

puts "movido=$destino longitud=[string length $destino]"
""", """
**Lo que esta clase enseña en Tcl.** Tcl usa **conteo de referencias con copia al escribir**, como
Pascal, y lo aplica a **todos los valores**, no solo a las cadenas.

Cada valor de Tcl es un objeto interno (`Tcl_Obj`) con un contador. `set destino $palabra` incrementa
el contador; nada se copia. Y cuando alguien modifica uno de los dos, Tcl comprueba el contador: si es
1, **modifica en el sitio**; si es mayor, copia primero.

Ese mecanismo es lo que hace correctas las optimizaciones de la clase 054:

```tcl
append sec "-$i"       ;# contador 1: modifica en el sitio, LINEAL
lappend lista $x       ;# igual
set b $a               ;# ahora el contador es 2...
append a "x"           ;# ...y ESTO sí copia
```

El programador ve siempre **semántica de valor pura** —nadie te cambia un dato por detrás— con el
rendimiento de la referencia mientras nadie escriba.

Y Tcl tiene el mismo problema de ciclos que Pascal, con una diferencia: **como los valores son
inmutables desde fuera, no se pueden formar ciclos entre ellos**. Un valor no puede contenerse a sí
mismo. Los ciclos solo aparecen entre estructuras de C registradas por extensiones, y por eso Tcl no
necesita un recolector de ciclos.

Es un ejemplo interesante de cómo una decisión de diseño —valores inmutables— elimina de raíz el
problema que obligó a Swift a inventar `weak`.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my $palabra = $linea;

print "movido=$palabra longitud=", length($palabra), "\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl usa **conteo de referencias puro**, sin recolector de
ciclos, y esa decisión tiene una consecuencia que hay que conocer: **las estructuras circulares no se
liberan nunca**.

```perl
my $a = {};
my $b = { otro => $a };
$a->{otro} = $b;        # ciclo: NUNCA se liberan, ni al salir del ámbito
```

La solución de Perl son las **referencias débiles** de `Scalar::Util`:

```perl
use Scalar::Util qw(weaken);
$a->{padre} = $b;
weaken($a->{padre});    # no cuenta para el contador
```

Es el mismo `weak` de Swift y el mismo `weak_ptr` de C++, y por el mismo motivo.

A cambio, el conteo de referencias da algo que un recolector no da: **destrucción determinista**. Un
objeto se destruye **en el instante** en que su última referencia desaparece, así que el método
`DESTROY` se ejecuta cuando toca:

```perl
{
    my $f = Fichero->new('datos.txt');
    ...
}   # aquí, exactamente aquí, se cierra el fichero
```

Ese es el RAII de C++ obtenido con conteo de referencias, y es la razón de que Perl no necesite un
`finally` para cerrar recursos — igual que Python, que usa el mismo modelo.

Java y Lisp, con recolector generacional, **no** lo tienen: el finalizador se ejecuta cuando el
recolector pasa, que puede ser nunca. De ahí `try-with-resources` y `with`.
"""),
        "cpp": ("""
#include <iostream>
#include <string>
#include <utility>

int main() {
    std::string linea;
    if (!std::getline(std::cin, linea)) return 1;

    //  std::move NO mueve nada: convierte a referencia rvalue, y eso permite
    //  al constructor de destino ROBAR el búfer en vez de copiarlo.
    std::string destino = std::move(linea);

    std::cout << "movido=" << destino
              << " longitud=" << destino.size() << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** **`std::move` no mueve nada.** Es una conversión de tipo: convierte
su argumento en una **referencia rvalue** (`T&&`), y eso hace que la sobrecarga elegida sea el
constructor de movimiento en lugar del de copia.

```cpp
std::string b = a;              // COPIA: reserva memoria y copia los bytes
std::string b = std::move(a);   // MUEVE: roba el puntero interno de a
```

Tras el movimiento, `a` queda en un estado **válido pero no especificado**: se puede asignar y
destruir, y no se debe leer su valor. Es exactamente lo que hace `move_alloc` en Fortran, con dos
diferencias: aquí lo implementa cada clase, y **el compilador no impide usar el origen después**.

Ahí está la diferencia con Rust, y es toda la diferencia: Rust puso esta operación en el **sistema de
tipos**, así que usar el origen después **no compila**. C++ la puso en la biblioteca, y usarlo es un
error en ejecución que nadie detecta.

La semántica de movimiento (C++11) fue el cambio más importante del lenguaje moderno, porque resolvió
un problema que tenía treinta años: **devolver un objeto grande de una función**. Antes había que
devolver punteros o pasar parámetros de salida; desde C++11, `return v;` no copia nada.

Y `std::unique_ptr` es la propiedad hecha tipo: **no se puede copiar, solo mover**, así que el
compilador garantiza que hay exactamente un dueño. Es lo más cerca que llega C++ al modelo de Rust, y
llegó cuatro años antes.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi MOVIDO;
  palabra varchar(100) const;
end-pi;

dcl-s destino varchar(100);
dcl-s salida  char(150);

destino = palabra;      // copia: RPG no tiene movimiento ni referencias

salida = 'movido=' + destino + ' longitud=' + %char(%len(destino));
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** Como COBOL, **RPG evita el problema no teniendo memoria dinámica**
en el código de negocio: las variables se dimensionan al compilar y viven en el almacenamiento
automático o estático de la clase 069.

Un programa RPG típico **no puede tener fugas**, y esa propiedad es parte de por qué las aplicaciones
de IBM i llevan décadas ejecutándose sin reiniciar.

RPG sí tiene memoria dinámica cuando hace falta, con el vocabulario de C:

```rpgle
dcl-s p pointer;
dcl-s buffer char(65535) based(p);

p = %alloc(1000);          // malloc
...
dealloc p;                 // free
p = *null;
```

`%alloc`, `%realloc` y `dealloc` son literalmente `malloc`, `realloc` y `free`, con los mismos
riesgos: fugas, doble liberación y punteros colgantes. Se usan para hablar con las APIs del sistema y
para manejar datos de tamaño imprevisible, no en la lógica de negocio.

Y hay una propiedad de la plataforma que cambia el panorama: en IBM i, **la memoria dinámica de un
programa se libera automáticamente al terminar su grupo de activación**. Aunque un programa tenga
fugas, al cerrar el trabajo desaparecen. Es una red de seguridad a nivel de sistema operativo que
pocos entornos ofrecen, y que explica que el asunto se vigile menos que en C.
"""),
        "pli": ("""
 movido: procedure options(main);

    declare palabra character(200) varying;
    declare destino character(200) varying;

    get edit (palabra) (a(200));
    palabra = trim(palabra);

    destino = palabra;      /* copia: PL/I no tiene semántica de movimiento */

    put skip list ('movido=' || destino ||
                   ' longitud=' || trim(char(length(destino))));

 end movido;
""", """
**Lo que esta clase enseña en PL/I.** PL/I **sí tiene memoria dinámica**, y con más formas que casi
cualquier lenguaje de esta página, gracias a las cuatro clases de almacenamiento de la clase 042:

```pli
declare v(1000) fixed binary(31) controlled;

allocate v;        /* APILA una instancia nueva */
allocate v;        /* otra encima: la anterior sigue viva, oculta */
free v;            /* desapila la última */
```

`controlled` mantiene **una pila de asignaciones** de la misma variable, y `allocation(v)` dice
cuántas hay. Es un mecanismo que no tiene equivalente en ningún lenguaje moderno, y que se usaba para
implementar recursión antes de que fuera barata, y para guardar contexto en manejadores de error.

Y `based` con `allocate ... set(p)` es el `malloc` clásico, con todos los riesgos.

Lo que PL/I **no** tiene es ninguna forma de gestión automática: ni recolector, ni conteo de
referencias, ni destructores. **Cada `allocate` necesita su `free`**, y no hay nada que lo compruebe.

Es coherente con su época —1964, antes de que el recolector de Lisp se considerara viable para
lenguajes de propósito general— y es una de las razones de que los programas PL/I grandes tuvieran
fama de fugar memoria.

La comparación con COBOL es instructiva: COBOL evitó el problema **no dando la herramienta**, y PL/I lo
creó **dándola sin barandillas**. Las dos decisiones se pueden defender, y la segunda es la que la
industria repitió con C.
"""),
        "mumps": ("""
MOVIDO ; Movimiento y prestamo -- clase 081
 read palabra
 set destino = palabra
 write "movido=", destino, " longitud=", $length(destino), !
 quit
""", """
**Lo que esta clase enseña en M.** M gestiona la memoria automáticamente y la pregunta de esta clase
no aparece — pero por un motivo distinto del de Lisp, y es el más interesante de la página: **en M el
dato importante no está en memoria, está en disco**.

Una variable local vive lo que viva la rutina. Un ***global*** —`^PACIENTE`— **es persistente por
definición**, y su gestión no es un problema de memoria sino de base de datos: bloques, índices,
transacciones y recuperación ante fallos.

```mumps
 set ^PACIENTE(id) = datos      ; esto es una ESCRITURA EN DISCO
 kill ^PACIENTE(id)             ; y esto un BORRADO
```

`kill` sobre un global borra el nodo **y todos sus descendientes**, transaccionalmente. No hay
"liberar memoria": hay borrar datos.

Esa inversión —que el almacenamiento principal sea el disco y la memoria un detalle— es lo que hace
que M no tenga las categorías de esta clase. No hay propiedad que transferir porque el dato no es de
nadie: **está en la base de datos**.

Para las variables locales, `kill` las elimina y `new` de la clase 069 las restaura al salir. El
consumo de memoria de un proceso M está acotado por el tamaño de su tabla de símbolos locales, que las
implementaciones limitan explícitamente.

Es el mismo razonamiento que hace que un programa COBOL no tenga fugas, llevado un paso más allá: **si
todo lo que importa está en disco, la gestión de memoria deja de ser un problema de diseño del
lenguaje**.
"""),
        "smalltalk": ("""
| palabra destino |

palabra := stdin nextLine trimBoth.
destino := palabra.        "comparten el mismo objeto: no hay copia"

Transcript
    show: 'movido=', destino;
    show: ' longitud=', destino size printString;
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** `destino := palabra` **no copia nada**: las dos variables
apuntan al mismo objeto. En Smalltalk **toda variable es una referencia**, siempre, y el recolector se
encarga del resto.

Y Smalltalk tiene un mecanismo que casi ningún lenguaje ofrece y que encaja exactamente en esta
clase: **el objeto puede enterarse de que va a ser recolectado**.

```smalltalk
unObjeto finalizationRegistry add: unObjeto executor: unBloque
```

Los **finalizadores** de Pharo permiten ejecutar código cuando un objeto se vuelve inalcanzable —
cerrar un fichero, liberar un recurso del sistema operativo—. Es lo mismo que los `PhantomReference`
de Java y con la misma advertencia: **no está garantizado cuándo ocurre**, así que no sirve para
recursos escasos. Para eso está `ensure:` de la clase 071.

Y hay dos capacidades que solo tienen sentido en un sistema donde la memoria es un objeto más:

```smalltalk
unObjeto becomeForward: otro     "TODAS las referencias a unObjeto pasan a otro"
Smalltalk garbageCollect          "forzar una recolección"
unObjeto pointersTo               "¿QUIÉN me está apuntando?"
```

**`become:` intercambia la identidad de dos objetos en todo el sistema**, en una operación. Se usa
para migrar instancias cuando cambia una clase —el sistema está vivo y hay objetos existentes— y no
tiene equivalente en ningún otro lenguaje.

Y `pointersTo` responde a la pregunta más difícil de depurar en cualquier lenguaje con recolector:
**"¿por qué este objeto sigue vivo?"**. En Java hace falta un analizador de volcados de memoria; aquí
es un mensaje.
"""),
    },
)

# ---------------------------------------------------------------------------
# 082 — Alcance (scope) y sombreado (shadowing)
# ---------------------------------------------------------------------------
SPECS["082"] = dict(
    gancho="""
Un valor calculado **dentro** de un ámbito y otro que sigue intacto **fuera**. Parece elemental, y
resulta que **COBOL no tiene ámbitos**: todas sus variables son globales al programa, siempre, sin
excepción. Y Fortran tuvo que esperar hasta **2008** para tener bloques con variables locales.
""",
    porque="""
Aquí el concepto es el **ámbito léxico**, y estos lenguajes lo enseñan porque muestran su ausencia.
En **COBOL** todo es global: un programa de cinco mil líneas tiene un solo espacio de nombres, y por
eso sus variables llevan prefijos —`WS-`, `CLI-`, `LK-`— que son un sistema de ámbitos hecho a mano
con convenciones de nombres.

Y **M** tiene la respuesta más distinta de todas: **ámbito dinámico** con `new`, donde una variable no
es local al bloque sino a la **duración de la llamada**, y las rutinas llamadas la ven. Es el mismo
mecanismo que `local` en Perl y las variables especiales de Lisp, y comparar los dos modelos es lo
más valioso de esta clase.
""",
    cierre="""
Lo transferible: **el ámbito léxico se determina leyendo el texto; el dinámico, ejecutando el
programa**. Con léxico, una función solo ve lo que está escrito alrededor de ella. Con dinámico, ve lo
que haya puesto quien la llamó, así que el mismo código se comporta distinto según desde dónde se
invoque. El léxico ganó porque es analizable — pero el dinámico sigue vivo donde hace falta un
contexto implícito: `local` en Perl, las variables especiales de Lisp, y prácticamente todo el código
de MUMPS.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. ALCANCE.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA    PIC X(80).
01  N        PIC S9(9) COMP-3.
01  INTERNO  PIC S9(9) COMP-3.
01  ED-I     PIC -(8)9.
01  ED-N     PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N

    PERFORM CALCULAR

    MOVE INTERNO TO ED-I
    MOVE N       TO ED-N
    DISPLAY "interno=" FUNCTION TRIM(ED-I)
            " externo=" FUNCTION TRIM(ED-N)
    STOP RUN.

CALCULAR.
    COMPUTE INTERNO = N + 10.
""", """
**Lo que esta clase enseña en COBOL.** **COBOL no tiene ámbitos.** Ni de bloque, ni de párrafo, ni de
sección. Todo lo declarado en `WORKING-STORAGE` es visible desde cualquier punto del programa, y no
hay forma de declarar algo "solo para este trozo".

La consecuencia es que un programa de cinco mil líneas tiene **un único espacio de nombres**, y el
sustituto que inventó la industria son las **convenciones de prefijos**:

```cobol
01  WS-CONTADOR      PIC 9(4).     *> WS = Working-Storage
01  LK-PARAMETRO     PIC X(10).    *> LK = Linkage
01  CLI-NOMBRE       PIC X(40).    *> por módulo funcional
01  I-CLIENTES-KEY   PIC X(8).     *> por fichero
```

Eso no es estilo: es un **sistema de ámbitos implementado con nombres**, y toda instalación grande
tiene su estándar documentado. Cuando falla —dos módulos que usan `WS-CONTADOR` para cosas distintas
en el mismo programa— aparece el error más difícil de encontrar de COBOL.

COBOL sí tiene una forma de ámbito, y llegó tarde: los **programas anidados** de COBOL-85.

```cobol
IDENTIFICATION DIVISION.
PROGRAM-ID. PRINCIPAL.
...
    IDENTIFICATION DIVISION.
    PROGRAM-ID. INTERNO IS COMMON.
    DATA DIVISION.
    WORKING-STORAGE SECTION.
    01  PRIVADO  PIC 9(4).      *> invisible desde PRINCIPAL
    ...
    END PROGRAM INTERNO.
END PROGRAM PRINCIPAL.
```

Un programa anidado tiene su propio `WORKING-STORAGE` **privado**, y solo ve lo que el padre marque
con `GLOBAL`. Es encapsulación de verdad, disponible desde 1985 y **muy poco usada** — porque para
entonces ya había millones de líneas escritas con prefijos.
"""),
        "fortran": ("""
program alcance
   implicit none
   integer :: n, interno

   read(*, *) n

   block                          ! Fortran 2008: bloque con declaraciones
      integer :: n_local
      n_local = n + 10
      interno = n_local
   end block                      ! n_local deja de existir aquí

   write(*, '(A,I0,A,I0)') 'interno=', interno, ' externo=', n
end program alcance
""", """
**Lo que esta clase enseña en Fortran.** La construcción **`block`** —con declaraciones propias— llegó
en **Fortran 2008**. Hasta entonces, **el ámbito más pequeño de Fortran era el procedimiento**: todas
las declaraciones iban arriba y valían para toda la subrutina.

Eso obligaba a un estilo reconocible: procedimientos con veinte declaraciones al principio, la mitad
de ellas temporales usadas en un solo bucle. Es la misma limitación que Pascal, y por el mismo motivo
histórico —la compilación en una pasada—.

`block` permite además **sombrear**:

```fortran
integer :: x
x = 1
block
   integer :: x      ! SOMBREA la exterior
   x = 99
end block
print *, x           ! 1: la exterior no se tocó
```

Y tiene una capacidad que va más allá del ámbito: **dentro de un `block` se puede usar `exit` con
nombre** para salir de él, como se vio en la clase 058, lo que da un bloque con salida temprana sin
`goto`.

El otro mecanismo de ámbito de Fortran son los **procedimientos internos** en `contains`, que **ven
las variables del anfitrión** —eso es la clase 083— y los **módulos**, que son la clase 086.

Y una nota importante: en Fortran, **una variable local de un procedimiento no conserva su valor entre
llamadas**, salvo que lleve `save` o esté inicializada en la declaración — la trampa de la clase 042.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Alcance is
   N : Integer;
begin
   Get (N);

   declare
      Interno : constant Integer := N + 10;   --  solo existe aquí
   begin
      Put ("interno=");
      Put (Interno, Width => 1);
   end;

   Put (" externo=");
   Put (N, Width => 1);
   New_Line;
end Alcance;
""", """
**Lo que esta clase enseña en Ada.** El bloque **`declare … begin … end`** puede aparecer **en
cualquier punto** donde vaya una sentencia, y crea un ámbito con sus propias declaraciones. Es la
misma idea que el `block` de Fortran 2008, disponible en Ada desde 1983.

Y tiene una ventaja concreta sobre declarar arriba: **permite `constant`**. `Interno` se calcula
justo donde se sabe su valor, y queda sellado. Declararlo al principio del procedimiento obligaría a
dejarlo variable.

Los bloques de Ada pueden además **llevar nombre** y **manejadores de excepción propios**:

```ada
Validacion : declare
   Datos : Registro := Leer;
begin
   Procesar (Datos);
exception
   when Constraint_Error =>
      Put_Line ("datos inválidos");     --  solo captura lo de ESTE bloque
end Validacion;
```

Un ámbito con su propio manejo de errores, acotado a las líneas que lo necesitan. Es exactamente lo
que en C++ se consigue anidando un `try` y en Java un bloque `try`, con la diferencia de que aquí el
bloque **también** delimita las declaraciones.

Sobre el sombreado, Ada lo permite pero es **muy estricto con la ambigüedad**: si dos nombres visibles
por `use` colisionan, **ninguno de los dos es visible** y hay que cualificar. Eso evita el problema
clásico de "importé un paquete y ahora mi función llama a otra cosa" — el compilador se niega en lugar
de elegir por ti.
"""),
        "pascal": ("""
program Alcance;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N, Interno: Integer;

procedure Calcular;
var
  Temp: Integer;        { local al PROCEDIMIENTO: no existe fuera }
begin
  Temp := N + 10;       { ve N, del ámbito que lo contiene }
  Interno := Temp;
end;

begin
  Read(N);
  Calcular;
  WriteLn('interno=', IntToStr(Interno), ' externo=', IntToStr(N));
end.
""", """
**Lo que esta clase enseña en Pascal.** **Pascal no tiene ámbito de bloque**: `begin`/`end` agrupa
sentencias pero **no puede declarar variables**. El ámbito más pequeño es el **procedimiento**.

Lo que Pascal sí tiene, y fue una de sus grandes aportaciones, son los **procedimientos anidados**
con **ámbito léxico completo**:

```pascal
procedure Externo;
var
  A: Integer;

  procedure Interno;
  var
    B: Integer;
  begin
    B := A + 1;        { VE la A de Externo }
  end;

begin
  A := 1;
  Interno;
end;
```

Un procedimiento anidado **ve todas las variables de los que lo contienen**, a cualquier profundidad.
Eso viene de ALGOL 60 y **C nunca lo tuvo** —solo funciones al nivel superior—, lo que obligó a C a
usar variables globales o a pasar estructuras de contexto.

La implementación de eso es lo interesante: hace falta un **enlace estático** en cada marco de pila,
que apunta al marco del procedimiento que lo contiene léxicamente, para poder llegar a sus variables.
Es el mecanismo que después se generalizó en las clausuras de la clase 083.

Ada, Fortran (con `contains`), PL/I y JavaScript tienen anidamiento léxico; C, Java y Go no —Java lo
recuperó con las clases internas y Go con las clausuras—.

Y el sombreado funciona: una variable interna con el mismo nombre oculta a la externa, y Free Pascal
avisa con `-vh` si sospecha que fue un accidente.
"""),
        "lisp": ("""
(let ((n (read)))
  (format t "interno=~D externo=~D~%"
          (let ((n (+ n 10))) n)     ; esta n SOMBREA la exterior
          n))                         ; aquí vuelve a ser la exterior
""", """
**Lo que esta clase enseña en Common Lisp.** El sombreado de este programa es visible en una línea:
la `n` interna del `let` oculta a la externa **dentro de sus paréntesis**, y fuera vuelve a valer la
original.

Y Lisp es el lenguaje donde mejor se ve la diferencia entre los **dos tipos de ámbito**, porque tiene
los dos:

```lisp
(defvar *tasa* 0.21)                  ; variable ESPECIAL: ámbito DINÁMICO
(defun con-iva (x) (* x (+ 1 *tasa*)))

(defun ejemplo ()
  (let ((*tasa* 0.10))                ; reenlaza la especial...
    (con-iva 100)))                    ; ...y con-iva ve 0.10, aunque no lo sepa
```

`con-iva` **no recibe la tasa como parámetro y no la ve por ámbito léxico**: la ve porque quien la
llamó reenlazó la variable especial. Eso es **ámbito dinámico**, y en Lisp está marcado por
convención con asteriscos —los *earmuffs*— precisamente para que se note.

Con una variable normal (`let` sobre un símbolo no especial), el ámbito es **léxico**: solo la ve el
código escrito dentro.

Tener los dos, y distinguirlos tipográficamente, es lo que hace de Lisp el mejor sitio para entender
esta clase. El dinámico sirve para el **contexto implícito** —la tasa vigente, el flujo de salida, el
nivel de registro— que en otros lenguajes obliga a pasar un parámetro por toda la cadena de llamadas
o a usar una variable global sin restaurar.

Es exactamente lo que hace `new` en M y `local` en Perl, y lo que Java resuelve con `ThreadLocal`.
"""),
        "tcl": ("""
proc calcular {n} {
    set n [expr {$n + 10}]     ;# n es LOCAL al proc: no toca la del llamante
    return $n
}

gets stdin linea
set n [string trim $linea]

puts "interno=[calcular $n] externo=$n"
""", """
**Lo que esta clase enseña en Tcl.** El ámbito de Tcl es **el procedimiento, y nada más**: no hay
ámbito de bloque, y —esto es lo llamativo— **un `proc` NO ve las variables globales**.

```tcl
set config "algo"
proc f {} {
    puts $config        ;# ERROR: "can't read config: no such variable"
}
```

Hay que declararlo explícitamente:

```tcl
proc f {} {
    global config       ;# ahora sí
    puts $config
}
```

Esa decisión —**las globales son invisibles salvo que las pidas**— es exactamente la contraria de la
de casi todos los lenguajes, y es deliberada: en un lenguaje de guion incrustado en una aplicación
grande, que un procedimiento pueda leer accidentalmente cualquier variable del sistema sería un
desastre.

Python tomó la decisión inversa y a medias: **puede leer** las globales sin declarar nada, pero para
**escribirlas** necesita `global`. Tcl es más estricto en las dos direcciones.

Y Tcl tiene además `namespace`, que da un tercer nivel:

```tcl
namespace eval ::miapp {
    variable contador 0          ;# variable de ESPACIO DE NOMBRES
    proc incrementar {} {
        variable contador        ;# se declara para verla
        incr contador
    }
}
```

`variable` es a los espacios de nombres lo que `global` al nivel superior. Con eso Tcl tiene tres
niveles —local, de espacio de nombres y global— y **los tres exigen declaración explícita** para
usarse desde dentro de un procedimiento.
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

my $interno;
{
    my $n = $n + 10;      # el $n de la DERECHA es todavía el EXTERIOR
    $interno = $n;
}

print "interno=$interno externo=$n\\n";
""", """
**Lo que esta clase enseña en Perl.** La línea `my $n = $n + 10;` merece explicación porque parece
imposible y es correcta: **una variable declarada con `my` no es visible hasta que TERMINA la
sentencia que la declara**.

Así que en el lado derecho, `$n` todavía se refiere al **exterior**. A partir de la siguiente línea,
`$n` es el nuevo. Es una regla precisa y muy útil para el idioma
`my $x = $x` —tomar una copia local de algo del ámbito exterior—.

Perl tiene **tres declaradores**, y esta clase es donde se distinguen:

| | Ámbito | Qué hace |
|---|---|---|
| `my` | **Léxico** | Variable nueva, visible solo en el bloque |
| `our` | Léxico | Un **alias** a la variable global del paquete |
| `local` | **DINÁMICO** | Guarda el valor de una global y lo restaura al salir |

`local` es la que sorprende, y es exactamente el `new` de M y las variables especiales de Lisp:

```perl
our $separador = ',';
sub imprimir { print join($separador, @_) }

sub con_tabulador {
    local $separador = "\\t";     # cambia la GLOBAL durante esta llamada
    imprimir(@_);                  # imprimir ve el tabulador, sin saberlo
}                                  # y al salir se restaura la coma
```

`imprimir` no recibe el separador y no lo ve por ámbito léxico: lo ve porque `local` lo cambió
temporalmente. Es el contexto implícito de la ficha de Lisp, con otra palabra.

El uso más común de `local` en Perl real es sobre las variables especiales del propio lenguaje:
`local $/ = undef;` para leer un fichero entero de una vez, o `local $_` para no pisar la variable
implícita.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    int interno{};
    {
        const int n_interno = n + 10;   // ámbito de BLOQUE
        interno = n_interno;
    }   // n_interno deja de existir aquí

    std::cout << "interno=" << interno << " externo=" << n << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ tiene **ámbito de bloque** desde C, y cualquier par de llaves
crea uno. Y el sombreado es legal, con un aviso:

```cpp
int x = 1;
{
    int x = 2;      // SOMBREA; -Wshadow lo avisa
}
```

`-Wshadow` no está en `-Wall` y conviene activarlo: el sombreado accidental —sobre todo de un
parámetro por una variable local— es una fuente real de errores.

Lo que C++ añade a esta clase, y es lo importante, es que **el ámbito determina el tiempo de vida**:

```cpp
{
    std::lock_guard<std::mutex> cierre(m);   // se bloquea aquí
    std::ofstream f("salida.txt");           // se abre aquí
    ...
}   // el destructor de f cierra el fichero, el de cierre libera el mutex
```

Ese es **RAII**, y es la razón de que en C++ el ámbito sea una herramienta de gestión de recursos y no
solo de visibilidad. Abrir un bloque `{ }` sin más motivo que **acotar el tiempo de vida de un
recurso** es un idioma normal del lenguaje.

C++17 añadió además el inicializador en `if` y `switch`, que acota el ámbito a la sentencia:

```cpp
if (auto it = m.find(k); it != m.end()) { ... }   // it muere al salir del if
```

Y C++20 los espacios de nombres en línea, los módulos y `using enum`, que refinan la visibilidad —
tema de la clase 086.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller) main(Principal);

dcl-s global_n int(10);          // GLOBAL: visible en todo el módulo

dcl-proc Principal;
  dcl-pi *n;
    n int(10) const;
  end-pi;

  dcl-s salida char(50);

  global_n = n;
  salida = 'interno=' + %char(calcular())
         + ' externo=' + %char(global_n);
  dsply salida;
end-proc;

dcl-proc calcular;
  dcl-pi *n int(10);
  end-pi;
  dcl-s temp int(10);            // LOCAL al procedimiento
  temp = global_n + 10;
  return temp;
end-proc;
""", """
**Lo que esta clase enseña en RPG.** RPG tiene **dos niveles y solo dos**: lo declarado fuera de
cualquier `dcl-proc` es **global al módulo**, y lo declarado dentro es **local al procedimiento**. No
hay ámbito de bloque.

Y esa distinción **no existía antes de ILE**. En el RPG clásico, absolutamente todo era global —como
en COBOL— y las subrutinas (`begsr`/`endsr`) compartían todas las variables del programa. Por eso el
código antiguo usa prefijos por subrutina, exactamente igual que COBOL con `WS-`.

Los subprocedimientos de ILE trajeron el ámbito local, y con él la posibilidad de escribir código
reutilizable de verdad.

RPG tiene además dos palabras que afinan la visibilidad **entre módulos**:

```rpgle
dcl-s contador int(10) static;    // conserva el valor entre llamadas
dcl-proc calcular export;         // VISIBLE desde otros módulos
dcl-proc auxiliar;                // sin export: PRIVADO del módulo
```

`export` en un `dcl-proc` es lo que decide si el procedimiento entra en la interfaz del módulo. Sin
él, es privado. Es exactamente el `static` de C aplicado a funciones, con la lógica invertida —en C
hay que escribir `static` para ocultar; en RPG hay que escribir `export` para mostrar—.

Esa inversión es mejor: **lo privado por defecto** es lo que hoy recomiendan todas las guías, y lo
que hacen Rust, Java (paquete) y los módulos de C++20.
"""),
        "pli": ("""
 alcance: procedure options(main);

    declare n fixed binary(31);

    get list (n);

    begin;                              /* BLOQUE con su propio ámbito */
       declare interno fixed binary(31);
       interno = n + 10;
       put skip list ('interno=' || trim(char(interno)) ||
                      ' externo=' || trim(char(n)));
    end;

 end alcance;
""", """
**Lo que esta clase enseña en PL/I.** El **bloque `begin`** de PL/I es un ámbito completo con sus
propias declaraciones, y estaba en el lenguaje **desde 1964** — mucho antes que en Fortran (2008) y
que en C.

Y PL/I tiene **anidamiento léxico ilimitado** con la regla clásica de ALGOL: un bloque interno ve
todo lo de los que lo contienen, y puede sombrearlo.

```pli
declare x fixed binary(31);
begin;
   declare x character(10);      /* SOMBREA el x exterior, y con OTRO TIPO */
   ...
end;
```

Lo que distingue a PL/I es la interacción del ámbito con las **clases de almacenamiento** de la clase
042: un `begin` block **activa el almacenamiento automático** de lo que declara, así que entrar y
salir tiene coste. Por eso existe `do; ... end;`, que agrupa **sin** crear ámbito ni marco:

```pli
if c then do;  ... end;      /* solo agrupa: barato */
if c then begin; ... end;    /* ámbito nuevo: puede declarar, cuesta más */
```

Tener las dos construcciones con esa diferencia de coste explícita es muy propio del lenguaje, y
también es la clase de detalle que hay que conocer para leer código ajeno: `begin` y `do` parecen
intercambiables y no lo son.

Y `begin` puede llevar sus propios manejadores `ON`, igual que el bloque de Ada — el ámbito delimita
también el manejo de errores.
"""),
        "mumps": ("""
ALCANCE ; Alcance y sombreado -- clase 082
 read n
 do calcular
 write "interno=", interno, " externo=", n, !
 quit
 ;
calcular ; usa NEW para no pisar variables del llamante
 new temp
 set temp = n + 10
 set interno = temp
 quit
""", """
**Lo que esta clase enseña en M.** **M no tiene ámbito léxico. Todas las variables son globales al
proceso**, y lo único que existe es **`new`**, que da **ámbito dinámico**.

```mumps
calcular ;
 new temp              ; guarda el valor ACTUAL de temp (sea de quien sea)...
 set temp = 5
 quit                  ; ...y lo restaura al salir
```

`new temp` **no crea una variable local**: guarda en una pila el valor que `temp` tuviera en todo el
proceso, lo deja indefinido, y lo restaura al salir de la rutina.

La diferencia con el ámbito léxico es la que da la lección de esta clase: **una rutina llamada desde
aquí VE la `temp` de esta rutina**, porque no hay barrera léxica. Con ámbito léxico eso sería
imposible.

```mumps
 new formato
 set formato = "corto"
 do IMPRIMIR^REP      ; IMPRIMIR ve "corto" sin que nadie se lo pase
```

Ese es el contexto implícito de la ficha de Lisp y del `local` de Perl, y en M **es el único modelo
que hay**. Todo el código de VistA lo usa: se establecen variables convenidas antes de llamar, y las
rutinas llamadas las leen.

Es frágil —un `new` olvidado corrompe el estado del llamante— y es la razón de que las guías de estilo
de M sean obsesivas con `new`. Y es potente: permite pasar contexto a través de veinte niveles de
llamada sin tocar ninguna firma.

Existe además `new` **exclusivo**: `new (a, b)` guarda **todo menos** `a` y `b`, que es la forma de
aislar completamente una rutina.
"""),
        "smalltalk": ("""
| n interno |

n := stdin nextLine trimBoth asNumber.

interno := [ :x | | temp | temp := x + 10. temp ] value: n.

Transcript
    show: 'interno=', interno printString;
    show: ' externo=', n printString;
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** El bloque de este programa declara su propia temporal
—`| temp |` dentro de los corchetes— y esa variable **solo existe durante la evaluación del bloque**.

Smalltalk tiene una jerarquía de ámbitos muy clara, de dentro afuera:

1. **Temporales del bloque** — `[ :x | | t | ... ]`
2. **Argumentos y temporales del método**
3. **Variables de instancia** del objeto
4. **Variables de clase**, compartidas por la clase y sus instancias
5. **Variables globales**, en el diccionario `Smalltalk`

Y todo es **léxico**: un bloque ve las variables del método que lo creó, aunque se evalúe muy lejos —
eso es la clase 083.

Lo que hace especial a Smalltalk en esta clase es que **el ámbito es un objeto inspeccionable**.
`thisContext` de la clase 066 da acceso al marco de activación actual, con sus temporales, su receptor
y su llamante:

```smalltalk
thisContext tempNames          "los nombres de las temporales"
thisContext receiver            "el objeto que recibió el mensaje"
thisContext sender              "el marco que llamó"
```

Por eso el depurador de Smalltalk puede mostrar y **modificar** las variables locales de cualquier
marco de la pila, y continuar. En un lenguaje compilado esa información solo existe si se compiló con
símbolos de depuración; aquí **es parte del modelo de objetos**.

Y las variables de instancia no llevan `self.` delante: se escriben a secas, lo que hace que un método
de Smalltalk se lea muy limpio y exija conocer la clase para saber qué es local y qué es de instancia.
"""),
    },
)

# ---------------------------------------------------------------------------
# 083 — Cierres (closures) y captura de variables
# ---------------------------------------------------------------------------
SPECS["083"] = dict(
    gancho="""
Dos funciones que recuerdan un valor que ya no está en ningún parámetro. Eso es una **clausura**: una
función más el trozo de entorno que capturó al nacer. Es la base de la programación funcional
moderna, de los manejadores de eventos y de medio JavaScript — y de estos doce lenguajes, **solo
cuatro la tienen completa**.
""",
    porque="""
Aquí el concepto es la **captura del entorno**, y estos lenguajes lo enseñan porque muestran los tres
niveles. **Clausura completa**: Lisp y Smalltalk, donde la función es un valor que se puede guardar,
devolver y llamar mucho después, con su entorno vivo. **Anidamiento léxico sin primera clase**:
Fortran, Ada, Pascal y PL/I, donde un procedimiento interno **ve** las variables del que lo contiene
pero **no se puede devolver**. Y **nada**: COBOL, RPG y M.

La diferencia entre los dos primeros niveles es exactamente **el problema del funarg ascendente**: si
la función sobrevive al procedimiento que la creó, ¿dónde viven sus variables capturadas? La respuesta
—en el montículo, no en la pila— es lo que separa una clausura de un procedimiento anidado.
""",
    cierre="""
Lo transferible: **una clausura es un objeto con un método, y un objeto es una clausura con varios
métodos**. Son la misma idea vista desde dos lados, y por eso los lenguajes que tienen clausuras de
primera clase pueden construir objetos con ellas —y Smalltalk, que tiene objetos, construye sus
estructuras de control con bloques—. Cuando un lenguaje no tiene ninguna de las dos, como COBOL o
RPG, el sustituto es siempre el mismo: una **variable global más una convención**.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. CLAUSURA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  BASE-V  PIC S9(9) COMP-3.
01  K       PIC S9(9) COMP-3.
01  R       PIC S9(9) COMP-3.
01  ED-1    PIC -(8)9.
01  ED-2    PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO BASE-V

    MOVE 1 TO K
    PERFORM SUMAR
    MOVE R TO ED-1

    MOVE 2 TO K
    PERFORM SUMAR
    MOVE R TO ED-2

    DISPLAY "r1=" FUNCTION TRIM(ED-1)
            " r2=" FUNCTION TRIM(ED-2)
    STOP RUN.

SUMAR.
    COMPUTE R = BASE-V + K.
""", """
**Lo que esta clase enseña en COBOL.** **COBOL no tiene clausuras, ni funciones anónimas, ni funciones
como valores.** No hay nada que capturar porque no hay funciones de primera clase.

Y lo que este programa hace es exactamente lo que hace COBOL cuando necesitaría una: **variables
globales y una convención de llamada**. `SUMAR` no recibe parámetros; lee `BASE-V` y `K` porque son
globales, y deja el resultado en `R`. El "entorno capturado" es el estado global del programa.

Es el patrón que COBOL usa para todo, y funciona mientras nadie más toque esas variables. En un
programa de cinco mil líneas con cuarenta párrafos, esa garantía es la disciplina del equipo.

Lo más cerca que llega COBOL a una función como valor es la llamada dinámica de la clase 068:

```cobol
01  NOMBRE-RUTINA  PIC X(8).
...
MOVE "CALCIVA" TO NOMBRE-RUTINA
CALL NOMBRE-RUTINA USING IMPORTE, RESULTADO
```

Se puede **elegir qué código ejecutar** guardando su nombre en una variable, lo que da tablas de
despacho. Lo que no se puede es **crear** una función nueva ni capturar nada: el programa llamado
tiene su propio `WORKING-STORAGE` y no ve el del llamante.

Es la diferencia entre "seleccionar entre funciones que existen" y "fabricar una función con estado",
y es justo lo que esta clase mide.
"""),
        "fortran": ("""
program clausura
   implicit none
   integer :: base

   read(*, *) base

   write(*, '(A,I0,A,I0)') 'r1=', sumar(1), ' r2=', sumar(2)

contains

   function sumar(k) result(r)
      integer, intent(in) :: k
      integer :: r
      r = base + k        ! VE `base` del programa anfitrión: asociación de anfitrión
   end function sumar

end program clausura
""", """
**Lo que esta clase enseña en Fortran.** `sumar` **ve `base` sin recibirla**, gracias a la **asociación
de anfitrión** (*host association*): un procedimiento interno declarado tras `contains` accede a todas
las variables del programa o subrutina que lo contiene.

Eso es **ámbito léxico**, y es la mitad de una clausura. Lo que falta es la otra mitad: **no se puede
devolver `sumar` ni guardarla**.

```fortran
! Esto NO se puede hacer en Fortran:
!   f = crear_sumador(10)     ! devolver una función que recuerde el 10
```

La razón es el **problema del funarg ascendente**: si `sumar` sobreviviera a `clausura`, ¿dónde
viviría `base`? En la pila, y esa pila ya se destruyó. Para permitirlo hay que mover el entorno al
montículo y que alguien lo libere — exactamente lo que hacen Lisp, Smalltalk y JavaScript, y lo que
Fortran no quiere hacer por su modelo de memoria.

Lo que Fortran sí tiene son **punteros a procedimiento**, que permiten pasar y guardar procedimientos
—pero **sin entorno capturado**:

```fortran
procedure(interfaz), pointer :: f
f => mi_funcion
resultado = f(x)
```

Es un puntero a función de C: se puede elegir qué se llama, no fabricar una función con estado. La
misma limitación que COBOL, con mejor sintaxis.

Y una advertencia: pasar un procedimiento interno como argumento **sí** conserva la asociación de
anfitrión mientras el anfitrión esté activo. En cuanto termina, usarlo es comportamiento indefinido.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Clausura is
   Base : Integer;

   --  Función anidada: VE Base, pero no se puede devolver ni guardar.
   function Sumar (K : Integer) return Integer is
   begin
      return Base + K;
   end Sumar;

begin
   Get (Base);

   Put ("r1="); Put (Sumar (1), Width => 1);
   Put (" r2="); Put (Sumar (2), Width => 1);
   New_Line;
end Clausura;
""", """
**Lo que esta clase enseña en Ada.** Como Fortran y Pascal, Ada tiene **anidamiento léxico** pero **no
clausuras de primera clase**. `Sumar` ve `Base`; no se puede devolver.

Y Ada lo impide **explícitamente**, con una de sus reglas más características: **las comprobaciones de
accesibilidad**.

```ada
type Funcion is access function (K : Integer) return Integer;

function Crear return Funcion is
   Local : Integer := 10;
   function F (K : Integer) return Integer is (Local + K);
begin
   return F'Access;      --  ERROR DE COMPILACIÓN: nivel de accesibilidad
end Crear;
```

El compilador **rechaza** devolver un puntero a un subprograma anidado, porque su entorno vive en la
pila y estaría muerto al usarlo. En C, el equivalente compila y produce comportamiento indefinido; en
Ada, no compila.

Esa comprobación —el **nivel de accesibilidad**, que Ada calcula para cada tipo de acceso— se aplica
también a los punteros a datos: no se puede devolver un puntero a una variable local. Es, en la
práctica, **una parte del análisis de tiempo de vida de Rust**, disponible desde 1983.

Para lo que en otros lenguajes se haría con una clausura, Ada usa **genéricos** (clase 078) o un
**tipo etiquetado con estado**:

```ada
type Sumador is tagged record Base : Integer; end record;
function Aplicar (S : Sumador; K : Integer) return Integer is (S.Base + K);
```

Un objeto con un método, que es la otra cara de la misma idea.
"""),
        "pascal": ("""
program Clausura;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Base: Integer;

function Sumar(K: Integer): Integer;    { anidada al programa: ve Base }
begin
  Result := Base + K;
end;

begin
  Read(Base);
  WriteLn('r1=', IntToStr(Sumar(1)), ' r2=', IntToStr(Sumar(2)));
end.
""", """
**Lo que esta clase enseña en Pascal.** El Pascal ISO tiene anidamiento léxico —heredado de ALGOL 60—
y **no tiene clausuras**: un procedimiento anidado ve el entorno pero no es un valor.

**Delphi 2009 sí las añadió**, con una palabra clave que dice exactamente lo que hace:

```pascal
type
  TSumador = reference to function(K: Integer): Integer;

function CrearSumador(Base: Integer): TSumador;
begin
  Result := function(K: Integer): Integer
            begin
              Result := Base + K;      { CAPTURA Base }
            end;
end;

var F: TSumador;
begin
  F := CrearSumador(10);
  WriteLn(F(1));      { 11 -- Base sigue viva }
end;
```

**`reference to function`** es lo que la distingue de un puntero a función normal (`function(...)`):
implica **captura del entorno** y **conteo de referencias** sobre el objeto que lo guarda.

Ese detalle de implementación es la clave de toda la clase: para que `Base` sobreviva a
`CrearSumador`, el compilador **la mueve al montículo** y crea un objeto invisible que la contiene.
La clausura es ese objeto, y se libera cuando nadie la referencia.

Es exactamente lo que hace JavaScript, lo que hace `std::function` en C++ y lo que Java resolvió con
las clases anónimas. **La clausura es un objeto**, y ese es el punto de esta clase.

Free Pascal lo soporta con `{$modeswitch functionreferences}`.
"""),
        "lisp": ("""
(let* ((base (read))
       (f1 (lambda () (+ base 1)))     ; CAPTURA base
       (f2 (lambda () (+ base 2))))
  (format t "r1=~D r2=~D~%" (funcall f1) (funcall f2)))
""", """
**Lo que esta clase enseña en Common Lisp.** Las dos lambdas **capturan `base`**, y son valores de
primera clase: se pueden guardar en variables, meter en listas, devolver de una función y llamar mucho
después.

La forma canónica, que devuelve la clausura, muestra el mecanismo entero:

```lisp
(defun crear-sumador (base)
  (lambda (k) (+ base k)))          ; base sobrevive a crear-sumador

(let ((f (crear-sumador 10)))
  (funcall f 1))                     ; => 11
```

Cuando `crear-sumador` termina, su marco de pila desaparece — pero `base` **no**, porque la lambda la
capturó y el compilador la movió al montículo. Ese es el **problema del funarg ascendente**, y
resolverlo bien fue uno de los grandes avances de Scheme en 1975; Common Lisp lo heredó.

Y las clausuras con **estado mutable** son objetos con todas las letras:

```lisp
(defun crear-contador ()
  (let ((n 0))
    (list (lambda () (incf n))        ; incrementar
          (lambda () n))))             ; leer
```

Dos funciones que **comparten** la misma `n` privada, inaccesible desde fuera. Eso es un objeto con
dos métodos y un campo encapsulado, construido solo con `let` y `lambda`.

Es el argumento clásico de que **objetos y clausuras son la misma idea**: en Lisp se construyen
objetos con clausuras, y en Smalltalk se construyen estructuras de control con bloques. Los dos
caminos llevan al mismo sitio.
"""),
        "tcl": ("""
gets stdin linea
set base [string trim $linea]

#  Tcl no tiene clausuras: los valores se "hornean" en un prefijo de comando.
set f1 [list apply {{b} {expr {$b + 1}}} $base]
set f2 [list apply {{b} {expr {$b + 2}}} $base]

puts "r1=[{*}$f1] r2=[{*}$f2]"
""", """
**Lo que esta clase enseña en Tcl.** **Tcl no tiene clausuras**: `apply` recibe una lambda —una lista
de dos o tres elementos— y sus argumentos, pero la lambda **no captura nada** del entorno donde se
escribió.

El idioma que la sustituye es el de este programa: **hornear los valores en un prefijo de comando**.
`[list apply {...} $base]` construye una lista que **contiene el valor de `base`**, y `{*}` la expande
como comando cuando toca.

```tcl
set f [list apply {{b k} {expr {$b + $k}}} 10]
{*}$f 5        ;# apply {...} 10 5  ->  15
```

Es **aplicación parcial** hecha con datos: el "entorno capturado" es literalmente parte de la lista
que representa al comando. En un lenguaje donde el código es una cadena, eso es lo natural.

Y `apply` tiene un tercer elemento opcional, el **espacio de nombres** donde se evalúa la lambda:

```tcl
apply {{x} {expr {$x * $factor}} ::miapp} 5    ;# $factor se busca en ::miapp
```

Con eso se consigue algo parecido a un entorno capturado, aunque compartido en lugar de privado.

La razón de fondo de que Tcl no tenga clausuras es su modelo: **las variables se resuelven por nombre
en tiempo de ejecución** (clase 080), y un entorno capturado exigiría reificar la tabla de variables.
`uplevel` y `upvar` cubren los casos que en otros lenguajes se resuelven capturando.
"""),
        "perl": ("""
use strict;
use warnings;

my $base = <STDIN>;
chomp $base;

my $f1 = sub { return $base + 1 };    # CAPTURA $base
my $f2 = sub { return $base + 2 };

print "r1=", $f1->(), " r2=", $f2->(), "\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl tiene **clausuras completas** desde la versión 5 (1994), y
son uno de los mecanismos más usados del lenguaje.

La forma canónica es la misma que en Lisp:

```perl
sub crear_sumador {
    my ($base) = @_;
    return sub { return $base + $_[0] };    # $base sobrevive
}

my $f = crear_sumador(10);
print $f->(1);      # 11
```

`$base` es una variable `my` de `crear_sumador`. Cuando la subrutina termina, **normalmente moriría**;
pero como la clausura la referencia, el conteo de referencias de la clase 081 la mantiene viva. Se
libera cuando la clausura desaparece.

Y con estado compartido se construyen objetos sin clases, el llamado **objeto en línea**:

```perl
sub crear_contador {
    my $n = 0;
    return {
        incr => sub { return ++$n },
        leer => sub { return $n },
    };
}
```

Dos clausuras compartiendo una `$n` verdaderamente privada — más privada que cualquier atributo de un
paquete de Perl, que siempre es accesible desde fuera. Es la **encapsulación por clausura**, y en Perl
es una técnica reconocida para datos que deben ser inaccesibles.

Hay una trampa clásica que conviene conocer: **capturar la variable del bucle**.

```perl
my @fs;
for my $i (1 .. 3) { push @fs, sub { $i } }    # correcto: `my $i` es NUEVA cada vuelta
```

En Perl funciona porque `my $i` en un `foreach` crea una variable nueva por iteración. En JavaScript
con `var` no, y ese es el error más famoso de las clausuras.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    int base{};
    if (!(std::cin >> base)) return 1;

    auto f1 = [base]() { return base + 1; };   // captura POR VALOR
    auto f2 = [base]() { return base + 2; };

    std::cout << "r1=" << f1() << " r2=" << f2() << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** Los corchetes de `[base]` son la **lista de captura**, y C++ es el
único lenguaje de esta página donde **hay que declarar explícitamente qué se captura y cómo**.

```cpp
[base]      // por VALOR: una copia
[&base]     // por REFERENCIA: si base muere, la clausura queda colgando
[=]         // todo lo usado, por valor
[&]         // todo lo usado, por referencia
[base = std::move(v)]   // captura con inicializador, C++14
[this]      // el objeto actual
```

Esa explicitud existe porque C++ **no tiene recolector**: si capturas por referencia algo que muere
antes que la clausura, tienes una referencia colgante y comportamiento indefinido. En Lisp, Perl o
JavaScript el recolector se encarga; aquí la decisión es tuya y el compilador no la comprueba.

Es la trampa número uno de las lambdas en C++:

```cpp
auto crear() {
    int x = 10;
    return [&x]() { return x; };    // ¡x muere al salir! COLGANTE
}
```

Con `[x]` sería correcto. Con `[&x]`, compila y falla.

Y la lambda **es un objeto**: el compilador genera una clase sin nombre con un `operator()` y un campo
por cada variable capturada. Se puede comprobar — `sizeof` de una lambda que captura un `int` es 4.
Eso confirma literalmente la tesis de esta clase: **una clausura es un objeto con un método**.

`std::function` puede guardar cualquier lambda, a costa de borrado de tipos e indirección; `auto`
conserva el tipo concreto y permite integrarla en línea.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller) main(Principal);

dcl-s base int(10) static;      // el "entorno": una global del módulo

dcl-proc Principal;
  dcl-pi *n;
    n int(10) const;
  end-pi;

  dcl-s salida char(50);

  base = n;
  salida = 'r1=' + %char(sumar(1)) + ' r2=' + %char(sumar(2));
  dsply salida;
end-proc;

dcl-proc sumar;
  dcl-pi *n int(10);
    k int(10) const;
  end-pi;
  return base + k;              // lee la global: no hay captura
end-proc;
""", """
**Lo que esta clase enseña en RPG.** **RPG no tiene clausuras, ni funciones anónimas, ni funciones de
primera clase con entorno.** Lo que hay es lo de este programa: **una variable estática del módulo y
una convención**.

Y esa combinación —variable `static` a nivel de módulo más procedimientos que la leen— es en realidad
un patrón conocido: **es un objeto con un solo ejemplar**. El módulo es la clase, las globales son los
campos y los procedimientos exportados son los métodos.

```rpgle
// modulo CONTADOR
dcl-s valor int(10) static;

dcl-proc incrementar export;
  valor += 1;
end-proc;

dcl-proc leer export;
  dcl-pi *n int(10); end-pi;
  return valor;
end-proc;
```

Eso es exactamente el "objeto en línea" de la ficha de Perl, construido con las herramientas de un
lenguaje que no tiene ni clausuras ni objetos. Y funciona: es el patrón dominante en el RPG moderno
bien escrito, y se llama **módulo con estado**.

Su limitación es la que cabe esperar: **hay un solo ejemplar**. No se pueden tener dos contadores
independientes sin duplicar el módulo o inventar un array indexado por identificador.

Para funciones como valor, RPG tiene los punteros a procedimiento de la clase 068 (`%paddr` y
`extproc`), sin entorno capturado — igual que Fortran y C.
"""),
        "pli": ("""
 clausura: procedure options(main);

    declare base fixed binary(31);

    get list (base);

    put skip list ('r1=' || trim(char(sumar(1))) ||
                   ' r2=' || trim(char(sumar(2))));

 sumar: procedure (k) returns (fixed binary(31));
    declare k fixed binary(31);
    return (base + k);       /* VE `base` del procedimiento que lo contiene */
 end sumar;

 end clausura;
""", """
**Lo que esta clase enseña en PL/I.** PL/I tiene **anidamiento léxico completo** desde 1964: un
procedimiento interno ve todas las variables de los que lo contienen, a cualquier profundidad. Es la
herencia de ALGOL, la misma que Pascal y Ada.

Lo que **no** tiene son clausuras de primera clase. Se puede pasar un procedimiento como argumento
—el tipo `entry` de la clase 068— pero **el entorno capturado solo vive mientras el anfitrión esté
activo**.

```pli
declare f entry;
f = sumar;              /* legal: se guarda la referencia */
call otra(f);           /* legal mientras `clausura` siga en la pila */
```

Si `clausura` termina y alguien llama a `f`, el resultado es indefinido: `base` ya no existe. PL/I
**no lo comprueba**, al contrario que Ada con su análisis de accesibilidad.

Y PL/I añade un mecanismo que sí resuelve el problema del contexto, aunque de otra manera: las
**variables `controlled`** de la clase 081, que forman una pila explícita.

```pli
declare contexto fixed binary(31) controlled;

allocate contexto;      /* apila un contexto nuevo */
contexto = 5;
call procesar;          /* todo lo llamado ve ESTE contexto */
free contexto;          /* y al liberar, vuelve el anterior */
```

Eso es exactamente **ámbito dinámico implementado a mano**, con la misma semántica que `new` en M y
`local` en Perl. Y hace ver que las dos ideas —clausura léxica y contexto dinámico— resuelven el
mismo problema práctico: **que una función vea algo que no le pasaron**.
"""),
        "mumps": ("""
CLAUSURA ; Cierres -- clase 083
 read base
 write "r1=", $$sumar(1), " r2=", $$sumar(2), !
 quit
 ;
sumar(k) ; suma k a la variable `base` del llamante (ambito DINAMICO)
 quit base + k
""", """
**Lo que esta clase enseña en M.** M **no tiene clausuras**, y no las necesita para este caso: **como
todas las variables son globales al proceso, `sumar` ve `base` sin capturarla**.

Eso parece resolver el problema, y es al mismo tiempo su gran diferencia con una clausura. Compara:

- **Clausura (léxica)**: la función recuerda **el entorno donde fue ESCRITA**. Dos clausuras creadas
  en momentos distintos recuerdan valores distintos.
- **Ámbito dinámico (M)**: la función ve **el entorno de quien la LLAMA**. La misma rutina ve cosas
  distintas según desde dónde se invoque.

La consecuencia práctica es que **en M no se pueden tener dos "sumadores" con bases distintas vivos a
la vez**. Solo hay una `base`, y vale lo que valga en el momento de la llamada.

Lo más cercano que M ofrece a una función como valor es la **indirección** de la clase 068:

```mumps
 set rutina = "CALCULAR^UTIL"
 do @rutina                      ; ejecuta lo que diga la variable
 set x = @("$$" _ funcion _ "(" _ arg _ ")")   ; construir la llamada como TEXTO
```

Se puede elegir qué se ejecuta y hasta construir la llamada concatenando cadenas. Lo que no hay es
entorno privado: **el estado siempre es el del proceso**.

Es el modelo más antiguo de todos —anterior incluso a que el ámbito léxico se considerara la opción
correcta— y sigue funcionando en producción porque las convenciones de `new` de la clase 082 lo
mantienen bajo control.
"""),
        "smalltalk": ("""
| base f1 f2 |

base := stdin nextLine trimBoth asNumber.

f1 := [ base + 1 ].      "un BLOQUE: captura base"
f2 := [ base + 2 ].

Transcript
    show: 'r1=', f1 value printString;
    show: ' r2=', f2 value printString;
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** **Un bloque es una clausura completa**, y lo ha sido desde
los años 70 — mucho antes que Lisp la popularizara fuera de la academia y treinta años antes de que
Java las tuviera.

`[ base + 1 ]` es un objeto de la clase `BlockClosure` que **captura el entorno léxico**: ve `base`,
las temporales del método, el receptor `self` y hasta el marco de activación. Se guarda, se pasa, se
devuelve y se evalúa con `value`.

Y esa capacidad es **la base de todo el lenguaje**, no una característica más. Como se ha visto a lo
largo de la Parte 4:

```smalltalk
cond ifTrue: [ ... ] ifFalse: [ ... ]     "condicional: clase 046"
[ cond ] whileTrue: [ ... ]                "bucle: clase 063"
1 to: n do: [ :i | ... ]                   "rango: clase 064"
col select: [ :x | ... ]                   "filtro: clase 067"
[ ... ] on: Error do: [ :e | ... ]         "excepciones: clase 071"
[ ... ] ensure: [ ... ]                    "finally"
dict at: k ifAbsent: [ ... ]               "valor por defecto: clase 072"
```

**Todas las estructuras de control del lenguaje son métodos que reciben clausuras.** Smalltalk no
tiene sintaxis de control porque no la necesita: con bloques baratos y envío de mensajes, se construye
todo.

Y el retorno no local de la clase 070 —`^` dentro de un bloque termina el **método** que lo creó—
significa que el bloque captura también el **contexto de retorno**, no solo las variables. Es una
clausura más potente que la de casi cualquier lenguaje, y la que permite escribir `detect:ifNone:` y
que se comporte como una construcción nativa.
"""),
    },
)

# ---------------------------------------------------------------------------
# 084 — Funciones puras y efectos secundarios
# ---------------------------------------------------------------------------
SPECS["084"] = dict(
    gancho="""
Elevar un número al cuadrado. La función más inocente posible, y la excusa para la pregunta que
define la programación funcional: **¿esta función hace algo más que devolver un valor?** Si no toca
nada de fuera, se puede memorizar, reordenar, paralelizar y probar sin montar nada. Y **Fortran es el
único lenguaje de esta página donde el compilador lo COMPRUEBA**.
""",
    porque="""
Aquí el concepto es la **pureza**, y estos lenguajes lo enseñan porque uno de ellos la convirtió en
palabra clave por un motivo puramente práctico. **`pure` en Fortran 95 no se añadió por elegancia
funcional: se añadió para poder paralelizar.** Una función pura se puede llamar desde un `forall` o un
`do concurrent` sin riesgo, y el compilador **rechaza** el código que la viole.

Ada llegó al mismo sitio desde otro lado, con `Global => null` y SPARK, por la certificación. Y en el
extremo opuesto, COBOL y M no tienen ningún concepto de pureza porque **todas sus variables son
globales**: la pregunta no se puede ni formular.
""",
    cierre="""
Lo transferible: **la pureza no es una preferencia estética, es una licencia para el compilador**. Si
una función es pura, se puede memorizar, eliminar si su resultado no se usa, ejecutar en otro hilo o
evaluar en compilación. Por eso `pure` está en Fortran, `constexpr` en C++ y `Global => null` en Ada:
los tres son promesas comprobadas a cambio de optimización. Y por eso, cuando un lenguaje no puede
comprobarlo, la pureza pasa a ser disciplina — que es exactamente lo que ocurre en el 80 % del código
de esta página.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. PURA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9)  COMP-3.
01  R       PIC S9(18) COMP-3.
01  ED-R    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N

    COMPUTE R = N * N

    MOVE R TO ED-R
    DISPLAY "puro=" FUNCTION TRIM(ED-R)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** **En COBOL la pureza no se puede ni expresar.** Un párrafo no
tiene parámetros ni retorno (clase 073) y todas las variables son globales (clase 082), así que
**cualquier párrafo puede modificar cualquier cosa**. No hay nada que declarar ni que comprobar.

Eso no significa que el concepto sea inútil ahí: significa que es **disciplina**. Las guías de estilo
de COBOL llevan décadas recomendando párrafos que "solo calculen", con una convención de nombres que
lo indique, y que los efectos —E/S, actualización de ficheros— estén concentrados en párrafos
separados. Es exactamente la separación entre núcleo puro y cáscara con efectos que hoy se predica en
arquitectura hexagonal.

Donde COBOL sí se acerca es en las **funciones definidas por el usuario** de COBOL 2002:

```cobol
IDENTIFICATION DIVISION.
FUNCTION-ID. CUADRADO.
DATA DIVISION.
LINKAGE SECTION.
01  X  PIC S9(9) COMP-3.
01  R  PIC S9(18) COMP-3.
PROCEDURE DIVISION USING X RETURNING R.
    COMPUTE R = X * X.
END FUNCTION CUADRADO.
```

Una `FUNCTION-ID` **tiene parámetros y valor de retorno**, y se puede usar dentro de una expresión:
`COMPUTE TOTAL = FUNCTION CUADRADO(A) + FUNCTION CUADRADO(B)`. Es lo más cerca que llega COBOL a una
función en el sentido matemático.

Sigue sin haber garantía de pureza —la función puede tener su propio `WORKING-STORAGE` estático y
acordarse de llamadas anteriores— pero al menos el flujo de datos entra y sale por la firma.
"""),
        "fortran": ("""
program pura
   implicit none
   integer :: n

   read(*, *) n
   write(*, '(A,I0)') 'puro=', cuadrado(n)

contains

   pure function cuadrado(x) result(r)
      integer, intent(in) :: x
      integer :: r
      r = x * x
   end function cuadrado

end program pura
""", """
**Lo que esta clase enseña en Fortran.** **`pure` es la única palabra clave de pureza COMPROBADA por el
compilador en toda esta página**, y Fortran la tiene desde **Fortran 95**.

Dentro de una función `pure` está **prohibido**:

- modificar cualquier argumento (todos deben ser `intent(in)` o `value`);
- modificar variables del anfitrión, de un módulo o `save`;
- ejecutar cualquier operación de **entrada/salida**;
- llamar a un procedimiento que no sea `pure`;
- ejecutar `stop`.

El compilador **rechaza** el código que lo viole. No es documentación: es un contrato.

Y no se añadió por convicción funcional. Se añadió porque **`forall` y `do concurrent` necesitan
garantizar que las iteraciones son independientes**:

```fortran
do concurrent (i = 1:n)
   v(i) = cuadrado(v(i))      ! solo es seguro si cuadrado es PURE
end do
```

Sin la garantía, el compilador no puede vectorizar ni mandar el bucle a la GPU. **La pureza es la
condición que habilita el paralelismo**, y por eso está en un lenguaje de cálculo numérico y no en uno
funcional.

Y `elemental` va un paso más allá: implica `pure` y hace que la función se aplique **elemento a
elemento sobre arrays de cualquier rango**:

```fortran
elemental function cuadrado(x) result(r)
...
w = cuadrado(v)        ! sobre un array entero, sin bucle
m = cuadrado(matriz)   ! y sobre una matriz
```

Existe además `impure elemental`, para el caso raro en que se quiere la aplicación elemento a elemento
pero con efectos. Que haya que escribir `impure` explícitamente dice mucho de las prioridades.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Pura is

   --  El contrato dice qué garantiza la función, y SPARK lo demuestra.
   function Cuadrado (X : Integer) return Integer
     with Post => Cuadrado'Result >= 0;

   function Cuadrado (X : Integer) return Integer is
   begin
      return X * X;
   end Cuadrado;

   N : Integer;
begin
   Get (N);

   Put ("puro=");
   Put (Cuadrado (N), Width => 1);
   New_Line;
end Pura;
""", """
**Lo que esta clase enseña en Ada.** Ada llegó a la pureza desde la **certificación**, no desde el
paralelismo, y su vocabulario lo refleja.

Hasta Ada 2005, una **función no podía tener parámetros `out`**, lo que la empujaba hacia la pureza
sin nombrarla. Y desde Ada 2012 hay contratos que la declaran explícitamente:

```ada
function Cuadrado (X : Integer) return Integer
  with Global => null,           --  NO accede a ninguna variable global
       Pre    => X in -46340 .. 46340,   --  no desborda
       Post   => Cuadrado'Result = X * X;
```

`Global => null` es la declaración de pureza, y **SPARK la demuestra estáticamente**: no comprueba en
ejecución, **prueba** que la función no toca nada de fuera. Si accede a una global sin declararla, el
analizador lo rechaza.

Y `Pre`/`Post` van más lejos que la pureza: describen **qué exige y qué garantiza**. Con SPARK, la
precondición se demuestra en cada sitio de llamada, y si se demuestra, la comprobación en ejecución se
elimina.

Ada tiene además el `pragma Pure` a nivel de **paquete completo**, que declara que un paquete no tiene
estado y permite al compilador compartir su código entre particiones distribuidas.

La comparación con Fortran es instructiva: **los dos llegaron a la misma característica por motivos
opuestos** —uno para paralelizar, otro para certificar— y la implementaron casi igual. Es una señal
bastante clara de que la pureza es una propiedad útil con independencia del paradigma.
"""),
        "pascal": ("""
program Pura;
{$MODE OBJFPC}{$H+}
uses SysUtils;

function Cuadrado(X: Integer): Int64;
begin
  Result := Int64(X) * X;
end;

var
  N: Integer;

begin
  Read(N);
  WriteLn('puro=', IntToStr(Cuadrado(N)));
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal **no tiene ninguna forma de declarar pureza**, y la
distinción `function` / `procedure` es lo más cerca que llega: por convención, una **función devuelve
un valor y no debería tener efectos**; un **procedimiento** hace algo.

Wirth lo consideraba una regla de estilo, no del lenguaje. Y el propio Pascal la incumple: nada impide
que una función modifique una global o escriba en un fichero.

Ese es un caso claro de lo que esta clase quiere mostrar: **una convención sin comprobación es una
convención que se rompe**. El código Pascal real está lleno de funciones con efectos, y la única forma
de saberlo es leerlas.

Free Pascal y Delphi añadieron `const` en los parámetros (clase 079), que impide modificar el
argumento — la mitad del problema. Lo que falta es impedir el acceso a globales.

Fíjate también en `Int64(X) * X` de este programa: la conversión **antes** de multiplicar. Sin ella, la
multiplicación se haría en `Integer` de 32 bits y desbordaría con valores grandes antes de promocionar
al `Int64` del resultado. Es un error clásico que ninguna anotación de pureza evita, y que aparece en
todos los lenguajes con tipos enteros de ancho fijo:

```pascal
Result := X * X;          { desborda en Integer y LUEGO promociona }
Result := Int64(X) * X;   { correcto: la multiplicación ya es de 64 bits }
```
"""),
        "lisp": ("""
(defun cuadrado (x)
  (* x x))

(let ((n (read)))
  (format t "puro=~D~%" (cuadrado n)))
""", """
**Lo que esta clase enseña en Common Lisp.** Common Lisp **no es un lenguaje puro** y no tiene forma
estándar de declarar pureza — es multiparadigma y `setf` está por todas partes.

Lo que sí tiene son **declaraciones de optimización que dependen de la pureza**, y SBCL las aprovecha:

```lisp
(declaim (ftype (function (fixnum) fixnum) cuadrado))
(defun cuadrado (x)
  (declare (optimize (speed 3)) (type fixnum x))
  (the fixnum (* x x)))
```

Y hay una construcción que **explota la pureza directamente**: las **funciones incorporadas marcadas
como "flushable" y "foldable"** en el compilador. Si SBCL sabe que una función es pura y su resultado
no se usa, **elimina la llamada entera**; si sus argumentos son constantes, la **evalúa al compilar**.

```lisp
(defun f () (sqrt 2.0))     ; SBCL calcula la raíz AL COMPILAR
```

Eso es exactamente `constexpr` de C++, deducido en lugar de declarado.

Y la comunidad Lisp aporta a esta clase el concepto que da nombre a todo esto: **la transparencia
referencial**. Una expresión es transparente si se puede sustituir por su valor sin cambiar el
programa. Con `(cuadrado 4)` se puede; con `(read)` no.

Ese es el criterio operativo de la pureza, y es más útil que la definición formal: **¿puedo sustituir
la llamada por su resultado?** Si sí, es pura, y entonces se puede memorizar —la técnica de la clase
069— reordenar y paralelizar.
"""),
        "tcl": ("""
proc cuadrado {x} {
    return [expr {$x * $x}]
}

gets stdin linea
set n [string trim $linea]

puts "puro=[cuadrado $n]"
""", """
**Lo que esta clase enseña en Tcl.** Tcl **no tiene ninguna noción de pureza**, y no puede tenerla
fácilmente: cualquier procedimiento puede usar `global`, `upvar` o `uplevel` para tocar el entorno de
quien lo llama (clases 080 y 082).

De hecho, `uplevel` hace que **ni siquiera se pueda saber estáticamente qué toca un procedimiento**,
porque el código que evalúa puede venir de una cadena construida en ejecución.

Lo que Tcl sí ofrece, y encaja en esta clase, es una forma muy directa de aprovechar la pureza cuando
existe: **la memorización con un array**.

```tcl
proc cuadrado {x} {
    global memo
    if {[info exists memo($x)]} { return $memo($x) }
    set memo($x) [expr {$x * $x}]
    return $memo($x)
}
```

Ese patrón —comprobar la caché, calcular, guardar— es la aplicación práctica de la pureza, y solo es
correcto **si la función es pura**. Si dependiera de algo externo que cambia, la caché devolvería
resultados obsoletos.

Es exactamente la memorización de la ficha de Lisp de la clase 069, y la razón de que esta clase
importe aunque el lenguaje no la comprueba: **la pureza es lo que hace que una optimización sea
correcta**.

Y hay una ironía útil: los **valores de Tcl son inmutables** (clase 081), así que en la práctica una
gran parte del código Tcl es más puro de lo que parece — lo que se modifica son variables, no valores
compartidos.
"""),
        "perl": ("""
use strict;
use warnings;

sub cuadrado {
    my ($x) = @_;
    return $x * $x;
}

my $n = <STDIN>;
chomp $n;

print "puro=", cuadrado($n), "\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl no tiene declaración de pureza, y **su modelo de `@_` la
dificulta especialmente**: como los argumentos son alias (clase 080), una subrutina puede modificar
las variables del llamante sin que nada lo indique.

Por eso `my ($x) = @_;` no es solo comodidad: **es lo que hace pura a la función**. Sin esa línea,
cualquier escritura en `$_[0]` sería un efecto secundario invisible.

Lo que Perl sí tiene es una **memorización de una sola línea**, gracias a `Memoize`, un módulo del
núcleo:

```perl
use Memoize;
memoize('cuadrado');       # a partir de aquí, cachea los resultados
```

`memoize` **reemplaza la subrutina por una envoltura con caché** en tiempo de ejecución, sin tocar su
código. Es posible porque en Perl la tabla de símbolos es modificable —`*cuadrado = sub {...}`— y es
el mismo mecanismo que `rename` en Tcl (clase 073).

Y funciona **solo si la función es pura**. La documentación de `Memoize` lo dice explícitamente y
enumera los casos en que no debe usarse: funciones con efectos, que dependan del tiempo, del estado
global o del contexto.

Perl 5.36 añadió además los **atributos de subrutina** `:const` y `:lvalue`, y el pragma `builtin`
con funciones que el compilador sabe puras. Son pasos pequeños hacia lo que Fortran tiene desde 1995.
"""),
        "cpp": ("""
#include <iostream>

//  constexpr: se puede evaluar en tiempo de COMPILACIÓN si los argumentos
//  se conocen. Implica restricciones muy parecidas a la pureza.
constexpr long long cuadrado(int x) {
    return static_cast<long long>(x) * x;
}

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    static_assert(cuadrado(4) == 16);      // comprobado AL COMPILAR

    std::cout << "puro=" << cuadrado(n) << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** **`constexpr` es la pureza de C++**, aunque no se llame así. Una
función `constexpr` **no puede** tener efectos observables: no puede modificar globales, no puede
hacer E/S, y **si sus argumentos se conocen al compilar, se evalúa entonces**.

El `static_assert` de este programa lo demuestra: `cuadrado(4)` se calcula **durante la compilación** y
el resultado se comprueba ahí mismo. Si fuera 15, el programa no compilaría.

Y la misma función sirve para las dos cosas: con `n` leído de la entrada, se ejecuta normalmente. Es
una propiedad muy práctica — no hay que escribir dos versiones.

C++ ha ido acumulando calificadores en esta línea, y conviene distinguirlos:

| | Qué promete |
|---|---|
| `constexpr` | **Puede** evaluarse al compilar |
| `consteval` (C++20) | **Debe** evaluarse al compilar; si no, error |
| `constinit` (C++20) | Se inicializa en compilación, pero no es constante |
| `noexcept` | No lanza |
| `[[nodiscard]]` | Avisa si se ignora el resultado — típico de funciones puras |
| `const` (método) | No modifica el objeto |

Lo que C++ **no** tiene es una declaración de "esta función no toca ninguna global" para el caso
general en ejecución. GCC y Clang ofrecen los atributos `__attribute__((pure))` y `((const))`, que
habilitan optimizaciones fuertes —eliminar llamadas repetidas— pero **no los comprueban**: si mientes,
el resultado es comportamiento indefinido.

Ahí está la diferencia con Fortran: **una promesa comprobada frente a una promesa creída**.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi PURA;
  n int(10) const;
end-pi;

dcl-s salida char(40);

salida = 'puro=' + %char(cuadrado(n));
dsply salida;

*inlr = *on;
return;

dcl-proc cuadrado;
  dcl-pi *n int(20);
    x int(10) const;      // const: no modifica el argumento
  end-pi;
  return x * x;           // y no toca ninguna global
end-proc;
""", """
**Lo que esta clase enseña en RPG.** RPG **no tiene declaración de pureza**, y su equivalente práctico
es una combinación de dos cosas que sí se declaran:

1. **`const` en todos los parámetros** — garantiza que no se modifican (clase 079).
2. **Ninguna variable global del módulo** — que no se puede declarar, solo respetar.

La segunda es la que falta, y es exactamente el problema de esta clase: **la mitad de la pureza es
comprobable y la otra mitad es disciplina**.

RPG tiene además una palabra que va en la dirección contraria y que conviene conocer, porque su
presencia delata que un procedimiento **no** es puro:

```rpgle
dcl-proc contador;
  dcl-s n int(10) static;    // STATIC: recuerda entre llamadas
  n += 1;
  return n;
end-proc;
```

`static` en una variable local es la marca de estado entre invocaciones (clase 069). Un procedimiento
con `static` **nunca es puro**, y buscar esa palabra es la forma práctica de auditar un módulo.

Y hay una razón por la que esto importa mucho en IBM i: los procedimientos de un **módulo de servicio**
se comparten entre trabajos, y un `static` mal usado puede filtrar datos de un usuario a otro. Es un
problema de seguridad, no solo de corrección, y la guía de la plataforma insiste en que el estado
compartido se declare y se justifique.
"""),
        "pli": ("""
 pura: procedure options(main);

    declare n fixed binary(31);

    get list (n);
    put skip list ('puro=' || trim(char(cuadrado(n))));

 cuadrado: procedure (x) returns (fixed binary(31));
    declare x fixed binary(31);
    return (x * x);
 end cuadrado;

 end pura;
""", """
**Lo que esta clase enseña en PL/I.** PL/I **no tiene ninguna noción de pureza**, y su modelo la hace
especialmente difícil de garantizar: el paso por referencia por defecto (clase 080) significa que
cualquier procedimiento puede modificar sus argumentos, y el anidamiento léxico (clase 083) le da
acceso a todo lo que lo contenga.

Lo que PL/I sí tiene, y es una idea de esta clase, son las **funciones incorporadas matemáticas
declaradas como tales**: `sqrt`, `sin`, `log`, `abs`, `mod`, `max`. El compilador **sabe que son
puras** y las evalúa en compilación cuando los argumentos son constantes.

```pli
declare tabla(10) float initial((10) 0);
x = sqrt(2);      /* el compilador puede calcularlo al compilar */
```

Es el mismo mecanismo que el *constant folding* de cualquier compilador moderno, y funciona
únicamente porque la pureza de esas funciones **está codificada en el compilador**, no declarada por
el programador.

Esa es, en el fondo, la observación que cierra esta clase para toda la sección: **todos estos
lenguajes aprovechan la pureza cuando la conocen**. Lo que cambia es quién se lo dice al compilador:

- **Fortran**: el programador, con `pure`, y se comprueba.
- **Ada/SPARK**: el programador, con `Global => null`, y se demuestra.
- **C++**: el programador, con `constexpr`, y se comprueba parcialmente.
- **Lisp, PL/I, COBOL**: solo lo sabe el compilador de sus propias intrínsecas.
- **Tcl, Perl, M, RPG**: nadie; es disciplina.

Y esa escala —de la garantía a la costumbre— es exactamente lo que separa a un lenguaje que puede
paralelizar automáticamente de uno que no.
"""),
        "mumps": ("""
PURA ; Funciones puras -- clase 084
 read n
 write "puro=", $$cuadrado(n), !
 quit
 ;
cuadrado(x) ; devuelve x al cuadrado
 quit x * x
""", """
**Lo que esta clase enseña en M.** **En M la pureza es prácticamente inexpresable.** Todas las
variables son globales al proceso (clase 082), cualquier rutina puede leerlas y escribirlas, y la
indirección (clase 068) permite ejecutar código construido en tiempo de ejecución.

Ni siquiera se puede saber **estáticamente qué toca una rutina**.

Y hay un motivo de fondo que va más allá del lenguaje: **en M, el efecto secundario es el propósito**.
Un sistema clínico existe para escribir en `^PACIENTE`, no para calcular valores. La operación
central del lenguaje —`set ^GLOBAL(clave) = valor`— es una escritura en disco visible
inmediatamente para todos los procesos (clase 054).

En ese modelo, una función pura es la excepción, no la norma.

Lo que M sí tiene, y es lo que ocupa el lugar de las garantías de pureza, es el **control de
concurrencia**:

```mumps
 lock +^PACIENTE(id)          ; bloqueo cooperativo sobre ese nodo
 tstart                        ; inicio de TRANSACCIÓN
 set ^PACIENTE(id,"saldo") = nuevo
 tcommit
 lock -^PACIENTE(id)
```

`lock`, `tstart`, `tcommit` y `trollback` dan atomicidad y aislamiento sobre los efectos. Es la
respuesta de una base de datos al mismo problema que la pureza resuelve en un lenguaje funcional:
**hacer que los efectos sean predecibles**.

Dos estrategias opuestas —evitar los efectos o controlarlos transaccionalmente— y las dos llevan
décadas funcionando en producción.
"""),
        "smalltalk": ("""
| n |

n := stdin nextLine trimBoth asNumber.

Transcript show: 'puro=', (n * n) printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk **no tiene declaración de pureza**, y su modelo
—objetos con estado que se envían mensajes— está construido alrededor del efecto: un mensaje suele
cambiar el estado del receptor.

Pero la comunidad Smalltalk aportó a esta clase una distinción de diseño que hoy es doctrina y que se
enseña con su nombre: **la separación entre consulta y orden** (*command-query separation*), formulada
por Bertrand Meyer en el contexto de Eiffel, muy cercano a este mundo.

> **Un método o bien devuelve un valor y no cambia nada, o bien cambia algo y no devuelve nada. Nunca
> las dos cosas.**

Y la biblioteca de Smalltalk la sigue de forma muy visible, con una convención de nombres que la hace
evidente:

```smalltalk
coleccion size            "CONSULTA: pura"
coleccion sorted          "CONSULTA: devuelve una copia ordenada"
coleccion sort            "ORDEN: ordena en el sitio, devuelve self"
cadena asUppercase        "CONSULTA: una copia nueva"
cadena reversed           "CONSULTA"    vs   reverse  "ORDEN"
```

El participio (`sorted`, `reversed`) para la versión pura y el imperativo (`sort`, `reverse`) para la
que muta. Es la misma convención que Ruby resuelve con el sufijo `!` y que Lisp resuelve con el
prefijo `n` de la clase 054.

Que tres comunidades distintas hayan inventado una marca tipográfica para lo mismo dice bastante: **si
el lenguaje no distingue lo puro de lo impuro, los programadores lo distinguen en los nombres**.
"""),
    },
)
