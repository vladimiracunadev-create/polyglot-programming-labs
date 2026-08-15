# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 143

> [⬅️ Volver a la clase 143](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Partir `1.2.3` en mayor, menor y parche. Detrás de ese formato de tres números está el contrato social
más importante de la ingeniería de software moderna —**el versionado semántico**— y esta página muestra
que **no es moderno en absoluto**: IBM i lleva desde 1988 comprobando compatibilidad de bibliotecas con
una **firma criptográfica calculada sobre la lista de exportaciones**, que es más fuerte que cualquier
número de versión.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **dependencia entre unidades de software y su compatibilidad**, y estos
> lenguajes lo enseñan porque **casi ninguno tuvo un gestor de paquetes durante décadas** y tuvieron que
> resolverlo de otras maneras: la copia de fuentes (COBOL), el fichero de módulo atado al compilador
> (Fortran), la firma del objeto (RPG), la imagen entera como unidad (Lisp y Smalltalk).
>
> Y aparece el problema que ningún gestor de paquetes ha resuelto del todo: **el infierno de las
> dependencias** —dos bibliotecas que exigen versiones incompatibles de una tercera— y las tres estrategias
> para vivir con él.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con una versión `mayor.menor.parche` → stdout: `mayor=<M> menor=<m> parche=<p>`
- **Regla:** `separar la versión por puntos`

| stdin | esperado |
|---|---|
| `1.2.3` | `mayor=1 menor=2 parche=3` |
| `0.5.10` | `mayor=0 menor=5 parche=10` |
| `2.0.0` | `mayor=2 menor=0 parche=0` |

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
PROGRAM-ID. VERSION.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(40).
01  C-MAY   PIC X(10).
01  C-MEN   PIC X(10).
01  C-PAR   PIC X(10).

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY "."
        INTO C-MAY C-MEN C-PAR
    END-UNSTRING

    DISPLAY "mayor=" FUNCTION TRIM(C-MAY)
            " menor=" FUNCTION TRIM(C-MEN)
            " parche=" FUNCTION TRIM(C-PAR)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** COBOL tiene el modelo de dependencias más simple y más peligroso
de esta página: **`COPY` es una inclusión textual**, igual que `#include` en C.

```cobol
       01  REG-CLIENTE.
           COPY CLIENTE.
```

Y de ahí sale el problema que define el mantenimiento de estos sistemas: **si el *copybook* cambia, hay
que recompilar todo lo que lo usa** — y si algo no se recompila, **lee la estructura con el mapa
antiguo**.

El resultado es basura silenciosa: los campos se desplazan y el programa lee el apellido donde espera
la fecha. Es el mismo fallo que la clase 106 describía para los ficheros de longitud fija, dentro del
proceso.

Y la solución que la industria construyó es una pieza de ingeniería seria que merece conocerse: **los
gestores de configuración de mainframe**.

| Herramienta | Qué hace |
|---|---|
| **Endevor** (CA/Broadcom) | inventario, promoción entre entornos, **recompilación automática de los dependientes** |
| **ChangeMan ZMF** | control de cambios con aprobaciones y auditoría |
| **SCLM** | el de IBM, incluido en ISPF |

**La capacidad clave es el análisis de impacto**: Endevor mantiene **un grafo de qué programa usa qué
copybook**, y al modificar uno **recompila todo lo que depende de él, en orden**.

Eso es exactamente lo que hoy hace un sistema de construcción con grafo de dependencias, y es de los
años ochenta.

Y el ciclo de promoción —**DEV → QA → PROD**, con aprobación en cada paso y **retroceso automático**—
es lo que hoy se llama despliegue por entornos (clase 148).

Y hay un detalle sobre las versiones que conviene extraer, porque contradice la intuición moderna: **en
estos sistemas no hay versiones de bibliotecas, hay una única versión desplegada**.

No existe "la aplicación A usa la versión 2 y la B usa la 3": **hay un copybook `CLIENTE` y todo el
sistema lo usa**. Es rígido, y a cambio **elimina por completo el infierno de dependencias**.

Es la primera de las tres estrategias que esta clase debe nombrar, y sigue siendo válida: **una sola
versión de todo, actualizada a la vez** — que es lo que hoy se llama repositorio único con dependencias
fijadas, y lo que hacen Google y varias empresas grandes por las mismas razones.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program version
   implicit none
   character(len=40) :: linea
   integer :: p1, p2

   read(*, '(A)') linea
   linea = adjustl(linea)

   p1 = index(linea, '.')
   p2 = index(linea(p1+1:), '.') + p1

   write(*, '(A)') 'mayor=' // trim(linea(1:p1-1)) //             &
                   ' menor=' // trim(linea(p1+1:p2-1)) //          &
                   ' parche=' // trim(adjustl(linea(p2+1:)))
end program version
```

**Lo que esta clase enseña en Fortran.** Fortran tiene un problema de dependencias que ningún otro
lenguaje de esta página tiene con la misma dureza: **los ficheros `.mod`**.

```bash
gfortran -c constantes.f90     # produce constantes.mod Y constantes.o
gfortran -c fisica.f90          # necesita constantes.mod PARA COMPILAR
gfortran -o prog *.o
```

Y esos ficheros tienen tres propiedades que complican todo:

**Primera, imponen un orden de compilación.** No se puede compilar `fisica.f90` antes que
`constantes.f90`, así que **el sistema de construcción tiene que conocer el grafo de `use`**. De ahí que
existan herramientas dedicadas —`makedepf90`, `fortdepend`, y el escáner de dependencias de CMake— **solo
para leer los `use` y generar el orden**.

**Segunda, y es la peor: el formato de `.mod` es específico del compilador y de su versión.**

```text
Fatal Error: Cannot read module 'constantes' at (1) because it was created
by a different version of GNU Fortran
```

**Un `.mod` de gfortran 12 no lo lee gfortran 13**, y desde luego no lo lee ifort. Así que **una
biblioteca Fortran precompilada solo sirve con el compilador exacto con que se hizo**.

Eso hace imposible lo que en otros lenguajes es normal —distribuir binarios— y explica por qué **el
ecosistema Fortran distribuye código fuente** y por qué gestores como Spack y EasyBuild **compilan
todo desde cero** para cada combinación de compilador y versión.

**Y tercera, la recompilación en cascada**: cambiar cualquier cosa en un módulo invalida su `.mod`, y
todo lo que lo usa se recompila. En un código de un millón de líneas eso son horas.

Y el ecosistema moderno, que por fin existe:

| Herramienta | Notas |
|---|---|
| **fpm** (*Fortran Package Manager*) | `fpm.toml`, resolución de dependencias desde git |
| **Spack** | gestor científico: compila y versiona por compilador y opciones |
| **CMake ≥ 3.7** | escanea `use` y genera el orden automáticamente |
| **stdlib** | la biblioteca estándar comunitaria |

**fpm es de 2020**: Fortran pasó **sesenta y tres años sin gestor de paquetes**. Y la lección de esta
clase es lo que eso costó: **cada laboratorio reimplementó las mismas rutinas**, y de ahí el estado del
código científico heredado.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO; use Ada.Text_IO;

procedure Version is
   Linea : String (1 .. 40);
   Ultimo : Natural;
   P1, P2 : Natural := 0;
begin
   Get_Line (Linea, Ultimo);

   for I in 1 .. Ultimo loop
      if Linea (I) = '.' then
         if P1 = 0 then
            P1 := I;
         else
            P2 := I;
         end if;
      end if;
   end loop;

   Put_Line ("mayor=" & Linea (1 .. P1 - 1) &
             " menor=" & Linea (P1 + 1 .. P2 - 1) &
             " parche=" & Linea (P2 + 1 .. Ultimo));
end Version;
```

**Lo que esta clase enseña en Ada.** Ada resolvió en 1983 lo que Fortran no resolvió hasta 2020, y de
una forma que merece conocerse: **el compilador conoce el grafo de dependencias porque el lenguaje lo
obliga**.

```ada
with Constantes;      --  esto NO es una inclusión textual: es una dependencia declarada
package Fisica is ...
```

Y de ahí sale la característica que la clase 123 ya adelantó: **el fase de *bind* comprueba que todas
las unidades compiladas son coherentes entre sí**.

```text
error: "constantes.ads" has been modified and must be recompiled
```

**El sistema detecta que una especificación cambió y que algo que dependía de ella no se recompiló**, y
se niega a enlazar. Es exactamente el fallo del *copybook* de COBOL en esta página, **detectado en vez
de sufrido**.

Y `gnatmake` / `gprbuild` **recompilan lo necesario en orden, solos**, sin fichero de dependencias
escrito a mano — porque leen los `with`.

Y hay una distinción del lenguaje que es directamente el tema de esta clase (clase 088):

```ada
package Cliente is                  --  la ESPECIFICACIÓN: el contrato
   procedure Guardar (C : Datos);
end Cliente;

package body Cliente is             --  la IMPLEMENTACIÓN
   ...
end Cliente;
```

**Quien depende de `Cliente` depende de la especificación, no del cuerpo.** Así que **cambiar el cuerpo
NO obliga a recompilar a los clientes** — solo a reenlazar.

Eso es control de dependencias en el lenguaje, y es lo que en C++ hay que conseguir a mano con el
patrón *pimpl* o con módulos (C++20).

Y el ecosistema moderno:

| Herramienta | Notas |
|---|---|
| **Alire** (`alr`) | gestor de paquetes: `alire.toml`, `alire.lock`, versionado semántico |
| **gprbuild / GPR** | proyectos con dependencias, variantes y escenarios |
| **`gnatls -d`** | listar de qué depende cada unidad |

**Alire es de 2018 y sigue el versionado semántico estrictamente**, con fichero de bloqueo. Y su
resolución hace algo que conviene entender: **elige un conjunto de versiones que satisfaga todas las
restricciones a la vez**, que es un problema de satisfacibilidad —resoluble, pero NP-completo en el caso
general.

Es la razón por la que instalar dependencias a veces tarda tanto: **el gestor está resolviendo un
sistema de restricciones**, no descargando ficheros.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Version;
{$MODE OBJFPC}{$H+}
uses SysUtils, StrUtils;

var
  Linea: string;
  P1, P2: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);

  P1 := Pos('.', Linea);
  P2 := PosEx('.', Linea, P1 + 1);

  WriteLn('mayor=',   Copy(Linea, 1, P1 - 1),
          ' menor=',  Copy(Linea, P1 + 1, P2 - P1 - 1),
          ' parche=', Copy(Linea, P2 + 1, Length(Linea)));
end.
```

**Lo que esta clase enseña en Pascal.** Pascal fue **de los primeros lenguajes con un modelo de módulos
compilados de verdad**, y la unidad de Turbo Pascal es su aportación:

```pascal
unit Calculos;
interface                    { lo que se exporta: el CONTRATO }
  function Sumar(A, B: Integer): Integer;
implementation                { lo privado }
  function Sumar(A, B: Integer): Integer;
  begin Result := A + B; end;
end.
```

**La separación `interface` / `implementation` en un solo fichero** es la misma idea que la
especificación y el cuerpo de Ada de esta página, con menos ceremonia.

Y el compilador produce un `.ppu` —el equivalente del `.mod` de Fortran— con la misma consecuencia:
**está atado a la versión del compilador**.

```text
Fatal: Can't find unit Calculos used by Programa
  (o: PPU file version mismatch)
```

Y de ahí el mecanismo más característico del ecosistema Delphi y que merece explicarse, porque es un
caso de estudio del problema de esta clase: **los paquetes en tiempo de ejecución**.

```pascal
{ Un .bpl es una DLL con clases Delphi dentro }
{$IFDEF USEPACKAGES} requires rtl, vcl, mipaquete; {$ENDIF}
```

Y su trampa histórica: **los `.bpl` incluyen el número de versión del compilador en el nombre**
—`rtl280.bpl` para Delphi 11, `rtl290.bpl` para el 12— **precisamente porque no son compatibles entre
versiones**.

Eso convirtió el ecosistema Delphi en un caso extremo de esta clase: **cada componente de terceros
tenía que publicarse recompilado para cada versión del IDE**, y actualizar de Delphi implicaba **esperar
a que todos los proveedores publicaran**.

Es la lección más clara de esta página sobre los binarios: **distribuir binarios ata al compilador; el
código fuente no**. Fortran, Pascal y C++ lo pagan; Lisp, Tcl, Perl y M no.

Y el ecosistema moderno lo resolvió por la vía del fuente:

| Herramienta | Notas |
|---|---|
| **fpmake / fppkg** | el de Free Pascal |
| **Delphinus / Boss** | gestores de la comunidad Delphi, desde git |
| **GetIt** | el mercado oficial de Embarcadero |

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let* ((linea (read-line))
       (p1 (position #\. linea))
       (p2 (position #\. linea :start (1+ p1))))
  (format t "mayor=~A menor=~A parche=~A~%"
          (subseq linea 0 p1)
          (subseq linea (1+ p1) p2)
          (string-trim '(#\Space #\Return) (subseq linea (1+ p2)))))
```

**Lo que esta clase enseña en Common Lisp.** Lisp tiene un modelo de dependencias que se deriva de la
Parte 8 y que es distinto de todo lo demás de esta página: **el sistema se carga en una imagen viva, y
la imagen es el resultado**.

```lisp
;; mi-proyecto.asd  -- ASDF: el sistema de construcción de Common Lisp
(defsystem "mi-proyecto"
  :depends-on ("alexandria" "cl-ppcre" "bordeaux-threads")
  :components ((:file "paquetes")
               (:file "utilidades" :depends-on ("paquetes"))
               (:file "principal"  :depends-on ("utilidades"))))
```

**ASDF resuelve el orden de compilación desde el grafo declarado**, igual que gprbuild en Ada, y añade
algo propio: **recompila solo lo que cambió y lo carga en la imagen actual**.

Y **Quicklisp** es la capa de distribución, con una decisión de diseño que resuelve el problema central
de esta clase de una forma que merece explicarse:

**Quicklisp no resuelve versiones. Distribuye *dists*: conjuntos completos de bibliotecas probadas
juntas.**

```lisp
(ql:quickload "hunchentoot")           ; instala lo que haga falta
(ql:dist-version "quicklisp")           ; "2024-10-12"
```

**Toda la distribución tiene una fecha, y esa fecha ES la versión.** No hay resolución de
restricciones, no hay conflictos entre versiones y no hay fichero de bloqueo: **hay un conjunto que
funciona, publicado mensualmente tras compilar y probar las mil y pico bibliotecas juntas**.

Es la segunda de las tres estrategias de esta clase, y es la misma que usan Debian estable, Stackage en
Haskell y las distribuciones de Linux enteras: **en lugar de que cada proyecto resuelva versiones, un
integrador publica un conjunto coherente**.

Ventaja: **el infierno de dependencias desaparece**. Coste: **no puedes usar la última versión de una
biblioteca si el conjunto no la ha adoptado**.

Y la tercera estrategia también aparece en Lisp, porque el lenguaje la permite: **cargar dos versiones a
la vez**, en paquetes distintos (clase 087). Los espacios de nombres separan los símbolos, así que
**`v1:procesar` y `v2:procesar` pueden coexistir en la misma imagen**.

Es lo que hace Node.js con su árbol de `node_modules`, y lo que casi ningún lenguaje compilado permite.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
lassign [split [string trim $linea] .] mayor menor parche

puts "mayor=$mayor menor=$menor parche=$parche"
```

**Lo que esta clase enseña en Tcl.** Tcl tiene el sistema de versiones de paquetes **en el núcleo del
lenguaje**, y es de 1993 — anterior a casi todo lo demás de esta página.

```tcl
package require http 2.9          ;# 2.9 o superior COMPATIBLE
package require -exact tls 1.7.16  ;# exactamente esa
package provide mipaquete 1.2       ;# lo que yo ofrezco
```

Y la regla de compatibilidad de Tcl es **el versionado semántico antes de que se llamara así**:

> `package require foo 2.9` acepta cualquier `2.x` con `x >= 9`, **pero nunca una `3.0`**.

**Un cambio de número mayor significa incompatible, y el intérprete lo aplica.** Eso está en la
documentación de Tcl desde 1993, once años antes de que Tom Preston-Werner escribiera la especificación
de SemVer.

Y el mecanismo de carga tiene una propiedad práctica que merece conocerse: **`pkgIndex.tcl`**.

```tcl
# pkgIndex.tcl -- generado por pkg_mkIndex
package ifneeded http 2.9.5 [list source [file join $dir http.tcl]]
```

**`package ifneeded` no carga: registra CÓMO cargar.** Así que el intérprete **conoce todas las versiones
disponibles sin haber leído ningún código**, y carga la que haga falta, cuando haga falta.

Es carga perezosa con resolución de versiones, en cuatro líneas de mecanismo.

Y Tcl permite lo que Lisp permitía en esta página, y con más facilidad:

```tcl
package require mipkg 1.0
namespace eval ::v2 { source mipkg2.tcl }     ;# dos versiones a la vez
```

**Los espacios de nombres aíslan** (clase 086), así que dos versiones conviven.

El ecosistema:

| Herramienta | Notas |
|---|---|
| **teapot / TEA** | repositorios de paquetes binarios y de fuentes |
| **tcllib / tklib** | la biblioteca estándar comunitaria, muy amplia |
| **starkit / starpack** | **la aplicación con TODAS sus dependencias en un fichero** |

**Starkit merece la mención final**, y la clase 144 la retoma: **empaqueta el intérprete, los paquetes y
los datos en un único ejecutable**, con un sistema de ficheros virtual dentro.

Es la respuesta más radical al problema de esta clase: **si nada se resuelve en el destino, no hay
conflicto de versiones posible**. Es lo mismo que hoy hacen los contenedores y los binarios estáticos, y
en Tcl es de 2002.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

my ($mayor, $menor, $parche) = split /\./, $linea;

print "mayor=$mayor menor=$menor parche=$parche\n";
```

**Lo que esta clase enseña en Perl.** Perl construyó **CPAN en 1995**, y es **el primer archivo de
paquetes de un lenguaje de programación** en el sentido moderno: índice central, dependencias
declaradas, instalación automática y pruebas.

Todo lo que vino después —PyPI, RubyGems, npm, Maven, crates.io— sigue el molde de CPAN.

Y CPAN tiene una institución que ningún otro ecosistema ha reproducido con la misma ambición: **CPAN
Testers**.

```text
Cada versión subida se compila y se prueba automáticamente en cientos de
combinaciones de sistema operativo, versión de Perl y arquitectura,
y los informes son públicos.
```

**Antes de instalar un módulo, se puede ver si pasa las pruebas en tu plataforma exacta.** Es control de
calidad distribuido y voluntario, funcionando desde 1998.

Y la evolución del manejo de versiones en Perl es la historia de esta clase en miniatura:

| Etapa | Herramienta | Qué aportó |
|---|---|---|
| 1995 | `CPAN.pm` | instalar con dependencias |
| 2010 | `cpanminus` (`cpanm`) | rápido, sin configuración |
| 2011 | `local::lib` | **dependencias por proyecto**, no globales |
| 2012 | `Carton` + `cpanfile` | **fichero de bloqueo**: `cpanfile.snapshot` |
| hoy | `Carmel`, `App::FatPacker` | empaquetado y despliegue |

**`cpanfile.snapshot` es un fichero de bloqueo con todo lo que esta clase defiende**: registra **la
versión exacta de cada dependencia y de cada dependencia transitiva**, con su suma de comprobación.

```perl
# cpanfile
requires 'DBI', '>= 1.640';
requires 'JSON::XS', '== 4.03';
on 'test' => sub { requires 'Test::More', '0.98'; };
```

Y Perl aporta una advertencia que esta clase debe recoger y que se aprendió con dolor: **el módulo
instalado globalmente**.

Durante años, `cpan` instalaba en el Perl del sistema, así que **actualizar un módulo para un proyecto
rompía otro** — y en algunos casos, **rompía herramientas del sistema operativo escritas en Perl**.

`local::lib` y `Carton` resolvieron eso con la solución que hoy es universal: **un árbol de
dependencias por proyecto**.

Y es una lección que se repitió en todos los ecosistemas —virtualenv en Python, bundler en Ruby,
node_modules en JavaScript— y siempre con la misma conclusión: **las dependencias son del proyecto, no
de la máquina**.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

int main() {
    std::string linea;
    if (!std::getline(std::cin, linea)) return 1;

    const auto p1 = linea.find('.');
    const auto p2 = linea.find('.', p1 + 1);

    std::cout << "mayor="  << linea.substr(0, p1)
              << " menor="  << linea.substr(p1 + 1, p2 - p1 - 1)
              << " parche=" << linea.substr(p2 + 1) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ tiene **el peor problema de dependencias de esta página**, y
merece explicarse por qué, porque es instructivo.

**Primero, `#include` es inclusión textual.** El preprocesador pega el fichero, así que **el compilador
ve millones de líneas** y **cualquier cambio en una cabecera obliga a recompilar todo lo que la
incluye**.

**Segundo, no hay ABI estándar** (clase 157). Dos bibliotecas compiladas con compiladores distintos, o
con banderas distintas, **pueden no enlazar o —peor— enlazar y fallar en ejecución**:

```text
undefined reference to `foo(std::__cxx11::basic_string<...>)'
```

**Ese `__cxx11` es el cambio de ABI de `std::string` de GCC 5 (2015)**, y partió el ecosistema de Linux
en dos durante años.

**Y tercero, no hubo gestor de paquetes durante treinta y ocho años.** El resultado:

```text
/usr/include, /usr/local/include, ./vendor/, ./third_party/,
git submodules, ExternalProject_Add, FetchContent, y "copia el .h en tu proyecto"
```

Y el ecosistema actual, que por fin funciona:

| Herramienta | Notas |
|---|---|
| **vcpkg** (Microsoft, 2016) | **compila desde fuente**; `vcpkg.json` + fichero de bloqueo |
| **Conan** (2016) | binarios con perfiles: compilador, versión, ABI, opciones |
| **CPM.cmake** | envoltorio de `FetchContent` |
| **CMake** | el estándar de facto para construir |

**Conan merece el detalle**, porque su solución al problema del ABI es la correcta: **el identificador
del paquete incluye el compilador, su versión, el estándar de C++, el tipo de biblioteca estándar y las
opciones**.

```text
zlib/1.3:6af9cc7cb931c5ad942174fd7838eb655717c709
   settings: os=Linux, compiler=gcc, compiler.version=13,
             compiler.libcxx=libstdc++11, build_type=Release
```

**Ese identificador es la respuesta a "¿este binario sirve en mi proyecto?"**, y es más honesta que un
número de versión: **la compatibilidad de C++ no depende solo de la versión de la biblioteca**.

Es la misma idea que la firma de programa de servicio de IBM i en esta página, y la misma que los
identificadores de Spack en Fortran: **cuando el binario depende del entorno, la identidad del paquete
tiene que incluir el entorno**.

Y C++20 trajo **módulos**, que atacan la raíz:

```cpp
export module geometria;
export int area(int a, int b);
```

**Un módulo se compila una vez y se importa como interfaz binaria**, sin repetir el texto — con la misma
consecuencia que el `.mod` de Fortran de esta página: **atado al compilador**. La adopción va lenta,
seis años después, precisamente por lo que cuesta encajar eso en los sistemas de construcción
existentes.

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

dcl-pi VERSION;
  v char(20) const;
end-pi;

dcl-s texto varchar(20);
dcl-s p1 int(10);
dcl-s p2 int(10);

texto = %trim(v);
p1 = %scan('.' : texto);
p2 = %scan('.' : texto : p1 + 1);

dsply ('mayor=' + %subst(texto : 1 : p1 - 1) +
       ' menor=' + %subst(texto : p1 + 1 : p2 - p1 - 1) +
       ' parche=' + %subst(texto : p2 + 1));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** Aquí está el caso que el gancho anunciaba, y es la mejor respuesta
de esta página al problema de la compatibilidad binaria: **la firma del programa de servicio**.

Un programa de servicio (clase 086) exporta procedimientos, y **IBM i calcula una firma —un valor de
16 bytes— a partir de la lista ordenada de exportaciones**. Cada programa que lo usa **guarda esa firma
dentro**.

```text
CPF3EE1 - La firma del programa de servicio UTILES no coincide
```

**Y ese error salta al ACTIVAR el programa, no al llamar a la función.** Es decir: si alguien cambia la
biblioteca de forma incompatible, **todo lo que dependía de ella se niega a arrancar** en lugar de
llamar a la función equivocada.

Compárese con C++ en esta página, donde el mismo escenario **enlaza y falla en ejecución de forma
impredecible**.

Y el mecanismo tiene una segunda mitad, que es la que lo hace usable: **el lenguaje de enlace con
niveles de firma**.

```text
STRPGMEXP PGMLVL(*CURRENT) SIGNATURE('UTILES V2')
  EXPORT SYMBOL('CALCULAR')
  EXPORT SYMBOL('VALIDAR')
  EXPORT SYMBOL('FORMATEAR')      /* nuevo en V2: SE AÑADE AL FINAL */
ENDPGMEXP

STRPGMEXP PGMLVL(*PRV) SIGNATURE('UTILES V1')      /* la firma ANTERIOR */
  EXPORT SYMBOL('CALCULAR')
  EXPORT SYMBOL('VALIDAR')
ENDPGMEXP
```

**Un programa de servicio puede declarar varias firmas a la vez**, así que **los clientes viejos siguen
funcionando y los nuevos ven las funciones nuevas**.

Eso es **compatibilidad hacia atrás explícita y verificada**, y es exactamente lo que el versionado
semántico intenta expresar con un número — pero **comprobado por el sistema en lugar de prometido por
el autor**.

Y la regla operativa que se deriva, y que es transferible a cualquier biblioteca compartida: **añade
siempre al final, nunca reordenes ni quites**. Es la misma regla que rige los campos de Protocol Buffers
y las tablas de métodos virtuales de C++, y aquí el sistema la hace cumplir.

Es, con diferencia, el modelo de compatibilidad más riguroso de esta página, y es de 1988.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 version: procedure options(main);

    declare linea  char(40) varying;
    declare (p1, p2) fixed binary(31);

    get edit (linea) (a(40));
    linea = trim(linea);

    p1 = index(linea, '.');
    p2 = index(substr(linea, p1 + 1), '.') + p1;

    put skip list ('mayor=' || substr(linea, 1, p1 - 1) ||
                   ' menor=' || substr(linea, p1 + 1, p2 - p1 - 1) ||
                   ' parche=' || substr(linea, p2 + 1));

 end version;
```

**Lo que esta clase enseña en PL/I.** PL/I comparte con COBOL el modelo de esta página —**`%INCLUDE` es
inclusión textual y la gestión la hace el sistema de configuración**, no el lenguaje— y aporta una
distinción que merece explicarse porque es directamente el tema de la clase.

```pli
 %include estructuras;          /* inclusión textual, como COPY */

 declare calcular entry (fixed binary(31)) returns (fixed binary(31))
         external;               /* una DEPENDENCIA DE ENLACE, con su tipo */
```

**La segunda forma declara el tipo de la función externa**, así que **el compilador comprueba las
llamadas** — cosa que C no hacía hasta los prototipos de 1989 y que COBOL no hace nunca.

Y el enlazador de z/OS resuelve el resto, con dos modos que definen el despliegue de estos sistemas:

**Enlace estático**: el código de la subrutina se copia dentro del módulo de carga. **Cambiarla obliga a
reenlazar todo lo que la usa** — el problema de esta clase en su forma clásica.

**Y enlace dinámico con `FETCH`**:

```pli
 fetch calcular;                /* cargar el módulo AHORA */
 call calcular(x);
 release calcular;               /* y descargarlo */
```

**`FETCH` carga un módulo por nombre en tiempo de ejecución**, así que **la nueva versión se despliega
sustituyendo el módulo, sin tocar los llamadores**.

Es la carga dinámica de bibliotecas, y en PL/I es una sentencia del lenguaje, no una llamada al sistema
operativo.

Y hay un detalle sobre versiones en z/OS que conviene conocer porque resuelve el problema de forma
distinta a todo lo demás de esta página: **la concatenación de bibliotecas**.

```jcl
//STEPLIB  DD DSN=MI.PRUEBAS.LOADLIB,DISP=SHR
//         DD DSN=SISTEMA.PROD.LOADLIB,DISP=SHR
```

**El sistema busca el módulo en orden**, así que **poner una biblioteca delante sustituye versiones sin
tocar nada**.

Es exactamente la lista de bibliotecas de IBM i (clase 139) y exactamente el `PATH` de un sistema Unix:
**resolución por orden de búsqueda en lugar de por número de versión**.

Y tiene la virtud de esta clase llevada al extremo: **la vuelta atrás es quitar una línea del JCL**.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
VERSION ; Partir una version -- clase 143
 read linea
 write "mayor=", $piece(linea, ".", 1)
 write " menor=", $piece(linea, ".", 2)
 write " parche=", $piece(linea, ".", 3), !
 quit
```

**Lo que esta clase enseña en M.** `$piece` con `.` como delimitador resuelve el programa en tres
llamadas, y es el operador que define el manejo de texto en M (clase 093).

Y sobre dependencias, M tiene el modelo más distinto de esta página, porque **el código vive en la base
de datos, no en ficheros** (clase 123).

Una rutina M es una entrada más del sistema, y **una llamada `do CALCULAR^UTILES` se resuelve por nombre
en el momento de ejecutarse**. No hay enlace, no hay compilación previa obligatoria y **no hay
versiones**: hay **la rutina `UTILES` que esté cargada**.

Eso significa que **el problema de esta clase no existe dentro de un sistema M** —solo hay una versión de
todo— y que **el problema entero se traslada al despliegue**.

Y la comunidad VistA construyó para eso una pieza de ingeniería considerable que merece conocerse:
**KIDS, el *Kernel Installation and Distribution System***.

Un paquete KIDS es **una global** que contiene:

- **Las rutinas** a instalar, como texto.
- **Las definiciones de ficheros** de FileMan y sus cambios de estructura.
- **Los requisitos previos**: qué parches deben estar ya instalados, con sus números.
- **El código de instalación previa y posterior**, que puede migrar datos.
- **Y las comprobaciones de entorno**.

```text
Parche XU*8.0*655
  Requiere: XU*8.0*640, XU*8.0*651
```

**Ese "requiere" con números de parche es la resolución de dependencias**, y el instalador **se niega a
instalar fuera de orden**.

Es exactamente lo que hace `apt` o `yum` con los paquetes de un sistema operativo, construido para un
lenguaje sin ficheros y desplegado en cientos de hospitales.

Y hay un detalle que ilustra bien la diferencia de modelo: **la instalación es transaccional y en
caliente**. El paquete se carga en globals, se verifica, y **la sustitución de rutinas ocurre con el
sistema funcionando** — porque una rutina es un dato y sustituirla es una escritura.

En un hospital que no puede pararse, esa propiedad no es una comodidad: **es el requisito**.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| linea partes |

linea := stdin nextLine trimBoth.
partes := linea substrings: '.'.

Transcript
    show: 'mayor=',   (partes at: 1);
    show: ' menor=',  (partes at: 2);
    show: ' parche=', (partes at: 3);
    cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk tiene el problema de esta clase en su forma más
peculiar, y viene de la Parte 8: **la unidad de despliegue es la imagen entera**.

Una imagen es un fichero con **todos los objetos del sistema**, incluidas todas las clases de todas las
bibliotecas. No hay ficheros de biblioteca, no hay enlace y no hay carga de módulos: **hay clases que
están en la imagen o no están**.

Y de ahí sale la pregunta que la comunidad tuvo que resolver: **¿cómo se controla la versión de algo que
no son ficheros?**

La respuesta llegó en dos capas, y son de las herramientas más interesantes de esta página:

**Monticello (2003)**, el control de versiones de código Smalltalk:

```text
Un paquete no es un fichero: es un CONJUNTO DE MÉTODOS Y CLASES.
Monticello guarda versiones de ese conjunto, con ancestros y fusiones,
y compara a nivel de MÉTODO, no de línea.
```

**Comparar dos versiones da la lista de métodos añadidos, quitados y cambiados** — no un diff de texto.
Es control de versiones semántico, y resuelve de raíz el problema que la clase 145 detallará: **el ruido
del diff textual**.

**Y Metacello (2010)**, la gestión de dependencias sobre eso:

```smalltalk
Metacello new
    baseline: 'MiProyecto';
    repository: 'github://usuario/proyecto:v1.2.3/src';
    load.
```

```smalltalk
spec baseline: 'Seaside3' with: [ spec repository: 'github://...' ];
     project: 'Zinc' with: [ spec versionString: '2.4.5' ].
```

**Metacello distingue *baseline* —qué depende de qué— de *version* —qué versiones concretas—**, que es
exactamente la distinción entre el fichero de dependencias y el de bloqueo de esta clase.

Y Smalltalk añade una capacidad que ningún otro de esta página tiene: **la imagen guardada es un fichero
de bloqueo perfecto**.

```smalltalk
Smalltalk snapshot: true andQuit: true.
```

**Guardar la imagen congela el estado exacto de todo el código y todos los objetos.** Al reabrirla,
**no hay nada que resolver, nada que descargar y nada que compilar**: el sistema está tal cual estaba.

Es la forma más fuerte de reproducibilidad de esta página, y la clase 144 la retoma — con su coste
correspondiente: **una imagen son decenas o cientos de megabytes, y es opaca**.

Es el mismo compromiso que los contenedores plantearon cuarenta años después, con la misma discusión.

---

## Y de vuelta a la clase

Lo transferible: **una versión es una promesa sobre la compatibilidad, y una promesa no es una
garantía**. El versionado semántico funciona en la medida en que los autores lo respeten, y por eso
existe el fichero de bloqueo: **no dice qué versiones son compatibles, dice cuáles se probaron**. La
disciplina que hay que llevarse es doble: **fijar versiones exactas para desplegar** y **actualizarlas
deliberadamente, no por accidente** — y saber que la alternativa que casi nadie considera, **tener menos
dependencias**, sigue siendo la que mejor funciona.

⏮️ [Volver a la clase 143](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
