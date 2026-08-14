# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 073

> [⬅️ Volver a la clase 073](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Una función que suma dos enteros. El programa más simple de la Parte 5, elegido porque obliga a
responder la pregunta fundacional: **¿qué es exactamente una función en este lenguaje?** Y la
respuesta más sorprendente de esta página es la de COBOL, donde la unidad de código reutilizable
—el párrafo— **no tiene parámetros ni valor de retorno**: todo son variables globales.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **firma como contrato**, y estos lenguajes lo enseñan porque muestran los tres
> niveles históricos. El primero: **COBOL con `PERFORM`**, que ejecuta un bloque de código sin
> argumentos ni retorno — literalmente un `goto` con vuelta. El segundo: **el subprograma con
> parámetros**, que es lo que trajeron FORTRAN II, ALGOL y todos los demás. Y el tercero: **el modo de
> cada parámetro declarado en la firma** —`intent(in)` de Fortran, `in`/`out`/`in out` de Ada— que dice
> no solo qué recibe una función, sino **qué va a hacer con ello**.
>
> Ese tercer nivel es el que casi ningún lenguaje del núcleo tiene, y el que hace legible una firma sin
> leer el cuerpo.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea `a b` (dos enteros) → stdout: `suma=<a+b>`
- **Regla:** `suma(a, b) = a + b`

| stdin | esperado |
|---|---|
| `3 4` | `suma=7` |
| `10 20` | `suma=30` |
| `-5 5` | `suma=0` |

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
```

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

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
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
```

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

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
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
```

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

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
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
```

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

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(defun suma (x y)
  "Devuelve la suma de X e Y."
  (+ x y))

(let* ((a (read))
       (b (read)))
  (format t "suma=~D~%" (suma a b)))
```

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

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
proc suma {x y} {
    return [expr {$x + $y}]
}

gets stdin linea
lassign [split [string trim $linea]] a b

puts "suma=[suma $a $b]"
```

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

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

sub suma {
    my ($x, $y) = @_;
    return $x + $y;
}

my $linea = <STDIN>;
chomp $linea;
my ($p, $q) = split ' ', $linea;

print "suma=", suma($p, $q), "\n";
```

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

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int suma(int x, int y) {
    return x + y;
}

int main() {
    int a{}, b{};
    if (!(std::cin >> a >> b)) return 1;

    std::cout << "suma=" << suma(a, b) << '\n';
    return 0;
}
```

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
```

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

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 sumar: procedure options(main);

    declare (a, b) fixed binary(31);

    get list (a, b);
    put skip list ('suma=' || trim(char(suma(a, b))));

 suma: procedure (x, y) returns (fixed binary(31));
    declare (x, y) fixed binary(31);
    return (x + y);
 end suma;

 end sumar;
```

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

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
SUMAR ; Firma y retorno -- clase 073
 read linea
 set a = $piece(linea, " ", 1)
 set b = $piece(linea, " ", 2)
 write "suma=", $$suma(a, b), !
 quit
 ;
suma(x, y) ; devuelve x + y
 quit x + y
```

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

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| partes a b |

partes := stdin nextLine substrings collect: [ :cada | cada asNumber ].
a := partes first.
b := partes second.

Transcript show: 'suma=', (a + b) printString; cr.
```

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

---

## Y de vuelta a la clase

Lo transferible: **una firma dice cuatro cosas, y muchos lenguajes solo escriben dos**. El nombre y
los tipos casi todos; **la dirección de cada parámetro** solo Fortran, Ada, Pascal y PL/I; y **qué
efectos tiene la función** solo Fortran (`pure`), Ada (`Global => null`) y C++ (`const`, `noexcept`,
`[[nodiscard]]`). Cuanto más dice la firma, menos hay que leer el cuerpo — y eso es exactamente el
valor de una función como unidad de abstracción.

⏮️ [Volver a la clase 073](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
