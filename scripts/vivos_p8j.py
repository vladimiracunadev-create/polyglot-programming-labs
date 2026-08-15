# -*- coding: utf-8 -*-
"""Parte 8, lote J — clases 135 y 136. Ver `vivos_parte8.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 135 — Actores y paso de mensajes
# ---------------------------------------------------------------------------
SPECS["135"] = dict(
    gancho="""
Sumar una lista repartiendo el trabajo. El modelo de actores —procesos aislados que solo se comunican
por mensajes— lo formuló **Carl Hewitt en 1973, en el MIT y sobre Lisp**, y su implementación más
famosa es Erlang. Y aquí hay tres sistemas que llevan décadas haciendo exactamente eso sin llamarlo
así: **COBOL bajo CICS, RPG con colas de datos y M con procesos sobre *globals***.
""",
    porque="""
Aquí el concepto es **la unidad aislada que solo se comunica por mensajes**, y estos lenguajes lo
enseñan porque muestran que el modelo se descubrió dos veces. **En la academia**: Hewitt en Lisp
(1973), Milner con CSP y Hoare, y de ahí Erlang (1986) y el modelo BEAM. **Y en la industria**: los
monitores transaccionales de IBM, que en 1969 ya ejecutaban miles de tareas aisladas que se
comunicaban por colas.

Y **Smalltalk** aporta el eslabón: Alan Kay decía que lo importante de los objetos **era el paso de
mensajes** (clase 110), y Hewitt formuló los actores inspirándose en Smalltalk y en Simula.
""",
    cierre="""
Lo transferible: **el modelo de actores no es una técnica de concurrencia, es una decisión sobre los
fallos**. Si nada se comparte, un actor puede morir sin corromper a los demás, y otro puede
reiniciarlo — que es la idea de los árboles de supervisión de Erlang y su famoso "déjalo fallar". Los
sistemas transaccionales llegaron a lo mismo por el mismo camino: **una transacción que falla se
deshace sola y no arrastra a las demás**. Cuando el aislamiento es la prioridad, este modelo aparece
solo.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. ACTORES.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(200).
01  TOKEN   PIC X(20).
01  TLEN    PIC 9(2)  COMP VALUE 0.
01  I       PIC 9(4)  COMP.
01  TOTAL   PIC S9(18) COMP-3 VALUE 0.
01  ED-T    PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    MOVE SPACES TO TOKEN

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > 200
        IF LINEA(I:1) = SPACE
            PERFORM ENVIAR-MENSAJE
        ELSE
            ADD 1 TO TLEN
            MOVE LINEA(I:1) TO TOKEN(TLEN:1)
        END-IF
    END-PERFORM
    PERFORM ENVIAR-MENSAJE

    MOVE TOTAL TO ED-T
    DISPLAY "total=" FUNCTION TRIM(ED-T)
    STOP RUN.

ENVIAR-MENSAJE.
    IF TLEN > 0
        COMPUTE TOTAL = TOTAL + FUNCTION NUMVAL(TOKEN)
        MOVE SPACES TO TOKEN
        MOVE 0 TO TLEN
    END-IF.
""", """
**Lo que esta clase enseña en COBOL.** El modelo de un sistema CICS **es el modelo de actores**, y la
correspondencia es punto por punto:

| Actor (Erlang) | Transacción (CICS) |
|---|---|
| Proceso aislado, sin memoria compartida | **tarea con su propia `WORKING-STORAGE`** |
| Buzón de mensajes | **cola de entrada de la transacción** |
| Enviar un mensaje | `EXEC CICS START` / `WRITEQ TS` |
| Si falla, muere y no arrastra a nadie | **la transacción se deshace y se abandona** |
| Un supervisor lo reinicia | **el monitor rearranca la transacción** |

**Las dos columnas describen la misma arquitectura**, y la de la derecha es de 1969.

Y la última fila merece detalle, porque es el punto del cierre de esta clase: **el "déjalo fallar" de
Erlang existe en CICS con otro nombre**.

```text
ABEND de una transacción → CICS deshace sus cambios, suelta sus bloqueos,
                            registra el fallo y la tarea desaparece.
                            Las otras 40.000 tareas no se enteran.
```

**Un fallo no puede propagarse porque no hay estado compartido que corromper.** Es exactamente el
argumento de Joe Armstrong sobre por qué los actores dan tolerancia a fallos.

Y hay una diferencia real a favor de CICS que conviene señalar: **la transacción deshace los cambios en
los datos**. Un actor de Erlang que muere a mitad de una operación **deja los efectos que ya haya
provocado**; una transacción CICS los revierte.

Es la diferencia entre aislamiento de memoria y aislamiento transaccional, y explica por qué los
sistemas financieros eligieron el segundo.

Y para el paso de mensajes entre programas, COBOL usa las colas de la clase 119:

```cobol
EXEC CICS WRITEQ TS QUEUE('COLA') FROM(MENSAJE) END-EXEC
EXEC CICS START TRANSID('PROC') FROM(DATOS) END-EXEC
```

Y en IMS, el modelo es todavía más literal: **un programa lee mensajes de una cola, los procesa y
escribe respuestas en otra**. Es un actor con el buzón en el sistema operativo.
"""),
        "fortran": ("""
program actores
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

   write(*, '(A,I0)') 'total=', sum(v(1:n))
end program actores
""", """
**Lo que esta clase enseña en Fortran.** **MPI es paso de mensajes puro**, y es el modelo dominante de
la computación científica desde 1994.

```fortran
call MPI_Reduce(parcial, total, 1, MPI_INTEGER, MPI_SUM, 0, MPI_COMM_WORLD, ierr)
```

Y merece comparar MPI con los actores, porque las diferencias explican dos culturas:

| | Actores (Erlang) | MPI |
|---|---|---|
| Número de procesos | **dinámico**, millones | **fijo al arrancar** |
| Direccionamiento | por identificador de proceso | **por rango numérico** |
| Topología | arbitraria | comunicadores y cartesiana |
| Envío | asíncrono, al buzón | **síncrono o asíncrono, con encuentro** |
| Si uno muere | **el supervisor lo reinicia** | **el trabajo entero aborta** |

**Esa última fila es la diferencia cultural.** MPI se diseñó para máquinas donde **un fallo de nodo era
raro** y donde el trabajo se relanza desde un punto de control.

Y esa suposición dejó de ser cierta: **en una máquina de cien mil nodos, algo se rompe cada pocas
horas**. De ahí que Fortran 2018 añadiera lo que la clase 121 mencionaba:

```fortran
if (image_status(i) == stat_failed_image) then ...
form team (...)                                    ! reorganizar sin la imagen muerta
```

**La detección de imágenes fallidas y la reorganización en equipos** es tolerancia a fallos al estilo
de los supervisores de Erlang, llegada a Fortran en 2018 por necesidad de escala.

Y las **colectivas** de MPI y de los coarrays son la operación que esta clase pide:

```fortran
call co_sum(parcial, result_image=1)      ! Fortran 2018: reducción entre imágenes
```

**`co_sum` suma el valor de todas las imágenes**, y la implementación usa un árbol de comunicación —no
un bucle— con coste logarítmico.

Es una operación de agregación distribuida en una línea del lenguaje, y es lo que hace que Fortran siga
siendo competitivo en máquinas con decenas de miles de nodos.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Actores is
   Linea  : String (1 .. 400);
   Ultimo : Natural;
   Pos    : Integer := 1;
   Valor  : Integer;
   Fin    : Positive;
   Total  : Integer := 0;
begin
   Get_Line (Linea, Ultimo);

   loop
      while Pos <= Ultimo and then Linea (Pos) = ' ' loop
         Pos := Pos + 1;
      end loop;
      exit when Pos > Ultimo;

      Get (Linea (Pos .. Ultimo), Valor, Fin);
      Total := Total + Valor;
      Pos := Fin + 1;
   end loop;

   Put ("total=");
   Put (Total, Width => 1);
   New_Line;
end Actores;
""", """
**Lo que esta clase enseña en Ada.** Las tareas de Ada **son actores con memoria compartida**, y esa
combinación es lo que las distingue del modelo de Erlang.

```ada
task Trabajador is
   entry Procesar (X : Integer);      --  el "buzón"
end Trabajador;
```

**Una `entry` es un buzón con una diferencia crucial: la cita es SÍNCRONA** (clase 122). El emisor
espera a que el receptor acepte, mientras que un mensaje a un actor de Erlang **se deposita y sigue**.

| | Actor (asíncrono) | Cita de Ada (síncrona) |
|---|---|---|
| El emisor | sigue inmediatamente | **espera al receptor** |
| Buzón | crece sin límite | la cola de la entrada |
| Contrapresión | **no hay** | **automática** |
| Acoplamiento temporal | ninguno | **fuerte** |

**La ausencia de contrapresión es el problema clásico del modelo de actores**: un productor rápido
llena el buzón de un consumidor lento **hasta agotar la memoria**. Erlang lo sufre y se gestiona a
mano; Ada no lo tiene por construcción.

Y Ada permite las dos formas: **las colas sincronizadas** (clase 120) dan el modelo asíncrono con
capacidad acotada, que es contrapresión.

Y sobre distribución, Ada tiene una parte del estándar que casi nadie conoce: **el Anexo E, sistemas
distribuidos**.

```ada
pragma Remote_Call_Interface;        --  este paquete se puede llamar EN REMOTO
pragma Shared_Passive;                --  datos compartidos entre particiones
```

**Con el Anexo E, un programa Ada se reparte en *particiones* que pueden ejecutarse en máquinas
distintas**, y una llamada a un procedimiento de otra partición se convierte en una llamada remota —
con comprobación de tipos y sin escribir serialización.

Es una llamada a procedimiento remoto **integrada en el lenguaje y con tipos**, en 1995, y la
implementación libre —**GLADE** y después **PolyORB**— llegó a usarse en sistemas reales.

Es otro ejemplo del patrón de Ada: **poner en el lenguaje, con garantías, lo que otros dejan a la
biblioteca**.
"""),
        "pascal": ("""
program Actores;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  Linea, Tok: string;
  I, Total: Integer;
  C: Char;

begin
  ReadLn(Linea);

  Total := 0;
  Tok := '';

  for I := 1 to Length(Linea) + 1 do
  begin
    if I <= Length(Linea) then C := Linea[I] else C := ' ';
    if C = ' ' then
    begin
      if Tok <> '' then
      begin
        Total := Total + StrToInt(Tok);
        Tok := '';
      end;
    end
    else
      Tok := Tok + C;
  end;

  WriteLn('total=', IntToStr(Total));
end.
""", """
**Lo que esta clase enseña en Pascal.** Pascal **no tiene actores**, y su ecosistema los construye con
las piezas de las clases 121 y 133: hilos y colas con bloqueo.

```pascal
Cola := TThreadedQueue<TMensaje>.Create(1024, INFINITE, INFINITE);
TTask.Run(procedure
begin
  while Cola.PopItem(Msg) = wrSignaled do Procesar(Msg);
end);
```

**Un hilo con una cola de entrada es un actor**, y `TThreadedQueue` con capacidad da la contrapresión
que a Erlang le falta.

Y esta clase es buen sitio para nombrar la aportación de la familia Wirth a este modelo, que es
histórica y va por otro camino: **el monitor de Brinch Hansen** (clase 121).

**Concurrent Pascal** (1975) organizaba los programas en **procesos que solo se comunicaban a través de
monitores**, sin variables compartidas directas. Es aislamiento por construcción, con el punto de
encuentro en un objeto sincronizado en lugar de en un buzón.

Y Brinch Hansen escribió sobre exactamente lo que discute esta clase: **su artículo *Distributed
Processes: A Concurrent Programming Concept* (1978)** propone procesos que se comunican **solo por
llamadas a procedimiento remoto**, sin memoria compartida.

**Ese artículo es uno de los antecedentes directos de la cita de Ada** y del modelo que hoy usan los
microservicios.

Es un patrón que esta parte del curso repite: **las ideas de concurrencia de los setenta —monitores,
citas, actores, CSP— se propusieron casi a la vez y por gente que se leía entre sí**, y hoy conviven
todas.

En el Delphi actual, lo que se usa para sistemas distribuidos es la capa de encima: **DataSnap**, REST,
y colas de mensajes externas —RabbitMQ, Kafka— con clientes en Pascal. Es el modelo de actores a escala
de red, que es donde ha acabado triunfando.
"""),
        "lisp": ("""
(let ((total 0))
  (loop for x = (read *standard-input* nil nil)
        while x
        do (incf total x))
  (format t "total=~D~%" total))
""", """
**Lo que esta clase enseña en Common Lisp.** Aquí está el origen: **Carl Hewitt formuló el modelo de
actores en 1973, en el MIT, y su primera implementación —PLASMA— era un lenguaje sobre Lisp**.

Y la genealogía que da esta clase es notable, porque conecta con lo que ya se ha contado:

```text
Simula (1967) ─┐
Smalltalk (1972) ┼→ Hewitt: ACTORES (1973) → PLASMA, Act1, Act2 (en Lisp)
Lisp (1958)     ┘         ↓
                     Erlang (1986) → BEAM → Elixir
                          ↓
                     Akka, Orleans, los microservicios
```

Hewitt cita explícitamente a **Smalltalk** como inspiración, y Alan Kay decía que lo importante de los
objetos era el paso de mensajes (clase 110). **Actores y objetos nacieron de la misma idea, y se
separaron en lo que hicieron con el estado compartido.**

Y Lisp tiene además la conexión con la otra rama: **la investigación en concurrencia de los ochenta
—Multilisp con sus futuros (clase 122), las máquinas Lisp con multitarea— se hizo aquí**.

Hoy, el ecosistema lo cubre:

```lisp
(ql:quickload :lparallel)
(lparallel:make-channel)
(lparallel:submit-task canal #'trabajo)
(lparallel:receive-result canal)

(ql:quickload :cl-actors)
(ql:quickload :calispel)          ; canales al estilo CSP
```

**`lparallel` usa canales explícitos**, y `calispel` implementa CSP con `select` — el modelo de Hoare,
que es el otro gran linaje de esta clase.

Y merece cerrar con la observación de fondo: **el modelo de actores y la programación funcional
encajan de forma natural**, y por eso Erlang es funcional.

Si el estado es inmutable (clase 114), **no hay nada que compartir por accidente**, y el paso de
mensajes deja de ser una disciplina para convertirse en la única opción posible.

Es la misma conclusión desde dos lados: **Erlang llegó a la inmutabilidad porque quería aislamiento**;
los lenguajes funcionales llegaron al aislamiento porque querían inmutabilidad.
"""),
        "tcl": ("""
gets stdin linea

set total 0
foreach x [split [string trim $linea]] {
    incr total $x
}

puts "total=$total"
""", """
**Lo que esta clase enseña en Tcl.** **El modelo de hilos de Tcl es el modelo de actores**, y ya se
explicó en las clases 121 y 133: **un intérprete completo por hilo, sin nada compartido, comunicación
por mensajes**.

```tcl
set id [thread::create]
thread::send $id { ... } resultado          ;# síncrono
thread::send -async $id { ... } variable     ;# asíncrono
thread::wait                                  ;# el hilo espera mensajes: un BUZÓN
```

**`thread::wait` convierte un hilo en un actor**: entra en el bucle de eventos y **procesa los guiones
que le envíen**, uno cada vez.

Y esa es la correspondencia exacta con Erlang: **un proceso con un buzón, que atiende mensajes en
orden y no comparte memoria**.

Lo que Tcl envía no son datos: **son guiones**. Un mensaje es código que el hilo destinatario evalúa,
lo que es más potente y más peligroso que enviar datos.

```tcl
thread::send $id [list procesar $datos]     ;# construir el mensaje como LISTA
```

Y el ecosistema tiene la capa de encima:

```tcl
tpool::create -maxworkers 4 -initcmd { ... }
tpool::post $pool { trabajo }
tpool::wait $pool $ids
```

**`tpool` es un grupo de trabajadores**, que es el patrón dominante en los sistemas de actores reales.

Y Tcl tiene un mecanismo de aislamiento adicional que esta clase debe nombrar, y que ya apareció en la
132: **los intérpretes seguros**.

```tcl
set i [interp create -safe]
$i eval $codigo_ajeno                ;# sin acceso a ficheros, red ni exec
interp delete $i
```

**Un intérprete seguro es un actor con permisos restringidos**: puede calcular y comunicarse, y no
puede tocar el sistema. Y con `interp alias` se le dan exactamente las capacidades que se quiera.

Eso es un aislamiento de capacidades, el mismo modelo que hoy tienen WebAssembly con WASI y los
espacios de nombres de los contenedores — y en Tcl está desde 1995, diseñado para ejecutar applets
en el navegador con Tcl plugin.
"""),
        "perl": ("""
use strict;
use warnings;
use List::Util qw(sum0);

my $linea = <STDIN>;
chomp $linea;

print "total=", sum0(split ' ', $linea), "\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl no tiene actores en el núcleo, y **su modelo idiomático —
`fork` con tuberías— es paso de mensajes puro** (clase 133).

```perl
use Parallel::ForkManager;
my $pm = Parallel::ForkManager->new(4);

$pm->run_on_finish(sub {
    my ($pid, $codigo, $id, $senal, $core, $datos) = @_;
    $total += $$datos;                     # recibir el resultado del hijo
});

for my $trozo (@trozos) {
    $pm->start and next;
    my $parcial = procesar($trozo);
    $pm->finish(0, \\$parcial);              # ENVIAR el resultado al padre
}
$pm->wait_all_children;
```

**`$pm->finish(0, \\$parcial)` envía datos del hijo al padre**, serializándolos por una tubería. Es un
mensaje entre actores, con procesos del sistema operativo como actores.

Y esta clase permite señalar una propiedad del modelo de procesos que los hilos no tienen y que conecta
con el cierre: **el aislamiento ante fallos es real**.

**Un proceso hijo que revienta —por un fallo de segmentación en una extensión en C, por agotar la
memoria— no se lleva al padre.** Con hilos, sí.

Esa es exactamente la razón por la que los servidores web de Perl, Python y Ruby usaron el modelo de
preforkeo durante dos décadas: **un fallo en una petición no puede tumbar el servidor**.

Y es el mismo argumento de Erlang, con el sistema operativo poniendo el aislamiento en lugar de la
máquina virtual.

El ecosistema tiene además implementaciones explícitas del modelo:

```perl
use AnyEvent;  use AnyEvent::Handle;      # eventos y mensajes
use MCE;                                    # Many-Core Engine: reparto de trabajo
use ZMQ::FFI;                                # ZeroMQ: mensajes entre procesos y máquinas
```

**MCE** merece la mención: reparte trabajo entre procesos con colas y reducciones, y su API se parece
mucho a un `pmap` — es el modelo de actores empaquetado como paralelismo de datos.

Es el mismo camino que `lparallel` en Lisp: **el usuario quiere repartir trabajo, no gestionar
actores**.
"""),
        "cpp": ("""
#include <iostream>
#include <iterator>
#include <numeric>
#include <vector>

int main() {
    const std::vector<int> v{std::istream_iterator<int>(std::cin),
                             std::istream_iterator<int>()};

    std::cout << "total=" << std::accumulate(v.begin(), v.end(), 0) << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ **no tiene actores en el estándar**, y sus bibliotecas los
implementan con una diferencia de coste que merece cuantificar frente a Erlang:

```text
proceso de Erlang:  ~300 bytes, creación en microsegundos, millones por nodo
actor en C++:        depende de la biblioteca; con hilos, MB por actor
```

Por eso las bibliotecas serias de C++ **no usan un hilo por actor**: usan un grupo de hilos con una
cola de trabajo, que es lo que hacen también Akka y Orleans.

```cpp
// CAF: C++ Actor Framework
behavior sumador(event_based_actor* self) {
    return {
        [=](int x) { return x * 2; }
    };
}
auto a = sistema.spawn(sumador);
self->send(a, 21);
```

**CAF** implementa el modelo completo —creación, monitorización, supervisión, actores remotos— con
comprobación de tipos en los mensajes, que es algo que Erlang no tiene.

Y esta clase permite señalar la aportación que C++ sí hace y que es la base de todo lo demás: **el
modelo de memoria** (clase 133).

Un sistema de actores necesita garantizar que **cuando un mensaje llega, el receptor ve todo lo que el
emisor escribió antes de enviarlo**. Eso es una relación de "ocurre antes", y **es exactamente lo que
define el modelo de memoria de C++11** con `std::atomic` y sus órdenes.

```cpp
std::atomic<Nodo*> cabeza;
cabeza.store(nuevo, std::memory_order_release);      // "todo lo anterior es visible"
auto p = cabeza.load(std::memory_order_acquire);      // "y yo lo veo"
```

**Sin ese modelo, ninguna biblioteca de actores podría ser correcta**, y antes de C++11 el estándar no
lo definía.

Es un buen recordatorio de la Parte 8 entera: **las abstracciones de alto nivel de la clase 121
descansan sobre garantías de bajo nivel que alguien tuvo que especificar**.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi ACTORES;
  entrada char(200) const;
end-pi;

dcl-s texto varchar(200);
dcl-s tok   varchar(20) inz('');
dcl-s c     char(1);
dcl-s i     int(10);
dcl-s total int(20) inz(0);

texto = %trimr(entrada);

for i = 1 to %len(texto) + 1;
  if i <= %len(texto);
    c = %subst(texto : i : 1);
  else;
    c = ' ';
  endif;
  if c = ' ';
    if tok <> '';
      total += %int(tok);
      tok = '';
    endif;
  else;
    tok += c;
  endif;
endfor;

dsply ('total=' + %char(total));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** La arquitectura clásica de IBM i **es el modelo de actores**, y con
una correspondencia tan exacta como la de COBOL de esta página:

```text
Trabajo servidor ← [cola de datos] ← Trabajos clientes
      ↓
  [cola de respuestas] → cada cliente recoge la suya por CLAVE
```

**Cada trabajo es un actor**: memoria propia, sin nada compartido, un buzón —la cola— y un bucle que
atiende mensajes.

```rpgle
dow *on;
  callp recibir('PETICIONES' : 'MIBIB' : lon : mensaje : -1);   // esperar
  procesar(mensaje);
  callp enviar('RESPUESTAS' : 'MIBIB' : lon : respuesta);
enddo;
```

Y hay tres propiedades que este modelo tiene y el de Erlang no, todas de las clases 121 y 134:

1. **Las colas son persistentes**: sobreviven a la caída del consumidor.
2. **Participan en transacciones**: un mensaje leído dentro de una transacción que se deshace **vuelve
   a la cola**.
3. **Y el reparto entre consumidores lo hace el sistema**: varios trabajos esperando en la misma cola
   se reparten los mensajes.

**La segunda es la importante**, y es la diferencia entre un sistema de mensajería y un sistema de
actores en memoria: **con transacciones, un mensaje no se pierde ni se procesa dos veces**.

Ese es el problema que hoy se llama *entrega exactamente una vez*, y que los sistemas de mensajería
modernos resuelven con esfuerzo — y en IBM i lo da la integración de la cola con el gestor de
transacciones.

Y para la supervisión, la plataforma tiene el equivalente del árbol de Erlang:

```text
Subsistema → arranca trabajos automáticos, los vigila y los REARRANCA
```

**Un trabajo de arranque automático que muere lo puede rearrancar el subsistema**, y la descripción del
subsistema define esa política.

Es tolerancia a fallos por supervisión, configurada por un administrador en lugar de escrita en el
código — que es la diferencia de fondo entre las plataformas de gestión y los lenguajes de esta
página.
"""),
        "pli": ("""
 actores: procedure options(main);

    declare linea char(200) varying;
    declare tok   char(20)  varying initial('');
    declare c     char(1);
    declare (i, total) fixed binary(31);

    get edit (linea) (a(200));
    linea = trim(linea);
    total = 0;

    do i = 1 to length(linea) + 1;
       if i <= length(linea) then c = substr(linea, i, 1); else c = ' ';
       if c = ' ' then do;
          if tok ^= '' then do;
             total = total + tok;
             tok = '';
          end;
       end;
       else tok = tok || c;
    end;

    put skip list ('total=' || trim(char(total)));

 end actores;
""", """
**Lo que esta clase enseña en PL/I.** PL/I no tiene actores, y el entorno donde vive **es un sistema de
mensajería**, igual que el de COBOL de esta página.

Y esta clase permite nombrar la pieza que hace de bus de mensajes en el mundo del mainframe y que
merece conocerse: **IBM MQ**, antes MQSeries.

```pli
 call MQPUT (hconn, hobj, md, pmo, longitud, buffer, compcode, reason);
 call MQGET (hconn, hobj, md, gmo, longitud, buffer, datalen, compcode, reason);
```

**MQ es de 1993 y es probablemente el sistema de mensajería más desplegado del mundo** en banca y
seguros. Sus propiedades son las que esta clase discute:

- **Colas persistentes y transaccionales**: el mensaje participa en la transacción del programa.
- **Entrega garantizada**, con reintentos y colas de mensajes no entregados.
- **Y comunicación entre plataformas**: un programa PL/I en z/OS y un servicio en Java hablan por la
  misma cola.

**Esa última es la razón de que MQ siga siendo central**: es el pegamento entre el mainframe y todo lo
demás, y es el patrón de la clase 105 —modernizar por los bordes— aplicado a la integración.

Y PL/I tiene, dentro del lenguaje, la construcción que se acerca al modelo: **la multitarea con
eventos** (clases 119 y 121), con la que se escribe un productor-consumidor.

Merece cerrar la página de PL/I en esta parte con el balance que la Parte 8 ha ido dejando: **PL/I tuvo
multitarea, eventos, promesas, punteros, áreas y excepciones reanudables antes que casi nadie**, y su
entorno resolvió por otra vía casi todo lo que el lenguaje ofrecía.

La lección, que ya apareció en la clase 122, es la más útil de esta parte sobre PL/I: **una
característica solo arraiga si resuelve un problema que la comunidad tiene y no tiene ya resuelto de
otra forma**.
"""),
        "mumps": ("""
ACTORES ; Actores y paso de mensajes -- clase 135
 read linea
 set total = 0
 for i=1:1:$length(linea, " ") set total = total + $piece(linea, " ", i)
 write "total=", total, !
 quit
""", """
**Lo que esta clase enseña en M.** Un sistema M **es un sistema de procesos aislados que se comunican
por datos compartidos**, y esa es una variante del modelo de esta clase que merece distinguir:

| | Actores | M |
|---|---|---|
| Aislamiento | **total** | variables locales sí, *globals* no |
| Comunicación | **mensajes al buzón** | **escribir en un *global*** |
| Sincronización | orden del buzón | `lock` y transacciones |
| Si uno muere | el supervisor reinicia | el sistema deshace su transacción |

**M comparte el estado, y lo hace a través de un mecanismo que impone las reglas** (clase 133). No es
el modelo de actores: es el modelo de la base de datos compartida.

Y las dos arquitecturas resuelven el mismo problema —que un fallo no corrompa a los demás— por caminos
opuestos: **los actores no comparten nada; M comparte todo y lo protege con transacciones**.

Para el paso de mensajes de verdad, M usa lo de la clase 120: **un *global* como cola**, con
`$increment` atómico.

Y hay un mecanismo que sí es paso de mensajes puro y que merece nombrarse: **el protocolo de
distribución de VistA**.

```text
HL7 / MailMan: los hospitales de VistA se envían mensajes entre sí
```

**MailMan** es un sistema de mensajería escrito en M en los años ochenta, con buzones, colas y
enrutamiento, que conecta cientos de instalaciones. Y **HL7** —el estándar de mensajería sanitaria— es
el formato.

Es una red de actores a escala nacional, escrita en M, funcionando desde antes de que existiera el
correo electrónico tal como lo conocemos.

Y la modernización va por ahí, como se dijo en la clase 122: **IRIS Interoperability** es un bus de
mensajes con productores, procesos de negocio y operaciones, con colas persistentes, reintentos y
trazabilidad — construido sobre *globals*.

**Es el modelo de actores implementado sobre una base de datos**, y es lo que hace que IRIS se venda
hoy como plataforma de integración sanitaria.
"""),
        "smalltalk": ("""
| v |

v := stdin nextLine substrings collect: [ :cada | cada asNumber ].

Transcript
    show: 'total=', (v inject: 0 into: [ :a :b | a + b ]) printString;
    cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Aquí está el eslabón que esta clase necesita: **Alan Kay
concibió los objetos como actores**.

Su modelo mental, ya citado en la clase 110, eran **células biológicas y ordenadores en red**:
entidades autónomas que **solo se comunican por mensajes** y de las que nadie ve el interior.

Y Carl Hewitt formuló el modelo de actores en 1973 **citando a Smalltalk** como una de sus
inspiraciones. Los dos modelos son hermanos, y se separaron en un punto:

| | Smalltalk | Actores |
|---|---|---|
| Envío de mensaje | **síncrono**: se espera la respuesta | **asíncrono** |
| Estado | compartido si se pasan referencias | **nunca compartido** |
| Concurrencia | procesos separados | **cada actor es concurrente** |

**Ese "síncrono" es la diferencia.** En Smalltalk, `objeto mensaje` es una llamada: el emisor espera. En
el modelo de actores, enviar es depositar y seguir.

Kay lamentó eso explícitamente: dijo que **si volviera a diseñarlo, los mensajes serían asíncronos** —
y que ese es el punto en el que su idea original se acercaba más a Erlang que a Java.

Y en Smalltalk el modelo asíncrono se construye con las piezas de las clases 121 y 133:

```smalltalk
| cola |
cola := SharedQueue new.
[ [ true ] whileTrue: [ | msg | msg := cola next. self procesar: msg ] ] fork.
cola nextPut: mensaje.
```

**Un proceso con una `SharedQueue` es un actor**, y en Pharo hay bibliotecas que lo empaquetan.

Y hay un detalle histórico que cierra bien esta clase: **Erlang se diseñó en Ericsson a mediados de los
ochenta**, y sus autores —Joe Armstrong, Robert Virding, Mike Williams— citan Prolog, Smalltalk y los
actores de Hewitt.

La cadena completa es esta:

```text
Simula → Smalltalk (Kay) → Actores (Hewitt) → Erlang (Armstrong) → Elixir, Akka, microservicios
```

**Y hoy, cuando se describe una arquitectura de microservicios —servicios aislados, sin estado
compartido, que se comunican por mensajes y donde un fallo no propaga— se está describiendo la idea
original de Alan Kay sobre lo que debían ser los objetos.**

Tardó cincuenta años en llegar, y llegó a la escala de la red en lugar de a la del programa.
"""),
    },
)

# ---------------------------------------------------------------------------
# 136 — El modelo de memoria y las condiciones de carrera
# ---------------------------------------------------------------------------
SPECS["136"] = dict(
    gancho="""
Incrementar un contador `n` veces. Con un hilo es trivial; con dos, es el problema más sutil de la
informática concurrente. Y aquí hay un dato que ordena la página: **hasta C++11, ningún lenguaje de
uso general de esta lista tenía un modelo de memoria especificado** — Ada sí, con sus objetos
protegidos, y COBOL, RPG y M lo evitaron **no compartiendo memoria mutable**.
""",
    porque="""
Aquí el concepto es **qué ve un hilo de lo que escribe otro**, y estos lenguajes lo enseñan porque
muestran las dos únicas soluciones que funcionan. **Especificar el modelo**: C++11 lo hizo, y su
trabajo lo adoptaron C11 y Rust. **O evitar el problema**: Ada con objetos protegidos donde el
compilador genera la sincronización, y COBOL, RPG y M con procesos aislados y transacciones.

Y el aviso que esta clase debe dar es serio: **una condición de carrera no es un fallo con síntomas —
es un programa sin significado definido**, y el compilador puede optimizar suponiendo que no ocurre.
""",
    cierre="""
Lo transferible: **`contador++` no es una operación, son tres** —leer, sumar, escribir— y entre ellas
cabe otro hilo. Esa es la carrera clásica, y las soluciones son cuatro: **no compartir**, **hacerlo
atómico**, **protegerlo con exclusión** o **hacerlo inmutable**. Ninguna es gratis, y la peor decisión
es la que se toma sin darse cuenta: **compartir una variable entre hilos sin pensarlo**. Si dudas de si
un dato se comparte, ya tienes el problema.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. CARRERA.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(80).
01  N       PIC 9(9) COMP.
01  I       PIC 9(9) COMP.
01  CUENTA  PIC 9(9) COMP VALUE 0.
01  ED-C    PIC Z(8)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)

    PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
        ADD 1 TO CUENTA
    END-PERFORM

    MOVE CUENTA TO ED-C
    DISPLAY "cuenta=" FUNCTION TRIM(ED-C)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** **COBOL no tiene modelo de memoria porque no tiene hilos**, y sus
sistemas concurrentes evitan el problema por construcción: **cada transacción tiene su propia copia de
la `WORKING-STORAGE`** (clase 133).

Y donde sí hay estado compartido —los datos— la disciplina la impone el gestor de recursos:

```cobol
EXEC CICS READ FILE('CONTADOR') RIDFLD(CLAVE) UPDATE END-EXEC
ADD 1 TO CUENTA
EXEC CICS REWRITE FILE('CONTADOR') END-EXEC
EXEC CICS SYNCPOINT END-EXEC
```

**`UPDATE` bloquea el registro hasta el `SYNCPOINT`**, así que la secuencia leer-sumar-escribir es
atómica respecto a las demás transacciones. **Es exactamente la solución del cierre de esta clase:
protegerlo con exclusión**, con el gestor poniendo el bloqueo.

Y hay una construcción de COBOL que esta clase debe nombrar porque es donde sí puede haber carreras:
**el almacenamiento compartido**.

```cobol
01  CONTADOR  PIC 9(9) COMP EXTERNAL.
```

**`EXTERNAL` declara un dato compartido entre todos los programas de una unidad de ejecución**, y en un
entorno con hilos —COBOL for JVM, o CICS con TCB abiertos— **eso es memoria compartida sin
sincronización**.

Es una de las pocas formas de escribir una condición de carrera en COBOL, y es la razón de que las
guías desaconsejen `EXTERNAL` en programas que puedan ejecutarse en varios hilos.

Y merece cerrar con el dato que da la medida de la solución de esta plataforma: **DB2 y CICS ejecutan
millones de operaciones concurrentes sobre los mismos datos sin condiciones de carrera visibles para el
programador**, porque **la unidad de razonamiento es la transacción, no la instrucción**.

Es un nivel de abstracción por encima del modelo de memoria: en lugar de razonar sobre qué ve cada hilo
de cada escritura, se razona sobre **qué ve cada transacción del estado**, con los niveles de
aislamiento de SQL.

Esa abstracción es más fácil de usar correctamente, y es una de las razones por las que los sistemas de
gestión pudieron escalar en concurrencia sin que los programadores fueran expertos en modelos de
memoria.
"""),
        "fortran": ("""
program carrera
   implicit none
   integer :: n, i, cuenta

   read(*, *) n

   cuenta = 0
   do i = 1, n
      cuenta = cuenta + 1
   end do

   write(*, '(A,I0)') 'cuenta=', cuenta
end program carrera
""", """
**Lo que esta clase enseña en Fortran.** Fortran tiene un modelo de memoria **desde 2008**, y llegó con
los coarrays (clase 121) porque los necesitaban.

```fortran
integer :: contador[*]
sync all                       ! BARRERA: todo lo anterior es visible para todos
sync images ([2, 3])            ! barrera parcial
critical
   contador[1] = contador[1] + 1     ! SECCIÓN CRÍTICA: solo una imagen a la vez
end critical
```

**`sync all` es la barrera de memoria del lenguaje**: garantiza que todas las escrituras anteriores son
visibles para todas las imágenes.

Y Fortran 2018 añadió las operaciones atómicas, que son lo que esta clase pide:

```fortran
use iso_fortran_env
integer(atomic_int_kind) :: contador[*]

call atomic_add(contador[1], 1)              ! ATÓMICO: sin carrera
call atomic_fetch_add(contador[1], 1, viejo)  ! y devuelve el anterior
call atomic_cas(contador[1], comparar, nuevo, viejo)   ! comparar e intercambiar
```

**`atomic_cas` —comparar e intercambiar— es la primitiva sobre la que se construyen todas las
estructuras sin bloqueo**, y está en el estándar de Fortran desde 2018.

Y dentro de un nodo, con OpenMP, el problema clásico de esta clase aparece exactamente como se espera:

```fortran
!$omp parallel do
do i = 1, n
   cuenta = cuenta + 1        ! ¡CARRERA! varias hebras leen y escriben
end do

!$omp parallel do reduction(+:cuenta)
do i = 1, n
   cuenta = cuenta + 1         ! correcto: cada hebra acumula y se combina al final
end do
```

**`reduction` es la solución del cierre de esta clase por la vía de no compartir**: cada hilo tiene su
copia privada y se combinan al final.

Es la misma idea que los acumuladores por hilo de cualquier marco de trabajo de paralelismo de datos, y
es la razón de que `sum(v)` (clase 114) se pueda paralelizar sin sincronización.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;

procedure Carrera is
   protected Contador is           --  exclusión mutua GENERADA por el compilador
      procedure Incrementar;
      function Valor return Integer;
   private
      C : Integer := 0;
   end Contador;

   protected body Contador is
      procedure Incrementar is
      begin
         C := C + 1;
      end Incrementar;

      function Valor return Integer is (C);
   end Contador;

   N : Integer;
begin
   Get (N);

   for I in 1 .. N loop
      Contador.Incrementar;         --  seguro aunque lo llamen varias tareas
   end loop;

   Put ("cuenta=");
   Put (Contador.Valor, Width => 1);
   New_Line;
end Carrera;
""", """
**Lo que esta clase enseña en Ada.** **Ada resolvió esta clase en 1983 sin necesitar un modelo de
memoria explícito**, y merece entender cómo: **eliminando la posibilidad de escribir la carrera**.

```ada
protected Contador is
   procedure Incrementar;     --  acceso EXCLUSIVO: el compilador lo garantiza
   function Valor return Integer;
private
   C : Integer := 0;           --  NADIE puede tocar C desde fuera
end Contador;
```

**El dato está en la parte privada del objeto protegido**, así que **no hay forma de acceder a él sin
pasar por una operación protegida**, y esas operaciones tienen exclusión mutua garantizada por el
runtime.

**La carrera no se evita: se hace inexpresable.** Es la misma filosofía que la clase 116 con los
subtipos —*hacer que los estados inválidos sean irrepresentables*— aplicada a la concurrencia.

Y Ada 2012 añadió lo que faltaba para el caso general: **los aspectos de datos compartidos**.

```ada
X : Integer with Volatile;              --  no se cachea en registros
Y : Integer with Atomic;                 --  lectura y escritura ATÓMICAS
Z : Integer with Independent;             --  no comparte palabra con vecinos
pragma Volatile_Components (Tabla);
```

**`Atomic`** garantiza que la lectura y la escritura son indivisibles; **`Volatile`** que no se
reordenan ni se cachean; y **`Independent`** que el compilador no la empaqueta con otras variables en
la misma palabra de memoria — un problema real que causa carreras invisibles cuando dos hilos escriben
campos vecinos.

Y para los sistemas de tiempo real, la restricción que cierra el problema:

```ada
pragma Profile (Ravenscar);
```

**Ravenscar** (clase 124) restringe la concurrencia a un subconjunto **analizable**: tareas fijas,
objetos protegidos con una sola entrada, sin colas dinámicas. **Sobre ese subconjunto se puede demostrar
la ausencia de interbloqueos y calcular los tiempos de respuesta.**

Es la respuesta más fuerte de esta página al problema de esta clase: **no detectar las carreras, sino
restringir el lenguaje hasta que no puedan existir y se pueda demostrar**.
"""),
        "pascal": ("""
program Carrera;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N, I, Cuenta: Integer;

begin
  Read(N);

  Cuenta := 0;
  for I := 1 to N do
    Inc(Cuenta);

  WriteLn('cuenta=', IntToStr(Cuenta));
end.
""", """
**Lo que esta clase enseña en Pascal.** Object Pascal **no tiene un modelo de memoria especificado**, y
depende del que provea la plataforma —el de C++11 en la práctica, porque comparte el hardware y el
sistema operativo.

Lo que sí tiene son las operaciones atómicas, en la clase `TInterlocked`:

```pascal
TInterlocked.Increment(Cuenta);
TInterlocked.Add(Cuenta, 5);
TInterlocked.CompareExchange(Destino, Nuevo, Comparando);
TInterlocked.Exchange(A, B);
```

**`TInterlocked.Increment` es un incremento atómico**, y es exactamente lo que el cierre de esta clase
recomienda para el contador: **hacerlo atómico**, sin bloqueo.

Y Delphi tiene una advertencia propia y muy conocida que ilustra el problema de esta clase mejor que
ningún ejemplo teórico: **el conteo de referencias de las cadenas**.

```pascal
var S: string;      { global, compartida entre hilos }
...
S := S + 'x';        { en dos hilos a la vez: CORRUPCIÓN }
```

**Las cadenas de Pascal llevan un contador de referencias** (clase 102), y **ese contador se incrementa
y decrementa sin sincronización** en las versiones antiguas. Dos hilos manipulando la misma cadena
pueden corromper el contador y liberar la memoria dos veces.

Free Pascal lo resolvió haciendo el conteo atómico **cuando `cthreads` está activa** (clase 133), y de
ahí la importancia de esa unidad: **sin ella, el runtime asume un solo hilo y usa operaciones no
atómicas**.

Es un ejemplo perfecto de lo que esta parte del curso quiere mostrar: **la concurrencia no es solo un
tema del código de usuario — el runtime entero tiene que ser seguro para hilos**, incluidos el gestor
de memoria, el de cadenas y el de excepciones.

Y de ahí el consejo práctico del ecosistema Delphi: **no compartir cadenas, arreglos dinámicos ni
interfaces entre hilos sin sincronizar**, porque su gestión automática de memoria es el punto de
carrera menos evidente.
"""),
        "lisp": ("""
(let ((n (read))
      (cuenta 0))
  (dotimes (i n)
    (incf cuenta))
  (format t "cuenta=~D~%" cuenta))
""", """
**Lo que esta clase enseña en Common Lisp.** El estándar **no dice nada sobre concurrencia** (clase
121), así que **no hay modelo de memoria**, y cada implementación define el suyo.

En SBCL:

```lisp
(sb-ext:atomic-incf (car celda))
(sb-ext:compare-and-swap (symbol-value 'contador) viejo nuevo)
(sb-thread:with-mutex (m) ...)
(sb-ext:atomic-push x (cdr lugar))
```

**`compare-and-swap` es la primitiva de la que se derivan todas las estructuras sin bloqueo**, y SBCL
la expone sobre lugares (clase 095) — sobre un `car`, sobre el valor de un símbolo, sobre un campo de
estructura.

Y Common Lisp tiene una propiedad que ayuda en esta clase y que viene de la clase 121: **las variables
especiales son por hilo**.

```lisp
(defvar *acumulador* 0)          ; cada hilo tiene su enlace
```

**El estado dinámico está aislado por defecto**, así que la carrera solo puede ocurrir sobre estructuras
explícitamente compartidas. Es una decisión que reduce mucho la superficie del problema.

Y merece señalar el peligro específico de un lenguaje con recolector y estructuras mutables:

```lisp
(push x lista)          ; NO es atómico: leer, construir, escribir
```

**`push` sobre una lista compartida entre hilos es una carrera clásica**, y puede perder elementos. La
versión segura es `sb-ext:atomic-push` o un cerrojo.

Y la conclusión es la de esta parte: **un lenguaje sin modelo de memoria especificado deja el
comportamiento concurrente en manos de la implementación**, y el código deja de ser portable.

Es exactamente el problema que C++ tenía antes de 2011, y la razón de que el estándar de C++11 sea la
contribución más importante de esa versión — más que las lambdas o el movimiento.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

set cuenta 0
for {set i 0} {$i < $n} {incr i} {
    incr cuenta
}

puts "cuenta=$cuenta"
""", """
**Lo que esta clase enseña en Tcl.** **En Tcl no puede haber condiciones de carrera sobre variables**, y
esa afirmación fuerte se sostiene por la decisión de las clases 121 y 133: **cada hilo tiene su propio
intérprete y no comparte ninguna variable**.

```tcl
set contador 0        ;# esta variable es de ESTE intérprete y de nadie más
```

**No hay memoria compartida, así que no hay modelo de memoria que especificar.** El problema
desaparece por construcción.

Lo que sí se comparte, explícitamente, son las variables `tsv`:

```tcl
tsv::set compartido contador 0
tsv::incr compartido contador        ;# ATÓMICO: lo garantiza la implementación
tsv::lock compartido { ... }          ;# o exclusión explícita
```

**`tsv::incr` es atómico** y `tsv::lock` da exclusión sobre un conjunto de operaciones. La
sincronización está en el mecanismo de compartir, no en el lenguaje general.

Y esa arquitectura tiene una propiedad que el cierre de esta clase destaca: **para tener una carrera hay
que pedirla explícitamente**. En C++ o en Java, compartir es el defecto y aislar cuesta trabajo; en
Tcl es al revés.

Es el mismo diseño que los *web workers* de JavaScript, que los procesos de Erlang y que los
subintérpretes que Python está adoptando (clase 133).

Y merece cerrar con la comparación que esta clase permite hacer entre los tres lenguajes de guion que
se enfrentaron al problema en los noventa:

| | Decisión | Carreras posibles |
|---|---|---|
| **Tcl** | un intérprete por hilo | **solo con `tsv`, sincronizado** |
| **Perl** | copiar el intérprete | solo con `:shared`, y con `lock` |
| **Python** | un cerrojo global (GIL) | **sí, en el código Python** |

**El GIL de Python protege las estructuras internas del intérprete, no el código del usuario.** Un
`contador += 1` en dos hilos de Python **sí puede perder incrementos**, porque el GIL se libera entre
bytecodes.

Es un malentendido muy extendido, y esta comparación lo deja claro: **Tcl y Perl eligieron el
aislamiento; Python eligió proteger el intérprete y dejó la carrera en manos del programador**.
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

my $cuenta = 0;
$cuenta++ for 1 .. $n;

print "cuenta=$cuenta\\n";
""", """
**Lo que esta clase enseña en Perl.** Con **iThreads**, Perl evita el problema como Tcl: **nada se
comparte salvo lo declarado** (clase 133).

```perl
use threads;
use threads::shared;

my $cuenta :shared = 0;

my @hilos = map { threads->create(sub {
    for (1 .. 1000) {
        lock($cuenta);          # SIN esto, hay carrera
        $cuenta++;
    }
}) } 1 .. 4;
$_->join for @hilos;
```

**`:shared` marca la variable como compartida y `lock` da exclusión mutua**, con la propiedad de que
**el bloqueo se suelta automáticamente al salir del ámbito** — es RAII (clase 132) aplicado al cerrojo.

Y sin `lock`, `$cuenta++` **es exactamente la carrera del cierre de esta clase**: leer, sumar,
escribir, con otro hilo en medio.

Perl documenta además una advertencia que esta clase debe recoger: **compartir una estructura anidada
requiere que cada nivel sea compartido**.

```perl
my %h :shared;
$h{a} = shared_clone({ x => 1 });     # hay que CLONAR a memoria compartida
```

**`shared_clone`** copia una estructura al espacio compartido, y olvidarlo produce errores confusos —
la referencia se comparte y el contenido no.

Es el mismo problema que en cualquier sistema con memoria segmentada, y la razón de que el modelo de
Perl sea tan poco usado en la práctica: **compartir es tan incómodo que la gente prefiere `fork`**
(clase 133).

Y ahí está la conclusión práctica de esta página, que Perl ilustra sin ambigüedad: **cuando compartir
memoria es caro e incómodo, la comunidad elige no compartir** — y ese resultado es exactamente el que
el cierre de esta clase recomienda.

A veces la mejor solución a un problema difícil es que la alternativa sea más cómoda.
"""),
        "cpp": ("""
#include <atomic>
#include <iostream>

int main() {
    int n{};
    if (!(std::cin >> n)) return 1;

    std::atomic<int> cuenta{0};
    for (int i = 0; i < n; ++i) {
        cuenta.fetch_add(1, std::memory_order_relaxed);   // ATÓMICO
    }

    std::cout << "cuenta=" << cuenta.load() << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** **C++11 especificó el primer modelo de memoria de un lenguaje de
uso general**, y esa es una de las contribuciones más importantes de esta página a la informática —
más que cualquier característica sintáctica.

Antes de 2011, **el estándar no decía nada** sobre qué ve un hilo de lo que escribe otro. El código
concurrente dependía del compilador, del procesador y de la fase de la luna, y las bibliotecas de hilos
funcionaban por convención.

C++11 definió:

**La regla fundamental**: dos accesos concurrentes al mismo objeto, siendo uno de escritura y sin
sincronización, son **comportamiento indefinido**. No "un valor raro": **el programa no tiene
significado**.

**Y los órdenes de memoria**:

```cpp
std::memory_order_relaxed    // solo atomicidad; sin garantías de orden
std::memory_order_acquire    // las lecturas posteriores no se adelantan
std::memory_order_release     // las escrituras anteriores son visibles
std::memory_order_acq_rel
std::memory_order_seq_cst      // orden total: el defecto, el más caro
```

**`relaxed` es correcto para un contador** —solo hace falta que no se pierdan incrementos, no que se
ordene nada— y es notablemente más rápido que el defecto en ARM y en POWER.

Ese nivel de control es lo que permite escribir estructuras sin bloqueo correctas y portables, y **ese
trabajo lo adoptaron después C11, Rust y Java** —cuyo modelo de memoria de 2004 fue en realidad el
primero, y sirvió de base al de C++—.

Y las herramientas de esta clase son imprescindibles:

```bash
g++ -fsanitize=thread          # ThreadSanitizer: DETECTA carreras en ejecución
```

**ThreadSanitizer instrumenta cada acceso a memoria** y detecta accesos concurrentes sin
sincronización, aunque no fallen en esa ejecución. Es la única forma práctica de encontrar carreras, y
debería estar en las pruebas de cualquier proyecto concurrente.

Y merece cerrar con lo que C++20 añadió y que hacía falta:

```cpp
cuenta.wait(viejo);          // esperar sin condition_variable
cuenta.notify_all();
std::latch  std::barrier      // sincronización por fases
```
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi CARRERA;
  n int(10) const;
end-pi;

dcl-s i      int(10);
dcl-s cuenta int(10) inz(0);

for i = 1 to n;
  cuenta += 1;
endfor;

dsply ('cuenta=' + %char(cuenta));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG **no tiene modelo de memoria** porque su modelo de concurrencia
es multitrabajo (clases 121 y 133): **cada trabajo tiene su memoria y no comparte**.

Y donde sí hay estado compartido, la plataforma da mecanismos con sincronización incorporada:

```rpgle
in(e) contador;            // LEER un *DTAARA y bloquearlo
contador += 1;
out contador;               // escribir y liberar el bloqueo
```

**`in` y `out` sobre un espacio de datos toman y sueltan un bloqueo del sistema**, así que la secuencia
es atómica entre trabajos — y **persistente**.

Y para los contadores de verdad, Db2 for i da lo que corresponde:

```sql
CREATE SEQUENCE contador AS BIGINT START WITH 1;
VALUES NEXT VALUE FOR contador INTO :n;
```

**Una secuencia de base de datos es un contador atómico, persistente y compartido entre todos los
trabajos y todas las máquinas**, con caché para rendimiento.

Y aquí está el punto que esta clase quiere dejar sobre las plataformas de gestión: **el problema del
contador compartido está resuelto en la capa de datos desde hace décadas**, y con garantías que una
variable atómica en memoria no da — persistencia y participación en transacciones.

Donde RPG **sí** puede tener carreras es en el caso de la clase 087: **el estado estático de un módulo
en un programa de servicio con activación compartida**.

```rpgle
dcl-s cache int(10) dim(100) static;      // ¡compartido entre trabajos!
```

**Si el programa de servicio se activa en un grupo compartido, ese `static` lo ven varios trabajos**, y
sin ninguna sincronización.

Es la fuente de carreras más real de la plataforma, y la razón de la norma que ya se citó: **los
módulos de servicio, sin estado**.

Y merece señalar que ese fallo es especialmente insidioso porque **depende de la configuración de
activación, no del código**: el mismo programa es correcto en un grupo y tiene carreras en otro.
"""),
        "pli": ("""
 carrera: procedure options(main);

    declare n fixed binary(31);
    declare i fixed binary(31);
    declare cuenta fixed binary(31) initial(0);

    get list (n);

    do i = 1 to n;
       cuenta = cuenta + 1;
    end;

    put skip list ('cuenta=' || trim(char(cuenta)));

 end carrera;
""", """
**Lo que esta clase enseña en PL/I.** PL/I tuvo multitarea en 1964 (clase 121) y **no tuvo modelo de
memoria**, como ningún lenguaje hasta 2004.

Y esa combinación —concurrencia sin modelo— es exactamente el problema que esta clase describe: **con
tareas compartiendo `static` y `external` sin garantías especificadas, escribir código concurrente
correcto dependía del compilador y del hardware**.

Lo que PL/I ofrecía para sincronizar eran los eventos (clase 121):

```pli
 declare recurso event;
 wait(recurso);
 completion(recurso) = '0'b;       /* tomar */
 ...
 completion(recurso) = '1'b;        /* soltar */
```

**Un evento usado como semáforo binario**, con la advertencia de que **`completion` no es
necesariamente atómico** en todas las implementaciones — lo que hace de este idioma algo delicado.

Y en el z/OS de la época, la sincronización de verdad venía del sistema operativo:

```text
ENQ / DEQ    -- serialización de recursos con nombre, a nivel de sistema
Compare and Swap (CS)  -- instrucción atómica de la arquitectura, desde 1970
```

**La instrucción `CS` —comparar e intercambiar— está en la arquitectura de IBM desde el System/370 en
1970**, y fue una de las primeras primitivas atómicas de hardware de uso general. Se diseñó
específicamente para multiprocesadores.

Es un dato que da perspectiva a esta clase: **el hardware tuvo la primitiva atómica veinte años antes
de que los lenguajes tuvieran un modelo de memoria que la explicara**.

Y merece cerrar esta parte del curso desde PL/I con la observación que la recorre: **tuvo la
concurrencia antes que nadie y no tuvo cómo razonar sobre ella**, porque la teoría no existía. El
modelo de memoria de Java es de 2004 y el de C++ de 2011.

**Cuarenta años entre tener la capacidad y saber usarla correctamente** es un recordatorio útil de que
una característica sin la teoría que la sostiene es una trampa.
"""),
        "mumps": ("""
CARRERA ; Modelo de memoria y carreras -- clase 136
 read n
 set cuenta = 0
 for i=1:1:n set cuenta = cuenta + 1
 write "cuenta=", cuenta, !
 quit
""", """
**Lo que esta clase enseña en M.** M **no tiene modelo de memoria** y **no lo necesita para las
variables locales**: cada proceso tiene las suyas y no se comparten (clase 133).

Donde hay estado compartido —los *globals*— el problema es real, y M lo resuelve con lo de la clase
121: **`lock` y transacciones**.

```mumps
 lock +^CONTADOR:10
 if $test do
 . set ^CONTADOR = ^CONTADOR + 1
 . lock -^CONTADOR
```

Y M tiene una primitiva que resuelve esta clase concreta de forma directa y elegante: **`$increment`**.

```mumps
 set n = $increment(^CONTADOR)        ; ATÓMICO: incrementa y devuelve el nuevo valor
 set n = $increment(^CONTADOR, 5)      ; en 5
```

**`$increment` es atómico y no necesita `lock`**, y es exactamente lo que el cierre de esta clase
recomienda: **hacerlo atómico**.

Su implementación es lo interesante: **la hace el motor de base de datos**, con el bloqueo del bloque
de disco correspondiente, así que es atómica **entre todos los procesos del sistema y persistente**.

Comparada con un `std::atomic` de C++, tiene tres diferencias:

- **Es mucho más cara** —involucra la caché de bloques de la base de datos—.
- **Es persistente**: sobrevive al reinicio.
- **Y funciona entre procesos y entre máquinas** con ECP (clase 133).

Es la misma operación en un nivel de abstracción completamente distinto.

Y merece cerrar la Parte 8 desde M con la observación que la recorre: **este lenguaje evita la mayoría
de los problemas de esta parte moviendo el problema a la capa de datos**.

Sin punteros no hay punteros colgantes (clase 129); sin memoria compartida mutable no hay carreras
(clase 136); sin reserva explícita no hay fugas (clase 128). Y todo lo que sí es compartido está en una
base de datos transaccional que impone las reglas.

**Es un diseño coherente, tomado en 1966 y sostenido desde entonces** — y explica por qué un lenguaje
que parece primitivo sostiene sistemas que otros no podrían.
"""),
        "smalltalk": ("""
| n cuenta |

n := stdin nextLine trimBoth asNumber.

cuenta := 0.
n timesRepeat: [ cuenta := cuenta + 1 ].

Transcript show: 'cuenta=', cuenta printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk tiene una propiedad que hace esta clase mucho más
simple de lo que sería en otro sitio, y viene de la clase 133: **los procesos son cooperativos dentro
de cada prioridad**.

**Un proceso no cede el control hasta que se bloquea o llama a `yield`**, así que **dos procesos de la
misma prioridad no pueden interrumpirse en mitad de una operación**.

```smalltalk
cuenta := cuenta + 1.        "atómico respecto a los procesos de la misma prioridad"
```

**La carrera clásica del cierre de esta clase no puede ocurrir entre iguales**, porque no hay
desalojo.

Con procesos de prioridad distinta sí puede, y para eso está el mecanismo de siempre:

```smalltalk
| sem |
sem := Semaphore forMutualExclusion.
sem critical: [ cuenta := cuenta + 1 ].
```

Y hay una construcción que Smalltalk tiene y que responde a esta clase con precisión: **la sección
atómica del planificador**.

```smalltalk
[ ... ] valueUnpreemptively.        "no ceder el control durante esto"
Processor activeProcess priority: Processor highIOPriority.
```

Y como el planificador está escrito en Smalltalk (clase 121), **se puede leer exactamente qué garantiza**
— algo que con un planificador del sistema operativo es imposible.

Ahora, la limitación real, ya nombrada: **la máquina virtual de Pharo usa un solo hilo del sistema**, así
que **no hay paralelismo verdadero y por tanto no hay carreras a nivel de hardware**. El problema de
esta clase —qué ve un núcleo de lo que escribe otro— **no llega a plantearse**.

Y para el paralelismo real, el ecosistema usa varias imágenes con mensajes (clase 135), que es la
primera solución del cierre: **no compartir**.

Merece cerrar la Parte 8 con lo que Smalltalk ilustra mejor que ningún otro lenguaje de esta página:
**casi todos los problemas de las dieciséis clases de esta parte —compilación, memoria, pila,
recolección, concurrencia— son observables y modificables desde el propio lenguaje**.

La máquina virtual, el planificador, el recolector, el compilador y la pila **son objetos**. Cuando
alguien pregunta cómo funciona Smalltalk por dentro, la respuesta literal es la misma que la clase 121
daba sobre la concurrencia: **abre el navegador y léelo**.
"""),
    },
)
