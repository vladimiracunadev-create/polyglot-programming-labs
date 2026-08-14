# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 079

> [⬅️ Volver a la clase 079](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Una función que dobla lo que recibe, y una variable del llamante que **no cambia**. Eso es el paso
por valor, y parece la opción evidente hasta que se descubre que **la mitad de estos lenguajes hacen
lo contrario por defecto**: en Fortran, PL/I, RPG y COBOL el paso es **por referencia** salvo que se
diga otra cosa, y esa decisión de los años 50 tiene consecuencias que todavía muerden.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **qué recibe realmente una función**, y estos lenguajes lo enseñan porque
> representan la época en que **copiar era caro**. En una máquina de 1957, pasar una copia de un array
> de mil elementos era impensable, así que se pasaba la dirección. Por eso Fortran, COBOL, PL/I y RPG
> son por referencia por defecto.
>
> Y de ahí sale la trampa histórica más famosa de la informática: en el FORTRAN antiguo se podía pasar
> la constante `2` a una subrutina, la subrutina la modificaba, y **a partir de ese momento el literal
> `2` valía otra cosa en todo el programa**. No es una leyenda: era el comportamiento real de varios
> compiladores.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` → stdout: `original=<n> local=<2n>`
- **Regla:** `la función duplica una copia; el original permanece`

| stdin | esperado |
|---|---|
| `5` | `original=5 local=10` |
| `3` | `original=3 local=6` |
| `0` | `original=0 local=0` |

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
```

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

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
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
```

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

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
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
```

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

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
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
```

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

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(defun doblar (x)
  (* x 2))

(let ((n (read)))
  (format t "original=~D local=~D~%" n (doblar n)))
```

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

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
proc doblar {x} {
    set x [expr {$x * 2}]      ;# x es una COPIA local
    return $x
}

gets stdin linea
set n [string trim $linea]

puts "original=$n local=[doblar $n]"
```

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

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

sub doblar {
    my ($x) = @_;              # la COPIA: sin esta línea, @_ sería un alias
    $x = $x * 2;
    return $x;
}

my $n = <STDIN>;
chomp $n;

print "original=$n local=", doblar($n), "\n";
```

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

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int doblar(int x) {       // por VALOR: x es una copia
    x *= 2;
    return x;
}

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "original=" << n << " local=" << doblar(n) << '\n';
    return 0;
}
```

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
```

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

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
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
```

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

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
PORVALOR ; Paso por valor -- clase 079
 read n
 write "original=", n, " local=", $$doblar(n), !
 quit
 ;
doblar(x) ; devuelve el doble; x es una COPIA
 set x = x * 2
 quit x
```

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

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n |

n := stdin nextLine trimBoth asNumber.

Transcript
    show: 'original=', n printString;
    show: ' local=', (n * 2) printString;
    cr.
```

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

---

## Y de vuelta a la clase

Lo transferible: **el defecto de tu lenguaje no es neutral, es una decisión histórica**. Los
lenguajes nacidos cuando la memoria era cara pasan por referencia; los nacidos después pasan por
valor. Y en los modernos con objetos, la respuesta correcta es la tercera: **se pasa por valor una
referencia**, así que reasignar el parámetro no afecta al llamante pero **mutar el objeto sí**. Esa
distinción —valor frente a referencia frente a "valor de una referencia"— explica casi todas las
sorpresas al cambiar de lenguaje.

⏮️ [Volver a la clase 079](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
