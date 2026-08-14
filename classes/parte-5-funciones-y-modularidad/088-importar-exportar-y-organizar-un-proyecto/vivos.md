# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 088

> [⬅️ Volver a la clase 088](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

El valor absoluto, calculado por algo que vive en otro sitio. La última clase de la Parte 5 cierra el
recorrido: **cómo se junta el trabajo de varias personas en un solo programa**. Y la respuesta separa
a estos lenguajes en dos épocas: los que **copian texto** —`COPY`, `%INCLUDE`, `#include`— y los que
**enlazan unidades compiladas con su interfaz comprobada**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **organización de un proyecto**, y estos lenguajes lo enseñan porque cargan con
> la solución antigua y con la moderna a la vez. **COBOL con `COPY`**, **PL/I con `%INCLUDE`** y **C++
> con `#include`** son sustitución textual: sin comprobación entre unidades, con recompilación en
> cascada y con el orden importando.
>
> Enfrente, **Ada con `with`**, **Fortran con `use`**, **Pascal con `uses`** y **RPG con los directorios
> de enlace** compilan cada unidad por separado y **comprueban que encajen**. Ada lo hacía en 1983 y
> C++ lo consiguió en 2020.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` → stdout: `abs=<|n|>`
- **Regla:** `abs(n) = |n|`

| stdin | esperado |
|---|---|
| `-5` | `abs=5` |
| `3` | `abs=3` |
| `0` | `abs=0` |

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
PROGRAM-ID. ABSOLUTO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9) COMP-3.
01  R       PIC 9(9)  COMP-3.
01  ED-R    PIC Z(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION NUMVAL(LINEA) TO N

    COMPUTE R = FUNCTION ABS(N)

    MOVE R TO ED-R
    DISPLAY "abs=" FUNCTION TRIM(ED-R)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** COBOL tiene **dos formas de reutilizar**, y son de naturalezas
opuestas.

**`COPY`** es **inclusión textual** en tiempo de compilación, como el `#include` de C:

```cobol
COPY CLIENTE.
COPY CLIENTE REPLACING ==:PRE:== BY ==CLI==.
```

Comparte **definiciones de datos**, y su versión con `REPLACING` es el genérico de los pobres de la
clase 078. Sus problemas son los conocidos: cambiar un copybook obliga a **recompilar todos los
programas que lo usan**, y nadie garantiza que se haga.

Ese es un problema operativo serio en un sistema con miles de programas, y la solución es una
herramienta de gestión de dependencias —IBM Dependency Based Build, Endevor, Changeman— que mantiene
un **grafo de qué programa usa qué copybook** y decide qué recompilar. Es un `make` para mainframe, y
lleva funcionando décadas.

**`CALL`** es lo contrario: enlaza con un programa **compilado por separado**, y puede ser estático
—resuelto al enlazar— o dinámico —resuelto al ejecutar, clase 085—. Cambiar un subprograma llamado
dinámicamente **no obliga a recompilar a sus clientes**.

Esa distinción define la arquitectura de un sistema COBOL: **los datos se comparten por texto y el
código por enlace**. Y explica por qué los copybooks se tratan con tanto cuidado: son la única
dependencia que se propaga a la compilación.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
module matematicas
   implicit none
   private
   public :: valor_absoluto

contains

   pure function valor_absoluto(x) result(r)
      integer, intent(in) :: x
      integer :: r
      r = abs(x)
   end function valor_absoluto

end module matematicas


program absoluto
   use matematicas, only: valor_absoluto     ! importación SELECTIVA
   implicit none
   integer :: n

   read(*, *) n
   write(*, '(A,I0)') 'abs=', valor_absoluto(n)
end program absoluto
```

**Lo que esta clase enseña en Fortran.** `use modulo, only: nombre` es la importación de Fortran, y la
cláusula **`only`** es la práctica recomendada: importa **solo lo que se usa**, y la dependencia queda
documentada en la propia línea.

Y hay una forma más, para resolver colisiones:

```fortran
use matematicas, only: mi_abs => valor_absoluto    ! RENOMBRA al importar
use otro_modulo, only: valor_absoluto
```

El operador `=>` renombra, así que dos módulos con el mismo nombre pueden convivir. Es lo mismo que
`as` en Python y `use x as y` en Rust.

Lo que distingue a Fortran en esta clase es una consecuencia práctica de los módulos: **el orden de
compilación importa**. Un módulo tiene que estar compilado antes que quien lo usa, porque el
compilador genera un fichero `.mod` con su interfaz que el cliente necesita leer.

En un proyecto con cien módulos, calcular ese orden a mano es inviable, y de ahí que Fortran tenga un
ecosistema entero de herramientas para deducir el grafo de dependencias —`makedepf90`, y hoy
**`fpm`**, el gestor de paquetes oficial—:

```toml
name = "mi_proyecto"
[dependencies]
stdlib = { git = "https://github.com/fortran-lang/stdlib" }
```

`fpm` deduce el orden solo, compila y gestiona dependencias externas. Que un lenguaje de 1957
consiguiera su gestor de paquetes en 2020 es tarde, y es exactamente el tipo de modernización que esta
sección quiere mostrar.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Absoluto is

   package Matematicas is
      function Valor_Absoluto (X : Integer) return Integer;
   end Matematicas;

   package body Matematicas is
      function Valor_Absoluto (X : Integer) return Integer is
        (if X < 0 then -X else X);
   end Matematicas;

   N : Integer;
begin
   Get (N);

   Put ("abs=");
   Put (Matematicas.Valor_Absoluto (N), Width => 1);
   New_Line;
end Absoluto;
```

**Lo que esta clase enseña en Ada.** Ada separa **dos cosas** que en casi todos los lenguajes van
juntas, y esa separación es de las mejores decisiones de su diseño:

```ada
with Ada.Text_IO;        --  DEPENDENCIA: "necesito compilar contra esto"
use  Ada.Text_IO;        --  VISIBILIDAD: "y quiero sus nombres sin cualificar"
```

`with` declara la dependencia y **es lo único que necesita el compilador**. `use` es opcional y solo
afecta a la comodidad de escritura. Se puede tener `with` sin `use` y escribir
`Ada.Text_IO.Put_Line (...)` completo, que es lo que hacen las guías de estilo para código crítico —
porque el sitio de la llamada dice de dónde viene cada cosa.

Compara con `#include` de C++, que hace las dos cosas a la vez y sin control, o con `import` de
Python, donde `from x import *` es la opción desaconsejada.

Y Ada tiene una regla que evita el problema clásico de `use`: **si dos paquetes usados exportan el
mismo nombre, ninguno de los dos es visible** y hay que cualificar. El compilador **se niega** en
lugar de elegir por ti, que es lo contrario de la resolución de sobrecarga de C++.

Sobre la organización, Ada impone una correspondencia estricta que GNAT convierte en regla de
ficheros: `paquete.ads` para la especificación, `paquete.adb` para el cuerpo, y los subpaquetes
jerárquicos con guion — `matematicas-vectores.ads` para `Matematicas.Vectores`.

Y **Alire** (`alr`), el gestor de paquetes moderno, completa el cuadro: `alr with aws` añade una
dependencia, resuelve versiones y compila. Llegó en 2018.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Absoluto;
{$MODE OBJFPC}{$H+}
uses SysUtils, Math;      { unidades: SysUtils para IntToStr, Math para Abs }

var
  N: Integer;

begin
  Read(N);
  WriteLn('abs=', IntToStr(Abs(N)));
end.
```

**Lo que esta clase enseña en Pascal.** La cláusula **`uses`** es la importación, y tiene una
propiedad que la distingue de casi todas las demás: **importa TODO lo público de la unidad, sin
selección**.

No hay `uses Math only (Abs)`. Y como consecuencia, **el orden importa**: si dos unidades declaran el
mismo nombre, **gana la última** de la lista.

```pascal
uses UnidadA, UnidadB;    { si las dos declaran Doblar, se usa la de UnidadB }
```

Esa regla —"gana la última"— es sencilla y es una fuente real de errores al añadir una unidad a un
programa grande. La solución es cualificar: `UnidadA.Doblar(x)`.

Y Pascal distingue **dos secciones `uses`**, lo que sí es un acierto:

```pascal
unit Mi;
interface
uses A;          { A es visible para QUIEN USE Mi }
implementation
uses B;          { B es un detalle interno; nadie más lo ve }
```

Poner una dependencia en `implementation` la mantiene privada y **rompe las dependencias circulares**:
dos unidades pueden usarse mutuamente si al menos una lo hace desde `implementation`. Es un mecanismo
que Ada resuelve con `limited with` y que C++ resuelve con declaraciones adelantadas.

El ecosistema moderno lo completa con el **Online Package Manager** de Lazarus y con **fpcupdeluxe**,
y Delphi con **GetIt** — gestores de paquetes que llegaron tarde, como en casi todos los lenguajes de
esta página.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((n (read)))
  (format t "abs=~D~%" (abs n)))
```

**Lo que esta clase enseña en Common Lisp.** El estándar de Common Lisp **no dice nada sobre ficheros,
compilación ni proyectos**: define `defpackage` para los nombres (clase 086) y nada más. Cómo se
carga el código es problema del entorno.

Esa laguna la llenó **ASDF** (*Another System Definition Facility*), que es el `make` del mundo Lisp:

```lisp
(defsystem "mi-proyecto"
  :depends-on ("alexandria" "cl-ppcre")
  :components ((:file "paquetes")
               (:file "utiles" :depends-on ("paquetes"))
               (:file "principal" :depends-on ("utiles"))))
```

Un fichero `.asd` declara los componentes, sus dependencias y el orden. ASDF calcula el grafo,
recompila lo necesario y lo carga.

Y encima está **Quicklisp**, que resuelve la distribución: `(ql:quickload "cl-ppcre")` descarga,
compila y carga una biblioteca y todas sus dependencias.

Lo interesante es la separación en tres capas, que Lisp hace más explícita que nadie:

| Capa | Qué resuelve | En Lisp |
|---|---|---|
| Espacio de nombres | Colisión de nombres | `defpackage` (en el lenguaje) |
| Sistema de construcción | Orden y compilación | ASDF (biblioteca) |
| Gestor de paquetes | Distribución y versiones | Quicklisp (externo) |

En Python son `import`, `setuptools` y `pip`; en Rust, `mod`, `cargo build` y `crates.io`. Lo que en
Rust es una sola herramienta, en Lisp son tres piezas independientes — con la ventaja de que se pueden
sustituir por separado, y el inconveniente de que hay que conocer las tres.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
namespace eval ::matematicas {
    namespace export valor_absoluto
    proc valor_absoluto {x} { return [expr {abs($x)}] }
}

namespace import ::matematicas::valor_absoluto     ;# importar al espacio actual

gets stdin linea
set n [string trim $linea]

puts "abs=[valor_absoluto $n]"
```

**Lo que esta clase enseña en Tcl.** Tcl separa con claridad **la carga** de **la visibilidad**, igual
que Ada separa `with` de `use`:

```tcl
package require http 2.9          ;# CARGAR, con requisito de VERSIÓN
namespace import ::http::*        ;# hacer visibles sus nombres aquí
```

`package require` busca el paquete en la ruta de bibliotecas, comprueba la versión y lo carga **una
sola vez**. Y el mecanismo que lo hace posible es el **índice de paquetes**:

```tcl
# pkgIndex.tcl -- generado automáticamente
package ifneeded http 2.9.5 [list source [file join $dir http.tcl]]
```

`package ifneeded` registra **cómo cargar** un paquete sin cargarlo. Tcl solo ejecuta ese guion si
alguien lo pide, así que un directorio con doscientos paquetes se indexa sin cargar ninguno. Es carga
perezosa a nivel de proyecto, y funciona desde 1996.

Y `namespace import` copia **los nombres exportados** al espacio actual, con la posibilidad de
renombrar:

```tcl
namespace import ::matematicas::valor_absoluto
namespace import {*}[namespace children ::plugins]
namespace forget ::matematicas::*                  ;# deshacer la importación
```

`namespace forget` no tiene equivalente en la mayoría de los lenguajes: **retira** una importación. En
un intérprete vivo, donde el estado persiste entre cargas, poder deshacer importa.

Para la distribución, el ecosistema tiene **teapot** y **TEA** (*Tcl Extension Architecture*), y los
**Starkits** de la clase 041 permiten empaquetar aplicación, intérprete y paquetes en un solo fichero
ejecutable.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

package Matematicas;
sub valor_absoluto { return abs($_[0]) }

package main;

my $n = <STDIN>;
chomp $n;

print "abs=", Matematicas::valor_absoluto($n), "\n";
```

**Lo que esta clase enseña en Perl.** Como se vio en la clase 086, **`use` es `require` más `import`**,
y esa segunda mitad es lo que hace peculiar a Perl: **`import` es un método normal que el módulo
define**.

```perl
use Mi::Modulo qw(foo bar);
#  equivale a:
#  BEGIN { require Mi::Modulo; Mi::Modulo->import('foo', 'bar'); }
```

El módulo decide qué hacer con esos argumentos. Casi todos heredan de **`Exporter`**:

```perl
package Matematicas;
use Exporter 'import';
our @EXPORT_OK = qw(valor_absoluto);      # se exportan si se piden
our @EXPORT    = qw();                     # se exportan SIEMPRE (desaconsejado)
our %EXPORT_TAGS = (todo => [@EXPORT_OK]); # grupos: use X qw(:todo)
```

La distinción entre `@EXPORT` y `@EXPORT_OK` es la lección: **`@EXPORT` contamina el espacio del
cliente sin que lo pida**, y la práctica moderna es dejarlo vacío y usar solo `@EXPORT_OK`.

Y el ecosistema es la aportación histórica de Perl a esta clase: **CPAN**, de 1995, fue **el primer
gran repositorio de módulos de la historia**, y el modelo del que salieron PyPI, npm, RubyGems y
crates.io.

Lo que CPAN tiene y casi ningún otro ecosistema ha replicado es **CPAN Testers**: una red de
voluntarios que ejecuta automáticamente la batería de pruebas de cada módulo en **decenas de
combinaciones** de sistema operativo y versión de Perl, y publica los resultados. Antes de instalar
algo se puede consultar si pasa en tu plataforma exacta.

Para fijar versiones por proyecto están `cpanfile` y **Carton**, el equivalente de un *lockfile*.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <cstdlib>
#include <iostream>

namespace matematicas {
    int valor_absoluto(int x) { return std::abs(x); }
}

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "abs=" << matematicas::valor_absoluto(n) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** `#include` es **sustitución textual**, y durante cuarenta años ha
sido la única forma de compartir código en C y C++. Sus consecuencias, ya apuntadas en la clase 086,
son medibles: un `.cpp` que incluya `<iostream>` compila decenas de miles de líneas.

De ahí una colección entera de técnicas que existen **solo** para mitigar el `#include`:

```cpp
#pragma once                     // guardas de inclusión
class Widget;                    // declaración adelantada: evita incluir la cabecera
class Impl;                      // modismo PIMPL: ocultar la implementación
// unity builds, cabeceras precompiladas, include-what-you-use...
```

**Los módulos de C++20** resuelven el problema de raíz —una unidad compilada, importada ya
analizada— y su adopción avanza despacio porque exige que el sistema de construcción entienda el
grafo de dependencias entre módulos, que no se puede deducir del texto tan fácilmente.

Y el ecosistema es la otra mitad de esta clase. C++ estuvo **treinta años sin gestor de paquetes**, y
hoy hay dos que compiten:

```bash
vcpkg install fmt          # Microsoft, orientado a bibliotecas del sistema
conan install .            # con perfiles y binarios precompilados
```

Que llegaran tan tarde explica una peculiaridad cultural del mundo C++: **la costumbre de incluir las
dependencias como submódulos de Git o de copiarlas al repositorio**, que en Rust o Node sería
impensable.

Y `std::abs` para enteros está en `<cstdlib>`, no en `<cmath>` — un detalle heredado de C que sigue
sorprendiendo.

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

dcl-pi ABSOLUTO;
  n int(10) const;
end-pi;

dcl-s salida char(30);

salida = 'abs=' + %char(valorAbsoluto(n));
dsply salida;

*inlr = *on;
return;

// En un proyecto real: otro módulo con `export`, enlazado en un
// PROGRAMA DE SERVICIO y localizado por un DIRECTORIO DE ENLACE.
dcl-proc valorAbsoluto;
  dcl-pi *n int(10);
    x int(10) const;
  end-pi;
  return %abs(x);
end-proc;
```

**Lo que esta clase enseña en RPG.** La organización de un proyecto en IBM i tiene cuatro piezas que
ya aparecieron en la clase 086, y aquí se ven en su papel de "importar":

1. **`/COPY` o `/INCLUDE`** — inclusión **textual** de prototipos, como el `COPY` de COBOL. Es como se
   comparten las declaraciones `dcl-pr`.
2. **Módulo** — la unidad compilada.
3. **Programa de servicio** — la biblioteca dinámica.
4. **Directorio de enlace** (`*BNDDIR`) — **dónde buscar** lo que falte al enlazar.

La cuarta es la que hace de "ruta de búsqueda": se declara en el propio fuente y el enlazador la
consulta.

```rpgle
ctl-opt bnddir('MIAPP/UTILES');
/include qrpgleref,prototipos
```

Con eso, `valorAbsoluto` se resuelve automáticamente en el programa de servicio correspondiente, sin
enumerar módulos.

Y hay una diferencia importante con casi todos los lenguajes de esta página: **el enlace por defecto
es dinámico**. Un programa de servicio se carga en tiempo de ejecución y se **comparte entre todos los
trabajos** que lo usen. Corregir un error es recompilar el programa de servicio; **los programas que
lo llaman no se tocan**, siempre que la firma de la clase 086 no cambie.

Esa propiedad —actualizar una biblioteca sin recompilar a sus clientes, con verificación de firma al
cargar— es exactamente lo que en Linux dan los `soname`, y en IBM i está integrada en el sistema desde
1993.

El ecosistema moderno añade Git, **`bob`** para construcción reproducible y **`iproj.json`** para
declarar la estructura del proyecto desde VS Code.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 absoluto: procedure options(main);

    declare n fixed binary(31);

    get list (n);
    put skip list ('abs=' || trim(char(valor_absoluto(n))));

 valor_absoluto: procedure (x) returns (fixed binary(31));
    declare x fixed binary(31);
    return (abs(x));
 end valor_absoluto;

 end absoluto;
```

**Lo que esta clase enseña en PL/I.** PL/I organiza un proyecto con las dos herramientas de su época,
y las dos son las antiguas:

**`%INCLUDE`** para las declaraciones —inclusión textual, con todos los problemas del `COPY` de COBOL
y del `#include` de C—:

```pli
%include declaraciones;
%include registro_cliente;
```

Y **procedimientos externos** enlazados por nombre, sin comprobación de firma entre unidades. Si un
programa declara `entry (fixed binary(31))` y el procedimiento real espera `fixed decimal(15,2)`, el
enlazador **empareja los nombres igualmente** y el resultado es corrupción de datos.

Esa es la carencia que Ada resolvió en 1983 con la comprobación entre unidades de compilación, y es
uno de los argumentos más fuertes a favor de los módulos.

Lo que sí tiene el mundo PL/I, y compensa parte del problema, es la infraestructura del mainframe: los
**gestores de cambio** —Endevor, Changeman, IBM DBB— mantienen el grafo de dependencias entre fuentes
e includes, y recompilan en cascada lo que haga falta. Es un sistema de construcción externo al
lenguaje, y lleva funcionando desde los 80.

El preprocesador de PL/I merece una nota final, porque va mucho más allá de `%INCLUDE`: tiene
**variables, condicionales, bucles y procedimientos propios**, ejecutados en tiempo de compilación.

```pli
%declare depurar fixed;
%depurar = 1;
%if depurar = 1 %then %do;
   put skip list ('traza');
%end;
```

Es un lenguaje completo dentro del lenguaje, y es el antepasado directo de la metaprogramación por
preprocesador — con las mismas virtudes y los mismos abusos que hoy se le reprochan al de C.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
ABSOLUTO ; Importar y organizar -- clase 088
 read n
 write "abs=", $$abs^ABSOLUTO(n), !
 quit
 ;
abs(x) ; valor absoluto
 quit $select(x<0 : -x, 1 : x)
```

**Lo que esta clase enseña en M.** **M no tiene importación.** No hay `import`, `use`, `require` ni
`with`: **todas las rutinas del entorno son visibles desde cualquier rutina**, y se invocan con
`ETIQUETA^RUTINA`.

```mumps
 do PROCESAR^FACTURA(id)
 set x = $$CALCULAR^UTIL(a, b)
```

El `^` separa la etiqueta del nombre de la rutina, y no hace falta declarar nada. Es el modelo más
simple posible, y tiene el problema de la clase 086: **un único espacio de nombres global** para todo
el sistema.

Y sin embargo hay una propiedad que compensa parcialmente y que conviene entender: **la carga es
automática y perezosa**. La primera vez que se ejecuta `do X^Y`, el sistema busca `Y`, la carga en el
área de rutinas del proceso y la ejecuta. No hay fase de enlace, no hay ejecutable y **no hay
recompilación en cascada**: corregir una rutina afecta a todo el sistema **en la siguiente llamada**.

Eso hace que el despliegue en M sea trivial —copiar una rutina y ya está— y explica que los sistemas
de M lleven décadas sin reiniciarse.

El ecosistema moderno ha añadido lo que faltaba: **YottaDB tiene un gestor de paquetes** y una
estructura de proyecto con directorios de rutinas y variables de entorno (`$ZROUTINES`) que definen la
ruta de búsqueda — algo parecido a un `PATH` para código.

Y en **VistA**, la distribución tiene su propio nombre y su propio formato: los **KIDS builds**
(*Kernel Installation and Distribution System*), que empaquetan rutinas, definiciones de FileMan y
guiones de instalación en un fichero que se despliega en cientos de hospitales. Es un gestor de
paquetes de dominio específico, construido sobre un lenguaje que no tiene ninguno.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n |

n := stdin nextLine trimBoth asNumber.

Transcript show: 'abs=', n abs printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** **En Smalltalk no se importa nada.** Todas las clases del
sistema están siempre disponibles en el diccionario `Smalltalk`, así que `n abs` funciona sin
declarar ninguna dependencia.

Eso es consecuencia directa del modelo de **imagen** de la clase 041: no hay ficheros que enlazar
porque **todo el sistema ya está cargado y vivo**. La pregunta "¿de dónde viene esta clase?" se
responde con una herramienta, no con una línea de código.

Y ahí está el problema que la comunidad tardó veinte años en resolver: **si no hay dependencias
declaradas, ¿cómo se distribuye un proyecto?** La imagen es un binario de cientos de megas con todo
mezclado.

La respuesta es una pila de herramientas que hoy funciona bien:

| Herramienta | Qué resuelve |
|---|---|
| **Monticello** | Versionado de paquetes; el "commit" de Smalltalk |
| **Metacello** | **Declaración de dependencias y versiones**, el `package.json` |
| **Tonel** | Guardar el código como **ficheros de texto** legibles por Git |
| **Iceberg** | Integración con Git y GitHub desde dentro de la imagen |

Una especificación de Metacello se parece bastante a lo que se espera hoy:

```smalltalk
spec baseline: 'MiProyecto' with: [
    spec repository: 'github://usuario/proyecto:main/src' ].
```

Y **Tonel** es la pieza decisiva: convirtió el código de Smalltalk en ficheros de texto, uno por
clase, y con eso lo hizo compatible con Git, con las revisiones por *pull request* y con la
integración continua.

Es la respuesta a la crítica más justificada que recibió Smalltalk durante décadas —"no encaja en un
flujo moderno"— y llegó, como tantas cosas de esta sección, mucho después de que el lenguaje se diera
por muerto.

---

## Y de vuelta a la clase

Lo transferible: **la unidad de reutilización determina la arquitectura**. Si compartir código es
copiar texto, la unidad natural es el fichero y los proyectos acaban con cientos de cabeceras
interdependientes. Si es una unidad compilada con interfaz, la unidad natural es el módulo y las
dependencias se ven. Y si además hay un gestor de paquetes —`fpm`, Alire, Quicklisp, CPAN, vcpkg— la
unidad pasa a ser la **biblioteca versionada**. Los tres niveles conviven hoy en casi todos estos
lenguajes, y saber en cuál estás explica por qué tu compilación tarda lo que tarda.

⏮️ [Volver a la clase 088](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
