# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 161

> [⬅️ Volver a la clase 161](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Sumar lo que llega por la entrada estándar. Es literalmente lo que hace todo programa de este curso
(clase 040), y esta clase explica por qué esa elección no es casual: **la entrada y la salida estándar
son la frontera entre lenguajes más simple, más portable y más antigua que existe**. Y detrás hay una
frase que cambió la informática: **Doug McIlroy propuso las tuberías de Unix en 1964 con la idea de
"conectar programas como mangueras de jardín"**, y se implementaron en 1973.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es la **comunicación entre procesos**, y estos lenguajes la enseñan porque **cubren
> todas las formas que existen**: **ficheros temporales entre pasos** (COBOL con JCL), **paso de mensajes
> entre miles de procesos** (Fortran con MPI), **la cita entre tareas** (Ada), **colas persistentes**
> (RPG y MQ), **la base de datos como canal** (M) y **los sockets con bucle de eventos** (Tcl, Perl,
> C++).
>
> Y aparecen los tres ejes que ordenan cualquier decisión: **¿mismo proceso o procesos separados?
> ¿Síncrono o asíncrono? ¿Se pierde el mensaje si el receptor no está?**
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con enteros separados por espacio (mensajes en la cola) → stdout: `recibido=<suma de los mensajes>`
- **Regla:** `sumar los mensajes recibidos en orden`

| stdin | esperado |
|---|---|
| `1 2 3` | `recibido=6` |
| `5` | `recibido=5` |
| `10 20 30 40` | `recibido=100` |

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
```

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

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
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
```

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

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
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
```

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

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
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
```

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

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((total 0))
  (with-input-from-string (s (read-line))
    (loop for valor = (read s nil nil)
          while valor
          do (incf total valor)))
  (format t "recibido=~D~%" total))
```

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

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea

set total 0
foreach v [split [string trim $linea]] {
    if {$v ne ""} { incr total $v }
}

puts "recibido=$total"
```

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

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;
use List::Util qw(sum0);

my $linea = <STDIN>;
chomp $linea;

print "recibido=", sum0(split ' ', $linea), "\n";
```

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
open3(\*ESCRIBIR, \*LEER, \*ERRORES, @comando);   # las TRES a la vez

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
run \@comando, \$entrada, \$salida, \$errores;   # correcto, sin pensar
```

Y merece cerrar con la observación práctica de esta clase: **la lista de argumentos, nunca la cadena**.

```perl
system("rm $fichero");            # ✗ inyección de comandos (clase 153)
system('rm', '--', $fichero);      # ✓ sin intérprete de órdenes de por medio
```

**Con lista, no hay `sh` en medio**, así que un nombre de fichero con `;` o con espacios **no puede
ejecutar nada**.

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>

int main() {
    long long total = 0, valor = 0;
    while (std::cin >> valor) total += valor;

    std::cout << "recibido=" << total << '\n';
    return 0;
}
```

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
```

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

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
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
```

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

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
RECIBIR ; Sumar lo recibido -- clase 161
 read linea
 new i, total, n
 set total = 0
 for i = 1:1:$length(linea, " ") do
 . set n = $piece(linea, " ", i)
 . if n '= "" set total = total + n
 write "recibido=", total, !
 quit
```

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

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| linea total |

linea := stdin nextLine trimBoth.
total := 0.

(linea substrings: ' ') do: [ :p | total := total + p asNumber ].

Transcript show: 'recibido=', total printString; cr.
```

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

---

## Y de vuelta a la clase

Lo transferible: **elegir un mecanismo de comunicación es elegir qué pasa cuando el otro lado no está**.
Una llamada de función supone que está; una tubería, que arranca a la vez; un socket, que está ahora
mismo; **una cola persistente, que llegará algún día** — y esa última es la única que sobrevive a un
reinicio. De ahí la regla que evita los peores diseños: **empezar por el modo de fallo, no por el
rendimiento**. Y la segunda, que ahorra mucho trabajo: **texto por la entrada y la salida estándar es
suficiente sorprendentemente a menudo**, y es la única frontera que funciona igual en los doce
lenguajes de esta página.

⏮️ [Volver a la clase 161](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
