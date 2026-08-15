# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase 135

> [⬅️ Volver a la clase 135](README.md) · [🧬 Primos del Atlas](primos.md) ·
> [🧟 Índice de lenguajes vivos](../../../atlas/vivos.md) · [📚 Índice](../../README.md)

Sumar una lista repartiendo el trabajo. El modelo de actores —procesos aislados que solo se comunican
por mensajes— lo formuló **Carl Hewitt en 1973, en el MIT y sobre Lisp**, y su implementación más
famosa es Erlang. Y aquí hay tres sistemas que llevan décadas haciendo exactamente eso sin llamarlo
así: **COBOL bajo CICS, RPG con colas de datos y M con procesos sobre *globals***.

> **🎯 Estos lenguajes no están aquí por ser antiguos**
>
> El criterio es doble y se declara en la [ficha de cada uno](../../../atlas/vivos.md):
> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a
> la vista un concepto que los diez del núcleo esconden**.
>
> Aquí el concepto es **la unidad aislada que solo se comunica por mensajes**, y estos lenguajes lo
> enseñan porque muestran que el modelo se descubrió dos veces. **En la academia**: Hewitt en Lisp
> (1973), Milner con CSP y Hoare, y de ahí Erlang (1986) y el modelo BEAM. **Y en la industria**: los
> monitores transaccionales de IBM, que en 1969 ya ejecutaban miles de tareas aisladas que se
> comunicaban por colas.
>
> Y **Smalltalk** aporta el eslabón: Alan Kay decía que lo importante de los objetos **era el paso de
> mensajes** (clase 110), y Hewitt formuló los actores inspirándose en Smalltalk y en Simula.
>
> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,
> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.

## El contrato, igual para todos

- **Entrada / salida:** stdin: una línea con enteros separados por espacio → stdout: `total=<suma de todos>`
- **Regla:** `cada número es un mensaje al actor; el actor acumula`

| stdin | esperado |
|---|---|
| `1 2 3` | `total=6` |
| `5` | `total=5` |
| `10 20` | `total=30` |

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
```

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

### Fortran

[Ficha completa](../../../atlas/fortran.md) · HPC, clima, física, BLAS/LAPACK · `gfortran -O2 prog.f90`

```fortran
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
```

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

### Ada

[Ficha completa](../../../atlas/ada.md) · Aviónica, espacio, ferrocarril, defensa · `gnatmake prog.adb`

```ada
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
```

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

### Pascal

[Ficha completa](../../../atlas/pascal.md) · Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal) · `fpc -Mobjfpc prog.pas`

```pascal
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
```

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

### Common Lisp

[Ficha completa](../../../atlas/common-lisp.md) · IA simbólica, CAD, investigación · `sbcl --script prog.lisp`

```lisp
(let ((total 0))
  (loop for x = (read *standard-input* nil nil)
        while x
        do (incf total x))
  (format t "total=~D~%" total))
```

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

### Tcl

[Ficha completa](../../../atlas/tcl.md) · Diseño de chips (EDA), redes, testing · `tclsh prog.tcl`

```tcl
gets stdin linea

set total 0
foreach x [split [string trim $linea]] {
    incr total $x
}

puts "total=$total"
```

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

### Perl

[Ficha completa](../../../atlas/perl.md) · Sysadmin, texto, bioinformática · `perl prog.pl`

```perl
use strict;
use warnings;
use List::Util qw(sum0);

my $linea = <STDIN>;
chomp $linea;

print "total=", sum0(split ' ', $linea), "\n";
```

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
    $pm->finish(0, \$parcial);              # ENVIAR el resultado al padre
}
$pm->wait_all_children;
```

**`$pm->finish(0, \$parcial)` envía datos del hijo al padre**, serializándolos por una tubería. Es un
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

### C++

[Ficha completa](../../../atlas/cpp.md) · Videojuegos, navegadores, finanzas, HPC · `g++ -std=c++17 prog.cpp`

```cpp
#include <iostream>
#include <iterator>
#include <numeric>
#include <vector>

int main() {
    const std::vector<int> v{std::istream_iterator<int>(std::cin),
                             std::istream_iterator<int>()};

    std::cout << "total=" << std::accumulate(v.begin(), v.end(), 0) << '\n';
    return 0;
}
```

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
```

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

---

## ⚪ Correctos, sin sello de máquina

Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI.

### PL/I

[Ficha completa](../../../atlas/pl-i.md) · Mainframe z/OS: banca, seguros · `IBM Enterprise PL/I for z/OS`

```pli
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
```

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

### M / MUMPS

[Ficha completa](../../../atlas/mumps.md) · Sanidad: historia clínica, VistA, Epic · `YottaDB`

```mumps
ACTORES ; Actores y paso de mensajes -- clase 135
 read linea
 set total = 0
 for i=1:1:$length(linea, " ") set total = total + $piece(linea, " ", i)
 write "total=", total, !
 quit
```

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

### Smalltalk

[Ficha completa](../../../atlas/smalltalk.md) · Banca, seguros, trading · `Pharo`

```smalltalk
| v |

v := stdin nextLine substrings collect: [ :cada | cada asNumber ].

Transcript
    show: 'total=', (v inject: 0 into: [ :a :b | a + b ]) printString;
    cr.
```

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

---

## Y de vuelta a la clase

Lo transferible: **el modelo de actores no es una técnica de concurrencia, es una decisión sobre los
fallos**. Si nada se comparte, un actor puede morir sin corromper a los demás, y otro puede
reiniciarlo — que es la idea de los árboles de supervisión de Erlang y su famoso "déjalo fallar". Los
sistemas transaccionales llegaron a lo mismo por el mismo camino: **una transacción que falla se
deshace sola y no arrastra a las demás**. Cuando el aislamiento es la prioridad, este modelo aparece
solo.

⏮️ [Volver a la clase 135](README.md) · 🧬 [Los primos del Atlas](primos.md) ·
🧟 [Índice de lenguajes vivos](../../../atlas/vivos.md)
