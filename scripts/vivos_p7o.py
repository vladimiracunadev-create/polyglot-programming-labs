# -*- coding: utf-8 -*-
"""Parte 7, lote O — clase 121. Ver `vivos_parte7.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 121 — Concurrente: hilos, tareas y canales
# ---------------------------------------------------------------------------
SPECS["121"] = dict(
    gancho="""
Sumar en paralelo. Aquí hay un hecho que ordena la página entera: **Ada tenía tareas, citas, colas de
entrada y objetos protegidos EN EL LENGUAJE en 1983**, cuando C no tenía hilos, C++ no existía y
Fortran no tenía ni `while`. Y **PL/I tenía multitarea con eventos en 1964**. La concurrencia no llegó
con los procesadores multinúcleo: **llegó con los sistemas de control y las transacciones**.
""",
    porque="""
Aquí el concepto es la **ejecución simultánea con estado compartido**, y estos lenguajes lo enseñan
porque tienen las tres respuestas históricas y las tres siguen vivas. **En el lenguaje, con
comprobación**: Ada, con tareas y objetos protegidos que garantizan exclusión mutua sin escribir un
`lock`. **En la biblioteca, con primitivas**: C++ con `std::thread` y `std::mutex`, donde una condición
de carrera es comportamiento indefinido y nadie te avisa. **Y en la plataforma**: COBOL bajo CICS y
RPG con sus trabajos, donde **el paralelismo lo da el sistema ejecutando muchas copias del programa**.

Esa tercera es la que más código mueve hoy, y casi nunca aparece en las discusiones sobre
concurrencia.
""",
    cierre="""
Lo transferible: **el problema de la concurrencia no es ejecutar a la vez, es compartir**. Si dos
hilos no comparten nada, no hay problema; si comparten, hace falta disciplina, y las opciones son
pocas: **no compartir** —procesos, actores, mensajes—, **compartir con exclusión** —cerrojos, objetos
protegidos, transacciones— o **compartir solo datos inmutables** (clase 114). Todo lo demás son
detalles. Cuando elijas, la pregunta útil no es qué primitiva usar, sino **qué se comparte y quién
puede tocarlo**.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. CONCUR.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(2)  COMP VALUE 0.
01  I       PIC 9(4)  COMP.
01  SUMA    PIC S9(18) COMP-3 VALUE 0.
01  ED-S    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE SPACES TO TOKEN

    *> COBOL no tiene hilos: el paralelismo lo da el sistema
    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        IF LINEA(I:1) = SPACE
            PERFORM ACUMULAR
        ELSE
            ADD 1 TO TLEN
            MOVE LINEA(I:1) TO TOKEN(TLEN:1)
        END-IF
    END-PERFORM
    PERFORM ACUMULAR

    MOVE SUMA TO ED-S
    DISPLAY "suma=" FUNCTION TRIM(ED-S)
    STOP RUN.

ACUMULAR.
    IF TLEN > 0
        COMPUTE SUMA = SUMA + FUNCTION NUMVAL(TOKEN)
        MOVE SPACES TO TOKEN
        MOVE 0 TO TLEN
    END-IF.
""", """
**Lo que esta clase enseña en COBOL.** **COBOL no tiene hilos**, y los sistemas escritos en COBOL están
entre los más concurrentes que existen: un CICS grande atiende **decenas de miles de transacciones por
segundo**.

La explicación es la del gancho de esta clase: **la concurrencia está en la plataforma, no en el
lenguaje**.

```text
10.000 terminales → CICS → N copias del mismo programa COBOL, a la vez
```

Y ahí está la decisión de diseño que lo hace funcionar: **cada transacción es independiente y no
comparte estado con las demás**. El programa se arranca, procesa un mensaje y termina (clase 119). No
hay variables globales entre transacciones, así que **no hay condiciones de carrera que evitar**.

Es exactamente la estrategia de "no compartir" del cierre de esta clase, aplicada a escala industrial
y cuarenta años antes de que los actores se pusieran de moda.

Lo que sí se comparte son **los datos**, y ahí la disciplina la impone el gestor de recursos:

```cobol
EXEC CICS READ FILE('CLIENTES') RIDFLD(ID) UPDATE END-EXEC
*> el registro queda BLOQUEADO hasta el SYNCPOINT
EXEC CICS REWRITE FILE('CLIENTES') END-EXEC
EXEC CICS SYNCPOINT END-EXEC
*> aquí se confirma y se sueltan los bloqueos
```

**`UPDATE` bloquea el registro; `SYNCPOINT` confirma la transacción y libera todo.** Si el programa
falla, CICS **deshace los cambios y suelta los bloqueos** automáticamente.

Eso es exclusión mutua con recuperación, gestionada por el monitor, y es más robusto que cualquier
`mutex`: **un hilo que muere con un `mutex` tomado deja el sistema colgado; una transacción que muere
se deshace sola**.

Y hay una capacidad más, propia del mainframe: **el paralelismo de trabajos por lotes**.

```text
//PASO1 EXEC PGM=PROC,PARM='PARTICION=1'
//PASO2 EXEC PGM=PROC,PARM='PARTICION=2'
```

Partir un fichero en N trozos y lanzar N trabajos que procesan cada uno el suyo. Es MapReduce escrito
en JCL, y es cómo se procesan los cierres nocturnos desde los años setenta.
"""),
        "fortran": ("""
program concur
   implicit none
   integer, allocatable :: v(:)
   integer :: n, ios, i, suma

   character(len=400) :: linea

   read(*, '(A)') linea

   n = 0
   do i = 1, 100
      if (allocated(v)) deallocate(v)
      allocate(v(i))
      read(linea, *, iostat=ios) v
      if (ios /= 0) exit
      n = i
   end do
   if (allocated(v)) deallocate(v)
   allocate(v(n))
   read(linea, *) v

   !  sum() es una reducción: el compilador puede paralelizarla
   suma = sum(v)

   write(*, '(A,I0)') 'suma=', suma
end program concur
""", """
**Lo que esta clase enseña en Fortran.** Fortran es **el lenguaje de esta página con más capacidad de
paralelismo real**, y lo tiene en tres niveles distintos.

**El primero, implícito**: `sum(v)` es una reducción, y el compilador puede repartirla entre unidades
vectoriales o núcleos. Es lo que la clase 114 explicaba: **declarar en lugar de ordenar da libertad al
compilador**.

**El segundo, `do concurrent`** (Fortran 2008), la promesa explícita de independencia:

```fortran
do concurrent (i = 1:n)
   w(i) = f(v(i))
end do

do concurrent (i = 1:n) reduce(+:suma)     ! Fortran 2023: reducciones
   suma = suma + v(i)
end do
```

**El programador promete que las iteraciones son independientes**, y el compilador reparte. Con
`nvfortran -stdpar=gpu`, ese bucle **se ejecuta en una tarjeta gráfica sin escribir CUDA** — y ese es
hoy uno de los argumentos más fuertes de Fortran frente a C++ en computación científica.

**El tercero, los coarrays** (Fortran 2008), que son el modelo de memoria distribuida:

```fortran
real :: parcial[*]                       ! una copia por IMAGEN
parcial = sum(v(inicio:fin))              ! cada imagen suma su trozo
sync all
if (this_image() == 1) then
   total = sum([(parcial[i], i = 1, num_images())])
end if
```

**`this_image()`** dice qué proceso soy, **`num_images()`** cuántos hay, y **`parcial[i]`** accede a la
copia de otro proceso **con sintaxis de arreglo**. No hay MPI, no hay biblioteca y no hay envío de
mensajes explícito.

Es el modelo **PGAS** —espacio de direcciones global particionado— y Fortran es el único lenguaje
mayoritario que lo tiene en el estándar. Fortran 2018 añadió además **equipos** —subgrupos de
imágenes— y **detección de imágenes fallidas**, que es tolerancia a fallos para máquinas con cien mil
nodos donde algo se rompe cada pocas horas.

Los códigos que corren en los superordenadores más grandes del mundo —clima, fusión, astrofísica— usan
exactamente esto. **La concurrencia de Fortran no es un añadido: es la razón de que siga siendo el
lenguaje de esos sistemas.**
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Concur is
   Linea  : String (1 .. 400);
   Ultimo : Natural;
   V      : array (1 .. 100) of Integer := (others => 0);
   N      : Natural := 0;
   Pos    : Integer := 1;
   Valor  : Integer;
   Fin    : Positive;

   --  OBJETO PROTEGIDO: exclusión mutua sin escribir un solo cerrojo
   protected Acumulador is
      procedure Anadir (X : Integer);
      function Total return Integer;
   private
      Suma : Integer := 0;
   end Acumulador;

   protected body Acumulador is
      procedure Anadir (X : Integer) is
      begin
         Suma := Suma + X;
      end Anadir;

      function Total return Integer is (Suma);
   end Acumulador;

begin
   Get_Line (Linea, Ultimo);

   loop
      while Pos <= Ultimo and then Linea (Pos) = ' ' loop
         Pos := Pos + 1;
      end loop;
      exit when Pos > Ultimo;
      Get (Linea (Pos .. Ultimo), Valor, Fin);
      N := N + 1;
      V (N) := Valor;
      Pos := Fin + 1;
   end loop;

   declare
      task type Sumador is
         entry Arranca (X : Integer);
      end Sumador;

      task body Sumador is
         Mio : Integer;
      begin
         accept Arranca (X : Integer) do
            Mio := X;
         end Arranca;
         Acumulador.Anadir (Mio);
      end Sumador;

      T : array (1 .. N) of Sumador;      --  N TAREAS de verdad
   begin
      for I in 1 .. N loop
         T (I).Arranca (V (I));
      end loop;
   end;   --  el bloque ESPERA a que todas terminen

   Put ("suma=");
   Put (Acumulador.Total, Width => 1);
   New_Line;
end Concur;
""", """
**Lo que esta clase enseña en Ada.** Este programa lanza **tareas de verdad** y no tiene ni un cerrojo,
y esas dos cosas juntas son la aportación de Ada a esta clase.

**El objeto protegido** es la pieza central:

```ada
protected Acumulador is
   procedure Anadir (X : Integer);      --  acceso EXCLUSIVO de escritura
   function Total return Integer;        --  acceso COMPARTIDO de lectura
private
   Suma : Integer := 0;
end Acumulador;
```

El compilador y el runtime garantizan que **solo un procedimiento se ejecuta a la vez**, y que **varias
funciones pueden leer simultáneamente**. Es un cerrojo de lectura-escritura, generado automáticamente,
**imposible de olvidar y imposible de dejar tomado** — si el cuerpo lanza una excepción, se libera
igual.

Compara con `std::mutex` en C++: hay que declararlo, tomarlo, soltarlo, y nada impide acceder al dato
sin tomarlo.

Y hay una tercera operación que ningún otro lenguaje de esta página tiene en la sintaxis: **la entrada
con barrera**.

```ada
protected Buffer is
   entry Sacar (X : out Integer);       --  ENTRY, no procedure
private
   entry Sacar when Contador > 0;        --  BARRERA: solo si hay datos
end Buffer;
```

**`entry ... when` es una condición de guarda**: quien llame **se bloquea automáticamente hasta que la
condición sea cierta**. Es una variable de condición, sin escribir `wait` ni `signal` y sin el error
clásico de la señal perdida.

Y las otras dos piezas del programa:

- **`T : array (1 .. N) of Sumador`** crea N tareas; **arrancan solas al declararse**.
- **`end;` del bloque espera a que todas terminen.** No hay `join`: **el ámbito es la barrera**.

Ese modelo —**tareas cuyo padre no puede terminar antes que ellas**— es lo que hoy se llama
*concurrencia estructurada*, propuesta en 2018 y adoptada por Kotlin, Swift y Java 21.

**Ada la tiene desde 1983**, y por la misma razón que todo lo demás: en un sistema de control, una
tarea huérfana es un fallo.
"""),
        "pascal": ("""
program Concur;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, Tok: string;
  I, Suma: Integer;
  C: Char;

begin
  ReadLn(Linea);

  Suma := 0;
  Tok := '';

  for I := 1 to Length(Linea) + 1 do
  begin
    if I <= Length(Linea) then C := Linea[I] else C := ' ';
    if C = ' ' then
    begin
      if Tok <> '' then
      begin
        Suma := Suma + StrToInt(Tok);
        Tok := '';
      end;
    end
    else
      Tok := Tok + C;
  end;

  WriteLn('suma=', IntToStr(Suma));
end.
""", """
**Lo que esta clase enseña en Pascal.** El Pascal original **no tenía concurrencia**, y hay una razón
histórica excelente para contarla aquí: **Wirth sí diseñó un lenguaje concurrente, y no fue Pascal**.

**Concurrent Pascal** (Per Brinch Hansen, 1975) y **Modula** (Wirth, 1977) fueron los primeros
lenguajes con concurrencia integrada, y de ahí salió una de las ideas más importantes del área: **el
monitor**.

```text
monitor Buffer;
   var datos: array ...;
   procedure entry Poner(x: Integer);   { EXCLUSIÓN MUTUA automática }
   procedure entry Sacar(var x: Integer);
end;
```

**Un monitor es un objeto con exclusión mutua garantizada**, y es exactamente el objeto protegido de
Ada de esta misma página, la palabra `synchronized` de Java y el `lock` de C#.

La formuló Hoare en 1974 y Brinch Hansen la implementó en Concurrent Pascal, sobre el que se escribió
**Solo**, un sistema operativo completo. Es uno de los pocos casos en que un concepto de concurrencia
nace en un lenguaje y acaba en todos.

Object Pascal moderno tiene hilos por biblioteca:

```pascal
uses Classes, SyncObjs;

TMiHilo = class(TThread)
  procedure Execute; override;
end;

Critica := TCriticalSection.Create;
Critica.Enter; try ... finally Critica.Leave; end;

TInterlocked.Add(Suma, X);        { atómico, sin cerrojo }
```

Y desde Delphi XE7, la biblioteca de programación paralela:

```pascal
TParallel.For(1, N, procedure(I: Integer) begin ... end);
TTask.Run(procedure begin ... end).Wait;
```

Hay una restricción de la plataforma que conviene conocer y que sorprende: **en Free Pascal sobre
Unix, hay que poner `cthreads` como primera unidad del programa** para que el soporte de hilos
funcione. Sin ella, el programa compila y falla en ejecución de formas confusas.

Y otra que define el ecosistema Delphi: **la biblioteca visual (VCL) no es segura para hilos**. Un
hilo que toque un control **debe** hacerlo con `TThread.Synchronize` o `Queue`, que encolan el trabajo
al hilo principal. Es la misma regla de todas las interfaces gráficas —Swing, WPF, Cocoa— y por la
misma razón: **la interfaz es estado compartido**.
"""),
        "lisp": ("""
(let ((suma 0))
  (loop for x = (read *standard-input* nil nil)
        while x
        do (incf suma x))
  (format t "suma=~D~%" suma))
""", """
**Lo que esta clase enseña en Common Lisp.** **El estándar de Common Lisp (1984) no dice nada sobre
concurrencia**, y esa laguna es de época: cuando se estandarizó, los hilos no eran una preocupación de
un lenguaje de propósito general.

Lo que hay es el ecosistema, y está resuelto:

```lisp
(ql:quickload :bordeaux-threads)

(bt:make-thread (lambda () ...) :name "trabajador")
(bt:join-thread hilo)
(bt:with-lock-held (cerrojo) ...)
(bt:condition-wait cv cerrojo)
```

**Bordeaux-Threads** es la capa portable, y por debajo cada implementación tiene lo suyo —SBCL con
hilos nativos, LispWorks, CCL—.

Y hay una peculiaridad de Lisp que esta clase debe explicar, porque es una fuente de sorpresas: **las
variables especiales son por hilo**.

```lisp
(defvar *contexto* nil)          ; especial (clase 082)

(let ((*contexto* 'principal))
  (bt:make-thread (lambda () *contexto*)))   ; ¿qué ve el hilo nuevo?
```

En la mayoría de las implementaciones, **cada hilo tiene su propia pila de enlaces**, así que un hilo
nuevo ve **el valor global**, no el enlazado por su creador. Es coherente con el alcance dinámico
(clase 082) y sorprende a quien espera herencia de contexto.

Esa propiedad tiene un uso excelente: **`*standard-output*` es una variable especial**, así que se
puede redirigir la salida de un hilo sin afectar a los demás.

Y Common Lisp tiene una respuesta al problema del cierre de esta clase que va por el otro camino:
**los actores y el paso de mensajes**.

```lisp
(ql:quickload :lparallel)
(lparallel:pmap 'list #'procesar datos)      ; map PARALELO
(lparallel:future (calcular))                 ; promesa
```

**lparallel** ofrece `pmap`, `preduce`, futuros y colas de tareas, con una API declarativa: **se dice
qué paralelizar, no cómo repartir**.

Y hay una nota histórica que merece la pena: **las máquinas Lisp de los ochenta tenían multitarea con
memoria compartida y recolección de basura concurrente**, cuando eso era ciencia ficción en otras
plataformas. El problema de Lisp con la concurrencia no fue técnico — **fue que el estándar llegó
justo antes de que hiciera falta**.
"""),
        "tcl": ("""
gets stdin linea

set suma 0
foreach x [split [string trim $linea]] {
    incr suma $x
}

puts "suma=$suma"
""", """
**Lo que esta clase enseña en Tcl.** Tcl tiene **el modelo de concurrencia más inusual de esta
página**, y es una decisión de diseño deliberada: **cada hilo tiene su propio intérprete y no comparte
absolutamente nada**.

```tcl
package require Thread

set id [thread::create]
thread::send $id { set x [expr {2 + 2}] } resultado
thread::send -async $id { trabajo_largo }
```

**Un hilo de Tcl es un intérprete completo e independiente.** No hay variables compartidas, no hay
estructuras compartidas y **por tanto no hay condiciones de carrera posibles**. La comunicación es por
mensajes:

```tcl
tsv::set compartido clave valor       ;# variables compartidas EXPLÍCITAS
tpool::create -maxworkers 4            ;# grupo de trabajadores
thread::send $id { ... }                ;# enviar un GUION a otro hilo
```

Es el modelo de **actores** —o el de los *web workers* de JavaScript, o el de los procesos de Erlang—
y es exactamente la primera opción del cierre de esta clase: **no compartir**.

La contrapartida es la que cabe esperar: **pasar datos entre hilos cuesta una copia**, porque hay que
serializar. Para trabajo grueso es irrelevante; para compartir un arreglo enorme, es caro.

Y `tsv` —variables compartidas entre hilos— es la escotilla para cuando hace falta, con acceso
sincronizado por el sistema.

Ahora bien, **el modelo de concurrencia idiomático de Tcl no son los hilos**: es el bucle de eventos de
la clase 119, con un solo hilo y sin bloqueo. Y desde 8.6, las **corrutinas** (clase 122):

```tcl
coroutine trabajador apply {{} {
    while 1 {
        set peticion [yield]
        procesar $peticion
    }
}}
```

Esa combinación —**un hilo con bucle de eventos y corrutinas, y varios intérpretes independientes
cuando hace falta más de un núcleo**— es exactamente la arquitectura que hoy usan Node.js con sus
*worker threads*, Python con `asyncio` y multiproceso, y Erlang con sus planificadores.

**Tcl llegó a ella en 1990 y 1997 respectivamente**, y por la misma razón que los demás: **el estado
compartido con cerrojos es difícil de hacer bien, y evitarlo sale más barato**.
"""),
        "perl": ("""
use strict;
use warnings;
use List::Util qw(sum0);

my $linea = <STDIN>;
chomp $linea;

print "suma=", sum0(split ' ', $linea), "\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl tiene una historia con los hilos que merece contarse porque
es un caso de estudio sobre decisiones irreversibles.

**Perl 5.005 (1998)** introdujo hilos con memoria compartida —los *5.005 threads*— y fueron un
desastre: el intérprete no era seguro para hilos y los fallos eran impredecibles. Se retiraron.

**Perl 5.6 (2000)** los sustituyó por **iThreads**, con un enfoque radicalmente distinto: **cada hilo
tiene su propia copia COMPLETA del intérprete y de todas las variables**.

```perl
use threads;
use threads::shared;

my $total :shared = 0;             # explícitamente compartida
my $t = threads->create(sub { lock($total); $total += 5 });
$t->join;
```

**Todo se copia al crear el hilo, y solo lo marcado con `:shared` se comparte.** Es el modelo de Tcl,
con el mismo razonamiento — y con un coste que en Perl resultó prohibitivo: **crear un hilo copia todo
el programa**, lo que en un proceso con muchos módulos cargados son megabytes.

El resultado es que **la documentación oficial de Perl desaconseja los hilos**, y la comunidad usa
otra cosa:

```perl
my $pid = fork();                          # PROCESOS, no hilos
use Parallel::ForkManager;                  # grupo de procesos
use AnyEvent;  use IO::Async;                # bucle de eventos
```

**`fork` es la respuesta idiomática de Perl a la concurrencia**, y en Unix es barata gracias a la
copia-al-escribir del sistema operativo: el proceso hijo comparte la memoria físicamente hasta que
alguno escribe.

Es la misma conclusión de Tcl por otro camino: **no compartir**. Y en Perl esa decisión la tomó el
sistema operativo, no el lenguaje.

Y hay una lección de diseño que esta clase quiere dejar: **Perl intentó los hilos con memoria
compartida, falló, y el arreglo fue peor que el problema**. Los lenguajes que llegaron después
—Erlang, Go, Rust— tomaron nota, y cada uno resolvió el problema del cierre de esta clase de una forma
distinta: Erlang no compartiendo, Go con canales, y Rust **comprobando en compilación quién puede
tocar qué**.
"""),
        "cpp": ("""
#include <iostream>
#include <iterator>
#include <numeric>
#include <thread>
#include <vector>

int main() {
    const std::vector<int> v{std::istream_iterator<int>(std::cin),
                             std::istream_iterator<int>()};

    //  cada hilo escribe en SU posición: sin carrera, sin cerrojos
    std::vector<int> parciales(v.size(), 0);
    std::vector<std::thread> hilos;
    hilos.reserve(v.size());

    for (std::size_t i = 0; i < v.size(); ++i) {
        hilos.emplace_back([&parciales, &v, i] { parciales[i] = v[i]; });
    }
    for (auto& h : hilos) {
        h.join();
    }

    std::cout << "suma="
              << std::accumulate(parciales.begin(), parciales.end(), 0) << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** Este programa lanza hilos de verdad y **no necesita ningún
cerrojo**, porque cada hilo escribe en una posición distinta. Esa es la primera lección: **la mejor
sincronización es la que no hace falta**.

**C++ no tuvo hilos en el estándar hasta C++11.** Antes eran POSIX threads, Win32 o Boost, y —lo más
importante— **el estándar no definía un modelo de memoria**, así que el comportamiento del código
concurrente dependía del compilador y del hardware.

C++11 trajo las dos cosas a la vez, y la segunda es la que de verdad importaba:

```cpp
std::thread   std::mutex   std::lock_guard   std::scoped_lock
std::condition_variable    std::atomic<T>     std::future / std::async
std::memory_order_relaxed / acquire / release / seq_cst
```

**El modelo de memoria de C++11** define qué puede ver un hilo de lo que escribe otro, y establece la
regla fundamental: **dos accesos concurrentes al mismo dato, siendo uno de escritura y sin
sincronización, son comportamiento indefinido**.

Ese "comportamiento indefinido" es duro y es honesto: **el compilador puede asumir que no ocurre**, y
por eso puede optimizar agresivamente. La contrapartida es que **una condición de carrera no es un
fallo con síntomas: es un programa sin significado**.

Y ahí está la diferencia con Ada de esta misma página: **en Ada el objeto protegido hace imposible
olvidar la exclusión; en C++ nada te obliga a tomar el cerrojo**.

Las herramientas ayudan y son imprescindibles:

```bash
g++ -fsanitize=thread     # ThreadSanitizer: detecta carreras en ejecución
```

C++20 añadió lo que faltaba para la concurrencia estructurada:

```cpp
std::jthread t{...};        // se UNE sola en el destructor, y admite cancelación
std::stop_token             // cancelación cooperativa
std::latch  std::barrier    // sincronización por fases
std::atomic<T>::wait/notify // espera eficiente sin condition_variable
```

**`std::jthread`** corrige el error de diseño de `std::thread`: si un `std::thread` se destruye sin
`join`, **el programa termina abruptamente**. `jthread` se une solo. Es RAII (clase 103) aplicado a
los hilos, y llegó nueve años tarde.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi CONCUR;
  entrada char(200) const;
end-pi;

dcl-s texto varchar(200);
dcl-s tok   varchar(20) inz('');
dcl-s c     char(1);
dcl-s i     int(10);
dcl-s suma  int(20) inz(0);

texto = %trimr(entrada);

for i = 1 to %len(texto) + 1;
  if i <= %len(texto);
    c = %subst(texto : i : 1);
  else;
    c = ' ';
  endif;
  if c = ' ';
    if tok <> '';
      suma += %int(tok);
      tok = '';
    endif;
  else;
    tok += c;
  endif;
endfor;

dsply ('suma=' + %char(suma));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG **no tiene hilos** y la plataforma tiene una arquitectura de
concurrencia completa, con la misma filosofía que COBOL: **el paralelismo es de trabajos, no de
hilos**.

```text
SBMJOB CMD(CALL PGM(PROCESA) PARM('1')) JOB(PARTE1)
SBMJOB CMD(CALL PGM(PROCESA) PARM('2')) JOB(PARTE2)
```

**`SBMJOB`** envía un trabajo a una cola, y **el subsistema decide cuántos ejecutar a la vez** según su
configuración. La concurrencia se administra —cuántos trabajadores, con qué prioridad, con qué
memoria— **sin tocar el programa**.

Y la coordinación entre trabajos usa las piezas ya vistas:

- **Colas de datos** (clases 096 y 119) para repartir trabajo entre varios consumidores.
- **Colas de mensajes** para notificar.
- **Espacios de datos** (`*DTAARA`) como estado compartido, con bloqueo:

```rpgle
in(e) contador;          // LEER y bloquear
contador = contador + 1;
out contador;             // escribir y liberar
```

`in` y `out` sobre un `*DTAARA` **toman y sueltan un bloqueo del sistema**, así que es un contador
compartido entre trabajos con exclusión mutua — y persistente.

Y la exclusión sobre los datos la da la base de datos, como en COBOL:

```rpgle
chain (id) CLIENTES;      // bloquea el registro (clase 104)
update CLIREG;             // escribe y libera
```

**El bloqueo a nivel de registro es automático**, y si el trabajo termina, el sistema lo libera. Es la
misma robustez que se comentó en COBOL: **una transacción que muere se deshace sola**.

Y merece nombrar la capacidad que la plataforma sí da al programador cuando hace falta: **RPG puede
crear hilos** con las APIs `pthread_create` del sistema, y **los procedimientos deben declararse
`THREAD(*CONCURRENT)`** para poder ejecutarse en varios hilos a la vez.

Es posible y está desaconsejado: **el modelo de la plataforma es multitrabajo**, y forzar hilos dentro
de un trabajo suele dar más problemas que ventajas.
"""),
        "pli": ("""
 concur: procedure options(main);

    declare linea char(200) varying;
    declare tok   char(20)  varying initial('');
    declare c     char(1);
    declare (i, suma) fixed binary(31);

    get edit (linea) (a(200));
    linea = trim(linea);
    suma = 0;

    do i = 1 to length(linea) + 1;
       if i <= length(linea) then c = substr(linea, i, 1); else c = ' ';
       if c = ' ' then do;
          if tok ^= '' then do;
             suma = suma + tok;
             tok = '';
          end;
       end;
       else tok = tok || c;
    end;

    put skip list ('suma=' || trim(char(suma)));

 end concur;
""", """
**Lo que esta clase enseña en PL/I.** Aquí está el dato que abre el gancho de esta clase y que sigue
sorprendiendo: **PL/I tenía multitarea en 1964**.

```pli
 declare listo(4) event;
 declare total fixed binary(31);

 do i = 1 to 4;
    call procesar(datos(i), total) task(t(i)) event(listo(i)) priority(5);
 end;

 wait(listo);              /* esperar a las CUATRO */
```

Tres cosas en una sentencia: **`task`** lanza el procedimiento como tarea concurrente, **`event`**
asocia un suceso a su finalización y **`priority`** fija su prioridad relativa.

Y `wait` admite esperar a todos los eventos o **solo a N de ellos** (clase 119), que es `Promise.all` y
`Promise.race`.

Para la exclusión mutua, PL/I ofrece:

```pli
 declare recurso event;
 wait(recurso);
 completion(recurso) = '0'b;      /* "tomar" el semáforo */
 ...
 completion(recurso) = '1'b;       /* soltarlo */
```

**`completion`** es una pseudovariable que lee y escribe el estado de un evento, con lo que un evento
hace de semáforo binario.

Ahora la parte honesta, que esta sección exige: **casi nadie lo usó**. Los compiladores lo
implementaron de forma desigual, la documentación advertía de su coste, y sobre todo **no hacía
falta**: en un mainframe, el paralelismo lo daba el sistema ejecutando muchos trabajos y muchas
transacciones a la vez (clase 119).

Es el mismo patrón que la clase 120 señalaba: **PL/I tenía la característica, la plataforma resolvía
el problema por otra vía, y la característica no arraigó**.

Y merece cerrar con la perspectiva completa: **PL/I (1964), Concurrent Pascal (1975), Modula (1977) y
Ada (1983) tuvieron concurrencia en el lenguaje**, y los lenguajes que dominaron después —C, C++,
Java hasta cierto punto— la dejaron a la biblioteca.

La concurrencia estructurada, los actores y los canales, que hoy se presentan como novedades, **son
redescubrimientos de ideas que estos lenguajes probaron primero**.
"""),
        "mumps": ("""
CONCUR ; Concurrente -- clase 121
 read linea
 set suma = 0
 for i=1:1:$length(linea, " ") set suma = suma + $piece(linea, " ", i)
 write "suma=", suma, !
 quit
""", """
**Lo que esta clase enseña en M.** M **no tiene hilos**, y es **uno de los lenguajes más concurrentes
en producción de esta página**: un sistema VistA grande atiende a miles de usuarios simultáneos sobre
los mismos datos.

La arquitectura es la de COBOL y RPG: **muchos procesos independientes, cada uno con su propio espacio
de variables locales, compartiendo los *globals***.

```mumps
 job procesar^INFORME(id)          ; lanzar un proceso en segundo plano
```

Y toda la concurrencia se resuelve en el acceso a los datos, con dos mecanismos del lenguaje que son
notables por lo integrados que están.

**`lock`**, que es un bloqueo por nombre de estructura:

```mumps
 lock +^PACIENTE(id):10            ; bloquear ESE paciente, esperar 10 s
 if $test do
 . set ^PACIENTE(id, "estado") = "revisado"
 . lock -^PACIENTE(id)              ; liberar
```

**Se bloquea un nodo del árbol, no una tabla ni una fila**, y el bloqueo **cubre implícitamente todo su
subárbol**. Es granularidad arbitraria: se puede bloquear un paciente entero, o solo una de sus
mediciones.

El `:10` es un tiempo de espera y `$test` dice si se consiguió. Es adquisición con límite temporal, en
la sintaxis, desde el estándar de 1977.

**Y las transacciones** (clases 103 y 114):

```mumps
 tstart
 set ^SALDO(a) = ^SALDO(a) - importe
 set ^SALDO(b) = ^SALDO(b) + importe
 tcommit
```

**Atomicidad, aislamiento y recuperación sobre estructuras de datos del lenguaje**, sin SQL y sin capa
de persistencia.

Ese par —bloqueo por nodo y transacciones— es lo que permite que un lenguaje sin hilos, sin tipos y sin
ámbitos sostenga sistemas con miles de usuarios concurrentes. **La concurrencia no está en el
lenguaje: está en el modelo de datos**, que es lo mismo que decir que está donde importa.

Y es la conclusión que esta parte del curso ha ido repitiendo con los cuatro lenguajes de gestión:
**COBOL con CICS, RPG con los trabajos, PL/I con el mainframe y M con los globals resolvieron la
concurrencia sin hilos**, con transacciones y procesos aislados.

Cuarenta años después, esa es exactamente la arquitectura que se recomienda para los sistemas
distribuidos.
"""),
        "smalltalk": ("""
| v suma |

v := stdin nextLine substrings collect: [ :cada | cada asNumber ].

suma := v inject: 0 into: [ :acc :cada | acc + cada ].

Transcript show: 'suma=', suma printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk **tiene concurrencia desde 1980**, y con la
coherencia que le caracteriza: **un proceso es un objeto**.

```smalltalk
p := [ trabajo ] fork.                    "crear un proceso"
p := [ trabajo ] forkAt: Processor userBackgroundPriority.
p suspend.  p resume.  p terminate.
Processor yield.
Processor activeProcess.
(Delay forSeconds: 2) wait.
```

**`fork` sobre un bloque crea un proceso ligero**, planificado por la máquina virtual con prioridades.
Y como todo en Smalltalk, **el proceso se puede inspeccionar, suspender, examinar su pila y depurar en
marcha** (clase 096).

Para la sincronización, la biblioteca trae lo esperable:

```smalltalk
Semaphore forMutualExclusion.
sem critical: [ ... ].                     "sección crítica"
SharedQueue new.                            "cola con bloqueo"
Monitor new.
```

Y hay una decisión de diseño que define el modelo y que hay que conocer: **los procesos de Smalltalk
son cooperativos dentro de cada prioridad**. Un proceso **no cede el control hasta que se bloquea o
llama a `yield`**, así que dos procesos de la misma prioridad **no se interrumpen entre sí**.

Eso hace que muchas secciones críticas sean innecesarias —**si no puedes ser interrumpido, no hay
carrera**— y hace que un proceso que no cede **bloquee todo el sistema**, incluida la interfaz.

Es el mismo compromiso que el bucle de eventos de Tcl y de JavaScript (clase 119), con el mismo
resultado práctico: **la disciplina de no bloquear**.

Y **los Smalltalk modernos siguen sin usar varios núcleos de verdad**: la máquina virtual de Pharo es
de un solo hilo del sistema operativo. Para el paralelismo real se usan **varias imágenes comunicadas
por mensajes**, que es —otra vez— el modelo de actores y la primera opción del cierre de esta clase.

Merece cerrar con lo que resume el lenguaje: **el planificador está escrito en Smalltalk**, y
`Processor` es un objeto que se puede consultar y modificar. Cuando alguien pregunta cómo funciona la
concurrencia de Smalltalk, la respuesta literal es **"abre el navegador y léelo"**.
"""),
    },
)
