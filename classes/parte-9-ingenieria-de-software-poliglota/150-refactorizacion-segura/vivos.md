# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 150

> [⬅️ Volver a la clase 150](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Duplicar un número y afirmar que el resultado es equivalente. Es el contrato de toda refactorización:
**cambiar cómo, sin cambiar qué**. Y esta página tiene el origen de la disciplina: **el Refactoring
Browser, escrito en Smalltalk por John Brant y Don Roberts a mediados de los noventa, fue la primera
herramienta de refactorización automática de la historia**, y los ejemplos del libro de Martin Fowler
que popularizó el término salieron de ese entorno.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es el **cambio de estructura sin cambio de comportamiento**, y estos lenguajes lo
> enseñan porque **tienen el código más viejo del mundo y no pueden reescribirlo**. Un sistema COBOL de
> 1985 en producción no se tira: se transforma poco a poco, con red. Y la red es lo que esta página
> compara: **el compilador** (Ada, C++), **las pruebas de caracterización** (COBOL, PL/I), **el
> verificador de equivalencia** (clase 140), **y las herramientas que refactorizan sobre el árbol
> sintáctico en lugar de sobre el texto**.
>
> Y aparece el límite que nadie puede saltarse: **lo que se puede refactorizar con seguridad depende de lo
> que se pueda analizar**.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` → stdout: `equivalente=<true|false> resultado=<2n>`
- **Regla:** `viejo = n*2 ; nuevo = n+n ; equivalente si coinciden`

| stdin | esperado |
|---|---|
| `5` | `equivalente=true resultado=10` |
| `0` | `equivalente=true resultado=0` |
| `7` | `equivalente=true resultado=14` |

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
PROGRAM-ID. REFACT.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(40).
01  N       PIC S9(9) COMP.
01  R       PIC S9(9) COMP.
01  ED      PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    PERFORM DOBLAR

    MOVE R TO ED
    DISPLAY "equivalente=true resultado=" FUNCTION TRIM(ED)
    STOP RUN.

DOBLAR.
    COMPUTE R = N * 2.
```

**Lo que esta clase enseña en COBOL.** El programa extrae el cálculo a un párrafo y lo invoca con
`PERFORM` — que es **la refactorización más básica y más útil de COBOL: extraer párrafo** (clase 084).

Y COBOL es el lenguaje donde esta clase tiene más consecuencias económicas del mundo, porque **hay
cientos de miles de millones de líneas en producción y casi ninguna se puede reescribir**.

Y el método que funciona lo formalizó Michael Feathers en *Working Effectively with Legacy Code* (2004),
con una definición que merece citarse porque es incómoda y exacta:

> **Código heredado es código sin pruebas.**

Y su técnica central es la que esta página necesita: **las pruebas de caracterización**.

```text
1. Se ejecuta el programa actual con entradas reales y se GUARDA la salida.
2. Esa salida se declara "lo esperado" —aunque contenga errores conocidos—.
3. Se refactoriza.
4. Si la salida cambia, el cambio rompió algo.
```

**El paso 2 es el que cuesta aceptar**: no se prueba que el programa sea correcto, **se prueba que sigue
haciendo exactamente lo mismo**, errores incluidos.

Y es lo correcto, porque **los errores de un sistema de treinta años forman parte de su
comportamiento**: hay procesos aguas abajo que dependen de ellos (clase 140).

Y COBOL tiene una técnica propia para el problema más difícil de esta clase —**cómo se prueba un
programa que solo funciona con CICS y DB2**— que Feathers llamó *seam* y aquí es literal:

```cobol
      *> Antes: la lógica está pegada a la infraestructura
       EXEC SQL SELECT SALDO INTO :WS-SALDO ... END-EXEC
       COMPUTE WS-NUEVO = WS-SALDO * WS-TASA
       EXEC CICS SEND MAP('PANTALLA') END-EXEC

      *> Después: la lógica es un programa llamable y PROBABLE
       CALL 'CALCINT' USING WS-SALDO WS-TASA WS-NUEVO
```

**Extraer el cálculo a un programa que solo recibe y devuelve datos** es la operación que hace probable
el 90 % de la lógica de negocio, y es la tarea número uno de cualquier modernización (clase 149).

Y las herramientas del mundo COBOL para esto son sustanciales y merecen nombrarse:

| Herramienta | Qué hace |
|---|---|
| **Micro Focus Enterprise Analyzer** | grafo de llamadas y de datos de todo el sistema |
| **CAST Imaging** | análisis de impacto entre lenguajes y tecnologías |
| **IBM ADDI** | análisis de aplicaciones y descubrimiento de reglas de negocio |
| **cobol-check** | pruebas unitarias insertadas en una copia del programa (clase 139) |

**El análisis de impacto es lo que hace viable el paso pequeño del cierre de esta clase**: antes de
tocar un campo, saber **exactamente qué programas lo usan** — que en un sistema de treinta millones de
líneas no es una pregunta que se pueda responder leyendo.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program refact
   implicit none
   integer :: n

   read(*, *) n

   write(*, '(A,I0)') 'equivalente=true resultado=', doblar(n)

contains

   pure integer function doblar(x)
      integer, intent(in) :: x
      doblar = 2 * x
   end function doblar

end program refact
```

**Lo que esta clase enseña en Fortran.** El programa usa `contains` con una función **`pure`**, y esa
palabra es la refactorización de esta página: **`pure` declara que la función no tiene efectos
secundarios**, y el compilador lo comprueba.

Es documentación verificada, y además **permite al compilador optimizar y paralelizar**.

Y Fortran tiene el problema de esta clase en su forma más pesada, porque el código heredado científico
tiene características muy concretas:

```fortran
      COMMON /ESTADO/ X(1000), Y(1000), NPTS, ITER
      EQUIVALENCE (BUF(1), X(1))
      GOTO (10, 20, 30), MODO
      ENTRY ALTERNATIVA
```

**`COMMON` es estado global compartido por nombre y por posición** (clase 088): dos rutinas pueden
declarar el mismo bloque con distintos nombres y tipos, **y funciona**. Es imposible saber quién toca
qué sin leerlo todo.

**`EQUIVALENCE` hace que dos nombres sean la misma memoria.** **`GOTO` calculado** salta según un índice.
Y **`ENTRY`** da varios puntos de entrada al mismo procedimiento.

Y la refactorización canónica de Fortran es la que resuelve todo eso a la vez, y merece describirse en
orden porque el orden importa:

**Paso 1 — capturar el comportamiento**: guardar entradas y salidas de casos reales (clase 140), con
tolerancia numérica justificada.

**Paso 2 — `implicit none`**, fichero a fichero. Rompe la compilación de todo lo que dependía de tipos
implícitos, y **cada rotura es un error latente encontrado** (clase 137).

**Paso 3 — `COMMON` a `module`**:

```fortran
module estado
   implicit none
   integer, parameter :: dp = kind(1.0d0)
   real(dp), allocatable :: x(:), y(:)
   integer :: npts, iter
end module
```

**Con eso, el compilador comprueba los tipos** y `use estado, only: x, npts` **documenta qué usa cada
rutina**.

**Paso 4 — interfaces explícitas**: mover los procedimientos sueltos a módulos activa la comprobación de
argumentos (clase 109), que es donde aparecen los fallos silenciosos de décadas.

**Y paso 5 — `intent` en todo argumento**, que documenta la dirección y la hace comprobar.

Y las herramientas:

```bash
findent -ofree                 # formato fijo a libre (clase 145)
fprettify                       # formateo
plusFORT / SPAG                  # reestructuración automática: quita GOTO, analiza COMMON
```

**plusFORT merece la mención** porque hace algo raro: **reestructura el flujo de control
automáticamente**, convirtiendo marañas de `GOTO` en bucles y condicionales — con demostración de
equivalencia.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Refact is

   function Doblar (X : Integer) return Integer is (2 * X);

   N : Integer;
begin
   Get (N);

   Put ("equivalente=true resultado=");
   Put (Doblar (N), Width => 1);
   New_Line;
end Refact;
```

**Lo que esta clase enseña en Ada.** `function Doblar (X : Integer) return Integer is (2 * X);` es una
**función de expresión** de Ada 2012: el cuerpo es una única expresión, sin `begin` ni `end`.

Y es relevante para esta clase por un motivo concreto: **una función de expresión es visible para el
demostrador**, así que `gnatprove` puede razonar sobre ella en las llamadas — cosa que con un cuerpo
normal no siempre puede.

Y Ada tiene la mejor red de esta página para refactorizar, y merece enumerarla porque el conjunto es
inusual:

**Primera, el sistema de tipos como red.** Renombrar un tipo, cambiar un rango, mover un campo: **el
compilador señala todos los sitios afectados**. En un lenguaje sin tipos fuertes, eso es una búsqueda de
texto con esperanza.

**Segunda, la comprobación de coherencia entre unidades** (clase 143): si se cambia una especificación y
algo no se recompila, **el enlace falla**. No hay forma de acabar con la mitad del sistema usando la
interfaz vieja.

**Tercera, los contratos como afirmación de equivalencia** (clase 140):

```ada
function Nueva_Version (X : Integer) return Integer
   with Post => Nueva_Version'Result = Vieja_Version (X);
```

**Se declara literalmente que la nueva debe dar lo mismo que la vieja**, y se comprueba en cada llamada
durante el periodo de transición.

**Y cuarta, la demostración formal**: `gnatprove` puede demostrar que la versión refactorizada **no
introduce errores de ejecución**, y en algunos casos que es equivalente.

Y las herramientas de refactorización asistida:

| Herramienta | Qué hace |
|---|---|
| **GNAT Studio** | renombrar, extraer subprograma, extraer variable, **sobre el árbol sintáctico** |
| **`gnatstub`** | generar el esqueleto del cuerpo desde la especificación |
| **`gnattest`** | regenerar las pruebas al cambiar la interfaz (clase 139) |
| **libadalang** | biblioteca de análisis: **escribir refactorizaciones propias** |

**libadalang merece el detalle**, porque es la respuesta al límite que el "por qué" de esta clase
enunciaba: **da acceso al árbol sintáctico y a la información semántica de un proyecto Ada completo**,
desde Python o Ada.

```python
for nodo in unidad.root.findall(lal.CallExpr):
    if nodo.f_name.p_referenced_decl() == decl_obsoleta:
        ...   # reescritura SEGURA: se sabe a qué se refiere cada nombre
```

**"Se sabe a qué se refiere cada nombre" es toda la diferencia** entre una refactorización y un
`sed -i`.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Refact;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N: Integer;

function Doblar(X: Integer): Integer;
begin
  Result := 2 * X;
end;

begin
  Read(N);
  WriteLn('equivalente=true resultado=', IntToStr(Doblar(N)));
end.
```

**Lo que esta clase enseña en Pascal.** El ecosistema Delphi tiene un caso de refactorización a gran
escala que merece contarse, porque es el más doloroso de esta página y enseña una lección general: **la
migración a Unicode de Delphi 2009**.

**Hasta Delphi 2007, `string` era `AnsiString`: un byte por carácter.** A partir de Delphi 2009,
**`string` pasó a ser `UnicodeString`: UTF-16** (clase 093).

Y eso rompió, de golpe, todo el código que suponía "un carácter, un byte":

```pascal
Length(S)                  { ahora cuenta unidades de código de 16 bits }
SizeOf(Char)                { pasó de 1 a 2 }
BlockRead(F, S[1], N)        { lee bytes en una cadena de caracteres anchos: BASURA }
PChar(S)                      { ahora es PWideChar }
Move(Origen, Destino, Longitud)  { ¿longitud en bytes o en caracteres? }
```

**El código que trataba cadenas como memoria dejó de funcionar**, y a menudo **sin error de
compilación** — que es el peor caso posible.

Y la forma en que la comunidad lo resolvió es exactamente la del cierre de esta clase:

**Paso 1 — hacer explícito lo implícito.** Antes de migrar, sustituir `string` por `AnsiString` **donde
de verdad se querían bytes** y por `string` donde se querían caracteres. Eso se hace **en la versión
vieja**, donde nada cambia de comportamiento, y **es refactorización pura**.

**Paso 2 — introducir `RawByteString` y `TBytes`** para los datos binarios, que es lo que había estado
viajando en cadenas por comodidad.

**Paso 3 — migrar**, con el compilador señalando lo que queda.

Y la lección general merece destacarse porque se aplica a cualquier migración grande: **la
refactorización se hace ANTES del cambio, en el sistema que todavía funciona**.

Preparar el código para el cambio y hacer el cambio son dos operaciones distintas, y hacerlas a la vez
es lo que convierte una migración en un desastre — que es la tercera regla del cierre de esta clase.

Y las herramientas del ecosistema:

| Herramienta | Qué hace |
|---|---|
| **Refactorizaciones del IDE** | renombrar, extraer método, declarar variable, cambiar firma |
| **Pascal Analyzer** | variables sin usar, ámbitos, dependencias, complejidad |
| **ModelMaker Code Explorer** | refactorización avanzada y navegación |
| **DUnitX + Delphi-Mocks** | la red de pruebas (clase 139) |

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(defun doblar (x) (* 2 x))

(let ((n (read)))
  (format t "equivalente=true resultado=~D~%" (doblar n)))
```

**Lo que esta clase enseña en Common Lisp.** Lisp tiene, para esta clase, una ventaja estructural que
merece explicarse: **el programa ya es un árbol sintáctico** (clase 123), así que **una refactorización
es una transformación de listas**.

```lisp
;; Un refactorizador en Lisp es un programa que recorre código como datos
(defun sustituir-llamada (forma vieja nueva)
  (cond ((atom forma) forma)
        ((eq (car forma) vieja) (cons nueva (cdr forma)))
        (t (mapcar (lambda (f) (sustituir-llamada f vieja nueva)) forma))))
```

**No hace falta un analizador**, porque no hay texto que analizar. Es la misma propiedad que hace
posibles las macros (clase 123), aplicada a las herramientas.

Y Lisp tiene una capacidad de refactorización que ningún lenguaje compilado de esta página iguala, y
viene de la Parte 8: **se puede refactorizar con el sistema en marcha y comprobar cada paso al
instante**.

```lisp
(defun calcular (x) ...)      ; C-c C-c: recompila y ya está activa
(calcular 42)                  ; comprobar inmediatamente
```

**El ciclo de un paso de refactorización dura segundos**, que es lo que hace practicable la segunda regla
del cierre: **pasos pequeños comprobados uno a uno**.

Y las herramientas del ecosistema:

| Herramienta | Qué hace |
|---|---|
| **SLIME** | `M-.` ir a la definición, `M-?` quién la llama, recompilar función |
| **`who-calls` / `who-references`** | el grafo de llamadas, desde la imagen viva |
| **`trace`** | comprobar que el comportamiento no cambió (clase 141) |
| **`lisp-critic`** | sugerencias de idiomas más limpios (clase 146) |
| **Paredit / Lispy** | **edición estructural**: mover y envolver expresiones, no texto |

**Paredit merece la mención final**, porque es refactorización a nivel de tecleo: **las operaciones son
"envolver esta expresión", "sacar esta expresión del padre", "partir este nodo"** — nunca "insertar un
paréntesis".

El resultado es que **el código nunca queda con los paréntesis desequilibrados**, ni siquiera a mitad de
una edición.

Es lo mismo que las refactorizaciones de un IDE hacen para lenguajes con sintaxis, y en Lisp llega hasta
el movimiento del cursor.

Y merece cerrar con el límite honesto, que es el del "por qué" de esta clase: **la potencia de Lisp
también dificulta el análisis**. `eval`, `funcall` con símbolos construidos, `intern` de nombres
calculados y las macros que generan definiciones **hacen que "quién llama a esto" no siempre tenga
respuesta exacta**.

Es el mismo compromiso de siempre, aquí en la caja de herramientas: **lo que es dinámico es difícil de
analizar, y lo que es difícil de analizar es difícil de refactorizar con garantías**.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

proc doblar {x} { return [expr {2 * $x}] }

puts "equivalente=true resultado=[doblar $n]"
```

**Lo que esta clase enseña en Tcl.** Tcl está en el extremo difícil de esta clase, y merece decirlo con
claridad porque es una consecuencia directa de su diseño: **en Tcl, casi nada se puede analizar
estáticamente** (clase 123).

```tcl
set comando "procesar"
$comando $datos                  ;# ¿quién llama a "procesar"? imposible saberlo
eval $codigoConstruido
uplevel 1 $fragmento
namespace eval $nombreVariable { ... }
```

**Una búsqueda de "procesar" no encuentra esa llamada**, y ninguna herramienta puede garantizar que ha
encontrado todas.

Y de ahí que la red en Tcl sea **necesariamente dinámica**:

**Primera, las pruebas** (clase 139) con `tcltest`, que en Tcl son más importantes que en ningún otro
lenguaje de esta página por lo que se acaba de decir.

**Segunda, `trace` para verificar la equivalencia** (clase 141):

```tcl
# antes de refactorizar: grabar todas las llamadas y sus resultados
trace add execution procesar leave {apply {{cmd code res op} {
    puts $::grabacion "[lrange $cmd 1 end] -> $res"
}}}
```

**Grabar el comportamiento real en producción y usarlo como pruebas de caracterización** es la aplicación
directa de la técnica de COBOL de esta página, y en Tcl se monta en cinco líneas sin tocar el código.

**Y tercera, `nagelfar`**, que es lo más parecido a un análisis estático que Tcl tiene: comprueba
aridades, nombres de comando y citación (clase 137).

Y Tcl aporta a esta clase una refactorización propia que merece conocerse, porque es un mecanismo de
sustitución que otros lenguajes no tienen:

```tcl
# Sustituir gradualmente una implementación por otra, midiendo la equivalencia
rename ::procesar ::procesar_viejo
proc ::procesar {args} {
    set viejo [::procesar_viejo {*}$args]
    set nuevo [::procesar_nuevo {*}$args]
    if {$viejo ne $nuevo} { puts stderr "DIFIERE: $args" }
    return $viejo          ;# de momento, se sirve el viejo
}
```

**Las dos implementaciones se ejecutan, se comparan, y se sirve la vieja mientras dure la
verificación.**

Eso es el patrón que Martin Fowler llamó *Branch by Abstraction* con verificación —y GitHub popularizó
como *Scientist*— **implementado en Tcl con un `rename` y una `proc`**, sin bibliotecas y sin modificar
a los llamadores.

Es la mejor demostración de esta página de que **la refactorización segura depende más de tener un punto
donde interceptar que de las herramientas**.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

sub doblar { my ($x) = @_; return 2 * $x }

my $n = <STDIN>;
chomp $n;

print "equivalente=true resultado=", doblar($n), "\n";
```

**Lo que esta clase enseña en Perl.** Perl comparte el límite de Tcl en esta página —**el análisis
estático es difícil**— y por una razón célebre: **solo Perl puede analizar Perl**.

La frase es de Larry Wall y es literalmente cierta: **la gramática de Perl depende del código que ya se
ha compilado**, porque los prototipos de subrutina y los `use` pueden cambiar cómo se analiza lo que
viene después.

```perl
sub mifuncion($$);      # el prototipo cambia el análisis de las llamadas
use Try::Tiny;           # y esto añade sintaxis nueva
```

Y de ahí que exista una herramienta muy interesante que merece explicarse: **PPI**.

**PPI —*Parse Perl Isolated*— analiza Perl sin ejecutarlo**, aceptando que el resultado es
**aproximado**. Es la base de `Perl::Critic` (clase 146) y de las herramientas de refactorización del
ecosistema.

```perl
my $doc = PPI::Document->new('modulo.pm');
for my $sub ($doc->find('PPI::Statement::Sub')->@*) {
    print $sub->name, "\n";
}
```

**Y el compromiso que representa es la lección de esta página**: PPI da un árbol sintáctico útil para el
99 % del código real, **y no puede garantizar nada** para el 1 % que hace magia.

Y las herramientas del ecosistema:

| Herramienta | Qué hace |
|---|---|
| **PPI** | árbol sintáctico aproximado, sin ejecutar |
| **Perl::Critic** | reglas de estilo y patrones peligrosos |
| **Devel::Cover** | cobertura: **qué cubre la red antes de tocar nada** |
| **App::perlimports** | limpiar y explicitar las importaciones |
| **Test::Deep / Test::Differences** | comparar salidas antes y después (clase 140) |

**`Devel::Cover` merece el primer puesto en esta clase**, y es una recomendación general: **antes de
refactorizar, medir qué cubren las pruebas**.

```bash
cover -test -report html
```

**Refactorizar una zona con el 20 % de cobertura es trabajar sin red**, por muchas pruebas que tenga el
resto del proyecto. Y la respuesta correcta no es refactorizar con cuidado: **es escribir pruebas de
caracterización de esa zona primero**.

Es la primera regla del cierre de esta clase, y la que más se salta por prisa.

Y Perl aporta una técnica que su dinamismo permite y que resuelve el mismo problema que el `rename` de
Tcl en esta página:

```perl
use Test::MockModule;
my $mod = Test::MockModule->new('Pedido');
$mod->redefine('calcular', sub { ... });     # sustituir para probar
```

**Sustituir cualquier función de cualquier módulo durante una prueba**, sin que el código lo haya
previsto — que es lo que permite poner una red alrededor de código heredado que no fue diseñado para
probarse.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

constexpr long long doblar(long long x) { return 2 * x; }

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "equivalente=true resultado=" << doblar(n) << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** `constexpr` declara que la función **se puede evaluar en tiempo de
compilación** (clase 122), y aquí es también una refactorización: convertir una función normal en
`constexpr` **no cambia el comportamiento** y permite que el compilador la evalúe cuando los argumentos
son constantes.

Y C++ tiene, en herramientas de refactorización, una de las mejores infraestructuras que existen, y
merece explicar por qué: **Clang expone su propio análisis**.

```bash
clang-tidy --fix --checks='modernize-*' *.cpp    # reescribe el código
clang-rename -offset=1234 -new-name=calcularTotal archivo.cpp
clangd                                             # el servidor de lenguaje del editor
```

**Y la diferencia con una búsqueda y sustitución merece subrayarse**: `clang-rename` **sabe a qué se
refiere cada nombre**, así que renombrar un método `procesar` **no toca los `procesar` de otras clases,
ni los de los comentarios, ni los de las cadenas** — y sí toca las llamadas que llegan por una
referencia a la clase base.

Es la diferencia entre una operación semántica y una textual, y es lo que hace que la refactorización sea
segura.

Y las refactorizaciones que `modernize-*` aplica automáticamente son sustanciales:

```cpp
// antes                              // después
NULL                                → nullptr
typedef int Entero;                  → using Entero = int;
for (auto it = v.begin(); ...)        → for (const auto& x : v)
new Foo()                              → std::make_unique<Foo>()
virtual void f() { }                    → void f() override { }
```

**Aplicar eso a un millón de líneas es un comando**, y es la respuesta a la objeción de que un estándar
nuevo no se puede aplicar a código existente (clase 146).

Y C++ aporta a esta clase su propia red, que es distinta de la de los demás:

| Red | Qué caza |
|---|---|
| **El compilador con `-Wall -Wextra -Werror`** | tipos, conversiones, sombras de nombres |
| **Los desinfectantes** | comportamiento indefinido introducido al refactorizar |
| **`abi-compliance-checker`** | **si la refactorización rompió el ABI** (clase 143) |
| **Pruebas + cobertura (`gcov`, `llvm-cov`)** | la red clásica |
| **`csmith` / comparación de binarios** | equivalencia a nivel de compilador (clase 140) |

**La tercera fila es específica de C++ y fácil de olvidar**: mover un miembro de sitio, añadir un campo
privado o cambiar el orden de las funciones virtuales **cambia el ABI**, así que **una refactorización
"interna" puede romper a todos los que usan la biblioteca ya compilados**.

Es la razón de existir del patrón `pimpl` (clase 149), y un buen ejemplo de que **en C++ hay
refactorizaciones que no son transparentes aunque no cambien el comportamiento del código**.

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

dcl-pi REFACT;
  n int(10) const;
end-pi;

dcl-proc doblar;
  dcl-pi *n int(20);
    x int(10) const;
  end-pi;
  return 2 * x;
end-proc;

dsply ('equivalente=true resultado=' + %char(doblar(n)));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** RPG ha vivido **la refactorización a mayor escala de esta página**,
y es la que la clase 146 describía: **la conversión de formato fijo a formato totalmente libre**.

```text
     C                   EVAL      TOTAL = PRECIO * CANTIDAD
```

```rpgle
total = precio * cantidad;
```

Y lo interesante para esta clase es que **existen herramientas que lo hacen automáticamente y de forma
verificable**:

| Herramienta | Qué hace |
|---|---|
| **ARCAD Transformer RPG** | conversión de fijo a libre, con equivalencia comprobada |
| **CVTRPGSRC / RDi** | conversión asistida, con revisión |
| **Linoma / Fresche** | modernización de fuentes y de interfaces |

**Y el método es el del cierre de esta clase**: se convierte, **se compila, y se compara el objeto
resultante** — porque **si la conversión es realmente equivalente, el código generado debe ser el
mismo**.

Es un verificador de equivalencia a nivel de compilador (clase 140), y es una red mucho más fuerte que
un conjunto de pruebas.

Y la segunda gran refactorización de esta plataforma, que ya apareció en la clase 149, merece verse como
una secuencia porque es un ejemplo modélico de pasos pequeños:

```text
1. Extraer el cálculo a una SUBRUTINA dentro del mismo programa    (sin riesgo)
2. Convertir la subrutina en un PROCEDIMIENTO con parámetros        (elimina globales)
3. Mover el procedimiento a un módulo aparte                          (compila igual)
4. Enlazar el módulo en un PROGRAMA DE SERVICIO                        (ahora es reutilizable)
5. Escribir pruebas unitarias con RPGUnit                               (¡ya hay red!)
6. Y ahora sí: cambiar la implementación                                 (con red)
```

**Los pasos 1 a 4 no cambian el comportamiento y cada uno se puede desplegar por separado.** El paso 5
es el que crea la red, y solo entonces empieza el cambio real.

Es la secuencia del cierre de esta clase aplicada literalmente, y es la razón por la que la
modernización de IBM i tiene una tasa de éxito notablemente mejor que las reescrituras completas.

Y merece cerrar con el dato que lo justifica: **las reescrituras completas de sistemas heredados fracasan
con mucha más frecuencia de lo que la industria admite**, y el motivo es siempre el mismo — **el
comportamiento real del sistema viejo no está documentado en ninguna parte más que en su propio código**,
y en los treinta años de casos particulares que ha ido acumulando.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 refact: procedure options(main);

    declare n fixed binary(31);

    doblar: procedure (x) returns (fixed binary(31));
       declare x fixed binary(31);
       return (2 * x);
    end doblar;

    get list (n);

    put skip list ('equivalente=true resultado=' || trim(char(doblar(n))));

 end refact;
```

**Lo que esta clase enseña en PL/I.** El programa declara `doblar` como **procedimiento anidado** (clase
149), que es la unidad de extracción natural del lenguaje.

Y PL/I aporta a esta clase la perspectiva del sistema que **no se puede refactorizar del todo**, y merece
tratarla con seriedad porque es la situación real de mucho software crítico.

Los factores que lo hacen difícil son concretos:

**Primero, no queda quien lo escribió.** Un sistema de 1975 tiene autores jubilados, y **la
documentación es el código**.

**Segundo, el lenguaje permite construcciones que impiden el análisis:**

```pli
 declare p pointer;
 declare estructura based(p);           /* la forma depende de lo que apunte */
 declare texto char(100) defined(otro);  /* dos nombres, una memoria */
 goto etiqueta_variable;                  /* salto a una etiqueta CALCULADA */
```

**`goto` a una variable de etiqueta** es especialmente duro: **el destino se decide en ejecución**, así
que el grafo de flujo no se puede construir.

**Y tercero, las reglas de conversión implícita** (clase 140): cualquier cambio de tipo puede alterar
resultados de formas sutiles.

Y la estrategia que la industria aplica en estos casos merece conocerse, porque es distinta de
refactorizar y es legítima: **encapsular en lugar de transformar**.

```text
1. NO se toca el sistema viejo.
2. Se le pone una fachada: un servicio que lo llama y expone una interfaz moderna.
3. Todo lo NUEVO se escribe fuera, contra esa interfaz.
4. Y las funciones se van sacando de una en una, cuando hay razón para tocarlas.
```

**Eso es el patrón del *estrangulador***, que Martin Fowler nombró y que es la técnica de referencia para
sistemas que no se pueden reescribir: **el sistema nuevo crece alrededor del viejo hasta que el viejo se
puede apagar**, en un plazo de años.

Y su propiedad más valiosa es la del cierre de esta clase: **cada paso es pequeño y reversible**, y **el
sistema funciona en todo momento**.

Frente a la alternativa —**la reescritura completa**, que exige dos años sin entregar nada y termina
compitiendo contra un original que mientras tanto ha seguido cambiando— la diferencia en tasa de éxito
está bien documentada, y es grande.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
REFACT ; Refactorizacion segura -- clase 150
 read n
 write "equivalente=true resultado=", $$doblar(n), !
 quit
 ;
doblar(x) ; devuelve el doble
 quit x * 2
```

**Lo que esta clase enseña en M.** El programa extrae el cálculo a una **función extrínseca** —`$$doblar`,
con el doble símbolo de dólar— que es la unidad de extracción de M y la refactorización básica del
lenguaje.

Y M está en el extremo más difícil de esta página, y conviene ser explícito sobre por qué: **la
indirección hace imposible el análisis estático completo** (clase 123).

```mumps
 do @rutina             ; el nombre de la rutina es una VARIABLE
 set @nombre = valor     ; el nombre de la variable es una variable
 xecute codigo            ; código construido en marcha
 do @("EN^" _ paquete)     ; llamada compuesta con concatenación
```

**"¿Quién llama a esta rutina?" no tiene respuesta fiable**, y en VistA —donde la indirección se usa de
verdad— eso es una limitación real.

Y las redes que sí funcionan en este mundo:

**Primera, las sumas de comprobación de rutina** (clase 144): **detectan cualquier modificación**, lo
que permite saber exactamente qué cambió.

**Segunda, las pruebas de caracterización sobre globals** (clase 140): **ejecutar antes y después y
comparar el estado de la base de datos**, que en M captura todos los efectos porque **todo el estado
importante está ahí**.

```mumps
 ; grabar el estado antes, ejecutar, comparar después
 do copiar^UTIL("^PACIENTE", "^ANTES")
 do procesar^MIRUT(caso)
 write $$comparar^UTIL("^PACIENTE", "^ESPERADO")
```

**Y esa es una red más fuerte que la de la mayoría de los lenguajes de esta página**, porque **compara el
efecto completo, no solo el valor devuelto**.

Es la misma idea que el diario de IBM i de la clase 140, y viene del mismo sitio: **cuando el estado vive
en la base de datos, la equivalencia se comprueba sobre el estado**.

**Y tercera, el prefijo de paquete como frontera** (clase 146): las convenciones de nombres de VistA
hacen que **el ámbito de un cambio sea identificable** aunque el análisis automático falle.

Y merece cerrar con la refactorización más valiosa que se puede hacer en M, y que es aplicable a
cualquier lenguaje con estado global: **añadir `new`**.

```mumps
procesar(caso) ;
 new i, j, temporal, resultado      ; ← esta línea
 ...
```

**Declarar como locales las variables que la rutina usa** convierte una rutina que puede corromper el
estado de quien la llama en una que no puede — **sin cambiar lo que hace**.

Es la definición exacta de una refactorización, cuesta una línea, y es la primera que el estándar de
VistA exige (clase 146) precisamente porque es la que más fallos elimina por unidad de esfuerzo.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n |

n := stdin nextLine trimBoth asNumber.

Transcript
    show: 'equivalente=true resultado=', (n * 2) printString;
    cr.
```

**Lo que esta clase enseña en Smalltalk.** Aquí está el origen del gancho, y merece contarse completo
porque es la historia de esta disciplina: **el Refactoring Browser fue la primera herramienta de
refactorización automática**.

**John Brant y Don Roberts lo escribieron en la Universidad de Illinois a mediados de los noventa**,
dirigidos por Ralph Johnson —uno de los cuatro autores del libro de patrones de diseño—. Y ofrecía, ya
entonces:

```text
Renombrar clase, método, variable, argumento
Extraer método   /  Insertar método (inline)
Extraer variable temporal  /  Insertar
Mover método a otra clase
Subir método a la superclase  /  Bajarlo a las subclases
Añadir y quitar parámetros
Convertir variable temporal en instancia
Abstraer variable de instancia (crear accesores y usarlos)
```

**Esa lista es, prácticamente, el menú "Refactor" de cualquier IDE actual**, y es de hace treinta años.

Y **`Refactoring` de Martin Fowler (1999)**, el libro que dio nombre a la disciplina, **usa Java en los
ejemplos pero nació de este entorno**: Ralph Johnson y Don Roberts firman capítulos, y las técnicas se
habían practicado y automatizado en Smalltalk antes.

Y merece explicar **por qué la herramienta apareció aquí y no en otro sitio**, porque la respuesta es la
de la Parte 8:

**Primero, el código es un objeto.** No hay que analizar texto: **el sistema ya tiene el árbol
sintáctico de cada método**, accesible como objetos.

**Segundo, `allCallsOn:` responde de verdad** (clase 138): se puede recorrer todo el sistema preguntando
qué método envía qué mensaje.

**Y tercero, el ciclo es instantáneo**: recompilar un método son milisegundos, y las pruebas —con SUnit,
inventado en el mismo entorno (clase 139)— se ejecutan en el acto.

**Las tres condiciones que la segunda regla del cierre de esta clase necesita —pasos pequeños,
comprobados, rápidos— estaban dadas.**

Y el límite honesto también hay que decirlo, y es el mismo que en Lisp y Tcl en esta página: **el
dinamismo**.

```smalltalk
objeto perform: (nombre , 'Total') asSymbol.     "el selector se construye"
```

**Un mensaje enviado con `perform:` y un selector calculado es invisible para el analizador.** El
Refactoring Browser **avisa** cuando detecta `perform:` cerca de lo que se está renombrando, pero no
puede garantizarlo.

Y esa advertencia es la conclusión más útil de esta página entera: **ninguna herramienta de
refactorización es completamente segura en un lenguaje dinámico**, y el que las inventó lo sabía y lo
decía. La red final siguen siendo las pruebas.

---

## Y de vuelta a la clase

Lo transferible: **refactorizar sin red no es refactorizar, es reescribir con esperanza**. La secuencia
que funciona es siempre la misma: **primero conseguir una red** —pruebas de caracterización que capturen
el comportamiento actual, aunque sea el equivocado—; **después cambiar en pasos pequeños y reversibles**,
comprobando después de cada uno; **y no mezclar nunca la refactorización con un cambio de
comportamiento**, porque si algo se rompe hay que saber cuál de las dos cosas fue. Y la regla que evita
la mayoría de los desastres: **si no se puede volver atrás en cinco minutos, el paso era demasiado
grande**.

⏮️ [Volver a la clase 150](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
