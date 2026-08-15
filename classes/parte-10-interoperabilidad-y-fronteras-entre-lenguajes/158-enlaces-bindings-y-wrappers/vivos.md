# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 158

> [⬅️ Volver a la clase 158](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Una función que llama a otra y adorna el resultado: `wrap(10)`. Es la definición exacta de un
envoltorio, y esta clase trata de la pregunta que decide su calidad: **¿el envoltorio debe parecerse a
la biblioteca original o al lenguaje que lo usa?** Y hay un dato que ordena la página: **SWIG, de 1996,
generaba enlaces automáticos para Tcl, Perl, Python y Guile desde las mismas cabeceras de C**, y sigue
siendo la herramienta de referencia treinta años después.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **capa que traduce entre dos mundos**, y estos lenguajes la enseñan porque
> **cubren las tres formas de construirla**: **generada automáticamente** desde las cabeceras (SWIG,
> `f2py`, `-fdump-ada-spec`), **escrita a mano** con criterio (los envoltorios idiomáticos de casi todas
> las bibliotecas serias) y **traducida a mano una vez** —el caso extremo del proyecto JEDI, que portó
> decenas de miles de líneas de cabeceras de Windows a Pascal—.
>
> Y aparece la tensión que define la clase: **la traducción literal es fácil de generar y horrible de
> usar**; la idiomática es lo contrario.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` → stdout: `envuelto=wrap(<2n>)`
- **Regla:** `wrapper que aplica doble y formatea`

| stdin | esperado |
|---|---|
| `5` | `envuelto=wrap(10)` |
| `0` | `envuelto=wrap(0)` |
| `7` | `envuelto=wrap(14)` |

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
PROGRAM-ID. ENVOLV.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(40).
01  N       PIC S9(9) COMP-5.
01  R       PIC S9(9) COMP-5.
01  ED      PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    CALL "NUCLEO" USING N R

    MOVE R TO ED
    DISPLAY "envuelto=wrap(" FUNCTION TRIM(ED) ")"
    STOP RUN.

IDENTIFICATION DIVISION.
PROGRAM-ID. NUCLEO.
DATA DIVISION.
LINKAGE SECTION.
01  X       PIC S9(9) COMP-5.
01  Y       PIC S9(9) COMP-5.
PROCEDURE DIVISION USING X Y.
    COMPUTE Y = X * 2.
    GOBACK.
END PROGRAM NUCLEO.
END PROGRAM ENVOLV.
```

**Lo que esta clase enseña en COBOL.** El programa separa **el núcleo que calcula** del **envoltorio que
formatea**, y esa separación es exactamente la arquitectura que la clase 149 recomendaba para modernizar
COBOL: **la lógica en un programa llamable, la presentación fuera**.

Y merece verlo como lo que es en este mundo: **el envoltorio es la pieza que convierte un programa
heredado en un servicio**.

```text
Cliente REST  →  envoltorio  →  programa COBOL de 1990
                     ↑
        traduce JSON a COMMAREA y viceversa,
        convierte tipos, maneja errores, y no toca el original
```

Y el ecosistema tiene herramientas que generan esa capa automáticamente, y merecen conocerse porque la
generan **desde el copybook**:

| Herramienta | Qué hace |
|---|---|
| **IBM z/OS Connect** | expone un programa COBOL como API REST, **leyendo su copybook** |
| **CICS Web Services** | genera WSDL desde el copybook, y viceversa |
| **`DFHLS2JS` / `DFHJS2LS`** | los generadores: de copybook a JSON y al revés |
| **Micro Focus / Rocket** | equivalentes fuera del mainframe |

**Y la razón por la que eso funciona es la de la clase 159: un copybook es una descripción de datos
completa** —tipos, longitudes, escalas decimales, arreglos— **legible por una máquina**.

```cobol
       01  PETICION.
           05  CLIENTE-ID    PIC X(10).
           05  IMPORTE       PIC S9(9)V99 COMP-3.
           05  NUM-LINEAS    PIC 9(2) COMP.
           05  LINEA OCCURS 1 TO 50 TIMES DEPENDING ON NUM-LINEAS.
               10  ARTICULO  PIC X(8).
               10  CANTIDAD  PIC 9(4) COMP.
```

**El generador puede deducir de ahí un esquema JSON completo**, incluida la longitud de cada campo y la
escala de los decimales.

Y merece señalar las traducciones que el generador tiene que decidir, porque son el contenido de esta
clase:

| COBOL | JSON | Decisión |
|---|---|---|
| `PIC X(10)` con espacios | `"ABC"` | **¿se recortan los espacios?** |
| `COMP-3` con `V99` | `12.34` o `"12.34"` | **¿número o cadena?** (precisión) |
| `OCCURS DEPENDING ON` | arreglo | natural |
| Campo sin valor | `""` o ausente | **¿espacios o null?** |

**Ninguna de esas cuatro tiene una respuesta obvia**, y es exactamente por eso que el cierre de esta
clase separa la capa literal de la idiomática: **la primera puede generarse; la segunda requiere decidir
qué significan los espacios de un campo vacío en el dominio**.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
module nucleo
   implicit none
contains

   pure integer function doblar(x)
      integer, intent(in) :: x
      doblar = 2 * x
   end function doblar

end module nucleo

program envolv
   use nucleo
   implicit none
   integer :: n

   read(*, *) n
   write(*, '(A,I0,A)') 'envuelto=wrap(', doblar(n), ')'
end program envolv
```

**Lo que esta clase enseña en Fortran.** Fortran tiene el generador de enlaces más antiguo y más usado
de esta página, y merece contarlo porque **hizo posible el ecosistema científico de Python**: **`f2py`**.

```bash
f2py -c -m milib calculos.f90
```

```python
import milib
r = milib.nucleo.doblar(21)     # ¡y ya está!
```

**`f2py` lee el fuente Fortran, deduce las interfaces y genera el módulo de Python**, incluido:

- **La conversión de arreglos de NumPy a arreglos de Fortran**, respetando el orden por columnas (clase
  089) y **evitando la copia cuando es posible**.
- **El manejo de los argumentos de salida**: lo que en Fortran es `intent(out)` **se convierte en valor
  de retorno de Python**.
- **Y la deducción de dimensiones**: un argumento `n` que solo sirve para dar la longitud de un arreglo
  **desaparece de la firma de Python**, porque NumPy ya la sabe.

**Ese último punto es la lección de esta clase**, y merece subrayarse: **f2py no hace una traducción
literal — hace una traducción idiomática**.

```fortran
subroutine sumar(v, n, total)
   real(8), intent(in)  :: v(n)
   integer, intent(in)  :: n
   real(8), intent(out) :: total
```

```python
total = milib.sumar(v)      # sin n, y con el resultado devuelto
```

**Tres argumentos se convierten en uno, y uno de ellos pasa a ser el valor de retorno.** Es exactamente
la capa de arriba del cierre de esta clase, **generada automáticamente** porque `intent` da la
información necesaria.

Es la mejor demostración de una idea que merece extraerse: **cuanto más declara el lenguaje sobre sus
interfaces, mejores enlaces se pueden generar**. `intent`, las dimensiones declaradas y los tipos con
`kind` son lo que permite que f2py acierte.

Y el ecosistema tiene más opciones, cada una en un punto distinto del compromiso:

| Herramienta | Notas |
|---|---|
| **f2py** | en NumPy; el estándar de facto |
| **f90wrap** | envuelve tipos derivados y programación orientada a objetos de Fortran |
| **ctypes / cffi** | manual, sobre `bind(C)` (clase 156) |
| **Cython** | escribir la capa idiomática a mano, con rendimiento |
| **SWIG** | funciona, pero se usa más para C y C++ |

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Envolv is

   --  El núcleo: lo que de verdad calcula.
   function Nucleo (X : Integer) return Integer is (2 * X);

   --  El envoltorio: adapta el resultado al formato que espera quien llama.
   function Envuelto (X : Integer) return String is
      Bruto : constant String := Integer'Image (Nucleo (X));
   begin
      return "wrap(" & Bruto (2 .. Bruto'Last) & ")";
   end Envuelto;

   N : Integer;
begin
   Get (N);
   Put_Line ("envuelto=" & Envuelto (N));
end Envolv;
```

**Lo que esta clase enseña en Ada.** El programa separa `Nucleo` de `Envuelto`, que son literalmente las
dos capas del cierre de esta clase.

Y Ada tiene la generación de enlaces integrada en el compilador, cosa que ningún otro de esta página
ofrece:

```bash
g++ -c -fdump-ada-spec -C /usr/include/sqlite3.h
```

**GNAT lee la cabecera de C y produce el paquete Ada equivalente**: los tipos, las constantes, las
enumeraciones y los prototipos, con los `Convention => C` y los `External_Name` correctos (clase 156).

Y el resultado es exactamente **la capa de abajo** del cierre: literal, fea y correcta.

```ada
--  generado: literal
function sqlite3_open (filename : Interfaces.C.Strings.chars_ptr;
                       ppDb : System.Address) return int
  with Import => True, Convention => C, External_Name => "sqlite3_open";
```

**Y la capa de arriba se escribe a mano**, y en Ada tiene una forma muy reconocible:

```ada
package Sqlite is
   type Base_De_Datos is limited private;    --  tipo LIMITADO: no se puede copiar

   procedure Abrir (BD : out Base_De_Datos; Ruta : String);
   --  Lanza Error_Sqlite si falla. Cierra sola al salir del ámbito.

private
   type Base_De_Datos is limited new Ada.Finalization.Limited_Controlled with record
      Handle : System.Address := System.Null_Address;
   end record;

   overriding procedure Finalize (BD : in out Base_De_Datos);
end Sqlite;
```

Y merece señalar las tres decisiones que convierten eso en un buen envoltorio, porque son
transferibles:

**Una, `String` de Ada en lugar de `chars_ptr`.** Quien usa el paquete **no ve nunca un puntero de C**;
la conversión y la liberación las hace el envoltorio.

**Dos, excepción en lugar de código de retorno.** El `int` que devuelve la función de C se comprueba y
**se convierte en la forma de error nativa del lenguaje** (clase 116).

**Y tres, `Limited_Controlled` con `Finalize`**: el recurso **se cierra solo al salir del ámbito**
(clase 132), así que **es imposible olvidarse**.

Esa tercera es la que más valor añade y la que ninguna herramienta puede generar: **requiere saber que
`sqlite3_close` existe y que hay que llamarlo**.

Es la definición práctica de la capa idiomática: **la que codifica lo que hay que saber para usar bien la
biblioteca**.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Envolv;
{$MODE OBJFPC}{$H+}
uses SysUtils;

function Nucleo(X: Integer): Integer;
begin
  Result := 2 * X;
end;

function Envuelto(X: Integer): string;
begin
  Result := 'wrap(' + IntToStr(Nucleo(X)) + ')';
end;

var
  N: Integer;

begin
  Read(N);
  WriteLn('envuelto=', Envuelto(N));
end.
```

**Lo que esta clase enseña en Pascal.** El mundo Delphi tiene el ejemplo más extremo de esta clase, y
merece contarlo porque es una hazaña que hoy nadie repetiría: **el proyecto JEDI**.

**La API de Windows está definida en cabeceras de C** —miles de ficheros, decenas de miles de funciones,
estructuras, constantes y macros—. Y para usarla desde Delphi hacía falta **traducirlas a Object
Pascal**.

```pascal
{ JEDI API Library: traducción manual, función por función }
function CreateFileW(lpFileName: LPCWSTR; dwDesiredAccess: DWORD;
  dwShareMode: DWORD; lpSecurityAttributes: PSecurityAttributes;
  dwCreationDisposition: DWORD; dwFlagsAndAttributes: DWORD;
  hTemplateFile: THandle): THandle; stdcall; external 'kernel32.dll';
```

**El proyecto JEDI tradujo, a mano y durante años, prácticamente toda la API de Windows**, más DirectX,
OpenGL y decenas de bibliotecas más. Son **cientos de miles de líneas de declaraciones**.

Y merece preguntarse por qué a mano, porque la respuesta es la tesis de esta clase: **las cabeceras de C
contienen cosas que ningún generador traduce bien**.

```c
#define INVALID_HANDLE_VALUE ((HANDLE)(LONG_PTR)-1)   /* una macro con conversiones */
typedef struct { ... } POINT, *PPOINT, *LPPOINT;       /* tres nombres para lo mismo */
#ifdef UNICODE
#define CreateFile CreateFileW                          /* ¡el nombre depende de un #define! */
#endif
```

**Las macros del preprocesador no son declaraciones: son texto**, y un generador automático o las ignora
o las traduce mal.

Es el argumento central del cierre de esta clase: **la capa de abajo se puede generar cuando la
información está declarada, y no cuando está en macros, en documentación o en la cabeza de alguien**.

Y el ecosistema tiene también generadores para lo que sí se puede:

| Herramienta | Notas |
|---|---|
| **h2pas** | incluido en Free Pascal: convierte `.h` a unidades Pascal |
| **Chet / HeadConv** | conversores de la comunidad |
| **JEDI API Library** | la traducción manual de referencia |
| **Delphi «Import Type Library»** | genera enlaces desde una biblioteca de tipos de COM |

**La última merece destacarse** y conecta con la clase 160: **COM incluye una descripción de tipos
legible por máquina** —la *type library*—, y por eso **los enlaces sí se generan perfectamente**.

Es la diferencia entre una interfaz con esquema y una sin él, que es el tema de las dos clases
siguientes.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(defun nucleo (x) (* 2 x))

(defun envuelto (x)
  (format nil "wrap(~D)" (nucleo x)))

(let ((n (read)))
  (format t "envuelto=~A~%" (envuelto n)))
```

**Lo que esta clase enseña en Common Lisp.** Lisp tiene una ventaja para esta clase que ningún otro de la
página comparte: **las macros permiten generar la capa de abajo desde dentro del lenguaje**.

```lisp
;; En vez de generar un fichero, se genera CÓDIGO en tiempo de compilación
(defmacro definir-enlaces (biblioteca &body funciones)
  `(progn
     ,@(loop for (nombre retorno . args) in funciones
             collect `(cffi:defcfun (,(string-downcase nombre) ,nombre)
                          ,retorno ,@args))))

(definir-enlaces "libm"
  (sqrt :double (x :double))
  (pow  :double (x :double) (y :double))
  (fabs :double (x :double)))
```

**Ese `defmacro` es un generador de enlaces escrito en veinte líneas y ejecutado al compilar** (clase
122).

Y eso quita la parte más molesta del flujo habitual: **no hay un fichero generado que mantener
sincronizado**, ni un paso de construcción, ni un artefacto que se olvida de regenerar.

Es una aplicación directa de la idea de la clase 149 —**construir el lenguaje hasta el problema**— al
problema concreto de esta clase.

Y la capa de arriba, la idiomática, en Lisp tiene una forma característica:

```lisp
(defmacro con-base-de-datos ((var ruta) &body cuerpo)
  `(let ((,var (abrir-bd ,ruta)))
     (unwind-protect (progn ,@cuerpo)
       (cerrar-bd ,var))))

(con-base-de-datos (bd "datos.db")
  (consultar bd "SELECT ..."))       ; se cierra sola, pase lo que pase
```

**`unwind-protect` garantiza el cierre incluso si hay una condición** (clase 132), y **la macro
`con-...` convierte eso en una construcción del lenguaje**.

Es exactamente lo mismo que `Limited_Controlled` en Ada de esta página y que RAII en C++, conseguido con
una macro en lugar de con el sistema de tipos.

Y las herramientas del ecosistema:

| Herramienta | Notas |
|---|---|
| **CFFI** | la base (clase 156) |
| **cffi-grovel** | **compila un programa C que averigua tamaños y constantes reales** |
| **SWIG** | genera enlaces para CFFI |
| **cl-autowrap** | **lee las cabeceras con Clang** y genera los enlaces automáticamente |

**`cffi-grovel` merece la explicación**, porque resuelve un problema real de la clase 157: **las
constantes y los tamaños de una biblioteca dependen de la plataforma**.

```lisp
(constant (+o-rdonly+ "O_RDONLY"))
(ctype size-t "size_t")
```

**Grovel genera un programa en C, lo compila, lo ejecuta y le pregunta**. Es la única forma fiable de
saber cuánto mide un `size_t` o qué valor tiene `O_RDONLY` en ese sistema — y es lo que hacen, con otro
nombre, `autoconf`, `bindgen` y todos los generadores serios.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

proc nucleo {x} { expr {2 * $x} }
proc envuelto {x} { return "wrap([nucleo $x])" }

puts "envuelto=[envuelto $n]"
```

**Lo que esta clase enseña en Tcl.** Aquí está el dato del gancho, y merece contarse porque es una pieza
de infraestructura que casi nadie sabe de dónde salió: **SWIG lo escribió Dave Beazley en 1996, y su
primer objetivo fue Tcl**.

**SWIG —*Simplified Wrapper and Interface Generator*—** nació en el Laboratorio Nacional de Los Álamos,
para el mismo problema de la clase 155: **físicos con simulaciones en C y C++ que querían controlarlas
desde un lenguaje de guion**.

```swig
// milib.i
%module milib
%{
#include "milib.h"
%}
%include "milib.h"
```

```bash
swig -tcl milib.i        # genera milib_wrap.c
swig -python milib.i      # el MISMO fichero .i, otro lenguaje
swig -perl milib.i
swig -java milib.i
```

**Y esa es la aportación de SWIG**: **una descripción de la interfaz, muchos lenguajes destino**. Hoy
soporta más de veinte.

Y merece explicar qué hace bien y qué no, porque es la tesis de esta clase:

**Lo que hace bien**: la capa de abajo. Lee las declaraciones de C y C++ —incluidas clases, herencia,
plantillas y sobrecargas— y genera envoltorios correctos.

**Lo que no hace**: la capa de arriba. Un `char**` en una firma **puede ser un arreglo de cadenas, un
parámetro de salida o un puntero a puntero**, y SWIG no lo sabe.

Y su solución es la que merece extraerse, porque es un buen diseño: **los *typemaps***.

```swig
%typemap(in) (int argc, char **argv) {
    /* convertir una LISTA de Tcl en argc/argv */
}
```

**Un typemap dice cómo traducir un patrón de argumentos concreto**, así que **la capa idiomática se
escribe una vez, de forma declarativa, y se aplica a todas las funciones que encajen**.

Es la reconciliación de las dos capas del cierre de esta clase: **generar por defecto, y declarar las
excepciones**.

Y el ecosistema Tcl tiene además:

| Herramienta | Notas |
|---|---|
| **SWIG** | el generador multi-lenguaje |
| **critcl** | C dentro del guion (clase 156) |
| **TEA** | la arquitectura estándar de extensiones, con `configure` |
| **Ffidl** | llamadas sin compilar |

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

sub nucleo   { return 2 * $_[0] }
sub envuelto { return 'wrap(' . nucleo($_[0]) . ')' }

my $n = <STDIN>;
chomp $n;

print "envuelto=", envuelto($n), "\n";
```

**Lo que esta clase enseña en Perl.** Perl tiene una colección de generadores de enlaces que ilustra bien
la escala del problema, y merece verla porque cada uno ataca una parte:

| Herramienta | Qué genera |
|---|---|
| **`h2xs`** | el esqueleto de un módulo XS **desde una cabecera de C** |
| **`h2ph`** | traduce las **macros** de un `.h` a Perl |
| **SWIG** | el envoltorio completo, desde la interfaz |
| **`Inline::C`** | **C dentro del guion Perl**, compilado y cacheado |
| **`FFI::Platypus`** | sin generar nada (clase 156) |

**`Inline::C` merece la mención** porque es la misma idea que `critcl` en Tcl de esta página, y es
sorprendentemente cómoda:

```perl
use Inline C => <<'FIN';
int doblar(int x) { return 2 * x; }
FIN

print doblar(21);      # 42
```

**Ese C se compila la primera vez y se guarda en caché**; las siguientes ejecuciones lo cargan.

Y Perl aporta a esta clase la mejor ilustración de por qué la capa idiomática importa, con un caso que
todo el ecosistema conoce: **DBI**.

```perl
# La capa de abajo: DBD::Pg, DBD::mysql, DBD::SQLite, DBD::Oracle...
#   cada una envuelve la biblioteca C del fabricante, con sus rarezas

# La capa de arriba: DBI, la MISMA interfaz para todas
my $dbh = DBI->connect("dbi:Pg:dbname=x", $u, $p, { RaiseError => 1 });
my $sth = $dbh->prepare("SELECT * FROM t WHERE id = ?");
$sth->execute($id);
while (my $fila = $sth->fetchrow_hashref) { ... }
```

**DBI (1994) definió una interfaz común y dejó que cada base de datos escribiera su controlador**, y ese
diseño se copió literalmente en todas partes: **JDBC en Java, DB-API en Python, ODBC antes**.

Y merece señalar la decisión concreta que lo hizo bueno y que es la lección del cierre: **DBI no expone
la API de PostgreSQL ni la de Oracle** — expone **una abstracción propia** con `prepare`, `execute`,
`fetch` y transacciones.

**La capa de abajo es distinta en cada controlador; la de arriba es idéntica.** Y por eso cambiar de base
de datos en un programa Perl es cambiar una cadena de conexión.

Es el mejor argumento de esta página a favor de invertir en la capa idiomática: **no solo hace la
biblioteca agradable — puede hacer que varias bibliotecas distintas se usen igual**.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <string>

// El núcleo, con enlace de C: lo que otros lenguajes envolverán.
extern "C" long long nucleo(long long x) { return 2 * x; }

// El envoltorio idiomático: tipos del lenguaje, no de la frontera.
std::string envuelto(long long x) {
    return "wrap(" + std::to_string(nucleo(x)) + ")";
}

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "envuelto=" << envuelto(n) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** El programa muestra las dos capas del cierre en cinco líneas:
`nucleo` con enlace de C —la frontera— y `envuelto` con `std::string` —lo idiomático—.

Y C++ está en los dos lados de esta clase, y merece verlos por separado.

**Como origen**: envolver C++ es difícil por lo que la clase 157 explicó —**no hay ABI estable, las
plantillas no existen fuera, las excepciones no cruzan**—.

Y la solución canónica es la de la clase 156: **una interfaz en C con punteros opacos**, y encima el
enlace del otro lenguaje.

```text
C++ real  →  capa extern "C"  →  enlace del lenguaje destino  →  capa idiomática
```

**Cuatro capas**, y por eso las bibliotecas C++ pensadas para ser usadas desde fuera —como LLVM, que
publica una API en C— dedican trabajo real a esa frontera.

**Como destino**: envolver C desde C++ es donde RAII brilla (clase 132), y merece el ejemplo porque es la
capa idiomática en su forma más clara:

```cpp
class Fichero {
public:
    explicit Fichero(const char* ruta)
        : f_(std::fopen(ruta, "rb")) {
        if (!f_) throw std::runtime_error("no se pudo abrir");
    }
    ~Fichero() { if (f_) std::fclose(f_); }

    Fichero(const Fichero&) = delete;              // no copiable
    Fichero& operator=(const Fichero&) = delete;
    Fichero(Fichero&& o) noexcept : f_(std::exchange(o.f_, nullptr)) {}

    std::FILE* get() const { return f_; }
private:
    std::FILE* f_;
};
```

**Ese envoltorio de veinte líneas convierte una API de C que se puede usar mal de seis formas en una que
solo se puede usar bien**:

- **No se puede olvidar el `fclose`**: el destructor lo hace.
- **No se puede usar un fichero no abierto**: el constructor lanza.
- **No se puede cerrar dos veces**: no es copiable.
- **Y el error llega como excepción**, no como un puntero nulo que hay que recordar comprobar.

Es la definición práctica de la capa de arriba del cierre, y merece la observación general: **un buen
envoltorio no añade funcionalidad — quita formas de equivocarse**.

Y las herramientas para la capa de abajo:

| Herramienta | Notas |
|---|---|
| **SWIG** | C++ hacia veinte lenguajes |
| **pybind11 / nanobind** | C++ moderno hacia Python, con plantillas |
| **cppyy** | enlaces **automáticos en ejecución**, con Cling |
| **bindgen** | cabeceras de C hacia Rust |
| **Emscripten** | hacia JavaScript y WebAssembly (clase 162) |

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

dcl-pi ENVOLV;
  n int(10) const;
end-pi;

dcl-proc nucleo;
  dcl-pi *n int(20);
    x int(10) const;
  end-pi;
  return 2 * x;
end-proc;

dcl-proc envuelto;
  dcl-pi *n varchar(40);
    x int(10) const;
  end-pi;
  return 'wrap(' + %char(nucleo(x)) + ')';
end-proc;

dsply ('envuelto=' + envuelto(n));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** IBM i tiene el generador de envoltorios más práctico de esta página
para el problema que la plataforma tiene de verdad: **convertir un programa RPG de treinta años en una
API REST sin escribir código**.

**IWS, *Integrated Web Services*:**

```text
1. Se toma un programa o un procedimiento de un programa de servicio.
2. El asistente LEE SU PROTOTIPO: nombres, tipos, longitudes, direcciones.
3. Y genera un servicio REST o SOAP, con su descripción OpenAPI o WSDL.
4. Sin tocar el programa original.
```

**Y funciona porque el prototipo de RPG es una descripción de interfaz completa** (clase 156): tipos con
longitud y escala, `const` frente a modificable, estructuras con sus campos.

Es lo mismo que z/OS Connect hace con los copybooks de COBOL en esta página, y por la misma razón: **la
interfaz ya estaba declarada de forma legible por una máquina**.

Y merece señalar la decisión de diseño que el envoltorio tiene que tomar y que ninguna herramienta
resuelve sola, porque es la tesis del cierre de esta clase:

```rpgle
dcl-pr consultarCliente;
  id       char(10) const;
  nombre   char(50);           // ← ¿parámetro de SALIDA?
  saldo    packed(11:2);        // ← ¿salida también?
  codError int(10);              // ← ¿esto es un error o un dato?
end-pr;
```

**El generador no sabe que `codError` distinto de cero significa que `nombre` y `saldo` no valen nada.**

Y por eso la capa idiomática hay que escribirla: **traducir el código de error a un estado HTTP, decidir
qué campos van en el cuerpo y cuáles no, y recortar los espacios de los campos de longitud fija**.

Y el ecosistema moderno da además las piezas para hacerlo dentro de RPG:

| Herramienta | Qué hace |
|---|---|
| **`DATA-INTO` / `DATA-GEN`** | analizar y generar JSON o XML **con una instrucción** (clase 159) |
| **YAJL** | analizador y generador de JSON, rápido, muy usado |
| **`HTTPAPI` / `SQL HTTP functions`** | consumir servicios desde RPG |
| **IWS / Code4i** | exponer y desplegar |

**`DATA-INTO` merece la mención final** porque cambia el reparto de esta clase: **antes, la capa
idiomática se escribía fuera de RPG, en Java o en Node; ahora se puede escribir en RPG**.

Es lo que ha permitido que la lógica de negocio de estos sistemas se exponga sin poner una segunda
tecnología en medio — que es exactamente la regla de la clase 155: **menos fronteras y más gruesas**.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 envolv: procedure options(main);

    declare n fixed binary(31);

    nucleo: procedure (x) returns (fixed binary(31));
       declare x fixed binary(31);
       return (2 * x);
    end nucleo;

    envuelto: procedure (x) returns (char(40) varying);
       declare x fixed binary(31);
       return ('wrap(' || trim(char(nucleo(x))) || ')');
    end envuelto;

    get list (n);

    put skip list ('envuelto=' || envuelto(n));

 end envolv;
```

**Lo que esta clase enseña en PL/I.** PL/I comparte el mundo de COBOL en esta página —**los envoltorios
los generan las herramientas del mainframe desde las declaraciones**— y aporta una construcción del
lenguaje que es directamente un envoltorio: **`GENERIC`**.

```pli
 declare procesar generic (
    procesar_entero  when (fixed binary),
    procesar_decimal when (fixed decimal),
    procesar_texto   when (character)
 );

 call procesar(42);          /* → procesar_entero */
 call procesar('hola');       /* → procesar_texto */
```

**`GENERIC` declara un nombre que se resuelve, en compilación, al procedimiento cuyo tipo encaja.**

Es sobrecarga de nombres, y su utilidad para esta clase es concreta: **permite escribir una capa
idiomática con un solo nombre encima de varias funciones externas con nombres distintos**.

```pli
 declare abrir generic (
    abrir_fichero when (character),
    abrir_por_id  when (fixed binary)
 );
```

Y merece señalar que resuelve, con una declaración, lo que en C requiere macros con `_Generic` y en
COBOL no tiene solución.

Y PL/I aporta a esta clase la perspectiva del envoltorio más común del mundo mainframe, que no es hacia
C: **el envoltorio de un programa hacia una transacción**.

```pli
 /* La lógica pura, sin CICS: probable y reutilizable */
 calcular_interes: procedure (saldo, tasa, dias) returns (fixed decimal(11,2));
    ...
 end calcular_interes;

 /* El envoltorio de transacción: lee la COMMAREA, llama, escribe la respuesta */
 exec cics address commarea(ptr_comm);
 resultado = calcular_interes(comm.saldo, comm.tasa, comm.dias);
 comm.resultado = resultado;
 exec cics return;
```

**Separar el cálculo del envoltorio de transacción** es lo que permite que la misma lógica se exponga
después como servicio web, como llamada por lotes o como procedimiento almacenado de DB2 — **sin
tocarla**.

Es la aplicación de las dos capas del cierre de esta clase al problema de la modernización, y es la
recomendación número uno de cualquier proyecto de este tipo (clases 149 y 150).

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
ENVOLV ; Nucleo y envoltorio -- clase 158
 read n
 write "envuelto=", $$envuelto(n), !
 quit
 ;
nucleo(x) ; el calculo
 quit x * 2
 ;
envuelto(x) ; el formato
 quit "wrap(" _ $$nucleo(x) _ ")"
```

**Lo que esta clase enseña en M.** El programa separa `$$nucleo` de `$$envuelto`, que es la separación
del cierre de esta clase escrita con funciones extrínsecas.

Y M ilustra un caso de esta clase que merece destacarse porque es de los más grandes que existen: **el
RPC Broker de VistA** (clase 155) es un envoltorio, y su diseño enseña bien.

```text
Registro de la RPC en el fichero REMOTE PROCEDURE:
  NOMBRE:        ORWPT LIST ALL
  RUTINA:        LIST^ORWPT
  TIPO RETORNO:  ARRAY
  PARÁMETROS:    LITERAL, LITERAL
  DESCRIPCIÓN:   Devuelve la lista de pacientes que empiezan por...
```

**Cada RPC se registra como un dato**, con su rutina, sus parámetros y su tipo de retorno.

Y esa decisión —**la interfaz como entrada de base de datos, no como declaración en el código**— tiene
las dos caras que merece contrastar:

**A favor**: **se puede consultar y listar el catálogo de operaciones disponibles**, con su
documentación, y **añadir una RPC no requiere recompilar ni redesplegar nada**. Además, **el control de
acceso es por RPC**, con las claves de seguridad de la clase 153.

**En contra**: **la interfaz no está en el código** (clase 145), así que no se versiona con él y **el
programa no documenta lo que expone**.

Es exactamente el mismo compromiso que la tabla de llamadas externas de la clase 156 y que las tablas de
reglas de la clase 151: **en M, todo tiende a acabar siendo un dato**, con la flexibilidad y la opacidad
que eso trae.

Y el ecosistema moderno ha añadido lo que faltaba:

| Herramienta | Qué hace |
|---|---|
| **VistA RPC Broker** | el envoltorio histórico, por TCP con protocolo propio |
| **VistA FHIR / VX-API** | los mismos datos, con **contratos estándar de salud** (clase 160) |
| **YottaDB con envoltorios de Go, Python...** | acceso directo a las globals (clase 156) |
| **IRIS `%JSON.Adaptor`** | serialización automática de objetos a JSON |

**La segunda fila es la interesante y conecta con la clase siguiente**: **FHIR es un estándar de
interoperabilidad sanitaria** con esquemas definidos, así que **el envoltorio moderno de VistA no expone
sus estructuras internas: expone un contrato que otros sistemas ya entienden**.

Es la mejor forma de la capa idiomática del cierre de esta clase: **no adaptarse al lenguaje que llama,
sino a un estándar del dominio que todos comparten**.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n nucleo envuelto |

nucleo := [ :x | x * 2 ].
envuelto := [ :x | 'wrap(', (nucleo value: x) printString, ')' ].

n := stdin nextLine trimBoth asNumber.

Transcript show: 'envuelto=', (envuelto value: n); cr.
```

**Lo que esta clase enseña en Smalltalk.** El programa usa bloques como funciones de primera clase (clase
121), y componerlos —un bloque que llama a otro— **es el envoltorio en su forma más pequeña**.

Y Smalltalk aporta a esta clase un mecanismo que ningún otro lenguaje de la página tiene y que permite
construir envoltorios de una forma completamente distinta: **`doesNotUnderstand:`**.

```smalltalk
Object subclass: #Proxy
    instanceVariableNames: 'real registro'

Proxy >> doesNotUnderstand: unMensaje
    registro add: unMensaje selector.
    ^ unMensaje sendTo: real
```

**Cuando un objeto recibe un mensaje que no entiende, el sistema le envía `doesNotUnderstand:` con el
mensaje reificado** (clase 111) — y ahí se puede hacer lo que sea: registrarlo, reenviarlo, transformarlo
o rechazarlo.

**Y eso es un envoltorio que funciona para CUALQUIER interfaz, sin declarar nada.**

```smalltalk
proxy := Proxy sobre: unaBaseDeDatos.
proxy consultar: 'SELECT ...'.       "se registra y se reenvía, sin haberlo previsto"
```

Es el patrón Proxy (clase 151) obtenido gratis, y es la base de:

- **Los objetos simulados** de las pruebas, sin biblioteca (clase 139).
- **Los objetos remotos**: un proxy que reenvía el mensaje por la red.
- **La carga perezosa**: el objeto real no existe hasta el primer mensaje.
- **Y el registro de auditoría** sobre objetos existentes, sin tocarlos.

Es lo mismo que `tie` en Perl y `rename` en Tcl de la clase 151, aplicado al envío de mensajes, y es
**más general que los tres** porque **no hay que enumerar qué se intercepta**.

Y merece cerrar señalando el otro lado de la moneda, que es la constante de este curso: **eso mismo hace
imposible saber estáticamente qué mensajes entiende un objeto** (clase 150), así que las herramientas de
refactorización y de análisis no pueden razonar sobre un proxy.

La flexibilidad que hace el envoltorio trivial es la misma que impide comprobarlo — y decidir cuánta de
esa flexibilidad se quiere es, al final, la decisión que separa a los lenguajes de esta página.

---

## Y de vuelta a la clase

Lo transferible: **un buen envoltorio tiene dos capas, y confundirlas es el error habitual**. La de
abajo es la **traducción literal**, que se puede generar, se actualiza sola y expone la biblioteca tal
cual. La de arriba es la **capa idiomática**, escrita a mano, que usa los tipos, los errores y las
convenciones del lenguaje anfitrión — y que es donde se decide si la biblioteca resulta agradable. La
regla práctica: **generar la de abajo, escribir la de arriba, y no dejar que el resto del programa vea
nunca la de abajo**.

⏮️ [Volver a la clase 158](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
