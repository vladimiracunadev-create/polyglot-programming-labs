# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 138

> [⬅️ Volver a la clase 138](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Un valor, su cuadrado y su cubo. El programa es una excusa para la pregunta de esta clase: **cuando
algo va mal, ¿qué puedes mirar?** Y aquí hay dos extremos que definen el espectro: **Smalltalk, donde
el error abre un depurador sobre el sistema vivo y puedes escribir el método que falta y continuar**,
y **COBOL en un lote nocturno, donde lo único que hay es un volcado de memoria y un listado de
compilación**.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **observabilidad de un programa en marcha**, y estos lenguajes lo enseñan porque
> tienen las herramientas más distintas de esta página. **El volcado y el listado**: COBOL y PL/I, donde
> la depuración es forense. **El registro del trabajo**: IBM i, donde cada mensaje queda con su pila.
> **El código como dato**: M con `$text` y `$stack` (clases 123 y 127). **Y el sistema vivo**: Smalltalk
> y Lisp, donde el depurador es parte del programa.
>
> Y el eje que las ordena no es la antigüedad: **es si el programa sigue vivo cuando lo miras**.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` → stdout: `valor=<n> cuadrado=<n²> cubo=<n³>`
- **Regla:** `inspeccionar n, n² y n³`

| stdin | esperado |
|---|---|
| `3` | `valor=3 cuadrado=9 cubo=27` |
| `2` | `valor=2 cuadrado=4 cubo=8` |
| `5` | `valor=5 cuadrado=25 cubo=125` |

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
PROGRAM-ID. DEPURA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC S9(9)  COMP-3.
01  CUAD    PIC S9(18) COMP-3.
01  CUBO    PIC S9(18) COMP-3.
01  ED-N    PIC -(8)9.
01  ED-C    PIC -(17)9.
01  ED-K    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    COMPUTE CUAD = N * N
    COMPUTE CUBO = N * N * N

    MOVE N    TO ED-N
    MOVE CUAD TO ED-C
    MOVE CUBO TO ED-K
    DISPLAY "valor=" FUNCTION TRIM(ED-N)
            " cuadrado=" FUNCTION TRIM(ED-C)
            " cubo=" FUNCTION TRIM(ED-K)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** La depuración en el mundo COBOL tiene dos modos muy distintos, y
merece conocer los dos.

**El interactivo**, con IBM Debug Tool o Micro Focus, que hace lo esperable: puntos de ruptura,
inspección de variables, ejecución paso a paso y **modificación de datos en marcha**.

**Y el forense**, que es el que define la cultura: **el volcado**.

```text
ABEND S0C7 → volcado de memoria + listado de compilación
```

Cuando un lote nocturno falla a las 3:40, **no hay nadie mirando y no se puede reproducir**. Lo que
queda es:

- **El volcado**: la memoria del programa en el instante del fallo.
- **El listado con `MAP` y `OFFSET`** (clase 137): **qué campo hay en cada desplazamiento**.
- **Y el desplazamiento del error**, que el sistema informa.

Con esas tres cosas se localiza **qué instrucción falló y qué contenía cada campo**, sin ejecutar
nada. Es arqueología, y funciona.

Y COBOL tiene ayudas del lenguaje que esta clase debe nombrar:

```cobol
DISPLAY "traza: " CAMPO UPON SYSOUT       *> el printf de siempre
DECLARATIVES ... USE FOR DEBUGGING ON ...  *> secciones de depuración
```

**`USE FOR DEBUGGING`** es una construcción del estándar que declara código que **solo se ejecuta si la
compilación tiene `WITH DEBUGGING MODE`**, y que puede dispararse **cada vez que cambia un dato o se
ejecuta un párrafo**.

```cobol
DEBUG-ITEM       *> variable especial: qué párrafo, qué línea, qué valor
```

Es un mecanismo de traza integrado en el lenguaje, de 1974, y hoy se considera obsoleto — pero la idea
—**instrumentación activable al compilar**— es la de cualquier marco de registro moderno.

Y hay una técnica del mainframe que conviene mencionar porque no tiene equivalente: **CEDF**, el
facilitador de depuración interactiva de CICS, que **intercepta cada comando `EXEC CICS` de una
transacción en producción y lo muestra**, permitiendo modificar los datos antes de continuar.

Es depuración de una transacción viva en un sistema en producción, con miles de usuarios conectados.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program depura
   implicit none
   integer :: n

   read(*, *) n

   write(*, '(A,I0,A,I0,A,I0)') 'valor=', n, ' cuadrado=', n * n, &
                                ' cubo=', n * n * n
end program depura
```

**Lo que esta clase enseña en Fortran.** La depuración en Fortran tiene una peculiaridad que la
distingue: **el problema no suele ser un fallo, es un número equivocado**.

Un programa numérico que produce resultados sutilmente incorrectos —por un índice mal puesto, por una
condición de contorno o por pérdida de precisión— **no falla**: da un resultado plausible y erróneo.

De ahí que las herramientas de Fortran se centren en las comprobaciones:

```bash
gfortran -g -fcheck=all -ffpe-trap=invalid,zero,overflow \
         -fbacktrace -Wall -Wextra prog.f90
```

- **`-fcheck=all`**: índices, punteros no asociados, conformidad de arreglos.
- **`-ffpe-trap`**: **convierte NaN, infinito y división por cero en una excepción**, en lugar de
  propagar un NaN silenciosamente por todo el cálculo.
- **`-fbacktrace`**: traza de la pila al abortar.
- **`-finit-real=snan`**: inicializar los reales con NaN señalizador, para **detectar el uso de
  variables sin inicializar**.

**`-ffpe-trap` es la más importante** y merece la explicación: en coma flotante, `0.0/0.0` da `NaN`, y
`NaN` se propaga por cualquier operación. Un cálculo de ocho horas puede terminar con todo a `NaN` y
**sin saber dónde empezó**. Con la trampa activada, **el programa se detiene en la operación culpable**.

Y para la depuración interactiva, Fortran usa **gdb** con soporte específico:

```text
(gdb) print v(3)@10        # imprimir 10 elementos desde v(3)
(gdb) print matriz
(gdb) info locals
```

Y para el paralelismo, hay herramientas especializadas que esta clase debe nombrar porque el problema
es real: **depurar 10.000 procesos MPI**.

```text
TotalView, Arm DDT   -- depuradores paralelos: agrupan procesos por comportamiento
Intel Inspector       -- carreras en OpenMP
Valgrind, MAP          -- perfilado
```

**Agrupar procesos por comportamiento** es la técnica clave: en lugar de mirar 10.000 pilas, la
herramienta muestra "9.997 procesos están aquí, 3 están allí" — y esos 3 son el problema.

Es una idea que la observabilidad moderna ha redescubierto con el agrupamiento de trazas.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Depura is
   N : Integer;
begin
   Get (N);

   Put ("valor=");      Put (N,         Width => 1);
   Put (" cuadrado=");  Put (N * N,     Width => 1);
   Put (" cubo=");      Put (N * N * N, Width => 1);
   New_Line;
end Depura;
```

**Lo que esta clase enseña en Ada.** La filosofía de Ada en esta clase es coherente con toda su página
en la Parte 8: **el mejor depurador es el que no hace falta**.

Con las comprobaciones activadas por defecto (clase 124), **un error de ejecución en Ada llega con
información**:

```text
raised CONSTRAINT_ERROR : prog.adb:15 index check failed
```

**Fichero, línea y qué comprobación falló**, sin depurador y sin símbolos. Compara con
`Segmentation fault` de C++ (clase 137).

Y GNAT añade la traza:

```bash
gnatmake -g -gnata -bargs -E prog.adb     # -E: guardar la traza en las excepciones
```

```ada
with GNAT.Traceback.Symbolic;
Put_Line (GNAT.Traceback.Symbolic.Symbolic_Traceback (E));
```

**Obtener la pila de una excepción desde el propio programa**, para registrarla.

Y Ada tiene tres mecanismos de depuración que son propios y que esta clase debe destacar:

**Primero, los contratos como aserciones activables** (clase 118):

```ada
pragma Assertion_Policy (Check);      --  o Ignore, en producción
function F (X : Integer) return Integer with Pre => X > 0;
```

**Las precondiciones se comprueban en desarrollo y se desactivan en producción**, con la misma
declaración. Y con SPARK, **lo que se demuestra ya no hace falta comprobarlo**.

**Segundo, `Ada.Exceptions` con información estructurada**:

```ada
exception
   when E : others =>
      Put_Line (Exception_Name (E));       --  qué excepción
      Put_Line (Exception_Message (E));      --  el mensaje
      Put_Line (Exception_Information (E));   --  todo, incluida la traza
```

**Y tercero, la depuración de tareas**: GDB con soporte de Ada muestra **las tareas, su estado, en qué
entrada están esperando y quién tiene cada objeto protegido**.

```text
(gdb) info tasks
   ID   TID       P-ID  Pri  State           Name
   1    ...       0     15   Runnable        main_task
   2    ...       1     15   Waiting on entry call  sensor
```

**Ver que una tarea está esperando en una entrada concreta** es la información que hace falta para
diagnosticar un interbloqueo, y en la mayoría de los lenguajes hay que deducirla de las pilas.

Es depuración con el vocabulario del modelo de concurrencia del lenguaje, no con el del sistema
operativo.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Depura;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N: Integer;

begin
  Read(N);

  WriteLn('valor=', IntToStr(N),
          ' cuadrado=', IntToStr(N * N),
          ' cubo=', IntToStr(N * N * N));
end.
```

**Lo que esta clase enseña en Pascal.** El mundo Pascal tiene una tradición de depuración muy marcada, y
viene de la clase 123: **Turbo Pascal integró el depurador en el editor en 1987**, cuando eso no
existía.

Poner un punto de ruptura con F5, ejecutar paso a paso con F7 e inspeccionar variables con Ctrl+F4
**en el mismo entorno donde se escribía el código** era revolucionario. Es el modelo de todos los IDE
modernos.

Hoy, Free Pascal usa **GDB** y Lazarus lo integra, y el ecosistema tiene tres herramientas que merecen
nombrarse:

**El registro de errores con pila**:

```pascal
uses SysUtils;
{$IFDEF DEBUG}
  SetHeapTraceOutput('fugas.txt');    { del unit heaptrc }
{$ENDIF}
```

**`heaptrc`** es la unidad de detección de fugas de Free Pascal (clase 130): con `-gh`, **al terminar el
programa informa de cada bloque no liberado con la pila de dónde se reservó**.

```bash
fpc -gh -gl prog.pas       # -gh: rastreo de montón; -gl: números de línea
```

**Y `-gl` es el complemento**: hace que las trazas incluyan fichero y línea, con lo que un error de
ejecución da:

```text
Runtime error 216 at $0000000000401234
  $0000000000401234  PROCESAR,  line 42 of prog.pas
```

Y en Delphi, la herramienta de referencia es **madExcept** o **EurekaLog**, que capturan cualquier
excepción no manejada y producen **un informe con la pila, las variables, la versión y una captura de
pantalla** — pensado para recibir informes de fallos de usuarios finales.

Es una capacidad que el ecosistema desarrolló porque su público es el software de escritorio
distribuido: **el fallo ocurre en la máquina del cliente**, y hay que diagnosticarlo sin acceso.

Es exactamente el problema que hoy resuelven Sentry y los sistemas de telemetría de fallos, y en el
mundo Delphi está resuelto desde hace veinte años.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((n (read)))
  (format t "valor=~D cuadrado=~D cubo=~D~%" n (* n n) (* n n n)))
```

**Lo que esta clase enseña en Common Lisp.** Lisp tiene, junto con Smalltalk, **la mejor experiencia de
depuración de esta página**, y por la misma razón: **el programa está vivo mientras lo miras**.

Cuando salta un error, se entra en el depurador **con la pila intacta y el sistema funcionando**:

```text
The value 3 is not of type STRING.
   [Condition of type TYPE-ERROR]

Restarts:
  0: [USE-VALUE] Specify a value to use instead.
  1: [RETRY] Retry SLIME REPL evaluation request.
  2: [ABORT] Return to SLIME's top level.

Backtrace:
  0: (MI-FUNCION 3)
  1: (OTRA-FUNCION)
```

Y **los reinicios** son lo que distingue a Lisp de todo lo demás (clases 103 y 116): **no solo se ve el
error, se ofrecen formas de continuar**.

`USE-VALUE` permite **dar el valor correcto y seguir desde ahí**, sin reiniciar el programa.

Y el arsenal del depurador:

```lisp
(trace mi-funcion)                 ; registrar cada llamada y su resultado
(untrace)
(break)                             ; punto de ruptura explícito
(inspect objeto)                     ; inspector interactivo
(describe objeto)
(step (mi-funcion 3))                 ; ejecución paso a paso
(sb-debug:print-backtrace)
(disassemble 'mi-funcion)              ; ver el código máquina (clase 123)
(time (mi-funcion 3))                   ; tiempo Y memoria reservada (clase 128)
```

**`trace` funciona sobre cualquier función, incluidas las del sistema**, sin recompilar y sin
instrumentar el código: envuelve la función en marcha.

Y con **SLIME** —el entorno de Emacs para Lisp— todo eso está integrado: **la pila navegable, el
inspector, la recompilación de una función y la reanudación**, todo sobre la imagen viva.

Y hay una capacidad que esta clase debe cerrar y que ilustra lo que significa "programa vivo": **se
puede depurar un servidor en producción conectándose por red**.

```lisp
(swank:create-server :port 4005)
```

**Abrir un servidor SLIME dentro de la aplicación en marcha** y conectarse desde el editor, para
inspeccionar, redefinir funciones y arreglar el problema **sin detener el servicio**.

Es una práctica real en despliegues de Common Lisp, y suena imprudente hasta que se compara con la
alternativa: reiniciar y perder el estado que provocó el fallo.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

puts "valor=$n cuadrado=[expr {$n * $n}] cubo=[expr {$n * $n * $n}]"
```

**Lo que esta clase enseña en Tcl.** Tcl tiene un mecanismo de depuración que ningún otro lenguaje de
esta página iguala en potencia y en simplicidad: **`trace`**.

```tcl
trace add variable x write { apply {{n1 n2 op} { puts "x cambió a $::x" }} }
trace add variable x read  { ... }
trace add variable x unset { ... }
trace add execution miProc enter { ... }
trace add execution miProc leave { ... }
trace add execution miProc enterstep { ... }     ;# ¡CADA COMANDO de dentro!
```

**`trace add execution ... enterstep` ejecuta código antes de CADA comando dentro de un
procedimiento**, sin modificar el código y sin recompilar.

Eso es un depurador paso a paso construido con un comando, y es lo que hace el depurador de Tcl.

Y `trace add variable ... write` responde a la pregunta más difícil de la depuración: **"¿quién cambió
esto?"**. En la mayoría de los entornos hace falta un punto de ruptura de datos del hardware; en Tcl es
una línea.

El resto del arsenal:

```tcl
info level 0                 ;# la llamada actual, con sus argumentos
info level -1                 ;# la del llamante
info frame                     ;# fichero y línea
catch { ... } r opts            ;# con -errorinfo: la pila completa (clase 137)
rename puts puts_orig            ;# INTERCEPTAR cualquier comando (clase 109)
```

**`rename` más un procedimiento envoltorio permite interceptar cualquier comando del sistema**, y es
como se instrumentan bibliotecas ajenas sin tocarlas.

Y el ecosistema tiene:

```bash
tclsh -encoding utf-8 ...
package require TclDebugger      # el depurador de ActiveState
nagelfar prog.tcl                 # análisis estático (clase 137)
```

Y en Tcl 8.7, la depuración de corrutinas (clase 134):

```tcl
coroprobe $nombre { info level }    ;# mirar DENTRO de una corrutina suspendida
```

**Inspeccionar una corrutina suspendida** es un problema abierto en la mayoría de los entornos
asíncronos —¿dónde está la pila de una tarea que no se está ejecutando?— y Tcl lo resolvió con un
comando.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

printf "valor=%d cuadrado=%d cubo=%d\n", $n, $n * $n, $n * $n * $n;
```

**Lo que esta clase enseña en Perl.** Perl trae **un depurador completo en el intérprete**, sin instalar
nada:

```bash
perl -d programa.pl
```

```text
  DB<1> n              # siguiente línea
  DB<2> s               # entrar en la función
  DB<3> c 42             # continuar hasta la línea 42
  DB<4> x $estructura     # volcar una estructura de datos, RECURSIVAMENTE
  DB<5> T                  # la pila
  DB<6> b 15 $x > 100       # punto de ruptura CONDICIONAL
  DB<7> w $variable          # vigilar una variable
```

**`x` es el comando estrella**: vuelca una estructura anidada con indentación y tipos, y es lo que
hace utilizable la depuración de estructuras complejas de Perl (clase 097).

Y `perl -d` tiene una propiedad poco conocida: **el depurador está escrito en Perl** —`perl5db.pl`— y
se puede sustituir:

```bash
PERL5DB='BEGIN { require "mi_depurador.pl" }' perl -d prog.pl
perl -d:Trace prog.pl          # módulos Devel::*
perl -d:NYTProf prog.pl         # el PERFILADOR de referencia
```

**`Devel::NYTProf`** merece la mención: es uno de los mejores perfiladores de cualquier lenguaje de
guion, con informes HTML línea a línea y desglose por llamada.

Y el arsenal de diagnóstico de Perl es de los más ricos de esta página:

```perl
use Data::Dumper;   print Dumper($estructura);      # volcar
use Devel::Peek;     Dump($x);                       # la estructura INTERNA (clase 128)
use Carp;            confess "error";                 # morir CON la pila
use Devel::Cycle;    find_cycle($x);                   # ciclos (clase 131)
$SIG{__DIE__} = sub { ... };                            # gancho global (clase 119)
```

**`Carp::confess`** es `die` con la pila completa, y `cluck` es `warn` con pila. Son la forma
idiomática de que un error de una biblioteca diga desde dónde se la llamó (clase 127).

Y `Data::Dumper` tiene una propiedad que encaja con esta parte del curso: **su salida es código Perl
válido**, así que una estructura volcada **se puede volver a leer con `eval`**.

Es la misma idea que `print`/`read` en Lisp (clase 104) y `storeString` en Smalltalk: **el volcado de
depuración y el formato de serialización son el mismo**.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "valor=" << n
              << " cuadrado=" << n * n
              << " cubo=" << n * n * n << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ tiene **las herramientas de depuración más potentes y las
menos integradas** de esta página, y esa combinación define su cultura.

```bash
g++ -g -O0 prog.cpp        # -g: símbolos de depuración; -O0: sin optimizar
gdb ./prog
lldb ./prog
```

Y la primera lección es la del compromiso: **`-g` con `-O2` produce información de depuración
engañosa**. El compilador reordena, elimina variables y funde funciones, así que **el depurador muestra
valores optimizados o "value optimized out"**.

De ahí la práctica universal: **compilar dos veces**, una para depurar y otra para producción — con el
riesgo conocido de que **el fallo solo aparezca con optimización**, que suele significar comportamiento
indefinido (clase 137).

El arsenal de C++ es enorme, y merece organizarlo por lo que responde:

| Pregunta | Herramienta |
|---|---|
| ¿Qué estado hay ahora? | **gdb**, **lldb**, puntos de ruptura condicionales |
| ¿Quién tocó esta memoria? | **watchpoints** de hardware: `watch *ptr` |
| ¿Hay fugas o accesos inválidos? | **AddressSanitizer**, **Valgrind** |
| ¿Hay carreras? | **ThreadSanitizer** (clase 136) |
| ¿Hay comportamiento indefinido? | **UBSan** |
| ¿Dónde se va el tiempo? | **perf**, **VTune**, **Callgrind** |
| ¿Y en producción? | **eBPF**, volcados de núcleo, `std::stacktrace` (C++23) |

**Los `watchpoints` de hardware** merecen destacarse: `watch *0x7fff1234` hace que el procesador
detenga el programa **cuando algo escriba en esa dirección**, y responde a la pregunta "¿quién está
corrompiendo esto?" — que es la más difícil de C++.

Es lo mismo que `trace add variable ... write` en Tcl de esta página, con el hardware haciendo el
trabajo en lugar del intérprete.

Y **rr** merece la mención final porque cambia el tipo de pregunta que se puede hacer:

```bash
rr record ./prog       # graba la ejecución
rr replay              # y la reproduce, con GDB, hacia ATRÁS
(gdb) reverse-continue  # ejecutar hacia atrás hasta el punto de ruptura
```

**Depuración reversible**: reproducir exactamente la misma ejecución —incluidas las condiciones de
carrera— y **retroceder desde el fallo hasta la causa**.

Es la respuesta más directa al cierre de esta clase: **cuando puedes reproducir el fallo
determinísticamente, el problema está medio resuelto**.

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

dcl-pi DEPURA;
  n int(10) const;
end-pi;

dcl-s cuad int(20);
dcl-s cubo int(20);

cuad = n * n;
cubo = n * n * n;

dsply ('valor=' + %char(n) + ' cuadrado=' + %char(cuad) + ' cubo=' + %char(cubo));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** IBM i tiene, en depuración, la propiedad que más lo distingue de
todas las plataformas de esta página: **todo queda registrado sin configurar nada**.

**El registro del trabajo** (clase 137):

```text
DSPJOBLOG JOB(123456/USUARIO/MIAPP)
```

Cada mensaje lleva **el código, el texto, la ayuda de segundo nivel, el programa, el número de
sentencia y la pila de llamadas en ese momento**. Sin instrumentar el código y sin activar nada.

**El depurador del sistema**:

```text
STRDBG PGM(MIBIB/MIAPP) UPDPROD(*YES)
```

Y con `DBGVIEW(*SOURCE)` al compilar, **el depurador muestra el fuente**, aunque el objeto esté en otra
máquina — porque **la vista de depuración se guarda dentro del objeto programa**.

Eso resuelve un problema clásico: **no hace falta tener el fuente para depurar**. Está en el objeto.

**El depurador de servicio**, que es la capacidad que sorprende:

```text
STRSRVJOB JOB(123456/USUARIO/OTROTRABAJO)
STRDBG PGM(...)
```

**Depurar un trabajo AJENO que ya está en ejecución**, incluido uno de un usuario conectado o un
trabajo por lotes en marcha, desde otra sesión.

Y por SQL, la forma moderna (clase 117):

```sql
SELECT * FROM TABLE(QSYS2.STACK_INFO('*'))          -- pilas de TODOS los trabajos
SELECT * FROM TABLE(QSYS2.JOBLOG_INFO('123456/USUARIO/MIAPP'))
SELECT * FROM QSYS2.ACTIVE_JOB_INFO(...)
```

**Consultar la pila de llamadas y el registro de cualquier trabajo del sistema con `WHERE` y
`ORDER BY`.**

Es observabilidad por defecto, y es una diferencia cultural profunda: **en IBM i la pregunta "¿qué
estaba haciendo el programa?" tiene respuesta siempre**, mientras que en un servidor moderno depende
de si alguien puso el registro adecuado antes de que pasara.

Es exactamente lo que el cierre de esta clase señala: **lo que hay que mejorar cuando un fallo no se
diagnostica no es la técnica, es lo que el sistema registra** — y aquí lo registra la plataforma.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 depura: procedure options(main);

    declare n fixed binary(31);

    get list (n);

    put skip list ('valor=' || trim(char(n)) ||
                   ' cuadrado=' || trim(char(n * n)) ||
                   ' cubo=' || trim(char(n * n * n)));

 end depura;
```

**Lo que esta clase enseña en PL/I.** PL/I comparte con COBOL la cultura forense del volcado (clase
138, apartado COBOL) y tiene dos capacidades de diagnóstico propias que merecen conocerse.

**La primera es `put data`**, ya nombrada en la clase 106:

```pli
 put data;                    /* vuelca TODAS las variables del ámbito */
 put data (x, y, estructura);  /* o las indicadas */
```

**`put data` sin argumentos imprime cada variable con su nombre y su valor**, con formato
`NOMBRE=VALOR`. Es un volcado de depuración integrado en el lenguaje, y su salida **se puede volver a
leer con `get data`**.

Es la misma propiedad que `Data::Dumper` en Perl y `print`/`read` en Lisp de esta página: **el volcado
de depuración y el formato de intercambio son el mismo**.

**Y la segunda es el manejo de condiciones como instrumentación** (clases 103 y 137):

```pli
 on error snap begin;
    put data;                 /* volcar el estado */
    put skip list ('en ' || onloc());     /* dónde ocurrió */
 end;
```

**`snap`** es la palabra clave que lo hace especial: **hace que el sistema imprima la traza de la pila**
antes de ejecutar el manejador.

Y las funciones de contexto de las condiciones dan información estructurada:

```pli
 onloc()      /* el nombre del procedimiento donde ocurrió */
 oncode()     /* el código numérico de la condición */
 onchar()     /* el carácter que causó un error de conversión */
 onsource()   /* la CADENA que lo causó, y se puede MODIFICAR (clase 116) */
 onfile()     /* el fichero implicado */
```

**`onsource` es la que no tiene equivalente**: da el dato que causó el error de conversión **y permite
cambiarlo y reanudar** — lo que en la clase 116 se comparaba con los reinicios de Lisp.

Y el listado de compilación de PL/I (clase 137), con `XREF`, `MAP`, `ATTRIBUTES` y `LIST`, completa el
cuadro: **un documento que dice dónde está cada variable, quién la usa y qué código se generó**.

Es depuración sin depurador, diseñada para una época en que la máquina estaba en otro edificio.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
DEPURA ; Depuracion -- clase 138
 read n
 write "valor=", n, " cuadrado=", n * n, " cubo=", n * n * n, !
 quit
```

**Lo que esta clase enseña en M.** M tiene una propiedad que lo hace singular en esta clase y que viene
de las clases 123 y 127: **el código fuente es un dato accesible en ejecución**.

```mumps
 write $text(+3^MIRUT)                 ; la línea 3 del fuente
 write $stack($stack, "MCODE")          ; el CÓDIGO de la línea actual de la pila
 write $stack(-1)                        ; cuántos niveles hay
 write $stack(2, "PLACE")                 ; dónde está el nivel 2
 write $zstatus                            ; el error completo (extensión)
```

**`$stack(nivel, "MCODE")` devuelve el texto del código de ese nivel de la pila.** Es una traza que
muestra **el código, no solo los nombres de función**, y sin depurador ni símbolos.

Y el manejo de errores con `$etrap` (clase 137) permite construir un registro completo:

```mumps
 set $etrap = "do ^ERRLOG"
 ...
errlog ;
 new i
 for i=$stack(-1):-1:1 write $stack(i,"PLACE")," ",$stack(i,"MCODE"),!
 quit
```

**Ese bucle imprime la pila entera con el código de cada línea**, y es un patrón real en los sistemas
VistA.

Y M tiene además el depurador interactivo del entorno:

```mumps
 zbreak procesar^RUTINA           ; punto de ruptura (extensión $Z)
 zstep into
 zshow "V"                          ; mostrar todas las variables
 zwrite                              ; volcar el espacio de variables
```

**`zwrite` sin argumentos vuelca todas las variables locales con sus subíndices**, y es el `put data`
de PL/I de esta página.

Y hay una capacidad que se deriva del modelo de M y que esta clase debe cerrar: **el estado se puede
inspeccionar desde otro proceso**.

```mumps
 write ^PACIENTE(123)              ; desde CUALQUIER proceso, en cualquier momento
```

**Como los datos están en *globals*, un proceso puede examinar lo que otro está haciendo**, sin
depurador y sin detenerlo — siempre que el programa haya escrito su estado ahí.

Es lo mismo que la observabilidad de IBM i de esta página, conseguido por la vía del modelo de datos:
**si el estado importante vive en la base de datos, siempre se puede mirar**.

Y es la conclusión práctica del cierre de esta clase: **lo que se registra es lo que se puede
diagnosticar**, y en M el registro es el modelo de datos.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n |

n := stdin nextLine trimBoth asNumber.

Transcript
    show: 'valor=', n printString;
    show: ' cuadrado=', (n * n) printString;
    show: ' cubo=', (n * n * n) printString;
    cr.
```

**Lo que esta clase enseña en Smalltalk.** Aquí está el extremo del espectro que abre esta clase, y
cierra la Parte 8 entera: **en Smalltalk, el depurador no es una herramienta externa — es parte del
sistema, escrito en Smalltalk, y opera sobre el programa vivo**.

Cuando salta un error:

1. **Se abre el depurador sobre el proceso**, que sigue suspendido y con todo su estado.
2. **La pila es navegable**, y cada marco muestra sus variables, su receptor y su código (clase 127).
3. **Se puede inspeccionar y modificar cualquier objeto** de cualquier marco.
4. **Se puede editar el método ahí mismo**, aceptarlo y **pulsar "reintentar"**.
5. **Y el programa continúa** desde ese punto, con el método nuevo.

**El paso 4 es el que no tiene equivalente en ninguna otra fila de esta página.**

Y el arsenal está todo en el lenguaje:

```smalltalk
self halt.                          "punto de ruptura en el código"
self inspect.                        "abrir el inspector sobre este objeto"
thisContext.                          "el marco actual (clase 127)"
objeto browse.                         "abrir el navegador en su clase"
objeto chasePointers.                   "quién lo retiene (clase 131)"
MessageTally spyOn: [ ... ].             "PERFILADOR: dónde se va el tiempo"
Object subclass: ... instanceVariableNames: ...    "crear una clase, en marcha"
```

**`MessageTally spyOn:`** es el perfilador, escrito en Smalltalk, que muestrea la pila del proceso y
produce un árbol de llamadas con porcentajes.

Y hay dos capacidades que resumen la diferencia de modelo:

**El navegador de mensajes** (clase 098):

```smalltalk
SystemNavigation default allCallsOn: #imprimir
SystemNavigation default browseAllImplementorsOf: #imprimir
```

**"¿Quién llama a esto?" y "¿quién lo implementa?" se responden recorriendo la imagen**, en un segundo
y sin herramientas externas.

**Y la depuración remota sobre la imagen en producción**, igual que el `swank` de Lisp de esta página:
conectarse a un sistema en marcha, inspeccionar, corregir y continuar.

Y con eso cierra la Parte 8, con la observación que la recorre entera: **Smalltalk tomó en cada una de
las dieciséis clases la decisión que maximiza la observabilidad** —bytecode con JIT, todo en el montón,
sin punteros, la pila como objeto, recolector, compilador en el sistema— **y el resultado es un entorno
donde casi cualquier pregunta sobre el programa tiene respuesta inmediata**.

El precio está en la otra columna: menos control, menos predecibilidad y menos rendimiento en el peor
caso. **Es el mismo compromiso de siempre, tomado con coherencia absoluta durante cuarenta y seis
años.**

---

## Y de vuelta a la clase

Lo transferible: **depurar es reducir el espacio de estados posibles, y las herramientas solo ayudan a
mirar**. Un depurador da el estado actual; un registro, la historia; un volcado, la foto final; y una
prueba que reproduce el fallo, el control. La más valiosa es la última, y por eso la depuración
empieza casi siempre por **conseguir reproducirlo**. Cuando un fallo no se reproduce, lo que hay que
mejorar no es la técnica de depuración: es lo que el programa registra.

⏮️ [Volver a la clase 138](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
