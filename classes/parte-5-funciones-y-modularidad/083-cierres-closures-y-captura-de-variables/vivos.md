# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 083

> [⬅️ Volver a la clase 083](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Dos funciones que recuerdan un valor que ya no está en ningún parámetro. Eso es una **clausura**: una
función más el trozo de entorno que capturó al nacer. Es la base de la programación funcional
moderna, de los manejadores de eventos y de medio JavaScript — y de estos doce lenguajes, **solo
cuatro la tienen completa**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **captura del entorno**, y estos lenguajes lo enseñan porque muestran los tres
> niveles. **Clausura completa**: Lisp y Smalltalk, donde la función es un valor que se puede guardar,
> devolver y llamar mucho después, con su entorno vivo. **Anidamiento léxico sin primera clase**:
> Fortran, Ada, Pascal y PL/I, donde un procedimiento interno **ve** las variables del que lo contiene
> pero **no se puede devolver**. Y **nada**: COBOL, RPG y M.
>
> La diferencia entre los dos primeros niveles es exactamente **el problema del funarg ascendente**: si
> la función sobrevive al procedimiento que la creó, ¿dónde viven sus variables capturadas? La respuesta
> —en el montículo, no en la pila— es lo que separa una clausura de un procedimiento anidado.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `base` → stdout: `r1=<base+1> r2=<base+2>`
- **Regla:** `sumar = λx. base + x ; r1 = sumar(1) ; r2 = sumar(2)`

| stdin | esperado |
|---|---|
| `10` | `r1=11 r2=12` |
| `0` | `r1=1 r2=2` |
| `100` | `r1=101 r2=102` |

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
```

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

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
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
```

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

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
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
```

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

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
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
```

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

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((base (read))
       (f1 (lambda () (+ base 1)))     ; CAPTURA base
       (f2 (lambda () (+ base 2))))
  (format t "r1=~D r2=~D~%" (funcall f1) (funcall f2)))
```

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

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set base [string trim $linea]

#  Tcl no tiene clausuras: los valores se "hornean" en un prefijo de comando.
set f1 [list apply {{b} {expr {$b + 1}}} $base]
set f2 [list apply {{b} {expr {$b + 2}}} $base]

puts "r1=[{*}$f1] r2=[{*}$f2]"
```

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

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $base = <STDIN>;
chomp $base;

my $f1 = sub { return $base + 1 };    # CAPTURA $base
my $f2 = sub { return $base + 2 };

print "r1=", $f1->(), " r2=", $f2->(), "\n";
```

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

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    int base{};
    if (!(std::cin >> base)) return 1;

    auto f1 = [base]() { return base + 1; };   // captura POR VALOR
    auto f2 = [base]() { return base + 2; };

    std::cout << "r1=" << f1() << " r2=" << f2() << '\n';
    return 0;
}
```

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
```

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

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
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
```

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

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
CLAUSURA ; Cierres -- clase 083
 read base
 write "r1=", $$sumar(1), " r2=", $$sumar(2), !
 quit
 ;
sumar(k) ; suma k a la variable `base` del llamante (ambito DINAMICO)
 quit base + k
```

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

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| base f1 f2 |

base := stdin nextLine trimBoth asNumber.

f1 := [ base + 1 ].      "un BLOQUE: captura base"
f2 := [ base + 2 ].

Transcript
    show: 'r1=', f1 value printString;
    show: ' r2=', f2 value printString;
    cr.
```

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

---

## Y de vuelta a la clase

Lo transferible: **una clausura es un objeto con un método, y un objeto es una clausura con varios
métodos**. Son la misma idea vista desde dos lados, y por eso los lenguajes que tienen clausuras de
primera clase pueden construir objetos con ellas —y Smalltalk, que tiene objetos, construye sus
estructuras de control con bloques—. Cuando un lenguaje no tiene ninguna de las dos, como COBOL o
RPG, el sustituto es siempre el mismo: una **variable global más una convención**.

⏮️ [Volver a la clase 083](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
