# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 086

> [⬅️ Volver a la clase 086](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Una función `doblar` que vive **dentro de algo**. La pregunta de esta clase es cómo evita un lenguaje
que dos personas que nunca se han visto elijan el mismo nombre. Y aquí hay un hallazgo importante:
**el paquete de Ada, de 1983, es el antepasado directo del módulo moderno**, y su separación entre
especificación e implementación es la que copiaron Modula-2, C++ y todos los demás.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **espacio de nombres y la unidad de compilación**, y estos lenguajes lo enseñan
> porque uno de ellos lo inventó. El **`package` de Ada** separa *qué ofrece* de *cómo lo hace*, con
> compilación separada y comprobación entre unidades — algo que C no tuvo nunca y que C++ solo consiguió
> con los módulos de C++20.
>
> Y en el otro extremo, **COBOL y M no tienen espacios de nombres en absoluto**: el nombre de una rutina
> de M es global a todo el sistema, y los prefijos de tres letras —`DIC`, `DIE`, `ZZ`— son un registro
> de nombres administrado por convención humana desde hace cincuenta años.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` → stdout: `resultado=<2n>`
- **Regla:** `modulo.doble(n) = 2n`

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `-4` | `resultado=-8` |

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
PROGRAM-ID. MODULOS.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9)  COMP-3.
01  R       PIC S9(18) COMP-3.
01  ED-R    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N

    PERFORM DOBLAR

    MOVE R TO ED-R
    DISPLAY "resultado=" FUNCTION TRIM(ED-R)
    STOP RUN.

DOBLAR.
    COMPUTE R = N * 2.
```

**Lo que esta clase enseña en COBOL.** **COBOL no tiene espacios de nombres.** Los nombres de programa
son globales a toda la instalación —una biblioteca de carga con miles de miembros de ocho caracteres—
y los nombres de datos son globales al programa (clase 082).

De ahí las dos convenciones que sostienen los sistemas grandes:

1. **Prefijos de nombre de programa por aplicación**: `CLI0100`, `CLI0200`, `FAC0100`. Los tres o
   cuatro primeros caracteres identifican el subsistema, y hay un registro documentado de quién posee
   cada prefijo. Es un espacio de nombres administrado por un ser humano.
2. **Copybooks** para compartir definiciones (clase 052), con `REPLACING` para parametrizarlos.

Y la limitación de ocho caracteres para el nombre de programa no es de COBOL: es del **sistema de
bibliotecas de z/OS**, y ha condicionado la nomenclatura de la industria durante sesenta años.

COBOL sí tiene una forma de módulo, y es la de la clase 082: los **programas anidados** con `GLOBAL` y
`COMMON`.

```cobol
    IDENTIFICATION DIVISION.
    PROGRAM-ID. UTILES IS COMMON.      *> visible para los HERMANOS anidados
```

Un programa `COMMON` es visible desde los demás programas anidados del mismo padre, pero no desde
fuera. Es encapsulación real y **muy poco usada**, porque llegó en 1985 cuando ya había millones de
líneas escritas con prefijos.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
module utiles
   implicit none
   private                       ! todo privado por defecto
   public :: doblar

contains

   pure function doblar(x) result(r)
      integer, intent(in) :: x
      integer :: r
      r = 2 * x
   end function doblar

end module utiles


program modulos
   use utiles, only: doblar      ! importa SOLO lo que necesita
   implicit none
   integer :: n

   read(*, *) n
   write(*, '(A,I0)') 'resultado=', doblar(n)
end program modulos
```

**Lo que esta clase enseña en Fortran.** El **`module`** llegó con **Fortran 90** y fue el cambio más
importante del lenguaje después del formato libre. Antes, todo era subrutinas externas sueltas y
bloques `COMMON`:

```fortran
      COMMON /DATOS/ X, Y, Z      ! memoria compartida por POSICIÓN
```

Un `COMMON` empareja variables **por posición, no por nombre**, y **cada fichero declara su propia
versión**. Si dos ficheros lo declaraban distinto —un `REAL` donde otro ponía `INTEGER`— el programa
compilaba y los datos se corrompían en silencio. Era la mayor fuente de errores del Fortran clásico.

El módulo lo resuelve todo de golpe:

- **Interfaces explícitas**: el compilador comprueba las llamadas entre unidades.
- **`private` / `public`**: encapsulación real (clase 087).
- **`use ... only:`**: importación selectiva, que evita colisiones.
- Y permite **argumentos opcionales, palabras clave y genéricos**, que necesitan interfaz explícita.

Fíjate en `private` como primera línea del módulo: **invierte el defecto** para que todo sea privado
salvo lo que se declare `public`. Es la práctica recomendada, y es la misma política que Rust, RPG y
los módulos de C++20.

Y `use utiles, only: doblar` es importación explícita: sin `only`, se importa todo y aumenta el riesgo
de colisión. Con él, la dependencia queda documentada en la línea.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Modulos is

   --  ESPECIFICACIÓN: qué ofrece el paquete.
   package Utiles is
      function Doblar (X : Integer) return Integer;
   end Utiles;

   --  CUERPO: cómo lo hace. En un proyecto real, en otro fichero.
   package body Utiles is
      function Doblar (X : Integer) return Integer is (2 * X);
   end Utiles;

   N : Integer;
begin
   Get (N);

   Put ("resultado=");
   Put (Utiles.Doblar (N), Width => 1);
   New_Line;
end Modulos;
```

**Lo que esta clase enseña en Ada.** **El paquete de Ada es el antepasado directo del módulo
moderno**, y su aportación decisiva es la separación en **dos unidades de compilación**:

```ada
--  utiles.ads : la ESPECIFICACIÓN. Es el contrato.
package Utiles is
   function Doblar (X : Integer) return Integer;
end Utiles;

--  utiles.adb : el CUERPO. Es la implementación.
package body Utiles is
   function Doblar (X : Integer) return Integer is (2 * X);
end Utiles;
```

Quien usa el paquete **solo necesita la especificación**, y el compilador **comprueba que el cuerpo la
cumpla**. Si cambia la implementación sin cambiar la especificación, **no hay que recompilar a los
clientes**.

Compara con C y C++ hasta 2020: el `.h` es **texto que se copia** en cada unidad, sin ninguna
comprobación de que el `.c` lo respete, y cambiar una cabecera obliga a recompilar todo lo que la
incluya. Ada resolvió eso en 1983.

Modula-2 (1978, Wirth) tuvo la misma idea casi a la vez, y de ahí la tomaron Turbo Pascal con las
`unit`, C++ con los módulos de C++20 y Rust con `mod`.

Ada añade además tres cosas que la mayoría no tiene: la **parte privada** (clase 087), los
**subpaquetes jerárquicos** —`Utiles.Texto`, `Utiles.Fechas`— que permiten extender un paquete sin
tocarlo, y los **paquetes genéricos** (clase 078), que se instancian con parámetros.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Modulos;
{$MODE OBJFPC}{$H+}
uses SysUtils;

{  En un proyecto real esto iría en una UNIT aparte:
   unit Utiles;  interface  function Doblar(...)  implementation ...  }
function Doblar(X: Integer): Integer;
begin
  Result := X * 2;
end;

var
  N: Integer;

begin
  Read(N);
  WriteLn('resultado=', IntToStr(Doblar(N)));
end.
```

**Lo que esta clase enseña en Pascal.** La **`unit`** de Turbo Pascal (1987) tomó la idea de Modula-2
y la hizo popular, con una estructura que se lee sola:

```pascal
unit Utiles;

interface                    { lo PÚBLICO: lo que ven los demás }
function Doblar(X: Integer): Integer;

implementation               { lo PRIVADO: nadie de fuera lo ve }
function Doblar(X: Integer): Integer;
begin
  Result := X * 2;
end;

initialization               { código que se ejecuta al CARGAR la unidad }
finalization                 { y al DESCARGARLA }
end.
```

Cuatro secciones con nombres que dicen exactamente qué hacen. Y la sección `interface` es lo único
que necesita quien haga `uses Utiles`.

`initialization` y `finalization` no tienen equivalente en Ada ni en C++: son bloques que el runtime
ejecuta al cargar y descargar la unidad, en orden de dependencias. Se usan para registrar clases,
abrir recursos y liberarlos, y son la razón de que muchas bibliotecas de Delphi funcionen con solo
añadirlas a la cláusula `uses`.

La compilación de Pascal aprovecha esto al máximo: **el compilador genera un fichero `.ppu` con la
interfaz ya analizada**, así que compilar un programa que usa cien unidades no reanaliza cien
cabeceras. Es la razón principal de la velocidad legendaria de Turbo Pascal y Free Pascal frente a
C++.

Lo que Pascal **no** tiene son espacios de nombres anidados de verdad. Delphi añadió los *namespaces
con puntos* —`Sistema.Utiles.Texto`— pero son un prefijo en el nombre de la unidad, no una jerarquía
real como los subpaquetes de Ada.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(defpackage :utiles
  (:use :cl)
  (:export #:doblar))

(in-package :utiles)

(defun doblar (x) (* 2 x))

(in-package :cl-user)

(let ((n (read)))
  (format t "resultado=~D~%" (utiles:doblar n)))
```

**Lo que esta clase enseña en Common Lisp.** Los **paquetes de Lisp no son módulos: son espacios de
nombres de SÍMBOLOS**, y esa diferencia es la clave para entenderlos.

Un paquete es una tabla que asocia **nombres a símbolos**. Cuando el lector encuentra `doblar`, busca
en el paquete actual el símbolo con ese nombre; si no está, lo crea. `utiles:doblar` es "el símbolo
`doblar` del paquete `utiles`".

De ahí salen dos notaciones que hay que distinguir:

```lisp
utiles:doblar      ; símbolo EXPORTADO: parte de la interfaz
utiles::interno    ; DOS puntos: acceso a un símbolo NO exportado
```

El doble dos puntos **funciona siempre** — se puede acceder a cualquier símbolo interno de cualquier
paquete. No es una barrera, es una señal: escribir `::` es declarar por escrito que estás usando algo
privado. Es la misma filosofía que el guion bajo en Python.

Y como los paquetes agrupan **símbolos**, no funciones, agrupan a la vez funciones, variables, clases,
macros y tipos — todo lo que tenga nombre.

Lo que Lisp **no** tiene en el estándar es un sistema de ficheros ni de compilación: `defpackage` dice
qué nombres hay, no de dónde salen. Eso lo aporta **ASDF**, el sistema de construcción de facto, con
`Quicklisp` encima para la distribución. Es la misma separación que en Python entre el `import` del
lenguaje y `pip`.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
namespace eval ::utiles {
    namespace export doblar

    proc doblar {x} {
        return [expr {$x * 2}]
    }
}

gets stdin linea
set n [string trim $linea]

puts "resultado=[::utiles::doblar $n]"
```

**Lo que esta clase enseña en Tcl.** Los **espacios de nombres** llegaron en **Tcl 8.0 (1997)**, y son
jerárquicos con separador `::`, igual que C++.

```tcl
namespace eval ::miapp::datos {
    variable cache          ;# variable del ESPACIO (clase 082)
    proc cargar {} { ... }
}
::miapp::datos::cargar
```

Y son **contenedores de tres cosas**: procedimientos, variables y otros espacios anidados.

Lo que hace peculiar a Tcl es que la **resolución de nombres es dinámica y por reglas de búsqueda**,
no estática:

```tcl
namespace eval ::miapp {
    proc f {} { g }       ;# ¿qué g?  Se busca en ::miapp, y si no, en ::
}
```

Un comando no cualificado se busca **primero en el espacio actual y después en el global**. Eso es
cómodo y produce sorpresas: definir un `::miapp::puts` cambia el significado de `puts` dentro de ese
espacio.

Y hay una separación que conviene conocer, porque Tcl tiene **dos** mecanismos donde otros tienen uno:

- **`namespace`** resuelve la **colisión de nombres**.
- **`package`** resuelve la **carga y las versiones**: `package require http 2.9` busca, carga y
  comprueba la versión.

Los dos son independientes: un paquete puede definir varios espacios, y un espacio puede montarse a
mano sin paquete. En Java, Python o Rust las dos cosas van juntas; en Tcl, como en Lisp con ASDF,
están separadas — y esa separación es la que permite `namespace import` selectivo.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

package Utiles;

sub doblar { return $_[0] * 2 }

package main;

my $n = <STDIN>;
chomp $n;

print "resultado=", Utiles::doblar($n), "\n";
```

**Lo que esta clase enseña en Perl.** `package` cambia **el espacio de nombres actual**, y todo lo
declarado a partir de ahí pertenece a él. `Utiles::doblar` es la cualificación completa, con `::` como
separador.

Y un paquete de Perl **no es un fichero ni una unidad de compilación**: es una entrada en la tabla de
símbolos global. Un fichero puede definir varios paquetes —como este programa— y un paquete puede
estar repartido en varios ficheros.

La convención —**un paquete por fichero, con la ruta del nombre**— es solo eso, una convención, y es lo
que `use` da por supuesto:

```perl
use Mi::Modulo;        # busca Mi/Modulo.pm en @INC
```

Perl separa además con claridad **tres cosas** que en otros lenguajes van juntas:

| Mecanismo | Qué hace |
|---|---|
| `package` | Declara el espacio de nombres |
| `require` | **Carga** el fichero, una sola vez, en ejecución |
| `use` | `require` en tiempo de compilación **+ `import`** |

`use` es literalmente `BEGIN { require X; X->import(...) }`, y esa tercera pieza —`import`— es un
**método normal** que el módulo define. Por eso `Exporter` es un módulo y no una característica del
lenguaje: exportar nombres es código que se ejecuta.

Eso permite módulos que hacen cosas muy distintas al importarse —`use strict` cambia el compilador,
`use constant` define constantes, `use parent` establece herencia— y es una de las capacidades más
características de Perl. También es la razón de que `use` no sea inocuo: **ejecuta código**.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

namespace utiles {
    int doblar(int x) { return x * 2; }
}

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "resultado=" << utiles::doblar(n) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** Los **espacios de nombres** (1998) resolvieron la colisión de
nombres, y **no** resolvieron la compilación separada — que era el otro problema de la clase.

Durante veintidós años, C++ compartió código con **`#include`**, que es **sustitución textual**: el
preprocesador copia el fichero entero en cada unidad de traducción. Las consecuencias son conocidas:

- Un `.cpp` de cien líneas que incluye `<iostream>` compila **decenas de miles** de líneas.
- Cambiar una cabecera obliga a recompilar todo lo que la incluya.
- El orden de los `#include` puede cambiar el significado del programa.
- Hacen falta guardas —`#pragma once`— para no incluir dos veces.

**C++20 introdujo los módulos**, que son por fin lo que Ada tenía en 1983:

```cpp
export module utiles;
export int doblar(int x) { return x * 2; }

// y en el cliente:
import utiles;
```

Un módulo se compila **una vez** a una representación binaria, y quien lo importa la lee ya analizada
—como el `.ppu` de Pascal—. Además, **lo no exportado es realmente invisible**, no solo por
convención.

La adopción va despacio por el ecosistema de sistemas de construcción, pero es el cambio estructural
más importante del lenguaje en décadas.

Y sobre los espacios: `using namespace std;` **en una cabecera** es el error clásico, porque contamina
a todo el que la incluya. En un `.cpp` es discutible; en un `.h`, no.

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

dcl-pi MODULOS;
  n int(10) const;
end-pi;

dcl-s salida char(40);

salida = 'resultado=' + %char(doblar(n));
dsply salida;

*inlr = *on;
return;

// En un proyecto real, esto estaría en OTRO módulo, con export,
// y se enlazaría en un PROGRAMA DE SERVICIO.
dcl-proc doblar;
  dcl-pi *n int(20);
    x int(10) const;
  end-pi;
  return x * 2;
end-proc;
```

**Lo que esta clase enseña en RPG.** El sistema de módulos de RPG llegó con **ILE** (1993) y es de los
más elaborados de esta página, con cuatro piezas:

1. **Módulo** (`*MODULE`): el resultado de compilar un fuente. Sus procedimientos son privados salvo
   que lleven `export`.
2. **Programa de servicio** (`*SRVPGM`): varios módulos enlazados en una unidad **compartida y
   cargada dinámicamente**, como una biblioteca dinámica.
3. **Directorio de enlace** (`*BNDDIR`): la lista de dónde buscar lo que falte al enlazar.
4. **Fuente de exportación de enlace**: **la lista ordenada de qué exporta un programa de servicio**.

La cuarta es la interesante y no tiene equivalente en el núcleo. Es un fichero que enumera los
procedimientos exportados **en orden**, y ese orden determina el número que usa el enlazador:

```text
STRPGMEXP PGMLVL(*CURRENT) SIGNATURE('UTILES V1')
  EXPORT SYMBOL("DOBLAR")
  EXPORT SYMBOL("TRIPLICAR")
ENDPGMEXP
```

La **firma** (`SIGNATURE`) permite versionar la interfaz: si se añade un procedimiento **al final**,
los programas antiguos siguen funcionando sin recompilar. Si se cambia el orden o se quita algo, la
firma cambia y **los clientes fallan al arrancar** con un mensaje claro.

Es control de versiones de ABI en el enlazador, exactamente el problema que en Linux resuelven los
`soname` y los scripts de versión de `ld`, integrado en la plataforma desde 1993.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 modulos: procedure options(main);

    declare n fixed binary(31);

    get list (n);
    put skip list ('resultado=' || trim(char(doblar(n))));

 doblar: procedure (x) returns (fixed binary(31));
    declare x fixed binary(31);
    return (x * 2);
 end doblar;

 end modulos;
```

**Lo que esta clase enseña en PL/I.** **PL/I no tiene módulos ni espacios de nombres.** Tiene
**procedimientos externos**, compilados por separado y enlazados por nombre, exactamente como C antes
de los módulos.

```pli
 doblar: procedure (x) returns (fixed binary(31)) external;
```

`external` declara que el nombre es visible para el enlazador. Y de ahí viene el problema clásico:
**los nombres externos son globales a todo el ejecutable**, y el enlazador los empareja por texto sin
comprobar firmas.

El sustituto de los módulos en PL/I es **`%INCLUDE`**, que es inclusión textual como el `COPY` de
COBOL y el `#include` de C:

```pli
%include declaraciones;
```

Con los mismos inconvenientes: sin comprobación entre unidades, con recompilación en cascada y con el
orden importando.

Lo que PL/I sí ofrece, y es lo que se usa en su lugar, es el **anidamiento léxico ilimitado** de la
clase 083: un procedimiento externo grande con procedimientos internos anidados **es** una forma de
módulo — lo interno es privado y lo externo es la interfaz.

```pli
 utiles: procedure external;
    declare estado fixed binary(31) static;   /* privado del "módulo" */

    doblar: procedure (x) returns (fixed binary(31));  /* privado también */
    ...
 end utiles;
```

Es encapsulación por anidamiento, la misma técnica que se usa en JavaScript con las funciones
inmediatamente invocadas, y era lo mejor disponible en 1964.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
MODULOS ; Modulos y espacios de nombres -- clase 086
 read n
 write "resultado=", $$doblar^MODULOS(n), !
 quit
 ;
doblar(x) ; devuelve el doble
 quit x * 2
```

**Lo que esta clase enseña en M.** **M no tiene espacios de nombres.** La unidad es la **rutina**, y su
nombre es **global a todo el sistema**: `$$doblar^UTILES` significa "la etiqueta `doblar` de la rutina
`UTILES`", y solo puede haber una `UTILES` en el entorno.

Peor aún: **los nombres de rutina están limitados a ocho caracteres** en el estándar, igual que los
nombres de programa de z/OS.

La solución que inventó la comunidad es la más artesanal de esta página: **un registro de prefijos
administrado por humanos**. En **VistA**, cada paquete tiene asignado un prefijo de dos o tres letras
por la oficina que coordina el proyecto:

```text
DI   -> FileMan (diccionario)
DIC  -> FileMan, búsquedas
LR   -> Laboratorio
PS   -> Farmacia
ZZ   -> reservado para código LOCAL de cada hospital
```

Todas las rutinas y todos los *globals* de Farmacia empiezan por `PS`. El prefijo `ZZ` está reservado
para las modificaciones locales de cada centro, de modo que **no colisionen con las actualizaciones
nacionales**.

Eso es un espacio de nombres implementado con documentación y disciplina, funcionando en un sistema de
millones de líneas desde los años 80. Es exactamente lo mismo que los prefijos `WS-` de COBOL y los
nombres `CLI0100`, escalado a nivel nacional.

Las implementaciones modernas sí lo resolvieron: **InterSystems IRIS tiene *namespaces* de verdad** —
entornos separados con sus propias rutinas y globals, y mapeos entre ellos—, y **YottaDB** permite
separar la configuración de globals por entorno. Pero el lenguaje base sigue sin ellos.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n |

n := stdin nextLine trimBoth asNumber.

Transcript show: 'resultado=', (n * 2) printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** **El Smalltalk-80 clásico no tiene espacios de nombres.**
Hay **un único diccionario global**, llamado `Smalltalk`, donde viven todas las clases del sistema. Dos
paquetes que definan una clase `Punto` colisionan.

La solución de la comunidad es la misma de M y COBOL: **prefijos**.

```smalltalk
RBParser         "Refactoring Browser"
GLMorphic        "Glamorous Toolkit"
ZnClient         "Zinc HTTP"
SUnitTest        "SUnit"
```

Dos o tres letras al principio de cada clase, por convención. Es un registro de prefijos exactamente
como el de VistA.

Lo que Smalltalk sí tiene, y es distinto, son dos mecanismos de **organización** que no son espacios
de nombres:

- **Categorías**: agrupan clases y métodos para el navegador. Son puramente organizativas.
- **Paquetes** (Monticello, Metacello): unidades de versionado y carga, con dependencias.

Un paquete decide **qué se carga y en qué orden**; una categoría decide **cómo se ve en la
herramienta**. Ninguno de los dos evita una colisión de nombres.

Los intentos de añadir espacios de nombres reales —VisualWorks los tiene, y hubo propuestas para
Pharo— chocaron con una dificultad de fondo: **en un sistema vivo con objetos ya instanciados**,
cambiar cómo se resuelven los nombres afecta a código en ejecución. Es un problema que un lenguaje
compilado no tiene.

Es el precio de la imagen viva de la clase 041, y una de las pocas cosas en las que el modelo de
Smalltalk sale claramente perdiendo.

---

## Y de vuelta a la clase

Lo transferible: **un módulo resuelve dos problemas distintos, y conviene no confundirlos**. Uno es la
**colisión de nombres**, que se resuelve con cualificación. El otro es la **compilación separada con
comprobación**: poder compilar A y B por separado y que el enlazador garantice que encajan. Los
lenguajes con `#include` textual —C, C++ hasta 2020, COBOL con `COPY`— resuelven el segundo mal, y por
eso sus tiempos de compilación y sus errores de enlace son lo que son.

⏮️ [Volver a la clase 086](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
