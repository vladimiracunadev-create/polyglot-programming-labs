# -*- coding: utf-8 -*-
"""Parte 5, lote A — clases 073 a 078. Ver `vivos_parte5.py` y `gen_vivos.py`.

El código de los ocho lenguajes de la sección 🟢 se ejecuta en CI contra el
`casos.json` de la clase (`scripts/verificar_vivos.py`).
"""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 073 — Firma: parámetros, argumentos y retorno
# ---------------------------------------------------------------------------
SPECS["073"] = dict(
    gancho="""
Una función que suma dos enteros. El programa más simple de la Parte 5, elegido porque obliga a
responder la pregunta fundacional: **¿qué es exactamente una función en este lenguaje?** Y la
respuesta más sorprendente de esta página es la de COBOL, donde la unidad de código reutilizable
—el párrafo— **no tiene parámetros ni valor de retorno**: todo son variables globales.
""",
    porque="""
Aquí el concepto es la **firma como contrato**, y estos lenguajes lo enseñan porque muestran los tres
niveles históricos. El primero: **COBOL con `PERFORM`**, que ejecuta un bloque de código sin
argumentos ni retorno — literalmente un `goto` con vuelta. El segundo: **el subprograma con
parámetros**, que es lo que trajeron FORTRAN II, ALGOL y todos los demás. Y el tercero: **el modo de
cada parámetro declarado en la firma** —`intent(in)` de Fortran, `in`/`out`/`in out` de Ada— que dice
no solo qué recibe una función, sino **qué va a hacer con ello**.

Ese tercer nivel es el que casi ningún lenguaje del núcleo tiene, y el que hace legible una firma sin
leer el cuerpo.
""",
    cierre="""
Lo transferible: **una firma dice cuatro cosas, y muchos lenguajes solo escriben dos**. El nombre y
los tipos casi todos; **la dirección de cada parámetro** solo Fortran, Ada, Pascal y PL/I; y **qué
efectos tiene la función** solo Fortran (`pure`), Ada (`Global => null`) y C++ (`const`, `noexcept`,
`[[nodiscard]]`). Cuanto más dice la firma, menos hay que leer el cuerpo — y eso es exactamente el
valor de una función como unidad de abstracción.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. SUMAR.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TXT-A   PIC X(20).
01  TXT-B   PIC X(20).
01  A       PIC S9(9)  COMP-3.
01  B       PIC S9(9)  COMP-3.
01  R       PIC S9(18) COMP-3.
01  ED-R    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    PERFORM CALCULAR-SUMA

    MOVE R TO ED-R
    DISPLAY "suma=" FUNCTION TRIM(ED-R)
    STOP RUN.

CALCULAR-SUMA.
    COMPUTE R = A + B.
""", """
**Lo que esta clase enseña en COBOL.** **`CALCULAR-SUMA` no tiene parámetros, no tiene retorno y no
tiene ámbito propio.** Es un párrafo: una etiqueta con código debajo. `PERFORM` salta ahí, ejecuta y
vuelve. Lee `A` y `B` porque son **globales**, y deja el resultado en `R` porque también lo es.

Eso es lo que hay que ver de esta clase: en el COBOL clásico, **la comunicación entre unidades de
código es por variables compartidas**, no por argumentos. Un programa de cinco mil líneas con
cuarenta párrafos tiene cuarenta trozos de código que leen y escriben el mismo `WORKING-STORAGE`, y
saber qué toca cada uno exige leerlos todos.

Ese es, con diferencia, el mayor problema de mantenimiento del COBOL heredado, y no tiene que ver con
la sintaxis: tiene que ver con no haber tenido parámetros.

COBOL sí tiene subprogramas de verdad, con firma, desde el principio — pero son **programas
separados**:

```cobol
CALL "CALCULAR" USING BY REFERENCE A, BY CONTENT B, BY VALUE C
                RETURNING RESULTADO
```

`BY REFERENCE` (el defecto), `BY CONTENT` (copia) y `BY VALUE` **están en el sitio de la llamada**,
no en la declaración — al revés que en casi todos los lenguajes. Y COBOL 2002 añadió `FUNCTION-ID`
para definir funciones con valor de retorno usables dentro de una expresión.

En la práctica, el código moderno mezcla: párrafos para la estructura interna y programas o funciones
para lo que se reutiliza.
"""),
        "fortran": ("""
program sumar
   implicit none
   integer :: a, b

   read(*, *) a, b
   write(*, '(A,I0)') 'suma=', suma(a, b)

contains

   pure function suma(x, y) result(s)
      integer, intent(in) :: x, y
      integer :: s
      s = x + y
   end function suma

end program sumar
""", """
**Lo que esta clase enseña en Fortran.** Esta firma de cuatro líneas dice **más que la mayoría de las
firmas del núcleo**, y conviene desglosarla:

- **`pure`** — la función **no tiene efectos secundarios**: no modifica sus argumentos, no toca
  variables globales, no hace E/S. El compilador lo **comprueba**, y a cambio puede llamarla desde un
  `do concurrent` y paralelizarla, o eliminar llamadas repetidas.
- **`intent(in)`** — los parámetros son de **solo lectura**. Intentar modificarlos no compila. Los
  otros modos son `intent(out)` (el valor de entrada no existe) e `intent(inout)`.
- **`result(s)`** — nombra la variable del resultado, en lugar de asignar al nombre de la función.

Los tres son **opcionales en el estándar y obligatorios en cualquier código serio**, y las guías de
estilo de la comunidad los exigen. La razón es práctica: en Fortran los argumentos se pasan **por
referencia por defecto**, así que sin `intent` no hay forma de saber, leyendo la llamada, si la
función va a modificar lo que le pasas.

`pure` merece un apunte más. Existe también `elemental`, que implica `pure` y además hace que la
función se aplique **elemento a elemento sobre arrays** —lo que se vio en la clase 060 con `max`—.
Declarar una función `elemental` la convierte en aplicable a escalares y a arrays de cualquier rango,
gratis.

Es un nivel de información en la firma que solo Ada iguala.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Sumar is

   function Suma (X, Y : Integer) return Integer is
   begin
      return X + Y;
   end Suma;

   A, B : Integer;
begin
   Get (A);
   Get (B);

   Put ("suma=");
   Put (Suma (A, B), Width => 1);
   New_Line;
end Sumar;
""", """
**Lo que esta clase enseña en Ada.** Ada distingue **procedimiento** de **función** de forma
tajante, y esa distinción no es cosmética:

```ada
procedure Guardar (Dato : in Registro);              --  hace algo; NO devuelve
function  Calcular (X : Integer) return Integer;     --  devuelve; en Ada 83, SIN efectos
```

Hasta Ada 2012, **una función no podía tener parámetros `out`**: si algo devolvía un valor, no podía
además modificar sus argumentos. Era una forma de empujar hacia funciones puras sin llamarlas así.

Y los **modos de parámetro** son la aportación de Ada a esta clase:

| Modo | Significado | Implementación |
|---|---|---|
| `in` | Solo lectura, es el defecto | Por valor o referencia, **decide el compilador** |
| `out` | Solo escritura; el valor de entrada no existe | El compilador comprueba que se asigne |
| `in out` | Se lee y se modifica | |

Fíjate en la columna de la derecha: **Ada no dice cómo se pasa un parámetro, dice qué se puede hacer
con él**. El compilador elige valor o referencia según el tamaño y el tipo. Eso es una abstracción
más alta que la de C++ —donde `const T&` mezcla la intención con el mecanismo— y permite optimizar
sin que el programador se meta.

Ada 2012 añadió los **contratos** —`with Pre`, `with Post`, `with Global => null`— que llevan la
firma más lejos todavía: qué exige, qué garantiza y a qué variables globales accede. Con SPARK, todo
eso se demuestra.
"""),
        "pascal": ("""
program Sumar;
{$MODE OBJFPC}{$H+}
uses SysUtils;

function Suma(X, Y: Integer): Integer;
begin
  Result := X + Y;
end;

var
  A, B: Integer;

begin
  Read(A, B);
  WriteLn('suma=', IntToStr(Suma(A, B)));
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal separa **`function`** (devuelve) de **`procedure`** (no
devuelve) igual que Ada, y fue quien inventó esa distinción — Ada la heredó.

Y tiene tres formas de pasar parámetros, declaradas **en la firma**:

```pascal
procedure P(A: Integer);          { por VALOR: copia }
procedure P(var A: Integer);      { por REFERENCIA: se puede modificar }
procedure P(const A: TRegistro);  { por referencia, pero de SOLO LECTURA }
procedure P(out A: Integer);      { solo salida (Delphi/FPC) }
```

`const` merece atención porque resuelve un problema real: pasar un registro grande **por valor**
copia todos sus bytes; pasarlo con `var` evita la copia pero permite modificarlo. `const` da lo mejor
de los dos —sin copia y sin escritura—, y es exactamente lo que en C++ se escribe `const T&`.

Sobre el retorno, Object Pascal tiene una peculiaridad: **`Result`** es una variable implícita
declarada por el compilador.

```pascal
function Contar: Integer;
begin
  Result := 0;
  while ... do Inc(Result);      { se puede leer y escribir varias veces }
end;
```

No es una palabra de retorno como `return`: es un **lugar**, así que se puede acumular en él. El
Pascal ISO usaba el nombre de la función —`Contar := 0`— que era ambiguo con la llamada recursiva.
`Result` lo resolvió, y `Exit(valor)` de Delphi 2009 añadió por fin el `return` inmediato.
"""),
        "lisp": ("""
(defun suma (x y)
  "Devuelve la suma de X e Y."
  (+ x y))

(let* ((a (read))
       (b (read)))
  (format t "suma=~D~%" (suma a b)))
""", """
**Lo que esta clase enseña en Common Lisp.** La cadena que va después de la lista de parámetros no es
un comentario: es la **cadena de documentación**, y **forma parte del objeto función**.

```lisp
(documentation 'suma 'function)     ; => "Devuelve la suma de X e Y."
(describe 'suma)                     ; muestra firma, tipo, documentación...
```

En el REPL, `C-c C-d d` sobre cualquier símbolo muestra su documentación **del sistema vivo**, no de
un fichero aparte. Python copió la idea con los *docstrings*, y viene de aquí.

Y la **lambda-lista** de Common Lisp es de las más ricas que existen: en una sola declaración caben
posicionales, opcionales con valor por defecto, variádicos y nombrados.

```lisp
(defun f (a b                        ; obligatorios
          &optional (c 10) d         ; opcionales, con y sin defecto
          &rest resto                ; variádicos
          &key (color :rojo) tamano  ; NOMBRADOS
          &aux (tmp (* a b))))       ; variables auxiliares, no son parámetros
```

Las clases 074, 075 y 076 estudian por separado lo que aquí aparece junto. Que un lenguaje de 1984
tenga las cuatro formas de parámetro con una sintaxis unificada, y que Python llegara a algo casi
idéntico treinta años después de forma independiente, dice bastante sobre cuáles son las necesidades
reales.

Y en Lisp **una función es un objeto**: `#'suma` la obtiene, `(funcall f 1 2)` la llama,
`(setf (symbol-function 'suma) otra)` la redefine en caliente.
"""),
        "tcl": ("""
proc suma {x y} {
    return [expr {$x + $y}]
}

gets stdin linea
lassign [split [string trim $linea]] a b

puts "suma=[suma $a $b]"
""", """
**Lo que esta clase enseña en Tcl.** `proc` es **un comando que crea comandos**. No es una palabra
clave: recibe tres argumentos —nombre, lista de parámetros y cuerpo— y registra un comando nuevo en
el intérprete.

La consecuencia es que **los procedimientos se pueden crear, inspeccionar y destruir en ejecución**:

```tcl
proc suma {x y} { ... }
info body suma          ;# devuelve el CUERPO como una cadena
info args suma          ;# devuelve {x y}
rename suma sumaVieja   ;# cambiarle el nombre
rename suma {}          ;# BORRARLO
proc suma {x y} {...}   ;# y redefinirlo
```

`rename` es la clave de una técnica muy usada en Tcl: **envolver un comando existente**, incluidos
los del propio lenguaje.

```tcl
rename puts puts_original
proc puts {args} {
    puts_original "LOG: $args"
    uplevel 1 puts_original $args
}
```

Acabas de instrumentar `puts` en todo el programa sin tocar ninguna llamada. Es lo que en otros
lenguajes se llama *monkey patching* o instrumentación, y en Tcl es una operación de dos líneas
porque **los comandos son entradas en una tabla, no símbolos compilados**.

Sobre el retorno: `return` es también un comando, y si se omite, un `proc` devuelve **el valor de la
última sentencia** — como en Lisp, Ruby y Rust.
"""),
        "perl": ("""
use strict;
use warnings;

sub suma {
    my ($x, $y) = @_;
    return $x + $y;
}

my $linea = <STDIN>;
chomp $linea;
my ($p, $q) = split ' ', $linea;

print "suma=", suma($p, $q), "\\n";
""", """
**Lo que esta clase enseña en Perl.** Durante treinta años, **una subrutina de Perl no tenía firma**:
todos los argumentos llegaban aplanados en el array `@_`, y desempaquetarlos era responsabilidad del
programador.

```perl
sub suma { my ($x, $y) = @_; ... }     # el idioma universal
```

Eso significa que **el número de argumentos no se comprueba**: llamar `suma(1)` o `suma(1,2,3)`
compila y se ejecuta, dejando `$y` sin definir o ignorando el tercero. Es la fuente de errores más
común del Perl clásico.

Y `@_` tiene una propiedad que sorprende y que ya apareció en la clase 054: **sus elementos son
alias de los argumentos originales**, no copias.

```perl
sub doblar { $_[0] *= 2 }
my $x = 5;
doblar($x);        # ¡$x ahora vale 10!
```

Modificar `@_` modifica las variables del llamante. Es paso por referencia implícito, y es la razón
de que el idioma sea copiar a variables `my` en la primera línea.

**Perl 5.36 estabilizó las firmas**, y hoy se escriben así:

```perl
use v5.36;
sub suma ($x, $y) { return $x + $y }        # aridad COMPROBADA
sub pot ($base, $exp = 2) { ... }           # con valor por defecto
sub total ($primero, @resto) { ... }        # variádicos
```

Con firma, llamar con el número equivocado de argumentos **es un error**. Es un cambio grande para un
lenguaje de 1987, y la razón de que el material moderno se vea tan distinto del de los 90.
"""),
        "cpp": ("""
#include <iostream>

int suma(int x, int y) {
    return x + y;
}

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::cout << "suma=" << suma(a, b) << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** La firma de C++ es donde más información se puede poner, y el
código moderno la usa entera:

```cpp
[[nodiscard]] constexpr int suma(int x, int y) noexcept;
```

- **`[[nodiscard]]`** (C++17) — el compilador **avisa si se ignora el valor devuelto**. Para una
  función pura, ignorar el resultado significa que la llamada no hizo nada.
- **`constexpr`** — se puede evaluar en tiempo de compilación (clase 069).
- **`noexcept`** — promete no lanzar. Permite optimizaciones y es lo que hace que `std::vector`
  **mueva** en vez de copiar al crecer.

Y C++ tiene la sobrecarga, que en esta clase importa: **la firma incluye los tipos de los
parámetros**, así que puede haber varias funciones con el mismo nombre.

```cpp
int  suma(int, int);
double suma(double, double);
```

Eso obliga al compilador a un proceso de **resolución de sobrecarga** que es una de las partes más
complejas del lenguaje: conversiones implícitas, plantillas, promociones… y la razón de que los
mensajes de error de C++ sean legendarios.

Sobre el paso de parámetros, la guía moderna es una tabla corta:

```cpp
void f(int x);                  // barato: por valor
void f(const std::string& s);   // solo lectura, sin copiar
void f(std::string& s);         // se va a modificar
void f(std::string s);          // se va a QUEDAR con él (y se mueve al llamar)
```

Elegir mal no es un error de compilación: es una copia silenciosa. Las clases 079 y 081 vuelven sobre
esto.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi SUMAR;
  a int(10) const;
  b int(10) const;
end-pi;

dcl-s salida char(40);

salida = 'suma=' + %char(suma(a : b));
dsply salida;

*inlr = *on;
return;

dcl-proc suma;
  dcl-pi *n int(20);
    x int(10) const;
    y int(10) const;
  end-pi;
  return x + y;
end-proc;
""", """
**Lo que esta clase enseña en RPG.** RPG separa el **prototipo** (`dcl-pr`) de la **interfaz**
(`dcl-pi`), y esa distinción confunde al principio:

```rpgle
dcl-pr suma int(20);            // PROTOTIPO: cómo se LLAMA (para el que llama)
  x int(10) const;
  y int(10) const;
end-pr;

dcl-proc suma;
  dcl-pi *n int(20);            // INTERFAZ: cómo se DEFINE (dentro del procedimiento)
    x int(10) const;
    y int(10) const;
  end-pi;
  ...
end-proc;
```

Es exactamente la pareja declaración/definición de C —el `.h` y el `.c`—, con la ventaja de que RPG
**comprueba que coincidan** si están en el mismo fuente. El `*n` de la interfaz significa "sin nombre":
lo toma del `dcl-proc`.

Y el vocabulario de la firma de RPG es rico:

```rpgle
dcl-pi *n int(10);
  a int(10) const;              // const: no se modifica, admite expresiones
  b int(10) value;              // por VALOR: copia
  c char(10);                   // por referencia (el DEFECTO)
  d int(10) options(*nopass);   // OPCIONAL (clase 074)
  e char(100) options(*varsize);// tamaño variable
end-pi;
```

**El paso por referencia es el defecto**, herencia de la época en que copiar era caro. `const` y
`value` son las formas modernas y las que se recomiendan, porque hacen visible en la firma si el
argumento puede cambiar — el mismo problema que Fortran resolvió con `intent`.
"""),
        "pli": ("""
 sumar: procedure options(main);

    declare (a, b) fixed binary(31);

    get list (a, b);
    put skip list ('suma=' || trim(char(suma(a, b))));

 suma: procedure (x, y) returns (fixed binary(31));
    declare (x, y) fixed binary(31);
    return (x + y);
 end suma;

 end sumar;
""", """
**Lo que esta clase enseña en PL/I.** La firma de PL/I introduce un concepto que casi ningún lenguaje
moderno hace explícito: **`entry`**, el tipo de una referencia a procedimiento.

```pli
declare suma entry (fixed binary(31), fixed binary(31))
             returns (fixed binary(31));
```

Eso es un **prototipo**, y como en RPG y en C, permite al compilador comprobar las llamadas antes de
ver la definición. Sin él, PL/I asume una firma y los errores aparecen en ejecución.

Y el paso de parámetros de PL/I tiene una regla peculiar que conviene conocer, porque es fuente de
sorpresas: **por defecto es por referencia**, pero **si el argumento es una expresión o no coincide
el tipo, el compilador crea una copia temporal (*dummy argument*)** y pasa esa.

```pli
call p(x);        /* por referencia: p puede modificar x */
call p(x + 0);    /* ¡es una EXPRESIÓN: se pasa una copia! */
call p((x));      /* los paréntesis extra FUERZAN la copia -- idioma clásico */
```

Ese `((x))` con doble paréntesis es el idioma de PL/I para "pásalo por valor", y aparece en código
antiguo sin ninguna explicación. Fortran tiene exactamente el mismo comportamiento y el mismo truco.

Es la razón de que los lenguajes posteriores prefieran declarar el modo en la firma: **si el
mecanismo depende de la forma del argumento en el sitio de la llamada, nadie puede saber qué pasa
leyendo solo la declaración**.
"""),
        "mumps": ("""
SUMAR ; Firma y retorno -- clase 073
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 write "suma=", $$suma(a, b), !
 quit
 ;
suma(x, y) ; devuelve x + y
 quit x + y
""", """
**Lo que esta clase enseña en M.** M tiene **dos formas de invocar código**, y la diferencia está en
si devuelve valor:

```mumps
 do RUTINA^MODULO          ; llamada SIN valor de retorno
 do RUTINA^MODULO(a, b)    ; con argumentos
 set x = $$FUNCION^MODULO(a, b)   ; FUNCIÓN EXTRÍNSECA: devuelve con QUIT valor
```

El **doble dólar** distingue la función extrínseca de las funciones incorporadas (`$piece`,
`$select`), que llevan uno solo. Y `quit valor` es el `return`.

Los parámetros de M tienen una peculiaridad importante: **por defecto se pasan por valor, y con un
punto delante, por referencia**.

```mumps
 do PROC^RUT(a, .b)        ; a por VALOR, b por REFERENCIA
```

Ese punto en el **sitio de la llamada** —no en la declaración— es como COBOL con `BY REFERENCE`: quien
llama decide el mecanismo. Y tiene una capacidad que casi nadie más ofrece: **pasar por referencia un
array entero**, con todos sus subíndices, que la rutina llamada puede recorrer y modificar.

```mumps
 do CARGAR^DATOS(.resultado)     ; la rutina RELLENA el array completo
 for  set i = $order(resultado(i))  quit:i=""  write resultado(i), !
```

Es el idioma estándar para devolver estructuras en M: **no se devuelve una colección, se rellena un
array del llamante**. Es la razón de que las APIs de VistA y FileMan tengan esa forma tan
característica.
"""),
        "smalltalk": ("""
| partes a b |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

Transcript show: 'suma=', (a + b) printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** En Smalltalk **no hay funciones: hay métodos**, y un método
siempre pertenece a una clase y siempre tiene un receptor. No existe la función suelta.

La firma es el **selector**, y su forma es única entre los lenguajes de esta página:

```smalltalk
Numero >> suma: otro                      "selector: suma:"
Rectangulo >> ancho: a alto: b            "selector: ancho:alto:"
Coleccion >> copyFrom: i to: j            "selector: copyFrom:to:"
```

**El nombre del método está intercalado entre los argumentos.** `copyFrom: 1 to: 5` se lee entero, y
el selector completo es `copyFrom:to:`. Eso hace innecesarios los argumentos nombrados de la clase
075: **en Smalltalk todos los argumentos van nombrados siempre**, porque el nombre es parte del
método.

Y de ahí sale una propiedad que conviene entender: **no hay sobrecarga**. Dos métodos con distinto
número de argumentos tienen **selectores distintos**, así que no compiten. `Punto x: 1` y
`Punto x: 1 y: 2` son dos métodos sin ninguna relación entre sí. Toda la complejidad de la resolución
de sobrecarga de C++ y Java simplemente no existe.

Sobre el retorno: **`^` devuelve, y si no lo escribes el método devuelve `self`**. Ese valor por
defecto es deliberado: permite encadenar mensajes de configuración (`obj poner: 1; poner: 2; yourself`)
sin escribir retornos.
"""),
    },
)

# ---------------------------------------------------------------------------
# 074 — Parámetros por defecto y opcionales
# ---------------------------------------------------------------------------
SPECS["074"] = dict(
    gancho="""
Elevar un número a una potencia, con el exponente **2 si no se indica**. El valor por defecto es una
de esas comodidades que parecen triviales hasta que se cuenta cuántos de estos doce lenguajes la
tienen: **cinco**. Los otros siete resuelven el problema de tres maneras distintas, y una de ellas
—la de Smalltalk— es tan limpia que hace innecesaria la característica.
""",
    porque="""
Aquí el concepto es el **argumento ausente**, y estos lenguajes enseñan las cuatro respuestas
posibles. **Valor por defecto en la declaración**: Ada, Lisp, Tcl, Pascal moderno y C++. **Argumento
declarado opcional más una pregunta**: Fortran con `optional` y `present()`, RPG con `options(*nopass)`
y `%parms`. **Nada, hay que comprobar**: COBOL, PL/I, M. Y **métodos distintos con nombres
distintos**: Smalltalk.

Esa última merece atención: cuando el nombre del método incluye sus argumentos, `pot:` y `pot:exp:`
son dos métodos, y uno puede llamar al otro. **La sobrecarga por número de argumentos deja de existir
como problema.**
""",
    cierre="""
Lo transferible es una advertencia sobre los valores por defecto: **en la mayoría de los lenguajes se
evalúan en el sitio de la LLAMADA, pero no en todos**. En C++ y Ada, el valor por defecto se evalúa en
cada llamada; en Python —el caso famoso— se evalúa **una sola vez, al definir la función**, y por eso
un valor por defecto mutable es un error clásico. Antes de poner un valor por defecto que no sea una
constante, comprueba cuándo se evalúa en tu lenguaje.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. POTENCIA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TXT-B   PIC X(20).
01  TXT-E   PIC X(20).
01  BASE-V  PIC S9(9)  COMP-3.
01  EXPO    PIC S9(9)  COMP-3.
01  R       PIC S9(18) COMP-3.
01  I       PIC 9(4)   COMP-3.
01  ED-R    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE SPACES TO TXT-E
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-B TXT-E

    MOVE FUNCTION NUMVAL(TXT-B) TO BASE-V

    IF TXT-E = SPACES
        MOVE 2 TO EXPO
    ELSE
        MOVE FUNCTION NUMVAL(TXT-E) TO EXPO
    END-IF

    MOVE 1 TO R
    PERFORM VARYING I FROM 1 BY 1 UNTIL I > EXPO
        COMPUTE R = R * BASE-V
    END-PERFORM

    MOVE R TO ED-R
    DISPLAY "resultado=" FUNCTION TRIM(ED-R)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** **COBOL no tiene parámetros por defecto ni opcionales.** Un
`CALL` con menos argumentos de los que el programa espera es un error en ejecución, no un valor por
defecto.

La comprobación de este programa —`IF TXT-E = SPACES`— es el idioma real: **usar el valor "vacío"
como señal de ausencia**, que es exactamente el problema de los centinelas de la clase 053. Funciona
mientras "vacío" no sea un dato legítimo.

Cuando hace falta de verdad, COBOL tiene dos mecanismos, y ninguno es cómodo:

```cobol
*> 1) El programa llamado pregunta cuántos argumentos recibió
CALL "SUBPROG" USING A, B
...
*> en SUBPROG, con la extensión de IBM:
IF NUMBER-OF-CALL-PARAMETERS = 1 ...

*> 2) Un campo indicador explícito
CALL "SUBPROG" USING A, B, WS-B-PRESENTE
```

La segunda —pasar una bandera diciendo qué argumentos son válidos— es la que se ve en código real, y
es exactamente lo que hace RPG con `%parms` pero sin apoyo del lenguaje.

Y hay una razón histórica para esta ausencia: en COBOL, **la lista de parámetros es un contrato de
memoria**. `USING` pasa direcciones, y el programa llamado las mapea sobre su `LINKAGE SECTION`. No
hay un mecanismo que "rellene" un hueco, porque no hay quien lo rellene: el enlace es directo.
"""),
        "fortran": ("""
program potencia
   implicit none
   character(len=100) :: linea
   integer :: base, expo, ios

   read(*, '(A)') linea

   read(linea, *, iostat=ios) base, expo
   if (ios /= 0) then
      read(linea, *) base
      write(*, '(A,I0)') 'resultado=', pot(base)
   else
      write(*, '(A,I0)') 'resultado=', pot(base, expo)
   end if

contains

   pure function pot(b, e) result(r)
      integer, intent(in) :: b
      integer, intent(in), optional :: e     ! OPCIONAL, sin valor por defecto
      integer :: r, i, ee
      ee = 2
      if (present(e)) ee = e                 ! el defecto se escribe DENTRO
      r = 1
      do i = 1, ee
         r = r * b
      end do
   end function pot

end program potencia
""", """
**Lo que esta clase enseña en Fortran.** Fortran tiene **`optional`, pero no valores por defecto**, y
esa combinación es característica: el argumento puede faltar, y **el defecto se escribe dentro de la
función** con `present()`.

```fortran
integer, intent(in), optional :: e
...
if (present(e)) then ... else ... end if
```

Puede parecer un rodeo frente a `e = 2` en la firma, y tiene una ventaja concreta: **el defecto puede
depender de los otros argumentos**, cosa que un valor en la declaración no permite.

```fortran
if (present(tolerancia)) then
   tol = tolerancia
else
   tol = epsilon(x) * 100.0        ! depende del TIPO del otro argumento
end if
```

Y hay una regla que causa errores reales: **`present()` solo se puede llamar sobre el propio
parámetro**, y **usar un argumento opcional ausente es comportamiento indefinido**. Compilar con
`-fcheck=all` lo detecta.

Fortran combina además `optional` con los **argumentos por palabra clave** de la clase 075, y ahí es
donde la característica cobra sentido:

```fortran
call resolver(matriz, tolerancia=1e-9)     ! salto los intermedios
```

Con `optional` a secas, para pasar el quinto argumento habría que pasar los cuatro anteriores. Con
palabras clave, no. **Las dos características juntas son lo que hace usables las interfaces de
LAPACK**, que tienen rutinas de quince parámetros.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Potencia is

   --  El valor por defecto va EN LA FIRMA.
   function Pot (B : Integer; E : Integer := 2) return Integer is
      R : Integer := 1;
   begin
      for I in 1 .. E loop
         R := R * B;
      end loop;
      return R;
   end Pot;

   Linea      : String (1 .. 100);
   Ultimo     : Natural;
   Pos        : Positive := 1;
   Fin        : Positive;
   Base, Expo : Integer;
   Hay_Expo   : Boolean := False;
begin
   Get_Line (Linea, Ultimo);
   Get (Linea (Pos .. Ultimo), Base, Fin);
   Pos := Fin + 1;

   if Pos <= Ultimo then
      Get (Linea (Pos .. Ultimo), Expo, Fin);
      Hay_Expo := True;
   end if;

   Put ("resultado=");
   if Hay_Expo then
      Put (Pot (Base, Expo), Width => 1);
   else
      Put (Pot (Base), Width => 1);
   end if;
   New_Line;
end Potencia;
""", """
**Lo que esta clase enseña en Ada.** `E : Integer := 2` en la firma es el valor por defecto, y Ada lo
combina con la **asociación por nombre** de la clase 075 para conseguir algo que C++ no puede:
**omitir un parámetro intermedio**.

```ada
procedure Dibujar (X, Y : Integer; Color : Color_T := Negro;
                   Grosor : Positive := 1; Relleno : Boolean := False);

Dibujar (10, 20);                          --  todos por defecto
Dibujar (10, 20, Relleno => True);         --  ¡salto Color y Grosor!
Dibujar (X => 10, Y => 20, Grosor => 3);
```

En C++ los valores por defecto **solo pueden omitirse desde el final**: para pasar el quinto hay que
pasar los cuatro anteriores. En Ada, con nombres, no. Es la misma ventaja que Fortran obtiene con
`optional` más palabras clave, y la razón de que estas dos características se diseñen juntas.

Y hay un detalle de Ada que merece la pena: **el valor por defecto se evalúa en cada llamada**, en el
ámbito de la declaración. Así que puede ser una expresión, incluso una llamada a función:

```ada
procedure Registrar (Msg : String; Cuando : Time := Clock);   --  la hora ACTUAL
```

Compara con Python, donde el defecto se evalúa **una sola vez al definir** y `def f(x=[])` es el error
clásico. Ada, C++ y Ruby evalúan en cada llamada; Python y JavaScript (con `var`) no. Es una
diferencia que conviene comprobar en cada lenguaje nuevo.
"""),
        "pascal": ("""
program Potencia;
{$MODE OBJFPC}{$H+}
uses SysUtils;

function Pot(B: Integer; E: Integer = 2): Int64;
var
  I: Integer;
begin
  Result := 1;
  for I := 1 to E do
    Result := Result * B;
end;

var
  Linea: string;
  P: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);
  P := Pos(' ', Linea);

  if P = 0 then
    WriteLn('resultado=', IntToStr(Pot(StrToInt(Linea))))
  else
    WriteLn('resultado=', IntToStr(Pot(StrToInt(Copy(Linea, 1, P - 1)),
                                       StrToInt(Trim(Copy(Linea, P + 1, Length(Linea)))))));
end.
""", """
**Lo que esta clase enseña en Pascal.** **El Pascal ISO no tiene valores por defecto.** Los añadieron
Delphi 4 (1999) y Free Pascal, con la sintaxis `E: Integer = 2` de este programa.

Y llevan una restricción que conviene conocer: **el valor por defecto debe ser una constante conocida
al compilar**, no una expresión.

```pascal
function F(A: Integer = 10): Integer;              { correcto }
function G(A: Integer = Calcular): Integer;        { NO compila }
function H(const S: string = ''): Integer;         { correcto }
```

Es una restricción más estricta que la de Ada y C++, y viene del modelo de compilación en una sola
pasada: el valor se incrusta en el sitio de la llamada, así que tiene que ser un literal.

De ahí que el idioma clásico de Pascal para el argumento opcional sea la **sobrecarga**, disponible
desde Delphi 1:

```pascal
function Pot(B: Integer): Int64; overload;
function Pot(B, E: Integer): Int64; overload;
```

Dos funciones con el mismo nombre y distinta firma. `overload` es obligatorio en Object Pascal —a
diferencia de C++, donde la sobrecarga es implícita— y esa obligación es deliberada: **declara la
intención**, y evita que dos funciones colisionen por accidente al fusionar código.

Fíjate también en `Pos(' ', Linea)`, que devuelve la posición de la primera aparición o **0** si no
está. Es el mismo cero de la clase 053 haciendo de centinela: funciona porque las posiciones de
cadena en Pascal empiezan en 1.
"""),
        "lisp": ("""
(defun pot (b &optional (e 2))
  (expt b e))

(let* ((base (read))
       (expo (read *standard-input* nil :sin)))
  (if (eq expo :sin)
      (format t "resultado=~D~%" (pot base))
      (format t "resultado=~D~%" (pot base expo))))
""", """
**Lo que esta clase enseña en Common Lisp.** `&optional (e 2)` declara un parámetro opcional **con su
valor por defecto en la propia lambda-lista**, y Lisp añade dos refinamientos que casi nadie tiene.

El primero: **el valor por defecto puede usar los parámetros anteriores**.

```lisp
(defun rango (inicio &optional (fin (+ inicio 10)) (paso (if (> fin inicio) 1 -1)))
  ...)
```

`fin` depende de `inicio`, y `paso` depende de los dos. Se evalúan de izquierda a derecha, en cada
llamada. Es la ventaja que Fortran consigue escribiendo el defecto dentro del cuerpo, aquí obtenida
en la firma.

El segundo, y es el que resuelve un problema real: **la variable "¿lo pasaron?"**.

```lisp
(defun f (a &optional (b 0 b-dado))
  (if b-dado
      (format t "me pasaron b, y vale ~D" b)
      (format t "b no vino; uso el defecto")))
```

El tercer elemento de la lista —`b-dado`— es un booleano que dice si el argumento **se pasó
explícitamente**. Eso distingue "no lo pasó" de "pasó justo el valor por defecto", que son cosas
distintas y que en C++, Ada y Pascal no se pueden separar. Es exactamente el problema de la clase 053
aplicado a los parámetros.

Y `(expt b e)` es la exponenciación de Lisp, que con enteros da **resultados exactos sin límite**:
`(expt 2 1000)` devuelve el número completo.
"""),
        "tcl": ("""
proc pot {base {expo 2}} {
    return [expr {$base ** $expo}]
}

gets stdin linea
set partes [split [string trim $linea]]

if {[llength $partes] == 1} {
    puts "resultado=[pot [lindex $partes 0]]"
} else {
    puts "resultado=[pot [lindex $partes 0] [lindex $partes 1]]"
}
""", """
**Lo que esta clase enseña en Tcl.** `{expo 2}` en la lista de parámetros declara el valor por
defecto, y la sintaxis revela cómo funciona: **la lista de parámetros de `proc` es una lista de
Tcl**, donde cada elemento es o bien un nombre, o bien una lista de dos elementos —nombre y defecto—.

```tcl
proc f {a {b 10} {c "hola"} args} { ... }
```

No hay sintaxis especial: es la estructura de datos normal del lenguaje, interpretada por `proc`. Por
eso se puede construir en ejecución:

```tcl
set params [list a [list b 10]]
proc dinamica $params { ... }        ;# la FIRMA se construye como un dato
```

Y como se vio en la clase 073, `info args` y `info default` permiten **inspeccionar la firma** de
cualquier procedimiento, incluidos los defectos. Eso es lo que usan los generadores de documentación
y los envoltorios automáticos.

Sobre la comprobación: Tcl **sí verifica la aridad**. Llamar `pot` sin argumentos da
`wrong # args: should be "pot base ?expo?"`, con los opcionales entre interrogaciones. Ese formato de
mensaje es una convención de todo el lenguaje y de sus bibliotecas.

Y `**` es el operador de exponenciación, disponible dentro de `expr` desde Tcl 8.5, con enteros de
precisión arbitraria detrás.
"""),
        "perl": ("""
use strict;
use warnings;

sub pot {
    my ($base, $expo) = @_;
    $expo //= 2;                 # // : solo si NO ESTÁ DEFINIDO
    return $base ** $expo;
}

my $linea = <STDIN>;
chomp $linea;
my @partes = split ' ', $linea;

print "resultado=", pot(@partes), "\\n";
""", """
**Lo que esta clase enseña en Perl.** `$expo //= 2` es el idioma clásico, y la elección del operador
es la lección: **`//=` asigna solo si el valor no está DEFINIDO**, mientras que `||=` lo haría también
si fuera falso.

```perl
$expo ||= 2;     # MAL: un exponente 0 se convertiría en 2
$expo //= 2;     # BIEN: solo si no vino
```

Es exactamente el problema de la clase 053 —distinguir "no hay valor" de "el valor es cero"— aplicado
a los parámetros, y es un error real: `pot(5, 0)` debería dar 1 y con `||=` daría 25.

Fíjate también en `pot(@partes)`: al pasar un array a una subrutina, **se aplana en `@_`**. Si
`@partes` tiene un elemento, la subrutina recibe uno; si tiene dos, dos. No hace falta comprobar
nada en el sitio de la llamada. Ese aplanamiento es una característica de Perl que sorprende y que
aquí resulta muy cómoda — aunque es también la razón de que pasar dos arrays a una función exija
referencias.

Y **Perl 5.36 permite el valor por defecto en la firma**, que es como se escribe hoy:

```perl
use v5.36;
sub pot ($base, $expo = 2) { return $base ** $expo }
sub log_msg ($msg, $nivel = 'info', @extra) { ... }
```

El defecto en una firma se evalúa **en cada llamada** y puede usar los parámetros anteriores, igual
que en Lisp: `sub rango ($ini, $fin = $ini + 10) { ... }`.
"""),
        "cpp": ("""
#include <iostream>
#include <sstream>
#include <string>

long long pot(int base, int expo = 2) {
    long long r = 1;
    for (int i = 0; i < expo; ++i) r *= base;
    return r;
}

int main() {
    std::string linea;
    if (!std::getline(std::cin, linea)) return 1;

    std::istringstream iss(linea);
    int base{}, expo{};
    iss >> base;

    if (iss >> expo) {
        std::cout << "resultado=" << pot(base, expo) << '\\n';
    } else {
        std::cout << "resultado=" << pot(base) << '\\n';
    }
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** Los argumentos por defecto de C++ tienen **dos restricciones
importantes** que conviene tener claras.

La primera: **solo se pueden omitir desde el final**. No hay forma de pasar el tercero sin pasar el
segundo, porque C++ no tiene argumentos nombrados —clase 075—.

La segunda, y es la que causa errores: **el valor por defecto pertenece a la DECLARACIÓN, no a la
función**, y si la declaración está en una cabecera, **cada unidad de traducción puede ver un defecto
distinto**.

```cpp
// cabecera.h
void f(int x = 10);

// otro.cpp
void f(int x = 20);      // legal en OTRO ámbito: dos defectos para la misma función
```

Por eso la regla es: **el defecto se escribe una sola vez, en la declaración de la cabecera, y nunca
en la definición**.

Y hay un aviso de fondo: **los argumentos por defecto no participan en el polimorfismo**. Si una clase
derivada redefine un método virtual con otro defecto, **se usa el defecto del tipo ESTÁTICO** y el
cuerpo del dinámico:

```cpp
struct Base    { virtual void f(int x = 1) { ... } };
struct Derivada: Base { void f(int x = 2) override { ... } };

Base* p = new Derivada;
p->f();      // llama a Derivada::f... ¡con x = 1!
```

Es un comportamiento sorprendente, está en todas las listas de trampas de C++, y la recomendación de
las *Core Guidelines* es tajante: **no pongas argumentos por defecto en funciones virtuales**.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi POTENCIA;
  base int(10) const;
  expo int(10) const options(*nopass);   // OPCIONAL: se puede no pasar
end-pi;

dcl-s e      int(10);
dcl-s r      int(20) inz(1);
dcl-s i      int(10);
dcl-s salida char(40);

// %parms dice CUÁNTOS argumentos llegaron de verdad.
if %parms >= 2;
  e = expo;
else;
  e = 2;
endif;

for i = 1 to e;
  r *= base;
endfor;

salida = 'resultado=' + %char(r);
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG resuelve esta clase con dos piezas que van siempre juntas:
**`options(*nopass)`** en la firma, que declara que el argumento puede no venir, y **`%parms`**, que
dice cuántos llegaron de verdad.

```rpgle
dcl-pi *n;
  a int(10) const;
  b int(10) const options(*nopass);
  c int(10) const options(*nopass);   // los *nopass van SIEMPRE al final
end-pi;

if %parms >= 3; ... endif;
```

Los opcionales tienen que ir al final, como en C++, y por la misma razón: sin nombres, la posición es
lo único que identifica al argumento.

Y hay una trampa de seguridad que conviene conocer, porque es específica de RPG: **acceder a un
parámetro `*nopass` que no se pasó es leer memoria ajena**. No hay comprobación automática; el
programa lee lo que haya en esa dirección. Es tan peligroso como leer un puntero no inicializado en
C, y la única protección es comprobar `%parms` **antes**.

RPG tiene además `options(*omit)`, que permite pasar `*omit` explícitamente en una posición
intermedia:

```rpgle
dcl-pi *n;
  a pointer options(*omit);
end-pi;
...
callp proceso(*omit : otro);       // el primero se omite EXPLÍCITAMENTE
if %addr(a) <> *null; ... endif;
```

Con `*omit` sí se pueden saltar posiciones intermedias, y la comprobación es sobre la dirección. Es
la versión de RPG del argumento nombrado, y es tan incómoda como suena.
"""),
        "pli": ("""
 potencia: procedure options(main);

    declare linea character(80) varying;
    declare (base_v, expo, r, i) fixed binary(31);
    declare p fixed binary(31);

    get edit (linea) (a(80));
    linea = trim(linea);

    p = index(linea, ' ');
    if p = 0 then do;
       base_v = linea;
       expo = 2;                      /* el defecto se escribe A MANO */
    end;
    else do;
       base_v = substr(linea, 1, p - 1);
       expo = substr(linea, p + 1);
    end;

    r = 1;
    do i = 1 to expo;
       r = r * base_v;
    end;

    put skip list ('resultado=' || trim(char(r)));

 end potencia;
""", """
**Lo que esta clase enseña en PL/I.** **PL/I no tiene parámetros por defecto ni opcionales**, y es
llamativo en un lenguaje que tenía casi todo lo demás. La comprobación se escribe a mano, como en
COBOL.

Lo que sí ofrece, y es su respuesta a esta clase, es el atributo **`generic`**, que selecciona entre
varios procedimientos **según el número y el tipo de los argumentos**:

```pli
declare pot generic (pot2 when (fixed binary),
                     potn when (fixed binary, fixed binary));

x = pot(3);        /* llama a pot2 */
y = pot(2, 3);     /* llama a potn */
```

Es **sobrecarga por aridad y por tipo**, declarada explícitamente en una tabla en lugar de deducida
por el compilador. Funciona igual que el `overload` de Object Pascal y que la sobrecarga implícita de
C++, con la diferencia de que aquí las alternativas están **enumeradas en un solo sitio** y se pueden
leer.

Esa explicitud tiene una ventaja que se aprecia al mantener código: para saber a qué se llama con
`pot(3)`, se lee la declaración `generic`, no se reconstruye mentalmente el algoritmo de resolución de
sobrecarga del compilador.

Y `index(cadena, subcadena)` de este programa es la función de búsqueda de PL/I —devuelve 0 si no
encuentra—, la misma que `Pos` en Pascal y `%scan` en RPG.
"""),
        "mumps": ("""
POT ; Parametros opcionales -- clase 074
 read linea
 set base = $piece(linea, " ", 1)
 set expo = $piece(linea, " ", 2)
 if expo = "" write "resultado=", $$pot(base), ! quit
 write "resultado=", $$pot(base, expo), !
 quit
 ;
pot(b, e) ; b elevado a e (e por defecto 2)
 new i, r
 set e = $get(e, 2)          ; $GET con valor por defecto: el idioma de M
 set r = 1
 for i = 1:1:e set r = r * b
 quit r
""", """
**Lo que esta clase enseña en M.** **`$get(variable, valorPorDefecto)`** es la respuesta de M, y es
más elegante de lo que parece: en M, **llamar a una función con menos argumentos de los declarados es
perfectamente legal**, y los parámetros que faltan quedan simplemente **sin definir**.

```mumps
 set x = $$pot(3)          ; e queda INDEFINIDA dentro de pot
 set e = $get(e, 2)        ; y $get le da el valor por defecto
```

No hay que declarar nada opcional ni preguntar cuántos argumentos llegaron: **la ausencia es un
estado del dato**, y `$data`/`$get` son las funciones que ya se vieron en la clase 053.

Esa uniformidad es notable: el mismo mecanismo que distingue "esta variable no existe" de "vale
cero" sirve para "este parámetro no se pasó". En los demás lenguajes de esta página hacen falta dos
mecanismos distintos —`present()` y `$data`, `%parms` y `%nullind`—.

Y M lleva la idea más lejos: **también se puede llamar con MÁS argumentos de los declarados**, y los
sobrantes se ignoran. Es tan permisivo que un error de aridad no da ningún aviso, lo que enlaza con
todo lo dicho sobre M: máxima flexibilidad, cero comprobación.

`new i, r` al principio de la función es lo de la clase 069: sin él, las variables temporales serían
globales y la recursión se rompería.
"""),
        "smalltalk": ("""
| partes base expo |

partes := stdin nextLine substrings.
base := partes first asNumber.
expo := partes size > 1
    ifTrue:  [ partes second asNumber ]
    ifFalse: [ 2 ].

Transcript show: 'resultado=', (base raisedTo: expo) printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** **Smalltalk no tiene parámetros por defecto, y no los
necesita.** Como el nombre del método incluye sus argumentos —clase 073—, dos aridades distintas son
**dos métodos con nombres distintos**, y uno delega en el otro:

```smalltalk
Number >> potencia
    ^self potencia: 2                 "el defecto: delega"

Number >> potencia: exponente
    ^self raisedTo: exponente
```

`potencia` y `potencia:` son selectores diferentes. No compiten, no hay sobrecarga que resolver, y el
"valor por defecto" es simplemente **el argumento que el método corto le pasa al largo**.

Ese patrón recorre toda la biblioteca y es reconocible al instante:

```smalltalk
coleccion detect: unBloque
coleccion detect: unBloque ifNone: otroBloque

diccionario at: clave
diccionario at: clave ifAbsent: unBloque

cadena indexOf: caracter
cadena indexOf: caracter startingAt: indice
cadena indexOf: caracter startingAt: indice ifAbsent: unBloque
```

Cada versión larga añade información y la corta delega con un valor razonable. Es más verboso de
declarar y **mucho más legible en el sitio de la llamada**, porque el nombre dice exactamente qué
hace esa variante.

Y tiene una ventaja de mantenimiento real: cambiar el valor por defecto es editar **un método**, no
recompilar a todos los que llamaban con el defecto — que es exactamente el problema de C++ con los
defectos en cabeceras.
"""),
    },
)

# ---------------------------------------------------------------------------
# 075 — Argumentos nombrados y de palabra clave
# ---------------------------------------------------------------------------
SPECS["075"] = dict(
    gancho="""
Construir el texto `punto(x=3, y=4)`. Un programa trivial que sirve de excusa para la pregunta de la
clase: **¿se puede decir a qué parámetro corresponde cada argumento en el sitio de la llamada?**
Porque `dibujar(10, 20, 1, 0, 1)` no se entiende sin ir a buscar la firma, y ese problema tiene
sesenta años.
""",
    porque="""
Aquí el concepto son los **argumentos nombrados**, y estos lenguajes lo enseñan porque **tres de
ellos los tienen desde hace décadas y son mejores que los de casi todo el núcleo**. **Ada** los
introdujo en 1983 con `Nombre => Valor` y permite mezclarlos con los posicionales. **Fortran 90** los
tiene y son la razón de que las interfaces de LAPACK, con quince parámetros, sean usables. **Lisp**
los tiene con `&key`. Y **Smalltalk** los tiene de una forma que hace innecesaria la característica:
**el nombre está en el selector**, así que todos los argumentos van siempre nombrados.

Enfrente, **C++ sigue sin tenerlos** en 2026, y esa es una de sus carencias más comentadas.
""",
    cierre="""
Lo transferible es una regla de diseño de APIs: **si una función tiene más de tres parámetros del
mismo tipo, el sitio de la llamada es ilegible sin nombres**. Los lenguajes que no los tienen han
inventado sustitutos —un `struct` de opciones en C++, un hash en Perl, un objeto de configuración en
JavaScript— y todos son el mismo remedio. Cuando diseñes una firma larga, la pregunta no es cuántos
parámetros caben: es **si alguien podrá leer la llamada dentro de un año**.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. PUNTO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TXT-A   PIC X(20).
01  TXT-B   PIC X(20).
01  X-V     PIC S9(9) COMP-3.
01  Y-V     PIC S9(9) COMP-3.
01  ED-X    PIC -(8)9.
01  ED-Y    PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO X-V
    MOVE FUNCTION NUMVAL(TXT-B) TO Y-V

    MOVE X-V TO ED-X
    MOVE Y-V TO ED-Y
    DISPLAY "punto(x=" FUNCTION TRIM(ED-X)
            ", y=" FUNCTION TRIM(ED-Y) ")"
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** COBOL **no tiene argumentos nombrados**, y un `CALL ... USING`
con seis campos es exactamente el problema que esta clase describe.

Pero COBOL tiene una solución al mismo problema que es característica suya y que sigue siendo buena:
**pasar una estructura con campos nombrados en lugar de una lista de argumentos**.

```cobol
01  PARAMETROS-DIBUJO.
    05  PD-X         PIC S9(4) COMP-3.
    05  PD-Y         PIC S9(4) COMP-3.
    05  PD-COLOR     PIC X(10).
    05  PD-GROSOR    PIC 9(2)  COMP-3.
    05  PD-RELLENO   PIC X.
        88  CON-RELLENO  VALUE "S".

MOVE 10 TO PD-X
MOVE 20 TO PD-Y
SET CON-RELLENO TO TRUE
CALL "DIBUJAR" USING PARAMETROS-DIBUJO
```

Cada valor se asigna **por su nombre** antes de la llamada, y la llamada pasa un solo argumento. Es
verboso y es completamente legible: se ve qué se está poniendo y qué se deja como estaba.

Ese patrón —el "bloque de parámetros"— es el estándar de facto en el mundo mainframe, y es idéntico a
lo que hoy se hace en C++ con un `struct` de opciones, en JavaScript con un objeto y en Go con el
patrón de opciones funcionales. **Cuando un lenguaje no tiene argumentos nombrados, todos acaban
inventando el mismo sustituto.**

Y el copybook de la clase 052 hace que esa estructura se comparta entre todos los programas que la
usan.
"""),
        "fortran": ("""
program punto
   implicit none
   integer :: a, b

   read(*, *) a, b

   !  Llamada con PALABRAS CLAVE: el orden deja de importar.
   call mostrar(x = a, y = b)

contains

   subroutine mostrar(x, y)
      integer, intent(in) :: x, y
      character(len=32) :: bx, by
      write(bx, '(I0)') x
      write(by, '(I0)') y
      write(*, '(A,A,A,A,A)') 'punto(x=', trim(bx), ', y=', trim(by), ')'
   end subroutine mostrar

end program punto
""", """
**Lo que esta clase enseña en Fortran.** `call mostrar(x = a, y = b)` usa **argumentos por palabra
clave**, que Fortran tiene desde 1990 y que casi nadie asocia con este lenguaje.

La regla es la misma que en Python: **los posicionales primero, los nombrados después**, y una vez que
empiezas a nombrar ya no puedes volver a la posición.

```fortran
call resolver(matriz, vector, tolerancia = 1e-9, maxiter = 500)
```

Y aquí está el motivo real de que exista: **combinado con `optional` de la clase 074, permite saltar
parámetros intermedios**. Las rutinas de LAPACK y de las bibliotecas numéricas tienen firmas de
quince argumentos, la mayoría opcionales, y sin palabras clave serían inutilizables.

Hay un requisito importante: **la palabra clave es el nombre del parámetro tal como aparece en la
interfaz**, así que el compilador tiene que conocerla. Eso obliga a que la rutina esté en un `module`
o en un `contains`, o a declarar una `interface` explícita. Con las subrutinas externas al estilo
FORTRAN 77 —sin interfaz— **no se pueden usar palabras clave**.

Es una de las razones de que el Fortran moderno insista tanto en poner todo dentro de módulos: sin
interfaz explícita se pierden las palabras clave, la comprobación de tipos en las llamadas y los
argumentos opcionales.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Strings;         use Ada.Strings;
with Ada.Strings.Fixed;

procedure Punto is

   function Formatear (X, Y : Integer) return String is
      use Ada.Strings.Fixed;
   begin
      return "punto(x=" & Trim (Integer'Image (X), Both) &
             ", y=" & Trim (Integer'Image (Y), Both) & ")";
   end Formatear;

   A, B : Integer;
begin
   Get (A);
   Get (B);

   --  ASOCIACIÓN POR NOMBRE: el orden deja de importar.
   Put_Line (Formatear (X => A, Y => B));
end Punto;
""", """
**Lo que esta clase enseña en Ada.** `X => A` es la **asociación por nombre**, y Ada la tiene desde
1983 — antes que ningún otro lenguaje de uso general.

Y no es solo para llamadas: **la misma sintaxis funciona en todos los sitios donde hay una
correspondencia**.

```ada
Formatear (X => 10, Y => 20);                       --  llamadas
V : Vector := (1 => 10, 2 => 20, others => 0);      --  agregados de array
P : Punto  := (X => 10, Y => 20);                   --  agregados de registro
package Mi_IO is new Text_IO.Integer_IO (Num => Mi_Tipo);   --  genéricos
Put (Item => X, Width => 5, Base => 16);            --  y con valores por defecto
```

Esa uniformidad es muy propia de Ada: **un mecanismo, aplicado en todos los contextos donde tiene
sentido**.

Y hay una construcción que merece verse porque no tiene equivalente: **el agregado con `others`**.

```ada
Config : Opciones := (Color => Rojo, others => <>);
```

`others => <>` significa "el resto, con su valor por defecto". Con eso, un registro de veinte campos
se construye nombrando solo los tres que interesan, y el compilador **comprueba que estén todos
cubiertos**. Es lo que en C++ se intenta con los inicializadores designados de C++20 y en Rust con
`..Default::default()`.

La regla de Ada es la misma que en Fortran: los posicionales primero, y una vez nombrado, todo
nombrado.
"""),
        "pascal": ("""
program Punto;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea: string;
  P, X, Y: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);
  P := Pos(' ', Linea);
  X := StrToInt(Copy(Linea, 1, P - 1));
  Y := StrToInt(Trim(Copy(Linea, P + 1, Length(Linea))));

  WriteLn(Format('punto(x=%d, y=%d)', [X, Y]));
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal **no tiene argumentos nombrados**, y su sustituto es el
**registro**, que es la misma solución que el bloque de parámetros de COBOL:

```pascal
type
  TOpcionesDibujo = record
    X, Y: Integer;
    Color: TColor;
    Grosor: Integer;
    Relleno: Boolean;
  end;

var
  Op: TOpcionesDibujo;
begin
  Op := Default(TOpcionesDibujo);    { todo a cero/vacío }
  Op.X := 10;
  Op.Y := 20;
  Op.Relleno := True;
  Dibujar(Op);
```

`Default(T)` de Delphi moderno inicializa el registro entero a valores nulos, lo que evita el
problema de olvidar un campo.

Fíjate también en `Format('punto(x=%d, y=%d)', [X, Y])`: es el `printf` de Object Pascal, con los
argumentos en un **array abierto** entre corchetes. Y admite **índices de argumento**, que es lo más
cerca que llega Pascal a los nombres en el formato:

```pascal
Format('%1:d viene antes de %0:d', [A, B]);     { reordena los argumentos }
```

Ese `%1:d` es útil para traducciones, donde el orden de las palabras cambia según el idioma. Es la
misma idea que `{0}` y `{1}` en C# y `%1$s` en `printf` de POSIX.
"""),
        "lisp": ("""
(defun punto (&key x y)
  (format nil "punto(x=~D, y=~D)" x y))

(let* ((a (read))
       (b (read)))
  (format t "~A~%" (punto :x a :y b)))
""", """
**Lo que esta clase enseña en Common Lisp.** `&key` declara parámetros **de palabra clave**, y la
llamada los pasa con `:nombre valor`. El orden es irrelevante y los que falten toman su valor por
defecto.

```lisp
(defun dibujar (&key x y (color :negro) (grosor 1) relleno)
  ...)

(dibujar :y 20 :x 10 :relleno t)     ; en cualquier orden, saltando los que sea
```

Y `:x` no es una cadena ni un identificador: es un **símbolo de palabra clave**, un objeto de primera
clase que se puede guardar, comparar y pasar como dato. Eso permite construir listas de argumentos en
ejecución:

```lisp
(let ((args (list :x 10 :y 20)))
  (apply #'dibujar args))            ; los argumentos, como DATO
```

Ese patrón —una lista de propiedades que se aplica a una función— es la base de gran parte del código
de configuración en Lisp, y es lo que hace que las funciones con muchas opciones sean cómodas de
envolver.

Lisp permite además combinar las cuatro clases de parámetro que ya aparecieron en la clase 073, y
tiene `&allow-other-keys` para aceptar claves que no conoce —útil para pasar opciones a una función
interna sin enumerarlas—.

La contrapartida honesta: `&key` tiene un coste en ejecución. Cada llamada recorre la lista buscando
las claves, así que en un bucle muy caliente se prefieren los posicionales. Es la misma disyuntiva
que en Python.
"""),
        "tcl": ("""
proc punto {args} {
    array set op {-x 0 -y 0}
    array set op $args
    return "punto(x=$op(-x), y=$op(-y))"
}

gets stdin linea
lassign [split [string trim $linea]] a b

puts [punto -x $a -y $b]
""", """
**Lo que esta clase enseña en Tcl.** Tcl **no tiene argumentos nombrados en el lenguaje**, y sin
embargo los usa por todas partes — porque los construye con las piezas normales.

El idioma es el de este programa: **`args` recoge todo, y `array set` lo interpreta como pares
opción-valor**, sobre unos valores por defecto puestos antes. Tres líneas.

```tcl
array set op {-x 0 -y 0 -color negro}    ;# defectos
array set op $args                        ;# los del usuario los pisan
```

Y funciona porque `args` recibe una lista plana y `array set` espera exactamente eso: una lista de
pares. **No hay ninguna sintaxis nueva.**

Esa convención —opciones con guion delante— es la de todos los comandos del propio Tcl:

```tcl
lsort -integer -decreasing $lista
string match -nocase $patron $texto
switch -regexp -matchvar m -- $x { ... }
regsub -all -- $patron $texto $reemplazo
```

Por eso los procedimientos de usuario la imitan: **la coherencia con el lenguaje es más valiosa que
una sintaxis dedicada**.

Para casos serios, Tcllib ofrece `cmdline::getoptions`, que además genera el mensaje de uso. Y el
`--` que aparece en varios de esos ejemplos es lo de la clase 061: marca el final de las opciones,
para que un valor que empiece por guion no se confunda con una.
"""),
        "perl": ("""
use strict;
use warnings;

sub punto {
    my %arg = @_;                  # los argumentos, como pares clave => valor
    return "punto(x=$arg{x}, y=$arg{y})";
}

my $linea = <STDIN>;
chomp $linea;
my ($p, $q) = split ' ', $linea;

print punto(x => $p, y => $q), "\\n";
""", """
**Lo que esta clase enseña en Perl.** `my %arg = @_;` es el idioma universal de Perl para argumentos
nombrados, y funciona por una razón elegante: **`@_` es una lista plana, y asignar una lista a un
hash la interpreta como pares clave-valor**.

Y `=>` no es un operador especial: es **una coma que además entrecomilla lo que tiene a su
izquierda**. Por eso `x => 3` es exactamente `'x', 3`.

```perl
punto(x => 3, y => 4);      # la subrutina recibe la lista ('x', 3, 'y', 4)
```

El patrón completo, con valores por defecto y validación, es este:

```perl
sub dibujar {
    my %arg = (color => 'negro', grosor => 1, @_);   # defectos PRIMERO
    die "falta x" unless exists $arg{x};
    ...
}
```

Poner los defectos **antes** de `@_` en la lista hace que los del usuario los pisen, porque en la
construcción de un hash **gana la última aparición de cada clave**. Es el mismo truco que
`array set` en Tcl, con otra sintaxis.

Y en Perl moderno se usa `Params::Validate` o el módulo del núcleo `builtin` para validar, o bien la
firma de 5.36 con un hash:

```perl
use v5.36;
sub dibujar ($x, $y, %opciones) { ... }     # posicionales y luego nombrados
```
"""),
        "cpp": ("""
#include <iostream>
#include <string>

struct Punto {
    int x;
    int y;
};

std::string formatear(const Punto& p) {
    return "punto(x=" + std::to_string(p.x) + ", y=" + std::to_string(p.y) + ")";
}

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::cout << formatear(Punto{a, b}) << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** **C++ no tiene argumentos nombrados**, en 2026, y es una de sus
carencias más señaladas. Ha habido propuestas repetidas al comité y ninguna ha prosperado.

Los sustitutos son tres, y todos son incómodos:

```cpp
// 1) Struct de opciones -- el más usado
struct OpcionesDibujo { int x; int y; Color color = Negro; int grosor = 1; };
dibujar({.x = 10, .y = 20, .grosor = 3});     // inicializadores DESIGNADOS, C++20

// 2) Tipos fuertes para que no se confundan
dibujar(Ancho{10}, Alto{20});

// 3) Encadenar setters -- el patrón "builder"
Dibujo{}.x(10).y(20).grosor(3).ejecutar();
```

La primera es la más cercana, y llegó con **C++20**: los **inicializadores designados** —`.x = 10`—
permiten construir un agregado nombrando los campos. Vienen de C99, donde existían desde hacía veinte
años, y **C++ los adoptó con una restricción**: tienen que ir **en el orden de declaración**, cosa que
en C no hace falta.

La segunda merece atención porque es una técnica de diseño transferible: envolver cada parámetro en
su propio tipo hace **imposible confundir el orden**. `dibujar(Alto{20}, Ancho{10})` no compila. Es
más trabajo y da una garantía que ningún argumento nombrado da — es la idea de los tipos de Ada de la
clase 050, aplicada a las firmas.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi PUNTO;
  x int(10) const;
  y int(10) const;
end-pi;

dcl-s salida char(60);

salida = 'punto(x=' + %char(x) + ', y=' + %char(y) + ')';
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG **no tiene argumentos nombrados**, y su sustituto es el mismo
que el de COBOL: **una estructura de datos con campos nombrados**.

```rpgle
dcl-ds opcionesDibujo qualified template;
  x       int(10);
  y       int(10);
  color   char(10) inz('negro');
  grosor  int(10)  inz(1);
end-ds;

dcl-ds op likeds(opcionesDibujo);

op.x = 10;
op.y = 20;
op.grosor = 3;
dibujar(op);
```

Tres palabras clave hacen que esto funcione bien, y merecen conocerse:

- **`qualified`** obliga a escribir `op.x` en lugar de `x` a secas. Sin ella, los subcampos serían
  nombres globales del programa —herencia del RPG antiguo— y colisionarían.
- **`template`** declara la estructura **sin reservar memoria**: solo sirve como molde para `likeds`.
  Es el `typedef` que RPG no tenía.
- **`likeds`** declara una variable con la misma forma que otra, que es la inferencia de la clase 052.

`inz()` en los campos da los valores por defecto, así que la estructura nace con ellos y solo hay que
tocar lo que cambie. Es exactamente el patrón de la clase 074 resuelto con datos en lugar de con
parámetros.

Y `qualified` es una de esas mejoras pequeñas que cambian mucho un lenguaje: pasar de un espacio de
nombres global plano a nombres cualificados es lo que permitió que RPG tuviera estructuras
reutilizables.
"""),
        "pli": ("""
 punto: procedure options(main);

    declare (x, y) fixed binary(31);

    get list (x, y);

    put skip list ('punto(x=' || trim(char(x)) ||
                   ', y='     || trim(char(y)) || ')');

 end punto;
""", """
**Lo que esta clase enseña en PL/I.** PL/I **no tiene argumentos nombrados**, pero tiene una
construcción que resuelve el mismo problema desde otro ángulo y que no existe en ningún lenguaje del
núcleo: **`BY NAME`**.

```pli
declare 1 origen,
          2 x fixed binary(31),
          2 y fixed binary(31),
          2 color character(10);

declare 1 destino,
          2 x fixed binary(31),
          2 y fixed binary(31),
          2 grosor fixed binary(31);

destino = origen, by name;      /* copia SOLO los campos que coinciden POR NOMBRE */
```

`by name` copia estructura a estructura **emparejando los campos por su nombre**, ignorando los que
no existan en el otro lado. Es una operación que hoy se resuelve a mano campo a campo, o con
reflexión, o con una biblioteca de mapeo de objetos.

RPG tiene la misma idea con **`eval-corr`** (*evaluate corresponding*), y COBOL con **`MOVE
CORRESPONDING`**. Los tres lenguajes de negocio la tienen, y los de sistemas no — porque el caso de
uso es el mismo: **mover datos entre dos registros parecidos pero no idénticos**, que es lo que hace
una aplicación de gestión todo el día.

Es un buen ejemplo de que "lenguaje antiguo" no significa "menos expresivo": significa **expresivo en
otras cosas**.
"""),
        "mumps": ("""
PUNTO ; Argumentos nombrados -- clase 075
 read linea
 set x = $piece(linea, " ", 1)
 set y = $piece(linea, " ", 2)
 write "punto(x=", x, ", y=", y, ")", !
 quit
""", """
**Lo que esta clase enseña en M.** M **no tiene argumentos nombrados**, y su sustituto es el más
natural del lenguaje: **pasar un array por referencia**, con los nombres como subíndices.

```mumps
 kill opciones
 set opciones("x") = 10
 set opciones("y") = 20
 set opciones("relleno") = 1
 do DIBUJAR^GRAF(.opciones)          ; el punto = por referencia
 ;
DIBUJAR(op) ;
 new x, y
 set x = $get(op("x"), 0)            ; con valor por defecto, clase 074
 set y = $get(op("y"), 0)
 ...
```

Ese patrón es el estándar de facto en el mundo M, y en **VistA** es literalmente la convención de
todas las APIs de FileMan: se rellena un array local con subíndices convenidos y se pasa con punto.

Tiene dos propiedades interesantes. La primera: **el array puede tener cualquier estructura**, así que
un "argumento nombrado" puede ser a su vez un subárbol completo —`opciones("borde","color")`—. Es
JSON antes de JSON.

La segunda: **la rutina llamada puede añadir campos al array**, así que el mismo mecanismo sirve para
devolver resultados y errores, que es lo de la clase 072.

La contrapartida es la de siempre en M: **ningún nombre está declarado en ninguna parte**. Escribir
`opciones("colr")` no da error; simplemente ese campo nunca se lee. La documentación del array es el
único contrato, y por eso FileMan tiene un diccionario que la describe.
"""),
        "smalltalk": ("""
| partes x y |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
x := partes first.
y := partes second.

Transcript
    show: 'punto(x=', x printString, ', y=', y printString, ')';
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** **En Smalltalk todos los argumentos van nombrados,
siempre, y no hay forma de que no lo estén.** El nombre del método está **intercalado** entre ellos:

```smalltalk
Punto x: 10 y: 20
rectangulo desde: origen hasta: esquina
coleccion copyFrom: 1 to: 5
imagen dibujarEn: lienzo con: color grosor: 2 relleno: true
```

Esa última llamada se lee entera sin consultar ninguna firma. Compárala con
`dibujar(lienzo, color, 2, true)` en cualquier lenguaje posicional: los dos últimos argumentos son
indescifrables sin ir a buscar la declaración.

Y la propiedad importante es que **el nombre no es opcional ni decorativo: ES el selector**. El
método se llama `dibujarEn:con:grosor:relleno:`, con las cuatro partes. Cambiar el orden no es
reordenar argumentos: es **llamar a otro método que probablemente no existe**, y el compilador lo
detecta.

De ahí se siguen tres cosas:

1. **No hay sobrecarga**, porque dos métodos con distintos argumentos tienen distinto nombre.
2. **No hacen falta argumentos por defecto**, porque la variante corta es otro selector (clase 074).
3. **No hay confusión de orden**, porque el orden está fijado por el nombre.

Es la decisión de diseño más influyente de Smalltalk que **casi nadie copió** —solo Objective-C y,
parcialmente, Swift—, y sigue siendo la respuesta más limpia a esta clase.
"""),
    },
)

# ---------------------------------------------------------------------------
# 076 — Parámetros variádicos
# ---------------------------------------------------------------------------
SPECS["076"] = dict(
    gancho="""
Una función que suma **todos los números que le pases, sean los que sean**. Los parámetros variádicos
parecen imprescindibles hasta que se cuenta cuántos de estos lenguajes los tienen: **cuatro**. Los
otros ocho resuelven el problema con una idea distinta y, en varios casos, mejor — **pasar una
colección**.
""",
    porque="""
Aquí el concepto es la **aridad variable**, y estos lenguajes lo enseñan porque muestran que hay dos
problemas distintos escondidos bajo el mismo nombre. Uno es **"no sé cuántos valores del mismo tipo
vendrán"**, y para eso un array es mejor que un variádico: **Fortran** lo resuelve con arrays de
forma supuesta, **Ada** con arrays no restringidos y **Pascal** con arrays abiertos, y los tres
conservan el tipo y la comprobación.

El otro es **"no sé cuántos ni de qué tipo"**, que es el caso de `printf`, y ahí sí hacen falta
variádicos de verdad. En C es la fuente de una familia entera de vulnerabilidades; en C++ se resolvió
con paquetes de plantilla comprobados al compilar.
""",
    cierre="""
La regla práctica: **si todos los argumentos son del mismo tipo, no quieres variádicos, quieres una
colección**. Es más seguro, se puede recorrer dos veces, se puede pasar adelante sin perder la aridad,
y el compilador conserva el tipo. Los variádicos solo son necesarios cuando el número **y los tipos**
varían — y entonces la pregunta es si el lenguaje los comprueba (C++, Lisp) o confía (C, PL/I).
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. SUMAVAR.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  I       PIC 9(4)  COMP-3.
01  LARGO   PIC 9(4)  COMP-3.
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(4)  COMP-3.
01  C       PIC X.
01  TOTAL   PIC S9(18) COMP-3.
01  ED-T    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE 0 TO TOTAL
    MOVE SPACES TO TOKEN
    MOVE 0 TO TLEN
    COMPUTE LARGO = FUNCTION LENGTH(FUNCTION TRIM(LINEA)) + 1

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > LARGO
        MOVE LINEA(I:1) TO C
        IF C = SPACE
            IF TLEN > 0
                COMPUTE TOTAL = TOTAL + FUNCTION NUMVAL(TOKEN(1:TLEN))
                MOVE SPACES TO TOKEN
                MOVE 0 TO TLEN
            END-IF
        ELSE
            ADD 1 TO TLEN
            MOVE C TO TOKEN(TLEN:1)
        END-IF
    END-PERFORM

    MOVE TOTAL TO ED-T
    DISPLAY "suma=" FUNCTION TRIM(ED-T)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** **COBOL no tiene parámetros variádicos**, y su respuesta es la
de la clase 065: una **tabla con `OCCURS DEPENDING ON`** y una variable que dice cuántos elementos
son válidos.

```cobol
01  LOTE.
    05  CUANTOS  PIC 9(4) COMP-3.
    05  VALOR    OCCURS 1 TO 500 TIMES
                 DEPENDING ON CUANTOS
                 PIC S9(9) COMP-3.

CALL "SUMAR" USING LOTE
```

Se pasa **un solo argumento** —la estructura entera— y dentro va el contador. Es exactamente lo que
esta clase recomienda: cuando todos los valores son del mismo tipo, una colección es mejor que una
lista variable de argumentos.

Y `OCCURS DEPENDING ON` tiene una propiedad que conviene señalar: **la longitud del registro cambia
con el contador**. Si `CUANTOS` vale 3, la estructura ocupa lo que ocupan tres elementos, no
quinientos. Al escribirla en un fichero, se escribe solo lo usado. Es un registro de longitud
variable declarado de forma declarativa, algo que en C exige el truco del *array flexible* al final
de un `struct`.

Lo que COBOL sí tiene, y es lo más parecido a un variádico, es el **`CALL` con lista variable** en el
sitio de la llamada, más la comprobación de cuántos llegaron con la extensión de IBM. Es incómodo y
apenas se usa: el bloque de parámetros de la clase 075 es la solución idiomática.
"""),
        "fortran": ("""
program suma_variadica
   implicit none
   character(len=1000) :: linea
   integer :: v(200), n, i, ios

   read(*, '(A)') linea

   n = 0
   do i = 1, 200
      read(linea, *, iostat=ios) v(1:i)
      if (ios /= 0) exit
      n = i
   end do

   write(*, '(A,I0)') 'suma=', suma_todos(v(1:n))

contains

   pure function suma_todos(valores) result(s)
      integer, intent(in) :: valores(:)      ! array de FORMA SUPUESTA
      integer :: s
      s = sum(valores)
   end function suma_todos

end program suma_variadica
""", """
**Lo que esta clase enseña en Fortran.** **Fortran no tiene variádicos**, y su respuesta —`valores(:)`,
un **array de forma supuesta**— es probablemente mejor que un variádico para este caso.

`integer, intent(in) :: valores(:)` significa "un array de una dimensión, del tamaño que sea". La
función recibe **el array y su forma**, así que `size(valores)`, `lbound` y `ubound` funcionan dentro
sin que nadie pase un contador.

```fortran
function f(v)
   real, intent(in) :: v(:)        ! forma supuesta: tamaño desconocido, forma conocida
   real, intent(in) :: m(:,:)      ! una matriz de cualquier tamaño
   ...
   n = size(v)                      ! el tamaño viaja CON el array
```

Compara con C, donde hay que pasar `int* v, size_t n` y confiar en que quien llama no se equivoque —
la causa de una parte enorme de los desbordamientos de búfer de la historia.

Fortran tiene además la **forma diferida** (`allocatable`, el tamaño se decide al asignar) y la
**forma explícita** (`v(n)`, con `n` como parámetro anterior), y elegir entre las tres es una decisión
de rendimiento: la forma supuesta pasa un descriptor y permite pasar porciones no contiguas; la
explícita garantiza memoria contigua y vectoriza mejor.

Y para el caso de "distintos tipos", Fortran no tiene nada: la interoperabilidad con `printf` de C se
hace con `iso_c_binding` y es incómoda a propósito.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Suma_Variadica is

   type Vector is array (Positive range <>) of Integer;   --  tamaño NO restringido

   function Suma_Todos (V : Vector) return Integer is
      S : Integer := 0;
   begin
      for E of V loop
         S := S + E;
      end loop;
      return S;
   end Suma_Todos;

   Linea  : String (1 .. 500);
   Ultimo : Natural;
   Pos    : Positive := 1;
   Fin    : Positive;
   Datos  : Vector (1 .. 200);
   N      : Natural := 0;
begin
   Get_Line (Linea, Ultimo);

   while Pos <= Ultimo loop
      N := N + 1;
      Get (Linea (Pos .. Ultimo), Datos (N), Fin);
      Pos := Fin + 1;
   end loop;

   Put ("suma=");
   Put (Suma_Todos (Datos (1 .. N)), Width => 1);
   New_Line;
end Suma_Variadica;
""", """
**Lo que esta clase enseña en Ada.** `array (Positive range <>)` es un **tipo de array no
restringido**: el tipo existe, pero el tamaño se fija al declarar cada objeto. El `<>` se lee "caja",
y es la forma de Ada de decir "aquí va un rango que decidirás luego".

```ada
type Vector is array (Positive range <>) of Integer;

V1 : Vector (1 .. 10);
V2 : Vector (1 .. N);              --  tamaño en EJECUCIÓN
V3 : constant Vector := (1, 2, 3); --  deducido del agregado
```

Y una función que recibe `V : Vector` acepta **cualquiera de los tres**, con sus límites reales
disponibles dentro: `V'First`, `V'Last`, `V'Length`, `V'Range`. **Los límites viajan con el array**,
igual que en Fortran.

Eso es lo que hace innecesarios los variádicos para el caso homogéneo, y además permite la
construcción de este programa: `Datos (1 .. N)` es una **porción**, y pasarla es pasar solo esa parte
sin copiar.

Fíjate también en que `String` en Ada **es exactamente eso**: `array (Positive range <>) of
Character`. Por eso las funciones sobre cadenas de la clase 048 son funciones sobre arrays, y por eso
`Trim` funciona con cualquier longitud.

Ada **no tiene variádicos heterogéneos**, y es deliberado: en un sistema que hay que certificar, una
función cuyo número y tipo de argumentos no se conoce al compilar es exactamente lo que no se quiere.
"""),
        "pascal": ("""
program SumaVariadica;
{$MODE OBJFPC}{$H+}
uses SysUtils;

function SumaTodos(const V: array of Integer): Integer;   { ARRAY ABIERTO }
var
  I: Integer;
begin
  Result := 0;
  for I := Low(V) to High(V) do
    Result := Result + V[I];
end;

var
  Linea, Token: string;
  I: Integer;
  Datos: array of Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea) + ' ';
  SetLength(Datos, 0);
  Token := '';

  for I := 1 to Length(Linea) do
  begin
    if Linea[I] = ' ' then
    begin
      if Token <> '' then
      begin
        SetLength(Datos, Length(Datos) + 1);
        Datos[High(Datos)] := StrToInt(Token);
        Token := '';
      end;
    end
    else
      Token := Token + Linea[I];
  end;

  WriteLn('suma=', IntToStr(SumaTodos(Datos)));
end.
""", """
**Lo que esta clase enseña en Pascal.** `array of Integer` **como tipo de parámetro** es un **array
abierto**: acepta un array de cualquier longitud, y dentro se usan `Low` y `High` para conocer sus
límites. Es la aportación de Turbo Pascal 7 y Delphi, y es el equivalente de la forma supuesta de
Fortran.

Hay un detalle importante: **dentro de la función, un array abierto SIEMPRE va de 0 a High(V)**, sin
importar los índices que tuviera el original. Por eso se escribe `Low(V)` y no `1`.

Y Object Pascal tiene además el **constructor de array en la llamada**, que es lo más parecido a un
variádico:

```pascal
WriteLn(SumaTodos([1, 2, 3, 4]));           { array abierto construido al vuelo }
```

Para el caso **heterogéneo** —el de `printf`— existe `array of const`, que es el mecanismo real de
`Format`:

```pascal
procedure Registrar(const Msg: string; const Args: array of const);
...
Registrar('%s tiene %d años', ['Ada', 36]);
```

`array of const` recibe un array de `TVarRec`, un registro con **una etiqueta de tipo y una unión**.
Es decir: Object Pascal implementa los variádicos heterogéneos **como datos con tipo comprobado en
ejecución**, no como una convención de llamada insegura.

Esa es la diferencia con el `...` de C: aquí el tipo de cada argumento **viaja con él**, así que
`Format` puede comprobar que `%d` recibe un entero en lugar de leer la pila a ciegas.
"""),
        "lisp": ("""
(defun suma-todos (&rest numeros)
  (reduce #'+ numeros :initial-value 0))

(let ((lista (loop for v = (read *standard-input* nil :fin)
                   until (eq v :fin)
                   collect v)))
  (format t "suma=~D~%" (apply #'suma-todos lista)))
""", """
**Lo que esta clase enseña en Common Lisp.** `&rest numeros` recoge **todos los argumentos restantes
en una lista**, y `apply` hace lo contrario: **convierte una lista en argumentos**.

```lisp
(suma-todos 1 2 3)              ; numeros vale (1 2 3)
(apply #'suma-todos '(1 2 3))   ; equivalente: la lista se DESPLIEGA
(apply #'suma-todos 1 2 '(3 4)) ; los primeros sueltos, el último desplegado
```

`&rest` y `apply` son las dos direcciones del mismo puente, y esa simetría es lo que hace cómodo
envolver funciones en Lisp:

```lisp
(defun con-registro (f &rest args)
  (format t "llamando con ~S~%" args)
  (apply f args))                       ; pasa TODO adelante, sin conocer la aridad
```

Esa función envuelve **cualquier** función, con cualquier número de argumentos, sin declarar nada. En
un lenguaje con firmas fijas eso exige plantillas variádicas o reflexión.

Lisp tiene además **`&body`**, que es idéntico a `&rest` pero le dice al editor que ese argumento es
un cuerpo de código y debe indentarlo como tal. Es metadatos para las herramientas dentro de la
firma — un detalle pequeño y muy revelador de una cultura donde el entorno importa tanto como el
lenguaje.

Y hay un límite práctico que conviene conocer: `call-arguments-limit` define cuántos argumentos admite
una llamada. En SBCL es enorme, pero `(apply #'+ lista-de-un-millón)` puede fallar. Para eso está
`reduce`, que es lo que usa este programa por dentro.
"""),
        "tcl": ("""
proc sumaTodos {args} {
    set t 0
    foreach v $args { incr t $v }
    return $t
}

gets stdin linea

puts "suma=[sumaTodos {*}[split [string trim $linea]]]"
""", """
**Lo que esta clase enseña en Tcl.** **`args` es un nombre mágico**: si el último parámetro de un
`proc` se llama exactamente `args`, recibe **una lista con todos los argumentos sobrantes**.

```tcl
proc f {a b args} { ... }
f 1 2 3 4 5          ;# a=1, b=2, args={3 4 5}
```

No hay sintaxis especial —ni `...`, ni `&rest`, ni `*`—: es una **convención sobre el nombre**, lo
que encaja con que la lista de parámetros de `proc` sea una lista normal (clase 074).

Y **`{*}`** es el operador inverso, la **expansión**, añadido en Tcl 8.5:

```tcl
set lista {1 2 3}
sumaTodos $lista          ;# UN argumento: la lista entera como una cadena
sumaTodos {*}$lista       ;# TRES argumentos: 1, 2 y 3
```

Esa distinción es exactamente `f(lista)` frente a `f(*lista)` en Python, y su ausencia era una de las
quejas históricas de Tcl: antes de 8.5 había que usar `eval` con las comillas cuidadosamente puestas,
lo que era lento y una vía de inyección.

`{*}` es un ejemplo curioso de diseño: **no es un comando ni un operador**, es una marca que el
analizador reconoce delante de una palabra. Se eligió esa sintaxis rara precisamente para que no
pudiera chocar con ningún nombre de comando existente en treinta años de código.
"""),
        "perl": ("""
use strict;
use warnings;

sub suma_todos {
    my $t = 0;
    $t += $_ for @_;
    return $t;
}

my $linea = <STDIN>;
chomp $linea;

print "suma=", suma_todos(split ' ', $linea), "\\n";
""", """
**Lo que esta clase enseña en Perl.** En Perl **todas las subrutinas son variádicas por defecto**. No
hay que declarar nada: `@_` contiene lo que haya llegado, y punto. Es el extremo opuesto de Ada.

Y eso ocurre porque **las listas se aplanan al pasarlas**:

```perl
suma_todos(1, 2, 3);              # @_ = (1, 2, 3)
suma_todos(@lista);               # @_ = los elementos de @lista
suma_todos(@a, @b);               # @_ = los de @a Y los de @b, mezclados
```

Esa última línea es la trampa clásica: **no se pueden pasar dos arrays a una función y distinguirlos
dentro**, porque llegan aplanados en uno solo. La solución es pasar **referencias**:

```perl
procesar(\\@a, \\@b);              # dos referencias: dos argumentos
sub procesar { my ($ra, $rb) = @_; ... @$ra ... }
```

Ese aplanamiento es una decisión de diseño muy de Perl —cómoda el 90 % de las veces y sorprendente el
10 %— y es la razón de que las referencias sean tan centrales en el lenguaje.

Con las **firmas** de 5.36, el variádico se declara explícitamente y se puede combinar:

```perl
use v5.36;
sub log_msg ($nivel, @resto) { ... }        # uno fijo y el resto
sub config ($nombre, %opciones) { ... }     # uno fijo y pares nombrados
```

Y `$t += $_ for @_;` de este programa es el modificador de sentencia de la clase 064, con `$_` como
sujeto implícito.
"""),
        "cpp": ("""
#include <iostream>
#include <iterator>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>

int main() {
    std::string linea;
    if (!std::getline(std::cin, linea)) return 1;

    //  El número de valores se conoce en EJECUCIÓN, así que un paquete de
    //  plantilla no sirve: hay que usar un contenedor.
    std::istringstream iss(linea);
    const std::vector<int> v{std::istream_iterator<int>(iss),
                             std::istream_iterator<int>()};

    std::cout << "suma=" << std::accumulate(v.begin(), v.end(), 0) << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** El comentario del código es la lección: **los variádicos de C++
son de tiempo de compilación**, así que no sirven cuando el número de valores se conoce en ejecución.
Para eso, un contenedor.

Cuando sí se conocen al compilar, C++11 trajo los **paquetes de plantilla** y C++17 las **expresiones
de plegado**, que los hacen legibles:

```cpp
template <typename... Args>
auto suma_todos(Args... args) {
    return (args + ... + 0);        // expresión de PLEGADO, C++17
}

suma_todos(1, 2, 3, 4);             // se genera una función para ESTA llamada
```

Y aquí está la diferencia decisiva con el `...` de C: **el paquete conserva los tipos**. El compilador
genera una función específica, comprueba cada argumento y puede integrarla en línea. No hay
`va_arg`, no hay que decir cuántos son y no se puede leer la pila a ciegas.

Ese `...` heredado de C sigue existiendo y es el mecanismo de `printf`, con toda su familia de
vulnerabilidades: si el formato no coincide con los argumentos, `printf` lee memoria arbitraria. Por
eso C++20 añadió **`std::format`**, que valida el formato **en tiempo de compilación**:

```cpp
std::format("{} tiene {} años", nombre, edad);     // comprobado al COMPILAR
std::print("{:.2f}\\n", x);                         // C++23
```

Y para el caso homogéneo hay `std::initializer_list<T>`, que es lo que permite escribir
`f({1, 2, 3})` con tipo comprobado y sin plantillas.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi SUMAVAR;
  linea varchar(200) const;
end-pi;

dcl-s trozos varchar(20) dim(50);
dcl-s i      int(10);
dcl-s total  int(20) inz(0);
dcl-s salida char(40);

trozos = %split(linea : ' ');

for i = 1 to %elem(trozos);
  total += %int(trozos(i));
endfor;

salida = 'suma=' + %char(total);
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG **no tiene variádicos de verdad**, y tiene dos aproximaciones
que conviene distinguir.

La primera es la de la clase 074: **varios `options(*nopass)` y `%parms`**.

```rpgle
dcl-pi *n int(20);
  a int(10) const;
  b int(10) const options(*nopass);
  c int(10) const options(*nopass);
  d int(10) const options(*nopass);
end-pi;

select;
  when %parms = 4; return a + b + c + d;
  when %parms = 3; return a + b + c;
  ...
```

Funciona hasta un máximo fijo y es tan incómodo como parece. Es exactamente lo que hacen las
bibliotecas de C antes de los variádicos: declarar `f2`, `f3`, `f4`.

La segunda, y la correcta, es la de este programa: **pasar una matriz**, con `%elem` para saber
cuántos elementos tiene. Es la misma conclusión que Fortran, Ada y COBOL — **para el caso homogéneo,
una colección**.

Y RPG tiene una tercera vía para el caso heterogéneo, que se usa al llamar a APIs del sistema:
`options(*varsize)` más un puntero y un descriptor de longitud. Es programación de bajo nivel, con las
mismas garantías que el `...` de C —ninguna—, y por eso se limita a las llamadas al sistema
operativo.
"""),
        "pli": ("""
 sumavar: procedure options(main);

    declare linea character(200) varying;
    declare (i, p, total) fixed binary(31);

    get edit (linea) (a(200));
    linea = trim(linea) || ' ';

    total = 0;
    p = 1;
    do i = 1 to length(linea);
       if substr(linea, i, 1) = ' ' then do;
          if i > p then total = total + substr(linea, p, i - p);
          p = i + 1;
       end;
    end;

    put skip list ('suma=' || trim(char(total)));

 end sumavar;
""", """
**Lo que esta clase enseña en PL/I.** PL/I **no tiene variádicos**, y su respuesta es la de los demás
lenguajes de negocio: **arrays con límites consultables**.

```pli
declare v(*) fixed binary(31);          /* array de límites SUPUESTOS */

suma: procedure (v) returns (fixed binary(31));
   declare v(*) fixed binary(31);
   declare (i, t) fixed binary(31);
   t = 0;
   do i = lbound(v, 1) to hbound(v, 1);   /* los límites REALES */
      t = t + v(i);
   end;
   return (t);
end suma;
```

`v(*)` declara un parámetro array **cuyos límites se toman del argumento**, y `lbound`/`hbound` los
consultan dentro. Es exactamente la forma supuesta de Fortran y el array no restringido de Ada.

Y PL/I tiene una capacidad relacionada que no tiene ningún lenguaje del núcleo: **arrays de límites
ajustables en ejecución**, con expresiones que dependen de otros parámetros.

```pli
p: procedure (n, v);
   declare n fixed binary(31);
   declare v(n, n) fixed decimal(15,2);   /* ¡matriz n×n, con n del argumento! */
```

Una matriz cuadrada cuyo tamaño se decide al llamar, con toda la aritmética de arrays de la clase 067
disponible sobre ella. En C haría falta memoria dinámica y aritmética de punteros; en C++, un
`vector<vector<double>>` con su indirección.

Es otra muestra de lo que se repite en toda esta sección: PL/I tenía una cantidad notable de buenas
ideas, y su problema fue el conjunto, no las piezas.
"""),
        "mumps": ("""
SUMAVAR ; Variadicos -- clase 076
 read linea
 write "suma=", $$suma(linea), !
 quit
 ;
suma(l) ; suma los enteros separados por espacio en l
 new i, t
 set t = 0
 for i = 1:1:$length(l, " ") set t = t + $piece(l, " ", i)
 quit t
""", """
**Lo que esta clase enseña en M.** M **sí acepta un número variable de argumentos**, y de la forma más
permisiva posible: **puedes llamar a cualquier rutina con menos o con más argumentos de los
declarados**, sin ninguna comprobación.

```mumps
suma(a, b, c) ;
 quit $get(a, 0) + $get(b, 0) + $get(c, 0)
 ;
 write $$suma(1)          ; b y c quedan indefinidas; $get las pone a 0
 write $$suma(1, 2, 3, 4) ; el cuarto se ignora
```

Es la misma uniformidad de la clase 074: **la ausencia de un parámetro es simplemente una variable no
definida**, y `$data`/`$get` la manejan igual que cualquier otra ausencia.

Para el caso verdaderamente variable, M usa las dos estructuras que ya conocemos:

```mumps
 do PROC^RUT(.datos)          ; un ARRAY por referencia: cualquier número de elementos
 set l = "1^2^3^4"            ; o una cadena con delimitadores
```

El array por referencia es la forma idiomática, y tiene una ventaja sobre los variádicos de otros
lenguajes: **puede ser jerárquico**. `datos("cliente","direccion","calle")` es un argumento tan válido
como `datos(1)`.

Y el M estándar tiene `$quit` y, en implementaciones modernas, formas de consultar cuántos argumentos
se pasaron. Pero el idioma dominante sigue siendo `$get` con valor por defecto, porque no distingue
"no vino" de "vino vacío" — y en M eso casi nunca importa.
"""),
        "smalltalk": ("""
| valores |

valores := stdin nextLine substrings collect: [ :cada | cada asNumber ].

Transcript
    show: 'suma=', (valores inject: 0 into: [ :a :b | a + b ]) printString;
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** **Smalltalk no tiene variádicos, y no puede tenerlos**: el
número de argumentos está fijado por el **selector**, como se vio en la clase 073. Un método llamado
`con:y:` recibe exactamente dos, siempre.

Su respuesta es la que esta clase recomienda: **pasar una colección**.

```smalltalk
coleccion sum
coleccion inject: 0 into: [ :a :b | a + b ]
(Array with: 1 with: 2 with: 3) sum
#(1 2 3 4) sum                        "literal de array"
{ 1. 2. base + 1 } sum                "array construido en EJECUCIÓN"
```

`{ ... }` con puntos es el constructor dinámico de arrays de Pharo, y `#( ... )` el literal. Los dos
producen una colección que se pasa como un único argumento.

Y para el caso en que **el número de argumentos se decide en ejecución** —envolver una llamada, un
proxy, un despachador— Smalltalk tiene el mecanismo de reflexión:

```smalltalk
receptor perform: #con:y: with: 1 with: 2
receptor perform: unSelector withArguments: unArray     "¡el apply de Lisp!"
```

`perform:withArguments:` es exactamente `apply`: toma un **selector** y un **array**, y envía el
mensaje. Con él se escriben proxies genéricos, y combinado con `doesNotUnderstand:` de la clase 051 se
construyen objetos que responden a mensajes que nadie implementó.

Es la misma capacidad que `apply` en Lisp y `{*}` en Tcl, obtenida por reflexión sobre el sistema de
objetos.
"""),
    },
)

# ---------------------------------------------------------------------------
# 077 — Múltiples retornos y desestructuración
# ---------------------------------------------------------------------------
SPECS["077"] = dict(
    gancho="""
Cociente y resto en una sola operación. El procesador los calcula a la vez —una sola instrucción de
división produce los dos—, y sin embargo la mayoría de los lenguajes obligan a pedirlos por separado
y a dividir dos veces. Esta clase es sobre **cómo devuelve un lenguaje más de un valor**, y sobre por
qué **COBOL, que es de 1959, lo hace mejor que C**.
""",
    porque="""
Aquí el concepto es el **retorno múltiple**, y estos lenguajes cubren las cuatro estrategias.
**COBOL** tiene `DIVIDE … GIVING … REMAINDER`: una sentencia, dos resultados, que es lo que hace el
hardware. **Ada, Fortran, Pascal, PL/I y RPG** usan **parámetros de salida**, con el modo declarado
en la firma. **Lisp** tiene **valores múltiples**, un mecanismo del lenguaje sin coste. Y **Perl,
Tcl, M y Smalltalk** devuelven una **estructura** y la desmontan al recibirla.

Y C++ estuvo cuarenta años sin nada de esto hasta las **descomposiciones estructuradas** de C++17.
""",
    cierre="""
Lo transferible: **si dos valores se calculan juntos, devolverlos juntos evita calcular dos veces**.
`divmod`, `minmax`, `find` con posición y encontrado, `parse` con valor y resto — todos son la misma
forma. Y la desestructuración en el sitio de la recepción es lo que hace que esa forma sea cómoda: sin
ella, un retorno múltiple obliga a declarar variables antes y estorba más de lo que ayuda. Por eso las
dos características —devolver varios y desmontarlos— aparecen siempre juntas en los lenguajes
modernos.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. DIVMOD.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TXT-A   PIC X(20).
01  TXT-B   PIC X(20).
01  A       PIC S9(9) COMP-3.
01  B       PIC S9(9) COMP-3.
01  COC     PIC S9(9) COMP-3.
01  RES     PIC S9(9) COMP-3.
01  ED-C    PIC -(8)9.
01  ED-R    PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    DIVIDE A BY B GIVING COC REMAINDER RES

    MOVE COC TO ED-C
    MOVE RES TO ED-R
    DISPLAY "cociente=" FUNCTION TRIM(ED-C)
            " resto=" FUNCTION TRIM(ED-R)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** **`DIVIDE A BY B GIVING COC REMAINDER RES` es una sola
sentencia que produce dos resultados**, y es exactamente lo que hace el procesador: la instrucción de
división de cualquier arquitectura devuelve cociente y resto a la vez.

En C hay que escribir `a / b` y `a % b`. El compilador **suele** reconocer el patrón y emitir una sola
división, pero es una optimización, no una garantía — y por eso la biblioteca estándar de C tiene
`div()` y `ldiv()`, que devuelven una estructura con los dos.

COBOL lo tiene en el verbo desde 1959, y no es el único caso:

```cobol
DIVIDE A BY B GIVING C REMAINDER R
UNSTRING LINEA DELIMITED BY "," INTO A B C
    WITH POINTER P TALLYING EN N          *> ¡tres salidas a la vez!
INSPECT TEXTO TALLYING N FOR ALL "a"
    REPLACING ALL "b" BY "c"              *> cuenta Y sustituye en una pasada
```

`UNSTRING` con `POINTER` y `TALLYING` devuelve los trozos, la posición final **y** cuántos campos
llenó. `INSPECT` cuenta y sustituye en un solo recorrido.

El patrón de fondo es el mismo: **los verbos de COBOL están diseñados alrededor de lo que la máquina
hace en una pasada**, no alrededor de la idea matemática de función con un solo resultado. Es una
consecuencia de venir del hardware en lugar de venir del cálculo lambda, y en esta clase concreta
juega a su favor.
"""),
        "fortran": ("""
program divmod
   implicit none
   integer :: a, b, cociente, resto

   read(*, *) a, b
   call dividir(a, b, cociente, resto)

   write(*, '(A,I0,A,I0)') 'cociente=', cociente, ' resto=', resto

contains

   pure subroutine dividir(x, y, coc, res)
      integer, intent(in)  :: x, y
      integer, intent(out) :: coc, res      ! DOS salidas declaradas
      coc = x / y
      res = mod(x, y)
   end subroutine dividir

end program divmod
""", """
**Lo que esta clase enseña en Fortran.** La distinción entre **`function`** y **`subroutine`** de
Fortran existe precisamente para esto: una función devuelve **un** valor y se usa dentro de una
expresión; una subrutina no devuelve nada y comunica por **parámetros `intent(out)`**.

```fortran
y = f(x)                      ! función: un resultado, dentro de una expresión
call s(x, a, b, c)            ! subrutina: varios resultados, sentencia propia
```

Y `intent(out)` tiene una garantía que conviene conocer: **el valor de entrada del argumento no
existe dentro de la subrutina**. El compilador puede asumirlo y avisar si lo lees antes de asignarlo.
No es solo documentación; cambia lo que el optimizador puede suponer.

Cuando los valores están relacionados, el Fortran moderno prefiere un **tipo derivado**, que es la
alternativa a los parámetros de salida:

```fortran
type :: Resultado
   integer :: cociente, resto
end type

function dividir(x, y) result(r)
   type(Resultado) :: r
   r%cociente = x / y
   r%resto = mod(x, y)
end function
```

Devolver una estructura es más limpio en el sitio de la llamada —`z = dividir(a, b)`— y permite usar
el resultado en una expresión. Lo que Fortran **no** tiene es desestructuración: hay que escribir
`z%cociente`, no `[c, r] = dividir(...)`.

Y `pure subroutine` es legal: una subrutina puede ser pura si sus únicos efectos son sus `intent(out)`.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Divmod is

   procedure Dividir (X, Y : in Integer; Coc, Res : out Integer) is
   begin
      Coc := X / Y;
      Res := X mod Y;
   end Dividir;

   A, B, Cociente, Resto : Integer;
begin
   Get (A);
   Get (B);
   Dividir (A, B, Cociente, Resto);

   Put ("cociente="); Put (Cociente, Width => 1);
   Put (" resto=");   Put (Resto, Width => 1);
   New_Line;
end Divmod;
""", """
**Lo que esta clase enseña en Ada.** Los parámetros `out` son el mecanismo, y Ada añade una garantía
que ningún otro lenguaje de esta página da: **el compilador comprueba que todo `out` se asigne en
todos los caminos** antes de salir, y avisa si se lee antes de escribirlo.

Y la alternativa idiomática, cuando los valores forman una unidad conceptual, es **devolver un
registro**:

```ada
type Division is record
   Cociente, Resto : Integer;
end record;

function Dividir (X, Y : Integer) return Division is
begin
   return (Cociente => X / Y, Resto => X mod Y);    --  agregado NOMBRADO
end Dividir;

D : constant Division := Dividir (17, 5);
```

Fíjate en dos cosas. La primera: el **agregado con nombres** de la clase 075 hace que el retorno se
lea sin ambigüedad. La segunda, y es la que importa: **el resultado puede declararse `constant`**, cosa
imposible con parámetros `out`.

Ese es el argumento que empujó a Ada 2012 a permitir funciones con efectos y que empuja hoy a todos
los lenguajes hacia devolver estructuras en lugar de rellenar parámetros: **inmutabilidad**.

Lo que Ada no tiene es desestructuración en la recepción. `D.Cociente` es la forma; no existe
`(C, R) := Dividir (...)`. Es la misma carencia que Fortran, y la diferencia con Lisp, Perl, Tcl y el
C++ moderno.
"""),
        "pascal": ("""
program Divmod;
{$MODE OBJFPC}{$H+}
uses SysUtils;

procedure Dividir(X, Y: Integer; out Coc, Res: Integer);
begin
  Coc := X div Y;
  Res := X mod Y;
end;

var
  A, B, Cociente, Resto: Integer;

begin
  Read(A, B);
  Dividir(A, B, Cociente, Resto);

  WriteLn('cociente=', IntToStr(Cociente), ' resto=', IntToStr(Resto));
end.
""", """
**Lo que esta clase enseña en Pascal.** `out` en Object Pascal es lo mismo que en Ada: **solo
escritura**, el valor de entrada no cuenta. Se distingue de `var` —que es entrada y salida— y del paso
por valor.

Hay un detalle de implementación que diferencia `out` de `var` en Delphi y que conviene conocer:
**con `out`, el compilador libera el valor anterior del argumento antes de la llamada** si es un tipo
gestionado —una cadena, una interfaz, un array dinámico—. Con `var` no lo hace. Elegir mal produce
fugas o liberaciones dobles con tipos gestionados.

La alternativa de Pascal es el **registro**, y Object Pascal moderno permite devolverlo directamente:

```pascal
type
  TDivision = record
    Cociente, Resto: Integer;
  end;

function Dividir(X, Y: Integer): TDivision;
begin
  Result.Cociente := X div Y;
  Result.Resto := X mod Y;
end;
```

Es más limpio y permite `const D := Dividir(17, 5);` con la inferencia de la clase 052.

Y Pascal **no tiene desestructuración**: hay que escribir `D.Cociente`. Es una carencia que se nota
al lado de Lisp o del C++17 de esta misma página, y que ninguna versión ha resuelto.
"""),
        "lisp": ("""
(let* ((a (read))
       (b (read)))
  (multiple-value-bind (cociente resto) (truncate a b)
    (format t "cociente=~D resto=~D~%" cociente resto)))
""", """
**Lo que esta clase enseña en Common Lisp.** `truncate` **ya devuelve los dos valores**: no hay que
escribir nada. Es una función del estándar, y devolver cociente y resto juntos es su comportamiento
normal desde 1984.

Los **valores múltiples** de Lisp son un mecanismo del lenguaje, no una tupla, y esa diferencia es la
clave:

```lisp
(truncate 17 5)                                  ; en contexto normal, solo el PRIMERO
(multiple-value-bind (c r) (truncate 17 5) ...)   ; los dos
(multiple-value-list (truncate 17 5))             ; => (3 2)  como lista, si hace falta
(nth-value 1 (truncate 17 5))                     ; => 2  solo el segundo
(values 1 2 3)                                    ; devolver varios
(values)                                          ; devolver NINGUNO
```

**Ignorar los valores extra es gratis**: no se construye ninguna estructura, no hay que escribir `_`
y no hay coste. En Go hay que poner `_`; en Rust hay que destruir la tupla; en Python se construye
una tupla real aunque solo quieras el primero.

Toda la biblioteca lo aprovecha, y ya lo hemos visto en varias clases: `gethash` devuelve valor y "¿la
clave estaba?" (053), `floor` y `round` devuelven cociente y resto (049), `parse-integer` devuelve el
número y dónde paró, `read-line` devuelve la línea y si terminó por fin de fichero.

Y `destructuring-bind` cubre la otra mitad de esta clase —desmontar una estructura anidada— con
soporte para opcionales, `&rest` y valores por defecto, como se vio en la clase 062.
"""),
        "tcl": ("""
proc dividir {a b} {
    return [list [expr {$a / $b}] [expr {$a % $b}]]
}

gets stdin linea
lassign [split [string trim $linea]] a b
lassign [dividir $a $b] cociente resto

puts "cociente=$cociente resto=$resto"
""", """
**Lo que esta clase enseña en Tcl.** Como **todo comando devuelve una cadena**, devolver varios
valores es devolver **una lista**, y `lassign` la desmonta. Es el mismo mecanismo para las dos
direcciones.

```tcl
lassign {1 2 3} a b c           ;# a=1 b=2 c=3
lassign {1 2} a b c             ;# c queda VACÍA, no da error
set sobra [lassign {1 2 3 4} a b]   ;# lassign DEVUELVE lo que sobró: {3 4}
```

Ese último detalle es útil y poco conocido: `lassign` devuelve los elementos no asignados, así que se
puede encadenar para procesar una lista por trozos.

Y Tcl tiene una segunda vía, la de la clase 073: **modificar las variables del llamante** con
`upvar`.

```tcl
proc dividir {a b cocVar resVar} {
    upvar 1 $cocVar coc
    upvar 1 $resVar res
    set coc [expr {$a / $b}]
    set res [expr {$a % $b}]
}
dividir 17 5 c r        ;# se pasan los NOMBRES de las variables
```

`upvar 1 $nombre local` liga una variable local al **nombre** de una variable del llamante. Es el
paso por referencia de Tcl, y funciona porque en Tcl las variables se identifican por su nombre en
tiempo de ejecución.

Ese es el mecanismo con el que están escritos comandos como `scan`, `regexp` y `binary scan`, que
dejan sus resultados en variables en lugar de devolverlos — como se vio en la clase 062.
"""),
        "perl": ("""
use strict;
use warnings;

sub dividir {
    my ($x, $y) = @_;
    return (int($x / $y), $x % $y);      # devolver una LISTA
}

my $linea = <STDIN>;
chomp $linea;
my ($p, $q) = split ' ', $linea;

my ($cociente, $resto) = dividir($p, $q);

print "cociente=$cociente resto=$resto\\n";
""", """
**Lo que esta clase enseña en Perl.** Las subrutinas de Perl **devuelven listas de forma nativa**, y
la asignación de listas las desmonta. No hay tuplas ni estructuras: es el mismo mecanismo de la clase
076, en la dirección contraria.

Y aquí aparece el **contexto** de la clase 041 en su forma más importante:

```perl
my ($c, $r) = dividir(17, 5);     # contexto de LISTA: recibe los dos
my $x = dividir(17, 5);           # contexto ESCALAR: recibe... ¿qué?
```

Esa segunda línea es la trampa. `return (a, b)` en contexto escalar **no devuelve una lista**:
devuelve **el último elemento**, porque el operador coma en contexto escalar evalúa y descarta. Así
que `$x` vale el resto, no el cociente ni un contador.

Por eso el idioma correcto en Perl es usar `wantarray` de la clase 072 para decidir, o devolver una
**referencia** cuando el resultado debe comportarse como una unidad:

```perl
return { cociente => $c, resto => $r };     # una referencia a hash
my $d = dividir(17, 5);
print $d->{cociente};
```

La desestructuración de Perl va bastante lejos, con `undef` para descartar y desmontado de hashes:

```perl
my (undef, $segundo, @resto) = @lista;      # descartar el primero
my ($a, $b) = @hash{qw(x y)};                # "rebanada" de hash por claves
```

Lo que no tiene es desestructuración anidada al estilo de JavaScript o Rust; para eso está
`List::Util` o la desreferencia explícita.
"""),
        "cpp": ("""
#include <iostream>

struct Division {
    int cociente;
    int resto;
};

Division dividir(int a, int b) {
    return {a / b, a % b};
}

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    const auto [cociente, resto] = dividir(a, b);   // DESCOMPOSICIÓN, C++17

    std::cout << "cociente=" << cociente << " resto=" << resto << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** `auto [cociente, resto] = ...` es la **descomposición
estructurada**, y llegó con **C++17**. Antes de eso, devolver dos valores era incómodo de las tres
maneras posibles:

```cpp
// 1) Parámetros de salida, como C
void dividir(int a, int b, int* c, int* r);

// 2) std::pair, con nombres inútiles
std::pair<int,int> d = dividir(a, b);
usar(d.first, d.second);          // ¿cuál era cuál?

// 3) std::tie, con las variables declaradas ANTES
int c, r;
std::tie(c, r) = dividir(a, b);   // no permite const, no permite auto
```

La descomposición resuelve las tres: **declara, nombra y permite `const`** en una sola línea. Y
funciona sobre `std::pair`, `std::tuple`, arrays y **cualquier estructura con campos públicos** — como
la `Division` de este programa, sin necesidad de que herede ni implemente nada.

Combinada con el `if` con inicializador de la clase 058, da el idioma moderno para las operaciones que
devuelven valor y estado:

```cpp
if (const auto [it, insertado] = conjunto.insert(x); insertado) { ... }
for (const auto& [clave, valor] : mapa) { ... }
```

Un detalle que conviene conocer: **los nombres de la descomposición no son variables de verdad**, son
alias de los miembros. Por eso no se pueden capturar en una lambda en C++17 —se arregló en C++20— y
por eso `auto&` frente a `auto` cambia si se copia o no toda la estructura.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi DIVMOD;
  a int(10) const;
  b int(10) const;
end-pi;

dcl-ds resultado qualified;
  cociente int(10);
  resto    int(10);
end-ds;

dcl-s salida char(60);

resultado.cociente = %div(a : b);
resultado.resto    = %rem(a : b);

salida = 'cociente=' + %char(resultado.cociente)
       + ' resto='   + %char(resultado.resto);
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG tiene las dos formas, y la elección entre ellas cambió con el
tiempo.

La clásica son los **parámetros de salida**: como el paso por referencia es el defecto en RPG
(clase 073), cualquier parámetro sin `const` ni `value` es una salida potencial.

```rpgle
dcl-pr dividir;
  a   int(10) const;
  b   int(10) const;
  coc int(10);          // sin const: se MODIFICA
  res int(10);
end-pr;
```

La moderna, y la recomendada, es **devolver una estructura de datos**, como en este programa. Desde
IBM i 7.2, un subprocedimiento **puede devolver una `dcl-ds` completa**:

```rpgle
dcl-proc dividir;
  dcl-pi *n likeds(tipoResultado);
    a int(10) const;
    b int(10) const;
  end-pi;
  dcl-ds r likeds(tipoResultado);
  r.cociente = %div(a : b);
  r.resto = %rem(a : b);
  return r;
end-proc;
```

Antes de 7.2 eso no era posible y había que usar parámetros de salida obligatoriamente. Es otro
ejemplo de característica añadida recientemente a un lenguaje de 1959.

RPG **no tiene desestructuración**: hay que escribir `r.cociente`. Y `qualified` sigue siendo
necesario para que los subcampos no invadan el espacio de nombres global, como se vio en la clase 075.
"""),
        "pli": ("""
 divmod: procedure options(main);

    declare (a, b, cociente, resto) fixed binary(31);

    get list (a, b);
    call dividir(a, b, cociente, resto);

    put skip list ('cociente=' || trim(char(cociente)) ||
                   ' resto='   || trim(char(resto)));

 dividir: procedure (x, y, coc, res);
    declare (x, y, coc, res) fixed binary(31);
    coc = divide(x, y, 31);
    res = mod(x, y);
 end dividir;

 end divmod;
""", """
**Lo que esta clase enseña en PL/I.** PL/I usa parámetros de salida, con la particularidad de la clase
073: **el paso es por referencia por defecto**, así que cualquier parámetro que se asigne dentro
modifica el del llamante. No hay que declarar nada — y por eso tampoco hay forma de saber, leyendo la
llamada, cuáles son salidas.

Ese es exactamente el problema que resolvieron los modos `in`/`out` de Ada y los `intent` de Fortran.

Lo que PL/I sí tiene, y es su aportación a esta clase, es que **una función puede devolver una
estructura completa**, con toda la aritmética de estructuras disponible:

```pli
declare 1 division,
          2 cociente fixed binary(31),
          2 resto    fixed binary(31);

f: procedure (x, y) returns (like division);   /* LIKE: el tipo de otra estructura */
   declare 1 r like division;
   r.cociente = divide(x, y, 31);
   r.resto = mod(x, y);
   return (r);
end f;
```

`returns (like division)` usa el atributo `like` de la clase 052 para no repetir la declaración. Y
`by name` de la clase 075 permite copiar entre estructuras emparejando campos.

PL/I **no tiene desestructuración**, pero tiene algo cercano en el otro sentido: **`get data`** de la
clase 056, que lee variables **por su nombre** desde la entrada. Es desmontar una estructura textual
en variables, resuelto en el sistema de E/S en lugar de en la asignación.
"""),
        "mumps": ("""
DIVMOD ; Multiples retornos -- clase 077
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 set r = $$dividir(a, b)
 write "cociente=", $piece(r, "^", 1)
 write " resto=", $piece(r, "^", 2), !
 quit
 ;
dividir(x, y) ; devuelve "cociente^resto"
 quit (x\\y) _ "^" _ (x#y)
""", """
**Lo que esta clase enseña en M.** Devolver **una cadena con delimitador** —`"3^2"`— es el idioma de M
para los resultados compuestos, y ya apareció en las clases 048 y 072. `$piece` es la
desestructuración.

Pero M tiene una segunda forma, más potente, que es la que se usa en las APIs reales: **rellenar un
array pasado por referencia**.

```mumps
 do DIVIDIR^MAT(17, 5, .resultado)
 write resultado("cociente"), " ", resultado("resto")
 ;
DIVIDIR(x, y, res) ;
 set res("cociente") = x\\y
 set res("resto") = x#y
 quit
```

Ese patrón tiene tres ventajas sobre la cadena: **los campos van nombrados** (clase 075), **puede ser
jerárquico**, y **no hay límite de tamaño**. Es la convención de FileMan y de prácticamente todas las
APIs de VistA.

Y como se vio en la clase 072, el mismo array sirve para devolver **el resultado y los errores** a la
vez, en subárboles distintos:

```mumps
 set res("datos", 1) = ...
 set res("error", "codigo") = ...
```

En un lenguaje sin tipos, sin estructuras y sin retornos múltiples, **el array local por referencia
acaba haciendo de todo**: parámetros nombrados, retorno múltiple, estructura anidada y canal de
errores. Es una sola herramienta muy afilada, que es la descripción exacta de M.
"""),
        "smalltalk": ("""
| partes a b resultado |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

resultado := Array with: a // b with: a \\\\ b.

Transcript
    show: 'cociente=', resultado first printString;
    show: ' resto=', resultado second printString;
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk **no tiene retornos múltiples**: un método
devuelve **un objeto**, siempre. Y no lo echa de menos, porque devolver un objeto compuesto es
barato:

```smalltalk
^Array with: cociente with: resto           "un array"
^cociente -> resto                           "una ASOCIACIÓN clave->valor"
^Dictionary newFrom: { #cociente -> c. #resto -> r }
^DivisionResultado cociente: c resto: r      "una CLASE propia"
```

La cuarta es la que la comunidad recomienda, y el argumento es de diseño: **si dos valores van
siempre juntos, probablemente son un concepto que merece nombre**. Un `Punto`, un `Intervalo`, un
`ResultadoDeBusqueda`. Devolver una tupla anónima es aplazar esa decisión.

Y hay una alternativa muy idiomática que evita el problema por completo: **pasar un bloque que reciba
los dos valores**.

```smalltalk
Numero >> dividir: b conResultado: unBloque
    ^unBloque value: self // b value: self \\\\ b

17 dividir: 5 conResultado: [ :c :r | Transcript show: c printString, '/', r printString ]
```

El "retorno múltiple" se convierte en **una llamada con dos argumentos**, y no hay estructura
intermedia que construir ni desmontar. Es el mismo patrón que `at:ifAbsent:` de la clase 072 — en un
lenguaje donde pasar código es gratis, muchos problemas de retorno se convierten en problemas de
continuación.

Y `\\\\` y `//` son el resto y la división al suelo de la clase 055.
"""),
    },
)

# ---------------------------------------------------------------------------
# 078 — Genéricos y polimorfismo paramétrico
# ---------------------------------------------------------------------------
SPECS["078"] = dict(
    gancho="""
El mayor de dos valores. Escrito una vez y que funcione **con enteros, con reales, con fechas y con
cualquier cosa que se pueda comparar**. Eso es el polimorfismo paramétrico, y esta clase reparte a
los doce lenguajes en tres grupos muy nítidos: los que lo resuelven **al compilar**, los que lo
resuelven **al ejecutar** por no tener tipos, y los que **no lo resuelven**.
""",
    porque="""
Aquí el concepto son los **genéricos**, y estos lenguajes lo enseñan porque **Ada los tuvo primero, en
1983**, con un diseño que sigue siendo el más explícito de todos: los parámetros del genérico se
declaran, incluidas las operaciones que necesita, y la instanciación es una sentencia visible. C++
llegó después con las plantillas —más potentes y con la instanciación implícita—, y Java y C# mucho
más tarde.

Y en el otro extremo, **COBOL no tiene genéricos** y **Fortran los resuelve con interfaces genéricas**
que son sobrecarga con otro nombre. Ver las tres estrategias juntas explica por qué "genérico"
significa cosas distintas según el lenguaje.
""",
    cierre="""
Lo transferible es la distinción entre **borrado de tipos** y **monomorfización**. Java borra: hay
**una** versión del código y los tipos desaparecen en ejecución. C++, Ada y Rust **generan una versión
por cada tipo usado**: más rápido, sin conversiones, y a costa de binarios grandes y tiempos de
compilación largos. Ninguna es mejor en abstracto, y saber cuál usa tu lenguaje explica sus tiempos de
compilación, el tamaño de su binario y por qué en Java no puedes hacer `new T[]`.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. MAXIMO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  TXT-A   PIC X(20).
01  TXT-B   PIC X(20).
01  A       PIC S9(9) COMP-3.
01  B       PIC S9(9) COMP-3.
01  MAYOR   PIC S9(9) COMP-3.
01  ED-M    PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES INTO TXT-A TXT-B
    MOVE FUNCTION NUMVAL(TXT-A) TO A
    MOVE FUNCTION NUMVAL(TXT-B) TO B

    COMPUTE MAYOR = FUNCTION MAX(A, B)

    MOVE MAYOR TO ED-M
    DISPLAY "max=" FUNCTION TRIM(ED-M)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** **COBOL no tiene genéricos, y no los ha tenido nunca.** Cada
subprograma trabaja con los tipos exactos declarados en su `LINKAGE SECTION`, y para otro tipo hay
que escribir otro subprograma.

Lo que sí tiene, y cumple una función parecida, es el **copybook con `REPLACING`**:

```cobol
*> En el copybook TABLA:
01  :PREFIJO:-TABLA.
    05  :PREFIJO:-CUANTOS  PIC 9(4) COMP-3.
    05  :PREFIJO:-ELEM     OCCURS 1 TO 100 TIMES
                           DEPENDING ON :PREFIJO:-CUANTOS
                           PIC :TIPO:.

*> Y en cada programa:
COPY TABLA REPLACING ==:PREFIJO:== BY ==CLI==
                     ==:TIPO:==    BY ==X(40)==.
COPY TABLA REPLACING ==:PREFIJO:== BY ==IMP==
                     ==:TIPO:==    BY ==S9(11)V99 COMP-3==.
```

`COPY ... REPLACING` es **sustitución textual en tiempo de compilación**, parametrizada. Es
exactamente lo que hacían las macros de C antes de las plantillas, y tiene los mismos problemas:
ninguna comprobación de tipos, errores que aparecen en el texto expandido, y ninguna forma de
restringir qué se puede sustituir.

Es genérico en el sentido más literal —el mismo texto, con otros nombres— y es la razón de que el
material de esta clase sea tan revelador: **la diferencia entre una macro y un genérico es la
comprobación**, y esa comprobación es lo que Ada añadió en 1983.

`FUNCTION MAX` de este programa sí es polimórfica, pero está incorporada al compilador: no se puede
escribir otra igual.
"""),
        "fortran": ("""
program maximo
   implicit none
   integer :: a, b

   read(*, *) a, b
   write(*, '(A,I0)') 'max=', mayor(a, b)

contains

   pure function mayor(x, y) result(m)
      integer, intent(in) :: x, y
      integer :: m
      m = merge(x, y, x > y)
   end function mayor

end program maximo
""", """
**Lo que esta clase enseña en Fortran.** Fortran **no tiene genéricos con parámetros de tipo**. Lo que
tiene son **interfaces genéricas**, que son sobrecarga: se escriben varias versiones y se agrupan bajo
un nombre común.

```fortran
interface mayor
   module procedure mayor_entero
   module procedure mayor_real
   module procedure mayor_doble
end interface

! Y ahora `mayor(a, b)` elige según los tipos, en tiempo de compilación.
```

Es exactamente el mecanismo con el que están construidas las funciones intrínsecas del propio
lenguaje: `max`, `abs`, `sqrt` y `sum` funcionan con todos los tipos numéricos porque hay una versión
por tipo detrás.

El precio es evidente: **hay que escribir cada versión**. Para una función corta como esta, es
copiar y pegar cambiando el tipo — el problema que los genéricos vinieron a resolver.

Por eso una parte del mundo Fortran usa **el preprocesador de C** (`fpp` o `cpp`) para generar las
versiones a partir de una plantilla:

```fortran
#define TIPO integer
#include "mayor.inc"
#define TIPO real(real64)
#include "mayor.inc"
```

Que es, otra vez, la macro textual de COBOL con otra sintaxis.

El comité lleva años trabajando en **plantillas genéricas** para el estándar siguiente, y es la
característica más pedida por la comunidad. En 2026 todavía no están, y es probablemente la carencia
más señalada del lenguaje.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Generico is

   --  Un GENÉRICO: declara qué necesita del tipo que le pasen.
   generic
      type Elemento is private;
      with function "<" (L, R : Elemento) return Boolean is <>;
   function Mayor_Gen (A, B : Elemento) return Elemento;

   function Mayor_Gen (A, B : Elemento) return Elemento is
   begin
      if A < B then
         return B;
      else
         return A;
      end if;
   end Mayor_Gen;

   --  INSTANCIACIÓN explícita: se genera la versión para Integer.
   function Mayor is new Mayor_Gen (Integer);

   A, B : Integer;
begin
   Get (A);
   Get (B);

   Put ("max=");
   Put (Mayor (A, B), Width => 1);
   New_Line;
end Generico;
""", """
**Lo que esta clase enseña en Ada.** **Ada tuvo genéricos en 1983**, antes que C++, Java y C#, y su
diseño sigue siendo el más explícito de todos. La clave está en el bloque `generic`:

```ada
generic
   type Elemento is private;                                  --  el TIPO
   with function "<" (L, R : Elemento) return Boolean is <>;  --  la OPERACIÓN que necesita
```

**El genérico declara todo lo que exige del tipo**: no basta con decir "un tipo cualquiera", hay que
enumerar las operaciones que se van a usar. Si el tipo que instancias no tiene `<`, **no compila la
instanciación**, con un error que apunta al sitio correcto.

Compara con las plantillas de C++ antes de los conceptos: allí el error aparecía **dentro** de la
plantilla, con veinte niveles de expansión, y decía algo sobre un operador que faltaba en una línea
que no habías escrito. Los **conceptos de C++20** son exactamente esto de Ada, cuarenta años después.

Y la **instanciación es explícita**: `function Mayor is new Mayor_Gen (Integer);` es una sentencia que
se ve. En C++ ocurre sola al usar la plantilla, lo que es cómodo y hace muy difícil saber cuántas
versiones se están generando —una de las causas de los binarios enormes y las compilaciones lentas—.

Ada permite además parametrizar por **paquete completo**, no solo por tipo o función, lo que da un
sistema de módulos genéricos que Java y C# no tienen. Toda la biblioteca de contenedores de Ada 2005
está construida así.
"""),
        "pascal": ("""
program Maximo;
{$MODE OBJFPC}{$H+}
uses SysUtils, Math;

var
  A, B: Integer;

begin
  Read(A, B);
  WriteLn('max=', IntToStr(Max(A, B)));
end.
""", """
**Lo que esta clase enseña en Pascal.** El Pascal ISO **no tiene genéricos**, y su sustituto histórico
era el **puntero sin tipo** —`Pointer`— con conversiones manuales, que es tan inseguro como suena.

Free Pascal y Delphi los añadieron en 2006, con una sintaxis propia:

```pascal
{ Free Pascal, modo ObjFPC }
generic function Mayor<T>(A, B: T): T;
begin
  if A < B then Result := B else Result := A;
end;

var
  M: Integer;
begin
  M := specialize Mayor<Integer>(3, 7);
end.
```

Las palabras **`generic`** y **`specialize`** son obligatorias en modo ObjFPC, y no existen en Delphi
—que usa la sintaxis `function Mayor<T>(...)` sin adornos—. Esa divergencia entre los dos dialectos es
una de las incompatibilidades más molestas del ecosistema Pascal.

Y hay una restricción importante: **el genérico se resuelve por instanciación explícita**, como en Ada,
y **no hay inferencia de argumentos de tipo** en las funciones libres. Hay que escribir
`specialize Mayor<Integer>(...)`, no `Mayor(3, 7)`. Delphi sí infiere en muchos casos.

Los genéricos de Object Pascal **generan código por tipo** —monomorfización, como C++ y Ada— así que
son rápidos y engordan el binario. `Generics.Collections` es la biblioteca estándar construida sobre
ellos, y es lo que dio a Delphi contenedores con tipos treinta años después de Turbo Pascal.
"""),
        "lisp": ("""
(defun mayor (a b)
  (if (< a b) b a))

(let* ((a (read))
       (b (read)))
  (format t "max=~D~%" (mayor a b)))
""", """
**Lo que esta clase enseña en Common Lisp.** En un lenguaje dinámico, **el polimorfismo paramétrico es
gratis**: `mayor` funciona con enteros, reales, fracciones, cadenas y cualquier cosa para la que `<`
esté definido. No hay que declarar nada.

Lo que Lisp añade, y no tiene ningún lenguaje del núcleo, es el **despacho múltiple** de CLOS:

```lisp
(defgeneric combinar (a b))

(defmethod combinar ((a number) (b number))  (+ a b))
(defmethod combinar ((a string) (b string))  (concatenate 'string a b))
(defmethod combinar ((a list)   (b list))    (append a b))
(defmethod combinar ((a number) (b string))  (format nil "~D~A" a b))
```

El método se elige según **los tipos de TODOS los argumentos**, no solo del primero. En Java, C++ o
Smalltalk el despacho es sobre el receptor y punto: para depender de dos tipos hay que usar el patrón
*Visitor*, que es notoriamente incómodo.

Y CLOS añade los **métodos auxiliares**, que permiten componer comportamiento sin herencia:

```lisp
(defmethod combinar :before ((a number) (b number)) (print "sumando..."))
(defmethod combinar :around (a b) (list :resultado (call-next-method)))
```

`:before`, `:after` y `:around` se ejecutan alrededor del método principal. Es programación orientada
a aspectos, en el estándar de 1994.

Y para el rendimiento, las **declaraciones de tipo** de la clase 052 permiten que SBCL genere código
especializado cuando hace falta: lo genérico por defecto, lo específico cuando se pide.
"""),
        "tcl": ("""
proc mayor {a b} {
    return [expr {$a > $b ? $a : $b}]
}

gets stdin linea
lassign [split [string trim $linea]] a b

puts "max=[mayor $a $b]"
""", """
**Lo que esta clase enseña en Tcl.** Sin tipos no hay nada que parametrizar: `mayor` funciona con lo
que sea que `expr` sepa comparar. Es polimorfismo por ausencia de restricciones.

Y esa ausencia tiene una consecuencia que conviene ver: **la comparación depende de cómo interprete
`expr` los operandos**, no de un tipo declarado.

```tcl
expr {"10" > "9"}          ;# 1  -- los lee como NÚMEROS
expr {"abc" > "abd"}       ;# 0  -- como CADENAS, porque no son números
expr {"10" gt "9"}         ;# 0  -- forzando comparación de cadenas
```

Es exactamente la ambigüedad de la clase 051, aquí aplicada a una función "genérica": la misma función
compara de dos maneras distintas según los datos que reciba, y **eso puede ser lo que quieres o un
error silencioso**.

Cuando el comportamiento debe ser explícito, Tcl usa lo que la clase 068 llamaba tabla de despacho:
**pasar el comparador como argumento**.

```tcl
proc mayorCon {a b comparador} {
    return [expr {[apply $comparador $a $b] ? $a : $b}]
}
mayorCon 3 7 {{x y} {expr {$x > $y}}}
```

Es el mismo mecanismo que el parámetro `with function "<"` del genérico de Ada, resuelto en ejecución
en lugar de al compilar. Y es exactamente lo que hace `lsort -command` de la biblioteca estándar,
que ordena con el criterio que le des.
"""),
        "perl": ("""
use strict;
use warnings;

sub mayor {
    my ($x, $y) = @_;
    return $x > $y ? $x : $y;
}

my $linea = <STDIN>;
chomp $linea;
my ($p, $q) = split ' ', $linea;

print "max=", mayor($p, $q), "\\n";
""", """
**Lo que esta clase enseña en Perl.** Como en Tcl, sin tipos no hay genéricos: la función acepta lo
que sea. Y como en Tcl, la trampa es que **hay que elegir el operador según cómo quieras comparar**
—la tabla de la clase 051—:

```perl
sub mayor_num { $_[0] > $_[1] ? $_[0] : $_[1] }     # numérico
sub mayor_txt { $_[0] gt $_[1] ? $_[0] : $_[1] }    # alfabético
```

Escribir una sola función que sirva para los dos exige **pasar el comparador**, que es el mismo patrón
de Ada y Tcl:

```perl
sub mayor_con {
    my ($cmp, $x, $y) = @_;
    return $cmp->($x, $y) > 0 ? $x : $y;
}
mayor_con(sub { $_[0] <=> $_[1] }, 3, 7);      # numérico
mayor_con(sub { $_[0] cmp $_[1] }, 'a', 'b');  # textual
```

`<=>` y `cmp` son los **operadores de comparación de tres vías** de la clase 055, y son exactamente lo
que `sort` espera:

```perl
sort { $a <=> $b } @numeros;
sort { $a->{edad} <=> $b->{edad} } @personas;
```

Y Perl tiene una forma de polimorfismo que sí se parece a los genéricos: **la sobrecarga de
operadores** con el pragma `overload`, que permite que una clase propia responda a `<`, `+` o `""`.
Con ella, una función escrita para números funciona con tu tipo sin cambiarla — que es la definición
operativa del polimorfismo paramétrico en un lenguaje dinámico.
"""),
        "cpp": ("""
#include <iostream>

template <typename T>
T mayor(const T& a, const T& b) {
    return (a < b) ? b : a;
}

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::cout << "max=" << mayor(a, b) << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** `template <typename T>` genera **una función distinta por cada
tipo con el que se use**, en tiempo de compilación. Eso se llama **monomorfización**, y es la razón de
las tres características de C++ en este terreno:

1. **Sin coste en ejecución**: no hay conversiones, no hay indirección, el cuerpo se integra en línea.
2. **Binarios grandes y compilación lenta**: cada instanciación es código nuevo.
3. **Errores descomunales**: si el tipo no tiene `<`, el error aparece **dentro** de la plantilla.

C++20 resolvió el tercero con los **conceptos**, que son literalmente lo que Ada tenía en 1983:

```cpp
template <typename T>
concept Comparable = requires(T a, T b) { { a < b } -> std::convertible_to<bool>; };

template <Comparable T>
T mayor(const T& a, const T& b) { return (a < b) ? b : a; }
```

Ahora el error dice "`T` no satisface `Comparable`" en el sitio de la llamada, que es lo correcto.

Y la comparación con **Java** es la que da la lección de esta clase: Java **borra los tipos**. Hay una
sola versión del código, `List<String>` y `List<Integer>` son la misma clase en ejecución, y por eso
no puedes hacer `new T[]` ni `instanceof List<String>`. A cambio, el binario es pequeño y la
compilación rápida.

C++, Ada, Rust y C# (para tipos de valor) monomorfizan; Java y C# (para referencias) borran. **Ninguna
es mejor**, y saber cuál usa tu lenguaje explica muchas de sus limitaciones aparentemente
arbitrarias.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi MAXIMO;
  a int(10) const;
  b int(10) const;
end-pi;

dcl-s mayorV like(a);       // LIKE: el tipo se hereda, no se repite
dcl-s salida char(30);

if a > b;
  mayorV = a;
else;
  mayorV = b;
endif;

salida = 'max=' + %char(mayorV);
dsply salida;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** **RPG no tiene genéricos.** No hay parámetros de tipo, no hay
plantillas y no se puede escribir una función que sirva para `packed` y para `char`.

Lo que tiene, y cubre una parte del problema, son las **plantillas de datos** de la clase 052:

```rpgle
dcl-s tipoImporte packed(11:2) template;    // TEMPLATE: no ocupa memoria
dcl-s total  like(tipoImporte);
dcl-s parcial like(tipoImporte);

dcl-ds tipoCliente qualified template;
  codigo char(8);
  nombre char(40);
end-ds;
dcl-ds cliente likeds(tipoCliente);
```

`template` declara un molde y `like`/`likeds` lo copian. Eso resuelve la **duplicación de
declaraciones** —si cambia el tipo, cambia en un sitio— pero **no la duplicación de código**: sigue
haciendo falta una función por tipo.

Y hay dos mecanismos de bajo nivel que dan algo parecido a la genericidad, con las garantías de C:

```rpgle
dcl-pi *n;
  datos pointer;                       // un puntero a lo que sea
  tam   int(10) const;
end-pi;
...
dcl-s buffer char(65535) based(datos); // interpretar esos bytes como caracteres
```

`based(puntero)` es la variable `based` de PL/I de la clase 053: un nombre que mira donde apunte un
puntero. Con él se escriben rutinas que operan sobre "cualquier cosa", sin ninguna comprobación de
tipos. Se usa para hablar con las APIs del sistema, y en código de negocio se evita.
"""),
        "pli": ("""
 maximo: procedure options(main);

    declare (a, b) fixed binary(31);

    get list (a, b);

    put skip list ('max=' || trim(char(max(a, b))));

 end maximo;
""", """
**Lo que esta clase enseña en PL/I.** PL/I **no tiene genéricos con parámetros de tipo**, pero tiene
el atributo **`generic`**, que ya apareció en la clase 074 y que aquí es central: **selecciona entre
varios procedimientos según los tipos de los argumentos**.

```pli
declare mayor generic (
   mayor_bin  when (fixed binary, fixed binary),
   mayor_dec  when (fixed decimal, fixed decimal),
   mayor_char when (character, character)
);

x = mayor(1, 2);          /* llama a mayor_bin */
y = mayor('a', 'b');      /* llama a mayor_char */
```

Es exactamente la **interfaz genérica de Fortran** con otra sintaxis: sobrecarga declarada en una
tabla explícita. Y comparte su limitación: **hay que escribir cada versión**.

La ventaja frente a la sobrecarga implícita de C++ es que **la tabla se lee**. Para saber a qué se
llama, se mira la declaración `generic`, en lugar de reconstruir el algoritmo de resolución del
compilador.

Y PL/I tiene, en su lugar, algo que sí es genuinamente genérico y que ningún lenguaje del núcleo
ofrece: **la aritmética funciona sobre cualquier combinación de base y escala**. Una rutina escrita
para `fixed decimal(15,2)` acepta un `fixed binary(31)` porque el lenguaje convierte. Es
polimorfismo por conversión implícita — cómodo, y con todos los problemas de la clase 050.

Es una constante de esta sección: **PL/I resuelve muchos problemas por conversión donde los lenguajes
posteriores los resuelven por tipos**.
"""),
        "smalltalk": ("""
| partes a b |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

Transcript show: 'max=', (a max: b) printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** `max:` está implementado **una sola vez**, en la clase
abstracta `Magnitude`, y funciona con todo lo que sepa compararse:

```smalltalk
Magnitude >> max: unaMagnitud
    ^self > unaMagnitud ifTrue: [ self ] ifFalse: [ unaMagnitud ]
```

`Number`, `Character`, `Date`, `Time`, `String` y `Duration` heredan de `Magnitude`. Basta con
implementar **`<`** en una clase nueva para heredar `max:`, `min:`, `between:and:`, `>`, `<=` y `>=`,
todos definidos en términos de `<`.

Eso es polimorfismo **por herencia de interfaz**, y es la respuesta de Smalltalk a esta clase: no hay
parámetros de tipo porque no hay tipos, y la reutilización viene de la jerarquía.

Y es exactamente el mismo diseño que `Comparable` de Java, `Ord` de Haskell y `PartialOrd` de Rust:
**una operación primitiva, y el resto derivado**. Smalltalk lo hizo en los 70 y sin necesidad de
declarar la interfaz — basta con responder al mensaje.

La contrapartida, honesta: **no hay comprobación estática**. Si pasas a `max:` un objeto que no
entiende `<`, el error aparece **cuando se ejecuta esa línea**, no al compilar. Es el mismo
compromiso de toda la sección sobre Smalltalk, y es la razón de que estos proyectos se apoyen tanto en
pruebas — y de que SUnit naciera aquí.

Existen investigaciones de tipado estático para Smalltalk —Strongtalk, y hoy los *type hints* de
Pharo— pero nunca entraron en el lenguaje.
"""),
    },
)
