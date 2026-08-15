# -*- coding: utf-8 -*-
"""Parte 8, lote I — clases 133 y 134. Ver `vivos_parte8.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 133 — Concurrencia: procesos, hilos y memoria compartida
# ---------------------------------------------------------------------------
SPECS["133"] = dict(
    gancho="""
Contar elementos. El programa es trivial y la pregunta de esta clase es la del sistema operativo:
**¿qué es exactamente una unidad de ejecución?** La clase 121 vio los modelos de los lenguajes; esta
mira debajo, y ahí estos doce se reparten en dos mundos: **los que usan hilos del sistema** —C++,
Fortran, Ada, Pascal— y **los que usan procesos o hilos verdes** —Perl, Tcl, Smalltalk, COBOL, RPG,
M—, que resultó ser la decisión que la industria acabó adoptando.
""",
    porque="""
Aquí el concepto es **el coste de la unidad de ejecución**: cuánto ocupa, cuánto cuesta crearla y quién
la planifica. Estos lenguajes lo enseñan porque probaron los dos extremos durante décadas. **Un
proceso del sistema** cuesta megabytes y milisegundos y **aísla por completo**; **un hilo** cuesta
kilobytes y microsegundos y **comparte toda la memoria**; **un hilo verde** cuesta cientos de bytes y
lo planifica el propio runtime.

Y el veredicto histórico está en esta página: **COBOL con CICS, RPG con sus trabajos y M con sus
procesos eligieron el aislamiento**, y sostienen las cargas concurrentes más grandes que existen.
""",
    cierre="""
Lo transferible: **la pregunta no es "¿procesos o hilos?" sino "¿qué se comparte?"**. Compartir memoria
es rapidísimo y obliga a sincronizar todo; no compartir nada obliga a copiar y elimina una clase entera
de errores. Y hay un punto intermedio que la industria redescubrió hace poco: **hilos ligeros que no
comparten estado mutable y se comunican por mensajes** — Erlang, Go, los actores y los hilos virtuales
de Java 21. Es exactamente lo que hacen los sistemas de esta página desde hace cuarenta años.
""",
    langs={
        "cobol": ("""
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
""", """
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
"""),
        "fortran": ("""
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
""", """
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
"""),
        "ada": ("""
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
""", """
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
"""),
        "pascal": ("""
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
""", """
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
"""),
        "lisp": ("""
(let ((n 0))
  (loop for x = (read *standard-input* nil nil)
        while x
        do (incf n))
  (format t "cuenta=~D~%" n))
""", """
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
"""),
        "tcl": ("""
gets stdin linea
set v [split [string trim $linea]]

puts "cuenta=[llength $v]"
""", """
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
"""),
        "perl": ("""
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my @v = split ' ', $linea;

print "cuenta=", scalar(@v), "\\n";
""", """
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
"""),
        "cpp": ("""
#include <iostream>
#include <iterator>
#include <vector>

int main() {
    const std::vector<int> v{std::istream_iterator<int>(std::cin),
                             std::istream_iterator<int>()};

    std::cout << "cuenta=" << v.size() << '\\n';
    return 0;
}
""", """
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
"""),
        "rpg": ("""
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
""", """
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
"""),
        "pli": ("""
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
""", """
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
"""),
        "mumps": ("""
CONCURR ; Concurrencia -- clase 133
 read linea
 write "cuenta=", $length(linea, " "), !
 quit
""", """
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
"""),
        "smalltalk": ("""
| v |

v := stdin nextLine substrings.

Transcript show: 'cuenta=', v size printString; cr.
""", """
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
"""),
    },
)

# ---------------------------------------------------------------------------
# 134 — Tareas, corrutinas y canales
# ---------------------------------------------------------------------------
SPECS["134"] = dict(
    gancho="""
Encontrar el máximo. La pregunta de esta clase es **cómo se suspende y se reanuda algo sin bloquear un
hilo**, y su respuesta más antigua está aquí: **Melvin Conway acuñó "corrutina" en 1958**, describiendo
un compilador de COBOL. Y en esta página hay dos implementaciones vivas: **las corrutinas de Tcl
(2012)** y **la cita de Ada (1983)**, que es un canal síncrono con otro nombre.
""",
    porque="""
Aquí el concepto es la **suspensión sin bloqueo**: guardar el estado de una ejecución y reanudarla
después. Estos lenguajes lo enseñan porque contienen el origen —el término es de 1958, describiendo
cómo se comunicaban las fases de un compilador— y porque tienen las dos formas modernas.

**El canal síncrono**: la cita de Ada, donde emisor y receptor se encuentran y se bloquean el uno por
el otro. **Y la corrutina**: Tcl, con `yield` y reanudación por nombre, sin colorear funciones (clase
122). Los dos resuelven lo mismo desde lados opuestos —**la sincronización por encuentro y la
suspensión explícita**— y los dos preceden a Go en décadas.
""",
    cierre="""
Lo transferible: **un canal y una corrutina son la misma idea vista desde dos sitios**. Una corrutina
que hace `yield` de un valor a otra es, de hecho, un canal de capacidad cero; y un canal con un
productor y un consumidor es un par de corrutinas. Lo que cambia es quién controla el flujo: con
corrutinas lo controla el código; con canales, la disponibilidad de los datos. Cuando diseñes,
pregúntate **qué debe esperar a qué**, y la elección se decide sola.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. TAREAS.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(2)  COMP VALUE 0.
01  I       PIC 9(4)  COMP.
01  VALOR   PIC S9(9) COMP-3.
01  MAXIMO  PIC S9(9) COMP-3.
01  HAY     PIC X VALUE "N".
01  ED-M    PIC -(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE SPACES TO TOKEN

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        IF LINEA(I:1) = SPACE
            PERFORM CERRAR
        ELSE
            ADD 1 TO TLEN
            MOVE LINEA(I:1) TO TOKEN(TLEN:1)
        END-IF
    END-PERFORM
    PERFORM CERRAR

    MOVE MAXIMO TO ED-M
    DISPLAY "max=" FUNCTION TRIM(ED-M)
    STOP RUN.

CERRAR.
    IF TLEN > 0
        COMPUTE VALOR = FUNCTION NUMVAL(TOKEN)
        IF HAY = "N" OR VALOR > MAXIMO
            MOVE VALOR TO MAXIMO
            MOVE "S" TO HAY
        END-IF
        MOVE SPACES TO TOKEN
        MOVE 0 TO TLEN
    END-IF.
""", """
**Lo que esta clase enseña en COBOL.** Aquí está el dato que abre esta clase, y es de los mejores de
toda la sección: **el término "corrutina" lo acuñó Melvin Conway en 1958, en un artículo sobre el
diseño de un compilador de COBOL**.

*Design of a Separable Transition-Diagram Compiler* (Conway, 1963) describía un compilador organizado
en **fases que se pasaban el control mutuamente**, sin que ninguna fuera la principal: el analizador
léxico produce un símbolo y **cede el control**; el sintáctico lo consume y **cede de vuelta**.

Ese es exactamente el patrón productor-consumidor que hoy se escribe con generadores, y Conway lo
describió **para un compilador de COBOL, en 1958**.

Y el mismo Conway es el autor de la observación que hoy se llama **ley de Conway** —las organizaciones
diseñan sistemas que copian su estructura de comunicación—, formulada en el mismo contexto.

En el COBOL del lenguaje, lo más cercano a una corrutina son las construcciones de la clase 107:

```cobol
SORT FICHERO
    INPUT PROCEDURE IS FILTRAR
    OUTPUT PROCEDURE IS PROCESAR
```

**`INPUT PROCEDURE` y `OUTPUT PROCEDURE` son corrutinas de verdad**: el `SORT` llama a `FILTRAR` para
pedir el registro siguiente, `FILTRAR` hace `RELEASE` de uno y **devuelve el control**; después el
`SORT` llama a `PROCESAR`, que hace `RETURN` de los ordenados.

```cobol
FILTRAR SECTION.
    PERFORM UNTIL FIN
        READ ENTRADA AT END SET FIN TO TRUE
        NOT AT END RELEASE REG-ORDENAR FROM REG-ENTRADA
        END-READ
    END-PERFORM.
```

**`RELEASE` produce y `RETURN` consume**, y el control va y viene entre el `SORT` y los procedimientos.
Es un canal con el ordenador en medio, en COBOL desde 1968.

Es la corrutina de Conway, en el lenguaje sobre el que la describió.
"""),
        "fortran": ("""
program tareas
   implicit none
   integer :: v(100), n, ios, i

   character(len=400) :: linea

   read(*, '(A)') linea

   n = 0
   do i = 1, 100
      read(linea, *, iostat=ios) v(1:i)
      if (ios /= 0) exit
      n = i
   end do

   write(*, '(A,I0)') 'max=', maxval(v(1:n))
end program tareas
""", """
**Lo que esta clase enseña en Fortran.** **Fortran no tiene corrutinas ni canales**, y su modelo es el
de la clase 133: procesos con mensajes o hilos con memoria compartida.

Lo que sí tiene, y encaja en esta clase, son **los eventos de Fortran 2018**:

```fortran
use iso_fortran_env
type(event_type) :: listo[*]

if (this_image() == 1) then
   ! producir datos
   event post (listo[2])            ! avisar a la imagen 2
else if (this_image() == 2) then
   event wait (listo)                ! esperar el aviso
   ! consumir
end if
```

**`event post` y `event wait` son señalización entre imágenes**, y con ellos se construye un canal de
capacidad uno: el productor avisa, el consumidor espera.

Y Fortran 2018 añadió además los **equipos** y la sincronización parcial, que son las piezas para
tuberías distribuidas:

```fortran
sync images ([2, 3])              ! sincronizar solo con esas imágenes
form team (color, mi_equipo)       ! dividir las imágenes en subgrupos
change team (mi_equipo)
   ...                              ! aquí num_images() es el del EQUIPO
end team
```

**Los equipos permiten dividir un cálculo en fases con topologías distintas** —unos procesos hacen la
física, otros la entrada/salida—, que es la arquitectura de tuberías de esta clase a escala de
superordenador.

Y merece decir con claridad lo que Fortran no tiene y por qué no le hace falta: **`async`/`await` y las
corrutinas sirven para no bloquear un hilo mientras se espera entrada/salida** (clase 122), y **un
programa Fortran no espera: calcula**.

Su problema no es la latencia, es el rendimiento agregado, y para eso la respuesta es el paralelismo de
datos, no la concurrencia.

Es un buen recordatorio de que **una característica ausente no siempre es una carencia**: a veces es
que el problema que resuelve no aparece en ese dominio.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Tareas is
   Linea  : String (1 .. 400);
   Ultimo : Natural;
   Pos    : Integer := 1;
   Valor  : Integer;
   Fin    : Positive;
   Maximo : Integer := Integer'First;
begin
   Get_Line (Linea, Ultimo);

   loop
      while Pos <= Ultimo and then Linea (Pos) = ' ' loop
         Pos := Pos + 1;
      end loop;
      exit when Pos > Ultimo;

      Get (Linea (Pos .. Ultimo), Valor, Fin);
      if Valor > Maximo then
         Maximo := Valor;
      end if;
      Pos := Fin + 1;
   end loop;

   Put ("max=");
   Put (Maximo, Width => 1);
   New_Line;
end Tareas;
""", """
**Lo que esta clase enseña en Ada.** **La cita de Ada es un canal síncrono**, y esa equivalencia merece
explicarse porque es exacta.

```ada
task Productor is
   entry Dar (X : out Integer);
end Productor;

--  El consumidor llama:
Productor.Dar (Valor);        --  se BLOQUEA hasta que el productor haga accept
```

En Go se escribiría así:

```go
valor := <-canal        // se bloquea hasta que alguien envíe
```

**Son la misma operación.** Un canal sin búfer en Go es un encuentro: emisor y receptor se esperan
mutuamente. La cita de Ada es exactamente eso, con la diferencia de que **el "canal" tiene nombre y
pertenece a una tarea**.

Y Ada llega más lejos en dos aspectos:

**Primero, `select` con guardas** (clase 119), que es el `select` de Go **con condiciones**:

```ada
select
   when Cola_No_Llena =>
      accept Poner (X : Integer) do ... end Poner;
or
   when Cola_No_Vacia =>
      accept Sacar (X : out Integer) do ... end Sacar;
or
   delay 5.0;
   Put_Line ("inactivo");
end select;
```

**`when` delante de cada alternativa** hace que una rama solo esté disponible si la condición se
cumple. En Go hay que simular eso poniendo un canal a `nil`, que es un idioma conocido y menos claro.

**Y segundo, las colas con contrapresión y prioridad** (clase 120), que Go no tiene en el lenguaje.

Y desde Ada 2022 hay además **corrutinas por biblioteca** y **paralelismo estructurado**:

```ada
parallel do
   Tarea_A;
and
   Tarea_B;
end do;
```

**`parallel ... and ... end` de Ada 2022 lanza bloques en paralelo y espera a todos**, con la
sintaxis del propio lenguaje. Es concurrencia estructurada (clase 121) con soporte sintáctico, y muy
pocos lenguajes la tienen así.

Es el mismo camino que Ada lleva recorriendo desde 1983: **poner en la gramática lo que otros dejan a
la biblioteca**.
"""),
        "pascal": ("""
program Tareas;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, Tok: string;
  I, Valor, Maximo: Integer;
  C: Char;
  Hay: Boolean;

begin
  ReadLn(Linea);

  Hay := False;
  Maximo := 0;
  Tok := '';

  for I := 1 to Length(Linea) + 1 do
  begin
    if I <= Length(Linea) then C := Linea[I] else C := ' ';
    if C = ' ' then
    begin
      if Tok <> '' then
      begin
        Valor := StrToInt(Tok);
        if (not Hay) or (Valor > Maximo) then
        begin
          Maximo := Valor;
          Hay := True;
        end;
        Tok := '';
      end;
    end
    else
      Tok := Tok + C;
  end;

  WriteLn('max=', IntToStr(Maximo));
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal **no tiene corrutinas** en el lenguaje, y su historia
contiene una de las mejores implementaciones de la idea: **los `iterator` de Turbo Pascal para
Windows**... que en realidad no existieron.

Lo que sí existió, y es relevante, son **las corrutinas de Modula-2**, el lenguaje siguiente de Wirth:

```text
NEWPROCESS(P, espacio, tamaño, corrutina);
TRANSFER(actual, siguiente);        (* ceder el control explícitamente *)
```

**`TRANSFER` cambia de corrutina guardando el contexto actual**, y era la primitiva sobre la que
Modula-2 construía su concurrencia. Wirth la eligió deliberadamente en lugar de hilos: **una primitiva
mínima sobre la que construir lo demás**.

Es exactamente el modelo de las corrutinas simétricas, y precede a las de Lua y a las de Tcl en
décadas.

En Object Pascal, lo que hay son las capas de la clase 122 —tareas, futuros, `Synchronize`— y **las
funciones anónimas** que permiten escribir el patrón productor-consumidor:

```pascal
Cola := TThreadedQueue<Integer>.Create(100, INFINITE, INFINITE);
TTask.Run(procedure begin
  for var I := 1 to 100 do Cola.PushItem(I);      { productor }
end);
while Cola.PopItem(Valor) = wrSignaled do ...      { consumidor }
```

**`TThreadedQueue<T>` es un canal con capacidad**: `PushItem` bloquea si está llena y `PopItem` si está
vacía. Es contrapresión (clase 120), con la misma forma que las colas sincronizadas de Ada.

Y Free Pascal tiene además algo que se le acerca desde otro lado: **los generadores implementados con
hilos**, y la extensión experimental de corrutinas en algunas ramas.

Merece cerrar señalando la conexión que esta clase revela: **Wirth eligió corrutinas y transferencia
explícita; Hoare y Ada eligieron el encuentro; Hansen eligió el monitor** (clase 121). Los tres
trabajaban a la vez, en los setenta, sobre el mismo problema — y las tres ideas siguen vivas.
"""),
        "lisp": ("""
(let ((maximo nil))
  (loop for x = (read *standard-input* nil nil)
        while x
        do (when (or (null maximo) (> x maximo))
             (setf maximo x)))
  (format t "max=~D~%" maximo))
""", """
**Lo que esta clase enseña en Common Lisp.** **Common Lisp no tiene corrutinas en el estándar**, y tiene
la primitiva de la que se derivan todas: **las continuaciones** — aunque no en el estándar, sino en
Scheme.

`call/cc` de Scheme captura **el resto del cálculo como un valor**, y con eso se implementan corrutinas,
generadores, retroceso (clase 118) y `async`/`await`. Es la primitiva más general de control que
existe.

Common Lisp no la tiene —el comité la consideró demasiado costosa de implementar con eficiencia— y el
ecosistema lo resuelve por otras vías:

```lisp
(ql:quickload :cl-cont)              ; continuaciones por transformación de código
(cl-cont:with-call/cc ...)

(ql:quickload :snakes)                ; generadores al estilo Python
(defgenerator contar (n)
  (loop for i from 1 to n do (yield i)))

(ql:quickload :bordeaux-threads)       ; y los hilos, para lo demás
```

**`cl-cont`** merece la explicación porque es un ejemplo excelente de lo que las macros permiten:
**transforma el código a estilo de paso de continuaciones en tiempo de compilación**, con lo que
`call/cc` funciona dentro de su ámbito.

Eso es lo que hace un compilador con `async`/`await` (clase 122) —transformar la función en una máquina
de estados— **escrito como biblioteca**.

Y Lisp tiene una construcción del estándar que da el efecto de un generador en muchos casos, y que ya
apareció en la clase 120: **las macros `with-` con un bloque**.

```lisp
(do-lineas (linea "fichero.txt")     ; una macro propia
  (procesar linea))
```

**El "generador" es una macro que recorre y llama al cuerpo**, que es iteración interna (clase 097) — la
misma solución que Smalltalk con `do:`.

Es la diferencia de fondo de esta clase: **un generador da el control al consumidor; la iteración
interna lo deja en el productor**. Y para la mayoría de los casos, la segunda basta y es más simple.

Cuando no basta —recorrer dos secuencias a la vez, entrelazar— hace falta la corrutina, y ahí Lisp
recurre a las bibliotecas.
"""),
        "tcl": ("""
proc maximizar {} {
    set m ""
    while 1 {
        set x [yield]
        if {$x eq ""} { return $m }
        if {$m eq "" || $x > $m} { set m $x }
    }
}

gets stdin linea

coroutine acum maximizar             ;# se ejecuta hasta el primer yield
foreach x [split [string trim $linea]] {
    acum $x                           ;# ENVIAR un valor a la corrutina
}

puts "max=[acum {}]"
""", """
**Lo que esta clase enseña en Tcl.** Este programa usa **una corrutina como consumidor**: `yield`
devuelve el control **y el valor que se le envíe al reanudarla**.

```tcl
set x [yield]         ;# suspende, y al reanudar recibe el argumento
acum $x                ;# reanudar, pasando un valor
```

**Eso es un canal**: la corrutina espera datos, el llamante los envía. Y es exactamente la equivalencia
del cierre de esta clase — **una corrutina que recibe por `yield` es el extremo receptor de un canal
de capacidad cero**.

Las corrutinas de Tcl 8.6 tienen tres propiedades que las hacen de las mejores de esta página:

**Primera: no colorean funciones** (clase 122). Cualquier procedimiento llamado desde una corrutina
puede hacer `yield`, sin declarar nada.

**Segunda: `yieldto` permite ceder a otra corrutina directamente**, sin pasar por el llamante:

```tcl
yieldto otraCorrutina $datos      ;# corrutinas SIMÉTRICAS
```

Eso son las corrutinas simétricas —el `TRANSFER` de Modula-2 de esta misma clase— y muy pocos lenguajes
las ofrecen: Python y JavaScript solo tienen las asimétricas, donde `yield` siempre vuelve al llamante.

**Y tercera: se integran con el bucle de eventos** (clase 119), que es lo que las hace útiles para
entrada/salida:

```tcl
yieldto fileevent $canal readable [info coroutine]
```

Y todo eso fue posible por el cambio de implementación de la clase 127: **NRE**, que sacó la pila del
intérprete de la pila de C.

Y Tcl 8.7 añade lo que faltaba para depurarlas:

```tcl
coroprobe $nombre { info level }     ;# ejecutar código DENTRO de una corrutina suspendida
coroinject $nombre { ... }            ;# inyectarle código
```

**Inspeccionar una corrutina suspendida** es un problema conocido en todos los entornos asíncronos, y
Tcl lo resolvió con dos comandos.
"""),
        "perl": ("""
use strict;
use warnings;
use List::Util qw(max);

my $linea = <STDIN>;
chomp $linea;
my @v = split ' ', $linea;

print "max=", max(@v), "\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl **no tiene corrutinas ni canales en el núcleo**, y el
ecosistema los ha construido de tres formas distintas, que ilustran bien las opciones de esta clase.

**Primera: con hilos y colas** —el modelo directo—:

```perl
use threads;
use Thread::Queue;
my $cola = Thread::Queue->new;
threads->create(sub { while (defined(my $x = $cola->dequeue)) { ... } });
$cola->enqueue(1, 2, 3);
$cola->end;
```

**`Thread::Queue` es un canal con bloqueo**, con la advertencia de la clase 121: los hilos de Perl son
caros.

**Segunda: con clausuras, que dan generadores sin corrutinas**:

```perl
sub contador {
    my $n = 0;
    return sub { return $n++ };       # cada llamada avanza el estado
}
my $g = contador();
$g->(); $g->();                        # 0, 1
```

**Una clausura con estado es un generador limitado**: puede producir valores, y **no puede suspenderse
en medio de un bucle**. Para lo segundo hace falta una corrutina de verdad.

**Y tercera: `Coro`**, una biblioteca de CPAN que implementa corrutinas reales manipulando la pila de C:

```perl
use Coro;
use Coro::Channel;
my $canal = Coro::Channel->new(4);      # canal con CAPACIDAD
async { $canal->put($_) for 1 .. 10 };
async { while (defined(my $x = $canal->get)) { ... } };
cede;
```

**`Coro::Channel` con capacidad es exactamente un canal de Go**, con contrapresión (clase 120), y
`async` crea una corrutina.

`Coro` es una obra de ingeniería notable —cambia pilas de C a mano— y por eso es frágil entre versiones
de Perl, lo que ilustra el problema de fondo: **añadir corrutinas a un intérprete que no las previó
exige tocar su núcleo**.

Es exactamente lo que Tcl tuvo que hacer con NRE (clase 127), y lo que Perl no ha hecho en el núcleo.
Por eso hoy el camino recomendado es `IO::Async` con futuros y `Future::AsyncAwait` (clase 122), que
transforman el código en lugar de manipular la pila.
"""),
        "cpp": ("""
#include <algorithm>
#include <iostream>
#include <iterator>
#include <vector>

int main() {
    const std::vector<int> v{std::istream_iterator<int>(std::cin),
                             std::istream_iterator<int>()};
    if (v.empty()) return 1;

    std::cout << "max=" << *std::max_element(v.begin(), v.end()) << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** **C++20 añadió corrutinas**, y su diseño es el más peculiar de esta
página: **el lenguaje aporta la transformación y no aporta los tipos** (clase 122).

```cpp
generator<int> contar(int n) {
    for (int i = 0; i < n; ++i)
        co_yield i;              // suspende y produce un valor
}
```

Tres palabras clave —`co_await`, `co_yield`, `co_return`— y **el compilador transforma la función en
una máquina de estados** con su marco guardado.

Y ahí está la propiedad que hace especiales a las corrutinas de C++: **la elisión del marco**.

Si el compilador puede demostrar que el marco de la corrutina no sobrevive al llamante, **puede
colocarlo en la pila y evitar la reserva de memoria**. En el mejor caso, **una corrutina cuesta lo
mismo que un bucle escrito a mano**.

Es la promesa de C++ de siempre —abstracción sin coste— aplicada a la concurrencia.

El precio es la complejidad: **para usar `co_yield` hace falta un tipo `generator` con su
`promise_type`**, y escribirlo a mano es notoriamente difícil. C++23 añadió por fin
`std::generator`, y para el resto están cppcoro, Boost.Asio y libunifex.

Y sobre canales, C++ **no tiene ninguno en el estándar**, lo cual sorprende. La construcción se hace a
mano:

```cpp
std::queue<T> cola;
std::mutex m;
std::condition_variable cv;      // el trío clásico
```

O con bibliotecas: `boost::fibers::buffered_channel`, las colas concurrentes de TBB, `moodycamel`.

**La propuesta de ejecutores —`std::execution`, prevista para C++26—** traerá por fin el modelo
completo: planificadores, remitentes y receptores, con los que se componen operaciones asíncronas de
forma tipada.

Es un buen ejemplo de cómo evoluciona C++: **primero el mecanismo de coste cero, y las políticas
después**.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi TAREAS;
  entrada char(200) const;
end-pi;

dcl-s texto  varchar(200);
dcl-s tok    varchar(20) inz('');
dcl-s c      char(1);
dcl-s i      int(10);
dcl-s valor  int(10);
dcl-s maximo int(10);
dcl-s hay    ind inz(*off);

texto = %trimr(entrada);

for i = 1 to %len(texto) + 1;
  if i <= %len(texto);
    c = %subst(texto : i : 1);
  else;
    c = ' ';
  endif;
  if c = ' ';
    if tok <> '';
      valor = %int(tok);
      if not hay or valor > maximo;
        maximo = valor;
        hay = *on;
      endif;
      tok = '';
    endif;
  else;
    tok += c;
  endif;
endfor;

dsply ('max=' + %char(maximo));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG no tiene corrutinas, y **la plataforma tiene el canal**: las
colas de datos de las clases 096, 119 y 122.

```text
Trabajo A → [cola de datos] → Trabajo B
```

Y merece comparar esa cola con un canal de Go, porque las diferencias son instructivas:

| | Canal de Go | Cola de datos de IBM i |
|---|---|---|
| Ámbito | dentro de un proceso | **entre trabajos, y entre máquinas** |
| Persistencia | no | **sí, opcional** |
| Sobrevive a un fallo | no | **sí** |
| Disciplina | FIFO | **FIFO, LIFO o por CLAVE** |
| Coste por operación | nanosegundos | microsegundos |
| Contrapresión | por capacidad | por tamaño máximo |

**La cola de datos es un canal persistente y distribuido**, tres órdenes de magnitud más cara y con
garantías que un canal en memoria no puede dar.

Y la disciplina **por clave** es la que no tiene equivalente: permite que varios consumidores esperen
en la misma cola y **cada uno reciba solo los mensajes con su clave** — que es lo que hace falta para
el patrón petición-respuesta de la clase 122.

Y RPG tiene además la construcción que se acerca a un generador, aunque no se llame así: **el ciclo de
lectura de un fichero**.

```rpgle
setll (*loval) MOVIMIENTOS;
dow *on;
  reade MOVIMIENTOS;
  if %eof(MOVIMIENTOS);
    leave;
  endif;
  // procesar
enddo;
```

**`reade` produce el registro siguiente sin cargar el fichero**, manteniendo la posición en el índice —
que es exactamente lo que hace un generador: **estado suspendido entre invocaciones**.

Es la conclusión que esta parte del curso repite: **los conceptos de esta clase existen en las
plataformas de gestión con otros nombres y a otra escala**.
"""),
        "pli": ("""
 tareas: procedure options(main);

    declare linea char(200) varying;
    declare tok   char(20)  varying initial('');
    declare c     char(1);
    declare (i, valor, maximo) fixed binary(31);
    declare hay bit(1) initial('0'b);

    get edit (linea) (a(200));
    linea = trim(linea);

    do i = 1 to length(linea) + 1;
       if i <= length(linea) then c = substr(linea, i, 1); else c = ' ';
       if c = ' ' then do;
          if tok ^= '' then do;
             valor = tok;
             if ^hay | valor > maximo then do;
                maximo = valor;
                hay = '1'b;
             end;
             tok = '';
          end;
       end;
       else tok = tok || c;
    end;

    put skip list ('max=' || trim(char(maximo)));

 end tareas;
""", """
**Lo que esta clase enseña en PL/I.** PL/I no tiene corrutinas ni canales, y tiene las piezas de la
clase 119 con las que se construye el patrón:

```pli
 declare listo(4) event;
 call productor(datos) task(t1) event(listo(1));
 call consumidor(datos) task(t2) event(listo(2));
 wait(listo);
```

Y una construcción que se acerca a un canal más de lo que parece: **la multitarea con `event` como
señal de disponibilidad**.

Con un búfer compartido, un evento de "hay datos" y otro de "hay hueco", **se construye un canal con
contrapresión** — que es exactamente cómo se implementa un canal por debajo en cualquier runtime.

Lo interesante de esta clase en PL/I es otra cosa, y conecta con COBOL de esta misma página: **PL/I y
COBOL son los dos lenguajes sobre los que se describieron las corrutinas**.

Conway describió el concepto en 1958 para un compilador de COBOL, y el mismo patrón se usó en los
compiladores de PL/I: **fases que se pasan el control produciendo y consumiendo símbolos**.

Y hay un uso de corrutinas en el mundo del mainframe que sigue vivo y que casi nadie llama así: **las
salidas de usuario de las utilidades de ordenación**.

```text
DFSORT con EXIT E15 (entrada) y E35 (salida)
```

**El programa de salida E15 se llama para cada registro de entrada**, decide si lo pasa, lo modifica o
lo descarta, y devuelve el control. **E35 hace lo mismo con la salida.**

Es la misma estructura que el `SORT` de COBOL de esta página, y es exactamente el patrón de Conway: **el
control va y viene entre la utilidad y el código del usuario**, sin que ninguno sea el programa
principal.

Y ese patrón —**el marco de trabajo llama a tu código, no al revés**— es la inversión de control de la
clase 119, y estaba en las utilidades de ordenación de los años sesenta.
"""),
        "mumps": ("""
TAREAS ; Tareas, corrutinas y canales -- clase 134
 read linea
 set maximo = ""
 for i=1:1:$length(linea, " ") do
 . set x = $piece(linea, " ", i)
 . if maximo = "" set maximo = x quit
 . if x > maximo set maximo = x
 write "max=", maximo, !
 quit
""", """
**Lo que esta clase enseña en M.** M **no tiene corrutinas ni canales**, y tiene la construcción que en
la práctica hace de generador y que ya ha aparecido en varias clases: **`$order`**.

```mumps
 set id = ""
 for  set id = $order(^PACIENTE(id))  quit:id=""  do procesar(id)
```

**`$order` devuelve el subíndice siguiente y mantiene la posición implícita en el argumento**, así que
el bucle recorre diez millones de registros **sin cargar nada y sin cursor** (clase 120).

Eso es un generador: **estado suspendido entre invocaciones, un elemento cada vez, memoria constante**.
Y funciona igual sobre memoria y sobre disco.

Y para el canal, M usa lo de la clase 120: **un *global* como cola**.

```mumps
 ; productor
 set ^COLA($increment(^COLA)) = mensaje

 ; consumidor
 for  set n = $order(^COLA(""))  quit:n=""  do
 . set msg = ^COLA(n)
 . kill ^COLA(n)
 . do procesar(msg)
```

**`$increment` es atómico**, así que varios productores no colisionan, y el *global* es persistente y
transaccional.

Comparado con un canal de Go, tiene las mismas diferencias que las colas de IBM i de esta página:
**mucho más caro y con garantías que un canal en memoria no puede dar** — sobrevive a la caída del
consumidor, se puede inspeccionar desde otro proceso y participa en transacciones.

Y para la espera, M tiene `lock` con tiempo límite (clase 121) y `hang`:

```mumps
 for  quit:$data(^COLA)  hang 0.1        ; sondeo
 lock +^COLA:5                            ; o esperar el bloqueo
```

**El sondeo es la forma tradicional**, y es una carencia real: **M no tiene una primitiva de espera
sobre un *global***. Las implementaciones modernas la añaden —eventos en IRIS, y en YottaDB se usan
mecanismos del sistema— pero el lenguaje base obliga a sondear.

Es de las pocas cosas de esta parte donde M queda claramente por detrás, y merece decirlo.
"""),
        "smalltalk": ("""
| v |

v := stdin nextLine substrings collect: [ :cada | cada asNumber ].

Transcript show: 'max=', (v inject: v first into: [ :a :b | a max: b ]) printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk **puede implementar corrutinas dentro del propio
lenguaje**, y esa capacidad viene de lo que la clase 127 explicaba: **el contexto de pila es un
objeto**.

```smalltalk
| ctx |
ctx := thisContext.               "el marco actual, como objeto"
ctx suspend.                       "guardarlo"
ctx resume: valor.                  "y reanudarlo después"
```

**Guardar un contexto y reanudarlo es exactamente una corrutina**, y en Smalltalk no hace falta soporte
del compilador ni palabras clave: **es manipulación de objetos**.

Sobre eso, Pharo implementa generadores en una clase de biblioteca:

```smalltalk
| g |
g := Generator on: [ :salida |
        1 to: 10 do: [ :i | salida yield: i ] ].
g next.                            "1"
g next.                             "2"
g do: [ :cada | ... ].
```

**`Generator` está escrito en Smalltalk**, usando `Process` y semáforos por debajo, y es un buen
ejemplo del argumento de la clase 107: **lo que en otros lenguajes es sintaxis, aquí es una clase**.

Y para los canales, la biblioteca tiene `SharedQueue` (clases 120 y 121):

```smalltalk
| cola |
cola := SharedQueue new.
[ 1 to: 100 do: [ :i | cola nextPut: i ] ] fork.
[ [ true ] whileTrue: [ procesar: cola next ] ] fork.
```

**`cola next` bloquea si está vacía**, que es la mitad de un canal; con `SharedQueue2` y capacidad
limitada se obtiene la contrapresión.

Y merece cerrar esta clase con la observación que la recorre entera, y que Smalltalk ilustra mejor que
nadie: **corrutina, canal, generador, continuación y excepción reanudable son todos la misma
capacidad** —guardar y reanudar un estado de ejecución— **vista desde ángulos distintos**.

En Smalltalk, las cinco se construyen sobre la misma pieza: **el contexto como objeto**. Y por eso el
depurador puede reanudar desde un marco (clase 127), las excepciones pueden `resume:` (clase 116) y los
generadores son una clase de biblioteca.

**Una primitiva, cinco características.** Es el mejor argumento a favor de exponer el mecanismo en
lugar de las políticas.
"""),
    },
)
