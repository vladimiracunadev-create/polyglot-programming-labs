# -*- coding: utf-8 -*-
"""Parte 10, lote C — clases 161 y 162. Ver `vivos_parte10.py` y `gen_vivos.py`."""

SPECS: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# 161 — Procesos y comunicación
# ---------------------------------------------------------------------------
SPECS["161"] = dict(
    gancho="""
Sumar lo que llega por la entrada estándar. Es literalmente lo que hace todo programa de este curso
(clase 040), y esta clase explica por qué esa elección no es casual: **la entrada y la salida estándar
son la frontera entre lenguajes más simple, más portable y más antigua que existe**. Y detrás hay una
frase que cambió la informática: **Doug McIlroy propuso las tuberías de Unix en 1964 con la idea de
"conectar programas como mangueras de jardín"**, y se implementaron en 1973.
""",
    porque="""
Aquí el concepto es la **comunicación entre procesos**, y estos lenguajes la enseñan porque **cubren
todas las formas que existen**: **ficheros temporales entre pasos** (COBOL con JCL), **paso de mensajes
entre miles de procesos** (Fortran con MPI), **la cita entre tareas** (Ada), **colas persistentes**
(RPG y MQ), **la base de datos como canal** (M) y **los sockets con bucle de eventos** (Tcl, Perl,
C++).

Y aparecen los tres ejes que ordenan cualquier decisión: **¿mismo proceso o procesos separados?
¿Síncrono o asíncrono? ¿Se pierde el mensaje si el receptor no está?**
""",
    cierre="""
Lo transferible: **elegir un mecanismo de comunicación es elegir qué pasa cuando el otro lado no está**.
Una llamada de función supone que está; una tubería, que arranca a la vez; un socket, que está ahora
mismo; **una cola persistente, que llegará algún día** — y esa última es la única que sobrevive a un
reinicio. De ahí la regla que evita los peores diseños: **empezar por el modo de fallo, no por el
rendimiento**. Y la segunda, que ahorra mucho trabajo: **texto por la entrada y la salida estándar es
suficiente sorprendentemente a menudo**, y es la única frontera que funciona igual en los doce
lenguajes de esta página.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. RECIBIR.

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
    DISPLAY "recibido=" FUNCTION TRIM(ED)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** El mundo del lote lleva sesenta años practicando la comunicación
entre procesos con el mecanismo más humilde de esta página: **el fichero temporal entre pasos** (clase
149).

```jcl
//PASO1 EXEC PGM=EXTRAER
//SALIDA DD DSN=&&TEMP,DISP=(NEW,PASS),SPACE=(CYL,(10,5))
//PASO2 EXEC PGM=CALCULAR
//ENTRADA DD DSN=&&TEMP,DISP=(OLD,DELETE)
```

**`&&TEMP` es un conjunto de datos temporal** que existe solo mientras dura el trabajo, y **`DISP=PASS`
lo pasa al paso siguiente**.

Y merece comparar esa arquitectura con una tubería de Unix, porque las diferencias importan:

| Aspecto | Tubería de Unix | Fichero temporal de JCL |
|---|---|---|
| Los procesos corren | **a la vez** | **uno tras otro** |
| Memoria intermedia | un búfer pequeño | **el fichero entero, en disco** |
| Si el paso 2 falla | hay que repetir todo | **se reejecuta solo el paso 2** |
| Se puede inspeccionar | no | **sí: el fichero está ahí** |
| Escala | limitada por el proceso más lento | **se puede ordenar en medio** |

**La tercera fila es la razón por la que el lote industrial funciona así**: en un proceso nocturno de seis
horas, **poder reanudar desde el paso que falló** vale más que el ahorro de disco.

Es una decisión que la industria de datos redescubrió: **Spark, Airflow y los orquestadores modernos
materializan los resultados intermedios exactamente por eso**.

Y el mundo mainframe tiene, además, el mecanismo asíncrono que la clase 160 nombraba y que merece verse
aquí como comunicación:

```cobol
           EXEC CICS WRITEQ TS QUEUE('MICOLA') FROM(DATOS) END-EXEC
           EXEC CICS READQ TS QUEUE('MICOLA') INTO(DATOS) END-EXEC

      *> o, entre sistemas y máquinas, con IBM MQ:
           CALL 'MQPUT' USING HCONN HOBJ MSGDESC PUTOPTS BUFLEN BUFFER
                              COMPCODE REASON
```

**Las colas TS de CICS son temporales y locales; MQ es persistente, transaccional y entre máquinas**.

Y esa distinción es exactamente el cierre de esta clase: **con MQ, si el receptor está apagado, el
mensaje espera**. Con una llamada, se pierde la operación.

Es la razón por la que los sistemas financieros usan colas para todo lo que no puede perderse, y por la
que la respuesta a "¿cómo desacoplo esto?" sigue siendo la misma que en 1993.
"""),
        "fortran": ("""
program recibir
   implicit none
   character(len=200) :: linea
   integer :: valor, total, ios, pos

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

   write(*, '(A,I0)') 'recibido=', total
end program recibir
""", """
**Lo que esta clase enseña en Fortran.** El programa lee **la línea entera** y luego la recorre con
lectura interna, y ese detalle es una trampa real de Fortran que merece señalar: **cada sentencia `read`
con formato de lista avanza al registro siguiente**, así que tres `read` consecutivos leen tres líneas,
no tres números de la misma línea. Fortran practica la comunicación entre procesos a una escala que
ningún otro lenguaje de esta página alcanza: **MPI, con decenas o cientos de miles de procesos**.

```fortran
use mpi_f08
call MPI_Init()
call MPI_Comm_rank(MPI_COMM_WORLD, mi_rango)
call MPI_Comm_size(MPI_COMM_WORLD, n_procs)

! Envío punto a punto
call MPI_Send(datos, n, MPI_DOUBLE_PRECISION, destino, etiqueta, MPI_COMM_WORLD)
call MPI_Recv(datos, n, MPI_DOUBLE_PRECISION, origen, etiqueta, MPI_COMM_WORLD, estado)

! Y colectivas: TODOS los procesos participan
call MPI_Allreduce(local, total, 1, MPI_DOUBLE_PRECISION, MPI_SUM, MPI_COMM_WORLD)
```

**`MPI_Allreduce` merece la explicación** porque es lo que hace esta clase interesante: **suma un valor de
cada uno de los cien mil procesos y deja el resultado en todos**, en tiempo logarítmico.

Y lo hace usando **la topología real de la red**: en un superordenador, la biblioteca sabe qué nodos
comparten conmutador y organiza el árbol de reducción para minimizar los saltos.

Es exactamente el programa de esta clase —**sumar lo que llega**— resuelto a escala planetaria y con
conocimiento del hardware.

Y MPI aporta a esta clase las tres decisiones que su API obliga a tomar y que son los ejes del "por
qué":

| Modo | Qué significa |
|---|---|
| **`MPI_Send` bloqueante** | vuelve cuando es seguro reutilizar el búfer |
| **`MPI_Isend` no bloqueante** | vuelve inmediatamente; hay que esperar con `MPI_Wait` |
| **`MPI_Bsend` con búfer** | copia y vuelve; el usuario aporta el búfer |
| **`MPI_Ssend` síncrono** | vuelve **cuando el receptor ha empezado a recibir** |

**Y elegir mal produce el fallo clásico del cálculo paralelo: el interbloqueo.**

```fortran
! ✗ si TODOS los procesos hacen esto a la vez y el mensaje no cabe en el búfer:
call MPI_Send(...)   ! espera a que el otro reciba
call MPI_Recv(...)   ! ...pero el otro también está en Send. INTERBLOQUEO.
```

**La solución es `MPI_Sendrecv`, o intercalar por paridad de rango**, y es uno de los primeros errores
que aprende cualquiera que programe MPI.

Y merece la observación general del cierre de esta clase: **MPI supone que todos los procesos están
vivos y arrancan a la vez**. Si uno muere, **todo el trabajo muere** — no hay tolerancia a fallos.

Es una decisión deliberada, porque **la alternativa cuesta rendimiento**, y es la razón por la que los
cálculos largos guardan puntos de control periódicos: **la tolerancia a fallos está fuera del modelo de
comunicación**.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Recibir is
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

   Put_Line ("recibido=" &
             Ada.Strings.Fixed.Trim (Total'Image, Ada.Strings.Both));
end Recibir;
""", """
**Lo que esta clase enseña en Ada.** Ada tiene la comunicación **dentro** del lenguaje —la cita entre
tareas de la clase 135— y también **entre máquinas**, con un mecanismo que casi nadie conoce y que merece
contarse: **el anexo E, de sistemas distribuidos**.

```ada
--  Una unidad que vive en OTRA máquina, declarada en el lenguaje
package Sensores is
   pragma Remote_Call_Interface;

   function Leer (Id : Positive) return Medida;
   procedure Calibrar (Id : Positive);
end Sensores;
```

**`pragma Remote_Call_Interface` declara que ese paquete se llama desde otra partición**, y a partir de
ahí:

```ada
Valor := Sensores.Leer (3);      --  parece local; ocurre en la otra máquina
```

**El anexo E define particiones, llamadas remotas, tipos de acceso remotos y datos compartidos**, todo
como parte del estándar de Ada de 1995 — con implementaciones como **GLADE** y **PolyORB**.

Y merece compararlo con CORBA (clase 160), porque tiene el mismo problema y una defensa mejor:

**El problema es el mismo**: **hacer que lo remoto parezca local esconde el fallo de red**.

**Y la defensa de Ada es que el fallo es una excepción declarada**:

```ada
begin
   Valor := Sensores.Leer (3);
exception
   when System.RPC.Communication_Error => ...   --  la red falló: hay que decidir
end;
```

**`Communication_Error` es parte del contrato**, así que el compilador y el lector saben que esa llamada
puede fallar por razones que una llamada local no tiene.

Es una mejora sobre la abstracción transparente, aunque no resuelve el problema de fondo: **la latencia
sigue siendo invisible**.

Y hay un mecanismo del anexo E que merece destacarse porque es poco común y muy útil: **los objetos
compartidos pasivos**.

```ada
package Estado_Global is
   pragma Shared_Passive;
   Contador : Integer := 0;      --  ¡compartido entre particiones, PERSISTENTE!
end Estado_Global;
```

**Una partición pasiva es memoria compartida entre programas, que sobrevive a su terminación** — que es,
conceptualmente, una base de datos declarada en el lenguaje.

Es lo más parecido de esta página a las globals de M, y viene de un requisito real de los sistemas
distribuidos de defensa: **estado compartido entre nodos, con tipos comprobados**.
"""),
        "pascal": ("""
program Recibir;
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

  WriteLn('recibido=', IntToStr(Total));
end.
""", """
**Lo que esta clase enseña en Pascal.** Free Pascal trae en la distribución las tres formas de
comunicación de esta página, y merece verlas porque su API es de las más legibles:

```pascal
uses Process;
var P: TProcess;
begin
  P := TProcess.Create(nil);
  P.Executable := 'sort';
  P.Options := [poUsePipes];        { ← tuberías con el hijo }
  P.Execute;
  P.Input.Write(Datos[1], Length(Datos));
  P.CloseInput;
  P.Output.Read(Buffer, SizeOf(Buffer));
end;
```

```pascal
uses ssockets;
var S: TInetServer;
begin
  S := TInetServer.Create(8080);
  S.OnConnect := @AtenderCliente;
  S.StartAccepting;
end;
```

**`poUsePipes` es la clave del primero**: sin él, el hijo hereda la entrada y la salida del padre; con
él, se crean tuberías y el padre habla con el hijo.

Y merece señalar la trampa clásica de las tuberías, porque produce interbloqueos y casi nadie la
anticipa: **el búfer de la tubería es pequeño**.

```pascal
{ ✗ INTERBLOQUEO si los datos superan el búfer de la tubería (~64 KB) }
P.Input.Write(DatosGrandes, N);    { el padre escribe y se bloquea porque el búfer está lleno }
P.CloseInput;                       { ...nunca llega aquí }
P.Output.Read(...);                  { y el hijo está bloqueado escribiendo su salida }
```

**Los dos procesos se bloquean escribiendo, porque ninguno lee.**

Y la solución es la de siempre en esta clase: **leer y escribir a la vez** —con hilos, con `select` o con
el bucle de eventos— o **usar ficheros temporales** como el JCL de esta página.

Es exactamente el mismo interbloqueo que MPI en Fortran de esta página, con otro vocabulario, y es la
razón por la que `TProcess` tiene el método `RunCommandIndir` que lo hace bien por dentro.

Y el ecosistema Delphi añade el mecanismo propio de Windows que merece nombrarse:

```pascal
{ Memoria compartida con nombre: el IPC más rápido de Windows }
H := CreateFileMapping(INVALID_HANDLE_VALUE, nil, PAGE_READWRITE, 0, 4096, 'MiMapa');
P := MapViewOfFile(H, FILE_MAP_ALL_ACCESS, 0, 0, 0);
```

**Memoria compartida sin copia**, que es lo más rápido posible — y también lo que exige sincronización
explícita y no tiene ninguna de las garantías de una cola (clase 136).
"""),
        "lisp": ("""
(let ((total 0))
  (with-input-from-string (s (read-line))
    (loop for valor = (read s nil nil)
          while valor
          do (incf total valor)))
  (format t "recibido=~D~%" total))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp aporta a esta clase un mecanismo que su modelo hace
natural y que merece destacarse: **el canal de comunicación puede transportar estructuras, no solo
bytes** (clase 159).

```lisp
;; Servidor
(let ((socket (usocket:socket-listen "0.0.0.0" 4005)))
  (loop
    (let* ((con (usocket:socket-accept socket))
           (flujo (usocket:socket-stream con)))
      (let ((peticion (read flujo)))          ; ← lee una ESTRUCTURA
        (print (procesar peticion) flujo)      ; ← y escribe otra
        (force-output flujo)))))
```

**`read` y `print` sobre un socket transportan listas anidadas directamente** (clase 104), sin
serializador y sin esquema.

Y la advertencia va con ello y es la de la clase 153: **`read` sobre un socket es ejecución remota de
código** si `*read-eval*` está activo. **En producción hay que desactivarlo** o usar un formato de datos
de verdad.

Y Lisp tiene el mecanismo de comunicación más característico de su ecosistema, que ya apareció en la
clase 138 y que merece verse aquí como lo que es: **swank**.

```lisp
(swank:create-server :port 4005 :dont-close t)
```

**Eso abre un canal por el que otro proceso —el editor— puede evaluar expresiones dentro de la imagen
viva**, inspeccionar objetos, abrir el depurador y redefinir funciones.

Es un protocolo de comunicación entre procesos **cuyo contenido es código**, y es la razón por la que se
puede depurar un servidor Lisp en producción desde el portátil (clase 148).

Y el ecosistema, para lo demás:

| Biblioteca | Notas |
|---|---|
| **usocket** | sockets portables entre implementaciones |
| **bordeaux-threads** | hilos, y con ellos colas en memoria |
| **lparallel** | **colas, canales y tareas**, al estilo de los actores (clase 133) |
| **cl-async / woo** | entrada y salida asíncrona sobre libuv |
| **uiop:run-program** | lanzar procesos, con tuberías |

**`lparallel` merece la mención** porque implementa el modelo que la clase 133 describía: **canales y
tareas**, con una cola de trabajo y un conjunto de hilos.

Y con eso Lisp cubre los tres ejes del "por qué" de esta clase — pero merece señalar el que le falta a
casi todas las columnas de esta página: **ninguno de esos mecanismos es persistente**. Si el proceso
muere, lo que había en la cola se pierde.

Para eso hacen falta las colas del mainframe, las de RPG o una base de datos — que es la conclusión del
cierre.
"""),
        "tcl": ("""
gets stdin linea

set total 0
foreach v [split [string trim $linea]] {
    if {$v ne ""} { incr total $v }
}

puts "recibido=$total"
""", """
**Lo que esta clase enseña en Tcl.** Tcl tiene la API de comunicación más uniforme de esta página, y su
diseño merece destacarse porque es una idea que otros lenguajes tardaron décadas en adoptar: **todo es un
canal**.

```tcl
set c [open "fichero.txt" r]           ;# un fichero
set c [open "|sort -n" r+]              ;# ¡un PROCESO, con tubería bidireccional!
set c [socket localhost 8080]            ;# un socket
set c stdin                               ;# la entrada estándar

# y a todos se les habla igual:
puts $c "datos"
gets $c linea
fconfigure $c -blocking 0 -buffering line -encoding utf-8
close $c
```

**`open "|comando"` abre un proceso como si fuera un fichero**, y a partir de ahí `gets` y `puts`
funcionan igual que con cualquier otra cosa.

Es la generalización de la idea de Unix —**todo es un fichero**— llevada al lenguaje, y hace que **el
mismo código sirva para leer de un fichero, de una tubería o de la red**.

Y `fconfigure` es donde se declaran las decisiones de esta clase:

| Opción | Qué decide |
|---|---|
| **`-blocking 0`** | no bloquear: el bucle de eventos se encarga |
| **`-buffering line/full/none`** | cuándo se vacía (clase 141) |
| **`-encoding utf-8`** | la codificación del texto (clase 093) |
| **`-translation binary`** | sin conversión de fin de línea |

**`-translation binary` merece la advertencia**, porque es el error clásico: **sin él, Tcl traduce los
fines de línea**, y un fichero binario leído como texto se corrompe.

Y la otra mitad del modelo de Tcl es el **bucle de eventos** (clase 134):

```tcl
socket -server aceptar 8080
proc aceptar {canal dir puerto} {
    fconfigure $canal -blocking 0
    fileevent $canal readable [list leer $canal]     ;# ← avísame cuando haya datos
}
vwait forever
```

**`fileevent` registra una retrollamada para cuando el canal tenga datos**, y `vwait` entra en el bucle.

**Eso es entrada y salida asíncrona con un solo hilo**, y es el modelo que Node.js popularizó quince años
después — con la misma arquitectura y las mismas ventajas: **miles de conexiones simultáneas sin un hilo
por cada una** (clase 136).

Y Tcl lo tenía en 1993, por la misma razón que lo tenía Tk: **una interfaz gráfica también es un bucle de
eventos**.
"""),
        "perl": ("""
use strict;
use warnings;
use List::Util qw(sum0);

my $linea = <STDIN>;
chomp $linea;

print "recibido=", sum0(split ' ', $linea), "\\n";
""", """
**Lo que esta clase enseña en Perl.** Perl es el lenguaje de la filosofía de Unix, y esta clase es el
sitio para contar de dónde viene la idea del gancho.

**Doug McIlroy escribió en un memorando de 1964:**

> Deberíamos tener alguna forma de acoplar programas como **mangueras de jardín**: enroscar otro segmento
> cuando haga falta manipular los datos de otra manera.

**Y en 1973 Ken Thompson implementó las tuberías en una noche.** Al día siguiente, McIlroy cuenta que
todo el laboratorio estaba encadenando comandos con una euforia que recordaba como "un delirio".

Y las cuatro reglas de la filosofía que salió de ahí merecen citarse porque son el cierre de esta clase:

```text
1. Haz que cada programa haga una cosa bien.
2. Espera que la salida de un programa sea la entrada de otro.
3. Diseña para probar pronto; no dudes en tirar lo torpe y rehacerlo.
4. Usa herramientas antes que ayuda no cualificada, incluso para tareas de usar y tirar.
```

**La regla 2 es la que este curso aplica en 176 clases**: cada programa lee de la entrada estándar y
escribe en la salida estándar (clase 040), y por eso **el mismo verificador comprueba los doce
lenguajes**.

Y Perl da todos los mecanismos, con la sintaxis más compacta de esta página:

```perl
open(my $fh, '-|', 'sort', '-n') or die;        # leer de un proceso
open(my $fh, '|-', 'mail', '-s', $asunto) or die; # escribir a un proceso

use IPC::Open3;
open3(\\*ESCRIBIR, \\*LEER, \\*ERRORES, @comando);   # las TRES a la vez

my $pid = fork();                                  # bifurcar
if ($pid == 0) { ...hijo... } else { waitpid($pid, 0) }

use IO::Socket::INET;
my $s = IO::Socket::INET->new(PeerAddr => 'host:80');
```

**`open3` merece la advertencia**, porque tiene el interbloqueo de Pascal de esta página en su forma más
fácil de provocar: **si se escribe mucho sin leer la salida, los dos procesos se bloquean**.

Y la solución es `IPC::Run`, que hace el `select` por dentro:

```perl
use IPC::Run qw(run);
run \\@comando, \\$entrada, \\$salida, \\$errores;   # correcto, sin pensar
```

Y merece cerrar con la observación práctica de esta clase: **la lista de argumentos, nunca la cadena**.

```perl
system("rm $fichero");            # ✗ inyección de comandos (clase 153)
system('rm', '--', $fichero);      # ✓ sin intérprete de órdenes de por medio
```

**Con lista, no hay `sh` en medio**, así que un nombre de fichero con `;` o con espacios **no puede
ejecutar nada**.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    long long total = 0, valor = 0;
    while (std::cin >> valor) total += valor;

    std::cout << "recibido=" << total << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ es donde se implementan los mecanismos que los demás usan, y
esta clase es el sitio para ordenarlos por lo que cuestan, que es la decisión real.

| Mecanismo | Latencia típica | Nota |
|---|---|---|
| **Llamada de función** | ~1 ns | mismo proceso |
| **Cola sin bloqueo en memoria** | ~20-100 ns | mismo proceso, entre hilos |
| **Memoria compartida** | ~100 ns | procesos distintos, **misma máquina** |
| **Tubería / socket local** | ~5-50 µs | con paso por el núcleo |
| **Socket de red (misma sala)** | ~50-500 µs | |
| **Cola persistente** | ~1-10 ms | **sobrevive al reinicio** |
| **Entre continentes** | ~100-300 ms | la velocidad de la luz no negocia |

**Esa tabla es el contenido práctico de esta clase**, y merece subrayar los saltos: **de memoria
compartida a socket local hay dos órdenes de magnitud**, y **de ahí a una cola persistente, otros dos**.

Y cada salto compra algo: **aislamiento, luego máquinas distintas, luego supervivencia al fallo** — que
es exactamente lo que el cierre de esta clase dice que hay que elegir primero.

Y C++ moderno tiene las herramientas de las dos puntas:

```cpp
// Memoria compartida entre procesos, sin copia
#include <sys/mman.h>
void* p = mmap(nullptr, tam, PROT_READ | PROT_WRITE,
               MAP_SHARED | MAP_ANONYMOUS, -1, 0);

// Entrada y salida asíncrona moderna en Linux: io_uring
struct io_uring anillo;
io_uring_queue_init(256, &anillo, 0);
```

**`io_uring` merece la mención** porque cambia el modelo: **dos colas circulares compartidas entre el
programa y el núcleo** —una de peticiones y otra de resultados— **de modo que se pueden enviar cientos de
operaciones sin una sola llamada al sistema**.

Es la respuesta al coste de la cuarta fila de la tabla, y es de 2019.

Y merece cerrar con la advertencia que la clase 136 anticipó y que aquí es crítica: **la memoria
compartida entre procesos no tiene sincronización**.

```cpp
std::atomic<int>* contador = static_cast<std::atomic<int>*>(p);
contador->fetch_add(1, std::memory_order_relaxed);
```

**Hay que poner las barreras a mano**, y **los punteros no sirven**: la misma región puede estar
mapeada en direcciones distintas en cada proceso, así que **dentro de la memoria compartida solo pueden
viajar desplazamientos, no punteros**.

Es un error clásico y silencioso, y es la razón por la que las bibliotecas serias
—`boost::interprocess`— proporcionan punteros relativos.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi RECIBIR;
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

dsply ('recibido=' + %char(total));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** IBM i tiene un mecanismo de comunicación entre procesos que es del
sistema operativo y que merece conocerse porque casi ninguna plataforma lo tiene igual: **las colas de
datos**.

```text
CRTDTAQ DTAQ(MIBIB/MICOLA) MAXLEN(1000) SEQ(*FIFO)
```

```rpgle
// Enviar
dcl-pr enviarDtaQ extpgm('QSNDDTAQ');
  cola     char(10) const;
  bib      char(10) const;
  longitud packed(5:0) const;
  datos    char(1000) const options(*varsize);
end-pr;

// Recibir, con ESPERA
dcl-pr recibirDtaQ extpgm('QRCVDTAQ');
  cola     char(10) const;
  bib      char(10) const;
  longitud packed(5:0);
  datos    char(1000) options(*varsize);
  espera   packed(5:0) const;      // segundos; -1 = esperar indefinidamente
end-pr;
```

Y las propiedades que la hacen valiosa merecen enumerarse, porque cubren los tres ejes del "por qué":

- **Es del sistema operativo**: no hay servidor de colas que instalar ni mantener.
- **`SEQ(*FIFO)`, `*LIFO` o `*KEYED`**: con clave, un receptor puede pedir **solo los mensajes de cierto
  tipo**.
- **El receptor espera sin consumir CPU**, con tiempo límite.
- **Y puede ser persistente**: con `FORCE(*YES)` sobrevive a un reinicio.

**La tercera es la que la hace el mecanismo estándar de esta plataforma**: **un programa servidor espera
en la cola, sin gastar nada**, y se despierta cuando llega trabajo.

Es el patrón productor-consumidor de la clase 135, resuelto por el sistema operativo, y es como se
construyen los servicios de fondo en IBM i desde hace treinta años.

Y el resto del arsenal de la plataforma:

| Mecanismo | Nota |
|---|---|
| **Colas de datos** | el estándar; rápido, con clave, opcionalmente persistente |
| **Colas de usuario** (`*USRQ`) | más rápidas todavía, de más bajo nivel |
| **Espacios de usuario** (`*USRSPC`) | **memoria compartida con nombre**, hasta 16 MB |
| **Colas de mensajes** | para avisos a operadores y a trabajos |
| **MQ / sockets / IFS** | lo estándar del sector |
| **La propia base de datos** | una tabla como cola, con `SELECT ... FOR UPDATE` |

**La última fila merece el comentario**, porque es lo que muchos sistemas modernos acaban haciendo:
**usar la base de datos como cola** tiene la ventaja de ser transaccional con el resto del trabajo — que
es exactamente el argumento que M desarrolla en esta misma página.
"""),
        "pli": ("""
 recibir: procedure options(main);

    declare valor fixed binary(31);
    declare total fixed binary(31) initial(0);

    on endfile(sysin) goto fin;

    do while ('1'b);
       get list (valor);
       total = total + valor;
    end;

 fin:
    put skip list ('recibido=' || trim(char(total)));

 end recibir;
""", """
**Lo que esta clase enseña en PL/I.** PL/I aporta a esta clase el mecanismo que definió la integración
empresarial durante treinta años y que la clase 160 ya nombró: **la cola de mensajes**.

```pli
 call MQOPEN (hconn, objdesc, options, hobj, compcode, reason);
 call MQPUT  (hconn, hobj, msgdesc, putopts, buflen, buffer, compcode, reason);
 call MQGET  (hconn, hobj, msgdesc, getopts, buflen, buffer, datalen,
              compcode, reason);
 call MQCMIT (hconn, compcode, reason);      /* ¡CONFIRMAR la transacción! */
```

**`MQCMIT` es la línea que merece explicarse**, porque es la propiedad que distingue a MQ de un socket y
que el cierre de esta clase señala como decisiva:

```text
La operación PONER un mensaje forma parte de la MISMA transacción
que la actualización de la base de datos.

Si la transacción se deshace, el mensaje NO se envía.
Si se confirma, el mensaje está garantizado.
```

**Eso resuelve el problema más difícil de los sistemas distribuidos**: que la base de datos y el mensaje
queden coherentes.

Sin ello, hay dos fallos posibles y los dos ocurren: **actualizar la base y morir antes de enviar** —el
otro sistema nunca se entera— o **enviar y morir antes de confirmar** —el otro procesa algo que no
ocurrió—.

Y es tan importante que tiene nombre en la literatura moderna: **el problema del *dual write***, y las
soluciones actuales —el patrón de bandeja de salida, las transacciones distribuidas, los registros de
eventos como Kafka— **están intentando recuperar lo que MQ con dos fases ya daba en 1993**.

Y merece explicar el mecanismo, porque es una pieza de ingeniería seria: **la confirmación en dos
fases**.

```text
Fase 1 (preparar): el coordinador pregunta a la base de datos y a MQ:
                   "¿puedes confirmar?" — y los dos se comprometen.
Fase 2 (confirmar): si todos dijeron que sí, el coordinador ordena confirmar.
                    Si alguno dijo que no, ordena deshacer.
```

**En z/OS, el coordinador es RRS; en CICS, el propio gestor de transacciones.**

Y su coste hay que decirlo, porque es la razón de que hoy se use menos: **bloquea recursos durante las
dos fases** y **si el coordinador cae entre la fase 1 y la 2, los participantes quedan en duda**, con
los recursos retenidos hasta que se resuelve a mano.

Es el compromiso clásico entre consistencia y disponibilidad, y explica por qué los sistemas modernos
prefieren la consistencia eventual con compensación — que es más barata y **traslada el problema al
programa**.
"""),
        "mumps": ("""
RECIBIR ; Sumar lo recibido -- clase 161
 read linea
 new i, total, n
 set total = 0
 for i = 1:1:$length(linea, " ") do
 . set n = $piece(linea, " ", i)
 . if n '= "" set total = total + n
 write "recibido=", total, !
 quit
""", """
**Lo que esta clase enseña en M.** M tiene la respuesta más peculiar de esta página, y es la que su
modelo hace inevitable: **la comunicación entre procesos es la base de datos**.

```mumps
 ; Proceso A escribe
 tstart
 set ^COLA($increment(^COLA)) = mensaje
 tcommit

 ; Proceso B lee
 set n = $order(^COLA(""))
 if n '= "" do
 . set mensaje = ^COLA(n)
 . kill ^COLA(n)
```

**Y esa cola tiene, gratis, las propiedades que en otros ecosistemas requieren un producto entero:**

- **Persistencia**: está en disco.
- **Transaccionalidad**: participa en `tstart`/`tcommit`, **junto con el resto del trabajo** — que es
  exactamente lo que PL/I necesita dos fases para conseguir en esta página.
- **Orden garantizado**: los subíndices están ordenados (clase 095).
- **Y visibilidad**: cualquier proceso puede mirar la cola sin bloquear a nadie.

**La segunda es la valiosa**: en M, **escribir el dato y encolar el aviso son la misma transacción**,
así que el problema de la doble escritura **no existe**.

Es una ventaja arquitectónica real, y es la razón por la que los sistemas construidos sobre M tienen
menos incidencias de datos incoherentes de lo que su edad haría esperar.

Y M tiene además el mecanismo de sincronización del lenguaje:

```mumps
 lock +^RECURSO("cuenta", 4711):5     ; bloqueo con TIEMPO LÍMITE de 5 segundos
 if $test do
 . ; ... trabajar ...
 . lock -^RECURSO("cuenta", 4711)
```

**`lock` es un bloqueo con nombre, del sistema, con tiempo límite y con conteo** — y merece señalar que
**es consultivo**: bloquea contra otros que también hagan `lock`, no contra quien escriba directamente.

Es la misma semántica que `flock` en Unix, y la misma trampa: **funciona si todo el mundo coopera**.

Y el resto:

```mumps
 job procesar^MIRUT                  ; lanzar un proceso M en segundo plano
 open "|TCP|4005"::"SOCKET"           ; sockets, con la sintaxis de dispositivos
 write $zjob                           ; identificador del trabajo
```

Y merece cerrar con la observación general: **cuando el estado compartido es la base de datos, la
comunicación entre procesos y el almacenamiento son la misma cosa** — con la ventaja de la
transaccionalidad y el coste de que **todo pasa por disco**, que es la fila más lenta de la tabla de C++
en esta página.
"""),
        "smalltalk": ("""
| linea total |

linea := stdin nextLine trimBoth.
total := 0.

(linea substrings: ' ') do: [ :p | total := total + p asNumber ].

Transcript show: 'recibido=', total printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk tiene una posición peculiar en esta clase, y viene
de la Parte 8: **dentro de la imagen, todo son objetos y no hace falta comunicación; fuera, hay que
salir del mundo**.

```smalltalk
"Dentro: procesos ligeros compartiendo objetos"
| cola |
cola := SharedQueue new.
[ 1 to: 10 do: [ :i | cola nextPut: i ] ] fork.
[ 10 timesRepeat: [ Transcript show: cola next printString ] ] fork.
```

**`SharedQueue` es una cola con sincronización**, y `fork` crea un proceso ligero de Smalltalk (clase
135) — **todo dentro de la misma imagen y sin serializar nada**.

Y hacia fuera:

```smalltalk
"Sockets"
| socket |
socket := Socket newTCP.
socket connectToHostNamed: 'ejemplo.com' port: 80.
socket sendData: 'GET / HTTP/1.0', String crlf, String crlf.

"Procesos externos"
LibC runCommand: 'sort -n < entrada.txt'.
OSSUnixSubprocess new command: 'sort'; arguments: #('-n'); runAndWaitOnExitDo: [...]
```

Y Smalltalk aporta a esta clase un mecanismo que ningún otro de la página tiene con la misma naturalidad,
y es la consecuencia de que la pila sea un objeto (clase 127): **enviar un mensaje a otra imagen**.

```smalltalk
"El objeto remoto se comporta como uno local"
remoto := RemoteObject on: 'otra-maquina' port: 4242 id: #servicioPedidos.
remoto crearPedido: unPedido.
```

**El proxy usa `doesNotUnderstand:`** (clase 158) **para capturar cualquier mensaje, serializarlo con
Fuel** (clase 159) **y enviarlo**.

Y merece señalar la misma advertencia que el anexo E de Ada en esta página: **hacer que lo remoto parezca
local esconde la latencia y el fallo**.

La diferencia es que en Smalltalk **eso se puede construir en una tarde**, con lo que la tentación es
mayor — y es una de las razones por las que el modelo de objetos distribuidos, tan atractivo sobre el
papel, perdió frente al paso de mensajes explícito (clase 160).

Y merece cerrar con el sistema que sí lo resolvió bien y que la clase 148 nombró: **GemStone/S**.

**Múltiples máquinas virtuales de Smalltalk comparten un repositorio de objetos transaccional**, así que
**la comunicación entre procesos es el propio grafo de objetos**, con transacciones y persistencia.

Es exactamente el modelo de M en esta página —**el estado compartido es la base de datos**— construido
con objetos en lugar de con globals, y lleva funcionando en sistemas financieros desde los años noventa.
"""),
    },
)

# ---------------------------------------------------------------------------
# 162 — WebAssembly como objetivo común
# ---------------------------------------------------------------------------
SPECS["162"] = dict(
    gancho="""
Elevar al cuadrado. El programa da igual: lo que esta clase pregunta es **dónde se ejecuta**. Y la
respuesta nueva es **un formato binario portátil que corre en el navegador, en el servidor y en el borde
de la red, con aislamiento por diseño**. Y aquí hay una sorpresa que merece el titular: **de los doce
lenguajes de esta página, al menos siete tienen hoy alguna forma de ejecutarse en WebAssembly** — y
entre ellos están Perl, Pascal y Smalltalk.
""",
    porque="""
Aquí el concepto es el **objetivo de compilación común**, y estos lenguajes lo enseñan porque **ya
vivieron esta historia**: la máquina virtual de Smalltalk (1980), el bytecode de Tcl y de Perl, la
máquina virtual de Java (1995), la de .NET (2002). **WebAssembly es el enésimo intento de un formato
intermedio universal**, y el primero que ha conseguido que casi todos lo apunten.

Y aparece la pregunta que decide cuánto sirve para cada uno: **¿el lenguaje necesita un recolector de
basura, hilos o llamadas al sistema?** Porque WebAssembly, por diseño, **no tenía nada de eso**.
""",
    cierre="""
Lo transferible: **WebAssembly no es un lenguaje ni un sustituto de nada — es un objetivo de compilación
con aislamiento por defecto**. Y esa última parte es lo importante: **un módulo no puede hacer nada que
no se le haya dado explícitamente**, ni leer ficheros, ni abrir sockets, ni ver la memoria de nadie. Es
el modelo de capacidades de la clase 153 aplicado al despliegue. La regla práctica al considerarlo:
**preguntar qué necesita el lenguaje que no está en el modelo** —recolector, hilos, sistema de
ficheros— porque de eso depende si la portabilidad sale casi gratis o cuesta un año.
""",
    langs={
        "cobol": ("""
IDENTIFICATION DIVISION.
PROGRAM-ID. CUADRADO.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  LINEA   PIC X(40).
01  N       PIC S9(9) COMP.
01  R       PIC S9(18) COMP.
01  ED      PIC -(17)9.

PROCEDURE DIVISION.
    ACCEPT LINEA
    COMPUTE N = FUNCTION NUMVAL(LINEA)
    COMPUTE R = N * N

    MOVE R TO ED
    DISPLAY "resultado=" FUNCTION TRIM(ED)
    STOP RUN.
""", """
**Lo que esta clase enseña en COBOL.** COBOL en el navegador suena a broma y no lo es, y merece contarlo
porque el camino es instructivo.

**GnuCOBOL traduce COBOL a C** (clase 123), y **C compila a WebAssembly con Emscripten**. Así que:

```bash
cobc -x -free -C prog.cob             # → prog.c
emcc prog.c libcob.a -o prog.html      # → WebAssembly
```

**Y funciona**: hay demostraciones públicas de GnuCOBOL ejecutándose en el navegador, y proyectos que lo
usan para enseñar COBOL sin instalar nada.

Y merece preguntarse para qué sirve de verdad, porque la respuesta es más interesante que la anécdota:

**Primero, para formación y para pruebas.** Un entorno donde escribir y ejecutar COBOL sin acceso a un
mainframe **resuelve un problema real de una industria con un problema de relevo generacional** (clase
154).

**Segundo, para llevar la lógica de negocio al cliente.** Hay reglas —el cálculo de un interés, la
validación de un IBAN, una tarifa— **que están implementadas en COBOL y validadas durante décadas**, y
que hoy se reimplementan en JavaScript para el navegador, **con el riesgo de que las dos versiones
diverjan** (clase 140).

**Compilar la original a WebAssembly elimina esa duplicación.**

Y ahí está el argumento más serio de esta clase para los lenguajes de esta columna: **WebAssembly permite
reutilizar código validado en sitios donde ese lenguaje no llegaba**.

Y las limitaciones hay que decirlas, y son las del cierre:

| Necesita | ¿Está en WebAssembly? |
|---|---|
| Ficheros indexados VSAM | **no**: hay que emular o llevar los datos a memoria |
| CICS, DB2 | **no**: son el entorno, no el lenguaje |
| Decimal empaquetado | **sí**: es aritmética; GnuCOBOL lo implementa en software |
| Ficheros secuenciales | **sí, con WASI** o con el sistema de ficheros virtual de Emscripten |

**La tercera fila merece destacarse** y conecta con la clase 072: **el decimal exacto de COBOL no
depende del hardware**, así que **se conserva perfectamente** — que es justo lo que hace que valga la
pena portar cálculos financieros y no reescribirlos con `double`.
"""),
        "fortran": ("""
program cuadrado
   implicit none
   integer(kind=8) :: n

   read(*, *) n

   write(*, '(A,I0)') 'resultado=', n * n
end program cuadrado
""", """
**Lo que esta clase enseña en Fortran.** Fortran llega a WebAssembly por el camino que la clase 123
describía: **LLVM**.

```bash
flang-new --target=wasm32-wasi -o prog.wasm prog.f90     # con LLVM Flang
# o el camino histórico:
f2c prog.f && emcc prog.c -lf2c -o prog.js
```

**Flang, el compilador Fortran de LLVM, genera la misma representación intermedia que Clang**, y de ahí
sale WebAssembly.

Y merece explicar por qué esto importa en este dominio, porque el caso de uso es concreto y bueno: **los
modelos de simulación en el navegador**.

```text
Un modelo de dinámica de fluidos, de clima o de estructuras
está escrito en Fortran y validado durante veinte años.

Antes: para enseñarlo o demostrarlo había que instalarlo, o montar un servidor.
Ahora: compila a WebAssembly y se ejecuta en la página, en el cliente.
```

Y hay proyectos reales haciéndolo: **modelos climáticos simplificados, simuladores educativos y
herramientas de ingeniería** que ejecutan el código original en el navegador.

Y las limitaciones de esta columna son las que el cierre de esta clase anuncia, y en Fortran son
específicas:

| Necesidad | Estado en WebAssembly |
|---|---|
| **Aritmética de coma flotante** | **sí, y con IEEE 754 estricto** |
| **Arreglos grandes** | sí, con memoria de 64 bits en propuestas recientes |
| **OpenMP (hilos)** | **parcial**: requiere hilos de WebAssembly y aislamiento cruzado |
| **MPI** | **no**: no hay procesos ni red directa |
| **SIMD y vectorización** | **sí**: WebAssembly tiene SIMD de 128 bits |
| **Entrada y salida de ficheros** | con WASI o con el sistema virtual de Emscripten |

**La cuarta fila es la que limita el uso real**: el cálculo de producción es paralelo y distribuido, y
**eso no cabe en el modelo**.

Así que el papel de WebAssembly en este dominio no es sustituir al clúster: **es llevar el mismo código a
la demostración, a la docencia y al preprocesado en el cliente**.

Y merece señalar una ventaja de esta clase que se pasa por alto y que a Fortran le viene bien: **la
reproducibilidad**.

**WebAssembly especifica la aritmética de coma flotante de forma estricta y determinista** —sin FMA
implícito, sin registros de 80 bits, sin reasociación—, así que **el mismo módulo da exactamente los
mismos bits en cualquier máquina**.

Es lo que la clase 140 buscaba con `-ffp-contract=off` y `MKL_CBWR`, **garantizado por el formato**.
"""),
        "ada": ("""
with Ada.Text_IO;         use Ada.Text_IO;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Strings;
with Ada.Strings.Fixed;

procedure Cuadrado is
   N : Integer;
   R : Long_Long_Integer;
begin
   Get (N);
   R := Long_Long_Integer (N) * Long_Long_Integer (N);

   Put_Line ("resultado=" &
             Ada.Strings.Fixed.Trim (R'Image, Ada.Strings.Both));
end Cuadrado;
""", """
**Lo que esta clase enseña en Ada.** Ada llega a WebAssembly por dos caminos, y merece distinguirlos
porque representan dos filosofías:

**GNAT-LLVM**, que compila Ada a la representación intermedia de LLVM y de ahí a `wasm32-wasi`.

**Y GNAT con la biblioteca de ejecución reducida** —`Light` o `Light-Tasking`, antes llamada ZFP, *zero
footprint*—, que es la que hace esto viable.

Y ahí está el contenido de esta clase para Ada, y merece explicarlo porque es exactamente la pregunta del
"por qué":

```text
La biblioteca de ejecución de Ada incluye:
  - el planificador de tareas
  - el manejo de excepciones con propagación
  - las comprobaciones de restricción
  - la finalización controlada
  - y la entrada y salida

WebAssembly (sin extensiones) no tiene hilos, ni pila secundaria, ni sistema operativo.
```

**Así que Ada completo no cabe; Ada reducido sí.**

Y el perfil reducido es exactamente el que Ada ya usa en sistemas embarcados (clase 146):

```ada
pragma Restrictions (No_Exception_Propagation);
pragma Restrictions (No_Tasking);
pragma Restrictions (No_Allocators);
```

**Y esa es la observación interesante: el subconjunto que hace falta para WebAssembly es el mismo que
Ada lleva cuarenta años usando en satélites.**

No es coincidencia: **un microcontrolador sin sistema operativo y un módulo WebAssembly aislado tienen
las mismas carencias** —sin hilos del sistema, sin sistema de ficheros, sin memoria dinámica ilimitada—
y por eso **los lenguajes que ya sabían funcionar sin sistema operativo llegaron antes**.

Es la razón por la que Rust y C fueron los primeros destinos serios de WebAssembly, y por la que los
lenguajes con recolector tardaron hasta que llegó la propuesta de recolección de basura en 2023.

Y merece cerrar con lo que Ada aporta al modelo de esta clase y que encaja sorprendentemente bien: **el
aislamiento de WebAssembly y las restricciones de Ada persiguen lo mismo por caminos distintos** — que un
componente **no pueda** hacer más de lo que se le permitió.

Uno lo consigue con el sistema de tipos y las restricciones del compilador; el otro, con el formato y el
entorno de ejecución. **Y combinados, dan un componente cuyo comportamiento está acotado por dos vías
independientes**, que es justo lo que un sistema crítico quiere.
"""),
        "pascal": ("""
program Cuadrado;
{$MODE OBJFPC}{$H+}
uses SysUtils;

var
  N: Int64;

begin
  Read(N);
  WriteLn('resultado=', IntToStr(N * N));
end.
""", """
**Lo que esta clase enseña en Pascal.** Free Pascal tiene una sorpresa para esta clase que merece el
titular del gancho: **soporta WebAssembly como destino nativo del compilador**.

```bash
fpc -Twasi -Pwasm32 prog.pas       # ← ¡un destino más, como Win64 o ARM!
```

**No hay Emscripten, ni LLVM, ni traducción a C**: **el generador de código de WebAssembly está dentro de
Free Pascal**, junto a los de x86, ARM, PowerPC, SPARC y los demás.

Y eso encaja con lo que la clase 147 destacaba del compilador: **Free Pascal está escrito en Pascal y
tiene generadores de código propios para cada arquitectura**, así que **añadir WebAssembly fue añadir un
generador más**.

Es una posición poco común: **la mayoría de los lenguajes de esta página llegan a WebAssembly a través de
LLVM o de C**, y Free Pascal llega directamente.

Y las dos variantes que soporta merecen distinguirse porque son las dos formas de usar WebAssembly:

```bash
fpc -Twasi -Pwasm32 prog.pas         # WASI: consola, ficheros, argumentos
fpc -Tembedded -Pwasm32 lib.pas       # módulo puro, para llamar desde JavaScript
```

**El primero produce un programa que se ejecuta con `wasmtime` o `wasmer`**, con entrada y salida
estándar — que es lo que este curso usa.

**Y el segundo produce un módulo sin sistema operativo**, para importar desde una página web y llamar
desde JavaScript.

Y el ecosistema ha construido encima lo que faltaba:

| Pieza | Qué aporta |
|---|---|
| **`wasmtime` / `wasmer`** | ejecutar módulos WASI fuera del navegador |
| **Enlace con JavaScript de FPC** | declarar funciones de JS y exportar las de Pascal |
| **`pas2js`** | **el otro camino: Pascal a JavaScript**, para interfaces |
| **Lazarus + `pas2js`** | aplicaciones web con el mismo código de escritorio |

**`pas2js` merece la mención** porque representa la alternativa histórica: **compilar a JavaScript en vez
de a WebAssembly**.

Y la comparación es la que esta clase debe dejar clara: **a JavaScript se llega antes y se integra mejor
con el navegador; a WebAssembly se llega con más rendimiento y con la semántica exacta del lenguaje
original** —enteros de 64 bits, punteros, aritmética predecible—.

Es el mismo compromiso que la clase 156 planteaba con las FFI: **traducir al idioma del anfitrión o
hablar el propio y pagar la frontera**.
"""),
        "lisp": ("""
(let ((n (read)))
  (format t "resultado=~D~%" (* n n)))
""", """
**Lo que esta clase enseña en Common Lisp.** Lisp es el caso donde la pregunta del "por qué" de esta clase
muerde con más fuerza, y merece explicarlo porque es el argumento central: **Lisp necesita un recolector
de basura, y WebAssembly no tenía uno**.

```text
El modelo original de WebAssembly (2017):
  - memoria lineal: un gran arreglo de bytes
  - sin recolector
  - sin punteros gestionados
  - sin objetos ni estructuras
```

**Así que un lenguaje con recolección tenía que llevar el suyo dentro del módulo**, compilado a
WebAssembly, gestionando su propio montón dentro de la memoria lineal.

Y eso funciona —es lo que hacen las implementaciones de Lisp que llegaron por Emscripten— con dos
costes que merecen enunciarse:

**Uno, el tamaño**: el módulo incluye el recolector, el compilador y toda la biblioteca. Un "hola mundo"
de Lisp en WebAssembly puede ocupar megabytes.

**Y dos, la cooperación**: **el recolector del módulo no ve los objetos de JavaScript y viceversa**, así
que **un ciclo de referencias entre los dos mundos no se recoge nunca** — una fuga estructural.

Y las implementaciones que hoy funcionan:

| Implementación | Camino |
|---|---|
| **ECL** | compila a C, y de ahí con Emscripten |
| **JSCL** | Common Lisp **compilado a JavaScript**, en el navegador |
| **Clasp** | sobre LLVM, con camino a WebAssembly |
| **Hoot (Guile)** | **Scheme a WebAssembly, usando la propuesta de recolección** |

**Hoot merece el detalle** porque es la novedad que cambia esta clase: **la propuesta WasmGC**, aceptada
en 2023 y ya en los navegadores, **añade tipos gestionados y recolección de basura al propio
WebAssembly**.

```text
Con WasmGC, el lenguaje NO lleva su recolector:
  - usa el del entorno, que ya está ahí
  - los objetos son visibles para el recolector del navegador
  - y los ciclos entre módulos y JavaScript SÍ se recogen
```

**Y el resultado es drástico: los módulos pasan de megabytes a decenas de kilobytes.**

Es lo que ha permitido que Java, Kotlin, Dart, Scheme y OCaml lleguen a WebAssembly de forma práctica en
los últimos dos años, y es la respuesta a la pregunta del cierre de esta clase: **lo que el lenguaje
necesitaba y no estaba, acabó añadiéndose al formato**.

Es la historia de todas las máquinas virtuales universales: **empiezan mínimas y crecen hacia los
lenguajes que quieren atraer**.
"""),
        "tcl": ("""
gets stdin linea
set n [string trim $linea]

puts "resultado=[expr {$n * $n}]"
""", """
**Lo que esta clase enseña en Tcl.** Tcl llega a WebAssembly por el camino de Emscripten, y su caso
merece contarse porque **el resultado es especialmente útil**: **un intérprete completo dentro del
navegador**.

```bash
emconfigure ./configure --host=wasm32
emmake make
# → tcl.wasm: el intérprete entero
```

Y la diferencia con los lenguajes compilados de esta página es importante y merece subrayarse:

```text
Fortran o Pascal a WebAssembly:  se compila EL PROGRAMA.
Tcl a WebAssembly:                se compila EL INTÉRPRETE,
                                  y luego ejecuta cualquier guion.
```

**Eso significa que el módulo puede ejecutar código que no existía cuando se compiló** — lo que en el
navegador tiene un uso claro: **entornos interactivos, consolas y demostraciones**.

Es exactamente lo mismo que hacen Pyodide con Python y WebR con R, y es una de las aplicaciones más
exitosas de WebAssembly: **llevar un lenguaje entero, con su ecosistema, a una página web**.

Y esta clase es el sitio para señalar una coincidencia que Tcl ilumina bien: **WebAssembly redescubrió la
arquitectura de Tcl**.

| Idea | Tcl (1988) | WebAssembly (2017) |
|---|---|---|
| Un motor pequeño, incrustable | **el intérprete como biblioteca** (clase 155) | el módulo, con su tiempo de ejecución |
| **Aislamiento por defecto** | **Safe-Tcl** (clase 153) | el módulo no puede hacer nada sin permiso |
| Capacidades concedidas una a una | **los *alias*** de Safe-Tcl | **las importaciones** del módulo |
| Extensible por el anfitrión | comandos nuevos en C | funciones importadas |

**La tercera fila es la coincidencia notable**: **un módulo WebAssembly declara qué funciones importa, y
el anfitrión decide cuáles le da** — que es literalmente el mecanismo de los alias de Safe-Tcl, treinta
años después.

Es la mejor ilustración de la tesis del cierre de esta clase: **lo importante de WebAssembly no es el
rendimiento, es el modelo de seguridad** — y ese modelo es el de capacidades que la clase 153 describía,
adoptado por fin como norma de la industria.

Y **WASI**, la interfaz de sistema de WebAssembly, lo lleva al extremo:

```bash
wasmtime --dir=./datos prog.wasm      # ← solo ve ESE directorio. Nada más.
```

**El módulo recibe un descriptor del directorio permitido y no puede nombrar rutas fuera de él.** Es
seguridad por capacidades aplicada al sistema de ficheros, y es de las pocas veces que un modelo
académicamente correcto ha llegado a la práctica masiva.
"""),
        "perl": ("""
use strict;
use warnings;

my $n = <STDIN>;
chomp $n;

print "resultado=", $n * $n, "\\n";
""", """
**Lo que esta clase enseña en Perl.** Aquí está una de las sorpresas del gancho, y merece contarla porque
es un proyecto notable de una sola persona: **WebPerl**.

**Hauke Dämpfling compiló el intérprete de Perl completo a WebAssembly con Emscripten**, y el resultado
es que **se puede escribir Perl en una página web**:

```html
<script src="webperl.js"></script>
<script type="text/perl">
    use strict; use warnings;
    my @datos = map { $_ * 2 } (1 .. 10);
    js('document')->getElementById('salida')->{innerHTML} = "@datos";
</script>
```

**`<script type="text/perl">` funciona como `type="text/javascript"`**, y **`js(...)` da acceso al DOM
desde Perl**.

Y merece señalar lo que eso implica técnicamente, porque es más de lo que parece: **Perl completo**
—expresiones regulares, referencias, el recolector por conteo, `eval`, los módulos puros de CPAN— **corre
en el navegador**.

Y las limitaciones son exactamente las del cierre de esta clase:

| Necesita Perl | Estado |
|---|---|
| Recolección por conteo de referencias | **sí**: es suya, va dentro del módulo |
| **Módulos XS** (compilados en C) | **no**: habría que compilarlos también |
| `fork`, procesos, señales | **no** |
| Sockets | solo a través de JavaScript |
| Sistema de ficheros | el virtual de Emscripten, en memoria |

**La segunda fila es la que más limita**, y es la misma que afecta a Pyodide con las extensiones de
Python: **el ecosistema de un lenguaje maduro incluye mucho código compilado**, y llevarlo entero
requiere recompilarlo todo.

Y merece extraer la observación general que este caso ilustra mejor que ninguno de esta página:
**WebAssembly no porta lenguajes, porta implementaciones**.

Lo que llega al navegador **no es "Perl": es el intérprete de Perl compilado**, con sus decisiones, sus
dependencias y sus limitaciones.

Y por eso el trabajo real de portar un lenguaje a WebAssembly **no está en el generador de código: está
en la biblioteca de ejecución** —qué hace cuando pide memoria, cuando abre un fichero, cuando crea un
hilo— y en decidir qué se emula, qué se delega al anfitrión y qué simplemente no estará.

Es la misma conclusión que Ada y Lisp en esta página, dicha desde el otro extremo del espectro.
"""),
        "cpp": ("""
#include <iostream>

int main() {
    long long n{};
    if (!(std::cin >> n)) return 1;

    std::cout << "resultado=" << n * n << '\\n';
    return 0;
}
""", """
**Lo que esta clase enseña en C++.** C++ es **el lenguaje con el que nació WebAssembly**, y merece contar
la historia porque explica el diseño del formato.

```text
2011: Alon Zakai escribe EMSCRIPTEN: compila LLVM a JavaScript.
      Funciona, y es lento.
2013: asm.js — un SUBCONJUNTO de JavaScript con anotaciones de tipo,
      que los motores pueden compilar a código nativo directamente.
      El navegador lo ejecuta como JavaScript normal si no lo reconoce.
2015: los cuatro fabricantes de navegadores acuerdan WebAssembly.
2017: soporte en todos los navegadores.
2019: WASI — WebAssembly fuera del navegador.
2023: WasmGC y componentes.
```

**El paso de 2013 es el ingenioso**: asm.js era **JavaScript válido**, así que funcionaba en todas
partes, y **los motores que lo reconocían lo compilaban a nativo**.

Es una técnica de compatibilidad que merece admirarse: **desplegar algo nuevo que degrada limpiamente en
lo viejo**.

Y compilar C++ es directo:

```bash
emcc prog.cpp -O2 -o prog.html                  # navegador, con HTML y JS
emcc prog.cpp -O2 -s WASM=1 -o prog.js           # solo el módulo
clang --target=wasm32-wasi prog.cpp -o prog.wasm  # WASI, sin Emscripten
```

Y los casos de uso reales de C++ en WebAssembly son de los más visibles del ecosistema:

| Aplicación | Qué es |
|---|---|
| **Figma** | editor de diseño; el motor de renderizado en C++ |
| **AutoCAD web** | décadas de C++ llevadas al navegador |
| **Google Earth** | idem |
| **FFmpeg.wasm** | codificación de vídeo en el cliente |
| **SQLite wasm** | base de datos completa en la página |
| **Unity / Unreal** | juegos, con el motor compilado |

**Ese es el argumento económico de esta clase**: **millones de líneas de C++ validado que antes solo
funcionaban instaladas, funcionan ahora en una pestaña**.

Y las limitaciones que C++ encuentra merecen decirse porque son las del cierre:

```text
- Las excepciones costaban mucho; ahora hay una propuesta nativa
- Los hilos requieren SharedArrayBuffer y cabeceras de aislamiento cruzado
- No hay JIT dentro del módulo: nada de generar código en marcha
- El tamaño del módulo importa: hay que descargarlo
```

**La segunda merece la advertencia práctica**: **`std::thread` funciona en WebAssembly solo si el
servidor envía las cabeceras COOP y COEP**, y muchos no las envían — con lo que un programa que compila
falla al arrancar en producción.

Es un buen recordatorio de que **el destino de compilación trae su propio contrato con el entorno**, y de
que conviene leerlo antes de prometer nada.
"""),
        "rpg": ("""
**free
ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-pi CUADRADO;
  n int(10) const;
end-pi;

dcl-s r int(20);

r = n * n;

dsply ('resultado=' + %char(r));

*inlr = *on;
return;
""", """
**Lo que esta clase enseña en RPG.** RPG **no compila a WebAssembly**, y merece explicar por qué, porque
la razón es exactamente la del cierre de esta clase y es más interesante que la lista de los que sí.

```text
RPG no es solo un lenguaje: es un lenguaje ATADO a una plataforma.

Un programa RPG usa:
  - ficheros de la base de datos integrada, con acceso por clave
  - la lista de bibliotecas para resolver nombres (clase 148)
  - grupos de activación y el manejo de condiciones de ILE (clase 157)
  - punteros de 16 bytes con etiqueta por hardware (clase 153)
  - y ficheros de pantalla 5250
```

**Nada de eso existe fuera de IBM i.** Un "RPG a WebAssembly" tendría que llevar consigo medio sistema
operativo.

Y esa es la observación que merece extraerse y que vale para muchos lenguajes: **la portabilidad de un
lenguaje no depende de su sintaxis, sino de cuánto de su semántica está en la plataforma**.

C es portable porque supone muy poco. RPG no lo es porque supone mucho — **y eso mismo es lo que lo hace
productivo en su plataforma** (clases 142 y 148).

Y aun así, la plataforma sí participa del mundo de WebAssembly por otra vía, y merece nombrarla:

```text
En PASE (el entorno AIX dentro de IBM i) se pueden ejecutar:
   - Node.js, y por tanto módulos WebAssembly
   - Python, con wasmtime
   - y runtimes de WebAssembly compilados para POWER
```

**Así que IBM i puede EJECUTAR WebAssembly aunque RPG no compile a él** — y ese reparto tiene sentido con
la arquitectura de la clase 149: **la lógica de negocio en RPG, y los componentes portables de terceros
como módulos aislados**.

Y merece cerrar con lo que sí se está haciendo en esta plataforma y que persigue el mismo objetivo que
esta clase: **exponer la lógica como API** (clase 160) **y consumirla desde donde sea**.

Es la alternativa a portar el código: **no mover la lógica, mover la frontera**. Y para un sistema que
funciona, está validado y no se puede parar, suele ser la decisión correcta — que es la misma conclusión
que la clase 150 alcanzaba sobre las reescrituras.
"""),
        "pli": ("""
 cuadrado: procedure options(main);

    declare n fixed binary(31);
    declare r fixed binary(63);

    get list (n);
    r = n * n;

    put skip list ('resultado=' || trim(char(r)));

 end cuadrado;
""", """
**Lo que esta clase enseña en PL/I.** PL/I comparte el diagnóstico de RPG en esta página —**no hay un
compilador a WebAssembly**— y por razones que merecen distinguirse, porque no son las mismas.

**RPG no llega porque su semántica está en la plataforma. PL/I no llega porque no hay quien lo lleve.**

```text
Los compiladores de PL/I en producción son:
  - IBM Enterprise PL/I para z/OS      (propietario)
  - IBM PL/I para AIX / Windows         (propietario)
  - Iron Spring PL/I                     (subconjunto, para OS/2 y Linux)

No hay ningún compilador de PL/I sobre LLVM ni sobre GCC con soporte activo.
```

**Y sin una interfaz con LLVM, no hay camino a WebAssembly** — porque casi todos los destinos nuevos
llegan por ahí (clase 123).

Y merece extraer la lección, porque es de las más importantes de este curso y aparece aquí con claridad:
**la supervivencia de un lenguaje depende de que alguien mantenga una implementación libre**.

Compárese con los demás de esta página:

| Lenguaje | Implementación libre | ¿Llega a destinos nuevos? |
|---|---|---|
| COBOL | **GnuCOBOL** | sí, vía C |
| Fortran | **gfortran, LLVM Flang** | sí |
| Ada | **GNAT (FSF)** | sí, vía GCC y LLVM |
| Pascal | **Free Pascal** | **sí, con generador propio** |
| Lisp | **SBCL, ECL, Clasp** | sí |
| Tcl, Perl, C++ | libres | sí |
| **PL/I** | **no** | **no** |
| **RPG** | no | no |

**Las dos últimas filas son las únicas de esta página sin implementación libre**, y son las dos que se
quedan fuera de cada plataforma nueva.

Es una observación de fondo sobre el ecosistema del software: **un lenguaje sin implementación libre
depende, para cada plataforma nueva, de que su propietario decida invertir** — y esa decisión se toma
mirando el mercado, no la técnica.

Y por eso el destino de PL/I está donde está: **millones de líneas en producción, funcionando
perfectamente, en una plataforma concreta y sin camino de salida más allá de la traducción a otro
lenguaje** — que es lo que la clase 150 llamaba el patrón del estrangulador, aplicado a un lenguaje
entero.
"""),
        "mumps": ("""
CUADRADO ; Elevar al cuadrado -- clase 162
 read n
 write "resultado=", n * n, !
 quit
""", """
**Lo que esta clase enseña en M.** M sí llega a WebAssembly, y por el camino que su implementación libre
permite: **YottaDB está escrito en C, y C compila a WebAssembly**.

**Y hay algo más interesante que merece contarse**: existen **intérpretes de M escritos para el
navegador**, y **Mumps.js** y proyectos similares permiten ejecutar rutinas M en una página.

Pero la parte sustancial de esta clase para M es otra, y merece explicarla porque toca el problema real
de este ecosistema: **el motor de base de datos no cabe en el modelo**.

```text
Un sistema M no es un intérprete: es un intérprete MÁS una base de datos
con transacciones, bloqueos, diario y memoria compartida entre procesos.

WebAssembly (sin extensiones) no tiene:
  - memoria compartida entre módulos
  - ficheros mapeados
  - bloqueos entre procesos
  - ni procesos
```

**Así que lo que puede llegar al navegador es un M de un solo proceso, con la base en memoria** — útil
para docencia y para demostraciones, no para un hospital.

Y esta clase es el sitio para señalar dónde WebAssembly sí encaja bien con este mundo, y es una idea que
merece destacarse: **como formato de extensión segura**.

```text
Un sistema clínico necesita ejecutar reglas escritas por el hospital:
  cálculos de dosis, alertas, validaciones locales.

Hoy eso se hace con código M dentro del diccionario de datos (clase 151),
que es ejecución de código arbitrario con todos los permisos (clase 153).

Un módulo WebAssembly haría lo mismo con AISLAMIENTO:
  - solo puede llamar a las funciones que se le den
  - no puede tocar globals que no se le pasen
  - y el consumo de CPU y memoria se puede acotar
```

**Eso es el modelo de capacidades del cierre de esta clase aplicado exactamente donde hace falta**, y es
lo que ya hacen sistemas modernos con complementos: **Envoy, Istio y varias bases de datos ejecutan
extensiones de usuario como módulos WebAssembly precisamente por eso**.

Y merece cerrar con la observación general que este caso ilustra: **el uso más valioso de WebAssembly no
es portar lenguajes viejos a la web — es ejecutar código de terceros con garantías**.

La portabilidad es lo llamativo; **el aislamiento es lo que resuelve un problema que no tenía solución
buena**.
"""),
        "smalltalk": ("""
| n |

n := stdin nextLine trimBoth asNumber.

Transcript show: 'resultado=', (n * n) printString; cr.
""", """
**Lo que esta clase enseña en Smalltalk.** Smalltalk tiene, para esta clase, la observación más
irónica de toda la página, y merece decirla claramente: **Smalltalk lleva haciendo esto desde 1980**.

```text
Smalltalk-80 ya tenía:
  - un formato de BYTECODE portátil (clase 125)
  - una máquina virtual pequeña, portable a cualquier hardware
  - una IMAGEN que se ejecuta igual en cualquier plataforma
  - y aislamiento: el código no puede tocar memoria arbitraria (clase 129)
```

**Es, punto por punto, la lista de propiedades de WebAssembly** — cuarenta años antes.

Y esta clase permite ver la genealogía completa de la idea, que merece ordenarse:

| Año | Sistema | Qué aportó |
|---|---|---|
| 1966 | **O-code** (BCPL) | bytecode portátil |
| 1970 | **P-code** (Pascal) | **el compilador se portaba escribiendo un intérprete** |
| **1980** | **Smalltalk-80** | bytecode + imagen + VM portable |
| 1995 | **JVM** | bytecode con verificación y **seguridad** |
| 2002 | **CLR (.NET)** | bytecode **multi-lenguaje** desde el diseño |
| 2013 | **asm.js** | subconjunto de JavaScript compilable |
| **2017** | **WebAssembly** | binario, verificado, aislado, multi-lenguaje |

**El P-code de Pascal merece destacarse** porque su idea era la misma de esta clase y funcionó: **para
llevar Pascal a una máquina nueva bastaba con escribir un intérprete de P-code**, y así se extendió el
lenguaje por decenas de arquitecturas en los años setenta.

Y Smalltalk llega hoy a WebAssembly por varios caminos:

| Proyecto | Qué es |
|---|---|
| **SqueakJS** | **la máquina virtual de Squeak en JavaScript**: ejecuta imágenes reales de 1998 |
| **Squeak/Pharo con Emscripten** | la VM compilada a WebAssembly |
| **PharoJS** | traduce código Pharo a JavaScript |

**SqueakJS merece el cierre**, porque demuestra algo de esta clase de forma contundente: **puede cargar y
ejecutar en el navegador una imagen de Smalltalk-80 de 1978**, restaurada, **con su interfaz original
funcionando**.

**Cuarenta y ocho años de compatibilidad binaria, en una pestaña.**

Y esa es la mejor conclusión de esta clase y de la Parte 10 entera: **el bytecode portátil no es una idea
nueva, y lo que WebAssembly ha aportado no es la técnica sino el acuerdo**.

Lo difícil nunca fue definir un formato intermedio —hay decenas— sino **conseguir que todos los
fabricantes implementaran el mismo**. Y eso, que es un problema de coordinación y no de ingeniería, es lo
que había impedido durante cuarenta años que la idea de Smalltalk se convirtiera en la infraestructura de
todos.
"""),
    },
)
