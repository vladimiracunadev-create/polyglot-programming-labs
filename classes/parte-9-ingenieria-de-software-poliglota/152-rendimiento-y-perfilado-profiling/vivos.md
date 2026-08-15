# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 152

> [⬅️ Volver a la clase 152](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Contar las operaciones y devolver la suma: `operaciones=5 resultado=15`. Es un programa que **se mide a
sí mismo**, que es la forma más antigua y más honesta de perfilar. Y esta clase existe por una razón
que las herramientas no arreglan: **la intuición sobre el rendimiento es sistemáticamente equivocada**.
Aquí está el caso que mejor lo demuestra: **la reescritura de LINPACK a LAPACK multiplicó por diez el
rendimiento sin cambiar un solo algoritmo** — solo el orden en que se tocaba la memoria.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **medición antes que la optimización**, y estos lenguajes lo enseñan porque
> **cubren todo el rango de lo que significa "rápido"**. Fortran y C++ pelean por ciclos y por caché.
> COBOL y RPG pelean por operaciones de entrada y salida, que es donde está su tiempo. Ada pelea por el
> **peor caso**, no por el promedio. Y Lisp y Smalltalk tienen perfiladores escritos en el propio lenguaje
> que muestrean el sistema vivo.
>
> Y aparece la distinción que ordena la clase: **latencia, rendimiento total y peor caso son tres cosas
> distintas**, y optimizar una puede empeorar las otras.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: un entero `n` (n >= 1) → stdout: `operaciones=<n> resultado=<1+...+n>`
- **Regla:** `sumar 1..n contando cada suma`

| stdin | esperado |
|---|---|
| `5` | `operaciones=5 resultado=15` |
| `1` | `operaciones=1 resultado=1` |
| `3` | `operaciones=3 resultado=6` |

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
PROGRAM-ID. PERFIL.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(40).
01  N       PIC S9(9) COMP.
01  I       PIC S9(9) COMP.
01  TOTAL   PIC S9(18) COMP VALUE 0.
01  ED-N    PIC -(8)9.
01  ED-T    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        ADD I TO TOTAL
    END-PERFORM

    MOVE N     TO ED-N
    MOVE TOTAL TO ED-T
    DISPLAY "operaciones=" FUNCTION TRIM(ED-N)
            " resultado=" FUNCTION TRIM(ED-T)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** En el mundo del lote, **el rendimiento casi nunca es cuestión de
CPU: es cuestión de entrada y salida**, y esa diferencia de enfoque merece explicarse porque sigue
siendo válida.

Un programa que procesa diez millones de registros **pasa la mayor parte del tiempo esperando al
disco**. Optimizar el cálculo no cambia nada; optimizar los accesos lo cambia todo.

Y las técnicas del mundo mainframe son de una eficacia que sorprende:

**El tamaño de bloque.** Un fichero secuencial se lee por bloques, no por registros:

```jcl
//SALIDA DD DSN=MI.FICHERO,BLKSIZE=27998,LRECL=200
```

**Con `BLKSIZE=0`, el sistema calcula el tamaño de bloque óptimo para el dispositivo** — y pasar de un
bloque pequeño a uno óptimo puede **dividir por veinte el número de operaciones físicas**.

Es la misma idea que el búfer de la clase 104, decidida a nivel de fichero.

**El orden de acceso.** Y aquí está la técnica que define el diseño de estos sistemas:

```text
❌  Leer un fichero de 10 millones de registros y, por cada uno, consultar una tabla indexada.
✓  ORDENAR el fichero por la misma clave que la tabla y leer las dos en paralelo, una vez.
```

**Eso es el *match-merge*, y convierte 10 millones de accesos aleatorios en dos recorridos
secuenciales.** La diferencia en un disco es de dos órdenes de magnitud.

Y por eso **`SORT` es el programa más ejecutado del mainframe** y por eso los productos de ordenación
—DFSORT, Syncsort— son piezas de software muy afinadas.

Es el mismo razonamiento que hoy justifica ordenar antes de unir en un sistema de datos masivos, y es de
los años sesenta.

Y la medición, que en esta plataforma es automática (clase 142):

```text
Los registros SMF dan, por paso y por transacción:
  - CPU en milisegundos
  - operaciones de E/S CONTADAS, por fichero
  - tiempo de espera
  - memoria usada
```

**Con `EXCP count` por fichero se ve exactamente qué fichero está costando el tiempo**, sin instrumentar
nada. Y **Strobe** o **APA** dan el perfil por línea de código.

Es observabilidad de rendimiento por defecto, y es la razón de que la pregunta "¿por qué tarda este
lote?" tenga respuesta en minutos.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program perfil
   implicit none
   integer :: n, i
   integer(kind=8) :: total

   read(*, *) n
   total = 0

   do i = 1, n
      total = total + i
   end do

   write(*, '(A,I0,A,I0)') 'operaciones=', n, ' resultado=', total
end program perfil
```

**Lo que esta clase enseña en Fortran.** Aquí está el caso del gancho, y merece desarrollarse porque es
la mejor lección de rendimiento que existe: **LINPACK a LAPACK**.

**LINPACK (1979)** expresaba sus algoritmos en operaciones **vector-vector** —BLAS nivel 1—. **LAPACK
(1992)** los reformuló en operaciones **matriz-matriz** —BLAS nivel 3— (clase 149).

**El mismo algoritmo matemático. Diez veces más rápido.**

Y la razón es la de la clase 128: **la jerarquía de memoria**.

```text
Producto escalar (nivel 1):  2n operaciones,  2n datos leídos  →  1 operación por dato
Matriz por vector (nivel 2): 2n² operaciones, n² datos          →  2 operaciones por dato
Matriz por matriz (nivel 3): 2n³ operaciones, 3n² datos          →  ~n operaciones por dato
```

**Solo el nivel 3 hace suficiente trabajo por dato leído como para que la caché compense**. Los otros
dos están limitados por el ancho de banda de memoria: **el procesador está esperando**.

Y la consecuencia práctica que hay que llevarse, y vale para cualquier lenguaje: **en cálculo numérico,
el cuello de botella no es la aritmética — es traer los datos**.

Y de ahí las optimizaciones características de Fortran, todas sobre la memoria:

```fortran
! El orden de los bucles importa: Fortran guarda por COLUMNAS (clase 089)
do j = 1, n
   do i = 1, n
      a(i, j) = ...      ! ✓ i variando rápido: memoria contigua
   end do
end do
! Al revés, cada acceso salta n posiciones: fallo de caché en cada uno
```

**Cambiar el orden de dos bucles puede multiplicar por diez el tiempo**, y es la optimización que más
veces se pasa por alto — porque el código se lee igual de bien de las dos formas.

Y las herramientas del ecosistema:

```bash
gprof ./prog                       # perfil clásico, por función
perf record ./prog; perf report     # muestreo, sin instrumentar
perf stat -e cache-misses ./prog     # ¡CONTADORES DEL PROCESADOR!
valgrind --tool=cachegrind ./prog     # simulación de caché
likwid-perfctr -g MEM ./prog           # ancho de banda de memoria
Intel VTune / Arm MAP                   # perfiladores completos, con MPI
```

**`perf stat -e cache-misses` merece destacarse** porque mide lo que esta explicación dice que importa:
no cuánto tiempo pasa en cada función, sino **cuántas veces el procesador tuvo que esperar a la
memoria**.

Es la métrica que hace visible el problema que LAPACK resolvió, y la que convierte "va lento" en "va
lento por esto".

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Perfil is
   N     : Integer;
   Total : Long_Long_Integer := 0;
begin
   Get (N);

   for I in 1 .. N loop
      Total := Total + Long_Long_Integer (I);
   end loop;

   Put_Line
     ("operaciones=" & Ada.Strings.Fixed.Trim (N'Image, Ada.Strings.Both) &
      " resultado="  & Ada.Strings.Fixed.Trim (Total'Image, Ada.Strings.Both));
end Perfil;
```

**Lo que esta clase enseña en Ada.** Ada plantea esta clase desde un ángulo distinto al de todos los
demás de esta página, y merece explicarlo porque cambia qué se mide: **en tiempo real, lo que importa no
es el promedio — es el peor caso**.

```text
Un algoritmo que tarda 1 ms de media y 50 ms en el peor caso
es PEOR que uno que tarda 5 ms SIEMPRE,
si el plazo del sistema es de 10 ms.
```

Y de ahí un concepto que esta clase debe nombrar y que en otros dominios casi no existe: **el WCET, el
*tiempo de ejecución del peor caso***.

Calcularlo es un problema difícil, y las técnicas merecen conocerse:

| Método | Cómo |
|---|---|
| **Análisis estático** | recorrer todos los caminos del código y sumar los costes de las instrucciones |
| **Medición** | ejecutar con las entradas más desfavorables conocidas, muchas veces |
| **Híbrido** | medir bloques básicos y componer el peor camino |

Y las herramientas del sector —**aiT**, **RapiTime**, **Bound-T**— hacen análisis estático **teniendo en
cuenta la caché y la predicción de saltos del procesador concreto**.

Y aquí aparece una tensión que merece señalarse, porque es contraintuitiva: **las cachés y la ejecución
especulativa mejoran el promedio y empeoran la predecibilidad**.

Por eso **en sistemas críticos a veces se desactivan las cachés**, o se usan procesadores sin
especulación: **se renuncia a velocidad para poder garantizar el plazo**.

Es la aplicación más extrema del cierre de esta clase: **"rápido" no significa nada hasta que se dice
respecto a qué**.

Y las características del lenguaje que sostienen esto son las de la Parte 8 y la clase 146:

```ada
pragma Restrictions (No_Allocators);        --  sin montón: sin pausas imprevisibles
pragma Restrictions (No_Recursion);          --  pila acotada y calculable
pragma Profile (Ravenscar);                   --  planificación analizable
```

**Sin reserva dinámica y sin recursión, el peor caso se puede calcular** — que es justamente por qué
esas restricciones existen.

Y Ada tiene medición en el lenguaje:

```ada
with Ada.Real_Time; use Ada.Real_Time;
T0 : constant Time := Clock;
...
D : constant Time_Span := Clock - T0;
```

**`Ada.Real_Time.Clock` es un reloj monótono con resolución garantizada**, distinto de
`Ada.Calendar.Clock` —la hora del día, que puede saltar—. **Confundirlos es un error clásico de
medición**, y Ada los separa en el sistema de tipos.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Perfil;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N, I: Integer;
  Total: Int64;

begin
  Read(N);
  Total := 0;

  for I := 1 to N do
    Total := Total + I;

  WriteLn('operaciones=', IntToStr(N), ' resultado=', IntToStr(Total));
end.
```

**Lo que esta clase enseña en Pascal.** Free Pascal y Delphi producen código nativo y rápido, y el
ecosistema tiene una tradición de medición que viene de una época en la que el rendimiento se notaba:
**Turbo Pascal competía con el ensamblador**.

Las herramientas:

```bash
fpc -O3 -Xs -CX prog.pas          # -O3: optimización; -CX: enlace inteligente
fpc -pg prog.pas && gprof ./prog   # perfil clásico
valgrind --tool=callgrind ./prog    # grafo de llamadas con costes
```

| Herramienta | Notas |
|---|---|
| **`gprof`** | por función; requiere `-pg` |
| **Sampling Profiler** (Delphi) | muestreo sin instrumentar |
| **AQtime / Nexus Quality Suite** | perfiladores comerciales del mundo Delphi |
| **`EpikTimer`** | medición de alta resolución, portable |
| **`heaptrc`** | reservas y fugas (clase 138) |

Y el ecosistema Pascal aporta a esta clase una lección muy concreta que merece destacarse, porque es la
optimización que más veces resuelve un problema real en este tipo de aplicaciones: **la concatenación de
cadenas en un bucle**.

```pascal
{ ✗ O(n²): cada concatenación copia toda la cadena }
for I := 1 to 100000 do
  S := S + Linea[I];

{ ✓ O(n): un constructor con capacidad que crece }
SB := TStringBuilder.Create;
for I := 1 to 100000 do
  SB.Append(Linea[I]);
S := SB.ToString;
```

**La primera versión con 100.000 elementos tarda minutos; la segunda, milisegundos.**

Y el motivo conecta con la clase 093: **una cadena es un bloque contiguo**, así que concatenar significa
**reservar un bloque nuevo y copiar todo lo anterior** — y hacerlo n veces es cuadrático.

Es el mismo problema en Java, C#, Python y todos los lenguajes con cadenas inmutables, y es
probablemente **el error de rendimiento más común de la programación de aplicaciones**.

Y merece extraer el principio general, porque se aplica a mucho más que a cadenas: **cuidado con las
operaciones que parecen O(1) y son O(n) sobre una estructura que crece**. Concatenar cadenas, insertar
al principio de un arreglo, buscar en una lista: cada una es barata una vez y cuadrática en un bucle.

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((n (read))
      (total 0))
  (dotimes (i n)
    (incf total (1+ i)))
  (format t "operaciones=~D resultado=~D~%" n total))
```

**Lo que esta clase enseña en Common Lisp.** Lisp tiene, por lo que la clase 124 explicó, una herramienta
de medición que ningún lenguaje compilado de esta página iguala en comodidad: **`time` mide una
expresión cualquiera, en marcha, sin recompilar**.

```lisp
(time (procesar-todo datos))
```

```text
Evaluation took:
  2.340 seconds of real time
  2.310000 seconds of total run time (2.180000 user, 0.130000 system)
  [ Run times consist of 0.410 seconds GC time, and 1.900 seconds non-GC time. ]
  98.72% CPU
  6,382,142,268 processor cycles
  1,048,585,712 bytes consed          ← ¡MEMORIA RESERVADA!
```

**Las dos líneas destacadas son las que Lisp da y casi nadie más**: **cuánto tiempo se fue en el
recolector de basura** y **cuántos bytes se reservaron**.

Y eso es decisivo, porque en un lenguaje con recolección **el problema de rendimiento casi nunca es el
cálculo: es la basura que se genera** (clase 131).

**Un `1.048.585.712 bytes consed` en un bucle que "no reserva nada" es el diagnóstico completo.**

Y el perfilador estadístico:

```lisp
(require :sb-sprof)
(sb-sprof:with-profiling (:report :flat :mode :cpu)
  (procesar-todo datos))
```

```text
Self  Total  Cumul   Function
25.3   45.1   25.3   SB-KERNEL:%COERCE-CALLABLE-TO-FUN
18.2   18.2   43.5   MI-PAQUETE::CALCULAR
```

**`:mode :alloc`** cambia el eje: **muestrea reservas en lugar de tiempo**, y dice **qué función genera
la basura**.

Y Lisp tiene una capacidad de optimización que merece cerrar esta explicación y que viene de la clase
124: **el compilador dice por qué no puede optimizar**.

```lisp
(declaim (optimize (speed 3) (safety 1) (debug 0)))

(defun sumar (a b) (+ a b))
; note: doing signed word to integer coercion
;       unable to open code because: the operands might not be fixnums
```

**Esa nota es una invitación**: añadiendo una declaración de tipo, el compilador genera aritmética
nativa:

```lisp
(defun sumar (a b)
  (declare (type fixnum a b) (optimize (speed 3)))
  (+ a b))
```

**Es optimización guiada por el compilador, en diálogo**, y es una experiencia que casi ningún otro
lenguaje de esta página ofrece: los demás optimizan en silencio o no optimizan, pero no explican.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set n [string trim $linea]

set total 0
for {set i 1} {$i <= $n} {incr i} {
    incr total $i
}

puts "operaciones=$n resultado=$total"
```

**Lo que esta clase enseña en Tcl.** Tcl trae la medición en el núcleo, con un comando pensado
exactamente para esta clase:

```tcl
puts [time { procesar $datos } 1000]
# → 42.7 microseconds per iteration
```

**`time` ejecuta un guion N veces y da el promedio**, que es la forma correcta de medir algo rápido:
**una sola ejecución mide sobre todo el ruido**.

Y Tcl tiene una particularidad de rendimiento que merece explicarse porque es de las más
contraintuitivas de esta página y ya apareció en la clase 146: **las llaves cambian el rendimiento por
un factor grande**.

```tcl
expr {$a + $b}      ;# se compila a bytecode UNA VEZ (clase 125)
expr "$a + $b"       ;# se sustituye y se REANALIZA en cada iteración
```

**La segunda forma puede ser diez veces más lenta**, porque el compilador de bytecode no puede compilar
una expresión que no conoce hasta que se ejecuta.

Es el mismo principio que en cualquier lenguaje con compilación: **lo que se construye en marcha no se
puede optimizar de antemano**.

Y la otra propiedad de rendimiento característica de Tcl es **la representación dual** (clase 081):

```tcl
set x 42          ;# guardado como cadena "42"
incr x             ;# ahora TAMBIÉN tiene una representación entera, en caché
puts $x            ;# vuelve a generar la cadena si hace falta
```

**Un valor de Tcl guarda a la vez su forma textual y su forma interna optimizada**, y **la conversión se
hace una vez y se recuerda**.

Y de ahí un antipatrón clásico que merece conocerse: **alternar los usos destruye la caché**.

```tcl
# ✗ cada vuelta invalida la representación interna: "shimmering"
for {set i 0} {$i < 100000} {incr i} {
    set s "$lista"        ;# fuerza la forma de CADENA
    lappend lista $i       ;# fuerza la forma de LISTA
}
```

**Ese fenómeno se llama *shimmering*** y es el problema de rendimiento más específico de Tcl: **un valor
que se usa alternativamente como lista y como cadena se reconvierte en cada paso**, y una operación
O(1) pasa a ser O(n).

Y las herramientas:

```tcl
package require profiler
::profiler::init
::profiler::print
tcl::unsupported::disassemble proc miProc     ;# ¡ver el BYTECODE! (clase 125)
```

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

my $total = 0;
$total += $_ for 1 .. $n;

print "operaciones=$n resultado=$total\n";
```

**Lo que esta clase enseña en Perl.** `$total += $_ for 1 .. $n;` es un **modificador de sentencia**, y
`1 .. $n` en un `for` **no construye la lista**: Perl optimiza los rangos en bucles para iterar
perezosamente.

Es un detalle relevante para esta clase: **la misma sintaxis en otro contexto —`my @l = (1 .. $n)`— sí
reserva n elementos**.

Y Perl tiene el mejor perfilador de guiones de esta página, y merece explicarlo: **`Devel::NYTProf`**.

```bash
perl -d:NYTProf script.pl
nytprofhtml --open
```

Y lo que da es notablemente más de lo habitual:

- **Tiempo por LÍNEA**, no solo por subrutina.
- **Tiempo por *bloque* y por sentencia.**
- **Número de llamadas y tiempo exclusivo frente a inclusivo.**
- **Un mapa de calor sobre el código fuente**, en HTML.
- **Y el tiempo de las llamadas a `eval` y a los módulos**, incluido el tiempo de carga.

**El desglose por línea es lo que lo hace útil de verdad**, porque en un lenguaje denso una sola línea
puede contener una expresión regular, dos llamadas y una ordenación.

Y Perl aporta a esta clase la advertencia sobre las expresiones regulares, que es su problema de
rendimiento característico y que conecta con la clase 153: **el retroceso catastrófico**.

```perl
# ✗ esta expresión tarda un tiempo EXPONENCIAL con la entrada
$texto =~ /^(a+)+$/;
# con "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa!" tarda años
```

**El motor prueba todas las formas de repartir las `a` entre los dos cuantificadores.**

Y las defensas:

```perl
use re 'debug';                      # ver qué hace el motor
$texto =~ /^(?>a+)+$/;                # grupo atómico: sin retroceso
$texto =~ /^a++$/;                     # cuantificador posesivo
use Regexp::Debugger;                   # depurador interactivo de regex
```

Es un problema de rendimiento que **también es una vulnerabilidad** —el ataque se llama ReDoS— y es un
buen ejemplo de por qué esta clase y la 153 están juntas: **una entrada elegida por un atacante puede
convertir un tiempo lineal en exponencial**, y ahí el rendimiento deja de ser una cuestión de comodidad.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    long long total = 0;
    for (long long i = 1; i <= n; ++i) total += i;

    std::cout << "operaciones=" << n << " resultado=" << total << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ tiene las mejores herramientas de medición de esta página, y una
lección que merece ir primero: **el compilador es más listo de lo que parece**.

```bash
g++ -O2 -S prog.cpp    # ver el ensamblador generado
```

**Con `-O2`, un bucle que suma 1..n puede desaparecer por completo** si el compilador demuestra que
equivale a `n*(n+1)/2`. Es una optimización real de GCC y LLVM.

Y de ahí la primera advertencia de esta clase, que arruina más mediciones de las que se admite: **el
compilador elimina el código cuyo resultado no se usa**.

```cpp
// ✗ esto no mide nada: el bucle se elimina entero
auto t0 = now();
for (int i = 0; i < 1000000; ++i) calcular(i);
auto t1 = now();

// ✓ impedir la eliminación
benchmark::DoNotOptimize(calcular(i));
```

**Toda medición de microrrendimiento en C++ tiene que usar una barrera de optimización**, o mide el
tiempo de un bucle vacío. Es la razón de existir de `google/benchmark`.

Y el arsenal, organizado por la pregunta que responde:

| Pregunta | Herramienta |
|---|---|
| ¿Dónde se va el tiempo? | `perf record`, VTune, Instruments |
| ¿Cuántos fallos de caché? | `perf stat -e cache-misses`, cachegrind |
| ¿Qué reserva memoria? | `heaptrack`, massif, `perf -e page-faults` |
| ¿Qué hace el compilador? | **Compiler Explorer (godbolt.org)**, `-S`, `-fopt-info` |
| ¿Cuánto tarda esta función? | `google/benchmark`, `nanobench` |
| ¿Y en producción? | **perfiladores continuos**: `pprof`, Parca, eBPF |

**Compiler Explorer merece la mención** porque cambió la cultura: **ver el ensamblador de varios
compiladores lado a lado, en el navegador, al instante** convirtió una pregunta de expertos en algo que
cualquiera puede comprobar.

Y merece cerrar con la observación que la clase 128 anticipó y que en C++ es la más rentable de todas:
**la disposición de los datos importa más que el código**.

```cpp
// ✗ Array of Structs: para sumar solo las x, se traen y y z inútilmente
struct P { float x, y, z; };  std::vector<P> puntos;

// ✓ Struct of Arrays: los x están contiguos
struct Puntos { std::vector<float> x, y, z; };
```

**El segundo puede ser tres veces más rápido en un recorrido que solo usa `x`**, porque **cada línea de
caché trae solo datos útiles**.

Es exactamente la misma lección que LAPACK en Fortran de esta página, aplicada a estructuras en lugar de
a matrices: **el rendimiento moderno es un problema de memoria, no de aritmética**.

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

dcl-pi PERFIL;
  n int(10) const;
end-pi;

dcl-s i     int(10);
dcl-s total int(20);

total = 0;

for i = 1 to n;
  total += i;
endfor;

dsply ('operaciones=' + %char(n) + ' resultado=' + %char(total));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** IBM i comparte el diagnóstico de COBOL en esta página —**el tiempo
está en la entrada y salida**— y aporta la técnica que más rendimiento ha ganado en esta plataforma en
los últimos veinte años, y que merece explicarse porque es un cambio de mentalidad completo: **pasar de
registro a registro a operar por conjuntos**.

```rpgle
// ✗ el idioma clásico de RPG: un viaje por registro
setll (cliente) pedidos;
dow %equal;
  reade (cliente) pedidos;
  if not %eof;
    total += pedidos.importe;
  endif;
enddo;
```

```sql
-- ✓ una sola llamada, y el motor optimiza el acceso
exec sql SELECT SUM(importe) INTO :total
         FROM pedidos WHERE cliente = :cliente;
```

**La diferencia con un millón de filas es de dos órdenes de magnitud**, y el motivo es doble:

**Primero, cada operación registro a registro cruza la frontera entre el programa y el gestor de base
de datos.** Un millón de registros son un millón de cruces.

**Y segundo, y es lo importante: el optimizador de Db2 puede elegir el plan.** Puede usar un índice,
puede paralelizar, puede leer solo el índice si contiene la columna. **El bucle no puede: hace lo que
dice, en el orden que dice.**

Y las herramientas de medición de la plataforma son de las mejores de esta página:

| Herramienta | Qué da |
|---|---|
| **`WRKACTJOB`** | CPU por trabajo, en tiempo real |
| **`STRPFRCOL` / Performance Tools** | recogida histórica de todo el sistema |
| **Visual Explain** | **el plan de acceso de una consulta, en gráfico** |
| **Db2 Index Advisor** | **qué índices FALTAN, deducido del uso real** |
| **`QSYS2.ACTIVE_JOB_INFO`** | todo lo anterior, por SQL (clase 142) |
| **`STRPEX`** (Performance Explorer) | perfil por sentencia de programa |

**El *Index Advisor* merece destacarse** porque hace algo poco común: **el sistema registra las
consultas que se ejecutan y deduce qué índices habrían ayudado**, con una estimación de la mejora.

```sql
SELECT * FROM QSYS2.SYSIXADV ORDER BY TIMES_ADVISED DESC;
```

**Es el sistema diciendo dónde está el cuello de botella**, sin que nadie perfile nada, y es la
aplicación más directa del cierre de esta clase: **medir primero**, con la ventaja de que aquí la medida
ya está tomada.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 perfil: procedure options(main);

    declare n     fixed binary(31);
    declare i     fixed binary(31);
    declare total fixed binary(63) initial(0);

    get list (n);

    do i = 1 to n;
       total = total + i;
    end;

    put skip list ('operaciones=' || trim(char(n)) ||
                   ' resultado=' || trim(char(total)));

 end perfil;
```

**Lo que esta clase enseña en PL/I.** PL/I comparte con COBOL el mundo de la medición por SMF (clase 142)
y aporta una lección de rendimiento propia del lenguaje que merece explicarse, porque es la trampa
número uno de PL/I: **las conversiones implícitas cuestan**.

```pli
 declare a fixed decimal(15,2);
 declare b fixed binary(31);
 declare c float decimal(16);

 a = a + b;         /* binario -> decimal: CONVERSIÓN en cada vuelta */
 c = a * 1.5;        /* decimal -> flotante: otra */
```

**Cada conversión es código generado que no se ve en el fuente**, y en un bucle de millones de vueltas es
la mayor parte del tiempo.

Y el diagnóstico está donde el mundo mainframe siempre lo pone (clase 137): **en el listado de
compilación**.

```text
OPTIONS: LIST, AGGREGATE, ATTRIBUTES, XREF
```

**Con `LIST`, el compilador imprime el ensamblador generado**, y ahí se ven las llamadas a las rutinas
de conversión de la biblioteca — que en el fuente eran un signo `+`.

Es la misma técnica que Compiler Explorer en C++ de esta página, hecha con un listado impreso, y por el
mismo motivo: **ver lo que de verdad se ejecuta, no lo que se escribió**.

Y la regla práctica que se deriva y que vale para cualquier lenguaje con tipos numéricos ricos: **usar
el mismo tipo en todo el cálculo**.

```pli
 declare (a, b, total) fixed binary(63);     /* todo del mismo tipo: cero conversiones */
```

Y hay una decisión de rendimiento propia de PL/I que merece conocerse porque no tiene equivalente:
**las condiciones activadas cuestan**.

```pli
 (subscriptrange, stringrange, size):     /* comprobaciones ACTIVAS */
 procesar: procedure;
```

**Cada acceso a un arreglo comprueba el índice; cada subcadena comprueba los límites** (clases 124 y
137). En un bucle intensivo, eso puede ser el 30 % del tiempo.

Y la decisión —**activarlas en desarrollo y en pruebas, y decidir conscientemente en producción**— es
exactamente la misma que Pascal con `{$R+}`, Ada con `pragma Suppress` y C++ con `assert`.

Es la constante de toda esta parte del curso: **seguridad y velocidad son la misma palanca**, y lo único
que cambia entre lenguajes es quién decide dónde ponerla y si esa decisión queda escrita.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
PERFIL ; Medir operaciones -- clase 152
 read n
 new i, total
 set total = 0
 for i = 1:1:n set total = total + i
 write "operaciones=", n, " resultado=", total, !
 quit
```

**Lo que esta clase enseña en M.** M tiene un modelo de rendimiento peculiar y muy claro: **casi todo el
tiempo se va en la base de datos**, porque **en M no hay diferencia entre una variable y la base de
datos** salvo el circunflejo.

```mumps
 set x = 1            ; memoria: nanosegundos
 set ^x = 1            ; DISCO: microsegundos, y transaccional
```

**Ese circunflejo es la diferencia entre una operación de memoria y una de base de datos**, y es un
carácter.

Y de ahí que la optimización característica de M sea la que ya apareció en la clase 099: **el diseño de
los subíndices de la global**.

```mumps
 ; ✗ recorrer todos los pacientes buscando por apellido
 for  set dfn = $order(^PACIENTE(dfn)) quit:dfn=""  do
 . if $piece(^PACIENTE(dfn, 0), "^", 1) [ apellido ...

 ; ✓ un ÍNDICE: la respuesta en un salto
 set dfn = $order(^PACIENTE("B", apellido, ""))
```

**`^PACIENTE("B", apellido, dfn)` es un índice secundario**, y en VistA se llaman así —`"B"`, `"C"`,
`"AC"`— por convención de FileMan.

**Y `$order` sobre él es O(log n)**, porque las globals son árboles B en disco (clase 099).

Es el mismo razonamiento que un índice de base de datos relacional, con una diferencia importante:
**aquí el índice lo mantiene el programa**, no el motor. Si alguien escribe sin actualizar el índice, el
índice miente — y es el fallo clásico de este mundo.

Y las herramientas de medición:

```mumps
 write $zjobexam                    ; volcado del estado del proceso
 write $storage                      ; memoria disponible
 do ^%SS                              ; estado del sistema: procesos y su actividad
 view "GVSTAT"                         ; estadísticas de acceso a globals (GT.M/YottaDB)
```

**`GVSTAT` es la métrica clave de esta plataforma**: **cuántas lecturas y escrituras de global ha hecho
el proceso**, desglosadas.

Y es la aplicación exacta del cierre de esta clase: **no se mide el tiempo, se cuentan las operaciones
que cuestan**. Un proceso que hace un millón de accesos a global tiene un problema de diseño de índices,
y eso se ve en el contador antes que en el reloj.

Es lo mismo que el `EXCP count` de COBOL en esta página: **en sistemas dominados por la entrada y
salida, contar las operaciones diagnostica mejor que cronometrar**.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| n total |

n := stdin nextLine trimBoth asNumber.
total := 0.

1 to: n do: [ :i | total := total + i ].

Transcript
    show: 'operaciones=', n printString;
    show: ' resultado=', total printString;
    cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk parte de una desventaja de rendimiento evidente
—**todo es un objeto y todo es un envío de mensaje** (clase 125)— y tiene, a cambio, **el perfilador más
integrado de esta página**.

```smalltalk
MessageTally spyOn: [ self procesarTodo ].
```

Y lo que produce es un árbol de llamadas con porcentajes, sobre el sistema vivo:

```text
 - 100.0% (2,340ms) MiClase>>procesarTodo
    | 62.1% (1,453ms) MiClase>>calcular:
    |    | 48.3% (1,130ms) Collection>>detect:
    |    |    | 45.1% (1,055ms) OrderedCollection>>do:
    | 31.2% (730ms) MiClase>>formatear:
```

**Está escrito en Smalltalk, muestrea el proceso desde otro proceso, y no requiere recompilar nada.**

Y el resto del arsenal, todo dentro del sistema:

```smalltalk
[ self calcular ] timeToRun.                    "milisegundos"
[ self calcular ] bench.                         "iteraciones por segundo"
Smalltalk vmStatistics.                           "estadísticas de la máquina virtual"
Smalltalk garbageCollect; garbageCollectMost.      "forzar el recolector"
SpaceTally new spaceTally: MiClase.                 "cuánta memoria ocupa cada clase"
```

**`SpaceTally` merece la mención** porque responde a una pregunta que en la mayoría de los lenguajes es
difícil: **cuánta memoria ocupan las instancias de cada clase, en el sistema real**.

Y Smalltalk aporta a esta clase una lección que la clase 125 anticipó y que merece cerrar: **el
rendimiento de un lenguaje dinámico depende de las cachés de envío**.

```text
Envío de mensaje SIN caché:  buscar el selector en la clase, subir por la jerarquía...
Envío CON caché en línea:    comprobar si la clase es la misma que la última vez → saltar
```

**Y la caché monomórfica en línea acierta más del 90 % de las veces en el código real**, porque **en un
punto concreto del programa, casi siempre llega el mismo tipo de objeto**.

Ese descubrimiento —hecho en Smalltalk y en Self a finales de los ochenta— es el fundamento de **todos
los compiladores JIT modernos**: V8, HotSpot, LuaJIT y PyPy usan la misma técnica, con el mismo nombre.

Y la conclusión que conecta con la primera línea de esta explicación: **la desventaja teórica del
despacho dinámico se recuperó en gran parte con una observación empírica sobre cómo se comportan los
programas de verdad**.

Es la mejor ilustración del cierre de esta clase: **la intuición decía que el despacho dinámico era
inviable; la medición dijo que era predecible**.

---

## Y de vuelta a la clase

Lo transferible: **medir, cambiar una cosa, volver a medir** — y en ese orden, siempre. La razón es que
el cuello de botella casi nunca está donde se cree: en la mayoría de los programas reales, el tiempo se
va en **esperar entrada y salida, en fallos de caché y en reservar memoria**, no en el bucle que parece
caro. Y la segunda regla, que ahorra más trabajo que ninguna optimización: **preguntar antes si hace
falta que sea rápido**. Un proceso nocturno que tarda veinte minutos y tiene ocho horas de ventana no
tiene un problema de rendimiento, por mucho que se pueda mejorar.

⏮️ [Volver a la clase 152](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
