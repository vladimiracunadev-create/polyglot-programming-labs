# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 133

> [⬅️ Volver a la clase 133](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Contar elementos. El programa es trivial y la pregunta de esta clase es la del sistema operativo:
**¿qué es exactamente una unidad de ejecución?** La clase 121 vio los modelos de los lenguajes; esta
mira debajo, y ahí estos doce se reparten en dos mundos: **los que usan hilos del sistema** —C++,
Fortran, Ada, Pascal— y **los que usan procesos o hilos verdes** —Perl, Tcl, Smalltalk, COBOL, RPG,
M—, que resultó ser la decisión que la industria acabó adoptando.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **el coste de la unidad de ejecución**: cuánto ocupa, cuánto cuesta crearla y quién
> la planifica. Estos lenguajes lo enseñan porque probaron los dos extremos durante décadas. **Un
> proceso del sistema** cuesta megabytes y milisegundos y **aísla por completo**; **un hilo** cuesta
> kilobytes y microsegundos y **comparte toda la memoria**; **un hilo verde** cuesta cientos de bytes y
> lo planifica el propio runtime.
>
> Y el veredicto histórico está en esta página: **COBOL con CICS, RPG con sus trabajos y M con sus
> procesos eligieron el aislamiento**, y sostienen las cargas concurrentes más grandes que existen.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con enteros separados por espacio → stdout: `cuenta=<número de elementos>`
- **Regla:** `acumulador compartido que cuenta los elementos`

| stdin | esperado |
|---|---|
| `1 2 3` | `cuenta=3` |
| `5` | `cuenta=1` |
| `10 20 30 40` | `cuenta=4` |

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
PROGRAM-ID. CONCURR.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  I       PIC 9(4) COMP.
01  N       PIC 9(4) COMP VALUE 0.
01  DENTRO  PIC 9   COMP VALUE 0.
01  ED-N    PIC Z(3)9.

PROCEDURE DIVISION.
    ACCEPT LINEA

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        IF LINEA(I:1) = SPACE
            MOVE 0 TO DENTRO
        ELSE
            IF DENTRO = 0
                ADD 1 TO N
                MOVE 1 TO DENTRO
            END-IF
        END-IF
    END-PERFORM

    MOVE N TO ED-N
    DISPLAY "cuenta=" FUNCTION TRIM(ED-N)
    STOP RUN.
```

**Lo que esta clase enseña en COBOL.** La unidad de concurrencia de un sistema COBOL es **la
transacción**, y merece mirar qué es por debajo, porque no es ni un proceso ni un hilo.

En **CICS**, una transacción se ejecuta en una **tarea**: una estructura ligera que el monitor
planifica **dentro de una región**, que sí es un proceso del sistema.

```text
Región CICS (un proceso del z/OS)
  └─ miles de TAREAS, planificadas por CICS, no por el sistema operativo
```

**CICS es un planificador de hilos verdes de 1969.** Sus tareas cuestan poco, no las ve el sistema
operativo, y el monitor decide cuál corre — exactamente lo que hoy hacen las corrutinas de Go y los
hilos virtuales de Java 21.

Y la decisión clave, ya vista en las clases 119 y 121: **las tareas no comparten estado mutable**. Cada
una tiene su copia de la `WORKING-STORAGE` del programa que ejecuta, y lo compartido —ficheros, colas,
áreas comunes— **está bajo control del gestor de recursos, con bloqueo y transacción**.

Esa arquitectura es la razón de que un CICS grande atienda **decenas de miles de transacciones por
segundo** con latencias predecibles, y de que las condiciones de carrera no sean un problema
cotidiano en ese mundo.

Y CICS moderno añadió los hilos del sistema donde hacen falta: **los TCB abiertos** (*open transaction
environment*), que permiten que una tarea que llame a Java o a código que bloquea **se ejecute en su
propio hilo del sistema** sin detener a las demás.

Es el mismo problema que resuelven los hilos de plataforma bajo los hilos virtuales de Java: **una
llamada bloqueante no debe bloquear al planificador**.

Y merece cerrar con la observación de escala: **una región CICS con 50.000 tareas concurrentes es
normal**. Con hilos del sistema operativo, eso serían 50.000 pilas de 1 MB — 50 GB solo en pilas. La
razón de los hilos verdes no es elegancia: **es que la aritmética no sale de otra forma**.

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
program concurr
   implicit none
   integer :: v(200), n, ios, i
   character(len=400) :: linea

   read(*, '(A)') linea

   n = 0
   do i = 1, 200
      read(linea, *, iostat=ios) v(1:i)
      if (ios /= 0) exit
      n = i
   end do

   write(*, '(A,I0)') 'cuenta=', n
end program concurr
```

**Lo que esta clase enseña en Fortran.** Fortran usa **procesos** para el paralelismo de verdad, y esa
elección viene de la escala a la que trabaja.

Un modelo climático corre en **cientos o miles de nodos**, cada uno con memoria propia, conectados por
red de alta velocidad. **Ahí no hay memoria compartida que compartir**: la unidad tiene que ser el
proceso.

De ahí los dos modelos que usa:

**MPI** —una biblioteca, no parte del lenguaje— donde cada proceso es independiente y se comunica con
mensajes explícitos:

```fortran
call MPI_Init(ierr)
call MPI_Comm_rank(MPI_COMM_WORLD, mi_rango, ierr)
call MPI_Send(datos, n, MPI_REAL, destino, etiqueta, MPI_COMM_WORLD, ierr)
call MPI_Recv(datos, n, MPI_REAL, origen, etiqueta, MPI_COMM_WORLD, estado, ierr)
```

**Y los coarrays** (clase 121), que son lo mismo integrado en el lenguaje:

```fortran
real :: campo(100)[*]
campo(:)[3] = campo(:)[1]        ! el compilador genera la comunicación
sync all
```

Y dentro de cada nodo, Fortran usa **hilos** con OpenMP, que es donde sí hay memoria compartida:

```fortran
!$omp parallel do reduction(+:suma)
do i = 1, n
   suma = suma + v(i)
end do
!$omp end parallel do
```

**Ese modelo híbrido —MPI entre nodos, OpenMP dentro— es la arquitectura estándar de la computación de
alto rendimiento**, y responde exactamente a la pregunta del cierre de esta clase: **se comparte lo
que está físicamente cerca y se copia lo que está lejos**.

Y hay un detalle de rendimiento que esta clase debe contar y que domina en máquinas grandes: **NUMA**.

En un nodo con varios procesadores, **la memoria de otro socket es más lenta**, así que **dónde vive un
dato importa**. Fortran y OpenMP tienen mecanismos —la política de primer toque, `numactl`, las
afinidades de hilo— para colocar los datos cerca de quien los usa.

Es una capa que la mayoría de los lenguajes de esta página ignora, y que en cálculo puede significar un
factor de dos.

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Concurr is
   Linea  : String (1 .. 400);
   Ultimo : Natural;
   Pos    : Integer := 1;
   Valor  : Integer;
   Fin    : Positive;
   N      : Natural := 0;
begin
   Get_Line (Linea, Ultimo);

   loop
      while Pos <= Ultimo and then Linea (Pos) = ' ' loop
         Pos := Pos + 1;
      end loop;
      exit when Pos > Ultimo;
      Get (Linea (Pos .. Ultimo), Valor, Fin);
      N := N + 1;
      Pos := Fin + 1;
   end loop;

   Put ("cuenta=");
   Put (N, Width => 1);
   New_Line;
end Concurr;
```

**Lo que esta clase enseña en Ada.** Ada tiene tareas en el lenguaje (clase 121), y **el estándar no
dice cómo se implementan**: eso lo decide el runtime, y esa flexibilidad es deliberada.

En la práctica hay tres implementaciones, y elegir entre ellas es una decisión de despliegue:

| Runtime | Las tareas son | Dónde se usa |
|---|---|---|
| **Completo** | hilos del sistema (pthreads) | Linux, Windows |
| **Ravenscar** | tareas planificadas por el runtime | tiempo real empotrado |
| **ZFP / bare metal** | corrutinas sobre el hardware | microcontroladores |

**El mismo código Ada puede compilarse para los tres**, y esa portabilidad es lo que se buscaba en 1983:
que el modelo de concurrencia fuera del lenguaje, no del sistema operativo.

Y Ada expone lo que hace falta para el control de tiempo real, que ningún otro lenguaje de esta página
tiene en el estándar:

```ada
pragma Priority (10);                          --  prioridad de la tarea
pragma Task_Dispatching_Policy (FIFO_Within_Priorities);
pragma Locking_Policy (Ceiling_Locking);        --  techo de prioridad
pragma Queuing_Policy (Priority_Queuing);        --  clase 096
delay until Siguiente_Periodo;                    --  instante ABSOLUTO
```

**`Ceiling_Locking`** merece la explicación porque resuelve un problema real y famoso: **la inversión de
prioridades**.

Ocurre cuando una tarea de baja prioridad tiene un recurso que necesita una de alta prioridad, y una
de prioridad media impide a la baja terminar. La de alta prioridad queda bloqueada indefinidamente por
una de media.

**Eso es lo que le pasó a la Mars Pathfinder en 1997**: la sonda se reiniciaba sola en Marte por una
inversión de prioridades, y se arregló activando la herencia de prioridad **por telemetría, desde la
Tierra**.

**El protocolo de techo de prioridad de Ada evita el problema por construcción**: quien toma un objeto
protegido **sube automáticamente a la prioridad más alta de todos los que puedan usarlo**, así que nadie
de prioridad media puede interponerse.

Que eso sea una directiva del lenguaje y no una opción de biblioteca es la razón de que Ada siga siendo
la elección para sistemas donde llegar tarde es un fallo.

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
program Concurr;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea: string;
  I, N: Integer;
  Dentro: Boolean;

begin
  ReadLn(Linea);

  N := 0;
  Dentro := False;
  for I := 1 to Length(Linea) do
  begin
    if Linea[I] = ' ' then
      Dentro := False
    else if not Dentro then
    begin
      Inc(N);
      Dentro := True;
    end;
  end;

  WriteLn('cuenta=', IntToStr(N));
end.
```

**Lo que esta clase enseña en Pascal.** Los hilos de Object Pascal son **hilos del sistema operativo**,
y `TThread` es una envoltura fina sobre ellos.

Y esta clase permite señalar el detalle de la clase 121 que más sorprende a quien empieza en Free
Pascal:

```pascal
program MiPrograma;
uses
  {$IFDEF UNIX} cthreads, {$ENDIF}     { ¡DEBE ir la PRIMERA! }
  Classes, SysUtils;
```

**Sin `cthreads` como primera unidad, el soporte de hilos de Free Pascal no se inicializa** en Unix, y
el programa falla de formas confusas —a menudo al usar cadenas o el gestor de memoria desde un hilo—.

La razón es técnica y reveladora: **el gestor de memoria y el de cadenas de Free Pascal tienen versiones
con y sin bloqueo**, y `cthreads` instala las seguras para hilos. Sin ella, el runtime asume un solo
hilo y usa las rápidas.

Es un ejemplo de algo que esta clase quiere mostrar: **el soporte de concurrencia no está solo en la
sintaxis, está en el runtime entero** — el gestor de memoria, el de excepciones y el de cadenas tienen
que ser seguros para hilos.

Y de ahí la otra regla del ecosistema, ya nombrada: **la biblioteca visual no es segura para hilos**.

```pascal
TThread.Synchronize(nil, procedure begin Etiqueta.Caption := Texto end);
TThread.Queue(nil, procedure begin ... end);     { asíncrono, sin esperar }
```

**`Synchronize` bloquea hasta que el hilo principal ejecute el bloque; `Queue` lo encola y sigue.** Esa
distinción es la misma que en Swing entre `invokeAndWait` e `invokeLater`.

Y Delphi moderno añade la capa de más alto nivel de la clase 122:

```pascal
TParallel.For(1, N, procedure(I: Integer) begin ... end);
TTask.Run(...).Wait;
TThreadedQueue<T>;                    { cola con bloqueo, para productor-consumidor }
```

**`TThreadedQueue`** es el canal de esta parte: una cola con bloqueo y capacidad limitada, que es
contrapresión (clase 120).

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((n 0))
  (loop for x = (read *standard-input* nil nil)
        while x
        do (incf n))
  (format t "cuenta=~D~%" n))
```

**Lo que esta clase enseña en Common Lisp.** Como se dijo en la clase 121, el estándar no menciona la
concurrencia, y las implementaciones eligieron distinto — lo que hace de Lisp un buen mirador para esta
clase.

| Implementación | Modelo |
|---|---|
| **SBCL** | hilos del sistema operativo |
| **CCL** | hilos del sistema |
| **CLISP** | sin hilos (o muy limitados) |
| **ECL** | hilos del sistema, y corrutinas |
| **LispWorks / Allegro** | hilos, con planificador propio |

Y **Bordeaux-Threads** unifica la API por encima.

Lo que Lisp aporta a esta clase, y es específico de un lenguaje con recolector, es el problema que la
clase 131 anticipaba: **la interacción entre el recolector y los hilos**.

Un recolector tiene que **detener todos los hilos** para recorrer el montón con seguridad —o usar
barreras y hacerlo concurrentemente— y ese es uno de los problemas más difíciles de implementar en un
runtime.

En SBCL se ve:

```lisp
(sb-ext:gc :full t)                  ; detiene todos los hilos
sb-thread:*all-threads*               ; los hilos vivos
(sb-thread:make-thread ... :name "x")
```

Y hay una decisión de diseño de SBCL que merece nombrarse: **las variables especiales son por hilo**
(clase 121), con lo que `*standard-output*` se puede redirigir en un hilo sin afectar a los demás.

Eso hace que **el estado dinámico esté aislado por defecto** y solo el estado global explícito se
comparta — una decisión muy alineada con el cierre de esta clase.

Y para el paralelismo de datos, el ecosistema tiene la capa que oculta todo esto:

```lisp
(lparallel:pmap 'list #'procesar datos)      ; grupo de hilos, reparto automático
(lparallel:pdotimes (i n) ...)
```

**lparallel gestiona un grupo de trabajadores** y reparte, con lo que el programador no ve hilos.

Es el mismo camino que ha seguido toda la industria: **de los hilos a los grupos de trabajadores y de
ahí a las operaciones paralelas declarativas** — que es lo que Fortran tiene con `do concurrent` desde
2008.

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea
set v [split [string trim $linea]]

puts "cuenta=[llength $v]"
```

**Lo que esta clase enseña en Tcl.** Tcl tomó en esta clase la decisión más radical de la página y la
que mejor ha envejecido: **un intérprete por hilo, sin nada compartido** (clase 121).

```tcl
package require Thread
set id [thread::create]           ;# un INTÉRPRETE COMPLETO, nuevo
thread::send $id { ... }
```

Y merece explicar por qué se eligió eso, porque la razón es de implementación: **hacer que un
intérprete sea seguro para hilos con memoria compartida es carísimo**.

Todo lo que Tcl tiene —la tabla de comandos, la de variables, los objetos con conteo de referencias, la
caché de bytecode— tendría que estar protegido con cerrojos, y **cada acceso pagaría el coste**.

Con un intérprete por hilo, **nada se comparte y nada necesita bloqueo**: cada uno va a velocidad
completa.

Es exactamente el mismo razonamiento que llevó a **Python al GIL** —proteger el intérprete con un solo
cerrojo global— y a **Perl a iThreads** (clase 121). Los tres lenguajes se encontraron con el mismo
problema en los noventa y eligieron distinto:

| | Solución | Consecuencia |
|---|---|---|
| **Tcl** | un intérprete por hilo | **paralelismo real**, comunicación por mensajes |
| **Perl** | copiar el intérprete al crear el hilo | **caro**: desaconsejado |
| **Python** | un cerrojo global (GIL) | **sin paralelismo** de CPU en un proceso |

**La de Tcl es la que ha resultado mejor con el tiempo**, y es la que Python está adoptando treinta años
después con los **subintérpretes con GIL propio** de PEP 684 y el modo sin GIL de PEP 703.

Y Tcl añade lo que hace usable el modelo:

```tcl
tsv::set compartido clave valor       ;# variables compartidas explícitas, sincronizadas
tpool::create -maxworkers 4            ;# grupo de trabajadores
thread::send -async $id { ... } var     ;# envío asíncrono con respuesta
```

**`tsv`** es el único estado compartido, y está sincronizado por el sistema — lo que el cierre de esta
clase recomienda: **compartir poco y explícitamente**.

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my @v = split ' ', $linea;

print "cuenta=", scalar(@v), "\n";
```

**Lo que esta clase enseña en Perl.** La historia de Perl con los hilos, contada en la clase 121, es el
mejor caso de estudio de esta clase, y merece el detalle de implementación.

**iThreads copia el intérprete entero al crear un hilo.** Eso significa:

```text
crear un hilo = clonar todas las variables, todos los paquetes, todos los módulos cargados
```

Con veinte módulos de CPAN cargados, eso son **decenas de megabytes por hilo** y un tiempo de creación
enorme. En un servidor que crea un hilo por petición, es inviable.

De ahí que la respuesta idiomática sea **`fork`**, y aquí está la razón técnica de que sea barata en
Unix: **la copia al escribir del sistema operativo**.

```perl
my $pid = fork();
```

**`fork` no copia la memoria: marca las páginas como de solo lectura y las comparte**, y solo copia una
página cuando alguno de los dos procesos escribe en ella. Un proceso hijo que solo lee **no copia
nada**.

Ese mecanismo es el que hace viable el modelo de preforkeo que usaron Apache, `Starman`, `uWSGI` y
media web durante veinte años:

```text
arrancar → cargar todos los módulos → fork() N veces → los hijos COMPARTEN el código cargado
```

**La memoria del código y de los datos de solo lectura se comparte físicamente**, así que veinte
procesos ocupan mucho menos que veinte veces uno.

Y el ecosistema lo empaqueta:

```perl
use Parallel::ForkManager;
my $pm = Parallel::ForkManager->new(4);
for my $tarea (@tareas) {
    $pm->start and next;
    procesar($tarea);
    $pm->finish;
}
$pm->wait_all_children;
```

Es exactamente el cierre de esta clase: **no compartir estado mutable, aprovechar lo inmutable**. Y lo
resolvió el sistema operativo, no el lenguaje.

Merece cerrar con el matiz: **en Windows no hay `fork` real**, y Perl lo emula con hilos — con lo que
todas las ventajas desaparecen. Es una de las diferencias de portabilidad más grandes del ecosistema.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <iterator>
#include <vector>

int main() {
    const std::vector<int> v{std::istream_iterator<int>(std::cin),
                             std::istream_iterator<int>()};

    std::cout << "cuenta=" << v.size() << '\n';
    return 0;
}
```

**Lo que esta clase enseña en C++.** C++ usa **hilos del sistema operativo**, sin capa intermedia:
`std::thread` es una envoltura directa sobre `pthread_create` o la API de Windows.

Y esa decisión es coherente con el principio del lenguaje —**no pagar por lo que no usas**— y tiene el
coste que esta clase quiere cuantificar:

```text
crear un hilo del sistema:  ~10-100 microsegundos, 1-8 MB de pila reservada
crear una corrutina:         ~100 nanosegundos, cientos de bytes
```

**Tres órdenes de magnitud.** Por eso un servidor que crea un hilo por conexión se agota en unos miles
de conexiones, y de ahí el famoso *problema de las 10.000 conexiones*.

C++ da las herramientas para no crear hilos constantemente:

```cpp
std::async(std::launch::async, tarea);          // puede usar un grupo (depende)
std::jthread                                      // C++20: se une solo (clase 121)
std::hardware_concurrency()                        // cuántos núcleos hay
```

Y para el paralelismo de datos, C++17 añadió **las políticas de ejecución**, que es lo más declarativo
que tiene el lenguaje:

```cpp
#include <execution>
std::sort(std::execution::par, v.begin(), v.end());
std::reduce(std::execution::par_unseq, v.begin(), v.end());
```

**`std::execution::par` le dice al algoritmo que puede paralelizar**, y la implementación decide cómo
—normalmente con Intel TBB o con OpenMP por debajo—. Es exactamente el `do concurrent` de Fortran
(clase 121), llegado nueve años después.

Y sobre memoria compartida, C++11 aportó lo que de verdad faltaba y que la clase 121 mencionaba: **el
modelo de memoria**.

Antes de C++11, **el estándar no decía nada sobre qué ve un hilo de lo que escribe otro**, así que el
código concurrente dependía del compilador y del procesador. C++11 lo especificó, con
`std::atomic` y los órdenes de memoria — y ese trabajo **lo adoptó después C11 y sirvió de modelo a
Rust**.

Es una de las contribuciones más importantes de C++ a la informática, y no tiene sintaxis vistosa: es
un capítulo del estándar.

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

dcl-pi CONCURR;
  entrada char(200) const;
end-pi;

dcl-s texto  varchar(200);
dcl-s c      char(1);
dcl-s i      int(10);
dcl-s n      int(10) inz(0);
dcl-s dentro ind inz(*off);

texto = %trimr(entrada);

for i = 1 to %len(texto);
  c = %subst(texto : i : 1);
  if c = ' ';
    dentro = *off;
  else;
    if not dentro;
      n += 1;
      dentro = *on;
    endif;
  endif;
endfor;

dsply ('cuenta=' + %char(n));

*inlr = *on;
return;
```

**Lo que esta clase enseña en RPG.** La unidad de concurrencia de IBM i es **el trabajo**, y merece
explicar qué es, porque no encaja exactamente en la división de esta clase.

Un **trabajo** (*job*) de IBM i es más que un proceso: **es una unidad administrable con su propia cola
de mensajes, su biblioteca de trabajo, su descripción, sus atributos de ejecución y su registro**.

```text
Subsistema (contenedor de trabajos, con reglas y recursos)
  └─ Trabajos, cada uno con sus hilos, su memoria y su identidad
```

Y **el subsistema es el planificador administrable**: se configura cuántos trabajos concurrentes
admite, con qué prioridad, en qué grupo de memoria y de qué cola toman el trabajo — **todo desde fuera
del programa**.

```text
CRTSBSD SBSD(MIAPP) POOLS((1 *BASE))
ADDJOBQE SBSD(MIAPP) JOBQ(MIAPP) MAXACT(4)     -- máximo 4 a la vez
```

**Cambiar `MAXACT` de 4 a 10 cambia el paralelismo de la aplicación sin tocar ni recompilar nada.**

Es la misma idea que ajustar el tamaño de un grupo de trabajadores, con la diferencia de que **está en
el sistema operativo y lo administra un operador**.

Y sobre memoria compartida, IBM i usa el modelo de esta página: **los trabajos no comparten memoria**,
y lo compartido son objetos del sistema —espacios de usuario, colas de datos, espacios de datos, la
base de datos— **con bloqueo y transacción**.

RPG sí puede crear hilos, con las API `pthread`, y **la plataforma lo desaconseja** (clase 121): el
modelo es multitrabajo.

Y hay una razón histórica que lo explica: **el estado estático de un módulo se comparte entre los hilos
de un trabajo** (clase 087), así que la mayoría del código RPG existente **no es seguro para hilos**. Un
programa de treinta años con variables globales no puede ejecutarse en dos hilos a la vez.

Es la misma barrera que Python tiene con las extensiones en C y el GIL: **la compatibilidad hacia atrás
condiciona el modelo de concurrencia**.

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
 concurr: procedure options(main);

    declare linea char(200) varying;
    declare c char(1);
    declare (i, n) fixed binary(31);
    declare dentro bit(1);

    get edit (linea) (a(200));
    linea = trim(linea);
    n = 0;
    dentro = '0'b;

    do i = 1 to length(linea);
       c = substr(linea, i, 1);
       if c = ' ' then dentro = '0'b;
       else do;
          if ^dentro then do;
             n = n + 1;
             dentro = '1'b;
          end;
       end;
    end;

    put skip list ('cuenta=' || trim(char(n)));

 end concurr;
```

**Lo que esta clase enseña en PL/I.** PL/I tenía multitarea en 1964 (clase 121), y esta clase permite
mirar **qué era una `task` por debajo**, porque no era un hilo en el sentido actual.

En el z/OS de la época, una tarea era una **TCB** (*Task Control Block*), la unidad de planificación
del sistema operativo. **`call ... task(t)` creaba una TCB**, con su propia pila y su estado, dentro del
mismo espacio de direcciones.

**Eso es exactamente un hilo**, y el término no existía todavía: los "hilos" se popularizaron en los
ochenta con Mach y con los sistemas Unix.

Y merece señalar la coincidencia: **z/OS tuvo hilos con memoria compartida dentro de un proceso desde
los años sesenta**, y Unix no los tuvo hasta veinticinco años después.

Lo que pasó con la multitarea de PL/I ya se contó y es la lección de esta clase: **casi nadie la usó**,
y el motivo tiene que ver con la pregunta del cierre.

**En un mainframe, el paralelismo venía de ejecutar muchos trabajos y muchas transacciones a la vez**,
cada uno con su memoria, y el sistema operativo lo gestionaba. La concurrencia dentro de un programa
resolvía un problema que casi nadie tenía.

Y había una razón más práctica: **el modelo de datos**. Con `static` y `external` compartidos entre
tareas y sin sincronización comprobada, **escribir código concurrente correcto en PL/I era tan difícil
como en C** — y en un entorno donde la corrección financiera es lo primero, nadie lo intentaba sin
necesidad.

Es la conclusión que esta parte del curso ha ido acumulando sobre PL/I, y aquí se ve otra vez: **tenía
la característica, la plataforma resolvía el problema por otra vía, y la característica no arraigó**.

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
CONCURR ; Concurrencia -- clase 133
 read linea
 write "cuenta=", $length(linea, " "), !
 quit
```

**Lo que esta clase enseña en M.** M usa **procesos del sistema operativo**, cada uno con su intérprete
y su espacio de variables locales, y **lo único compartido son los *globals*** (clase 121).

Y esta clase permite explicar por qué eso funciona tan bien a escala, porque el mecanismo es
interesante: **la memoria compartida de la base de datos**.

```text
Proceso 1 ─┐
Proceso 2 ─┼─→ CACHÉ DE BLOQUES en memoria COMPARTIDA ─→ ficheros de base de datos
Proceso N ─┘
```

**Todos los procesos comparten la caché de bloques de la base de datos**, así que un bloque leído por
uno está disponible para todos sin volver a leerlo, y las escrituras se agrupan y se ordenan.

Es memoria compartida **con una disciplina de acceso muy estricta** —bloqueo por nodo (clase 121),
transacciones, registro por delante— en lugar de memoria compartida libre con cerrojos ad hoc.

Y esa es exactamente la respuesta del cierre de esta clase: **se comparte, y a través de un mecanismo
que impone las reglas**.

De ahí una propiedad medible que sorprende: **un sistema M con diez mil procesos concurrentes sobre los
mismos datos es normal**, y no tiene los problemas de un servidor con diez mil hilos, porque **el
estado mutable compartido está todo en un sitio, con transacciones**.

Y las implementaciones modernas lo llevan más lejos:

- **YottaDB** usa memoria compartida POSIX y semáforos, con procesos independientes.
- **IRIS** tiene un modelo de procesos con caché compartida y **ECP** (*Enterprise Cache Protocol*),
  que **extiende esa caché compartida a varias máquinas** — memoria compartida distribuida sobre red.

**ECP** es notable: un proceso en la máquina B accede a un *global* de la máquina A **con la misma
sintaxis**, y el protocolo se ocupa de la coherencia de la caché y de los bloqueos distribuidos.

Es memoria compartida distribuida, un problema que la investigación en sistemas distribuidos considera
difícil, resuelto para un modelo de datos concreto y en producción desde hace décadas.

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| v |

v := stdin nextLine substrings.

Transcript show: 'cuenta=', v size printString; cr.
```

**Lo que esta clase enseña en Smalltalk.** Smalltalk usa **hilos verdes**: los `Process` son objetos
planificados por la propia máquina virtual, **no por el sistema operativo** (clase 121).

```smalltalk
[ ... ] fork.
Processor activeProcess.
Processor yield.
Processor userSchedulingPriority.
```

Y esta clase permite dar los números que hacen relevante esa decisión:

```text
Process de Smalltalk:  un objeto con su contexto → cientos de bytes
hilo del sistema:       pila reservada → 1-8 MB
```

**Crear cien mil procesos Smalltalk es viable; crear cien mil hilos del sistema, no.**

Y el planificador es de prioridades con **cesión cooperativa dentro de cada nivel** (clase 121): un
proceso corre hasta que se bloquea o llama a `yield`, y los de prioridad mayor lo desalojan.

Eso tiene la ventaja que aquella clase señalaba —**dentro de una prioridad no hay carreras**— y el
inconveniente de que **un proceso que no cede bloquea a los de su nivel**.

Y aquí está la limitación real de Pharo hoy: **la máquina virtual usa un solo hilo del sistema
operativo**, así que **los procesos de Smalltalk no aprovechan varios núcleos**.

Para el paralelismo real, el ecosistema usa lo que el cierre de esta clase recomienda: **varias
imágenes comunicándose por mensajes**.

```smalltalk
"lanzar otra imagen y hablar con ella por sockets o por STON (clase 105)"
```

Es el modelo de actores, y es la misma decisión que Tcl con sus intérpretes y que Erlang con sus
procesos.

Y merece cerrar con el dato histórico que conecta esta página entera: **Erlang, el lenguaje que
convirtió ese modelo en su bandera, se diseñó en Ericsson a mediados de los ochenta**, y sus autores
citan Smalltalk y Prolog entre sus influencias.

**Los procesos ligeros aislados que se comunican por mensajes —el modelo BEAM de la clase 135— son la
idea de Smalltalk y de los actores de Hewitt**, industrializada para telefonía.

Y hoy, con los hilos virtuales de Java 21 y las corrutinas de Go, **es el modelo dominante**. Cuarenta
años después.

---

## Y de vuelta a la clase

Lo transferible: **la pregunta no es "¿procesos o hilos?" sino "¿qué se comparte?"**. Compartir memoria
es rapidísimo y obliga a sincronizar todo; no compartir nada obliga a copiar y elimina una clase entera
de errores. Y hay un punto intermedio que la industria redescubrió hace poco: **hilos ligeros que no
comparten estado mutable y se comunican por mensajes** — Erlang, Go, los actores y los hilos virtuales
de Java 21. Es exactamente lo que hacen los sistemas de esta página desde hace cuarenta años.

⏮️ [Volver a la clase 133](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
