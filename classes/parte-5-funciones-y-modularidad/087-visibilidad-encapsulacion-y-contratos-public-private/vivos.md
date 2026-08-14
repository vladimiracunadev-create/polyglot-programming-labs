# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 087

> [⬅️ Volver a la clase 087](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Un saldo que solo se puede cambiar depositando. La encapsulación en su forma mínima: **un dato que
nadie de fuera puede tocar directamente**. Y aquí hay dos posturas radicalmente distintas: **Ada tiene
una "parte privada" en la especificación** —visible para leer, inaccesible para usar— y **Smalltalk
hace todos los campos privados y todos los métodos públicos, sin excepción y sin palabras clave**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **ocultación de información**, formulada por David Parnas en 1972, y estos
> lenguajes la implementan de formas muy distintas. **Ada** separa la especificación en parte pública y
> **parte privada**, que el cliente puede leer pero no usar — una idea que ningún lenguaje del núcleo
> copió y que resuelve el problema de que el compilador necesita saber el tamaño de un tipo aunque el
> programador no deba conocerlo.
>
> **Fortran** lo hace con `private` a nivel de módulo, **RPG** con `export`, y **COBOL, PL/I y M** no
> tienen nada: la encapsulación es convención.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (monto de cada depósito) → stdout: `saldo=<2n>` (tras depositar n dos veces)
- **Regla:** `cuenta.depositar(n) dos veces; saldo = 2n`

| stdin | esperado |
|---|---|
| `50` | `saldo=100` |
| `0` | `saldo=0` |
| `30` | `saldo=60` |

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
PROGRAM-ID. ENCAPSULA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9)  COMP-3.
01  SALDO   PIC S9(18) COMP-3 VALUE 0.
01  IMPORTE PIC S9(9)  COMP-3.
01  ED-S    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N

    MOVE N TO IMPORTE
    PERFORM DEPOSITAR
    PERFORM DEPOSITAR

    MOVE SALDO TO ED-S
    DISPLAY "saldo=" FUNCTION TRIM(ED-S)
    STOP RUN.

DEPOSITAR.
    COMPUTE SALDO = SALDO + IMPORTE.
```

**Lo que esta clase enseña en COBOL.** **En COBOL no hay encapsulación posible dentro de un
programa**: `SALDO` es global y cualquier párrafo puede escribirlo. La disciplina de "solo se toca
desde `DEPOSITAR`" es una convención que nada comprueba.

Donde COBOL sí tiene ocultación de verdad es **entre programas**, y de la forma más fuerte posible:
**el `WORKING-STORAGE` de un programa es completamente inaccesible desde otro**. No hay forma de leer
las variables de un programa llamado; solo lo que viaje por `USING` y `RETURNING`.

Eso es encapsulación total por unidad de compilación, y es la razón de que la arquitectura típica de
un sistema COBOL sea **muchos programas pequeños** en lugar de uno grande: **el programa es la unidad
de encapsulación**.

Y los **programas anidados** de COBOL-85 (clase 082) dan un nivel intermedio:

```cobol
    IDENTIFICATION DIVISION.
    PROGRAM-ID. CUENTA IS COMMON.
    DATA DIVISION.
    WORKING-STORAGE SECTION.
    01  SALDO  PIC S9(18) COMP-3 VALUE 0.    *> PRIVADO
    ...
```

`SALDO` no es visible para el programa padre, y `CUENTA` sí lo es para sus hermanos anidados. Es un
objeto con estado privado y métodos públicos, escrito en COBOL de 1985.

Y en el padre, la palabra clave `GLOBAL` en una declaración la hace visible para los anidados:
`01 CONFIG PIC X(40) GLOBAL.` — encapsulación con excepciones declaradas, que es exactamente lo que
hace `protected` en un lenguaje de objetos.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
module cuenta
   implicit none
   private                          ! todo privado por defecto
   public :: depositar, saldo_actual

   integer :: saldo = 0             ! PRIVADO: invisible desde fuera del módulo

contains

   subroutine depositar(x)
      integer, intent(in) :: x
      saldo = saldo + x
   end subroutine depositar

   function saldo_actual() result(s)
      integer :: s
      s = saldo
   end function saldo_actual

end module cuenta


program encapsula
   use cuenta
   implicit none
   integer :: n

   read(*, *) n
   call depositar(n)
   call depositar(n)

   write(*, '(A,I0)') 'saldo=', saldo_actual()
end program encapsula
```

**Lo que esta clase enseña en Fortran.** La línea **`private`** suelta al principio del módulo
**invierte el defecto**: todo es privado salvo lo que se declare `public`. Es la política que hoy
recomiendan todas las guías y que Rust adoptó como norma del lenguaje.

Y es un cambio enorme respecto al Fortran clásico, donde los bloques `COMMON` eran **memoria
compartida sin ninguna protección**: cualquier subrutina que declarara el mismo `COMMON` podía leer y
escribir esas variables.

```fortran
      COMMON /CUENTA/ SALDO      ! cualquiera que escriba esto ve SALDO
```

El módulo con `private` es la respuesta directa a ese problema, y es la razón principal de que la
migración a módulos sea la recomendación número uno para modernizar código Fortran.

Fortran 2003 añadió además el **`protected`**, que no tiene equivalente en el núcleo:

```fortran
integer, public, protected :: version = 3
```

`protected` significa **público para leer, privado para escribir**. Desde fuera del módulo se puede
consultar `version` pero no asignarla. Es exactamente un `readonly` público, y evita el par
`private` + función de acceso que en otros lenguajes hay que escribir a mano.

Y a nivel de tipos derivados, los componentes también pueden ser `private`:

```fortran
type :: Cuenta
   private
   integer :: saldo = 0        ! invisible incluso teniendo el objeto
end type
```

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Encapsula is

   package Cuenta is
      procedure Depositar (X : Integer);
      function Saldo return Integer;
   private
      --  PARTE PRIVADA: el cliente la ve al leer, pero NO puede usarla.
      Total : Integer := 0;
   end Cuenta;

   package body Cuenta is
      procedure Depositar (X : Integer) is
      begin
         Total := Total + X;
      end Depositar;

      function Saldo return Integer is (Total);
   end Cuenta;

   N : Integer;
begin
   Get (N);
   Cuenta.Depositar (N);
   Cuenta.Depositar (N);

   Put ("saldo=");
   Put (Cuenta.Saldo, Width => 1);
   New_Line;
end Encapsula;
```

**Lo que esta clase enseña en Ada.** La **parte privada de una especificación** es una idea de Ada que
casi nadie copió y que resuelve un problema real de diseño de lenguajes.

El problema es este: para declarar una variable de un tipo, **el compilador necesita saber cuánto
ocupa**. Pero el programador **no debería** conocer su estructura interna. Las dos cosas parecen
incompatibles.

La solución de Ada es partir la especificación en dos:

```ada
package Cuentas is
   type Cuenta is private;                    --  el cliente sabe que existe...
   procedure Depositar (C : in out Cuenta; X : Integer);
   function Saldo (C : Cuenta) return Integer;
private
   type Cuenta is record                       --  ...y NO puede usar esto
      Total : Integer := 0;
      Historial : ...;
   end record;
end Cuentas;
```

El cliente **compila** contra la parte privada —así el compilador conoce el tamaño— pero **el lenguaje
le prohíbe acceder a sus campos**. Si escribe `C.Total`, no compila.

C++ resuelve lo mismo poniendo los campos privados en la clase, con el mismo efecto: están en la
cabecera, se ven al leer, no se pueden usar. La diferencia es que Ada **lo dice explícitamente con una
sección llamada `private`**, mientras que en C++ hay que entender por qué los campos privados están en
el `.h`.

Y la alternativa —ocultarlos de verdad— es el modismo *pimpl* en C++ y los **tipos incompletos**
(`limited private`) en Ada, a costa de una indirección.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Encapsula;
{$MODE OBJFPC}{$H+}
uses SysUtils;

type
  TCuenta = class
  private
    FSaldo: Integer;          { PRIVADO }
  public
    procedure Depositar(X: Integer);
    property Saldo: Integer read FSaldo;    { solo lectura desde fuera }
  end;

procedure TCuenta.Depositar(X: Integer);
begin
  FSaldo := FSaldo + X;
end;

var
  N: Integer;
  C: TCuenta;

begin
  Read(N);
  C := TCuenta.Create;
  try
    C.Depositar(N);
    C.Depositar(N);
    WriteLn('saldo=', IntToStr(C.Saldo));
  finally
    C.Free;
  end;
end.
```

**Lo que esta clase enseña en Pascal.** Object Pascal tiene **cinco niveles de visibilidad**, más que
casi cualquier lenguaje de esta página:

| Nivel | Quién accede |
|---|---|
| `strict private` | **Solo** la propia clase |
| `private` | La clase **y cualquier código de la misma unidad** |
| `protected` | La clase y sus descendientes |
| `public` | Todos |
| `published` | Como `public`, **y además genera RTTI** para el inspector |

Las dos peculiares son la segunda y la quinta. **`private` en Delphi NO es estrictamente privado**:
cualquier código del mismo fichero puede acceder. Es una decisión pragmática —permite que clases
relacionadas cooperen— y sorprende a quien viene de Java. Por eso Delphi 2005 añadió `strict private`.

**`published`** no existe en ningún otro lenguaje: marca los miembros que el **inspector de objetos**
del IDE puede ver y editar, y que se guardan en el fichero `.dfm` del formulario. Es visibilidad al
servicio de la herramienta, y es lo que hace posible el diseño visual de la clase 073.

Y `property Saldo: Integer read FSaldo;` sin `write` es una **propiedad de solo lectura**: desde fuera
se lee como un campo y no se puede asignar. Es el `protected` de Fortran con otra sintaxis, y el
mecanismo que .NET copió literalmente.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((n (read))
       (saldo 0)
       (depositar (lambda (x) (incf saldo x))))
  (funcall depositar n)
  (funcall depositar n)
  (format t "saldo=~D~%" saldo))
```

**Lo que esta clase enseña en Common Lisp.** Lisp tiene **dos formas de encapsular**, y son muy
distintas.

La primera es la de este programa: **la clausura** de la clase 083. `saldo` es una variable léxica que
**solo la lambda puede tocar**. Es privacidad real —no hay forma de acceder a `saldo` desde fuera— y
no necesita ninguna palabra clave.

```lisp
(defun crear-cuenta ()
  (let ((saldo 0))
    (list :depositar (lambda (x) (incf saldo x))
          :saldo     (lambda () saldo))))
```

Eso es un objeto con estado **verdaderamente privado**, más privado que cualquier campo de CLOS.

La segunda es la de los **paquetes** (clase 086): exportar o no exportar un símbolo. Y ahí Lisp toma
una postura característica: **`utiles::interno` con dos puntos accede a cualquier símbolo no
exportado**. No hay barrera técnica.

Esa decisión es deliberada y refleja una filosofía: **la privacidad es una indicación de diseño, no
una cerradura**. El autor dice "esto es interno"; quien lo use asume el riesgo de que cambie. Es la
misma postura que Python con el guion bajo, y la contraria a Java y C++.

En CLOS, los campos (*slots*) **no tienen niveles de visibilidad**: se controla el acceso decidiendo
qué accesores se generan y cuáles se exportan.

```lisp
(defclass cuenta ()
  ((saldo :initform 0 :reader saldo)))    ; solo LECTOR, no escritor
```

Sin `:accessor` ni `:writer`, no hay forma pública de asignar — el mismo `protected` de Fortran, otra
vez.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
namespace eval ::cuenta {
    variable saldo 0                  ;# no se exporta: "privado" por convención
    namespace export depositar saldo_actual

    proc depositar {x} {
        variable saldo
        set saldo [expr {$saldo + $x}]
    }

    proc saldo_actual {} {
        variable saldo
        return $saldo
    }
}

gets stdin linea
set n [string trim $linea]

::cuenta::depositar $n
::cuenta::depositar $n

puts "saldo=[::cuenta::saldo_actual]"
```

**Lo que esta clase enseña en Tcl.** Los espacios de nombres de Tcl **no tienen privacidad real**:
`namespace export` decide qué se puede importar con `namespace import`, pero **cualquiera puede
escribir `::cuenta::saldo` y acceder directamente**.

Es la misma postura que Lisp con `::` y Python con el guion bajo: **una indicación, no una cerradura**.

Donde Tcl sí tiene encapsulación de verdad es en **TclOO**, el sistema de objetos que entró en el
núcleo con Tcl 8.6:

```tcl
oo::class create Cuenta {
    variable saldo                     ;# variable de INSTANCIA, privada
    constructor {} { set saldo 0 }
    method depositar {x} { incr saldo $x }
    method saldo {} { return $saldo }
}

set c [Cuenta new]
$c depositar 50
```

Las variables declaradas con `variable` dentro de una clase TclOO son **de instancia y privadas**: no
hay sintaxis para acceder a ellas desde fuera del objeto.

Y TclOO tiene un rasgo poco común: **las clases se pueden modificar en ejecución**, añadiendo métodos
y cambiando la jerarquía sobre objetos que ya existen. Es el modelo de Smalltalk, y viene del mismo
sitio — el diseño de TclOO se inspiró explícitamente en él y en el sistema de metaobjetos de CLOS.

Además tiene `oo::mixin` y filtros de método, que permiten componer comportamiento sin herencia, y
`unexport` para retirar un método de la interfaz pública.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

{
    package Cuenta;

    my $saldo = 0;                     # léxica del bloque: VERDADERAMENTE privada

    sub depositar { $saldo += $_[0] }
    sub saldo     { return $saldo }
}

my $n = <STDIN>;
chomp $n;

Cuenta::depositar($n);
Cuenta::depositar($n);

print "saldo=", Cuenta::saldo(), "\n";
```

**Lo que esta clase enseña en Perl.** Perl tiene **dos niveles de privacidad muy distintos**, y este
programa usa el fuerte.

**El débil** es la convención: una subrutina o variable de paquete cuyo nombre empieza por guion bajo
—`_ayudante`— se considera privada, y **nada lo impide**. `Cuenta::_ayudante()` funciona.

**El fuerte** es el de este programa: una variable **léxica** (`my`) declarada en el ámbito del
fichero o de un bloque. `$saldo` **no está en la tabla de símbolos**, así que **no hay ninguna forma
de acceder a ella desde fuera**, ni siquiera con manipulación de *globs*.

```perl
my $secreto = 42;              # invisible desde cualquier otro sitio
our $publico = 42;             # accesible como $Cuenta::publico
```

Esa privacidad es más fuerte que la de Java —donde la reflexión rompe `private`— y es la razón de que
el patrón de la clase 083, los objetos hechos con clausuras, se use en Perl cuando los datos deben ser
realmente inaccesibles.

Para los objetos normales, Perl usa `bless` sobre un hash, y **todos sus campos son accesibles**:
`$obj->{saldo}` funciona desde cualquier sitio. Es la crítica clásica al modelo de objetos de Perl 5.

Las alternativas de CPAN lo resuelven: **`Moose`** y **`Moo`** dan atributos con `is => 'ro'`,
constructores y validación; y los **campos de instancia** de la nueva palabra clave `class`
(experimental desde 5.38) son léxicos y por tanto privados de verdad.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

class Cuenta {
    int saldo_ = 0;                 // PRIVADO por defecto en una class
public:
    void depositar(int x) { saldo_ += x; }
    int saldo() const { return saldo_; }
};

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    Cuenta c;
    c.depositar(n);
    c.depositar(n);

    std::cout << "saldo=" << c.saldo() << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** La única diferencia entre `class` y `struct` en C++ es el
**defecto**: `class` empieza en `private`, `struct` en `public`. Todo lo demás es idéntico — una
`struct` puede tener métodos, herencia y constructores.

Y hay tres niveles —`private`, `protected`, `public`— más el mecanismo que más discusión ha generado:
**`friend`**.

```cpp
class Cuenta {
    int saldo_ = 0;
    friend class Auditor;                       // Auditor ve mis privados
    friend std::ostream& operator<<(std::ostream&, const Cuenta&);
};
```

`friend` **rompe la encapsulación de forma declarada**: la clase decide quién puede mirar dentro. Se
critica como un agujero, y su defensa es sólida: es la propia clase quien concede el permiso, así que
la lista de quién ve sus privados **está escrita en la clase**. Es más honesto que hacer todo público.

El caso canónico es el `operator<<` de la primera línea: una función libre que necesita acceder a los
campos para imprimirlos, y que no puede ser un método porque el receptor es el flujo.

Fíjate también en `int saldo() const`: el **`const` al final** promete que el método no modifica el
objeto, y el compilador lo comprueba. Es la mitad de la pureza de la clase 084, aplicada a los
métodos, y no tiene equivalente en Java ni en Python.

Y el subrayado final en `saldo_` es una convención muy extendida para distinguir el campo del método
que lo devuelve.

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

dcl-s saldo int(20) static;      // global del MÓDULO: sin export, es privada

dcl-proc Principal;
  dcl-pi *n;
    n int(10) const;
  end-pi;

  dcl-s salida char(40);

  depositar(n);
  depositar(n);

  salida = 'saldo=' + %char(saldoActual());
  dsply salida;
end-proc;

dcl-proc depositar export;       // EXPORT: parte de la interfaz del módulo
  dcl-pi *n;
    x int(10) const;
  end-pi;
  saldo += x;
end-proc;

dcl-proc saldoActual export;
  dcl-pi *n int(20); end-pi;
  return saldo;
end-proc;
```

**Lo que esta clase enseña en RPG.** La palabra **`export`** en un `dcl-proc` es todo el mecanismo de
visibilidad de RPG, y tiene la polaridad correcta: **sin ella, el procedimiento es privado del
módulo**.

```rpgle
dcl-proc publico export;   // visible desde otros módulos
dcl-proc privado;          // solo desde este módulo
```

Es el `static` de C invertido: en C hay que escribir `static` para **ocultar**; en RPG hay que
escribir `export` para **mostrar**. La segunda opción es mejor, y es la que eligieron después Rust,
los módulos de C++20 y Java con los paquetes.

Y las **variables globales del módulo** —como `saldo` en este programa— son **siempre privadas**: no
hay forma de exportar una variable en RPG. Solo se exportan procedimientos.

Eso fuerza el patrón que se vio en la clase 083: **un módulo con estado privado y procedimientos de
acceso** es, exactamente, un objeto con un solo ejemplar. Y es la arquitectura recomendada de la
plataforma para el código reutilizable.

Hay además una advertencia de seguridad propia de IBM i que conviene conocer: si el módulo se enlaza
en un **programa de servicio** con activación compartida, **el estado `static` se comparte entre
trabajos**. Un dato de un usuario puede quedar visible para otro. Por eso la guía es que los módulos
de servicio sean **sin estado**, y que el estado viva en el programa que los usa.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 encapsula: procedure options(main);

    declare n     fixed binary(31);
    declare saldo fixed binary(31) static initial(0);   /* "privado" del bloque */

    get list (n);

    call depositar(n);
    call depositar(n);

    put skip list ('saldo=' || trim(char(saldo)));

 depositar: procedure (x);
    declare x fixed binary(31);
    saldo = saldo + x;        /* ve `saldo` por anidamiento léxico */
 end depositar;

 end encapsula;
```

**Lo que esta clase enseña en PL/I.** **PL/I no tiene ninguna palabra clave de visibilidad**: no hay
`private`, `public` ni `export`. Lo único que controla el acceso es el **anidamiento léxico** de la
clase 083.

Una variable declarada en un procedimiento **es invisible desde fuera** y visible para todo lo anidado
dentro. Con eso se construye encapsulación:

```pli
 modulo: procedure external;
    declare estado fixed binary(31) static;    /* privado: nadie de fuera lo ve */

    publico: procedure external;                /* pero ESTE sí es visible */
       ...
    end publico;
 end modulo;
```

El `external` en un procedimiento interno lo hace visible al enlazador, así que la combinación
—estado en el ámbito exterior, procedimientos `external` anidados dentro— da un módulo con estado
privado.

Es exactamente el patrón que en JavaScript se llamó **expresión de función inmediatamente invocada**
(*IIFE*) y que durante quince años fue la única forma de tener privacidad en ese lenguaje. En PL/I
funciona desde 1964.

Lo que falta es lo que Ada añadió: **una declaración explícita de qué es interfaz y qué es
implementación**, comprobada por el compilador y legible por el cliente. En PL/I hay que deducirlo del
anidamiento, y en un procedimiento de dos mil líneas eso no es trivial.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
ENCAPSULA ; Encapsulacion -- clase 087
 read n
 kill ^SALDO
 set ^SALDO = 0
 do depositar(n)
 do depositar(n)
 write "saldo=", ^SALDO, !
 quit
 ;
depositar(x) ;
 set ^SALDO = ^SALDO + x
 quit
```

**Lo que esta clase enseña en M.** **M no tiene encapsulación de ninguna clase.** Todas las variables
locales son globales al proceso (clase 082) y todos los ***globals*** son visibles para todos los
procesos del entorno. `^SALDO` lo puede leer y escribir cualquier rutina del sistema.

No hay `private`, no hay módulos y no hay barreras. Y esa ausencia total es, seguramente, la
diferencia más grande entre M y cualquier otro lenguaje de esta página.

Lo que hay en su lugar es lo de la clase 086: **convención de prefijos** más una capa construida
encima. En **VistA**, esa capa es **FileMan**, y es la respuesta seria al problema:

```mumps
 do FILE^DICN(...)        ; crear un registro
 do UPDATE^DIE(...)       ; actualizar
 set x = $$GET1^DIQ(...)  ; consultar un campo
```

La regla de la plataforma es que **el código de aplicación NO toca los globals directamente**: los
toca a través de las APIs de FileMan, que validan los datos, respetan la seguridad, mantienen los
índices y registran la auditoría.

Eso es encapsulación implementada **como una biblioteca y una norma**, no como una característica del
lenguaje. Y funciona: VistA lleva cuarenta años y millones de líneas con ese contrato.

También falla exactamente como cabría esperar: **hay código antiguo que accede directamente a los
globals**, saltándose la validación, y localizarlo es un problema recurrente de mantenimiento. Cuando
la barrera es una norma, alguien acaba cruzándola.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n saldo |

n := stdin nextLine trimBoth asNumber.

saldo := 0.
saldo := saldo + n.
saldo := saldo + n.

Transcript show: 'saldo=', saldo printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk tiene la regla más simple y más tajante de toda
esta página, y **no hace falta ninguna palabra clave para expresarla**:

> **Todas las variables de instancia son privadas. Todos los métodos son públicos. Siempre.**

No hay `private`, no hay `public`, no hay `protected`. Un objeto **no puede** acceder a las variables
de otro, ni siquiera de la misma clase: tiene que enviarle un mensaje.

```smalltalk
Cuenta >> depositar: x
    saldo := saldo + x.          "saldo es MÍO"

Cuenta >> sumarA: otraCuenta
    otraCuenta saldo             "tengo que PREGUNTARLE, no puedo mirar"
```

Compara con Java o C++, donde un método puede acceder a los campos privados **de otra instancia de su
misma clase**. En Smalltalk eso es imposible, y esa restricción refuerza el paso de mensajes como
único mecanismo de comunicación — la idea de Alan Kay de la clase 043.

Que **todos los métodos sean públicos** parece una carencia y es coherente: si la privacidad de un
método fuera una barrera, sería una barrera al envío de mensajes, que es lo único que hay. La
convención es marcar los internos poniéndolos en una **categoría llamada `private`** en el navegador —
organización, no protección.

Y es la misma postura que Python y Lisp: **la privacidad es una indicación de diseño**. Ese consenso
entre tres lenguajes muy distintos, frente al de Java y C++, es una de las divisiones más nítidas del
diseño de lenguajes.

---

## Y de vuelta a la clase

Lo transferible: **la encapsulación no es esconder, es prometer poco**. Un campo público es una
promesa de que ese campo existirá para siempre con ese nombre y ese tipo; uno privado deja libertad
para cambiarlo. Por eso los lenguajes modernos hacen **privado el defecto** —Rust, los módulos de
C++20, `private` en Fortran, `export` en RPG— y por eso el consejo práctico es el mismo en todos:
**exporta lo mínimo, y lo que exportes, no lo cambies**.

⏮️ [Volver a la clase 087](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
