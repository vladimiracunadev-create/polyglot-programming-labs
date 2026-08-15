# -*- coding: utf-8 -*-
"""Parte 9, lote B — clases 143 a 146. Ver `vivos_parte9.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 143 — Dependencias, versiones y ficheros de bloqueo
# ---------------------------------------------------------------------------
SPECS["143"] = dict(
    gancho="""
Partir `1.2.3` en mayor, menor y parche. Detrás de ese formato de tres números está el contrato social
más importante de la ingeniería de software moderna —**el versionado semántico**— y esta página muestra
que **no es moderno en absoluto**: IBM i lleva desde 1988 comprobando compatibilidad de bibliotecas con
una **firma criptográfica calculada sobre la lista de exportaciones**, que es más fuerte que cualquier
número de versión.
""",
    porque="""
Aquí el concepto es la **dependencia entre unidades de software y su compatibilidad**, y estos
lenguajes lo enseñan porque **casi ninguno tuvo un gestor de paquetes durante décadas** y tuvieron que
resolverlo de otras maneras: la copia de fuentes (COBOL), el fichero de módulo atado al compilador
(Fortran), la firma del objeto (RPG), la imagen entera como unidad (Lisp y Smalltalk).

Y aparece el problema que ningún gestor de paquetes ha resuelto del todo: **el infierno de las
dependencias** —dos bibliotecas que exigen versiones incompatibles de una tercera— y las tres estrategias
para vivir con él.
""",
    cierre="""
Lo transferible: **una versión es una promesa sobre la compatibilidad, y una promesa no es una
garantía**. El versionado semántico funciona en la medida en que los autores lo respeten, y por eso
existe el fichero de bloqueo: **no dice qué versiones son compatibles, dice cuáles se probaron**. La
disciplina que hay que llevarse es doble: **fijar versiones exactas para desplegar** y **actualizarlas
deliberadamente, no por accidente** — y saber que la alternativa que casi nadie considera, **tener menos
dependencias**, sigue siendo la que mejor funciona.
""",
    langs={
        "cobol": ("""
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
""", """
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
"""),
        "fortran": ("""
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
""", """
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
"""),
        "ada": ("""
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
""", """
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
"""),
        "pascal": ("""
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
""", """
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
"""),
        "lisp": ("""
(let* ((linea (read-line))
       (p1 (position #\\. linea))
       (p2 (position #\\. linea :start (1+ p1))))
  (format t "mayor=~A menor=~A parche=~A~%"
          (subseq linea 0 p1)
          (subseq linea (1+ p1) p2)
          (string-trim '(#\\Space #\\Return) (subseq linea (1+ p2)))))
""", """
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
"""),
        "tcl": ("""
gets stdin linea
lassign [split [string trim $linea] .] mayor menor parche

puts "mayor=$mayor menor=$menor parche=$parche"
""", """
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
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

my ($mayor, $menor, $parche) = split /\\./, $linea;

print "mayor=$mayor menor=$menor parche=$parche\\n";
""", """
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
"""),
        "cpp": ("""
#include <iostream>
#include <string>

int main() {
    std::string linea;
    if (!std::getline(std::cin, linea)) return 1;

    const auto p1 = linea.find('.');
    const auto p2 = linea.find('.', p1 + 1);

    std::cout << "mayor="  << linea.substr(0, p1)
              << " menor="  << linea.substr(p1 + 1, p2 - p1 - 1)
              << " parche=" << linea.substr(p2 + 1) << '\\n';
    return 0;
}
""", """
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
"""),
        "rpg": ("""
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
""", """
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
"""),
        "pli": ("""
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
""", """
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
"""),
        "mumps": ("""
VERSION ; Partir una version -- clase 143
 read linea
 write "mayor=", $piece(linea, ".", 1)
 write " menor=", $piece(linea, ".", 2)
 write " parche=", $piece(linea, ".", 3), !
 quit
""", """
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
"""),
        "smalltalk": ("""
| linea partes |

linea := stdin nextLine trimBoth.
partes := linea substrings: '.'.

Transcript
    show: 'mayor=',   (partes at: 1);
    show: ' menor=',  (partes at: 2);
    show: ' parche=', (partes at: 3);
    cr.
""", """
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
"""),
    },
)

# ---------------------------------------------------------------------------
# 144 — Compilación reproducible y empaquetado
# ---------------------------------------------------------------------------
SPECS["144"] = dict(
    gancho="""
Una suma de comprobación: sumar los enteros de una línea. Es el ejemplo mínimo de la idea que sostiene
esta clase — **reducir algo grande a un número que permite decir "esto es exactamente lo mismo"**. Y la
pregunta que la clase persigue es incómoda: **si compilas el mismo código dos veces, ¿sale el mismo
binario?** La respuesta por defecto, en casi todos los lenguajes de esta página, es **no** — y las
razones son sorprendentes.
""",
    porque="""
Aquí el concepto es la **reproducibilidad de la construcción**, y estos lenguajes lo enseñan porque
cubren todas las respuestas posibles. **COBOL y PL/I en z/OS producen módulos de carga con marcas de
tiempo dentro.** **Fortran y Pascal generan ficheros intermedios atados al compilador.** **Tcl y Lisp
empaquetan el intérprete entero.** **Y Smalltalk lleva la idea al extremo: el artefacto es la imagen.**

Y el motivo por el que esto importa hoy tiene nombre: **la cadena de suministro**. Si dos personas
compilan el mismo fuente y obtienen binarios distintos, **no hay forma de verificar que el binario
publicado viene del fuente publicado**.
""",
    cierre="""
Lo transferible: **una construcción reproducible convierte un binario en algo verificable**. Cualquiera
puede recompilar y comprobar que le sale lo mismo, y eso cierra la puerta al ataque más difícil de
detectar de todos: **modificar el compilador o la máquina de construcción en lugar del código**. Las
tres fuentes de irreproducibilidad son siempre las mismas —**tiempo, rutas y orden**— y las tres tienen
solución conocida. La disciplina que hay que llevarse: **fijar la versión de todo lo que participa en la
construcción**, porque la reproducibilidad no es una propiedad del código, es una propiedad del
entorno.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. SUMA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  I       PIC 9(4) COMP.
01  C       PIC X.
01  NUM     PIC S9(9) COMP VALUE 0.
01  TOTAL   PIC S9(9) COMP VALUE 0.
01  ENNUM   PIC 9      VALUE 0.
01  ED      PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        MOVE LINEA(I:1) TO C
        IF C IS NUMERIC
            COMPUTE NUM = NUM * 10 + FUNCTION NUMVAL(C)
            MOVE 1 TO ENNUM
        ELSE
            IF ENNUM = 1
                COMPUTE TOTAL = TOTAL + NUM
                MOVE 0 TO NUM
                MOVE 0 TO ENNUM
            END-IF
        END-IF
    END-PERFORM

    MOVE TOTAL TO ED
    DISPLAY "checksum=" FUNCTION TRIM(ED)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** El programa recorre la línea carácter a carácter con
`LINEA(I:1)` —**modificación de referencia**, la forma de COBOL de tomar una subcadena— y usa la
condición de clase `IS NUMERIC`, que es una comprobación integrada en el lenguaje.

Y sobre reproducibilidad, el mundo mainframe tiene una respuesta que merece explicarse porque llegó por
un camino distinto al de la industria libre: **la auditoría**.

En un banco, **hay que poder demostrar qué versión del fuente produjo el módulo que está en
producción**, y eso es un requisito regulatorio, no técnico.

La solución no fue hacer la compilación determinista, sino **registrar la construcción**:

```text
Endevor / ChangeMan guardan, por cada módulo desplegado:
  - el fuente exacto, con su número de versión
  - las opciones de compilación usadas
  - las versiones de todos los copybooks incluidos
  - quién lo compiló, cuándo y con qué autorización
  - y el listado de compilación completo
```

**Eso es una lista de materiales del software** —lo que hoy se llama SBOM— **de los años ochenta**, y
resuelve el mismo problema por otra vía: **si no puedes reproducir el binario, conserva la prueba de
cómo se hizo**.

Y el módulo de carga de z/OS ayuda, porque **lleva metadatos dentro**:

```text
IDENTIFY  MIPGM('COMPILADO 2024-03-15 POR JSMITH V2.4')
```

**El enlazador puede grabar identificadores en el módulo**, y `AMBLIST` los muestra después. Es
información de procedencia embebida en el artefacto.

Y en el lado libre, GnuCOBOL sí permite la construcción determinista con las mismas técnicas que C:

```bash
export SOURCE_DATE_EPOCH=1700000000
cobc -x -free -ffile-prefix-map=$PWD=. prog.cob
sha256sum prog
```

Y merece señalar la fuente de irreproducibilidad más específica de COBOL, porque es la de esta página:
**el copybook**. Dos compilaciones del mismo programa **con distintas versiones de un copybook producen
binarios distintos**, y el fuente del programa no cambió.

Es la razón por la que la lista de materiales de un módulo COBOL tiene que incluir **todos los
copybooks con su versión** — que es exactamente lo que Endevor registra.
"""),
        "fortran": ("""
program suma
   implicit none
   character(len=200) :: linea
   integer :: total, valor, ios, pos

   read(*, '(A)') linea
   total = 0
   pos = 1

   do
      read(linea(pos:), *, iostat=ios) valor
      if (ios /= 0) exit
      total = total + valor
      pos = pos + index(linea(pos:), ' ')
      if (pos > len_trim(linea)) exit
   end do

   write(*, '(A,I0)') 'checksum=', total
end program suma
""", """
**Lo que esta clase enseña en Fortran.** El programa usa **lectura interna** —`read` desde una cadena— y
avanza con `index`, que es la forma clásica de tokenizar en Fortran sin bibliotecas.

Y sobre reproducibilidad, Fortran tiene el caso más difícil de esta página, y por dos motivos distintos
que conviene separar.

**El primero es el de todos: el binario.** Fuentes de irreproducibilidad conocidas:

```bash
gfortran -ffile-prefix-map=$PWD=.      # rutas absolutas dentro del binario
export SOURCE_DATE_EPOCH=1700000000     # marcas de tiempo
gfortran -frandom-seed=0                 # ¡el generador de símbolos internos!
```

**`-frandom-seed` es específico de Fortran y sorprende**: gfortran genera nombres internos con un
componente aleatorio, así que **dos compilaciones producen símbolos distintos** salvo que se fije la
semilla.

**Y el segundo es propio del dominio y más profundo: la reproducibilidad del RESULTADO.**

Como la clase 140 explicó, **el mismo programa da números distintos según el compilador, las
optimizaciones, el número de hilos y hasta el modelo de procesador**.

```bash
gfortran -O2 -march=native      # ¡usa las instrucciones de ESTA máquina!
```

**`-march=native` es la trampa clásica**: produce un binario que **no funciona en otra máquina** y que
**da otros números en la que sí funciona**. Es cómodo para un cálculo propio y desastroso para
distribuir.

Y de ahí las herramientas del ecosistema:

| Herramienta | Qué aporta |
|---|---|
| **Spack** | compila con un identificador que incluye compilador, versión, opciones y arquitectura |
| **EasyBuild** | recetas reproducibles para clústeres |
| **`environment modules`** | fijar la versión de compilador y bibliotecas por sesión |
| **contenedores** | Singularity/Apptainer: la imagen entera, para HPC |

**Spack merece la explicación** porque su modelo es el correcto para el problema de esta página: **el
identificador de un paquete instalado es un valor calculado sobre toda su configuración**.

```text
zlib@1.3.1%gcc@13.2.0+optimize+pic+shared arch=linux-ubuntu22.04-zen3
     ^^^^^^^^^^^^ hash: 5rk3nlv...
```

**Dos configuraciones distintas son dos instalaciones distintas, coexistiendo.** Es la respuesta al
problema del `.mod` de la clase 143, y es lo mismo que hace Nix.

Y la conclusión de esta clase para el cálculo científico es una que la comunidad tardó en aceptar: **un
artículo que publica resultados numéricos sin publicar el contenedor o el `spack.lock` no es
reproducible**, aunque publique el código.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Suma is
   Total, Valor : Integer := 0;
begin
   Total := 0;
   loop
      begin
         Get (Valor);
         Total := Total + Valor;
      exception
         when others => exit;
      end;
   end loop;

   Put ("checksum=");
   Put (Total, Width => 1);
   New_Line;
end Suma;
""", """
**Lo que esta clase enseña en Ada.** El programa lee enteros hasta que falla, capturando la excepción de
fin de fichero — que es el idioma de Ada para "leer hasta que se acabe" (clase 116).

Y sobre reproducibilidad, Ada parte de una ventaja estructural sobre C++ y Fortran, y es la de la clase
143: **el compilador conoce el grafo completo de dependencias**, así que **la construcción es determinista
en su orden**.

Y `gprbuild` lo formaliza:

```ada
project Mi_Proyecto is
   for Source_Dirs use ("src");
   for Object_Dir use "obj";
   package Compiler is
      for Default_Switches ("Ada") use ("-O2", "-gnatwa", "-gnat2022");
   end Compiler;
end Mi_Proyecto;
```

**El fichero de proyecto declara las opciones exactas**, así que **no dependen de quién teclea el
comando** — que es una de las tres fuentes de irreproducibilidad del cierre de esta clase.

Y hay una capacidad de Ada que es directamente el tema de esta página y que ningún otro lenguaje de la
lista tiene igual: **la certificación de la cadena de herramientas**.

En aviación y ferrocarril, **el compilador mismo tiene que estar cualificado**:

```text
DO-330 / DO-178C: Tool Qualification
  - se demuestra que el compilador traduce correctamente
  - se congela su versión EXACTA para todo el proyecto
  - y cualquier cambio obliga a repetir la cualificación
```

**Congelar la versión del compilador durante los diez o veinte años de vida del programa** es la norma
en estos sectores, y es la aplicación más estricta de la regla del cierre de esta clase: **la
reproducibilidad es una propiedad del entorno**.

Y de ahí una práctica que merece conocerse: **se archiva la máquina de construcción entera**, a veces
como imagen de disco, a veces como hardware físico guardado.

Y AdaCore da las herramientas para verificar el resultado:

```bash
gnatcheck        # reglas de codificación
gnatmetric        # métricas del fuente
gnatstub / gnattest
gnatcoverage       # cobertura sin instrumentar, sobre el binario FINAL
```

**`gnatcoverage` sin instrumentar es lo relevante para esta clase**: mide la cobertura **del binario que
se va a desplegar**, no de una versión modificada.

Es una diferencia que importa cuando hay que certificar, porque **lo que se prueba y lo que se despliega
tienen que ser el mismo objeto** — y en la mayoría de los ecosistemas no lo son.
"""),
        "pascal": ("""
program Suma;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, Tok: string;
  I, Total: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea) + ' ';
  Total := 0;
  Tok := '';

  for I := 1 to Length(Linea) do
    if Linea[I] = ' ' then
    begin
      if Tok <> '' then Total := Total + StrToInt(Tok);
      Tok := '';
    end
    else
      Tok := Tok + Linea[I];

  WriteLn('checksum=', IntToStr(Total));
end.
""", """
**Lo que esta clase enseña en Pascal.** El programa acumula el número en `Tok` y lo convierte al llegar
al separador — el tokenizador manual de toda la vida, sin depender de bibliotecas.

Y sobre empaquetado, Pascal tiene una virtud que define su ecosistema y que merece destacarse: **el
ejecutable de Pascal es autocontenido y pequeño**.

```bash
fpc -O2 -XX -Xs prog.pas       # -XX: enlace inteligente; -Xs: quitar símbolos
ls -l prog                      # unos pocos cientos de KB, sin dependencias
```

**`-XX` es el enlace inteligente**: el compilador coloca cada función en una sección propia y **el
enlazador descarta las que no se usan**. El resultado es un binario que incluye **solo lo que hace
falta** de la biblioteca estándar.

Eso, más el hecho de que la biblioteca de tiempo de ejecución de Pascal sea pequeña, da lo que Turbo
Pascal hizo famoso: **un `.exe` de 30 KB que funciona en cualquier máquina, sin instalar nada**.

Es exactamente lo que hoy se busca con los binarios estáticos de Go y Rust, y era la norma en 1987.

Y sobre reproducibilidad:

```bash
fpc -B prog.pas            # -B: reconstruir TODO, sin usar .ppu previos
```

**`-B` es importante para esta clase**: sin él, el compilador reutiliza los `.ppu` existentes, y **una
construcción incremental puede mezclar objetos de estados distintos del código**.

Es el mismo problema del `make` sin dependencias correctas, y es la razón por la que las construcciones
de publicación se hacen siempre **desde cero, en un directorio limpio**.

Y hay una fuente de irreproducibilidad específica de Pascal que conviene conocer:

```pascal
{$I %DATE%}     { la fecha de compilación, INSERTADA en el binario }
{$I %TIME%}
{$I %FPCVERSION%}
```

**Esas directivas insertan la fecha y la hora en el ejecutable**, y son de uso muy extendido para
mostrar la versión en el "Acerca de". Y hacen imposible la reproducibilidad bit a bit.

La solución es la de toda esta clase: **sustituirlas por un valor derivado del control de versiones** —el
identificador del *commit*, que es determinista— en lugar del reloj.

Es un ejemplo pequeño y muy representativo del tipo de decisión que hay que revisar: **cualquier cosa
que lea el reloj durante la construcción rompe la reproducibilidad**.
"""),
        "lisp": ("""
(let ((total 0))
  (with-input-from-string (s (read-line))
    (loop for valor = (read s nil nil)
          while valor
          do (incf total valor)))
  (format t "checksum=~D~%" total))
""", """
**Lo que esta clase enseña en Common Lisp.** El programa usa `with-input-from-string` para leer números
de una cadena con el propio lector del lenguaje — que es lo natural en Lisp: **el analizador ya existe**
(clase 123).

Y sobre empaquetado, Lisp tiene la respuesta más peculiar de esta página, y es directamente la del
modelo de la Parte 8:

```lisp
(sb-ext:save-lisp-and-die "miapp"
                          :executable t
                          :toplevel #'main
                          :compression t)
```

**`save-lisp-and-die` vuelca el estado completo del sistema a un fichero ejecutable.** Dentro va **el
compilador, el depurador, el recolector, todas las bibliotecas cargadas y todos los objetos que
existían en ese momento**.

Y eso tiene consecuencias que definen el compromiso de esta clase:

**A favor:**

- **Arranque instantáneo**: no hay que cargar ni compilar nada; el estado ya está construido.
- **Cero dependencias en el destino**: es un fichero.
- **Y se pueden precalcular tablas, cachés e índices** antes de guardar, y **estarán ahí al arrancar**.

**En contra:**

- **Decenas de megabytes**, aunque la compresión ayuda.
- **Y es opaco**: lo que hay dentro es lo que había en la imagen, incluida cualquier cosa que se cargara
  por accidente.

Ese último punto es la advertencia práctica de esta explicación: **una imagen guardada desde una sesión
interactiva puede contener variables sueltas, credenciales tecleadas en el REPL o estado de pruebas**.

De ahí la regla del ecosistema: **la imagen de publicación se construye desde un proceso limpio y con un
guion**, nunca desde la sesión donde se estuvo trabajando.

```bash
sbcl --non-interactive --load construir.lisp
```

Y sobre reproducibilidad, Lisp tiene una ventaja y una desventaja concretas:

**A favor**, Quicklisp con `dist-version` fija (clase 143) da un conjunto de dependencias determinista, y
existe `qlot` para bloquear versiones por proyecto.

**En contra**, **las tablas de dispersión y los conjuntos no tienen orden garantizado**, así que
cualquier código que genere salida recorriendo una tabla **puede producir órdenes distintos entre
ejecuciones**.

Es la tercera fuente de irreproducibilidad del cierre de esta clase —**el orden**— y aparece en todos los
lenguajes con tablas de dispersión. La solución es siempre la misma: **ordenar explícitamente antes de
emitir**.
"""),
        "tcl": ("""
gets stdin linea

set total 0
foreach v [split [string trim $linea]] {
    if {$v ne ""} { incr total $v }
}

puts "checksum=$total"
""", """
**Lo que esta clase enseña en Tcl.** Tcl inventó, en 2002, la solución al empaquetado que hoy se
considera moderna: **el Starkit**.

```bash
sdx wrap miapp.kit              # empaqueta la aplicación
sdx wrap miapp.exe -runtime tclkit-win32.exe    # ...con el intérprete dentro
```

Y lo que hay dentro merece explicarse, porque la idea es elegante:

**Un Starkit es un fichero que contiene un sistema de ficheros virtual completo** —**Metakit** o
**VFS**— con el código, los paquetes, las imágenes, la documentación y los datos.

Y el intérprete **lo monta como un directorio** al arrancar:

```tcl
source [file join $starkit::topdir lib app-miapp miapp.tcl]
```

**El programa cree que está leyendo ficheros normales**, y en realidad están dentro del ejecutable.

Un **Starpack** añade el intérprete al principio del fichero, y el resultado es **un único ejecutable
sin dependencias**, para Windows, Linux o macOS.

Eso es, exactamente, lo que hoy hacen AppImage, los ejecutables de PyInstaller, los binarios únicos de
Node y Deno, y en buena medida los contenedores. **En Tcl es de hace más de veinte años.**

Y hay una propiedad del Starkit que sigue siendo poco común y que merece señalarse: **el sistema de
ficheros virtual es de lectura y escritura**.

**Una aplicación puede escribir dentro de su propio Starkit** —configuración, complementos, datos—, y el
fichero se actualiza solo. Es una aplicación que se autocontiene por completo, incluidos sus datos.

Y sobre reproducibilidad, Tcl está en el lado fácil de esta página por la razón de la clase 143:
**distribuye fuente, no binarios**. El único binario es el intérprete, que se descarga precompilado y
verificable.

La irreproducibilidad que sí aparece es la del orden:

```tcl
foreach k [array names datos] { ... }         ;# ORDEN ARBITRARIO
foreach k [lsort [array names datos]] { ... }  ;# determinista
```

**`array names` no garantiza orden**, porque es una tabla de dispersión. Es la misma advertencia que en
Lisp en esta página, y la misma solución: **ordenar antes de emitir**.

Y el detalle que lo hace crítico aquí: **un Starkit construido recorriendo un directorio sin ordenar
produce ficheros distintos en cada construcción**, aunque el contenido sea idéntico.
"""),
        "perl": ("""
use strict;
use warnings;
use List::Util qw(sum0);

my $linea = <STDIN>;
chomp $linea;

print "checksum=", sum0(split ' ', $linea), "\\n";
""", """
**Lo que esta clase enseña en Perl.** `sum0` de `List::Util` suma una lista devolviendo 0 si está vacía
—el `sum` a secas devuelve `undef`—, y es un detalle representativo de una biblioteca estándar pensada
por gente que se había quemado.

Y sobre empaquetado, Perl tiene tres soluciones que cubren tres escenarios distintos y que merecen
conocerse:

**Primera, `App::FatPacker`**, para guiones:

```bash
fatpack pack script.pl > script-empaquetado.pl
```

**Mete todos los módulos puros de Perl dentro del propio guion**, en una sección de datos, y el guion
los carga desde ahí. El resultado es **un solo fichero `.pl` que funciona en cualquier Perl**, sin
instalar nada.

**Segunda, `PAR::Packer`**, para aplicaciones:

```bash
pp -o miapp.exe script.pl
```

**Empaqueta el intérprete, los módulos —incluidos los compilados en C— y los datos en un ejecutable**.
Es el equivalente exacto del Starpack de Tcl en esta página.

**Y tercera, `Carton` con `cpanfile.snapshot`** (clase 143), para servidores: **se despliega el árbol de
dependencias exacto**, verificado por suma de comprobación.

Y Perl aporta a esta clase una advertencia sobre reproducibilidad que es más importante de lo que
parece, y es la tercera fuente del cierre: **el orden de las claves de una tabla de dispersión es
deliberadamente aleatorio**.

```perl
for my $k (keys %datos) { ... }            # ORDEN DISTINTO EN CADA EJECUCIÓN
for my $k (sort keys %datos) { ... }        # determinista
```

**Desde Perl 5.18 (2013), el orden cambia entre ejecuciones del mismo programa**, y no por descuido: es
una medida de seguridad contra **los ataques de colisión de dispersión**, en los que un atacante envía
claves elegidas para degradar la tabla a una lista y consumir la CPU del servidor.

Perl añadió una semilla aleatoria por proceso, y **eso rompió muchísimo código que dependía sin saberlo
del orden**.

Es una lección doble y muy transferible:

**Una, sobre reproducibilidad**: **nunca dependas de un orden que no está garantizado**, porque el día
que cambie no habrá aviso.

**Y otra, sobre seguridad** (clase 153): **una estructura de datos puede ser un vector de ataque**, y la
defensa —aleatorizar— puede romper suposiciones que nadie escribió.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    long long total = 0, valor = 0;
    while (std::cin >> valor) total += valor;

    std::cout << "checksum=" << total << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ es el lenguaje donde el movimiento de las construcciones
reproducibles nació y donde más trabajo ha costado, y merece contar por qué.

**El problema, en concreto**: compilar dos veces el mismo fuente producía binarios distintos por
razones tontas pero reales.

| Causa | Solución |
|---|---|
| `__DATE__` y `__TIME__` en el binario | `SOURCE_DATE_EPOCH` |
| **Rutas absolutas** en la información de depuración | `-ffile-prefix-map=$PWD=.` |
| **Orden de los ficheros** al enlazar | ordenar la lista explícitamente |
| **Orden de lectura del directorio** | ordenar; no confiar en `readdir` |
| Marcas de tiempo en los `.a` | `ar D` (determinista), por defecto hoy |
| **Rutas en `__FILE__`** (assert, logs) | `-fmacro-prefix-map` |
| Símbolos de plantillas en orden variable | fijar el orden de las unidades |
| **Paralelismo del enlazador** | `--sort-section=name`, LTO determinista |

**El proyecto *Reproducible Builds*** (2013, nacido en Debian) recorrió esa lista para **decenas de miles
de paquetes**, y hoy **más del 90 % de Debian se compila de forma reproducible**.

Y la razón por la que ese esfuerzo importa merece explicarse, porque es el argumento central de esta
clase:

**Ken Thompson lo planteó en 1984, en "Reflections on Trusting Trust"**: se puede modificar un
compilador para que **inserte una puerta trasera al compilar un programa concreto**, y para que
**inserte esa misma modificación al compilarse a sí mismo** — de modo que **la puerta trasera no aparece
en ningún código fuente**.

**Las construcciones reproducibles son la defensa práctica contra eso**: si varias personas
independientes compilan el mismo fuente con sus propias herramientas y obtienen **exactamente el mismo
binario**, hay evidencia fuerte de que ese binario viene de ese fuente.

Y el ataque no es teórico: **SolarWinds (2020)** fue exactamente eso —**comprometer la máquina de
construcción, no el repositorio**— y afectó a decenas de miles de organizaciones.

Las herramientas del ecosistema hoy:

```bash
diffoscope binario1 binario2     # QUÉ difiere entre dos binarios, recursivamente
strip-nondeterminism              # limpiar marcas de tiempo de los artefactos
cosign / in-toto / SLSA            # firmar y atestiguar la procedencia
```

**`diffoscope` merece la mención final** porque es una herramienta sorprendentemente buena: **desempaqueta
recursivamente** —archivos dentro de paquetes dentro de imágenes— y **desensambla, descomprime y compara
metadatos** hasta encontrar el byte que cambió y explicar por qué.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi SUMA;
  linea char(200) const;
end-pi;

dcl-s texto varchar(200);
dcl-s pos   int(10);
dcl-s total int(20);

texto = %trim(linea) + ' ';
total = 0;

dow %len(%trim(texto)) > 0;
  pos = %scan(' ' : texto);
  if pos = 0;
    leave;
  endif;
  if pos > 1;
    total += %int(%subst(texto : 1 : pos - 1));
  endif;
  texto = %trim(%subst(texto : pos + 1));
enddo;

dsply ('checksum=' + %char(total));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** IBM i tiene, para el empaquetado, un formato propio que resuelve el
problema de esta clase de una forma que merece conocerse: **el fichero de salvado**.

```text
CRTSAVF FILE(QGPL/ENTREGA)
SAVOBJ OBJ(*ALL) LIB(MIAPP) DEV(*SAVF) SAVF(QGPL/ENTREGA)
```

**Un fichero de salvado contiene objetos completos** —programas, tablas, áreas de datos, colas— **con
todos sus metadatos**: propietario, autoridades, descripción, fecha de creación, **la vista de
depuración** (clase 141) y **la información de qué fuente lo creó**.

Y esa última parte es directamente el tema de esta clase:

```text
DSPOBJD OBJ(MIAPP/MIPGM) OBJTYPE(*PGM) DETAIL(*SERVICE)
   Fuente ......... : MIAPP/QRPGLESRC(MIPGM)
   Fecha del fuente : 2024-03-15 09:22:41
   Compilador ...... : IBM RPG 7.4
   Nivel de destino  : V7R3M0
```

**El objeto sabe de qué fuente salió, cuándo y con qué compilador.** Es procedencia embebida, sin
herramienta externa — lo que Endevor tiene que registrar aparte en COBOL, aquí está en el objeto.

Y el ecosistema moderno cerró el resto del círculo:

| Herramienta | Qué aporta |
|---|---|
| **ibmi-bob** | construcción desde fuentes **en el IFS**, con `Makefile` y dependencias |
| **Git en el IFS** | los fuentes en ficheros de flujo, no en ficheros físicos (clase 145) |
| **Code4i / RDi** | compilar y desplegar desde VS Code o Eclipse |
| **`SAVRSTOBJ`** | salvar y restaurar entre sistemas en una operación |

**ibmi-bob es el cambio importante de la última década**: llevó la construcción de IBM i al modelo
normal —**fuentes en git, construcción declarada, dependencias resueltas, salida verificable**— cuando
antes cada tienda tenía su propio programa CL de compilación.

Y hay un detalle sobre reproducibilidad específico de esta plataforma que merece señalarse: **el nivel
de destino**.

```text
CRTBNDRPG ... TGTRLS(V7R3M0)
```

**`TGTRLS` fija para qué versión del sistema operativo se genera el objeto**, y con eso **el objeto
funciona en cualquier sistema de esa versión o posterior**.

Es compatibilidad hacia adelante declarada explícitamente, y es coherente con la firma de programa de
servicio de la clase 143: **en esta plataforma, la compatibilidad se declara y el sistema la comprueba**,
en lugar de suponerse.
"""),
        "pli": ("""
 suma: procedure options(main);

    declare valor fixed binary(31);
    declare total fixed binary(31) initial(0);

    on endfile(sysin) goto fin;

    do while ('1'b);
       get list (valor);
       total = total + valor;
    end;

 fin:
    put skip list ('checksum=' || trim(char(total)));

 end suma;
""", """
**Lo que esta clase enseña en PL/I.** El programa usa `on endfile` con un salto —el idioma clásico de
PL/I para leer hasta el final (clase 103)— y `do while ('1'b)`, que es el bucle infinito con una
constante de bit.

Y sobre empaquetado, z/OS tiene un modelo que merece conocerse porque su unidad es distinta de todo lo
demás de esta página: **el módulo de carga en una biblioteca particionada**.

```text
PDS/PDSE: un fichero que contiene MIEMBROS con nombre
   MI.PROD.LOADLIB(MIPGM)     <-- el módulo ejecutable
   MI.PROD.SOURCE(MIPGM)       <-- el fuente
   MI.PROD.COPYLIB(CLIENTE)     <-- el copybook
```

**Una biblioteca particionada es a la vez un directorio y un fichero**, y se copia, se salva y se
transporta como una unidad.

Y de ahí la forma clásica de desplegar en el mainframe, que es asombrosamente simple:

```jcl
//COPIA  EXEC PGM=IEBCOPY
//SYSUT1  DD DSN=MI.QA.LOADLIB,DISP=SHR
//SYSUT2  DD DSN=MI.PROD.LOADLIB,DISP=SHR
//SYSIN   DD *
  COPY OUTDD=SYSUT2,INDD=SYSUT1
  SELECT MEMBER=(MIPGM)
```

**Copiar un miembro de una biblioteca a otra ES el despliegue** (clase 148), y la vuelta atrás es
copiar el anterior de vuelta — que se conserva porque **las bibliotecas se versionan por generaciones**:

```text
MI.PROD.LOADLIB.G0042V00     <-- grupo de datos generacional
MI.PROD.LOADLIB.G0041V00      <-- la anterior, automáticamente conservada
```

**Los *generation data groups*** mantienen las últimas N versiones automáticamente, y se referencian con
`(0)` para la actual, `(-1)` para la anterior.

Es control de versiones de artefactos integrado en el sistema de ficheros, y es de los años sesenta.

Y sobre reproducibilidad, PL/I comparte la solución de COBOL de esta página —**registrar la construcción
en lugar de reproducirla**— con una particularidad propia que conviene nombrar: **el listado de
compilación con `AGGREGATE` y `ATTRIBUTES`** documenta **la disposición exacta en memoria de cada
estructura**.

Y eso importa aquí porque **en PL/I la disposición depende de opciones de compilación** —`ALIGNED`,
`UNALIGNED`, el modelo de direccionamiento—, así que **el mismo fuente puede producir estructuras con
distinto tamaño**.

Es la misma clase de dependencia oculta que el ABI de C++ en esta página: **el binario depende de cosas
que no están en el fuente**, y por eso la lista de materiales tiene que incluir las opciones.
"""),
        "mumps": ("""
SUMA ; Suma de comprobacion -- clase 144
 read linea
 new i, total, n
 set total = 0
 for i = 1:1:$length(linea, " ") do
 . set n = $piece(linea, " ", i)
 . if n '= "" set total = total + n
 write "checksum=", total, !
 quit
""", """
**Lo que esta clase enseña en M.** `$length(linea, " ")` devuelve **cuántos trozos hay** al partir por
espacios, y `$piece` extrae cada uno: es el par de funciones que hace el reparto de texto en M sin
crear listas (clase 093).

Y sobre empaquetado, M tiene el modelo más ajeno de esta página y ya apareció en la clase 143: **el
artefacto es una global**.

Un paquete KIDS **es una estructura de datos en la base**, no un fichero, y contiene el código como
texto junto con las definiciones de datos y los guiones de instalación.

Y eso tiene una consecuencia que merece destacarse para esta clase: **la instalación es una transacción
de base de datos**.

```mumps
 tstart
 ; cargar rutinas, migrar datos, actualizar definiciones
 tcommit
```

**Si algo falla a mitad, se deshace todo** — incluidas las rutinas ya sustituidas, porque las rutinas
son datos.

En un despliegue de ficheros, "deshacer a mitad" significa restaurar una copia de seguridad y esperar. En
M es un `trollback`.

Y sobre reproducibilidad y verificación, la comunidad M construyó una técnica que merece conocerse
porque resuelve el problema de esta clase con los medios del lenguaje: **la suma de comprobación de
rutina**.

```mumps
 ; ^%RCMP y CHKSUM^XTSUMBLD en VistA
 do CHKSUM^XTSUMBLD("MIRUT")
 ; devuelve un valor calculado sobre el CÓDIGO de la rutina
```

**Cada rutina de VistA tiene una suma de comprobación publicada**, y el sistema puede recorrer todas las
rutinas instaladas y **comprobar que ninguna ha sido modificada localmente**.

Eso responde a una pregunta muy concreta y muy real en estos sistemas: **"¿este hospital ha parcheado
algo a mano?"** — y la respuesta importa, porque un parche local puede romper una actualización o puede
ser la razón por la que un fallo no se reproduce en otro sitio.

Es exactamente la función de un `sha256sum` sobre los binarios instalados, adaptada a un sistema donde el
código vive en la base de datos.

Y la lección transferible es la del cierre de esta clase: **un artefacto verificable requiere una
identidad calculada sobre su contenido**, y da igual si ese contenido es un binario, un fichero de texto
o una entrada de base de datos.
"""),
        "smalltalk": ("""
| linea total |

linea := stdin nextLine trimBoth.
total := 0.

(linea substrings: ' ') do: [ :p | total := total + p asNumber ].

Transcript show: 'checksum=', total printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Aquí está el extremo de esta clase, y es coherente con toda
la Parte 8: **el artefacto de despliegue es la imagen**.

```smalltalk
Smalltalk snapshot: true andQuit: true.
```

Y eso significa que **lo que se despliega es el estado completo del sistema**: todas las clases, todos
los métodos compilados, todos los objetos vivos, las conexiones abiertas, las cachés calentadas y las
ventanas que estuvieran abiertas.

**A favor**, es la reproducibilidad más fuerte que hay: **no hay nada que instalar, resolver, compilar
ni configurar**. La aplicación arranca exactamente en el estado en que se guardó, en milisegundos.

**En contra**, es opaca. **¿Qué hay dentro de una imagen de 80 MB?** Todo lo que alguien cargó alguna
vez, incluidos experimentos, versiones antiguas de métodos y objetos huérfanos.

Y de ahí las dos prácticas que la comunidad desarrolló y que merecen conocerse porque son la respuesta a
esta clase:

**Primera, la construcción de imagen desde cero, con guion:**

```bash
# Pharo: descargar una imagen limpia y cargar el proyecto encima
curl get.pharo.org/64/110 | bash
./pharo Pharo.image eval "Metacello new baseline: 'MiApp';
    repository: 'github://org/miapp:v1.2.3/src'; load."
./pharo Pharo.image save miapp
```

**La imagen se construye desde una imagen base conocida más una lista de paquetes con versión** — que es
exactamente el modelo de un contenedor con su fichero de construcción.

**Y segunda, la reducción de imagen**:

```smalltalk
Smalltalk garbageCollect.
Smalltalk cleanUp: true.
SystemNavigation default obsoleteBehaviors.     "clases zombis"
```

**Limpiar el sistema antes de guardar** quita las clases obsoletas, las referencias de las herramientas
de desarrollo y los objetos inalcanzables.

Y hay una versión extrema de esto que merece nombrarse: **el reductor de imagen** de algunos Smalltalk
comerciales **elimina las clases y métodos que la aplicación no usa**, analizando el grafo de envíos —lo
que produce imágenes de pocos megabytes.

Es el mismo enlace inteligente que Pascal tiene con `-XX` en esta página, aplicado a un sistema de
objetos vivos, y con la misma dificultad que en cualquier lenguaje dinámico: **`perform:` con un
selector construido en marcha hace imposible saber qué se usa** (clase 111).

Y ahí está la observación que cierra esta clase para Smalltalk: **la flexibilidad que hace tan buena la
depuración es la misma que impide reducir el sistema con garantías** — el compromiso que la Parte 8
mostró clase tras clase, apareciendo una vez más en el empaquetado.
"""),
    },
)

# ---------------------------------------------------------------------------
# 145 — Git y control de versiones para proyectos poliglotas
# ---------------------------------------------------------------------------
SPECS["145"] = dict(
    gancho="""
Contar cuántos mensajes de *commit* hay en una línea. El programa es trivial; lo que no lo es, es que
**tres de los lenguajes de esta página no guardan su código en ficheros de texto**: RPG lo tuvo durante
décadas en ficheros de base de datos con números de secuencia, M lo tiene dentro de la propia base de
datos, y Smalltalk lo tiene dentro de una imagen binaria. **Git supone que el código son ficheros de
texto separados por saltos de línea**, y esa suposición es la clase entera.
""",
    porque="""
Aquí el concepto es el **control de versiones y sus supuestos**, y estos lenguajes lo enseñan porque
**cada uno rompe uno de ellos**. COBOL y Fortran tienen **formato por columnas**, así que un cambio de
sangrado produce un diff enorme. RPG guardaba el fuente en **ficheros físicos con números de
secuencia**. M vive en la base de datos. Smalltalk versiona **métodos, no líneas**. Y todos ellos han
tenido que encajar en una herramienta que se diseñó para el núcleo de Linux.

Y aparece la fricción concreta que cualquier proyecto poliglota sufre: **finales de línea,
codificaciones, ficheros generados y binarios**.
""",
    cierre="""
Lo transferible: **el control de versiones no versiona código, versiona ficheros — y esa diferencia
tiene consecuencias**. De ahí las tres reglas que aparecen en toda esta página: **no versionar lo que se
genera**, porque produce conflictos que no significan nada; **normalizar el formato antes de que llegue
al repositorio**, con `.gitattributes` y un formateador automático, porque un cambio de estilo mezclado
con un cambio de lógica hace ilegible la revisión; y **hacer *commits* que cuenten una cosa**, porque el
historial es documentación y es lo único que quedará explicando por qué.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. COMMITS.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  I       PIC 9(4) COMP.
01  CNT     PIC 9(4) COMP VALUE 0.
01  ENPAL   PIC 9      VALUE 0.
01  ED      PIC -(3)9.

PROCEDURE DIVISION.
    ACCEPT LINEA

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        IF LINEA(I:1) = SPACE
            MOVE 0 TO ENPAL
        ELSE
            IF ENPAL = 0
                MOVE 1 TO ENPAL
                ADD 1 TO CNT
            END-IF
        END-IF
    END-PERFORM

    MOVE CNT TO ED
    DISPLAY "commits=" FUNCTION TRIM(ED)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** COBOL tiene el conflicto más directo con las herramientas
modernas de esta página, y es de formato: **el formato fijo por columnas**.

```text
Columnas 1-6:   número de secuencia (histórico: el número de la TARJETA)
Columna 7:      indicador: * comentario, - continuación, / salto de página
Columnas 8-11:  área A: divisiones, secciones, nombres de nivel 01 y 77
Columnas 12-72: área B: el resto del código
Columnas 73-80: identificación del programa (histórico)
```

**Ese formato viene de la tarjeta perforada de 80 columnas**, y las columnas 1-6 se usaban para
**reordenar la baraja si se caía al suelo**.

Y su consecuencia para esta clase es doble y muy práctica:

**Primera, muchos fuentes heredados llevan números de secuencia**, y hay herramientas que los
renumeran. **Renumerar cambia todas las líneas**, así que el diff resultante es del 100 % del fichero y
la revisión es imposible.

La regla es la del cierre de esta clase: **normalizar de una vez, en un *commit* que no haga otra cosa,
y no volver a tocarlo**.

**Y segunda, el área A y el área B importan**: mover una línea dos espacios **puede cambiar el
significado**. Así que **no se puede aplicar un formateador genérico** ni confiar en la sangría
automática de un editor que no conozca COBOL.

Y el formato libre —`>>SOURCE FORMAT FREE`, que este curso usa con `cobc -free`— es el estándar desde
COBOL 2002, y es la recomendación para código nuevo por exactamente esta razón.

Y hay una fricción específica del mundo mainframe que merece explicarse: **la codificación**.

**El fuente en z/OS está en EBCDIC**, no en ASCII ni en UTF-8. Así que llevarlo a git implica
**transcodificar**, y ahí aparecen problemas reales: **los caracteres que no existen en ambas
codificaciones** —el signo `¬`, la barra vertical, los corchetes— **cambian según la página de códigos
nacional**.

```text
En la página 037 (EE. UU.), el corchete izquierdo es x'BA'
En la 297 (Francia), esa posición es otra cosa
```

**Un fuente COBOL transcodificado con la página de códigos equivocada compila mal o no compila.**

Y por eso `.gitattributes` es imprescindible en un repositorio mainframe:

```text
*.cbl  working-tree-encoding=IBM-1047 text eol=lf
*.cpy  working-tree-encoding=IBM-1047 text eol=lf
```

**Git puede guardar en UTF-8 y presentar en EBCDIC**, con esa configuración. Es una capacidad poco
conocida y es justo lo que este caso necesita.
"""),
        "fortran": ("""
program commits
   implicit none
   character(len=200) :: linea
   integer :: i, cnt
   logical :: en_palabra

   read(*, '(A)') linea
   cnt = 0
   en_palabra = .false.

   do i = 1, len_trim(linea)
      if (linea(i:i) == ' ') then
         en_palabra = .false.
      else if (.not. en_palabra) then
         en_palabra = .true.
         cnt = cnt + 1
      end if
   end do

   write(*, '(A,I0)') 'commits=', cnt
end program commits
""", """
**Lo que esta clase enseña en Fortran.** Fortran comparte el problema de COBOL en esta página —**el
formato fijo**— y con una historia igual de concreta:

```text
Columnas 1-5:   etiqueta numérica
Columna 6:      continuación (cualquier carácter distinto de espacio o 0)
Columnas 7-72:  el código
Columnas 73-80: ignoradas (números de secuencia)
```

**Y la columna 73 en adelante se IGNORA.** Esa es la trampa clásica: una línea de más de 72 caracteres
**se trunca en silencio**, y el compilador no avisa.

```fortran
      IF (X .GT. 0) CALL PROCESAR(A, B, C, D, E, F, G, H, VALOR_LARGO)
!                                                          ^ columna 73: TODO ESTO SE PIERDE
```

Y para esta clase, la consecuencia es la misma que en COBOL: **cualquier herramienta que reformatee o
reindente puede romper el código en silencio**, y un diff de reformateo es ilegible.

El formato libre —desde Fortran 90, con extensión `.f90`— es la recomendación evidente. Pero hay millones
de líneas en formato fijo, y de ahí las herramientas del ecosistema:

| Herramienta | Qué hace |
|---|---|
| **fprettify** | formateador para Fortran libre; sangrado y espaciado consistentes |
| **findent** | **convierte formato fijo a libre** y viceversa |
| **`.editorconfig`** | tabuladores frente a espacios, ancho de línea |

**`findent` merece la mención** porque hace la conversión que casi todo proyecto heredado acaba
necesitando, y la conversión es exactamente el tipo de cambio que **debe ir en su propio *commit***.

Y Fortran aporta a esta clase una fricción propia y muy común, que es la de la clase 143: **los ficheros
generados**.

```gitignore
*.mod        # generados por el compilador, atados a su versión
*.o
*.smod       # submódulos
build/
```

**Versionar un `.mod` es garantizarse conflictos sin significado**, porque es un binario que cambia con
cada compilación.

Y merece extraer la regla general, porque es la primera del cierre de esta clase y se viola
constantemente: **si un fichero se puede regenerar desde otro que está versionado, no se versiona**.

La excepción que sí conviene conocer: **cuando regenerarlo requiere una herramienta que no todo el
mundo tiene** —un generador de analizadores, un compilador de esquemas—, a veces se versiona el
resultado a propósito. Es una decisión legítima **si se toma conscientemente y se documenta**, y un
desastre si ocurre por descuido.
"""),
        "ada": ("""
with Ada.Text_IO; use Ada.Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Commits is
   Linea      : String (1 .. 200);
   Ultimo     : Natural;
   Cnt        : Natural := 0;
   En_Palabra : Boolean := False;
begin
   Get_Line (Linea, Ultimo);

   for I in 1 .. Ultimo loop
      if Linea (I) = ' ' then
         En_Palabra := False;
      elsif not En_Palabra then
         En_Palabra := True;
         Cnt := Cnt + 1;
      end if;
   end loop;

   Put_Line ("commits=" &
             Ada.Strings.Fixed.Trim (Cnt'Image, Ada.Strings.Both));
end Commits;
""", """
**Lo que esta clase enseña en Ada.** El programa usa `'Image` con `Trim` para quitar el espacio inicial
del signo, y `Get_Line` con un parámetro `Ultimo` que devuelve cuántos caracteres se leyeron de verdad
— porque la cadena es de longitud fija (clase 093).

Y sobre control de versiones, Ada tiene una propiedad estructural que ayuda mucho y que merece
señalarse: **la separación de especificación y cuerpo en ficheros distintos** (clase 143).

```text
cliente.ads     <-- el contrato: cambia POCAS veces
cliente.adb      <-- la implementación: cambia MUCHO
```

**Un cambio en `.ads` es un cambio de interfaz, y un cambio en `.adb` no lo es.** Y eso se ve
directamente en el historial: **`git log -- '*.ads'` muestra la evolución de las interfaces del
sistema**, separada del ruido de la implementación.

Es una propiedad muy útil para revisar y para entender un sistema ajeno, y en lenguajes donde todo está
en un fichero no se puede obtener.

Y Ada tiene una convención de nombres que interactúa con los sistemas de ficheros y que conviene
conocer, porque produce conflictos reales en equipos mixtos:

```text
Mi_Paquete.Sub_Unidad   →   mi_paquete-sub_unidad.ads
```

**GNAT usa nombres de fichero en minúsculas derivados del nombre de la unidad**, con `-` para los
hijos. Y en macOS y Windows, **el sistema de ficheros no distingue mayúsculas de minúsculas**, así que
un fichero renombrado solo de mayúsculas **git no lo detecta como cambio** en esas plataformas.

Es una fricción de proyecto poliglota clásica, y la configuración que la evita:

```bash
git config core.ignorecase false
```

Y el ecosistema de Ada añade herramientas de formato que encajan con la segunda regla del cierre:

```bash
gnatpp -rnb *.adb          # formateador oficial, en su sitio
gnatcheck -rules -from=reglas.rules
```

**`gnatpp` es un formateador determinista**, así que **ponerlo en un gancho de pre-commit elimina para
siempre los diffs de estilo** — que es la práctica que esta clase recomienda y que en Ada tiene el
respaldo de una herramienta oficial.

Y merece nombrarse la práctica de los proyectos críticos que va más allá de lo habitual: **cada *commit*
enlaza con un requisito o un informe de problema**, y hay herramientas que **verifican la trazabilidad
completa** entre requisitos, código, pruebas y cambios.

Es una obligación de las normas de certificación, y es la versión estricta de "un *commit* cuenta una
cosa".
"""),
        "pascal": ("""
program Commits;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea: string;
  I, Cnt: Integer;
  EnPalabra: Boolean;

begin
  ReadLn(Linea);
  Cnt := 0;
  EnPalabra := False;

  for I := 1 to Length(Linea) do
    if Linea[I] = ' ' then
      EnPalabra := False
    else if not EnPalabra then
    begin
      EnPalabra := True;
      Inc(Cnt);
    end;

  WriteLn('commits=', IntToStr(Cnt));
end.
""", """
**Lo que esta clase enseña en Pascal.** El ecosistema Pascal aporta a esta clase el ejemplo canónico de
lo que **no** hay que versionar, y es una historia con mucha sangre: **los ficheros del diseñador
visual**.

```text
Unit1.pas    <-- el código: texto, se revisa bien
Unit1.dfm     <-- el FORMULARIO: posiciones, tamaños, propiedades de cada control
Unit1.lfm      <-- lo mismo en Lazarus
Project1.dproj  <-- XML del proyecto, reescrito por el IDE en cada guardado
```

**El `.dfm` es donde está el problema.** Es un fichero que el diseñador reescribe entero cada vez que
alguien mueve un control dos píxeles, y contiene la posición y el tamaño de todos ellos.

Consecuencias, todas reales:

- **Dos personas tocando el mismo formulario producen un conflicto casi seguro**, aunque hayan cambiado
  cosas distintas.
- **El conflicto es imposible de resolver a mano** con sensatez, porque el orden de las propiedades no
  es estable.
- **Y el `.dproj` cambia por sí solo** al abrir el proyecto, generando *commits* sin contenido.

Las prácticas que el ecosistema desarrolló:

```text
# guardar el formulario en TEXTO, no en binario (opción del IDE)
# y en .gitattributes:
*.dfm  text eol=crlf
*.pas  text eol=crlf
*.lfm  text eol=lf
*.dproj merge=ours          <-- no intentar fusionar; quedarse con el propio
```

**Y la regla de organización que de verdad funciona: un formulario, una persona.** Es una restricción
social impuesta por una limitación técnica, y es honesta reconocerla.

Y Pascal aporta la otra fricción clásica de esta página, y esta afecta a cualquier proyecto poliglota:
**los finales de línea**.

El mundo Delphi es de Windows y usa CRLF; Free Pascal en Linux usa LF. **Y un fichero que cambia de
final de línea aparece en git como modificado entero.**

```text
# .gitattributes: la solución correcta
*        text=auto              # normalizar a LF en el repositorio
*.pas    text eol=crlf           # ...y entregar CRLF a Windows
*.sh     text eol=lf              # los guiones SIEMPRE con LF
*.bat    text eol=crlf
*.png    binary
```

**`text=auto` guarda LF en el repositorio y entrega lo que cada plataforma espera.** Es la
configuración que todo repositorio poliglota debería tener desde el primer *commit*, y añadirla después
produce un cambio masivo que hay que aislar en su propio *commit*.
"""),
        "lisp": ("""
(let ((linea (read-line))
      (cnt 0)
      (en-palabra nil))
  (loop for c across linea
        do (if (char= c #\\Space)
               (setf en-palabra nil)
               (unless en-palabra
                 (setf en-palabra t)
                 (incf cnt))))
  (format t "commits=~D~%" cnt))
""", """
**Lo que esta clase enseña en Common Lisp.** `loop for c across linea` recorre una cadena carácter a
carácter — `across` es para vectores y `in` para listas, una distinción que `loop` mantiene explícita.

Y sobre control de versiones, Lisp tiene una fricción propia que merece explicarse, porque es directamente
el supuesto que esta clase cuestiona: **git compara por líneas, y el código Lisp es un árbol**.

```lisp
(defun procesar (datos)
  (let ((resultado '()))
    (dolist (d datos)
      (push (transformar d) resultado))
    (nreverse resultado)))
```

**Envolver ese cuerpo en un `handler-case` cambia la sangría de todas las líneas de dentro**, y el diff
muestra el bloque entero como modificado — cuando lo que pasó es que se añadió un nivel.

Es el mismo problema que cualquier lenguaje con bloques anidados, agravado porque **en Lisp la sangría
es muy significativa para la lectura** y la comunidad la respeta estrictamente.

Y las herramientas que lo mitigan:

```bash
git diff -w                    # ignorar cambios de espacio en blanco
git diff --word-diff            # comparar por PALABRAS, no por líneas
```

**`--word-diff` es especialmente útil en Lisp** por la densidad de las expresiones: una línea con seis
formas anidadas cambia entera aunque solo se toque una.

Y el ecosistema:

| Herramienta | Notas |
|---|---|
| **`cl-format` / `lisp-format`** | formateo automático, para ganchos de pre-commit |
| **SLIME + Paredit** | edición estructural: nunca se desequilibran los paréntesis |
| **`.dir-locals.el`** | reglas de sangría por proyecto, en Emacs |

Y Lisp aporta a esta clase una advertencia específica y muy suya, que viene de la Parte 8: **el estado
de la imagen no está en git**.

En un flujo de trabajo interactivo, es normal **redefinir funciones en el REPL** mientras se prueba. Y
entonces:

- **La imagen tiene una definición y el fichero tiene otra.**
- **Las pruebas pasan en la imagen y fallan en una construcción limpia.**
- **Y el cambio que hacía funcionar todo puede no haberse guardado nunca.**

Es el equivalente Lisp de "funciona en mi máquina", y la disciplina que lo evita es la que el ecosistema
recomienda: **recargar el sistema desde cero antes de dar nada por bueno**.

```lisp
(asdf:load-system "mi-proyecto" :force t)
```

Es la misma lección que Smalltalk en esta página, y viene del mismo sitio: **cuando el entorno de
desarrollo tiene estado, ese estado puede mentir**.
"""),
        "tcl": ("""
gets stdin linea

set n 0
foreach p [split [string trim $linea]] {
    if {$p ne ""} { incr n }
}

puts "commits=$n"
""", """
**Lo que esta clase enseña en Tcl.** Tcl está en el lado cómodo de esta clase —**el código es texto plano
sin formato obligatorio**— y aporta algo distinto: **es el lenguaje con el que se han automatizado
muchísimos flujos de control de versiones**.

Pero hay una fricción propia que merece explicarse, y es de las más frecuentes en proyectos poliglotas:
**los ganchos de git son guiones, y los guiones necesitan finales de línea LF**.

```bash
#!/usr/bin/env tclsh
# .git/hooks/pre-commit
```

**Si ese fichero se guarda con CRLF en Windows, falla con un mensaje incomprensible**:

```text
/usr/bin/env: 'tclsh\r': No such file or directory
```

**El `\\r` acaba formando parte del nombre del intérprete.** Es uno de los errores más desconcertantes
que produce un repositorio mal configurado, y la solución está en `.gitattributes`:

```text
*.sh        text eol=lf
*.tcl       text eol=lf
hooks/*     text eol=lf
```

Y Tcl es especialmente adecuado para escribir esos ganchos, por lo mismo que la clase 140 señalaba:
**ejecutar programas y comparar salidas es su especialidad**.

```tcl
#!/usr/bin/env tclsh
# pre-commit: rechazar si algún fichero tiene tabuladores mezclados
set ficheros [exec git diff --cached --name-only --diff-filter=ACM]
foreach f [split $ficheros \\n] {
    if {[file extension $f] ne ".tcl"} continue
    set fh [open $f]; set contenido [read $fh]; close $fh
    if {[string match "*\\t*" $contenido]} {
        puts stderr "ERROR: $f contiene tabuladores"
        exit 1
    }
}
exit 0
```

Y merece señalar el principio general que hay detrás y que es la segunda regla del cierre: **lo que se
puede comprobar automáticamente no debe comprobarse en la revisión**.

Un revisor humano que dedica atención a los tabuladores **no la está dedicando a la lógica**. Los ganchos
y el formateador automático existen para liberar esa atención, y la clase 146 lo desarrolla.

Y una advertencia práctica sobre los ganchos que conviene conocer: **los ganchos locales no se
versionan** —viven en `.git/hooks`, que no está en el repositorio— así que **no se puede confiar en que
todo el mundo los tenga**.

La solución habitual es tenerlos en un directorio versionado y **apuntar `core.hooksPath` ahí**, o
—mejor— **hacer la misma comprobación también en la integración continua** (clase 147), que es el único
sitio donde no se puede saltar.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;

my @commits = split ' ', $linea;

print "commits=", scalar(@commits), "\\n";
""", """
**Lo que esta clase enseña en Perl.** `scalar(@commits)` fuerza el contexto escalar de un arreglo, que es
su número de elementos — uno de los idiomas más característicos del lenguaje (clase 090).

Y sobre control de versiones, Perl tiene una conexión histórica directa que merece contarse: **git se
escribió inicialmente con una parte importante en Perl**.

`git-svn`, `git-send-email`, `git-cvsimport`, `git-request-pull` y varios más eran guiones de Perl, y
algunos lo siguen siendo. **La fontanería en C y la porcelana en guiones** fue la arquitectura original
de git, y Perl era el lenguaje de la porcelana.

Y Perl es todavía la herramienta natural para el trabajo que esta clase implica:

```perl
# reescribir el historial, analizar registros, migrar de un sistema a otro
git filter-branch --tree-filter 'perl -pi -e "s/viejo/nuevo/g" *.pl' HEAD
git log --format='%h %ae %s' | perl -ane '$c{$F[1]}++; END { ... }'
```

Y aporta a esta clase la advertencia más importante sobre la reescritura del historial, que merece
decirse con claridad:

**Reescribir el historial de un repositorio compartido rompe el de todos los demás.** `filter-branch`,
`filter-repo` y `rebase` sobre ramas publicadas **cambian los identificadores de todos los *commits*
posteriores**, y quien tenga el historial anterior se encontrará con dos versiones divergentes de la
misma historia.

Es una operación legítima —para quitar un fichero enorme, o unas credenciales filtradas— pero **exige
coordinar con todo el equipo**, y no se deshace.

Y hay un caso donde sí es obligatoria y esta clase debe nombrarlo, porque conecta con la clase 153: **si
se han filtrado credenciales al repositorio, borrarlas en un *commit* nuevo NO basta**.

```bash
git filter-repo --path secretos.env --invert-paths
```

**El *commit* antiguo sigue ahí y el secreto sigue siendo accesible** para cualquiera que clone. Hay que
reescribir el historial **y, en cualquier caso, rotar la credencial** — porque si estuvo publicada, hay
que darla por comprometida.

Y las herramientas para prevenirlo, que es lo que de verdad funciona:

```bash
git-secrets --install          # gancho que rechaza patrones de credenciales
gitleaks detect                 # escaneo del historial completo
trufflehog git file://.          # busca entropía alta: claves y tokens
```

**Ejecutarlas sobre el historial existente** es una de esas tareas que casi ningún proyecto hace y casi
todos deberían.
"""),
        "cpp": ("""
#include <iostream>
#include <string>

int main() {
    std::string palabra;
    int cnt = 0;
    while (std::cin >> palabra) ++cnt;

    std::cout << "commits=" << cnt << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ aporta a esta clase el problema del proyecto grande, y es el
que justifica media herramienta moderna: **la fragmentación del código en dos ficheros por unidad**.

```text
geometria.hpp    <-- la declaración
geometria.cpp     <-- la definición
```

**Un cambio de firma toca los dos**, así que **el diff de un cambio simple aparece repartido**, y es
fácil actualizar uno y olvidar el otro — con el resultado de la clase 137: un error de enlace.

Y hay dos fricciones más que aparecen en cualquier proyecto C++ mediano:

**Primera, los ficheros generados y los submódulos.**

```gitignore
build/
*.o
*.so
compile_commands.json      # generado por CMake; útil pero NO se versiona
```

Y los submódulos de git, que el ecosistema C++ usa mucho por falta de gestor de paquetes (clase 143),
tienen fama merecida de problemáticos: **un submódulo apunta a un *commit* concreto, y quien clona sin
`--recursive` obtiene un directorio vacío** y un error de compilación desconcertante.

**Y segunda, el formato.** C++ permite tantos estilos que un equipo sin acuerdo produce diffs
inservibles. La solución es la que hoy se considera obligatoria:

```yaml
# .clang-format
BasedOnStyle: LLVM
IndentWidth: 4
ColumnLimit: 100
```

```bash
git clang-format          # formatear SOLO lo que se ha cambiado
```

**`git clang-format` es la pieza que hace esto práctico**: reformatea únicamente las líneas del cambio
actual, así que **no produce un diff masivo** al introducir el formateador en un proyecto existente.

Y sobre la introducción del formateador en un proyecto viejo, git tiene una característica poco conocida
que resuelve el problema del cierre de esta clase:

```bash
# 1. reformatear TODO en un commit que no hace nada más
git commit -am "Formateo con clang-format (sin cambios funcionales)"
git rev-parse HEAD >> .git-blame-ignore-revs

# 2. y decirle a git que lo ignore al atribuir líneas
git config blame.ignoreRevsFile .git-blame-ignore-revs
```

**`.git-blame-ignore-revs` hace que `git blame` salte esos *commits***, así que **la atribución sigue
apuntando a quien escribió la lógica**, no a quien pasó el formateador.

Es la respuesta al argumento más usado contra reformatear un proyecto antiguo, y GitHub y GitLab
respetan ese fichero.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi COMMITS;
  linea char(200) const;
end-pi;

dcl-s i     int(10);
dcl-s cnt   int(10);
dcl-s enpal ind;

cnt = 0;
enpal = *off;

for i = 1 to %len(%trimr(linea));
  if %subst(linea : i : 1) = ' ';
    enpal = *off;
  elseif not enpal;
    enpal = *on;
    cnt += 1;
  endif;
endfor;

dsply ('commits=' + %char(cnt));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** Aquí está el caso que el gancho de la clase anunciaba, y es el más
llamativo de esta página: **durante casi cuarenta años, el fuente de RPG no estuvo en ficheros de
texto**.

```text
MIBIB/QRPGLESRC        <-- un FICHERO FÍSICO de base de datos
   Miembro: MIPGM       <-- cada programa es un MIEMBRO
      Registro 1: SEQNBR=0001.00  DATE=880115  "     H DFTACTGRP(*NO)"
      Registro 2: SEQNBR=0002.00  DATE=920304  "     D cliente  S ..."
```

**Cada línea de código es una fila de una tabla**, con **su número de secuencia y su fecha de última
modificación**.

Y eso tiene implicaciones fascinantes para esta clase:

**A favor**: **cada línea sabe cuándo se cambió por última vez.** Es un `git blame` de granularidad de
línea, integrado en el almacenamiento, desde 1988. El editor SEU lo mostraba, y sigue ahí.

**En contra**: **es incompatible con todo lo demás.** No hay diff, no hay ramas, no hay fusión, no hay
historial de versiones —solo la última fecha— y desde luego no hay git.

Y de ahí que la modernización de la plataforma en la última década haya consistido, en buena parte, en
**sacar el fuente de los ficheros físicos y ponerlo en el IFS**, el sistema de ficheros de flujo:

```text
/home/proyecto/qrpglesrc/mipgm.rpgle     <-- un fichero de texto normal
```

Y con eso llegó todo lo demás:

| Herramienta | Qué permite |
|---|---|
| **Git en el IFS** | ramas, fusiones, revisión, historial completo |
| **ibmi-bob** | construir desde el IFS con `Makefile` (clase 144) |
| **Code4i / RDi** | editar en VS Code o Eclipse, compilar en el sistema |
| **`CPYFRMSTMF` / `CPYTOSTMF`** | mover entre IFS y ficheros físicos, con transcodificación |

Y hay dos fricciones que la migración destapó y que merecen conocerse:

**La codificación**, igual que en COBOL de esta página: **los fuentes en ficheros físicos están en
EBCDIC** —CCSID 37, 273, 297 según el país— y el IFS puede estar en UTF-8. La conversión es explícita y
la página de códigos hay que declararla.

**Y la longitud de línea**: los ficheros físicos de fuente tienen **ancho fijo** —92 o 112 caracteres—,
así que **el código nunca superó ese ancho**. Al pasar a ficheros de texto, esa restricción desaparece,
y conviene decidir un límite deliberadamente en lugar de heredarlo por accidente.
"""),
        "pli": ("""
 commits: procedure options(main);

    declare linea  char(200) varying;
    declare i      fixed binary(31);
    declare cnt    fixed binary(31) initial(0);
    declare enpal  bit(1) initial('0'b);

    get edit (linea) (a(200));

    do i = 1 to length(linea);
       if substr(linea, i, 1) = ' ' then
          enpal = '0'b;
       else if ^enpal then
          do;
             enpal = '1'b;
             cnt = cnt + 1;
          end;
    end;

    put skip list ('commits=' || trim(char(cnt)));

 end commits;
""", """
**Lo que esta clase enseña en PL/I.** PL/I comparte con COBOL el mundo de esta página —**EBCDIC,
bibliotecas particionadas y gestores de configuración**— y aporta una perspectiva histórica que merece
recogerse, porque el control de versiones no empezó con git.

**La genealogía de la disciplina en el mainframe:**

| Época | Sistema | Qué aportó |
|---|---|---|
| Años 70 | **SCCS** (Unix, 1972) | el primer control de versiones: *deltas* |
| Años 70-80 | **Librarian**, **Panvalet** | versiones de miembros de PDS, con auditoría |
| Años 80-90 | **Endevor**, **ChangeMan** | promoción por entornos, aprobaciones, impacto |
| Hoy | **Git + Zowe / IDz** | el mainframe conectado al flujo moderno |

**SCCS es de 1972 y ya tenía la idea central**: guardar los cambios, no las copias.

Y los gestores de mainframe añadieron algo que git no tiene y que conviene conocer, porque no es una
carencia sino un enfoque distinto: **el flujo de aprobación como parte del sistema**.

```text
DEV → UNIT → QA → PRE → PROD
Cada promoción requiere:
  - la aprobación de un rol distinto al que hizo el cambio
  - que las pruebas de ese entorno hayan pasado
  - una ventana de cambio autorizada
  - y queda registrado quién aprobó qué y cuándo
```

**Eso es una obligación regulatoria en banca**, y es la razón de que estos sistemas parezcan pesados: **no
son un control de versiones, son un control de cambios**.

En el mundo moderno, ese papel lo cumplen las reglas de protección de ramas, las revisiones obligatorias
y los entornos con aprobación de las plataformas de integración continua — pero **la separación de
funciones** —quien escribe no aprueba, quien aprueba no despliega— **es un concepto que viene de aquí** y
que muchos equipos redescubren cuando les llega la primera auditoría.

Y merece cerrar con la razón por la que hoy el mainframe se conecta a git en lugar de sustituirlo:
**Zowe** —un proyecto abierto de la Open Mainframe Project— **expone z/OS por API REST**, así que **el
fuente puede vivir en git, la construcción se lanza desde una integración continua normal, y el resultado
se despliega en el mainframe**.

Es la reconciliación de los dos mundos de esta página, y es de la última década.
"""),
        "mumps": ("""
COMMITS ; Contar mensajes -- clase 145
 read linea
 new i, cnt, p
 set cnt = 0
 for i = 1:1:$length(linea, " ") do
 . set p = $piece(linea, " ", i)
 . if p '= "" set cnt = cnt + 1
 write "commits=", cnt, !
 quit
""", """
**Lo que esta clase enseña en M.** M rompe el supuesto de esta clase de la forma más profunda: **el
código no está en ficheros, está en la base de datos** (clase 123).

Una rutina M vive como una entrada del sistema, y **no hay un fichero `MIRUT.m` en ningún directorio**
—salvo que alguien lo exporte a propósito.

Y de ahí que el control de versiones en M haya seguido dos caminos, y los dos merecen conocerse:

**El primero es el histórico, y es el de la clase 144: el sistema de parches de VistA.**

```text
Parche XU*8.0*655
  - descripción del problema y de la solución
  - rutinas afectadas, con su SUMA DE COMPROBACIÓN antes y después
  - requisitos previos: qué parches deben estar instalados
  - y todo el paquete distribuido como una global
```

**La suma de comprobación por rutina hace de identificador de versión**, y el sistema puede comprobar
si una rutina está en el estado que el parche espera **antes de tocarla**.

Es control de versiones basado en el contenido, no en el historial, y funciona sorprendentemente bien
para el problema que resuelve: **coordinar actualizaciones en cientos de instalaciones independientes
que pueden haber divergido**.

**Y el segundo es el moderno: exportar a ficheros y usar git.**

```mumps
 do ^%RO          ; exportar rutinas a un fichero de texto
 do ^%RI           ; importarlas
```

Y las implementaciones actuales lo han integrado:

| Sistema | Qué ofrece |
|---|---|
| **YottaDB** | rutinas como ficheros `.m` en disco, con `$ZROUTINES` |
| **GT.M** | igual: el fuente está en el sistema de ficheros |
| **InterSystems IRIS** | **exportación automática a ficheros al guardar**, para git |
| **VistA moderno** | repositorios git con las rutinas exportadas |

**La exportación automática al guardar es la solución práctica**: el desarrollador edita en el entorno
nativo, y **un gancho escribe el fichero de texto correspondiente**, que git ve.

Es exactamente lo mismo que Smalltalk resolvió con Tonel en esta página, y por la misma razón: **cuando
el entorno de desarrollo no usa ficheros, hay que fabricar una proyección a ficheros para que las
herramientas del mundo funcionen**.

Y merece extraer la observación general, porque explica por qué esta clase existe: **git ganó tan
completamente que hoy todo entorno de desarrollo tiene que proyectarse a ficheros de texto, aunque su
modelo interno sea otro**.

Los que no pueden —o no quieren— quedan fuera del ecosistema de revisión, integración continua y
automatización, y esa presión es la que ha modernizado estas plataformas en la última década.
"""),
        "smalltalk": ("""
| linea partes |

linea := stdin nextLine trimBoth.
partes := linea substrings: ' '.

Transcript show: 'commits=', partes size printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk rompe el supuesto de esta clase de la manera más
interesante: **su unidad de cambio no es la línea ni el fichero — es el método**.

Y eso da un control de versiones **mejor** que el de ficheros para lo que esta clase busca, y **peor**
para todo lo demás.

**Monticello** (clase 143) compara así:

```text
Comparando MiPaquete-v12 con MiPaquete-v13:
  + Cliente >> #calcularDescuento:      (método AÑADIDO)
  - Cliente >> #metodoViejo              (ELIMINADO)
  ~ Pedido >> #total                      (MODIFICADO)
  + Clase: DescuentoEspecial
```

**Eso es un diff semántico**: dice qué métodos cambiaron, no qué líneas. Y con eso:

- **Mover un método de sitio en el fichero no aparece como cambio** —porque no hay fichero.
- **Reordenar métodos no genera conflicto.**
- **Y dos personas que tocan métodos distintos de la misma clase NO tienen conflicto**, aunque en un
  fichero estarían a diez líneas de distancia.

Ese último punto es una ventaja real y considerable: **la mayoría de los conflictos de fusión en
lenguajes de ficheros son artefactos de la representación**, no desacuerdos de verdad.

**Y la desventaja es la que la clase 144 anticipó: el mundo funciona con ficheros y con git.**

De ahí **Tonel** (2016), la solución que reconcilió Smalltalk con el ecosistema:

```text
src/
  MiPaquete/
    Cliente.class.st           <-- una clase, un fichero, en texto
    Cliente.extension.st
    package.st
```

**Tonel escribe cada clase en un fichero de texto legible**, con los métodos en orden estable, **para
que git pueda versionarlo, GitHub pueda mostrarlo y las herramientas de revisión funcionen**.

Y **Iceberg** es la herramienta que integra git dentro de Pharo: **hacer *commit*, cambiar de rama y
fusionar, desde el entorno**, con la imagen sincronizándose con el árbol de trabajo.

Y hay una fricción que merece nombrarse porque es la misma que Lisp señalaba en esta página y es
característica de los entornos con imagen: **la imagen y el repositorio pueden divergir**.

Se puede cambiar un método en la imagen y olvidar confirmarlo; o cambiar de rama y **quedarse con una
imagen que tiene métodos de las dos**. Iceberg avisa, pero la disciplina la pone la persona.

Y cierra esta clase con la observación que la atraviesa: **git ganó, y ganar significa que todo lo demás
se adapta a él**. Smalltalk tenía un modelo de versionado más fino y más adecuado a su lenguaje, y aun
así **construyó Tonel para poder hablar el idioma de todos** — porque el valor de estar en el ecosistema
común superó al de tener la mejor herramienta propia.
"""),
    },
)

# ---------------------------------------------------------------------------
# 146 — Revisión de código y estándares
# ---------------------------------------------------------------------------
SPECS["146"] = dict(
    gancho="""
Un identificador es válido si está todo en minúsculas. Es una regla de estilo arbitraria, y ahí está el
punto de esta clase: **casi todas lo son**. Lo que no es arbitrario es **quién la comprueba**. Y esta
página tiene los dos extremos del mundo: **MISRA y las normas de certificación de Ada**, donde cada
desviación se documenta y se justifica ante un auditor, y **M**, donde la convención más importante
nació de un límite físico: **los nombres no podían pasar de ocho caracteres**.
""",
    porque="""
Aquí el concepto es el **estándar de codificación y la revisión como proceso**, y estos lenguajes lo
enseñan porque **inventaron la disciplina**. La revisión formal de código —con roles, actas y métricas—
se formalizó en IBM en 1976, sobre programas COBOL y PL/I. Los estándares de codificación restrictivos
—MISRA, JSF, SPARK— nacieron en C y Ada para sistemas donde un fallo mata. Y **Perl aportó la idea
opuesta**: un analizador que aplica un libro de estilo, configurable y con severidades.

Y aparece la pregunta que decide el valor de una revisión: **¿qué debe mirar una persona, y qué debe
mirar una máquina?**
""",
    cierre="""
Lo transferible: **todo lo que una máquina pueda comprobar, debe comprobarlo la máquina** — formato,
nombres, complejidad, patrones peligrosos, cobertura. Lo que queda para la revisión humana es lo único
que una herramienta no puede juzgar: **si el código resuelve el problema correcto, si el diseño
aguantará el próximo cambio, y si alguien que llegue dentro de dos años lo entenderá**. Una revisión que
discute sangrados está desperdiciando lo más caro del proceso, que es la atención de otra persona. Y una
regla que no se puede automatizar y nadie recuerda, **no es un estándar: es una aspiración**.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. ESTILO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(60).
01  I       PIC 9(4) COMP.
01  LG      PIC 9(4) COMP.
01  VALIDO  PIC X(5) VALUE "true".

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE FUNCTION LENGTH(FUNCTION TRIM(LINEA)) TO LG

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > LG
        IF LINEA(I:1) IS NOT ALPHABETIC-LOWER
            MOVE "false" TO VALIDO
        END-IF
    END-PERFORM

    DISPLAY "valido=" FUNCTION TRIM(VALIDO)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** El programa usa **`ALPHABETIC-LOWER`**, una condición de clase
integrada en el lenguaje: COBOL tiene `NUMERIC`, `ALPHABETIC`, `ALPHABETIC-UPPER` y `ALPHABETIC-LOWER`
como comprobaciones nativas, más las clases definidas por el usuario con `CLASS`.

Y sobre revisión, aquí está el origen histórico que el "por qué" de esta clase anunciaba: **la
inspección de código formal, inventada por Michael Fagan en IBM en 1976**.

Y merece detallarse porque casi todo lo que hoy se hace en una revisión viene de ahí:

**Los roles están separados:**

- **Moderador**: dirige, no revisa el código; su papel es que la reunión no derive.
- **Autor**: presenta, **y no defiende** — explica.
- **Lector**: parafrasea el código en voz alta, línea a línea. **No es el autor.**
- **Inspectores**: buscan defectos contra una **lista de comprobación**.
- **Escriba**: registra cada defecto encontrado.

**Las reglas duras:**

- **Se buscan defectos, no soluciones.** Discutir cómo arreglarlo está prohibido en la reunión.
- **No se evalúa a la persona.** Los datos de la inspección **no pueden usarse para evaluar al autor**,
  o el proceso se corrompe de inmediato.
- **Hay preparación previa obligatoria**, con tiempo medido.
- **Y un ritmo máximo**: unas **150 líneas por hora**. Más rápido, y la eficacia se desploma.

**Los datos de IBM fueron contundentes**: las inspecciones encontraban entre el 60 % y el 90 % de los
defectos, y **detectarlos ahí costaba entre 10 y 100 veces menos que en producción**.

Y el dato del ritmo sigue siendo la crítica más útil a la revisión moderna: **una petición de cambios de
800 líneas revisada en veinte minutos no es una revisión**. Los estudios de Cisco y SmartBear de los
años 2000 confirmaron el mismo límite, con el mismo número.

Y las herramientas actuales del mundo COBOL:

| Herramienta | Qué comprueba |
|---|---|
| **SonarQube (plugin COBOL)** | complejidad, duplicación, reglas de mantenibilidad |
| **cobolint / GnuCOBOL `-Wall`** | avisos del compilador como norma |
| **CAST / Micro Focus Enterprise Analyzer** | análisis de sistemas enteros y grafo de impacto |
| **`GO TO` prohibido salvo `GO TO ... EXIT`** | la regla de estilo más extendida en COBOL |

**La última merece explicarse**: COBOL permite `ALTER` y saltos arbitrarios, y el estándar de facto de
la industria desde los años ochenta es **prohibirlos** — dejando solo `GO TO` hacia la etiqueta de
salida de un párrafo.

Es la aplicación práctica de la programación estructurada, impuesta por norma de equipo, en un lenguaje
que nunca la impuso.
"""),
        "fortran": ("""
program estilo
   implicit none
   character(len=60) :: linea
   integer :: i, n, c
   logical :: valido

   read(*, '(A)') linea
   n = len_trim(linea)
   valido = n > 0

   do i = 1, n
      c = iachar(linea(i:i))
      if (c < iachar('a') .or. c > iachar('z')) valido = .false.
   end do

   if (valido) then
      write(*, '(A)') 'valido=true'
   else
      write(*, '(A)') 'valido=false'
   end if
end program estilo
""", """
**Lo que esta clase enseña en Fortran.** El programa compara con `iachar`, que da el código **ASCII**
del carácter — frente a `ichar`, que da el del juego de caracteres del procesador. En una máquina
EBCDIC eso importa, y usar `iachar` hace el programa portable.

Y sobre estándares, Fortran tiene el suyo escrito en la primera línea de todos los programas de este
curso: **`implicit none`**.

La clase 137 contó por qué. Aquí importa la otra mitad: **es una regla de estilo que el compilador puede
imponer**.

```bash
gfortran -fimplicit-none -Wall -Wextra -std=f2018 -pedantic
```

**`-std=f2018 -pedantic` rechaza las extensiones no estándar**, que es la regla más valiosa en un
lenguaje con sesenta años de extensiones específicas de cada fabricante.

Y las reglas que la comunidad científica ha consolidado, y que merecen conocerse porque son sustanciales:

| Regla | Motivo |
|---|---|
| **`implicit none` siempre** | los nombres mal escritos crean variables (clase 137) |
| **Todo en `module`** | activa la comprobación de interfaces (clase 109) |
| **`intent(in/out/inout)` en cada argumento** | documenta y hace comprobar la dirección |
| **`private` por defecto en los módulos** | `public :: solo_lo_que_exporto` |
| **Nada de `common`, `equivalence` ni `goto` calculado** | de la era de las tarjetas |
| **`real(dp)` con `dp` de `iso_fortran_env`** | y nunca `real*8`, que no es estándar |
| **`pure` y `elemental` donde se pueda** | permite optimizar y documenta que no hay efectos |

**`intent` merece el detalle**, porque es una regla de estilo con consecuencias reales: declarar
`intent(in)` **hace que el compilador rechace cualquier modificación del argumento**, y **permite pasar
por referencia sin copia con seguridad**.

Es documentación que el compilador comprueba, que es lo mejor que puede ser una convención.

Y las herramientas:

```bash
fprettify --indent 3 --strict-indent      # formateo determinista
fortran-linter prog.f90
findent -ofree                              # convertir formato fijo a libre
```

Y merece cerrar con la observación cultural que esta clase permite: **el código científico se revisa
poco**, porque históricamente lo escribía **una persona sola, para su propia tesis**, y nadie más lo
leía.

La consecuencia se ve en el legado: programas de cien mil líneas sin pruebas, sin módulos y con
variables de tres letras. Y la respuesta de la comunidad en la última década —revistas que exigen el
código, revisión de software científico, iniciativas como el *Journal of Open Source Software*— es
exactamente esta clase aplicada a un campo que la necesitaba.
"""),
        "ada": ("""
with Ada.Text_IO; use Ada.Text_IO;

procedure Estilo is
   Linea  : String (1 .. 60);
   Ultimo : Natural;
   Valido : Boolean;
begin
   Get_Line (Linea, Ultimo);
   Valido := Ultimo > 0;

   for I in 1 .. Ultimo loop
      if Linea (I) not in 'a' .. 'z' then
         Valido := False;
      end if;
   end loop;

   if Valido then
      Put_Line ("valido=true");
   else
      Put_Line ("valido=false");
   end if;
end Estilo;
""", """
**Lo que esta clase enseña en Ada.** `Linea (I) not in 'a' .. 'z'` usa la pertenencia a un rango de un
tipo enumerado —`Character` lo es— que es una construcción del lenguaje, no una comparación numérica.

Y sobre estándares, Ada tiene los más estrictos de esta página, y merece ver cómo funcionan de verdad.

**Primero, el lenguaje impone restricciones por declaración:**

```ada
pragma Restrictions (No_Allocators);              --  prohibido reservar en el montón
pragma Restrictions (No_Recursion);                --  prohibida la recursión
pragma Restrictions (No_Secondary_Stack);           --  sin pila secundaria
pragma Restrictions (No_Exception_Propagation);      --  las excepciones no suben
pragma Restrictions (Max_Tasks => 8);                 --  como mucho ocho tareas
pragma Profile (Ravenscar);                            --  el perfil de tiempo real
```

**Esas restricciones las comprueba el compilador y se niega a compilar si se violan.** No son
recomendaciones: son parte del programa.

**Y el perfil Ravenscar** es un conjunto de restricciones sobre la concurrencia (clase 135) que hace el
sistema **analizable**: sin creación dinámica de tareas, sin entradas con guardas complejas, con
prioridades fijas — de modo que **se puede demostrar que se cumplen los plazos**.

Es una decisión de ingeniería que merece entenderse: **se renuncia deliberadamente a la mitad del
lenguaje para poder demostrar propiedades**. Y funciona: Ravenscar se usa en satélites y en control de
vuelo.

**Segundo, las normas del sector:**

| Norma | Ámbito |
|---|---|
| **DO-178C** | aviónica; niveles A a E, con MC/DC en el nivel A |
| **EN 50128** | ferrocarril |
| **IEC 61508** | seguridad funcional industrial |
| **JSF++ / MISRA** | los equivalentes en C++ y C |
| **AdaCore Coding Standard** | el estándar de estilo con `gnatcheck` |

**Y la propiedad que las define todas**: cada desviación **se documenta, se justifica técnicamente y la
aprueba un auditor**. No hay "lo dejo así porque tengo prisa".

**Y tercero, las herramientas:**

```bash
gnatcheck -rules -from=proyecto.rules      # reglas de codificación
gnatmetric                                  # complejidad ciclomática, anidamiento
gnatpp                                       # formateo determinista
gnatprove                                     # DEMOSTRACIÓN de ausencia de errores
```

Y merece cerrar con lo que esto significa para la revisión humana, porque es la respuesta a la pregunta
del "por qué" de esta clase: **cuando las reglas mecánicas las aplica el compilador y las propiedades
las demuestra una herramienta, la revisión humana se dedica íntegramente a si el requisito es el
correcto**.

Y en estos sistemas ese es, de hecho, el sitio donde están los fallos que matan: **no en el código, en la
especificación**.
"""),
        "pascal": ("""
program Estilo;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea: string;
  I: Integer;
  Valido: Boolean;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);
  Valido := Length(Linea) > 0;

  for I := 1 to Length(Linea) do
    if not (Linea[I] in ['a'..'z']) then
      Valido := False;

  if Valido then
    WriteLn('valido=true')
  else
    WriteLn('valido=false');
end.
""", """
**Lo que esta clase enseña en Pascal.** `Linea[I] in ['a'..'z']` usa **el operador de conjuntos** de
Pascal (clase 094): `['a'..'z']` es un conjunto literal, y `in` comprueba la pertenencia en una sola
instrucción de máquina, con máscaras de bits.

Es una construcción de 1970 que sigue siendo más legible que la comparación doble de casi todos los
lenguajes de esta página.

Y sobre estilo, Pascal tiene una historia particular: **fue diseñado como lenguaje de enseñanza**, y eso
le dio una cultura de estilo explícita desde el principio.

Las convenciones del ecosistema, muy estables desde los años noventa:

| Convención | Ejemplo |
|---|---|
| Tipos con `T` | `TCliente`, `TFormaPago` |
| Interfaces con `I` | `IRepositorio` |
| Campos privados con `F` | `FNombre` |
| Argumentos con `A` | `ANombre` |
| **PascalCase** para todo lo público | `CalcularTotal` |
| Constantes con prefijo del grupo | `clRojo`, `mrOk` |

**El prefijo `F` para campos merece la explicación**, porque no es capricho: en Delphi, **una propiedad
y su campo de respaldo tienen el mismo nombre conceptual**:

```pascal
private
  FNombre: string;
published
  property Nombre: string read FNombre write SetNombre;
```

**Sin el prefijo, habría colisión**, así que la convención resuelve una restricción real del lenguaje. Y
esa es la clase de regla de estilo que sobrevive: **la que resuelve algo**.

Y las herramientas del ecosistema:

```bash
ptop -c ptop.cfg entrada.pas salida.pas    # el formateador de Free Pascal
```

| Herramienta | Qué hace |
|---|---|
| **`ptop`** | formateador incluido en Free Pascal |
| **Jedi Code Format** | el formateador de referencia en Delphi |
| **Pascal Analyzer (Peganza)** | análisis estático profundo: variables no usadas, ámbitos |
| **`{$WARN ... ERROR}`** | convertir avisos concretos en errores |

**`{$WARN SYMBOL_DEPRECATED ERROR}` merece la mención**, porque es la forma limpia de aplicar una regla
de equipo: **marcar lo obsoleto y hacer que su uso no compile**.

```pascal
procedure MetodoViejo; deprecated 'usa MetodoNuevo';
```

Es documentación, aviso y regla de estilo en una declaración, y el compilador la hace cumplir — que es
lo que el cierre de esta clase pide.
"""),
        "lisp": ("""
(let ((palabra (string-trim '(#\\Space #\\Return) (read-line))))
  (format t "valido=~A~%"
          (if (and (plusp (length palabra))
                   (every #'lower-case-p palabra))
              "true" "false")))
""", """
**Lo que esta clase enseña en Common Lisp.** `every` con `#'lower-case-p` es la forma idiomática de
comprobar una propiedad sobre toda una secuencia (clase 115), y `plusp` comprueba que sea positiva —Lisp
tiene predicados con nombre para casi todo.

Y sobre estilo, Lisp tiene convenciones muy consolidadas y **muy informativas**, porque **el nombre dice
el tipo de cosa**:

| Convención | Significado |
|---|---|
| `nombre-p` / `nombrep` | **predicado**: devuelve verdadero o falso |
| `*variable-global*` | *earmuffs*: **variable especial** (clase 088) |
| `+constante+` | constante definida con `defconstant` |
| `%interno%` o `%funcion` | **de bajo nivel**, no usar desde fuera |
| `nombre!` (raro en CL) | destructivo — en Scheme es la norma |
| `n` de prefijo: `nreverse` | **destructivo**: reutiliza la estructura |
| `with-...` | macro que establece un contexto y lo deshace |
| `do-...` | macro de iteración |
| `define-...` / `def...` | definición |

**Los asteriscos de `*variable*` merecen destacarse** porque no son decorativos: marcan que la variable
tiene **alcance dinámico** (clase 088), y **enlazarla con `let` afecta a todo lo que se llame desde
ahí**.

Confundir una variable especial con una léxica produce fallos muy difíciles de encontrar, y **la
convención de nombres es la única defensa**, porque el lenguaje no lo distingue sintácticamente.

Es un ejemplo perfecto de la regla del cierre: **una convención que codifica información que el
compilador no da**.

Y el prefijo `n` de los destructivos —`nreverse`, `nconc`, `nsubst`— es igual de sustancial: avisa de
que **la estructura de entrada puede quedar destrozada**, que es la diferencia entre un programa
correcto y uno con corrupción silenciosa (clase 102).

Las herramientas:

```bash
sbcl --eval '(compile-file "prog.lisp")'    # los avisos del compilador SON el analizador
```

| Herramienta | Notas |
|---|---|
| **Los avisos de SBCL** | inferencia de tipos, variables sin usar, notas de optimización |
| **`lisp-critic`** | sugiere idiomas más limpios; nació para enseñar |
| **`sblint` / `sbcl-lint`** | los avisos en formato consumible |
| **`(declaim (optimize (safety 3) (debug 3)))`** | la política de compilación como norma |

**`lisp-critic` es curioso y merece la mención**: es un sistema experto con reglas del estilo *"esto es
un `(if x t nil)`, escribe `x` a secas"*, escrito para enseñar buen estilo Lisp a estudiantes.

Es el antepasado directo de los analizadores que sugieren idiomas, y es de los años noventa.
"""),
        "tcl": ("""
gets stdin linea
set p [string trim $linea]

if {$p ne "" && [string is lower -strict $p]} {
    puts "valido=true"
} else {
    puts "valido=false"
}
""", """
**Lo que esta clase enseña en Tcl.** **`string is lower -strict`** hace el trabajo entero: Tcl tiene una
familia de comprobaciones de clase —`alpha`, `digit`, `integer`, `double`, `boolean`, `space`, `xdigit`,
`wordchar`— y **`-strict` es la parte importante**: sin él, **la cadena vacía devuelve verdadero**.

Es una decisión de diseño discutible que ha causado muchos fallos, y por eso `-strict` es prácticamente
obligatorio en código serio. Es un buen ejemplo de regla de estilo con motivo.

Y Tcl tiene un estándar de estilo con nombre y con autoridad: **las *Tcl Style Guidelines* de John
Ousterhout**, el creador del lenguaje, publicadas en 1997.

Y sus reglas principales siguen siendo el estándar de facto:

| Regla | Motivo |
|---|---|
| **Llaves siempre en `expr` y en `if`**: `if {$x > 5}` | **sin llaves, hay doble sustitución: es un riesgo de inyección** |
| **`{*}` en lugar de `eval`** | `eval` sobre datos ajenos es ejecución de código |
| Espacios de nombres para todo paquete | evita colisiones globales (clase 086) |
| `::` explícito para las globales | deja claro el alcance |
| Comentarios con `#` **al principio de comando** | `#` a mitad de línea **no es un comentario** |

**La primera es la más importante y merece explicarse**, porque es a la vez estilo, rendimiento y
seguridad:

```tcl
if {$x > 5} { ... }        ;# CORRECTO: la expresión se compila una vez
if "$x > 5" { ... }         ;# MAL: se sustituye y se reanaliza CADA VEZ
```

**Sin llaves, el valor de `$x` se pega al texto y luego se analiza como expresión.** Si `$x` contiene
`1] ; exec rm -rf /  ; expr [1`, **eso se ejecuta**.

Es una inyección de código idéntica en naturaleza a la inyección SQL (clase 153), y la regla de estilo
—**pon llaves siempre**— es la defensa completa.

Y de paso es más rápido: **con llaves, el compilador de bytecode de Tcl compila la expresión una sola
vez** (clase 125).

Es el mejor ejemplo de esta página de una regla de estilo que **no es cosmética**: protege de una
vulnerabilidad y multiplica el rendimiento.

Y las herramientas:

```bash
nagelfar prog.tcl        # análisis estático: aridades, comandos, citación
frink -w prog.tcl         # formateo y comprobación de estilo
tclchecker                 # el de ActiveState
```

**Nagelfar detecta precisamente los `expr` sin llaves**, entre otras cosas, y es la herramienta que
convierte estas reglas en algo comprobable — que es lo que el cierre de esta clase exige.
"""),
        "perl": ("""
use strict;
use warnings;

my $palabra = <STDIN>;
chomp $palabra;

print "valido=", ($palabra =~ /^[a-z]+$/ ? 'true' : 'false'), "\\n";
""", """
**Lo que esta clase enseña en Perl.** La expresión regular `^[a-z]+$` resuelve el problema en una línea,
y es el argumento de Perl entero: **para trabajar con texto, la herramienta correcta es una expresión
regular** (clase 093).

Y sobre estándares, Perl aportó a esta clase algo que merece contarse, porque **cambió cómo la industria
piensa los estándares de estilo**.

En 2005, Damian Conway publicó **Perl Best Practices**: 256 reglas de estilo, **cada una con su
justificación**. Y al año siguiente, Jeffrey Ryan Thalhammer escribió **`Perl::Critic`**, un analizador
que **aplica esas reglas** — con dos características que hoy son estándar en todos los analizadores y
que entonces no lo eran:

**Primera, severidades:**

```bash
perlcritic --brutal prog.pl      # nivel 1: TODO, incluso lo discutible
perlcritic --cruel prog.pl        # nivel 2
perlcritic --harsh prog.pl         # nivel 3
perlcritic --stern prog.pl          # nivel 4
perlcritic --gentle prog.pl          # nivel 5: solo lo grave (por defecto)
```

**Que las reglas tengan severidad graduable es lo que permite adoptarlas en un proyecto existente**: se
empieza por lo grave y se sube el listón con el tiempo.

**Y segunda, la configuración por proyecto y las excepciones justificadas:**

```perl
# .perlcriticrc
severity = 3
[-Subroutines::ProhibitExplicitReturnUndef]
[Variables::ProhibitPunctuationVars]
allow = $@ $! $0
```

```perl
## no critic (ProhibitStringyEval)
my $r = eval $codigo;   # justificado: el código viene de la configuración firmada
## use critic
```

**La anotación en línea con el nombre de la regla concreta** obliga a decir **qué** se está saltando, y
deja constancia en el código.

Es el modelo que hoy tienen `eslint-disable`, `# noqa`, `#[allow(...)]` y `// NOLINT`, y **viene de
aquí**.

Y hay una regla de Perl Best Practices que merece citarse porque es la más contraintuitiva y la más
útil:

> **Escribe las expresiones regulares con `/x`**, que permite espacios y comentarios dentro.

```perl
if ($fecha =~ m{
        ^(\\d{4})    # año
        -(\\d{2})     # mes
        -(\\d{2})$     # día
    }x) { ... }
```

**Una expresión regular comentada es legible; una de sesenta caracteres no lo es.** Y en un lenguaje
famoso por producir código ilegible, la respuesta de su comunidad no fue prohibir la característica: fue
**dar una forma legible de usarla**.

Es el mejor resumen de la filosofía de esta clase: **los estándares no están para limitar el lenguaje,
están para que el código siga siendo legible dentro de dos años**.
"""),
        "cpp": ("""
#include <algorithm>
#include <cctype>
#include <iostream>
#include <string>

int main() {
    std::string palabra;
    if (!(std::cin >> palabra)) return 1;

    const bool valido = !palabra.empty() &&
        std::all_of(palabra.begin(), palabra.end(),
                    [](unsigned char c) { return std::islower(c) != 0; });

    std::cout << "valido=" << (valido ? "true" : "false") << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** El `unsigned char` en el parámetro de la lambda **no es
decorativo**: pasar un `char` con signo negativo a `std::islower` es **comportamiento indefinido**, y es
uno de los errores más frecuentes y menos conocidos de la biblioteca estándar de C.

Es exactamente el tipo de regla que un estándar de codificación debe recoger y una herramienta debe
comprobar, porque **nadie lo recuerda**.

Y C++ tiene los estándares más elaborados de esta página, cada uno con su motivo:

| Estándar | Ámbito | Carácter |
|---|---|---|
| **C++ Core Guidelines** | general; Stroustrup y Sutter | recomendaciones, con herramienta |
| **MISRA C++** | automoción | restrictivo; se prohíbe mucho |
| **AUTOSAR C++14** | automoción moderna | fusionado hoy con MISRA |
| **JSF++** | aviónica militar (F-35) | el más estricto: 221 reglas |
| **CERT C++** | seguridad | centrado en vulnerabilidades |
| **Google / LLVM style** | industria | sobre todo formato y nombres |

**Y el patrón común de los restrictivos merece verse**, porque enseña qué se considera peligroso:

```text
Prohibido: reserva dinámica después del arranque
Prohibido: excepciones (¡en JSF++ y en muchos sistemas embarcados!)
Prohibido: herencia múltiple de clases con implementación
Prohibido: sobrecarga de operadores salvo casos listados
Prohibido: recursión
Prohibido: goto, salvo salida de bucles anidados
Obligatorio: llaves en TODO if, incluso de una línea
```

**"Prohibidas las excepciones" sorprende y tiene un motivo concreto**: el tiempo de propagación de una
excepción **no está acotado**, porque depende de cuántos destructores haya que ejecutar. En un sistema
con plazos duros, eso es inaceptable.

Es la misma lógica que las restricciones de Ada en esta página: **se renuncia a características para
poder demostrar propiedades temporales**.

Y las herramientas, que en C++ son de las mejores que existen:

```bash
clang-tidy --checks='cppcoreguidelines-*,modernize-*,bugprone-*' prog.cpp
clang-format -i prog.cpp
cppcheck --enable=all prog.cpp
g++ -Wall -Wextra -Wpedantic -Wshadow -Wconversion -Werror
include-what-you-use prog.cpp
```

**`clang-tidy` con `modernize-*` merece la mención final**, porque hace algo poco común: **reescribe el
código**.

```bash
clang-tidy --fix --checks='modernize-use-nullptr,modernize-loop-convert' *.cpp
```

Convierte `NULL` en `nullptr`, bucles con índice en bucles por rango, `typedef` en `using`. **Es
migración automatizada de estilo a escala de millones de líneas**, y es la respuesta a la objeción de
que un estándar nuevo no se puede aplicar a código existente.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi ESTILO;
  palabra char(60) const;
end-pi;

dcl-s texto  varchar(60);
dcl-s i      int(10);
dcl-s valido ind;

texto = %trim(palabra);
valido = %len(texto) > 0;

for i = 1 to %len(texto);
  if %subst(texto : i : 1) < 'a' or %subst(texto : i : 1) > 'z';
    valido = *off;
  endif;
endfor;

if valido;
  dsply 'valido=true';
else;
  dsply 'valido=false';
endif;

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG es el caso más dramático de esta página en materia de estándares
de codificación, porque **el estándar cambió el lenguaje entero**.

Comparar las dos formas explica por sí solo lo que es un estándar de estilo:

```text
     C                   EVAL      TOTAL = PRECIO * CANTIDAD
     C                   IF        TOTAL > 1000
     C                   EVAL      DESCUENTO = TOTAL * 0.1
     C                   ENDIF
```

```rpgle
total = precio * cantidad;
if total > 1000;
  descuento = total * 0.1;
endif;
```

**Lo primero es RPG de formato fijo por columnas** —herencia de la tarjeta perforada, igual que COBOL y
Fortran en esta página—: la columna 6 es el tipo de especificación, la 7-11 el nivel, la 12-25 el factor
1, la 26-35 la operación...

**Y lo segundo es el mismo lenguaje en formato totalmente libre**, disponible desde 2013.

Y el estándar de la comunidad hoy es inequívoco:

| Regla | Motivo |
|---|---|
| **Formato totalmente libre para todo lo nuevo** | legibilidad, herramientas, git (clase 145) |
| **Nada de indicadores numéricos** (`*IN03`) | usar nombres: `dcl-s salir ind` |
| **Procedimientos, no subrutinas** | ámbito local y parámetros, en vez de globales |
| **Programas de servicio para la lógica** | permite pruebas unitarias (clase 139) |
| **`dcl-s`, `dcl-ds`, `dcl-pr` explícitos** | frente a las especificaciones D |
| **SQL embebido en lugar de acceso registro a registro** | conjuntos en vez de bucles (clase 117) |
| **Sin `goto`, sin `cabxx`** | de la era de los operadores de comparación con salto |

**"Nada de indicadores" merece la explicación**, porque es la seña de identidad del RPG antiguo: el
lenguaje tenía **99 indicadores numéricos globales** —`*IN01` a `*IN99`— que servían para todo:
condiciones, teclas de función, control de errores.

```text
     C                   IF        *IN03
```

**Nadie sabe qué es `*IN03` sin buscar en la pantalla o en la documentación.** Es el ejemplo perfecto de
una convención que el hardware impuso y que se mantuvo cuarenta años por inercia.

Y la modernización real de RPG consistió en **darle nombre a las cosas** — que es, reducido a lo
esencial, de lo que trata esta clase entera.

Las herramientas:

| Herramienta | Qué hace |
|---|---|
| **RDi / Code4i** | verificador de sintaxis, formateo, navegación |
| **ARCAD Observer / Transformer** | **conversión automática de fijo a libre** |
| **SonarQube (plugin RPG)** | métricas y reglas |
| **`OPTION(*SRCSTMT)`** | números de sentencia del fuente en los errores |
"""),
        "pli": ("""
 estilo: procedure options(main);

    declare palabra char(60) varying;
    declare i       fixed binary(31);
    declare valido  bit(1) initial('1'b);
    declare c       char(1);

    get edit (palabra) (a(60));
    palabra = trim(palabra);

    if length(palabra) = 0 then valido = '0'b;

    do i = 1 to length(palabra);
       c = substr(palabra, i, 1);
       if c < 'a' | c > 'z' then valido = '0'b;
    end;

    if valido then
       put skip list ('valido=true');
    else
       put skip list ('valido=false');

 end estilo;
""", """
**Lo que esta clase enseña en PL/I.** PL/I es el lenguaje que mejor ilustra **por qué existen los
estándares de codificación restrictivos**, porque es el caso de estudio del problema opuesto: **un
lenguaje que lo permite todo**.

PL/I se diseñó en 1964 para unificar el mundo científico de Fortran y el comercial de COBOL, **y añadió
además concurrencia, procesamiento de listas, manejo de excepciones y programación de sistemas**.

El resultado fue enorme, y la reacción de la comunidad académica fue igual de célebre: **Edsger
Dijkstra escribió que era un lenguaje "demasiado barroco para ser dominado"** y **Niklaus Wirth diseñó
Pascal en gran medida como respuesta** — un lenguaje pequeño, con una sola forma de hacer cada cosa.

**Pascal y PL/I son las dos filosofías de esta clase en estado puro**, y las dos siguen vivas: los
lenguajes que dan un camino y los que dan veinte.

Y la solución práctica en PL/I fue la de esta clase: **subconjuntos de uso obligatorio**.

```text
Estándares típicos de una instalación PL/I:
  - Prohibido DEFAULT: declarar TODO explícitamente
  - Prohibido el alias por DEFINED y BASED salvo casos aprobados
  - Prohibidas las conversiones implícitas: conversión explícita siempre
  - Un solo punto de retorno por procedimiento
  - Prefijos de condición obligatorios: (SUBSCRIPTRANGE, STRINGRANGE, SIZE)
  - Nada de GOTO fuera del bloque
```

**"Prohibido `DEFAULT`" merece la explicación**, porque es la característica más peligrosa del lenguaje:

```pli
 default range(a:z) fixed binary(31);   /* TODO lo no declarado es entero */
```

**`DEFAULT` permite redefinir las reglas de tipos implícitos para todo un programa.** Es potentísimo y
convierte el código en ilegible para quien no vio esa línea — el mismo problema que el `implicit` de
Fortran en esta página, elevado a norma configurable.

Y las opciones del compilador que aplican el estándar:

```text
PP(MACRO) FLAG(W) RULES(NOLAXDCL, NOLAXCTL, NOLAXIF, NOLAXQUAL)
```

**`RULES(NOLAXDCL)` exige que todo esté declarado**, `NOLAXIF` prohíbe las comparaciones laxas y
`NOLAXQUAL` obliga a cualificar los nombres de estructura.

Es `implicit none` y `use strict` de esta página, en un compilador de IBM, aplicable por opción de
compilación — y es la forma correcta de imponer un estándar: **que no compile**.
"""),
        "mumps": ("""
ESTILO ; Validar identificador -- clase 146
 read palabra
 new i, c, valido
 set valido = $select($length(palabra) > 0 : 1, 1 : 0)
 for i = 1:1:$length(palabra) do
 . set c = $extract(palabra, i)
 . if (c < "a") ! (c > "z") set valido = 0
 write "valido=", $select(valido : "true", 1 : "false"), !
 quit
""", """
**Lo que esta clase enseña en M.** Aquí está el caso que el gancho de la clase anunciaba: **la convención
más importante de M nació de una limitación física**.

**El estándar de M limitaba los nombres a ocho caracteres** —y en la práctica, muchas implementaciones
solo distinguían los primeros ocho—. Además, **el espacio de rutinas era plano y global**: no hay
espacios de nombres.

Y de ahí salió la convención que define el código VistA y que merece explicarse, porque es una solución
ingeniosa a un problema real:

```text
DPT      -- fichero de pacientes
XU       -- Kernel (utilidades del sistema)
XUS      -- Kernel, seguridad
DI       -- FileMan
LR       -- laboratorio
PS       -- farmacia
RA       -- radiología
```

**Cada paquete tiene un prefijo de dos o tres letras asignado formalmente**, y **todas sus rutinas,
globals y variables empiezan por él**.

```mumps
 do EN^PSOORDER          ; punto de entrada EN de la rutina PSOORDER (farmacia)
 set ^PSDRUG(ien, 0)      ; la global de medicamentos
```

**Eso es un espacio de nombres implementado con una convención de nombres**, administrado por un
registro central, y funcionando en un sistema de decenas de miles de rutinas.

Es la respuesta más pura de esta página a la pregunta de qué es un estándar de codificación: **una
convención que sustituye a una característica que el lenguaje no tiene**.

Y VistA tiene el documento que lo formaliza, y merece nombrarse: **el SAC, *VistA Programming Standards
and Conventions***, que además de los prefijos regula:

| Regla | Motivo |
|---|---|
| **`new` obligatorio para toda variable local** | el ámbito es global por defecto (clase 088) |
| **Nada de `$zx` específico del fabricante** en código portable | funciona en varias implementaciones |
| **Puntos de entrada documentados**, con `;;` | la línea de doble comentario es la interfaz |
| **Nada de `kill` sin argumentos** | borraría todas las variables del proceso |
| **`$$` para funciones extrínsecas** | distingue función de procedimiento |
| **Nada de indirección ni `xecute` sin justificar** | imposible de analizar (clase 123) |

**La primera es la más importante y la más peligrosa de olvidar**: en M, **una variable no declarada es
global al proceso**, así que **una rutina que usa `I` como contador sin hacer `new I` destruye el
contador de quien la llamó**.

Es el mismo fallo que las variables globales de cualquier lenguaje, agravado porque **aquí es el
comportamiento por defecto**.

Y por eso la regla del SAC es tajante y la revisión de código de VistA la comprueba siempre: **`new`
todo lo que uses**. Es la convención que hace posible que miles de rutinas de decenas de paquetes
convivan en un espacio de variables compartido.
"""),
        "smalltalk": ("""
| palabra valido |

palabra := stdin nextLine trimBoth.

valido := palabra notEmpty and: [
    palabra allSatisfy: [ :c | c isLowercase ] ].

Transcript show: 'valido=', (valido ifTrue: [ 'true' ] ifFalse: [ 'false' ]); cr.
""", """
**Lo que esta clase enseña en Smalltalk.** `allSatisfy:` con un bloque es el `every` de Lisp y el
`all_of` de C++ de esta página, y `and:` con un bloque es la conjunción **perezosa**: el segundo
argumento **solo se evalúa si el primero es verdadero** (clase 084).

Y sobre estilo, Smalltalk tiene las convenciones más peculiares de esta página, porque **la sintaxis de
mensajes con palabras clave convierte los nombres en frases**:

```smalltalk
cuenta transferir: 100 desde: origen a: destino.
coleccion detect: [ :x | x > 5 ] ifNone: [ nil ].
```

**El selector completo es `transferir:desde:a:`**, y las convenciones giran alrededor de eso:

| Convención | Ejemplo |
|---|---|
| **El selector debe leerse como una frase** | `at:put:`, no `set:with:` |
| Predicados con `is` o adjetivo | `isEmpty`, `notNil`, `includes:` |
| Devolver `self` en los que modifican | permite encadenar con `;` |
| **Los métodos, cortos** | tres a siete líneas es lo habitual |
| Categorías (protocolos) para agrupar | `accessing`, `printing`, `private` |
| Comentario de clase obligatorio | explica el **propósito**, no la implementación |

**"Los métodos cortos" no es una recomendación blanda en Smalltalk: es cultural y muy estricta.** Un
método de treinta líneas se considera un defecto, y la razón es concreta: **el navegador muestra un
método a la vez**, así que **un método que no cabe en la ventana es un método que no se puede leer de
una vez**.

Es un caso claro de una convención de estilo formada por la herramienta, igual que el ancho de 80
columnas viene del terminal y las ocho letras de M vienen del estándar.

Y las herramientas del ecosistema, que aquí son especiales por la razón de siempre —**el sistema se
analiza a sí mismo**:

| Herramienta | Qué hace |
|---|---|
| **SmallLint / Code Critics** | reglas de estilo y defectos, integradas en el navegador |
| **`allCallsOn:`** | quién llama a un selector (clase 138) |
| **Refactoring Browser** | **renombrar, extraer método, mover, con seguridad** |
| **Metrics / Moose** | métricas y análisis de arquitectura sobre el sistema vivo |

**SmallLint merece la mención final**, porque hace algo que muy pocos analizadores hacen: **avisa
mientras escribes, dentro del navegador de clases, y ofrece la corrección aplicable con un clic**.

Y la razón por la que puede hacerlo es la de la Parte 8: **el código es un objeto, así que el analizador
es un programa que recorre objetos** — no un analizador de texto que reimplementa el lenguaje.

Es la conclusión de esta clase en su forma más limpia: **cuando el entorno entiende el código, la
comprobación mecánica es barata y automática, y la revisión humana queda libre para lo que solo una
persona puede juzgar**.
"""),
    },
)
