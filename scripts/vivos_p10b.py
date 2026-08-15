# -*- coding: utf-8 -*-
"""Parte 10, lote B — clases 158 a 160. Ver `vivos_parte10.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 158 — Enlaces (bindings) y envoltorios (wrappers)
# ---------------------------------------------------------------------------
SPECS["158"] = dict(
    gancho="""
Una función que llama a otra y adorna el resultado: `wrap(10)`. Es la definición exacta de un
envoltorio, y esta clase trata de la pregunta que decide su calidad: **¿el envoltorio debe parecerse a
la biblioteca original o al lenguaje que lo usa?** Y hay un dato que ordena la página: **SWIG, de 1996,
generaba enlaces automáticos para Tcl, Perl, Python y Guile desde las mismas cabeceras de C**, y sigue
siendo la herramienta de referencia treinta años después.
""",
    porque="""
Aquí el concepto es la **capa que traduce entre dos mundos**, y estos lenguajes la enseñan porque
**cubren las tres formas de construirla**: **generada automáticamente** desde las cabeceras (SWIG,
`f2py`, `-fdump-ada-spec`), **escrita a mano** con criterio (los envoltorios idiomáticos de casi todas
las bibliotecas serias) y **traducida a mano una vez** —el caso extremo del proyecto JEDI, que portó
decenas de miles de líneas de cabeceras de Windows a Pascal—.

Y aparece la tensión que define la clase: **la traducción literal es fácil de generar y horrible de
usar**; la idiomática es lo contrario.
""",
    cierre="""
Lo transferible: **un buen envoltorio tiene dos capas, y confundirlas es el error habitual**. La de
abajo es la **traducción literal**, que se puede generar, se actualiza sola y expone la biblioteca tal
cual. La de arriba es la **capa idiomática**, escrita a mano, que usa los tipos, los errores y las
convenciones del lenguaje anfitrión — y que es donde se decide si la biblioteca resulta agradable. La
regla práctica: **generar la de abajo, escribir la de arriba, y no dejar que el resto del programa vea
nunca la de abajo**.
""",
    langs={
        "cobol": ("""
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
""", """
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
"""),
        "fortran": ("""
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
""", """
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
"""),
        "ada": ("""
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
""", """
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
"""),
        "pascal": ("""
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
""", """
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
"""),
        "lisp": ("""
(defun nucleo (x) (* 2 x))

(defun envuelto (x)
  (format nil "wrap(~D)" (nucleo x)))

(let ((n (read)))
  (format t "envuelto=~A~%" (envuelto n)))
""", """
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
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

proc nucleo {x} { expr {2 * $x} }
proc envuelto {x} { return "wrap([nucleo $x])" }

puts "envuelto=[envuelto $n]"
""", """
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
"""),
        "perl": ("""
use strict;
use warnings;

sub nucleo   { return 2 * $_[0] }
sub envuelto { return 'wrap(' . nucleo($_[0]) . ')' }

my $n = <STDIN>;
chomp $n;

print "envuelto=", envuelto($n), "\\n";
""", """
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
"""),
        "cpp": ("""
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

    std::cout << "envuelto=" << envuelto(n) << '\\n';
    return 0;
}
""", """
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
"""),
        "rpg": ("""
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
""", """
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
"""),
        "pli": ("""
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
""", """
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
"""),
        "mumps": ("""
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
""", """
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
"""),
        "smalltalk": ("""
| n nucleo envuelto |

nucleo := [ :x | x * 2 ].
envuelto := [ :x | 'wrap(', (nucleo value: x) printString, ')' ].

n := stdin nextLine trimBoth asNumber.

Transcript show: 'envuelto=', (envuelto value: n); cr.
""", """
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
"""),
    },
)

# ---------------------------------------------------------------------------
# 159 — Serialización entre lenguajes
# ---------------------------------------------------------------------------
SPECS["159"] = dict(
    gancho="""
Convertir un nombre y un valor en `x:5`. Es la serialización más simple imaginable, y la clase trata de
lo que ocurre cuando eso hay que hacerlo bien entre dos lenguajes que no comparten nada. Y esta página
tiene el dato que pone JSON en perspectiva: **el copybook de COBOL es una descripción de datos binaria
con tipos, escalas y arreglos variables — es decir, un esquema— y es de 1959**; **ASN.1, con su
codificación binaria y su compilador de esquemas, es de 1984**; y Protocol Buffers, de 2008.
""",
    porque="""
Aquí el concepto es el **formato de intercambio**, y estos lenguajes lo enseñan porque **sufrieron todos
los problemas antes de que existiera JSON**: el orden de los bytes, la codificación de caracteres, los
decimales con precisión, los registros de longitud variable y la evolución del esquema. **Y varios
tienen una propiedad que la industria redescubrió: su representación textual se puede volver a leer** —
Lisp con `print`/`read`, PL/I con `put data`/`get data`, Smalltalk con `storeString`.

Y aparece la pregunta que decide el formato: **¿lo leen personas o máquinas, y quién controla las dos
puntas?**
""",
    cierre="""
Lo transferible: **el formato es la parte fácil; el esquema y su evolución son la difícil**. Elegir entre
JSON, Protobuf o MessagePack cambia el tamaño y la velocidad; **lo que decide si el sistema sobrevive es
cómo se añade un campo sin romper a quien todavía no se ha actualizado**. De ahí las tres reglas que
atraviesan la página: **campos nuevos siempre opcionales y con valor por defecto**; **nunca reutilizar un
identificador o una posición que estuvo en uso**; y **los dos lados deben tolerar lo que no conocen** —
ignorar los campos desconocidos en lugar de fallar, que es lo que hace posible desplegar por partes.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. SERIAL.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(60).
01  C-NOM   PIC X(20).
01  C-VAL   PIC X(20).

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES
        INTO C-NOM C-VAL
    END-UNSTRING

    DISPLAY "serializado=" FUNCTION TRIM(C-NOM)
            ":" FUNCTION TRIM(C-VAL)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** Aquí está el dato del gancho, y merece desarrollarse porque
cambia la perspectiva sobre lo que es nuevo y lo que no: **un copybook es un esquema de serialización
binaria**.

```cobol
       01  PEDIDO.
           05  CLIENTE        PIC X(10).
           05  FECHA          PIC 9(8).
           05  IMPORTE        PIC S9(9)V99 COMP-3.
           05  DIVISA         PIC X(3).
           05  NUM-LINEAS     PIC 9(2) COMP.
           05  LINEA OCCURS 1 TO 99 DEPENDING ON NUM-LINEAS.
               10  ARTICULO   PIC X(8).
               10  CANTIDAD   PIC S9(5) COMP-3.
```

**Eso define, sin ambigüedad, cada byte del registro**: dónde empieza cada campo, cuántos bytes ocupa,
qué codificación tiene y cuántas repeticiones hay.

Y **`COMP-3` merece la explicación** porque es la razón de que este formato siga en uso (clase 072):
**decimal empaquetado, dos dígitos por byte, con el signo en el último medio byte**.

```text
El importe 12345.67 en S9(9)V99 COMP-3 ocupa 6 bytes:
   00 01 23 45 67 0C        (C = positivo, D = negativo)
```

**Es exacto —sin el redondeo binario de `double`— y es compacto.** Un `12345.67` en JSON son ocho
caracteres; aquí son seis bytes que además no pierden precisión.

Y las tres dificultades clásicas de intercambiar estos registros con otros sistemas merecen enumerarse,
porque son las de toda esta clase:

**Una, la codificación**: el mainframe usa **EBCDIC**, el resto del mundo ASCII o UTF-8. **Y la
conversión hay que hacerla campo a campo**, porque **los campos `COMP-3` y `COMP` NO se deben
convertir**: son binarios, y traducirlos como texto los destruye.

Es el error número uno al mover ficheros del mainframe: **un FTP en modo texto convierte todo el
registro y corrompe los campos numéricos**.

**Dos, el orden de los bytes**: los `COMP` del mainframe son de byte más significativo primero; los de
Intel, al revés (clase 128).

**Y tres, la evolución del esquema.** Y aquí COBOL enseña la regla que el cierre de esta clase propone,
porque la aprendió por las malas: **los campos nuevos se añaden AL FINAL del registro y con relleno
reservado**.

```cobol
           05  FILLER PIC X(100).      *> espacio reservado para el futuro
```

**Reservar relleno en el registro** era la práctica estándar precisamente porque **cambiar la posición
de un campo obliga a recompilar y redesplegar todo lo que lo lee, a la vez** — que es exactamente el
problema que los identificadores de campo de Protobuf resuelven hoy.
"""),
        "fortran": ("""
program serial
   implicit none
   character(len=60) :: linea
   character(len=20) :: nombre, valor
   integer :: p1

   read(*, '(A)') linea
   linea = adjustl(linea)

   p1 = index(linea, ' ')
   nombre = linea(1:p1-1)
   valor  = adjustl(linea(p1+1:))

   write(*, '(A)') 'serializado=' // trim(nombre) // ':' // trim(valor)
end program serial
""", """
**Lo que esta clase enseña en Fortran.** Fortran tiene un formato binario propio y una trampa clásica que
merece explicarse, porque es la que más datos científicos ha hecho ilegibles: **los ficheros sin
formato**.

```fortran
open(unit=10, file='datos.bin', form='unformatted')
write(10) n, matriz
```

**Eso escribe los bytes tal cual… más algo que casi nadie espera: los marcadores de registro.**

```text
Un registro secuencial sin formato de gfortran es:
   [longitud: 4 bytes] [los datos] [longitud otra vez: 4 bytes]
```

**Los marcadores existen para poder leer hacia atrás**, y **su tamaño y presencia dependen del
compilador**: gfortran usa 4 bytes por defecto —8 con `-frecord-marker=8`—, y otros compiladores usan
otra cosa.

**Así que un fichero sin formato escrito por ifort puede no leerse con gfortran**, y desde luego **no se
puede leer con un programa en C sin conocer el detalle**.

Y a eso se suma **el orden de los bytes**:

```fortran
open(10, file='datos.bin', form='unformatted', access='stream', &
     convert='big_endian')          ! extensión, no estándar
```

**`access='stream'` (Fortran 2003) es la solución moderna**: escribe **sin marcadores de registro**, byte
a byte, y es lo que hay que usar para intercambiar con otros lenguajes.

Y de ahí que la comunidad científica adoptara formatos con esquema, y merece nombrarlos porque resuelven
exactamente lo que el cierre de esta clase pide:

| Formato | Qué aporta |
|---|---|
| **NetCDF** | arreglos con dimensiones, unidades y metadatos; **autodescriptivo** |
| **HDF5** | jerárquico, con compresión, y paralelo con MPI |
| **CF conventions** | un vocabulario estándar de nombres para variables climáticas |
| **Zarr** | arreglos por trozos, pensado para almacenamiento en la nube |

**NetCDF y HDF5 son autodescriptivos**, que es la propiedad clave: **el fichero lleva dentro qué
variables contiene, con qué dimensiones, tipos y unidades**.

Y eso significa que **un programa que no conocía ese fichero puede leerlo y entenderlo** — que es
justamente lo que un formato sin esquema no permite, y la razón por la que un `.bin` de hace veinte años
suele ser irrecuperable.

Es la lección más práctica de esta página para cualquier dominio: **los datos sobreviven a los programas
que los escribieron**, así que **el formato tiene que llevar su propia descripción**.
"""),
        "ada": ("""
with Ada.Text_IO; use Ada.Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Serial is
   Linea  : String (1 .. 60);
   Ultimo : Natural;
   Sep    : Natural;
begin
   Get_Line (Linea, Ultimo);
   Sep := Ada.Strings.Fixed.Index (Linea (1 .. Ultimo), " ");

   Put_Line ("serializado=" & Linea (1 .. Sep - 1) & ":" &
             Ada.Strings.Fixed.Trim (Linea (Sep + 1 .. Ultimo), Ada.Strings.Both));
end Serial;
""", """
**Lo que esta clase enseña en Ada.** Ada tiene la serialización en el estándar, con dos mecanismos que
merece distinguir porque resuelven problemas distintos.

**El primero son los *streams*:**

```ada
with Ada.Streams.Stream_IO;

type Registro is record
   Codigo : Integer;
   Nombre : String (1 .. 20);
end record;

Registro'Write (Flujo, Mi_Registro);      --  serializar
Registro'Read  (Flujo, Otro);              --  y volver a leer
```

**`'Write` y `'Read` son atributos que el compilador genera para cualquier tipo**, incluidos los
compuestos y los etiquetados —donde `'Class'Output` **escribe también la etiqueta del tipo**, para poder
reconstruir el descendiente correcto—.

Es serialización automática con polimorfismo, en el lenguaje, sin biblioteca.

**Y su límite hay que decirlo, porque es el mismo que en todos lados**: **el formato lo define la
implementación**. Sirve para guardar y recuperar con el mismo programa, **no para intercambiar entre
lenguajes**.

**Y el segundo mecanismo sí sirve para eso: las cláusulas de representación** (clase 157).

```ada
type Trama is record
   Version  : Integer range 0 .. 15;
   Tipo     : Integer range 0 .. 255;
   Longitud : Integer range 0 .. 65_535;
end record;

for Trama use record
   Version  at 0 range 0 .. 3;
   Tipo     at 0 range 4 .. 11;
   Longitud at 2 range 0 .. 15;
end record;

for Trama'Size use 32;
for Trama'Bit_Order use System.High_Order_First;   --  ¡orden de bits explícito!
```

**Con eso, el registro de Ada tiene exactamente la disposición que exige el protocolo**, y
`Unchecked_Conversion` lo convierte en bytes.

Es la mejor herramienta de esta página para **implementar un formato binario definido por una norma** —
una trama de red, un mensaje CAN, un paquete de telemetría—, porque **el formato se declara y el
compilador comprueba que cuadra**.

Y merece la comparación que resume la clase: **`'Write` es cómodo y propietario; las cláusulas de
representación son laboriosas e interoperables**.

Es la misma disyuntiva que `Storable` frente a JSON en Perl, o la serialización nativa de Java frente a
Protobuf: **el formato propio del lenguaje siempre es más fácil y nunca cruza la frontera**.
"""),
        "pascal": ("""
program Serial;
{$MODE OBJFPC}{$H+}
uses SysUtils, StrUtils;

var
  Linea, Nombre, Valor: string;
  P: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);

  P := Pos(' ', Linea);
  Nombre := Copy(Linea, 1, P - 1);
  Valor  := Trim(Copy(Linea, P + 1, Length(Linea)));

  WriteLn('serializado=', Nombre, ':', Valor);
end.
""", """
**Lo que esta clase enseña en Pascal.** El ecosistema Delphi tiene un mecanismo de serialización que
merece contarse porque llegó muy pronto y por un camino inesperado: **el sistema de *streaming* de
componentes**.

```pascal
{ Un .dfm es la serialización de un árbol de objetos, en TEXTO }
object Form1: TForm1
  Left = 100
  Top = 50
  Caption = 'Mi ventana'
  object Button1: TButton
    Left = 20
    Caption = 'Aceptar'
    OnClick = Button1Click
  end
end
```

**Ese fichero se genera automáticamente desde los objetos y se vuelve a leer para reconstruirlos**, y
funciona **por la RTTI de los miembros `published`** (clase 139).

Es serialización automática dirigida por metadatos, **de 1995**, y es la misma idea que hoy usan los
serializadores por anotaciones de Java, C# y Python.

Y sus propiedades merecen verse porque son las que el cierre de esta clase pide:

- **Solo se escriben las propiedades que difieren del valor por defecto** —de ahí que un `.dfm` sea
  compacto—.
- **Al leer, una propiedad desconocida se puede ignorar**, con un manejador de errores. **Eso es
  tolerancia a lo desconocido**, la tercera regla del cierre.
- **Y hay una versión binaria y una textual del mismo formato**, convertibles entre sí.

Y el ecosistema moderno cubre el resto:

| Herramienta | Notas |
|---|---|
| **`fpjson` / `System.JSON`** | JSON en la distribución |
| **`TJSONSerializer` (Delphi)** | objetos a JSON **por RTTI extendida** |
| **mORMot** | serialización rápida, con soporte de esquemas |
| **`TFPObjectList` + streaming** | el mecanismo clásico |

Y merece señalar la trampa que este ecosistema enseña bien y que aplica a cualquier serialización por
reflexión: **si el formato se deriva automáticamente de los campos de la clase, renombrar un campo rompe
el formato**.

```pascal
[JSONName('cliente_id')]      { ← el nombre del CAMPO deja de ser el del FORMATO }
FClienteID: Integer;
```

**Anotar explícitamente el nombre externo** es la práctica que separa el modelo interno del contrato
publicado — y es la primera cosa que hay que hacer en cuanto ese contrato tenga más de un consumidor
(clase 160).
"""),
        "lisp": ("""
(let* ((linea (read-line))
       (sep (position #\\Space linea))
       (nombre (subseq linea 0 sep))
       (valor (string-trim '(#\\Space #\\Return) (subseq linea (1+ sep)))))
  (format t "serializado=~A:~A~%" nombre valor))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp tiene la propiedad que el "por qué" de esta clase
anunciaba, y es de las más elegantes del lenguaje: **lo que `print` escribe, `read` lo vuelve a leer**.

```lisp
(with-open-file (f "datos.lisp" :direction :output)
  (let ((*print-readably* t))
    (print '(:pedido 4711 :items ((:art "A1" :cant 3) (:art "B2" :cant 1))) f)))

(with-open-file (f "datos.lisp")
  (read f))     ; → la estructura, exactamente igual
```

**No hay serializador**: el lector y el impresor del lenguaje **ya son un formato de intercambio** (clase
104).

Y sus ventajas merecen enumerarse porque son reales:

- **Cero código**: no hay esquema que declarar ni biblioteca que instalar.
- **Estructuras anidadas arbitrarias**, sin límite de profundidad.
- **Y `*print-circle*` maneja referencias compartidas y ciclos**, con la notación `#1=` y `#1#` — cosa
  que JSON no puede.

Y las desventajas, que son las del cierre de esta clase:

- **Solo lo lee Lisp.** Es el formato propio del lenguaje, como `'Write` en Ada de esta página.
- **Y `read` es peligroso sobre datos externos** (clase 153): con `*read-eval*` activado, ejecuta código.

De ahí que el ecosistema tenga formatos serios para cruzar la frontera:

| Biblioteca | Formato |
|---|---|
| **jzon / cl-json / yason** | JSON |
| **cl-messagepack** | MessagePack |
| **cl-protobufs** | Protocol Buffers, con compilador de `.proto` |
| **conspack** | binario, pensado para Lisp, con referencias compartidas |

Y merece cerrar con una observación que Lisp permite ver mejor que ningún otro lenguaje de esta página y
que es la tesis del "por qué": **el formato de intercambio de datos y el formato del código son la misma
cosa cuando el lenguaje es homoicónico**.

Eso hace que **la configuración, los datos y el programa se escriban igual**, y es lo que hicieron
después EDN en Clojure, los ficheros de Emacs Lisp y, en otro nivel, YAML y TOML — que son intentos de
tener un formato de datos legible **sin** el peligro de que sea código.

Y ese es el compromiso exacto: **la homoiconicidad hace la serialización trivial y la seguridad
difícil**.
"""),
        "tcl": ("""
gets stdin linea
lassign [string trim $linea] nombre valor

puts "serializado=$nombre:$valor"
""", """
**Lo que esta clase enseña en Tcl.** Tcl tiene una propiedad que lo hace peculiar en esta clase y que
viene de la clase 081: **todo valor de Tcl ya tiene una representación textual canónica**.

```tcl
set d [dict create nombre "Ana" edad 30 items {a b c}]
puts $d
# → nombre Ana edad 30 items {a b c}

set d2 $d            ;# y esa cadena SE PUEDE VOLVER A INTERPRETAR como diccionario
```

**Una lista, un diccionario o un arreglo anidado son cadenas**, y **volver a interpretarlas es
gratuito**.

Es la misma propiedad que `print`/`read` en Lisp de esta página, y con la misma consecuencia práctica:
**guardar una estructura de Tcl es escribirla, y leerla es leer la línea**.

Y merece señalar el detalle de citación que lo hace correcto, porque es donde se cometen los errores:

```tcl
set l [list "un valor" "con {llaves}" "y \\"comillas\\""]
puts $l
# → {un valor} {con \\{llaves\\}} {y "comillas"}
```

**`list` genera la citación correcta automáticamente**, así que **el resultado siempre se puede volver a
leer**. Construir la cadena a mano con `join` **no lo garantiza**, y ese es el fallo clásico.

Y la regla que se deriva vale para cualquier lenguaje: **la serialización la hace la biblioteca, nunca la
concatenación**.

Y el ecosistema:

| Paquete | Formato |
|---|---|
| **`json` (tcllib)** | JSON, en las dos direcciones |
| **`huddle`** | estructuras con tipo, para generar JSON correcto |
| **`tdom`** | XML y XPath |
| **`csv` (tcllib)** | con citación correcta |
| **`binary format` / `binary scan`** | **formatos binarios, con plantilla** |

**`binary scan` merece la mención final** porque resuelve el problema de las columnas de la izquierda de
esta página con una sintaxis compacta:

```tcl
binary scan $bytes "IuIu a10 s" longitud tipo nombre flags
#              ↑ enteros big-endian sin signo, 10 chars, y un short
```

**Una cadena de plantilla describe la disposición del registro**, y `binary format` hace lo inverso.

Es la respuesta de un lenguaje sin tipos al problema de las cláusulas de representación de Ada: **no se
declara el tipo, se declara la plantilla en el punto de conversión** — más flexible, y sin ninguna
comprobación.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($nombre, $valor) = split ' ', $linea;

print "serializado=$nombre:$valor\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl tiene la colección más completa de serializadores de esta
página, y compararlos enseña bien el compromiso de la clase:

| Módulo | Formato | Nota |
|---|---|---|
| **`JSON::XS` / `Cpanel::JSON::XS`** | JSON | rapidísimo; el estándar de facto |
| **`Storable`** | binario **propio de Perl** | rápido y **solo lo lee Perl** |
| **`Data::Dumper`** | código Perl | legible y **se puede `eval`** |
| **`YAML::XS`** | YAML | legible por personas |
| **`Sereal`** | binario | **más rápido y compacto que Storable**, con compresión |
| **`Google::ProtocolBuffers`** | Protobuf | con esquema |
| **`Data::MessagePack`** | MessagePack | JSON binario |

**`Storable` merece la advertencia** porque ilustra el peligro del formato propio del lenguaje:

```perl
use Storable qw(store retrieve);
store($estructura, 'datos.bin');
my $x = retrieve('datos.bin');
```

**El formato de `Storable` ha cambiado entre versiones de Perl**, así que **un fichero guardado con una
versión puede no leerse con otra** — y no hay aviso hasta que ocurre.

Es la misma trampa que la serialización nativa de Java y que `pickle` en Python, y la regla que se
deriva es la del cierre de esta clase: **el formato propio del lenguaje sirve para una caché, nunca para
archivar ni para intercambiar**.

Y Perl aporta a esta clase las dos advertencias que más problemas causan en JSON, y merecen decirse
porque son universales:

**Una, los números grandes.**

```perl
# JSON no distingue enteros de reales, y JavaScript solo tiene double
# → un identificador de 64 bits pierde precisión al pasar por JavaScript
{"id": 9007199254740993}      # se convierte en 9007199254740992
```

**La solución que la industria adoptó es enviar los identificadores grandes como cadenas**, y merece
conocerse porque parece un rodeo y no lo es.

**Y dos, la codificación.**

```perl
use JSON::XS;
my $json = JSON::XS->new->utf8->canonical->encode($datos);
```

**`->utf8` codifica a bytes; sin él, se devuelven caracteres** — y confundirlos produce la doble
codificación clásica que convierte los acentos en `Ã¡` (clase 093).

**Y `->canonical` ordena las claves**, lo que hace la salida **determinista** — imprescindible si se va a
comparar, firmar o versionar (clase 144).
"""),
        "cpp": ("""
#include <iostream>
#include <string>

int main() {
    std::string nombre, valor;
    if (!(std::cin >> nombre >> valor)) return 1;

    std::cout << "serializado=" << nombre << ':' << valor << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ tiene un problema estructural con esta clase que merece
enunciarse porque explica el ecosistema entero: **C++ no tiene reflexión**.

```cpp
struct Pedido { int id; std::string cliente; double total; };
// No hay forma estándar de preguntar "¿qué campos tiene Pedido?"
```

**Así que la serialización automática es imposible**, y las tres salidas que el ecosistema encontró son
las tres formas de esta clase:

**Una, escribirla a mano:**

```cpp
void to_json(nlohmann::json& j, const Pedido& p) {
    j = {{"id", p.id}, {"cliente", p.cliente}, {"total", p.total}};
}
```

**Dos, declararla una vez con plantillas:**

```cpp
template <class Archive>
void serialize(Archive& ar, Pedido& p) {      // Boost.Serialization, cereal
    ar(CEREAL_NVP(p.id), CEREAL_NVP(p.cliente), CEREAL_NVP(p.total));
}
```

**Y tres —la que la industria eligió—: generar el código desde un esquema.**

```protobuf
message Pedido {
  int32  id      = 1;
  string cliente = 2;
  double total   = 3;
}
```

```bash
protoc --cpp_out=. --python_out=. --java_out=. pedido.proto
```

**Y ahí está la razón por la que Protocol Buffers ganó**, y merece verla: **el esquema es la fuente de
verdad y de él se generan las clases de todos los lenguajes**.

Y los números `= 1`, `= 2`, `= 3` son la pieza que resuelve el problema del cierre de esta clase:

```text
- El identificador viaja en el mensaje, NO el nombre del campo → compacto
- Un campo nuevo con un identificador nuevo lo IGNORAN los lectores antiguos
- Un campo borrado deja su identificador RESERVADO para siempre
- Y renombrar un campo NO rompe nada, porque el nombre no viaja
```

**`reserved 3, 7 to 9; reserved "total_viejo";`** es la declaración que impide reutilizar un
identificador — la segunda regla del cierre, hecha comprobable por el compilador de esquemas.

Y merece la comparación que ordena la elección:

| Formato | Tamaño | Velocidad | Legible | Esquema |
|---|---|---|---|---|
| **JSON** | grande | media | **sí** | opcional (JSON Schema) |
| **MessagePack** | medio | rápida | no | opcional |
| **Protobuf** | pequeño | muy rápida | no | **obligatorio** |
| **FlatBuffers / Cap'n Proto** | pequeño | **sin analizar** | no | obligatorio |
| **CBOR** | medio | rápida | no | opcional |

**FlatBuffers merece la mención final**: el mensaje **se lee directamente de la memoria sin
deserializar**, accediendo por desplazamientos.

Es la técnica de los registros de longitud fija de COBOL de esta página —**acceder por posición sin
analizar**— reinventada para juegos y sistemas de baja latencia, con la ventaja añadida de la evolución
de esquema.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi SERIAL;
  linea char(60) const;
end-pi;

dcl-s texto  varchar(60);
dcl-s pos    int(10);
dcl-s nombre varchar(20);
dcl-s valor  varchar(20);

texto = %trim(linea);
pos = %scan(' ' : texto);

nombre = %subst(texto : 1 : pos - 1);
valor  = %trim(%subst(texto : pos + 1));

dsply ('serializado=' + nombre + ':' + valor);

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG recibió en 2018 y 2019 dos instrucciones que cambiaron por
completo su posición en esta clase, y merecen explicarse porque son de un diseño poco común:
**`DATA-INTO` y `DATA-GEN`**.

```rpgle
dcl-ds pedido qualified;
  id       int(10);
  cliente  varchar(50);
  total    packed(11:2);
  numLineas int(5);
  linea likeds(tLinea) dim(50);
end-ds;

// Analizar JSON DIRECTAMENTE a la estructura
data-into pedido %data(jsonRecibido) %parser('YAJLINTO');

// Y generarlo
data-gen pedido %data(salida) %gen('YAJLDTAGEN');
```

**`DATA-INTO` analiza JSON o XML y rellena una estructura de datos de RPG**, emparejando **por nombre de
subcampo**.

Y merece destacar la decisión de diseño que lo hace especial: **el analizador es un parámetro**.

```rpgle
%parser('YAJLINTO')        // JSON, con YAJL
%parser('XML-INTO')         // XML
%parser('MIPARSER')          // uno propio, para CSV o para un formato interno
```

**IBM no incorporó un analizador de JSON: definió una interfaz de analizadores.** Cualquiera puede
escribir uno —en RPG, en C o en el lenguaje que sea— y **`DATA-INTO` lo usa igual**.

Es exactamente la separación de la clase 158: **la instrucción es la capa idiomática y el analizador es
la capa de abajo, intercambiable**.

Y hay dos detalles prácticos que esta clase debe recoger porque son la tercera regla del cierre:

```rpgle
data-into pedido %data(json : 'allowextra=yes allowmissing=yes')
                 %parser('YAJLINTO');
```

**`allowextra=yes` ignora los campos que llegan y no están en la estructura** —tolerancia a lo
desconocido— **y `allowmissing=yes` acepta que falten** —campos opcionales—.

**Sin esas dos opciones, `DATA-INTO` falla ante cualquier campo inesperado**, y eso hace imposible
desplegar por partes: **el emisor no puede añadir un campo hasta que todos los receptores se
actualicen**.

Es la lección más práctica de esta clase, y aquí se ve con nombre propio: **la tolerancia se configura, y
hay que acordarse de configurarla**.
"""),
        "pli": ("""
 serial: procedure options(main);

    declare linea  char(60) varying;
    declare nombre char(20) varying;
    declare valor  char(20) varying;
    declare p      fixed binary(31);

    get edit (linea) (a(60));
    linea = trim(linea);

    p = index(linea, ' ');
    nombre = substr(linea, 1, p - 1);
    valor = trim(substr(linea, p + 1));

    put skip list ('serializado=' || nombre || ':' || valor);

 end serial;
""", """
**Lo que esta clase enseña en PL/I.** PL/I tiene la propiedad que el "por qué" de esta clase anunciaba, y
es de 1964: **`PUT DATA` escribe con nombres, y `GET DATA` lo vuelve a leer**.

```pli
 declare 1 pedido,
           2 id      fixed binary(31) initial(4711),
           2 cliente char(20) varying  initial('ACME'),
           2 total   fixed decimal(11,2) initial(1234.56);

 put data (pedido);
 /* → PEDIDO.ID= 4711  PEDIDO.CLIENTE='ACME'  PEDIDO.TOTAL= 1234.56; */

 get data (pedido);      /* y lo LEE de vuelta */
```

**Eso es serialización con nombres, autodescriptiva y reversible**, en dos sentencias del lenguaje.

Y merece compararlo con lo que hoy se considera moderno, porque las propiedades son las mismas:

| Propiedad | `PUT DATA` (1964) | JSON |
|---|---|---|
| Autodescriptivo | **sí**: lleva los nombres | sí |
| Legible por personas | sí | sí |
| Reversible | **sí**: `GET DATA` | sí |
| Tipos | **sí**: la declaración los da | limitados |
| **Decimales exactos** | **sí**: `FIXED DECIMAL` | **no**: `double` |
| Interoperable | **no**: solo PL/I | **sí** |

**La fila de los decimales merece subrayarse**, porque es la limitación de JSON que más problemas causa
en sistemas financieros y que este formato no tenía: **`1234.56` en `FIXED DECIMAL(11,2)` es exacto**;
en JSON depende de cómo lo lea el receptor.

Es la misma razón por la que Protobuf tiene `decimal` en algunas variantes, por la que las APIs
financieras envían los importes como cadenas, y por la que existen tipos decimales en todos los
lenguajes serios (clase 072).

Y PL/I aporta también el formato binario declarado, que es el de COBOL en esta página:

```pli
 declare 1 registro based(p),
           2 codigo  char(4),
           2 importe fixed decimal(9,2),     /* empaquetado */
           2 fecha   picture '99999999';
```

**Una estructura declarada es un formato de registro**, y `read file(f) into(registro)` **lo lee tal
cual**.

Y merece cerrar con lo que este mundo enseña y que el cierre de esta clase recoge: **estos formatos
sobrevivieron cincuenta años porque el esquema estaba escrito y era obligatorio**.

Un fichero de datos del mainframe **viene siempre acompañado de su copybook o de su declaración**, y sin
él no se puede leer. Es más rígido que JSON y tiene una ventaja que se aprecia con el tiempo: **no
existen ficheros huérfanos cuyo significado nadie recuerde**.
"""),
        "mumps": ("""
SERIAL ; Serializar un par nombre-valor -- clase 159
 read linea
 new nombre, valor
 set nombre = $piece(linea, " ", 1)
 set valor = $piece(linea, " ", 2)
 write "serializado=", nombre, ":", valor, !
 quit
""", """
**Lo que esta clase enseña en M.** M tiene una relación con esta clase que merece explicarse porque es
distinta de todas: **la serialización está en el modelo de datos**.

```mumps
 set ^PEDIDO(4711, "CLIENTE") = "ACME"
 set ^PEDIDO(4711, "TOTAL") = 1234.56
 set ^PEDIDO(4711, "LINEA", 1) = "A1^3"
 set ^PEDIDO(4711, "LINEA", 2) = "B2^1"
```

**Una global ya es una estructura jerárquica persistente** (clase 099), así que **guardar no requiere
serializar**: la estructura *es* el almacenamiento.

Y el formato interno de cada nodo es la otra mitad, y es característico de este mundo: **los campos
separados por acento circunflejo**.

```mumps
 set ^DPT(dfn, 0) = nombre_"^"_sexo_"^"_fechaNac_"^"_ssn
 set nombre = $piece(^DPT(dfn, 0), "^", 1)
```

**Eso es un registro de campos delimitados**, y `$piece` es el acceso por posición.

Y merece señalar las tres propiedades que tiene y las tres que le faltan, porque es un buen resumen de
esta clase:

**Tiene**: es compacto, es rapidísimo de leer con `$piece`, y **añadir un campo al final no rompe nada**
—los lectores viejos siguen leyendo las posiciones que conocen—, que es exactamente la primera regla del
cierre.

**Le falta**: **no hay esquema declarado en el código**. La correspondencia entre la posición 3 y "fecha
de nacimiento" **vive en el diccionario de FileMan** (clase 149) o, peor, en la cabeza de alguien.

Y de ahí que la interoperabilidad de estos sistemas haya requerido siempre una capa de traducción, que
hoy es la que la clase 158 nombraba:

| Capa | Qué hace |
|---|---|
| **FileMan API** | leer y escribir por **nombre de campo**, no por posición |
| **RPC Broker** | el formato de transporte histórico |
| **HL7 v2** | el estándar sanitario clásico: **campos delimitados por `\\|`** |
| **FHIR** | el moderno: **recursos JSON con esquema** |
| **`%JSON.Adaptor` (IRIS)** | objetos a JSON automáticamente |

**HL7 v2 merece la mención** porque es el mismo diseño que las globals: **segmentos y campos separados
por delimitadores, con posiciones fijas y un diccionario aparte**. Es de 1987, mueve la mayor parte de
los mensajes clínicos del mundo, y tiene exactamente los mismos problemas: **compacto, rápido y sin
esquema legible por máquina**.

**Y FHIR es la respuesta**: JSON con esquema, recursos definidos y validación — la tercera regla del
cierre aplicada a un dominio entero, treinta años después.
"""),
        "smalltalk": ("""
| linea partes |

linea := stdin nextLine trimBoth.
partes := linea substrings: ' '.

Transcript
    show: 'serializado=', (partes at: 1), ':', (partes at: 2);
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk tiene la propiedad de Lisp y PL/I de esta página, y
con una vuelta de tuerca: **`storeString` produce código Smalltalk que reconstruye el objeto**.

```smalltalk
| p |
p := OrderedCollection with: 1 with: 'dos' with: 3/4.
p storeString.
"→ '((OrderedCollection new) add: 1; add: ''dos''; add: 3/4; yourself)'"

Compiler evaluate: p storeString.     "→ una colección igual"
```

**Y el detalle que lo hace notable: `3/4` sobrevive como fracción exacta**, no como `0.75`. Smalltalk
tiene números racionales y enteros de precisión arbitraria (clase 072), y **la serialización los
conserva**.

Es una propiedad que casi ningún formato de intercambio tiene, y que la columna de la izquierda de esta
página —COBOL con `COMP-3`, PL/I con `FIXED DECIMAL`— también tenía por otros medios.

Y el ecosistema tiene serializadores serios:

| Herramienta | Notas |
|---|---|
| **Fuel** | binario, rapidísimo; **serializa CUALQUIER objeto, incluidos bloques y clases** |
| **STON** | textual, legible, tipo JSON pero con clases y referencias |
| **NeoJSON** | JSON, con mapeo declarativo |
| **`storeString`** | código, para casos pequeños |

**Fuel merece el detalle** porque hace algo que ningún otro serializador de esta página puede: **serializa
grafos de objetos con ciclos, incluidas las clases y los métodos compilados**.

```smalltalk
FLSerializer serialize: unGrafoCompleto toFileNamed: 'estado.fuel'.
```

**Se puede guardar un proceso suspendido, con su pila, y reanudarlo después** — que es la misma capacidad
que hacía posible enviar el contexto de un error para depurarlo en otra máquina (clase 141).

Y **STON** es el que resuelve el problema de esta clase, y su diseño merece verse:

```text
Pedido {
  #id : 4711,
  #cliente : 'ACME',
  #total : 1234.56,
  #lineas : [ Linea { #art : 'A1', #cant : 3 } ]
}
```

**Es JSON con el nombre de la clase delante**, y con referencias compartidas (`@1`).

Y eso ilustra la tensión final de esta clase: **para que un formato conserve la identidad de las clases y
los objetos compartidos, tiene que salir de JSON** — y en cuanto sale, **deja de ser interoperable**.

Es el mismo compromiso que `'Write` en Ada, `Storable` en Perl y `pickle` en Python: **el formato que
captura todo lo que el lenguaje sabe es el formato que solo ese lenguaje entiende**.
"""),
    },
)

# ---------------------------------------------------------------------------
# 160 — Contratos de API: REST, gRPC y esquemas
# ---------------------------------------------------------------------------
SPECS["160"] = dict(
    gancho="""
Componer un contrato: `GET /users`. Dos palabras y una barra, y ahí está el acuerdo entre dos sistemas
que quizá no comparten lenguaje, empresa ni continente. Y esta clase existe porque **ese acuerdo es lo
único que impide que un cambio en un lado rompa el otro**. Y aquí hay una genealogía que conviene
conocer: **el contrato de interfaz descrito en un lenguaje aparte, del que se generan los clientes y los
servidores, no lo inventó gRPC — lo inventó CORBA en 1991, y antes ASN.1 en 1984**.
""",
    porque="""
Aquí el concepto es el **contrato como artefacto independiente**, y estos lenguajes lo enseñan porque
**llevan décadas conviviendo con contratos que no pueden romperse**: la COMMAREA de una transacción
CICS, la firma de un programa de servicio de IBM i, la especificación de un paquete Ada, el registro de
una RPC de VistA. Y todos aportan la misma lección desde ángulos distintos: **un contrato sirve si está
declarado en un sitio, si se puede comprobar y si tiene una regla de evolución**.

Y aparece la pregunta que decide la arquitectura: **¿el contrato se escribe primero, o se deduce del
código?**
""",
    cierre="""
Lo transferible: **el contrato es más duradero que cualquiera de sus dos lados, así que merece más
cuidado que ninguno de los dos**. De ahí las tres prácticas que aparecen en toda la página: **escribirlo
en un artefacto propio y versionado** —no deducirlo del código, porque entonces cualquier refactorización
lo cambia—; **comprobarlo automáticamente en los dos lados**, con pruebas de contrato que fallen en la
integración continua cuando alguien lo rompa; y **evolucionarlo solo añadiendo**, porque en cuanto hay
más de un consumidor **ya no se puede desplegar todo a la vez** — que es exactamente el problema que la
clase 148 planteaba con los datos.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. CONTRATO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(60).
01  C-VERBO PIC X(10).
01  C-REC   PIC X(30).

PROCEDURE DIVISION.
    ACCEPT LINEA
    UNSTRING LINEA DELIMITED BY ALL SPACES
        INTO C-VERBO C-REC
    END-UNSTRING

    DISPLAY "contrato=" FUNCTION TRIM(C-VERBO)
            " /" FUNCTION TRIM(C-REC)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** El mundo CICS tiene un contrato con nombre propio, y merece
explicarlo porque es uno de los más antiguos en producción continua: **la COMMAREA**.

```cobol
       01  COMMAREA-PEDIDO.
           05  CA-VERSION      PIC 9(2).        *> ¡la VERSIÓN, en el contrato!
           05  CA-OPERACION    PIC X(10).
           05  CA-CLIENTE      PIC X(10).
           05  CA-IMPORTE      PIC S9(9)V99 COMP-3.
           05  CA-COD-RETORNO  PIC 9(4).
           05  CA-MENSAJE      PIC X(80).
           05  FILLER          PIC X(200).      *> reservado para el futuro
```

**Ese copybook es el contrato entre el programa que llama y el que responde**, y las dos partes lo
comparten como fichero.

Y merece destacar las dos decisiones que aparecen ahí y que son el cierre de esta clase:

**`CA-VERSION` en el propio mensaje.** El receptor lee la versión y decide cómo interpretar el resto —lo
que permite que convivan clientes viejos y nuevos.

**Y el `FILLER` reservado**, que es la primera regla del cierre: **espacio para añadir sin mover nada**.

Y la limitación histórica de la COMMAREA merece contarse porque provocó un cambio de diseño: **está
limitada a 32 KB**. Cuando eso se quedó corto, CICS introdujo **los *channels* y *containers***:

```cobol
           EXEC CICS PUT CONTAINER('PETICION') FROM(DATOS)
                     CHANNEL('CANAL-PEDIDO') END-EXEC
           EXEC CICS LINK PROGRAM('PGMPED') CHANNEL('CANAL-PEDIDO') END-EXEC
           EXEC CICS GET CONTAINER('RESPUESTA') INTO(RESULTADO) END-EXEC
```

**Los contenedores tienen nombre, tamaño ilimitado y se pueden añadir sin romper nada** — porque **el
receptor pide los que conoce e ignora los demás**.

Es exactamente la tercera regla del cierre de esta clase, y es la misma solución que los campos con
identificador de Protobuf (clase 159): **pasar de posiciones fijas a elementos con nombre**.

Y hoy, la capa que expone todo eso como API moderna:

```text
z/OS Connect lee el copybook y genera OpenAPI 3.0
El contrato REST se deriva del contrato COBOL, y se publica.
```

**Y ahí aparece la pregunta del "por qué" de esta clase**: ese contrato **se deduce del código**, así que
**un cambio en el copybook cambia la API publicada**.

La práctica correcta —y la que la disciplina de estos sistemas ya aplicaba— es la contraria: **el
copybook de la interfaz es un artefacto propio, distinto de las estructuras internas del programa**, y se
gestiona con su propio ciclo de aprobación.
"""),
        "fortran": ("""
program contrato
   implicit none
   character(len=60) :: linea
   character(len=10) :: verbo
   character(len=30) :: recurso
   integer :: p1

   read(*, '(A)') linea
   linea = adjustl(linea)

   p1 = index(linea, ' ')
   verbo = linea(1:p1-1)
   recurso = adjustl(linea(p1+1:))

   write(*, '(A)') 'contrato=' // trim(verbo) // ' /' // trim(recurso)
end program contrato
""", """
**Lo que esta clase enseña en Fortran.** El mundo científico tiene contratos de interfaz muy serios, y
merecen conocerse porque **no son APIs de red: son especificaciones de bibliotecas y de formatos de
datos**.

**El caso mayor es el de la clase 149: BLAS y LAPACK.**

```text
La especificación de BLAS define, para cada rutina:
  - el nombre exacto y el orden de los argumentos
  - qué hace cada uno y en qué dirección
  - qué valores son válidos y qué pasa si no lo son
  - y la semántica matemática exacta
```

**Y esa especificación es el contrato**: Intel, AMD, NVIDIA y OpenBLAS escriben implementaciones
independientes **que son intercambiables** porque todas cumplen el mismo documento.

Es exactamente lo que un contrato de API busca, con una diferencia notable: **lleva cuarenta años sin
romperse**.

Y merece preguntarse por qué funcionó tan bien, porque las razones son las del cierre de esta clase:

**Uno, el contrato es un artefacto propio** —un documento y unas cabeceras de referencia—, no la
implementación de nadie.

**Dos, existe una implementación de referencia** contra la que comparar (clase 140).

**Y tres, se evoluciona solo añadiendo**: BLAS ha crecido con niveles y con variantes nuevas, **sin
cambiar nunca la firma de una rutina existente**.

Y el segundo contrato de este mundo es de datos, y ya apareció en la clase 159: **las convenciones CF**.

```text
CF Conventions define, para ficheros NetCDF de datos climáticos:
  - los nombres estándar de las variables (air_temperature, sea_surface_height...)
  - las unidades, con una sintaxis formal
  - cómo se declaran las coordenadas, las mallas y el tiempo
  - y cómo se marca lo que falta
```

**Con eso, un programa puede leer un fichero de un centro que no conoce y saber qué contiene**, porque el
vocabulario está acordado.

Es un contrato **semántico**, no solo estructural, y merece destacarlo porque es lo que le falta a la
mayoría de las APIs: **JSON Schema dice que un campo es un número; CF dice que es una temperatura del
aire en kelvin a dos metros del suelo**.

Y esa diferencia —**estructura frente a significado**— es la que separa una interfaz que se puede
consumir de una que además se puede entender.
"""),
        "ada": ("""
with Ada.Text_IO; use Ada.Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Contrato is
   Linea  : String (1 .. 60);
   Ultimo : Natural;
   Sep    : Natural;
begin
   Get_Line (Linea, Ultimo);
   Sep := Ada.Strings.Fixed.Index (Linea (1 .. Ultimo), " ");

   Put_Line ("contrato=" & Linea (1 .. Sep - 1) & " /" &
             Ada.Strings.Fixed.Trim (Linea (Sep + 1 .. Ultimo), Ada.Strings.Both));
end Contrato;
""", """
**Lo que esta clase enseña en Ada.** Ada tiene el contrato dentro del lenguaje, y esta clase es el sitio
para verlo como lo que es: **una especificación de paquete es un contrato de API completo** (clase 154).

```ada
package Cuentas is

   type Cuenta is private;
   type Importe is delta 0.01 range 0.00 .. 1_000_000.00;

   Saldo_Insuficiente : exception;

   function Saldo (C : Cuenta) return Importe
     with Post => Saldo'Result >= 0.00;

   procedure Retirar (C : in out Cuenta; Cantidad : Importe)
     with Pre  => Cantidad > 0.00,
          Post => Saldo (C) = Saldo (C'Old) - Cantidad;

private
   ...
end Cuentas;
```

**Ahí está todo lo que un contrato de API necesita**, y merece enumerarlo porque la correspondencia es
exacta:

| Elemento de Ada | Equivalente en una API |
|---|---|
| Los subprogramas públicos | los puntos de acceso |
| Los tipos y subtipos con rango | **el esquema, con validación** |
| Las excepciones declaradas | los códigos de error documentados |
| **`Pre`** | qué peticiones son válidas |
| **`Post`** | qué garantiza la respuesta |
| La parte `private` | lo que no es contrato y puede cambiar |

**Y la diferencia con un contrato de API típico es que este se comprueba** (clase 118): las
precondiciones fallan en ejecución, y con SPARK se demuestran.

Es la primera práctica del cierre —**un artefacto propio y versionado**— con la ventaja de que **el
compilador se niega a compilar si la implementación no lo cumple**.

Y merece contar el contrato más famoso del mundo de Ada, porque es una lección de esta clase: **el
estándar mismo**.

```text
El Ada Reference Manual es un documento normativo, numerado párrafo a párrafo,
con Ada Issues (AI) que registran cada aclaración y cada cambio,
y un conjunto de PRUEBAS DE CONFORMIDAD -la ACATS- que un compilador debe pasar.
```

**La ACATS es un contrato ejecutable para implementadores de compiladores**: miles de programas de
prueba que verifican que el compilador cumple el estándar.

Es, exactamente, lo que la segunda práctica del cierre pide —**comprobar el contrato automáticamente**—
aplicado al lenguaje entero, y explica por qué el código Ada es tan portable entre compiladores comparado
con C++ (clase 147).
"""),
        "pascal": ("""
program Contrato;
{$MODE OBJFPC}{$H+}
uses SysUtils, StrUtils;

var
  Linea, Verbo, Recurso: string;
  P: Integer;

begin
  ReadLn(Linea);
  Linea := Trim(Linea);

  P := Pos(' ', Linea);
  Verbo := Copy(Linea, 1, P - 1);
  Recurso := Trim(Copy(Linea, P + 1, Length(Linea)));

  WriteLn('contrato=', Verbo, ' /', Recurso);
end.
""", """
**Lo que esta clase enseña en Pascal.** El mundo Delphi vivió de cerca la generación de contratos más
ambiciosa de los años noventa, y merece contarla porque es la abuela de gRPC: **COM y su biblioteca de
tipos**.

```pascal
{ Una interfaz COM en Object Pascal }
type
  ICalculadora = interface(IUnknown)
    ['{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}']    { ← el GUID: la IDENTIDAD }
    function Sumar(A, B: Integer): Integer; safecall;
  end;
```

Y las tres decisiones de COM que merecen destacarse porque resuelven el cierre de esta clase:

**Una, el GUID como identidad de la interfaz.** Un identificador único global, no un nombre.

**Y la regla que va con él es tajante y es la mejor formulación de la tercera práctica del cierre**:

> **Una interfaz COM publicada NUNCA se modifica. Si hace falta cambiarla, se crea `IFoo2`.**

**Nada de añadir un método, nada de cambiar un parámetro.** Y por eso existen `IShellFolder`,
`IShellFolder2`, `IPersistStream`, `IPersistStreamInit`… **con nombres feos y compatibilidad de
treinta años**.

Es una disciplina extrema y funciona: **binarios de 1997 siguen funcionando en Windows actual**.

**Dos, la biblioteca de tipos** —la *type library*—, que es el contrato legible por máquina: **describe
las interfaces, los métodos, los tipos y las constantes**, y **de ella se generan los enlaces
automáticamente** en Delphi, en C++, en Visual Basic y en .NET (clase 158).

**Y tres, `safecall`**, que ya apareció en la clase 157: **la convención de llamada convierte las
excepciones en códigos de error**, así que **el contrato incluye la semántica de fallo** y funciona entre
lenguajes con modelos de excepciones distintos.

Y el ecosistema Pascal actual está en el mundo REST:

| Herramienta | Qué hace |
|---|---|
| **mORMot** | servicios con interfaces de Pascal, y OpenAPI generado |
| **DataSnap / RAD Server** | servicios REST integrados |
| **`OpenAPI` generators** | generan cliente Delphi desde una especificación |

Y merece cerrar con la comparación que esta página permite: **COM exigía disciplina y daba compatibilidad
binaria de décadas; REST no exige nada y por eso casi todas las APIs REST rompen a sus clientes al menos
una vez**.

La diferencia no está en la tecnología: está en **si hay una regla escrita sobre qué se puede cambiar**.
"""),
        "lisp": ("""
(let* ((linea (read-line))
       (sep (position #\\Space linea))
       (verbo (subseq linea 0 sep))
       (recurso (string-trim '(#\\Space #\\Return) (subseq linea (1+ sep)))))
  (format t "contrato=~A /~A~%" verbo recurso))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp aporta a esta clase una capacidad que su naturaleza
hace natural y que merece destacarse: **el contrato puede ser un dato del que se genere todo**.

```lisp
(define-api pedidos
  (:get "/pedidos/:id"
   :respuesta (:id integer :cliente string :total decimal)
   :errores ((404 "no encontrado")))
  (:post "/pedidos"
   :cuerpo (:cliente string :items (list-of item))
   :respuesta (:id integer)))
```

**Y de esa única declaración se puede generar, con macros** (clase 122):

- **Las rutas del servidor y la validación de la entrada.**
- **El cliente**, con funciones tipadas.
- **La documentación** en OpenAPI.
- **Y las pruebas de contrato.**

Es la primera práctica del cierre —**el contrato como artefacto propio**— con la particularidad de que
**el artefacto vive en el mismo lenguaje**, así que no hay un paso de generación separado ni un fichero
que se olvide de regenerar.

Es la misma idea que la clase 158 mostraba con los enlaces, aplicada a las APIs.

Y merece señalar el compromiso, porque es el de siempre: **ese contrato solo lo entiende Lisp**. Para que
lo entienda el resto del mundo hay que **emitir OpenAPI o un `.proto`** desde ahí — lo que devuelve el
problema al terreno común.

Y el ecosistema:

| Biblioteca | Notas |
|---|---|
| **Hunchentoot / Clack / Woo** | servidores HTTP |
| **Snooze / cl-rest-server** | rutas declarativas |
| **cl-protobufs** | Protobuf con compilador de `.proto` |
| **cl-json-schema** | validación contra JSON Schema |

Y Lisp permite cerrar esta clase con una observación que la atraviesa: **un contrato es una gramática, y
las gramáticas se pueden ejecutar en las dos direcciones**.

De una misma descripción se puede **generar** un mensaje válido y **validar** uno recibido — y las
herramientas que hacen las dos cosas desde la misma fuente son las que de verdad garantizan que no
divergen.

Es la razón por la que los formatos con esquema obligatorio —Protobuf, ASN.1— tienen menos incidentes de
incompatibilidad que los que lo tienen opcional: **cuando la validación y la generación salen del mismo
sitio, no pueden discrepar**.
"""),
        "tcl": ("""
gets stdin linea
lassign [string trim $linea] verbo recurso

puts "contrato=$verbo /$recurso"
""", """
**Lo que esta clase enseña en Tcl.** Tcl aporta a esta clase la perspectiva del lenguaje que **consume**
contratos ajenos, que es el papel de un lenguaje de pegamento (clase 155).

```tcl
package require http
package require json

set tok [http::geturl "https://api.ejemplo.com/pedidos/4711" \\
             -headers {Accept application/json}]
set datos [json::json2dict [http::data $tok]]
http::cleanup $tok

dict get $datos cliente
```

**Y ahí aparece el problema central de esta clase desde el lado del consumidor**: `dict get $datos
cliente` **falla si el campo no está**, y **nada avisó de que podía no estar**.

Y las tres defensas que un consumidor debería aplicar y que casi nadie aplica merecen enumerarse:

```tcl
# 1. valor por defecto en vez de fallo
set cliente [expr {[dict exists $datos cliente] ? [dict get $datos cliente] : ""}]

# 2. validar contra el esquema publicado, no confiar
package require json::write
# (o validar con una biblioteca de JSON Schema)

# 3. y NO fallar por campos desconocidos: ignorarlos
```

**La tercera es la que hace posible que el emisor evolucione** (clase 159), y es la tercera regla del
cierre de esta clase vista desde el otro lado: **el consumidor tolerante es lo que permite al proveedor
añadir**.

Y Tcl aporta un caso de contrato muy distinto y muy real, que merece contarse porque es el suyo: **los
flujos de diseño de circuitos**.

```tcl
# El "contrato" entre el diseñador y la herramienta:
read_verilog diseno.v
set_clock_period 2.5
compile_ultra
write_verilog netlist.v
```

**Los comandos de Tcl que una herramienta de Synopsys o Cadence expone son su API**, y **cambiarlos entre
versiones rompe flujos de diseño de decenas de miles de líneas** que las empresas han afinado durante
años.

Y por eso esas herramientas mantienen **compatibilidad de comandos durante décadas**, con la misma
disciplina que COM en esta página: **los comandos viejos siguen, marcados como obsoletos, y los nuevos se
añaden**.

Es la misma conclusión, en un dominio inesperado: **cuando el coste de romper es alto y visible, la
disciplina de contrato aparece sola**.
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my ($verbo, $recurso) = split ' ', $linea;

print "contrato=$verbo /$recurso\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl aporta a esta clase la práctica que el cierre nombra en segundo
lugar y que es la más útil de todas: **comprobar el contrato automáticamente en los dos lados**.

Y el ecosistema tiene la herramienta que la implementa:

```perl
use Test::More;
use JSON::Schema::Modern;

my $esquema = decode_json(path('contratos/pedido.schema.json')->slurp);
my $validador = JSON::Schema::Modern->new(schema => $esquema);

my $respuesta = $cliente->get('/pedidos/4711');
ok($validador->evaluate(decode_json($respuesta->content))->valid,
   'la respuesta cumple el contrato publicado');
```

**Esa prueba se ejecuta en el lado del proveedor y en el del consumidor, con el mismo fichero de
esquema**, y falla en la integración continua si alguien lo rompe (clase 147).

Y merece explicar la técnica que va un paso más allá y que resuelve el problema real, porque es una de
las mejores ideas de la última década: **las pruebas de contrato dirigidas por el consumidor**.

```text
1. Cada CONSUMIDOR escribe qué necesita de la API, como un "pacto":
     "cuando pido GET /pedidos/4711, espero un objeto con id y total"
2. Ese pacto se publica en un repositorio compartido.
3. El PROVEEDOR ejecuta TODOS los pactos de todos sus consumidores en su CI.
4. Si un cambio rompe a alguien, el proveedor se entera ANTES de desplegar.
```

**Eso invierte la responsabilidad**, y es lo que lo hace funcionar: **el proveedor no tiene que adivinar
qué usan sus consumidores — se lo dicen, en forma ejecutable**.

Y resuelve el problema práctico que la clase 148 planteaba: **cómo desplegar sin coordinar a todo el
mundo a la vez**.

El ecosistema:

| Herramienta | Notas |
|---|---|
| **`Pact::Perl` / Pact en general** | pruebas de contrato dirigidas por el consumidor |
| **`JSON::Schema::Modern`** | validación de JSON Schema |
| **`OpenAPI::Client`** | cliente generado desde una especificación OpenAPI |
| **`Mojolicious::Plugin::OpenAPI`** | **servidor que valida entrada y salida contra la especificación** |

**El último merece la mención final** porque aplica la primera práctica del cierre de la forma más
estricta: **la especificación OpenAPI es la fuente, y el marco valida cada petición y cada respuesta
contra ella en ejecución**.

**Si el código devuelve algo que no cumple lo publicado, falla en desarrollo** — con lo que la
documentación no puede mentir, que es el fallo más común de las APIs escritas a mano.
"""),
        "cpp": ("""
#include <iostream>
#include <string>

int main() {
    std::string verbo, recurso;
    if (!(std::cin >> verbo >> recurso)) return 1;

    std::cout << "contrato=" << verbo << " /" << recurso << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ es donde vive **gRPC**, y esta clase es el sitio para ver por
qué su diseño es el que es — y de dónde viene, que es el dato del gancho.

```protobuf
syntax = "proto3";

service Pedidos {
  rpc Obtener(ObtenerReq) returns (Pedido);
  rpc Listar(ListarReq) returns (stream Pedido);      // flujo de salida
  rpc Cargar(stream Linea) returns (Resumen);          // flujo de entrada
  rpc Chat(stream Msg) returns (stream Msg);            // bidireccional
}

message ObtenerReq { int32 id = 1; }
```

```bash
protoc --cpp_out=. --grpc_out=. --python_out=. --go_out=. pedidos.proto
```

**Un fichero, muchos lenguajes, cliente y servidor generados.**

Y **la genealogía merece contarse**, porque casi nadie la conoce:

| Año | Sistema | Qué aportó |
|---|---|---|
| **1984** | **ASN.1** | esquema formal + codificaciones binarias (BER, DER, PER) |
| **1988** | **Sun RPC / XDR** | IDL + generación de cliente y servidor (NFS lo usa) |
| **1991** | **CORBA IDL** | IDL independiente del lenguaje, con objetos remotos |
| **1996** | **DCOM** | lo mismo, en el mundo de Microsoft |
| **1998** | **SOAP / WSDL** | lo mismo, en XML y sobre HTTP |
| **2008** | **Protobuf** (interno desde 2001) | esquema compacto y **evolución bien pensada** |
| **2015** | **gRPC** | Protobuf + HTTP/2 + flujos |

**ASN.1 sigue en uso masivo hoy** —los certificados TLS, la telefonía móvil y el correo seguro están
codificados en ASN.1 DER— y es de hace cuarenta años.

Y merece preguntarse qué hizo Protobuf mejor que CORBA, porque la respuesta es la lección de esta clase:

**CORBA intentó hacer que un objeto remoto se pareciera a uno local** —con herencia, referencias, ciclo
de vida y transacciones distribuidas— **y esa abstracción se rompía**: la red falla, y un método remoto
que parece local esconde eso.

**Protobuf y gRPC hicieron lo contrario**: **mensajes explícitos, sin objetos remotos, sin estado
compartido, y con el fallo visible**.

Es la aplicación de una regla que atraviesa toda la Parte 10: **una frontera debe verse como frontera**.
Ocultarla hace el código más bonito y el sistema más frágil.

Y las herramientas de comprobación, que es la segunda práctica del cierre:

```bash
buf lint                  # comprueba estilo del .proto
buf breaking --against '.git#branch=main'    # ¿este cambio ROMPE el contrato?
```

**`buf breaking` compara dos versiones del esquema y falla si el cambio es incompatible** —quitar un
campo, reutilizar un identificador, cambiar un tipo—.

Es exactamente `abi-compliance-checker` de la clase 157, aplicado al contrato de datos en lugar de al
binario, y merece estar en la integración continua por la misma razón.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi CONTRATO;
  verbo   char(10) const;
  recurso char(30) const;
end-pi;

dsply ('contrato=' + %trim(verbo) + ' /' + %trim(recurso));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** IBM i tiene, en esta clase, el contrato mejor comprobado de toda la
página, y ya apareció dos veces: **la firma de un programa de servicio** (clases 143 y 157).

Y merece verlo aquí como lo que es —**un contrato de API con verificación automática**— y compararlo con
lo que hace la industria:

| Aspecto | Programa de servicio de IBM i | API REST típica |
|---|---|---|
| El contrato | **la lista ordenada de exportaciones** | OpenAPI, si alguien lo mantiene |
| Verificación | **el sistema, al activar el programa** | esperanza, o pruebas de contrato |
| Al romperse | **el programa no arranca, con mensaje claro** | error en producción |
| Evolución | **firmas múltiples**: la nueva y las anteriores | versionado en la URL, si acaso |
| Coste | cero: está en el objeto | herramientas y disciplina |

**La fila de la evolución merece subrayarse**, porque es la tercera práctica del cierre implementada:

```text
STRPGMEXP PGMLVL(*CURRENT) SIGNATURE('PEDIDOS V3')
  EXPORT SYMBOL('CREAR')
  EXPORT SYMBOL('CONSULTAR')
  EXPORT SYMBOL('ANULAR')        /* nuevo */
ENDPGMEXP
STRPGMEXP PGMLVL(*PRV) SIGNATURE('PEDIDOS V2')
  EXPORT SYMBOL('CREAR')
  EXPORT SYMBOL('CONSULTAR')
ENDPGMEXP
```

**El proveedor declara explícitamente qué versiones del contrato sigue soportando**, y el sistema
comprueba cuál usa cada cliente.

Es lo que en el mundo REST se intenta con `/v1/` y `/v2/` en la URL, con la diferencia de que **aquí la
comprobación es automática y el fallo es al arrancar, no en la primera petición rara**.

Y la capa moderna, que la clase 158 ya nombró:

```text
IWS lee el prototipo y publica el servicio con su OpenAPI.
El contrato REST se DERIVA del contrato RPG.
```

**Y ahí aparece la advertencia de esta clase**: derivar el contrato del código significa que **cualquier
cambio en el prototipo cambia la API publicada**.

La práctica correcta, y es la primera del cierre: **el prototipo que se expone es un artefacto propio**
—un procedimiento de fachada, escrito para eso— **distinto de los procedimientos internos que pueden
evolucionar libremente**.

Es la misma separación que la clase 158 pedía entre la capa literal y la idiomática, aplicada aquí a lo
que se publica y lo que se reserva.
"""),
        "pli": ("""
 contrato: procedure options(main);

    declare linea   char(60) varying;
    declare verbo   char(10) varying;
    declare recurso char(30) varying;
    declare p       fixed binary(31);

    get edit (linea) (a(60));
    linea = trim(linea);

    p = index(linea, ' ');
    verbo = substr(linea, 1, p - 1);
    recurso = trim(substr(linea, p + 1));

    put skip list ('contrato=' || verbo || ' /' || recurso);

 end contrato;
""", """
**Lo que esta clase enseña en PL/I.** PL/I vive en el sistema que inventó buena parte del vocabulario de
esta clase, y merece recogerlo porque explica de dónde salieron las ideas.

**El mainframe tiene contratos de interfaz muy formales, y varios tipos:**

| Contrato | Entre qué |
|---|---|
| **La COMMAREA / los contenedores** | programas de una transacción CICS (COBOL en esta página) |
| **El *program interface block*** | programa y gestor de base de datos IMS |
| **La lista de parámetros de LE** | módulos de lenguajes distintos (clase 157) |
| **El *copybook* / la declaración compartida** | cualquier par de programas |
| **La definición de MQ** | sistemas separados, por cola de mensajes |

**Y el último merece el detalle**, porque es la arquitectura de integración más influyente que salió de
este mundo: **IBM MQ, de 1993**.

```text
Un programa PONE un mensaje en una cola con un formato acordado.
Otro programa, quizá en otra máquina, otro sistema operativo y otro lenguaje,
lo SACA cuando puede.
```

Y las propiedades que eso da son las que hicieron carrera:

- **Desacoplamiento temporal**: el receptor no tiene que estar vivo cuando el emisor envía.
- **Entrega garantizada y transaccional**: el mensaje participa en la transacción.
- **Y el contrato es el formato del mensaje**, no una firma de función.

**Es la arquitectura orientada a mensajes**, y de ahí salió directamente todo el vocabulario de los
*Enterprise Integration Patterns* (clase 151) y, en buena medida, la arquitectura de eventos actual.

Y merece señalar la ventaja concreta que tiene sobre una llamada síncrona y que esta clase debe
recoger: **el contrato de una cola es más fácil de evolucionar**.

```text
Con una llamada:  si el receptor cambia, el emisor falla AHORA.
Con una cola:     los mensajes viejos y nuevos conviven en la cola,
                  y el receptor puede manejar las dos versiones a su ritmo.
```

Es la tercera práctica del cierre de esta clase —**no se puede desplegar todo a la vez**— convertida en
propiedad de la arquitectura en lugar de en disciplina de las personas.

Y es la razón por la que, treinta años después, la respuesta habitual a "¿cómo desacoplo estos dos
sistemas?" sigue siendo la misma: **poner una cola en medio**.
"""),
        "mumps": ("""
CONTRATO ; Contrato de API -- clase 160
 read linea
 new verbo, recurso
 set verbo = $piece(linea, " ", 1)
 set recurso = $piece(linea, " ", 2)
 write "contrato=", verbo, " /", recurso, !
 quit
""", """
**Lo que esta clase enseña en M.** El mundo sanitario tiene los contratos de interoperabilidad más
desarrollados de cualquier sector, y merece contarlos porque **es el mejor caso de estudio de esta clase
que existe**.

**HL7 v2 (1987): el contrato de posiciones.**

```text
MSH|^~\\&|LAB|HOSP|EMR|HOSP|20240315103000||ORU^R01|MSG001|P|2.5
PID|1||123456^^^HOSP^MR||GARCIA^ANA||19800101|F
OBX|1|NM|GLU^Glucosa^LN||95|mg/dL|70-110|N|||F
```

**Segmentos con nombre, campos separados por barras, posiciones fijas**, y un diccionario aparte que dice
qué es cada una.

Es exactamente el modelo de las globals de M (clase 159), y sus problemas son los mismos: **compacto,
universal y con el significado fuera del mensaje**.

Y hay algo más grave que merece decirse, porque es la lección: **HL7 v2 tiene tantos campos opcionales y
tanta variabilidad permitida que en la práctica cada hospital lo implementa distinto**.

**Un contrato que permite demasiado no es un contrato.** Y por eso la integración de dos sistemas
sanitarios sigue costando meses: **hay que negociar qué subconjunto usa cada uno**.

**FHIR (2014): el contrato con esquema.**

```json
{
  "resourceType": "Patient",
  "id": "123456",
  "identifier": [{"system": "http://hosp/mrn", "value": "123456"}],
  "name": [{"family": "García", "given": ["Ana"]}],
  "birthDate": "1980-01-01"
}
```

Y lo que FHIR hace distinto merece enumerarse, porque es el cierre de esta clase aplicado con rigor:

- **Recursos definidos formalmente**, con esquemas en JSON Schema, XML Schema y `StructureDefinition`.
- **Vocabularios controlados**: LOINC para pruebas, SNOMED para diagnósticos — **contrato semántico**,
  como las convenciones CF de Fortran en esta página.
- **Perfiles**: un país o una organización **restringe** el estándar para su uso, y **esa restricción es
  también un artefacto formal y validable**.
- **Y extensiones con URL**, para añadir lo propio **sin romper a quien no las conoce** — la tercera regla
  del cierre, con nombre.

**Los perfiles son la idea más valiosa y la más transferible**: reconocen que **un estándar global tiene
que permitir mucho**, y que **la interoperabilidad real ocurre cuando alguien publica formalmente qué
subconjunto usa**.

Es la respuesta al problema de HL7 v2, y es aplicable a cualquier API grande: **publicar no solo lo que se
puede enviar, sino lo que de verdad se envía**.
"""),
        "smalltalk": ("""
| linea partes |

linea := stdin nextLine trimBoth.
partes := linea substrings: ' '.

Transcript
    show: 'contrato=', (partes at: 1), ' /', (partes at: 2);
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk aporta a esta clase una perspectiva incómoda y útil:
**su noción de contrato es el protocolo, y el protocolo no está declarado en ninguna parte** (clase 149).

```smalltalk
"Un 'protocolo' es un conjunto de mensajes que un objeto entiende.
 No hay declaración: si responde, sirve."
```

**Eso es tipado por comportamiento**, y hace el código extraordinariamente flexible **y el contrato
implícito**.

Y la comunidad lo reconoció y construyó respuestas parciales que merecen conocerse:

**Las categorías de método** —los *protocols* del navegador— agrupan los mensajes por propósito
(`accessing`, `printing`, `private`), y **funcionan como documentación de qué forma parte de la interfaz
pública**.

```smalltalk
"Por convención, la categoría 'private' marca lo que NO es contrato"
```

**Los *traits* y los tipos explícitos** de algunos dialectos —Strongtalk, Pharo con `Typer`— intentaron
declararlo formalmente.

**Y las pruebas** —SUnit, inventado aquí (clase 139)— **son el contrato ejecutable**: en un lenguaje sin
declaraciones de tipo, **la prueba es lo que dice qué se espera de un objeto**.

Es la conclusión práctica que la comunidad dinámica alcanzó y merece extraerse: **cuando el lenguaje no
declara el contrato, las pruebas tienen que hacerlo** — y por eso la cultura de pruebas nació en los
lenguajes dinámicos y no en los tipados.

Y para las APIs de red, el ecosistema es moderno y competente:

| Herramienta | Notas |
|---|---|
| **Zinc HTTP** | cliente y servidor HTTP |
| **Teapot / Seaside REST** | rutas declarativas |
| **NeoJSON / STON** | serialización (clase 159) |
| **OpenAPI para Pharo** | generar cliente y documentación |

Y merece cerrar la clase, y con ella el bloque de contratos, con la observación que la página entera
sostiene:

**Todos los mecanismos de esta página** —la COMMAREA, la firma de programa de servicio, la especificación
de Ada, el GUID de COM, el `.proto`, el perfil FHIR, la prueba de SUnit— **hacen lo mismo: escribir en un
sitio lo que dos partes tienen que creer**.

Y todos fracasan por el mismo motivo cuando fracasan: **porque alguien cambió una de las partes sin mirar
el papel**. La tecnología solo decide **si eso se detecta antes o después de que llegue a producción** —
y esa es, al final, toda la diferencia que la ingeniería puede aportar aquí.
"""),
    },
)
